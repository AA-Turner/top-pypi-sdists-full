# test/test_util_packaging.py
# Part of ‘python-daemon’, an implementation of PEP 3143.
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit test for ‘util.packaging’ packaging module. """

import builtins
import types
import unittest.mock

import testscenarios

from util import packaging


class FakeModule(types.ModuleType):
    """ A fake module object with no code. """


def patch_builtins_import(
        testcase,
        *,
        fake_module=None,
        fake_module_name='lorem',
):
    """ Patch the built-in ‘__import__’ for the `testcase`. """
    if fake_module is None:
        fake_module = FakeModule(name=fake_module_name)

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        result = (
                fake_module if (name == fake_module_name)
                else orig_import(
                    name,
                    globals=globals, locals=locals,
                    fromlist=fromlist, level=level)
        )
        return result

    orig_import = builtins.__import__
    func_patcher = unittest.mock.patch.object(
            builtins, '__import__',
            wraps=fake_import)
    func_patcher.start()
    testcase.addCleanup(func_patcher.stop)


class main_module_by_name_TestCase(
        testscenarios.WithScenarios, unittest.TestCase):
    """ Test cases for ‘get_changelog_path’ function. """

    def setUp(self):
        """ Set up test fixtures. """
        super().setUp()

        self.test_module_name = 'lorem'
        self.test_module = FakeModule(self.test_module_name)
        patch_builtins_import(
            self,
            fake_module=self.test_module,
            fake_module_name=self.test_module_name,
        )

    def test_returns_expected_module_for_correct_name(self):
        """ Should return expected module object. """
        result = packaging.main_module_by_name(self.test_module_name)
        self.assertEqual(self.test_module, result)

    def test_raises_importerror_for_unexpected_name(self):
        """ Should raise ImportError when name is unexpected. """
        with self.assertRaises(ModuleNotFoundError):
            __ = packaging.main_module_by_name('b0gUs')


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
