# test/test_util_metadata.py
# Part of ‘python-daemon’, an implementation of PEP 3143.
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Unit test for ‘util.metadata’ packaging module. """

import textwrap

import testscenarios
import testtools

import chug.model

import util.metadata

from .scaffold import mock_builtin_open_for_fake_files


class parse_person_field_TestCase(
        testscenarios.WithScenarios, testtools.TestCase):
    """ Test cases for ‘get_latest_version’ function. """

    scenarios = [
            ('simple', {
                'test_person': "Foo Bar <foo.bar@example.com>",
                'expected_result': ("Foo Bar", "foo.bar@example.com"),
                }),
            ('empty', {
                'test_person': "",
                'expected_result': (None, None),
                }),
            ('none', {
                'test_person': None,
                'expected_error': TypeError,
                }),
            ('no email', {
                'test_person': "Foo Bar",
                'expected_result': ("Foo Bar", None),
                }),
            ]

    def test_returns_expected_result(self):
        """ Should return expected result. """
        if hasattr(self, 'expected_error'):
            self.assertRaises(
                    self.expected_error,
                    util.metadata.parse_person_field, self.test_person)
        else:
            result = util.metadata.parse_person_field(self.test_person)
            self.assertEqual(self.expected_result, result)


class FakeObject(object):
    """ A fake object for testing. """


class docstring_from_object_TestCase(
        testscenarios.WithScenarios, testtools.TestCase):
    """ Test cases for ‘docstring_from_object’ function. """

    scenarios = [
            ('single-line', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.
                    """),
                'expected_result': "Lorem ipsum, dolor sit amet.",
                }),
            ('synopsis one-paragraph', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.
                    """),
                'expected_result': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis."""),
                }),
            ('synopsis three-paragraphs', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Ut ac ultrices turpis. Nam tellus ex, scelerisque ac
                    tellus ac, placerat convallis erat. Nunc id mi libero.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.

                    Suspendisse potenti. Fusce egestas id quam non posuere.
                    Maecenas egestas faucibus elit. Aliquam erat volutpat.
                    """),
                'expected_result': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Ut ac ultrices turpis. Nam tellus ex, scelerisque ac
                    tellus ac, placerat convallis erat. Nunc id mi libero.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.

                    Suspendisse potenti. Fusce egestas id quam non posuere.
                    Maecenas egestas faucibus elit. Aliquam erat volutpat."""),
                }),
            ]

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()
        self.test_object = FakeObject()
        self.test_object.__doc__ = self.test_docstring

    def test_returns_expected_result(self):
        """ Should return expected result. """
        result = util.metadata.docstring_from_object(self.test_object)
        self.assertEqual(self.expected_result, result)


class description_fields_from_docstring_TestCase(
        testscenarios.WithScenarios, testtools.TestCase):
    """ Test cases for ‘description_fields_from_docstring’ function. """

    function_to_test = staticmethod(
        util.metadata.description_fields_from_docstring)

    docstring_scenarios = [
            ('single-line', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.
                    """),
                'expected_synopsis': "Lorem ipsum, dolor sit amet.",
                'expected_description': "",
                }),
            ('synopsis one-paragraph', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.
                    """),
                'expected_synopsis': "Lorem ipsum, dolor sit amet.",
                'expected_description': textwrap.dedent("""\
                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis."""),
                }),
            ('synopsis three-paragraphs', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Ut ac ultrices turpis. Nam tellus ex, scelerisque ac
                    tellus ac, placerat convallis erat. Nunc id mi libero.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.

                    Suspendisse potenti. Fusce egestas id quam non posuere.
                    Maecenas egestas faucibus elit. Aliquam erat volutpat.
                    """),
                'expected_synopsis': "Lorem ipsum, dolor sit amet.",
                'expected_description': textwrap.dedent("""\
                    Ut ac ultrices turpis. Nam tellus ex, scelerisque ac
                    tellus ac, placerat convallis erat. Nunc id mi libero.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.

                    Suspendisse potenti. Fusce egestas id quam non posuere.
                    Maecenas egestas faucibus elit. Aliquam erat volutpat."""),
                }),
            ]

    content_type_scenarios = [
        ('default', {
            'expected_content_type': "text/plain",
        }),
        ('text-plain', {
            'test_content_type': "text/plain",
            'expected_content_type': "text/plain",
        }),
        ('text-rst', {
            'test_content_type': "text/x-rst",
            'expected_content_type': "text/x-rst",
        }),
        ('text-markdown', {
            'test_content_type': "text/x-markdown",
            'expected_content_type': "text/x-markdown",
        }),
    ]

    scenarios = testscenarios.multiply_scenarios(
            docstring_scenarios, content_type_scenarios)

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.expected_content_type = (
            self.test_content_type if getattr(self, 'test_content_type', None)
            else "text/plain")

        self.test_args = [self.test_docstring]
        self.test_kwargs = dict()
        if hasattr(self, 'test_content_type'):
            self.test_kwargs['content_type'] = self.test_content_type

    def test_returns_expected_result(self):
        """ Should return expected result. """
        result = util.metadata.description_fields_from_docstring(
                *self.test_args, **self.test_kwargs)
        expected_result = util.metadata.DescriptionMetadata(
                synopsis=self.expected_synopsis,
                long_description=self.expected_description,
                content_type=self.expected_content_type,
        )
        self.assertEqual(expected_result, result)


class synopsis_and_description_from_docstring_TestCase(
        testscenarios.WithScenarios, testtools.TestCase):
    """ Test cases for ‘synopsis_and_description_from_docstring’ function. """

    scenarios = [
            ('single-line', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.
                    """),
                'expected_synopsis': "Lorem ipsum, dolor sit amet.",
                'expected_description': "",
                }),
            ('synopsis one-paragraph', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.
                    """),
                'expected_synopsis': "Lorem ipsum, dolor sit amet.",
                'expected_description': textwrap.dedent("""\
                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis."""),
                }),
            ('synopsis three-paragraphs', {
                'test_docstring': textwrap.dedent("""\
                    Lorem ipsum, dolor sit amet.

                    Ut ac ultrices turpis. Nam tellus ex, scelerisque ac
                    tellus ac, placerat convallis erat. Nunc id mi libero.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.

                    Suspendisse potenti. Fusce egestas id quam non posuere.
                    Maecenas egestas faucibus elit. Aliquam erat volutpat.
                    """),
                'expected_synopsis': "Lorem ipsum, dolor sit amet.",
                'expected_description': textwrap.dedent("""\
                    Ut ac ultrices turpis. Nam tellus ex, scelerisque ac
                    tellus ac, placerat convallis erat. Nunc id mi libero.

                    Donec et semper sapien, et faucibus felis. Nunc suscipit
                    quam id lectus imperdiet varius. Praesent mattis arcu in
                    sem laoreet, at tincidunt velit venenatis.

                    Suspendisse potenti. Fusce egestas id quam non posuere.
                    Maecenas egestas faucibus elit. Aliquam erat volutpat."""),
                }),
            ]

    def test_returns_expected_result(self):
        """ Should return expected result. """
        result = util.metadata.synopsis_and_description_from_docstring(
                self.test_docstring)
        expected_result = (self.expected_synopsis, self.expected_description)
        self.assertEqual(expected_result, result)


class get_latest_changelog_entry_TestCase(testtools.TestCase):
    """ Test cases for ‘get_latest_changelog_entry’ function. """

    function_to_test = staticmethod(util.metadata.get_latest_changelog_entry)

    def setUp(self):
        """ Set up fixtures for this test case. """
        super().setUp()

        self.test_document_path = "/example/path/ChangeLog"
        self.setup_mock_changelog_file(path=self.test_document_path)

        self.test_args = [self.test_document_path]

    def setup_mock_changelog_file(self, path):
        fake_changelog_file_text = textwrap.dedent("""\
            Change Log
            ##########

            Version 1.7.2
            =============

            :Released: 2020-01-10
            :Maintainer: Cathy Morris <cathy.morris@example.com>

            …

            Version 1.5
            ===========

            :Released: 2019-08-04
            :Maintainer: Luis Flores <ayalaian@example.org>

            …
            """)
        mock_builtin_open_for_fake_files(
            self,
            fake_file_content_by_path={
                path: fake_changelog_file_text,
            })

    def test_returns_expected_result(self):
        """ Should return expected result. """
        result = self.function_to_test(*self.test_args)
        expected_result = chug.model.ChangeLogEntry(
            version="1.7.2",
            release_date="2020-01-10",
            maintainer="Cathy Morris <cathy.morris@example.com>",
            body="…",
        )
        self.assertEqual(expected_result, result)


# Copyright © 2008–2024 Ben Finney <ben+python@benfinney.id.au>
#
# This is free software: you may copy, modify, and/or distribute this work
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of that license or any later version.
# No warranty expressed or implied. See the file ‘LICENSE.GPL-3’ for details.


# Local variables:
# coding: utf-8
# mode: python
# End:
# vim: fileencoding=utf-8 filetype=python :
