import logging
import os.path
import sys

from rook.processor.namespaces.python_object_namespace import PythonObjectNamespace
from rook.processor.namespaces.container_namespace import ContainerNamespace


class LogRecordNamespace(PythonObjectNamespace):

    def __init__(self, record):
        super(LogRecordNamespace, self).__init__(record, methods=self.METHODS)
        self.record = None

    def format(self, args=None):
        if self.record is None:
            self.obj = self.calc_record()
        return PythonObjectNamespace(self.obj.getMessage())
    
    def read_attribute(self, name):
        if self.record is None:
            self.obj = self.calc_record()
        return super(LogRecordNamespace, self).read_attribute(name)

    @staticmethod
    def find_caller():
        _logging_srcfile = logging._srcfile

        f = sys._getframe(8)
        while hasattr(f, "f_code") and f.f_code.co_name != "_callback":
            f = f.f_back

        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back

        rv = "(unknown file)", 0, "(unknown function)"
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _logging_srcfile:
                f = f.f_back
                continue

            rv = co.co_filename, f.f_lineno, co.co_name
            break

        return rv

    def calc_record(self):
        logger, level, fn, lno, msg, args, exc_info, func, extra = self.obj

        if fn is None:
            try:
                fn, lno, func = self.find_caller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"

        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        self.record = logger.makeRecord(logger.name, level, fn, lno, msg, args, exc_info, func, extra)
        return self.record

    def dump(self, args=None):
        if self.record is None:
            self.obj = self.calc_record()
        return ContainerNamespace({
            'name': PythonObjectNamespace(self.obj.name),
            'msg': PythonObjectNamespace(self.obj.msg),
            'formatted_message': self.format(),
            'args': PythonObjectNamespace(self.obj.args),
            'level_name': PythonObjectNamespace(self.obj.levelname),
            'level_no': PythonObjectNamespace(self.obj.levelno),
            'path_name': PythonObjectNamespace(self.obj.pathname),
            'filename': PythonObjectNamespace(self.obj.filename),
            'module': PythonObjectNamespace(self.obj.module),
            'lineno': PythonObjectNamespace(self.obj.lineno),
            'function': PythonObjectNamespace(self.obj.funcName),
            'time': PythonObjectNamespace(self.obj.created),
            'thread_id': PythonObjectNamespace(self.obj.thread),
            'thread_name': PythonObjectNamespace(self.obj.threadName),
            'process_name': PythonObjectNamespace(self.obj.processName),
            'process_id': PythonObjectNamespace(self.obj.process)
        })

    METHODS = (format, dump)
