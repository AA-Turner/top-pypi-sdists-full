use crate::{node::Node, span::Span};

/// Iterator over nodes.
pub struct Iter<'data, 'node, S>
where
	S: Span,
{
	pub(super) node: Option<&'node Node<'data, S>>,
	pub(super) children: Option<Box<dyn Iterator<Item = &'node Node<'data, S>> + 'node>>,
}

impl<'data, 'node, S> std::iter::Iterator for Iter<'data, 'node, S>
where
	S: Span,
{
	type Item = &'node Node<'data, S>;

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
