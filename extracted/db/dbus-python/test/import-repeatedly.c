/* Regression test for https://bugs.freedesktop.org/show_bug.cgi?id=23831 */
/*
 * Copyright 2010-2016 Collabora Ltd.
 * SPDX-License-Identifier: MIT
 */

#include <stdio.h>

#include <Python.h>

#include "dbus_bindings-internal.h"

int main(void)
{
    int i;

    puts("1..1");

    for (i = 0; i < 100; ++i) {
        Py_Initialize();
        if (PyRun_SimpleString("import dbus\n") != 0) {
            puts("not ok 1 - there was an exception");
            return 1;
        }
        Py_Finalize();

#if DBUSPY_PY_VERSION_AT_LEAST(3, 12, 0, 0)
        puts("ok 1 # SKIP https://gitlab.freedesktop.org/dbus/dbus-python/-/issues/55");
        return 0;
#endif
    }

    puts("ok 1 - was able to import dbus 100 times");

    return 0;
}
