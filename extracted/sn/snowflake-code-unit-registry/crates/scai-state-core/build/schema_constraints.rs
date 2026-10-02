//! Extracts schema-derived structural constraints into
//! `src/generated/schema_constraints.rs`.  Three tables are emitted, all
//! consumed by the runtime `validate_kind_rules` pipeline:
//!
//! - `ALLOWED_WHEN_CONSTRAINTS` — every `x-allowed-when` annotation, with
//!   the gated leaf addressed as `(parent_pointer, leaf_name)` so the
//!   validator can fan out across array items in `parent_pointer` before
//!   checking the leaf and resolving each gate lexically from the parent
//!   upward.
//! - `REQUIRED_WHEN_CONSTRAINTS` — every `x-required-when` annotation;
//!   same row shape as `AllowedWhen`, opposite semantic (leaf must be
//!   **present** when all gates resolve to allowed values).
//! - `ALLOWED_FIELD_CONSTRAINTS` — every `x-allowed-fields` annotation,
//!   expressed as `(json_pointer, allowed_fields)`.

use crate::schema::{JsonObject, SchemaDoc};

/// JSON Schema custom annotation: presence allow-list gated by sibling /
/// ancestor field values.  See validator's `apply_allowed_when_constraints`.
const X_ALLOWED_WHEN: &str = "x-allowed-when";

/// JSON Schema custom annotation: presence-required gated by sibling /
/// ancestor field values (mirror of `x-allowed-when`).  See validator's
/// `apply_required_when_constraints`.
const X_REQUIRED_WHEN: &str = "x-required-when";

/// JSON Schema custom annotation: object sub-key allow-list.  See validator's
/// `apply_allowed_field_constraints`.
const X_ALLOWED_FIELDS: &str = "x-allowed-fields";

pub fn generate_schema_constraints(doc: &SchemaDoc) -> String {
    let mut code = String::from("// AUTO-GENERATED FROM JSON SCHEMA - DO NOT EDIT MANUALLY\n");
    code.push_str("// Schema-derived structural constraints\n\n");

    emit_when_table(
        doc,
        &mut code,
        X_ALLOWED_WHEN,
        "AllowedWhen",
        ALLOWED_WHEN_STRUCT_DOC,
        "ALLOWED_WHEN_CONSTRAINTS",
    );
    code.push('\n');
    emit_when_table(
        doc,
        &mut code,
        X_REQUIRED_WHEN,
        "RequiredWhen",
        REQUIRED_WHEN_STRUCT_DOC,
        "REQUIRED_WHEN_CONSTRAINTS",
    );
    code.push('\n');
    emit_allowed_field_table(doc, &mut code);

    code
}

/// Per-struct rustdoc for `AllowedWhen` — paired with [`X_ALLOWED_WHEN`].
const ALLOWED_WHEN_STRUCT_DOC: &str =
    "/// One `x-allowed-when` constraint extracted from the schema.\n\
     ///\n\
     /// `parent_pointer` is the JSON Pointer (RFC 6901) to the parent of\n\
     /// the gated leaf in the schema.  At runtime the validator walks the\n\
     /// same path in the document, fanning out across `/items` segments,\n\
     /// then looks up `leaf_name` on each parent occurrence.\n\
     ///\n\
     /// `when` is a conjunction of `(gate_path, allowed_values)` predicates.\n\
     /// `gate_path` is a dotted segment list (e.g. `\"kind\"` or\n\
     /// `\"codeStatus.conversion.status\"`) resolved **lexically** from the\n\
     /// parent occurrence upward — the closest enclosing scope that\n\
     /// defines the gate's first segment wins.  Absent gate values are\n\
     /// vacuously satisfied so upstream presence checks can issue their\n\
     /// own dedicated diagnostics.\n";

/// Per-struct rustdoc for `RequiredWhen` — paired with [`X_REQUIRED_WHEN`].
const REQUIRED_WHEN_STRUCT_DOC: &str =
    "/// One `x-required-when` constraint extracted from the schema.\n\
     ///\n\
     /// Same shape as [`AllowedWhen`] but opposite semantic: the leaf is\n\
     /// **required to be present** when every gate resolves to one of its\n\
     /// allowed values.  Gate path resolution is identical (lexical from\n\
     /// the parent occurrence up).  Absent gates are vacuously satisfied,\n\
     /// matching [`AllowedWhen`] so upstream presence checks own the\n\
     /// `kind`-missing diagnostic.\n";

/// `(gate_path, allowed_values)` extracted from one gate entry of an
/// `x-allowed-when` / `x-required-when` annotation.  `gate_path` is a
/// dotted segment list resolved lexically by the validator.
type GatePredicate = (String, Vec<String>);

/// `(parent_pointer, leaf_name, gate_predicates)` — one row of either the
/// `x-allowed-when` or `x-required-when` table.  `parent_pointer` is a
/// JSON Pointer (RFC 6901) into the schema; `leaf_name` is the gated
/// property name within that parent.  Shared by both annotations because
/// the row shape is identical (only the runtime semantic differs).
type AllowedWhenRow = (String, String, Vec<GatePredicate>);

/// Emit a comma-separated list of quoted string literals — `"a", "b", "c"` —
/// for placement inside a Rust array literal.  Used wherever the codegen
/// needs to spell out a `&[&str]` element-by-element.
fn emit_quoted_str_list<S: AsRef<str>>(code: &mut String, items: &[S]) {
    for (i, s) in items.iter().enumerate() {
        if i > 0 {
            code.push_str(", ");
        }
        code.push_str(&format!("\"{}\"", s.as_ref()));
    }
}

/// Parse the `when` object of an `x-allowed-when` / `x-required-when`
/// annotation into a sorted list of `(gate_path, allowed_values)`
/// predicates.  Panics with a single-source-of-truth error message
/// keyed on `(annotation_key, pointer, gate)` whenever the annotation
/// is malformed — those are schema-authoring bugs that should fail the
/// build loudly.  Sorting here, not at the call site, keeps the
/// canonicalization next to the structure it canonicalizes.
fn parse_gate_predicates(
    when: &JsonObject,
    annotation_key: &str,
    pointer: &str,
) -> Vec<GatePredicate> {
    let mut gates: Vec<GatePredicate> = Vec::with_capacity(when.len());
    for (gate, values) in when {
        let allowed = values
            .as_array()
            .unwrap_or_else(|| {
                panic!(
                    "{annotation_key} at {pointer} expects an array of allowed values for '{gate}'"
                )
            })
            .iter()
            .map(|v| {
                v.as_str()
                    .unwrap_or_else(|| {
                        panic!(
                            "{annotation_key} at {pointer} expects string allowed values for '{gate}'"
                        )
                    })
                    .to_string()
            })
            .collect();
        gates.push((gate.clone(), allowed));
    }
    gates.sort_by(|a, b| a.0.cmp(&b.0));
    gates
}

/// Walk the schema for every annotation matching `annotation_key` and emit
/// a flat `(parent_pointer, leaf_name, when)` table that the schema-driven
/// validator can iterate over without re-parsing the schema at runtime.
///
/// Used by both `x-allowed-when` and `x-required-when` — the row shape is
/// identical (a presence-gated leaf with conjunctive sibling/ancestor
/// gates); only the runtime semantic and the emitted struct/const names
/// differ.  Per-struct rustdoc is passed in as `struct_doc` so the doc
/// describing the runtime semantic stays close to its struct definition.
fn emit_when_table(
    doc: &SchemaDoc,
    code: &mut String,
    annotation_key: &str,
    struct_name: &str,
    struct_doc: &str,
    const_name: &str,
) {
    let mut rows: Vec<AllowedWhenRow> = Vec::new();

    walk_for_annotations(doc, "", &doc.root, &mut |pointer, node| {
        let Some(when) = node.get(annotation_key).and_then(|v| v.as_object()) else {
            return;
        };
        let (parent_pointer, leaf_name) = split_schema_pointer(pointer)
            .unwrap_or_else(|| {
                panic!(
                    "{annotation_key} at {pointer} must sit on a property (parent_pointer/leaf split failed)"
                )
            });
        let gates = parse_gate_predicates(when, annotation_key, pointer);
        rows.push((parent_pointer, leaf_name, gates));
    });

    rows.sort_by(|a, b| a.0.cmp(&b.0).then_with(|| a.1.cmp(&b.1)));

    code.push_str(struct_doc);
    code.push_str(&format!(
        "pub struct {struct_name} {{\n    pub parent_pointer: &'static str,\n    pub leaf_name: &'static str,\n    pub when: &'static [(&'static str, &'static [&'static str])],\n}}\n\n",
    ));
    code.push_str(&format!("pub const {const_name}: &[{struct_name}] = &[\n"));
    for (parent_pointer, leaf_name, gates) in &rows {
        code.push_str(&format!("    {struct_name} {{\n"));
        code.push_str(&format!("        parent_pointer: \"{parent_pointer}\",\n"));
        code.push_str(&format!("        leaf_name: \"{leaf_name}\",\n"));
        code.push_str("        when: &[");
        for (i, (gate, allowed)) in gates.iter().enumerate() {
            if i > 0 {
                code.push_str(", ");
            }
            code.push_str(&format!("(\"{gate}\", &["));
            emit_quoted_str_list(code, allowed);
            code.push_str("])");
        }
        code.push_str("],\n");
        code.push_str("    },\n");
    }
    code.push_str("];\n");
}

/// Split a schema JSON Pointer that ends in `/properties/<name>` into the
/// `(parent_pointer, name)` parts used by [`AllowedWhen`].  Returns `None`
/// for pointers whose tail does not match this shape (malformed annotation).
fn split_schema_pointer(pointer: &str) -> Option<(String, String)> {
    // Pointer is expected to look like "/properties/foo/.../properties/leaf".
    let (parent, last) = pointer.rsplit_once('/')?;
    let (grand, properties) = parent.rsplit_once('/')?;
    if properties != "properties" {
        return None;
    }
    Some((grand.to_string(), last.to_string()))
}

/// Walk the schema for every `x-allowed-fields` annotation and emit a flat
/// table keyed by the JSON Pointer to the use site.
fn emit_allowed_field_table(doc: &SchemaDoc, code: &mut String) {
    let mut rows: Vec<(String, Vec<String>)> = Vec::new();

    walk_for_annotations(doc, "", &doc.root, &mut |pointer, node| {
        let Some(fields) = node.get(X_ALLOWED_FIELDS).and_then(|v| v.as_array()) else {
            return;
        };
        let allowed: Vec<String> = fields
            .iter()
            .map(|v| {
                v.as_str()
                    .unwrap_or_else(|| {
                        panic!("{X_ALLOWED_FIELDS} at {pointer} expects string entries")
                    })
                    .to_string()
            })
            .collect();
        rows.push((pointer.to_string(), allowed));
    });

    rows.sort_by(|a, b| a.0.cmp(&b.0));

    code.push_str(
        "/// One `x-allowed-fields` constraint at a `$ref`'d use site.\n\
         ///\n\
         /// `pointer` is the JSON Pointer (RFC 6901) to the constrained\n\
         /// reference within the schema document.  At runtime the validator\n\
         /// walks the same path in the code-unit document and rejects any\n\
         /// sub-field that is not in `allowed_fields`.\n\
         pub struct AllowedFieldConstraint {\n    pub pointer: &'static str,\n    pub allowed_fields: &'static [&'static str],\n}\n\n",
    );
    code.push_str("pub const ALLOWED_FIELD_CONSTRAINTS: &[AllowedFieldConstraint] = &[\n");
    for (pointer, allowed) in &rows {
        code.push_str("    AllowedFieldConstraint {\n");
        code.push_str(&format!("        pointer: \"{pointer}\",\n"));
        code.push_str("        allowed_fields: &[");
        emit_quoted_str_list(code, allowed);
        code.push_str("],\n");
        code.push_str("    },\n");
    }
    code.push_str("];\n");
}

/// Recursively walk the raw (unresolved) schema, calling `visit` for every
/// reachable property and array `items` node.  `$ref` nodes are resolved
/// for descent only — the *visited* node is the unresolved use-site value,
/// preserving any `x-*` annotations attached at the use site.
///
/// The callback receives the JSON Pointer (RFC 6901) of the current node
/// within the raw schema and the unresolved node value.  Both annotation
/// tables today key purely off the JSON Pointer — runtime path resolution
/// happens in the validator from the schema-side `parent_pointer`, so the
/// codegen has no need to track a separate semantic dotted path.
fn walk_for_annotations(
    doc: &SchemaDoc,
    json_pointer: &str,
    node: &serde_json::Value,
    visit: &mut impl FnMut(&str, &serde_json::Value),
) {
    visit(json_pointer, node);

    let resolved = doc.resolve(node);

    if let Some(properties) = resolved.get("properties").and_then(|p| p.as_object()) {
        let mut keys: Vec<&str> = properties.keys().map(|s| s.as_str()).collect();
        keys.sort();
        for name in keys {
            let child = &properties[name];
            let child_pointer = format!("{json_pointer}/properties/{name}");
            walk_for_annotations(doc, &child_pointer, child, visit);
        }
    }

    if let Some(items) = resolved.get("items") {
        let items_pointer = format!("{json_pointer}/items");
        walk_for_annotations(doc, &items_pointer, items, visit);
    }
}
