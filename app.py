#!/usr/bin/env python
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from linebot.exceptions import(InvalidSignatureError)
import os

app = Flask(__name__)

#get env variable
# Lineの情報を格納
# 自分の発行したトークンを入れる
YOUR_CHANNEL_ACCESS_TOKEN = 'qivpsoFG7viTFV/yCe6ji9qeaMJDXO4lb2DWSNFii7/Tz/nkKU4FyeEXcyz7TT4tqmSWyaXx5gxi1V4cdLOZyI7KhAFX+5VbEj/rdzSXxWYi7KbvL9t2cIIRl9UCVEAiA/WAyPyJ2NDJtc9w5R9IbgdB04t89/1O/w1cDnyilFU='
YOUR_CHANNEL_SECRET       = '593354068bbc3c108f4e52e180811af6' # 自分のSECRET
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# 変更：テストのルーティング
@app.route('/test')
def test():
    return 'test'

# callbackのルーティングでユーザーからの文字列を受信（ここは基本的に変更しない）
@app.route('/callback',methods=['POST'])
def callback():
    #get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    #get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    #handle webhook body
    try :
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# リプライ（自由に変更可）
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# おまじない
if __name__ == '__main__':
    app.run()
