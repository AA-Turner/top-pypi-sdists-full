use std::collections::HashMap;
use std::path::{Path, PathBuf};

use lsp_types::{Diagnostic, InitializeParams, Uri};

use crate::diagnostics;

pub struct ProjectState {
    workspace_roots: Vec<PathBuf>,
    open_docs: HashMap<String, String>,
}

impl ProjectState {
    pub fn new(params: &InitializeParams) -> Self {
        let workspace_roots: Vec<PathBuf> = params
            .workspace_folders
            .as_ref()
            .map(|folders| {
                folders
                    .iter()
                    .filter_map(|f| uri_to_file_path(&f.uri))
                    .collect()
            })
            .or_else(|| {
                #[allow(deprecated)]
                params.root_uri.as_ref().and_then(|u| uri_to_file_path(u)).map(|p| vec![p])
            })
            .unwrap_or_default();

        Self {
            workspace_roots,
            open_docs: HashMap::new(),
        }
    }

    pub fn on_open(&mut self, uri: Uri, text: String) {
        self.open_docs.insert(uri.as_str().to_string(), text);
    }

    pub fn on_change(&mut self, uri: Uri, text: String) {
        self.open_docs.insert(uri.as_str().to_string(), text);
    }

    pub fn on_close(&mut self, uri: &Uri) {
        self.open_docs.remove(uri.as_str());
    }

    pub fn diagnostics(&self, uri: &Uri) -> Vec<Diagnostic> {
        let Some(text) = self.open_docs.get(uri.as_str()) else {
            return Vec::new();
        };

        let Some(file_path) = uri_to_file_path(uri) else {
            return Vec::new();
        };

        let project_root = self.project_root_for(&file_path);
        diagnostics::lint(project_root.as_deref(), &file_path, text)
    }

    fn project_root_for(&self, file_path: &Path) -> Option<PathBuf> {
        for root in &self.workspace_roots {
            if file_path.starts_with(root) && has_chalk_config(root) {
                return Some(root.clone());
            }
        }
        let mut dir = file_path.parent();
        while let Some(d) = dir {
            if has_chalk_config(d) {
                return Some(d.to_path_buf());
            }
            dir = d.parent();
        }
        None
    }
}

fn has_chalk_config(dir: &Path) -> bool {
    chalk_project::PROJECT_CONFIG_FILENAMES
        .iter()
        .any(|name| dir.join(name).is_file())
}

/// Extract a filesystem path from a `file://` URI.
fn uri_to_file_path(uri: &Uri) -> Option<PathBuf> {
    let s = uri.as_str();
    if let Some(rest) = s.strip_prefix("file://") {
        // Decode percent-encoded characters.
        let decoded = percent_decode(rest);
        Some(PathBuf::from(decoded))
    } else {
        None
    }
}

fn percent_decode(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    let mut bytes = s.bytes();
    while let Some(b) = bytes.next() {
        if b == b'%' {
            let hi = bytes.next().and_then(|c| (c as char).to_digit(16));
            let lo = bytes.next().and_then(|c| (c as char).to_digit(16));
            if let (Some(h), Some(l)) = (hi, lo) {
                out.push((h * 16 + l) as u8 as char);
            }
        } else {
            out.push(b as char);
        }
    }
    out
}
