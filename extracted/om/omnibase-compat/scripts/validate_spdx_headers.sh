#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# Validate SPDX headers on Python files.
# Replaces the previous `uv run onex spdx validate` entry which required
# the onex CLI from omnibase_core (not available in this repo).

set -euo pipefail

FAILED=0

for f in "$@"; do
    # Skip non-Python files
    [[ "$f" == *.py ]] || continue
    # Skip __pycache__
    [[ "$f" == *__pycache__* ]] && continue
    # Skip archived directories
    [[ "$f" == archived/* || "$f" == archive/* ]] && continue

    # Check first 10 lines for SPDX markers
    HEAD=$(head -10 "$f" 2>/dev/null || true)
    if ! echo "$HEAD" | grep -q "SPDX-FileCopyrightText"; then
        echo "MISSING SPDX header: $f"
        FAILED=1
    fi
    if ! echo "$HEAD" | grep -q "SPDX-License-Identifier"; then
        echo "MISSING SPDX license: $f"
        FAILED=1
    fi
done

if [ "$FAILED" -eq 1 ]; then
    echo ""
    echo "FIX: Add these lines to the top of each file:"
    echo "  # SPDX-FileCopyrightText: 2025 OmniNode.ai Inc."
    echo "  # SPDX-License-Identifier: MIT"
    exit 1
fi

exit 0
