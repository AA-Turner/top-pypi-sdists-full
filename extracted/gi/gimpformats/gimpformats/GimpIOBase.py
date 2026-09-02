"""A specialized binary file base for Gimp files."""

from __future__ import annotations

import struct
from enum import Enum
from typing import Any

from gimpformats.binaryiotools import IO
from gimpformats.GimpParasites import GimpParasite
from gimpformats.GimpVectors import GimpVector
from gimpformats.utils import repr_indent_lines


def _prop_cmp(val: int, prop: ImageProperties | list[ImageProperties]) -> bool:
	if isinstance(prop, list):
		return any(_prop_cmp(val, p) for p in prop)
	return list(ImageProperties)[val] == prop


def camel_to_pascal_with_spaces(val: str) -> str:
	text = "".join([f" {char}" if char.isupper() else char for char in val])
	return text[0].upper() + text[1:]


class ColorMode(Enum):
	RGB = "RGB"
	Grayscale = "Grayscale"
	Indexed = "Indexed"


class Units(Enum):
	Inches = "Inches"
	Millimetres = "Millimetres"
	Points = "Points"
	Picas = "Picas"


class CompositeMode(Enum):
	Union = "Union"
	Clip_to_backdrop = "Clip to backdrop"
	Clip_to_layer = "Clip to layer"
	Intersection = "Intersection"


class CompositeSpace(Enum):
	RGB_linear = "RGB (linear)"
	RGB_perceptual = "RGB (perceptual)"
	LAB = "LAB"


class TagColor(Enum):
	None_Color = "None"
	Blue = "Blue"
	Green = "Green"
	Yellow = "Yellow"
	Orange = "Orange"
	Brown = "Brown"
	Red = "Red"
	Violet = "Violet"
	Gray = "Gray"


class CompressionMode(Enum):
	None_Compression = "None"
	RLE = "RLE"
	Zlib = "Zlib"
	Fractal = "Fractal"


class GimpBlendMode(Enum):
	NORMAL_LEGACY = "Normal (legacy)"
	DISSOLVE_LEGACY = "Dissolve (legacy)"
	BEHIND_LEGACY = "Behind (legacy)"
	MULTIPLY_LEGACY = "Multiply (legacy)"
	SCREEN_LEGACY = "Screen (legacy)"
	OLD_BROKEN_OVERLAY = "Old broken Overlay"
	DIFFERENCE_LEGACY = "Difference (legacy)"
	ADDITION_LEGACY = "Addition (legacy)"
	SUBTRACT_LEGACY = "Subtract (legacy)"
	DARKEN_ONLY_LEGACY = "Darken only (legacy)"
	LIGHTEN_ONLY_LEGACY = "Lighten only (legacy)"
	HUE_HSV_LEGACY = "Hue (HSV) (legacy)"
	SATURATION_HSV_LEGACY = "Saturation (HSV) (legacy)"
	COLOR_HSL_LEGACY = "Color (HSL) (legacy)"
	VALUE_HSV_LEGACY = "Value (HSV) (legacy)"
	DIVIDE_LEGACY = "Divide (legacy)"
	DODGE_LEGACY = "Dodge (legacy)"
	BURN_LEGACY = "Burn (legacy)"
	HARD_LIGHT_LEGACY = "Hard Light (legacy)"
	SOFT_LIGHT_LEGACY = "Soft light (legacy)"
	GRAIN_EXTRACT_LEGACY = "Grain extract (legacy)"
	GRAIN_MERGE_LEGACY = "Grain merge (legacy)"
	COLOR_ERASE_LEGACY = "Color erase (legacy)"
	OVERLAY = "Overlay"
	HUE_LCH = "Hue (LCH)"
	CHROMA_LCH = "Chroma (LCH)"
	COLOR_LCH = "Color (LCH)"
	LIGHTNESS_LCH = "Lightness (LCH)"
	NORMAL = "Normal"
	BEHIND = "Behind"
	MULTIPLY = "Multiply"
	SCREEN = "Screen"
	DIFFERENCE = "Difference"
	ADDITION = "Addition"
	SUBSTRACT = "Substract"
	DARKEN_ONLY = "Darken only"
	LIGHTEN_ONLY = "Lighten only"
	HUE_HSV = "Hue (HSV)"
	SATURATION_HSV = "Saturation (HSV)"
	COLOR_HSL = "Color (HSL)"
	VALUE_HSV = "Value (HSV)"
	DIVIDE = "Divide"
	DODGE = "Dodge"
	BURN = "Burn"
	HARD_LIGHT = "Hard light"
	SOFT_LIGHT = "Soft light"
	GRAIN_EXTRACT = "Grain extract"
	GRAIN_MERGE = "Grain merge"
	VIVID_LIGHT = "Vivid light"
	PIN_LIGHT = "Pin light"
	LINEAR_LIGHT = "Linear light"
	HARD_MIX = "Hard mix"
	EXCLUSION = "Exclusion"
	LINEAR_BURN = "Linear burn"
	LUMA_DARKEN_ONLY = "Luma/Luminance darken only"
	LUMA_LIGHTEN_ONLY = "Luma/Luminance lighten only"
	LUMINANCE = "Luminance"
	COLOR_ERASE = "Color erase"
	ERASE = "Erase"
	MERGE = "Merge"
	SPLIT = "Split"
	PASS_THROUGH = "Pass through"


class ImageProperties(Enum):
	PROP_END = 0
	PROP_COLORMAP = 1
	PROP_ACTIVE_LAYER = 2
	PROP_ACTIVE_CHANNEL = 3
	PROP_SELECTION = 4
	PROP_FLOATING_SELECTION = 5
	PROP_OPACITY = 6
	PROP_MODE = 7
	PROP_VISIBLE = 8
	PROP_LINKED = 9
	PROP_LOCK_ALPHA = 10
	PROP_APPLY_MASK = 11
	PROP_EDIT_MASK = 12
	PROP_SHOW_MASK = 13
	PROP_SHOW_MASKED = 14
	PROP_OFFSETS = 15
	PROP_COLOR = 16
	PROP_COMPRESSION = 17
	PROP_GUIDES = 18
	PROP_RESOLUTION = 19
	PROP_TATTOO = 20
	PROP_PARASITES = 21
	PROP_UNIT = 22
	PROP_PATHS = 23
	PROP_USER_UNIT = 24
	PROP_VECTORS = 25
	PROP_TEXT_LAYER_FLAGS = 26
	PROP_OLD_SAMPLE_POINTS = 27
	PROP_LOCK_CONTENT = 28
	PROP_GROUP_ITEM = 29
	PROP_ITEM_PATH = 30
	PROP_GROUP_ITEM_FLAGS = 31
	PROP_LOCK_POSITION = 32
	PROP_FLOAT_OPACITY = 33
	PROP_COLOR_TAG = 34
	PROP_COMPOSITE_MODE = 35
	PROP_COMPOSITE_SPACE = 36
	PROP_BLEND_SPACE = 37
	PROP_FLOAT_COLOR = 38
	PROP_SAMPLE_POINTS = 39
	PROP_NUM_PROPS = 40


class GimpIOBase:
	def __init__(self, parent: Any = None) -> None:
		self.parent = parent
		self.parasites: list[GimpParasite] = []
		self.guidelines: list[tuple[bool, int]] = []
		self.itemPath: list[int] | None = None
		self.vectors: list[GimpVector] = []
		self.colorMap: list[tuple[int, int, int]] = []
		self.userUnits: GimpUserUnits | None = None
		self.samplePoints: list[tuple[int, int]] = []
		self.selected: bool = False
		self.isSelection: bool = False
		self.selectionAttachedTo: int | None = None
		self.blendMode: GimpBlendMode = GimpBlendMode.ADDITION
		self.visible: bool = False
		self.isLinked: bool = False
		self.lockAlpha: bool = False
		self.applyMask: bool = False
		self.editingMask: bool = False
		self.showMask: bool = False
		self.showMasked: bool = False
		self.xOffset: int = 0
		self.yOffset: int = 0
		self.compression: CompressionMode = CompressionMode.None_Compression
		self.horizontalResolution = None
		self.verticalResolution = None
		self.uniqueId = None
		self.units: Units = Units.Inches
		self.textLayerFlags = None
		self.locked = None
		self.isGroup = None
		self.groupItemFlags: int = 0
		self.positionLocked: bool = False
		self.opacity: float = 1.0
		self.colorTag: TagColor = TagColor.Blue
		self.compositeMode: CompositeMode = CompositeMode.Union
		self.compositeSpace: CompositeSpace = CompositeSpace.RGB_linear
		self.blendSpace = None
		self.color = None
		self.vectorsVersion: int = 0
		self.activeVectorIndex: int = 0
		self.paths = []

	@property
	def pointerSize(self) -> int:
		"""Determine the size of the "pointer" datatype based on the document version.

		NOTE: prior to version 11, it was 32-bit,
			since then it is 64-bit, thus supporting
			larger image files
		"""
		if self.doc.version >= 11:
			return 64
		return 32

	def _pointerDecode(self, ioBuf: IO) -> int:
		if self.pointerSize == 64:
			return ioBuf.u64
		return ioBuf.u32

	def _pointerEncode(self, ptr: int, ioBuf: IO | None = None) -> bytearray:
		if ioBuf is None:
			ioBuf = IO()
		if self.pointerSize == 64:
			ioBuf.u64 = ptr
		else:
			ioBuf.u32 = ptr
		return ioBuf.data

	@property
	def doc(self) -> GimpIOBase:
		item = self
		while item.parent != item:
			item = item.parent
		return item

	@property
	def root(self) -> GimpIOBase:
		"""Get the root of the file object tree (Which is the same as self.doc)."""
		return self.doc

	@property
	def tattoo(self) -> Any | None:
		"""Gimp nomenclature for the item's unique id."""
		return self.uniqueId

	@tattoo.setter
	def tattoo(self, tattoo: Any | None) -> None:
		"""Gimp nomenclature for the item's unique id."""
		self.uniqueId = tattoo

	def _parasitesDecode(self, data: bytearray) -> int:
		"""Decode list of parasites."""
		index: int = 0
		self.parasites = []  # reset
		while index < len(data):
			parasite = GimpParasite()
			index = parasite.decode(data, index)
			self.parasites.append(parasite)
		return index

	def _parasitesEncode(self) -> bytearray:
		"""Encode list of parasites."""
		ioBuf = IO()
		for parasite in self.parasites:
			ioBuf.addbytearray(parasite.encode())
		return ioBuf.data

	def _guidelinesDecode(self, data: bytearray) -> None:
		"""Decode guidelines."""
		index: int = 0
		while index < len(data):
			position = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			isVertical = struct.unpack(">c", data[index : index + 1])[0] == 2
			index += 1
			self.guidelines.append((isVertical, position))

	def _itemPathDecode(self, data: bytearray) -> None:
		"""Decode item path."""
		index: int = 0
		path = []
		while index < len(data):
			pathElem = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			path.append(pathElem)
		self.itemPath = path

	def _vectorsDecode(self, data: bytearray) -> None:
		"""Decode vectors."""
		index: int = 0
		self.vectorsVersion = struct.unpack(">I", data[index : index + 4])[0]
		index += 4
		self.activeVectorIndex = struct.unpack(">I", data[index : index + 4])[0]
		index += 4
		numPaths = struct.unpack(">I", data[index : index + 4])[0]
		index += 4
		for _ in range(numPaths):
			gimpV = GimpVector(self)
			gimpV.decode(data)
			self.vectors.append(gimpV)

	@property
	def activeVector(self) -> GimpVector:
		"""Get the vector that is currently active."""
		return self.vectors[self.activeVectorIndex]

	@property
	def expanded(self) -> bool:
		"""Is the group layer expanded."""
		return self.groupItemFlags & 0x00000001 > 0

	@expanded.setter
	def expanded(self, expanded: bool) -> None:
		"""Is the group layer expanded."""
		if expanded:
			self.groupItemFlags |= 0x00000001
		else:
			self.groupItemFlags &= ~0x00000001

	def _colormapDecode(self, data: bytearray | IO, index: int = 0) -> None:
		"""_colormapDecode_.

		:param data: can be bytearray or an IO object

		decode colormap/palette
		"""
		ioObj = None
		if isinstance(data, IO):
			ioObj = data
			index = data.index
			data = data.data
		_ = struct.unpack(">I", data[0:4])[0]  # number of colors
		index += 4
		colors = []
		while index < len(data):
			red = data[index]
			index += 1
			green = data[index]
			index += 1
			blue = data[index]
			index += 1
			colors.append((red, green, blue))
		self.colorMap = colors
		if ioObj is not None:
			ioObj.index = index

	def _userUnitsDecode(self, data: bytearray) -> None:
		"""Decode a set of user-defined measurement units."""
		userUnits = GimpUserUnits()
		userUnits.decode(data)
		self.userUnits = userUnits

	def _samplePointsDecode(self, data: bytearray) -> None:
		"""Decode a series of points."""
		index: int = 0
		samplePoints = []
		while index < len(data):
			x = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			y = struct.unpack(">I", data[index : index + 4])[0]
			index += 4
			samplePoints.append((x, y))
		self.samplePoints = samplePoints

	def _propertyDecode(self, prop: int, data: bytearray) -> int:
		"""Decode a single property.

		Many properties are in the form
		prop: one of PROP_
		lengthOfData: 4
		data: varies but is often ioBuf.32 or ioBuf.boolean
		"""
		ioBuf = IO(data, boolSize=32)
		if _prop_cmp(prop, ImageProperties.PROP_COLORMAP):
			self._colormapDecode(ioBuf)
		elif _prop_cmp(
			prop, [ImageProperties.PROP_ACTIVE_LAYER, ImageProperties.PROP_ACTIVE_CHANNEL]
		):
			self.selected = True
		elif _prop_cmp(prop, ImageProperties.PROP_SELECTION):
			self.isSelection = True
		elif _prop_cmp(prop, ImageProperties.PROP_FLOATING_SELECTION):
			self.selectionAttachedTo = ioBuf.u32
		elif _prop_cmp(prop, ImageProperties.PROP_OPACITY):
			self.opacity = ioBuf.u32
		elif _prop_cmp(prop, ImageProperties.PROP_MODE):
			self.blendMode = list(GimpBlendMode)[ioBuf.u32]
		elif _prop_cmp(prop, ImageProperties.PROP_VISIBLE):
			self.visible = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_LINKED):
			self.isLinked = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_LOCK_ALPHA):
			self.lockAlpha = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_APPLY_MASK):
			self.applyMask = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_EDIT_MASK):
			self.editingMask = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_SHOW_MASK):
			self.showMask = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_SHOW_MASKED):
			self.showMasked = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_OFFSETS):
			self.xOffset = ioBuf.i32
			self.yOffset = ioBuf.i32
		elif _prop_cmp(prop, ImageProperties.PROP_COLOR):
			red = ioBuf.byte
			green = ioBuf.byte
			blue = ioBuf.byte
			self.color = [red, green, blue]
		elif _prop_cmp(prop, ImageProperties.PROP_COMPRESSION):
			self.compression = list(CompressionMode)[int(ioBuf.byte)]
		elif _prop_cmp(prop, ImageProperties.PROP_GUIDES):
			self._guidelinesDecode(data)
		elif _prop_cmp(prop, ImageProperties.PROP_RESOLUTION):
			self.horizontalResolution = ioBuf.float32
			self.verticalResolution = ioBuf.float32
		elif _prop_cmp(prop, ImageProperties.PROP_TATTOO):
			self.uniqueId = data.hex()
		elif _prop_cmp(prop, ImageProperties.PROP_PARASITES):
			self._parasitesDecode(data)
		elif _prop_cmp(prop, ImageProperties.PROP_UNIT):
			self.units = ioBuf.u32
		elif _prop_cmp(prop, ImageProperties.PROP_PATHS):
			_numPaths = ioBuf.u32
			"""
			for _ in range(numPaths):
				nRead, path = self._pathDecode_(data[index:])
				self.paths.append(path)
				index += nRead
			"""
		elif _prop_cmp(prop, ImageProperties.PROP_USER_UNIT):
			self._userUnitsDecode(data)
		elif _prop_cmp(prop, ImageProperties.PROP_VECTORS):
			pass
			# self._vectorsDecode_(data)
		elif _prop_cmp(prop, ImageProperties.PROP_TEXT_LAYER_FLAGS):
			if isinstance(data, bytearray):
				self.textLayerFlags = int.from_bytes(data, byteorder="big")
			else:
				self.textLayerFlags = int(data)
		elif _prop_cmp(prop, ImageProperties.PROP_OLD_SAMPLE_POINTS):
			msg = "ERR: old sample points structure not supported"
			raise RuntimeError(msg)
		elif _prop_cmp(prop, ImageProperties.PROP_LOCK_CONTENT):
			self.locked = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_GROUP_ITEM):
			self.isGroup = True
		elif _prop_cmp(prop, ImageProperties.PROP_ITEM_PATH):
			self._itemPathDecode(data)
		elif _prop_cmp(prop, ImageProperties.PROP_GROUP_ITEM_FLAGS):
			self.groupItemFlags = ioBuf.u32
		elif _prop_cmp(prop, ImageProperties.PROP_LOCK_POSITION):
			self.positionLocked = ioBuf.boolean
		elif _prop_cmp(prop, ImageProperties.PROP_FLOAT_OPACITY):
			self.opacity = ioBuf.float32
		elif _prop_cmp(prop, ImageProperties.PROP_COLOR_TAG):
			self.colorTag = ioBuf.u32
		elif _prop_cmp(prop, ImageProperties.PROP_COMPOSITE_MODE):
			self.compositeMode = ioBuf.i32
		elif _prop_cmp(prop, ImageProperties.PROP_COMPOSITE_SPACE):
			self.compositeSpace = ioBuf.i32
		elif _prop_cmp(prop, ImageProperties.PROP_BLEND_SPACE):
			self.blendSpace = ioBuf.u32
		elif _prop_cmp(prop, ImageProperties.PROP_FLOAT_COLOR):
			red = ioBuf.float32
			green = ioBuf.float32
			blue = ioBuf.float32
			self.color = [red, green, blue]
		elif _prop_cmp(prop, ImageProperties.PROP_SAMPLE_POINTS):
			self._samplePointsDecode(data)
		else:
			msg = f"Unknown property id {prop}"
			raise RuntimeError(msg)
		return ioBuf.index

	def _propertyEncode(self, prop: int) -> bytearray:
		"""Encode a single property.

		Many properties are in the form
		prop: one of PROP_
		lengthOfData: 4
		data: varies but is often ioBuf.32 or ioBuf.boolean

		If the property is the same as the default, or not specified, returns empty array
		"""
		ioBuf = IO(boolSize=32)
		if _prop_cmp(prop, ImageProperties.PROP_COLORMAP):
			if self.colorMap is not None and self.colorMap:
				ioBuf.u32 = ImageProperties.PROP_COLORMAP
				# ioBuf.addbytearray(self._colormapEncode_())
		elif _prop_cmp(
			prop, [ImageProperties.PROP_ACTIVE_LAYER, ImageProperties.PROP_ACTIVE_CHANNEL]
		):
			if self.selected is not None and self.selected:
				ioBuf.u32 = ImageProperties.PROP_ACTIVE_LAYER.value

		elif _prop_cmp(prop, ImageProperties.PROP_SELECTION):
			if self.isSelection is not None and self.isSelection:
				ioBuf.u32 = ImageProperties.PROP_SELECTION.value
		elif _prop_cmp(prop, ImageProperties.PROP_FLOATING_SELECTION):
			if self.selectionAttachedTo is not None:
				ioBuf.u32 = ImageProperties.PROP_FLOATING_SELECTION.value
				ioBuf.u32 = self.selectionAttachedTo
		elif _prop_cmp(prop, ImageProperties.PROP_OPACITY):
			if self.opacity is not None and not isinstance(self.opacity, float):
				ioBuf.u32 = ImageProperties.PROP_OPACITY.value
				ioBuf.u32 = self.opacity
		elif _prop_cmp(prop, ImageProperties.PROP_MODE):
			if self.blendMode is not None:
				ioBuf.u32 = ImageProperties.PROP_MODE.value
				ioBuf.u32 = self.blendMode
		elif _prop_cmp(prop, ImageProperties.PROP_VISIBLE):
			if self.visible is not None:
				ioBuf.u32 = ImageProperties.PROP_VISIBLE.value
				ioBuf.boolean = self.visible
		elif _prop_cmp(prop, ImageProperties.PROP_LINKED):
			if self.isLinked is not None and self.isLinked:
				ioBuf.u32 = ImageProperties.PROP_LINKED.value
				ioBuf.boolean = self.isLinked
		elif _prop_cmp(prop, ImageProperties.PROP_LOCK_ALPHA):
			if self.lockAlpha is not None and self.lockAlpha:
				ioBuf.u32 = ImageProperties.PROP_LOCK_ALPHA.value
				ioBuf.boolean = self.lockAlpha
		elif _prop_cmp(prop, ImageProperties.PROP_APPLY_MASK):
			if self.applyMask is not None:
				ioBuf.u32 = ImageProperties.PROP_APPLY_MASK.value
				ioBuf.boolean = self.applyMask
		elif _prop_cmp(prop, ImageProperties.PROP_EDIT_MASK):
			if self.editingMask is not None and self.editingMask:
				ioBuf.u32 = ImageProperties.PROP_EDIT_MASK.value
				ioBuf.boolean = self.editingMask
		elif _prop_cmp(prop, ImageProperties.PROP_SHOW_MASK):
			if self.showMask is not None and self.showMask:
				ioBuf.u32 = ImageProperties.PROP_SHOW_MASK.value
				ioBuf.boolean = self.showMask
		elif _prop_cmp(prop, ImageProperties.PROP_SHOW_MASKED):
			if self.showMasked is not None:
				ioBuf.u32 = ImageProperties.PROP_SHOW_MASKED.value
				ioBuf.boolean = self.showMasked
		elif _prop_cmp(prop, ImageProperties.PROP_OFFSETS):
			if self.xOffset is not None and self.yOffset is not None:
				ioBuf.u32 = ImageProperties.PROP_OFFSETS.value
				ioBuf.i32 = self.xOffset
				ioBuf.i32 = self.yOffset
		elif _prop_cmp(prop, ImageProperties.PROP_COLOR):
			if (
				self.color is not None
				and not isinstance(self.color[0], float)
				and not isinstance(self.color[1], float)
				and not isinstance(self.color[2], float)
			):
				ioBuf.u32 = ImageProperties.PROP_COLOR.value
				ioBuf.byte = self.color[0]
				ioBuf.byte = self.color[1]
				ioBuf.byte = self.color[2]
		elif _prop_cmp(prop, ImageProperties.PROP_COMPRESSION):
			if self.compression is not None:
				ioBuf.u32 = ImageProperties.PROP_COMPRESSION.value
				ioBuf.u32 = self.compression
		elif _prop_cmp(prop, ImageProperties.PROP_GUIDES):
			if self.guidelines is not None and self.guidelines:
				pass
				# ioBuf.u32 = ImageProperties.PROP_GUIDES
				# ioBuf.addbytearray(self._guidelinesEncode_())
		elif _prop_cmp(prop, ImageProperties.PROP_RESOLUTION):
			if self.horizontalResolution is not None and self.verticalResolution is not None:
				ioBuf.u32 = ImageProperties.PROP_RESOLUTION.value
				ioBuf.u32 = int(self.horizontalResolution)
				ioBuf.i32 = int(self.verticalResolution)
		elif _prop_cmp(prop, ImageProperties.PROP_TATTOO):
			if self.uniqueId is not None:
				ioBuf.u32 = int(self.uniqueId, 16)
		elif _prop_cmp(prop, ImageProperties.PROP_PARASITES):
			if self.parasites is not None and self.parasites:
				ioBuf.u32 = ImageProperties.PROP_PARASITES.value
				ioBuf.addbytearray(self._parasitesEncode())
		elif _prop_cmp(prop, ImageProperties.PROP_UNIT):
			if self.units is not None:
				ioBuf.u32 = ImageProperties.PROP_UNIT.value
				ioBuf.u32 = self.units
		elif _prop_cmp(prop, ImageProperties.PROP_PATHS):
			if self.paths is not None and self.paths:
				# ioBuf.u32 = ImageProperties.PROP_PATHS
				# ioBuf.u32 = len(self.paths)
				"""
				for path in self.paths:
					ioBuf.append(self._pathEncode_(path))
				"""
		elif _prop_cmp(prop, ImageProperties.PROP_USER_UNIT):
			if self.userUnits is not None:
				pass
				# ioBuf.u32 = ImageProperties.PROP_USER_UNIT
				# ioBuf.addbytearray(self._userUnitsEncode_())
		elif _prop_cmp(prop, ImageProperties.PROP_VECTORS):
			if self.vectors is not None and self.vectors:
				pass
				# ioBuf.u32 = ImageProperties.PROP_VECTORS
				# ioBuf.addbytearray(self._vectorsEncode_())
		elif _prop_cmp(prop, ImageProperties.PROP_TEXT_LAYER_FLAGS):
			if self.textLayerFlags is not None:
				ioBuf.u32 = ImageProperties.PROP_TEXT_LAYER_FLAGS.value
				ioBuf.u32 = self.textLayerFlags
		elif _prop_cmp(prop, ImageProperties.PROP_OLD_SAMPLE_POINTS):
			pass
		elif _prop_cmp(prop, ImageProperties.PROP_LOCK_CONTENT):
			if self.locked is not None and self.locked:
				ioBuf.u32 = ImageProperties.PROP_LOCK_CONTENT.value
				ioBuf.boolean = self.locked
		elif _prop_cmp(prop, ImageProperties.PROP_GROUP_ITEM):
			if self.isGroup is not None and self.isGroup:
				ioBuf.u32 = ImageProperties.PROP_GROUP_ITEM.value
		elif _prop_cmp(prop, ImageProperties.PROP_ITEM_PATH):
			if self.itemPath is not None:
				pass
				# ioBuf.u32 = ImageProperties.PROP_ITEM_PATH
				# ioBuf.addbytearray(self._itemPathEncode_())
		elif _prop_cmp(prop, ImageProperties.PROP_GROUP_ITEM_FLAGS):
			if self.groupItemFlags is not None:
				ioBuf.u32 = ImageProperties.PROP_GROUP_ITEM_FLAGS.value
				ioBuf.u32 = self.groupItemFlags
		elif _prop_cmp(prop, ImageProperties.PROP_LOCK_POSITION):
			if self.positionLocked is not None and self.positionLocked:
				ioBuf.u32 = ImageProperties.PROP_LOCK_POSITION.value
				ioBuf.boolean = self.positionLocked
		elif _prop_cmp(prop, ImageProperties.PROP_FLOAT_OPACITY):
			if self.opacity is not None and isinstance(self.opacity, float):
				ioBuf.u32 = ImageProperties.PROP_FLOAT_OPACITY.value
				ioBuf.float32 = self.opacity
		elif _prop_cmp(prop, ImageProperties.PROP_COLOR_TAG):
			if self.colorTag is not None:
				ioBuf.u32 = ImageProperties.PROP_COLOR_TAG.value
				ioBuf.u32 = self.colorTag
		elif _prop_cmp(prop, ImageProperties.PROP_COMPOSITE_MODE):
			if self.compositeMode is not None:
				ioBuf.u32 = ImageProperties.PROP_COMPOSITE_MODE.value
				ioBuf.i32 = self.compositeMode
		elif _prop_cmp(prop, ImageProperties.PROP_COMPOSITE_SPACE):
			if self.compositeSpace is not None:
				ioBuf.u32 = ImageProperties.PROP_COMPOSITE_SPACE.value
				ioBuf.i32 = self.compositeSpace
		elif _prop_cmp(prop, ImageProperties.PROP_BLEND_SPACE):
			if self.blendSpace is not None:
				ioBuf.u32 = ImageProperties.PROP_BLEND_SPACE.value
				ioBuf.u32 = self.blendSpace
		elif _prop_cmp(prop, ImageProperties.PROP_FLOAT_COLOR):
			if (
				self.color is not None
				and isinstance(self.color[0], float)
				and isinstance(self.color[1], float)
				and isinstance(self.color[2], float)
			):
				ioBuf.u32 = ImageProperties.PROP_FLOAT_COLOR.value
				ioBuf.float32 = self.color[0]
				ioBuf.float32 = self.color[1]
				ioBuf.float32 = self.color[2]
		elif _prop_cmp(prop, ImageProperties.PROP_SAMPLE_POINTS):
			if self.samplePoints is not None and self.samplePoints:
				pass
				# ioBuf.u32 = ImageProperties.PROP_SAMPLE_POINTS
				# self.addbytearray(self._samplePointsEncode_())
		else:
			msg = f"Unknown property id {prop}"
			raise RuntimeError(msg)
		return ioBuf.data

	def _propertiesDecode(self, ioBuf: IO) -> int:
		"""Decode a list of properties."""
		while True:
			try:
				prop = ioBuf.u32
				dataLength = ioBuf.u32
			except struct.error:  # end of data, so that's that.
				break
			if prop == 0:
				break
			self._propertyDecode(prop, ioBuf.getbytearray(dataLength))
		return ioBuf.index

	def _propertiesEncode(self) -> bytearray:
		"""Encode a list of properties."""
		ioBuf = IO()
		for prop in range(1, ImageProperties.PROP_NUM_PROPS.value):
			moData = self._propertyEncode(prop)
			if moData:
				ioBuf.addbytearray(moData)
		return ioBuf.data

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.__repr__()

	def __repr__(self) -> str:
		"""Get a textual representation of this object."""
		return (
			f"<GimpIOBase "
			f"uniqueId={self.uniqueId!r}, itemPath={self.itemPath!r}, "
			f"visible={self.visible}, opacity={self.opacity:.2f}, blendMode={self.blendMode}, "
			f"xOffset={self.xOffset}, yOffset={self.yOffset}, positionLocked={self.positionLocked}, "
			f"isGroup={self.isGroup}, groupItemFlags={self.groupItemFlags}, "
			f"locked={self.locked}, lockAlpha={self.lockAlpha}, editingMask={self.editingMask}>"
		)

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		attrs = [
			"userUnits",
			"selected",
			"isSelection",
			"selectionAttachedTo",
			"blendMode",
			"visible",
			"isLinked",
			"lockAlpha",
			"applyMask",
			"editingMask",
			"showMask",
			"showMasked",
			"xOffset",
			"yOffset",
			"compression",
			"horizontalResolution",
			"verticalResolution",
			"uniqueId",
			"units",
			"textLayerFlags",
			"locked",
			"isGroup",
			"groupItemFlags",
			"positionLocked",
			"opacity",
			"colorTag",
			"compositeMode",
			"compositeSpace",
			"blendSpace",
			"color",
			"vectorsVersion",
			"activeVectorIndex",
			"paths",
		]

		ret = [
			f"{camel_to_pascal_with_spaces(attr)}: {getattr(self, attr)}"
			for attr in attrs
			if getattr(self, attr) is not None
		]

		if self.xOffset is not None:
			ret.append(f"Offset: {self.xOffset} x {self.yOffset}")
		if self.horizontalResolution is not None:
			res = str(self.horizontalResolution) + f"ppi x {self.verticalResolution}ppi"
			ret.append(f"Resolution: {res}")
		if self.color is not None:
			ret.append(f"Color: ({self.color[0]}, {self.color[1]}, {self.color[2]})")
		if self.userUnits is not None:
			ret.append("User Units:")
			ret.append(self.userUnits.full_repr(indent=indent + 1))
		if self.parasites:
			ret.append("Parasites:")
			for item in self.parasites:
				ret.append(item.__repr__())
		if self.guidelines:
			ret.append("Guidelines:")
			for item in self.guidelines:
				ret.append(item.__repr__())
		if self.samplePoints:
			ret.append("Sample Points:")
			for item in self.samplePoints:
				ret.append(f"({item[0]},{item[1]})")
		if self.vectors:
			ret.append("Vectors:")
			for item in self.vectors:
				ret.append(item.full_repr(indent=indent + 1))
		if self.colorMap:
			ret.append("Color Map:")
			for i, color in enumerate(self.colorMap):
				ret.append(str(i) + f": ({color[0]},{color[1]},{color[2]})")
		return repr_indent_lines(indent, ret)


class GimpUserUnits:
	"""User-defined measurement units."""

	def __init__(self) -> None:
		self.factor: int = 0
		self.numDigits: int = 0
		self.id = ""
		self.symbol = ""
		self.abbrev = ""
		self.sname = ""
		self.pname = ""

	def decode(self, data: bytearray, index: int = 0) -> int:
		"""Decode a byte buffer.

		Args:
		----
			data (bytearray): data buffer to decode
			index (int, optional): index within the buffer to start at]. Defaults to 0.

		Returns:
		-------
			int: offset

		"""
		ioBuf = IO(data, index)
		self.factor = ioBuf.float32
		self.numDigits = ioBuf.u32
		self.id = ioBuf.sz754
		self.symbol = ioBuf.sz754
		self.abbrev = ioBuf.sz754
		self.sname = ioBuf.sz754
		self.pname = ioBuf.sz754
		return ioBuf.index

	def encode(self) -> bytearray:
		"""Convert this object to raw bytearray."""
		ioBuf = IO()
		ioBuf.float32 = self.factor
		ioBuf.u32 = self.numDigits
		ioBuf.sz754 = self.id
		ioBuf.sz754 = self.symbol
		ioBuf.sz754 = self.abbrev
		ioBuf.sz754 = self.sname
		ioBuf.sz754 = self.pname
		return ioBuf.data

	def __str__(self) -> str:
		"""Get a textual representation of this object."""
		return self.full_repr()

	def full_repr(self, indent: int = 0) -> str:
		"""Get a textual representation of this object."""
		ret = []
		ret.append(f"Factor: {self.factor}")
		ret.append(f"Num Digits: {self.numDigits}")
		ret.append(f"ID: {self.id}")
		ret.append(f"Symbol: {self.symbol}")
		ret.append(f"Abbreviation: {self.abbrev}")
		ret.append(f"Singular Name: {self.sname}")
		ret.append(f"Plural Name: {self.pname}")
		return repr_indent_lines(indent, ret)
