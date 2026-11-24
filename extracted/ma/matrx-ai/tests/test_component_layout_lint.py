"""The layout contract's save checks WARN with the fix and never refuse (CGU-09 kind shell)."""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_ai.tools.implementations import kind_component as kc
from matrx_ai.tools.implementations import kind_layer
from matrx_ai.tools.implementations.kind_shared import (
    component_layout_lint,
    component_save_notices,
    component_source_lint,
)

CAPPED = """export default function C({ data }) {
  return <div className="space-y-2">
    <KindHeaderBar title="T" />
    <div className="max-h-64 overflow-y-auto">{data.body}</div>
  </div>;
}"""
CLEAN = """export default function C({ data }) {
  return <div className="space-y-2">
    <KindHeaderBar title="T" />
    <ChatClamp>{data.body}</ChatClamp>
  </div>;
}"""
FULL = """export default function C({ data }) {
  const [o, setO] = useState(false);
  return <div>{o && <div className="fixed inset-0 z-50 bg-background">{data.body}</div>}</div>;
}"""
PADDED = """export default function C({ data }) {
  return <div className="px-3 py-2 space-y-2"><KindHeaderBar title="T" />{data.body}</div>;
}"""


def test_warning_fires_on_a_capped_scroller_and_offers_the_fix() -> None:
    (line,) = component_layout_lint(CAPPED)
    assert "max-h-* overflow-y-auto" in line and "ChatClamp" in line
    assert component_layout_lint('<div className="overflow-y-auto max-h-[320px]">')
    assert component_layout_lint(CLEAN) == []
    assert component_layout_lint('<div className="overflow-y-auto">') == []
    assert component_layout_lint('<div className="max-h-64 overflow-hidden">') == []


def test_own_full_screen_and_outer_padding_warn() -> None:
    (full,) = component_layout_lint(FULL)
    assert "KindHeaderBar" in full and "fixed inset-0" in full
    (pad,) = component_layout_lint(PADDED)
    assert "outermost" in pad
    assert component_layout_lint('return <div className="space-y-2"><p className="px-2">x</p></div>') == []
    assert component_layout_lint(None) == []


def test_a_warning_never_refuses_the_save() -> None:
    assert component_source_lint(CAPPED) is None
    # The fixture draws <KindHeaderBar> unimported, so the unbound-element offer follows the layout one.
    assert component_save_notices(CAPPED)[:1] == component_layout_lint(CAPPED)


def test_every_write_tool_attaches_the_layout_notices() -> None:
    for fn in (kc._kindcomp_update_code_save, kc._kindcomp_patch_code_save, kind_layer.layer_create):
        assert "component_save_notices(" in stable_source(fn), fn.__name__
