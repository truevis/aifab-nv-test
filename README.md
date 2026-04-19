# Kimi 2.5 Chatbot via NVIDIA NIM

*Sponsored by [aifab.xyz](https://aifab.xyz)*

A simple, elegant Streamlit chatbot application powered by the `moonshotai/kimi-k2.5` language model, accessed via the NVIDIA NIM API.

## Features

- **Streamlit Interface**: Clean and easy-to-use chat interface.
- **NVIDIA NIM Integration**: Uses the NVIDIA API (`https://integrate.api.nvidia.com/v1`) to securely communicate with the Kimi 2.5 model.
- **Streaming Responses**: Real-time streaming of response tokens for a low-latency feel.
- **Session State**: Remembers the context of the conversation using Streamlit session state.

## File Structure

- `app.py`: The main Streamlit application script containing UI logic and API calls.
- `.streamlit/secrets.toml`: The configuration file containing your private API key (make sure this is in your `.gitignore`).

## Usage Note

Ensure you have a valid NVIDIA API Key with access to the Kimi 2.5 model via the NVIDIA NGC integrate API. <https://build.nvidia.com/>
