use nom::{
	Parser,
	branch::alt,
	character::complete::{char, line_ending, space0, space1},
	combinator::{eof, map},
	multi::{fold_many_m_n, fold_many0},
	sequence::terminated,
};

use derive_where::derive_where;

use crate::{
	Input,
	context::Context,
	error::ParseError,
	lossless::TokenKind,
	node::{Element, Sequence, block::inline_block},
	scope::Scope,
	span::{Span, Syntax, WithToken},
	unparse::Unparse,
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

impl<S: Span, N: Unparse> Unparse for Heading<S, N> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		write!(
			f,
			"{} {}",
			"#".repeat(self.level as usize),
			self.content.unparse()
		)
	}
}

/// Parse a heading.
///
/// # Errors
/// If the data does not begin with heading content.
pub fn heading<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Heading<S, Element<'data, S>>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	// `space1` on the final line, so every iteration consumes input
	let blank_line = (
		context.line_prefix().token::<S>(TokenKind::QuotePrefix),
		alt((
			(
				space0.token::<S>(TokenKind::Indent),
				line_ending.token::<S>(TokenKind::LineEnding),
			)
				.map(|(space, line_ending)| space.join(line_ending)),
			terminated(space1.token::<S>(TokenKind::Indent), eof),
		)),
	)
		.map(|(prefix, rest)| prefix.join(rest));

	map(
		(
			fold_many_m_n(1, MAX_HEADING_LEVEL, char('#'), || 0u8, |acc, _| acc + 1)
				.with_token::<S>(TokenKind::HeadingMarker),
			space1.token::<S>(TokenKind::Whitespace), // TODO: should this be exactly 1 space?
			inline_block(context.with_scope(Scope::Block)),
			fold_many0(blank_line, S::Syntax::default, Syntax::join),
		),
		|((level, marker), space, mut content, blank_lines): (_, _, Sequence<S, _>, _)| {
			content.span.attach(marker.join(space).join(blank_lines));
			Heading { level, content }
		},
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		bold, italic, link, spanned_vec,
		test_utils::{handle_nom_err, resolved_block},
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

	#[test]
	fn basic_heading() {
		let s = "# foo";
		let (rem, res) = heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		let (rem, res) = heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		let (rem, res) = heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		let (rem, res) = heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		let (rem, _) = heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
	}

	#[test]
	fn heading_leaves_indented_content() {
		let s = "# foo\n  bar";
		let (rem, _) = heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "  bar");
	}

	#[test]
	fn heading_must_have_space_between_control_char_and_content() {
		let s = "#1 priority";
		heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse heading with no separating space");
	}

	#[test]
	fn heading_cannot_exceed_level_3() {
		let s = "#### foo ";
		heading::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse >3 level heading");
	}
}
