# Kimi 2.5 Chatbot via NVIDIA NIM

*Sponsored by [aifab.xyz](https://aifab.xyz)*

A simple Streamlit chatbot application using the `moonshotai/kimi-k2.5` language model, accessed via the NVIDIA NIM API.

## Features

- **Streamlit Interface**: Clean and easy-to-use chat interface.
- **NVIDIA NIM Integration**: Uses the NVIDIA API (`https://integrate.api.nvidia.com/v1`) to securely communicate with the Kimi 2.5 model.
- **Streaming Responses**: Real-time streaming of response tokens for a low-latency feel.
- **Session State**: Remembers the context of the conversation using Streamlit session state.

## File Structure

- `app.py`: The main Streamlit application script containing UI logic and API calls.
- `.streamlit/secrets.toml`: The configuration file containing your private API key (make sure this is in your `.gitignore`).

## Usage & Configuration

Ensure you have a valid NVIDIA API Key via the NVIDIA NGC integrate API. You can get one at <https://build.nvidia.com/>.

To configure your API key for Streamlit:
1. Create a directory named `.streamlit` in the root of the project.
2. Inside that directory, create a file named `secrets.toml`.
3. Add your NVIDIA API key to `.streamlit/secrets.toml` like this:
   ```toml
   NVIDIA_API_KEY = "your-nvidia-api-key-here"
   ```

See [Streamlit documentation](https://docs.streamlit.io/) for further details on installation and usage.
