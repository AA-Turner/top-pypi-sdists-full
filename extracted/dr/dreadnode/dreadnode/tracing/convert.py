import typing as t

if t.TYPE_CHECKING:
    import networkx as nx

    from dreadnode.tracing.span import TaskSpan


def task_span_to_graph(task: "TaskSpan[t.Any]") -> "nx.DiGraph":
    """
    Convert a TaskSpan hierarchy to a networkx directed graph.

    Args:
        task: The root TaskSpan to convert.

    Returns:
        A networkx DiGraph representing the task hierarchy.
    """
    try:
        import networkx as nx
    except ImportError as e:
        raise RuntimeError(
            "The `networkx` package is required for graph conversion. Install with: pip install networkx"
        ) from e

    graph = nx.DiGraph()
    graph.add_node(
        task.task_id,
        name=task.name,
        label=task.label,
        start_time=task.start_time,
        end_time=task.end_time,
        duration=task.duration,
        status="failed" if task.failed else "running" if task.is_recording else "completed",
        tags=task.tags,
    )

    for child_task in task.all_tasks:
        graph.add_node(
            child_task.span_id,
            name=child_task.name,
            label=child_task.label,
            start_time=child_task.start_time,
            end_time=child_task.end_time,
            duration=child_task.duration,
            status="failed"
            if child_task.failed
            else "running"
            if child_task.active
            else "completed",
            tags=child_task.tags,
        )

        parent_id = child_task.parent_task.span_id if child_task.parent_task else task.task_id
        graph.add_edge(parent_id, child_task.span_id)

    return graph


# Backwards compatibility alias
run_span_to_graph = task_span_to_graph
