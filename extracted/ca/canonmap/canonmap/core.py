import logging

from canonmap.utils.logger import setup_logger
from canonmap.config.validate_configs import (
    CanonMapArtifactsConfig,
    CanonMapEmbeddingConfig,
)
from canonmap.services.artifact_generation.generate_artifacts import generate_artifacts_helper
from canonmap.services.entity_mapping.entity_mapping_helper import map_entities_helper
from canonmap.requests.artifact_generation_request import ArtifactGenerationRequest
from canonmap.requests.entity_mapping_request import EntityMappingRequest
from canonmap.responses.artifact_generation_response import ArtifactGenerationResponse
from canonmap.responses.entity_mapping_response import EntityMappingResponse


logger = setup_logger()

class CanonMap:
    def __init__(
        self,
        artifacts_config: CanonMapArtifactsConfig,
        embedding_config: CanonMapEmbeddingConfig,
        verbose: bool = False,
        api_mode: bool = False,
    ):
        from canonmap.config.utils.loaders import get_embedder, get_artifacts_dir
        
        self.verbose = verbose
        level = logging.INFO if self.verbose else logging.WARNING
        logging.getLogger('canonmap').setLevel(level)

        self.api_mode = api_mode

        # Validate artifacts configuration
        self.artifacts_config = artifacts_config
        if self.api_mode and self.artifacts_config.gcs_config:
            self.artifacts_config.gcs_config.validate_bucket()
        try:
            if not get_artifacts_dir(self.artifacts_config, self.api_mode):
                if self.artifacts_config.gcs_config:
                    logger.warning("No artifacts found locally or in GCS. You will need to generate them first before running matching requests.")
                else:
                    logger.warning("No artifacts found locally. You will need to generate them first before running matching requests.")
                logger.warning("    HINT: Run <your CanonMap instance>.generate_artifacts(ArtifactGenerationRequest) to generate artifacts.")
        except (FileNotFoundError, PermissionError) as e:
            logger.warning(f"Artifacts integration disabled due to configuration issues: {e}")


        # Validate embedding configuration
        self.embedding_config = embedding_config
        if self.api_mode and self.embedding_config.gcs_config:
            self.embedding_config.gcs_config.validate_bucket()
        self.embedder = get_embedder(self.embedding_config, self.api_mode)
        if not self.embedder:
            logger.warning("Embedding model could not be loaded. Semantic search will be disabled.")


    def generate_artifacts(self, request: ArtifactGenerationRequest) -> ArtifactGenerationResponse:
        return generate_artifacts_helper(
            request=request,
            artifacts_config=self.artifacts_config,
            embedder=self.embedder,
        )
    


    def map_entities(self, request: EntityMappingRequest) -> EntityMappingResponse:
        return map_entities_helper(
            request=request,
            artifacts_config=self.artifacts_config,
            embedder=self.embedder,
        )