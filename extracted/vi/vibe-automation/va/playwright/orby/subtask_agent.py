import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple
from playwright.async_api import Page
import requests

from .utils import extract_content_by_tags, simple_prompt_to_messages
from .actions import execute_action, get_action_hints
from .template import Template


async def perform_task(page: Page, goal: str, max_steps=20):
    """Perform a task with the given Playwright page"""
    agent = SubtaskAgent(
        model="sft-experiment-6-demo",
        goal=goal,
        current_screenshot=await page.screenshot(),
    )

    # Track action history for updates
    action_trace = []

    # Main agent loop
    num_steps = 0
    while num_steps < max_steps:
        num_steps += 1

        # Get action from agent
        action, _ = agent.act()
        print("Agent returned action: ", action)

        # Execute the action using the unified browser_actions module
        done, result = await execute_action(page, action)
        if done:
            return

        # Always update agent with new screenshot and action trace
        new_screenshot = await page.screenshot()
        action_trace.append((action, ""))  # Add action with no error
        agent.update(screenshot=new_screenshot, trace=action_trace)

    raise RuntimeError(f"Agent did not finish the task within {max_steps} steps.")


@dataclass
class RewardModelResponse:
    """The response from the reward model"""

    should_end: bool
    goal_achieved: bool
    answer: str
    reasoning: str


class OrbyModelClient:
    """Simple OpenAI-compatible client for making API calls."""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = "http://model.internal.orby.ai/v1",
        model: str = "sft-experiment-6-demo",
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def generate(self, messages: List[Dict], **kwargs) -> str:
        """Generate a response using the OpenAI-compatible API."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 512),
            "temperature": kwargs.get("temperature", 0.0),
        }

        response = requests.post(
            f"{self.base_url}/chat/completions", json=payload, headers=headers
        )
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]


class SubtaskAgent:
    """Minimal agent for browser automation with vision-based navigation."""

    def __init__(
        self,
        goal: str,
        current_screenshot: bytes,
        model: str,
        base_url: str = "http://model.internal.orby.ai/v1",
        api_key: str = None,
        reward_model: str = None,
    ):
        """
        Initialize the OrbyAgent.

        Args:
            api_key: API key if needed (or set OPENAI_API_KEY env var)
            base_url: API base URL (default: internal Orby endpoint)
            model: Model name for executor (default: sft-experiment-6-demo)
            reward_model: Model name for reward model (default: same as executor)
        """
        self.model = OrbyModelClient(api_key=api_key, base_url=base_url, model=model)

        # Set up reward model - use same model if not specified
        if reward_model:
            self.reward_model = OrbyModelClient(
                api_key=api_key, base_url=base_url, model=reward_model
            )
        else:
            self.reward_model = self.model

        # Get action hints from browser_actions module
        self.action_hints = get_action_hints()

        # Load default prompt template from sva_v3
        self.prompt_template = Template(
            os.path.join(os.path.dirname(__file__), "20250508.jinja2")
        )

        # State management
        self.goal = goal
        self.screenshot_history = [current_screenshot]
        self.action_history = []
        self.llm_trace = []

    def update(self, screenshot: bytes, trace: List[Tuple[str, str]]):
        """
        Update agent state with new observation.

        Args:
            screenshot: New screenshot as bytes
            trace: List of (action, error) tuples
        """
        self.screenshot_history.append(screenshot)
        if trace:
            # Update action history with the trace - always add new actions to show progression
            self.action_history = trace.copy()  # Replace with the full trace

    def act(self, **kwargs) -> Tuple[str, Dict]:
        """
        Generate the next action using two-stage approach: reward model then executor.

        Returns:
            Tuple of (action_string, metadata_dict)
        """
        # Prepare history string with screenshots
        history_parts = []
        for i, (action, error) in enumerate(self.action_history):
            # Add screenshot reference
            history_parts.append(f"<image:screenshot_{i}>")
            # Add thinking and action
            history_parts.append(f"<thinking>\nPrevious action {i + 1}\n</thinking>")
            history_parts.append(f"<action>\n{action}\n</action>")
            if error:
                history_parts.append(f"Error: {error}")
        history_str = "\n".join(history_parts) if history_parts else ""

        # Prepare template variables - must include current_screenshot
        template_vars = {
            "goal": self.goal,
            "action_hints": self.action_hints,
            "history": history_str,
            "current_screenshot": self.screenshot_history[-1]
            if self.screenshot_history
            else None,
        }

        # Add historical screenshots to template vars
        for i, screenshot in enumerate(self.screenshot_history[:-1]):
            template_vars[f"screenshot_{i}"] = screenshot

        # Stage 1: Use reward model to determine if we should end the task
        reward_model_prompt, reward_images = self.prompt_template.render(
            block="reward_model", **template_vars
        )
        reward_model_messages = simple_prompt_to_messages(
            reward_model_prompt, images=reward_images
        )
        reward_model_response = self.reward_model.generate(
            messages=reward_model_messages, **kwargs
        )

        # Parse reward model response
        reward_response = self._parse_reward_model_response(reward_model_response)

        # Record reward model in trace
        self.llm_trace.append(
            {
                "type": "reward_model",
                "messages": reward_model_messages,
                "response": reward_model_response,
            }
        )

        if reward_response.should_end:
            # Task should end - create completion action
            if reward_response.goal_achieved:
                action = f'complete(answer="{reward_response.answer}")'
            else:
                action = f'complete(infeasible_reason="{reward_response.reasoning}")'

            return action, {
                "reward_model_response": reward_model_response,
                "should_end": True,
                "goal_achieved": reward_response.goal_achieved,
            }

        # Stage 2: Use executor model to generate next action
        executor_prompt, executor_images = self.prompt_template.render(
            block="executor", **template_vars
        )
        executor_messages = simple_prompt_to_messages(
            executor_prompt, images=executor_images
        )
        executor_response = self.model.generate(messages=executor_messages, **kwargs)

        # Record executor in trace
        self.llm_trace.append(
            {
                "type": "executor",
                "messages": executor_messages,
                "response": executor_response,
            }
        )

        # Extract action from executor response
        action = self._extract_action(executor_response)

        return action, {
            "reward_model_response": reward_model_response,
            "executor_response": executor_response,
            "should_end": False,
        }

    def _extract_action(self, response: str) -> str:
        """
        Extract action from model response.

        Args:
            response: Model response string

        Returns:
            Extracted action string
        """
        # Try to extract from <action> tags
        action_match = re.search(r"<action>(.*?)</action>", response, re.DOTALL)
        if action_match:
            return action_match.group(1).strip()

        # Fallback: look for function call pattern
        func_match = re.search(r"(\w+)\([^)]*\)", response)
        if func_match:
            return func_match.group(0)

        return ""

    def _parse_reward_model_response(
        self, reward_model_response: str
    ) -> RewardModelResponse:
        """
        Parse the reward model response to determine if task should end.

        Args:
            reward_model_response: The response from the reward model

        Returns:
            RewardModelResponse with parsed values
        """
        # Extract content using tags
        contents = extract_content_by_tags(
            reward_model_response,
            ["should_end", "goal_achieved", "answer", "reasoning"],
        )

        # Parse should_end
        if contents.get("should_end") is not None:
            should_end = contents["should_end"].strip().lower() == "true"
        else:
            should_end = False

        # Parse goal_achieved
        if contents.get("goal_achieved") is not None:
            goal_achieved = contents["goal_achieved"].strip().lower() == "true"
        else:
            goal_achieved = False

        # Parse answer
        if contents.get("answer") is not None:
            answer = contents["answer"].strip()
        else:
            answer = ""

        # Parse reasoning
        if contents.get("reasoning") is not None:
            reasoning = contents["reasoning"].strip().replace("\n", " ")
        else:
            reasoning = ""

        return RewardModelResponse(should_end, goal_achieved, answer, reasoning)
