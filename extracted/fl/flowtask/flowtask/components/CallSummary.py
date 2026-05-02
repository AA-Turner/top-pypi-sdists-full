from typing import List
from collections.abc import Callable
import asyncio
import json
from ..interfaces.ParrotBot import ParrotBot
from .flow import FlowComponent
from pydantic import BaseModel, Field


class SentimentItem(BaseModel):
    """A model to replace dict[str, float] for sentiment distribution."""
    sentiment: str = Field(description="The name of the sentiment (e.g., 'Positive', 'Neutral')")
    percentage: float = Field(description="The percentage of this sentiment, from 0.0 to 1.0")

class EmotionCount(BaseModel):
    """A model to replace tuple[str, int] for top emotions."""
    emotion: str = Field(description="The identified emotion")
    count: int = Field(description="The number of occurrences of this emotion")

class CallAnalysisSummary(BaseModel):
    sentiment_distribution: List[SentimentItem] = Field(
        description="Percentage distribution of sentiments"
    )
    most_frequent_sentiment: str = Field(
        description="The most common sentiment across all calls"
    )
    top_emotions: List[EmotionCount] = Field(
        description="Top emotions with occurrence counts"
    )
    common_key_topics: list[str] = Field(
        description="Recurring topics across calls"
    )
    brief_notes_summary: str = Field(
        description="Synthesized summary of all brief notes"
    )
    consolidated_recommendations: list[str] = Field(
        description="4-6 prioritized actionable recommendations"
    )
    average_utterance_seconds: float = Field(
        description="Overall average utterance duration"
    )
    utterance_interpretation: str = Field(
        description="Explanation of what the utterance metric indicates"
    )

class CallSummary(ParrotBot, FlowComponent):
    """
    CallSummary.

    Overview

        The CallSummary class is a component for interacting with an IA Agent for making Call Summarization.
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
          CallSummary:
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
        self._goal: str = 'Your task is to provide a concise and insightful analysis of Call Transcripts'
        self.system_prompt_file: str = 'call_summary.txt'
        prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')
        self._prompt_file = prompt_path.joinpath(self.system_prompt_file)

    def format_question(self, caller_number, caller_name, calls_day, analysis):
        question = f"""
        Caller Number: {caller_number}
        Caller Name: {caller_name}
        Date: {calls_day}

        Call Analysis:
        """  # noqa
        for a in analysis:
            rv = json.dumps(a, indent=2)
            question += f"* {rv}\n"
        return question

    async def bot_evaluation(self):
        """
            bot_evaluation

            Overview

                The run method is a method for running the ParrotBot component.

            Return

                A Pandas Dataframe with the IA-based statistics.

        """
        self.data[self.output_column] = None
        self.data[self.summary_column] = None
        for idx, row in self.data.iterrows():
            caller_number = row['caller_number']
            caller_name = row['caller_name']
            calls_day = row[self.date_column]
            analysis = row['extracted_analysis']
            formatted_question = self.format_question(caller_number, caller_name, calls_day, analysis)
            # first summary, text summary:
            try:
                result = await self._bot.invoke(
                    question=formatted_question,
                    use_conversation_history=False,
                )
                self.data.at[idx, self.output_column] = result.output
            except Exception as e:
                self.logger.error(f"Error during first summary generation: {e}")
                self.data.at[idx, self.output_column] = None
                continue
            try:
                # Second Summary, structured summary:
                result = await self._bot.invoke(
                    question=formatted_question,
                    response_model=CallAnalysisSummary,
                    use_conversation_history=False,
                )
                output = result.output
                if isinstance(output, str):
                    # try to parse string as json, removing newlines
                    try:
                        output = json.loads(output.replace('\n', ''))
                    except json.JSONDecodeError:
                        pass
                if isinstance(output, CallAnalysisSummary):
                    output = output.model_dump(
                        by_alias=False,
                        exclude_none=True,
                    )
                self.data.at[idx, self.summary_column] = output
            except Exception as e:
                self.logger.error(f"Error during second summary generation: {e}")
                self.data.at[idx, self.summary_column] = None
                continue
        return self.data
