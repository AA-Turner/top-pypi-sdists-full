import logging
import os
from logging.handlers import RotatingFileHandler

# Define paths
log_path = os.path.join(os.getcwd(), "deploy_server.log")

# Create handlers explicitly
console_handler = logging.StreamHandler()

# Use RotatingFileHandler with 0.5 GB max size and 3 backup files
# When the log reaches 0.5 GB, it's rotated to deploy_server.log.1, deploy_server.log.2, etc.
# Oldest logs are automatically deleted when backup count is exceeded
file_handler = RotatingFileHandler(
    log_path,
    maxBytes=500 * 1024 * 1024,  # 0.5 GB = 500 MB
    backupCount=3,  # Keep 3 backup files (total ~2 GB max: 0.5GB current + 3x0.5GB backups)
    encoding="utf-8",
)

# Set levels — env-driven so per-frame DEBUG doesn't flood disk on the hot path.
# MATRICE_LOG_LEVEL (default INFO) controls file + root level; console stays INFO.
_lvl = getattr(logging, os.environ.get("MATRICE_LOG_LEVEL", "INFO").upper(), logging.INFO)
console_handler.setLevel(logging.INFO)
file_handler.setLevel(_lvl)

# Define a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Get the root logger
logger = logging.getLogger()
logger.setLevel(_lvl)  # env-driven (default INFO); avoids per-frame DEBUG formatting/IO

# Optional: remove any default handlers if basicConfig was called earlier
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Silence noisy third-party loggers regardless of app level (per-request/frame chatter).
for _n in ("httpx", "httpcore", "kafka", "urllib3"):
    logging.getLogger(_n).setLevel(logging.WARNING)
