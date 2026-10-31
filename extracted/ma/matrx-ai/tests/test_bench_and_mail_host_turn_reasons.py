"""Host-turn reasons the aidream host writes are registered, so the Model view can name them (wave 16)."""

from matrx_ai.config.platform_parts import host_turn_reason_registered


def test_host_written_turns_are_registered() -> None:
    for reason in ("agent_mail", "bench_search_results", "platform_repair"):
        assert host_turn_reason_registered(reason), reason
    assert not host_turn_reason_registered("not_a_reason")
