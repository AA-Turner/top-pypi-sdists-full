//! Tests for plain text output format support.

use html_to_markdown_rs::{ConversionOptions, OutputFormat, convert};

fn plain_options() -> ConversionOptions {
    ConversionOptions {
        output_format: OutputFormat::Plain,
        ..Default::default()
    }
}

#[test]
fn test_plain_basic_paragraph() {
    let html = "<p>Hello world</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "Hello world\n");
}

#[test]
fn test_plain_no_strong_markers() {
    let html = "<p>This is <strong>bold</strong> text</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "This is bold text\n");
}

#[test]
fn test_plain_no_emphasis_markers() {
    let html = "<p>This is <em>italic</em> text</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "This is italic text\n");
}

#[test]
fn test_plain_link_text_only() {
    let html = r#"<p>Visit <a href="https://example.com">our site</a> today</p>"#;
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "Visit our site today\n");
}

#[test]
fn test_plain_image_alt_text() {
    let html = r#"<img alt="A cute cat">"#;
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "A cute cat\n");
}

#[test]
fn test_plain_image_skipped_when_option_set() {
    let html = r#"<img alt="A cute cat">"#;
    let mut opts = plain_options();
    opts.skip_images = true;
    let result = convert(html, Some(opts)).unwrap();
    assert_eq!(result, "");
}

#[test]
fn test_plain_code_block() {
    let html = "<pre><code>fn main() {}</code></pre>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "fn main() {}\n");
}

#[test]
fn test_plain_blockquote_no_prefix() {
    let html = "<blockquote><p>Quoted text</p></blockquote>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        !result.contains('>'),
        "Plain text should not contain blockquote prefix, got: {result}"
    );
    assert!(result.contains("Quoted text"));
}

#[test]
fn test_plain_list_items_on_separate_lines() {
    let html = "<ul><li>First</li><li>Second</li><li>Third</li></ul>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(result.contains("First"));
    assert!(result.contains("Second"));
    assert!(result.contains("Third"));
    // Items should be on separate lines
    let lines: Vec<&str> = result.lines().filter(|l| !l.is_empty()).collect();
    assert!(lines.len() >= 3, "Expected at least 3 lines, got: {result}");
}

#[test]
fn test_plain_table_cells_extracted() {
    let html = "<table><tr><td>A</td><td>B</td></tr><tr><td>C</td><td>D</td></tr></table>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(result.contains('A'));
    assert!(result.contains('B'));
    assert!(result.contains('C'));
    assert!(result.contains('D'));
}

#[test]
fn test_plain_no_escaping() {
    let html = "<p>* not a list</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        result.contains("* not a list"),
        "Plain text should not escape asterisks, got: {result}"
    );
    assert!(
        !result.contains("\\*"),
        "Plain text should not backslash-escape, got: {result}"
    );
}

#[test]
fn test_plain_script_excluded() {
    let html = "<p>Before</p><script>alert('xss')</script><p>After</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        !result.contains("alert"),
        "Script content should be excluded, got: {result}"
    );
    assert!(result.contains("Before"));
    assert!(result.contains("After"));
}

#[test]
fn test_plain_style_excluded() {
    let html = "<p>Hello</p><style>.foo { color: red; }</style>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        !result.contains("color"),
        "Style content should be excluded, got: {result}"
    );
    assert!(result.contains("Hello"));
}

#[test]
fn test_plain_br_becomes_newline() {
    let html = "<p>Line one<br>Line two</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        result.contains("Line one\nLine two"),
        "Expected newline from <br>, got: {result}"
    );
}

#[test]
fn test_plain_hr_becomes_blank_line() {
    let html = "<p>Above</p><hr><p>Below</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(result.contains("Above"));
    assert!(result.contains("Below"));
    // Should have blank line between
    assert!(result.contains("\n\n"), "Expected blank line from <hr>, got: {result}");
}

#[test]
fn test_plain_nested_inline_formatting_stripped() {
    let html = "<p>Start <strong>bold <em>and italic</em></strong> end</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "Start bold and italic end\n");
}

#[test]
fn test_plain_heading_no_markers() {
    let html = "<h1>Title</h1><p>Content</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        !result.contains('#'),
        "Plain text should not contain heading markers, got: {result}"
    );
    assert!(result.contains("Title"));
    assert!(result.contains("Content"));
}

#[test]
fn test_plain_parse_variants() {
    assert_eq!(OutputFormat::parse("plain"), OutputFormat::Plain);
    assert_eq!(OutputFormat::parse("plaintext"), OutputFormat::Plain);
    assert_eq!(OutputFormat::parse("text"), OutputFormat::Plain);
    assert_eq!(OutputFormat::parse("Plain"), OutputFormat::Plain);
    assert_eq!(OutputFormat::parse("PLAINTEXT"), OutputFormat::Plain);
}

#[test]
fn test_plain_empty_input() {
    let html = "";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "");
}

#[test]
fn test_plain_whitespace_only_html() {
    let html = "<p>   </p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert_eq!(result, "");
}

#[test]
fn test_plain_inline_code_no_backticks() {
    let html = "<p>Use <code>fmt.Println</code> to print</p>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        !result.contains('`'),
        "Plain text should not contain backticks, got: {result}"
    );
    assert!(result.contains("fmt.Println"));
}

#[test]
fn test_plain_pre_preserves_whitespace() {
    let html = "<pre>  indented\n    more</pre>";
    let result = convert(html, Some(plain_options())).unwrap();
    assert!(
        result.contains("  indented\n    more"),
        "Pre blocks should preserve whitespace, got: {result}"
    );
}
