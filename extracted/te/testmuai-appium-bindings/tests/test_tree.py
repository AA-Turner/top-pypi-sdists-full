"""The Android producer's own claims about what it publishes.

The parse itself is asserted from the runner against a captured corpus. What is
stated here is the one claim that cannot be read off the rows: how many elements
the DRIVER would return for a selector compiled from them, which is a different
number because the parser admits fewer nodes than `find_elements` searches.
"""
from testmu_appium.perception import parse_tree

SCREEN_W, SCREEN_H = 1080, 2340

#: A WebView screen as Chrome really projects one. The same link arrives twice:
#: the node the parser admits, and a twin with zero height carrying the same
#: strings. `_parse_bounds` rejects the twin, `find_elements` does not — measured
#: at 556 zero-area nodes across the Android corpus, overwhelmingly on the
#: WebView screen.
PROJECTED = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node class="android.widget.FrameLayout" bounds="[0,0][1080,2340]">
    <node class="android.view.View" resource-id="com.app:id/cta"
          content-desc="Contact Sales" text="Contact Sales"
          clickable="true" enabled="true" bounds="[40,100][440,220]"/>
    <node class="android.widget.TextView"
          content-desc="Contact Sales" text="Contact Sales"
          bounds="[93,84][480,84]"/>
    <node class="android.widget.Button" resource-id="com.app:id/go" text="Go"
          clickable="true" enabled="true" bounds="[40,300][440,420]"/>
  </node>
</hierarchy>
"""

#: Two cards whose quantity readouts share an id AND the value printed in them.
#: This is the shape `view_id_text` exists for, and the one it gets wrong: the
#: compound is emitted as unambiguous without anything having measured it.
RECYCLED = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node class="android.widget.FrameLayout" bounds="[0,0][1080,2340]">
    <node class="android.widget.TextView" resource-id="com.app:id/qty" text="1"
          bounds="[40,100][240,200]"/>
    <node class="android.widget.TextView" resource-id="com.app:id/qty" text="1"
          bounds="[40,300][240,400]"/>
  </node>
</hierarchy>
"""


def _rows(xml=PROJECTED):
    return parse_tree(xml, SCREEN_W, SCREEN_H)


def _row(name, xml=PROJECTED):
    return next(r for r in _rows(xml) if r["name"] == name)


class TestTheTwinIsNotARow:
    """Unchanged behaviour, asserted because the counts below depend on it."""

    def test_a_zero_height_node_earns_no_row(self):
        assert [r["name"] for r in _rows()] == ["Contact Sales", "Go"]

    def test_the_row_is_the_node_that_has_area(self):
        assert _row("Contact Sales")["bounds"] == (40, 100, 440, 220)


class TestTheCountTheDriverWouldGet:
    """`find_elements` searches the hierarchy; the rows are a subset of it.

    Uniqueness judged on the rows alone is judged on a set the twin was removed
    from, and answers optimistically — the failure it produces is a recorded
    selector that resolves to two elements at replay.
    """

    def test_a_text_the_twin_repeats_is_reported_twice(self):
        assert _row("Contact Sales")["query_matches"]["text"] == 2

    def test_a_description_the_twin_repeats_is_reported_twice(self):
        assert _row("Contact Sales")["query_matches"]["content_desc"] == 2

    def test_the_rows_alone_would_have_called_it_unique(self):
        rows = _rows()
        assert sum(1 for r in rows if r["text"] == "Contact Sales") == 1

    def test_an_id_the_twin_does_not_carry_stays_unique(self):
        assert _row("Contact Sales")["query_matches"]["resource_id"] == 1

    def test_a_row_publishes_no_count_for_a_field_it_does_not_carry(self):
        """Absent, not zero: nothing was measured, so nothing is claimed."""
        assert "content_desc" not in _row("Go")["query_matches"]

    def test_a_field_a_row_does_carry_is_always_reported(self):
        assert _row("Go")["query_matches"]["resource_id"] == 1
        assert _row("Go")["query_matches"]["text"] == 1


class TestTheCompoundStrategy:
    """`view_id_text` pins two fields, so its count is its own question.

    A recycled id paired with the text beside it is the usual way out of an
    ambiguous row — but two cards showing the same quantity share both, and
    nothing today measures that.
    """

    def test_the_pair_is_reported_for_a_row_carrying_both(self):
        row = _rows(RECYCLED)[0]
        assert row["query_matches"]["resource_id+text"] == 2

    def test_the_pair_is_absent_when_the_row_carries_only_one_half(self):
        rows = parse_tree(
            RECYCLED.replace('text="1"', 'text=""'), SCREEN_W, SCREEN_H)
        assert "resource_id+text" not in rows[0]["query_matches"]

    def test_a_pair_no_other_node_repeats_is_unique(self):
        assert _row("Go")["query_matches"]["resource_id+text"] == 1
