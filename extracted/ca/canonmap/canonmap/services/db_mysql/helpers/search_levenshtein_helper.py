import logging

from canonmap.services.db_mysql.schemas import EntityMappingRequest

logger = logging.getLogger(__name__)

try:
    import Levenshtein  # pip install python-Levenshtein
    _have_lev = True
except ImportError:
    from difflib import SequenceMatcher
    _have_lev = False


def search_levenshtein(conn, request: EntityMappingRequest):
    entity_name = request.entity_name
    threshold = request.threshold
    max_prefilter = request.max_prefilter

    for field_object in request.select_fields:
        field_name = field_object.field_name
        table_name = field_object.table_name
        
        # Create a more flexible prefix by taking the first word and making it case-insensitive
        entity_name_split = entity_name.split(" ")
        if len(entity_name_split[0]) >= 2:
            # Use first 2+ characters of first word for broader matching
            prefix = entity_name_split[0][:2].lower() + '%'
        else:
            prefix = entity_name_split[0].lower() + '%'
        
        # Use case-insensitive LIKE for prefix matching and select the actual field values
        sql = """
        SELECT `{field_name}`
        FROM `{table_name}`
        WHERE LOWER(`{field_name}`) LIKE %s
        LIMIT %s;
        """
        sql = sql.format(table_name=table_name, field_name=field_name)
        cur = conn.cursor(buffered=True)
        cur.execute(sql, (prefix, max_prefilter))
        candidates = cur.fetchall()
        logger.info(f"Found {len(candidates)} candidates for prefix '{prefix}'")
        
        # normalize query once
        name_norm = entity_name.lower().replace(" ", "")

        results = []
        for row in candidates:
            cand = row[0]  # Get the field value from the first column
            # normalize candidate
            cand_norm = cand.lower().replace(" ", "")
            if _have_lev:
                score = Levenshtein.ratio(name_norm, cand_norm)
            else:
                score = SequenceMatcher(None, name_norm, cand_norm).ratio()
            if score >= threshold:
                results.append((cand, round(score, 3)))
        
        # If we have candidates but no results and threshold > 0, try with threshold = 0.0
        if len(candidates) > 0 and len(results) == 0 and threshold > 0.0:
            logger.info(f"No results found with threshold {threshold}, retrying with threshold 0.0")
            request_copy = EntityMappingRequest(
                entity_name=request.entity_name,
                select_fields=request.select_fields,
                threshold=0.0,
                max_prefilter=request.max_prefilter
            )
            return search_levenshtein(conn, request_copy)
        
        # sort by best match first
        results.sort(key=lambda x: x[1], reverse=True)
        return results

