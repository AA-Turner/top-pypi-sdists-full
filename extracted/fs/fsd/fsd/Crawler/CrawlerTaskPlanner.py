import os
import json
import sys
import re
from urllib.parse import urlparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class CrawlerTaskPlanner:
    """
    A class to extract and filter crawlable URLs from text.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner.

        Args:
            repo: Repository instance
        """
        self.repo = repo
        # Common image file extensions to exclude
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', 
                               '.svg', '.bmp', '.tiff', '.ico', '.PNG', 
                               '.JPG', '.JPEG', '.GIF', '.WEBP', '.SVG', 
                               '.BMP', '.TIFF', '.ICO'}

    def is_valid_url(self, url):
        """Check if the URL is valid and not an image file."""
        try:
            result = urlparse(url)
            is_valid = all([result.scheme, result.netloc])
            if not is_valid:
                return False
            
            # Check if URL ends with an image extension
            path = result.path.lower()
            return not any(path.endswith(ext) for ext in self.image_extensions)
        except:
            return False

    def extract_urls(self, text):
        """Extract URLs from text using regex pattern."""
        # URL pattern that matches http/https URLs
        url_pattern = r'https?://[^\s<>"\'\{\}\[\]`]+[a-zA-Z0-9/]'
        urls = re.findall(url_pattern, text)
        return list(set(urls))  # Remove duplicates

    async def get_crawl_plans(self, prompt):
        """
        Extract crawlable URLs from the prompt text.

        Args:
            prompt (str): Text containing URLs to extract.

        Returns:
            dict: Dictionary containing crawl tasks with valid URLs.
        """
        logger.debug("\n #### Extracting crawlable URLs from prompt")
        
        # Extract and filter URLs
        urls = self.extract_urls(prompt)
        valid_urls = [url for url in urls if self.is_valid_url(url)]
        
        # Create crawl tasks for valid URLs
        crawl_tasks = [{"crawl_url": url} for url in valid_urls]
        
        result = {"crawl_tasks": crawl_tasks}
        logger.debug(f"\n #### Found {len(crawl_tasks)} valid URLs to crawl")
        
        return result
