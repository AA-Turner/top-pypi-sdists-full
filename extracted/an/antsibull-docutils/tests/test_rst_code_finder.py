# Author: Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or
# https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024, Ansible Project

"""
Test rst_utils module.
"""

from __future__ import annotations

import pytest

from antsibull_docutils.rst_code_finder import CodeBlockInfo, find_code_blocks

FIND_CODE_BLOCKS: list[tuple[str, list[CodeBlockInfo]]] = [
    (
        r"""
Hello
=====

.. code-block::

  Foo
  Bar


.. code-block:: python



      Foo
        
    Bar

.. code-block::    foo  

Test

.. parsed-literal::

   # Escaped emphasis
   $ find \*foo\*

   # Not escaped emphasis
   $ find *foo*

.. does-not-exist::

""".lstrip(),
        [
            CodeBlockInfo(
                language=None,
                row_offset=5,
                col_offset=2,
                position_exact=True,
                directly_replacable_in_content=True,
                content="Foo\nBar\n",
                attributes={},
            ),
            CodeBlockInfo(
                language="python",
                row_offset=13,
                col_offset=4,
                position_exact=True,
                directly_replacable_in_content=True,
                content="  Foo\n\nBar\n",
                attributes={},
            ),
            CodeBlockInfo(
                language="foo",
                row_offset=19,
                col_offset=0,
                position_exact=False,
                directly_replacable_in_content=False,
                content="\n",
                attributes={},
            ),
        ],
    ),
    (
        r"""
+--------------------+-------------------------------+
| .. code-block::    | This is a test.               |
|                    |                               |
|    foo             | .. sourcecode:: python        |
|                    |                               |
|      bar           |    def foo(bar):              |
|                    |        return bar + 1         |
| Test               |                               |
|                    | More test!                    |
|      baz           |                               |
+--------------------+ * List item 1                 |
|                    | * List item 2 has some code   |
| Foo::              |                               |
|                    |   .. code::    c++            |
|   Bar!             |    :caption: Some test        |
|                    |                               |
| ::                 |    template<typename T>       |
|                    |    std::vector<T> create()    |
|   Baz              |    { return {}; }             |
+--------------------+-------------------------------+
| .. code:: foo      | .. code:: bar                 |
|                    |                               |
|   foo              |                               |
|                    |      foo                      |
|     !bar           |                               |
|                    |        !bar                   |
+--------------------+-------------------------------+

1. Test
2. Here is another table:

   +------------------------------+
   | .. code::                    |
   |                              |
   |   A test                     |
   +------------------------------+
   | .. code::                    |
   |   :caption: bla              |
   |                              |
   |   Another test               |
   +------------------------------+

3. Here is a CSV table:

   .. csv-table::
     :header: "Foo", "Bar"

     "A ""cell""!", ".. code::

       foo
       bar 1!"
     "Another cell", "A final one"

4. And here's a list table:

   .. list-table::
     :header-rows: 1

     * - Foo
       - Bar
     * - A "cell"!
       - .. code::

           foo
           bar 2!
     * - Another cell
       - A final one
""".lstrip(),
        [
            CodeBlockInfo(
                language=None,
                row_offset=3,
                col_offset=0,
                position_exact=False,
                directly_replacable_in_content=False,
                content="foo\n\n  bar\n",
                attributes={},
            ),
            CodeBlockInfo(
                language="python",
                row_offset=5,
                col_offset=0,
                position_exact=False,
                directly_replacable_in_content=False,
                content="def foo(bar):\n    return bar + 1\n",
                attributes={},
            ),
            CodeBlockInfo(
                language="c++",
                row_offset=15,
                col_offset=0,
                position_exact=False,
                directly_replacable_in_content=False,
                content="template<typename T>\nstd::vector<T> create()\n{ return {}; }\n",
                attributes={},
            ),
            CodeBlockInfo(
                language="foo",
                row_offset=22,
                col_offset=0,
                position_exact=False,
                directly_replacable_in_content=False,
                content="foo\n\n  !bar\n",
                attributes={},
            ),
            CodeBlockInfo(
                language="bar",
                row_offset=22,
                col_offset=0,
                position_exact=False,
                directly_replacable_in_content=False,
                content="foo\n\n  !bar\n",
                attributes={},
            ),
            CodeBlockInfo(
                language=None,
                row_offset=34,
                col_offset=3,
                position_exact=False,
                directly_replacable_in_content=False,
                content="A test\n",
                attributes={},
            ),
            CodeBlockInfo(
                language=None,
                row_offset=38,
                col_offset=3,
                position_exact=False,
                directly_replacable_in_content=False,
                content="Another test\n",
                attributes={},
            ),
            CodeBlockInfo(
                language=None,
                row_offset=49,
                col_offset=7,
                position_exact=False,
                directly_replacable_in_content=False,
                content="foo\nbar 1!\n",
                attributes={},
            ),
            CodeBlockInfo(
                language=None,
                row_offset=63,
                col_offset=11,
                position_exact=True,
                directly_replacable_in_content=True,
                content="foo\nbar 2!\n",
                attributes={},
            ),
        ],
    ),
]


@pytest.mark.parametrize("source, expected_code_block_infos", FIND_CODE_BLOCKS)
def test_rst_escape(
    source: str, expected_code_block_infos: list[CodeBlockInfo]
) -> None:
    found_code_block_infos = list(find_code_blocks(source))
    assert found_code_block_infos == expected_code_block_infos
