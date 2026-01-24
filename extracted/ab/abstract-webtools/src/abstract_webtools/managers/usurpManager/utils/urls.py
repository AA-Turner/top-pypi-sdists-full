from .imports import *
from .paths import *
# Import your custom classes/functions
# from your_module import linkManager, get_soup_mgr
def get_domain_name_from_url(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    parsed_spl = netloc.split('.')
    directory_name = '.'.join(parsed_spl[:-1])
    if directory_name.startswith('www.'):
        directory_name = directory_name[len('www.'):]
    return directory_name
def get_domain_directory_from_url(url,base_dir=None):
    base_dir =base_dir or os.getcwd()
    domain_name = get_domain_name_from_url(url)
    return make_directory(directory,domain_name)
# Configuration
def normalize_url(url, base_url):
    """
    Normalize and resolve relative URLs, ensuring proper domain and format.
    """
    # If URL starts with the base URL repeated, remove the extra part
    if url.startswith(base_url):
        url = url[len(base_url):]

    # Resolve the URL against the base URL
    normalized_url = urljoin(base_url, url.split('#')[0])

    # Ensure only URLs belonging to the base domain are kept
    if not normalized_url.startswith(base_url):
        return None

    return normalized_url


def is_valid_url(url, base_domain):
    """
    Check if the URL is valid and belongs to the same domain.
    """
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and parsed.netloc == base_domain
