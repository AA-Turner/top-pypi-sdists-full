# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test markdown module.
"""

from __future__ import annotations

import typing as t

import pytest

from antsibull_docutils.markdown import (
    Context,
    DocumentContext,
    GlobalContext,
    render_as_markdown,
)
from antsibull_docutils.utils import get_document_structure

RENDER_AS_MARKDOWN_AND_STRUCTURE_DATA: list[
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
        r"Hello world\.",
        set(),
    ),
    (
        "link",
        "`foo <bar>`__",
        "restructuredtext",
        "[foo](bar)",
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
        r"""A list\:

- an <em>entry</em>
- another <strong>one</strong>

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
        r"""An enumeration\:

1. an <code>entry</code>

   it has two lines\.

   ```
   And some code.
   ```
1. another one
1.
1. a last one""",
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
        r"""# Test doc

- [Test section](\#test\-section)

  - [Test subsection](\#test\-subsection)
- [Another section](\#another\-section)

A test document\.

<a id="label"></a>

<a id="test-section"></a>
## Test section

This is a test section\. It has a label\.

```
Code without language
```

Another code block\:

`````
````
This one has no language, either.
````
`````

<a id="test-subsection"></a>
### Test subsection

Linking the [label](\#label)\.

```python
def f():
    return 42
```

<a id="another-section"></a>
## Another section

Buh\!

> Some block quote\.
> Another line\.

A line\.

> [!NOTE]
> This is a note\.
> A second line\!
>
> And a second paragraph\.""",
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
        r"""This is an image\:

![](foo\.png)
![alt text](foo\.png)
<img src="foo.png" width="50cm">
<img src="foo.png" height="50em">
<img src="foo.png" alt="alt text" width="50ex">

---

<img src="foo.png" width="10px" height="20px">""",
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
""",
        "restructuredtext",
        r"""This is a table\:

<table>
<thead>
<tr><th class="head"><p>Header 1</p></th>
<th class="head"><p>Header 2</p></th>
<th class="head"><p>Header 3</p></th>
</tr>
</thead>
<tbody>
<tr><td><p>body row 1</p></td>
<td><p>column 2</p></td>
<td><p>column 3</p></td>
</tr>
<tr><td><p>body row 2</p></td>
<td colspan="2"><p>Cells may span columns.</p></td>
</tr>
<tr><td><p>body row 3</p></td>
<td rowspan="2"><p>Cells may
span rows.</p></td>
<td rowspan="2"><ul class="simple">
<li><p>Cells</p></li>
<li><p>contain</p></li>
<li><p>blocks.</p></li>
</ul>
</td>
</tr>
<tr><td><p>body row 4</p></td>
</tr>
</tbody>
</table>""",
        set(),
    ),
    (
        "title-ref",
        "`foo`",
        "restructuredtext",
        r"""<em class="title-reference">foo</em>""",
        set(),
    ),
    (
        "simple-rst",
        r"""`This` *is* **a** `simple <This>`_ `test <https://example.com>`__.""",
        "restructuredtext",
        r"""<em class="title-reference">This</em> <em>is</em> <strong>a</strong> [simple](This) [test](https\://example\.com)\.""",
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
        r"""# Main title

Some text\.

## Table of Contents

- [1   This is a subtitle](\#this\-is\-a\-subtitle)
- [2   Another subtitle](\#another\-subtitle)

  - [2\.1   A sub\-sub\-title](\#a\-sub\-sub\-title)
  - [2\.2   A sub\-sub\-title](\#a\-sub\-sub\-title\-1)
<a id="label"></a>
<a id="label-2"></a>

<a id="this-is-a-subtitle"></a>
## 1   This is a subtitle

Some test with <code>code</code>\.
Some <em>emphasis</em> and <strong>bold</strong> text\.

A [link](https\://ansible\.com/\))\.

A [reference](\#label)\.

A list\:

- Item 1\.
- Item 2\.

  This is still item 2\.
- Item 3\.
-
- Item 5 after an empty item\.

An enumeration\:

1. Entry 1

   More of Entry 1
1. Entry 2
1. Entry 3
   Second line of entry 3

   - Sublist
   - Another entry

     1. Subenum

        ````markdown
        Some codeblock:
        ```python
        def main(argv): ...
        ```
        ````
     1. Another entry

<a id="another-subtitle"></a>
## 2   Another subtitle

Some code\:

```python
def main(argv):
    if argv[1] == 'help':
        print('Help!')
```

> [!NOTE]
> Some note\.
>
> This note has two paragraphs\.

<a id="a-sub-sub-title"></a>
### 2\.1   A sub\-sub\-title

Something problematic\: <a href="#system-message-1"><span class="problematic">\:pep\:\`1000000\`</span></a>

<details>
<summary><strong>ERROR/3</strong> (&lt;string&gt;, line 77)</summary>

PEP number must be a number from 0 to 9999\; \"1000000\" is invalid\.

</details>

Some text\.\.\.

> Some block quote\.
>
> > A nested block quote\.

---

Some unformatted code\:

```
foo bar!
baz bam.
```

<a id="a-sub-sub-title-1"></a>
### 2\.2   A sub\-sub\-title

The same sub\-sub\-title again\.""",
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
        r"""# Main title

Some text\.

<details>
<summary><strong>ERROR/3</strong> (&lt;string&gt;, line 10)</summary>

Unknown directive type \"unknown\-shit\"\.

```
.. unknown-shit::

  Something.
```

</details>""",
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
        r"""Image\:

![An image](image\.png)

Image w/o alt\:

![](https\://example\.com/image\.png)

Image w/o alt\, with size\:

<img src="https://example.com/image.png" width="100px" height="50px">

Image with size\:

<img src="https://example.com/image.png" alt="An image" width="150px">""",
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

.. list-table::
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
        r"""# Tables

<a id="tables"></a>

Regular table\:

<table>
<thead>
<tr><th class="head"><p>Foo</p></th>
<th class="head"><p>Bar</p></th>
</tr>
</thead>
<tbody>
<tr><td><p>A</p></td>
<td><p>B</p></td>
</tr>
<tr><td><p>C</p></td>
<td><p>D
DD</p>
<p>DDD</p>
</td>
</tr>
</tbody>
</table>

A list table\:

<table style="width: 100%;">
<thead>
<tr><th class="head"><p>Foo</p></th>
<th class="head"><p>Bar</p></th>
</tr>
</thead>
<tbody>
<tr><td><p>A</p></td>
<td><p>B</p></td>
</tr>
<tr><td><p>C</p></td>
<td><p>D</p>
<p>DD</p>
<p>DDD</p>
</td>
</tr>
</tbody>
</table>""",
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
        r"""# Test doc

Bar\.

<a id="test-subsection"></a>
## Test subsection

Foo\.""",
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
        r"""A block quote\:

> Some block quote\.
> Another line\.
>
> Another paragraph\.

> [!NOTE]
> This is a note\.
> A second line\!
>
> And a second paragraph\.

> [!NOTE]
> And another note\.

- A list item
- > [!NOTE]
  > This is a note\.
  > A second line\!
  >
  > And a second paragraph\.

  > [!NOTE]
  > And another note\.""",
        set(),
    ),
]


@pytest.mark.parametrize(
    "title, input, input_parser, expected_output, expected_unsupported_class_names",
    RENDER_AS_MARKDOWN_AND_STRUCTURE_DATA,
    ids=[e[0] for e in RENDER_AS_MARKDOWN_AND_STRUCTURE_DATA],
)
def test_render_as_markdown(
    title: str,
    input: str,
    input_parser: t.Literal["markdown", "restructuredtext"],
    expected_output: str,
    expected_unsupported_class_names: set[str],
) -> None:
    result = render_as_markdown(input, parser_name=input_parser)
    print(get_document_structure(input, parser_name=input_parser).output)
    assert result.output == expected_output
    assert result.unsupported_class_names == expected_unsupported_class_names


def test_global_context() -> None:
    global_context = GlobalContext()
    assert global_context.register_new_fragment("foo") == "foo"
    assert global_context.register_new_fragment("foo") == "foo-1"
    assert global_context.register_new_fragment("foo") == "foo-2"
    code = r"""
====
Test
====

Some test.

.. _foo:
.. _foobar:

Foo
^^^

This is some text. `Foo`_.
"""
    expected = r"""# Test

Some test\.

<a id="foo-3"></a>
<a id="foobar"></a>

<a id="foo-1-1"></a>
## Foo

This is some text\. [Foo](\#foo\-3)\."""
    assert (
        render_as_markdown(
            code, global_context=global_context, parser_name="restructuredtext"
        ).output
        == expected
    )
    assert global_context.register_new_fragment("foo") == "foo-4"


def test_context() -> None:
    context = Context(has_top=False)
    with pytest.raises(ValueError) as exc:
        context.add_top("test")
    assert str(exc.value) == "Context has no top part"

    subcontext = Context(has_top=True)
    subcontext.close()
    with pytest.raises(ValueError) as exc:
        context.append(subcontext)
    assert str(exc.value) == "Context has no top part"

    context2 = Context(has_top=True)
    context2.append(subcontext)


def test_document_context() -> None:
    global_context = GlobalContext()
    doc_context = DocumentContext(global_context)

    with pytest.raises(ValueError) as exc:
        doc_context.pop_context()
    assert str(exc.value) == "Cannot pop last element"

    previous_top = doc_context.top

    a_context = Context()
    doc_context.push_context(a_context)
    assert doc_context.top is a_context
    doc_context.pop_context()

    assert doc_context.top is previous_top
