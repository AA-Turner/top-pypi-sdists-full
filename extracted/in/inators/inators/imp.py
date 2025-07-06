# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import importlib


def import_object(name):
    """
    Resolve a fully-qualified dotted name to an importable object inside a
    module (i.e., to a class, function, etc. in the module's global scope).

    E.g., ``'inators.imp.import_object'`` refers to :func:`import_object` in the
    :mod:`inators.imp` module, i.e., to this very function.

    :param str name: The fully-qualified dotted name to resolve.
    :return: The imported object.
    """

    steps = name.split('.')
    return getattr(importlib.import_module('.'.join(steps[0:-1])), steps[-1])
