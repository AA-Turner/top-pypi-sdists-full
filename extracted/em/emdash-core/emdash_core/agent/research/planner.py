"""Planner agent for creating research plans.

The Planner decomposes research goals into questions that map to
how the team works. It aligns with team values by:
- V3: Creating reviewer-first output sections
- V4: Setting budgets for cost awareness
- V5: Ensuring actionable outcomes
- V6: Using team vocabulary
"""

import json
from typing import Optional

from rich.console import Console

from ..providers import get_provider
from ..providers.factory import DEFAULT_MODEL
from .state import (
    ResearchPlan,
    ResearchQuestion,
)
from .macros import suggest_macros, TOOL_MACROS


# Valid tool names that can be suggested
VALID_TOOLS = set(TOOL_MACROS.keys())


# Standard questions aligned with team workflows
STANDARD_QUESTIONS = [
    {
        "category": "feature",
        "template": "What is the feature/behavior of {topic}?",
        "priority": "P0",
        "deliverable": "Design",
        "criteria": ["Entry points identified", "Main functionality described"],
    },
    {
        "category": "implementation",
        "template": "Where is {topic} implemented?",
        "priority": "P0",
        "deliverable": "Implementation",
        "criteria": ["File paths found", "Key functions/classes identified"],
    },
    {
        "category": "dependencies",
        "template": "What depends on {topic}?",
        "priority": "P1",
        "deliverable": "Implementation",
        "criteria": ["Callers identified", "Dependency graph understood"],
    },
    {
        "category": "ownership",
        "template": "Who owns or touches {topic}?",
        "priority": "P1",
        "deliverable": "Review",
        "criteria": ["Authors identified", "Expertise areas mapped"],
    },
    {
        "category": "risk",
        "template": "What's risky about {topic}?",
        "priority": "P1",
        "deliverable": "Review",
        "criteria": ["Risk factors identified", "Impact scope assessed"],
    },
    {
        "category": "testing",
        "template": "What tests/CI validate {topic}?",
        "priority": "P2",
        "deliverable": "Testing",
        "criteria": ["Test files identified", "Coverage understood"],
    },
    {
        "category": "review",
        "template": "What should a reviewer check for {topic}?",
        "priority": "P1",
        "deliverable": "Review",
        "criteria": ["Review checklist created", "Critical paths identified"],
    },
]

# Required sections in final report (V3: Reviewer-first)
REQUIRED_SECTIONS = [
    "Findings (fact-grounded)",
    "Evidence Coverage Matrix",
    "Design/Spec Implications",
    "Risks & Unknowns",
    "Recommended Tasks",
    "Reviewer Checklist",
    "Tooling Summary",
]

# Team values checklist for Critic
TEAM_VALUES_CHECKLIST = [
    "V1: All claims have evidence IDs (no ungrounded statements)",
    "V2: Evidence is reproducible (tool calls documented)",
    "V3: Output includes reviewer checklist and acceptance criteria",
    "V4: Budget was respected (no wasteful tool calls)",
    "V5: Report ends with actionable tasks",
    "V6: Uses team vocabulary (tasks, PRs, reviewers)",
]

# Default budgets (V4: Cost awareness)
DEFAULT_BUDGETS = {
    "tool_calls": 100,
    "tokens": 150000,
    "time_s": 600,  # 10 minutes
}


PLANNER_SYSTEM_PROMPT = """You are a research planner that creates structured research plans.

Your job is to decompose a research goal into questions that align with team workflows.

TEAM VALUES YOU MUST RESPECT:
- V1: Truth over fluency - prefer "unknown" over guesses
- V2: Evidence-first - all claims must be backed by tool outputs
- V3: Reviewer-first - output must include review checklists
- V4: Cost awareness - minimize tool calls, start with cheap models
- V5: Actionable outcomes - end with concrete tasks
- V6: Team alignment - use team vocabulary

QUESTION CATEGORIES:
1. Feature/Behavior - What is it?
2. Implementation - Where is the code?
3. Dependencies - What depends on it?
4. Ownership - Who owns/touches it?
5. Risk - What could go wrong?
6. Testing - How is it tested?
7. Review - What should reviewers check?

AVAILABLE TOOL MACROS (only use these names):
- deep_feature_analysis: Understand feature behavior and impact
- team_activity_analysis: Find owners, expertise, velocity risks
- architectural_deep_dive: Map architecture and key modules
- implementation_trace: Trace specific implementation paths
- risk_assessment: Assess risks of modifications
- pr_context: Understand PR and change context

OUTPUT FORMAT:
Return a JSON object with:
{
  "topic": "extracted topic from goal",
  "questions": [
    {
      "qid": "Q1",
      "question": "specific question",
      "priority": "P0|P1|P2",
      "success_criteria": ["criterion 1", "criterion 2"],
      "suggested_tools": ["deep_feature_analysis"],
      "deliverable": "Design|Implementation|Testing|Review|Ops"
    }
  ],
  "max_iterations": 5,
  "budgets": {
    "tool_calls": 100,
    "tokens": 150000,
    "time_s": 600
  }
}

PRIORITIES:
- P0: Must answer (blocking)
- P1: Should answer (important)
- P2: Nice to have (optional)

Be specific in questions. Avoid vague language. Every question should be answerable with tools.
IMPORTANT: Only suggest tools from the AVAILABLE TOOL MACROS list above."""


class PlannerAgent:
    """Creates research plans with team-aligned questions.

    The Planner analyzes the research goal and creates a structured
    plan with prioritized questions, budgets, and success criteria.
    """

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
    ):
        """Initialize the planner agent.

        Args:
            model: LLM model to use
            verbose: Whether to print progress
        """
        self.provider = get_provider(model)
        self.model = model
        self.verbose = verbose
        self.console = Console()

    def create_plan(
        self,
        goal: str,
        context: str = "",
        max_iterations: int = 3,
        budgets: Optional[dict] = None,
    ) -> ResearchPlan:
        """Create a research plan for a goal.

        Args:
            goal: The research goal
            context: Additional context
            max_iterations: Maximum research iterations
            budgets: Resource budgets (tool_calls, tokens, time_s)

        Returns:
            ResearchPlan with questions and budgets
        """
        if self.verbose:
            self.console.print(f"[cyan]Planning research for:[/cyan] {goal}")

        # Try LLM-based planning first
        try:
            plan = self._llm_plan(goal, context, max_iterations, budgets)
            if plan and plan.questions:
                if self.verbose:
                    self.console.print(f"[green]Created plan with {len(plan.questions)} questions[/green]")
                return plan
        except Exception as e:
            if self.verbose:
                self.console.print(f"[yellow]LLM planning failed: {e}. Using template.[/yellow]")

        # Fallback to template-based planning
        return self._template_plan(goal, context, max_iterations, budgets)

    def _llm_plan(
        self,
        goal: str,
        context: str,
        max_iterations: int,
        budgets: Optional[dict],
    ) -> Optional[ResearchPlan]:
        """Create plan using LLM.

        Args:
            goal: Research goal
            context: Additional context
            max_iterations: Max iterations
            budgets: Resource budgets

        Returns:
            ResearchPlan or None on failure
        """
        user_message = f"""Create a research plan for this goal:

GOAL: {goal}

{f'CONTEXT: {context}' if context else ''}

Create questions that will help understand this topic thoroughly.
Prioritize P0 questions that are essential to answer.
Suggest appropriate tool macros for each question.

Return JSON only, no markdown code blocks."""

        messages = [
            {"role": "user", "content": user_message},
        ]

        response = self.provider.chat(messages, system=PLANNER_SYSTEM_PROMPT)
        content = response.content or ""

        # Parse JSON from response
        try:
            # Try to extract JSON from response
            json_str = content
            if "```" in content:
                # Extract from code block
                start = content.find("```")
                end = content.find("```", start + 3)
                if end > start:
                    json_str = content[start + 3:end]
                    if json_str.startswith("json"):
                        json_str = json_str[4:]

            data = json.loads(json_str.strip())

            # Build questions
            questions = []
            for i, q in enumerate(data.get("questions", [])):
                # Filter suggested tools to only include valid ones
                raw_tools = q.get("suggested_tools", [])
                valid_suggested = [t for t in raw_tools if t in VALID_TOOLS]
                # If no valid tools, use suggest_macros to pick appropriate ones
                if not valid_suggested:
                    valid_suggested = suggest_macros(q.get("question", ""))

                questions.append(ResearchQuestion(
                    qid=q.get("qid", f"Q{i+1}"),
                    question=q["question"],
                    priority=q.get("priority", "P1"),
                    success_criteria=q.get("success_criteria", []),
                    suggested_tools=valid_suggested,
                    deliverable=q.get("deliverable", "Implementation"),
                ))

            if not questions:
                return None

            # Use provided budgets or defaults
            final_budgets = budgets or data.get("budgets", DEFAULT_BUDGETS)

            return ResearchPlan(
                goal=goal,
                questions=questions,
                max_iterations=data.get("max_iterations", max_iterations),
                budgets=final_budgets,
                required_sections=REQUIRED_SECTIONS,
                team_values_checklist=TEAM_VALUES_CHECKLIST,
            )

        except (json.JSONDecodeError, KeyError, TypeError):
            return None

    def _template_plan(
        self,
        goal: str,
        context: str,
        max_iterations: int,
        budgets: Optional[dict],
    ) -> ResearchPlan:
        """Create plan using templates.

        Fallback method that generates questions from standard templates.

        Args:
            goal: Research goal
            context: Additional context
            max_iterations: Max iterations
            budgets: Resource budgets

        Returns:
            ResearchPlan
        """
        # Extract topic from goal
        topic = self._extract_topic(goal)

        # Generate questions from templates
        questions = []
        suggested_macros = suggest_macros(goal)

        for i, template in enumerate(STANDARD_QUESTIONS):
            question_text = template["template"].format(topic=topic)

            # Suggest macros based on category
            tools = []
            if template["category"] == "feature":
                tools = ["deep_feature_analysis"]
            elif template["category"] == "implementation":
                tools = ["implementation_trace"]
            elif template["category"] == "dependencies":
                tools = ["deep_feature_analysis"]
            elif template["category"] == "ownership":
                tools = ["team_activity_analysis"]
            elif template["category"] == "risk":
                tools = ["risk_assessment"]
            elif template["category"] == "testing":
                tools = ["implementation_trace"]
            elif template["category"] == "review":
                tools = ["risk_assessment", "team_activity_analysis"]

            questions.append(ResearchQuestion(
                qid=f"Q{i+1}",
                question=question_text,
                priority=template["priority"],
                success_criteria=template["criteria"],
                suggested_tools=tools,
                deliverable=template["deliverable"],
            ))

        return ResearchPlan(
            goal=goal,
            questions=questions,
            max_iterations=max_iterations,
            budgets=budgets or DEFAULT_BUDGETS,
            required_sections=REQUIRED_SECTIONS,
            team_values_checklist=TEAM_VALUES_CHECKLIST,
        )

    def _extract_topic(self, goal: str) -> str:
        """Extract the main topic from a goal.

        Simple heuristic extraction. Could be improved with NLP.

        Args:
            goal: The research goal

        Returns:
            Extracted topic
        """
        # Remove common prefixes
        topic = goal
        prefixes = [
            "how does", "what is", "where is", "who owns",
            "explain", "understand", "investigate", "research",
            "analyze", "find", "look into",
        ]

        topic_lower = topic.lower()
        for prefix in prefixes:
            if topic_lower.startswith(prefix):
                topic = topic[len(prefix):].strip()
                break

        # Remove trailing punctuation
        topic = topic.rstrip("?!.")

        # Clean up "the" at start
        if topic.lower().startswith("the "):
            topic = topic[4:]

        return topic.strip() or goal

    def adjust_plan(
        self,
        plan: ResearchPlan,
        critique_feedback: list[str],
        drop_p2: bool = False,
    ) -> ResearchPlan:
        """Adjust plan based on critique feedback.

        Called when budget is running low or Critic requests changes.

        Args:
            plan: Current plan
            critique_feedback: Feedback from Critic
            drop_p2: Whether to drop P2 questions

        Returns:
            Adjusted ResearchPlan
        """
        questions = list(plan.questions)

        if drop_p2:
            questions = [q for q in questions if q.priority != "P2"]

        # Could add more sophisticated adjustment based on feedback

        return ResearchPlan(
            goal=plan.goal,
            questions=questions,
            max_iterations=plan.max_iterations,
            budgets=plan.budgets,
            required_sections=plan.required_sections,
            team_values_checklist=plan.team_values_checklist,
        )
