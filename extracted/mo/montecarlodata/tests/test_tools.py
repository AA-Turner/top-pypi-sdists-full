from unittest import TestCase
from unittest.mock import patch

import montecarlodata.settings as settings
from montecarlodata.tools import prompt_for_hidden_values


class PromptForHiddenValuesTest(TestCase):
    @patch("montecarlodata.tools.click.prompt")
    def test_single_sentinel_value_is_prompted(self, prompt_mock):
        prompt_mock.return_value = "entered-secret"

        result = prompt_for_hidden_values(
            {"databricks_client_secret": settings.SHOW_PROMPT_VALUE, "user": "Apollo"}
        )

        self.assertEqual(result, {"databricks_client_secret": "entered-secret", "user": "Apollo"})
        prompt_mock.assert_called_once_with("databricks_client_secret", hide_input=True)

    @patch("montecarlodata.tools.click.prompt")
    def test_multiple_sentinel_values_each_prompted(self, prompt_mock):
        prompt_mock.side_effect = ["secret-a", "secret-b"]

        result = prompt_for_hidden_values(
            {
                "databricks_client_secret": settings.SHOW_PROMPT_VALUE,
                "databricks_client_id": "public-id",
                "token": settings.SHOW_PROMPT_VALUE,
            }
        )

        self.assertEqual(
            result,
            {
                "databricks_client_secret": "secret-a",
                "databricks_client_id": "public-id",
                "token": "secret-b",
            },
        )
        self.assertEqual(prompt_mock.call_count, 2)

    @patch("montecarlodata.tools.click.prompt")
    def test_non_sentinel_values_pass_through_untouched(self, prompt_mock):
        changes = {"user": "Apollo", "host": "example.com"}

        result = prompt_for_hidden_values(changes)

        self.assertEqual(result, changes)
        prompt_mock.assert_not_called()

    @patch("montecarlodata.tools.click.prompt")
    def test_value_containing_but_not_equal_to_sentinel_is_untouched(self, prompt_mock):
        # Only an exact "-1" match should prompt — substrings must not.
        changes = {"password": "-1234", "note": "value -1 here"}

        result = prompt_for_hidden_values(changes)

        self.assertEqual(result, changes)
        prompt_mock.assert_not_called()

    @patch("montecarlodata.tools.click.prompt")
    def test_empty_dict_prompts_nothing(self, prompt_mock):
        result = prompt_for_hidden_values({})

        self.assertEqual(result, {})
        prompt_mock.assert_not_called()

    @patch("montecarlodata.tools.click.prompt")
    def test_none_passes_through(self, prompt_mock):
        result = prompt_for_hidden_values(None)

        self.assertIsNone(result)
        prompt_mock.assert_not_called()
