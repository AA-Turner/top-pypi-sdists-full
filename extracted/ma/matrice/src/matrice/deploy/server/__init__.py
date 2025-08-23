import os
import logging

# Root logger
logging.basicConfig(level=logging.DEBUG)

# Console handler (INFO+)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# File handler (DEBUG+)
log_path = os.path.join(os.getcwd(), "deploy_server.log")
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to root logger
logging.getLogger().addHandler(console_handler)
logging.getLogger().addHandler(file_handler)
