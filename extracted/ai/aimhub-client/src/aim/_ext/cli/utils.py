import os
import sys
import subprocess
import logging
from aim._sdk.configs import AIM_LOG_LEVEL_KEY


class ShellCommandException(Exception):
    pass


def set_log_level(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % log_level)
    os.environ[AIM_LOG_LEVEL_KEY] = str(numeric_level)
    logging.basicConfig(level=numeric_level)


def build_uvicorn_command(app,
                          host='0.0.0.0',
                          port=0,
                          workers=1,
                          uds=None,
                          ssl_keyfile=None,
                          ssl_certfile=None,
                          log_level='warning',
                          reload=False,
                          reload_dirs=[]):
    cmd = [sys.executable, '-m', 'uvicorn',
           '--ws-max-size', '1073741824',  # 1MB
           '--host', host, '--port', f'{port}',
           '--workers', f'{workers}']
    if reload:
        cmd += ['--reload', '--reload-dirs', reload_dirs]
    if uds:
        cmd += ['--uds', uds]
    if ssl_keyfile:
        cmd += ['--ssl-keyfile', ssl_keyfile]
    if ssl_certfile:
        cmd += ['--ssl-certfile', ssl_certfile]
    cmd += ['--log-level', log_level.lower()]
    cmd += [app]
    return cmd


def exec_cmd(
    cmd, throw_on_error=True, env=None, stream_output=False, cwd=None, cmd_stdin=None, **kwargs
):
    """
    Runs a command as a child process.
    A convenience wrapper for running a command from a Python script.
    Keyword arguments:
    cmd -- the command to run, as a list of strings
    throw_on_error -- if true, raises an Exception if the exit code of the program is nonzero
    env -- additional environment variables to be defined when running the child process
    cwd -- working directory for child process
    stream_output -- if true, does not capture standard output and error; if false, captures these
      streams and returns them
    cmd_stdin -- if specified, passes the specified string as stdin to the child process.
    Note on the return value: If stream_output is true, then only the exit code is returned. If
    stream_output is false, then a tuple of the exit code, standard output and standard error is
    returned.
    """
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)
    if stream_output:
        child = subprocess.Popen(
            cmd, env=cmd_env, cwd=cwd, universal_newlines=True, stdin=subprocess.PIPE, **kwargs
        )
        child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code != 0:
            raise ShellCommandException("Non-zero exitcode: %s" % (exit_code))
        return exit_code
    else:
        child = subprocess.Popen(
            cmd,
            env=cmd_env,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            universal_newlines=True,
            **kwargs
        )
        (stdout, stderr) = child.communicate(cmd_stdin)
        exit_code = child.wait()
        if throw_on_error and exit_code != 0:
            raise ShellCommandException(
                "Non-zero exit code: %s\n\nSTDOUT:\n%s\n\nSTDERR:%s" % (exit_code, stdout, stderr)
            )
        return exit_code, stdout, stderr


def start_uvicorn_app(app: str, **uvicorn_args):
    cmd = build_uvicorn_command(app, **uvicorn_args)
    exec_cmd(cmd, stream_output=True)


def get_free_port_num():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port_num = s.getsockname()[1]
    s.close()
    return port_num
