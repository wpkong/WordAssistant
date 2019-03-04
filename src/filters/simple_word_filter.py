from collections import Iterable
from .file_based_filter import FileBasedFilter
from .base import Filter


class SimpleWordFilter(Filter):
    """
    简单词过滤器
    """

    def __new__(cls, *args, **kwargs):
        return FileBasedFilter(dict(file="data/simple-words.txt"))

    def filter(self, words: Iterable):
        pass
