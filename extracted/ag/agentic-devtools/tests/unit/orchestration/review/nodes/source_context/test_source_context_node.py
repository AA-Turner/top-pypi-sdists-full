"""Tests for source_context_node."""

from __future__ import annotations

from unittest.mock import patch


class TestSourceContextNodeDisabled:
    """Tests for pass-through behavior when source_context_enabled=False."""

    def test_disabled_sets_context_status_on_all_files(self) -> None:
        """When disabled, all files get context_status='disabled'."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "source_context_enabled": False,
            "files": [
                {"path": "/src/app.py", "changeType": "edit", "patch": "diff"},
                {"path": "/src/utils.py", "changeType": "add", "patch": "diff2"},
            ],
            "commit_hash": "abc123",
            "config": {},
        }

        result = source_context_node(state)

        assert "files" in result
        assert len(result["files"]) == 2
        for f in result["files"]:
            assert f["context_status"] == "disabled"
        # Pass-through (FR-009): upstream fields are left unchanged and no
        # context fields are cleared/added beyond context_status.
        assert result["files"][0]["path"] == "/src/app.py"
        assert result["files"][1]["patch"] == "diff2"
        assert "full_content_source" not in result["files"][0]
        assert "truncation_applied" not in result["files"][0]

    def test_disabled_preserves_upstream_fields(self) -> None:
        """Upstream fields (path, changeType, patch) are preserved."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "source_context_enabled": False,
            "files": [{"path": "/src/app.py", "changeType": "edit", "patch": "some diff", "item": {"id": 1}}],
            "commit_hash": "abc",
            "config": {},
        }

        result = source_context_node(state)
        f = result["files"][0]
        assert f["path"] == "/src/app.py"
        assert f["changeType"] == "edit"
        assert f["patch"] == "some diff"
        assert f["item"] == {"id": 1}


class TestSourceContextNodeEnabled:
    """Tests for source context retrieval when enabled."""

    def test_empty_files_returns_empty(self) -> None:
        """Empty files list returns empty list."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {"files": [], "commit_hash": "abc", "config": {}}
        result = source_context_node(state)
        assert result == {"files": []}

    def test_binary_files_skipped(self) -> None:
        """Binary files are skipped with appropriate status."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/assets/logo.png", "changeType": "edit", "isBinary": True}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            result = source_context_node(state)

        assert result["files"][0]["context_status"] == "skipped_binary"

    def test_returns_complete_files_list(self) -> None:
        """Node returns complete files list preserving all entries."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {"path": "/src/a.py", "changeType": "edit"},
                {"path": "/src/b.py", "changeType": "add"},
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            result = source_context_node(state)

        assert len(result["files"]) == 2

    def test_populates_full_content_from_retrieval(self) -> None:
        """Successfully retrieved content is populated on file entries."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="source content", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(content="target content", context_status="success"),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["full_content_source"] == "source content"
        assert f["full_content_target"] == "target content"
        assert f["context_status"] == "success"

    def test_new_file_no_target_expected(self) -> None:
        """New files (add) report partial with not_found_on_target."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/new.py", "changeType": "add"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/new.py", "source"): RetrievalResult(content="new file", context_status="success"),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "partial"
        assert f["context_status_reason"] == "not_found_on_target"

    def test_deleted_file_no_source_expected(self) -> None:
        """Deleted files report partial with not_found_on_source."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/old.py", "changeType": "delete"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/old.py", "target"): RetrievalResult(content="deleted file", context_status="success"),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "partial"
        assert f["context_status_reason"] == "not_found_on_source"

    def test_rename_uses_original_path_for_target_lookup(self) -> None:
        """Renames fetch base-side content from originalPath."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {
                    "path": "/src/new_name.py",
                    "originalPath": "/src/old_name.py",
                    "changeType": "rename",
                }
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            source_context_node(state)

        assert mock_retrieve.call_args_list
        requests = mock_retrieve.call_args_list[0].args[0]
        assert ("/src/new_name.py", "abc123", "source") in requests
        assert ("/src/old_name.py", "def456", "target") in requests

    def test_rename_without_string_original_path_falls_back_to_current_path(self) -> None:
        """Invalid originalPath values do not break rename target lookup."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/new_name.py", "originalPath": None, "changeType": "rename"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            source_context_node(state)

        requests = mock_retrieve.call_args_list[0].args[0]
        assert ("/src/new_name.py", "def456", "target") in requests

    def test_deep_depth_fetches_related_file_contents(self) -> None:
        """Deep depth attaches retrieved test and import contents to the file entry."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {
                    "path": "/agentic_devtools/state.py",
                    "changeType": "edit",
                    "addedLines": [{"line": 5}],
                }
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "source"): RetrievalResult(
                        content="from agentic_devtools.config import x\n",
                        context_status="success",
                    ),
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(content="y", context_status="success"),
                },
                {
                    ("tests/test_state.py", "related_test_source"): RetrievalResult(
                        content="def test_state():\n    assert True",
                        context_status="success",
                    ),
                    ("agentic_devtools/config.py", "import_source"): RetrievalResult(
                        content="SETTING = 1\n",
                        context_status="success",
                    ),
                },
            ]
            mock_discover.return_value = {"related_tests": ["tests/test_state.py"], "missing_tests": False}
            mock_imports.return_value = ["agentic_devtools/config.py"]

            result = source_context_node(state)

        f = result["files"][0]
        assert f["related_test_contents"] == [
            {"path": "tests/test_state.py", "content": "def test_state():\n    assert True"}
        ]
        assert f["resolved_import_contents"] == [{"path": "agentic_devtools/config.py", "content": "SETTING = 1\n"}]

    def test_deleted_file_uses_target_side_for_deep_related_context(self) -> None:
        """Deleted files derive tests/imports from the base-side content and commit."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {
                    "path": "/agentic_devtools/old_module.py",
                    "changeType": "delete",
                    "removedLines": [{"line": 2}],
                }
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/old_module.py", "target"): RetrievalResult(
                        content="from agentic_devtools.config import SETTING\nold = SETTING\n",
                        context_status="success",
                    ),
                },
                {
                    (
                        "tests/unit/orchestration/review/old_module/test_old_module.py",
                        "related_test_target",
                    ): RetrievalResult(
                        content="def test_old():\n    assert True",
                        context_status="success",
                    ),
                    ("agentic_devtools/config.py", "import_target"): RetrievalResult(
                        content="SETTING = 1\n",
                        context_status="success",
                    ),
                },
            ]
            mock_discover.return_value = {
                "related_tests": ["tests/unit/orchestration/review/old_module/test_old_module.py"],
                "missing_tests": False,
            }
            mock_imports.return_value = ["agentic_devtools/config.py"]

            result = source_context_node(state)

        mock_discover.assert_called_once_with(
            "/agentic_devtools/old_module.py",
            repo_root="/repo",
            source_content="from agentic_devtools.config import SETTING\nold = SETTING\n",
            auto_detect_repo_root=False,
        )
        mock_imports.assert_called_once_with(
            "from agentic_devtools.config import SETTING\nold = SETTING\n",
            "/agentic_devtools/old_module.py",
            diff_lines=[2],
            repo_root="/repo",
        )
        supplemental_requests = mock_retrieve.call_args_list[1].args[0]
        assert (
            "tests/unit/orchestration/review/old_module/test_old_module.py",
            "def456",
            "related_test_target",
        ) in supplemental_requests
        assert ("agentic_devtools/config.py", "def456", "import_target") in supplemental_requests
        file_entry = result["files"][0]
        assert file_entry["related_test_contents"] == [
            {
                "path": "tests/unit/orchestration/review/old_module/test_old_module.py",
                "content": "def test_old():\n    assert True",
            }
        ]
        assert file_entry["resolved_import_contents"] == [
            {"path": "agentic_devtools/config.py", "content": "SETTING = 1\n"}
        ]

    def test_skips_non_string_related_paths_and_unsuccessful_supplemental_results(self) -> None:
        """Supplemental retrieval only uses string paths and only keeps successful content results."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
            "model_config_raw": {"default-model": 123},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                side_effect=RuntimeError("missing"),
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "source"): RetrievalResult(content="x", context_status="success"),
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(content="y", context_status="success"),
                },
                {
                    ("tests/test_state.py", "related_test_source"): RetrievalResult(
                        context_status="unavailable",
                        context_status_reason="git_show_failed",
                    ),
                    ("agentic_devtools/config.py", "import_source"): RetrievalResult(
                        context_status="skipped_too_large",
                        context_status_reason="too_large",
                    ),
                },
            ]
            mock_discover.return_value = {"related_tests": ["tests/test_state.py", 123], "missing_tests": False}
            mock_imports.return_value = ["agentic_devtools/config.py", 456]

            result = source_context_node(state)

        supplemental_requests = mock_retrieve.call_args_list[1].args[0]
        assert ("tests/test_state.py", "abc123", "related_test_source") in supplemental_requests
        assert ("agentic_devtools/config.py", "abc123", "import_source") in supplemental_requests
        assert all(not isinstance(path, int) for path, _, _ in supplemental_requests)
        f = result["files"][0]
        assert f["related_test_contents"] == []
        assert f["resolved_import_contents"] == []

    def test_api_only_mode_filters_unverified_related_paths(self) -> None:
        """API-only mode keeps only successfully retrieved related paths as verified."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/pkg/main.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value="/not-a-real-repo-root",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/pkg/main.py", "source"): RetrievalResult(content="import pkg.helpers", context_status="success"),
                    ("/pkg/main.py", "target"): RetrievalResult(content="old", context_status="success"),
                },
                {
                    ("tests/unit/pkg/main/test_main.py", "related_test_source"): RetrievalResult(
                        content="def test_main(): assert True",
                        context_status="success",
                    ),
                    ("tests/unit/pkg/main/test_extra.py", "related_test_source"): RetrievalResult(
                        context_status="unavailable",
                        context_status_reason="not_found",
                    ),
                    ("pkg/helpers.py", "import_source"): RetrievalResult(content="VALUE = 1", context_status="success"),
                    ("pkg/missing.py", "import_source"): RetrievalResult(
                        context_status="unavailable",
                        context_status_reason="not_found",
                    ),
                },
            ]
            mock_discover.return_value = {
                "related_tests": [
                    "tests/unit/pkg/main/test_main.py",
                    "tests/unit/pkg/main/test_extra.py",
                ],
                "missing_tests": True,
            }
            mock_imports.return_value = ["pkg/helpers.py", "pkg/missing.py"]

            result = source_context_node(state)

        file_entry = result["files"][0]
        assert file_entry["related_tests"] == ["tests/unit/pkg/main/test_main.py"]
        assert file_entry["resolved_imports"] == ["pkg/helpers.py"]
        assert file_entry["related_test_candidates"] == [
            "tests/unit/pkg/main/test_main.py",
            "tests/unit/pkg/main/test_extra.py",
        ]
        assert file_entry["resolved_import_candidates"] == ["pkg/helpers.py", "pkg/missing.py"]
        assert file_entry["missing_tests"] is False

    def test_deep_depth_discovers_and_fetches_related_config_docs(self) -> None:
        """Deep depth includes nearby changed config/doc files as lowest-priority context."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {"path": "/agentic_devtools/orchestration/review/nodes/source_context.py", "changeType": "edit"},
                {"path": "/agentic_devtools/orchestration/review/README.md", "changeType": "edit"},
                {"path": "/pyproject.toml", "changeType": "edit"},
                {"path": "/specs/1888-implement-source-context-retrieval/plan.md", "changeType": "edit"},
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/orchestration/review/nodes/source_context.py", "source"): RetrievalResult(
                        content="print('x')\n",
                        context_status="success",
                    ),
                    ("/agentic_devtools/orchestration/review/nodes/source_context.py", "target"): RetrievalResult(
                        content="print('old')\n",
                        context_status="success",
                    ),
                    ("/agentic_devtools/orchestration/review/README.md", "source"): RetrievalResult(
                        content="# Review docs\n",
                        context_status="success",
                    ),
                    ("/agentic_devtools/orchestration/review/README.md", "target"): RetrievalResult(
                        content="# Old review docs\n",
                        context_status="success",
                    ),
                    ("/pyproject.toml", "source"): RetrievalResult(
                        content="[project]\nname='agdt'\n",
                        context_status="success",
                    ),
                    ("/pyproject.toml", "target"): RetrievalResult(
                        content="[project]\nname='agdt-old'\n",
                        context_status="success",
                    ),
                    ("/specs/1888-implement-source-context-retrieval/plan.md", "source"): RetrievalResult(
                        content="# unrelated spec\n",
                        context_status="success",
                    ),
                    ("/specs/1888-implement-source-context-retrieval/plan.md", "target"): RetrievalResult(
                        content="# old spec\n",
                        context_status="success",
                    ),
                },
                {
                    ("agentic_devtools/orchestration/review/README.md", "config_doc_source"): RetrievalResult(
                        content="# Review docs\n",
                        context_status="success",
                    ),
                    ("pyproject.toml", "config_doc_source"): RetrievalResult(
                        content="[project]\nname='agdt'\n",
                        context_status="success",
                    ),
                },
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []

            result = source_context_node(state)

        file_entry = result["files"][0]
        assert file_entry["related_config_docs"] == [
            "agentic_devtools/orchestration/review/README.md",
            "pyproject.toml",
        ]
        assert file_entry["related_config_doc_contents"] == [
            {"path": "agentic_devtools/orchestration/review/README.md", "content": "# Review docs\n"},
            {"path": "pyproject.toml", "content": "[project]\nname='agdt'\n"},
        ]
        assert "specs/1888-implement-source-context-retrieval/plan.md" not in file_entry["related_config_docs"]

    def test_deep_depth_without_source_side_content_skips_import_resolution(self) -> None:
        """Deep depth leaves resolved imports empty when the relevant side has no content."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "source"): RetrievalResult(
                        context_status="unavailable",
                        context_status_reason="git_show_failed",
                    ),
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(
                        content="old\n", context_status="success"
                    ),
                },
                {},
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}

            result = source_context_node(state)

        mock_imports.assert_not_called()
        assert result["files"][0]["resolved_imports"] == []

    def test_unsuccessful_related_config_doc_fetch_is_not_retained(self) -> None:
        """Config/doc candidates with unsuccessful supplemental fetches do not retain content."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {"path": "/agentic_devtools/orchestration/review/nodes/source_context.py", "changeType": "edit"},
                {"path": "/pyproject.toml", "changeType": "edit"},
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value=None,
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/orchestration/review/nodes/source_context.py", "source"): RetrievalResult(
                        content="print('x')\n",
                        context_status="success",
                    ),
                    ("/agentic_devtools/orchestration/review/nodes/source_context.py", "target"): RetrievalResult(
                        content="print('old')\n",
                        context_status="success",
                    ),
                    ("/pyproject.toml", "source"): RetrievalResult(
                        content="[project]\nname='agdt'\n",
                        context_status="success",
                    ),
                    ("/pyproject.toml", "target"): RetrievalResult(
                        content="[project]\nname='old'\n",
                        context_status="success",
                    ),
                },
                {
                    ("pyproject.toml", "config_doc_source"): RetrievalResult(
                        context_status="unavailable",
                        context_status_reason="not_found",
                    ),
                },
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []

            result = source_context_node(state)

        file_entry = result["files"][0]
        assert file_entry["related_config_doc_candidates"] == ["pyproject.toml"]
        assert file_entry["related_config_docs"] == []
        assert file_entry["related_config_doc_contents"] == []

    def test_non_string_related_config_doc_candidates_are_skipped(self) -> None:
        """Only string config/doc candidates are queued for supplemental retrieval."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._discover_related_config_docs",
                return_value=["pyproject.toml", 123],
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "source"): RetrievalResult(
                        content="value = 1\n", context_status="success"
                    ),
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(
                        content="old = 1\n", context_status="success"
                    ),
                },
                {
                    ("pyproject.toml", "config_doc_source"): RetrievalResult(
                        content="[project]\nname='agdt'\n",
                        context_status="success",
                    ),
                },
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []

            result = source_context_node(state)

        supplemental_requests = mock_retrieve.call_args_list[1].args[0]
        assert ("pyproject.toml", "abc123", "config_doc_source") in supplemental_requests
        assert all(isinstance(path, str) for path, _, _ in supplemental_requests)
        assert result["files"][0]["related_config_doc_contents"] == [
            {"path": "pyproject.toml", "content": "[project]\nname='agdt'\n"}
        ]

    def test_deleted_file_uses_base_commit_for_related_config_docs(self) -> None:
        """Deleted files fetch related config/doc context from the base commit."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {"path": "/agentic_devtools/state.py", "changeType": "delete"},
                {"path": "/pyproject.toml", "changeType": "edit"},
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value=None,
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._discover_related_config_docs",
                return_value=["pyproject.toml"],
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(
                        content="from agentic_devtools.config import VALUE\n",
                        context_status="success",
                    ),
                    ("/pyproject.toml", "source"): RetrievalResult(
                        content="[project]\nname='agdt'\n",
                        context_status="success",
                    ),
                    ("/pyproject.toml", "target"): RetrievalResult(
                        content="[project]\nname='old'\n",
                        context_status="success",
                    ),
                },
                {
                    ("pyproject.toml", "config_doc_target"): RetrievalResult(
                        content="[project]\nname='old'\n",
                        context_status="success",
                    ),
                },
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []

            result = source_context_node(state)

        supplemental_requests = mock_retrieve.call_args_list[1].args[0]
        assert ("pyproject.toml", "def456", "config_doc_target") in supplemental_requests
        assert result["files"][0]["related_config_doc_contents"] == [
            {"path": "pyproject.toml", "content": "[project]\nname='old'\n"}
        ]

    def test_missing_supplemental_commit_skips_related_file_lookups(self) -> None:
        """Discovered related files are left unverified when no supplemental commit ref exists."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "delete"}],
            "commit_hash": "abc123",
            "base_commit_hash": "",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value=None,
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._discover_related_config_docs",
                return_value=["pyproject.toml"],
            ),
        ):
            mock_retrieve.side_effect = [{}, {}]
            mock_discover.return_value = {"related_tests": ["tests/test_state.py"], "missing_tests": True}
            mock_imports.return_value = ["agentic_devtools/config.py"]

            result = source_context_node(state)

        assert mock_retrieve.call_args_list[1].args[0] == []
        file_entry = result["files"][0]
        assert file_entry["related_tests"] == []
        assert file_entry["resolved_imports"] == []
        assert file_entry["related_config_docs"] == []

    def test_missing_head_commit_skips_non_delete_supplemental_lookups(self) -> None:
        """Non-delete files also skip supplemental verification when commit_hash is missing."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "edit"}],
            "commit_hash": None,
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value=None,
            ),
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._discover_related_config_docs",
                return_value=["pyproject.toml"],
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(
                        content="old = 1\n",
                        context_status="success",
                    ),
                },
                {},
            ]
            mock_discover.return_value = {"related_tests": ["tests/test_state.py"], "missing_tests": True}
            mock_imports.return_value = ["agentic_devtools/config.py"]

            result = source_context_node(state)

        assert mock_retrieve.call_args_list[1].args[0] == []
        file_entry = result["files"][0]
        assert file_entry["related_tests"] == []
        assert file_entry["resolved_imports"] == []
        assert file_entry["related_config_docs"] == []

    def test_ignores_explicit_review_model_id_uses_routing_instead(self) -> None:
        """review.model_id is ignored — budget uses the per-file routing result."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal", "model_id": "gpt-4o"}},
            "model_config_raw": {"default-model": "claude-opus-4.8"},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.budget.TokenBudget") as mock_budget,
            patch("agentic_devtools.orchestration.review.content_assembler.assemble_context") as mock_assemble,
        ):
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="source", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(content="target", context_status="success"),
            }
            mock_budget.return_value = type(
                "Budget",
                (),
                {
                    "consumed": 0,
                    "remaining": 0,
                    "chars_per_token": 3.5,
                },
            )()
            mock_assemble.side_effect = lambda files, _budget: files
            source_context_node(state)

        assert mock_budget.call_args is not None
        # review.model_id ("gpt-4o") is NOT used; routing resolves default-model instead
        assert mock_budget.call_args.kwargs["model_id"] == "claude-opus-4.8"

    def test_budget_bounded_by_smallest_routed_model(self) -> None:
        """Each file gets its own budget using the model it will actually be routed to."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {"path": "/src/app.py", "changeType": "edit"},
                {"path": "/docs/readme.md", "changeType": "edit"},
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
            "model_config_raw": {
                "default-model": "gpt-4o",
                "rules": [
                    {"pattern": "*.py", "model": "gpt-4"},
                    {"pattern": "*.md", "model": "claude-opus-4.8"},
                ],
            },
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.budget.TokenBudget") as mock_budget,
            patch("agentic_devtools.orchestration.review.content_assembler.assemble_context") as mock_assemble,
        ):
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="source", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(content="target", context_status="success"),
                ("/docs/readme.md", "source"): RetrievalResult(content="doc source", context_status="success"),
                ("/docs/readme.md", "target"): RetrievalResult(content="doc target", context_status="success"),
            }
            mock_budget.side_effect = [
                type("Budget", (), {"consumed": 0, "remaining": 0, "chars_per_token": 3.5})(),
                type("Budget", (), {"consumed": 0, "remaining": 0, "chars_per_token": 3.5})(),
            ]
            mock_assemble.side_effect = lambda files, _budget: files
            source_context_node(state)

        assert [call.kwargs["model_id"] for call in mock_budget.call_args_list] == [
            "gpt-4",
            "claude-opus-4.8",
        ]

    def test_deep_depth_ignores_non_integer_added_line_values(self, tmp_path) -> None:
        """Malformed addedLines entries are ignored instead of aborting deep import resolution."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        (tmp_path / "agentic_devtools").mkdir()
        (tmp_path / "agentic_devtools" / "state.py").write_text("from x import y\n")

        state = {
            "files": [
                {
                    "path": "/agentic_devtools/state.py",
                    "changeType": "edit",
                    "addedLines": [{"line": "5"}, {"line": 7}, {"line": 0}, {"line": None}],
                }
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value=tmp_path.as_posix(),
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "source"): RetrievalResult(
                        content="from x import y\n", context_status="success"
                    ),
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(
                        content="old\n", context_status="success"
                    ),
                },
                {},
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []

            result = source_context_node(state)

        mock_imports.assert_called_once_with(
            "from x import y\n",
            "/agentic_devtools/state.py",
            diff_lines=[7],
            repo_root=tmp_path.as_posix(),
        )
        assert result["files"][0]["resolved_imports"] == []

    def test_unverified_repo_root_uses_api_only_discovery_mode(self) -> None:
        """An unrelated local checkout is treated as API-only for tests and imports."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.cli.azure_devops.pr_review_manifest.resolve_repo_root",
                return_value="/definitely-missing-root",
            ),
        ):
            mock_retrieve.side_effect = [
                {
                    ("/agentic_devtools/state.py", "source"): RetrievalResult(
                        content="from agentic_devtools.config import x\n",
                        context_status="success",
                    ),
                    ("/agentic_devtools/state.py", "target"): RetrievalResult(
                        content="old\n",
                        context_status="success",
                    ),
                },
                {},
            ]
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []

            source_context_node(state)

        assert mock_discover.call_args is not None
        assert mock_discover.call_args.kwargs["repo_root"] is None
        assert mock_discover.call_args.kwargs["auto_detect_repo_root"] is False
        assert mock_discover.call_args.kwargs["source_content"] == "from agentic_devtools.config import x\n"
        assert mock_imports.call_args is not None
        assert mock_imports.call_args.kwargs["repo_root"] is None

    def test_partial_retrieval_status(self) -> None:
        """Partial retrieval (one side fails) sets partial status."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="source", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(
                    context_status="unavailable", context_status_reason="git_show_failed"
                ),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "partial"
        assert f["context_status_reason"] == "target: unavailable (git_show_failed)"

    def test_preserves_enriched_entry_when_assembly_returns_empty(self) -> None:
        """An empty assembler result falls back to the pre-assembled enriched file entry."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.content_assembler.assemble_context", return_value=[]),
        ):
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="source", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(content="target", context_status="success"),
            }
            result = source_context_node(state)

        assert result["files"][0]["full_content_source"] == "source"
        assert result["files"][0]["full_content_target"] == "target"

    def test_both_sides_fail_unavailable(self) -> None:
        """Both sides failing sets unavailable status."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(
                    context_status="unavailable", context_status_reason="git_show_failed"
                ),
                ("/src/app.py", "target"): RetrievalResult(
                    context_status="unavailable", context_status_reason="git_show_failed"
                ),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "unavailable"

    def test_both_sides_skipped_preserves_skip_status(self) -> None:
        """When both sides are deliberately skipped the skip classification is preserved."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(
                    context_status="skipped_too_large", context_status_reason="exceeds 500000 bytes"
                ),
                ("/src/app.py", "target"): RetrievalResult(
                    context_status="skipped_binary", context_status_reason="binary_file_detected"
                ),
            }
            result = source_context_node(state)

        f = result["files"][0]
        # Preserves source-side skip status; must not be "unavailable".
        assert f["context_status"] == "skipped_too_large"
        assert "exceeds 500000 bytes" in f["context_status_reason"]
        assert "binary_file_detected" in f["context_status_reason"]

    def test_no_commit_hash_add_file(self) -> None:
        """Add file with no commit_hash sets unavailable."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/new.py", "changeType": "add"}],
            "commit_hash": "",
            "base_commit_hash": "",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "unavailable"

    def test_standard_depth_discovers_tests(self) -> None:
        """Standard depth triggers test discovery."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/agentic_devtools/state.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "standard"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.return_value = {
                ("/agentic_devtools/state.py", "source"): RetrievalResult(content="x", context_status="success"),
                ("/agentic_devtools/state.py", "target"): RetrievalResult(content="y", context_status="success"),
                ("tests/test_state.py", "related_test_source"): RetrievalResult(
                    content="def test_x(): pass", context_status="success"
                ),
            }
            mock_discover.return_value = {"related_tests": ["tests/test_state.py"], "missing_tests": False}
            result = source_context_node(state)

        f = result["files"][0]
        assert f["related_tests"] == ["tests/test_state.py"]
        assert f["missing_tests"] is False

    def test_deep_depth_resolves_imports(self) -> None:
        """Deep depth triggers import resolution."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {
                    "path": "/agentic_devtools/state.py",
                    "changeType": "edit",
                    "addedLines": [{"line": 5}],
                }
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
            patch(
                "agentic_devtools.orchestration.review.nodes.source_context._resolve_verified_repo_root",
                return_value="/repo",
            ),
        ):
            mock_retrieve.return_value = {
                ("/agentic_devtools/state.py", "source"): RetrievalResult(
                    content="from agentic_devtools.config import x\n", context_status="success"
                ),
                ("/agentic_devtools/state.py", "target"): RetrievalResult(content="y", context_status="success"),
                ("agentic_devtools/config.py", "import_source"): RetrievalResult(
                    content="CONFIG = {}", context_status="success"
                ),
            }
            mock_discover.return_value = {"related_tests": [], "missing_tests": True}
            mock_imports.return_value = ["agentic_devtools/config.py"]
            result = source_context_node(state)

        f = result["files"][0]
        assert f["resolved_imports"] == ["agentic_devtools/config.py"]

    def test_invalid_depth_defaults_to_standard(self) -> None:
        """Invalid depth config defaults to standard."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc",
            "base_commit_hash": "def",
            "config": {"review": {"context_depth": "invalid_value"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
        ):
            mock_retrieve.return_value = {}
            mock_discover.return_value = {"related_tests": [], "missing_tests": True}
            result = source_context_node(state)

        # Should not crash, defaults to standard (which calls discover)
        assert len(result["files"]) == 1

    def test_non_scalar_depth_defaults_to_standard(self) -> None:
        """Non-scalar depth config (e.g. dict/list) defaults to standard without raising."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        for bad_depth in [{"unexpected": "object"}, ["unexpected", "list"]]:
            state = {
                "files": [{"path": "/src/app.py", "changeType": "edit"}],
                "commit_hash": "abc",
                "base_commit_hash": "def",
                "config": {"review": {"context_depth": bad_depth}},
            }

            with (
                patch(
                    "agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent"
                ) as mock_retrieve,
                patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            ):
                mock_retrieve.return_value = {}
                mock_discover.return_value = {"related_tests": [], "missing_tests": True}
                result = source_context_node(state)

            # Should not crash, defaults to standard (which calls discover)
            assert len(result["files"]) == 1
            assert mock_discover.called

    def test_delete_no_base_commit_unavailable(self) -> None:
        """Deleted file with no base_commit_hash sets unavailable."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/old.py", "changeType": "delete"}],
            "commit_hash": "abc",
            "base_commit_hash": "",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "unavailable"

    def test_empty_path_skipped(self) -> None:
        """File with empty path is skipped entirely."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "", "changeType": "edit"}, {"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc",
            "base_commit_hash": "def",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            result = source_context_node(state)

        # Both files returned but empty path one has no retrieval attempted
        assert len(result["files"]) == 2

    def test_add_file_retrieval_fails(self) -> None:
        """Add file where source retrieval returns non-success status."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/new.py", "changeType": "add"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/new.py", "source"): RetrievalResult(
                    context_status="unavailable", context_status_reason="git_show_failed"
                ),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "unavailable"
        assert f["context_status_reason"] == "git_show_failed"

    def test_delete_file_retrieval_fails(self) -> None:
        """Delete file where target retrieval returns non-success status."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/old.py", "changeType": "delete"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/old.py", "target"): RetrievalResult(
                    context_status="unavailable", context_status_reason="git_show_failed"
                ),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "unavailable"
        assert f["context_status_reason"] == "git_show_failed"

    def test_deep_depth_no_added_lines(self) -> None:
        """Deep depth with no addedLines still resolves imports."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [
                {
                    "path": "/agentic_devtools/state.py",
                    "changeType": "edit",
                }
            ],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "deep"}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
            patch("agentic_devtools.orchestration.review.import_resolver.resolve_imports") as mock_imports,
        ):
            mock_retrieve.return_value = {
                ("/agentic_devtools/state.py", "source"): RetrievalResult(
                    content="import os\n", context_status="success"
                ),
                ("/agentic_devtools/state.py", "target"): RetrievalResult(content="y", context_status="success"),
            }
            mock_discover.return_value = {"related_tests": [], "missing_tests": False}
            mock_imports.return_value = []
            result = source_context_node(state)

        f = result["files"][0]
        assert f["resolved_imports"] == []
        # resolve_imports was called with diff_line_numbers=None
        mock_imports.assert_called_once()
        call_kwargs = mock_imports.call_args
        assert call_kwargs[1].get("diff_line_numbers") is None or call_kwargs[0][3] is None

    def test_partial_source_fails_target_ok(self) -> None:
        """Edit where source fails but target succeeds is partial."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(
                    context_status="unavailable", context_status_reason="git_show_failed"
                ),
                ("/src/app.py", "target"): RetrievalResult(content="target", context_status="success"),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "partial"
        assert f["context_status_reason"] == "source: unavailable (git_show_failed)"

    def test_partial_status_preserves_skip_reasons(self) -> None:
        """Partial status surfaces precise skip reason instead of generic not-found."""
        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="source", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(
                    context_status="skipped_too_large", context_status_reason="exceeds 500000 bytes"
                ),
            }
            result = source_context_node(state)

        f = result["files"][0]
        assert f["context_status"] == "partial"
        assert f["context_status_reason"] == "target: skipped_too_large (exceeds 500000 bytes)"

    def test_invalid_numeric_review_config_values_fallback_safely(self) -> None:
        """String/invalid numeric values in review config do not crash retrieval."""
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            "config": {"review": {"context_depth": "minimal", "token_budget": "oops", "max_concurrency": "oops"}},
        }

        with patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve:
            mock_retrieve.return_value = {}
            result = source_context_node(state)

        assert len(result["files"]) == 1


class TestSourceContextNodeSupplementalCap:
    """Tests for the budget-derived supplemental request cap (FR-008)."""

    def test_supplemental_requests_capped_by_max_supplemental_per_category(self) -> None:
        """Supplemental requests are capped per category when discoveries exceed the budget-derived limit."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        # Pretend discovery returns more test paths than any reasonable budget allows.
        many_tests = [f"tests/test_mod_{i}.py" for i in range(200)]

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            # Tiny token budget: effective = 100 * 0.9 = 90 tokens
            # 2000 chars / 3.5 chars-per-token ≈ 572 tokens per file
            # → max_supplemental_per_category = min(50, max(1, 90 // 572)) = 1
            "config": {"review": {"context_depth": "standard", "token_budget": 100}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
        ):
            mock_discover.return_value = {"related_tests": many_tests, "missing_tests": False}
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="src", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(content="tgt", context_status="success"),
            }

            source_context_node(state)

        # retrieve_files_concurrent is called twice: once for the primary files and
        # once for supplemental.  Check the supplemental call (second call).
        assert mock_retrieve.call_count == 2
        supplemental_call_args = mock_retrieve.call_args_list[1].args[0]
        test_requests = [r for r in supplemental_call_args if r[2].startswith("related_test")]
        # With budget=100 tokens: effective=90, tokens_per_supplemental=ceil(2000/3.5)=572
        # → max_supplemental_per_category = min(50, max(1, 90 // 572)) = 1
        assert len(test_requests) == 1

    def test_supplemental_requests_not_capped_below_one(self) -> None:
        """Even with the smallest conceivable budget, at least 1 supplemental per category is allowed."""
        from unittest.mock import patch

        from agentic_devtools.orchestration.review.file_retriever import RetrievalResult
        from agentic_devtools.orchestration.review.nodes.source_context import source_context_node

        state = {
            "files": [{"path": "/src/app.py", "changeType": "edit"}],
            "commit_hash": "abc123",
            "base_commit_hash": "def456",
            # Smallest allowed positive budget.
            "config": {"review": {"context_depth": "standard", "token_budget": 1}},
        }

        with (
            patch("agentic_devtools.orchestration.review.file_retriever.retrieve_files_concurrent") as mock_retrieve,
            patch("agentic_devtools.orchestration.review.test_discovery.discover_related_tests") as mock_discover,
        ):
            mock_discover.return_value = {"related_tests": ["tests/test_a.py"], "missing_tests": False}
            mock_retrieve.return_value = {
                ("/src/app.py", "source"): RetrievalResult(content="src", context_status="success"),
                ("/src/app.py", "target"): RetrievalResult(content="tgt", context_status="success"),
            }

            source_context_node(state)

        assert mock_retrieve.call_count == 2
        supplemental_requests = mock_retrieve.call_args_list[1].args[0]
        test_requests = [r for r in supplemental_requests if r[2].startswith("related_test")]
        # Must have at least 1 test request (cap is max(1, ...)).
        assert len(test_requests) >= 1
