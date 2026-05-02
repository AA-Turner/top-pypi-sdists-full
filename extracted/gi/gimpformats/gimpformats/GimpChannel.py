"""Represents a single channel or mask in a gimp image."""

from __future__ import annotations

from PIL import Image

from gimpformats.binaryiotools import IO
from gimpformats.GimpImageHierarchy import GimpImageHierarchy
from gimpformats.GimpIOBase import GimpIOBase
from gimpformats.utils import repr_indent_lines


class GimpChannel(GimpIOBase):
	"""Represents a single channel or mask in a GIMP image."""

	def __init__(
		self, parent: GimpIOBase, name: str = "", image: Image.Image | None = None
	) -> None:
		"""Initialize a GIMP Channel instance.

		Args:
		----
			parent ([type]): some parent node/ object
			name (str, optional): name of the channel. Defaults to "".
			image (Image.Image, optional): image to set. Defaults to None.

		"""
		GimpIOBase.__init__(self, parent)
		self.width = 0
		self.height = 0
		self.name = name
		self._imageHierarchy = None
		self._imageHierarchyPtr = None
		if image is not None:  # this is last because image can reset values
			self.image = image
		self._data = None

	def decode(self, data: bytearray, index: int = 0) -> int:
		"""Decode a byte buffer.

		Args:
		----
			data (bytearray): data to decode
			index (int, optional): index to start from. Defaults to 0.

		Returns:
		-------
			int: pointer

		"""
		ioBuf = IO(data, index)
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		self.name = ioBuf.sz754
		self._propertiesDecode(ioBuf)
		self._imageHierarchyPtr = self._pointerDecode(ioBuf)
		self._data = ioBuf.data
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Encode this object to a byte buffer."""
		ioBuf = IO()
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		ioBuf.sz754 = self.name
		ioBuf.addbytearray(self._propertiesEncode())
		imgH = self._imageHierarchyPtr or 0
		ioBuf.addbytearray(self._pointerEncode(imgH))
		return ioBuf.data

	@property
	def image(self) -> Image.Image | None:
		"""Get the compiled image."""
		if self.imageHierarchy:
			return self.imageHierarchy.image
		return None

	@image.setter
	def image(self, image: Image.Image) -> None:
		"""Set the compiled image."""
		self.width, self.height = image.size
		if not self.name and isinstance(image, str):
			self.name = image.rsplit("\\", 1)[-1].rsplit("/", 1)[-1]
		self._imageHierarchy = GimpImageHierarchy(self, image)

	@property
	def imageHierarchy(self) -> GimpImageHierarchy | None:
		"""Get the image hierarchy."""
		if self._data and self._imageHierarchyPtr:
			if self._imageHierarchy is None:
				self._imageHierarchy = GimpImageHierarchy(self)
				self._imageHierarchy.decode(self._data, self._imageHierarchyPtr)
			return self._imageHierarchy
		msg = "self._data or self._imageHierarchyPtr is None"
		raise RuntimeError(msg)

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.full_repr()

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = [f"Name: {self.name}", f"Size: {self.width} x {self.height}"]
		ret.append(super().full_repr(indent))
		return repr_indent_lines(indent, ret)
