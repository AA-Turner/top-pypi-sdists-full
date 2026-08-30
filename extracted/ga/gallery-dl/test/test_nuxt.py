#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2026 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gallery_dl import text, dt  # noqa E402
from gallery_dl.extractor.utils import nuxt  # noqa E402


TEST_CASES_EQ = (
    ("int"   , [-42], -42),
    ("str"   , ["foo!!!"], "foo!!!"),
    ("Object", [{"foo": 1, "x-y": 2}, "bar", "z"], {"foo": "bar", "x-y": "z"}),
    ("Array"            , [[1, 2, 3], "a", "b", "c"], ["a", "b", "c"]),
    ("Array (empty)"    , [[]], []),
    ("Array (sparse)"   , [[-2, 1, -2], "b"], [None, "b", None]),
    ("str (repetition)" , [[1, 1], "astring"], ["astring", "astring"]),
    ("None (repetition)", [[1, 1], None], [None, None]),
    ("dict (repetition)", [[1, 1], {}], [{}, {}]),
    ("cross-realm POJO" , [{}], {}),
    ("Object without prototype", [["null"]], {}),

    ("Number", [["Object", 42]], 42),
    ("String", [["Object", "var"]], "var"),
    ("RegExp", [["RegExp", "regexp", "gim"]], text.re_compile("regexp")),
    ("Date"  , [["Date", "2001-09-09T01:46:40.000Z"]], dt.datetime(2001, 9, 9, 1, 46, 40)),  # noqa: E501
    ("Set"   , [["Set", 1, 2, 3], 1, 2, 3], [1, 2, 3]),
    ("Map"   , [["Map", 1, 2], "a", "b"], [["a", "b"]]),
    ("BigInt", [["BigInt", "1"]], 1),
    ("Uint8Array" , [["Uint8Array", "AQID"]], [1, 2, 3]),
    ("ArrayBuffer", [["ArrayBuffer", "AQID"]], [1, 2, 3]),
)

TEST_CASES_IS = (
    ("bool"     , [True], True),
    ("Boolean"  , [["Object", False]], False),
    ("null"     , [None], None),
)

TEST_CASES_ERR = (
    ("empty string", ""  , IndexError, "string index out of range"),
    ("number"      , 42  , TypeError , "'int' object is not subscriptable"),
    ("boolean"     , True, TypeError , "'bool' object is not subscriptable"),
    ("null"        , None, TypeError , "'NoneType' object is not subscriptable"),  # noqa: E501
    ("object"      , {}  , KeyError  , "0"),
    ("empty array" , []  , IndexError, "list index out of range"),
    ("Python negative indexing",
     [[1, 2, 3, 4, 5, 6, 7, -7], 1, 2, 3, 4, 5, 6, 7],
     IndexError, "invalid index: -7"),
)


class TestDevalue(unittest.TestCase):
    def test_nuxt_resolve_equals(self):
        for name, input, expected in TEST_CASES_EQ:
            self.assertEqual(nuxt.resolve(input), expected, name)

    def test_nuxt_resolve_is(self):
        for name, input, expected in TEST_CASES_IS:
            self.assertIs(nuxt.resolve(input), expected, name)

    def test_nuxt_resolve_err(self):
        for name, input, exc, msg in TEST_CASES_ERR:
            with self.assertLogs("nuxt") as log_info:
                nuxt.resolve(input)
            self.assertEqual(len(log_info.output), 1, name)
            self.assertRegex(log_info.output[0],
                             f"^ERROR:nuxt:{exc.__name__}: .*{msg}", name)

    def test_nuxt_resolve_cyclical(self):
        name = "Map (cyclical)"
        result = nuxt.resolve([["Map", 1, 0], "self"])
        self.assertEqual(result[0][0], "self", name)
        self.assertIs(result, result[0][1], name)

        name = "Set (cyclical)"
        result = nuxt.resolve([["Set", 0, 1], 42])
        self.assertEqual(result[1], 42, name)
        self.assertIs(result, result[0], name)

        result = nuxt.resolve([[0]])
        self.assertIs(result, result[0], "Array (cyclical)")

        name = "Object (cyclical)"
        result = nuxt.resolve([{"self": 0}])
        self.assertIs(result, result["self"], name)

        name = "Object with null prototype (cyclical)"
        result = nuxt.resolve([["null", "self", 0]])
        self.assertIs(result, result["self"], name)

        name = "Objects (cyclical)"
        result = nuxt.resolve([[1, 2], {"second": 2}, {"first": 1}])
        self.assertIs(result[0], result[1]["first"], name)
        self.assertIs(result[1], result[0]["second"], name)


if __name__ == "__main__":
    unittest.main()
