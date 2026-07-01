#![warn(clippy::pedantic)]
#![cfg_attr(test, allow(clippy::similar_names))]
#![doc = include_str!("../README.md")]

use std::fmt::{Debug, Display};

use context::Context;
pub use context::Options;
use nom::{combinator::all_consuming, Finish, Parser};

use node::SpannedNodes;

/// Parsing block markdown content.
pub mod block;
/// Context for parsing markdown content.
pub mod context;
pub mod error;
/// Markdown grammar definitions.
pub mod grammar;
/// Parsing inline markdown content.
pub mod inline;
mod input;
/// Markdown nodes.
pub mod node;
/// Rules for parsing markdown content.
pub mod rule;
/// Spans for Markdown nodes
pub mod span;
#[cfg(test)]
mod test_utils;
pub mod unparse;
pub mod util;

#[doc(hidden)]
pub mod macros;

pub use input::Input;
use span::Span;
use tracing::Level;

use crate::error::ParseError;

/// Parse markdown content.
///
/// # Errors
/// If parsing fails. Ideally this should never happen, since all content is markdown content.
#[tracing::instrument(ret, err, level = Level::DEBUG)]
pub fn parse<'data, S, E>(
	data: impl Into<Input<'data>> + Debug,
	options: Options,
) -> Result<SpannedNodes<'data, S>, E>
where
	S: Span,
	E: ParseError<'data> + Display,
{
	Ok(all_consuming(block::block(Context::new(options)))
		.parse_complete(data.into())
		.finish()?
		.1)
}

#[cfg(test)]
mod test {
	use super::parse;
	use crate::context::Options;
	use crate::test_utils::handle_nom_err;
	use crate::{
		bold, code_block, heading, list, list_item, paragraph, spanned_vec, spoiler, text,
	};
	use ntest::timeout;

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
	fn block_content_inside_inline() {
		let s = "||\n# test\nstuff goes here\n```js\nconst a = '2'\n```\n||";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![paragraph!(spoiler!(
				heading!(1, "test"),
				text!("stuff goes here\n"),
				code_block!(language = "js", "const a = '2'\n"),
				text!("\n")
			))]
		);
	}

	#[test]
	fn blocks_cannot_be_nested_in_other_blocks_via_middleman_inline_node() {
		let s = "- content ||\n# test||";
		let res = parse::<(), _>(s, Options::default())
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(
			res,
			spanned_vec![list!(-[list_item!("content ||")]), heading!(1, "test||")]
		);
	}

	#[test]
	#[timeout(1000)]
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
	#[timeout(1000)]
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

	#[test]
	#[timeout(1000)]
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
	#[timeout(1000)]
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
}
