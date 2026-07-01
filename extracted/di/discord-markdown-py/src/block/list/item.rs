use nom::{branch::alt, combinator::map, multi::fold_many0, sequence::preceded, Parser};

use crate::{
	block::{inline_block, list::indent},
	context::Context,
	error::ParseError,
	grammar::Grammar,
	node::{Node, SpannedNodes},
	span::{Span, WithSpan},
	unparse::Unparse,
	Input,
};

use super::{indented, Type};

/// Number of additional spaces required to considered an item to be nested inside the parent.
///
/// In the following example, "bar" is nested inside "foo" because it is indented by this value.
/// ```md
/// 1. foo
///   2. bar
/// ```
///
/// In the following example, "bar" is _not_ nested inside "foo" because it is indented by less
/// than this value.
/// ```md
/// 1. foo
///  2. bar
/// ```
pub const INDENT_STEP: usize = 2;

/// A list item represented by its [`Type`] and a Vec of [`Node`]s as content. List items will
/// only ever contain [`Node::Paragraph`] as the first item and can only contain
/// [`Node::Paragraph`] or [`Node::List`] as any additional content.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Item<'data, S: Span> {
	pub content: SpannedNodes<'data, S>,
}

impl<S> Unparse for Item<'_, S>
where
	S: Span,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		Unparse::fmt(&self.content, f)
	}
}

fn content<'data, S, E>(
	context: Context,
	item_indent: usize,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	move |data| {
		let context = context.clone();
		let (data, first_content) =
			// TODO: verify that InlineBlockRule is correct here (possibly should be BlockRule)
			map(inline_block(context.clone().with_grammar(Grammar::Block)), Node::Paragraph).span().parse_complete(data)?;

		fold_many0(
			alt((
				// first check if the next item is indented enough to be considered a child list
				map(indented(context.clone(), item_indent), Node::List).span(),
				// then we can continue parsing current list items
				map(
					preceded(
						indent(item_indent),
						inline_block(context.with_grammar(Grammar::Block)),
					),
					Node::Paragraph,
				)
				.span(),
			)),
			move || vec![first_content.clone()],
			|mut acc, item| {
				acc.push(item);
				acc
			},
		)
		.span()
		.parse_complete(data)
	}
}

/// Parse a list item with a current indent level. The indent level can be 0 or detected with
/// [`super::peek_indent`].
///
/// ```
/// # use discord_markdown::{
/// #    node::Node,
/// #    rule::RuleSet,
/// #    block::list::item::{Item, item},
/// # };
/// # use nom::Parser;
/// use discord_markdown::{context::Context, block::list::{unknown_type, Type}, spanned_vec};
///
/// let (rem, (kind, item)) = item::<(), nom::error::Error<_>>(Context::default(), 0, unknown_type)
///     .parse_complete("1. foo".into())
///     .expect("should parse");
///
/// assert_eq!(rem, "");
/// assert_eq!(kind, Type::Ordered(1));
/// assert_eq!(
///     item,
///     Item {
///         content: spanned_vec![Node::Paragraph(spanned_vec![Node::Text("foo".into())])]
///     }
/// );
/// ```
pub fn item<'data, S, E>(
	context: Context,
	indent_amount: usize,
	parse_type: impl Parser<Input<'data>, Output = Type, Error = E>,
) -> impl Parser<Input<'data>, Output = (Type, Item<'data, S>), Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	preceded(
		indent(indent_amount),
		(
			parse_type,
			map(content(context, indent_amount + INDENT_STEP), |content| {
				Item { content }
			}),
		),
	)
}
