# (c) Copyright 2018 Palantir Technologies Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .._lib import (
    ConjureBeanType,
    ConjureEnumType,
    ConjureUnionType,
    DecodableType,
    BinaryType,
    OptionalTypeWrapper,
    DictType,
    ListType,
    OptionalType,
)
from typing import Optional, Type, Union, get_origin, get_args
from typing import Dict, Any, List
import inspect
import json

NoneType = type(None)


class ConjureDecoder(object):
    """Decodes json into a conjure object"""

    @classmethod
    def decode_conjure_bean_type(
        cls, obj, conjure_type, return_none_for_unknown_union_types=False
    ):
        """Decodes json into a conjure bean type (a plain bean, not enum
        or union).

        Args:
            obj: the json object to decode
            conjure_type: a class object which is the bean type
                we're decoding into
            return_none_for_unknown_union_types: if set to True, returns None
                instead of raising an exception when an unknown union type is
                encountered
        Returns:
            A instance of a bean of type conjure_type.
        """
        deserialized: Dict[str, Any] = {}
        for (
            python_arg_name,
            field_definition,
        ) in conjure_type._fields().items():
            field_identifier = field_definition.identifier

            if field_identifier not in obj or obj[field_identifier] is None:
                cls.check_null_field(
                    obj, deserialized, python_arg_name, field_definition
                )
            else:
                value = obj[field_identifier]
                field_type = field_definition.field_type
                deserialized[python_arg_name] = cls.do_decode(
                    value, field_type, return_none_for_unknown_union_types
                )
        return conjure_type(**deserialized)

    @classmethod
    def check_null_field(
        cls, obj, deserialized, python_arg_name, field_definition
    ):
        type_origin = get_origin(field_definition.field_type)
        if isinstance(field_definition.field_type, ListType):
            deserialized[python_arg_name] = []
        elif isinstance(field_definition.field_type, DictType):
            deserialized[python_arg_name] = {}
        elif isinstance(field_definition.field_type, OptionalType):
            deserialized[python_arg_name] = None
        elif type_origin is OptionalTypeWrapper:
            deserialized[python_arg_name] = None
        elif type_origin is list:
            deserialized[python_arg_name] = []
        elif type_origin is dict:
            deserialized[python_arg_name] = {}
        else:
            raise Exception(
                "field {} not found in object {}".format(
                    field_definition.identifier, obj
                )
            )

    @classmethod
    def decode_conjure_union_type(
        cls, obj, conjure_type, return_none_for_unknown_union_types=False
    ):
        """Decodes json into a conjure union type.

        Args:
            obj: the json object to decode
            conjure_type: a class object which is the union type
                we're decoding into
            return_none_for_unknown_union_types: if set to True, returns None
                instead of raising an exception when an unknown union type is
                encountered
        Returns:
            An instance of type conjure_type.
        """
        type_of_union: str = obj["type"]
        for attr, conjure_field in conjure_type._options().items():
            if conjure_field.identifier == type_of_union:
                attribute = attr
                conjure_field_definition = conjure_field
                break
        else:
            if return_none_for_unknown_union_types:
                return None
            else:
                raise ValueError(
                    "unknown union type {0} for {1}".format(
                        type_of_union, conjure_type
                    )
                )

        deserialized: Dict[str, Any] = {}
        if type_of_union not in obj or obj[type_of_union] is None:
            cls.check_null_field(
                obj, deserialized, attribute, conjure_field_definition
            )
        else:
            value = obj[type_of_union]
            field_type = conjure_field_definition.field_type
            deserialized[attribute] = cls.do_decode(
                value, field_type, return_none_for_unknown_union_types
            )

        # for backwards compatibility with conjure-python,
        # only pass in arg type_of_union if it is expected
        param_dict = inspect.signature(conjure_type.__init__).parameters
        if "type_of_union" in param_dict:
            deserialized["type_of_union"] = type_of_union
        return conjure_type(**deserialized)

    @classmethod
    def decode_conjure_enum_type(cls, obj, conjure_type):
        """Decodes json into a conjure enum type.

        Args:
            obj: the json object to decode
            conjure_type: a class object which is the enum type
                we're decoding into.
        Returns:
            An instance of enum of type conjure_type.
        """
        if not (isinstance(obj, str) or str(type(obj)) == "<type 'unicode'>"):
            raise Exception(
                "Expected to find str type but found {} instead".format(
                    type(obj)
                )
            )

        if obj in conjure_type.__members__:
            return conjure_type[obj]

        else:
            return conjure_type["UNKNOWN"]

    @classmethod
    def decode_dict(
        cls,
        obj: Dict[Any, Any],
        key_type: Type[DecodableType],
        item_type: Type[DecodableType],
        return_none_for_unknown_union_types: bool = False,
    ) -> Dict[Any, Any]:
        """Decodes json into a dictionary, handling conversion of the
        keys/values (the keys/values may themselves require conversion).

        Args:
            obj: the json object to decode
            key_type: a class object which is the conjure type
                of the keys in this dict
            item_type: a class object which is the conjure type
                of the values in this dict
            return_none_for_unknown_union_types: if set to True, returns None
                instead of raising an exception when an unknown union type is
                encountered
        Returns:
            A python dictionary, where the keys are instances of type key_type
            and the values are of type value_type.
        """
        if not isinstance(obj, dict):
            raise Exception("expected a python dict")
        if (
            key_type is str
            or isinstance(key_type, BinaryType)
            or key_type is BinaryType
            or (
                inspect.isclass(key_type)
                and issubclass(key_type, ConjureEnumType)
            )
        ):
            return dict(
                (
                    (
                        cls.do_decode(
                            x[0], key_type, return_none_for_unknown_union_types
                        ),
                        cls.do_decode(
                            x[1],
                            item_type,
                            return_none_for_unknown_union_types,
                        ),
                    )
                    for x in obj.items()
                )
            )

        return dict(
            (
                (
                    cls.do_decode(
                        json.loads(x[0]),
                        key_type,
                        return_none_for_unknown_union_types,
                    ),
                    cls.do_decode(
                        x[1], item_type, return_none_for_unknown_union_types
                    ),
                )
                for x in obj.items()
            )
        )

    @classmethod
    def decode_list(
        cls,
        obj: List[Any],
        element_type: Type[DecodableType],
        return_none_for_unknown_union_types: bool = False,
    ) -> List[Any]:
        """Decodes json into a list, handling conversion of the elements.

        Args:
            obj: the json object to decode
            element_type: a class object which is the conjure type of
                the elements in this list.
            return_none_for_unknown_union_types: if set to True, returns None
                instead of raising an exception when an unknown union type is
                encountered
        Returns:
            A python list where the elements are instances of type
                element_type.
        """
        if not isinstance(obj, list):
            raise Exception("expected a python list")

        return list(
            map(
                lambda x: cls.do_decode(
                    x, element_type, return_none_for_unknown_union_types
                ),
                obj,
            )
        )

    @classmethod
    def decode_optional(
        cls,
        obj: Optional[Any],
        object_type: Type[DecodableType],
        return_none_for_unknown_union_types: bool = False,
    ) -> Optional[Any]:
        """Decodes json into an element, returning None if the provided object
        is None.

        Args:
            obj: the json object to decode
            object_type: a class object which is the conjure type of
                the object if present.
            return_none_for_unknown_union_types: if set to True, returns None
                instead of raising an exception when an unknown union type is
                encountered
        Returns:
            The decoded obj or None if no obj is provided.
        """
        if obj is None:
            return None

        return cls.do_decode(
            obj, object_type, return_none_for_unknown_union_types
        )

    @classmethod
    def decode_primitive(cls, obj, object_type):
        def raise_mismatch():
            raise Exception(
                "Expected to find {} type but found {} instead".format(
                    object_type, type(obj)
                )
            )

        if object_type is float:
            return float(obj)
        elif (
            object_type is str
            or object_type is BinaryType
            or isinstance(object_type, BinaryType)
        ):
            # Python 2/3 compatible way of checking string
            if not (
                isinstance(obj, str) or str(type(obj)) == "<type 'unicode'>"
            ):
                raise_mismatch()
        elif not isinstance(obj, object_type):
            raise_mismatch()

        return obj

    @classmethod
    def do_decode(
        cls,
        obj: Any,
        obj_type: Type[DecodableType],
        return_none_for_unknown_union_types: bool = False,
    ) -> Any:
        """Decodes json into the specified type

        Args:
            obj: the json object to decode
            obj_type: a class object which is the type we're decoding into.
            return_none_for_unknown_union_types: if set to True, returns None
                instead of raising an exception when an unknown union type is
                encountered
        """

        type_origin = get_origin(obj_type)
        type_args = get_args(obj_type)

        if inspect.isclass(obj_type) and issubclass(obj_type, ConjureBeanType):
            return cls.decode_conjure_bean_type(
                obj, obj_type, return_none_for_unknown_union_types
            )

        elif inspect.isclass(obj_type) and issubclass(
            obj_type, ConjureUnionType
        ):
            return cls.decode_conjure_union_type(
                obj, obj_type, return_none_for_unknown_union_types
            )

        elif inspect.isclass(obj_type) and issubclass(
            obj_type, ConjureEnumType
        ):
            return cls.decode_conjure_enum_type(obj, obj_type)

        elif isinstance(obj_type, DictType):
            return cls.decode_dict(
                obj,
                obj_type.key_type,
                obj_type.value_type,
                return_none_for_unknown_union_types,
            )

        elif isinstance(obj_type, ListType):
            return cls.decode_list(
                obj, obj_type.item_type, return_none_for_unknown_union_types
            )

        elif isinstance(obj_type, OptionalType):
            return cls.decode_optional(
                obj, obj_type.item_type, return_none_for_unknown_union_types
            )

        elif type_origin is OptionalTypeWrapper:
            return cls.decode_optional(
                obj, type_args[0], return_none_for_unknown_union_types
            )

        elif type_origin is dict:
            (key_type, value_type) = type_args
            return cls.decode_dict(
                obj, key_type, value_type, return_none_for_unknown_union_types
            )

        elif type_origin is list:
            return cls.decode_list(
                obj, type_args[0], return_none_for_unknown_union_types
            )

        return cls.decode_primitive(obj, obj_type)

    def decode(
        self,
        obj: Any,
        obj_type: Type[DecodableType],
        return_none_for_unknown_union_types: bool = False,
    ) -> Any:
        return self.do_decode(
            obj, obj_type, return_none_for_unknown_union_types
        )

    def read_from_string(
        self,
        string_value: str,
        obj_type: Type[DecodableType],
        return_none_for_unknown_union_types: bool = False,
    ) -> Any:
        deserialized = json.loads(string_value)
        return self.decode(
            deserialized, obj_type, return_none_for_unknown_union_types
        )
