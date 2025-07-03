import sys
import os

print(
    "Hud does not support this platform yet. The SDK has initiated a graceful shutdown. Your application remains unaffected. See the compatibility matrix for details: https://docs.hud.io/docs/hud-sdk-compatibility-matrix-for-python"
)

def run_previous_sitecustomize() -> None:
    auto_init_dir = os.path.dirname(__file__)
    if auto_init_dir not in sys.path:
        try:
            import sitecustomize  # type: ignore[import-not-found] # noqa: F401
        except ImportError:
            pass
        return

    index = sys.path.index(auto_init_dir)
    del sys.path[index]

    our_sitecustomize = sys.modules["sitecustomize"]
    del sys.modules["sitecustomize"]

    try:
        import sitecustomize  # noqa: F401
    except ImportError:
        sys.modules["sitecustomize"] = our_sitecustomize
    finally:
        sys.path.insert(index, auto_init_dir)

run_previous_sitecustomize()