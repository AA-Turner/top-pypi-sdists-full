use std::collections::{hash_map::Entry, HashMap};
use std::path::{Component, Path, PathBuf};
use std::str::FromStr;

use lsp_types::{Diagnostic, InitializeParams, Uri};

use crate::diagnostics;

#[derive(Clone)]
pub struct OpenDoc {
    pub uri: Uri,
    text: String,
    revision: u64,
}

pub struct ExternalFileDiagnostics {
    pub uri: Uri,
    pub uri_key: String,
    pub diagnostics: Vec<Diagnostic>,
}

#[derive(Clone, Debug)]
pub struct PathScope {
    path: PathBuf,
    is_dir: bool,
}

impl PathScope {
    pub fn from_paths(project_root: &Path, paths: &[PathBuf]) -> Vec<Self> {
        paths
            .iter()
            .map(|path| {
                let absolute = if path.is_absolute() {
                    path.to_path_buf()
                } else {
                    project_root.join(path)
                };
                Self {
                    path: absolute
                        .canonicalize()
                        .unwrap_or_else(|_| normalize_lexically(&absolute)),
                    is_dir: absolute.is_dir(),
                }
            })
            .collect()
    }

    pub fn contains(&self, project_root: &Path, path: &Path) -> bool {
        let absolute = if path.is_absolute() {
            path.to_path_buf()
        } else {
            project_root.join(path)
        };
        let path = absolute
            .canonicalize()
            .unwrap_or_else(|_| normalize_lexically(&absolute));
        if self.is_dir {
            path.starts_with(&self.path)
        } else {
            path == self.path
        }
    }
}

pub struct ProjectState {
    workspace_roots: Vec<PathBuf>,
    local_diagnostics_enabled: bool,
    open_docs: HashMap<String, OpenDoc>,
    builtin_diagnostics: HashMap<String, Vec<Diagnostic>>,
    cheapo_diagnostics: HashMap<String, ExternalFileDiagnostics>,
    external_diagnostics: HashMap<String, ExternalFileDiagnostics>,
    latest_cheapo_run_id: u64,
    latest_external_run_id: u64,
}

impl ProjectState {
    pub fn new(params: &InitializeParams, local_diagnostics_enabled: bool) -> Self {
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
                params
                    .root_uri
                    .as_ref()
                    .and_then(uri_to_file_path)
                    .map(|p| vec![p])
            })
            .unwrap_or_default();

        Self {
            workspace_roots,
            local_diagnostics_enabled,
            open_docs: HashMap::new(),
            builtin_diagnostics: HashMap::new(),
            cheapo_diagnostics: HashMap::new(),
            external_diagnostics: HashMap::new(),
            latest_cheapo_run_id: 0,
            latest_external_run_id: 0,
        }
    }

    pub fn on_open(&mut self, uri: Uri, text: String) {
        let key = uri.as_str().to_string();
        let revision = self.next_doc_revision(&key);
        self.open_docs.insert(
            key,
            OpenDoc {
                uri: uri.clone(),
                text,
                revision,
            },
        );
        self.refresh_builtin_diagnostics(&uri);
    }

    pub fn on_change(&mut self, uri: Uri, text: String) {
        let key = uri.as_str().to_string();
        let revision = self.next_doc_revision(&key);
        self.open_docs.insert(
            key,
            OpenDoc {
                uri: uri.clone(),
                text,
                revision,
            },
        );
        self.refresh_builtin_diagnostics(&uri);
    }

    pub fn on_save(&mut self, uri: Uri, text: Option<String>) {
        let key = uri.as_str().to_string();
        if let Some(doc) = self.open_docs.get_mut(&key) {
            if let Some(text) = text {
                doc.text = text;
            }
            doc.revision += 1;
        } else if let Some(text) = text {
            self.open_docs.insert(
                key,
                OpenDoc {
                    uri: uri.clone(),
                    text,
                    revision: 1,
                },
            );
        }
        self.refresh_builtin_diagnostics(&uri);
    }

    pub fn on_close(&mut self, uri: &Uri) {
        self.open_docs.remove(uri.as_str());
        self.builtin_diagnostics.remove(uri.as_str());
        self.cheapo_diagnostics.remove(uri.as_str());
    }

    pub fn document_text(&self, uri: &Uri) -> Option<&str> {
        self.open_docs
            .get(uri.as_str())
            .map(|doc| doc.text.as_str())
    }

    /// All open documents that map to a file path, keyed by absolute file path.
    /// Used to overlay unsaved edits onto the project AST index.
    pub fn open_documents_by_path(&self) -> HashMap<String, String> {
        self.open_docs
            .values()
            .filter_map(|doc| {
                let path = uri_to_file_path(&doc.uri)?;
                Some((path.to_string_lossy().to_string(), doc.text.clone()))
            })
            .collect()
    }

    pub fn open_file_paths_for_project(&self, project_root: &Path) -> Vec<PathBuf> {
        let mut paths: Vec<PathBuf> = self
            .open_docs
            .values()
            .filter_map(|doc| uri_to_file_path(&doc.uri))
            .filter(|path| self.project_root_for(path).as_deref() == Some(project_root))
            .collect();
        paths.sort();
        paths.dedup();
        paths
    }

    pub fn workspace_roots(&self) -> &[PathBuf] {
        &self.workspace_roots
    }

    pub fn project_root_for(&self, file_path: &Path) -> Option<PathBuf> {
        let mut dir = file_path.parent();
        while let Some(d) = dir {
            if has_chalk_config(d) {
                return Some(d.to_path_buf());
            }
            dir = d.parent();
        }
        None
    }

    pub fn merged_diagnostics(&self, uri: &Uri) -> Vec<Diagnostic> {
        let key = uri.as_str();
        let mut diagnostics = Vec::new();
        diagnostics.extend(
            self.builtin_diagnostics
                .get(key)
                .cloned()
                .unwrap_or_default(),
        );
        if let Some(cheapo) = self.cheapo_diagnostics.get(key) {
            diagnostics.extend(cheapo.diagnostics.clone());
        }
        if let Some(external) = self.external_diagnostics.get(key) {
            diagnostics.extend(external.diagnostics.clone());
        }
        diagnostics
    }

    pub fn set_local_diagnostics_enabled(&mut self, enabled: bool) -> Vec<Uri> {
        if self.local_diagnostics_enabled == enabled {
            return Vec::new();
        }

        self.local_diagnostics_enabled = enabled;
        let mut affected_uris: Vec<Uri> = self
            .open_docs
            .values()
            .map(|document| document.uri.clone())
            .collect();
        if enabled {
            for uri in &affected_uris {
                self.refresh_builtin_diagnostics(uri);
            }
        } else {
            self.builtin_diagnostics.clear();
        }
        affected_uris.sort();
        affected_uris
    }

    pub fn start_cheapo_run(&mut self) -> u64 {
        self.latest_cheapo_run_id += 1;
        self.latest_cheapo_run_id
    }

    pub fn invalidate_cheapo_runs(&mut self) {
        self.latest_cheapo_run_id += 1;
    }

    pub fn is_current_cheapo_run(&self, run_id: u64) -> bool {
        run_id == self.latest_cheapo_run_id
    }

    pub fn replace_cheapo_diagnostics(&mut self, files: Vec<ExternalFileDiagnostics>) -> Vec<Uri> {
        let mut affected_by_key: HashMap<String, Uri> = self
            .cheapo_diagnostics
            .values()
            .map(|file| (file.uri_key.clone(), file.uri.clone()))
            .collect();

        let mut new_cheapo_diagnostics: HashMap<String, ExternalFileDiagnostics> = HashMap::new();
        for file in files {
            let uri_key = file.uri_key.clone();
            affected_by_key
                .entry(uri_key.clone())
                .or_insert_with(|| file.uri.clone());
            match new_cheapo_diagnostics.entry(uri_key) {
                Entry::Occupied(mut entry) => {
                    entry.get_mut().diagnostics.extend(file.diagnostics);
                }
                Entry::Vacant(entry) => {
                    entry.insert(file);
                }
            }
        }

        self.cheapo_diagnostics = new_cheapo_diagnostics;

        let mut affected_uris: Vec<Uri> = affected_by_key.into_values().collect();
        affected_uris.sort();
        affected_uris
    }

    pub fn start_external_run(&mut self) -> u64 {
        self.latest_external_run_id += 1;
        self.latest_external_run_id
    }

    pub fn invalidate_external_runs(&mut self) {
        self.latest_external_run_id += 1;
    }

    pub fn is_current_external_run(&self, run_id: u64) -> bool {
        run_id == self.latest_external_run_id
    }

    pub fn replace_external_diagnostics(
        &mut self,
        files: Vec<ExternalFileDiagnostics>,
    ) -> Vec<Uri> {
        let mut affected_by_key: HashMap<String, Uri> = self
            .external_diagnostics
            .values()
            .map(|file| (file.uri_key.clone(), file.uri.clone()))
            .collect();

        let mut new_external_diagnostics: HashMap<String, ExternalFileDiagnostics> = HashMap::new();
        for file in files {
            let uri_key = file.uri_key.clone();
            affected_by_key
                .entry(uri_key.clone())
                .or_insert_with(|| file.uri.clone());
            match new_external_diagnostics.entry(uri_key) {
                Entry::Occupied(mut entry) => {
                    entry.get_mut().diagnostics.extend(file.diagnostics);
                }
                Entry::Vacant(entry) => {
                    entry.insert(file);
                }
            }
        }

        self.external_diagnostics = new_external_diagnostics;

        let mut affected_uris: Vec<Uri> = affected_by_key.into_values().collect();
        affected_uris.sort();
        affected_uris
    }

    fn refresh_builtin_diagnostics(&mut self, uri: &Uri) {
        let key = uri.as_str().to_string();
        if !self.local_diagnostics_enabled {
            self.builtin_diagnostics.remove(&key);
            return;
        }
        let diagnostics = self.compute_builtin_diagnostics(uri);
        self.builtin_diagnostics.insert(key, diagnostics);
    }

    fn compute_builtin_diagnostics(&self, uri: &Uri) -> Vec<Diagnostic> {
        let Some(doc) = self.open_docs.get(uri.as_str()) else {
            return Vec::new();
        };
        let Some(file_path) = uri_to_file_path(uri) else {
            return Vec::new();
        };

        let project_root = self.project_root_for(&file_path);
        diagnostics::lint(project_root.as_deref(), &file_path, &doc.text)
    }

    fn next_doc_revision(&self, key: &str) -> u64 {
        self.open_docs
            .get(key)
            .map(|doc| doc.revision + 1)
            .unwrap_or(1)
    }
}

fn has_chalk_config(dir: &Path) -> bool {
    chalk_project::PROJECT_CONFIG_FILENAMES
        .iter()
        .any(|name| dir.join(name).is_file())
}

fn normalize_lexically(path: &Path) -> PathBuf {
    let mut normalized = PathBuf::new();
    for component in path.components() {
        match component {
            Component::CurDir => {}
            Component::ParentDir => {
                normalized.pop();
            }
            Component::Prefix(_) | Component::RootDir | Component::Normal(_) => {
                normalized.push(component.as_os_str());
            }
        }
    }
    normalized
}

pub fn uri_to_file_path(uri: &Uri) -> Option<PathBuf> {
    let s = uri.as_str();
    if let Some(rest) = s.strip_prefix("file://") {
        let decoded = percent_decode(rest);
        Some(PathBuf::from(decoded))
    } else {
        None
    }
}

pub fn path_to_file_uri(path: &Path) -> Option<Uri> {
    let path = if path.is_absolute() {
        path.to_path_buf()
    } else {
        std::env::current_dir().ok()?.join(path)
    };
    let path = path.to_str()?;
    Uri::from_str(&format!("file://{}", percent_encode_path(path))).ok()
}

fn percent_decode(s: &str) -> String {
    let mut out = Vec::with_capacity(s.len());
    let bytes = s.as_bytes();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'%' && i + 2 < bytes.len() {
            let hi = (bytes[i + 1] as char).to_digit(16);
            let lo = (bytes[i + 2] as char).to_digit(16);
            if let (Some(h), Some(l)) = (hi, lo) {
                out.push((h * 16 + l) as u8);
                i += 3;
                continue;
            }
        }
        out.push(bytes[i]);
        i += 1;
    }
    String::from_utf8_lossy(&out).into_owned()
}

fn percent_encode_path(path: &str) -> String {
    let mut out = String::with_capacity(path.len());
    for b in path.as_bytes() {
        match b {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'/' | b'-' | b'.' | b'_' | b'~' => {
                out.push(*b as char)
            }
            _ => out.push_str(&format!("%{b:02X}")),
        }
    }
    out
}
