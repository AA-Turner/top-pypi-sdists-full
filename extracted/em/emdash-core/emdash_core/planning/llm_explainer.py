"""LLM-based feature explanation using AST graph context."""

from typing import Optional

from ..core.config import get_config
from .feature_context import FeatureContext
from ..utils.logger import log
from ..agent.providers import get_provider
from ..agent.providers.factory import DEFAULT_MODEL


class LLMExplainer:
    """Uses LLM to explain a feature graph."""

    SYSTEM_PROMPTS = {
        "developer": """You are a senior developer explaining code to another developer.
Focus on:
- Implementation details and patterns used
- How components interact with each other
- Key functions and their responsibilities
- Important design decisions

Be technical but clear. Use code references when helpful.""",

        "architect": """You are a software architect explaining system design.
Focus on:
- High-level architecture and design patterns
- Module boundaries and dependencies
- Data flow between components
- Extensibility and maintainability considerations

Think about the big picture and system organization.""",

        "onboarding": """You are helping a new developer understand the codebase.
Focus on:
- What this code does in simple terms
- Why it's structured this way
- Key concepts a newcomer should understand
- How to get started working with this code

Use analogies and clear explanations. Avoid jargon where possible.""",
    }

    def __init__(self, model: str = DEFAULT_MODEL):
        """Initialize LLM explainer.

        Args:
            model: LLM model to use (claude-* for Anthropic, gpt-* for OpenAI)
        """
        self.model = model
        self._provider = None
        self._available = None

    @property
    def is_available(self) -> bool:
        """Check if LLM is available."""
        if self._available is None:
            try:
                # Try to create provider to check availability
                self._provider = get_provider(self.model)
                self._available = True
            except ValueError as e:
                log.warning(f"LLM provider not available: {e}")
                self._available = False
        return self._available

    def explain_feature(
        self,
        context: FeatureContext,
        style: str = "developer",
        model: Optional[str] = None,
        max_tokens: int = 2000,
    ) -> str:
        """Generate LLM explanation of the feature.

        Args:
            context: The feature context with AST graph
            style: Explanation style - "developer", "architect", or "onboarding"
            model: LLM model to use (defaults to instance model)
            max_tokens: Maximum tokens in response (used as hint)

        Returns:
            LLM-generated explanation
        """
        if not self.is_available:
            return "Error: LLM API key not configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable."

        # Use provided model or default
        use_model = model or self.model
        if use_model != self.model:
            provider = get_provider(use_model)
        else:
            provider = self._provider

        prompt = self._build_prompt(context)
        system_prompt = self.SYSTEM_PROMPTS.get(style, self.SYSTEM_PROMPTS["developer"])

        log.info(f"Generating {style} explanation for: {context.query}")

        try:
            response = provider.chat(
                messages=[{"role": "user", "content": prompt}],
                system=system_prompt,
            )
            return response.content or ""

        except Exception as e:
            log.error(f"LLM explanation failed: {e}")
            return f"Error generating explanation: {e}"

    def _build_prompt(self, context: FeatureContext) -> str:
        """Build prompt from feature context."""
        graph = context.feature_graph

        sections = []

        # Query
        sections.append(f"# Feature Query: {context.query}")
        sections.append("")

        # Root node
        root = context.root_node
        sections.append("## Starting Point")
        sections.append(f"- **Type**: {root.get('type', 'Unknown')}")
        sections.append(f"- **Name**: {root.get('name', 'Unknown')}")
        sections.append(f"- **File**: {root.get('file_path', 'N/A')}")
        if root.get('docstring'):
            docstring = root['docstring'][:300]
            sections.append(f"- **Description**: {docstring}")
        sections.append("")

        # Call graph
        if graph.call_graph:
            sections.append("## Function Call Graph")
            for call in graph.call_graph[:15]:
                sections.append(f"- `{call['caller']}` calls `{call['callee']}`")
            if len(graph.call_graph) > 15:
                sections.append(f"- ... and {len(graph.call_graph) - 15} more calls")
            sections.append("")

        # Classes
        if graph.classes:
            sections.append("## Classes Involved")
            for cls in graph.classes[:10]:
                name = cls.get('name', 'Unknown')
                doc = cls.get('docstring') or 'No description'
                sections.append(f"- **{name}**: {doc[:100]}")
            if len(graph.classes) > 10:
                sections.append(f"- ... and {len(graph.classes) - 10} more classes")
            sections.append("")

        # Functions
        if graph.functions:
            sections.append("## Key Functions")
            for func in graph.functions[:12]:
                name = func.get('name', 'Unknown')
                doc = func.get('docstring') or 'No description'
                sections.append(f"- **{name}**: {doc[:80]}")
            if len(graph.functions) > 12:
                sections.append(f"- ... and {len(graph.functions) - 12} more functions")
            sections.append("")

        # Inheritance
        if graph.inheritance:
            sections.append("## Class Inheritance")
            for inh in graph.inheritance[:8]:
                sections.append(f"- `{inh['child']}` extends `{inh['parent']}`")
            sections.append("")

        # Files
        if graph.files:
            sections.append("## Files")
            for f in graph.files[:8]:
                path = f.get('path', f.get('name', 'Unknown'))
                sections.append(f"- `{path}`")
            if len(graph.files) > 8:
                sections.append(f"- ... and {len(graph.files) - 8} more files")
            sections.append("")

        # Related PRs
        if context.related_prs:
            sections.append("## Related Pull Requests")
            for pr in context.related_prs[:5]:
                sections.append(f"- PR #{pr['number']}: {pr.get('title', 'N/A')}")
            sections.append("")

        # Authors
        if context.authors:
            sections.append("## Domain Experts")
            for author in context.authors[:5]:
                sections.append(f"- {author['name']} ({author['commit_count']} commits)")
            sections.append("")

        # Final instruction
        sections.append("---")
        sections.append("Based on the AST graph above, explain how this feature works, its key components, and how they interact.")

        return "\n".join(sections)
