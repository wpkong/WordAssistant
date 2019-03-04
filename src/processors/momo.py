import requests
import json
import execjs
import logging
from nltk.stem import WordNetLemmatizer
from .base import Processor
from datetime import datetime


class Momo(Processor):
    """
    墨墨背单词处理器
    """
    indispensable = ["account", "notepadID", "save", "is_private"]

    def __init__(self, config):
        super().__init__(config)
        self.lemmatizer = WordNetLemmatizer()
        self.account = config["account"]
        self.notepadID = config["notepadID"]
        self.savepath = config["save"]
        self.is_private = config["is_private"]

        logging.info("initializing Momo tools")
        with open("utils/parseArticle.js", "r") as f:
            self.parseArticle = execjs.compile(f.read())

        lib_url = "https://www.maimemo.com/res/editor/assets/library.json"
        self.library = requests.get(lib_url).text
        logging.info("initialization complete")

        self.__login()

    def __login(self):
        """
        登录墨墨
        :return:
        """
        url = "https://www.maimemo.com/auth/login"
        data = self.account
        res = requests.post(url, data)
        self.cookies = res.cookies
        logging.info("login successfully")

    def __extract_words(self, article):
        """
        从文章提取单词
        :param article:
        :return:
        """
        data = self.parseArticle.call("parseNotepad", article, self.library)
        words = data["words"].keys()
        phrases = data["phrases"].keys()
        vocabulary = list(words) + list(phrases)
        return vocabulary

    def __purify_words(self, vocabulary):
        """
        精炼单词从墨墨服务器检查以及经过nltk恢复原形
        :param vocabulary: 提取出的单词  来自extract words
        :return:
        """
        url = "https://www.maimemo.com/api/v1/vocabulary/check_exists?token="
        vocabulary = [self.lemmatizer.lemmatize(self.lemmatizer.lemmatize(v, pos='v'))
                      for v in vocabulary if len(v) > 2]
        res = requests.post(url, data=dict(spellings=vocabulary), cookies=self.cookies)
        res = json.loads(res.text)
        vocabulary = res["data"]["exists"]
        return vocabulary

    def __download_notepad_data(self):
        """
        获取编辑器里已有的数据
        :return:
        """
        url = "https://www.maimemo.com/api/v1/notepads/{}".format(self.notepadID)
        res = requests.get(url, cookies=self.cookies).text
        res = json.loads(res)
        content = res["data"]["notepad"]["content"]

        with open(self.savepath, "w") as f:
            f.write(content)

        return content

    def __notepad_to_words(self, content):
        """
        把notepad里面的数据转换成单词，进行查重
        :param content:
        :return:
        """
        words = self.__extract_words(content)
        return set(words)

    def process(self, collector):
        """
        处理单词
        :param collector:
        :return:
        """
        content = self.__download_notepad_data()
        vocab = self.__notepad_to_words(content)
        new_words = []

        max_count = None
        if "max_count" in self.get_config().keys() and type(self.get_config()["max_count"]) == int:
            max_count = self.get_config()["max_count"]
            logging.info("max count limit: {}".format(max_count))

        for article in collector.generate():
            words = self.__extract_words(article)
            words = set(self.__purify_words(words))
            words = words - vocab
            new_words += words
            vocab |= words
            logging.info("Already loading {} new words".format(len(new_words)))
            if max_count is not None:
                if len(new_words) > max_count:
                    new_words = new_words[:max_count]
                    break
        return new_words

    def write(self, words):
        """
        写入新数据(最终完成的单词
        :return:
        """
        now = datetime.now()
        with open(self.savepath, "a") as f:
            f.write("\n#")
            f.write(now.strftime('%Y年%m月%d日'))
            f.write("\n")
            f.write("\n".join(words))

        with open(self.savepath, "r") as f:
            content = f.read()

        data = {
            "publish": True,
            "notepad": {
                "content": content,
                "is_private": self.is_private,
                "version": 1
            }
        }

        url = "https://www.maimemo.com/api/v1/notepads/{}".format(self.notepadID)
        res = requests.post(url, cookies=self.cookies, json=data)

        res = json.loads(res.text)
        if res["success"]:
            logging.info("成功上传至墨墨服务器")
        else:
            logging.error(res)
