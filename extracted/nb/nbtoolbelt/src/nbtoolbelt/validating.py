"""
Functions for validating notebooks

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import nbformat
from nbformat import NotebookNode


def validate_nb(nb: NotebookNode, assertive: bool) -> bool:
    """Validate notebook.

    :param nb: notebook to validate
    :param assertive: whether to raise an exception when invalid
    :return: whether ``nb`` is valid
    """
    try:
        nbformat.validate(nb)
        return True
    except nbformat.ValidationError:
        if assertive:
            raise
        else:
            return False
