from typing import Any, Dict, List, Optional

import attr
import attrs

from grazie.api.client.utils import typ


@attrs.define(auto_attribs=True, frozen=True)
class AnswerChunk:
    documents: Optional[List[Dict[str, Any]]] = None
    summaryChunk: Optional[str] = None
    summaryChunkType: Optional[str] = None
    summaryReferences: Optional[List[str]] = None


@attrs.define(auto_attribs=True, frozen=True)
class AnswerStreamV2:
    chunk: AnswerChunk = typ(AnswerChunk)


@attrs.define(auto_attribs=True, frozen=True)
class RetrieveResponse:
    documents: List[Dict[str, Any]]
