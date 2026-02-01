//! Regression coverage for issue #200.

use html_to_markdown_rs::convert;

#[test]
fn test_definition_list_spacing_consistency() {
    let html1 = r#"
<div>
 <dl>
  <dt>Tags:</dt>
  <dd>
   <ul>
    <li>
     <a href="https://site.com">php</a>
    </li>
    <li>
     <a href="https://site.com/search/">closure</a>
    </li>
   </ul>
   <button type="button">Add tags</button>
  </dd>
 </dl>
</div>
"#;

    let html2 = r#"<div><dl><dt>Tags:</dt><dd><ul><li><a href="https://site.com">php</a></li><li><a href="https://site.com/search/">closure</a></li></ul><button type="button">Add tags</button></dd></dl></div>"#;

    let markdown1 = convert(html1, None).expect("conversion should succeed");
    let markdown2 = convert(html2, None).expect("conversion should succeed");

    assert_eq!(markdown1, markdown2);
    assert!(markdown1.contains("Tags:"));
    assert!(markdown1.contains("\n:   - [php]"));
    assert!(markdown1.contains("\n    - [closure]"));
    assert!(markdown1.contains("\n    Add tags"));
}
