import re
import copy

import bs4

VALID_MATCH_TYPES = {"exact", "partial", "regex"}

_MAIN_STRING_TYPES = bs4.element.Tag.MAIN_CONTENT_STRING_TYPES


def _stripped_text_lengths(root) -> dict[int, int]:
    """``id(tag) -> len(tag.get_text(strip=True))`` for ``root`` and every tag in it,
    counting the strings bs4's default ``get_text`` counts (NavigableString and
    CData), in ONE post-order walk instead of one subtree walk per tag. Only valid
    for a tag whose ``interesting_string_types`` are those defaults (the caller
    checks)."""
    lengths: dict[int, int] = {}
    if not isinstance(root, bs4.element.Tag):
        return lengths
    stack = [(root, iter(root.contents))]
    totals = [0]
    while stack:
        node, children = stack[-1]
        child = next(children, None)
        if child is None:
            stack.pop()
            total = totals.pop()
            lengths[id(node)] = total
            if totals:
                totals[-1] += total
        elif isinstance(child, bs4.element.Tag):
            stack.append((child, iter(child.contents)))
            totals.append(0)
        elif type(child) in _MAIN_STRING_TYPES:
            totals[-1] += len(child.strip())
    return lengths


class ScrapeFilter:
    def __init__(self, content_filter_config=None, main_content_config=None):
        """
        Initialize with the new config structure

        Args:
            config: Dict with "content_filter" and "main_content" keys
        """
        self.content_filters = content_filter_config or []
        self.main_content_selectors = main_content_config or []

    def _check_string_match(self, text: str, value: str, match_type: str) -> bool:
        """Match string based on match type"""
        if match_type == "exact" and text == value:
            return True
        elif match_type == "partial" and value in text:
            return True
        elif match_type == "regex":
            try:
                pattern = re.compile(value)
                if pattern.search(text):
                    return True
            except re.error:
                pass
        return False

    def _check_class_attribute(self, element: bs4.element.Tag, value: str, match_type: str) -> bool:
        """Check class attribute"""
        if not element.has_attr("class"):
            return False

        element_classes = element["class"]

        if " " in value:
            value_classes = value.split()
            return all(vc in element_classes for vc in value_classes)
        else:
            for cls in element_classes:
                if self._check_string_match(cls, value, match_type):
                    return True

        return False

    def _check_style_attribute(self, element: bs4.element.Tag, value: str, match_type: str) -> bool:
        """Check style attribute"""
        if not element.has_attr("style"):
            return False

        style_str = element["style"].lower().strip()
        if not style_str:
            return False

        styles = {}
        for s in style_str.split(";"):
            if ":" in s:
                k, v = s.split(":", 1)
                styles[k.strip()] = v.strip()

        if ":" in value:
            prop, val = value.split(":", 1)
            prop = prop.strip()
            val = val.strip()

            if prop in styles:
                return self._check_string_match(styles[prop], val, match_type)
        else:
            return value in styles

        return False

    def check_element(
        self, element: bs4.element.Tag, attribute: str, values: list[str], match_type: str
    ) -> tuple[bool, str | None]:
        """
        Check if element matches the given attribute and values using the specified match type

        Returns:
            Tuple of (is_match, trigger_value)
        """
        if match_type not in VALID_MATCH_TYPES:
            return False, None

        if attribute == "tag":
            if not element.name:
                return False, None

            for value in values:
                if self._check_string_match(element.name, value, match_type):
                    return True, value
            return False, None

        if attribute == "text":
            text = element.get_text(strip=True)
            if not text:
                return False, None

            for value in values:
                if self._check_string_match(text, value, match_type):
                    return True, value
            return False, None

        if attribute == "class":
            for value in values:
                if self._check_class_attribute(element, value, match_type):
                    return True, value
            return False, None

        if attribute == "style":
            for value in values:
                if self._check_style_attribute(element, value, match_type):
                    return True, value
            return False, None

        if not element.has_attr(attribute):
            return False, None

        attr_value = element[attribute]

        if isinstance(attr_value, list):
            for value in values:
                for av in attr_value:
                    if self._check_string_match(str(av), value, match_type):
                        return True, value
        else:
            for value in values:
                if self._check_string_match(str(attr_value), value, match_type):
                    return True, value

        return False, None

    # ------------------------------------------------------------------
    # Compiled matching — the SAME answers as `check_element`, without
    # rescanning per element. `filter_soup` asks every element every filter;
    # `check_element` answers each question by looping every value (and, for
    # the "text" filter, by extracting the element's whole subtree text), so a
    # page cost elements x values and elements x subtree. Each filter is
    # compiled ONCE per pass into a check that answers the common case from a
    # set lookup, an alternation search, or a per-element text LENGTH computed
    # for the whole tree in one walk — and hands every case it cannot settle
    # cheaply (a hit whose trigger needs the ordered loop, regex values,
    # multi-valued attributes, a tag created with a string class, an unusual
    # config) to `check_element` itself, so the trigger value is always the
    # one the ordered loop names. Pinned by tests/test_parse_identity.py (output)
    # and tests/test_parse_works_on_one_tree.py (the text rule's call count).
    # ------------------------------------------------------------------

    def _compile_config(self, filter_config, target, state: dict) -> list[tuple[str, object, object]]:
        """One rule's checks, compiled the first time the loop reaches that rule (so a
        malformed rule fails exactly where reading it per element used to)."""
        attribute = filter_config.get("attribute")
        if not attribute:
            return []
        checks: list[tuple[str, object, object]] = []
        for match_type_str in ["exact", "partial", "regex"]:
            values = filter_config.get(match_type_str, [])
            if not values:
                continue
            if attribute == "text" and match_type_str != "regex" and state.get("text_lengths") is None:
                state["text_lengths"] = _stripped_text_lengths(target)
            check = self._compile_check(attribute, values, match_type_str, state.get("text_lengths"))
            checks.append((match_type_str, check, attribute))
        return checks

    def _compile_check(self, attribute, values, match_type: str, text_lengths):
        def generic(element):
            return self.check_element(element, attribute, values, match_type)

        if (
            match_type not in VALID_MATCH_TYPES
            or not isinstance(attribute, str)
            or not isinstance(values, (list, tuple))
            or not all(isinstance(v, str) for v in values)
            or match_type == "regex"
            or attribute == "style"
        ):
            return generic

        if match_type == "partial":
            # Existence only: some value is a substring of the string. A hit is
            # then answered by the ordered loop, which names the right value.
            any_value = re.compile("|".join(re.escape(v) for v in values))

        if attribute == "tag":
            if match_type == "exact":
                first = {}
                for v in values:
                    first.setdefault(v, v)

                def tag_exact(element):
                    if not element.name:
                        return False, None
                    hit = first.get(element.name)
                    return (True, hit) if hit is not None else (False, None)

                return tag_exact

            def tag_partial(element):
                if not element.name or any_value.search(element.name) is None:
                    return False, None
                return generic(element)

            return tag_partial

        if attribute == "text":
            lengths = {len(v) for v in values}
            shortest = min(lengths)

            def text_check(element):
                types = element.interesting_string_types
                if types is not None and types != _MAIN_STRING_TYPES:
                    return generic(element)
                n = text_lengths.get(id(element))
                if n is None:
                    return generic(element)
                # get_text(strip=True) is the stripped strings joined with "",
                # so its length is exactly n: "" never matches, an exact value
                # only at its own length, a substring only when it fits.
                if n == 0:
                    return False, None
                if match_type == "exact" and n not in lengths:
                    return False, None
                if match_type == "partial" and n < shortest:
                    return False, None
                return generic(element)

            return text_check

        if attribute == "class":
            plain = [v for v in values if " " not in v]
            if match_type == "exact" and len(plain) == len(values):
                first_index = {}
                for i, v in enumerate(values):
                    first_index.setdefault(v, i)

                def class_exact(element):
                    if not element.has_attr("class"):
                        return False, None
                    classes = element["class"]
                    if not isinstance(classes, list) or not all(isinstance(c, str) for c in classes):
                        return generic(element)
                    best = None
                    for c in classes:
                        i = first_index.get(c)
                        if i is not None and (best is None or i < best):
                            best = i
                    return (True, values[best]) if best is not None else (False, None)

                return class_exact

            if match_type == "partial" and len(plain) == len(values):

                def class_partial(element):
                    if not element.has_attr("class"):
                        return False, None
                    classes = element["class"]
                    if not isinstance(classes, list) or not all(isinstance(c, str) for c in classes):
                        return generic(element)
                    for c in classes:
                        if any_value.search(c) is not None:
                            return generic(element)
                    return False, None

                return class_partial

            return generic

        # Any other attribute: compared as one string unless multi-valued.
        if match_type == "exact":
            value_set = set(values)

            def attr_exact(element):
                if not element.has_attr(attribute):
                    return False, None
                attr_value = element[attribute]
                if isinstance(attr_value, list):
                    return generic(element)
                s = str(attr_value)
                return (True, s) if s in value_set else (False, None)

            return attr_exact

        def attr_partial(element):
            if not element.has_attr(attribute):
                return False, None
            attr_value = element[attribute]
            if isinstance(attr_value, list):
                return generic(element)
            if any_value.search(str(attr_value)) is None:
                return False, None
            return generic(element)

        return attr_partial

    def find_main_content(self, soup: bs4.BeautifulSoup) -> bs4.element.Tag | None:
        """
        Find and extract main content based on selectors.
        If no selectors provided or no matches found, returns None.
        """
        if not self.main_content_selectors:
            return None

        main_content = soup.new_tag("div")
        found_any = False
        for selector in self.main_content_selectors:
            elements = soup.select(selector)
            for element in elements:
                found_any = True
                element_copy = copy.deepcopy(element)
                main_content.append(element_copy)

        return main_content if found_any else None

    def filter_soup(
        self,
        soup: bs4.BeautifulSoup,
        main_content_config=None,
        content_filter_config=None,
        remove: bool = False,
        copy_input: bool = True,
    ) -> bs4.BeautifulSoup:
        """
        Filter soup based on configurations.
        If main_content selectors are provided, only filter within that content.

        ``copy_input=False`` filters ``soup`` IN PLACE instead of a deep copy —
        for a caller that owns a throwaway tree (the parse pipeline hands over
        the noise pass's output and never reads it again).
        """
        if main_content_config is not None:
            self.main_content_selectors = main_content_config

        if content_filter_config is not None:
            self.content_filters = content_filter_config

        processed_soup = copy.deepcopy(soup) if copy_input else soup
        main_content = self.find_main_content(processed_soup)
        target_soup = main_content if main_content else processed_soup

        elements_to_remove = []
        protected_tags = ["ContentFilter", "body", "html"]
        compiled: dict[int, list] = {}
        compile_state: dict = {}

        for element in target_soup.find_all():
            if element.name in protected_tags:
                continue

            if element.parent and element.parent.name == "ContentFilter":
                continue

            for index, filter_config in enumerate(self.content_filters):
                checks = compiled.get(index)
                if checks is None:
                    checks = compiled[index] = self._compile_config(filter_config, target_soup, compile_state)
                is_match = False  # set default to prevent reuse between match_type iterations

                for match_type_str, check, attribute in checks:
                    is_match, trigger_value = check(element)

                    if is_match:
                        if remove:
                            elements_to_remove.append(element)
                        else:
                            filter_tag = processed_soup.new_tag(
                                "ContentFilter",
                                type=attribute,
                                match_type=match_type_str,
                                trigger_item=str(trigger_value),
                            )
                            element.wrap(filter_tag)
                        break

                if is_match:
                    break

        if remove:
            for element in elements_to_remove:
                element.decompose()

        if main_content:
            for child in list(processed_soup.body.children):
                child.decompose()
            processed_soup.body.append(main_content)

        return processed_soup
