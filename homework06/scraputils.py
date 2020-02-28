import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    table = parser.table.findAll("table", {"class": "itemlist"})[0]
    headers = table.findAll("a", {"class": "storylink"})
    infos = table.findAll("td", {"class": "subtext"})
    for i in range(len(headers)):
        title = headers[i].text
        url = headers[i]["href"]
        if url[:4] == "item":
            url = "https://news.ycombinator.com/" + url
        info_a = infos[i].findAll("a")
        if len(info_a) < 4:
            comments = 0
            author = ""
            points = 0
        else:
            points = int(infos[i].findAll("span", {"class": "score"})[0].text.split(" ")[0])
            author = infos[i].findAll("a", {"class": "hnuser"})[0].text
            if info_a[3].text == "discuss":
                comments = 0
            else:
                comments = int(info_a[3].text.split("\xa0")[0])
        row = {
            "author": author,
            "title": title,
            "url": url,
            "comments": comments,
            "points": points
        }
        news_list.append(row)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.table.findAll("table")[1].findAll("a")[-1]["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
