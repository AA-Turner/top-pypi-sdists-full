from typing import Dict, List, Optional

import attr

from grazie.api.client.profiles import LLMProfile


@attr.s(auto_attribs=True)
class EmbeddingRequest:
    texts: List[str]
    model: Optional[str] = None
    normalize: bool = False
    format_cbor: bool = False


@attr.s(auto_attribs=True)
class LLMEmbeddingRequest:
    texts: List[str]
    profile: LLMProfile
    dimensions: Optional[int] = None
