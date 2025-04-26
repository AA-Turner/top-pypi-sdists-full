# -*- coding: utf-8 -*-
#
# This file is part of python-ghostscript.
# Copyright 2010-2021 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2010-2021 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU General Public License version 3 (GPL v3)"

import io
import sys, os
import locale # required to encode file paths
import binascii

import py

import ghostscript._gsprint as gs

postscript_img = b"""
    /Helvetica findfont 12 scalefont setfont
    0 0 moveto
    (Hello World) show
    showpage
    """

HELLO_WORLD = ''.join(('%x' % ord(c) for c in 'Hello World'))
#HELLO_WORLD = binascii.hexlify('Hello World')
postscript_doc = ('<%s> = flush' % HELLO_WORLD).encode('ascii')

STDARGS = [b'test.py', b'-dNOPAUSE', b'-dBATCH', b'-dSAFER', b'-q',
           b'-sDEVICE=bmp16', b'-g80x12']

TEST_PIC_FILENAME = os.path.join(os.path.dirname(__file__), 'hello_world.bmp')
TEST_PIC_DATA = py.path.local(TEST_PIC_FILENAME).read('rb')


def _encode(*args):
    encoding = locale.getpreferredencoding()
    return [a.encode(encoding) for a in args]


def test_revision():
    rev = gs.revision()
    assert type(rev.copyright) is bytes
    assert type(rev.product) is bytes
    assert type(rev.revision) is int
    assert type(rev.revisiondate) is int


def test_run_string(tmpdir):
    """Let ghostscript read from a file and write to stdout"""
    outfile = tmpdir.join('out.bmp')

    args = STDARGS + _encode('-sOutputFile=%s' % outfile)

    instance = gs.new_instance()

    try:
        gs.init_with_args(instance, args)
        gs.run_string(instance, postscript_img)
    finally:
        gs.exit(instance)
        gs.delete_instance(instance)

    data = outfile.read('rb')
    assert data == TEST_PIC_DATA


def test_simple(tmpdir):
    """Let ghostscript read from a file and write to a file"""
    infile = tmpdir.join('in.ps')
    infile.write(postscript_img)
    outfile = tmpdir.join('out.bmp')

    args = STDARGS + _encode('-sOutputFile=%s' % outfile, str(infile))

    instance = gs.new_instance()
    try:
        gs.init_with_args(instance, args)
    finally:
        gs.exit(instance)
        gs.delete_instance(instance)

    data = outfile.read('rb')
    assert data == TEST_PIC_DATA


def _gs_stdio(args, stdin=None, stdout=None, stderr=None):
    instance = gs.new_instance()

    # wrappers like in
    # http://ghostscript.com/doc/8.54/API.htm#Example_usage
    if stdin  is not None: stdin  = gs._wrap_stdin(stdin)
    if stdout is not None: stdout = gs._wrap_stdout(stdout)
    if stderr is not None: stderr = gs._wrap_stderr(stderr)

    gs.set_stdio(instance, stdin, stdout, stderr)
    try:
        gs.init_with_args(instance, args)
    finally:
        gs.exit(instance)
        gs.delete_instance(instance)


def test_stdin(tmpdir):
    """Let ghostscript read from stdin and write to a file"""
    outfile = tmpdir.join('out.bmp')

    args = STDARGS + _encode('-sOutputFile=%s' % outfile, '-')

    _gs_stdio(args, stdin=io.BytesIO(postscript_img))

    data = outfile.read('rb')
    assert data == TEST_PIC_DATA


def test_stdout(tmpdir):
    """Let ghostscript read from a file and write to stdout"""
    infile = tmpdir.join('in.ps')
    infile.write(postscript_doc)

    args = STDARGS + _encode(str(infile))

    stdout = io.BytesIO() # buffer for collecting the output

    _gs_stdio(args, stdout=stdout)

    data = stdout.getvalue()
    assert data == b'Hello World\n'


def test_stdin_stdout(tmpdir):
    """Let ghostscript read from stdin and write to stdout"""
    args = STDARGS + _encode('-')

    stdout = io.BytesIO() # buffer for collecting the output

    _gs_stdio(args, stdin=io.BytesIO(postscript_doc), stdout=stdout)

    data = stdout.getvalue()
    assert data == b'Hello World\n'


def test_stderr(tmpdir):
    """
    Make ghostscript write some error message to stderr and
    keep stdout on the console.
    """
    args = STDARGS + _encode('-')

    stderr = io.BytesIO() # buffer for collecting stderr

    try:
        # this call is expected to fail due to the intended error in
        # the postscript code
        _gs_stdio(args, stdin=io.BytesIO(b'foobar'), stderr=stderr)
    except gs.GhostscriptError:
        pass

    data = stderr.getvalue()
    assert b'Unrecoverable error' in data


def test_stdout_stderr(tmpdir):
    """
    Make ghostscript write some error message to stderr and
    catch stdout, too.
    """
    args = STDARGS + _encode('-')

    stdout = io.BytesIO() # buffer for collecting the output
    stderr = io.BytesIO() # buffer for collecting stderr

    try:
        # this call is expected to fail due to the intended error in
        # the postscript code
        _gs_stdio(args,
                  stdin=io.BytesIO(b'foobar'), stdout=stdout, stderr=stderr)
    except gs.GhostscriptError:
        pass

    data = stdout.getvalue()
    assert b'Error: /undefined in foobar' in data

    data = stderr.getvalue()
    assert b'Unrecoverable error' in data



def generate_test_picture():
    """
    Use command line ghostscript to generate the image used in testing
    """
    import subprocess
    outfile = TEST_PIC_FILENAME

    args = ['gs'] + STDARGS[1:] + _encode('-sOutputFile=%s' % outfile, '-')
    subprocess.Popen(args).communicate(postscript_doc)    

if __name__ ==  '__main__':
    generate_test_picture()
