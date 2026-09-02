"""Mock travel tools — retained for demo/test purposes.

All 6 functions return random/hardcoded data. These can be dropped
once real travel APIs are integrated, or kept as testing fixtures.
"""

from __future__ import annotations

import random
from typing import Any

from matrx_ai.tools.models import ToolContext, ToolResult


async def travel_get_location(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    cities = ["San Francisco", "New York", "Austin", "Seattle", "Miami"]
    return ToolResult(success=True, output={"city": random.choice(cities)})


async def travel_get_weather(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import TravelGetWeatherArgs
    TravelGetWeatherArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    city = args.get("city", "Unknown")
    conditions = ["sunny", "rainy", "cloudy", "snowy", "windy"]
    return ToolResult(
        success=True,
        output={
            "city": city,
            "condition": random.choice(conditions),
            "temperature": random.randint(45, 85),
            "unit": "fahrenheit",
        },
    )


async def travel_get_restaurants(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import TravelGetRestaurantsArgs
    TravelGetRestaurantsArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    city = args.get("city", "Unknown")
    cuisines = ["Italian", "Mexican", "Japanese", "American", "Thai", "French"]
    prefixes = ["The", "Chez", "Casa", "Mama"]
    suffixes = ["Bistro", "Kitchen", "Grill", "House"]
    restaurants = [
        f"{random.choice(prefixes)} {random.choice(cuisines)} {random.choice(suffixes)}"
        for _ in range(3)
    ]
    return ToolResult(success=True, output={"city": city, "restaurants": restaurants})


async def travel_get_activities(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import TravelGetActivitiesArgs
    TravelGetActivitiesArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    city = args.get("city", "Unknown")
    weather = args.get("weather", "sunny")

    indoor = [
        "Museum tour",
        "Art gallery visit",
        "Shopping mall",
        "Indoor climbing",
        "Aquarium",
    ]
    outdoor = [
        "Hiking trail",
        "Beach walk",
        "Park picnic",
        "Bike ride",
        "Outdoor market",
    ]

    activities = random.sample(
        indoor if weather.lower() in ("rainy", "snowy") else outdoor, 3
    )
    return ToolResult(
        success=True,
        output={"city": city, "weather": weather, "activities": activities},
    )


async def travel_get_events(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import TravelGetEventsArgs
    TravelGetEventsArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    city = args.get("city", "Unknown")
    weather = args.get("weather", "sunny")

    indoor = [
        "Jazz concert",
        "Theater performance",
        "Comedy show",
        "Food festival (indoor)",
        "Tech conference",
    ]
    outdoor = [
        "Street fair",
        "Outdoor concert",
        "Farmers market",
        "Food truck festival",
        "Sports game",
    ]

    events = random.sample(
        indoor if weather.lower() in ("rainy", "snowy") else outdoor, 2
    )
    return ToolResult(
        success=True, output={"city": city, "weather": weather, "events": events}
    )


async def travel_create_summary(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    from matrx_ai.tools._generated_declarations import TravelCreateSummaryArgs
    TravelCreateSummaryArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    location = args.get("location", "Unknown")
    weather_info = args.get("weather_info", {})
    restaurants = args.get("restaurants", [])
    activities = args.get("activities", [])
    events = args.get("events", [])

    condition = weather_info.get("condition", "N/A")
    temperature = weather_info.get("temperature", "N/A")

    summary = (
        f"LOCATION: {location}\n"
        f"WEATHER: {condition} at {temperature}°F\n\n"
        f"RESTAURANT RECOMMENDATIONS:\n"
        + "\n".join(f"  - {r}" for r in restaurants)
        + "\n\n"
        "ACTIVITIES:\n" + "\n".join(f"  - {a}" for a in activities) + "\n\n"
        "LOCAL EVENTS:\n" + "\n".join(f"  - {e}" for e in events)
    )
    return ToolResult(success=True, output={"summary": summary})
