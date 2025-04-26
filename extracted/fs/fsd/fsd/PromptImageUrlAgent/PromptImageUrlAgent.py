import os
import sys
import re
from urllib.parse import urlparse, urljoin
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class PromptImageUrlAgent:
    def __init__(self, repo):
        """
        Initialize the PromptImageUrlAgent with the repository.

        Args:
            repo: The repository object.
        """
        self.repo = repo
        self.valid_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.svg', '.PNG', '.JPG', '.JPEG', '.ico')

    def _is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid and has an image extension."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and url.lower().endswith(self.valid_extensions)
        except:
            return False

    def _fix_url(self, url: str) -> str:
        """Add https:// prefix if missing from URL."""
        if not url.startswith(('http://', 'https://')):
            return f'https://{url}'
        return url

    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text using regex pattern."""
        # URL pattern that matches both with and without protocol
        url_pattern = r'(?:https?:\/\/)?(?:[\w-]+\.)+[\w-]+(?:\/[\w\-\.\/\?=&#%]*)*(?:\.(?:jpg|jpeg|png|webp|svg|ico))+'
        urls = re.findall(url_pattern, text, re.IGNORECASE)
        return [self._fix_url(url) for url in urls if url]

    async def process_image_links(self, idea: str) -> Dict[str, List[str]]:
        """
        Extract and validate image links from the given text.

        Args:
            idea (str): The text to extract image links from.

        Returns:
            Dict[str, List[str]]: Dictionary containing list of valid image links.
        """
        # logger.debug("\n #### PromptImageUrlAgent is extracting image links")
        
        # # Extract URLs and validate them
        # extracted_urls = self._extract_urls(idea)
        # valid_urls = [url for url in extracted_urls if self._is_valid_url(url)]
        
        # logger.debug(f"Found {len(valid_urls)} valid image URLs")
        # return {"assets_link": valid_urls}
        
        return {"assets_link": []}
