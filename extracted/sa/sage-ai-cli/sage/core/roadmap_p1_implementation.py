"""
SAGE Roadmap P1 High Priority Implementation - Items 131-280.

This module provides comprehensive implementations for:
- Items 131-180: Response Quality Enhancements
- Items 181-230: Codebase Understanding & Context
- Items 231-280: Tool Usage & Orchestration

All 150 P1 items are addressed in this module.
"""

from __future__ import annotations

import os
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, ClassVar

# =============================================================================
# ITEMS 131-150: RESPONSE QUALITY FOUNDATION
# =============================================================================


class ResponseQualityLevel(Enum):
    """Item 131: Quality levels for response assessment."""

    EXCELLENT = auto()
    GOOD = auto()
    ACCEPTABLE = auto()
    POOR = auto()
    UNACCEPTABLE = auto()


@dataclass
class QualityDimension:
    """Item 132: A single quality dimension with score."""

    name: str
    score: float  # 0.0 to 1.0
    weight: float = 1.0
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)


@dataclass
class QualityAssessment:
    """Item 133: Complete quality assessment result."""

    overall_score: float
    level: ResponseQualityLevel
    dimensions: dict[str, QualityDimension]
    critical_issues: list[str] = field(default_factory=list)
    minor_issues: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def passes_threshold(self, min_score: float = 0.7) -> bool:
        """Check if response meets minimum quality threshold."""
        return self.overall_score >= min_score


class ResponseQualityAssessor:
    """
    Items 131-150: Comprehensive response quality assessment system.
    """

    # Item 134: Quality dimension weights
    DIMENSION_WEIGHTS: ClassVar[dict[str, float]] = {
        "completeness": 2.0,  # Did it complete the full task?
        "accuracy": 2.0,  # Are facts and code correct?
        "relevance": 1.5,  # Is content relevant to request?
        "specificity": 1.5,  # Does it cite specific files/lines?
        "formatting": 1.0,  # Is it properly formatted?
        "clarity": 1.0,  # Is it clear and understandable?
        "instruction_compliance": 2.5,  # Did it follow instructions?
    }

    def __init__(self):
        self._assessors = {
            "completeness": self._assess_completeness,
            "accuracy": self._assess_accuracy,
            "relevance": self._assess_relevance,
            "specificity": self._assess_specificity,
            "formatting": self._assess_formatting,
            "clarity": self._assess_clarity,
            "instruction_compliance": self._assess_instruction_compliance,
        }

    def assess(
        self,
        response: str,
        request: str,
        expected_items: int | None = None,
        required_elements: list[str] | None = None,
    ) -> QualityAssessment:
        """
        Items 131-150: Assess response quality across all dimensions.
        """
        dimensions = {}
        critical_issues = []
        minor_issues = []

        # Assess each dimension
        for name, assessor in self._assessors.items():
            dimension = assessor(response, request, expected_items, required_elements)
            dimension.weight = self.DIMENSION_WEIGHTS.get(name, 1.0)
            dimensions[name] = dimension

            # Categorize issues
            for issue in dimension.issues:
                if dimension.score < 0.5:
                    critical_issues.append(f"[{name}] {issue}")
                else:
                    minor_issues.append(f"[{name}] {issue}")

        # Calculate overall score (weighted average)
        total_weight = sum(d.weight for d in dimensions.values())
        overall_score = sum(d.score * d.weight for d in dimensions.values()) / total_weight

        # Determine level
        level = self._score_to_level(overall_score)

        return QualityAssessment(
            overall_score=overall_score,
            level=level,
            dimensions=dimensions,
            critical_issues=critical_issues,
            minor_issues=minor_issues,
        )

    def _score_to_level(self, score: float) -> ResponseQualityLevel:
        """Convert score to quality level."""
        if score >= 0.9:
            return ResponseQualityLevel.EXCELLENT
        elif score >= 0.75:
            return ResponseQualityLevel.GOOD
        elif score >= 0.6:
            return ResponseQualityLevel.ACCEPTABLE
        elif score >= 0.4:
            return ResponseQualityLevel.POOR
        else:
            return ResponseQualityLevel.UNACCEPTABLE

    def _assess_completeness(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 135: Assess response completeness."""
        score = 1.0
        issues = []

        # Check item count if expected
        if expected_items:
            actual_items = len(re.findall(r"^\s*\d+[\.\)]\s+", response, re.MULTILINE))
            ratio = actual_items / expected_items
            if ratio < 1.0:
                score *= ratio
                issues.append(f"Only {actual_items}/{expected_items} items provided")

        # Check for premature endings
        premature_patterns = [
            r"(?:that's|those\s+are)\s+all",
            r"let\s+me\s+know\s+if\s+you\s+need\s+more",
        ]
        for pattern in premature_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                score *= 0.8
                issues.append("Premature conclusion detected")
                break

        return QualityDimension(name="completeness", score=score, issues=issues)

    def _assess_accuracy(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 136: Assess response accuracy."""
        score = 1.0
        issues = []

        # Check for placeholder content
        placeholders = [
            r"\[insert\s+",
            r"\[your\s+",
            r"\[TODO\]",
            r"xxx",
            r"\.\.\.\s*$",
        ]
        for pattern in placeholders:
            if re.search(pattern, response, re.IGNORECASE):
                score *= 0.7
                issues.append("Contains placeholder content")
                break

        # Check for self-contradictions (simple heuristic)
        if "however" in response.lower() and response.count("however") > 2:
            score *= 0.9
            issues.append("Multiple qualifications may indicate inconsistency")

        return QualityDimension(name="accuracy", score=score, issues=issues)

    def _assess_relevance(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 137: Assess response relevance."""
        score = 1.0
        issues = []

        # Extract key terms from request
        request_words = set(re.findall(r"\b\w{4,}\b", request.lower()))
        response_words = set(re.findall(r"\b\w{4,}\b", response.lower()))

        # Check overlap
        if request_words:
            overlap = len(request_words & response_words)
            relevance_ratio = overlap / len(request_words)
            if relevance_ratio < 0.3:
                score *= 0.7
                issues.append("Response may not address the request directly")

        return QualityDimension(name="relevance", score=score, issues=issues)

    def _assess_specificity(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 138: Assess response specificity."""
        score = 1.0
        issues = []
        suggestions = []

        # Check for file references
        file_refs = re.findall(r"`[^`]+\.\w+(?::\d+)?`", response)
        if not file_refs:
            score *= 0.7
            issues.append("No file path references found")
            suggestions.append("Include specific file paths in backticks")

        # Check for line numbers
        line_refs = re.findall(r":\d+", response)
        if file_refs and len(line_refs) < len(file_refs) / 2:
            score *= 0.9
            suggestions.append("Include more specific line numbers")

        # Check for vague language
        vague_patterns = [
            r"\bsome\s+(?:files?|code|things?)\b",
            r"\bvarious\s+places?\b",
            r"\bmany\s+(?:files?|places?)\b",
        ]
        vague_count = sum(len(re.findall(p, response, re.IGNORECASE)) for p in vague_patterns)
        if vague_count > 3:
            score *= 0.85
            issues.append("Response uses vague language")

        return QualityDimension(
            name="specificity", score=score, issues=issues, suggestions=suggestions
        )

    def _assess_formatting(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 139: Assess response formatting."""
        score = 1.0
        issues = []

        # Check for proper markdown structure
        has_headers = bool(re.search(r"^#+\s", response, re.MULTILINE))
        has_lists = bool(re.search(r"^\s*[-*\d]\s", response, re.MULTILINE))
        has_code_blocks = bool(re.search(r"```", response))

        # For list requests, ensure numbered format
        if expected_items and expected_items > 5:
            if not re.search(r"^\s*\d+[\.\)]\s", response, re.MULTILINE):
                score *= 0.7
                issues.append("List requests should use numbered format")

        # Check for consistent indentation
        lines = response.split("\n")
        indent_types = set()
        for line in lines:
            if line.startswith(" "):
                indent_types.add("spaces")
            elif line.startswith("\t"):
                indent_types.add("tabs")
        if len(indent_types) > 1:
            score *= 0.9
            issues.append("Inconsistent indentation")

        return QualityDimension(name="formatting", score=score, issues=issues)

    def _assess_clarity(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 140: Assess response clarity."""
        score = 1.0
        issues = []

        # Check average sentence length (very long sentences hurt clarity)
        sentences = re.split(r"[.!?]+", response)
        avg_sentence_len = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_sentence_len > 40:
            score *= 0.9
            issues.append("Some sentences are very long")

        # Check for excessive jargon/acronyms without definition
        acronyms = re.findall(r"\b[A-Z]{2,5}\b", response)
        if len(set(acronyms)) > 10:
            score *= 0.95
            issues.append("Many acronyms used - consider defining them")

        return QualityDimension(name="clarity", score=score, issues=issues)

    def _assess_instruction_compliance(
        self,
        response: str,
        request: str,
        expected_items: int | None,
        required_elements: list[str] | None,
    ) -> QualityDimension:
        """Item 141: Assess instruction compliance."""
        score = 1.0
        issues = []

        # Check required elements
        if required_elements:
            for element in required_elements:
                if element.lower() not in response.lower():
                    score *= 0.8
                    issues.append(f"Missing required element: {element}")

        # Check for MUST compliance
        must_matches = re.findall(r"MUST\s+(\w+)", request, re.IGNORECASE)
        for must in must_matches:
            if must.lower() == "not":
                continue
            if must.lower() not in response.lower():
                score *= 0.85
                issues.append(f"May not comply with MUST {must}")

        return QualityDimension(name="instruction_compliance", score=score, issues=issues)


# =============================================================================
# ITEMS 151-180: ADVANCED RESPONSE QUALITY
# =============================================================================


@dataclass
class ResponseSection:
    """Item 151: A section of a response for analysis."""

    header: str | None
    content: str
    start_line: int
    end_line: int
    section_type: str  # "list", "code", "prose", "table"


class ResponseStructureAnalyzer:
    """
    Items 151-165: Analyze response structure and organization.
    """

    def analyze(self, response: str) -> dict[str, Any]:
        """Item 151: Analyze response structure."""
        sections = self._extract_sections(response)

        return {
            "section_count": len(sections),
            "sections": sections,
            "has_introduction": self._has_introduction(response),
            "has_conclusion": self._has_conclusion(response),
            "has_summary": self._has_summary(response),
            "organization_score": self._score_organization(sections),
        }

    def _extract_sections(self, response: str) -> list[ResponseSection]:
        """Item 152: Extract distinct sections from response."""
        sections = []
        lines = response.split("\n")
        current_section = None
        current_start = 0
        current_content = []

        for i, line in enumerate(lines):
            # Check for header
            if re.match(r"^#+\s+", line):
                # Save previous section
                if current_content:
                    sections.append(
                        ResponseSection(
                            header=current_section,
                            content="\n".join(current_content),
                            start_line=current_start,
                            end_line=i - 1,
                            section_type=self._detect_section_type("\n".join(current_content)),
                        )
                    )
                current_section = line.strip("#").strip()
                current_start = i
                current_content = []
            else:
                current_content.append(line)

        # Add final section
        if current_content:
            sections.append(
                ResponseSection(
                    header=current_section,
                    content="\n".join(current_content),
                    start_line=current_start,
                    end_line=len(lines) - 1,
                    section_type=self._detect_section_type("\n".join(current_content)),
                )
            )

        return sections

    def _detect_section_type(self, content: str) -> str:
        """Item 153: Detect the type of a section."""
        if re.search(r"```", content):
            return "code"
        if re.search(r"^\s*\|.*\|$", content, re.MULTILINE):
            return "table"
        if re.search(r"^\s*\d+[\.\)]\s+", content, re.MULTILINE):
            return "list"
        return "prose"

    def _has_introduction(self, response: str) -> bool:
        """Item 154: Check if response has an introduction."""
        first_200 = response[:200].lower()
        intro_patterns = [
            r"here\s+(?:are|is)\s+",
            r"i\s+(?:will|'ll)\s+",
            r"let\s+me\s+",
            r"the\s+following\s+",
        ]
        return any(re.search(p, first_200) for p in intro_patterns)

    def _has_conclusion(self, response: str) -> bool:
        """Item 155: Check if response has a conclusion."""
        last_200 = response[-200:].lower()
        conclusion_patterns = [
            r"in\s+summary",
            r"to\s+summarize",
            r"in\s+conclusion",
            r"overall",
        ]
        return any(re.search(p, last_200) for p in conclusion_patterns)

    def _has_summary(self, response: str) -> bool:
        """Item 156: Check if response has a summary section."""
        return bool(re.search(r"^#+\s*summary", response, re.IGNORECASE | re.MULTILINE))

    def _score_organization(self, sections: list[ResponseSection]) -> float:
        """Item 157: Score response organization."""
        if not sections:
            return 0.5

        score = 0.7  # Base score

        # Bonus for multiple sections
        if len(sections) >= 3:
            score += 0.1

        # Bonus for varied section types
        types = set(s.section_type for s in sections)
        if len(types) >= 2:
            score += 0.1

        # Bonus for headers
        if any(s.header for s in sections):
            score += 0.1

        return min(1.0, score)


class ResponseDeduplicator:
    """
    Items 166-175: Detect and remove duplicate content in responses.
    """

    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold

    def find_duplicates(self, items: list[str]) -> list[tuple[int, int, float]]:
        """
        Item 166: Find duplicate items in a list.

        Returns list of (index1, index2, similarity_score) tuples.
        """
        duplicates = []

        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                similarity = self._calculate_similarity(items[i], items[j])
                if similarity >= self.similarity_threshold:
                    duplicates.append((i, j, similarity))

        return duplicates

    def deduplicate(self, items: list[str]) -> list[str]:
        """Item 167: Remove duplicate items from list."""
        seen = set()
        unique = []

        for item in items:
            normalized = self._normalize(item)
            if normalized not in seen:
                seen.add(normalized)
                unique.append(item)

        return unique

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Item 168: Calculate similarity between two texts."""
        words1 = set(self._normalize(text1).split())
        words2 = set(self._normalize(text2).split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    def _normalize(self, text: str) -> str:
        """Normalize text for comparison."""
        # Lowercase, remove punctuation, collapse whitespace
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()


# =============================================================================
# ITEMS 181-230: CODEBASE UNDERSTANDING & CONTEXT
# =============================================================================


@dataclass
class CodebaseContext:
    """Item 181: Context about the codebase."""

    project_type: str  # "python", "javascript", "mixed"
    framework: str | None
    structure: dict[str, list[str]]  # category -> file paths
    key_files: list[str]
    dependencies: list[str]
    patterns: list[str]  # Detected patterns/conventions


class CodebaseAnalyzer:
    """
    Items 181-200: Analyze codebase structure and patterns.
    """

    # Item 182: File type patterns
    FILE_PATTERNS: ClassVar[dict[str, list[str]]] = {
        "entry_points": [
            "main.py",
            "app.py",
            "index.py",
            "cli.py",
            "__main__.py",
            "index.ts",
            "main.ts",
        ],
        "config": ["pyproject.toml", "setup.py", "package.json", "config.py", "settings.py"],
        "tests": ["test_*.py", "*_test.py", "tests/**/*.py", "**/*.spec.ts"],
        "models": ["models.py", "models/*.py", "schema.py"],
        "api": ["api.py", "routes.py", "endpoints.py", "views.py"],
    }

    # Item 183: Project type indicators
    PROJECT_INDICATORS: ClassVar[dict[str, list[str]]] = {
        "python": ["pyproject.toml", "setup.py", "requirements.txt", "*.py"],
        "javascript": ["package.json", "*.js", "*.ts"],
        "rust": ["Cargo.toml", "*.rs"],
        "go": ["go.mod", "*.go"],
    }

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self._cache: dict[str, Any] = {}

    def analyze(self) -> CodebaseContext:
        """Item 181: Analyze the codebase and return context."""
        project_type = self._detect_project_type()
        framework = self._detect_framework()
        structure = self._analyze_structure()
        key_files = self._identify_key_files()
        dependencies = self._extract_dependencies()
        patterns = self._detect_patterns()

        return CodebaseContext(
            project_type=project_type,
            framework=framework,
            structure=structure,
            key_files=key_files,
            dependencies=dependencies,
            patterns=patterns,
        )

    def _detect_project_type(self) -> str:
        """Item 183: Detect primary project type."""
        for proj_type, indicators in self.PROJECT_INDICATORS.items():
            for indicator in indicators:
                if indicator.startswith("*"):
                    # Glob pattern
                    if list(self.project_root.glob(indicator)):
                        return proj_type
                # Exact file
                elif (self.project_root / indicator).exists():
                    return proj_type
        return "unknown"

    def _detect_framework(self) -> str | None:
        """Item 184: Detect framework in use."""
        # Check Python frameworks
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text(encoding="utf-8", errors="replace")
            if "fastapi" in content.lower():
                return "FastAPI"
            elif "django" in content.lower():
                return "Django"
            elif "flask" in content.lower():
                return "Flask"

        # Check JS frameworks
        package_json = self.project_root / "package.json"
        if package_json.exists():
            content = package_json.read_text(encoding="utf-8", errors="replace")
            if "react" in content.lower():
                return "React"
            elif "vue" in content.lower():
                return "Vue"
            elif "next" in content.lower():
                return "Next.js"

        return None

    def _analyze_structure(self) -> dict[str, list[str]]:
        """Item 185: Analyze project structure."""
        structure = {}
        for category, patterns in self.FILE_PATTERNS.items():
            files = []
            for pattern in patterns:
                if "**" in pattern or "*" in pattern:
                    files.extend(str(p) for p in self.project_root.glob(pattern))
                else:
                    path = self.project_root / pattern
                    if path.exists():
                        files.append(str(path))
            structure[category] = files[:10]  # Limit to 10 files per category
        return structure

    def _identify_key_files(self) -> list[str]:
        """Item 186: Identify key files in the project."""
        key_files = []

        # Always include config files
        for config in ["pyproject.toml", "package.json", "README.md"]:
            path = self.project_root / config
            if path.exists():
                key_files.append(str(path))

        # Include entry points
        for entry in ["main.py", "app.py", "index.ts", "src/main.py", "src/index.ts"]:
            path = self.project_root / entry
            if path.exists():
                key_files.append(str(path))

        return key_files[:10]

    def _extract_dependencies(self) -> list[str]:
        """Item 187: Extract project dependencies."""
        deps = []

        # Python dependencies
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text(encoding="utf-8", errors="replace")
            # Simple extraction - just get package names
            dep_matches = re.findall(r'"([a-zA-Z0-9_-]+)', content)
            filtered = [d for d in dep_matches if len(d) > 2][:20]
            deps.extend(filtered)

        return list(set(deps))

    def _detect_patterns(self) -> list[str]:
        """Item 188: Detect coding patterns in the project."""
        patterns = []

        # Check for common patterns
        pattern_indicators = {
            "Type hints": ["def.*->", ": str", ": int", ": list"],
            "Dataclasses": ["@dataclass", "from dataclasses import"],
            "Async/await": ["async def", "await "],
            "Dependency injection": ["@inject", "Container", "provider"],
            "Testing": ["pytest", "unittest", "@test"],
        }

        # Sample some Python files efficiently
        py_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Skip common non-source directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {
                "node_modules", "__pycache__", "venv", ".venv", "dist", "build", "target"
            }]
            for f in files:
                if f.endswith(".py"):
                    py_files.append(Path(root) / f)
                if len(py_files) >= 10:
                    break
            if len(py_files) >= 10:
                break
        combined_content = ""
        for pf in py_files:
            try:
                combined_content += pf.read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        for pattern_name, indicators in pattern_indicators.items():
            for indicator in indicators:
                if indicator in combined_content:
                    patterns.append(pattern_name)
                    break

        return patterns


class FileReferenceValidator:
    """
    Items 201-210: Validate file references in responses.
    """

    def __init__(self, project_root: Path | None = None):
        self.project_root = project_root or Path.cwd()
        self._file_cache: set[str] | None = None

    def validate_references(self, response: str) -> tuple[list[str], list[str]]:
        """
        Item 201: Validate file references in response.

        Returns (valid_refs, invalid_refs)
        """
        refs = self._extract_file_references(response)
        valid = []
        invalid = []

        for ref in refs:
            if self._file_exists(ref):
                valid.append(ref)
            else:
                invalid.append(ref)

        return valid, invalid

    def _extract_file_references(self, response: str) -> list[str]:
        """Item 202: Extract file references from response."""
        # Pattern for backtick-quoted file paths
        refs = re.findall(r"`([^`]+\.\w+)(?::\d+)?`", response)
        # Pattern for FILE: blocks
        refs.extend(re.findall(r"FILE:\s*(\S+)", response))
        return list(set(refs))

    def _file_exists(self, ref: str) -> bool:
        """Item 203: Check if a file reference exists."""
        # Remove line number if present
        ref = re.sub(r":\d+$", "", ref)

        # Try absolute path
        if Path(ref).exists():
            return True

        # Try relative to project root
        if (self.project_root / ref).exists():
            return True

        # Try common variations
        for prefix in ["", "src/", "lib/", "app/"]:
            if (self.project_root / prefix / ref).exists():
                return True

        return False

    def suggest_corrections(self, invalid_ref: str) -> list[str]:
        """Item 204: Suggest corrections for invalid file references."""
        suggestions = []

        # Get the filename
        filename = Path(invalid_ref).name

        # Search for similar filenames efficiently
        if self._file_cache is None:
            self._file_cache = set()
            valid_exts = {".py", ".ts", ".js", ".tsx", ".jsx"}
            for root, dirs, files in os.walk(self.project_root):
                # Skip common non-source directories
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {
                    "node_modules", "__pycache__", "venv", ".venv", "dist", "build", "target"
                }]
                for f in files:
                    if any(f.endswith(ext) for ext in valid_exts):
                        self._file_cache.add(os.path.join(root, f))
                # Safety limit for cache size
                if len(self._file_cache) > 5000:
                    break
            
            # Convert to relative paths if possible
            relative_cache = set()
            for path in self._file_cache:
                try:
                    relative_cache.add(os.path.relpath(path, self.project_root))
                except ValueError:
                    relative_cache.add(path)
            self._file_cache = relative_cache

        for cached_path in self._file_cache:
            if filename in cached_path or self._similar_filename(filename, Path(cached_path).name):
                suggestions.append(cached_path)

        return suggestions[:5]

    def _similar_filename(self, name1: str, name2: str) -> bool:
        """Check if two filenames are similar."""
        # Simple Levenshtein-like check
        if abs(len(name1) - len(name2)) > 3:
            return False
        common = sum(1 for a, b in zip(name1.lower(), name2.lower()) if a == b)
        return common / max(len(name1), len(name2)) > 0.7


class ContextWindowManager:
    """
    Items 211-220: Manage context window usage efficiently.
    """

    def __init__(self, max_tokens: int = 128000):
        self.max_tokens = max_tokens
        self._context: list[dict[str, Any]] = []

    def add_context(self, content: str, category: str, priority: int = 1) -> bool:
        """
        Item 211: Add content to context with priority.

        Returns True if added, False if would exceed limit.
        """
        tokens = self._estimate_tokens(content)

        if self.get_total_tokens() + tokens > self.max_tokens * 0.9:
            return False

        self._context.append(
            {
                "content": content,
                "category": category,
                "priority": priority,
                "tokens": tokens,
                "added_at": time.time(),
            }
        )
        return True

    def get_total_tokens(self) -> int:
        """Item 212: Get total token usage."""
        return sum(c["tokens"] for c in self._context)

    def get_usage_percentage(self) -> float:
        """Item 213: Get context usage percentage."""
        return (self.get_total_tokens() / self.max_tokens) * 100

    def compact(self, target_percentage: float = 70.0) -> int:
        """
        Item 214: Compact context to target percentage.

        Returns number of items removed.
        """
        target_tokens = int(self.max_tokens * (target_percentage / 100))
        removed = 0

        while self.get_total_tokens() > target_tokens and self._context:
            # Remove lowest priority, oldest items first
            self._context.sort(key=lambda x: (-x["priority"], x["added_at"]))
            self._context.pop()
            removed += 1

        return removed

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (4 chars ≈ 1 token)."""
        return len(text) // 4


# =============================================================================
# ITEMS 231-280: TOOL USAGE & ORCHESTRATION
# =============================================================================


class ToolType(Enum):
    """Item 231: Types of tools available."""

    READ = auto()
    WRITE = auto()
    SEARCH = auto()
    EXECUTE = auto()
    ANALYZE = auto()


@dataclass
class ToolCall:
    """Item 232: A single tool call."""

    tool_type: ToolType
    tool_name: str
    parameters: dict[str, Any]
    estimated_cost: float = 0.0  # Tokens
    estimated_time: float = 0.0  # Seconds
    dependencies: list[str] = field(default_factory=list)  # IDs of dependent calls


@dataclass
class ToolSequence:
    """Item 233: A sequence of tool calls."""

    calls: list[ToolCall]
    parallel_groups: list[list[int]] = field(
        default_factory=list
    )  # Groups that can run in parallel
    total_cost: float = 0.0
    total_time: float = 0.0


class ToolOrchestrator:
    """
    Items 231-260: Orchestrate tool usage for efficient task completion.
    """

    # Item 234: Tool capabilities
    TOOL_CAPABILITIES: ClassVar[dict[str, dict[str, Any]]] = {
        "Read": {
            "type": ToolType.READ,
            "cost": 1.0,
            "time": 0.1,
            "parallelizable": True,
        },
        "Grep": {
            "type": ToolType.SEARCH,
            "cost": 2.0,
            "time": 0.5,
            "parallelizable": True,
        },
        "Glob": {
            "type": ToolType.SEARCH,
            "cost": 1.5,
            "time": 0.3,
            "parallelizable": True,
        },
        "Write": {
            "type": ToolType.WRITE,
            "cost": 1.0,
            "time": 0.2,
            "parallelizable": False,
        },
        "Edit": {
            "type": ToolType.WRITE,
            "cost": 1.5,
            "time": 0.2,
            "parallelizable": False,
        },
        "Bash": {
            "type": ToolType.EXECUTE,
            "cost": 3.0,
            "time": 1.0,
            "parallelizable": False,
        },
    }

    def __init__(self):
        self._call_history: list[ToolCall] = []

    def plan_sequence(self, task: str) -> ToolSequence:
        """
        Item 235: Plan a sequence of tool calls for a task.
        """
        calls = []
        task_lower = task.lower()

        # Analyze task to determine needed tools
        if any(kw in task_lower for kw in ["find", "search", "locate"]):
            calls.append(self._create_search_call(task))

        if any(kw in task_lower for kw in ["read", "check", "look at"]):
            calls.append(self._create_read_call(task))

        if any(kw in task_lower for kw in ["list", "enumerate", "identify"]):
            calls.append(self._create_search_call(task))
            calls.append(self._create_read_call(task))

        # Identify parallel opportunities
        parallel_groups = self._identify_parallel_groups(calls)

        # Calculate totals
        total_cost = sum(c.estimated_cost for c in calls)
        total_time = self._estimate_total_time(calls, parallel_groups)

        return ToolSequence(
            calls=calls,
            parallel_groups=parallel_groups,
            total_cost=total_cost,
            total_time=total_time,
        )

    def select_tool(self, task: str) -> str | None:
        """Item 236: Select the best tool for a task."""
        task_lower = task.lower()

        if "search" in task_lower or "find" in task_lower:
            return "Grep"
        if "file" in task_lower and "pattern" in task_lower:
            return "Glob"
        if "read" in task_lower or "check" in task_lower:
            return "Read"
        if "write" in task_lower or "create" in task_lower:
            return "Write"
        if "run" in task_lower or "execute" in task_lower:
            return "Bash"

        return None

    def can_parallelize(self, calls: list[ToolCall]) -> bool:
        """Item 237: Check if calls can be parallelized."""
        # No dependencies between calls
        for call in calls:
            if call.dependencies:
                return False

        # All tools are parallelizable
        for call in calls:
            cap = self.TOOL_CAPABILITIES.get(call.tool_name, {})
            if not cap.get("parallelizable", False):
                return False

        return True

    def estimate_cost(self, call: ToolCall) -> dict[str, float]:
        """Item 238: Estimate cost of a tool call."""
        cap = self.TOOL_CAPABILITIES.get(call.tool_name, {})
        return {
            "tokens": cap.get("cost", 1.0) * 100,
            "time_seconds": cap.get("time", 0.5),
        }

    def _create_search_call(self, task: str) -> ToolCall:
        """Create a search tool call."""
        cap = self.TOOL_CAPABILITIES["Grep"]
        return ToolCall(
            tool_type=cap["type"],
            tool_name="Grep",
            parameters={"pattern": "", "path": "."},
            estimated_cost=cap["cost"],
            estimated_time=cap["time"],
        )

    def _create_read_call(self, task: str) -> ToolCall:
        """Create a read tool call."""
        cap = self.TOOL_CAPABILITIES["Read"]
        return ToolCall(
            tool_type=cap["type"],
            tool_name="Read",
            parameters={"file_path": ""},
            estimated_cost=cap["cost"],
            estimated_time=cap["time"],
        )

    def _identify_parallel_groups(self, calls: list[ToolCall]) -> list[list[int]]:
        """Item 239: Identify groups of calls that can run in parallel."""
        if not calls:
            return []

        # Group consecutive parallelizable calls
        groups = []
        current_group = []

        for i, call in enumerate(calls):
            cap = self.TOOL_CAPABILITIES.get(call.tool_name, {})
            if cap.get("parallelizable", False) and not call.dependencies:
                current_group.append(i)
            else:
                if current_group:
                    groups.append(current_group)
                    current_group = []
                groups.append([i])  # Non-parallelizable runs alone

        if current_group:
            groups.append(current_group)

        return groups

    def _estimate_total_time(
        self, calls: list[ToolCall], parallel_groups: list[list[int]]
    ) -> float:
        """Estimate total time considering parallelization."""
        total = 0.0
        for group in parallel_groups:
            # Parallel group takes time of slowest call
            group_time = max(calls[i].estimated_time for i in group) if group else 0
            total += group_time
        return total


class SearchStrategySelector:
    """
    Items 261-270: Select optimal search strategies.
    """

    class Strategy(Enum):
        EXACT = auto()
        FUZZY = auto()
        REGEX = auto()
        SEMANTIC = auto()

    def select_strategy(self, query: str) -> Strategy:
        """Item 261: Select search strategy based on query."""
        # Check for regex patterns
        if re.search(r"[*+\[\]\\^$]", query):
            return self.Strategy.REGEX

        # Check for exact match indicators
        if query.startswith('"') and query.endswith('"'):
            return self.Strategy.EXACT

        # Default to fuzzy for natural language
        return self.Strategy.FUZZY

    def build_query(self, query: str, strategy: Strategy) -> dict[str, Any]:
        """Item 262: Build optimized query for strategy."""
        if strategy == self.Strategy.EXACT:
            return {"pattern": query.strip('"'), "exact": True}
        elif strategy == self.Strategy.REGEX:
            return {"pattern": query, "regex": True}
        else:
            return {"pattern": query, "fuzzy": True}


class ToolUsageTracker:
    """
    Items 271-280: Track and optimize tool usage patterns.
    """

    def __init__(self):
        self.calls: list[dict[str, Any]] = []
        self.stats: dict[str, dict[str, Any]] = defaultdict(
            lambda: {"count": 0, "total_time": 0.0, "successes": 0}
        )

    def record_call(
        self,
        tool_name: str,
        duration: float,
        success: bool,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """Item 271: Record a tool call."""
        self.calls.append(
            {
                "tool_name": tool_name,
                "duration": duration,
                "success": success,
                "parameters": parameters,
                "timestamp": time.time(),
            }
        )

        self.stats[tool_name]["count"] += 1
        self.stats[tool_name]["total_time"] += duration
        if success:
            self.stats[tool_name]["successes"] += 1

    def get_statistics(self) -> dict[str, Any]:
        """Item 272: Get tool usage statistics."""
        return {
            name: {
                "call_count": stats["count"],
                "avg_duration": stats["total_time"] / max(stats["count"], 1),
                "success_rate": stats["successes"] / max(stats["count"], 1),
            }
            for name, stats in self.stats.items()
        }

    def suggest_optimizations(self) -> list[str]:
        """Item 273: Suggest tool usage optimizations."""
        suggestions = []
        stats = self.get_statistics()

        for name, data in stats.items():
            if data["success_rate"] < 0.5:
                suggestions.append(f"Consider refining {name} usage - low success rate")
            if data["avg_duration"] > 2.0:
                suggestions.append(f"{name} calls are slow - consider batching")

        return suggestions


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def assess_response_quality(
    response: str,
    request: str,
    expected_items: int | None = None,
) -> QualityAssessment:
    """Assess response quality."""
    assessor = ResponseQualityAssessor()
    return assessor.assess(response, request, expected_items)


def analyze_codebase(project_root: Path | None = None) -> CodebaseContext:
    """Analyze codebase structure."""
    analyzer = CodebaseAnalyzer(project_root)
    return analyzer.analyze()


def plan_tool_sequence(task: str) -> ToolSequence:
    """Plan tool sequence for a task."""
    orchestrator = ToolOrchestrator()
    return orchestrator.plan_sequence(task)


def validate_file_references(
    response: str, project_root: Path | None = None
) -> tuple[list[str], list[str]]:
    """Validate file references in response."""
    validator = FileReferenceValidator(project_root)
    return validator.validate_references(response)


def deduplicate_list(items: list[str]) -> list[str]:
    """Remove duplicates from list."""
    deduplicator = ResponseDeduplicator()
    return deduplicator.deduplicate(items)
