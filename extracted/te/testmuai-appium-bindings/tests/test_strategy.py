"""Strategy compiler: per-platform data tables, loud on anything unknown."""
import json
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from testmu_appium._errors import UnknownStrategy, UnsupportedOnPlatform
from testmu_appium._helpers import _strategy


def test_accessibility_id_compiles_to_the_native_by():
    assert _strategy.compile_selector(
        {"strategy": "accessibility_id", "selector": "Compose"}, "android"
    ) == (AppiumBy.ACCESSIBILITY_ID, "Compose")


def test_view_id_compiles_to_a_resource_id_uiselector():
    by, value = _strategy.compile_selector(
        {"strategy": "view_id", "selector": "com.google.android.gm:id/compose"}, "android"
    )
    assert by == AppiumBy.ANDROID_UIAUTOMATOR
    assert value == 'new UiSelector().resourceId("com.google.android.gm:id/compose")'


def test_view_id_matches_an_id_carrying_no_package_prefix():
    """A Flutter or React Native view id is a bare developer string rather than an
    Android resource name. `resourceId` compares it verbatim, so both shapes compile
    the same way."""
    by, value = _strategy.compile_selector(
        {"strategy": "view_id", "selector": "proceed"}, "android"
    )
    assert by == AppiumBy.ANDROID_UIAUTOMATOR
    assert value == 'new UiSelector().resourceId("proceed")'


def test_view_id_values_are_escaped():
    _, value = _strategy.compile_selector(
        {"strategy": "view_id", "selector": 'odd"id\nhere'}, "android"
    )
    assert value == 'new UiSelector().resourceId("odd\\"id\\nhere")'


def test_view_id_and_view_id_text_render_the_same_resource_id_clause():
    _, simple = _strategy.compile_selector(
        {"strategy": "view_id", "selector": "com.app:id/row"}, "android"
    )
    _, compound = _strategy.compile_selector(
        {"strategy": "view_id_text", "selector": "com.app:id/row\nGo"}, "android"
    )
    assert simple == 'new UiSelector().resourceId("com.app:id/row")'
    assert compound.startswith('new UiSelector().resourceId("com.app:id/row")')


def test_text_compiles_to_a_uiselector():
    by, value = _strategy.compile_selector(
        {"strategy": "text", "selector": "Compose"}, "android"
    )
    assert by == AppiumBy.ANDROID_UIAUTOMATOR
    assert value == 'new UiSelector().text("Compose")'


def test_view_id_text_is_a_compound_uiselector():
    """The compound strategy owns its value encoding: "{view_id}\\n{text}"."""
    by, value = _strategy.compile_selector(
        {"strategy": "view_id_text",
         "selector": "com.google.android.gm:id/compose\nCompose"},
        "android",
    )
    assert by == AppiumBy.ANDROID_UIAUTOMATOR
    assert value == (
        'new UiSelector().resourceId("com.google.android.gm:id/compose").text("Compose")'
    )


def test_view_id_text_without_a_separator_degrades_to_resource_id_only():
    by, value = _strategy.compile_selector(
        {"strategy": "view_id_text", "selector": "com.app:id/only"}, "android"
    )
    assert by == AppiumBy.ANDROID_UIAUTOMATOR
    assert value == 'new UiSelector().resourceId("com.app:id/only")'


def test_uiselector_values_are_escaped():
    """A recorded label containing a quote or backslash must not break out of the
    UiSelector string literal."""
    _, value = _strategy.compile_selector(
        {"strategy": "text", "selector": 'He said "hi"\\'}, "android"
    )
    assert value == 'new UiSelector().text("He said \\"hi\\"\\\\")'


@pytest.mark.parametrize("raw,escaped", [
    ("Line one\nLine two", "Line one\\nLine two"),
    ("Windows\r\nnewline", "Windows\\r\\nnewline"),
    ("Name\tValue", "Name\\tValue"),
    ("bell\x07here", "bell\\u0007here"),
    ("null\x00byte", "null\\u0000byte"),
    ("vertical\x0btab", "vertical\\u000btab"),
    ("del\x7fchar", "del\\u007fchar"),
])
def test_control_characters_are_escaped_not_passed_through(raw, escaped):
    """A raw control character is not a literal character in a Java string, so an
    unescaped one produces a selector the device rejects outright — and that rejection
    escapes the strategy walk, which catches only staleness."""
    _, value = _strategy.compile_selector({"strategy": "text", "selector": raw}, "android")
    assert value == f'new UiSelector().text("{escaped}")'


def test_a_multiline_value_leaves_no_raw_control_character_in_the_query():
    _, value = _strategy.compile_selector(
        {"strategy": "text", "selector": "221B Baker Street\nLondon"}, "android"
    )
    assert not any(character <= "\x1f" for character in value)


def test_the_compound_strategy_escapes_both_halves():
    """The separator itself is a newline, so only the halves are escaped — a text half
    that contains its own newline must still not break the literal."""
    _, value = _strategy.compile_selector(
        {"strategy": "view_id_text", "selector": "com.app:id/row\nLine one\nLine two"},
        "android",
    )
    assert value == (
        'new UiSelector().resourceId("com.app:id/row").text("Line one\\nLine two")'
    )


def test_unknown_strategy_raises_with_the_known_set():
    with pytest.raises(UnknownStrategy) as exc:
        _strategy.compile_selector({"strategy": "ios_predicate", "selector": "x"}, "android")
    assert "ios_predicate" in str(exc.value)
    assert "accessibility_id" in str(exc.value)


def test_missing_strategy_raises():
    with pytest.raises(UnknownStrategy):
        _strategy.compile_selector({"selector": "#css-would-be-web"}, "android")


class TestIosStrategies:
    def test_accessibility_id_is_the_direct_form(self):
        by, value = _strategy.compile_selector(
            {"strategy": "accessibility_id", "selector": "Compose"}, "ios")
        assert by == AppiumBy.ACCESSIBILITY_ID
        assert value == "Compose"

    def test_text_compares_every_attribute_it_could_have_come_from(self):
        """iOS splits across label/value/name what Android keeps in `text`.

        The recorder does not preserve which one a label was read off, so a
        strategy that picked one would miss whenever it guessed wrong.
        """
        by, value = _strategy.compile_selector(
            {"strategy": "text", "selector": "Sign in"}, "ios")
        assert by == AppiumBy.IOS_PREDICATE
        assert value == 'label == "Sign in" OR name == "Sign in" OR value == "Sign in"'

    def test_text_escapes_a_quote_so_the_predicate_still_parses(self):
        """An unescaped quote ends the literal early — the driver rejects the whole
        query as malformed, which is a parse error rather than a miss."""
        _, value = _strategy.compile_selector(
            {"strategy": "text", "selector": 'say "hi"'}, "ios")
        assert r'label == "say \"hi\""' in value

    def test_predicate_and_class_chain_pass_through_as_written(self):
        """Both are strategies in their own right: a healed or hand-written
        selector legitimately arrives already expressed in one."""
        assert _strategy.compile_selector(
            {"strategy": "predicate", "selector": "type == 'XCUIElementTypeButton'"},
            "ios") == (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeButton'")
        assert _strategy.compile_selector(
            {"strategy": "class_chain", "selector": "**/XCUIElementTypeCell[1]"},
            "ios") == (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeCell[1]")

    def test_ios_has_no_view_id_row(self):
        """`name` IS the identifier when one was set and a copy of the label when
        not, so there is no second attribute for a `view_id` row to mean."""
        assert "view_id" not in _strategy.known_strategies("ios")
        assert "view_id_text" not in _strategy.known_strategies("ios")

    def test_an_android_strategy_raises_naming_the_ios_set(self):
        with pytest.raises(UnknownStrategy) as exc:
            _strategy.compile_selector(
                {"strategy": "view_id", "selector": "com.app:id/go"}, "ios")
        assert "accessibility_id" in str(exc.value)


def test_unknown_platform_raises():
    with pytest.raises(UnsupportedOnPlatform):
        _strategy.compile_selector(
            {"strategy": "accessibility_id", "selector": "x"}, "tizen"
        )


def test_known_strategies_reports_the_android_column():
    assert _strategy.known_strategies("android") == {
        "accessibility_id", "view_id", "view_id_text", "text", "child_text",
        "ancestor_of", "sibling_of", "attrs_xpath",
    }


class TestAttrsXpath:
    """The element's own attributes, compiled to XPath instead of a UiSelector.

    Same evidence `view_id` carries, searched differently. A UiSelector reads the
    ACTIVE window; a Compose or React Native dropdown, menu or dialog renders in
    a window of its own, so a page source spanning windows shows the element and
    every UiSelector form then fails to find it. XPath is evaluated over that same
    source, which makes it the only Android strategy able to reach one.
    """

    @staticmethod
    def _payload(**clauses):
        return json.dumps({"v": 1, "op": "attrs_xpath", "target": clauses},
                          separators=(",", ":"))

    def test_it_compiles_one_clause_to_an_xpath_over_the_page_source(self):
        by, value = _strategy.compile_selector(
            {"strategy": "attrs_xpath",
             "selector": self._payload(resource_id="shipping-state-option-13")},
            "android",
        )
        assert by == AppiumBy.XPATH
        assert value == "//*[normalize-space(@resource-id)='shipping-state-option-13']"

    def test_it_ands_every_recorded_clause(self):
        _, value = _strategy.compile_selector(
            {"strategy": "attrs_xpath",
             "selector": self._payload(resource_id="row", text="Illinois")},
            "android",
        )
        assert value == ("//*[normalize-space(@resource-id)='row'"
                         " and normalize-space(@text)='Illinois']")

    def test_it_escapes_a_value_carrying_a_quote(self):
        _, value = _strategy.compile_selector(
            {"strategy": "attrs_xpath", "selector": self._payload(text="it's here")},
            "android",
        )
        assert value == '//*[normalize-space(@text)="it\'s here"]'

    def test_it_refuses_a_payload_carrying_no_clause(self):
        """An empty predicate compiles to `//*[]`, which is not an XPath at all —
        and a `//*` without one would match the whole screen."""
        with pytest.raises(UnknownStrategy):
            _strategy.compile_selector(
                {"strategy": "attrs_xpath", "selector": self._payload()}, "android")

    def test_ios_has_no_row_for_it(self):
        """iOS names its own two query languages; it does not borrow this one."""
        with pytest.raises(UnknownStrategy):
            _strategy.compile_selector(
                {"strategy": "attrs_xpath",
                 "selector": self._payload(resource_id="x")}, "ios")


class TestChildText:
    """A clickable container labelled only by a descendant's text."""

    def test_it_matches_the_clickable_ancestor_of_the_text(self):
        by, value = _strategy.compile_selector(
            {"strategy": "child_text", "selector": "About phone"}, "android"
        )
        assert by == AppiumBy.ANDROID_UIAUTOMATOR
        assert value == (
            'new UiSelector().clickable(true)'
            '.childSelector(new UiSelector().text("About phone"))'
        )

    def test_the_child_text_is_escaped_inside_the_nested_selector(self):
        _, value = _strategy.compile_selector(
            {"strategy": "child_text", "selector": 'say "hi"\nnow'}, "android"
        )
        assert '.text("say \\"hi\\"\\nnow")' in value

    def test_ios_has_no_row_for_it(self):
        """child_text is a UiSelector shape with no iOS counterpart, and it is
        never emitted even on Android — so iOS raises UnknownStrategy naming what
        it does have, rather than pretending the platform is unfinished."""
        with pytest.raises(UnknownStrategy) as exc:
            _strategy.compile_selector(
                {"strategy": "child_text", "selector": "About phone"}, "ios"
            )
        assert "ancestor_of" in str(exc.value)


def test_order_by_score_is_descending_and_stable():
    selectors = [
        {"strategy": "text", "selector": "a", "score": 70},
        {"strategy": "view_id", "selector": "b", "score": 90},
        {"strategy": "accessibility_id", "selector": "c", "score": 90},
    ]
    assert [s["selector"] for s in _strategy.order_by_score(selectors)] == ["b", "c", "a"]


def test_order_by_score_defaults_missing_scores_to_zero():
    selectors = [{"strategy": "text", "selector": "a"},
                 {"strategy": "view_id", "selector": "b", "score": 10}]
    assert [s["selector"] for s in _strategy.order_by_score(selectors)] == ["b", "a"]


class TestDescriptorLookup:
    """compile_descriptor builds the post-heal strict lookup."""

    def test_prefers_resource_id_and_text(self):
        by, value = _strategy.compile_descriptor(
            {"resource_id": "com.app:id/x", "text": "Go", "content_desc": "",
             "cls": "android.widget.Button"},
            "android",
        )
        assert by == AppiumBy.ANDROID_UIAUTOMATOR
        assert value == 'new UiSelector().resourceId("com.app:id/x").text("Go")'

    def test_falls_back_to_content_desc(self):
        by, value = _strategy.compile_descriptor(
            {"resource_id": "", "text": "", "content_desc": "Compose",
             "cls": "android.widget.Button"},
            "android",
        )
        assert by == AppiumBy.ACCESSIBILITY_ID
        assert value == "Compose"

    def test_falls_back_to_class_and_text(self):
        by, value = _strategy.compile_descriptor(
            {"resource_id": "", "text": "Send", "content_desc": "",
             "cls": "android.widget.Button"},
            "android",
        )
        assert by == AppiumBy.ANDROID_UIAUTOMATOR
        assert value == 'new UiSelector().className("android.widget.Button").text("Send")'

    def test_class_only_descriptor_still_compiles(self):
        by, value = _strategy.compile_descriptor(
            {"resource_id": "", "text": "", "content_desc": "",
             "cls": "android.widget.ImageView"},
            "android",
        )
        assert by == AppiumBy.ANDROID_UIAUTOMATOR
        assert value == 'new UiSelector().className("android.widget.ImageView")'

    def test_empty_descriptor_raises(self):
        with pytest.raises(UnknownStrategy):
            _strategy.compile_descriptor(
                {"resource_id": "", "text": "", "content_desc": "", "cls": ""}, "android"
            )

    def test_ios_prefers_the_identifier_over_the_label(self):
        """`name` is the developer's own handle; `label` is user-visible text that
        localizes and gets reworded."""
        by, value = _strategy.compile_descriptor(
            {"content_desc": "compose_button", "name": "Compose"}, "ios")
        assert by == AppiumBy.ACCESSIBILITY_ID
        assert value == "compose_button"

    def test_ios_pairs_the_type_with_the_label_when_there_is_no_identifier(self):
        """A "Done" button and the "Done" text beside it share a label and are
        separated only by their type."""
        by, value = _strategy.compile_descriptor(
            {"content_desc": "", "name": "Done", "cls": "XCUIElementTypeButton"}, "ios")
        assert by == AppiumBy.IOS_PREDICATE
        assert value == 'type == "XCUIElementTypeButton" AND label == "Done"'

    def test_ios_falls_back_to_the_label_alone(self):
        by, value = _strategy.compile_descriptor({"name": "Done"}, "ios")
        assert by == AppiumBy.IOS_PREDICATE
        assert value == 'label == "Done"'

    def test_ios_descriptor_with_nothing_identifying_raises(self):
        with pytest.raises(UnknownStrategy):
            _strategy.compile_descriptor(
                {"name": "", "text": "", "content_desc": "", "cls": ""}, "ios")


class TestDisambiguateByCentre:
    """The descriptor retains bounds/centre from the SAME parse the server's
    dom_index refers to, so it can name which of several identical matches was meant.
    Everything ambiguous returns None: an almost-right row is a wrong tap.
    """

    #: A 1080x300 row whose centre sits at y=1050 — tolerance is half the box, so
    #: ±540 horizontally and ±150 vertically.
    DESCRIPTOR = {"bounds": (0, 900, 1080, 1200), "center": (540, 1050)}

    class _El:
        def __init__(self, top, height=300):
            self.rect = {"x": 0, "y": top, "width": 1080, "height": height}

    def test_the_row_at_the_recorded_centre_wins(self):
        rows = [self._El(300), self._El(600), self._El(900), self._El(1200)]
        assert _strategy.disambiguate_by_centre(rows, self.DESCRIPTOR) is rows[2]

    def test_a_row_that_scrolled_within_tolerance_still_wins(self):
        rows = [self._El(600), self._El(1000), self._El(1300)]
        assert _strategy.disambiguate_by_centre(rows, self.DESCRIPTOR) is rows[1]

    def test_nothing_within_tolerance_is_none(self):
        rows = [self._El(0), self._El(1800)]
        assert _strategy.disambiguate_by_centre(rows, self.DESCRIPTOR) is None

    def test_two_rows_within_tolerance_is_none(self):
        rows = [self._El(900), self._El(920)]
        assert _strategy.disambiguate_by_centre(rows, self.DESCRIPTOR) is None

    @pytest.mark.parametrize(
        "descriptor",
        [
            {},
            {"bounds": (0, 900, 1080, 1200)},
            {"center": (540, 1050)},
            {"bounds": (0, 900, 1080, 1200), "center": (540,)},
            {"bounds": (0, 900), "center": (540, 1050)},
            {"bounds": (0, 900, 0, 1200), "center": (540, 1050)},
            {"bounds": (0, 900, 1080, 900), "center": (540, 1050)},
        ],
        ids=["empty", "no-centre", "no-bounds", "short-centre", "short-bounds",
             "zero-width", "zero-height"],
    )
    def test_an_unusable_descriptor_is_none(self, descriptor):
        assert _strategy.disambiguate_by_centre([self._El(900)], descriptor) is None

    def test_the_british_spelling_is_accepted_too(self):
        rows = [self._El(600), self._El(900)]
        descriptor = {"bounds": (0, 900, 1080, 1200), "centre": (540, 1050)}
        assert _strategy.disambiguate_by_centre(rows, descriptor) is rows[1]

    def test_elements_with_unreadable_geometry_are_skipped(self):
        class _Stale:
            @property
            def rect(self):
                raise RuntimeError("stale")

        rows = [_Stale(), self._El(900)]
        assert _strategy.disambiguate_by_centre(rows, self.DESCRIPTOR) is rows[1]

    def test_an_empty_match_list_is_none(self):
        assert _strategy.disambiguate_by_centre([], self.DESCRIPTOR) is None


class TestAncestorOf:
    """A row with no attribute of its own, named by a label it contains.

    UiSelector cannot express this: childSelector returns the descendant it
    matched, and fromParent cannot return the parent it walked to. Only XPath's
    ancestor:: axis moves upward.
    """

    @staticmethod
    def _payload(clause, value):
        return json.dumps({"v": 1, "op": "ancestor_of",
                           "anchor": {"clause": clause, "value": value}},
                          separators=(",", ":"))

    def _compile(self, clause, value):
        return _strategy.compile_selector(
            {"strategy": "ancestor_of", "selector": self._payload(clause, value)},
            "android")

    def test_a_content_desc_anchor_matches_the_content_desc_attribute(self):
        by, query = self._compile("description", "KLJ Noida One")
        assert by == AppiumBy.XPATH
        assert query.startswith(
            "//*[normalize-space(@content-desc)='KLJ Noida One']/ancestor::*[")

    def test_a_text_anchor_matches_the_text_attribute(self):
        """The clause travels with the value: matching a content-desc label with
        @text resolves nothing, which is how child_text failed."""
        _, query = self._compile("text", "Basket")
        assert query.startswith("//*[normalize-space(@text)='Basket']/ancestor::*[")

    def test_only_the_nearest_interactive_ancestor_is_taken(self):
        """ancestor:: is a reverse axis, so [1] is the nearest match — a clickable
        row still wins over the scrollable list it sits in."""
        _, query = self._compile("text", "Basket")
        assert query.endswith("][1]")

    @pytest.mark.parametrize("attr", ["clickable", "long-clickable",
                                      "checkable", "scrollable"])
    def test_every_way_the_recorder_calls_an_element_interactive_is_reachable(self, attr):
        """A carousel is admitted by `scrollable` alone; a clickable-only predicate
        cannot name it, and 18 of 189 elements across captured screens are that shape."""
        _, query = self._compile("text", "Basket")
        assert f"@{attr}='true'" in query

    def test_transient_focus_is_not_treated_as_interactivity(self):
        """`focused` is which element has focus right now, not what it is."""
        _, query = self._compile("text", "Basket")
        assert "@focused" not in query

    def test_an_apostrophe_switches_the_quoting(self):
        _, query = self._compile("description", "Bob's Place")
        assert '"Bob\'s Place"' in query

    def test_both_quote_kinds_are_assembled_with_concat(self):
        """XPath 1.0 has no escape character, so a value carrying both quote
        kinds cannot be written as a single literal."""
        _, query = self._compile("text", "both \" and '")
        assert query.startswith("//*[normalize-space(@text)=concat(")

    def test_an_unknown_anchor_clause_raises_rather_than_guessing(self):
        with pytest.raises(UnknownStrategy):
            self._compile("hint", "Search")


class TestSiblingOf:
    """A grid card's button, named by the product title in another branch of the card.

    The button's view id is shared by every card and its label is shared by every
    card's button, so nothing it carries says WHICH one. The title does, and it is
    neither a descendant of the button nor a direct sibling of it.
    """

    ADD = {"resource_id": "com.shop:id/tv_title", "description": "ADD"}

    @staticmethod
    def _payload(clause, value, target):
        return json.dumps({"v": 1, "op": "sibling_of",
                           "anchor": {"clause": clause, "value": value},
                           "target": target},
                          separators=(",", ":"))

    def _compile(self, clause="description", value="Amul Taaza Toned Milk",
                 target=None):
        return _strategy.compile_selector(
            {"strategy": "sibling_of",
             "selector": self._payload(clause, value, self.ADD if target is None
                                       else target)},
            "android")

    def test_it_scopes_the_target_to_the_container_the_anchor_shares_with_it(self):
        by, query = self._compile()
        assert by == AppiumBy.XPATH
        target = ("normalize-space(@resource-id)='com.shop:id/tv_title' and "
                  "normalize-space(@content-desc)='ADD'")
        assert query == (
            "//*[normalize-space(@content-desc)='Amul Taaza Toned Milk']"
            f"/ancestor::*[.//*[{target}]][1]//*[{target}]"
        )

    def test_the_shared_container_is_the_nearest_one_holding_the_target(self):
        """ancestor:: is a reverse axis, so [1] on a predicate that requires a
        target-shaped descendant is the SMALLEST container the two share — the
        card, not the grid that holds every card."""
        _, query = self._compile()
        assert "/ancestor::*[.//*[" in query and "][1]//*[" in query

    def test_every_recorded_target_clause_narrows_the_match(self):
        """A card whose item is already in the basket shows a quantity readout
        under the same view id; only the label tells the two apart."""
        both = self._compile()[1]
        assert both.count("normalize-space(@content-desc)='ADD'") == 2

        only_id = self._compile(target={"resource_id": "com.shop:id/tv_title"})[1]
        assert "'ADD'" not in only_id
        assert only_id.count(
            "normalize-space(@resource-id)='com.shop:id/tv_title'") == 2

    def test_a_text_anchor_matches_the_text_attribute(self):
        _, query = self._compile(clause="text", value="Basket")
        assert query.startswith("//*[normalize-space(@text)='Basket']/ancestor::")

    def test_the_anchor_and_the_target_are_both_quoted_for_xpath(self):
        _, query = self._compile(value="Bob's Place",
                                 target={"text": "both \" and '"})
        assert '"Bob\'s Place"' in query
        assert "normalize-space(@text)=concat(" in query

    def test_a_target_with_no_clause_raises_rather_than_matching_everything(self):
        """An empty predicate would compile to `//*[...]//*[]` — every descendant
        of the card, which is a confident wrong answer rather than a miss."""
        with pytest.raises(UnknownStrategy):
            self._compile(target={})

    def test_an_unknown_target_clause_raises_rather_than_guessing(self):
        with pytest.raises(UnknownStrategy):
            self._compile(target={"hint": "Search"})

    def test_ios_compiles_the_same_shape_through_its_own_clauses(self):
        """The relation is platform-neutral; only the attribute names differ.

        iOS clauses are label/name/value — the vocabulary its parser publishes —
        so an Android payload's `resource_id` is not silently accepted here.
        """
        by, query = _strategy.compile_selector(
            {"strategy": "sibling_of",
             "selector": self._payload("label", "Amul Taaza Toned Milk",
                                       {"name": "add_button"})}, "ios")
        assert by == AppiumBy.XPATH
        target = "normalize-space(@name)='add_button'"
        assert query == (
            "//*[normalize-space(@label)='Amul Taaza Toned Milk']"
            f"/ancestor::*[.//*[{target}]][1]//*[{target}]")

    def test_ios_rejects_an_android_clause_rather_than_guessing(self):
        with pytest.raises(UnknownStrategy) as exc:
            _strategy.compile_selector(
                {"strategy": "sibling_of",
                 "selector": self._payload("resource_id", "x", {"name": "y"})}, "ios")
        assert "label" in str(exc.value)


class TestTheDescriptorKeepsItsCardinalityEvidence:
    """The producer measured the driver's answer (`query_matches`) — including
    nodes the parser admitted no row for, which is exactly where a duplicate
    identifier hides. Heal fires when layout shifted, which is when the
    geometry tiebreak is weakest, so measured ambiguity compiles the compound."""

    def test_a_measured_ambiguous_identifier_pins_the_type(self):
        by, value = _strategy.compile_descriptor({
            "content_desc": "Text", "cls": "XCUIElementTypeButton",
            "query_matches": {"content_desc": 2, "content_desc+cls": 1},
        }, "ios")
        assert by == AppiumBy.IOS_PREDICATE
        assert value == 'type == "XCUIElementTypeButton" AND name == "Text"'

    def test_a_measured_unique_identifier_stays_bare(self):
        by, value = _strategy.compile_descriptor({
            "content_desc": "compose_button", "cls": "XCUIElementTypeButton",
            "query_matches": {"content_desc": 1, "content_desc+cls": 1},
        }, "ios")
        assert by == AppiumBy.ACCESSIBILITY_ID
        assert value == "compose_button"

    def test_an_ambiguous_pair_is_left_to_geometry(self):
        """When even (type, name) matches twice, the compound buys nothing —
        the bare id keeps today's disambiguate-by-centre path."""
        by, _ = _strategy.compile_descriptor({
            "content_desc": "Pay", "cls": "XCUIElementTypeButton",
            "query_matches": {"content_desc": 2, "content_desc+cls": 2},
        }, "ios")
        assert by == AppiumBy.ACCESSIBILITY_ID

    def test_no_evidence_keeps_the_bare_identifier(self):
        """A descriptor from an older capture carries no counts; nothing is
        claimed, so nothing changes."""
        by, _ = _strategy.compile_descriptor(
            {"content_desc": "Text", "cls": "XCUIElementTypeButton"}, "ios")
        assert by == AppiumBy.ACCESSIBILITY_ID
