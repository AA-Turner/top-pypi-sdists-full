from abstract_webtools import *

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
        directory = os.path.join(base_dir,path)
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
    session=requests.Session()
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
            response.raise_for_status()
            with open(asset_full_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Saved asset: {asset_full_path}")
        except Exception as e:
            print(f"Failed to save asset {asset_url}: {e}")
        return downloaded_assets
class usurpManager():
    def __init__(self,url,output_dir=None,max_depth=None,wait_between_requests=None,operating_system=None, browser=None, version=None,user_agent=None,website_bot=None):
        self.url = url
        website_bot = website_bot or 'http://yourwebsite.com/bot'
        self.user_agent_mgr = UserAgentManager(operating_system=operating_system,browser=browser,version=version,user_agent=user_agent)
        self.BASE_URL = urlManager(url=self.url).url  # Replace with your website's URL
        self.OUTPUT_DIR = output_dir or 'download_site'
        self.MAX_DEPTH = max_depth or 5  # Adjust as needed
        self.WAIT_BETWEEN_REQUESTS = wait_between_requests or 1  # Seconds to wait between requests
        USER_AGENT = self.user_agent_mgr.get_user_agent()
        self.USER_AGENT = f"{USER_AGENT};{website_bot})"  # Customize as needed
        # Initialize global sets
        self.visited_pages = set()
        self.downloaded_assets = set()

        # Session with custom headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept-Language': 'en-US,en;q=0.5',
            "Access-Control-Allow-Origin": "*"})

    def process_page(self,url, depth, base_domain):
        """
        Process a single page: download assets, save HTML, and crawl links.
        """
        print(url)
        if url in self.visited_pages or depth > self.MAX_DEPTH:
            return
        self.visited_pages.add(url)
        
 
        # Fetch the page content
        response = self.session.get(url)
        #response.raise_for_status()
        content = response.text
                                  
        # Use your get_soup_mgr function to get the soup and attributes
        soup_mgr = get_soup_mgr(url=url)
        soup = soup_mgr.soup
        all_attributes = soup_mgr.get_all_attribute_values()
        # Now you can use all_attributes as needed

        # Update asset links to local paths
        for tag in soup.find_all(['img', 'script', 'link']):
            attr = 'src' if tag.name != 'link' else 'href'
            asset_url = tag.get(attr)
            if asset_url:
                full_asset_url = normalize_url(asset_url, url)
                parsed_asset_url = urlparse(full_asset_url)

                if is_valid_url(full_asset_url, base_domain):
                    self.downloaded_assets = save_asset(full_asset_url,
                                                        self.url,
                                                        self.OUTPUT_DIR,
                                                        self.downloaded_assets,
                                                        self.session)
                    # Update tag to point to the local asset
                    local_asset_path = '/' + parsed_asset_url.path.lstrip('/')
                    tag[attr] = local_asset_path

        # Save the modified page
        save_page(url, str(soup),self.OUTPUT_DIR)
        # Use your linkManager to find all domain links
        link_mgr = linkManager(url=url)
        all_domains = link_mgr.find_all_domain()
        
        # Process each domain link
        for link_url in make_list(all_domains):
            normalized_link = normalize_url(link_url, url)
            if is_valid_url(normalized_link, base_domain):
                time.sleep(self.WAIT_BETWEEN_REQUESTS)
                self.process_page(normalized_link, depth + 1, base_domain)


    def main(self):
        # Ensure output directory exists
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)

        base_parsed = urlparse(self.BASE_URL)
        base_domain = base_parsed.netloc

        self.process_page(self.BASE_URL, 0, base_domain)
        print("Website copying completed.")

def usurpit(url,output_dir=None,max_depth=None,wait_between_requests=None,operating_system=None, browser=None, version=None,user_agent=None,website_bot=None):
    output_dir = get_domain_name_from_url(url) or  make_directory(path='usurped')
    site_mgr = usurpManager(url,output_dir=output_dir,max_depth=max_depth,wait_between_requests=wait_between_requests,operating_system=operating_system, browser=browser, version=version,user_agent=user_agent,website_bot=website_bot)
    site_mgr.main()
##url = "https://www.youtube.com/watch?v=wp43OdtAAkM"
##ua_mgr = UserAgentManager(randomAll=True)
##while True:
##    user_agent = ua_mgr.get_user_agent()
##    headers = ua_mgr.generate_headers()
##    request_mgr = requestManager(url=url,user_agent=user_agent,headers=headers)
##    source_code = request_mgr.source_code
##    soup = BeautifulSoup(source_code, "html.parser")
##    text = soup.text
##    if 'Please update your browser' not in text and 'Bitte aktualisiere deinen BrowserDein Browser' not in text and 'browser is no longer supported' not in text:
##        
##        print(user_agent)
##        print(headers)
##        input(text)


