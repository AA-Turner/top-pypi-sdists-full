import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from canonmap.connectors.mysql_connector.connector import MySQLConnector
from canonmap.mapping.models import EntityMappingRequest, EntityMappingResponse, MappingWeights, SingleMappedEntity
from canonmap.mapping.utils.blocking import block_candidates
from canonmap.mapping.utils.normalize import normalize
from canonmap.mapping.utils.scoring import scorer

logger = logging.getLogger(__name__)


class MappingPipeline:
    def __init__(self, db_connection_manager: MySQLConnector):
        self.db_connection_manager = db_connection_manager

    def run(self, entity_mapping_request: EntityMappingRequest, mapping_weights: MappingWeights = None) -> EntityMappingResponse:
        logger.info("Running matching pipeline")
        mapping_weights = mapping_weights or MappingWeights()
        normalized_entity = normalize(entity_mapping_request.entity_name)
        table_name = entity_mapping_request.candidate_table_name
        field_name = entity_mapping_request.candidate_field_name
        top_n = entity_mapping_request.top_n

        try:
            block_types = [
                "phonetic",
                "soundex",
                "initialism",
                "exact",
            ]

            candidate_sets = []
            with ThreadPoolExecutor(max_workers=len(block_types)) as executor:
                future_to_name = {
                    executor.submit(
                        block_candidates,
                        self.db_connection_manager,
                        normalized_entity,
                        table_name,
                        field_name,
                        block_type,
                    ): block_type
                    for block_type in block_types
                }
                for future in as_completed(future_to_name):
                    name = future_to_name[future]
                    try:
                        result = future.result()
                        logger.info(f"{name} returned {len(result)} candidates")
                        candidate_sets.append(result)
                    except Exception as e:
                        logger.error(f"{name} error: {e}")

            candidates = set().union(*candidate_sets)
        except Exception as e:
            logger.error(f"Error getting candidates: {e}")
            return EntityMappingResponse(results=[])

        signatures = []
        with ThreadPoolExecutor() as ex:
            futures = {ex.submit(scorer, normalized_entity, c, mapping_weights): c for c in candidates}
            for future in as_completed(futures):
                candidate_name, score = future.result()
                signatures.append((candidate_name, score))

        signatures.sort(key=lambda x: x[1], reverse=True)
        initial_results = []
        for candidate_name, score in signatures[:top_n]:
            score_float = float(score) if score is not None else 0.0
            initial_results.append(SingleMappedEntity(
                raw_entity=entity_mapping_request.entity_name,
                canonical_entity=candidate_name,
                canonical_table_name=table_name,
                canonical_field_name=field_name,
                score=score_float,
            ))

        return EntityMappingResponse(results=initial_results)

