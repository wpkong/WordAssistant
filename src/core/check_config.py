from collections import Iterable


class ConfigurationChecker:
    indispensable = None

    def __init__(self, config: dict):
        self.__config = config
        self._check_indispensable()

    def _check_indispensable(self):
        if self.__config is not None and isinstance(self.__config, dict) \
                and self.indispensable is not None and isinstance(self.indispensable, Iterable):

            for i in self.indispensable:
                if i not in self.__config.keys():
                    raise RuntimeError("缺少必要的参数: " + i)

    def get_config(self):
        return self.__config
