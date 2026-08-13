"""
@anaconda_models — Metaflow step decorator for pulling Anaconda catalog models.

Usage:
    from metaflow_extensions.outerbounds.plugins.anaconda_models import anaconda_models

    class MyFlow(FlowSpec):
        @anaconda_models
        @step
        def start(self):
            model = self.anaconda_models.model("Qwen2.5-0.5B", pull=True)
            print(model.path)
            self.next(self.end)
"""

from metaflow import user_step_decorator
from metaflow.user_decorators.user_step_decorator import StepMutator

from .exceptions import ModelAccessDenied


# ------------------------------------------------------------------
# Card painting — translates AnacondaModel state into card components
# ------------------------------------------------------------------


def _paint_card(card, models):
    """
    Paint all model metadata onto the card.

    Parameters
    ----------
    card : CardComponentManager
        The blank card bound to id='anaconda_models'.
    models : list[AnacondaModel]
        All models resolved/pulled in this step (single files and
        safetensor collections alike).
    """
    try:
        from metaflow.cards import Markdown, Table
    except ImportError:
        return

    if not models:
        card.append(Markdown("# Anaconda Models\n\n*No models loaded.*"))
        card.refresh()
        return

    card.clear()
    card.append(Markdown("# Anaconda Models"))

    for model in models:
        _paint_model(card, model, Markdown, Table)

    card.refresh()


def _paint_model(card, model, Markdown, Table):
    """Paint one model's full metadata onto the card."""
    # Handle denied models
    if isinstance(model, _DeniedModel):
        card.append(Markdown("## %s" % model.name))
        card.append(Markdown("### Access Denied"))
        card.append(
            Table(
                _kv_rows({"Model": model.name, "Reason": model.access_denied_reason}),
                headers=["Property", "Value"],
            )
        )
        return

    ident = model.identity
    prov = model.provenance
    lic = model.license_info
    sq = model.selected_model

    # --- Header ---
    card.append(Markdown("## %s" % ident["name"]))
    desc = ident.get("description") or ""
    if desc:
        card.append(Markdown(desc[:600]))

    # --- Model Details ---
    card.append(Markdown("### Model Details"))
    card.append(
        Table(
            _kv_rows(
                {
                    "Parameters": _format_params(ident.get("num_parameters")),
                    "Type": ident.get("model_type"),
                    "Trained For": ident.get("trained_for"),
                    "Context Window": _format_int(ident.get("context_window_size")),
                    "Chat Template": _yes_no(ident.get("has_chat_template")),
                    "Tool Calling": _yes_no(ident.get("supports_tool_calling")),
                    "Library": ident.get("library_name"),
                    "Base Model": ", ".join(ident.get("base_models") or [])
                    or ident.get("base_model")
                    or "-",
                }
            ),
            headers=["Property", "Value"],
        )
    )

    # --- Provenance ---
    source = prov.get("source") or {}
    langs = prov.get("languages") or []
    tags = prov.get("tags") or []
    tag_names = ", ".join(
        t["name"] if isinstance(t, dict) else str(t) for t in tags[:8]
    )

    card.append(Markdown("### Provenance"))
    card.append(
        Table(
            _kv_rows(
                {
                    "Source": source.get("name", "-"),
                    "Published": (prov.get("first_published") or "-")[:10],
                    "Origin": prov.get("country_of_origin") or "-",
                    "Languages": (
                        ", ".join(langs[:10]) + ("..." if len(langs) > 10 else "")
                        if langs
                        else "-"
                    ),
                    "Paper": prov.get("paper_url") or "-",
                    "Tags": tag_names or "-",
                }
            ),
            headers=["Property", "Value"],
        )
    )

    # --- License ---
    card.append(Markdown("### License"))
    card.append(
        Table(
            _kv_rows(
                {
                    "License": lic.get("license") or "-",
                    "Summary": (lic.get("license_summary") or "-")[:200],
                    "Commercial Use": _yes_no(lic.get("commercial_use")),
                    "Fine-tuning": _yes_no(lic.get("fine_tuning_permitted")),
                    "Attribution": _yes_no(lic.get("attribution_required")),
                    "Open Weights": _yes_no(lic.get("open_weights")),
                }
            ),
            headers=["Property", "Value"],
        )
    )

    # --- Test Scores ---
    if model.test_scores:
        card.append(Markdown("### Evaluation Scores (%s)" % sq.get("quant_method", "")))
        score_rows = []
        for ts in sorted(model.test_scores, key=lambda t: t.get("test_name", "")):
            score_rows.append(
                [
                    ts.get("test_name", "?"),
                    (
                        "%.1f" % ts["test_value"]
                        if ts.get("test_value") is not None
                        else "-"
                    ),
                ]
            )
        card.append(Table(score_rows, headers=["Benchmark", "Score"]))

    # --- Selected File / Collection ---
    if sq.get("is_collection"):
        card.append(Markdown("### Selected Collection"))
        card.append(
            Table(
                _kv_rows(
                    {
                        "Format": sq.get("format"),
                        "Type": sq.get("collection_type"),
                        "Files": sq.get("file_count"),
                        "Total Size": _format_size(sq.get("total_size_bytes")),
                    }
                ),
                headers=["Property", "Value"],
            )
        )
    else:
        card.append(Markdown("### Selected Quantization"))
        card.append(
            Table(
                _kv_rows(
                    {
                        "Method": sq.get("quant_method"),
                        "Format": sq.get("format"),
                        "Engine": sq.get("quant_engine"),
                        "File Size": _format_size(sq.get("size_bytes")),
                        "Max RAM": _format_size(sq.get("max_ram_usage")),
                        "SHA256": (sq.get("sha256") or "")[:24] + "...",
                    }
                ),
                headers=["Property", "Value"],
            )
        )

    # --- Files (only interesting for multi-file collections) ---
    if len(model.files) > 1:
        file_rows = []
        for f in model.files[:20]:
            file_rows.append(
                [
                    f.get("filename", "?"),
                    _format_size(f.get("size_bytes")),
                    f.get("status", "-"),
                ]
            )
        card.append(Markdown("### Files"))
        card.append(Table(file_rows, headers=["Filename", "Size", "Status"]))
        if len(model.files) > 20:
            card.append(Markdown("*… and %d more files*" % (len(model.files) - 20)))

    # --- All Quantizations ---
    if len(model.all_quants) > 1:
        card.append(Markdown("### All Quantizations"))
        q_rows = []
        for q in sorted(model.all_quants, key=lambda x: x.get("size_bytes") or 0):
            selected = " *" if q.get("file_uuid") == sq.get("file_uuid") else ""
            q_rows.append(
                [
                    (q.get("quant_method") or q.get("format") or "?") + selected,
                    _format_size(q.get("size_bytes")),
                    _format_size(q.get("max_ram_usage")),
                    "Yes" if q.get("published") else "No",
                ]
            )
        card.append(Table(q_rows, headers=["Method", "Size", "Max RAM", "Published"]))

    # --- Download Status ---
    card.append(Markdown("### Download"))
    card.append(
        Table(
            _kv_rows(
                {
                    "Status": model.download_status or "not pulled",
                    "Path": model.path,
                }
            ),
            headers=["Property", "Value"],
        )
    )


# --- Formatting helpers ---


def _kv_rows(d):
    return [[k, str(v) if v is not None else "-"] for k, v in d.items()]


def _format_params(n):
    if n is None:
        return "-"
    if n >= 1e9:
        return "%.1fB" % (n / 1e9)
    if n >= 1e6:
        return "%.0fM" % (n / 1e6)
    return str(n)


def _format_size(b):
    if b is None:
        return "-"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(b) < 1024:
            return "%.1f %s" % (b, unit)
        b /= 1024
    return "%.1f PB" % b


def _format_int(n):
    if n is None:
        return "-"
    return "{:,}".format(n)


def _yes_no(v):
    if v is None:
        return "-"
    return "Yes" if v else "No"


# ------------------------------------------------------------------
# _DeniedModel — lightweight stand-in when policy blocks access
# ------------------------------------------------------------------


class _DeniedModel:
    """Minimal model object representing a policy-denied model for card display."""

    def __init__(self, name, reason):
        self.name = name
        self.access_denied_reason = reason
        self.identity = {"name": name}
        self.provenance = {}
        self.license_info = {}
        self.selected_model = {}
        self.all_quants = []
        self.test_scores = []
        self.files = []
        self.is_collection = False
        self.download_status = "denied"
        self.path = None


# ------------------------------------------------------------------
# The user_step_decorator — wraps user code, creates client, exposes
# self.anaconda_models before yield. Paints card after yield.
# ------------------------------------------------------------------


@user_step_decorator
def _anaconda_models_wrapper(step_name, flow, inputs=None, attr=None):
    """Runtime wrapper injected by the anaconda_models StepMutator."""
    import os
    from .client import AnacondaModelClient

    attr = attr or {}
    temp_dir_root = attr.get("temp_dir_root")

    # Get the card (injected by mutate). If card is unavailable for any
    # reason, we still work — just no card output.
    card = None
    try:
        from metaflow import current

        card = current.card["anaconda_models"]
    except Exception:
        pass

    client = AnacondaModelClient()
    accessor = _AnacondaModelsAccessor(client, temp_dir_root, card)
    flow.anaconda_models = accessor

    try:
        yield  # user's step code runs here
    finally:
        # Final card paint — captures all models used during the step.
        if card is not None:
            try:
                _paint_card(card, accessor.models)
            except Exception:
                pass  # card painting must never break the user process


# ------------------------------------------------------------------
# Accessor — the object exposed as self.anaconda_models inside the step
# ------------------------------------------------------------------


class _AnacondaModelsAccessor:
    """
    Exposed as ``self.anaconda_models`` inside a step.

    Wraps AnacondaModelClient with the temp_dir_root baked in,
    so the user only needs to specify model name.

    Tracks all models resolved/pulled during the step via ``.models``.
    Incrementally updates the card after each .model() call.
    """

    def __init__(self, client, temp_dir_root, card=None):
        self._client = client
        self._temp_dir_root = temp_dir_root
        self._card = card
        self._models = []

    @property
    def models(self):
        """All models resolved/pulled in this step (in order)."""
        return list(self._models)

    def model(self, model, pull=False, **filters):
        """
        Resolve a model from the Anaconda catalog. Single-file gguf quants
        and multi-file safetensor collections both come through here —
        filters pick what lands on disk.

        Parameters
        ----------
        model : str
            Model name in the catalog (e.g. "Qwen2.5-0.5B").
        pull : bool
            If True, download the model immediately.
        **filters
            Field constraints used to pick the file, e.g.
            ``quant_method="q4_k_m"``, ``format="gguf"`` or
            ``format="safetensors"`` (resolves the collection; If omitted,
            the smallest published single file is chosen.

        Returns
        -------
        AnacondaModel or _DeniedModel
            The model handle. Call .pull() to download, .path for location
            (a file for single files, a HuggingFace-layout directory for
            collections). If access is denied by policy, returns a
            _DeniedModel with .access_denied_reason set.
        """
        try:
            m = self._client.model(
                model,
                root_dir=self._temp_dir_root,
                **filters,
            )
            if pull:
                m.pull()
        except ModelAccessDenied as e:
            m = _DeniedModel(name=model, reason=e.reason)

        self._models.append(m)

        # Incrementally paint card after each model is resolved/pulled.
        if self._card is not None:
            try:
                _paint_card(self._card, self._models)
            except Exception:
                pass  # never break user process

        return m

    def list_models(self, limit=20, **filters):
        """List models from the catalog (passthrough to client)."""
        return self._client.list_models(limit=limit, **filters)


# ------------------------------------------------------------------
# StepMutator — the @anaconda_models(...) decorator itself
# ------------------------------------------------------------------


class anaconda_models(StepMutator):
    """
    Pull Anaconda catalog models inside a Metaflow step.

    Injects ``@card`` and exposes ``self.anaconda_models`` with a
    ``.model(...)`` method. Authentication is handled via OBP platform
    environment variables (OBP_API_SERVER, OBP_PERIMETER, METAFLOW_SERVICE_HEADERS).

    Parameters
    ----------
    temp_dir_root : str, optional
        Root directory for downloaded model files.
        Defaults to a new temp directory per step execution.
    """

    def init(self, temp_dir_root=None):
        self._temp_dir_root = temp_dir_root

    def mutate(self, mutable_step):
        # 0. Prevent duplicate @anaconda_models on the same step.
        for spec in mutable_step.decorator_specs:
            if spec[0] == "_anaconda_models_wrapper":
                return  # already mutated

        # 1. Inject @card FIRST (outermost) so current.card is ready
        #    before the wrapper runs.
        mutable_step.add_decorator(
            "card",
            deco_kwargs={
                "type": "blank",
                "id": "anaconda_models",
                "save_on_fail": True,
            },
            duplicates=mutable_step.IGNORE,
        )

        # 2. Add the runtime wrapper that creates the client.
        mutable_step.add_decorator(
            _anaconda_models_wrapper,
            deco_kwargs={
                "temp_dir_root": self._temp_dir_root,
            },
            duplicates=mutable_step.ERROR,
        )
