# coding: utf-8
import logging

import sys
import ast
from io import StringIO
from .printer import Printer
from .unparser36 import Unparser as Unparser36

log = logging.getLogger(__name__)

version_info = sys.version_info[:2]
if version_info == (3, 6):
    from .unparser36 import Unparser
elif version_info == (3, 7):
    from .unparser37 import Unparser
elif version_info == (3, 8):
    from .unparser38 import Unparser
else:
    from .unparser import Unparser


__version__ = "1.6.2"
__instrumented = False


def unparse(tree):
    if version_info >= (3, 9):
        instrument_ast()
        source = ast.unparse(tree)
    else:
        v = StringIO()
        Unparser(tree, file=v)
        source = v.getvalue()
    return source


def dump(tree):
    v = StringIO()
    Printer(file=v).visit(tree)
    return v.getvalue()


def delimit_if(func):
    """
    python 3.9 introduced a new native unparse method that conditionally adds parenthesis, unlike python 3.8 and down
    we need to instrument the delimit_if to always add parenthesis, otherwise, hashes will change
    https://github.com/python/cpython/commit/397b96f6d7a89f778ebc0591e32216a8183fe667#diff-abeeed217a24ce3c21e15c2e32e2f0886cea69986c2641455c1eefc983c1f977R659
    """

    def wrapper(*args, **kwargs):
        args = list(args)
        if len(args) == 3:
            kwargs["condition"] = True
        else:
            args[3] = True
        return func(*args, **kwargs)

    return wrapper


def maybe_newline(func):
    """
    python 3.9 introduced a new native unparse method that conditionally adds new lines, unlike python 3.8 and down
    we need to instrument the maybe_newline to always add a new line, otherwise, hashes will change
    https://github.com/python/cpython/commit/493bf1cc316b0b5bd90779ecd1132878c881669e
    """

    def wrapper(*args, **kwargs):
        self = args[0]
        self.write("\n")

    return wrapper


def set_precedence(func):
    """
    As part of the scan process, when visiting a function we clean all inner functions
    We had a bug in cleaning lambdas. We set body = [] which throws an exception in python 3.9 and up.
    The fix impacted hashes, so we needed to patch it to maintain hashes
    """

    def wrapper(*args, **kwargs):
        nodes = args[2:]
        if len(nodes) == 1 and nodes[0] == []:
            return
        return func(*args, **kwargs)

    return wrapper


def ast_unparse(func):
    def wrapper(*args, **kwargs):
        source = func(*args, **kwargs)
        source = "".join([source, "\n"]) if source else "\n"
        return source

    return wrapper


def instrument_ast():
    global __instrumented
    if __instrumented:
        return
    try:
        # On Python 3.9-3.13, ast._Unparser is defined directly in ast.py.
        # On Python 3.14+, the class was moved to a private _ast_unparse module
        # (CPython PR #131953) and is only lazily attached to ast on first ast.unparse() call.
        # We resolve the class via getattr with a fallback import, then re-attach it
        # to the ast module so CPython's lazy import finds our already-patched class.
        _unparser_cls = getattr(ast, "_Unparser", None)
        if _unparser_cls is None:
            from _ast_unparse import Unparser as _unparser_cls

            ast._Unparser = _unparser_cls

        _unparser_cls.delimit_if = delimit_if(_unparser_cls.delimit_if)
        _unparser_cls.maybe_newline = maybe_newline(_unparser_cls.maybe_newline)
        _unparser_cls.set_precedence = set_precedence(_unparser_cls.set_precedence)
        ast.unparse = ast_unparse(ast.unparse)
        __instrumented = True
    except Exception:
        log.warning(
            "Failed instrumenting ast. This can lead to false code modifications. Please open a support ticket with logs"
        )
