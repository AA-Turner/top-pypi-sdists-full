"""An element the body draws but never binds is named at save (copperline_job_card, 2026-11-17).

The frame renders such an element as a 'Not found' stand-in and files ``unresolved_import`` rows; the save
offers the fix first. It is an offer, never a refusal (a design-system part the frame supplies bare is fine).
"""

from __future__ import annotations

from matrx_ai.tools.implementations.kind_shared import (
    component_save_notices,
    unresolved_jsx_elements,
    unresolved_jsx_notices,
)

LIVE_DEFECT = """
import { KindHeaderBar } from "@/components/kind-kit/KindHeaderBar";
export default function JobCard({ data }) {
  return (
    <div className="space-y-3">
      <KindHeaderBar title={data?.title ?? "Job"} />
      <RichContent content={data?.notes ?? ""} />
    </div>
  );
}
"""

BOUND = """
import { KindHeaderBar } from "@/components/kind-kit/KindHeaderBar";
import Markdown from "@/components/Markdown";
import { Check } from "lucide-react";
// <Commented /> is not drawn
function Row({ icon: Icon, label }) { return <li><Icon className="h-4" />{label}</li>; }
const Panel = ({ children }) => <section>{children}</section>;
export default function Card({ data }) {
  const ref = React.useRef<HTMLDivElement>(null);
  const [m] = useState<Record<string, Array<number>>>({});
  return (
    <Panel>
      <KindHeaderBar title={data?.title} />
      <Markdown content={data?.body} />
      <Row icon={Check} label="ok" />
      <Check />
      <React.Fragment />
    </Panel>
  );
}
"""


def test_the_live_defect_names_the_unbound_element() -> None:
    assert unresolved_jsx_elements(LIVE_DEFECT) == ["RichContent"]
    notes = unresolved_jsx_notices(LIVE_DEFECT)
    assert len(notes) == 1 and "<RichContent>" in notes[0]
    assert any("<RichContent>" in n for n in component_save_notices(LIVE_DEFECT))


def test_imported_declared_destructured_icons_and_generics_are_bound() -> None:
    assert unresolved_jsx_elements(BOUND) == []
    assert unresolved_jsx_notices(BOUND) == []
