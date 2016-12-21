# -*- encoding: utf8 -*-
import tornado
from config.settings import mysql_to_mysql_job_template
from libs.exceptions import HTTPAPIError


class CheckPara(object):

    def __init__(self, read, write, common):
        read_value = [read[key] for key in read]
        write_value = [write[key] for key in write]
        common_value = [common[key] for key in common]
        if not (any(read_value) or any(write_value) or any(common_value)):
            raise HTTPAPIError(error_data='参数错误', error_code=400)

class MakeMySQLToMySQL(CheckPara):
    def __init__(self, read, write, common):
        self.read_data = read
        self.write_data = write
        self.common = common
        super(MakeMySQLToMySQL, self).__init__(read, write, common)

    def make_struct(self):
        '''
        read_value = [self.read_data[key] for key in self.read_data]
        write_value = [self.write_data[key] for key in self.write_data]
        common_value = [self.common[key] for key in self.common]

        if any(read_value) or any(write_value) or any(common_value):
            return HTTPAPIError(status_code=200, error_data='参数错误', error_code=400)

        '''

        job_demo = mysql_to_mysql_job_template
        job_demo['job']['setting']['speed']['channel'] = int(self.common['juxtaposed'])
        read_demo = job_demo['job']['content'][0]['reader']
        write_demo = job_demo['job']['content'][0]['writer']
        read_demo['parameter']['username'] = self.read_data['username']
        read_demo['parameter']['password'] = self.read_data['password']
        read_demo['parameter']['connection'] = {
            "querySql": self.read_data['querysql'],
            "jdbcUrl": job_demo['job']['content'][0]['reader']['parameter']['connection'][0]["jdbcUrl"][0] % (
                self.read_data['host'], self.read_data['port'], self.read_data['db'])
        }

        write_demo['parameter']['writeMode'] = self.write_data['writeMode']
        write_demo['parameter']['username'] = self.write_data['username']
        write_demo['parameter']['password'] = self.write_data['password']
        column_list = [item['values'] for item in self.common['column']]
        write_demo['parameter']['column'] = column_list
        write_demo['parameter']['session'] = "set session sql_mode='%s' " % self.write_data['sql_mode']

        write_demo['parameter']['connection'] = [
            {
                "jdbcUrl": mysql_to_mysql_job_template['job']['content'][0]['writer']['parameter']['connection'][0]["jdbcUrl"] % (
                    self.write_data['host'], self.write_data['port'], self.write_data['db']),
                "table": [
                    self.write_data["table"]
                ]
            }

        ]

        job_demo['job']['content'][0]['reader'] = read_demo
        job_demo['job']['content'][0]['writer'] = write_demo
        print job_demo


