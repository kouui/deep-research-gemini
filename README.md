# Deep Research + Gemini + Apify

this Deep Research implementation is based on the n8n workflow [host-your-own-ai-deep-research-agent-with-n8n-apify-and-openai-o3](https://n8n.io/workflows/2878-host-your-own-ai-deep-research-agent-with-n8n-apify-and-openai-o3/)

see [instructions](instructions/1.md) for more details.

## Installation

```bash
uv sync
```
## API KEY setup

in the `.env` file, add your apify api key like
```
APIFY_API_KEY=apify_api_***
```

in the `keys.json` file, add your multiple gemini api with key-value format.
```json
{
    "google-gemini-1": "AIzaSy***",
    "google-gemini-2": "AIzaSy***",
}
```

## Usage


streamlit as UI
```bash
uv run main.py
```

for testting agents without UI,
```bash
uv run tests/test_agents.py
``` 