import pytest

from agentql import ContainerListNode, ContainerNode, IdListNode, IdNode, QueryParser

# pylint: disable=missing-function-docstring

TO_STRING_TEST_DATA = [
    """{
  sign_in_btn
  container {
    child1
  }
  container_list[] {
    child2
    child3
  }
  id_list[]
}""",
    """{
  sign_in_btn(good)
  container {
    child1
  }
  container_list[] {
    child2(pasha)[] {
      pasha
    }
    child3(bad)
  }
  id_list(i hate lists)[]
}""",
]


@pytest.mark.parametrize("query", TO_STRING_TEST_DATA)
def test_to_str(query):
    node = QueryParser(query).parse()
    assert str(node) == query


PARSE_TEST_DATA = [
    (
        # Id Node without description
        "{sign_in_btn}",
        ContainerNode(name="", description=None, children=[IdNode(name="sign_in_btn", description=None)]),
    ),
    (
        # Id Node with missing description
        "{sign_in_btn}",
        ContainerNode(name="", children=[IdNode(name="sign_in_btn")]),
    ),
    (
        # Id Node with description
        "{sign_in_btn(a (good) button)}",
        ContainerNode(
            name="",
            description=None,
            children=[IdNode(name="sign_in_btn", description="a (good) button")],
        ),
    ),
    (
        # Container Node without description
        """
        {
            container {
                sign_in_btn
            }
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                ContainerNode(
                    name="container",
                    description=None,
                    children=[IdNode(name="sign_in_btn", description=None)],
                )
            ],
        ),
    ),
    (
        # Container Node with description
        """
        {
            container(a very good container) {
                sign_in_btn
            }
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                ContainerNode(
                    name="container",
                    description="a very good container",
                    children=[IdNode(name="sign_in_btn", description=None)],
                )
            ],
        ),
    ),
    (
        # IdList Node without description
        "{sign_in_btn[]}",
        ContainerNode(name="", description=None, children=[IdListNode(name="sign_in_btn", description=None)]),
    ),
    (
        # IdList Node with description
        "{sign_in_btn(good buttons)[]}",
        ContainerNode(
            name="",
            description=None,
            children=[IdListNode(name="sign_in_btn", description="good buttons")],
        ),
    ),
    (
        # ContainerList Node without description
        """
        {
            container[] {
                sign_in_btn
            }
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                ContainerListNode(
                    name="container",
                    description=None,
                    children=[IdNode(name="sign_in_btn", description=None)],
                )
            ],
        ),
    ),
    (
        # ContainerList Node with description
        """
        {
            container(a very good container)[] {
                sign_in_btn
            }
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                ContainerListNode(
                    name="container",
                    description="a very good container",
                    children=[IdNode(name="sign_in_btn", description=None)],
                )
            ],
        ),
    ),
    (
        # Complex query
        """
        {
            sign_in_btn
            container {
                child1(a good child) {
                    child(bad)
                }
            }
            container_list[] {
                child2
                child3(i (love children))
            }
            id_list[]
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdNode(name="sign_in_btn", description=None),
                ContainerNode(
                    name="container",
                    description=None,
                    children=[
                        ContainerNode(
                            name="child1",
                            description="a good child",
                            children=[IdNode(name="child", description="bad")],
                        )
                    ],
                ),
                ContainerListNode(
                    name="container_list",
                    description=None,
                    children=[
                        IdNode(name="child2", description=None),
                        IdNode(name="child3", description="i (love children)"),
                    ],
                ),
                IdListNode(name="id_list", description=None),
            ],
        ),
    ),
    (
        # Complex query without specifying description for some nodes
        """
        {
            sign_in_btn
            container {
                child1(a good child) {
                    child(bad)
                }
            }
            container_list[] {
                child2
                child3(i (love children))
            }
            id_list[]
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdNode(name="sign_in_btn"),
                ContainerNode(
                    name="container",
                    description=None,
                    children=[
                        ContainerNode(
                            name="child1",
                            description="a good child",
                            children=[IdNode(name="child", description="bad")],
                        )
                    ],
                ),
                ContainerListNode(
                    name="container_list",
                    children=[
                        IdNode(name="child2", description=None),
                        IdNode(name="child3", description="i (love children)"),
                    ],
                ),
                IdListNode(name="id_list", description=None),
            ],
        ),
    ),
    (
        # Complex query with weird quotes and apostrophes
        """
        {
            sign_in_btn
            container() {
                child1("a good child") {
                    child(bad)
                }
            }
            container_list[] {
                child2
                child3(i ('love c"hildren'))
            }
            id_list('good")[]
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdNode(name="sign_in_btn", description=None),
                ContainerNode(
                    name="container",
                    description="",
                    children=[
                        ContainerNode(
                            name="child1",
                            description="a good child",
                            children=[IdNode(name="child", description="bad")],
                        )
                    ],
                ),
                ContainerListNode(
                    name="container_list",
                    description=None,
                    children=[
                        IdNode(name="child2", description=None),
                        IdNode(name="child3", description="i ('love c\"hildren')"),
                    ],
                ),
                IdListNode(name="id_list", description="'good\""),
            ],
        ),
    ),
    (
        # Comma after the last child
        """
        {
            search_btn,
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[IdNode(name="search_btn", description=None)],
        ),
    ),
    (
        # Comma after the last child with description
        """
        {
            search_btn (description),
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[IdNode(name="search_btn", description="description")],
        ),
    ),
    (
        # Comma after last containerList
        """
        {
            products[],
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[IdListNode(name="products", description=None)],
        ),
    ),
    (
        # Comma after last containerNode
        """
        {
            header {
                about
            },
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                ContainerNode(
                    name="header",
                    description=None,
                    children=[IdNode(name="about", description=None)],
                )
            ],
        ),
    ),
    (
        # Comma between items
        """
        {
            header,
            about
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdNode(name="header", description=None),
                IdNode(name="about", description=None),
            ],
        ),
    ),
    (
        # Comma between items with no new line character
        """
        {
            header (top of the page),about
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdNode(name="header", description="top of the page"),
                IdNode(name="about", description=None),
            ],
        ),
    ),
    (
        # Comma between containerList and IdNode
        """
        {
            products[],
            footer
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdListNode(name="products", description=None),
                IdNode(name="footer", description=None),
            ],
        ),
    ),
    (
        # Comma between containerList and IdNode with description
        """
        {
            products(description)[] ,
            footer
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                IdListNode(name="products", description="description"),
                IdNode(name="footer", description=None),
            ],
        ),
    ),
    (
        # Comma between containerList and IdNode with description
        """
        {
            products[] {
                name,price
            } ,
            footer
        }
        """,
        ContainerNode(
            name="",
            description=None,
            children=[
                ContainerListNode(
                    name="products",
                    description=None,
                    children=[
                        IdNode(name="name", description=None),
                        IdNode(name="price", description=None),
                    ],
                ),
                IdNode(name="footer", description=None),
            ],
        ),
    ),
]


@pytest.mark.parametrize("query, expected", PARSE_TEST_DATA)
def test_parse(query, expected):
    node = QueryParser(query).parse()
    assert expected == node


QUERY_NAME_TEST_DATA = [
    ("{id_list[]}", "id_list[]"),
    ("{container_list[]}", "container_list[]"),
    ("{container { child }}", "container"),
    ("{id_node}", "id_node"),
    ("{id_node(with description)}", "id_node(with description)"),
    ("{id_list(with description)[]}", "id_list(with description)[]"),
    ("{container_list(with description)[]{ child }}", "container_list(with description)[]"),
    ("{container(with description){ child }}", "container(with description)"),
]


@pytest.mark.parametrize("query, expected", QUERY_NAME_TEST_DATA)
def test_query_name(query, expected):
    node = QueryParser(query).parse()
    assert node.children[0].query_name == expected
