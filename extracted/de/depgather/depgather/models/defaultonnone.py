from typing import Any

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined


class DefaultOnNoneModel(BaseModel):
	@model_validator(mode="before")
	@classmethod
	def default_on_none(cls, values: Any) -> Any | dict[Any, Any]:
		if not isinstance(values, dict):
			return values

		result = dict(values)

		for name, field in cls.model_fields.items():
			if name in result and result[name] is None:
				if field.default_factory is not None:
					result[name] = field.default_factory()
				elif field.default is not None:
					result[name] = field.default

		return result

	@field_validator("*", mode="wrap")
	@classmethod
	def fallback_to_default(
		cls,
		value: Any,
		handler,
		info: ValidationInfo,
	) -> Any:
		try:
			return handler(value)
		except Exception:
			field: FieldInfo = cls.model_fields[info.field_name]

			if field.default_factory is not None:
				return field.default_factory()

			if field.default is not PydanticUndefined:
				return field.default

			raise
