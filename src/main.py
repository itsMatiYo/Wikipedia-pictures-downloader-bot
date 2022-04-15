import concurrent.futures

from wikipage import WikipediaImage, WikiPediaPage


def run(imageLink):
    img = WikipediaImage(imageLink, wikipage)
    img.download_img()


again = True
prompt_message_url = """enter wikipedia page URL:
for example --> https://en.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart
Or you can enter keyword and extract the page:
"""

if __name__ == "__main__":
    while again:
        url = input(prompt_message_url)
        wikipage = WikiPediaPage(url)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(run, wikipage.get_image_links())

        print(f"{wikipage.get_page_title()} images successfully downloaded 💯")

        prompt_message_again = "Do you want to extract another page?(Type Y for yes)"
        answer = input(prompt_message_again)
        if answer != "Y":
            again = False
