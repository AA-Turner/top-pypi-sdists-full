"""
Request classifier for SAGE - Comprehensive implementation of Roadmap Items 1-80.

This module provides:
- P0 Items 1-15: Request Classification (quantity detection, spelled numbers)
- P0 Items 16-25: Output Format Enforcement
- P0 Items 26-40: Multi-Step Pipeline Selection
- P0 Items 41-55: Code Generation Prevention
- P0 Items 56-70: Instruction Following
- P0 Items 71-80: Response Quality

All 80 P0 items are addressed in this module.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar

from sage.core.list_generator import extract_list_item_count

# =============================================================================
# ITEM 1-5: QUANTITY DETECTION - Spelled out numbers, various patterns
# =============================================================================

SPELLED_NUMBERS: dict[str, int] = {
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
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
    "thousand": 1000,
    "dozen": 12,
    "score": 20,
    "couple": 2,
    "few": 3,
    "several": 5,
    "many": 10,
}

# Compound number patterns like "twenty-five", "one hundred fifty"
COMPOUND_NUMBER_PATTERNS = [
    (
        r"\b(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)[- ]?(one|two|three|four|five|six|seven|eight|nine)\b",
        lambda m: SPELLED_NUMBERS.get(m.group(1), 0) + SPELLED_NUMBERS.get(m.group(2), 0),
    ),
    (
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten)\s+hundred\s*(?:and\s+)?(one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)?\b",
        lambda m: (
            SPELLED_NUMBERS.get(m.group(1), 1) * 100
            + (SPELLED_NUMBERS.get(m.group(2), 0) if m.group(2) else 0)
        ),
    ),
]


def extract_quantity_comprehensive(text: str) -> int | None:
    """
    Item 1-5: Comprehensive quantity extraction from text.

    Handles:
    - Numeric quantities: "100 items", "over 50"
    - Spelled out numbers: "hundred things", "fifty improvements"
    - Compound numbers: "twenty-five issues", "one hundred fifty"
    - Relative quantities: "at least X", "more than X", "over X"
    - Implicit quantities: "a few" -> 3, "several" -> 5, "many" -> 10
    - Approximate quantities: "about 100", "around fifty", "roughly 25"
    """
    text_lower = text.lower()

    # Pattern priority order (most specific first)
    patterns = [
        # "over/at least/more than X items"
        (r"\b(?:over|at\s+least|more\s+than|minimum\s+of?)\s+(\d+)\b", lambda m: int(m.group(1))),
        # "X+ items" or "X or more"
        (r"\b(\d+)\+\b", lambda m: int(m.group(1))),
        (r"\b(\d+)\s+or\s+more\b", lambda m: int(m.group(1))),
        # "about/around/roughly X items" (Item 14)
        (r"\b(?:about|around|roughly|approximately)\s+(\d+)\b", lambda m: int(m.group(1))),
        # Plain numeric: "100 items", "50 different things"
        (
            r"\b(\d+)\s+(?:different\s+)?(?:things?|items?|improvements?|issues?|problems?|suggestions?|recommendations?|changes?|fixes?|points?|results?)\b",
            lambda m: int(m.group(1)),
        ),
        # "list/identify/find X things"
        (r"\b(?:list|identify|find|give|provide|show)\s+(\d+)\b", lambda m: int(m.group(1))),
        # "first X results" or "top X" (Item 11)
        (r"\b(?:first|top)\s+(\d+)\b", lambda m: int(m.group(1))),
        # Just a number followed by list-like context
        (r"\b(\d+)\s+\w+\s+(?:that|which|to)\b", lambda m: int(m.group(1))),
    ]

    for pattern, extractor in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return extractor(match)

    # Check compound spelled numbers (Item 4)
    for pattern, extractor in COMPOUND_NUMBER_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return extractor(match)

    # Check for "about/around/roughly <spelled number>" (Item 14)
    approx_spelled = re.search(
        r"\b(?:about|around|roughly|approximately)\s+(zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|dozen)\b",
        text_lower,
    )
    if approx_spelled:
        return SPELLED_NUMBERS.get(approx_spelled.group(1))

    # Check single spelled numbers in various contexts (Item 3)
    noun_patterns = r"(?:things?|items?|improvements?|issues?|problems?|suggestions?|recommendations?|changes?|fixes?|points?|results?|ways?|examples?)"

    for word, value in sorted(SPELLED_NUMBERS.items(), key=lambda x: -x[1]):  # Check larger first
        if re.search(rf"\b{word}\b", text_lower):
            # Various quantity contexts
            contexts = [
                # "give me twenty suggestions"
                rf"\b(?:give|create|list|show|identify|find|provide)\s+(?:\w+\s+)*{word}\b",
                # "twenty suggestions please"
                rf"\b{word}\s+(?:different\s+)?{noun_patterns}\b",
                # "a couple suggestions" / "a few items"
                rf"\ba\s+{word}\s+{noun_patterns}\b",
                # "couple of items"
                rf"\b{word}\s+of\s+{noun_patterns}\b",
            ]

            for ctx_pattern in contexts:
                if re.search(ctx_pattern, text_lower):
                    return value

            # Always match these as quantities
            if word in ("hundred", "thousand", "dozen"):
                return value

    return None


# =============================================================================
# ITEM 6-15: REQUEST TYPE CLASSIFICATION
# =============================================================================


class RequestType(Enum):
    """Classification of user request types."""

    # Read-only analysis - NO code changes allowed
    ANALYSIS = auto()  # "analyze", "review", "audit", "assess"
    LIST_GENERATION = auto()  # "list X things", "identify 100 improvements"
    QUESTION = auto()  # "what is", "how does", "explain"
    SEARCH = auto()  # "find", "search", "locate"
    COMPARISON = auto()  # "compare", "difference between"
    SUMMARY = auto()  # "summarize", "overview", "tldr"

    # Implementation - code changes expected
    IMPLEMENTATION = auto()  # "fix", "implement", "add", "create"
    REFACTOR = auto()  # "refactor", "restructure", "reorganize"
    DEBUG = auto()  # "debug", "fix bug", "why is X failing"
    TEST_WRITING = auto()  # "write tests", "add test coverage"
    DOCUMENTATION = auto()  # "document", "add comments", "write docs"

    # Hybrid - may require both
    FIX_ALL = auto()  # "fix all X items" - needs list then implementation
    PLAN = auto()  # "plan how to" - analysis then potentially implementation


class OutputFormat(Enum):
    """Expected output format for each request type."""

    MARKDOWN_LIST = auto()  # Numbered/bulleted list
    MARKDOWN_TABLE = auto()  # Structured table
    CODE_FILES = auto()  # FILE: blocks with code
    EXPLANATION = auto()  # Prose explanation
    MIXED = auto()  # Combination based on context
    STEP_BY_STEP = auto()  # Numbered procedural steps
    COMPARISON_TABLE = auto()  # Side-by-side comparison
    TEXT = auto()  # Plain text response (alias for EXPLANATION)
    MARKDOWN = auto()  # Generic markdown formatting


class PipelineType(Enum):
    """
    Item 26-40: Pipeline type selection.

    Different request types require different processing pipelines.
    """

    ANALYSIS_ONLY = auto()  # Explore -> Analyze -> Format (NO code generation)
    LIST_GENERATION = auto()  # Explore -> Enumerate -> Validate -> Format
    IMPLEMENTATION = auto()  # Plan -> Test -> Implement -> Validate
    MULTI_STEP = auto()  # Complex tasks requiring multiple phases
    SIMPLE_RESPONSE = auto()  # Direct answer, no exploration needed


@dataclass
class ClassifiedRequest:
    """
    Result of request classification.

    Item 7: Classification confidence score
    Item 9: Intent verification fields
    """

    original_request: str
    request_type: RequestType
    expected_format: OutputFormat
    pipeline_type: PipelineType

    # Extracted requirements
    quantity_required: int | None = None
    priority_ranking: bool = False
    files_mentioned: list[str] = field(default_factory=list)

    # Item 7: Confidence scoring
    classification_confidence: float = 1.0  # 0.0 to 1.0
    alternative_types: list[RequestType] = field(default_factory=list)

    # Constraints
    read_only: bool = False
    strict_read_only: bool = False  # Item 5: Hard block on all code
    requires_file_verification: bool = True
    requires_search: bool = False
    requires_exploration: bool = False  # Item 161: Mandatory exploration
    is_informational: bool = False

    # Validation
    min_items: int = 0
    max_items: int | None = None
    must_include_file_paths: bool = False
    must_include_line_numbers: bool = False

    # Item 66: Instruction priority hierarchy
    instruction_priorities: list[str] = field(default_factory=list)

    # TDD-specific requirements
    requires_tdd: bool = False
    tdd_strict_mode: bool = False  # If True, reject any impl without tests

    def __post_init__(self):
        """Set constraints based on request type."""
        # Read-only types
        if self.request_type in (
            RequestType.ANALYSIS,
            RequestType.LIST_GENERATION,
            RequestType.QUESTION,
            RequestType.SEARCH,
            RequestType.COMPARISON,
            RequestType.SUMMARY,
        ):
            self.read_only = True
            self.requires_exploration = True

            # Item 5: Strict mode for analysis tasks
            if self.request_type in (RequestType.ANALYSIS, RequestType.LIST_GENERATION):
                self.strict_read_only = True

        # Informational determination
        self.is_informational = self.request_type in (
            RequestType.QUESTION,
            RequestType.SUMMARY,
        )

        # List generation specifics
        if self.request_type == RequestType.LIST_GENERATION:
            self.must_include_file_paths = True
            if self.quantity_required and self.quantity_required >= 50:
                self.must_include_line_numbers = True

        # Pipeline selection (Item 26-30)
        if self.request_type in (RequestType.ANALYSIS, RequestType.QUESTION, RequestType.SUMMARY):
            self.pipeline_type = PipelineType.ANALYSIS_ONLY
        elif self.request_type == RequestType.LIST_GENERATION:
            self.pipeline_type = PipelineType.LIST_GENERATION
        elif self.request_type in (
            RequestType.IMPLEMENTATION,
            RequestType.REFACTOR,
            RequestType.TEST_WRITING,
        ):
            self.pipeline_type = PipelineType.IMPLEMENTATION
            # Implementation requests require TDD
            self.requires_tdd = True
        elif self.request_type == RequestType.FIX_ALL:
            self.pipeline_type = PipelineType.MULTI_STEP
            # FIX_ALL also requires TDD
            self.requires_tdd = True
            self.tdd_strict_mode = True  # Strict because implementing many items

        # Check for explicit TDD keywords in original request
        if self.original_request:
            tdd_keywords = ["tdd", "test-driven", "test driven", "tests first", "write tests first"]
            if any(kw in self.original_request.lower() for kw in tdd_keywords):
                self.requires_tdd = True
                self.tdd_strict_mode = True

        # Item 66: Set instruction priorities
        self._set_instruction_priorities()

    @property
    def expected_output_format(self) -> OutputFormat:
        """Alias for expected_format for backwards compatibility."""
        return self.expected_format

    @property
    def classification_reasons(self) -> list[str]:
        """Return instruction priorities as classification reasons."""
        return self.instruction_priorities

    @property
    def is_complex(self) -> bool:
        """Check if this is a complex multi-step request."""
        return self.pipeline_type == PipelineType.MULTI_STEP

    @property
    def query_expansion(self) -> str | None:
        """Return query expansion if exploration is required."""
        if self.requires_exploration:
            return f"Explore codebase for: {self.original_request}"
        return None

    @property
    def context_needs(self) -> list[str]:
        """Return context requirements."""
        needs = []
        if self.requires_search:
            needs.append("search_results")
        if self.requires_exploration:
            needs.append("file_exploration")
        if self.must_include_file_paths:
            needs.append("file_references")
        return needs

    def _set_instruction_priorities(self):
        """Item 66: Define instruction priority hierarchy."""
        if self.request_type == RequestType.LIST_GENERATION:
            self.instruction_priorities = [
                "QUANTITY: Must produce required number of items",
                "GROUNDING: All items must reference real files",
                "FORMAT: Use numbered list or table format",
                "PRIORITY: Rank items if requested",
            ]
        elif self.request_type == RequestType.ANALYSIS:
            self.instruction_priorities = [
                "READ_ONLY: No code generation allowed",
                "EXPLORATION: Must search codebase before conclusions",
                "GROUNDING: Reference only verified files",
                "SPECIFICITY: Include file paths and line numbers",
            ]
        elif self.request_type == RequestType.IMPLEMENTATION:
            if self.requires_tdd:
                self.instruction_priorities = [
                    "TDD_MANDATORY: Write failing tests BEFORE any implementation code",
                    "RED_PHASE: Tests MUST fail initially (no implementation exists)",
                    "TESTS_FIRST: FILE: blocks for tests MUST come before implementation",
                    "GREEN_PHASE: Implementation must make tests pass",
                    "NO_PLACEHOLDERS: All code must be complete, no TODOs or pass statements",
                    "VERIFICATION: Run tests to confirm red/green phases",
                ]
            else:
                self.instruction_priorities = [
                    "VERIFICATION: Must read files before modifying",
                    "TESTS: Write tests before implementation",
                    "VALIDATION: Run tests after changes",
                    "COMPLETENESS: Complete the full task",
                ]
        elif self.request_type == RequestType.FIX_ALL:
            self.instruction_priorities = [
                "TDD_STRICT: Each fix MUST follow TDD (test first, then impl)",
                "SEQUENTIAL: Complete one fix at a time before moving to next",
                "VERIFICATION: Run tests after each fix to confirm success",
                "NO_PLACEHOLDERS: All code must be complete and functional",
                "COMPLETENESS: Do not stop until all items are fixed",
            ]


class RequestClassifier:
    """
    Classifies user requests to determine appropriate response type.

    Implements Items 1-15 from the roadmap.
    """

    # Item 3: More comprehensive patterns
    ANALYSIS_PATTERNS: ClassVar[list[str]] = [
        r"\b(analyze|analyse|review|audit|assess|evaluate|examine|inspect|check)\b",
        r"\b(what\s+needs|identify\s+issues|find\s+problems|check\s+for|look\s+for)\b",
        r"\b(recommendations?|suggestions?|improvements?)\b(?!.*\b(implement|fix|apply|do)\b)",
        r"\b(architecture|design|code)\s+(review|critique|analysis|assessment)\b",
        r"\b(quality|performance|security)\s+(review|assessment|check|audit)\b",
        r"\b(investigate|diagnose|troubleshoot)\b(?!.*\b(fix|implement)\b)",
        r"\bcreate\s+(?:a\s+)?(?:product\s+)?roadmap\b",
        r"\bwhat(?:'s|\s+is)\s+wrong\b",
    ]

    LIST_PATTERNS: ClassVar[list[str]] = [
        r"\b(list|enumerate|identify|find|give\s+me|provide|show)\s+(?:\w+\s+)*(?:things?|items?|issues?|improvements?|problems?|suggestions?|recommendations?|ways?|areas?)\b",
        r"\b(\d+)\s+(?:different\s+)?(?:things?|items?|improvements?|issues?|problems?)\b",
        r"\bover\s+(?:\d+|hundred|thousand)\b",
        r"\b(?:at\s+least|more\s+than|minimum)\s+(?:\d+|hundred|fifty)\b",
        r"\bhundred(?:\s+different)?\s+(?:things?|items?|improvements?)\b",
        r"\b(rank|prioritize|order)\s+(?:them\s+)?by\b",
        r"\btop\s+\d+\b",
        r"\bmake\s+(?:a\s+)?(?:comprehensive\s+)?list\b",
    ]

    IMPLEMENTATION_PATTERNS: ClassVar[list[str]] = [
        r"\b(fix|implement|add|create|build|write|develop|make|code)\b(?!.*\b(list|roadmap|plan)\b)",
        r"\b(refactor|restructure|reorganize|rewrite|redesign)\b",
        r"\b(update|modify|change|edit|patch|alter)\b",
        r"\b(apply|execute|do)\s+(?:the\s+)?(?:changes?|fixes?|improvements?)\b",
        r"\bcomplete(?:\s+all)?\s+(?:the\s+)?(?:\d+\s+)?(?:items?|tasks?)\b",
    ]

    QUESTION_PATTERNS: ClassVar[list[str]] = [
        r"^(?:what|how|why|when|where|which|who|can|does|is|are|should|would|could)\s+",
        r"\?$",
        r"\b(explain|describe|tell\s+me\s+about|clarify|elaborate)\b",
        r"\bwhat\s+(?:is|are|does)\b",
    ]

    FIX_ALL_PATTERNS: ClassVar[list[str]] = [
        r"\b(fix|implement|do|complete|execute)\s+(?:all|every|each)\s+(?:\d+\s+)?(?:items?|things?|issues?|points?)?\b",
        r"\bdo\s+it\s+all\b",
        r"\bfix\s+all\s+\d+\b",
        r"\bimplement\s+(?:all\s+)?(?:the\s+)?(?:\d+\s+)?(?:items?|changes?)\b",
        r"\bcomplete\s+(?:all\s+)?(?:the\s+)?(?:\d+\s+)?(?:tasks?|items?)\b",
    ]

    # MODE TRANSITION PATTERNS - Detect when user wants to switch from analysis to implementation
    # These patterns indicate the user has seen analysis results and now wants implementation
    MODE_TRANSITION_PATTERNS: ClassVar[list[str]] = [
        # "implement all of these"
        r"\bimplement\s+(?:all\s+)?(?:of\s+)?(?:these|them|this|the\s+list)\b",
        # "do the first X items"
        r"\bdo\s+(?:the\s+)?(?:first\s+)?\d+\s*(?:items?|things?|points?)?\b",
        # "implement items 1-5" or "do items 1 through 5"
        r"\b(?:implement|do|fix|complete)\s+(?:items?\s+)?\d+\s*(?:-|to|through)\s*\d+\b",
        # "go ahead and fix them"
        r"\bgo\s+ahead\s+(?:and\s+)?(?:fix|implement|do|complete)\b",
        # "start implementing"
        r"\bstart\s+(?:implementing|fixing|coding|working)\b",
        # "implement them using TDD"
        r"\bimplement\s+(?:them|these|all|it)\s+(?:using\s+)?(?:tdd|test.?driven)\b",
        # "fix these issues"
        r"\b(?:fix|implement|do)\s+these\s+(?:issues?|items?|things?|problems?)\b",
        # "let's implement" or "now implement"
        r"\b(?:let'?s?|now)\s+(?:implement|fix|do|complete|start)\b",
        # "proceed with implementation"
        r"\bproceed\s+(?:with\s+)?(?:implementation|fixing|coding)\b",
        # "yes, implement" or "yes implement them"
        r"\byes[,.]?\s*(?:implement|fix|do|complete|go\s+ahead)\b",
        # "implement it" or "do it"
        r"\b(?:implement|fix|complete)\s+it\b",
        # "make those changes"
        r"\bmake\s+(?:those|these|the)\s+(?:changes?|fixes?|improvements?)\b",
        # "apply the fixes"
        r"\bapply\s+(?:the\s+)?(?:fixes?|changes?|improvements?)\b",
    ]

    # Item 14: Negative patterns (things that should NOT trigger certain types)
    NOT_ANALYSIS_PATTERNS: ClassVar[list[str]] = [
        r"\b(?:then\s+)?(?:fix|implement|do|apply|execute)\s+(?:them|it|all|each)\b",
        r"\bstart\s+(?:fixing|implementing|coding)\b",
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for efficiency."""
        self._analysis_re = [re.compile(p, re.IGNORECASE) for p in self.ANALYSIS_PATTERNS]
        self._list_re = [re.compile(p, re.IGNORECASE) for p in self.LIST_PATTERNS]
        self._impl_re = [re.compile(p, re.IGNORECASE) for p in self.IMPLEMENTATION_PATTERNS]
        self._question_re = [re.compile(p, re.IGNORECASE) for p in self.QUESTION_PATTERNS]
        self._fix_all_re = [re.compile(p, re.IGNORECASE) for p in self.FIX_ALL_PATTERNS]
        self._not_analysis_re = [re.compile(p, re.IGNORECASE) for p in self.NOT_ANALYSIS_PATTERNS]
        self._mode_transition_re = [
            re.compile(p, re.IGNORECASE) for p in self.MODE_TRANSITION_PATTERNS
        ]

    def classify(self, request: str) -> ClassifiedRequest:
        """
        Classify a user request and determine response constraints.

        Items 6-15: Comprehensive classification with confidence scoring.
        """
        request_lower = request.lower()

        # Item 1-5: Enhanced quantity extraction
        quantity = extract_quantity_comprehensive(request)
        priority_ranking = bool(re.search(r"\b(rank|priorit|order)\w*\s+by\b", request_lower))

        # Item 7: Calculate confidence and alternatives
        scores = self._calculate_type_scores(request)
        sorted_scores = sorted(scores.items(), key=lambda x: -x[1])

        primary_type = sorted_scores[0][0] if sorted_scores else RequestType.ANALYSIS
        confidence = sorted_scores[0][1] if sorted_scores else 0.5
        alternatives = [t for t, s in sorted_scores[1:3] if s > 0.3]

        # CRITICAL: Check for MODE TRANSITION patterns FIRST
        # These indicate user wants to switch from analysis to implementation
        # This takes highest priority - if user says "implement all of these", they mean it!
        if any(p.search(request) for p in self._mode_transition_re):
            return ClassifiedRequest(
                original_request=request,
                request_type=RequestType.FIX_ALL,
                expected_format=OutputFormat.CODE_FILES,
                pipeline_type=PipelineType.MULTI_STEP,
                quantity_required=quantity,
                priority_ranking=priority_ranking,
                classification_confidence=0.95,  # High confidence - explicit mode switch
                alternative_types=[],
                read_only=False,  # CRITICAL: NOT read-only - user wants implementation
                requires_tdd=True,  # Implementation should use TDD
                tdd_strict_mode=True,
            )

        # Item 8: Reclassification check - if asking for implementation AFTER analysis
        if any(p.search(request) for p in self._not_analysis_re):
            if primary_type in (RequestType.ANALYSIS, RequestType.LIST_GENERATION):
                primary_type = RequestType.FIX_ALL
                confidence *= 0.8  # Lower confidence due to ambiguity

        # Check for "fix all" pattern first (hybrid request)
        if any(p.search(request) for p in self._fix_all_re):
            return ClassifiedRequest(
                original_request=request,
                request_type=RequestType.FIX_ALL,
                expected_format=OutputFormat.MIXED,
                pipeline_type=PipelineType.MULTI_STEP,
                quantity_required=quantity,
                priority_ranking=priority_ranking,
                classification_confidence=confidence,
                alternative_types=alternatives,
                read_only=False,
                requires_search=True,
            )

        # Check for list generation requests
        if any(p.search(request) for p in self._list_re):
            # Don't classify as list if also asking for implementation
            if not any(p.search(request) for p in self._not_analysis_re):
                return ClassifiedRequest(
                    original_request=request,
                    request_type=RequestType.LIST_GENERATION,
                    expected_format=OutputFormat.MARKDOWN_TABLE
                    if quantity and quantity > 20
                    else OutputFormat.MARKDOWN_LIST,
                    pipeline_type=PipelineType.LIST_GENERATION,
                    quantity_required=quantity or 10,
                    priority_ranking=priority_ranking,
                    classification_confidence=confidence,
                    alternative_types=alternatives,
                    min_items=quantity or 10,
                    must_include_file_paths=True,
                    read_only=True,  # List generation is read-only - no FILE: blocks allowed
                    requires_file_verification=True,  # Must gather evidence via READ:/SEARCH:
                )

        # Check for analysis requests
        if any(p.search(request) for p in self._analysis_re):
            if any(p.search(request) for p in self._impl_re) and any(
                p.search(request) for p in self._not_analysis_re
            ):
                return ClassifiedRequest(
                    original_request=request,
                    request_type=RequestType.IMPLEMENTATION,
                    expected_format=OutputFormat.CODE_FILES,
                    pipeline_type=PipelineType.IMPLEMENTATION,
                    classification_confidence=confidence,
                    alternative_types=alternatives,
                    read_only=False,
                )
            return ClassifiedRequest(
                original_request=request,
                request_type=RequestType.ANALYSIS,
                expected_format=OutputFormat.MARKDOWN_LIST,
                pipeline_type=PipelineType.ANALYSIS_ONLY,
                priority_ranking=priority_ranking,
                classification_confidence=confidence,
                alternative_types=alternatives,
                quantity_required=quantity,
                min_items=quantity or 0,
                read_only=True,  # Analysis is read-only - no FILE: blocks allowed
                requires_file_verification=True,  # Must gather evidence
            )

        # Check for questions
        if any(p.search(request) for p in self._question_re):
            return ClassifiedRequest(
                original_request=request,
                request_type=RequestType.QUESTION,
                expected_format=OutputFormat.EXPLANATION,
                pipeline_type=PipelineType.SIMPLE_RESPONSE,
                classification_confidence=confidence,
                alternative_types=alternatives,
            )

        # Check for implementation requests
        if any(p.search(request) for p in self._impl_re):
            return ClassifiedRequest(
                original_request=request,
                request_type=RequestType.IMPLEMENTATION,
                expected_format=OutputFormat.CODE_FILES,
                pipeline_type=PipelineType.IMPLEMENTATION,
                classification_confidence=confidence,
                alternative_types=alternatives,
                read_only=False,
            )

        # Default to analysis (safer - won't accidentally modify files)
        return ClassifiedRequest(
            original_request=request,
            request_type=RequestType.ANALYSIS,
            expected_format=OutputFormat.EXPLANATION,
            pipeline_type=PipelineType.ANALYSIS_ONLY,
            classification_confidence=0.5,  # Low confidence for default
            alternative_types=[RequestType.QUESTION],
            read_only=True,  # Default to read-only for safety
        )

    def _calculate_type_scores(self, request: str) -> dict[RequestType, float]:
        """Item 7: Calculate confidence scores for each request type."""
        scores: dict[RequestType, float] = {}

        # Count pattern matches for each type
        analysis_matches = sum(1 for p in self._analysis_re if p.search(request))
        list_matches = sum(1 for p in self._list_re if p.search(request))
        impl_matches = sum(1 for p in self._impl_re if p.search(request))
        question_matches = sum(1 for p in self._question_re if p.search(request))
        fix_all_matches = sum(1 for p in self._fix_all_re if p.search(request))

        # Normalize scores
        total = (
            analysis_matches + list_matches + impl_matches + question_matches + fix_all_matches + 1
        )

        scores[RequestType.ANALYSIS] = analysis_matches / total
        scores[RequestType.LIST_GENERATION] = list_matches / total
        scores[RequestType.IMPLEMENTATION] = impl_matches / total
        scores[RequestType.QUESTION] = question_matches / total
        scores[RequestType.FIX_ALL] = fix_all_matches / total

        # Boost list_generation if quantity is mentioned
        if extract_quantity_comprehensive(request):
            scores[RequestType.LIST_GENERATION] += 0.3

        return scores


# =============================================================================
# ITEMS 16-25: OUTPUT FORMAT ENFORCEMENT
# =============================================================================


@dataclass
class FormatRequirement:
    """Item 16-25: Output format requirements."""

    format_type: OutputFormat
    min_items: int = 0
    max_items: int | None = None
    requires_numbering: bool = False
    requires_table: bool = False
    requires_priority: bool = False
    requires_file_refs: bool = False
    requires_line_numbers: bool = False
    requires_code_blocks: bool = False
    forbidden_patterns: list[str] = field(default_factory=list)


class OutputFormatEnforcer:
    """
    Items 16-25: Enforces output format requirements.
    """

    @staticmethod
    def get_requirements(classification: ClassifiedRequest) -> FormatRequirement:
        """Get format requirements for a classification."""
        req = FormatRequirement(format_type=classification.expected_format)

        if classification.request_type == RequestType.LIST_GENERATION:
            req.min_items = classification.min_items or 10
            req.requires_numbering = True
            req.requires_file_refs = True
            if classification.quantity_required and classification.quantity_required > 20:
                req.requires_table = True
            if classification.priority_ranking:
                req.requires_priority = True
            # Item 44: Forbidden patterns for list generation (no code)
            req.forbidden_patterns = [
                r"^FILE:\s*",
                r"```(?:python|javascript|typescript|java|go|rust)",
            ]

        elif classification.request_type == RequestType.ANALYSIS:
            req.requires_file_refs = True
            req.requires_line_numbers = True
            req.forbidden_patterns = [
                r"^FILE:\s*",
                r"```(?:python|javascript|typescript|java|go|rust)",
            ]

        elif classification.request_type == RequestType.IMPLEMENTATION:
            req.requires_code_blocks = True

        return req

    @staticmethod
    def validate_format(response: str, requirements: FormatRequirement) -> tuple[bool, list[str]]:
        """Item 17: Validate response against format requirements."""
        errors = []

        # Check forbidden patterns (Item 44)
        for pattern in requirements.forbidden_patterns:
            if re.search(pattern, response, re.MULTILINE):
                errors.append(f"Response contains forbidden pattern: {pattern}")

        # Check numbering
        if requirements.requires_numbering:
            numbered_items = len(re.findall(r"^\s*\d+[\.\)]\s+", response, re.MULTILINE))
            if numbered_items < requirements.min_items:
                errors.append(
                    f"Response has {numbered_items} numbered items but requires {requirements.min_items}"
                )

        # Check table format
        if requirements.requires_table:
            table_rows = len(re.findall(r"^\|.*\|$", response, re.MULTILINE))
            if table_rows < 3:  # Header + separator + at least 1 row
                errors.append("Response requires table format but lacks proper markdown table")

        # Check priority indicators
        if requirements.requires_priority:
            has_priority = bool(
                re.search(
                    r"\b(P[0-4]|CRITICAL|HIGH|MEDIUM|LOW|Priority)\b", response, re.IGNORECASE
                )
            )
            if not has_priority:
                errors.append("Response requires priority ranking but lacks priority indicators")

        # Check file references
        if requirements.requires_file_refs:
            file_refs = re.findall(r"`[^`]+\.(?:py|js|ts|json|yaml|toml|md)`", response)
            if len(file_refs) < max(3, requirements.min_items // 10):
                errors.append(
                    f"Response has only {len(file_refs)} file references but should have more"
                )

        # Check code blocks
        if requirements.requires_code_blocks:
            code_blocks = len(re.findall(r"```", response)) // 2
            if code_blocks == 0:
                errors.append("Response requires code blocks but has none")

        return len(errors) == 0, errors


# =============================================================================
# ITEMS 41-55: CODE GENERATION PREVENTION
# =============================================================================


class CodeGenerationBlocker:
    """
    Items 41-55: Prevents code generation for read-only requests.
    """

    # Item 43: Patterns that indicate code generation
    CODE_PATTERNS: ClassVar[list[str]] = [
        r"^FILE:\s*\S+",
        r"```(?:python|javascript|typescript|java|go|rust|cpp|c\+\+|csharp|ruby|php|swift|kotlin)",
        r"def\s+\w+\s*\(",
        r"class\s+\w+\s*[:\(]",
        r"function\s+\w+\s*\(",
        r"const\s+\w+\s*=",
        r"import\s+\w+\s+from",
        r"from\s+\w+\s+import",
    ]

    # Item 53: Allowlist - code that's OK even in analysis (examples)
    ALLOWED_CODE_PATTERNS: ClassVar[list[str]] = [
        r"```(?:bash|shell|console|text|output|log)",  # Command examples OK
        r"# Example:?\s*$",  # Inline examples OK
        r"```\s*#\s*example",  # Explicitly marked examples
    ]

    @classmethod
    def check_for_code(cls, response: str) -> tuple[bool, list[str]]:
        """
        Item 43: Detect code in response.

        Returns (has_forbidden_code, list of violations)
        """
        violations = []

        for pattern in cls.CODE_PATTERNS:
            matches = re.findall(pattern, response, re.MULTILINE | re.IGNORECASE)
            if matches:
                # Check if it's in the allowlist
                is_allowed = any(
                    re.search(allowed, response, re.MULTILINE | re.IGNORECASE)
                    for allowed in cls.ALLOWED_CODE_PATTERNS
                )
                if not is_allowed:
                    violations.append(f"Found forbidden code pattern: {pattern[:30]}...")

        return len(violations) > 0, violations

    @classmethod
    def strip_code_blocks(cls, response: str) -> str:
        """Item 44: Remove code blocks from response (for read-only requests)."""
        # Remove FILE: blocks with their code blocks (handles indented and non-indented)
        response = re.sub(
            r"^\s*FILE:\s*\S+\s*\n\s*```[\s\S]*?```",
            "[File block removed - read-only analysis]",
            response,
            flags=re.MULTILINE,
        )

        # Also remove standalone FILE: references without immediate code blocks
        response = re.sub(r"^\s*FILE:\s*\S+\s*$", "", response, flags=re.MULTILINE)

        # Remove language-specific code blocks (keep bash/text examples)
        response = re.sub(
            r"```(?:python|javascript|typescript|java|go|rust|cpp|csharp|ruby|php|swift|kotlin)[\s\S]*?```",
            "[Code block removed - read-only analysis]",
            response,
            flags=re.IGNORECASE,
        )

        return response

    @classmethod
    def get_blocking_prompt(cls, classification: ClassifiedRequest) -> str:
        """Item 41-42: Generate prompt text that blocks code generation."""
        if not classification.strict_read_only:
            return ""

        return """

## ⛔ CRITICAL: CODE GENERATION BLOCKED ⛔

This request is classified as READ-ONLY ANALYSIS. You are FORBIDDEN from:
- Writing FILE: blocks
- Generating implementation code
- Creating new files
- Modifying existing files
- Writing code that could be executed

ANY CODE YOU GENERATE WILL BE AUTOMATICALLY STRIPPED FROM YOUR RESPONSE.

Your response MUST contain ONLY:
- Analysis text
- File path references (in backticks)
- Line number citations
- Numbered list items
- Priority rankings

DO NOT WRITE CODE. DO NOT USE FILE: BLOCKS. ANALYSIS ONLY.

"""


# =============================================================================
# ITEMS 56-70: INSTRUCTION FOLLOWING
# =============================================================================


class InstructionManager:
    """
    Items 56-70: Manages instruction following for the model.
    """

    @staticmethod
    def build_instruction_block(
        classification: ClassifiedRequest, repeat_interval: int = 500
    ) -> str:
        """
        Item 56-57: Build instruction block with repetition markers.

        Args:
            classification: The request classification
            repeat_interval: Character interval for instruction repetition
        """
        instructions = []

        # Item 57: Task restatement
        instructions.append(f"## YOUR TASK\n{classification.original_request}\n")

        # Item 66: Instruction priority hierarchy
        if classification.instruction_priorities:
            instructions.append("## INSTRUCTION PRIORITIES (IN ORDER OF IMPORTANCE)")
            for i, priority in enumerate(classification.instruction_priorities, 1):
                instructions.append(f"{i}. {priority}")
            instructions.append("")

        # Item 69: Explicit negative instructions
        if classification.read_only:
            instructions.append("## DO NOT")
            instructions.append("- Generate FILE: blocks")
            instructions.append("- Write implementation code")
            instructions.append("- Create or modify files")
            instructions.append("- Start implementing without explicit user request")
            instructions.append("")

        # Quantity requirement
        if classification.quantity_required:
            instructions.append("## QUANTITY REQUIREMENT")
            instructions.append(
                f"You MUST produce at least {classification.quantity_required} items."
            )
            instructions.append("Number each item clearly: 1., 2., 3., etc.")
            instructions.append("")

        return "\n".join(instructions)

    @staticmethod
    def get_mid_response_reminder(classification: ClassifiedRequest) -> str:
        """Item 60: Mid-response reminder to prevent drift."""
        reminders = []

        if classification.read_only:
            reminders.append("REMINDER: This is READ-ONLY analysis. No code generation.")

        if classification.quantity_required:
            reminders.append(f"REMINDER: You need {classification.quantity_required}+ items total.")

        if classification.must_include_file_paths:
            reminders.append("REMINDER: Reference real file paths for each item.")

        return " | ".join(reminders) if reminders else ""

    @staticmethod
    def check_instruction_compliance(
        response: str, classification: ClassifiedRequest
    ) -> tuple[bool, list[str]]:
        """Item 63-64: Check if response complies with instructions."""
        violations = []

        # Check read-only compliance
        if classification.read_only:
            has_code, code_violations = CodeGenerationBlocker.check_for_code(response)
            if has_code:
                violations.extend(code_violations)

        # Check quantity compliance using unified extraction
        if classification.quantity_required:
            item_count = extract_list_item_count(response)
            if item_count < classification.quantity_required:
                violations.append(
                    f"Only {item_count} items found but {classification.quantity_required} required"
                )

        # Check file reference compliance
        if classification.must_include_file_paths:
            file_refs = re.findall(r"`[^`]+\.\w+`", response)
            if len(file_refs) < 5:
                violations.append(f"Only {len(file_refs)} file references found")

        return len(violations) == 0, violations


# =============================================================================
# ITEMS 71-80: RESPONSE QUALITY
# =============================================================================


@dataclass
class ResponseQualityMetrics:
    """Item 71-80: Response quality metrics."""

    relevance_score: float = 0.0  # Item 71
    specificity_score: float = 0.0  # Item 75
    actionability_score: float = 0.0  # Item 76
    grounding_score: float = 0.0  # Item 80
    completeness_score: float = 0.0  # Item 73

    topic_drift: bool = False  # Item 72
    redundancy_count: int = 0  # Item 74

    file_references: list[str] = field(default_factory=list)
    unverified_claims: list[str] = field(default_factory=list)


class ResponseQualityValidator:
    """
    Items 71-80: Validates response quality.
    """

    @staticmethod
    def calculate_metrics(
        response: str, classification: ClassifiedRequest, verified_files: set[str]
    ) -> ResponseQualityMetrics:
        """Calculate quality metrics for a response."""
        metrics = ResponseQualityMetrics()

        # Item 71: Relevance score (based on keyword overlap)
        request_words = set(classification.original_request.lower().split())
        response_words = set(response.lower().split())
        overlap = len(request_words & response_words)
        metrics.relevance_score = min(1.0, overlap / max(len(request_words), 1))

        # Item 75: Specificity score (file refs + line numbers)
        file_refs = re.findall(r"`([^`]+\.\w+)`", response)
        line_refs = re.findall(r"line\s+\d+|:\d+", response, re.IGNORECASE)
        metrics.specificity_score = min(1.0, (len(file_refs) + len(line_refs)) / 20)
        metrics.file_references = file_refs

        # Item 76: Actionability score (action verbs + concrete suggestions)
        action_patterns = [
            r"\bshould\s+\w+",
            r"\bneed\s+to\s+\w+",
            r"\brecommend\s+\w+",
            r"\bfix\s+by\s+\w+",
            r"\bchange\s+\w+\s+to\b",
        ]
        action_count = sum(len(re.findall(p, response, re.IGNORECASE)) for p in action_patterns)
        metrics.actionability_score = min(1.0, action_count / 10)

        # Item 80: Grounding score (verified file references)
        verified_refs = [
            f
            for f in file_refs
            if f in verified_files or any(f.endswith(v) for v in verified_files)
        ]
        metrics.grounding_score = len(verified_refs) / max(len(file_refs), 1) if file_refs else 0.5

        # Item 73: Completeness score using unified extraction
        if classification.quantity_required:
            item_count = extract_list_item_count(response)
            metrics.completeness_score = min(1.0, item_count / classification.quantity_required)
        else:
            metrics.completeness_score = 0.8  # Default for non-list requests

        # Item 72: Topic drift detection
        # Check if later parts of response diverge from request
        response_parts = response.split("\n\n")
        if len(response_parts) > 3:
            later_text = " ".join(response_parts[-2:]).lower()
            early_text = " ".join(response_parts[:2]).lower()
            later_overlap = len(request_words & set(later_text.split()))
            early_overlap = len(request_words & set(early_text.split()))
            metrics.topic_drift = later_overlap < early_overlap * 0.5

        # Item 74: Redundancy detection
        sentences = re.split(r"[.!?]\s+", response)
        seen_patterns = set()
        for sentence in sentences:
            # Normalize sentence
            normalized = re.sub(r"\d+", "N", sentence.lower()[:50])
            if normalized in seen_patterns:
                metrics.redundancy_count += 1
            seen_patterns.add(normalized)

        return metrics

    @staticmethod
    def get_quality_issues(metrics: ResponseQualityMetrics) -> list[str]:
        """Get list of quality issues from metrics."""
        issues = []

        if metrics.relevance_score < 0.3:
            issues.append("Low relevance to original request")

        if metrics.specificity_score < 0.2:
            issues.append("Lacks specific file references and line numbers")

        if metrics.actionability_score < 0.2:
            issues.append("Suggestions are not actionable")

        if metrics.grounding_score < 0.5:
            issues.append("Many file references are unverified")

        if metrics.completeness_score < 0.5:
            issues.append("Response is incomplete (missing required items)")

        if metrics.topic_drift:
            issues.append("Response drifts from original topic")

        if metrics.redundancy_count > 3:
            issues.append(f"Response has {metrics.redundancy_count} redundant items")

        return issues


# =============================================================================
# COMBINED RESPONSE VALIDATION (Items 16-80)
# =============================================================================


@dataclass
class ResponseValidation:
    """Complete validation result for a response."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    # Metrics
    item_count: int = 0
    file_references: int = 0
    code_blocks: int = 0

    # Quality metrics
    quality_metrics: ResponseQualityMetrics | None = None

    # Retry recommendation
    should_retry: bool = False
    retry_prompt: str | None = None


class ResponseValidator:
    """
    Comprehensive response validator implementing Items 16-80.
    """

    def validate(
        self, response: str, classification: ClassifiedRequest, verified_files: set[str]
    ) -> ResponseValidation:
        """
        Validate response against all requirements.
        """
        errors = []
        warnings = []

        # Item 17: Format validation
        format_req = OutputFormatEnforcer.get_requirements(classification)
        format_valid, format_errors = OutputFormatEnforcer.validate_format(response, format_req)
        errors.extend(format_errors)

        # Items 41-55: Code generation check
        if classification.read_only:
            has_code, code_violations = CodeGenerationBlocker.check_for_code(response)
            if has_code:
                errors.extend(code_violations)

        # Items 56-70: Instruction compliance
        compliant, compliance_violations = InstructionManager.check_instruction_compliance(
            response, classification
        )
        if not compliant:
            errors.extend(compliance_violations)

        # Items 71-80: Quality validation
        quality_metrics = ResponseQualityValidator.calculate_metrics(
            response, classification, verified_files
        )
        quality_issues = ResponseQualityValidator.get_quality_issues(quality_metrics)
        warnings.extend(quality_issues)

        # Count items
        item_count = len(re.findall(r"^\s*\d+[\.\)]\s+", response, re.MULTILINE))
        file_refs = len(re.findall(r"`[^`]+\.\w+`", response))
        code_blocks = len(re.findall(r"```", response)) // 2

        # Determine if retry is needed
        should_retry = False
        retry_prompt = None

        if errors:
            should_retry = True
            retry_prompt = self._build_retry_prompt(errors, classification)
        elif quality_metrics.completeness_score < 0.5:
            should_retry = True
            retry_prompt = self._build_continuation_prompt(classification, item_count)

        return ResponseValidation(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            item_count=item_count,
            file_references=file_refs,
            code_blocks=code_blocks,
            quality_metrics=quality_metrics,
            should_retry=should_retry,
            retry_prompt=retry_prompt,
        )

    def _build_retry_prompt(self, errors: list[str], classification: ClassifiedRequest) -> str:
        """Build a retry prompt based on validation errors."""
        prompt_parts = [
            "Your previous response had the following issues:\n",
            "\n".join(f"- {e}" for e in errors),
            "\n\nPlease regenerate your response fixing these issues.",
        ]

        if classification.read_only:
            prompt_parts.append("\nREMINDER: This is a READ-ONLY request. NO code generation.")

        if classification.quantity_required:
            prompt_parts.append(
                f"\nREMINDER: You must provide at least {classification.quantity_required} items."
            )

        return "".join(prompt_parts)

    def _build_continuation_prompt(
        self, classification: ClassifiedRequest, current_count: int
    ) -> str:
        """Build a continuation prompt for incomplete responses."""
        remaining = (classification.quantity_required or 10) - current_count
        return f"""
Your response is incomplete. You have provided {current_count} items but need {classification.quantity_required or 10}.

Continue your list from item {current_count + 1}. You need at least {remaining} more items.

CONTINUE THE LIST (no need to repeat previous items):
"""


# =============================================================================
# REQUEST EXPANDER (Enhanced)
# =============================================================================


class RequestExpander:
    """
    Enhanced request expander implementing Items 1-80.
    """

    def expand(self, request: str, classification: ClassifiedRequest) -> str:
        """
        Expand a user request with comprehensive instructions.
        """
        expanded_parts = [request]

        # Item 41-42: Add code blocking prompt if needed
        if classification.strict_read_only:
            expanded_parts.append(CodeGenerationBlocker.get_blocking_prompt(classification))

        # Item 56-57: Add instruction block
        expanded_parts.append(InstructionManager.build_instruction_block(classification))

        # Items 161: Mandatory exploration for analysis
        if classification.requires_exploration:
            expanded_parts.append("""
## MANDATORY EXPLORATION PHASE

Before providing your response, you MUST:
1. Use SEARCH: to discover the project structure
2. Use READ: on key files (README.md, pyproject.toml, main files)
3. Build an accurate understanding of what exists
4. Reference ONLY files you have verified exist

Start with SEARCH: and READ: commands NOW.
""")

        # Quantity requirement
        if classification.quantity_required:
            expanded_parts.append(f"""
## QUANTITY REQUIREMENT: {classification.quantity_required}+ ITEMS

You MUST provide at least {classification.quantity_required} distinct items.
Each item must be numbered: 1., 2., 3., ...
Each item must reference a specific file or code location.
DO NOT stop until you have {classification.quantity_required} items.
""")

        # Priority ranking
        if classification.priority_ranking:
            expanded_parts.append("""
## PRIORITY RANKING REQUIRED

Rank all items using priority labels:
- P0/CRITICAL: Security issues, blocking bugs
- P1/HIGH: Important improvements
- P2/MEDIUM: Nice to have
- P3/LOW: Minor optimizations

Include priority in EVERY item.
""")

        return "\n".join(expanded_parts)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def classify_request(request: str) -> ClassifiedRequest:
    """Classify a user request."""
    return RequestClassifier().classify(request)


def expand_request(request: str) -> str:
    """Classify and expand a user request."""
    classification = classify_request(request)
    return RequestExpander().expand(request, classification)


def validate_response(
    response: str, classification: ClassifiedRequest, verified_files: set[str] | None = None
) -> ResponseValidation:
    """Validate a response against its classification."""
    return ResponseValidator().validate(response, classification, verified_files or set())


def should_use_analysis_pipeline(classification: ClassifiedRequest) -> bool:
    """Item 26: Check if analysis-only pipeline should be used."""
    return classification.pipeline_type in (
        PipelineType.ANALYSIS_ONLY,
        PipelineType.LIST_GENERATION,
    )


def should_block_multi_step(classification: ClassifiedRequest) -> bool:
    """Item 26: Check if multi-step implementation pipeline should be blocked."""
    return classification.read_only and classification.strict_read_only


# =============================================================================
# P0 ITEMS 9-10: EVIDENCE TRACKING AND SYNTHESIS GATING
# =============================================================================


@dataclass
class EvidenceTracker:
    """
    P0 Item 9-10: Track verified evidence during analysis.

    This class tracks all file reads, searches, and their results to ensure
    that synthesis only happens when sufficient verified evidence exists.
    """

    verified_files: set[str] = field(default_factory=set)
    failed_files: set[str] = field(default_factory=set)
    failed_searches: set[str] = field(default_factory=set)
    search_results: list[tuple[str, list[str]]] = field(default_factory=list)
    search_count: int = 0
    empty_search_count: int = 0
    command_results: list[tuple[str, bool]] = field(default_factory=list)

    def record_file_read(self, filepath: str, success: bool = True) -> None:
        """Record a file read attempt."""
        if success:
            self.verified_files.add(filepath)
        else:
            self.failed_files.add(filepath)

    def record_search(self, pattern: str, results: list[str]) -> None:
        """Record a search and its results."""
        self.search_count += 1
        if results:
            self.search_results.append((pattern, results))
            for f in results:
                self.verified_files.add(f)
        else:
            self.empty_search_count += 1
            self.failed_searches.add(pattern)

    def record_command(self, command: str, success: bool) -> None:
        """Record a command execution result."""
        self.command_results.append((command, success))

    def has_verified_evidence(self) -> bool:
        """Check if any verified evidence exists."""
        return len(self.verified_files) > 0

    def has_successful_searches(self) -> bool:
        """Check if any searches returned results."""
        return len(self.search_results) > 0

    def all_reads_failed(self) -> bool:
        """Check if all file reads failed."""
        return len(self.failed_files) > 0 and len(self.verified_files) == 0

    def all_searches_empty(self) -> bool:
        """Check if all searches returned empty."""
        return self.search_count > 0 and self.empty_search_count == self.search_count

    def get_evidence_summary(self) -> dict:
        """Get a summary of collected evidence."""
        return {
            "verified_files": len(self.verified_files),
            "failed_files": len(self.failed_files),
            "successful_searches": len(self.search_results),
            "empty_searches": self.empty_search_count,
            "total_commands": len(self.command_results),
            "successful_commands": sum(1 for _, s in self.command_results if s),
        }


@dataclass
class SynthesisGate:
    """
    P0 Item 9-10: Gate that blocks synthesis without sufficient evidence.

    This ensures that analysis/list generation tasks don't proceed to
    synthesis if they have no verified evidence to base findings on.
    """

    min_files: int = 0  # Minimum verified files required
    min_searches: int = 0  # Minimum successful searches required
    require_any_evidence: bool = True  # Require at least some evidence

    def check(self, tracker: EvidenceTracker) -> tuple[bool, str]:
        """
        Check if synthesis should be allowed.

        Returns:
            Tuple of (can_synthesize, reason)
        """
        # Check for any evidence
        if self.require_any_evidence and not tracker.has_verified_evidence():
            if tracker.all_reads_failed():
                return False, "All file read attempts failed - no verified evidence available."
            if tracker.all_searches_empty():
                return (
                    False,
                    "All search attempts returned empty results - no verified evidence available.",
                )
            return False, "No verified evidence gathered - cannot synthesize findings."

        # Check minimum file requirement
        if self.min_files > 0 and len(tracker.verified_files) < self.min_files:
            return (
                False,
                f"Insufficient evidence: need {self.min_files} verified files, have {len(tracker.verified_files)}.",
            )

        # Check minimum search requirement
        if self.min_searches > 0 and len(tracker.search_results) < self.min_searches:
            return (
                False,
                f"Insufficient evidence: need {self.min_searches} successful searches, have {len(tracker.search_results)}.",
            )

        return True, "Sufficient evidence gathered for synthesis."

    def get_evidence_requirements(self) -> dict:
        """Get the evidence requirements for synthesis."""
        return {
            "min_files": self.min_files,
            "min_searches": self.min_searches,
            "require_any_evidence": self.require_any_evidence,
        }
