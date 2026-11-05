use derive_where::derive_where;

use crate::{
	Input,
	context::Context,
	error::{Fail, PResult},
	lossless::TokenKind,
	node::{Element, Sequence, block::inline_block},
	scope::Scope,
	span::{Span, Syntax},
};

/// The maximum level a heading is allowed to be.
pub const MAX_HEADING_LEVEL: usize = 3;

/// A heading element.
#[derive_where(Debug, Clone, PartialEq, Eq; N)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(bound(
		serialize = "N: serde::Serialize",
		deserialize = "N: serde::Deserialize<'de>"
	))
)]
pub struct Heading<S: Span, N> {
	/// The heading level, up to [`MAX_HEADING_LEVEL`].
	pub level: u8,
	pub content: Sequence<S, N>,
}

/// Consume a blank line after a heading: whitespace up to a line ending, or to the end of the
/// input.
fn blank_line<S: Span>(input: &mut Input, context: &Context) -> PResult<S::Syntax> {
	let prefix = input.token::<S, _>(TokenKind::QuotePrefix, |input| context.line_prefix(input))?;

	let rest = input.attempt(|input| {
		let space = input.token::<S, _>(TokenKind::Indent, |input| Ok(input.space0()))?;
		let line_ending = input.token::<S, _>(TokenKind::LineEnding, Input::line_ending)?;
		Ok(space.join(line_ending))
	})?;
	if let Some(rest) = rest {
		return Ok(prefix.join(rest));
	}

	// `space1` on the final line, so every blank line consumes input
	let space = input.token::<S, _>(TokenKind::Indent, Input::space1)?;
	if !input.is_empty() {
		return Err(Fail::NoMatch);
	}
	Ok(prefix.join(space))
}

/// Parse a heading.
///
/// # Errors
/// If the data does not begin with heading content.
pub fn heading<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<Heading<S, Element<'data, S>>> {
	let (level, marker) = input.with_token::<S, _>(TokenKind::HeadingMarker, |input| {
		let mut level = 0u8;
		while usize::from(level) < MAX_HEADING_LEVEL && input.eat("#") {
			level += 1;
		}
		if level == 0 {
			Err(Fail::NoMatch)
		} else {
			Ok(level)
		}
	})?;
	// TODO: should this be exactly 1 space?
	let space = input.token::<S, _>(TokenKind::Whitespace, Input::space1)?;
	let mut text = inline_block::<S>(input, &context.clone().with_scope(Scope::Block))?;

	let mut blank_lines = S::Syntax::default();
	while let Some(blank_line) = input.attempt(|input| blank_line::<S>(input, context))? {
		blank_lines.append(blank_line);
	}

	text.span.attach(marker.join(space).join(blank_lines));
	Ok(Heading {
		level,
		content: text,
	})
}

#[cfg(test)]
mod test {
	use crate::{
		bold, italic, link, spanned_vec,
		test_utils::{resolved_block, run},
		text,
		{
			context::Context,
			node::{Block, Element, Inline, inline::timestamp::Timestamp},
		},
	};

	use super::{Heading, heading};

	/// Resolve the delimiters in a heading, as a whole parse would.
	fn resolved_heading(heading: Heading<(), Element<'_, ()>>) -> Heading<(), Inline<'_, ()>> {
		match resolved_block(Element::Heading(heading)) {
			Block::Heading(heading) => heading,
			other => panic!("expected a heading, got {other:?}"),
		}
	}

	fn parse(s: &str) -> crate::error::PResult<(crate::Input<'_>, Heading<(), Element<'_, ()>>)> {
		run(s, |input| heading::<()>(input, &Context::default()))
	}

	#[test]
	fn basic_heading() {
		let s = "# foo";
		let (rem, res) = parse(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_heading(res),
			Heading {
				level: 1,
				content: spanned_vec![text!("foo")]
			}
		);
	}

	#[test]
	fn heading_with_link() {
		let s = "## https://wnelson.dev";
		let (rem, res) = parse(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_heading(res),
			Heading {
				level: 2,
				content: spanned_vec![link!("https://wnelson.dev")]
			}
		);
	}

	#[test]
	fn complex_heading() {
		let s = "### _foo_ **https://wnelson.dev** <t:1234> bar";
		let (rem, res) = parse(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_heading(res),
			Heading {
				level: 3,
				content: spanned_vec![
					italic!("foo"),
					text!(" "),
					bold!(link!("https://wnelson.dev")),
					text!(" "),
					Inline::Timestamp(Timestamp {
						value: 1234,
						style: None
					}),
					text!(" bar")
				]
			}
		);
	}

	#[test]
	fn heading_consumes_blank_lines() {
		let s = "# foo\n\n \t\n\nbar";
		let (rem, res) = parse(s).expect("unable to parse");
		assert_eq!(rem, "bar");
		assert_eq!(
			resolved_heading(res),
			Heading {
				level: 1,
				content: spanned_vec![text!("foo")]
			}
		);
	}

	#[test]
	fn heading_consumes_final_whitespace_line() {
		let s = "# foo\n\n  ";
		let (rem, _) = parse(s).expect("unable to parse");
		assert_eq!(rem, "");
	}

	#[test]
	fn heading_leaves_indented_content() {
		let s = "# foo\n  bar";
		let (rem, _) = parse(s).expect("unable to parse");
		assert_eq!(rem, "  bar");
	}

	#[test]
	fn heading_must_have_space_between_control_char_and_content() {
		let s = "#1 priority";
		parse(s).expect_err("able to parse heading with no separating space");
	}

	#[test]
	fn heading_cannot_exceed_level_3() {
		let s = "#### foo ";
		parse(s).expect_err("able to parse >3 level heading");
	}
}
