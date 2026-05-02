import logging

import os

from termcolor import colored
import inspect

tty_size = os.popen('stty size', 'r').read().split()
tty_rows, tty_columns = (int(tty_size[0]), int(tty_size[1]))


class Colors:
    grey = 'grey'
    red = 'red'
    green = 'green'
    yellow = 'yellow'
    blue = 'blue'
    magenta = 'magenta'
    cyan = 'cyan'
    white = 'white'

    all_colors = [grey, red, green, yellow, blue, magenta, cyan, white]


def log(msg: str, char_to_surround_with: str = None, logger=logging.info, right_justify=False, left_justify=False,
        center_message=False, color=None, print_func_name=False) -> ():
    """
    :param msg: the message to log
    :param char_to_surround_with: the character(s) to surround the log message with
    :param logger: the logger you want to use, defaults to logging.info
    :param right_justify: whether to right justify the log message
    :param left_justify: whether to left justify the log message
    :param center_message: whether to center the log message
    :param color: 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan' or 'white'
    :param print_func_name True if you want to print the name of the function from within which log was called
    :return:
    """

    if not char_to_surround_with:
        char_to_surround_with = '#'

    surround_with_string = char_to_surround_with.center(tty_rows, char_to_surround_with)

    message_line = msg

    if center_message:
        message_line = msg.center(tty_rows, ' ')
    elif left_justify:
        message_line = msg.ljust(tty_rows, ' ')
    elif right_justify:
        message_line = msg.rjust(tty_rows, ' ')

    pre_text = None

    if print_func_name:
        pre_text = f'log called from {inspect.stack()[1][3]}'.center(tty_rows,
                                                                     ' ')

    if color:
        if color not in Colors.all_colors:
            raise ValueError(f"Color must be one of {', '.join(Colors.all_colors)} ")
        message_line = colored(message_line, color)

    if pre_text:

        logger(f'\n{pre_text}\n{surround_with_string}\n {message_line} \n{surround_with_string}')
    else:
        logger(f'\n{surround_with_string}\n {message_line} \n{surround_with_string}')
