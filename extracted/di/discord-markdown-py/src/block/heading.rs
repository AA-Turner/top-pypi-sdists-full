use nom::{
	Parser,
	character::complete::{char, space1},
	combinator::map,
	multi::fold_many_m_n,
	sequence::separated_pair,
};

use derive_where::derive_where;

use crate::{
	Input,
	block::inline_block,
	context::Context,
	error::ParseError,
	grammar::Grammar,
	node::{Node, ParsedNode, Sequence},
	span::Span,
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

impl<S: Span> Unparse for Heading<S, Node<'_, S>> {
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
) -> impl Parser<Input<'data>, Output = Heading<S, ParsedNode<'data, S>>, Error = E>
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
		bold, italic, link,
		range::Content,
		spanned_vec,
		test_utils::{handle_nom_err, resolved_node},
		text,
		{
			context::Context,
			inline::timestamp::Timestamp,
			node::{Element, Node, ParsedNode},
		},
	};

	use super::{Heading, heading};

	/// Resolve the delimiters in a heading, as a whole parse would.
	fn resolved_heading(heading: Heading<(), ParsedNode<'_, ()>>) -> Heading<(), Node<'_, ()>> {
		match resolved_node(
			ParsedNode::Element(Element::Heading(heading)),
			Content::Blocks,
		) {
			Node::Element(Element::Heading(heading)) => heading,
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
					Node::Element(Element::Timestamp(Timestamp {
						value: 1234,
						style: None
					})),
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
