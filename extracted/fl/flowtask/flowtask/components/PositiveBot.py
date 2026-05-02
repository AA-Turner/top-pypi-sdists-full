from collections.abc import Callable
import asyncio
from ..interfaces.ParrotBot import ParrotBot
from .flow import FlowComponent


class PositiveBot(ParrotBot, FlowComponent):
    """
    PositiveBot.

    Overview

        The PositiveBot class is a component for interacting with an IA Agent for making Customer Satisfaction Analysis.
        It extends the FlowComponent class.

    :widths: auto

        | output_column    |   Yes    | Column for saving the Customer Satisfaction information.                                         |
    Return

        A Pandas Dataframe with the Customer Satisfaction statistics.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PositiveBot:
          # attributes here
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
        self._goal: str = 'Your task is to provide a concise and insightful analysis of positive reviews'

    def format_question(self, product_name, reviews):
        question = f"""
        Product: {product_name}

        Question:
        "What are the primary positive aspects, features, and customer sentiments based on these positive product reviews for {product_name}?"

        Positive Customer Reviews:

        """  # noqa
        for review in reviews:
            rv = review.strip() if len(review) < 200 else review[:200]
            question += f"* {rv}\n"
        return question

    async def run(self):
        self._result = await self.bot_evaluation()
        self._print_data_(self._result, 'PositiveBot')
        return self._result

    async def close(self):
        pass
