# src/common/ingest_utils.py
import hashlib
from pyspark.sql.functions import current_timestamp, lit, col
from dbx_elt_utils.notebook_utils import get_schema_location_base, get_checkpoint_base


def _derive_schema_location(env_suffix: str, origen: str) -> str:
    """Genera una ruta de schema location única basada en hash del path completo.
    Evita colisiones cuando dos fuentes tienen el mismo nombre de directorio final."""
    path_hash = hashlib.md5(origen.encode()).hexdigest()[:12]
    safe_name = origen.rstrip("/").split("/")[-1].replace(".", "_")
    return f"{get_schema_location_base(env_suffix)}/{safe_name}_{path_hash}"


def _detect_ingestion_type(origen: str) -> str:
    """Detección inteligente del tipo de ingesta basada en el origen.
    
    Orden de evaluación:
    1. Si termina en .delta o contiene _delta_log -> delta_path
    2. Si es una URI de cloud storage (abfss://, s3://, gs://) -> auto_loader
    3. Si contiene / (es un path) -> auto_loader
    4. Si es formato catalog.schema.table -> delta_table
    """
    origen_lower = origen.lower().rstrip("/")
    
    # Delta path detection (rutas que apuntan a tablas Delta en storage)
    if origen_lower.endswith(".delta") or "_delta_log" in origen_lower:
        return "delta_path"
    
    # Explicit cloud storage URIs -> Auto Loader
    if any(origen_lower.startswith(p) for p in ["abfss://", "s3://", "gs://", "wasbs://"]):
        return "auto_loader"
    
    # Mount paths or DBFS paths (that are NOT delta) -> Auto Loader
    if origen.startswith("/mnt/") or origen.startswith("/dbfs/") or origen.startswith("/Volumes/"):
        return "auto_loader"
    
    # If contains dots and no slashes -> Unity Catalog table reference
    if "." in origen and "/" not in origen:
        return "delta_table"
    
    # Generic path fallback
    if "/" in origen:
        return "auto_loader"
    
    return "delta_table"


def ingesta_hibrida(spark, origen, tipo="auto_detect", formato_archivo="json", env_suffix="_dev", streaming=True):
    """
    Ingestor Universal v2.0 - Soporta Delta tables, Delta paths, Auto Loader y Batch directo.
    
    Args:
        origen (str): Nombre de tabla (cat.esq.tab) O Ruta (abfss://... | /mnt/... | /Volumes/...)
        tipo (str): "delta_table", "delta_path", "auto_loader", "batch_files" o "auto_detect"
        formato_archivo (str): csv, json, parquet, avro (Para Auto Loader y batch_files)
        env_suffix (str): Sufijo de ambiente ("_dev", "_prod") para rutas de checkpoint
        streaming (bool): True=streaming (@dp.table), False=batch (@dp.materialized_view). Obligatorio según el decorador usado.
    
    Returns:
        DataFrame con columnas de auditoría (_source_type, _ingested_at)
    """
    from dbx_elt_utils.notebook_utils import is_test_run_active

    # 1. Resolución Automática de Modo (Protección contra Hanging)
    is_test = is_test_run_active()
    if is_test and streaming:
        streaming = False

    # 2. Auto-detección inteligente de tipo
    if tipo == "auto_detect":
        tipo = _detect_ingestion_type(origen)

    mode_str = "STREAMING" if streaming else "BATCH"
    if is_test:
        print(f"🏗️  Contexto de TEST detectado. Forzando lectura en modo {mode_str}.")
    
    print(f"🏭 Ingesta Híbrida activada ({mode_str}): {tipo.upper()} -> {origen}")

    # 3. Lógica de Lectura
    reader = spark.readStream if streaming else spark.read

    # --- CASO A: UNITY CATALOG TABLE (Tablas por nombre: catalog.schema.table) ---
    if tipo == "delta_table":
        return (
            reader.table(origen)
            .withColumn("_source_type", lit("unity_catalog"))
            .withColumn("_ingested_at", current_timestamp())
        )

    # --- CASO B: AUTO LOADER (Archivos sueltos en cloud storage) ---
    elif tipo == "auto_loader":
        schema_loc = _derive_schema_location(env_suffix, origen)
        
        cloud_reader = (
            reader.format("cloudFiles")
            .option("cloudFiles.format", formato_archivo)
            .option("cloudFiles.inferColumnTypes", "true")
            .option("cloudFiles.schemaEvolutionMode", "addNewColumns")
            .option("cloudFiles.schemaLocation", schema_loc)
        )

        # Ajustes específicos para CSV
        if formato_archivo == "csv":
            cloud_reader = cloud_reader.option("header", "true").option("delimiter", ",")

        return (
            cloud_reader.load(origen)
            .withColumn("_source_type", lit(f"file_{formato_archivo}"))
            .withColumn("_source_file", col("_metadata.file_path"))
            .withColumn("_ingested_at", current_timestamp())
        )

    # --- CASO C: DELTA PATH (Tablas Delta por ruta: /mnt/.../tabla.delta) ---
    elif tipo == "delta_path":
        return (
            reader.format("delta").load(origen)
            .withColumn("_source_type", lit("delta_path"))
            .withColumn("_ingested_at", current_timestamp())
        )

    # --- CASO D: BATCH FILES (Lectura directa sin Auto Loader, ej. Parquet/ORC/Avro) ---
    elif tipo == "batch_files":
        batch_reader = spark.read.format(formato_archivo)
        
        if formato_archivo == "csv":
            batch_reader = batch_reader.option("header", "true").option("inferSchema", "true")
        
        return (
            batch_reader.load(origen)
            .withColumn("_source_type", lit(f"batch_{formato_archivo}"))
            .withColumn("_source_file", col("_metadata.file_path"))
            .withColumn("_ingested_at", current_timestamp())
        )

    else:
        raise ValueError(f"Tipo de ingesta desconocido: '{tipo}'. Valores válidos: delta_table, delta_path, auto_loader, batch_files, auto_detect")
