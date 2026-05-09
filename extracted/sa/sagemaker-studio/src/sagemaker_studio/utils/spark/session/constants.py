"""Shared constants for Spark Connect session managers."""

LOG_DIR = "/var/log/studio/data-notebook-kernel-server"

# TODO: Session logging and metrics separation to be handled in a follow-up.
SPARK_CONNECT_LOG_FILE = f"{LOG_DIR}/athena_spark_session.log"
