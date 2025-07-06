import pickle
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
import zipfile
from datetime import datetime
from typing import Union
from dataclasses import dataclass
import time
from contextlib import contextmanager

import pandas as pd

from canonmap.utils.logger import setup_logger
from canonmap.config.validate_configs import CanonMapArtifactsConfig
from canonmap.config.utils.gcs import upload_to_gcs
from canonmap.requests.artifact_generation_request import ArtifactGenerationRequest
from canonmap.responses.artifact_generation_response import ArtifactGenerationResponse
from canonmap.services.artifact_generation.utils.convert_input import convert_data_to_df
from canonmap.services.artifact_generation.utils.process_table import process_table
from canonmap.services.artifact_generation.utils.clean_columns import clean_and_format_columns, _clean_column_name
from canonmap.services.artifact_generation.utils.infer_schema import generate_db_schema_from_df
from canonmap.services.artifact_generation.utils.db_types.mariadb.generate_mariadb_loader_script import generate_mariadb_loader_script

logger = setup_logger(__name__)

@contextmanager
def log_stage(stage_name: str):
    """
    Context manager to log the duration of a pipeline stage.
    """
    start = time.time()
    logger.info(f"Stage '{stage_name}' started")
    try:
        yield
    finally:
        duration = time.time() - start
        logger.info(f"Stage '{stage_name}' finished in {duration:.2f}s")

@dataclass
class ArtifactPaths:
    schema: Path
    entity_fields_schema: Path
    semantic_fields_schema: Path
    processed_data: Path
    canonical_entities: Path
    canonical_entity_embeddings: Path
    data_loader_script: Path
    semantic_texts: Path


def _ingest_tables(
    raw_input: Union[str, Path],
    request: 'ArtifactGenerationRequest'
) -> Dict[str, pd.DataFrame]:
    """
    Handle normalization and validation of the input path,
    then ingest it into a dict of DataFrames.
    """
    # Convert Path to str
    if isinstance(raw_input, Path):
        raw_input = str(raw_input)

    # Directory vs file handling
    if isinstance(raw_input, str) and Path(raw_input).is_dir():
        logger.info(f"Directory input detected at '{raw_input}'")
        if not request.file_pattern:
            logger.warning("A 'file_pattern' must be provided when passing a directory.")
        else:
            logger.info(f"Using file pattern '{request.file_pattern}' to match files.")

    # Validate existence
    input_path = Path(raw_input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {raw_input}")

    # Ingest to DataFrame(s)
    tables = convert_data_to_df(
        raw_input,
        request.num_rows,
        request.recursive,
        request.file_pattern
    )

    # Handle table naming based on input type and configuration
    if isinstance(tables, pd.DataFrame):
        # Single file case
        if request.table_name:
            name = request.table_name
        elif input_path.is_file():
            name = input_path.stem
        else:
            name = "data"
        tables = {name: tables}
    else:
        # Directory case - multiple DataFrames
        if request.table_name and not request.table_name_from_file:
            # If table_name is provided and table_name_from_file is False,
            # use the provided table_name as a prefix for all tables
            renamed_tables = {}
            for i, (original_name, df) in enumerate(tables.items()):
                if len(tables) == 1:
                    # Single table from directory, use the provided name
                    new_name = request.table_name
                else:
                    # Multiple tables, use prefix with counter
                    new_name = f"{request.table_name}_{i+1}"
                renamed_tables[new_name] = df
            tables = renamed_tables
            logger.info(f"Renamed tables using provided table_name '{request.table_name}' as prefix")
        elif request.table_name and request.table_name_from_file:
            # If table_name is provided but table_name_from_file is True,
            # log a warning that table_name is being ignored
            logger.warning(f"table_name '{request.table_name}' provided but table_name_from_file=True, using file-based names")
        elif not request.table_name and not request.table_name_from_file:
            # If table_name is None and table_name_from_file is False,
            # use source_name as base for generic names with counters
            renamed_tables = {}
            for i, (original_name, df) in enumerate(tables.items()):
                if len(tables) == 1:
                    # Single table from directory, use source_name
                    new_name = request.source_name
                else:
                    # Multiple tables, use source_name with counter
                    new_name = f"{request.source_name}_table_{i+1}"
                renamed_tables[new_name] = df
            tables = renamed_tables
            logger.info(f"No table_name provided and table_name_from_file=False, using '{request.source_name}' as base for generic names")
        # If not request.table_name and request.table_name_from_file is True (default),
        # keep the original file-based names

    return tables


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


def _normalize(name: str) -> str:
    """Lowercase, strip, and replace spaces with underscores."""
    return name.lower().strip().replace(" ", "_")


def _get_paths(
    base: Path, source: str, table: str, db_type: str
) -> ArtifactPaths:
    """
    Returns an ArtifactPaths object with all artifact paths for a single table.
    """
    base.mkdir(parents=True, exist_ok=True)
    return ArtifactPaths(
        schema=base / f"{source}_{table}_schema.pkl",
        entity_fields_schema=base / f"{source}_{table}_entity_fields_schema.pkl",
        semantic_fields_schema=base / f"{source}_{table}_semantic_fields_schema.pkl",
        processed_data=base / f"{source}_{table}_processed_data.pkl",
        canonical_entities=base / f"{source}_{table}_canonical_entities.pkl",
        canonical_entity_embeddings=base / f"{source}_{table}_canonical_entity_embeddings.npz",
        data_loader_script=base / f"load_{table}_table_to_{db_type}.py",
        semantic_texts=base / f"{source}_{table}_semantic_texts.zip",
    )


def _write_combined_artifacts(
    config: ArtifactGenerationRequest,
    output_path: Path,
    entities: Dict[str, list[dict]],
    embeddings: Dict[str, np.ndarray],
    tables: Dict[str, pd.DataFrame],
) -> Dict[str, Path]:
    combined: Dict[str, Path] = {}

    # 1) processed_data
    if config.save_processed_data:
        processed_path = output_path / f"{config.source_name}_processed_data.pkl"
        combined_data = {
            "metadata": {"source_name": config.source_name, "tables": list(tables.keys())},
            "tables": {
                name: clean_and_format_columns(df)
                if config.normalize_field_names else df
                for name, df in tables.items()
            },
        }
        with open(processed_path, "wb") as f:
            pickle.dump(combined_data, f)
        combined["processed_data"] = processed_path

    # 2) schema
    if config.generate_schemas:
        schema = {config.source_name: {}}
        for name, df in tables.items():
            schema[config.source_name][name] = generate_db_schema_from_df(
                df, config.database_type, config.normalize_field_names
            )
        schema_path = output_path / f"{config.source_name}_schema.pkl"
        with open(schema_path, "wb") as f:
            pickle.dump(schema, f)
        combined["schema"] = schema_path
        
        # Create filtered schemas for entity fields and semantic fields
        if config.entity_fields:
            # Extract unique field names from entity_fields
            entity_field_names = list(set([
                ef.field_name for ef in config.entity_fields
                if ef.table_name in tables.keys()
            ]))
            
            if entity_field_names:
                entity_schema = {}
                for table_name in tables.keys():
                    table_entity_fields = [
                        ef.field_name for ef in config.entity_fields
                        if ef.table_name == table_name
                    ]
                    if table_entity_fields:
                        entity_schema.update(_create_filtered_schema(
                            schema, config.source_name, table_name, 
                            table_entity_fields, config.normalize_field_names
                        ))
                
                if entity_schema:
                    entity_schema_path = output_path / f"{config.source_name}_entity_fields_schema.pkl"
                    with open(entity_schema_path, "wb") as f:
                        pickle.dump(entity_schema, f)
                    combined["entity_fields_schema"] = entity_schema_path
        
        if config.semantic_fields:
            # Extract unique field names from semantic_fields
            semantic_field_names = list(set([
                sf.field_name for sf in config.semantic_fields
                if sf.table_name in tables.keys()
            ]))
            
            if semantic_field_names:
                semantic_schema = {}
                for table_name in tables.keys():
                    table_semantic_fields = [
                        sf for sf in config.semantic_fields
                        if sf.table_name == table_name
                    ]
                    if table_semantic_fields:
                        semantic_schema.update(_create_filtered_schema(
                            schema, config.source_name, table_name, 
                            [sf.field_name for sf in table_semantic_fields], config.normalize_field_names
                        ))
                
                if semantic_schema:
                    semantic_schema_path = output_path / f"{config.source_name}_semantic_fields_schema.pkl"
                    with open(semantic_schema_path, "wb") as f:
                        pickle.dump(semantic_schema, f)
                    combined["semantic_fields_schema"] = semantic_schema_path

    # 3) flat canonical entities
    if config.generate_canonical_entities:
        flat_list: list[dict] = []
        for tbl in tables.keys():
            flat_list.extend(entities.get(tbl, []))

        ents_path = output_path / f"{config.source_name}_canonical_entities.pkl"
        with open(ents_path, "wb") as f:
            pickle.dump(flat_list, f)
        combined["canonical_entities"] = ents_path

    # 4) flat combined embeddings
    if config.generate_embeddings and embeddings:
        arrays = [embeddings[tbl] for tbl in tables.keys()]
        flat_embs = np.vstack(arrays) if arrays else np.empty((0,))
        emb_path = output_path / f"{config.source_name}_canonical_entity_embeddings.npz"
        np.savez_compressed(emb_path, embeddings=flat_embs)
        combined["canonical_entity_embeddings"] = emb_path

    # 5) loader script
    if config.generate_schemas:
        loader_path = output_path / f"load_{config.source_name}_to_{config.database_type}.py"
        script = generate_mariadb_loader_script(
            schema[config.source_name], list(tables.keys()), str(loader_path), is_combined=True
        )
        loader_path.write_text(script)
        combined["data_loader_script"] = loader_path

    # 6) combined semantic texts
    if config.generate_semantic_texts and config.semantic_fields:
        combined_semantic_path = output_path / f"{config.source_name}_semantic_texts.zip"
        
        with zipfile.ZipFile(combined_semantic_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            used_filenames = {}  # Track used filenames to handle duplicates
            
            for table_name, df in tables.items():
                # Create case-insensitive column mapping for this table
                column_map = {col.lower(): col for col in df.columns}
                
                # Filter semantic fields for this table
                table_semantic_fields = [
                    sf for sf in config.semantic_fields
                    if sf.table_name == table_name
                ]
                
                # Create a dictionary to store all semantic field values for each row
                row_semantic_fields = {}
                row_title_values = {}  # Store title field values for each row
                
                # Get title field for this table if specified
                title_field = None
                if config.semantic_text_title_fields:
                    for tf in config.semantic_text_title_fields:
                        if tf.table_name == table_name:
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
                                logger.warning(f"Title field '{title_field_name}' not found in table '{table_name}'")
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
                
                # Create one text file per row containing all semantic fields
                for row_idx, field_values in row_semantic_fields.items():
                    if field_values:  # Only create file if there are non-empty values
                        # Use title field value if available, otherwise use row index
                        if row_idx in row_title_values:
                            base_filename = f"{table_name}_{row_title_values[row_idx]}"
                        else:
                            base_filename = f"{table_name}_row_{row_idx}"
                        
                        # Handle duplicate filenames by adding a counter
                        filename = f"{base_filename}.txt"
                        counter = used_filenames.get(base_filename, 0)
                        while filename in zipf.namelist():
                            counter += 1
                            filename = f"{base_filename}_{counter}.txt"
                        used_filenames[base_filename] = counter
                        
                        content = "\n".join(field_values)
                        zipf.writestr(filename, content)
        
        combined["semantic_texts"] = combined_semantic_path

    return combined


def _process_all_tables(
    tables: Dict[str, pd.DataFrame],
    request: ArtifactGenerationRequest,
    artifacts_config: CanonMapArtifactsConfig
) -> tuple[Dict[str, ArtifactPaths], Dict[str, list[dict]], list[tuple[str, list[str]]]]:
    """
    Process each table: run process_table and collect artifact paths, entities, and embedding jobs.
    """
    result_paths: Dict[str, ArtifactPaths] = {}
    entity_map: Dict[str, list[dict]] = {}
    embedding_jobs: list[tuple[str, list[str]]] = []

    is_multi = len(tables) > 1
    for table_name, df in tables.items():
        logger.info(f"Processing table: {table_name}")
        local_cfg = request.model_copy(deep=True)
        local_cfg.table_name = table_name

        base_dir = Path(artifacts_config.artifacts_local_path) / table_name if is_multi else Path(artifacts_config.artifacts_local_path)
        artifact_paths = _get_paths(
            base_dir,
            request.source_name,
            table_name,
            request.database_type
        )

        # Convert to dict for process_table, then wrap back into ArtifactPaths
        raw_paths_dict, entities, emb_strs = process_table(df, local_cfg, vars(artifact_paths))
        paths = ArtifactPaths(**raw_paths_dict)

        result_paths[table_name] = paths
        entity_map[table_name] = entities

        if request.generate_embeddings:
            embedding_jobs.append((table_name, emb_strs))

    return result_paths, entity_map, embedding_jobs


def _execute_embeddings(
    embedding_jobs: list[tuple[str, list[str]]],
    embedder,
    result_paths: Dict[str, ArtifactPaths]
) -> Dict[str, np.ndarray]:
    """
    Run embeddings for all jobs and save each result back to its artifact path.
    """
    embedding_map: Dict[str, np.ndarray] = {}
    if embedding_jobs and embedder:
        logger.info(f"Embedding canonical entities for {len(embedding_jobs)} tables…")
        embedding_map = embedder.embed_texts(embedding_jobs)
        for tbl, arr in embedding_map.items():
            emb_path = result_paths[tbl].canonical_entity_embeddings
            np.savez_compressed(emb_path, embeddings=arr)
    return embedding_map


def generate_artifacts_helper(
    request: ArtifactGenerationRequest,
    artifacts_config: CanonMapArtifactsConfig,
    embedder=None,
) -> ArtifactGenerationResponse:
    """
    Generate artifacts based on the request and current configuration.
    
    Args:
        request: ArtifactGenerationRequest specifying what to generate
        artifacts_config: Configuration for artifacts storage
        embedder: Optional embedder instance for generating embeddings
        
    Returns:
        ArtifactGenerationResponse containing generation results and metadata
        
    Raises:
        ValueError: If request validation fails
        FileNotFoundError: If input path doesn't exist
        Exception: If generation process fails
    """
    # Validate request and ingest data
    if not request.input_path:
        raise ValueError("input_path is required in ArtifactGenerationRequest")

    with log_stage("ingestion"):
        tables = _ingest_tables(request.input_path, request)
    logger.info(f"Ingested {len(tables)} tables")
    logger.debug(f"Tables keys: {list(tables.keys())}")

    # Use artifacts_config for storage settings
    output_path = artifacts_config.artifacts_local_path

    is_multi = len(tables) > 1

    # 3) optionally normalize all table names and entity_fields
    if request.normalize_table_names:
        normalized: Dict[str, pd.DataFrame] = {}
        for raw_name, df in tables.items():
            norm = _normalize(raw_name)
            normalized[norm] = df
        tables = normalized

        if request.entity_fields:
            for ef in request.entity_fields:
                ef.table_name = _normalize(ef.table_name)
        
        if request.semantic_fields:
            for sf in request.semantic_fields:
                sf.table_name = _normalize(sf.table_name)

    logger.info(f"Normalized tables: {tables}")
    logger.info(f"Entity fields: {request.entity_fields}")
    logger.info(f"Semantic fields: {request.semantic_fields}")

    # 4) per-table processing
    with log_stage("per-table processing"):
        result_paths, entity_map, embedding_jobs = _process_all_tables(
            tables, request, artifacts_config
        )

    # 5) embeddings
    with log_stage("embeddings"):
        embedding_map = _execute_embeddings(embedding_jobs, embedder, result_paths)

    # 6) combined (multi-table) artifacts
    if is_multi:
        with log_stage("combined artifacts"):
            output_dir = Path(output_path)
            result_paths[request.source_name] = _write_combined_artifacts(
                request, output_dir, entity_map, embedding_map, tables
            )

    logger.info("Artifact generation pipeline finished")

    # 7) optionally upload to GCS
    with log_stage("gcs upload"):
        if request.upload_artifacts_to_gcs:
            count = upload_to_gcs(
                artifacts_config.artifacts_gcp_service_account_json_path,
                artifacts_config.artifacts_gcp_bucket_name,
                artifacts_config.artifacts_gcp_bucket_prefix,
                Path(output_path)
            )
            logger.info(f"Uploaded {count} artifact files to GCS")
            gcp_upload_info = {"uploaded_files_count": count}
        else:
            gcp_upload_info = None

    # Build response
    response = ArtifactGenerationResponse(
        status="success",
        message="Artifact generation completed successfully",
        source_name=request.source_name,
        table_names=list(tables.keys()),
        gcp_upload_info=gcp_upload_info,
        timestamp=datetime.now()
    )

    # Add generated artifacts to response
    total_entities = sum(len(entities) for entities in entity_map.values())
    total_embeddings = sum(len(embeddings) for embeddings in embedding_map.values()) if embedding_map else 0
    
    # Mapping from artifact types to response attribute names
    field_map = {
        "schema": "schema_path",
        "entity_fields_schema": "entity_fields_schema_path",
        "semantic_fields_schema": "semantic_fields_schema_path",
        "processed_data": "processed_data_path",
        "canonical_entities": "canonical_entities_path",
        "canonical_entity_embeddings": "canonical_entity_embeddings_path",
        "semantic_texts": "semantic_texts_path",
        "data_loader_script": "data_loader_script_path",
    }

    # Add individual table artifacts
    for table_name, paths in result_paths.items():
        # Support both ArtifactPaths and raw dict for combined artifacts
        if hasattr(paths, '__dict__'):
            items = vars(paths).items()
        else:
            items = paths.items()
        for artifact_type, path in items:
            if path.exists():
                file_size = path.stat().st_size if path.exists() else None
                response.add_artifact(
                    artifact_type=artifact_type,
                    file_path=str(path),
                    table_name=table_name,
                    source_name=request.source_name,
                    file_size_bytes=file_size
                )
                attr = field_map.get(artifact_type)
                if attr:
                    setattr(response, attr, str(path))

    # Set processing stats
    response.set_processing_stats(
        total_tables=len(tables),
        total_rows=sum(len(df) for df in tables.values()),
        total_entities=total_entities,
        total_embeddings=total_embeddings,
        processing_time=0.0,  # TODO: Add actual timing
        start_time=datetime.now(),  # TODO: Add actual start time
        end_time=datetime.now()
    )

    return response 
