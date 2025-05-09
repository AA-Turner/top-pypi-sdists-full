class Frame(object):
    def __init__(
            self,
            f_back,
            f_fileno,
            f_code,
            f_locals,
            f_globals=None,
            f_trace=None):
        self.f_back = f_back
        self.f_lineno = f_fileno
        self.f_code = f_code
        self.f_locals = f_locals
        self.f_globals = f_globals
        self.f_trace = f_trace

        if self.f_globals is None:
            self.f_globals = {}


class FCode(object):
    def __init__(self, name, filename):
        self.co_name = name
        self.co_filename = filename


def add_exception_to_frame(frame, exception_info):
    frame.f_locals['__exception__'] = exception_info


def remove_exception_from_frame(frame):
    try:
        frame.f_locals.pop('__exception__', None)
    except:
        if "__exception__" in frame.f_locals:
           frame.f_locals["__exception__"] = None


FILES_WITH_IMPORT_HOOKS = ['pydev_monkey_qt.py', 'pydev_import_hook.py']

def just_raised(trace):
    if trace is None:
        return False
    return trace.tb_next is None

def ignore_exception_trace(trace):
    while trace is not None:
        filename = trace.tb_frame.f_code.co_filename
        if filename in (
            '<frozen importlib._bootstrap>', '<frozen importlib._bootstrap_external>'):
            # Do not stop on inner exceptions in py3 while importing
            return True

        # ImportError should appear in a user's code, not inside debugger
        for file in FILES_WITH_IMPORT_HOOKS:
            if filename.endswith(file):
                return True

        trace = trace.tb_next

    return False

def cached_call(obj, func, *args):
    cached_name = '_cached_' + func.__name__
    if not hasattr(obj, cached_name):
        setattr(obj, cached_name, func(*args))

    return getattr(obj, cached_name)
