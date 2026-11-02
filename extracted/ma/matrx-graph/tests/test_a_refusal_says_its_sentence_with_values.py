"""A Safety Check's refusal is the author's sentence, filled from the step's inputs.

Live 2026-10-27 ("Ensure material" → "enough material"): the refusal showed the
check's predicate code and could not say how thin the material was. The message
now fills ``{path}`` placeholders from the inputs (the shared template language,
``:n`` groups a number only when the template asks) and the predicate is technical detail only.
"""

from __future__ import annotations

from matrx_graph import Definition, MemoryCheckpointer, NodeRegistry, RunStatus, Scheduler, compile_graph
from matrx_graph.nodes import register_builtin_nodes

from tests._fixtures import make_app_context


async def test_the_refusal_names_the_values_and_hides_the_code() -> None:
    registry = register_builtin_nodes(NodeRegistry())
    defn = Definition.model_validate(
        {
            "nodes": [
                {
                    "id": "enough",
                    "type": "data.assert",
                    "position": {"x": 0, "y": 0},
                    "data": {
                        "config": {
                            "predicate": "int(inputs['material']['total_chars']) >= int(inputs['min_chars'])",
                            "message": "Too thin: {material.total_chars} characters read, {min_chars:n} needed (checked {year}).",
                        }
                    },
                }
            ],
            "edges": [],
        }
    )
    graph = compile_graph(defn, registry=registry)
    result = await Scheduler(graph, MemoryCheckpointer(), make_app_context(), registry=registry).run(
        run_id="t-refusal", inputs={"material": {"total_chars": 58}, "min_chars": 1000, "year": 2026}
    )
    assert result.status is RunStatus.ERRORED
    failure = result.failure
    assert failure is not None
    shown = failure.message
    assert shown == "Too thin: 58 characters read, 1,000 needed (checked 2026)."  # grouping only when asked
    assert "predicate" not in shown and "inputs[" not in shown
    assert "assertion_failed" not in shown
