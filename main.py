from bs4 import BeautifulSoup
import requests
import csv
# from pprint import pprint as pp
# from datetime import datetime

CSV = 'kivano_note.csv'
HOST = 'https://www.kivano.kg/'
URL = 'https://www.kivano.kg/noutbuki'
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

def get_html(url, params = ''):
    response = requests.get(URL, params = params, headers=HEADERS, verify=False)
    return response

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('div', class_='item product_listbox oh')
    comps = []

    for item in items:
        comps.append({
            'title' : item.find('div', class_='listbox_title oh').find('a').get_text(strip=True),
            'price' : item.find('div', class_='listbox_price text-center').get_text(strip=True),
            'link' : HOST + item.find('div', class_='listbox_img pull-left').find('img').get('src')
        })
    return comps

def save(items, path):
    with open(path, 'a') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Цена', 'Картинка'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['link']])

def parser():
    PAGEBATOR = input("Введите номер страницы: ")
    PAGEBATOR = int(PAGEBATOR.strip())
    html = get_html(URL)
    if html.status_code == 200:
        new_list = []
        for page in range(1, PAGEBATOR):
            print(f"Страница №{page} готова")
            html = get_html(URL, params={'page':page})
            new_list.extend(get_content(html.text))
        save(new_list, CSV)
        print("Готово!")
    else:
        print("Error...")

parser()