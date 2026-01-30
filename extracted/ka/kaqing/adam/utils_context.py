from copy import copy

from adam.repl_session import ReplSession
from adam.utils import Color, ConfigHolder, _log, log2, pod_log_dir
from adam.utils_async_job import AsyncJobs

class Context:
    ALL = 'all'
    PODS = 'pods'
    LOCAL = 'local'

    def new(cmd: str = None, backgrounded = False, show_out = False, text_color: str = None, show_verbose = False, history = 'all', debug: bool = None):
        if show_verbose and not show_out:
            # override show_out to True
            show_out = True
            if not text_color:
                text_color = Color.gray

        return Context(cmd, backgrounded=backgrounded, show_out=show_out, text_color=text_color, show_verbose=show_verbose, history=history, debug=debug)

    def copy(self,
             backgrounded: bool = None,
             extra: dict[str, str] = {},
             pod_log_file: str = None,
             show_out: bool = None,
             text_color: str = None,
             show_verbose: bool = None,
             history: str = None,
             debug: bool = None):
        ctx1 = copy(self)
        if backgrounded is not None:
            ctx1.backgrounded = backgrounded

        if not self.backgrounded and ctx1.backgrounded:
            ctx1._init_backgrounded(extra)

        if pod_log_file:
            ctx1._pod_log_file = pod_log_file

        if show_out is not None:
            ctx1.show_out = show_out

        if text_color:
            ctx1.text_color = text_color

        if show_verbose is not None:
            ctx1.show_verbose = show_verbose

        if history is not None:
            ctx1.history = history

        if debug is not None:
            ctx1.debug = debug

        return ctx1

    def __init__(self, cmd: str, backgrounded = False, show_out = False, text_color: str = None, show_verbose: bool = False, history = 'all', debug: bool = False):
        self.cmd = cmd
        self.backgrounded = backgrounded
        self.show_out = show_out
        self.text_color = text_color
        self.show_verbose = show_verbose
        self.history = history
        self.debug = debug
        if self.debug is None:
            self.debug = ConfigHolder().config.is_debug()

        self.log_file: str = None
        self._histories = set()
        self.job_id = None
        self._pod_log_file: str = None

        if backgrounded:
            self._init_backgrounded()

    def _init_backgrounded(self, extra: dict[str, str] = {}):
        self.job_id = AsyncJobs.new_id()
        log2(f'[{self.job_id}] Use :? to get the results.')

        log_file = AsyncJobs.local_log_file(self.cmd, self.job_id, extra=extra)
        self.log_file = log_file

    def log(self, s = None, nl = True, text_color: str = None, verbose = False):
        return self._log(s=s, nl=nl, text_color=text_color, verbose=verbose)

    def log2(self, s = None, nl = True, text_color: str = None, verbose = False):
        return self._log(s=s, nl=nl, text_color=text_color, err=True, verbose=verbose)

    def _log(self, s = None, nl = True, text_color: str = None, err = False, verbose = False):
        if self.log_file and self.history in [Context.ALL, Context.LOCAL]:
            self.append_history(f':tail {self.log_file}')

        if verbose:
            if self.show_verbose: # alter tables
                if not text_color:
                    text_color = Color.gray

                return _log(s=s, nl=nl, file=self.log_file if self.backgrounded else None, text_color=text_color, err=err)
        elif self.show_out:
            if not text_color:
                text_color = self.text_color

            return _log(s=s, nl=nl, file=self.log_file if self.backgrounded else None, text_color=text_color, err=err)

    def pod_log_file(self, pod: str = None, suffix = '.log', history=True):
        if self._pod_log_file:
            return self._pod_log_file

        log_file = AsyncJobs.pod_log_file(self.cmd, job_id=self.job_id, pod_suffix='', suffix=suffix, dir=pod_log_dir())
        if pod and history and self.history in [Context.ALL, Context.PODS]:
            self.append_history(f'@{pod} tail {log_file}')

        return log_file

    def append_history(self, command: str):
        if command not in self._histories:
            ReplSession().append_history(command)

            self._histories.add(command)

Context.NULL = Context(None, backgrounded=False)