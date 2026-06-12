from abstract_webtools.managers import *
import os, re, hashlib
from collections import deque
from urllib.parse import urlparse, urljoin, urldefrag

def get_abs_path():
    return os.path.abspath(__file__)

def get_abs_dir():
    abs_path = get_abs_path()
    return os.path.dirname(abs_path)
def join_abs_path(path):
    abs_dir = get_abs_dir()
    return os.path.join(abs_dir,path)
def get_rel_dir():
    return os.getcwd()
def join_rel_path(path):
    rel_dir = get_rel_dir()
    return os.path.join(rel_dir,path) 
# Import your custom classes/functions
# from your_module import linkManager, get_soup_mgr
def make_directory(directory=None,path=None):
    if directory==None:
        directory=os.getcwd()
    if path:
        directory = os.path.join(directory,path)
    os.makedirs(directory,exist_ok=True)
    return directory
def get_paths(*paths):
    all_paths = []
    for path in paths:
        all_paths+=path.split('/')
    return all_paths
def makeAllDirs(*paths):
    full_path= ''
    paths = get_paths(*paths)
    for i,path in enumerate(paths):
        if i == 0:
            full_path = path
            if not full_path.startswith('/'):
                full_path = join_rel_path(full_path)
        else:
            full_path = os.path.join(full_path,path)
        os.makedirs(full_path,exist_ok=True)
    return full_path
def currate_full_path(full_path):
    dirname = os.path.dirname(full_path)
    basename = os.path.basename(full_path)
    full_dirname = makeAllDirs(dirname)
    full_path = os.path.join(full_dirname,basename)
    return full_path
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
def get_save_page_path(url, output_dir):
    """
    Save HTML page to local directory.
    """
    parsed_url = urlparse(url)
    page_path = parsed_url.path.lstrip('/')

    if not page_path or page_path.endswith('/'):
        page_path = os.path.join(page_path, 'index.html')
    elif not os.path.splitext(page_path)[1]:
        page_path += '.html'

    page_full_path = os.path.join(output_dir, page_path)
    return page_full_path
def save_page(url, content,output_dir):
    page_full_path = get_save_page_path(url=url,
                                        output_dir=output_dir)
    page_full_path = currate_full_path(page_full_path)
    if page_full_path:
        dirname = os.path.dirname(page_full_path)
        

        with open(page_full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved page: {page_full_path}")
def get_asset_path(asset_url,
                   base_url,
                   output_dir,
                   downloaded_assets=None,
                   session=None):
    """
    Download and save assets like images, CSS, JS files.
    """
    # Use the managed session passed in; only fall back to a bare session when
    # none was provided (was unconditionally overwriting the managed session).
    session = session or requests.Session()
    downloaded_assets = downloaded_assets or set()
    asset_url = normalize_url(asset_url, base_url)
    if asset_url in list(downloaded_assets):
        return
    downloaded_assets.add(asset_url)

    parsed_url = urlparse(asset_url)
    asset_path = parsed_url.path.lstrip('/')
    if not asset_path:
        return  # Skip if asset path is empty

    asset_full_path = os.path.join(output_dir, asset_path)
    return asset_full_path
def save_asset(asset_url,
               base_url,
               output_dir,
               downloaded_assets=None,
               session=None):
   
    asset_full_path = get_asset_path(asset_url=asset_url,
                                     base_url=base_url,
                                     output_dir=output_dir,
                                     downloaded_assets=downloaded_assets,
                                     session=session)
    if asset_full_path:
        os.makedirs(os.path.dirname(asset_full_path), exist_ok=True)

        try:
            response = session.get(asset_url, stream=True)
   
            write_to_file(contents=response.text,file_path=asset_full_path)
            print(f"Saved asset: {asset_full_path}")
        except Exception as e:
            print(f"Failed to save asset {asset_url}: {e}")
        return downloaded_assets
class usurpManager():
    def __init__(self,url,output_dir=None,max_depth=None,wait_between_requests=None,operating_system=None, browser=None, version=None,user_agent=None,website_bot=None,
                 req_mgr=None, ua_mgr=None, url_mgr=None, mirror_external_assets=True):
        self.url = url
        website_bot = website_bot or 'http://yourwebsite.com/bot'
        # Reuse the shared request stack: it already owns the user agent, ciphers,
        # SSL/TLS adapter, proxies and cookies. Building our own bare
        # requests.Session() (as this used to) threw all of that away.
        self.req_mgr = req_mgr or get_req_mgr(url=url, url_mgr=url_mgr)
        self.url_mgr = self.req_mgr.url_mgr
        self.user_agent_mgr = ua_mgr or self.req_mgr.ua_mgr or get_ua_mgr(
            operating_system=operating_system, browser=browser, version=version, user_agent=user_agent)
        self.BASE_URL = self.url_mgr.url  # reuse the already-resolved url manager
        self.OUTPUT_DIR = output_dir or 'download_site'
        # Default: capture the WHOLE site — recurse every same-domain link with no
        # depth cap (the visited_pages set keeps this finite and loop-free). Pass
        # an int max_depth to limit how deep the crawl goes.
        self.MAX_DEPTH = max_depth  # None => unlimited
        self.WAIT_BETWEEN_REQUESTS = wait_between_requests or 1  # Seconds to wait between requests
        USER_AGENT = user_agent or self.req_mgr.user_agent or self.user_agent_mgr.get_user_agent()
        self.USER_AGENT = f"{USER_AGENT};{website_bot})"  # Customize as needed
        # Crawl scope: pages are mirrored only within this host; referenced assets
        # (css/js/img/fonts) may come from CDNs and are mirrored too so styles work.
        self.base_netloc = urlparse(self.BASE_URL).netloc
        self.mirror_external_assets = mirror_external_assets
        # Initialize global sets / maps
        self.visited_pages = set()
        self.downloaded_assets = set()
        # Single source of truth mapping absolute URL -> local file path, shared
        # across every page/css/asset so all references resolve consistently.
        self.url_map = {}

        # The managed session (configured by the request stack). We only layer the
        # crawler-specific identification header on top instead of replacing it.
        self.session = self.req_mgr.session
        self.session.headers.update({
            'User-Agent': self.USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.5',
            "Access-Control-Allow-Origin": "*"})

    # HTML attributes that carry a single URL.
    _URL_ATTRS = {
        'link': ['href'], 'script': ['src'], 'img': ['src'],
        'source': ['src'], 'video': ['src', 'poster'], 'audio': ['src'],
        'embed': ['src'], 'object': ['data'], 'input': ['src'], 'track': ['src'],
    }
    # HTML attributes that carry a comma-separated srcset list.
    _SRCSET_ATTRS = {'img': ['srcset'], 'source': ['srcset']}
    # Extensions we treat as crawlable HTML pages (anything else linked is an asset).
    _PAGE_EXTS = {'', '.html', '.htm', '.php', '.asp', '.aspx', '.jsp', '.xhtml'}
    _SKIP_SCHEMES = ('data:', 'mailto:', 'tel:', 'javascript:', 'blob:', 'about:', '#')

    # ------------------------------------------------------------------
    # path / reference helpers
    # ------------------------------------------------------------------
    def _local_path_for(self, url, is_page=False):
        """Deterministic local file path mirroring the URL's host + path.

        Same-host content lives under OUTPUT_DIR; cross-host assets under
        OUTPUT_DIR/_external/<host>/. Query strings are folded into the
        filename via a short hash so e.g. ``app.css?v=2`` doesn't clobber
        ``app.css``.
        """
        parsed = urlparse(url)
        rel = parsed.path.lstrip('/')
        if parsed.netloc and parsed.netloc != self.base_netloc:
            root = os.path.join(self.OUTPUT_DIR, '_external', parsed.netloc)
        else:
            root = self.OUTPUT_DIR

        if rel == '' or rel.endswith('/'):
            rel = rel + ('index.html' if is_page else 'index')
        base, ext = os.path.splitext(os.path.basename(rel))
        if is_page and ext.lower() not in self._PAGE_EXTS:
            rel = rel + '.html'
        elif is_page and not ext:
            rel = rel + '.html'

        if parsed.query:
            qhash = hashlib.md5(parsed.query.encode('utf-8')).hexdigest()[:8]
            dirn, bn = os.path.split(rel)
            b, e = os.path.splitext(bn)
            rel = os.path.join(dirn, f"{b}__{qhash}{e or ''}")

        return os.path.normpath(os.path.join(root, rel))

    @staticmethod
    def _rel_ref(from_local, to_local):
        """Relative href/src from one local file to another (posix separators)."""
        rel = os.path.relpath(to_local, start=os.path.dirname(from_local))
        return rel.replace(os.sep, '/')

    @staticmethod
    def _is_skippable(ref):
        ref = (ref or '').strip()
        if not ref:
            return True
        low = ref.lower()
        return any(low.startswith(s) for s in usurpManager._SKIP_SCHEMES)

    def _downloadable(self, abs_url):
        parsed = urlparse(abs_url)
        if parsed.scheme not in ('http', 'https'):
            return False
        if parsed.netloc != self.base_netloc and not self.mirror_external_assets:
            return False
        return True

    # ------------------------------------------------------------------
    # asset + css mirroring
    # ------------------------------------------------------------------
    def download_asset(self, abs_url):
        """Download an asset once, returning its local path. CSS is post-processed
        so its own ``url(...)`` / ``@import`` references are mirrored and rewritten.
        Returns None when the asset is out of scope / unfetchable."""
        abs_url, _frag = urldefrag(abs_url)
        if abs_url in self.url_map:
            return self.url_map[abs_url]
        if not self._downloadable(abs_url):
            return None

        local = self._local_path_for(abs_url, is_page=False)
        # Reserve the mapping up-front so cyclic CSS @imports don't recurse forever.
        self.url_map[abs_url] = local
        try:
            r = self.session.get(abs_url, stream=True, timeout=30)
            r.raise_for_status()
            os.makedirs(os.path.dirname(local), exist_ok=True)
            ctype = r.headers.get('Content-Type', '')
            if local.lower().endswith('.css') or 'text/css' in ctype:
                css = self.process_css(r.text, base_url=abs_url, css_local=local)
                with open(local, 'w', encoding='utf-8') as f:
                    f.write(css)
            else:
                with open(local, 'wb') as f:
                    for chunk in r.iter_content(8192):
                        if chunk:
                            f.write(chunk)
            self.downloaded_assets.add(abs_url)
            print(f"Saved asset: {local}")
        except Exception as e:
            print(f"Failed asset {abs_url}: {e}")
        return local

    def _localize_css_ref(self, ref, base_url, css_local):
        if self._is_skippable(ref):
            return ref
        abs_url = urljoin(base_url, ref)
        local = self.download_asset(abs_url)
        if not local:
            return ref
        return self._rel_ref(css_local, local)

    def process_css(self, css_text, base_url, css_local):
        """Mirror and rewrite every url(...) and @import in a stylesheet."""
        def _url(m):
            quote, ref = m.group(1), m.group(2)
            return f"url({quote}{self._localize_css_ref(ref, base_url, css_local)}{quote})"

        def _imp(m):
            quote, ref = m.group(1), m.group(2)
            return f"@import {quote}{self._localize_css_ref(ref, base_url, css_local)}{quote}"

        css_text = re.sub(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""", _url, css_text)
        css_text = re.sub(r"""@import\s+(['"])([^'"]+)\1""", _imp, css_text)
        return css_text

    def _localize_attr(self, abs_url, page_local):
        """Download a referenced asset and return its relative href from the page."""
        local = self.download_asset(abs_url)
        if not local:
            return None
        return self._rel_ref(page_local, local)

    def _rewrite_srcset(self, value, page_url, page_local):
        out = []
        for part in value.split(','):
            part = part.strip()
            if not part:
                continue
            bits = part.split(None, 1)
            ref = bits[0]
            descriptor = f" {bits[1]}" if len(bits) > 1 else ""
            if self._is_skippable(ref):
                out.append(part)
                continue
            rel = self._localize_attr(urljoin(page_url, ref), page_local)
            out.append(f"{rel or ref}{descriptor}")
        return ", ".join(out)

    # ------------------------------------------------------------------
    # page mirroring + crawl
    # ------------------------------------------------------------------
    def process_page(self, url, depth, base_domain=None):
        """Fetch one page, mirror every asset it references (rewriting each
        reference to a local relative path so the saved copy renders offline with
        styles intact), save it, and return the same-domain page links found.

        This processes a single page; ``crawl`` drives the recursion across the
        returned links.
        """
        base_domain = base_domain or self.base_netloc
        url, _frag = urldefrag(url)
        if url in self.visited_pages or (self.MAX_DEPTH is not None and depth > self.MAX_DEPTH):
            return []
        self.visited_pages.add(url)

        try:
            response = self.session.get(url, timeout=30)
        except Exception as e:
            print(f"Failed page {url}: {e}")
            return []
        soup = BeautifulSoup(response.text, "html.parser")  # single fetch, one soup

        page_local = self._local_path_for(url, is_page=True)
        self.url_map[url] = page_local  # so links from other pages resolve here

        # 1) Single-URL attributes (css, js, images, media, icons...).
        for tag in soup.find_all(list(self._URL_ATTRS.keys())):
            for attr in self._URL_ATTRS.get(tag.name, []):
                ref = tag.get(attr)
                if not ref or self._is_skippable(ref):
                    continue
                rel = self._localize_attr(urljoin(url, ref), page_local)
                if rel:
                    tag[attr] = rel

        # 2) Responsive srcset attributes.
        for tag in soup.find_all(list(self._SRCSET_ATTRS.keys())):
            for attr in self._SRCSET_ATTRS.get(tag.name, []):
                if tag.get(attr):
                    tag[attr] = self._rewrite_srcset(tag[attr], url, page_local)

        # 3) Inline style="" attributes and <style> blocks (background urls, fonts).
        for tag in soup.find_all(style=True):
            tag['style'] = self.process_css(tag['style'], base_url=url, css_local=page_local)
        for style_tag in soup.find_all('style'):
            if style_tag.string:
                style_tag.string.replace_with(
                    self.process_css(style_tag.string, base_url=url, css_local=page_local))

        # 4) Anchor links: same-domain pages get localized + queued; assets get
        #    downloaded; everything else is left absolute.
        page_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if self._is_skippable(href):
                continue
            abs_url, frag = urldefrag(urljoin(url, href))
            parsed = urlparse(abs_url)
            if parsed.netloc != base_domain:
                continue  # external site: leave the link as-is
            ext = os.path.splitext(parsed.path)[1].lower()
            if ext in self._PAGE_EXTS:
                link_local = self._local_path_for(abs_url, is_page=True)
                a['href'] = self._rel_ref(page_local, link_local) + (f"#{frag}" if frag else "")
                page_links.append(abs_url)
            else:
                rel = self._localize_attr(abs_url, page_local)
                if rel:
                    a['href'] = rel + (f"#{frag}" if frag else "")

        # Save the rewritten page at its mirrored location.
        os.makedirs(os.path.dirname(page_local), exist_ok=True)
        with open(page_local, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"Saved page: {page_local}")

        # Return the same-domain page links found here; the crawl driver
        # (``crawl``) walks them iteratively so an unbounded full-site capture
        # never risks Python's recursion limit on deep link chains.
        return page_links

    def crawl(self, start=None, base_domain=None):
        """Iteratively capture the site from ``start`` (default: the base URL).

        Breadth-first over same-domain page links; ``visited_pages`` keeps it
        finite and loop-free, and ``MAX_DEPTH`` (None by default => unlimited)
        bounds how deep it goes. Returns the crawl summary.
        """
        start = start or self.BASE_URL
        base_domain = base_domain or self.base_netloc
        queue = deque([(start, 0)])
        first = True
        while queue:
            url, depth = queue.popleft()
            url, _frag = urldefrag(url)
            if url in self.visited_pages:
                continue
            if self.MAX_DEPTH is not None and depth > self.MAX_DEPTH:
                continue
            if not first:
                time.sleep(self.WAIT_BETWEEN_REQUESTS)
            first = False
            for link_url in self.process_page(url, depth, base_domain):
                if link_url not in self.visited_pages and (
                        self.MAX_DEPTH is None or depth < self.MAX_DEPTH):
                    queue.append((link_url, depth + 1))
        return {'output_dir': self.OUTPUT_DIR,
                'pages': sorted(self.visited_pages),
                'assets': sorted(self.downloaded_assets)}

    def main(self):
        # Ensure output directory exists
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        summary = self.crawl(self.BASE_URL, self.base_netloc)
        print(f"Website copying completed: {len(self.visited_pages)} pages, "
              f"{len(self.downloaded_assets)} assets -> {self.OUTPUT_DIR}")
        return summary
def get_verified_mgr(url,
                     ua_mgr=None,
                     wait_between_requests=None,
                     operating_system=None,
                     browser=None,
                     version=None,
                     headers=None,
                     user_agent=None,
                     user_agent_manager=None,
                     ssl_manager=None,
                     tls_adapter=None,
                     proxies=None,
                     cookies=None,
                     ciphers=None,
                     certification=None,
                     ssl_options=None
                     ):
    blocked_markers = (
        'Please update your browser',
        'Bitte aktualisiere deinen BrowserDein Browser',
        'browser is no longer supported',
    )
    max_attempts = 5
    for _ in range(max_attempts):
        # Regenerate the user agent on every attempt. Previously a single ua_mgr
        # was built once outside the loop, so a blocked page looped forever
        # retrying with the exact same (rejected) user agent.
        attempt_ua = ua_mgr or get_ua_mgr(
            randomAll=True,
            user_agent=user_agent,
            browser=browser,
            version=version,
            operating_system=operating_system,
            )
        req_mgr = requestManager(
             url=url,
             ua_mgr=attempt_ua,
             headers=attempt_ua.generate_headers(),
             ssl_manager=ssl_manager,
             tls_adapter=tls_adapter,
             user_agent=user_agent,
             proxies=proxies,
             cookies=cookies,
             ciphers=ciphers,
             certification=certification,
             ssl_options=ssl_options
             )
        # Reuse the req_mgr's already-fetched source; soupManager won't re-fetch.
        soup_mgr = soupManager(req_mgr=req_mgr)
        text = soup_mgr.soup.text
        if not any(marker in text for marker in blocked_markers):
            return soup_mgr
        # A fixed ua_mgr can't be re-rolled; drop it so the next attempt randomizes.
        ua_mgr = None
    return soup_mgr
def usurpit( url,
             output_dir=None,
             max_depth=None,
             wait_between_requests=None,
             browser=None,
             version=None,
             website_bot=None,
             ua_mgr=None,
             headers=None,
             operating_system=None,
             user_agent=None,
             ssl_manager=None,
             tls_adapter=None,
             proxies=None,
             cookies=None,
             ciphers=None,
             certification=None,
             ssl_options=None):
    soup_mgr = get_verified_mgr(
        url=url,
            user_agent=user_agent,
            browser=browser,
            version=version,
            operating_system=operating_system,
             ua_mgr=ua_mgr,
             headers=headers,
             ssl_manager=ssl_manager,
             tls_adapter=tls_adapter,
             proxies=proxies,
             cookies=cookies,
             ciphers=ciphers,
             certification=certification,
             ssl_options=ssl_options)
    output_dir = output_dir or get_domain_name_from_url(url) or make_directory(path='usurped')
    # Hand the verified req_mgr (and its configured session / ua_mgr) straight to
    # usurpManager instead of passing scalar strings and rebuilding from scratch.
    site_mgr = usurpManager(url,
                            output_dir=output_dir,
                            max_depth=max_depth,
                            wait_between_requests=wait_between_requests,
                            req_mgr=soup_mgr.req_mgr,
                            ua_mgr=soup_mgr.req_mgr.ua_mgr,
                            browser=browser,
                            version=version,
                            user_agent=soup_mgr.req_mgr.user_agent,
                            website_bot=website_bot,
                            )
    site_mgr.main()



