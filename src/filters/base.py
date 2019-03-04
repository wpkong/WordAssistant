import importlib
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
        if config is not list or config is not tuple or config is not set:
            raise RuntimeError("FilterSet配置应为list, tuple, set")
        for c in config:
            Cls = self.__get_cls(c["class"])
            f = Cls(c.get("config"))
            self.__add(f)

    def __add(self, filter: Filter):
        if isinstance(filter, FilterSet):
            raise RuntimeError("不能在FilterSet中添加FilterSet")
        self.filters.append(filter)

    def __get_cls(self, cls_name):
        module_name, name = cls_name.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_name)
        return getattr(module, name)

    def filter(self, words: Iterable):
        for f in self.filters:
            words = f.filter(words)
        return words
