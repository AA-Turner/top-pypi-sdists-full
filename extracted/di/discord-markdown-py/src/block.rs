use std::{fmt::Debug, marker::PhantomData};

use crate::{
	error::ParseError,
	span::{TraceOk, TraceParse},
};

pub use self::{heading::Heading, list::List, small::Small};

use nom::{
	branch::alt,
	character::complete::line_ending,
	combinator::{map, value},
	multi::many0,
	sequence::terminated,
	Parser,
};
use tracing::Level;

use super::{
	context::Context,
	grammar::Grammar,
	inline,
	node::{Node, SpannedNodes},
	span::{Span, WithSpan},
	Input,
};

/// Markdown headings.
///
/// For example:
///
/// ```md
/// # Hello world!
/// ```
pub mod heading;

/// Markdown lists.
///
/// For example:
///
/// ```md
/// - Hello world!
/// ```
pub mod list;

/// Markdown quotes.
///
/// For example:
///
/// ```md
/// > Hello world!
/// ```
pub mod quote;

/// Markdown small content.
///
/// For example
///
/// ```md
/// -# Hello world!
/// ```
pub mod small;

fn inline_block<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	let terminal = context.grammar.terminal_sequence();
	terminated(inline::inline(context), terminal)
}

struct BlockParser<S, E> {
	context: Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for BlockParser<S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("BlockParser")
			.field("context", &self.context)
			.field("span", &self.span)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for BlockParser<S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = SpannedNodes<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "block_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		many0(alt((
			value(Node::Empty, line_ending).span(),
			self.context.allowed_block_rules().span(),
			map(
				inline_block(self.context.clone().with_grammar(Grammar::InlineBlock)),
				Node::Paragraph,
			)
			.span(),
		)))
		.span()
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse block content.
///
/// # Errors
/// If parsing fails. Ideally this should not happen, since all content is block content.
#[must_use]
pub fn block<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	BlockParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}

// foo\n\nbar -> unstyled(text)

#[cfg(test)]
mod test {
	use std::fs::{read_dir, read_to_string};

	use nom::{Finish, Parser};
	use pretty_assertions::assert_eq;

	use crate::{
		heading, paragraph, spanned_vec,
		test_utils::handle_nom_err,
		{context::Context, node::SpannedNodes},
	};

	use super::block;

	#[test]
	fn simple_text() {
		let s = "foo";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![paragraph!("foo")]);
	}

	#[test]
	fn multi_line_text() {
		let s = "foo\nbar";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![paragraph!("foo"), paragraph!("bar")]);
	}

	#[test]
	fn heading_with_text() {
		let s = "# foo\nbar";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![heading!(1, "foo"), paragraph!("bar")]);
	}

	#[test]
	fn heading_with_nested_new_line() {
		let s = "# _foo\nbar_";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![heading!(1, "_foo"), paragraph!("bar_")]);
	}

	#[test]
	fn large_contents() {
		let contents_files = read_dir("test_content").unwrap();
		for entry in contents_files {
			let entry = entry.unwrap();

			let content_path = entry.path().join("content.md");
			let result_path = entry.path().join("result.json");

			let markdown = read_to_string(content_path).unwrap();
			let expected = read_to_string(result_path).unwrap();

			let (rem, res) = block::<(), _>(Context::default())
				.parse_complete((&*markdown).into())
				.finish()
				.map_err(handle_nom_err(&markdown))
				.expect("unable to parse");

			let expected: SpannedNodes<_> = serde_json::from_str(&expected)
				.unwrap_or_else(|err| panic!("error parsing {}: {}", entry.path().display(), err));

			assert_eq!(rem, "");
			assert_eq!(res, expected);
		}
	}

	#[test]
	fn no_content() {
		let s = "";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![]);
	}
}
