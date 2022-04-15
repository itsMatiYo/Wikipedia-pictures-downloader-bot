import configparser
import sys
import urllib

import bs4
import requests

invalid_filename_letters = [
    "\\",
    "/",
    "File:",
    ":",
    "*",
    "?",
    "<",
    ">",
    "|",
    '"',
]


from utils import create_directory, get_os_config

config = configparser.ConfigParser()
config.read("config.ini")

HEADERS = {"User-Agent": config["wikipedia"]["USER-AGENT-HEADER"]}
WIKIPEDIA_URL = config["wikipedia"]["WIKIPEDIA-URL"]


class WikiPediaPage:
    def __init__(self, url):
        if self.is_valid_url(url):
            self.url = url
        else:
            self.url = self.get_first_url_by_serach(url)
        create_directory("media")
        # Make WikiPage Directory
        self.init_soup()
        create_directory(["media", self.get_page_title()])

    def get_page_title(self):
        return self.soup.title.getText()

    def init_soup(self):
        try:
            req = requests.get(f"{self.url}", headers=HEADERS)
        except:
            print("No connection")
            sys.exit()
        self.soup = bs4.BeautifulSoup(req.text, "lxml")

    def get_image_links(self):
        return self.soup.select("a.image")

    @staticmethod
    def get_first_url_by_serach(keyword):
        url = f"https://en.wikipedia.org/w/index.php?search={keyword}&title=Special:Search&fulltext=1&ns0=1"
        try:
            req = requests.get(url, headers=HEADERS)
        except:
            print("no connection")
        soup = bs4.BeautifulSoup(req.text, "lxml")
        first_link = soup.select_one(
            ".mw-search-result \
            > .mw-search-result-heading \
            > a"
        )["href"]
        url = f"{WIKIPEDIA_URL}{first_link}"
        return url

    @staticmethod
    def is_valid_url(url):
        if url.find(WIKIPEDIA_URL) == -1:
            return False
        return True


class WikipediaImage:
    def __init__(self, image_tag, wikipage: WikiPediaPage):
        if self.is_not_thumbnail(image_tag):
            self.image_tag = image_tag
            self.page_title = wikipage.get_page_title()

    def extract_img_dl_url(self):
        imagePageURL = self.image_tag["href"]
        url_pic = f"{WIKIPEDIA_URL}{imagePageURL}"
        self.file_name = url_pic.split("/")[-1]
        req = requests.get(url_pic, headers=HEADERS)
        soup = bs4.BeautifulSoup(req.text, "lxml")
        imageTag = soup.select_one(".fullImageLink > a > img")
        download_link = imageTag["src"]
        return download_link

    def validate_filename(self):
        # decode image name to utf-8
        self.file_name = urllib.parse.unquote(self.file_name, encoding="utf-8")
        file_name = self.file_name
        # making a legit file name
        for letter in invalid_filename_letters:
            file_name = file_name.replace(letter, "")
        return file_name

    def save_img(self):
        imageRequest = requests.get(
            f"https:{self.extract_img_dl_url()}", headers=HEADERS
        )
        CWD, slash = get_os_config()
        fileName = self.validate_filename()
        with open(
            f"{CWD}{slash}media{slash}{self.page_title}{slash}{fileName}", "wb+"
        ) as f:
            f.write(imageRequest.content)

    def download_img(self):
        if not (self.is_not_thumbnail(self.image_tag)):
            return
        self.extract_img_dl_url()
        self.save_img()

    @staticmethod
    def is_not_thumbnail(imageTag):
        if int(imageTag.img["width"]) > 100:
            return True
        return False
