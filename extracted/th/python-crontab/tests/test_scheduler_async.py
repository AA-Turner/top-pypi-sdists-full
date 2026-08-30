#!/usr/bin/env python
#
# Copyright (C) 2025 Martin Owens
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.
#
"""
Test any internal async scheduling
"""

import os
import sys

import asyncio
import datetime
import crontab
import string
import random
import pytest

TEST_DIR = os.path.dirname(__file__)
COMMAND = os.path.join(TEST_DIR, 'data', 'crontest ')

try:
    import pytest_asyncio

    @pytest.mark.asyncio
    async def test_run_async():
        exact = (datetime.datetime.now().minute % 10) == 0
        slices = "*/10 * * * *"
        count = 10
        result = 1 + exact
        tab = crontab.CronTab()

        uid = random.choice(string.ascii_letters)
        tab.new(command=COMMAND + '-h ' + uid).setall(slices)

        proc = 0
        async for payload in tab.run_scheduler_async(count, cadence=0.01, warp=True):
            proc += 1
            assert payload == '-h|' + uid
        assert proc == result

except ImportError:
    def test_run_async():
        # skipTest("pytest-asyncio not installed")
        pass
