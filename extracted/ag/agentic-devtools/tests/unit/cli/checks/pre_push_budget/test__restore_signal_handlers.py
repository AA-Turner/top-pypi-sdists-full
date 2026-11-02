from agentic_devtools.cli.checks.pre_push_budget import _restore_signal_handlers


def test_empty_restoration_is_a_noop():
    _restore_signal_handlers([], None)
