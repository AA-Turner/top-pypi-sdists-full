//! Indexed fields, their derived values, and candidate prefilters for
//! backends that can push filters down (SQLite).
//!
//! A [`Prefilter`] is a **conservative** condition over [`IndexedField`]s:
//! every document the original predicate (a [`crate::filter::Filter`] or a
//! `find_by_object` partial) would match also satisfies the prefilter. The
//! backend uses it only to pick *candidates* through its indexes; the
//! registry then runs the original predicate over the candidates, so results
//! are identical with or without pushdown.
//!
//! The guarantee is stated for **regular** documents only (see [`derive`]).
//! Backends must always include irregular documents in the candidate set,
//! which keeps every strict-load error (invalid JSON, a value serde rejects,
//! ID/key mismatch, migration failures) surfacing for filtered reads.

use serde_json::Value;

use crate::registry::loader::parse_stored;

/// The JSON type an indexed field holds in a regular document.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum FieldKind {
    /// JSON string.
    Text,
    /// JSON integer.
    Integer,
    /// JSON boolean, indexed as `1` / `0`.
    Bool,
}

/// A code unit field mirrored into an indexed column.
///
/// A field's *indexed value* for a regular document is its value in the
/// typed serialization of the strictly parsed unit — exactly the JSON the
/// registry's predicates evaluate (see [`derive`]): a JSON string as text, an
/// integer as is, `true` / `false` as `1` / `0`, absent or `null` as SQL
/// `NULL`. Serde defaults (`inScope`, `isMissing`) are therefore always
/// present.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub(crate) enum IndexedField {
    /// The code unit `id`. Backed by the storage key itself (no column of
    /// its own): for a regular document the embedded `id` is absent or
    /// equals the key, and the loader sets an absent `id` to the key, so the
    /// predicate always sees `id` = key.
    Id,
    Kind,
    SourceObjectType,
    TargetObjectType,
    SourceDatabase,
    SourceSchema,
    SourceName,
    SourceCanonicalName,
    TargetDatabase,
    TargetSchema,
    Wave,
    InScope,
    IsMissing,
}

impl IndexedField {
    /// Number of indexed fields.
    pub(crate) const COUNT: usize = 13;

    pub(crate) const ALL: [IndexedField; Self::COUNT] = [
        Self::Id,
        Self::Kind,
        Self::SourceObjectType,
        Self::TargetObjectType,
        Self::SourceDatabase,
        Self::SourceSchema,
        Self::SourceName,
        Self::SourceCanonicalName,
        Self::TargetDatabase,
        Self::TargetSchema,
        Self::Wave,
        Self::InScope,
        Self::IsMissing,
    ];

    /// JSON path segments of the field, as used in filter expressions.
    pub(crate) fn path(self) -> &'static [&'static str] {
        match self {
            Self::Id => &["id"],
            Self::Kind => &["kind"],
            Self::SourceObjectType => &["source", "objectType"],
            Self::TargetObjectType => &["target", "objectType"],
            Self::SourceDatabase => &["source", "database"],
            Self::SourceSchema => &["source", "schema"],
            Self::SourceName => &["source", "name"],
            Self::SourceCanonicalName => &["source", "canonicalName"],
            Self::TargetDatabase => &["target", "database"],
            Self::TargetSchema => &["target", "schema"],
            Self::Wave => &["planning", "wave"],
            Self::InScope => &["inScope"],
            Self::IsMissing => &["isMissing"],
        }
    }

    pub(crate) fn kind(self) -> FieldKind {
        match self {
            Self::Wave => FieldKind::Integer,
            Self::InScope | Self::IsMissing => FieldKind::Bool,
            _ => FieldKind::Text,
        }
    }

    /// Value serde substitutes when a stored document omits the field
    /// (`inScope` defaults to `true`, `isMissing` to `false`). Such a field
    /// is a plain `bool` in `CodeUnit`, so its indexed value is never `NULL`
    /// for a regular document.
    pub(crate) fn default_value(self) -> Option<IndexValue> {
        match self {
            Self::InScope => Some(IndexValue::Integer(1)),
            Self::IsMissing => Some(IndexValue::Integer(0)),
            _ => None,
        }
    }

    /// Storage column name for the field.
    pub(crate) fn column(self) -> &'static str {
        match self {
            Self::Id => "id",
            Self::Kind => "kind",
            Self::SourceObjectType => "source_object_type",
            Self::TargetObjectType => "target_object_type",
            Self::SourceDatabase => "source_database",
            Self::SourceSchema => "source_schema",
            Self::SourceName => "source_name",
            Self::SourceCanonicalName => "source_canonical_name",
            Self::TargetDatabase => "target_database",
            Self::TargetSchema => "target_schema",
            Self::Wave => "wave",
            Self::InScope => "in_scope",
            Self::IsMissing => "is_missing",
        }
    }

    /// Whether the field is the storage key column rather than a column
    /// holding a derived value.
    pub(crate) fn is_storage_key(self) -> bool {
        self == Self::Id
    }

    /// Look up the indexed field with the given JSON path, if any.
    pub(crate) fn from_path<S: AsRef<str>>(path: &[S]) -> Option<Self> {
        Self::ALL.into_iter().find(|f| {
            f.path().len() == path.len() && f.path().iter().zip(path).all(|(a, b)| *a == b.as_ref())
        })
    }
}

/// A comparison operand in a [`Prefilter`].
#[derive(Debug, Clone, PartialEq)]
pub(crate) enum IndexValue {
    Text(String),
    Integer(i64),
}

/// One end of a [`Prefilter::Range`].
#[derive(Debug, Clone, PartialEq)]
pub(crate) struct Bound {
    pub(crate) value: IndexValue,
    pub(crate) inclusive: bool,
}

/// Conservative candidate condition (see module docs). SQL semantics over
/// the indexed values: a comparison with a `NULL` indexed value is false.
#[derive(Debug, Clone, PartialEq)]
pub(crate) enum Prefilter {
    /// All must hold. An empty `And` is true.
    And(Vec<Prefilter>),
    /// At least one must hold. An empty `Or` is false.
    Or(Vec<Prefilter>),
    /// The indexed value equals one of `values` (SQL `IN`, `BINARY` collation).
    In(IndexedField, Vec<IndexValue>),
    /// The indexed value lies within the bounds (either may be open; with
    /// both open it is true, `NULL` included).
    Range {
        field: IndexedField,
        low: Option<Bound>,
        high: Option<Bound>,
    },
    /// The indexed value is SQL `NULL` (`negated`: is not `NULL`).
    IsNull { field: IndexedField, negated: bool },
}

// ── Derived values ──────────────────────────────────────────────────────

/// What an index stores for one document: whether it is regular, and the
/// indexed value of every field.
#[derive(Debug, Clone, PartialEq)]
pub(crate) struct Derived {
    pub(crate) regular: bool,
    /// The indexed value of each of [`IndexedField::ALL`], in that order
    /// (`None` = SQL `NULL`). All `None` when the document is not regular.
    pub(crate) values: [Option<IndexValue>; IndexedField::COUNT],
}

impl Derived {
    /// The indexed value of `field`.
    pub(crate) fn value(&self, field: IndexedField) -> Option<&IndexValue> {
        let position = IndexedField::ALL.iter().position(|f| *f == field);
        self.values[position.expect("field is in ALL")].as_ref()
    }
}

/// Derive the indexed values of the document stored under `key` as `text`.
///
/// The document is **regular** when the strict load every read applies
/// succeeds ([`parse_stored`]: JSON syntax, schema migration, deserializing
/// into `CodeUnit`, embedded `id` absent or equal to `key`) and its typed
/// serialization holds every indexed field with its [`FieldKind`]'s JSON
/// type (or `null` / absent). The values then come from that serialization
/// with `id` = `key`, which is the very JSON `Filter::matches` and
/// `matches_partial` evaluate — after migration, after serde defaults and
/// with serde's handling of duplicate keys (the last one wins). A predicate
/// over the indexed fields therefore sees exactly the indexed values of a
/// regular document, and every other document is a candidate for every
/// filtered read.
///
/// The result depends on this library's `CodeUnit` and schema migrations,
/// which is why the SQLite index file is keyed on a hash of the schema (see
/// `sqlite.rs`). Changing this function's logic needs an index format bump.
pub(crate) fn derive(key: &str, text: &str) -> Derived {
    let values = parse_stored(key, text, String::new)
        .ok()
        .and_then(|unit| serde_json::to_value(&unit).ok())
        .and_then(|seen| indexed_values(&seen));
    match values {
        Some(values) => Derived {
            regular: true,
            values,
        },
        None => Derived {
            regular: false,
            values: Default::default(),
        },
    }
}

/// Indexed values of the typed serialization `seen`; `None` when a field
/// holds a JSON type other than its kind's (impossible for a `CodeUnit`,
/// and then the document is simply irregular).
fn indexed_values(seen: &Value) -> Option<[Option<IndexValue>; IndexedField::COUNT]> {
    let mut values: [Option<IndexValue>; IndexedField::COUNT] = Default::default();
    for (slot, field) in values.iter_mut().zip(IndexedField::ALL) {
        *slot = indexed_value(field, seen)?;
    }
    Some(values)
}

/// `Some(value)` (`None` = `NULL`) when `field` is absent, `null`, or holds
/// its kind's JSON type in `seen`; `None` otherwise.
fn indexed_value(field: IndexedField, seen: &Value) -> Option<Option<IndexValue>> {
    let mut value = seen;
    for segment in field.path() {
        value = match value {
            Value::Object(map) => match map.get(*segment) {
                Some(child) => child,
                None => return Some(None),
            },
            Value::Null => return Some(None),
            _ => return None,
        };
    }
    match (field.kind(), value) {
        (_, Value::Null) => Some(None),
        (FieldKind::Text, Value::String(s)) => Some(Some(IndexValue::Text(s.clone()))),
        (FieldKind::Integer, Value::Number(n)) => Some(Some(IndexValue::Integer(n.as_i64()?))),
        (FieldKind::Bool, Value::Bool(b)) => Some(Some(IndexValue::Integer(i64::from(*b)))),
        _ => None,
    }
}
