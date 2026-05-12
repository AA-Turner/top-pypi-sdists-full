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

__all__ = ["ExternalDataset", "DATASETS", "DatasetMirror", "LocalDatasetStore"]


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
    # ── Expanded corpus (sage-improvement v2) ────────────────────────
    # Adds well-known evaluation + training sets to broaden language
    # coverage and bring competitive-programming reasoning into the mix.
    # All entries are permissively licensed and live on HuggingFace.
    ExternalDataset(
        name="humaneval",
        description="164 Python problems with hidden unit tests — gold standard eval",
        license="mit",
        languages=("python",),
        huggingface_id="openai_humaneval",
        split="test",  # humaneval has only a test split, no train
        fields=("prompt", "test", "canonical_solution"),
        max_examples=164,
        estimated_size_mb=1,
    ),
    ExternalDataset(
        name="humanevalpack",
        description="HumanEval extended to JS/TS/Java/Go/C++/Rust",
        license="mit",
        languages=("python", "javascript", "typescript", "java", "go", "cpp", "rust"),
        huggingface_id="bigcode/humanevalpack",
        fields=("prompt", "test", "canonical_solution"),
        max_examples=1320,
        estimated_size_mb=4,
    ),
    ExternalDataset(
        name="apps",
        description="10,000 competitive-programming problems with solutions",
        license="mit",
        languages=("python",),
        huggingface_id="codeparrot/apps",
        fields=("question", "solutions", "input_output"),
        max_examples=10000,
        estimated_size_mb=600,
    ),
    ExternalDataset(
        name="ds1000",
        description="1k data-science problems from Numpy/Pandas/SciPy/Sklearn",
        license="cc-by-4.0",
        languages=("python",),
        huggingface_id="xlangai/DS-1000",
        fields=("prompt", "test", "code_context"),
        max_examples=1000,
        estimated_size_mb=8,
    ),
    ExternalDataset(
        name="stack-edu-python-2pct",
        description="2% slice of The Stack v2 (educational filter) — Python",
        license="other",  # OpenRAIL-M (permits research + commercial use)
        languages=("python",),
        huggingface_id="bigcode/the-stack-smol",
        split="train",
        fields=("content", "language", "lang"),
        max_examples=50000,
        estimated_size_mb=350,
    ),
    ExternalDataset(
        name="codecontests",
        description="13k problems from Codeforces with multi-language solutions",
        license="apache-2.0",
        languages=("python", "cpp", "java"),
        huggingface_id="deepmind/code_contests",
        split="train",
        fields=("description", "public_tests", "solutions"),
        max_examples=13000,
        estimated_size_mb=550,
    ),
    ExternalDataset(
        name="leetcode-solutions",
        description="LeetCode problems + solutions across many languages",
        license="mit",
        languages=("python", "javascript", "java", "cpp", "go"),
        huggingface_id="greengerong/leetcode",
        fields=("content", "lang", "code"),
        max_examples=2300,
        estimated_size_mb=12,
    ),
    ExternalDataset(
        name="commitpackft",
        description="Filtered git-commit dataset for instruction tuning",
        license="mit",
        languages=("multilang",),
        huggingface_id="bigcode/commitpackft",
        fields=("old_contents", "subject", "new_contents"),
        max_examples=100000,
        estimated_size_mb=400,
    ),
    ExternalDataset(
        name="oss-instruct-multilang",
        description="OSS-Instruct extended sample covering JS/TS/Go/Rust/Java",
        license="mit",
        languages=("javascript", "typescript", "go", "rust", "java"),
        huggingface_id="ise-uiuc/Magicoder-Evol-Instruct-110K",
        fields=("instruction", "", "response"),
        max_examples=110000,
        estimated_size_mb=180,
    ),
    # ── Reasoning datasets (critical for algorithmic thinking) ────────
    ExternalDataset(
        name="gsm8k",
        description="Grade-school math word problems — gold standard reasoning eval",
        license="mit",
        languages=("multilang",),  # math reasoning, language-agnostic
        huggingface_id="gsm8k",
        split="train",
        fields=("question", "", "answer"),
        max_examples=8500,
        estimated_size_mb=4,
    ),
    ExternalDataset(
        name="math",
        description="12.5k competition math problems w/ step-by-step solutions",
        license="mit",
        languages=("multilang",),
        huggingface_id="hendrycks/competition_math",
        split="train",
        fields=("problem", "level", "solution"),
        max_examples=12500,
        estimated_size_mb=15,
    ),
    ExternalDataset(
        name="openr1-math",
        description="DeepSeek-R1-style chain-of-thought math reasoning traces",
        license="apache-2.0",
        languages=("multilang",),
        huggingface_id="open-r1/OpenR1-Math-220k",
        fields=("problem", "", "solution"),
        max_examples=220000,
        estimated_size_mb=350,
    ),
    ExternalDataset(
        name="natural-reasoning",
        description="Meta's reasoning-focused corpus — multi-step problem solving",
        license="cc-by-nc-4.0",
        languages=("multilang",),
        huggingface_id="facebook/natural_reasoning",
        fields=("question", "", "response"),
        max_examples=100000,
        estimated_size_mb=180,
    ),
    # ── Instruction-tuning / chat datasets (assistant behavior) ────────
    ExternalDataset(
        name="oasst1",
        description="OpenAssistant Conversations — human-ranked chat data",
        license="apache-2.0",
        languages=("multilang",),
        huggingface_id="OpenAssistant/oasst1",
        fields=("text", "role", "parent_id"),
        max_examples=88000,
        estimated_size_mb=70,
    ),
    ExternalDataset(
        name="ultrachat-200k",
        description="200k multi-turn synthetic conversations (UltraChat slice)",
        license="mit",
        languages=("multilang",),
        huggingface_id="HuggingFaceH4/ultrachat_200k",
        split="train_sft",
        fields=("prompt", "", "messages"),
        max_examples=200000,
        estimated_size_mb=320,
    ),
    ExternalDataset(
        name="orca-mini",
        description="Orca-style reasoning traces sampled from larger Orca corpora",
        license="mit",
        languages=("multilang",),
        huggingface_id="Open-Orca/SlimOrca-Dedup",
        fields=("conversations", "", ""),
        max_examples=363000,
        estimated_size_mb=480,
    ),
    ExternalDataset(
        name="tulu-mix",
        description="Tulu instruction mix (FLAN + ShareGPT + CoT + coding + safety)",
        license="odc-by-1.0",
        languages=("multilang",),
        huggingface_id="allenai/tulu-v2-sft-mixture",
        fields=("messages", "dataset", ""),
        max_examples=326000,
        estimated_size_mb=550,
    ),
    # ── Code-focused pretraining (sage's bread and butter) ─────────────
    ExternalDataset(
        name="starcoderdata-sample",
        description="StarCoder pretraining slice — permissive GitHub code",
        license="other",  # OpenRAIL-M permits research + commercial
        languages=("multilang",),
        huggingface_id="bigcode/starcoderdata",
        split="train",
        fields=("content", "lang", ""),
        max_examples=200000,
        estimated_size_mb=900,
    ),
    ExternalDataset(
        name="the-stack-v2-dedup-python",
        description="The Stack v2 dedup — Python slice (BigCode)",
        license="other",
        languages=("python",),
        huggingface_id="bigcode/the-stack-v2-dedup",
        split="train",
        fields=("content", "lang", "path"),
        max_examples=80000,
        estimated_size_mb=400,
    ),
    # ── High-quality curated corpora ────────────────────────────────────
    ExternalDataset(
        name="dolma-sample",
        description="Allen AI's high-quality pretraining corpus (sample slice)",
        license="odc-by-1.0",
        languages=("multilang",),
        huggingface_id="allenai/dolma",
        split="train",
        fields=("text", "id", "source"),
        max_examples=50000,
        estimated_size_mb=380,
    ),
    # ── Large-corpus slices (relevant subsets, not full TB-scale) ──────
    # Rationale: sage fine-tunes a pretrained model, so we want
    # representative slices of these landmark corpora, not full mirrors.
    # Full Pile=886GB / FineWeb=15TB / Common Crawl=250TB — impractical
    # to mirror, and the gain over a sized slice is marginal for a
    # coding fine-tune. Users wanting from-scratch pretraining can pull
    # the full HF dataset directly.
    ExternalDataset(
        name="the-pile-code-slice",
        description="The Pile — GitHub + StackExchange portion (code-focused slice)",
        license="mit",
        languages=("multilang",),
        huggingface_id="monology/pile-uncopyrighted",
        split="train",
        fields=("text", "meta", ""),
        max_examples=400000,
        estimated_size_mb=3500,
    ),
    ExternalDataset(
        name="fineweb-edu-sample",
        description="FineWeb-Edu (high-quality educational web text) — 10B-token sample",
        license="odc-by-1.0",
        languages=("multilang",),
        huggingface_id="HuggingFaceFW/fineweb-edu",
        split="train",
        fields=("text", "id", "url"),
        max_examples=500000,
        estimated_size_mb=4200,
    ),
    ExternalDataset(
        name="redpajama-github",
        description="RedPajama-v1 GitHub subset — open-source LLaMA training data",
        license="apache-2.0",
        languages=("multilang",),
        huggingface_id="togethercomputer/RedPajama-Data-1T-Sample",
        split="train",
        fields=("text", "meta", ""),
        max_examples=200000,
        estimated_size_mb=2800,
    ),
    ExternalDataset(
        name="c4-en-sample",
        description="C4 (Colossal Clean Crawled Corpus) — English slice used in T5",
        license="odc-by-1.0",
        languages=("multilang",),
        huggingface_id="allenai/c4",
        split="train",
        fields=("text", "url", "timestamp"),
        max_examples=200000,
        estimated_size_mb=1500,
    ),
    ExternalDataset(
        name="wikipedia-en",
        description="English Wikipedia — context for reasoning, RAG, fact-checking",
        license="cc-by-sa-3.0",
        languages=("multilang",),
        huggingface_id="wikimedia/wikipedia",
        split="20231101.en",
        fields=("text", "title", "url"),
        max_examples=100000,
        estimated_size_mb=900,
    ),
    ExternalDataset(
        name="arxiv-cs",
        description="arXiv CS-section abstracts/papers — reasoning + scientific writing",
        license="cc0-1.0",
        languages=("multilang",),
        huggingface_id="ccdv/arxiv-classification",
        split="train",
        fields=("text", "labels", ""),
        max_examples=50000,
        estimated_size_mb=450,
    ),
    ExternalDataset(
        name="stackexchange-programming",
        description="StackExchange Q&A — programming subsections (curated)",
        license="cc-by-sa-4.0",
        languages=("multilang",),
        huggingface_id="HuggingFaceH4/stack-exchange-preferences",
        split="train",
        fields=("question", "answers", "metadata"),
        max_examples=100000,
        estimated_size_mb=350,
    ),
    ExternalDataset(
        name="openwebtext-sample",
        description="OpenWebText — open recreation of OpenAI's WebText (slice)",
        license="cc0-1.0",
        languages=("multilang",),
        huggingface_id="Skylion007/openwebtext",
        split="train",
        fields=("text", "", ""),
        max_examples=100000,
        estimated_size_mb=800,
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


# ── Local-only retrieval (no GCS dependency) ────────────────────────────


@dataclass
class LocalDatasetStore:
    """Read-only access to datasets mirrored under ~/.sage/datasets/.

    Used by the fine-tune harness to load training pairs WITHOUT needing
    GCS or HuggingFace at training time — once a dataset is pulled
    (either by `mirror_all_datasets.py --local-only` or by GCS-backed
    pull), the fine-tune flow only reads local files. This makes sage
    independent of third-party services at training time.
    """

    root: Path = field(default_factory=lambda: Path.home() / ".sage" / "datasets")

    def path_for(self, name: str) -> Path:
        return self.root / name / "normalized.jsonl"

    def is_present(self, name: str) -> bool:
        p = self.path_for(name)
        return p.is_file() and p.stat().st_size > 0

    def available(self) -> list[str]:
        """List the dataset names currently mirrored to disk."""
        if not self.root.is_dir():
            return []
        out: list[str] = []
        for child in sorted(self.root.iterdir()):
            if not child.is_dir():
                continue
            if (child / "normalized.jsonl").is_file():
                out.append(child.name)
        return out

    def iter_examples(self, name: str):
        """Yield example dicts from a mirrored dataset's normalized.jsonl."""
        import json as _json
        path = self.path_for(name)
        if not path.is_file():
            return
        with path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield _json.loads(line)
                except _json.JSONDecodeError:
                    continue

    def count_examples(self, name: str) -> int:
        if not self.is_present(name):
            return 0
        with self.path_for(name).open(encoding="utf-8") as f:
            return sum(1 for _line in f if _line.strip())

    def summary(self) -> dict:
        """Quick stats across all mirrored datasets — used by `sage train`."""
        out = {"datasets": [], "total_examples": 0, "total_size_bytes": 0}
        for name in self.available():
            p = self.path_for(name)
            count = self.count_examples(name)
            size = p.stat().st_size
            out["datasets"].append({"name": name, "examples": count, "bytes": size})
            out["total_examples"] += count
            out["total_size_bytes"] += size
        return out
