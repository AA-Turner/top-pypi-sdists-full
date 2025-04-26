#! /usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2012 Jehan <tinysegmenter at zemarmot.net>
# TinySegmenter is freely distributable under the terms of a new BSD licence.
# See the COPYING file included with the distribution.

import tinysegmenter
import unittest

class Test(unittest.TestCase):
    # TODO: add new tests here.
    __basic_test_cases = {
        u'私の名前は中野です': [u'私', u'の', u'名前', u'は', u'中野', u'です'],
        u'東京に住む': [u'東京', u'に', u'住む'],
        u'フランスで赤ちゃんはbébéです。': [u'フランス', u'で', u'赤ちゃん', u'は', u'bébé', u'です', u'。']
        }

    def __run_test_cases(self, test_cases):
        segmenter = tinysegmenter.TinySegmenter()
        for text in test_cases:
            result = segmenter.tokenize(text)
            self.assertEqual(result, test_cases[text])

    # methods whose name start with "test" will be run by unittest.main().
    # Should later add special cases if they are discovered, debugged and fixed.

    def test_basic(self):
        self.__run_test_cases(self.__basic_test_cases)

if __name__ == '__main__':
    unittest.main()
