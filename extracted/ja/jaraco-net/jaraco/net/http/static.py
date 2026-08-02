import os
import argparse
import importlib

import cherrypy

from . import htmldir


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=80, type=int)
    return parser.parse_args()


def serve_local():
    """
    Serve the current directory as static files.
    """
    importlib.import_module('jaraoc.net.http.staticdirindex')
    args = get_args()
    config = {
        'global': {'server.socket_host': '::0', 'server.socket_port': args.port},
        '/': {
            'tools.staticdir.on': 'true',
            'tools.staticdir.indexlister': htmldir.htmldir,
            'tools.staticdir.dir': os.getcwd(),
        },
    }
    cherrypy.quickstart(None, config=config)
