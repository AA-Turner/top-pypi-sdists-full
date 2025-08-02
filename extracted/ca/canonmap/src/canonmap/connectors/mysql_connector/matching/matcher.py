# src/canonmap/connectors/mysql_connector/matching/matcher.py

from canonmap.connectors.mysql_connector.matching.pipeline import MatchingPipeline

class Matcher:
    """
    Facade for entity matching. Handles setup, and delegates to MatchingPipeline.
    """

    def __init__(self, connection_manager, weights=None):
        self._pipeline = MatchingPipeline(connection_manager, weights)

    def match(self, request):
        """
        Matches an entity to candidates in the database according to the pipeline.
        :param request: An EntityMappingRequest (or similar)
        :return: List of results (can be dicts, pydantic models, etc.)
        """
        return self._pipeline.match(request)