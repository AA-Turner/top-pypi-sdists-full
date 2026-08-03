//! Shared "JSON-fragment-text -> typed Arrow column" toolkit.
//!
//! Extracted from `python.rs`'s Arrow-native `normalise()` reconstruction
//! (`build_normalise_table`, github.com/amaye15/JSON-Tools-rs/issues/35) so
//! it can also back the flat-DataFrame fast path for plain
//! `execute(df)` -- both need the exact same per-cell type classification
//! (bool > numeric > string > temporal priority, mixed -> stringify) and
//! Arrow builder dispatch, just fed from different sources (JSON-parsed rows
//! for `normalise()`, directly-extracted column values for the fast path).
//!
//! Every function here operates on plain JSON-fragment text (e.g. `123`,
//! `true`, `"2024-01-15"` -- a bare token or a JSON-quoted string, never a
//! full document) via `&str`, with no dependency on `serde_json::Value` or
//! row/document structure -- callers own how they got that text.
//!
//! The whole module is gated on the `python` feature at its declaration site
//! (`lib.rs`), not here -- everything in it depends on `arrow-array`/
//! `arrow-schema`, which are only pulled in for that feature.

use arrow_array::builder::{
    ArrayBuilder, BooleanBuilder, Date32Builder, Float64Builder, Int64Builder, ListBuilder,
    StringBuilder, TimestampMicrosecondBuilder,
};
use arrow_array::ArrayRef;
use arrow_schema::{DataType, Field};
use std::sync::Arc;

/// Scalar Arrow type a column (or a list column's element type) resolves to.
/// `Date32`/`TimestampUtcMicros` are scalar-column-only (never a list
/// element's type -- see `ColumnPlan`'s doc comment) and only ever chosen
/// when the caller's `.convert_dates()`/`.auto_convert_types()` config is
/// enabled (see `raw_scalar_kind`'s `dates_enabled` parameter) -- this
/// engine never independently pattern-matches a plain string into a date
/// against the user's own wishes, only promotes what the core engine's own
/// existing, opt-in date recognition already normalized.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum ScalarKind {
    Bool,
    Int64,
    Float64,
    Date32,
    TimestampUtcMicros,
    Utf8,
}

/// A column's overall shape: either every row's value is a scalar, or at
/// least one row's value is a JSON array (in which case every other non-null
/// cell is treated as a single-element list of that same element kind --
/// same "once any row is list-valued, wrap every other cell too" rule
/// `union_and_columnarize` used, ported unchanged). List columns never
/// resolve to `Date32`/`TimestampUtcMicros` -- date detection only runs at
/// the top level (see `raw_scalar_kind`); a date-shaped string inside a
/// `handle_key_collision(True)` array is deliberately left as plain text,
/// a narrow, explicit scope boundary rather than doubling the number of
/// `ColumnBuilder::List*` variants for a very rare combination.
#[derive(Debug, Clone, Copy)]
pub(crate) enum ColumnPlan {
    Scalar(ScalarKind),
    List(ScalarKind),
}

/// Per-column (or per-list-column-element) kind flags accumulated during a
/// classification scan -- mirrors the old `classify_scalar_kind`'s (bool,
/// numeric, str) triple, split into (bool, int, float, date, datetime) since
/// this engine -- unlike a `PyAny`-based approach, which gets int/float
/// distinction for free from Python's own object types -- must decide the
/// exact Arrow type itself to pick the right builder.
#[derive(Default, Clone, Copy)]
pub(crate) struct KindFlags {
    pub(crate) bool_: bool,
    pub(crate) int_: bool,
    pub(crate) float_: bool,
    pub(crate) str_: bool,
    pub(crate) date_: bool,
    pub(crate) datetime_: bool,
}

impl KindFlags {
    pub(crate) fn merge(&mut self, other: KindFlags) {
        self.bool_ |= other.bool_;
        self.int_ |= other.int_;
        self.float_ |= other.float_;
        self.str_ |= other.str_;
        self.date_ |= other.date_;
        self.datetime_ |= other.datetime_;
    }

    /// Resolve to a single Arrow scalar type, matching `classify_scalar_kind`'s
    /// established priority: any 2+ of {bool, numeric, str, temporal} present ->
    /// stringify fallback (Utf8); numeric alone -> Float64 if any float seen
    /// (including an integer too large for i64, downgraded here rather than
    /// erroring -- an accepted precision tradeoff for a value this large) else
    /// Int64; temporal alone -> TimestampUtcMicros if any genuine datetime seen
    /// (a bare date promotes to midnight UTC, the same "promote the narrower
    /// kind" pattern int->float already uses) else Date32 if only bare dates;
    /// str alone, or nothing seen at all (all-null column) -> Utf8, matching the
    /// old all-None default.
    pub(crate) fn resolve(&self) -> ScalarKind {
        let numeric = self.int_ || self.float_;
        let temporal = self.date_ || self.datetime_;
        let kinds_present = [self.bool_, numeric, self.str_, temporal]
            .into_iter()
            .filter(|p| *p)
            .count();
        if kinds_present > 1 {
            ScalarKind::Utf8
        } else if self.bool_ {
            ScalarKind::Bool
        } else if self.float_ {
            ScalarKind::Float64
        } else if self.int_ {
            ScalarKind::Int64
        } else if self.datetime_ {
            ScalarKind::TimestampUtcMicros
        } else if self.date_ {
            ScalarKind::Date32
        } else {
            ScalarKind::Utf8
        }
    }
}

/// Classify a single JSON scalar leaf's raw text. Returns `None` for `null`
/// (nulls never contribute to kind flags -- consistent with treating null as
/// compatible with any column, same as the old Python-`None` handling).
/// Callers only ever hand this a genuine scalar or a literal `{}` -- flatten
/// mode's own recursive expansion means a non-empty object/array can never
/// survive as a leaf (verified directly against `flatten.rs`'s walkers), and
/// a non-empty `[...]` is filtered out before this is reached (routed to the
/// list-column path instead). A literal **empty object** `{}` is the one
/// object-shaped leaf that *can* still reach here (when
/// `remove_empty_objects(False)` is set) -- classified as `str_` and
/// stringified to its own literal text `"{}"`, the same "unusual value ->
/// stringify" treatment already applied to any other kind this engine can't
/// give a cleaner Arrow type. Confirmed via direct reproduction that without
/// this case, `{}`'s `{` first byte fell through to the number-parsing
/// branch below and panicked on the inevitable parse failure.
/// `dates_enabled` gates date/datetime detection on the caller's own
/// `.convert_dates()`/`.auto_convert_types()` setting (checked once by the
/// caller, not re-derived per cell) -- this engine never independently
/// pattern-matches an ordinary string into a date; it only promotes what the
/// core flatten engine's own opt-in date recognition already normalized into
/// this crate's fixed ISO8601 shape (`convert.rs`'s
/// `try_parse_and_normalize_iso8601`: a bare `YYYY-MM-DD` date, or a
/// `Z`/offset-suffixed RFC3339 datetime -- always normalized to UTC when
/// recognized). When disabled, a date-shaped string is just an ordinary
/// string, same as before this feature existed.
pub(crate) fn raw_scalar_kind(text: &str, dates_enabled: bool) -> Option<KindFlags> {
    match *text.as_bytes().first()? {
        b'n' => None, // null
        b't' | b'f' => Some(KindFlags {
            bool_: true,
            ..Default::default()
        }),
        b'"' => {
            // Cheap quote-stripping, not full JSON unescaping: this crate's own
            // normalized date/datetime text never contains characters that need
            // escaping (only digits/`-`/`:`/`T`/`.`/`Z`/offset signs), so a plain
            // slice is safe and avoids an allocation for the common case where
            // dates_enabled is true but this particular string isn't a date --
            // an escaped string that coincidentally looked date-shaped after
            // naive slicing would just fail the strict chrono parse below and
            // fall through to the ordinary str_ classification, harmlessly.
            if dates_enabled && text.len() >= 2 {
                let inner = &text[1..text.len() - 1];
                match parse_normalized_date_or_datetime(inner) {
                    Some(DateOrDateTime::Date(_)) => {
                        return Some(KindFlags {
                            date_: true,
                            ..Default::default()
                        })
                    }
                    Some(DateOrDateTime::DateTime(_)) => {
                        return Some(KindFlags {
                            datetime_: true,
                            ..Default::default()
                        })
                    }
                    None => {}
                }
            }
            Some(KindFlags {
                str_: true,
                ..Default::default()
            })
        }
        b'{' => Some(KindFlags {
            str_: true,
            ..Default::default()
        }),
        _ => {
            // Number: `.`/`e`/`E` or an integer too large for i64 both need
            // Float64; everything else fits Int64.
            let is_float_syntax = text.bytes().any(|b| matches!(b, b'.' | b'e' | b'E'));
            if !is_float_syntax && text.parse::<i64>().is_ok() {
                Some(KindFlags {
                    int_: true,
                    ..Default::default()
                })
            } else {
                Some(KindFlags {
                    float_: true,
                    ..Default::default()
                })
            }
        }
    }
}

/// A successfully-recognized date or datetime, from `parse_normalized_date_or_datetime`.
enum DateOrDateTime {
    Date(chrono::NaiveDate),
    DateTime(chrono::DateTime<chrono::Utc>),
}

/// Attempt to parse `inner` (already quote-stripped) as this engine's own
/// normalized date/datetime shape -- a real `chrono` parse (RFC3339 for
/// datetimes, `%Y-%m-%d` for bare dates), not a regex/length heuristic, so a
/// malformed or merely date-*looking* string never false-positives.
fn parse_normalized_date_or_datetime(inner: &str) -> Option<DateOrDateTime> {
    if let Ok(date) = chrono::NaiveDate::parse_from_str(inner, "%Y-%m-%d") {
        return Some(DateOrDateTime::Date(date));
    }
    if let Ok(dt) = chrono::DateTime::parse_from_rfc3339(inner) {
        return Some(DateOrDateTime::DateTime(dt.with_timezone(&chrono::Utc)));
    }
    None
}

/// Days since the Unix epoch, for building a `Date32Builder` value.
fn date32_days(date: chrono::NaiveDate) -> i32 {
    date.signed_duration_since(chrono::NaiveDate::from_ymd_opt(1970, 1, 1).expect("valid date"))
        .num_days() as i32
}

/// Python `str()`-equivalent text for a raw JSON scalar leaf -- used only for
/// the mixed-kind stringify fallback, so behavior matches what
/// `union_and_columnarize`'s old `cell.str()?` already produced: a JSON
/// string's own (unescaped) content, `True`/`False` (capitalized, matching
/// Python bool's `__str__`) for booleans, and a number's own JSON text
/// as-is (Python's `str(int)`/`str(float)` and JSON's own number formatting
/// agree for the vast majority of real values; an exact byte-for-byte match
/// of Python's float-repr algorithm is not chased here -- this is already a
/// best-effort fallback for a column too heterogeneous to type cleanly, not
/// a precision-critical path).
pub(crate) fn stringify_raw(text: &str) -> std::borrow::Cow<'_, str> {
    match text.as_bytes().first() {
        Some(b'"') => match serde_json::from_str::<String>(text) {
            Ok(s) => std::borrow::Cow::Owned(s),
            Err(_) => std::borrow::Cow::Borrowed(text),
        },
        Some(b't') => std::borrow::Cow::Borrowed("True"),
        Some(b'f') => std::borrow::Cow::Borrowed("False"),
        _ => std::borrow::Cow::Borrowed(text),
    }
}

/// One column's Arrow array under construction. A `List*` variant's inner
/// builder holds every list cell's elements back-to-back; `append` calls on
/// the outer `ListBuilder` mark each cell's boundary (`append(true)` for a
/// present -- possibly empty -- list, `append(false)` for a null cell).
pub(crate) enum ColumnBuilder {
    Bool(BooleanBuilder),
    Int64(Int64Builder),
    Float64(Float64Builder),
    Date32(Date32Builder),
    TimestampUtcMicros(TimestampMicrosecondBuilder),
    Utf8(StringBuilder),
    ListBool(ListBuilder<BooleanBuilder>),
    ListInt64(ListBuilder<Int64Builder>),
    ListFloat64(ListBuilder<Float64Builder>),
    ListUtf8(ListBuilder<StringBuilder>),
}

impl ColumnBuilder {
    pub(crate) fn new(plan: ColumnPlan, capacity: usize) -> Self {
        match plan {
            ColumnPlan::Scalar(ScalarKind::Bool) => {
                ColumnBuilder::Bool(BooleanBuilder::with_capacity(capacity))
            }
            ColumnPlan::Scalar(ScalarKind::Int64) => {
                ColumnBuilder::Int64(Int64Builder::with_capacity(capacity))
            }
            ColumnPlan::Scalar(ScalarKind::Float64) => {
                ColumnBuilder::Float64(Float64Builder::with_capacity(capacity))
            }
            ColumnPlan::Scalar(ScalarKind::Date32) => {
                ColumnBuilder::Date32(Date32Builder::with_capacity(capacity))
            }
            ColumnPlan::Scalar(ScalarKind::TimestampUtcMicros) => {
                ColumnBuilder::TimestampUtcMicros(
                    TimestampMicrosecondBuilder::with_capacity(capacity).with_timezone("UTC"),
                )
            }
            ColumnPlan::Scalar(ScalarKind::Utf8) => {
                ColumnBuilder::Utf8(StringBuilder::with_capacity(capacity, capacity * 8))
            }
            ColumnPlan::List(ScalarKind::Bool) => {
                ColumnBuilder::ListBool(ListBuilder::with_capacity(BooleanBuilder::new(), capacity))
            }
            ColumnPlan::List(ScalarKind::Int64) => {
                ColumnBuilder::ListInt64(ListBuilder::with_capacity(Int64Builder::new(), capacity))
            }
            ColumnPlan::List(ScalarKind::Float64) => ColumnBuilder::ListFloat64(
                ListBuilder::with_capacity(Float64Builder::new(), capacity),
            ),
            ColumnPlan::List(ScalarKind::Utf8) => {
                ColumnBuilder::ListUtf8(ListBuilder::with_capacity(StringBuilder::new(), capacity))
            }
            // Date32/TimestampUtcMicros are never chosen for a List plan --
            // see ColumnPlan's doc comment (date detection is scalar-only).
            ColumnPlan::List(ScalarKind::Date32 | ScalarKind::TimestampUtcMicros) => {
                unreachable!("date/datetime kinds are never resolved for a list column")
            }
        }
    }

    pub(crate) fn arrow_field(&self, name: &str) -> Field {
        fn item_field(kind_dt: DataType) -> Arc<Field> {
            Arc::new(Field::new("item", kind_dt, true))
        }
        let dt = match self {
            ColumnBuilder::Bool(_) => DataType::Boolean,
            ColumnBuilder::Int64(_) => DataType::Int64,
            ColumnBuilder::Float64(_) => DataType::Float64,
            ColumnBuilder::Date32(_) => DataType::Date32,
            ColumnBuilder::TimestampUtcMicros(_) => {
                DataType::Timestamp(arrow_schema::TimeUnit::Microsecond, Some("UTC".into()))
            }
            ColumnBuilder::Utf8(_) => DataType::Utf8,
            ColumnBuilder::ListBool(_) => DataType::List(item_field(DataType::Boolean)),
            ColumnBuilder::ListInt64(_) => DataType::List(item_field(DataType::Int64)),
            ColumnBuilder::ListFloat64(_) => DataType::List(item_field(DataType::Float64)),
            ColumnBuilder::ListUtf8(_) => DataType::List(item_field(DataType::Utf8)),
        };
        Field::new(name, dt, true)
    }

    /// Append one row's raw JSON-fragment text. `raw = None` means the value
    /// is entirely absent (union null-fill, or a fast-path cell filtered to
    /// null); `Some(text)` where `text` is JSON `null` means present but
    /// explicitly null -- both append a null cell. Takes the fragment text
    /// directly (not a `&serde_json::value::RawValue`) so callers that never
    /// had a `RawValue` in the first place (the columnar fast path, which
    /// reads Arrow/pandas values directly) don't need to fabricate one just
    /// to call this. Every `.parse()`/text-shape assumption below is
    /// guaranteed to hold by the caller's own prior classification pass
    /// (this column's `ColumnPlan` was derived from scanning these exact same
    /// values) -- `.expect()` on failure indicates a bug in that
    /// classification, not a possible-in-practice user-facing error, and PyO3
    /// converts an `#[pymethod]`-body panic into a Python exception rather
    /// than crashing.
    pub(crate) fn append_row(&mut self, text: Option<&str>) {
        let is_null = text.is_none() || text.map(|t| t.as_bytes()[0]) == Some(b'n');
        match self {
            ColumnBuilder::Bool(b) => {
                if is_null {
                    b.append_null();
                } else {
                    b.append_value(text.expect("checked non-null above") == "true");
                }
            }
            ColumnBuilder::Int64(b) => {
                if is_null {
                    b.append_null();
                } else {
                    let t = text.expect("checked non-null above");
                    b.append_value(
                        t.parse::<i64>()
                            .expect("Pass 1 classified this column Int64"),
                    );
                }
            }
            ColumnBuilder::Float64(b) => {
                if is_null {
                    b.append_null();
                } else {
                    let t = text.expect("checked non-null above");
                    b.append_value(
                        t.parse::<f64>()
                            .expect("Pass 1 classified this column Float64"),
                    );
                }
            }
            ColumnBuilder::Date32(b) => {
                if is_null {
                    b.append_null();
                } else {
                    let t = text.expect("checked non-null above");
                    let inner = &t[1..t.len() - 1];
                    let parsed = parse_normalized_date_or_datetime(inner)
                        .expect("Pass 1 classified this column Date32");
                    let DateOrDateTime::Date(date) = parsed else {
                        unreachable!("Date32 column never sees a genuine datetime value")
                    };
                    b.append_value(date32_days(date));
                }
            }
            ColumnBuilder::TimestampUtcMicros(b) => {
                if is_null {
                    b.append_null();
                } else {
                    let t = text.expect("checked non-null above");
                    let inner = &t[1..t.len() - 1];
                    let parsed = parse_normalized_date_or_datetime(inner)
                        .expect("Pass 1 classified this column TimestampUtcMicros");
                    let micros = match parsed {
                        DateOrDateTime::Date(d) => d
                            .and_hms_opt(0, 0, 0)
                            .expect("valid time")
                            .and_utc()
                            .timestamp_micros(),
                        DateOrDateTime::DateTime(dt) => dt.timestamp_micros(),
                    };
                    b.append_value(micros);
                }
            }
            ColumnBuilder::Utf8(b) => {
                if is_null {
                    b.append_null();
                } else {
                    b.append_value(stringify_raw(text.expect("checked non-null above")));
                }
            }
            ColumnBuilder::ListBool(_)
            | ColumnBuilder::ListInt64(_)
            | ColumnBuilder::ListFloat64(_)
            | ColumnBuilder::ListUtf8(_) => {
                unreachable!("list columns are appended via append_list_cell, not append_row")
            }
        }
    }

    /// Append one row's pre-parsed list cell (see `ListCell`'s doc comment
    /// for why this takes an already-parsed cell rather than raw text).
    pub(crate) fn append_list_cell(&mut self, cell: &ListCell<'_>) {
        match self {
            ColumnBuilder::ListBool(b) => append_list_row(b, cell, |inner, t| match t {
                Some(t) => inner.append_value(t == "true"),
                None => inner.append_null(),
            }),
            ColumnBuilder::ListInt64(b) => append_list_row(b, cell, |inner, t| match t {
                Some(t) => inner.append_value(
                    t.parse::<i64>()
                        .expect("Pass 1 classified this column's list elements Int64"),
                ),
                None => inner.append_null(),
            }),
            ColumnBuilder::ListFloat64(b) => append_list_row(b, cell, |inner, t| match t {
                Some(t) => inner.append_value(
                    t.parse::<f64>()
                        .expect("Pass 1 classified this column's list elements Float64"),
                ),
                None => inner.append_null(),
            }),
            ColumnBuilder::ListUtf8(b) => append_list_row(b, cell, |inner, t| match t {
                Some(t) => inner.append_value(stringify_raw(t)),
                None => inner.append_null(),
            }),
            _ => unreachable!("append_list_cell only called for List* ColumnBuilder variants"),
        }
    }

    pub(crate) fn finish(self) -> ArrayRef {
        match self {
            ColumnBuilder::Bool(mut b) => Arc::new(b.finish()),
            ColumnBuilder::Int64(mut b) => Arc::new(b.finish()),
            ColumnBuilder::Float64(mut b) => Arc::new(b.finish()),
            ColumnBuilder::Date32(mut b) => Arc::new(b.finish()),
            ColumnBuilder::TimestampUtcMicros(mut b) => Arc::new(b.finish()),
            ColumnBuilder::Utf8(mut b) => Arc::new(b.finish()),
            ColumnBuilder::ListBool(mut b) => Arc::new(b.finish()),
            ColumnBuilder::ListInt64(mut b) => Arc::new(b.finish()),
            ColumnBuilder::ListFloat64(mut b) => Arc::new(b.finish()),
            ColumnBuilder::ListUtf8(mut b) => Arc::new(b.finish()),
        }
    }
}

/// A list column's cell, pre-parsed exactly once during the classification
/// scan and reused during the build scan -- the array text used to be parsed
/// twice (once to classify element kinds, once again to build), a real,
/// measured cost for `handle_key_collision(True)`'s own headline scenario
/// (many rows, each a JSON array). Caching the parse result for one column
/// at a time (freed once that column's `ArrayRef` is built) avoids the
/// second `serde_json::from_str` + `Vec` allocation per cell without
/// changing memory scaling (bounded by that single column's row count
/// either way).
pub(crate) enum ListCell<'a> {
    /// Key entirely absent from this row (union null-fill).
    Absent,
    /// Key present but explicitly JSON `null`.
    Null,
    /// A genuine JSON array, already split into its top-level elements.
    Elems(Vec<&'a serde_json::value::RawValue>),
    /// A scalar cell in a list-typed column: wraps into a single-element
    /// list, same as `union_and_columnarize`'s existing rule.
    Scalar(&'a str),
}

/// Shared per-row append logic for every `List*` `ColumnBuilder` variant --
/// `append_elem` does the one type-specific thing (parse this element's text
/// into the inner builder's own value type, or append a null when given
/// `None`); everything else (null cell vs. present list vs. wrapped scalar)
/// is identical across all four element types. Takes an already-parsed
/// `ListCell` (see its doc comment) rather than raw text, so this never
/// re-parses a JSON array that the classification pass already parsed.
fn append_list_row<T: ArrayBuilder>(
    list_builder: &mut ListBuilder<T>,
    cell: &ListCell<'_>,
    mut append_elem: impl FnMut(&mut T, Option<&str>),
) {
    match cell {
        ListCell::Absent | ListCell::Null => list_builder.append(false),
        ListCell::Elems(elems) => {
            for elem in elems {
                let elem_text = elem.get();
                if elem_text.as_bytes().first() == Some(&b'n') {
                    append_elem(list_builder.values(), None);
                } else {
                    append_elem(list_builder.values(), Some(elem_text));
                }
            }
            list_builder.append(true);
        }
        ListCell::Scalar(text) => {
            append_elem(list_builder.values(), Some(text));
            list_builder.append(true);
        }
    }
}
