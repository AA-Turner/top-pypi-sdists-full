use nom::{
	Parser,
	bytes::complete::tag,
	character::complete::space1,
	combinator::map,
	sequence::{pair, preceded},
};

use derive_where::derive_where;

use crate::{
	Input,
	block::inline_block,
	context::Context,
	error::ParseError,
	grammar::Grammar,
	node::{Node, ParsedNode, Sequence, SpannedNodes},
	span::Span,
	unparse::Unparse,
};

pub const PREFIX: &str = "-#";

/// Small content.
#[derive_where(Debug, Clone, PartialEq, Eq; N)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(bound(
		serialize = "N: serde::Serialize",
		deserialize = "N: serde::Deserialize<'de>"
	))
)]
pub struct Small<S: Span, N> {
	pub content: Sequence<S, N>,
}

impl<S> Unparse for Small<S, Node<'_, S>>
where
	S: Span,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		Unparse::fmt(&self.content, f)
	}
}

/// Unparse small content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	write!(f, "{} {}", PREFIX, content.unparse())
}

/// Parse small content.
pub fn small<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Small<S, ParsedNode<'data, S>>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	map(
		preceded(
			pair(tag(PREFIX), space1),
			inline_block(context.with_grammar(Grammar::Block)),
		),
		|content| Small { content },
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		context::Context,
		node::{Element, Node, ParsedNode},
		range::Content,
		spanned_vec,
		test_utils::{handle_nom_err, resolved_node},
		text,
	};

	use super::{Small, small};

	#[test]
	fn basic_small() {
		let s = "-# foo";
		let (rem, res) = small::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_node(ParsedNode::Element(Element::Small(res)), Content::Blocks),
			Node::Element(Element::Small(Small {
				content: spanned_vec![text!("foo")]
			}))
		);
	}
}
