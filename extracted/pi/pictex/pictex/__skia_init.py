import os
import sys
import contextlib

_skia_icu_primed = False
def prime_skia_icu_engine():
    global _skia_icu_primed
    if _skia_icu_primed:
        return

    try:
        import skia
        
        with _suppress_stderr():
            skia.Unicode.ICU_Make()

    except Exception:
        pass
    finally:
        _skia_icu_primed = True

@contextlib.contextmanager
def _suppress_stderr():
    original_stderr_fd = sys.stderr.fileno()
    saved_stderr_fd = os.dup(original_stderr_fd)
    try:
        devnull_fd = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull_fd, original_stderr_fd)
        yield
    finally:
        os.dup2(saved_stderr_fd, original_stderr_fd)
        os.close(saved_stderr_fd)
        if 'devnull_fd' in locals():
            os.close(devnull_fd)
