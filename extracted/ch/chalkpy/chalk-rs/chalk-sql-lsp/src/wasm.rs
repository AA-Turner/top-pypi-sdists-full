#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

/// A SQL analysis session for use from JavaScript/WASM.
///
/// Holds the current document text and provides LSP-like operations
/// that return JSON strings.
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub struct SqlSession {
    text: String,
}

#[cfg(feature = "wasm")]
#[wasm_bindgen]
impl SqlSession {
    #[wasm_bindgen(constructor)]
    pub fn new() -> SqlSession {
        SqlSession {
            text: String::new(),
        }
    }

    /// Update the document text and return diagnostics as a JSON array.
    pub fn update_text(&mut self, text: &str) -> String {
        self.text = text.to_string();
        let diags = crate::diagnostics::diagnostics(&self.text);
        serde_json::to_string(&diags).unwrap_or_else(|_| "[]".to_string())
    }

    /// Get completions at the given 0-based line/column. Returns JSON array.
    pub fn completions(&self, line: u32, col: u32) -> String {
        let items = crate::completions::completions(&self.text, line, col);
        serde_json::to_string(&items).unwrap_or_else(|_| "[]".to_string())
    }

    /// Get hover info at the given 0-based line/column. Returns JSON or null.
    pub fn hover(&self, line: u32, col: u32) -> Option<String> {
        let h = crate::hover::hover(&self.text, line, col)?;
        serde_json::to_string(&h).ok()
    }

    /// Get signature help at the given 0-based line/column. Returns JSON or null.
    pub fn signature_help(&self, line: u32, col: u32) -> Option<String> {
        let sh = crate::signature_help::signature_help(&self.text, line, col)?;
        serde_json::to_string(&sh).ok()
    }
}
