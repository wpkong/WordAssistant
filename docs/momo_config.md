# 墨墨背单词配置说明

```python
{
    "class": "processors.momo.Momo",
    "config": {
        "account": {
            "email": "your email",
            "password": "your password",
        },
        "notepadID": "***",
        "save": "data/momo-bbc.txt",
        "is_private": 1,
        "max_count": 200
    }
}
```

config必填。

account（必填）为账户，按照墨墨背单词的注册情况来填写

notepadID（必填）为词库ID，可以创建一个新词库，填写好标题、简介和标签后保存，截取当前url中notepadId参数

save（必填）为临时文件保存目录

is_private（必填）为是否保存为私有词库，1为私有词库，0为公开词库

max_count（选填）为从collector中一次性能获得的最大单词量，但单词最终会经过过滤器，因此实际单词量会小于这个值
