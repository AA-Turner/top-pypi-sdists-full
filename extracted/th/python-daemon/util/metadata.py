# util/metadata.py
# Part of ‘python-daemon’, an implementation of PEP 3143.
#
# This is free software, and you are welcome to redistribute it under
# certain conditions; see the end of this file for copyright
# information, grant of license, and disclaimer of warranty.

""" Functionality to work with project metadata.

    This module implements ways to derive various project metadata at build
    time.
    """

import collections
import inspect
import pydoc
import re

import chug.parsers.rest


rfc822_person_regex = re.compile(
        r"^(?P<name>[^<]+) <(?P<email>[^>]+)>$")

ParsedPerson = collections.namedtuple('ParsedPerson', ['name', 'email'])


def parse_person_field(value):
    """ Parse a person field into name and email address.

        :param value: The text value specifying a person.
        :return: A 2-tuple (name, email) for the person's details.

        If the `value` does not match a standard person with email
        address, the `email` item is ``None``.
        """
    result = ParsedPerson(None, None)

    match = rfc822_person_regex.match(value)
    if len(value):
        if match is not None:
            result = ParsedPerson(
                    name=match.group('name'),
                    email=match.group('email'))
        else:
            result = ParsedPerson(name=value, email=None)

    return result


def docstring_from_object(object):
    """ Extract the `object` docstring as a simple text string.

        :param object: The Python object to inspect.
        :return: The docstring (text), “cleaned” according to :PEP:`257`.
        """
    docstring = inspect.getdoc(object)
    return docstring


DescriptionMetadata = collections.namedtuple(
    'DescriptionMetadata',
    ['synopsis', 'long_description', 'content_type'])


def description_fields_from_docstring(
        docstring,
        *,
        content_type="text/plain"
):
    """ Parse metadata description fields, from `docstring`.

        :param docstring: The documentation string (“docstring”, text) to
            parse.
        :param content_type: The MIME Content-Type value to describe the
            content of the long description.
        :return: A `DescriptionMetadata` instance representing the information
            parsed from `docstring`.

        The `docstring` is expected to be a document of the form described in
        :PEP:`257`:

        > Multi-line docstrings consist of a summary line just like a one-line
        > docstring, followed by a blank line, followed by a more elaborate
        > description.
        """
    (synopsis, long_description) = pydoc.splitdoc(docstring)
    metadata = DescriptionMetadata(
        synopsis=synopsis,
        long_description=long_description,
        content_type=content_type,
    )
    return metadata


def synopsis_and_description_from_docstring(docstring):
    """ Parse one-line synopsis and long description, from `docstring`.

        :param docstring: The documentation string (“docstring”, text) to
            parse.
        :return: A 2-tuple (`synopsis`, `long_description`) of the values
            parsed from `docstring`.

        The `docstring` is expected to be of the form described in :PEP:`257`:

        > Multi-line docstrings consist of a summary line just like a one-line
        > docstring, followed by a blank line, followed by a more elaborate
        > description.
        """
    (synopsis, long_description) = pydoc.splitdoc(docstring)
    return (synopsis, long_description)


def get_latest_changelog_entry(infile_path):
    """ Get the latest entry data from the changelog at `infile_path`.

        :param infile_path: The filesystem path (text) from which to read the
            change log document.
        :return: The most recent change log entry, as a `chug.ChangeLogEntry`.
        """
    document_text = chug.parsers.get_changelog_document_text(infile_path)
    document = chug.parsers.rest.parse_rest_document_from_text(document_text)
    entries = chug.parsers.rest.make_change_log_entries_from_document(
        document)
    latest_entry = entries[0]
    return latest_entry


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
