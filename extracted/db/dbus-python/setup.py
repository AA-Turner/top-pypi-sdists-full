#!/usr/bin/env python
# encoding: utf-8

# Copyright © 2016 Collabora Ltd. <http://www.collabora.co.uk/>
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from setuptools.dist import Distribution
from setuptools import setup, Extension
import os
import subprocess
import sys


if (
    os.environ.get('DBUS_PYTHON_USE_AUTOTOOLS', '')
    or sys.version_info < (3, 7)
):
    use_autotools = True
    setup_requires = ['setuptools', 'wheel']
else:
    use_autotools = False
    setup_requires = ['meson>=0.60.0', 'ninja', 'setuptools', 'wheel']

if os.path.exists('.version'):
    version = open('.version').read().strip()
elif use_autotools:
    version = subprocess.check_output(['autoconf', '--trace', 'AC_INIT:$2',
        'configure.ac']).decode('utf-8').strip()
else:
    with open('meson.build') as reader:
        for line in reader:
            if line.strip().replace(' ', '').startswith('version:'):
                version = line.split(':', 1)[1]
                version = version.replace(',', '')
                version = version.replace('"', '')
                version = version.replace("'", '')
                break
        else:
            raise AssertionError('Cannot find version in meson.build')

class Build(Distribution().get_command_class('build')):
    """Dummy version of distutils build which runs an Autotools or Meson
    build system instead.
    """

    def run(self):
        srcdir = os.getcwd()
        builddir = os.path.join(srcdir, self.build_temp)
        os.makedirs(builddir, exist_ok=True)

        if use_autotools:
            configure = os.path.join(srcdir, 'configure')

            if not os.path.exists(configure):
                configure = os.path.join(srcdir, 'autogen.sh')

            subprocess.check_call([
                    configure,
                    '--disable-maintainer-mode',
                    'PYTHON=' + sys.executable,
                    # Put the documentation, etc. out of the way: we only want
                    # the Python code and extensions
                    '--prefix=' + os.path.join(builddir, 'prefix'),
                ],
                cwd=builddir)
            make_args = [
                'pythondir=' + os.path.join(srcdir, self.build_lib),
                'pyexecdir=' + os.path.join(srcdir, self.build_lib),
            ]
            subprocess.check_call(['make', '-C', builddir] + make_args)
            subprocess.check_call(['make', '-C', builddir, 'install'] + make_args)
        else:
            subprocess.check_call(
                [
                    sys.executable,
                    '-m', 'mesonbuild.mesonmain',
                    '--prefix=' + os.path.join(builddir, 'prefix'),
                    '-Ddoc=disabled',
                    '-Dinstalled_tests=false',
                    '-Dpython=' + sys.executable,
                    '-Dpython.platlibdir=' + os.path.join(srcdir, self.build_lib),
                    '-Dpython.purelibdir=' + os.path.join(srcdir, self.build_lib),
                    '-Dtests=disabled',
                    srcdir,
                    builddir,
                ]
            )
            subprocess.check_call(['meson', 'compile', '-C', builddir])
            subprocess.check_call(['meson', 'install', '-C', builddir])

class BuildExt(Distribution().get_command_class('build_ext')):
    def run(self):
        pass

class BuildPy(Distribution().get_command_class('build_py')):
    def run(self):
        pass

dbus_bindings = Extension('_dbus_bindings',
        sources=['dbus_bindings/module.c'])
dbus_glib_bindings = Extension('_dbus_glib_bindings',
        sources=['dbus_glib_bindings/module.c'])

setup(
    name='dbus-python',
    version=version,
    packages=['dbus'],
    ext_modules=[dbus_bindings, dbus_glib_bindings],
    cmdclass={
        'build': Build,
        'build_py': BuildPy,
        'build_ext': BuildExt,
    },
    setup_requires=setup_requires,
    tests_require=['tap.py'],
)
