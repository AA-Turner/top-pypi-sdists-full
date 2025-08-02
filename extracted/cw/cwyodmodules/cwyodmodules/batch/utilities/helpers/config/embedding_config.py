from ..document_loading_helper import LoadingSettings
from ..document_chunking_helper import ChunkingSettings


class EmbeddingConfig(ChunkingSettings, LoadingSettings):
    def __init__(
        self,
        document_type: str,
        chunking: ChunkingSettings | None,
        loading: LoadingSettings | None,
        use_advanced_image_processing: bool,
    ):
        self.document_type = document_type
        self.chunking = chunking
        self.loading = loading
        self.use_advanced_image_processing = use_advanced_image_processing

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (
                self.document_type == other.document_type
                and self.chunking == other.chunking
                and self.loading == other.loading
                and self.use_advanced_image_processing
                == other.use_advanced_image_processing
            )
        return False

    def to_dict(self):
        return {
            "document_type": self.document_type,
            "chunking": self.chunking.to_dict() if self.chunking else None,
            "loading": self.loading.to_dict() if self.loading else None,
            "use_advanced_image_processing": self.use_advanced_image_processing,
        }
