from collections import Iterable
from .base import Filter


class FileBasedFilter(Filter):
    """
    基于文件的单词过滤器
    """
    __simple_word_list = set()

    def __init__(self, config):
        super().__init__(config)
        self.__file_path = config["file"]
        with open(self.__file_path, "r") as f:
            self.__simple_word_list = set([line.strip() for line in f.readlines()])

    def filter(self, words: Iterable):
        return list(set(words) - self.__simple_word_list)
