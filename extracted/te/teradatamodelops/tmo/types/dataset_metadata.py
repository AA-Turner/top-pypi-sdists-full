from enum import Enum

from tmo.decorators.functional import functional


class DataType(Enum):
    FLOAT = "float"
    INTEGER = "integer"
    VARCHAR = "varchar"


class TypeEnum(Enum):
    ENTITY = "entity"
    FEATURE = "feature"
    TARGET = "target"


class CatalogType(Enum):
    VANTAGE = "VANTAGE"
    NO_CATALOG = "NONE"


class CatalogBodyType(Enum):
    VANTAGE = "CatalogBody"
    NO_CATALOG = "NoCatalogBody"


@functional
class Variable(object):
    name: str = None  # NOSONAR
    data_type: DataType = None  # NOSONAR
    type: TypeEnum = None  # NOSONAR
    selected: str = None  # NOSONAR
    entity_id: str = None  # NOSONAR


@functional
class FeaturesEntityTargets(object):
    entity: str = None  # NOSONAR
    sql: str = None  # NOSONAR
    variables: list[Variable] = []

    def set_columns(self, columns: list[Variable]) -> object:
        join = self.variables + columns
        self.variables = join
        return self

    def add_column(self, variable: Variable) -> object:
        v = [variable]
        join = self.variables + v
        self.variables = join
        return self


@functional
class Predictions(object):
    database: str = None  # NOSONAR
    entity_sql: str = None  # NOSONAR
    table: str = None  # NOSONAR


@functional
class Metadata(object):
    entity_and_targets: FeaturesEntityTargets = None  # NOSONAR
    features: FeaturesEntityTargets = None  # NOSONAR
    predictions: Predictions = None  # NOSONAR
    type: CatalogBodyType = None  # NOSONAR


@functional
class FeatureMetadata(object):
    database: str = None  # NOSONAR
    table: str = None  # NOSONAR


# Mapping functions between CatalogType and CatalogBodyType
# Both enums share the same keys (VANTAGE, NO_CATALOG), simplifying mapping


def catalog_type_to_body_type(catalog_type: CatalogType) -> CatalogBodyType:
    """
    Converts a CatalogType to its corresponding CatalogBodyType using enum name mapping.

    Args:
        catalog_type: The CatalogType to convert

    Returns:
        CatalogBodyType: The corresponding body type

    Raises:
        ValueError: If catalog_type is invalid or not recognized

    Examples:
        >>> catalog_type_to_body_type(CatalogType.VANTAGE)
        <CatalogBodyType.VANTAGE: 'CatalogBody'>
        >>> catalog_type_to_body_type(CatalogType.NO_CATALOG)
        <CatalogBodyType.NO_CATALOG: 'NoCatalogBody'>
    """
    try:
        return CatalogBodyType[catalog_type.name]
    except KeyError:
        raise ValueError(f"Unknown CatalogType: {catalog_type}")


def body_type_to_catalog_type(body_type: CatalogBodyType) -> CatalogType:
    """
    Converts a CatalogBodyType to its corresponding CatalogType using enum name mapping.

    Args:
        body_type: The CatalogBodyType to convert

    Returns:
        CatalogType: The corresponding catalog type

    Raises:
        ValueError: If body_type is invalid or not recognized

    Examples:
        >>> body_type_to_catalog_type(CatalogBodyType.VANTAGE)
        <CatalogType.VANTAGE: 'VANTAGE'>
        >>> body_type_to_catalog_type(CatalogBodyType.NO_CATALOG)
        <CatalogType.NO_CATALOG: 'NONE'>
    """
    try:
        return CatalogType[body_type.name]
    except KeyError:
        raise ValueError(f"Unknown CatalogBodyType: {body_type}")


def get_body_type_from_string(body_type_str: str) -> CatalogBodyType:
    """
    Converts a string representation to CatalogBodyType by value lookup.

    Args:
        body_type_str: String like "CatalogBody" or "NoCatalogBody"

    Returns:
        CatalogBodyType: The corresponding body type

    Raises:
        ValueError: If string doesn't match any known body type

    Examples:
        >>> get_body_type_from_string("CatalogBody")
        <CatalogBodyType.VANTAGE: 'CatalogBody'>
        >>> get_body_type_from_string("NoCatalogBody")
        <CatalogBodyType.NO_CATALOG: 'NoCatalogBody'>
    """
    for body_type in CatalogBodyType:
        if body_type.value == body_type_str:
            return body_type
    raise ValueError(f"Unknown body type string: {body_type_str}")


def get_catalog_type_from_string(catalog_type_str: str) -> CatalogType:
    """
    Converts a string representation to CatalogType by value lookup.

    Args:
        catalog_type_str: String like "VANTAGE" or "NONE"

    Returns:
        CatalogType: The corresponding catalog type

    Raises:
        ValueError: If string doesn't match any known catalog type

    Examples:
        >>> get_catalog_type_from_string("VANTAGE")
        <CatalogType.VANTAGE: 'VANTAGE'>
        >>> get_catalog_type_from_string("NONE")
        <CatalogType.NO_CATALOG: 'NONE'>
    """
    for catalog_type in CatalogType:
        if catalog_type.value == catalog_type_str:
            return catalog_type
    raise ValueError(f"Unknown catalog type string: {catalog_type_str}")


def catalog_type_string_to_body_type(catalog_type_str: str) -> CatalogBodyType:
    """
    Converts a CatalogType string directly to its corresponding CatalogBodyType.

    This is a convenience function that combines get_catalog_type_from_string()
    and catalog_type_to_body_type().

    Args:
        catalog_type_str: String like "VANTAGE" or "NONE"

    Returns:
        CatalogBodyType: The corresponding body type

    Raises:
        ValueError: If string doesn't match any known catalog type

    Examples:
        >>> catalog_type_string_to_body_type("VANTAGE")
        <CatalogBodyType.VANTAGE: 'CatalogBody'>
        >>> catalog_type_string_to_body_type("NONE")
        <CatalogBodyType.NO_CATALOG: 'NoCatalogBody'>
    """
    catalog_type = get_catalog_type_from_string(catalog_type_str)
    return catalog_type_to_body_type(catalog_type)


def body_type_string_to_catalog_type(body_type_str: str) -> CatalogType:
    """
    Converts a CatalogBodyType string directly to its corresponding CatalogType.

    This is a convenience function that combines get_body_type_from_string()
    and body_type_to_catalog_type().

    Args:
        body_type_str: String like "CatalogBody" or "NoCatalogBody"

    Returns:
        CatalogType: The corresponding catalog type

    Raises:
        ValueError: If string doesn't match any known body type

    Examples:
        >>> body_type_string_to_catalog_type("CatalogBody")
        <CatalogType.VANTAGE: 'VANTAGE'>
        >>> body_type_string_to_catalog_type("NoCatalogBody")
        <CatalogType.NO_CATALOG: 'NONE'>
    """
    body_type = get_body_type_from_string(body_type_str)
    return body_type_to_catalog_type(body_type)
