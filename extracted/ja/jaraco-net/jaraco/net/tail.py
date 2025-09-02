import sys
import time

import cherrypy.process.plugins


class TailedFile:
    interval = 0.1

    def __init__(self, filename):
        self.file = open(filename)

    def next(self):
        # while hasattr(self, 'file'):
        while True:
            where = self.file.tell()
            line = self.file.readline()
            if line:
                return line
            self.file.seek(where)
            time.sleep(self.interval)

    def __iter__(self):
        return self

    def close(self):
        self.file.close()
        del self.file


class TailedFileServer:
    """
    A simple CherryPy controller that will tail a file and stream it to a
    browser.
    """

    def __init__(self, filename):
        self.filename = filename

    @cherrypy.expose
    def index(self):
        cherrypy.response.stream = True
        cherrypy.response.headers['content-type'] = 'text/plain'
        cherrypy.request.source = TailedFile(self.filename)
        cherrypy.engine.publish('register-tail')
        return cherrypy.request.source


class TailTracker(cherrypy.process.plugins.SimplePlugin, list):
    def __init__(self, bus):
        self.bus = bus
        self.bus.subscribe('register-tail', self.register)

    def register(self):
        self.append(cherrypy.request.source)

    def stop(self):
        self.bus.log("Closing tails")
        # close all tails
        for tail in self:
            tail.close()
        self.bus.log("Done closing tails")

    # need this to be called before server stop (25)
    stop.priority = 20  # type: ignore[attr-defined]

    def __hash__(self):
        return hash(id(self))


def handle_command_line():
    TailTracker(cherrypy.engine).subscribe()
    cherrypy.quickstart(TailedFileServer(sys.argv[1]))


if __name__ == '__main__':
    handle_command_line()
