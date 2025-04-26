# -*- coding: utf-8 -*-
# Copyright 2019 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Test module for ansicon
"""

import unittest

import ansicon


class TestANSICON(unittest.TestCase):
    """
    Basic tests for ansicon
    """

    def test_load_unload(self):
        """
        Load/Unload DLL without raising an error
        """

        # Make sure we're not already loaded
        self.assertFalse(ansicon.loaded())

        # Test print
        print('\n')
        print(u'\x1b[32m UNLOADED \x1b[m')

        # Load without error
        ansicon.load()
        self.assertTrue(ansicon.loaded())

        # Test print
        print(u'\x1b[32m LOADED \x1b[m')

        # Make sure loading again doesn't throw an error
        ansicon.load()

        # unload without error
        ansicon.unload()
        self.assertFalse(ansicon.loaded())

        # Test print
        print(u'\x1b[32m UNLOADED \x1b[m')

        # Make sure unloading again doesn't throw an error
        ansicon.unload()

    def test_unload_fail(self):
        """
        Raise an Error when operation fails
        """

        # Load and capture handle
        ansicon.load()
        old_dll = ansicon._ANSICON.dll  # pylint: disable=protected-access

        # Unload
        ansicon.unload()

        # Force failure with old handle
        ansicon._ANSICON.dll = old_dll  # pylint: disable=protected-access
        with self.assertRaises(WindowsError):  # pylint: disable=undefined-variable
            ansicon.unload()
