from datetime import datetime
import html
import json
import os
import threading
import traceback
from typing import Callable, TypeVar, Union
import sys
import time
import click
from prompt_toolkit import print_formatted_text, HTML

from adam.config_holder import ConfigHolder
from adam.utils_color import Color
from adam.utils_fs import creating_dir

T = TypeVar('T')

log_state = threading.local()

def log(s = None, file: str = None, text_color: str = None):
    return _log(s=s, file=file, text_color=text_color)

def log2(s = None, nl = True, file: str = None, text_color: str = None):
    return _log(s=s, nl=nl, file=file, text_color=text_color, err=True)

def _log(s = None, nl = True, file: str = None, text_color: str = None, err = False):
    if not loggable():
        return False

    if s:
        if isinstance(s, Exception):
            s = str(s)

        if file:
            with open(file, 'at') as f:
                f.write(s)
                if nl:
                    f.write('\n')
        elif text_color:
            l = f'<ansi{text_color}>{html.escape(s)}</ansi{text_color}>'
            try:
                print_formatted_text(HTML(l), file=sys.stderr if err else None, end='\n' if nl else '')
            except:
                click.echo(s, err=err, nl=nl)
        else:
            click.echo(s, err=err, nl=nl)
    else:
        if file:
            with open(file, 'at') as f:
                f.write('\n')
        else:
            print(file=sys.stderr if err else None)

    return True

def debug(s = None):
    if ConfigHolder().config.is_debug():
        log2(s, text_color=Color.gray)

def debug_complete(s = None):
    CommandLog.log(s, config=ConfigHolder().config.get('debugs.complete', 'off'))

def debug_trace():
    if ConfigHolder().config.is_debug():
        log2(traceback.format_exc(), text_color=Color.gray)

class Ing:
    def __init__(self, msg: str, suppress_log=False, job_log: str = None, condition = True):
        self.msg = msg
        self.suppress_log = suppress_log
        self.job_log = job_log
        self.condition = condition

    def __enter__(self):
        if not self.condition:
            return None

        if not hasattr(log_state, 'ing_cnt'):
            log_state.ing_cnt = 0

        try:
            if not log_state.ing_cnt:
                if not self.suppress_log and not ConfigHolder().config.is_debug():
                    log2(f'{self.msg}...', nl=False, file=self.job_log)

            return None
        finally:
            log_state.ing_cnt += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.condition:
            return False

        log_state.ing_cnt -= 1
        if not log_state.ing_cnt:
            if not self.suppress_log and not ConfigHolder().config.is_debug():
                log2(' OK', file=self.job_log)

        return False

def ing(msg: str, body: Callable[[], None]=None, suppress_log=False, job_log: str = None, condition = True):
    if not body:
        return Ing(msg, suppress_log=suppress_log, job_log=job_log, condition=condition)

    r = None

    t = Ing(msg, suppress_log=suppress_log)
    t.__enter__()
    try:
        r = body()
    finally:
        t.__exit__(None, None, None)

    return r

def loggable():
    return ConfigHolder().config and ConfigHolder().config.is_debug() or not hasattr(log_state, 'ing_cnt') or not log_state.ing_cnt

class TimingNode:
    def __init__(self, depth: int, s0: time.time = time.time(), line: str = None):
        self.depth = depth
        self.s0 = s0
        self.line = line
        self.children = []

    def __str__(self):
        return f'[{self.depth}: {self.line}, children={len(self.children)}]'

    def tree(self):
        lines = []
        if self.line:
            lines.append(self.line)

        for child in self.children:
            if child.line:
                lines.append(child.tree())
        return '\n'.join(lines)

class LogTiming:
    def __init__(self, msg: str, s0: time.time = None):
        self.msg = msg
        self.s0 = s0

    def __enter__(self):
        if (config := ConfigHolder().config.get('debugs.timings', 'off')) not in ['on', 'file']:
            return

        if not hasattr(log_state, 'timings'):
            log_state.timings = TimingNode(0)

        self.me = log_state.timings
        log_state.timings = TimingNode(self.me.depth+1)
        if not self.s0:
            self.s0 = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if (config := ConfigHolder().config.get('debugs.timings', 'off')) not in ['on', 'file']:
            return False

        if hasattr(log_state, 'timings'):
            child = log_state.timings
            log_state.timings.line = timing_log_line(self.me.depth, self.msg, self.s0)

            if child and child.line:
                self.me.children.append(child)
            log_state.timings = self.me

            if not self.me.depth:
                # log timings finally
                CommandLog.log(self.me.tree(), config)

                log_state.timings = TimingNode(0)

        return False

def log_timing(msg: str, body: Callable[..., T]=None, s0: time.time = None) -> T:
    if not s0 and not body:
        return LogTiming(msg, s0=s0)

    if not ConfigHolder().config.get('debugs.timings', False):
        if body:
            return body()

        return

    r: T = None

    t = LogTiming(msg, s0=s0)
    t.__enter__()
    try:
        if body:
            r = body()
    finally:
        t.__exit__(None, None, None)

    return r

def timing_log_line(depth: int, msg: str, s0: time.time):
    elapsed = time.time() - s0
    offloaded = '-' if threading.current_thread().name.startswith('offload') or threading.current_thread().name.startswith('async') else '+'
    prefix = f'[{offloaded} timings] '

    if depth:
        if elapsed > 0.01:
            prefix = ('  ' * (depth-1)) + '* '
        else:
            prefix = '  ' * depth

    return f'{prefix}{msg}: {elapsed:.2f} sec'

class WaitLog:
    wait_log_flag = False

def wait_log(msg: str):
    if not WaitLog.wait_log_flag:
        if threading.current_thread().name == 'MainThread':
            # disable wait logs if not on main thread
            log2(msg)

        WaitLog.wait_log_flag = True

def clear_wait_log_flag():
    WaitLog.wait_log_flag = False

class LogTrace:
    def __init__(self, err_msg: Union[str, callable, bool] = None):
        self.err_msg = err_msg

    def __enter__(self):
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            if self.err_msg is True:
                log2(str(exc_val))
            elif callable(self.err_msg):
                log2(self.err_msg(exc_val))
            elif self.err_msg is not False and self.err_msg:
                log2(self.err_msg)

            if self.err_msg is not False and ConfigHolder().config.is_debug():
                traceback.print_exception(exc_type, exc_val, exc_tb, file=sys.stderr)

        # swallow exception
        return True

def log_exc(err_msg: Union[str, callable, bool] = None):
    return LogTrace(err_msg=err_msg)

def kaqing_log_file_name(suffix = 'log', job_id: str = None):
    if not job_id:
        job_id = datetime.now().strftime('%d%H%M%S')
    return f"{log_dir()}/{job_id}.{suffix}"

def log_dir():
    return creating_dir(ConfigHolder().config.get('log-dir', '/tmp/qing-db/q/logs'))

def pod_log_dir():
    return ConfigHolder().config.get('pod-log-dir', '/tmp/q/logs')

class LogFileHandler:
    def __init__(self, suffix = 'log', condition=True):
        self.suffix = suffix
        self.condition = condition

    def __enter__(self):
        self.f = None
        if self.condition:
            self.f = open(kaqing_log_file_name(suffix=self.suffix), 'w')
            self.f.__enter__()

        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.f:
            self.f.__exit__(exc_type, exc_val, exc_tb)

            if ConfigHolder().append_command_history:
                ConfigHolder().append_command_history(f':cat {self.f.name}')

        return False

def kaqing_log_file(suffix = 'log', condition=True):
    return LogFileHandler(suffix = suffix, condition=condition)

class CommandLog:
    log_file = None

    def log(line: str, config: str = 'off'):
        if config == 'file':
            if not CommandLog.log_file:
                try:
                    CommandLog.log_file = open(kaqing_log_file_name(suffix='cmd.log'), 'w')
                except:
                    pass

            try:
                CommandLog.log_file.write(line + '\n')
            except:
                pass
        elif config == 'on':
            log2(line, text_color=Color.gray)

    def close_log_file():
        if CommandLog.log_file:
            try:
                CommandLog.log_file.close()
            except:
                pass

            if ConfigHolder().append_command_history:
                ConfigHolder().append_command_history(f':cat {CommandLog.log_file.name}')

            CommandLog.log_file = None

class LogFile(str):
    def __init__(self, s: str):
        super().__init__()

    def __repr__(self):
        return super().__repr__()

    def to_command(self, cmd: str = ':tail'):
        return f'{cmd} {self}'

class PodLogFile(LogFile):
    def __new__(cls, value, pod: str, pid: str = None, size: str = None, exit_code: str = None):
        return super().__new__(cls, value)

    def __init__(self, value, pod: str, pid: str = None, size: str = None, exit_code: str = None):
         super().__init__(value)
         self.pod = pod
         self.pid = pid
         self.size = size
         self.exit_code = exit_code

    def __repr__(self):
        return super().__repr__()

    def to_command(self, cmd: str = 'tail'):
        return f'@{self.pod} {cmd} {self}'

# used until logging system is bootstrapped
class Log:
    DEBUG = False

    def is_debug():
        return Log.DEBUG

    def debug(s: None):
        if Log.DEBUG:
            Log.log2(f'DEBUG {s}')

    def log(s = None):
        # want to print empty line for False or empty collection
        if s == None:
            print()
        else:
            click.echo(s)

    def log2(s = None):
        if s:
            click.echo(s, err=True)
        else:
            print(file=sys.stderr)

    def log_to_file(config: dict[any, any]):
        with log_exc():
            base = f"/tmp/logs"
            os.makedirs(base, exist_ok=True)

            now = datetime.now()
            timestamp_str = now.strftime("%Y%m%d-%H%M%S")
            filename = f"{base}/login.{timestamp_str}.txt"
            with open(filename, 'w') as f:
                if isinstance(config, dict):
                    try:
                        json.dump(config, f, indent=4)
                    except:
                        f.write(config)
                else:
                        f.write(config)