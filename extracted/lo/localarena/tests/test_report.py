from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from localarena.evaluation import EvaluationRunner, ModelJudge, ModelTarget
from localarena.generation import GenerationRequest, GenerationResult, ModelInfo
from localarena.report import render_html_report, write_html_report
from localarena.tasks import Contains, ExactMatch, PromptTask


class StaticProvider:
    name = "static"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        return GenerationResult(
            text="<script>alert('unsafe')</script> Paris",
            provider=self.name,
            model=request.model,
            latency_seconds=0.01,
        )

    def list_models(self) -> tuple[ModelInfo, ...]:
        return (ModelInfo("model", self.name),)


class JudgeProvider:
    name = "judge-provider"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        text = (
            '{"score":0.8,"reason":"acceptable"}'
            if request.model == "judge-model"
            else "candidate answer"
        )
        return GenerationResult(
            text=text,
            provider=self.name,
            model=request.model,
        )


class HtmlReportTests(unittest.TestCase):
    def test_report_is_self_contained_and_escapes_model_output(self) -> None:
        run = EvaluationRunner(
            (ModelTarget("demo", StaticProvider(), "model"),),
            (
                PromptTask.from_text(
                    "capital",
                    "Capital of France?",
                    evaluator=Contains("Paris"),
                ),
            ),
            include_content=True,
        ).run(name="Demo <run>")

        rendered = render_html_report(run)
        self.assertIn("<!doctype html>", rendered)
        self.assertIn("Leaderboard", rendered)
        self.assertIn("Task matrix", rendered)
        self.assertIn("Judge latency (s)", rendered)
        self.assertIn("Successful / runs", rendered)
        self.assertIn("&lt;script&gt;alert", rendered)
        self.assertNotIn("<script>alert", rendered)
        self.assertNotIn("https://", rendered)
        self.assertIn('<link rel="icon" href="data:,">', rendered)

    def test_write_returns_the_destination(self) -> None:
        run = EvaluationRunner(
            (ModelTarget("demo", StaticProvider(), "model"),),
            (PromptTask.from_text("task", "prompt"),),
        ).run()
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "report.html"
            self.assertEqual(write_html_report(run, destination), destination)
            self.assertTrue(destination.read_text().startswith("<!doctype html>"))

    def test_no_content_run_does_not_render_retained_content(self) -> None:
        run = EvaluationRunner(
            (ModelTarget("model", StaticProvider(), "model"),),
            (
                PromptTask.from_text(
                    "private",
                    "<private prompt>",
                    evaluator=ExactMatch("<private expected>"),
                ),
            ),
            include_content=False,
        ).run()

        rendered = render_html_report(run)

        self.assertNotIn("&lt;script&gt;alert", rendered)
        self.assertNotIn("&lt;private prompt&gt;", rendered)
        self.assertNotIn("&lt;private expected&gt;", rendered)
        self.assertIn("Not retained", rendered)

    def test_report_keeps_safe_judge_identity_without_judge_content(self) -> None:
        provider = JudgeProvider()
        judge = ModelJudge(
            ModelTarget(
                "judge-target",
                provider,
                "judge-model",
                max_tokens=37,
            ),
            rubric="private rubric marker",
        )
        run = EvaluationRunner(
            (ModelTarget("candidate", provider, "candidate-model"),),
            (
                PromptTask.from_text(
                    "judged-task",
                    "private prompt marker",
                    evaluator=judge,
                ),
            ),
        ).run()

        rendered = render_html_report(run)

        self.assertIn("Live judges", rendered)
        self.assertIn("judge-target", rendered)
        self.assertIn("judge-provider", rendered)
        self.assertIn("judge-model", rendered)
        self.assertNotIn("private rubric marker", rendered)
        self.assertNotIn("private prompt marker", rendered)


if __name__ == "__main__":
    unittest.main()
