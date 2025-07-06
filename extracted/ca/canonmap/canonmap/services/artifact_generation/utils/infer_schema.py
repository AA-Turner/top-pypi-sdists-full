from typing import Dict, Any

import pandas as pd

from canonmap.utils.logger import setup_logger
from canonmap.services.artifact_generation.utils.db_types.mariadb.mariadb_schema_datatypes import MariaDBSchemaInferrer
from canonmap.services.artifact_generation.utils.clean_columns import clean_and_format_columns
from canonmap.services.artifact_generation.utils.augment_examples import augment_schema_with_examples

logger = setup_logger(__name__)

def generate_db_schema_from_df(
        df: pd.DataFrame,
        db_type: str,
        normalize_field_names: bool = False
    ) -> Dict[str, Dict[str, Any]]:
    """
    Generate a database schema from a pandas DataFrame.
    Currently supports MariaDB schema generation.
    
    Args:
        df: Input DataFrame to infer schema from
        db_type: Type of database (currently only "mariadb" supported)
        normalize_field_names: Whether to clean and format column names
        
    Returns:
        Dict containing the inferred schema with field types and examples
    """
    if normalize_field_names:
        df = clean_and_format_columns(df)

    if db_type.lower().strip() == "mariadb":
        original_schema = MariaDBSchemaInferrer().infer_mariadb_schema(df)
        # return original_schema
        augmented_schema = augment_schema_with_examples(df, original_schema)
        return augmented_schema
    else:
        raise ValueError(f"Unsupported database type: {db_type}")