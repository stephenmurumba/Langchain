import streamlit as st

from agent import create_daily_planner_agent, get_weather_data

st.set_page_config(
    page_title="Daily Planner Agent",
    page_icon="🗓️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .planner-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .planner-subtitle {
            color: #6b7280;
            margin-bottom: 1.5rem;
        }

        div[data-testid="stSidebar"] {
            border-right: 1px solid #e5e7eb;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "city" not in st.session_state:
    st.session_state.city = "Nairobi"

if "latest_weather" not in st.session_state:
    st.session_state.latest_weather = None


@st.cache_resource
def get_agent():
    return create_daily_planner_agent()


def run_agent(prompt: str):
    """Send the user message to the LangChain agent and return its response."""
    agent = get_agent()

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
    )

    return result["messages"][-1].content


def add_message(role: str, content: str):
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


with st.sidebar:
    st.header("Planner settings")

    city = st.text_input(
        "City",
        value=st.session_state.city,
        placeholder="e.g. Nairobi",
    )

    st.session_state.city = city.strip() or "Nairobi"

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.latest_weather = None
        st.rerun()

    # st.caption(
    #     ""
    # )


st.markdown('<div class="planner-title">🗓️ Daily Planner</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="planner-subtitle">'
    "A weather-aware assistant for planning your day."
    "</div>",
    unsafe_allow_html=True,
)

left_column, right_column = st.columns([2, 1], gap="large")

with left_column:
    st.subheader(f"Plan for {st.session_state.city}")

    if st.button("✨ Generate today’s plan", type="primary", use_container_width=True):
        prompt = (
            f"Create a detailed but practical daily plan for today in "
            f"{st.session_state.city}. Check the weather first using the weather tool. "
            f"Include suggested morning, afternoon, and evening activities, "
            f"clothing advice, and any weather precautions."
        )

        add_message("user", f"Generate my daily plan for {st.session_state.city}.")

        with st.spinner("Checking weather and building your plan..."):
            try:
                answer = run_agent(prompt)
                add_message("assistant", answer)
            except Exception as exc:
                add_message(
                    "assistant",
                    f"Sorry, I could not generate the plan. Error: `{exc}`",
                )

        st.rerun()

    st.divider()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input(
        f"Ask about your day in {st.session_state.city}...",
        key="planner_chat_input",
    )

    if user_prompt:
        add_message("user", user_prompt)

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Planning..."):
                try:
                    full_prompt = (
                        f"The user's active city is {st.session_state.city}. "
                        f"User request: {user_prompt}"
                    )
                    answer = run_agent(full_prompt)
                    st.markdown(answer)
                    add_message("assistant", answer)
                except Exception as exc:
                    error_message = f"Sorry, something went wrong: `{exc}`"
                    st.error(error_message)
                    add_message("assistant", error_message)


with right_column:
    st.subheader("Current weather")

    if st.button("🌦️ Refresh weather", use_container_width=True):
        with st.spinner("Fetching weather..."):
            st.session_state.latest_weather = get_weather_data.invoke(
                {"city": st.session_state.city}
            )

    if st.session_state.latest_weather:
        st.info(st.session_state.latest_weather)
    else:
        st.caption(
            "Click “Refresh weather” to preview current conditions, or generate "
            "a plan and the agent will retrieve them automatically."
        )

    st.divider()

    st.subheader("Try asking")
    st.caption(
        "• What should I wear today?\n\n"
        "• Give me an outdoor-friendly afternoon plan.\n\n"
        "• Move errands to the best weather window.\n\n"
        "• Make a focused work schedule around the forecast."
    )