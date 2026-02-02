"""
DSLighting Data Analyzer Service

Re-export dsat.services.data_analyzer.DataAnalyzer.
"""
try:
    from dsat.services.data_analyzer import DataAnalyzer
except ImportError:
    DataAnalyzer = None

__all__ = ["DataAnalyzer"]
