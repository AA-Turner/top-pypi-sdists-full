#!/bin/bash
# Extract the original interpreter at $1 and all args thereafter with ${@:2}
exec "$1" -Xfrozen_modules=off /opt/python/debugpy --listen "0.0.0.0:${AWS_LAMBDA_DEBUG_PORT:-5678}" --wait-for-client "${@:2}"