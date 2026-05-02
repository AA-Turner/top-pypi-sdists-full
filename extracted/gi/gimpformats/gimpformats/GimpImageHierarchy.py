"""Gets packed pixels from a gimp image.

NOTE: This was originally designed to be a hierarchy, like
	an image pyramid, through in practice they only use the
	top level of the pyramid (64x64) and ignore the rest.
"""

from __future__ import annotations

from PIL import Image

from gimpformats.GimpImageLevel import GimpImageLevel
from gimpformats.GimpIOBase import IO, GimpIOBase


class GimpImageHierarchy(GimpIOBase):
	"""
	Represents packed pixels from a GIMP image hierarchy.

	NOTE: Originally designed as a hierarchy, but currently only the top level (64x64) is used.
	"""

	def __init__(self, parent, image: Image.Image | None = None) -> None:
		super().__init__(parent)
		self.width: int = 0
		self.height: int = 0
		self.bpp: int = 0  # Number of bytearray per pixel
		self._levelPtrs = []
		self._levels = None
		self._data = None
		if image is not None:
			self.image = image

	def decode(self, data: bytearray, index: int = 0) -> int:
		"""
		Decode packed pixels from a byte buffer.
		"""
		if not data:
			msg = "No data provided for decoding."
			raise RuntimeError(msg)

		ioBuf = IO(data, index)
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		self.bpp = ioBuf.u32

		if not (1 <= self.bpp <= 4):
			msg = f"Unexpected bytearray-per-pixel value: {self.bpp}. Possible file corruption."
			raise RuntimeError(msg)

		while True:
			ptr = self._pointerDecode(ioBuf)
			if ptr == 0:
				break
			self._levelPtrs.append(ptr)

		if self._levelPtrs:
			self._levelPtrs = [self._levelPtrs[0]]
		self._data = data
		return ioBuf.index

	def encode(self) -> bytearray:
		"""
		Encode packed pixels data into a byte buffer.
		"""
		dataioBuf = IO()
		ioBuf = IO()
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		ioBuf.u32 = self.bpp
		dataIndex = ioBuf.index + self.pointerSize * (len(self.levels) + 1)
		for level in self.levels:
			ioBuf.addbytearray(self._pointerEncode(dataIndex + dataioBuf.index))
			dataioBuf.addbytearray(level.encode())
		ioBuf.addbytearray(self._pointerEncode(0))
		ioBuf.addbytearray(dataioBuf.data)
		return ioBuf.data

	@property
	def levels(self) -> list[GimpImageLevel]:
		"""Get the levels within this hierarchy.

		Presently hierarchy is not really used by gimp,
		so this returns an array of one item
		"""
		if self._levels is None:
			for ptr in self._levelPtrs or []:
				level = GimpImageLevel(self)
				level.decode(self._data, ptr)
				self._levels = [level]
		return self._levels or []

	@property
	def image(self) -> Image.Image | None:
		"""Get a final, compiled image."""
		return self.levels[0].image if self.levels else None

	@image.setter
	def image(self, image: Image.Image) -> None:
		"""Set the image."""
		self.width, self.height = image.size
		if image.mode not in ["L", "LA", "RGB", "RGBA"]:
			msg = "Unsupported PIL image type."
			raise NotImplementedError(msg)
		self.bpp = len(image.mode)
		self._levelPtrs = None

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return f"<GimpImageHierarchy size={self.width}x{self.height}, bpp={self.bpp}>"
