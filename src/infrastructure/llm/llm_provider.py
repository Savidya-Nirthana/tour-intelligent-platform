"""
Chat llm Providers - 3-model architecture

Three specialised models for three different tasks:
1. Routing - llama-3.1-8b-instant
2. Extraction - llama-3.1-8b-instant
3. Chat - gemini-2.5-flash

"""

from langchain_openai import ChatOpenAI
from typing import Optional, Any
from infrastructure.config import (
    ROUTER_MODEL,
    ROUTER_PROVIDER,
    EXTRACTOR_MODEL, 
    EXTRACTOR_PROVIDER,
    GROQ_BASE_URL,
    CHAT_MODEL,
    CHAT_PROVIDER, 
    OPENROUTER_BASE_URL, 
    get_api_key
)

def _build_llm(
    model: str,
    provider: str,
    temperature: float = 0.0,
    max_tokens: Optional[int] = None,
    **kwargs
)-> ChatOpenAI:
    """Internal factory - builds a chat open ai instance"""

    llm_kwargs: dict[str, Any] = dict(
        model = model,
        temperature = temperature,
        streaming = streaming,
        max_tokens = max_tokens,
        **kwargs
    )

    if provider == "openrouter":
        llm_kwargs["openai_api_key"] = get_api_key("openrouter")
        llm_kwargs["openai_api_base"] = OPENROUTER_BASE_URL
    elif provider == "groq":
        llm_kwargs["openai_api_key"] = get_api_key("groq")
        llm_kwargs["openai_api_base"] = GROQ_BASE_URL
    elif provider == "openai":
        llm_kwargs['openai_api_key'] = get_api_key("openai")
    
    return ChatOpenAI(**llm_kwargs)



 
def get_router_llm(temperature: float = 0, **kwargs: Any) -> ChatOpenAI:
    """Get router LLM instance"""
    return _build_llm(
        model = ROUTER_MODEL,
        provider = ROUTER_PROVIDER,
        temperature = temperature,
        **kwargs
    )


def get_extractor_llm(temperature: float = 0, **kwargs: Any) -> ChatOpenAI:
    """Get extractor LLM instance"""
    return _build_llm(
        model = EXTRACTOR_MODEL,
        provider = EXTRACTOR_PROVIDER,
        temperature = temperature,
        **kwargs
    )


def get_chat_llm(temperature: float = 0, **kwargs: Any) -> ChatOpenAI:
    """Get chat LLM instance"""
    return _build_llm(
        model = CHAT_MODEL,
        provider = CHAT_PROVIDER,
        temperature = temperature,
        **kwargs
    )