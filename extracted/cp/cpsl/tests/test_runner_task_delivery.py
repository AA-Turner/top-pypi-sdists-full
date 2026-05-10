import asyncio
import os
import sys
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor

from aiohttp.test_utils import make_mocked_request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from cpsl.clients.capsule import ClaimTaskResponse, GetUserIntegrationsResponse, TaskDelivery
from cpsl.constants import (
    HEADER_AUTHENTICATED,
    HEADER_EMAIL,
    HEADER_ORG_ID,
    HEADER_USER_ID,
)
from cpsl.runner import Runner


class RunnerTaskDeliveryTests(unittest.IsolatedAsyncioTestCase):
    def runner(self) -> Runner:
        r = Runner.__new__(Runner)
        r._version_id = "serve-new"
        r._version_type = "serve"
        r._app_id = "app-1"
        r._tasks = {}
        r._sessions = {}
        r._runner_stub = None
        r._session_stub = None
        r._task_stub = None
        r._data_stub = None
        r._data_app_id = "app-1"
        r._loop = None

        async def track_start():
            r._tracked_start = True

        async def track_end():
            r._tracked_end = True

        r._track_start = track_start
        r._track_end = track_end
        return r

    async def test_request_context_fetches_integrations_with_owner_id(self):
        r = self.runner()
        calls = []

        class StubSessionService:
            def get_user_integrations(self, req):
                calls.append(req)
                return GetUserIntegrationsResponse()

        r._session_stub = StubSessionService()
        request = make_mocked_request(
            "GET",
            "/",
            headers={
                HEADER_AUTHENTICATED: "true",
                HEADER_EMAIL: "viewer@example.com",
                HEADER_USER_ID: "viewer-hash",
                HEADER_ORG_ID: "org:org-1",
            },
        )

        ctx = await r._build_request_context(request)
        session = await r._build_request_session(request)

        self.assertTrue(ctx.authenticated)
        self.assertEqual(ctx.user.owner_id, "org:org-1")
        self.assertEqual(session.user.owner_id, "org:org-1")
        self.assertEqual(len(calls), 2)
        for req in calls:
            self.assertEqual(req.user_email, "viewer@example.com")
            self.assertEqual(req.owner_id, "org:org-1")

    async def test_submit_result_is_dispatched_off_event_loop(self):
        r = self.runner()
        r._loop = None
        r._submit_executor = ThreadPoolExecutor(max_workers=1)
        submitted = threading.Event()

        class SlowRunnerStub:
            def submit_result(self, _req):
                time.sleep(0.2)
                submitted.set()

        r._runner_stub = SlowRunnerStub()
        started = time.perf_counter()
        r._submit("req-1", "hello", session_id="sess-1")
        elapsed = time.perf_counter() - started

        self.assertLess(elapsed, 0.05)
        self.assertTrue(await asyncio.get_running_loop().run_in_executor(None, submitted.wait, 1))
        r._submit_executor.shutdown(wait=True)

    async def test_task_session_stream_reply_notifies_with_fresh_request_ids(self):
        r = self.runner()
        calls = []

        class NotifySessionStub:
            def notify_session(self, req):
                calls.append(req)

        session = await r._get_task_session("sess-1")
        r._session_stub = NotifySessionStub()

        async with session.stream_reply() as reply:
            reply.write("hello")
        async with session.stream_reply() as reply:
            reply.write("world")
        for _ in range(20):
            if len(calls) >= 2:
                break
            await asyncio.sleep(0.01)

        request_ids = [req.request_id for req in calls]
        self.assertNotEqual(request_ids[0], request_ids[1])
        self.assertEqual([req.text for req in calls], ["hello", "world"])
        self.assertEqual([req.external_delivery for req in calls], [True, True])

    async def test_stale_task_delivery_is_skipped_before_claim(self):
        r = self.runner()
        r._claim_called = False

        async def claim_task(_task_id):
            r._claim_called = True
            return True

        async def complete_task(*_args, **_kwargs):
            raise AssertionError("stale tasks must not be completed")

        r._claim_task = claim_task
        r._complete_task = complete_task

        await r._handle_task(
            TaskDelivery(
                task_id="task-old",
                task_name="work",
                version_id="serve-old",
            )
        )

        self.assertFalse(r._claim_called)
        self.assertTrue(r._tracked_start)
        self.assertTrue(r._tracked_end)

    async def test_versionless_task_delivery_is_skipped_for_serve_runner(self):
        r = self.runner()
        r._version_type = "serve"
        r._claim_called = False

        async def claim_task(_task_id):
            r._claim_called = True
            return True

        r._claim_task = claim_task
        await r._handle_task(TaskDelivery(task_id="legacy-task", task_name="work"))

        self.assertFalse(r._claim_called)

    async def test_claim_failure_skips_execution(self):
        r = self.runner()
        r._executed = False

        async def claim_task(_task_id):
            return False

        async def complete_task(*_args, **_kwargs):
            raise AssertionError("unclaimed tasks must not be completed")

        r._claim_task = claim_task
        r._complete_task = complete_task
        r._tasks["work"] = lambda: setattr(r, "_executed", True)

        await r._handle_task(
            TaskDelivery(
                task_id="task-1",
                task_name="work",
                version_id="serve-new",
            )
        )

        self.assertFalse(r._executed)

    async def test_claim_task_returns_false_when_server_rejects(self):
        r = self.runner()
        r._task_stub = type(
            "TaskStub",
            (),
            {"claim_task": staticmethod(lambda _req: ClaimTaskResponse(ok=False))},
        )()

        self.assertFalse(await r._claim_task("task-1"))


if __name__ == "__main__":
    unittest.main()
