"""Integration tests for AgentStage at the Project and MainController level.

Tests persistence, serialization, workflow_stages, delete_stage, and
interactions with the project repository (save/load cycles).
"""

import json
import unittest
from pathlib import Path

from abstra_internals.repositories.project.project import (
    AgentPermission,
    AgentStage,
    FormStage,
    NotificationTrigger,
    ScriptStage,
    WorkflowTransition,
)
from tests.fixtures import BaseTest


class TestAgentProjectPersistence(BaseTest):
    """Test that agents survive save/load cycles through the project repository."""

    def test_save_and_load_empty_agents(self):
        project = self.repositories.project.load()
        self.assertEqual(len(project.agents), 0)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        self.assertEqual(len(reloaded.agents), 0)

    def test_save_and_load_single_agent(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(
            title="Test Agent",
            file="test.md",
            id="agent-1",
            workflow_position=(100, 200),
        )
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        self.assertEqual(len(reloaded.agents), 1)
        self.assertEqual(reloaded.agents[0].id, "agent-1")
        self.assertEqual(reloaded.agents[0].title, "Test Agent")
        self.assertEqual(reloaded.agents[0].file, "test.md")
        self.assertEqual(reloaded.agents[0].workflow_position, (100, 200))

    def test_save_and_load_agent_with_permissions(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(
            title="Agent With Perms",
            file="perms.md",
            id="agent-perms",
            permissions=[
                AgentPermission(type="tables", action="select", table_name="users"),
                AgentPermission(type="files", action="read"),
                AgentPermission(
                    type="connections",
                    action="execute",
                    connection_name="my_db",
                ),
            ],
        )
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        loaded_agent = reloaded.get_agent("agent-perms")
        self.assertIsNotNone(loaded_agent)
        self.assertEqual(len(loaded_agent.permissions), 3)
        self.assertEqual(loaded_agent.permissions[0].type, "tables")
        self.assertEqual(loaded_agent.permissions[0].table_name, "users")
        self.assertEqual(loaded_agent.permissions[1].type, "files")
        self.assertEqual(loaded_agent.permissions[1].action, "read")
        self.assertEqual(loaded_agent.permissions[2].connection_name, "my_db")

    def test_save_and_load_agent_with_transitions(self):
        project = self.repositories.project.load()
        # Create a target script so transitions are valid
        script = ScriptStage(
            id="script-1",
            file="script.py",
            title="Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        project.scripts.append(script)

        agent = AgentStage.create(
            title="Agent With Transitions",
            file="trans.md",
            id="agent-trans",
        )
        agent.workflow_transitions = [
            WorkflowTransition(
                id="t1",
                target_id="script-1",
                target_type="scripts",
                type="task",
                task_type="completed",
            ),
        ]
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        loaded_agent = reloaded.get_agent("agent-trans")
        self.assertEqual(len(loaded_agent.workflow_transitions), 1)
        self.assertEqual(loaded_agent.workflow_transitions[0].task_type, "completed")

    def test_save_and_load_multiple_agents(self):
        project = self.repositories.project.load()
        for i in range(5):
            agent = AgentStage.create(
                title=f"Agent {i}",
                file=f"agent_{i}.md",
                id=f"agent-{i}",
            )
            project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        self.assertEqual(len(reloaded.agents), 5)
        ids = {a.id for a in reloaded.agents}
        for i in range(5):
            self.assertIn(f"agent-{i}", ids)

    def test_save_and_load_agent_with_all_fields(self):
        project = self.repositories.project.load()

        # Add a target script so the transition is not orphaned
        target_script = ScriptStage(
            id="next",
            file="next.py",
            title="Next Script",
            workflow_position=(500, 400),
            workflow_transitions=[],
        )
        project.scripts.append(target_script)

        agent = AgentStage.create(
            title="Full Agent",
            file="full.md",
            id="agent-full",
            workflow_position=(300, 400),
            permissions=[
                AgentPermission(
                    type="tables",
                    action="insert",
                    table_name="logs",
                    condition={"column": "status", "value": "active"},
                ),
            ],
        )
        agent.input = True
        agent.output = True
        agent.workflow_transitions = [
            WorkflowTransition(
                id="t1", target_id="next", target_type="scripts", type="task"
            )
        ]
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        loaded = reloaded.get_agent("agent-full")
        self.assertEqual(loaded.title, "Full Agent")
        self.assertEqual(loaded.file, "full.md")
        self.assertEqual(loaded.workflow_position, (300, 400))
        self.assertTrue(loaded.input)
        self.assertTrue(loaded.output)
        self.assertEqual(len(loaded.permissions), 1)
        self.assertEqual(
            loaded.permissions[0].condition, {"column": "status", "value": "active"}
        )
        self.assertEqual(len(loaded.workflow_transitions), 1)


class TestAgentInWorkflowStages(BaseTest):
    """Test that agents appear correctly in workflow_stages and related operations."""

    def test_agent_appears_in_workflow_stages(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(title="WF Agent", file="wf.md", id="agent-wf")
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        stage_ids = [s.id for s in reloaded.workflow_stages]
        self.assertIn("agent-wf", stage_ids)

    def test_agent_coexists_with_other_stages_in_workflow(self):
        project = self.repositories.project.load()

        form = FormStage(
            id="form-1",
            path="form1",
            title="Form",
            file="form.py",
            workflow_position=(0, 0),
            workflow_transitions=[],
            notification_trigger=NotificationTrigger(
                variable_name="val", enabled=False
            ),
        )
        script = ScriptStage(
            id="script-1",
            file="script.py",
            title="Script",
            workflow_position=(100, 0),
            workflow_transitions=[],
        )
        agent = AgentStage.create(title="Agent", file="agent.md", id="agent-1")

        project.forms.append(form)
        project.scripts.append(script)
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        stage_ids = {s.id for s in reloaded.workflow_stages}
        self.assertIn("form-1", stage_ids)
        self.assertIn("script-1", stage_ids)
        self.assertIn("agent-1", stage_ids)
        self.assertEqual(len(reloaded.workflow_stages), 3)

    def test_get_stage_returns_agent(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(
            title="Findable Agent", file="find.md", id="agent-find"
        )
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        stage = reloaded.get_stage("agent-find")
        self.assertIsNotNone(stage)
        self.assertIsInstance(stage, AgentStage)
        self.assertEqual(stage.title, "Findable Agent")

    def test_get_initial_stages_includes_agent(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(
            title="Initial Agent", file="init.md", id="agent-init"
        )
        agent.is_initial = True
        project.add_stage(agent)
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        initial_stages = reloaded.get_initial_stages()
        initial_ids = [s.id for s in initial_stages]
        self.assertIn("agent-init", initial_ids)


class TestAgentDeleteStage(BaseTest):
    """Test deleting agents from the project."""

    def test_delete_agent(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(title="Delete Me", file="delete.md", id="agent-del")
        project.add_stage(agent)
        self.repositories.project.save(project)

        project = self.repositories.project.load()
        self.assertEqual(len(project.agents), 1)

        project.delete_stage("agent-del")
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        self.assertEqual(len(reloaded.agents), 0)
        self.assertIsNone(reloaded.get_agent("agent-del"))

    def test_delete_agent_does_not_affect_other_agents(self):
        project = self.repositories.project.load()
        for i in range(3):
            agent = AgentStage.create(
                title=f"Agent {i}", file=f"agent_{i}.md", id=f"agent-{i}"
            )
            project.add_stage(agent)
        self.repositories.project.save(project)

        project = self.repositories.project.load()
        project.delete_stage("agent-1")
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        self.assertEqual(len(reloaded.agents), 2)
        ids = {a.id for a in reloaded.agents}
        self.assertIn("agent-0", ids)
        self.assertIn("agent-2", ids)
        self.assertNotIn("agent-1", ids)

    def test_delete_agent_does_not_affect_other_stage_types(self):
        project = self.repositories.project.load()
        form = FormStage(
            id="form-1",
            path="form1",
            title="Form",
            file="form.py",
            workflow_position=(0, 0),
            workflow_transitions=[],
            notification_trigger=NotificationTrigger(
                variable_name="val", enabled=False
            ),
        )
        agent = AgentStage.create(title="Agent", file="agent.md", id="agent-1")
        project.forms.append(form)
        project.add_stage(agent)
        self.repositories.project.save(project)

        project = self.repositories.project.load()
        project.delete_stage("agent-1")
        self.repositories.project.save(project)

        reloaded = self.repositories.project.load()
        self.assertEqual(len(reloaded.agents), 0)
        self.assertEqual(len(reloaded.forms), 1)
        self.assertEqual(reloaded.forms[0].id, "form-1")


class TestMainControllerAgents(BaseTest):
    """Test MainController methods for agents."""

    def test_create_agent(self):
        agent = self.controller.create_agent("My Agent", "my_agent.md")
        self.assertEqual(agent.title, "My Agent")
        self.assertEqual(agent.file, "my_agent.md")
        self.assertTrue(len(agent.id) > 0)

    def test_create_agent_writes_template_file(self):
        agent = self.controller.create_agent("Agent", "agent.md")
        file_path = Path(agent.file)
        self.assertTrue(file_path.exists())
        content = file_path.read_text(encoding="utf-8")
        self.assertIn("trigger_task", content)

    def test_create_agent_with_custom_id(self):
        agent = self.controller.create_agent("Agent", "agent.md", id="custom-123")
        self.assertEqual(agent.id, "custom-123")

    def test_create_agent_with_position(self):
        agent = self.controller.create_agent(
            "Agent", "agent.md", workflow_position=(100, 200)
        )
        self.assertEqual(agent.workflow_position, (100, 200))

    def test_get_agents_empty(self):
        agents = self.controller.get_agents()
        self.assertEqual(len(agents), 0)

    def test_get_agents_returns_sorted(self):
        self.controller.create_agent("Zebra", "z.md")
        self.controller.create_agent("Alpha", "a.md")
        self.controller.create_agent("Middle", "m.md")

        agents = self.controller.get_agents()
        self.assertEqual(len(agents), 3)
        self.assertEqual(agents[0].title, "Alpha")
        self.assertEqual(agents[1].title, "Middle")
        self.assertEqual(agents[2].title, "Zebra")

    def test_get_agent_by_id(self):
        created = self.controller.create_agent("Agent", "agent.md", id="agent-123")
        found = self.controller.get_agent("agent-123")
        self.assertIsNotNone(found)
        self.assertEqual(found.id, created.id)
        self.assertEqual(found.title, "Agent")

    def test_get_agent_nonexistent(self):
        found = self.controller.get_agent("nonexistent")
        self.assertIsNone(found)

    def test_update_stage_title(self):
        self.controller.create_agent("Old Title", "agent.md", id="agent-update")
        self.controller.update_stage("agent-update", {"title": "New Title"})
        updated = self.controller.get_agent("agent-update")
        self.assertEqual(updated.title, "New Title")

    def test_update_stage_permissions(self):
        self.controller.create_agent("Agent", "agent.md", id="agent-perms")
        self.controller.update_stage(
            "agent-perms",
            {
                "permissions": [
                    {"type": "tables", "action": "select", "tableName": "users"},
                    {"type": "files", "action": "write"},
                ]
            },
        )
        updated = self.controller.get_agent("agent-perms")
        self.assertEqual(len(updated.permissions), 2)
        self.assertEqual(updated.permissions[0].table_name, "users")

    def test_update_stage_prompt_content(self):
        agent = self.controller.create_agent("Agent", "agent.md", id="agent-prompt")
        new_prompt = "Custom prompt: {{ trigger_task.type }}"
        self.controller.update_stage("agent-prompt", {"prompt_content": new_prompt})

        # Verify the file was updated
        from abstra_internals.settings import Settings

        file_path = Settings.root_path / agent.file
        content = file_path.read_text(encoding="utf-8")
        self.assertEqual(content, new_prompt)

    def test_update_stage_input_output(self):
        self.controller.create_agent("Agent", "agent.md", id="agent-io")
        self.controller.update_stage("agent-io", {"input": True, "output": True})
        updated = self.controller.get_agent("agent-io")
        self.assertTrue(updated.input)
        self.assertTrue(updated.output)

    def test_update_stage_is_initial(self):
        """Note: is_initial is recalculated from the transition graph on save/load.
        Here we test that update_stage accepts the field without error."""
        self.controller.create_agent("Agent", "agent.md", id="agent-initial")
        # update_stage should accept is_initial without raising
        self.controller.update_stage("agent-initial", {"is_initial": False})

    def test_update_stage_multiple_fields(self):
        self.controller.create_agent("Agent", "agent.md", id="agent-multi")
        self.controller.update_stage(
            "agent-multi",
            {
                "title": "Updated Agent",
                "input": True,
                "permissions": [
                    {"type": "tables", "action": "select", "tableName": "data"}
                ],
            },
        )
        updated = self.controller.get_agent("agent-multi")
        self.assertEqual(updated.title, "Updated Agent")
        self.assertTrue(updated.input)
        self.assertEqual(len(updated.permissions), 1)

    def test_delete_stage(self):
        self.controller.create_agent("Agent", "agent.md", id="agent-del")
        self.controller.delete_stage("agent-del")
        self.assertIsNone(self.controller.get_agent("agent-del"))
        self.assertEqual(len(self.controller.get_agents()), 0)

    def test_delete_stage_with_remove_file(self):
        agent = self.controller.create_agent(
            "Agent", "del_file.md", id="agent-del-file"
        )
        file_path = Path(agent.file)
        self.assertTrue(file_path.exists())

        self.controller.delete_stage("agent-del-file", remove_file=True)
        self.assertFalse(file_path.exists())


class TestAgentProjectSerialization(BaseTest):
    """Test that the abstra.json file correctly serializes agent data."""

    def test_agents_key_in_abstra_json(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(title="JSON Agent", file="json.md", id="agent-json")
        project.add_stage(agent)
        self.repositories.project.save(project)

        abstra_json_path = self.root / "abstra.json"
        with open(abstra_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("agents", data)
        self.assertEqual(len(data["agents"]), 1)
        self.assertEqual(data["agents"][0]["id"], "agent-json")
        self.assertEqual(data["agents"][0]["title"], "JSON Agent")
        self.assertEqual(data["agents"][0]["file"], "json.md")

    def test_agents_permissions_in_abstra_json(self):
        project = self.repositories.project.load()
        agent = AgentStage.create(
            title="Perm Agent",
            file="perm.md",
            id="agent-perm-json",
            permissions=[
                AgentPermission(type="tables", action="select", table_name="users"),
            ],
        )
        project.add_stage(agent)
        self.repositories.project.save(project)

        abstra_json_path = self.root / "abstra.json"
        with open(abstra_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        perms = data["agents"][0]["permissions"]
        self.assertEqual(len(perms), 1)
        self.assertEqual(perms[0]["type"], "tables")
        self.assertEqual(perms[0]["action"], "select")
        # camelCase in JSON
        self.assertEqual(perms[0]["tableName"], "users")

    def test_empty_agents_key_in_abstra_json(self):
        project = self.repositories.project.load()
        self.repositories.project.save(project)

        abstra_json_path = self.root / "abstra.json"
        with open(abstra_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("agents", data)
        self.assertEqual(data["agents"], [])


if __name__ == "__main__":
    unittest.main()
