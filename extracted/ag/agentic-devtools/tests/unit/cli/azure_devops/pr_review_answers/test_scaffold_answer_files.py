"""Tests for scaffold_answer_files."""

import json

from agentic_devtools.cli.azure_devops.pr_review_answers import (
    compute_prompt_hash,
    scaffold_answer_files,
)


class TestScaffoldAnswerFiles:
    def test_scaffolds_for_each_row(self, tmp_path):
        (tmp_path / "file-a.md").write_text("PROMPT A", encoding="utf-8")
        manifest = {
            "files": [
                {
                    "fileKey": "a-key",
                    "normalizedPath": "/src/a.py",
                    "reviewMode": "diff",
                    "reviewDepth": "deep",
                    "promptFile": "file-a.md",
                },
                {
                    "fileKey": "b-key",
                    "normalizedPath": "/src/b.py",
                    "reviewMode": "diff",
                    "reviewDepth": "light",
                    "promptFile": "file-b.md",
                },
                {
                    "fileKey": "c-key",
                    "normalizedPath": "/src/c.py",
                    "reviewMode": "binary",
                    "reviewDepth": None,
                },
            ]
        }
        written = scaffold_answer_files(7, tmp_path, manifest, "deadbeef")
        answers = tmp_path / "answers"
        assert len(written) == 3

        a = json.loads((answers / "a-key.answer.json").read_text(encoding="utf-8"))
        assert a["prId"] == 7
        assert a["commitHash"] == "deadbeef"
        assert a["reviewDepth"] == "deep"
        assert a["status"] == "pending"
        assert a["filePath"] == "/src/a.py"
        assert a["promptHash"] == compute_prompt_hash("PROMPT A")

        b = json.loads((answers / "b-key.answer.json").read_text(encoding="utf-8"))
        assert b["promptHash"] == compute_prompt_hash("")

        c = json.loads((answers / "c-key.answer.json").read_text(encoding="utf-8"))
        assert c["reviewMode"] == "binary"
        assert c["promptHash"] == compute_prompt_hash("")

    def test_idempotent_skips_existing(self, tmp_path):
        manifest = {
            "files": [
                {
                    "fileKey": "a",
                    "normalizedPath": "/a",
                    "reviewMode": "diff",
                    "reviewDepth": "deep",
                    "promptFile": "x.md",
                }
            ]
        }
        first = scaffold_answer_files(1, tmp_path, manifest, "h")
        assert len(first) == 1
        second = scaffold_answer_files(1, tmp_path, manifest, "h")
        assert second == []
