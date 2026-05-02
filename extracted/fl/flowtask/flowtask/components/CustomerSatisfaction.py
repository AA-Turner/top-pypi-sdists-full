from collections.abc import Callable
import asyncio
from ..interfaces.ParrotBot import ParrotBot
from .flow import FlowComponent


DEFAULT_PROMPT = """
Product: {obj_name}

Question:
"What is the overall customer sentiment, likes and dislikes,
and what insights can be derived from these product reviews for product: {obj_name}?"

Customer Reviews:

"""


class CustomerSatisfaction(ParrotBot, FlowComponent):
    """
    CustomerSatisfaction

    Overview

        The CustomerSatisfaction class is a component for interacting with an IA Agent for making Customer Satisfaction Analysis.
        It extends the FlowComponent class and supports both review analysis and survey analysis modes.

    :widths: auto

        | output_column    |   Yes    | Column for saving the Customer Satisfaction information.                                         |
        | question_prompt  |   No     | Custom question prompt template. Uses default if not provided.                                  |
        | survey           |   No     | Set to true for survey mode (counts responses, no rating). Default: false (review mode).       |
    Return

        A Pandas Dataframe with the Customer Satisfaction statistics.

        **Review Mode Output Columns:**
        - Grouped columns (as specified in 'columns')
        - num_reviews: Count of reviews per group
        - avg_rating: Average rating per group
        - {output_column}: Bot analysis result

        **Survey Mode Output Columns:**
        - Grouped columns (as specified in 'columns')
        - num_responses: Count of survey responses per group
        - weighted_score: Extracted from bot's "Weighted Score" calculation
        - {output_column}: Bot analysis result

    Example (Review Mode):


    Example (Survey Mode):

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CustomerSatisfaction:
          llm:
          llm: google
          model: gemini-2.5-flash
          temperature: 0.4
          max_tokens: 4096
          eval_column: review
          description_column: product_name
          rating_column: rating
          columns:
          - product_id
          - product_name
          output_column: customer_satisfaction
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        self._goal: str = "Customer Satisfaction Analysis using Reviews"
        # Get question prompt from config or use default
        self._question_prompt: str = kwargs.get('question_prompt', DEFAULT_PROMPT)

    def format_question(self, obj_name, reviews, row=None):
        question = self._question_prompt.format(obj_name=obj_name)
        
        # Calculate total responses
        if isinstance(reviews, dict):
            total_responses = sum(reviews.values())
        else:
            total_responses = len(reviews)
               
        # Add metadata to question
        question += f"\nTotal responses: {total_responses}\n"        
        # Check if we're in survey mode and have grouped responses with counts
        if hasattr(self, '_survey_mode') and self._survey_mode and isinstance(reviews, dict):
            # Survey mode: reviews is a dict with response counts
            for response_text, count in reviews.items():
                question += f"* {response_text} (mentioned {count} times)\n"
        elif self._survey_mode and row is not None:
            # Survey mode: pass complete row data with question_id
            for i, review in enumerate(reviews):
                if i < len(row) and 'question_id' in row.iloc[i]:
                    question_id = row.iloc[i]['question_id']
                    rv = review.strip()[:200] if len(review) > 200 else review.strip()
                    question += f"* {question_id} - {rv}\n"
                else:
                    rv = review.strip()[:200] if len(review) > 200 else review.strip()
                    question += f"* {rv}\n"
        else:
            # Review mode or fallback: reviews is a list of individual reviews
            for review in reviews:
                rv = review.strip()[:200] if len(review) > 200 else review.strip()
                question += f"* {rv}\n"
        
        return question

    async def run(self):
        self._result = await self.bot_evaluation()
        self._print_data_(self._result, 'CustomerSatisfaction')
        return self._result

    async def close(self):
        pass
