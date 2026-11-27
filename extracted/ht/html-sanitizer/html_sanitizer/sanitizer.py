import re
import unicodedata
from collections import deque

import lxml.html
import lxml.html.clean
from lxml import etree
from lxml.html import defs


__all__ = ("Sanitizer",)


def sanitize_href(href):
    """
    Verify that a given href is benign and allowed.

    This is a stupid check, which probably should be much more elaborate
    to be safe.
    """
    if href.startswith(("/", "mailto:", "http:", "https:", "#", "tel:")):
        return href
    return "#"


typographic_whitespace_names = [
    "NO-BREAK SPACE",
    "EN QUAD",
    "EM QUAD",
    "EN SPACE",
    "EM SPACE",
    "THREE-PER-EM SPACE",
    "FOUR-PER-EM SPACE",
    "SIX-PER-EM SPACE",
    "FIGURE SPACE",
    "PUNCTUATION SPACE",
    "THIN SPACE",
    "HAIR SPACE",
    "NARROW NO-BREAK SPACE",
    "MEDIUM MATHEMATICAL SPACE",
    "IDEOGRAPHIC SPACE",
]

typographic_whitespace = "".join(
    {unicodedata.lookup(n) for n in typographic_whitespace_names}
)


def bold_span_to_strong(element):
    if element.tag == "span" and "bold" in element.get("style", ""):
        element.tag = "strong"
    return element


def italic_span_to_em(element):
    if element.tag == "span" and "italic" in element.get("style", ""):
        element.tag = "em"
    return element


def tag_replacer(from_, to_):
    def replacer(element):
        if element.tag == from_:
            element.tag = to_
        return element

    return replacer


def target_blank_noopener(element):
    if (
        element.tag == "a"
        and element.attrib.get("target") == "_blank"
        and "noopener" not in element.attrib.get("rel", "")
    ):
        element.attrib["rel"] = " ".join(
            part for part in (element.attrib.get("rel", ""), "noopener") if part
        )
    return element


def anchor_id_to_name(element):
    if (
        element.tag == "a"
        and element.attrib.get("id")
        and not element.attrib.get("name")
    ):
        element.attrib["name"] = element.attrib["id"]
    return element


def filter_control_characters(text):
    """Filter out control characters that lxml cannot handle."""
    if not text:
        return text
    return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)


def drop_tag(element):
    """
    Same as lxml's ``element.drop_tag()``, but runs in constant time instead
    of time proportional to the number of siblings (lxml uses
    ``parent.index(element)``)
    """
    parent = element.getparent()
    previous = element.getprevious()
    if element.text and isinstance(element.tag, str):
        if previous is None:
            parent.text = (parent.text or "") + element.text
        else:
            previous.tail = (previous.tail or "") + element.text
    if element.tail:
        if len(element):
            last = element[-1]
            last.tail = (last.tail or "") + element.tail
        elif previous is None:
            parent.text = (parent.text or "") + element.tail
        else:
            previous.tail = (previous.tail or "") + element.tail
        element.tail = None
    for child in list(element):
        element.addprevious(child)
    parent.remove(element)


def normalize_whitespace_in_text_or_tail(
    element,
    *,
    whitespace_re=None,
    keep_typographic_whitespace=False,
    normalize_text=True,
    normalize_tail=True,
):
    # Always filter control characters regardless of whitespace settings
    if element.text:
        element.text = filter_control_characters(element.text)
    if element.tail:
        element.tail = filter_control_characters(element.tail)

    if keep_typographic_whitespace:
        return element

    if whitespace_re is None:
        whitespace_re = re.compile(r"\s+")
    if element.text and normalize_text:
        while True:
            text = whitespace_re.sub(" ", element.text)
            if element.text == text:
                break
            element.text = text

    if element.tail and normalize_tail:
        while True:
            text = whitespace_re.sub(" ", element.tail)
            if element.tail == text:
                break
            element.tail = text

    return element


DEFAULT_SETTINGS = {
    "tags": {
        "a",
        "h1",
        "h2",
        "h3",
        "strong",
        "em",
        "p",
        "ul",
        "ol",
        "li",
        "br",
        "sub",
        "sup",
        "hr",
    },
    "attributes": {"a": ("href", "name", "target", "title", "rel")},
    "empty": {"hr", "a", "br"},
    "separate": {"a", "p", "li"},
    "whitespace": {"br"},
    "preserve_whitespace": {"pre"},
    "keep_typographic_whitespace": False,
    "drop_disallowed_contents": False,
    "add_nofollow": False,
    "autolink": False,
    "embedded_hosts": set(),
    "sanitize_href": sanitize_href,
    "element_preprocessors": [
        # convert span elements into em/strong if a matching style rule
        # has been found. strong has precedence, strong & em at the same
        # time is not supported
        bold_span_to_strong,
        italic_span_to_em,
        tag_replacer("b", "strong"),
        tag_replacer("i", "em"),
        tag_replacer("form", "p"),
        target_blank_noopener,
        anchor_id_to_name,
    ],
    "element_postprocessors": [],
}


# The tags lxml-html-clean's Cleaner kills (removes including their contents)
# and removes (keeping their contents) depending on its flags
CLEANER_TAGS = [
    ("scripts", {"script"}, set()),
    ("comments", {etree.Comment}, set()),
    ("processing_instructions", {etree.ProcessingInstruction}, set()),
    ("style", {"style"}, set()),
    ("links", {"link"}, set()),
    ("meta", {"meta"}, set()),
    ("page_structure", set(), {"head", "html", "title"}),
    ("embedded", {"applet"}, {"iframe", "embed", "layer", "object", "param"}),
    ("frames", defs.frame_tags, set()),
    ("forms", {"button", "input", "select", "textarea"}, {"form"}),
    ("annoying_tags", set(), {"blink", "marquee"}),
]


def coerce_to_set(value):
    if isinstance(value, set):
        return value
    elif isinstance(value, tuple | list):
        return set(value)
    raise TypeError(f"Expected a set but got value {value!r} of type {type(value)}")


class Sanitizer:
    def __init__(self, settings=None):
        self.__dict__.update(DEFAULT_SETTINGS)
        self.__dict__.update(settings or {})

        # Allow iterables of any kind, not just sets.
        self.tags = coerce_to_set(self.tags)
        self.empty = coerce_to_set(self.empty)
        self.separate = coerce_to_set(self.separate)
        self.whitespace = coerce_to_set(self.whitespace)
        self.embedded_hosts = coerce_to_set(self.embedded_hosts)
        # Preserving whitespace inside tags which are removed later would
        # leak unnormalized whitespace into the output.
        self.preserve_whitespace = coerce_to_set(self.preserve_whitespace) & self.tags
        self.attributes = {
            tag: coerce_to_set(attributes)
            for tag, attributes in self.attributes.items()
        }

        if self.keep_typographic_whitespace:
            re_whitespace = r"[^\S%s]" % typographic_whitespace
        else:
            re_whitespace = r"\s"

        self.only_whitespace_re = re.compile(rf"^{re_whitespace}*$")
        self.whitespace_re = re.compile(rf"{re_whitespace}+")

        # Validate the settings.
        if not self.tags:
            raise TypeError(
                "Empty list of allowed tags is not supported by the underlying"
                " lxml cleaner. If you really do not want to pass any tags"
                " pass a made-up tag name which will never exist in your"
                " document."
            )
        if not self.tags.issuperset(self.empty):
            raise TypeError(
                f'Tags in "empty", but not allowed: {self.empty - self.tags!r}'
            )
        if not self.tags.issuperset(self.separate):
            raise TypeError(
                f'Tags in "separate", but not allowed: {self.separate - self.tags!r}'
            )
        if not self.tags.issuperset(self.attributes.keys()):
            raise TypeError(
                f'Tags in "attributes", but not allowed: {set(self.attributes.keys()) - self.tags!r}'
            )

        anchor_attributes = self.attributes.get("a", ())
        if "target" in anchor_attributes and "rel" not in anchor_attributes:
            raise TypeError(
                'Always allow "rel" when allowing "target" as anchor attribute'
            )

    @staticmethod
    def is_mergeable(e1, e2):
        """
        Decide if the adjacent elements of the same type e1 and e2 can be
        merged. This can be overriden to honouring distinct classes etc.
        """
        return True

    def normalize_whitespace(self, element):
        inside = any(e.tag in self.preserve_whitespace for e in element.iterancestors())
        return normalize_whitespace_in_text_or_tail(
            element,
            whitespace_re=self.whitespace_re,
            keep_typographic_whitespace=self.keep_typographic_whitespace,
            normalize_text=not inside and element.tag not in self.preserve_whitespace,
            normalize_tail=not inside,
        )

    def remove_elements(self, doc, drop, *, normalize=True):
        """
        Remove all elements in ``drop`` (see ``unwrap_children``) from the
        document in linear time
        """
        if drop:
            for parent in reversed([doc, *doc.iterdescendants()]):
                self.unwrap_children(parent, drop, normalize=normalize)

    def remove_like_cleaner(self, doc, cleaner):
        """
        Remove the elements the lxml-html-clean ``Cleaner`` would remove
        because it does this one by one which takes quadratic time

        This is only an optimization, the cleaner still runs afterwards.
        """
        kill = set(cleaner.kill_tags or ())
        remove = set(cleaner.remove_tags or ())
        for flag, kill_tags, remove_tags in CLEANER_TAGS:
            if getattr(cleaner, flag):
                kill.update(kill_tags)
                remove.update(remove_tags)
        if "head" in kill or "head" in remove:
            kill.add("base")

        drop = {}
        for element in doc.iterdescendants():
            if element.tag in kill:
                mode = "tree"
            elif element.tag in remove:
                mode = "tag"
            else:
                continue
            if not cleaner.allow_element(element):
                drop[element] = mode
        self.remove_elements(doc, drop, normalize=False)

    def clean(self, doc, **kwargs):
        cleaner = lxml.html.clean.Cleaner(**kwargs)
        self.remove_like_cleaner(doc, cleaner)
        cleaner(doc)

    def unwrap_children(self, parent, drop, *, normalize=True):
        """
        Remove the children of ``parent`` which are keys of ``drop``. The
        value ``"tag"`` keeps the text and the children of the removed
        element (like lxml's ``drop_tag()``), ``"tree"`` only keeps the tail
        (like lxml's ``drop_tree()``).

        Removing elements one by one takes quadratic time when there are many
        of them, because each removal moves the text accumulated so far to
        the previous sibling. This collects text parts and joins them once.
        """
        children = list(parent)
        if not any(child in drop for child in children):
            return

        # The text being extended is either parent.text (target is None) or
        # the tail of the last child which is kept.
        target = None
        parts = [parent.text or ""]

        def flush():
            if len(parts) > 1:
                text = "".join(parts) or None
                if target is None:
                    parent.text = text
                    if normalize:
                        self.normalize_whitespace(parent)
                else:
                    target.tail = text
                    if normalize:
                        self.normalize_whitespace(target)

        for child in children:
            mode = drop.pop(child, None)
            if mode is None:
                flush()
                target = child
                parts = [child.tail or ""]
                continue

            if mode == "tag":
                if isinstance(child.tag, str):  # Not a comment etc.
                    parts.append(child.text or "")
                for grandchild in list(child):
                    flush()
                    child.addprevious(grandchild)
                    target = grandchild
                    parts = [grandchild.tail or ""]
            parts.append(child.tail or "")
            parent.remove(child)
        flush()

    def merge_adjacent(self, doc):
        """
        Merge adjacent elements of the same tag type if there is nothing but
        whitespace between them, e.g. ``<b>a</b> <b>b</b>`` to ``<b>a b</b>``

        Merges whole runs of elements at once so that the work done is linear
        in the size of the document.
        """
        mergeable = self.tags - self.separate
        stack = [doc]
        while stack:
            children = list(stack.pop())
            i = 0
            while i < len(children):
                element = children[i]
                i += 1
                stack.append(element)
                if element.tag not in mergeable:
                    continue

                run = []
                last = element
                while (
                    i < len(children)
                    and self.only_whitespace_re.match(last.tail or "")
                    and children[i].tag == element.tag
                    and self.is_mergeable(element, children[i])
                ):
                    last = children[i]
                    run.append(last)
                    i += 1
                if run:
                    self.merge_run(element, run)

    def merge_run(self, element, run):
        # The text being extended is either element.text (target is None) or
        # the tail of the last child. Collect its parts and join them once.
        target = element[-1] if len(element) else None
        parts = [(element.text if target is None else target.tail) or ""]

        def flush():
            text = "".join(parts) or None
            if target is None:
                element.text = text
            else:
                target.tail = text

        between = element.tail
        for nx in run:
            parts.extend((between or "", nx.text or ""))
            for child in list(nx):
                flush()
                element.append(child)
                target = child
                parts = [child.tail or ""]
            between = nx.tail
            nx.getparent().remove(nx)
        flush()
        element.tail = between

        self.normalize_whitespace(element)
        for child in element:
            self.normalize_whitespace(child)

    def sanitize(self, html):  # noqa: C901 -- I know.
        """
        Clean HTML code from ugly copy-pasted CSS and empty elements

        Removes everything not explicitly allowed in ``self.allowed_tags``.

        Requires ``lxml`` and, for especially broken HTML, ``beautifulsoup4``.
        """

        # normalize unicode
        if self.keep_typographic_whitespace:
            html = unicodedata.normalize("NFC", html)
        else:
            html = unicodedata.normalize("NFKC", html)

        html = "<div>%s</div>" % html
        try:
            doc = lxml.html.fromstring(html)
            lxml.html.tostring(doc, encoding="utf-8")
        except Exception:  # noqa: BLE001 -- we could and maybe should be more specific
            from lxml.html import soupparser  # noqa: PLC0415

            doc = soupparser.fromstring(html)

        self.clean(
            doc,
            remove_unknown_tags=False,
            # Remove style *tags* if not explicitly allowed
            style="style" not in self.tags,
            # Do not strip out style attributes; we still need the style
            # information to convert spans into em/strong tags
            safe_attrs_only=False,
            inline_style=False,
            # Do not strip all form tags; we will filter them below
            forms=False,
            host_whitelist=self.embedded_hosts,
        )

        # walk the tree recursively, because we want to be able to remove
        # previously emptied elements completely
        backlog = deque(doc.iterdescendants())

        doc = self.normalize_whitespace(doc)

        # Elements to remove, see unwrap_children. Elements are only marked
        # and removed when processing their parent; removing them right away
        # takes quadratic time.
        drop = {}

        while True:
            try:
                element = backlog.pop()
            except IndexError:
                break

            # All children have been processed already
            self.unwrap_children(element, drop)

            for processor in self.element_preprocessors:
                element = processor(element)

            if self.drop_disallowed_contents and element.tag not in self.tags:
                drop[element] = "tree"
                continue

            element = self.normalize_whitespace(element)

            # remove empty tags if they are not explicitly allowed
            if (
                (not element.text or self.only_whitespace_re.match(element.text))
                and element.tag not in self.empty
                and not len(element)
            ):
                drop[element] = "tag"
                continue

            # remove tags which only contain whitespace and/or <br>s
            if (
                element.tag not in self.empty
                and self.only_whitespace_re.match(element.text or "")
                and {e.tag for e in element} <= self.whitespace
                and all(self.only_whitespace_re.match(e.tail or "") for e in element)
            ):
                drop[element] = "tree"
                continue

            if element.tag in {"li", "p"}:
                # remove p-in-li and p-in-p tags
                for p in element.findall("p"):
                    if getattr(p, "text", None):
                        p.text = " " + p.text + " "
                    drop[p] = "tag"
                self.unwrap_children(element, drop)

                # remove list markers, maybe copy-pasted from word or whatever
                if element.text:
                    element.text = filter_control_characters(
                        re.sub(r"^\s*(-|\*|&#183;)\s+", "", element.text)
                    )

            elif element.tag in self.whitespace:
                # Drop the next element if
                # 1. it is a <br> too and 2. there is no content in-between
                # (siblings marked for removal do not count)
                only_whitespace = self.only_whitespace_re.match(element.tail or "")
                nx = element.getnext()
                while only_whitespace and nx is not None and nx in drop:
                    only_whitespace = (
                        drop[nx] == "tree"
                        or self.only_whitespace_re.match(nx.text or "")
                    ) and self.only_whitespace_re.match(nx.tail or "")
                    nx = nx.getnext()
                if only_whitespace and nx is not None and nx.tag == element.tag:
                    drop[nx] = "tag"

            # No text before first child and first child is a <br>: Drop it,
            # and all following <br>s too
            dropped = False
            while not element.text:
                first = next(iter(element), None)
                if first is None or first.tag not in self.whitespace:
                    break
                drop_tag(first)
                dropped = True
            if dropped:
                # Process element again
                backlog.append(element)
                continue

            for processor in self.element_postprocessors:
                element = processor(element)

            # remove all attributes which are not explicitly allowed
            allowed = self.attributes.get(element.tag, [])
            for key in element.keys():  # noqa: SIM118 (do not remove .keys())
                if key not in allowed:
                    del element.attrib[key]
                elif not self.keep_typographic_whitespace:
                    element.set(key, self.whitespace_re.sub(" ", element.get(key)))

            # Clean hrefs so that they are benign
            href = element.get("href")
            if href is not None:
                element.set("href", self.sanitize_href(href))

            element = self.normalize_whitespace(element)

        self.unwrap_children(doc, drop)
        self.merge_adjacent(doc)

        if self.autolink is True:
            lxml.html.clean.autolink(doc)
        elif isinstance(self.autolink, dict):
            lxml.html.clean.autolink(doc, **self.autolink)

        # Remove disallowed tags (but keep their contents) here and not in the
        # cleaner below, because lxml's drop_tag() takes quadratic time
        self.remove_elements(
            doc,
            {
                element: "tag"
                for element in doc.iterdescendants()
                if isinstance(element.tag, str) and element.tag not in self.tags
            },
        )

        # Run cleaner again, but this time with even more strict settings
        self.clean(
            doc,
            allow_tags=self.tags,
            remove_unknown_tags=False,
            safe_attrs_only=False,  # Our attributes allowlist is sufficient.
            add_nofollow=self.add_nofollow,
            forms=False,
            host_whitelist=self.embedded_hosts,
        )

        html = lxml.html.tostring(doc, encoding="unicode")

        # add a space before the closing slash in empty tags
        html = re.sub(r"<([^/>]+)/>", r"<\1 />", html)

        # remove wrapping tag needed by XML parser
        html = re.sub(r"^<div>|</div>$", "", html)

        return html
