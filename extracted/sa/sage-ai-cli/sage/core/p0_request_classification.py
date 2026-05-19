"""
P0 Request Classification for SAGE - Items 21-50 from Roadmap P0.

This module provides the V2 request classification and pipeline selection logic.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar, Any

from sage.core.quantity_detection import QuantityParser, QuantityResult


class IntentType(Enum):
    """Fine-grained intent classification."""

    ANALYZE = auto()  # Pure analysis, no changes
    LIST = auto()  # Generate a list
    IMPLEMENT = auto()  # Make code changes
    FIX = auto()  # Fix bugs/issues
    TEST = auto()  # Write/run tests
    EXPLAIN = auto()  # Explain something
    PLAN = auto()  # Create a plan
    DEBUG = auto()  # Debug an issue
    REFACTOR = auto()  # Restructure code
    DOCUMENT = auto()  # Add documentation
    SEARCH = auto()  # Find/search something
    QUESTION = auto()  # Answer a question
    COMPARE = auto()  # Compare things
    REVIEW = auto()  # Code review
    DEPLOY = auto()  # Deployment tasks
    MIGRATE = auto()  # Migration tasks
    OPTIMIZE = auto()  # Performance optimization
    SECURE = auto()  # Security fixes
    CONFIGURE = auto()  # Configuration changes
    UNKNOWN = auto()  # Unknown intent


class ExecutionMode(Enum):
    """Execution mode determines what actions are allowed."""

    READ_ONLY = auto()  # Only reading, no modifications
    WRITE_ENABLED = auto()  # Can create/modify files
    FULL_ACCESS = auto()  # All operations including dangerous ones


@dataclass
class IntentSignal:
    """A signal indicating a particular intent."""

    pattern: str
    intent_type: IntentType
    weight: float = 1.0
    requires_context: bool = False
    negates: list[IntentType] = field(default_factory=list)


@dataclass
class HybridIntent:
    """
    P0 Item 1-10: Hybrid intent for requests that combine multiple intents.
    """

    primary_intents: list[IntentType]
    secondary_intents: list[IntentType]
    requires_analysis_first: bool = False
    requires_implementation: bool = False
    is_hybrid: bool = False
    execution_mode: ExecutionMode = ExecutionMode.READ_ONLY
    confidence: float = 0.0
    intent_chain: list[IntentType] = field(default_factory=list)
    analysis_confidence: float = 0.5
    implementation_confidence: float = 0.5
    phases: list[str] = field(default_factory=list)
    priority: str = "normal"
    scope: str = ""

    @property
    def allows_file_writes(self) -> bool:
        """Check if this intent allows file writes."""
        return self.execution_mode in (ExecutionMode.WRITE_ENABLED, ExecutionMode.FULL_ACCESS)

    @property
    def is_implementation_intent(self) -> bool:
        """Check if this is an implementation intent."""
        implementation_intents = {
            IntentType.IMPLEMENT,
            IntentType.FIX,
            IntentType.REFACTOR,
            IntentType.TEST,
            IntentType.DOCUMENT,
            IntentType.OPTIMIZE,
            IntentType.SECURE,
            IntentType.CONFIGURE,
        }
        return any(i in implementation_intents for i in self.primary_intents)

    @property
    def requires_analysis(self) -> bool:
        """Check if this intent requires analysis."""
        analysis_intents = {
            IntentType.ANALYZE,
            IntentType.LIST,
            IntentType.EXPLAIN,
            IntentType.SEARCH,
        }
        return (
            any(i in analysis_intents for i in self.primary_intents) or self.requires_analysis_first
        )

    def is_valid(self) -> bool:
        """Check if intent is valid."""
        return len(self.primary_intents) > 0 or self.is_hybrid


class RequestTypeV2(Enum):
    """Item 24: Enhanced request type enum with clear categorization."""

    # Read-only types - NO code generation allowed
    ANALYSIS = auto()  # "analyze", "review", "audit"
    LIST_GENERATION = auto()  # "list X things", "identify improvements"
    QUESTION = auto()  # "what is", "how does", "explain"
    SEARCH = auto()  # "find", "search for", "locate"
    COMPARISON = auto()  # "compare", "difference between"
    SUMMARY = auto()  # "summarize", "overview"
    EXPLANATION = auto()  # "explain", "describe"

    # Implementation types - code generation expected
    IMPLEMENTATION = auto()  # "implement", "add", "create"
    FIX = auto()  # "fix", "repair", "solve"
    REFACTOR = auto()  # "refactor", "improve", "optimize"
    TEST_WRITING = auto()  # "write tests", "add test coverage"
    DOCUMENTATION = auto()  # "document", "add comments"

    # Hybrid types - require special handling
    FIX_ALL = auto()  # "fix all X items"
    ANALYZE_THEN_FIX = auto()  # "analyze and then fix"
    PLAN_IMPLEMENTATION = auto()  # "plan how to implement"
    MULTI_STEP = auto()  # Multi-step pipeline tasks


class OutputFormatV2(Enum):
    """Enhanced output format with all variants."""

    PLAIN_TEXT = auto()
    MARKDOWN_LIST = auto()  # Numbered/bulleted list
    NUMBERED_LIST = auto()
    MARKDOWN_TABLE = auto()  # Structured table
    CODE_ONLY = auto()
    CODE_WITH_EXPLANATION = auto()
    CODE_FILES = auto()  # FILE: blocks with code
    EXPLANATION = auto()  # Prose explanation
    MIXED = auto()  # Combination
    STEP_BY_STEP = auto()  # Numbered steps
    COMPARISON_TABLE = auto()  # Side-by-side
    TEXT = auto()  # Plain text
    JSON = auto()  # JSON format
    HIERARCHICAL = auto()  # Nested categories


class PipelineTypeV2(Enum):
    """
    Items 36-50: Pipeline type with strict enforcement rules.
    """

    ANALYSIS_ONLY = auto()  # Explore -> Analyze -> Format (NO code)
    LIST_GENERATION = auto()  # Explore -> Enumerate -> Validate -> Format
    IMPLEMENTATION = auto()  # Plan -> Test -> Implement -> Validate
    MULTI_STEP = auto()  # Complex hybrid tasks
    SIMPLE_RESPONSE = auto()  # Direct answer

    @property
    def allows_code_generation(self) -> bool:
        """Item 43-45: Check if pipeline allows code generation."""
        return self in (PipelineTypeV2.IMPLEMENTATION, PipelineTypeV2.MULTI_STEP)

    @property
    def requires_exploration(self) -> bool:
        """Check if pipeline requires codebase exploration first."""
        return self in (
            PipelineTypeV2.ANALYSIS_ONLY,
            PipelineTypeV2.LIST_GENERATION,
            PipelineTypeV2.IMPLEMENTATION,
        )

    @property
    def forbidden_patterns(self) -> list[str]:
        """Item 42-45: Get forbidden output patterns for this pipeline."""
        if self == PipelineTypeV2.ANALYSIS_ONLY:
            return [
                r"^FILE:\s*\S+",
                r"```(?:python|javascript|typescript|java|go|rust|cpp|c\+\+|ruby|php|swift|kotlin)",
                r"^\s{4}(?:def|class|function|const|let|var|import|from)\s",
            ]
        elif self == PipelineTypeV2.LIST_GENERATION:
            return [
                r"^FILE:\s*\S+",
                r"```(?:python|javascript|typescript|java|go|rust)",
            ]
        return []


@dataclass
class ClassifiedRequestV2:
    """
    Items 21-35: Comprehensive request classification result.
    """

    original_request: str = ""
    request_type: RequestTypeV2 = RequestTypeV2.ANALYSIS
    output_format: OutputFormatV2 = OutputFormatV2.MARKDOWN_LIST
    pipeline_type: PipelineTypeV2 = PipelineTypeV2.ANALYSIS_ONLY

    # Quantity detection (Items 1-20)
    quantity_result: QuantityResult | None = None

    # Classification metadata (Item 32-34)
    confidence: float = 1.0
    alternative_types: list[RequestTypeV2] = field(default_factory=list)
    classification_reasons: list[str] = field(default_factory=list)

    # Constraints (Items 36-50)
    read_only: bool = True
    strict_read_only: bool = False
    requires_exploration: bool = True
    is_informational: bool = False

    # Extracted requirements (Items 91-105)
    explicit_instructions: list[str] = field(default_factory=list)
    must_include: list[str] = field(default_factory=list)
    must_exclude: list[str] = field(default_factory=list)
    files_mentioned: list[str] = field(default_factory=list)

    # Validation requirements (Items 106-120)
    min_items: int = 0
    max_items: int | None = None
    requires_file_refs: bool = False
    requires_line_numbers: bool = False
    requires_priority_ranking: bool = False
    requires_tdd: bool = False

    def __post_init__(self):
        """Set derived constraints based on classification."""
        # Cap huge list requests to reduce padded / spam output
        _max_qty = 60
        if self.quantity_result is not None and self.quantity_result.quantity is not None:
            self.quantity_result.quantity = min(self.quantity_result.quantity, _max_qty)

        # Read-only determination
        self.read_only = self.request_type in (
            RequestTypeV2.ANALYSIS,
            RequestTypeV2.LIST_GENERATION,
            RequestTypeV2.QUESTION,
            RequestTypeV2.SEARCH,
            RequestTypeV2.COMPARISON,
            RequestTypeV2.SUMMARY,
            RequestTypeV2.EXPLANATION,
        )

        # Informational determination
        self.is_informational = self.request_type in (
            RequestTypeV2.QUESTION,
            RequestTypeV2.SUMMARY,
            RequestTypeV2.EXPLANATION,
        )

        # Refined informational check: if it's a question but looks like it's about the codebase,
        # we don't treat it as purely informational (which triggers general knowledge/web search).
        if self.is_informational:
            codebase_keywords = [
                "code", "file", "function", "class", "method", "variable", "bug", "error",
                "fix", "implement", "refactor", "test", "app", "api", "endpoint", "database",
                "repo", "repository", "directory", "folder", "module", "package", "config",
                "setup", "build", "run", "execute", "logic", "flow", "structure", "auth",
                "architecture", "component", "service", "frontend", "backend", "client", "server"
            ]
            request_lower = self.original_request.lower()
            
            # Check for codebase keywords
            has_codebase_kw = any(kw in request_lower for kw in codebase_keywords)
            
            # Check for file path patterns (e.g., path/to/file.py)
            has_file_path = bool(re.search(r"\b[\w\-/]+\.(?:py|js|ts|tsx|jsx|html|css|json|md|txt|yaml|yml|sh|bash|sql|c|cpp|h|hpp|rs|go|java|kt|rb|php)\b", request_lower))
            
            # If it's about the codebase or mentions a file, it's NOT purely informational
            if has_codebase_kw or has_file_path:
                self.is_informational = False

        # Strict read-only (no code at all)
        self.strict_read_only = self.request_type in (
            RequestTypeV2.ANALYSIS,
            RequestTypeV2.LIST_GENERATION,
        )

        # Exploration requirement
        self.requires_exploration = self.pipeline_type.requires_exploration

        # TDD requirement
        self.requires_tdd = self.pipeline_type in (
            PipelineTypeV2.IMPLEMENTATION,
            PipelineTypeV2.MULTI_STEP,
        )

        # List generation specifics
        if self.request_type == RequestTypeV2.LIST_GENERATION:
            self.requires_file_refs = True
            if self.quantity_result and self.quantity_result.quantity:
                self.min_items = self.quantity_result.quantity
                if self.min_items >= 50:
                    self.requires_line_numbers = True

    @property
    def expected_output_format(self) -> OutputFormatV2:
        """Alias for backwards compatibility."""
        return self.output_format

    @property
    def quantity_required(self) -> int | None:
        """Get required quantity from result."""
        return self.quantity_result.quantity if self.quantity_result else None

    @property
    def requested_quantity(self) -> int | None:
        """Get requested quantity from result (alias)."""
        return self.quantity_result.quantity if self.quantity_result else None


class RequestClassifierV2:
    """
    Items 21-35: Enhanced request classifier with comprehensive pattern matching.
    """

    ANALYSIS_PATTERNS: ClassVar[list[str]] = [
        r"\b(analyze|analyse|review|audit|assess|evaluate|examine|inspect)\b",
        r"\b(what\s+needs|identify\s+issues|find\s+problems|check\s+for)\b",
        r"\b(recommendations?|suggestions?|improvements?)\b(?!.*\b(implement|fix|apply)\b)",
        r"\b(architecture|code|design)\s+(review|analysis|assessment)\b",
        r"\bcreate\s+(?:a\s+)?(?:comprehensive\s+)?(?:product\s+)?roadmap\b",
        r"\bwhat(?:'s|\s+is)\s+wrong\b",
    ]

    LIST_PATTERNS: ClassVar[list[str]] = [
        r"\b(list|enumerate)\s+(?:\w+\s+)*(?:things?|items?|issues?|improvements?)\b",
        r"\bidentify\s+(?:the\s+)?(?:\w+\s+)*things?\s+(?:that|to|which)\b",
        r"\bover\s+(?:\d+|hundred|thousand)\s+(?:things?|items?)\b",
        r"\b(?:at\s+least|more\s+than)\s+(?:\d+|hundred)\b",
        r"\bhundred\s+(?:different\s+)?(?:things?|items?|improvements?)\b",
        r"\bmake\s+(?:a\s+)?(?:comprehensive\s+)?list\b",
        r"\b(\d+)\+?\s+(?:things?|items?|improvements?)\b",
        r"\b(?:give|provide|show|find)\s+(?:me\s+)?(\d+)\s+(?:suggestions?|recommendations?|problems?|ideas?|options?|examples?)\b",
        r"\bidentify\s+(\d+)\s+(?:bugs?|issues?|errors?|problems?)\b",
        r"\bgenerate\s+(\d+)\s+(?:ideas?|suggestions?|options?|alternatives?)\b",
        r"\bfind\s+(\d+)\s+(?:areas?|places?|spots?)\s+to\s+(?:improve|fix|update)\b",
    ]

    IMPLEMENTATION_PATTERNS: ClassVar[list[str]] = [
        r"\b(implement|add|create|build|write|develop)\s+(?:a\s+|the\s+|new\s+)?(?:\w+\s+)*(?:feature|function|class|module|component|api|endpoint|service|test|model|handler|controller|view|schema)\b",
        r"\bcode\s+(?:a\s+|the\s+)?(?:solution|feature|fix)\b",
        r"\b(refactor|restructure|reorganize|rewrite)\s+\w+\b",
        r"\b(update|modify|change|edit|patch)\s+(?:the\s+)?(?:code|file|function|class)\b",
        r"\b(apply|execute|do)\s+(?:the\s+)?(?:changes?|fixes?)\b",
        r"\bapply\s+(?:the\s+)?(?:\w+)",
        r"\bfix\s+(?:the\s+)?(?:\w+\s+)?(?:bug|error|issue|problem)\b",
        r"\bfix\s+(?:this|that|it|the\s+code)\b",
        r"\bnow\s+implement\b",
        r"\b(?:write|create)\s+(?:the\s+)?(?:test|tests)\s+(?:for|files?)\b",
        r"\b(?:implement|do|execute)\s+item\s*\d+\b",
        r"\b(?:implement|do|execute)\s+(?:the\s+)?(?:first|second|third|\d+(?:st|nd|rd|th)?)\s+(?:item|step|improvement|fix)\b",
        r"^implement\b",
        r"\b(modify|change|alter)\s+(?:the\s+)?(?:existing\s+)?(?:\w+)",
        r"\b(repair|fix)\s+(?:the\s+)?(?:broken\s+)?(?:\w+)",
        r"\bexecute\s+(?:the\s+)?(?:\w+)",
        r"\b(update|upgrade)\s+(?:the\s+)?(?:configuration|config|settings?)\b",
        r"\bcreate\s+(?:a\s+)?(?:\w+\s+)?(?:page|form|dialog|modal|component|widget)\b",
        r"\bcreate\s+(?:a\s+)?(?:\w+\.(?:py|js|ts|go|rb|java|cs|cpp|c|rs|swift|kt|php|html|css|json|yaml|yml|sh|md))\b",
        r"\bwrite\s+(?:a\s+)?(?:\w+\.(?:py|js|ts|go|rb|java|cs|cpp|c|rs|swift|kt|php|html|css|json|yaml|yml|sh|md))\b",
        r"\b(?:create|make|generate|write)\s+(?:\w+\s+){0,5}(?:called|named)\s+\w+\.(?:py|js|ts|go|rb|java|cs|cpp|c|rs|swift|kt|php|html|css|sh)\b",
        r"\b(?:create|make|write|add)\b.*\b\w+\.(?:py|js|ts|go|rb|java|cs|cpp|c|html|css|sh)\b",
        r"\bchange\s+(?:the\s+)?(?:algorithm|logic|behavior|implementation)\b",
        r"\b(?:write|create)\s+(?:the\s+)?(?:solution|fix|implementation)\b",
        r"\badd\s+(?:the\s+)?(?:functionality|feature|capability|support)\b",
    ]

    FIX_ALL_PATTERNS: ClassVar[list[str]] = [
        r"\b(fix|implement|do|complete)\s+(?:all|every)\s+(?:\d+\s+)?(?:items?|things?)\b",
        r"\bfix\s+all\s+\d+\b",
    ]

    NEGATION_PATTERNS: ClassVar[list[str]] = [
        r"\b(?:do\s+)?not\s+(?:write|generate|create)\s+(?:any\s+)?code\b",
        r"\bno\s+code\s+generation\b",
        r"\banalysis\s+only\b",
        r"\bread[- ]only\b",
        r"\bjust\s+(?:analyze|review|examine|look|check)\b",
        r"\bdon'?t\s+(?:change|modify|update|edit|implement|fix)\s*(?:any\s*thing|anything|files?|code|it)?\b",
        r"\bdo\s+not\s+(?:change|modify|update|edit|implement|fix)\b",
        r"\bno\s+(?:modifications?|changes?|edits?|implementations?)\b",
        r"\bdon'?t\s+(?:implement|write|create|generate)\b",
        r"\b(?:without|no)\s+(?:making\s+)?(?:any\s+)?(?:changes?|modifications?)\b",
        r"\b(?:examine|inspect|review|check)\s+(?:but\s+)?(?:without|don'?t)\b",
    ]

    def __init__(self):
        self.quantity_parser = QuantityParser()
        self._compile_patterns()

    EXPLANATION_PATTERNS: ClassVar[list[str]] = [
        r"\b(tell\s+me\s+about|explain|describe|what\s+is|who\s+is|where\s+is|when\s+did)\b",
        r"\b(summarize|overview|background|history|biography)\b",
    ]

    def _compile_patterns(self):
        """Compile all regex patterns."""
        self._analysis_re = [re.compile(p, re.IGNORECASE) for p in self.ANALYSIS_PATTERNS]
        self._list_re = [re.compile(p, re.IGNORECASE) for p in self.LIST_PATTERNS]
        self._impl_re = [re.compile(p, re.IGNORECASE) for p in self.IMPLEMENTATION_PATTERNS]
        self._fix_all_re = [re.compile(p, re.IGNORECASE) for p in self.FIX_ALL_PATTERNS]
        self._negation_re = [re.compile(p, re.IGNORECASE) for p in self.NEGATION_PATTERNS]
        self._explanation_re = [re.compile(p, re.IGNORECASE) for p in self.EXPLANATION_PATTERNS]

    def classify(self, request: str) -> ClassifiedRequestV2:
        """
        Items 21-35: Classify request with comprehensive analysis.
        """
        reasons = []

        # Extract mentioned files
        files_mentioned = []
        file_pattern = re.compile(r"\b([\w\-/]+\.(?:py|js|ts|tsx|jsx|html|css|json|md|txt|yaml|yml|sh|bash|sql|c|cpp|h|hpp|rs|go|java|kt|rb|php))\b")
        files_mentioned = list(set(file_pattern.findall(request)))

        # Item 1-20: Parse quantity
        quantity_result = self.quantity_parser.parse(request)
        if quantity_result.quantity:
            reasons.append(
                f"Detected quantity: {quantity_result.quantity} ({quantity_result.detection_method})"
            )

        # Item 26: Check for negation (forces read-only)
        has_negation = any(p.search(request) for p in self._negation_re)
        if has_negation:
            reasons.append("Explicit negation detected: forcing read-only")

        # Calculate type scores
        list_score = sum(1 for p in self._list_re if p.search(request))
        analysis_score = sum(1 for p in self._analysis_re if p.search(request))
        impl_score = sum(1 for p in self._impl_re if p.search(request))

        # Check fix-all first (hybrid)
        if any(p.search(request) for p in self._fix_all_re) and not has_negation:
            reasons.append("Fix-all pattern detected")
            return ClassifiedRequestV2(
                original_request=request,
                request_type=RequestTypeV2.FIX_ALL,
                output_format=OutputFormatV2.MIXED,
                pipeline_type=PipelineTypeV2.MULTI_STEP,
                quantity_result=quantity_result,
                classification_reasons=reasons,
                read_only=False,
                files_mentioned=files_mentioned
            )

        # Check for hybrid patterns
        has_fix_verb = re.search(r"\b(fix|implement|apply|update|change|refactor|patch|resolve|modify)\b", request, re.IGNORECASE) is not None
        has_do_verb = re.search(r"\bdo\b(?!\s+not)", request, re.IGNORECASE) is not None
        has_analysis_verb = re.search(r"\b(analyze|identify|find|check|review|audit|examine)\b", request, re.IGNORECASE) is not None

        if (has_fix_verb or has_do_verb) and has_analysis_verb and not has_negation:
            reasons.append("Hybrid request detected (analysis + implementation)")
            return ClassifiedRequestV2(
                original_request=request,
                request_type=RequestTypeV2.MULTI_STEP,
                output_format=OutputFormatV2.MIXED,
                pipeline_type=PipelineTypeV2.MULTI_STEP,
                quantity_result=quantity_result,
                classification_reasons=reasons,
                read_only=False,
                requires_file_refs=True,
                files_mentioned=files_mentioned
            )

        # Check list generation
        has_quantity_list_indicators = (
            quantity_result.quantity
            and quantity_result.quantity >= 10
            and re.search(r"\b(list|things?|items?|improvements?|issues?)\b", request, re.IGNORECASE) is not None
        )

        if list_score > 0 or has_quantity_list_indicators:
            if not impl_score and (not analysis_score or list_score > 0):
                reasons.append(f"List generation detected (score: {list_score})")
                output_format = OutputFormatV2.MARKDOWN_TABLE if (quantity_result.quantity and quantity_result.quantity > 20) else OutputFormatV2.MARKDOWN_LIST
                return ClassifiedRequestV2(
                    original_request=request,
                    request_type=RequestTypeV2.LIST_GENERATION,
                    output_format=output_format,
                    pipeline_type=PipelineTypeV2.LIST_GENERATION,
                    quantity_result=quantity_result,
                    classification_reasons=reasons,
                    min_items=quantity_result.quantity or 10,
                    files_mentioned=files_mentioned
                )

        # Check implementation
        if impl_score > 0 and not has_negation:
            reasons.append(f"Implementation pattern detected (score: {impl_score})")
            return ClassifiedRequestV2(
                original_request=request,
                request_type=RequestTypeV2.IMPLEMENTATION,
                output_format=OutputFormatV2.CODE_FILES,
                pipeline_type=PipelineTypeV2.IMPLEMENTATION,
                quantity_result=quantity_result,
                classification_reasons=reasons,
                read_only=False,
                files_mentioned=files_mentioned
            )

        # Check analysis
        if analysis_score > 0:
            reasons.append(f"Analysis pattern detected (score: {analysis_score})")
            return ClassifiedRequestV2(
                original_request=request,
                request_type=RequestTypeV2.ANALYSIS,
                output_format=OutputFormatV2.MARKDOWN_LIST,
                pipeline_type=PipelineTypeV2.ANALYSIS_ONLY,
                quantity_result=quantity_result,
                classification_reasons=reasons,
                files_mentioned=files_mentioned
            )

        # Check explanation/informational
        if any(p.search(request) for p in self._explanation_re):
            reasons.append("Explanation/Informational pattern detected")
            return ClassifiedRequestV2(
                original_request=request,
                request_type=RequestTypeV2.EXPLANATION,
                output_format=OutputFormatV2.EXPLANATION,
                pipeline_type=PipelineTypeV2.SIMPLE_RESPONSE,
                quantity_result=quantity_result,
                classification_reasons=reasons,
                files_mentioned=files_mentioned
            )

        # Check question
        if re.search(r"\?|^(what|how|why|who|where|when|which|is|are|can|do|does)\b", request, re.IGNORECASE):
            reasons.append("Question pattern detected")
            return ClassifiedRequestV2(
                original_request=request,
                request_type=RequestTypeV2.QUESTION,
                output_format=OutputFormatV2.PLAIN_TEXT,
                pipeline_type=PipelineTypeV2.SIMPLE_RESPONSE,
                quantity_result=quantity_result,
                classification_reasons=reasons,
                files_mentioned=files_mentioned
            )

        # Default fallback
        reasons.append("No strong patterns detected: falling back to ANALYSIS")
        return ClassifiedRequestV2(
            original_request=request,
            request_type=RequestTypeV2.ANALYSIS,
            output_format=OutputFormatV2.MARKDOWN_LIST,
            pipeline_type=PipelineTypeV2.ANALYSIS_ONLY,
            quantity_result=quantity_result,
            classification_reasons=reasons,
            files_mentioned=files_mentioned
        )


class HybridIntentDetector:
    """
    P0 Items 1-50: Detects hybrid requests that combine multiple intents.
    """

    INTENT_SIGNALS: ClassVar[list[IntentSignal]] = [
        IntentSignal(r"\b(fix|repair|correct|patch)\s+(?:this|that|the|a|an)?\s*(?:bug|error|issue|problem|failing|code)", IntentType.FIX, weight=2.0),
        IntentSignal(r"\b(patch|repair|fix)\s+(?:the\s+)?(?:security\s+)?(?:vulnerability|broken\s+code|damage)", IntentType.FIX, weight=2.0),
        IntentSignal(r"^(fix|repair|correct)\s+(?:this|that|it)\b", IntentType.FIX, weight=2.5),
        IntentSignal(r"\b(?:and|then|,)\s*(fix|repair|correct)\b", IntentType.FIX, weight=2.0),
        IntentSignal(r"\b(implement|create|build|add|write|develop|make)\b", IntentType.IMPLEMENT, weight=1.5),
        IntentSignal(r"\b(refactor|restructure|reorganize|rewrite|redesign)\b", IntentType.REFACTOR, weight=1.5),
        IntentSignal(r"\b(modify|change|alter|edit)\s+(?:the\s+)?(?:existing\s+)?(?:code|file|function|class)", IntentType.IMPLEMENT, weight=1.8),
        IntentSignal(r"\b(test|write\s+test|add\s+test|create\s+test)\b", IntentType.TEST, weight=1.5),
        IntentSignal(r"\b(document|add\s+docstring|add\s+comment|write\s+docs?)\b", IntentType.DOCUMENT, weight=1.5),
        IntentSignal(r"\b(optimize|improve|enhance|speed\s+up|make\s+faster|update|upgrade)\b", IntentType.OPTIMIZE, weight=1.5),
        IntentSignal(r"\b(secure|fix\s+vulnerability|patch\s+security)\b", IntentType.SECURE, weight=2.0),
        IntentSignal(r"\b(deploy|release|publish|ship)\b", IntentType.DEPLOY, weight=1.5),
        IntentSignal(r"\b(migrate|upgrade|update\s+(?:to|version))\b", IntentType.MIGRATE, weight=1.5),
        IntentSignal(r"\b(configure|set\s+up|setup|install)\b", IntentType.CONFIGURE, weight=1.3),
        IntentSignal(r"\b(debug|troubleshoot|diagnose)\s+(?:and\s+)?(?:fix)?", IntentType.DEBUG, weight=1.8),
        IntentSignal(r"\bthen\s+do\b", IntentType.IMPLEMENT, weight=2.0),
        IntentSignal(r"\bdo\s+(?:it|them|all|everything)\b", IntentType.IMPLEMENT, weight=1.8),
        IntentSignal(r"\b(analyze|analyse|review|audit|assess|evaluate|examine)\b", IntentType.ANALYZE, weight=1.0),
        IntentSignal(r"\b(?:with|start|begin|do)\s+(?:an?\s+)?analysis\b", IntentType.ANALYZE, weight=1.2),
        IntentSignal(r"\bwhat(?:'s| is)\s+wrong\b", IntentType.ANALYZE, weight=1.5),
        IntentSignal(r"\bfind\s+(?:the\s+)?(?:problems?|issues?|bugs?|errors?)\b", IntentType.ANALYZE, weight=1.5),
        IntentSignal(r"\bcheck\s+(?:for\s+)?(?:potential\s+)?(?:bugs?|problems?|issues?|errors?)\b", IntentType.ANALYZE, weight=1.5),
        IntentSignal(r"\b(?:identify|spot|detect)\s+(?:potential\s+)?(?:bugs?|problems?|issues?)\b", IntentType.ANALYZE, weight=1.5),
        IntentSignal(r"\b(?:to|proceed|move|with)\s+(?:the\s+)?implementation\b", IntentType.IMPLEMENT, weight=1.5),
        IntentSignal(r"\b(list|enumerate|identify|find|show)\s+(?:\d+\s+)?(?:things?|items?|issues?|improvements?)", IntentType.LIST, weight=1.0),
        IntentSignal(r"\b(explain|describe|tell\s+me|clarify)\b", IntentType.EXPLAIN, weight=0.8),
        IntentSignal(r"\b(compare|difference|contrast)\b", IntentType.COMPARE, weight=0.8),
        IntentSignal(r"\b(search|find|locate|look\s+for)\b", IntentType.SEARCH, weight=0.8),
        IntentSignal(r"\b(plan|design|architect|outline)\b", IntentType.PLAN, weight=1.0),
        IntentSignal(r"^(?:what|how|why|when|where|which|who|can|does|is|are)\s+", IntentType.QUESTION, weight=0.8),
        IntentSignal(r"\?$", IntentType.QUESTION, weight=0.5),
    ]

    HYBRID_CONNECTORS: ClassVar[list[str]] = [
        r"\b(?:and\s+(?:then\s+)?(?:also\s+)?|then\s+|after\s+(?:that|this)\s+|,\s*then\s+|;\s*then\s+)",
        r"\bfirst\s+.{5,50}\s+then\s+",
        r"\bafter\s+(?:you\s+)?(?:analyze|list|identify|find).{5,50}\s+(?:fix|implement|do|apply|execute)",
        r"\b(?:analyze|list|review).{0,50}(?:and|then)\s+(?:fix|implement|do|apply|execute)\b",
        r"\b(?:start|begin)\s+(?:with|by)\s+.{5,50}(?:proceed|move|continue)\s+(?:to|with)\s+",
        r"\s+->\s+",
        r"\b(?:analyze|list|review)\s*,\s*(?:plan|design)\s*,\s*(?:implement|fix|do)\b",
    ]

    IMPLEMENTATION_OVERRIDE_SIGNALS: ClassVar[list[str]] = [
        r"\b(?:don't\s+just|not\s+just|actually|really)\s+(?:analyze|list|review|identify)",
        r"\b(?:then\s+)?(?:fix|implement|do|apply|execute|solve)\s+(?:them|it|all|each|every)\b",
        r"\b(?:start|begin)\s+(?:fixing|implementing|coding|developing)\b",
        r"\bmake\s+(?:the\s+)?(?:changes?|fixes?|updates?|improvements?)\b",
        r"\bdo\s+(?:all\s+)?(?:the\s+)?(?:items?|things?|changes?|fixes?)\b",
        r"\bapply\s+(?:all\s+)?(?:the\s+)?(?:changes?|fixes?|suggestions?)\b",
        r"\bexecute\s+(?:all\s+)?(?:the\s+)?(?:steps?|tasks?|items?)\b",
        r"\b(?:use\s+)?TDD\b",
        r"\bwrite\s+(?:the\s+)?(?:code|tests?|implementation)\b",
        r"\b(?:create|generate)\s+(?:the\s+)?(?:files?|code|implementation)\b",
        r"\bactually\s+(?:code|implement|fix|do)\b",
        r"\bstop\s+(?:analyzing|listing|reviewing)\s+and\s+(?:start\s+)?(?:fix|implement|code)",
        r"\bfix\s+(?:the\s+)?(?:error|bug|issue|problem|failing)",
    ]

    READ_ONLY_SIGNALS: ClassVar[list[str]] = [
        r"\bjust\s+(?:analyze|list|review|explain|describe|tell)\b",
        r"\bonly\s+(?:analyze|list|review|explain|describe|tell)\b",
        r"\bdon't\s+(?:make\s+changes?|modify|change|fix|implement)\b",
        r"\bdo\s+not\s+(?:make\s+changes?|modify|change|fix|implement)\b",
        r"\bno\s+(?:changes?|modifications?|code)\b",
        r"\bread[- ]only\b",
        r"\bwithout\s+(?:making\s+)?(?:changes?|modifications?)\b",
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for efficiency."""
        self._intent_patterns = [
            (re.compile(s.pattern, re.IGNORECASE), s) for s in self.INTENT_SIGNALS
        ]
        self._hybrid_re = [re.compile(p, re.IGNORECASE) for p in self.HYBRID_CONNECTORS]
        self._impl_override_re = [
            re.compile(p, re.IGNORECASE) for p in self.IMPLEMENTATION_OVERRIDE_SIGNALS
        ]
        self._read_only_re = [re.compile(p, re.IGNORECASE) for p in self.READ_ONLY_SIGNALS]

    def detect(self, request: str) -> HybridIntent:
        """Detect hybrid intent from request."""
        intent_scores: dict[IntentType, float] = {}
        for pattern, signal in self._intent_patterns:
            if pattern.search(request):
                current = intent_scores.get(signal.intent_type, 0.0)
                intent_scores[signal.intent_type] = current + signal.weight

        has_hybrid_connector = any(p.search(request) for p in self._hybrid_re)
        has_impl_override = any(p.search(request) for p in self._impl_override_re)
        has_read_only_signal = any(p.search(request) for p in self._read_only_re)

        sorted_intents = sorted(intent_scores.items(), key=lambda x: -x[1])
        primary_intents = [i for i, s in sorted_intents[:2] if s >= 1.0]
        secondary_intents = [i for i, s in sorted_intents[2:] if s >= 0.5]

        if not primary_intents:
            primary_intents = [IntentType.UNKNOWN]

        is_hybrid = has_hybrid_connector or len(primary_intents) >= 2 or has_impl_override

        implementation_intents = {
            IntentType.IMPLEMENT, IntentType.FIX, IntentType.REFACTOR, IntentType.TEST,
            IntentType.DOCUMENT, IntentType.OPTIMIZE, IntentType.SECURE, IntentType.CONFIGURE,
            IntentType.DEBUG, IntentType.DEPLOY, IntentType.MIGRATE,
        }

        has_implementation_intent = any(i in implementation_intents for i in primary_intents)

        if has_read_only_signal and not has_impl_override:
            execution_mode = ExecutionMode.READ_ONLY
        elif has_impl_override or has_implementation_intent:
            execution_mode = ExecutionMode.WRITE_ENABLED
        else:
            execution_mode = ExecutionMode.READ_ONLY

        return HybridIntent(
            primary_intents=primary_intents,
            secondary_intents=secondary_intents,
            is_hybrid=is_hybrid,
            execution_mode=execution_mode,
            requires_implementation=execution_mode == ExecutionMode.WRITE_ENABLED
        )
