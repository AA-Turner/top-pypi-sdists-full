//! Parsed JSON Schema with centralized navigation helpers and a generic
//! object-tree walker.  Created once in `main` and shared across every
//! generator so the schema is parsed and `definitions` are resolved in
//! exactly one place.

const DEFINITION_REF_PREFIX: &str = "#/definitions/";

pub type JsonObject = serde_json::Map<String, serde_json::Value>;

pub struct SchemaDoc {
    pub root: serde_json::Value,
}

impl SchemaDoc {
    pub fn from_str(text: &str) -> Self {
        let root: serde_json::Value =
            serde_json::from_str(text).expect("Failed to parse schema JSON");
        SchemaDoc { root }
    }

    pub fn definitions(&self) -> Option<&JsonObject> {
        self.root.get("definitions").and_then(|d| d.as_object())
    }

    /// Resolve a `$ref` node to its target definition.
    /// Non-ref nodes pass through unchanged.
    /// Panics on malformed or unresolvable refs — those are schema-authoring
    /// errors that should fail the build loudly.
    pub fn resolve<'a>(&'a self, node: &'a serde_json::Value) -> &'a serde_json::Value {
        let Some(ref_path) = node.get("$ref").and_then(|r| r.as_str()) else {
            return node;
        };
        let def_name = ref_path
            .strip_prefix(DEFINITION_REF_PREFIX)
            .unwrap_or_else(|| panic!("Unsupported $ref format: {ref_path}"));
        self.definitions()
            .and_then(|d| d.get(def_name))
            .unwrap_or_else(|| panic!("Unresolved $ref: {ref_path}"))
    }

    /// Sorted property entries of a JSON Schema object node.
    /// Returns an empty vec for non-objects or objects without a `properties` key.
    pub fn sorted_properties<'a>(
        &'a self,
        node: &'a serde_json::Value,
    ) -> Vec<(&'a str, &'a serde_json::Value)> {
        let Some(properties) = node.get("properties").and_then(|p| p.as_object()) else {
            return Vec::new();
        };
        let mut entries: Vec<(&str, &serde_json::Value)> =
            properties.iter().map(|(k, v)| (k.as_str(), v)).collect();
        entries.sort_by_key(|(k, _)| *k);
        entries
    }

    /// Schema `type` keyword, defaulting to `"object"` when absent.
    pub fn node_type<'a>(&self, node: &'a serde_json::Value) -> &'a str {
        node.get("type")
            .and_then(|t| t.as_str())
            .unwrap_or("object")
    }

    pub fn root_properties(&self) -> Vec<(&str, &serde_json::Value)> {
        self.sorted_properties(&self.root)
    }
}

/// Recursively visit every property of every reachable object node in the
/// schema, resolving `$ref` along the way.  Arrays and scalars are
/// intentionally skipped — the generated path constants are consumed by
/// object-only JSON navigation helpers that do not model array indices.
///
/// The `visit` callback receives the full segment path and the *resolved*
/// property value for every property of every reachable object.
pub fn walk_object_tree(
    doc: &SchemaDoc,
    current_path: &[String],
    node: &serde_json::Value,
    visit: &mut impl FnMut(&[String], &serde_json::Value),
) {
    let node = doc.resolve(node);
    if doc.node_type(node) != "object" {
        return;
    }

    for (name, raw_child) in doc.sorted_properties(node) {
        let child = doc.resolve(raw_child);
        let mut child_path = current_path.to_vec();
        child_path.push(name.to_string());
        visit(&child_path, child);
        walk_object_tree(doc, &child_path, child, visit);
    }
}
