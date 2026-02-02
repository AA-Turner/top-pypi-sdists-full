from ..imports import *
db_max_clients = 500/int(get_env_val("DB_MAX_CLIENTS") or '20', 10);
idle_timeout_ms = int(get_env_val("IDLE_TIMEOUT_MS") or '10000', 10); 
connection_timeout_ms = int(get_env_val("CONECTION_TIMEOUT_MS") or '5000', 10);
