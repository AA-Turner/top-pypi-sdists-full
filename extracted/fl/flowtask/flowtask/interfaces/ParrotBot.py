from abc import abstractmethod
from pathlib import Path
from typing import Any, Optional
import aiofiles
from navconfig.logging import logging
from parrot.bots.basic import BasicBot
from ..exceptions import ConfigError, ComponentError
import re
import pandas as pd

class ParrotBot:
    """ParrotBot.

    Interface for creating new chatbots to be used directly as Flowtask Components

    """
    def __init__(self, *args, **kwargs):
        self._bot_name = kwargs.get('bot_name', 'ParrotBot')
        self._bot: Any = None
        self.llm = kwargs.get('llm', {})
        if isinstance(self.llm, str):
            self.llm = {'llm': self.llm}
        self._logger = logging.getLogger(f'Bot.{self._bot_name.lower()}')
        self._prompt_file = kwargs.get('prompt_file', 'prompt.txt')
        self._goal: str = kwargs.get('goal', 'Customer Satisfaction Analysis using Reviews')
        self._rating_column: str = kwargs.get('rating_column', 'rating')
        self._eval_column: str = kwargs.get('eval_column', 'evaluation')
        self._desc_column: str = kwargs.get('description_column', 'description')
        self.output_column: str = kwargs.get('output_column')
        # Survey mode flag - changes behavior for survey data vs review data
        self._survey_mode: bool = kwargs.get('survey', False)
        # System Prompt:
        self.system_prompt = "Customer Satisfaction: "
        super(ParrotBot, self).__init__(*args, **kwargs)
        # TaskStorage
        # Find in the taskstorage, the "prompts" directory.
        # prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')
        # if not prompt_path.exists():
        #     raise ConfigError(
        #         f"{self.system_prompt} Prompts Path Not Found: {prompt_path}"
        #     )
        # self.prompt_path = prompt_path
        # # is hardcoded to this particular Bot.
        # self.system_prompt_file = self._prompt_file
        # Bot Object:
        self._bot: Any = None

    async def get_prompt(self, prompt_file: Optional[Path] = None) -> str:
        """get_prompt

            Overview

                The get_prompt method is a method for getting the prompt for the ParrotBot component.

            Return

                The prompt for the ParrotBot component.

        """
        # check if Prompt File exists
        prompt_file = prompt_file or self.prompt_path.joinpath(self.system_prompt_file)
        if not prompt_file.exists():
            raise ConfigError(
                f"{self.system_prompt} Prompt File Not Found: {prompt_file}"
            )
        self.system_prompt_file = prompt_file.name
        # read the prompt file as text:
        prompt = ''
        async with aiofiles.open(prompt_file, 'r') as f:
            prompt = await f.read()
        return prompt

    async def start(self, **kwargs):
        """
            start

            Overview

                The start method is a method for starting the CustomerSatisfaction component.

            Parameters

                kwargs: dict
                    A dictionary containing the parameters for the CustomerSatisfaction component.

            Return

                True if the CustomerSatisfaction component started successfully.

        """
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                f"{self._bot_name.lower()}: Data Was Not Found"
            )
        if not self.output_column:
            raise ConfigError(
                f"{self._bot_name.lower()}: output_column is required"
            )

        # Initialize TaskStorage and prompt_path now that FlowComponent is initialized
        # Find in the taskstorage, the "prompts" directory.
        prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')
        if not prompt_path.exists():
            raise ConfigError(
                f"{self.system_prompt} Prompts Path Not Found: {prompt_path}"
            )
        self.prompt_path = prompt_path
        # is hardcoded to this particular Bot.
        self.system_prompt_file = self._prompt_file
        self.system_prompt = await self.get_prompt()

        # Set the Bot:
        try:
            # Extract all LLM configuration parameters
            bot_config = {
                'name': self._bot_name,
                'system_prompt': self.system_prompt,
                'goal': self._goal,
                'llm': self.llm.get('llm', 'google'),
                'model': self.llm.get('model', 'gemini-2.5-pro'),
            }

            # Add optional LLM parameters if they exist in config
            if 'temperature' in self.llm:
                bot_config['temperature'] = self.llm['temperature']
            if 'max_tokens' in self.llm:
                bot_config['max_tokens'] = self.llm['max_tokens']
            if 'top_p' in self.llm:
                bot_config['top_p'] = self.llm['top_p']
            if 'top_k' in self.llm:
                bot_config['top_k'] = self.llm['top_k']

            self._bot = BasicBot(**bot_config)
            # configure the bot:
            await self._bot.configure()
        except Exception as err:
            raise ComponentError(
                f"{self.system_prompt} Error Configuring Bot: {err}"
            ) from err
        return True

    @abstractmethod
    def format_question(self, obj_name, reviews, row=None):
        pass

    async def bot_evaluation(self):
        """
            bot_evaluation

            Overview

                The run method is a method for running the ParrotBot component.

            Return

                A Pandas Dataframe with the IA-based statistics.

        """
        # Group reviews by product_name and aggregate them into a list
        grouped = self.data.groupby(self._desc_column)[self._eval_column].apply(list).reset_index()
        _evaluation = {}
        for _, row in grouped.iterrows():
            product_name = row[self._desc_column]
            reviews = row[self._eval_column]
            if self._survey_mode:
                formatted_question = self.format_question(product_name, reviews, row)
            else:
                formatted_question = self.format_question(product_name, reviews)
            result = await self._bot.invoke(
                question=formatted_question,
            )
            _evaluation[product_name] = {
                "answer": result.output
            }
        # Then, create a dataframe only with the columns in "self.columns" grouped.
        if self._survey_mode:
            # Survey mode: count responses and no rating required
            grouped_df = self.data.groupby(self.columns).agg(
                num_responses=(self._eval_column, "count")
            ).reset_index()
        else:
            # Review mode: count reviews and calculate average rating
            grouped_df = self.data.groupby(self.columns).agg(
                num_reviews=(self._eval_column, "count"),
                avg_rating=(self._rating_column, "mean")
            ).reset_index()
        # Add the Customer Satisfaction column, using the dictionary and match per product_name column
        grouped_df[self.output_column] = grouped_df[self._desc_column].map(
            lambda x: _evaluation[x]['answer']
        )
        # Remove the starting ```json and ending ``` using a regex
        grouped_df[self.output_column] = grouped_df[self.output_column].str.replace(r'^```json\s*|\s*```$', '', regex=True)

        # Extract Weighted Score for survey mode (similar to avg_rating for reviews)
        if self._survey_mode:
            def extract_weighted_score(text):
                """Extract Weighted Score from the analysis text"""
                if pd.isna(text):
                    return None
                # Look for "Weighted Score: X.X" pattern
                match = re.search(r'Weighted Score:\s*([+-]?\d+\.?\d*)', str(text))
                if match:
                    try:
                        return float(match.group(1))
                    except (ValueError, TypeError):
                        return None
                return None

            grouped_df['weighted_score'] = grouped_df[self.output_column].apply(extract_weighted_score)
        # return the grouped dataframe
        return grouped_df

    async def run(self):
        self._result = await self.bot_evaluation()
        self._print_data_(self._result, ' :: AI Bot Evaluation ::')
        return self._result

    async def close(self):
        pass
