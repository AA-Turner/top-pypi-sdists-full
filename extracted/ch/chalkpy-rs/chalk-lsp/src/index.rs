//! Building an [`AstProjectIndex`] for a Chalk project, overlaying the in-memory
//! text of open documents so that go-to-definition and completion see unsaved
//! edits.

use std::collections::HashMap;
use std::io;
use std::path::{Path, PathBuf};
use std::sync::Arc;

use chalk_ast::{AstFileSystem, AstProjectIndex};

/// A filesystem that serves the in-memory text of open documents, falling back
/// to disk for everything else.
struct OverlayFileSystem {
    files: Vec<String>,
    overlay: HashMap<String, String>,
}

impl AstFileSystem for OverlayFileSystem {
    fn read_to_string(&self, path: &str) -> io::Result<String> {
        if let Some(text) = self.overlay.get(&canonical_key(path)) {
            return Ok(text.clone());
        }
        std::fs::read_to_string(path)
    }

    fn all_files(&self) -> io::Result<Vec<String>> {
        Ok(self.files.clone())
    }
}

/// Canonicalize a path for use as an overlay key, falling back to the raw path
/// when the file does not exist on disk (e.g. a brand-new unsaved buffer).
fn canonical_key(path: &str) -> String {
    std::fs::canonicalize(path)
        .map(|p| p.to_string_lossy().to_string())
        .unwrap_or_else(|_| path.to_string())
}

/// Build a fresh AST index for the project rooted at `project_root`, overlaying
/// the given open documents (keyed by absolute file path).
///
/// A fresh index is built per request. That keeps the implementation free of
/// cache-invalidation bugs at the cost of re-walking the project; it is only
/// triggered by explicit user actions (go-to-definition / completion), so the
/// cost is acceptable. The project walk respects `.gitignore` / `.chalkignore`.
pub fn build_project_index(
    project_root: &Path,
    open_docs: &HashMap<String, String>,
) -> Option<AstProjectIndex> {
    let files: Vec<String> = chalk_ignore::get_project_files(project_root, None::<&Path>, &[])
        .ok()?
        .into_iter()
        .filter(|path| path.extension().and_then(|ext| ext.to_str()) == Some("py"))
        .map(|path| path.to_string_lossy().to_string())
        .collect();

    let overlay: HashMap<String, String> = open_docs
        .iter()
        .map(|(path, text)| (canonical_key(path), text.clone()))
        .collect();

    let fs = Arc::new(OverlayFileSystem {
        files: files.clone(),
        overlay,
    });
    AstProjectIndex::with_filesystem(project_root.to_path_buf(), files, fs).ok()
}

/// Build an index from an explicit file list (used by tests and callers that
/// already know the project files).
pub fn build_index_from_files(
    project_root: &Path,
    files: Vec<PathBuf>,
    open_docs: &HashMap<String, String>,
) -> Option<AstProjectIndex> {
    let files: Vec<String> = files
        .into_iter()
        .filter(|path| path.extension().and_then(|ext| ext.to_str()) == Some("py"))
        .map(|path| path.to_string_lossy().to_string())
        .collect();

    let overlay: HashMap<String, String> = open_docs
        .iter()
        .map(|(path, text)| (canonical_key(path), text.clone()))
        .collect();

    let fs = Arc::new(OverlayFileSystem {
        files: files.clone(),
        overlay,
    });
    AstProjectIndex::with_filesystem(project_root.to_path_buf(), files, fs).ok()
}
