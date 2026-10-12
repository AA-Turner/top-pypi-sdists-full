use bstr::Finder;
use once_cell::sync::Lazy;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::PyFrame;

macro_rules! count {
    // Macro magic to find the length of $path
    // https://youtu.be/q6paRBbLgNw?t=4380
    ($($element:expr),*) => {
        [$(count![@SUBSTR; $element]),*].len()
    };
    (@SUBSTR; $_element:expr) => {()};
}

// This macro abstracts away the boilerplate of creating a `Finder` instance from a path fragment.
// Each finder is created lazily with `once_cell::sync::Lazy`.
macro_rules! finder {
    // Create a `Finder` from a path fragment.
    ($name:ident = $path:expr) => {
        static $name: Lazy<Finder> = Lazy::new(|| Finder::new($path));
    };
    // Create a `Finder` from a path fragment at pub scope.
    (pub $name:ident = $path:expr) => {
        pub static $name: Lazy<Finder> = Lazy::new(|| Finder::new($path));
    };
    // Create an array of `Finder`s from path fragments at pub scope.
    (pub $name:ident = $($path:expr),+ $(,)?) => {
        pub static $name: Lazy<[Finder; count!($($path),*)]> = Lazy::new(|| {
            [
                $(Finder::new($path),)+
            ]
        });
    };
}

finder!(FROZEN_FINDER = "<frozen ");
finder!(EXEC_FINDER = "<string>");

#[cfg(target_os = "windows")]
mod windows {
    use bstr::Finder;
    use once_cell::sync::Lazy;
    finder!(pub LIBRARY_FINDERS = "lib\\python", "\\site-packages\\", "\\x64\\lib\\");
    finder!(pub LOWER_PYTHON_FINDER = "\\python\\");
    finder!(pub UPPER_PYTHON_FINDER = "\\Python\\");
    finder!(pub LOWER_LIB_FINDER = "\\lib\\");
    finder!(pub UPPER_LIB_FINDER = "\\Lib\\");
    finder!(pub KOLO_DIR_FINDER = "\\kolo\\");
    /// Every module and subpackage of the kolo package, relative to its directory.
    pub const KOLO_MODULES: [&str; 43] = [
        "__init__.py",
        "__main__.py",
        "_attach.py",
        "_construction.py",
        "_emit_auto.py",
        "_kolotxt.py",
        "_paths.py",
        "_repr_audit.py",
        "build_frame_tree.py",
        "checks.py",
        "cli_mcp_shared.py",
        "config.py",
        "core.py",
        "db.py",
        "emit.py",
        "emit_flat.py",
        "filters\\",
        "git.py",
        "kv.py",
        "mcp_plumbing.py",
        "mcp_server.py",
        "middleware.py",
        "monitoring.py",
        "navigator.py",
        "node.py",
        "open_in_pycharm.py",
        "plugins.py",
        "profiler.py",
        "pth_init.py",
        "pytest_plugin.py",
        "serialize.py",
        "settings.py",
        "sql_overview.py",
        "subtree_flush.py",
        "threads.py",
        "trace.py",
        "trace_build.py",
        "trace_container.py",
        "types.py",
        "upload.py",
        "utils.py",
        "version.py",
        "web\\",
    ];
}
#[cfg(target_os = "windows")]
use windows::*;

#[cfg(not(target_os = "windows"))]
mod not_windows {
    use bstr::Finder;
    use once_cell::sync::Lazy;
    finder!(pub LIBRARY_FINDERS = "lib/python", "lib64/python", "/site-packages/");
    finder!(pub KOLO_DIR_FINDER = "/kolo/");
    /// Every module and subpackage of the kolo package, relative to its directory.
    pub const KOLO_MODULES: [&str; 43] = [
        "__init__.py",
        "__main__.py",
        "_attach.py",
        "_construction.py",
        "_emit_auto.py",
        "_kolotxt.py",
        "_paths.py",
        "_repr_audit.py",
        "build_frame_tree.py",
        "checks.py",
        "cli_mcp_shared.py",
        "config.py",
        "core.py",
        "db.py",
        "emit.py",
        "emit_flat.py",
        "filters/",
        "git.py",
        "kv.py",
        "mcp_plumbing.py",
        "mcp_server.py",
        "middleware.py",
        "monitoring.py",
        "navigator.py",
        "node.py",
        "open_in_pycharm.py",
        "plugins.py",
        "profiler.py",
        "pth_init.py",
        "pytest_plugin.py",
        "serialize.py",
        "settings.py",
        "sql_overview.py",
        "subtree_flush.py",
        "threads.py",
        "trace.py",
        "trace_build.py",
        "trace_container.py",
        "types.py",
        "upload.py",
        "utils.py",
        "version.py",
        "web/",
    ];
}
#[cfg(not(target_os = "windows"))]
use not_windows::*;

/// Check if any library finder matches the filename.
pub fn library_filter(co_filename: &str) -> bool {
    for finder in LIBRARY_FINDERS.iter() {
        if finder.find(co_filename).is_some() {
            return true;
        }
    }
    #[cfg(target_os = "windows")]
    {
        (LOWER_PYTHON_FINDER.find(co_filename).is_some()
            || UPPER_PYTHON_FINDER.find(co_filename).is_some())
            && (LOWER_LIB_FINDER.find(co_filename).is_some()
                || UPPER_LIB_FINDER.find(co_filename).is_some())
    }
    #[cfg(not(target_os = "windows"))]
    false
}

/// Check if the filename is for a frozen module.
pub fn frozen_filter(co_filename: &str) -> bool {
    FROZEN_FINDER.find(co_filename).is_some()
}

/// Check if the filename is for an `exec` call.
pub fn exec_filter(co_filename: &str) -> bool {
    EXEC_FINDER.find(co_filename).is_some()
}

/// Check if the filename is for Kolo code.
pub fn kolo_filter(co_filename: &str) -> bool {
    let needle_len = KOLO_DIR_FINDER.needle().len();
    let mut haystack = co_filename;
    while let Some(index) = KOLO_DIR_FINDER.find(haystack) {
        let rest = &haystack[index + needle_len..];
        if KOLO_MODULES.iter().any(|module| rest.starts_with(module)) {
            return true;
        }
        // The needle starts and ends with a separator, so a match can begin
        // at the separator closing this one (e.g. `/kolo/kolo/core.py`).
        haystack = &haystack[index + needle_len - 1..];
    }
    false
}

fn frame_filename(frame: Bound<'_, PyAny>) -> String {
    let py = frame.py();
    let f_code = frame.getattr("f_code").expect("A frame has a code object.");
    let co_filename = f_code
        .getattr(intern!(py, "co_filename"))
        .expect("A code object has a filename.");
    co_filename
        .extract::<String>()
        .expect("A filename is a string.")
}

pub fn attrs_generated_filter(co_filename: &str) -> bool {
    co_filename.starts_with("<attrs generated")
}

pub fn attrs_filter_monitoring(py: Python, co_filename: &str) -> Result<bool, PyErr> {
    // If filename is not empty, just check if it starts with "<attrs generated"
    // This matches the Python behavior in monitoring.py attrs_filter()
    if !co_filename.is_empty() {
        return Ok(attrs_generated_filter(co_filename));
    }

    // Filename is empty - need to check parent frames for attrs code
    // Wrap in error handling since the call stack may not be deep enough
    let sys = PyModule::import(py, "sys")?;
    let frame_1 = match sys.call_method1("_getframe", (1,)) {
        Ok(frame) => frame,
        Err(_) => return Ok(false), // Stack not deep enough, not attrs code
    };
    let filename = match frame_filename(frame_1) {
        filename if filename.is_empty() => {
            match sys.call_method1("_getframe", (2,)) {
                Ok(frame) => frame_filename(frame),
                Err(_) => return Ok(false), // Stack not deep enough
            }
        }
        filename => filename,
    };

    #[cfg(target_os = "windows")]
    let make_path = "attr\\_make.py";
    #[cfg(not(target_os = "windows"))]
    let make_path = "attr/_make.py";

    Ok(filename.ends_with(make_path))
}

/// Check if we're processing attrs generated code.
pub fn attrs_filter(co_filename: &str, pyframe: &Bound<'_, PyFrame>) -> bool {
    if !co_filename.is_empty() {
        return attrs_generated_filter(co_filename);
    }

    let py = pyframe.py();
    let previous = pyframe
        .getattr(intern!(py, "f_back"))
        .expect("A frame has an `f_back` attribute.");
    if previous.is_none() {
        return false;
    }

    let f_code = previous
        .getattr(intern!(py, "f_code"))
        .expect("A frame has a code object.");
    let co_filename = f_code
        .getattr(intern!(py, "co_filename"))
        .expect("A code object has a filename.");
    let co_filename = co_filename
        .extract::<String>()
        .expect("A filename is a string.");

    #[cfg(target_os = "windows")]
    let make_path = "attr\\_make.py";
    #[cfg(not(target_os = "windows"))]
    let make_path = "attr/_make.py";

    if co_filename.is_empty() {
        let previous = previous
            .getattr(intern!(py, "f_back"))
            .expect("A frame has an `f_back` attribute.");
        if previous.is_none() {
            return false;
        }
        let f_code = previous
            .getattr(intern!(py, "f_code"))
            .expect("A frame has a code object.");
        let co_filename = f_code
            .getattr(intern!(py, "co_filename"))
            .expect("A code object has a filename.");
        let co_filename = co_filename
            .extract::<String>()
            .expect("A filename is a string.");
        co_filename.ends_with(make_path)
    } else {
        co_filename.ends_with(make_path)
    }
}

/// Check if the filename is for pytest generated code.
pub fn pytest_generated_filter(co_filename: &str) -> bool {
    co_filename == "<pytest match expression>"
}

/// Turn a vector of path fragments into a vector of finders.
#[cfg(target_os = "windows")]
pub fn build_finders(paths: Vec<String>) -> Finders {
    Finders {
        finders: paths
            .iter()
            .map(|path| path.replace("/", "\\"))
            .map(|path| Finder::new(&path).into_owned())
            .collect(),
    }
}
#[cfg(not(target_os = "windows"))]
pub fn build_finders(paths: Vec<String>) -> Finders {
    Finders {
        finders: paths
            .iter()
            .map(Finder::new)
            .map(|finder| finder.into_owned())
            .collect(),
    }
}

#[derive(Clone)]
pub struct Finders {
    finders: Vec<Finder<'static>>,
}

impl Finders {
    pub fn check(&self, filename: &str) -> bool {
        self.finders
            .iter()
            .any(|finder| finder.find(filename).is_some())
    }

    /// Whether both match exactly the same path fragments, in order.
    pub fn same_fragments(&self, other: &Finders) -> bool {
        self.finders.len() == other.finders.len()
            && self
                .finders
                .iter()
                .zip(&other.finders)
                .all(|(left, right)| left.needle() == right.needle())
    }
}

/// Check if Kolo's builtin filters exclude this filename.
pub fn default_ignore_frame(py: Python, co_filename: &str) -> Result<bool, PyErr> {
    if library_filter(co_filename)
        || frozen_filter(co_filename)
        || kolo_filter(co_filename)
        || exec_filter(co_filename)
        || pytest_generated_filter(co_filename)
    {
        Ok(true)
    } else {
        attrs_filter_monitoring(py, co_filename)
    }
}

/// Check if a frame from this filename belongs in the trace.
pub fn include_frame(
    py: Python,
    filename: &str,
    include_frames: &Finders,
    ignore_frames: &Finders,
) -> Result<bool, PyErr> {
    Ok(include_frames.check(filename)
        || !(default_ignore_frame(py, filename)? || ignore_frames.check(filename)))
}

/// Construct a vector of Finders for ignore_frames or include_frames.
///
/// `filters` is a Python dictionary loaded from a config dictionary, or None.
/// `key` is `"ignore_frames"` or `"include_frames"`.
pub fn load_filters(filters: &Option<Bound<'_, PyAny>>, key: &str) -> Result<Finders, PyErr> {
    Ok(match filters {
        Some(filters) => match filters.get_item(key) {
            Ok(filters) => build_finders(filters.extract()?),
            Err(_) => Finders {
                finders: Vec::new(),
            },
        },
        None => Finders {
            finders: Vec::new(),
        },
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_attrs_generated_filter() {
        assert!(attrs_generated_filter(
            "<attrs generated repr __main__.Author>"
        ));
        assert!(!attrs_generated_filter("src/example.py"));
    }

    #[test]
    fn test_kolo_filter_matches_core_py() {
        let path = "/some/path/kolo/python/src/kolo/core.py";
        assert!(
            kolo_filter(path),
            "kolo_filter should match kolo/core.py in path: {}",
            path
        );
    }

    #[test]
    fn test_kolo_filter_matches_various_kolo_paths() {
        let paths = vec![
            "/some/path/kolo/core.py",
            "/kolo/config.py",
            "/path/to/kolo/middleware.py",
            "/kolo/profiler.py",
            "/kolo/trace_build.py",
        ];
        for path in paths {
            assert!(kolo_filter(path), "kolo_filter should match path: {}", path);
        }
    }

    #[test]
    fn test_kolo_filter_matches_trace_container_reader() {
        #[cfg(target_os = "windows")]
        let path = r"C:\some\path\kolo\trace_container.py";
        #[cfg(not(target_os = "windows"))]
        let path = "/some/path/kolo/trace_container.py";

        assert!(kolo_filter(path));
    }

    /// Every module of the kolo package must be filtered: Kolo's own code
    /// (e.g. the auto-emit lock check its save thread runs) must never be
    /// recorded into a user's trace.
    #[test]
    fn test_kolo_filter_matches_every_kolo_module() {
        fn python_files(dir: &std::path::Path, files: &mut Vec<std::path::PathBuf>) {
            for entry in std::fs::read_dir(dir).expect("kolo package dir is readable") {
                let path = entry.expect("dir entry").path();
                if path.is_dir() {
                    python_files(&path, files);
                } else if path.extension().is_some_and(|ext| ext == "py") {
                    files.push(path);
                }
            }
        }
        let package_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("..")
            .join("src")
            .join("kolo");
        let mut files = Vec::new();
        python_files(&package_dir, &mut files);
        assert!(files.len() > 30, "found only {} kolo modules", files.len());
        let missing: Vec<_> = files
            .iter()
            .map(|path| path.to_str().expect("utf-8 path").to_string())
            .filter(|path| !kolo_filter(path))
            .collect();
        assert!(missing.is_empty(), "add these to KOLO_MODULES: {missing:?}");
    }

    #[test]
    fn test_kolo_filter_does_not_match_user_code() {
        let paths = vec![
            "/Users/user/myapp/views.py",
            "/path/to/myproject/models.py",
            "/some/random/file.py",
        ];
        for path in paths {
            assert!(
                !kolo_filter(path),
                "kolo_filter should NOT match path: {}",
                path
            );
        }
    }
}
