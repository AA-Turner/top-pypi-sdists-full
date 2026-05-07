"""
Tests for forms in AFAT
"""

# Standard Library
from unittest.mock import patch

# Alliance Auth AFAT
from afat.forms import (
    AFatClickFatForm,
    AFatEsiFatForm,
    AFatManualFatForm,
    DoctrineAdminForm,
    FatLinkEditForm,
    FleetSnapshot,
    SettingAdminForm,
    get_mandatory_form_label_text,
    sanitize_cleaned_data,
)
from afat.models import Doctrine
from afat.tests import BaseTestCase


class TestGetMandatoryFormLabelText(BaseTestCase):
    """
    Test get_mandatory_form_label_text function
    """

    def test_returns_safe_string_with_asterisk_for_plain_text(self):
        """
        Test that the function returns a SafeString with the correct asterisk for plain text.

        :return:
        :rtype:
        """

        label = "Field Label"
        result = get_mandatory_form_label_text(label)

        self.assertIn(label, result)
        self.assertIn(
            '<span aria-label="This field is mandatory" class="form-required-marker">*</span>',
            result,
        )


class TestSanitizeCleanedData(BaseTestCase):
    """
    Test sanitize_cleaned_data function
    """

    def test_return_none_when_input_is_none(self):
        """
        Test return none when input is None.

        :return:
        :rtype:
        """

        self.assertIsNone(sanitize_cleaned_data(None))

    def test_return_empty_dict_when_input_is_empty(self):
        """
        Test return empty dict when input is empty.

        :return:
        :rtype:
        """

        inp = {}

        self.assertEqual(sanitize_cleaned_data(inp), {})

    def test_non_string_values_are_untouched(self):
        """
        Test non string values are untouched.

        :return:
        :rtype:
        """

        original = {"num": 1, "lst": [1, 2], "map": {"a": "b"}, "none": None}

        self.assertEqual(sanitize_cleaned_data(original.copy()), original)

    def test_strips_simple_html_tags_from_strings(self):
        """
        Test strips simple HTML tags from strings.

        :return:
        :rtype:
        """

        inp = {"field": "<div>Hello <span>World</span></div>"}
        out = sanitize_cleaned_data(inp)

        self.assertEqual(out["field"], "Hello World")

    def test_removes_control_characters_but_keeps_linefeeds(self):
        """
        Test removes control characters and keeps linefeeds.

        :return:
        :rtype:
        """

        inp = {"text": "A\x00B\x07C\x0bD\tE\nF\x0cG\x7fH"}
        out = sanitize_cleaned_data(inp)

        self.assertNotIn("\x00", out["text"])
        self.assertNotIn("\x07", out["text"])
        self.assertNotIn("\x0b", out["text"])
        self.assertNotIn("\x0c", out["text"])
        self.assertNotIn("\x7f", out["text"])
        self.assertNotIn("\t", out["text"])
        self.assertIn("\n", out["text"])

    def test_normalizes_crlf_and_cr_to_lf_and_preserves_line_structure(self):
        """
        Test normalizes CRLF and CR to LF and preserves line structure.

        :return:
        :rtype:
        """

        inp = {"lines": "one\r\ntwo\rthree\nfour"}
        out = sanitize_cleaned_data(inp)

        self.assertNotIn("\r", out["lines"])
        self.assertEqual(out["lines"].split("\n"), ["one", "two", "three", "four"])

    def test_collapses_spaces_and_tabs_within_each_line_and_trims(self):
        """
        Test collapses spaces and tabs within each line and trims.

        :return:
        :rtype:
        """

        inp = {"p": "  lead  spaces\tand   multiple\t\tspaces  \n  second   line "}
        out = sanitize_cleaned_data(inp)

        self.assertEqual(out["p"], "lead spaces and multiple spaces\nsecond line")

    def test_mixed_fields_only_string_fields_are_sanitized(self):
        """
        Test mixed fields only string fields are sanitized.

        :return:
        :rtype:
        """

        inp = {"a": "<b>hi</b>", "b": 0, "c": "  spaced \n <i>tag</i>two  "}
        out = sanitize_cleaned_data(inp.copy())

        self.assertEqual(out["a"], "hi")
        self.assertEqual(out["b"], 0)
        self.assertEqual(out["c"], "spaced\ntagtwo")

    def test_preserves_unicode_and_emojis(self):
        """
        Test preserve unicode and emojis in sanitize_cleaned_data.

        :return:
        :rtype:
        """

        raw = "<span>Emoji 👍\n\tand    multiple   spaces</span>"
        cleaned_data = {"val": raw}

        result = sanitize_cleaned_data(cleaned_data)

        self.assertEqual(result["val"], "Emoji 👍\nand multiple spaces")

    def test_collapses_spaces_and_tabs_when_keep_tabs_false(self):
        """
        Test collapses spaces and tabs when keep_tabs is false.

        :return:
        :rtype:
        """

        data = {"field": "  a\t\tb   c \t d  "}
        result = sanitize_cleaned_data(data.copy(), keep_tabs=False)

        # leading/trailing whitespace trimmed and internal sequences of spaces/tabs collapsed
        self.assertEqual(result["field"], "a b c d")

    def test_preserves_tabs_when_keep_tabs_true_and_collapses_multiple_spaces(self):
        """
        Test preserves tabs when keep_tabs is True and collapses multiple spaces.

        :return:
        :rtype:
        """

        data = {"field": "\t\tA  B\tC  "}
        result = sanitize_cleaned_data(data.copy(), keep_tabs=True)

        # consecutive spaces collapsed to one, tabs preserved, trailing spaces removed but not tabs
        self.assertEqual(result["field"], "A B\tC")

    def test_removes_html_and_control_chars_and_normalizes_newlines(self):
        """
        Test removes html and control chars and normalizes newlines.

        :return:
        :rtype:
        """

        raw = "Hello\r\n<b>World</b>\x00\x1f!"
        data = {"field": raw}
        result = sanitize_cleaned_data(data.copy(), keep_tabs=False)

        # HTML tags removed, control chars removed, CRLF normalized to LF
        self.assertEqual(result["field"], "Hello\nWorld!")


class TestAFatEsiFatForm(BaseTestCase):
    """
    Test AFatEsiFatForm
    """

    def test_sanitizes_name_esi_removes_html_and_collapses_spaces(self):
        """
        Test sanitizes name_esi by removing HTML tags and collapsing spaces.

        :return:
        :rtype:
        """

        form = AFatEsiFatForm(data={"name_esi": "  <b>Emoji 👍</b>   and   spaces  "})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name_esi"], "Emoji 👍 and spaces")

    def test_sanitizes_optional_fields_control_chars_tabs_and_linebreaks_are_normalized(
        self,
    ):
        """
        Test sanitizes optional fields by removing control characters, normalizing tabs and line breaks, and collapsing spaces.

        :return:
        :rtype:
        """

        raw_type = "Line1\t\t Line2\rLine3\x01"
        raw_doctrine = "<b>Doc</b>\r\n\tSub\tSection"

        form = AFatEsiFatForm(
            data={"name_esi": "X", "type_esi": raw_type, "doctrine_esi": raw_doctrine}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["type_esi"], "Line1 Line2\nLine3")
        self.assertEqual(form.cleaned_data["doctrine_esi"], "Doc\nSub Section")
        self.assertNotIn("\x01", form.cleaned_data["type_esi"])
        self.assertNotIn("\t", form.cleaned_data["doctrine_esi"])

    def test_missing_optional_fields_still_valid_and_name_is_sanitized(self):
        """
        Test missing optional fields still valid and name are sanitized.

        :return:
        :rtype:
        """

        form = AFatEsiFatForm(data={"name_esi": "  Fleet <i>Name</i>  "})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name_esi"], "Fleet Name")
        # Optional fields may be absent or empty but form remains valid
        self.assertIn("name_esi", form.cleaned_data)

    def test_name_esi_required_validation_fails_when_empty(self):
        """
        Test name_esi required validation fails when empty.

        :return:
        :rtype:
        """

        form = AFatEsiFatForm(data={"name_esi": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("name_esi", form.errors)

    def test_all_fields_preserve_unicode_and_emoji_characters(self):
        """
        Test all fields preserve unicode and emoji characters.

        :return:
        :rtype:
        """

        form = AFatEsiFatForm(
            data={
                "name_esi": "Emoji 👍  ",
                "type_esi": "Type 😊\t\t",
                "doctrine_esi": "Doc 😃\r\nLine",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name_esi"], "Emoji 👍")
        self.assertEqual(form.cleaned_data["type_esi"], "Type 😊")
        self.assertEqual(form.cleaned_data["doctrine_esi"], "Doc 😃\nLine")


class TestAFatManualFatForm(BaseTestCase):
    """
    Test AFatManualFatForm
    """

    def test_sanitizes_all_fields_and_preserves_linebreaks(self):
        """
        Test sanitizes all fields and preserve linebreaks.

        :return:
        :rtype:
        """

        form = AFatManualFatForm(
            data={
                "character": "  <b>Captain</b>  ",
                "system": "System\tName\r\nSub\tSection  ",
                "shiptype": "Ship\x01Type   ",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["character"], "Captain")
        self.assertEqual(form.cleaned_data["system"], "System Name\nSub Section")
        self.assertEqual(form.cleaned_data["shiptype"], "ShipType")

    def test_required_validation_fails_for_blank_or_whitespace_only_fields(self):
        """
        Test required fields validation fails when blank or whitespace only fields.

        :return:
        :rtype:
        """

        form = AFatManualFatForm(
            data={"character": "   ", "system": "", "shiptype": " \t "}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("character", form.errors)
        self.assertIn("system", form.errors)
        self.assertIn("shiptype", form.errors)

    def test_field_length_validation_fails_when_values_exceed_max_lengths(self):
        """
        Test field length validation fails when values exceed maximum length.

        :return:
        :rtype:
        """

        long_char = "c" * 256  # character max_length = 255
        long_system = "s" * 101  # system max_length = 100
        long_ship = "t" * 101  # shiptype max_length = 100

        form = AFatManualFatForm(
            data={"character": long_char, "system": long_system, "shiptype": long_ship}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("character", form.errors)
        self.assertIn("system", form.errors)
        self.assertIn("shiptype", form.errors)

    def test_control_characters_removed_tabs_converted_and_cr_normalized(self):
        """
        Test control characters removed tabs converted and cr normalized.

        :return:
        :rtype:
        """

        raw_character = "Name\x02\x03\r\nSecond  Line\t\t"
        raw_system = "\x01Sys\tPart\rThird"
        raw_ship = "Sh\x07ip\tType"

        form = AFatManualFatForm(
            data={
                "character": raw_character,
                "system": raw_system,
                "shiptype": raw_ship,
            }
        )

        self.assertTrue(form.is_valid())
        # control chars removed, CR normalized to LF, tabs collapsed to single spaces, leading/trailing trimmed
        self.assertEqual(form.cleaned_data["character"], "Name\nSecond Line")
        self.assertEqual(form.cleaned_data["system"], "Sys Part\nThird")
        self.assertEqual(form.cleaned_data["shiptype"], "Ship Type")


class TestAFatClickFatForm(BaseTestCase):
    """
    Test AFatClickFatForm
    """

    def test_sets_duration_initial_from_setting_on_init(self):
        """
        Test sets duration initial from setting.

        :return:
        :rtype:
        """

        with patch("afat.forms.Setting.get_setting", return_value=45):
            form = AFatClickFatForm()

            self.assertEqual(form.fields["duration"].initial, 45)

    def test_validates_and_sanitizes_input_and_accepts_valid_duration(self):
        """
        Test validates and sanitizes input and accept valid duration.

        :return:
        :rtype:
        """

        with patch("afat.forms.Setting.get_setting", return_value=30):
            form = AFatClickFatForm(
                data={
                    "name": "  <b>Fleet</b>  ",
                    "type": "Type\t\tA  ",
                    "doctrine": "Doc\r\nLine\tSub",
                    "duration": "5",
                }
            )

            self.assertTrue(form.is_valid())
            self.assertEqual(form.cleaned_data["name"], "Fleet")
            self.assertEqual(form.cleaned_data["type"], "Type A")
            self.assertEqual(form.cleaned_data["doctrine"], "Doc\nLine Sub")
            self.assertEqual(form.cleaned_data["duration"], 5)

    def test_invalid_duration_below_minimum_shows_error(self):
        """
        Test invalid duration below minimum shows error.

        :return:
        :rtype:
        """

        with patch("afat.forms.Setting.get_setting", return_value=10):
            form = AFatClickFatForm(data={"name": "X", "duration": "0"})

            self.assertFalse(form.is_valid())
            self.assertIn("duration", form.errors)

    def test_name_required_validation_fails_when_blank_or_whitespace_only(self):
        """
        Test name required validation fails when blank or whitespace only

        :return:
        :rtype:
        """

        with patch("afat.forms.Setting.get_setting", return_value=10):
            form = AFatClickFatForm(data={"name": "   ", "duration": "15"})

            self.assertFalse(form.is_valid())
            self.assertIn("name", form.errors)

    def test_preserves_unicode_and_emojis_in_text_fields_while_sanitizing_whitespace(
        self,
    ):
        """
        Test preserve unicode and emojis in text fields while sanitizing whitespace.

        :return:
        :rtype:
        """

        with patch("afat.forms.Setting.get_setting", return_value=20):
            form = AFatClickFatForm(
                data={
                    "name": "Emoji 👍  ",
                    "type": "Type 😊\t\tMore",
                    "doctrine": "Doc 😃\r\nLine  ",
                    "duration": "12",
                }
            )

            self.assertTrue(form.is_valid())
            self.assertEqual(form.cleaned_data["name"], "Emoji 👍")
            self.assertEqual(form.cleaned_data["type"], "Type 😊 More")
            self.assertEqual(form.cleaned_data["doctrine"], "Doc 😃\nLine")


class TestFatLinkEditForm(BaseTestCase):
    """
    Test FatLinkEditForm
    """

    def test_sanitizes_fleet_field_removes_html_and_trims_whitespace(self):
        """
        Test sanitizes fleet field remove html and trims whitespace.

        :return:
        :rtype:
        """

        form = FatLinkEditForm(data={"fleet": "  <b> Fleet Name </b>  "})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["fleet"], "Fleet Name")

    def test_required_validation_fails_for_blank_or_whitespace_only(self):
        """
        Test required validation fails for  blank or whitespace only.

        :return:
        :rtype:
        """

        form = FatLinkEditForm(data={"fleet": "   "})

        self.assertFalse(form.is_valid())
        self.assertIn("fleet", form.errors)

    def test_preserves_unicode_and_emojis_and_collapses_tabs(self):
        """
        Test preserve unicode and emojis and collapses tabs.

        :return:
        :rtype:
        """

        form = FatLinkEditForm(data={"fleet": "Emoji 👍\t\t more  "})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["fleet"], "Emoji 👍 more")

    def test_removes_control_characters_and_normalizes_crlf_to_lf(self):
        """
        Test remove control characters and normalizes crlf to lf.

        :return:
        :rtype:
        """

        raw = "Name\x01\r\nSecond\t\tLine\x02"

        form = FatLinkEditForm(data={"fleet": raw})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["fleet"], "Name\nSecond Line")

    def test_enforces_max_length_for_fleet_field(self):
        """
        Test enforces max length for  fleet field.

        :return:
        :rtype:
        """

        long_value = "x" * 256  # max_length is 255

        form = FatLinkEditForm(data={"fleet": long_value})

        self.assertFalse(form.is_valid())
        self.assertIn("fleet", form.errors)


class TestSettingAdminForm(BaseTestCase):
    """
    Test SettingAdminForm
    """

    def test_delegates_sanitization_and_uses_sanitized_cleaned_data(self):
        """
        Test delegates sanitization and uses sanitized cleaned data.

        :return:
        :rtype:
        """

        with patch(
            "afat.forms.sanitize_cleaned_data",
            return_value={"default_fatlink_expiry_time": 99},
        ) as mock_sanitize:
            form = SettingAdminForm(
                data={
                    "default_fatlink_expiry_time": "30",
                    "default_fatlink_reopen_duration": "60",
                    "default_fatlink_reopen_grace_time": "15",
                    "default_log_duration": "10",
                    "use_doctrines_from_fittings_module": "on",
                }
            )
            form.full_clean()

            mock_sanitize.assert_called_once()
            # Ensure the form used the sanitized result
            self.assertEqual(form.cleaned_data.get("default_fatlink_expiry_time"), 99)

    def test_numeric_and_boolean_fields_are_parsed_and_preserved_after_clean(self):
        """
        Test numeric and boolean fields are parsed and preserved after clean.

        :return:
        :rtype:
        """

        form = SettingAdminForm(
            data={
                "default_fatlink_expiry_time": "45",
                "default_fatlink_reopen_duration": "30",
                "default_fatlink_reopen_grace_time": "20",
                "default_log_duration": "7",
                "use_doctrines_from_fittings_module": "on",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertIsInstance(form.cleaned_data["default_fatlink_expiry_time"], int)
        self.assertEqual(form.cleaned_data["default_fatlink_expiry_time"], 45)
        self.assertIsInstance(
            form.cleaned_data["use_doctrines_from_fittings_module"], bool
        )
        self.assertTrue(form.cleaned_data["use_doctrines_from_fittings_module"])

    def test_invalid_numeric_input_produces_validation_error(self):
        """
        Test invalid numeric input produces validation error.

        :return:
        :rtype:
        """
        form = SettingAdminForm(
            data={
                "default_fatlink_expiry_time": "not-a-number",
                "default_fatlink_reopen_duration": "30",
                "default_fatlink_reopen_grace_time": "20",
                "default_log_duration": "7",
                "use_doctrines_from_fittings_module": "on",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("default_fatlink_expiry_time", form.errors)

    def test_clean_handles_no_changes_and_returns_cleaned_data_structure(self):
        """
        Test clean handles no changes and return cleaned data structure.

        :return:
        :rtype:
        """

        form = SettingAdminForm(
            data={
                "default_fatlink_expiry_time": "60",
                "default_fatlink_reopen_duration": "60",
                "default_fatlink_reopen_grace_time": "60",
                "default_log_duration": "60",
                "use_doctrines_from_fittings_module": "",
            }
        )

        # Should be valid and cleaned_data should be a dict containing expected keys
        self.assertTrue(form.is_valid())
        keys = {
            "default_fatlink_expiry_time",
            "default_fatlink_reopen_duration",
            "default_fatlink_reopen_grace_time",
            "default_log_duration",
            "use_doctrines_from_fittings_module",
        }
        self.assertTrue(keys.issubset(set(form.cleaned_data.keys())))


class TestDoctrineAdminForm(BaseTestCase):
    """
    Tests for the Doctrine admin form.
    """

    def test_sanitizes_name_and_notes_removes_html_control_characters_and_normalizes_linebreaks(
        self,
    ):
        """
        Test sanitizes name and notes removes HTML control characters and normalizes linebreaks.

        :return:
        :rtype:
        """

        form = DoctrineAdminForm(
            data={
                "name": "  <b>Alpha</b>  ",
                "notes": "First\x01Line\r\n\tSecond\t\tLine\x02",
                "is_enabled": "on",
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Alpha")
        self.assertEqual(form.cleaned_data["notes"], "FirstLine\nSecond Line")
        self.assertTrue(form.cleaned_data["is_enabled"])

    def test_parses_boolean_field_off_and_allows_empty_notes(self):
        """
        Test parses boolean field off and allows empty notes.

        :return:
        :rtype:
        """

        form = DoctrineAdminForm(
            data={"name": "DocEmptyNotes", "notes": "", "is_enabled": ""}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["notes"], "")
        self.assertFalse(form.cleaned_data["is_enabled"])

    def test_duplicate_name_violates_unique_constraint_and_reports_error(self):
        """
        Test duplicate name violates unique constraint.

        :return:
        :rtype:
        """

        Doctrine.objects.create(name="UniqueDoctrine", notes="x", is_enabled=True)
        form = DoctrineAdminForm(
            data={"name": "UniqueDoctrine", "notes": "x", "is_enabled": "on"}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_preserves_unicode_and_emojis_while_collapsing_whitespace(self):
        """
        Test preserve unicode and emojis while collapsing whitespace.

        :return:
        :rtype:
        """

        form = DoctrineAdminForm(
            data={
                "name": "EmojiName   ",
                "notes": "Note 😊\t\tmore  \r\nend",
                "is_enabled": "on",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "EmojiName")
        self.assertEqual(form.cleaned_data["notes"], "Note 😊 more\nend")


class TestFleetSnapshotForm(BaseTestCase):
    """
    Tests for the Fleet Snapshot form.
    """

    def test_keeps_tabs_and_collapses_multiple_spaces_per_line(self):
        """
        Test keeps tabs and collapses multiple spaces per line.

        :return:
        :rtype:
        """

        raw = "\tRounon Dax\t\tDO6H-Q\tMetamorphosis\tFrigate\tFleet       Commander (Boss)\t5 - 5 - 5\t\t"
        form = FleetSnapshot(data={"fleet_composition": raw})

        self.assertTrue(form.is_valid())

        cleaned = form.cleaned_data["fleet_composition"]
        expected = "Rounon Dax\t\tDO6H-Q\tMetamorphosis\tFrigate\tFleet Commander (Boss)\t5 - 5 - 5"

        self.assertEqual(cleaned, expected)

    def test_init_handles_copy_exception_and_sanitizes_data(self):
        """
        Ensure FleetSnapshot.__init__ handles exceptions from data.copy() by
        falling back to dict(data) and still sanitizing the fleet_composition field.

        :return:
        :rtype:
        """

        class BrokenCopyMapping:
            """
            Broken Copy Mapping.
            """

            def __init__(self, d):
                """
                Initialize BrokenCopyMapping.

                :param d:
                :type d:
                """

                self._d = dict(d)

            def __contains__(self, key):
                """
                Check if key is in self._d.

                :param key:
                :type key:
                :return:
                :rtype:
                """

                return key in self._d

            def copy(self):
                """
                Copy Mapping.

                :return:
                :rtype:
                """

                raise Exception("copy failed")

            def __iter__(self):
                """
                Iterate Mapping.

                :return:
                :rtype:
                """

                return iter(self._d)

            def __getitem__(self, key):
                """
                Get Mapping.

                :param key:
                :type key:
                :return:
                :rtype:
                """

                return self._d[key]

            def items(self):
                """
                Get Mapping Items.
                :return:
                :rtype:
                """

                return self._d.items()

            def keys(self):
                """
                Get Mapping Keys.

                :return:
                :rtype:
                """

                # Provide mapping protocol so dict(self) works in fallback
                return self._d.keys()

            def get(self, key, default=None):
                """
                Get Mapping Key.

                :param key:
                :type key:
                :param default:
                :type default:
                :return:
                :rtype:
                """

                return self._d.get(key, default)

        raw = "\tRounon Dax\t\tDO6H-Q\tMetamorphosis\tFrigate\tFleet       Commander (Boss)\t5 - 5 - 5\t\t"

        broken = BrokenCopyMapping({"fleet_composition": raw})

        # Should not raise despite copy() raising internally
        form = FleetSnapshot(data=broken)

        self.assertTrue(form.is_valid())

        cleaned = form.cleaned_data["fleet_composition"]
        expected = "Rounon Dax\t\tDO6H-Q\tMetamorphosis\tFrigate\tFleet Commander (Boss)\t5 - 5 - 5"

        self.assertEqual(cleaned, expected)

    def test_skip_pre_sanitization_when_raw_value_is_none(self):
        """
        Ensure the pre-sanitization block in FleetSnapshot.__init__ (the
        `if raw_value is not None` at forms.py:224) is skipped when the
        provided data contains the key but its value is None. We verify
        this by patching sanitize_cleaned_data and asserting it is only
        called once (from clean), not during __init__.

        :return:
        :rtype:
        """

        with patch("afat.forms.sanitize_cleaned_data") as mock_sanitize:
            # Make sanitize return a harmless structure for clean()
            mock_sanitize.return_value = {"fleet_composition": None}

            form = FleetSnapshot(data={"fleet_composition": None})

            # Trigger validation (calls clean)
            is_valid = form.is_valid()

            # sanitize_cleaned_data should have been called exactly once (from clean)
            self.assertEqual(mock_sanitize.call_count, 1)

            # Form should be invalid because required field is None
            self.assertFalse(is_valid)
            self.assertIn("fleet_composition", form.errors)
