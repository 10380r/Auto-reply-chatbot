## Step1 

### Webフレームワークを使用してみる
- Flask
当講義ではpythonのWebフレームワークであるFlaskを利用してWeb開発の基礎を勉強します。  

- Webとはなにか？
  ざっくり説明をすると **Webページはただ閲覧するものではなく、ユーザーが利用するアプリケーションとなった**アプリケーションの処理、面倒なページの自動作成をするシステムをプログラミングしている。というところがWeb作成にプログラミングを利用する理由です。

### 実際に画面に出力させてみましょう
まずは、 **"Hello World"をWebページに出力する"**ことから始めましょう。  
実行ができるように写経を行い、その後にコードを解説していきます。  

### プロジェクトのフォルダを作成
webを開発する上でのファイルをまとめるフォルダを作ります  
`$ mkdir flask-project` ($ マークはターミナルで実行するコマンドを表す記号でよく使います。)  

#### アプリファイルの作成
Flaskを利用したPythonプログラムをフォルダ内に記述する。
名前は `app.py` とします。

```python
# flaskのインポート
from flask import Flask

# インスタンスの作成
app = Flask(__name__)

# ルーティング
@app.route('/')
def hello():
    name = "Hello World"
        return name

# おまじない（気になる方はご自分で調べてください。）
if __name__ == "__main__":
      app.run()
```
おまじないに関して(講義では割愛します)  
--> http://blog.pyq.jp/entry/Python_kaiketsu_180207

### Flaskサーバーの起動
いよいよFlaskサーバーを起動させます。 起動のさせ方はapp.pyを実行するだけです。 flask-projectのフォルダ内にいる状態で  
`$ python app.py`  
を実行すると  
` * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`  
と出力されます。  
http://127.0.0.1:5000/
にアクセスてみましょう。  

### ルーティングの指定
ルーティングとは指定したURLによってレスポンスを制御する機能のことです。  
上のコードでは８行目の@app.route('/')がルーティングの部分です。  
では新しく `foo` というURLをルーティングで作成してみます。  

```python
# flaskのインポート
from flask import Flask

# インスタンスの作成
app = Flask(__name__)

# ルーティング
@app.route('/')
def hello():
    name = "Hello World"
    return name
    
@app.route('/foo')
def foo():
    return '😇'
    
# おまじない
if __name__ == "__main__":
    app.run()
```
そのあと先ほどと同様にサーバーを立ち上げ、http://127.0.0.1:5000/foo にアクセスしてみましょう。

### <p style='color:red'>演習</p>
`app.py`に`test` というURLを作成し、任意の文字が表示されるようにルーティングをしてみましょう。

### HTMLファイルを返す
今回チャットボットには使用しませんが、これが一般的な使用の仕方です。
今までは指定したURLにアクセスしたら文字列が返されました。  
通常はWebサイトでは事前にHTMLファイルを用意してそれを指定したURLに設置しています。  
Flaskでは任意のHTMLをレンダリング（返す）関数が提供されております。  

これから作成するファイル構造は以下の通り  
```
.
│──app.py
└ ──templates
    └ ─index.html
```

まずはHTMLファイルを`index.html`として準備しましょう

-HTML-
```html
<!DOCTYPE HTML>
<html>
<head>
    <title>Sample Page</title>
</head>
<body>
    <h1>Hello, Flask</h1>
    <h2>This is HTML file</h2>
</body>
</html>
```

-Python-
```python
# flaskのインポート
from flask import Flask
# htmlファイルをレンダリングするためのライブラリ
from flask import render_template

# インスタンスの作成
app = Flask(__name__)

# ルーティング
@app.route('/')
def hello():
    name = "Hello World"
    return name

@app.route('/html')
def html():
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
```

サーバーを立ち上げ、 http://127.0.0.1:5000/html にアクセスしてみましょう。

## Step2 実際にLINEのMessaging APIを使用してみる
必要な設定やツール  
- LINEアカウント  
- ngrok (ローカルサーバを立てて、URLを発行してくれる)  

### Macを使用してる方はHomebrewからのインストールをオススメします。
- Homebrewのインストールがまだの方  
  `$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`  
  ターミナルに上記コマンドを入力することで、Homebrewを導入することができます  
- ngrokのインストール  
  `$ brew cask install ngrok`  

### 手続き
https://developers.line.biz/jp/  
にアクセスして、Developerとして登録  
チャンネル基本設定
- Webhook URLにngrokで発行したURLを入力(発行の仕方に関しては後述)
  - その際、 `[乱数].ngrok.io/callback` に書き換え  
- Webhook送信：`利用する`に変更
- 自動応答メッセージ：`利用しない`に変更

lineの開発チームが公式で「おうむ返し」のスクリプトを提示しているので、まずはそれを使用して開発してきます。
https://github.com/line/line-bot-sdk-python
[公式ドキュメンツ](https://developers.line.biz/ja/reference/messaging-api/)

### ライブラリのインストール
`$ pip install line-bot-sdk`

### 該当スクリプト
そのままコピペしても、実際に写経しても構いません。

```python
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

line_bot_api = LineBotApi('Messaging APIで発行したトークン')
handler = WebhookHandler('Messaging APIのsecret')

# 変更：テストのルーティング
@app.route('/test')
def test():
    return 'test'

# Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # get request body as text
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)

    # handleの処理を終えればOK
    return 'OK'

#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

# おまじない
if __name__ == "__main__":
    app.run()
```

### ngrokでURL発行
- ターミナルをもう1画面出す 
  Macだと `⌘ + N` で新規画面を出せます。
- ターミナルにて`$ ngrok http 5000` と入力
  すると

```
ngrok by @inconshreveable
(Ctrl+C to quit)

Session Status                online
Session Expires               7 hours, 59 minutes
Version                       2.3.25
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://b1acd61c.ngrok.io -> http://localhost:5000
Forwarding                    https://b1acd61c.ngrok.io -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

といった様な画面になるかと思います。

`Forwarding` という欄が実際に発行されたURLになります。  
そこのURLをコピーし、チャンネル基本設定のWebhookURLの欄に格納してください。  
**URLの末尾に`/callback/`をつけるのを忘れずに**  

### プログラムの実行
- `$ python app.py`
- 今までのプログラムが問題なく書けていると、おうむ返しのbotが完成すると思います。

## a3rt APIを使用して、機械学習要素を導入する
### What is a3rt
リクルートが出している無料で使用できる機械学習系のAPIです  
https://a3rt.recruit-tech.co.jp/  
様々なAPIがありますが、今回は `Talk API` を使用します。Keyを発行しましょう。

### まずはコンソール上で会話できるスクリプトを作成してみる
サンプルコード
`talk.py`
```python
# -*- coding: utf-8 -*-
import pya3rt

apikey = "YOUR_API_KEY"
client = pya3rt.TalkClient(apikey)

results = client.talk("おはよう")
print(results)
```

#### 実行
`$ python talk.py`
すると、
```
{'status': 0, 'message': 'ok', 'results': [{'perplexity': 0.07743213382788067, 'reply': 'おはようございます'}]}
```
という様な結果が返ってくるかと思います。  
この変数`results`は、Pythonの辞書なので、うまく処理することで任意の値のみを得ることができます。  

#### プチ演習
任意の値を取り出してみましょう

### 最終ミッション
#### 演習
上記プログラム二つを組み合わせて、対話ボットを作りましょう。

