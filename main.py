from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
from bs4 import BeautifulSoup

# FastAPI setup
app = FastAPI()

# Set up Jinja2 for templating
templates = Jinja2Templates(directory="templates")

# Custom headers for the requests
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://eduboom.it/',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

def get_m3u8(temp_url):
    response = requests.get(temp_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    data_params = soup.find('div', class_='ucha-player play-button')['data-params']
    real_data = json.loads(data_params)
    m3u8_link = real_data['sources']['main']['smil']
    if "smil:trailer" in m3u8_link:
        m3u8_link = m3u8_link.replace("smil:trailers", "smil:videos").replace("/registration", "")
    return m3u8_link

def eduboom(query):
    params = {'term': query}
    response = requests.get('https://eduboom.it/ajax/lessons-search', params=params, headers=headers)
    data = response.json()
    return data

@app.get("/", response_class=HTMLResponse)
async def search_form(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_results(request: Request, query: str = Form(...)):
    results = eduboom(query)
    return templates.TemplateResponse("results.html", {"request": request, "results": results, "query": query})

@app.get("/video/{video_id}", response_class=HTMLResponse)
async def video_details(request: Request, video_id: int, query: str):
    results = eduboom(query)
    selected_item = results[video_id - 1]
    link = selected_item['url']
    m3u8_link = get_m3u8(link)
    return templates.TemplateResponse("detail.html", {
        "request": request,
        "name": selected_item['value'],
        "category": selected_item['category'],
        "grade": selected_item['grade'],
        "m3u8_link": m3u8_link
    })
