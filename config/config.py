# -*- encoding: utf8 -*-
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
