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
	context::Context,
	error::ParseError,
	node::{Element, Inlines, Sequence, block::inline_block},
	scope::Scope,
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

impl<S, N> Unparse for Small<S, N>
where
	S: Span,
	N: Unparse,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		Unparse::fmt(&self.content, f)
	}
}

/// Unparse small content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(content: &Inlines<S>, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	write!(f, "{} {}", PREFIX, content.unparse())
}

/// Parse small content.
pub fn small<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Small<S, Element<'data, S>>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	map(
		preceded(
			pair(tag(PREFIX), space1),
			inline_block(context.with_scope(Scope::Block)),
		),
		|content| Small { content },
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		context::Context,
		node::{Block, Element},
		spanned_vec,
		test_utils::{handle_nom_err, resolved_block},
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
			resolved_block(Element::Small(res)),
			Block::Small(Small {
				content: spanned_vec![text!("foo")]
			})
		);
	}
}
