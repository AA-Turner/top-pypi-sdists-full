# Copyright (c) 2018, Dirk Gütlin & Thomas Hartmann
# All rights reserved.
#
# This file is part of the pymatreader Project, see: https://gitlab.com/obob/pymatreader
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Test helper functions."""

import contextlib
import string
import types
from pathlib import Path

import numpy as np
import xmltodict


def assertDeepAlmostEqual(expected, actual, *args, **kwargs):  # noqa PLR0912
    # This code has been adapted from https://github.com/larsbutler/oq-engine/blob/master/tests/utils/helpers.py
    """
    Assert that two complex structures have almost equal contents.

    Compares lists, dicts and tuples recursively. Checks numeric values
    using test_case's :py:meth:`unittest.TestCase.assertAlmostEqual` and
    checks all other values with :py:meth:`unittest.TestCase.assertEqual`.
    Accepts additional positional and keyword arguments and pass those
    intact to assertAlmostEqual() (that's how you specify comparison
    precision).
    """
    is_root = '__trace' not in kwargs
    trace = kwargs.pop('__trace', 'ROOT')

    if isinstance(expected, np.ndarray) and expected.size == 0:
        expected = None

    if isinstance(actual, np.ndarray) and actual.size == 0:
        actual = None

    try:
        if isinstance(expected, (int, float, complex)):
            np.testing.assert_almost_equal(expected, actual, *args, **kwargs)
        elif isinstance(expected, (list, tuple, np.ndarray, types.GeneratorType)):
            if isinstance(expected, types.GeneratorType):
                expected = list(expected)
                actual = list(actual)
            # if any of them are None, len(None) throws a TypeError
            try:
                assert len(expected) == len(actual)
            except TypeError:
                # if both are None, they are equal
                if not expected and not actual:
                    pass
                else:
                    raise AssertionError

            for index in range(len(expected)):
                v1, v2 = expected[index], actual[index]
                assertDeepAlmostEqual(v1, v2, __trace=repr(index), *args, **kwargs)
        elif isinstance(expected, dict):
            assert set(expected) == set(actual)
            for key in expected:
                assertDeepAlmostEqual(expected[key], actual[key], __trace=repr(key), *args, **kwargs)
        else:
            assert expected == actual
    except AssertionError as exc:
        exc.__dict__.setdefault('traces', []).append(trace)
        if is_root:
            trace = ' -> '.join(reversed(exc.traces))
            message = ''
            with contextlib.suppress(AttributeError):
                message = exc.message
            exc = AssertionError(f'{message}\nTRACE: {trace}')
        raise exc


def _sanitize_dict(d):
    d = {k: d[k] for k in d if not k.startswith('__')}

    return d


def _read_xml_data(f_name):
    with Path(f_name).open('rb') as xml_file:
        xml_data = xmltodict.parse(xml_file)

    new_data = _convert_strings2numbers_xml(xml_data)

    return new_data['test_data']['for_xml']


def _convert_strings2numbers_xml(xml_data):
    if isinstance(xml_data, dict):
        if len(xml_data.keys()) == 1 and list(xml_data.keys())[0] == 'item' and isinstance(xml_data['item'], list):
            xml_data = np.array(_convert_strings2numbers_xml(xml_data['item']))
        else:
            for cur_key in xml_data:
                xml_data[cur_key] = _convert_strings2numbers_xml(xml_data[cur_key])
    elif isinstance(xml_data, list):
        new_list = []
        for cur_item in xml_data:
            new_list.append(_convert_strings2numbers_xml(cur_item))

        xml_data = new_list
    elif isinstance(xml_data, str) and _is_string_matrix(xml_data):
        try:
            xml_data = np.array(np.asmatrix(str(xml_data).replace('i', 'j')))
            if xml_data.size == 1:
                xml_data = xml_data[0][0]
        except ValueError:
            pass
    elif isinstance(xml_data, str) and xml_data.startswith('[uint'):
        num_str = xml_data[8:-2]
        return int(num_str)

    return xml_data


def _is_string_matrix(value):
    ok = string.digits + '.,; []e-ij+'
    return all(c in ok for c in value)
