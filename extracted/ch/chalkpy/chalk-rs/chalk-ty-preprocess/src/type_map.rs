use std::collections::HashMap;

use anyhow::{Context, Result};
use chalk_proto::chalk::graph::v1::{feature_type, Graph};
use prost::Message;

use crate::arrow_to_python::arrow_type_to_python;

/// A key for looking up a feature's Python type: (ClassName, attribute_name).
/// ClassName is the Python class name (e.g. "User"), attribute_name is the
/// field name as written in code (e.g. "id", "name").
pub type FeatureKey = (String, String);

/// Information about a feature's type.
#[derive(Debug, Clone)]
pub struct FeatureTypeInfo {
    /// The Python type annotation string (e.g. "int", "str", "float").
    pub python_type: String,
    /// Whether the feature is nullable (wraps in `| None`).
    pub is_nullable: bool,
}

impl FeatureTypeInfo {
    /// Return the full annotation string, including `| None` if nullable.
    pub fn annotation(&self) -> String {
        if self.is_nullable {
            format!("{} | None", self.python_type)
        } else {
            self.python_type.clone()
        }
    }
}

/// Maps (ClassName, attribute_name) -> FeatureTypeInfo.
/// Also tracks namespace -> class_name mapping for has-one/has-many.
#[derive(Debug)]
pub struct TypeMap {
    /// (class_name, attribute_name) -> type info
    pub features: HashMap<FeatureKey, FeatureTypeInfo>,
    /// namespace (snake_case) -> class_name (PascalCase)
    pub namespace_to_class: HashMap<String, String>,
    /// class_name -> set of (attribute_name, type_annotation) for generating stubs
    pub class_fields: HashMap<String, Vec<(String, String)>>,
}

/// Load an Export protobuf from bytes and extract the Graph.
pub fn load_graph_from_export_bytes(bytes: &[u8]) -> Result<Graph> {
    let export = chalk_proto::chalk::artifacts::v1::Export::decode(bytes)
        .context("failed to decode Export protobuf")?;
    export.graph.context("Export has no graph field")
}

/// Load a Graph protobuf directly from bytes.
pub fn load_graph_from_bytes(bytes: &[u8]) -> Result<Graph> {
    Graph::decode(bytes).context("failed to decode Graph protobuf")
}

/// Load a TypeMap directly from Go-style proto JSON (as produced by `chalk graph`).
/// This handles the non-standard JSON format where oneof fields use PascalCase
/// wrapper keys (e.g., `"Type": {"Scalar": {...}}` and `"ArrowTypeEnum": {"LargeUtf8": {}}`).
pub fn load_type_map_from_json(json_bytes: &[u8]) -> Result<TypeMap> {
    let text = std::str::from_utf8(json_bytes).context("invalid UTF-8 in JSON file")?;

    // Skip any header lines before the JSON object.
    let json_start = text.find('{').context("no JSON object found in file")?;
    let json_text = &text[json_start..];

    let root: serde_json::Value =
        serde_json::from_str(json_text).context("failed to parse JSON")?;

    // The root might be {"graph": {...}} or just the graph directly.
    let graph = root.get("graph").unwrap_or(&root);

    let feature_sets = graph
        .get("feature_sets")
        .and_then(|v| v.as_array())
        .context("no feature_sets in graph JSON")?;

    let mut features = HashMap::new();
    let mut namespace_to_class = HashMap::new();
    let mut class_fields: HashMap<String, Vec<(String, String)>> = HashMap::new();

    for fs in feature_sets {
        let namespace = fs.get("name").and_then(|v| v.as_str()).unwrap_or("");
        let class_name = snake_to_pascal(namespace);
        namespace_to_class.insert(namespace.to_string(), class_name.clone());

        let fs_features = fs.get("features").and_then(|v| v.as_array());
        let Some(fs_features) = fs_features else {
            continue;
        };

        for feature in fs_features {
            // Go-style JSON wraps oneof in {"Type": {"Scalar": {...}}}
            let type_obj = feature.get("Type").or_else(|| feature.get("type"));
            let Some(type_obj) = type_obj else { continue };

            if let Some(scalar) = type_obj.get("Scalar").or_else(|| type_obj.get("scalar")) {
                let name = scalar.get("name").and_then(|v| v.as_str()).unwrap_or("");
                let attr_name = scalar
                    .get("attribute_name")
                    .and_then(|v| v.as_str())
                    .filter(|s| !s.is_empty())
                    .unwrap_or(name);
                let is_nullable = scalar
                    .get("is_nullable")
                    .and_then(|v| v.as_bool())
                    .unwrap_or(false);
                let python_type = extract_arrow_type_from_json(scalar.get("arrow_type"));
                let info = FeatureTypeInfo {
                    python_type: python_type.clone(),
                    is_nullable,
                };
                features.insert((class_name.clone(), attr_name.to_string()), info);
                class_fields
                    .entry(class_name.clone())
                    .or_default()
                    .push((attr_name.to_string(), python_type));
            } else if let Some(has_one) = type_obj.get("HasOne").or_else(|| type_obj.get("hasOne"))
            {
                let name = has_one.get("name").and_then(|v| v.as_str()).unwrap_or("");
                let foreign_ns = has_one
                    .get("foreign_namespace")
                    .or_else(|| has_one.get("foreignNamespace"))
                    .and_then(|v| v.as_str())
                    .unwrap_or("");
                let foreign_class = snake_to_pascal(foreign_ns);
                let is_nullable = has_one
                    .get("is_nullable")
                    .or_else(|| has_one.get("isNullable"))
                    .and_then(|v| v.as_bool())
                    .unwrap_or(false);
                let info = FeatureTypeInfo {
                    python_type: foreign_class.clone(),
                    is_nullable,
                };
                features.insert((class_name.clone(), name.to_string()), info);
                let display_type = if is_nullable {
                    format!("{foreign_class} | None")
                } else {
                    foreign_class
                };
                class_fields
                    .entry(class_name.clone())
                    .or_default()
                    .push((name.to_string(), display_type));
            } else if let Some(has_many) =
                type_obj.get("HasMany").or_else(|| type_obj.get("hasMany"))
            {
                let name = has_many.get("name").and_then(|v| v.as_str()).unwrap_or("");
                let foreign_ns = has_many
                    .get("foreign_namespace")
                    .or_else(|| has_many.get("foreignNamespace"))
                    .and_then(|v| v.as_str())
                    .unwrap_or("");
                let foreign_class = snake_to_pascal(foreign_ns);
                let python_type = format!("DataFrame[{foreign_class}]");
                let info = FeatureTypeInfo {
                    python_type,
                    is_nullable: false,
                };
                features.insert((class_name.clone(), name.to_string()), info);
                class_fields
                    .entry(class_name.clone())
                    .or_default()
                    .push((name.to_string(), format!("DataFrame[{foreign_class}]")));
            }
            // Skip FeatureTime, Windowed, GroupBy — same as protobuf path.
        }
    }

    Ok(TypeMap {
        features,
        namespace_to_class,
        class_fields,
    })
}

/// Extract Python type from a Go-style JSON ArrowType.
fn extract_arrow_type_from_json(arrow_type: Option<&serde_json::Value>) -> String {
    let Some(at) = arrow_type else {
        return "Any".to_string();
    };
    // Go JSON: {"ArrowTypeEnum": {"LargeUtf8": {}}}
    let type_enum = at
        .get("ArrowTypeEnum")
        .or_else(|| at.get("arrow_type_enum"));
    let Some(type_enum) = type_enum else {
        return "Any".to_string();
    };

    if type_enum
        .get("LargeUtf8")
        .or_else(|| type_enum.get("large_utf8"))
        .is_some()
    {
        return "str".to_string();
    }
    if type_enum
        .get("Utf8")
        .or_else(|| type_enum.get("utf8"))
        .is_some()
    {
        return "str".to_string();
    }
    if type_enum
        .get("Int64")
        .or_else(|| type_enum.get("int64"))
        .is_some()
    {
        return "int".to_string();
    }
    if type_enum
        .get("Int32")
        .or_else(|| type_enum.get("int32"))
        .is_some()
    {
        return "int".to_string();
    }
    if type_enum
        .get("Int16")
        .or_else(|| type_enum.get("int16"))
        .is_some()
    {
        return "int".to_string();
    }
    if type_enum
        .get("Int8")
        .or_else(|| type_enum.get("int8"))
        .is_some()
    {
        return "int".to_string();
    }
    if type_enum
        .get("Uint64")
        .or_else(|| type_enum.get("uint64"))
        .is_some()
    {
        return "int".to_string();
    }
    if type_enum
        .get("Uint32")
        .or_else(|| type_enum.get("uint32"))
        .is_some()
    {
        return "int".to_string();
    }
    if type_enum
        .get("Float64")
        .or_else(|| type_enum.get("float64"))
        .is_some()
    {
        return "float".to_string();
    }
    if type_enum
        .get("Float32")
        .or_else(|| type_enum.get("float32"))
        .is_some()
    {
        return "float".to_string();
    }
    if type_enum
        .get("Bool")
        .or_else(|| type_enum.get("bool"))
        .is_some()
    {
        return "bool".to_string();
    }
    if type_enum
        .get("Timestamp")
        .or_else(|| type_enum.get("timestamp"))
        .is_some()
    {
        return "datetime.datetime".to_string();
    }
    if type_enum
        .get("Date64")
        .or_else(|| type_enum.get("date64"))
        .is_some()
    {
        return "datetime.date".to_string();
    }
    if type_enum
        .get("Date32")
        .or_else(|| type_enum.get("date32"))
        .is_some()
    {
        return "datetime.date".to_string();
    }
    if type_enum
        .get("Duration")
        .or_else(|| type_enum.get("duration"))
        .is_some()
    {
        return "datetime.timedelta".to_string();
    }
    if type_enum
        .get("Binary")
        .or_else(|| type_enum.get("binary"))
        .is_some()
        || type_enum
            .get("LargeBinary")
            .or_else(|| type_enum.get("large_binary"))
            .is_some()
    {
        return "bytes".to_string();
    }
    if type_enum
        .get("Decimal128")
        .or_else(|| type_enum.get("decimal_128"))
        .is_some()
        || type_enum
            .get("Decimal256")
            .or_else(|| type_enum.get("decimal_256"))
            .is_some()
    {
        return "decimal.Decimal".to_string();
    }
    // Lists, structs, maps — use Any for simplicity.
    "Any".to_string()
}

/// Build a TypeMap from a protograph Graph.
pub fn build_type_map(graph: &Graph) -> TypeMap {
    let mut features = HashMap::new();
    let mut namespace_to_class = HashMap::new();
    let mut class_fields: HashMap<String, Vec<(String, String)>> = HashMap::new();

    for feature_set in &graph.feature_sets {
        let namespace = &feature_set.name;
        // Derive class name from namespace: snake_case -> PascalCase
        let class_name = snake_to_pascal(namespace);
        namespace_to_class.insert(namespace.clone(), class_name.clone());

        for feature_type in &feature_set.features {
            let Some(ref ft) = feature_type.r#type else {
                continue;
            };
            match ft {
                feature_type::Type::Scalar(scalar) => {
                    let attr_name = if scalar.attribute_name.is_empty() {
                        &scalar.name
                    } else {
                        &scalar.attribute_name
                    };
                    let python_type = scalar
                        .arrow_type
                        .as_ref()
                        .map(arrow_type_to_python)
                        .unwrap_or_else(|| "Any".to_string());

                    let info = FeatureTypeInfo {
                        python_type: python_type.clone(),
                        is_nullable: scalar.is_nullable,
                    };
                    features.insert((class_name.clone(), attr_name.to_string()), info);
                    class_fields
                        .entry(class_name.clone())
                        .or_default()
                        .push((attr_name.to_string(), python_type));
                }
                feature_type::Type::HasOne(has_one) => {
                    let attr_name = &has_one.name;
                    let foreign_class = snake_to_pascal(&has_one.foreign_namespace);
                    let python_type = if has_one.is_nullable {
                        format!("{foreign_class} | None")
                    } else {
                        foreign_class.clone()
                    };
                    let info = FeatureTypeInfo {
                        python_type: foreign_class,
                        is_nullable: has_one.is_nullable,
                    };
                    features.insert((class_name.clone(), attr_name.to_string()), info);
                    class_fields
                        .entry(class_name.clone())
                        .or_default()
                        .push((attr_name.to_string(), python_type));
                }
                feature_type::Type::HasMany(has_many) => {
                    let attr_name = &has_many.name;
                    let foreign_class = snake_to_pascal(&has_many.foreign_namespace);
                    let python_type = format!("DataFrame[{foreign_class}]");
                    let info = FeatureTypeInfo {
                        python_type,
                        is_nullable: false,
                    };
                    features.insert((class_name.clone(), attr_name.to_string()), info);
                    class_fields
                        .entry(class_name.clone())
                        .or_default()
                        .push((attr_name.to_string(), format!("DataFrame[{foreign_class}]")));
                }
                feature_type::Type::FeatureTime(_) => {
                    let info = FeatureTypeInfo {
                        python_type: "datetime.datetime".to_string(),
                        is_nullable: false,
                    };
                    features.insert((class_name.clone(), "__chalk_ts__".to_string()), info);
                }
                feature_type::Type::Windowed(_) | feature_type::Type::GroupBy(_) => {
                    // Windowed/GroupBy features are complex — skip for now
                }
            }
        }
    }

    TypeMap {
        features,
        namespace_to_class,
        class_fields,
    }
}

/// Convert a snake_case string to PascalCase.
fn snake_to_pascal(s: &str) -> String {
    s.split('_')
        .map(|part| {
            let mut chars = part.chars();
            match chars.next() {
                Some(c) => {
                    let mut s = c.to_uppercase().to_string();
                    s.extend(chars);
                    s
                }
                None => String::new(),
            }
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snake_to_pascal() {
        assert_eq!(snake_to_pascal("user"), "User");
        assert_eq!(snake_to_pascal("user_account"), "UserAccount");
        assert_eq!(snake_to_pascal("transaction"), "Transaction");
    }
}
