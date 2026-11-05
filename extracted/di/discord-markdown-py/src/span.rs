use std::{
	fmt::Debug,
	ops::{Deref, DerefMut},
};

use crate::lossless::TokenKind;

/// A value `T` annotated with a span `S`.
#[derive(Clone, PartialEq, Eq, Default)]
pub struct Spanned<T, S> {
	pub value: T,
	pub span: S,
}

impl<T, S> Debug for Spanned<T, S>
where
	T: Debug,
	S: Debug,
{
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		if size_of::<S>() == 0 {
			self.value.fmt(f)
		} else {
			f.debug_struct("Spanned")
				.field("value", &self.value)
				.field("span", &self.span)
				.finish()
		}
	}
}

#[cfg(feature = "serde")]
impl<T, Span> serde::Serialize for Spanned<T, Span>
where
	T: serde::Serialize,
{
	fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
	where
		S: serde::Serializer,
	{
		self.value.serialize(serializer)
	}
}

#[cfg(feature = "serde")]
impl<'de, T, S> serde::Deserialize<'de> for Spanned<T, S>
where
	T: serde::Deserialize<'de>,
	S: Default,
{
	fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
	where
		D: serde::Deserializer<'de>,
	{
		Ok(Self {
			value: T::deserialize(deserializer)?,
			span: S::default(),
		})
	}
}

impl<T, S> Deref for Spanned<T, S> {
	type Target = T;

	fn deref(&self) -> &Self::Target {
		&self.value
	}
}

impl<T, S> DerefMut for Spanned<T, S> {
	fn deref_mut(&mut self) -> &mut Self::Target {
		&mut self.value
	}
}

impl<T, S> IntoIterator for Spanned<T, S>
where
	T: IntoIterator,
{
	type Item = T::Item;
	type IntoIter = T::IntoIter;

	fn into_iter(self) -> Self::IntoIter {
		self.value.into_iter()
	}
}

/// Something that holds information about a span, which is simply a start and end index.
pub trait Span: 'static + Debug + Clone + Default + PartialEq + Eq {
	/// The syntax a span records: what its node was written with outside its children, like a
	/// heading's `# `. `()` for a span that records none.
	type Syntax: Syntax;

	fn new(start: usize, end: usize) -> Self;

	/// Widens this span to also cover `other`.
	fn merge(&mut self, other: &Self);

	/// Records `syntax` as written by this span's node.
	fn attach(&mut self, syntax: Self::Syntax);
}

impl Span for () {
	type Syntax = ();

	fn new(_start: usize, _end: usize) -> Self {}

	fn merge(&mut self, _other: &Self) {}

	fn attach(&mut self, _syntax: Self::Syntax) {}
}

/// Syntax tokens recorded while parsing, for [`Span::Syntax`].
pub trait Syntax: 'static + Debug + Clone + Default + PartialEq + Eq {
	/// One token of `kind` from `start` to `end`.
	fn token(kind: TokenKind, start: usize, end: usize) -> Self;

	fn append(&mut self, other: Self);

	#[must_use]
	fn join(mut self, other: Self) -> Self {
		self.append(other);
		self
	}
}

impl Syntax for () {
	fn token(_kind: TokenKind, _start: usize, _end: usize) -> Self {}

	fn append(&mut self, _other: Self) {}
}

/// A recorded syntax token.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SyntaxToken {
	pub kind: TokenKind,
	pub start: usize,
	pub end: usize,
}

impl Syntax for Vec<SyntaxToken> {
	fn token(kind: TokenKind, start: usize, end: usize) -> Self {
		vec![SyntaxToken { kind, start, end }]
	}

	fn append(&mut self, other: Self) {
		self.extend(other);
	}
}

/// Moves the syntax parsed alongside a value into its span.
pub fn attach<T, S: Span>(
	Spanned {
		value: (value, syntax),
		mut span,
	}: Spanned<(T, S::Syntax), S>,
) -> Spanned<T, S> {
	span.attach(syntax);
	Spanned { value, span }
}

/// A debug span containing information about the start and end of the value.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct TrackedSpan {
	pub start: usize,
	pub end: usize,
}

/// Offsets as `u32`s: a JavaScript binding makes a `BigInt` of any `u64`, and no text a host can
/// hold is longer than a `u32` counts.
#[cfg(feature = "serde")]
impl serde::Serialize for TrackedSpan {
	fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
	where
		S: serde::Serializer,
	{
		use serde::ser::{Error, SerializeStruct};

		let offset = |offset| u32::try_from(offset).map_err(S::Error::custom);
		let mut span = serializer.serialize_struct("TrackedSpan", 2)?;
		span.serialize_field("start", &offset(self.start)?)?;
		span.serialize_field("end", &offset(self.end)?)?;
		span.end()
	}
}

impl Span for TrackedSpan {
	type Syntax = ();

	fn new(start: usize, end: usize) -> Self {
		TrackedSpan { start, end }
	}

	fn merge(&mut self, other: &Self) {
		self.start = self.start.min(other.start);
		self.end = self.end.max(other.end);
	}

	fn attach(&mut self, _syntax: Self::Syntax) {}
}

/// A [`TrackedSpan`] that also records its node's syntax, for [`crate::parse_lossless`].
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct LosslessSpan {
	pub start: usize,
	pub end: usize,
	pub syntax: Vec<SyntaxToken>,
}

impl Span for LosslessSpan {
	type Syntax = Vec<SyntaxToken>;

	fn new(start: usize, end: usize) -> Self {
		LosslessSpan {
			start,
			end,
			syntax: Vec::new(),
		}
	}

	fn merge(&mut self, other: &Self) {
		self.start = self.start.min(other.start);
		self.end = self.end.max(other.end);
		self.syntax.extend(other.syntax.iter().cloned());
	}

	fn attach(&mut self, syntax: Self::Syntax) {
		self.syntax.extend(syntax);
	}
}

/// Records a parser's result on the current [`tracing::Span`], in its `ok` and `output` fields.
pub trait Trace: Sized {
	#[must_use]
	fn trace(self) -> Self;
}

impl<T: Debug, E> Trace for Result<T, E> {
	// Every parser result passes through here, so with tracing off it must not look up the
	// current span.
	fn trace(self) -> Self {
		if tracing::level_enabled!(tracing::Level::TRACE) {
			let span = tracing::Span::current();
			span.record("ok", self.is_ok());
			if let Ok(output) = &self {
				span.record("output", tracing::field::debug(output));
			}
		}
		self
	}
}
