use std::borrow::Cow;
use std::fmt::Debug;
use std::marker::PhantomData;

use nom::Parser;
use nom::branch::alt;
use nom::character::complete::{anychar, line_ending};
use nom::combinator::map;
use nom::error::ErrorKind;
use nom::multi::many1;
use nom::sequence::preceded;
use tracing::Level;

use crate::context::TerminalOutput;
use crate::error::{OutOfFuel, ParseError};
use crate::span::{TraceOk, TraceParse};

use super::Input;
use super::context::Context;
use super::grammar::Grammar;
use super::node::{Node, SpannedNodes, flatten_owned};
use super::span::{Span, WithSpan};

pub use {
	bold::bold, code::code, code_block::code_block, italic::italic, link::link, mention::mention,
	spoiler::spoiler, strikethrough::strikethrough, text::text, timestamp::timestamp,
	underline::underline,
};

pub mod bold;
pub mod code;
pub mod code_block;
pub mod emoji;
pub mod italic;
pub mod link;
pub mod mention;
pub mod spoiler;
pub mod strikethrough;
pub mod text;
pub mod timestamp;
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
		// Every inline parse costs a unit of fuel, including the ones an enclosing rule goes on to
		// abandon. Running dry is a `Failure` rather than an `Error` so that it aborts the parse
		// instead of being swallowed by the surrounding `alt`, which would just retry against an
		// empty tank. `OutOfFuel` travels as an external error, so an error type that cares can
		// keep it (see `crate::error::Error`); the `ErrorKind` is only what nom's signature
		// demands, and carries no meaning here.
		if !self.context.consume_fuel() {
			return Err(nom::Err::Failure(E::from_external_error(
				input,
				ErrorKind::Fail,
				OutOfFuel,
			)));
		}

		let ctx = self.context.with_hints(&input);

		many1(alt((
			ctx.matched_pairs()
				// TODO: this should respect the inner content by outputting a Node (or list of Nodes) rather than Input
				.map(|seq| Node::<S>::Text(seq.content.into()))
				.span(),
			ctx.guard_terminal_sequence(|| {
				alt((
					ctx.allowed_inline_rules(),
					preceded((line_ending, ctx.line_prefix()), ctx.allowed_block_rules()),
					text::text(ctx.clone()).map(|content| Node::Text(Cow::Owned(content))),
					// If we failed to capture the current character after stepping through all rules
					// then we are likely dealing with an unpaired control character, so consume it
					// and allow the rules to continue.
					map(anychar, |ch: char| Node::Text(ch.to_string().into())),
				))
			})
			.map(|seq| match seq {
				TerminalOutput::Override(seq) => Node::Text(seq.content.into()),
				TerminalOutput::Normal(node) => node,
			})
			.span(),
		)))
		.map(flatten_owned)
		.span()
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse inline content.
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
		text, underline,
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

	/// An underscore glued to a word on both sides is part of that word, not a delimiter, so it
	/// must not open an italic -- otherwise the *opening* `_` of a later, real italic gets consumed
	/// as its closer and everything between the two is wrongly emphasised.
	#[test]
	fn intraword_underscore_does_not_open_italic() {
		let s = "the discord_admin codebase and _really_ don't";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![
				text!("the discord_admin codebase and "),
				italic!("really"),
				text!(" don't")
			]
		);
	}

	/// As [`intraword_underscore_does_not_open_italic`], for an underscore followed by `(` rather
	/// than by another alphanumeric.
	#[test]
	fn intraword_underscore_paren_does_not_open_italic() {
		let s = "Endemic_(epidemiology) and _really_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![text!("Endemic_(epidemiology) and "), italic!("really")]
		);
	}

	/// A consequence of the rule above: the underscore that would have opened the italic never
	/// gets the chance, so the trailing one has nothing to close and stays literal.
	#[test]
	fn trailing_underscore_after_word_is_literal() {
		let s = "foo_bar baz_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo_bar baz_")]);
	}

	/// The override is anchored on a *preceding* alphanumeric, so an underscore that starts a word
	/// still opens an italic -- including the `_(` case, which the terminal-side override treats
	/// unconditionally.
	#[test]
	fn leading_underscore_still_opens_italic() {
		let s = "_(foo)_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![italic!("(foo)")]);
	}

	/// A bold nested in an asterisk italic survives in every container, because they all descend
	/// through the same terminal guard.
	#[test]
	fn nested_bold_survives_in_any_container() {
		for s in [
			"*foo **bar** baz*",
			"> *foo **bar** baz*",
			"# *foo **bar** baz*",
		] {
			let res = crate::parse::<(), _>(s, crate::context::Options::default())
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert!(
				res.iter()
					.any(|node| node.iter().any(|node| matches!(node, Node::Bold(_)))),
				"expected a nested bold for {s:?}, got {res:?}"
			);
		}
	}

	/// Three underscores are an ambiguous run, so the overlapping-rule probe stays out of it and
	/// the rules resolve it in declaration order -- `Italic` precedes `Underline`, so the italic is
	/// the outer node. Both orders render the same, but pin it so the choice is deliberate.
	#[test]
	fn a_triple_underscore_run_nests_italic_outside_underline() {
		let s = "___foo___";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![italic!(underline!("foo"))]);
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
	fn link_in_a_parenthetical() {
		let s = "(see https://wnelson.dev).";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec![text!("(see "), link!("https://wnelson.dev"), text!(").")]
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

	/// A schemaless host in the middle of a word is not a link.
	///
	/// Without this, `getscammeddiscord.gg/x` hands a scam domain a real invite: the run before the
	/// host becomes its own text node and the tail becomes a coded link, so the client resolves an
	/// invite for a domain the author never wrote. The same shape keeps a scheme we do not support
	/// from being silently dropped -- `ftp://discord.gg/x` must not become an invite either.
	#[test]
	fn schemaless_domain_mid_token_is_text() {
		for s in [
			"getscammeddiscord.gg/invitelink",
			"getscammed_discord.gg/invitelink",
			"getscammed1discord.gg/invitelink",
			// a zero-width space is not whitespace, and reads as one token
			"getscammed\u{200b}discord.gg/invitelink",
			"ftp://discord.gg/code",
			"javascript://discord.gg/code",
			"//discord.gg/code",
			"xdiscord.gg/code",
		] {
			let (rem, res) = inline::<(), _>(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");

			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert!(
				res.iter().all(|node| matches!(node.value, Node::Text(_))),
				"expected only text for {s:?}, got {res:?}"
			);
		}
	}

	/// A host inside the run of an existing link does not start a second one.
	#[test]
	fn schemaless_domain_inside_a_link_is_part_of_it() {
		let s = "canary.discord.com/quests/1suffix.discord.com/quests/2";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res.value.len(), 1, "expected one node, got {res:?}");
		assert!(
			matches!(res.value[0].value, Node::Link(_)),
			"expected a link, got {res:?}"
		);
	}

	/// The boundary is whitespace, not "anything non-alphanumeric".
	#[test]
	fn schemaless_domain_after_whitespace_is_a_link() {
		for s in [
			"discord.gg/code",
			"hello discord.gg/code",
			"hello\ndiscord.gg/code",
			"hello\tdiscord.gg/code",
			// the whole host, not `discord.gg` at an offset inside it
			"www.discord.gg/code",
		] {
			let (rem, res) = inline::<(), _>(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");

			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert!(
				res.iter().any(|node| matches!(node.value, Node::Link(_))),
				"expected a link for {s:?}, got {res:?}"
			);
		}
	}

	/// A scheme delimits itself, so it is still detected mid-token.
	#[test]
	fn schemed_url_mid_token_still_detected() {
		let s = "lolhttps://discord.gg/code";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert!(
			res.iter().any(|node| matches!(node.value, Node::Link(_))),
			"expected a link, got {res:?}"
		);
	}
}
