import sys
import importlib
import pkgutil

from importlib.metadata import version as _get_version
from packaging.version import Version as _Version

PROTOBUF_MAJOR_VERSION = _Version(_get_version("protobuf")).major


def _import_proto() -> None:
    """Patch sys.modules so that imports like `query_cache_protobuf.query_cache.shared_pb2`
    resolve to code generated for the installed protobuf major version."""
    try:
        compat_root = importlib.import_module(
            f"{__name__}._proto{PROTOBUF_MAJOR_VERSION}.query_cache_protobuf"
        )
    except ModuleNotFoundError:
        raise ImportError(
            f"Missing generated protobuf code for protobuf {PROTOBUF_MAJOR_VERSION}.x. "
            f"Expected package '{__name__}._proto{PROTOBUF_MAJOR_VERSION}' not found. "
            "Try reinstalling the query-cache-protobuf package."
        ) from None
    for _, name, _ in pkgutil.walk_packages(
        compat_root.__path__,
        prefix=f"{__name__}._proto{PROTOBUF_MAJOR_VERSION}.query_cache_protobuf.",
    ):
        module = importlib.import_module(name)
        # Remap e.g. query_cache_protobuf._proto4.query_cache_protobuf.query_cache.shared_pb2
        #          -> query_cache_protobuf.query_cache.shared_pb2
        suffix = name.split(f"._proto{PROTOBUF_MAJOR_VERSION}.query_cache_protobuf.", 1)[1]
        sys.modules[f"{__name__}.{suffix}"] = module


if PROTOBUF_MAJOR_VERSION >= 4 and PROTOBUF_MAJOR_VERSION < 6:
    _import_proto()
elif PROTOBUF_MAJOR_VERSION != 6:
    raise ImportError(
        f"Unsupported protobuf major version: {PROTOBUF_MAJOR_VERSION}. "
        "Supported major versions are 4, 5, and 6."
    )
