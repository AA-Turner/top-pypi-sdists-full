from bs4 import BeautifulSoup
from typing import Any
import os
import re
from urllib.parse import urlparse, parse_qs, urlencode, urljoin

import tldextract
from functools import lru_cache

from matrx_files import FileManager
from matrx_utils import vcprint


def get_soup(soup: Any) -> BeautifulSoup:
    if isinstance(soup, BeautifulSoup):
        return soup
    else:
        return BeautifulSoup(str(soup), "lxml")


class URLInfo:
    def __init__(self, url):
        self.url = self.clean_url(url)
        self.parsed_url = urlparse(self.url)
        self.extracted = tldextract.extract(self.parsed_url.netloc)

        self.full_domain = self.construct_full_domain()
        self.path = self.construct_path()
        self.unique_page_name = self.construct_unique_page_name()
        self.website = f"{self.extracted.domain}.{self.extracted.suffix}"
        self.subdomain = self.extracted.subdomain  # No default to 'www' here
        self.domain_type = self.extracted.suffix
        self.extension = self.get_extension()

    def clean_url(self, url):
        # Ensure the URL has the scheme
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = "https://" + url
            parsed_url = urlparse(url)

        # Remove fragment
        url = url.split("#")[0]
        parsed_url = urlparse(url)

        # Remove empty query parameters
        query_params = parse_qs(parsed_url.query)
        query_params = {k: v for k, v in query_params.items() if v and v[0]}
        query_string = urlencode(query_params, doseq=True)

        # Extract domain components without assuming 'www' by default
        extracted = tldextract.extract(parsed_url.netloc)
        subdomain = extracted.subdomain  # Keep subdomain as-is, do not assume 'www' if empty
        domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        netloc = f"{subdomain}.{domain}" if subdomain else domain

        # Normalize path: remove trailing slash unless it's the root '/'
        path = parsed_url.path
        if path == "/":
            path = ""

        # Reconstruct URL including the query string
        if query_string:
            url = f"{parsed_url.scheme}://{netloc}{path}?{query_string}"
        else:
            url = f"{parsed_url.scheme}://{netloc}{path}"

        return url

    def construct_full_domain(self):
        # Only include the subdomain if it exists
        website = (
            f"{self.extracted.domain}.{self.extracted.suffix}"
            if self.extracted.suffix
            else self.extracted.domain
        )
        full_domain = (
            f"{self.extracted.subdomain}.{website}" if self.extracted.subdomain else website
        )
        return full_domain

    def construct_path(self):
        path = self.parsed_url.path
        # Normalize path: remove trailing slash unless it's the root '/'
        if path == "/":
            path = ""
        elif path.endswith("/"):
            path = path.rstrip("/")

        query_params = parse_qs(self.parsed_url.query)
        query_params = {k: v for k, v in query_params.items() if v and v[0]}
        query_string = urlencode(query_params, doseq=True)

        if query_string:
            path += f"?{query_string}"

        return path

    def construct_unique_page_name(self):
        # Use the actual full domain without defaulting to 'www'
        combined = self.full_domain + self.path
        unique_page_name = re.sub(r"[^a-zA-Z0-9]", "_", combined)
        return unique_page_name

    def get_extension(self):
        # Extract path without fragment or query
        path = self.parsed_url.path
        extension = os.path.splitext(path)[1][1:]  # Extract extension without dot
        return extension if extension else None

    def get_metadata(self):
        return {
            "url": self.url,
            "website": self.website,
            "full_domain": self.full_domain,
            "subdomain": self.subdomain,  # This will be an empty string if no subdomain exists
            "path": self.path,
            "domain_type": self.domain_type,
            "unique_page_name": self.unique_page_name,
            "extension": self.extension,  # Add extension to the metadata
            "path_segments": [seg for seg in self.path.split("/") if seg.strip()],
        }


@lru_cache(maxsize=1000)
def get_metadata_by_url(url):
    return URLInfo(url).get_metadata()


def join_url(url, path):
    """
    Join the base URL with the provided path.
    """
    if url is None:
        return path

    if path is None:
        return url

    # Convert path to string if it's not already
    path = str(path).strip()

    # If path is empty, return the base URL
    if not path:
        return url

    # Check if path is already a complete URL
    if re.match(r"^(?:http|https|ftp|file)://", path):
        return path

    # Check if path is a data URL (including base64)
    if path.startswith("data:"):
        return path

    # Check if path is already an absolute URL with a different protocol
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", path):
        return path

    # Handle protocol-relative URLs (//example.com/path)
    if path.startswith("//") and not path.startswith("///"):
        parsed_base = urlparse(url)
        return f"{parsed_base.scheme}:{path}"

    # Normalize paths with multiple leading slashes (more than one, but not protocol-relative)
    if re.match(r"^/{3,}", path):
        path = "/" + path.lstrip("/")

    # Special handling for base URLs with multiple trailing slashes - ADD CHECK FOR URL NOT NONE
    if url is not None:  # This simple check fixes the error
        base_url_trailing_slashes = re.search(r"/{2,}$", url)
        if base_url_trailing_slashes and not path.startswith("/"):
            # For relative paths, preserve the extra slashes
            return url + path

    # Join the base URL with the path
    return urljoin(url, path)


def is_data_url(url):
    """
    Determines if a URL is a data URL, optionally checking if it's base64 encoded.

    Args:
        url (str): The URL to check.

    Returns:
        tuple: (is_data_url, is_base64)
            - is_data_url (bool): True if the URL is a data URL
            - is_base64 (bool): True if the data URL is base64 encoded
    """
    if url is None:
        return False, False

    # Convert to string and strip whitespace
    url = str(url).strip().lower()

    # Check if it's a data URL
    if not url.startswith("data:"):
        return False, False

    # Check if it's base64 encoded
    is_base64 = ";base64," in url

    return True, is_base64


import requests

verbose = True

# Registry mapping list names to their official URL and local file name.
LIST_REGISTRY = {
    "easylist": {
        "url": "https://easylist.to/easylist/easylist.txt",
        "local": "easylist-filters.txt",
    },
    "fanboy": {
        "url": "https://easylist.to/easylist/fanboy-annoyance.txt",
        "local": "fanboy-annoyance-filters.txt",
    },
}


class AdblockConfigLoader:
    _instance = None

    def __new__(cls, file_manager: FileManager):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, file_manager: FileManager):
        # Prevent reinitialization.
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.file_manager = file_manager
        self._configs = {}  # Cache: {list_key: config_content}
        self._initialized = True

    def load_config(self, list_key: str) -> str:
        """
        Load and cache the adblock configuration for the given list key.

        On the FIRST load for this list_key:
          - Always try to fetch from the official URL.
          - If fetching fails, fall back to a local file.
        On subsequent loads, return the previously cached content.
        """
        if list_key in self._configs:
            # Already loaded; return cached data
            return self._configs[list_key]

        if list_key not in LIST_REGISTRY:
            raise ValueError(f"List key '{list_key}' not found in registry")

        registry_entry = LIST_REGISTRY[list_key]
        local_file = registry_entry["local"]
        url = registry_entry["url"]

        content = ""
        try:
            # Attempt to fetch from the web first.
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                # Save it to temp so there's a copy on disk if needed later.
                self.file_manager.write_temp_text(local_file, content)
                vcprint(
                    f"Fetched and saved '{local_file}' successfully from URL.",
                    color="green",
                    verbose=verbose,
                )
            else:
                raise Exception(f"Failed to fetch file, status code {response.status_code}")
        except Exception as e:
            vcprint(
                f"Fetching from URL failed: {e}. Checking for local copy on disk.",
                color="light_yellow",
                verbose=verbose,
            )
            if self.file_manager.file_exists(root="temp", path=local_file):
                content = self.file_manager.read_temp_text(local_file)
                vcprint(
                    f"Loaded local copy of '{local_file}'.",
                    color="green",
                    verbose=verbose,
                )
            else:
                vcprint(
                    f"Local copy of '{local_file}' not found. No filters loaded.",
                    color="red",
                    verbose=verbose,
                )
                content = ""

        # Cache the result (even if empty), so subsequent loads skip the web/local steps
        self._configs[list_key] = content
        return content

    def load_configs(self, keys: str) -> list[str]:
        results = []
        for key in keys:
            results.append(self.load_config(key))
        return results


class DomainFilter:
    """
    A domain filter that can load and merge multiple adblock lists.
    It is a per-combination singleton:
      - If you request "easylist" alone multiple times, you'll get the same instance.
      - If you request ["easylist", "fanboy"], that is a separate instance –
        but also reused if requested again with the same set of keys.
    """

    _instances = {}  # {(frozenset_of_keys): DomainFilterInstance}

    def __new__(cls, list_keys, file_manager: FileManager = None):
        # Normalize list_keys to a list
        if isinstance(list_keys, str):
            list_keys = [list_keys]

        # Create a canonical key for our dictionary (using frozenset)
        key_set = frozenset(list_keys)

        if key_set not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key_set] = instance
        return cls._instances[key_set]

    def __init__(self, list_keys, file_manager: FileManager = None):
        # If already initialized, don't re-do it.
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Normalize list_keys
        if isinstance(list_keys, str):
            list_keys = [list_keys]

        self.file_manager = file_manager or FileManager("scraper")
        self.list_keys = list_keys
        self.blocked_domains = set()
        self.loaded_count = 0
        self.skipped_count = 0
        self._initialized = True

        self._load_filters()

    def _load_filters(self):
        """
        Loads all specified lists from the AdblockConfigLoader, processes their rules,
        and merges them into a single set of blocked domains.
        """
        loader = AdblockConfigLoader(self.file_manager)
        for list_key in self.list_keys:
            content = loader.load_config(list_key)
            for line in content.splitlines():
                self._process_rule(line.strip())

        vcprint(
            f"Created DomainFilter for lists: {', '.join(self.list_keys)}. "
            f"Loaded {self.loaded_count} rules, skipped {self.skipped_count}.",
            color="blue",
            verbose=verbose,
        )

    def _process_rule(self, rule: str):
        """Process a single adblock rule to extract the domain if it's a simple domain-block rule."""
        # Skip comments and empty lines
        if not rule or rule.startswith("!"):
            return
        # Skip element hiding rules
        if "##" in rule:
            return
        # Skip exception rules (starting with @@)
        if rule.startswith("@@"):
            return
        # Skip any rules with options ($)
        if "$" in rule:
            self.skipped_count += 1
            return
        # Process simple domain rules (e.g. ||example.com^)
        if rule.startswith("||") and "^" in rule:
            domain = rule[2 : rule.find("^")]
            # Skip invalid domains
            if not domain or "/" in domain or ":" in domain:
                self.skipped_count += 1
                return
            self.blocked_domains.add(domain)
            self.loaded_count += 1
        else:
            self.skipped_count += 1

    def should_block(self, url: str) -> bool:
        """Check if the given URL should be blocked based on the loaded domain rules."""
        try:
            domain = urlparse(url).netloc
            # Remove port if present
            if ":" in domain:
                domain = domain.split(":")[0]
            if not domain:
                return False
            # Direct domain match
            if domain in self.blocked_domains:
                return True
            # Check parent domains for subdomain matching
            parts = domain.split(".")
            for i in range(1, len(parts)):
                parent = ".".join(parts[i:])
                if parent in self.blocked_domains:
                    return True
            return False
        except Exception:
            return False
