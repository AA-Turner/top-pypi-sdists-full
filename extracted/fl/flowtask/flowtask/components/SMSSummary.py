from typing import List
from collections.abc import Callable
import asyncio
import json
import pandas as pd
from pydantic import BaseModel, Field
from .CallSummary import CallSummary, SentimentItem, EmotionCount


class SMSAnalysisSummary(BaseModel):
    sentiment_distribution: List[SentimentItem] = Field(
        description="Percentage distribution of sentiments"
    )
    most_frequent_sentiment: str = Field(
        description="The most common sentiment across all SMS conversations"
    )
    top_emotions: List[EmotionCount] = Field(
        description="Top emotions with occurrence counts"
    )
    common_key_topics: list[str] = Field(
        description="Recurring topics across SMS conversations"
    )
    brief_notes_summary: str = Field(
        description="Synthesized summary of all brief notes"
    )
    consolidated_recommendations: list[str] = Field(
        description="4-6 prioritized actionable recommendations"
    )
    engagement_summary: str = Field(
        description="Summary of engagement levels across conversations"
    )
    intent_distribution: str = Field(
        description="Distribution of conversation intents"
    )
    outcome_distribution: str = Field(
        description="Distribution of conversation outcomes"
    )
    avg_response_time_minutes: float = Field(
        description="Average response time in minutes across conversations"
    )
    response_time_interpretation: str = Field(
        description="Explanation of what the response time metric indicates"
    )
    follow_up_rate: float = Field(
        description="Percentage of conversations that recommend follow-up (0.0 to 1.0)"
    )


class SMSSummary(CallSummary):
    """
    SMSSummary.

    Overview

        The SMSSummary class is a component for interacting with an IA Agent
        for making SMS Conversation Summarization per agent per day.
        It extends the CallSummary class and adapts it for SMS analysis data.

    .. code-block:: yaml

        SMSSummary:
          eval_column: extracted_analysis
          date_column: summary_date
          output_column: sms_summary
          summary_column: sms_summarization
          llm:
            llm: google
            model: gemini-2.5-pro
            temperature: 0.1
            max_tokens: 8192

    |---|---|---|
    | version | No | version of component |
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
        self._goal: str = 'Your task is to provide a concise and insightful analysis of SMS Conversations'
        self.system_prompt_file: str = 'sms_summary.txt'
        prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')
        self._prompt_file = prompt_path.joinpath(self.system_prompt_file)
        self.skip_existing: bool = kwargs.get('skip_existing', False)

    def format_question(self, extension, owner_name, summary_day, analysis):
        question = f"""
        Agent Extension: {extension}
        Agent Name: {owner_name}
        Date: {summary_day}

        SMS Conversation Analysis:
        """
        for a in analysis:
            rv = json.dumps(a, indent=2)
            question += f"* {rv}\n"
        return question

    async def bot_evaluation(self):
        """
        bot_evaluation

        Overview

            Iterates each row (agent+date), makes two LLM calls per row:
            1. Generate markdown report -> output_column
            2. Generate structured JSON via Pydantic -> summary_column

        Return

            A Pandas Dataframe with the IA-based statistics.
        """
        if self.output_column not in self.data.columns:
            self.data[self.output_column] = None
        if self.summary_column not in self.data.columns:
            self.data[self.summary_column] = None
        skipped_count = 0
        for idx, row in self.data.iterrows():
            # Skip rows where both outputs already exist (from AddDataset join)
            if self.skip_existing:
                existing_out = row.get(self.output_column)
                existing_sum = row.get(self.summary_column)
                if (
                    existing_out is not None and not pd.isna(existing_out) and str(existing_out).strip() != ''
                    and existing_sum is not None and not pd.isna(existing_sum) and str(existing_sum).strip() != ''
                ):
                    skipped_count += 1
                    continue
            owner_name = row['owner_name']
            extension = row['extension']
            summary_day = row[self.date_column]
            analysis = row[self._eval_column]
            if isinstance(analysis, list):
                for session in analysis:
                    if isinstance(session, dict):
                        session_id = session.get('session_id', 'unknown')
                        if session.get('sentiment') is None and session.get('message_stats') is None:
                            self.logger.warning(
                                f"Session {session_id} (ext={extension}, date={summary_day}) "
                                f"has null analysis fields — possible corrupt or double-encoded "
                                f"JSON in flexroc.sms_analysis"
                            )
            formatted_question = self.format_question(
                extension, owner_name, summary_day, analysis
            )
            # First summary: text/markdown summary
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
            # Second summary: structured summary via Pydantic
            try:
                result = await self._bot.invoke(
                    question=formatted_question,
                    response_model=SMSAnalysisSummary,
                    use_conversation_history=False,
                )
                output = result.output
                if isinstance(output, str):
                    try:
                        output = json.loads(output.replace('\n', ''))
                    except json.JSONDecodeError:
                        pass
                if isinstance(output, SMSAnalysisSummary):
                    output = output.model_dump(
                        by_alias=False,
                        exclude_none=True,
                    )
                if isinstance(output, (dict, list)):
                    output = json.dumps(output, ensure_ascii=False)
                self.data.at[idx, self.summary_column] = output
            except Exception as e:
                self.logger.error(f"Error during second summary generation: {e}")
                self.data.at[idx, self.summary_column] = None
                continue
        if skipped_count:
            self.logger.info(
                f"SMSSummary: skipped {skipped_count} already-summarized rows"
            )
        return self.data
