import os
import sys
import json
import datetime

from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options

from libs.options import parse_options


class Application(web.Application):
    def __init__(self):
        from urls import handlers, ui_modules

        settings = dict(debug=options.debug,
                        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
                        static_path=os.path.join(os.path.dirname(__file__), 'static'),
                        ui_modules=ui_modules)

        super(Application, self).__init__(handlers, **settings)

    def reverse_api(self, request):
        """Returns a URL name for a request"""
        handlers = self._get_host_handlers(request)

        for spec in handlers:
            match = spec.regex.match(request.path)
            if match:
                return spec.name

        return None

def proc_init():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(project_dir)
    os.chdir(project_dir)


def main():
    proc_init()
    parse_options()
    http_server = HTTPServer(Application(), xheaders=True)
    http_server.bind(int(options.port), '127.0.0.1')  # listen local only
    http_server.start(1)

    IOLoop.instance().start()


if __name__ == '__main__':
    main()