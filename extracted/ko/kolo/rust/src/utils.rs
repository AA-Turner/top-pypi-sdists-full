use hashbrown::HashMap;
use pyo3::exceptions::PyAttributeError;
use pyo3::exceptions::PyKeyError;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyFrame, PyTuple, PyType, PyModule, PyAny};
use std::env::current_dir;
use std::path::Path;
use std::time::SystemTime;
use ulid::Ulid;
use rmpv::Value as RmpvValue;

use super::config;

pub const STRING_KEY: &str = "a string is always a valid dict key";

/// A serialized frame is a sequence of msgpack-encoded bytes.
pub type SerializedFrame = Vec<u8>;

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
    frames: Vec<(PyObject, String)>,
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
        let call_frames = self
            .frames
            .iter()
            .map(|(frame, frame_id)| (frame.bind(py).clone(), frame_id.clone()))
            .collect();
        let user_code_call_site = user_code_call_site(call_frames, frame_id)?;
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
    pub fn write_msgpack(
        self,
        assign: (&str, Bound<'_, PyAny>),
        lightweight_repr: bool,
    ) -> Result<SerializedFrame, PyErr> {
        let mut buf: Vec<u8> = vec![];

        rmp::encode::write_map_len(&mut buf, 8).expect("Writing to memory, not I/O");
        write_str_pair(&mut buf, "path", Some(&self.path));
        write_str_pair(&mut buf, "co_name", Some(&self.co_name));
        write_str_pair(&mut buf, "qualname", Some(&self.qualname));
        write_str_pair(&mut buf, "event", Some("line"));
        write_str_pair(&mut buf, "frame_id", self.frame_id.as_deref());
        write_f64_pair(&mut buf, "timestamp", self.timestamp);
        write_str_pair(&mut buf, "type", Some("frame"));
        write_assign_tuple(&mut buf, assign, lightweight_repr)?;

        Ok(buf)
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
pub fn filename_with_lineno(
    frame: &Bound<'_, PyFrame>,
    py: Python,
) -> Result<(String, usize), PyErr> {
    let f_code = frame.getattr(intern!(py, "f_code"))?;
    let co_filename = f_code.getattr(intern!(py, "co_filename"))?;
    let filename = co_filename.extract::<String>()?;
    let lineno = frame.getattr(intern!(py, "f_lineno"))?;
    let lineno = lineno.extract()?;
    Ok((filename, lineno))
}

/// Combine a filename and line number into Kolo's standard format.
pub fn format_frame_path(filename: &str, lineno: usize) -> String {
    let path = Path::new(filename);
    let dir = current_dir().expect("Current directory is invalid");
    let relative_path = match path.strip_prefix(&dir) {
        Ok(relative_path) => relative_path,
        Err(_) => path,
    };
    format!("{}:{}", relative_path.display(), lineno)
}

/// Get the frame path from a Python frame.
fn frame_path(frame: &Bound<'_, PyFrame>, py: Python) -> Result<String, PyErr> {
    let (filename, lineno) = filename_with_lineno(frame, py)?;
    Ok(format_frame_path(&filename, lineno))
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
            let module = globals
                .get_item("__name__")
                .unwrap_or_else(|_| "<unknown>".to_object(py).into_bound(py));
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
        let module = globals
            .get_item("__name__")
            .unwrap_or_else(|_| "<unknown>".to_object(py).into_bound(py));
        return Ok(Some(format!("{}.<module>", module)));
    }

    // Fallback handling for legacy Python versions without `co_qualname`.
    match _get_qualname_inner(frame, py, &co_name) {
        Ok(qualname) => Ok(qualname),
        Err(_) => Ok(None),
    }
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
    let inspect = PyModule::import_bound(py, "inspect")?;
    let getattr_static = inspect.getattr(intern!(py, "getattr_static"))?;
    match locals.get_item("self") {
        Ok(locals_self) => {
            let function = getattr_static.call1((locals_self, co_name))?;
            let builtins = py.import_bound("builtins")?;
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
            let module = globals
                .get_item("__name__")
                .unwrap_or_else(|_| "<unknown>".to_object(py).into_bound(py));
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

/// Serialize an arbitrary Python object as msgpack by delegating to `kolo.serialize.dump_msgpack`
/// or `kolo.serialize.dump_msgpack_lightweight_repr`.
pub fn dump_msgpack(
    py: Python,
    data: &Bound<'_, PyAny>,
    lightweight_repr: bool,
) -> Result<Vec<u8>, PyErr> {
    let serialize = PyModule::import_bound(py, "kolo.serialize")?;
    let args = PyTuple::new_bound(py, [&data]);
    let data = match lightweight_repr {
        false => serialize.call_method1("dump_msgpack", args)?,
        true => serialize.call_method1("dump_msgpack_lightweight_repr", args)?,
    };
    data.extract::<Vec<u8>>()
}

/// Write a key, value pair of a msgpack map where the value is a string or None.
fn write_str_pair(buf: &mut Vec<u8>, key: &str, value: Option<&str>) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    match value {
        Some(value) => rmp::encode::write_str(buf, value).expect("Writing to memory, not I/O"),
        None => rmp::encode::write_nil(buf).expect("Writing to memory, not I/O"),
    };
}

/// Write a key, value pair of a msgpack map where the value is already valid msgpack bytes.
fn write_raw_pair(buf: &mut Vec<u8>, key: &str, value: &mut Vec<u8>) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    buf.append(value);
}

/// Write a key, value pair of a msgpack map where the value is an integer or None.
fn write_int_pair(buf: &mut Vec<u8>, key: &str, value: Option<usize>) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    match value {
        Some(value) => {
            rmp::encode::write_uint(buf, value as u64).expect("Writing to memory, not I/O");
        }
        None => {
            rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
        }
    }
}

/// Write a key, value pair of a msgpack map where the value is a float.
fn write_f64_pair(buf: &mut Vec<u8>, key: &str, value: f64) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    rmp::encode::write_f64(buf, value).expect("Writing to memory, not I/O");
}


fn write_bool_pair(buf: &mut Vec<u8>, key: &str, value: bool) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    rmp::encode::write_bool(buf, value).expect("Writing to memory, not I/O");
}


/// Write a msgpack array from a vector of already valid msgpack frames.
fn write_raw_frames(buf: &mut Vec<u8>, frames: Vec<SerializedFrame>) {
    rmp::encode::write_array_len(buf, frames.len() as u32).expect("Writing to memory, not I/O");
    buf.append(&mut frames.into_iter().flatten().collect());
}

/// Serialize the `user_code_call_site` of the trace as msgpack.
///
/// Must be called in the context of writing a msgpack map.
fn write_user_code_call_site(buf: &mut Vec<u8>, user_code_call_site: Option<UserCodeCallSite>) {
    let user_code_call_site = match user_code_call_site {
        Some(user_code_call_site) => user_code_call_site.into_msgpack_value(),
        None => rmpv::Value::Nil,
    };
    rmp::encode::write_str(buf, "user_code_call_site").expect("Writing to memory, not I/O");
    rmpv::encode::write_value(buf, &user_code_call_site).unwrap();
}

/// Serialize the command line arguments of the Python program as msgpack.
///
/// Must be called in the context of writing a msgpack map.
/// The first value written is the `command_line_args` key. The other values are the command
/// line argument list as the map value.
fn write_argv(buf: &mut Vec<u8>, argv: Vec<String>) {
    rmp::encode::write_str(buf, "command_line_args").expect("Writing to memory, not I/O");
    rmp::encode::write_array_len(buf, argv.len() as u32).expect("Writing to memory, not I/O");
    for arg in argv {
        rmp::encode::write_str(buf, &arg).expect("Writing to memory, not I/O");
    }
}

/// Serialize the `frames_of_interest` of the trace as msgpack.
///
/// Must be called in the context of writing a msgpack map.
/// The first value written is the `frames` key. The other value is a list of frames.
fn write_frames_of_interest(buf: &mut Vec<u8>, frames_of_interest: Vec<SerializedFrame>) {
    rmp::encode::write_str(buf, "frames_of_interest").expect("Writing to memory, not I/O");
    write_raw_frames(buf, frames_of_interest);
}

/// Serialize the `frames` of the trace as msgpack.
///
/// Must be called in the context of writing a msgpack map.
/// The first value written is the `frames` key. The other values are a map from `thread_id` to
/// a list of frames.
fn write_frames(buf: &mut Vec<u8>, frames: HashMap<String, Vec<SerializedFrame>>) {
    rmp::encode::write_str(buf, "frames").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, frames.len() as u32).expect("Writing to memory, not I/O");
    for (thread_id, frames) in frames {
        rmp::encode::write_str(buf, &thread_id).expect("Writing to memory, not I/O");
        write_raw_frames(buf, frames);
    }
}

fn write_threads(
    py: Python,
    buf: &mut Vec<u8>,
    threads: &HashMap<String, PyObject>,
    frames_by_thread: &HashMap<String, Vec<SerializedFrame>>,
) {
    rmp::encode::write_str(buf, "threads").expect("Writing to memory, not I/O");
    // Start writing the 'threads' map
    // The map has as many key-value pairs as there are threads
    let thread_count = u32::try_from(threads.len()).unwrap();
    rmp::encode::write_map_len(buf, thread_count).expect("Writing to memory, not I/O");

    for (thread_id, thread) in threads.iter() {
        // Serialize the thread_id as the key
        rmp::encode::write_str(buf, &thread_id).expect("Writing to memory, not I/O");

        // Prepare to serialize the thread_info map

        // The 5 keys below + frames
        rmp::encode::write_map_len(buf, 6).expect("Writing to memory, not I/O");

        // Retrieve thread attributes
        let name: String = thread.getattr(py, "name")
            .expect("Failed to get 'name' attribute")
            .extract(py)
            .expect("Failed to extract 'name' as String");
        write_str_pair(buf, "name", Some(&name));

        // Safely access 'ident' attribute
        let ident: Option<usize> = match thread.getattr(py, "ident") {
            Ok(id) => id.extract(py).unwrap_or(None),
            Err(_) => None,
        };
        write_int_pair(buf, "ident", ident);
        
        // Safely access 'native_id' attribute
        let native_id: Option<usize> = match thread.getattr(py, "native_id") {
            Ok(id) => id.extract(py).unwrap_or(None),
            Err(_) => None,
        };
        write_int_pair(buf, "native_id", native_id);
        
        let daemon: bool = thread.getattr(py, "daemon")
            .expect("Failed to get 'daemon' attribute")
            .extract(py)
            .expect("Failed to extract 'daemon' as bool");
        write_bool_pair(buf, "daemon", daemon);
        
        let is_alive: bool = thread.call_method0(py, "is_alive")
            .expect("Failed to call 'is_alive' method")
            .extract(py)
            .expect("Failed to extract 'is_alive' as bool");
        write_bool_pair(buf, "is_alive", is_alive);

        rmp::encode::write_str(buf, "frames").expect("Writing to memory, not I/O");
        if let Some(frames) = frames_by_thread.get(&thread_id.clone()) {            
            write_raw_frames(buf, frames.to_vec());
        } else {
            write_raw_frames(buf, vec![]);
        }
    }
}

/// Writes a key and a `RmpvValue` pair to the buffer.
///
/// # Arguments
///
/// * `buf` - The buffer to write to.
/// * `key` - The key as a string slice.
/// * `value` - The value as a reference to `RmpvValue`.
fn write_rmpv_pair(buf: &mut Vec<u8>, key: &str, value: &RmpvValue) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    rmpv::encode::write_value(buf, value).expect("Writing to memory, not I/O");
}

/// Updates the `write_meta` method to handle `RmpvValue` types for config values.
fn write_meta(
    buf: &mut Vec<u8>,
    version: &str,
    source: &str,
    environment: &HashMap<String, String>,
    config: &HashMap<String, RmpvValue>,
) {
    rmp::encode::write_str(buf, "meta").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, 4).expect("Writing to memory, not I/O");

    write_str_pair(buf, "version", Some(version));
    write_str_pair(buf, "source", Some(source));

    // Serialize 'environment' as a nested map
    rmp::encode::write_str(buf, "environment").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, environment.len() as u32)
        .expect("Writing to memory, not I/O");
    for (key, value) in environment {
        write_str_pair(buf, key, Some(value));
    }

    // Serialize 'config' as a nested map with `RmpvValue` types
    rmp::encode::write_str(buf, "config").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, config.len() as u32)
        .expect("Writing to memory, not I/O");
    for (key, value) in config {
        write_rmpv_pair(buf, key, value);
    }
}

fn write_assign_tuple(
    buf: &mut Vec<u8>,
    assign: (&str, Bound<'_, PyAny>),
    lightweight_repr: bool,
) -> Result<(), PyErr> {
    const PY_TUPLE_EXTENSION_TYPE: i8 = 6;
    let (variable, assigned) = assign;
    let py = assigned.py();

    let mut inner: Vec<u8> = vec![];
    rmp::encode::write_array_len(&mut inner, 2).expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut inner, variable).expect("Writing to memory, not I/O");
    let mut assigned = dump_msgpack(py, &assigned, lightweight_repr)?;
    inner.append(&mut assigned);

    rmp::encode::write_str(buf, "assign").expect("Writing to memory, not I/O");
    rmp::encode::write_ext_meta(
        buf,
        inner.len().try_into().expect("Length should fit in a u32"),
        PY_TUPLE_EXTENSION_TYPE,
    )
    .expect("Writing to memory, not I/O");
    buf.append(&mut inner);
    Ok(())
}

pub fn build_trace(
    py: Python,
    frames_by_thread: HashMap<String, Vec<SerializedFrame>>,
    threads: HashMap<String, Py<PyAny>>,
    trace_id: &str,
    trace_name: Option<String>,
    source: &str,
    current_thread_id: String,
    timestamp: f64,
    config: &config::Config,
) -> Result<Py<PyBytes>, PyErr> {
    let version = kolo_version(py)?;
    let commit_sha = git_commit_sha(py)?;
    let argv = get_argv(py)?;

    // Collect environment information
    let environment = collect_environment(py)?;

    // Collect and filter configuration
    let filtered_config = collect_config(py, config)?;

    let mut buf: Vec<u8> = vec![];

    // Start writing the top-level msgpack map. The following entries are key, value pairs.
    // Total top level key-value pairs: 9
    rmp::encode::write_map_len(&mut buf, 10).expect("Writing to memory, not I/O");

    write_str_pair(&mut buf, "trace_id", Some(trace_id));
    write_str_pair(&mut buf, "trace_name", trace_name.as_deref());
    write_str_pair(&mut buf, "current_thread_id", Some(&current_thread_id));
    write_f64_pair(&mut buf, "timestamp", timestamp);
    write_str_pair(&mut buf, "current_commit_sha", commit_sha.as_deref());
    
    // Write 'meta' containing 'version', 'source', 'environment', and 'config'
    write_meta(&mut buf, &version, source, &environment, &filtered_config);
    write_argv(&mut buf, argv);

    write_threads(py, &mut buf, &threads, &frames_by_thread);
    write_frames_of_interest(&mut buf, vec![]); // empty frames_of_interest list
    write_frames(&mut buf, HashMap::new()); // empty frames dictionary 

    Ok(PyBytes::new_bound(py, &buf).unbind())
}

/// Collect environment information similar to the Python `environment` dict.
pub fn collect_environment(py: Python) -> Result<HashMap<String, String>, PyErr> {
    let sys = PyModule::import_bound(py, "sys")?;
    let platform_mod = PyModule::import_bound(py, "platform")?;

    let py_version = platform_mod.call_method0("python_version")?.extract::<String>()?;
    let py_version_full = sys.getattr(intern!(py, "version"))?.extract::<String>()?;
    let platform_info = platform_mod.call_method0("platform")?.extract::<String>()?;
    let system = platform_mod.call_method0("system")?.extract::<String>()?;
    let machine = platform_mod.call_method0("machine")?.extract::<String>()?;
    let processor = platform_mod.call_method0("processor")?.extract::<String>()?;

    let mut environment = HashMap::new();
    environment.insert("py_version".to_string(), py_version);
    environment.insert("py_version_full".to_string(), py_version_full);
    environment.insert("platform".to_string(), platform_info);
    environment.insert("system".to_string(), system);
    environment.insert("machine".to_string(), machine);
    environment.insert("processor".to_string(), processor);

    Ok(environment)
}

pub fn collect_config(py: Python, config: &config::Config) -> Result<HashMap<String, RmpvValue>, PyErr> {
    let raw_config = config.to_dict(py)?;
    let mut filtered_config = HashMap::new();

    for (key, value) in raw_config {
        filtered_config.insert(key, value.into()); // Convert PyAny to RmpvValue
    }

    filtered_config.insert("use_monitoring".to_string(), RmpvValue::Boolean(config.get_or(py, "use_monitoring", false)?));
    filtered_config.insert("use_rust".to_string(), RmpvValue::Boolean(true));

    Ok(filtered_config)
}

#[allow(clippy::too_many_arguments)]
pub fn write_frame(
    buf: &mut Vec<u8>,
    pyframe: &Bound<'_, PyFrame>,
    user_code_call_site: Option<UserCodeCallSite>,
    arg: Arg,
    event: Event,
    name: &str,
    frame_id: &str,
    lightweight_repr: bool,
    omit_return_locals: bool,
) -> Result<(), PyErr> {
    let py = pyframe.py();
    let none = py.None().into_bound(py);
    let (arg, arg_key) = match arg {
        Arg::None => (&none, "arg"),
        Arg::Argument(arg) => (arg, "arg"),
        Arg::Exception(exception) => (exception, "exception"),
    };

    let path = frame_path(pyframe, py)?;
    let qualname = get_qualname(pyframe, py)?;
    let locals = get_locals(pyframe, event, omit_return_locals)?;

    // Serialize frame data as msgpack
    let mut arg = dump_msgpack(py, arg, lightweight_repr)?;
    let mut locals = dump_msgpack(py, &locals, lightweight_repr)?;

    // The map length must match the number of key, value pairs written next exactly.
    rmp::encode::write_map_len(buf, 10).expect("Writing to memory, not I/O");

    write_str_pair(buf, "path", Some(&path));
    write_str_pair(buf, "co_name", Some(name));
    write_str_pair(buf, "qualname", qualname.as_deref());
    write_str_pair(buf, "event", Some(event.into()));
    write_str_pair(buf, "frame_id", Some(frame_id));
    write_raw_pair(buf, arg_key, &mut arg);
    write_raw_pair(buf, "locals", &mut locals);
    write_f64_pair(buf, "timestamp", timestamp());
    write_str_pair(buf, "type", Some("frame"));
    write_user_code_call_site(buf, user_code_call_site);
    Ok(())
}


pub struct UserCodeCallSite {
    pub call_frame_id: String,
    pub line_number: i32,
}

impl UserCodeCallSite {
    fn into_msgpack_value(self) -> rmpv::Value {
        rmpv::Value::Map(vec![
            ("call_frame_id".into(), self.call_frame_id.into()),
            ("line_number".into(), self.line_number.into()),
        ])
    }

    pub fn into_pydict(self, py: Python) -> Bound<'_, PyDict> {
        let call_site = PyDict::new_bound(py);
        call_site
            .set_item("call_frame_id", self.call_frame_id)
            .expect(STRING_KEY);
        call_site
            .set_item("line_number", self.line_number)
            .expect(STRING_KEY);
        call_site
    }
}

/// Find the frame_id and line number of the user code that called the active function.
///
/// Analagous to `kolo.serialize.user_code_call_site`.
pub fn user_code_call_site(
    call_frames: Vec<(Bound<'_, PyAny>, String)>,
    frame_id: &str,
) -> Result<Option<UserCodeCallSite>, PyErr> {
    let (call_frame, call_frame_id) = match call_frames
        .iter()
        .rev()
        .take(2)
        .find(|(_f, f_id)| f_id != frame_id)
    {
        Some(frame_data) => frame_data,
        None => {
            return Ok(None);
        }
    };

    let pyframe = call_frame.downcast::<PyFrame>()?;
    let py = pyframe.py();
    Ok(Some(UserCodeCallSite {
        call_frame_id: call_frame_id.to_string(),
        line_number: pyframe.getattr(intern!(py, "f_lineno"))?.extract()?,
    }))
}

/// Load Kolo's version from Python.
fn kolo_version(py: Python) -> Result<String, PyErr> {
    PyModule::import_bound(py, "kolo.version")?
        .getattr(intern!(py, "__version__"))?
        .extract::<String>()
}

/// Get the current git commit sha from Python.
fn git_commit_sha(py: Python) -> Result<Option<String>, PyErr> {
    PyModule::import_bound(py, "kolo.git")?
        .getattr(intern!(py, "COMMIT_SHA"))?
        .extract::<Option<String>>()
}

/// Get the command line arguments of the traced program from Python.
fn get_argv(py: Python) -> Result<Vec<String>, PyErr> {
    PyModule::import_bound(py, "sys")?
        .getattr(intern!(py, "argv"))?
        .extract::<Vec<String>>()
}

/// Load the local variables from a Python frame.
///
/// Omit the `__builtins__` entry from the trace because it is large and rarely interesting.
fn get_locals<'py>(
    frame: &Bound<'py, PyFrame>,
    event: Event,
    omit_return_locals: bool,
) -> Result<Bound<'py, PyAny>, PyErr> {
    let py = frame.py();

    if event == Event::Return && omit_return_locals {
        return Ok(py.None().into_bound(py));
    }

    let locals = frame.getattr(intern!(py, "f_locals"))?;
    let locals = locals.downcast_into::<PyDict>().unwrap();
    let result = match locals
        .get_item("__builtins__")
        .expect("locals.get(\"__builtins__\") should not raise.")
    {
        Some(_) => {
            let locals = locals.copy().unwrap();
            locals.del_item("__builtins__").unwrap();
            locals
        }
        None => locals,
    };

    Ok(result.into_any())
}

pub fn get_thread_id(thread: &Bound<'_, PyAny>, py: Python) -> Result<String, PyErr> {
    // Attempt to get 'native_id'
    let native_id: Option<usize> = match thread.getattr(intern!(py, "native_id")) {
        Ok(id) => id.extract()?,
        Err(err) if err.is_instance_of::<PyAttributeError>(py) => None,
        Err(err) => return Err(err),
    };

    // Attempt to get 'ident' if 'native_id' is not available
    let ident: Option<usize> = match thread.getattr(intern!(py, "ident")) {
        Ok(id) => id.extract()?,
        Err(err) if err.is_instance_of::<PyAttributeError>(py) => None,
        Err(err) => return Err(err),
    };

    // Construct 'thread_id'
    let thread_id = if let Some(id) = native_id {
        format!("native_{}", id)
    } else if let Some(id) = ident {
        format!("ident_{}", id)
    } else {
        // Attempt to retrieve the thread's name
        let thread_name: String = match thread.getattr(intern!(py, "name")) {
            Ok(name) => name.extract()?,
            Err(_) => "<unknown>".to_string(),
        };
        println!(
            "Kolo warning: thread has no id: {}",
            thread_name
        );
        "no_thread_id".to_string()
    };

    Ok(thread_id)
}

pub fn get_current_thread_id(py: Python) -> Result<String, PyErr> {
    let threading = PyModule::import_bound(py, "threading")?;
    let thread = threading.call_method0("current_thread")?;

    get_thread_id(thread.as_ref(), py)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_frame_path_invalid_path() {
        let frame_path = format_frame_path("<module>", 23);

        assert_eq!(frame_path, "<module>:23");
    }
}

/// Extract HTTP request/response information from frames to set a trace name.
/// Looks for django_request and django_response frame types from the Django filter.
pub fn extract_http_trace_name(frames_by_thread: &HashMap<String, Vec<SerializedFrame>>, current_thread_id: &str) -> Option<String> {
    let frames = frames_by_thread.get(current_thread_id)?;
    
    // Get first three and last three frames since request/response pairs are typically at the start/end
    let first_three = frames.iter().take(3);
    let last_three = frames.iter().rev().take(3);
    let relevant_frames: Vec<_> = first_three.chain(last_three).collect();

    let mut request_frame = None;
    let mut response_frame = None;

    // Look for django_request and django_response frames
    for frame_bytes in relevant_frames {
        if let Ok(frame) = rmpv::decode::read_value(&mut &frame_bytes[..]) {
            if let rmpv::Value::Map(frame_map) = frame {
                // Extract frame type
                let frame_type = frame_map.iter()
                    .find(|(k, _)| k == &rmpv::Value::String("type".into()))
                    .and_then(|(_, v)| match v {
                        rmpv::Value::String(s) => s.as_str(),
                        _ => None
                    });

                match frame_type {
                    Some("django_request") if request_frame.is_none() => {
                        // First request frame wins
                        request_frame = Some(frame_map);
                    }
                    Some("django_response") => {
                        // Last response frame wins (since we're iterating in order)
                        response_frame = Some(frame_map);
                    }
                    _ => {}
                }
            }
        }
    }

    // Extract trace name components if we have both frames
    if let (Some(req), Some(res)) = (&request_frame, &response_frame) {
        let method = req.iter()
            .find(|(k, _)| k == &rmpv::Value::String("method".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None
            });

        let path = req.iter()
            .find(|(k, _)| k == &rmpv::Value::String("path_info".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None
            });

        let status_code = res.iter()
            .find(|(k, _)| k == &rmpv::Value::String("status_code".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::Integer(n) => Some(n.to_string()),
                _ => None
            });

        if let (Some(method), Some(path), Some(status)) = (method, path, status_code) {
            return Some(format!("{} {} {}", status, method, path));
        }
    }

    None
}

pub fn extract_test_trace_name(frames_by_thread: &HashMap<String, Vec<SerializedFrame>>, current_thread_id: &str) -> Option<String> {
    let frames = frames_by_thread.get(current_thread_id)?;
    if frames.is_empty() {
        return None;
    }

    // Get first three and last three frames since start/end test pairs are typically at the start/end
    let first_three = frames.iter().take(3);
    let last_three = frames.iter().rev().take(3);
    let relevant_frames: Vec<_> = first_three.chain(last_three).collect();

    let mut start_test_frame = None;
     // we don't actually need anything stored under _end_test_frame yet
    let mut _end_test_frame = None;

    // Look for start_test and end_test frames
    for frame_bytes in relevant_frames {
        if let Ok(frame) = rmpv::decode::read_value(&mut &frame_bytes[..]) {
            if let rmpv::Value::Map(frame_map) = frame {
                // Extract frame type
                let frame_type = frame_map.iter()
                    .find(|(k, _)| k == &rmpv::Value::String("type".into()))
                    .and_then(|(_, v)| match v {
                        rmpv::Value::String(s) => s.as_str(),
                        _ => None
                    });

                match frame_type {
                    Some("start_test") if start_test_frame.is_none() => {
                        // First start_test frame wins
                        start_test_frame = Some(frame_map);
                    }
                    Some("end_test") => {
                        // Last end_test frame wins (since we're iterating in order)
                        _end_test_frame = Some(frame_map);
                    }
                    _ => {}
                }
            }
        }
    }

    // Extract trace name components if we have both frames
    if let Some(start) = start_test_frame {
        let test_name = start.iter()
            .find(|(k, _)| k == &rmpv::Value::String("test_name".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None
            })?;

        let test_class = start.iter()
            .find(|(k, _)| k == &rmpv::Value::String("test_class".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None
            });

        return Some(match test_class {
            Some(class_name) => format!("{}.{}", class_name, test_name),
            None => test_name.to_string(),
        });
    }

    None
}

