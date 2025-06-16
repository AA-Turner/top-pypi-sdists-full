# SPDX-FileCopyrightText: (c) 2021 Arteom iG (rtmigo.github.io)
# SPDX-License-Identifier: MIT
import os
import sys
from pathlib import Path
from subprocess import run as run_process, PIPE, STDOUT, \
    CompletedProcess
from tempfile import TemporaryDirectory
from typing import Optional, List, Union, Type, Any

from ._cleaner import BuildCleaner
from ._exceptions import TwineCheckFailed, FailedToInstallPackage, \
    CannotInitializeEnvironment, CodeExecutionFailed, CompletedProcessError
from ._require_pytyped import get_module_path, require_dir_contains_pytyped
from ._venvs import TempVenv


def print_command(cmd: Union[str, List[str]], title: str, at: str):
    print()
    print('== ' + title.upper() + ' ' +
          ('=' * (80 - len(at) - len(title) - 4 - 4)) +
          ' ' + at + ' ==')
    if isinstance(cmd, str):
        print(cmd)
    else:
        print(' '.join(repr(arg) for arg in cmd))
    print('=' * 80)
    print()


def find_latest_wheel(parent_dir: Path) -> Path:
    """Finds *.whl file with the latest modification time"""
    files = [(f.stat().st_mtime, f) for f in parent_dir.glob('*.whl')]
    if not files:
        raise FileNotFoundError(".whl file not found")
    max_mod_time = max((mt for mt, _ in files))
    max_mod_time_file = next(f for t, f in files if t == max_mod_time)
    return max_mod_time_file


class Runner:
    """Prints the commands to the stdout with the same 'at' comments.
    Runs python commands with the same executable.
    """

    def __init__(self, python_exe, at):
        self.python_exe = python_exe
        self.at = at

    def python(self,
               args: Union[str, List[str]],
               title: str,
               cwd: Union[Path, str] = None,
               exception: Type[BaseException] = None):

        args_list = args.split() if isinstance(args, str) else args
        args_list = [self.python_exe] + args_list
        return self._run(args_list, title, cwd, exception)

    def command(self,
                args: Union[str, List[str]],
                title: str,
                cwd: Union[Path, str] = None,
                exception: Type[BaseException] = None,
                executable: str = None,
                shell: bool = False,
                expected_return_code: int = 0):
        args_list = args
        return self._run(args_list, title, cwd, exception,
                         executable=executable, shell=shell,
                         expected_return_code=expected_return_code)

    def _run(self,
             args_list,
             title: str,
             cwd: Union[Path, str] = None,
             exception: Type[BaseException] = None,
             executable: str = None,
             shell: bool = False,
             expected_return_code: int = 0):

        print_command(cmd=args_list, at=self.at, title=title)

        cp = run_process(args_list, cwd=cwd, encoding=sys.stdout.encoding,
                         stdout=PIPE, stderr=STDOUT,
                         executable=executable,
                         shell=shell,
                         universal_newlines=True)

        output = cp.stdout.rstrip()
        if output:
            print(output)

        if cp.returncode != expected_return_code:
            if exception is None:
                exception = CompletedProcessError
            if exception == CompletedProcessError:
                raise CompletedProcessError(process=cp)
            raise exception()
            # if exception is None:
            #     # the CalledProcessError always prints something like
            #     # "greeter_cli hi' returned non-zero exit status 0."
            #     # The message is a bit weird, but the exception is the
            #     # most common and expected
            #     raise CalledProcessError(cp.returncode, args_list, cp.stdout,
            #                              cp.stderr)
            # elif exception==CodeExecutionFailed:
            #     raise CodeExecutionFailed(
            #         "Unexpected return code",
            #         process=cp
            #     )
            # else:
            #     raise exception()

        return cp


class Package:
    """During initialization, this object creates a .whl distribution
    and installs the packages from the distribution into a test virtual
    environment.

    After that, using the methods of the object, we can execute commands
    in the test environment, checking that the packages were
    installed correctly."""

    def __init__(self, project_dir: Union[str, Path] = '.'):
        # we will call __exit__ for each of the following objects
        self._exit_on_cleanup: List[Any] = list()

        self._installer: Optional[Runner] = None
        self.project_source_dir = Path(project_dir).absolute()
        self.installer_venv: Optional[TempVenv] = None

    def __enter__(self):
        self.init()
        return self

    def init(self):
        builder_venv = TempVenv()
        self._exit_on_cleanup.append(builder_venv)
        builder_python_exe: str = builder_venv.__enter__()
        builder_runner = Runner(builder_python_exe, at='builder venv')

        # INSTALLING BUILD ####################################################

        builder_runner.python('-m pip install --upgrade pip',
                              title='Upgrading pip',
                              exception=CannotInitializeEnvironment)
        builder_runner.python('-m pip install --upgrade build',
                              title='Installing build',
                              exception=CannotInitializeEnvironment)

        with TemporaryDirectory() as temp_dist_dir:
            # BUILDING ########################################################

            with BuildCleaner(self.project_source_dir):
                builder_runner.python(
                    ['-m', 'build', '--outdir', temp_dist_dir, '--wheel'],
                    title='Building the .whl',
                    cwd=self.project_source_dir)

            # finding the .whl file we just created
            newly_built_whl_file: Path = find_latest_wheel(Path(temp_dist_dir))
            newly_built_whl_file = newly_built_whl_file.absolute()
            print(f'Latest wheel: {newly_built_whl_file}')

            # TWINE CHECK #####################################################

            # 2021-11: python3.9 -m build creates .whl unsupported by twine.
            #
            # InvalidDistribution: Invalid distribution metadata.
            # This version of twine supports Metadata-Version 1.0, 1.1, 1.2,
            # 2.0, and 2.1.

            builder_runner.python('-m pip install --upgrade twine',
                                  title='Installing twine',
                                  exception=CannotInitializeEnvironment)

            # running twine checks on the new file
            builder_runner.python(['-m', 'twine', 'check',
                                   str(newly_built_whl_file),
                                   '--strict'],
                                  title='Twine check',
                                  exception=TwineCheckFailed)

            # TEST VENV #######################################################

            self.installer_venv = TempVenv()
            self._exit_on_cleanup.append(self.installer_venv)
            installer_python_exe: str = self.installer_venv.__enter__()
            self._installer = Runner(installer_python_exe, at='installer venv')

            self._installer.python('-m pip install --upgrade pip',
                                   title='Upgrading pip',
                                   exception=CannotInitializeEnvironment)

            self._installer.python(
                ['-m', 'pip', 'install', '--force-reinstall',
                 str(newly_built_whl_file)],
                title=f'Installing {newly_built_whl_file.name}',
                exception=FailedToInstallPackage)

    def cleanup(self, exc_type=None, exc_val=None, exc_tb=None):
        for x in reversed(self._exit_on_cleanup):
            x.__exit__(exc_type, exc_val, exc_tb)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup(exc_type, exc_val, exc_tb)

    @staticmethod
    def _output(cp: CompletedProcess, rstrip: bool = True) -> str:
        o: str = cp.stdout
        if rstrip:
            o = o.rstrip()
        return o

    def run_python_code(self, code: str, rstrip: bool = True) -> str:
        assert self._installer is not None
        with TemporaryDirectory() as temp_current_dir:
            cp = self._installer.python(
                ['-c', code],
                title="Running Python code (cwd is temp dir)",
                cwd=temp_current_dir,
                exception=CodeExecutionFailed)
            return self._output(cp, rstrip)

    @property
    def _can_run_bash(self):
        return os.path.exists("/bin/bash")

    def _run_bash_code(self, code: str, rstrip: bool = True,
                       expected_return_code: int = 0):

        with TemporaryDirectory() as temp_cwd:
            assert self.installer_venv is not None
            activate = self.installer_venv.paths.posix_bash_activate
            code = '\n'.join(["#!/bin/bash",
                              "set -e",
                              f'source "{activate}"',
                              code])

            # we need executable='/bin/bash' for Ubuntu 18.04, it will run
            # '/bin/sh' otherwise. For MacOS 10.13 it seems to be optional
            assert self._installer is not None
            cp = self._installer.command(
                code,
                title="Running Bash code (cwd is temp dir)",
                cwd=temp_cwd,
                executable='/bin/bash',
                shell=True,
                exception=CodeExecutionFailed,
                expected_return_code=expected_return_code
            )

            return self._output(cp, rstrip)

    def _run_cmdexe_code(self, code: str,
                         rstrip: bool = True,
                         expected_return_code: int = 0):
        """Runs command in cmd.exe"""
        with TemporaryDirectory() as temp_cwd:
            assert self.installer_venv is not None
            activate_bat = self.installer_venv.paths.windows_cmdexe_activate

            # temp file with commands to run
            temp_bat_file = Path(temp_cwd) / "_run_cmdexe_code.bat"
            temp_bat_file.write_text(
                '\n'.join([f"CALL {activate_bat}",
                           code]))

            # todo param /u formats output as unicode?
            assert self._installer is not None
            cp = self._installer.command(
                ["cmd.exe", "/q", "/c", str(temp_bat_file)],
                title="Running code in cmd.exe (cwd is temp dir)",
                cwd=temp_cwd,
                shell=False,
                exception=CodeExecutionFailed,
                expected_return_code=expected_return_code)

            return self._output(cp, rstrip)

    def run_shell_code(self, code: str, rstrip: bool = True,
                       expected_return_code: int = 0) -> str:
        if os.name == 'nt':
            method = self._run_cmdexe_code
        else:
            method = self._run_bash_code
        return method(code, rstrip=rstrip,
                      expected_return_code=expected_return_code)

    def require_pytyped(self, module: str):
        assert self._installer is not None
        path = get_module_path(self._installer.python_exe, module)
        require_dir_contains_pytyped(path.parent)
