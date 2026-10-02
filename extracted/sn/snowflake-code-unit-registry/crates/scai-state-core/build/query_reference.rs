//! Generates the human-readable query reference table embedded in
//! `src/generated/query_reference.rs`.  Has its own recursive traversal
//! (rather than using `walk_object_tree`) because it handles arrays,
//! enums, and `x-query-help` exclusion — none of which apply to the
//! path-oriented generators that share `walk_object_tree`.

use crate::schema::SchemaDoc;

/// A flattened field descriptor extracted from the JSON Schema.
struct FieldInfo {
    path: String,
    type_name: String,
    enum_values: Option<String>,
    description: String,
}

/// Walk the JSON Schema and produce a Rust source file containing
/// `pub const QUERY_REFERENCE: &str` with the full flattened field reference.
pub fn generate_query_reference(doc: &SchemaDoc, template: &str, rs_template: &str) -> String {
    let mut fields = Vec::new();
    for (name, prop) in doc.root_properties() {
        collect_fields(&mut fields, name, prop, doc);
    }

    let fields_table = format_fields_table(&fields);
    let reference = template.replace("{fields_table}", &fields_table);
    let ref_literal = format!("r#\"{}\"#", reference);
    rs_template.replace("{ref_literal}", &ref_literal)
}

/// Returns true if the property is explicitly excluded from the query reference
/// via `"x-query-help": false`.
fn is_excluded(prop: &serde_json::Value) -> bool {
    prop.get("x-query-help")
        .and_then(|v| v.as_bool())
        .is_some_and(|v| !v)
}

/// Recursively walk the schema, collecting leaf and container field descriptors.
fn collect_fields(
    fields: &mut Vec<FieldInfo>,
    prefix: &str,
    prop: &serde_json::Value,
    doc: &SchemaDoc,
) {
    if is_excluded(prop) {
        return;
    }

    let prop = doc.resolve(prop);

    let type_str = doc.node_type(prop);
    let description = prop
        .get("description")
        .and_then(|d| d.as_str())
        .unwrap_or("")
        .to_string();

    match type_str {
        "object" => {
            fields.push(FieldInfo {
                path: prefix.to_string(),
                type_name: "object".to_string(),
                enum_values: None,
                description,
            });
            for (name, sub_prop) in doc.sorted_properties(prop) {
                let child_path = format!("{}.{}", prefix, name);
                collect_fields(fields, &child_path, sub_prop, doc);
            }
        }
        "array" => {
            let item_desc = prop
                .get("items")
                .map(|i| describe_array_items(i, doc))
                .unwrap_or_default();
            let full_desc = if description.is_empty() {
                item_desc
            } else if item_desc.is_empty() {
                description
            } else {
                format!("{}; items: {}", description, item_desc)
            };
            fields.push(FieldInfo {
                path: prefix.to_string(),
                type_name: "array".to_string(),
                enum_values: None,
                description: full_desc,
            });
        }
        _ => {
            let enum_values = prop.get("enum").and_then(|e| {
                e.as_array().map(|arr| {
                    arr.iter()
                        .filter_map(|v| v.as_str().map(String::from))
                        .collect::<Vec<_>>()
                        .join(", ")
                })
            });
            let display_type = if enum_values.is_some() {
                "enum".to_string()
            } else {
                type_str.to_string()
            };
            fields.push(FieldInfo {
                path: prefix.to_string(),
                type_name: display_type,
                enum_values,
                description,
            });
        }
    }
}

/// Produce a short description of array item shapes (for display only).
fn describe_array_items(items: &serde_json::Value, doc: &SchemaDoc) -> String {
    let resolved = doc.resolve(items);

    match resolved.get("type").and_then(|t| t.as_str()) {
        Some("string") => "string".to_string(),
        Some("object") => {
            let props = doc.sorted_properties(resolved);
            if props.is_empty() {
                "object".to_string()
            } else {
                let keys: Vec<&str> = props.iter().map(|(k, _)| *k).collect();
                format!("{{{}}}", keys.join(", "))
            }
        }
        Some(t) => t.to_string(),
        None => String::new(),
    }
}

/// Format the collected fields into an aligned table string.
fn format_fields_table(fields: &[FieldInfo]) -> String {
    let path_width = fields
        .iter()
        .map(|f| f.path.len())
        .max()
        .unwrap_or(20)
        .max(20);
    let type_width = 10;

    let mut out = String::new();
    out.push_str(&format!(
        "  {:<path_width$}  {:<type_width$}  {}\n",
        "Field", "Type", "Allowed Values / Description",
    ));
    out.push_str(&format!("  {}\n", "─".repeat(path_width + type_width + 40)));

    for f in fields {
        let detail = match (&f.enum_values, f.description.is_empty()) {
            (Some(vals), true) => vals.clone(),
            (Some(vals), false) => format!("{} ({})", vals, f.description),
            (None, false) => f.description.clone(),
            (None, true) => String::new(),
        };
        out.push_str(&format!(
            "  {:<path_width$}  {:<type_width$}  {}\n",
            f.path, f.type_name, detail,
        ));
    }

    out
}
