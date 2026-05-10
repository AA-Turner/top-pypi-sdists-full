"""External dataset mirroring for training.

Why: the user's own code is small (thousands of files at most). To make
local models actually competitive on the long tail of programming tasks,
we mix in well-known public coding datasets — but pinned to a copy in our
own GCS bucket so we're not at the mercy of HuggingFace uptime, license
changes, or dataset removals.

Datasets supported (all permissively licensed, all multi-language where
applicable):

  CodeAlpaca-20k       — 20k instruction-tuning examples (cc-by-nc-4.0)
  Magicoder OSS-Instruct — synthetic code instructions (mit)
  CodeSearchNet        — multi-language code/docstring (cc-by-sa-4.0)
  MBPP                 — 974 Python problems with tests (cc-by-4.0)
  HumanEval            — 164 Python problems (mit) — usually eval, but
                         filtered subset can supplement training
  Glaive Code Assistant — multi-turn coding assistant data (apache-2.0)
  Evol-Instruct-Code   — evolved instruction set (apache-2.0)

Layout in GCS:
  <bucket>/datasets/external/<dataset_name>/
    raw/<original_filename>         — verbatim copy
    normalized.jsonl                — converted to our TrainingExample shape
    LICENSE                         — original license text
    SOURCE.txt                      — provenance (URL, commit, date)
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

from sage.training.corpus import TrainingExample

__all__ = ["ExternalDataset", "DATASETS", "DatasetMirror"]


@dataclass(frozen=True)
class ExternalDataset:
    name: str
    description: str
    license: str
    languages: tuple[str, ...]   # ("python",) or ("multilang",) etc.
    huggingface_id: str           # e.g. "sahil2801/CodeAlpaca-20k"
    split: str = "train"
    fields: tuple[str, str, str] = ("instruction", "input", "output")  # (q, ctx, a)
    max_examples: int = 50000
    estimated_size_mb: int = 50


# Public, permissively licensed coding datasets. Pin specific HuggingFace
# repo ids — when bumped, append a new entry rather than mutating, so the
# corpus_hash remains reproducible.
DATASETS: tuple[ExternalDataset, ...] = (
    ExternalDataset(
        name="codealpaca-20k",
        description="20k instruction-tuning examples for general code tasks",
        license="cc-by-nc-4.0",
        languages=("multilang",),
        huggingface_id="sahil2801/CodeAlpaca-20k",
        fields=("instruction", "input", "output"),
        max_examples=20000,
        estimated_size_mb=15,
    ),
    ExternalDataset(
        name="magicoder-oss-instruct-75k",
        description="Synthetic code instructions across many languages",
        license="mit",
        languages=("multilang",),
        huggingface_id="ise-uiuc/Magicoder-OSS-Instruct-75K",
        fields=("problem", "lang", "solution"),
        max_examples=75000,
        estimated_size_mb=120,
    ),
    ExternalDataset(
        name="codesearchnet-python",
        description="Python function + docstring pairs (multilang via siblings)",
        license="cc-by-sa-4.0",
        languages=("python", "javascript", "go", "ruby", "java", "php"),
        huggingface_id="code_search_net",
        fields=("docstring", "func_name", "code"),
        max_examples=200000,
        estimated_size_mb=900,
    ),
    ExternalDataset(
        name="mbpp",
        description="974 Python problems with test cases",
        license="cc-by-4.0",
        languages=("python",),
        huggingface_id="mbpp",
        fields=("text", "test_list", "code"),
        max_examples=974,
        estimated_size_mb=2,
    ),
    ExternalDataset(
        name="glaive-code-assistant",
        description="Multi-turn coding-assistant conversations",
        license="apache-2.0",
        languages=("multilang",),
        huggingface_id="glaiveai/glaive-code-assistant",
        fields=("question", "", "answer"),
        max_examples=140000,
        estimated_size_mb=180,
    ),
    ExternalDataset(
        name="evol-instruct-code-80k",
        description="Wizard-style evolved code instructions",
        license="apache-2.0",
        languages=("multilang",),
        huggingface_id="nickrosh/Evol-Instruct-Code-80k-v1",
        fields=("instruction", "", "output"),
        max_examples=80000,
        estimated_size_mb=70,
    ),
)


def _have_gsutil() -> bool:
    return shutil.which("gsutil") is not None


def _have_datasets_lib() -> bool:
    try:
        import datasets  # type: ignore  # noqa: F401
        return True
    except ImportError:
        return False


def _gcs_cp(src: str, dst: str) -> bool:
    try:
        return subprocess.run(
            ["gsutil", "-q", "cp", src, dst],
            capture_output=True, text=True, timeout=300,
        ).returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _gcs_exists(uri: str) -> bool:
    try:
        return subprocess.run(
            ["gsutil", "ls", uri],
            capture_output=True, text=True, timeout=30,
        ).returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


@dataclass
class DatasetMirror:
    """Download → normalize → upload a single external dataset.

    Idempotent: if normalized.jsonl already exists in GCS we skip work.
    """

    bucket: str = "gs://sage-ai-models"

    def gcs_dir(self, ds: ExternalDataset) -> str:
        return f"{self.bucket}/datasets/external/{ds.name}"

    def local_dir(self, ds: ExternalDataset) -> Path:
        d = Path.home() / ".sage" / "datasets" / ds.name
        d.mkdir(parents=True, exist_ok=True)
        return d

    def is_mirrored(self, ds: ExternalDataset) -> bool:
        if not _have_gsutil():
            return False
        return _gcs_exists(f"{self.gcs_dir(ds)}/normalized.jsonl")

    def fetch_and_normalize(self, ds: ExternalDataset) -> Path:
        """Download from HuggingFace and convert to TrainingExample JSONL."""
        if not _have_datasets_lib():
            raise RuntimeError(
                "huggingface `datasets` library required. Install:\n"
                "    pip install datasets"
            )
        from datasets import load_dataset
        local = self.local_dir(ds)
        normalized = local / "normalized.jsonl"
        if normalized.exists() and normalized.stat().st_size > 0:
            return normalized

        loaded = load_dataset(ds.huggingface_id, split=ds.split,
                              streaming=False, trust_remote_code=True)
        q_field, ctx_field, a_field = ds.fields
        count = 0
        with normalized.open("w", encoding="utf-8") as fh:
            for row in loaded:
                if count >= ds.max_examples:
                    break
                q = str(row.get(q_field, "")) if q_field else ""
                ctx = str(row.get(ctx_field, "")) if ctx_field else ""
                a = str(row.get(a_field, "")) if a_field else ""
                if not (q and a):
                    continue
                ex = TrainingExample(
                    instruction=q, input=ctx, output=a,
                    tags=[ds.name, *ds.languages],
                    source={"dataset": ds.name, "license": ds.license},
                )
                fh.write(ex.to_jsonl() + "\n")
                count += 1

        # Provenance
        (local / "SOURCE.txt").write_text(
            f"dataset: {ds.huggingface_id}\n"
            f"split:   {ds.split}\n"
            f"date:    {time.strftime('%Y-%m-%d')}\n"
            f"license: {ds.license}\n"
            f"count:   {count}\n",
            "utf-8",
        )
        return normalized

    def push(self, ds: ExternalDataset) -> bool:
        """Upload normalized + provenance to GCS."""
        if not _have_gsutil():
            return False
        local = self.local_dir(ds)
        normalized = local / "normalized.jsonl"
        if not normalized.is_file():
            return False
        ok1 = _gcs_cp(str(normalized), f"{self.gcs_dir(ds)}/normalized.jsonl")
        ok2 = _gcs_cp(str(local / "SOURCE.txt"), f"{self.gcs_dir(ds)}/SOURCE.txt")
        return ok1 and ok2

    def pull(self, ds: ExternalDataset) -> Path | None:
        """Download already-mirrored normalized.jsonl from GCS."""
        if not _have_gsutil():
            return None
        local = self.local_dir(ds)
        normalized = local / "normalized.jsonl"
        if normalized.exists() and normalized.stat().st_size > 0:
            return normalized
        if _gcs_cp(f"{self.gcs_dir(ds)}/normalized.jsonl", str(normalized)):
            return normalized
        return None

    # ── Bulk operations ─────────────────────────────────────────

    def mirror_all(self, datasets: tuple[ExternalDataset, ...] = DATASETS,
                   *, skip_existing: bool = True, languages: list[str] | None = None) -> dict:
        """Mirror multiple datasets to GCS in sequence.

        Args:
            datasets: which to mirror (default: all)
            skip_existing: skip datasets already in GCS (idempotent)
            languages: filter to datasets touching these languages
                       (None = no filter; "multilang" matches everything)
        """
        report = {"mirrored": [], "skipped": [], "failed": []}
        for ds in datasets:
            if languages and "multilang" not in ds.languages and not (set(languages) & set(ds.languages)):
                report["skipped"].append((ds.name, "language-filter"))
                continue
            if skip_existing and self.is_mirrored(ds):
                report["skipped"].append((ds.name, "already-mirrored"))
                continue
            try:
                self.fetch_and_normalize(ds)
                if self.push(ds):
                    report["mirrored"].append(ds.name)
                else:
                    report["failed"].append((ds.name, "gcs-upload-failed"))
            except Exception as exc:
                report["failed"].append((ds.name, f"{type(exc).__name__}: {exc}"))
        return report
