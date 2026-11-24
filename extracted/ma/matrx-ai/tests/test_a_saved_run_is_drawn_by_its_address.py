"""A button whose run saves its answer as a record is drawn by the record's address, never by ``output``.

FIX-L7 (2026-11-03, release 36eaeafb684): Company Setup built a "Social post" card whose
"Analyse this post" button ran ``into: { state: "analysis_run", record: {} }`` and drew
``itemState.analysis_run.output``. A run with ``into.record`` keeps only the saved record's
``address`` on the item (``KindRunView``, Doctrine R6), so after ~100 s the button said
"Saved" and the card showed nothing — even after reload — and the analysis card's own
"Draft post ideas" button never appeared. The component write gate now refuses that source
and names the right shape (``<Kind record={itemState.X.address._record_id} />``).
"""

from __future__ import annotations

import pytest

from matrx_ai.tools.implementations.kind_shared import component_run_output_lint

# The live card's shape (content_ir.kind_component "social_post_card", org torn down), trimmed.
LIVE_SOCIAL_POST_CARD = """
import { KindActionButton } from "@/components/kind-kit/KindActionButton";
const ANALYSE_JOB = "bakery_post.analyse_post";
export default function SocialPost({ data, runAction, itemState }) {
  const arun = itemState?.analysis_run;
  const a = arun?.output && typeof arun.output === "object" ? arun.output : null;
  return (
    <div>
      <KindActionButton runAction={runAction} action="run"
        input={() => ({ mandate: ANALYSE_JOB, variables: { title: data?.title ?? "" },
                        into: { state: "analysis_run", record: {} } })}
        label={a ? "Analyse again" : "Analyse this post"} />
      {a ? <p>{a.summary}</p> : null}
    </div>
  );
}
"""

DRAWN_BY_ADDRESS = """
import { KindActionButton } from "@/components/kind-kit/KindActionButton";
import { Kind } from "@ai-matrx/applets/react";
export default function SocialPost({ data, runAction, itemState }) {
  const saved = itemState?.analysis_run?.address?._record_id;
  return (
    <div>
      <KindActionButton runAction={runAction} action="run"
        input={() => ({ mandate: "bakery_post.analyse_post", variables: { title: data?.title ?? "" },
                        into: { state: "analysis_run", record: {} } })}
        label="Analyse this post" />
      {saved ? <Kind record={saved} /> : null}
    </div>
  );
}
"""

KEPT_ON_THE_ITEM = """
export default function PostIdea({ data, runAction, itemState }) {
  const ref = itemState?.idea_0_image?.output?.images?.[0];
  return <KindActionButton runAction={runAction} action="run"
    input={() => ({ action: "workflow.id_dafe8ad8897e4bf1bd92cb86530e8aaa", input: { prompt: data.title },
                    into: { state: "idea_0_image" } })} label="Generate image" />;
}
"""


def test_the_live_card_that_said_saved_and_showed_nothing_is_refused() -> None:
    refusal = component_run_output_lint(LIVE_SOCIAL_POST_CARD)
    assert refusal is not None
    assert "itemState.analysis_run" in refusal
    assert "<Kind record={itemState.analysis_run?.address?._record_id} />" in refusal
    assert "Nothing was written" in refusal


@pytest.mark.parametrize(
    "reader",
    [
        "const v = itemState.analysis_run.output;",
        "const v = itemState?.analysis_run?.output;",
        'const v = itemState["analysis_run"]?.output;',
        "const { analysis_run } = itemState; const v = analysis_run?.output;",
        "const { analysis_run: run } = itemState; const v = run.output;",
    ],
)
def test_every_way_of_reading_output_off_a_record_landed_run_is_caught(reader: str) -> None:
    source = (
        "export default function C({ data, runAction, itemState }) { "
        + reader
        + ' return <KindActionButton runAction={runAction} action="run" '
        'input={{ mandate: "x.y", into: { state: "analysis_run", record: { table: "t" } } }} label="Go" />; }'
    )
    assert component_run_output_lint(source) is not None


def test_drawing_the_saved_record_by_its_address_passes() -> None:
    assert component_run_output_lint(DRAWN_BY_ADDRESS) is None


def test_a_run_kept_on_the_item_may_read_its_output() -> None:
    assert component_run_output_lint(KEPT_ON_THE_ITEM) is None


def test_a_key_some_run_fills_without_a_record_may_read_output() -> None:
    source = (
        "export default function C({ data, runAction, itemState }) { const o = itemState.r?.output; return <>"
        '<KindActionButton runAction={runAction} action="run" input={{ mandate: "a.b", into: { state: "r", record: {} } }} label="Save" />'
        '<KindActionButton runAction={runAction} action="run" input={{ mandate: "a.b", into: { state: "r" } }} label="Try" />'
        "</>; }"
    )
    assert component_run_output_lint(source) is None


@pytest.mark.asyncio
async def test_the_component_write_gate_refuses_it() -> None:
    from matrx_ai.tools.implementations.kind_component import _refuse_broken_source

    refusal, _checked = await _refuse_broken_source(LIVE_SOCIAL_POST_CARD)
    assert refusal is not None
    assert "address" in str(refusal.error.message if refusal.error else refusal)
