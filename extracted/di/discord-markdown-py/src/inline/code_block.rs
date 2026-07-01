use std::borrow::Cow;

use nom::{
	bytes::complete::{escaped_transform, tag, take_till1, take_until, take_until1},
	character::char,
	combinator::{map, opt, verify},
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
		match self.language {
			Some(ref language) => write!(
				f,
				"{}{}\n{}\n{}",
				DELIMITER, language, self.content, DELIMITER
			),
			None => write!(f, "{}\n{}\n{}", DELIMITER, self.content, DELIMITER),
		}
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
	map(
		delimited(
			tag(DELIMITER),
			(
				opt(terminated(
					opt(take_till1(|ch| matches!(ch, '\n' | '`'))),
					char('\n'),
				))
				.map(|lang| lang.flatten()),
				// TODO: we don't really support escape sequences in codeblocks today
				escaped_transform(take_until1(DELIMITER), '\\', tag(DELIMITER)),
			),
			tag(DELIMITER),
		),
		|(language, content): (Option<Input<'data>>, String)| CodeBlock {
			language: language.map(|l| l.content),
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
