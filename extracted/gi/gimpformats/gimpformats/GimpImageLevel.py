"""Gets packed pixels from a gimp image.

This represents a single level in an imageHierarchy
"""

from __future__ import annotations

import math
import zlib

import PIL.Image
from PIL.Image import Image

from gimpformats.GimpIOBase import IO, CompressionMode, GimpIOBase

# pylint:disable=invalid-name


class GimpImageLevel(GimpIOBase):
	"""Gets packed pixels from a gimp image.

	This represents a single level in an imageHierarchy
	"""

	def __init__(self, parent) -> None:
		GimpIOBase.__init__(self, parent)
		self.width = 0
		self.height = 0
		self._tiles = None  # tile PIL images
		self._image = None

	def decode(self, data: bytearray | bytes | None, index: int = 0) -> int:
		"""Decode a byte buffer.

		:param data: data buffer to decode
		:param index: index within the buffer to start at
		"""
		if data is None:
			return -1
		ioBuf = IO(data, index)
		# print 'Decoding image level at',ioBuf.index
		self.width = ioBuf.u32
		self.height = ioBuf.u32
		if self.width != self.parent.width or self.height != self.parent.height:
			currentSize = f"({self.width}" + f",{self.height})"
			expectedSize = f"({self.parent.width}" + f",{self.parent.height})"
			msg = " Usually this implies file corruption."
			raise RuntimeError(
				"Image data size mismatch. " + currentSize + "!=" + expectedSize + msg
			)
		self._tiles = []
		self._image = None
		for y in range(0, self.height, 64):
			for x in range(0, self.width, 64):
				ptr = self._pointerDecode(ioBuf)
				size = (min(self.width - x, 64), min(self.height - y, 64))
				totalbytearray = size[0] * size[1] * self.bpp
				if self.doc.compression == CompressionMode.None_Compression:  # none
					data = ioBuf.data[ptr : ptr + totalbytearray]
				elif self.doc.compression == CompressionMode.RLE:  # RLE
					data = self._decodeRLE(ioBuf.data, size[0] * size[1], self.bpp, ptr)
				elif self.doc.compression == CompressionMode.Zlib:  # zip
					data = zlib.decompress(
						ioBuf.data[ptr : ptr + totalbytearray + 24]
					)  # guess how many bytearray are needed
				else:
					msg = f"ERR: unsupported compression mode {self.doc.compression}"
					raise RuntimeError(msg)
				subImage = PIL.Image.frombytes(self.mode, size, bytearray(data), decoder_name="raw")
				self._tiles.append(subImage)
		_ = self._pointerDecode(ioBuf)  # list ends with nul character
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Encode this object to a byte buffer."""
		dataioBuf = IO()
		ioBuf = IO()
		ioBuf.u32 = self.width
		ioBuf.u32 = self.height
		dataIndex = ioBuf.index + self.pointerSize * (len(self.tiles or []) + 1)
		for tile in self.tiles or []:
			ioBuf.addbytearray(self._pointerEncode(dataIndex + dataioBuf.index))
			data = tile.tobytearray()
			if self.doc.compression == 0:  # none
				pass
			elif self.doc.compression == 1:  # RLE
				data = self._encodeRLE(data, self.bpp)
				# raise RuntimeError('RLE Compression is a work in progress!')
			elif self.doc.compression == 2:  # zip
				data = zlib.compress(data)
			else:
				msg = f"ERR: unsupported compression mode {self.doc.compression}"
				raise RuntimeError(msg)
			dataioBuf.addbytearray(data)
		ioBuf.addbytearray(self._pointerEncode(0))
		ioBuf.addbytearray(dataioBuf.data)
		return ioBuf.data

	def _decodeRLE(self, data: bytearray, pixels: int, bpp, index=0) -> bytearray:
		_ = self
		"""Decode RLE encoded image data."""
		ret = [bytearray() for _ in range(bpp)]  # Use bytearray to avoid repeated list appends

		for chan in range(bpp):
			n = 0
			while n < pixels:
				opcode = data[index]
				index += 1

				if 0 <= opcode <= 126:  # Short run of identical bytes
					val = data[index]
					index += 1
					ret[chan].extend([val] * (opcode + 1))  # Extend is faster than append in a loop
					n += opcode + 1

				elif opcode == 127:  # Long run of identical bytes
					m = data[index]
					index += 1
					b = data[index]
					index += 1
					val = data[index]
					index += 1
					amt = (m << 8) + b
					ret[chan].extend([val] * amt)
					n += amt

				elif opcode == 128:  # Long run of different bytes
					m = data[index]
					index += 1
					b = data[index]
					index += 1
					amt = (m << 8) + b
					ret[chan].extend(data[index : index + amt])  # Slicing instead of looping
					index += amt
					n += amt

				elif 129 <= opcode <= 255:  # Short run of different bytes
					amt = 256 - opcode
					ret[chan].extend(data[index : index + amt])  # Slicing instead of looping
					index += amt
					n += amt

				else:
					raise RuntimeError("Invalid RLE opcode")

		# Flatten channels efficiently
		flat = bytearray(pixels * bpp)
		for i in range(pixels):
			for chan in range(bpp):
				flat[i * bpp + chan] = ret[chan][i]

		return flat

	def _encodeRLE(self, data, bpp):
		"""Encode image to RLE image data."""
		_ = self

		def countSame(data, startIdx):
			"""Count how many times bytearray are identical."""
			idx = startIdx
			l = len(data)
			if idx >= l:
				return 0
			c = data[idx]
			idx = startIdx + 1
			while idx < l and data[idx] == c:
				idx += 1
			return idx - startIdx

		def countDifferent(data, startIdx):
			"""Count how many times bytearray are different."""
			idx = startIdx
			l = len(data)
			if idx >= l:
				return 1
			c = data[idx]
			idx = startIdx + 1
			while idx < (l - 1) and data[idx] != c:
				idx += 1
				c = data[idx]
			return idx - startIdx

		def rleEncodeChan(data):
			"""Rle encode a single channel of data."""
			ret = []
			idx = 0
			while idx < len(data):
				nRepeats = countSame(data, 0)
				if nRepeats == 1:  # different bytearray
					nDifferences = countDifferent(data, 1)
					if nDifferences <= 127:  # short run of different bytearray
						ret.append(129 + nRepeats - 1)
						ret.append(data[idx])
						idx += nDifferences
					else:  # long run of different bytearray
						ret.append(128)
						ret.append(math.floor(nDifferences / 256.0))
						ret.append(nDifferences % 256)
						ret.append(data[idx])
						idx += nDifferences
				elif nRepeats <= 127:  # short run of same bytearray
					ret.append(nRepeats - 1)
					ret.append(data[idx])
					idx += nRepeats
				else:  # long run of same bytearray
					ret.append(127)
					ret.append(math.floor(nRepeats / 256.0))
					ret.append(nRepeats % 256)
					ret.append(data[idx])
					idx += nRepeats
			return ret

		# if there is only one channel, encode and return it directly
		if bpp == 1:
			return rleEncodeChan(data)
		# split into channels
		dataByChannel = []
		for chan in range(bpp):
			chanData = []
			for index in range(chan, bpp, len(data)):
				chanData.append(data[index])
			dataByChannel.append(chanData)
		# encode each channel
		for dbc in dataByChannel:  # iterate through 2d array
			dbc = rleEncodeChan(dbc)
		# join and return
		return "".join("".join(str(x)) for x in dataByChannel)

	@property
	def bpp(self):
		"""Get bpp."""
		return self.parent.bpp

	@property
	def mode(self):
		"""Get mode."""
		MODES = [None, "L", "LA", "RGB", "RGBA"]
		return MODES[self.bpp]

	@property
	def tiles(self):
		"""Get tiles."""
		if self._tiles is not None:
			return self._tiles
		if self.image is not None:
			return self._imgToTiles(self.image)
		return None

	def _imgToTiles(self, image):
		"""
		Break an image into a series of tiles, each<=64x64.
		"""
		ret = []
		for y in range(0, self.height, 64):
			for x in range(0, self.width, 64):
				bounds = (x, y, min(self.width - x, 64), min(self.height - y, 64))
				ret.append(image.crop(bounds))
		return ret

	@property
	def image(self) -> Image:
		"""
		Get a final, compiled image.
		"""
		if self._image is None:
			self._image = PIL.Image.new(self.mode, (self.width, self.height), color=None)
			tileNum = 0
			for y in range(0, self.height, 64):
				for x in range(0, self.width, 64):
					subImage = self._tiles[tileNum]
					tileNum += 1
					self._image.paste(subImage, (x, y))
			# self._tiles = None
		return self._image

	@image.setter
	def image(self, image: Image) -> None:
		self._image = image
		self._tiles = None
		self.width = image.width
		self.height = image.height
		self.tiles = None

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return f"<GimpImageLevel size={self.width}x{self.height}>"
