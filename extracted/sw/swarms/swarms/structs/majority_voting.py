import concurrent.futures
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, List, Optional

from swarms.structs.agent import Agent
from swarms.structs.conversation import Conversation
from swarms.structs.multi_agent_exec import run_agents_concurrently
from swarms.structs.swarm_id import swarm_id
from swarms.utils.formatter import formatter
from swarms.utils.loguru_logger import initialize_logger
from swarms.utils.output_types import OutputType

logger = initialize_logger(log_folder="majority_voting")


class MajorityVoting:
    """
    A multi-loop majority voting system for agents that enables iterative consensus building.

    This system allows agents to run multiple loops where each subsequent loop considers
    the previous consensus, enabling agents to refine their responses and build towards
    a more robust final consensus. The system maintains conversation history across
    all loops and provides methods to analyze the evolution of consensus over time.

    Key Features:
    - Multi-loop consensus building with configurable loop count
    - Agent memory retention across loops
    - Comprehensive consensus history tracking
    - Flexible output formats (string, dict, list)
    - Loop-by-loop analysis capabilities
    """

    def __init__(
        self,
        id: str = swarm_id(),
        name: str = "MajorityVoting",
        description: str = "A multi-loop majority voting system for agents",
        agents: List[Agent] = None,
        consensus_agent: Optional[Agent] = None,
        autosave: bool = False,
        verbose: bool = False,
        max_loops: int = 1,
        output_type: OutputType = "dict",
        *args,
        **kwargs,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.agents = agents
        self.consensus_agent = consensus_agent
        self.autosave = autosave
        self.verbose = verbose
        self.max_loops = max_loops
        self.output_type = output_type

        self.conversation = Conversation(
            time_enabled=False, *args, **kwargs
        )

        self.initialize_majority_voting()

    def initialize_majority_voting(self):

        if self.agents is None:
            raise ValueError("Agents list is empty")

        # Log the agents
        formatter.print_panel(
            f"Initializing majority voting system\nNumber of agents: {len(self.agents)}\nAgents: {', '.join(agent.agent_name for agent in self.agents)}",
            title="Majority Voting",
        )

        if self.consensus_agent is None:
            # if no consensus agent is provided, use the last agent
            self.consensus_agent = self.agents[-1]

    def run(self, task: str, *args, **kwargs) -> List[Any]:
        """
        Runs the majority voting system with multi-loop functionality and returns the majority vote.

        Args:
            task (str): The task to be performed by the agents.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: The majority vote.

        """
        initial_task = task

        for loop_num in range(self.max_loops):
            if self.verbose:
                logger.info(
                    f"Starting loop {loop_num + 1}/{self.max_loops}"
                )

            # For subsequent loops, include previous consensus in the task
            if loop_num > 0:
                # Get the last consensus message from the conversation history
                history = (
                    self.conversation.return_messages_as_dictionary()
                )
                if history:
                    previous_consensus = history[
                        -1
                    ]  # Get the last message
                    task = f"""{initial_task}

                    Previous consensus from loop {loop_num}:
                    {previous_consensus['content']}

                    Please refine your response based on this previous consensus and provide an updated analysis."""
                else:
                    task = initial_task

            # Run agents concurrently on the current task
            results = run_agents_concurrently(
                self.agents, task, max_workers=os.cpu_count()
            )

            # Add responses to conversation and log them
            for agent, response in zip(self.agents, results):
                response = (
                    response
                    if isinstance(response, list)
                    else [response]
                )
                self.conversation.add(
                    f"{agent.agent_name}_loop_{loop_num + 1}",
                    response,
                )

            # Generate consensus prompt with full conversation history
            responses = self.conversation.return_history_as_string()

            prompt = f"""Conduct a detailed majority voting analysis on the following conversation from loop {loop_num + 1}:
            {responses}

            Between the following agents: {[agent.agent_name for agent in self.agents]}

            Please:
            1. Identify the most common answer/recommendation across all agents in this loop
            2. Analyze any major disparities or contrasting viewpoints between agents
            3. Highlight key areas of consensus and disagreement
            4. Evaluate the strength of the majority opinion
            5. Note any unique insights from minority viewpoints
            6. Compare with previous loops if applicable and note any evolution in consensus
            7. Provide a final synthesized recommendation based on the current majority consensus

            Focus on finding clear patterns while being mindful of important nuances in the responses.
            """

            # Generate consensus using the designated consensus agent
            if self.consensus_agent is not None:
                majority_vote = self.consensus_agent.run(prompt)
                consensus_name = self.consensus_agent.agent_name
            else:
                # Use the last agent as consensus agent
                majority_vote = self.agents[-1].run(prompt)
                consensus_name = self.agents[-1].agent_name

            # Add consensus to conversation with loop identifier
            self.conversation.add(
                f"{consensus_name}_consensus_loop_{loop_num + 1}",
                majority_vote,
            )

            if self.verbose:
                logger.info(
                    f"Completed loop {loop_num + 1}/{self.max_loops}"
                )

        # Return the final result based on output type
        if self.output_type == "str":
            return self.conversation.get_str()
        elif self.output_type == "dict":
            return self.conversation.return_messages_as_dictionary()
        elif self.output_type == "list":
            return self.conversation.return_messages_as_list()
        else:
            return self.conversation.return_history_as_string()

    def batch_run(
        self, tasks: List[str], *args, **kwargs
    ) -> List[Any]:
        """
        Runs the majority voting system in batch mode.

        Args:
            tasks (List[str]): List of tasks to be performed by the agents.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: List of majority votes for each task.
        """
        return [self.run(task, *args, **kwargs) for task in tasks]

    def run_concurrently(
        self, tasks: List[str], *args, **kwargs
    ) -> List[Any]:
        """
        Runs the majority voting system concurrently.

        Args:
            tasks (List[str]): List of tasks to be performed by the agents.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            List[Any]: List of majority votes for each task.
        """
        with ThreadPoolExecutor(
            max_workers=os.cpu_count()
        ) as executor:
            futures = [
                executor.submit(self.run, task, *args, **kwargs)
                for task in tasks
            ]
            return [
                future.result()
                for future in concurrent.futures.as_completed(futures)
            ]

    def get_consensus_history(self) -> List[dict]:
        """
        Get the history of all consensus decisions across loops.

        Returns:
            List[dict]: List of consensus messages from each loop
        """
        history = self.conversation.return_messages_as_dictionary()
        consensus_messages = []

        for message in history:
            if "consensus_loop" in message.get("role", ""):
                consensus_messages.append(message)

        return consensus_messages

    def get_final_consensus(self) -> Optional[dict]:
        """
        Get the final consensus from the last loop.

        Returns:
            Optional[dict]: The final consensus message, or None if no consensus exists
        """
        consensus_history = self.get_consensus_history()
        return consensus_history[-1] if consensus_history else None

    def get_loop_summary(self, loop_num: int) -> dict:
        """
        Get a summary of a specific loop including all agent responses and consensus.

        Args:
            loop_num (int): The loop number to summarize (1-indexed)

        Returns:
            dict: Summary containing agent responses and consensus for the specified loop
        """
        history = self.conversation.return_messages_as_dictionary()
        loop_messages = []

        for message in history:
            role = message.get("role", "")
            if f"loop_{loop_num}" in role:
                loop_messages.append(message)

        return {
            "loop_number": loop_num,
            "messages": loop_messages,
            "agent_count": len(
                [
                    m
                    for m in loop_messages
                    if f"_loop_{loop_num}" in m["role"]
                    and "consensus" not in m["role"]
                ]
            ),
            "consensus": next(
                (
                    m
                    for m in loop_messages
                    if "consensus" in m["role"]
                ),
                None,
            ),
        }

    def reset_conversation(self):
        """
        Reset the conversation history while keeping the same configuration.
        """
        self.conversation = Conversation(
            time_enabled=self.conversation.time_enabled,
            autosave=self.conversation.autosave,
            context_length=self.conversation.context_length,
            *self.conversation.__dict__.get("args", []),
            **self.conversation.__dict__.get("kwargs", {}),
        )

    def run_with_custom_loops(
        self, task: str, num_loops: int, *args, **kwargs
    ) -> List[Any]:
        """
        Run the majority voting system with a custom number of loops,
        overriding the default max_loops setting.

        Args:
            task (str): The task to be performed by the agents
            num_loops (int): Number of loops to run
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            List[Any]: The final result after specified number of loops
        """
        original_max_loops = self.max_loops
        self.max_loops = num_loops
        try:
            result = self.run(task, *args, **kwargs)
            return result
        finally:
            self.max_loops = original_max_loops
