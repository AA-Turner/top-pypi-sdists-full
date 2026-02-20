from unittest.mock import MagicMock, patch

from abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target import (
    MissingTaskSchemaForAgentTarget,
)


def _make_stage(id, title, task_schema=None):
    stage = MagicMock()
    stage.id = id
    stage.title = title
    stage.task_schema = task_schema
    return stage


def _make_transition(target_id):
    t = MagicMock()
    t.target_id = target_id
    return t


def _make_agent(title, transitions):
    agent = MagicMock()
    agent.title = title
    agent.workflow_transitions = transitions
    return agent


def _make_project(agents, stages_by_id):
    project = MagicMock()
    project.agents = agents
    project.get_stage = lambda id, **kw: stages_by_id.get(id)
    return project


class TestMissingTaskSchemaForAgentTarget:
    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_no_agents_no_issues(self, mock_repo_cls):
        mock_repo_cls.return_value.load.return_value = _make_project([], {})

        rule = MissingTaskSchemaForAgentTarget()
        issues = rule.find_issues()

        assert len(issues) == 0

    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_target_with_task_schema_no_issue(self, mock_repo_cls):
        target = _make_stage("s1", "Process Order", task_schema={"type": "object"})
        agent = _make_agent("Order Agent", [_make_transition("s1")])
        mock_repo_cls.return_value.load.return_value = _make_project(
            [agent], {"s1": target}
        )

        rule = MissingTaskSchemaForAgentTarget()
        issues = rule.find_issues()

        assert len(issues) == 0

    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_target_without_task_schema_raises_issue(self, mock_repo_cls):
        target = _make_stage("s1", "Process Order", task_schema=None)
        agent = _make_agent("Order Agent", [_make_transition("s1")])
        mock_repo_cls.return_value.load.return_value = _make_project(
            [agent], {"s1": target}
        )

        rule = MissingTaskSchemaForAgentTarget()
        issues = rule.find_issues()

        assert len(issues) == 1
        assert "Order Agent" in issues[0].label
        assert "Process Order" in issues[0].label

    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_target_with_empty_task_schema_raises_issue(self, mock_repo_cls):
        target = _make_stage("s1", "Process Order", task_schema={})
        agent = _make_agent("Order Agent", [_make_transition("s1")])
        mock_repo_cls.return_value.load.return_value = _make_project(
            [agent], {"s1": target}
        )

        rule = MissingTaskSchemaForAgentTarget()
        issues = rule.find_issues()

        assert len(issues) == 1

    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_multiple_agents_multiple_targets(self, mock_repo_cls):
        t1 = _make_stage("s1", "Stage A", task_schema={"type": "object"})
        t2 = _make_stage("s2", "Stage B", task_schema=None)
        t3 = _make_stage("s3", "Stage C", task_schema=None)

        agent1 = _make_agent(
            "Agent 1", [_make_transition("s1"), _make_transition("s2")]
        )
        agent2 = _make_agent("Agent 2", [_make_transition("s3")])

        mock_repo_cls.return_value.load.return_value = _make_project(
            [agent1, agent2], {"s1": t1, "s2": t2, "s3": t3}
        )

        rule = MissingTaskSchemaForAgentTarget()
        issues = rule.find_issues()

        assert len(issues) == 2

    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_transition_to_nonexistent_stage_ignored(self, mock_repo_cls):
        agent = _make_agent("Agent X", [_make_transition("deleted-stage-id")])
        mock_repo_cls.return_value.load.return_value = _make_project([agent], {})

        rule = MissingTaskSchemaForAgentTarget()
        issues = rule.find_issues()

        assert len(issues) == 0

    @patch(
        "abstra_internals.repositories.linter.rules.missing_task_schema_for_agent_target.LocalProjectRepository"
    )
    def test_check_returns_linter_check(self, mock_repo_cls):
        target = _make_stage("s1", "Target", task_schema=None)
        agent = _make_agent("My Agent", [_make_transition("s1")])
        mock_repo_cls.return_value.load.return_value = _make_project(
            [agent], {"s1": target}
        )

        rule = MissingTaskSchemaForAgentTarget()
        check = rule.check()

        assert check.name == "MissingTaskSchemaForAgentTarget"
        assert check.type == "warning"
        assert len(check.issues) == 1
