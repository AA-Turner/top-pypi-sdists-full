"""Tests for the post-generation ``Literal[<single-value>]`` defaults
injection in ``scripts/post_generate_fixes.py``.

The injection turns spec-required discriminator fields (whose type is
``Literal['x']`` with a single value) into defaulted fields. Wire
consumers are unaffected — the Literal type still enforces the tag.
In-process construction becomes ergonomic — ``TextContent(content='x')``
works without having to repeat ``asset_type='text'``.

These tests pin the behavior across a sampling of Asset, Pricing, and
Response types so a future regen that breaks the injection fails loudly
at the right layer.
"""

from __future__ import annotations

import pytest


class TestAssetContentDefaults:
    """Asset-content types all default their ``asset_type``
    discriminator to the correct tag."""

    def test_text_content_defaults_asset_type(self) -> None:
        from adcp.types import TextContent

        t = TextContent(content="hello")
        assert t.asset_type == "text"
        assert t.content == "hello"

    def test_html_content_defaults_asset_type(self) -> None:
        from adcp.types import HtmlContent

        h = HtmlContent(content="<p>x</p>")
        assert h.asset_type == "html"

    def test_css_content_defaults_asset_type(self) -> None:
        from adcp.types import CssContent

        c = CssContent(content="body{}")
        assert c.asset_type == "css"

    def test_javascript_content_defaults_asset_type(self) -> None:
        from adcp.types import JavascriptContent

        j = JavascriptContent(content="alert(1)")
        assert j.asset_type == "javascript"

    def test_url_content_defaults_asset_type(self) -> None:
        from adcp.types import UrlContent

        u = UrlContent(url="https://example.com/asset.jpg")
        assert u.asset_type == "url"


class TestVastDaastDiscriminators:
    """VAST/DAAST have two discriminators: ``asset_type`` (vast/daast)
    AND ``delivery_type`` (url/inline). Both are single-value Literals
    per the spec's oneOf-of-oneOfs structure; both get defaults."""

    def test_url_vast_asset_defaults_both_discriminators(self) -> None:
        from adcp.types.aliases import UrlVastAsset

        a = UrlVastAsset(url="https://vast.example.com/ad.xml")
        assert a.asset_type == "vast"
        assert a.delivery_type == "url"

    def test_inline_vast_asset_defaults_both_discriminators(self) -> None:
        from adcp.types.aliases import InlineVastAsset

        a = InlineVastAsset(content="<VAST>...</VAST>")
        assert a.asset_type == "vast"
        assert a.delivery_type == "inline"

    def test_url_daast_asset_defaults_both_discriminators(self) -> None:
        from adcp.types.aliases import UrlDaastAsset

        a = UrlDaastAsset(url="https://daast.example.com/ad.xml")
        assert a.asset_type == "daast"
        assert a.delivery_type == "url"


class TestDefaultsPreserveValidation:
    """The injected defaults are a construction convenience. The
    ``Literal`` type still rejects any OTHER value passed explicitly —
    defaulting doesn't weaken validation."""

    def test_wrong_explicit_asset_type_rejected(self) -> None:
        from pydantic import ValidationError

        from adcp.types import TextContent

        with pytest.raises(ValidationError):
            TextContent(asset_type="html", content="x")  # type: ignore[arg-type]

    def test_wrong_explicit_delivery_type_rejected(self) -> None:
        from pydantic import ValidationError

        from adcp.types.aliases import UrlVastAsset

        with pytest.raises(ValidationError):
            UrlVastAsset(
                delivery_type="inline",  # type: ignore[arg-type]
                url="https://vast.example.com/ad.xml",
            )


class TestDefaultsHonourWireFormat:
    """Validating a dict (wire format) still works — the defaults are
    injected via field metadata, not by pre-filling the input."""

    def test_text_content_from_wire_dict(self) -> None:
        from adcp.types import TextContent

        t = TextContent.model_validate({"asset_type": "text", "content": "hi"})
        assert t.asset_type == "text"
        assert t.content == "hi"

    def test_text_content_from_wire_dict_without_asset_type_still_works(self) -> None:
        """Wire consumers that omit the discriminator also get the
        default — useful for minimal client implementations."""
        from adcp.types import TextContent

        t = TextContent.model_validate({"content": "hi"})
        assert t.asset_type == "text"


class TestInjectorBehavior:
    """Meta-tests pinning the injector's pattern-match semantics. If
    these fail, the post-gen script's scope has drifted."""

    def test_injector_skips_multi_value_literals(self) -> None:
        """``Literal['a', 'b']`` fields stay required — there's no
        single correct default. The spec is saying "user must pick",
        and we must not pretend otherwise."""
        import ast

        from scripts.post_generate_fixes import _extract_single_literal_value

        # Annotated[Literal['a', 'b'], ...]
        module = ast.parse("x: Annotated[Literal['a', 'b'], Field()]")
        ann = module.body[0].annotation  # type: ignore[attr-defined]
        assert _extract_single_literal_value(ann) is None

    def test_injector_extracts_single_literal_value(self) -> None:
        import ast

        from scripts.post_generate_fixes import _extract_single_literal_value

        module = ast.parse("x: Annotated[Literal['text'], Field()]")
        ann = module.body[0].annotation  # type: ignore[attr-defined]
        assert _extract_single_literal_value(ann) == "text"

    def test_injector_extracts_bare_literal(self) -> None:
        """``Literal['x']`` without Annotated wrap also works."""
        import ast

        from scripts.post_generate_fixes import _extract_single_literal_value

        module = ast.parse("x: Literal['text']")
        ann = module.body[0].annotation  # type: ignore[attr-defined]
        assert _extract_single_literal_value(ann) == "text"

    def test_injector_skips_non_literal_annotations(self) -> None:
        import ast

        from scripts.post_generate_fixes import _extract_single_literal_value

        module = ast.parse("x: str")
        ann = module.body[0].annotation  # type: ignore[attr-defined]
        assert _extract_single_literal_value(ann) is None
