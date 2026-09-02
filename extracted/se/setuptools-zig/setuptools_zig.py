# coding: utf-8

import sys
import os
import subprocess
import platform
from pathlib import Path
from datetime import datetime as DateTime

from distutils.dist import Distribution
from setuptools.command.build_ext import build_ext as SetupToolsBuildExt


_version = "0.5.3"


class ZigCompilerError(Exception):
    """Some compile/link operation failed."""


class Debug:
    def __init__(self):
        self.first_time = True
        self.verbose = None
        try:
            vbs = os.environ['SETUPTOOLS_ZIG_VERBOSE']
            # self.print('getting setuptools')
            self.verbose = int(vbs)
        except KeyError:
            # self.print('>>> keyerror SETUPTOOLS_ZIG_VERBOSE')
            pass
        except ValueError:
            self.print(f'cannot interpret "{vbs}" as integer')
        if self.verbose is None:
            if '-v' in sys.argv:
                self.verbose = 1
            elif '-vv' in sys.argv:
                self.verbose = 2
            else:
                self.verbose = 0

    def print(self, *args):
        if self.verbose == 0:
            return
        tmpdir = Path(os.environ.get('TEMP', '/tmp'))
        with (tmpdir / 'setuptools_zig_debug.txt').open('a') as fh:
            if self.first_time:
                self.first_time = False
                print(f'\n\n{DateTime.now().replace(microsecond=0)} setuptools_zig: {_version}\n', file=fh)
            print(*args, file=fh)

    def __call__(self, *args):
        return self.print(*args)


debug = Debug()

zig = 'zig'  # if nothing else just try the command
try:
    import ziglang  # NOQA
    zig_dir = Path(ziglang.__file__).parent
    # setting env didn't work for Unifi alpine, as zig did not have executable bit set
    # as indicated by amalachowski https://sourceforge.net/p/ruamel-yaml-clibz/tickets/2/#9468
    zig_path = zig_dir / ('zig' + ('.exe' if platform.system() == 'Windows' else ''))
    zig_path.chmod(0o755)
    debug('zig executable', zig_path)
    debug('zig executable permissions:', oct(zig_path.stat().st_mode))
    zig = str(zig_path)
except ModuleNotFoundError as e:
    debug('could not import ziglang', e)
except Exception as e:
    debug('Exception finding zig', e)
zig = os.environ.get('PY_ZIG', zig)  # override zig in path, or found from ziglang, with specific version


# ext attributes:
#   define_macros
#   depends
#   export_symbols
#   extra_compile_args
#   extra_link_args
#   extra_objects
#   include_dirs
#   language
#   libraries
#   library_dirs
#   name
#   optional
#   py_limited_api
#   runtime_library_dirs
#   sources
#   swig_opts
#   undef_macros


class BuildExt(SetupToolsBuildExt):
    def __init__(self, dist, zig_value):
        self._zig_value = zig_value
        super().__init__(dist)

    def build_extension(self, ext):
        if not self._zig_value:
            return super().build_extension(ext)
        # debug(f'{debug.verbose=}')

        # check if every file in ext.sources exists
        for p in ext.sources:
            assert Path(p).exists()

        target = Path(self.get_ext_fullpath(ext.name))
        target.parent.mkdir(exist_ok=True, parents=True)  # subdir of build, not created by zig

        # zig = os.environ.get('PY_ZIG', 'zig')  # override zig in path with specific version
        bld_cmd = [
           zig,
           'build-lib',
           '-dynamic',
           '-fallow-shlib-undefined',  # if not specified you have to provide -L and -lpythonX.Y otherwise undefined symbols
           f'-femit-bin={target.resolve()}',  # windows needs absolute path
            '-lc',
        ]
        inc_dirs_added = set()
        for inc_dir in self.compiler.include_dirs:
            inc_dir_p = Path(inc_dir).resolve()  # because you can have xyz/Include and xyz/include from windows setup
            if not inc_dir_p.exists() or inc_dir_p in inc_dirs_added:
                continue
            inc_dirs_added.add(inc_dir_p)
            bld_cmd.extend(('-I', str(inc_dir_p)))
        for path in [
            '/usr/include',  # needed for docker compilation
            # '/usr/include/x86_64-linux-gnu/',  # cannot find how to get this from sysconfig or platform
        ]:
            path = Path(path)
            if not path.exists() or path in inc_dirs_added:
                continue
            inc_dirs_added.add(path)
            bld_cmd.extend(('-I', str(path)))
        for path in Path('/usr/include').glob('*-linux-gnu'):
            if path in inc_dirs_added:
                continue
            inc_dirs_added.add(path)
            bld_cmd.extend(('-I', str(path)))
        # debug('comp libdir:', self.compiler.library_dirs)
        # debug('ext  libdir:', ext.library_dirs)
        # debug('comp libs:', self.compiler.libraries)
        # debug('ext  libs:', ext.libraries)
        lib_dirs_added = set()
        for lib_dir in self.compiler.library_dirs:
            if not Path(lib_dir).exists() or lib_dir in lib_dirs_added:
                continue
            lib_dirs_added.add(lib_dir)
            bld_cmd.extend(('-L', str(lib_dir)))
        for lib_dir in ext.library_dirs:
            if not Path(lib_dir).exists() or lib_dir in lib_dirs_added:
                continue
            lib_dirs_added.add(lib_dir)
            bld_cmd.extend(('-L', str(lib_dir)))
        if '-O' not in ext.extra_compile_args:
            bld_cmd.extend(('-O', 'ReleaseFast'))
        bld_cmd.extend(ext.extra_compile_args)
        if platform.system() == 'Windows':
            # if '-target' not in bld_cmd:
            #     bld_cmd.extend(('-target', 'native-native-gnu'))
            bld_cmd.append(f'-lpython{sys.version_info.major}{sys.version_info.minor}')
        bld_cmd.extend(ext.sources)
        if debug.verbose > 1:
            debug('ext:')
            for elem in dir(ext):
                if elem and (elem[0] != '_'):
                    debug(f' {elem} -> {getattr(ext, elem)}')
            debug('compiler:')
            for k, v in self.compiler.__dict__.items():
                debug(f' {k} -> {v}')
        debug('cmd',  " ".join([x if " " not in x else '"' + x + '"' for x in bld_cmd]))
        print('cmd',  " ".join([x if " " not in x else '"' + x + '"' for x in bld_cmd]))
        print()
        sys.stdout.flush()
        res = subprocess.run(bld_cmd, capture_output=True, encoding='utf-8')
        if res.returncode != 0 or res.stderr:
            print('\nrun return:\n', res)
            print('\n')
            raise ZigCompilerError(res.stderr)
        debug('res:', res)
        debug('\ntarget:', [str(target)])
        debug('found:', [str(x) for x in target.parent.glob('*')])


class ZigBuildExtension:
    def __init__(self, value):
        self._value = value

    def __call__(self, dist):
        return BuildExt(dist, zig_value=self._value)


def setup_build_zig(dist, keyword, value):
    assert isinstance(dist, Distribution)
    assert keyword == 'build_zig'
    be = dist.cmdclass.get('build_ext')
    dist.cmdclass['build_ext'] = ZigBuildExtension(value)
