from unittest import TestCase
from unittest.mock import patch

from abstra_internals.controllers.editor_status_events import (
    EditorStatusEventController,
)

_MOD = "abstra_internals.controllers.editor_status_events"


class HasListenersTest(TestCase):
    def tearDown(self):
        EditorStatusEventController.listeners = []

    def test_false_without_listeners(self):
        EditorStatusEventController.listeners = []
        self.assertFalse(EditorStatusEventController.has_listeners())

    def test_true_with_a_listener(self):
        EditorStatusEventController.listeners = [object()]  # type: ignore[list-item]
        self.assertTrue(EditorStatusEventController.has_listeners())


class RegisterConnectCheckTest(TestCase):
    def tearDown(self):
        EditorStatusEventController.listeners = []

    def test_first_listener_triggers_version_check(self):
        EditorStatusEventController.listeners = []
        with patch.object(
            EditorStatusEventController, "_check_version_on_connect"
        ) as check:
            EditorStatusEventController.register(object())  # type: ignore[arg-type]

        check.assert_called_once()

    def test_additional_listener_does_not_trigger_check(self):
        EditorStatusEventController.listeners = [object()]  # type: ignore[list-item]
        with patch.object(
            EditorStatusEventController, "_check_version_on_connect"
        ) as check:
            EditorStatusEventController.register(object())  # type: ignore[arg-type]

        check.assert_not_called()


class BuildPayloadTest(TestCase):
    def test_builds_valid_payload_with_all_contract_fields(self):
        # Guards against a contract field being added without build_payload
        # being updated (which raises at runtime and breaks the ws).
        import json

        payload = json.loads(EditorStatusEventController.build_payload())

        self.assertEqual(
            sorted(payload.keys()), ["restart_status", "update", "version"]
        )
        self.assertIn("deferred", payload["update"])
        self.assertIn("required", payload["restart_status"])


class RefreshAndBroadcastTest(TestCase):
    def test_broadcasts_when_availability_changes(self):
        states = [
            {"available": False, "label": "", "restarts": False},
            {"available": True, "label": "9.9.9", "restarts": True},
        ]
        with (
            patch(f"{_MOD}.EditorUpdateController.state", side_effect=states),
            patch(f"{_MOD}.EditorUpdateController.refresh") as refresh,
            patch(
                f"{_MOD}.EditorUpdateController.auto_stage_if_needed",
                return_value=False,
            ),
            patch.object(EditorStatusEventController, "broadcast") as broadcast,
        ):
            changed = EditorStatusEventController.refresh_and_broadcast()

        self.assertTrue(changed)
        refresh.assert_called_once_with(revalidate=True)
        broadcast.assert_called_once()

    def test_broadcasts_when_slot_staged_even_if_availability_unchanged(self):
        # A version detected on a previous tick may only get auto-staged now;
        # restart_status changes, so we must broadcast even if update state is same.
        same = {"available": True, "label": "9.9.9", "restarts": False}
        with (
            patch(
                f"{_MOD}.EditorUpdateController.state", side_effect=[same, dict(same)]
            ),
            patch(f"{_MOD}.EditorUpdateController.refresh"),
            patch(
                f"{_MOD}.EditorUpdateController.auto_stage_if_needed", return_value=True
            ),
            patch.object(EditorStatusEventController, "broadcast") as broadcast,
        ):
            changed = EditorStatusEventController.refresh_and_broadcast()

        self.assertTrue(changed)
        broadcast.assert_called_once()

    def test_does_not_broadcast_when_nothing_changed(self):
        same = {"available": False, "label": "", "restarts": False}
        with (
            patch(
                f"{_MOD}.EditorUpdateController.state", side_effect=[same, dict(same)]
            ),
            patch(f"{_MOD}.EditorUpdateController.refresh") as refresh,
            patch(
                f"{_MOD}.EditorUpdateController.auto_stage_if_needed",
                return_value=False,
            ),
            patch.object(EditorStatusEventController, "broadcast") as broadcast,
        ):
            changed = EditorStatusEventController.refresh_and_broadcast()

        self.assertFalse(changed)
        refresh.assert_called_once_with(revalidate=True)
        broadcast.assert_not_called()
