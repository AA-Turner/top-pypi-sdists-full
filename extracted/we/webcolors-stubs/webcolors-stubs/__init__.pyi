# Stubs for webcolors
# https://github.com/ubernostrum/webcolors

# Copyright (c) 2020, Dominic Davis-Foster
# Copyright (c) 2008-2020, James Bennett
# BSD Licensed

# stdlib
from typing import Dict, NamedTuple, Pattern, Tuple, Union

__version__: str


def _reversedict(d: Dict) -> Dict: ...


HEX_COLOR_RE: Pattern[str]

HTML4: str = "html4"
CSS2: str = "css2"
CSS21: str = "css21"
CSS3: str = "css3"

SUPPORTED_SPECIFICATIONS: Tuple[str, str, str, str] = (HTML4, CSS2, CSS21, CSS3)

SPECIFICATION_ERROR_TEMPLATE: str

class IntegerRGB(NamedTuple):
	red: int
	green: int
	blue: int


class PercentRGB(NamedTuple):
	red: str
	green: str
	blue: str


class HTML5SimpleColor(NamedTuple):
	red: int
	green: int
	blue: int


IntTuple = Union[IntegerRGB, HTML5SimpleColor, Tuple[int, int, int]]
PercentTuple = Union[PercentRGB, Tuple[str, str, str]]

# Mappings of color names to normalized hexadecimal color values.
#################################################################

HTML4_NAMES_TO_HEX: Dict[str, str]

# CSS 2 used the same list as HTML 4.
CSS2_NAMES_TO_HEX: Dict[str, str]

# CSS 2.1 added orange.
CSS21_NAMES_TO_HEX: Dict[str, str]

# The CSS 3/SVG named colors.
CSS3_NAMES_TO_HEX: Dict[str, str]


# Mappings of normalized hexadecimal color values to color names.
#################################################################

HTML4_HEX_TO_NAMES: Dict[str, str]
CSS2_HEX_TO_NAMES: Dict[str, str]
CSS21_HEX_TO_NAMES: Dict[str, str]
CSS3_HEX_TO_NAMES: Dict[str, str]


# Normalization functions.
#################################################################

def normalize_hex(hex_value: str) -> str: ...


def _normalize_integer_rgb(value: int) -> int: ...


def normalize_integer_triplet(rgb_triplet: IntTuple) -> IntegerRGB: ...


def _normalize_percent_rgb(value: str) -> str: ...


def normalize_percent_triplet(rgb_triplet: PercentTuple) -> PercentRGB: ...


# Conversions from color names to various formats.
#################################################################

def name_to_hex(name: str, spec: str = CSS3) -> str: ...

def name_to_rgb(name: str, spec: str = CSS3) -> IntegerRGB: ...

def name_to_rgb_percent(name: str, spec: str = CSS3) -> PercentRGB: ...


# Conversions from hexadecimal color values to various formats.
#################################################################

def hex_to_name(hex_value: str, spec: str = CSS3) -> str: ...


def hex_to_rgb(hex_value: str) -> IntegerRGB: ...

def hex_to_rgb_percent(hex_value: str) -> PercentRGB: ...


# Conversions from  integer rgb() triplets to various formats.
#################################################################

def rgb_to_name(rgb_triplet: IntTuple, spec: str = CSS3) -> str: ...

def rgb_to_hex(rgb_triplet: IntTuple) -> str: ...

def rgb_to_rgb_percent(rgb_triplet: IntTuple) -> PercentRGB: ...


# Conversions from percentage rgb() triplets to various formats.
#################################################################

def rgb_percent_to_name(rgb_percent_triplet: PercentTuple, spec: str = CSS3) -> str: ...

def rgb_percent_to_hex(rgb_percent_triplet: PercentTuple) -> str: ...

def _percent_to_integer(percent: str) -> int: ...

def rgb_percent_to_rgb(rgb_percent_triplet: PercentTuple) -> IntegerRGB: ...


# HTML5 color algorithms.
#################################################################

def html5_parse_simple_color(input: str) -> HTML5SimpleColor: ...


def html5_serialize_simple_color(simple_color: IntTuple) -> str: ...


def html5_parse_legacy_color(input: str) -> HTML5SimpleColor: ...
