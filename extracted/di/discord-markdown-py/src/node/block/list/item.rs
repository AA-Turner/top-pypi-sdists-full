use derive_where::derive_where;
use nom::{Parser, branch::alt, character::complete::space1, combinator::map, multi::fold_many0};

use crate::{
	Input,
	context::Context,
	error::ParseError,
	lossless::TokenKind,
	node::{
		Element, Elements, Sequence,
		block::{inline_block, list::indent},
	},
	scope::Scope,
	span::{Span, Syntax, WithSpan, WithToken, attach},
	unparse::Unparse,
};

use super::{Type, indented};

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

/// A list item represented by its [`Type`] and a Vec of blocks as content.
///
/// List items will only ever contain [`Block::Paragraph`] as the first item and can only contain
/// [`Block::Paragraph`] or [`Block::List`] as any additional content. However, changes to this are
/// not considered a breaking change.
///
/// [`Block::Paragraph`]: crate::node::Block::Paragraph
/// [`Block::List`]: crate::node::Block::List
#[derive_where(Debug, Clone, PartialEq, Eq; N)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(bound(
		serialize = "N: serde::Serialize",
		deserialize = "N: serde::Deserialize<'de>"
	))
)]
pub struct Item<S: Span, N> {
	pub content: Sequence<S, N>,
}

impl<S, N> Unparse for Item<S, N>
where
	S: Span,
	N: Unparse,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		Unparse::fmt(&self.content, f)
	}
}

fn content<'data, S, E>(
	context: Context,
	item_indent: usize,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	move |data| {
		let context = context.clone();
		let (data, first_content) =
			// TODO: verify that InlineBlockRule is correct here (possibly should be BlockRule)
			map(inline_block(context.clone().with_scope(Scope::Block)), Element::Paragraph).span().parse_complete(data)?;

		fold_many0(
			(
				context
					.clone()
					.line_prefix()
					.token::<S>(TokenKind::QuotePrefix),
				alt((
					// first check if the next item is indented enough to be considered a child list
					map(indented(context.clone(), item_indent), Element::List).span(),
					// then we can continue parsing current list items
					map(
						(
							indent(item_indent).token::<S>(TokenKind::Indent),
							inline_block(context.with_scope(Scope::Block)),
						),
						|(indent, mut content): (_, Elements<'data, S>)| {
							content.span.attach(indent);
							Element::Paragraph(content)
						},
					)
					.span(),
				)),
			),
			move || (vec![first_content.clone()], S::Syntax::default()),
			|(mut nodes, syntax), (prefix, node)| {
				nodes.push(node);
				(nodes, syntax.join(prefix))
			},
		)
		.span()
		.map(attach)
		.parse_complete(data)
	}
}

/// Parse a list item with a current indent level. The indent level can be 0 or detected with
/// [`super::peek_indent`].
///
/// ```
/// # use discord_markdown::{
/// #    node::Element,
/// #    node::block::list::item::{Item, item},
/// # };
/// # use nom::Parser;
/// use discord_markdown::{context::Context, node::block::list::{start_type, Type}, spanned_vec};
///
/// let (rem, (kind, item)) = item::<(), nom::error::Error<_>>(Context::default(), 0, start_type)
///     .parse_complete("1. foo".into())
///     .expect("should parse");
///
/// assert_eq!(rem, "");
/// assert_eq!(kind, Type::Ordered(1.try_into().unwrap()));
/// assert_eq!(
///     item,
///     Item {
///         content: spanned_vec![Element::Paragraph(spanned_vec![Element::Text("foo".into())])]
///     }
/// );
/// ```
pub fn item<'data, S, E>(
	context: Context,
	indent_amount: usize,
	parse_type: impl Parser<Input<'data>, Output = Type, Error = E>,
) -> impl Parser<Input<'data>, Output = (Type, Item<S, Element<'data, S>>), Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	(
		indent(indent_amount).token::<S>(TokenKind::Indent),
		parse_type.with_token::<S>(TokenKind::ListMarker),
		space1.token::<S>(TokenKind::Whitespace),
		content(context, indent_amount + INDENT_STEP),
	)
		.map(
			|(indent, (kind, marker), space, mut content): (_, _, _, Elements<'data, S>)| {
				content.span.attach(indent.join(marker).join(space));
				(kind, Item { content })
			},
		)
}
