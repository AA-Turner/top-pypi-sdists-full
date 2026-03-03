from unittest import TestCase

from abstra_internals.repositories.project.json_migrations.migration_018 import (
    Migration018,
    _generate_py_content,
    _group_permissions,
)


class TestMigration018(TestCase):
    def test_basic_agent_to_script_conversion(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-1",
                        "file": "my_agent.md",
                        "title": "My Agent",
                        "is_initial": True,
                        "workflow_position": [100, 200],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["my_agent.md"] = "You are a helpful assistant."
        m.apply()

        self.assertEqual(m.data["version"], "18.0")
        self.assertNotIn("agents", m.data)
        self.assertEqual(len(m.data["scripts"]), 1)

        script = m.data["scripts"][0]
        self.assertEqual(script["id"], "agent-1")
        self.assertEqual(script["file"], "my_agent.py")
        self.assertEqual(script["title"], "My Agent")
        self.assertNotIn("permissions", script)
        self.assertNotIn("max_steps", script)

        written = m._test_written_files["my_agent.py"]
        self.assertIn("from abstra.ai import run_agent", written)
        self.assertIn("You are a helpful assistant.", written)

    def test_agent_with_permissions_generates_tools(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-2",
                        "file": "agent_perms.md",
                        "title": "Agent Perms",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [
                            {
                                "type": "tables",
                                "action": "select",
                                "tableName": "users",
                            },
                            {
                                "type": "tables",
                                "action": "insert",
                                "tableName": "users",
                            },
                            {"type": "files", "action": "read"},
                            {"type": "files", "action": "write"},
                            {
                                "type": "connections",
                                "action": "execute",
                                "connectionName": "slack",
                            },
                        ],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["agent_perms.md"] = "Handle tasks."
        m.apply()

        written = m._test_written_files["agent_perms.py"]
        self.assertIn(
            "from abstra_internals.agents.tools.tables import TablesTools", written
        )
        self.assertIn(
            "from abstra_internals.agents.tools.files import FilesTools", written
        )
        self.assertIn(
            "from abstra_internals.agents.tools.connectors import ConnectorsTools",
            written,
        )
        self.assertIn(
            'TablesTools(method=["select", "insert"], table="users")', written
        )
        self.assertIn('FilesTools(actions=["read", "write"])', written)
        self.assertIn('ConnectorsTools(action=["execute"])', written)

    def test_transitions_rewritten(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [
                    {
                        "id": "form-1",
                        "transitions": [
                            {
                                "id": "t1",
                                "target_id": "agent-1",
                                "target_type": "agents",
                                "type": "task",
                            },
                            {
                                "id": "t2",
                                "target_id": "script-1",
                                "target_type": "scripts",
                                "type": "task",
                            },
                        ],
                    }
                ],
                "hooks": [],
                "jobs": [],
                "scripts": [{"id": "script-1", "transitions": []}],
                "agents": [
                    {
                        "id": "agent-1",
                        "file": "a.md",
                        "title": "A",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["a.md"] = "test"
        m.apply()

        form_transitions = m.data["forms"][0]["transitions"]
        self.assertEqual(form_transitions[0]["target_type"], "scripts")
        self.assertEqual(form_transitions[1]["target_type"], "scripts")

    def test_non_default_max_steps(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-3",
                        "file": "steps.md",
                        "title": "Steps",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 50,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["steps.md"] = "test"
        m.apply()

        written = m._test_written_files["steps.py"]
        self.assertIn("max_steps=50", written)

    def test_no_agents_is_noop(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [{"id": "s1", "transitions": []}],
                "agents": [],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m.apply()

        self.assertEqual(m.data["version"], "18.0")
        self.assertNotIn("agents", m.data)
        self.assertEqual(len(m.data["scripts"]), 1)

    def test_browser_permissions_generate_browser_tools(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-b",
                        "file": "browser_agent.md",
                        "title": "Browser Agent",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [
                            {
                                "type": "browser",
                                "allowedUrls": ["https://example.com"],
                            },
                        ],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["browser_agent.md"] = "Browse the web."
        m.apply()

        written = m._test_written_files["browser_agent.py"]
        self.assertIn("BrowserTools", written)
        self.assertIn("https://example.com", written)
        self.assertIn(
            "from abstra_internals.agents.tools.browser import BrowserTools", written
        )

    def test_browser_permissions_no_urls(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-bn",
                        "file": "browser_no_urls.md",
                        "title": "Browser No URLs",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [{"type": "browser", "allowedUrls": None}],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["browser_no_urls.md"] = "Browse anything."
        m.apply()

        written = m._test_written_files["browser_no_urls.py"]
        self.assertIn("BrowserTools()", written)

    def test_md_file_deleted_after_conversion(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-del",
                        "file": "to_delete.md",
                        "title": "Delete Test",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["to_delete.md"] = "Delete me."
        m.apply()

        self.assertIn("to_delete.py", m._test_written_files)
        self.assertIn("to_delete.md", m._test_deleted_files)

    def test_multiple_agents_md_files_deleted(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "a1",
                        "file": "first.md",
                        "title": "First",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    },
                    {
                        "id": "a2",
                        "file": "second.md",
                        "title": "Second",
                        "is_initial": False,
                        "workflow_position": [100, 0],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    },
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["first.md"] = "First agent."
        m._test_prompts["second.md"] = "Second agent."
        m.apply()

        self.assertEqual(m._test_deleted_files, {"first.md", "second.md"})
        self.assertEqual(len(m._test_written_files), 2)

    def test_agent_to_agent_transition_rewritten(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-a",
                        "file": "a.md",
                        "title": "Agent A",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [
                            {
                                "id": "t-ab",
                                "target_id": "agent-b",
                                "target_type": "agents",
                                "type": "task",
                            }
                        ],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    },
                    {
                        "id": "agent-b",
                        "file": "b.md",
                        "title": "Agent B",
                        "is_initial": False,
                        "workflow_position": [100, 0],
                        "transitions": [],
                        "permissions": [],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    },
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["a.md"] = "Agent A prompt"
        m._test_prompts["b.md"] = "Agent B prompt"
        m.apply()

        self.assertEqual(len(m.data["scripts"]), 2)
        self.assertNotIn("agents", m.data)

        script_a = next(s for s in m.data["scripts"] if s["id"] == "agent-a")
        self.assertEqual(len(script_a["transitions"]), 1)
        self.assertEqual(script_a["transitions"][0]["target_id"], "agent-b")
        self.assertEqual(script_a["transitions"][0]["target_type"], "scripts")

    def test_source_code_permissions_emit_warning(self):
        m = Migration018(
            {
                "workspace": {"name": "Test"},
                "home": {"access_control": {"is_public": False, "required_roles": []}},
                "forms": [],
                "hooks": [],
                "jobs": [],
                "scripts": [],
                "agents": [
                    {
                        "id": "agent-sc",
                        "file": "sc.md",
                        "title": "SC Agent",
                        "is_initial": True,
                        "workflow_position": [0, 0],
                        "transitions": [],
                        "permissions": [
                            {"type": "source_code", "action": "read"},
                        ],
                        "input": False,
                        "output": False,
                        "task_schema": None,
                        "max_steps": 30,
                    }
                ],
                "version": "17.0",
            }
        )
        m.set_as_test()
        m._test_prompts["sc.md"] = "test"
        m.apply()

        self.assertTrue(any("source_code" in w for w in m.warnings))
        self.assertTrue(any("SC Agent" in w for w in m.warnings))


class TestGroupPermissions(TestCase):
    def test_group_tables(self):
        perms = [
            {"type": "tables", "action": "select", "tableName": "users"},
            {"type": "tables", "action": "insert", "tableName": "users"},
        ]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0], 'TablesTools(method=["select", "insert"], table="users")'
        )

    def test_group_files(self):
        perms = [
            {"type": "files", "action": "read"},
            {"type": "files", "action": "write"},
        ]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'FilesTools(actions=["read", "write"])')

    def test_group_connections(self):
        perms = [
            {"type": "connections", "action": "execute", "connectionName": "slack"},
        ]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'ConnectorsTools(action=["execute"])')

    def test_source_code_skipped(self):
        perms = [{"type": "source_code", "action": "read"}]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 0)

    def test_browser_with_urls(self):
        perms = [{"type": "browser", "allowedUrls": ["https://a.com"]}]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'BrowserTools(url=["https://a.com"])')

    def test_browser_without_urls(self):
        perms = [{"type": "browser", "allowedUrls": None}]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "BrowserTools()")

    def test_tables_no_table_name(self):
        perms = [
            {"type": "tables", "action": "select"},
        ]
        result = _group_permissions(perms)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], 'TablesTools(method=["select"])')


class TestGeneratePyContent(TestCase):
    def test_basic_generation(self):
        content = _generate_py_content("Hello", [], 30)
        self.assertIn("from abstra.ai import run_agent", content)
        self.assertIn("Hello", content)
        self.assertNotIn("tools=", content)
        self.assertNotIn("max_steps=", content)

    def test_prompt_ending_with_quote(self):
        content = _generate_py_content('She said "hello"', [], 30)
        compile(content, "<test>", "exec")

    def test_prompt_with_triple_quotes(self):
        content = _generate_py_content('text with """triple""" quotes', [], 30)
        compile(content, "<test>", "exec")

    def test_valid_python(self):
        content = _generate_py_content("test prompt", [], 30)
        compile(content, "<test>", "exec")

    def test_with_tools_valid_python(self):
        perms = [
            {"type": "tables", "action": "select", "tableName": "t"},
            {"type": "files", "action": "read"},
        ]
        content = _generate_py_content("test", perms, 30)
        compile(content, "<test>", "exec")

    def test_with_browser_valid_python(self):
        perms = [
            {"type": "browser", "allowedUrls": ["https://example.com"]},
            {"type": "tables", "action": "select", "tableName": "t"},
        ]
        content = _generate_py_content("test", perms, 30)
        compile(content, "<test>", "exec")

    def test_imports_use_correct_paths(self):
        perms = [
            {"type": "tables", "action": "select", "tableName": "t"},
            {"type": "files", "action": "read"},
            {"type": "connections", "action": "execute"},
            {"type": "browser", "allowedUrls": None},
        ]
        content = _generate_py_content("test", perms, 30)
        self.assertIn(
            "from abstra_internals.agents.tools.tables import TablesTools", content
        )
        self.assertIn(
            "from abstra_internals.agents.tools.files import FilesTools", content
        )
        self.assertIn(
            "from abstra_internals.agents.tools.connectors import ConnectorsTools",
            content,
        )
        self.assertIn(
            "from abstra_internals.agents.tools.browser import BrowserTools", content
        )
