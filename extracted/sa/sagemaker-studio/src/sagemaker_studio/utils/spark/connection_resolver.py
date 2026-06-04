"""
Connection resolution and session manager creation for Spark Connect.

Extracted from sparkutils to break the circular import between sparkutils
and lazy_spark_session. sparkutils imports LazySparkSession at module level,
and LazySparkSession needs _resolve_connection_and_create_session_manager at
runtime — keeping both in sparkutils created a cycle.
"""

import logging
import warnings
from functools import lru_cache

from sagemaker_studio.project import ClientConfig, Project
from sagemaker_studio.utils._internal import InternalUtils

logger = logging.getLogger()


def _resolve_connection_id_from_notebook(config: ClientConfig) -> str:
    """Resolve the default spark connection ID from notebook metadata.

    Delegates to InternalUtils._resolve_connection_id_from_notebook.
    """
    return InternalUtils()._resolve_connection_id_from_notebook(config)


@lru_cache(maxsize=1)
def _ensure_project():
    """Initialize Project on demand (cached singleton)."""
    return Project()


def _identify_service_from_props(connection) -> str:
    """Identify the backend service from the connection's props structure.

    Uses props-based identification (design doc Section 2.1):
    - sparkEmrProperties.computeArn contains "emr-serverless" → EMR_SERVERLESS
    - sparkEmrProperties.computeArn contains "emr-containers" → EMR_EKS
    - sparkEmrProperties.computeArn contains "elasticmapreduce" → EMR_EC2
    - sparkGlueProperties exists → GLUE
    - athenaProperties exists → ATHENA
    - Default → UNKNOWN (no recognized props)
    """
    try:
        conn_data = getattr(connection, "_Connection__connection_data", {})
        props = conn_data.get("props", {}) if isinstance(conn_data, dict) else {}

        # Check sparkEmrProperties.computeArn for EMR services
        compute_arn = props.get("sparkEmrProperties", {}).get("computeArn", "")
        if compute_arn:
            if "emr-serverless" in compute_arn:
                return "EMR_SERVERLESS"
            if "emr-containers" in compute_arn:
                return "EMR_EKS"
            if "elasticmapreduce" in compute_arn:
                return "EMR_EC2"
            logger.warning(f"Unrecognized computeArn pattern: {compute_arn}")
            return "UNKNOWN"

        # Check for Glue
        if "sparkGlueProperties" in props:
            return "GLUE"

        # Check for Athena
        if "athenaProperties" in props:
            return "ATHENA"

    except Exception as e:
        logger.warning(f"Error identifying service from props: {e}")

    logger.warning("No recognized props in SPARK_CONNECT connection")
    return "UNKNOWN"


def _create_session_manager(
    connection, connection_name, connection_id, config, is_explicit_choice=False, spark_conf=None
):
    """Route to the correct session manager based on connection type and props.

    Uses SPARK_CONNECT type filtering + props-based service identification:
    - SPARK_CONNECT type → identify service from props (computeArn / athenaProperties / sparkGlueProperties)
    - Unknown type:
        - If user explicitly chose this connection → raise error (don't silently give them Athena)
        - If no explicit choice (default path) → fall back to Athena
    """
    from sagemaker_studio.utils.spark.session.athena.athena_spark_session_manager import (
        AthenaSparkSessionManager,
    )
    from sagemaker_studio.utils.spark.session.emr_serverless.emr_serverless_spark_session_manager import (
        EMRServerlessSparkSessionManager,
    )

    conn_type = getattr(connection, "type", None)

    if conn_type == "SPARK_CONNECT":
        service = _identify_service_from_props(connection)
        logger.info(f"Connection type SPARK_CONNECT, identified service={service}")

        if service == "EMR_SERVERLESS":
            return EMRServerlessSparkSessionManager(
                connection=connection,
                connection_name=connection_name,
                config=config,
                spark_conf=spark_conf,
            )

        if service in ("GLUE", "EMR_EKS", "EMR_EC2"):
            raise RuntimeError(
                f"Spark Connect is not yet supported for {service} connections. "
                "Supported backends: Athena, EMR Serverless."
            )

        if service == "UNKNOWN":
            raise RuntimeError(
                "Could not identify the Spark backend from the connection properties. "
                "Ensure the connection has valid athenaProperties or sparkEmrProperties "
                "with a recognized computeArn. Supported backends: Athena, EMR Serverless."
            )

        if service == "ATHENA":
            return AthenaSparkSessionManager(
                connection=connection,
                connection_name=connection_name,
                connection_id=connection_id,
                config=config,
                spark_conf=spark_conf,
            )

        # Should not reach here for SPARK_CONNECT
        raise RuntimeError(
            f"Unhandled Spark Connect service type: {service}. "
            "Supported backends: Athena, EMR Serverless."
        )

    # Unrecognized connection type for Spark Connect
    if is_explicit_choice:
        raise RuntimeError(
            f"Connection type '{conn_type}' is not a recognized Spark Connect type. "
            "Verify that the connection type is SPARK_CONNECT with the appropriate "
            "service properties (e.g., athenaProperties, sparkEmrProperties, sparkGlueProperties)."
        )

    # No explicit choice (default path) — fall back to Athena
    logger.warning(
        f"Connection type '{conn_type}' does not match a Spark Connect-enabled backend — defaulting to Athena session manager"
    )
    warnings.warn(
        f"Connection type '{conn_type}' is not a recognized Spark Connect type. "
        "Falling back to Athena Spark Connect. Verify that the connection type is "
        "SPARK_CONNECT with the appropriate service properties (e.g., athenaProperties, "
        "sparkEmrProperties, sparkGlueProperties).",
        stacklevel=2,
    )
    return AthenaSparkSessionManager(config=config, spark_conf=spark_conf)


def get_spark_options(connection_name: str):
    """Get Spark options for a connection."""
    try:
        project = _ensure_project()
    except Exception as e:
        raise RuntimeError("Project is not initialized.") from e

    connection = project.connection(connection_name)
    return connection._spark_options()


def _resolve_connection_and_create_session_manager(
    connection_name: str = None,
    config: ClientConfig = None,
    spark_conf: dict = None,
):
    """Resolve the connection and create the appropriate session manager.

    Called lazily by LazySparkSession on first spark.* access. All network calls
    (GetNotebook, GetConnection) happen here, not at sparkutils.init() time.
    """
    import time

    config = config or ClientConfig()

    resolve_start = time.time()

    # Resolution priority: explicit name → notebook metadata → default Athena SPARK_CONNECT.
    connection_id = None
    is_explicit_choice = False
    if connection_name:
        logger.info(f"Resolving connection for connection_name={connection_name}")
        is_explicit_choice = True
    else:
        try:
            t0 = time.time()
            resolved_id = _resolve_connection_id_from_notebook(config)
            logger.info(f"Notebook metadata lookup took {int((time.time() - t0) * 1000)}ms")
            if resolved_id:
                connection_id = resolved_id
                is_explicit_choice = True
            else:
                logger.info("Falling back to default SPARK_CONNECT connection")
        except Exception as e:
            logger.warning(f"Notebook metadata lookup failed, falling back to default: {e}")

    project = _ensure_project()
    t0 = time.time()
    if connection_id:
        connection = project.connection(id=connection_id)
    elif connection_name:
        connection = project.connection(connection_name)
    else:
        connection = project.connection(type="SPARK_CONNECT")
    logger.info(f"Connection resolution took {int((time.time() - t0) * 1000)}ms")

    session_manager = _create_session_manager(
        connection,
        connection_name,
        connection_id,
        config,
        is_explicit_choice,
        spark_conf=spark_conf,
    )

    logger.info(
        f"Connection resolution and session manager creation took {int((time.time() - resolve_start) * 1000)}ms"
    )
    return session_manager
