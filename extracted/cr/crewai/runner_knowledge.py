import os
from crewai_tools import SerperDevTool

from crewai import Agent, Crew, Task
from crewai.knowledge.knowledge_config import KnowledgeConfig
from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.llm import LLM

agent = Agent(
    role="Agent",
    goal="Agent goal",
    backstory="Agent backstory",
    knowledge_sources=[
        CrewDoclingSource(
            file_paths=[
                "https://arxiv.org/pdf/2503.23513",
            ],
        )
    ],
    knowledge_config=KnowledgeConfig(results_limit=10, score_threshold=0.5),
    llm=LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
)

task = Task(
    description="Your goal is to answer the question based on the knowledge sources: {task}",
    expected_output="Answer the question in 3 paragraphs. Find the most relevant information from the knowledge sources.",
    agent=agent,
)
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    # memory=True,
)
result = crew.kickoff(inputs={"task": "What is RARE’s core philosophy?"})
print(result)
print("usage metrics", result.token_usage)
