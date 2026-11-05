//! Blocks: the [`Block`] nodes of the finished tree, and the parsers for block markdown content.

use derive_where::derive_where;

use crate::{
	Input,
	context::Context,
	error::PResult,
	lossless::TokenKind,
	range::delim,
	scope::Scope,
	span::{Span, Syntax, Trace},
};

pub use self::{heading::Heading, list::List, small::Small};

use tracing::Level;

use super::{Blocks, Element, Elements, Inline, Inlines, SpannedElement, inline};

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

/// Parse a line of inline content, ending at `context`'s terminal sequence.
fn inline_block<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<Elements<'data, S>> {
	let mut line = inline::inline::<S>(input, context)?;
	let line_ending = input.token::<S, _>(TokenKind::LineEnding, |input| {
		context.scope.terminal_sequence(input)
	})?;
	line.span.attach(line_ending);
	Ok(line)
}

/// Parse a line of block content: one node, or a delimiter run opening before a block rule, as in
/// `*1. foo`.
fn line<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<(Option<SpannedElement<'data, S>>, SpannedElement<'data, S>)> {
	let allowed = context.syntaxes;

	if let Some(empty) = input.attempt(|input| {
		input.spanned_with_syntax(|input| {
			let line_ending = input.token::<S, _>(TokenKind::LineEnding, Input::line_ending)?;
			Ok((Element::Empty, line_ending))
		})
	})? {
		return Ok((None, empty));
	}

	if let Some(block) = input
		.attempt(|input| input.spanned_with_syntax(|input| context.allowed_block_syntax(input)))?
	{
		return Ok((None, block));
	}

	if let Some(opened) = input.attempt(|input| {
		let delim = input.spanned(|input| {
			delim::opener(input, allowed, |start| context.is_disabled_opener(start))
				.map(Element::Delim)
		})?;
		let block = input.spanned_with_syntax(|input| context.allowed_block_syntax(input))?;
		Ok((Some(delim), block))
	})? {
		return Ok(opened);
	}

	// a line of nothing but delimiters, like the `||` around a spoiled list
	if let Some(alone) = input.attempt(|input| {
		input.spanned_with_syntax(|input| {
			let delim = delim::delim(input, allowed)?;
			let line_ending =
				input.token::<S, _>(TokenKind::LineEnding, Input::line_ending_or_eof)?;
			let delim = Element::Delim(delim::Delim {
				alone: true,
				..delim
			});
			Ok((delim, line_ending))
		})
	})? {
		return Ok((None, alone));
	}

	let context = context.clone().with_scope(Scope::InlineBlock);
	let paragraph = input.spanned(|input| inline_block(input, &context).map(Element::Paragraph))?;
	Ok((None, paragraph))
}

/// Parse block content.
///
/// # Errors
/// If the parse runs out of fuel. Any other failure would be a bug, since all content is block
/// content.
#[tracing::instrument(name = "block_parser", level = Level::TRACE, skip_all, fields(ok, output))]
pub fn block<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<Elements<'data, S>> {
	input
		.spanned_with_syntax(|input| {
			let mut nodes = Vec::new();
			let mut syntax = S::Syntax::default();

			// Each iteration begins at the start of a line, so the enclosing container's line
			// prefix (e.g. `> ` inside a quote) is consumed here. It matches empty when there is no
			// container, and failing it is what ends the container when a line stops being part
			// of it.
			while let Some((prefix, (delim, node))) = input.attempt(|input| {
				let prefix = input
					.token::<S, _>(TokenKind::QuotePrefix, |input| context.line_prefix(input))?;
				context.remaining_fuel().spend()?;
				Ok((prefix, line(input, context)?))
			})? {
				syntax.append(prefix);
				nodes.extend(delim);
				nodes.push(node);
			}

			Ok((nodes, syntax))
		})
		.trace()
}

// foo\n\nbar -> unstyled(text)

#[cfg(test)]
mod test {
	use std::fs::{read_dir, read_to_string};

	use pretty_assertions::assert_eq;

	use crate::{
		heading, italic, paragraph, spanned_vec,
		test_utils::{parsed, resolved_blocks, run},
		{context::Context, node::Blocks},
	};

	use super::block;

	#[test]
	fn simple_text() {
		let s = "foo";
		let (rem, res) =
			run(s, |input| block::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_blocks(res), spanned_vec![paragraph!("foo")]);
	}

	#[test]
	fn multi_line_text() {
		let s = "foo\nbar";
		let (rem, res) =
			run(s, |input| block::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec![paragraph!("foo"), paragraph!("bar")]
		);
	}

	#[test]
	fn heading_with_text() {
		let s = "# foo\nbar";
		let (rem, res) =
			run(s, |input| block::<()>(input, &Context::default())).expect("unable to parse");

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
		let (rem, res) =
			run(s, |input| block::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![]);
	}
}
