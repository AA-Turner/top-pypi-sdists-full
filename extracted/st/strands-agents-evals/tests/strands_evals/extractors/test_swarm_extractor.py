from unittest.mock import Mock

from strands_evals.extractors.swarm_extractor import (
    extract_swarm_handoffs,
    extract_swarm_interactions,
    extract_swarm_interactions_from_handoffs,
)


def test_swarm_extractor_extract_handoffs_with_handoff():
    """Test extracting handoffs from swarm result with handoff tool usage"""
    mock_swarm_result = Mock()
    mock_swarm_result.results = {
        "agent1": Mock(
            result=Mock(
                message={"content": [{"text": "Hello from agent1"}]},
                metrics=Mock(tool_metrics={"handoff_to_agent": Mock(tool={"input": {"agent_name": "agent2"}})}),
            )
        )
    }

    result = extract_swarm_handoffs(mock_swarm_result)

    assert len(result) == 1
    assert result[0]["from"] == "agent1"
    assert result[0]["to"] == "agent2"
    assert result[0]["messages"] == ["Hello from agent1"]


def test_swarm_extractor_extract_handoffs_without_handoff():
    """Test extracting handoffs from swarm result without handoff tool usage"""
    mock_swarm_result = Mock()
    mock_swarm_result.results = {
        "agent1": Mock(result=Mock(message={"content": [{"text": "Hello from agent1"}]}, metrics=Mock(tool_metrics={})))
    }

    result = extract_swarm_handoffs(mock_swarm_result)

    assert len(result) == 1
    assert result[0]["from"] == "agent1"
    assert result[0]["to"] is None
    assert result[0]["messages"] == ["Hello from agent1"]


def test_swarm_extractor_extract_handoffs_multiple_agents():
    """Test extracting handoffs from multiple agents"""
    mock_swarm_result = Mock()
    mock_swarm_result.results = {
        "agent1": Mock(
            result=Mock(
                message={"content": [{"text": "Message 1"}, {"text": "Message 2"}]},
                metrics=Mock(tool_metrics={"handoff_to_agent": Mock(tool={"input": {"agent_name": "agent2"}})}),
            )
        ),
        "agent2": Mock(result=Mock(message={"content": [{"text": "Final message"}]}, metrics=Mock(tool_metrics={}))),
    }

    result = extract_swarm_handoffs(mock_swarm_result)

    assert len(result) == 2
    assert result[0]["from"] == "agent1"
    assert result[0]["to"] == "agent2"
    assert result[0]["messages"] == ["Message 1", "Message 2"]
    assert result[1]["from"] == "agent2"
    assert result[1]["to"] is None
    assert result[1]["messages"] == ["Final message"]


def test_swarm_extractor_extract_handoffs_empty_result():
    """Test extracting handoffs from empty swarm result"""
    mock_swarm_result = Mock()
    mock_swarm_result.results = {}

    result = extract_swarm_handoffs(mock_swarm_result)

    assert result == []


def test_swarm_extractor_extract_interactions_from_handoffs():
    """Test converting handoffs to interactions format"""
    handoffs_info = [
        {"from": "agent1", "to": "agent2", "messages": ["Hello from agent1"]},
        {"from": "agent2", "to": None, "messages": ["Final message"]},
    ]

    result = extract_swarm_interactions_from_handoffs(handoffs_info)

    assert len(result) == 2
    assert result[0]["node_name"] == "agent1"
    assert result[0]["messages"] == ["Hello from agent1"]
    assert result[0]["dependencies"] == []
    assert result[1]["node_name"] == "agent2"
    assert result[1]["messages"] == ["Final message"]
    assert result[1]["dependencies"] == ["agent1"]


def test_swarm_extractor_extract_interactions_from_handoffs_complex():
    """Test converting complex handoffs to interactions format"""
    handoffs_info = [
        {"from": "agent1", "to": "agent2", "messages": ["Message 1"]},
        {"from": "agent2", "to": "agent3", "messages": ["Message 2"]},
        {"from": "agent3", "to": None, "messages": ["Message 3"]},
    ]

    result = extract_swarm_interactions_from_handoffs(handoffs_info)

    assert len(result) == 3
    assert result[0]["node_name"] == "agent1"
    assert result[0]["dependencies"] == []
    assert result[1]["node_name"] == "agent2"
    assert result[1]["dependencies"] == ["agent1"]
    assert result[2]["node_name"] == "agent3"
    assert result[2]["dependencies"] == ["agent2"]


def test_swarm_extractor_extract_interactions_from_handoffs_empty():
    """Test converting empty handoffs to interactions format"""
    result = extract_swarm_interactions_from_handoffs([])

    assert result == []


def test_swarm_extractor_extract_interactions():
    """Test extracting interactions directly from swarm result"""
    mock_swarm_result = Mock()
    mock_swarm_result.results = {
        "agent1": Mock(
            result=Mock(
                message={"content": [{"text": "Hello from agent1"}]},
                metrics=Mock(tool_metrics={"handoff_to_agent": Mock(tool={"input": {"agent_name": "agent2"}})}),
            )
        ),
        "agent2": Mock(result=Mock(message={"content": [{"text": "Final message"}]}, metrics=Mock(tool_metrics={}))),
    }

    result = extract_swarm_interactions(mock_swarm_result)

    assert len(result) == 2
    assert result[0]["node_name"] == "agent1"
    assert result[0]["messages"] == ["Hello from agent1"]
    assert result[0]["dependencies"] == []
    assert result[1]["node_name"] == "agent2"
    assert result[1]["messages"] == ["Final message"]
    assert result[1]["dependencies"] == ["agent1"]


def test_swarm_extractor_extract_interactions_empty():
    """Test extracting interactions from empty swarm result"""
    mock_swarm_result = Mock()
    mock_swarm_result.results = {}

    result = extract_swarm_interactions(mock_swarm_result)

    assert result == []
