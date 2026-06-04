#!/usr/bin/env python3
# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
#
# client example: executing commands with simplified syntax

import sys
from tango import DeviceProxy, DevFailed, Except

dev_name = "sys/tg_test/1"
cmd_name = "DevShort"

# step 1 create the device proxy
try:
    dev = DeviceProxy(dev_name)
    print(f"proxy for {dev_name} created")
except DevFailed as ex:
    print("failed to create DeviceProxy")
    Except.print_exception(ex)
    sys.exit(1)

try:
    data_out = dev.DevShort(1234)  # simplified and more natural syntax
    print(f"command_inout DevShort result: {data_out}")
    my_dbl = 1.22  # here my_dbl  is a float
    my_str = "ABC"  # here my_str  is a string
    print(f"types of variables before data_out extraction: {type(data_out)}, {type(my_dbl)}, {type(my_str)}")
    my_dbl = data_out  # here my_dbl turns into a short
    my_str = data_out  # here my_str turns into a short
    print(
        f"command_inout DevVoid results extracted to existing variable: "
        f"{data_out}, {my_dbl}, {my_str}, {type(data_out)}, {type(my_dbl)}, {type(my_str)}"
    )
    # type of variables changes if handled by python! powerful, easy, can play tricks...
except DevFailed as ex:
    print("failed to execute command DevShort")

# now with DevVoid
try:
    dev.DevVoid()
    print("command_inout DevVoid OK")
except DevFailed as ex:
    print("failed to execute command DevVoid")

"""
Typical output:

➜  training git:(develop) ✗ docker-compose exec cli /training/client/command02.py
proxy for sys/tg_test/1 created
command_inout DevShort result: 1234
types of variables before data_out extraction: <class 'int'>, <class 'float'>, <class 'str'>
command_inout DevVoid results extracted to existing variable: 1234, 1234, 1234, <class 'int'>, <class 'int'>, <class 'int'>
command_inout DevVoid OK
"""
