"""LoRA prep — extract training data from a codebase and emit a recipe.

This module does the *prep* half of LoRA fine-tuning: walking the user's
project, extracting function/class-level chunks, formatting them as
instruction→completion pairs, and writing a paste-and-run recipe for
actual training via axolotl or HuggingFace transformers+peft.

It does NOT run training itself — that needs PyTorch + peft + a real
GPU, and the right infrastructure for the user's setup. The recipe
file shows exactly how to run it on RunPod, Vast, the user's own GPU,
or a Modal instance.

Output layout:
  ~/.pw-agent/training/<project_hash>/
    train.jsonl           training pairs in {"instruction":..., "input":..., "output":...} format
    eval.jsonl            10% holdout
    config.yml            axolotl-compatible training config
    recipe.md             step-by-step instructions to actually train
    Modelfile             ready-to-use Ollama Modelfile pointing at the base + LoRA adapter
    meta.json             stats about the dataset

The default base model is qwen2.5-coder:7b — small enough to LoRA on
a single 24GB GPU but capable enough to learn project style.
"""

import hashlib
import json
import os
import re
import time
from typing import Optional


DEFAULT_TRAINING_DIR = os.path.expanduser("~/.pw-agent/training")
DEFAULT_BASE_MODEL = "qwen2.5-coder:7b"
HF_BASE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"

# Files we extract training data from
EXTRACTABLE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".go", ".rs", ".java", ".kt", ".swift",
    ".rb", ".php", ".cs", ".scala",
}

IGNORED_DIRS = {
    "node_modules", ".git", ".venv", "venv", "env", "__pycache__",
    "dist", "build", "out", "target", ".next", ".cache",
    ".pytest_cache", "vendor", "bower_components",
    ".planning", ".worktrees", ".auto-claude",
}

MAX_FILE_BYTES = 100_000  # 100KB cap per file
MIN_CHUNK_LINES = 5
MAX_CHUNK_LINES = 80


# Language-specific function/class regex (rough but good enough for prep)
FUNCTION_PATTERNS = {
    ".py":  re.compile(r'^(?:async\s+)?(?:def|class)\s+(\w+)', re.MULTILINE),
    ".js":  re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)|^(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(', re.MULTILINE),
    ".jsx": re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)|^(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(', re.MULTILINE),
    ".ts":  re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)|^(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(|^(?:export\s+)?(?:abstract\s+)?(?:class|interface)\s+(\w+)', re.MULTILINE),
    ".tsx": re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+(\w+)|^(?:export\s+)?(?:const|let)\s+(\w+)\s*=\s*(?:async\s+)?\(|^(?:export\s+)?(?:abstract\s+)?(?:class|interface)\s+(\w+)', re.MULTILINE),
    ".go":  re.compile(r'^func\s+(?:\([^)]+\)\s+)?(\w+)', re.MULTILINE),
    ".rs":  re.compile(r'^(?:pub\s+)?(?:async\s+)?fn\s+(\w+)|^(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)', re.MULTILINE),
    ".java": re.compile(r'(?:public|private|protected)?\s*(?:static\s+)?(?:[\w<>\[\]]+)\s+(\w+)\s*\([^)]*\)\s*\{', re.MULTILINE),
}


def project_training_path(project_dir: str) -> str:
    """Return the storage dir for a project's training assets."""
    project_dir = os.path.abspath(project_dir)
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:12]
    return os.path.join(DEFAULT_TRAINING_DIR, project_hash)


def extract_function_chunks(project_dir: str, max_files: int = 2000) -> list[dict]:
    """Walk the project, extract function/class chunks. Returns list of dicts:
       {"path": "...", "name": "foo", "signature": "def foo(...)",
        "body": "def foo(...): ...", "lang": ".py"}
    """
    project_dir = os.path.abspath(project_dir)
    chunks = []
    files_scanned = 0

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS and not d.startswith(".")]

        for fname in files:
            if files_scanned >= max_files:
                return chunks
            ext = os.path.splitext(fname)[1].lower()
            if ext not in EXTRACTABLE_EXTENSIONS:
                continue
            path = os.path.join(root, fname)
            try:
                if os.path.getsize(path) > MAX_FILE_BYTES:
                    continue
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception:
                continue

            files_scanned += 1
            rel_path = os.path.relpath(path, project_dir)

            # Extract chunks via the language-specific pattern
            pattern = FUNCTION_PATTERNS.get(ext)
            if not pattern:
                continue

            lines = content.split("\n")
            matches = list(pattern.finditer(content))
            if not matches:
                continue

            # For each function match, find its body by looking at indentation
            # (Python) or brace counting (JS/TS/Go/Rust/Java)
            for i, m in enumerate(matches):
                # Get the line number of this match
                start_char = m.start()
                start_line = content[:start_char].count("\n")
                # Walk to end of this function
                end_line = _find_function_end(lines, start_line, ext)
                chunk_lines = lines[start_line:end_line]
                if len(chunk_lines) < MIN_CHUNK_LINES or len(chunk_lines) > MAX_CHUNK_LINES:
                    continue
                body = "\n".join(chunk_lines).strip()
                if not body:
                    continue
                # Extract the name from the regex groups (first non-None)
                name_groups = [g for g in m.groups() if g]
                name = name_groups[0] if name_groups else "anonymous"
                # First line is the signature
                signature = chunk_lines[0].strip()

                chunks.append({
                    "path": rel_path,
                    "name": name,
                    "signature": signature,
                    "body": body,
                    "lang": ext,
                })

    return chunks


def _find_function_end(lines: list[str], start: int, ext: str) -> int:
    """Find the line after the function ends. Heuristic: indent-based for Python,
    brace-counting for everything else."""
    if start >= len(lines):
        return start

    if ext == ".py":
        # Python: scan for the next non-blank line with indent <= the def's indent
        first = lines[start]
        first_indent = len(first) - len(first.lstrip())
        for i in range(start + 1, len(lines)):
            line = lines[i]
            stripped = line.strip()
            if not stripped:
                continue
            indent = len(line) - len(line.lstrip())
            if indent <= first_indent:
                return i
        return len(lines)

    # Brace-counting for C-family
    depth = 0
    started = False
    for i in range(start, len(lines)):
        line = lines[i]
        for ch in line:
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
                if started and depth == 0:
                    return i + 1
        if i - start > MAX_CHUNK_LINES:
            return i + 1
    return len(lines)


def chunks_to_training_pairs(chunks: list[dict]) -> list[dict]:
    """Convert raw function chunks into instruction-tuning format.
    Output schema (alpaca-style):
      {"instruction": "Write a Python function...", "input": "", "output": "<code>"}
    """
    pairs = []
    for ch in chunks:
        lang = _lang_name(ch["lang"])
        path = ch["path"]
        name = ch["name"]
        sig = ch["signature"]

        # Synthesize a natural-language instruction from the signature + path
        instruction = (
            f"Write a {lang} {_kind_from_signature(sig)} `{name}` for the file "
            f"`{path}` that matches the project's existing style and conventions."
        )

        pairs.append({
            "instruction": instruction,
            "input": "",
            "output": ch["body"],
            "_meta": {
                "path": path,
                "name": name,
                "lang": lang,
            },
        })
    return pairs


def _lang_name(ext: str) -> str:
    return {
        ".py": "Python", ".js": "JavaScript", ".jsx": "JSX",
        ".ts": "TypeScript", ".tsx": "TSX", ".go": "Go",
        ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
        ".swift": "Swift", ".rb": "Ruby", ".php": "PHP",
        ".cs": "C#", ".scala": "Scala",
    }.get(ext, "code")


def _kind_from_signature(sig: str) -> str:
    sig_lower = sig.lower()
    if sig_lower.startswith(("class ", "abstract class")):
        return "class"
    if "interface " in sig_lower:
        return "interface"
    if "struct " in sig_lower:
        return "struct"
    if "enum " in sig_lower:
        return "enum"
    if "trait " in sig_lower:
        return "trait"
    return "function"


def write_training_assets(project_dir: str, base_model: str = DEFAULT_BASE_MODEL,
                          hf_model: str = HF_BASE_MODEL,
                          eval_split: float = 0.1) -> dict:
    """Run the full prep pipeline. Returns a stats dict + the output dir."""
    out_dir = project_training_path(project_dir)
    os.makedirs(out_dir, exist_ok=True)

    chunks = extract_function_chunks(project_dir)
    pairs = chunks_to_training_pairs(chunks)

    # Shuffle deterministically and split
    import random
    rng = random.Random(42)
    rng.shuffle(pairs)
    split_idx = int(len(pairs) * (1 - eval_split))
    train_pairs = pairs[:split_idx]
    eval_pairs = pairs[split_idx:]

    # Write JSONL files
    train_path = os.path.join(out_dir, "train.jsonl")
    eval_path = os.path.join(out_dir, "eval.jsonl")
    _write_jsonl(train_path, train_pairs)
    _write_jsonl(eval_path, eval_pairs)

    # Write axolotl config
    config_path = os.path.join(out_dir, "config.yml")
    with open(config_path, "w") as f:
        f.write(_axolotl_config(hf_model, train_path, eval_path))

    # Write Modelfile
    modelfile_path = os.path.join(out_dir, "Modelfile")
    with open(modelfile_path, "w") as f:
        f.write(_ollama_modelfile(base_model, project_dir))

    # Write recipe markdown
    recipe_path = os.path.join(out_dir, "recipe.md")
    with open(recipe_path, "w") as f:
        f.write(_recipe_markdown(out_dir, hf_model, base_model, len(train_pairs), len(eval_pairs)))

    # Write meta
    meta = {
        "project_dir": os.path.abspath(project_dir),
        "created_at": time.time(),
        "base_model": base_model,
        "hf_model": hf_model,
        "chunks_extracted": len(chunks),
        "train_pairs": len(train_pairs),
        "eval_pairs": len(eval_pairs),
    }
    with open(os.path.join(out_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    return {
        "out_dir": out_dir,
        "chunks": len(chunks),
        "train": len(train_pairs),
        "eval": len(eval_pairs),
        "train_path": train_path,
        "eval_path": eval_path,
        "config_path": config_path,
        "recipe_path": recipe_path,
        "modelfile_path": modelfile_path,
    }


def _write_jsonl(path: str, items: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            # Strip _meta from output (only used internally)
            clean = {k: v for k, v in item.items() if not k.startswith("_")}
            f.write(json.dumps(clean) + "\n")


def _axolotl_config(hf_model: str, train_path: str, eval_path: str) -> str:
    """Generate an axolotl-compatible LoRA config."""
    return f"""# pw-agent generated axolotl config
# Run with: axolotl train config.yml
base_model: {hf_model}
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_4bit: true
strict: false

datasets:
  - path: {train_path}
    type: alpaca
    field_instruction: instruction
    field_input: input
    field_output: output

test_datasets:
  - path: {eval_path}
    type: alpaca
    field_instruction: instruction
    field_input: input
    field_output: output

dataset_prepared_path: ./prepared
val_set_size: 0.0
output_dir: ./pw-lora-out

adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
  - gate_proj
  - down_proj
  - up_proj

sequence_len: 2048
sample_packing: true
pad_to_sequence_len: true

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 0.0002

bf16: auto
tf32: false
gradient_checkpointing: true
flash_attention: true

warmup_steps: 10
evals_per_epoch: 1
saves_per_epoch: 1
logging_steps: 5

weight_decay: 0.01
"""


def _ollama_modelfile(base_model: str, project_dir: str) -> str:
    """Generate a Modelfile that loads the base model + the trained LoRA.

    The user fills in the path to the GGUF-converted adapter after training.
    """
    project_name = os.path.basename(os.path.abspath(project_dir))
    return f"""# pw-agent generated Modelfile for {project_name}
# After training:
#   1. Convert the LoRA adapter to GGUF: python llama.cpp/convert_lora_to_gguf.py ./pw-lora-out
#   2. Update the ADAPTER path below
#   3. Build: ollama create {project_name}-coder -f Modelfile
#   4. Use in pw-agent: /use 1 then pick this model

FROM {base_model}

# ADAPTER ./pw-lora-out/lora.gguf

PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER repeat_penalty 1.1

SYSTEM \"\"\"You are a coding assistant fine-tuned on the {project_name} codebase.
Match the project's existing style, naming conventions, and patterns when writing new code.\"\"\"
"""


def _recipe_markdown(out_dir: str, hf_model: str, base_model: str,
                     n_train: int, n_eval: int) -> str:
    return f"""# LoRA Fine-tuning Recipe — pw-agent

Generated by pw-agent. This trains a small LoRA adapter on top of `{hf_model}`
using your own codebase as training data, so the model learns YOUR patterns,
naming, and style.

## Stats
- Training pairs: **{n_train}**
- Eval pairs: **{n_eval}**
- Base model: **{hf_model}**
- Output: `~/.pw-agent/training/<hash>/pw-lora-out/`

## What you need
- A single NVIDIA GPU with **24GB+ VRAM** (for QLoRA at sequence_len=2048)
- Or **48GB+** for full LoRA without quantization
- Python 3.10+
- ~1-3 hours of compute time

## Step 1 — Install axolotl

```bash
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl
pip install -e .
pip install flash-attn --no-build-isolation
```

Or use Docker:
```bash
docker run --gpus all -v {out_dir}:/workspace winglian/axolotl:main-latest \\
    accelerate launch -m axolotl.cli.train /workspace/config.yml
```

## Step 2 — Train

```bash
cd {out_dir}
accelerate launch -m axolotl.cli.train config.yml
```

The output adapter weights will land in `./pw-lora-out/`. Watch the eval loss
in the logs — if it stops decreasing after 1 epoch, you may want to reduce
`num_epochs` to avoid overfitting on a small codebase.

## Step 3 — Convert to GGUF for Ollama

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
pip install -r requirements.txt
python convert_lora_to_gguf.py {out_dir}/pw-lora-out --outfile {out_dir}/lora.gguf
```

## Step 4 — Build the Ollama model

```bash
# Edit Modelfile and uncomment the ADAPTER line
cd {out_dir}
ollama create my-project-coder -f Modelfile
```

## Step 5 — Use it in pw-agent

```bash
pw-agent
> /models           # confirm my-project-coder shows up
> /use 1            # pick the slot running it
```

## Alternative: train on Vast.ai or RunPod

Both let you rent a 24GB GPU by the hour for ~$0.40/hr. Upload `train.jsonl`,
`eval.jsonl`, and `config.yml` to the rented instance, install axolotl, run.

## Re-running the prep
You can re-run the prep step anytime to refresh training data after the
codebase has changed:

```
pw-agent
> /train prep
```

## Troubleshooting

- **OOM during training**: drop `micro_batch_size` to 1 and `sequence_len` to 1024
- **Loss plateaus too early**: increase `learning_rate` to 5e-4 or `num_epochs` to 5
- **Model overfits and forgets general knowledge**: lower `lora_r` to 8, drop epochs to 2
"""


def status(project_dir: str) -> dict:
    """Check if training assets exist for this project. Returns meta dict or empty."""
    out_dir = project_training_path(project_dir)
    meta_path = os.path.join(out_dir, "meta.json")
    if not os.path.exists(meta_path):
        return {}
    try:
        with open(meta_path, "r") as f:
            meta = json.load(f)
        meta["out_dir"] = out_dir
        return meta
    except Exception:
        return {}
