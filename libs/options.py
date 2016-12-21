# -*- encoding: utf8 -*-

import os
from tornado.options import define
from tornado.options import options
from tornado.options import parse_command_line

def parse_config_file(path):
    '''Rewrite tornado default parse_config_file.

    Parses and loads the Python config file at the given path.

    This version allow customize new options which are not defined before
    from a configuration file.
    '''
    config = {}
    execfile(path, config, config)

    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])


def parse_options():
    _root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    _settings = os.path.join(_root, 'config', 'settings.py')

    try:
        parse_config_file(_settings)
        options.logger.info('Using settings.py as default settings.')
    except Exception, e:
        options.logger.error('No any default settings, are you sure? Exception: %s' % e)

    parse_command_line()