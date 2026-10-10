use pyo3::exceptions::{PyAttributeError, PyRecursionError};
use pyo3::ffi;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict, PyFrame, PyString, PyStringMethods};
use std::sync::atomic::{AtomicBool, Ordering};

use super::frame_locals::fast_locals_dict;
use super::frame_path::{
    frame_line_number_i32_with, frame_line_number_with, CodeLines, FramePathCache,
};
use super::frame_store::STRING_KEY;
use super::frame_types::{get_qualname, get_qualname_module, timestamp, Arg, Event, FrameId};
use super::msgpack_encoding::{
    write_f64_pair, write_frame_path_pair, write_frame_qualname_pair, write_str_pair,
    write_user_code_call_site,
};
use super::value_serializer::{Encoded, NativeMsgpackEncoder, Serializer, ValueInterningContext};

/// Immutable per-code metadata a caller already holds: the relative path,
/// `co_qualname`, the native-eligibility diagnostic and the line table.
pub type CachedCodeMetadata<'a> = (
    &'a str,
    Option<&'a str>,
    Option<&'a AtomicBool>,
    Option<&'a CodeLines>,
);

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
    value_interning: Option<ValueInterningContext<'_>>,
    max_value_bytes: Option<usize>,
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
        None,
        value_interning,
        max_value_bytes,
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
    cached_code_metadata: CachedCodeMetadata<'_>,
    value_interning: Option<ValueInterningContext<'_>>,
    max_value_bytes: Option<usize>,
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
        Some(cached_code_metadata),
        value_interning,
        max_value_bytes,
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
    cached_code_metadata: Option<CachedCodeMetadata<'_>>,
    value_interning: Option<ValueInterningContext<'_>>,
    max_value_bytes: Option<usize>,
) -> Result<(), PyErr> {
    let py = pyframe.py();
    let none = py.None().into_bound(py);
    let (arg, arg_key) = match arg {
        Arg::None => (&none, "arg"),
        Arg::Argument(arg) => (arg, "arg"),
        Arg::Exception(exception) => (exception, "exception"),
    };
    // Only exits are ever recorded without their values.
    if matches!(event, Event::Return | Event::Unwind | Event::Yield) && super::values_omitted() {
        return write_frame_without_values(
            buf,
            pyframe,
            frame_paths,
            user_code_call_site.as_ref(),
            arg_key,
            event,
            name,
            frame_id,
            cached_code_metadata,
        );
    }

    // Keep the established error propagation for the five fallible PyFrame
    // reads below. Their failure arms are not injectable on an exact CPython
    // frame, while the observable path, qualname, and rollback branches are
    // covered directly.
    let (path, cached_path, mut qualname, cached_qualname, code_id, native_eligibility) =
        match cached_code_metadata {
            Some((relative_path, co_qualname, native_eligibility, code_lines)) => {
                let lineno = frame_line_number_with(pyframe, code_lines)?;
                let (qualname, cached_qualname) = match co_qualname {
                    Some(co_qualname) => {
                        (None, Some((get_qualname_module(pyframe, py)?, co_qualname)))
                    }
                    None => (get_qualname(pyframe, py)?, None),
                };
                (
                    None,
                    Some((relative_path, lineno)),
                    qualname,
                    cached_qualname,
                    None,
                    native_eligibility.map(|eligible| (eligible.load(Ordering::Relaxed), eligible)),
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
                    native_eligible.then_some(code_id),
                    None,
                )
            }
        };
    let locals = match get_locals(pyframe, event, omit_return_locals) {
        Ok(locals) => locals,
        Err(error) => {
            return without_values_at_recursion_limit(
                error,
                buf,
                pyframe,
                frame_paths,
                user_code_call_site.as_ref(),
                arg_key,
                event,
                name,
                frame_id,
                cached_code_metadata,
            )
        }
    };

    let frame_start = buf.len();
    let mut encoder =
        NativeMsgpackEncoder::with_value_interning(serializer, lightweight_repr, value_interning);
    encoder.set_value_budget(max_value_bytes);

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
    let mut encoded = encoder
        .encode_value(arg, buf)
        .map(|_| ())
        .map_err(|error| error.into_pyerr());
    if encoded.is_ok() {
        rmp::encode::write_str(buf, "locals").expect("Writing to memory, not I/O");
        encoded = encode_locals(&mut encoder, &locals, buf);
    }
    if let Err(error) = encoded {
        buf.truncate(frame_start);
        return without_values_at_recursion_limit(
            error,
            buf,
            pyframe,
            frame_paths,
            user_code_call_site.as_ref(),
            arg_key,
            event,
            name,
            frame_id,
            cached_code_metadata,
        );
    }
    write_f64_pair(buf, "timestamp", timestamp());
    write_str_pair(buf, "type", Some("frame"));
    write_user_code_call_site(buf, user_code_call_site.as_ref());

    if encoder.used_default_hook() {
        // Diagnostics only: remember code whose values needed the msgpack
        // default hook (formerly routed to the Python serializer).
        if let Some((true, native_eligibility)) = native_eligibility {
            // The diagnostic cache getter pairs this one-time transition with
            // Acquire. The ordinary hot-path eligibility probe remains Relaxed.
            native_eligibility.store(false, Ordering::Release);
        } else if let Some(code_id) = code_id {
            frame_paths.mark_native_msgpack_unsupported(py, code_id);
        }
    }
    Ok(())
}

/// Encode `locals`. When the dict as a whole exceeds the value budget, the
/// budget applies to each variable instead, so one oversized local becomes a
/// truncation marker without losing the others.
fn encode_locals(
    encoder: &mut NativeMsgpackEncoder<'_>,
    locals: &Bound<'_, PyAny>,
    buf: &mut Vec<u8>,
) -> Result<(), PyErr> {
    let start = buf.len();
    let encoded = encoder
        .encode_value(locals, buf)
        .map_err(|error| error.into_pyerr())?;
    if encoded == Encoded::Complete {
        return Ok(());
    }
    let Ok(locals) = locals.cast_exact::<PyDict>() else {
        return Ok(());
    };
    buf.truncate(start);
    let items = locals.items();
    rmp::encode::write_map_len(buf, items.len() as u32).expect("Writing to memory, not I/O");
    for item in items.iter() {
        let (name, value) = item.extract::<(Bound<'_, PyAny>, Bound<'_, PyAny>)>()?;
        encoder
            .encode_unbudgeted(&name, buf)
            .map_err(|error| error.into_pyerr())?;
        encoder
            .encode_value(&value, buf)
            .map_err(|error| error.into_pyerr())?;
    }
    Ok(())
}

/// `error`, unless it comes from the recursion limit: then the frame is
/// written without its values instead (see `write_frame_without_values`).
#[cold]
#[inline(never)]
#[allow(clippy::too_many_arguments)]
fn without_values_at_recursion_limit(
    error: PyErr,
    buf: &mut Vec<u8>,
    pyframe: &Bound<'_, PyFrame>,
    frame_paths: &FramePathCache,
    user_code_call_site: Option<&UserCodeCallSite>,
    arg_key: &str,
    event: Event,
    name: &str,
    frame_id: &str,
    cached_code_metadata: Option<CachedCodeMetadata<'_>>,
) -> Result<(), PyErr> {
    if !hit_recursion_limit(pyframe.py(), &error) {
        return Err(error);
    }
    write_frame_without_values(
        buf,
        pyframe,
        frame_paths,
        user_code_call_site,
        arg_key,
        event,
        name,
        frame_id,
        cached_code_metadata,
    )
}

/// Write a frame without its argument, exception and locals, which there is
/// too little stack (or recursion depth) left to serialize: recorded anyway,
/// so its entry and exit still pair. Readers expect locals to be a mapping.
/// Kept out of line so the common path above stays as it was.
#[cold]
#[inline(never)]
#[allow(clippy::too_many_arguments)]
fn write_frame_without_values(
    buf: &mut Vec<u8>,
    pyframe: &Bound<'_, PyFrame>,
    frame_paths: &FramePathCache,
    user_code_call_site: Option<&UserCodeCallSite>,
    arg_key: &str,
    event: Event,
    name: &str,
    frame_id: &str,
    cached_code_metadata: Option<CachedCodeMetadata<'_>>,
) -> Result<(), PyErr> {
    let py = pyframe.py();
    // Everything fallible first, so a failure leaves `buf` untouched.
    let (path, lineno, qualname) = match cached_code_metadata {
        Some((relative_path, co_qualname, _, code_lines)) => {
            let lineno = frame_line_number_with(pyframe, code_lines)?;
            let qualname = match co_qualname {
                Some(co_qualname) => {
                    let module = get_qualname_module(pyframe, py)?;
                    Some(format!("{module}.{co_qualname}"))
                }
                None => get_qualname(pyframe, py)?,
            };
            (relative_path.to_string(), Some(lineno), qualname)
        }
        None => {
            let (path, _, _) = frame_paths.frame_path_and_native_eligibility(pyframe)?;
            (path, None, get_qualname(pyframe, py)?)
        }
    };
    rmp::encode::write_map_len(buf, 11).expect("Writing to memory, not I/O");
    match lineno {
        Some(lineno) => write_frame_path_pair(buf, &path, lineno),
        None => write_str_pair(buf, "path", Some(&path)),
    }
    write_str_pair(buf, "co_name", Some(name));
    write_str_pair(buf, "qualname", qualname.as_deref());
    write_str_pair(buf, "event", Some(event.into()));
    write_str_pair(buf, "frame_id", Some(frame_id));
    rmp::encode::write_str(buf, arg_key).expect("Writing to memory, not I/O");
    rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
    rmp::encode::write_str(buf, "locals").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, 0).expect("Writing to memory, not I/O");
    write_f64_pair(buf, "timestamp", timestamp());
    write_str_pair(buf, "type", Some("frame"));
    write_user_code_call_site(buf, user_code_call_site);
    write_str_pair(buf, "values_omitted", Some("stack_limit"));
    Ok(())
}

/// Whether `error` comes from CPython's recursion guard: a `RecursionError`,
/// or an error raised while handling one (the encoder's own fallback, which
/// then fails at the limit too). Only that close: an unrelated error further
/// down the chain is reported as before, not hidden behind a values-free
/// frame. Errors from user `__repr__`s never get here (the encoder records
/// those as values).
fn hit_recursion_limit(py: Python, error: &PyErr) -> bool {
    // An interrupt raised while a `RecursionError` was being handled has it
    // as context, but must still reach the program.
    if super::reaches_program(py, error) {
        return false;
    }
    let exception = error.value(py);
    if exception.is_instance_of::<PyRecursionError>() {
        return true;
    }
    // Safety: `exception` is a live exception instance; this returns a new
    // reference to its `__context__`, or NULL.
    let context = unsafe { ffi::PyException_GetContext(exception.as_ptr()) };
    unsafe { Bound::from_owned_ptr_or_opt(py, context) }
        .is_some_and(|context| context.is_instance_of::<PyRecursionError>())
}

pub struct UserCodeCallSite {
    pub(super) call_frame_id: FrameId,
    pub line_number: Option<i32>,
}

impl UserCodeCallSite {
    #[cfg(test)]
    pub(super) fn into_pydict<'py>(&self, py: Python<'py>) -> Bound<'py, PyDict> {
        let call_site = PyDict::new(py);
        call_site
            .set_item("call_frame_id", self.call_frame_id.as_str())
            .expect(STRING_KEY);
        call_site
            .set_item("line_number", self.line_number)
            .expect(STRING_KEY);
        call_site
    }
}

pub struct PluginUserCodeCallSite {
    call_frame_id: String,
    line_number: Option<i32>,
}

impl PluginUserCodeCallSite {
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
) -> Result<Option<PluginUserCodeCallSite>, PyErr> {
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

    let pyframe = call_frame.cast::<PyFrame>()?;
    Ok(Some(PluginUserCodeCallSite {
        call_frame_id: call_frame_id.clone(),
        line_number: frame_line_number_i32_with(pyframe, None)?,
    }))
}

pub(super) fn build_user_code_call_site(
    call_frame: &Bound<'_, PyAny>,
    call_frame_id: FrameId,
    code_lines: Option<&CodeLines>,
) -> Result<Option<UserCodeCallSite>, PyErr> {
    let pyframe = call_frame.cast::<PyFrame>()?;
    Ok(Some(UserCodeCallSite {
        call_frame_id,
        line_number: frame_line_number_i32_with(pyframe, code_lines)?,
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

    // Python 3.13+: snapshot optimized frames' fast locals directly instead
    // of copying a FrameLocalsProxy. The snapshot is a fresh dict we own.
    let (locals, owned) = match fast_locals_dict(frame)? {
        Some(dict) => (dict, true),
        None => {
            let locals = frame.getattr(intern!(py, "f_locals"))?;

            // In Python 3.13+, f_locals might be a proxy object (FrameLocalsProxy) instead of a dict
            // Try to downcast to PyDict, if that fails, convert to dict
            match locals.cast::<PyDict>() {
                Ok(dict) => (dict.clone(), false),
                Err(_) => {
                    // Convert to dict by calling dict() constructor on the proxy
                    let dict_type = py.get_type::<PyDict>();
                    (dict_type.call1((&locals,))?.cast_into::<PyDict>()?, true)
                }
            }
        }
    };

    let builtins_key = intern!(py, "__builtins__");
    let result = match locals
        .get_item(builtins_key)
        .expect("locals.get(\"__builtins__\") should not raise.")
    {
        Some(_) => {
            let locals = if owned {
                locals
            } else {
                locals.copy().unwrap()
            };
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
