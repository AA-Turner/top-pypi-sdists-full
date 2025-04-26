from __future__ import annotations

from datetime import date, datetime
import json
import random
import string
from typing import cast, Dict, get_args, List, Optional, Protocol, Union

from benchling_api_client.v2.beta.models.base_manifest_config import BaseManifestConfig
from benchling_api_client.v2.beta.models.benchling_app_manifest import BenchlingAppManifest
from benchling_api_client.v2.beta.models.dropdown_dependency import DropdownDependency
from benchling_api_client.v2.beta.models.entity_schema_dependency import EntitySchemaDependency
from benchling_api_client.v2.beta.models.field_definitions_manifest import FieldDefinitionsManifest
from benchling_api_client.v2.beta.models.manifest_array_config import ManifestArrayConfig
from benchling_api_client.v2.beta.models.manifest_boolean_scalar_config import ManifestBooleanScalarConfig
from benchling_api_client.v2.beta.models.manifest_date_scalar_config import ManifestDateScalarConfig
from benchling_api_client.v2.beta.models.manifest_datetime_scalar_config import ManifestDatetimeScalarConfig
from benchling_api_client.v2.beta.models.manifest_float_scalar_config import ManifestFloatScalarConfig
from benchling_api_client.v2.beta.models.manifest_integer_scalar_config import ManifestIntegerScalarConfig
from benchling_api_client.v2.beta.models.manifest_json_scalar_config import ManifestJsonScalarConfig
from benchling_api_client.v2.beta.models.manifest_scalar_config import ManifestScalarConfig
from benchling_api_client.v2.beta.models.manifest_secure_text_scalar_config import (
    ManifestSecureTextScalarConfig,
)
from benchling_api_client.v2.beta.models.manifest_text_scalar_config import ManifestTextScalarConfig
from benchling_api_client.v2.beta.models.resource_dependency import ResourceDependency
from benchling_api_client.v2.beta.models.schema_dependency import SchemaDependency
from benchling_api_client.v2.beta.models.schema_dependency_subtypes import (
    SchemaDependencySubtypes as SchemaDependencySubtypesBeta,
)
from benchling_api_client.v2.beta.models.workflow_task_schema_dependency import WorkflowTaskSchemaDependency
from benchling_api_client.v2.extensions import UnknownType
from benchling_api_client.v2.stable.types import UNSET, Unset

from benchling_sdk.apps.config.decryption_provider import BaseDecryptionProvider
from benchling_sdk.apps.config.errors import UnsupportedConfigItemError
from benchling_sdk.apps.config.framework import _supported_config_item, ConfigItemStore, StaticConfigProvider
from benchling_sdk.apps.config.helpers import (
    _element_definition_from_dependency,
    _enum_from_dependency,
    _field_definitions_from_dependency,
    _options_from_dependency,
    _ScalarConfigTypes,
    _subtype_from_entity_schema_dependency,
    _workflow_task_schema_output_from_dependency,
    datetime_config_value_to_str,
)
from benchling_sdk.apps.config.types import ConfigurationReference
from benchling_sdk.apps.types import JsonType
from benchling_sdk.helpers.logging_helpers import log_stability_warning, StabilityLevel
from benchling_sdk.models import (
    AppConfigItem,
    ArrayElementAppConfigItem,
    ArrayElementAppConfigItemType,
    BooleanAppConfigItem,
    BooleanAppConfigItemType,
    DateAppConfigItem,
    DateAppConfigItemType,
    DatetimeAppConfigItem,
    DatetimeAppConfigItemType,
    EntitySchemaAppConfigItem,
    EntitySchemaAppConfigItemType,
    FieldAppConfigItem,
    FieldAppConfigItemType,
    FloatAppConfigItem,
    FloatAppConfigItemType,
    GenericApiIdentifiedAppConfigItem,
    GenericApiIdentifiedAppConfigItemType,
    IntegerAppConfigItem,
    IntegerAppConfigItemType,
    JsonAppConfigItem,
    JsonAppConfigItemType,
    LinkedAppConfigResourceSummary,
    SchemaDependencySubtypes,
    SecureTextAppConfigItem,
    SecureTextAppConfigItemType,
    TextAppConfigItem,
    TextAppConfigItemType,
)

ManifestDependencies = Union[
    DropdownDependency,
    EntitySchemaDependency,
    ManifestArrayConfig,
    ManifestScalarConfig,
    ResourceDependency,
    SchemaDependency,
    WorkflowTaskSchemaDependency,
    UnknownType,
]

log_stability_warning(StabilityLevel.BETA)


class MockDecryptionFunction(Protocol):
    """Mock out a decryption function for use with secure text."""

    def __call__(self, ciphertext: str) -> str:
        """Return a string representing plaintext given input ciphertext."""


class MockDecryptionProvider(BaseDecryptionProvider):
    """
    Mock Decryption Provider.

    A generic class mocking a BaseDecryptionProvider. Can be passed a function to mock arbitrary decryption.

    It's recommended to extend this class or use a specific implementation instead of initializing an instance.
    """

    _mock_decryption_function: MockDecryptionFunction

    def __init__(self, mock_decryption_function: MockDecryptionFunction):
        """
        Init Mock Decryption Provider.

        Pass a function that returns desired mocked plaintext given ciphertext.
        """
        self._mock_decryption_function = mock_decryption_function

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt.

        Invokes the mocked decryption function provided when instantiating the class to return a "decrypted" value.
        """
        return self._mock_decryption_function(ciphertext)


class MockConfigItemStore(ConfigItemStore):
    """
    Mock App Config.

    A helper class for easily mocking app config in various permutations.

    Easily mock all config items from a manifest model (which can be loaded from
    `benchling_sdk.apps.helpers.manifest_helpers.manifest_from_file()`.
    """

    _config_items: List[AppConfigItem]

    def __init__(self, config_items: List[AppConfigItem]):
        """
        Init Mock Benchling App Config.

        The class can be initialized by providing a list of AppConfigItem, but the recommended
        usage is to mock directly from a manifest, like `MockBenchlingAppConfig.from_manifest()`
        """
        super().__init__(StaticConfigProvider([_supported_config_item(item) for item in config_items]))
        self._config_items = config_items

    @classmethod
    def from_manifest(cls, manifest: BenchlingAppManifest) -> MockConfigItemStore:
        """
        From Manifest.

        Reads a manifest amd mocks out all dependencies.
        """
        config_items = mock_app_config_items_from_manifest(manifest)
        return cls(config_items)

    def with_replacement(self, replacement: AppConfigItem) -> MockConfigItemStore:
        """
        With Replacement.

        Returns a new MockBenchlingAppConfig with the app config item at the specified path replaced.
        """
        # list() solves "List is invariant"
        replaced_app_config = replace_mocked_config_item_by_path(
            list(self.config_items), _config_path(replacement), replacement
        )
        return MockConfigItemStore(replaced_app_config)

    def with_replacements(self, replacements: List[AppConfigItem]) -> MockConfigItemStore:
        """
        With Replacement.

        Returns a new MockBenchlingAppConfig with the app config item at the specified path replaced.
        """
        # list() solves "List is invariant"
        replaced_app_config: List[AppConfigItem] = list(self.config_items)
        for replacement in replacements:
            replaced_app_config = replace_mocked_config_item_by_path(
                list(replaced_app_config), _config_path(replacement), replacement
            )
        return MockConfigItemStore(list(replaced_app_config))

    @property
    def config_items(self) -> List[ConfigurationReference]:
        """List the config items in the mock app config, excluding any unknown types."""
        return [_supported_config_item(config_item) for config_item in self._config_items]

    @property
    def config_items_with_unknown(self) -> List[AppConfigItem]:
        """List the config items in the mock app config, including any unknown types."""
        return self._config_items


class MockDecryptionProviderStatic(MockDecryptionProvider):
    """
    Mock Decryption Provider Static.

    Always return the same "decrypted" value regardless of what ciphertext is passed.
    Useful if you only have a single secret value.
    """

    def __init__(self, decrypt_value: str):
        """
        Init Mock Decryption Provider Static.

        Supply the string to always be returned.
        """

        def decrypt(ciphertext: str) -> str:
            return decrypt_value

        super().__init__(decrypt)


class MockDecryptionProviderMapped(MockDecryptionProvider):
    """
    Mock Decryption Provider Mapped.

    Returns a "decrypted" value based on the input ciphertext.
    Useful if you have multiple secrets to mock simultaneously.
    """

    def __init__(self, decrypt_mapping: Dict[str, str]):
        """
        Init Mock Decryption Provider Mapped.

        Supply the dictionary mapping with ciphertext as keys and plaintext as values.
        Any ciphertext decrypted without a corresponding value will result in a KeyError.
        """

        def decrypt(ciphertext: str) -> str:
            return decrypt_mapping[ciphertext]

        super().__init__(decrypt)


def mock_app_config_items_from_manifest(manifest: BenchlingAppManifest) -> List[AppConfigItem]:
    """
    Mock Benchling App Config Items.

    This method accepts an app manifest model and creates mocked values for app the app config.

    The concrete mocked out values, such as API Ids and schema names are nonsensical and random,
    but are valid.

    Code should avoid relying on specific values or conventions (such as API prefixes). If
    specific dependency values need to be tested in isolation, the caller can selectively
    override the randomized values with replace_mocked_config_item_by_path().
    """
    root_config_items = [_mock_dependency(dependency) for dependency in manifest.configuration]
    return [config_item for sub_config_items in root_config_items for config_item in sub_config_items]


def replace_mocked_config_item_by_path(
    original_config: List[AppConfigItem], replacement_path: List[str], replacement_item: AppConfigItem
) -> List[AppConfigItem]:
    """Return an updated list of app config items with a specific config item replaced with the provided mock."""
    replaced_config = [config for config in original_config if _config_path(config) != replacement_path]
    replaced_config.append(replacement_item)
    return replaced_config


def mock_bool_app_config_item(path: List[str], value: Optional[bool]) -> BooleanAppConfigItem:
    """Mock a bool app config item with a path and specified value."""
    return BooleanAppConfigItem(
        path=path,
        value=value,
        type=BooleanAppConfigItemType.BOOLEAN,
        id=_random_string("aci_"),
    )


def mock_date_app_config_item(path: List[str], value: Optional[date]) -> DateAppConfigItem:
    """Mock a date app config item with a path and specified value."""
    return DateAppConfigItem(
        path=path,
        value=str(value) if value is not None else None,
        type=DateAppConfigItemType.DATE,
        id=_random_string("aci_"),
    )


def mock_datetime_app_config_item(path: List[str], value: Optional[datetime]) -> DatetimeAppConfigItem:
    """Mock a datetime app config item with a path and specified value."""
    return DatetimeAppConfigItem(
        path=path,
        value=datetime_config_value_to_str(value) if value else None,
        type=DatetimeAppConfigItemType.DATETIME,
        id=_random_string("aci_"),
    )


def mock_float_app_config_item(path: List[str], value: Optional[float]) -> FloatAppConfigItem:
    """Mock a float app config item with a path and specified value."""
    return FloatAppConfigItem(
        path=path,
        value=value,
        type=FloatAppConfigItemType.FLOAT,
        id=_random_string("aci_"),
    )


def mock_int_app_config_item(path: List[str], value: Optional[int]) -> IntegerAppConfigItem:
    """Mock an int app config item with a path and specified value."""
    return IntegerAppConfigItem(
        path=path,
        value=value,
        type=IntegerAppConfigItemType.INTEGER,
        id=_random_string("aci_"),
    )


def mock_json_app_config_item(path: List[str], value: Optional[JsonType]) -> JsonAppConfigItem:
    """Mock an int app config item with a path and specified value."""
    return JsonAppConfigItem(
        path=path,
        value=json.dumps(value) if value is not None else None,
        type=JsonAppConfigItemType.JSON,
        id=_random_string("aci_"),
    )


def mock_secure_text_app_config_item(path: List[str], value: Optional[str]) -> SecureTextAppConfigItem:
    """Mock a secure text app config item with a path and specified value."""
    return SecureTextAppConfigItem(
        path=path,
        value=value,
        type=SecureTextAppConfigItemType.SECURE_TEXT,
        id=_random_string("aci_"),
    )


def mock_text_app_config_item(path: List[str], value: Optional[str]) -> TextAppConfigItem:
    """Mock a text app config item with a path and specified value."""
    return TextAppConfigItem(
        path=path,
        value=value,
        type=TextAppConfigItemType.TEXT,
        id=_random_string("aci_"),
    )


def _mock_dependency(  # noqa:PLR0911
    dependency: ManifestDependencies,
    parent_path: Optional[List[str]] = None,
) -> List[AppConfigItem]:
    """Mock a dependency from its manifest definition."""
    parent_path = parent_path if parent_path else []
    # MyPy has trouble inferring lists with [config_item] + sub_items so use the syntax like:
    # [*[config_item], *sub_items]
    # See https://github.com/python/mypy/issues/3933#issuecomment-808739063
    if isinstance(dependency, DropdownDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=parent_path + [dependency.name],
            type=GenericApiIdentifiedAppConfigItemType.DROPDOWN,
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency, parent_path=parent_path)
            for subdependency in _options_from_dependency(dependency)
        ]
        return [*[config_item], *sub_items]
    elif isinstance(dependency, EntitySchemaDependency):
        linked_resource_id = _random_string("val_")
        subtype = _subtype_from_entity_schema_dependency(dependency)
        optional_subtype: Union[SchemaDependencySubtypes, Unset] = (
            _convert_entity_subtype(subtype) if subtype is not None else UNSET
        )
        entity_item = EntitySchemaAppConfigItem(
            id=_random_string("aci_"),
            path=parent_path + [dependency.name],
            type=EntitySchemaAppConfigItemType.ENTITY_SCHEMA,
            subtype=optional_subtype,
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency, parent_path=parent_path)
            for subdependency in _field_definitions_from_dependency(dependency)
        ]
        return [*[entity_item], *sub_items]
    elif isinstance(dependency, SchemaDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=parent_path + [dependency.name],
            type=GenericApiIdentifiedAppConfigItemType(dependency.type),
            value=_random_string("val_"),
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency, parent_path=parent_path)
            for subdependency in _field_definitions_from_dependency(dependency)
        ]
        return [*[config_item], *sub_items]
    elif isinstance(dependency, WorkflowTaskSchemaDependency):
        linked_resource_id = _random_string("val_")
        config_item = GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=parent_path + [dependency.name],
            type=GenericApiIdentifiedAppConfigItemType.WORKFLOW_TASK_SCHEMA,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        sub_items = [
            _mock_subdependency(subdependency, dependency, parent_path=parent_path)
            for subdependency in _field_definitions_from_dependency(dependency)
        ]
        workflow_task_output = _workflow_task_schema_output_from_dependency(dependency)
        if workflow_task_output:
            output_fields = _field_definitions_from_dependency(workflow_task_output)
            output_items = [
                _mock_workflow_output_subdependency(subdependency, dependency, parent_path=parent_path)
                for subdependency in output_fields
            ]
            sub_items += output_items
        return [*[config_item], *sub_items]
    # Python can't compare isinstance for Union types until Python 3.10 so just do this for now
    # from: https://github.com/python/typing/discussions/1132#discussioncomment-2560441
    elif isinstance(dependency, get_args(ManifestScalarConfig)):
        # Ignore type since MyPy definitely can't tell from above
        return [_mock_scalar_dependency(dependency, parent_path=parent_path)]  # type: ignore
    elif isinstance(dependency, ManifestArrayConfig):
        return _mock_array_dependency(dependency, parent_path=parent_path)
    elif isinstance(dependency, UnknownType):
        return [UnknownType(value="Unknown")]
    else:
        linked_resource_id = _random_string("val_")
        return [
            GenericApiIdentifiedAppConfigItem(
                id=_random_string("aci_"),
                path=parent_path + [dependency.name],
                type=GenericApiIdentifiedAppConfigItemType(dependency.type),
                value=linked_resource_id,
                linked_resource=_mock_linked_resource(linked_resource_id),
            )
        ]


def _convert_entity_subtype(manifest_subtype: SchemaDependencySubtypesBeta) -> SchemaDependencySubtypes:
    # Manifest types and config types should be equivalent but are technically different Enums
    source_value: str = manifest_subtype.value
    return SchemaDependencySubtypes(source_value)


def _mock_scalar_dependency(  # noqa:PLR0911
    dependency: ManifestScalarConfig, parent_path: Optional[List[str]] = None
) -> AppConfigItem:
    parent_path = parent_path if parent_path else []
    if isinstance(dependency, ManifestBooleanScalarConfig):
        bool_value = cast(bool, _mock_scalar_value(dependency))
        bool_config = mock_bool_app_config_item([dependency.name], bool_value)
        return _append_config_item_path(bool_config, parent_path)
    elif isinstance(dependency, ManifestDateScalarConfig):
        date_value = cast(date, _mock_scalar_value(dependency))
        date_config = mock_date_app_config_item([dependency.name], date_value)
        return _append_config_item_path(date_config, parent_path)
    elif isinstance(dependency, ManifestDatetimeScalarConfig):
        datetime_value = cast(datetime, _mock_scalar_value(dependency))
        datetime_config = mock_datetime_app_config_item([dependency.name], datetime_value)
        return _append_config_item_path(datetime_config, parent_path)
    elif isinstance(dependency, ManifestFloatScalarConfig):
        float_value = cast(float, _mock_scalar_value(dependency))
        float_config = mock_float_app_config_item([dependency.name], float_value)
        return _append_config_item_path(float_config, parent_path)
    elif isinstance(dependency, ManifestIntegerScalarConfig):
        int_value = cast(int, _mock_scalar_value(dependency))
        int_config = mock_int_app_config_item([dependency.name], int_value)
        return _append_config_item_path(int_config, parent_path)
    elif isinstance(dependency, ManifestJsonScalarConfig):
        json_value = cast(JsonType, _mock_scalar_value(dependency))
        json_config = mock_json_app_config_item([dependency.name], json_value)
        return _append_config_item_path(json_config, parent_path)
    elif isinstance(dependency, ManifestSecureTextScalarConfig):
        secure_text_value = cast(str, _mock_scalar_value(dependency))
        secure_text_config = mock_secure_text_app_config_item([dependency.name], secure_text_value)
        return _append_config_item_path(secure_text_config, parent_path)
    else:
        assert not isinstance(dependency, UnknownType), f"Unable to mock unknown type {dependency}"
        text_value = cast(str, _mock_scalar_value(dependency))
        text_config = mock_text_app_config_item([dependency.name], text_value)
        return _append_config_item_path(text_config, parent_path)


def _append_config_item_path(config_item: AppConfigItem, parent_path: List[str]) -> AppConfigItem:
    if isinstance(config_item, UnknownType):
        return config_item
    config_item.path = parent_path + config_item.path
    return config_item


def _mock_array_dependency(
    dependency: ManifestArrayConfig, parent_path: Optional[List[str]] = None, rows: int = 1
) -> List[AppConfigItem]:
    config_rows = []
    parent_path = parent_path if parent_path else []
    for _ in range(rows):
        row = _mock_array_row(dependency, parent_path=parent_path)
        elements = _element_definition_from_dependency(dependency)
        element_configs = [_mock_dependency(element, row.path) for element in elements]
        flattened_configs = [element for sublist in element_configs for element in sublist]
        config_rows.append(row)
        config_rows.extend(flattened_configs)
    return config_rows


def _mock_array_row(dependency: ManifestArrayConfig, parent_path: Optional[List[str]] = None):
    row_name = _random_string("Row ")
    parent_path = parent_path if parent_path else []
    return ArrayElementAppConfigItem(
        id=_random_string("aci_"),
        path=parent_path + [dependency.name, row_name],
        type=ArrayElementAppConfigItemType.ARRAY_ELEMENT,
        value=row_name,
    )


def _mock_scalar_with_enum(dependency: ManifestScalarConfig) -> Union[float, int, str]:
    assert isinstance(
        dependency, (ManifestFloatScalarConfig, ManifestIntegerScalarConfig, ManifestTextScalarConfig)
    )
    value = random.choice(dependency.enum)
    if isinstance(dependency, ManifestFloatScalarConfig):
        return cast(float, value)
    elif isinstance(dependency, ManifestIntegerScalarConfig):
        return cast(int, value)
    return str(value)


def _is_scalar_with_enum(dependency: ManifestScalarConfig) -> bool:
    if isinstance(
        dependency, (ManifestFloatScalarConfig, ManifestIntegerScalarConfig, ManifestTextScalarConfig)
    ):
        # MyPy doesn't find this to be truthy without a specific len check
        return len(_enum_from_dependency(dependency)) > 0
    return False


def _mock_subdependency(
    subdependency: Union[BaseManifestConfig, FieldDefinitionsManifest],
    parent_config,
    parent_path: Optional[List[str]] = None,
) -> AppConfigItem:
    parent_path = parent_path if parent_path else []
    if isinstance(parent_config, DropdownDependency):
        linked_resource_id = _random_string("opt_")
        return GenericApiIdentifiedAppConfigItem(
            id=_random_string("aci_"),
            path=parent_path + [parent_config.name, subdependency.name],
            type=GenericApiIdentifiedAppConfigItemType.DROPDOWN_OPTION,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
    elif isinstance(parent_config, (EntitySchemaDependency, SchemaDependency, WorkflowTaskSchemaDependency)):
        path = [parent_config.name, subdependency.name]
        linked_resource_id = _random_string("tsf_")
        app_config = FieldAppConfigItem(
            id=_random_string("aci_"),
            path=parent_path + path,
            type=FieldAppConfigItemType.FIELD,
            value=linked_resource_id,
            linked_resource=_mock_linked_resource(linked_resource_id),
        )
        return app_config
    raise RuntimeError(f"Can't mock unsupported dependency ({subdependency})")


def _mock_workflow_output_subdependency(
    subdependency: Union[BaseManifestConfig, FieldDefinitionsManifest],
    parent_config,
    parent_path: Optional[List[str]] = None,
) -> AppConfigItem:
    parent_path = parent_path if parent_path else []
    linked_resource_id = _random_string("tsf_")
    app_config = FieldAppConfigItem(
        id=_random_string("aci_"),
        path=parent_path + [parent_config.name, "output", subdependency.name],
        type=FieldAppConfigItemType.FIELD,
        value=linked_resource_id,
        linked_resource=_mock_linked_resource(linked_resource_id),
    )
    return app_config


def _mock_linked_resource(id: str, name: Optional[str] = None) -> LinkedAppConfigResourceSummary:
    return LinkedAppConfigResourceSummary(id=id, name=name if name else _random_string("Resource Name"))


def _mock_scalar_value(  # noqa:PLR0911
    dependency: ManifestScalarConfig,
) -> Union[bool, date, datetime, int, float, str, Dict[str, Union[str, float]]]:
    """Mock a scalar config value from its manifest definition."""
    if isinstance(dependency, UnknownType):
        raise UnsupportedConfigItemError(
            f"Unable to mock scalar value for unsupported dependency type {dependency}"
        )
    # These types should be equivalent and this appeases MyPy
    scalar_type = _ScalarConfigTypes(dependency.type)
    if _is_scalar_with_enum(dependency):
        return _mock_scalar_with_enum(dependency)
    elif scalar_type == scalar_type.BOOLEAN:
        return True
    elif scalar_type == scalar_type.DATE:
        return date.today()
    elif scalar_type == scalar_type.DATETIME:
        return datetime.now()
    elif scalar_type == scalar_type.FLOAT:
        return random.random()
    elif scalar_type == scalar_type.INTEGER:
        return random.randint(-1000, 1000)
    elif scalar_type == scalar_type.JSON:
        return json.dumps(
            {_random_string(): [_random_string(), _random_string()], _random_string(): random.random()}
        )
    return _random_string()


def _random_string(prefix: str = "", random_length: int = 20) -> str:
    """Generate a randomized string up to a specified length with an optional prefix."""
    delimited_prefix = f"{prefix}-" if prefix else ""
    return f"{delimited_prefix}{''.join(random.choice(string.ascii_letters) for i in range(random_length))}"


def _config_path(config_item: AppConfigItem) -> List[str]:
    if isinstance(config_item, UnknownType):
        return config_item.value["path"]
    return config_item.path
