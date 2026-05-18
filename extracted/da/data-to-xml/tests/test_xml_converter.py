#############################################
#	Dual License: BSD-3-Clause AND MPL-2.0	#
#	Copyright (c) 2024, Adam Nogowski		#
#############################################

# System Imports
import xml.etree.ElementTree as ET
from typing import Any

# 3rd Party Imports
import pytest

# User Imports
from data_to_xml.xml_converter import XMLConverter


class TestMinifiedXML:
	"""Tests for the ``minified_xml`` property of ``XMLConverter``."""

	def test_simple_dict_produces_valid_xml(self) -> None:
		"""Verify that a simple dict produces parseable XML.

		Notes
		-----
		Asserts that ``ET.fromstring`` does not raise for a flat dict input.
		"""
		data: dict[str, Any] = {'name': 'Alice', 'age': '30'}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='person')
		ET.fromstring(text=converter.minified_xml)  # Should not raise

	def test_simple_dict_text_content(self) -> None:
		"""Verify that flat dict values become element text content.

		Notes
		-----
		Checks that ``<name>`` and ``<age>`` elements contain the expected text.
		"""
		data: dict[str, Any] = {'name': 'Alice', 'age': '30'}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='person')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		assert root.find(path='name').text == 'Alice'
		assert root.find(path='age').text == '30'

	def test_root_node_tag(self) -> None:
		"""Verify that ``root_node`` becomes the XML root element tag.

		Notes
		-----
		The root element tag must exactly match the ``root_node`` argument.
		"""
		data: dict[str, Any] = {'key': 'value'}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='myroot')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		assert root.tag == 'myroot'

	def test_default_root_node_is_objects(self) -> None:
		"""Verify that omitting ``root_node`` defaults to ``"objects"`` as the root tag.

		Notes
		-----
		When ``root_node=None``, the converter wraps the output in ``<objects>``.
		"""
		data: dict[str, Any] = {'key': 'value'}
		converter: XMLConverter = XMLConverter(my_dict=data)
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		assert root.tag == 'objects'

	def test_integer_values_converted_to_string(self) -> None:
		"""Verify that integer dict values are coerced to strings in element text.

		Notes
		-----
		``str()`` is called on every non-string leaf value during conversion.
		"""
		data: dict[str, Any] = {'count': 42}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		assert root.find(path='count').text == '42'

	def test_no_xml_header_by_default(self) -> None:
		"""Verify that the XML declaration is absent when ``use_xml_header=False``.

		Notes
		-----
		The default value of ``use_xml_header`` is ``False``.
		"""
		converter: XMLConverter = XMLConverter(my_dict={'key': 'val'}, root_node='root')
		assert not converter.minified_xml.startswith('<?xml')

	def test_xml_header_when_enabled(self) -> None:
		"""Verify that the XML declaration is prepended when ``use_xml_header=True``.

		Notes
		-----
		The declaration uses double-quoted attributes and includes ``standalone="yes"``.
		"""
		converter: XMLConverter = XMLConverter(my_dict={'key': 'val'}, root_node='root', use_xml_header=True)
		assert converter.minified_xml.startswith('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')

	def test_minified_has_no_newlines_or_indentation(self) -> None:
		"""Verify that the minified output contains no newline or tab characters.

		Notes
		-----
		Formatting whitespace is only present in ``formatted_xml``, not ``minified_xml``.
		"""
		data: dict[str, Any] = {'parent': {'child': 'value'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		assert '\n' not in converter.minified_xml
		assert '\t' not in converter.minified_xml


class TestAttributes:
	"""Tests for XML attribute handling via ``@``-prefixed dict keys."""

	def test_attribute_prefix(self) -> None:
		"""Verify that ``@``-prefixed keys become XML attributes on their element.

		Notes
		-----
		``@id`` → ``id="..."`` and ``@type`` → ``type="..."`` on the enclosing element.
		"""
		data: dict[str, Any] = {'item': {'@id': '1', '@type': 'foo'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		item: ET.Element | None = root.find(path='item')
		assert item is not None
		assert item.get(key='id') == '1'
		assert item.get(key='type') == 'foo'

	def test_attribute_only_produces_self_closing_tag(self) -> None:
		"""Verify that an element with only attributes uses a self-closing tag.

		Notes
		-----
		No child elements means the element serialises as ``<tag attr="..."/>``.
		"""
		data: dict[str, Any] = {'item': {'@id': '42'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		assert '/>' in converter.minified_xml

	def test_mixed_attributes_and_children(self) -> None:
		"""Verify that an element can have both attributes and child elements.

		Notes
		-----
		``@``-prefixed keys become attributes; all other keys become child elements.
		"""
		data: dict[str, Any] = {'item': {'@id': '1', 'name': 'Alice'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		item: ET.Element | None = root.find(path='item')
		assert item.get(key='id') == '1'
		assert item.find(path='name').text == 'Alice'


class TestNestedStructures:
	"""Tests for nested dict and list structures."""

	def test_nested_dict(self) -> None:
		"""Verify that a nested dict produces nested XML elements.

		Notes
		-----
		A dict value is recursively converted and wrapped in its parent key's tag.
		"""
		data: dict[str, Any] = {'parent': {'child': 'value'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		assert root.find(path='parent/child').text == 'value'

	def test_list_value_creates_repeated_elements(self) -> None:
		"""Verify that a list value produces repeated sibling elements.

		Notes
		-----
		Each list item becomes a sibling element sharing the list key's tag name.
		"""
		data: dict[str, Any] = {'items': [{'name': 'a'}, {'name': 'b'}]}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		items: list[ET.Element] = root.findall(path='items')
		assert len(items) == 2
		assert items[0].find(path='name').text == 'a'
		assert items[1].find(path='name').text == 'b'

	def test_list_with_attribute_items(self) -> None:
		"""Verify that list items with ``@``-prefixed keys produce attribute elements.

		Notes
		-----
		Each dict in the list becomes a sibling element with the expected attributes.
		"""
		data: dict[str, Any] = {'persons': [{'@name': 'Alice'}, {'@name': 'Bob'}]}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)
		persons: list[ET.Element] = root.findall(path='persons')
		assert len(persons) == 2
		assert persons[0].get(key='name') == 'Alice'
		assert persons[1].get(key='name') == 'Bob'

	def test_complex_example(self) -> None:
		"""Verify a deeply nested structure with mixed attributes and child elements.

		Notes
		-----
		Reproduces the example from ``examples/example.py`` and validates the full
		element tree including grandchild elements and their attributes.
		"""
		data: dict[str, Any] = {
		    'name': "The Andersson's",
		    'size': 4,
		    'members': {
		        'total-age': 62,
		        'child': [
		            {
		                '@name': 'Tom',
		                '@sex': 'male',
		            },
		            {
		                '@name': 'Betty',
		                '@sex': 'female',
		                'grandchild': [
		                    {
		                        '@name': 'herbert',
		                        '@sex': 'male',
		                    },
		                    {
		                        '@name': 'lisa',
		                        '@sex': 'female',
		                    },
		                ],
		            },
		        ],
		    },
		}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='family')
		root: ET.Element = ET.fromstring(text=converter.minified_xml)

		assert root.tag == 'family'
		assert root.find(path='name').text == "The Andersson's"
		assert root.find(path='size').text == '4'

		members: ET.Element | None = root.find(path='members')
		assert members is not None
		assert members.find(path='total-age').text == '62'

		children: list[ET.Element] = members.findall(path='child')
		assert len(children) == 2
		assert children[0].get(key='name') == 'Tom'
		assert children[0].get(key='sex') == 'male'
		assert children[1].get(key='name') == 'Betty'

		grandchildren: list[ET.Element] = children[1].findall(path='grandchild')
		assert len(grandchildren) == 2
		assert grandchildren[0].get(key='name') == 'herbert'
		assert grandchildren[1].get(key='name') == 'lisa'


class TestFormattedXML:
	"""Tests for the ``formatted_xml`` property of ``XMLConverter``."""

	def test_formatted_xml_has_newlines(self) -> None:
		"""Verify that the formatted output contains newline characters.

		Notes
		-----
		``ET.indent`` introduces newlines between sibling elements.
		"""
		data: dict[str, Any] = {'parent': {'child': 'value'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		assert '\n' in converter.formatted_xml

	def test_formatted_xml_has_indentation(self) -> None:
		"""Verify that the formatted output contains tab indentation.

		Notes
		-----
		``ET.indent`` is called with ``space="\\t"``.
		"""
		data: dict[str, Any] = {'parent': {'child': 'value'}}
		converter: XMLConverter = XMLConverter(my_dict=data, root_node='root')
		assert '\t' in converter.formatted_xml

	def test_formatted_xml_with_header(self) -> None:
		"""Verify that the XML declaration is prepended to ``formatted_xml`` when enabled.

		Notes
		-----
		The custom declaration is prepended before the ``ET.tostring`` output.
		"""
		converter: XMLConverter = XMLConverter(my_dict={'key': 'val'}, root_node='root', use_xml_header=True)
		assert converter.formatted_xml.startswith('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
