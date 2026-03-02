"""
Aggregator package for handling deployment streaming and results aggregation.
"""

# Import modules to make them available for external use
from matrice_inference.tmp.aggregator.pipeline import ResultsAggregationPipeline
from matrice_inference.tmp.aggregator.synchronizer import ResultsSynchronizer
from matrice_inference.tmp.aggregator.ingestor import ResultsIngestor
from matrice_inference.tmp.aggregator.aggregator import ResultsAggregator
from matrice_inference.tmp.aggregator.publisher import ResultsPublisher

__all__ = [
    "ResultsAggregationPipeline",
    "ResultsSynchronizer", 
    "ResultsIngestor",
    "ResultsAggregator",
    "ResultsPublisher",
] 