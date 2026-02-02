# pylint: skip-file
from unittest import mock

import pytest

from bec_lib.bl_checks import (
    BeamlineCheckError,
    BeamlineChecks,
    _run_on_failure,
    _run_with_bl_checks,
)


def test_run_with_bl_checks():
    bl_checks = mock.MagicMock()
    bl_checks._levels = []
    bl_checks._is_paused = False
    _run_with_bl_checks(bl_checks, mock.MagicMock(), 1, 2, 3, a=4, b=5)
    assert not bl_checks._levels


def test_bl_check_raises_on_failed_nested_calls():
    bl_checks = mock.MagicMock()
    bl_checks._levels = [{"fcn": mock.MagicMock()}]
    bl_checks._is_paused = False
    bl_checks.beam_is_okay = False
    with pytest.raises(BeamlineCheckError):
        _run_with_bl_checks(bl_checks, mock.MagicMock(), 1, 2, 3, a=4, b=5)


def test_bl_check_run_on_failure():
    bl_checks = mock.MagicMock()
    bl_checks._levels = []
    bl_checks._is_paused = False
    bl_checks.beam_is_okay = False
    fcn = mock.MagicMock()
    fcn.side_effect = BeamlineCheckError
    _run_on_failure(bl_checks, fcn, 1, 2, 3, a=4, b=5)
    bl_checks.wait_for_beamline_checks.assert_called_once()


def test_bl_check_register():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    condition = mock.MagicMock()
    condition.name = "test"
    bl_check.register(condition)
    assert bl_check.test == condition  # pylint: disable=no-member
    assert bl_check._beamline_checks["test"] == condition


def test_bl_check_pause():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check.pause()
    assert bl_check._is_paused


def test_bl_check_resume():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._is_paused = True
    bl_check.resume()
    assert not bl_check._is_paused


def test_bl_check_reset():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._beam_is_okay = False
    bl_check._check_msgs = ["test"]
    bl_check.reset()
    assert bl_check._beam_is_okay
    assert not bl_check._check_msgs


def test_bl_check_disable_check():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._beamline_checks = {"test": mock.MagicMock()}
    bl_check.disable_check("test")
    assert not bl_check._beamline_checks["test"].enabled


def test_bl_check_enable_check():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._beamline_checks = {"test": mock.MagicMock()}
    bl_check.enable_check("test")
    assert bl_check._beamline_checks["test"].enabled


def test_bl_check_disable_all_checks():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._beamline_checks = {"test": mock.MagicMock()}
    bl_check.disable_all_checks()
    assert not bl_check._beamline_checks["test"].enabled


def test_bl_check_enable_all_checks():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._beamline_checks = {"test": mock.MagicMock()}
    bl_check.enable_all_checks()
    assert bl_check._beamline_checks["test"].enabled


def test_bl_check_run_beamline_checks():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._beamline_checks = {"test": mock.MagicMock()}
    bl_check._beam_is_okay = True
    bl_check._run_beamline_checks()
    assert bl_check._beam_is_okay
    bl_check._beamline_checks["test"].run.assert_called_once()
    bl_check._beamline_checks["test"].on_failure_msg.assert_not_called()


def test_bl_check_send_to_scilog():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._send_to_scilog("test")
    client.logbook.send_logbook_message.assert_called_once()


def test_bl_check_beam_status_is_okay():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    with mock.patch.object(bl_check, "_run_beamline_checks") as mock_run:
        mock_run.return_value = []
        assert bl_check._beam_status_is_okay() is True


def test_bl_check_wait_for_beamline_checks():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._check_msgs = ["test"]
    bl_check._beam_is_okay = False
    with mock.patch.object(bl_check, "_print_beamline_checks") as mock_print:
        with mock.patch.object(bl_check, "_send_to_scilog") as mock_send:
            with mock.patch.object(bl_check, "_run_beamline_checks") as mock_run:
                mock_run.return_value = ["test"]
                bl_check.wait_for_beamline_checks()
                mock_print.assert_called_once()
                mock_send.assert_called()


def test_bl_check_start():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._started = False
    bl_check._beam_is_okay = True
    with mock.patch("bec_lib.bl_checks.threading.Thread") as mock_thread:
        bl_check.start()
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()


def test_bl_check_stop():
    client = mock.MagicMock()
    bl_check = BeamlineChecks(client=client)
    bl_check._started = True
    bl_check._beam_is_okay = True
    bl_check._beam_check_thread = mock.MagicMock()
    bl_check.stop()
    bl_check._beam_check_thread.join.assert_called_once()
