"""The iOS producer's own claims about what it publishes.

The rest of the iOS parser is asserted from the runner, against a captured corpus
of eight apps. What is stated here is the one claim that cannot be read off the
rows: how many elements the DRIVER would return for a selector compiled from
them, which is a different number precisely because the parser admits fewer nodes
than `find_elements` searches.
"""
from testmu_appium.perception import parse_tree

SCREEN_W, SCREEN_H = 414, 896

#: A UIKit button as it really appears: the control is the accessibility element
#: and its caption is a separate `accessible="false"` StaticText INSIDE it. The
#: two buttons differ in exactly one way, and it is the difference that decides
#: whether the identifier is ambiguous — `toast` carries a developer identifier
#: the caption does not repeat, while `Text` has none, so `name` fell back to the
#: label and the caption carries the same string.
FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<XCUIElementTypeApplication type="XCUIElementTypeApplication" name="Proverbial"
    label="Proverbial" enabled="true" visible="true" accessible="false"
    x="0" y="0" width="414" height="896">
  <XCUIElementTypeButton type="XCUIElementTypeButton" name="toast" label="Toast"
      enabled="true" visible="true" accessible="true"
      x="20" y="448" width="177" height="41">
    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" name="Toast"
        value="Toast" label="Toast" enabled="true" visible="true"
        accessible="false" x="90" y="460" width="36" height="17"/>
  </XCUIElementTypeButton>
  <XCUIElementTypeButton type="XCUIElementTypeButton" name="Text" label="Text"
      enabled="true" visible="true" accessible="true"
      x="20" y="548" width="177" height="41">
    <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" name="Text"
        value="Text" label="Text" enabled="true" visible="true"
        accessible="false" x="94" y="560" width="28" height="17"/>
  </XCUIElementTypeButton>
</XCUIElementTypeApplication>
"""


def _rows():
    return parse_tree(FIXTURE, SCREEN_W, SCREEN_H, platform="ios")


def _row(name):
    return next(r for r in _rows() if r["name"] == name)


class TestTheCaptionIsNotARow:
    """Unchanged behaviour, asserted because the counts below depend on it."""

    def test_a_button_and_its_caption_are_one_row(self):
        assert [r["name"] for r in _rows()] == ["Toast", "Text"]

    def test_the_row_is_the_control_and_not_the_caption(self):
        assert _row("Text")["cls"] == "XCUIElementTypeButton"


class TestTheCountTheDriverWouldGet:
    """`find_elements` searches the hierarchy; the rows are a subset of it.

    Uniqueness judged on the rows alone is judged on a set the caption was
    removed from, and answers optimistically — the failure it produces is a
    recorded selector that resolves to two elements at replay.
    """

    def test_an_identifier_the_caption_repeats_is_reported_twice(self):
        assert _row("Text")["query_matches"]["content_desc"] == 2

    def test_the_rows_alone_would_have_called_it_unique(self):
        rows = _rows()
        assert sum(1 for r in rows if r["content_desc"] == "Text") == 1

    def test_pinning_the_type_beside_it_resolves_to_the_control(self):
        assert _row("Text")["query_matches"]["content_desc+cls"] == 1

    def test_a_developer_identifier_the_caption_does_not_repeat_stays_unique(self):
        """`toast` is the identifier; `Toast` is the caption. Different strings,
        so the query for one never returns the other."""
        assert _row("Toast")["query_matches"]["content_desc"] == 1

    def test_a_label_query_counts_nodes_rather_than_attributes(self):
        """`text` compiles to `label == v OR name == v OR value == v`. The caption
        answers on all three and the button on two; that is two elements, not
        five."""
        assert _row("Toast")["query_matches"]["name"] == 2

    def test_a_row_with_no_identifier_publishes_no_identifier_count(self):
        """Absent, not zero: nothing was measured, so nothing is claimed."""
        rows = parse_tree(
            FIXTURE.replace('name="Text"', 'name=""'), SCREEN_W, SCREEN_H,
            platform="ios")
        unidentified = next(r for r in rows if r["name"] == "Text")
        assert "content_desc" not in unidentified["query_matches"]


class TestTheTabBarRescue:
    """WDA reports on-screen, drawn, tappable tab-bar buttons `visible="false"`
    while the bar containing them reports true — which dropped an app's primary
    navigation from every capture. The rescue is deliberately the narrowest
    gate that readmits them: accessible, on screen, and the PARENT's word."""

    _XML = """<AppiumAUT>
<XCUIElementTypeApplication type="XCUIElementTypeApplication" name="Demo"
    enabled="true" visible="true" accessible="false" x="0" y="0" width="414" height="896">
  <XCUIElementTypeTabBar type="XCUIElementTypeTabBar" name="Tab Bar"
      enabled="true" visible="true" accessible="false"
      x="0" y="813" width="414" height="83">
    <XCUIElementTypeButton type="XCUIElementTypeButton" name="Home" label="Home"
        enabled="true" visible="false" accessible="true"
        x="2" y="814" width="136" height="48"/>
    <XCUIElementTypeButton type="XCUIElementTypeButton" name="Search" label="Search"
        enabled="true" visible="false" accessible="true"
        x="139" y="814" width="136" height="48"/>
  </XCUIElementTypeTabBar>
  <XCUIElementTypeOther type="XCUIElementTypeOther" name="offstage" label="offstage"
      enabled="true" visible="false" accessible="true"
      x="0" y="900" width="414" height="50"/>
  <XCUIElementTypeOther type="XCUIElementTypeOther" name="hidden-parent-hidden"
      label="hidden-parent-hidden" enabled="true" visible="false" accessible="false"
      x="0" y="100" width="100" height="40"/>
</XCUIElementTypeApplication>
</AppiumAUT>"""

    def _names(self):
        return [r["name"] for r in parse_tree(self._XML, SCREEN_W, SCREEN_H,
                                              platform="ios")]

    def test_tab_buttons_under_a_visible_bar_are_admitted(self):
        names = self._names()
        assert "Home" in names and "Search" in names

    def test_an_off_screen_invisible_node_stays_out(self):
        """The parent says visible, the node is accessible — but it is BELOW
        the screen, and bounds still gate."""
        assert "offstage" not in self._names()

    def test_an_inaccessible_invisible_node_stays_out(self):
        assert "hidden-parent-hidden" not in self._names()


class TestTheAnchorClimbStopsAtTheList:
    """Two identical buttons in two cells of one Table, one unique header
    OUTSIDE it. Climbing past the Table would hand both cells that header as a
    "sibling" anchor — unique on screen, matching both copies."""

    _XML = """<AppiumAUT>
<XCUIElementTypeApplication type="XCUIElementTypeApplication" name="Demo"
    enabled="true" visible="true" accessible="false" x="0" y="0" width="414" height="896">
  <XCUIElementTypeStaticText type="XCUIElementTypeStaticText" name="Payees"
      value="Payees" label="Payees" enabled="true" visible="true"
      accessible="true" x="20" y="60" width="100" height="20"/>
  <XCUIElementTypeTable type="XCUIElementTypeTable" enabled="true" visible="true"
      accessible="false" x="0" y="100" width="414" height="700">
    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true"
        accessible="false" x="0" y="100" width="414" height="80">
      <XCUIElementTypeButton type="XCUIElementTypeButton" name="Pay" label="Pay"
          enabled="true" visible="true" accessible="true"
          x="300" y="120" width="80" height="40"/>
    </XCUIElementTypeCell>
    <XCUIElementTypeCell type="XCUIElementTypeCell" enabled="true" visible="true"
        accessible="false" x="0" y="180" width="414" height="80">
      <XCUIElementTypeButton type="XCUIElementTypeButton" name="Pay" label="Pay"
          enabled="true" visible="true" accessible="true"
          x="300" y="200" width="80" height="40"/>
    </XCUIElementTypeCell>
  </XCUIElementTypeTable>
</XCUIElementTypeApplication>
</AppiumAUT>"""

    def test_a_repeated_control_does_not_inherit_the_outside_header(self):
        rows = parse_tree(self._XML, SCREEN_W, SCREEN_H, platform="ios")
        for row in rows:
            if row["name"] != "Pay":
                continue
            anchors = [a["value"] for a in row["anchors"]["sibling"]]
            assert "Payees" not in anchors, (
                "the header outside the Table would match every cell")


class TestTheOwningApplication:
    """The Application element is `accessible=false` and never earns a row, so
    a `root is node` test stamped every row's `package` with ""."""

    def test_every_row_carries_the_application_name(self):
        for row in _rows():
            assert row["package"] == "Proverbial"
