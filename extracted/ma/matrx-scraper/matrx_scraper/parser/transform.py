from collections.abc import Callable

from bs4 import BeautifulSoup

from matrx_scraper.media_embed import video_embed_provider

from .utils import get_soup


class HtmlTransformer:
    """
    A class to transform HTML content before extraction:
    1. Fix broken HTML issues
    2. Transform complex CMS elements into simpler structures
    3. Standardize custom elements for consistent extraction

    This acts as a preprocessing pipeline before the HTML reaches the extractor.
    """

    # more ideas for site specific detection, service detection and more only if needed: https://claude.ai/chat/d6592370-ba7d-4c43-a095-c8b0fd8a666c

    def __init__(self, html: str | BeautifulSoup):
        """
        Initialize the HtmlTransformer with HTML content.

        Args:
            html (Union[str, bs4.BeautifulSoup]): HTML content as a string or BeautifulSoup object.
        """
        self.soup = self._initialize_soup(html)

        # Core fixers that run first (fix structural issues)
        self.core_fixers = [
            self.broken_tag_fix,
            self.orphan_li_fixer,
        ]

        # Custom transformers for CMS-specific elements
        self.custom_transformers = []

        # Register all default transformers
        self._register_default_transformers()

    def _initialize_soup(self, html: str | BeautifulSoup) -> BeautifulSoup:
        """
        Parse HTML content into a BeautifulSoup object.
        """
        return get_soup(html)

    def process(self, soup=True) -> str | BeautifulSoup:
        """
        Apply all transformations to the HTML content.

        Returns:
            Union[str, BeautifulSoup]: The transformed HTML content.
        """
        # Apply core fixers first
        for fixer in self.core_fixers:
            fixer()

        # Then apply custom transformers
        for transformer in self.custom_transformers:
            transformer["transform_func"](self.soup)

        if soup:
            return self.soup
        else:
            return str(self.soup)

    def register_transformer(
        self,
        name: str,
        transform_func: Callable,
        tag: str = None,
        class_name: str = None,
        id: str = None,
        selector: str = None,
    ):
        """
        Register a custom transformer.

        Args:
            name: Name of the transformer for identification
            selector: CSS selector to find elements to transform
            transform_func: Function that transforms the elements
        """
        self.custom_transformers.append(
            {"name": name, "selector": selector, "transform_func": transform_func}
        )

    def _register_default_transformers(self):
        """Register all default transformers for known CMS patterns"""
        # WordPress Gutenberg Blocks
        self.register_transformer(
            name="convert_bsp_carousel",
            tag="bsp-carousel",
            transform_func=self._transform_bsp_carousel,
        )

        self.register_transformer(
            name="transform_content_headers",
            transform_func=self._transform_content_headers,
        )

        self.register_transformer(
            name="transform_common_video_iframes",
            transform_func=self._transform_common_video_iframes,
        )

    # Core fixers
    def broken_tag_fix(self):
        """Fix malformed or broken HTML tags"""
        try:
            self.soup = BeautifulSoup(str(self.soup), "lxml")
        except Exception as e:
            print(f"Error fixing broken tags: {e}")

    def orphan_li_fixer(self):
        """Wraps consecutive orphan <li> elements in a <ul> tag."""
        all_li_elements = self.soup.find_all("li")
        consecutive_orphans = []

        for li in all_li_elements:
            if li.parent.name not in ["ul", "ol"]:
                consecutive_orphans.append(li)
            else:
                if consecutive_orphans:
                    self._wrap_orphan_li(consecutive_orphans)
                    consecutive_orphans = []

        if consecutive_orphans:
            self._wrap_orphan_li(consecutive_orphans)

    def _wrap_orphan_li(self, li_elements: list):
        """Wraps orphan <li> elements in a <ul> tag."""
        if not li_elements:
            return

        new_ul = self.soup.new_tag("ul")
        li_elements[0].insert_before(new_ul)

        for li in li_elements:
            new_ul.append(li.extract())

    # Selective fixers
    def _transform_bsp_carousel(self, soup: BeautifulSoup):
        """Transform BSP carousels into simple lists"""
        for carousel in soup.select("bsp-carousel"):
            container = soup.new_tag("div")
            container["class"] = "transformed-carousel"

            title_elem = carousel.find("h2", class_="Carousel-title")
            title = (
                title_elem.get("data-override-title", title_elem.get_text(strip=True))
                if title_elem
                else "Untitled Carousel"
            )

            title_p = soup.new_tag("p")
            title_p.string = f"Carousel: {title}"
            container.append(title_p)

            ul = soup.new_tag("ul")
            container.append(ul)

            # Process slides
            for slide in carousel.find_all("div", class_="Carousel-slide"):
                # Extract slide data
                desc_elem = slide.find("span", class_="CarouselSlide-infoDescription")
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                picture = slide.find("picture")

                # Add the description text
                text = description or f"[Slide {slide.get('data-slidenumber', '')}]"
                li = soup.new_tag("li")
                li.append(soup.new_string(text))
                ul.append(li)

                if picture:
                    li = soup.new_tag("li")
                    li.append(picture)
                    ul.append(li)

            carousel.replace_with(container)

    def _transform_content_headers(self, soup: BeautifulSoup):
        """
        Transform content-rich headers into divs to preserve them.

        Args:
            soup: BeautifulSoup object to transform
        """
        for header in soup.find_all("header"):
            is_content = self._is_content_header_tag(header)

            if is_content:
                # print("IT IS A CONTENT HEADER")
                # Create a new div to replace the header
                content_div = soup.new_tag("div")
                content_div["class"] = "preserved-content"
                content_div["data-original-tag"] = "header"

                # Move all content from header to the new div
                for child in list(header.children):
                    content_div.append(child.extract())

                # Replace the header with our new div
                header.replace_with(content_div)

    def _is_content_header_tag(self, header):
        """
        Determine if a header contains valuable content.

        Args:
            header: Header tag to evaluate

        Returns:
            bool: True if the header contains valuable content
        """
        # Headers with headings are almost always content
        if header.find(["h1", "h2", "h3"]):
            return True

        # Headers with time elements are usually content
        if header.find("time"):
            return True

        # Check for navigation patterns
        nav_elements = header.find_all(["nav", "menu"])
        list_elements = header.find_all(["ul", "ol"])
        list_with_links = any(len(ul.find_all("a")) > 2 for ul in list_elements)

        if (nav_elements or list_with_links) and not header.find(["h1", "h2", "h3", "time"]):
            return False

        return True

    def _transform_common_video_iframes(self, soup: BeautifulSoup):
        for iframe in soup.find_all("iframe"):
            src_attributes = {}

            # Find all attributes that contain "src"
            for attr_name, attr_value in iframe.attrs.items():
                if "src" in attr_name.lower() and attr_value:
                    src_attributes[attr_name] = attr_value

            valid_src = None
            matched_provider = None

            for attr_name, attr_value in src_attributes.items():
                provider = video_embed_provider(attr_value)
                if provider:
                    valid_src = attr_value
                    matched_provider = provider
                    break

            if valid_src:
                video_tag = soup.new_tag("video")

                if iframe.has_attr("width"):
                    video_tag["width"] = iframe["width"]
                if iframe.has_attr("height"):
                    video_tag["height"] = iframe["height"]

                video_tag["provider"] = matched_provider

                source_tag = soup.new_tag("source")
                source_tag["src"] = valid_src
                source_tag["type"] = "unknown"

                video_tag.append(source_tag)
                iframe.replace_with(video_tag)
