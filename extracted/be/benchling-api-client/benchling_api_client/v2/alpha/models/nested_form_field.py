from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.barcode_scan_form_instance_provider import BarcodeScanFormInstanceProvider
from ..models.entity_search_form_instance_provider import EntitySearchFormInstanceProvider
from ..models.nested_form_definition import NestedFormDefinition
from ..models.nested_form_field_type import NestedFormFieldType
from ..models.new_blank_form_instance_provider import NewBlankFormInstanceProvider
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedFormField")


@attr.s(auto_attribs=True, repr=False)
class NestedFormField:
    """  """

    _definition: Union[Unset, NestedFormDefinition] = UNSET
    _instance_providers: Union[
        Unset,
        List[
            Union[
                BarcodeScanFormInstanceProvider,
                EntitySearchFormInstanceProvider,
                NewBlankFormInstanceProvider,
                UnknownType,
            ]
        ],
    ] = UNSET
    _type: Union[Unset, NestedFormFieldType] = UNSET
    _description: Union[Unset, str] = UNSET
    _is_required: Union[Unset, bool] = UNSET
    _key: Union[Unset, str] = UNSET
    _label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("definition={}".format(repr(self._definition)))
        fields.append("instance_providers={}".format(repr(self._instance_providers)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("key={}".format(repr(self._key)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "NestedFormField({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        definition: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._definition, Unset):
            definition = self._definition.to_dict()

        instance_providers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._instance_providers, Unset):
            instance_providers = []
            for instance_providers_item_data in self._instance_providers:
                if isinstance(instance_providers_item_data, UnknownType):
                    instance_providers_item = instance_providers_item_data.value
                elif isinstance(instance_providers_item_data, BarcodeScanFormInstanceProvider):
                    instance_providers_item = instance_providers_item_data.to_dict()

                elif isinstance(instance_providers_item_data, EntitySearchFormInstanceProvider):
                    instance_providers_item = instance_providers_item_data.to_dict()

                else:
                    instance_providers_item = instance_providers_item_data.to_dict()

                instance_providers.append(instance_providers_item)

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        description = self._description
        is_required = self._is_required
        key = self._key
        label = self._label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if definition is not UNSET:
            field_dict["definition"] = definition
        if instance_providers is not UNSET:
            field_dict["instanceProviders"] = instance_providers
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if key is not UNSET:
            field_dict["key"] = key
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_definition() -> Union[Unset, NestedFormDefinition]:
            definition: Union[Unset, Union[Unset, NestedFormDefinition]] = UNSET
            _definition = d.pop("definition")

            if not isinstance(_definition, Unset):
                definition = NestedFormDefinition.from_dict(_definition)

            return definition

        try:
            definition = get_definition()
        except KeyError:
            if strict:
                raise
            definition = cast(Union[Unset, NestedFormDefinition], UNSET)

        def get_instance_providers() -> Union[
            Unset,
            List[
                Union[
                    BarcodeScanFormInstanceProvider,
                    EntitySearchFormInstanceProvider,
                    NewBlankFormInstanceProvider,
                    UnknownType,
                ]
            ],
        ]:
            instance_providers = []
            _instance_providers = d.pop("instanceProviders")
            for instance_providers_item_data in _instance_providers or []:

                def _parse_instance_providers_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    BarcodeScanFormInstanceProvider,
                    EntitySearchFormInstanceProvider,
                    NewBlankFormInstanceProvider,
                    UnknownType,
                ]:
                    instance_providers_item: Union[
                        BarcodeScanFormInstanceProvider,
                        EntitySearchFormInstanceProvider,
                        NewBlankFormInstanceProvider,
                        UnknownType,
                    ]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        instance_providers_item = BarcodeScanFormInstanceProvider.from_dict(data, strict=True)

                        return instance_providers_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        instance_providers_item = EntitySearchFormInstanceProvider.from_dict(
                            data, strict=True
                        )

                        return instance_providers_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        instance_providers_item = NewBlankFormInstanceProvider.from_dict(data, strict=True)

                        return instance_providers_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                instance_providers_item = _parse_instance_providers_item(instance_providers_item_data)

                instance_providers.append(instance_providers_item)

            return instance_providers

        try:
            instance_providers = get_instance_providers()
        except KeyError:
            if strict:
                raise
            instance_providers = cast(
                Union[
                    Unset,
                    List[
                        Union[
                            BarcodeScanFormInstanceProvider,
                            EntitySearchFormInstanceProvider,
                            NewBlankFormInstanceProvider,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        def get_type() -> Union[Unset, NestedFormFieldType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = NestedFormFieldType(_type)
                except ValueError:
                    type = NestedFormFieldType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, NestedFormFieldType], UNSET)

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        def get_is_required() -> Union[Unset, bool]:
            is_required = d.pop("isRequired")
            return is_required

        try:
            is_required = get_is_required()
        except KeyError:
            if strict:
                raise
            is_required = cast(Union[Unset, bool], UNSET)

        def get_key() -> Union[Unset, str]:
            key = d.pop("key")
            return key

        try:
            key = get_key()
        except KeyError:
            if strict:
                raise
            key = cast(Union[Unset, str], UNSET)

        def get_label() -> Union[Unset, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, str], UNSET)

        nested_form_field = cls(
            definition=definition,
            instance_providers=instance_providers,
            type=type,
            description=description,
            is_required=is_required,
            key=key,
            label=label,
        )

        nested_form_field.additional_properties = d
        return nested_form_field

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
    def definition(self) -> NestedFormDefinition:
        if isinstance(self._definition, Unset):
            raise NotPresentError(self, "definition")
        return self._definition

    @definition.setter
    def definition(self, value: NestedFormDefinition) -> None:
        self._definition = value

    @definition.deleter
    def definition(self) -> None:
        self._definition = UNSET

    @property
    def instance_providers(
        self,
    ) -> List[
        Union[
            BarcodeScanFormInstanceProvider,
            EntitySearchFormInstanceProvider,
            NewBlankFormInstanceProvider,
            UnknownType,
        ]
    ]:
        """Form instance declare how users can generate new instances of nested forms within a nested form field. The most obvious way to do this is just to add a new blank form; however, very often we want to describe behavior like everytime I scan a barcode, please add a new instance of this nested form with that barcode being resolved to an entity in a specific field."""
        if isinstance(self._instance_providers, Unset):
            raise NotPresentError(self, "instance_providers")
        return self._instance_providers

    @instance_providers.setter
    def instance_providers(
        self,
        value: List[
            Union[
                BarcodeScanFormInstanceProvider,
                EntitySearchFormInstanceProvider,
                NewBlankFormInstanceProvider,
                UnknownType,
            ]
        ],
    ) -> None:
        self._instance_providers = value

    @instance_providers.deleter
    def instance_providers(self) -> None:
        self._instance_providers = UNSET

    @property
    def type(self) -> NestedFormFieldType:
        """The type of this form field. Type declares how this field behaves and dictates the additional properties passed along with the required properties like label and key"""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: NestedFormFieldType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def description(self) -> str:
        """ Description of the purpose of this field """
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def is_required(self) -> bool:
        """ Whether this field is required to be filled out in order to be a valid submission """
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

    @property
    def key(self) -> str:
        """ Reference key of this form field. Used to fix identity of fields beyond the label """
        if isinstance(self._key, Unset):
            raise NotPresentError(self, "key")
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    @key.deleter
    def key(self) -> None:
        self._key = UNSET

    @property
    def label(self) -> str:
        """ End user facing name of this form field. What you see when you fill out the form each time """
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET
