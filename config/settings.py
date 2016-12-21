# -*- encoding: utf8 -*-

import os
from libs import mlogger

debug = True
port = 8888
send_error_email = True

# 路径配置
root_dir = os.getcwd()

# LOG级别置为DEBUG
log_level_def = 10
log_config_map = {
    'main': {
        'name': 'main',
        'level': log_level_def,
        'filepath': os.path.join(root_dir, 'log', 'bwapi'),
    }
}

logger = mlogger.get_logger(log_config_map['main']['name'], log_config_map['main']['filepath'],
                            log_config_map['main']['level'])

mysql_to_mysql_job_template = {
    "setting": {},
    "job": {
        "setting": {
            "speed": {
                "channel": 1
            }
        },
        "content": [
            {
                "reader": {
                    "name": "mysqlreader",
                    "parameter": {
                        "username": "",
                        "password": "",
                        "connection": [
                            {
                                "querySql": [],
                                "jdbcUrl": ["jdbc:mysql://%s:%s/%s?useUnicode=true&characterEncoding=utf-8"]
                            }
                        ]
                    }
                },
                "writer": {
                    "name": "mysqlwriter",
                    "parameter": {
                        "writeMode": "",
                        "username": "",
                        "password": "",
                        "column": [

                        ],
                        "session": [
                            ""
                        ],
                        "preSql": [
                            "select 1"
                        ],
                        "connection": [
                            {
                                "jdbcUrl": "jdbc:mysql://%s:%s/%s?useUnicode=true&characterEncoding=utf-8",
                                "table": [
                                    ""
                                ]
                            }
                        ]
                    }
                }
            }
        ]
    }
}
