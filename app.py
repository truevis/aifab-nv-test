import streamlit as st
from openai import OpenAI

# Page configuration
st.set_page_config(page_title="Kimi 2.5 Chat", page_icon="💬", layout="centered")

# Header
st.title("💬 Kimi 2.5 Chatbot")
st.write("Powered by `moonshotai/kimi-k2.5` via NVIDIA NIM")
st.caption("Accessing via *https://integrate.api.nvidia.com/v1*")

# Retrieve API Key from Streamlit Secrets
try:
    nvidia_api_key = st.secrets["NVIDIA_API_KEY"]
except KeyError:
    st.error("Error: `NVIDIA_API_KEY` could not be found in `.streamlit/secrets.toml`.")
    st.stop()

# Initialize OpenAI Client pointing to NVIDIA NIM endpoint
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar with clear chat button
with st.sidebar:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Render existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
if prompt := st.chat_input("What's on your mind?"):
    # Display the user's message
    st.chat_message("user").markdown(prompt)

    # Append user's message to the history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare API messages payload
    api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    model_name = "moonshotai/kimi-k2.5"

    # Spinner stays visible for the entire LLM call + streaming
    full_response = ""
    spinner_label = (
        f"Waiting for LLM response... "
        f"Model: `{model_name}"
    )
    with st.spinner(spinner_label):
        try:
            response_stream = client.chat.completions.create(
                model=model_name,
                messages=api_messages,
                stream=True,
            )
            for chunk in response_stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta_content = chunk.choices[0].delta.content
                    if delta_content is not None:
                        full_response += delta_content
        except Exception as e:
            st.error(f"An API error occurred: {e}")
            st.stop()

    # Display the completed response in the assistant chat bubble
    with st.chat_message("assistant"):
        st.markdown(full_response)

    # Store the final response in session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
