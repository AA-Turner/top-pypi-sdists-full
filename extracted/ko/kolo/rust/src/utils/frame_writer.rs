use pyo3::exceptions::{PyAttributeError, PyOSError};
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyFrame, PyString, PyStringMethods};
use std::sync::atomic::{AtomicBool, Ordering};

use super::frame_path::FramePathCache;
use super::frame_store::STRING_KEY;
use super::frame_types::{get_qualname, get_qualname_module, timestamp, Arg, Event};
use super::msgpack_encoding::{
    write_f64_pair, write_frame_path_pair, write_frame_qualname_pair, write_str_pair,
    write_user_code_call_site,
};
use super::value_serializer::{NativeMsgpackEncoder, Serializer, ValueInterningContext};

#[allow(clippy::too_many_arguments)]
pub fn write_frame_with_serializer(
    buf: &mut Vec<u8>,
    pyframe: &Bound<'_, PyFrame>,
    serializer: &Serializer,
    frame_paths: &FramePathCache,
    user_code_call_site: Option<UserCodeCallSite>,
    arg: Arg,
    event: Event,
    name: &str,
    frame_id: &str,
    lightweight_repr: bool,
    omit_return_locals: bool,
    native_root: bool,
    value_interning: Option<ValueInterningContext<'_>>,
) -> Result<(), PyErr> {
    write_frame_with_serializer_inner(
        buf,
        pyframe,
        serializer,
        frame_paths,
        user_code_call_site,
        arg,
        event,
        name,
        frame_id,
        lightweight_repr,
        omit_return_locals,
        native_root,
        None,
        value_interning,
    )
}

#[allow(clippy::too_many_arguments)]
pub fn write_frame_with_cached_code_metadata(
    buf: &mut Vec<u8>,
    pyframe: &Bound<'_, PyFrame>,
    serializer: &Serializer,
    frame_paths: &FramePathCache,
    user_code_call_site: Option<UserCodeCallSite>,
    arg: Arg,
    event: Event,
    name: &str,
    frame_id: &str,
    lightweight_repr: bool,
    omit_return_locals: bool,
    native_root: bool,
    cached_code_metadata: (&str, Option<&str>, Option<&AtomicBool>),
    value_interning: Option<ValueInterningContext<'_>>,
) -> Result<(), PyErr> {
    write_frame_with_serializer_inner(
        buf,
        pyframe,
        serializer,
        frame_paths,
        user_code_call_site,
        arg,
        event,
        name,
        frame_id,
        lightweight_repr,
        omit_return_locals,
        native_root,
        Some(cached_code_metadata),
        value_interning,
    )
}

#[allow(clippy::too_many_arguments)]
fn write_frame_with_serializer_inner(
    buf: &mut Vec<u8>,
    pyframe: &Bound<'_, PyFrame>,
    serializer: &Serializer,
    frame_paths: &FramePathCache,
    user_code_call_site: Option<UserCodeCallSite>,
    arg: Arg,
    event: Event,
    name: &str,
    frame_id: &str,
    lightweight_repr: bool,
    omit_return_locals: bool,
    native_root: bool,
    cached_code_metadata: Option<(&str, Option<&str>, Option<&AtomicBool>)>,
    value_interning: Option<ValueInterningContext<'_>>,
) -> Result<(), PyErr> {
    let py = pyframe.py();
    let none = py.None().into_bound(py);
    let (arg, arg_key) = match arg {
        Arg::None => (&none, "arg"),
        Arg::Argument(arg) => (arg, "arg"),
        Arg::Exception(exception) => (exception, "exception"),
    };

    // Keep the established error propagation for the five fallible PyFrame
    // reads below. Their failure arms are not injectable on an exact CPython
    // frame, while the observable path, qualname, fallback, and rollback
    // branches are covered directly.
    let (
        path,
        cached_path,
        mut qualname,
        cached_qualname,
        code_id,
        native_eligible,
        cached_native_eligibility,
    ) = match cached_code_metadata {
        Some((relative_path, co_qualname, native_eligibility)) => {
            let lineno = pyframe
                .getattr(intern!(py, "f_lineno"))
                .and_then(|lineno| lineno.extract::<usize>())?;
            let (qualname, cached_qualname) = match co_qualname {
                Some(co_qualname) => (None, Some((get_qualname_module(pyframe, py)?, co_qualname))),
                None => (get_qualname(pyframe, py)?, None),
            };
            (
                None,
                Some((relative_path, lineno)),
                qualname,
                cached_qualname,
                None,
                native_eligibility
                    .map(|eligible| eligible.load(Ordering::Relaxed))
                    .unwrap_or(false),
                native_eligibility,
            )
        }
        None => {
            let (path, code_id, native_eligible) =
                frame_paths.frame_path_and_native_eligibility(pyframe)?;
            (
                Some(path),
                None,
                get_qualname(pyframe, py)?,
                None,
                Some(code_id),
                native_eligible,
                None,
            )
        }
    };
    let locals = get_locals(pyframe, event, omit_return_locals)?;

    if native_root && !lightweight_repr && native_eligible {
        let native_start = buf.len();
        let mut encoder = match value_interning {
            Some(context) => NativeMsgpackEncoder::with_value_interning(context),
            _ => NativeMsgpackEncoder::new(),
        };

        rmp::encode::write_map_len(buf, 10).expect("Writing to memory, not I/O");
        match cached_path {
            Some((relative_path, lineno)) => write_frame_path_pair(buf, relative_path, lineno),
            None => write_str_pair(buf, "path", path.as_deref()),
        }
        write_str_pair(buf, "co_name", Some(name));
        let wrote_cached_qualname = cached_qualname
            .as_ref()
            .and_then(|(module, co_qualname)| {
                module
                    .cast_exact::<PyString>()
                    .ok()
                    .and_then(|module| module.to_str().ok())
                    .map(|module| write_frame_qualname_pair(buf, module, co_qualname))
            })
            .is_some();
        if !wrote_cached_qualname {
            qualname = qualname.or_else(|| {
                cached_qualname
                    .as_ref()
                    .map(|(module, co_qualname)| format!("{module}.{co_qualname}"))
            });
            write_str_pair(buf, "qualname", qualname.as_deref());
        }
        write_str_pair(buf, "event", Some(event.into()));
        write_str_pair(buf, "frame_id", Some(frame_id));
        rmp::encode::write_str(buf, arg_key).expect("Writing to memory, not I/O");

        let arg_complete = encoder.write(arg, buf, 0);
        if let Some(error) = encoder.writer_circuit_error.take() {
            buf.truncate(native_start);
            return Err(PyOSError::new_err(error));
        }
        if arg_complete {
            rmp::encode::write_str(buf, "locals").expect("Writing to memory, not I/O");
            let locals_complete = encoder.write(&locals, buf, 0);
            if let Some(error) = encoder.writer_circuit_error.take() {
                buf.truncate(native_start);
                return Err(PyOSError::new_err(error));
            }
            if locals_complete {
                write_f64_pair(buf, "timestamp", timestamp());
                write_str_pair(buf, "type", Some("frame"));
                write_user_code_call_site(buf, user_code_call_site.as_ref());
                return Ok(());
            }
        }

        // The native probe writes directly into the destination arena. Roll
        // back the incomplete root before the established all-Python fallback
        // so callers still observe an atomic frame append.
        buf.truncate(native_start);

        if let Some(native_eligibility) = cached_native_eligibility {
            // The diagnostic cache getter pairs this one-time transition with
            // Acquire. The ordinary hot-path eligibility probe remains Relaxed.
            native_eligibility.store(false, Ordering::Release);
        } else if let Some(code_id) = code_id {
            frame_paths.mark_native_msgpack_unsupported(py, code_id);
        }

        // Atomic fallback: pass the complete frame map to the existing Python
        // serializer after discarding the incomplete native root above.
        let path = path.unwrap_or_else(|| {
            let (relative_path, lineno) = cached_path.expect("cached frame path exists");
            format!("{relative_path}:{lineno}")
        });
        qualname = qualname.or_else(|| {
            cached_qualname
                .as_ref()
                .map(|(module, co_qualname)| format!("{module}.{co_qualname}"))
        });
        let frame_data = PyDict::new(py);
        frame_data.set_item("path", &path)?;
        frame_data.set_item("co_name", name)?;
        frame_data.set_item("qualname", qualname.as_deref())?;
        frame_data.set_item("event", <Event as Into<&str>>::into(event))?;
        frame_data.set_item("frame_id", frame_id)?;
        frame_data.set_item(arg_key, arg)?;
        frame_data.set_item("locals", &locals)?;
        frame_data.set_item("timestamp", timestamp())?;
        frame_data.set_item("type", "frame")?;
        frame_data.set_item(
            "user_code_call_site",
            user_code_call_site
                .as_ref()
                .map(|call_site| call_site.into_pydict(py)),
        )?;
        return serializer.dump_msgpack_into(py, frame_data.as_any(), false, buf);
    }

    // A code object already known to be ineligible skips native encoding and
    // uses the established Python serializer path. The event that discovered
    // unsupported data still took the atomic whole-root fallback above.
    // Serialize frame data as msgpack.
    let path = path.unwrap_or_else(|| {
        let (relative_path, lineno) = cached_path.expect("cached frame path exists");
        format!("{relative_path}:{lineno}")
    });
    qualname = qualname.or_else(|| {
        cached_qualname
            .as_ref()
            .map(|(module, co_qualname)| format!("{module}.{co_qualname}"))
    });
    let arg = serializer.dump_msgpack_bytes(py, arg, lightweight_repr)?;
    let locals = serializer.dump_msgpack_bytes(py, &locals, lightweight_repr)?;

    // Reserve once for the already-known payloads and string fields. The fixed
    // allowance covers the ten map keys, msgpack headers, timestamp, type, and
    // an ordinary user-code call site. This avoids repeatedly growing every
    // per-event frame buffer without retaining a blanket 1 KiB allocation for
    // small frames.
    buf.reserve(
        arg.as_bytes().len()
            + locals.as_bytes().len()
            + path.len()
            + name.len()
            + qualname.as_deref().map_or(0, str::len)
            + frame_id.len()
            + 192,
    );

    // The map length must match the number of key, value pairs written next exactly.
    rmp::encode::write_map_len(buf, 10).expect("Writing to memory, not I/O");

    write_str_pair(buf, "path", Some(&path));
    write_str_pair(buf, "co_name", Some(name));
    write_str_pair(buf, "qualname", qualname.as_deref());
    write_str_pair(buf, "event", Some(event.into()));
    write_str_pair(buf, "frame_id", Some(frame_id));
    rmp::encode::write_str(buf, arg_key).expect("Writing to memory, not I/O");
    buf.extend_from_slice(arg.as_bytes());
    rmp::encode::write_str(buf, "locals").expect("Writing to memory, not I/O");
    buf.extend_from_slice(locals.as_bytes());
    write_f64_pair(buf, "timestamp", timestamp());
    write_str_pair(buf, "type", Some("frame"));
    write_user_code_call_site(buf, user_code_call_site.as_ref());
    Ok(())
}

pub struct UserCodeCallSite {
    pub call_frame_id: String,
    pub line_number: i32,
}

impl UserCodeCallSite {
    pub fn into_pydict<'py>(&self, py: Python<'py>) -> Bound<'py, PyDict> {
        let call_site = PyDict::new(py);
        call_site
            .set_item("call_frame_id", &self.call_frame_id)
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

    build_user_code_call_site(call_frame, call_frame_id)
}

pub(super) fn build_user_code_call_site(
    call_frame: &Bound<'_, PyAny>,
    call_frame_id: &str,
) -> Result<Option<UserCodeCallSite>, PyErr> {
    let pyframe = call_frame.downcast::<PyFrame>()?;
    let py = pyframe.py();
    Ok(Some(UserCodeCallSite {
        call_frame_id: call_frame_id.to_string(),
        line_number: pyframe.getattr(intern!(py, "f_lineno"))?.extract()?,
    }))
}

/// Load Kolo's version from Python.
pub(super) fn kolo_version(py: Python) -> Result<String, PyErr> {
    PyModule::import(py, "kolo.version")?
        .getattr(intern!(py, "__version__"))?
        .extract::<String>()
}

/// Get the current git commit sha from Python.
pub(super) fn git_commit_sha(py: Python) -> Result<Option<String>, PyErr> {
    PyModule::import(py, "kolo.git")?
        .getattr(intern!(py, "COMMIT_SHA"))?
        .extract::<Option<String>>()
}

/// Get the command line arguments of the traced program from Python.
pub(super) fn get_argv(py: Python) -> Result<Vec<String>, PyErr> {
    PyModule::import(py, "sys")?
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

    // In Python 3.13+, f_locals might be a proxy object (FrameLocalsProxy) instead of a dict
    // Try to downcast to PyDict, if that fails, convert to dict
    let locals = match locals.downcast::<PyDict>() {
        Ok(dict) => dict.clone(),
        Err(_) => {
            // Convert to dict by calling dict() constructor on the proxy
            let dict_type = py.get_type::<PyDict>();
            dict_type.call1((&locals,))?.downcast_into::<PyDict>()?
        }
    };

    let builtins_key = intern!(py, "__builtins__");
    let result = match locals
        .get_item(builtins_key)
        .expect("locals.get(\"__builtins__\") should not raise.")
    {
        Some(_) => {
            let locals = locals.copy().unwrap();
            locals.del_item(builtins_key).unwrap();
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
        println!("Kolo warning: thread has no id: {}", thread_name);
        "no_thread_id".to_string()
    };

    Ok(thread_id)
}
