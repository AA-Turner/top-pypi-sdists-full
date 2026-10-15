use hashbrown::{HashMap, HashSet};
use pyo3::exceptions::{PyAttributeError, PyKeyError};
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyFrame, PyString, PyType};
#[cfg(test)]
use std::env::current_dir;
use std::ops::Deref;
#[cfg(test)]
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::time::SystemTime;
use ulid::Ulid;

use super::frame_path::{format_path_with_line, frame_line_number, CodeLines, FramePathCache};
use super::frame_writer::{build_user_code_call_site, UserCodeCallSite};
use super::msgpack_encoding::{
    write_assign_tuple, write_f64_pair, write_frame_path_pair, write_str_pair,
};
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

const FRAME_ID_PREFIX: &[u8; 4] = b"frm_";
const FRAME_ID_LEN: usize = FRAME_ID_PREFIX.len() + ulid::ULID_LEN;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) struct FrameId([u8; FRAME_ID_LEN]);

impl FrameId {
    fn new() -> Self {
        let mut bytes = [0; FRAME_ID_LEN];
        bytes[..FRAME_ID_PREFIX.len()].copy_from_slice(FRAME_ID_PREFIX);
        let mut ulid = [0; ulid::ULID_LEN];
        Ulid::new().array_to_str(&mut ulid);
        bytes[FRAME_ID_PREFIX.len()..].copy_from_slice(&ulid);
        Self(bytes)
    }

    #[cfg(test)]
    pub(super) fn from_str(frame_id: &str) -> Self {
        Self(
            frame_id
                .as_bytes()
                .try_into()
                .expect("Kolo frame IDs have a fixed length"),
        )
    }

    pub(crate) fn as_str(&self) -> &str {
        // Values are either generated from ASCII constants or copied from a valid `str`.
        unsafe { std::str::from_utf8_unchecked(&self.0) }
    }
}

impl Deref for FrameId {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        self.as_str()
    }
}

#[derive(Default)]
pub struct CallFrames {
    frames: Vec<(Py<PyAny>, FrameId, Option<Arc<CodeLines>>)>,
}

impl CallFrames {
    pub fn snapshot_call_site_frames<'py>(
        &self,
        py: Python<'py>,
    ) -> Vec<(Bound<'py, PyAny>, String)> {
        // Plugin attribution only examines the last two frames. Keep them owned so
        // plugin processing can release the GIL or re-enter without borrowing this stack.
        self.frames[self.frames.len().saturating_sub(2)..]
            .iter()
            .map(|(frame, frame_id, _)| (frame.bind(py).clone(), frame_id.as_str().to_owned()))
            .collect()
    }

    pub fn get_user_code_call_site(
        &mut self,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        frame_id: &FrameId,
        code_lines: Option<&Arc<CodeLines>>,
    ) -> Result<Option<UserCodeCallSite>, PyErr> {
        let py = pyframe.py();
        let user_code_call_site = match self
            .frames
            .iter()
            .rev()
            .take(2)
            .find(|(_frame, call_frame_id, _)| call_frame_id != frame_id)
        {
            Some((call_frame, call_frame_id, call_code_lines)) => build_user_code_call_site(
                call_frame.bind(py),
                *call_frame_id,
                call_code_lines.as_deref(),
            )?,
            None => None,
        };
        self.update_call_frames(event, pyframe, frame_id, code_lines);
        Ok(user_code_call_site)
    }

    /// Undo the call-site bookkeeping of an entry event whose processing
    /// Kolo raised into (see `reaches_program`): the frame never started as
    /// far as the trace is concerned.
    pub fn abandon(&mut self, frame_id: &FrameId) {
        if let Some(index) = self.frames.iter().rposition(|(_, id, _)| id == frame_id) {
            self.frames.truncate(index);
        }
    }

    fn update_call_frames(
        &mut self,
        event: Event,
        frame: &Bound<'_, PyAny>,
        frame_id: &FrameId,
        code_lines: Option<&Arc<CodeLines>>,
    ) {
        match (event, frame_id) {
            (Event::Call | Event::Resume | Event::Throw, frame_id) => {
                self.frames
                    .push((frame.clone().into(), *frame_id, code_lines.cloned()));
            }
            (Event::Return | Event::Unwind | Event::Yield, frame_id) => {
                // Close this frame (and any entries left above it), not
                // whatever is on top: when Kolo raises an interrupt into an
                // exit event (see `reaches_program`), CPython reports the
                // same frame's exit again, and the second must not close
                // the caller.
                if let Some(index) = self.frames.iter().rposition(|(_, id, _)| id == frame_id) {
                    self.frames.truncate(index);
                }
            }
        }
    }
}

#[derive(Default)]
pub struct FrameIds {
    frame_ids: HashMap<usize, FrameId>,
    /// Frames whose entry Kolo raised into and whose exit CPython will still
    /// report (see `abandon`).
    abandoned: HashSet<usize>,
}

impl FrameIds {
    /// Forget a frame whose entry event Kolo raised into (see
    /// `reaches_program`), so its exit is not matched to a recorded call.
    /// With `exit_follows`, CPython still reports that exit, and
    /// `take_abandoned` tells the caller to skip it.
    pub(crate) fn abandon(&mut self, pyframe_id: usize, exit_follows: bool) {
        self.frame_ids.remove(&pyframe_id);
        if exit_follows {
            self.abandoned.insert(pyframe_id);
        }
    }

    /// Whether this exit belongs to a frame whose entry was abandoned.
    pub(crate) fn take_abandoned(&mut self, pyframe_id: usize) -> bool {
        !self.abandoned.is_empty() && self.abandoned.remove(&pyframe_id)
    }

    fn set(&mut self, pyframe_id: usize) -> FrameId {
        if !self.abandoned.is_empty() {
            self.abandoned.remove(&pyframe_id);
        }
        let frame_id = FrameId::new();
        self.frame_ids.insert(pyframe_id, frame_id);
        frame_id
    }

    fn get(&self, pyframe_id: usize) -> FrameId {
        match self.frame_ids.get(&pyframe_id) {
            Some(frame_id) => *frame_id,
            None => FrameId::new(),
        }
    }

    pub(crate) fn get_option(&self, pyframe_id: usize) -> Option<FrameId> {
        self.frame_ids.get(&pyframe_id).copied()
    }

    pub(crate) fn get_or_set(&mut self, event: Event, pyframe_id: usize) -> FrameId {
        match event {
            Event::Call | Event::Resume | Event::Throw => self.set(pyframe_id),
            Event::Return | Event::Unwind | Event::Yield => self.get(pyframe_id),
        }
    }
}

/// What every line frame of one code object shares, read once per code
/// object instead of once per assignment.
pub struct LineCode {
    /// The code's filename relative to where tracing started, without a line.
    pub relative_path: String,
    pub co_name: String,
    /// `co_qualname` as `get_qualname` formats it. `None` when the code has
    /// no exact str `co_qualname`, which `get_qualname` then works out.
    pub co_qualname: Option<String>,
    /// The last module name this code ran under and the qualname joined
    /// from it. The module is compared as text and no reference to it is
    /// kept, so a frame holds nothing the traced program could count.
    qualname: Mutex<Option<(String, Arc<str>)>>,
}

impl LineCode {
    pub(crate) fn new(code: &Bound<'_, PyAny>, relative_path: String) -> Result<Self, PyErr> {
        let py = code.py();
        let co_name = code.getattr(intern!(py, "co_name"))?.extract::<String>()?;
        let co_qualname = code
            .getattr(intern!(py, "co_qualname"))
            .ok()
            .filter(|co_qualname| co_qualname.is_exact_instance_of::<PyString>())
            .map(|co_qualname| co_qualname.to_string());
        Ok(Self {
            relative_path,
            co_name,
            co_qualname,
            qualname: Mutex::new(None),
        })
    }

    /// `get_qualname(frame)`, joined once per module name instead of once
    /// per assignment when `__name__` is an ordinary str.
    fn qualname(&self, frame: &Bound<'_, PyFrame>) -> Result<Arc<str>, PyErr> {
        let py = frame.py();
        let Some(co_qualname) = &self.co_qualname else {
            return Ok(get_qualname(frame, py)?
                .expect("qualname always exists on Python 3.12+")
                .into());
        };
        let globals = frame.getattr(intern!(py, "f_globals"))?;
        let module = module_name_from_globals(&globals, py);
        let text = module
            .cast_exact::<PyString>()
            .ok()
            .and_then(|module| module.to_str().ok());
        let Some(text) = text else {
            // Formatted every time: another object's `__str__` may run user
            // code, and a lone surrogate is replaced.
            return Ok(format!("{module}.{co_qualname}").into());
        };
        let mut cached = self.qualname.lock().expect("qualname cache poisoned");
        Ok(match &*cached {
            Some((cached_module, qualname)) if cached_module == text => qualname.clone(),
            _ => {
                let qualname: Arc<str> = format!("{text}.{co_qualname}").into();
                *cached = Some((text.to_string(), qualname.clone()));
                qualname
            }
        })
    }
}

/// A line frame minus its assignment, captured at the store instruction and
/// written at the next event, once the stored value can be read.
pub struct LineFrame {
    code: Arc<LineCode>,
    /// The whole path of a frame that does not run `code` (see `capture`).
    foreign_path: Option<String>,
    lineno: Option<usize>,
    qualname: Arc<str>,
    frame_id: Option<FrameId>,
    timestamp: f64,
}

impl LineFrame {
    /// Read what a line frame records about `frame` now: its line, its
    /// qualname and the time. `code` holds the fields of `instruction_code`,
    /// which `frame` runs unless `sys._getframe` was replaced before the
    /// monitor looked it up; such a frame's path and qualname are read from
    /// the frame itself, as every frame's used to be.
    pub(crate) fn capture(
        code: &Arc<LineCode>,
        instruction_code: &Bound<'_, PyAny>,
        frame: &Bound<'_, PyFrame>,
        frame_paths: &FramePathCache,
        frame_id: Option<FrameId>,
    ) -> Result<Self, PyErr> {
        let py = frame.py();
        // Safety: `frame` is a live frame; this returns a new reference.
        #[cfg(Py_3_12)]
        let frame_code = unsafe {
            Bound::from_owned_ptr(py, pyo3::ffi::PyFrame_GetCode(frame.as_ptr().cast()).cast())
        };
        #[cfg(not(Py_3_12))]
        let frame_code = frame.getattr(intern!(py, "f_code"))?;
        let (foreign_path, lineno, qualname) = if frame_code.is(instruction_code) {
            (None, frame_line_number(frame)?, code.qualname(frame)?)
        } else {
            let path = frame_paths.format_frame_path(frame)?;
            let qualname = get_qualname(frame, py)?
                .expect("qualname always exists on Python 3.12+")
                .into();
            (Some(path), None, qualname)
        };
        Ok(Self {
            code: code.clone(),
            foreign_path,
            lineno,
            qualname,
            frame_id,
            timestamp: timestamp(),
        })
    }

    #[cfg(test)]
    pub(crate) fn for_test(path: &str, name: &str) -> Self {
        Self {
            code: Arc::new(LineCode {
                relative_path: path.to_string(),
                co_name: name.to_string(),
                co_qualname: None,
                qualname: Mutex::new(None),
            }),
            foreign_path: None,
            lineno: None,
            qualname: name.into(),
            frame_id: None,
            timestamp: 0.0,
        }
    }

    pub fn write_msgpack_into(
        &self,
        buf: &mut Vec<u8>,
        serializer: &Serializer,
        assign: (&str, Bound<'_, PyAny>),
        lightweight_repr: bool,
        max_value_bytes: Option<usize>,
    ) -> Result<(), PyErr> {
        rmp::encode::write_map_len(buf, 8).expect("Writing to memory, not I/O");
        if let Some(path) = &self.foreign_path {
            write_str_pair(buf, "path", Some(path));
        } else if u32::try_from(self.code.relative_path.len() + 21).is_ok() {
            write_frame_path_pair(buf, &self.code.relative_path, self.lineno);
        } else {
            let path = format_path_with_line(&self.code.relative_path, self.lineno);
            write_str_pair(buf, "path", Some(&path));
        }
        write_str_pair(buf, "co_name", Some(&self.code.co_name));
        write_str_pair(buf, "qualname", Some(&self.qualname));
        write_str_pair(buf, "event", Some("line"));
        write_str_pair(
            buf,
            "frame_id",
            self.frame_id.as_ref().map(FrameId::as_str),
        );
        write_f64_pair(buf, "timestamp", self.timestamp);
        write_str_pair(buf, "type", Some("frame"));
        write_assign_tuple(buf, serializer, assign, lightweight_repr, max_value_bytes)?;
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
    FrameId::new().as_str().to_owned()
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
    if name.as_str() == "<module>" {
        let globals = frame.getattr(intern!(py, "f_globals"))?;
        let module = module_name_from_globals(&globals, py);
        return Ok(Some(format!("{}.<module>", module)));
    }

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
            let property = property.cast()?;
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
