from collections import defaultdict, Counter
import re

from bs4 import NavigableString, Tag, Comment, BeautifulSoup
from markdownify import markdownify as md
from matrx_utils import vcprint

from .data_types import (
    OrganizedData,
    Image,
    Video,
    Audio,
    Header,
    ElementMetadata,
    ListElement,
    TextContent,
    ContentUnion,
    CodeBlock,
    Table,
    Quote,
    BaseContent,
)
from .utils import DomainFilter, join_url, is_data_url
from .flattener import HTMLFlattener

print_in_extraction = False


class ElementExtractor:
    @staticmethod
    def _DEFAULT_METADATA() -> defaultdict:
        return defaultdict(int)

    def __init__(self):
        # Default dictionaries and structures
        self.url = None
        self.hashes = None
        self.metadata = self._DEFAULT_METADATA()
        self.skip_empty_clicks = True
        self.domain_filter = DomainFilter(list_keys="easylist")
        self.debug = False

        # New structured data containers
        self.organized_data: OrganizedData | None = None
        self.header_stack: list[OrganizedData | Header] | None = None

    def _create_metadata(self, element: Tag | NavigableString) -> ElementMetadata:
        """Creates an ElementMetadata object from a BeautifulSoup element."""
        filtered_parent = element.find_parent(["ContentFilter", "contentfilter"])
        if filtered_parent:
            # Only call .get() on Tag objects, not NavigableString
            if isinstance(element, Tag):
                attr_name = filtered_parent.get("type")
                match_type = filtered_parent.get("match_type")
                trigger_item = filtered_parent.get("trigger_item")
            else:
                attr_name = None
                match_type = None
                trigger_item = None

            removal_details = {"attr": attr_name, "match": match_type, "value": trigger_item}
        else:
            removal_details = None

        filter_kwargs = {"filtered": bool(filtered_parent), "filter_details": removal_details}

        if isinstance(element, NavigableString):
            return ElementMetadata(tag=None, attributes={}, **filter_kwargs)
        if isinstance(element, Tag):
            attrs = dict(element.attrs)
            return ElementMetadata(tag=element.name, attributes=attrs, **filter_kwargs)

        return ElementMetadata(**filter_kwargs)

    def has_element_children(self, element):
        return any(child for child in element.children if child.name is not None)

    def get_clean_html(self, main_content):
        flattened_html = HTMLFlattener(main_content, url=self.url).process_html()
        soup = BeautifulSoup(re.sub(r"<!--.*?-->", "", flattened_html, flags=re.DOTALL), "lxml")
        return soup

    def _add_content(self, content_item: ContentUnion | None):
        """Appends a content object to the current container in the hierarchy."""
        if content_item and self.header_stack:
            # If the item is a list, extend the content, otherwise append
            if isinstance(content_item, list):
                self.header_stack[-1].content.extend(c for c in content_item if c)
            else:
                self.header_stack[-1].content.append(content_item)

    def _increment_metadata_count(self, content_type: str):
        if content_type in ["Lists", "Ordered Lists", "ul", "ol"]:
            self.metadata["list_count"] += 1
        elif content_type == "Table":
            self.metadata["table_count"] += 1
        elif content_type == "code":
            self.metadata["code_block_count"] += 1

    def extract_content(self, main_content, clean=True, url=None, debug=False):
        # Reset state for a new extraction
        self.url = url
        self.debug = debug
        self.metadata = self._DEFAULT_METADATA()
        self.hashes = []
        self.organized_data = OrganizedData()

        # Create initial "unassociated" header for content before any real headers
        unassociated_header = Header(
            level=0, text="unassociated", content=[], metadata=ElementMetadata()
        )
        self.organized_data.content.append(unassociated_header)
        self.header_stack = [self.organized_data, unassociated_header]

        if main_content:
            if clean:
                main_content = self.get_clean_html(main_content)

            vcprint(
                data=None,
                title="[Extracting Content]",
                verbose=print_in_extraction,
                color="white",
                background="black",
            )
            self._extract_from_element(main_content, add=True)
        return {
            "organized_data": self.organized_data,
            "metadata": self.metadata,
            "hashes": self.hashes,
        }

    def _extract_from_element(self, element, add=True):
        vcprint(
            data=None,
            title=f"\n[Extracting from Element] {element.name}",
            verbose=print_in_extraction,
            color="white",
            background="black",
        )

        if element.name == "table":
            try:
                return self.handle_tables(element, add)
            except Exception as e:
                vcprint(
                    f"Error extracting table: {e}",
                    verbose=print_in_extraction,
                    color="white",
                    background="black",
                )
                pass

        items = []

        for child in element.children:
            vcprint(
                data=None,
                title=f"\n[Child] {child.name}",
                verbose=print_in_extraction,
                color="white",
                background="black",
            )

            content = self._process_child(child, add)

            if content:
                items.append(content)

        return items

    def _process_child(self, child, add=True):
        if isinstance(child, Comment):
            return None
        if isinstance(child, NavigableString):
            return self._handle_navigable_string(child, add)

        handler_map = {
            "figure": self._parse_figure,
            "img": self._parse_img,
            "picture": self._parse_picture,
            "audio": self._parse_audio,
            "video": self._parse_video,
            "dynamic-content": self._handle_dynamic_content,
            "pre": self._handle_code,
            "code": self._handle_code,
            "blockquote": self._handle_blockquote,
            "ul": self.extract_lists,
            "ol": self.extract_lists,
            "table": self.handle_tables,
            "p": self._handle_p,
            "span": self._handle_p,
            "a": self._handle_a,
            "th": self._handle_th,
        }
        if child.name in handler_map:
            return handler_map[child.name](child, add)
        elif child.name and child.name.startswith("h") and child.name[1:].isdigit():
            return self._handle_header(child)
        else:
            return self._extract_from_element(child, add)

    def _handle_dynamic_content(self, element, add=True):
        text_content = str(element.get("data-click-name")).strip()
        if not text_content and self.skip_empty_clicks:
            return None

        collected_content = []
        metadata = self._create_metadata(element)

        click_text_obj = TextContent(content=f"[{text_content} : Clicked Item]", metadata=metadata)
        if add:
            self._add_content(click_text_obj)
        else:
            collected_content.append(click_text_obj)

        if self.has_element_children(element):
            children_content = self._extract_from_element(element, add=add)
            if not add and children_content:
                collected_content.extend(children_content)

        return collected_content if not add else None

    def _handle_blockquote(self, element, add=True):
        if self.has_element_children(element):
            return self._extract_from_element(element, add)

        else:
            metadata = self._create_metadata(element)
            text = element.get_text().strip()

            quote_obj = Quote(content=text, metadata=metadata)
            if add:
                self._add_content(quote_obj)
            return quote_obj

    def _handle_navigable_string(self, child, add=True):
        if child.parent.name == "[document]":
            return

        text = " ".join(child.strip().split())
        if not text:
            return None

        metadata = self._create_metadata(child)
        text_obj = TextContent(content=text, metadata=metadata)
        if add:
            self._add_content(text_obj)
            return None
        else:
            return text_obj

    def _handle_code(self, element, add=True):
        self._increment_metadata_count("code")
        rendered_code = md(str(element))
        rendered_code = rendered_code.strip().lstrip("`").rstrip("`")

        if not rendered_code:
            return None

        metadata = self._create_metadata(element)
        code_obj = CodeBlock(content=rendered_code, metadata=metadata)
        if add:
            self._add_content(code_obj)
            return None
        else:
            return code_obj

    def _handle_th(self, element, add=True):
        if self.has_element_children(element):
            return self._extract_from_element(element, add)
        else:
            text = element.get_text(strip=True)
            if not text:
                return None
            metadata = self._create_metadata(element)
            text_obj = TextContent(content=text, metadata=metadata)
            if add:
                self._add_content(text_obj)
                return None
            else:
                return text_obj

    def _handle_p(self, element, add=True):
        if self.has_element_children(element):
            return self._extract_from_element(element, add)
        else:
            text = element.get_text(strip=True)
            if not text:
                return None
            metadata = self._create_metadata(element)
            text_obj = TextContent(content=text, metadata=metadata)
            if add:
                self._add_content(text_obj)
                return None
            else:
                return text_obj

    def _handle_a(self, element, add=True):
        if self.has_element_children(element):
            return self._extract_from_element(element, add)
        else:
            text = element.get_text(strip=True)
            if not text:
                return None
            metadata = self._create_metadata(element)
            text_obj = TextContent(content=text, metadata=metadata)
            if add:
                self._add_content(text_obj)
                return None
            else:
                return text_obj

    def _handle_header(self, element):
        text = self._normalize_text(element.get_text().strip())
        if not text:
            return None
        level = int(element.name[1:])
        metadata = self._create_metadata(element)
        new_header = Header(level=level, text=text, content=[], metadata=metadata)

        # If we're currently in the unassociated header (level 0), pop it and add to root
        if (
            len(self.header_stack) > 1
            and isinstance(self.header_stack[-1], Header)
            and self.header_stack[-1].level == 0
        ):
            self.header_stack.pop()  # Remove unassociated header from stack

        # Pop headers until we find one with a lower level than the new header
        while (
            isinstance(self.header_stack[-1], Header)
            and self.header_stack[-1].level >= new_header.level
        ):
            self.header_stack.pop()

        parent = self.header_stack[-1]
        parent.content.append(new_header)
        self.header_stack.append(new_header)
        return None

    def _table_has_consistent_columns(self, table_element):
        rows = table_element.find_all("tr")
        if len(rows) < 2:
            return False
        column_counts = [len(row.find_all(recursive=False)) for row in rows]
        counts = Counter(column_counts)
        most_common_frequency = counts.most_common(1)[0][1]
        return most_common_frequency >= 0.9 * len(column_counts)

    def _is_table_one_column_layout(self, table_element):
        all_rows = table_element.find_all("tr")
        current_tables_rows = [tr for tr in all_rows if tr.find_parent("table") == table_element]
        num_columns = set()
        for tr in current_tables_rows:
            num_columns.add(len(list(tr.children)))
        num_columns = list(num_columns)
        if len(num_columns) == 1 and num_columns[0] == 1:
            return True
        return False

    def _is_data_table(self, table_element):
        if table_element.find("table"):
            return False, "Table has nested tables. Most likely layout table."
        role = table_element.get("role")
        if role == "presentation":
            return False, 'Table has role="presentation", not a data table.'
        if role == "table":
            return True, 'Table has role="table", so it is a data table.'

        def belongs_to_main_table(element):
            return element.find_parent("table") == table_element

        if self._is_table_one_column_layout(table_element):
            return False, "Table is a single-column layout, likely a layout table."

        if table_element.find_all(lambda tag: tag.name == "th" and belongs_to_main_table(tag)):
            return True, "Table contains <th> elements, so it is a data table."
        if table_element.find(lambda tag: tag.name == "thead" and belongs_to_main_table(tag)):
            return True, "Table contains a <thead> element, so it is a data table."
        if table_element.find(lambda tag: tag.name == "tfoot" and belongs_to_main_table(tag)):
            return True, "Table contains a <tfoot> element, so it is a data table."
        if table_element.find(lambda tag: tag.name == "caption" and belongs_to_main_table(tag)):
            return True, "Table contains a <caption> element, so it is a data table."
        if table_element.find(lambda tag: tag.name == "colgroup" and belongs_to_main_table(tag)):
            return True, "Table contains a <colgroup> element, so it is a data table."
        if table_element.get("border") == "1":
            return True, 'Table has border="1", so it is a data table.'
        th_with_scope = table_element.find_all(
            lambda tag: tag.name == "th" and tag.get("scope") and belongs_to_main_table(tag)
        )
        if th_with_scope:
            return True, "Table contains <th> elements with scope attribute, so it is a data table."
        if self._table_has_consistent_columns(table_element):
            return (
                True,
                "Table has consistent columns across rows and number of rows is greater than 2 ",
            )
        return False, "None of the data table indicators were found, likely a layout table."

    def handle_tables(self, table_element, add=True):
        is_valid, validation_message = self._is_data_table(table_element)
        if is_valid:
            vcprint(
                data=validation_message,
                title="[Data Table Found]",
                verbose=print_in_extraction,
                color="white",
                background="black",
            )
            return self.extract_tables(table_element, add=add)
        else:
            vcprint(
                data=validation_message,
                title="[Layout Table Found]",
                verbose=print_in_extraction,
                color="white",
                background="black",
            )
            table_element.name = "div"
            return self._extract_from_element(table_element, add=add)

    def _extract_table_cell_content(self, table_td, add):
        """extracts content from table data cell. Only to be used when td has multiple items after flattening."""
        contents = self._extract_from_element(table_td, add=add)
        if contents:
            if len(contents) == 1 and isinstance(contents[0], list):
                return contents[0]
            return contents
        else:
            return None

    def extract_tables(self, element, add=True):
        def flatten_to_items(obj) -> list[dict]:
            result = []

            def recurse(value):
                if isinstance(value, BaseContent):
                    result.append(value)
                elif isinstance(value, list):
                    for item in value:
                        recurse(item)

            recurse(obj)
            return result

        self._increment_metadata_count("Table")
        vcprint(
            data=None,
            title="[Table]",
            verbose=print_in_extraction,
            color="white",
            background="black",
        )

        pre_table_texts = []
        for sibling in element.find_previous_siblings():
            if sibling.name == "p":
                pre_table_texts.insert(0, sibling.get_text(strip=True))  # Pre-table text

        # Step 1: Find headers
        headers = []
        thead = element.find("thead")
        first_row = element.find("tr")

        if thead:
            # If <thead> exists, use it
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
            skip_first_row = (
                True  # We can skip the first <tr> since it may contain header-like content
            )
        elif first_row and all(th.name == "th" for th in first_row.find_all(recursive=False)):
            # If the first <tr> has only <th> elements, treat it as headers
            headers = [th.get_text(strip=True) for th in first_row.find_all("th")]
            # print(headers)
            skip_first_row = True  # Since it's a header row, we skip it for data
        else:
            # Fallback: Use generic headers (col1, col2, ...)
            first_data_row = first_row.find_all(recursive=False) if first_row else []

            col_count = len(first_data_row)
            headers = [f"col{i + 1}" for i in range(col_count)]
            skip_first_row = False  # Do not skip the first row, treat it as data

        max_columns = max(len(row.find_all(recursive=False)) for row in element.find_all("tr"))

        if len(headers) < max_columns:
            additional_headers = [f"col{i + 1}" for i in range(len(headers), max_columns)]
            headers.extend(additional_headers)

        # Step 2: Extract rows
        data = []
        rows = element.find_all("tr")

        # If skip_first_row is True, skip the first row, otherwise, process all rows
        for row in rows[(1 if skip_first_row else 0) :]:
            row_data = {}
            cells = row.find_all(recursive=False)  # Look for both <td> and <th> cells
            for i, cell in enumerate(cells):
                if cell.name not in ["td", "th"]:
                    # Nested extraction for non-standard table cells
                    cell_content = self._extract_table_cell_content(cell, add=False)
                    cell_content = flatten_to_items(cell_content)
                    if isinstance(cell_content, list):
                        row_data[headers[i]] = (
                            cell_content
                            if len(cell_content) > 1
                            else (cell_content[0] if len(cell_content) > 0 else [])
                        )
                    elif cell_content is not None:
                        row_data[headers[i]] = cell_content
                    else:
                        row_data[headers[i]] = []  # Fallback if no content
                else:
                    # Standard extraction for <td> or <th> cells
                    cell_content = TextContent(
                        content=cell.get_text(separator="\n", strip=True),
                        metadata=self._create_metadata(cell),
                    )
                    row_data[headers[i]] = [cell_content]
            data.append(row_data)

        metadata = self._create_metadata(element)
        table_obj = Table(content=data, metadata=metadata)
        if add:
            self._add_content(table_obj)
            return None
        else:
            return table_obj

    def extract_lists(self, element, add=True):
        # Counted here, at the ONE dispatch site for <ul>/<ol> — nested lists
        # are handled by parse_list's own recursion, never re-dispatched, so
        # this fires exactly once per top-level list. Without it `list_count`
        # stayed 0 on every page ever parsed, which also made
        # `overview.has_structured_content` wrong on a list-only page (AD192).
        self._increment_metadata_count("ul")

        def parse_list(ele):
            """
            Recursively parse a list element (<ul> or <ol>) and return a structured representation.
            """
            items = []
            for li in ele.find_all(recursive=False):
                # Check for children
                if not self.has_element_children(li):
                    li_metadata = self._create_metadata(li)
                    li_content = TextContent(content=li.get_text(strip=True), metadata=li_metadata)
                    _add_items(li_content, items)
                    continue

                # Initialize a list to store content for this item
                item_content = []

                # Process each part of the <li> contents in order
                for part in li.children:
                    if part.name not in ["ul", "ol"]:
                        contents = self._process_child(part, add=False)
                        if contents:
                            _add_items(contents, item_content)

                    elif part.name in ["ul", "ol"]:
                        # Handle nested lists recursively
                        nested_items = parse_list(part)
                        if nested_items:
                            _add_items(nested_items, item_content)

                    else:
                        _add_items(part.get_text(strip=True), item_content)

                # Add the content of the current <li> item to the list
                if item_content:
                    _add_items(item_content, items)

            return items

        def normalize_lists(obj):
            if isinstance(obj, list):
                # First, recursively flatten all elements in the list
                flattened_list = [normalize_lists(element) for element in obj]

                # Then, iteratively flatten the list if it contains only one list
                while len(flattened_list) == 1 and isinstance(flattened_list[0], list):
                    flattened_list = flattened_list[0]
                    # Recursively flatten again in case of multiple nested single lists
                    flattened_list = [normalize_lists(element) for element in flattened_list]

                return flattened_list

            else:
                return obj

        def _add_items(content, items):
            if isinstance(content, list) and len(content) == 1:
                items.extend(content)
            elif isinstance(content, list):
                items.append(content)
            elif isinstance(content, str) and content.strip():
                items.append(content)
            elif not isinstance(content, str):
                items.append(content)

            return items

        list_items = parse_list(element)
        metadata = self._create_metadata(element)
        list_obj = ListElement(content=list_items, metadata=metadata)
        new_content = normalize_lists(list_obj.content)
        list_obj.content = new_content
        if add:
            self._add_content(list_obj)

        return list_obj

    def _normalize_text(self, text) -> str:
        if text and text.strip():
            return "  ".join(text.split("\n")).strip()
        return ""

    def _is_tracking_pixel(self, src):
        if not src:
            return False
        is_data, is_base_64 = is_data_url(src)
        if is_data and is_base_64:
            tracking_pixel_pattern = (
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8"
            )
            return tracking_pixel_pattern in src
        return False

    def _parse_img(self, element, add=True):
        source_attributes = [
            "src",
            "data-src",
            "data-lazy",
            "data-original",
            "data-lazy-src",
            "data-original-src",
            "data-url",
            "data-hi-res-src",
            "data-full-src",
            "lazy-src",
            "nitro-lazy-src",
            "srcset",
        ]
        final_src = ""
        found_attr = None

        for attr in source_attributes:
            value = element.get(attr, "")
            if attr == "srcset" and value:
                srcset_parts = value.split(",")
                if srcset_parts:
                    first_src = srcset_parts[0].strip().split(" ")[0]
                    if first_src:
                        value = first_src
            if value:
                joined_value = self._join_and_check_url(value)
                if joined_value:
                    found_attr = attr
                    final_src = joined_value
                    break
        if not final_src:
            return None

        is_data, _ = is_data_url(final_src)
        if is_data and found_attr == "src":
            for attr in source_attributes[1:]:
                value = element.get(attr, "")
                if attr == "srcset" and value:
                    srcset_parts = value.split(",")
                    if srcset_parts:
                        first_src = srcset_parts[0].strip().split(" ")[0]
                        if first_src:
                            value = first_src
                if value:
                    joined_value = self._join_and_check_url(value)
                    if joined_value:
                        final_src = joined_value
                        is_data = False
                        break
        if not final_src:
            return None

        width = element.get("width", "")
        height = element.get("height", "")
        if (width == "1" and height == "1") or (width == "0" and height == "0"):
            return None
        if self._is_tracking_pixel(final_src):
            return None

        metadata = self._create_metadata(element)
        image_obj = Image(
            src=final_src,
            alt=self._normalize_text(element.get("alt", "")),
            width=width,
            height=height,
            title=element.get("title", ""),
            loading=element.get("loading", ""),
            is_data_url=is_data,
            metadata=metadata,
        )
        if add:
            self._add_content(image_obj)
            return None
        else:
            return image_obj

    def _parse_picture(self, element, add=True):
        sources = element.find_all("source")
        all_sources = []
        for source in sources:
            for attr_name, attr_value in source.attrs.items():
                if "srcset" in attr_name.lower():
                    entries = attr_value.split(",")
                    for entry in entries:
                        parts = entry.strip().split(" ")
                        if parts:
                            candidate_url = self._join_and_check_url(parts[0])
                            if candidate_url:
                                all_sources.append(candidate_url)
        img = element.find("img")
        best_src = ""
        if img and img.has_attr("src"):
            joined_img_src = self._join_and_check_url(img["src"])
            if joined_img_src:
                best_src = joined_img_src
        if best_src:
            is_data_url_img, _ = is_data_url(best_src)
            if is_data_url_img and all_sources:
                best_src = all_sources[0]
        elif all_sources:
            best_src = all_sources[0]
        if not best_src:
            return None
        if self._is_tracking_pixel(best_src):
            return None

        metadata = self._create_metadata(element)
        image_obj = Image(
            src=best_src,
            alt=self._normalize_text(img.get("alt", "")) if img else "",
            width=img.get("width", "") if img else "",
            height=img.get("height", "") if img else "",
            title=img.get("title", "") if img else "",
            loading=img.get("loading", "") if img else "",
            all_sources=all_sources,
            metadata=metadata,
        )
        if add:
            self._add_content(image_obj)
            return None
        else:
            return image_obj

    def _parse_figure(self, element, add=True):
        figcaption = element.find("figcaption")
        caption = self._normalize_text(figcaption.get_text()) if figcaption else ""

        image_obj = None
        picture = element.find("picture")
        if picture:
            image_obj = self._parse_picture(picture, add=False)
        else:
            imgs = element.find_all("img")
            best_img = self._select_best_image(imgs) if imgs else None
            if best_img:
                image_obj = self._parse_img(best_img, add=False)

        if (not image_obj or not image_obj.src) or (
            image_obj and self._is_tracking_pixel(image_obj.src)
        ):
            if self.has_element_children(element):
                return self._extract_from_element(element, add)
            return

        # The final object represents the <figure>, so its metadata is used.
        metadata = self._create_metadata(element)
        image_obj.metadata = metadata
        image_obj.caption = caption

        if add:
            self._add_content(image_obj)

        return image_obj

    def _select_best_image(self, imgs):
        if not imgs:
            return None
        if len(imgs) == 1:
            return imgs[0]
        scored_imgs = []
        for img in imgs:
            score = 0
            try:
                width = int(img.get("width", "0"))
                height = int(img.get("height", "0"))
                if width > 100 and height > 100:
                    score += 10
                area = width * height
                score += min(area / 10000, 10)
            except ValueError:
                pass
            if img.get("alt"):
                score += 5
            cls = img.get("class", "")
            cls_str = " ".join(cls).lower() if isinstance(cls, list) else str(cls).lower()
            if any(x in cls_str for x in ["icon", "logo", "avatar", "thumbnail"]):
                score -= 5
            scored_imgs.append((score, img))
        scored_imgs.sort(reverse=True, key=lambda x: x[0])
        return scored_imgs[0][1] if scored_imgs else imgs[0]

    def _parse_audio(self, element, add=True):
        src = element.get("src", "")
        normalized_src = join_url(self.url, src) if src else ""
        sources = element.find_all("source")
        all_sources = []
        for source in sources:
            for attr_name, attr_value in source.attrs.items():
                if "src" in attr_name.lower():
                    normalized_url = join_url(self.url, attr_value)
                    all_sources.append({"url": normalized_url, "type": source.get("type", "")})
        tracks = []
        for track in element.find_all("track"):
            track_src = track.get("src", "")
            if track_src:
                tracks.append(
                    {
                        "url": join_url(self.url, track_src),
                        "kind": track.get("kind", ""),
                        "label": track.get("label", ""),
                        "srclang": track.get("srclang", ""),
                    }
                )

        final_src = (
            normalized_src if normalized_src else (all_sources[0]["url"] if all_sources else "")
        )
        if not final_src:
            return None

        metadata = self._create_metadata(element)
        audio_obj = Audio(
            src=final_src,
            controls=element.has_attr("controls"),
            autoplay=element.has_attr("autoplay"),
            loop=element.has_attr("loop"),
            muted=element.has_attr("muted"),
            preload=element.get("preload", ""),
            sources=all_sources,
            tracks=tracks,
            metadata=metadata,
        )
        if add:
            self._add_content(audio_obj)
            return None
        else:
            return audio_obj

    def _parse_video(self, element, add=True):
        src = element.get("src", "")
        normalized_src = join_url(self.url, src) if src else ""
        sources = element.find_all("source")
        all_sources = []
        for source in sources:
            for attr_name, attr_value in source.attrs.items():
                if "src" in attr_name.lower():
                    normalized_url = join_url(self.url, attr_value)
                    all_sources.append({"url": normalized_url, "type": source.get("type", "")})
        poster = element.get("poster", "")
        normalized_poster = join_url(self.url, poster) if poster else ""
        tracks = []
        for track in element.find_all("track"):
            track_src = track.get("src", "")
            if track_src:
                tracks.append(
                    {
                        "url": join_url(self.url, track_src),
                        "kind": track.get("kind", ""),
                        "label": track.get("label", ""),
                        "srclang": track.get("srclang", ""),
                    }
                )

        final_src = (
            normalized_src if normalized_src else (all_sources[0]["url"] if all_sources else "")
        )
        if not final_src:
            return None

        metadata = self._create_metadata(element)
        video_obj = Video(
            src=final_src,
            poster=normalized_poster,
            width=element.get("width", ""),
            height=element.get("height", ""),
            controls=element.has_attr("controls"),
            autoplay=element.has_attr("autoplay"),
            loop=element.has_attr("loop"),
            muted=element.has_attr("muted"),
            preload=element.get("preload", ""),
            playsinline=element.has_attr("playsinline"),
            sources=all_sources,
            tracks=tracks,
            provider=element.get("provider", "unknown"),
            metadata=metadata,
        )
        if add:
            self._add_content(video_obj)
            return None
        else:
            return video_obj

    def _join_and_check_url(self, path):
        joined = join_url(url=self.url, path=path)
        if not joined:
            return None
        if self.domain_filter.should_block(url=joined):
            return None
        return joined
