"""UzhavarNeri configuration and model resolution.

Supports:
- Amazon Bedrock (Nova Pro, Nova Lite, Claude)
- AWS User Group Madurai hosted cloud endpoint (Qwen3.5-4b)
- Local Ollama execution
"""

from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def get_llm_provider() -> str:
    return os.environ.get("LLM_PROVIDER", "ugmdu").lower().strip()


def get_agent_model():
    """Return an initialized model instance compatible with strands.Agent."""
    provider = get_llm_provider()

    if provider == "bedrock":
        from strands.models.bedrock import BedrockModel
        model_id = os.environ.get("BEDROCK_MODEL_ID", "us.amazon.nova-lite-v1:0")
        region = os.environ.get("AWS_REGION", "us-east-1")
        return BedrockModel(model_id=model_id, region_name=region)

    if provider == "local":
        from strands.models.ollama import OllamaModel
        url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")
        model_id = os.environ.get("LLM_MODEL_ID", "qwen3.5:4b")
        return OllamaModel(url, model_id=model_id)

    # Default to AWS User Group Madurai hosted cloud
    from strands.models.openai import OpenAIModel
    base_url = os.environ.get("UGMDU_BASE_URL", "https://da25tnxy06gjk.cloudfront.net/v1")
    key = os.environ.get("DECIDER_API_KEY", "dcd_live_nuWIZjnQNLG2WC6nyfDchTy9zbb0nZHAVwNm7tqCGY2QibAd")
    model_id = os.environ.get("LLM_MODEL_ID", "qwen3.5-4b")
    return OpenAIModel(
        client_args={"base_url": base_url, "api_key": key},
        model_id=model_id
    )
