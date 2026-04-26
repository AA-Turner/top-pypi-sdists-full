"""Tests for CLI utility functions."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from anteroom.cli.instructions import (
    find_project_instructions,
    load_instructions,
)
from anteroom.cli.repl import (
    _detect_git_branch,
    _estimate_tokens,
    _expand_file_references,
    _filter_tools_for_inline_pdf_turn,
)
from anteroom.services.document_extractor import ExtractionResult


class TestExpandFileReferences:
    def test_file_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "hello.txt"
            test_file.write_text("hello world")
            result = _expand_file_references("check @hello.txt please", tmpdir)
            assert "hello world" in result
            assert "<file" in result

    def test_directory_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            sub = Path(tmpdir) / "mydir"
            sub.mkdir()
            (sub / "a.txt").touch()
            (sub / "b.txt").touch()
            result = _expand_file_references("list @mydir/ please", tmpdir)
            assert "a.txt" in result
            assert "b.txt" in result
            assert "<directory" in result

    def test_nonexistent_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = _expand_file_references("check @nonexistent.txt", tmpdir)
            assert result == "check @nonexistent.txt"

    def test_no_references(self) -> None:
        result = _expand_file_references("hello world", "/tmp")
        assert result == "hello world"

    def test_quoted_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "my file.txt"
            test_file.write_text("spaced content")
            result = _expand_file_references('@"my file.txt"', tmpdir)
            assert "spaced content" in result

    def test_binary_file_uses_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "deck.pptx"
            test_file.write_bytes(b"PK fake pptx data")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="Extracted slide content"),
            ):
                result = _expand_file_references("check @deck.pptx", tmpdir)
                assert "Extracted slide content" in result
                assert "<file" in result

    def test_binary_file_extraction_returns_none_shows_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "deck.pptx"
            test_file.write_bytes(b"PK fake pptx data")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text=None),
            ):
                result = _expand_file_references("check @deck.pptx", tmpdir)
                assert "Binary file" in result
                assert "deck.pptx" in result
                assert "use tools to read this file" not in result

    def test_unextractable_binary_shows_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "archive.zip"
            test_file.write_bytes(b"PK\x03\x04 fake zip")
            result = _expand_file_references("check @archive.zip", tmpdir)
            assert "Binary file" in result
            assert "archive.zip" in result
            assert "use tools to read this file" not in result

    def test_xlsx_binary_uses_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "data.xlsx"
            test_file.write_bytes(b"PK fake xlsx data")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="Sheet1 data"),
            ):
                result = _expand_file_references("check @data.xlsx", tmpdir)
                assert "Sheet1 data" in result
                assert "<file" in result

    def test_pdf_binary_uses_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "report.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="PDF content here"),
            ):
                result = _expand_file_references("check @report.pdf", tmpdir)
                assert "PDF content here" in result

    def test_bare_absolute_pdf_path_uses_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "report.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="Bare PDF content"),
            ) as mock_extract:
                result = _expand_file_references(f"{test_file} what's in this pdf", tmpdir)
                assert "Bare PDF content" in result
                assert "what's in this pdf" in result
                assert f'name="{test_file.name}"' in result
                assert str(test_file) not in result
                assert 'source="inline_pdf_extraction"' in result
                assert "no file-reading tool is needed" in result
                assert "docx" not in result.lower()
                assert "Use the appropriate tool" not in result
                mock_extract.assert_called_once()

    def test_bare_quoted_pdf_path_with_spaces_uses_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "ID Card.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="Identity card content"),
            ):
                result = _expand_file_references(f'"{test_file}" summarize this', tmpdir)
                assert "Identity card content" in result
                assert "summarize this" in result
                assert f'name="{test_file.name}"' in result
                assert str(test_file) not in result
                assert "docx" not in result.lower()

    def test_bare_unquoted_pdf_path_with_spaces_uses_longest_existing_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "ID Card.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="Unquoted card content"),
            ):
                result = _expand_file_references(f"{test_file} what's in this pdf", tmpdir)
                assert "Unquoted card content" in result
                assert "what's in this pdf" in result
                assert f'name="{test_file.name}"' in result
                assert str(test_file) not in result
                assert "docx" not in result.lower()

    def test_bare_shell_escaped_pdf_path_with_spaces_uses_extractor(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "ID Card.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            escaped_path = str(test_file).replace(" ", r"\ ")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="Shell escaped card content"),
            ) as mock_extract:
                result = _expand_file_references(f"{escaped_path} what's in this pdf", tmpdir)
                assert "Shell escaped card content" in result
                assert "what's in this pdf" in result
                assert f'name="{test_file.name}"' in result
                assert str(test_file) not in result
                assert escaped_path not in result
                assert 'source="inline_pdf_extraction"' in result
                assert "docx" not in result.lower()
                mock_extract.assert_called_once()

    def test_bare_pdf_extracted_text_is_not_rescanned_for_file_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "report.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            secret_file = Path(tmpdir) / "secret.txt"
            secret_file.write_text("secret contents")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(text="PDF says @secret.txt"),
            ):
                result = _expand_file_references(f"{test_file} summarize", tmpdir)
                assert "PDF says @secret.txt" in result
                assert "secret contents" not in result

    def test_leading_bare_pdf_probe_does_not_expand_slash_command_file_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            notes = Path(tmpdir) / "notes.txt"
            notes.write_text("notes content")
            result = _expand_file_references(
                "/some-skill @notes.txt",
                tmpdir,
                leading_bare_pdf_only=True,
                expand_at_references=False,
            )
            assert result == "/some-skill @notes.txt"

    def test_bare_missing_pdf_path_is_left_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            missing_file = Path(tmpdir) / "missing.pdf"
            with patch("anteroom.services.document_extractor.extract_text") as mock_extract:
                result = _expand_file_references(f"{missing_file} what's in this pdf", tmpdir)
                assert result == f"{missing_file} what's in this pdf"
                mock_extract.assert_not_called()

    def test_bare_blocked_pdf_path_is_left_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("anteroom.services.document_extractor.extract_text") as mock_extract:
                result = _expand_file_references("/proc/blocked.pdf what's in this pdf", tmpdir)
                assert result == "/proc/blocked.pdf what's in this pdf"
                mock_extract.assert_not_called()

    def test_prose_like_pdf_token_is_left_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("anteroom.services.document_extractor.extract_text") as mock_extract:
                result = _expand_file_references("Please return report.pdf-style notes", tmpdir)
                assert result == "Please return report.pdf-style notes"
                mock_extract.assert_not_called()

    def test_pdf_extraction_warning_reports_failure_without_tool_routing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "report.pdf"
            test_file.write_bytes(b"%PDF-1.4 fake pdf")
            with patch(
                "anteroom.services.document_extractor.extract_text",
                return_value=ExtractionResult(
                    text=None,
                    warnings=["pypdf not installed - PDF text extraction unavailable"],
                ),
            ):
                result = _expand_file_references("check @report.pdf", tmpdir)
                assert "PDF text could not be extracted automatically" in result
                assert "pypdf not installed" in result
                assert str(test_file) not in result
                assert 'name="report.pdf"' in result
                assert "use tools to read this file" not in result
                assert "Use the appropriate tool" not in result

    def test_inline_pdf_turn_filters_file_and_delegation_tools(self) -> None:
        tools = [
            {"type": "function", "function": {"name": "bash"}},
            {"type": "function", "function": {"name": "docx"}},
            {"type": "function", "function": {"name": "glob_files"}},
            {"type": "function", "function": {"name": "grep"}},
            {"type": "function", "function": {"name": "pptx"}},
            {"type": "function", "function": {"name": "read_file"}},
            {"type": "function", "function": {"name": "run_agent"}},
            {"type": "function", "function": {"name": "xlsx"}},
            {"type": "function", "function": {"name": "ask_user"}},
            {"type": "function", "function": {"name": "save_memory"}},
        ]

        filtered = _filter_tools_for_inline_pdf_turn(tools)
        names = {tool["function"]["name"] for tool in filtered or []}

        assert names == {"ask_user", "save_memory"}
        assert {tool["function"]["name"] for tool in tools} >= {"bash", "run_agent"}


class TestEstimateTokens:
    def test_empty_messages(self) -> None:
        assert _estimate_tokens([]) == 0

    def test_simple_message(self) -> None:
        messages = [{"role": "user", "content": "hello world"}]
        tokens = _estimate_tokens(messages)
        assert tokens > 0

    def test_message_with_tool_calls(self) -> None:
        messages = [
            {
                "role": "assistant",
                "content": "Let me check",
                "tool_calls": [
                    {
                        "id": "call_1",
                        "type": "function",
                        "function": {
                            "name": "read_file",
                            "arguments": '{"path": "test.py"}',
                        },
                    }
                ],
            }
        ]
        tokens = _estimate_tokens(messages)
        assert tokens > 4  # More than just overhead

    def test_list_content(self) -> None:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "hello"},
                    {"type": "text", "text": "world"},
                ],
            }
        ]
        tokens = _estimate_tokens(messages)
        assert tokens > 0

    def test_special_tokens_in_content(self) -> None:
        """Regression test: tiktoken special tokens in content should not crash."""
        messages = [
            {"role": "user", "content": "Review this code with <|endoftext|> token"},
            {"role": "assistant", "content": "Found <|fim_prefix|> and <|fim_suffix|> patterns"},
        ]
        tokens = _estimate_tokens(messages)
        assert tokens > 0

    def test_special_tokens_in_tool_calls(self) -> None:
        """Regression test: special tokens in tool call args should not crash."""
        messages = [
            {
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "read_file",
                            "arguments": '{"path": "file_with_<|endoftext|>.py"}',
                        }
                    }
                ],
            }
        ]
        tokens = _estimate_tokens(messages)
        assert tokens > 0


class TestDetectGitBranch:
    def test_detect_branch(self) -> None:
        # This test assumes we're in a git repo
        branch = _detect_git_branch()
        # In CI or non-git dir, branch might be None
        if branch is not None:
            assert isinstance(branch, str)
            assert len(branch) > 0


class TestInstructions:
    def test_find_project_instructions(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            anteroom_md = Path(tmpdir) / "ANTEROOM.md"
            anteroom_md.write_text("# Project Instructions\nDo things.")
            result = find_project_instructions(tmpdir)
            assert result is not None
            assert "Project Instructions" in result

    def test_find_project_instructions_none(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = find_project_instructions(tmpdir)
            assert result is None

    def test_load_instructions_project_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            anteroom_md = Path(tmpdir) / "ANTEROOM.md"
            anteroom_md.write_text("project instructions")
            result = load_instructions(tmpdir)
            assert result is not None
            assert "project instructions" in result
