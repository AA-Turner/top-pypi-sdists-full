use nom::{
	bytes::complete::tag,
	character::complete::space1,
	combinator::map,
	sequence::{pair, preceded},
	Parser,
};

use crate::{
	block::inline_block, context::Context, error::ParseError, grammar::Grammar, node::SpannedNodes,
	span::Span, unparse::Unparse, Input,
};

pub const PREFIX: &str = "-#";

/// Small content.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Small<'data, S: Span> {
	pub content: SpannedNodes<'data, S>,
}

impl<S> Unparse for Small<'_, S>
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
) -> impl Parser<Input<'data>, Output = Small<'data, S>, Error = E>
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

	use crate::{context::Context, spanned_vec, test_utils::handle_nom_err, text};

	use super::{small, Small};

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
			res,
			Small {
				content: spanned_vec![text!("foo")]
			}
		);
	}
}
