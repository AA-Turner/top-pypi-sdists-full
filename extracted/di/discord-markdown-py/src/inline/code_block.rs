//! Code block parsing.

use std::borrow::Cow;

use nom::{
	bytes::complete::{escaped_transform, tag, take_until1, take_while1},
	character::char,
	combinator::{map, opt},
	error::ParseError,
	sequence::{delimited, terminated},
	Parser,
};

use crate::{unparse::Unparse, Input};

pub const DELIMITER: &str = "```";

#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct CodeBlock<'data> {
	pub language: Option<Cow<'data, str>>,
	pub content: String,
}

impl Unparse for CodeBlock<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		f.write_str(DELIMITER)?;
		if let Some(ref language) = self.language {
			f.write_str(language)?;
		}
		f.write_str("\n")?;
		// The content includes its own trailing newline, so writing one here grew the block by a
		// blank line on every round trip.
		f.write_str(&self.content)?;

		f.write_str(DELIMITER)
	}
}

/// Parse a codeblock.
///
/// # Note
/// This is inline because codeblocks can be started inline, but they should be omitted as a valid
/// rule from most other rules and ideally become a block level element at some point.
///
/// # Errors
/// If the content does not begin with a codeblock.
#[must_use]
pub fn code_block<'data, E>() -> impl Parser<Input<'data>, Output = CodeBlock<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	fn is_language_char(ch: char) -> bool {
		matches!(ch, 'a'..='z' | 'A'..='Z' | '0'..='9' | '_' | '+' | '-' | '.' | '#')
	}

	map(
		delimited(
			tag(DELIMITER),
			(
				opt(terminated(
					// we need 2 separate `opt`s so that we consume an empty line without making an empty language
					opt(take_while1(is_language_char)),
					char('\n'),
				))
				.map(Option::flatten),
				// TODO: we don't really support escape sequences in codeblocks today
				escaped_transform(take_until1(DELIMITER), '\\', tag(DELIMITER)),
			),
			tag(DELIMITER),
		),
		|(language, content): (Option<Input<'data>>, String)| CodeBlock {
			language: language.map(|l| Cow::Borrowed(l.content)),
			content,
		},
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::test_utils::handle_nom_err;

	use super::{code_block, CodeBlock};

	#[test]
	fn basic_codeblock() {
		let s = "```foo```";
		let (rem, res) = code_block()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			CodeBlock {
				language: None,
				content: "foo".into()
			}
		);
	}

	#[test]
	fn one_line_codeblock_with_trailing_newline() {
		let s = "```foo```\n";
		let (rem, res) = code_block()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "\n");
		assert_eq!(
			res,
			CodeBlock {
				language: None,
				content: "foo".into()
			}
		);
	}

	#[test]
	fn leading_new_line() {
		let s = "```\nfoo```";
		let (rem, res) = code_block()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			CodeBlock {
				language: None,
				content: "foo".into()
			}
		);
	}

	#[test]
	fn empty_codeblock() {
		let s = "``````";
		code_block()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	#[ignore = "supported today but dubious"]
	fn codeblock_with_new_line() {
		let s = "```\n```";
		let (rem, res) = code_block()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			CodeBlock {
				language: None,
				content: String::new()
			}
		);
	}

	#[test]
	fn codeblock_with_language() {
		let s = "```foo\nbar```";
		let (rem, res) = code_block()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			CodeBlock {
				language: Some("foo".into()),
				content: "bar".into()
			}
		);
	}
}
