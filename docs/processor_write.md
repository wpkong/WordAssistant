# 处理器编写说明

使用命令创建新文件：
```shell
python manage.py new processor [filename]
```

```python
class $name(Processor):
    indispensable = []

    def __init__(self, config):
        super().__init__(config)

    def process(self, collector: Collector) -> Iterable:
        return []

    def write(self, words: Iterable):
        pass

```
必须实现process和write方法。

process负责读取传入的collector中的文章，经过处理得到一系列单词并返回。文章的获取可以使用for article in collector.generate():得到，其中article应是字符串

write负责将传入的单词写入相应的位置，或者上传到单词app
