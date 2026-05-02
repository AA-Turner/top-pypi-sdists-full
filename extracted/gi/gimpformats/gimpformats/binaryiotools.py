"""
Base binary I/O helper.

Does boilerplate things like reading the next uint32 from a file or binary stream

Create a new IO object and initialize/ set data

Example:
-------
```python
f = open(fileName, "rb")
data = f.read()
f.close()
io = IO(data)
width = io.u32
height = io.u32
```

The example above reads a file in binary and sets the variables width and height
as the first two unsigned integer 32s

For a file starting with the bytearray:

```none
00 00 00 C8 00 01 90
```

The values for width and height would be 200, 400

"""

from __future__ import annotations

import struct
from typing import Any

# ruff: noqa: ANN401


class IO:
	"""Class to handle i/o to a byte buffer or file-like object."""

	def __init__(
		self,
		data: bytearray | bytes | None = None,
		idx: int = 0,
		littleEndian: bool = False,
		boolSize: int = 8,
		stringEncoding: str = "U",
	) -> None:
		"""Class to handle i/o to a byte buffer or file-like object.

		:param data: can be a data buffer or a file-like object
		:param idx: start reading/writing the data at the given index
		:param littleEndian: whether the default is big-endian or little-endian
		:param boolSize: how many default bits to use for a bool (8,16,32,or 64)
		:param stringEncoding: default string encoding A=Ascii, U=UTF-8, W-Unicode wide
		"""
		if data is None:
			data = bytearray()
		self._data = data
		self._index = idx
		self._contexts = []
		self.littleEndian = littleEndian
		self.boolSize = boolSize
		self.stringEncoding = stringEncoding  # A=Ascii, U=UTF-8, W-Unicode wide

	def __len__(self) -> int:
		"""Length of data."""
		return len(self.data)

	def __getitem__(self, idx: int):
		"""Get data at a specific idx."""
		return self.data[idx]

	@property
	def data(self) -> bytearray:
		"""Return data as a mutable bytearray."""
		if isinstance(self._data, bytearray):
			return self._data
		if not hasattr(self, "_converted_data"):  # Cache converted bytearray
			self._converted_data = bytearray(self._data)
		return self._converted_data

	@data.setter
	def data(self, data: bytearray) -> None:
		"""Set data."""
		if not hasattr(data, "__getitem__"):
			raise RuntimeError("ERR: incorrect type for data buffer" + str(type(data)))
		self._data = data

	@property
	def index(self) -> int:
		"""Return data."""
		return self._index

	@index.setter
	def index(self, index: int) -> None:
		"""Set index."""
		self._index = index

	def beginContext(self, newIndex: int) -> None:
		"""Start a new context where the index can be changed all you want...

		and when endContext() is called, it will be restored to the current position
		"""
		self._contexts.append(newIndex)

	def endContext(self) -> None:
		"""Restore the index to the previous location where it was when	beginContext() was called."""
		self.index = self._contexts.pop()

	def _write(self, size: int, fmt: str, data: Any) -> None:
		"""General formatted write."""
		if self.index + size >= len(self.data):
			self.data.extend(bytearray((self.index + size) - len(self.data)))
		try:
			struct.pack_into(fmt, self.data, self.index, data)
			self.index += size
		except (DeprecationWarning, struct.error) as upstream:
			raise RuntimeError(type(data), fmt, size, data) from upstream

	def _read(self, size: int, fmt: str) -> Any:
		"""General formatted read."""
		try:
			data = struct.unpack(fmt, self.data[self.index : self.index + size])[0]
		except (DeprecationWarning, struct.error) as upstream:
			raise RuntimeError(
				str(fmt)
				+ " "
				+ str(size)
				+ " "
				+ str(self.index)
				+ " "
				+ str(len(self.data))
				+ " "
				+ str(self.data[self.index : self.index + size])
			) from upstream
		# Move the pointer forward
		self.index += size
		return data

	@property
	def boolean(self) -> bool:
		"""Return bool."""
		if self.boolSize == 8:
			return self.bool8
		if self.boolSize == 16:
			return self.bool16
		if self.boolSize == 32:
			return self.bool32
		if self.boolSize == 64:
			return self.bool64
		raise RuntimeError("Unknown bool size " + str(self.boolSize))

	@boolean.setter
	def boolean(self, ioBool: bool) -> None:
		"""Set bool."""
		if self.boolSize == 8:
			self.bool8 = ioBool
		elif self.boolSize == 16:
			self.bool16 = ioBool
		elif self.boolSize == 32:
			self.bool32 = ioBool
		elif self.boolSize == 64:
			self.bool64 = ioBool
		else:
			raise RuntimeError("Unknown bool size " + str(self.boolSize))

	@property
	def bool8(self) -> bool:
		"""Get bool8."""
		return self.u8 != 0

	@bool8.setter
	def bool8(self, ioBool: bool) -> None:
		"""Set a bool8."""
		self.u8 = ioBool

	@property
	def bool16(self) -> bool:
		"""Get bool16."""
		return self.u16 != 0

	@bool16.setter
	def bool16(self, ioBool: bool) -> None:
		"""Set bool16."""
		self.u16 = ioBool

	@property
	def bool32(self) -> bool:
		"""Get bool32."""
		return self.u32 != 0

	@bool32.setter
	def bool32(self, ioBool: bool) -> None:
		"""Set bool32."""
		self.u32 = ioBool

	@property
	def bool64(self) -> bool:
		"""Get bool64."""
		return self.u64 != 0

	@bool64.setter
	def bool64(self, ioBool: bool) -> None:
		"""Set bool64."""
		self.u64 = ioBool

	@property
	def byte(self) -> Any:
		"""Get byte."""
		return self.i8

	@byte.setter
	def byte(self, byte: Any) -> None:
		"""Set byte."""
		self.i8 = byte

	@property
	def unsignedByte(self) -> Any:
		"""Get unsigned byte."""
		return self.u8

	@unsignedByte.setter
	def unsignedByte(self, byte: Any) -> None:
		"""Set unsigned byte."""
		self.u8 = byte

	@property
	def word(self) -> Any:
		"""Get a word."""
		return self.i16

	@word.setter
	def word(self, word: Any) -> None:
		"""Set a word."""
		self.i16 = word

	@property
	def unsignedWord(self) -> Any:
		"""Get an unsigned word."""
		return self.u16

	@unsignedWord.setter
	def unsignedWord(self, unsignedWord: Any) -> None:
		"""Set an unsigned word."""
		self.u16 = unsignedWord

	@property
	def dword(self) -> Any:
		"""Get a dword."""
		return self.i32

	@dword.setter
	def dword(self, dword: Any) -> None:
		"""Set a dword."""
		self.i32 = dword

	@property
	def unsignedDword(self) -> Any:
		"""Get a unsigned dword."""
		return self.u32

	@unsignedDword.setter
	def unsignedDword(self, unsignedDword: Any) -> None:
		"""Set an unsigned dword."""
		self.u32 = unsignedDword

	@property
	def qword(self) -> Any:
		"""Get a qword."""
		return self.i64

	@qword.setter
	def qword(self, qword: Any) -> None:
		"""Set a qword."""
		self.i64 = qword

	@property
	def unsignedQword(self) -> Any:
		"""Get an unsigned qword."""
		return self.u64

	@unsignedQword.setter
	def unsignedQword(self, unsignedQword: Any) -> None:
		"""Set an unsigned qword."""
		self.u64 = unsignedQword

	@property
	def i8(self) -> int:
		"""Get an int8."""
		if self.littleEndian:
			return self.i8le
		return self.i8be

	@i8.setter
	def i8(self, i8: int) -> None:
		"""Set an int8."""
		if self.littleEndian:
			self.i8le = i8
		else:
			self.i8be = i8

	@property
	def u8(self) -> int:
		"""Get an unsigned int."""
		if self.littleEndian:
			return self.u8le
		return self.u8be

	@u8.setter
	def u8(self, u8: int) -> None:
		"""Set an unsigned int."""
		if self.littleEndian:
			self.u8le = u8
		else:
			self.u8be = u8

	@property
	def i16(self) -> int:
		"""Get an int16."""
		if self.littleEndian:
			return self.i16le
		return self.i16be

	@i16.setter
	def i16(self, i16: int) -> None:
		"""Set an int16."""
		if self.littleEndian:
			self.i16le = i16
		else:
			self.i16be = i16

	@property
	def u16(self) -> int:
		"""Get an uint16."""
		if self.littleEndian:
			return self.u16le
		return self.u16be

	@u16.setter
	def u16(self, u16: int) -> None:
		"""Set an unint16."""
		if self.littleEndian:
			self.u16le = u16
		else:
			self.u16be = u16

	@property
	def i32(self) -> int:
		"""Get an int32."""
		if self.littleEndian:
			return self.i32le
		return self.i32be

	@i32.setter
	def i32(self, i32: int) -> None:
		"""Set an int32."""
		if self.littleEndian:
			self.i32le = i32
		else:
			self.i32be = i32

	@property
	def u32(self) -> int:
		"""Get a uint32."""
		if self.littleEndian:
			return self.u32le
		return self.u32be

	@u32.setter
	def u32(self, u32: int) -> None:
		"""Set a unint32."""
		if self.littleEndian:
			self.u32le = u32
		else:
			self.u32be = u32

	@property
	def i64(self) -> int:
		"""Get an int64."""
		if self.littleEndian:
			return self.i64le
		return self.i64be

	@i64.setter
	def i64(self, i64: int) -> None:
		"""Set an int64."""
		if self.littleEndian:
			self.i64le = i64
		else:
			self.i64be = i64

	@property
	def u64(self) -> int:
		"""Get a uint64."""
		if self.littleEndian:
			return self.u64le
		return self.u64be

	@u64.setter
	def u64(self, u64: int) -> None:
		"""Set a uint64."""
		if self.littleEndian:
			self.u64le = u64
		else:
			self.u64be = u64

	@property
	def float32(self) -> float:
		"""Get a float32."""
		if self.littleEndian:
			return self.float32le
		return self.float32be

	@float32.setter
	def float32(self, float32: float) -> None:
		"""Set a float32."""
		if self.littleEndian:
			self.float32le = float32
		else:
			self.float32be = float32

	@property
	def float64(self) -> float:
		"""Get a float64."""
		if self.littleEndian:
			return self.float64le
		return self.float64be

	@float64.setter
	def float64(self, float64: float) -> None:
		"""Set a float64."""
		if self.littleEndian:
			self.float64le = float64
		else:
			self.float64be = float64

	@property
	def u8be(self) -> int:
		"""Read the next uint8 and advance the index."""
		return self._read(1, ">B")

	@u8be.setter
	def u8be(self, u8be: int) -> None:
		"""Set the uint8."""
		self._write(1, ">B", u8be)

	@property
	def u8le(self) -> int:
		"""Read the next uint8 and advance the index."""
		return self._read(1, "<B")

	@u8le.setter
	def u8le(self, u8le: int) -> None:
		"""Set the uint8."""
		self._write(1, "<B", u8le)

	@property
	def i8le(self) -> int:
		"""Read the next signed int8 and advance the index."""
		return self._read(1, "<b")

	@i8le.setter
	def i8le(self, i8le: int) -> None:
		"""Set the int8."""
		self._write(1, "<b", i8le)

	@property
	def i8be(self) -> int:
		"""Read the next signed int8 and advance the index."""
		return self._read(1, ">b")

	@i8be.setter
	def i8be(self, i8be: int) -> None:
		"""Set the int8."""
		self._write(1, ">b", i8be)

	@property
	def u16be(self) -> int:
		"""Read the next uint16 and advance the index."""
		return self._read(2, ">H")

	@u16be.setter
	def u16be(self, u16be: int) -> None:
		"""Set the uint16."""
		self._write(2, ">H", u16be)

	@property
	def u16le(self) -> int:
		"""Read the next uint16 and advance the index."""
		return self._read(2, "<H")

	@u16le.setter
	def u16le(self, u16le: int) -> None:
		"""Set the uint16."""
		self._write(2, "<H", u16le)

	@property
	def i16le(self) -> int:
		"""Read the next signed int16 and advance the index."""
		return self._read(2, "<h")

	@i16le.setter
	def i16le(self, i16le: int) -> None:
		"""Set the int16."""
		self._write(2, "<h", i16le)

	@property
	def i16be(self) -> int:
		"""Read the next signed int16 and advance the index."""
		return self._read(2, ">h")

	@i16be.setter
	def i16be(self, i16be: int) -> None:
		"""Set the int16."""
		self._write(2, ">h", i16be)

	@property
	def u32be(self) -> int:
		"""Read the next uint32 and advance the index."""
		return self._read(4, ">I")

	@u32be.setter
	def u32be(self, u32be: int) -> None:
		"""Set the uint32."""
		self._write(4, ">I", u32be)

	@property
	def u32le(self) -> int:
		"""Read the next uint32 and advance the index."""
		return self._read(4, "<I")

	@u32le.setter
	def u32le(self, u32le: int) -> None:
		"""Set the uint32."""
		self._write(4, "<I", u32le)

	@property
	def i32le(self) -> int:
		"""Read the next signed int32 and advance the index."""
		return self._read(4, "<i")

	@i32le.setter
	def i32le(self, i32le: int) -> None:
		"""Set the int32."""
		self._write(4, "<i", i32le)

	@property
	def i32be(self) -> int:
		"""Read the next signed int32 and advance the index."""
		return self._read(4, ">i")

	@i32be.setter
	def i32be(self, i32be: int) -> None:
		"""Set the int32."""
		self._write(4, ">i", i32be)

	@property
	def u64be(self) -> int:
		"""Read the next uint64 and advance the index."""
		return self._read(8, ">Q")

	@u64be.setter
	def u64be(self, u64be: int) -> None:
		"""Set the uint64."""
		self._write(8, ">Q", u64be)

	@property
	def u64le(self) -> int:
		"""Read the next uint64 and advance the index."""
		return self._read(8, "<Q")

	@u64le.setter
	def u64le(self, u64le: int) -> None:
		"""Set the uint64."""
		self._write(8, "<Q", u64le)

	@property
	def i64le(self) -> int:
		"""Read the next signed int64 and advance the index."""
		return self._read(8, "<q")

	@i64le.setter
	def i64le(self, i64le: int) -> None:
		"""Set the int64."""
		self._write(8, "<q", i64le)

	@property
	def i64be(self) -> int:
		"""Read the next signed int64 and advance the index."""
		return self._read(8, ">q")

	@i64be.setter
	def i64be(self, i64be: int) -> None:
		"""Set the int64."""
		self._write(8, ">q", i64be)

	@property
	def floating(self) -> float:
		"""Get a float."""
		return self.float32

	@floating.setter
	def floating(self, floating: float) -> None:
		"""Set a float."""
		self.float32 = floating

	@property
	def double(self) -> float:
		"""Get a double."""
		return self.float64

	@double.setter
	def double(self, floating: float) -> None:
		"""Set a double."""
		self.float64 = floating

	@property
	def float32be(self) -> float:
		"""Read the next 32 bit float and advance the index."""
		return self._read(4, ">f")

	@float32be.setter
	def float32be(self, float32be: float) -> None:
		"""Set a 32 bit float."""
		self._write(4, ">f", float32be)

	@property
	def float32le(self) -> float:
		"""Read the next 32 bit float and advance the index."""
		return self._read(4, "<f")

	@float32le.setter
	def float32le(self, float32le: float) -> None:
		"""Set a 32 bit float."""
		self._write(4, "<f", float32le)

	@property
	def float64be(self) -> float:
		"""Read the next 64 bit float and advance the index."""
		return self._read(8, ">d")

	@float64be.setter
	def float64be(self, float64be: float) -> None:
		"""Set a 64 bit float."""
		self._write(8, ">d", float64be)

	@property
	def float64le(self) -> float:
		"""Read the next 64 bit float and advance the index."""
		return self._read(8, "<d")

	@float64le.setter
	def float64le(self, float64le: float) -> None:
		"""Set a 64 bit float."""
		self._write(8, "<d", float64le)

	def getbytearray(self, nbytearray: int):
		"""Grab some raw bytearray and advance the index."""
		data = self.data[self.index : self.index + nbytearray]
		self.index += nbytearray
		return data

	def addbytearray(self, iobytearray: Any) -> None:
		"""Add some raw bytearray and advance the index.

		alias for setbytearray()

		:param bytearray: can be a string, bytearray, or another IO object
		"""
		self.setbytearray(iobytearray)

	def setbytearray(self, iobytearray: Any) -> None:
		"""Add some raw bytearray and advance the index.

		alias for addbytearray()

		:param iobytearray: can be a string, bytearray, or another IO object
		"""
		if isinstance(iobytearray, IO):
			iobytearray = iobytearray.data
		if isinstance(iobytearray, str):
			iobytearray = bytearray(iobytearray, encoding="utf-8")
		if self.index >= len(self.data):
			# if we're at the end, simply extend the buffer
			self.data.extend(iobytearray)
			self.index += len(iobytearray)
		else:
			if self.index + len(iobytearray) >= len(self.data):
				self.data.extend(bytearray((self.index + len(iobytearray)) - len(self.data)))
			for ioByte in iobytearray:
				self.data[self.index] = ioByte
				self.index += 1

	def _sz754(self, encoding: str) -> str:
		"""Read the next string conforming to IEEE 754 and advance the index.

		Note, string format is:
			uint32   n+1  Number of bytearray that follow, including the zero byte
			byte[n]  ...  String data in Unicode, encoded using UTF-8
			byte     0    Zero marks the end of the string.
		or simply uint32=0 for empty string
		"""
		nchars = self.u32
		if nchars == 0:
			return ""
		data = self.data[self.index : self.index + nchars - 1]
		self.index += nchars
		if encoding == "A":
			return data
		if encoding == "U":
			return data.decode("UTF-8", errors="replace")
		if encoding == "W":
			return data.decode("UTF-16", errors="replace")
		raise RuntimeError

	def _sz754set(self, sz754: Any, _encoding: str) -> None:
		"""_sz754set."""
		self.u32 = len(sz754)
		self.setbytearray(sz754)
		self.u8 = 0

	@property
	def sz754(self) -> Any:
		"""sz754."""
		return self._sz754(self.stringEncoding)

	@sz754.setter
	def sz754(self, sz754: Any) -> None:
		"""Set sz754."""
		return self._sz754set(sz754, self.stringEncoding)

	@property
	def sz754A(self) -> Any:
		"""sz754A."""
		return self._sz754("A")

	@sz754A.setter
	def sz754A(self, sz754: Any) -> None:
		"""Set sz754A."""
		return self._sz754set(sz754, "A")

	@property
	def sz754W(self) -> Any:
		"""sz754W."""
		return self._sz754("W")

	@sz754W.setter
	def sz754W(self, sz754: Any) -> None:
		"""Set sz754W."""
		return self._sz754set(sz754, "W")

	@property
	def sz754U(self) -> Any:
		"""sz754U."""
		return self._sz754("U")

	@sz754U.setter
	def sz754U(self, sz754: Any) -> None:
		"""Set sz754U."""
		return self._sz754set(sz754, "U")

	def _readUntil(self, until: str, encoding: str = "A") -> str:
		"""Read a sequence of chars in a set encoding until a set char.

		:param until: must be within the ascii character set
		:param encoding: one of A (ascii), U (UTF-8) or W (UCS-2)
		"""
		data = []
		if encoding == "A":
			encoding = "ascii"
		elif encoding == "U":
			encoding = "UTF-8"
		elif encoding == "W":
			encoding = "UCS-2"
		else:
			msg = "bogus encoding"
			raise RuntimeError(msg)
		untilB = until.encode("ascii")[0]  # always ascii
		while True:
			char = self.data[self.index]
			self.index += 1
			if encoding == "W":  # get one more byte
				data.append(char)
				char = self.data[self.index]
				self.index += 1
			if char == untilB:
				break
			data.append(char)
		return bytearray(data).decode(encoding, errors="replace")

	@property
	def textLine(self) -> str:
		"""Read a sequence of chars until the next new line char."""
		ret = self._readUntil("\n", self.stringEncoding)
		if ret[-1] == "\r":
			ret = ret[-1]
		return ret

	@textLine.setter
	def textLine(self, text: str) -> None:
		"""Set a sequence of chars until the next new line char."""
		self.setbytearray(text)
		if isinstance(text, (int, float)) or text[-1] != "\n":
			self.setbytearray("\n")

	@property
	def textLineA(self) -> str:
		"""Read a sequence of chars until the next new line char in ascii."""
		ret = self._readUntil("\n", "A")
		if ret[-1] == "\r":
			ret = ret[-1]
		return ret

	@textLineA.setter
	def textLineA(self, text: str) -> None:
		"""Set a sequence of chars until the next new line char in ascii."""
		self.setbytearray(text)
		if isinstance(text, (int, float)) or text[-1] != "\n":
			self.setbytearray("\n")

	@property
	def textLineW(self) -> str:
		"""Read a sequence of chars until the next new line char in ucs-2."""
		ret = self._readUntil("\n", "W")
		if ret[-1] == "\r":
			ret = ret[-1]
		return ret

	@textLineW.setter
	def textLineW(self, text: str) -> None:
		"""Set a sequence of chars until the next new line char in ucs-2."""
		self.setbytearray(text)
		if isinstance(text, (int, float)) or text[-1] != "\n":
			self.setbytearray("\0\n")

	@property
	def textLineU(self) -> str:
		"""Read a sequence of chars until the next new line char in utf-8."""
		ret = self._readUntil("\n", "U")
		if ret[-1] == "\r":
			ret = ret[-1]
		return ret

	@textLineU.setter
	def textLineU(self, text: str) -> None:
		"""Set a sequence of chars until the next new line char in utf-8."""
		self.setbytearray(text)
		if isinstance(text, (int, float)) or text[-1] != "\n":
			self.setbytearray("\n")

	@property
	def cString(self) -> str:
		"""Read a sequence of chars until the next null byte."""
		return self._readUntil("\0", self.stringEncoding)

	@cString.setter
	def cString(self, text: str) -> None:
		"""Set a sequence of chars and add a null byte."""
		self.setbytearray(text)
		self.setbytearray("\0")

	@property
	def cStringA(self) -> str:
		"""Read a sequence of chars until the next null byte in ascii."""
		return self._readUntil("\0", "A")

	@cStringA.setter
	def cStringA(self, text: str) -> None:
		"""Set a sequence of chars and add a null byte in ascii."""
		self.setbytearray(text)
		self.setbytearray("\0")

	@property
	def cStringW(self) -> str:
		"""Read a sequence of chars until the next null byte in ucs-2."""
		return self._readUntil("\0", "W")

	@cStringW.setter
	def cStringW(self, text: str) -> None:
		"""Set a sequence of chars and add a null byte in ucs-2."""
		self.setbytearray(text)
		self.setbytearray("\0\0")

	@property
	def cStringU(self) -> str:
		"""Read a sequence of chars until the next null byte in utf-8."""
		return self._readUntil("\0", "U")

	@cStringU.setter
	def cStringU(self, text: str) -> None:
		"""Set a sequence of chars and add a null byte in utf-8."""
		self.setbytearray(text)
		self.setbytearray("\0")
