#!/usr/bin/env python
"""flowtask.

    Framework for Task orchestration.
See:
https://github.com/phenobarbital/flowtask
"""
import ast
from os import path

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup


def get_path(filename):
    """get_path.
    Get relative path for a file.
    """
    return path.join(path.dirname(path.abspath(__file__)), filename)


def readme():
    """readme.
    Get the content of README file.
    Returns:
        str: string of README file.
    """
    with open(get_path('README.md'), encoding='utf-8') as file:
        return file.read()


version = get_path('flowtask/version.py')
with open(version, 'r', encoding='utf-8') as meta:
    t = compile(meta.read(), version, 'exec', ast.PyCF_ONLY_AST)
    for node in (n for n in t.body if isinstance(n, ast.Assign)):
        if len(node.targets) == 1:
            name = node.targets[0]
            if isinstance(name, ast.Name) and name.id == '__version__':
                __version__ = node.value.s
                break


COMPILE_ARGS = ["-O2"]

extensions = [
    Extension(
        name='flowtask.parsers.base',
        sources=['flowtask/parsers/base.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers._yaml',
        sources=['flowtask/parsers/_yaml.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers.json',
        sources=['flowtask/parsers/json.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.parsers.toml',
        sources=['flowtask/parsers/toml.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.utils.parserqs',
        sources=['flowtask/utils/parseqs.pyx'],
        extra_compile_args=COMPILE_ARGS,
    ),
    Extension(
        name='flowtask.utils.json',
        sources=['flowtask/utils/json.pyx'],
        extra_compile_args=COMPILE_ARGS,
        language="c++"
    ),
    Extension(
        name='flowtask.types.typedefs',
        sources=['flowtask/types/typedefs.pyx'],
        extra_compile_args=COMPILE_ARGS
    ),
    Extension(
        name='flowtask.utils.functions',
        sources=['flowtask/utils/functions.pyx'],
        extra_compile_args=COMPILE_ARGS,
        language="c++"
    ),
]


setup(
    ext_modules=cythonize(extensions),
)
