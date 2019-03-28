#!/usr/bin/env python
import pya3rt
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

with open('keys.txt', 'r') as f:
    keys_list = f.readlines()
    line_token  = keys_list[0]
    line_secret = keys_list[1]
    a3rt_key    = keys_list[2]

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

    print('callback through')
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(client)
    reply = get_reply(client, event.message.text)
    print(reply)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def get_reply(client, text):
    print('im in get reply')
    response = client.talk(text)
    reply = ((response['results'])[0])['reply']
    return reply

if __name__ == "__main__":
    app.run()
