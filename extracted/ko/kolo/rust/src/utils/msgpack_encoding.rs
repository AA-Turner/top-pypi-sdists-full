use hashbrown::HashMap;
use pyo3::prelude::*;
use pyo3::types::{PyAny, PyBool, PyBytes, PyFloat, PyInt, PyString};
use rmpv::Value as RmpvValue;

use super::frame_store::SerializedFrame;
use super::frame_writer::UserCodeCallSite;
use super::value_serializer::Serializer;

/// Write a key, value pair of a msgpack map where the value is a string or None.
pub(super) fn write_str_pair(buf: &mut Vec<u8>, key: &str, value: Option<&str>) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    match value {
        Some(value) => rmp::encode::write_str(buf, value).expect("Writing to memory, not I/O"),
        None => rmp::encode::write_nil(buf).expect("Writing to memory, not I/O"),
    };
}

pub(super) fn write_frame_path_pair(buf: &mut Vec<u8>, relative_path: &str, lineno: usize) {
    let mut digits = [0_u8; 20];
    let mut start = digits.len();
    let mut remaining = lineno;
    loop {
        start -= 1;
        digits[start] = b'0' + (remaining % 10) as u8;
        remaining /= 10;
        if remaining == 0 {
            break;
        }
    }
    let digits = &digits[start..];
    let path_len = relative_path.len() + 1 + digits.len();

    rmp::encode::write_str(buf, "path").expect("Writing to memory, not I/O");
    rmp::encode::write_str_len(
        buf,
        path_len
            .try_into()
            .expect("frame path length should fit in u32"),
    )
    .expect("Writing to memory, not I/O");
    buf.extend_from_slice(relative_path.as_bytes());
    buf.push(b':');
    buf.extend_from_slice(digits);
}

pub(super) fn write_frame_qualname_pair(buf: &mut Vec<u8>, module: &str, co_qualname: &str) {
    let qualname_len = module.len() + 1 + co_qualname.len();

    rmp::encode::write_str(buf, "qualname").expect("Writing to memory, not I/O");
    rmp::encode::write_str_len(
        buf,
        qualname_len
            .try_into()
            .expect("frame qualname length should fit in u32"),
    )
    .expect("Writing to memory, not I/O");
    buf.extend_from_slice(module.as_bytes());
    buf.push(b'.');
    buf.extend_from_slice(co_qualname.as_bytes());
}

/// Write a key, value pair of a msgpack map where the value is an integer or None.
pub(super) fn write_int_pair(buf: &mut Vec<u8>, key: &str, value: Option<usize>) {
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
pub(super) fn write_f64_pair(buf: &mut Vec<u8>, key: &str, value: f64) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    rmp::encode::write_f64(buf, value).expect("Writing to memory, not I/O");
}

pub(super) fn write_bool_pair(buf: &mut Vec<u8>, key: &str, value: bool) {
    rmp::encode::write_str(buf, key).expect("Writing to memory, not I/O");
    rmp::encode::write_bool(buf, value).expect("Writing to memory, not I/O");
}

/// Write a msgpack array from a vector of already valid msgpack frames.
pub(super) fn write_raw_frame_slice(buf: &mut Vec<u8>, frames: &[SerializedFrame]) {
    rmp::encode::write_array_len(buf, frames.len() as u32).expect("Writing to memory, not I/O");
    for frame in frames {
        buf.extend_from_slice(frame);
    }
}

fn write_raw_frames(buf: &mut Vec<u8>, frames: Vec<SerializedFrame>) {
    write_raw_frame_slice(buf, &frames);
}

/// Serialize the `user_code_call_site` of the trace as msgpack.
///
/// Must be called in the context of writing a msgpack map.
pub(super) fn write_user_code_call_site(
    buf: &mut Vec<u8>,
    user_code_call_site: Option<&UserCodeCallSite>,
) {
    rmp::encode::write_str(buf, "user_code_call_site").expect("Writing to memory, not I/O");
    let Some(user_code_call_site) = user_code_call_site else {
        rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
        return;
    };

    rmp::encode::write_map_len(buf, 2).expect("Writing to memory, not I/O");
    write_str_pair(
        buf,
        "call_frame_id",
        Some(&user_code_call_site.call_frame_id),
    );
    rmp::encode::write_str(buf, "line_number").expect("Writing to memory, not I/O");
    rmp::encode::write_sint(buf, i64::from(user_code_call_site.line_number))
        .expect("Writing to memory, not I/O");
}

/// Serialize the command line arguments of the Python program as msgpack.
///
/// Must be called in the context of writing a msgpack map.
/// The first value written is the `command_line_args` key. The other values are the command
/// line argument list as the map value.
pub(super) fn write_argv(buf: &mut Vec<u8>, argv: Vec<String>) {
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
pub(super) fn write_frames_of_interest(
    buf: &mut Vec<u8>,
    frames_of_interest: Vec<SerializedFrame>,
) {
    rmp::encode::write_str(buf, "frames_of_interest").expect("Writing to memory, not I/O");
    write_raw_frames(buf, frames_of_interest);
}

/// Serialize the `frames` of the trace as msgpack.
///
/// Must be called in the context of writing a msgpack map.
/// The first value written is the `frames` key. The other values are a map from `thread_id` to
/// a list of frames.
pub(super) fn write_frames(buf: &mut Vec<u8>, frames: HashMap<String, Vec<SerializedFrame>>) {
    rmp::encode::write_str(buf, "frames").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, frames.len() as u32).expect("Writing to memory, not I/O");
    for (thread_id, frames) in frames {
        rmp::encode::write_str(buf, &thread_id).expect("Writing to memory, not I/O");
        write_raw_frames(buf, frames);
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
pub(super) fn write_meta(
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
    rmp::encode::write_map_len(buf, environment.len() as u32).expect("Writing to memory, not I/O");
    for (key, value) in environment {
        write_str_pair(buf, key, Some(value));
    }

    // Serialize 'config' as a nested map with `RmpvValue` types
    rmp::encode::write_str(buf, "config").expect("Writing to memory, not I/O");
    rmp::encode::write_map_len(buf, config.len() as u32).expect("Writing to memory, not I/O");
    for (key, value) in config {
        write_rmpv_pair(buf, key, value);
    }
}

pub(super) fn write_assign_tuple(
    buf: &mut Vec<u8>,
    serializer: &Serializer,
    assign: (&str, Bound<'_, PyAny>),
    lightweight_repr: bool,
) -> Result<(), PyErr> {
    const PY_TUPLE_EXTENSION_TYPE: i8 = 6;
    let (variable, assigned) = assign;
    let py = assigned.py();

    let mut inner: Vec<u8> = vec![];
    rmp::encode::write_array_len(&mut inner, 2).expect("Writing to memory, not I/O");
    rmp::encode::write_str(&mut inner, variable).expect("Writing to memory, not I/O");
    let assigned_start = inner.len();
    if !write_exact_msgpack_scalar(&assigned, &mut inner) {
        // Exact scalar probes never invoke user code and write nothing on
        // failure. Unsupported values therefore enter the established Python
        // serializer atomically, preserving subclass behavior, repr ordering,
        // and serialization errors.
        debug_assert_eq!(inner.len(), assigned_start);
        inner.truncate(assigned_start);
        serializer.dump_msgpack_into(py, &assigned, lightweight_repr, &mut inner)?;
    }

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

/// Write the exact scalar types that msgpack handles without its Python
/// `default` callback. This intentionally excludes containers and subclasses:
/// line assignments need a bounded, side-effect-free probe before falling
/// back atomically to the established Python serializer. Keep these byte
/// choices aligned with the scalar arms of `NativeMsgpackEncoder::write`.
pub(super) fn write_exact_msgpack_scalar(value: &Bound<'_, PyAny>, buf: &mut Vec<u8>) -> bool {
    if value.is_none() {
        rmp::encode::write_nil(buf).expect("Writing to memory, not I/O");
        return true;
    }
    if value.is_exact_instance_of::<PyBool>() {
        let value = value
            .extract::<bool>()
            .expect("an exact bool extracts as bool");
        rmp::encode::write_bool(buf, value).expect("Writing to memory, not I/O");
        return true;
    }
    if value.is_exact_instance_of::<PyInt>() {
        if let Ok(value) = value.extract::<i64>() {
            rmp::encode::write_sint(buf, value).expect("Writing to memory, not I/O");
            return true;
        }
        if let Ok(value) = value.extract::<u64>() {
            rmp::encode::write_uint(buf, value).expect("Writing to memory, not I/O");
            return true;
        }
        return false;
    }
    if value.is_exact_instance_of::<PyFloat>() {
        let value = value
            .extract::<f64>()
            .expect("an exact float extracts as f64");
        rmp::encode::write_f64(buf, value).expect("Writing to memory, not I/O");
        return true;
    }
    if value.is_exact_instance_of::<PyString>() {
        let value = value
            .cast::<PyString>()
            .expect("exact string type already checked");
        let Ok(value) = value.to_str() else {
            return false;
        };
        if u32::try_from(value.len()).is_err() {
            return false;
        }
        rmp::encode::write_str(buf, value).expect("Writing to memory, not I/O");
        return true;
    }
    if value.is_exact_instance_of::<PyBytes>() {
        let value = value
            .cast::<PyBytes>()
            .expect("exact bytes type already checked");
        if u32::try_from(value.as_bytes().len()).is_err() {
            return false;
        }
        rmp::encode::write_bin(buf, value.as_bytes()).expect("Writing to memory, not I/O");
        return true;
    }

    false
}
