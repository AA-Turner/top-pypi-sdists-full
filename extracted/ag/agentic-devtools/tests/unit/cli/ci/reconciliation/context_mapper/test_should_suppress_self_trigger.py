from agentic_devtools.cli.ci.reconciliation.context_mapper import should_suppress_self_trigger


def test_should_suppress_self_trigger_detects_marker_or_identity() -> None:
    assert should_suppress_self_trigger(sender_login="", body="<!-- ai-pr-loop:generated -->")
    assert should_suppress_self_trigger(sender_login="BOT", self_identities=frozenset({"bot"}))
    assert not should_suppress_self_trigger(sender_login="human")
