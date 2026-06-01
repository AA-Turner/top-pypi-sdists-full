"""
Travel Agent Streaming Workflow Example

Demonstrates streaming tokens from durable agents with parallel execution.

This workflow:
1. Creates agents with web search capabilities
2. Runs parallel searches (weather + places) using Runner.run() in workflow
3. Streams tokens from each agent in real-time using Task API
4. Combines results into a travel plan
"""

import asyncio

from mistralai.client.models import TextChunk, WebSearchTool
from pydantic import BaseModel, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import workflow
from mistralai.workflows.core.task import Task

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger()


class AgentStreamState(BaseModel):
    """State for tracking agent streaming output."""

    text: str = Field(default="", description="Accumulated text from agent")


class WorkflowParams(BaseModel):
    city: str = Field(description="City to plan trip for")
    days: int = Field(description="Number of days for the trip")


class WorkflowOutput(BaseModel):
    response: str = Field(description="Complete trip plan")


@workflows.workflow.define(name="travel-agent-streaming-workflow")
class TravelAgentStreamingWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowOutput:
        """
        Execute travel planning workflow with parallel agent searches.

        Agents run INSIDE the workflow and stream tokens in real-time.
        """
        logger.info("Workflow: Starting travel agent workflow", city=params.city, days=params.days)

        # Use remote session for durable execution
        session = workflows_mistralai.RemoteSession(stream=True)

        # Create weather search agent
        logger.info("Workflow: Creating weather search agent")
        weather_agent = workflows_mistralai.Agent(
            description="Agent to search weather information",
            instructions="Use web search to find accurate, up-to-date weather forecasts. Be concise and factual.",
            name="weather-search-agent",
            tools=[WebSearchTool()],
        )

        # Create places search agent
        logger.info("Workflow: Creating places search agent")
        places_agent = workflows_mistralai.Agent(
            description="Agent to search for places to visit",
            instructions="Use web search to find popular tourist attractions and outdoor activities. Be specific.",
            name="places-search-agent",
            tools=[WebSearchTool()],
        )

        # Create planning agent
        logger.info("Workflow: Creating planning agent")
        planning_agent = workflows_mistralai.Agent(
            description="Travel planning agent",
            instructions=(
                "You are a helpful travel planner. Given weather forecasts and place recommendations, "
                "create a detailed, day-by-day itinerary that accounts for weather conditions. "
                "Be specific and practical."
            ),
            name="planning-agent",
        )

        # Run weather and places searches in parallel
        logger.info("Workflow: Starting parallel searches")

        weather_task = workflows_mistralai.Runner.run(
            agent=weather_agent,
            inputs=f"What is the weather forecast for {params.city} for the next {params.days} days?",
            session=session,
        )

        places_task = workflows_mistralai.Runner.run(
            agent=places_agent,
            inputs=f"What are the best outdoor places to visit in {params.city}?",
            session=session,
        )

        # Await both results
        weather_outputs, places_outputs = await asyncio.gather(weather_task, places_task)

        # Extract text from outputs and stream using Task API
        weather_text = ""
        async with Task[AgentStreamState](type="weather-search", state=AgentStreamState()) as weather_stream:
            for output in weather_outputs:
                if isinstance(output, TextChunk):
                    weather_text += output.text
                    await weather_stream.set_state(AgentStreamState(text=weather_text))

        places_text = ""
        async with Task[AgentStreamState](type="places-search", state=AgentStreamState()) as places_stream:
            for output in places_outputs:
                if isinstance(output, TextChunk):
                    places_text += output.text
                    await places_stream.set_state(AgentStreamState(text=places_text))

        logger.info("Workflow: Searches complete, starting planning")

        # Generate trip plan from search results
        planning_prompt = f"""Based on the following information, plan a trip:

Weather Information:
{weather_text}

Places to Visit:
{places_text}

Task: Plan a {params.days}-day trip to {params.city} that accounts for weather and recommended places.

Please provide a detailed day-by-day plan."""

        plan_outputs = await workflows_mistralai.Runner.run(
            agent=planning_agent,
            inputs=planning_prompt,
            session=session,
        )

        # Stream planning output using Task API
        plan_text = ""
        async with Task[AgentStreamState](type="trip-planning", state=AgentStreamState()) as plan_stream:
            for output in plan_outputs:
                if isinstance(output, TextChunk):
                    plan_text += output.text
                    await plan_stream.set_state(AgentStreamState(text=plan_text))

        logger.info("Workflow: Trip planning complete")
        return WorkflowOutput(response=plan_text)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([TravelAgentStreamingWorkflow]))
