use derive_where::derive_where;

use crate::{
	Input,
	context::Context,
	error::PResult,
	lossless::TokenKind,
	node::{
		Element, Elements, Sequence,
		block::{inline_block, list::indent},
	},
	scope::Scope,
	span::{Span, Syntax},
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

fn content<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
	item_indent: usize,
) -> PResult<Elements<'data, S>> {
	// TODO: verify that InlineBlockRule is correct here (possibly should be BlockRule)
	let block_context = context.clone().with_scope(Scope::Block);
	let first_content =
		input.spanned(|input| inline_block(input, &block_context).map(Element::Paragraph))?;

	input.spanned_with_syntax(|input| {
		let mut nodes = vec![first_content];
		let mut syntax = S::Syntax::default();
		while let Some((prefix, node)) = input.attempt(|input| {
			let prefix =
				input.token::<S, _>(TokenKind::QuotePrefix, |input| context.line_prefix(input))?;
			// first check if the next item is indented enough to be considered a child list
			let list = input.attempt(|input| {
				input.spanned(|input| indented(input, context, item_indent).map(Element::List))
			})?;
			let node = match list {
				Some(list) => list,
				// then we can continue parsing current list items
				None => input.spanned(|input| {
					let indent = input
						.token::<S, _>(TokenKind::Indent, |input| indent(input, item_indent))?;
					let mut paragraph = inline_block::<S>(input, &block_context)?;
					paragraph.span.attach(indent);
					Ok(Element::Paragraph(paragraph))
				})?,
			};
			Ok((prefix, node))
		})? {
			nodes.push(node);
			syntax.append(prefix);
		}
		Ok((nodes, syntax))
	})
}

/// Parse a list item with a current indent level. The indent level can be 0 or detected with
/// [`super::peek_indent`].
///
/// ```
/// # use discord_markdown::{
/// #    Input,
/// #    node::Element,
/// #    node::block::list::item::{Item, item},
/// # };
/// use discord_markdown::{context::Context, node::block::list::{start_type, Type}, spanned_vec};
///
/// let mut input = Input::from("1. foo");
/// let (kind, item) = item::<()>(&mut input, &Context::default(), 0, start_type)
///     .expect("should parse");
///
/// assert_eq!(input, "");
/// assert_eq!(kind, Type::Ordered(1.try_into().unwrap()));
/// assert_eq!(
///     item,
///     Item {
///         content: spanned_vec![Element::Paragraph(spanned_vec![Element::Text("foo".into())])]
///     }
/// );
/// ```
///
/// # Errors
/// If the content does not begin with a list item at that indent level.
pub fn item<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
	indent_amount: usize,
	parse_type: impl FnOnce(&mut Input<'data>) -> PResult<Type>,
) -> PResult<(Type, Item<S, Element<'data, S>>)> {
	let indent = input.token::<S, _>(TokenKind::Indent, |input| indent(input, indent_amount))?;
	let (kind, marker) = input.with_token::<S, _>(TokenKind::ListMarker, parse_type)?;
	let space = input.token::<S, _>(TokenKind::Whitespace, Input::space1)?;
	let mut body = content::<S>(input, context, indent_amount + INDENT_STEP)?;
	body.span.attach(indent.join(marker).join(space));
	Ok((kind, Item { content: body }))
}
