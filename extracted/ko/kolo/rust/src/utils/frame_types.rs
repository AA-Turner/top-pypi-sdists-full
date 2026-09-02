use hashbrown::HashMap;
use pyo3::exceptions::{PyAttributeError, PyKeyError};
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyFrame, PyType};
#[cfg(test)]
use std::env::current_dir;
#[cfg(test)]
use std::path::Path;
use std::time::SystemTime;
use ulid::Ulid;

use super::frame_writer::{build_user_code_call_site, UserCodeCallSite};
use super::msgpack_encoding::{write_assign_tuple, write_f64_pair, write_str_pair};
use super::value_serializer::Serializer;

pub(super) fn module_name_from_globals<'py>(
    globals: &Bound<'py, PyAny>,
    py: Python<'py>,
) -> Bound<'py, PyAny> {
    let module = match globals.cast_exact::<PyDict>() {
        Ok(globals) => globals.get_item(intern!(py, "__name__")).ok().flatten(),
        Err(_) => globals.get_item("__name__").ok(),
    };
    module.unwrap_or_else(|| "<unknown>".into_pyobject(py).unwrap().into_any())
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Event {
    Call,
    Return,
    Unwind,
    Resume,
    Yield,
    Throw,
}

impl From<Event> for &str {
    fn from(event: Event) -> Self {
        match event {
            Event::Call => "call",
            Event::Return => "return",
            Event::Unwind => "unwind",
            Event::Resume => "resume",
            Event::Yield => "yield",
            Event::Throw => "throw",
        }
    }
}

#[derive(Clone)]
pub enum Arg<'a, 'py> {
    None,
    Argument(&'a Bound<'py, PyAny>),
    Exception(&'a Bound<'py, PyAny>),
}

impl<'a, 'py> Arg<'a, 'py> {
    pub fn into_inner(self, py: Python) -> Py<PyAny> {
        match self {
            Self::None => py.None().into_any(),
            Self::Argument(arg) => arg.clone().unbind(),
            Self::Exception(exception) => exception.clone().unbind(),
        }
    }
}

#[derive(Default)]
pub struct CallFrames {
    frames: Vec<(Py<PyAny>, String)>,
}

impl CallFrames {
    pub fn get_bound<'py>(&self, py: Python<'py>) -> Vec<(Bound<'py, PyAny>, String)> {
        self.frames
            .iter()
            .map(|(frame, frame_id)| (frame.bind(py).clone(), frame_id.clone()))
            .collect()
    }

    pub fn get_user_code_call_site(
        &mut self,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        frame_id: &str,
    ) -> Result<Option<UserCodeCallSite>, PyErr> {
        let py = pyframe.py();
        let user_code_call_site = match self
            .frames
            .iter()
            .rev()
            .take(2)
            .find(|(_frame, call_frame_id)| call_frame_id != frame_id)
        {
            Some((call_frame, call_frame_id)) => {
                build_user_code_call_site(call_frame.bind(py), call_frame_id)?
            }
            None => None,
        };
        self.update_call_frames(event, pyframe, frame_id);
        Ok(user_code_call_site)
    }

    fn update_call_frames(&mut self, event: Event, frame: &Bound<'_, PyAny>, frame_id: &str) {
        match (event, frame_id) {
            (Event::Call | Event::Resume | Event::Throw, frame_id) => {
                self.frames
                    .push((frame.clone().into(), frame_id.to_string()));
            }
            (Event::Return | Event::Unwind | Event::Yield, _) => {
                self.frames.pop();
            }
        }
    }
}

#[derive(Default)]
pub struct FrameIds {
    frame_ids: HashMap<usize, String>,
}

impl FrameIds {
    fn set(&mut self, pyframe_id: usize) -> String {
        let frame_id = frame_id();
        self.frame_ids.insert(pyframe_id, frame_id.clone());
        frame_id
    }

    fn get(&self, pyframe_id: usize) -> String {
        match self.frame_ids.get(&pyframe_id) {
            Some(frame_id) => frame_id.clone(),
            None => frame_id(),
        }
    }

    pub fn get_option(&self, pyframe_id: usize) -> Option<String> {
        self.frame_ids.get(&pyframe_id).cloned()
    }

    pub fn get_or_set(&mut self, event: Event, pyframe_id: usize) -> String {
        match event {
            Event::Call | Event::Resume | Event::Throw => self.set(pyframe_id),
            Event::Return | Event::Unwind | Event::Yield => self.get(pyframe_id),
        }
    }
}

pub struct LineFrame {
    path: String,
    co_name: String,
    qualname: String,
    frame_id: Option<String>,
    timestamp: f64,
}

impl LineFrame {
    pub fn new(
        path: String,
        co_name: String,
        qualname: String,
        frame_id: Option<String>,
        timestamp: f64,
    ) -> Self {
        Self {
            path,
            co_name,
            qualname,
            frame_id,
            timestamp,
        }
    }
    pub fn write_msgpack_into(
        &self,
        buf: &mut Vec<u8>,
        serializer: &Serializer,
        assign: (&str, Bound<'_, PyAny>),
        lightweight_repr: bool,
    ) -> Result<(), PyErr> {
        rmp::encode::write_map_len(buf, 8).expect("Writing to memory, not I/O");
        write_str_pair(buf, "path", Some(&self.path));
        write_str_pair(buf, "co_name", Some(&self.co_name));
        write_str_pair(buf, "qualname", Some(&self.qualname));
        write_str_pair(buf, "event", Some("line"));
        write_str_pair(buf, "frame_id", self.frame_id.as_deref());
        write_f64_pair(buf, "timestamp", self.timestamp);
        write_str_pair(buf, "type", Some("frame"));
        write_assign_tuple(buf, serializer, assign, lightweight_repr)?;
        Ok(())
    }
}

/// A unix timestamp for the current time.
pub fn timestamp() -> f64 {
    SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .expect("System time is before unix epoch")
        .as_secs_f64()
}

/// Create a Kolo frame_id from a ulid.
pub fn frame_id() -> String {
    let frame_ulid = Ulid::new();
    format!("frm_{}", frame_ulid.to_string())
}

/// Create a Kolo trace_id from a ulid.
pub fn trace_id() -> String {
    let trace_ulid = Ulid::new();
    format!("trc_{}", trace_ulid.to_string())
}

/// Read the filename and current line number from a Python frame object.
#[cfg(test)]
pub fn filename_with_lineno(
    frame: &Bound<'_, PyFrame>,
    py: Python,
) -> Result<(String, usize), PyErr> {
    let f_code = frame.getattr(intern!(py, "f_code"))?;
    let co_filename = f_code.getattr(intern!(py, "co_filename"))?;
    let filename = co_filename.extract::<String>()?;
    let lineno = frame.getattr(intern!(py, "f_lineno"))?.extract()?;
    Ok((filename, lineno))
}

/// Combine a filename and line number into Kolo's standard format.
#[cfg(test)]
pub fn format_frame_path(filename: &str, lineno: usize) -> String {
    let path = Path::new(filename);
    let dir = current_dir().expect("Current directory is invalid");
    let relative_path = match path.strip_prefix(&dir) {
        Ok(relative_path) => relative_path,
        Err(_) => path,
    };
    format!("{}:{}", relative_path.display(), lineno)
}

/// Get the qualname for the Python object represented by the frame.
///
/// Equivalent to `kolo.profiler.get_qualname`.
pub fn get_qualname(frame: &Bound<'_, PyFrame>, py: Python) -> Result<Option<String>, PyErr> {
    let f_code = frame.getattr(intern!(py, "f_code"))?;
    // Read `co_qualname` on modern Python versions.
    match f_code.getattr(intern!(py, "co_qualname")) {
        Ok(qualname) => {
            let globals = frame.getattr(intern!(py, "f_globals"))?;
            let module = module_name_from_globals(&globals, py);
            return Ok(Some(format!("{}.{}", module, qualname)));
        }
        Err(err) if err.is_instance_of::<PyAttributeError>(py) => {}
        Err(err) => return Err(err),
    }

    let co_name = f_code.getattr(intern!(py, "co_name"))?;
    let name = co_name.extract::<String>()?;
    // Special case for module objects
    if name.as_str() == "<module>" {
        let globals = frame.getattr(intern!(py, "f_globals"))?;
        let module = module_name_from_globals(&globals, py);
        return Ok(Some(format!("{}.<module>", module)));
    }

    // Fallback handling for legacy Python versions without `co_qualname`.
    match _get_qualname_inner(frame, py, &co_name) {
        Ok(qualname) => Ok(qualname),
        Err(_) => Ok(None),
    }
}

/// Get the live module name used to qualify cached `code.co_qualname`.
///
/// The module name deliberately remains a live frame-global lookup: the same
/// code object can be executed by functions with different globals mappings.
pub fn get_qualname_module<'py>(
    frame: &Bound<'py, PyFrame>,
    py: Python<'py>,
) -> Result<Bound<'py, PyAny>, PyErr> {
    let globals = frame.getattr(intern!(py, "f_globals"))?;
    Ok(module_name_from_globals(&globals, py))
}

fn _get_qualname_inner(
    frame: &Bound<'_, PyFrame>,
    py: Python,
    co_name: &Bound<'_, PyAny>,
) -> Result<Option<String>, PyErr> {
    let outer_frame = frame.getattr(intern!(py, "f_back"))?;
    if outer_frame.is_none() {
        return Ok(None);
    }

    let outer_frame_locals = outer_frame.getattr(intern!(py, "f_locals"))?;
    match outer_frame_locals.get_item(co_name) {
        Ok(function) => {
            let module = function.getattr(intern!(py, "__module__"))?;
            let qualname = function.getattr(intern!(py, "__qualname__"))?;
            return Ok(Some(format!("{}.{}", module, qualname)));
        }
        Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
        Err(_) => return Ok(None),
    }

    let locals = frame.getattr(intern!(py, "f_locals"))?;
    let inspect = PyModule::import(py, "inspect")?;
    let getattr_static = inspect.getattr(intern!(py, "getattr_static"))?;
    match locals.get_item("self") {
        Ok(locals_self) => {
            let function = getattr_static.call1((locals_self, co_name))?;
            let builtins = py.import("builtins")?;
            let property = builtins.getattr(intern!(py, "property"))?;
            let property = property.downcast()?;
            let function = match function.is_instance(property)? {
                true => function.getattr(intern!(py, "fget"))?,
                false => function,
            };
            let module = function.getattr(intern!(py, "__module__"))?;
            let qualname = function.getattr(intern!(py, "__qualname__"))?;
            return Ok(Some(format!("{}.{}", module, qualname)));
        }
        Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
        Err(_) => return Ok(None),
    };

    match locals.get_item("cls") {
        Ok(cls) if cls.is_instance_of::<PyType>() => {
            let function = getattr_static.call1((cls, co_name))?;
            let module = function.getattr(intern!(py, "__module__"))?;
            let qualname = function.getattr(intern!(py, "__qualname__"))?;
            return Ok(Some(format!("{}.{}", module, qualname)));
        }
        Ok(_) => {}
        Err(err) if err.is_instance_of::<PyKeyError>(py) => {}
        Err(_) => return Ok(None),
    }
    let globals = frame.getattr(intern!(py, "f_globals"))?;
    match locals.get_item("__qualname__") {
        Ok(qualname) => {
            let module = module_name_from_globals(&globals, py);
            Ok(Some(format!("{}.{}", module, qualname)))
        }
        Err(err) if err.is_instance_of::<PyKeyError>(py) => {
            let function = globals.get_item(co_name)?;
            let module = function.getattr(intern!(py, "__module__"))?;
            let qualname = function.getattr(intern!(py, "__qualname__"))?;
            Ok(Some(format!("{}.{}", module, qualname)))
        }
        Err(_) => Ok(None),
    }
}
