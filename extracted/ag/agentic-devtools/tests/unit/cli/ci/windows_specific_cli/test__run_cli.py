"""Tests for the Windows-specific command entry point."""

from unittest.mock import Mock

from agentic_devtools.cli.ci import windows_specific_cli


def test_run_cli_constructs_dispatcher_and_forwards_arguments(monkeypatch):
    argv = ["gate", "--selection-json", "{}"]
    callbacks = (Mock(), Mock(), Mock(), Mock())
    dispatcher = Mock()
    dispatcher.run.return_value = 23
    dispatcher_factory = Mock(return_value=dispatcher)
    monkeypatch.setattr(windows_specific_cli, "_Dispatcher", dispatcher_factory, raising=False)

    status = windows_specific_cli._run_cli(
        argv,
        load_policy=callbacks[0],
        select_groups=callbacks[1],
        run_selected_tests=callbacks[2],
        evaluate_gate=callbacks[3],
    )

    assert status == 23
    dispatcher_factory.assert_called_once_with(*callbacks)
    dispatcher.run.assert_called_once_with(argv)
