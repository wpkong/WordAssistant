from collections import Generator
from .base import Collector
import requests
import json
import logging
import lxml.etree as etree


class ChinaDaily(Collector):
    indispensable = []

    __headers = {
        "User-Agent": "ChinaDaily/7.1.0 (iPhone; iOS 12.1.4; Scale/2.00; ChinaDailyIOS/7.1.0)",
        "Host": "enapp.chinadaily.com.cn",
        "Connection": "keep-alive"
    }

    def __init__(self, config):
        super().__init__(config)
        self.__column = config["column"] if config is not None and "column" in config.keys() else "global"
        self.__proxies = config["proxies"] if config is not None and "proxies" in config.keys() else None

    def __article_urls(self):
        url = "https://enapp.chinadaily.com.cn/channels/enapp/custom-columns.json"
        res = requests.get(url, headers=self.__headers, proxies=self.__proxies).text
        datas = json.loads(res)
        data = None
        for d in datas:
            if d["dirname"] == self.__column:
                data = d
                break
        if data is None: return None

        column_id = data["uuid"]
        url = "http://enapp.chinadaily.com.cn/channels/enapp/columns/{}/stories.json".format(column_id)
        res = requests.get(url, headers=self.__headers, proxies=self.__proxies).text
        data = json.loads(res)
        stories = data["stories"]
        logging.info("loading ChinaDaily articles completed, and got {} urls".format(len(stories)))
        for story in stories:
            yield story["jsonUrl"]

    def __parse_article_page(self, url):
        res = requests.get(url, headers=self.__headers, proxies=self.__proxies).text
        data = json.loads(res)
        title = data["title"]
        content = data["content"]

        tree = etree.HTML(content)
        page = title + "\n" + ("".join(tree.xpath("//text()")).strip().replace("\n", " "))
        logging.info("download article completed [url = {}]".format(url))
        return page

    def generate(self) -> Generator:
        for url in self.__article_urls():
            yield self.__parse_article_page(url)
