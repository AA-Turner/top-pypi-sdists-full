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

import sys, os, six, datetime

from unittest import TestCase, main
from icu import *


class TestTimeZone(TestCase):

    def testBasic(self):

        tz = TimeZone.createTimeZone("America/Los_Angeles")
        self.assertTrue(isinstance(tz, BasicTimeZone))
        self.assertEqual(str(tz), "America/Los_Angeles")

    def testGetRules(self):

        tz = TimeZone.createTimeZone("America/Los_Angeles")
        rules = tz.getTimeZoneRules()
        self.assertTrue(len(rules) > 0)
        self.assertTrue(isinstance(rules[0], InitialTimeZoneRule))
        for rule in rules[1:]:
          self.assertTrue(
              isinstance(rule, (TimeArrayTimeZoneRule, AnnualTimeZoneRule)))

    def testVTimeZone(self):

        vtz = VTimeZone.createVTimeZoneByID("Pacific/Fiji")
        data = vtz.write()

        vtz.createVTimeZone(data)
        self.assertEqual(vtz.write(), data)

        data = vtz.writeSimple(
            datetime.datetime(2021, 4, 10, 12, 43, 33, 411400))
        self.assertTrue(data.startswith(
            "BEGIN:VTIMEZONE\r\nTZID:Pacific/Fiji\r\n"))

        if ICU_VERSION >= '4.6':
            tz = TimeZone.createTimeZone("America/Los_Angeles")
            vtz = VTimeZone.createVTimeZoneFromBasicTimeZone(tz)
            data = vtz.write()
            vtz.createVTimeZone(data)
            self.assertEqual(vtz.write(), data)

    def testTransition(self):

        tz = TimeZone.createTimeZone("Pacific/Fiji")
        pytz = ICUtzinfo.getInstance("Pacific/Fiji")

        tzr = tz.getNextTransition(
            datetime.datetime(2021, 4, 10, 12, 43, 33, tzinfo=pytz))

        tzr_time = tzr.getTime()
        self.assertEqual(datetime.datetime.fromtimestamp(tzr_time, pytz),
                         datetime.datetime(2021, 11, 14, 2, 0, tzinfo=pytz))

        pytz = ICUtzinfo.getInstance("America/Los_Angeles")
        self.assertEqual(datetime.datetime.fromtimestamp(tzr_time, pytz),
                         datetime.datetime(2021, 11, 13, 6, 0, tzinfo=pytz))


if __name__ == "__main__":
    main()
