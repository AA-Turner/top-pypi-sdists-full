from typing import Any, Literal
import xml.etree.ElementTree as ET


class XMLConverter:

	def __init__(self, my_dict: dict, root_node: str | None = None, use_xml_header: bool = False) -> None:
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
		return self._minified_xml

	@property
	def formatted_xml(self) -> str:
		return self._formatted_xml

	def data_to_xml(self, my_dict: dict | list, root_node: str | None = None) -> str:
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
	"""Serialize xml

	Args:
		xml (str): xml string to serialize
		f_name (str, optional): file name. Defaults to "min.xml".
	"""
	with open(file=f_name, mode="w+") as f:
		f.write(xml)
