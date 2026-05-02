"""
SAGE Unified Request Classification System.

This module unifies the dual classification systems (request_classifier.py and
roadmap_p0_implementation.py) into a single, coherent classification system.

Key features:
- Comprehensive quantity detection (spelled, numeric, compound, relative)
- Request type classification (analysis, generation, implementation, etc.)
- Pipeline selection based on request characteristics
- Output format determination
- Instruction extraction and compliance validation
- Priority and complexity scoring

This addresses Items 201-400 from the SAGE Ultimate Roadmap.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════


class RequestType(Enum):
    """Types of user requests."""

    ANALYSIS = auto()  # Understand/explain existing code
    LIST_GENERATION = auto()  # Generate lists of items/ideas
    IMPLEMENTATION = auto()  # Write new code
    REFACTORING = auto()  # Modify existing code
    DEBUGGING = auto()  # Find and fix bugs
    DOCUMENTATION = auto()  # Write docs/comments
    TESTING = auto()  # Write/run tests
    RESEARCH = auto()  # Explore/investigate
    QUESTION = auto()  # Answer questions
    MULTI_STEP = auto()  # Complex multi-phase task


class OutputFormat(Enum):
    """Expected output formats."""

    PLAIN_TEXT = auto()  # Simple text response
    MARKDOWN_LIST = auto()  # Bulleted/numbered list
    NUMBERED_LIST = auto()  # Numbered items (1, 2, 3...)
    TABLE = auto()  # Tabular data
    CODE_ONLY = auto()  # Just code, no explanation
    CODE_WITH_EXPLANATION = auto()  # Code + explanation
    JSON = auto()  # JSON formatted output
    DIAGRAM = auto()  # ASCII diagram or mermaid


class Pipeline(Enum):
    """Processing pipelines."""

    ANALYSIS_ONLY = auto()  # Read and analyze, no modifications
    LIST_GENERATION = auto()  # Generate lists of items
    SINGLE_FILE_EDIT = auto()  # Edit one file
    MULTI_FILE_EDIT = auto()  # Edit multiple files
    FULL_IMPLEMENTATION = auto()  # Create new functionality
    RESEARCH = auto()  # Search and investigate
    CONVERSATION = auto()  # Chat/Q&A
    MULTI_STEP = auto()  # Complex orchestrated task


class Complexity(Enum):
    """Task complexity levels."""

    TRIVIAL = 1  # One-liner, simple answer
    SIMPLE = 2  # Few lines, straightforward
    MODERATE = 3  # Multiple components, some thought
    COMPLEX = 4  # Multiple files, careful planning
    EXPERT = 5  # Architecture-level, deep expertise


# ═══════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class QuantityResult:
    """Result of quantity detection."""

    quantity: int | None = None
    modifier: str | None = None  # "over", "at least", "about", etc.
    range_max: int | None = None  # For ranges like "50-100"
    detection_method: str = "none"
    confidence: float = 0.0

    @property
    def is_exact(self) -> bool:
        """Check if this is an exact quantity (not modified)."""
        return self.modifier is None and self.range_max is None

    @property
    def minimum_required(self) -> int:
        """Get minimum required quantity."""
        if self.quantity is None:
            return 0
        if self.modifier in ("over", "more_than", "at_least", "minimum"):
            return self.quantity
        return self.quantity


@dataclass
class ClassificationResult:
    """Complete classification of a user request."""

    # Original request
    original_request: str

    # Primary classification
    request_type: RequestType = RequestType.QUESTION
    pipeline: Pipeline = Pipeline.CONVERSATION
    output_format: OutputFormat = OutputFormat.PLAIN_TEXT
    complexity: Complexity = Complexity.SIMPLE

    # Quantity detection
    quantity: QuantityResult = field(default_factory=QuantityResult)

    # Constraints
    read_only: bool = False
    must_include_code: bool = False
    must_include_file_paths: bool = False
    priority_ranking_required: bool = False

    # Extracted requirements
    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    file_patterns: list[str] = field(default_factory=list)
    explicit_instructions: list[str] = field(default_factory=list)

    # Scores
    classification_confidence: float = 0.0

    def get_summary(self) -> str:
        """Get a human-readable summary."""
        parts = [
            f"Type: {self.request_type.name}",
            f"Pipeline: {self.pipeline.name}",
            f"Format: {self.output_format.name}",
            f"Complexity: {self.complexity.name}",
        ]
        if self.quantity.quantity:
            parts.append(f"Quantity: {self.quantity.quantity}")
        if self.read_only:
            parts.append("READ-ONLY")
        return " | ".join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
# UNIFIED QUANTITY PARSER
# ═══════════════════════════════════════════════════════════════════════════════


class UnifiedQuantityParser:
    """
    Unified quantity parser merging best approaches from both systems.

    Handles all forms of quantity expression:
    - Numeric: "100 items", "50 things"
    - Spelled: "hundred", "fifty", "dozen"
    - Compound: "twenty-five", "one hundred fifty"
    - Relative: "over 100", "at least 50", "more than 200"
    - Approximate: "about 100", "around fifty", "roughly 25"
    - Ranges: "50-100", "between 50 and 100"
    - Implicit: "couple", "few", "several", "many"
    """

    # Comprehensive spelled number mapping
    SPELLED_NUMBERS: ClassVar[dict[str, int]] = {
        # Basic numbers 0-20
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        # Tens
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        # Large numbers - CRITICAL
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        # Special quantities
        "dozen": 12,
        "score": 20,
        "gross": 144,
        # Implicit quantities
        "couple": 2,
        "pair": 2,
        "few": 3,
        "several": 5,
        "many": 10,
        "some": 5,
        "numerous": 20,
        "lots": 20,
        "plenty": 20,
    }

    # Modifier keywords
    QUANTITY_MODIFIERS: ClassVar[dict[str, str]] = {
        "over": "over",
        "at least": "at_least",
        "more than": "more_than",
        "minimum of": "minimum",
        "minimum": "minimum",
        "about": "approximate",
        "around": "approximate",
        "roughly": "approximate",
        "approximately": "approximate",
        "nearly": "approximate",
        "almost": "approximate",
        "up to": "up_to",
        "under": "under",
        "less than": "less_than",
        "fewer than": "less_than",
        "no more than": "maximum",
        "maximum of": "maximum",
    }

    # List item indicators
    LIST_INDICATORS: ClassVar[list[str]] = [
        "things",
        "items",
        "improvements",
        "issues",
        "problems",
        "suggestions",
        "recommendations",
        "changes",
        "fixes",
        "points",
        "results",
        "examples",
        "features",
        "bugs",
        "tasks",
        "steps",
        "ideas",
        "concepts",
        "errors",
        "warnings",
        "tips",
        "notes",
        "questions",
        "answers",
        "options",
        "ways",
        "methods",
        "approaches",
        "techniques",
        "patterns",
        "practices",
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns for efficiency."""
        # Modifier pattern
        modifier_parts = "|".join(re.escape(m) for m in self.QUANTITY_MODIFIERS.keys())
        self._modifier_pattern = re.compile(rf"\b({modifier_parts})\s+", re.IGNORECASE)

        # Range pattern
        self._range_pattern = re.compile(r"\b(\d+)\s*(?:[-–]|to)\s*(\d+)\b", re.IGNORECASE)

        # Between pattern
        self._between_pattern = re.compile(r"\bbetween\s+(\d+)\s+and\s+(\d+)\b", re.IGNORECASE)

        # List indicator pattern
        indicators = "|".join(self.LIST_INDICATORS)
        self._list_indicator_pattern = re.compile(rf"\b(?:{indicators})\b", re.IGNORECASE)

        # Compound spelled number patterns
        tens = "twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety"
        ones = "one|two|three|four|five|six|seven|eight|nine"
        self._compound_tens_ones = re.compile(rf"\b({tens})[- ]?({ones})\b", re.IGNORECASE)

        # "X hundred Y" pattern
        self._hundreds_pattern = re.compile(
            rf"\b({ones}|two|three|four|five|six|seven|eight|nine|ten)\s+hundred\s*(?:and\s+)?({ones}|{tens})?\b",
            re.IGNORECASE,
        )

    def parse(self, text: str) -> QuantityResult:
        """
        Parse quantity from text with comprehensive detection.

        Returns QuantityResult with detected quantity and metadata.
        """
        text_lower = text.lower()
        result = QuantityResult()

        # Priority 1: Check for explicit numeric with modifier
        if modified := self._parse_modified_numeric(text_lower):
            return modified

        # Priority 2: Check for ranges
        if range_result := self._parse_range(text_lower):
            return range_result

        # Priority 3: Check compound spelled numbers
        if compound := self._parse_compound_spelled(text_lower):
            return compound

        # Priority 4: Check numeric with list indicator
        if numeric := self._parse_numeric_with_context(text_lower):
            return numeric

        # Priority 5: Check single spelled numbers
        if spelled := self._parse_single_spelled(text_lower):
            return spelled

        # Priority 6: Check implicit quantities
        if implicit := self._parse_implicit(text_lower):
            return implicit

        return result  # No quantity detected

    def _parse_modified_numeric(self, text: str) -> QuantityResult | None:
        """Parse modified numeric quantities like 'over 100', 'at least 50'."""
        for modifier_text, modifier_type in self.QUANTITY_MODIFIERS.items():
            pattern = rf"\b{re.escape(modifier_text)}\s+(\d+)\b"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return QuantityResult(
                    quantity=int(match.group(1)),
                    modifier=modifier_type,
                    detection_method="modified_numeric",
                    confidence=0.95,
                )
        return None

    def _parse_range(self, text: str) -> QuantityResult | None:
        """Parse range expressions like '50-100' or 'between 50 and 100'."""
        # Check "X-Y" or "X to Y"
        match = self._range_pattern.search(text)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                range_max=int(match.group(2)),
                detection_method="range",
                confidence=0.9,
            )

        # Check "between X and Y"
        match = self._between_pattern.search(text)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                range_max=int(match.group(2)),
                detection_method="range",
                confidence=0.9,
            )

        return None

    def _parse_compound_spelled(self, text: str) -> QuantityResult | None:
        """Parse compound spelled numbers like 'twenty-five' or 'one hundred fifty'."""
        # Check "X hundred Y"
        match = self._hundreds_pattern.search(text)
        if match:
            hundreds = self.SPELLED_NUMBERS.get(match.group(1).lower(), 0) * 100
            remainder = self.SPELLED_NUMBERS.get(match.group(2).lower(), 0) if match.group(2) else 0
            return QuantityResult(
                quantity=hundreds + remainder,
                detection_method="compound_hundreds",
                confidence=0.95,
            )

        # Check "twenty-five" style
        match = self._compound_tens_ones.search(text)
        if match:
            tens = self.SPELLED_NUMBERS.get(match.group(1).lower(), 0)
            ones = self.SPELLED_NUMBERS.get(match.group(2).lower(), 0)
            return QuantityResult(
                quantity=tens + ones,
                detection_method="compound_tens",
                confidence=0.95,
            )

        return None

    def _parse_numeric_with_context(self, text: str) -> QuantityResult | None:
        """Parse numeric quantities with list indicators."""
        # Pattern: "100 items", "50 different things"
        pattern = r"\b(\d+)\s+(?:different\s+)?(?:" + "|".join(self.LIST_INDICATORS) + r")\b"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                detection_method="numeric_with_context",
                confidence=0.95,
            )

        # Pattern: "list/give/provide X"
        verbs = r"list|give|provide|show|find|identify|create|generate|write"
        pattern = rf"\b(?:{verbs})\s+(\d+)\b"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                detection_method="verb_numeric",
                confidence=0.9,
            )

        # Pattern: "first/top X"
        pattern = r"\b(?:first|top)\s+(\d+)\b"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return QuantityResult(
                quantity=int(match.group(1)),
                detection_method="ordinal_numeric",
                confidence=0.9,
            )

        return None

    def _parse_single_spelled(self, text: str) -> QuantityResult | None:
        """Parse single spelled numbers like 'hundred' or 'fifty'."""
        # Check if text has list indicator context
        has_list_context = bool(self._list_indicator_pattern.search(text))

        for word, value in sorted(
            self.SPELLED_NUMBERS.items(), key=lambda x: -len(x[0])
        ):  # Longer words first
            if value >= 10:  # Skip small implicit quantities
                pattern = rf"\b{re.escape(word)}\b"
                if re.search(pattern, text, re.IGNORECASE):
                    return QuantityResult(
                        quantity=value,
                        detection_method="spelled_single",
                        confidence=0.9 if has_list_context else 0.7,
                    )

        return None

    def _parse_implicit(self, text: str) -> QuantityResult | None:
        """Parse implicit quantities like 'couple', 'few', 'several'."""
        implicit_words = [
            "couple",
            "pair",
            "few",
            "several",
            "many",
            "some",
            "numerous",
            "lots",
            "plenty",
        ]

        for word in implicit_words:
            pattern = rf"\b{word}\b"
            if re.search(pattern, text, re.IGNORECASE):
                return QuantityResult(
                    quantity=self.SPELLED_NUMBERS.get(word, 5),
                    detection_method="implicit",
                    confidence=0.6,
                )

        return None


# ═══════════════════════════════════════════════════════════════════════════════
# UNIFIED REQUEST CLASSIFIER
# ═══════════════════════════════════════════════════════════════════════════════


class UnifiedRequestClassifier:
    """
    Unified request classifier that combines the best of both classification systems.

    Features:
    - Request type detection (analysis, implementation, debugging, etc.)
    - Pipeline selection (read-only, single-file, multi-file, etc.)
    - Output format determination (list, code, table, etc.)
    - Complexity estimation
    - Language/framework detection
    - Explicit instruction extraction
    """

    # Request type indicators
    ANALYSIS_INDICATORS: ClassVar[list[str]] = [
        "analyze",
        "explain",
        "describe",
        "understand",
        "what is",
        "what are",
        "how does",
        "why does",
        "review",
        "assess",
        "evaluate",
        "examine",
        "look at",
        "tell me about",
        "show me",
        "help me understand",
    ]

    LIST_INDICATORS: ClassVar[list[str]] = [
        "list",
        "enumerate",
        "give me",
        "provide",
        "show me all",
        "what are all",
        "identify all",
        "find all",
        "compile",
        "gather",
        "collect",
    ]

    IMPLEMENTATION_INDICATORS: ClassVar[list[str]] = [
        "implement",
        "create",
        "build",
        "write",
        "develop",
        "code",
        "make",
        "add",
        "generate",
        "produce",
        "design",
        "construct",
    ]

    DEBUGGING_INDICATORS: ClassVar[list[str]] = [
        "fix",
        "debug",
        "debugging",
        "solve",
        "resolve",
        "troubleshoot",
        "diagnose",
        "repair",
        "correct",
        "patch",
        "address",
        "bug",
        "bugs",
        "error",
        "errors",
        "issue",
        "issues",
        "fix the",
        "debug the",
        "fix bug",
        "debug bug",
    ]

    REFACTORING_INDICATORS: ClassVar[list[str]] = [
        "refactor",
        "improve",
        "optimize",
        "clean up",
        "restructure",
        "reorganize",
        "simplify",
        "modernize",
        "update",
        "enhance",
    ]

    DOCUMENTATION_INDICATORS: ClassVar[list[str]] = [
        "document",
        "documentation",
        "add comments",
        "write docs",
        "docstring",
        "docstrings",
        "readme",
        "api documentation",
        "explain in comments",
        "write documentation",
        "document the",
        "documenting",
    ]

    TESTING_INDICATORS: ClassVar[list[str]] = [
        "test",
        "tests",
        "write tests",
        "unit test",
        "unit tests",
        "integration test",
        "add tests",
        "test coverage",
        "create tests",
        "testing",
        "test cases",
        "test case",
        "test suite",
        "pytest",
        "unittest",
    ]

    READ_ONLY_INDICATORS: ClassVar[list[str]] = [
        "don't modify",
        "don't change",
        "don't edit",
        "do not modify",
        "do not change",
        "read only",
        "just analyze",
        "just explain",
        "without changing",
        "without modifying",
        "leave unchanged",
        "don't write",
        "don't create",
        "only analyze",
        "only explain",
        "just tell me",
        "without fixing",
        "don't fix",
        "do not fix",
        "tell me what",
        "what's wrong",
        "what is wrong",
        "only tell",
    ]

    # Programming languages and their extensions
    LANGUAGES: ClassVar[dict[str, list[str]]] = {
        "python": [".py", "python", "py"],
        "javascript": [".js", "javascript", "js"],
        "typescript": [".ts", ".tsx", "typescript", "ts"],
        "rust": [".rs", "rust"],
        "go": [".go", "golang", "go"],
        "java": [".java", "java"],
        "cpp": [".cpp", ".cc", ".cxx", "c++", "cpp"],
        "c": [".c", ".h"],
        "ruby": [".rb", "ruby"],
        "php": [".php", "php"],
        "swift": [".swift", "swift"],
        "kotlin": [".kt", "kotlin"],
        "scala": [".scala", "scala"],
        "shell": [".sh", ".bash", "bash", "shell", "zsh"],
    }

    # Frameworks
    FRAMEWORKS: ClassVar[dict[str, list[str]]] = {
        "react": ["react", "jsx", "tsx"],
        "vue": ["vue", ".vue"],
        "angular": ["angular", "ng"],
        "django": ["django"],
        "flask": ["flask"],
        "fastapi": ["fastapi"],
        "express": ["express", "express.js"],
        "nextjs": ["next.js", "nextjs"],
        "rails": ["rails", "ruby on rails"],
        "spring": ["spring", "spring boot"],
        "laravel": ["laravel"],
        "tensorflow": ["tensorflow", "tf"],
        "pytorch": ["pytorch", "torch"],
    }

    def __init__(self):
        self.quantity_parser = UnifiedQuantityParser()
        self._compile_patterns()

    def _compile_patterns(self):
        """Compile regex patterns."""

        # Combine indicators into patterns
        def make_pattern(indicators: list[str]) -> re.Pattern:
            escaped = [re.escape(i) for i in indicators]
            return re.compile(r"\b(" + "|".join(escaped) + r")\b", re.IGNORECASE)

        self._analysis_pattern = make_pattern(self.ANALYSIS_INDICATORS)
        self._list_pattern = make_pattern(self.LIST_INDICATORS)
        self._implementation_pattern = make_pattern(self.IMPLEMENTATION_INDICATORS)
        self._debugging_pattern = make_pattern(self.DEBUGGING_INDICATORS)
        self._refactoring_pattern = make_pattern(self.REFACTORING_INDICATORS)
        self._documentation_pattern = make_pattern(self.DOCUMENTATION_INDICATORS)
        self._testing_pattern = make_pattern(self.TESTING_INDICATORS)
        self._read_only_pattern = make_pattern(self.READ_ONLY_INDICATORS)

        # File path patterns
        self._file_path_pattern = re.compile(
            r"(?:^|[\s\"'\(])([/\w\-\.]+\.(?:py|js|ts|tsx|jsx|rs|go|java|cpp|c|rb|php|swift|kt|scala|sh|md|json|yaml|yml|toml))(?:[\s\"'\)]|$)",
            re.IGNORECASE,
        )

        # Priority/ranking indicators
        self._priority_pattern = re.compile(
            r"\b(?:priorit|prioritize|prioritized|priority|priorities|rank|ranking|rankings|ranked|order|ordered|sort|sorted|p0|p1|p2|p3|critical|high|medium|low|urgent|important|severity)\b",
            re.IGNORECASE,
        )

    def classify(self, request: str) -> ClassificationResult:
        """
        Classify a user request with full analysis.

        Returns ClassificationResult with all detected attributes.
        """
        result = ClassificationResult(original_request=request)
        text_lower = request.lower()

        # Parse quantity
        result.quantity = self.quantity_parser.parse(request)

        # Check read-only constraint first
        result.read_only = bool(self._read_only_pattern.search(text_lower))

        # Detect request type
        result.request_type = self._detect_request_type(text_lower)

        # Determine output format
        result.output_format = self._determine_output_format(text_lower, result)

        # Select pipeline
        result.pipeline = self._select_pipeline(result)

        # Estimate complexity
        result.complexity = self._estimate_complexity(request, result)

        # Extract languages and frameworks
        result.languages = self._detect_languages(text_lower)
        result.frameworks = self._detect_frameworks(text_lower)

        # Extract file patterns
        result.file_patterns = self._file_path_pattern.findall(request)

        # Check for priority ranking requirement
        result.priority_ranking_required = bool(self._priority_pattern.search(text_lower))

        # Extract explicit instructions
        result.explicit_instructions = self._extract_instructions(request)

        # Set code requirement
        result.must_include_code = result.request_type in (
            RequestType.IMPLEMENTATION,
            RequestType.DEBUGGING,
            RequestType.REFACTORING,
            RequestType.TESTING,
        )

        # Calculate confidence
        result.classification_confidence = self._calculate_confidence(result)

        return result

    def _detect_request_type(self, text: str) -> RequestType:
        """Detect the primary request type."""
        # Score each type with appropriate weights
        # Higher specificity types get higher multipliers
        scores = {
            RequestType.DEBUGGING: len(self._debugging_pattern.findall(text)) * 3.0,
            RequestType.TESTING: len(self._testing_pattern.findall(text)) * 2.5,
            RequestType.DOCUMENTATION: len(self._documentation_pattern.findall(text)) * 2.5,
            RequestType.REFACTORING: len(self._refactoring_pattern.findall(text)) * 2.0,
            RequestType.LIST_GENERATION: len(self._list_pattern.findall(text)) * 2.0,
            RequestType.ANALYSIS: len(self._analysis_pattern.findall(text)) * 1.5,
            RequestType.IMPLEMENTATION: len(self._implementation_pattern.findall(text)) * 1.0,
        }

        # Find highest score
        max_score = max(scores.values()) if scores else 0
        if max_score == 0:
            # Default to QUESTION if no indicators found
            if "?" in text:
                return RequestType.QUESTION
            return RequestType.ANALYSIS

        # Return type with highest score (prioritized order for ties)
        priority_order = [
            RequestType.DEBUGGING,
            RequestType.TESTING,
            RequestType.DOCUMENTATION,
            RequestType.REFACTORING,
            RequestType.LIST_GENERATION,
            RequestType.ANALYSIS,
            RequestType.IMPLEMENTATION,
        ]

        for req_type in priority_order:
            if scores.get(req_type, 0) == max_score:
                return req_type

        return RequestType.ANALYSIS

    def _determine_output_format(self, text: str, result: ClassificationResult) -> OutputFormat:
        """Determine expected output format."""
        # Check for explicit format requests
        if re.search(r"\bjson\b", text, re.IGNORECASE):
            return OutputFormat.JSON
        if re.search(r"\btable\b", text, re.IGNORECASE):
            return OutputFormat.TABLE
        if re.search(r"\bdiagram\b", text, re.IGNORECASE):
            return OutputFormat.DIAGRAM

        # List generation -> numbered or bullet list
        if result.request_type == RequestType.LIST_GENERATION:
            if result.quantity.quantity and result.quantity.quantity > 0:
                return OutputFormat.NUMBERED_LIST
            return OutputFormat.MARKDOWN_LIST

        # Implementation/debugging/testing -> code
        if result.request_type in (
            RequestType.IMPLEMENTATION,
            RequestType.DEBUGGING,
            RequestType.TESTING,
            RequestType.REFACTORING,
        ):
            if re.search(r"\bonly\s+code\b|\bjust\s+code\b|\bcode\s+only\b", text):
                return OutputFormat.CODE_ONLY
            return OutputFormat.CODE_WITH_EXPLANATION

        # Analysis or questions -> plain text
        return OutputFormat.PLAIN_TEXT

    def _select_pipeline(self, result: ClassificationResult) -> Pipeline:
        """Select appropriate processing pipeline."""
        # Read-only -> analysis pipeline
        if result.read_only:
            return Pipeline.ANALYSIS_ONLY

        # List generation
        if result.request_type == RequestType.LIST_GENERATION:
            return Pipeline.LIST_GENERATION

        # Research/questions
        if result.request_type in (RequestType.RESEARCH, RequestType.QUESTION):
            return Pipeline.RESEARCH

        # Analysis
        if result.request_type == RequestType.ANALYSIS:
            return Pipeline.ANALYSIS_ONLY

        # Multi-step complex tasks
        if result.complexity in (Complexity.COMPLEX, Complexity.EXPERT):
            return Pipeline.MULTI_STEP

        # Implementation with multiple file patterns
        if len(result.file_patterns) > 1:
            return Pipeline.MULTI_FILE_EDIT

        # Single file edit
        if result.request_type in (RequestType.DEBUGGING, RequestType.REFACTORING):
            return Pipeline.SINGLE_FILE_EDIT

        # Full implementation
        if result.request_type == RequestType.IMPLEMENTATION:
            return Pipeline.FULL_IMPLEMENTATION

        return Pipeline.CONVERSATION

    def _estimate_complexity(self, text: str, result: ClassificationResult) -> Complexity:
        """Estimate task complexity."""
        score = 0

        # Quantity increases complexity significantly
        if result.quantity.quantity:
            if result.quantity.quantity >= 100:
                score += 6
            elif result.quantity.quantity >= 50:
                score += 4
            elif result.quantity.quantity >= 20:
                score += 3
            elif result.quantity.quantity >= 10:
                score += 2
            elif result.quantity.quantity >= 5:
                score += 1

        # Multiple files
        score += len(result.file_patterns) * 2

        # Multiple languages/frameworks
        languages = self._detect_languages(text.lower())
        score += (len(languages) - 1) * 2 if languages else 0

        # Complexity indicators in text (each word adds more)
        complexity_words = [
            "complex",
            "comprehensive",
            "complete",
            "full",
            "entire",
            "all",
            "every",
            "architecture",
            "system",
            "framework",
            "redesign",
            "overhaul",
            "rewrite",
            "major",
            "significant",
        ]
        score += sum(2 for w in complexity_words if w in text.lower())

        # Map to complexity level with adjusted thresholds
        if score <= 1:
            return Complexity.TRIVIAL
        elif score <= 2:
            return Complexity.SIMPLE
        elif score <= 5:
            return Complexity.MODERATE
        elif score <= 8:
            return Complexity.COMPLEX
        else:
            return Complexity.EXPERT

    def _detect_languages(self, text: str) -> list[str]:
        """Detect programming languages mentioned."""
        detected = []
        for lang, patterns in self.LANGUAGES.items():
            for pattern in patterns:
                if pattern.lower() in text:
                    if lang not in detected:
                        detected.append(lang)
                    break
        return detected

    def _detect_frameworks(self, text: str) -> list[str]:
        """Detect frameworks mentioned."""
        detected = []
        for framework, patterns in self.FRAMEWORKS.items():
            for pattern in patterns:
                if pattern.lower() in text:
                    if framework not in detected:
                        detected.append(framework)
                    break
        return detected

    def _extract_instructions(self, text: str) -> list[str]:
        """Extract explicit instructions from the request."""
        instructions = []

        # Look for imperative sentences
        sentences = re.split(r"[.!]", text)
        for sentence in sentences:
            sentence = sentence.strip()
            # Check if starts with a verb (likely an instruction)
            if re.match(
                r"^(?:make sure|ensure|don\'t|do not|always|never|use|avoid)",
                sentence,
                re.IGNORECASE,
            ):
                instructions.append(sentence)

        return instructions

    def _calculate_confidence(self, result: ClassificationResult) -> float:
        """Calculate classification confidence score."""
        confidence = 0.5  # Base confidence

        # Boost for clear quantity
        if result.quantity.quantity and result.quantity.confidence > 0.8:
            confidence += 0.15

        # Boost for detected languages/frameworks
        if result.languages:
            confidence += 0.1

        # Boost for explicit instructions
        if result.explicit_instructions:
            confidence += 0.1

        # Boost for file patterns
        if result.file_patterns:
            confidence += 0.1

        return min(1.0, confidence)


# ═══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def classify_request(request: str) -> ClassificationResult:
    """Classify a request using the unified classifier."""
    classifier = UnifiedRequestClassifier()
    return classifier.classify(request)


def parse_quantity(text: str) -> QuantityResult:
    """Parse quantity from text using the unified parser."""
    parser = UnifiedQuantityParser()
    return parser.parse(text)


def is_read_only_request(request: str) -> bool:
    """Quick check if request is read-only."""
    classifier = UnifiedRequestClassifier()
    result = classifier.classify(request)
    return result.read_only


def get_required_quantity(request: str) -> int:
    """Get required quantity from request, or 0 if none."""
    parser = UnifiedQuantityParser()
    result = parser.parse(request)
    return result.minimum_required
