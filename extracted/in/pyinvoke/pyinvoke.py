# The MIT License (MIT)
#
# Copyright (c) 2018 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from __future__ import print_function

__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = '1.0.4'

import argparse
import sys


def main(argv=None, prog=None):
  if argv is None:
    argv = sys.argv[1:]
  if prog is None:
    prog = 'pyinvoke'

  if not argv:
    print('usage: {} --version | <module:function> [args...]'.format(prog))
    return sys.exit(0)

  if argv[0] == '--version':
    print('pyinvoke', __version__)
    sys.exit(0)

  module, function = argv[0].partition(':')[::2]
  if not module or not function:
    print('fatal: invalid spec {!r}'.format(argv[0]))
    sys.exit(1)

  sys.__argv__ = sys.argv[:]
  sys.argv = argv
  sys.exit(getattr(__import__(module, fromlist=[None]), function)())


if __name__ == '__main__':
  sys.exit(main())
