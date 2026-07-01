use std::{
	fmt::Debug,
	marker::PhantomData,
	ops::{Deref, DerefMut},
};

use nom::{error::ParseError, Mode, Parser};

use crate::unparse::Unparse;

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

pub trait Span: 'static + Debug + Clone + Default {
	fn new(start: usize, end: usize) -> Self;
}

impl Span for () {
	fn new(_start: usize, _end: usize) -> Self {}
}

/// A debug span containing information about the start and end of the value.
#[derive(Debug, Clone, Default)]
pub struct TrackedSpan {
	pub start: usize,
	pub end: usize,
}

impl Span for TrackedSpan {
	fn new(start: usize, end: usize) -> Self {
		TrackedSpan { start, end }
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
