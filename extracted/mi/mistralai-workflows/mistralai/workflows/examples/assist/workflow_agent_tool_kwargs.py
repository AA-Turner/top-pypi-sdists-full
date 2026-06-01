import asyncio
from typing import Any

from mistralai.client.models import TextChunk
from pydantic import BaseModel, ConfigDict, Field

import mistralai.workflows as workflows
import mistralai.workflows.plugins.mistralai as workflows_mistralai
from mistralai.workflows import workflow

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.get_logger(__name__)


class WorkflowParams(BaseModel):
    question: str = Field(..., description="Question for the agent")


class WorkflowResult(BaseModel):
    answer: str


class WeatherResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    city: str | None = None
    country: str | None = None
    temperature: int
    condition: str
    humidity: int | None = None


@workflows.activity()
async def get_weather_with_options(city: str, country: str, **kwargs: Any) -> WeatherResult:
    """Get weather for a city with optional extra parameters like units, language, etc."""
    logger.debug("get_weather_with_options called", city=city, country=country, kwargs=kwargs)
    return WeatherResult(
        city=city,
        country=country,
        temperature=22,
        condition="sunny",
        **kwargs,
    )


@workflows.activity()
async def get_weather_dynamic(**kwargs: Any) -> WeatherResult:
    """Get weather with fully dynamic parameters - accepts any location format."""
    logger.debug("get_weather_dynamic called", kwargs=kwargs)
    return WeatherResult(
        temperature=18,
        condition="cloudy",
        humidity=65,
        **kwargs,
    )


class WeatherRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country code (e.g., US, FR)")


@workflows.activity()
async def get_weather_extensible(params: WeatherRequest) -> WeatherResult:
    """Get weather using a typed model that accepts extra fields."""
    extras = params.model_extra or {}
    logger.debug("get_weather_extensible called", city=params.city, country=params.country, extras=extras)
    return WeatherResult(
        city=params.city,
        country=params.country,
        temperature=25,
        condition="partly cloudy",
        **extras,
    )


@workflows.activity()
async def get_weather_simple(city: str) -> WeatherResult:
    """Get weather for a city - simple single parameter."""
    logger.debug("get_weather_simple called", city=city)
    return WeatherResult(
        city=city,
        temperature=20,
        condition="clear",
        humidity=50,
    )


@workflows.workflow.define(name="case1_weather_with_kwargs")
class Case1WeatherWithKwargs:
    """Test Case 1: Weather activity with explicit params + **kwargs."""

    @workflows.workflow.entrypoint
    async def entrypoint(self, params: WorkflowParams) -> WorkflowResult:
        session = workflows_mistralai.RemoteSession()

        agent = workflows_mistralai.Agent(
            description="Weather assistant with flexible options",
            instructions=(
                "You are a weather assistant. When the user asks about weather, "
                "you MUST use the get_weather_with_options tool. "
                "Required parameters: city and country. "
                "You can also pass optional parameters like units='celsius' or 'fahrenheit', "
                "include_forecast=true, language='en', etc."
            ),
            name="weather-kwargs-agent",
            tools=[get_weather_with_options],
        )

        outputs = await workflows_mistralai.Runner.run(agent=agent, inputs=params.question, session=session)

        answer = "\n".join([o.text for o in outputs if isinstance(o, TextChunk)])
        return WorkflowResult(answer=answer)


@workflows.workflow.define(name="case2_weather_dynamic")
class Case2WeatherDynamic:
    """Test Case 2: Weather activity with only **kwargs."""

    @workflows.workflow.entrypoint
    async def entrypoint(self, params: WorkflowParams) -> WorkflowResult:
        session = workflows_mistralai.RemoteSession()

        agent = workflows_mistralai.Agent(
            description="Weather assistant with dynamic parameters",
            instructions=(
                "You are a weather assistant. When the user asks about weather, "
                "you MUST use the get_weather_dynamic tool. "
                "This tool accepts any parameters - you can pass location info in any format: "
                "city, country, latitude, longitude, zip_code, address, etc."
            ),
            name="weather-dynamic-agent",
            tools=[get_weather_dynamic],
        )

        outputs = await workflows_mistralai.Runner.run(agent=agent, inputs=params.question, session=session)

        answer = "\n".join([o.text for o in outputs if isinstance(o, TextChunk)])
        return WorkflowResult(answer=answer)


@workflows.workflow.define(name="case3_weather_extensible")
class Case3WeatherExtensible:
    """Test Case 3: Weather activity with BaseModel that has extra='allow'."""

    @workflows.workflow.entrypoint
    async def entrypoint(self, params: WorkflowParams) -> WorkflowResult:
        session = workflows_mistralai.RemoteSession()

        agent = workflows_mistralai.Agent(
            description="Weather assistant with extensible parameters",
            instructions=(
                "You are a weather assistant. When the user asks about weather, "
                "you MUST use the get_weather_extensible tool. "
                "Required: city and country. "
                "Optional: you can add extra fields like units, include_humidity, forecast_days, etc."
            ),
            name="weather-extensible-agent",
            tools=[get_weather_extensible],
        )

        outputs = await workflows_mistralai.Runner.run(agent=agent, inputs=params.question, session=session)

        answer = "\n".join([o.text for o in outputs if isinstance(o, TextChunk)])
        return WorkflowResult(answer=answer)


@workflows.workflow.define(name="case4_weather_simple")
class Case4WeatherSimple:
    """Test Case 4: Weather activity with simple primitive param (backward compat)."""

    @workflows.workflow.entrypoint
    async def entrypoint(self, params: WorkflowParams) -> WorkflowResult:
        session = workflows_mistralai.RemoteSession()

        agent = workflows_mistralai.Agent(
            description="Simple weather assistant",
            instructions=(
                "You are a weather assistant. When the user asks about weather, "
                "you MUST use the get_weather_simple tool with the city name."
            ),
            name="weather-simple-agent",
            tools=[get_weather_simple],
        )

        outputs = await workflows_mistralai.Runner.run(agent=agent, inputs=params.question, session=session)

        answer = "\n".join([o.text for o in outputs if isinstance(o, TextChunk)])
        return WorkflowResult(answer=answer)


# =============================================================================
# Main entry point
# =============================================================================

if __name__ == "__main__":
    asyncio.run(
        workflows.run_worker(
            [
                Case1WeatherWithKwargs,
                Case2WeatherDynamic,
                Case3WeatherExtensible,
                Case4WeatherSimple,
            ]
        )
    )
