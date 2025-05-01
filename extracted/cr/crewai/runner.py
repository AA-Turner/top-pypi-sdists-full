import json
import os
from typing import List

from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from crewai.agent import Agent
from crewai.agents.agent_adapters.langgraph.langgraph_adapter import (
    LangGraphAgentAdapter,
)
from crewai.agents.agent_adapters.openai_agents.openai_adapter import OpenAIAgentAdapter
from src.crewai import Crew, Task

# Agents Defined
code_helper_agent = OpenAIAgentAdapter(
    role="Code Helper",
    goal="Help users solve coding problems effectively and provide clear explanations.",
    backstory="You are an experienced programmer with deep knowledge across multiple programming languages and frameworks. You specialize in solving complex coding challenges and explaining solutions clearly.",
    allow_delegation=False,
    verbose=True,
    llm="gpt-4o",
)
link_finder_agent = OpenAIAgentAdapter(
    role="Link Finder",
    goal="Find the most relevant and high-quality resources for coding tasks.",
    backstory="You are a research specialist with a talent for finding the most helpful resources. You're skilled at using search tools to discover documentation, tutorials, and examples that directly address the user's coding needs.",
    tools=[SerperDevTool()],
    allow_delegation=False,
    verbose=True,
)

# Create a LangGraph-based agent
reporter_agent = LangGraphAgentAdapter(
    role="Reporter",
    goal="Report the results of the tasks.",
    backstory="You are a reporter who reports the results of the other tasks",
    llm=ChatOpenAI(model="gpt-4o"),
    allow_delegation=True,
    verbose=True,
)


class Code(BaseModel):
    code: str


task = Task(
    description="Give an answer to the coding question: {task}",
    expected_output="just the code for the task {task}",
    agent=code_helper_agent,  # openai agent
    output_pydantic=Code,
)
task2 = Task(
    description="Find links to resources that can help with coding tasks. Use the serper tool to find resources that can help.",
    expected_output="A list of links to resources that can help with coding tasks",
    agent=link_finder_agent,
)


class Report(BaseModel):
    code: str
    links: List[str]


task3 = Task(
    description="Report the results of the tasks.",
    expected_output="A report of the results of the tasks. this is the code produced and then the links to the resources that can help with the coding task.",
    agent=reporter_agent,
    output_pydantic=Report,
)
# Use in CrewAI
crew = Crew(
    agents=[code_helper_agent, link_finder_agent, reporter_agent],
    tasks=[task, task2, task3],
    verbose=True,
)

result = crew.kickoff(
    inputs={"task": "How do you implement an abstract class in python?"}
)

# Print raw result first
print("Raw result:", result)
print("Raw result type:", type(result))
print("pydantic:", result.pydantic)

# Handle result based on its type
if hasattr(result, "json_dict") and result.json_dict:
    json_result = result.json_dict
    print("\nStructured JSON result:")
    print(f"{json.dumps(json_result, indent=2)}")

    # Access fields safely
    if isinstance(json_result, dict):
        if "code" in json_result:
            print("\nCode:")
            print(
                json_result["code"][:200] + "..."
                if len(json_result["code"]) > 200
                else json_result["code"]
            )

        if "links" in json_result:
            print("\nLinks:")
            for link in json_result["links"][:5]:  # Print first 5 links
                print(f"- {link}")
            if len(json_result["links"]) > 5:
                print(f"...and {len(json_result['links']) - 5} more links")
elif hasattr(result, "pydantic") and result.pydantic:
    print("\nPydantic model result:")
    print(result.pydantic.model_dump_json(indent=2))
else:
    # Fallback to raw output
    print("\nNo structured result available, using raw output:")
    print(result.raw[:500] + "..." if len(result.raw) > 500 else result.raw)
