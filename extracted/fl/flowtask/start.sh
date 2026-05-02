#!/bin/bash

REDIS_HOST="$REDIS_HOST"
REDIS_PORT="6379"
QW_WORKER_LIST="QW_WORKER_LIST"

# redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" ltrim "$QW_WORKER_LIST" 1 0
# ulimit -Sn 65535 &&  TZ=America/New_York python  /code/run.py
ulimit -Sn 65535 && gunicorn nav:navigator -c gunicorn_config.py -k aiohttp.GunicornUVLoopWebWorker --preload
