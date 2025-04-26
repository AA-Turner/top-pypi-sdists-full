# -*- coding: utf-8 -*-
import os
import sys
import types

import six
from functools import partial

from .exts.cloud_debug_python.module_explorer import GetCodeObjectAtLine, _GetModuleCodeObjects, _GetLineNumbers

from rook.logger import logger
from rook.config import LoggingConfiguration
from rook.singleton import singleton_obj
from rook.processor.error import Error

from ..exceptions import RookBdbCodeNotFound, RookBdbSetBreakpointFailed, RookInvalidPositionException, \
    RookSettingBreakpointError

try:
    from . import cdbg_native
    cdbg_native.InitializeModule(None)
except ImportError:
    # Special handling for Google AppEngine (Python 2.7)
    from google.devtools.cdbg.debuglets.python import cdbg_native


class BPStatus(object):
    __slots__ = ["disabled"]

    def __init__(self):
        self.disabled = False

class Bdb(object):
    def __init__(self):
        self.fncache = {}
        self._cookies = {}
        self._cookies_to_func = {}
        self._func_to_original_co_code = {}
        self._bp_status = {}
        self.user_line = None


    def set_trace(self):
        # Not needed
        pass

    def canonic(self, filename):
        if filename[0] == "<" and filename[-1] == ">":
            return filename
        canonic = self.fncache.get(filename)
        if not canonic:
            canonic = os.path.abspath(filename)
            canonic = os.path.normpath(canonic)
            self.fncache[filename] = canonic
        return canonic

    def ignore_current_thread(self):
        # Not needed
        pass

    def set_break(self, item, filename, lineno, aug_id):
        filename = self.canonic(filename)

        if isinstance(item, types.ModuleType):
            self._set_break_module(item, filename, lineno, aug_id)
        elif isinstance(item, types.CodeType):
            # the caller doesn't know if the code object has this line, so verify here
            self._set_break_code_object(item, filename, lineno, aug_id)
        else:
            raise KeyError(type(item))

    def _set_break_module(self, module, filename, lineno, aug_id):
        status, code_object = GetCodeObjectAtLine(module, lineno)
        if not status:
            if hasattr(module, '__file__'):
                logger.debug("CodeNotFound module filename %s", module.__file__)

            for code_object_node in _GetModuleCodeObjects(module):
                inner_cobj = code_object_node.obj
                logger.debug("Name: %s", inner_cobj.co_name)
                for cline in _GetLineNumbers(inner_cobj):
                    logger.debug("Name: %s, Line %d", inner_cobj.co_name, cline)

            if code_object == (None, None):
                raise RookBdbCodeNotFound(filename=filename)
            else:
                raise RookInvalidPositionException(filename=filename, line=lineno, alternatives=code_object)

        self._set_break_code_object(code_object, filename, lineno, aug_id)

    def _set_code_object(self, code_object_node, code_object):
        if isinstance(code_object_node.parent, tuple):
            co_consts = list(code_object_node.parent)
            index = co_consts.index(code_object_node.obj)
            co_consts[index] = code_object
            # In this case, the parent of obj is the tuple itself, and the grandparent
            # is the one holding the tuple in co_consts
            cdbg_native.UpdateCoConsts(code_object_node.grandparent, tuple(co_consts))
        else:
            logger.debug("Trying to change __code__ of object of type %s", str(type(code_object_node.parent)))
            code_object_node.parent.__code__ = code_object

    def _set_break_code_object(self, code_object_node, filename, lineno, aug_id):
        try:
            code_object = self._func_to_original_co_code[code_object_node.get_id()]
        except KeyError:
            code_object = code_object_node.obj

        # Install the breakpoint
        bp_status = BPStatus()
        callback_partial = self._get_callback_partial(callback, lineno, code_object, bp_status, filename, aug_id)
        error_callback_partial = self._get_callback_partial(error_callback, lineno, code_object, bp_status, filename, aug_id)

        if LoggingConfiguration.DEV_DEBUG:
            import dis
            import io

            with io.StringIO() as f:
                dis.dis(code_object, file=f)
                dis_output = f.getvalue()
                logger.debug("code_object before patch aug_id: %s, filename: %s, lineno: %d, dis: %s:", aug_id, filename, lineno, dis_output)
        if sys.version_info >= (3, 11, 0):
            cookie, new_co_code = cdbg_native.SetConditionalBreakpoint(code_object, lineno, None, callback_partial,
                                                                       error_callback_partial)
            new_code_object = code_object.replace(co_code=new_co_code)
            self._set_code_object(code_object_node, new_code_object)
        else:
            cookie = cdbg_native.SetConditionalBreakpoint(code_object, lineno, None, callback_partial,
                                                          error_callback_partial)

        if LoggingConfiguration.DEV_DEBUG:
            with io.StringIO() as f:
                if sys.version_info >= (3, 11, 0):
                    dis.dis(new_code_object, file=f)
                else:
                    dis.dis(code_object, file=f)
                dis_output = f.getvalue()
                logger.debug("code_object after patch aug_id: %s, filename: %s, lineno: %d, dis: %s:",aug_id, filename, lineno, dis_output)

        if cookie < 0:
            raise RookBdbSetBreakpointFailed("%s on line %d" % (code_object.co_name, lineno))

        self._cookies[aug_id] = cookie
        self._cookies_to_func[cookie] = code_object_node
        if code_object_node.get_id() not in self._func_to_original_co_code:
            self._func_to_original_co_code[code_object_node.get_id()] = code_object
        self._bp_status[aug_id] = bp_status

    def _get_callback_partial(self, callback, lineno, code_object, bp_status, filename, aug_id):
        return partial(callback, lineno=lineno,
                user_line=self.user_line,
                callback_object_id=id(
                    code_object),
                bp_status=bp_status,
                filename=filename,
                pid=os.getpid(),
                aug_id=aug_id)

    def clear_break(self, aug_id):
        try:
            cookie = self._cookies[aug_id]
            code_object_node = self._cookies_to_func[cookie]
            status = self._bp_status[aug_id]
        except KeyError:
            return

        try:
            code_object = self._func_to_original_co_code[code_object_node.get_id()]
        except KeyError:
            code_object = code_object_node.obj

        new_co_code = cdbg_native.ClearConditionalBreakpoint(cookie)

        if sys.version_info >= (3, 11, 0):
            new_code_object = code_object.replace(co_code=new_co_code)
            self._set_code_object(code_object_node, new_code_object)

        status.disabled = True

        del self._cookies[aug_id]
        del self._cookies_to_func[cookie]
        del self._bp_status[aug_id]

    def clear_all_breaks(self):
        for cookie in six.itervalues(self._cookies):
            cdbg_native.ClearConditionalBreakpoint(cookie)

        for status in six.itervalues(self._bp_status):
            status.disabled = True

        self._cookies = {}
        self._bp_status = {}

    def close(self):
        pass


def error_callback(lineno, user_line, callback_object_id, bp_status, filename, pid, aug_id):
    message = "Line: {lineno}, not found in file: {filename}, please contact support.".format(
        lineno=lineno, filename=filename)
    send_error_for_aug(aug_id, message)


def send_error_for_aug(aug_id, message):
    logger.error(message)
    if hasattr(singleton_obj, '_output'):
        exception = RookSettingBreakpointError(message)
        error = Error(exc=exception, message=message)
        singleton_obj._output.send_rule_status(aug_id, 'Error', error)


# This function has been moved outside of the class so that it can be pickled
# safely by cloudpickle (which will pickle any objects referred to by its closure)
# When changing it, take care to avoid using references to anything not imported within the function
def callback(lineno, user_line, callback_object_id, bp_status, filename, pid, aug_id):
    try:
        if bp_status.disabled is True:
            return

        import inspect
        frame = inspect.currentframe().f_back

        callback_was_pickled = False#callback_object_id != id(frame.f_code) or pid != os.getpid()

        if not callback_was_pickled and frame and user_line:
            user_line(frame, filename, lineno=lineno, aug_id=aug_id)
    except:  # this is very last line of defense in the hook, can't report from here lgtm[py/catch-base-exception]
        pass
