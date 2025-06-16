import requests
from newspaper import Article
from diskcache import Cache
from time import sleep
from typing import List, Dict, Optional


class Research:
    def __init__(self, api_key: str, cache_enabled: bool = True, cache_dir: str = ".brave_cache", rate_limit: float = 1.0):
        self.api_key = api_key
        self.api_url = "https://api.search.brave.com/res/v1/web/search"
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        self.cache_enabled = cache_enabled
        self.cache = Cache(cache_dir) if cache_enabled else None
        self.rate_limit = rate_limit  # seconds between requests

    def _get_cached(self, key: str) -> Optional[List[Dict]]:
        return self.cache.get(key) if self.cache_enabled else None

    def _set_cached(self, key: str, value: List[Dict]):
        if self.cache_enabled:
            self.cache.set(key, value, expire=3600)

    def _search_brave(self, query: str, count: int = 10) -> List[Dict]:
        params = {"q": query, "count": count}
        response = requests.get(self.api_url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Brave API error: {response.status_code} - {response.text}")

        results = response.json().get("web", {}).get("results", [])
        return [
            {
                "title": item["title"],
                "url": item["url"],
                "description": item.get("description", "")
            }
            for item in results
        ]

    def _extract_content(self, url: str) -> str:
        try:
            article = Article(url)
            article.download()
            article.parse()
            return article.text
        except Exception:
            return ""

    def search_with_content(self, query: str, count: int = 5) -> List[Dict]:
        cache_key = f"search:{query.lower()}:{count}"
        if cached := self._get_cached(cache_key):
            return cached

        search_results = self._search_brave(query, count)
        full_results = []

        for result in search_results:
            print(f"Fetching: {result['title']} - {result['url']}")
            content = self._extract_content(result["url"])
            full_results.append({
                "title": result["title"],
                "url": result["url"],
                "description": result["description"],
                "content": content or "Content could not be extracted."
            })
            sleep(self.rate_limit)

        self._set_cached(cache_key, full_results)
        return full_results
