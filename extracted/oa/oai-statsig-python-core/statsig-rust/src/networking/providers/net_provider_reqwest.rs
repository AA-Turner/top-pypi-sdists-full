use std::collections::{HashMap, VecDeque};
use std::io::{BufReader, Seek, SeekFrom, Write};
use std::sync::Arc;
use std::time::{Duration, Instant};

use async_trait::async_trait;
use parking_lot::Mutex;

use crate::log_d;
use crate::{
    StatsigErr, log_e, log_w,
    networking::{
        NetworkProvider, get_source_service_and_request_path,
        http_types::{HttpMethod, RequestArgs, Response, ResponseData, ResponseLimitOutcome},
        url_path_has_suffix,
    },
};

use crate::networking::proxy_config::ProxyConfig;
use reqwest::{Method, redirect::Policy};

const TAG: &str = "NetworkProviderReqwest";
const LOG_EVENT_REUSE_PATH: &[&str] = &["v1", "log_event"];
const SDK_EXCEPTION_REUSE_PATH: &[&str] = &["v1", "sdk_exception"];
const MAX_RESPONSE_LIMIT_CLIENTS: usize = 16;
const MAX_HTTP2_ORIGINS: usize = 64;
const HTTP2_CAPABILITY_TTL: Duration = Duration::from_secs(300);
const HTTP2_PROBE_BUDGET: Duration = Duration::from_millis(250);

fn direct_probe_allowed() -> bool {
    // Windows may discover a system proxy outside the process environment.
    // Conservatively keep the existing transport when direct routing is uncertain.
    !cfg!(windows)
        && !["HTTP_PROXY", "http_proxy", "ALL_PROXY", "all_proxy"]
            .iter()
            .any(|name| std::env::var_os(name).is_some_and(|value| !value.is_empty()))
}

async fn probe_plaintext_http2(host: &str, port: u16) -> bool {
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    let Ok(mut socket) = tokio::net::TcpStream::connect((host, port)).await else {
        return false;
    };
    // Connection-level discovery only: no URL, headers, SDK key or body is sent.
    if socket
        .write_all(b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n\0\0\0\x04\0\0\0\0\0")
        .await
        .is_err()
    {
        return false;
    }
    let mut header = [0; 9];
    if socket.read_exact(&mut header).await.is_err() {
        return false;
    }
    let length = ((header[0] as usize) << 16) | ((header[1] as usize) << 8) | header[2] as usize;
    if header[3] != 4
        || header[4] & 1 != 0
        || header[5..9] != [0; 4]
        || length > 16_384
        || length % 6 != 0
    {
        return false;
    }
    let mut payload = vec![0; length];
    socket.read_exact(&mut payload).await.is_ok()
}

fn plaintext_probe_host(url: &url::Url) -> Option<&str> {
    // URL authorities bracket IPv6 literals; socket address resolution must not.
    url.host_str()
        .map(|host| host.trim_start_matches('[').trim_end_matches(']'))
}

#[derive(Debug)]
enum ResponseDataReadError {
    Statsig(StatsigErr),
    SizeLimitExceeded { max_response_bytes: u64 },
}

impl ResponseDataReadError {
    const fn is_size_limit_exceeded(&self) -> bool {
        matches!(self, Self::SizeLimitExceeded { .. })
    }
}

impl From<StatsigErr> for ResponseDataReadError {
    fn from(error: StatsigErr) -> Self {
        Self::Statsig(error)
    }
}

impl std::fmt::Display for ResponseDataReadError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Statsig(error) => write!(formatter, "{error}"),
            Self::SizeLimitExceeded { max_response_bytes } => write!(
                formatter,
                "{}",
                StatsigErr::SerializationError(format!(
                    "Response exceeded maximum allowed bytes ({max_response_bytes})"
                ))
            ),
        }
    }
}

#[derive(Clone, Eq, Hash, PartialEq)]
struct ResponseLimitClientKey {
    proxy_host: Option<String>,
    proxy_port: Option<u16>,
    proxy_auth: Option<String>,
    proxy_protocol: Option<String>,
    ca_cert_pem: Option<Vec<u8>>,
    disable_redirects: bool,
}

impl ResponseLimitClientKey {
    fn from_request_args(request_args: &RequestArgs) -> Self {
        let (proxy_host, proxy_port, proxy_auth, proxy_protocol) =
            match request_args.proxy_config.as_ref() {
                Some(proxy_config)
                    if proxy_config.proxy_host.is_some() && proxy_config.proxy_port.is_some() =>
                {
                    (
                        proxy_config.proxy_host.clone(),
                        proxy_config.proxy_port,
                        proxy_config.proxy_auth.clone(),
                        proxy_config.proxy_protocol.clone(),
                    )
                }
                _ => (None, None, None, None),
            };

        Self {
            proxy_host,
            proxy_port,
            proxy_auth,
            proxy_protocol,
            ca_cert_pem: request_args.ca_cert_pem.clone(),
            disable_redirects: true,
        }
    }
}

#[derive(Default)]
struct ResponseLimitClientCache {
    entries: HashMap<ResponseLimitClientKey, reqwest::Client>,
    lru: VecDeque<ResponseLimitClientKey>,
}

impl ResponseLimitClientCache {
    fn get(&mut self, key: &ResponseLimitClientKey) -> Option<reqwest::Client> {
        let client = self.entries.get(key)?.clone();
        self.touch(key);
        Some(client)
    }

    fn insert(&mut self, key: ResponseLimitClientKey, client: reqwest::Client) {
        if self.entries.remove(&key).is_some() {
            self.lru.retain(|entry| entry != &key);
        }

        while self.entries.len() >= MAX_RESPONSE_LIMIT_CLIENTS {
            let Some(oldest) = self.lru.pop_front() else {
                break;
            };
            self.entries.remove(&oldest);
        }

        self.lru.push_back(key.clone());
        self.entries.insert(key, client);
    }

    fn touch(&mut self, key: &ResponseLimitClientKey) {
        self.lru.retain(|entry| entry != key);
        self.lru.push_back(key.clone());
    }
}

pub struct NetworkProviderReqwest {
    has_file_write_access: bool,
    shared_client: reqwest::Client,
    http2_clients: Mutex<ResponseLimitClientCache>,
    http2_origins: Mutex<HashMap<String, (Instant, Arc<tokio::sync::OnceCell<bool>>)>>,
    response_limit_clients: Mutex<ResponseLimitClientCache>,
}

impl NetworkProviderReqwest {
    pub fn new() -> Self {
        Self {
            has_file_write_access: tempfile::tempfile().is_ok(),
            shared_client: reqwest::Client::new(),
            http2_clients: Mutex::new(ResponseLimitClientCache::default()),
            http2_origins: Mutex::new(HashMap::new()),
            response_limit_clients: Mutex::new(ResponseLimitClientCache::default()),
        }
    }
}

impl Default for NetworkProviderReqwest {
    fn default() -> Self {
        Self::new()
    }
}

#[async_trait]
impl NetworkProvider for NetworkProviderReqwest {
    async fn send(&self, method: &HttpMethod, args: &RequestArgs) -> Response {
        self.send_impl(method, args, false).await
    }

    async fn send_without_redirects(&self, method: &HttpMethod, args: &RequestArgs) -> Response {
        self.send_impl(method, args, true).await
    }

    async fn send_http2_preferred(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        max_response_bytes: Option<u64>,
        disable_redirects: bool,
    ) -> ResponseLimitOutcome {
        if args
            .is_shutdown
            .as_ref()
            .is_some_and(|shutdown| shutdown.load(std::sync::atomic::Ordering::SeqCst))
        {
            return ResponseLimitOutcome::Response(request_configuration_error(
                "Request was shutdown",
            ));
        }
        let budget = Duration::from_millis(if args.timeout_ms == 0 {
            10_000
        } else {
            args.timeout_ms
        });
        let mut received_status = None;
        tokio::time::timeout(budget, async {
            let use_http2 = self.plaintext_http2_available(args, budget).await;
            if args
                .is_shutdown
                .as_ref()
                .is_some_and(|flag| flag.load(std::sync::atomic::Ordering::SeqCst))
            {
                return ResponseLimitOutcome::Response(request_configuration_error(
                    "Request was shutdown",
                ));
            }
            let client = if use_http2 {
                match self.get_http2_client(args, true) {
                    Ok(client) => client,
                    Err(error) => {
                        return ResponseLimitOutcome::Unsupported(request_configuration_error(
                            error,
                        ));
                    }
                }
            } else {
                // HTTPS already negotiates h2/http1.1 with ALPN. Unknown or proxied
                // cleartext receivers use the existing transport before any payload is sent.
                self.get_client(args, max_response_bytes.is_some() || disable_redirects)
            };
            let request = Self::build_request_with_client(&client, method, args);
            let response = if use_http2 && max_response_bytes.is_none() {
                self.send_http2_with_redirects(args, request, disable_redirects)
                    .await
            } else {
                request.send().await
            };
            // Keep the final status if the total attempt budget expires while reading
            // the body, so a terminal response cannot become a retryable timeout.
            received_status = response.as_ref().ok().map(|value| value.status().as_u16());
            match max_response_bytes {
                Some(limit) => self.read_limited_response(args, response, limit).await,
                None => ResponseLimitOutcome::Response(
                    self.read_unlimited_response(args, response).await,
                ),
            }
        })
        .await
        .unwrap_or_else(|_| {
            ResponseLimitOutcome::Response(Response {
                status_code: received_status,
                data: None,
                error: Some("HTTP request timed out".to_string()),
            })
        })
    }

    async fn send_with_response_limit(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        max_response_bytes: u64,
    ) -> ResponseLimitOutcome {
        self.send_with_response_limit_impl(method, args, max_response_bytes)
            .await
    }
}

impl NetworkProviderReqwest {
    async fn plaintext_http2_available(
        &self,
        args: &RequestArgs,
        request_budget: Duration,
    ) -> bool {
        let Ok(url) = url::Url::parse(&args.url) else {
            return false;
        };
        if url.scheme() != "http" || args.proxy_config.is_some() || !direct_probe_allowed() {
            return false;
        }
        let Some(host) = plaintext_probe_host(&url) else {
            return false;
        };
        let Some(port) = url.port_or_known_default() else {
            return false;
        };
        let origin = url.origin().ascii_serialization();
        // Coalesce discovery per origin without holding a cache lock during I/O.
        let capability = {
            let mut origins = self.http2_origins.lock();
            origins.retain(|_, (checked, _)| checked.elapsed() < HTTP2_CAPABILITY_TTL);
            if let Some((_, capability)) = origins.get(&origin) {
                capability.clone()
            } else {
                if origins.len() >= MAX_HTTP2_ORIGINS {
                    if let Some(oldest) = origins
                        .iter()
                        .min_by_key(|(_, (at, _))| *at)
                        .map(|(origin, _)| origin.clone())
                    {
                        origins.remove(&oldest);
                    }
                }
                let capability = Arc::new(tokio::sync::OnceCell::new());
                origins.insert(origin, (Instant::now(), capability.clone()));
                capability
            }
        };
        let budget = HTTP2_PROBE_BUDGET.min(request_budget / 4);
        tokio::time::timeout(
            budget,
            capability.get_or_init(|| async {
                tokio::time::timeout(
                    budget.saturating_sub(Duration::from_millis(1)),
                    probe_plaintext_http2(host, port),
                )
                .await
                .unwrap_or(false)
            }),
        )
        .await
        .copied()
        .unwrap_or(false)
    }

    async fn send_http2_with_redirects(
        &self,
        args: &RequestArgs,
        builder: reqwest::RequestBuilder,
        disable_redirects: bool,
    ) -> Result<reqwest::Response, reqwest::Error> {
        let (client, request) = builder.build_split();
        let request = request?;
        let Some(mut redirected) = request.try_clone() else {
            return client.execute(request).await;
        };
        let response = client.execute(request).await?;
        if disable_redirects || !matches!(response.status().as_u16(), 301 | 302 | 303 | 307 | 308) {
            return Ok(response);
        }
        let next = response
            .headers()
            .get(reqwest::header::LOCATION)
            .and_then(|value| value.to_str().ok())
            .and_then(|value| response.url().join(value).ok());
        let Some(next) = next else {
            return Ok(response);
        };
        // A real redirect response authorizes following Location; transport failures
        // never reach this branch. Leave later redirects to reqwest's normal policy.
        if response.status().as_u16() == 303
            || (matches!(response.status().as_u16(), 301 | 302)
                && redirected.method() == Method::POST)
        {
            *redirected.method_mut() = Method::GET;
            *redirected.body_mut() = None;
            for header in [
                "content-type",
                "content-length",
                "content-encoding",
                "transfer-encoding",
            ] {
                redirected.headers_mut().remove(header);
            }
        }
        if next.host_str() != response.url().host_str()
            || next.port_or_known_default() != response.url().port_or_known_default()
        {
            for header in [
                "authorization",
                "cookie",
                "cookie2",
                "proxy-authorization",
                "www-authenticate",
            ] {
                redirected.headers_mut().remove(header);
            }
        }
        let mut referer = response.url().clone();
        let _ = referer.set_username("");
        let _ = referer.set_password(None);
        referer.set_fragment(None);
        if let Ok(value) = reqwest::header::HeaderValue::from_str(referer.as_str()) {
            redirected
                .headers_mut()
                .insert(reqwest::header::REFERER, value);
        }
        *redirected.url_mut() = next;
        drop(response);
        // One redirect has already been followed. Plaintext targets may use H1;
        // HTTPS targets negotiate normally. No application request is replayed.
        let mut builder = reqwest::Client::builder().redirect(Policy::limited(9));
        if let Some(pem) = &args.ca_cert_pem {
            for cert in reqwest::Certificate::from_pem_bundle(pem)? {
                builder = builder.add_root_certificate(cert);
            }
        }
        let client = builder.build()?;
        client.execute(redirected).await
    }

    async fn send_impl(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        disable_redirects: bool,
    ) -> Response {
        if let Some(is_shutdown) = &args.is_shutdown {
            if is_shutdown.load(std::sync::atomic::Ordering::SeqCst) {
                return Response {
                    status_code: None,
                    data: None,
                    error: Some("Request was shutdown".to_string()),
                };
            }
        }

        let request = self.build_request(method, args, disable_redirects);
        self.send_request(args, request).await
    }

    async fn send_request(&self, args: &RequestArgs, request: reqwest::RequestBuilder) -> Response {
        self.read_unlimited_response(args, request.send().await)
            .await
    }

    async fn read_unlimited_response(
        &self,
        args: &RequestArgs,
        result: Result<reqwest::Response, reqwest::Error>,
    ) -> Response {
        let mut error = None;
        let mut status_code = None;
        let mut data = None;

        match result {
            Ok(response) => {
                status_code = Some(response.status().as_u16());

                let data_result =
                    if !self.has_file_write_access || args.disable_file_streaming == Some(true) {
                        Self::write_unlimited_response_to_in_memory_buffer(response).await
                    } else {
                        Self::write_unlimited_response_to_temp_file(response).await
                    };

                match data_result {
                    Ok(response_data) => data = Some(response_data),
                    Err(e) => {
                        error = Some(e.to_string());
                    }
                }
            }
            Err(e) => {
                let error_message = get_error_message(e);
                error = Some(error_message);
            }
        }

        Response {
            status_code,
            data,
            error,
        }
    }
    async fn send_with_response_limit_impl(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        max_response_bytes: u64,
    ) -> ResponseLimitOutcome {
        if let Some(is_shutdown) = &args.is_shutdown {
            if is_shutdown.load(std::sync::atomic::Ordering::SeqCst) {
                return ResponseLimitOutcome::Response(Response {
                    status_code: None,
                    data: None,
                    error: Some("Request was shutdown".to_string()),
                });
            }
        }

        let request = self.build_request(method, args, true);
        self.send_limited_request(args, request, max_response_bytes)
            .await
    }

    async fn send_limited_request(
        &self,
        args: &RequestArgs,
        request: reqwest::RequestBuilder,
        max_response_bytes: u64,
    ) -> ResponseLimitOutcome {
        self.read_limited_response(args, request.send().await, max_response_bytes)
            .await
    }

    async fn read_limited_response(
        &self,
        args: &RequestArgs,
        result: Result<reqwest::Response, reqwest::Error>,
        max_response_bytes: u64,
    ) -> ResponseLimitOutcome {
        let mut error = None;
        let mut status_code = None;
        let mut data = None;
        let mut response_size_limit_exceeded = false;

        match result {
            Ok(response) => {
                status_code = Some(response.status().as_u16());

                let data_result =
                    if !self.has_file_write_access || args.disable_file_streaming == Some(true) {
                        Self::write_response_to_in_memory_buffer(response, Some(max_response_bytes))
                            .await
                    } else {
                        Self::write_response_to_temp_file(response, Some(max_response_bytes)).await
                    };

                match data_result {
                    Ok(response_data) => data = Some(response_data),
                    Err(e) => {
                        response_size_limit_exceeded = e.is_size_limit_exceeded();
                        error = Some(e.to_string());
                    }
                }
            }
            Err(e) => {
                let error_message = get_error_message(e);
                error = Some(error_message);
            }
        }

        let response = Response {
            status_code,
            data,
            error,
        };
        if response_size_limit_exceeded {
            ResponseLimitOutcome::SizeLimitExceeded(response)
        } else {
            ResponseLimitOutcome::Response(response)
        }
    }

    fn build_request(
        &self,
        method: &HttpMethod,
        request_args: &RequestArgs,
        disable_redirects: bool,
    ) -> reqwest::RequestBuilder {
        let client = self.get_client(request_args, disable_redirects);
        Self::build_request_with_client(&client, method, request_args)
    }

    fn build_request_with_client(
        client: &reqwest::Client,
        method: &HttpMethod,
        request_args: &RequestArgs,
    ) -> reqwest::RequestBuilder {
        let method_actual = match method {
            HttpMethod::GET => Method::GET,
            HttpMethod::POST => Method::POST,
        };
        let is_post = method_actual == Method::POST;

        let mut request = client.request(method_actual, &request_args.url);

        let timeout_duration = match request_args.timeout_ms > 0 {
            true => Duration::from_millis(request_args.timeout_ms),
            false => Duration::from_secs(10),
        };
        request = request.timeout(timeout_duration);

        if let Some(headers) = &request_args.headers {
            for (key, value) in headers {
                request = request.header(key, value);
            }
        }

        if let Some(params) = &request_args.query_params {
            request = request.query(params);
        }

        if is_post {
            let bytes = match &request_args.body {
                Some(b) => b.clone(),
                None => vec![],
            };
            let byte_len = bytes.len();

            request = request.body(bytes);
            request = request.header("Content-Length", byte_len.to_string());
        }

        request
    }

    fn get_client(&self, request_args: &RequestArgs, disable_redirects: bool) -> reqwest::Client {
        if disable_redirects {
            // Reuse the redirect-disabled clients already used by response-limited requests.
            return self.get_response_limited_client(request_args);
        }

        if !self.should_use_shared_client(request_args) {
            return Self::build_client(request_args, false);
        }

        self.shared_client.clone()
    }

    fn get_response_limited_client(&self, request_args: &RequestArgs) -> reqwest::Client {
        let key = ResponseLimitClientKey::from_request_args(request_args);
        let mut clients = self.response_limit_clients.lock();
        if let Some(client) = clients.get(&key) {
            return client;
        }

        let client = Self::build_client(request_args, true);
        clients.insert(key, client.clone());
        client
    }

    fn get_http2_client(
        &self,
        args: &RequestArgs,
        disable_redirects: bool,
    ) -> Result<reqwest::Client, String> {
        let mut key = ResponseLimitClientKey::from_request_args(args);
        key.disable_redirects = disable_redirects;
        let mut clients = self.http2_clients.lock();
        if args.log_event_connection_reuse {
            if let Some(client) = clients.get(&key) {
                return Ok(client);
            }
        }

        let mut builder = reqwest::Client::builder().http2_prior_knowledge();
        if disable_redirects {
            builder = builder.redirect(Policy::none());
        }
        if let Some(proxy) = &args.proxy_config {
            builder = Self::configure_proxy(builder, proxy);
        }
        if let Some(pem) = &args.ca_cert_pem {
            let certs = reqwest::Certificate::from_pem_bundle(pem)
                .map_err(|error| format!("Failed to parse HTTP/2 CA certificate: {error}"))?;
            if certs.is_empty() {
                return Err("HTTP/2 CA configuration contains no certificates".to_string());
            }
            for cert in certs {
                builder = builder.add_root_certificate(cert);
            }
        }
        let client = builder
            .build()
            .map_err(|error| format!("Failed to build HTTP/2 client: {error}"))?;
        if args.log_event_connection_reuse {
            clients.insert(key, client.clone());
        }
        Ok(client)
    }

    fn should_use_shared_client(&self, request_args: &RequestArgs) -> bool {
        if request_args.proxy_config.is_some() || request_args.ca_cert_pem.is_some() {
            return false;
        }

        (request_args.log_event_connection_reuse
            && (is_log_event_endpoint(&request_args.url)
                || is_config_sync_endpoint(&request_args.url)))
            || is_sdk_exception_endpoint(&request_args.url)
    }

    fn build_client(request_args: &RequestArgs, disable_redirects: bool) -> reqwest::Client {
        let mut client_builder = reqwest::Client::builder();
        if disable_redirects {
            client_builder = client_builder.redirect(Policy::none());
        }

        // configure proxy if available
        if let Some(proxy_config) = request_args.proxy_config.as_ref() {
            client_builder = Self::configure_proxy(client_builder, proxy_config);
        }

        if let Some(ca_cert_pem) = &request_args.ca_cert_pem {
            match reqwest::Certificate::from_pem(ca_cert_pem) {
                Ok(cert) => {
                    client_builder = client_builder.add_root_certificate(cert);
                }
                Err(e) => {
                    log_e!(TAG, "Failed to parse network CA cert PEM: {}", e);
                }
            }
        }

        client_builder.build().unwrap_or_else(|e| {
            log_e!(TAG, "Failed to build reqwest client with proxy config: {}. Falling back to default client.", e);
            Self::build_default_client(disable_redirects)
        })
    }

    fn build_default_client(disable_redirects: bool) -> reqwest::Client {
        if disable_redirects {
            return reqwest::Client::builder()
                .redirect(Policy::none())
                .build()
                .expect("default reqwest client with redirects disabled should build");
        }

        reqwest::Client::new()
    }

    fn configure_proxy(
        client_builder: reqwest::ClientBuilder,
        proxy_config: &ProxyConfig,
    ) -> reqwest::ClientBuilder {
        let (Some(host), Some(port)) = (&proxy_config.proxy_host, &proxy_config.proxy_port) else {
            return client_builder;
        };

        let proxy_url = format!(
            "{}://{}:{}",
            proxy_config.proxy_protocol.as_deref().unwrap_or("http"),
            host,
            port
        );

        let Ok(proxy) = reqwest::Proxy::all(&proxy_url) else {
            log_w!(TAG, "Failed to create proxy for URL: {}", proxy_url);
            return client_builder;
        };

        let Some(auth) = &proxy_config.proxy_auth else {
            return client_builder.proxy(proxy);
        };

        let Some((username, password)) = auth.split_once(':') else {
            log_w!(
                TAG,
                "Invalid proxy auth format. Expected 'username:password'"
            );
            return client_builder.proxy(proxy);
        };

        client_builder.proxy(proxy.basic_auth(username, password))
    }

    async fn write_unlimited_response_to_temp_file(
        response: reqwest::Response,
    ) -> Result<ResponseData, StatsigErr> {
        let headers = get_response_headers(&response);
        let mut response = response;
        let mut temp_file = tempfile::spooled_tempfile(1024 * 1024 * 2); // 2MB

        let mut total_bytes = 0;
        while let Some(item) = response
            .chunk()
            .await
            .map_err(|e| StatsigErr::FileError(e.to_string()))?
        {
            total_bytes += item.len();
            temp_file
                .write_all(&item)
                .map_err(|e| StatsigErr::FileError(e.to_string()))?;
        }

        temp_file
            .seek(SeekFrom::Start(0))
            .map_err(|e| StatsigErr::FileError(e.to_string()))?;

        let reader = BufReader::new(temp_file);

        log_d!(TAG, "Wrote {} bytes to spooled temp file", total_bytes);

        Ok(ResponseData::from_stream_with_headers(
            Box::new(reader),
            headers,
        ))
    }

    async fn write_unlimited_response_to_in_memory_buffer(
        response: reqwest::Response,
    ) -> Result<ResponseData, StatsigErr> {
        let headers = get_response_headers(&response);
        let bytes = response
            .bytes()
            .await
            .map_err(|e| StatsigErr::SerializationError(e.to_string()))?;

        log_d!(TAG, "Wrote {} bytes to in-memory buffer", bytes.len());

        Ok(ResponseData::from_bytes_with_headers(
            bytes.to_vec(),
            headers,
        ))
    }

    async fn write_response_to_temp_file(
        response: reqwest::Response,
        max_response_bytes: Option<u64>,
    ) -> Result<ResponseData, ResponseDataReadError> {
        validate_response_content_length(&response, max_response_bytes)?;
        let headers = get_response_headers(&response);
        let mut response = response;
        let mut temp_file = tempfile::spooled_tempfile(1024 * 1024 * 2); // 2MB

        let mut total_bytes = 0u64;
        while let Some(item) = response
            .chunk()
            .await
            .map_err(|e| ResponseDataReadError::from(StatsigErr::FileError(e.to_string())))?
        {
            total_bytes = checked_response_size(total_bytes, item.len(), max_response_bytes)?;
            temp_file
                .write_all(&item)
                .map_err(|e| ResponseDataReadError::from(StatsigErr::FileError(e.to_string())))?;
        }

        temp_file
            .seek(SeekFrom::Start(0))
            .map_err(|e| ResponseDataReadError::from(StatsigErr::FileError(e.to_string())))?;

        let reader = BufReader::new(temp_file);

        log_d!(TAG, "Wrote {} bytes to spooled temp file", total_bytes);

        Ok(ResponseData::from_stream_with_headers(
            Box::new(reader),
            headers,
        ))
    }

    async fn write_response_to_in_memory_buffer(
        mut response: reqwest::Response,
        max_response_bytes: Option<u64>,
    ) -> Result<ResponseData, ResponseDataReadError> {
        validate_response_content_length(&response, max_response_bytes)?;
        let headers = get_response_headers(&response);
        let mut bytes = Vec::new();
        let mut total_bytes = 0u64;
        while let Some(item) = response.chunk().await.map_err(|e| {
            ResponseDataReadError::from(StatsigErr::SerializationError(e.to_string()))
        })? {
            total_bytes = checked_response_size(total_bytes, item.len(), max_response_bytes)?;
            bytes.extend_from_slice(&item);
        }

        log_d!(TAG, "Wrote {} bytes to in-memory buffer", bytes.len());

        Ok(ResponseData::from_bytes_with_headers(bytes, headers))
    }
}

fn request_configuration_error(error: impl Into<String>) -> Response {
    Response {
        status_code: None,
        data: None,
        error: Some(error.into()),
    }
}

fn validate_response_content_length(
    response: &reqwest::Response,
    max_response_bytes: Option<u64>,
) -> Result<(), ResponseDataReadError> {
    let Some(max_response_bytes) = max_response_bytes else {
        return Ok(());
    };
    if response
        .content_length()
        .is_some_and(|content_length| content_length > max_response_bytes)
    {
        return Err(response_size_limit_error(max_response_bytes));
    }
    Ok(())
}

fn checked_response_size(
    current_bytes: u64,
    next_chunk_bytes: usize,
    max_response_bytes: Option<u64>,
) -> Result<u64, ResponseDataReadError> {
    let total_bytes = current_bytes
        .checked_add(next_chunk_bytes as u64)
        .ok_or_else(|| response_size_limit_error(max_response_bytes.unwrap_or(u64::MAX)))?;
    if max_response_bytes.is_some_and(|max_bytes| total_bytes > max_bytes) {
        return Err(response_size_limit_error(
            max_response_bytes.unwrap_or(u64::MAX),
        ));
    }
    Ok(total_bytes)
}

fn response_size_limit_error(max_response_bytes: u64) -> ResponseDataReadError {
    ResponseDataReadError::SizeLimitExceeded { max_response_bytes }
}

fn get_error_message(error: reqwest::Error) -> String {
    let mut error_message = error.to_string();

    if let Some(url_error) = error.url() {
        error_message.push_str(&format!(". URL: {}", url_error));
    }

    if let Some(status_error) = error.status() {
        error_message.push_str(&format!(". Status: {}", status_error));
    }

    error_message
}

fn is_log_event_endpoint(url: &str) -> bool {
    url_path_has_suffix(url, LOG_EVENT_REUSE_PATH)
}

fn is_sdk_exception_endpoint(url: &str) -> bool {
    url_path_has_suffix(url, SDK_EXCEPTION_REUSE_PATH)
}

fn is_config_sync_endpoint(url: &str) -> bool {
    let (_, request_path) = get_source_service_and_request_path(url);
    matches!(
        request_path.as_str(),
        "/v1/download_config_specs"
            | "/v2/download_config_specs"
            | "/v1/get_id_lists"
            | "/v1/download_id_list_file"
    )
}

fn get_response_headers(response: &reqwest::Response) -> Option<HashMap<String, String>> {
    let headers = response.headers();
    if headers.is_empty() {
        return None;
    }

    let mut headers_map = HashMap::new();
    for (key, value) in headers {
        headers_map.insert(key.to_string(), value.to_str().unwrap_or("").to_string());
    }

    Some(headers_map)
}

#[cfg(test)]
#[path = "../__tests__/net_provider_reqwest_http2_tests.rs"]
mod http2_tests;

#[cfg(test)]
mod tests {
    use super::{
        NetworkProviderReqwest, ResponseDataReadError, checked_response_size,
        is_config_sync_endpoint, is_log_event_endpoint, is_sdk_exception_endpoint,
    };
    use crate::networking::proxy_config::ProxyConfig;
    use crate::networking::{HttpMethod, NetworkProvider, RequestArgs, ResponseLimitOutcome};
    use wiremock::matchers::{method, path};
    use wiremock::{Mock, MockServer, ResponseTemplate};

    #[test]
    fn test_is_log_event_endpoint_matches_exact_suffix() {
        assert!(is_log_event_endpoint(
            "https://api.oaistatsig.com/v1/log_event"
        ));
        assert!(is_log_event_endpoint(
            "https://api.oaistatsig.com/v1/log_event/"
        ));
        assert!(is_log_event_endpoint(
            "https://api.oaistatsig.com/prefix/v1/log_event?foo=bar"
        ));

        assert!(!is_log_event_endpoint(
            "https://api.oaistatsig.com/v1/log_event/extra"
        ));
        assert!(!is_log_event_endpoint(
            "https://api.oaistatsig.com/v1/log_events"
        ));
        assert!(!is_log_event_endpoint(
            "https://api.oaistatsig.com/log_event"
        ));
    }

    #[test]
    fn test_is_sdk_exception_endpoint_matches_exact_suffix() {
        assert!(is_sdk_exception_endpoint(
            "https://api.oaistatsig.com/v1/sdk_exception"
        ));
        assert!(is_sdk_exception_endpoint(
            "https://api.oaistatsig.com/prefix/v1/sdk_exception#frag"
        ));

        assert!(!is_sdk_exception_endpoint(
            "https://api.oaistatsig.com/v1/sdk_exception/extra"
        ));
        assert!(!is_sdk_exception_endpoint(
            "https://api.oaistatsig.com/v1/sdk_exceptions"
        ));
    }

    #[test]
    fn test_checked_response_size_enforces_limit() {
        assert_eq!(checked_response_size(3, 2, Some(5)).unwrap(), 5);
        assert!(matches!(
            checked_response_size(3, 3, Some(5)),
            Err(ResponseDataReadError::SizeLimitExceeded {
                max_response_bytes: 5
            })
        ));
    }

    #[test]
    fn test_is_config_sync_endpoint_matches_supported_paths() {
        assert!(is_config_sync_endpoint(
            "https://statsigcdn.openai.com/v2/download_config_specs/secret-key.json?sinceTime=1"
        ));
        assert!(is_config_sync_endpoint(
            "https://statsigcdn.openai.com/v1/download_config_specs/secret-key.json"
        ));
        assert!(is_config_sync_endpoint(
            "https://statsigcdn.openai.com/v1/get_id_lists/secret-key.json"
        ));
        assert!(is_config_sync_endpoint(
            "https://statsigcdn.openai.com/v1/download_id_list_file/list-id"
        ));

        assert!(!is_config_sync_endpoint(
            "https://statsigcdn.openai.com/v1/log_event"
        ));
        assert!(!is_config_sync_endpoint(
            "https://statsigcdn.openai.com/v2/download_config_specs_extra/secret-key.json"
        ));
    }

    #[test]
    fn response_limited_requests_reuse_clients_by_network_configuration() {
        let provider = NetworkProviderReqwest::new();
        let request_args = RequestArgs {
            url: "https://statsigcdn.openai.com/v1/dynamic_config_value/test".to_string(),
            ..RequestArgs::new()
        };

        let _ = provider.get_client(&request_args, true);
        let _ = provider.get_client(&request_args, true);
        assert_eq!(provider.response_limit_clients.lock().entries.len(), 1);

        let mut proxied_args = request_args.clone();
        proxied_args.proxy_config = Some(ProxyConfig {
            proxy_host: Some("127.0.0.1".to_string()),
            proxy_port: Some(8080),
            proxy_auth: None,
            proxy_protocol: Some("http".to_string()),
            ca_cert_path: None,
        });
        let _ = provider.get_client(&proxied_args, true);
        assert_eq!(provider.response_limit_clients.lock().entries.len(), 2);
    }

    #[tokio::test]
    async fn response_limited_requests_do_not_follow_redirects() {
        let source = MockServer::start().await;
        let target = MockServer::start().await;
        let redirect_url = format!("{}/escaped", target.uri());

        Mock::given(method("GET"))
            .and(path("/v1/dynamic_config_value/test"))
            .respond_with(ResponseTemplate::new(302).insert_header("location", redirect_url))
            .expect(1)
            .mount(&source)
            .await;
        Mock::given(method("GET"))
            .and(path("/escaped"))
            .respond_with(ResponseTemplate::new(200).set_body_bytes(b"escaped"))
            .expect(0)
            .mount(&target)
            .await;

        let provider = NetworkProviderReqwest::new();
        let outcome = provider
            .send_with_response_limit(
                &HttpMethod::GET,
                &RequestArgs {
                    url: format!("{}/v1/dynamic_config_value/test", source.uri()),
                    ..RequestArgs::new()
                },
                1024,
            )
            .await;
        let response = match outcome {
            ResponseLimitOutcome::Response(response)
            | ResponseLimitOutcome::SizeLimitExceeded(response)
            | ResponseLimitOutcome::Unsupported(response) => response,
        };

        assert_eq!(response.status_code, Some(302));
        source.verify().await;
        target.verify().await;
    }

    #[test]
    fn test_config_sync_reuses_only_default_transport_when_enabled() {
        let provider = NetworkProviderReqwest::new();
        let mut request_args = RequestArgs {
            url: "https://statsigcdn.openai.com/v2/download_config_specs/secret-key.json"
                .to_string(),
            log_event_connection_reuse: true,
            ..RequestArgs::new()
        };

        assert!(provider.should_use_shared_client(&request_args));

        request_args.log_event_connection_reuse = false;
        assert!(!provider.should_use_shared_client(&request_args));

        request_args.log_event_connection_reuse = true;
        request_args.ca_cert_pem = Some(Vec::new());
        assert!(!provider.should_use_shared_client(&request_args));
    }
}
