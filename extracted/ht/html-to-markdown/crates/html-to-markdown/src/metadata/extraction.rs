//! Metadata extraction utilities and helpers.

use super::types::{DocumentMetadata, StructuredData, StructuredDataType, TextDirection};
use std::collections::BTreeMap;

/// Extract document metadata from collected head metadata.
///
/// Parses head metadata into structured document metadata,
/// handling special cases like Open Graph, Twitter Card, keywords, etc.
pub(crate) fn extract_document_metadata(
    head_metadata: BTreeMap<String, String>,
    lang: Option<String>,
    dir: Option<String>,
) -> DocumentMetadata {
    let mut doc = DocumentMetadata::default();

    for (raw_key, value) in head_metadata {
        let mut key = raw_key.as_str();
        let mut replaced_key: Option<String> = None;

        if let Some(stripped) = key.strip_prefix("meta-") {
            key = stripped;
        }

        if key.as_bytes().contains(&b':') {
            replaced_key = Some(key.replace(':', "-"));
            key = replaced_key.as_deref().unwrap_or(key);
        }

        match key {
            "title" => doc.title = Some(value),
            "description" => doc.description = Some(value),
            "author" => doc.author = Some(value),
            "canonical" => doc.canonical_url = Some(value),
            "base" | "base-href" => doc.base_href = Some(value),
            key if key.starts_with("og-") => {
                let og_key = if key.as_bytes().contains(&b'-') {
                    key.trim_start_matches("og-").replace('-', "_")
                } else {
                    key.trim_start_matches("og-").to_string()
                };
                doc.open_graph.insert(og_key, value);
            }
            key if key.starts_with("twitter-") => {
                let tw_key = if key.as_bytes().contains(&b'-') {
                    key.trim_start_matches("twitter-").replace('-', "_")
                } else {
                    key.trim_start_matches("twitter-").to_string()
                };
                doc.twitter_card.insert(tw_key, value);
            }
            "keywords" => {
                doc.keywords = value
                    .split(',')
                    .map(|s| s.trim().to_string())
                    .filter(|s| !s.is_empty())
                    .collect();
            }
            _ => {
                let meta_key = if key.as_ptr() == raw_key.as_ptr() && key.len() == raw_key.len() {
                    raw_key
                } else if let Some(replaced) = replaced_key {
                    replaced
                } else {
                    key.to_string()
                };
                doc.meta_tags.insert(meta_key, value);
            }
        }
    }

    if let Some(lang) = lang {
        doc.language = Some(lang);
    }

    if let Some(dir) = dir {
        if let Some(parsed_dir) = TextDirection::parse(&dir) {
            doc.text_direction = Some(parsed_dir);
        }
    }

    doc
}

/// Extract structured data blocks into `StructuredData` items.
pub(crate) fn extract_structured_data(json_ld: Vec<String>) -> Vec<StructuredData> {
    let mut result = Vec::with_capacity(json_ld.len());

    for json_str in json_ld {
        let schema_type = scan_schema_type(&json_str)
            .or_else(|| {
                if json_str.contains("\"@type\"") {
                    serde_json::from_str::<serde_json::Value>(&json_str).ok().and_then(|v| {
                        v.get("@type")
                            .and_then(|t| t.as_str().map(std::string::ToString::to_string))
                    })
                } else {
                    None
                }
            })
            .or_else(|| {
                if !json_str.contains("\"@graph\"") {
                    return None;
                }

                let value = serde_json::from_str::<serde_json::Value>(&json_str).ok()?;
                let graph = value.get("@graph")?;
                let items = graph.as_array()?;
                items.iter().find_map(|item| {
                    item.get("@type")
                        .and_then(|t| t.as_str().map(std::string::ToString::to_string))
                })
            });

        result.push(StructuredData {
            data_type: StructuredDataType::JsonLd,
            raw_json: json_str,
            schema_type,
        });
    }

    result
}

/// Scan for @type in JSON string without full parsing.
fn scan_schema_type(json_str: &str) -> Option<String> {
    let needle = "\"@type\"";
    let start = json_str.find(needle)? + needle.len();
    let bytes = json_str.as_bytes();
    let mut i = start;

    while i < bytes.len() && bytes[i].is_ascii_whitespace() {
        i += 1;
    }
    if i >= bytes.len() || bytes[i] != b':' {
        return None;
    }
    i += 1;
    while i < bytes.len() && bytes[i].is_ascii_whitespace() {
        i += 1;
    }
    if i >= bytes.len() {
        return None;
    }

    if bytes[i] == b'[' {
        i += 1;
        while i < bytes.len() && bytes[i].is_ascii_whitespace() {
            i += 1;
        }
        if i >= bytes.len() || bytes[i] != b'"' {
            return None;
        }
    } else if bytes[i] != b'"' {
        return None;
    }

    let start_quote = i;
    i += 1;
    let mut escaped = false;
    while i < bytes.len() {
        let byte = bytes[i];
        if escaped {
            escaped = false;
            i += 1;
            continue;
        }
        if byte == b'\\' {
            escaped = true;
            i += 1;
            continue;
        }
        if byte == b'"' {
            let end_quote = i;
            let slice = &json_str[start_quote..=end_quote];
            return serde_json::from_str::<String>(slice).ok();
        }
        i += 1;
    }

    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_extract_document_metadata() {
        let mut head_metadata = BTreeMap::new();
        head_metadata.insert("title".to_string(), "Test Title".to_string());
        head_metadata.insert("description".to_string(), "Test Description".to_string());
        head_metadata.insert("keywords".to_string(), "rust, testing".to_string());

        let doc = extract_document_metadata(head_metadata, Some("en".to_string()), Some("ltr".to_string()));

        assert_eq!(doc.title, Some("Test Title".to_string()));
        assert_eq!(doc.description, Some("Test Description".to_string()));
        assert_eq!(doc.keywords, vec!["rust", "testing"]);
        assert_eq!(doc.language, Some("en".to_string()));
    }

    #[test]
    fn test_extract_document_metadata_with_og() {
        let mut head_metadata = BTreeMap::new();
        head_metadata.insert("og-title".to_string(), "OG Title".to_string());
        head_metadata.insert("og-description".to_string(), "OG Description".to_string());

        let doc = extract_document_metadata(head_metadata, None, None);

        assert_eq!(doc.open_graph.get("title"), Some(&"OG Title".to_string()));
        assert_eq!(doc.open_graph.get("description"), Some(&"OG Description".to_string()));
    }

    #[test]
    fn test_scan_schema_type() {
        let json = r#"{"@type":"Article","title":"Test"}"#;
        assert_eq!(scan_schema_type(json), Some("Article".to_string()));

        let json_array = r#"{"@type":["Article","NewsArticle"]}"#;
        assert_eq!(scan_schema_type(json_array), Some("Article".to_string()));

        let no_type = r#"{"title":"Test"}"#;
        assert_eq!(scan_schema_type(no_type), None);
    }
}
