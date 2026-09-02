"""Report-rendering tests: human-readable summary, unknown handling."""

from __future__ import annotations

from runlayer_cli.scan.agents.detect import (
    DiscoveredAgent,
    Evidence,
    METHOD_STATIC,
)
from runlayer_cli.scan.agents.report import format_summary


def _agent(name, fw, lang, conf, method=METHOD_STATIC):
    return DiscoveredAgent(
        location=f"/x/{name}",
        name=name,
        framework_id=fw,
        display_name=fw.title() if fw else None,
        language=lang,
        confidence=conf,
        margin=0.9,
        score=9.0,
        runner_up=None,
        runner_up_score=0.0,
        detection_method=method,
        evidence=[Evidence("package_dep", "langchain", "pyproject.toml")] if fw else [],
        manifests=["pyproject.toml"],
        languages=[lang] if lang else [],
        agent_fingerprint="f" * 64 if fw else None,
    )


def test_format_summary_human_readable():
    detections = [_agent("a", "langchain", "Python", 0.9)]
    text = format_summary(detections)
    assert "1 agent(s)" in text
    assert "Langchain" in text


def test_format_summary_no_agents():
    text = format_summary([_agent("u", None, None, 0.0)])
    assert "no agents detected" in text
