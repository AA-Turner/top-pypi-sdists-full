"""The perception API published for callers outside this package.

`testmu_appium.perception` is the supported import path for the UI-tree parser and
`_helpers/_tree.py` holds the vendored implementation. These pins fail when a public
name is dropped or renamed, when the two paths stop resolving to the same objects, or
when the entry shape or the 1-based index contract changes.
"""
import pytest

import testmu_appium
from testmu_appium import perception
from testmu_appium._helpers import _tree

#: The exact public surface. Dropping a name, renaming it, or exporting it from only
#: one of the two paths fails one of the pins below.
PUBLIC_NAMES = {
    "parse_tree", "format_for_prompt", "find_by_fingerprint", "position_hint",
    "ELEMENT_CONTRACT", "MAX_ANCHOR_CLIMB",
}

#: The package root retains the generated-test surface. The climb limit is a
#: perception concern consumed by the document serializer, not generated code.
ROOT_NAMES = PUBLIC_NAMES - {"MAX_ANCHOR_CLIMB"}

#: The web reader published alongside them. Kept apart because these come from
#: `_action_web`, not from the vendored tree copy the pins below are about.
WEB_NAMES = {"open_web_surface", "Surface", "release_web_surface"}
WEB_NAMES |= {"VisibleWebTarget", "probe_visible_web_target", "is_chrome_package"}
WEB_NAMES |= {"prepare_web_surface"}

#: Every key a parse_tree entry carries. Exact, not a subset: an added key is a
#: contract change for the consumers reading these dicts.
ENTRY_KEYS = {
    "index", "role", "name", "visual_name", "bounds", "center", "states",
    "affordances", "scrollable", "scroll_axis", "interactive", "editable", "depth", "cls",
    "raw_child_count",
    "package", "resource_id", "content_desc", "text", "hint", "showing_hint",
    "position", "anchors", "query_matches",
    "source_index", "source_path", "parent_index", "displayed", "clickable",
    "checkable", "checked", "enabled", "focusable", "focused", "long_clickable",
    "context_clickable", "selected", "dismissable", "accessibility_focused",
    "a11y_important", "screen_reader_focusable", "input_type", "input_kind",
    "multiline", "max_text_length", "selection_start", "selection_end",
    "content_invalid", "error_text", "pane_title", "tooltip_text", "heading",
    "text_entry_key", "text_has_clickable_span", "live_region", "window_id",
    "drawing_order", "accessibility_actions", "capabilities", "semantic_traits",
    "role_description", "html_role",
}

SCREEN_W, SCREEN_H = 1080, 2340

#: Interactive controls, informational rows, and a structural wrapper that is
#: promoted rather than emitted.
FIXTURE = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node class="android.widget.FrameLayout" bounds="[0,0][1080,2340]">
    <node class="android.widget.Button" resource-id="com.app:id/go" text="Go"
          content-desc="" clickable="true" enabled="true" bounds="[40,100][440,220]" />
    <node class="android.widget.EditText" resource-id="com.app:id/query" text=""
          content-desc="" hint="Search" enabled="true" bounds="[40,300][1040,420]" />
    <node class="android.widget.TextView" text="Order total"
          bounds="[40,500][1040,620]" />
    <node class="android.widget.FrameLayout" resource-id="com.app:id/card"
          bounds="[40,700][1040,900]" />
  </node>
</hierarchy>
"""


@pytest.fixture
def entries():
    return perception.parse_tree(FIXTURE, SCREEN_W, SCREEN_H)


class TestPublishedNames:
    """The four names resolve, from both paths, to the vendored implementations."""

    def test_the_module_exports_exactly_the_public_surface(self):
        assert set(perception.__all__) == PUBLIC_NAMES | WEB_NAMES

    @pytest.mark.parametrize("name", sorted(PUBLIC_NAMES))
    def test_the_name_resolves_on_the_perception_module(self, name):
        assert getattr(perception, name) is not None

    @pytest.mark.parametrize("name", sorted(ROOT_NAMES))
    def test_the_package_root_re_exports_the_same_object(self, name):
        assert name in testmu_appium.__all__
        assert getattr(testmu_appium, name) is getattr(perception, name)

    @pytest.mark.parametrize(
        "name", sorted(PUBLIC_NAMES - {"parse_tree", "ELEMENT_CONTRACT"})
    )
    def test_the_public_helper_is_the_android_implementation(self, name):
        assert getattr(perception, name) is getattr(_tree, name)

    def test_parse_tree_is_the_platform_selecting_facade(self):
        assert perception.parse_tree is not _tree.parse_tree
        assert perception.ELEMENT_CONTRACT is _tree.ELEMENT_CONTRACT

    def test_a_bare_parse_tree_call_follows_the_configured_platform(self, monkeypatch):
        """`configure(platform="ios")` then `parse_tree(xml, w, h)` must select
        the iOS producer — a hardwired android default here re-reads every
        configured session's document with the wrong parser."""
        from testmu_appium import _config

        monkeypatch.setitem(_config._config, "platform", "ios")
        ios_xml = (
            '<AppiumAUT><XCUIElementTypeApplication type="XCUIElementTypeApplication"'
            ' name="Demo" enabled="true" visible="true" accessible="false"'
            ' x="0" y="0" width="414" height="896">'
            '<XCUIElementTypeButton type="XCUIElementTypeButton" name="Go"'
            ' label="Go" enabled="true" visible="true" accessible="true"'
            ' x="10" y="10" width="100" height="44"/>'
            "</XCUIElementTypeApplication></AppiumAUT>"
        )
        rows = perception.parse_tree(ios_xml, 414, 896)
        assert [row["name"] for row in rows] == ["Go"]

    def test_an_explicit_platform_still_wins_over_the_configured_one(self, monkeypatch):
        from testmu_appium import _config

        monkeypatch.setitem(_config._config, "platform", "ios")
        rows = perception.parse_tree(
            "<hierarchy rotation='0'/>", 1080, 2340, platform="android"
        )
        assert rows == []


class TestWebNames:
    """The web reader is published from the same module, and is not the tree's."""

    @pytest.mark.parametrize("name", sorted(WEB_NAMES))
    def test_the_name_resolves_on_the_perception_module(self, name):
        assert getattr(perception, name) is not None

    @pytest.mark.parametrize("name", sorted(WEB_NAMES))
    def test_the_web_reader_is_not_taken_from_the_vendored_tree(self, name):
        assert not hasattr(_tree, name)


class TestEntryShape:
    """parse_tree returns the entry dict third-party callers read."""

    def test_label_id_or_touch_nodes_become_entries(self, entries):
        assert [e["role"] for e in entries] == [
            "button", "input", "text", "group"]
        assert [e["interactive"] for e in entries] == [
            True, True, False, False]

    @pytest.mark.parametrize("position", range(4))
    def test_every_entry_carries_exactly_the_documented_keys(self, entries, position):
        assert set(entries[position]) == ENTRY_KEYS
        assert set(entries[position]) == set(perception.ELEMENT_CONTRACT)
        for field, spec in perception.ELEMENT_CONTRACT.items():
            assert isinstance(entries[position][field], spec.value_type), field
            assert spec.meaning

    def test_indices_are_one_based_and_contiguous(self, entries):
        assert [e["index"] for e in entries] == list(range(1, len(entries) + 1))

    def test_bounds_and_center_are_device_pixel_tuples(self, entries):
        assert entries[0]["bounds"] == (40, 100, 440, 220)
        assert entries[0]["center"] == (240, 160)

    def test_a_label_falls_back_to_the_hint(self, entries):
        assert entries[0]["name"] == "Go"
        assert entries[1]["name"] == "Search"

    def test_raw_attributes_are_carried_through(self, entries):
        assert entries[0]["resource_id"] == "com.app:id/go"
        assert entries[0]["cls"] == "android.widget.Button"
        assert entries[1]["hint"] == "Search"
        assert entries[0]["scroll_axis"] is None
        assert entries[0]["raw_child_count"] == 0

    def test_the_position_hint_is_row_dash_column(self, entries):
        assert entries[0]["position"] == "top-left"

    def test_scroll_axis_is_owned_by_the_binding_tree(self):
        xml = """<hierarchy>
          <node class="android.widget.HorizontalScrollView" scrollable="true"
                bounds="[0,0][1080,200]" />
          <node class="androidx.recyclerview.widget.RecyclerView" scrollable="true"
                bounds="[0,300][1080,2200]">
            <node bounds="[0,300][1080,700]" />
            <node bounds="[0,700][1080,1100]" />
          </node>
          <node class="android.view.View" scrollable="true"
                bounds="[0,2200][1080,2340]" />
        </hierarchy>"""
        parsed = perception.parse_tree(xml, SCREEN_W, SCREEN_H)
        assert [entry["scroll_axis"] for entry in parsed] == [
            "horizontal", "vertical", None]
        assert [entry["raw_child_count"] for entry in parsed] == [0, 2, 0]


class TestPublishedHelpers:
    def test_format_for_prompt_renders_one_line_per_entry(self, entries):
        lines = perception.format_for_prompt(entries).splitlines()
        assert len(lines) == 2
        assert lines[0].startswith("[1] button")
        assert lines[1].startswith("[2] input")

    def test_find_by_fingerprint_re_finds_by_resource_id(self, entries):
        found = perception.find_by_fingerprint(entries, {"resource_id": "com.app:id/go"})
        assert found is entries[0]

    def test_find_by_fingerprint_returns_none_for_an_absent_element(self, entries):
        assert perception.find_by_fingerprint(entries, {"resource_id": "nope"}) is None

    def test_web_fingerprint_is_strict_about_frame_identity(self):
        base = {
            "surface": "web", "css": "#pay", "name": "Pay",
            "resource_id": "", "content_desc": "", "text": "",
        }
        top = {
            **base, "frame_path": "", "center": (50, 20),
            "bounds": (0, 0, 100, 40),
        }
        framed = {
            **base, "frame_path": ">f0", "center": (50, 120),
            "bounds": (0, 100, 100, 140),
        }
        fingerprint = {
            "surface": "web", "css": "#pay", "name": "Pay",
            "frame_path": ">f0", "cx": 50, "cy": 120,
            "bounds": [0, 100, 100, 140],
        }
        assert perception.find_by_fingerprint([top, framed], fingerprint) is framed
        assert perception.find_by_fingerprint([top], fingerprint) is None

    def test_editability_is_a_neutral_boolean(self, entries):
        assert [entry["editable"] for entry in entries] == [False, True, False, False]


class TestTheChromePackageRule:
    """One owner for "is this Chrome", so consumers cannot drift apart.

    v16's collapsed-projection classifier and this binding's visibility probe
    both gate on it; a second copy would diverge silently, and the failure mode
    is a candidate the probe then refuses as an unsupported package.
    """

    @pytest.mark.parametrize("package", sorted({
        "com.android.chrome", "com.chrome.beta",
        "com.chrome.dev", "com.chrome.canary",
    }))
    def test_every_chrome_channel_is_recognised(self, package):
        assert perception.is_chrome_package(package) is True

    @pytest.mark.parametrize("package", [
        "", "com.google.android.gm", "org.mozilla.firefox",
        "com.android.chrome.evil", "com.lambdatest.kanedragdrop",
    ])
    def test_anything_else_is_not(self, package):
        assert perception.is_chrome_package(package) is False
