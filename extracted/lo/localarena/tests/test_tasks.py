from __future__ import annotations

import copy
import unittest

from localarena.generation import GenerationResult
from localarena.tasks import (
    ChoiceMatch,
    Contains,
    ExactMatch,
    ExtractMatch,
    JsonMatch,
    Match,
    NumericMatch,
    PromptTask,
    RegexMatch,
    TokenF1,
    evaluator_from_config,
)


def generation(text: str) -> GenerationResult:
    return GenerationResult(
        text=text,
        provider="test",
        model="test-model",
    )


class PromptTaskTests(unittest.TestCase):
    def test_text_task_builds_portable_messages(self) -> None:
        task = PromptTask.from_text(
            "capital",
            "Capital of France?",
            system="Answer briefly.",
            evaluator=ExactMatch("Paris"),
            metadata={"category": "knowledge"},
        )

        self.assertEqual(
            task.to_dict(),
            {
                "id": "capital",
                "messages": [
                    {"role": "system", "content": "Answer briefly."},
                    {"role": "user", "content": "Capital of France?"},
                ],
                "evaluator": {
                    "type": "exact",
                    "expected": "Paris",
                    "strip": True,
                    "ignore_case": False,
                },
                "metadata": {"category": "knowledge"},
            },
        )

    def test_task_requires_messages(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            PromptTask("empty", ())

    def test_task_rejects_malformed_custom_evaluator_config(self) -> None:
        class MalformedEvaluator:
            name = "custom"

            def evaluate(self, task, generated):
                return None

            def to_config(self):
                return "private evaluator detail"

        with self.assertRaises(TypeError):
            PromptTask.from_text(
                "task",
                "prompt",
                evaluator=MalformedEvaluator(),
            )

    def test_task_and_score_metadata_are_recursively_immutable(self) -> None:
        metadata = {"nested": {"values": [1, 2]}}
        task = PromptTask.from_text("task", "prompt", metadata=metadata)
        metadata["nested"]["values"].append(3)

        self.assertEqual(task.to_dict()["metadata"]["nested"]["values"], [1, 2])
        with self.assertRaises(TypeError):
            task.metadata["new"] = "value"
        self.assertIs(copy.deepcopy(task), task)


class DeterministicEvaluatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task = PromptTask.from_text("task", "prompt")

    def test_exact_match_normalization_is_explicit(self) -> None:
        score = ExactMatch("PARIS", ignore_case=True).evaluate(
            self.task,
            generation(" Paris\n"),
        )
        self.assertEqual(score.value, 1)
        self.assertTrue(score.passed)
        for source, folded in (
            ("ﬓ", "մն"),
            ("և", "եւ"),
            ("ᾲ", "ὰι"),
            ("Ꭰ", "Ꭰ"),
        ):
            with self.subTest(source=source):
                self.assertTrue(
                    ExactMatch(folded, ignore_case=True)
                    .evaluate(self.task, generation(source))
                    .passed
                )

    def test_contains_supports_all_and_any_modes(self) -> None:
        all_score = Contains(("red", "blue")).evaluate(
            self.task,
            generation("red only"),
        )
        any_score = Contains(("red", "blue"), mode="any").evaluate(
            self.task,
            generation("red only"),
        )
        self.assertEqual(all_score.value, 0)
        self.assertEqual(any_score.value, 1)
        self.assertEqual(all_score.metadata["matched"], 1)

    def test_match_supports_multiple_references_and_locations(self) -> None:
        cases = (
            (
                Match(("Paris", "Lyon"), ignore_case=True),
                " paris\n",
            ),
            (
                Match(("Final:", "Answer:"), mode="begin"),
                "Answer: 42",
            ),
            (
                Match(("41", "42"), mode="end"),
                "The result is 42",
            ),
            (
                Match(("red", "blue"), mode="any"),
                "The answer is blue.",
            ),
        )
        for evaluator, output in cases:
            with self.subTest(mode=evaluator.mode):
                self.assertTrue(
                    evaluator.evaluate(self.task, generation(output)).passed
                )
        self.assertFalse(
            Match(("cat", "dog"), mode="any")
            .evaluate(self.task, generation("bird"))
            .passed
        )
        self.assertEqual(
            Match(("Paris", "Lyon"), ignore_case=True).to_config(),
            {
                "type": "match",
                "expected": ["Paris", "Lyon"],
                "mode": "exact",
                "strip": True,
                "ignore_case": True,
            },
        )

    def test_choice_match_extracts_only_boundary_safe_leading_labels(
        self,
    ) -> None:
        evaluator = ChoiceMatch(("B",), ("A", "AA", "B"))
        score = evaluator.evaluate(self.task, generation(" (b) because"))
        self.assertTrue(score.passed)
        self.assertEqual(score.metadata["choice"], "B")
        self.assertTrue(
            ChoiceMatch(("AA",), ("A", "AA"))
            .evaluate(self.task, generation("AA is correct"))
            .passed
        )
        for output in (
            "Apple is a fruit",
            "Answer: B",
            "Because it follows",
        ):
            with self.subTest(output=output):
                self.assertFalse(
                    evaluator.evaluate(self.task, generation(output)).passed
                )
        self.assertFalse(
            ChoiceMatch(("A",), ("A", "B"))
            .evaluate(self.task, generation("A\u0301ccent"))
            .passed
        )
        with self.assertRaisesRegex(ValueError, "must occur in choices"):
            ChoiceMatch(("C",), ("A", "B"))
        with self.assertRaisesRegex(ValueError, "unique"):
            ChoiceMatch(("A",), ("A", "a"))
        with self.assertRaisesRegex(TypeError, "sequence"):
            ChoiceMatch("A", ("A",))  # type: ignore[arg-type]

    def test_extract_match_compares_capture_against_any_reference(self) -> None:
        evaluator = ExtractMatch(
            ("42", "forty-two"),
            r"####\s*([+-]?\d+)",
        )
        self.assertTrue(
            evaluator.evaluate(
                self.task,
                generation("Work shown\n#### 42"),
            ).passed
        )
        self.assertTrue(
            ExtractMatch(
                ("answer: 42",),
                r"ANSWER:\s*\d+",
                group=0,
                ignore_case=True,
            )
            .evaluate(self.task, generation("Answer: 42"))
            .passed
        )
        unavailable = ExtractMatch(("x",), r"(x)?y").evaluate(
            self.task,
            generation("y"),
        )
        self.assertFalse(unavailable.passed)
        self.assertIn("unavailable", unavailable.reason)
        self.assertFalse(
            evaluator.evaluate(self.task, generation("no final marker")).passed
        )

    def test_token_f1_uses_multisets_and_best_reference(self) -> None:
        evaluator = TokenF1(
            ("red green", "red blue green"),
            threshold=0.75,
        )
        score = evaluator.evaluate(self.task, generation("RED blue"))
        self.assertAlmostEqual(score.value, 0.8)
        self.assertTrue(score.passed)
        self.assertAlmostEqual(score.metadata["precision"], 1)
        self.assertAlmostEqual(score.metadata["recall"], 2 / 3)
        self.assertEqual(score.metadata["reference_index"], 1)
        self.assertFalse(
            TokenF1(
                ("red green", "red blue green"),
                threshold=0.9,
            )
            .evaluate(self.task, generation("red blue"))
            .passed
        )
        repeated = TokenF1(("a a b",), threshold=0).evaluate(
            self.task,
            generation("a b b"),
        )
        self.assertAlmostEqual(repeated.value, 2 / 3)
        self.assertTrue(
            TokenF1(("red blue",))
            .evaluate(self.task, generation("red\u00a0blue"))
            .passed
        )
        with self.assertRaisesRegex(ValueError, "between zero and one"):
            TokenF1(("answer",), threshold=1.1)

    def test_regex_can_search_or_require_full_output(self) -> None:
        self.assertEqual(
            RegexMatch(r"\b42\b").evaluate(
                self.task,
                generation("Answer: 42."),
            ).value,
            1,
        )
        self.assertEqual(
            RegexMatch(r"42", full_match=True).evaluate(
                self.task,
                generation("Answer: 42."),
            ).value,
            0,
        )

    def test_json_validation_and_comparison(self) -> None:
        self.assertEqual(
            JsonMatch().evaluate(
                self.task,
                generation('{"ok":true}'),
            ).value,
            1,
        )
        self.assertEqual(
            JsonMatch({"ok": True}, compare=True).evaluate(
                self.task,
                generation('{"ok":false}'),
            ).value,
            0,
        )
        invalid = JsonMatch().evaluate(self.task, generation("{"))
        self.assertFalse(invalid.passed)
        self.assertIn("invalid JSON", invalid.reason)
        self.assertFalse(
            JsonMatch().evaluate(self.task, generation("NaN")).passed
        )
        self.assertFalse(
            JsonMatch().evaluate(
                self.task,
                generation('{"a":1,"a":2}'),
            ).passed
        )
        self.assertFalse(
            JsonMatch({"value": 1}, compare=True).evaluate(
                self.task,
                generation('{"value":true}'),
            ).passed
        )
        expected = {"values": [1, 2]}
        evaluator = JsonMatch(expected, compare=True)
        expected["values"].append(3)
        self.assertEqual(
            evaluator.evaluate(
                self.task,
                generation('{"values":[1,2]}'),
            ).value,
            1,
        )

    def test_numeric_tolerance(self) -> None:
        close = NumericMatch(3.14, tolerance=0.01).evaluate(
            self.task,
            generation("3.145"),
        )
        far = NumericMatch(3.14, tolerance=0.001).evaluate(
            self.task,
            generation("3.145"),
        )
        self.assertTrue(close.passed)
        self.assertFalse(far.passed)

    def test_config_factory_rejects_unknown_types(self) -> None:
        evaluator = evaluator_from_config(
            {
                "type": "contains",
                "expected": ["a", "b"],
                "mode": "any",
            }
        )
        self.assertIsInstance(evaluator, Contains)
        for config, evaluator_type in (
            (
                {
                    "type": "match",
                    "expected": ["a", "b"],
                    "mode": "end",
                    "strip": True,
                    "ignore_case": False,
                },
                Match,
            ),
            (
                {
                    "type": "choice",
                    "expected": ["B"],
                    "choices": ["A", "B"],
                    "ignore_case": True,
                },
                ChoiceMatch,
            ),
            (
                {
                    "type": "extract",
                    "expected": ["42"],
                    "pattern": r"(\d+)",
                    "group": 1,
                    "strip": True,
                    "ignore_case": False,
                },
                ExtractMatch,
            ),
            (
                {
                    "type": "token_f1",
                    "expected": ["red blue"],
                    "threshold": 0.5,
                    "ignore_case": True,
                },
                TokenF1,
            ),
        ):
            with self.subTest(evaluator_type=evaluator_type.__name__):
                restored = evaluator_from_config(config)
                self.assertIsInstance(restored, evaluator_type)
                self.assertEqual(restored.to_config(), config)
        self.assertIsNone(evaluator_from_config(None))
        with self.assertRaisesRegex(ValueError, "unsupported"):
            evaluator_from_config({"type": "mystery"})

    def test_config_factory_rejects_unknown_fields_and_missing_type(self) -> None:
        with self.assertRaises(ValueError):
            evaluator_from_config(
                {
                    "type": "numeric",
                    "expected": 42,
                    "absolute_tolerance": 1,
                }
            )
        with self.assertRaises(TypeError):
            evaluator_from_config({"expected": "answer"})


if __name__ == "__main__":
    unittest.main()
