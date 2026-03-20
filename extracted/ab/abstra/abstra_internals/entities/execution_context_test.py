import unittest

from abstra_internals.entities.execution_context import (
    CodeSnippetContext,
    FormContext,
    HookContext,
    JobContext,
    PageContext,
    Request,
    Response,
    ScriptContext,
)
from abstra_internals.repositories.producer import PreExecution


def _make_preexecution(context) -> PreExecution:
    pe = PreExecution(stage_id="test", context=context, execution_id="123")
    serialized = pe.dump_json()
    return PreExecution.model_validate_json(serialized)


class TestContextDiscriminatorRoundtrip(unittest.TestCase):
    """Ensure all context types survive JSON serialization/deserialization."""

    def test_page_context_roundtrip(self):
        ctx = PageContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        pe = _make_preexecution(ctx)
        self.assertIsInstance(pe.context, PageContext)
        self.assertEqual(pe.context.type, "page")

    def test_hook_context_roundtrip(self):
        ctx = HookContext(
            request=Request(query_params={}, headers={}, method="POST", body="{}"),
            response=Response(headers={}, status=200, body=""),
        )
        pe = _make_preexecution(ctx)
        self.assertIsInstance(pe.context, HookContext)
        self.assertEqual(pe.context.type, "hook")

    def test_form_context_roundtrip(self):
        ctx = FormContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
        )
        pe = _make_preexecution(ctx)
        self.assertIsInstance(pe.context, FormContext)
        self.assertEqual(pe.context.type, "form")

    def test_script_context_roundtrip(self):
        ctx = ScriptContext(task_id="task-123")
        pe = _make_preexecution(ctx)
        self.assertIsInstance(pe.context, ScriptContext)
        self.assertEqual(pe.context.type, "script")

    def test_job_context_roundtrip(self):
        ctx = JobContext()
        pe = _make_preexecution(ctx)
        self.assertIsInstance(pe.context, JobContext)
        self.assertEqual(pe.context.type, "job")

    def test_code_snippet_context_roundtrip(self):
        ctx = CodeSnippetContext()
        pe = _make_preexecution(ctx)
        self.assertIsInstance(pe.context, CodeSnippetContext)
        self.assertEqual(pe.context.type, "code_snippet")

    def test_page_not_confused_with_hook(self):
        """The original bug: PageContext and HookContext have identical fields,
        so without the discriminator, pydantic would deserialize PageContext as HookContext."""
        page_ctx = PageContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        hook_ctx = HookContext(
            request=Request(query_params={}, headers={}, method="GET", body=""),
            response=Response(headers={}, status=200, body=""),
        )
        page_pe = _make_preexecution(page_ctx)
        hook_pe = _make_preexecution(hook_ctx)
        self.assertIsInstance(page_pe.context, PageContext)
        self.assertIsInstance(hook_pe.context, HookContext)
        self.assertNotIsInstance(page_pe.context, HookContext)
        self.assertNotIsInstance(hook_pe.context, PageContext)


class TestContextDiscriminatorLegacy(unittest.TestCase):
    """Ensure old messages without 'type' field are correctly inferred."""

    def _validate(self, context_dict, expected_type):
        msg = {
            "stageId": "test",
            "executionId": "123",
            "userJwt": None,
            "sendQueue": None,
            "recvQueue": None,
            "queueExpireMs": None,
            "context": context_dict,
        }
        pe = PreExecution.model_validate(msg)
        self.assertIsInstance(pe.context, expected_type)

    def test_legacy_hook(self):
        self._validate(
            {
                "request": {
                    "queryParams": {},
                    "headers": {},
                    "method": "GET",
                    "body": "",
                },
                "response": {"headers": {}, "status": 200, "body": ""},
                "sentTasks": [],
                "legacyThreadData": {},
                "mockExecution": {"testPendingTasks": [], "testRequest": None},
            },
            HookContext,
        )

    def test_legacy_form(self):
        self._validate(
            {
                "request": {
                    "queryParams": {},
                    "headers": {},
                    "method": "GET",
                    "body": "",
                },
                "sentTasks": [],
                "legacyThreadData": {},
                "mockExecution": {"testPendingTasks": [], "testAnswers": []},
            },
            FormContext,
        )

    def test_legacy_script(self):
        self._validate(
            {
                "taskId": "task-123",
                "sentTasks": [],
                "legacyThreadData": {},
                "mockExecution": {"testPendingTasks": []},
            },
            ScriptContext,
        )

    def test_legacy_job(self):
        self._validate(
            {
                "sentTasks": [],
                "legacyThreadData": {},
                "mockExecution": {"testPendingTasks": []},
            },
            JobContext,
        )

    def test_legacy_code_snippet(self):
        self._validate(
            {"mockExecution": {"testPendingTasks": []}},
            CodeSnippetContext,
        )
