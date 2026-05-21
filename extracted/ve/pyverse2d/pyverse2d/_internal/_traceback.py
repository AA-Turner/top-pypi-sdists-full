# ======================================== IMPORTS ========================================
import sys
import linecache
from pathlib import Path
from types import TracebackType

# ======================================== CONSTANTS ========================================
_ENGINE_ROOT: Path = Path(__file__).resolve().parent.parent

# ======================================== GLOBAL ========================================
_enabled: bool = False
_original_excepthook = sys.excepthook

# ======================================== EXCPECT HOOK ========================================
def excepthook(exc_type: type[BaseException], exc: BaseException, tb: TracebackType | None):
    """Hook d'exception"""
    if not _is_engine_related(tb):
        return sys.__excepthook__(exc_type, exc, tb)

    print("Traceback (most recent call last):")

    filtered = []
    while tb:
        if not _should_hide(tb):
            filtered.append(tb)
        tb = tb.tb_next

    for tb in filtered:
        frame = tb.tb_frame
        code = frame.f_code

        filename = code.co_filename
        lineno = tb.tb_lineno
        func = code.co_name

        line = linecache.getline(filename, lineno).strip()

        print(
            f'  File "{filename}", '
            f'line {lineno}, in {func}'
        )

        if line:
            print(f"    {line}")

    print(f"{exc_type.__name__}: {exc}")

def enable():
    """Activation du traceback personnalisé"""
    global _enabled
    if sys.excepthook is excepthook:
        return
    sys.excepthook = excepthook
    _enabled = True

def disable():
    """Désactivation du traceback personnalisé"""
    global _enabled
    if not _enabled:
        return
    sys.excepthook = _original_excepthook
    _enabled = False

def set_enabled(value: bool):
    """Basculement du traceback personnalisé"""
    if value:
        enable()
    else:
        disable()

# ======================================== INTERNALS ========================================
def _is_engine_related(tb: TracebackType) -> bool:
    """Vérification que l'erreur est relative à l'engine"""
    while tb:
        filename = Path(tb.tb_frame.f_code.co_filename)
        try:
            filename.relative_to(_ENGINE_ROOT)
            return True
        except ValueError:
            pass
        tb = tb.tb_next
    return False

def _should_hide(tb: TracebackType) -> bool:
    """Tri des frames"""
    frame = tb.tb_frame
    if frame.f_locals.get("__tracebackhide__"):
        return True
    filename = frame.f_code.co_filename.replace("\\", "/")
    return "/_internal/" in filename

# ======================================== EXPORTS ========================================
__all__ = [
    "excepthook",

    "enable",
    "disable",
    "set_enabled",
]