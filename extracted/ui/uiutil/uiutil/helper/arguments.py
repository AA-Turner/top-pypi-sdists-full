# encoding: utf-8

import attr
from .introspection import calling_base_frame
from ..tk_names import HORIZONTAL, VERTICAL

ROW = u'row'
COLUMN = u'column'
ROW_SPAN = u'rowspan'
COLUMN_SPAN = u'columnspan'
STICKY = u'sticky'
PAD_X = u'padx'
PAD_Y = u'pady'

GRID_KWARGS = (ROW,
               COLUMN,
               ROW_SPAN,
               COLUMN_SPAN,
               STICKY,
               PAD_X,
               PAD_Y)

START = u'start'
CURRENT = u'current'
NEXT = u'next'
LAST = u'last'
MAX = u'max'


@attr.s(frozen=True)
class _Position(object):
    FIRST = attr.ib(default=START)
    START = attr.ib(default=START)
    CURRENT = attr.ib(default=CURRENT)
    NEXT = attr.ib(default=NEXT)
    LAST = attr.ib(default=LAST)
    MAX = attr.ib(default=MAX)


Position = _Position()


def pop_mandatory_kwarg(kwargs,
                        key):
    try:
        return kwargs.pop(key)
    except KeyError:
        raise ValueError(u'Missing mandatory parameter "{key}"'.format(key=key))


def pop_kwarg(kwargs,
              key,
              default=None):
    try:
        return kwargs.pop(key)
    except KeyError:
        return default


def raise_on_positional_args(caller, args):
    if args:
        raise ValueError(u'positional arguments are not accepted by {c}'.format(c=caller.__class__))


def kwargs_only(f):
    def new_f(**kwargs):
        return f(**kwargs)
    return new_f


def get_grid_kwargs(frame=None,
                    **kwargs):

    grid_kwargs = {key: value
                   for key, value in iter(kwargs.items())
                   if key in GRID_KWARGS}
    grid_kwargs_passed = {key: value
                          for key, value in iter(grid_kwargs.items())}
    if not frame:
        frame = calling_base_frame()

    try:
        incrementers = {ROW: frame.row,
                        COLUMN: frame.column,
                        ROW_SPAN: frame.row,
                        COLUMN_SPAN: frame.column}
    except AttributeError:
        return grid_kwargs

    defaults = {ROW: frame.row.current,
                COLUMN: frame.column.current}

    # Support automatic spanning
    for field, vector, auto_pos in ((COLUMN_SPAN, COLUMN, HORIZONTAL),
                                    (ROW_SPAN, ROW, VERTICAL)):
        incrementer = incrementers[field]
        auto_pos_adjust = {False: 1,
                           True:  0}[frame.AUTO_POSITION == auto_pos]
        if grid_kwargs.get(field) == Position.MAX:
            try:
                start = int(grid_kwargs[vector])
            except (KeyError, ValueError):
                grid_kwargs[vector] = 0
                grid_kwargs[field] = incrementer.max + auto_pos_adjust
            else:
                grid_kwargs[field] = incrementer.max - start + auto_pos_adjust

    # Auto position to start of next row or column
    if frame.AUTO_POSITION is HORIZONTAL:
        if grid_kwargs.get(ROW) is Position.NEXT and grid_kwargs_passed.get(COLUMN) is None:
            grid_kwargs[COLUMN] = Position.START
    elif frame.AUTO_POSITION is VERTICAL:
        if grid_kwargs.get(COLUMN) is Position.NEXT and grid_kwargs_passed.get(ROW) is None:
            grid_kwargs[ROW] = Position.START

    # Don't need to set row or column in the original call
    # if it's just the current value
    for vector in (ROW, COLUMN):
        grid_kwargs[vector] = grid_kwargs.get(vector, defaults[vector])
        incrementer = incrementers[vector]

        if grid_kwargs[vector] == Position.START:
            grid_kwargs[vector] = incrementer.start()

        elif grid_kwargs[vector] == Position.NEXT:
            grid_kwargs[vector] = incrementer.next()

        elif grid_kwargs[vector] == Position.CURRENT:
            # Don't need to set CURRENT, as it's used by default,
            # but added for those why prefer to use it in their
            # calls.
            grid_kwargs[vector] = incrementer.current

        elif grid_kwargs[vector] == Position.FIRST:
            grid_kwargs[vector] = incrementer.first()

        elif grid_kwargs[vector] == Position.LAST:
            grid_kwargs[vector] = incrementer.last()

        elif grid_kwargs[vector] is not None:
            # Absolute position
            incrementer.set(grid_kwargs[vector])

    return grid_kwargs


def get_non_grid_kwargs(**kwargs):
    return {k: v for k, v in iter(kwargs.items()) if k not in GRID_KWARGS}


def grid_and_non_grid_kwargs(frame=None,
                             **kwargs):
    return (get_grid_kwargs(frame=frame,
                            **kwargs),
            get_non_grid_kwargs(**kwargs))


def get_widget_kwargs(**kwargs):
        return {key: value
                for key, value in iter(kwargs.items())
                if key not in GRID_KWARGS}
