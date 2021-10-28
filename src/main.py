import bs4
import os
import requests
import lxml

CWD = os.getcwd()

"""Creating Media Directory"""
try:
    os.mkdir(f'{CWD}\\media')
    print('media directory created')
except:
    print('media directory was already created')


url = input(
    'enter wikipedia page URL: \nfor example --> https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart\n')

# header for Wikipedia User-Agent Policy
headers = {
    'User-Agent': 'WikiPic Downloader Bot /0.0 (https://github.com/m4t11n) BeautifulSoup',
}

# regex to check if it is wikipedia
if url.find(r'wikipedia.org') != -1:
    req = requests.get(f'{url}', headers=headers)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    page_name = soup.title.getText()

    # Make Page Directory
    try:
        os.mkdir(f'{CWD}\\media\\{page_name}')
    except FileExistsError:
        print('This page directory was already created')
    except OSError:
        print("Creation of the directory failed")
    else:
        print("Successfully created the directory")

    print(f'extrating the images of... \n{page_name}')
    for enlarger in soup.findAll('a', {'title': 'Enlarge'}):
        # print(enlarger)
        url_dl = enlarger['href']
        url_pic = f'https://en.wikipedia.org{url_dl}'
        img_name = url_pic.split('/')[-1]

        # downloading pic from main page
        req = requests.get(url_pic, headers=headers)
        soup2 = bs4.BeautifulSoup(req.text, 'lxml')
        tag = soup2.select_one(' .fullImageLink')
        pic_url = tag.a.img['src']
        img_name = img_name.replace('File:', '')
        pic_req = requests.get(f'https:{pic_url}', headers=headers)
        with open(f'{CWD}\\media\\{page_name}\\{img_name}', 'wb+') as f:
            f.write(pic_req.content)
