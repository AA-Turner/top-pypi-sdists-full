use bstr::Finder;
use hashbrown::HashMap;
use pyo3::prelude::*;
use pyo3::sync::GILProtected;
use pyo3::types::{PyAny, PyDict, PyFrame, PyList, PyModule};
use pyo3::{PyErr, Python};
use std::cell::RefCell;
use ulid::Ulid;

use super::utils;
use super::utils::Event;

/// This struct holds data for targetted profiling.
///
/// Analogous to `kolo.plugins.PluginProcessor`.
pub struct PluginProcessor {
    /// A `Finder` to match against candidate filenames.
    filename_finder: Finder<'static>,
    /// The type of the Kolo frame when processing a `call` event.
    call_type: String,
    /// The type of the Kolo frame when processing a `return` event.
    return_type: String,
    /// The type of the Kolo frame when processing an `unwind` event.
    unwind_type: String,
    /// The type of the Kolo frame when processing a `resume` event.
    resume_type: String,
    /// The type of the Kolo frame when processing a `yield` event.
    yield_type: String,
    /// The type of the Kolo frame when processing a `yield` event.
    throw_type: String,
    /// The subtype of the Kolo frame.
    subtype: Option<String>,
    /// A Python function used to add additional filtering logic.
    call: Option<PyObject>,
    /// A Python function used to add additional processing logic.
    process: Option<PyObject>,
    /// A list of events to filter against.
    events: Option<Vec<String>>,
    /// A Python dictionary used to store information between different process calls.
    context: Py<PyDict>,
    /// A Rust dictionary mapping the Python `id` of a frame to the Kolo `frame_id`.
    frame_ids: GILProtected<RefCell<HashMap<usize, String>>>,
}

impl std::fmt::Debug for PluginProcessor {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("PluginProcessor")
            .field("filename_finder", &self.filename_finder)
            .field("call_type", &self.call_type)
            .field("return_type", &self.return_type)
            .field("unwind_type", &self.unwind_type)
            .field("resume_type", &self.resume_type)
            .field("yield_type", &self.yield_type)
            .field("throw_type", &self.throw_type)
            .field("subtype", &self.subtype)
            .field("call", &self.call)
            .field("process", &self.process)
            .field("events", &self.events)
            .field("context", &self.context)
            .finish()
    }
}

/// Load a frame processor's `subtype` from a plugin_data dictionary
fn get_subtype(plugin_data: &Bound<'_, PyDict>) -> Result<Option<String>, PyErr> {
    let subtype = plugin_data.get_item("subtype").expect(utils::STRING_KEY);

    Ok(match subtype {
        Some(subtype) => Some(subtype.extract()?),
        None => None,
    })
}

/// Load a frame processor's `call` function from a plugin_data dictionary
fn get_callable(plugin_data: &Bound<'_, PyDict>, key: &str) -> Option<PyObject> {
    let callable = plugin_data.get_item(key).expect(utils::STRING_KEY);

    match callable {
        Some(callable) if callable.is_none() => None,
        Some(callable) => Some(callable.into()),
        None => None,
    }
}

/// Load a frame processor's `events` list from a plugin_data dictionary
fn get_events(plugin_data: &Bound<'_, PyDict>) -> Result<Option<Vec<String>>, PyErr> {
    let events = plugin_data.get_item("events").expect(utils::STRING_KEY);

    Ok(match events {
        Some(events) if events.is_none() => None,
        Some(events) => Some(events.extract()?),
        None => None,
    })
}

/// Load a frame processor's `path_fragment` from a plugin_data dictionary
fn get_filename(plugin_data: &Bound<'_, PyDict>) -> Result<String, PyErr> {
    let filename = plugin_data.as_any().get_item("path_fragment")?;
    let filename: String = filename.extract()?;
    #[cfg(target_os = "windows")]
    let filename = filename.replace("/", "\\");
    Ok(filename)
}

impl PluginProcessor {
    /// Create a new `PluginProcessor` from `plugin_data`.
    fn new(plugin_data: &Bound<'_, PyDict>, context: &Bound<'_, PyDict>) -> Result<Self, PyErr> {
        let filename = &get_filename(plugin_data)?;
        let call_type: String = plugin_data.as_any().get_item("call_type")?.extract()?;
        let return_type: String = plugin_data.as_any().get_item("return_type")?.extract()?;
        let unwind_type = match plugin_data.get_item("unwind_type")? {
            Some(unwind_type) => unwind_type.extract()?,
            None => return_type.clone(),
        };
        let resume_type = match plugin_data.get_item("resume_type")? {
            Some(resume_type) => resume_type.extract()?,
            None => call_type.clone(),
        };
        let yield_type = match plugin_data.get_item("yield_type")? {
            Some(yield_type) => yield_type.extract()?,
            None => return_type.clone(),
        };
        let throw_type = match plugin_data.get_item("throw_type")? {
            Some(throw_type) => throw_type.extract()?,
            None => unwind_type.clone(),
        };
        Ok(Self {
            filename_finder: Finder::new(filename).into_owned(),
            call_type,
            return_type,
            unwind_type,
            resume_type,
            yield_type,
            throw_type,
            subtype: get_subtype(plugin_data)?,
            call: get_callable(plugin_data, "call"),
            process: get_callable(plugin_data, "process"),
            events: get_events(plugin_data)?,
            // Cloning here is just bumping the reference count. This is what we want,
            // so Python knows we need `context` to continue to exist.
            context: context.clone().unbind(),
            frame_ids: GILProtected::new(HashMap::new().into()),
        })
    }

    /// Check if we should process the current frame event.
    pub fn matches_frame(
        &self,
        py: Python,
        frame: &Bound<'_, PyAny>,
        event: Event,
        arg: &PyObject,
        filename: &str,
    ) -> Result<bool, PyErr> {
        let filename_matches = self.filename_finder.find(filename).is_some();
        match &self.call {
            None => Ok(filename_matches),
            Some(call) => {
                let event: &str = event.into();
                Ok(filename_matches
                    && call
                        .call1(py, (frame, event, arg, &self.context))?
                        .extract(py)?)
            }
        }
    }

    /// Create a new Kolo `frame_id` for a Python frame object.
    ///
    /// Store the Python `id` of the frame and the Kolo `frame_id` in `self.frame_ids` for use
    /// later.
    fn create_frame_id(&self, pyframe: &Bound<'_, PyFrame>) -> String {
        let py = pyframe.py();
        let pyframe_id = pyframe.as_ptr() as usize;
        let frame_id = Ulid::new();
        let frame_id = format!("frm_{}", frame_id.to_string());
        self.frame_ids
            .get(py)
            .borrow_mut()
            .insert(pyframe_id, frame_id.clone());
        frame_id
    }

    /// Get the Kolo `frame_id` for a Python frame object.
    ///
    /// If the Python frame has been seen before, get the `frame_id` from `self.frame_ids`.
    /// Otherwise create a new one.
    fn get_frame_id(&self, pyframe: &Bound<'_, PyFrame>) -> String {
        let py = pyframe.py();
        let pyframe_id = pyframe.as_ptr() as usize;
        match self.frame_ids.get(py).borrow().get(&pyframe_id) {
            Some(frame_id) => frame_id.clone(),
            None => {
                let frame_id = Ulid::new();
                format!("frm_{}", frame_id.to_string())
            }
        }
    }

    /// Get or create a new Kolo `frame_id` for a given Python frame object
    fn frame_id(&self, pyframe: &Bound<'_, PyFrame>, event: Event) -> String {
        match event {
            Event::Call => self.create_frame_id(pyframe),
            Event::Return => self.get_frame_id(pyframe),
            Event::Unwind => self.get_frame_id(pyframe),
            Event::Resume => self.create_frame_id(pyframe),
            Event::Yield => self.get_frame_id(pyframe),
            Event::Throw => self.create_frame_id(pyframe),
        }
    }

    /// Process a frame event to build a custom Kolo frame
    pub fn process(
        &self,
        py: Python,
        pyframe: &Bound<'_, PyFrame>,
        event: Event,
        arg: &PyObject,
        call_frames: Vec<(Bound<'_, PyAny>, String)>,
        lightweight_repr: bool,
    ) -> Result<Option<(String, utils::SerializedFrame)>, PyErr> {
        // Exit early if the `event` is not in `self.events`.
        if let Some(events) = &self.events {
            if events.iter().all(|e| {
                let event: &str = event.into();
                e != event
            }) {
                return Ok(None);
            }
        }

        // Set standard frame data
        let data = PyDict::new_bound(py);
        let frame_id = self.frame_id(pyframe, event);
        data.set_item("frame_id", frame_id.clone())
            .expect(utils::STRING_KEY);
        data.set_item("timestamp", utils::timestamp())
            .expect(utils::STRING_KEY);


        let call_site = utils::user_code_call_site(call_frames, &frame_id)?
            .map(|call_site| call_site.into_pydict(py));
        data.set_item("user_code_call_site", call_site)
            .expect(utils::STRING_KEY);

        match event {
            Event::Call => data
                .set_item("type", &self.call_type)
                .expect(utils::STRING_KEY),
            Event::Return => data
                .set_item("type", &self.return_type)
                .expect(utils::STRING_KEY),
            Event::Unwind => data
                .set_item("type", &self.unwind_type)
                .expect(utils::STRING_KEY),
            Event::Resume => data
                .set_item("type", &self.resume_type)
                .expect(utils::STRING_KEY),
            Event::Yield => data
                .set_item("type", &self.yield_type)
                .expect(utils::STRING_KEY),
            Event::Throw => data
                .set_item("type", &self.throw_type)
                .expect(utils::STRING_KEY),
        }
        if let Some(subtype) = &self.subtype {
            data.set_item("subtype", subtype).expect(utils::STRING_KEY);
        }

        // Update with custom frame data
        if let Some(process) = &self.process {
            let event: &str = event.into();
            data.update(
                process
                    .call1(py, (pyframe, event, arg, &self.context))?
                    .downcast_bound(py)?,
            )?;
        }

        let frame_type = data
            .get_item("type")?
            .expect("type is always set")
            .extract::<String>()?;

        let data = utils::dump_msgpack(py, &data, lightweight_repr)?;
        Ok(Some((frame_type, data)))
    }
}

/// Create PluginProcessor instances from plugin_data.
fn load_plugin_data(
    py: Python,
    plugins: &Bound<'_, PyList>,
    config: &Bound<'_, PyDict>,
) -> Result<HashMap<String, Vec<PluginProcessor>>, PyErr> {
    let mut processors: HashMap<String, Vec<PluginProcessor>> =
        HashMap::with_capacity(plugins.len());

    for plugin_data in plugins {
        let plugin_data: &Bound<'_, PyDict> = plugin_data.downcast()?;
        let co_names = plugin_data.as_any().get_item("co_names")?;
        let context = match plugin_data
            .get_item("build_context")
            .expect(utils::STRING_KEY)
        {
            Some(build_context) => {
                if build_context.is_none() {
                    PyDict::new_bound(py)
                } else {
                    build_context.call1((config,))?.downcast_into()?
                }
            }
            None => PyDict::new_bound(py),
        };
        for co_name in co_names.iter()? {
            let co_name: String = co_name?.extract()?;
            let processor = PluginProcessor::new(plugin_data, &context)?;
            processors.entry(co_name).or_default().push(processor);
        }
    }
    Ok(processors)
}

/// Load all plugins based on config data.
pub fn load_plugins(
    py: Python,
    config: &Bound<'_, PyDict>,
) -> Result<HashMap<String, Vec<PluginProcessor>>, PyErr> {
    let kolo_plugins = PyModule::import_bound(py, "kolo.plugins")
        .expect("kolo.plugins should always be importable");
    let load = kolo_plugins
        .getattr("load_plugin_data")
        .expect("load_plugin_data should exist");
    let plugins = load
        .call1((config,))
        .expect("load_plugin_data should be callable");
    let plugins = plugins
        .downcast()
        .expect("load_plugin_data should return a list");
    load_plugin_data(py, plugins, config)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::_kolo::utils;
    use pyo3::exceptions::{PyKeyError, PyTypeError, PyValueError};
    use pyo3::types::PyBytes;
    use testresult::TestResult;

    fn load_msgpack(py: Python<'_>, data: Vec<u8>) -> Bound<'_, PyAny> {
        let serialize =
            PyModule::import_bound(py, "kolo.serialize").expect("Could not import kolo.serialize");
        let data = PyBytes::new_bound(py, &data);
        serialize
            .call_method1("load_msgpack", (data,))
            .expect("Invalid msgpack data")
    }

    fn assert_error_message(py: Python, err: PyErr, expected: &str) -> TestResult {
        let message = err.value_bound(py).getattr("args")?.get_item(0)?;
        let message: &str = message.extract()?;
        assert_eq!(message, expected);
        Ok(())
    }

    fn assert_keyerror(
        py: Python,
        context: &Bound<'_, PyDict>,
        plugin_data: &Bound<'_, PyDict>,
        key: &str,
    ) -> TestResult {
        let err = PluginProcessor::new(plugin_data, context).unwrap_err();
        assert!(err.is_instance_of::<PyKeyError>(py));
        assert!(err.value_bound(py).getattr("args")?.eq((key,))?);
        Ok(())
    }

    fn assert_typeerror(
        py: Python,
        context: &Bound<'_, PyDict>,
        plugin_data: &Bound<'_, PyDict>,
        message: &str,
    ) -> TestResult {
        let err = PluginProcessor::new(plugin_data, context).unwrap_err();
        assert!(err.is_instance_of::<PyTypeError>(py));
        assert_error_message(py, err, message)
    }

    #[test]
    fn test_new() -> TestResult {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new_bound(py);
            let plugin_data = PyDict::new_bound(py);
            assert_keyerror(py, &context, &plugin_data, "path_fragment")?;

            plugin_data.set_item("path_fragment", py.None())?;
            assert_typeerror(
                py,
                &context,
                &plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            )?;

            plugin_data.set_item("path_fragment", "kolo").unwrap();
            assert_keyerror(py, &context, &plugin_data, "call_type")?;

            plugin_data.set_item("call_type", py.None())?;
            assert_typeerror(
                py,
                &context,
                &plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            )?;

            plugin_data.set_item("call_type", "call").unwrap();
            assert_keyerror(py, &context, &plugin_data, "return_type")?;

            plugin_data.set_item("return_type", py.None())?;
            assert_typeerror(
                py,
                &context,
                &plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            )?;

            plugin_data.set_item("return_type", "return")?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            assert!(processor.context.bind(py).eq(&context)?);
            assert_eq!(processor.call_type, "call");
            assert_eq!(processor.return_type, "return");
            assert!(processor.subtype.is_none());
            assert!(processor.call.is_none());
            assert!(processor.process.is_none());
            assert!(processor
                .filename_finder
                .find("dev/kolo/middleware.py")
                .is_some());
            assert!(processor
                .filename_finder
                .find("dev/django/middleware.py")
                .is_none());

            plugin_data.set_item("subtype", py.None())?;
            assert_typeerror(
                py,
                &context,
                &plugin_data,
                "'NoneType' object cannot be converted to 'PyString'",
            )?;

            plugin_data.set_item("subtype", "subtype")?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            assert_eq!(processor.subtype.unwrap(), "subtype");

            plugin_data.set_item("call", py.None())?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            assert!(processor.call.is_none());

            plugin_data.set_item("process", py.None())?;
            let processor = PluginProcessor::new(&plugin_data, &context).unwrap();
            assert!(processor.process.is_none());
            Ok(())
        })
    }

    #[test]
    fn test_debug() -> TestResult {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new_bound(py);
            let plugin_data = PyDict::new_bound(py);

            plugin_data.set_item("path_fragment", "kolo").unwrap();
            plugin_data.set_item("call_type", "call").unwrap();
            plugin_data.set_item("return_type", "return")?;
            plugin_data.set_item("unwind_type", "unwind")?;
            plugin_data.set_item("resume_type", "resume")?;
            plugin_data.set_item("yield_type", "yield")?;
            plugin_data.set_item("throw_type", "throw")?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;

            let expected = format!(
                "PluginProcessor {{ filename_finder: {:?}, call_type: \"call\", return_type: \"return\", unwind_type: \"unwind\", resume_type: \"resume\", yield_type: \"yield\", throw_type: \"throw\", subtype: None, call: None, process: None, events: None, context: {:?} }}",
                processor.filename_finder,
                processor.context,
            );
            assert_eq!(format!("{processor:?}"), expected);
            Ok(())
        })
    }

    #[test]
    fn test_matches() -> TestResult {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new_bound(py);
            let plugin_data = PyDict::new_bound(py);
            plugin_data.set_item("path_fragment", "kolo")?;
            plugin_data.set_item("call_type", "call")?;
            plugin_data.set_item("return_type", "return")?;

            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let frame = PyModule::from_code_bound(
                py,
                "
import inspect

frame = inspect.currentframe()
                ",
                "kolo/filename.py",
                "module",
            )?
            .getattr("frame")?;
            let (filename, _) = utils::filename_with_lineno(frame.downcast()?, py)?;
            let processor_match =
                processor.matches_frame(py, &frame, Event::Call, &py.None(), &filename);
            assert!(processor_match?);

            let call = PyModule::from_code_bound(
                py,
                "def call(frame, event, arg, context):
                    return event == 'call'
                ",
                "",
                "",
            )?
            .getattr("call")?;

            plugin_data.set_item("call", call)?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let processor_match =
                processor.matches_frame(py, &frame, Event::Call, &py.None(), &filename);
            assert!(processor_match?);
            let processor_match =
                processor.matches_frame(py, &frame, Event::Return, &py.None(), &filename);
            assert!(!processor_match?);

            let invalid_return_type = PyModule::from_code_bound(
                py,
                "def call(frame, event, arg, context):
                    return 'call'
                ",
                "",
                "",
            )?
            .getattr("call")?;

            plugin_data.set_item("call", invalid_return_type)?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let err = processor
                .matches_frame(py, &frame, Event::Call, &py.None(), &filename)
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object cannot be converted to 'PyBool'")?;

            plugin_data.set_item("call", "invalid_callable")?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let err = processor
                .matches_frame(py, &frame, Event::Call, &py.None(), &filename)
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object is not callable")?;
            Ok(())
        })
    }

    #[test]
    fn test_process() -> TestResult {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let context = PyDict::new_bound(py);
            let plugin_data = PyDict::new_bound(py);
            plugin_data.set_item("path_fragment", "kolo")?;
            plugin_data.set_item("call_type", "call")?;
            plugin_data.set_item("return_type", "return")?;

            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let frame = PyModule::from_code_bound(
                py,
                "
import inspect

frame = inspect.currentframe()
                ",
                "kolo/filename.py",
                "module",
            )?
            .getattr("frame")?;
            let frame = frame.downcast()?;

            let (frame_type, data) = processor
                .process(py, frame, Event::Call, &py.None(), vec![], false)?
                .unwrap();
            let data = load_msgpack(py, data);
            let type_ = data.get_item("type")?;
            let type_: &str = type_.extract()?;
            assert_eq!(type_, "call");
            assert_eq!(type_, frame_type);
            data.get_item("frame_id")?.extract::<&str>()?;
            data.get_item("timestamp")?.extract::<f64>()?;

            let (frame_type, data) = processor
                .process(py, frame, Event::Return, &py.None(), vec![], false)?
                .unwrap();
            let data = load_msgpack(py, data);
            let type_ = data.get_item("type")?;
            let type_: &str = type_.extract()?;
            assert_eq!(type_, "return");
            assert_eq!(type_, frame_type);

            plugin_data.set_item("subtype", "rust")?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let (_frame_type, data) = processor
                .process(py, frame, Event::Return, &py.None(), vec![], false)?
                .unwrap();
            let data = load_msgpack(py, data);
            let subtype = data.get_item("subtype")?;
            let subtype: &str = subtype.extract()?;
            assert_eq!(subtype, "rust");

            let process = PyModule::from_code_bound(
                py,
                "def process(frame, event, arg, context):
                    return {
                        'event': event,
                    }
                ",
                "",
                "",
            )?
            .getattr("process")?;
            plugin_data.set_item("process", process)?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let (_frame_type, data) = processor
                .process(py, frame, Event::Call, &py.None(), vec![], false)?
                .unwrap();
            let data = load_msgpack(py, data);
            let event = data.get_item("event")?;
            let event: &str = event.extract()?;
            assert_eq!(event, "call");

            let invalid_return_type = PyModule::from_code_bound(
                py,
                "def process(frame, event, arg, context):
                    return 'process'
                ",
                "",
                "",
            )?
            .getattr("process")?;
            plugin_data.set_item("process", invalid_return_type)?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let err = processor
                .process(py, frame, Event::Call, &py.None(), vec![], false)
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object cannot be converted to 'Mapping'")?;

            plugin_data.set_item("process", "invalid_callable")?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let err = processor
                .process(py, frame, Event::Call, &py.None(), vec![], false)
                .unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object is not callable")?;

            let weird_mapping = PyModule::from_code_bound(
                py,
                "
from collections.abc import Mapping


class WeirdMapping(Mapping):
    def __getitem__(self, key):
        raise ValueError('Weird')

    def __iter__(self):
        raise ValueError('Weird')

    def __len__(self):
        raise ValueError('Weird')


def process(frame, event, arg, context):
    return WeirdMapping()
                ",
                "",
                "",
            )?
            .getattr("process")?;
            plugin_data.set_item("process", weird_mapping)?;
            let processor = PluginProcessor::new(&plugin_data, &context)?;
            let err = processor
                .process(py, frame, Event::Call, &py.None(), vec![], false)
                .unwrap_err();
            assert!(err.is_instance_of::<PyValueError>(py));
            assert_error_message(py, err, "Weird")?;
            Ok(())
        })
    }

    #[test]
    fn test_load_plugin_data() -> TestResult {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let plugins = PyList::empty_bound(py);
            let config = PyDict::new_bound(py);

            let processors = load_plugin_data(py, &plugins, &config)?;
            assert_eq!(processors.len(), 0);

            let plugins = PyList::new_bound(py, vec![py.None()]);
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'NoneType' object cannot be converted to 'PyDict'")?;

            let plugin_data = PyDict::new_bound(py);
            let plugins = PyList::new_bound(py, vec![&plugin_data]);
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyKeyError>(py));
            assert_error_message(py, err, "co_names")?;

            plugin_data.set_item("co_names", py.None())?;
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'NoneType' object is not iterable")?;

            plugin_data.set_item("co_names", (py.None(),))?;
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(
                py,
                err,
                "'NoneType' object cannot be converted to 'PyString'",
            )?;

            let weird_co_names = PyModule::from_code_bound(
                py,
                "
def weird_gen():
    raise ValueError('Weird')
    yield

weird = weird_gen()
                ",
                "",
                "",
            )?
            .getattr("weird")?;

            plugin_data.set_item("co_names", weird_co_names)?;
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyValueError>(py));
            assert_error_message(py, err, "Weird")?;

            plugin_data.set_item("co_names", ("foo",))?;
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyKeyError>(py));
            assert_error_message(py, err, "path_fragment")?;

            plugin_data.set_item("path_fragment", "kolo")?;
            plugin_data.set_item("call_type", "call_foo")?;
            plugin_data.set_item("return_type", "return_foo")?;

            let processors = load_plugin_data(py, &plugins, &config)?;
            assert_eq!(processors.len(), 1);

            plugin_data.set_item("build_context", py.None())?;
            let processors = load_plugin_data(py, &plugins, &config)?;
            assert_eq!(processors.len(), 1);

            plugin_data.set_item("build_context", "invalid callable")?;
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object is not callable")?;

            let invalid_return_type = PyModule::from_code_bound(
                py,
                "def build_context(config):
                    return 'invalid'
                ",
                "",
                "",
            )?
            .getattr("build_context")?;
            plugin_data.set_item("build_context", invalid_return_type)?;
            let err = load_plugin_data(py, &plugins, &config).unwrap_err();
            assert!(err.is_instance_of::<PyTypeError>(py));
            assert_error_message(py, err, "'str' object cannot be converted to 'PyDict'")?;

            let build_context = PyModule::from_code_bound(
                py,
                "def build_context(config):
                    return {'frame_ids': []}
                ",
                "",
                "",
            )?
            .getattr("build_context")?;
            plugin_data.set_item("build_context", build_context)?;
            let processors = load_plugin_data(py, &plugins, &config)?;
            assert_eq!(processors.len(), 1);
            assert_eq!(processors["foo"].len(), 1);
            assert!(processors["foo"][0]
                .context
                .bind(py)
                .get_item("frame_ids")?
                .unwrap()
                .is_instance_of::<PyList>());
            Ok(())
        })
    }

    #[test]
    fn test_load_plugins() -> TestResult {
        pyo3::prepare_freethreaded_python();

        Python::with_gil(|py| {
            let config = PyDict::new_bound(py);
            let processors = load_plugins(py, &config)?;
            assert!(!processors.is_empty());
            Ok(())
        })
    }
}
