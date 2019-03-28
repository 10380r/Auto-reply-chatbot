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

## Step2
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

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    # X-Line-Signature:各リクエストに発行されるID
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
```
