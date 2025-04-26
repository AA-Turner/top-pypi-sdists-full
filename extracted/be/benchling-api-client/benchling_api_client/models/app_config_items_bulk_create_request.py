from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.app_config_item_boolean_create import AppConfigItemBooleanCreate
from ..models.app_config_item_date_create import AppConfigItemDateCreate
from ..models.app_config_item_datetime_create import AppConfigItemDatetimeCreate
from ..models.app_config_item_float_create import AppConfigItemFloatCreate
from ..models.app_config_item_generic_create import AppConfigItemGenericCreate
from ..models.app_config_item_integer_create import AppConfigItemIntegerCreate
from ..models.app_config_item_json_create import AppConfigItemJsonCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigItemsBulkCreateRequest")


@attr.s(auto_attribs=True, repr=False)
class AppConfigItemsBulkCreateRequest:
    """  """

    _app_configuration_items: List[
        Union[
            AppConfigItemGenericCreate,
            AppConfigItemBooleanCreate,
            AppConfigItemIntegerCreate,
            AppConfigItemFloatCreate,
            AppConfigItemDateCreate,
            AppConfigItemDatetimeCreate,
            AppConfigItemJsonCreate,
            UnknownType,
        ]
    ]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app_configuration_items={}".format(repr(self._app_configuration_items)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppConfigItemsBulkCreateRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app_configuration_items = []
        for app_configuration_items_item_data in self._app_configuration_items:
            if isinstance(app_configuration_items_item_data, UnknownType):
                app_configuration_items_item = app_configuration_items_item_data.value
            elif isinstance(app_configuration_items_item_data, AppConfigItemGenericCreate):
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            elif isinstance(app_configuration_items_item_data, AppConfigItemBooleanCreate):
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            elif isinstance(app_configuration_items_item_data, AppConfigItemIntegerCreate):
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            elif isinstance(app_configuration_items_item_data, AppConfigItemFloatCreate):
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            elif isinstance(app_configuration_items_item_data, AppConfigItemDateCreate):
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            elif isinstance(app_configuration_items_item_data, AppConfigItemDatetimeCreate):
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            else:
                app_configuration_items_item = app_configuration_items_item_data.to_dict()

            app_configuration_items.append(app_configuration_items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app_configuration_items is not UNSET:
            field_dict["appConfigurationItems"] = app_configuration_items

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app_configuration_items() -> List[
            Union[
                AppConfigItemGenericCreate,
                AppConfigItemBooleanCreate,
                AppConfigItemIntegerCreate,
                AppConfigItemFloatCreate,
                AppConfigItemDateCreate,
                AppConfigItemDatetimeCreate,
                AppConfigItemJsonCreate,
                UnknownType,
            ]
        ]:
            app_configuration_items = []
            _app_configuration_items = d.pop("appConfigurationItems")
            for app_configuration_items_item_data in _app_configuration_items:

                def _parse_app_configuration_items_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[
                    AppConfigItemGenericCreate,
                    AppConfigItemBooleanCreate,
                    AppConfigItemIntegerCreate,
                    AppConfigItemFloatCreate,
                    AppConfigItemDateCreate,
                    AppConfigItemDatetimeCreate,
                    AppConfigItemJsonCreate,
                    UnknownType,
                ]:
                    app_configuration_items_item: Union[
                        AppConfigItemGenericCreate,
                        AppConfigItemBooleanCreate,
                        AppConfigItemIntegerCreate,
                        AppConfigItemFloatCreate,
                        AppConfigItemDateCreate,
                        AppConfigItemDatetimeCreate,
                        AppConfigItemJsonCreate,
                        UnknownType,
                    ]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        app_config_item_create: Union[
                            AppConfigItemGenericCreate,
                            AppConfigItemBooleanCreate,
                            AppConfigItemIntegerCreate,
                            AppConfigItemFloatCreate,
                            AppConfigItemDateCreate,
                            AppConfigItemDatetimeCreate,
                            AppConfigItemJsonCreate,
                            UnknownType,
                        ]
                        if discriminator_value == "aa_sequence":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "boolean":
                            app_config_item_create = AppConfigItemBooleanCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "box":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "box_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "container":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "container_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "custom_entity":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "date":
                            app_config_item_create = AppConfigItemDateCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "datetime":
                            app_config_item_create = AppConfigItemDatetimeCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "dna_oligo":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "dna_sequence":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "dropdown":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "dropdown_option":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "entity_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "entry":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "entry_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "field":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "float":
                            app_config_item_create = AppConfigItemFloatCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "folder":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "integer":
                            app_config_item_create = AppConfigItemIntegerCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "json":
                            app_config_item_create = AppConfigItemJsonCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "legacy_request_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "location":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "location_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "mixture":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "molecule":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "plate":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "plate_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "project":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "registry":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "result_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "rna_oligo":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "rna_sequence":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "run_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "secure_text":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "text":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "workflow_task_schema":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "workflow_task_status":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create
                        if discriminator_value == "worklist":
                            app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=False)

                            return app_config_item_create

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemGenericCreate.from_dict(data, strict=True)

                        return app_config_item_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemBooleanCreate.from_dict(data, strict=True)

                        return app_config_item_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemIntegerCreate.from_dict(data, strict=True)

                        return app_config_item_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemFloatCreate.from_dict(data, strict=True)

                        return app_config_item_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemDateCreate.from_dict(data, strict=True)

                        return app_config_item_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemDatetimeCreate.from_dict(data, strict=True)

                        return app_config_item_create
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        app_config_item_create = AppConfigItemJsonCreate.from_dict(data, strict=True)

                        return app_config_item_create
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
                List[
                    Union[
                        AppConfigItemGenericCreate,
                        AppConfigItemBooleanCreate,
                        AppConfigItemIntegerCreate,
                        AppConfigItemFloatCreate,
                        AppConfigItemDateCreate,
                        AppConfigItemDatetimeCreate,
                        AppConfigItemJsonCreate,
                        UnknownType,
                    ]
                ],
                UNSET,
            )

        app_config_items_bulk_create_request = cls(
            app_configuration_items=app_configuration_items,
        )

        app_config_items_bulk_create_request.additional_properties = d
        return app_config_items_bulk_create_request

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
    def app_configuration_items(
        self,
    ) -> List[
        Union[
            AppConfigItemGenericCreate,
            AppConfigItemBooleanCreate,
            AppConfigItemIntegerCreate,
            AppConfigItemFloatCreate,
            AppConfigItemDateCreate,
            AppConfigItemDatetimeCreate,
            AppConfigItemJsonCreate,
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
                AppConfigItemGenericCreate,
                AppConfigItemBooleanCreate,
                AppConfigItemIntegerCreate,
                AppConfigItemFloatCreate,
                AppConfigItemDateCreate,
                AppConfigItemDatetimeCreate,
                AppConfigItemJsonCreate,
                UnknownType,
            ]
        ],
    ) -> None:
        self._app_configuration_items = value
