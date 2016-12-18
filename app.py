# -*- encoding: utf8 -*-
import os
import json
from tornado import web, ioloop

from datahandlers.make_struct import MakeMySQLToMySQL


class BaseHandler(web.RequestHandler):
    """docstring for BaseHandler"""
    def get_current_user(self):
        username = self.get_secure_cookie('user')

        if not username:
            return None

        # 这里还可以加一些其他的东西，比如时间戳啊 token 啊之类的校验


class Login(web.RequestHandler):
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

class Main(web.RequestHandler):
    def get(self, *args, **kwargs):
        if not self.get_secure_cookie('user'):
            self.redirect("/login")
            return

        self.redirect('/main')

    def post(self, *args, **kwargs):
        pass

class Main(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("main.html")


class MySQLToMySQL(web.RequestHandler):
    """mysql-mysql 的数据传输"""
    def post(self, *args, **kwargs):
        post_data = self.request.arguments
        write_para, read_para, common_para = json.loads(post_data['writer'][0]), json.loads(post_data['reader'][0]), json.loads(post_data['setting'][0])
        obj = MakeMySQLToMySQL(read_para, write_para, common_para)
        obj.make_struct()


class MySQLToOracle(web.RequestHandler):
    """mysql-oracle 的数据传输"""
    def post(self, *args, **kwargs):
        pass



class ProcessMySQLToMySQL(web.RequestHandler):
    def post(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    settings = {
        "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "debug": True
    }
    app = web.Application(
        [
        ('/login', Login),
        ('/main', Main),
        ('/mysql_to_mysql', MySQLToMySQL)


                           ], **settings)
    app.listen(8888)
    ioloop.IOLoop.instance().start()