#!/usr/bin/env python
import os
import platform
import shlex
import struct
import subprocess
from collections import deque

import colored
import sys

import tabulate
from colored.colored import stylize
from dnutils.tools import ifnot, ifnone
from threading import RLock
import re


class ASCII:
    '''
    A collection of ACSII escape sequences to be used with ASCII tty devices such as the console.
    '''

    _PREFIX = chr(27) + '['
    CLS = _PREFIX + '2J'
    HFILL = _PREFIX + 'K'
    HFILLR = _PREFIX + 'K\n'
    UP = _PREFIX + '%dA'
    DOWN = _PREFIX + '%dB'
    LEFT = _PREFIX + '%dC'
    RIGHT = _PREFIX + '%dD'
    SAVE = _PREFIX + 's'
    RESTORE = _PREFIX + 'u'
    MOVE_CURSOR = _PREFIX + '{row};{col}H'

    @staticmethod
    def _apply(code):
        print(code, end='')

    @staticmethod
    def cls():
        '''
        Clear the console screen and move the cursor to the upper left corner.
        :return:
        '''
        ASCII.bottom()
        ASCII._apply(ASCII.CLS)
        ASCII.mv()

    @staticmethod
    def mv(row=0, col=0):
        '''
        Move the cursor to the specified ``row`` and ``col``umn.

        :param row:
        :param col:
        :return:
        '''
        ASCII._apply(ASCII.MOVE_CURSOR.format(row=row, col=col))

    @staticmethod
    def save():
        ASCII._apply(ASCII.SAVE)

    @staticmethod
    def restore():
        ASCII._apply(ASCII.RESTORE)

    @staticmethod
    def up(n=1):
        '''
        Move the cursor ``n`` lines up.

        :param n:
        :return:
        '''
        ASCII._apply(ASCII.UP % n)

    @staticmethod
    def down(n=1):
        '''
        Move the cursor ``n`` lines down.
        :param n:
        :return:
        '''
        ASCII._apply(ASCII.DOWN % n)

    @staticmethod
    def left(n=1):
        '''
        Move the cursor ``n`` characters to the left.
        :param n:
        :return:
        '''
        ASCII._apply(ASCII.LEFT % n)

    @staticmethod
    def right(n=1):
        '''
        Move the cursor ``n`` characters to the right.
        :param n:
        :return:
        '''
        ASCII._apply(ASCII.RIGHT % n)

    @staticmethod
    def hfill():
        ASCII._apply(ASCII.HFILL)

    @staticmethod
    def bottom():
        c, r = os.get_terminal_size()
        ASCII.mv(r, c)


def bf(s):
    '''Return a copy of the string ``s`` in boldface'''
    return colored.stylize(s, colored.attr('bold'))


def style(txt, color, bold=False):
    '''
    Return a copy of the string ``txt`` in ``color`` and ``bold`` (True/False)
    :param txt:
    :param color:
    :param bold:
    :return:
    '''
    return colored.stylize(txt, colored.fg(color) + (colored.attr('bold') if bold else ''))


def ljust(t, l, f):
    s = cleanstr(t)
    n = l - len(s)
    if n <= 0: return t
    return t + f * n


# ------------------------------------------------------------------------------
# parts of this file are taken from https://gist.github.com/jtriley/1108174
# and adapted to Python 3
# ------------------------------------------------------------------------------

def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console.rst
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console.rst-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)  # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass


def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])


def tty(stream):
    isatty = getattr(stream, 'isatty', None)
    return isatty and isatty()


def barstr(width, percent, color=None, inf=False):
    '''
    Returns the string representation of an ASCII 'progress bar'.

    :param width:       the maximum space of the bar in number of of characters
    :param percent:     the percentage of ``width`` that the bar will consume.
    :param color:       string specifying the color of the bar
    :param inf:         boolean determining whether the bar is supposed to be "infinite".
    :return:            the string representation of the progress bar.
    '''
    width = width - 13  # constant number of characters for the numbers
    if not inf:
        barw = int(round(width * percent))
        bar = ''.ljust(barw, '=')
        bar = bar.ljust(width, ' ')
    else:
        bar = infbarstr(width, int(percent))
    if color is not None:
        filler = '\u25A0'
        bar = bar.replace('=', filler)
        bar = stylize('[', colored.attr('bold')) + stylize(bar, colored.fg(color)) + stylize(']', colored.attr('bold'))
    else:
        bar = '[%s]' % bar
    if inf:
        return bar
    return '{0} {1: >7.3f} %'.format(bar, percent * 100.)


def infbarstr(width, pos):
    '''
    Returns the string representation of an ASCII 'progress bar'.
    :param width:
    :param pos:
    :return:
    '''
    bw = int(round(width * .2))
    bar = ' ' * pos
    bar += '=' * bw
    bar = bar[0:width]
    front = int(max(0, (pos + bw) - width))
    bar = ('=' * front) + bar[front:]
    bar = bar.ljust(width, ' ')
    return bar


class ProgressBar:
    '''
    An ASCII progress bar to show progress in the console.rst.
    '''

    def __init__(self, layout='100%:0%', value=0, steps=None, label='', color=None, stream=sys.stdout, inf=False):
        self.layout = layout
        self.setlayout(layout)
        self.steps = steps
        self.inf = inf
        self.lock = RLock()
        if inf:
            self.steps = self.barwidth - 13
            self.step = self.value = 0
        elif steps is not None:
            self.step = value
            self.value = float(value) / steps
        else:
            self.value = value
            self.step = None
            self.steps = None
        self.color = color
        self._label = label
        if tty(sys.stdout):
            self.update(self.value)

    def setlayout(self, layout):
        '''Specifies the layout of the progress bar.

        ``layout`` must be a string of the form "X:Y" or "X", where
        `X` determines the width of the bar part of the progress bar and
        `Y` determines the width of the label part of the progress bar.
        Values can be absolute (in console.rst characters) or relative (in percentage values)
        to the console.rst width.

        :example:

            >>> bar = ProgressBar(value=.2, color='green', label='in progress...please wait...')
            [■■■■■■■■■■■■■■■■■■■                                                                           ]  20.000 %
            >>> bar.setlayout('70%:30%')
            >>> print(bar)
            [■■■■■■■■■■■■                                                  ]  20.000 % in progress...please wait...
            >>> bar.setlayout('100%:0%')
            >>> print(bar)
            [■■■■■■■■■■■■■■■■■■■                                                                           ]  20.000 %
            >>> bar.setlayout('60:40')
            >>> print(bar)
            [■■■■■■■■■                                      ]  20.000 % in progress...please wait...

        '''
        if ':' in layout:
            barw, lblw = layout.split(':')
        else:
            barw, lblw = layout, ''
        if '%' in barw:
            barw = float(barw.strip('% ')) / 100.
        elif barw:
            barw = int(barw)
        else:
            barw = -1
        if '%' in lblw:
            lblw = float(lblw.strip('% ')) / 100.
        elif lblw:
            lblw = int(lblw)
        else:
            lblw = -1
        if barw == -1 and lblw == -1:
            raise AttributeError('Illegal layout specification: "%s"' % layout)
        termw, _ = get_terminal_size()
        if barw != -1:
            self.barwidth = barw if type(barw) is int else int(round((termw * barw)))
        if lblw != -1:
            self.lblwidth = lblw if type(lblw) is int else int(round((termw * lblw)))
        else:
            self.lblwidth = termw - self.barwidth
        if barw == -1:
            self.barwidth = termw - self.lblwidth

    def label(self, label):
        '''Set the current label of the bar.'''
        self._label = label
        self.setlayout(self.layout)
        self.update(self.value)

    def update(self, value, label=None):
        '''Set the current value of the bar to ``value`` and update the label by ``label``.'''
        self.setlayout(self.layout)
        self.value = value
        if label is not None: self._label = label
        if value == 1: self._label = ''
        if tty(sys.stdout):
            sys.stdout.write(str(self))
            sys.stdout.flush()

    def finish(self, erase=True, msg='', end='\n'):
        '''Terminates the progress bar.

        :param erase:    If ``True``, the progress bar will be removed (overwritten) from the console.rst.
        :param msg:      Optional "goodbye"-message to be printed.
        :param end:      Final character to be printed (default is '\\n' to move to a new line)
        '''
        if erase: sys.stdout.write('\r' + msg.ljust(self.lblwidth + self.barwidth, ' '))
        sys.stdout.write(end)

    def inc(self, steps=1):
        '''Increment the current value of the progress bar by ``steps`` steps.'''
        self.setlayout(self.layout)
        with self.lock:
            if self.steps is None:
                raise Exception('Cannot call inc() on a real-valued progress bar.')
            self.step += steps
            if not self.inf:
                value = float(self.step) / self.steps
                self.update(value)
            else:
                self.update(self.step)
                self.step %= (self.barwidth - 13)

    def __str__(self):
        return '\r' + barstr(self.barwidth, self.value, color=self.color, inf=self.inf) + ' ' + self._label[
                                                                                                :self.lblwidth].ljust(
            self.lblwidth, ' ')


ansi_escape = re.compile(r'\x1b[^m]*m')


def cleanstr(s):
    return ansi_escape.sub('', s)


class StatusMsg(object):
    '''Print a Linux-style status message to the console.rst.'''
    ERROR = colored.stylize('ERROR', (colored.fg('red'), colored.attr('bold')))
    FAILED = colored.stylize('FAILED', (colored.fg('red'), colored.attr('bold')))
    OK = colored.stylize('OK', (colored.fg('green'), colored.attr('bold')))
    WARNING = colored.stylize('WARNING', (colored.fg('yellow'), colored.attr('bold')))
    PASSED = colored.stylize('PASSED', (colored.fg('green'), colored.attr('bold')))

    def __init__(self, message='', status=None, width='100%', stati=None):
        if stati is None:
            self.stati = {StatusMsg.ERROR, StatusMsg.OK, StatusMsg.WARNING, StatusMsg.FAILED, StatusMsg.PASSED}
        else:
            self.stati = stati
        self.widthstr = width
        self.setwidth(self.widthstr)
        self.msg = message
        self.status = status
        self.write()

    def setwidth(self, width):
        '''
        Sets the with in relative or absolute numbers of console.rst characters.
        :param width:
        :return:
        '''
        if '%' in width:
            consolewidth, _ = get_terminal_size()
            self.width = int(round(consolewidth * float(width.strip('%')) * .01))
        else:
            self.width = int(width)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, s):
        if s not in self.stati and s is not None:
            raise ValueError('Status "%s" cannot be set.' % str(s))
        self._status = s
        self.write()

    def message(self, msg):
        self.msg = msg
        self.write()

    def write(self):
        self.setwidth(self.widthstr)
        statuswidth = max(map(len, [cleanstr(s) for s in self.stati]))
        lblwidth = self.width - statuswidth - 4
        msg = self.msg
        if lblwidth < len(cleanstr(self.msg)):
            msg = self.msg[:lblwidth - 4] + '...'
        sts = ifnone(self._status, '')
        s = ljust(msg, lblwidth - 1, ' ') + ' [ %s ]' % sts.center(statuswidth + (len(sts) - len(cleanstr(sts))), ' ')
        sys.stdout.write('\r' + s)

    def finish(self, erase=False, end='\n'):
        if erase: sys.stdout.write('\r' + ' ' * self.width)
        sys.stdout.write(end)


def treetable(data_generator, headers=None, tablefmt=None):
    '''
    Computes a string representation of the ``data`` in the style of a tree/table combination.

    Data is passed in the form of a generator object that yields ``(level, row)`` pairs, where each
    ``level`` is an integer specifying the level on which the data row ``row`` resides in the tree.
    ``row`` is then a ``list`` or ``tuple`` holding the single table entries.

    :param tablefmt:
    :param headers:
    :param data_generator:
    '''
    preserve_whitespace = tabulate.PRESERVE_WHITESPACE
    tabulate.PRESERVE_WHITESPACE = True
    data = deque()
    lastlevel = 0
    for level, item in data_generator:
        if level - 1 > lastlevel:
            raise ValueError('illegal level: can only increment level by one.')
        lastlevel = level
        data.append([((' ' * (2 * level)) + '+ %s' % item[0])] + list(item[1:]))
    s = tabulate.tabulate(list(data), headers=headers, tablefmt=tablefmt)
    tabulate.PRESERVE_WHITESPACE = preserve_whitespace
    return s


def bars(values, texts=None, mode='norm', width=None, color=None):
    '''
    Prints horizontal bars in vertical order of the values ``values``, which is any iterable object holding numeric values.
    All values must be non-negative.

    :param values: array-like object storing numeric values
    :param texts:  optional texts that appear on the right side of the bars.
    :param mode:   how the bars shall be computed. 'norm', 'max'
    :param width:  the width of the bars (in console characters), default: console width
    :param color:
    :return:
    '''
    if not all(v >= 0 for v in values):
        raise ValueError('All values must be non-negative.')
    texts = ifnone(texts, [''] * len(values))
    z = 0
    if mode == 'norm':
        z = sum(values)
    if mode == 'max':
        z = max(values)
    w = ifnone(width, os.get_terminal_size()[1])
    for idx, ((v, r), t) in enumerate(zip([(v, v / z) if z > 0 else (0, 0) for v in values], texts)):
        print('%.2d: %s (%s) %s' % (idx, barstr(w, r, color=color), v, t))


def askyesno(question, default=True, allownone=False):
    '''
    Ask the user a Yes/No question.

    :param allownone:   Allow 'c' for cancel. Will return ``None`` in this case.
    :param question:    The question to be asked.
    :param default:     The default value. Can be either ``True``, ``False``, or ``None``.
    :return:
    '''
    choices = {0: 'n', 1: 'y'}
    if allownone:
        choices[None] = 'c'
    # idx = choices.index(default)
    choices[default] = choices[default].upper()
    while 1:
        i = input('%s [%s] ' % (question, '/'.join(choices.values()))).strip().lower()
        if not i:
            i = default
        elif i in ''.join(choices.values()).lower():
            i = {'n': False, 'y': True, 'c': None}[i]
        else:
            continue
        return i


def user_select(question, options, default=0):
    '''Display number of options to the user an ask him to select one by typing a number.
    The ``question`` is a string prepended to the list of possible ``options``.
    ``default`` is the (one-based) index of the selection that is selected by default.

    If the "c" character is entered, ``None`` is returned indicating that no selection was made.

    :param question:    question to be displayed to the user
    :param options:     list of entities the user is supposed to pick one, their string representations will be displayed.
    :param default:     the (one-based) index of the default selection. Entering nothing but just hitting "return" will return this selection.
    :return:
    '''
    default += 1
    txt = question + '\n'
    indent = '1' if len(options) < 10 else ('2' if len(options) < 100 else 3)
    idxpattern = '[%%.%sd] ' % indent
    pattern = '  %s%%s\n' % idxpattern
    for i, opt in enumerate(options):
        txt += pattern % (i + 1, opt)
    print(txt)
    while 1:
        sel = input('Your selection (c for cancel, default is [%s]): ' % (default))
        if sel == 'c':
            return None
        try:
            if sel:
                sel = int(sel)
                if not 1 <= sel <= len(options):
                    continue
            else:
                sel = default
        except ValueError:
            continue
        else:
            return sel - 1