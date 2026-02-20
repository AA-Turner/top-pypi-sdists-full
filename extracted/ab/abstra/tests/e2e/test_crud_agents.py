import pathlib
import unittest

from abstra_internals.templates import new_agent_code
from tests.fixtures import BaseTest


class TestCRUDAgents(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()

    # --- LIST ---

    def test_api_list_empty(self):
        agents = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents), 0)

    def test_api_list_after_create(self):
        self.client.post(
            "/_editor/api/agents/",
            json={"title": "My Agent", "file": "agent.md"},
        )
        agents = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["title"], "My Agent")
        self.assertEqual(agents[0]["file"], "agent.md")

    def test_api_list_multiple_sorted(self):
        self.client.post(
            "/_editor/api/agents/",
            json={"title": "Zebra Agent", "file": "zebra.md"},
        )
        self.client.post(
            "/_editor/api/agents/",
            json={"title": "Alpha Agent", "file": "alpha.md"},
        )
        self.client.post(
            "/_editor/api/agents/",
            json={"title": "Middle Agent", "file": "middle.md"},
        )
        agents = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents), 3)
        # Should be sorted alphabetically by title
        self.assertEqual(agents[0]["title"], "Alpha Agent")
        self.assertEqual(agents[1]["title"], "Middle Agent")
        self.assertEqual(agents[2]["title"], "Zebra Agent")

    # --- GET ---

    def test_api_get_by_id(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "My Agent", "file": "agent.md"},
        ).get_json()
        agent_id = created["id"]

        agent = self.client.get(f"/_editor/api/agents/{agent_id}").get_json()
        self.assertEqual(agent["id"], agent_id)
        self.assertEqual(agent["title"], "My Agent")

    def test_api_get_nonexistent_returns_404(self):
        response = self.client.get("/_editor/api/agents/nonexistent-id")
        self.assertEqual(response.status_code, 404)

    # --- CREATE ---

    def test_api_create_returns_agent(self):
        response = self.client.post(
            "/_editor/api/agents/",
            json={"title": "New Agent", "file": "new_agent.md"},
        )
        self.assertEqual(response.status_code, 200)
        agent = response.get_json()
        self.assertEqual(agent["title"], "New Agent")
        self.assertEqual(agent["file"], "new_agent.md")
        self.assertIn("id", agent)
        self.assertTrue(len(agent["id"]) > 0)

    def test_api_create_with_custom_id(self):
        response = self.client.post(
            "/_editor/api/agents/",
            json={
                "title": "Agent",
                "file": "agent.md",
                "id": "custom-agent-id",
            },
        )
        agent = response.get_json()
        self.assertEqual(agent["id"], "custom-agent-id")

    def test_api_create_with_position(self):
        response = self.client.post(
            "/_editor/api/agents/",
            json={
                "title": "Agent",
                "file": "agent.md",
                "position": [100, 200],
            },
        )
        agent = response.get_json()
        self.assertEqual(agent["workflow_position"], [100, 200])

    def test_api_create_writes_template_file(self):
        agent = self.client.post(
            "/_editor/api/agents/",
            json={"title": "New Agent", "file": "agent.md"},
        ).get_json()
        file_content = pathlib.Path(agent["file"]).read_text(encoding="utf-8")
        self.assertEqual(file_content, new_agent_code)

    def test_api_create_missing_title_returns_400(self):
        response = self.client.post(
            "/_editor/api/agents/",
            json={"file": "agent.md"},
        )
        self.assertEqual(response.status_code, 400)

    def test_api_create_missing_file_returns_400(self):
        response = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent"},
        )
        self.assertEqual(response.status_code, 400)

    def test_api_create_empty_body_returns_400(self):
        response = self.client.post(
            "/_editor/api/agents/",
            content_type="application/json",
            data="null",
        )
        self.assertEqual(response.status_code, 400)

    # --- UPDATE ---

    def test_api_update_title(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Old Title", "file": "agent.md"},
        ).get_json()

        self.client.put(
            f"/_editor/api/agents/{created['id']}",
            json={"title": "New Title"},
        )

        agent = self.client.get(f"/_editor/api/agents/{created['id']}").get_json()
        self.assertEqual(agent["title"], "New Title")

    def test_api_update_permissions(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        self.client.put(
            f"/_editor/api/agents/{created['id']}",
            json={
                "permissions": [
                    {"type": "tables", "action": "select", "tableName": "users"},
                    {"type": "files", "action": "read"},
                ]
            },
        )

        agent = self.client.get(f"/_editor/api/agents/{created['id']}").get_json()
        self.assertEqual(len(agent["permissions"]), 2)
        self.assertEqual(agent["permissions"][0]["tableName"], "users")
        self.assertEqual(agent["permissions"][1]["type"], "files")

    def test_api_update_is_initial(self):
        """Note: is_initial is recalculated from the transition graph on save/load.
        This test verifies the field is accepted without error."""
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()
        self.assertTrue(created["is_initial"])

        # Should not raise an error
        response = self.client.put(
            f"/_editor/api/agents/{created['id']}",
            json={"is_initial": False},
        )
        self.assertEqual(response.status_code, 200)

    def test_api_update_input_output(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        self.client.put(
            f"/_editor/api/agents/{created['id']}",
            json={"input": True, "output": True},
        )

        agent = self.client.get(f"/_editor/api/agents/{created['id']}").get_json()
        self.assertTrue(agent["input"])
        self.assertTrue(agent["output"])

    def test_api_update_prompt_content_writes_file(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        new_prompt = "You are a custom agent.\n{{ trigger_task.type }}"
        self.client.put(
            f"/_editor/api/agents/{created['id']}",
            json={"prompt_content": new_prompt},
        )

        file_content = pathlib.Path(created["file"]).read_text(encoding="utf-8")
        self.assertEqual(file_content, new_prompt)

    def test_api_update_workflow_position(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        self.client.put(
            f"/_editor/api/agents/{created['id']}",
            json={"workflow_position": [500, 600]},
        )

        agent = self.client.get(f"/_editor/api/agents/{created['id']}").get_json()
        self.assertEqual(agent["workflow_position"], [500, 600])

    # --- DELETE ---

    def test_api_delete(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        agents_before = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents_before), 1)

        response = self.client.delete(f"/_editor/api/agents/{created['id']}")
        self.assertEqual(response.status_code, 200)

        agents_after = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents_after), 0)

    def test_api_delete_with_remove_file(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        file_path = pathlib.Path(created["file"])
        self.assertTrue(file_path.exists())

        self.client.delete(f"/_editor/api/agents/{created['id']}?remove_file=true")

        agents_after = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents_after), 0)
        self.assertFalse(file_path.exists())

    def test_api_delete_without_remove_file_keeps_file(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        file_path = pathlib.Path(created["file"])
        self.assertTrue(file_path.exists())

        self.client.delete(f"/_editor/api/agents/{created['id']}")

        self.assertTrue(file_path.exists())

    # --- RUN ---

    def test_api_run_enqueues_agent(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        response = self.client.post(
            f"/_editor/api/agents/{created['id']}/run",
            json={"task_id": "task-123"},
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["ok"])
        self.assertIn("execution_id", data)

    def test_api_run_nonexistent_agent_returns_404(self):
        response = self.client.post(
            "/_editor/api/agents/nonexistent-id/run",
            json={"task_id": "task-123"},
        )
        self.assertEqual(response.status_code, 404)

    def test_api_run_missing_task_id_returns_400(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        response = self.client.post(
            f"/_editor/api/agents/{created['id']}/run",
            json={},
        )
        self.assertEqual(response.status_code, 400)

    def test_api_run_no_body_returns_400(self):
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Agent", "file": "agent.md"},
        ).get_json()

        response = self.client.post(
            f"/_editor/api/agents/{created['id']}/run",
            content_type="application/json",
            data="null",
        )
        self.assertEqual(response.status_code, 400)

    # --- PERSISTENCE ---

    def test_agent_persists_after_reload(self):
        """Agent should survive a project reload (save/load cycle)."""
        created = self.client.post(
            "/_editor/api/agents/",
            json={"title": "Persistent Agent", "file": "persist.md"},
        ).get_json()

        # Force a fresh project load by getting from a new controller view
        agents = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents), 1)
        self.assertEqual(agents[0]["title"], "Persistent Agent")
        self.assertEqual(agents[0]["id"], created["id"])

    def test_multiple_agents_persist(self):
        for i in range(5):
            self.client.post(
                "/_editor/api/agents/",
                json={"title": f"Agent {i}", "file": f"agent_{i}.md"},
            )

        agents = self.client.get("/_editor/api/agents/").get_json()
        self.assertEqual(len(agents), 5)

    def test_agent_coexists_with_other_stages(self):
        """Agents should not interfere with other stage types."""
        # Create a hook
        self.client.post(
            "/_editor/api/hooks/", json={"title": "My Hook", "file": "hook.py"}
        )
        # Create an agent
        self.client.post(
            "/_editor/api/agents/",
            json={"title": "My Agent", "file": "agent.md"},
        )
        # Create a script
        self.client.post(
            "/_editor/api/scripts/", json={"title": "My Script", "file": "script.py"}
        )

        hooks = self.client.get("/_editor/api/hooks/").get_json()
        agents = self.client.get("/_editor/api/agents/").get_json()
        scripts = self.client.get("/_editor/api/scripts/").get_json()

        self.assertEqual(len(hooks), 1)
        self.assertEqual(len(agents), 1)
        self.assertEqual(len(scripts), 1)


if __name__ == "__main__":
    unittest.main()
