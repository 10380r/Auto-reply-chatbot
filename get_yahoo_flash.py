import urllib
from bs4 import BeautifulSoup

# urlを変数に格納する
url = 'https://news.yahoo.co.jp/flash'
# urlに対してリクエストを送り、レスポンスの情報を変数に格納する
res = urllib.request.urlopen(url)
# beautifulsoupを使用して、レスポンスの情報を格納する
soup = BeautifulSoup(res)

div  = soup.find('div', 'articleList lastCon')
dts  = div.findAll('dt', 'titl')

for dt in dts:
    print(dt.text.replace(' ','').replace('\n',''))
