#!/usr/bin/env python3
"""Quick diagnostic: list every OpenAI model the configured key can call.

Useful when a model that appears enabled in the OpenAI dashboard returns
403/404 model_not_found at the API layer (project-scope mismatch between
the dashboard view and the API key's scope).

Usage:
    OPENAI_API_KEY=sk-... uv run python scripts/list_openai_models.py
    # or with the optional [openai] extra installed system-wide:
    OPENAI_API_KEY=sk-... python scripts/list_openai_models.py
"""

from __future__ import annotations

import os
import sys

try:
    from openai import OpenAI
except ModuleNotFoundError:
    sys.exit(
        "install the openai SDK first: uv sync --extra openai (or pip install 'openai>=1.40,<3')"
    )

if not os.environ.get("OPENAI_API_KEY"):
    sys.exit("set OPENAI_API_KEY in the environment before running")

client = OpenAI()
models = list(client.models.list())
gpt5 = sorted(m.id for m in models if m.id.startswith("gpt-5"))

print(f"total models accessible: {len(models)}")
print(f"gpt-5* models ({len(gpt5)}):")
for mid in gpt5:
    print(f"  {mid}")
print()
print(f"all models ({len(models)}):")
for m in sorted(models, key=lambda m: m.id):
    print(f"  {m.id}")
