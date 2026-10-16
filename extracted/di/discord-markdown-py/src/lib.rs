#![warn(clippy::pedantic)]
#![cfg_attr(test, allow(clippy::similar_names))]
#![doc = include_str!("../README.md")]

use std::{
	collections::HashSet,
	fmt::{Debug, Display},
};

use context::Context;
pub use context::{DEFAULT_FUEL, Options};
use nom::{Finish, Parser, combinator::all_consuming};

use node::Blocks;
use range::Unmatched;
use span::Spanned;

/// Context for parsing markdown content.
pub mod context;
/// Error types for the parser.
pub mod error;
/// Markdown grammar definitions.
pub mod grammar;
mod input;
/// Markdown nodes.
pub mod node;
pub mod range;
/// Rules for parsing markdown content.
pub mod rule;
/// Spans for Markdown nodes
pub mod span;
#[cfg(test)]
mod test_utils;
/// Convert nodes back into markdown.
pub mod unparse;
/// Parsing utilities.
pub mod util;

#[doc(hidden)]
pub mod macros;

pub use input::Input;
use span::Span;
use tracing::Level;
pub use unparse::unparse;

use crate::error::ParseError;

/// Parse markdown content.
///
/// # Errors
/// If parsing fails. Ideally this should never happen, since all content is markdown content.
#[tracing::instrument(ret, err, level = Level::DEBUG)]
pub fn parse<'data, S, E>(
	data: impl Into<Input<'data>> + Debug,
	options: Options,
) -> Result<Blocks<'data, S>, E>
where
	S: Span,
	E: ParseError<'data> + Display,
{
	// Modifiers are parsed as delimiters and resolved into the tree once the whole message is in;
	// see `range`.
	//
	// An opener read before block syntax that then matches nothing was not an opener, and its line
	// is a paragraph; parse again without it. Each round settles at least one, and the rounds
	// share one fuel tank. Past the last, whatever is left stays where it stands.
	const ROUNDS: usize = 4;

	let input = data.into();
	let mut disabled = HashSet::new();
	let mut context = Context::new(options);

	for round in 1..=ROUNDS {
		context = context.with_disabled_openers(&disabled);
		let parsed = all_consuming(node::block::block(context.clone()))
			.parse_complete(input.clone())
			.finish()?
			.1;

		let unmatched = if round < ROUNDS {
			Unmatched::Reject
		} else {
			Unmatched::Text
		};
		match range::resolve(
			parsed.value,
			options.allowed_rules,
			unmatched,
			&mut node::Ids::default(),
		) {
			Ok(nodes) => {
				return Ok(Spanned {
					value: nodes,
					span: parsed.span,
				});
			}
			Err(unmatched) => disabled.extend(unmatched),
		}
	}

	unreachable!("the last round resolves regardless")
}

#[cfg(test)]
mod test {
	use super::parse;
	use crate::context::{DEFAULT_FUEL, Options};
	use crate::error::Error;
	use crate::node::{Block, Inline};
	use crate::rule::{Rule, RuleSet};
	use crate::test_utils::handle_nom_err;
	use crate::{
		bold, code_block, heading, italic, link, list, list_item, paragraph, spanned_vec, spoiler,
		text,
	};
	use ntest::timeout;

	// These guard against algorithmic blowup -- quadratic backtracking on adversarial input --
	// rather than against small regressions, so the budget only has to be tight enough to catch a
	// multiple. CI runs `cargo test --release`, where the worst of them takes ~80ms, so 1s there
	// leaves better than 10x headroom. A debug build is ~15x slower and lands near the same 1s,
	// which makes the tests flap on nothing more than a busy laptop; debug gets a budget scaled to
	// match instead.

	/// Exhausting the tank fails the parse outright — the caller gets an error, not a truncated
	/// AST — and an error type that keeps the external error says so. This is the cost of setting
	/// [`Options::fuel`] too low.
	#[test]
	fn fuel_exhaustion_fails_the_parse() {
		let s = "**bold** and _italic_";

		let err = parse::<(), Error<'_>>(
			s,
			Options {
				fuel: 1,
				..Default::default()
			},
		)
		.expect_err("one unit cannot cover a line and its inline parse");
		assert_eq!(err, Error::OutOfFuel);

		parse::<(), Error<'_>>(s, Options::default())
			.expect("the same input parses with the default budget");
	}

	/// The worst 4000-character inputs the timeout tests know about stay far inside
	/// [`DEFAULT_FUEL`], which is what makes that default safe to ship. If this starts failing,
	/// a rule change has made backtracking much more expensive.
	#[test]
	fn default_fuel_covers_worst_case_message_content() {
		// Discord's message limit is 4000 characters.
		for s in [
			"__".repeat(1_000) + "x" + &"_".repeat(1_998),
			"**".repeat(1_000) + "x" + &"*".repeat(1_998),
			// every line opens a delimiter before block syntax that only the last lines close
			"**a\n__a\n~~a\n||a\n".repeat(249) + "a||\na~~\na__\na**",
		] {
			assert_eq!(s.chars().count(), 4_000 - 1);

			let used = (1..=5)
				.map(|n| DEFAULT_FUEL / 10 * n)
				.find(|&fuel| {
					parse::<(), Error<'_>>(
						&*s,
						Options {
							fuel,
							..Default::default()
						},
					)
					.is_ok()
				})
				.expect("worst-case message content should fit in half the default budget");

			assert!(
				used <= DEFAULT_FUEL / 2,
				"worst-case message content used {used} of {DEFAULT_FUEL} fuel, leaving too little headroom"
			);
		}
	}

	/// Escape sequences are independent of one another.
	///
	/// A backslash the parser cannot use as an escape -- before an ASCII alphanumeric, before
	/// whitespace, or at the very end of the input -- is literal text, and says nothing about the
	/// escapes around it. Each of those still drops its own backslash and still suppresses the
	/// delimiter it precedes, whether it comes before or after the unusable one.
	#[test]
	fn escapes_are_independent() {
		// The control: no unusable backslash anywhere.
		let s = r"a \* b \* c";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec![paragraph!(text!(r"a * b * c"))]);

		// The same escapes, followed by a backslash that cannot be used as one. The `\*` pair
		// must still suppress the italics it would otherwise open.
		for (s, expected) in [
			(r"a \* b \* c \d", r"a * b * c \d"),
			("a \\* b \\* c \\", "a * b * c \\"),
			("a \\* b \\* c \\ ", "a * b * c \\ "),
		] {
			let res = parse::<(), _>(s, Options::default())
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(
				res,
				spanned_vec![paragraph!(Inline::Text(expected.into()))],
				"unexpected output for {s:?}"
			);
		}

		// ...and preceded by one, which has always worked: the run restarts after it.
		let s = r"regex \d+ then \_escaped\_";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![paragraph!(text!(r"regex \d+ then _escaped_"))]
		);
	}

	/// Every way of writing a `dev` link is a link with [`Rule::DevLink`], and text without it.
	#[test]
	fn dev_links_need_their_rule() {
		let without_dev = Options {
			allowed_rules: RuleSet::all() - Rule::DevLink,
			..Default::default()
		};

		for (s, expected) in [
			(
				"dev://branch/main",
				spanned_vec![link!("dev://branch/main")],
			),
			(
				"<dev://branch/main>",
				spanned_vec![link!("dev://branch/main")],
			),
			(
				"[branch](dev://branch/main)",
				spanned_vec![link!("dev://branch/main", [text!("branch")])],
			),
		] {
			let res = parse::<(), _>(s, Options::default())
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(
				res,
				spanned_vec![Block::Paragraph(expected)],
				"unexpected output for {s:?}"
			);

			let res = parse::<(), _>(s, without_dev)
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(
				res,
				spanned_vec![paragraph!(Inline::Text(s.into()))],
				"unexpected output for {s:?} without the rule"
			);
		}
	}

	/// The rule does not widen what the `dev` scheme accepts.
	#[test]
	fn dev_link_with_an_unrouted_domain_is_text() {
		let s = "dev://nonsense/foo";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec![paragraph!(Inline::Text(s.into()))]);
	}

	#[test]
	fn flattened_compound_test() {
		let s = r"**_bar_baz**";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec![paragraph!(bold!("_bar_baz"))]);
	}

	#[test]
	fn flattened_compound_test2() {
		let s = r"**baz****baab**";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec![paragraph!(bold!("bazbaab"))]);
	}

	/// Both italic grammars share [`Rule::Italic`], so one delimiter nests inside the other. The
	/// inner wrapper applies nothing, and keeping it would round trip as an underline, since
	/// italics always unparse to `_`.
	#[test]
	fn flattened_nested_italic_test() {
		for s in ["_*a*_", "*_a_*"] {
			let res = parse::<(), _>(s, Options::default())
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(
				res,
				spanned_vec![paragraph!(italic!("a"))],
				"unexpected output for {s:?}"
			);
		}
	}

	/// A nested italic that is not the sole child merges the text it was separating.
	#[test]
	fn flattened_nested_italic_merges_its_siblings_test() {
		let s = "_a *b* c_";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec![paragraph!(italic!("a b c"))]);
	}

	/// The collapse reaches through the bold in between, which loses the `_c_` that was written.
	#[test]
	fn flattened_nested_italic_through_bold_test() {
		let s = "*a **b _c_ d** e*";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![paragraph!(italic!(
				text!("a "),
				bold!("b c d"),
				text!(" e")
			))]
		);
	}

	/// A merged node spans both halves, delimiters included -- a start/end pair cannot describe
	/// the two disjoint regions the content actually came from.
	#[test]
	fn flattened_spans_cover_both_halves() {
		use crate::span::TrackedSpan;

		let s = r"**baz****baab**";
		let res = parse::<TrackedSpan, _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		let paragraph = &res.value[0];
		let Block::Paragraph(content) = &paragraph.value else {
			panic!("expected a paragraph, got {:?}", paragraph.value)
		};
		let bold = &content.value[0];
		let Inline::Bold(children) = &bold.value else {
			panic!("expected bold, got {:?}", bold.value)
		};

		let spans = [
			(bold.span.start, bold.span.end),
			(children.span.start, children.span.end),
			(children.value[0].span.start, children.value[0].span.end),
		];
		assert_eq!(spans, [(0, 15), (2, 13), (2, 13)]);
		assert_eq!(&s[0..15], "**baz****baab**");
		assert_eq!(&s[2..13], "baz****baab");
	}

	#[test]
	fn should_not_match_heading_inside_text() {
		let s = "there is text here with a # but it shouldn't match headings!";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![paragraph!(
				"there is text here with a # but it shouldn't match headings!"
			)]
		);
	}

	#[test]
	fn left_arrow() {
		let s = "<";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(res, spanned_vec![paragraph!("<")]);
	}

	#[test]
	fn block_content_inside_modifier() {
		let s = "||\n# test\nstuff goes here\n```js\nconst a = '2'\n```\n||";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![
				heading!(1, [spoiler!("test")]),
				paragraph!(spoiler!("stuff goes here")),
				paragraph!(spoiler!(code_block!(language = "js", "const a = '2'\n")))
			]
		);
	}

	/// A modifier opened mid-paragraph applies to the blocks that follow it, inside each list item.
	#[test]
	fn a_modifier_opened_mid_paragraph_covers_a_following_list() {
		let s = "foo ||\n- a\n- b||";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![
				paragraph!("foo "),
				list!(-[
					list_item!(paragraph!(spoiler!("a"))),
					list_item!(paragraph!(spoiler!("b")))
				])
			]
		);
	}

	#[test]
	fn blocks_cannot_be_nested_in_other_blocks_via_middleman_inline_node() {
		let s = "- content ||\n# test||";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		// the spoiler reaches from the list into the heading, but neither block holds the other
		assert_eq!(
			res,
			spanned_vec![
				list!(-[list_item!("content ")]),
				heading!(1, [spoiler!("test")])
			]
		);
	}

	/// End to end, a list written across quoted lines is a single list inside a single quote --
	/// including when it nests, and for both quote syntaxes.
	#[test]
	fn quoted_lists_are_cohesive_through_the_public_api() {
		for s in ["> - foo\n>   - bar\n> - baz", ">>> - foo\n  - bar\n- baz"] {
			let res = parse::<(), _>(s, Options::default())
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(
				res,
				spanned_vec![Block::Quote(spanned_vec![list!(-[
					list_item![paragraph!("foo"), list!(-[list_item!("bar")])],
					list_item!("baz")
				])])],
				"unexpected output for {s:?}"
			);
		}
	}

	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn single_repeats() {
		for c in [
			"\t", " ", "!", "\"", "#", "$", "%", "\'", "(", ")", "*", "+", ",", "-", ".", "/", ":",
			";", "<", "=", ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~",
		] {
			let s = c.repeat(2_000);
			// Checking for timeouts
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
	}

	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn pair_repeats_matched() {
		let opens = ["(", "<", "[", "{", "~~", "_", "__", "*", "**", "<", "<:"];
		let closes = [")", ">", "]", "}", "~~", "_", "__", "*", "**", ":/", ":>"];
		for (i, open_c) in opens.iter().enumerate() {
			let close_c = closes[i];
			// Checking for timeouts when there are equal opens and closes
			let open_s = open_c.repeat(2_000);
			let close_s = close_c.repeat(2_000);
			let s = open_s + "x" + &close_s;
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
	}

	/// Runs where every delimiter could both open and close, where the pairing has to choose
	/// between an italic and a bold at each one, plus deep alternating nesting, which every pass
	/// over the rebuilt tree recurses through.
	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn overlapping_delimiter_repeats() {
		let mut nested = String::new();
		for i in 0..500 {
			nested.push_str(if i % 2 == 0 { "*" } else { "**" });
			nested.push('x');
		}
		for i in (0..500).rev() {
			nested.push_str(if i % 2 == 0 { "*" } else { "**" });
		}

		for s in [
			"*".to_owned() + &"**".repeat(1_300),
			"_".to_owned() + &"__".repeat(1_300),
			"*x".repeat(1_000) + &"*".repeat(2_000),
			"_x".repeat(1_000) + &"_".repeat(2_000),
			"*a **b** ".repeat(440),
			nested,
		] {
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
	}

	/// Lines that each open a delimiter before block syntax, only some of which anything closes:
	/// every unmatched one costs a parse without it.
	///
	/// Each input is about the 4000 character message limit.
	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn opener_before_block_repeats() {
		for s in [
			"*a\n_a\n".repeat(660) + "a_\na*",
			"**a\n__a\n~~a\n||a\n".repeat(235) + "a||\na~~\na__\na**",
			"*1. a\n".repeat(660) + "a*",
		] {
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
	}

	/// As [`opener_before_block_repeats`], for other line shapes, plus pairs that would nest far
	/// deeper than anything written by hand.
	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn delimiter_line_repeats() {
		for s in [
			"***a\n___a\n".repeat(400),
			"*a\n".repeat(1_300),
			"*- a\n".repeat(1_000) + "*",
			"> *a\n".repeat(800) + "> a*",
			"*_".repeat(1_000) + "x" + &"_*".repeat(1_000),
			"**".repeat(1_000) + "x" + &"*".repeat(1_998),
		] {
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
	}

	/// Closers that each find an opener they cannot pair with, under many openers of another
	/// character. Far past the message limit, so a search per closer shows; only release builds are
	/// fast enough for a size that does.
	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn refused_pairs_repeat() {
		let n = if cfg!(debug_assertions) {
			16_000
		} else {
			64_000
		};
		let s = "*a ".to_string() + &"_ ".repeat(n) + &"* ".repeat(n);
		let options = Options {
			allowed_rules: RuleSet::all() - Rule::Italic,
			..Default::default()
		};
		let _ = parse::<(), _>(&*s, options)
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");
	}

	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn pair_repeats_partially_matched() {
		let opens = ["(", "<", "[", "{", "~~", "_", "__", "*", "**", "<", "<:"];
		let closes = [")", ">", "]", "}", "~~", "_", "__", "*", "**", ":/", ":>"];
		for (i, open_c) in opens.iter().enumerate() {
			let close_c = closes[i];
			// Checking for timeouts if there's more opens than closes
			let open_s = open_c.repeat(2_000);
			let close_s = close_c.repeat(1_000);
			let s = open_s + "x" + &close_s;
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
		for (i, open_c) in opens.iter().enumerate() {
			let close_c = closes[i];
			// Checking for timeouts if there's more closes than opens
			let open_s = open_c.repeat(1_000);
			let close_s = close_c.repeat(2_000);
			let s = open_s + "x" + &close_s;
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}
	}

	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn bracket_paren_repeats() {
		// Pure "](" — no '[' start, each position fails the first-byte check in O(1)
		let s = "](".repeat(2_000);
		let _ = parse::<(), _>(&*s, Options::default())
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");

		// One '[' followed by many "](" — balanced scan finds span_len=2, one link attempt
		let s = "[".to_string() + &"](".repeat(2_000);
		let _ = parse::<(), _>(&*s, Options::default())
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");

		// Many '[' then many "](" — each '[' position does O(n) balanced scan, one link attempt
		let s = "[".repeat(2_000) + &"](".repeat(2_000);
		let _ = parse::<(), _>(&*s, Options::default())
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");
	}

	/// An escape the text parser does not recognise used to abort the whole text run, which the
	/// inline parser then retried one character further along, rescanning to the same backslash
	/// every time. A 4 KiB run took over three seconds; these are ~1ms each.
	#[test]
	#[cfg_attr(debug_assertions, timeout(3000))]
	#[cfg_attr(not(debug_assertions), timeout(1000))]
	fn unrecognised_escape_repeats() {
		// A backslash at the end of the input, which `escaped_transform` rejects outright.
		let s = "x".repeat(4_000) + "\\";
		let _ = parse::<(), _>(&*s, Options::default())
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");

		// A backslash before a character that cannot be escaped.
		for tail in ["\\y", "\\ ", "\\\n"] {
			let s = "x".repeat(4_000) + tail;
			let _ = parse::<(), _>(&*s, Options::default())
				.map_err(handle_nom_err(&s))
				.expect("unable to parse");
		}

		// Many unrecognised escapes, each one ending a run the next has to rescan.
		let s = "x".repeat(20) + "\\y";
		let s = s.repeat(200);
		let _ = parse::<(), _>(&*s, Options::default())
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");
	}
}
