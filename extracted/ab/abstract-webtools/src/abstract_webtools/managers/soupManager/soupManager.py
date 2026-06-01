from ..urlManager import *
from ..requestManager import *
from bs4 import BeautifulSoup
import re, json
from bs4 import BeautifulSoup, Tag
class soupManager:
    """
    SoupManager is a class for managing and parsing HTML source code using BeautifulSoup.

    Args:
        url (str or None): The URL to be parsed (default is None).
        source_code (str or None): The HTML source code (default is None).
        url_mgr (UrlManager or None): An instance of UrlManager (default is None).
        requestManager (SafeRequest or None): An instance of SafeRequest (default is None).
        parse_type (str): The type of parser to be used by BeautifulSoup (default is "html.parser").

    Methods:
        re_initialize(): Reinitialize the SoupManager with the current settings.
        update_url(url): Update the URL and reinitialize the SoupManager.
        update_source_code(source_code): Update the source code and reinitialize the SoupManager.
        update_requestManager(requestManager): Update the request manager and reinitialize the SoupManager.
        update_url_mgr(url_mgr): Update the URL manager and reinitialize the SoupManager.
        update_parse_type(parse_type): Update the parsing type and reinitialize the SoupManager.
        all_links: A property that provides access to all discovered links.
        _all_links_get(): A method to load all discovered links.
        get_all_website_links(tag="a", attr="href"): Get all URLs belonging to the same website.
        meta_tags: A property that provides access to all discovered meta tags.
        _meta_tags_get(): A method to load all discovered meta tags.
        get_meta_tags(): Get all meta tags in the source code.
        find_all(element, soup=None): Find all instances of an HTML element in the source code.
        get_class(class_name, soup=None): Get the specified class from the HTML source code.
        has_attributes(tag, *attrs): Check if an HTML tag has the specified attributes.
        get_find_all_with_attributes(*attrs): Find all HTML tags with specified attributes.
        get_all_desired_soup(tag=None, attr=None, attr_value=None): Get HTML tags based on specified criteria.
        extract_elements(url, tag=None, class_name=None, class_value=None): Extract portions of source code based on filters.
        find_all_with_attributes(class_name=None, *attrs): Find classes with associated href or src attributes.
        get_images(tag_name, class_name, class_value): Get images with specific class and attribute values.
        discover_classes_and_meta_images(tag_name, class_name_1, class_name_2, class_value, attrs): Discover classes and meta images.

    Note:
        - The SoupManager class is designed for parsing HTML source code using BeautifulSoup.
        - It provides various methods to extract data and discover elements within the source code.
    """

class soupManager:
    def __init__(self, url=None, url_mgr=None, source_code=None, req_mgr=None, parse_type="html.parser", soup=None, soup_mgr=None):
        self.url_mgr = get_url_mgr(url=url, url_mgr=url_mgr)
        self.url = self.url_mgr.url
        self.req_mgr = req_mgr or requestManager(url_mgr=self.url_mgr, url=self.url, source_code=source_code)
        self.source_code = (source_code or (req_mgr.source_code if req_mgr else "")) or ""
        self.parse_type = parse_type
        self.soup = BeautifulSoup(self.source_code, parse_type)
        self._all_links_data = None
        self._meta_tags_data = None

    def all_meta(self):
        out = []
        for m in self.soup.find_all("meta"):
            row = {}
            for k in ("name","property","http-equiv","itemprop","charset","content"):
                v = m.get(k)
                if v: row[k] = v
            if row: out.append(row)
        return out

    def citation_dict(self):
        out = {}
        for m in self.soup.find_all("meta"):
            k = (m.get("name") or m.get("property") or "").lower()
            if k.startswith("citation_") and m.get("content"):
                out.setdefault(k, []).append(m["content"])
        return out



    @property
    def all_links(self):
        if self._all_links_data is None:
            self._all_links_data = self._all_links_get()
        return self._all_links_data

    def _all_links_get(self):
        links = []
        for l in self.soup.find_all("link"):
            rel = l.get("rel")
            if isinstance(rel, list): rel = " ".join(rel)
            links.append({
                "rel": rel, "href": l.get("href"),
                "type": l.get("type"), "title": l.get("title"), "hreflang": l.get("hreflang")
            })
        return links

    def get_all_website_links(self, tag="a", attr="href") -> list:
        """Return all same-domain URLs found in anchors (or given tag/attr)."""
        urls = []
        domain = self.url_mgr.domain
        for t in self.find_all(tag):
            href = t.get(attr)
            if not href:
                continue
            href = self.url_mgr.get_relative_href(self.url_mgr.url, href)
            if not self.url_mgr.is_valid_url(href):
                continue
            if domain and domain not in href:
                continue
            if href not in urls:
                urls.append(href)
        return urls

    def all_jsonld(self):
        blocks = []
        for s in self.soup.find_all("script", type=re.compile("application/ld\\+json", re.I)):
            txt = s.get_text(strip=True)
            try:
                blocks.append(json.loads(txt))
            except Exception:
                blocks.append({"raw": txt})
        return blocks
    def re_initialize(self):
        self.soup= BeautifulSoup(self.source_code, self.parse_type)
        self._all_links_data = None
        self._meta_tags_data = None
    def update_url(self,url):
        self.url_mgr.update_url(url=url)
        self.url=self.url_mgr.url
        self.req_mgr.update_url(url=url)
        self.source_code = self.req_mgr.source_code_bytes
        self.re_initialize()
    def update_source_code(self,source_code):
        if source_code:
            source_code = str(source_code)
        self.source_code = source_code
        self.re_initialize()
    def update_requestManager(self,requestManager):
        self.req_mgr = requestManager
        self.url_mgr=self.req_mgr.url_mgr
        self.url=self.url_mgr.url
        self.source_code = self.req_mgr.source_code_bytes
        self.re_initialize()
    def update_url_mgr(self,url_mgr):
        self.url_mgr=url_mgr
        self.url=self.url_mgr.url
        self.req_mgr.update_url_mgr(url_mgr=self.url_mgr)
        self.source_code = self.req_mgr.source_code_bytes
        self.re_initialize()
    def update_parse_type(self,parse_type):
        self.parse_type=parse_type
        self.re_initialize()
        
    def get_all_website_links(self, tag="a", attr="href") -> list:
        """Return all same-domain URLs found in anchors (or given tag/attr)."""
        urls = []
        domain = self.url_mgr.domain
        
        for t in self.find_all(tag):
            href = t.get(attr)
            if not href:
                continue
            href = self.url_mgr.get_relative_href(self.url_mgr.url, href)
            if not self.url_mgr.is_valid_url(href):
                continue
            if domain and domain not in href:
                continue
            if href not in urls:
                urls.append(href)
            
        return urls




    @property
    def meta_tags(self):
        if self._meta_tags_data is None:
            self._meta_tags_data = self._meta_tags_get()
        return self._meta_tags_data

    def _meta_tags_get(self):
        meta = {}
        for tag in self.soup.find_all("meta"):
            for attr, val in tag.attrs.items():
                meta.setdefault(attr, [])
                if val not in meta[attr]:
                    meta[attr].append(val)
        return meta
    def get_meta_tags(self):
        tags = self.find_all("meta")
        for meta_tag in tags:
            for attr, values in meta_tag.attrs.items():
                if attr not in self.meta_tags:
                    self.meta_tags[attr] = []
                if values not in self.meta_tags[attr]:
                    self.meta_tags[attr].append(values)

                    


    def find_all(self, element, soup=None):
        soup = self.soup if soup is None else soup
        return soup.find_all(element)


    def findit(self, criteria, *, soup=None):
        """
        The One True findit — stops at first match, exactly as you commanded.

        "span" → returns the moment it finds:
            • tag name == span
            OR
            • any attribute name contains "span"
            OR
            • any attribute value contains "span"
            OR
            • text content contains "span"

        As soon as one condition wins → all tags matching that condition are returned.
        No further conditions are checked for that term.
        """
        soup = soup or self.soup
        if not soup:
            return []

        results = []
        seen = set()  # dedupe by identity

        for term in make_list(criteria):
            term_str = str(term).lower().strip()
            if not term_str:
                continue

            # Case 1: Structured dict — precise, respectful, always checked fully
            if isinstance(term, dict):
                for tag_name, condition in term.items():
                    tag_name = tag_name.lower()
                    candidates = soup.find_all(tag_name) if tag_name else soup.find_all(True)

                    for tag in candidates:
                        if not isinstance(tag, Tag) or id(tag) in seen:
                            continue

                        if condition is None:
                            # {"span": None} → just the tag
                            results.append(tag)
                            seen.add(id(tag))
                            continue

                        if isinstance(condition, dict):
                            match = True
                            for attr, expected in condition.items():
                                attr = attr.lower()
                                val = tag.get(attr)

                                if expected is None:
                                    if val is None:
                                        match = False
                                        break
                                elif callable(expected):
                                    if not expected(val):
                                        match = False
                                        break
                                else:
                                    expected_vals = make_list(expected)
                                    actual_vals = make_list(val) if val is not None else []
                                    if attr == "class":
                                        if not any(e in a for e in expected_vals for a in actual_vals):
                                            match = False
                                            break
                                    elif not any(str(e) in str(a) for e in expected_vals for a in actual_vals):
                                        match = False
                                        break
                            if match:
                                results.append(tag)
                                seen.add(id(tag))
                continue  # dict terms are precise — don't fall through to loose search

            # Case 2: Loose string search — "span"
            # We check in priority order — stop at first winning condition
            found = False

            # 1. Tag name contains term → highest priority
            for tag in soup.find_all(lambda t: term_str in t.name.lower()):
                if id(tag) not in seen:
                    results.append(tag)
                    seen.add(id(tag))
            if results and len(results) > len(seen) - 100:  # heuristic: many matches → likely done
                found = True

            # 2. Attribute NAME contains term
            if not found:
                for tag in soup.find_all(True):
                    if id(tag) in seen:
                        continue
                    if any(term_str in attr_name.lower() for attr_name in tag.attrs):
                        results.append(tag)
                        seen.add(id(tag))
                        found = True

            # 3. Attribute VALUE contains term
            if not found:
                for tag in soup.find_all(True):
                    if id(tag) in seen:
                        continue
                    if any(term_str in str(val).lower() for val in tag.attrs.values() for val in make_list(val)):
                        results.append(tag)
                        seen.add(id(tag))
                        found = True

            # 4. Text content contains term — last resort
            if not found:
                for tag in soup.find_all(string=lambda s: s and term_str in s.lower()):
                    parent = tag.parent
                    if isinstance(parent, Tag) and id(parent) not in seen:
                        results.append(parent)
                        seen.add(id(parent))

        # Return in original document order
        ordered = []
        for tag in soup.descendants:
            if isinstance(tag, Tag) and id(tag) in seen:
                ordered.append(tag)
                if len(ordered) == len(seen):
                    break
        return ordered
    @staticmethod
    def has_attributes(tag, *attrs):
        return any(tag.has_attr(attr) for attr in attrs)

    def get_find_all_with_attributes(self, *attrs):
        return self.soup.find_all(lambda t: self.has_attributes(t, *attrs))

    def find_tags_by_attributes(self, tag: str = None, attr: str = None, attr_values: list[str] | None = None) -> list:
        tags = self.soup.find_all(tag) if tag else self.soup.find_all(True)
        out = []
        for t in tags:
            if attr:
                val = t.get(attr)
                if not val:
                    continue
                if attr_values and not any(v in val for v in (val if isinstance(val, list) else [val]) for v in attr_values):
                    continue
            out.append(t)
        return out

    def extract_elements(self,url:str=None, tag:str=None, class_name:str=None, class_value:str=None) -> list:
        """
        Extracts portions of the source code from the specified URL based on provided filters.

        Args:
            url (str): The URL to fetch the source code from.
            element_type (str, optional): The HTML element type to filter by. Defaults to None.
            attribute_name (str, optional): The attribute name to filter by. Defaults to None.
            class_name (str, optional): The class name to filter by. Defaults to None.

        Returns:
            list: A list of strings containing portions of the source code that match the provided filters.
        """
        elements = []
        # If no filters are provided, return the entire source code
        if not tag and not class_name and not class_value:
            elements.append(str(self.soup))
            return elements
        # Find elements based on the filters provided
        if tag:
            elements.extend([str(tags) for tags in self.get_all_desired(tag)])
        if class_name:
            elements.extend([str(tags) for tags in self.get_all_desired(tag={class_name: True})])
        if class_value:
            elements.extend([str(tags) for tags in self.get_all_desired(class_name=class_name)])
        return elements
    def find_all_with_attributes(self, class_name=None, *attrs):
        """
        Discovers classes in the HTML content of the provided URL 
        that have associated href or src attributes.

        Args:
            base_url (str): The URL from which to discover classes.

        Returns:
            set: A set of unique class names.
        """

    
        unique_classes = set()
        for tag in self.get_find_all_with_attributes(*attrs):
            class_list = self.get_class(class_name=class_name, soup=tag)
            unique_classes.update(class_list)
        return unique_classes
    def get_images(self, tag_name, class_name, class_value):
        images = []
        for tag in self.soup.find_all(tag_name):
            if class_name in tag.attrs and tag.attrs[class_name] == class_value:
                content = tag.attrs.get('content', '')
                if content:
                    images.append(content)
        return images
    def extract_text_sections(self) -> list:
        """
        Extract all sections of text from an HTML content using BeautifulSoup.

        Args:
            html_content (str): The HTML content to be parsed.

        Returns:
            list: A list containing all sections of text.
        """
        # Remove any script or style elements to avoid extracting JavaScript or CSS code
        for script in self.soup(['script', 'style']):
            script.decompose()

        # Extract text from the remaining elements
        text_sections = self.soup.stripped_strings
        return [text for text in text_sections if text]
    def discover_classes_and_meta_images(self, tag_name, class_name_1, class_name_2, class_value, attrs):
        """
        Discovers classes in the HTML content of the provided URL 
        that have associated href or src attributes. Also, fetches 
        image references from meta tags.

        Args:
            base_url (str): The URL from which to discover classes and meta images.

        Returns:
            tuple: A set of unique class names and a list of meta images.
        """
    
        unique_classes = self.find_all_with_attributes(class_name=class_name_1, *attrs)
        images = self.get_images(tag_name=tag_name, class_name=class_name_2, class_value=class_value)
        return unique_classes, images
    def get_all_tags_and_attribute_names(self):
        tag_names = set()  # Using a set to ensure uniqueness
        attribute_names = set()
        get_all = self.find_tags_by_attributes()
        for tag in get_all:  # True matches all tags
            tag_names.add(tag.name)
            for attr in tag.attrs:
                attribute_names.add(attr)
        tag_names_list = list(tag_names)
        attribute_names_list = list(attribute_names)
        return {"tags":tag_names_list,"attributes":attribute_names_list}

    def get_all_attribute_values(self, tags_lists=None):
        """
        Collects all attribute values for each specified tag or all tags if none are specified.
        
        Parameters:
        - tags_list: List of specific tags to retrieve attributes from, e.g., ['script', 'img'].
                    If None, retrieves attributes for all tags.
        
        Returns:
        - attribute_values: Dictionary where each key is an attribute and the value is a list of unique values for that attribute.
        """
        attribute_values = {}
        tags_lists = tags_lists or self.get_all_tags_and_attribute_names()
        # Get all tags matching tags_list criteria
        for key,tags_list in tags_lists.items():
            for tag_name in tags_list:
                for tag in self.soup.find_all(tag_name):
                    for attr, value in tag.attrs.items():
                        if attr not in attribute_values:
                            attribute_values[attr] = set()
                        
                        # Add attribute values
                        if isinstance(value, list):
                            attribute_values[attr].update(value)
                        else:
                            attribute_values[attr].add(value)
        
        # Convert each set to a list for consistency
        for attr, values in attribute_values.items():
            attribute_values[attr] = list(values)

        # Capture JavaScript URLs inside <script> tags
        attribute_values['script_links'] = self.get_js_links()

        return attribute_values

    def get_js_links(self):
        """Extract URLs embedded in JavaScript within <script> tags."""
        js_links = []
        script_tags = self.soup.find_all('script')
        for script in script_tags:
            # Find URLs in the JavaScript code
            urls_in_js = re.findall(r'["\'](https?://[^"\']+|/[^"\']+)["\']', script.get_text())
            js_links.extend(urls_in_js)
        return list(set(js_links))  # Remove duplicates
    
    @property
    def url(self):
        return self._url
    @url.setter
    def url(self, new_url):
        self._url = new_url




class SoupManagerSingleton():
    _instance = None
    @staticmethod
    def get_instance(url_mgr,requestManager,parse_type="html.parser",source_code=None):
        if SoupManagerSingleton._instance is None:
            SoupManagerSingleton._instance = SoupManager(url_mgr,requestManager,parse_type=parse_type,source_code=source_code)
        elif parse_type != SoupManagerSingleton._instance.parse_type  or source_code != SoupManagerSingleton._instance.source_code:
            SoupManagerSingleton._instance = SoupManager(url_mgr,requestManager,parse_type=parse_type,source_code=source_code)
        return SoupManagerSingleton._instance
def get_soup(url=None,url_mgr=None,req_mgr=None,source_code=None,soup_mgr=None,soup=None,parse_type=None):
    parse_type = parse_type or "html.parser"
    if source_code or soup_mgr:
        if soup_mgr:
            return soup_mgr.soup
        return BeautifulSoup(source_code, parse_type)
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
    url = get_url(url=url,url_mgr=url_mgr)
    req_mgr = req_mgr or get_req_mgr(url_mgr=url_mgr,url=url,source_code=source_code)
    source_code = req_mgr.source_code
    soup_mgr = get_soup_mgr(url=url,url_mgr=url_mgr,source_code=source_code,req_mgr=req_mgr,soup_mgr=soup_mgr,soup=soup)
    return soup_mgr.soup
def get_soup_mgr(url=None,url_mgr=None,source_code=None,req_mgr=None,soup_mgr=None,soup=None,parse_type=None):
    parse_type = parse_type or "html.parser"
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
    url = get_url(url=url,url_mgr=url_mgr)
    req_mgr = get_req_mgr(url_mgr=url_mgr,url=url,source_code=source_code)
    soup_mgr = soup_mgr or soupManager(url_mgr=url_mgr,req_mgr=req_mgr,url=url,source_code=source_code,soup=soup)
    return soup_mgr
def get_all_attribute_values(url=None,url_mgr=None,source_code=None,req_mgr=None,soup_mgr=None,soup=None,tags_list = None,parse_type=None):
    parse_type = parse_type or "html.parser"
    soup_mgr = get_soup_mgr(url=url,url_mgr=url_mgr,source_code=source_code,req_mgr=req_mgr,soup_mgr=soup_mgr,soup=soup)
    return soup_mgr.get_all_attribute_values(tags_list=tags_list)
def get_soup_text(url):
    try:
        return get_soup_mgr(url).soup.text
    except Exception as e:
        print(f"{e}")
    return ""
