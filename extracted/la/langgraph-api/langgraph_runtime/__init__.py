import importlib.util
import os
import sys
import types

import structlog

logger = structlog.stdlib.get_logger(__name__)

try:
    RUNTIME_EDITION = os.environ["LANGGRAPH_RUNTIME_EDITION"]
    RUNTIME_PACKAGE = f"langgraph_runtime_{RUNTIME_EDITION}"
except KeyError:
    raise ValueError(
        "LANGGRAPH_RUNTIME_EDITION environment variable is not set."
        " Expected LANGGRAPH_RUNTIME_EDITION to be set to one of:\n"
        " - inmem\n"
        " - postgres\n"
        " - community\n"
    ) from None

from langgraph_api.feature_flags import INMEM_USES_CORE  # noqa: E402

if INMEM_USES_CORE:
    # Go core persists everything; Python only runs graphs.
    backend = types.SimpleNamespace(
        checkpoint=importlib.import_module("langgraph_api.runtime.checkpoint"),
        database=importlib.import_module("langgraph_api.runtime.database"),
        encryption=importlib.import_module("langgraph_api.runtime.encryption"),
        ops=importlib.import_module("langgraph_api.grpc.ops"),
        routes=importlib.import_module("langgraph_api.runtime.routes"),
        store=importlib.import_module("langgraph_api.runtime.store"),
    )
    logger.info("Using the in-memory runtime on Go core")
elif importlib.util.find_spec(RUNTIME_PACKAGE):
    backend = importlib.import_module(RUNTIME_PACKAGE)
    logger.info(f"Using {RUNTIME_PACKAGE}")
else:
    raise ImportError(
        "Langgraph runtime backend not found. Please install with "
        f'`pip install "langgraph-runtime-{RUNTIME_EDITION}"`'
    ) from None

# All runtime backends share the same API
for module_name in (
    "checkpoint",
    "database",
    "lifespan",
    "ops",
    "retry",
    "store",
    "metrics",
    "routes",
):
    mod = getattr(backend, module_name, None)
    if mod is None and module_name in ("lifespan", "retry", "metrics"):
        # The shared modules import the backend modules registered above.
        mod = importlib.import_module("langgraph_api.runtime." + module_name)
    if mod is not None:
        globals()[module_name] = mod
        sys.modules["langgraph_runtime." + module_name] = mod
