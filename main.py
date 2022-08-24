import requests

URL = 'https://pass.rw.by/ru/route/?from=%D0%93%D0%BE%D0%BC%D0%B5%D0%BB%D1%8C&from_esr=&from_exp=&to=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA&to_esr=&to_exp=&date=2022-08-25'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/104.0.0.0 Safari/537.36',
           'accept': '*/*'}

html = requests.get(URL, headers=HEADERS)
print(html.status_code)
print(html.text)