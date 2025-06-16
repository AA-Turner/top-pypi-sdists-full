# -*- coding: utf-8 -*-

"""Test CLR method support."""

import System
import pytest
from Python.Test import Pep8Test

def test_pep8_method():
    """Test PEP8-styled alias of method."""
    assert "hello" == Pep8Test().Foo()
    assert "hello" == Pep8Test().foo()


def test_pep8_property():
    """Test PEP8-styled alias of property."""
    pep8_test = Pep8Test()
    assert 1 == pep8_test.Bar
    pep8_test.Bar = 2
    assert 2 == pep8_test.bar
    pep8_test.bar = 3
    assert 3 == pep8_test.bar


def test_pep8_field():
    """Test PEP8-styled alias of field."""
    pep8_test = Pep8Test()
    assert 3.14 == pep8_test.BazPi
    assert 3.14 == pep8_test.baz_pi
    pep8_test.baz_pi = 3.1415
    assert 3.1415 == pep8_test.BazPi
