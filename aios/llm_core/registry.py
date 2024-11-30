from hexel.llm_core.cores.api.google import GeminiLLM
from hexel.llm_core.cores.api.openai import GPTLLM
from hexel.llm_core.cores.api.anthropic import ClaudeLLM
from hexel.llm_core.cores.api.groq import GroqLLM
from hexel.llm_core.cores.local.hf import HfNativeLLM
from hexel.llm_core.cores.local.vllm import vLLM
from hexel.llm_core.cores.local.ollama import OllamaLLM

BACKEND_REGISTRY = {
    'openai': GPTLLM,
    'google': GeminiLLM,
    'huggingface': HfNativeLLM,
    'groq': GroqLLM,
    'vllm': vLLM,
    'ollama': OllamaLLM,
    'anthropic': ClaudeLLM
}

MODEL_PREFIX_MAP = {
    'gpt': 'openai',
    'gemini': 'google',
    'claude': 'anthropic',
    'mixtral': 'groq',
    'llama': 'huggingface',
    'ollama': 'ollama'
}