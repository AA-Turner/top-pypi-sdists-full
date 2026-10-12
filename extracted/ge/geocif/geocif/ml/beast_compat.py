"""Shims around the ``Rbeast`` binary wheel, shared by every BEAST call site.

Two problems, handled in one place:

* ``Rbeast`` is a compiled extension that is not always importable (no
  wheel for the interpreter, a numpy-ABI mismatch, or deliberately
  uninstalled). Call sites import it through :func:`import_rbeast`, which
  returns ``None`` after one warning per process instead of raising, so a
  caller can degrade (plain least squares instead of a segmented trend,
  or skip a diagnostic) rather than fail a whole run.

* Rbeast 0.1.25 on Python 3.13 reports, on *every* ``beast()`` call::

      Exception ignored in PyObject_HasAttrString(); consider using ...
      SystemError: .../Objects/dictobject.c:4114: bad argument to internal function

  The extension probes an attribute with a dict API on a non-dict. Python
  3.12 and older swallow that silently; 3.13 routes it through
  ``sys.unraisablehook``. The results are identical on 3.11, 3.12 and 3.13
  (checked 2026-10-11 on Linux x86_64 with numpy 2.1.3 and 2.4.6, Rbeast
  0.1.25), so the report is noise, but in ``yield_outlook`` it is one
  traceback per region in the log and reads like a failure (first seen on
  Google Colab, Python 3.13.15). :func:`quiet_rbeast` drops exactly that
  report for the duration of one call and passes every other unraisable
  exception to the previous hook untouched.
"""
import contextlib
import logging
import sys

logger = logging.getLogger(__name__)

_IMPORT_WARNED = False

# Substring of the ``err_msg`` Python 3.13 attaches to the Rbeast report.
_RBEAST_NOISE_MARK = "PyObject_HasAttrString"


def import_rbeast(log=None):
    """Return the ``Rbeast`` module, or ``None`` when it cannot be imported.

    Any import failure counts (``ImportError`` for a missing wheel, but also
    the ``SystemError`` an Rbeast built against numpy 1.x raises under
    numpy 2.x). The first failure in a process is logged as a warning on
    ``log`` (or this module's logger); later ones are silent.
    """
    global _IMPORT_WARNED
    try:
        import Rbeast as rb  # noqa: PLC0415 — lazy by design
    except Exception as exc:  # noqa: BLE001
        if not _IMPORT_WARNED:
            (log or logger).warning(
                "Rbeast is not importable (%s: %s): BEAST changepoint "
                "detection is off; trends fall back to plain least squares "
                "and BEAST-only diagnostics are skipped.",
                type(exc).__name__, exc,
            )
            _IMPORT_WARNED = True
        return None
    return rb


def _is_rbeast_noise(unraisable):
    return (
        isinstance(unraisable.exc_value, SystemError)
        and _RBEAST_NOISE_MARK in str(getattr(unraisable, "err_msg", "") or "")
    )


@contextlib.contextmanager
def quiet_rbeast():
    """Silence the Rbeast 0.1.25 / Python 3.13 unraisable report for one call.

    Only a ``SystemError`` reported from ``PyObject_HasAttrString`` is
    dropped; everything else goes to whatever hook was installed before
    (pytest's, for instance). The previous hook is restored on exit.
    """
    previous = sys.unraisablehook

    def hook(unraisable):
        if _is_rbeast_noise(unraisable):
            return
        previous(unraisable)

    sys.unraisablehook = hook
    try:
        yield
    finally:
        sys.unraisablehook = previous
