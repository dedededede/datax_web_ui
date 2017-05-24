# -*- encoding: utf8 -*-
import json
from tornado.web import RequestHandler
from handlers.base import APIHandler
from datahandlers.make_struct import MakeMySQLToMySQL


class MysqlToMysql(APIHandler):

    def post(self):
        post_data = self.request.arguments
        write_para, read_para, common_para = json.loads(post_data['writer'][0]), json.loads(
            post_data['reader'][0]), json.loads(post_data['setting'][0])
        obj = MakeMySQLToMySQL(read_para, write_para, common_para)
        result = obj.make_struct()
        self.finish(str(result))

class Login(APIHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        login_info = self.request.arguments
        try:
            user = login_info['user'][0]
            passwd = login_info['pwd'][0]
            if user == 'test' and passwd == 'test':
                self.write({'status': {'code': 200}})
                self.set_secure_cookie("user", user)

            else:
                self.write({'status':{'code': 400}})
        except Exception as e:
            pass


class Main(RequestHandler):
    def get(self, *args, **kwargs):
        if self.get_secure_cookie('user'):
            self.redirect("/login")
            return

        self.redirect('/main')


class MainContent(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("main.html")


handlers = [(r'/mysql_to_mysql', MysqlToMysql),
            ('/login', Login),
            ('/main', MainContent),
            ]



