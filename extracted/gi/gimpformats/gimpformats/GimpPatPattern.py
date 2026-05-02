"""Pure python implementation of a gimp pattern file."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image

from gimpformats import utils
from gimpformats.binaryiotools import IO


class GimpPatPattern:
	"""Pure python implementation of a gimp pattern file.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/pat.txt
	"""

	COLOR_MODES = [None, "L", "LA", "RGB", "RGBA"]

	def __init__(self, fileName: BytesIO | str | None = None) -> None:
		"""Pure python implementation of a gimp pattern file.

		Args:
		----
			fileName (BytesIO, optional): filename or pointer. Defaults to None.

		"""
		self.fileName = None
		self.version = 1
		self.width = 0
		self.height = 0
		self.bpp = 4
		self.mode = self.COLOR_MODES[self.bpp]
		self.name = ""
		self._rawImage = None
		self._image = None
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName: BytesIO | str | Path) -> None:
		"""Load a gimp file.

		:param fileName: can be a file name or a file-like object
		"""
		self.fileName, data = utils.fileOpen(fileName)
		self.decode(data)

	def decode(self, data: bytearray | bytes, index: int = 0) -> int:
		"""Decode a byte buffer.

		Args:
		----
			data (bytearray): data to decode
			index (int, optional): index to start from. Defaults to 0.

		Raises:
		------
			RuntimeError: "File format error.  Magic value mismatch."

		Returns:
		-------
			int: pointer

		"""
		ioBuf = IO(data, index)
		headerSize = ioBuf.u32
		self.version = ioBuf.u32
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		self.bpp = ioBuf.u32
		self.mode = self.COLOR_MODES[self.bpp]
		magic = ioBuf.getbytearray(4)
		if magic.decode("ascii") != "GPAT":
			msg = "File format error.  Magic value mismatch."
			raise RuntimeError(msg)
		nameLen = headerSize - ioBuf.index
		self.name = ioBuf.getbytearray(nameLen).decode("UTF-8")
		self._rawImage = ioBuf.getbytearray(self.width * self.height * self.bpp)
		self._image = None
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Encode to a byte buffer."""
		ioBuf = IO()
		ioBuf.u32 = 24 + len(self.name)
		ioBuf.u32 = self.version
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		ioBuf.u32 = len(self.image.mode)
		ioBuf.addbytearray("GPAT")
		ioBuf.addbytearray(self.name.encode("utf-8"))
		if self._rawImage is None and self.image:
			rawImage = self.image.tobytes(encoder_name="raw")
		else:
			rawImage = self._rawImage
		ioBuf.addbytearray(rawImage)
		return ioBuf.data

	@property
	def size(self) -> tuple[int, int]:
		"""The size of the pattern."""
		return (self.width, self.height)

	@property
	def image(self) -> Image.Image | None:
		"""Get a final, compiled image."""
		if self._image is None:
			if self._rawImage is None:
				return None
			self._image = Image.frombytes(self.mode, self.size, self._rawImage, decoder_name="raw")
		return self._image

	@image.setter
	def image(self, image: Image.Image) -> None:
		self._image = image
		self._rawImage = None

	def save(self, tofileName: Path | str | BytesIO, toExtension: str | None = None) -> None:
		"""Save this gimp image to a file."""

		asImage = False

		if toExtension is None:
			toExtension = Path(str(tofileName)).suffix or None

		if toExtension and toExtension != ".pat":
			asImage = True

		if asImage and self.image is not None:
			self.image.save(tofileName)
		else:
			utils.save(self.encode(), tofileName)

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return (
			f"<GimpPatPattern name={self.name!r}, version={self.version}, "
			f"size={self.width}x{self.height}, "
			f"bpp={self.bpp}, mode={self.mode}"
			f"{', fileName=' + repr(self.fileName) if self.fileName is not None else ''}>"
		)
