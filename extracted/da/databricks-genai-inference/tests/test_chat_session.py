import unittest
from unittest.mock import patch

from constants import (CHAT_COMPLETION_MESSAGES, CHAT_COMPLETION_MODEL_NAME, CHAT_COMPLETION_MODEL_SYSTEM_MESSAGE,
                       CHAT_COMPLETION_RESPONSE_OBJECT_1, CHAT_SESSION_PARAMETERS, COMPLETION_PROMPT_1)

from databricks_genai_inference import ChatSession


class TestChatSession(unittest.TestCase):

    def setUp(self):
        self.model = CHAT_COMPLETION_MODEL_NAME
        self.system_message = CHAT_COMPLETION_MODEL_SYSTEM_MESSAGE
        self.chat_session = ChatSession(self.model, self.system_message, **CHAT_SESSION_PARAMETERS)

    @patch("databricks_genai_inference.ChatCompletion.create", return_value=CHAT_COMPLETION_RESPONSE_OBJECT_1)
    def test_reply(self, mocked_request):
        self.chat_session.reply(COMPLETION_PROMPT_1)
        mocked_request.assert_called_once_with(model=self.model,
                                               messages=CHAT_COMPLETION_MESSAGES,
                                               **CHAT_SESSION_PARAMETERS)
        self.assertEqual(self.chat_session.chat_history[-1]["role"], "assistant")
        self.assertEqual(self.chat_session.chat_history[-1]["content"], CHAT_COMPLETION_RESPONSE_OBJECT_1.message)

    @patch("databricks_genai_inference.ChatCompletion.create", return_value=CHAT_COMPLETION_RESPONSE_OBJECT_1)
    def test_last(self, mocked_request):
        self.assertEqual(self.chat_session.last, "")
        self.chat_session.reply(COMPLETION_PROMPT_1)
        self.assertEqual(self.chat_session.last, CHAT_COMPLETION_RESPONSE_OBJECT_1.message)

    @patch("databricks_genai_inference.ChatCompletion.create", return_value=CHAT_COMPLETION_RESPONSE_OBJECT_1)
    def test_history(self, mocked_request):
        self.assertEqual(self.chat_session.history, [{"role": "system", "content": self.system_message}])
        self.chat_session.reply(COMPLETION_PROMPT_1)
        self.assertEqual(self.chat_session.history, [
            {
                "role": "system",
                "content": self.system_message
            },
            {
                "role": "user",
                "content": COMPLETION_PROMPT_1
            },
            {
                "role": "assistant",
                "content": CHAT_COMPLETION_RESPONSE_OBJECT_1.message
            },
        ])

    @patch("databricks_genai_inference.ChatCompletion.create", return_value=CHAT_COMPLETION_RESPONSE_OBJECT_1)
    def test_pretty_history(self, mocked_request):
        self.assertEqual(self.chat_session.pretty_history, f"\nsystem: {self.system_message}")
        self.chat_session.reply(COMPLETION_PROMPT_1)
        self.assertEqual(
            self.chat_session.pretty_history,
            f"\nsystem: {self.system_message}\nuser: {COMPLETION_PROMPT_1}\nassistant: {CHAT_COMPLETION_RESPONSE_OBJECT_1.message}"
        )

    @patch("databricks_genai_inference.ChatCompletion.create", return_value=CHAT_COMPLETION_RESPONSE_OBJECT_1)
    def test_count(self, mocked_request):
        self.assertEqual(self.chat_session.count, 0)
        self.chat_session.reply(COMPLETION_PROMPT_1)
        self.assertEqual(self.chat_session.count, 1)
