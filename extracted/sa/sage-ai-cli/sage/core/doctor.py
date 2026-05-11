"""Item #3 — sage doctor: audit every subsystem."""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["Check", "DoctorReport", "run_doctor"]


@dataclass
class Check:
    name: str
    status: str  # "green" | "yellow" | "red"
    detail: str = ""


@dataclass
class DoctorReport:
    checks: list[Check] = field(default_factory=list)

    @property
    def overall_status(self) -> str:
        statuses = {c.status for c in self.checks}
        if "red" in statuses:
            return "red"
        if "yellow" in statuses:
            return "yellow"
        return "green"


def _check_model() -> Check:
    try:
        # Use sys.modules to look up the current attribute so tests can
        # monkeypatch.setattr("sage.core.auto_model.list_installed_models", ...).
        import sys
        am = sys.modules.get("sage.core.auto_model")
        if am is None:
            from sage.core import auto_model as am  # noqa: F401
            am = sys.modules["sage.core.auto_model"]
        models = am.list_installed_models()
        if not models:
            return Check(name="model", status="red",
                         detail="no models installed — run `sage install`")
        coders = [m for m in models if m.is_coder]
        if not coders:
            return Check(name="model", status="yellow",
                         detail=f"{len(models)} models, but no coding-specialist")
        return Check(name="model", status="green",
                     detail=f"{len(coders)} coding models installed")
    except Exception as exc:
        return Check(name="model", status="red", detail=str(exc))


def _check_rag() -> Check:
    rag_dir = Path.home() / ".sage" / "rag"
    if not rag_dir.exists():
        return Check(name="rag", status="yellow", detail="no RAG indexes built yet")
    dbs = list(rag_dir.glob("*.db"))
    if not dbs:
        return Check(name="rag", status="yellow", detail="no project indexes")
    return Check(name="rag", status="green", detail=f"{len(dbs)} project index(es)")


def _check_ollama() -> Check:
    if not shutil.which("ollama"):
        return Check(name="ollama", status="yellow",
                     detail="Ollama not on PATH — install via brew/apt")
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=2.0)
        if r.status_code == 200:
            n = len(r.json().get("models", []))
            return Check(name="ollama", status="green",
                         detail=f"daemon up, {n} models")
        return Check(name="ollama", status="yellow",
                     detail=f"daemon HTTP {r.status_code}")
    except Exception:
        return Check(name="ollama", status="yellow",
                     detail="installed but daemon not responding")


def _check_disk() -> Check:
    try:
        usage = shutil.disk_usage(str(Path.home()))
        gb = usage.free / (1024 ** 3)
        if gb < 5:
            return Check(name="disk", status="red", detail=f"only {gb:.1f} GB free")
        if gb < 30:
            return Check(name="disk", status="yellow", detail=f"{gb:.1f} GB free")
        return Check(name="disk", status="green", detail=f"{gb:.1f} GB free")
    except Exception as exc:
        return Check(name="disk", status="yellow", detail=str(exc))


def _check_config() -> Check:
    cfg_path = Path.home() / ".sage" / "config.json"
    if not cfg_path.exists():
        return Check(name="config", status="yellow",
                     detail="no config — run `sage install`")
    try:
        from sage.config import load_config
        cfg = load_config()
        return Check(name="config", status="green",
                     detail=f"default_model={cfg.default_model}")
    except Exception as exc:
        return Check(name="config", status="red", detail=str(exc))


def run_doctor() -> DoctorReport:
    return DoctorReport(checks=[
        _check_model(),
        _check_rag(),
        _check_ollama(),
        _check_disk(),
        _check_config(),
    ])
