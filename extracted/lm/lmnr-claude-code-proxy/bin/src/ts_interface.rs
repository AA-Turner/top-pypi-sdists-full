use crate::interface::{DEFAULT_PORT, DEFAULT_TIMEOUT};

/// Run the proxy server in a background thread
#[napi_derive::napi]
pub fn run(target_url: String, port: Option<u16>) -> napi::Result<()> {
    let port = port.unwrap_or(DEFAULT_PORT);

    crate::interface::run(target_url, port)
        .map_err(|e| napi::Error::new(napi::Status::Cancelled, e))
}

/// Stop the proxy server on a specific port
/// Uses a default timeout of 4 seconds for graceful shutdown
#[napi_derive::napi]
#[deprecated(since = "0.1.12", note = "Use stop_with_timeout instead")]
pub fn stop(port: Option<u16>) -> napi::Result<()> {
    let port = port.unwrap_or(DEFAULT_PORT);

    crate::interface::stop(port).map_err(|e| napi::Error::new(napi::Status::Cancelled, e))
}

/// Stop the proxy server on a specific port with a timeout
/// If the server doesn't stop within the timeout, it will be forcefully terminated
#[napi_derive::napi]
pub fn stop_with_timeout(port: Option<u16>, timeout_secs: Option<u32>) -> napi::Result<()> {
    let port = port.unwrap_or(DEFAULT_PORT);
    let timeout_secs = timeout_secs.unwrap_or(DEFAULT_TIMEOUT as u32) as u64;

    crate::interface::stop_with_timeout(port, timeout_secs)
        .map_err(|e| napi::Error::new(napi::Status::Cancelled, e))
}
