# a3rtをで値を取得するプロトタイプ
import pya3rt

with open('keys.txt','r') as f:
    keys = f.readlines()
    apikey = keys[2].replace('\n', '')

while True:
    client = pya3rt.TalkClient(apikey)
    results = client.talk(input(''))
    print('>',results['results'][0]['reply'])
