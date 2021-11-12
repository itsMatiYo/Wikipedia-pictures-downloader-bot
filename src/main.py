import bs4
import os
import requests
import lxml
import urllib
import platform

nv = ''

if platform.system() == 'Linux':
    nv = '/'
elif platform.system() == 'Windows':
    nv = '\\'

CWD = os.getcwd()
WIKIPEDIA_URL = "https://en.wikipedia.org"

# header for Wikipedia User-Agent Policy
HEADERS = {
    'User-Agent': 'WikiPic Downloader Bot /0.0 (https://github.com/m4t11n) BeautifulSoup',
}

url = input(
    'enter wikipedia page URL: \nfor example --> https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart\nOr you can enter keyword and extract the page:\n')

"""Creating Media Directory"""
try:
    os.mkdir(f'{CWD}{nv}media')
    print('media directory created')
except FileExistsError:
    print('media directory was already created')


# regex to check if it is wikipedia url or it is a keyword
if url.find(r'en.wikipedia.org') == -1:
    # advanced serach
    url = f'https://en.wikipedia.org/w/index.php?search={url}&title=Special:Search&fulltext=1&ns0=1'
    req = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    first_link = soup.select_one(
        '.mw-search-result > .mw-search-result-heading > a')['href']
    url = f'{WIKIPEDIA_URL}{first_link}'
    print(f'Search lead to {url}')

req = requests.get(f'{url}', headers=HEADERS)
soup = bs4.BeautifulSoup(req.text, 'lxml')
page_name = soup.title.getText()

# Make WikiPage Directory
try:
    os.mkdir(f'{CWD}{nv}media{nv}{page_name}')
except FileExistsError:
    print('This page directory was already created')
except OSError:
    print("Creation of the directory failed")
else:
    print("Successfully created the directory")

print(f'extrating the images of... \n{page_name}')
for a in soup.select('a.image'):
    if int(a.img['width']) < 101:
        print(f'Ignoring {a["href"]}')
        break

    url_dl = a['href']
    url_pic = f'https://en.wikipedia.org{url_dl}'
    a_name = url_pic.split('/')[-1]

    # downloading pic from main page
    req = requests.get(url_pic, headers=HEADERS)
    soup2 = bs4.BeautifulSoup(req.text, 'lxml')
    tag = soup2.select_one('.fullImageLink > a > img')
    pic_url = tag['src']

    # decode image name to utf-8
    a_name = urllib.parse.unquote(a_name, encoding='utf-8')

    # making a legit file name (for windows)
    a_name = a_name.replace('File:', '').replace('/', '').replace("\\", '').replace(":", '').replace(
        "*", '').replace('?', '').replace("<", '').replace(">", '').replace("|", '').replace('"', '')
    print(f'extracting {a_name}')

    pic_req = requests.get(f'https:{pic_url}', headers=HEADERS)
    with open(f'{CWD}{nv}media{nv}{page_name}{nv}{a_name}', 'wb+') as f:
        f.write(pic_req.content)

print('Imagines successfully extracted 💯')


# ? future features
# image faqat ba enlarge kar mikone
