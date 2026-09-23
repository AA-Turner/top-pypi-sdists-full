"""A variable written inside a Questions part is filled at run time.

THE BREAK THIS CATCHES: ``UnifiedMessage.replace_variables`` substitutes only
content classes that carry ``replace_variables``. ``DecisionQuestionsContent``
had none, so an author who wrote "Is this a defect on {{route}}?" sent Jev the
literal braces while the text part beside it read the real page. Typed-messages
FEATURE.md: every string field of a part is a slot.

The path under test is the real one: stored agent JSON -> ``UnifiedMessage.from_dict``
-> ``UnifiedConfig.replace_variables`` -> the translator's ``to_prose`` / ``typed``.
"""

from __future__ import annotations

from matrx_ai.config.decision_input_config import DecisionQuestionsContent
from matrx_ai.config.message_config import UnifiedMessage
from matrx_ai.config.unified_config import UnifiedConfig

# One inbound feedback item for AI Matrx itself, shaped exactly as the
# "Feedback triage" agent stores it.
_USER_MESSAGE = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Filed as: {{filed_type}}\nPage: {{route}}\n\n{{description}}"},
        {
            "type": "decision_questions",
            "__kind": "decision_questions",
            "questions": [
                {
                    "name": "is_defect",
                    "type": "noul",
                    "instructions": "Is this a defect on {{route}} rather than a request for new behaviour?",
                    "criteria": {"true": "existing behaviour on {{route}} is wrong", "false": "new behaviour is wanted"},
                },
                {
                    "name": "owning_surface",
                    "type": "choice",
                    "instructions": "Which surface owns this {{filed_type}}?",
                    "criteria": {"frontend": "the browser UI", "server": "the Python API", "unclear": "cannot tell"},
                },
                {
                    "name": "urgency",
                    "type": "score",
                    "instructions": "How urgent is this?",
                    "criteria": ["cosmetic", "blocks {{route}}", "data at risk"],
                },
            ],
        },
    ],
}

_VALUES = {
    "route": "https://aimatrx.com/data-v2",
    "filed_type": "bug",
    "description": "Every quote card on the Kanban board stays on Loading.",
}


def _questions_part(config: UnifiedConfig) -> DecisionQuestionsContent:
    parts = [p for m in config.messages for p in m.content if isinstance(p, DecisionQuestionsContent)]
    assert len(parts) == 1, "the stored Questions part must parse to DecisionQuestionsContent"
    return parts[0]


def test_variables_inside_questions_are_filled_through_the_config_door():
    config = UnifiedConfig(model="jev-1.13", messages=[UnifiedMessage.from_dict(_USER_MESSAGE)])

    config.replace_variables(_VALUES)

    typed = _questions_part(config).typed()
    by_name = {q.name: q for q in typed.questions}
    assert by_name["is_defect"].instructions == (
        "Is this a defect on https://aimatrx.com/data-v2 rather than a request for new behaviour?"
    )
    assert by_name["is_defect"].criteria["true"] == "existing behaviour on https://aimatrx.com/data-v2 is wrong"
    assert by_name["owning_surface"].instructions == "Which surface owns this bug?"
    assert by_name["urgency"].score_levels()[1] == "blocks https://aimatrx.com/data-v2"
    assert "{{" not in _questions_part(config).to_prose()


def test_identifiers_are_never_slots():
    """A variable can fill what is asked, never rename what comes back."""
    part = DecisionQuestionsContent(
        questions=[
            {
                "name": "surface",
                "type": "choice",
                "instructions": "Which surface?",
                "criteria": {"{{route}}": "the page", "server": "the API"},
            }
        ]
    )

    assert part.replace_variables({"route": "frontend"}) is False
    assert part.questions[0]["name"] == "surface"
    assert list(part.questions[0]["criteria"]) == ["{{route}}", "server"]


def test_the_text_part_beside_it_is_still_filled():
    message = UnifiedMessage.from_dict(_USER_MESSAGE)
    message.replace_variables(_VALUES)

    text = message.content[0].text
    assert "https://aimatrx.com/data-v2" in text and "{{" not in text
