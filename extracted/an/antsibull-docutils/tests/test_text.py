# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test text module.
"""

from __future__ import annotations

import typing as t

import pytest

from antsibull_docutils._collector import ANSIState, EmptyState
from antsibull_docutils._string import ASCIIStringProcessor, UnicodeStringProcessor
from antsibull_docutils.text import (
    GlobalContext,
    _Context,
    _DocumentContext,
    _get_formatting_state,
    _get_string_proc,
    get_column_count,
    render_as_text,
    render_bold,
    render_title,
)
from antsibull_docutils.utils import get_document_structure

RENDER_AS_TEXT_AND_STRUCTURE_DATA: list[
    tuple[str, str, t.Literal["markdown", "restructuredtext"], str, set[str]]
] = [
    (
        "empty",
        "",
        "restructuredtext",
        "",
        set(),
    ),
    (
        "hello-world",
        "Hello world.",
        "restructuredtext",
        r"Hello world.",
        set(),
    ),
    (
        "link",
        "`foo <bar>`__",
        "restructuredtext",
        "\x1b[0;4mfoo\x1b[0m (\x1b[0;4mbar\x1b[0m)",
        set(),
    ),
    (
        "url",
        "https://example.com/foo https://example.com/~foo%20bar?a=b&c=d+e",
        "restructuredtext",
        "\x1b[0;4mhttps://example.com/foo\x1b[0m \x1b[0;4mhttps://example.com/~foo%20bar?a=b&c=d+e\x1b[0m",
        set(),
    ),
    (
        "lorem-ipsum",
        r"""
Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex
sapien ``vitae pellentesque sem placerat``. In id cursus mi pretium tellus duis
convallis. Tempus leo eu aenean sed diam urna tempor. **Pulvinar vivamus
fringilla lacus nec metus bibendum egestas.** Iaculis massa nisl malesuada
lacinia integer nunc posuere. *Ut hendrerit semper vel class aptent taciti
sociosqu.* Ad litora torquent per conubia nostra inceptos himenaeos.

Lorem ipsum dolor sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua::

  Ut enim ad minim veniam, quis nostrud exercitation
    ullamco laboris nisi ut aliquip ex ea commodo consequat.

* Lorem ipsum dolor sit *amet consectetur* adipiscing elit. Quisque faucibus ex
  sapien vitae pellentesque sem placerat. **In id cursus** mi pretium tellus duis
  convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus
  fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada
  lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti
  sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.

  * Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex
    sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis
    convallis. Tempus leo eu aenean sed diam urna tempor.

    * Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex
      sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis
      convallis.

      * Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex
        sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis
        convallis.

        * Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex
          sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis
          convallis.
""",
        "restructuredtext",
        """Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex
sapien `vitae pellentesque sem placerat`. In id cursus mi pretium tellus duis
convallis. Tempus leo eu aenean sed diam urna tempor. \x1b[0;1mPulvinar vivamus fringilla\x1b[0m
\x1b[0;1mlacus nec metus bibendum egestas.\x1b[0m Iaculis massa nisl malesuada lacinia integer
nunc posuere. \x1b[0;3mUt hendrerit semper vel class aptent taciti sociosqu.\x1b[0m Ad litora
torquent per conubia nostra inceptos himenaeos.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua:

  Ut enim ad minim veniam, quis nostrud exercitation
    ullamco laboris nisi ut aliquip ex ea commodo consequat.

- Lorem ipsum dolor sit \x1b[0;3mamet consectetur\x1b[0m adipiscing elit. Quisque faucibus ex
  sapien vitae pellentesque sem placerat. \x1b[0;1mIn id cursus\x1b[0m mi pretium tellus duis
  convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus
  fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada
  lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti
  sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.

  - Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus
    ex sapien vitae pellentesque sem placerat. In id cursus mi pretium
    tellus duis convallis. Tempus leo eu aenean sed diam urna tempor.

    - Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque
      faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi
      pretium tellus duis convallis.

      - Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque
        faucibus ex sapien vitae pellentesque sem placerat. In id cursus
        mi pretium tellus duis convallis.

        - Lorem ipsum dolor sit amet consectetur adipiscing elit.
          Quisque faucibus ex sapien vitae pellentesque sem placerat.
          In id cursus mi pretium tellus duis convallis.""",
        set(),
    ),
    (
        "list",
        r"""
A list:

* an :emphasis:`entry`
* another :strong:`one`

  + a nested list entry
  + another one
""",
        "restructuredtext",
        """A list:

- an \x1b[0;3mentry\x1b[0m
- another \x1b[0;1mone\x1b[0m

  - a nested list entry
  - another one""",
        set(),
    ),
    (
        "enumeration",
        r"""
An enumeration:

1. an :literal:`entry`

   it has two lines.

   .. code-block::

       And some code.

2. another one

3.

4. a last one
""",
        "restructuredtext",
        """An enumeration:

1. an `entry`

   it has two lines.

     And some code.
2. another one
3.
4. a last one""",
        set(),
    ),
    (
        "test-doc",
        r"""
========
Test doc
========

.. contents::
   :local:
   :depth: 2

A test document.

.. _label:

Test section
------------

This is a test section. It has a label.

.. code-block::

    Code without language

.. This is a comment

Another code block::

    ````
    This one has no language, either.
    ````

Test subsection
^^^^^^^^^^^^^^^

Linking the `label`_.

.. code-block:: python

    def f():
        return 42

Another section
---------------

Buh!

    Some block quote.
    Another line.

A line.

.. note::

  This is a note.
  A second line!

  And a second paragraph.
""",
        "restructuredtext",
        """\x1b[0;1mTest doc\x1b[0m
\x1b[0;1m════════\x1b[0m

- \x1b[0;4mTest section\x1b[0m

  - \x1b[0;4mTest subsection\x1b[0m
- \x1b[0;4mAnother section\x1b[0m

A test document.

\x1b[0;1mTest section\x1b[0m
\x1b[0;1m━━━━━━━━━━━━\x1b[0m

This is a test section. It has a label.

  Code without language

Another code block:

  ````
  This one has no language, either.
  ````

\x1b[0;1mTest subsection\x1b[0m
\x1b[0;1m───────────────\x1b[0m

Linking the \x1b[0;4mlabel\x1b[0m.

  def f():
      return 42

\x1b[0;1mAnother section\x1b[0m
\x1b[0;1m━━━━━━━━━━━━━━━\x1b[0m

Buh!

  Some block quote. Another line.

A line.

!⃝ This is a note. A second line!

   And a second paragraph.""",
        set(),
    ),
    (
        "images",
        r"""
This is an image:

.. image:: foo.png

.. image:: foo.png
   :alt: alt text

.. image:: foo.png
   :width: 50cm

.. image:: foo.png
   :height: 50em

.. image:: foo.png
   :alt: alt text
   :width: 50ex

------------

.. image:: foo.png
   :width: 10px
   :height: 20px
""",
        "restructuredtext",
        """This is an image:

────────────────────────────────────────────────────────────────────────────────""",
        set(),
    ),
    (
        "table",
        r"""
This is a table:

+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  |
+============+============+===========+
| body row 1 | column 2   | column 3  |
+------------+------------+-----------+
| body row 2 | Cells may span columns.|
+------------+------------+-----------+
| body row 3 | Cells may  | - Cells   |
+------------+ span rows. | - contain |
| body row 4 |            | - blocks. |
+------------+------------+-----------+
| body row 5 | One paragraph.         |
+------------+                        |
| body row 6 | Two paragraphs. กำ     |
+------------+------------+-----------+
""",
        "restructuredtext",
        """This is a table:

┌────────────┬──────────────────────┬─────────────┐
│ Header 1   │ Header 2             │ Header 3    │
╞════════════╪══════════════════════╪═════════════╡
│ body row 1 │ column 2             │ column 3    │
├────────────┼──────────────────────┴─────────────┤
│ body row 2 │ Cells may span columns.            │
├────────────┼──────────────────────┬─────────────┤
│ body row 3 │ Cells may span rows. │ - Cells     │
├────────────┤                      │ - contain   │
│ body row 4 │                      │ - blocks.   │
├────────────┼──────────────────────┴─────────────┤
│ body row 5 │ One paragraph.                     │
├────────────┤                                    │
│ body row 6 │ Two paragraphs. กำ                 │
└────────────┴────────────────────────────────────┘""",
        set(),
    ),
    (
        "title-ref",
        "`foo`",
        "restructuredtext",
        """\x1b[0;3mfoo\x1b[0m""",
        set(),
    ),
    (
        "simple-rst",
        r"""`This` *is* **a** `simple <This>`_ `test <https://example.com>`__.""",
        "restructuredtext",
        "\x1b[0;3mThis\x1b[0m \x1b[0;3mis\x1b[0m \x1b[0;1ma\x1b[0m \x1b[0;4msimple\x1b[0m (\x1b[0;4mThis\x1b[0m) \x1b[0;4mtest\x1b[0m (\x1b[0;4mhttps://example.com\x1b[0m).",
        set(),
    ),
    (
        "complex-rst",
        r"""
==========
Main title
==========

Some text.

.. sectnum::
.. contents:: Table of Contents

.. _label:
.. _label_2:

This is a subtitle
^^^^^^^^^^^^^^^^^^

Some test with ``code``.
Some *emphasis* and **bold** text.

A `link <https://ansible.com/)>`__.

A `reference <label>`_.

A list:

* Item 1.
* Item 2.

  This is still item 2.
* Item 3.
*
* Item 5 after an empty item.

An enumeration:

1. Entry 1

   More of Entry 1
2. Entry 2
3. Entry 3
   Second line of entry 3

   - Sublist
   - Another entry

     1. Subenum

        .. code:: markdown

            Some codeblock:
            ```python
            def main(argv): ...
            ```

     2. Another entry

Another subtitle
^^^^^^^^^^^^^^^^

Some code:

.. code:: python

    def main(argv):
        if argv[1] == 'help':
            print('Help!')

.. note::

  Some note.

  This note has two paragraphs.

A sub-sub-title
~~~~~~~~~~~~~~~

Something problematic: :pep:`1000000`

Some text...

  Some block quote.

    A nested block quote.

--------

Some unformatted code::

    foo bar!
    baz bam.

A sub-sub-title
~~~~~~~~~~~~~~~

The same sub-sub-title again.
""",
        "restructuredtext",
        """\x1b[0;1mMain title\x1b[0m
\x1b[0;1m══════════\x1b[0m

Some text.

\x1b[0;1mTable of Contents\x1b[0m
\x1b[0;1m━━━━━━━━━━━━━━━━━\x1b[0m

- \x1b[0;4m1\xa0\xa0\xa0This is a subtitle\x1b[0m
- \x1b[0;4m2\xa0\xa0\xa0Another subtitle\x1b[0m

  - \x1b[0;4m2.1\xa0\xa0\xa0A sub-sub-title\x1b[0m
  - \x1b[0;4m2.2\xa0\xa0\xa0A sub-sub-title\x1b[0m

\x1b[0;1m1\xa0\xa0\xa0This is a subtitle\x1b[0m
\x1b[0;1m━━━━━━━━━━━━━━━━━━━━━━\x1b[0m

Some test with `code`. Some \x1b[0;3memphasis\x1b[0m and \x1b[0;1mbold\x1b[0m text.

A \x1b[0;4mlink\x1b[0m (\x1b[0;4mhttps://ansible.com/)\x1b[0m).

A \x1b[0;4mreference\x1b[0m (\x1b[0;4mlabel\x1b[0m).

A list:

- Item 1.
- Item 2.

  This is still item 2.
- Item 3.
-
- Item 5 after an empty item.

An enumeration:

1. Entry 1

   More of Entry 1
2. Entry 2
3. Entry 3 Second line of entry 3

   - Sublist
   - Another entry

     1. Subenum

          Some codeblock:
          ```python
          def main(argv): ...
          ```
     2. Another entry

\x1b[0;1m2\xa0\xa0\xa0Another subtitle\x1b[0m
\x1b[0;1m━━━━━━━━━━━━━━━━━━━━\x1b[0m

Some code:

  def main(argv):
      if argv[1] == 'help':
          print('Help!')

!⃝ Some note.

   This note has two paragraphs.

\x1b[0;1m2.1\xa0\xa0\xa0A sub-sub-title\x1b[0m
\x1b[0;1m─────────────────────\x1b[0m

Something problematic: ⚠️ :pep:`1000000` ⚠️

\x1b[0;1m⚠️ ERROR/3 ⚠️ (<string>, line 77)\x1b[0m

  PEP number must be a number from 0 to 9999; "1000000" is invalid.

Some text...

  Some block quote.

    A nested block quote.

────────────────────────────────────────────────────────────────────────────────

Some unformatted code:

  foo bar!
  baz bam.

\x1b[0;1m2.2\xa0\xa0\xa0A sub-sub-title\x1b[0m
\x1b[0;1m─────────────────────\x1b[0m

The same sub-sub-title again.""",
        set(),
    ),
    (
        "system-messages",
        r"""
==========
Main title
==========

Some text.

.. Trigger a system message:

.. unknown-shit::

  Something.
""",
        "restructuredtext",
        """\x1b[0;1mMain title\x1b[0m
\x1b[0;1m══════════\x1b[0m

Some text.

\x1b[0;1m⚠️ ERROR/3 ⚠️ (<string>, line 10)\x1b[0m

  Unknown directive type "unknown-shit".

    .. unknown-shit::

      Something.""",
        set(),
    ),
    (
        "image",
        r"""Image:

.. image:: image.png
    :alt: An image

Image w/o alt:

.. image:: https://example.com/image.png

Image w/o alt, with size:

.. image:: https://example.com/image.png
    :width: 100px
    :height: 50px

Image with size:

.. image:: https://example.com/image.png
    :alt: An image
    :width: 150px
""",
        "restructuredtext",
        """Image:

Image w/o alt:

Image w/o alt, with size:

Image with size:""",
        set(),
    ),
    (
        "table",
        r""".. _tables:

======
Tables
======

Regular table:

+-----+-----+
| Foo | Bar |
+=====+=====+
| A   | B   |
+-----+-----+
| C   | D   |
|     | DD  |
|     |     |
|     | DDD |
+-----+-----+

A list table:

.. list-table:: The table's title
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Foo
    - Bar
  * - A
    - B
  * - C
    - D

      DD

      DDD
""",
        "restructuredtext",
        """\x1b[0;1mTables\x1b[0m
\x1b[0;1m══════\x1b[0m

Regular table:

┌─────┬──────┐
│ Foo │ Bar  │
╞═════╪══════╡
│ A   │ B    │
├─────┼──────┤
│ C   │ D DD │
│     │      │
│     │ DDD  │
└─────┴──────┘

A list table:

┌─────┬─────┐
│ Foo │ Bar │
╞═════╪═════╡
│ A   │ B   │
├─────┼─────┤
│ C   │ D   │
│     │     │
│     │ DD  │
│     │     │
│     │ DDD │
└─────┴─────┘
The table's title""",
        set(),
    ),
    (
        "subtitle",
        # TODO: what should we do with subtitles?
        r"""
========
Test doc
========

This ends up as a subtitle
--------------------------

Bar.

Test subsection
^^^^^^^^^^^^^^^

Foo.
""",
        "restructuredtext",
        """\x1b[0;1mTest doc\x1b[0m
\x1b[0;1m════════\x1b[0m

Bar.

\x1b[0;1mTest subsection\x1b[0m
\x1b[0;1m━━━━━━━━━━━━━━━\x1b[0m

Foo.""",
        {"subtitle"},
    ),
    (
        "bug-2",
        r"""
A block quote:

    Some block quote.
    Another line.

    Another paragraph.

.. note::

  This is a note.
  A second line!

  And a second paragraph.

.. note::

  And another note.

- A list item
- .. note::

    This is a note.
    A second line!

    And a second paragraph.

  .. note::

    And another note.
""",
        "restructuredtext",
        """A block quote:

  Some block quote. Another line.

  Another paragraph.

!⃝ This is a note. A second line!

   And a second paragraph.

!⃝ And another note.

- A list item
- !⃝ This is a note. A second line!

     And a second paragraph.

  !⃝ And another note.""",
        set(),
    ),
]


@pytest.mark.parametrize(
    "title, input, input_parser, expected_output, expected_unsupported_class_names",
    RENDER_AS_TEXT_AND_STRUCTURE_DATA,
    ids=[e[0] for e in RENDER_AS_TEXT_AND_STRUCTURE_DATA],
)
def test_render_as_text(
    title: str,
    input: str,
    input_parser: t.Literal["markdown", "restructuredtext"],
    expected_output: str,
    expected_unsupported_class_names: set[str],
) -> None:
    result = render_as_text(input, parser_name=input_parser)
    print(get_document_structure(input, parser_name=input_parser).output)
    print(result.output)
    print(repr(result.output))
    assert result.output == expected_output
    assert result.unsupported_class_names == expected_unsupported_class_names


def test_render_as_text_2() -> None:
    global_context = GlobalContext()
    global_context.use_ansi_formatting = "never"
    global_context.use_unicode_splitting = "never"
    input = """
=========
Foo क्षि Bar
=========

`Baz bam <https://example.com>`__.
"""
    result = render_as_text(
        input, global_context=global_context, parser_name="restructuredtext"
    )
    assert result.output == """Foo क्षि Bar
════════════

Baz bam (https://example.com)."""


def test_document_context() -> None:
    global_context = GlobalContext()
    doc_context = _DocumentContext(
        global_context=global_context, string_proc=ASCIIStringProcessor()
    )

    with pytest.raises(ValueError) as exc:
        doc_context.pop_context()
    assert str(exc.value) == "Cannot pop last element"

    previous_top = doc_context.top

    a_context = _Context(
        remaining_width=80, state=EmptyState(), string_proc=ASCIIStringProcessor()
    )
    doc_context.push_context(a_context)
    assert doc_context.top is a_context
    doc_context.pop_context()

    assert doc_context.top is previous_top


def test__get_formatting_state() -> None:
    global_context = GlobalContext()
    global_context.use_ansi_formatting = "always"
    assert isinstance(_get_formatting_state(global_context), ANSIState)
    global_context.use_ansi_formatting = "never"
    assert isinstance(_get_formatting_state(global_context), EmptyState)


def test__get_string_proc() -> None:
    global_context = GlobalContext()
    global_context.use_unicode_splitting = "always"
    assert isinstance(_get_string_proc(global_context), UnicodeStringProcessor)
    global_context.use_unicode_splitting = "never"
    assert isinstance(_get_string_proc(global_context), ASCIIStringProcessor)


def test_get_column_count() -> None:
    global_context = GlobalContext()
    global_context.use_unicode_splitting = "never"
    assert get_column_count("क्षि", global_context=global_context) == 4
    global_context.use_unicode_splitting = "always"
    assert get_column_count("क्षि", global_context=global_context) == 3


def test_render_bold() -> None:
    global_context = GlobalContext()
    global_context.use_ansi_formatting = "never"
    assert render_bold("foo", global_context=global_context) == "foo"
    global_context.use_ansi_formatting = "always"
    assert render_bold("foo", global_context=global_context) == "\x1b[0;1mfoo\x1b[0m"


def test_render_title() -> None:
    global_context = GlobalContext()
    global_context.use_ansi_formatting = "never"
    assert render_title("foo", level=1, global_context=global_context) == ["foo", "═══"]
    assert render_title("foo", level=2, global_context=global_context) == ["foo", "━━━"]
    global_context.use_ansi_formatting = "always"
    assert render_title("foo", level=1, global_context=global_context) == [
        "\x1b[0;1mfoo\x1b[0m",
        "\x1b[0;1m═══\x1b[0m",
    ]
