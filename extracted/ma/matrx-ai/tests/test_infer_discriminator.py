"""Missing action/command inference for dispatcher tools.

A rejected tool call still costs a full provider turn. When the discriminator
is omitted but variant-unique fields uniquely identify the action, fill it in;
when they conflict or nothing unique is present, return an actionable menu —
never Pydantic's "Unable to extract tag using discriminator …".
"""

from __future__ import annotations

from pydantic import ValidationError

from matrx_ai.tools._dispatch_util import (
    format_args_error,
    infer_missing_discriminator,
)
from matrx_ai.tools.arg_models import ContextArgs, CtxPatchArgs
from matrx_ai.tools.arg_models.web_args import WebArgs

# ---------------------------------------------------------------------------
# web — queries / url / urls
# ---------------------------------------------------------------------------


class TestWebInference:
    def test_queries_infers_search(self) -> None:
        r = infer_missing_discriminator({"queries": ["ai agents"]}, WebArgs)
        assert r.kind == "inferred"
        assert r.tag == "search"
        assert r.args is not None and r.args["action"] == "search"
        WebArgs.model_validate(r.args)

    def test_url_infers_read(self) -> None:
        r = infer_missing_discriminator({"url": "https://example.com"}, WebArgs)
        assert r.kind == "inferred" and r.tag == "read"
        assert r.args is not None
        WebArgs.model_validate(r.args)

    def test_urls_infers_batch_read(self) -> None:
        r = infer_missing_discriminator({"urls": ["https://a.com", "https://b.com"]}, WebArgs)
        assert r.kind == "inferred" and r.tag == "batch_read"
        assert r.args is not None
        WebArgs.model_validate(r.args)

    def test_conflicting_queries_and_url(self) -> None:
        r = infer_missing_discriminator({"queries": ["x"], "url": "https://example.com"}, WebArgs)
        assert r.kind == "ambiguous"
        assert r.error is not None
        assert "conflicting" in r.error.lower() or "Cannot infer" in r.error
        assert 'action="search"' in r.error
        assert 'action="read"' in r.error

    def test_empty_args_uninferable_with_menu(self) -> None:
        r = infer_missing_discriminator({}, WebArgs)
        assert r.kind == "uninferable"
        assert r.error is not None
        assert "action" in r.error
        assert "queries" in r.error
        assert "url" in r.error
        assert "urls" in r.error

    def test_action_already_set_is_not_applicable(self) -> None:
        r = infer_missing_discriminator({"action": "search", "queries": ["x"]}, WebArgs)
        assert r.kind == "not_applicable"

    def test_blank_action_treated_as_missing(self) -> None:
        r = infer_missing_discriminator({"action": "", "queries": ["x"]}, WebArgs)
        assert r.kind == "inferred" and r.tag == "search"


# ---------------------------------------------------------------------------
# context — key / requests / content
# ---------------------------------------------------------------------------


class TestContextInference:
    def test_key_alone_infers_get(self) -> None:
        r = infer_missing_discriminator({"key": "user_profile"}, ContextArgs)
        assert r.kind == "inferred" and r.tag == "get"
        assert r.args is not None
        ContextArgs.model_validate(r.args)

    def test_key_plus_content_infers_create(self) -> None:
        r = infer_missing_discriminator({"key": "scratch", "content": "hello"}, ContextArgs)
        assert r.kind == "inferred" and r.tag == "create"
        assert r.args is not None
        ContextArgs.model_validate(r.args)

    def test_requests_infers_batch(self) -> None:
        r = infer_missing_discriminator({"requests": [{"key": "a"}, {"key": "b"}]}, ContextArgs)
        assert r.kind == "inferred" and r.tag == "batch"
        assert r.args is not None
        ContextArgs.model_validate(r.args)


# ---------------------------------------------------------------------------
# context_patch — unique optional fields break the all-require-key tie
# ---------------------------------------------------------------------------


class TestContextPatchInference:
    def test_operations_infers_json_patch(self) -> None:
        r = infer_missing_discriminator(
            {"key": "doc", "operations": [{"op": "replace", "path": "/a", "value": 1}]},
            CtxPatchArgs,
        )
        assert r.kind == "inferred" and r.tag == "json_patch"

    def test_key_alone_ambiguous(self) -> None:
        r = infer_missing_discriminator({"key": "doc"}, CtxPatchArgs)
        assert r.kind == "ambiguous"
        assert r.error is not None
        assert "command" in r.error


# ---------------------------------------------------------------------------
# Prefer required-field variants over empty-required catch-alls
# ---------------------------------------------------------------------------


class TestPreferRequiredOverCatchall:
    def test_memory_query_infers_search_not_recall(self) -> None:
        from matrx_ai.tools.arg_models.memory_args import MemoryArgs

        r = infer_missing_discriminator({"query": "prefs"}, MemoryArgs)
        assert r.kind == "inferred" and r.tag == "search"

    def test_memory_empty_infers_recall(self) -> None:
        from matrx_ai.tools.arg_models.memory_args import MemoryArgs

        r = infer_missing_discriminator({}, MemoryArgs)
        assert r.kind == "inferred" and r.tag == "recall"


# ---------------------------------------------------------------------------
# format_args_error — no more raw discriminator vomit as the only signal
# ---------------------------------------------------------------------------


class TestFormatDiscriminatorError:
    def test_union_tag_not_found_is_readable(self) -> None:
        try:
            WebArgs.model_validate({"queries": ["x"]})
        except ValidationError as exc:
            msg = format_args_error(exc)
        assert "Unable to extract tag" not in msg
        assert "action" in msg
