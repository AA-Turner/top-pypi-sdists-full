from dataclasses import make_dataclass
from typing import Any
from unittest import mock
from unittest.case import TestCase

from tests.fixtures.books import BookForm, Books
from tests.fixtures.models import TypeA
from xsdata.exceptions import ParserError
from xsdata.formats.dataclass.models.elements import XmlType
from xsdata.formats.dataclass.models.generics import DerivedElement
from xsdata.formats.dataclass.parsers.bases import NodeParser
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.parsers.mixins import XmlHandler
from xsdata.formats.dataclass.parsers.nodes.primitive import PrimitiveNode
from xsdata.formats.dataclass.parsers.nodes.skip import SkipNode
from xsdata.models.enums import Namespace, QNames
from xsdata.utils.testing import XmlVarFactory


class NodeParserTests(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.parser = NodeParser()

    def test_parse(self) -> None:
        class TestHandler(XmlHandler):
            def parse(self, source: Any, ns_map: dict) -> Any:
                return Books()

        self.parser.handler = TestHandler
        self.assertEqual(Books(), self.parser.parse([], Books, {}))

    def test_parse_when_result_type_is_wrong(self) -> None:
        parser = self.parser
        with self.assertRaises(ParserError) as cm:
            parser.parse([], Books)

        self.assertEqual("Failed to create target class `Books`", str(cm.exception))

    def test_parse_with_fail_on_converter_warnings(self) -> None:
        parser = NodeParser(handler=XmlEventHandler)
        parser.config.fail_on_converter_warnings = True

        xml = """<TypeA>foo</TypeA>"""
        with self.assertRaises(ParserError) as cm:
            parser.from_string(xml, TypeA)

        self.assertEqual(
            "Failed to convert value for `TypeA.x`\n  `foo` is not a valid `int`",
            str(cm.exception),
        )

    def test_start(self) -> None:
        queue = []
        objects = []

        attrs = {"k": "v"}
        ns_map = {"a": "b"}
        self.parser.start(Books, queue, objects, "{urn:books}books", attrs, ns_map)
        actual = queue[0]

        self.assertEqual(1, len(queue))
        self.assertEqual(0, actual.position)
        self.assertEqual(self.parser.context, actual.context)
        self.assertEqual(self.parser.context.build(Books), actual.meta)
        self.assertEqual(self.parser.config, actual.config)
        self.assertEqual(attrs, actual.attrs)
        self.assertEqual(ns_map, actual.ns_map)
        self.assertFalse(actual.mixed)
        self.assertIsNone(actual.derived_factory)
        self.assertIsNone(actual.xsi_type)

        self.parser.start(Books, queue, objects, "book", {}, {})
        actual = queue[1]

        self.assertEqual(2, len(queue))
        self.assertEqual(0, actual.position)
        self.assertEqual(self.parser.context, actual.context)
        self.assertEqual(self.parser.context.build(BookForm), actual.meta)
        self.assertEqual(self.parser.config, actual.config)
        self.assertEqual({}, actual.attrs)
        self.assertEqual({}, actual.ns_map)
        self.assertFalse(actual.mixed)
        self.assertIsNone(actual.derived_factory)
        self.assertIsNone(actual.xsi_type)

    def test_start_with_undefined_class(self) -> None:
        parser = self.parser
        queue = []
        objects = []

        attrs = {"k": "v"}
        ns_map = {"a": "b"}
        parser.start(None, queue, objects, "{urn:books}books", attrs, ns_map)
        actual = queue[0]

        self.assertEqual(1, len(queue))
        self.assertEqual(0, actual.position)
        self.assertEqual(self.parser.context, actual.context)
        self.assertEqual(self.parser.context.build(Books), actual.meta)
        self.assertEqual(self.parser.config, actual.config)
        self.assertEqual(attrs, actual.attrs)
        self.assertEqual(ns_map, actual.ns_map)
        self.assertFalse(actual.mixed)
        self.assertIsNone(actual.derived_factory)
        self.assertIsNone(actual.xsi_type)

        with self.assertRaises(ParserError) as cm:
            parser.start(None, [], [], "{unknown}hopefully", {}, {})

        self.assertEqual(
            "No class found matching root: {unknown}hopefully", str(cm.exception)
        )

    def test_start_with_any_type_root(self) -> None:
        parser = self.parser
        queue = []
        objects = []

        attrs = {QNames.XSI_TYPE: "bk:books"}
        ns_map = {"bk": "urn:books", "xsi": Namespace.XSI.uri}
        parser.start(None, queue, objects, "whatever", attrs, ns_map)
        actual = queue[0]

        self.assertEqual(1, len(queue))
        self.assertEqual(0, actual.position)
        self.assertEqual(self.parser.context, actual.context)
        self.assertEqual(self.parser.context.build(Books), actual.meta)
        self.assertEqual(self.parser.config, actual.config)
        self.assertEqual(attrs, actual.attrs)
        self.assertEqual(ns_map, actual.ns_map)
        self.assertFalse(actual.mixed)
        self.assertEqual(DerivedElement, actual.derived_factory)
        self.assertEqual("{urn:books}books", actual.xsi_type)

    def test_start_with_derived_class(self) -> None:
        a = make_dataclass("a", fields=[])
        b = make_dataclass("b", fields=[], bases=(a,))

        parser = NodeParser()
        queue = []
        objects = []

        attrs = {QNames.XSI_TYPE: "b"}
        ns_map = {}
        parser.start(a, queue, objects, "a", attrs, ns_map)

        actual = queue[0]

        self.assertEqual(1, len(queue))
        self.assertEqual(0, actual.position)
        self.assertEqual(parser.context, actual.context)
        self.assertEqual(parser.context.build(b), actual.meta)
        self.assertEqual(parser.config, actual.config)
        self.assertEqual(attrs, actual.attrs)
        self.assertEqual({}, actual.ns_map)
        self.assertFalse(actual.mixed)
        self.assertEqual(DerivedElement, actual.derived_factory)
        self.assertEqual("b", actual.xsi_type)

    def test_start_with_nillable_element(self) -> None:
        a = make_dataclass("a", fields=[])

        parser = NodeParser()
        queue = []
        objects = []

        attrs = {QNames.XSI_NIL: "true"}
        ns_map = {}
        parser.start(a, queue, objects, "a", attrs, ns_map)

        actual = queue[0]

        self.assertEqual(1, len(queue))
        self.assertEqual(0, actual.position)
        self.assertTrue("b", actual.xsi_nil)

    @mock.patch.object(PrimitiveNode, "bind", return_value=True)
    def test_end(self, mock_assemble) -> None:
        parser = NodeParser()
        objects = [("q", "result")]
        queue = []
        var = XmlVarFactory.create(xml_type=XmlType.TEXT, name="foo")
        queue.append(PrimitiveNode(var, {}, False, parser.config))

        self.assertTrue(parser.end(queue, objects, "author", "foobar", None))
        self.assertEqual(0, len(queue))
        self.assertEqual(("q", "result"), objects[-1])
        mock_assemble.assert_called_once_with("author", "foobar", None, objects)

    def test_end_with_no_result(self) -> None:
        parser = NodeParser()
        objects = [("q", "result")]
        queue = [SkipNode()]

        self.assertFalse(parser.end(queue, objects, "author", "foobar", None))
        self.assertEqual(0, len(queue))

    def test_register_namespace(self) -> None:
        parser = NodeParser()
        ns_map = {}
        parser.register_namespace(ns_map, "bar", "foo")
        parser.register_namespace(ns_map, "bar", "exists")
        self.assertEqual({"bar": "foo"}, ns_map)

        parser.register_namespace(ns_map, None, "a")
        self.assertEqual({"bar": "foo", None: "a"}, ns_map)

        parser.register_namespace(ns_map, None, "b")
        self.assertEqual({"bar": "foo", None: "a"}, ns_map)
