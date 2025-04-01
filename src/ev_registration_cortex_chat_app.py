import _snowflake
import json
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Function to send a message to Cortex Analyst API
def send_message(prompt: str) -> dict:
    """Calls the Cortex Analyst REST API and returns the response."""
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "semantic_model_file": "@SNF_EV_DATA_DEMO.EV_POPULATION_DATA.AZURE/ev registration data_semantic_model_202503312000.yaml",
    }
    resp = _snowflake.send_snow_api_request(
        "POST",
        "/api/v2/cortex/analyst/message",
        {},
        {},
        request_body,
        {},
        30000,
    )
    if resp["status"] < 400:
        return json.loads(resp["content"])
    else:
        raise Exception(f"Failed request with status {resp['status']}: {resp}")

# Function to process and display the message
def process_message(prompt: str) -> None:
    """Processes a user message and adds the response to the chat."""
    st.session_state.messages.append(
        {"role": "user", "content": [{"type": "text", "text": prompt}]}
    )
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = send_message(prompt=prompt)
            content = response["message"]["content"]
            display_content(content=content)
    st.session_state.messages.append({"role": "assistant", "content": content})

# Function to display response content
def display_content(content: list) -> None:
    """Displays the response content from Cortex Analyst."""
    for item in content:
        if item["type"] == "text":
            st.markdown(item["text"])
        elif item["type"] == "suggestions":
            with st.expander("Suggestions", expanded=True):
                for idx, suggestion in enumerate(item["suggestions"]):
                    if st.button(suggestion, key=f"suggestion_{idx}"):
                        process_message(suggestion)
        elif item["type"] == "sql":
            with st.expander("SQL Query", expanded=False):
                st.code(item["statement"], language="sql")
            with st.expander("Results", expanded=True):
                with st.spinner("Running SQL..."):
                    session = get_active_session()
                    df = session.sql(item["statement"]).to_pandas()
                    st.dataframe(df)

# Main chat interface
def main():
    st.title("EV Registration Chatbot")
    st.markdown("Ask questions about EV registration data powered by Snowflake Cortex Analyst.")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            display_content(content=message["content"])

    # Chat input
    if user_input := st.chat_input("Ask about EV registrations (e.g., 'How many EVs were registered in 2023?')"):
        process_message(prompt=user_input)

if __name__ == "__main__":
    main()