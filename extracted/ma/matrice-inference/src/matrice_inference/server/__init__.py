import os
import logging
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
    encoding='utf-8'
)

# Set levels
console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# Define a formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Get the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Root level must be the lowest (DEBUG)

# Optional: remove any default handlers if basicConfig was called earlier
if logger.hasHandlers():
    logger.handlers.clear()

logger.addHandler(console_handler)
logger.addHandler(file_handler)