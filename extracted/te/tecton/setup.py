import codecs
import os.path
import pathlib

import setuptools


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    path = pathlib.Path(rel_path).resolve()
    if path.exists():
        for line in read(rel_path).splitlines():
            if line.startswith("VERSION"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        exc = RuntimeError("Unable to find version string.")
        raise exc
    else:
        # NOTE: we use `99.99.99.dev` here instead of raising an exception, since
        # pip-tools executes this file as part of dependency resolution. And our
        # version file isn't available nor necessary for it.
        return "99.99.99.dev"


setuptools.setup(version=get_version("tecton/_gen_version.py"))
