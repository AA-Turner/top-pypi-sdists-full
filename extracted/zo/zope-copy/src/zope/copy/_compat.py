##############################################################################
#
# Copyright (c) 2012 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zodbpickle.pickle import Pickler  # noqa: F401 imported but unused
from zodbpickle.pickle import Unpickler  # noqa: F401 imported but unused


def _memo(pickler):
    # Python uses a "PicklerMemoProxy" which is not subscriptable
    # by itself
    return pickler.memo.copy()


def _get_pid(pickler, oid):
    return _memo(pickler)[oid][0]


def _get_obj(unpickler, pid):
    return _memo(unpickler)[pid]
