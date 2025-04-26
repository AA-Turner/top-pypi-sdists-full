from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.barcode_scan_form_instance_provider_identifier_type import (
    BarcodeScanFormInstanceProviderIdentifierType,
)
from ..models.barcode_scan_form_instance_provider_mode import BarcodeScanFormInstanceProviderMode
from ..models.barcode_scan_form_instance_provider_type import BarcodeScanFormInstanceProviderType
from ..models.form_barcode_value_reference import FormBarcodeValueReference
from ..models.form_field_value_reference import FormFieldValueReference
from ..models.form_raw_string_query_value_part import FormRawStringQueryValuePart
from ..types import UNSET, Unset

T = TypeVar("T", bound="BarcodeScanFormInstanceProvider")


@attr.s(auto_attribs=True, repr=False)
class BarcodeScanFormInstanceProvider:
    """  """

    _identifier_type: Union[Unset, BarcodeScanFormInstanceProviderIdentifierType] = UNSET
    _mode: Union[Unset, BarcodeScanFormInstanceProviderMode] = UNSET
    _query_value_from: Union[
        Unset,
        List[
            Union[
                FormBarcodeValueReference, FormRawStringQueryValuePart, FormFieldValueReference, UnknownType
            ]
        ],
    ] = UNSET
    _type: Union[Unset, BarcodeScanFormInstanceProviderType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("identifier_type={}".format(repr(self._identifier_type)))
        fields.append("mode={}".format(repr(self._mode)))
        fields.append("query_value_from={}".format(repr(self._query_value_from)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BarcodeScanFormInstanceProvider({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        identifier_type: Union[Unset, int] = UNSET
        if not isinstance(self._identifier_type, Unset):
            identifier_type = self._identifier_type.value

        mode: Union[Unset, int] = UNSET
        if not isinstance(self._mode, Unset):
            mode = self._mode.value

        query_value_from: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._query_value_from, Unset):
            query_value_from = []
            for query_value_from_item_data in self._query_value_from:
                if isinstance(query_value_from_item_data, UnknownType):
                    query_value_from_item = query_value_from_item_data.value
                elif isinstance(query_value_from_item_data, FormBarcodeValueReference):
                    query_value_from_item = query_value_from_item_data.to_dict()

                elif isinstance(query_value_from_item_data, FormRawStringQueryValuePart):
                    query_value_from_item = query_value_from_item_data.to_dict()

                else:
                    query_value_from_item = query_value_from_item_data.to_dict()

                query_value_from.append(query_value_from_item)

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if identifier_type is not UNSET:
            field_dict["identifierType"] = identifier_type
        if mode is not UNSET:
            field_dict["mode"] = mode
        if query_value_from is not UNSET:
            field_dict["queryValueFrom"] = query_value_from
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_identifier_type() -> Union[Unset, BarcodeScanFormInstanceProviderIdentifierType]:
            identifier_type = UNSET
            _identifier_type = d.pop("identifierType")
            if _identifier_type is not None and _identifier_type is not UNSET:
                try:
                    identifier_type = BarcodeScanFormInstanceProviderIdentifierType(_identifier_type)
                except ValueError:
                    identifier_type = BarcodeScanFormInstanceProviderIdentifierType.of_unknown(
                        _identifier_type
                    )

            return identifier_type

        try:
            identifier_type = get_identifier_type()
        except KeyError:
            if strict:
                raise
            identifier_type = cast(Union[Unset, BarcodeScanFormInstanceProviderIdentifierType], UNSET)

        def get_mode() -> Union[Unset, BarcodeScanFormInstanceProviderMode]:
            mode = UNSET
            _mode = d.pop("mode")
            if _mode is not None and _mode is not UNSET:
                try:
                    mode = BarcodeScanFormInstanceProviderMode(_mode)
                except ValueError:
                    mode = BarcodeScanFormInstanceProviderMode.of_unknown(_mode)

            return mode

        try:
            mode = get_mode()
        except KeyError:
            if strict:
                raise
            mode = cast(Union[Unset, BarcodeScanFormInstanceProviderMode], UNSET)

        def get_query_value_from() -> Union[
            Unset,
            List[
                Union[
                    FormBarcodeValueReference,
                    FormRawStringQueryValuePart,
                    FormFieldValueReference,
                    UnknownType,
                ]
            ],
        ]:
            query_value_from = []
            _query_value_from = d.pop("queryValueFrom")
            for query_value_from_item_data in _query_value_from or []:

                def _parse_query_value_from_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    FormBarcodeValueReference,
                    FormRawStringQueryValuePart,
                    FormFieldValueReference,
                    UnknownType,
                ]:
                    query_value_from_item: Union[
                        FormBarcodeValueReference,
                        FormRawStringQueryValuePart,
                        FormFieldValueReference,
                        UnknownType,
                    ]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        query_value_from_item = FormBarcodeValueReference.from_dict(data, strict=True)

                        return query_value_from_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        query_value_from_item = FormRawStringQueryValuePart.from_dict(data, strict=True)

                        return query_value_from_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        query_value_from_item = FormFieldValueReference.from_dict(data, strict=True)

                        return query_value_from_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                query_value_from_item = _parse_query_value_from_item(query_value_from_item_data)

                query_value_from.append(query_value_from_item)

            return query_value_from

        try:
            query_value_from = get_query_value_from()
        except KeyError:
            if strict:
                raise
            query_value_from = cast(
                Union[
                    Unset,
                    List[
                        Union[
                            FormBarcodeValueReference,
                            FormRawStringQueryValuePart,
                            FormFieldValueReference,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        def get_type() -> Union[Unset, BarcodeScanFormInstanceProviderType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = BarcodeScanFormInstanceProviderType(_type)
                except ValueError:
                    type = BarcodeScanFormInstanceProviderType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, BarcodeScanFormInstanceProviderType], UNSET)

        barcode_scan_form_instance_provider = cls(
            identifier_type=identifier_type,
            mode=mode,
            query_value_from=query_value_from,
            type=type,
        )

        barcode_scan_form_instance_provider.additional_properties = d
        return barcode_scan_form_instance_provider

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
    def identifier_type(self) -> BarcodeScanFormInstanceProviderIdentifierType:
        """How we identify the entity that we should query for. Because Benchling entities have several different ways of declaring identity, we also must allow for different ways they can be distinguished by their barcodes."""
        if isinstance(self._identifier_type, Unset):
            raise NotPresentError(self, "identifier_type")
        return self._identifier_type

    @identifier_type.setter
    def identifier_type(self, value: BarcodeScanFormInstanceProviderIdentifierType) -> None:
        self._identifier_type = value

    @identifier_type.deleter
    def identifier_type(self) -> None:
        self._identifier_type = UNSET

    @property
    def mode(self) -> BarcodeScanFormInstanceProviderMode:
        """How we differentiate between single scan mode and multiple scan mode. This will allow a user to either choose to scan and load one barcode at a time or multiple barcodes."""
        if isinstance(self._mode, Unset):
            raise NotPresentError(self, "mode")
        return self._mode

    @mode.setter
    def mode(self, value: BarcodeScanFormInstanceProviderMode) -> None:
        self._mode = value

    @mode.deleter
    def mode(self) -> None:
        self._mode = UNSET

    @property
    def query_value_from(
        self,
    ) -> List[
        Union[FormBarcodeValueReference, FormRawStringQueryValuePart, FormFieldValueReference, UnknownType]
    ]:
        """Because in some contexts barcodes are not necessarily unique, we must also allow for ways to construct the actual value that we should use to match a Benchling entity with. An example here would be entities whose names are constructed like: <barcode>-<crop>"""
        if isinstance(self._query_value_from, Unset):
            raise NotPresentError(self, "query_value_from")
        return self._query_value_from

    @query_value_from.setter
    def query_value_from(
        self,
        value: List[
            Union[
                FormBarcodeValueReference, FormRawStringQueryValuePart, FormFieldValueReference, UnknownType
            ]
        ],
    ) -> None:
        self._query_value_from = value

    @query_value_from.deleter
    def query_value_from(self) -> None:
        self._query_value_from = UNSET

    @property
    def type(self) -> BarcodeScanFormInstanceProviderType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: BarcodeScanFormInstanceProviderType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
