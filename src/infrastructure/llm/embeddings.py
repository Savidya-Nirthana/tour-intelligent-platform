"""
embedding model provider

"""

from typing import Optional, Any
from langchain_openai import OpenAIEmbeddings

from infrastructure.config import (
    EMBEDDING_MODEL,PROVIDER,OPENROUTER_BASE_URL,get_api_key
)

def get_defailt_embedding(
    batch_size: int = 100,
    show_progress: bool = False, 
    **kwargs: Any
) -> OpenAIEmbeddings:
    """
    Get an OpenAIEmbeddings instance configured for the active provider.
    when PROVIDER = openrouter, requests are routed through openrouter
    otherwise direct openai api call
    """

    embedding_kwargs: dict[str, Any] = dict(
        model = EMBEDDING_MODEL,
        show_progress = show_progress,
        **kwargs
    )

    if PROVIDER == "openrouter":
        embedding_kwargs["openai_api_key"] = get_api_key("openrouter")
        embedding_kwargs["openai_api_base"] = OPENROUTER_BASE_URL
    else:
        embedding_kwargs["openai_api_key"] = get_api_key("openai")

    return OpenAIEmbeddings(**embedding_kwargs)