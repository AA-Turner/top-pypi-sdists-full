use std::{
	fmt::Debug,
	marker::PhantomData,
	ops::{Deref, DerefMut},
};

use nom::{Mode, Parser, error::ParseError};

use crate::{lossless::TokenKind, unparse::Unparse};

use super::Input;

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

impl<T, S> Unparse for Spanned<T, S>
where
	T: Unparse,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		self.value.fmt(f)
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

/// Parser that can have spans applied to its output.
pub trait WithSpan<'data> {
	type Output;
	type Error;

	#[must_use]
	fn span<S: Span>(
		self,
	) -> impl Parser<Input<'data>, Output = Spanned<Self::Output, S>, Error = Self::Error>;
}

impl<'data, T> WithSpan<'data> for T
where
	T: Parser<Input<'data>>,
	T::Error: ParseError<Input<'data>>,
{
	type Output = T::Output;
	type Error = T::Error;

	fn span<S: Span>(
		self,
	) -> impl Parser<Input<'data>, Output = Spanned<Self::Output, S>, Error = Self::Error> {
		Spanner {
			parser: self,
			location: PhantomData,
		}
	}
}

struct Spanner<'data, P, S> {
	parser: P,
	location: PhantomData<&'data S>,
}

impl<'data, S, P> Parser<Input<'data>> for Spanner<'data, P, S>
where
	S: Span,
	P: Parser<Input<'data>>,
	P::Error: ParseError<Input<'data>>,
{
	type Output = Spanned<P::Output, S>;
	type Error = P::Error;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let start = input.start;
		let res = self.parser.process::<OM>(input);

		match res {
			Ok((remaining, output)) => {
				let output = OM::Output::map(output, |output| Spanned {
					value: output,
					span: remaining.span(start),
				});

				Ok((remaining, output))
			}
			Err(err) => Err(err),
		}
	}
}

/// Parser whose input is recorded as a syntax token: see [`Span::Syntax`].
pub trait WithToken<'data>: Parser<Input<'data>> + Sized {
	/// Records what this parser consumed as a token of `kind`, alongside its output. Consuming
	/// nothing records nothing.
	fn with_token<S: Span>(
		self,
		kind: TokenKind,
	) -> impl Parser<Input<'data>, Output = (Self::Output, S::Syntax), Error = Self::Error> {
		Tokenizer {
			parser: self,
			kind,
			span: PhantomData::<&'data S>,
		}
	}

	/// As [`Self::with_token`], for a parser whose output is only syntax.
	fn token<S: Span>(
		self,
		kind: TokenKind,
	) -> impl Parser<Input<'data>, Output = S::Syntax, Error = Self::Error> {
		self.with_token::<S>(kind).map(|(_, syntax)| syntax)
	}
}

impl<'data, P> WithToken<'data> for P where P: Parser<Input<'data>> {}

struct Tokenizer<'data, P, S> {
	parser: P,
	kind: TokenKind,
	span: PhantomData<&'data S>,
}

impl<'data, S, P> Parser<Input<'data>> for Tokenizer<'data, P, S>
where
	S: Span,
	P: Parser<Input<'data>>,
{
	type Output = (P::Output, S::Syntax);
	type Error = P::Error;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let start = input.start;
		let (remaining, output) = self.parser.process::<OM>(input)?;
		let end = remaining.start;
		let kind = self.kind;
		let output = OM::Output::map(output, |output| {
			let syntax = if end > start {
				S::Syntax::token(kind, start, end)
			} else {
				S::Syntax::default()
			};
			(output, syntax)
		});
		Ok((remaining, output))
	}
}

/// Add a field `ok` to the current [`tracing::Span`], which records whether the result is [`Ok`].
pub trait TraceOk: Sized {
	#[must_use]
	fn trace_ok(self) -> Self;
}

impl<T, E> TraceOk for Result<T, E> {
	fn trace_ok(self) -> Self {
		tracing::Span::current().record("ok", self.is_ok());
		self
	}
}

/// Adds a field `output` to the current [`tracing::Span`], which records the output of the parser.
pub trait TraceParse<'data, P>
where
	P: Parser<Input<'data>>,
{
	fn trace_parse(self) -> impl Parser<Input<'data>, Output = P::Output, Error = P::Error>;
}

impl<'data, P> TraceParse<'data, P> for P
where
	P: Parser<Input<'data>>,
	P::Output: Debug,
{
	fn trace_parse(self) -> impl Parser<Input<'data>, Output = P::Output, Error = P::Error> {
		self.map(|res| {
			tracing::Span::current().record("output", tracing::field::debug(&res));
			res
		})
	}
}
