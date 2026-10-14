use std::{fmt::Debug, marker::PhantomData};

use crate::{
	context::fuel::ApplyFuel,
	error::ParseError,
	node::{Element, ParsedNode, ParsedNodes, SpannedParsedNode},
	range::delim,
	span::{TraceOk, TraceParse},
};

pub use self::{heading::Heading, list::List, small::Small};

use nom::{
	Parser,
	branch::alt,
	character::complete::line_ending,
	combinator::{eof, map, value},
	multi::many0,
	sequence::{preceded, terminated},
};
use tracing::Level;

use super::{
	Input,
	context::Context,
	grammar::Grammar,
	inline,
	span::{Span, WithSpan},
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
) -> impl Parser<Input<'data>, Output = ParsedNodes<'data, S>, Error = E>
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
	type Output = ParsedNodes<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "block_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let allowed = self.context.allowed_rules;
		let single = |piece| (None, piece);

		// A line is one node, or a delimiter run opening before a block rule, as in `*1. foo`.
		let line = alt((
			value(ParsedNode::Element(Element::Empty), line_ending)
				.span()
				.map(single),
			self.context
				.allowed_block_rules()
				.map(ParsedNode::Element)
				.span()
				.map(single),
			(
				delim::opener(allowed, |start| self.context.is_disabled_opener(start))
					.map(ParsedNode::Delim)
					.span(),
				self.context
					.allowed_block_rules()
					.map(ParsedNode::Element)
					.span(),
			)
				.map(|(delim, block)| (Some(delim), block)),
			// a line of nothing but delimiters, like the `||` around a spoiled list
			terminated(delim::delim(allowed), alt((line_ending, eof)))
				.map(|delim| {
					ParsedNode::Delim(delim::Delim {
						alone: true,
						..delim
					})
				})
				.span()
				.map(single),
			map(
				inline_block(self.context.clone().with_grammar(Grammar::InlineBlock)),
				|content| ParsedNode::Element(Element::Paragraph(content)),
			)
			.span()
			.map(single),
		))
		.apply_fuel(self.context.remaining_fuel());

		// Each iteration begins at the start of a line, so the enclosing container's line prefix
		// (e.g. `> ` inside a quote) is consumed here. It matches empty when there is no container,
		// and failing it is what ends the container when a line stops being part of it.
		many0(preceded(self.context.line_prefix(), line))
			.map(
				|lines: Vec<(
					Option<SpannedParsedNode<'data, S>>,
					SpannedParsedNode<'data, S>,
				)>| {
					lines
						.into_iter()
						.flat_map(|(delim, node)| delim.into_iter().chain([node]))
						.collect::<Vec<_>>()
				},
			)
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
) -> impl Parser<Input<'data>, Output = ParsedNodes<'data, S>, Error = E>
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
		heading, italic, paragraph,
		range::Content,
		spanned_vec,
		test_utils::{handle_nom_err, parsed, resolved},
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
		assert_eq!(
			resolved(res, Content::Blocks),
			spanned_vec![paragraph!("foo")]
		);
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
		assert_eq!(
			resolved(res, Content::Blocks),
			spanned_vec![paragraph!("foo"), paragraph!("bar")]
		);
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
		assert_eq!(
			resolved(res, Content::Blocks),
			spanned_vec![heading!(1, "foo"), paragraph!("bar")]
		);
	}

	#[test]
	/// A modifier reaches across the end of a heading into the next line.
	fn heading_with_nested_new_line() {
		assert_eq!(
			parsed("# _foo\nbar_"),
			spanned_vec![italic!(heading!(1, "foo"), paragraph!("bar"))]
		);
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

			let expected: SpannedNodes<_> = serde_json::from_str(&expected)
				.unwrap_or_else(|err| panic!("error parsing {}: {}", entry.path().display(), err));

			assert_eq!(parsed(&markdown), expected);
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
