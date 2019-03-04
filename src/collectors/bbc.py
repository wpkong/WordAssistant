import requests
from bs4 import BeautifulSoup
import logging
from collections import Generator
from .base import Collector
import re


class BBC(Collector):
    indispensable = []

    def __init__(self, config):
        super().__init__(config)
        self.__pattern = re.compile("^https?://www\\.bbc\\.com/news/.*?$")
        self.__proxies = config["proxies"] if config is not None and "proxies" in config.keys() else None

    def __article_urls(self):
        bbc_url = "https://www.bbc.com"
        res = requests.get(bbc_url, proxies=self.__proxies).text
        bs = BeautifulSoup(res)
        links = bs.find_all("a", attrs={"class": "media__link"})
        logging.info("loading BBC articles completed, and got {} urls".format(len(links)))

        for link in links:
            href = link.get("href")
            url = (href if href[0] == 'h' else bbc_url + href)
            if self.__pattern.match(url):
                yield url

    def __parse_article_page(self, url):
        res = requests.get(url, proxies= self.__proxies)
        if res.url != url: return ""

        bs = BeautifulSoup(res.text)
        title = bs.find("h1", attrs={"class": "story-body__h1"}).get_text()
        body = bs.find("div", attrs={"property": "articleBody"})
        content = "\n".join([item.get_text() for item in body.find_all("p")])

        logging.info("download article completed [url = {}]".format(url))

        return title + "\n" + content

    def generate(self) -> Generator:
        for url in self.__article_urls():
            yield self.__parse_article_page(url)
