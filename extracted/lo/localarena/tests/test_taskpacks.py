from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from localarena import GenerationResult, PromptTask, TaskPack
from localarena.taskpacks import (
    TASK_PACK_SCHEMA_VERSION,
    load_task_pack,
    parse_task_pack,
    task_pack_digest,
)


def _generation(text: str) -> GenerationResult:
    return GenerationResult(
        text=text,
        provider="test",
        model="test-model",
    )


class TaskPackTests(unittest.TestCase):
    def test_native_pack_is_validated_hashed_and_annotated(self) -> None:
        manifest = {
            "schema_version": 1,
            "name": "Portable smoke tasks",
            "version": "1.0.0",
            "description": "Small deterministic examples.",
            "license": "Apache-2.0",
            "source": {"kind": "example", "revision": 1},
            "tasks": [
                {
                    "id": "capital",
                    "prompt": "Capital of France?",
                    "evaluator": {
                        "type": "match",
                        "expected": ["Paris", "Paris."],
                        "mode": "exact",
                        "strip": True,
                        "ignore_case": False,
                    },
                    "metadata": {"category": "knowledge"},
                }
            ],
        }

        pack = parse_task_pack(manifest)

        self.assertEqual(TASK_PACK_SCHEMA_VERSION, 1)
        self.assertEqual(pack.name, "Portable smoke tasks")
        self.assertRegex(pack.digest, r"\Asha256:[0-9a-f]{64}\Z")
        self.assertEqual(pack.digest, task_pack_digest(manifest))
        provenance = pack.tasks[0].metadata["localarena_task_pack"]
        self.assertEqual(provenance["digest"], pack.digest)
        self.assertEqual(provenance["version"], "1.0.0")
        self.assertEqual(provenance["description"], manifest["description"])
        self.assertEqual(provenance["source"], manifest["source"])
        self.assertTrue(
            pack.tasks[0]
            .evaluator.evaluate(pack.tasks[0], _generation("Paris."))
            .passed
        )
        self.assertEqual(pack.to_dict()["digest"], pack.digest)
        reparsed = parse_task_pack(pack.to_dict())
        self.assertEqual(reparsed.digest, pack.digest)
        self.assertEqual(reparsed.format, pack.format)
        self.assertEqual(reparsed.to_dict(), pack.to_dict())

    def test_digest_normalizes_negative_zero_and_unicode_pairs(self) -> None:
        positive = task_pack_digest({"value": 0})
        negative = task_pack_digest(json.loads('{"value": -0}'))
        self.assertEqual(positive, negative)

        escaped = task_pack_digest(
            json.loads('{"value": "\\ud83d\\ude00"}')
        )
        literal = task_pack_digest({"value": "😀"})
        self.assertEqual(escaped, literal)

        with self.assertRaisesRegex(ValueError, "unpaired Unicode surrogate"):
            task_pack_digest(json.loads('{"value": "\\ud800"}'))

    def test_jsonl_auto_detects_evals_rows_and_preserves_chat_input(self) -> None:
        source = "\n".join(
            (
                json.dumps(
                    {
                        "id": "plain",
                        "input": "Return the first letter.",
                        "ideal": ["A", "A."],
                    }
                ),
                json.dumps(
                    {
                        "id": "chat",
                        "input": [
                            {"role": "system", "content": "Be brief."},
                            {"role": "user", "content": "Return B."},
                        ],
                        "ideal": "B",
                        "metadata": {"category": "chat"},
                    }
                ),
            )
        )

        pack = parse_task_pack(
            source,
            name="Imported rows",
            version="2026-07",
            license="MIT",
        )

        self.assertEqual(pack.format, "openai-evals-jsonl")
        self.assertEqual([task.id for task in pack.tasks], ["plain", "chat"])
        self.assertEqual(len(pack.tasks[1].messages), 2)
        self.assertTrue(
            pack.tasks[0]
            .evaluator.evaluate(pack.tasks[0], _generation("A. Explanation"))
            .passed
        )
        reparsed = parse_task_pack(pack.to_dict())
        self.assertEqual(reparsed.digest, pack.digest)
        self.assertEqual(reparsed.format, pack.format)

    def test_local_jsonl_and_file_loading_share_identity(self) -> None:
        source = json.dumps(
            {
                "id": "json",
                "prompt": "Return JSON.",
                "evaluator": {"type": "json", "compare": False},
            }
        )
        parsed = parse_task_pack(
            source,
            format="localarena-jsonl",
            name="Rows",
            license="CC0-1.0",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "rows.jsonl")
            path.write_text(source, encoding="utf-8")
            loaded = load_task_pack(
                path,
                format="localarena-jsonl",
                name="Rows",
                license="CC0-1.0",
            )
        self.assertEqual(loaded.digest, parsed.digest)
        self.assertEqual(loaded.tasks[0].id, "json")

    def test_rejects_missing_license_duplicates_and_reserved_metadata(self) -> None:
        base = {
            "schema_version": 1,
            "name": "Pack",
            "version": "1",
            "tasks": [{"id": "one", "prompt": "one"}],
        }
        with self.assertRaisesRegex((TypeError, ValueError), "license"):
            parse_task_pack(base)

        duplicate = {
            **base,
            "license": "MIT",
            "tasks": [
                {"id": "same", "prompt": "one"},
                {"id": "same", "prompt": "two"},
            ],
        }
        with self.assertRaisesRegex(ValueError, "unique"):
            parse_task_pack(duplicate)

        reserved = {
            **base,
            "license": "MIT",
            "tasks": [
                {
                    "id": "one",
                    "prompt": "one",
                    "metadata": {"localarena_task_pack": {}},
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "reserved"):
            parse_task_pack(reserved)

        invalid_versions = (
            {**base, "license": "MIT", "schema_version": True},
            {**base, "license": "MIT", "$schema": 1},
        )
        for invalid in invalid_versions:
            with self.subTest(invalid=invalid):
                with self.assertRaises((TypeError, ValueError)):
                    parse_task_pack(invalid)

        ambiguous = {
            **base,
            "license": "MIT",
            "tasks": [
                {
                    "id": "one",
                    "prompt": "one",
                    "messages": None,
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "either messages or prompt"):
            parse_task_pack(ambiguous)

        for digest in (
            "sha256:" + ("G" * 64),
            "sha256:" + ("a" * 63) + "_",
            "SHA256:" + ("a" * 64),
        ):
            with self.subTest(digest=digest):
                with self.assertRaisesRegex(ValueError, "sha256"):
                    parse_task_pack(
                        {
                            **base,
                            "license": "MIT",
                            "digest": digest,
                        }
                    )

    def test_constructor_keeps_manifest_identity_and_task_provenance_aligned(
        self,
    ) -> None:
        task = PromptTask.from_text("direct", "Reply yes.")
        manifest = {
            "schema_version": 1,
            "name": "Direct",
            "version": "1",
            "description": "",
            "license": "MIT",
            "source": {},
            "tasks": [task.to_dict()],
        }
        direct = TaskPack(
            name="Direct",
            version="1",
            license="MIT",
            tasks=(task,),
            digest=task_pack_digest(manifest),
            format="localarena",
        )
        provenance = direct.tasks[0].metadata["localarena_task_pack"]
        self.assertEqual(provenance["name"], direct.name)
        self.assertEqual(provenance["digest"], direct.digest)

        honest = parse_task_pack(
            {
                "schema_version": 1,
                "name": "Honest",
                "version": "1",
                "license": "MIT",
                "tasks": [{"id": "a", "prompt": "A"}],
            }
        )
        with self.assertRaisesRegex(ValueError, "manifest does not match"):
            TaskPack(
                name="Forged",
                version="9",
                license="proprietary",
                tasks=(PromptTask.from_text("b", "B"),),
                digest=honest.digest,
                format=honest.format,
                _manifest=honest.to_dict(),
            )

    def test_text_input_rejects_duplicate_keys_and_normalizes_unicode_ids(
        self,
    ) -> None:
        duplicate_key = (
            '{"schema_version":1,"name":"one","name":"two",'
            '"version":"1","license":"MIT",'
            '"tasks":[{"id":"a","prompt":"A"}]}'
        )
        with self.assertRaisesRegex(ValueError, "duplicate key"):
            parse_task_pack(duplicate_key)

        paired = "\ud83d\ude00"
        scalar = "😀"
        with self.assertRaisesRegex(ValueError, "unique"):
            parse_task_pack(
                {
                    "schema_version": 1,
                    "name": "Unicode",
                    "version": "1",
                    "license": "MIT",
                    "tasks": [
                        {"id": paired, "prompt": "A"},
                        {"id": scalar, "prompt": "B"},
                    ],
                }
            )

        for whitespace in ("\u001c", "\u0085", "\ufeff"):
            with self.subTest(code_point=ord(whitespace)):
                with self.assertRaisesRegex(ValueError, "whitespace"):
                    parse_task_pack(
                        {
                            "schema_version": 1,
                            "name": whitespace,
                            "version": "1",
                            "license": "MIT",
                            "tasks": [{"id": "a", "prompt": "A"}],
                        }
                    )


if __name__ == "__main__":
    unittest.main()
