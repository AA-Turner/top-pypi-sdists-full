# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import os

from tango import ApiUtil


def test_get_env_var():

    key = "MYTEST"
    value = "abcd"

    os.environ[key] = value
    assert ApiUtil.get_env_var(key) == value
