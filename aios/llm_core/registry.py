from cerebrum.llm.providers.api.anthropic import ClaudeLLM
from cerebrum.llm.providers.api.google import GeminiLLM
from cerebrum.llm.providers.api.openai import GPTLLM

from hexel.llm_core.cores.api.google import GeminiLLM
from hexel.llm_core.cores.api.openai import GPTLLM


MODEL_REGISTRY = {
    # Gemini
    "gemini-1.5-flash": GeminiLLM,
    "gemini-1.5-pro": GeminiLLM,

    # GPT
    'gpt-3.5-turbo': GPTLLM,
    'gpt-4-turbo': GPTLLM,
    'gpt-4o': GPTLLM,
    'gpt-4o-2024-05-13': GPTLLM,
    'gpt-4o-mini': GPTLLM,
}