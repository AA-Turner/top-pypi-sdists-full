import os

# Resolvendo as variáveis de ambiente
MAX_CLIENT_THREADS = int(os.getenv("MAX_CLIENT_THREADS", "50"))

CHECK_TASKS_INTERVAL = int(os.getenv("CHECK_TASKS_INTERVAL", "15"))

LOCK_SERVICE_WAIT_CONN_INTERVAL = int(
    os.getenv("LOCK_SERVICE_WAIT_CONN_INTERVAL", "30")
)
