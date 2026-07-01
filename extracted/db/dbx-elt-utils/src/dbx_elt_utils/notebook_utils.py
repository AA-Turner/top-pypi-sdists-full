# src/common/notebook_utils.py
import sys
import os
from pathlib import Path
import importlib

VERSION = "2.2.9"

# Variable global para que ingesta_hibrida sepa si debe ser Batch o Stream automáticamente en tests
_GLOBAL_IS_TEST_RUN = False
_SPARK_CACHE = None

def get_checkpoint_base(env_suffix: str = "_dev") -> str:
    """Retorna la ruta base para checkpoints de streaming."""
    base = os.getenv("ELT_CHECKPOINT_BASE")
    if base:
        return base.rstrip("/")
    return f"/Volumes/bronze{env_suffix}/temporary/checkpoints"

def get_schema_location_base(env_suffix: str = "_dev") -> str:
    """Retorna la ruta base para schema location de Auto Loader."""
    base = os.getenv("ELT_SCHEMA_BASE")
    if base:
        return base.rstrip("/")
    checkpoint_base = get_checkpoint_base(env_suffix)
    return f"{checkpoint_base}/schema"

# =============================================================================
# FUNCIONES GLOBALES DE PRUEBA Y DX (Developer Experience)
# =============================================================================

def is_test_run_active() -> bool:
    """Retorna si el entorno actual es un testrun interactivo."""
    return _GLOBAL_IS_TEST_RUN

def get_test_spark():
    global _SPARK_CACHE
    if _SPARK_CACHE is not None:
        return _SPARK_CACHE
    
    # 1. Workspace
    try:
        import IPython
        ip = IPython.get_ipython()
        if ip and ip.user_ns.get('spark') is not None:
            _SPARK_CACHE = ip.user_ns['spark']
            return _SPARK_CACHE
    except:
        pass

    # 2. Local (Databricks Connect)
    try:
        from databricks.connect import DatabricksSession
        from databricks.sdk.core import Config
        config = Config(profile="DEFAULT")
        _SPARK_CACHE = DatabricksSession.builder.sdkConfig(config).getOrCreate()
        return _SPARK_CACHE
    except Exception as e:
        print(f" Error creando sesión Spark Local/Connect: {e}")
        return None

def stop_local_spark():
    """Limpia streams activos pero MANTIENE la sesión viva."""
    global _SPARK_CACHE
    if _SPARK_CACHE is not None:
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            print("ℹ️ Sesión nativa de Databricks. No se detendrá la sesión.")
            return
        try:
            if hasattr(_SPARK_CACHE, "streams") and hasattr(_SPARK_CACHE.streams, "active"):
                active_streams = _SPARK_CACHE.streams.active
                if active_streams:
                    print(f"🛑 Deteniendo {len(active_streams)} proceso(s) de streaming activo(s)...")
                    for stream in active_streams:
                        stream.stop()
                        stream.awaitTermination(5)
        except Exception as e:
            print(f"⚠️ Error deteniendo los streams: {e}")
        print("✅ Recursos de Spark liberados. La sesión sigue activa para la próxima ejecución.")

def get_local_source_table(spark, source_official: str) -> str:
    """Descubre de dónde leer los datos (Temporal vs Unity Catalog oficial)."""
    parts = source_official.split(".")
    env_catalog = parts[0]
    target_table = parts[-1]
    
    oficial_name = source_official
    temp_name = f"{env_catalog}.temporary.{target_table}_tmp_sql"
    
    def table_exists(name):
        try:
            return spark.catalog.tableExists(name)
        except Exception:
            return False

    if table_exists(oficial_name):
        print(f"✅ Leyendo desde tabla oficial Unity Catalog: {oficial_name}")
        return oficial_name
    elif table_exists(temp_name):
        print(f"⚠️ Leyendo desde tabla TEMPORAL de prueba local: {temp_name}")
        return temp_name
    else:
        raise ValueError(
            f"❌ ERROR DE LINAJE LOCAL: No se encontró la tabla de origen.\n"
            f"Solución: Ejecuta el notebook de la capa anterior ({target_table}) para generar los datos."
        )

def clean_local_test_table(spark, source_table: str):
    """Limpia la tabla temporal local tras una prueba."""
    print("-" * 50)
    parts = source_table.split(".")
    env_catalog = parts[0]
    target_table = parts[-1]
    
    temp_name = source_table if target_table.endswith("_tmp_sql") else f"{env_catalog}.temporary.{target_table}_tmp_sql"
    
    # Validación básica de nombre para evitar inyecciones
    import re
    if not re.match(r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$', temp_name):
        print(f"⚠️ Nombre de tabla no válido: {temp_name}")
        return
    
    def table_exists(name):
        try:
            return spark.catalog.tableExists(name)
        except Exception:
            return False

    if table_exists(temp_name):
        print("🧹 Limpiando zona temporal...")
        try:
            spark.sql(f"DROP TABLE IF EXISTS {temp_name}")
            print(f"✨ Tabla local eliminada limpiamente.")
        except Exception as e:
            print(f"⚠️ Error limpiando la tabla temporal: {e}")

def display_test_results(spark, data, limit: int = 5):
    """Muestra un DataFrame o Tabla adaptándose al entorno."""
    try:
        if isinstance(data, str):
            table_name = data
            df = spark.read.table(table_name).limit(limit)
            print(f"\n✅ Resultado de la tabla: {table_name}")
        else:
            df = data.limit(limit)
            print(f"\n✅ Resultado del DataFrame (En memoria):")

        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            try:
                import IPython
                shell = IPython.get_ipython()
                if shell is not None and "display" in shell.user_ns:
                    shell.user_ns["display"](df)
                    return
                elif hasattr(df, "display"):
                    df.display()
                    return
            except Exception:
                pass

        df.show(n=limit, truncate=False)
    except Exception as e:
        print(f"⚠️ No se pudo mostrar el resultado: {e}")


# =============================================================================
# CLASE PRINCIPAL: NOTEBOOK CONTEXT (Tu navaja suiza)
# =============================================================================

class NotebookContext:
    def __init__(self, env, is_local, is_test_run=False, spark=None, dp=None):
        self.env = env
        self.is_local = is_local
        self.is_test_run = is_test_run
        self.spark = spark
        self.dp = dp

    # 🛠️ Métodos inyectados para facilitar el uso en los notebooks
    def get_test_spark(self):
        return get_test_spark()

    def get_source_table(self, source_official: str) -> str:
        return get_local_source_table(self.get_test_spark(), source_official)

    def display(self, data, limit: int = 5):
        display_test_results(self.get_test_spark(), data, limit)

    def clean_source(self, source_table: str):
        clean_local_test_table(self.get_test_spark(), source_table)

    def stop_spark(self):
        stop_local_spark()


# =============================================================================
# SDP MOCK COMPLETO (Para ejecución local en VSCode)
# Soporta tanto la API legacy (import dlt) como la moderna (pyspark.pipelines)
# =============================================================================

class _SdpMock:
    """Mock completo de SDP para ejecución local sin Databricks Runtime.
    Soporta todas las APIs: legacy @dp.table y moderna @dp.table / @dp.materialized_view.
    Todos los decoradores retornan la función original sin modificarla."""

    # --- Dataset Decorators ---
    def table(self, _fn=None, **kwargs):
        """@dp.table -> Streaming Table"""
        if _fn is not None:
            return _fn
        return lambda f: f

    def materialized_view(self, _fn=None, **kwargs):
        """@dp.materialized_view -> Materialized View (batch reads)"""
        if _fn is not None:
            return _fn
        return lambda f: f

    def view(self, _fn=None, **kwargs):
        """@dp.view -> Vista temporal"""
        if _fn is not None:
            return _fn
        return lambda f: f

    def temporary_view(self, _fn=None, **kwargs):
        """@dp.temporary_view -> Vista temporal (nueva API)"""
        if _fn is not None:
            return _fn
        return lambda f: f

    # --- Expectation Decorators ---
    def expect(self, name=None, condition=None, **kwargs):
        """@dp.expect('name', 'condition') -> Warn on violation"""
        def decorator(f):
            return f
        if callable(name):
            return name
        return decorator

    def expect_or_drop(self, name=None, condition=None, **kwargs):
        """@dp.expect_or_drop('name', 'condition') -> Drop violating rows"""
        def decorator(f):
            return f
        if callable(name):
            return name
        return decorator

    def expect_or_fail(self, name=None, condition=None, **kwargs):
        """@dp.expect_or_fail('name', 'condition') -> Fail pipeline on violation"""
        def decorator(f):
            return f
        if callable(name):
            return name
        return decorator

    # --- Flow Functions ---
    def create_streaming_table(self, name=None, **kwargs):
        """dp.create_streaming_table('name') -> Create empty streaming table target"""
        pass

    def create_auto_cdc_flow(self, target=None, source=None, keys=None, 
                             sequence_by=None, stored_as_scd_type="1", **kwargs):
        """dp.create_auto_cdc_flow(...) -> CDC/SCD flow into streaming table"""
        pass

    def create_auto_cdc_from_snapshot_flow(self, target=None, source=None, keys=None, **kwargs):
        """dp.create_auto_cdc_from_snapshot_flow(...) -> CDC from snapshots"""
        pass

    def append_flow(self, _fn=None, name=None, target=None, **kwargs):
        """@dp.append_flow(target='table') -> Append flow into streaming table"""
        if _fn is not None:
            return _fn
        return lambda f: f

    def create_sink(self, name=None, format=None, options=None, **kwargs):
        """dp.create_sink('name', 'delta', {...}) -> External sink"""
        pass

    # --- Legacy compatibility ---
    def apply_changes(self, *args, **kwargs):
        """Legacy alias for create_auto_cdc_flow"""
        pass

    def read(self, table_name):
        """dp.read('table') -> Mock read from pipeline table (legacy, use spark.read.table instead)"""
        return None

    def read_stream(self, table_name):
        """dp.read_stream('table') -> Mock streaming read (legacy, use spark.readStream.table instead)"""
        return None


# =============================================================================
# INICIALIZADOR
# =============================================================================

def _try_import_pipelines_module():
    """Intenta importar el módulo SDP en orden de preferencia:
    1. pyspark.pipelines (nueva API, Databricks Runtime 16.x+)
    2. dlt (fallback para Databricks Runtime <= 15.x)
    Retorna (module, is_mock=False) o (None, True) si ninguno está disponible.

    IMPORTANTE: fuera de un Databricks Runtime (DATABRICKS_RUNTIME_VERSION ausente)
    siempre retorna mock aunque pyspark.pipelines esté instalado, ya que llamar
    @dp.table() fuera de un pipeline declarativo lanza GRAPH_ELEMENT_DEFINED_OUTSIDE_OF_DECLARATIVE_PIPELINE."""
    if "DATABRICKS_RUNTIME_VERSION" not in os.environ:
        return None, True
    # Intentar nueva API primero
    try:
        from pyspark import pipelines as dp
        return dp, False
    except ImportError:
        pass
    # Fallback a legacy
    try:
        import dlt
        return dlt, False
    except ImportError:
        pass
    return None, True


def init_notebook():
    """Inicializa el entorno del notebook y retorna el NotebookContext."""
    # 1. SETUP PATH DE PROYECTO
    try:
        current_path = Path(__file__).resolve().parent
    except NameError:
        current_path = Path(os.getcwd())

    project_root = current_path
    for _ in range(5):
        if (project_root / "src").exists():
            break
        project_root = project_root.parent

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"✅ Root agregado al path: {project_root}")

    is_local = False
    is_test_run = False
    spark_session = None
    pipeline_module = None
    env_suffix = "_dev" 

    # 2. DETECCION DE SPARK (NUBE/CONNECT)
    try:
        import IPython
        ip = IPython.get_ipython()
        if ip and ip.user_ns.get('spark') is not None:
            spark_session = ip.user_ns['spark']
            try: 
                env_suffix = spark_session.conf.get("env_suffix", "_dev")
            except: 
                pass
    except:
        pass

    # 3. DETECCION DE SDP & TEST MODE
    pipeline_module, needs_mock = _try_import_pipelines_module()
    
    if not needs_mock:
        # Módulo real disponible (Databricks Runtime)
        if spark_session:
            try:
                spark_session.conf.get("pipelines.id")
                is_test_run = False  # Ejecutándose dentro de un pipeline real
            except:
                is_test_run = True   # Workspace interactivo con módulo disponible
        
        # SI ES UN TEST RUN (interactivo), debemos usar el Mock para que los decoradores @dp.table no fallen
        if is_test_run:
            pipeline_module = _SdpMock()
    else:
        # Sin módulo SDP -> Modo local (VSCode)
        is_local = True
        is_test_run = True
        pipeline_module = _SdpMock()
        
    global _GLOBAL_IS_TEST_RUN
    _GLOBAL_IS_TEST_RUN = is_test_run

    if is_local:
        print(f"⚠️  Modo Local: 'dp' simulado (SDP mock). Usando env='{env_suffix}'")
    elif is_test_run:
        print(f"🏗️  Modo Workspace (TEST): Entorno interactivo detectado. Usando env='{env_suffix}'")
    
    print(f"📦 dbx-elt-utils v{VERSION} inicializado.")

    return NotebookContext(
        env=env_suffix, 
        is_local=is_local, 
        is_test_run=is_test_run, 
        dp=pipeline_module,
        spark=spark_session
    )
