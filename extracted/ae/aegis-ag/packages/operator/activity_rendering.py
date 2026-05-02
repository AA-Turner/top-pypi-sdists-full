"""Activity operator rendering helpers."""

from __future__ import annotations

from packages.contracts import GoalNode


def _activity_goal_line(goal: GoalNode) -> str:
    return f"{goal.goal_id} | {goal.status} | {goal.priority} | {goal.title}"


def render_activity_goal_tree_lines(goals: tuple[GoalNode, ...]) -> tuple[str, ...]:
    if not goals:
        return ("- <empty>",)

    goal_ids = {goal.goal_id for goal in goals}
    children_by_parent: dict[str, list[GoalNode]] = {goal.goal_id: [] for goal in goals}
    roots: list[GoalNode] = []
    for goal in goals:
        parent_goal_id = goal.parent_goal_id
        if parent_goal_id is not None and parent_goal_id in goal_ids and parent_goal_id != goal.goal_id:
            children_by_parent[parent_goal_id].append(goal)
        else:
            roots.append(goal)

    lines: list[str] = []
    visited: set[str] = set()

    def append_goal(goal: GoalNode, *, depth: int) -> None:
        if goal.goal_id in visited:
            return
        visited.add(goal.goal_id)
        lines.append(f"{'  ' * depth}- {_activity_goal_line(goal)}")
        for child in children_by_parent.get(goal.goal_id, ()):
            append_goal(child, depth=depth + 1)

    for root in roots:
        append_goal(root, depth=0)
    for goal in goals:
        append_goal(goal, depth=0)
    return tuple(lines)
