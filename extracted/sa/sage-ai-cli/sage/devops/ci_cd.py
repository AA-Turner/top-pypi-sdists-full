"""CI/CD monitoring module for SAGE DevOps.

This module provides CI/CD operations including:
- Pipeline status monitoring
- Build triggering
- Test result parsing
- Deployment status

NOTE: This is a stub implementation. Full functionality coming soon.
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from typing import Any

from sage.devops.models import CIJob, CIPipeline, JobStatus, PipelineStatus, TestResult, TestSummary


class CICDMonitor:
    """CI/CD monitoring and interaction.

    Provides monitoring and control of CI/CD pipelines.
    Currently supports:
    - GitHub Actions
    - (Future) GitLab CI
    - (Future) CircleCI
    - (Future) Jenkins
    """

    def __init__(
        self,
        repo_path: Path | str | None = None,
        provider: str = "github",
    ):
        """Initialize CI/CD monitor.

        Args:
            repo_path: Path to the repository.
            provider: CI provider ('github', 'gitlab', 'circleci', 'jenkins').
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.provider = provider
        
        # Initialize GitOps to check repo status
        from sage.devops.git import GitOps
        self.git = GitOps(self.repo_path)
        
        self._validate_setup()

        # Initialize provider-specific ops
        if provider == "github":
            from sage.devops.github import GitHubOps

            self.gh = GitHubOps(self.repo_path)

    def diagnose(self, run_id: str) -> list[Any]:
        """Diagnose failures in a pipeline run."""
        # Stub implementation
        return []

    def auto_fix(self, diagnosis: Any, commit: bool = False, push: bool = False) -> bool:
        """Attempt to automatically fix a diagnosed issue."""
        # Stub implementation
        return False

    def _validate_setup(self) -> None:
        """Validate CI/CD setup."""
        # Check for workflow files
        github_workflows = self.repo_path / ".github" / "workflows"
        gitlab_ci = self.repo_path / ".gitlab-ci.yml"
        circleci = self.repo_path / ".circleci" / "config.yml"

        self.has_github_actions = github_workflows.exists()
        self.has_gitlab_ci = gitlab_ci.exists()
        self.has_circleci = circleci.exists()

    def get_latest_run(self, branch: str | None = None, workflow: str | None = None) -> CIPipeline | None:
        """Alias for get_latest_pipeline() with optional workflow filtering."""
        # Note: current implementation ignores workflow filter as it's a stub
        return self.get_latest_pipeline(branch)

    def watch_with_progress(self, pipeline_id: str) -> CIPipeline | None:
        """Monitor a pipeline with progress updates."""
        # Stub implementation
        return self.get_pipeline(pipeline_id)

    def deploy_and_watch(
        self,
        branch: str | None = None,
        commit_message: str | None = None,
        workflow: str | None = None,
        auto_fix: bool = False,
        max_retries: int = 3,
    ) -> tuple[bool, CIPipeline | None]:
        """Full deployment flow: commit, push, watch, and optionally auto-fix."""
        # Handle commit and push if message provided
        if commit_message:
            if not self.git.is_repo:
                print("Not a git repository. Cannot commit/push.")
                return False, None
            try:
                self.git.add_all()
                self.git.commit(commit_message)
                self.git.push()
            except Exception as e:
                print(f"Git operation failed: {e}")
                return False, None

        # Trigger and watch
        pipeline = self.trigger_pipeline(branch)
        if not pipeline:
            return False, None

        status_obj = self.watch_with_progress(pipeline.id)
        
        # Simple auto-fix loop if requested
        retries = 0
        while (not status_obj or status_obj.status == PipelineStatus.FAILED) and auto_fix and retries < max_retries:
            retries += 1
            print(f"Deployment failed. Attempting auto-fix {retries}/{max_retries}...")
            # Here we would call self.diagnose and self.auto_fix
            # For now, just retry
            pipeline = self.trigger_pipeline(branch)
            if not pipeline:
                break
            status_obj = self.watch_with_progress(pipeline.id)

        return (status_obj.status == PipelineStatus.SUCCESS if status_obj else False), status_obj

    def get_pipelines(self, limit: int = 10) -> list[CIPipeline]:
        """Get recent pipeline runs.

        Args:
            limit: Maximum number of pipelines to return.

        Returns:
            List of recent pipeline runs.
        """
        if self.provider == "github" and self.has_github_actions:
            return self._get_github_pipelines(limit)
        return []

    def _get_github_pipelines(self, limit: int) -> list[CIPipeline]:
        """Get GitHub Actions workflow runs."""
        try:
            result = subprocess.run(
                [
                    "gh",
                    "run",
                    "list",
                    "--limit",
                    str(limit),
                    "--json",
                    "databaseId,displayTitle,status,conclusion,headBranch,headSha,createdAt,url,workflowName",
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(result.stdout)

            pipelines = []
            for run in data:
                status_map = {
                    "queued": PipelineStatus.PENDING,
                    "in_progress": PipelineStatus.RUNNING,
                    "completed": PipelineStatus.SUCCESS,
                }
                if run.get("conclusion") == "failure":
                    status = PipelineStatus.FAILED
                elif run.get("conclusion") == "cancelled":
                    status = PipelineStatus.CANCELLED
                else:
                    status = status_map.get(run.get("status", ""), PipelineStatus.UNKNOWN)

                pipelines.append(
                    CIPipeline(
                        id=str(run["databaseId"]),
                        status=status,
                        branch=run.get("headBranch", ""),
                        commit_sha=run.get("headSha", "")[:7],
                        url=run.get("url"),
                        conclusion=run.get("conclusion"),
                        workflow_name=run.get("workflowName", "unknown"),
                        head_branch=run.get("headBranch", "unknown"),
                    )
                )
            return pipelines
        except Exception:
            return []

    def get_pipeline(self, pipeline_id: str) -> CIPipeline | None:
        """Get a specific pipeline by ID.

        Args:
            pipeline_id: The pipeline ID.

        Returns:
            The pipeline, or None if not found.
        """
        if self.provider == "github":
            return self._get_github_pipeline(pipeline_id)
        return None

    def _get_github_pipeline(self, run_id: str) -> CIPipeline | None:
        """Get a specific GitHub Actions workflow run."""
        try:
            result = subprocess.run(
                [
                    "gh",
                    "run",
                    "view",
                    run_id,
                    "--json",
                    "databaseId,displayTitle,status,conclusion,headBranch,headSha,createdAt,url,jobs",
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            run = json.loads(result.stdout)

            status_map = {
                "queued": PipelineStatus.PENDING,
                "in_progress": PipelineStatus.RUNNING,
                "completed": PipelineStatus.SUCCESS,
            }
            if run.get("conclusion") == "failure":
                status = PipelineStatus.FAILED
            elif run.get("conclusion") == "cancelled":
                status = PipelineStatus.CANCELLED
            else:
                status = status_map.get(run.get("status", ""), PipelineStatus.UNKNOWN)

            jobs = []
            for job in run.get("jobs", []):
                job_status_map = {
                    "queued": JobStatus.PENDING,
                    "in_progress": JobStatus.RUNNING,
                    "completed": JobStatus.SUCCESS,
                }
                if job.get("conclusion") == "failure":
                    job_status = JobStatus.FAILED
                elif job.get("conclusion") == "skipped":
                    job_status = JobStatus.SKIPPED
                else:
                    job_status = job_status_map.get(job.get("status", ""), JobStatus.PENDING)

                jobs.append(
                    CIJob(
                        name=job.get("name", ""),
                        status=job_status,
                    )
                )

            return CIPipeline(
                id=str(run["databaseId"]),
                status=status,
                branch=run.get("headBranch", ""),
                commit_sha=run.get("headSha", "")[:7],
                jobs=jobs,
                url=run.get("url"),
                conclusion=run.get("conclusion"),
                workflow_name=run.get("displayTitle", "unknown"),
                head_branch=run.get("headBranch", "unknown"),
            )
        except Exception:
            return None

    def get_latest_pipeline(self, branch: str | None = None) -> CIPipeline | None:
        """Get the latest pipeline for a branch.

        Args:
            branch: Branch name. If None, uses current branch.

        Returns:
            The latest pipeline, or None if none found.
        """
        if branch is None:
            if not self.git.is_repo:
                return None
            branch = self.git.get_current_branch()

        pipelines = self.get_pipelines(limit=20)
        for p in pipelines:
            if p.branch == branch:
                return p
        return None

    def trigger_pipeline(self, branch: str | None = None) -> CIPipeline | None:
        """Trigger a new pipeline run.

        Args:
            branch: Branch to run on. If None, uses current branch.

        Returns:
            The triggered pipeline, or None if failed.
        """
        if not self.has_github_actions:
            return None

        try:
            # Get workflow files
            workflows = list((self.repo_path / ".github" / "workflows").glob("*.yml"))
            if not workflows:
                return None

            # Trigger the first workflow (usually CI)
            workflow_file = workflows[0].name
            args = ["gh", "workflow", "run", workflow_file]
            if branch:
                args.extend(["--ref", branch])

            subprocess.run(args, cwd=self.repo_path, check=True, capture_output=True)

            # Return the latest pipeline after a brief delay
            time.sleep(2)
            return self.get_latest_pipeline(branch)
        except Exception:
            return None

    def cancel_pipeline(self, pipeline_id: str) -> bool:
        """Cancel a running pipeline.

        Args:
            pipeline_id: The pipeline ID.

        Returns:
            True if cancelled successfully.
        """
        try:
            subprocess.run(
                ["gh", "run", "cancel", pipeline_id],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
            )
            return True
        except Exception:
            return False

    def get_job_logs(self, pipeline_id: str, job_name: str) -> str | None:
        """Get logs for a specific job.

        Args:
            pipeline_id: The pipeline ID.
            job_name: The job name.

        Returns:
            Job logs as string, or None if not found.
        """
        try:
            result = subprocess.run(
                ["gh", "run", "view", pipeline_id, "--log"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            # Filter logs for the specific job
            logs = result.stdout
            if job_name:
                lines = []
                in_job = False
                for line in logs.split("\n"):
                    if job_name in line:
                        in_job = True
                    if in_job:
                        lines.append(line)
                        if line.strip() == "" and len(lines) > 1:
                            break
                return "\n".join(lines) if lines else logs
            return logs
        except Exception:
            return None

    def parse_test_results(self, pipeline_id: str) -> TestSummary | None:
        """Parse test results from a pipeline.

        Args:
            pipeline_id: The pipeline ID.

        Returns:
            Test summary, or None if not available.
        """
        logs = self.get_job_logs(pipeline_id, "test")
        if not logs:
            return None

        # Parse pytest-style output
        import re

        results: list[TestResult] = []
        total = passed = failed = skipped = 0

        # Look for pytest summary line: "X passed, Y failed, Z skipped"
        summary_match = re.search(r"(\d+) passed", logs)
        if summary_match:
            passed = int(summary_match.group(1))

        summary_match = re.search(r"(\d+) failed", logs)
        if summary_match:
            failed = int(summary_match.group(1))

        summary_match = re.search(r"(\d+) skipped", logs)
        if summary_match:
            skipped = int(summary_match.group(1))

        total = passed + failed + skipped

        # Parse individual test failures
        failure_pattern = re.compile(r"FAILED (.+?)(?:\s|$)")
        for match in failure_pattern.finditer(logs):
            results.append(
                TestResult(
                    name=match.group(1),
                    passed=False,
                )
            )

        return TestSummary(
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            results=results,
        )

    def get_workflow_files(self) -> list[Path]:
        """Get list of CI workflow files."""
        files: list[Path] = []

        if self.has_github_actions:
            workflows_dir = self.repo_path / ".github" / "workflows"
            files.extend(workflows_dir.glob("*.yml"))
            files.extend(workflows_dir.glob("*.yaml"))

        if self.has_gitlab_ci:
            files.append(self.repo_path / ".gitlab-ci.yml")

        if self.has_circleci:
            files.append(self.repo_path / ".circleci" / "config.yml")

        return files

    def validate_workflow(self, workflow_path: Path) -> list[str]:
        """Validate a workflow file.

        Args:
            workflow_path: Path to the workflow file.

        Returns:
            List of validation errors (empty if valid).
        """
        # Stub implementation - basic YAML validation
        errors = []

        if not workflow_path.exists():
            errors.append(f"Workflow file not found: {workflow_path}")
            return errors

        try:
            import yaml

            with open(workflow_path) as f:
                yaml.safe_load(f)
        except ImportError:
            pass  # YAML module not available
        except Exception as e:
            errors.append(f"Invalid YAML: {e}")

        return errors
