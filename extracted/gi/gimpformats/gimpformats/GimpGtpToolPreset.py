"""Pure python implementation of the gimp gtp tool preset format."""

from __future__ import annotations

from io import BytesIO

import brackettree

from gimpformats import utils


class ParenFileValue:
	"""A parentheses-based file format.

	(possibly "scheme" language?)
	"""

	def __init__(self, name: str | None = None, value: str = "", children=None) -> None:
		"""Parenthesis based file.

		Args:
		----
			name (str, optional): name of the file. Defaults to None.
			value (str, optional): some value, str(float) or str. Defaults to "".
			children ([type], optional): children. Defaults to None.

		"""

		self.name = name
		try:
			float(value)
			self.value = value
		except ValueError:
			self.value = '"' + value + '"'
		if value in ("yes", "no"):
			self.value = value
		self.children = children

	def _addValue(self, bufArray: str) -> None:
		if self.name is None:  # first value is the name
			self.name = bufArray
		if bufArray:
			bufArray = "".join(bufArray)
			if bufArray in ("yes", "no"):  # boolean
				self.value.append(bufArray == "yes")
			elif bufArray[0].isdigit():
				self.value.append(float(bufArray))
			elif bufArray[0] == '"':
				self.value.append(bufArray[1:-1])
			else:
				raise RuntimeError('What kind of value is "' + bufArray + '"?')

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		repr_str = f"<ParenFileValue name={self.name!r}, value={self.value!r}"
		if self.children is not None:
			repr_str += f", numChildren={len(self.children)}"
		repr_str += ">"
		return repr_str

	def full_repr(self) -> str:
		"""Get a textual representation of this object."""
		ret = []
		ret.append(f"({self.name}")
		ret.append(f" {self.value}")
		if self.children is None:
			ret.append(")")
		ret.append("\n")
		if self.children is not None:
			for index, child in enumerate(self.children):
				ret.append(f"    ({child.name}")
				ret.append(" " + child.value + ")")
				if index == len(self.children) - 1:
					ret.append(")")
				ret.append("\n")
		return "".join(ret)


def parenFileDecode(data: bytearray) -> list[ParenFileValue]:
	"""Decode a parentheses-based file format.

	(possibly "scheme" language?)
	"""
	nodes = brackettree.Node(data.decode("utf-8"))
	return walkTree(nodes.items)


def walkTree(items: list[brackettree.RoundNode]) -> list[ParenFileValue]:
	"""Walk the tree."""
	values = []
	for item in items:
		if isinstance(item, brackettree.RoundNode):
			if len(item.items) == 1:
				values.append(
					ParenFileValue(
						item.items[0].split(" ")[0].strip(), item.items[0].split(" ")[1].strip()
					)
				)
			if len(item.items) == 2:
				values.append(ParenFileValue(item.items[0].strip(), item.items[1].items[0].strip()))
			elif len(item.items) > 2:
				values.append(
					ParenFileValue(
						item.items[0].strip(),
						item.items[1].items[0].strip(),
						walkTree(item.items[2:]),
					)
				)
	return values


def parenFileEncode(values: list[ParenFileValue]) -> str:
	"""Encode a values tree to a buffer."""
	ret = []
	ret.append("# GIMP tool preset file\n\n")
	ret.append("")
	for val in values:
		if val.name is not None:
			ret.append(val.full_repr())
	ret.append("")
	ret.append("\n# end of GIMP tool preset file\n")
	ret.append("")
	return "".join(ret)


class GimpGtpToolPreset:
	"""Pure python implementation of the gimp gtp tool preset format."""

	def __init__(self, fileName: BytesIO | str | None = None) -> None:
		"""Pure python implementation of the gimp gtp tool preset format."""
		self.fileName = None
		self.values = []
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName: BytesIO | str) -> None:
		"""Load a gimp file.

		:param fileName: can be a file name or a file-like object
		"""
		self.fileName, data = utils.fileOpen(fileName)
		self.decode(data)

	def decode(self, data: bytearray | bytes, index: int = 0) -> int:
		"""Decode a byte buffer.

		:param data: data buffer to decode
		:param index: ignored
		"""
		self.values = parenFileDecode(data)
		return index

	def encode(self) -> bytes:
		"""Encode to bytearray."""
		return parenFileEncode(self.values).encode("utf-8")

	def save(self, tofileName: str | BytesIO) -> None:
		"""Save this gimp image to a file."""
		utils.save(self.encode(), tofileName)

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return f"<GimpGtpToolPreset numValues={len(self.values)}>"

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = [value.full_repr() for value in self.values]
		return utils.repr_indent_lines(indent, ret)
