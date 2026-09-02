from dataclasses import dataclass, field
from typing import Any, Union
from collections import defaultdict

from tabulate import tabulate


@dataclass
class ElementMetadata:
    """Holds metadata about the source HTML element."""

    tag: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    filtered: bool = False
    filter_details: dict | None = None


ContentUnion = Union[
    "TextContent",
    "CodeBlock",
    "Quote",
    "ListElement",
    "Table",
    "Header",
    "Image",
    "Audio",
    "Video",
]


@dataclass
class BaseContent:
    def to_content(self, settings: "ExtractionSettings") -> str:
        raise NotImplementedError

    def to_data(self, settings: "ExtractionSettings") -> Any:
        raise NotImplementedError

    def get(self, settings: "ExtractionSettings") -> Any:
        if settings.use_data_format:
            return self.to_data(settings)
        else:
            return self.to_content(settings)

    def is_allowed(self, settings: "ExtractionSettings") -> bool:
        return self.type in settings.allowed_types


@dataclass
class TextContent(BaseContent):
    type: str = field(default="text", init=False)
    content: str
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""
        if settings.remove_anchors:
            return self.content

        return self.metadata.attributes.get("fmt-txt") or self.content

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}
        if settings.remove_anchors:
            return {"type": "text", "content": self.content}
        content = self.metadata.attributes.get("fmt-txt") or self.content
        return {"type": "text", "content": content}


@dataclass
class CodeBlock(BaseContent):
    type: str = field(default="code", init=False)
    content: str
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}
        return {"type": "code", "content": self.content}

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""

        return f"```\n{self.content}\n```"


@dataclass
class Quote(BaseContent):
    type: str = field(default="quote", init=False)
    content: str
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}
        return {"type": "quote", "content": self.content}

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""

        return f"“{self.content}”"


@dataclass
class Image(BaseContent):
    type: str = field(default="image", init=False)
    src: str
    alt: str = ""
    width: str = ""
    height: str = ""
    title: str = ""
    loading: str = ""
    is_data_url: bool = False
    caption: str = ""
    all_sources: list[str] = field(default_factory=list)
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}

        return {
            "type": "image",
            "src": self.src,
            "alt": self.alt,
            "width": self.width,
            "height": self.height,
            "title": self.title,
            "caption": self.caption,
            "srcset": list(set(self.all_sources)),
        }

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""

        alt_text = ""
        title_text = ""

        if self.caption and self.caption.strip():
            alt_text = self.caption.strip()
        elif self.alt and self.alt.strip():
            alt_text = self.alt.strip()
        elif self.caption and self.alt:
            alt_text = self.caption if len(self.caption) > len(self.alt) else self.alt

        if self.src:
            src = self.src.strip()
            title_text = f' "{alt_text}"' if alt_text else ""
            return f"![{alt_text}]({src}{title_text})"

        return ""


@dataclass
class Audio(BaseContent):
    type: str = field(default="audio", init=False)
    src: str
    controls: bool = False
    autoplay: bool = False
    loop: bool = False
    muted: bool = False
    preload: str = ""
    sources: list[dict[str, str]] = field(default_factory=list)
    tracks: list[dict[str, str]] = field(default_factory=list)
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}

        return {"type": "audio", "src": self.src, "sources": self.sources, "tracks": self.tracks}

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""
        if self.src:
            return f"[Audio]({self.src})"
        return ""


@dataclass
class Video(BaseContent):
    type: str = field(default="video", init=False)
    src: str
    poster: str = ""
    width: str = ""
    height: str = ""
    controls: bool = False
    autoplay: bool = False
    loop: bool = False
    muted: bool = False
    preload: str = ""
    playsinline: bool = False
    sources: list[dict[str, str]] = field(default_factory=list)
    tracks: list[dict[str, str]] = field(default_factory=list)
    provider: str = ""
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}

        return {
            "type": "video",
            "src": self.src,
            "poster": self.poster,
            "width": self.width if self.width else None,
            "height": self.height if self.height else None,
            "sources": self.sources,
            "tracks": self.tracks,
            "provider": self.provider,
        }

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""

        if self.provider and self.provider.strip() and self.src:
            provider = self.provider.strip().capitalize()
            return f"[Watch {provider} Video]({self.src.strip()})"
        elif self.src:
            return f"[Watch Video]({self.src.strip()})"
        return ""


@dataclass
class ListElement(BaseContent):
    type: str = field(default="list", init=False)
    content: list[Any] = field(default_factory=list)
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def _flatten_python_list(self, items: list[Any], settings: "ExtractionSettings") -> list[str]:
        texts: list[str] = []
        for item in items:
            if isinstance(item, CodeBlock):
                code_content = item.to_content(settings)
                if code_content:
                    texts.append(code_content)
                continue

            if hasattr(item, "to_content"):
                content = item.to_content(settings)
                if content:
                    texts.append(str(content).replace("\n", " ").strip())

            elif isinstance(item, ListElement):
                if settings.remove_filtered and item.metadata.filtered:
                    continue
                texts.extend(self._flatten_python_list(item.content, settings))

            elif isinstance(item, dict):
                t = item.get("type")
                c = item.get("content")
                if t == "text" and isinstance(c, str):
                    texts.append(c.strip())
                elif t == "list" and isinstance(c, list):
                    texts.extend(self._flatten_python_list(c, settings))
                elif isinstance(c, str):
                    texts.append(c.strip())
                elif isinstance(c, list):
                    texts.extend(self._flatten_python_list(c, settings))

            elif isinstance(item, list):
                texts.extend(self._flatten_python_list(item, settings))

        return texts

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}

        return {
            "type": "list",
            "content": self._flatten_python_list(self.content, settings),
            "after": "",
            "before": "",
        }

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""

        lines = []
        for line in self._flatten_python_list(self.content, settings):
            if settings.remove_formatting:
                lines.append(f"{line}")
            else:
                lines.append(f"- {line}")
        return "\n".join(lines)

    def _extract_nested_allowed_content(self, content: list[ContentUnion], settings):
        items = []
        for item in content:
            if isinstance(item, list):
                nested_items = self._extract_nested_allowed_content(item, settings)
                if nested_items:
                    items.extend(nested_items)

            elif item.is_allowed(settings) and item.type != "text":
                items.append(item)
        return items

    def extract_nested_allowed_data(self, settings):
        items = self._extract_nested_allowed_content(self.content, settings)
        return [item.to_data(settings) for item in items]

    def extract_nested_allowed_content(self, settings):
        items = self._extract_nested_allowed_content(self.content, settings)
        return "\n".join([item.to_content(settings) for item in items])


@dataclass
class Table(BaseContent):
    type: str = field(default="table", init=False)
    content: list[dict[str, list[ContentUnion]]] = field(default_factory=list)
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def _flatten_cell_to_text(self, cell_content: list[ContentUnion], settings) -> str:
        result = []
        if isinstance(cell_content, TextContent):
            return cell_content.to_content(settings)

        if not isinstance(cell_content, list):
            cell_content = [cell_content]

        for item in cell_content:
            if hasattr(item, "to_content"):
                if (
                    settings.remove_filtered
                    and hasattr(item, "metadata")
                    and item.metadata.filtered
                ):
                    continue
                content = item.to_content(settings)
                if content:
                    result.append(str(content).replace("\n", " "))
        return " ".join(result)

    def _flatten_cell_to_data(
        self, cell_content: ContentUnion | list[ContentUnion], settings
    ) -> str:
        result = []
        items = cell_content if isinstance(cell_content, list) else [cell_content]
        for item in items:
            if hasattr(item, "to_content"):
                if (
                    not settings.remove_filtered
                    and hasattr(item, "metadata")
                    and item.metadata.filtered
                ):
                    continue
                content = item.to_content(settings)
                if content:
                    result.append(str(content))
        return "\n".join(result)

    def to_data(self, settings: "ExtractionSettings") -> dict:
        if settings.remove_filtered and self.metadata.filtered:
            return {}
        flattened_rows = []
        all_columns = set()
        for row in self.content:
            flattened_row = {}
            for column, cell_content in row.items():
                flattened_row[column] = self._flatten_cell_to_data(cell_content, settings)
                all_columns.add(column)
            if not any(val.strip() for val in flattened_row.values()):
                continue
            flattened_rows.append(flattened_row)
        normalized_rows = []
        for row in flattened_rows:
            normalized_row = {col: row.get(col, "") for col in all_columns}
            normalized_rows.append(normalized_row)

        return {
            "type": "table",
            "rows": normalized_rows,
            "before": "",
            "after": "",
        }

    def to_content(self, settings: "ExtractionSettings") -> str:
        if settings.remove_filtered and self.metadata.filtered:
            return ""
        if not self.content:
            return ""
        flattened_rows = []
        all_columns = set()
        for row in self.content:
            flattened_row = {}
            for column, cell_content in row.items():
                flattened_row[column] = self._flatten_cell_to_text(cell_content, settings)
                all_columns.add(column)
            if not any(val.strip() for val in flattened_row.values()):
                continue
            flattened_rows.append(flattened_row)
        normalized_rows = []
        for row in flattened_rows:
            normalized_row = {col: row.get(col, "") for col in all_columns}
            normalized_rows.append(normalized_row)

        if settings.remove_formatting:
            return tabulate(normalized_rows, tablefmt="plain", headers="keys")
        else:
            return tabulate(normalized_rows, tablefmt="simple", headers="keys")

    def _extract_nested_allowed_content(self, settings):
        items = []
        for row in self.content:
            for col_name, values in row.items():
                for value in values:
                    if value.is_allowed(settings) and value.type != "text":
                        items.append(value)

        return items

    def extract_nested_allowed_data(self, settings):
        items = self._extract_nested_allowed_content(settings)
        return [item.to_data(settings) for item in items]

    def extract_nested_allowed_content(self, settings):
        items = self._extract_nested_allowed_content(settings)
        return "\n".join([item.to_content(settings) for item in items])


@dataclass
class Header(BaseContent):
    type: str = field(default="header", init=False)
    level: int
    text: str
    content: list[ContentUnion] = field(default_factory=list)
    metadata: ElementMetadata = field(default_factory=ElementMetadata)

    def _flatten_to_data_lines(self, items: list[ContentUnion], settings) -> list[str]:
        lines = []
        for item in items:
            if not item.is_allowed(settings) and item.type != "header":
                continue

            if isinstance(item, CodeBlock):
                code = item.to_data(settings)
                if code:
                    lines.append(code)

            elif isinstance(item, ListElement) and "list" not in settings.allowed_types:
                allowed_items = item.extract_nested_allowed_data(settings)
                if allowed_items:
                    lines.extend(allowed_items)

            elif isinstance(item, Table) and "table" not in settings.allowed_types:
                allowed_items = item.extract_nested_allowed_data(settings)
                if allowed_items:
                    lines.extend(allowed_items)

            elif hasattr(item, "to_data"):
                if (
                    settings.remove_filtered
                    and hasattr(item, "metadata")
                    and item.metadata.filtered
                ):
                    continue
                content_block = item.to_data(settings)
                if content_block:
                    if isinstance(content_block, list):
                        lines.extend(content_block)
                    else:
                        lines.append(content_block)

            elif isinstance(item, list):
                for sub in item:
                    if hasattr(sub, "to_data"):
                        if (
                            settings.remove_filtered
                            and hasattr(sub, "metadata")
                            and sub.metadata.filtered
                        ):
                            continue
                        data = sub.to_data(settings)
                        if isinstance(data, list):
                            lines.extend(data)
                        else:
                            lines.append(data)

        return lines

    def _flatten_to_content_lines(self, items: list[ContentUnion], settings) -> list[str]:
        lines = []
        for item in items:
            if not item.is_allowed(settings) and item.type != "header":
                continue

            if isinstance(item, CodeBlock):
                code = item.to_content(settings)
                if code:
                    lines.extend(code.splitlines())

            elif isinstance(item, Table) and "table" not in settings.allowed_types:
                allowed_items_content = item.extract_nested_allowed_content(settings)
                if allowed_items_content.strip():
                    lines.extend(allowed_items_content.splitlines())

            elif isinstance(item, ListElement) and "list" not in settings.allowed_types:
                allowed_items_content = item.extract_nested_allowed_content(settings)
                if allowed_items_content.strip():
                    lines.extend(allowed_items_content.splitlines())

            elif hasattr(item, "to_content"):
                if (
                    settings.remove_filtered
                    and hasattr(item, "metadata")
                    and item.metadata.filtered
                ):
                    continue
                content_block = item.to_content(settings)
                if content_block:
                    lines.extend(content_block.splitlines())

            elif isinstance(item, list):
                for sub in item:
                    if hasattr(sub, "to_content"):
                        if (
                            settings.remove_filtered
                            and hasattr(sub, "metadata")
                            and sub.metadata.filtered
                        ):
                            continue
                        data = sub.to_content(settings)
                        if data:
                            lines.extend(data.splitlines())
        return lines

    def to_content(self, settings: "ExtractionSettings") -> str:
        if self.level == 0:
            header_line = ""
        else:
            if settings.remove_formatting:
                header_line = self.text
            else:
                header_line = f"{'#' * self.level} {self.text}"

        lines = []
        if self.is_allowed(settings):
            if not (settings.remove_filtered and self.metadata.filtered):
                lines.append(header_line)
        header_lines = self._flatten_to_content_lines(self.content, settings)
        if header_lines:
            lines.extend(header_lines)
        return "\n".join(lines)

    def to_data(self, settings: "ExtractionSettings") -> list:
        data_lines = []
        data = {"type": "header", "level": self.level, "content": self.text}
        if self.is_allowed(settings):
            if not (settings.remove_filtered and self.metadata.filtered):
                data_lines.append(data)

        flat_lines = self._flatten_to_data_lines(self.content, settings)
        if flat_lines:
            data_lines.extend(flat_lines)
        return data_lines


class ExtractionSettings:
    def __init__(self, allowed_children: list[str], options: list[str]):
        self.remove_formatting = "remove_formatting" in options
        self.remove_anchors = "remove_anchors" in options
        self.remove_filtered = "remove_filtered" in options
        self.use_content_format = False
        self.use_data_format = False
        self.organize_content_by_headers = "organize_content_by_headers" in options

        for opt in options:
            if opt == "content":
                self.use_content_format = True
                break
            elif opt == "data":
                self.use_data_format = True
                break

        self.allowed_types = set(allowed_children)
        if "paragraph" in self.allowed_types:
            self.allowed_types.remove("paragraph")
            self.allowed_types.add("text")
        if "header_text" in self.allowed_types:
            self.allowed_types.remove("header_text")
            self.allowed_types.add("header")

        # When organizing by headers, headers themselves must be allowed to structure the output
        if self.organize_content_by_headers:
            self.allowed_types.add("header")


@dataclass
class OrganizedData(BaseContent):
    content: list[ContentUnion] = field(default_factory=list)

    def _content_organized_by_headers(self, settings) -> dict[str, str]:
        result = {}
        header_counts = defaultdict(int)

        def _process_content(items: list[ContentUnion]):
            for item in items:
                if hasattr(item, "type") and item.type == "header":
                    header_text = item.text
                    header_counts[header_text] += 1
                    header_key = (
                        f"{header_text} ({header_counts[header_text]})"
                        if header_counts[header_text] > 1
                        else header_text
                    )
                    result[header_key] = item.to_content(settings)
                    if item.content:
                        _process_content(item.content)

        _process_content(self.content)
        return result

    def _ordered_content(self) -> list[ContentUnion]:
        """Document order, with the level-0 "unassociated" bucket moved last."""
        regular_content = [
            item for item in self.content if not (hasattr(item, "level") and item.level == 0)
        ]
        level_zero_content = [
            item for item in self.content if hasattr(item, "level") and item.level == 0
        ]
        return regular_content + level_zero_content

    def _extract_content(self, settings: "ExtractionSettings"):
        if settings.organize_content_by_headers:
            return self._content_organized_by_headers(settings)
        else:
            lines = []
            for item in self._ordered_content():
                item_lines = item.to_content(settings)
                if item_lines:
                    lines.extend(item_lines.splitlines())
            return "\n".join(lines)

    def _text_render_settings(self) -> "ExtractionSettings":
        from .extraction_rules import rules as _rules

        rule = next(r for r in _rules if r["name"] == "markdown_renderable")
        return ExtractionSettings(rule["allowed_children"], rule["options"])

    def to_text(self, add_markers: bool = False) -> str:
        """Render the whole page as readable text — the source of `text_data`.

        This lives HERE, on the object that owns the content, instead of in a
        standalone flattener. `text_data` used to be built by
        `json_to_text_lines()`, written for a legacy nested-dict page shape
        (`{"H1: Title": {...}, "Lists": [...]}`) that nothing in this package
        produces any more: handed an `OrganizedData` it matched no branch and
        returned "" for EVERY html page, taking `overview.char_count` with it.
        Reshaping the tree back into that dead format was the alternative, but
        the closest live shape is the `data` form, whose `{"type": ...}` keys
        leak type labels ("header", "text", "unassociated") into the prose.
        Every content type already knows how to render itself through
        `to_content()`, so rendering here reuses that one implementation — and
        produces exactly the text of the `markdown_renderable` rule.
        """
        settings = self._text_render_settings()
        if not add_markers:
            return self._extract_content(settings)

        blocks: list[str] = []
        for item in self._ordered_content():
            rendered = item.to_content(settings)
            if not rendered or not rendered.strip():
                continue
            kind = getattr(item, "type", "content")
            blocks.append(f"-- {kind} start --\n{rendered}\n-- {kind} end --")
        return "\n".join(blocks)

    def _extract_data(self, settings: "ExtractionSettings"):
        lines = []
        for item in self.content:
            item_lines = item.get(settings)
            if item_lines:
                lines.extend(item_lines)

        return lines

    def _extract_by_rule(self, rule):
        settings = ExtractionSettings(rule["allowed_children"], rule["options"])
        if settings.use_data_format:
            return self._extract_data(settings)
        else:
            return self._extract_content(settings)

    def extract(self, rules: list):
        output = {}
        for rule in rules:
            output[rule["name"]] = self._extract_by_rule(rule)

        return output
