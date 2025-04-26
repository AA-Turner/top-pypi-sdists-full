use hashbrown::HashMap;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::sync::GILProtected;
use pyo3::types::PyBytes;
use pyo3::types::PyCode;
use pyo3::types::PyDict;
use std::borrow::Cow;
use std::cell::RefCell;
use thread_local::ThreadLocal;

use super::config;
use super::filters;
use super::plugins::{load_plugins, PluginProcessor};
use super::utils;
use super::utils::{Event, LineFrame, SerializedFrame};

#[allow(clippy::enum_variant_names)]
enum Opname {
    StoreFast,
    StoreGlobal,
    StoreDeref,
}

impl Opname {
    fn assignment_value<'py>(
        &self,
        variable: &str,
        frame: &Bound<'py, PyAny>,
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        let py = frame.py();
        match self {
            Opname::StoreFast | Opname::StoreDeref => {
                let locals = frame.getattr(intern!(py, "f_locals"))?;
                Ok(locals.get_item(variable)?)
            }
            Opname::StoreGlobal => {
                let globals = frame.getattr(intern!(py, "f_globals"))?;
                Ok(globals.get_item(variable)?)
            }
        }
    }
}

struct InstructionData {
    variable: String,
    opname: Opname,
    line_frame: Py<PyAny>,
    line_frame_data: LineFrame,
}

#[pyclass(module = "kolo._kolo")]
pub struct KoloMonitor {
    #[pyo3(get)]
    tool_id: u8,
    #[pyo3(get, set)]
    active: bool,
    #[pyo3(set)]
    timestamp: f64,
    db_path: String,
    source: String,
    one_trace_per_test: bool,
    omit_return_locals: bool,
    sqlite_busy_timeout: usize,
    trace_id: GILProtected<RefCell<String>>,
    trace_name: Option<String>,
    include_frames: filters::Finders,
    ignore_frames: filters::Finders,
    default_include_frames: GILProtected<RefCell<HashMap<String, Vec<PluginProcessor>>>>,
    #[pyo3(get)]
    line_events: bool,
    frames_by_thread: GILProtected<RefCell<HashMap<String, Vec<SerializedFrame>>>>,
    threads: GILProtected<RefCell<HashMap<String, Py<PyAny>>>>,
    current_thread_id: String,
    lightweight_repr: bool,
    call_frames: ThreadLocal<RefCell<utils::CallFrames>>,
    _frame_ids: ThreadLocal<RefCell<utils::FrameIds>>,
    disable: Py<PyAny>,
    instruction_data: ThreadLocal<RefCell<Option<InstructionData>>>,
    config: config::Config,
}

impl KoloMonitor {
    pub fn new(
        db_path: String,
        config_dict: &Bound<'_, PyDict>,
        source: String,
        one_trace_per_test: bool,
        trace_name: Option<String>,
    ) -> Result<Self, PyErr> {
        let py = config_dict.py();
        let config = config::Config::new(config_dict)?;

        let sys = PyModule::import_bound(py, "sys")?;
        let monitoring = sys.getattr("monitoring")?;
        let disable = monitoring.getattr("DISABLE")?.unbind();
        let tool_id = monitoring.getattr("PROFILER_ID")?.extract()?;

        let omit_return_locals = config.get_or(py, "omit_return_locals", false)?;
        let line_events = config.get_or(py, "line_events", false)?;
        let lightweight_repr = config.get_or(py, "lightweight_repr", false)?;
        let sqlite_busy_timeout = config.get_or(py, "sqlite_busy_timeout", 60)?;

        let filters = config_dict
            .get_item("filters")
            .expect("config.get(\"filters\") should not raise.");
        let plugins = load_plugins(py, config_dict)?;

        Ok(KoloMonitor {
            active: false,
            tool_id,
            timestamp: utils::timestamp(),
            db_path,
            source,
            one_trace_per_test,
            omit_return_locals,
            sqlite_busy_timeout,
            trace_id: GILProtected::new(utils::trace_id().into()),
            trace_name,
            include_frames: filters::load_filters(&filters, "include_frames")?,
            ignore_frames: filters::load_filters(&filters, "ignore_frames")?,
            default_include_frames: GILProtected::new(plugins.into()),
            line_events,
            frames_by_thread: GILProtected::new(HashMap::new().into()),
            threads: GILProtected::new(HashMap::new().into()),
            current_thread_id: utils::get_current_thread_id(py).unwrap(),
            lightweight_repr,
            call_frames: ThreadLocal::new(),
            _frame_ids: ThreadLocal::new(),
            disable,
            instruction_data: ThreadLocal::new(),
            config,
        })
    }

    fn include(
        &self,
        py: Python,
        processor: &PluginProcessor,
        event: Event,
        filename: &str,
        arg: utils::Arg,
    ) -> Result<Option<(String, SerializedFrame)>, PyErr> {
        let sys = PyModule::import_bound(py, "sys")?;
        let frame = sys.call_method1("_getframe", (0,))?;
        let arg = arg.into_inner(py);
        if !processor.matches_frame(py, &frame, event, &arg, filename)? {
            return Ok(None);
        }
        let frame = frame.downcast()?;
        let call_frames = self.call_frames.get_or_default().borrow().get_bound(py);
        processor.process(py, frame, event, &arg, call_frames, self.lightweight_repr)
    }

    fn monitor(
        &self,
        code: &Bound<'_, PyCode>,
        arg: utils::Arg,
        event: Event,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let py = code.py();
        let co_filename = code
            .getattr(intern!(py, "co_filename"))
            .expect("Code objects always define co_filename");
        let co_name = code
            .getattr(intern!(py, "co_name"))
            .expect("Code objects always define co_name");
        let filename = co_filename
            .extract()
            .expect("`co_filename` is always a string");
        let name = co_name
            .extract::<Cow<str>>()
            .expect("`co_name` is always a string");

        let mut frames = vec![];
        let mut frame_types = vec![];
        let default_include_frames = self.default_include_frames.get(py).borrow();
        if let Some(processors) = default_include_frames.get(&name.to_string()) {
            for processor in processors.iter() {
                if let Some((frame_type, frame_data)) =
                    self.include(py, processor, event, filename, arg.clone())?
                {
                    frames.push(frame_data);
                    frame_types.push(frame_type);
                }
            }
        };
        if self.include_frame(py, filename)? {
            let frame_data = self.process(py, &name, event, arg)?;
            frames.push(frame_data);
            frame_types.push("frame".to_string());
        } else if frames.is_empty() {
            match event {
                Event::Call | Event::Return | Event::Resume | Event::Yield => {
                    return Ok(Some(self.disable.clone_ref(py)))
                }
                Event::Unwind | Event::Throw => return Ok(None),
            }
        }

        match event {
            Event::Call | Event::Resume | Event::Throw => {
                self.push_frames_call(py, &mut frames, frame_types)?
            }
            Event::Return | Event::Unwind | Event::Yield => {
                self.push_frames_return(py, &mut frames, &mut frame_types)?
            }
        }
        Ok(None)
    }

    fn process(
        &self,
        py: Python,
        name: &str,
        event: Event,
        arg: utils::Arg,
    ) -> Result<SerializedFrame, PyErr> {
        let sys = PyModule::import_bound(py, "sys")?;
        let frame = sys.call_method1("_getframe", (0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_id = self
            ._frame_ids
            .get_or_default()
            .borrow_mut()
            .get_or_set(event, pyframe_id);
        let pyframe = frame.downcast()?;
        let user_code_call_site = self
            .call_frames
            .get_or_default()
            .borrow_mut()
            .get_user_code_call_site(pyframe, event, &frame_id)?;
        let mut buf: Vec<u8> = vec![];
        utils::write_frame(
            &mut buf,
            pyframe,
            user_code_call_site,
            arg,
            event,
            name,
            &frame_id,
            self.lightweight_repr,
            self.omit_return_locals,
        )?;
        Ok(buf)
    }

    fn _monitor_instruction(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
    ) -> Result<Option<Py<PyAny>>, PyErr> {
        let py = code.py();
        let kolo_monitoring = PyModule::import_bound(py, "kolo.monitoring")?;
        let instruction = kolo_monitoring
            .call_method1(intern!(py, "get_instruction"), (code, instruction_offset))?;
        if instruction.is_none() {
            return Ok(Some(self.disable.clone_ref(py)));
        }
        let opname = match instruction.getattr(intern!(py, "opname"))?.extract()? {
            "STORE_FAST" => Opname::StoreFast,
            "STORE_GLOBAL" => Opname::StoreGlobal,
            "STORE_DEREF" => Opname::StoreDeref,
            _ => {
                return Ok(Some(self.disable.clone_ref(py)));
            }
        };
        let argval = instruction.getattr(intern!(py, "argval"))?;
        if !argval.is_none() && argval.extract::<&str>()?.starts_with('@') {
            return Ok(Some(self.disable.clone_ref(py)));
        }

        let co_filename = code
            .getattr(intern!(py, "co_filename"))
            .expect("Code objects always define co_filename");
        let co_name = code
            .getattr(intern!(py, "co_name"))
            .expect("Code objects always define co_name");
        let filename = co_filename
            .extract()
            .expect("`co_filename` is always a string");
        let name = co_name.extract().expect("`co_name` is always a string");

        match self.include_frame(py, filename)? {
            true => {
                self.process_instruction(filename, name, instruction, opname)?;
                Ok(None)
            }
            false => Ok(Some(self.disable.clone_ref(py))),
        }
    }

    fn process_instruction(
        &self,
        filename: &str,
        name: &str,
        instruction: Bound<'_, PyAny>,
        opname: Opname,
    ) -> Result<(), PyErr> {
        let py = instruction.py();
        let sys = PyModule::import_bound(py, "sys")?;
        let frame = sys.call_method1("_getframe", (0,))?;
        let pyframe_id = frame.as_ptr() as usize;
        let frame_id = self
            ._frame_ids
            .get_or_default()
            .borrow()
            .get_option(pyframe_id);
        let pyframe = frame.downcast()?;

        let variable = instruction.getattr(intern!(py, "argval"))?.extract()?;
        let lineno = frame.getattr(intern!(py, "f_lineno"))?.extract()?;
        let line_frame_data = LineFrame::new(
            utils::format_frame_path(filename, lineno),
            name.to_string(),
            utils::get_qualname(pyframe, py)?.expect("qualname always exists on Python 3.12+"),
            frame_id,
            utils::timestamp(),
        );
        self.instruction_data
            .get_or_default()
            .replace(Some(InstructionData {
                opname,
                variable,
                line_frame: frame.unbind(),
                line_frame_data,
            }));
        Ok(())
    }

    fn process_assignment(&self, py: Python) -> Result<(), PyErr> {
        let instruction_data = match self.instruction_data.get_or_default().replace(None) {
            None => return Ok(()),
            Some(instruction_data) => instruction_data,
        };
        let frame = instruction_data.line_frame.bind(py);
        let variable = instruction_data.variable;
        let assign = instruction_data.opname.assignment_value(&variable, frame)?;
        let mut frames = vec![instruction_data
            .line_frame_data
            .write_msgpack((&variable, assign), self.lightweight_repr)?];
        self.push_frame_data(py, &mut frames);
        Ok(())
    }

    /// Extract test name or HTTP request/response information from frames to set the trace name.
    fn _set_trace_name(&self, frames_by_thread: &HashMap<String, Vec<SerializedFrame>>) -> Option<String> {
        utils::extract_test_trace_name(frames_by_thread, &self.current_thread_id)
            .or_else(|| utils::extract_http_trace_name(frames_by_thread, &self.current_thread_id))
    }

    fn build_trace_inner(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        let frames_by_thread = self.frames_by_thread.get(py).take();
        let trace_id = self.trace_id.get(py).borrow().clone();

        // Extract trace name if one wasn't explicitly set
        let trace_name = if self.trace_name.is_none() {
            self._set_trace_name(&frames_by_thread)
        } else {
            self.trace_name.clone()
        };

        utils::build_trace(
            py,
            frames_by_thread,
            self.threads.get(py).take(),
            &trace_id,
            trace_name,
            &self.source,
            self.current_thread_id.clone(),
            self.timestamp,
            &self.config,
        )
    }

    fn push_frames_call(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
        frame_types: Vec<String>,
    ) -> Result<(), PyErr> {
        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                if frame_type.as_str() == "start_test" {
                    frames.drain(..index);
                    self.start_test(py)
                }
            }
        }

        self.push_frame_data(py, frames);
        Ok(())
    }

    fn push_frames_return(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
        frame_types: &mut [String],
    ) -> Result<(), PyErr> {
        frames.reverse();
        frame_types.reverse();
        if self.one_trace_per_test {
            for (index, frame_type) in frame_types.iter().enumerate() {
                if frame_type.as_str() == "end_test" {
                    let mut before: Vec<SerializedFrame> = frames.drain(..index + 1).collect();
                    self.push_frame_data(py, &mut before);
                    self.save(py)?;
                }
            }
        }

        self.push_frame_data(py, frames);
        Ok(())
    }

    fn push_frame_data(
        &self,
        py: Python,
        frames: &mut Vec<SerializedFrame>,
    ) {
        let threading = PyModule::import_bound(py, "threading").expect("Failed to import threading module");
        let current_thread = threading.call_method0("current_thread").expect("Failed to get current_thread");
        let thread_id = utils::get_thread_id(&current_thread, py).unwrap();

        self.threads.get(py).borrow_mut().entry(thread_id.clone()).or_insert_with(|| current_thread.into());

        self.frames_by_thread
            .get(py)
            .borrow_mut()
            .entry(thread_id)
            .or_insert_with(Vec::new)
            .append(frames);
    }

    fn start_test(&self, py: Python) {
        // Set a new `self.trace_id`.
        let trace_id = utils::trace_id();
        let mut self_trace_id = self.trace_id.get(py).borrow_mut();
        *self_trace_id = trace_id;

        // Clear `frames_by_thread` of earlier frames.
        let mut frames_by_thread = self.frames_by_thread.get(py).borrow_mut();
        *frames_by_thread = HashMap::new();
    }

    /// Check if we should exclude the current frame from the trace using Kolo's builtin filters.
    fn process_default_ignore_frames(&self, py: Python, co_filename: &str) -> Result<bool, PyErr> {
        if filters::library_filter(co_filename)
            | filters::frozen_filter(co_filename)
            | filters::kolo_filter(co_filename)
            | filters::exec_filter(co_filename)
            | filters::pytest_generated_filter(co_filename)
        {
            Ok(true)
        } else {
            filters::attrs_filter_monitoring(py, co_filename)
        }
    }

    /// Check if we should include the current frame in the trace.
    fn include_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        Ok(self.include_frames.check(filename) | !self.ignore_frame(py, filename)?)
    }

    /// Check if we should exclude the current frame from the trace.
    fn ignore_frame(&self, py: Python, filename: &str) -> Result<bool, PyErr> {
        Ok(self.process_default_ignore_frames(py, filename)? | self.ignore_frames.check(filename))
    }

    fn log_error(&self, py: Python, err: PyErr) {
        let logging = PyModule::import_bound(py, "logging").unwrap();
        let logger = logging.call_method1("getLogger", ("kolo",)).unwrap();

        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("exc_info", err).unwrap();

        logger
            .call_method("warning", ("Unexpected exception in Rust.",), Some(&kwargs))
            .unwrap();
    }

    fn return_or_log(&self, py: Python, value: Result<Option<Py<PyAny>>, PyErr>) -> Py<PyAny> {
        match value {
            Ok(Some(disable)) => disable,
            Ok(None) => py.None(),
            Err(err) => {
                self.log_error(py, err);
                py.None()
            }
        }
    }
}

#[pymethods]
impl KoloMonitor {
    fn save(&self, py: Python) -> Result<(), PyErr> {
        let trace = self.build_trace_inner(py)?;
        let kwargs = PyDict::new_bound(py);
        kwargs.set_item("timeout", self.sqlite_busy_timeout)?;
        kwargs.set_item("msgpack", trace)?;

        let trace_id = self.trace_id.get(py).borrow().clone();
        let db = PyModule::import_bound(py, "kolo.db")?;
        let save = db.getattr(intern!(py, "save_trace_in_sqlite"))?;
        save.call((&self.db_path, &trace_id), Some(&kwargs))?;
        Ok(())
    }

    fn build_trace(&self, py: Python) -> Result<Py<PyBytes>, PyErr> {
        self.build_trace_inner(py)
    }

    fn monitor_pystart(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(py, self.monitor(code, utils::Arg::None, Event::Call))
    }

    fn monitor_pyreturn(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        retval: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Argument(retval), Event::Return),
        )
    }

    fn monitor_pyunwind(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        exception: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Exception(exception), Event::Unwind),
        )
    }

    fn monitor_pyresume(&self, code: &Bound<'_, PyCode>, _instruction_offset: usize) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(py, self.monitor(code, utils::Arg::None, Event::Resume))
    }

    fn monitor_pyyield(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        retval: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Argument(retval), Event::Yield),
        )
    }

    fn monitor_pythrow(
        &self,
        code: &Bound<'_, PyCode>,
        _instruction_offset: usize,
        exception: &Bound<'_, PyAny>,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(
            py,
            self.monitor(code, utils::Arg::Exception(exception), Event::Throw),
        )
    }

    fn monitor_instruction(
        &self,
        code: &Bound<'_, PyCode>,
        instruction_offset: usize,
    ) -> Py<PyAny> {
        let py = code.py();
        if let Err(err) = self.process_assignment(py) {
            self.log_error(py, err);
        }
        self.return_or_log(py, self._monitor_instruction(code, instruction_offset))
    }
}
