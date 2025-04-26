from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.array_element_app_config_item import ArrayElementAppConfigItem
from ..models.boolean_app_config_item import BooleanAppConfigItem
from ..models.date_app_config_item import DateAppConfigItem
from ..models.datetime_app_config_item import DatetimeAppConfigItem
from ..models.entity_schema_app_config_item import EntitySchemaAppConfigItem
from ..models.field_app_config_item import FieldAppConfigItem
from ..models.float_app_config_item import FloatAppConfigItem
from ..models.generic_api_identified_app_config_item import GenericApiIdentifiedAppConfigItem
from ..models.integer_app_config_item import IntegerAppConfigItem
from ..models.json_app_config_item import JsonAppConfigItem
from ..models.secure_text_app_config_item import SecureTextAppConfigItem
from ..models.text_app_config_item import TextAppConfigItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigurationPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class AppConfigurationPaginatedList:
    """  """

    _app_configuration_items: Union[
        Unset,
        List[
            Union[
                ArrayElementAppConfigItem,
                DateAppConfigItem,
                DatetimeAppConfigItem,
                JsonAppConfigItem,
                EntitySchemaAppConfigItem,
                FieldAppConfigItem,
                BooleanAppConfigItem,
                IntegerAppConfigItem,
                FloatAppConfigItem,
                TextAppConfigItem,
                GenericApiIdentifiedAppConfigItem,
                SecureTextAppConfigItem,
                UnknownType,
            ]
        ],
    ] = UNSET
    _next_token: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("app_configuration_items={}".format(repr(self._app_configuration_items)))
        fields.append("next_token={}".format(repr(self._next_token)))
        return "AppConfigurationPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_configuration_items: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._app_configuration_items, Unset):
            app_configuration_items = []
            for app_configuration_items_item_data in self._app_configuration_items:
                if isinstance(app_configuration_items_item_data, UnknownType):
                    app_configuration_items_item = app_configuration_items_item_data.value
                elif isinstance(app_configuration_items_item_data, ArrayElementAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, DateAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, DatetimeAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, JsonAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, EntitySchemaAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, FieldAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, BooleanAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, IntegerAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, FloatAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, TextAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                elif isinstance(app_configuration_items_item_data, GenericApiIdentifiedAppConfigItem):
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                else:
                    app_configuration_items_item = app_configuration_items_item_data.to_dict()

                app_configuration_items.append(app_configuration_items_item)

        next_token = self._next_token

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_configuration_items is not UNSET:
            field_dict["appConfigurationItems"] = app_configuration_items
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_configuration_items() -> Union[
            Unset,
            List[
                Union[
                    ArrayElementAppConfigItem,
                    DateAppConfigItem,
                    DatetimeAppConfigItem,
                    JsonAppConfigItem,
                    EntitySchemaAppConfigItem,
                    FieldAppConfigItem,
                    BooleanAppConfigItem,
                    IntegerAppConfigItem,
                    FloatAppConfigItem,
                    TextAppConfigItem,
                    GenericApiIdentifiedAppConfigItem,
                    SecureTextAppConfigItem,
                    UnknownType,
                ]
            ],
        ]:
            app_configuration_items = []
            _app_configuration_items = d.pop("appConfigurationItems")
            for app_configuration_items_item_data in _app_configuration_items or []:

                def _parse_app_configuration_items_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    ArrayElementAppConfigItem,
                    DateAppConfigItem,
                    DatetimeAppConfigItem,
                    JsonAppConfigItem,
                    EntitySchemaAppConfigItem,
                    FieldAppConfigItem,
                    BooleanAppConfigItem,
                    IntegerAppConfigItem,
                    FloatAppConfigItem,
                    TextAppConfigItem,
                    GenericApiIdentifiedAppConfigItem,
                    SecureTextAppConfigItem,
                    UnknownType,
                ]:
                    app_configuration_items_item: Union[
                        ArrayElementAppConfigItem,
                        DateAppConfigItem,
                        DatetimeAppConfigItem,
                        JsonAppConfigItem,
                        EntitySchemaAppConfigItem,
                        FieldAppConfigItem,
                        BooleanAppConfigItem,
                        IntegerAppConfigItem,
                        FloatAppConfigItem,
                        TextAppConfigItem,
                        GenericApiIdentifiedAppConfigItem,
                        SecureTextAppConfigItem,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        app_config_item: Union[
                            ArrayElementAppConfigItem,
                            DateAppConfigItem,
                            DatetimeAppConfigItem,
                            JsonAppConfigItem,
                            EntitySchemaAppConfigItem,
                            FieldAppConfigItem,
                            BooleanAppConfigItem,
                            IntegerAppConfigItem,
                            FloatAppConfigItem,
                            TextAppConfigItem,
                            GenericApiIdentifiedAppConfigItem,
                            SecureTextAppConfigItem,
                            UnknownType,
                        ]
                        if discriminator_value == "aa_sequence":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "array_element":
                            app_config_item = ArrayElementAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "boolean":
                            app_config_item = BooleanAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "box":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "box_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "container":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "container_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "custom_entity":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "date":
                            app_config_item = DateAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "datetime":
                            app_config_item = DatetimeAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "dna_oligo":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "dna_sequence":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "dropdown":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "dropdown_option":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "entity_schema":
                            app_config_item = EntitySchemaAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "entry":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "entry_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "field":
                            app_config_item = FieldAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "float":
                            app_config_item = FloatAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "folder":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "integer":
                            app_config_item = IntegerAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "json":
                            app_config_item = JsonAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "legacy_request_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "location":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "location_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "mixture":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "molecule":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "plate":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "plate_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "project":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "registry":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "result_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "rna_oligo":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "rna_sequence":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "run_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "secure_text":
                            app_config_item = SecureTextAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "text":
                            app_config_item = TextAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "workflow_task_schema":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "workflow_task_status":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item
                        if discriminator_value == "worklist":
                            app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=False)

                            return app_config_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = ArrayElementAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = DateAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = DatetimeAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = JsonAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = EntitySchemaAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = FieldAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = BooleanAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = IntegerAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = FloatAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = TextAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = GenericApiIdentifiedAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item = SecureTextAppConfigItem.from_dict(data, strict=True)

                        return app_config_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                app_configuration_items_item = _parse_app_configuration_items_item(
                    app_configuration_items_item_data
                )

                app_configuration_items.append(app_configuration_items_item)

            return app_configuration_items

        try:
            app_configuration_items = get_app_configuration_items()
        except KeyError:
            if strict:
                raise
            app_configuration_items = cast(
                Union[
                    Unset,
                    List[
                        Union[
                            ArrayElementAppConfigItem,
                            DateAppConfigItem,
                            DatetimeAppConfigItem,
                            JsonAppConfigItem,
                            EntitySchemaAppConfigItem,
                            FieldAppConfigItem,
                            BooleanAppConfigItem,
                            IntegerAppConfigItem,
                            FloatAppConfigItem,
                            TextAppConfigItem,
                            GenericApiIdentifiedAppConfigItem,
                            SecureTextAppConfigItem,
                            UnknownType,
                        ]
                    ],
                ],
                UNSET,
            )

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        app_configuration_paginated_list = cls(
            app_configuration_items=app_configuration_items,
            next_token=next_token,
        )

        return app_configuration_paginated_list

    @property
    def app_configuration_items(
        self,
    ) -> List[
        Union[
            ArrayElementAppConfigItem,
            DateAppConfigItem,
            DatetimeAppConfigItem,
            JsonAppConfigItem,
            EntitySchemaAppConfigItem,
            FieldAppConfigItem,
            BooleanAppConfigItem,
            IntegerAppConfigItem,
            FloatAppConfigItem,
            TextAppConfigItem,
            GenericApiIdentifiedAppConfigItem,
            SecureTextAppConfigItem,
            UnknownType,
        ]
    ]:
        if isinstance(self._app_configuration_items, Unset):
            raise NotPresentError(self, "app_configuration_items")
        return self._app_configuration_items

    @app_configuration_items.setter
    def app_configuration_items(
        self,
        value: List[
            Union[
                ArrayElementAppConfigItem,
                DateAppConfigItem,
                DatetimeAppConfigItem,
                JsonAppConfigItem,
                EntitySchemaAppConfigItem,
                FieldAppConfigItem,
                BooleanAppConfigItem,
                IntegerAppConfigItem,
                FloatAppConfigItem,
                TextAppConfigItem,
                GenericApiIdentifiedAppConfigItem,
                SecureTextAppConfigItem,
                UnknownType,
            ]
        ],
    ) -> None:
        self._app_configuration_items = value

    @app_configuration_items.deleter
    def app_configuration_items(self) -> None:
        self._app_configuration_items = UNSET

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET
