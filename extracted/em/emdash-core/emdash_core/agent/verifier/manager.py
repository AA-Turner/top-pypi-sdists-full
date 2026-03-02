"""VerifierManager - runs verifiers and generates reports."""

import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any

from rich.console import Console

from ..providers import get_provider
from .models import VerifierConfig, VerifierResult, VerificationReport


console = Console()


class VerifierManager:
    """Manages and runs verification checks."""

    def __init__(self, repo_root: Path):
        """Initialize verifier manager.

        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root
        self.config_file = repo_root / ".emdash" / "verifiers.json"
        self.verifiers = self._load_config()

    def _load_config(self) -> list[VerifierConfig]:
        """Load verifiers from config file."""
        if not self.config_file.exists():
            return []

        try:
            data = json.loads(self.config_file.read_text())
            verifiers = []
            for v in data.get("verifiers", []):
                config = VerifierConfig.from_dict(v)
                if config.enabled:
                    verifiers.append(config)
            return verifiers
        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[yellow]Warning: Failed to load verifiers.json: {e}[/yellow]")
            return []

    def get_config(self) -> dict:
        """Get full config including max_attempts.

        Config options:
            max_attempts: Maximum number of attempts (default: 3)
                         Use 0 for infinite attempts (no limit)
        """
        if not self.config_file.exists():
            return {"verifiers": [], "max_attempts": 3}

        try:
            config = json.loads(self.config_file.read_text())
            # Support legacy max_retries as fallback
            if "max_attempts" not in config and "max_retries" in config:
                config["max_attempts"] = config["max_retries"]
            return config
        except json.JSONDecodeError:
            return {"verifiers": [], "max_attempts": 3}

    def save_config(self, config: dict) -> None:
        """Save config to file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config_file.write_text(json.dumps(config, indent=2))
        self.verifiers = self._load_config()

    def run_all(self, context: dict | None = None) -> VerificationReport:
        """Run all enabled verifiers.

        Args:
            context: Optional context dict with git_diff, goal, files_changed

        Returns:
            VerificationReport with all results
        """
        if context is None:
            context = {}

        results = []
        for verifier in self.verifiers:
            result = self._run_verifier(verifier, context)
            results.append(result)

        all_passed = all(r.passed for r in results) if results else True
        summary = self._build_summary(results)

        return VerificationReport(
            results=results,
            all_passed=all_passed,
            summary=summary,
        )

    def _run_verifier(self, config: VerifierConfig, context: dict) -> VerifierResult:
        """Run a single verifier."""
        if config.type == "command":
            return self._run_command_verifier(config)
        else:
            return self._run_llm_verifier(config, context)

    def _run_command_verifier(self, config: VerifierConfig) -> VerifierResult:
        """Run a command-based verifier."""
        if not config.command:
            return VerifierResult(
                name=config.name,
                passed=False,
                output="No command specified",
                duration=0,
                issues=["No command specified"],
            )

        start = time.time()
        try:
            result = subprocess.run(
                config.command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=config.timeout,
                cwd=self.repo_root,
            )
            passed = result.returncode == 0 if config.pass_on_exit_0 else True
            output = (result.stdout + result.stderr).strip()

            # Extract issues from output if failed
            issues = []
            if not passed:
                issues = self._extract_issues_from_output(output)

            return VerifierResult(
                name=config.name,
                passed=passed,
                output=output[:5000],  # truncate long output
                duration=time.time() - start,
                issues=issues,
            )

        except subprocess.TimeoutExpired:
            return VerifierResult(
                name=config.name,
                passed=False,
                output=f"Command timed out after {config.timeout}s",
                duration=config.timeout,
                issues=["Command timed out"],
            )
        except Exception as e:
            return VerifierResult(
                name=config.name,
                passed=False,
                output=str(e),
                duration=time.time() - start,
                issues=[str(e)],
            )

    def _run_llm_verifier(self, config: VerifierConfig, context: dict) -> VerifierResult:
        """Run an LLM-based verifier using fast_model from registry."""
        if not config.prompt:
            return VerifierResult(
                name=config.name,
                passed=False,
                output="No prompt specified",
                duration=0,
                issues=["No prompt specified"],
            )

        start = time.time()
        try:
            from ..providers.models import ModelRegistry
            registry = ModelRegistry.get()
            model = registry.fast_model or registry.default_model
            provider = get_provider(model)

            # Build prompt with context
            full_prompt = self._build_llm_prompt(config.prompt, context)

            response = provider.chat([{"role": "user", "content": full_prompt}])
            content = response.content or ""

            # Parse LLM response
            result_data = self._parse_llm_response(content)

            return VerifierResult(
                name=config.name,
                passed=result_data.get("pass", False),
                output=result_data.get("summary", content[:500]),
                duration=time.time() - start,
                issues=result_data.get("issues", []),
            )

        except Exception as e:
            return VerifierResult(
                name=config.name,
                passed=False,
                output=f"LLM error: {e}",
                duration=time.time() - start,
                issues=[str(e)],
            )

    def _build_llm_prompt(self, user_prompt: str, context: dict) -> str:
        """Build full prompt for LLM verifier."""
        parts = [user_prompt, "", "## Context"]

        if context.get("goal"):
            parts.append(f"- Goal: {context['goal']}")

        if context.get("files_changed"):
            files = context["files_changed"]
            if isinstance(files, list):
                parts.append(f"- Files changed: {', '.join(files[:10])}")

        if context.get("git_diff"):
            diff = context["git_diff"]
            # Truncate large diffs
            if len(diff) > 10000:
                diff = diff[:10000] + "\n... [truncated]"
            parts.append(f"\n## Git Diff\n```diff\n{diff}\n```")

        parts.append("""
## Response Format
Return JSON only:
{"pass": true/false, "issues": ["issue1", ...], "summary": "brief summary"}
""")

        return "\n".join(parts)

    def _parse_llm_response(self, content: str) -> dict[str, Any]:
        """Parse LLM response to extract pass/fail and issues."""
        try:
            # Try to find JSON in the response
            json_match = re.search(r"\{[\s\S]*\}", content)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "pass": data.get("pass", False),
                    "issues": data.get("issues", []),
                    "summary": data.get("summary", ""),
                }
        except json.JSONDecodeError:
            pass

        # Fallback: look for keywords
        content_lower = content.lower()
        passed = any(word in content_lower for word in ["pass", "approved", "looks good", "lgtm"])
        failed = any(word in content_lower for word in ["fail", "issue", "problem", "bug", "error"])

        return {
            "pass": passed and not failed,
            "issues": [content[:200]] if failed else [],
            "summary": content[:200],
        }

    def _extract_issues_from_output(self, output: str) -> list[str]:
        """Extract issues from command output."""
        issues = []

        # Common patterns for test failures, lint errors, etc.
        patterns = [
            r"FAIL[ED]?:?\s*(.+)",
            r"ERROR:?\s*(.+)",
            r"error:?\s*(.+)",
            r"AssertionError:?\s*(.+)",
            r"TypeError:?\s*(.+)",
            r"✗\s*(.+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE | re.MULTILINE)
            for match in matches[:5]:  # limit to 5 per pattern
                issue = match.strip()[:200]
                if issue and issue not in issues:
                    issues.append(issue)

        # If no patterns matched, use first few lines
        if not issues:
            lines = output.strip().split("\n")
            issues = [line.strip()[:200] for line in lines[:3] if line.strip()]

        return issues[:10]  # limit total issues

    def _build_summary(self, results: list[VerifierResult]) -> str:
        """Build summary string from results."""
        if not results:
            return "No verifiers configured"

        passed = sum(1 for r in results if r.passed)
        total = len(results)

        if passed == total:
            return f"All {total} verifier(s) passed"
        else:
            failed_names = [r.name for r in results if not r.passed]
            return f"{passed}/{total} passed. Failed: {', '.join(failed_names)}"
