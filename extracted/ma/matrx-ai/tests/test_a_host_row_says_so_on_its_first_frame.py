"""A host-written user row (a builder's launch or fix round) carries its host flags on its reservation frame, so the
live transcript hides it instead of drawing "This message has no displayable text." (med-concierge 2026-11-12)."""

from matrx_ai.config.message_config import host_authored_user_turn, person_authored_user_turn
from matrx_ai.orchestrator.executor import user_frame_host_flags


def test_a_host_turn_names_its_author_and_that_the_person_never_sees_it() -> None:
    flags = user_frame_host_flags(host_authored_user_turn("Fix only that.", reason="applets.build fix round"))
    assert flags == {"authored_by": "host", "authored_reason": "applets.build fix round", "is_visible_to_user": False}


def test_the_persons_own_turn_carries_no_host_flag() -> None:
    assert user_frame_host_flags(person_authored_user_turn("Make it blue")) == {}
