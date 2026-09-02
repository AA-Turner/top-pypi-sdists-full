use hashbrown::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::MutexExt;
use pyo3::types::{PyAny, PyFrame};
use std::env::current_dir;
use std::path::{Component, Path, PathBuf};
use std::sync::Mutex;

/// Session-scoped cache for paths relative to the directory tracing started in.
///
/// The Python code object is held strongly alongside the pointer key.  This
/// prevents pointer reuse from returning metadata for a dead code object while
/// bounding the cache lifetime to the profiler/monitor session.
pub struct FramePathCache {
    pub(super) root: PathBuf,
    pub(super) paths: Mutex<HashMap<usize, (Py<PyAny>, String, bool)>>,
}

impl FramePathCache {
    pub fn new() -> Self {
        Self {
            root: current_dir().expect("Current directory is invalid"),
            paths: Mutex::new(HashMap::new()),
        }
    }

    pub(super) fn frame_path_and_native_eligibility(
        &self,
        frame: &Bound<'_, PyFrame>,
    ) -> Result<(String, usize, bool), PyErr> {
        let py = frame.py();
        let code = frame.getattr(intern!(py, "f_code"))?;
        let code_id = code.as_ptr() as usize;
        let (relative_path, native_eligible) = {
            let mut paths = self
                .paths
                .lock_py_attached(py)
                .expect("frame path cache mutex poisoned");
            match paths.get(&code_id) {
                Some((_, relative_path, native_eligible)) => {
                    (relative_path.clone(), *native_eligible)
                }
                None => {
                    let filename = code
                        .getattr(intern!(py, "co_filename"))?
                        .extract::<String>()?;
                    let relative_path = self.relative_path(&filename);
                    paths.insert(code_id, (code.unbind(), relative_path.clone(), true));
                    (relative_path, true)
                }
            }
        };
        let lineno = frame.getattr(intern!(py, "f_lineno"))?.extract::<usize>()?;
        Ok((
            format!("{}:{}", relative_path, lineno),
            code_id,
            native_eligible,
        ))
    }

    pub fn format_frame_path(&self, frame: &Bound<'_, PyFrame>) -> Result<String, PyErr> {
        Ok(self.frame_path_and_native_eligibility(frame)?.0)
    }

    pub(super) fn mark_native_msgpack_unsupported(&self, py: Python, code_id: usize) {
        if let Some((_, _, native_eligible)) = self
            .paths
            .lock_py_attached(py)
            .expect("frame path cache mutex poisoned")
            .get_mut(&code_id)
        {
            *native_eligible = false;
        }
    }

    /// Format a filename relative to the directory in which tracing started.
    ///
    /// This is kept separate from `format_frame_path` so callers which already
    /// cache immutable code-object metadata do not need to recover `f_code` or
    /// lock the path cache on every event.
    pub fn relative_path(&self, filename: &str) -> String {
        let path = lexical_normalize(Path::new(filename));
        if path.is_absolute() {
            lexical_relative_path(&path, &self.root)
                .unwrap_or(path)
                .display()
                .to_string()
        } else {
            path.display().to_string()
        }
    }
}

/// Normalize `.` and `..` components without touching the filesystem.
///
/// Code filenames do not have to exist, so canonicalization is not an option.
/// This mirrors the lexical behavior Kolo's Python backends get from
/// `os.path.normpath` while keeping Python execution out of monitoring hooks.
pub(super) fn lexical_normalize(path: &Path) -> PathBuf {
    let mut normalized = PathBuf::new();
    let mut rooted = false;

    for component in path.components() {
        match component {
            Component::Prefix(prefix) => normalized.push(prefix.as_os_str()),
            Component::RootDir => {
                normalized.push(Path::new(std::path::MAIN_SEPARATOR_STR));
                rooted = true;
            }
            Component::CurDir => {}
            Component::ParentDir => {
                let can_pop = normalized
                    .file_name()
                    .is_some_and(|name| name != std::ffi::OsStr::new(".."));
                if can_pop {
                    normalized.pop();
                } else if !rooted {
                    normalized.push("..");
                }
            }
            Component::Normal(part) => normalized.push(part),
        }
    }

    if normalized.as_os_str().is_empty() {
        normalized.push(".");
    }
    normalized
}

pub(super) fn path_component_eq(left: Component<'_>, right: Component<'_>) -> bool {
    #[cfg(windows)]
    {
        left.as_os_str()
            .to_string_lossy()
            .eq_ignore_ascii_case(&right.as_os_str().to_string_lossy())
    }
    #[cfg(not(windows))]
    {
        left == right
    }
}

/// Return `path` relative to `root`, or `None` when Windows prefixes differ.
pub(super) fn lexical_relative_path(path: &Path, root: &Path) -> Option<PathBuf> {
    let normalized_root = lexical_normalize(root);
    let path_components: Vec<_> = path.components().collect();
    let root_components: Vec<_> = normalized_root.components().collect();

    if matches!(path_components.first(), Some(Component::Prefix(_)))
        && !matches!(root_components.first(), Some(Component::Prefix(_)))
        || matches!(root_components.first(), Some(Component::Prefix(_)))
            && !matches!(path_components.first(), Some(Component::Prefix(_)))
    {
        return None;
    }
    if let (Some(Component::Prefix(path_prefix)), Some(Component::Prefix(root_prefix))) =
        (path_components.first(), root_components.first())
    {
        if !path_component_eq(
            Component::Prefix(*path_prefix),
            Component::Prefix(*root_prefix),
        ) {
            return None;
        }
    }

    let common = path_components
        .iter()
        .zip(&root_components)
        .take_while(|(left, right)| path_component_eq(**left, **right))
        .count();
    let mut relative = PathBuf::new();
    for component in &root_components[common..] {
        if matches!(component, Component::Normal(_)) {
            relative.push("..");
        }
    }
    for component in &path_components[common..] {
        relative.push(component.as_os_str());
    }
    if relative.as_os_str().is_empty() {
        relative.push(".");
    }
    Some(relative)
}
