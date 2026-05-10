//! Default visitor implementations and utilities.
//!
//! This module provides standard visitor patterns and helpers for common use cases.

use std::cell::RefCell;
use std::rc::Rc;

/// Type alias for a visitor handle (Rc-wrapped `RefCell` for interior mutability).
///
/// This allows visitors to be passed around and shared while still being mutable.
pub type VisitorHandle = Rc<RefCell<dyn super::traits::HtmlVisitor>>;

#[cfg(test)]
mod tests {
    use super::super::traits::HtmlVisitor;
    use super::super::types::{NodeContext, NodeType, VisitResult};
    use std::collections::BTreeMap;

    #[derive(Debug)]
    struct TrackingVisitor {
        element_count: usize,
        text_count: usize,
    }

    impl HtmlVisitor for TrackingVisitor {
        fn visit_element_start(&mut self, _ctx: &NodeContext) -> VisitResult {
            self.element_count += 1;
            VisitResult::Continue
        }

        fn visit_text(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
            self.text_count += 1;
            VisitResult::Continue
        }
    }

    #[test]
    fn test_visitor_handle_creation() {
        let visitor = TrackingVisitor {
            element_count: 0,
            text_count: 0,
        };

        let handle = std::rc::Rc::new(std::cell::RefCell::new(visitor));

        {
            let mut v = handle.borrow_mut();
            let ctx = NodeContext {
                node_type: NodeType::Text,
                tag_name: "p".to_string(),
                attributes: BTreeMap::new(),
                depth: 1,
                index_in_parent: 0,
                parent_tag: Some("div".to_string()),
                is_inline: false,
            };
            v.visit_text(&ctx, "test");
        }

        let v = handle.borrow();
        assert_eq!(v.text_count, 1);
    }
}
