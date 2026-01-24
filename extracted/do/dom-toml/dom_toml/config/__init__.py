#!/usr/bin/env python3
#
#  __init__.py
"""
Nested configuration parsed from a TOML file.

.. extras-require:: config
	:pyproject:

.. versionadded:: 2.2.0
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import json
import re
from typing import Any, Callable, Dict, Mapping, Type, TypeVar, Union

# 3rd party
import attrs  # nodep
import tomli_w  # nodep
from typing_extensions import Self  # nodep

# this package
import dom_toml

__all__ = ("Config", "subtable_field", "to_kebab_case", "table_name")

_C = TypeVar("_C", bound="Config")


def subtable_field(submethod_type: Type[_C]) -> _C:
	"""
	Attrs field for a nested table.

	:param submethod_type: The :class:`~.Config` for the table.
	"""

	def on_setattr(inst: object, attr: attrs.Attribute, value: Any) -> _C:
		return submethod_type._coerce(value)

	# Actually returns attr.Attribute, but mypy doesn't like it
	return attrs.field(factory=submethod_type, converter=submethod_type._coerce, on_setattr=on_setattr)


_case_boundary_re = re.compile(r"([a-z])([A-Z])")
_single_letters_re = re.compile(r"([A-Z]|\d)([A-Z])([a-z])")
_underscore_boundary_re = re.compile(r'(\S)(_)(\S)')


def to_kebab_case(value: Union[str, Type["Config"], "Config"]) -> str:
	"""
	Convert the given string into ``kebab-case``.

	:param value:

	:rtype:

	.. versionadded:: 2.3.0
	"""

	if isinstance(value, str):
		pass
	elif isinstance(value, Config):
		value = getattr(value, "table_name", value.__class__.__name__)
	elif value is Config or (isinstance(value, type) and issubclass(value, Config)):
		value = getattr(value, "table_name", value.__name__)

	# Matches VSCode behaviour
	case_boundary = _case_boundary_re.findall(value)
	single_letters = _single_letters_re.findall(value)
	underscore_boundary = _underscore_boundary_re.findall(value)

	if not case_boundary and not single_letters and not underscore_boundary:
		return value.lower()

	value = _case_boundary_re.sub(r"\1-\2", value)
	value = _single_letters_re.sub(r"\1-\2\3", value)
	value = _underscore_boundary_re.sub(r"\1-\3", value)

	return value.lower()


def table_name(name: str) -> Callable[[Type[_C]], Type[_C]]:
	"""
	Decorator to override the table name on a :class:`~.Config` class.

	:param name: The new table name.

	:rtype:

	.. versionadded:: 2.3.0
	"""

	def deco(config_class: Type[_C]) -> Type[_C]:
		config_class.table_name = name  # type: ignore[attr-defined]
		return config_class

	return deco


@attrs.define
class Config:
	"""
	Configuration parsed from a TOML file.
	"""

	@classmethod
	def from_dict(cls: Type[Self], config: Mapping[str, Any]) -> Self:
		"""
		Construct a :class:`~.Config` from a dictionary or TOML table.

		:param config:
		"""

		return cls(**config)

	def to_dict(self) -> Dict[str, Any]:
		"""
		Convert a :class:`~.Config` to a dictionary.
		"""

		return attrs.asdict(self, recurse=True)

	@classmethod
	def from_toml(cls: Type[Self], toml_string: str) -> Self:
		"""
		Parse a :class:`~.Config` from a TOML string.

		:param toml_string:
		"""

		parsed_toml = dom_toml.loads(toml_string)
		return cls(**parsed_toml[to_kebab_case(cls)])

	@classmethod
	def from_json(cls: Type[Self], json_string: str) -> Self:
		"""
		Parse a :class:`~.Config` from a JSON string.

		:param json_string:
		"""

		parsed_json = json.loads(json_string)
		return cls(**parsed_json[to_kebab_case(cls)])

	def to_toml(self) -> str:
		"""
		Convert a :class:`~.Config` to a TOML string.
		"""

		return tomli_w.dumps({to_kebab_case(self): self.to_dict()})

	@classmethod
	def _coerce(cls: Type[Self], config: Any) -> Self:
		if isinstance(config, cls):
			return config
		elif isinstance(config, Mapping):
			return cls(**config)
		else:

			class_name = cls.__name__
			if class_name[0] in "aeiouAEIOU":
				raise TypeError(f"Cannot convert {type(config).__name__} to an {class_name}")
			# TODO: edge cases
			else:
				raise TypeError(f"Cannot convert {type(config).__name__} to a {class_name}")
