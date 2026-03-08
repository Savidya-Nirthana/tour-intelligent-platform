"""
Core domain models
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class Document:
    """
    Represents a crawled web document.

    Attributes:
        url: Source URL of the docuement
        title: Document or page title
        content: Full text content
        metadata: Additional metadata (headings, links, depath, etc.)
    """
    url: str
    title: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.url:
            raise ValueError("Document URL cannot be empty")
        if not self.content:
            raise ValueError("Document content cannot be empty")

@dataclass
class Chunk:
    """
    Represent a text chunk from a document.

    Attributes:
        text: The chunk content
        chunk_index: Position in the original document
        url: Source document url
        title: Source document title
        metadata: Additional metadata
    """
    text: str
    chunk_index: int 
    url: str
    title: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    

