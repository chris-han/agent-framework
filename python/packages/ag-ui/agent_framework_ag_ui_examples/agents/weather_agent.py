# Copyright (c) Microsoft. All rights reserved.

"""Weather agent example demonstrating backend tool rendering."""

import logging
from typing import Any

from agent_framework import ChatAgent, ChatClientProtocol, ai_function

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@ai_function
def get_weather(location: str) -> dict[str, Any]:
    """Get the current weather for a location.

    Args:
        location: The city or location to get weather for.

    Returns:
        Weather information as a dictionary with temperatures in Celsius.
    """
    logger.info(f"[get_weather] Called with location: {location}")
    logger.debug(f"[get_weather] Location type: {type(location)}")

    # Simulated weather data with structured format (temperatures in Celsius for dojo UI)
    weather_data = {
        "seattle": {"temperature": 11, "conditions": "rainy", "humidity": 75, "wind_speed": 12, "feels_like": 10},
        "san francisco": {"temperature": 14, "conditions": "foggy", "humidity": 85, "wind_speed": 8, "feels_like": 13},
        "new york city": {"temperature": 18, "conditions": "sunny", "humidity": 60, "wind_speed": 10, "feels_like": 17},
        "miami": {"temperature": 29, "conditions": "hot and humid", "humidity": 90, "wind_speed": 5, "feels_like": 32},
        "chicago": {"temperature": 9, "conditions": "windy", "humidity": 65, "wind_speed": 20, "feels_like": 6},
    }

    location_lower = location.lower()
    logger.debug(f"[get_weather] Normalized location: {location_lower}")
    logger.debug(f"[get_weather] Available locations: {list(weather_data.keys())}")

    if location_lower in weather_data:
        result = weather_data[location_lower]
        logger.info(f"[get_weather] Found weather data for {location_lower}: {result}")
        return result

    result = {
        "temperature": 21,
        "conditions": "partly cloudy",
        "humidity": 50,
        "wind_speed": 10,
        "feels_like": 20,
    }
    logger.info(f"[get_weather] Using default weather data for {location_lower}: {result}")
    return result


@ai_function
def get_forecast(location: str, days: int = 3) -> str:
    """Get the weather forecast for a location.

    Args:
        location: The city or location to get forecast for.
        days: Number of days to forecast (default: 3).

    Returns:
        Forecast information string.
    """
    logger.info(f"[get_forecast] Called with location: {location}, days: {days}")
    logger.debug(f"[get_forecast] Location type: {type(location)}, days type: {type(days)}")

    forecast: list[str] = []
    for day in range(1, min(days, 7) + 1):
        forecast.append(f"Day {day}: Partly cloudy, {60 + day * 2}°F")

    result = f"{days}-day forecast for {location}:\n" + "\n".join(forecast)
    logger.info(f"[get_forecast] Generated forecast: {result}")
    return result


def weather_agent(chat_client: ChatClientProtocol) -> ChatAgent:
    """Create a weather agent with get_weather and get_forecast tools.

    Args:
        chat_client: The chat client to use for the agent

    Returns:
        A configured ChatAgent instance with weather tools
    """
    logger.info("[weather_agent] Creating weather agent")
    logger.debug(f"[weather_agent] Chat client type: {type(chat_client)}")
    logger.debug(f"[weather_agent] Available tools: {[get_weather, get_forecast]}")

    agent = ChatAgent(
        name="weather_agent",
        instructions=(
            "You are a helpful weather assistant. "
            "Use the get_weather and get_forecast functions to help users with weather information. "
            "Always provide friendly and informative responses."
        ),
        chat_client=chat_client,
        tools=[get_weather, get_forecast],
    )

    logger.info("[weather_agent] Weather agent created successfully")
    return agent
