use derive_where::derive_where;

use crate::{
	Input,
	context::Context,
	error::PResult,
	lossless::TokenKind,
	node::{Element, Sequence, block::inline_block},
	scope::Scope,
	span::{Span, Syntax},
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

/// Parse small content.
///
/// # Errors
/// If the data does not begin with small content.
pub fn small<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<Small<S, Element<'data, S>>> {
	let marker = input.token::<S, _>(TokenKind::SmallMarker, |input| input.tag(PREFIX))?;
	let space = input.token::<S, _>(TokenKind::Whitespace, Input::space1)?;
	let mut text = inline_block::<S>(input, &context.clone().with_scope(Scope::Block))?;
	text.span.attach(marker.join(space));
	Ok(Small { content: text })
}

#[cfg(test)]
mod test {
	use crate::{
		context::Context,
		node::{Block, Element},
		spanned_vec,
		test_utils::{resolved_block, run},
		text,
	};

	use super::{Small, small};

	#[test]
	fn basic_small() {
		let s = "-# foo";
		let (rem, res) =
			run(s, |input| small::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_block(Element::Small(res)),
			Block::Small(Small {
				content: spanned_vec![text!("foo")]
			})
		);
	}
}
