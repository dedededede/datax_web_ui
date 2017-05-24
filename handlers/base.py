# -*- encoding: utf8 -*-
import traceback

from tornado import gen, escape
from tornado.options import options
from tornado.web import RequestHandler, HTTPError

from libs import exceptions


class APIHandler(RequestHandler):
    def finish(self, chunk=None, status=None):
        if chunk is None:
            chunk = {}

        if isinstance(chunk, (dict, list)):
            if status:
                chunk = {"result": {"status": status, "data": chunk}}
            else:
                chunk = {"result": {"status": {"code": 200, "msg": "ok"}, "data": chunk}}
        elif isinstance(chunk, tuple):
            if status:
                chunk = {"result": {"status": status, "data": list(chunk)}}
            else:
                chunk = {"result": {"status": {"code": 200, "msg": "ok"}, "data": list(chunk)}}

        callback = escape.utf8(self.get_argument("callback", None))
        if callback:
            self.set_header("Content-Type", "application/x-javascript")

            if isinstance(chunk, dict):
                chunk = escape.json_encode(chunk)

            self._write_buffer = [callback, "(", chunk, ")"] if chunk else []
            super(APIHandler, self).finish()
        else:
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            super(APIHandler, self).finish(chunk)

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages."""
        debug = self.settings.get("debug", False)
        try:
            exc_info = kwargs.pop('exc_info')
            e = exc_info[1]

            if isinstance(e, exceptions.HTTPAPIError):
                pass
            elif isinstance(e, HTTPError):
                e = exceptions.HTTPAPIError(e.status_code)
            else:
                e = exceptions.HTTPAPIError(500)

            exception = "".join([ln for ln in traceback.format_exception(*exc_info)])

            if status_code == 500 and not debug:
                self._send_error_email(exception)

            self.clear()
            self.set_status(status_code)  # always return 200 OK for API errors
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            self.finish(str(e))
        except Exception:
            options.logger.error(traceback.format_exc())
            return super(APIHandler, self).write_error(status_code, **kwargs)