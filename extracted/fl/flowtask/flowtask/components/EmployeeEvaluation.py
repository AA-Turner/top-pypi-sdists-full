from collections.abc import Callable
import asyncio
from typing import Any
import pandas as pd
# Bot Infraestructure:
from parrot.bots.basic import BasicBot
from .flow import FlowComponent
from ..exceptions import ComponentError, ConfigError

class EmployeeEvaluation(FlowComponent):
    """
    EmployeeEvaluation

    Overview

        The EmployeeEvaluation class is a component for interacting with an IA Agent evaluating Users chats.
    :widths: auto

        | output_column    |   Yes    | Column for saving the Customer Satisfaction information.                                         |
    Return

        A Pandas Dataframe with the EmployeeEvaluation statistics.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          EmployeeEvaluation:
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

        self._bot_name = kwargs.get('bot_name', 'EmployeeBot')
        # TaskStorage
        # Find in the taskstorage, the "prompts" directory.
        prompt_path = self._taskstore.path.joinpath(self._program, 'prompts')
        if not prompt_path.exists():
            raise ConfigError(
                f"{self.system_prompt} Prompts Path Not Found: {prompt_path}"
            )
        self.prompt_path = prompt_path
        # System Prompt:
        # is hardcoded to this particular Bot.
        self.system_prompt_file = 'employee.txt'
        # Bot Object:
        self._bot: Any = None

    async def start(self, **kwargs):
        """
            start

            Overview

                The start method is a method for starting the EmployeeEvaluation component.

            Return

                True if the EmployeeEvaluation component started successfully.

        """
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "EmployeeBot: Data Was Not Found"
            )
        if not self.output_column:
            raise ConfigError(
                "Employee Evaluation: output_column is required"
            )
        # check if Prompt File exists
        prompt_file = self.prompt_path.joinpath(self.system_prompt_file)
        if not prompt_file.exists():
            raise ConfigError(
                f"{self.system_prompt} Prompt File Not Found: {prompt_file}"
            )
        self.system_prompt_file = prompt_file.name
        # read the prompt file as text:
        with open(prompt_file, 'r') as f:
            self.system_prompt = f.read()
        # Set the Bot:
        try:
            self._bot = BasicBot(
                name=self._bot_name,
                system_prompt=self.system_prompt,
                goal="Employee Evaluation using chat messages",
                use_llm=self.llm.get('name', 'name'),
                model_name=self.llm.get('model_name', 'gemini-1.5-pro'),
            )
            # configure the bot:
            await self._bot.configure()
        except Exception as err:
            raise ComponentError(
                f"{self.system_prompt} Error Configuring Bot: {err}"
            ) from err
        return True

    def generate_prompt(self, df, sender_name, messages):
        # Filter the dataframe for the given `sender_name`
        employee_df = df[df['sender_name'] == sender_name].copy()

        # Extract the relevant statistics
        positive_count = employee_df['Positive_Count'].values[0]
        negative_count = employee_df['Negative_Count'].values[0]
        avg_message_length = employee_df['Avg_Message_Length'].values[0]
        percentage_of_messages = employee_df['Percentage_of_Messages'].values[0]
        rank_by_message_count = employee_df['Rank_by_Message_Count'].values[0]
        message_count = employee_df['Message_Count'].values[0]

        # # Extract the chat messages
        # chat_messages = ""
        # for chat in messages:
        #     chat_messages += f"* {chat}\n"

        # Extract the chat messages
        chat_messages = employee_df['text'].values[0]

        # Define the prompt for Gemini Pro
        prompt = f"""
        Please analyze the chat messages and provide insights and useful information about the employee's behavior,
        including their mood, feelings, and most relevant chat messages.

        Use the following statistics to support your analysis:
        - Positive_Count: {positive_count}
        - Negative_Count: {negative_count}
        - Avg_Message_Length: {avg_message_length}
        - Percentage_of_Messages: {percentage_of_messages}
        - Rank_by_Message_Count: {rank_by_message_count}
        - Message_Count: {message_count}

        Chat messages: {chat_messages}
        """

        return prompt

    async def run(self):
        """
            run

            Overview

                The run method is a method for running the CustomerSatisfaction component.

            Return

                A Pandas Dataframe with the Customer Satisfaction statistics.

        """
        # Create the summary statistics about employees conversations:
        # Aggregate the data by `sender_name` and count the number of messages
        message_counts = self.data.groupby('sender_name')['text'].count().reset_index(name='Message_Count')
        # Calculate the total number of messages sent by each employee
        total_messages = message_counts['Message_Count'].sum()
        # Calculate the percentage of messages sent by each employee
        message_counts['Percentage_of_Messages'] = (message_counts['Message_Count'] / total_messages) * 100
        # Rank the employees based on the number of messages sent
        message_counts['Rank_by_Message_Count'] = message_counts['Message_Count'].rank(ascending=False)
        # combine message_counts into self.data dataframe:
        self.data = self.data.merge(message_counts, on='sender_name')
        # Group the data by `sender_name` and calculate the average message length
        avg_message_length = self.data.groupby('sender_name')['text'].apply(
            lambda x: x.str.len().mean()
        ).reset_index(name='Avg_Message_Length')
        # combine avg_message_length into self.data dataframe:
        self.data = self.data.merge(avg_message_length, on='sender_name')

        # Filter for negative emotions and sentiments
        negative_interactions = self.data[
            self.data['predicted_emotion'].isin(['anger', 'disgust', 'fear', 'sadness']) | (self.data['predicted_sentiment'] == 'Negative')  # noqa
        ]

        # Group by `sender_name` and count the number of negative messages
        negative_counts = negative_interactions.groupby('sender_name').size().reset_index(name='Negative_Count')

        # Sort the results in descending order
        negative_counts = negative_counts.sort_values(by='Negative_Count', ascending=False)

        # Filter for positive emotions and sentiments
        positive_interactions = self.data[
            self.data['predicted_emotion'].isin(['joy'])
            | (self.data['predicted_sentiment'] == 'Positive')
        ]

        # Group by `sender_name` and count the number of positive messages
        positive_counts = positive_interactions.groupby('sender_name').size().reset_index(name='Positive_Count')

        # Sort the results in descending order
        positive_counts = positive_counts.sort_values(by='Positive_Count', ascending=False)

        # Merge the negative and positive counts to self.data:
        self.data = self.data.merge(negative_counts, on='sender_name', how='left')
        self.data = self.data.merge(positive_counts, on='sender_name', how='left')
        # Fill NaN values with 0
        self.data = self.data.fillna(0)

        columns = [
            "sender_name",
            'Positive_Count',
            'Negative_Count',
            'Avg_Message_Length',
            'Percentage_of_Messages',
            'Rank_by_Message_Count',
            'Message_Count'
        ]
        # Group by all created columns + sender name, and convert to a list the "text" column.
        grouped = self.data.groupby(columns)['text'].apply(list).reset_index()
        employee_evaluation = {}
        for _, row in grouped.iterrows():
            employee = row['sender_name']
            texts = row['text']
            formatted_question = self.generate_prompt(grouped, employee, texts)
            result = await self._bot.question(
                question=formatted_question,
                return_docs=False
            )
            employee_evaluation[employee] = {
                "answer": result.answer
            }
        # Join "grouped" dataset with employee evaluation based on sender_name
        grouped[self.output_column] = grouped['sender_name'].map(
            lambda x: employee_evaluation[x]['answer']
        )
        # return the grouped dataframe
        self._result = grouped
        return self._result

    async def close(self):
        pass
