//! Asynchronous visitor trait for HTML to Markdown conversion.
//!
//! This module contains the `AsyncHtmlVisitor` trait for async/await based visitation.

#[cfg(feature = "async-visitor")]
use async_trait::async_trait;

use super::types::{NodeContext, VisitResult};

/// Async visitor trait for HTML→Markdown conversion.
///
/// This trait is identical to `HtmlVisitor` but all methods are async. Use this for languages
/// with native async/await support:
/// - Python (with `async def` and `asyncio`)
/// - TypeScript/JavaScript (with `Promise`-based callbacks)
/// - Elixir (with message-passing processes)
///
/// For synchronous languages (Ruby, PHP, Go, Java, C#), use the sync `HtmlVisitor` trait.
///
/// # Example (Python-like)
///
/// ```ignore
/// use html_to_markdown_rs::visitor::{AsyncHtmlVisitor, NodeContext, VisitResult};
///
/// struct CustomAsyncVisitor;
///
/// #[async_trait::async_trait]
/// impl AsyncHtmlVisitor for CustomAsyncVisitor {
///     async fn visit_link(
///         &mut self,
///         ctx: &NodeContext,
///         href: &str,
///         text: &str,
///         title: Option<&str>,
///     ) -> VisitResult {
///         // Can await async operations here
///         VisitResult::Custom(format!("{} ({})", text, href))
///     }
/// }
/// ```
#[cfg(feature = "async-visitor")]
#[async_trait]
pub trait AsyncHtmlVisitor: std::fmt::Debug + Send + Sync {
    /// Called before entering any element (async version).
    async fn visit_element_start(&mut self, _ctx: &NodeContext) -> VisitResult {
        VisitResult::Continue
    }

    /// Called after exiting any element (async version).
    async fn visit_element_end(&mut self, _ctx: &NodeContext, _output: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit text nodes (async version - most frequent callback - ~100+ per document).
    async fn visit_text(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit anchor links `<a href="...">` (async version).
    async fn visit_link(&mut self, _ctx: &NodeContext, _href: &str, _text: &str, _title: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit images `<img src="...">` (async version).
    async fn visit_image(&mut self, _ctx: &NodeContext, _src: &str, _alt: &str, _title: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit heading elements `<h1>` through `<h6>` (async version).
    async fn visit_heading(&mut self, _ctx: &NodeContext, _level: u32, _text: &str, _id: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit code blocks `<pre><code>` (async version).
    async fn visit_code_block(&mut self, _ctx: &NodeContext, _lang: Option<&str>, _code: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit inline code `<code>` (async version).
    async fn visit_code_inline(&mut self, _ctx: &NodeContext, _code: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit list items `<li>` (async version).
    async fn visit_list_item(&mut self, _ctx: &NodeContext, _ordered: bool, _marker: &str, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Called before processing a list `<ul>` or `<ol>` (async version).
    async fn visit_list_start(&mut self, _ctx: &NodeContext, _ordered: bool) -> VisitResult {
        VisitResult::Continue
    }

    /// Called after processing a list `</ul>` or `</ol>` (async version).
    async fn visit_list_end(&mut self, _ctx: &NodeContext, _ordered: bool, _output: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Called before processing a table `<table>` (async version).
    async fn visit_table_start(&mut self, _ctx: &NodeContext) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit table rows `<tr>` (async version).
    async fn visit_table_row(&mut self, _ctx: &NodeContext, _cells: &[String], _is_header: bool) -> VisitResult {
        VisitResult::Continue
    }

    /// Called after processing a table `</table>` (async version).
    async fn visit_table_end(&mut self, _ctx: &NodeContext, _output: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit blockquote elements `<blockquote>` (async version).
    async fn visit_blockquote(&mut self, _ctx: &NodeContext, _content: &str, _depth: usize) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit strong/bold elements `<strong>`, `<b>` (async version).
    async fn visit_strong(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit emphasis/italic elements `<em>`, `<i>` (async version).
    async fn visit_emphasis(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit strikethrough elements `<s>`, `<del>`, `<strike>` (async version).
    async fn visit_strikethrough(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit underline elements `<u>`, `<ins>` (async version).
    async fn visit_underline(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit subscript elements `<sub>` (async version).
    async fn visit_subscript(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit superscript elements `<sup>` (async version).
    async fn visit_superscript(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit mark/highlight elements `<mark>` (async version).
    async fn visit_mark(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit line break elements `<br>` (async version).
    async fn visit_line_break(&mut self, _ctx: &NodeContext) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit horizontal rule elements `<hr>` (async version).
    async fn visit_horizontal_rule(&mut self, _ctx: &NodeContext) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit custom elements (web components) or unknown tags (async version).
    async fn visit_custom_element(&mut self, _ctx: &NodeContext, _tag_name: &str, _html: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit definition list `<dl>` (async version).
    async fn visit_definition_list_start(&mut self, _ctx: &NodeContext) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit definition term `<dt>` (async version).
    async fn visit_definition_term(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit definition description `<dd>` (async version).
    async fn visit_definition_description(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Called after processing a definition list `</dl>` (async version).
    async fn visit_definition_list_end(&mut self, _ctx: &NodeContext, _output: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit form elements `<form>` (async version).
    async fn visit_form(&mut self, _ctx: &NodeContext, _action: Option<&str>, _method: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit input elements `<input>` (async version).
    async fn visit_input(
        &mut self,
        _ctx: &NodeContext,
        _input_type: &str,
        _name: Option<&str>,
        _value: Option<&str>,
    ) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit button elements `<button>` (async version).
    async fn visit_button(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit audio elements `<audio>` (async version).
    async fn visit_audio(&mut self, _ctx: &NodeContext, _src: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit video elements `<video>` (async version).
    async fn visit_video(&mut self, _ctx: &NodeContext, _src: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit iframe elements `<iframe>` (async version).
    async fn visit_iframe(&mut self, _ctx: &NodeContext, _src: Option<&str>) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit details elements `<details>` (async version).
    async fn visit_details(&mut self, _ctx: &NodeContext, _open: bool) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit summary elements `<summary>` (async version).
    async fn visit_summary(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit figure elements `<figure>` (async version).
    async fn visit_figure_start(&mut self, _ctx: &NodeContext) -> VisitResult {
        VisitResult::Continue
    }

    /// Visit figcaption elements `<figcaption>` (async version).
    async fn visit_figcaption(&mut self, _ctx: &NodeContext, _text: &str) -> VisitResult {
        VisitResult::Continue
    }

    /// Called after processing a figure `</figure>` (async version).
    async fn visit_figure_end(&mut self, _ctx: &NodeContext, _output: &str) -> VisitResult {
        VisitResult::Continue
    }
}
