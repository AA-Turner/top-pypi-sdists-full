from typing import Any, Literal
import xml.etree.ElementTree as ET


class XMLConverter:
	"""Converts a Python dictionary or list to an XML string.

	Parameters
	----------
	my_dict : dict[str, Any]
		The data structure to convert to XML.
	root_node : str or None, optional
		The tag name for the root XML element. If ``None``, defaults to
		``"objects"`` and list items use the singular form (trailing ``s``
		stripped). Default is ``None``.
	use_xml_header : bool, optional
		When ``True``, prepends the XML declaration
		``<?xml version="1.0" encoding="UTF-8" standalone="yes"?>`` to
		both output strings. Default is ``False``.

	Examples
	--------
	>>> from data_to_xml.xml_converter import XMLConverter
	>>> converter = XMLConverter(my_dict={'name': 'Alice'}, root_node='person')
	>>> converter.minified_xml
	'<person><name>Alice</name></person>'
	"""

	def __init__(
	    self,
	    my_dict: dict[str, Any],
	    root_node: str | None = None,
	    use_xml_header: bool = False,
	) -> None:
		xml_heading: str = ''
		if use_xml_header:
			xml_heading: str = r'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
		self._minified_xml: str = xml_heading + self.data_to_xml(my_dict=my_dict, root_node=root_node)

		# write_xml_file(xml=self._minified_xml) # For debugging

		element: ET.Element = ET.XML(text=self._minified_xml)
		ET.indent(tree=element, space="\t")

		self._formatted_xml: str = xml_heading + "\n" + ET.tostring(element=element, encoding="UTF-8").decode(encoding="UTF-8")

	@property
	def minified_xml(self) -> str:
		"""str : The XML string with no whitespace formatting or newlines."""
		return self._minified_xml

	@property
	def formatted_xml(self) -> str:
		"""str : The XML string with tab indentation and newlines."""
		return self._formatted_xml

	def data_to_xml(
	    self,
	    my_dict: dict[str, Any] | list[Any],
	    root_node: str | None = None,
	) -> str:
		"""Recursively convert a dict or list to an XML string.

		Dictionary keys prefixed with ``@`` are treated as XML attributes on
		the enclosing element rather than child elements.

		Parameters
		----------
		my_dict : dict[str, Any] or list[Any]
			The data to convert. Dicts produce element trees; lists produce
			repeated sibling elements named after ``root_node``.
		root_node : str or None, optional
			The tag name to wrap this node in. When ``None`` the root tag
			defaults to ``"objects"`` and list items use the singular form
			(trailing ``s`` stripped). Default is ``None``.

		Returns
		-------
		str
			The XML fragment string for this node and all its descendants.

		Examples
		--------
		>>> converter = XMLConverter.__new__(XMLConverter)
		>>> converter.data_to_xml({'age': 30}, root_node='person')
		'<person><age>30</age></person>'
		"""
		wrap: bool = False if None == root_node or isinstance(my_dict, list) else True
		root: None | Any | Literal['objects'] = "objects" if None == root_node else root_node
		root_singular: Any | str | None = root[:-1] if 's' == root[-1] and None == root_node else root
		xml: str = ''
		attr: str = ''
		children: list[Any] = []

		# print(f"\n{my_dict}\n") # For debugging

		if isinstance(my_dict, dict):
			for key, value in my_dict.items():
				if key[0] == '@':
					attr = f'{attr} {key[1::]} ="{str(object=value)}"'
				elif isinstance(value, dict):
					children.append(self.data_to_xml(my_dict=value, root_node=key))
				elif isinstance(value, list):
					children.append(self.data_to_xml(my_dict=value, root_node=key))
				else:
					xml = f'<{key}>{str(object=value)}</{key}>'
					children.append(xml)

		if isinstance(my_dict, list):
			for value in my_dict:
				children.append(self.data_to_xml(my_dict=value, root_node=root_singular))

		end_tag: Literal['>'] | Literal['/>'] = '>' if 0 < len(children) else '/>'

		if wrap or isinstance(my_dict, dict):
			xml = f'<{root}{attr}{end_tag}'

		if 0 < len(children):
			for child in children:
				xml = xml + child

			if wrap or isinstance(my_dict, dict):
				xml = f'{xml}</{root}>'

		return xml


def write_xml_file(xml: str, f_name: str = "min.xml") -> None:
	"""Write an XML string to a file.

	Parameters
	----------
	xml : str
		The XML string to write.
	f_name : str, optional
		Destination file path. Default is ``"min.xml"``.
	"""
	with open(file=f_name, mode="w+") as f:
		f.write(xml)
