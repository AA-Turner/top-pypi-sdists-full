from .utils import parse_time_ago, flatten_dict
from datetime import datetime

class NewsArticle:
    """
    Represents a news article related to a trending topic.

    This class handles both dictionary and list-based article data from
    various Google Trends API endpoints.

    Parameters:
        title (str): Article title
        url (str): Article URL
        source (str): News source name
        picture (str): URL to article image
        time (str or int): Publication time or timestamp
        snippet (str): Article preview text

    Note:
        If time is provided as a string with 'ago' format (e.g., '2 hours ago'),
        it will be automatically converted to a timestamp.
    """
    def __init__(self, title=None, url=None, source=None, picture=None, time=None, snippet=None, article_ids=None):
        self.title = title
        self.url = url
        self.source = source
        self.picture = picture
        self.time = time
        if isinstance(self.time, str) and ('ago' in self.time):
            self.time = parse_time_ago(self.time)
        self.snippet = snippet

    @classmethod
    def from_api(cls, data):
        if isinstance(data, dict):
            return cls(
                title=data.get('title') or data.get('articleTitle'),
                url=data.get('url'),
                source=data.get('source'),
                picture=data.get('picture') or data.get('image', {}).get('imageUrl'),
                time=data.get('time') or data.get('timeAgo'),
                snippet=data.get('snippet')
            )
        elif isinstance(data, list):
            return cls(
                title=data[0],
                url=data[1],
                source=data[2],
                time=data[3][0] if data[3] else None,
                picture=data[4] if len(data) > 4 else None
            )
        else:
            raise ValueError("Unsupported data format: must be dict or list")

    def __repr__(self):
        return f"NewsArticle(title={self.title!r}, url={self.url!r}, source={self.source!r}, " \
               f"picture={self.picture!r}, time={self.time!r}, snippet={self.snippet!r})"

    def __str__(self):
        s =    'Title   : {}'.format(self.title)
        s += '\nURL     : {}'.format(self.url) if self.url else ''
        s += '\nSource  : {}'.format(self.source) if self.source else ''
        s += '\nPicture : {}'.format(self.picture) if self.picture else ''
        s += '\nTime    : {}'.format(datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H:%M:%S')) if self.time else ''
        s += '\nSnippet : {}'.format(self.snippet) if self.snippet else ''
        return s