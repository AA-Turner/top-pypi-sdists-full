"""Dedicated /activity and /audit shell handlers kept out of the large command file."""

from __future__ import annotations

from packages.operator import render_activity_lines, render_audit_lines


def _append_work(self, args: list[str]) -> None:
    action = args[0] if args else "inspect"
    surface = self.runtime.inspect_activity_surface(self.session_id)
    if action in {"inspect", "show", "list", "ls"} and len(args) <= 1:
        lines = list(render_activity_lines(surface))
        lines.extend(
            [
                "",
                "create: /activity create <title>",
                "inspect: /activity inspect <goal-id>",
                "focus: /activity focus <goal-id>",
                "drop: /activity drop <goal-id>",
            ]
        )
        self._append_entry("notice", "Activity", "\n".join(lines))
        return
    if action == "inspect":
        if len(args) < 2:
            self._append_entry("recovery", "Activity", "Usage: /activity inspect <goal-id>")
            return
        goal = self.runtime.inspect_goal(self.session_id, args[1])
        lines = [
            f"id: {goal.goal_id}",
            f"title: {goal.title}",
            f"status: {goal.status}",
            f"priority: {goal.priority}",
            f"owner: {goal.owner or 'none'}",
            f"parent: {goal.parent_goal_id or 'none'}",
            f"dependencies: {', '.join(goal.dependencies) or 'none'}",
            f"evidence: {', '.join(goal.evidence_refs) or 'none'}",
        ]
        self._append_entry("notice", "Activity item", "\n".join(lines))
        return
    if action == "create":
        title = " ".join(args[1:]).strip()
        if not title:
            self._append_entry("recovery", "Activity", "Usage: /activity create <title>")
            return
        goal = self.runtime.create_goal(self.session_id, title=title)
        self._append_entry("notice", "Activity item created", f"{goal.goal_id} | {goal.status} | {goal.priority} | {goal.title}")
        return
    if action == "focus":
        if len(args) < 2:
            self._append_entry("recovery", "Activity", "Usage: /activity focus <goal-id>")
            return
        _, updated, reason = self.runtime.update_goal(
            self.session_id,
            args[1],
            status="active",
            reason="activity focused from /activity surface",
        )
        self._append_entry("notice", "Activity item focused", f"{reason}: {updated.goal_id} | {updated.status} | {updated.priority} | {updated.title}")
        return
    if action in {"drop", "delete"}:
        if len(args) < 2:
            self._append_entry("recovery", "Activity", "Usage: /activity drop <goal-id>")
            return
        _, updated = self.runtime.delete_goal(
            self.session_id,
            args[1],
            reason="activity dropped from /activity surface",
        )
        self._append_entry("notice", "Activity item dropped", f"{updated.goal_id} | {updated.status} | {updated.priority} | {updated.title}")
        return
    self._append_entry("recovery", "Activity", "Usage: /activity [inspect|create|focus|drop]")


def _append_audit(self, args: list[str]) -> None:
    audit = self.runtime.inspect_audit_surface(self.session_id)
    lines = list(render_audit_lines(audit))
    if args and args[0] == "prompt":
        lines.extend(("", "rendered_prompt:", audit.rendered_prompt))
    else:
        first_line = audit.rendered_prompt.splitlines()[0] if audit.rendered_prompt else "<empty>"
        lines.append("")
        lines.append(f"rendered_prompt_preview: {first_line}")
        lines.append("full prompt: /audit prompt")
    self._append_entry("notice", "Audit", "\n".join(lines))
