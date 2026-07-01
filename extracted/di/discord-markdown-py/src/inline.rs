use std::borrow::Cow;
use std::fmt::Debug;
use std::marker::PhantomData;
use std::sync::atomic::Ordering;

use nom::branch::alt;
use nom::character::complete::{anychar, line_ending};
use nom::combinator::map;
use nom::error::ErrorKind;
use nom::multi::many1;
use nom::sequence::preceded;
use nom::Parser;
use tracing::Level;

use crate::context::TerminalOutput;
use crate::error::{Cancelled, ParseError};
use crate::span::{TraceOk, TraceParse};

use super::context::Context;
use super::grammar::Grammar;
use super::node::{flatten_owned, Node, SpannedNodes};
use super::span::{Span, WithSpan};
use super::Input;

pub use {
	bold::bold, code::code, code_block::code_block, italic::italic, link::link, mention::mention,
	spoiler::spoiler, strikethrough::strikethrough, text::text, timestamp::timestamp,
	underline::underline,
};

/// Bold parsing.
pub mod bold;
/// Inline code parsing.
pub mod code;
/// Code block parsing.
pub mod code_block;
/// Emoji parsing.
pub mod emoji;
/// Italic parsing.
pub mod italic;
/// Link parsing.
pub mod link;
/// Mention parsing.
pub mod mention;
/// Spoiler parsing.
pub mod spoiler;
/// Strikethrough parsing.
pub mod strikethrough;
/// Text parsing.
pub mod text;
/// Timestamp parsing.
pub mod timestamp;
/// Underline parsing.
pub mod underline;

struct InlineParser<S, E> {
	context: Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Clone for InlineParser<S, E> {
	fn clone(&self) -> Self {
		Self {
			context: self.context.clone(),
			span: PhantomData,
			error: PhantomData,
		}
	}
}

impl<S, E> Debug for InlineParser<S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("InlineParser")
			.field("context", &self.context)
			.field("span", &self.span)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for InlineParser<S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = SpannedNodes<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "inline_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		if self.context.cancelled.load(Ordering::Relaxed) {
			return Err(nom::Err::Failure(E::from_external_error(
				input,
				ErrorKind::Fail,
				Cancelled,
			)));
		}

		let ctx = self.context.with_hints(&input);

		let result = many1(alt((
			ctx.matched_pairs()
				// TODO: this should respect the inner content by outputting a Node (or list of Nodes) rather than Input
				.map(|seq| Node::<S>::Text(seq.content))
				.span(),
			ctx.guard_terminal_sequence(|| {
				alt((
					ctx.allowed_inline_rules(),
					preceded(line_ending, ctx.allowed_block_rules()),
					text::text(ctx.clone()).map(|content| Node::Text(Cow::Owned(content))),
					// If we failed to capture the current character after stepping through all rules
					// then we are likely dealing with an unpaired control character, so consume it
					// and allow the rules to continue.
					map(anychar, |ch: char| Node::Text(ch.to_string().into())),
				))
			})
			.map(|seq| match seq {
				TerminalOutput::Override(seq) => Node::Text(seq.content),
				TerminalOutput::Normal(node) => node,
			})
			.span(),
		)))
		.map(flatten_owned)
		.span()
		.trace_parse()
		.process::<OM>(input)
		.trace_ok();

		result
	}
}

/// Parse inline content.
///
/// # Errors
/// If parsing fails. Ideally this should never happen, since all content is inline content.
#[must_use]
pub fn inline<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	InlineParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		bold, code, code_block, emoji, italic, link, spanned_vec, spoiler,
		test_utils::handle_nom_err,
		text,
		{
			context::Context,
			inline::{mention::Mention, timestamp::Timestamp},
			node::Node,
		},
	};

	use super::inline;

	#[test]
	fn compound_test() {
		let s = r"_foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![italic!(
				text!("foo t_a "),
				bold!("bat"),
				text!(" "),
				emoji!(id = 1234, name = "abcd", animated),
				Node::Timestamp(Timestamp {
					value: 1234,
					style: None,
				}),
				Node::Mention(Mention::User(1234)),
				text!(" butt")
			)]
		);
	}

	#[test]
	fn link_detection() {
		let s = "foo https://wnelson.dev bar";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![text!("foo "), link!("https://wnelson.dev"), text!(" bar"),]
		);
	}

	#[test]
	fn masked_links() {
		let s = "foo [bar](https://wnelson.dev) baz";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![
				text!("foo "),
				link!("https://wnelson.dev", [text!("bar")]),
				text!(" baz"),
			]
		);
	}

	#[test]
	fn multi_line_end() {
		let s = "foo\nbar";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo\nbar")]);
	}

	#[test]
	fn simple_code() {
		let s = "`foo`";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![code!("foo")]);
	}

	#[test]
	fn complex_code() {
		let s = "foo `ba**r**`";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo "), code!("ba**r**")]);
	}

	#[test]
	fn simple_codeblock() {
		let s = "```\nfoo```";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![code_block!("foo")]);
	}

	#[test]
	fn complex_codeblock() {
		let s = "foo **bar**```baz\n_bar_``` _butt_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![
				text!("foo "),
				bold!("bar"),
				code_block!(language = "baz", "_bar_"),
				text!(" "),
				italic!("butt")
			]
		);
	}

	#[test]
	fn text_with_emoji() {
		let s = "foo 🦶";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo "), emoji!("🦶"),]);
	}

	#[test]
	fn text_with_colon_delimited_emoji() {
		let s = "foo :foot:";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo "), emoji!("🦶"),]);
	}

	#[test]
	fn text_with_spoiler() {
		let s = "foo ||bar|| baz";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![text!("foo "), spoiler!("bar"), text!(" baz")]
		);
	}

	// TODO | We need to capture the fact that the <...> was present in the generated AST. Right now we just lose that info.
	// TODO |  It is important for preventing link embedding on the backend.
	#[test]
	fn text_with_autolink() {
		let s = "foo <https://wnelson.dev> bar";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![text!("foo "), link!("https://wnelson.dev"), text!(" bar")]
		);
	}

	#[test]
	fn text_with_nested_rules() {
		let s = "**foo __bar **baz** foo__ bar**";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![bold!("foo __bar "), text!("baz"), bold!(" foo__ bar")]
		);
	}
}
