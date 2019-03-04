from abc import abstractmethod
from collections import Generator, Iterable
from core.check_config import ConfigurationChecker


class Collector(ConfigurationChecker):
    indispensable = None

    def __init__(self, config):
        super().__init__(config)
        self._check_indispensable()

    @abstractmethod
    def generate(self) -> Generator:
        pass
