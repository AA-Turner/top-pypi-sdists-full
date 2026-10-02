#!/usr/bin/env python

# Copyright (C) 2016-2018 g10 Code GmbH
# Copyright (C) 2004,2008 Igor Belyi <belyi@users.sourceforge.net>
# Copyright (C) 2002 John Goerzen <jgoerzen@complete.org>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA

import os
import os.path
import re
import shutil
import subprocess
import sys

from setuptools import setup, Extension
from setuptools.command.build import build

# Out-of-tree build of the gpg bindings.
gpgme_h = ''
include_dirs = [os.getcwd()]
library_dirs = []

if hasattr(subprocess, 'DEVNULL'):
    devnull = subprocess.DEVNULL
else:
    devnull = open(os.devnull, 'w')


version = version_raw = "2.0.0"
if '-' in version:
    version = version.split('-')[0]
major, minor, patch = map(int, version.split('.'))

if not (major > 1 or (major == 1 and minor >= 7)):
    sys.exit('Need at least GPGME version 1.7, found {}.'.format(version_raw))

libs = []
if '-L/usr/lib/x86_64-linux-gnu -lgpg-error':
    libs += '-L/usr/lib/x86_64-linux-gnu -lgpg-error'.split(' ')
if '-L/usr/lib/x86_64-linux-gnu -lgpgme':
    libs += '-L/usr/lib/x86_64-linux-gnu -lgpgme'.split(' ')

define_macros = []
if '':
    for item in ''.split(' '):
        if item.startswith('-I'):
            include_dirs.append(item[2:])
        elif item.startswith('-D'):
            defitem = item[2:].split('=', 1)
            if len(defitem) == 2:
                define_macros.append((defitem[0], defitem[1]))
            else:
                define_macros.append((defitem[0], None))
if '':
    for item in ''.split(' '):
        if item.startswith('-I'):
            include_dirs.append(item[2:])
        elif item.startswith('-D'):
            defitem = item[2:].split('=', 1)
            if len(defitem) == 2:
                define_macros.append((defitem[0], defitem[1]))
            else:
                define_macros.append((defitem[0], None))

# Adjust include and library locations in case of win32
uname_s = os.popen('uname -s').read()
if uname_s.startswith('MINGW32'):
    mnts = [
        x.split()[0:3:2] for x in os.popen('mount').read().split('\n') if x
    ]
    tmplist = sorted([(len(x[1]), x[1], x[0]) for x in mnts])
    tmplist.reverse()
    extra_dirs = []
    for item in include_dirs:
        for ln, mnt, tgt in tmplist:
            if item.startswith(mnt):
                item = os.path.normpath(item[ln:])
                while item[0] == os.path.sep:
                    item = item[1:]
                extra_dirs.append(os.path.join(tgt, item))
                break
    include_dirs += extra_dirs
    for item in [x[2:] for x in libs if x.startswith('-L')]:
        for ln, mnt, tgt in tmplist:
            if item.startswith(mnt):
                item = os.path.normpath(item[ln:])
                while item[0] == os.path.sep:
                    item = item[1:]
                library_dirs.append(os.path.join(tgt, item))
                break

if not gpgme_h:
    if os.path.exists(os.path.join('/usr/local', 'include', 'gpgme.h')):
        gpgme_h = os.path.join('/usr/local', 'include', 'gpgme.h')
    else:
        for include_dir in (include_dirs + ['/usr/include']):
            if os.path.exists(os.path.join(include_dir, 'gpgme.h')):
                gpgme_h = os.path.join(include_dir, 'gpgme.h')
                break

if not gpgme_h:
    sys.exit('gpgme.h not found.')


def in_srcdir(name):
    return os.path.join(os.environ.get('srcdir', ''), name)


def up_to_date(source, target):
    return (os.path.exists(target) and
            os.path.getmtime(source) <= os.path.getmtime(target))


# We build an Extension using SWIG, which generates a Python module.
# By default, the 'build_py' step is run before 'build_ext', and
# therefore the generated Python module is not copied into the build
# directory.
# Bugs: https://bugs.python.org/issue1016626
#       https://bugs.python.org/issue2624
# Workaround:
# https://stackoverflow.com/questions/12491328/python-distutils-not-include-the-swig-generated-module
#
# To install to multiple Python installations or to alternate ones run the
# following three commands (yes, run the build one twice):
#
# /path/to/pythonX.Y setup.py build
# /path/to/pythonX.Y setup.py build
# /path/to/pythonX.Y setup.py install
#
# It is highly likely that this will need to be run as root or with sudo (or
# sudo -H).  It may or may not work with venv. and outside a virtualenv

class BuildExtFirstHack(build):
    def _read_header(self, header, cflags):
        tmp_include = self._in_build_base('include1.h')
        with open(tmp_include, 'w') as f:
            f.write('#include <%s>' % header)
        return subprocess.check_output(
            os.environ.get('CPP', 'cc -E').split() + cflags +
            [tmp_include]).decode('utf-8')

    def _write_if_unchanged(self, target, content):
        if os.path.exists(target):
            with open(target) as f:
                if f.read() == content:
                    return

        with open(target, 'w') as sink:
            sink.write(content)

    def _generate_gpgme_h(self, source_name, sink_name):
        print('Using gpgme.h from {}'.format(source_name))
        shutil.copy2(source_name, sink_name)

    def _generate_errors_i(self):

        ge_cflags=''
        gpg_error_content = self._read_header(
            'gpg-error.h', ge_cflags.split(' ') if ge_cflags else [])

        filter_re = re.compile(r'GPG_ERR_[^ ]* =')
        rewrite_re = re.compile(r' *(.*) = .*')

        errors_i_content = ''
        for line in gpg_error_content.splitlines():
            if not filter_re.search(line):
                continue
            errors_i_content += rewrite_re.sub(
                r'%constant long \1 = \1;' + '\n', line.strip())

        self._write_if_unchanged(
            self._in_build_base('errors.i'), errors_i_content)

    def _in_build_base(self, name):
        return os.path.join(self.build_base, name)

    def _generate(self):
        # Cleanup gpgme.h from deprecated functions and typedefs.
        if not os.path.exists(self.build_base):
            os.makedirs(self.build_base)

        self._generate_gpgme_h(gpgme_h, self._in_build_base('gpgme.h'))
        self._generate_errors_i()

        # Copy due to https://bugs.python.org/issue2624
        # Avoid creating in srcdir
        for source, target in ((in_srcdir(n), self._in_build_base(n))
                               for n in ('gpgme.i', 'helpers.c', 'private.h',
                                         'helpers.h')):
            if not up_to_date(source, target):
                shutil.copy2(source, target)

        # Append generated files via build_base
        if not os.path.exists(os.path.join(self.build_lib, 'gpg')):
            os.makedirs(os.path.join(self.build_lib, 'gpg'))
        shutil.copy2('version.py', os.path.join(self.build_lib, 'gpg'))

    def run(self):
        self._generate()

        swige.sources.extend((self._in_build_base('gpgme.i'),
                              self._in_build_base('helpers.c')))
        swige.swig_opts.extend([
            '-I' + self.build_base, '-outdir',
            os.path.join(self.build_lib, 'gpg')
        ])
        include_dirs.insert(0, self.build_base)

        self.run_command('build_ext')
        build.run(self)


swig_sources = []
swig_opts = ['-threads']
swige = Extension(
    'gpg._gpgme',
    sources=swig_sources,
    swig_opts=swig_opts,
    include_dirs=include_dirs,
    define_macros=define_macros,
    library_dirs=library_dirs,
    extra_link_args=libs)

setup(
    cmdclass={'build': BuildExtFirstHack},
    version='2.0.0',
    ext_modules=[swige],
    packages=[
        'gpg', 'gpg.constants', 'gpg.constants.data', 'gpg.constants.keylist',
        'gpg.constants.sig', 'gpg.constants.tofu'
    ],
)
