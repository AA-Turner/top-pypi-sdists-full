# -*- coding: utf-8 -*-
# ====================================================================
# Copyright (c) 2021-2021 Open Source Applications Foundation.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# ====================================================================
#

import sys, os

from unittest import TestCase, main
from icu import *

class TestMessagePattern(TestCase):

    def testMessagePattern(self):
        text = 'Test this {PLACEHOLDER}'
        pattern = MessagePattern(text)
        self.assertEqual(pattern.countParts(), 5)

        part = pattern.getPart(2)
        self.assertEqual(text[part.getIndex():part.getLimit()], "PLACEHOLDER")
        self.assertEqual(part.getType(), UMessagePatternPartType.ARG_NAME)
        self.assertEqual(pattern.getPartType(2), UMessagePatternPartType.ARG_NAME)
        self.assertEqual(pattern.getSubstring(part), "PLACEHOLDER")
        self.assertEqual(str(part), '([11:22] type=8, arg=0, val=0)')
        self.assertEqual(repr(part), '<MessagePattern_Part: ([11:22] type=8, arg=0, val=0)>')

    def testEscapingRelated(self):
        text = "This pattern can't be '{SIMPLE}'"
        pattern = MessagePattern(UMessagePatternApostropheMode.DOUBLE_OPTIONAL)
        pattern.parse(text)
        self.assertEqual(str(pattern), text)
        self.assertEqual(pattern.autoQuoteApostropheDeep(),
                         "This pattern can''t be '{SIMPLE}'")

    def testComplexPattern(self):
        text = """{GENDER, select,
                    male {{NUMBER, plural,
                      one {He wrote 1 ICU message.}
                      other {He wrote # ICU messages.}}}
                    female {{NUMBER, plural,
                      one {She wrote 1 ICU message.}
                      other {She wrote # ICU messages.}}}
                    other {{NUMBER, plural,
                      one {They wrote 1 ICU message.}
                      other {They wrote # ICU messages.}}}}"""
        pattern = MessagePattern(text)
        types = set([pattern.getPartType(i)
                     for i in range(0, pattern.countParts())])
        expected = {
            UMessagePatternPartType.MSG_START,
            UMessagePatternPartType.MSG_LIMIT,
            UMessagePatternPartType.REPLACE_NUMBER,
            UMessagePatternPartType.ARG_START,
            UMessagePatternPartType.ARG_LIMIT,
            UMessagePatternPartType.ARG_NAME,
            UMessagePatternPartType.ARG_SELECTOR,
        }
        self.assertEqual(types, expected)

if __name__ == "__main__":
    main()

