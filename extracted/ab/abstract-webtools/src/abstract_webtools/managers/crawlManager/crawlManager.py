from ..imports import *
from ..linkManager import *
from ..soupManager import *

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

# Example usage:
if __name__ == "__main__":
    base_url = 'https://pump.fun'  # Replace with your website URL
    input(linkManager(base_url).find_all_domain())
    generator = SitemapGenerator(base_url)
    generator.run()

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

    def crawl(self, start=None, max_depth=2, _depth=0, visited=None, session=None):
        start = start or self.url
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
    all_domain_links = crawl_mgr.crawl(url=url, max_depth=max_depth, depth=depth)
    return all_domain_links
