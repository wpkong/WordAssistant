# 过滤器配置说明

## FileBasedFilter
基于文件的过滤器
```python
{
    "class": "filters.file_based_filter.FileBasedFilter",
    "config": {
        "file": "path to file"
    }
}
```

其中config必填，file为读取单词文件的文件路径，且单词文件须一个单词一行

## SimpleWordFilter
简单单词过滤器
```python
{
    "class": "filters.simple_word_filter.SimpleWordFilter",
}
```
无需任何配置

## FilterSet
可以同时使用多个过滤器

```python
{
    "class": "filters.base.FilterSet",
    "config": [
        {
            "class": "class",
            "config": {}
        }
    ]
}
```
config必填，且必须为list、tuple、set中的一种，config的元素为dict，其中class和config按照其他过滤器配置
