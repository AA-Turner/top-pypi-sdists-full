# util/packaging.py
# Part of ‘python-daemon’, an implementation of PEP 3143.
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Custom packaging functionality for this project.

    This module provides functionality for Setuptools to dynamically derive
    project metadata at build time.
    """


def main_module_by_name(
        module_name,
        *,
        fromlist=None,
):
    """ Get the main module of this project, named `module_name`.

        :param module_name: The name of the module to import.
        :param fromlist: The list (of `str`) of names of objects to import in
            the module namespace.
        :return: The Python `module` object representing the main module.
        """
    module = __import__(module_name, level=0, fromlist=fromlist)
    return module


# Copyright © 2008–2024 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
