MOMO_ACCOUNT = {
    "email": "your email",
    "password": "your password",
}

CNN_CONFIG = {
    "class": "collectors.cnn.CNN",
    "config": {
        "headers": {
            'cnn-vertical': "home",
            'cnn-app-name': "cnniosapp",
            'cnn-platform-version': "12.1.4",
            'cnn-app-version': "5.22",
            'cnn-platform': "iphone",
            'cnn-viewmode': "full",
            'cnn-location': "international"
        },
        "proxies": {
            "http": "socks5://127.0.0.1:1080",
            'https': 'socks5://127.0.0.1:1080'
        }
    }
}

BBC_CONFIG = {
    "class": "collectors.bbc.BBC",
    "config": {
        "proxies": {
            "http": "socks5://127.0.0.1:1080",
            'https': 'socks5://127.0.0.1:1080'
        }
    }
}

CHINA_DAILY_CONFIG = {
    "class": "collectors.china_daily.ChinaDaily",
}

THE_WASHINGTON_POST_CONFIG = {
    "class": "collectors.the_washington_post.TheWashingtonPost",
    "config": {
        "proxies": {
            "http": "socks5://127.0.0.1:1080",
            'https': 'socks5://127.0.0.1:1080'
        }
    }
}

PROCESS_CONFIG = (
    {
        "processor": {
            "class": "processors.momo.Momo",
            "config": {
                "account": MOMO_ACCOUNT,
                "notepadID": "5c7cfa17252347033ed82350",
                "save": "data/momo-cnn.txt",
                "is_private": 1,
                "max_count": 200
            }
        },
        "collector": CNN_CONFIG,
        "filter": {
            "class": "filters.simple_word_filter.SimpleWordFilter",
        },
    },

    {
        "processor": {
            "class": "processors.momo.Momo",
            "config": {
                "account": MOMO_ACCOUNT,
                "notepadID": "5c7cfa45252347033ed82352",
                "save": "data/momo-bbc.txt",
                "is_private": 1,
                "max_count": 200
            }
        },
        "collector": BBC_CONFIG,
        "filter": {
            "class": "filters.simple_word_filter.SimpleWordFilter",
        },
    },

    {
        "processor": {
            "class": "processors.momo.Momo",
            "config": {
                "account": MOMO_ACCOUNT,
                "notepadID": "5c7cfa61934e3f036831a51c",
                "save": "data/momo-china-daily.txt",
                "is_private": 1,
                "max_count": 200
            }
        },
        "collector": CHINA_DAILY_CONFIG,
        "filter": {
            "class": "filters.simple_word_filter.SimpleWordFilter",
        },
    },

    {
        "processor": {
            "class": "processors.momo.Momo",
            "config": {
                "account": MOMO_ACCOUNT,
                "notepadID": "5c7cfb4d01e61e032be17533",
                "save": "data/momo-washington-post.txt",
                "is_private": 1,
                "max_count": 200
            }
        },
        "collector": THE_WASHINGTON_POST_CONFIG,
        "filter": {
            "class": "filters.simple_word_filter.SimpleWordFilter",
        },
    },
)
