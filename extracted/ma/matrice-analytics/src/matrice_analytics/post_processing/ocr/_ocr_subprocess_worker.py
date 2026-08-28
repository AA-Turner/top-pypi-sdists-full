"""Long-lived OCR worker, run in an isolated interpreter (numpy<2 venv).

Launched by :mod:`_ocr_subprocess_client` as a **standalone script** with the
OCR venv's python::

    /opt/ocr-venv/bin/python3 .../ocr/_ocr_subprocess_worker.py --model <name> --providers <csv>

Running it by file path (not ``python -m matrice_analytics...``) is deliberate:
importing it as a package submodule would execute
``matrice_analytics/post_processing/__init__.py``, which eagerly imports the
entire 200+ use-case catalog + ``face_reg`` -- none of which is installed in
the slim OCR venv. As a script, only this file's directory is on ``sys.path``,
so the worker depends solely on stdlib, numpy, ``onnxruntime`` and the upstream
``fast_plate_ocr`` package (all present in the venv), plus its sibling
``_ocr_ipc`` module.

Protocol: see :mod:`_ocr_ipc`. ``stdout`` is reserved for the binary protocol;
all logs and tracebacks go to ``stderr`` (writing logs to stdout would corrupt
the frame stream and deadlock the parent's parser).

Lifecycle:

1. Build :class:`fast_plate_ocr.LicensePlateRecognizer` once (model is read
   from the hub cache; pre-baked into the image so no network at startup).
2. Run a self-test inference on a dummy frame -- readiness is declared only if
   it succeeds ("validation after running the subprocess").
3. Emit a ``ready`` control frame with a health report, then serve ``run``
   requests until stdin closes or SIGTERM arrives.
"""

from __future__ import annotations

import argparse
import os
import sys
import traceback

# Ensure the sibling _ocr_ipc module is importable when run by file path.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

import _ocr_ipc  # noqa: E402  (sibling module, resolved via sys.path above)


def _log(msg: str) -> None:
    """Write a diagnostic line to stderr (stdout is protocol-only)."""
    sys.stderr.write(f"[ocr-worker] {msg}\n")
    sys.stderr.flush()


def _stdin_read_exact(n: int) -> bytes:
    return _ocr_ipc.read_exact_from_stream(sys.stdin.buffer, n)


def _emit(frame_bytes: bytes) -> None:
    _ocr_ipc.write_frame(sys.stdout.buffer, frame_bytes)


def _build_recognizer(model_name: str, providers):
    """Instantiate the upstream LicensePlateRecognizer with explicit providers."""
    from fast_plate_ocr import LicensePlateRecognizer

    if providers:
        return LicensePlateRecognizer(model_name, providers=providers)
    return LicensePlateRecognizer(model_name, device="auto")


def _self_test(recognizer) -> None:
    """Run one dummy inference; raises if the OCR pipeline is not functional."""
    import numpy as np

    cfg = recognizer.config
    dummy = np.zeros((1, cfg.img_height, cfg.img_width, cfg.num_channels), dtype=np.uint8)
    result = recognizer.run(dummy, return_confidence=True)
    # Accept both upstream shapes: (texts, confs) tuple (<=1.0.x) and
    # list[PlatePrediction] (>=1.1.0). normalize_run_result handles both.
    texts, _confs = _ocr_ipc.normalize_run_result(result)
    if not isinstance(texts, list):
        raise RuntimeError(f"self-test returned unexpected shape: {type(result)}")


def _health_report(recognizer, model_name: str) -> dict:
    import numpy as np

    try:
        import onnxruntime as ort

        available = list(ort.get_available_providers())
    except Exception:  # pragma: no cover - defensive
        available = []
    return {
        "type": _ocr_ipc.CTRL_READY,
        "numpy_version": np.__version__,
        "available_providers": available,
        "bound_providers": list(getattr(recognizer, "providers", []) or []),
        "model_name": model_name,
        "model_loaded": True,
        "self_test_ok": True,
        "pid": os.getpid(),
    }


def _serve(recognizer) -> int:
    """Request loop. Returns process exit code."""
    while True:
        try:
            frame = _ocr_ipc.read_frame(_stdin_read_exact)
        except EOFError:
            _log("stdin closed; shutting down")
            return 0

        header = frame.header
        request_id = int(header.get("request_id", -1))
        op = header.get("op", "run")

        if op == "ping":
            _emit(_ocr_ipc.pack_control({"type": _ocr_ipc.CTRL_PONG}))
            continue

        # op == "run" / "run_batch": a single bad crop must not kill the worker.
        try:
            return_confidence = bool(header.get("return_confidence", True))
            if op == "run_batch":
                # One call for N crops. Each crop is still handed over as its own
                # array, so the recognizer's own preprocessing runs unchanged.
                source = _ocr_ipc.decode_request_arrays(frame)
            else:
                source = _ocr_ipc.decode_request_array(frame)
            result = recognizer.run(source, return_confidence=return_confidence)
            # Version-tolerant: handles the <=1.0.x (texts, confs) tuple and the
            # >=1.1.0 list[PlatePrediction] shapes identically.
            texts, confs = _ocr_ipc.normalize_run_result(result)
            if op == "run_batch":
                expected = len(header.get("shapes", []))
                if len(texts) != expected:
                    # A recognizer that ignores the list would return one text for N
                    # crops; associating it with all of them would put the wrong plate
                    # on a record. Fail the request so the parent falls back per crop.
                    raise ValueError(f"run_batch returned {len(texts)} texts for {expected} crops")
            _emit(_ocr_ipc.pack_response_ok(request_id, list(texts), confs if return_confidence else None))
        except Exception as exc:  # noqa: BLE001 - report, keep serving
            _log(f"{op} request {request_id} failed: {exc}\n{traceback.format_exc()}")
            _emit(_ocr_ipc.pack_response_error(request_id, str(exc)))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Matrice OCR subprocess worker")
    parser.add_argument("--model", default="cct-s-v1-global-model")
    parser.add_argument(
        "--providers",
        default="",
        help="Comma-separated ORT providers in precedence order (empty -> auto).",
    )
    args = parser.parse_args(argv)
    providers = [p for p in (args.providers or "").split(",") if p]

    # Build + self-test under a guard: any failure here means the GPU OCR path
    # is unavailable, so we tell the parent (which falls back to in-process CPU).
    try:
        recognizer = _build_recognizer(args.model, providers)
        _self_test(recognizer)
    except Exception as exc:  # noqa: BLE001
        _log(f"startup failed: {exc}\n{traceback.format_exc()}")
        try:
            _emit(_ocr_ipc.pack_control({"type": _ocr_ipc.CTRL_ERROR, "error": str(exc)}))
        except Exception:  # pragma: no cover - stdout may be gone
            pass
        return 1

    _emit(_ocr_ipc.pack_control(_health_report(recognizer, args.model)))
    _log(f"ready (model={args.model}, providers={getattr(recognizer, 'providers', None)})")
    return _serve(recognizer)


if __name__ == "__main__":
    # SIGTERM/SIGINT: default behavior raises KeyboardInterrupt/terminates; the
    # blocking stdin read returns EOF when the parent closes the pipe, so the
    # loop exits cleanly. Install a handler only to guarantee a clean exit code.
    import signal

    def _graceful(_signum, _frame):  # pragma: no cover - signal path
        sys.exit(0)

    try:
        signal.signal(signal.SIGTERM, _graceful)
        signal.signal(signal.SIGINT, _graceful)
    except Exception:  # pragma: no cover - non-main-thread / unsupported
        pass

    sys.exit(main())
