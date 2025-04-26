# -*- coding: utf-8 -*-
# ====================================================================
# Copyright (c) 2019 Open Source Applications Foundation.
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

import sys, os, six

from unittest import TestCase, main, SkipTest
from icu import *

class TestLocaleMatcher(TestCase):

    def setUp(self):
        if ICU_VERSION < '65.0':
            self.skipTest(ICU_VERSION)

    def testSetSupportedLocales(self):

        locales = (Locale.getFrance(), Locale.getGermany())
        matcher = LocaleMatcher.Builder().setSupportedLocales(locales).build()

        self.assertEqual(Locale.getFrance(),
                         matcher.getBestMatch(Locale.getItaly()))
        self.assertEqual(Locale.getGermany(),
                         matcher.getBestMatch(Locale('de-AT')))

    def testGetBestMatch(self):

        locales = (Locale.getFrance(), Locale.getGermany())
        matcher = LocaleMatcher.Builder().setSupportedLocales(locales).build()

        self.assertEqual(Locale.getGermany(),
                         matcher.getBestMatch((Locale('de-AT'), Locale('fr'))))

    def testGetBestMatchResult(self):

        locales = (Locale.getFrance(), Locale.getGermany())
        matcher = LocaleMatcher.Builder().setSupportedLocales(locales).build()
        result = matcher.getBestMatchResult((Locale('de-AT'), Locale('fr')))

        self.assertEqual(Locale('de-AT'), result.getDesiredLocale())
        self.assertEqual(Locale.getGermany(), result.getSupportedLocale())

    def testAcceptLanguage(self):

        locale, status = LocaleMatcher.acceptLanguage(
            ('fr-CH', 'fr', 'en', 'de', '*'), ('de-AT', 'fr-CA'))

        self.assertEqual('fr_CA', locale)
        self.assertEqual(UAcceptResult.FALLBACK, status)

        locale, status = LocaleMatcher.acceptLanguage(
            ('fr-CH', 'fr', 'en', 'de', '*'),
            list(Locale.getAvailableLocales().keys()))

        self.assertEqual('fr_CH', locale)
        self.assertEqual(UAcceptResult.VALID, status)

        locale, status = LocaleMatcher.acceptLanguage(
            ('fr-CH', 'fr', 'de'), ('en-CA',))
        self.assertEqual(None, locale)
        self.assertEqual(UAcceptResult.FAILED, status)

    def testAcceptLanguageFromHTTP(self):

        locale, status = LocaleMatcher.acceptLanguageFromHTTP(
            'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5', ('de-AT', 'fr-CA'))

        self.assertEqual('fr_CA', locale)
        self.assertEqual(UAcceptResult.FALLBACK, status)

        locale, status = LocaleMatcher.acceptLanguageFromHTTP(
            'fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5',
            list(Locale.getAvailableLocales().keys()))

        self.assertEqual('fr_CH', locale)
        self.assertEqual(UAcceptResult.VALID, status)

        locale, status = LocaleMatcher.acceptLanguageFromHTTP(
            'fr-CH, fr;q=0.9, de;q=0.7', ('en-CA',))
        self.assertEqual(None, locale)
        self.assertEqual(UAcceptResult.FAILED, status)


if __name__ == "__main__":
    if ICU_VERSION >= '65.0':
        main()
