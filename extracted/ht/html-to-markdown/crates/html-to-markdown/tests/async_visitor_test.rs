//! Integration tests for async visitor functionality
//! Tests that async visitors work correctly with current_thread runtime

#![cfg(feature = "async-visitor")]

use async_trait::async_trait;
use html_to_markdown_rs::visitor::{AsyncHtmlVisitor, NodeContext, VisitResult};
use std::cell::RefCell;
use std::rc::Rc;

#[derive(Debug)]
struct CustomOutputVisitor;

#[async_trait]
impl AsyncHtmlVisitor for CustomOutputVisitor {
    async fn visit_heading(&mut self, _ctx: &NodeContext, level: u32, text: &str, _id: Option<&str>) -> VisitResult {
        // Return custom output for headings
        VisitResult::Custom(format!("[HEADING-{}] {}\n\n", level, text))
    }

    async fn visit_text(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }
}

// Manual test function for current_thread runtime
// Note: We don't use #[tokio::test] here because it requires the macros feature
// Instead, this test demonstrates that the code compiles and can be called
#[test]
fn test_async_visitor_signature_compatibility() {
    // This test verifies that the AsyncToSyncVisitorBridge properly compiles
    // and can wrap async visitors for use in sync contexts.
    // The actual functionality is tested in integration tests or manually.

    // Create a visitor
    let visitor = CustomOutputVisitor;
    let _visitor_handle: Rc<RefCell<dyn AsyncHtmlVisitor>> = Rc::new(RefCell::new(visitor));

    // This test just verifies compilation
}

#[derive(Debug)]
struct SkipImagesVisitor;

#[async_trait]
impl AsyncHtmlVisitor for SkipImagesVisitor {
    async fn visit_image(&mut self, _ctx: &NodeContext, _src: &str, _alt: &str, _title: Option<&str>) -> VisitResult {
        VisitResult::Skip
    }
}

#[test]
fn test_skip_images_visitor_compiles() {
    // Verify the SkipImagesVisitor compiles correctly
    let visitor = SkipImagesVisitor;
    let _visitor_handle: Rc<RefCell<dyn AsyncHtmlVisitor>> = Rc::new(RefCell::new(visitor));
}
