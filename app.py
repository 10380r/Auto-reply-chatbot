#!/usr/bin/env python
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

line_bot_api = LineBotApi('H/Vecj2Nvdnu7q/NOckQNQpc+jDzZjfOHxw03qmMop8lgANncs01xwVcrQet2Q8KqmSWyaXx5gxi1V4cdLOZyI7KhAFX+5VbEj/rdzSXxWZ6BVt3ZPBaXZl8v57FTrrZugLX9GNhaG/7cUt0Q2sZwwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('593354068bbc3c108f4e52e180811af6')

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
