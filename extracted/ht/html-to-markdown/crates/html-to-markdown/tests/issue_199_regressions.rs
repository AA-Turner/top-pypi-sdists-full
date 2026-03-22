//! Regression coverage for issue #199.

use html_to_markdown_rs::convert;

#[test]
fn test_link_label_is_not_truncated() {
    let label = "a".repeat(600);
    let html = format!(r#"<a href="https://example.com">{label}</a>"#);

    let markdown = convert(&html, None).expect("conversion should succeed");
    let expected = format!("[{label}](https://example.com)");

    assert!(markdown.contains(&expected));
    assert!(!markdown.contains('…'));
}
