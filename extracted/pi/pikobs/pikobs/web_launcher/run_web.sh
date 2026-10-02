#!/usr/bin/env bash
# Compatibility wrapper. The preferred command is ./pikobs-web.
exec "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/pikobs-web" start
