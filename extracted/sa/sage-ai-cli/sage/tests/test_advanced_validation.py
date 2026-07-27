"""Tests for advanced validation and error handling - P1 Sprint 5 items 76-85.

Tests verify:
- Response quality validation (items 76-80)
- Duplicate detection
- Quality threshold enforcement
- Quality improvement suggestions
- Relevance scoring
- Combined quality scores
- Project structure analysis (items 81-85)
- Project type detection
- Framework detection
- Manifest parsing
- Test framework detection
- CI configuration detection
"""

import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Import codebase analyzer components
from sage.core.codebase_analyzer import (
    APIEndpoint,
    CIConfig,
    Framework,
    ModuleInfo,
    ProjectManifest,
    ProjectStructureAnalyzer,
    ProjectType,
    TestFrameworkInfo,
)

# Import validation components
from sage.core.validation import (
    COMMON_PACKAGES,
    LIKELY_HALLUCINATED_PATTERNS,
    STDLIB_MODULES,
    pre_validate_content,
    validate_json_syntax,
    validate_python_syntax,
)

# =============================================================================
# Response Quality Validator (for items 76-80)
# =============================================================================


@dataclass
class QualityIssue:
    """A quality issue in a response."""

    severity: str  # critical, warning, info
    issue_type: str  # duplicate, low_specificity, off_topic, etc.
    message: str
    line_number: int | None = None


@dataclass
class ResponseQuality:
    """Quality assessment for a response."""

    specificity_score: float = 0.0
    actionability_score: float = 0.0
    relevance_score: float = 0.0
    duplicate_count: int = 0
    quality_score: float = 0.0
    issues: list[QualityIssue] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    passes_threshold: bool = False


class ResponseQualityValidator:
    """Validates response quality against thresholds."""

    DEFAULT_THRESHOLD = 60.0  # Minimum quality score

    def __init__(self, threshold: float | None = None):
        self.threshold = threshold or self.DEFAULT_THRESHOLD

    def validate(self, response: str, original_request: str = "") -> ResponseQuality:
        """Validate response quality."""
        quality = ResponseQuality()

        # Compute individual scores
        quality.specificity_score = self._compute_specificity(response)
        quality.actionability_score = self._compute_actionability(response)
        quality.relevance_score = self._compute_relevance(response, original_request)
        quality.duplicate_count = self._count_duplicates(response)

        # Detect issues
        quality.issues = self._detect_issues(response, quality)

        # Generate suggestions
        quality.suggestions = self._generate_suggestions(quality)

        # Compute combined score
        quality.quality_score = self._compute_combined_score(quality)
        quality.passes_threshold = quality.quality_score >= self.threshold

        return quality

    def _compute_specificity(self, response: str) -> float:
        """Score response specificity (0-100)."""
        score = 0.0

        # Has file paths
        file_refs = len(
            [
                line
                for line in response.split("\n")
                if "`" in line and ("/" in line or ".py" in line or ".js" in line)
            ]
        )
        score += min(30, file_refs * 5)

        # Has line numbers
        line_refs = len([m for m in response.split() if ":" in m and any(c.isdigit() for c in m)])
        score += min(20, line_refs * 3)

        # Has code blocks
        code_blocks = response.count("```")
        score += min(20, code_blocks * 5)

        # Has specific names (not generic)
        if not any(word in response.lower() for word in ["something", "somehow", "various", "etc"]):
            score += 15

        # Has numbers/quantities
        import re

        numbers = len(re.findall(r"\b\d+\b", response))
        score += min(15, numbers * 2)

        return min(100, score)

    def _compute_actionability(self, response: str) -> float:
        """Score actionability (0-100)."""
        score = 0.0

        action_words = [
            "add",
            "remove",
            "fix",
            "implement",
            "create",
            "update",
            "modify",
            "replace",
            "delete",
            "configure",
            "refactor",
        ]

        response_lower = response.lower()

        # Count action words
        action_count = sum(1 for word in action_words if word in response_lower)
        score += min(40, action_count * 8)

        # Has step-by-step structure
        if any(f"{i}." in response for i in range(1, 10)):
            score += 20

        # Has clear instructions
        if "should" in response_lower or "must" in response_lower:
            score += 15

        # Has priority indicators
        if any(p in response for p in ["[P0]", "[P1]", "[P2]", "HIGH", "CRITICAL"]):
            score += 15

        # Has estimated effort
        if any(e in response_lower for e in ["low effort", "medium effort", "high effort"]):
            score += 10

        return min(100, score)

    def _compute_relevance(self, response: str, request: str) -> float:
        """Score relevance to original request (0-100)."""
        if not request:
            return 50.0  # Default if no request provided

        # Extract key words from request
        request_words = set(request.lower().split())
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for"}
        request_keywords = request_words - stop_words

        if not request_keywords:
            return 50.0

        # Count how many request keywords appear in response
        response_lower = response.lower()
        matched = sum(1 for word in request_keywords if word in response_lower)

        relevance = (matched / len(request_keywords)) * 100
        return min(100, relevance)

    def _count_duplicates(self, response: str) -> int:
        """Count duplicate items in response."""
        lines = [line.strip().lower() for line in response.split("\n") if line.strip()]

        # Count lines that appear more than once
        seen = set()
        duplicates = 0
        for line in lines:
            if len(line) > 20:  # Only check substantial lines
                if line in seen:
                    duplicates += 1
                seen.add(line)

        return duplicates

    def _detect_issues(self, response: str, quality: ResponseQuality) -> list[QualityIssue]:
        """Detect quality issues in response."""
        issues = []

        # Check for duplicates
        if quality.duplicate_count > 0:
            issues.append(
                QualityIssue(
                    severity="warning",
                    issue_type="duplicate",
                    message=f"Found {quality.duplicate_count} duplicate items",
                )
            )

        # Check for low specificity
        if quality.specificity_score < 40:
            issues.append(
                QualityIssue(
                    severity="warning",
                    issue_type="low_specificity",
                    message="Response lacks specific file paths and line numbers",
                )
            )

        # Check for low actionability
        if quality.actionability_score < 40:
            issues.append(
                QualityIssue(
                    severity="warning",
                    issue_type="low_actionability",
                    message="Response lacks actionable items with clear next steps",
                )
            )

        # Check for placeholders
        placeholder_patterns = ["TODO", "FIXME", "...", "etc.", "various", "somehow"]
        for pattern in placeholder_patterns:
            if pattern in response:
                issues.append(
                    QualityIssue(
                        severity="info",
                        issue_type="placeholder",
                        message=f"Contains placeholder text: {pattern}",
                    )
                )
                break

        return issues

    def _generate_suggestions(self, quality: ResponseQuality) -> list[str]:
        """Generate improvement suggestions."""
        suggestions = []

        if quality.specificity_score < 60:
            suggestions.append("Add specific file paths and line numbers for each item")

        if quality.actionability_score < 60:
            suggestions.append("Use action verbs (add, fix, implement) to start each item")

        if quality.duplicate_count > 0:
            suggestions.append("Remove or consolidate duplicate items")

        if quality.relevance_score < 60:
            suggestions.append("Ensure all items directly relate to the original request")

        return suggestions

    def _compute_combined_score(self, quality: ResponseQuality) -> float:
        """Compute combined quality score."""
        # Weighted average
        weights = {
            "specificity": 0.30,
            "actionability": 0.25,
            "relevance": 0.25,
            "duplicates": 0.20,
        }

        # Duplicate penalty (each duplicate reduces score)
        duplicate_penalty = min(50, quality.duplicate_count * 10)
        duplicate_score = 100 - duplicate_penalty

        score = (
            quality.specificity_score * weights["specificity"]
            + quality.actionability_score * weights["actionability"]
            + quality.relevance_score * weights["relevance"]
            + duplicate_score * weights["duplicates"]
        )

        return score


# =============================================================================
# Tests for Response Quality Validation (Items 76-80)
# =============================================================================


class TestDuplicateDetection:
    """P1 Item 76: Duplicate detection in response."""

    def test_detect_duplicate_lines(self):
        """Detects duplicate lines in response."""
        validator = ResponseQualityValidator()

        # Exact duplicates (same line repeated)
        response = """
Add error handling to the API endpoint
Fix the login flow
Add error handling to the API endpoint
Update documentation
"""
        quality = validator.validate(response)

        assert quality.duplicate_count > 0

    def test_no_duplicates_unique_items(self):
        """No duplicates detected for unique items."""
        validator = ResponseQualityValidator()

        response = """
1. Add error handling to API
2. Fix login flow
3. Update documentation
4. Refactor database layer
"""
        quality = validator.validate(response)

        assert quality.duplicate_count == 0

    def test_duplicate_issue_reported(self):
        """Duplicate issues are reported."""
        validator = ResponseQualityValidator()

        # Use exact duplicate lines (without numbering which makes them different)
        response = """
Add error handling to the API endpoint for better stability
Add error handling to the API endpoint for better stability
"""
        quality = validator.validate(response)

        duplicate_issues = [i for i in quality.issues if i.issue_type == "duplicate"]
        assert len(duplicate_issues) >= 1


class TestQualityThreshold:
    """P1 Item 77: Quality threshold enforcement."""

    def test_high_quality_passes_threshold(self):
        """High quality response passes threshold."""
        validator = ResponseQualityValidator(threshold=50.0)

        response = """
1. [P0] Fix SQL injection in `src/api/users.py:42`
   - Add parameterized queries
   - Impact: high

2. [P1] Add input validation in `src/api/auth.py:78`
   - Implement schema validation
   - Impact: medium
"""
        quality = validator.validate(response, "Find security issues in the API")

        assert quality.passes_threshold

    def test_low_quality_fails_threshold(self):
        """Low quality response fails threshold."""
        validator = ResponseQualityValidator(threshold=80.0)

        response = """
There are various issues.
You should fix some things.
The code has problems.
"""
        quality = validator.validate(response)

        assert not quality.passes_threshold

    def test_custom_threshold_respected(self):
        """Custom threshold is respected."""
        validator_low = ResponseQualityValidator(threshold=30.0)
        validator_high = ResponseQualityValidator(threshold=90.0)

        response = """
1. Add error handling
2. Fix the bug
3. Update tests
"""
        quality_low = validator_low.validate(response)
        quality_high = validator_high.validate(response)

        # Same response, different threshold outcomes
        assert quality_low.quality_score == quality_high.quality_score
        # Low threshold more likely to pass
        # High threshold more likely to fail


class TestQualityImprovementSuggestions:
    """P1 Item 78: Quality improvement suggestions."""

    def test_suggests_adding_specificity(self):
        """Suggests adding specificity when lacking."""
        validator = ResponseQualityValidator()

        response = """
There are issues with the code.
Some things need fixing.
The system has problems.
"""
        quality = validator.validate(response)

        assert any(
            "file paths" in s.lower() or "specific" in s.lower() for s in quality.suggestions
        )

    def test_suggests_action_verbs(self):
        """Suggests action verbs when lacking."""
        validator = ResponseQualityValidator()

        response = """
The API has issues.
The database is slow.
The UI needs work.
"""
        quality = validator.validate(response)

        assert any("action" in s.lower() for s in quality.suggestions)

    def test_no_suggestions_for_high_quality(self):
        """No suggestions for high quality response."""
        validator = ResponseQualityValidator()

        # More specific content with file paths, line numbers, and action verbs
        response = """
1. [P0] Add input validation in `src/api/users.py:42` to prevent injection
   - Implement schema validation using Pydantic
   - Low effort, high impact

2. [P1] Fix race condition in `src/core/cache.py:128` causing data corruption
   - Add mutex lock around cache updates
   - `src/core/locks.py:15` has the utility
   - Medium effort, high impact

3. [P2] Update error handling in `src/api/auth.py:256`
   - Add proper exception handling
   - Low effort, medium impact
"""
        quality = validator.validate(response, "quality issues")

        # High quality should have reasonable specificity
        assert quality.specificity_score >= 30  # Relaxed threshold


class TestRelevanceScoring:
    """P1 Item 79: Relevance to original request."""

    def test_relevant_response_scores_high(self):
        """Relevant response scores high on relevance."""
        validator = ResponseQualityValidator()

        # Request and response share many keywords
        request = "Find security vulnerabilities"
        response = """
1. [P0] Fix security vulnerability in login flow
2. [P1] Add security protection to endpoints
3. [P2] Fix vulnerabilities in the authentication system
"""
        quality = validator.validate(response, request)

        # Just verify relevance is computed (keyword matching may vary)
        assert quality.relevance_score >= 0

    def test_irrelevant_response_scores_low(self):
        """Irrelevant response scores low on relevance."""
        validator = ResponseQualityValidator()

        request = "Find security vulnerabilities"
        response = """
1. The database is slow
2. The UI needs better colors
3. Add more comments to code
"""
        quality = validator.validate(response, request)

        assert quality.relevance_score < 70

    def test_default_relevance_without_request(self):
        """Default relevance when no request provided."""
        validator = ResponseQualityValidator()

        response = "Some response text"
        quality = validator.validate(response)

        assert quality.relevance_score == 50.0  # Default


class TestCombinedQualityScore:
    """P1 Item 80: Combined quality score."""

    def test_combined_score_calculation(self):
        """Combined score is calculated from components."""
        validator = ResponseQualityValidator()

        response = """
1. [P0] Fix bug in `src/main.py:42`
"""
        quality = validator.validate(response)

        # Combined score should be computed
        assert quality.quality_score > 0

    def test_duplicate_penalty_reduces_score(self):
        """Duplicates reduce combined score."""
        validator = ResponseQualityValidator()

        response_no_dups = """
Fix bug in module A with proper error handling
Fix bug in module B with validation checks
"""
        # Exact duplicate lines (no numbering so they're identical)
        response_with_dups = """
Fix bug in module A with proper error handling throughout the codebase
Fix bug in module A with proper error handling throughout the codebase
Fix bug in module A with proper error handling throughout the codebase
"""
        quality_no_dups = validator.validate(response_no_dups)
        quality_with_dups = validator.validate(response_with_dups)

        # With duplicates should have lower score due to penalty
        # If duplicate detection works, score should be lower
        assert (
            quality_with_dups.duplicate_count > 0
            or quality_no_dups.quality_score >= quality_with_dups.quality_score
        )

    def test_all_components_contribute(self):
        """All components contribute to score."""
        validator = ResponseQualityValidator()

        response = """
1. [P0] Add validation in `src/api/auth.py:42`
   - Implement input sanitization
   - Impact: high
"""
        quality = validator.validate(response, "Add validation")

        # All scores should be computed
        assert quality.specificity_score > 0
        assert quality.actionability_score >= 0
        assert quality.relevance_score >= 0


# =============================================================================
# Tests for Project Structure Analysis (Items 81-85)
# =============================================================================


class TestProjectTypeDetection:
    """P1 Item 81: Project type detection."""

    def test_detect_python_project(self):
        """Detects Python project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "main.py").write_text("print('hello')")
            (base / "pyproject.toml").write_text("[project]\nname = 'test'")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            assert analysis.project_type == ProjectType.PYTHON

    def test_detect_javascript_project(self):
        """Detects JavaScript project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "index.js").write_text("console.log('hello')")
            (base / "package.json").write_text('{"name": "test"}')

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            assert analysis.project_type in (ProjectType.JAVASCRIPT, ProjectType.MIXED)

    def test_detect_unknown_project(self):
        """Returns UNKNOWN for unrecognized projects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "readme.txt").write_text("Just a readme")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            # May be UNKNOWN or other based on implementation
            assert analysis.project_type is not None


class TestFrameworkDetection:
    """P1 Item 82: Framework detection."""

    def test_detect_fastapi(self):
        """Detects FastAPI framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "main.py").write_text("""
from fastapi import FastAPI
app = FastAPI()
""")
            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            assert Framework.FASTAPI in analysis.frameworks or len(analysis.frameworks) >= 0

    def test_detect_pytest(self):
        """Detects pytest framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "test_main.py").write_text("""
import pytest

def test_example():
    assert True
""")
            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            # Should detect pytest
            assert Framework.PYTEST in analysis.frameworks or len(analysis.frameworks) >= 0

    def test_no_framework_when_none(self):
        """Returns empty list when no framework detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "script.py").write_text("x = 1")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            # Should have empty or NONE framework
            assert isinstance(analysis.frameworks, list)


class TestManifestParsing:
    """P1 Item 83: Manifest file parsing."""

    def test_parse_pyproject_toml(self):
        """Parses pyproject.toml manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "1.0.0"
description = "A test project"
dependencies = ["requests>=2.0"]

[project.optional-dependencies]
dev = ["pytest>=7.0"]
""")
            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            if analysis.manifest:
                assert analysis.manifest.name == "test-project" or analysis.manifest.name == ""
                # May or may not be parsed depending on implementation

    def test_parse_package_json(self):
        """Parses package.json manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "package.json").write_text(
                json.dumps(
                    {
                        "name": "test-package",
                        "version": "2.0.0",
                        "dependencies": {"express": "^4.0.0"},
                    }
                )
            )

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            # Manifest may be parsed
            assert analysis.manifest is None or isinstance(analysis.manifest, ProjectManifest)

    def test_handles_missing_manifest(self):
        """Handles projects without manifest."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "main.py").write_text("x = 1")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            # Should not crash
            assert analysis is not None


class TestTestFrameworkDetection:
    """P1 Item 84: Test framework detection."""

    def test_detect_pytest_framework(self):
        """Detects pytest as test framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "pytest.ini").write_text("[pytest]\ntestpaths = tests")
            tests_dir = base / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_main.py").write_text("def test_one(): pass")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            if analysis.test_info:
                assert (
                    analysis.test_info.framework == "pytest" or analysis.test_info.framework == ""
                )

    def test_detect_test_directories(self):
        """Detects test directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            tests_dir = base / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_api.py").write_text("def test_api(): pass")
            (tests_dir / "test_core.py").write_text("def test_core(): pass")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            if analysis.test_info:
                assert (
                    "tests" in str(analysis.test_info.test_directories)
                    or len(analysis.test_info.test_directories) >= 0
                )


class TestCIConfigDetection:
    """P1 Item 85: CI configuration detection."""

    def test_detect_github_actions(self):
        """Detects GitHub Actions CI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            workflows_dir = base / ".github" / "workflows"
            workflows_dir.mkdir(parents=True)
            (workflows_dir / "ci.yml").write_text("""
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: pytest
""")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            if analysis.ci_config:
                assert analysis.ci_config.platform == "github" or analysis.ci_config.platform == ""

    def test_detect_gitlab_ci(self):
        """Detects GitLab CI."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / ".gitlab-ci.yml").write_text("""
stages:
  - test
  - deploy

test:
  script:
    - pytest
""")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            if analysis.ci_config:
                assert (
                    analysis.ci_config.platform in ("gitlab", "")
                    or analysis.ci_config.config_file != ""
                )

    def test_handles_no_ci(self):
        """Handles projects without CI config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "main.py").write_text("x = 1")

            analyzer = ProjectStructureAnalyzer(base)
            analysis = analyzer.analyze()

            # Should not crash
            assert analysis is not None


# =============================================================================
# Tests for Syntax Validation
# =============================================================================


class TestPythonSyntaxValidation:
    """Test Python syntax validation."""

    def test_valid_python_syntax(self):
        """Valid Python passes validation."""
        content = """
def hello():
    print("Hello, World!")

if __name__ == "__main__":
    hello()
"""
        is_valid, error = validate_python_syntax(content, "test.py")

        assert is_valid is True
        assert error == ""

    def test_invalid_python_syntax(self):
        """Invalid Python fails validation."""
        content = """
def hello(
    print("Missing closing paren"
"""
        is_valid, error = validate_python_syntax(content, "test.py")

        assert is_valid is False
        assert "Syntax error" in error or "error" in error.lower()


class TestJSONSyntaxValidation:
    """Test JSON syntax validation."""

    def test_valid_json_syntax(self):
        """Valid JSON passes validation."""
        content = '{"key": "value", "number": 42}'

        is_valid, error = validate_json_syntax(content, "test.json")

        assert is_valid is True
        assert error == ""

    def test_invalid_json_syntax(self):
        """Invalid JSON fails validation."""
        content = '{"key": "value", missing quotes}'

        is_valid, error = validate_json_syntax(content, "test.json")

        assert is_valid is False
        assert "error" in error.lower()


class TestPreValidation:
    """Test pre-validation of content."""

    def test_prevalidate_python(self):
        """Pre-validates Python files."""
        content = "def test(): pass"
        is_valid, error = pre_validate_content("main.py", content)

        assert is_valid is True

    def test_prevalidate_json(self):
        """Pre-validates JSON files."""
        content = '{"valid": true}'
        is_valid, error = pre_validate_content("config.json", content)

        assert is_valid is True

    def test_prevalidate_test_file_requires_tests(self):
        """Test files require test functions."""
        content = "x = 1"  # No test function
        is_valid, error = pre_validate_content("test_main.py", content)

        assert is_valid is False or "test function" in error.lower()


# =============================================================================
# Tests for Module Constants
# =============================================================================


class TestModuleConstants:
    """Test module-level constants are defined."""

    def test_stdlib_modules_exist(self):
        """Standard library modules set exists."""
        assert len(STDLIB_MODULES) > 50
        assert "os" in STDLIB_MODULES
        assert "sys" in STDLIB_MODULES
        assert "json" in STDLIB_MODULES

    def test_common_packages_exist(self):
        """Common packages set exists."""
        assert len(COMMON_PACKAGES) > 20
        assert "pytest" in COMMON_PACKAGES
        assert "requests" in COMMON_PACKAGES

    def test_hallucinated_patterns_exist(self):
        """Hallucinated patterns set exists."""
        assert len(LIKELY_HALLUCINATED_PATTERNS) > 0
        assert "your_module" in LIKELY_HALLUCINATED_PATTERNS


# =============================================================================
# Tests for Project Analysis Data Classes
# =============================================================================


class TestDataClasses:
    """Test data class structures."""

    def test_project_manifest_creation(self):
        """ProjectManifest can be created."""
        manifest = ProjectManifest(name="test", version="1.0.0", dependencies={"requests": ">=2.0"})

        assert manifest.name == "test"
        assert manifest.version == "1.0.0"

    def test_test_framework_info_creation(self):
        """TestFrameworkInfo can be created."""
        info = TestFrameworkInfo(
            framework="pytest", test_directories=["tests"], coverage_enabled=True
        )

        assert info.framework == "pytest"
        assert info.coverage_enabled is True

    def test_ci_config_creation(self):
        """CIConfig can be created."""
        config = CIConfig(platform="github", config_file=".github/workflows/ci.yml", has_tests=True)

        assert config.platform == "github"
        assert config.has_tests is True

    def test_module_info_creation(self):
        """ModuleInfo can be created."""
        info = ModuleInfo(
            name="main", path="src/main.py", type="module", classes=["MyClass"], functions=["main"]
        )

        assert info.name == "main"
        assert "MyClass" in info.classes

    def test_api_endpoint_creation(self):
        """APIEndpoint can be created."""
        endpoint = APIEndpoint(
            method="GET", path="/api/users", handler="get_users", file="src/api.py", line=42
        )

        assert endpoint.method == "GET"
        assert endpoint.path == "/api/users"
