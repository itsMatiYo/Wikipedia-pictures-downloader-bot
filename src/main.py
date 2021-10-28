import bs4
import os
import requests
import lxml

url = input('enter wikipedia page URL:')
cwd = os.getcwd()
if url.find(r'wikipedia.org') != -1:
    try:
        os.mkdir(f'{cwd}\\test1')
    except OSError:
        print("Creation of the directory failed")
    else:
        print("Successfully created the directory")
    req = requests.get(f'https://{url}')
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    for img in soup.select(' .thumbimage'):
        url_dl = img['src']
        url_dl_copy = url_dl
        img_name = url_dl_copy.split('/')[-1]
        img_content = requests.get(f'https:{url_dl}')
        with open(f'{cwd}\\test1\\{img_name}', 'wb') as f:
            f.write(img_content.content)
