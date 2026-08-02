from typing import List, Union, Optional
from .constants import TREND_TOPICS
from .trend_keyword import TrendKeyword

class TrendList(list):
    """
    A list-like container for trending topics with additional filtering capabilities.
    Inherits from list to maintain all standard list functionality.
    """
    
    def __init__(self, trends: List[TrendKeyword]):
        super().__init__(trends)
    
    def filter_by_topic(self, topic: Union[int, str, List[Union[int, str]]]) -> 'TrendList':
        """
        Filter trends by topic ID or name.
        
        Args:
            topic: Topic identifier. Can be:
                - int: Topic ID (e.g., 18 for Technology)
                - str: Topic name (e.g., 'Technology')
                - list of int/str: Multiple topics (matches any)
        
        Returns:
            TrendList: New TrendList containing only trends matching the specified topic(s)
        """
        topics = [topic] if not isinstance(topic, list) else topic
        
        name_to_id = {name.lower(): id_ for id_, name in TREND_TOPICS.items()}
        
        topic_ids = set()
        for t in topics:
            if isinstance(t, int):
                topic_ids.add(t)
            elif isinstance(t, str):
                topic_id = name_to_id.get(t.lower())
                if topic_id:
                    topic_ids.add(topic_id)
                    
        filtered = [
            trend for trend in self 
            if any(topic_id in trend.topics for topic_id in topic_ids)
        ]
        
        return TrendList(filtered)
    
    def get_topics_summary(self) -> dict:
        """
        Get a summary of topics present in the trends.
        
        Returns:
            dict: Mapping of topic names to count of trends
        """
        topic_counts = {}
        for trend in self:
            for topic_id in trend.topics:
                topic_name = TREND_TOPICS.get(topic_id, f"Unknown ({topic_id})")
                topic_counts[topic_name] = topic_counts.get(topic_name, 0) + 1
        return dict(sorted(topic_counts.items(), key=lambda x: (-x[1], x[0])))
    
    def __str__(self) -> str:
        """Return string representation of the trends."""
        if not self:
            return "[]"
        return "[\n " + ",\n ".join(trend.brief_summary() for trend in self) + "\n]"