import os

from crewai_tools import SerperDevTool
from pydantic import BaseModel

from crewai.llm import LLM
from src.crewai import Agent, Crew, Task

models = {
    "llama32_11b_vision_instruct": "openai/Llama-3.2-11B-Vision-Instruct",
    "llama33_70b_instruct": "openai/Llama-3.3-70B-Instruct",
    "llama33_8b_instruct": "openai/Llama-3.3-8B-Instruct",
    "llama4_17b_instruct": "openai/Llama-4-Maverick-17B-128E-Instruct-FP8",
}

llama_llm = LLM(
    model=models["llama33_8b_instruct"],
    base_url="https://api.llama.com/compat/v1",
    api_key=os.getenv("LLAMA_API_KEY"),
)


# Agents
agent_coder = Agent(
    role="Agent Coder",
    goal="Help with coding task: {task}.",
    backstory="You are a helpful assistant that can help with coding tasks.",
    allow_delegation=False,
    verbose=True,
    llm=llama_llm,
)
agent_link_finder = Agent(
    role="Agent Link Finder",
    goal="Find links to resources that can help with coding tasks. Use the serper tool to find resources that can help.",
    backstory="You are a helpful assistant that can find links to resources that can help with coding tasks.",
    allow_delegation=False,
    verbose=True,
    llm=llama_llm,
    tools=[SerperDevTool()],
)
agent_reporter = Agent(
    role="Agent Reporter",
    goal="Report the results of the tasks.",
    backstory="You are a helpful assistant that can report the results of the tasks.",
    allow_delegation=False,
    verbose=True,
    llm=llama_llm,
)


class Code(BaseModel):
    code: str


task = Task(
    description="Give an answer to the coding question: {task}",
    expected_output="A thorough answer to the coding question: {task}",
    agent=agent_coder,
    output_json=Code,
)
task2 = Task(
    description="Find links to resources that can help with coding tasks. Use the serper tool to find resources that can help.",
    expected_output="A list of links to resources that can help with coding tasks",
    agent=agent_link_finder,
)
task3 = Task(
    description="Report the results of the tasks.",
    expected_output="A report of the results of the tasks. this is the code produced and then the links to the resources that can help with the coding task.",
    agent=agent_reporter,
)
# Use in CrewAI
crew = Crew(
    agents=[agent_coder, agent_link_finder, agent_reporter],
    tasks=[task, task2, task3],
    verbose=True,
    memory=True,
)

result = crew.kickoff(
    inputs={"task": "How do you implement an abstract class in python?"},
)
print("result", result)
