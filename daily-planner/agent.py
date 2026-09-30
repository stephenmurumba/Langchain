# Daily Planner

import os
import certifi
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_perplexity import ChatPerplexity
from langchain_tavily import TavilySearch
import requests

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv(override=True)

api_key = os.getenv("PERPLEXITY_API_KEY", "").strip()

tavily_key = os.getenv("TAVILY_API_KEY")

access_key=os.getenv("WEATHER_STACK_API_KEY", "").strip()

if not api_key:
    raise ValueError("PERPLEXITY_API_KEY is missing from .env")

search_tool = TavilySearch(max_results=3)

@tool
def get_weather_data(city: str) -> str:
    """Fetch current weather for a city."""
    if not access_key:
        return "WeatherStack API key is missing."

    url = "http://api.weatherstack.com/current"
    response = requests.get(
        url,
        params={"access_key": access_key, "query": city},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if "error" in data:
        return f"Weather lookup failed: {data['error'].get('info', 'Unknown API error')}"

    current = data.get("current")
    if not current:
        return f"No current weather data found for {city}."

    description = ", ".join(current.get("weather_descriptions", []))
    return (
        f"Weather in {city}: {description}; "
        f"temperature {current.get('temperature')}°C."
        f"humidity {current.get('humidity')}."
    )


llm = ChatPerplexity(
    model='openai/gpt-5.5',
    use_responses_api=True,
    timeout=60,
    api_key=api_key # type: ignore
)

""" agent = create_agent(
    model=llm,
    tools=[search_tool, get_weather_data],
    system_prompt=("Find the capital of Kenya. Using the weather data plan the day accordingly.")

) """

def create_daily_planner_agent():
    """Create and return the Daily Planner agent."""
    
    llm = ChatPerplexity(
        model="openai/gpt-5.5",
        use_responses_api=True,
        timeout=60,
        api_key=api_key # type: ignore
    )

    return create_agent(
        model=llm,
        tools=[get_weather_data],
        system_prompt="""
You are a practical, concise Daily Planner assistant.

Your job:
1. When the user provides a city, call get_weather_data for that city.
2. Use the reported conditions to create a useful plan for today.
3. Include recommended timing for outdoor activities, clothing guidance,
   transport or rain precautions when relevant, and a short priority list.
4. Never invent weather information. If the weather tool fails, clearly say so.
5. Format plans with readable Markdown headings and bullet points.
6. If the user does not provide a city, ask them for one.

The user may be in Kenya, so use East Africa Time where appropriate, but
do not assume a location unless the user specifies it.
""",
    )


""" response = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content":(
                'Daily weather forecast'
                'Create a daily planner for the foerecast'
            )
        }
    ]
})
print(response['messages'][-1].content) """
