from collections import Generator
import requests
import logging
from bs4 import BeautifulSoup
from .base import Collector


class TheWashingtonPost(Collector):
    indispensable = []
    __headers = {
        'User-Agent': "Classic/3.23.0#4305 iOS/12.1.4 (iPhone)",
    }

    def __init__(self, config):
        super().__init__(config)
        self.__proxies = config["proxies"] if config is not None and "proxies" in config.keys() else None

    def __article_urls(self):
        url = "https://www.washingtonpost.com/"
        res = requests.get(url, headers=self.__headers, proxies=self.__proxies).text
        bs = BeautifulSoup(res)
        links = bs.find_all("a", attrs={"data-pb-url-field": "canonical_url"})
        logging.info("loading The Washington Post articles completed, and got {} urls".format(len(links)))
        for link in links:
            yield link.get("href")

    def __parse_article_page(self, url):
        res = requests.get(url, headers=self.__headers, proxies=self.__proxies).text
        bs = BeautifulSoup(res)

        title = bs.find("h1", attrs={"itemprop": "headline"}).get_text()
        article = "\n".join(
            [paragraph.get_text() for paragraph in bs.find("article", attrs={"itemprop": "articleBody"}).find_all("p")])
        logging.info("download article completed [url = {} ]".format(url))
        return title + "\n" + article

    def generate(self) -> Generator:
        for url in self.__article_urls():
            yield self.__parse_article_page(url)
