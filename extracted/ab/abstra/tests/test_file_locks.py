import json
import unittest
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.controllers.codebase_events import CodebaseEventController
from abstra_internals.controllers.file_locks import (
    DEFAULT_HEARTBEAT_TTL,
    FileLockController,
    FileLockedException,
    LockState,
    PresenceState,
)
from abstra_internals.services import mcp_context
from tests.fixtures import BaseTest


class FileLockControllerTest(unittest.TestCase):
    def setUp(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []

    def tearDown(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []

    def test_acquire_grants_when_unlocked(self) -> None:
        granted, holder = FileLockController.acquire(
            "main.py", "sess-a", "alice@example.com", "Alice"
        )
        self.assertTrue(granted)
        self.assertIsNotNone(holder)
        assert holder is not None
        self.assertEqual(holder.holder_email, "alice@example.com")
        self.assertEqual(holder.session_id, "sess-a")
        self.assertEqual(len(FileLockController.get_all_locks()), 1)

    def test_acquire_blocks_other_user(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        granted, holder = FileLockController.acquire(
            "main.py", "sess-b", "bob@example.com", "Bob"
        )
        self.assertFalse(granted)
        assert holder is not None
        self.assertEqual(holder.holder_email, "alice@example.com")
        self.assertEqual(len(FileLockController.get_all_locks()), 1)

    def test_acquire_idempotent_same_session_extends_heartbeat(self) -> None:
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1000.0
        ):
            FileLockController.acquire(
                "main.py", "sess-a", "alice@example.com", "Alice"
            )
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1015.0
        ):
            granted, holder = FileLockController.acquire(
                "main.py", "sess-a", "alice@example.com", "Alice"
            )
        self.assertTrue(granted)
        assert holder is not None
        self.assertEqual(holder.acquired_at, 1000.0)
        self.assertEqual(holder.last_heartbeat_at, 1015.0)

    def test_two_tabs_same_user_second_blocked(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        granted, holder = FileLockController.acquire(
            "main.py", "sess-b", "alice@example.com", "Alice"
        )
        self.assertFalse(granted)
        assert holder is not None
        self.assertEqual(holder.session_id, "sess-a")

    def test_release_only_by_holder(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        released_wrong_session = FileLockController.release(
            "main.py", "sess-b", "alice@example.com"
        )
        self.assertFalse(released_wrong_session)
        released_wrong_email = FileLockController.release(
            "main.py", "sess-a", "bob@example.com"
        )
        self.assertFalse(released_wrong_email)
        self.assertEqual(len(FileLockController.get_all_locks()), 1)
        released_correct = FileLockController.release(
            "main.py", "sess-a", "alice@example.com"
        )
        self.assertTrue(released_correct)
        self.assertEqual(len(FileLockController.get_all_locks()), 0)

    def test_release_nonexistent_lock(self) -> None:
        released = FileLockController.release("ghost.py", "sess-x", "ghost@example.com")
        self.assertFalse(released)

    def test_heartbeat_extends_ttl(self) -> None:
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1000.0
        ):
            FileLockController.acquire(
                "main.py", "sess-a", "alice@example.com", "Alice"
            )
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1025.0
        ):
            still_held, _ = FileLockController.heartbeat_lock(
                "main.py", "sess-a", "alice@example.com"
            )
        self.assertTrue(still_held)
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1050.0
        ):
            FileLockController.sweep_once(ttl=DEFAULT_HEARTBEAT_TTL)
        self.assertEqual(len(FileLockController.get_all_locks()), 1)

    def test_heartbeat_fails_when_lock_lost(self) -> None:
        still_held, holder = FileLockController.heartbeat_lock(
            "main.py", "sess-a", "alice@example.com"
        )
        self.assertFalse(still_held)
        self.assertIsNone(holder)

    def test_heartbeat_fails_when_other_holder(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        still_held, holder = FileLockController.heartbeat_lock(
            "main.py", "sess-b", "bob@example.com"
        )
        self.assertFalse(still_held)
        assert holder is not None
        self.assertEqual(holder.holder_email, "alice@example.com")

    def test_sweeper_expires_stale_lock(self) -> None:
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1000.0
        ):
            FileLockController.acquire(
                "main.py", "sess-a", "alice@example.com", "Alice"
            )
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1100.0
        ):
            expired_locks, expired_presence = FileLockController.sweep_once(ttl=30.0)
        self.assertEqual(len(expired_locks), 1)
        self.assertEqual(expired_locks[0].file_path, "main.py")
        self.assertEqual(len(FileLockController.get_all_locks()), 0)
        self.assertEqual(expired_presence, [])

    def test_release_for_path_drops_lock(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        FileLockController.acquire("other.py", "sess-b", "bob@example.com", "Bob")
        released = FileLockController.release_for_path("main.py")
        self.assertEqual(len(released), 1)
        self.assertEqual(released[0].file_path, "main.py")
        remaining = FileLockController.get_all_locks()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].file_path, "other.py")

    def test_release_for_path_no_lock(self) -> None:
        released = FileLockController.release_for_path("ghost.py")
        self.assertEqual(released, [])

    def test_release_for_path_directory_prefix(self) -> None:
        FileLockController.acquire("src/foo.py", "sess-a", "alice@example.com", "Alice")
        FileLockController.acquire("src/bar.py", "sess-b", "bob@example.com", "Bob")
        FileLockController.acquire(
            "srcother/baz.py", "sess-c", "carol@example.com", "Carol"
        )
        released = FileLockController.release_for_path("src")
        self.assertEqual(len(released), 2)
        released_paths = {r.file_path for r in released}
        self.assertEqual(released_paths, {"src/foo.py", "src/bar.py"})
        remaining = FileLockController.get_all_locks()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0].file_path, "srcother/baz.py")

    def test_presence_join_update_leave(self) -> None:
        state_join = FileLockController.update_presence(
            "sess-a", "alice@example.com", "Alice", "main.py"
        )
        self.assertEqual(state_join.email, "alice@example.com")
        self.assertEqual(len(FileLockController.get_all_presence()), 1)

        state_update = FileLockController.update_presence(
            "sess-a", "alice@example.com", "Alice", "other.py"
        )
        self.assertEqual(state_update.current_file_path, "other.py")
        self.assertEqual(len(FileLockController.get_all_presence()), 1)

        removed = FileLockController.remove_presence("sess-a")
        self.assertTrue(removed)
        self.assertEqual(len(FileLockController.get_all_presence()), 0)

    def test_presence_remove_nonexistent(self) -> None:
        removed = FileLockController.remove_presence("sess-ghost")
        self.assertFalse(removed)

    def test_sweeper_expires_stale_presence(self) -> None:
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1000.0
        ):
            FileLockController.update_presence(
                "sess-a", "alice@example.com", "Alice", None
            )
        with patch(
            "abstra_internals.controllers.file_locks.time.time", return_value=1100.0
        ):
            _, expired_presence = FileLockController.sweep_once(ttl=30.0)
        self.assertEqual(len(expired_presence), 1)
        self.assertEqual(expired_presence[0].session_id, "sess-a")
        self.assertEqual(len(FileLockController.get_all_presence()), 0)

    def test_broadcast_acquire_uses_codebase_events_socket(self) -> None:
        listener = MagicMock()
        CodebaseEventController.listeners = [listener]

        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")

        self.assertEqual(listener.send.call_count, 1)
        sent_payload = json.loads(listener.send.call_args.args[0])
        self.assertEqual(sent_payload["event"], "lock_acquired")
        self.assertEqual(sent_payload["filepath"], "main.py")
        self.assertEqual(sent_payload["lock"]["holderEmail"], "alice@example.com")
        self.assertEqual(sent_payload["lock"]["sessionId"], "sess-a")

    def test_broadcast_release_event(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        listener = MagicMock()
        CodebaseEventController.listeners = [listener]

        FileLockController.release("main.py", "sess-a", "alice@example.com")

        self.assertEqual(listener.send.call_count, 1)
        sent_payload = json.loads(listener.send.call_args.args[0])
        self.assertEqual(sent_payload["event"], "lock_released")
        self.assertEqual(sent_payload["lock"]["holderEmail"], "alice@example.com")

    def test_broadcast_presence_join_and_update(self) -> None:
        listener = MagicMock()
        CodebaseEventController.listeners = [listener]

        FileLockController.update_presence(
            "sess-a", "alice@example.com", "Alice", "main.py"
        )
        FileLockController.update_presence(
            "sess-a", "alice@example.com", "Alice", "other.py"
        )

        self.assertEqual(listener.send.call_count, 2)
        first = json.loads(listener.send.call_args_list[0].args[0])
        second = json.loads(listener.send.call_args_list[1].args[0])
        self.assertEqual(first["event"], "presence_joined")
        self.assertEqual(second["event"], "presence_update")
        self.assertEqual(second["presence"]["currentFilePath"], "other.py")

    def test_no_broadcast_on_idempotent_reacquire(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        listener = MagicMock()
        CodebaseEventController.listeners = [listener]

        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")

        listener.send.assert_not_called()

    def test_dataclass_states_are_immutable(self) -> None:
        lock = LockState(
            file_path="x.py",
            holder_email="a@a",
            holder_name="A",
            session_id="s",
            acquired_at=0.0,
            last_heartbeat_at=0.0,
        )
        with self.assertRaises(Exception):
            lock.holder_email = "b@b"  # type: ignore[misc]
        presence = PresenceState(
            session_id="s",
            email="a@a",
            name="A",
            current_file_path=None,
            last_heartbeat_at=0.0,
        )
        with self.assertRaises(Exception):
            presence.email = "b@b"  # type: ignore[misc]


class FindBlockingLockTest(unittest.TestCase):
    def setUp(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []

    def tearDown(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []

    def test_none_when_unlocked(self) -> None:
        blocking = FileLockController.find_blocking_lock("main.py", "alice@example.com")
        self.assertIsNone(blocking)

    def test_none_for_holder(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        blocking = FileLockController.find_blocking_lock("main.py", "alice@example.com")
        self.assertIsNone(blocking)

    def test_blocks_other_email(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        blocking = FileLockController.find_blocking_lock("main.py", "bob@example.com")
        assert blocking is not None
        self.assertEqual(blocking.holder_email, "alice@example.com")

    def test_allows_same_email_other_session(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "alice@example.com", "Alice")
        blocking = FileLockController.find_blocking_lock("main.py", "alice@example.com")
        self.assertIsNone(blocking)

    def test_empty_email_never_bypasses(self) -> None:
        FileLockController.acquire("main.py", "sess-a", "", "")
        blocking = FileLockController.find_blocking_lock("main.py", "")
        assert blocking is not None
        self.assertEqual(blocking.session_id, "sess-a")

    def test_blocks_directory_with_locked_descendant(self) -> None:
        FileLockController.acquire("src/foo.py", "sess-a", "alice@example.com", "Alice")
        blocking = FileLockController.find_blocking_lock("src", "bob@example.com")
        assert blocking is not None
        self.assertEqual(blocking.file_path, "src/foo.py")

    def test_directory_descendant_held_by_requester_not_blocking(self) -> None:
        FileLockController.acquire("src/foo.py", "sess-a", "alice@example.com", "Alice")
        blocking = FileLockController.find_blocking_lock("src", "alice@example.com")
        self.assertIsNone(blocking)

    def test_ignores_sibling_path_prefix(self) -> None:
        FileLockController.acquire(
            "srcother/baz.py", "sess-a", "alice@example.com", "Alice"
        )
        blocking = FileLockController.find_blocking_lock("src", "bob@example.com")
        self.assertIsNone(blocking)


class CodebaseWriteLockGuardTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()
        FileLockController.reset_state()
        CodebaseEventController.listeners = []
        (self.root / "guarded.py").write_text("original", encoding="utf-8")

    def tearDown(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []
        super().tearDown()

    def _lock_as_other_user(self, path: str = "guarded.py") -> None:
        FileLockController.acquire(path, "sess-other", "other@example.com", "Other")

    def test_edit_blocked_when_locked_by_other_user(self) -> None:
        self._lock_as_other_user()
        response = self.client.put(
            "/_editor/api/codebase/files/guarded.py",
            json={"content": "hacked"},
        )
        self.assertEqual(response.status_code, 423)
        body = response.json or {}
        self.assertEqual(body.get("error"), "file_locked")
        self.assertEqual(body["holder"]["holderEmail"], "other@example.com")
        self.assertEqual(
            (self.root / "guarded.py").read_text(encoding="utf-8"), "original"
        )

    def test_edit_allowed_for_lock_holder_session(self) -> None:
        FileLockController.acquire("guarded.py", "tab-1", "local", "local")
        response = self.client.put(
            "/_editor/api/codebase/files/guarded.py",
            json={"content": "updated"},
            headers={"X-Abstra-Lock-Session-Id": "tab-1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            (self.root / "guarded.py").read_text(encoding="utf-8"), "updated"
        )

    def test_edit_allowed_for_same_user_other_session(self) -> None:
        FileLockController.acquire("guarded.py", "tab-1", "local", "local")
        response = self.client.put(
            "/_editor/api/codebase/files/guarded.py",
            json={"content": "updated"},
            headers={"X-Abstra-Lock-Session-Id": "tab-2"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            (self.root / "guarded.py").read_text(encoding="utf-8"), "updated"
        )

    def test_edit_allowed_when_unlocked(self) -> None:
        response = self.client.put(
            "/_editor/api/codebase/files/guarded.py",
            json={"content": "updated"},
        )
        self.assertEqual(response.status_code, 200)

    def test_create_overwrite_blocked_when_locked_by_other_user(self) -> None:
        self._lock_as_other_user()
        response = self.client.post(
            "/_editor/api/codebase/files/guarded.py?overwrite=true",
            data=b"hacked",
        )
        self.assertEqual(response.status_code, 423)
        self.assertEqual(
            (self.root / "guarded.py").read_text(encoding="utf-8"), "original"
        )

    def test_create_overwrite_allowed_for_ai_write_when_locked_by_other_user(
        self,
    ) -> None:
        self._lock_as_other_user()
        response = self.client.post(
            "/_editor/api/codebase/files/guarded.py?overwrite=true",
            data=b"ai content",
            headers={"X-Abstra-User-Message-Id": "msg-1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            (self.root / "guarded.py").read_text(encoding="utf-8"), "ai content"
        )

    def test_create_overwrite_with_invalid_message_id_still_blocked(self) -> None:
        self._lock_as_other_user()
        response = self.client.post(
            "/_editor/api/codebase/files/guarded.py?overwrite=true",
            data=b"hacked",
            headers={"X-Abstra-User-Message-Id": "bad value!"},
        )
        self.assertEqual(response.status_code, 423)
        self.assertEqual(
            (self.root / "guarded.py").read_text(encoding="utf-8"), "original"
        )

    def test_delete_blocked_when_locked_by_other_user(self) -> None:
        self._lock_as_other_user()
        response = self.client.delete("/_editor/api/codebase/files/guarded.py")
        self.assertEqual(response.status_code, 423)
        self.assertTrue((self.root / "guarded.py").exists())

    def test_delete_directory_blocked_when_descendant_locked(self) -> None:
        (self.root / "pkg").mkdir()
        (self.root / "pkg" / "mod.py").write_text("x", encoding="utf-8")
        FileLockController.acquire(
            "pkg/mod.py", "sess-other", "other@example.com", "Other"
        )
        response = self.client.delete("/_editor/api/codebase/files/pkg")
        self.assertEqual(response.status_code, 423)
        self.assertTrue((self.root / "pkg" / "mod.py").exists())

    def test_rename_blocked_when_locked_by_other_user(self) -> None:
        self._lock_as_other_user()
        response = self.client.patch(
            "/_editor/api/codebase/files",
            json={
                "pathParts": ["guarded.py"],
                "newPathParts": ["renamed.py"],
            },
        )
        self.assertEqual(response.status_code, 423)
        self.assertTrue((self.root / "guarded.py").exists())


class UpdateStageLockGuardTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        FileLockController.reset_state()
        CodebaseEventController.listeners = []
        self.stage = self.controller.create_stage("form", "My Form", "my_form.py")

    def tearDown(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []
        super().tearDown()

    def _stage_code(self) -> str:
        return (self.root / "my_form.py").read_text(encoding="utf-8")

    def test_code_update_blocked_when_locked_without_request_context(self) -> None:
        FileLockController.acquire(
            "my_form.py", "sess-other", "other@example.com", "Other"
        )
        original = self._stage_code()
        with self.assertRaises(FileLockedException) as ctx:
            self.controller.update_stage(
                self.stage.id, {"code_content": "print('hacked')"}
            )
        self.assertIn("other@example.com", str(ctx.exception))
        self.assertEqual(self._stage_code(), original)

    def test_code_update_allowed_when_unlocked(self) -> None:
        self.controller.update_stage(
            self.stage.id, {"code_content": "print('updated')"}
        )
        self.assertEqual(self._stage_code(), "print('updated')")

    def test_metadata_update_allowed_when_locked(self) -> None:
        FileLockController.acquire(
            "my_form.py", "sess-other", "other@example.com", "Other"
        )
        updated = self.controller.update_stage(self.stage.id, {"title": "Renamed"})
        self.assertEqual(updated.title, "Renamed")

    def test_code_update_allowed_for_lock_holder_session(self) -> None:
        FileLockController.acquire("my_form.py", "tab-1", "local", "local")
        app = flask.Flask(__name__)
        with app.test_request_context(headers={"X-Abstra-Lock-Session-Id": "tab-1"}):
            self.controller.update_stage(
                self.stage.id, {"code_content": "print('mine')"}
            )
        self.assertEqual(self._stage_code(), "print('mine')")

    def test_code_update_allowed_for_same_user_other_session(self) -> None:
        FileLockController.acquire("my_form.py", "tab-1", "local", "local")
        app = flask.Flask(__name__)
        with app.test_request_context(headers={"X-Abstra-Lock-Session-Id": "tab-2"}):
            self.controller.update_stage(
                self.stage.id, {"code_content": "print('other tab')"}
            )
        self.assertEqual(self._stage_code(), "print('other tab')")

    def test_code_update_allowed_for_ai_write_when_locked_by_other_user(self) -> None:
        FileLockController.acquire(
            "my_form.py", "sess-other", "other@example.com", "Other"
        )
        app = flask.Flask(__name__)
        with app.test_request_context():
            mcp_context.set_current_message_id("msg-1")
            self.controller.update_stage(
                self.stage.id, {"code_content": "print('ai write')"}
            )
        self.assertEqual(self._stage_code(), "print('ai write')")

    def test_stage_route_returns_423_when_locked(self) -> None:
        FileLockController.acquire(
            "my_form.py", "sess-other", "other@example.com", "Other"
        )
        client = self.get_editor_flask_client()
        response = client.put(
            f"/_editor/api/forms/{self.stage.id}",
            json={"code_content": "print('hacked')"},
        )
        self.assertEqual(response.status_code, 423)
        body = response.json or {}
        self.assertEqual(body.get("error"), "file_locked")
        self.assertEqual(body["holder"]["holderEmail"], "other@example.com")

    def test_stage_route_allows_holder_session(self) -> None:
        FileLockController.acquire("my_form.py", "tab-1", "local", "local")
        client = self.get_editor_flask_client()
        response = client.put(
            f"/_editor/api/forms/{self.stage.id}",
            json={"code_content": "print('mine')"},
            headers={"X-Abstra-Lock-Session-Id": "tab-1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self._stage_code(), "print('mine')")


class FileLockRoutesTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()
        FileLockController.reset_state()
        CodebaseEventController.listeners = []

    def tearDown(self) -> None:
        FileLockController.reset_state()
        CodebaseEventController.listeners = []
        super().tearDown()

    def test_get_locks_empty(self) -> None:
        response = self.client.get("/_editor/api/locks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"locks": []})

    def test_acquire_route_grants(self) -> None:
        response = self.client.post(
            "/_editor/api/locks/acquire",
            json={"filePath": "main.py", "sessionId": "sess-a"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json or {}
        self.assertTrue(body["granted"])
        self.assertIsNotNone(body["holder"])
        self.assertEqual(body["holder"]["filePath"], "main.py")

    def test_acquire_route_requires_fields(self) -> None:
        response = self.client.post(
            "/_editor/api/locks/acquire", json={"filePath": "main.py"}
        )
        self.assertEqual(response.status_code, 400)

    def test_release_route(self) -> None:
        self.client.post(
            "/_editor/api/locks/acquire",
            json={"filePath": "main.py", "sessionId": "sess-a"},
        )
        response = self.client.post(
            "/_editor/api/locks/release",
            json={"filePath": "main.py", "sessionId": "sess-a"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"released": True})

    def test_heartbeat_route(self) -> None:
        self.client.post(
            "/_editor/api/locks/acquire",
            json={"filePath": "main.py", "sessionId": "sess-a"},
        )
        response = self.client.post(
            "/_editor/api/locks/heartbeat",
            json={"filePath": "main.py", "sessionId": "sess-a"},
        )
        self.assertEqual(response.status_code, 200)
        body = response.json or {}
        self.assertTrue(body["stillHeld"])
        self.assertIsNotNone(body["lock"])

    def test_presence_routes(self) -> None:
        response = self.client.post(
            "/_editor/api/locks/presence/heartbeat",
            json={"sessionId": "sess-a", "currentFilePath": "main.py"},
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/_editor/api/locks/presence")
        self.assertEqual(response.status_code, 200)
        users = (response.json or {}).get("users", [])
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["sessionId"], "sess-a")
        self.assertEqual(users[0]["currentFilePath"], "main.py")

        response = self.client.post(
            "/_editor/api/locks/presence/leave", json={"sessionId": "sess-a"}
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/_editor/api/locks/presence")
        self.assertEqual((response.json or {}).get("users"), [])

    def test_presence_heartbeat_validates_session(self) -> None:
        response = self.client.post("/_editor/api/locks/presence/heartbeat", json={})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
