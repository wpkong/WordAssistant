# 过滤器编写说明

使用命令创建新文件：
```shell
python manage.py new filter [filename]
```

```python
class $name(Filter):
    def __init__(self):
        pass

    def filter(self, words: Iterable) -> Iterable:
        return words
```
必须实现filter方法，传入单词集合，过滤完成后返回新的单词集合
