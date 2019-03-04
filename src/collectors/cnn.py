import requests
import json
import logging
from bs4 import BeautifulSoup
from .base import Collector


class CNN(Collector):
    __url = "http://cerebro.api.cnn.io/api/v1/vertical/home"

    indispensable = ["headers"]

    def __init__(self, config):
        super().__init__(config)
        self.__headers = config["headers"]
        self.__proxies = config["proxies"] if config is not None and "proxies" in config.keys() else None

    def __article_urls(self):
        res = requests.get(self.__url, headers=self.__headers, proxies=self.__proxies)
        content = json.loads(res.text)
        articles = content["feed"]["items"]
        logging.info("loading CNN articles completed, and got {} urls".format(len(articles)))
        for article in articles:
            if article["type"] == "article":
                yield article["share_url"]

    def __parse_article_page(self, url):
        content = requests.get(url, proxies=self.__proxies).text
        bs = BeautifulSoup(content)
        [s.extract() for s in bs(["style", "script"])]
        title = bs.find("h1", {"class": "pg-headline"}).get_text()
        body = "\n".join([paragraph.get_text() for paragraph in bs.findAll("div", {"class": "zn-body__paragraph"})])
        logging.info("download article completed [url = {}]".format(url))
        return title + "\n" + body

    def generate(self):
        for url in self.__article_urls():
            yield self.__parse_article_page(url)
