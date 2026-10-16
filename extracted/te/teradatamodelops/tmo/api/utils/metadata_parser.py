"""
Utility module for parsing metadata from API responses.
Handles both VANTAGE and NO_CATALOG catalog types.
"""

import logging
from typing import Union

from tmo.types.dataset_metadata import (
    CatalogBodyType,
    CatalogType,
    DataType,
    FeaturesEntityTargets,
    Metadata,
    Predictions,
    TypeEnum,
    Variable,
)

logger = logging.getLogger(__name__)

STRING_DATA_TYPE_ALIAS = "string"


def parse_metadata_from_response(
    metadata_dict: dict,
    catalog_type: CatalogType,
    target_object,
) -> Union[Metadata, dict]:  # noqa
    """
    Parse metadata from API response based on catalog type.

    Parameters:
        metadata_dict (dict): Raw metadata dictionary from API response
        catalog_type (CatalogType): The catalog type (VANTAGE or NO_CATALOG)
        target_object: The object to set entity and target on (Dataset or DatasetTemplate)

    Returns:
        Union[Metadata, dict]: Parsed Metadata object for VANTAGE, or dict for NO_CATALOG
    """
    if not metadata_dict:
        logger.warning("Metadata dictionary is empty or None.")
        # Initialize entity and target to avoid AttributeError
        target_object.entity = None
        target_object.target = []
        return Metadata() if catalog_type == CatalogType.VANTAGE else {}

    if catalog_type == CatalogType.VANTAGE:
        return _parse_vantage_metadata(metadata_dict, target_object)
    elif catalog_type == CatalogType.NO_CATALOG:
        return _parse_no_catalog_metadata(metadata_dict, target_object)
    else:
        logger.warning(f"Unknown catalog type: {catalog_type}")
        return metadata_dict


def _parse_vantage_metadata(metadata_dict: dict, target_object) -> Metadata:
    """
    Parse VANTAGE catalog metadata into structured Metadata object.

    Parameters:
        metadata_dict (dict): Raw metadata dictionary from API response
        target_object: The object to set entity and target on

    Returns:
        Metadata: Structured metadata object
    """
    metadata = Metadata()
    metadata.type = CatalogBodyType(metadata_dict.get("type"))

    features_data = metadata_dict.get("features") or {}
    entity_targets_data = metadata_dict.get("entityAndTargets") or {}
    entity = features_data.get("entity")
    target_object.entity = entity

    # Extract targets
    if "variables" in entity_targets_data:
        target_variables = []
        for variable in entity_targets_data.get("variables", []):
            if variable.get("type") == TypeEnum.TARGET.value:
                target_variables.append(variable.get("name"))
        target_object.target = target_variables
    else:
        target_object.target = []

    metadata.features = FeaturesEntityTargets()
    metadata.entity_and_targets = FeaturesEntityTargets()
    metadata.predictions = Predictions()

    # Parse entity and target columns
    entity_target_columns = _dict_list_to_variable_list(
        entity_targets_data.get("variables", [])
    )

    metadata.entity_and_targets.variables = entity_target_columns
    metadata.entity_and_targets.entity = entity
    metadata.entity_and_targets.sql = entity_targets_data.get("sql")

    # Parse feature columns
    feature_columns = _dict_list_to_variable_list(features_data.get("variables", []))

    metadata.features.variables = feature_columns
    metadata.features.entity = entity
    metadata.features.sql = features_data.get("sql")

    # Parse predictions
    predictions_data = metadata_dict.get("predictions") or {}
    metadata.predictions.database = predictions_data.get("database")
    metadata.predictions.entity_sql = predictions_data.get("entitySql")
    metadata.predictions.table = predictions_data.get("table")

    return metadata


def _parse_no_catalog_metadata(metadata_dict: dict, target_object) -> dict:
    """
    Parse NO_CATALOG metadata by storing as JSON dict.

    Parameters:
        metadata_dict (dict): Raw metadata dictionary from API response
        target_object: The object to set entity and target on

    Returns:
        dict: The metadata as-is (JSON dict)
    """
    # Initialize entity and target to avoid AttributeError
    target_object.entity = None
    target_object.target = []

    return metadata_dict


def _parse_data_type(value, variable_name: str = None) -> DataType:
    """
    Convert a raw dataType value to DataType, falling back to VARCHAR.

    "string" is a known alias of VARCHAR and maps silently. Any other unknown
    value must not make the whole entity unparsable, so it logs a warning and
    is treated as VARCHAR.

    Parameters:
        value: Raw dataType value from the API response
        variable_name (str): Variable name, used for the warning message

    Returns:
        DataType: The matching DataType, or DataType.VARCHAR if unsupported
    """
    normalized = str(value).lower()
    if normalized == STRING_DATA_TYPE_ALIAS:
        return DataType.VARCHAR
    try:
        return DataType(normalized)
    except ValueError:
        logger.warning(
            f"Unsupported dataType '{value}' for variable '{variable_name}', "
            f"falling back to '{DataType.VARCHAR.value}'."
        )
        return DataType.VARCHAR


def _dict_list_to_variable_list(variables: list[dict]) -> list[Variable]:
    """
    Convert a list of variable dictionaries to Variable objects.

    Parameters:
        variables (list[dict]): List of variable dictionaries

    Returns:
        list[Variable]: List of Variable objects
    """
    return [
        Variable()
        .set_name(var.get("name"))
        .set_data_type(_parse_data_type(var.get("dataType"), var.get("name")))
        .set_type(TypeEnum(var.get("type")))
        for var in variables
    ]
