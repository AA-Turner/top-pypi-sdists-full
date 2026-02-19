from copy import copy
from typing import Callable, TypeVar, Union

from adam.config_holder import ConfigHolder
from adam.presentation.color import Color
from adam.utils_concurrent import offload
from adam.directories import Directories
from adam.thread_locals import thread_local_command
from adam.utils_job.job import Job
from adam.utils_log import _log, log2
from adam.utils_repl.repl_session import ReplSession

T = TypeVar('T')

class Context:
    ALL = 'all'
    PODS = 'pods'
    LOCAL = 'local'

    def new(cmd: str = None,
            background = False,
            show_out = False,
            text_color: str = None,
            history = 'pods',
            debug: bool = None,
            bg_init_msg: Union[str, bool] = None,
            job_id: str = None,
            retriable = False):
        return Context(cmd, background=background, show_out=show_out, text_color=text_color, history=history, debug=debug, bg_init_msg=bg_init_msg, job_id=job_id, retriable=retriable)

    def copy(self,
             background: bool = None,
             extra: dict[str, str] = {},
             pod_log_file: str = None,
             show_out: bool = None,
             text_color: str = None,
             history: str = None,
             debug: bool = None,
             bg_init_msg: Union[str, bool] = None,
             job_id: str = None,
             cmd: str = None):
        ctx1 = copy(self)

        if background is not None:
            ctx1.background = background

        if bg_init_msg:
            ctx1.bg_init_msg = bg_init_msg
        if not self.background and ctx1.background:
            ctx1._init_backgrounded(extra)

        if pod_log_file:
            ctx1._pod_log_file = pod_log_file

        if show_out is not None:
            ctx1.show_out = show_out

        if text_color:
            ctx1.text_color = text_color

        if history is not None:
            ctx1.history = history

        if debug is not None:
            ctx1.debug = debug

        if job_id is not None:
            ctx1.job_id = job_id
            # ctx1._init_backgrounded(extra)

        if cmd is not None:
            ctx1.cmd = cmd

        return ctx1

    def __init__(self,
                 cmd: str,
                 background = False,
                 show_out = False,
                 text_color: str = None,
                 history = 'pods',
                 debug: bool = False,
                 bg_init_msg: Union[str, bool] = None,
                 job_id: str = None,
                 retriable = False):
        self.cmd = cmd
        self.raw_cmd = thread_local_command().raw_command
        self.background = background
        self.show_out = show_out
        self.text_color = text_color
        self.history = history
        self.debug = debug
        if self.debug is None:
            self.debug = ConfigHolder().config.is_debug()
        self.bg_init_msg = bg_init_msg

        self.log_file: str = None
        self._histories = set()
        self.job_id = job_id
        self._pod_log_file: str = None
        self.retriable = retriable

        if background:
            self._init_backgrounded()

    def _init_backgrounded(self, extra: dict[str, str] = {}):
        if not self.job_id:
            self.job_id = Job.new_id(cmd=self.cmd)

            if self.bg_init_msg is not False:
                bg_init_msg = self.bg_init_msg
                if bg_init_msg is None:
                    bg_init_msg = '[{job_id}] Use :? to get the results.'

                bg_init_msg = bg_init_msg.replace('{job_id}', self.job_id)
                if bg_init_msg:
                    log2(bg_init_msg)

        log_file = Job.local_log_file(self.cmd, self.job_id, extra=extra, retriable=self.retriable)
        self.log_file = log_file

    def log(self, s = None, nl = True, text_color: str = None, debug = False):
        return self._log(s=s, nl=nl, text_color=text_color, debug=debug)

    def log2(self, s = None, nl = True, text_color: str = None, debug = False):
        return self._log(s=s, nl=nl, text_color=text_color, err=True, debug=debug)

    def _log(self, s = None, nl = True, text_color: str = None, err = False, debug = False):
        if self.log_file and self.history in [Context.ALL, Context.LOCAL]:
            self.append_history(f':tail {self.log_file}')

        if self.show_out:
            if debug:
                if not text_color:
                    text_color = Color.gray

                return _log(s=s, nl=nl, file=self.log_file if self.background else None, text_color=text_color, err=err)
            else:
                if not text_color:
                    text_color = self.text_color

                return _log(s=s, nl=nl, file=self.log_file if self.background else None, text_color=text_color, err=err)

    def pod_log_file(self, pod: str = None, suffix = '.log', history=True):
        if self._pod_log_file:
            return self._pod_log_file

        pod_log_file, pod_log_cnt = Job.pod_log_file(self.cmd, job_id=self.job_id, pod_suffix='', suffix=suffix, dir=Directories.remote_log_dir(), retriable=self.retriable)
        # append only the first accessed pod log to history
        if not pod_log_cnt and pod and history and self.history in [Context.ALL, Context.PODS]:
            self.append_history(f'@{pod} tail {pod_log_file}')

        return pod_log_file

    def append_history(self, command: str):
        if command not in self._histories:
            ReplSession().append_history(command)

            self._histories.add(command)

    # simple version with no message or specific thread pool
    def submit(self, fn: Callable[..., T], /, *args, **kwargs):
        with offload(self.background) as submit:
            submit(fn, *args, **kwargs)

    def switch_to_job_context(self, job_id: str):
        job: Job = Job.job(job_id)
        job_ctx = self.copy(cmd=job.command, job_id=job.job_id)
        job_ctx._init_backgrounded()

        return job_ctx

# the null object pattern
NULL = Context(None, background=False)