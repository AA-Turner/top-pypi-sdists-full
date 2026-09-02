"""Since the precision code is so unusual, I decided to create a class to parse it."""

from __future__ import annotations

from gimpformats.binaryiotools import IO


class Precision:
	"""Since the precision code is so unusual, I decided to create a class to parse it."""

	def __init__(self) -> None:
		"""Since the precision code is so unusual, I decided to create a class to parse it."""
		self.bits = 8
		self.gamma = True
		self.numberFormat = int

	def decode(self, gimpVersion: int, ioBuf: IO) -> None:
		"""Decode the precision code from the file."""
		if gimpVersion < 4:
			self.bits = 8
			self.gamma = True
			self.numberFormat = int
		else:
			code = ioBuf.u32
			if gimpVersion == 4:
				self.gamma = (True, True, False, False, False)[code]
				self.bits = (8, 16, 32, 16, 32)[code]
				self.numberFormat = (int, int, int, float, float)[code]
			elif gimpVersion in (5, 6):
				self.gamma = code % 100 != 0
				code = int(code / 100)
				self.bits = (8, 16, 32, 16, 32)[code]
				self.numberFormat = (int, int, int, float, float)[code]
			else:  # gimpVersion 7 or above
				self.gamma = code % 100 != 0
				code = int(code / 100)
				self.bits = (8, 16, 32, 16, 32, 64)[code]
				self.numberFormat = (int, int, int, float, float, float)[code]

	def encode(self, gimpVersion: int, ioBuf: IO) -> None:
		"""Encode this to the file.

		NOTE: will not mess with development versions 5 or 6
		"""
		if gimpVersion < 4:
			if self.bits != 8 or not (self.gamma) or isinstance(self.numberFormat, int):
				raise RuntimeError(
					f"Illegal precision ({self}" + f") for gimp version {gimpVersion}"
				)
		else:
			if gimpVersion == 4:
				if self.bits == 64:
					raise RuntimeError(
						f"Illegal precision ({self}" + f") for gimp version {gimpVersion}"
					)
				if isinstance(self.numberFormat, int):
					code = (8, 16, 32).index(self.bits)
				else:
					code = (16, 32).index(self.bits) + 2
				code = code * 100
				if self.gamma:
					code += 50
			elif gimpVersion in (5, 6):
				msg = f"Cannot save to gimp developer version {gimpVersion}"
				raise NotImplementedError(msg)
			else:  # version 7 or above
				if isinstance(self.numberFormat, int):
					code = (8, 16, 32).index(self.bits)
				else:
					code = (16, 32, 64).index(self.bits) + 2
				code = code * 100
				if self.gamma:
					code += 50
			ioBuf.u32 = code

	def requiredGimpVersion(self) -> int:
		"""Return the lowest gimp version that supports this precision."""
		if self.bits == 8 and self.gamma and isinstance(self.numberFormat, int):
			return 0
		if self.bits == 64:
			return 7
		return 4

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return (
			f"<GimpPrecision bits={self.bits}-bit, "
			f"gamma={'gamma' if self.gamma else 'linear'}, "
			f"format={'integer' if self.numberFormat is int else 'float'}>"
		)
