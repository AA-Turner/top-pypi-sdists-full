"""
Aggregator package for handling deployment streaming and results aggregation.
"""

# Import modules to make them available for external use
from .pipeline import ResultsAggregationPipeline
from .synchronizer import ResultsSynchronizer
from .ingestor import ResultsIngestor
from .aggregator import ResultsAggregator
from .publisher import ResultsPublisher

__all__ = [
    "ResultsAggregationPipeline",
    "ResultsSynchronizer", 
    "ResultsIngestor",
    "ResultsAggregator",
    "ResultsPublisher",
] 