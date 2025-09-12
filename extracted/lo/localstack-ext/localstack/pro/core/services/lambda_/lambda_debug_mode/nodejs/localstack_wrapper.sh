#!/bin/bash
major_version=$(node --version | cut -d'.' -f1 | sed 's/v//')

# Override the entrypoint to first wait for the debugger to be ready before proceeding if lower than v20
if [[ "$major_version" -ge 20 ]]; then
   export NODE_OPTIONS="${NODE_OPTIONS} --inspect-wait=0.0.0.0:${AWS_LAMBDA_DEBUG_PORT:-9229}"
else
   echo "require('inspector').waitForDebugger();" > /tmp/debug-init.js
   export NODE_OPTIONS="${NODE_OPTIONS} --inspect=0.0.0.0:${AWS_LAMBDA_DEBUG_PORT:-9229} --require /tmp/debug-init.js"
fi
exec "$@"
