"""Contract tests for the binding-owned fresh-perception tree parser."""

from pathlib import Path

from testmu_appium._helpers import _tree

_FIXTURES = Path(__file__).resolve().parent / "fixtures"
_XML = _FIXTURES / "page_source_gmail.xml"


def test_indexing_is_one_based_and_dense():
    entries = _tree.parse_tree(_XML.read_text(), 1080, 2340)
    assert [e["index"] for e in entries] == list(range(1, len(entries) + 1))


def test_offscreen_entries_are_viewport_filtered():
    entries = _tree.parse_tree(_XML.read_text(), 1080, 2340)
    assert all("Offscreen" not in e["name"] for e in entries)


def test_role_map_covers_the_mobile_widget_families():
    entries = _tree.parse_tree(_XML.read_text(), 1080, 2340)
    roles = {e["name"]: e["role"] for e in entries}
    assert roles["Open navigation drawer"] == "button"
    assert roles["Search in mail"] == "input"
    assert roles["Star"] == "checkbox"
    assert roles["Conversation view"] == "switch"


def test_name_folding_assembles_row_labels():
    entries = _tree.parse_tree(_XML.read_text(), 1080, 2340)
    names = [e["name"] for e in entries]
    assert "LambdaTest · Your build finished · 10:24 AM" in names


def test_static_text_is_kept_but_not_added_to_the_visual_prompt():
    entries = _tree.parse_tree(_XML.read_text(), 1080, 2340)
    informational = [entry for entry in entries if not entry["interactive"]]
    assert informational
    lines = _tree.format_for_prompt(entries).splitlines()
    assert len(lines) == sum(entry["interactive"] for entry in entries)
    assert [line.split("]", 1)[0] for line in lines] == [
        f"[{index}" for index in range(1, len(lines) + 1)]


def test_an_anchor_records_the_relation_and_distance_it_came_from():
    """Ranking needs to know a card's own title from a neighbour's."""
    direct_xml = (
        '<hierarchy rotation="0">'
        '<node class="android.widget.LinearLayout" bounds="[0,0][1080,600]">'
        '<node class="android.widget.FrameLayout" bounds="[0,0][1080,300]">'
        '<node class="android.widget.TextView" text="Amul Milk"'
        ' bounds="[0,0][1080,100]"></node>'
        '<node class="android.widget.Button" clickable="true" text="ADD"'
        ' bounds="[0,100][1080,300]"></node>'
        "</node>"
        "</node>"
        "</hierarchy>"
    )
    distant_xml = (
        '<hierarchy rotation="0">'
        '<node class="android.widget.LinearLayout" bounds="[0,0][1080,600]">'
        '<node class="android.widget.FrameLayout" bounds="[0,0][1080,300]">'
        '<node class="android.widget.Button" clickable="true" text="ADD"'
        ' bounds="[0,100][1080,300]"></node>'
        "</node>"
        '<node class="android.widget.TextView" text="Sponsored"'
        ' bounds="[0,300][1080,400]"></node>'
        "</node>"
        "</hierarchy>"
    )

    direct_add = next(
        e for e in _tree.parse_tree(direct_xml, 1080, 2400) if e["name"] == "ADD"
    )
    distant_add = next(
        e for e in _tree.parse_tree(distant_xml, 1080, 2400) if e["name"] == "ADD"
    )
    direct = {a["value"]: a for a in direct_add["anchors"]["sibling"]}
    distant = {a["value"]: a for a in distant_add["anchors"]["sibling"]}

    assert direct["Amul Milk"]["relation"] == "sibling"
    assert direct["Amul Milk"]["climb"] == 1
    assert distant["Sponsored"]["climb"] > direct["Amul Milk"]["climb"]


def test_a_row_carries_the_package_that_drew_it():
    """A multi-window capture mixes system chrome with the app; the row says which."""
    xml = (
        '<hierarchy rotation="0">'
        '<node class="android.widget.TextView" text="7:19"'
        ' package="com.android.systemui" bounds="[0,0][200,80]" />'
        '<node class="android.widget.Button" clickable="true" text="Save"'
        ' package="com.app" bounds="[0,200][300,300]" />'
        "</hierarchy>"
    )

    rows = _tree.parse_tree(xml, 1080, 2400)

    assert [row["package"] for row in rows] == ["com.android.systemui", "com.app"]


def test_a_row_reports_a_long_press_and_a_missing_label():
    """Both are in the source and neither reaches the caller today."""
    xml = (
        '<hierarchy rotation="0">'
        '<node class="android.widget.TextView" text="Note" clickable="true"'
        ' long-clickable="true" bounds="[0,0][300,100]" />'
        '<node class="android.widget.ImageView" clickable="true" enabled="true"'
        ' NAF="true" bounds="[0,200][100,300]" />'
        "</hierarchy>"
    )

    note, icon = _tree.parse_tree(xml, 1080, 2400)

    assert note["affordances"] == ["long-press"]
    assert icon["affordances"] == ["unlabelled"]


def test_editability_is_published_as_a_neutral_field():
    xml = (
        '<hierarchy rotation="0">'
        '<node class="android.widget.EditText" bounds="[0,0][300,100]" />'
        '<node class="android.widget.Button" clickable="true" bounds="[0,200][300,300]" />'
        "</hierarchy>"
    )

    field, button = _tree.parse_tree(xml, 1080, 2400)

    assert field["editable"] is True
    assert button["editable"] is False


def test_android_source_metadata_is_preserved_and_normalized():
    xml = """<hierarchy rotation="0">
      <node index="2" class="android.widget.LinearLayout" resource-id="app:id/form"
            package="com.app" bounds="[0,0][1080,800]" window-id="41">
        <node class="android.widget.FrameLayout" bounds="[0,0][1080,500]">
          <node index="7" class="android.widget.EditText" resource-id="app:id/email"
                text="" hint="Email" bounds="[20,20][900,160]" displayed="true"
                clickable="true" enabled="true" focusable="true" focused="true"
                long-clickable="true" context-clickable="true" selected="false"
                dismissable="false" a11y-focused="true" a11y-important="true"
                screen-reader-focusable="true" input-type="33" multiline="true"
                max-text-length="80" selection-start="2" selection-end="4"
                content-invalid="true" error="Enter a valid address"
                pane-title="Account" tooltip-text="Work email" heading="true"
                text-entry-key="true" text-has-clickable-span="true"
                live-region="2" window-id="41" drawing-order="3"
                actions="ACTION_CLICK,ACTION_SET_TEXT,ACTION_COPY,ACTION_CLICK,ACTION_CUSTOM_THING"
                extras="AccessibilityNodeInfo.roleDescription=email field;AccessibilityNodeInfo.chromeRole=textbox" />
        </node>
      </node>
    </hierarchy>"""

    form, email = _tree.parse_tree(xml, 1080, 2400)

    assert form["source_index"] == 2
    assert form["source_path"] == (0,)
    assert form["parent_index"] is None
    assert email["source_index"] == 7
    assert email["source_path"] == (0, 0, 0)
    assert email["parent_index"] == form["index"]
    assert email["displayed"] is True
    assert email["clickable"] is True
    assert email["enabled"] is True
    assert email["focusable"] is True
    assert email["focused"] is True
    assert email["long_clickable"] is True
    assert email["context_clickable"] is True
    assert email["selected"] is False
    assert email["dismissable"] is False
    assert email["accessibility_focused"] is True
    assert email["a11y_important"] is True
    assert email["screen_reader_focusable"] is True
    assert email["input_type"] == 33
    assert email["input_kind"] == "email"
    assert email["multiline"] is True
    assert (email["selection_start"], email["selection_end"]) == (2, 4)
    assert email["max_text_length"] == 80
    assert email["content_invalid"] is True
    assert email["error_text"] == "Enter a valid address"
    assert email["pane_title"] == "Account"
    assert email["tooltip_text"] == "Work email"
    assert email["live_region"] == 2
    assert email["window_id"] == 41
    assert email["drawing_order"] == 3
    assert email["accessibility_actions"] == [
        "ACTION_CLICK", "ACTION_SET_TEXT", "ACTION_COPY", "ACTION_CLICK",
        "ACTION_CUSTOM_THING"]
    assert email["capabilities"] == [
        "activate", "focus", "long-press", "context-click", "set-text", "copy",
        "custom-thing"]
    assert email["semantic_traits"] == [
        "heading", "text-entry-key", "clickable-span"]
    assert email["role_description"] == "email field"
    assert email["html_role"] == "textbox"


def test_absent_source_metadata_stays_unknown_without_changing_existing_fields():
    base = (
        '<hierarchy><node class="android.widget.Button" text="Pay" '
        'resource-id="app:id/pay" clickable="true" bounds="[0,0][300,100]" />'
        '</hierarchy>'
    )
    enriched = base.replace(
        'bounds=',
        'focusable="true" window-id="9" actions="ACTION_FOCUS" bounds=',
    )
    old_keys = {
        "index", "role", "name", "visual_name", "bounds", "center", "states",
        "affordances", "scrollable", "scroll_axis", "interactive", "editable",
        "raw_child_count", "depth", "cls", "package", "resource_id",
        "content_desc", "text", "hint", "showing_hint", "position", "anchors",
        "query_matches",
    }

    plain = _tree.parse_tree(base, 1080, 2400)[0]
    with_metadata = _tree.parse_tree(enriched, 1080, 2400)[0]

    assert {key: plain[key] for key in old_keys} == {
        key: with_metadata[key] for key in old_keys}
    assert plain["focusable"] is None
    assert plain["window_id"] is None
    assert plain["accessibility_actions"] == []
    assert plain["semantic_traits"] == []
    assert with_metadata["focusable"] is True
    assert with_metadata["window_id"] == 9
    assert with_metadata["capabilities"] == ["activate", "focus"]


def test_negative_android_range_sentinels_are_not_published_as_values():
    xml = (
        '<hierarchy><node class="android.widget.EditText" hint="Search" '
        'max-text-length="-1" selection-start="-1" selection-end="-1" '
        'bounds="[0,0][300,100]" /></hierarchy>'
    )

    field = _tree.parse_tree(xml, 1080, 2400)[0]

    assert field["max_text_length"] is None
    assert field["selection_start"] is None
    assert field["selection_end"] is None
