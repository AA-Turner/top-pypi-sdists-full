use nom::{
	Parser,
	branch::alt,
	bytes::complete::tag,
	character::complete::one_of,
	combinator::{opt, peek},
	sequence::preceded,
};

use crate::{
	Input,
	context::Context,
	error::ParseError,
	lossless::TokenKind,
	node::{Blocks, Elements},
	scope::Scope,
	span::{Span, WithToken},
	unparse::Unparse,
};

use super::block;

pub const LINE_PREFIX: char = '>';
pub const REST_PREFIX: &str = ">>>";

/// Unparse quote content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(content: &Blocks<S>, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	// Quotes need special handling - prefix each line with "> "
	let content_str = content.unparse().to_string();
	let lines: Vec<&str> = content_str.lines().collect();
	for (i, line) in lines.iter().enumerate() {
		if i > 0 {
			f.write_str("\n")?;
		}
		write!(f, "{LINE_PREFIX} {line}")?;
	}
	Ok(())
}

/// Parse a quote beginning with [`REST_PREFIX`], which quotes everything after it.
///
/// # Errors
/// If the data does not begin with such a quote.
#[must_use]
pub fn quote_rest<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	// As with `> `, exactly one space belongs to the prefix so that indentation on the first line
	// survives into the content.
	(
		(tag(REST_PREFIX), one_of(" \t")).token::<S>(TokenKind::QuotePrefix),
		block(context.with_scope(Scope::QuoteRest)),
	)
		.map(|(prefix, mut content): (_, Elements<'data, S>)| {
			content.span.attach(prefix);
			content
		})
}

/// Parse a quote whose every line begins with [`LINE_PREFIX`].
///
/// # Errors
/// If the data does not begin with such a quote.
#[must_use]
pub fn quote_line<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	// The prefix is peeked, not consumed: the block loop consumes it at the start of every line,
	// including the first. The trailing `opt` mops up a bare `>` on the final line, which the block
	// loop backtracks over because no block content follows it.
	preceded(
		peek(Scope::Quote.line_prefix()),
		(
			block(context.with_scope(Scope::Quote)),
			opt(Scope::Quote.line_prefix()).token::<S>(TokenKind::QuotePrefix),
		),
	)
	.map(|(mut content, prefix): (Elements<'data, S>, _)| {
		content.span.attach(prefix);
		content
	})
}

/// Parse a quote block.
///
/// A quote block is either a series of lines beginning with `>` or a region beginning with `>>>`.
///
/// # Errors
/// If the data does not begin with quote content.
#[must_use]
pub fn quote<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	alt((quote_line(context.clone()), quote_rest(context)))
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		bold, heading, italic, list, list_item, list_items, paragraph, spanned_vec,
		test_utils::{handle_nom_err, resolved_blocks},
		text, underline,
		{
			context::Context,
			node::{Block, Element},
		},
	};

	use super::quote;

	/// Parse `s` as a quote, asserting the whole input was consumed, and resolve it.
	fn parse_quote(s: &str) -> crate::node::Blocks<'_, ()> {
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining for {s:?}");
		resolved_blocks(res)
	}

	#[test]
	fn basic_quote() {
		let s = "> foo";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(resolved_blocks(res), spanned_vec!(paragraph!("foo")));
	}

	#[test]
	fn quote_with_new_line() {
		let s = "> foo\nbar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "bar");
		assert_eq!(resolved_blocks(res), spanned_vec!(paragraph!("foo")));
	}

	#[test]
	fn multi_line_quote() {
		let s = "> foo\n> bar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(paragraph!("foo"), paragraph!("bar"))
		);
	}

	#[test]
	fn multi_line_quote_with_empty() {
		let s = "> foo\n>\n> bar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(paragraph!("foo"), Block::Empty, paragraph!("bar"))
		);
	}

	#[test]
	fn quote_at_end() {
		let s = "> foo\n>";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(resolved_blocks(res), spanned_vec!(paragraph!("foo")));
	}

	#[test]
	fn quote_with_styling() {
		let s = "> **foo _bob_**\n> cat __a kitty cat__";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(
				paragraph!(bold!(text!("foo "), italic!("bob"))),
				paragraph!(text!("cat "), underline!("a kitty cat"))
			)
		);
	}

	/// `>` without a following space is not a quote at all, so the prefix must not match it. This
	/// distinguishes the prefix from the bare-`>`-on-an-empty-line case.
	#[test]
	fn prefix_requires_space_or_line_end() {
		let s = ">foo";
		let res = quote::<(), nom::error::Error<_>>(Context::default())
			.parse_complete(s.into())
			.finish();
		assert!(res.is_err(), "`>foo` should not parse as a quote: {res:?}");
	}

	/// A line that stops being quoted ends the quote and is left unconsumed, rather than being
	/// pulled in because the prefix was treated as optional.
	#[test]
	fn unquoted_line_ends_quote() {
		let s = "> foo\nbar\n> baz";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "bar\n> baz");
		assert_eq!(resolved_blocks(res), spanned_vec!(paragraph!("foo")));
	}

	/// Spans inside a quote index the original source. While quote bodies were joined into a new
	/// buffer, every offset after the first line drifted by the width of the stripped prefixes.
	#[test]
	fn spans_index_the_original_source() {
		use crate::span::TrackedSpan;

		let s = "> ab\n> cd";
		let (_, res) = quote::<TrackedSpan, _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		let spans = res
			.value
			.iter()
			.map(|node| (node.span.start, node.span.end))
			.collect::<Vec<_>>();
		assert_eq!(spans, vec![(2, 5), (7, 9)]);
		assert_eq!(&s[2..5], "ab\n");
		assert_eq!(&s[7..9], "cd");
	}

	/// The whole point of `>>>`: everything after it is quoted, including the lines that carry no
	/// prefix of their own. Where `>` ends at the first unprefixed line, this one runs to the end
	/// of the content.
	#[test]
	fn rest_prefix_quotes_the_rest_of_the_content() {
		let s = ">>> foo\nbar\nbaz";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(paragraph!("foo"), paragraph!("bar"), paragraph!("baz"))
		);
	}

	/// The space after `>>>` belongs to the prefix, exactly as it does for `> `, so it is not part
	/// of the quoted content.
	#[test]
	fn rest_prefix_consumes_its_space() {
		let s = ">>> foo";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(resolved_blocks(res), spanned_vec!(paragraph!("foo")));
	}

	/// `>>>` only opens a quote when a space follows it. A fourth `>` is not a space, and neither
	/// is a line ending, so none of these are quotes at all -- note that `>>>` also cannot fall
	/// back to the `>` prefix, whose own empty-line form would otherwise accept `>>>\n`.
	#[test]
	fn rest_prefix_requires_a_space() {
		for s in [">>>foo", ">>>> foo", ">>>\nfoo", ">>>"] {
			let res = quote::<(), nom::error::Error<_>>(Context::default())
				.parse_complete(s.into())
				.finish();
			assert!(res.is_err(), "{s:?} should not parse as a quote: {res:?}");
		}
	}

	/// Blank lines stay inside the quote rather than ending it, and produce the same `Element::Empty`
	/// a `>` quote does.
	#[test]
	fn rest_quote_keeps_empty_lines() {
		let s = ">>> foo\n\nbar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(paragraph!("foo"), Block::Empty, paragraph!("bar"))
		);
	}

	/// The content is block content, so block rules parse inside it -- including on the first line,
	/// which directly follows the prefix rather than a line ending.
	#[test]
	fn rest_quote_parses_block_rules() {
		let s = ">>> # foo\nbar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(heading!(1, "foo"), paragraph!("bar"))
		);
	}

	/// A heading eats the blank lines after it, prefixes included.
	#[test]
	fn heading_consumes_quoted_blank_lines() {
		let s = "> # foo\n>\n>   \n> bar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(heading!(1, "foo"), paragraph!("bar"))
		);
	}

	#[test]
	fn rest_quote_parses_inline_rules() {
		let s = ">>> **foo _bob_**\ncat __a kitty cat__";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(
				paragraph!(bold!(text!("foo "), italic!("bob"))),
				paragraph!(text!("cat "), underline!("a kitty cat"))
			)
		);
	}

	/// Quotes do not nest, in either direction: a `>` line inside a `>>>` quote is text, and so is
	/// a second `>>>`. The content is already quoted, so there is nothing for them to open.
	#[test]
	fn rest_quote_does_not_nest() {
		let s = ">>> foo\n> bar\n>>> baz";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(
				paragraph!("foo"),
				paragraph!("> bar"),
				paragraph!(">>> baz")
			)
		);
	}

	/// `>>>` inside a `>` quote is text for the same reason.
	#[test]
	fn rest_prefix_inside_a_line_quote_is_text() {
		let s = "> >>> foo";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(resolved_blocks(res), spanned_vec!(paragraph!(">>> foo")));
	}

	/// A block element that spans several quoted lines is one element, not one per line. The list
	/// parser consumes its own continuation lines, so it has to consume the `> ` on each of them --
	/// otherwise every line closes the list and the block loop opens a fresh one.
	#[test]
	fn quoted_list_is_one_list() {
		assert_eq!(
			parse_quote("> - foo\n> - bar"),
			spanned_vec!(list!(-[list_item!("foo"), list_item!("bar")]))
		);
	}

	/// The same applies to an ordered list, which takes the other branch of the item-type parser.
	#[test]
	fn quoted_ordered_list_is_one_list() {
		use crate::node::block::list::{List, Type};

		assert_eq!(
			parse_quote("> 1. foo\n> 2. bar"),
			spanned_vec!(Block::List(List {
				kind: Type::Ordered(1.try_into().unwrap()),
				items: list_items!(list_item!("foo"), list_item!("bar")),
			}))
		);
	}

	/// A continuation line belongs to the item above it, exactly as it would outside a quote.
	#[test]
	fn quoted_list_continuation_line() {
		assert_eq!(
			parse_quote("> - foo\n>   bar"),
			spanned_vec!(list!(-[list_item![paragraph!("foo"), paragraph!("bar")]]))
		);
	}

	/// Indentation inside a quote nests, which requires the prefix to claim only one space: a
	/// greedy one would eat the indent as well and flatten the child onto the parent's level.
	#[test]
	fn quoted_list_nests() {
		assert_eq!(
			parse_quote("> - foo\n>   - bar"),
			spanned_vec!(list!(-[list_item![
				paragraph!("foo"),
				list!(-[list_item!("bar")])
			]]))
		);
	}

	/// A blank quoted line splits the list in two, matching what `- foo\n\n- bar` does outside a
	/// quote. The prefix is consumed while looking for another item and given back when none is
	/// found, so the block loop still sees the line and turns it into `Element::Empty`.
	#[test]
	fn blank_quote_line_ends_quoted_list() {
		assert_eq!(
			parse_quote("> - foo\n>\n> - bar"),
			spanned_vec!(
				list!(-[list_item!("foo")]),
				Block::Empty,
				list!(-[list_item!("bar")])
			)
		);
	}

	/// An unquoted line still ends the quote rather than being pulled into the list: looking for
	/// the prefix must not make it optional.
	#[test]
	fn unquoted_line_ends_quoted_list() {
		let s = "> - foo\n- bar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "- bar");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(list!(-[list_item!("foo")]))
		);
	}

	/// The prefix is `>` plus a single space; anything past that is content. Consuming the run
	/// greedily is what kept [`quoted_list_nests`] from working.
	#[test]
	fn prefix_consumes_exactly_one_space() {
		assert_eq!(parse_quote(">  foo"), spanned_vec!(paragraph!(" foo")));
	}

	/// Spans of a list spanning quoted lines index the original source, as they do for paragraphs.
	#[test]
	fn quoted_list_spans_index_the_original_source() {
		use crate::span::TrackedSpan;

		let s = "> - ab\n> - cd";
		let (rem, res) = quote::<TrackedSpan, _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");

		let Element::List(list) = &res.value[0].value else {
			panic!("expected a list, got {res:?}");
		};
		let spans = list
			.items
			.iter()
			.flat_map(|item| item.content.iter())
			.map(|node| (node.span.start, node.span.end))
			.collect::<Vec<_>>();
		assert_eq!(spans, vec![(4, 7), (11, 13)]);
		assert_eq!(&s[4..7], "ab\n");
		assert_eq!(&s[11..13], "cd");
	}

	/// As with a `>` quote, spans inside a `>>>` quote index the original source: the prefix is
	/// consumed, not stripped into a new buffer, so every offset after it stays put.
	#[test]
	fn rest_quote_spans_index_the_original_source() {
		use crate::span::TrackedSpan;

		let s = ">>> ab\ncd";
		let (_, res) = quote::<TrackedSpan, _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		let spans = res
			.value
			.iter()
			.map(|node| (node.span.start, node.span.end))
			.collect::<Vec<_>>();
		assert_eq!(spans, vec![(4, 7), (7, 9)]);
		assert_eq!(&s[4..7], "ab\n");
		assert_eq!(&s[7..9], "cd");
	}

	/// `>>>` is a block rule, so it opens a quote at the start of the content or of a line, and is
	/// text anywhere else.
	#[test]
	fn rest_prefix_only_opens_a_quote_at_a_line_start() {
		use crate::node::block::block;

		let s = "x >>> y\n>>> z";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(
				paragraph!("x >>> y"),
				Block::Quote(spanned_vec!(paragraph!("z")))
			)
		);
	}

	/// A `>>>` line ends the `>` quote above it and opens its own, rather than being pulled in as
	/// another line of the first.
	#[test]
	fn rest_quote_after_a_line_quote_is_its_own_quote() {
		use crate::node::block::block;

		let s = "> foo\n>>> bar";
		let (rem, res) = block::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_blocks(res),
			spanned_vec!(
				Block::Quote(spanned_vec!(paragraph!("foo"))),
				Block::Quote(spanned_vec!(paragraph!("bar")))
			)
		);
	}

	/// Each quote syntax is enabled on its own: disabling one leaves it as text, and the other
	/// still parses.
	#[test]
	fn quote_syntaxes_are_independent() {
		use crate::{
			context::Options,
			parse,
			syntax::{Syntax, SyntaxSet},
		};

		let without = |syntax| Options {
			syntaxes: SyntaxSet::all() - syntax,
			..Options::default()
		};

		let s = ">>> foo";
		let res = parse::<(), _>(s, without(Syntax::MultilineQuote))
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec!(paragraph!(">>> foo")));
		let res = parse::<(), _>(s, without(Syntax::Quote))
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec!(Block::Quote(spanned_vec!(paragraph!("foo"))))
		);

		let s = "> foo";
		let res = parse::<(), _>(s, without(Syntax::Quote))
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec!(paragraph!("> foo")));
	}
}
