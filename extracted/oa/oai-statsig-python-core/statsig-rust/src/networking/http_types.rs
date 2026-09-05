use crate::StatsigErr;
use crate::networking::proxy_config::ProxyConfig;
use crate::sdk_diagnostics::marker::KeyType;
use async_trait::async_trait;
use chrono::Utc;
use serde::de::DeserializeOwned;
use std::io::Cursor;
use std::{
    collections::HashMap,
    sync::{Arc, atomic::AtomicBool},
};

#[derive(Clone)]
pub struct RequestArgs {
    pub url: String,
    pub body: Option<Vec<u8>>,
    pub retries: u32, // 1 initial + N 'retries'
    pub headers: Option<HashMap<String, String>>,
    pub query_params: Option<HashMap<String, String>>,
    pub id_list_file_id: Option<String>, // for logging
    pub deltas_enabled: bool,
    pub accept_gzip_response: bool,
    pub timeout_ms: u64,
    pub is_shutdown: Option<Arc<AtomicBool>>,
    pub diagnostics_key: Option<KeyType>,
    pub proxy_config: Option<ProxyConfig>,
    pub ca_cert_pem: Option<Vec<u8>>,
    pub disable_file_streaming: Option<bool>,
    /// Opt-in flag for reusing the default reqwest client on Statsig-owned endpoints.
    pub log_event_connection_reuse: bool,
}

impl Default for RequestArgs {
    fn default() -> Self {
        Self::new()
    }
}

impl RequestArgs {
    #[must_use]
    pub fn new() -> Self {
        RequestArgs {
            url: String::new(),
            body: None,
            retries: 0,
            headers: None,
            query_params: None,
            id_list_file_id: None,
            deltas_enabled: false,
            accept_gzip_response: false,
            timeout_ms: 0,
            is_shutdown: None,
            diagnostics_key: None,
            proxy_config: None,
            ca_cert_pem: None,
            disable_file_streaming: None,
            log_event_connection_reuse: false,
        }
    }

    pub fn get_fully_qualified_url(&self) -> String {
        let mut url = self.url.clone();
        let query_params = match &self.query_params {
            Some(params) => params,
            None => return url,
        };

        let query_params_str = query_params
            .iter()
            .map(|(k, v)| format!("{k}={v}"))
            .collect::<Vec<_>>()
            .join("&");

        if !query_params_str.is_empty() {
            url.push_str(&format!("?{query_params_str}"));
        }

        url
    }

    pub fn populate_headers(&mut self, extra_headers: HashMap<String, String>) {
        let mut headers = HashMap::new();
        headers.extend(extra_headers);

        headers.insert(
            "STATSIG-CLIENT-TIME".into(),
            Utc::now().timestamp_millis().to_string(),
        );

        if let Some(my_headers) = &mut self.headers {
            my_headers.extend(headers);
        } else {
            self.headers = Some(headers);
        }
    }
}

pub struct Response {
    pub status_code: Option<u16>,
    pub data: Option<ResponseData>,
    pub error: Option<String>,
}

pub enum ResponseLimitOutcome {
    Response(Response),
    SizeLimitExceeded(Response),
    Unsupported(Response),
}

impl ResponseLimitOutcome {
    pub(crate) fn into_parts(self) -> (Response, bool, bool) {
        match self {
            Self::Response(response) => (response, false, false),
            Self::SizeLimitExceeded(response) => (response, true, false),
            Self::Unsupported(response) => (response, false, true),
        }
    }
}

#[derive(PartialEq, Clone)]
pub enum HttpMethod {
    GET,
    POST,
}

#[async_trait]
pub trait NetworkProvider: Sync + Send {
    async fn send(&self, method: &HttpMethod, args: &RequestArgs) -> Response;

    async fn send_with_response_limit(
        &self,
        _method: &HttpMethod,
        _args: &RequestArgs,
        _max_response_bytes: u64,
    ) -> ResponseLimitOutcome {
        // Blob downloads require provider-level size and redirect enforcement.
        // Falling back to send() would silently bypass both protections.
        ResponseLimitOutcome::Unsupported(Response {
            status_code: None,
            data: None,
            error: Some("NetworkProvider does not support response-limited requests".to_string()),
        })
    }
}

pub trait ResponseDataStream:
    std::io::Read + std::io::Seek + std::fmt::Debug + Send + Sync
{
}

impl<T: std::io::Read + std::io::Seek + std::fmt::Debug + Send + Sync> ResponseDataStream for T {}

pub struct ResponseData {
    stream: Box<dyn ResponseDataStream>,
    headers: Option<HashMap<String, String>>,
    shared_bytes: Option<Arc<[u8]>>,
    prepared_protobuf_stream: Option<Arc<Vec<u8>>>,
    // The parser keeps the original stream for normal response semantics but
    // may attach a hydrated same-codec copy for durable datastore writes.
    data_store_protobuf_bytes: Option<Vec<u8>>,
}

const TAG: &str = "ResponseData";

impl ResponseData {
    pub fn from_bytes(bytes: Vec<u8>) -> Self {
        Self::from_bytes_with_headers(bytes, None)
    }

    pub fn from_bytes_with_headers(
        bytes: Vec<u8>,
        headers: Option<HashMap<String, String>>,
    ) -> Self {
        Self {
            stream: Box::new(Cursor::new(bytes)),
            headers,
            shared_bytes: None,
            prepared_protobuf_stream: None,
            data_store_protobuf_bytes: None,
        }
    }

    pub fn from_shared_bytes_with_headers(
        bytes: Arc<[u8]>,
        headers: Option<HashMap<String, String>>,
    ) -> Self {
        Self {
            stream: Box::new(Cursor::new(Arc::clone(&bytes))),
            headers,
            shared_bytes: Some(bytes),
            prepared_protobuf_stream: None,
            data_store_protobuf_bytes: None,
        }
    }

    pub fn from_stream(stream: Box<dyn ResponseDataStream>) -> Self {
        Self::from_stream_with_headers(stream, None)
    }

    pub fn from_stream_with_headers(
        stream: Box<dyn ResponseDataStream>,
        headers: Option<HashMap<String, String>>,
    ) -> Self {
        Self {
            stream,
            headers,
            shared_bytes: None,
            prepared_protobuf_stream: None,
            data_store_protobuf_bytes: None,
        }
    }

    pub fn get_stream_ref(&self) -> &dyn ResponseDataStream {
        &self.stream
    }

    pub fn get_stream_mut(&mut self) -> &mut dyn ResponseDataStream {
        &mut self.stream
    }

    pub fn get_header_ref(&self, key: &str) -> Option<&String> {
        self.headers.as_ref().and_then(|h| h.get(key))
    }

    pub(crate) fn set_scoped_expected_checksum(&mut self, checksum: &str) {
        self.headers.get_or_insert_with(HashMap::new).insert(
            "x-statsig-scoped-expected-checksum".to_string(),
            checksum.to_string(),
        );
    }

    pub(crate) fn scoped_expected_checksum(&self) -> Option<&str> {
        self.get_header_ref("x-statsig-scoped-expected-checksum")
            .map(String::as_str)
    }

    pub(crate) fn set_scoped_expected_lcut(&mut self, lcut: u64) {
        self.headers.get_or_insert_with(HashMap::new).insert(
            "x-statsig-scoped-expected-lcut".to_string(),
            lcut.to_string(),
        );
    }

    pub(crate) fn scoped_expected_lcut(&self) -> Option<u64> {
        self.get_header_ref("x-statsig-scoped-expected-lcut")
            .and_then(|lcut| lcut.parse().ok())
    }

    pub(crate) fn replace_bytes(&mut self, bytes: Vec<u8>) {
        self.stream = Box::new(Cursor::new(bytes));
        self.shared_bytes = None;
        self.prepared_protobuf_stream = None;
        self.data_store_protobuf_bytes = None;
    }

    pub(crate) fn set_prepared_protobuf_stream(&mut self, bytes: Vec<u8>) {
        self.prepared_protobuf_stream = Some(Arc::new(bytes));
    }

    pub(crate) fn get_prepared_protobuf_stream(&self) -> Option<Arc<Vec<u8>>> {
        self.prepared_protobuf_stream.clone()
    }

    pub(crate) fn set_data_store_protobuf_bytes(&mut self, bytes: Vec<u8>) {
        self.data_store_protobuf_bytes = Some(bytes);
    }

    pub(crate) fn take_data_store_protobuf_bytes(&mut self) -> Option<Vec<u8>> {
        self.data_store_protobuf_bytes.take()
    }

    pub fn deserialize_into<T: DeserializeOwned>(&mut self) -> Result<T, StatsigErr> {
        self.rewind()?;

        let result = match &self.shared_bytes {
            Some(bytes) => serde_json::from_slice(bytes.as_ref()),
            None => serde_json::from_reader(self.stream.as_mut()),
        }
        .map_err(|e| StatsigErr::JsonParseError(TAG.to_string(), e.to_string()))?;

        Ok(result)
    }

    pub fn deserialize_in_place<T: DeserializeOwned>(
        &mut self,
        place: &mut T,
    ) -> Result<(), StatsigErr> {
        self.rewind()?;

        let result = match &self.shared_bytes {
            Some(bytes) => {
                let mut deserializer = serde_json::Deserializer::from_slice(bytes.as_ref());
                T::deserialize_in_place(&mut deserializer, place)
            }
            None => {
                let mut deserializer = serde_json::Deserializer::from_reader(self.stream.as_mut());
                T::deserialize_in_place(&mut deserializer, place)
            }
        };

        result.map_err(|e| StatsigErr::JsonParseError(TAG.to_string(), e.to_string()))
    }

    pub fn read_to_string(&mut self) -> Result<String, StatsigErr> {
        let buf = self.read_to_bytes()?;

        String::from_utf8(buf)
            .map_err(|e| StatsigErr::JsonParseError(TAG.to_string(), e.to_string()))
    }

    pub fn read_to_bytes(&mut self) -> Result<Vec<u8>, StatsigErr> {
        self.rewind()?;

        let mut buf = Vec::new();

        self.stream
            .read_to_end(&mut buf)
            .map_err(|e| StatsigErr::SerializationError(e.to_string()))?;

        Ok(buf)
    }

    pub(crate) fn rewind(&mut self) -> Result<(), StatsigErr> {
        self.stream
            .rewind()
            .map_err(|e| StatsigErr::SerializationError(e.to_string()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};

    struct SendOnlyProvider {
        send_calls: AtomicUsize,
    }

    #[test]
    fn shared_bytes_support_repeated_slice_deserialization_and_stream_reads() {
        let bytes: Arc<[u8]> = Arc::from(br#"{"value":"shared"}"#.as_slice());
        let mut response = ResponseData::from_shared_bytes_with_headers(
            Arc::clone(&bytes),
            Some(HashMap::from([("format".to_string(), "json".to_string())])),
        );

        assert!(Arc::ptr_eq(
            response.shared_bytes.as_ref().expect("shared bytes"),
            &bytes
        ));
        assert_eq!(response.get_header_ref("format"), Some(&"json".to_string()));
        assert_eq!(
            response
                .deserialize_into::<serde_json::Value>()
                .expect("shared JSON should deserialize"),
            serde_json::json!({ "value": "shared" })
        );

        let mut value = serde_json::Value::Null;
        response
            .deserialize_in_place(&mut value)
            .expect("shared JSON should deserialize in place");
        assert_eq!(value, serde_json::json!({ "value": "shared" }));
        assert_eq!(
            response.read_to_bytes().expect("stream should rewind"),
            &*bytes
        );
    }

    #[test]
    fn shared_bytes_can_retry_after_failed_deserialization() {
        let mut response =
            ResponseData::from_shared_bytes_with_headers(Arc::from(b"false".as_slice()), None);

        assert!(response.deserialize_into::<String>().is_err());
        assert!(!response.deserialize_into::<bool>().expect("boolean JSON"));
    }

    #[test]
    fn replacing_shared_bytes_deserializes_the_replacement() {
        let mut response = ResponseData::from_shared_bytes_with_headers(
            Arc::from(br#"{"value":"original"}"#.as_slice()),
            None,
        );
        response.set_scoped_expected_checksum("expected");
        response.set_scoped_expected_lcut(123);
        response.replace_bytes(br#"{"value":"hydrated"}"#.to_vec());

        assert_eq!(
            response
                .deserialize_into::<serde_json::Value>()
                .expect("replacement JSON should deserialize"),
            serde_json::json!({ "value": "hydrated" })
        );
        let mut value = serde_json::Value::Null;
        response
            .deserialize_in_place(&mut value)
            .expect("replacement JSON should deserialize in place");
        assert_eq!(value, serde_json::json!({ "value": "hydrated" }));
        assert_eq!(response.scoped_expected_checksum(), Some("expected"));
        assert_eq!(response.scoped_expected_lcut(), Some(123));
    }

    #[async_trait]
    impl NetworkProvider for SendOnlyProvider {
        async fn send(&self, _method: &HttpMethod, _args: &RequestArgs) -> Response {
            self.send_calls.fetch_add(1, Ordering::SeqCst);
            Response {
                status_code: Some(200),
                data: Some(ResponseData::from_bytes(b"unbounded".to_vec())),
                error: None,
            }
        }
    }

    #[tokio::test]
    async fn default_response_limited_requests_fail_closed_without_sending() {
        let provider = SendOnlyProvider {
            send_calls: AtomicUsize::new(0),
        };

        let response = match provider
            .send_with_response_limit(&HttpMethod::GET, &RequestArgs::new(), 1)
            .await
        {
            ResponseLimitOutcome::Unsupported(response) => response,
            ResponseLimitOutcome::Response(_) | ResponseLimitOutcome::SizeLimitExceeded(_) => {
                panic!("send-only providers must not fall back to unbounded requests")
            }
        };

        assert_eq!(provider.send_calls.load(Ordering::SeqCst), 0);
        assert!(response.data.is_none());
        assert_eq!(
            response.error.as_deref(),
            Some("NetworkProvider does not support response-limited requests")
        );
    }
}
