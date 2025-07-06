import pickle
from typing import Dict, Any, List

import pandas as pd

from canonmap.utils.logger import setup_logger
from canonmap.services.artifact_generation.utils.clean_columns import clean_and_format_columns, _clean_column_name
from canonmap.services.artifact_generation.utils.infer_schema import generate_db_schema_from_df
from canonmap.services.artifact_generation.utils.canonical_entities_generator import generate_canonical_entities
from canonmap.services.artifact_generation.utils.db_types.mariadb.generate_mariadb_loader_script import generate_mariadb_loader_script

logger = setup_logger(__name__)


def _create_filtered_schema(
    full_schema: Dict[str, Dict[str, Any]],
    source_name: str,
    table_name: str,
    field_names: List[str],
    normalize_field_names: bool = False
) -> Dict[str, Dict[str, Any]]:
    """
    Create a filtered schema containing only the specified fields.
    
    Args:
        full_schema: The complete schema dictionary
        source_name: Name of the data source
        table_name: Name of the table
        field_names: List of field names to include
        normalize_field_names: Whether field names were cleaned
        
    Returns:
        Filtered schema dictionary
    """
    if not field_names:
        return {}
    
    # Create case-insensitive mapping for field matching
    table_schema = full_schema.get(source_name, {}).get(table_name, {})
    field_mapping = {}
    
    for field_name in field_names:
        # Try different variations of the field name
        cleaned_field = _clean_column_name(field_name) if normalize_field_names else field_name
        field_variations = [field_name, cleaned_field]
        
        for variation in field_variations:
            # Case-insensitive matching
            for actual_field in table_schema.keys():
                if actual_field.lower() == variation.lower():
                    field_mapping[field_name] = actual_field
                    break
            if field_name in field_mapping:
                break
    
    # Create filtered schema
    filtered_schema = {source_name: {table_name: {}}}
    for original_field, actual_field in field_mapping.items():
        if actual_field in table_schema:
            filtered_schema[source_name][table_name][actual_field] = table_schema[actual_field]
    
    return filtered_schema


def process_table(df, config, paths):
    # 1) Clean field names and dedupe
    if config.normalize_field_names:
        df = clean_and_format_columns(df)
        if df.columns.duplicated().any():
            seen: Dict[str, int] = {}
            new_cols: list[str] = []
            for col in df.columns:
                seen[col] = seen.get(col, 0)
                new_cols.append(col if seen[col] == 0 else f"{col}_{seen[col]}")
                seen[col] += 1
            df.columns = new_cols

    # 2) Schema
    schema: Dict[str, Any] = {}
    if config.generate_schemas:
        schema = {
            config.source_name: {
                config.table_name: generate_db_schema_from_df(
                    df, config.database_type, config.normalize_field_names
                )
            }
        }
        with open(paths["schema"], "wb") as f:
            pickle.dump(schema, f)
        
        # Create filtered schemas for entity fields and semantic fields
        if config.entity_fields:
            # Extract field names for this table
            table_entity_fields = [
                ef.field_name for ef in config.entity_fields
                if ef.table_name == config.table_name
            ]
            
            if table_entity_fields:
                entity_schema = _create_filtered_schema(
                    schema, config.source_name, config.table_name,
                    table_entity_fields, config.normalize_field_names
                )
                
                if entity_schema:
                    with open(paths["entity_fields_schema"], "wb") as f:
                        pickle.dump(entity_schema, f)
        
        if config.semantic_fields:
            # Extract field names for this table
            table_semantic_fields = [
                sf.field_name for sf in config.semantic_fields
                if sf.table_name == config.table_name
            ]
            
            if table_semantic_fields:
                semantic_schema = _create_filtered_schema(
                    schema, config.source_name, config.table_name,
                    table_semantic_fields, config.normalize_field_names
                )
                
                if semantic_schema:
                    with open(paths["semantic_fields_schema"], "wb") as f:
                        pickle.dump(semantic_schema, f)
        
        # if DEV:
        #     json_path = paths["schema"].with_suffix(".json")
        #     with open(json_path, "w") as f:
        #         json.dump(schema, f, indent=4)
        #     logger.info(f"Saved schema for {config.table_name} to {json_path}")

    # 3) Processed data
    if config.save_processed_data:
        df.to_pickle(paths["processed_data"])

    # 4) Canonical entities + prepare embeddings
    entities: list[dict] = []
    embedding_strings: list[str] = []
    if config.generate_canonical_entities:
        entities = generate_canonical_entities(
            df,
            schema,
            config.database_type,
            [
                ef.model_dump()
                for ef in config.entity_fields
                if ef.table_name == config.table_name
            ],
            config.source_name,
            config.table_name,
            config.use_other_fields_as_metadata,
            config.normalize_field_names,
            comma_separated_fields=[
                cf.model_dump()
                for cf in config.comma_separated_fields
                if cf.table_name == config.table_name
            ] if config.comma_separated_fields else None,
        )
        with open(paths["canonical_entities"], "wb") as f:
            pickle.dump(entities, f)
        # if DEV:
        #     json_path = paths["canonical_entities"].with_suffix(".json")
        #     with open(json_path, "w") as f:
        #         json.dump(entities, f, indent=4)
        #     logger.info(f"Saved canonical entities for {config.table_name} to {json_path}")

        if config.generate_embeddings:
            import json as _json
            embedding_strings = [
                _json.dumps({e["_field_name_"]: e["_canonical_entity_"]})
                for e in entities
            ]

    # 5) Write loader script
    if config.generate_schemas:
        script = generate_mariadb_loader_script(
            schema[config.source_name][config.table_name],
            config.table_name,
            str(paths["data_loader_script"]),
        )
        paths["data_loader_script"].write_text(script)

    # 6) Process semantic fields and create text files
    if config.generate_semantic_texts and config.semantic_fields:
        import zipfile
        from canonmap.services.artifact_generation.utils.clean_columns import _clean_column_name
        
        # Create case-insensitive column mapping
        column_map = {col.lower(): col for col in df.columns}
        
        # Filter semantic fields for this table
        table_semantic_fields = [
            sf for sf in config.semantic_fields
            if sf.table_name == config.table_name
        ]
        
        if table_semantic_fields:
            # Create a dictionary to store all semantic field values for each row
            row_semantic_fields = {}
            row_title_values = {}  # Store title field values for each row
            used_filenames = {}  # Track used filenames to handle duplicates
            
            # Get title field for this table if specified
            title_field = None
            if config.semantic_text_title_fields:
                for tf in config.semantic_text_title_fields:
                    if tf.table_name == config.table_name:
                        title_field_name = tf.field_name
                        cleaned_title = _clean_column_name(title_field_name)
                        field_to_check = cleaned_title if config.normalize_field_names else title_field_name
                        
                        # Try to find the title field (case-insensitive)
                        field_lower = title_field_name.lower()
                        cleaned_lower = cleaned_title.lower()
                        field_to_check_lower = field_to_check.lower()
                        
                        if field_to_check_lower in column_map:
                            title_field = column_map[field_to_check_lower]
                        elif field_lower in column_map:
                            title_field = column_map[field_lower]
                        elif cleaned_lower in column_map:
                            title_field = column_map[cleaned_lower]
                        
                        if title_field and title_field in df.columns:
                            # Get title values for each row
                            for row_idx, row in df.iterrows():
                                value = row[title_field]
                                if not pd.isna(value):
                                    value_str = str(value).strip()
                                    if value_str and value_str.lower() not in {"", "nan", "none", "null"}:
                                        # Clean the value to make it filesystem-safe
                                        safe_value = "".join(c for c in value_str if c.isalnum() or c in " -_")
                                        safe_value = safe_value.strip().replace(" ", "_")
                                        row_title_values[row_idx] = safe_value
                        else:
                            logger.warning(f"Title field '{title_field_name}' not found in table '{config.table_name}'")
                        break  # Only use the first matching title field
            
            for sf in table_semantic_fields:
                field_name = sf.field_name
                cleaned_field = _clean_column_name(field_name)
                field_to_check = cleaned_field if config.normalize_field_names else field_name
                
                # Try to find the field in the DataFrame (case-insensitive)
                field_lower = field_name.lower()
                cleaned_lower = cleaned_field.lower()
                field_to_check_lower = field_to_check.lower()
                
                actual_field = None
                if field_to_check_lower in column_map:
                    actual_field = column_map[field_to_check_lower]
                elif field_lower in column_map:
                    actual_field = column_map[field_lower]
                elif cleaned_lower in column_map:
                    actual_field = column_map[cleaned_lower]
                
                if actual_field and actual_field in df.columns:
                    # Process each row for this semantic field
                    for row_idx, row in df.iterrows():
                        value = row[actual_field]
                        
                        # Skip null/empty values
                        if pd.isna(value):
                            continue
                        
                        value_str = str(value).strip()
                        if not value_str or value_str.lower() in {"", "nan", "none", "null"}:
                            continue
                        
                        # Initialize dict for this row if not exists
                        if row_idx not in row_semantic_fields:
                            row_semantic_fields[row_idx] = []
                        
                        # Add field and value to the row's data
                        row_semantic_fields[row_idx].append(f"{actual_field}: {value_str}")
                        
                    # if DEV:
                    #     logger.info(f"Processed semantic field '{actual_field}' for table '{config.table_name}'")
                else:
                    logger.warning(f"Semantic field '{field_name}' not found in table '{config.table_name}'")
            
            # Create zip file with one text file per row containing all semantic fields
            with zipfile.ZipFile(paths["semantic_texts"], 'w', zipfile.ZIP_DEFLATED) as zipf:
                for row_idx, field_values in row_semantic_fields.items():
                    if field_values:  # Only create file if there are non-empty values
                        # Use title field value if available, otherwise use row index
                        if row_idx in row_title_values:
                            base_filename = f"{config.table_name}_{row_title_values[row_idx]}"
                        else:
                            base_filename = f"{config.table_name}_row_{row_idx}"
                        
                        # Handle duplicate filenames by adding a counter
                        filename = f"{base_filename}.txt"
                        counter = used_filenames.get(base_filename, 0)
                        while filename in zipf.namelist():
                            counter += 1
                            filename = f"{base_filename}_{counter}.txt"
                        used_filenames[base_filename] = counter
                        
                        content = "\n".join(field_values)
                        zipf.writestr(filename, content)

    return paths, entities, embedding_strings