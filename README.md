# Daily Planner Agent

A weather-aware daily planning assistant built with Streamlit and LangChain. Enter a city to generate a practical day plan informed by current weather, or ask follow-up questions in the chat.

## Features

- Generate a suggested morning, afternoon, and evening schedule.
- Retrieve current conditions for a city through WeatherStack.
- Get clothing, transport, and weather-precaution suggestions.
- Ask follow-up questions through a Streamlit chat interface.
- Preview weather separately and clear the conversation when needed.

The weather integration currently retrieves **current conditions**, not a forecast. Plans should not be treated as forecast-based unless a forecast endpoint is added.

## Technology Stack

| Area                            | Technology                             | Use                                                                                  |
| ------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------ |
| Language                        | Python                                 | Application and agent implementation                                                 |
| User interface                  | Streamlit                              | Planner page, chat, city input, and weather preview                                  |
| Agent framework                 | LangChain                              | Agent construction and tool integration                                              |
| Language model                  | `ChatPerplexity` with `openai/gpt-5.5` | Generates plans and responses through the configured Perplexity integration          |
| Weather data                    | WeatherStack API                       | Current weather lookup by city                                                       |
| HTTP client                     | Requests                               | Calls the WeatherStack endpoint                                                      |
| Configuration                   | `python-dotenv`                        | Loads API keys from a local `.env` file                                              |
| TLS certificates                | Certifi                                | Sets the certificate bundle path for outbound TLS connections                        |
| Search integration (not active) | Tavily / `langchain-tavily`            | A search tool is initialized in `agent.py`, but is not currently passed to the agent |

## Requirements

- Python 3.10 or newer is recommended.
- A Perplexity API key.
- A WeatherStack API key for weather-aware planning.
- Internet access to reach the model provider and WeatherStack.

## Setup

From the `dailyPlanner` directory, create and activate a virtual environment, then install the project dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create a `.env` file in `dailyPlanner` with the credentials below:

```dotenv
PERPLEXITY_API_KEY=your_perplexity_api_key
WEATHER_STACK_API_KEY=your_weatherstack_api_key
TAVILY_API_KEY=your_tavily_api_key
```

`TAVILY_API_KEY` is not currently needed by the active agent flow. The app can display an error from the weather tool if `WEATHER_STACK_API_KEY` is missing; a valid Perplexity key is required when `agent.py` is imported.

Start the app from `dailyPlanner`:

```powershell
streamlit run app.py
```

Streamlit prints the local URL in the terminal, usually `http://localhost:8501`.

## Using the App

1. Set the city in the sidebar. It defaults to Nairobi.
2. Select **Generate today's plan** for a structured plan, or enter a question in the chat.
3. Select **Refresh weather** to display current conditions in the weather panel.
4. Select **Clear conversation** to reset the chat and weather preview.

The planner prompt asks the model to use the weather tool and avoid inventing weather details. As with any language-model output, verify important travel or safety decisions against a trusted source.

## Project Structure

```text
dailyPlanner/
├── agent.py          # Model setup, weather tool, and LangChain agent
├── app.py            # Streamlit interface and session state
├── README.md         # Project documentation
└── requirements.txt  # Python dependencies
```

## Configuration and Implementation Notes

- The app caches the constructed agent with Streamlit's `st.cache_resource`.
- Chat messages are held in Streamlit session state. Each request currently invokes the agent with only the newest prompt, so prior turns are displayed but are not sent as conversation history to the model.
- The WeatherStack request currently uses an HTTP URL. Use HTTPS where supported by the WeatherStack plan and service configuration.
- The repository has a second, root-level `requirements.txt`; use the `dailyPlanner/requirements.txt` when setting up this app. Keep dependency manifests aligned as the project evolves.

## Potential Improvements

### Reliability and correctness

- Add a forecast endpoint and date/time-aware planning; current conditions alone cannot reliably determine the best weather window later in the day.
- Pass conversation history into the agent so follow-up questions can refer to previous answers, or clearly present the chat as stateless.
- Validate and normalize city input, handle ambiguous city names, and provide user-friendly handling for timeouts, rate limits, invalid credentials, and unavailable results.
- Return structured weather data (including units and observation time) from the tool, then render it consistently in the UI.
- Add tests for weather responses, API failures, agent instructions, and Streamlit-facing behavior using mocked external requests.

### Security and privacy

- Use HTTPS for weather requests where available and keep API keys out of source control. Add `.env` to `.gitignore` and provide a `.env.example` containing placeholders only.
- Avoid displaying raw exception text to users; log diagnostic details separately and show a concise, actionable message.
- Review provider data-retention and privacy settings before sending user prompts to external model or search services.

### Dependencies and maintainability

- Add direct dependencies used by the source to `dailyPlanner/requirements.txt`, including `langchain-tavily` and `certifi`, and pin or lock versions for reproducible installs.
- Remove Tavily setup and its environment variable if web search is not part of the product, or pass the search tool to the agent and document when it should be used.
- Consolidate duplicated model construction and centralize configuration validation so startup errors are clear and consistent.
- Add automated linting, formatting, and tests to a CI workflow.

### Product experience

- Let users choose planning preferences such as work hours, priorities, mobility, and indoor/outdoor preference.
- Show the location, units, and “last updated” time for weather data; support Celsius/Fahrenheit and user time zones.
- Add loading and retry states, accessible labels, and a way to export or copy a generated plan.
- Make the default city configurable rather than hard-coded to Nairobi.

## DEMO

https://langchain-csyj.onrender.com

## Troubleshooting

- **Missing `PERPLEXITY_API_KEY`:** Add it to `dailyPlanner/.env` and restart Streamlit.
- **Weather key missing or lookup fails:** Check `WEATHER_STACK_API_KEY`, the city spelling, network access, and your WeatherStack account limits.
- **Dependency import error:** Install from `dailyPlanner/requirements.txt`; ensure the active virtual environment is selected. Some imports in the current source are not listed in that requirements file, as noted under Potential Improvements.
- **Model or provider error:** Confirm your Perplexity key, account access to the configured model, and the installed `langchain-perplexity` compatibility.

## For Education Purposes only
