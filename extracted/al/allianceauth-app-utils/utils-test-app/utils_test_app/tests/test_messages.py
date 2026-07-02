from unittest.mock import patch

from django.test import RequestFactory, TestCase

from app_utils.messages import messages_plus

MODULE_PATH = "app_utils"


class TestMessagePlus(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    @patch(MODULE_PATH + ".messages.messages", spec=True)
    def test_valid_call(self, mock_messages):
        # given
        request = self.factory.get("https://www.example.com")
        # when
        messages_plus.debug(request, "Test Message")
        # then
        self.assertTrue(mock_messages.debug.called)
        call_args_list = mock_messages.debug.call_args_list
        args, _ = call_args_list[0]
        self.assertEqual(args[1], "Test Message")

    @patch(MODULE_PATH + ".messages.messages")
    def test_all_levels(self, mock_messages):
        text = "Test Message"
        request = self.factory.get("https://www.example.com")

        messages_plus.error(request, text)
        self.assertTrue(mock_messages.error.called)

        messages_plus.debug(request, text)
        self.assertTrue(mock_messages.debug.called)

        messages_plus.info(request, text)
        self.assertTrue(mock_messages.info.called)

        messages_plus.success(request, text)
        self.assertTrue(mock_messages.success.called)

        messages_plus.warning(request, text)
        self.assertTrue(mock_messages.warning.called)
