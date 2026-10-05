"""Real model `<decision>` output (live walk 2026-10-04) must parse to options.

Twin of the client test in matrx-frontend
components/mardown-display/blocks/inline-decision/__tests__/decision-real-output.test.ts —
same captured inputs, same expected labels.
"""

from matrx_ai.processing.blocks.parsers.decision_parser import parse_decision_from_raw_xml

INDENTED = """<decision prompt="Pick our first launch channel">
  <option id="email-waitlist" label="Email List / Waitlist">
    Reach out directly to people who have already shown interest; this offers the highest initial conversion rate and the fastest qualitative feedback.
  </option>
  <option id="niche-communities" label="Niche Communities & Early Adopter Platforms">
    Launch in targeted spaces like specialized subreddits, Discord/Slack groups, or Product Hunt to tap into an audience actively looking for new tools.
  </option>
  <option id="founder-social" label="Organic Social / Founder-Led Outreach">
    Share the launch story and problem-solving process on platforms like LinkedIn or X to generate organic traction and build trust in public.
  </option>
</decision>"""

LINE_START = """<decision prompt="Pick a pricing model">
<option id="subscription" label="Subscription (Monthly / Annual)">
Predictable recurring revenue.
</option>
<option id="freemium" label="Freemium with Premium Tiers">
A free base offering.
</option>
<option id="one-time" label="One-Time Early-Bird Access">
A discounted lifetime payment.
</option>
</decision>"""


def test_indented_with_id():
    d = parse_decision_from_raw_xml(INDENTED)
    assert d is not None and d.prompt == "Pick our first launch channel"
    assert [o.label for o in d.options] == [
        "Email List / Waitlist",
        "Niche Communities & Early Adopter Platforms",
        "Organic Social / Founder-Led Outreach",
    ]


def test_line_start_with_id():
    d = parse_decision_from_raw_xml(LINE_START)
    assert d is not None
    assert [o.label for o in d.options] == [
        "Subscription (Monthly / Annual)",
        "Freemium with Premium Tiers",
        "One-Time Early-Bird Access",
    ]


def test_single_quotes_and_self_describing():
    d = parse_decision_from_raw_xml(
        "<decision prompt='P'>\n<option label='A' id=\"a\">first</option>\n\n<option id=\"b\">Plain label only</option>\n</decision>"
    )
    assert d is not None
    assert [(o.label, o.text) for o in d.options] == [("A", "first"), ("Plain label only", "Plain label only")]
    assert d.prompt == "P"
