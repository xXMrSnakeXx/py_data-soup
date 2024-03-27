import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://quotes.toscrape.com"


def get_page_content(url):
    response = requests.get(url)
    content = BeautifulSoup(response.content, "html.parser")
    return content


def get_quotes(page_content):
    quotes = page_content.find_all("div", class_="quote")
    quote_list = []

    for quote in quotes:
        text = quote.find("span", class_="text").get_text().strip()
        author = quote.find("small", class_="author").get_text().strip()
        tags = [tag.get_text().strip() for tag in quote.select(".tag")]
        quote_list.append({"tags": tags, "author": author, "quote": text})
    return quote_list


def get_authors(page_content, authors):
    quotes = page_content.find_all("div", class_="quote")
    for quote in quotes:
        url = quote.find("a")["href"]
        document = get_page_content(BASE_URL + url)
        fullname = document.find("h3", class_="author-title").get_text().strip()
        if not any(author["fullname"] == fullname for author in authors):
            author_info = {
                "fullname": fullname,
                "born_date": document.find("span", class_="author-born-date")
                .get_text()
                .strip(),
                "born_location": document.find("span", class_="author-born-location")
                .get_text()
                .strip(),
                "description": document.find("div", class_="author-description")
                .get_text()
                .strip(),
            }
            authors.append(author_info)


def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[INFO] Error: {e}")


if __name__ == "__main__":
    quotes = []
    authors = []
    page_content = get_page_content(BASE_URL)
    quotes.extend(get_quotes(page_content))
    get_authors(page_content, authors)
    while True:
        nex_page_link = page_content.find("li", class_="next")
        if nex_page_link is None:
            break
        next_page_url = BASE_URL + nex_page_link.find("a")["href"]
        page_content = get_page_content(next_page_url)
        quotes.extend(get_quotes(page_content))
        get_authors(page_content, authors)
        print(next_page_url)

    save_json("authors.json", authors)
    save_json("quotes.json", quotes)
