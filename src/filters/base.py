from abc import abstractmethod
from collections import Iterable
from core.check_config import ConfigurationChecker


class Filter(ConfigurationChecker):
    """
    过滤器基类
    """
    indispensable = None

    def __init__(self, config):
        super().__init__(config)
        self.__config = config

    @abstractmethod
    def filter(self, words: Iterable) -> Iterable:
        return words


class FilterSet(Filter):
    def __init__(self, config):
        super().__init__(config)
        self.filters = []

    def add(self, filter: Filter):
        if isinstance(filter, FilterSet):
            raise RuntimeError("不能在FilterSet中添加FilterSet")
        self.filters.append(filter)

    def filter(self, words: Iterable):
        for f in self.filters:
            words = f.filter(words)
        return words
