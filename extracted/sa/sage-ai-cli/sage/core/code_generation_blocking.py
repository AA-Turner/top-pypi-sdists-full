"""
Code Generation Blocking for SAGE - Items 51-70 from Roadmap P0.

This module provides logic to block code generation in read-only analysis requests.
"""

from __future__ import annotations

import re
from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from sage.core.p0_request_classification import ClassifiedRequestV2


class CodeBlockerV2:
    """
    Items 51-70: Comprehensive code generation blocking for read-only requests.
    """

    # Item 51-56: Code patterns to block
    CODE_PATTERNS: ClassVar[list[tuple[str, str]]] = [
        (r"^FILE:\s*\S+", "FILE: block"),
        # Full language names
        (
            r"```(?:python|javascript|typescript|java|go|rust|cpp|c\+\+|ruby|php|swift|kotlin|csharp)",
            "language code block",
        ),
        # Short language aliases (py, js, ts, etc.)
        (r"```(?:py|js|ts|jsx|tsx|rb|rs|kt)\n", "language code block"),
        # Unlabeled/empty code blocks (just ``` with newline)
        (r"```\n[\s\S]*?```", "code block"),
        (r"^\s*def\s+\w+\s*\(", "function definition"),
        (r"^\s*class\s+\w+\s*[:\(]", "class definition"),
        (r"^\s*function\s+\w+\s*\(", "JS function"),
        (r"^\s*(?:const|let|var)\s+\w+\s*=", "variable declaration"),
        (r"^\s*import\s+\w+\s+from", "import statement"),
        (r"^\s*from\s+\w+\s+import", "Python import"),
        (r"^\s*require\s*\(", "require statement"),
    ]

    # Item 57-58: Allowed patterns (code references/examples)
    ALLOWED_PATTERNS: ClassVar[list[str]] = [
        r"```(?:bash|shell|console|text|output|log|terminal)",  # Command examples OK
        r"`[^`]+`",  # Inline code references OK
        r"```\s*#\s*(?:example|output)",  # Marked examples OK
    ]

    # Item 58+: Context patterns that indicate illustrative examples (not generation)
    ILLUSTRATIVE_CONTEXT_PATTERNS: ClassVar[list[str]] = [
        r"(?:current|existing|problematic|buggy|original)\s+code",  # "Current code:"
        r"(?:should|could|might)\s+be",  # "Should be changed to"
        r"(?:before|after)[:.]",  # Before/after examples
        r"(?:problem|issue|bug)(?:atic)?(?:\s+is)?[:.]",  # "The problem:"
        r"(?:here'?s|for\s+example|e\.g\.|example)[:.]",  # Example markers
        r"^\d+\.\s+",  # List item context
        r"^\*\s+",  # Bullet item context
        r"instead\s+of",  # Comparison context
    ]

    def __init__(self):
        self._code_re = [
            (re.compile(p, re.MULTILINE | re.IGNORECASE), name) for p, name in self.CODE_PATTERNS
        ]
        self._allowed_re = [
            re.compile(p, re.MULTILINE | re.IGNORECASE) for p in self.ALLOWED_PATTERNS
        ]
        self._illustrative_re = [
            re.compile(p, re.IGNORECASE | re.MULTILINE) for p in self.ILLUSTRATIVE_CONTEXT_PATTERNS
        ]

    def check(self, response: str) -> tuple[bool, list[str]]:
        """
        Items 51-62: Check response for forbidden code patterns.
        """
        violations = []

        # Check each code pattern
        for pattern, name in self._code_re:
            match = pattern.search(response)
            if match:
                # FILE: blocks are ALWAYS violations in read-only mode
                if name == "FILE: block":
                    violations.append(f"Contains {name}")
                    continue

                # For other code patterns, check if it's in an allowed/illustrative context
                matched_text = match.group(0)
                is_allowed = self._is_match_allowed(response, matched_text, match.start())
                if not is_allowed:
                    violations.append(f"Contains {name}")

        return len(violations) > 0, violations

    def has_code(self, text: str) -> bool:
        """Check if text contains code patterns."""
        has_violations, _ = self.check(text)
        return has_violations

    def detect_language(self, text: str) -> str | None:
        """Detect the programming language from code blocks."""
        match = re.search(r"```([\w+#]+)\n", text, re.IGNORECASE)
        if match:
            lang = match.group(1).lower()
            lang_map = {
                "py": "python",
                "js": "javascript",
                "ts": "typescript",
                "jsx": "javascript",
                "tsx": "typescript",
                "rb": "ruby",
                "rs": "rust",
                "kt": "kotlin",
                "cpp": "c++",
            }
            return lang_map.get(lang, lang)
        return None

    def _is_match_allowed(self, response: str, matched_text: str, match_pos: int) -> bool:
        """Item 57-58: Check if a specific match is in an allowed context."""
        bash_blocks = list(
            re.finditer(
                r"```(?:bash|shell|console|text|output|log|terminal)[\s\S]*?```",
                response,
                re.IGNORECASE,
            )
        )
        for block in bash_blocks:
            if block.start() <= match_pos <= block.end():
                return True

        if (
            matched_text.startswith("`")
            and matched_text.endswith("`")
            and "```" not in matched_text
        ):
            return True

        context_start = max(0, match_pos - 200)
        context_before = response[context_start:match_pos].lower()

        for pattern in self._illustrative_re:
            if pattern.search(context_before):
                return True

        line_start = response.rfind("\n", 0, match_pos) + 1
        line_text = response[line_start:match_pos]
        if re.match(r"^\d+\.\s+", line_text):
            return True

        if any(
            kw in context_before
            for kw in [
                "should be",
                "could be",
                "instead of",
                "before:",
                "after:",
                "current:",
                "fix:",
            ]
        ):
            return True

        return False

    def strip_code(self, response: str, remove_completely: bool = True) -> str:
        """Item 60: Remove code blocks from response."""
        replacement = "" if remove_completely else "[Code block removed - analysis only mode]"

        response = re.sub(
            r"^FILE:\s*\S+\s*\n```[\s\S]*?```", replacement, response, flags=re.MULTILINE
        )

        response = re.sub(
            r"```(?:python|javascript|typescript|java|go|rust|cpp|ruby|php|swift|kotlin|csharp)[\s\S]*?```",
            replacement,
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(
            r"```(?:py|js|ts|jsx|tsx|rb|rs|kt)\n[\s\S]*?```",
            replacement,
            response,
            flags=re.IGNORECASE,
        )

        response = re.sub(r"```\n[\s\S]*?```", replacement, response)

        return response

    def get_blocking_prompt(self, classification: ClassifiedRequestV2) -> str:
        """Items 63-64: Generate strong blocking prompt for read-only requests."""
        if not getattr(classification, 'strict_read_only', False):
            return ""

        quantity_reminder = ""
        quantity_required = getattr(classification, 'quantity_required', 0)
        if quantity_required:
            quantity_reminder = f"""

## QUANTITY REQUIREMENT: {quantity_required}+ ITEMS
You MUST produce at least {quantity_required} distinct, numbered items.
DO NOT stop until you have {quantity_required} items.
"""

        return f"""
## CODE GENERATION BLOCKED

This request is classified as: {classification.request_type.name if hasattr(classification.request_type, 'name') else classification.request_type}
Pipeline: {classification.pipeline_type.name if hasattr(classification.pipeline_type, 'name') else classification.pipeline_type}

You are FORBIDDEN from:
- Writing FILE: blocks
- Generating implementation code
- Creating code blocks with programming languages
- Writing code that modifies any files

Your response MUST contain ONLY:
- Analysis text and explanations
- File path references in backticks (`file.py`)
- Line number citations
- Numbered list items
- Priority rankings (P0, P1, P2, P3)

ANY CODE YOU WRITE WILL BE AUTOMATICALLY STRIPPED.
{quantity_reminder}
""".strip()

    def contains_code(self, text: str) -> bool:
        """Check if text contains code blocks."""
        for pattern, _ in self._code_re:
            if pattern.search(text):
                return True
        return False

    def has_file_blocks(self, text: str) -> bool:
        """Check if text contains FILE: blocks."""
        return bool(re.search(r"^FILE:\s*\S+", text, re.MULTILINE))

    def has_commands(self, text: str) -> bool:
        """Check if text contains command blocks or inline commands."""
        if re.search(r"```(?:bash|shell|console|terminal)", text, re.IGNORECASE):
            return True
        if re.search(r"(?:Run|Execute|run|execute):\s*`[^`]+`", text):
            return True
        if re.search(r"`(?:pip|npm|yarn|git|docker|make|cargo|go|python|node)\s+[^`]+`", text):
            return True
        return False

    def extract_code_blocks(self, text: str) -> list[dict]:
        """Extract all code blocks from text."""
        blocks = []
        for match in re.finditer(r"```(\w+)?\n([\s\S]*?)```", text):
            language = match.group(1) or "unknown"
            code = match.group(2)
            blocks.append(
                {"language": language, "code": code, "start": match.start(), "end": match.end()}
            )
        return blocks
