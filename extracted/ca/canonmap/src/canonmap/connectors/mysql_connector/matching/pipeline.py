# src/canonmap/connectors/mysql_connector/matching/pipeline.py

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

from canonmap.connectors.mysql_connector.matching.blocking import (
    block_by_phonetic, block_by_soundex, block_by_initialism,
    block_by_exact_match, get_more_candidates,
)
from canonmap.connectors.mysql_connector.matching.scoring import score_candidate
from canonmap.connectors.mysql_connector.matching.normalization import normalize
from canonmap.connectors.mysql_connector.matching.validation.requests import EntityMappingRequest, EntityMappingResponse
from canonmap.connectors.mysql_connector.matching.validation.models import SingleMappedEntity
from canonmap.connectors.mysql_connector.mysql_connector import MySQLConnector
from canonmap.exceptions import MatchingError

logger = logging.getLogger(__name__)

load_dotenv(override=True)

DEFAULT_WEIGHTS = {
    "exact": 6.0,
    "levenshtein": 1.0,
    "jaro": 1.2,
    "token": 2.0,
    "trigram": 1.0,
    "phonetic": 1.0,
    "soundex": 1.0,
    "initialism": 0.5,
    "multi_bonus": 1.0,
}

class MatchingPipeline:
    """
    Orchestrates the matching process: blocking, scoring, ranking.
    """

    def __init__(self, connection_manager: MySQLConnector, weights=None):
        self.connection_manager = connection_manager
        self.weights = weights or DEFAULT_WEIGHTS

    def match(self, request: EntityMappingRequest) -> EntityMappingResponse:
        # Validate request
        if not request.entity_name or not request.entity_name.strip():
            raise ValueError("entity_name cannot be empty")
        
        if not request.select_field:
            raise ValueError("select_field is required")
        
        # Normalize query
        normalized_entity_name = normalize(request.entity_name)
        table_name = request.select_field.table.name
        field_name = request.select_field.name
        top_n = request.top_n
        
        # Check if already connected to the right database
        database_name = request.select_field.table.database.name
        current_database = self.connection_manager.config.database
        
        # Only reconnect if not connected or connected to different database
        if not self.connection_manager.pool or current_database != database_name:
            logger.info(f"Connecting to database: {database_name}")
            self.connection_manager.config.database = database_name
            self.connection_manager.connect_to_database(database_name)
        else:
            logger.info(f"Already connected to database: {database_name}")
        
        if not self.connection_manager.pool:
            raise RuntimeError("Connection pool not initialized")
            
        conn = self.connection_manager.pool.get_connection()

        # Candidate blocking (all strategies)
        candidates = set()
        try:
            candidates.update(block_by_phonetic(conn, normalized_entity_name, table_name, field_name))
            candidates.update(block_by_soundex(conn, normalized_entity_name, table_name, field_name))
            candidates.update(block_by_initialism(conn, normalized_entity_name, table_name, field_name))
            candidates.update(block_by_exact_match(conn, normalized_entity_name, table_name, field_name))

            # Broaden if not enough candidates
            min_candidates = max(50, top_n * 3)
            if len(candidates) < min_candidates:
                more = get_more_candidates(conn, normalized_entity_name, table_name, field_name, min_candidates - len(candidates))
                candidates.update(more)
            
            # Ensure we have candidates to process
            if not candidates:
                return EntityMappingResponse(results=[])
        except Exception as e:
            logger.error(f"Error in matching process: {str(e)}")
            raise MatchingError(f"Error in matching process: {str(e)}")
        # finally:
        #     if conn is not None:
        #         logger.info(f"Closing connection to {database_name}")
        #         conn.close()

        # Score all candidates (parallel)
        def scorer(candidate_name):
            return candidate_name, score_candidate(normalized_entity_name, candidate_name, self.weights)

        signatures = []
        with ThreadPoolExecutor() as ex:
            futures = {ex.submit(scorer, c): c for c in candidates}
            for future in as_completed(futures):
                candidate_name, score = future.result()
                signatures.append((candidate_name, score))

        # Rank and package results
        signatures.sort(key=lambda x: x[1], reverse=True)
        initial_results = []
        for candidate_name, score in signatures[:top_n]:
            # Ensure score is a float
            score_float = float(score) if score is not None else 0.0
            initial_results.append(SingleMappedEntity(
                raw_entity=request.entity_name,
                canonical_entity=candidate_name,
                canonical_table_name=table_name,
                canonical_field_name=field_name,
                score=score_float,
            ))

        # Try semantic rerank with Cohere if API key is available
        if request.semantic_rerank and os.getenv("COHERE_API_KEY"):
            try:
                cohere_api_key = os.getenv("COHERE_API_KEY")
                if cohere_api_key and initial_results:
                    logger.info("Attempting semantic rerank with Cohere")
                    results = self._semantic_rerank(
                        query=request.entity_name,
                        candidates=initial_results,
                        top_n=top_n
                    )
                    logger.info(f"Semantic rerank completed, returned {len(results)} results")
                else:
                    results = initial_results
                    if not cohere_api_key:
                        logger.debug("COHERE_API_KEY not found, skipping semantic rerank")
                    else:
                        logger.debug("No candidates to rerank")
            except Exception as e:
                logger.warning(f"Semantic rerank failed, falling back to initial results: {str(e)}")
                results = initial_results
        else:
            results = initial_results

        return EntityMappingResponse(results=results)

    def _semantic_rerank(self, query: str, candidates: list, top_n: int) -> list:
        """
        Perform semantic reranking using Cohere's rerank API.
        
        Args:
            query: The original search query
            candidates: List of SingleMappedEntity objects to rerank
            top_n: Number of top results to return
            
        Returns:
            List of reranked SingleMappedEntity objects
        """
        try:
            import cohere
            
            # Initialize Cohere client
            co = cohere.ClientV2()
            
            # Prepare documents for Cohere API
            documents = [candidate.canonical_entity for candidate in candidates]
            
            # Call Cohere rerank API
            response = co.rerank(
                model="rerank-v3.5",
                query=query,
                documents=documents,
                top_n=min(top_n, len(documents))
            )
            
            # Map Cohere results back to our format
            reranked_results = []
            for result in response.results:
                index = result.index
                if 0 <= index < len(candidates):
                    # Create new entity with updated score
                    original_entity = candidates[index]
                    reranked_entity = SingleMappedEntity(
                        raw_entity=original_entity.raw_entity,
                        canonical_entity=original_entity.canonical_entity,
                        canonical_table_name=original_entity.canonical_table_name,
                        canonical_field_name=original_entity.canonical_field_name,
                        score=float(result.relevance_score)
                    )
                    reranked_results.append(reranked_entity)
            
            logger.info(f"Cohere rerank processed {len(reranked_results)} results")
            return reranked_results
            
        except ImportError:
            logger.error("Cohere library not installed. Install with: pip install cohere")
            return candidates
        except Exception as e:
            logger.error(f"Cohere rerank failed: {str(e)}")
            return candidates