"""Pure python implementation of the gimp gbr brush format."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import ClassVar

import PIL.Image

from gimpformats import utils
from gimpformats.binaryiotools import IO
from gimpformats.utils import repr_indent_lines


class GimpGbrBrush:
	"""Pure python implementation of the gimp gbr brush format.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/gbr.txt
	"""

	COLOR_MODES: ClassVar[list] = [None, "L", "LA", "RGB", "RGBA"]  # only L or RGB allowed

	def __init__(self, fileName: str | None = None) -> None:
		"""Pure python implementation of the gimp gbr brush format.

		Args:
		----
			fileName (str, optional): filename for the brush. Defaults to None.

		"""
		self.fileName = None
		self.version = 2
		self.width = 0
		self.height = 0
		self.bpp = 1
		self.mode = self.COLOR_MODES[self.bpp]
		self.name = ""
		self.rawImage = None
		self.spacing = 0
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

		Raises:
		------
			RuntimeError: "unknown brush version"
			RuntimeError: "File format error.  Magic value mismatch"

		Returns:
		-------
			int: offset]

		"""
		ioBuf = IO(data, index)
		headerSize = ioBuf.u32
		self.version = ioBuf.u32
		if self.version != 2:
			msg = f"ERR: unknown brush version {self.version}"
			raise RuntimeError(msg)
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		self.bpp = ioBuf.u32  # only allows grayscale or RGB
		self.mode = self.COLOR_MODES[self.bpp]
		magic = ioBuf.getbytearray(4)
		if magic.decode("ascii") != "GIMP":
			raise RuntimeError(
				'"'
				+ magic.decode("ascii")
				+ '" '
				+ str(index)
				+ " File format error.  Magic value mismatch."
			)
		self.spacing = ioBuf.u32
		nameLen = headerSize - ioBuf.index
		self.name = ioBuf.getbytearray(nameLen).decode("UTF-8")
		self.rawImage = ioBuf.getbytearray(self.width * self.height * self.bpp)
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Encode this object to byte array."""
		ioBuf = IO()
		ioBuf.u32 = 28 + len(self.name)
		ioBuf.u32 = self.version
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		ioBuf.u32 = self.bpp
		ioBuf.addbytearray("GIMP")
		ioBuf.u32 = self.spacing
		ioBuf.addbytearray(self.name)
		ioBuf.addbytearray(self.rawImage)
		return ioBuf.data

	@property
	def size(self) -> tuple[int, int]:
		"""Get the size."""
		return (self.width, self.height)

	@property
	def image(self) -> PIL.Image.Image | None:
		"""Get a final, compiled image."""
		if self.rawImage is None:
			return None
		return PIL.Image.frombytes(self.mode, self.size, self.rawImage, decoder_name="raw")

	def save(self, filename: str, extension: str | None = None) -> None:
		"""
		Save this GIMP image to a file.

		Args:
		----
			filename (str): The name of the file to save.
			extension (str, optional): The extension of the file. If not provided,
				it will be inferred from the filename.

		"""
		# Infer extension from filename if not provided
		if extension is None:
			extension = Path(filename).suffix if filename else None

		# Save as image if extension is provided and not "gbr"
		if extension and extension != ".gbr" and self.image:
			self.image.save(filename)
			self.image.close()
		else:
			# Save data directly if not an image or no image available
			Path(filename).write_bytes(self.encode())

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.full_repr()

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = []
		if self.fileName is not None:
			ret.append(f"fileName: {self.fileName}")
		ret.append(f"Name: {self.name}")
		ret.append(f"Version: {self.version}")
		ret.append(f"Size: {self.width} x {self.height}")
		ret.append(f"Spacing: {self.spacing}")
		ret.append(f"BPP: {self.bpp}")
		ret.append(f"Mode: {self.mode}")
		return repr_indent_lines(indent, ret)
