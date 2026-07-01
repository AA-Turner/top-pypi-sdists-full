# dbx_elt_utils - Utilidades ELT para Databricks
# Framework para pipelines Bronze/Silver/Gold con soporte local (VSCode) y Databricks Runtime

from dbx_elt_utils.notebook_utils import (
    init_notebook,
    NotebookContext,
    get_test_spark,
    display_test_results,
    stop_local_spark,
    get_local_source_table,
    clean_local_test_table,
    get_checkpoint_base,
    get_schema_location_base,
)
try:
    from dbx_elt_utils.ingest_utils import ingesta_hibrida
except ImportError:
    pass  # pyspark no disponible fuera de Databricks/Spark
try:
    from dbx_elt_utils.clean_utils import (
        extraer_valor_array_string,
        parse_json_array_column,
        normalize_string,
        safe_cast,
        dedup_by_key,
        add_surrogate_key,
    )
except ImportError:
    pass  # pyspark no disponible fuera de Databricks/Spark
from dbx_elt_utils.expectations_utils import ExpectationsFactory

VERSION = "2.0.0"
__version__ = VERSION

__all__ = [
    # Core
    "init_notebook",
    "NotebookContext",
    "VERSION",
    # Ingestion (solo disponible con pyspark)
    "ingesta_hibrida",
    # Test/DX
    "get_test_spark",
    "display_test_results",
    "stop_local_spark",
    "get_local_source_table",
    "clean_local_test_table",
    # Paths
    "get_checkpoint_base",
    "get_schema_location_base",
    # Clean
    "extraer_valor_array_string",
    "parse_json_array_column",
    "normalize_string",
    "safe_cast",
    "dedup_by_key",
    "add_surrogate_key",
    # Expectations
    "ExpectationsFactory",
]
