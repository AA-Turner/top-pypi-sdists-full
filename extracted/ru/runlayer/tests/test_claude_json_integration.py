"""Integration test for Claude Code config file parsing.

Tests verify that wildcard extraction in the projects.*.mcpServers structure:
1. Uses just the server name (no project path prefix)
2. Stores the full project path(s) in the project_name field as a list
3. Servers with same name in multiple projects are merged with all projects listed
"""


import pytest

from runlayer_cli.scan.clients import MCPClientDefinition, get_client_by_name


# Sample config data based on Claude Code's structure
SAMPLE_CLAUDE_CONFIG = {
    "mcpServers": {},  # Global servers empty in this case
    "projects": {
        "/home/user/psql": {
            "mcpServers": {
                "incidentio": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-1/mcp",
                },
                "posthog": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-2/mcp",
                },
            }
        },
        "/home/user/workspace/my-project": {
            "mcpServers": {
                "notion": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-3/mcp",
                },
                "linear3": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-4/mcp",
                },
            }
        },
        "/home/user/workspace": {
            "mcpServers": {
                "google-docs-2": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-5/mcp",
                },
                "linear": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-6/mcp",
                },
                "google-sheets": {
                    "type": "http",
                    "url": "https://example.com/api/v1/proxy/server-7/mcp",
                },
            }
        },
    },
}


class TestClaudeCodeConfigParsing:
    """Test Claude Code config parsing with real-world data."""

    def test_extract_servers_uses_just_server_name_with_project_field(self):
        """Verify server names are clean and project path is in project_name field."""
        client = get_client_by_name("claude_code")
        assert client is not None

        servers = client.extract_servers(SAMPLE_CLAUDE_CONFIG)

        # Verify we got the right number of servers (some may merge if same name)
        # psql: incidentio, posthog
        # my-project: notion, linear3
        # workspace: google-docs-2, linear, google-sheets
        # Total unique: 7 servers
        assert len(servers) == 7

        # Verify server names are just the server name, no project prefix
        assert "incidentio" in servers
        assert "posthog" in servers
        assert "notion" in servers
        assert "linear3" in servers
        assert "google-docs-2" in servers
        assert "linear" in servers
        assert "google-sheets" in servers

        # Verify no project paths in server names
        for server_name in servers.keys():
            assert "/" not in server_name, (
                f"Server name should not contain any path separator: {server_name}"
            )

        # Verify project_name field contains the full path(s) as a list
        assert servers["incidentio"]["project_name"] == ["/home/user/psql"]
        assert servers["posthog"]["project_name"] == ["/home/user/psql"]
        assert servers["linear3"]["project_name"] == ["/home/user/workspace/my-project"]
        assert servers["google-docs-2"]["project_name"] == ["/home/user/workspace"]

    def test_extract_servers_with_global_and_project_servers(self):
        """Test extraction when there are both global and project-level servers."""
        client = get_client_by_name("claude_code")
        assert client is not None

        config_with_global = {
            "mcpServers": {
                "global-server": {"command": "node", "args": ["server.js"]},
            },
            "projects": {
                "/home/user/my-project": {
                    "mcpServers": {
                        "project-server": {"command": "python", "args": ["serve.py"]},
                    }
                }
            },
        }

        servers = client.extract_servers(config_with_global)

        assert len(servers) == 2
        assert "global-server" in servers
        assert "project-server" in servers  # Just the server name, no project prefix

        # Global server should NOT have project_name field
        assert "project_name" not in servers["global-server"]

        # Project server should have project_name field with full path as a list
        assert servers["project-server"]["project_name"] == ["/home/user/my-project"]

    def test_project_path_with_deeply_nested_path(self):
        """Test that deeply nested paths are stored in full in project_name field."""
        client = MCPClientDefinition(
            name="test",
            display_name="Test",
            paths=[],
            servers_key="mcpServers",
            additional_servers_keys=["projects.*.mcpServers"],
        )

        config_data = {
            "mcpServers": {},
            "projects": {
                "/home/developer/projects/client-a/frontend": {
                    "mcpServers": {
                        "dev-server": {"command": "npm", "args": ["run", "dev"]},
                    }
                },
            },
        }

        servers = client.extract_servers(config_data)

        # Should be just "dev-server", no project path in the name
        assert "dev-server" in servers
        assert not any("/" in k for k in servers.keys())

        # project_name should contain the full path as a list
        assert servers["dev-server"]["project_name"] == ["/home/developer/projects/client-a/frontend"]

    def test_handles_empty_projects(self):
        """Test graceful handling of projects with no mcpServers."""
        client = get_client_by_name("claude_code")
        assert client is not None

        config_data = {
            "mcpServers": {"global": {"command": "node"}},
            "projects": {
                "/home/user/empty-project": {
                    "mcpServers": {}  # Empty
                },
                "/home/user/other-project": {
                    # No mcpServers key at all
                    "allowedTools": []
                },
            },
        }

        servers = client.extract_servers(config_data)
        assert len(servers) == 1
        assert "global" in servers

    def test_same_server_in_multiple_projects_merges_to_list(self):
        """Servers with same name in multiple projects should have all projects listed."""
        client = get_client_by_name("claude_code")
        assert client is not None

        config_data = {
            "mcpServers": {},
            "projects": {
                "/home/user/project-a": {
                    "mcpServers": {
                        "linear": {"type": "http", "url": "https://example.com/linear-1"},
                        "unique-a": {"command": "node"},
                    }
                },
                "/home/user/project-b": {
                    "mcpServers": {
                        "linear": {"type": "http", "url": "https://example.com/linear-2"},
                        "unique-b": {"command": "python"},
                    }
                },
                "/home/user/project-c": {
                    "mcpServers": {
                        "linear": {"type": "http", "url": "https://example.com/linear-3"},
                    }
                },
            },
        }

        servers = client.extract_servers(config_data)

        # Should have 3 unique server names: linear, unique-a, unique-b
        assert len(servers) == 3
        assert "linear" in servers
        assert "unique-a" in servers
        assert "unique-b" in servers

        # linear should have all 3 projects in project_name list
        linear_projects = servers["linear"]["project_name"]
        assert isinstance(linear_projects, list)
        assert len(linear_projects) == 3
        assert "/home/user/project-a" in linear_projects
        assert "/home/user/project-b" in linear_projects
        assert "/home/user/project-c" in linear_projects

        # Unique servers should have single-element lists
        assert servers["unique-a"]["project_name"] == ["/home/user/project-a"]
        assert servers["unique-b"]["project_name"] == ["/home/user/project-b"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
