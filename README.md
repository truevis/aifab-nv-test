# AI Chatbot via NVIDIA NIM

*Sponsored by [aifab.xyz](https://aifab.xyz)*

A Streamlit chatbot that lets you choose from several LLMs and chat via the [NVIDIA NIM API](https://build.nvidia.com/).

## Features

- **Streamlit interface**: Simple chat UI with conversation history.
- **Model selection**: Pick from multiple models in the sidebar (MiniMax, Qwen, Kimi, GLM, DeepSeek, Llama, and more).
- **NVIDIA NIM integration**: Uses the NVIDIA API (`https://integrate.api.nvidia.com/v1`) with your API key from Streamlit secrets.
- **Streaming responses**: Tokens stream in for a responsive feel.
- **Session state**: Conversation context is preserved until you clear the chat.

## Supported models

These models are available in the app sidebar:

| Model ID | Notes |
| --- | --- |
| `minimaxai/minimax-m3` | Default selection |
| `qwen/qwen3.5-397b-a17b` | |
| `moonshotai/kimi-k2.6` | Use this instead of `kimi-k2.5` (404 on NIM) |
| `z-ai/glm-5.1` | |
| `deepseek-ai/deepseek-v4-flash` | |
| `deepseek-ai/deepseek-v4-pro` | |
| `meta/llama-3.1-70b-instruct` | |

Model availability can change on NVIDIA NIM. Run `test_models.py` to verify which models respond.

## File structure

- `app.py` — Main Streamlit chat application.
- `test_models.py` — Smoke-test script that calls each model and writes a report.
- `model_test_results.md` — Generated report from the last test run (timing and sample responses).
- `.streamlit/secrets.toml` — Your NVIDIA API key (keep out of version control).
- `.streamlit/config.toml` — Streamlit theme and UI settings.
- `requirements.txt` — Python dependencies.

## Setup

1. **Get an API key** from [NVIDIA Build](https://build.nvidia.com/) (NVIDIA NGC integrate API).

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**:
   - Create `.streamlit/secrets.toml` in the project root.
   - Add:

     ```toml
     NVIDIA_API_KEY = "your-nvidia-api-key-here"
     ```

## Usage

**Run the chat app:**

```bash
streamlit run app.py
```

Use the sidebar to select a model and **Clear Chat** to reset the conversation.

**Test all models:**

```bash
python test_models.py
```

This sends a fixed prompt to each model (60s timeout per model) and saves results to `model_test_results.md`.

## References

- [NVIDIA NIM API](https://integrate.api.nvidia.com/v1)
- [Streamlit documentation](https://docs.streamlit.io/)
