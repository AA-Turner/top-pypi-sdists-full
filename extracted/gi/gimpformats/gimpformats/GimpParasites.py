"""Parasites are arbitrary (meta)data strings that can be attached to a document tree item.

They are used to store things like last-used plugin settings, gamma adjuetments, etc.

Format of known parasites:
	https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/parasites.txt
"""

from __future__ import annotations

from gimpformats.binaryiotools import IO

# TODO: how to best use these for our puproses??
KNOWN_DOCUMENT_PARASITES = [
	"jpeg-save-defaults",
	"png-save-defaults",
	"<plug-in>/_fu_data",
	"exif-orientation-rotate",
]
KNOWN_IMAGE_PARASITES = [
	"gimp-comment",
	"gimp-brush-name",
	"gimp-brush-pipe-name",
	"gimp-brush-pipe-parameters",
	"gimp-image-grid",
	"gimp-pattern-name",
	"tiff-save-options",
	"jpeg-save-options",
	"jpeg-exif-data",
	"jpeg-original-settings",
	"gamma",
	"chromaticity",
	"rendering-intent",
	"hot-spot",
	"exif-data",
	"gimp-metadata",
	"icc-profile",
	"icc-profile-name",
	"decompose-data",
	"print-settings",
	"print-page-setup",
	"dcm/XXXX-XXXX-AA",
]
KNOWN_LAYER_PARASITES = ["gimp-text-layer", "gfig"]


class GimpParasite:
	"""Parasites are arbitrary (meta)data strings that can be attached to a document tree item.

	They are used to store things like last-used plugin settings, gamma adjuetments, etc.

	Format of known parasites:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/parasites.txt
	"""

	def __init__(self) -> None:
		self.name = ""
		self.flags = 0
		self.data = None

	def decode(self, data: bytearray, index: int = 0) -> int:
		"""Decode a byte buffer.

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO(data, index)
		self.name = ioBuf.sz754
		self.flags = ioBuf.u32
		dataLength = ioBuf.u32
		self.data = ioBuf.getbytearray(dataLength)
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Encode a byte buffer.

		:param data: data buffer to encode
		:param index: index within the buffer to start at
		"""
		ioBuf = IO()
		ioBuf.sz754 = self.name
		ioBuf.u32 = self.flags
		ioBuf.u32 = len(self.data or b"")
		ioBuf.addbytearray(self.data)
		return ioBuf.data

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return (
			f"<GimpParasite name={self.name!r}, flags={self.flags}, "
			f"data_len={len(self.data or '')}>"
		)
