from tmo.types.dataset_metadata import CatalogType


def build_df_template(df) -> dict:
    """
    Build dictionary representation for Dataset or DatasetTemplate.

    Args:
        df: Dataset or DatasetTemplate object

    Returns:
        dict: Dictionary representation appropriate for the catalog type
    """
    # Base fields common to all catalog types
    result = {
        "name": df.name,
        "description": df.description,
        "catalogType": df.catalog_type,
    }

    # Add id field (different names for Dataset vs DatasetTemplate)
    if hasattr(df, "dataset_template_id"):
        # This is a Dataset
        result["datasetTemplateId"] = df.dataset_template_id
        result["scope"] = df.scope
    else:
        # This is a DatasetTemplate
        result["id"] = df.id

    # For NO_CATALOG, only include metadata JSON
    if df.catalog_type == CatalogType.NO_CATALOG:
        if isinstance(df.metadata, dict):
            result["metadata"] = df.metadata
    else:
        # For VANTAGE and other catalog types, include structured fields
        result.update({
            "entity": df.entity,
            "target": df.target,
            "features": df.features,
            "featuresQuery": df.features_query,
            "entityTargetsQuery": df.entity_targets_query,
            "predictionsQuery": df.predictions_query,
        })

    return result
