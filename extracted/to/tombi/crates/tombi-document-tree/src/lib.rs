//! Stable, implementation-independent operations over a semantic TOML document tree.
//!
//! This crate owns no parser, syntax tree, decoded-text pool, or document storage.
//! Tombi's source-backed implementation lives in `tombi-document-tree-syntax`.

use tombi_text::Span;

pub use tombi_date_time::{LocalDate, LocalDateTime, LocalTime, OffsetDateTime};

/// Common source-location operations for semantic document nodes.
pub trait Node {
    fn span(&self) -> Span;

    #[inline]
    fn symbol_span(&self) -> Span {
        self.span()
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum KeyKind {
    BareKey,
    BasicString,
    LiteralString,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StringKind {
    BasicString,
    LiteralString,
    MultiLineBasicString,
    MultiLineLiteralString,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IntegerKind {
    Binary,
    Octal,
    Decimal,
    Hexadecimal,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ArrayKind {
    ArrayOfTable,
    ParentArrayOfTable,
    Array,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TableKind {
    Root,
    Table,
    ParentTable,
    InlineTable { has_comment: bool },
    ParentKey,
    KeyValue,
}

macro_rules! copy_value {
    ($name:ident, $value:ty) => {
        #[derive(Debug, Clone, Copy, PartialEq)]
        pub struct $name {
            value: $value,
            span: Span,
        }

        impl $name {
            #[doc(hidden)]
            #[inline]
            pub fn new(value: $value, span: Span) -> Self {
                Self { value, span }
            }

            #[inline]
            pub fn value(self) -> $value {
                self.value
            }
        }

        impl Node for $name {
            #[inline]
            fn span(&self) -> Span {
                self.span
            }
        }
    };
}

copy_value!(BooleanValue, bool);
copy_value!(FloatValue, f64);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct IntegerValue {
    kind: IntegerKind,
    value: i64,
    span: Span,
}

impl IntegerValue {
    #[doc(hidden)]
    #[inline]
    pub fn new(kind: IntegerKind, value: i64, span: Span) -> Self {
        Self { kind, value, span }
    }

    #[inline]
    pub fn kind(self) -> IntegerKind {
        self.kind
    }

    #[inline]
    pub fn value(self) -> i64 {
        self.value
    }
}

impl Node for IntegerValue {
    #[inline]
    fn span(&self) -> Span {
        self.span
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct StringValue<'a> {
    kind: StringKind,
    content: &'a str,
    span: Span,
}

impl<'a> StringValue<'a> {
    #[doc(hidden)]
    #[inline]
    pub fn new(kind: StringKind, content: &'a str, span: Span) -> Self {
        Self {
            kind,
            content,
            span,
        }
    }

    #[inline]
    pub fn kind(self) -> StringKind {
        self.kind
    }

    #[inline]
    pub fn content(self) -> &'a str {
        self.content
    }

    #[inline]
    pub fn unquoted_span(self) -> Span {
        let mut span = self.span;
        let quote_width = match self.kind {
            StringKind::BasicString | StringKind::LiteralString => 1,
            StringKind::MultiLineBasicString | StringKind::MultiLineLiteralString => 3,
        };
        span.start += quote_width;
        span.end -= quote_width;
        span
    }
}

impl Node for StringValue<'_> {
    #[inline]
    fn span(&self) -> Span {
        self.span
    }
}

macro_rules! borrowed_value {
    ($name:ident, $value:ty) => {
        #[derive(Debug, Clone, Copy, PartialEq)]
        pub struct $name<'a> {
            value: &'a $value,
            span: Span,
        }

        impl<'a> $name<'a> {
            #[doc(hidden)]
            #[inline]
            pub fn new(value: &'a $value, span: Span) -> Self {
                Self { value, span }
            }

            #[inline]
            pub fn value(self) -> &'a $value {
                self.value
            }
        }

        impl Node for $name<'_> {
            #[inline]
            fn span(&self) -> Span {
                self.span
            }
        }
    };
}

borrowed_value!(OffsetDateTimeValue, OffsetDateTime);
borrowed_value!(LocalDateTimeValue, LocalDateTime);
borrowed_value!(LocalDateValue, LocalDate);
borrowed_value!(LocalTimeValue, LocalTime);

/// A semantic value that can be matched without exposing its storage.
#[derive(Debug, Clone, Copy)]
#[non_exhaustive]
pub enum Value<'a, A, T> {
    Boolean(BooleanValue),
    Integer(IntegerValue),
    Float(FloatValue),
    String(StringValue<'a>),
    OffsetDateTime(OffsetDateTimeValue<'a>),
    LocalDateTime(LocalDateTimeValue<'a>),
    LocalDate(LocalDateValue<'a>),
    LocalTime(LocalTimeValue<'a>),
    Array(&'a A),
    Table(&'a T),
    Incomplete { span: Span },
}

pub trait DocumentTree {
    type Table: Table;

    fn root(&self) -> &Self::Table;
}

pub trait Key: Node {
    fn kind(&self) -> KeyKind;
    fn content(&self) -> &str;
    fn unquoted_span(&self) -> Span;
}

pub trait Array: Node {
    type Value: ValueNode;

    fn kind(&self) -> ArrayKind;
    fn get(&self, index: usize) -> Option<&Self::Value>;
    fn values(&self) -> impl Iterator<Item = &Self::Value> + '_;
}

pub trait Table: Node {
    type Key: Key;
    type Value: ValueNode;

    fn kind(&self) -> TableKind;
    fn get(&self, key: &str) -> Option<&Self::Value>;
    fn get_key_value(&self, key: &str) -> Option<(&Self::Key, &Self::Value)>;
    fn entries(&self) -> impl Iterator<Item = (&Self::Key, &Self::Value)> + '_;
}

pub trait ValueNode: Node {
    type Array: Array<Value = Self>;
    type Table: Table<Value = Self>;

    fn value(&self) -> Value<'_, Self::Array, Self::Table>;
}

/// Follow semantic key/index accessors without exposing the tree's storage.
pub fn dig_accessors<'document, 'accessor, D>(
    document: &'document D,
    accessors: &'accessor [tombi_accessor::Accessor],
) -> Option<(
    &'accessor tombi_accessor::Accessor,
    &'document <<D as DocumentTree>::Table as Table>::Value,
)>
where
    D: DocumentTree,
    <D::Table as Table>::Value: ValueNode<Table = D::Table>,
{
    let first_key = accessors.first()?.as_key()?;
    let mut current_accessor = &accessors[0];
    let mut value = document.root().get(first_key);

    for accessor in &accessors[1..] {
        value = match (accessor, value?.value()) {
            (tombi_accessor::Accessor::Key(key), Value::Table(table)) => table.get(key.as_str()),
            (tombi_accessor::Accessor::Index(index), Value::Array(array)) => array.get(*index),
            _ => return None,
        };
        current_accessor = accessor;
    }

    Some((current_accessor, value?))
}
