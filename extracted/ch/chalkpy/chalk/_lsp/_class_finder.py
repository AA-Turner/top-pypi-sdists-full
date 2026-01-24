from __future__ import annotations

import ast
import importlib.machinery
import inspect
import linecache
import os
import sys
import types
from dataclasses import dataclass
from typing import Any, Callable, Optional, Type


class _ChalkClassFoundException(Exception):
    def __init__(self, node: ast.ClassDef):
        super().__init__()
        self.node = node


class _ChalkFunctionFoundException(Exception):
    def __init__(self, node: ast.FunctionDef | ast.AsyncFunctionDef):
        super().__init__()
        self.node = node


class _ChalkClassFinder(ast.NodeVisitor):
    def __init__(self, qualname: str):
        super().__init__()
        self.stack = []
        self.qualname = qualname

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.stack.append(node.name)
        self.stack.append("<locals>")
        self.generic_visit(node)
        self.stack.pop()
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.stack.append(node.name)
        self.stack.append("<locals>")
        self.generic_visit(node)
        self.stack.pop()
        self.stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.stack.append(node.name)
        if self.qualname == ".".join(self.stack):
            # Return the decorator for the class if present
            if node.decorator_list:
                line_number = node.decorator_list[0].lineno
            else:
                line_number = node.lineno

            # decrement by one since lines starts with indexing by zero
            line_number -= 1
            raise _ChalkClassFoundException(node=node)
        self.generic_visit(node)
        self.stack.pop()


class _ChalkFunctionFinder(ast.NodeVisitor):
    def __init__(self, name: str):
        super().__init__()
        self.stack = []
        self.name = name

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.stack.append(node.name)
        if self.name == ".".join(self.stack):
            raise _ChalkFunctionFoundException(node=node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.stack.append(node.name)
        if self.name == ".".join(self.stack):
            raise _ChalkFunctionFoundException(node=node)
        self.generic_visit(node)
        self.stack.pop()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()


def get_class_ast(cls: Type) -> ast.ClassDef:
    if not inspect.isclass(cls):
        raise ValueError(f"Expected class, but found {cls}")

    file = get_source_filename(cls)
    if file:
        # Invalidate cache if needed.
        linecache.checkcache(file)
    else:
        file = inspect.getfile(cls)
        # Allow filenames in form of "<something>" to pass through.
        # `doctest` monkeypatches `linecache` module to enable
        # inspection, so let `linecache.getlines` to be called.
        if not (file.startswith("<") and file.endswith(">")):
            raise OSError("source code not available")

    module = inspect.getmodule(cls, file)
    if module:
        lines = linecache.getlines(file, module.__dict__)
    else:
        lines = linecache.getlines(file)
    if not lines:
        raise OSError("could not get source code")

    qualname = cls.__qualname__
    source = "".join(lines)
    tree = ast.parse(source)
    class_finder = _ChalkClassFinder(qualname)
    try:
        class_finder.visit(tree)
    except _ChalkClassFoundException as e:
        return e.node
    else:
        raise OSError("could not find class definition")


def get_function_ast(fn: Callable) -> ast.FunctionDef | ast.AsyncFunctionDef:
    file = get_source_filename(fn)
    if file:
        # Invalidate cache if needed.
        linecache.checkcache(file)
    else:
        file = inspect.getfile(fn)
        # Allow filenames in form of "<something>" to pass through.
        # `doctest` monkeypatches `linecache` module to enable
        # inspection, so let `linecache.getlines` to be called.
        if not (file.startswith("<") and file.endswith(">")):
            raise OSError("source code not available")

    module = inspect.getmodule(fn, file)
    if module:
        lines = linecache.getlines(file, module.__dict__)
    else:
        lines = linecache.getlines(file)
    if not lines:
        raise OSError("could not get source code")

    name = fn.__name__  # not a class so I think we should use the name
    source = "".join(lines)
    tree = ast.parse(source)
    function_finder = _ChalkFunctionFinder(name)
    try:
        function_finder.visit(tree)
    except _ChalkFunctionFoundException as e:
        return e.node
    else:
        raise OSError("could not find function definition")


def get_source_filename(obj: Any) -> Optional[str]:
    """Modified in first line from inspect.getsource(obj)"""
    try:
        filename = sys.modules[obj.__module__].__file__
    except:
        filename = inspect.getfile(obj)
    if filename is None:
        return None
    all_bytecode_suffixes = importlib.machinery.DEBUG_BYTECODE_SUFFIXES[:]
    all_bytecode_suffixes += importlib.machinery.OPTIMIZED_BYTECODE_SUFFIXES[:]
    if any(filename.endswith(s) for s in all_bytecode_suffixes):
        filename = os.path.splitext(filename)[0] + importlib.machinery.SOURCE_SUFFIXES[0]
    elif any(filename.endswith(s) for s in importlib.machinery.EXTENSION_SUFFIXES):
        return None
    if os.path.exists(filename):
        return filename
    # only return a non-existent filename if the module has a PEP 302 loader
    module = inspect.getmodule(obj, filename)
    if getattr(module, "__loader__", None) is not None:
        return filename
    elif getattr(getattr(module, "__spec__", None), "loader", None) is not None:
        return filename
    # or it is in the linecache
    elif filename in linecache.cache:
        return filename
    return None


@dataclass
class FunctionCallerInfo:
    """Information about the caller of a function, including AST node and source details."""

    node: ast.Call | None
    source: str
    filename: str
    lineno: int
    caller_source: str | None


def get_function_caller_info(frame_offset: int = 1) -> FunctionCallerInfo:
    """Extract caller information including AST node and source details.

    Args:
        frame_offset: How many frames back to look (1 = immediate caller)

    Returns:
        FunctionCallerInfo with node, source, filename, lineno, and extracted caller_source
    """
    caller_source: str | None = None
    caller_filename: str | None = None
    caller_lineno: int | None = None
    caller_node: ast.Call | None = None
    source: str = ""

    current_frame = inspect.currentframe()
    if current_frame is not None:
        # Walk back the specified number of frames
        frame: types.FrameType | None = current_frame
        for _ in range(frame_offset + 1):  # +1 because we start from current frame
            if (
                frame is None
            ):  # This can happen after frame.f_back assignment # pyright: ignore[reportUnnecessaryComparison]
                break
            if frame.f_back is None:
                break
            frame = frame.f_back

        if frame is not None:  # pyright: ignore[reportUnnecessaryComparison]
            caller_filename = inspect.getfile(frame)
            caller_lineno = inspect.getlineno(frame)

            # Extract just the function call invocation, not the entire file
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            source = "".join(linecache.getlines(filename))

            try:
                tree = ast.parse(source, filename)

                # Find the Call node whose lineno matches
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and node.lineno == lineno:
                        # Grab the full text of that node
                        caller_source = ast.get_source_segment(source, node)
                        caller_node = node
                        break
            except:
                # If AST parsing fails, fall back to whole file
                pass

            # Fallback to whole file if AST parsing fails
            if caller_source is None:
                try:
                    caller_source = inspect.getsource(frame)
                except:
                    caller_source = None

    # Delete the frame reference to break circular dependency and help garbage collection
    del current_frame

    return FunctionCallerInfo(
        node=caller_node,
        source=source,
        filename=caller_filename or "<unknown file>",
        lineno=caller_lineno or 0,
        caller_source=caller_source,
    )
