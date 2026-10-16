use crate::{node::Inline, span::Span};

/// Iterator over inline nodes.
///
/// Created by [`Inline::iter`].
pub struct Iter<'data, 'node, S>
where
	S: Span,
{
	pub(super) node: Option<&'node Inline<'data, S>>,
	pub(super) children: Option<Box<dyn Iterator<Item = &'node Inline<'data, S>> + 'node>>,
}

impl<'data, 'node, S> std::iter::Iterator for Iter<'data, 'node, S>
where
	S: Span,
{
	type Item = &'node Inline<'data, S>;

	fn next(&mut self) -> Option<Self::Item> {
		if let Some(node) = self.node.take() {
			Some(node)
		} else if let Some(children) = &mut self.children {
			children.next()
		} else {
			None
		}
	}
}
