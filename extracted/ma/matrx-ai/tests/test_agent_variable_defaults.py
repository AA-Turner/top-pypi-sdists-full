"""Saved Agent Builder variable defaults must execute without a client fill."""

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.unified_config import UnifiedConfig

FILE_ID = "550e8400-e29b-41d4-a716-446655440000"


def _agent(*, default: str = FILE_ID, explicit: str | None = None) -> Agent:
    config = UnifiedConfig.from_dict(
        {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "url": "{{current_file}}",
                            "mime_type": "application/pdf",
                        }
                    ],
                }
            ],
        }
    )
    agent = Agent(
        config=config,
        variable_defaults={
            "current_file": AgentVariable(
                name="current_file", default_value=default
            )
        },
    )
    if explicit is not None:
        agent.set_variable("current_file", explicit)
    return agent


def test_agent_applies_saved_file_id_default_without_caller_variables() -> None:
    agent = _agent()

    agent.apply_variables()

    document = agent.config.messages[0].content[0]
    assert document.file_id == FILE_ID
    assert document.url is None


def test_explicit_file_id_overrides_saved_default() -> None:
    explicit = "660e8400-e29b-41d4-a716-446655440000"
    agent = _agent(explicit=explicit)

    agent.apply_variables()

    document = agent.config.messages[0].content[0]
    assert document.file_id == explicit
    assert document.url is None


def test_historical_literal_uuid_in_url_is_coerced_to_file_id() -> None:
    """The old Agent Builder stored selected files in the URL field.

    Keep this compatibility lane while the UI/migration upgrades definitions to
    the canonical file_id shape.
    """
    config = UnifiedConfig.from_dict(
        {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "document", "url": FILE_ID}],
                }
            ],
        }
    )

    config.replace_variables({})

    document = config.messages[0].content[0]
    assert document.file_id == FILE_ID
    assert document.url is None
