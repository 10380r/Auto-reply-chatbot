# a3rtをで値を取得するプロトタイプ
import pya3rt

with open('keys.txt','r') as f:
    keys = f.readlines()
    apikey = keys[2]

client = pya3rt.TalkClient(apikey)
results = client.talk("おはよう")
print(results)
