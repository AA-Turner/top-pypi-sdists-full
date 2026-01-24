from abstract_webtools.managers.videoDownloader import *
from abstract_webtools import *

from urllib.parse import urlparse, urljoin
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time
# --- Cookie normalizer ---
def normalize_cookies(cookies):
    """
    Normalize cookies into {name: str(value)} format.
    Handles dicts, nested dicts, and RequestsCookieJar.
    """
    normalized = {}
    if not cookies:
        logger.debug("No cookies provided.")
        return normalized

    if isinstance(cookies, dict):
        for k, v in cookies.items():
            if isinstance(v, dict):
                logger.warning(f"Cookie '{k}' is a dict, flattening with .get('value')")
                v = v.get("value") or str(v)
            if not isinstance(v, (str, bytes)):
                logger.warning(f"Cookie '{k}' is {type(v)}, coercing: {v!r}")
                v = str(v)
            normalized[str(k)] = v

    elif isinstance(cookies, requests.cookies.RequestsCookieJar):
        for c in cookies:
            v = c.value
            if not isinstance(v, (str, bytes)):
                logger.warning(f"Cookie '{c.name}' had non-string value {type(c.value)}, coercing: {v!r}")
                v = str(v)
            normalized[c.name] = v

    else:
        logger.error(f"Unexpected cookie container: {type(cookies)}")

    return normalized
class requestManager:
    """
    requestManager is a class for making HTTP requests with error handling and retries.
    It supports initializing with a provided source_code without requiring a URL.
    If source_code is provided, it uses that as the response content and skips fetching.
    Enhanced to parse source_code for URLs, PHP blocks, and React/JS data even if not HTML.
    Args:
        url (str or None): The URL to make requests to (default is None).
        url_mgr (urlManager or None): An instance of urlManager (default is None).
        network_manager (NetworkManager or None): An instance of NetworkManager (default is None).
        user_agent_manager (UserAgentManager or None): An instance of UserAgentManager (default is None).
        ssl_manager (SSlManager or None): An instance of SSLManager (default is None).
        tls_adapter (TLSAdapter or None): An instance of TLSAdapter (default is None).
        user_agent (str or None): The user agent string to use for requests (default is None).
        proxies (dict or None): Proxy settings for requests (default is None).
        headers (dict or None): Additional headers for requests (default is None).
        cookies (dict or None): Cookie settings for requests (default is None).
        session (requests.Session or None): A custom requests session (default is None).
        adapter (str or None): A custom adapter for requests (default is None).
        protocol (str or None): The protocol to use for requests (default is 'https://').
        ciphers (str or None): Cipher settings for requests (default is None).
        auth (tuple or None): Authentication credentials (default is None).
        login_url (str or None): The URL for authentication (default is None).
        email (str or None): Email for authentication (default is None).
        password (str or None): Password for authentication (default is None).
        certification (str or None): Certification settings for requests (default is None).
        ssl_options (str or None): SSL options for requests (default is None).
        stream (bool): Whether to stream the response content (default is False).
        timeout (float or None): Timeout for requests (default is None).
        last_request_time (float or None): Timestamp of the last request (default is None).
        max_retries (int or None): Maximum number of retries for requests (default is None).
        request_wait_limit (float or None): Wait time between requests (default is None).

    Methods:
        update_url_mgr(url_mgr): Update the URL manager and reinitialize the SafeRequest.
        update_url(url): Update the URL and reinitialize the SafeRequest.
        re_initialize(): Reinitialize the SafeRequest with the current settings.
        authenticate(s, login_url=None, email=None, password=None, checkbox=None, dropdown=None): Authenticate and make a request.
        fetch_response(): Fetch the response from the server.
        initialize_session(): Initialize the requests session with custom settings.
        process_response_data(): Process the fetched response data.
        get_react_source_code(): Extract JavaScript and JSX source code from <script> tags.
        get_status(url=None): Get the HTTP status code of a URL.
        wait_between_requests(): Wait between requests based on the request_wait_limit.
        make_request(): Make a request and handle potential errors.
        try_request(): Try to make an HTTP request using the provided session.

    Note:
        - The SafeRequest class is designed for making HTTP requests with error handling and retries.
        - It provides methods for authentication, response handling, and error management.
    """

    def __init__(self, url=None, source_code=None, url_mgr=None, network_manager=None,
                 ua_mgr=None, ssl_manager=None, ssl_options=None, tls_adapter=None,
                 user_agent=None, proxies=None, headers=None, cookies=None, session=None,
                 adapter=None, protocol=None, ciphers=None, spec_login=False,
                 login_referer=None, login_user_agent=None, auth=None, login_url=None,
                 email=None, password=None, checkbox=None, dropdown=None,
                 certification=None, stream=False, timeout=None, last_request_time=None,
                 max_retries=None, request_wait_limit=None):

        self.url_mgr = get_url_mgr(url=url, url_mgr=url_mgr)
        self.url = get_url(url=url, url_mgr=self.url_mgr)

        # UA/headers
        self.ua_mgr = ua_mgr or get_ua_mgr(user_agent=user_agent)
        self.user_agent = self.ua_mgr.user_agent
        # generate realistic headers tied to this URL
        self.headers = headers or self.ua_mgr.generate_for_url(self.url)

        # TLS / SSL / Network
        self.ciphers = ciphers or CipherManager().ciphers_string
        self.certification = certification
        self.ssl_manager = ssl_manager or SSLManager(ciphers=self.ciphers)
        self.tls_adapter = tls_adapter or TLSAdapter(ssl_manager=self.ssl_manager, certification=self.certification)
        self.network_manager = network_manager or NetworkManager(
            user_agent_manager=self.ua_mgr,
            ssl_manager=self.ssl_manager,
            tls_adapter=self.tls_adapter,
            user_agent=user_agent,
            proxies=proxies,
            cookies=cookies,
            ciphers=ciphers,
            certification=certification,
            ssl_options=ssl_options
        )

        # Session
        self.session = session or requests.Session()
        self.session.proxies = self.network_manager.proxies
        self.session.headers.update(self.headers)
        self.session.mount("https://", self.network_manager.tls_adapter)
        self.session.mount("http://", HTTPAdapter())
        if auth:
            self.session.auth = auth

        self.protocol = protocol or 'https://'
        self.timeout = timeout
        self.auth = auth
        self.spec_login = spec_login
        self.email = email
        self.password = password
        self.checkbox = checkbox
        self.dropdown = dropdown
        self.login_url = login_url
        self.login_user_agent = login_user_agent
        self.login_referer = login_referer
        self.stream = bool(stream)

        self.last_request_time = last_request_time
        self.max_retries = max_retries or 3
        self.request_wait_limit = request_wait_limit or 1.5

        # Response placeholders ...
        self._response = None
        self.status_code = None
        self.source_code = None
        self.source_code_bytes = None
        self.source_code_json = {}
        self.react_source_code = []
        self.extracted_urls = []
        self.php_blocks = []
        self._response_data = None

        if source_code is not None:
            self._response = source_code
            self.process_response_data()
        else:
            self.re_initialize()


    def update_url_mgr(self, url_mgr):
        self.url_mgr = url_mgr
        self.re_initialize()

    def update_url(self, url):
        self.url_mgr.update_url(url=url)
        self.re_initialize()

    # --- re_initialize, update_url_mgr, update_url unchanged except: ---
    def re_initialize(self):
        print("bef_re_initialize")
        self._response = None
        if self.url_mgr.url is not None:
            self.make_request()
        
        self.source_code = None
        self.source_code_bytes = None
        self.source_code_json = {}
        self.react_source_code = []
        self.extracted_urls = []
        self.php_blocks = []
        self._response_data = None
        print("bef_process_response_data")
        self.process_response_data()


    @property
    def response(self):
        if self._response is None and self.url_mgr.url is not None:
            self._response = self.fetch_response()
        return self._response


    def authenticate(self, session, login_url=None, email=None, password=None, checkbox=None, dropdown=None):
        login_urls = login_url or [self.url_mgr.url, self.url_mgr.domain, self.url_mgr.url_join(url=self.url_mgr.domain, path='login'), self.url_mgr.url_join(url=self.url_mgr.domain, path='auth')]
        s = session
        if not isinstance(login_urls, list):
            login_urls = [login_urls]
        for login_url in login_urls:
            login_url_mgr = urlManager(login_url)
            login_url = login_url_mgr.url
            r = s.get(login_url)
            soup = BeautifulSoup(r.content, "html.parser")
            # Find the token or any CSRF protection token
            token = soup.find('input', {'name': 'token'}).get('value') if soup.find('input', {'name': 'token'}) else None
            if token is not None:
                break
        login_data = {}
        if email is not None:
            login_data['email'] = email
        if password is not None:
            login_data['password'] = password
        if checkbox is not None:
            login_data['checkbox'] = checkbox
        if dropdown is not None:
            login_data['dropdown'] = dropdown
        if token is not None:
            login_data['token'] = token
        s.post(login_url, data=login_data)
        return s

    def fetch_response(self) -> requests.Response | None | str | bytes:
        """Actually fetches the response from the server."""
        return self.try_request()

    def spec_auth(self, session=None, email=None, password=None, login_url=None, login_referer=None, login_user_agent=None):
        s = session or requests.Session()
        domain = self.url_mgr.url_join(self.url_mgr.get_correct_url(self.url_mgr.domain), 'login') if login_url is None else login_url
        login_url = self.url_mgr.get_correct_url(url=domain)
        login_referer = login_referer or self.url_mgr.url_join(url=login_url, path='?role=fast&to=&s=1&m=1&email=YOUR_EMAIL')
        login_user_agent = login_user_agent or 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'
        headers = {"Referer": login_referer, 'User-Agent': login_user_agent}
        payload = {'email': email, 'pass': password}
        page = s.get(login_url)
        soup = BeautifulSoup(page.content, 'lxml')
        action_url = soup.find('form')['action']
        s.post(action_url, data=payload, headers=headers)
        return s

    def initialize_session(self):
        # Already done in __init__; keep for API compatibility
        return self.session


    def process_response_data(self):
        """Processes the fetched response data."""
        if not self.response:
            return  # No data to process
        if isinstance(self.response, (str, bytes)):
            if isinstance(self.response, str):
                self.source_code = self.response
                print("bef_source_code_bytes_1")
                self.source_code_bytes = self.response.encode('utf-8')  # Assume UTF-8
            else:
                print("bef_source_code_bytes_2")
                self.source_code_bytes = self.response
                try:
                    print("bef_source_code_2_1")
                    self.source_code = self.response.decode('utf-8')
                except UnicodeDecodeError:
                    print("bef_source_code_2_1")
                    self.source_code = self.response.decode('latin-1')  # Fallback
            # Check if it's JSON
            try:
                print("bef_json.loads(self.source_code)")
                data = json.loads(self.source_code)
                print("bef_source_code_json")
                self.source_code_json = data.get("response", data)
            except json.JSONDecodeError:
                pass
        else:
            print("bef_self.response.text")
            self.source_code = self.response.text
            self.source_code_bytes = self.response.content
            print("bef_self.response.headers")
            if self.response.headers.get('content-type', '').startswith('application/json'):
                try:
                    data = json.loads(self.source_code)
                    self.source_code_json = data.get("response", data)
                except json.JSONDecodeError:
                    pass
        print("bef_extract_urls")
        self.extract_urls()
        print("bef_extract_php_blocks")
        self.extract_php_blocks()
        print("bef_get_react_source_code")
        self.get_react_source_code()

    def extract_urls(self):
        """Extract URLs from source_code using regex."""
        if not self.source_code:
            return
        url_pattern = r'https?://[^\s<>"\']+'
        self.extracted_urls = re.findall(url_pattern, self.source_code)

    def extract_php_blocks(self):
        """Extract PHP blocks from source_code if present."""
        if not self.source_code:
            return
        php_pattern = r'<\?php(.*?)?\?>'
        self.php_blocks = re.findall(php_pattern, self.source_code, re.DOTALL)

    def get_react_source_code(self) -> list:
        """
        Extracts JavaScript and JSX source code from <script> tags if HTML-like.
        If not HTML and looks like JS/React code, appends the whole source_code.
        """
        if not self.source_code:
            return []
        # Check if likely JS code (e.g., contains 'import', 'function', 'React')
        is_js_like = any(keyword in self.source_code.lower() for keyword in ['import ', 'function ', 'react', 'export ', 'const ', 'let ', 'var '])
        # Check if HTML-like
        print("bef_get_react_source_code")
        is_html_like = self.source_code.strip().startswith('<') or '<html' in self.source_code.lower() or '<!doctype' in self.source_code.lower()
        if not is_html_like and is_js_like:
            print("bef_self.react_source_code6")
            self.react_source_code.append(self.source_code)
            return self.react_source_code
        print("bef_self.source_code_bytes")
        content = self.source_code_bytes or self.source_code.encode('utf-8')
        print("bef_BeautifulSoup(content, html.parser)")
        print(content)
        soup = get_beautifil_soup(content, "html.parser")
        print("aft_BeautifulSoup(content, html.parser)")
        print("bef_soup.find_all")
        script_tags = soup.find_all('script', type=lambda t: t and ('javascript' in t.lower() or 'jsx' in t.lower()))
        for script_tag in script_tags:
            if script_tag.string:
                print("bef_react_source_code_1")
                self.react_source_code.append(script_tag.string)
        # If no scripts found but JS-like, append whole
        if not script_tags and is_js_like:
            print("bef_react_source_code_2")
            self.react_source_code.append(self.source_code)
        print("bef_source_code_over")
        return self.react_source_code

    def initialize_session(self):
        # Already done in __init__; keep for API compatibility
        return self.session

    def fetch_response(self):
        return self.try_request()

    def get_status(self, url: str = None) -> int | None:
        url = url or self.url_mgr.url
        if url is None:
            return None
        try:
            r = self.session.head(url, timeout=5)
            return r.status_code
        except requests.RequestException:
            return None

    def wait_between_requests(self):
        if self.last_request_time:
            sleep_time = self.request_wait_limit - (time.time() - self.last_request_time)
            if sleep_time > 0:
                logger.info("Sleeping for %.2f seconds.", sleep_time)
                time.sleep(sleep_time)

    def make_request(self):
        if self.url_mgr.url is None:
            return None
        self.wait_between_requests()
        for _ in range(self.max_retries):
            try:
                self._response = self.try_request()
                if self._response:
                    if not isinstance(self._response, (str, bytes)):
                        self.status_code = self._response.status_code
                        if self.status_code == 200:
                            self.last_request_time = time.time()
                            return self._response
                        if self.status_code == 429:
                            logger.warning("429 from %s. Retrying...", self.url_mgr.url)
                            time.sleep(5)
                    else:
                        self.status_code = 200
                        return self._response
            except requests.Timeout as e:
                logger.error("Timeout %s: %s", self.url_mgr.url, e)
            except requests.ConnectionError:
                logger.error("Connection error %s", self.url_mgr.url)
            except requests.RequestException as e:
                logger.error("Request exception %s: %s", self.url_mgr.url, e)
        logger.error("Failed to retrieve content from %s after %d retries", self.url_mgr.url, self.max_retries)
        return None

    def try_request(self) -> requests.Response | str | bytes | None:
        """
        Tries Selenium first, then falls back to requests if Selenium fails.
        """
        if self.url_mgr.url is None:
            return None

        # 1. Try Selenium
        try:
            return get_selenium_source(self.url_mgr.url)
        except Exception as e:
            logging.warning(f"Selenium failed for {self.url_mgr.url}, falling back to requests: {e}")

        # 2. Fallback: requests
        try:
            resp = self.session.get(
                self.url_mgr.url,
                timeout=self.timeout or 10,
                stream=self.stream
            )
            return resp
        except requests.RequestException as e:
            logging.error(f"Requests fallback also failed for {self.url_mgr.url}: {e}")
            return None
    @property
    def url(self):
        return self.url_mgr.url

    @url.setter
    def url(self, new_url):
        if self.url_mgr:
            self.url_mgr.update_url(new_url)
        else:
            self.url_mgr = urlManager(new_url)
class SafeRequestSingleton:
    _instance = None
    @staticmethod
    def get_instance(url=None,headers:dict=None,max_retries=3,last_request_time=None,request_wait_limit=1.5):
        if SafeRequestSingleton._instance is None:
            SafeRequestSingleton._instance = SafeRequest(url,url_mgr=urlManagerSingleton,headers=headers,max_retries=max_retries,last_request_time=last_request_time,request_wait_limit=request_wait_limit)
        elif SafeRequestSingleton._instance.url != url or SafeRequestSingleton._instance.headers != headers or SafeRequestSingleton._instance.max_retries != max_retries or SafeRequestSingleton._instance.request_wait_limit != request_wait_limit:
            SafeRequestSingleton._instance = SafeRequest(url,url_mgr=urlManagerSingleton,headers=headers,max_retries=max_retries,last_request_time=last_request_time,request_wait_limit=request_wait_limit)
        return SafeRequestSingleton._instance
def get_source(url=None,url_mgr=None,source_code=None,req_mgr=None):
    req_mgr = get_req_mgr(req_mgr=req_mgr,url=url,url_mgr=url_mgr,source_code=source_code)
    return req_mgr.source_code
def get_req_mgr(url=None,url_mgr=None,source_code=None,req_mgr=None):
    
    url = get_url(url=url,url_mgr=url_mgr)
    
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr )
    
    req_mgr = req_mgr  or requestManager(url_mgr=url_mgr,url=url,source_code=source_code)
    input('aft_req_mgr')
    return req_mgr
class SitemapGenerator:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.visited = set()  # Track visited URLs
        self.sitemap_data = {}  # Store URL metadata including images and documents

    def crawl(self, url, max_depth=3, depth=1):
        """Recursively crawl website and collect internal URLs, images, and documents."""
        if depth > max_depth or url in self.visited:
            return

        print(f"Crawling: {url}")
        self.visited.add(url)

        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                soup = get_all_attribute_values(url)
                input(soup)
                # Initialize data storage for this URL
                self.sitemap_data[url] = {
                    'images': [],
                    'documents': [],
                    'changefreq': 'weekly',
                    'priority': '0.5',
                    'lastmod': time.strftime('%Y-%m-%d')
                }

                # Extract images
                images = [img.get('src') for img in soup.find_all('img', src=True)]
                images = [urljoin(url, img) for img in images]
                images = [img for img in images if self.is_internal_url(img)]
                self.sitemap_data[url]['images'].extend(images)

                # Extract documents (e.g., PDFs, DOCs)
                documents = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if self.is_internal_url(full_url):
                        if any(full_url.endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                            documents.append(full_url)
                        else:
                            if full_url not in self.visited:
                                self.crawl(full_url, max_depth, depth + 1)
                self.sitemap_data[url]['documents'].extend(documents)

                # Extract and crawl internal links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if self.is_internal_url(full_url) and full_url not in self.visited:
                        self.crawl(full_url, max_depth, depth + 1)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def is_internal_url(self, url):
        """Check if URL is within the same domain."""
        parsed_url = urlparse(url)
        base_parsed_url = urlparse(self.base_url)
        return (parsed_url.netloc == base_parsed_url.netloc or parsed_url.netloc == '') and not parsed_url.scheme.startswith('mailto')

    def generate_sitemap_xml(self):
        """Generate XML for the sitemap including URLs, images, and documents."""
        NSMAP = {
            None: "http://www.sitemaps.org/schemas/sitemap/0.9",
            'image': "http://www.google.com/schemas/sitemap-image/1.1"
        }
        urlset = ET.Element("urlset", xmlns=NSMAP[None], attrib={'xmlns:image': NSMAP['image']})

        for url, data in self.sitemap_data.items():
            url_element = ET.SubElement(urlset, "url")
            ET.SubElement(url_element, "loc").text = url
            ET.SubElement(url_element, "lastmod").text = data['lastmod']
            ET.SubElement(url_element, "changefreq").text = data['changefreq']
            ET.SubElement(url_element, "priority").text = data['priority']

            # Add images
            for img_url in data['images']:
                image_element = ET.SubElement(url_element, "{http://www.google.com/schemas/sitemap-image/1.1}image")
                ET.SubElement(image_element, "{http://www.google.com/schemas/sitemap-image/1.1}loc").text = img_url

            # Add documents as separate URLs
            for doc_url in data['documents']:
                doc_element = ET.SubElement(urlset, "url")
                ET.SubElement(doc_element, "loc").text = doc_url
                ET.SubElement(doc_element, "lastmod").text = data['lastmod']
                ET.SubElement(doc_element, "changefreq").text = data['changefreq']
                ET.SubElement(doc_element, "priority").text = data['priority']

        # Write to sitemap.xml
        tree = ET.ElementTree(urlset)
        tree.write("sitemap.xml", encoding="utf-8", xml_declaration=True)
        print("Sitemap generated and saved as sitemap.xml")

    def run(self):
        """Run the sitemap generator."""
        self.crawl(self.base_url)
        self.generate_sitemap_xml()



class crawlManager:
    def __init__(self, url, req_mgr, url_mgr, source_code=None, parse_type="html.parser"):
        self.url_mgr = url_mgr
        self.req_mgr = req_mgr
        self.url = url
        self.parse_type = parse_type
        self.source_code = source_code or req_mgr.source_code
        self.soup = BeautifulSoup(self.source_code or "", parse_type)
        self.base_netloc = urlparse(self.url).netloc

    def is_internal(self, link):
        u = urlparse(link)
        return (not u.netloc) or (u.netloc == self.base_netloc)

    def links_on_page(self):
        out = set()
        for a in self.soup.find_all("a", href=True):
            out.add(urljoin(self.url, a["href"]))
        return out

    def crawl(self,url=None, start=None, max_depth=2, _depth=0, visited=None, session=None):
        start = url or start or self.url
        visited = visited or set()
        if _depth > max_depth or start in visited:
            return visited
        visited.add(start)

        # fetch
        r = self.req_mgr.session.get(start, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, self.parse_type)

        for a in soup.find_all("a", href=True):
            link = urljoin(start, a["href"])
            if self.is_internal(link) and link not in visited:
                self.crawl(link, max_depth=max_depth, _depth=_depth+1, visited=visited)
        return visited
    def get_new_source_and_url(self, url=None):
        """Fetches new source code and response for a given URL."""
        url = url
        self.req_mgr = get_req_mgr(url=url)
        self.source_code = self.req_mgr.source_code
        self.response = self.req_mgr.response

    def get_classes_and_meta_info(self):
        """Returns unique classes and image links from meta tags."""
        tag_name = 'meta'
        class_name_1, class_name_2 = 'class', 'property'
        class_value = 'og:image'
        attrs = ['href', 'src']
        unique_classes, images = discover_classes_and_images(self, tag_name, class_name_1, class_name_2, class_value, attrs)
        return unique_classes, images

    def extract_links_from_url(self, url=None):
        """Extracts all href and src links from a given URL's source code."""
        url = url or self.url_mgr.url
        soup = BeautifulSoup(self.source_code, self.parse_type)
        links = {'images': [], 'external_links': []}

        if self.response:
            for attr in ['href', 'src']:
                for tag in soup.find_all(attrs={attr: True}):
                    link = tag.get(attr)
                    if link:
                        absolute_link = urljoin(url, link)
                        if link.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                            links['images'].append(absolute_link)
                        elif urlparse(absolute_link).netloc != urlparse(url).netloc:
                            links['external_links'].append(absolute_link)
        
        return links

    def get_all_website_links(self):
        """Finds all internal links on the website that belong to the same domain."""
        all_urls = [self.url_mgr.url]
        domain = self.url_mgr.domain
        all_attribs = self.extract_links_from_url(self.url_mgr.url)
        
        for href in all_attribs.get('href', []):
            if not href or not self.url_mgr.is_valid_url(href):
                continue
            full_url = urljoin(self.url_mgr.url, href)
            if domain in full_url and full_url not in all_urls:
                all_urls.append(full_url)
        
        return all_urls

    def correct_xml(self, xml_string):
        """Corrects XML by encoding special characters in <image:loc> tags."""
        root = ET.fromstring(xml_string)
        for image_loc in root.findall(".//image:loc", namespaces={'image': 'http://www.google.com/schemas/sitemap-image/1.1'}):
            if '&' in image_loc.text:
                image_loc.text = image_loc.text.replace('&', '&amp;')
        return ET.tostring(root, encoding='utf-8').decode('utf-8')

    def determine_values(self, url=None):
        """Determines frequency and priority based on URL type."""
        url = url or self.url
        if 'blog' in url:
            return ('weekly', '0.8') if '2023' in url else ('monthly', '0.6')
        elif 'contact' in url:
            return ('yearly', '0.3')
        return ('weekly', '1.0')

  
    def get_meta_info(self, url=None):
        """Fetches metadata, including title and meta tags, from the page."""
        url = url or self.url
        soup = BeautifulSoup(self.source_code, self.parse_type)
        meta_info = {"title": None, "meta_tags": {}}
        
        title_tag = soup.find("title")
        if title_tag:
            meta_info["title"] = title_tag.text

        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            if name and content:
                meta_info["meta_tags"][name] = content

        return meta_info

    def generate_sitemap(self,url=None):
        """Generates a sitemap.xml file with URLs, images, change frequency, and priority."""
        url = url or self.url
        urls = self.get_all_website_links()
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" ')
            f.write('xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n')

            for url in urls:
                f.write(f'  <url>\n    <loc>{url}</loc>\n')
                frequency, priority = self.determine_values(url)
                f.write(f'    <changefreq>{frequency}</changefreq>\n')
                f.write(f'    <priority>{priority}</priority>\n')

                images = [img for img in self.extract_links_from_url(url)['images']]
                for img in images:
                    escaped_img = img.replace('&', '&amp;')
                    f.write(f'    <image:image>\n      <image:loc>{escaped_img}</image:loc>\n    </image:image>\n')

                f.write('  </url>\n')

            f.write('</urlset>\n')
        
        print(f'Sitemap saved to sitemap.xml with {len(urls)} URLs.')

class crawlManagerSingleton():
    _instance = None
    @staticmethod
    def get_instance(url=None,source_code=None,parse_type="html.parser"):
        if crawlManagerSingleton._instance is None:
            crawlManagerSingleton._instance = CrawlManager(url=url,parse_type=parse_type,source_code=source_code)
        elif parse_type != crawlManagerSingleton._instance.parse_type or url != crawlManagerSingleton._instance.url  or source_code != crawlManagerSingleton._instance.source_code:
            crawlManagerSingleton._instance = CrawlManager(url=url,parse_type=parse_type,source_code=source_code)
        return crawlManagerSingleton._instance
def get_crawl_mgr(url=None,req_mgr=None,url_mgr=None,source_code=None,parse_type="html.parser"):
    
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
    url = get_url(url=url,url_mgr=url_mgr)
    req_mgr=get_req_mgr(url=url,url_mgr=url_mgr,source_code=source_code)
    source_code = get_source(url=url,url_mgr=url_mgr,source_code=source_code)
    soup_mgr = get_soup_mgr(url=url,url_mgr=url_mgr,source_code=source_code,req_mgr=req_mgr,parse_type=parse_type)
    crawl_mgr = crawlManager(url=url,req_mgr=req_mgr,url_mgr=url_mgr,source_code=source_code,parse_type=parse_type)
    return crawl_mgr
def get_domain_crawl(url=None,req_mgr=None,url_mgr=None,source_code=None,parse_type="html.parser",max_depth=3, depth=1):
    crawl_mgr = get_crawl_mgr(url=url,req_mgr=req_mgr,url_mgr=url_mgr,source_code=source_code,parse_type=parse_type)
    url = get_url(url=url,url_mgr=url_mgr)
    all_domain_links = crawl_mgr.crawl(url=url, max_depth=max_depth, _depth=depth)
    return all_domain_links
##url = "https://www.youtube.com/watch?v=ckM_TklU_AQ"
####source_code = read_from_file('source_code.txt')
####
####
####soup = BeautifulSoup(source_code, "html.parser")
####input(soup)
##sel_mgr = seleneumManager(url)
##
##sel_mgr = get_domain_crawl(url)
##input(sel_mgr)
##
##
##input(linkManager(url).find_all_desired())
