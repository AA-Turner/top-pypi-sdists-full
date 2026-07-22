"""
Mypyc-compiled build configuration for matrice_inference.

This setup.py can build in two modes:
- With mypyc: Compiles Python to native extensions (faster, platform-specific wheels)
- Without mypyc: Pure Python package (cross-platform, slower)

Set ENABLE_MYPYC=true environment variable to enable mypyc compilation.
"""

import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

# Package configuration
PACKAGE_NAME = "matrice_inference"
SOURCE_DIR = f"src/{PACKAGE_NAME}"

# Modules left as pure Python (NOT mypyc-compiled). Each entry below either
# segfaults / fails to build when natively compiled, or relies on dynamic Python
# semantics that mypyc's native classes do not preserve. mypyc gives no benefit
# on this I/O-bound / subprocess-bound / control-plane code anyway.
#
# The large "declared type is violated at runtime" group below is a direct
# consequence of this package's type posture: pyproject.toml's [tool.mypy]
# disables 20 error codes, so the source is NOT type-clean. Where mypy infers a
# narrow type that the code then violates (classically `self.x = None` in
# __init__ and a real object later), pure Python is happy but a mypyc native
# class enforces the type and raises TypeError at that very line. Those modules
# cannot be soundly compiled until the annotations are fixed; excluding them is
# the safe, behaviour-preserving choice. Each is annotated with the exact site.
#
# Their generated .pyi stubs are also stripped before the compiled build so
# that importing (compiled) modules type-check against the real .py source.
MYPYC_EXCLUDE_MODULES = {
    # --- build / import level ------------------------------------------------
    # C-extension interop (tritonclient grpc/http + torch) plus a long-lived
    # Triton subprocess and background monitor threads -> segfault during GC
    # when compiled (taxonomy: C-extension interop with threads).
    "triton_server.py",
    # AsyncProducerPool has a `self._thread` attribute, which mypyc emits as the
    # C struct field `__thread` -- a GCC reserved keyword (thread-local storage
    # specifier). The generated C fails to compile ("expected identifier before
    # '__thread'").
    "async_producer_pool.py",
    # Both use class-body constants as defaults for parameters of methods
    # declared in the SAME class body (StreamingPipeline's
    # `inference_queue_maxsize: int = DEFAULT_QUEUE_SIZE`, RedisFrameCache's
    # `ttl_seconds: int = DEFAULT_TTL_SECONDS`). CPython evaluates those against
    # the live class namespace; a mypyc native class has no such namespace, so
    # the compiled module raises KeyError('DEFAULT_QUEUE_SIZE') at import.
    "stream_pipeline.py",
    "frame_cache.py",
    # --- inferred type violated at runtime -> TypeError when compiled --------
    # model_manager_wrapper.py:255 `self.model_manager = ModelManager(...)`: the
    # attribute is inferred TritonModelManager from its first assignment, so the
    # DEFAULT (non-Triton) path raises
    # "TritonModelManager object expected; got ModelManager".
    "model_manager_wrapper.py",
    # model_manager.py:35-40 pass Optional[Callable] into `_create_*_wrapper`
    # methods declared `Callable` (the wrappers themselves start with
    # `if not func: return None`, so None is a real path), and the error paths of
    # inference()/batch_inference() return None from a `-> Tuple[dict, bool]`.
    "model_manager.py",
    # server.py:1154 `self._ip = "localhost"` and :892
    # `self.camera_config_manager = CameraConfigManager(...)`: both attributes are
    # initialised to None, so mypyc types them None and any real value raises
    # "None object expected; got str / CameraConfigManager".
    "server.py",
    # proxy_interface.py:273/350 pass a FastAPI `UploadFile | str` into
    # `_validate_fetch_url(url: str)` / `inference(extra_params: dict | None)`;
    # the file-upload route raises TypeError once those callees are native.
    "proxy_interface.py",
    # consumer_manager.py:573/1014 assign `Optional[str]` into a `str` local that
    # the code then explicitly None-checks ("if not frame_id: generate one").
    "consumer_manager.py",
    # app_deployment.py:455 `last_log_time = current_time` (int local <- float
    # time.time()) inside the connection-wait loop, and :624 assigns an
    # AbstractEventLoop into a None-initialised attribute.
    "app_deployment.py",
    # camera_config_manager.py:284 `convert_configs_for_engine` is annotated
    # `Dict[str, CameraConfig]` but its body explicitly handles plain dicts and
    # other objects; compiled, it rejects them with
    # "CameraConfig object expected; got dict".
    "camera_config_manager.py",
    # worker_metrics.py:472/489/506 write dicts into `result`, which mypy infers
    # as Dict[str, bool] from its first entry; and :325 passes the
    # `Deque` sample buffer into `_compute_latency_stats(samples: List[float])`
    # ("list object expected; got collections.deque") on every metrics snapshot.
    "worker_metrics.py",
    # inference_metric_logger.py:687/689 write dicts into a Dict[str, int] target.
    "inference_metric_logger.py",
    # metric_publisher.py:145 assigns a confluent-kafka Producer into
    # `self.producer`, which is None-initialised (-> "None object expected").
    "metric_publisher.py",
    # deployment_refresh_listener.py:165 writes a str into a Dict[str, Optional[int]]
    # target.
    "deployment_refresh_listener.py",
    # --- native classes have no __dict__ -------------------------------------
    # utils.py holds the only payload dataclasses (CameraConfig, StreamMessage).
    # A mypyc native class has no `__dict__`, and producer_worker's
    # _make_json_serializable() branches on `hasattr(obj, "__dict__")` to expand
    # custom objects via vars(); compiled, that branch is skipped and the object
    # is published as its str() repr instead of a nested dict -- a silent change
    # to the output payload. (They still pickle/deepcopy correctly; it is only
    # __dict__/vars() that is lost.) Keeping this 190-line module pure preserves
    # the serialization semantics for ~zero performance cost.
    "utils.py",
}


# Check if mypyc compilation is enabled.
# Falls back to build-config.json if env var is not set.
def _resolve_enable_mypyc() -> bool:
    env_val = os.environ.get("ENABLE_MYPYC")
    if env_val is not None:
        return env_val.lower() in ("true", "1", "yes")
    config_path = Path(__file__).parent / "build-config.json"
    if config_path.exists():
        import json

        try:
            with open(config_path) as f:
                config = json.load(f)
            return bool(config.get("build", {}).get("enable_mypyc", False))
        except Exception:
            pass
    return False


ENABLE_MYPYC = _resolve_enable_mypyc()


def get_version() -> str:
    """Get version from PACKAGE_VERSION environment variable."""
    version = os.environ.get("PACKAGE_VERSION", "0.0.0.dev0")
    print(f"Building version: {version}")
    return version


def ensure_py_typed():
    """Create py.typed marker file for PEP 561 compliance."""
    py_typed = Path(SOURCE_DIR) / "py.typed"
    if not py_typed.exists():
        py_typed.write_text("")
        print("Created py.typed file")


def run_stub_generator():
    """Run stub generator script to create .pyi files."""
    script_path = Path(__file__).parent / "stub_generation.py"
    if not script_path.exists():
        print(f"Warning: Stub generator not found: {script_path}")
        return

    print(f"Running stub generator: {script_path}")
    subprocess.run([sys.executable, str(script_path)], check=True)


def discover_modules() -> "list[str]":
    """Discover Python modules for mypyc compilation."""
    src_root = Path(SOURCE_DIR)
    if not src_root.exists():
        return []

    exclude = {"__pycache__", "tests", "test", "docs"}
    modules = []

    for path in src_root.rglob("*.py"):
        if any(part in exclude for part in path.parts):
            continue
        # Leave package __init__.py files as pure Python. They are thin
        # re-export shims, and compiling them makes mypyc resolve their
        # relative imports against the wrong package, breaking import at
        # runtime. The compiled leaf submodules are imported by these
        # shims normally.
        if path.name == "__init__.py":
            continue
        if path.name in MYPYC_EXCLUDE_MODULES:
            continue
        modules.append(str(path).replace("\\", "/"))

    print(f"Discovered {len(modules)} Python files for mypyc compilation")
    return modules


def get_ext_modules():
    """Get extension modules - mypyc compiled or empty for pure Python."""
    if not ENABLE_MYPYC:
        print("Building PURE PYTHON package (mypyc disabled)")
        return []

    print("Building MYPYC COMPILED package")
    from mypyc.build import mypycify

    # Strip the auto-generated .pyi stubs of the pure (excluded) modules. The
    # generator emits lossy stubs (dropping kwargs/attributes); if left in
    # place, the compiled modules that import these excluded ones type-check
    # against the lossy stub and fail. Removing them makes mypy resolve those
    # imports against the real .py source instead.
    _excluded_stems = {Path(m).stem for m in MYPYC_EXCLUDE_MODULES}
    for stub_path in Path(SOURCE_DIR).rglob("*.pyi"):
        if stub_path.stem in _excluded_stems:
            stub_path.unlink()
            print(f"Stripped lossy stub for excluded module: {stub_path}")

    # Dedicated type-checking config: keeps third-party packages opaque so the
    # build only checks our own modules.
    config_path = Path(__file__).parent / "typecheck.ini"
    mypyc_options = [
        f"--config-file={config_path}",
    ]
    return mypycify(mypyc_options + discover_modules(), opt_level="3")


# Build preparation
ensure_py_typed()
run_stub_generator()

# Setup
setup(
    name=PACKAGE_NAME,
    version=get_version(),
    package_dir={"": "src"},
    # Only ship the matrice_inference package; exclude any orphan top-level
    # packages or template scaffolding that may exist under src/.
    packages=find_packages(where="src", include=[PACKAGE_NAME, f"{PACKAGE_NAME}.*"]),
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi"],
    },
    ext_modules=get_ext_modules(),
    zip_safe=False,
    python_requires=">=3.8",
)
