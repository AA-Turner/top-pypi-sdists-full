from typing import List

import attr


@attr.s(auto_attribs=True, frozen=True)
class EmbeddingResponse:
    embeddings: List[List[float]]
