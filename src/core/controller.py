from config import PROCESS_CONFIG
import importlib
from filters.base import Filter
from collectors.base import Collector as BaseCollector
from processors.base import Processor as BaseProcessor
import logging
import coloredlogs
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(module)s %(funcName)s %(lineno)s: %(levelname)s: %(message)s",
    stream=sys.stdout
)

coloredlogs.install("DEBUG")


class Controller:
    def __init__(self):
        pass

    def __get_cls(self, cls_name):
        """
        从配置得到类
        :param config:
        :return:
        """
        module_name, name = cls_name.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_name)
        return getattr(module, name)

    def __epoch(self, config):
        """
        分析并处理一项配置
        :param config:
        :return:
        """
        if "processor" not in config.keys() or "collector" not in config.keys() \
                or "class" not in config["processor"].keys() \
                or "class" not in config["collector"].keys():
            raise RuntimeError("lack configuration")

        Processor = self.__get_cls(config["processor"]["class"])
        Collector = self.__get_cls(config["collector"]["class"])

        filter = None

        if "filter" in config.keys() and "class" in config["filter"].keys():
            Cls = self.__get_cls(config["filter"]["class"])
            if not issubclass(Cls, Filter):
                raise RuntimeError("filter doesn't inherit from filters.base.Filter")
            filter = Cls(config["filter"].get("config"))
            logging.info("filter {} loaded completely".format(filter.__class__.__name__))

        if not issubclass(Processor, BaseProcessor):
            raise RuntimeError("processor doesn't inherit from processors.base.Processor")
        if not issubclass(Collector, BaseCollector):
            raise RuntimeError("collector doesn't inherit from collectors.base.Collector")

        processor = Processor(config["processor"].get("config"))
        logging.info("processor {} loaded completely".format(processor.__class__.__name__))
        collector = Collector(config["collector"].get("config"))
        logging.info("collector {} loaded completely".format(collector.__class__.__name__))

        words = processor.process(collector)
        logging.info("words dealing completed and got {} words".format(len(words)))
        if filter is not None:
            words = filter.filter(words)
            logging.info("words filtering completed and got {} valid words".format(len(words)))

        logging.info("wringing words...")
        processor.write(words)
        logging.info("writing complete")

    def run(self):
        """
        运行单词助手
        :return:
        """
        logging.info("WordAssistant is starting!")
        for i, config in enumerate(PROCESS_CONFIG):
            logging.info("start dealing item '{}', configuration: ".format(i))
            logging.info(config)
            self.__epoch(config)
            try:
                self.__epoch(config)
            except Exception as e:
                logging.error(e)
                print(e)
            logging.info("———————— item '{}' complete ————————".format(i))
