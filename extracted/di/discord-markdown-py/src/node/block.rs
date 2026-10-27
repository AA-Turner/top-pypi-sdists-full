//! Blocks: the [`Block`] nodes of the finished tree, and the parsers for block markdown content.

use std::{fmt::Debug, marker::PhantomData};

use derive_where::derive_where;

use crate::{
	Input,
	context::{Context, fuel::ApplyFuel},
	error::ParseError,
	lossless::TokenKind,
	range::delim,
	scope::Scope,
	span::{Span, Syntax, TraceOk, TraceParse, WithSpan, WithToken, attach},
	unparse::Unparse,
};

pub use self::{heading::Heading, list::List, small::Small};

use nom::{
	Parser,
	branch::alt,
	character::complete::line_ending,
	combinator::{eof, map},
	multi::fold_many0,
};
use tracing::Level;

use super::{Blocks, Element, Elements, Inline, Inlines, inline};

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

/// A block of the finished tree. Its inline content is in [`Inline`]s, so no modifier can hold a
/// block: one covering several blocks is split into a fragment inside each.
#[derive_where(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case", bound = "")
)]
pub enum Block<'data, S: Span> {
	Heading(Heading<S, Inline<'data, S>>),
	List(List<S, Block<'data, S>>),
	Paragraph(Inlines<'data, S>),
	Quote(Blocks<'data, S>),
	Small(Small<S, Inline<'data, S>>),
	/// New line.
	Empty,
}

impl<'data, S: Span> Block<'data, S> {
	/// The blocks this block holds directly: those of a quote or of each list item.
	pub fn blocks(&self) -> impl Iterator<Item = &Block<'data, S>> {
		let (content, items) = match self {
			Self::Quote(content) => (Some(content), &[][..]),
			Self::List(List { items, .. }) => (None, items.value.as_slice()),
			_ => (None, &[][..]),
		};
		content
			.into_iter()
			.chain(items.iter().map(|item| &item.content))
			.flat_map(|content| content.iter().map(|block| &block.value))
	}

	/// The inline content this block holds directly: that of a paragraph, heading or small.
	pub fn inlines(&self) -> impl Iterator<Item = &Inline<'data, S>> {
		let content = match self {
			Self::Paragraph(content)
			| Self::Heading(Heading { content, .. })
			| Self::Small(Small { content }) => Some(content),
			_ => None,
		};
		content
			.into_iter()
			.flat_map(|content| content.iter().map(|inline| &inline.value))
	}

	/// Text content of this block and everything in it.
	#[must_use]
	pub fn content(&self) -> String {
		let mut content: String = self.blocks().map(Block::content).collect();
		content.extend(self.inlines().map(Inline::content));
		content
	}
}

impl<S: Span> Unparse for Block<'_, S> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self::Heading(heading) => Unparse::fmt(heading, f),
			Self::List(list) => Unparse::fmt(list, f),
			Self::Paragraph(content) => Unparse::fmt(content, f),
			Self::Quote(content) => quote::unparse(content, f),
			Self::Small(small) => small::unparse(&small.content, f),
			Self::Empty => f.write_str("\n"),
		}
	}
}

fn inline_block<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	let terminal = context.scope.terminal_sequence();
	(
		inline::inline(context),
		terminal.token::<S>(TokenKind::LineEnding),
	)
		.map(|(mut content, line_ending): (Elements<'data, S>, _)| {
			content.span.attach(line_ending);
			content
		})
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
	type Output = Elements<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "block_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let allowed = self.context.syntaxes;
		let single = |piece| (None, piece);

		// A line is one node, or a delimiter run opening before a block rule, as in `*1. foo`.
		let line = alt((
			line_ending
				.token::<S>(TokenKind::LineEnding)
				.map(|line_ending| (Element::Empty, line_ending))
				.span()
				.map(attach)
				.map(single),
			self.context
				.allowed_block_syntax()
				.span()
				.map(attach)
				.map(single),
			(
				delim::opener(allowed, |start| self.context.is_disabled_opener(start))
					.map(Element::Delim)
					.span(),
				self.context.allowed_block_syntax().span().map(attach),
			)
				.map(|(delim, block)| (Some(delim), block)),
			// a line of nothing but delimiters, like the `||` around a spoiled list
			(
				delim::delim(allowed),
				alt((line_ending, eof)).token::<S>(TokenKind::LineEnding),
			)
				.map(|(delim, line_ending)| {
					let delim = Element::Delim(delim::Delim {
						alone: true,
						..delim
					});
					(delim, line_ending)
				})
				.span()
				.map(attach)
				.map(single),
			map(
				inline_block(self.context.clone().with_scope(Scope::InlineBlock)),
				Element::Paragraph,
			)
			.span()
			.map(single),
		))
		.apply_fuel(self.context.remaining_fuel());

		// Each iteration begins at the start of a line, so the enclosing container's line prefix
		// (e.g. `> ` inside a quote) is consumed here. It matches empty when there is no container,
		// and failing it is what ends the container when a line stops being part of it.
		fold_many0(
			(
				self.context
					.line_prefix()
					.token::<S>(TokenKind::QuotePrefix),
				line,
			),
			|| (Vec::new(), S::Syntax::default()),
			|(mut nodes, mut syntax), (prefix, (delim, node))| {
				syntax.append(prefix);
				nodes.extend(delim);
				nodes.push(node);
				(nodes, syntax)
			},
		)
		.span()
		.map(attach)
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
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
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
		heading, italic, paragraph, spanned_vec,
		test_utils::{handle_nom_err, parsed, resolved_blocks},
		{context::Context, node::Blocks},
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
		assert_eq!(resolved_blocks(res), spanned_vec![paragraph!("foo")]);
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
			resolved_blocks(res),
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
			resolved_blocks(res),
			spanned_vec![heading!(1, "foo"), paragraph!("bar")]
		);
	}

	#[test]
	fn heading_with_blank_lines() {
		assert_eq!(
			parsed("# foo\n\n   \nbar"),
			spanned_vec![heading!(1, "foo"), paragraph!("bar")]
		);
	}

	#[test]
	/// A modifier reaches across the end of a heading into the next line.
	fn heading_with_nested_new_line() {
		assert_eq!(
			parsed("# _foo\nbar_"),
			spanned_vec![heading!(1, [italic!("foo")]), paragraph!(italic!("bar"))]
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

			let expected: Blocks<_> = serde_json::from_str(&expected)
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
