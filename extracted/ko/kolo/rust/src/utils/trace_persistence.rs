use hashbrown::HashMap;
use pyo3::exceptions::PyOSError;
use pyo3::intern;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyTuple};
use pyo3::types::{PyDict, PyModule};
#[cfg(not(target_arch = "wasm32"))]
use std::io;
use std::sync::Arc;

use super::super::config;
#[cfg(not(target_arch = "wasm32"))]
use super::super::trace_container::{FrameStore, TraceCapture};
use super::frame_store::FrameSequence;
use super::frame_writer::{get_argv, git_commit_sha, kolo_version};
use super::msgpack_encoding::{
    write_argv, write_bool_pair, write_f64_pair, write_frames, write_frames_of_interest,
    write_int_pair, write_meta, write_str_pair,
};
use super::runtime_metadata::{collect_config, collect_environment};

pub(crate) struct PreparedV3Trace {
    pub(crate) thread_meta: Vec<(u32, Vec<u8>)>,
    pub(crate) metadata: Vec<u8>,
}

#[allow(clippy::too_many_arguments)]
pub(crate) fn prepare_v3_trace_from_parts(
    py: Python,
    threads: &HashMap<String, Py<PyAny>>,
    thread_tokens: &HashMap<String, u32>,
    trace_id: &str,
    trace_name: Option<String>,
    source: &str,
    current_thread_id: String,
    timestamp: f64,
    config: &config::Config,
    use_monitoring: bool,
    root_trace_id: Option<&str>,
) -> Result<PreparedV3Trace, PyErr> {
    let version = kolo_version(py)?;
    let commit_sha = git_commit_sha(py)?;
    let argv = get_argv(py)?;
    let environment = collect_environment(py)?;
    let filtered_config = collect_config(py, config, use_monitoring)?;

    let mut metadata = Vec::with_capacity(2048);
    let map_len = if root_trace_id.is_some() { 10 } else { 9 };
    rmp::encode::write_map_len(&mut metadata, map_len).expect("Writing to memory, not I/O");
    write_str_pair(&mut metadata, "trace_id", Some(trace_id));
    write_str_pair(&mut metadata, "trace_name", trace_name.as_deref());
    write_str_pair(&mut metadata, "current_thread_id", Some(&current_thread_id));
    write_f64_pair(&mut metadata, "timestamp", timestamp);
    write_str_pair(&mut metadata, "current_commit_sha", commit_sha.as_deref());
    if let Some(root_id) = root_trace_id {
        write_str_pair(&mut metadata, "root_trace_id", Some(root_id));
    }
    write_meta(
        &mut metadata,
        &version,
        source,
        &environment,
        &filtered_config,
    );
    write_argv(&mut metadata, argv);
    write_frames_of_interest(&mut metadata, vec![]);
    write_frames(&mut metadata, HashMap::new());

    let mut thread_meta = Vec::with_capacity(threads.len());
    for (thread_id, thread) in threads {
        let token = *thread_tokens.get(thread_id).ok_or_else(|| {
            pyo3::exceptions::PyRuntimeError::new_err(format!(
                "missing v3 thread token for {thread_id}"
            ))
        })?;
        let mut payload = Vec::with_capacity(256);
        rmp::encode::write_map_len(&mut payload, 6).expect("Writing to memory, not I/O");
        write_str_pair(&mut payload, "thread_id", Some(thread_id));
        let name: String = thread.getattr(py, "name")?.extract(py)?;
        write_str_pair(&mut payload, "name", Some(&name));
        let ident: Option<usize> = thread
            .getattr(py, "ident")
            .ok()
            .and_then(|value| value.extract(py).ok())
            .flatten();
        write_int_pair(&mut payload, "ident", ident);
        let native_id: Option<usize> = thread
            .getattr(py, "native_id")
            .ok()
            .and_then(|value| value.extract(py).ok())
            .flatten();
        write_int_pair(&mut payload, "native_id", native_id);
        let daemon: bool = thread.getattr(py, "daemon")?.extract(py)?;
        write_bool_pair(&mut payload, "daemon", daemon);
        let is_alive: bool = thread.call_method0(py, "is_alive")?.extract(py)?;
        write_bool_pair(&mut payload, "is_alive", is_alive);
        thread_meta.push((token, payload));
    }
    Ok(PreparedV3Trace {
        thread_meta,
        metadata,
    })
}

#[allow(clippy::too_many_arguments)]
pub(crate) fn save_v3_trace_from_parts<S: FrameSequence>(
    py: Python,
    frames_by_thread: &HashMap<String, S>,
    threads: &HashMap<String, Py<PyAny>>,
    trace_id: &str,
    trace_name: Option<String>,
    source: &str,
    current_thread_id: String,
    timestamp: f64,
    config: &config::Config,
    use_monitoring: bool,
    root_trace_id: Option<&str>,
    value_table: Vec<(u32, Arc<[u8]>)>,
    db_path: &str,
    timeout: usize,
    ignore_errors: bool,
) -> Result<(), PyErr> {
    let mut next_token = 1u32;
    let mut thread_tokens = HashMap::with_capacity(frames_by_thread.len().max(threads.len()));
    for thread_id in frames_by_thread.keys().chain(threads.keys()) {
        if thread_tokens.contains_key(thread_id) {
            continue;
        }
        thread_tokens.insert(thread_id.clone(), next_token);
        next_token = next_token.checked_add(1).ok_or_else(|| {
            pyo3::exceptions::PyRuntimeError::new_err(
                "Kolo exhausted its per-capture thread token space",
            )
        })?;
    }

    // Finish all Python-derived metadata before the first final-artifact I/O.
    let prepared = prepare_v3_trace_from_parts(
        py,
        threads,
        &thread_tokens,
        trace_id,
        trace_name,
        source,
        current_thread_id,
        timestamp,
        config,
        use_monitoring,
        root_trace_id,
    )?;

    #[cfg(target_arch = "wasm32")]
    {
        let data = super::super::trace_container::build_container_bytes(
            trace_id,
            timestamp,
            frames_by_thread,
            &thread_tokens,
            prepared.thread_meta,
            prepared.metadata,
            value_table,
        )
        .map_err(PyOSError::new_err)?;
        return save_v3_container_bytes(py, trace_id, &data, db_path, timeout, ignore_errors);
    }

    #[cfg(not(target_arch = "wasm32"))]
    let result: PyResult<()> = (|| {
        let capture = TraceCapture::for_trace(db_path, trace_id, timestamp);
        // Reconstructed frame ranges may already contain extension-9 value
        // references. Publish their complete table before any copied frame
        // chunk so an interrupted artifact remains independently recoverable.
        capture
            .publish_table(&value_table)
            .map_err(pyo3::exceptions::PyOSError::new_err)?;
        let mut stores = HashMap::with_capacity(frames_by_thread.len());
        for (thread_id, frames) in frames_by_thread {
            let token = *thread_tokens
                .get(thread_id)
                .expect("every frame sequence was assigned a token");
            let mut store = FrameStore::new(capture.clone(), token);
            let mut scratch = Vec::new();
            for index in 0..frames.len() {
                let frame = frames
                    .frame(index, &mut scratch)
                    .map_err(pyo3::exceptions::PyOSError::new_err)?;
                store
                    .append_encoded::<io::Error, _>(|arena, _capture| {
                        arena.extend_from_slice(frame);
                        Ok(())
                    })
                    .map_err(pyo3::exceptions::PyOSError::new_err)?;
            }
            stores.insert(thread_id.clone(), store);
        }
        let layouts = stores
            .values_mut()
            .map(FrameStore::layout)
            .collect::<Result<Vec<_>, _>>()
            .map_err(pyo3::exceptions::PyOSError::new_err)?;
        capture
            .finish(prepared.thread_meta, prepared.metadata, layouts)
            .map_err(pyo3::exceptions::PyOSError::new_err)?;
        save_trace_metadata(py, trace_id, db_path, timeout, ignore_errors)
    })();

    #[cfg(not(target_arch = "wasm32"))]
    match result {
        Err(error) if ignore_errors && error.is_instance_of::<PyOSError>(py) => {
            let message = format!("Failed to save trace {trace_id} to file: {error}");
            PyModule::import(py, "kolo.db")?
                .getattr(intern!(py, "logger"))?
                .call_method1(intern!(py, "warning"), (message,))?;
            Ok(())
        }
        result => result,
    }
}

pub(crate) fn save_trace_metadata(
    py: Python,
    trace_id: &str,
    db_path: &str,
    timeout: usize,
    ignore_errors: bool,
) -> Result<(), PyErr> {
    let db = PyModule::import(py, "kolo.db")?;
    let pathlib = PyModule::import(py, "pathlib")?;
    let db_path_obj = pathlib.getattr(intern!(py, "Path"))?.call1((db_path,))?;
    let kwargs = PyDict::new(py);
    kwargs.set_item("db_path", db_path_obj)?;
    kwargs.set_item("ignore_errors", ignore_errors)?;
    kwargs.set_item("created_at", py.None())?;
    kwargs.set_item("timeout", timeout)?;
    db.getattr(intern!(py, "_save_trace_metadata"))?
        .call((trace_id,), Some(&kwargs))?;
    Ok(())
}

pub(crate) fn save_v3_container_bytes(
    py: Python,
    trace_id: &str,
    data: &[u8],
    db_path: &str,
    timeout: usize,
    ignore_errors: bool,
) -> Result<(), PyErr> {
    let db = PyModule::import(py, "kolo.db")?;
    let pathlib = PyModule::import(py, "pathlib")?;
    let db_path_obj = pathlib.getattr(intern!(py, "Path"))?.call1((db_path,))?;
    let chunks = PyTuple::new(py, [PyBytes::new(py, data)])?;
    let kwargs = PyDict::new(py);
    kwargs.set_item("db_path", db_path_obj)?;
    kwargs.set_item("ignore_errors", ignore_errors)?;
    kwargs.set_item("timeout", timeout)?;
    db.getattr(intern!(py, "save_v3_trace_chunks"))?
        .call((trace_id, chunks), Some(&kwargs))?;
    Ok(())
}
