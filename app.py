#!/usr/bin/env python
import pya3rt
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

with open('keys.txt', 'r') as f:
    keys_list = f.readlines()
    line_token  = keys_list[0].replace('\n','')
    line_secret = keys_list[1].replace('\n','')
    a3rt_key    = keys_list[2].replace('\n','')

line_bot_api = LineBotApi(line_token)
handler      = WebhookHandler(line_secret)
client       = pya3rt.TalkClient(a3rt_key)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = get_reply(client, event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

def get_reply(client, text):
    response = client.talk(text)
    reply = ((response['results'])[0])['reply']
    return reply

if __name__ == "__main__":
    app.run()
