//! Code block parsing.

use std::borrow::Cow;

use crate::{
	Input,
	error::PResult,
	lossless::TokenKind,
	span::{Span, Syntax},
};

pub const DELIMITER: &str = "```";

#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct CodeBlock<'data> {
	pub language: Option<Cow<'data, str>>,
	pub content: String,
}

fn is_language_char(ch: char) -> bool {
	matches!(ch, 'a'..='z' | 'A'..='Z' | '0'..='9' | '_' | '+' | '-' | '.' | '#')
}

/// Parse a codeblock.
///
/// # Note
/// This is inline because codeblocks can be started inline, but they should be omitted as a valid
/// rule from most other rules and ideally become a block level element at some point.
///
/// # Errors
/// If the content does not begin with a codeblock.
pub fn code_block<'data, S: Span>(
	input: &mut Input<'data>,
) -> PResult<(CodeBlock<'data>, S::Syntax)> {
	let open = input.token::<S, _>(TokenKind::CodeFence, |input| input.tag(DELIMITER))?;

	// A language is only a language if a line ending follows it; otherwise it is content. A bare
	// line ending is consumed without making an empty language.
	let first_line = input.attempt(|input| {
		let (language, language_syntax) = input
			.with_token::<S, _>(TokenKind::Language, |input| {
				Ok(input.take_while1(is_language_char).ok())
			})?;
		let line_ending = input.token::<S, _>(TokenKind::LineEnding, |input| input.char('\n'))?;
		Ok((language, language_syntax.join(line_ending)))
	})?;
	let (language, first_line) = first_line.unwrap_or_default();

	// TODO: we don't really support escape sequences in codeblocks today
	let (content, content_syntax) =
		input.with_token::<S, _>(TokenKind::CodeContent, |input| input.take_until1(DELIMITER))?;
	let close = input.token::<S, _>(TokenKind::CodeFence, |input| input.tag(DELIMITER))?;

	let code_block = CodeBlock {
		language: language.map(Cow::Borrowed),
		content: content.to_owned(),
	};
	Ok((
		code_block,
		open.join(first_line).join(content_syntax).join(close),
	))
}

#[cfg(test)]
mod test {
	use crate::test_utils::run;

	use super::{CodeBlock, code_block};

	#[test]
	fn basic_codeblock() {
		let s = "```foo```";
		let (rem, (res, ())) = run(s, code_block::<()>).expect("unable to parse");

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
		let (rem, (res, ())) = run(s, code_block::<()>).expect("unable to parse");

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
		let (rem, (res, ())) = run(s, code_block::<()>).expect("unable to parse");

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
		run(s, code_block::<()>).expect_err("able to parse");
	}

	#[test]
	#[ignore = "supported today but dubious"]
	fn codeblock_with_new_line() {
		let s = "```\n```";
		let (rem, (res, ())) = run(s, code_block::<()>).expect("unable to parse");

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
		let (rem, (res, ())) = run(s, code_block::<()>).expect("unable to parse");

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
