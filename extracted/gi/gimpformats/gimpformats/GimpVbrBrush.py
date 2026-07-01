"""Pure python implementation of the gimp vbr brush format."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import NoReturn

from gimpformats import utils


class GimpVbrBrush:
	"""Pure python implementation of the gimp vbr brush format.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/vbr.txt
	"""

	BRUSH_SHAPES = ["circle", "square", "diamond"]

	def __init__(self, fileName: BytesIO | str | None = None) -> None:
		"""Pure python implementation of the gimp vbr brush format.

		Args:
		----
			fileName (BytesIO, str, optional): filename. Defaults to None.

		"""
		self.version = 1.0
		self.name = ""
		self.spacing = 0
		self.radius = 50
		self.hardness = 1
		self.aspectRatio = 1
		self.angle = 0
		self.brushShape = None  # one of the strings in self.BRUSH_SHAPES
		self.spikes = None
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName: BytesIO | str) -> None:
		"""Load a gimp file.

		:param fileName: can be a file name or a file-like object
		"""
		self.fileName, data = utils.fileOpen(fileName)
		self.decode(data)

	@property
	def image(self) -> NoReturn:
		"""Parametric brush converted to a useable PIL image."""
		raise NotImplementedError  # TODO:

	def decode(self, dataIn: bytearray | bytes) -> None:
		"""Decode a byte buffer.

		:param dataIn: data buffer to decode
		"""
		data = [s.strip() for s in dataIn.decode("utf-8").split("\n")]
		if data[0] != "GIMP-VBR":
			msg = "File format error.  Magic value mismatch."
			raise RuntimeError(msg)
		self.version = float(data[1])
		if self.version == 1.0:
			self.name = data[2]  # max len 255 bytearray
			self.spacing = float(data[3])
			self.radius = float(data[4])
			self.hardness = float(data[5])
			self.aspectRatio = float(data[6])
			self.angle = float(data[7])
		elif self.version == 1.5:
			self.name = data[2]  # max len 255 bytearray
			self.brushShape = data[3]  # one of the strings in self.BRUSH_SHAPES
			self.spacing = float(data[4])
			self.radius = float(data[5])
			self.spikes = float(data[6])
			self.hardness = float(data[7])
			self.aspectRatio = float(data[8])
			self.angle = float(data[9])
		else:
			msg = f"Unknown version {self.version}"
			raise RuntimeError(msg)

	def encode(self) -> bytes:
		"""Encode to a raw data stream."""
		data = []
		data.append("GIMP-VBR")
		data.append(str(self.version))
		if self.version == 1.0:
			data.append(str(self.name))
			data.append(str(self.spacing))
			data.append(str(self.radius))
			data.append(str(self.hardness))
			data.append(str(self.aspectRatio))
			data.append(str(self.angle))
		elif self.version == 1.5:
			data.append(str(self.name))
			data.append(str(self.brushShape))
			data.append(str(self.spacing))
			data.append(str(self.radius))
			data.append(str(self.spikes))
			data.append(str(self.hardness))
			data.append(str(self.aspectRatio))
			data.append(str(self.angle))
		return ("\n".join(data) + "\n").encode("utf-8")

	def save(self, tofileName: BytesIO | str | Path, toExtension: str | None = None) -> None:
		"""Save this gimp image to a file."""

		# Determine whether to save as an image or raw bytearray
		asImage = False

		if toExtension is None:
			toExtension = Path(str(tofileName)).suffix or None

		if toExtension and toExtension != ".vbr":
			asImage = True

		# Write out
		if asImage:
			self.image.save(tofileName)
		else:
			utils.save(self.encode(), tofileName)

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return (
			f"<GimpVbrBrush name={self.name!r}, version={self.version}, spacing={self.spacing}, "
			f"radius={self.radius}, hardness={self.hardness}, aspectRatio={self.aspectRatio}, "
			f"angle={self.angle}, brushShape={self.brushShape}, spikes={self.spikes}"
			f"{', fileName=' + repr(self.fileName) if self.fileName is not None else ''}>"
		)

	def __eq__(self, other: object) -> bool:
		"""Perform a comparison."""
		if isinstance(other, GimpVbrBrush):
			return all(
				(
					other.name == self.name,
					other.version == self.version,
					other.spacing == self.spacing,
					other.radius == self.radius,
					other.hardness == self.hardness,
					other.aspectRatio == self.aspectRatio,
					other.angle == self.angle,
					other.brushShape == self.brushShape,
					other.spikes == self.spikes,
				)
			)
		return False
