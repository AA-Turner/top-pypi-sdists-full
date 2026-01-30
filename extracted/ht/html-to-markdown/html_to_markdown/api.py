"""High-level Python API backed by the Rust core."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, cast

import html_to_markdown._html_to_markdown as _rust
from html_to_markdown._html_to_markdown import (
    ConversionOptionsHandle as OptionsHandle,
)
from html_to_markdown._html_to_markdown import (
    InlineImageConfig,
    MetadataConfig,
)
from html_to_markdown.options import ConversionOptions, PreprocessingOptions

if TYPE_CHECKING:
    from html_to_markdown._html_to_markdown import ExtendedMetadata  # pragma: no cover
else:
    ExtendedMetadata = dict[str, object]  # type: ignore[assignment]


class InlineImage(TypedDict):
    """Inline image extracted during conversion."""

    data: bytes
    format: str
    filename: str | None
    description: str | None
    dimensions: tuple[int, int] | None
    source: Literal["img_data_uri", "svg_element"]
    attributes: dict[str, str]


class InlineImageWarning(TypedDict):
    """Warning produced during inline image extraction."""

    index: int
    message: str


def _as_list(value: set[str] | None) -> list[str]:
    return sorted(value) if value else []


def _rust_preprocessing(preprocessing: PreprocessingOptions) -> _rust.PreprocessingOptions:
    return _rust.PreprocessingOptions(
        enabled=preprocessing.enabled,
        preset=preprocessing.preset,
        remove_navigation=preprocessing.remove_navigation,
        remove_forms=preprocessing.remove_forms,
    )


def _rust_options(
    options: ConversionOptions | None,
    preprocessing: PreprocessingOptions | None,
) -> _rust.ConversionOptions | None:
    if options is None and preprocessing is None:
        return None

    if options is None:
        options = ConversionOptions()
    if preprocessing is None:
        preprocessing = PreprocessingOptions()

    return _rust.ConversionOptions(
        heading_style=options.heading_style,
        list_indent_type=options.list_indent_type,
        list_indent_width=options.list_indent_width,
        bullets=options.bullets,
        strong_em_symbol=options.strong_em_symbol,
        escape_asterisks=options.escape_asterisks,
        escape_underscores=options.escape_underscores,
        escape_misc=options.escape_misc,
        escape_ascii=options.escape_ascii,
        code_language=options.code_language,
        autolinks=options.autolinks,
        default_title=options.default_title,
        br_in_tables=options.br_in_tables,
        hocr_spatial_tables=options.hocr_spatial_tables,
        highlight_style=options.highlight_style,
        extract_metadata=options.extract_metadata,
        whitespace_mode=options.whitespace_mode,
        strip_newlines=options.strip_newlines,
        wrap=options.wrap,
        wrap_width=options.wrap_width,
        convert_as_inline=options.convert_as_inline,
        sub_symbol=options.sub_symbol,
        sup_symbol=options.sup_symbol,
        newline_style=options.newline_style,
        code_block_style=options.code_block_style,
        keep_inline_images_in=_as_list(options.keep_inline_images_in),
        preprocessing=_rust_preprocessing(preprocessing),
        debug=options.debug,
        strip_tags=_as_list(options.strip_tags),
        preserve_tags=_as_list(options.preserve_tags),
        encoding=options.encoding,
        skip_images=options.skip_images,
        output_format=options.output_format,
    )


def _build_inline_image_config(config: InlineImageConfig | dict[str, object] | None) -> InlineImageConfig:
    if config is None or isinstance(config, InlineImageConfig):
        return config or InlineImageConfig()

    max_decoded_size_bytes = config.get("max_decoded_size_bytes", config.get("maxDecodedSizeBytes"))
    filename_prefix = config.get("filename_prefix", config.get("filenamePrefix"))
    capture_svg = config.get("capture_svg", config.get("captureSvg"))
    infer_dimensions = config.get("infer_dimensions", config.get("inferDimensions"))

    defaults = InlineImageConfig()
    return InlineImageConfig(
        max_decoded_size_bytes=cast(
            "int", max_decoded_size_bytes if max_decoded_size_bytes is not None else defaults.max_decoded_size_bytes
        ),
        filename_prefix=cast(
            "str | None", filename_prefix if filename_prefix is not None else defaults.filename_prefix
        ),
        capture_svg=cast("bool", capture_svg if capture_svg is not None else defaults.capture_svg),
        infer_dimensions=cast("bool", infer_dimensions if infer_dimensions is not None else defaults.infer_dimensions),
    )


def _build_metadata_config(config: MetadataConfig | dict[str, object] | None) -> MetadataConfig:
    if config is None or isinstance(config, MetadataConfig):
        return config or MetadataConfig()

    extract_document = config.get("extract_document", config.get("extractDocument"))
    extract_headers = config.get("extract_headers", config.get("extractHeaders"))
    extract_links = config.get("extract_links", config.get("extractLinks"))
    extract_images = config.get("extract_images", config.get("extractImages"))
    extract_structured_data = config.get("extract_structured_data", config.get("extractStructuredData"))
    max_structured_data_size = config.get("max_structured_data_size", config.get("maxStructuredDataSize"))

    defaults = MetadataConfig()
    return MetadataConfig(
        extract_document=cast("bool", extract_document if extract_document is not None else defaults.extract_document),
        extract_headers=cast("bool", extract_headers if extract_headers is not None else defaults.extract_headers),
        extract_links=cast("bool", extract_links if extract_links is not None else defaults.extract_links),
        extract_images=cast("bool", extract_images if extract_images is not None else defaults.extract_images),
        extract_structured_data=cast(
            "bool",
            extract_structured_data if extract_structured_data is not None else defaults.extract_structured_data,
        ),
        max_structured_data_size=cast(
            "int",
            max_structured_data_size if max_structured_data_size is not None else defaults.max_structured_data_size,
        ),
    )


def convert(
    html: str,
    options: ConversionOptions | None = None,
    preprocessing: PreprocessingOptions | None = None,
) -> str:
    """Convert HTML to Markdown using the Rust backend."""
    rust_options = _rust_options(options, preprocessing)
    if rust_options is None:
        return _rust.convert(html, None)
    return _rust.convert(html, rust_options)


def convert_with_inline_images(
    html: str,
    options: ConversionOptions | None = None,
    preprocessing: PreprocessingOptions | None = None,
    image_config: InlineImageConfig | None = None,
) -> tuple[str, list[InlineImage], list[InlineImageWarning]]:
    """Convert HTML and extract inline images."""
    rust_options = _rust_options(options, preprocessing)
    image_config = _build_inline_image_config(image_config)
    markdown, images, warnings = _rust.convert_with_inline_images(html, rust_options, image_config)
    return markdown, list(images), list(warnings)


def convert_with_inline_images_handle(
    html: str,
    handle: OptionsHandle,
    image_config: InlineImageConfig | None = None,
) -> tuple[str, list[InlineImage], list[InlineImageWarning]]:
    """Convert HTML and extract inline images using a pre-built options handle."""
    if image_config is None:
        image_config = InlineImageConfig()

    markdown, images, warnings = _rust.convert_with_inline_images_handle(html, handle, image_config)
    return markdown, list(images), list(warnings)


def create_options_handle(
    options: ConversionOptions | None = None,
    preprocessing: PreprocessingOptions | None = None,
) -> OptionsHandle:
    """Create a reusable ConversionOptions handle backed by Rust."""
    if options is None:
        options = ConversionOptions()
    if preprocessing is None:
        preprocessing = PreprocessingOptions()
    rust_options = _rust_options(options, preprocessing)
    return _rust.create_options_handle(rust_options)


def start_profiling(output_path: str, frequency: int | None = None) -> None:
    """Start Rust-side profiling and write a flamegraph to output_path."""
    _rust.start_profiling(output_path, frequency)


def stop_profiling() -> None:
    """Stop Rust-side profiling and flush the flamegraph."""
    _rust.stop_profiling()


def convert_with_handle(html: str, handle: OptionsHandle) -> str:
    """Convert HTML using a pre-parsed ConversionOptions handle."""
    return _rust.convert_with_options_handle(html, handle)


def convert_with_metadata(
    html: str,
    options: ConversionOptions | None = None,
    preprocessing: PreprocessingOptions | None = None,
    metadata_config: MetadataConfig | None = None,
) -> tuple[str, ExtendedMetadata]:
    """Convert HTML and extract comprehensive metadata.

    Args:
        html: HTML string to convert
        options: Optional conversion configuration
        preprocessing: Optional preprocessing configuration
        metadata_config: Optional metadata extraction configuration

    Returns:
        Tuple of (markdown, metadata_dict) where metadata_dict contains:
        - document: Document-level metadata (title, description, lang, etc.)
        - headers: List of header elements with hierarchy
        - links: List of extracted hyperlinks with classification
        - images: List of extracted images with metadata
        - structured_data: List of JSON-LD, Microdata, or RDFa blocks
    """
    rust_options = _rust_options(options, preprocessing)
    metadata_config = _build_metadata_config(metadata_config)
    markdown, metadata = _rust.convert_with_metadata(html, rust_options, metadata_config)
    return markdown, metadata


def convert_with_metadata_handle(
    html: str,
    handle: OptionsHandle,
    metadata_config: MetadataConfig | None = None,
) -> tuple[str, ExtendedMetadata]:
    """Convert HTML and extract metadata using a pre-built options handle."""
    if metadata_config is None:
        metadata_config = MetadataConfig()

    markdown, metadata = _rust.convert_with_metadata_handle(html, handle, metadata_config)
    return markdown, metadata


def convert_with_visitor(
    html: str,
    options: ConversionOptions | None = None,
    preprocessing: PreprocessingOptions | None = None,
    visitor: object | None = None,
) -> str:
    """Convert HTML with a visitor pattern.

    This function enables custom processing of HTML elements during conversion
    using a visitor object. The visitor can inspect, modify, or skip elements
    during the conversion process.

    Args:
        html: HTML string to convert
        options: Optional conversion configuration
        preprocessing: Optional preprocessing configuration
        visitor: Optional visitor object with methods like visit_text, visit_link, etc.
                 Methods should return a result dict with 'type' key:
                 - {'type': 'continue'} - Use default conversion
                 - {'type': 'skip'} - Skip this element
                 - {'type': 'preserve_html'} - Preserve as raw HTML
                 - {'type': 'custom', 'output': 'markdown'} - Use custom output
                 - {'type': 'error', 'message': 'error'} - Stop with error

    Returns:
        Converted markdown string

    Example:
        >>> class MyVisitor:
        ...     def visit_heading(self, ctx, level, text, id):
        ...         return {"type": "custom", "output": f"HEADING[{level}]: {text}"}
        >>>
        >>> visitor = MyVisitor()
        >>> markdown = convert_with_visitor("<h1>Test</h1>", visitor=visitor)
    """
    if options is None:
        options = ConversionOptions()
    if preprocessing is None:
        preprocessing = PreprocessingOptions()

    if visitor is None:
        return convert(html, options, preprocessing)

    rust_options = _rust_options(options, preprocessing)
    return _rust.convert_with_visitor(html, rust_options, visitor)


def convert_with_async_visitor(
    html: str,
    options: ConversionOptions | None = None,
    preprocessing: PreprocessingOptions | None = None,
    visitor: object | None = None,
) -> str:
    """Convert HTML with an async visitor pattern.

    This function enables custom processing of HTML elements during conversion
    using a visitor object with async methods. The visitor can inspect, modify,
    or skip elements during the conversion process.

    Args:
        html: HTML string to convert
        options: Optional conversion configuration
        preprocessing: Optional preprocessing configuration
        visitor: Optional visitor object with async methods (on_element, on_text, etc.)
                 Methods should be coroutines that return a result dict with 'type' key

    Returns:
        Converted markdown string

    Example:
        >>> class MyVisitor:
        ...     async def on_element(self, context):
        ...         return {"type": "continue"}
        >>>
        >>> visitor = MyVisitor()
        >>> markdown = convert_with_async_visitor("<h1>Test</h1>", visitor=visitor)
    """
    if visitor is None:
        return convert(html, options, preprocessing)

    rust_options = _rust_options(options, preprocessing)
    return _rust.convert_with_async_visitor(html, rust_options, visitor)


__all__ = [
    "InlineImage",
    "InlineImageConfig",
    "InlineImageWarning",
    "MetadataConfig",
    "OptionsHandle",
    "convert",
    "convert_with_async_visitor",
    "convert_with_handle",
    "convert_with_inline_images",
    "convert_with_inline_images_handle",
    "convert_with_metadata",
    "convert_with_metadata_handle",
    "convert_with_visitor",
    "create_options_handle",
    "start_profiling",
    "stop_profiling",
]
