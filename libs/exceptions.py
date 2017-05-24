# -*- encoding: utf8 -*-

from tornado import escape
from tornado.web import HTTPError


class HTTPAPIError(HTTPError):
    """API error handling exception

    API server always returns formatted JSON to client even there is
    an internal server error.
    """
    def __init__(self, status_code=400, log_message=None, *args, **kwargs):
        super(HTTPAPIError, self).__init__(int(status_code), log_message, *args)
        self.error_type = kwargs.get('error_type', None)
        self.error_data = kwargs.get('error_data', {})

    def __str__(self):
        err = {"code": self.status_code, "msg": self.error_type}
        return escape.json_encode(err)