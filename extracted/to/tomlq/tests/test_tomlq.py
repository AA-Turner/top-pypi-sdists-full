#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tomlq` package."""

import pytest
import sys
from mock import patch
import tomlq


def test_run():
    testargs = ["tomlq", "-h"]
    with patch.object(sys, 'argv', testargs):
        with pytest.raises(SystemExit):
            tomlq.main()
