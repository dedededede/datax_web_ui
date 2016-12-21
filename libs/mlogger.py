import logging
from logging import Filter, Logger
from logging import FATAL, WARNING, INFO, DEBUG, NOTSET, ERROR
from logging.handlers import TimedRotatingFileHandler


LOG_FORMATTER = logging.Formatter('[%(levelname)s] [%(asctime)s] '
                                  '[%(message)s] [%(module)s %(filename)s %(lineno)d]')


class UpLevelFilter(Filter):
    def __init__(self, level):
        Filter.__init__(self)
        self.level = level

    def filter(self, record):
        return record.levelno <= self.level


class ReLogger(Logger):
    def __init__(self, name, level=NOTSET):
        Logger.__init__(self, name, level)

    def build(self, file_path, formatter):
        common_file_name = "%s.log" % file_path
        error_file_name = "%s.err.log" % file_path

        common_handler = TimedRotatingFileHandler(common_file_name, when='MIDNIGHT')
        common_handler.setLevel(DEBUG)
        common_handler.setFormatter(formatter)
        common_handler.addFilter(UpLevelFilter(INFO))

        self.addHandler(common_handler)

        error_handler = TimedRotatingFileHandler(error_file_name, when='MIDNIGHT')
        error_handler.setLevel(WARNING)
        error_handler.setFormatter(formatter)

        error_handler.addFilter(UpLevelFilter(FATAL))
        self.addHandler(error_handler)


def get_logger(name, file_path, level=NOTSET, formatter=LOG_FORMATTER):
    if name:
        logging.setLoggerClass(ReLogger)
        logger = Logger.manager.getLogger(name)
        logger.build(file_path, formatter)
        logger.setLevel(level)
        return logger
