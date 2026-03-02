use crossbeam_channel::{unbounded, Receiver, Sender};
use parking_lot::Mutex;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::Bound;
use smoldot_light::{
    platform::DefaultPlatform, AddChainConfig, AddChainConfigJsonRpc, Client, ChainId,
};

use std::collections::HashMap;
use std::num::NonZeroU32;
use std::sync::Arc;

struct ChainState {
    chain_id: ChainId,
    // Responses are pushed here by a background drainer thread.
    rx: Receiver<String>,
    // Keep sender so we can clone it into the drainer.
    _tx: Sender<String>,
}

#[pyclass]
pub struct SmoldotClient {
    inner: Arc<Mutex<Client<Arc<DefaultPlatform>, ()>>>,
    chains: Arc<Mutex<HashMap<u64, ChainState>>>, // expose chain ids as u64 in Python
    response_callback: Arc<Mutex<Option<Py<PyAny>>>>,
}

#[pymethods]
impl SmoldotClient {
    #[pyo3(signature = (user_agent_name=None, user_agent_version=None, response_callback=None))]
    #[new]
    pub fn new(
        user_agent_name: Option<String>,
        user_agent_version: Option<String>,
        response_callback: Option<Py<PyAny>>,
    ) -> Self {
        Python::initialize();
        let name = user_agent_name.unwrap_or_else(|| "py-smoldot-light".to_string());
        let ver = user_agent_version.unwrap_or_else(|| "0.1.0".to_string());

        let platform = DefaultPlatform::new(name.into(), ver.into());
        let client: Client<Arc<DefaultPlatform>, ()> = Client::new(platform);

        Self {
            inner: Arc::new(Mutex::new(client)),
            chains: Arc::new(Mutex::new(HashMap::new())),
            response_callback: Arc::new(Mutex::new(response_callback)),
        }
    }

    /// Add a chain.
    ///
    /// `chain_spec_json` is the chain specification JSON string (Polkadot, Kusama, etc).
    /// `relay_chain_ids` optionally links a parachain to its relay chain(s).
    /// Returns a numeric chain id usable from Python.
    #[pyo3(signature = (chain_spec_json, relay_chain_ids=None))]
    pub fn add_chain(
        &self,
        chain_spec_json: String,
        relay_chain_ids: Option<Vec<u64>>,
    ) -> PyResult<u64> {
        let relay_chain_ids: Vec<ChainId> = match relay_chain_ids {
            Some(ids) => {
                let chains = self.chains.lock();
                let mut out = Vec::with_capacity(ids.len());
                for id in ids {
                    let st = chains.get(&id).ok_or_else(|| {
                        PyErr::new::<pyo3::exceptions::PyKeyError, _>("Unknown relay chain_id")
                    })?;
                    out.push(st.chain_id);
                }
                out
            }
            None => Vec::new(),
        };

        let mut guard = self.inner.lock();

        // Minimal config: you will likely want to expose more knobs later.
        let cfg = AddChainConfig {
            user_data: (),
            specification: &chain_spec_json,
            database_content: "",
            potential_relay_chains: relay_chain_ids.into_iter(),
            json_rpc: AddChainConfigJsonRpc::Enabled {
                max_pending_requests: NonZeroU32::new(128).unwrap(),
                max_subscriptions: 1024,
            },
        };

        let success = guard
            .add_chain(cfg)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{e:?}")))?;

        let chain_id = success.chain_id;
        let chain_id_u64 = usize::from(chain_id) as u64;

        // Drain responses in a background thread into a channel.
        let responses = success.json_rpc_responses;
        let (tx, rx) = unbounded::<String>();
        let tx_for_thread = tx.clone();

        let response_callback = self.response_callback.clone();
        if let Some(mut responses) = responses {
            std::thread::spawn(move || {
                while let Some(msg) = futures_lite::future::block_on(responses.next()) {
                    Python::attach(|py| {
                        let guard = response_callback.lock();
                        if let Some(callback) = guard.as_ref() {
                            if let Err(err) = callback.call1(py, (msg.clone(),)) {
                                err.print(py);
                            }
                        }
                    });
                    if tx_for_thread.send(msg).is_err() {
                        break;
                    }
                }
            });
        }

        self.chains.lock().insert(
            chain_id_u64,
            ChainState {
                chain_id,
                rx,
                _tx: tx,
            },
        );

        Ok(chain_id_u64)
    }

    /// Queue a JSON-RPC request (string).
    pub fn json_rpc_request(&self, chain_id: u64, request: String) -> PyResult<()> {
        let chain_id = {
            let chains = self.chains.lock();
            let st = chains.get(&chain_id).ok_or_else(|| {
                PyErr::new::<pyo3::exceptions::PyKeyError, _>("Unknown chain_id")
            })?;
            st.chain_id
        };

        let mut guard = self.inner.lock();
        guard
            .json_rpc_request(request, chain_id)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{e:?}")))?;

        Ok(())
    }

    /// Queue a JSON-RPC request and block until the next response arrives.
    ///
    /// Note: this assumes only one outstanding request per chain. If multiple
    /// requests are in-flight, responses may not match the request you sent.
    // pub fn json_rpc_request_blocking(
    //     &self,
    //     chain_id: u64,
    //     request: String,
    //     timeout_ms: Option<u64>,
    // ) -> PyResult<String> {
    //     let (chain_id, rx) = {
    //         let chains = self.chains.lock();
    //         let st = chains.get(&chain_id).ok_or_else(|| {
    //             PyErr::new::<pyo3::exceptions::PyKeyError, _>("Unknown chain_id")
    //         })?;
    //         (st.chain_id, st.rx.clone())
    //     };
    //
    //     let mut guard = self.inner.lock();
    //     guard
    //         .json_rpc_request(request, chain_id)
    //         .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("{e:?}")))?;
    //
    //     let response = if let Some(timeout_ms) = timeout_ms {
    //         rx.recv_timeout(Duration::from_millis(timeout_ms))
    //             .map_err(|err| match err {
    //                 crossbeam_channel::RecvTimeoutError::Timeout => {
    //                     PyErr::new::<pyo3::exceptions::PyTimeoutError, _>(
    //                         "Timed out waiting for JSON-RPC response",
    //                     )
    //                 }
    //                 crossbeam_channel::RecvTimeoutError::Disconnected => {
    //                     PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
    //                         "Response channel closed",
    //                     )
    //                 }
    //             })?
    //     } else {
    //         rx.recv().map_err(|_| {
    //             PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Response channel closed")
    //         })?
    //     };
    //
    //     Ok(response)
    // }

    /// Drain any already-collected responses (non-blocking).
    pub fn drain_responses(&self, chain_id: u64, max: usize) -> PyResult<Vec<String>> {
        let chains = self.chains.lock();
        let st = chains.get(&chain_id).ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyKeyError, _>("Unknown chain_id")
        })?;

        let mut out = Vec::new();
        for _ in 0..max {
            match st.rx.try_recv() {
                Ok(v) => out.push(v),
                Err(_) => break,
            }
        }
        Ok(out)
    }
}

#[pymodule (name="smoldot_light")]
fn py_smoldot_light(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SmoldotClient>()?;
    Ok(())
}
