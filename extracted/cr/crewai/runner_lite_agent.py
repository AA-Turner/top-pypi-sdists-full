from typing import List

from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

from crewai import Agent


class MarketAnalysis(BaseModel):
    key_trends: List[str] = Field(description="List of identified market trends")
    market_size: str = Field(description="Estimated market size")
    competitors: List[str] = Field(description="Major competitors in the space")


agent = Agent(
    role="Market Research Analyst",
    goal="Analyze the market for the given product. Use the SerperDevTool to find information.",
    backstory="You are an experienced market analyst with expertise in identifying market trends and opportunities.",
    tools=[SerperDevTool()],
    # knowledge_sources=[
    #     KnowledgeSource(
    #         name="Market Research",
    #         description="Market research data for the given product",
    #         data="",
    #     )
    # ],
)

result = agent.kickoff(
    # messages="Analyze the market for apple products",
    messages=[{"role": "user", "content": "Analyze the market for apple products"}],
    response_format=MarketAnalysis,
)
print("result", result.pydantic)
