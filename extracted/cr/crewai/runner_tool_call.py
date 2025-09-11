import os

from crewai_tools import CrewaiEnterpriseTools

from crewai import Agent, Crew, Task

action_tools = CrewaiEnterpriseTools(
    enterprise_token=os.environ["ENTERPRISE_TOKEN"],
)

agent = Agent(
    role="A helpful assistant",
    goal="You are a helpful assistant that can answer questions and help with tasks.",
    backstory="You are a helpful assistant that can answer questions and help with tasks.",
    # tools=[SerperDevTool()],
    tools=action_tools,
)
task = Task(
    description="Send a slack message to lorenze jay saying: {message}",
    expected_output="The slack message sent to lorenze jay",
    agent=agent,
)
# task = Task(
#     description="Research topic based on: {message}",
#     expected_output="The research topic",
#     agent=agent,
# )

crew = Crew(agents=[agent], tasks=[task], tracing=True)
crew.kickoff(inputs={"message": "Hello, Lorenze Jay!"})
