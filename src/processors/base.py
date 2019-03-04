from abc import abstractmethod
from collections import Iterable
from collectors.base import Collector
from core.check_config import ConfigurationChecker


class Processor(ConfigurationChecker):

    def __init__(self, config):
        super().__init__(config)
        if type(config).__name__ != "dict":
            raise RuntimeError("缺少配置或配置非dict对象")
        self.__config = config

    @abstractmethod
    def process(self, collector: Collector) -> Iterable:
        pass

    @abstractmethod
    def write(self, words: Iterable):
        pass
