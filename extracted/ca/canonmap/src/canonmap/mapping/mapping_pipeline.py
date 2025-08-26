import logging
from typing import Any, Dict, Optional, Union
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from canonmap.connectors.mysql_connector.connector import MySQLConnector
from canonmap.mapping.models import EntityMappingRequest, EntityMappingResponse, MappingWeights, SingleMappedEntity
from canonmap.mapping.utils.blocking import block_candidates
from canonmap.mapping.utils.normalize import normalize
from canonmap.mapping.utils.scoring import scorer
from canonmap.connectors.mysql_connector.utils.db_metadata import (
    column_exists as _column_exists,
    get_primary_key_columns as _get_primary_key_columns,
)
from canonmap.connectors.mysql_connector.utils.transforms import (
    to_soundex as _to_soundex,
)
from metaphone import doublemetaphone

logger = logging.getLogger(__name__)


class MappingPipeline:
    def _sanitize_sql_for_logging(self, sql: str, table_name: str) -> str:
        """Sanitize SQL for logging by replacing large IN clauses with item counts."""
        if "IN (" not in sql or ")" not in sql:
            return sql
        
        try:
            import re
            # More flexible regex to match field names (including quoted ones)
            # This handles: field IN (...), `field` IN (...), "field" IN (...)
            match = re.search(r"WHERE\s+([`\"]?\w+[`\"]?)\s+IN\s*\([^)]+\)", sql, re.IGNORECASE)
            if match:
                field_name_in_sql = match.group(1)
                # Find the IN clause more robustly
                in_start = sql.find("IN (")
                if in_start != -1:
                    # Find the matching closing parenthesis
                    paren_count = 0
                    in_end = in_start + 4  # Skip "IN ("
                    for i, char in enumerate(sql[in_start + 4:], in_start + 4):
                        if char == '(':
                            paren_count += 1
                        elif char == ')':
                            if paren_count == 0:
                                in_end = i
                                break
                            paren_count -= 1
                    
                    # Extract and count items in the IN clause
                    in_clause = sql[in_start + 4:in_end]
                    # Split by comma, but be careful about commas inside quotes
                    items = []
                    current_item = ""
                    in_quotes = False
                    quote_char = None
                    
                    for char in in_clause:
                        if char in ["'", '"'] and (not in_quotes or char == quote_char):
                            if not in_quotes:
                                in_quotes = True
                                quote_char = char
                            else:
                                in_quotes = False
                                quote_char = None
                        elif char == ',' and not in_quotes:
                            if current_item.strip():
                                items.append(current_item.strip())
                            current_item = ""
                        else:
                            current_item += char
                    
                    # Add the last item
                    if current_item.strip():
                        items.append(current_item.strip())
                    
                    item_count = len(items)
                    return f"SELECT * FROM {table_name} WHERE {field_name_in_sql} IN ({item_count} items)"
        except Exception:
            # If sanitization fails, return a generic message
            return f"SELECT * FROM {table_name} WHERE [IN clause with multiple items]"
        
        return sql
    def __init__(self, db_connection_manager: MySQLConnector):
        self.db_connection_manager = db_connection_manager

    def run(
        self,
        entity_mapping_request: Union[EntityMappingRequest, Dict[str, Any]],
        mapping_weights: Optional[Union[MappingWeights, Dict[str, Any]]] = None,
    ) -> EntityMappingResponse:
        logger.info("Running matching pipeline")
        # Coerce raw inputs into validated Pydantic models to allow callers to pass dicts/kwargs
        if not isinstance(entity_mapping_request, EntityMappingRequest):
            if isinstance(entity_mapping_request, dict):
                entity_mapping_request = EntityMappingRequest(**entity_mapping_request)
            else:
                raise TypeError(
                    "entity_mapping_request must be EntityMappingRequest or dict[str, Any]"
                )

        if mapping_weights is None:
            mapping_weights = MappingWeights()
        elif not isinstance(mapping_weights, MappingWeights):
            if isinstance(mapping_weights, dict):
                mapping_weights = MappingWeights(**mapping_weights)
            else:
                raise TypeError(
                    "mapping_weights must be MappingWeights, dict[str, Any], or None"
                )

        normalized_entity = normalize(entity_mapping_request.entity_name)
        table_name = entity_mapping_request.candidate_table_name
        field_name = entity_mapping_request.candidate_field_name
        top_n = entity_mapping_request.top_n
        max_prefilter = entity_mapping_request.max_prefilter
        prefilter_sql = entity_mapping_request.prefilter_sql

        # Execute prefilter SQL if provided
        prefiltered_table = table_name
        prefilter_subquery = None
        if prefilter_sql:
            try:
                # Log a sanitized version of the SQL (without showing list contents)
                sanitized_sql = self._sanitize_sql_for_logging(prefilter_sql, table_name)
                logger.info(f"Executing prefilter SQL: {sanitized_sql}")
                prefilter_result = self.db_connection_manager.execute_query(
                    prefilter_sql, [], allow_writes=False
                )
                if prefilter_result.get("data"):
                    # Instead of creating a temporary table, we'll use the prefilter SQL as a subquery
                    prefilter_subquery = f"({prefilter_sql})"
                    logger.info(f"Using prefilter subquery with {len(prefilter_result['data'])} rows")
                else:
                    logger.warning("Prefilter SQL returned no data")
            except Exception as e:
                logger.error(f"Error executing prefilter SQL: {e}")
                # Continue with original table if prefilter fails

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
                        prefiltered_table,
                        field_name,
                        block_type,
                        max_prefilter,
                        prefilter_subquery,
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


    def run_dev(
        self,
        entity_mapping_request: Union[EntityMappingRequest, Dict[str, Any]],
        mapping_weights: Optional[Union[MappingWeights, Dict[str, Any]]] = None,
        per_strategy_limits: Optional[Dict[str, int]] = None,
        global_prefilter_cap: Optional[int] = None,
        debug: bool = True,
    ) -> EntityMappingResponse:
        """
        Development-focused mapping run with deterministic prefiltering, helper-field fallbacks,
        per-strategy limits, and richer debug logging. Returns the same response schema as run().
        """
        logger.info("Running matching pipeline (dev)")
        # Normalize inputs to Pydantic models
        if not isinstance(entity_mapping_request, EntityMappingRequest):
            if isinstance(entity_mapping_request, dict):
                entity_mapping_request = EntityMappingRequest(**entity_mapping_request)
            else:
                raise TypeError(
                    "entity_mapping_request must be EntityMappingRequest or dict[str, Any]"
                )

        if mapping_weights is None:
            mapping_weights = MappingWeights()
        elif not isinstance(mapping_weights, MappingWeights):
            if isinstance(mapping_weights, dict):
                mapping_weights = MappingWeights(**mapping_weights)
            else:
                raise TypeError(
                    "mapping_weights must be MappingWeights, dict[str, Any], or None"
                )

        normalized_entity = normalize(entity_mapping_request.entity_name)
        table_name = entity_mapping_request.candidate_table_name
        field_name = entity_mapping_request.candidate_field_name
        top_n = entity_mapping_request.top_n
        default_limit = entity_mapping_request.max_prefilter
        prefilter_sql = entity_mapping_request.prefilter_sql

        # Execute prefilter SQL if provided
        prefiltered_table = table_name
        prefilter_subquery = None
        if prefilter_sql:
            try:
                # Log a sanitized version of the SQL (without showing list contents)
                sanitized_sql = self._sanitize_sql_for_logging(prefilter_sql, table_name)
                logger.info(f"Executing prefilter SQL: {sanitized_sql}")
                prefilter_result = self.db_connection_manager.execute_query(
                    prefilter_sql, [], allow_writes=False
                )
                if prefilter_result.get("data"):
                    # Instead of creating a temporary table, we'll use the prefilter SQL as a subquery
                    prefilter_subquery = f"({prefilter_sql})"
                    logger.info(f"Using prefilter subquery with {len(prefilter_result['data'])} rows")
                else:
                    logger.warning("Prefilter SQL returned no data")
            except Exception as e:
                logger.error(f"Error executing prefilter SQL: {e}")
                # Continue with original table if prefilter fails

        # Strategy configuration
        block_types = [
            "phonetic",
            "soundex",
            "initialism",
            "exact",
        ]

        # Simple metadata caches for this invocation
        column_exists_cache: Dict[tuple[str, str], bool] = {}
        pk_cache: Dict[str, list[str]] = {}

        def _column_exists_cached(table: str, column: str) -> bool:
            key = (table, column)
            if key not in column_exists_cache:
                try:
                    column_exists_cache[key] = bool(_column_exists(self.db_connection_manager, table, column))
                except Exception:
                    column_exists_cache[key] = False
            return column_exists_cache[key]

        def _get_pk_columns_cached(table: str) -> list[str]:
            if table not in pk_cache:
                try:
                    pk_cache[table] = list(_get_primary_key_columns(self.db_connection_manager, table))
                except Exception:
                    pk_cache[table] = []
            return pk_cache[table]

        def _choose_helper_column(fld: str, suffix: str) -> Optional[str]:
            """Prefer __<field>_<suffix>__ then <field>_<suffix>__ if present."""
            primary = f"__{fld}_{suffix}__"
            fallback = f"{fld}_{suffix}__"
            if _column_exists_cached(prefiltered_table, primary):
                return primary
            if _column_exists_cached(prefiltered_table, fallback):
                return fallback
            return None

        def _order_by_clause() -> str:
            # When using DISTINCT, we can only ORDER BY columns in the SELECT list
            # Since we only SELECT the field_name, we can only ORDER BY that
            return f"ORDER BY LOWER(TRIM(`{field_name}`)), `{field_name}`"

        def _limit_for(strategy: str) -> int:
            if per_strategy_limits and strategy in per_strategy_limits:
                return int(per_strategy_limits[strategy])
            return int(default_limit)

        # Prepare parameters per strategy
        def _param_phonetic(entity: str) -> Optional[str]:
            p1, p2 = doublemetaphone(entity)
            return p1 or p2

        def _param_initialism(entity: str) -> Optional[str]:
            if not entity:
                return None
            import re as _re
            entity_clean = entity.strip().upper()
            if entity_clean.isalpha() and 2 <= len(entity_clean) <= 6 and " " not in entity_clean:
                return entity_clean
            parts = _re.findall(r"[A-Za-z]+", entity)
            return "".join(p[0].upper() for p in parts) if parts else None

        def _param_exact(entity: str) -> Optional[str]:
            if not entity:
                return None
            return entity.strip().lower()

        # Build and execute blocking queries deterministically
        strategy_to_candidates: Dict[str, set[str]] = {s: set() for s in block_types}

        for strategy in block_types:
            try:
                if strategy == "phonetic":
                    helper_col = _choose_helper_column(field_name, "phonetic")
                    param = _param_phonetic(normalized_entity)
                    if not param or not helper_col:
                        continue
                    
                    from_clause = f"`{prefiltered_table}`"
                    if prefilter_subquery:
                        from_clause = f"{prefilter_subquery} AS `{prefiltered_table}`"
                    
                    sql = f"""
                        SELECT DISTINCT `{field_name}` AS name
                        FROM {from_clause}
                        WHERE `{helper_col}` LIKE %s
                        {_order_by_clause()}
                    """
                    resp = self.db_connection_manager.execute_query(sql, [param], allow_writes=False, limit=_limit_for(strategy))
                elif strategy == "initialism":
                    helper_col = _choose_helper_column(field_name, "initialism")
                    param = _param_initialism(normalized_entity)
                    if debug:
                        logger.info("Initialism strategy: helper_col=%s, param=%s", helper_col, param)
                    if not param or not helper_col:
                        if debug:
                            logger.info("Initialism strategy: skipping - no param (%s) or no helper_col (%s)", param, helper_col)
                        continue
                    
                    from_clause = f"`{prefiltered_table}`"
                    if prefilter_subquery:
                        from_clause = f"{prefilter_subquery} AS `{prefiltered_table}`"
                    
                    sql = f"""
                        SELECT DISTINCT `{field_name}` AS name
                        FROM {from_clause}
                        WHERE `{helper_col}` = %s
                        {_order_by_clause()}
                    """
                    if debug:
                        logger.info("Initialism SQL: %s with param count: %d", sql, len([param]))
                    resp = self.db_connection_manager.execute_query(sql, [param], allow_writes=False, limit=_limit_for(strategy))
                elif strategy == "soundex":
                    # Prefer helper column; otherwise use DB SOUNDEX
                    helper_col = _choose_helper_column(field_name, "soundex")
                    params: list[Any]
                    
                    from_clause = f"`{prefiltered_table}`"
                    if prefilter_subquery:
                        from_clause = f"{prefilter_subquery} AS `{prefiltered_table}`"
                    
                    if helper_col:
                        try:
                            code = _to_soundex(normalized_entity)
                        except Exception:
                            code = None
                        if not code:
                            # Fallback to DB SOUNDEX if local soundex unavailable
                            sql = f"""
                                SELECT DISTINCT `{field_name}` AS name
                                FROM {from_clause}
                                WHERE SOUNDEX(`{field_name}`) = SOUNDEX(%s)
                                {_order_by_clause()}
                            """
                            params = [normalized_entity]
                        else:
                            sql = f"""
                                SELECT DISTINCT `{field_name}` AS name
                                FROM {from_clause}
                                WHERE `{helper_col}` = %s
                                {_order_by_clause()}
                            """
                            params = [code]
                    else:
                        sql = f"""
                            SELECT DISTINCT `{field_name}` AS name
                            FROM {from_clause}
                            WHERE SOUNDEX(`{field_name}`) = SOUNDEX(%s)
                            {_order_by_clause()}
                        """
                        params = [normalized_entity]
                    resp = self.db_connection_manager.execute_query(sql, params, allow_writes=False, limit=_limit_for(strategy))
                elif strategy == "exact":
                    param = _param_exact(normalized_entity)
                    if not param:
                        continue
                    
                    from_clause = f"`{prefiltered_table}`"
                    if prefilter_subquery:
                        from_clause = f"{prefilter_subquery} AS `{prefiltered_table}`"
                    
                    sql = f"""
                        SELECT DISTINCT `{field_name}` AS name
                        FROM {from_clause}
                        WHERE LOWER(TRIM(`{field_name}`)) LIKE %s
                        {_order_by_clause()}
                    """
                    resp = self.db_connection_manager.execute_query(sql, [param], allow_writes=False, limit=_limit_for(strategy))
                else:
                    continue

                rows = resp.get("data") or []
                names = {r["name"] for r in rows}
                strategy_to_candidates[strategy] |= names
                if debug:
                    logger.info("%s returned %d candidates", strategy, len(names))
            except Exception as e:
                logger.error("%s error: %s", strategy, e)

        # Union candidates across strategies
        union_candidates: Dict[str, set[str]] = defaultdict(set)
        for strategy, names in strategy_to_candidates.items():
            for n in names:
                union_candidates[n].add(strategy)

        # Optional global prefilter cap with deterministic ordering (lexical)
        candidate_names = sorted(union_candidates.keys(), key=lambda s: (s.lower(), s))
        if global_prefilter_cap is not None:
            candidate_names = candidate_names[: int(global_prefilter_cap)]

        # Score concurrently
        signatures: list[tuple[str, float]] = []
        with ThreadPoolExecutor() as ex:
            futures = {ex.submit(scorer, normalized_entity, c, mapping_weights): c for c in candidate_names}
            for future in as_completed(futures):
                candidate_name, score = future.result()
                signatures.append((candidate_name, float(score) if score is not None else 0.0))

        # Sort by score desc, deterministic tie-break by name
        signatures.sort(key=lambda x: (-x[1], x[0].lower(), x[0]))

        results: list[SingleMappedEntity] = []
        for candidate_name, score in signatures[:top_n]:
            results.append(SingleMappedEntity(
                raw_entity=entity_mapping_request.entity_name,
                canonical_entity=candidate_name,
                canonical_table_name=table_name,
                canonical_field_name=field_name,
                score=float(score),
            ))

        if debug:
            logger.info("Union candidates: %d; strategies hit counts: %s", len(union_candidates), {k: len(v) for k, v in strategy_to_candidates.items()})
            if results:
                logger.info("Top result: %s (score=%.4f)", results[0].canonical_entity, results[0].score)

        return EntityMappingResponse(results=results)
