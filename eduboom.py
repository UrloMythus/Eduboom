import requests
import json
from bs4 import BeautifulSoup
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://eduboom.it/',
    # 'Cookie': 'PHPSESSID=ibmi18fulfuhve42sq49tbkkme',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}


def get_m3u8(temp_url):
    response = requests.get(temp_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data_params = soup.find('div', class_='ucha-player play-button')['data-params']
    real_data = json.loads(data_params)
    m3u8_link = real_data['sources']['main']['smil']
    if "smil:trailer" in m3u8_link:
        m3u8_link = m3u8_link.replace("smil:trailers","smil:videos").replace("/registration","")
        print("Found .m3u8 link:", m3u8_link)
        return m3u8_link



def eduboom(query):
    try:
        params = {
            'term': query,
        }
        response = requests.get('https://eduboom.it/ajax/lessons-search', params=params, headers=headers)
        data = response.json()
        i = 0
        for item in data:
            i = i + 1
            name = item['value']
            category = item['category']
            grade = item['grade']
            print("ID:",i,"Name:",name,"Category:",category,"Grade:",grade)
        user_input = int(input("Enter the id of the video you want to watch: "))
        selected_item = data[user_input-1]
        link = selected_item['url']
        m3u8_link = get_m3u8(link)
        return m3u8_link

    except Exception as e:
        print("Nothing",e)
        return None
    

a = eduboom("Parini")
