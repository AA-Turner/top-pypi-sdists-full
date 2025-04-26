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
    finder!(pub KOLO_FINDERS = "\\kolo\\config.py",
        "\\kolo\\db.py",
        "\\kolo\\django_schema.py",
        "\\kolo\\filters\\",
        "\\kolo\\generate_tests\\",
        "\\kolo\\git.py",
        "\\kolo\\__init__.py",
        "\\kolo\\__main__.py",
        "\\kolo\\middleware.py",
        "\\kolo\\monitoring.py",
        "\\kolo\\plugins.py",
        "\\kolo\\profiler.py",
        "\\kolo\\pytest_plugin.py",
        "\\kolo\\serialize.py",
        "\\kolo\\utils.py",
        "\\kolo\\version.py");
}
#[cfg(target_os = "windows")]
use windows::*;

#[cfg(not(target_os = "windows"))]
mod not_windows {
    use bstr::Finder;
    use once_cell::sync::Lazy;
    finder!(pub LIBRARY_FINDERS = "lib/python", "lib64/python", "/site-packages/");
    finder!(pub KOLO_FINDERS = "/kolo/config.py",
        "/kolo/db.py",
        "/kolo/django_schema.py",
        "/kolo/filters/",
        "/kolo/generate_tests/",
        "/kolo/git.py",
        "/kolo/__init__.py",
        "/kolo/__main__.py",
        "/kolo/middleware.py",
        "/kolo/monitoring.py",
        "/kolo/plugins.py",
        "/kolo/profiler.py",
        "/kolo/pytest_plugin.py",
        "/kolo/serialize.py",
        "/kolo/utils.py",
        "/kolo/version.py");
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
    KOLO_FINDERS
        .iter()
        .any(|finder| finder.find(co_filename).is_some())
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

pub fn attrs_filter_monitoring(py: Python, co_filename: &str) -> Result<bool, PyErr> {
    if co_filename.starts_with("<attrs generated") {
        return Ok(true);
    }

    let sys = PyModule::import_bound(py, "sys")?;
    let frame_1 = sys.call_method1("_getframe", (1,))?;
    let filename = match frame_filename(frame_1) {
        filename if filename.is_empty() => {
            let frame_2 = sys.call_method1("_getframe", (2,))?;
            frame_filename(frame_2)
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
    if co_filename.starts_with("<attrs generated") {
        return true;
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

pub struct Finders {
    finders: Vec<Finder<'static>>,
}

impl Finders {
    pub fn check(&self, filename: &str) -> bool {
        self.finders
            .iter()
            .any(|finder| finder.find(filename).is_some())
    }
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
