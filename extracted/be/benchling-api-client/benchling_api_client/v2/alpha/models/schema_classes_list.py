from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.schema_class import SchemaClass
from ..types import UNSET, Unset

T = TypeVar("T", bound="SchemaClassesList")


@attr.s(auto_attribs=True, repr=False)
class SchemaClassesList:
    """  """

    _schema_classes: Union[Unset, List[SchemaClass]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("schema_classes={}".format(repr(self._schema_classes)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "SchemaClassesList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        schema_classes: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._schema_classes, Unset):
            schema_classes = []
            for schema_classes_item_data in self._schema_classes:
                schema_classes_item = schema_classes_item_data.to_dict()

                schema_classes.append(schema_classes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if schema_classes is not UNSET:
            field_dict["schemaClasses"] = schema_classes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_schema_classes() -> Union[Unset, List[SchemaClass]]:
            schema_classes = []
            _schema_classes = d.pop("schemaClasses")
            for schema_classes_item_data in _schema_classes or []:
                schema_classes_item = SchemaClass.from_dict(schema_classes_item_data, strict=False)

                schema_classes.append(schema_classes_item)

            return schema_classes

        try:
            schema_classes = get_schema_classes()
        except KeyError:
            if strict:
                raise
            schema_classes = cast(Union[Unset, List[SchemaClass]], UNSET)

        schema_classes_list = cls(
            schema_classes=schema_classes,
        )

        schema_classes_list.additional_properties = d
        return schema_classes_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def schema_classes(self) -> List[SchemaClass]:
        if isinstance(self._schema_classes, Unset):
            raise NotPresentError(self, "schema_classes")
        return self._schema_classes

    @schema_classes.setter
    def schema_classes(self, value: List[SchemaClass]) -> None:
        self._schema_classes = value

    @schema_classes.deleter
    def schema_classes(self) -> None:
        self._schema_classes = UNSET
