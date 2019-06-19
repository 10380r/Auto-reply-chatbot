#!/usr/bin/env python
import pya3rt
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from os.path import join, dirname
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(join(dirname(__file__), '.env'))

line_bot_api = LineBotApi(os.environ.get('LINE_TOKEN'))
handler      = WebhookHandler(os.environ.get('LINE_SECRT'))
client       = pya3rt.TalkClient(os.environ.get('A3RT_KEY'))

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
