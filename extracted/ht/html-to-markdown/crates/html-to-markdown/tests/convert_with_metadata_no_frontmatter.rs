#![allow(missing_docs)]

//! Regression tests: `convert_with_metadata` must never prepend YAML frontmatter
//! to the markdown string. Metadata is returned as a struct, so embedding it
//! in the content is redundant and pollutes the output.

use html_to_markdown_rs::ConversionOptions;
use html_to_markdown_rs::metadata::MetadataConfig;

#[test]
fn convert_with_metadata_omits_yaml_frontmatter_default_options() {
    let html = r#"
        <html>
          <head>
            <title>My Page Title</title>
            <meta name="description" content="A page description">
            <meta name="author" content="Jane Doe">
          </head>
          <body><p>Hello world</p></body>
        </html>
    "#;

    let (markdown, metadata) = html_to_markdown_rs::convert_with_metadata(html, None, MetadataConfig::default(), None)
        .expect("convert_with_metadata failed");

    // Metadata struct should contain the extracted data
    assert!(
        metadata.document.title.is_some(),
        "metadata.document.title should be populated"
    );

    // Markdown output must NOT contain YAML frontmatter delimiters
    assert!(
        !markdown.contains("---"),
        "markdown should not contain YAML frontmatter delimiters, got:\n{markdown}"
    );
    assert!(
        !markdown.starts_with("---\n"),
        "markdown should not start with YAML frontmatter, got:\n{markdown}"
    );
}

#[test]
fn convert_with_metadata_omits_frontmatter_even_when_extract_metadata_is_true() {
    let html = r#"
        <html>
          <head>
            <title>Test Title</title>
            <meta name="description" content="Test description">
          </head>
          <body><p>Content here</p></body>
        </html>
    "#;

    // Explicitly pass extract_metadata: true — convert_with_metadata should override it
    let options = ConversionOptions {
        extract_metadata: true,
        ..Default::default()
    };

    let (markdown, metadata) =
        html_to_markdown_rs::convert_with_metadata(html, Some(options), MetadataConfig::default(), None)
            .expect("convert_with_metadata failed");

    assert!(
        metadata.document.title.is_some(),
        "metadata struct should still contain title"
    );
    assert!(
        !markdown.contains("---"),
        "YAML frontmatter must not appear even when extract_metadata was explicitly true, got:\n{markdown}"
    );
}

#[test]
fn convert_with_metadata_body_content_is_clean() {
    let html = r#"
        <html>
          <head>
            <title>Page</title>
            <meta name="keywords" content="rust, html, markdown">
          </head>
          <body><h1>Heading</h1><p>Paragraph text.</p></body>
        </html>
    "#;

    let (markdown, _metadata) = html_to_markdown_rs::convert_with_metadata(html, None, MetadataConfig::default(), None)
        .expect("convert_with_metadata failed");

    // The output should start with the body content, not frontmatter
    let trimmed = markdown.trim();
    assert!(
        trimmed.starts_with('#') || trimmed.starts_with("Heading"),
        "markdown should start with body content, got:\n{markdown}"
    );
    assert!(
        trimmed.contains("Paragraph text."),
        "markdown should contain paragraph text, got:\n{markdown}"
    );
}
