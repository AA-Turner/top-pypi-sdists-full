import logging
from typing import Sequence

from llama_index import KnowledgeGraphIndex
from llama_index.data_structs.data_structs import KG
from llama_index.schema import BaseNode, MetadataMode
from llama_index.utils import get_tqdm_iterable

from ghostcoder.index.schema import CodeNode

logger = logging.getLogger(__name__)

class CodeKnowledgeGraph(KnowledgeGraphIndex):

    def _build_index_from_nodes(self, nodes: Sequence[BaseNode]) -> KG:
        """Build the index from nodes."""
        # do simple concatenation
        index_struct = self.index_struct_cls()
        nodes_with_progress = get_tqdm_iterable(
            nodes, self._show_progress, "Processing nodes"
        )
        for n in nodes_with_progress:
            if not isinstance(n, CodeNode):
                continue

            triplets = []
            for reference in n.codeblock.get_references():
                if reference.type == ReferenceType.IMPORT:
                    triplets.append((n.codeblock.identifier, "imports", reference.identifier))

            logger.debug(f"> Extracted triplets form {n.codeblock.identifier}: {triplets}")
            for triplet in triplets:
                subj, _, obj = triplet
                self.upsert_triplet(triplet)
                index_struct.add_node([subj, obj], n)

            if self.include_embeddings:
                triplet_texts = [str(t) for t in triplets]

                embed_model = self._service_context.embed_model
                embed_outputs = embed_model.get_text_embedding_batch(
                    triplet_texts, show_progress=self._show_progress
                )
                for rel_text, rel_embed in zip(triplet_texts, embed_outputs):
                    index_struct.add_to_embedding_dict(rel_text, rel_embed)

        return index_struct
