import logging
import os
import sys

from tecton_core import materialization_context


# TODO(deprecated_after=0.5): handle backward-compatibility for customer copies of builtin transformations that did not use tecton.materialization_context
# but instead directly accessed tecton_spark.materialization_context
sys.modules["tecton_spark.materialization_context"] = materialization_context

if os.environ.get("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "") == "cpp":
    msg = (
        "The 'cpp' implementation of protobuf cannot be made to work in a federated environment. "
        "The 'upb' implementation is about as fast and will almost certainly work; it is usually the default."
    )
    raise AssertionError(msg)

try:
    logging.getLogger("py4j").setLevel(logging.WARN)
except Exception:
    pass
