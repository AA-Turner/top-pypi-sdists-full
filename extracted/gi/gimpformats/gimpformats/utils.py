from __future__ import annotations

from io import BytesIO
from pathlib import Path


def fileOpen(file: BytesIO | str | Path) -> tuple[str, bytes]:
	"""Load a file.

	:param fileName: can be a file name or a file-like object
	"""
	if isinstance(file, BytesIO):
		with file:
			return file.name, file.read()
	pth = Path(file)
	return pth.name, pth.read_bytes()


def save(data: bytearray | bytes, file: BytesIO | str | Path) -> None:
	"""Save this gimp image to a file."""
	if isinstance(file, BytesIO):
		with file:
			file.write(data)
		return
	pth = Path(file)
	pth.write_bytes(data)


def repr_indent_lines(indent: int, lines: list[str]) -> str:
	indentstr = indent * "\t"
	return (indentstr) + ((f"\n{indentstr}").join(lines))
