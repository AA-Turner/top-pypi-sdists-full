"""Flowtask Factory — natural-language to Flowtask YAML.

This package hosts the orchestrator agent and its supporting infrastructure:

* :mod:`parser`     — pure YAML walker that produces a :class:`ParsedTask`
                      from raw text. No schema validation, no execution.
* :mod:`validator`  — validates a :class:`ParsedTask` against the JSON
                      schemas shipped under
                      ``flowtask/documentation/generated/components/``.
* :mod:`composer`   — DAG sketch + YAML rendering (added in a later step).
* :mod:`agent`      — ReAct-style orchestrator built on ai-parrot (added
                      in a later step).

Public API expands as each module lands. For now only the parser and
validator surfaces are stable.
"""
from .composer import (
    BoundNode,
    CandidateComponent,
    ComposedTask,
    ComposerError,
    DagComposer,
    DagNode,
    DagSketch,
    SketchedNode,
)
from .parser import (
    ParsedStep,
    ParsedTask,
    ParserError,
    YamlTaskParser,
)
from .validator import (
    FlowtaskSchemaValidator,
    ValidationIssue,
    ValidationReport,
)


def __getattr__(name: str):
    """Lazy import for the agent — keeps `flowtask.factory` cheap to import.

    ``FlowtaskBuilderAgent`` pulls in ai-parrot's runtime (BasicAgent,
    Chatbot, Google GenAI client, ...). Anything that only needs the parser
    / validator / composer should avoid paying that cost. Importing through
    this lazy hook keeps backward-compatible explicit imports working
    (``from flowtask.factory import FlowtaskBuilderAgent``) without forcing
    every consumer of the factory to install ai-parrot.
    """
    if name == "FlowtaskBuilderAgent":
        from .agent import FlowtaskBuilderAgent

        return FlowtaskBuilderAgent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BoundNode",
    "CandidateComponent",
    "ComposedTask",
    "ComposerError",
    "DagComposer",
    "DagNode",
    "DagSketch",
    "FlowtaskBuilderAgent",
    "FlowtaskSchemaValidator",
    "ParsedStep",
    "ParsedTask",
    "ParserError",
    "SketchedNode",
    "ValidationIssue",
    "ValidationReport",
    "YamlTaskParser",
]
