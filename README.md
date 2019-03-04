# 单词采集器

> 从CNN, BBC, 华盛顿邮报等网上采集文章,转换成单词输送到单词APP. 目前仅支持墨墨

[使用方法](#使用方法)

[项目结构](#项目结构)

[配置说明](#配置说明)

## 使用方法
```
python manage.py run    # 运行项目

python manage.py new collector [name]  # 从模板新建一个采集器

python manage.py new filter [name]  # 从模板新建一个过滤器

python manage.py new processor [name]  # 从模板新建一个处理器
```

## 项目结构
#### /
- manage.py  管理文件，无需更改
- config.py  配置文件

#### core
核心代码

- check_config.py  检查配置文件是否满足indispensable变量规定的关键词
- controller.py  控制器，活动在程序的生命周期


#### data
静态数据文件夹
- simple-words: 简单词,不会被采集到
- 其他转储文件

#### collectors
采集器以插件形式编写

- base.py:  采集器基类,所有采集器必须继承
- cnn.py:   CNN News采集器
- bbc.py:   BBC News采集器
- china_daily.py  China Daily英文网采集器
- the_washington_post.py  The Washington Post采集器

#### processors
数据处理器,将单词输入到单词APP或者其他地方,目前仅支持墨墨背单词

- base.py   处理器基类,所有处理器都要继承
- momo.py   墨墨背单词处理器


#### filters
单词过滤器，过滤不符合条件的单词

- base.py  过滤器基类，所有过滤器必须继承
- file_based_filter.py  基于文本文件的过滤器，须在配置文件中指明"file"，文件内一个单词占一行
- simple_word_filter.py  简单单词过滤器，file_based_filter的简单实现，无须指明文件

#### utils
常用工具

- parseArticle.js    墨墨背单词的网页文章分析器,利用它来分词


#### templates
模板文件


## 配置说明
在**config.py**文件中进行修改，且配置应为PROCESS_CONFIG变量，类型为list、set或者tuple等可迭代列表。

配置单元为dict对象，其中必须包含processor和collector关键词，filter关键词可选。

processor、collector、filter的值应为dict，且包含关键字class以指向具体的类，plugin可选，但具体看响应的类的规定。

即配置应满足
```python
PROCESS_CONFIG = (
    {
        "processor": {
            "class": "",
            "config": {}
        },
        "collector": {
            "class": "",
            "config": {}
        },
        "filter": {
            "class": "",
            "config": {}
        },
    },
)
```

具体的配置如下：
- [CNN](docs/cnn_config.md)
- [BBC](docs/bbc_config.md)
- [中国日报](docs/china_daily_config.md)
- [华盛顿邮报](docs/the_washington_post_config.md)
- [过滤器配置](docs/filter_config.md)
- [墨墨背单词](docs/momo_config.md)

#### ChinaDaily 中国日报
- column: [home global xismoments bilingual popular china business opinion world tech culture life travel sports audio video photo cheetah spec]
