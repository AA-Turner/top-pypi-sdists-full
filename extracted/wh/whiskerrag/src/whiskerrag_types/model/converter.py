import json
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, Generic, List, Type, TypeVar, Union, get_args, get_origin
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class GenericConverter(Generic[T]):
    """
    A generic model converter that supports any Pydantic BaseModel subclass.
    """

    def __init__(self, model_class: Type[T]):
        self.model_class = model_class
        self.field_types = self._get_field_type_info(model_class)

    @staticmethod
    @lru_cache
    def _get_field_type_info(model_class: Type[BaseModel]) -> Dict[str, Any]:
        """Retrieve type information for model fields (with caching optimization)."""
        return {
            field_name: field_info.annotation
            for field_name, field_info in model_class.model_fields.items()
        }

    def to_db_value(self, value: Any, field_type: Any = None) -> Any:
        """Convert Python/Pydantic values to database values."""
        if value is None:
            return None

        # Handle BaseModel
        if isinstance(value, BaseModel):
            return json.dumps(value.model_dump())

        # Handle Enums
        if isinstance(value, Enum):
            return value.value

        # Handle UUIDs
        if isinstance(value, UUID):
            return str(value)

        # Handle datetime
        if isinstance(value, datetime):
            return value.isoformat() if value.tzinfo else value

        # Handle dicts and lists
        if isinstance(value, (dict, list)):
            return json.dumps(value)

        return value

    def from_db_value(self, value: Any, target_type: Type) -> Any:
        """Convert database values to Python/Pydantic types."""
        if value is None:
            return None

        # Handle Optional/Union types
        if get_origin(target_type) in (Union, type(None)):
            types = [t for t in get_args(target_type) if t is not type(None)]
            if len(types) == 1:
                target_type = types[0]
            else:
                # Handle union types
                return self._handle_union_type(value, types)

        # Handle string JSON
        if isinstance(value, str):
            try:
                parsed_value = json.loads(value)
                if issubclass(target_type, BaseModel):
                    return target_type(**parsed_value)
                if target_type in (dict, list):
                    return parsed_value
            except (json.JSONDecodeError, ValueError):
                pass

        # Handle Enums
        if isinstance(value, (str, int)) and issubclass(target_type, Enum):
            try:
                return target_type(value)
            except ValueError:
                pass

        # Handle UUIDs
        if isinstance(value, str) and target_type == UUID:
            try:
                return UUID(value)
            except ValueError:
                pass

        return value

    def _handle_union_type(self, value: Any, types: List[Type]) -> Any:
        """Handle union types."""
        if isinstance(value, str):
            try:
                parsed_value = json.loads(value)
                # Try each possible type
                for t in types:
                    if issubclass(t, BaseModel):
                        try:
                            return t(**parsed_value)
                        except Exception:
                            continue
                return parsed_value
            except json.JSONDecodeError:
                pass
        return value

    def to_db_dict(self, model: T) -> Dict[str, Any]:
        """Convert a model to a database dictionary."""
        data = model.model_dump(exclude_unset=True)
        return {
            key: self.to_db_value(value, self.field_types.get(key))
            for key, value in data.items()
        }

    def from_db_dict(self, db_data: Dict[str, Any]) -> T:
        """Convert a database dictionary to a model."""
        converted_data = {}
        for field_name, value in db_data.items():
            if field_name in self.field_types:
                target_type = self.field_types[field_name]
                converted_data[field_name] = self.from_db_value(value, target_type)
            else:
                converted_data[field_name] = value

        return self.model_class(**converted_data)

    def batch_to_db_dict(self, models: List[T]) -> List[Dict[str, Any]]:
        """Batch convert models to database dictionaries."""
        return [self.to_db_dict(model) for model in models]

    def batch_from_db_dict(self, db_data_list: List[Dict[str, Any]]) -> List[T]:
        """Batch convert database dictionaries to models."""
        return [self.from_db_dict(data) for data in db_data_list]
