// AUTO-GENERATED FROM JSON SCHEMA - DO NOT EDIT MANUALLY
// Schema-derived structural constraints

/// One `x-allowed-when` constraint extracted from the schema.
///
/// `parent_pointer` is the JSON Pointer (RFC 6901) to the parent of
/// the gated leaf in the schema.  At runtime the validator walks the
/// same path in the document, fanning out across `/items` segments,
/// then looks up `leaf_name` on each parent occurrence.
///
/// `when` is a conjunction of `(gate_path, allowed_values)` predicates.
/// `gate_path` is a dotted segment list (e.g. `"kind"` or
/// `"codeStatus.conversion.status"`) resolved **lexically** from the
/// parent occurrence upward — the closest enclosing scope that
/// defines the gate's first segment wins.  Absent gate values are
/// vacuously satisfied so upstream presence checks can issue their
/// own dedicated diagnostics.
pub struct AllowedWhen {
    pub parent_pointer: &'static str,
    pub leaf_name: &'static str,
    pub when: &'static [(&'static str, &'static [&'static str])],
}

pub const ALLOWED_WHEN_CONSTRAINTS: &[AllowedWhen] = &[
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "cloudStatus",
        when: &[("kind", &["databaseObject", "script"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "codeStatus",
        when: &[("kind", &["databaseObject", "script", "etl"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "files",
        when: &[("kind", &["databaseObject", "script", "etl"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "issues",
        when: &[("kind", &["databaseObject", "script", "etl"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "parts",
        when: &[("kind", &["etl"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "planning",
        when: &[("kind", &["databaseObject", "script", "etl"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "scriptBindings",
        when: &[("kind", &["script"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "scriptMetadata",
        when: &[("kind", &["script"])],
    },
    AllowedWhen {
        parent_pointer: "",
        leaf_name: "signature",
        when: &[("kind", &["databaseObject"])],
    },
    AllowedWhen {
        parent_pointer: "/properties/codeStatus",
        leaf_name: "stabilization",
        when: &[("kind", &["etl"])],
    },
    AllowedWhen {
        parent_pointer: "/properties/parts/items/properties/target",
        leaf_name: "modelName",
        when: &[("format", &["dbt"])],
    },
    AllowedWhen {
        parent_pointer: "/properties/source",
        leaf_name: "customKind",
        when: &[("kind", &["custom"])],
    },
    AllowedWhen {
        parent_pointer: "/properties/source",
        leaf_name: "format",
        when: &[("kind", &["databaseObject", "script"])],
    },
    AllowedWhen {
        parent_pointer: "/properties/target",
        leaf_name: "customKind",
        when: &[("kind", &["custom"])],
    },
    AllowedWhen {
        parent_pointer: "/properties/target",
        leaf_name: "format",
        when: &[("kind", &["databaseObject", "script"])],
    },
];

/// One `x-required-when` constraint extracted from the schema.
///
/// Same shape as [`AllowedWhen`] but opposite semantic: the leaf is
/// **required to be present** when every gate resolves to one of its
/// allowed values.  Gate path resolution is identical (lexical from
/// the parent occurrence up).  Absent gates are vacuously satisfied,
/// matching [`AllowedWhen`] so upstream presence checks own the
/// `kind`-missing diagnostic.
pub struct RequiredWhen {
    pub parent_pointer: &'static str,
    pub leaf_name: &'static str,
    pub when: &'static [(&'static str, &'static [&'static str])],
}

pub const REQUIRED_WHEN_CONSTRAINTS: &[RequiredWhen] = &[RequiredWhen {
    parent_pointer: "/properties/target",
    leaf_name: "format",
    when: &[
        ("codeStatus.conversion.status", &["completed"]),
        ("kind", &["script"]),
    ],
}];

/// One `x-allowed-fields` constraint at a `$ref`'d use site.
///
/// `pointer` is the JSON Pointer (RFC 6901) to the constrained
/// reference within the schema document.  At runtime the validator
/// walks the same path in the code-unit document and rejects any
/// sub-field that is not in `allowed_fields`.
pub struct AllowedFieldConstraint {
    pub pointer: &'static str,
    pub allowed_fields: &'static [&'static str],
}

pub const ALLOWED_FIELD_CONSTRAINTS: &[AllowedFieldConstraint] = &[AllowedFieldConstraint {
    pointer: "/properties/parts/items/properties/cloudStatus",
    allowed_fields: &["testing", "deployment"],
}];
