# encoding: utf-8

import inspect
from uiutil.tk_names import ttk


def locate_calling_stack_frame_from_base_frame(frame=None,
                                               exclude=None):
    u"""
    Locate the calling ttk.Frame or ttk.LabelFrame
    :param frame: a frame reference or none
    :param exclude: A frame to skip when scanning the stack.
                    Supply self if calling from a frame.
    :return: ttk.Frame, ttk.LabelFrame based instance.
             This can be: the provided frame
                      or: the first ttk.Frame or ttk.LabelFrame
                          found when scanning back through the
                          stack.
    """

    # TODO: return the stack frame instead/as well. Will be useful for exceptions.

    if frame:
        return frame, None

    stack = inspect.stack()
    for stack_frame in stack:
        try:
            obj = stack_frame[0].f_locals[u'self']
            if exclude:
                if obj == exclude:
                    continue
            if isinstance(obj, (ttk.Frame, ttk.LabelFrame)):
                return obj, stack_frame
            try:
                return obj._main_frame, stack_frame
            except:
                pass

        except KeyError:
            pass  # Not called from an object

    raise RuntimeError(u"Introspection failure. 'frame' parameter was not provided "
                       u"and could not find ttk.Frame or ttk.LabelFrame in stack.")


def calling_base_frame(frame=None,
                       exclude=None):
    u"""
    Locate the calling ttk.Frame or ttk.LabelFrame
    :param frame: a frame reference or none
    :param exclude: A frame to skip when scanning the stack.
                    Supply self if calling from a frame.
    :return: ttk.Frame, ttk.LabelFrame based instance.
             This can be: the provided frame
                      or: the first ttk.Frame or ttk.LabelFrame
                          found when scanning back through the
                          stack.
    """

    # TODO: return the stack frame instead/as well. Will be useful for exceptions.

    return locate_calling_stack_frame_from_base_frame(frame=frame,
                                                      exclude=exclude)[0]
