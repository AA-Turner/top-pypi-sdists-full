"""Gimp color gradient."""

from __future__ import annotations

from io import BytesIO
from typing import ClassVar, NoReturn

from gimpformats import utils
from gimpformats.utils import repr_indent_lines


class GradientSegment:
	"""Single segment within a gradient."""

	BLEND_FUNCTIONS: ClassVar[list] = [
		"linear",
		"curved",
		"sinusoidal",
		"spherical (increasing)",
		"spherical (decreasing)",
		"step",
	]
	COLOR_TYPES: ClassVar[list] = ["RGB", "HSV CCW", "HSV CW"]
	ENDPOINT_COLOR_TYPES: ClassVar[list] = [
		"fixed",
		"foreground",
		"foreground transparent",
		"background",
		"background transparent",
	]

	def __init__(self) -> None:
		"""Single segment within a gradient."""
		self.leftPosition = 0
		self.middlePosition = 0.5
		self.rightPosition = 1.0
		self.leftColor = (0, 0, 0, 0)
		self.rightColor = (255, 255, 255, 0)
		self.blendFunc = None  # one of self.BLEND_FUNCTIONS
		self.colorType = None  # one of self.COLOR_TYPES
		self.leftColorType = None  # one of self.ENDPOINT_COLOR_TYPES
		self.rightColorType = None  # one of self.ENDPOINT_COLOR_TYPES

	def getColor(self, percent: float) -> NoReturn:
		"""Given a decimal percent (1.0 = 100%) retrieve the appropriate color
		for this point in the gradient.
		"""
		_ = self, percent
		raise NotImplementedError

	def decode(self, dataIn: str) -> None:
		"""Decode a byte buffer.

		Args:
		----
			dataIn (str): data buffer to decode

		Raises:
		------
			RuntimeError: [description]

		"""
		data = dataIn.split(" ")
		if len(data) < 11 or len(data) > 15:
			msg = f"Data table is unexpected size. {len(data)}"
			raise RuntimeError(msg)
		self.leftPosition = float(data[0])
		self.middlePosition = float(data[1])
		self.rightPosition = float(data[2])
		self.leftColor = (float(data[3]), float(data[4]), float(data[5]), float(data[6]))
		self.rightColor = (float(data[7]), float(data[8]), float(data[9]), float(data[10]))
		if len(data) >= 12:
			self.blendFunc = int(data[11])
			if len(data) >= 13:
				self.colorType = int(data[12])
				if len(data) >= 14:
					self.leftColorType = int(data[13])
					if len(data) >= 15:
						self.rightColorType = int(data[14])

	def encode(self) -> str:
		"""Encode this to a string."""
		ret = []
		ret.append(f"{self.leftPosition:06f}")
		ret.append(f"{self.middlePosition:06f}")
		ret.append(f"{self.rightPosition:06f}")
		ret.extend([f"{chan:06f}" for chan in self.leftColor])
		ret.extend([f"{chan:06f}" for chan in self.rightColor])
		if self.blendFunc is not None:
			ret.append(f"{self.blendFunc}")
			if self.colorType is not None:
				ret.append(f"{self.colorType}")
				if self.leftColorType is not None:
					ret.append(f"{self.leftColorType}")
					if self.rightColorType is not None:
						ret.append(f"{self.rightColorType}")
		return " ".join(ret)

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.full_repr()

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = []
		ret.append(f"Left Position: {self.leftPosition}")
		ret.append(f"Middle Position: {self.middlePosition}")
		ret.append(f"Right Position: {self.rightPosition}")
		ret.append(f"Left Color: {self.leftColor}")
		ret.append(f"Right Color: {self.rightColor}")
		if self.blendFunc:
			ret.append(f"Blend Function: {self.BLEND_FUNCTIONS[self.blendFunc]}")
		if self.colorType:
			ret.append(f"Color Type: {self.COLOR_TYPES[self.colorType]}")
		if self.leftColorType:
			ret.append(f"Left Color Type: {self.ENDPOINT_COLOR_TYPES[self.leftColorType]}")
		if self.rightColorType:
			ret.append(f"Right Color Type: {self.ENDPOINT_COLOR_TYPES[self.rightColorType]}")
		return repr_indent_lines(indent, ret)


class GimpGgrGradient:
	"""Gimp color gradient.

	See:
		https://gitlab.gnome.org/GNOME/gimp/blob/master/devel-docs/ggr.txt
	"""

	def __init__(self, fileName: str | None = None) -> None:
		"""GimpGgrGradient.

		Args:
		----
			fileName (str, optional): filename. Defaults to None.

		"""
		self.fileName = None
		self.segments = []
		self.name = ""
		if fileName is not None:
			self.load(fileName)

	def load(self, fileName: BytesIO | str) -> None:
		"""Load a gimp file.

		:param fileName: can be a file name or a file-like object
		"""
		self.fileName, data = utils.fileOpen(fileName)
		self.decode(data)

	def decode(self, dataIn: bytearray | bytes) -> None:
		"""Decode a byte buffer.

		Args:
		----
			dataIn (bytearray): data buffer to decode

		Raises:
		------
			RuntimeError: File format error.  Magic value mismatch.

		"""
		self.segments = []

		data = dataIn.decode("utf-8").split("\n")
		data = [line.strip() for line in data]
		if data[0] != "GIMP Gradient":
			msg = "File format error.  Magic value mismatch."
			raise RuntimeError(msg)
		self.name = data[1].split(":", 1)[-1].strip()
		numSegments = int(data[2])
		for i in range(numSegments):
			gSeg = GradientSegment()
			gSeg.decode(data[i + 3])
			self.segments.append(gSeg)

	def encode(self) -> bytes:
		"""Encode this to bytearray."""
		ret = ["GIMP Gradient"]
		ret.append(f"Name: {self.name}")
		ret.append(str(len(self.segments)))
		ret.extend([segment.encode() for segment in self.segments])
		return ("\n".join(ret) + "\n").encode("utf-8")

	def save(self, tofileName: str | BytesIO) -> None:
		"""Save this gimp image to a file."""
		utils.save(self.encode(), tofileName)

	def getColor(self, percent: float) -> NoReturn:
		"""Given a decimal percent (1.0 = 100%) retrieve...

		the appropriate color for this point in the gradient.
		"""
		raise NotImplementedError

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.full_repr()

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = []
		if self.fileName is not None:
			ret.append(f"fileName: {self.fileName}")
		ret.append(f"Name: {self.name}")
		ret.extend([ret.append(seg.full_repr(indent=indent + 1)) for seg in self.segments])

		return repr_indent_lines(indent, ret)
