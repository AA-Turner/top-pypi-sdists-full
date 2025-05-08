import asyncio
from typing import Any, Dict, List, Optional

import yaml
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field

from crewai.agent import Agent
from crewai.flow.flow import Flow, listen, start


class Product(BaseModel):
    product_name: str = Field(description="The product being analyzed")
    country: str = Field(description="The country being analyzed")


# Define a structured output format
class MarketAnalysis(BaseModel):
    key_trends: List[str] = Field(description="List of identified market trends")
    market_size: str = Field(description="Estimated market size")
    competitors: List[str] = Field(description="Major competitors in the space")
    product: Product = Field(description="The product being analyzed")


# Define flow state
class MarketResearchState(BaseModel):
    products: List[str] = Field(default=[], description="The products being analyzed")
    analysis: MarketAnalysis | None = None


# Create a flow class
class MarketResearchFlow(Flow[MarketResearchState]):
    @start()
    def initialize_research(self) -> Dict[str, Any]:
        print(f"Starting market research for {self.state.products}")
        return {"products": self.state.products}

    @listen(initialize_research)
    async def analyze_market(self) -> Dict[str, Any]:
        # Create an Agent for market research
        analyst = Agent(
            role="Market Analyst",
            goal="Analyze the market for the given product",
            backstory="You are a market analyst with a deep understanding of the market",
            tools=[SerperDevTool()],
        )

        # Assume self.state.product is a list of product names/descriptions to search
        # If it's a single product, wrap it in a list: products_to_search = [self.state.product]
        products_to_search = self.state.products
        if isinstance(products_to_search, str):
            products_to_search = [products_to_search]

        # Create tasks for concurrent execution
        tasks = []
        for product_name in products_to_search:
            query = f"""
            Research the market for {product_name}. Include:
            1. Key market trends
            2. Market size
            3. Major competitors

            Format your response according to the specified structure.
            """
            tasks.append(
                asyncio.create_task(
                    analyst.kickoff_async(query, response_format=MarketAnalysis)
                )
            )

        # Execute tasks concurrently and gather results
        all_results = await asyncio.gather(*tasks)
        print("all_results", all_results)

        print("all_results", all_results)
        if all_results and all_results[0].pydantic:  # Check if list is not empty
            print("result pydantic", all_results[0].pydantic)
        elif all_results:
            print("result", all_results[0])

        # Return the analysis to update the state (handling multiple results might be needed)
        # Returning only the first result for now, adjust as needed.
        return {"analysis": all_results[0].pydantic if all_results else None}

    @listen(analyze_market)
    def present_results(self, analysis) -> None:
        print("\nMarket Analysis Results")
        print("=====================")

        if isinstance(analysis, dict):
            # If we got a dict with 'analysis' key, extract the actual analysis object
            market_analysis = analysis.get("analysis")
        else:
            market_analysis = analysis

        if market_analysis and isinstance(market_analysis, MarketAnalysis):
            print("\nKey Market Trends:")
            for trend in market_analysis.key_trends:
                print(f"- {trend}")

            print(f"\nMarket Size: {market_analysis.market_size}")

            print("\nMajor Competitors:")
            for competitor in market_analysis.competitors:
                print(f"- {competitor}")
        else:
            print("No structured analysis data available.")
            print("Raw analysis:", analysis)


# Usage example
async def run_flow():
    flow = MarketResearchFlow()
    # flow.plot()
    result = await flow.kickoff_async(
        inputs={"products": ["apple iphone 16", "nvidia nims"]}
    )
    return result


# Run the flow
if __name__ == "__main__":
    # Use asyncio.run at the top level only
    # asyncio.run(run_flow())
    asyncio.run(run_flow())
