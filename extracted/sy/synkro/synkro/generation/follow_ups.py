"""Follow-up question generation for multi-turn conversations."""

import random
from typing import Literal

from synkro.llm.client import LLM
from synkro.models import Model, OpenAI
from synkro.prompts.multiturn_templates import FOLLOW_UP_GENERATION_PROMPT
from synkro.schemas import FollowUpQuestion
from synkro.types.core import Message

QuestionType = Literal["clarification", "edge_case", "what_if", "specificity", "challenge"]

# Weighted pool — any type can appear on any turn
QUESTION_TYPE_WEIGHTS: dict[QuestionType, float] = {
    "what_if": 0.25,
    "edge_case": 0.25,
    "challenge": 0.20,
    "specificity": 0.15,
    "clarification": 0.15,
}


class FollowUpGenerator:
    """
    Generates follow-up questions for multi-turn conversations.

    Uses weighted random selection for question types:
    - what_if (25%): Explore hypothetical variations
    - edge_case (25%): Probe boundary conditions
    - challenge (20%): Question reasoning or push back
    - specificity (15%): Drill into specific details
    - clarification (15%): Ask about ambiguous points

    Examples:
        >>> gen = FollowUpGenerator()
        >>> follow_up = await gen.generate(policy_text, messages, turn_index=2)
        >>> print(follow_up.question)
    """

    def __init__(self, llm: LLM | None = None, model: Model = OpenAI.GPT_4O_MINI):
        """
        Initialize the follow-up generator.

        Args:
            llm: LLM client to use (creates one if not provided)
            model: Model to use if creating LLM
        """
        self.llm = llm or LLM(model=model)

    def _select_question_type(self, turn_index: int) -> QuestionType:
        """Select a random question type weighted by usefulness."""
        types = list(QUESTION_TYPE_WEIGHTS.keys())
        weights = list(QUESTION_TYPE_WEIGHTS.values())
        return random.choices(types, weights=weights, k=1)[0]

    def _format_conversation(self, messages: list[Message]) -> str:
        """Format conversation messages for prompt inclusion."""
        formatted = []
        for msg in messages:
            role = msg.role.upper()
            content = msg.content or "[No content]"
            formatted.append(f"{role}: {content}")
        return "\n\n".join(formatted)

    async def generate(
        self,
        policy_text: str,
        messages: list[Message],
        turn_index: int,
        question_type: QuestionType | None = None,
        scenario_index: int = 0,
    ) -> FollowUpQuestion:
        """
        Generate a follow-up question for the conversation.

        Args:
            policy_text: The policy text for context
            messages: Conversation messages so far
            turn_index: Which turn this is (1-based)
            question_type: Override auto-selected question type
            scenario_index: Index for the scenario (default 0)

        Returns:
            FollowUpQuestion with the generated question
        """
        # Select question type if not specified
        if question_type is None:
            question_type = self._select_question_type(turn_index)

        # Format conversation for prompt
        conversation = self._format_conversation(messages)

        # Build prompt
        prompt = FOLLOW_UP_GENERATION_PROMPT.format(
            question_type=question_type,
            conversation=conversation,
            policy=policy_text,
        )

        try:
            # Generate the follow-up question
            response = await self.llm.generate(prompt)
            question_text = response.strip()

            return FollowUpQuestion(
                index=scenario_index,
                question=question_text,
                question_type=question_type,
            )
        except Exception:
            # Fallback generic follow-up
            fallback_questions = {
                "clarification": "Can you clarify that further?",
                "edge_case": "What about edge cases?",
                "what_if": "What if the situation changes?",
                "specificity": "Can you be more specific?",
                "challenge": "Why is that the best approach?",
            }
            return FollowUpQuestion(
                index=scenario_index,
                question=fallback_questions.get(question_type, "Can you elaborate?"),
                question_type=question_type,
            )
