"""Gimp Image Pipe Format.

The gih format is use to store a series of brushes, and some extra info
for how to use them.
"""

from __future__ import annotations

from io import BytesIO

from gimpformats import utils
from gimpformats.binaryiotools import IO
from gimpformats.GimpGbrBrush import GimpGbrBrush
from gimpformats.utils import repr_indent_lines


class GimpGihBrushSet:
	"""Gimp Image Pipe Format.

	The gih format is use to store a series of brushes, and some extra info
	for how to use them.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/gih.txt
	"""

	def __init__(self, fileName: str | None = None) -> None:
		"""Gimp Image Pipe Format.

		Args:
		----
			fileName (str, optional): filename. Defaults to None.

		"""
		self.fileName = None
		self.name = ""
		self.params = {}
		self.brushes = []
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

		Args:
		----
			data (bytearray): data buffer to decode
			index (int, optional): index within the buffer to start at. Defaults to 0.

		Returns:
		-------
			int: offset

		"""
		ioBuf = IO(data, index)
		self.name = ioBuf.textLine
		secondLine = ioBuf.textLine.split(" ")
		self.params = {}
		numBrushes = int(secondLine[0])
		# everything that's left is a gimp-image-pipe-parameters parasite
		for i in range(1, len(secondLine)):
			param = secondLine[i].split(":", 1)
			self.params[param[0].strip()] = param[1].strip()
		self.brushes = []
		for _ in range(numBrushes):
			brush = GimpGbrBrush()
			ioBuf.index = brush.decode(
				ioBuf.data, ioBuf.index
			)  # TODO: broken.  For some reason there is extra data between brushes!
			self.brushes.append(brush)
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Encode this object to bytearray."""
		ioBuf = IO()
		ioBuf.textLine = self.name
		# add the second line of data
		secondLine = [str(len(self.brushes))]
		for key, value in self.params.items():
			secondLine.append(f"{key}:{value}")
		ioBuf.textLine = " ".join(secondLine)
		# add the brushes
		for brush in self.brushes:
			ioBuf.addbytearray(brush.encode())
		return ioBuf.data

	def save(self, tofileName: str) -> None:
		"""Save this gimp image to a file."""
		utils.save(self.encode(), tofileName)

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.full_repr()

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = []
		if self.fileName is not None:
			ret.append(f"fileName: {self.fileName}")
		ret.append(f"Name: {self.name}")
		for k, val in list(self.params.items()):
			ret.append(k + f": {val}")
		for i, brush in enumerate(self.brushes):
			ret.append(f"Brush {i}")
			ret.append(brush.full_repr(indent=indent + 1))
		return repr_indent_lines(indent, ret)
