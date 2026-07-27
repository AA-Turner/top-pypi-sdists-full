"""CLI extensions for Sage — Wave 1-4 commands.

Kept in a separate module so we don't have to edit main.py's 15k-line body.
main.py registers these via a single `app.add_typer` call.

Commands added:
    sage rag index            — Build/refresh RAG index for cwd
    sage rag query <text>     — Test retrieval for a query
    sage rag status           — Show index stats
    sage search <query>       — DuckDuckGo web search (no API key)
    sage detect               — Show auto-detected project context
    sage auto-pick            — Show what auto_pick_default_model would choose
    sage finetune <model>     — Real LoRA fine-tune (lazy: cache-aware)
    sage corpus build         — Harvest cwd into a training-corpus snapshot
    sage corpus push          — Upload latest local snapshot to GCS
    sage corpus pull          — Download latest snapshot from GCS
"""

from __future__ import annotations

from pathlib import Path

import typer
from typing_extensions import Annotated

extensions_app = typer.Typer(help="Sage Wave 1-4 extensions (RAG, search, finetune)")
rag_app = typer.Typer(help="Local RAG over the codebase")
corpus_app = typer.Typer(help="GCS-shared training corpus")
extensions_app.add_typer(rag_app, name="rag")
extensions_app.add_typer(corpus_app, name="corpus")


# ── RAG ─────────────────────────────────────────────────────────────────

@rag_app.command("index")
def rag_index(
    force: Annotated[bool, typer.Option("--force", help="Re-embed everything")] = False,
) -> None:
    """Build or refresh the RAG index for the current directory."""
    from sage.core.rag import RAGIndex
    cwd = Path.cwd()
    typer.echo(f"Indexing {cwd} (force={force})...")
    try:
        index = RAGIndex(cwd)
    except Exception as exc:
        typer.echo(f"Failed to open index: {exc}", err=True)
        raise typer.Exit(1)
    stats = index.reindex(force=force)
    typer.echo(
        f"Done. files_seen={stats['files_seen']} "
        f"chunks_added={stats['chunks_added']} "
        f"backend={stats['vec_backend']}"
    )


@rag_app.command("query")
def rag_query(
    text: Annotated[str, typer.Argument(help="Query text")],
    k: Annotated[int, typer.Option("--top-k", "-k")] = 6,
) -> None:
    """Retrieve top-K chunks for a query."""
    from sage.core.rag import RAGIndex, format_chunks_for_prompt
    cwd = Path.cwd()
    index = RAGIndex(cwd)
    chunks = index.query(text, top_k=k)
    if not chunks:
        typer.echo("(no results — index may be empty; run `sage rag index` first)")
        return
    typer.echo(format_chunks_for_prompt(chunks))


@rag_app.command("status")
def rag_status() -> None:
    """Show index location and basic stats."""
    from sage.core.rag import RAGIndex
    import sqlite3
    cwd = Path.cwd()
    index = RAGIndex(cwd)
    conn = sqlite3.connect(index.db_path)
    file_count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    typer.echo(f"DB:       {index.db_path}")
    typer.echo(f"Files:    {file_count}")
    typer.echo(f"Chunks:   {chunk_count}")
    typer.echo(f"Backend:  {'sqlite-vec' if index._has_vec else 'cosine-fallback'}")


# ── Web search ──────────────────────────────────────────────────────────

@extensions_app.command("search")
def web_search(
    query: Annotated[str, typer.Argument(help="Search query")],
    limit: Annotated[int, typer.Option("--limit", "-n")] = 5,
) -> None:
    """Search the web via DuckDuckGo. No API key needed."""
    from sage.core.web_search import search_web
    results = search_web(query, limit=limit)
    if not results:
        typer.echo("(no results — DuckDuckGo unreachable or query empty)")
        return
    for r in results:
        typer.echo(r.to_text())
        typer.echo("")


# ── Project detection ──────────────────────────────────────────────────

@extensions_app.command("detect")
def detect() -> None:
    """Show what sage auto-detected about this project."""
    from sage.core.project_detect import detect_project, format_for_prompt
    ctx = detect_project(Path.cwd())
    if ctx.empty:
        typer.echo("(no project markers detected in cwd)")
        return
    typer.echo(format_for_prompt(ctx))


# ── Auto-pick model ────────────────────────────────────────────────────

@extensions_app.command("auto-pick")
def auto_pick() -> None:
    """Show which model Sage would auto-select based on what's installed."""
    from sage.core.auto_model import list_installed_models, pick_best_coder
    candidates = list_installed_models()
    if not candidates:
        typer.echo("No installed models found (Ollama not running, no GGUFs in ~/.sage/models/)")
        return
    typer.echo("Installed models:")
    for c in sorted(candidates, key=lambda x: -x.score):
        marker = "★ " if c.is_coder else "  "
        typer.echo(f"  {marker}{c.qualified_id:50s} {c.size_gb:6.1f} GB  score={c.score:.1f}")
    pick = pick_best_coder(candidates)
    if pick is not None:
        typer.echo(f"\nWould pick: {pick.qualified_id}")


# ── Fine-tuning ────────────────────────────────────────────────────────

@extensions_app.command("finetune")
def finetune_cmd(
    base_model: Annotated[str, typer.Argument(help="Base model (e.g. ollama:qwen3-coder-next)")],
    corpus: Annotated[str, typer.Option("--corpus", "-c", help="Path to JSONL or 'auto' to harvest cwd")] = "auto",
    steps: Annotated[int, typer.Option("--steps")] = 200,
    rank: Annotated[int, typer.Option("--rank")] = 8,
    cache_only: Annotated[bool, typer.Option("--cache-only", help="Don't train; only pull cached adapter")] = False,
    backend: Annotated[str, typer.Option("--backend", help="auto|mlx|unsloth|peft")] = "auto",
) -> None:
    """Fine-tune a model with QLoRA. Honours adapter cache."""
    from sage.config import load_config
    from sage.training.corpus import CorpusManager
    from sage.training.finetune import FinetuneConfig, finetune

    cfg = load_config()
    cwd = Path.cwd()

    if corpus == "auto":
        cm = CorpusManager(bucket=cfg.gcs_corpus_bucket)
        typer.echo("Harvesting corpus from cwd...")
        snapshot = cm.write_snapshot(cwd, cm.harvest_from_filesystem(cwd), upload=False)
        corpus_path = snapshot
        typer.echo(f"Snapshot: {snapshot}")
    else:
        corpus_path = Path(corpus)
        if not corpus_path.is_file():
            typer.echo(f"Corpus not found: {corpus_path}", err=True)
            raise typer.Exit(1)

    fcfg = FinetuneConfig(
        base_model=base_model, corpus_path=corpus_path,
        max_steps=steps, rank=rank, backend=backend,
    )
    typer.echo(f"Fine-tuning {base_model} (steps={steps}, rank={rank}, backend={backend})...")
    result = finetune(fcfg, bucket=cfg.gcs_corpus_bucket, cache_only=cache_only)
    if result.success:
        typer.echo(f"OK ({result.backend}, {result.duration_s:.1f}s)")
        typer.echo(f"Adapter: {result.adapter_dir}")
        if result.meta.get("hit") == "cache":
            typer.echo("(retrieved from adapter cache — no training needed)")
    else:
        typer.echo(f"FAILED ({result.backend}): {result.error}", err=True)
        raise typer.Exit(1)


# ── Corpus management ─────────────────────────────────────────────────

@corpus_app.command("build")
def corpus_build(
    upload: Annotated[bool, typer.Option("--upload/--no-upload")] = False,
    max_files: Annotated[int, typer.Option("--max-files")] = 500,
) -> None:
    """Harvest the cwd into a training-corpus snapshot."""
    from sage.config import load_config
    from sage.training.corpus import CorpusManager
    cfg = load_config()
    cm = CorpusManager(bucket=cfg.gcs_corpus_bucket)
    cwd = Path.cwd()
    typer.echo(f"Harvesting {cwd} (max_files={max_files})...")
    snap = cm.write_snapshot(
        cwd, cm.harvest_from_filesystem(cwd, max_files=max_files), upload=upload,
    )
    typer.echo(f"Snapshot: {snap}")
    if upload:
        typer.echo(f"Uploaded to: {cm.project(cwd).gcs_dir}")


@corpus_app.command("push")
def corpus_push() -> None:
    """Upload latest local snapshot to GCS."""
    from sage.config import load_config
    from sage.training.corpus import CorpusManager
    cfg = load_config()
    cm = CorpusManager(bucket=cfg.gcs_corpus_bucket)
    proj = cm.project(Path.cwd())
    if not proj.latest_local.exists():
        typer.echo("No local snapshot. Run `sage corpus build` first.", err=True)
        raise typer.Exit(1)
    cm.write_snapshot(
        Path.cwd(),
        (line for line in []),  # No new examples; just push existing latest
        upload=True,
    )
    typer.echo(f"Pushed to {proj.gcs_dir}")


@corpus_app.command("pull")
def corpus_pull() -> None:
    """Download latest snapshot from GCS."""
    from sage.config import load_config
    from sage.training.corpus import CorpusManager
    cfg = load_config()
    cm = CorpusManager(bucket=cfg.gcs_corpus_bucket)
    snap = cm.pull_latest(Path.cwd())
    if snap is None:
        typer.echo("No remote snapshot found (or gsutil unavailable).", err=True)
        raise typer.Exit(1)
    typer.echo(f"Downloaded: {snap}")


# ── External datasets ────────────────────────────────────────────────

datasets_app = typer.Typer(help="Mirror public coding datasets to GCS")
extensions_app.add_typer(datasets_app, name="datasets")


@datasets_app.command("list")
def datasets_list() -> None:
    """Show available public datasets."""
    from sage.training.datasets import DATASETS
    typer.echo(f"{'NAME':28s} {'LICENSE':16s} {'SIZE':>6s}  LANGS")
    for ds in DATASETS:
        size = f"{ds.estimated_size_mb}MB"
        langs = ",".join(ds.languages)
        typer.echo(f"{ds.name:28s} {ds.license:16s} {size:>6s}  {langs}")


@datasets_app.command("mirror")
def datasets_mirror(
    name: Annotated[str, typer.Option("--name", help="Specific dataset, or 'all'")] = "all",
    languages: Annotated[str, typer.Option("--languages", help="Comma-separated language filter")] = "",
    skip_existing: Annotated[bool, typer.Option("--skip-existing/--force")] = True,
) -> None:
    """Download datasets from HuggingFace, normalize, and upload to GCS."""
    from sage.config import load_config
    from sage.training.datasets import DATASETS, DatasetMirror
    cfg = load_config()
    mirror = DatasetMirror(bucket=cfg.gcs_corpus_bucket)
    selected = DATASETS if name == "all" else tuple(d for d in DATASETS if d.name == name)
    if not selected:
        typer.echo(f"Unknown dataset: {name}", err=True)
        raise typer.Exit(1)
    lang_filter = [l.strip() for l in languages.split(",") if l.strip()] or None
    typer.echo(f"Mirroring {len(selected)} dataset(s)...")
    report = mirror.mirror_all(selected, skip_existing=skip_existing, languages=lang_filter)
    typer.echo(f"\nMirrored:  {len(report['mirrored'])} — {report['mirrored']}")
    typer.echo(f"Skipped:   {len(report['skipped'])} — {report['skipped']}")
    typer.echo(f"Failed:    {len(report['failed'])} — {report['failed']}")


# ── Routing inspection ──────────────────────────────────────────────

@extensions_app.command("route")
def route_cmd(
    prompt: Annotated[str, typer.Argument(help="Prompt to route")],
    cloud: Annotated[bool, typer.Option("--allow-cloud")] = False,
) -> None:
    """Show which model the router would pick for a given prompt."""
    from sage.core.auto_model import list_installed_models
    from sage.core.route import RoutePolicy, route_request
    avail = [c.qualified_id for c in list_installed_models()]
    pol = RoutePolicy(allow_cloud=cloud, privacy_strict=not cloud)
    decision = route_request(prompt, available_models=avail, policy=pol)
    typer.echo(f"Difficulty: {decision.difficulty.value}")
    typer.echo(f"Model:      {decision.model}")
    typer.echo(f"Reasoning:  {decision.reasoning}")
    if decision.fallbacks:
        typer.echo(f"Fallbacks:  {', '.join(decision.fallbacks)}")


# ── Internet test ──────────────────────────────────────────────────

@extensions_app.command("internet-test")
def internet_test(
    query: Annotated[str, typer.Argument(help="Search query")] = "claude api docs",
) -> None:
    """Smoke-test Sage's internet stack end-to-end."""
    from sage.core.internet import Internet
    inet = Internet()
    typer.echo(f"Search: {query}")
    results = inet.search(query, limit=3)
    for r in results:
        typer.echo(f"  • {r.title} — {r.url}")
    if results:
        typer.echo(f"\nFetching: {results[0].url}")
        page = inet.fetch(results[0].url)
        if page.ok:
            typer.echo(f"OK: {len(page.text)} chars")
        else:
            typer.echo(f"FAIL: {page.error}")


# ── Bootstrap (auto-setup all new phases) ──────────────────────────

@extensions_app.command("bootstrap")
def bootstrap_cmd(
    pull_models: Annotated[bool, typer.Option("--pull-models/--no-pull-models")] = True,
    set_default: Annotated[bool, typer.Option("--set-default/--no-set-default")] = True,
    prewarm: Annotated[bool, typer.Option("--prewarm/--no-prewarm")] = True,
    build_llama_cpp: Annotated[bool, typer.Option("--build-llama-cpp/--no-build-llama-cpp")] = True,
    install_deps: Annotated[bool, typer.Option("--install-deps/--no-install-deps")] = True,
    build_rag: Annotated[bool, typer.Option("--build-rag/--no-build-rag")] = True,
    mirror_datasets: Annotated[bool, typer.Option("--mirror-datasets/--no-mirror-datasets")] = True,
    finetune: Annotated[bool, typer.Option("--finetune/--no-finetune", help="Run LoRA fine-tune (heavy)")] = False,
    finetune_background: Annotated[bool, typer.Option("--background/--foreground")] = True,
    full_datasets: Annotated[bool, typer.Option("--full-datasets", help="Mirror ALL public datasets, not just the small ones")] = False,
    quiet: Annotated[bool, typer.Option("--quiet", "-q")] = False,
) -> None:
    """Auto-bootstrap every Sage feature: pull models, set default, build
    llama.cpp, prewarm, install optional deps, build RAG index, mirror
    datasets, optionally fine-tune.

    Idempotent — safe to re-run. Each phase has a --no-X opt-out.
    """
    from sage.core.bootstrap import BootstrapOptions, run_bootstrap
    from sage.training.datasets import DATASETS

    opts = BootstrapOptions(
        pull_models=pull_models, set_default=set_default, prewarm=prewarm,
        build_llama_cpp=build_llama_cpp, install_deps=install_deps,
        build_rag=build_rag, mirror_datasets=mirror_datasets,
        finetune=finetune, finetune_background=finetune_background,
        cwd=Path.cwd(), quiet=quiet,
    )
    if full_datasets:
        opts.mirror_dataset_names = tuple(d.name for d in DATASETS)
    result = run_bootstrap(opts)
    typer.echo(result.summary())
    if not result.all_ok:
        raise typer.Exit(1)


def register(parent_app) -> None:
    """Wire extensions_app into the parent typer app.

    Call from main.py once with the top-level `app`. Idempotent.
    """
    parent_app.add_typer(extensions_app, name="ext")
    # Also register top-level shortcuts for the most common commands
    parent_app.add_typer(rag_app, name="rag")
    parent_app.add_typer(corpus_app, name="corpus")
