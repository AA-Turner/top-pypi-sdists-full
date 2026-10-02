use nom::{
	character::complete::{char, space1},
	combinator::map,
	multi::fold_many_m_n,
	sequence::separated_pair,
	Parser,
};

use crate::{
	block::inline_block, context::Context, error::ParseError, grammar::Grammar, node::SpannedNodes,
	span::Span, unparse::Unparse, Input,
};

/// The maximum level a heading is allowed to be.
pub const MAX_HEADING_LEVEL: usize = 3;

/// A heading element.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Heading<'data, S: Span> {
	/// The heading level, up to [`MAX_HEADING_LEVEL`].
	pub level: u8,
	pub content: SpannedNodes<'data, S>,
}

impl<S: Span> Unparse for Heading<'_, S> {
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
) -> impl Parser<Input<'data>, Output = Heading<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	map(
		separated_pair(
			fold_many_m_n(1, MAX_HEADING_LEVEL, char('#'), || 0u8, |acc, _| acc + 1),
			space1, // TODO: should this be exactly 1 space?
			inline_block(context.with_grammar(Grammar::Block)),
		),
		|(level, content)| Heading { level, content },
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		bold, italic, link, spanned_vec,
		test_utils::handle_nom_err,
		text,
		{context::Context, inline::timestamp::Timestamp, node::Node},
	};

	use super::{heading, Heading};

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
			res,
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
			res,
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
			res,
			Heading {
				level: 3,
				content: spanned_vec![
					italic!("foo"),
					text!(" "),
					bold!(link!("https://wnelson.dev")),
					text!(" "),
					Node::Timestamp(Timestamp {
						value: 1234,
						style: None
					}),
					text!(" bar")
				]
			}
		);
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
