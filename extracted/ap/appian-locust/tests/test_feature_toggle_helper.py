import unittest
from typing import List, Generator, Callable

import appian_locust._feature_toggle_helper as feature_toggle_helper
from appian_locust import AppianTaskSet, FeatureFlag
from locust import Locust, TaskSet

from .mock_client import CustomLocust


class FeatureToggleHelperTest(unittest.TestCase):

    relative_uri = '/suite/tempo/ui/sail-client/sites-05d032ca6319b11b6fc9.cache.js'
    html_snippet = (
        f'</script><script src="{relative_uri}?appian_environment=sites">\n'
        f'</script><script src="/suite/tempo/ui/sail-client/omnibox-05d032ca6319b11b6fc9.cache.js?appian_environment=sites" defer="true">\n'
        f'</script></body></html>'
    )
    js_snippet = """
                ADERS=exports.LEGACY_FEATURE_FLAGS=exports.DEFAULT_FEATURE_FLAGS=undefined;
                var RAW_DEFAULT_FEATURE_FLAGS={};var RAW_LEGACY_FEATURE_FLAGS=RAW_DEFAULT_FEATURE_FLAGS&2147483647;
                var DEFAULT_FEATURE_FLAGS=exports.DEFAULT_FEATURE_FLAGS=RAW_DEFAULT_FEATURE_FLAGS.toString(16);
                var LEGACY_FEATURE_FLAGS=exports.LEGACY_FEATURE_FLAGS=RAW_LEGACY_FEATURE_FLAGS.toString(16);var
                """
    web_asset_url = 'https://web-assets.appiancloud.com/casdbasdf/tempo/ui/sail-client/sites-6bd221b7ad2f1d9b84e8.cache.js'
    cloud_html_snippet = (
        f'<script async="" src="https://web-assets.appiancloud.com/bacdasdfASDAS/tempo/ui/sail-client/embeddedBootstrap.nocache.js?appian_environment=sites"'
        f'id="appianEmbedded" internal="true" data-bannerposition="hidden" data-primary-host="https://site.com/suite"></script>'
        f'<script src="{web_asset_url}?appian_environment=sites"></script>'
        f'</script></body></html>'
    )

    def setUp(self) -> None:
        self.custom_locust = CustomLocust(Locust())
        parent_task_set = TaskSet(self.custom_locust)
        setattr(parent_task_set, "host", "")
        setattr(parent_task_set, "credentials", [["", ""]])
        setattr(parent_task_set, "auth", ["", ""])

        self.task_set = AppianTaskSet(parent_task_set)
        self.task_set.host = ""

        # test_on_start_auth_success is covered here.
        self.custom_locust.set_response("auth?appian_environment=tempo", 200, '{}')
        self.task_set.on_start()

    def tearDown(self) -> None:
        self.task_set.on_stop()

    def test_get_javascript_uri_missing(self) -> None:
        # Given
        self.custom_locust.set_response("/suite/sites", 200, "abc")

        # When
        uri = feature_toggle_helper._get_javascript_uri(self.task_set.appian._interactor, {})

        # Then
        self.assertEqual(uri, None)

    def test_get_javascript_uri_present(self) -> None:
        # Given a snippet of the sites page
        self.custom_locust.set_response("/suite/sites", 200, self.html_snippet)

        # When
        uri = feature_toggle_helper._get_javascript_uri(self.task_set.appian._interactor, {})

        # Then
        self.assertEqual(uri, self.relative_uri)

    def test_get_javascript_uri_present_cloud_assets(self) -> None:
        # Given
        self.custom_locust.set_response("/suite/sites", 200, self.cloud_html_snippet)

        # When
        uri = feature_toggle_helper._get_javascript_uri(self.task_set.appian._interactor, {})

        # Then
        self.assertEqual(uri, self.web_asset_url)

    def test_get_javascript_and_find_feature_flag_missing_value(self) -> None:
        # Given
        script_uri = "abc"
        self.custom_locust.set_response(script_uri, 200, "body")

        # When
        flag = feature_toggle_helper._get_javascript_and_find_feature_flag(
            self.task_set.appian.client, script_uri, {})

        # Then
        self.assertEqual(flag, None)

    def test_get_javascript_and_find_feature_flag_value_present_hex(self) -> None:
        # Given a snippet of the minified js
        script_uri = "/suite/file.js"
        self.custom_locust.set_response(script_uri,
                                        200, self.js_snippet.format("0xdc9fffceebc"))

        # When
        uri = feature_toggle_helper._get_javascript_and_find_feature_flag(self.task_set.appian.client,
                                                                          script_uri, {})

        # Then
        self.assertEqual(
            uri, "0xdc9fffceebc")

    def test_get_javascript_and_find_feature_flag_value_present_big_int(self) -> None:
        # Given a snippet of the minified js
        script_uri = "/suite/file.js"
        for i in [9, 10]:
            self.custom_locust.set_response(script_uri,
                                            200, self.js_snippet.format(
                                                f'jsbi__WEBPACK_IMPORTED_MODULE_{i}__["default"].BigInt("0b110100100111011100000111111111111111001110111010111100")'))

            # When
            binVal = feature_toggle_helper._get_javascript_and_find_feature_flag(self.task_set.appian.client,
                                                                                 script_uri, {})

            # Then
            self.assertEqual(
                binVal, "0b110100100111011100000111111111111111001110111010111100")

    def test_get_javascript_and_find_feature_flag_value_present_integer(self) -> None:
        # Given a snippet of the minified js
        script_uri = "/suite/file.js"
        self.custom_locust.set_response(script_uri,
                                        200, self.js_snippet.format("5802956083228348"))
        # When
        uri = feature_toggle_helper._get_javascript_and_find_feature_flag(self.task_set.appian.client,
                                                                          script_uri, {})

        # Then
        self.assertEqual(
            uri, "5802956083228348")

    def test_get_feature_flags_from_regex_match_hex(self) -> None:
        # Given
        hex_val = "0xdc9fffceebc"

        # When
        flag, flag_extended = feature_toggle_helper._get_feature_flags_from_regex_match(
            hex_val)

        # Then
        self.assertEqual(flag, "7ffceebc")
        self.assertEqual(flag_extended, "dc9fffceebc")

    def test_get_feature_flags_from_regex_match_big_int(self) -> None:
        # Given
        big_int_val = "0b110100100111011100000111111111111111001110111010111100"

        # When
        flag, flag_extended = feature_toggle_helper._get_feature_flags_from_regex_match(
            big_int_val)

        # Then
        self.assertEqual(flag, "7ffceebc")
        self.assertEqual(flag_extended, "349dc1fffceebc")

    def test_get_feature_flags_from_regex_match_integer(self) -> None:
        # Given
        int_val = "5802956083228348"

        # When
        flag, flag_extended = feature_toggle_helper._get_feature_flags_from_regex_match(
            int_val)

        # Then
        self.assertEqual(flag, "7ffceebc")
        self.assertEqual(flag_extended, "149dc1fffceebc")

    def test_end_to_end_get_feature_flags(self) -> None:
        # Given a snippet of the sites page and js snippet
        self.custom_locust.set_response("/suite/sites", 200, self.html_snippet)
        self.custom_locust.set_response(self.relative_uri,
                                        200, self.js_snippet.format("5802956083228348"))

        # When
        flag, flag_extended = feature_toggle_helper.get_client_feature_toggles(
            self.task_set.appian._interactor,
            self.task_set.appian.client
        )

        # Then
        self.assertEqual(flag, "7ffceebc")
        self.assertEqual(flag_extended, "149dc1fffceebc")

    def test_end_to_end_get_feature_flags_fail_no_sites_link(self) -> None:
        # Given a missing js snippet
        self.custom_locust.set_response("/suite/sites", 200, '')

        # When and Then
        with self.assertRaisesRegex(Exception, "Could not find script uri to retrieve client feature"):
            feature_toggle_helper.get_client_feature_toggles(
                self.task_set.appian._interactor,
                self.task_set.appian.client
            )

    def test_end_to_end_get_feature_flags_fail_no_feature_toggles_found(self) -> None:
        # Given a missing feature toggle
        self.custom_locust.set_response("/suite/sites", 200, self.html_snippet)
        self.custom_locust.set_response(self.relative_uri,
                                        200, 'missing feature toggle')

        # When and Then
        with self.assertRaisesRegex(Exception, "Could not find flag string within uri /suite/tempo/ui"):
            feature_toggle_helper.get_client_feature_toggles(
                self.task_set.appian._interactor,
                self.task_set.appian.client
            )

    def test_to_hex_str(self) -> None:
        # Given
        hex_val = "0xdc9fffceebc"
        intVal = int(hex_val, 16)

        # When
        flagHexStr = feature_toggle_helper._to_hex_str(intVal)

        # Then
        self.assertEqual(flagHexStr, "dc9fffceebc")

    def test_truncate_flag_extended_long_input(self) -> None:
        # Given
        longHexVal = 0xdc9fffceebc

        # When
        shortVal = feature_toggle_helper._truncate_flag_extended(longHexVal)

        # Then
        self.assertEqual(shortVal, 0x7ffceebc)

    def test_truncate_flag_extended_short_input(self) -> None:
        # Given
        shortHexVal = 0x7ffceebc

        # When
        shortVal = feature_toggle_helper._truncate_flag_extended(shortHexVal)

        # Then
        self.assertEqual(shortVal, 0x7ffceebc)

    def create_override_flag_mask_runner(self, flags: Callable[[], Generator[FeatureFlag, None, None]], expectedResult: int) -> None:
        # When
        feature_flag_mask = feature_toggle_helper._create_override_flag_mask(flags)

        # Then
        self.assertEqual(feature_flag_mask, expectedResult)

    def test_create_override_flag_mask_no_flag(self) -> None:
        # Given
        def flags() -> Generator[FeatureFlag, None, None]:
            yield from ()
        expectedResult = 0

        # Then
        self.create_override_flag_mask_runner(flags, expectedResult)

    def test_create_override_flag_mask_one_flag(self) -> None:
        # Given
        def flags() -> Generator[FeatureFlag, None, None]:
            yield FeatureFlag.SAIL_FORMS
        expectedResult = 4

        # Then
        self.create_override_flag_mask_runner(flags, expectedResult)

    def test_create_override_flag_mask_multiple_flags(self) -> None:
        # Given
        def flags() -> Generator[FeatureFlag, None, None]:
            yield FeatureFlag.SAIL_FORMS
            yield FeatureFlag.COMPACT_URI_TEMPLATES
        expectedResult = 1028

        # Then
        self.create_override_flag_mask_runner(flags, expectedResult)

    def override_default_flags_runner(self, flags: Callable[[], Generator[FeatureFlag, None, None]], expected_featured_flag_extended: str,  expected_feature_flag: str) -> None:
        # Given a snippet of the sites page
        self.task_set.appian._interactor.client.feature_flag_extended = "149dc1fffceebc"
        self.task_set.appian._interactor.client.feature_flag = "7ffceebc"

        # When
        feature_toggle_helper.override_default_feature_flags(self.task_set.appian._interactor, flags)

        # Then
        self.assertEqual(self.task_set.appian._interactor.client.feature_flag_extended, expected_featured_flag_extended)
        self.assertEqual(self.task_set.appian._interactor.client.feature_flag, expected_feature_flag)

    def test_override_default_flags_no_flags(self) -> None:
        # Given a snippet of the sites page
        def flags() -> Generator[FeatureFlag, None, None]:
            yield from ()

        self.override_default_flags_runner((flags), "149dc1fffceebc", "7ffceebc")

    def test_override_default_flags_one_flag(self) -> None:
        # Given a snippet of the sites page
        def flags() -> Generator[FeatureFlag, None, None]:
            yield FeatureFlag.SHORT_CIRCUIT_PARTIAL_RENDERING

        self.override_default_flags_runner(flags, "149dc1fffcefbc", "7ffcefbc")

    def test_override_default_flags_multiple_flags(self) -> None:
        # Given a snippet of the sites page
        def flags() -> Generator[FeatureFlag, None, None]:
            yield FeatureFlag.SHORT_CIRCUIT_PARTIAL_RENDERING
            yield FeatureFlag.INLINE_TASK_CONTROLS

        self.override_default_flags_runner(flags, "149dc1fffcffbc", "7ffcffbc")

    def test_declare_device_as_mobile(self) -> None:
        # Given a snippet of the sites page
        self.custom_locust.set_response("/suite/sites", 200, self.html_snippet)

        # When
        feature_toggle_helper.set_mobile_feature_flags(self.task_set.appian._interactor)

        # Then
        self.assertEqual(self.task_set.appian._interactor.client.feature_flag_extended, "149dd1fffceebc")
        self.assertEqual(self.task_set.appian._interactor.client.feature_flag, "7ffceebc")


if __name__ == '__main__':
    unittest.main()
