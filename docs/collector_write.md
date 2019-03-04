# 采集器编写说明

使用命令创建新文件：
```shell
python manage.py new collector [filename]
```

```python
class $name(Collector):
    indispensable = []

    def __init__(self, config):
        super().__init__(config)

    def generate(self) -> Generator:
        yield None
```

generate方法必须实现，返回是一个生成器，每次迭代必须返回一个字符串对象，处理器会通过多次迭代来获得文章。
