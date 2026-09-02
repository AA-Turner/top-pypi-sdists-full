import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag, Comment

from .utils import join_url, is_data_url


class HTMLFlattener:
    """
    Converts Nested Structures to something sane
    With optional markdown syntax for anchors
    """

    def __init__(self, soup, url=None):
        self.url = url

        if isinstance(soup, str):
            self.soup = BeautifulSoup(soup, "lxml")  # Using 'lxml' parser for better handling
        elif isinstance(soup, Tag):
            self.soup = soup
        else:
            raise TypeError("Input must be a string or a BeautifulSoup Tag object.")

        # Enable/disable markdown syntax for anchors
        self.md_syntax = True

        # Define sets of inline, block, and media elements
        self.inline_elements = {
            "a",
            "abbr",
            "acronym",
            "b",
            "bdi",
            "bdo",
            "big",
            "br",
            "button",
            "cite",
            "code",
            "data",
            "datalist",
            "del",
            "dfn",
            "em",
            "i",
            "img",
            "input",
            "ins",
            "kbd",
            "label",
            "map",
            "mark",
            "meter",
            "noscript",
            "object",
            "output",
            "progress",
            "q",
            "ruby",
            "s",
            "samp",
            "select",
            "small",
            "span",
            "strong",
            "sub",
            "sup",
            "textarea",
            "time",
            "u",
            "tt",
            "var",
            "wbr",
            "td",
            "source",
        }

        self.block_elements = {
            "address",
            "article",
            "aside",
            "blockquote",
            "canvas",
            "dd",
            "div",
            "dl",
            "dt",
            "fieldset",
            "figcaption",
            "figure",
            "footer",
            "form",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "header",
            "hr",
            "li",
            "main",
            "nav",
            "ol",
            "p",
            "pre",
            "section",
            "table",
            "ul",
            "video",
            "picture",
            "audio",
        }

        # Media elements that should be preserved for the ElementExtractor
        self.media_elements = {"img", "video", "audio", "figure", "picture", "embed"}

    def is_protected(self, element):
        """
        Determine if an element should be treated as protected.
        - Always protect elements in always_protected_elements.
        - Protect 'code' if it contains newlines.
        - Always protect media elements
        - Protect spans with class 'flattened-text'
        """

        def _contains_more_than_one_word(text):
            return len(text.split(" ")) > 1

        if element.name == "pre":
            return True

        if "autoclicker-protected-element" in element.get("class", []):
            return True  # TODO: REMOVE THIS AFTER CONFIRMING THIS DOES NOT AFFECT ANYTHING

        if element.name == "code":
            # Check raw text for newlines
            if len(list(element.descendants)) > 1 and _contains_more_than_one_word(
                element.get_text(strip=True)
            ):
                element.name = "pre"
                return True
            else:
                element.unwrap()

        # Always protect media elements
        if element.name in self.media_elements:
            return True

        # Protect spans with class 'flattened-text'
        if element.name == "span" and "flattened-text" in element.get("class", []):
            return True

        return False

    def process_html(self):
        """Process the entire HTML document by fixing and flattening it."""
        self._flatten_element(self.soup)

        # Todo : This one is not important. Currently giving errors, needed to be fixed
        # try:
        #     self._flatten_nested_divs(self.soup)
        # except:
        #     pass

        return str(
            self.soup
        )  # Changed from prettify() to str(self.soup) to preserve original formatting

    def _flatten_element(self, element):
        """Recursively flatten elements from the deepest level to the top."""
        # Process children first (bottom-up approach)
        for child in list(element.children):
            if isinstance(child, Tag):
                # Skip protected elements to preserve content
                if self.is_protected(child):
                    continue

                # Recursively flatten the child element first
                self._flatten_element(child)

                # Handle inline elements
                if child.name in self.inline_elements and child.name != "a":
                    if self._has_block_children(child):
                        self._convert_to_block(child)
                    else:
                        self._join_inline_children(child)

                # Join consecutive inline elements or raw text in a block
                if child.name in self.block_elements:
                    self._join_consecutive_inlines(child)
            elif isinstance(child, Comment):
                # Preserve comments by not altering them
                continue
            else:
                # Handle NavigableString or other types if necessary
                continue

    def _flatten_nested_divs(self, soup):
        """Flatten deeply nested <div> elements."""
        for div in soup.find_all("div", recursive=False):
            self._flatten_divs(div)

    def _flatten_divs(self, element):
        """Flatten <div> elements that are nested without other content."""
        for child in list(element.children):
            if isinstance(child, Tag):
                self._flatten_divs(child)

        # Flatten <div> elements that contain only one non-whitespace child
        if element.name == "div":
            # Remove any whitespace-only content
            element.contents = [
                content
                for content in element.contents
                if not (isinstance(content, str) and content.strip() == "")
            ]

            # Check if there's exactly one child, and it's a <div>
            while (
                len(element.contents) == 1
                and isinstance(element.contents[0], Tag)
                and element.contents[0].name == "div"
            ):
                inner_div = element.contents[0]

                # Transfer all children from the innermost div to the current div
                for grandchild in list(inner_div.children):
                    element.append(grandchild.extract())

                # Remove the innermost div after transferring its contents
                try:
                    inner_div.decompose()
                except Exception:
                    pass

        # Remove divs that are empty
        for div in list(element.find_all("div", recursive=False)):
            if not div.contents or all(isinstance(c, str) and not c.strip() for c in div.contents):
                div.decompose()

    def _has_block_children(self, element):
        """Check if an element has any block-level children."""
        return any(
            isinstance(child, Tag) and child.name in self.block_elements
            for child in element.children
        )

    def _contains_media(self, element):
        """Check if element contains any media elements"""
        return bool(
            element.find(lambda tag: isinstance(tag, Tag) and tag.name in self.media_elements)
        )

    def _join_consecutive_inlines(self, element):
        """Join consecutive inline elements or raw text in a block."""
        new_children = []
        buffer = []
        fmt_buffer = []

        for child in element.children:
            if isinstance(child, Comment):
                # Flush the buffer before handling the comment
                if buffer:
                    self._append_flattened_span(new_children, buffer, fmt_buffer)
                    buffer = []
                    fmt_buffer = []
                # Append the comment as-is
                new_children.append(child)
            elif isinstance(child, Tag) and child.name in self.media_elements:
                # If buffer has accumulated text, add it before appending the media element
                if buffer:
                    self._append_flattened_span(new_children, buffer, fmt_buffer)
                    buffer = []
                    fmt_buffer = []
                # Preserve the media element as-is
                new_children.append(child)
            elif (
                isinstance(child, Tag)
                and child.name == "a"
                and self.md_syntax
                and not self._contains_media(child)
            ):
                # Special handling for anchors in markdown mode
                text = child.get_text(strip=True)
                href = child.get("href", "").strip()
                complete_url = join_url(self.url, href)

                data_url, has_base64 = is_data_url(url=complete_url)
                is_readable = self.is_readable_url(url=complete_url)
                # If both text and href exist, convert to markdown format
                if text and href and not data_url and is_readable:
                    # Add plain text to buffer, formatted text to fmt_buffer
                    buffer.append(text)
                    fmt_buffer.append(f"[{text}]({complete_url})")
                else:
                    # If invalid link, add plain text to both buffers
                    plain_text = child.get_text(separator=" ", strip=True)
                    buffer.append(plain_text)
                    fmt_buffer.append(plain_text)
            elif isinstance(child, Tag) and child.name in self.inline_elements:
                if self.is_protected(child) or self._contains_media(child):
                    # If buffer has accumulated text, add it before appending the protected tag
                    if buffer:
                        self._append_flattened_span(new_children, buffer, fmt_buffer)
                        buffer = []
                        fmt_buffer = []
                    # Append the protected tag as-is
                    new_children.append(child)
                else:
                    # Not protected; append text to both buffers
                    text = child.get_text(separator=" ", strip=True)
                    buffer.append(text)
                    fmt_buffer.append(text)
            elif isinstance(child, str):
                stripped_text = child.strip()
                if stripped_text:
                    buffer.append(stripped_text)
                    fmt_buffer.append(stripped_text)
            else:
                if buffer:
                    self._append_flattened_span(new_children, buffer, fmt_buffer)
                    buffer = []
                    fmt_buffer = []
                new_children.append(child)

        if buffer:
            self._append_flattened_span(new_children, buffer, fmt_buffer)

        element.clear()
        for new_child in new_children:
            element.append(new_child)

    def _append_flattened_span(self, new_children, buffer, fmt_buffer):
        """Helper method to create and append a span with flattened text and fmt-txt attribute."""
        concatenated = " ".join(filter(None, buffer))
        fmt_concatenated = " ".join(filter(None, fmt_buffer))
        if concatenated:
            span = self.soup.new_tag(
                "span", attrs={"class": "flattened-text", "fmt-txt": fmt_concatenated}
            )
            span.string = concatenated
            new_children.append(span)

    def _join_inline_children(self, element):
        """Join multiple inline elements within an inline element."""
        new_children = []
        buffer = []
        fmt_buffer = []

        for child in element.children:
            if isinstance(child, Comment):
                # Flush the buffer before handling the comment
                if buffer:
                    self._append_flattened_span(new_children, buffer, fmt_buffer)
                    buffer = []
                    fmt_buffer = []
                # Append the comment as-is
                new_children.append(child)
            elif isinstance(child, Tag) and child.name in self.media_elements:
                # If buffer has accumulated text, add it before appending the media element
                if buffer:
                    self._append_flattened_span(new_children, buffer, fmt_buffer)
                    buffer = []
                    fmt_buffer = []
                # Preserve the media element as-is
                new_children.append(child)
            elif (
                isinstance(child, Tag)
                and child.name == "a"
                and self.md_syntax
                and not self._contains_media(child)
            ):
                # Special handling for anchors in markdown mode
                text = child.get_text(strip=True)
                href = child.get("href", "")
                complete_url = join_url(self.url, href)
                data_url, has_base64 = is_data_url(url=complete_url)
                is_readable = self.is_readable_url(url=complete_url)

                # If both text and href exist, convert to markdown format
                if text and href and not data_url and is_readable:
                    # Add plain text to buffer, formatted text to fmt_buffer
                    buffer.append(text)
                    fmt_buffer.append(f"[{text}]({complete_url})")
                else:
                    # If invalid link, add plain text to both buffers
                    plain_text = child.get_text(separator=" ", strip=True)
                    buffer.append(plain_text)
                    fmt_buffer.append(plain_text)
            elif isinstance(child, Tag) and child.name in self.inline_elements:
                if self.is_protected(child) or self._contains_media(child):
                    # If buffer has accumulated text, add it before appending the protected tag
                    if buffer:
                        self._append_flattened_span(new_children, buffer, fmt_buffer)
                        buffer = []
                        fmt_buffer = []
                    # Append the protected tag as-is
                    new_children.append(child)
                else:
                    # Not protected; append text to both buffers
                    text = child.get_text(separator=" ", strip=True)
                    buffer.append(text)
                    fmt_buffer.append(text)
            elif isinstance(child, str):
                stripped_text = child.strip()
                if stripped_text:
                    buffer.append(stripped_text)
                    fmt_buffer.append(stripped_text)
            else:
                if buffer:
                    self._append_flattened_span(new_children, buffer, fmt_buffer)
                    buffer = []
                    fmt_buffer = []
                new_children.append(child)

        if buffer:
            self._append_flattened_span(new_children, buffer, fmt_buffer)

        element.clear()
        for new_child in new_children:
            element.append(new_child)

    def _convert_to_block(self, element):
        """Convert an inline element to a block element if it contains block children."""
        element.name = "div"  # Change to a block element

    def is_readable_url(self, url):
        # Check for None or empty string
        if not url or not isinstance(url, str):
            return False

        # Trim whitespace
        url = url.strip()

        # Check for JavaScript URLs
        if re.match(r"^javascript:", url, re.IGNORECASE):
            return False

        # Check for data URLs (often base64 encoded content)
        if re.match(r"^data:", url, re.IGNORECASE):
            return False

        # Allow telephone links
        if re.match(r"^tel:", url, re.IGNORECASE):
            return True

        # Allow email links
        if re.match(r"^mailto:", url, re.IGNORECASE):
            return True

        # For standard URLs, use urlparse
        try:
            parsed = urlparse(url)

            # Must have a scheme and netloc (domain) for most URLs
            if not parsed.scheme or not parsed.netloc:
                return False

            # Must be using a standard protocol
            valid_schemes = ["http", "https", "ftp", "ftps"]
            if parsed.scheme.lower() not in valid_schemes:
                return False

            return True
        except Exception:
            return False
