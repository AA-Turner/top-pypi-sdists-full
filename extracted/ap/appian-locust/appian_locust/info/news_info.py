from requests.models import Response
from typing import Any, Dict, Optional

from .._news import _News


class NewsInfo:
    """
    Class which provides metadata about news entries from the Tempo News tab
    """

    def __init__(self, news: _News):
        self.__news = news

    def get_all_available_entries(self, search_string: Optional[str] = None,
                                  locust_request_label: str = "News.AllAvailableEntries") -> Dict[str, Any]:
        """
        Retrieves all the available "news" and associated metadata from "Appian-Tempo-News"

        Args:
            search_string(str, optional): results will be filtered based on the search string.
            locust_request_label (str): Label locust should associate with the request

        Returns (dict): List of news and associated metadata

        Examples:

            >>> news_info.get_all()
        """
        return self.__news.get_all(search_string=search_string, locust_request_label=locust_request_label)

    def get_news_entry(self, news_name: str, exact_match: bool = True, search_string: Optional[str] = None) -> Dict[str, Any]:
        """
        Get the information about specific news by name.

        Args:
            news_name (str): name of the news entry
            exact_match (bool, optional): Should news name match exactly or to be partial match. Default : True
            search_string (str, optional): results will be filtered based on the search string.

        Returns: Specific News's info

        Raises: In case news is not found in the system, it throws an "Exception"

        Example:
            If full name of action is known,

            >>> news_info.get_news("news_name")

            If only partial name is known,

            >>> news_info.get_news("news_name", exact_match=False)

        """
        return self.__news.get_news(news_name, exact_match, search_string)

    def get_news_entry_related_records(self, news_name: str, exact_match: bool = True,
                                       search_string: Optional[str] = None,
                                       locust_request_label: Optional[str] = None) -> Optional[Response]:
        """
        Request related records information for a news entry
        Args:
            news_name (str): name of the news entry
            exact_match (bool, optional): Should news name match exactly or to be partial match. Default : True
            search_string (str, optional): results will be filtered based on the search string.
            locust_request_label (str, optional): Label locust should associate with the request for related records

        Returns: Response object with related records information, if any exists

        """
        locust_request_label = locust_request_label or f"News.Entry.{news_name}.RelatedRecords"
        news_entry = self.__news.get_news(news_name, exact_match, search_string)
        for link in news_entry['links']:
            if 'newsRelatedRecords' in link['href']:
                return self.__news.interactor.get_page(link['href'], label=locust_request_label)
        return None

    def get_news_entry_record_tags(self, news_name: str, locust_request_label: Optional[str] = None) -> Optional[Response]:
        """
        Get the record tags associated with a news entry
        Args:
            news_name (str): News entry ID
            locust_request_label (str, optional): Label locust should associate with the request for record tags

        Returns:

        """
        locust_request_label = locust_request_label or f"News.Entry.{news_name}.RecordTags"
        return self.__news.fetch_news_entry_record_tags(news_entry_id=news_name, locust_request_label=locust_request_label)
