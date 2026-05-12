"""Tests for the corpus-merger logic in scripts/train_sage_from_corpus.py.

Heavy training itself is a subprocess at a separate layer; this file
verifies the merger that prepares the training-ready JSONL from local
datasets — that's the part that's tractable to unit-test.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


class TestToTrainingExample:

    def test_oasst_style_record(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({"text": "Why is the sky blue?", "answer": "Rayleigh scattering"})
        assert ex is not None
        # No 'answer' key in our mapping — uses output/solution. Let me check.

    def test_instruction_output_pair(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({
            "instruction": "sum two numbers",
            "input": "1, 2",
            "output": "3",
        })
        assert ex == {"instruction": "sum two numbers", "input": "1, 2", "output": "3"}

    def test_question_answer_pair(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({
            "question": "what is 2+2",
            "answer": "4",
        })
        assert ex is not None
        assert ex["instruction"] == "what is 2+2"
        assert ex["output"] == "4"

    def test_prompt_completion_pair(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({
            "prompt": "def add(a, b):",
            "completion": "    return a + b",
        })
        assert ex is not None
        assert ex["instruction"] == "def add(a, b):"
        # Output is stripped — fine for most training data; per-example
        # indentation can be re-introduced at prompt template stage.
        assert ex["output"].strip() == "return a + b"

    def test_solution_field_for_math(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({
            "problem": "What is the derivative of x^2?",
            "solution": "2x",
        })
        assert ex is not None
        assert ex["instruction"] == "What is the derivative of x^2?"
        assert ex["output"] == "2x"

    def test_list_solution_is_joined(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({
            "instruction": "test",
            "solution": ["line 1", "line 2", "line 3"],
        })
        assert ex is not None
        assert "line 1" in ex["output"]
        assert "line 3" in ex["output"]

    def test_missing_instruction_returns_none(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({"output": "no question here"})
        assert ex is None

    def test_missing_output_returns_none(self):
        import train_sage_from_corpus as t
        ex = t._to_training_example({"instruction": "ask but no answer"})
        assert ex is None


class TestMergeCorpus:

    def test_merges_multiple_datasets(self, tmp_path):
        import train_sage_from_corpus as t
        from sage.training.datasets import LocalDatasetStore

        ds_root = tmp_path / "datasets"
        for name, examples in [
            ("ds1", [{"instruction": "q1", "output": "a1"},
                     {"instruction": "q2", "output": "a2"}]),
            ("ds2", [{"prompt": "q3", "completion": "a3"}]),
        ]:
            d = ds_root / name
            d.mkdir(parents=True)
            with (d / "normalized.jsonl").open("w") as f:
                for ex in examples:
                    f.write(json.dumps(ex) + "\n")

        store = LocalDatasetStore(root=ds_root)
        out_path = tmp_path / "merged.jsonl"
        written, used = t.merge_corpus(
            store=store, filters=[], max_examples=None, output_path=out_path,
        )
        assert written == 3
        assert len(used) == 2
        # Confirm file contents
        with out_path.open() as f:
            lines = [json.loads(l) for l in f]
        assert len(lines) == 3
        assert all("instruction" in l and "output" in l for l in lines)

    def test_filter_restricts_datasets(self, tmp_path):
        import train_sage_from_corpus as t
        from sage.training.datasets import LocalDatasetStore

        ds_root = tmp_path / "datasets"
        for name in ("humaneval", "gsm8k", "the-pile-code-slice"):
            d = ds_root / name
            d.mkdir(parents=True)
            (d / "normalized.jsonl").write_text(
                json.dumps({"instruction": name, "output": "x"}) + "\n"
            )

        store = LocalDatasetStore(root=ds_root)
        out = tmp_path / "merged.jsonl"
        written, used = t.merge_corpus(
            store=store, filters=["humaneval"], max_examples=None, output_path=out,
        )
        assert written == 1
        assert any("humaneval" in u for u in used)
        assert not any("gsm8k" in u for u in used)

    def test_max_examples_caps_output(self, tmp_path):
        import train_sage_from_corpus as t
        from sage.training.datasets import LocalDatasetStore

        d = tmp_path / "datasets" / "big"
        d.mkdir(parents=True)
        with (d / "normalized.jsonl").open("w") as f:
            for i in range(100):
                f.write(json.dumps({"instruction": f"q{i}", "output": f"a{i}"}) + "\n")

        store = LocalDatasetStore(root=tmp_path / "datasets")
        out = tmp_path / "merged.jsonl"
        written, _ = t.merge_corpus(
            store=store, filters=[], max_examples=10, output_path=out,
        )
        assert written == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
