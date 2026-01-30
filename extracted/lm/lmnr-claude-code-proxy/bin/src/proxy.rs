use crate::anthropic::request::PostMessagesRequest;
use crate::anthropic::response::MessageResponse;
use crate::spans::utils::{is_gzip_encoded, parse_span_id, parse_sse_events, parse_trace_id};
use crate::spans::{
    CompletedSpawningToolSpan, CompletedToolSpan, NestedContext, RegistrationContext,
    ResponseFailure, ResponseInfo, SpanProcessor, build_tool_span_request, create_span_request,
};
use crate::state::{CurrentTraceAndLaminarContext, SharedState};

use futures_util::stream::{Stream, StreamExt};
use http_body_util::{BodyExt, Full, StreamBody, combinators::BoxBody};
use hyper::{
    Method, Request, Response, StatusCode,
    body::{Bytes, Frame, Incoming},
};
use hyper_rustls::HttpsConnector;
use hyper_util::client::legacy::{Client, connect::HttpConnector};
use prost::Message;
use std::sync::Mutex;
use std::{
    pin::Pin,
    sync::Arc,
    task::{Context, Poll},
    time::{Duration, SystemTime, UNIX_EPOCH},
};
use tokio::task::JoinSet;

const CREATE_MESSAGE_PATH: &str = "/v1/messages";
const FOUNDRY_CREATE_MESSAGE_PATH: &str = "/anthropic/v1/messages";

fn get_unix_nano() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_else(|_| {
            eprintln!("System misconfigured: Time went backwards. Defaulting to 0.");
            Duration::from_nanos(0)
        })
        .as_nanos() as u64
}

fn should_create_span(uri_path: &str) -> bool {
    // The proper way would be to check for
    // azure endpoint and foundry path, but it's unlikely that Anthropic's
    // API will ever have a /anthropic path, so it's a safe assumption.
    uri_path == CREATE_MESSAGE_PATH || uri_path == FOUNDRY_CREATE_MESSAGE_PATH
}

fn is_azure_endpoint(host: &str) -> bool {
    host.contains("azure.com") || host.contains("services.ai")
}

async fn send_trace_to_lmnr(
    trace_request: crate::proto::opentelemetry_collector_trace_v1::ExportTraceServiceRequest,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    project_api_key: String,
    laminar_url: String,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let endpoint = format!("{laminar_url}/v1/traces");

    // Encode the protobuf message
    let mut buf = Vec::new();
    if let Err(e) = trace_request.encode(&mut buf) {
        eprintln!("Failed to encode trace request: {}", e);
        return Err(e.into());
    }

    // Build the request body
    let body = Full::new(Bytes::from(buf))
        .map_err(|never| match never {})
        .boxed();

    // Build the request with Authorization header
    let auth_header = format!("Bearer {}", project_api_key);
    let req = match Request::builder()
        .method(Method::POST)
        .uri(&endpoint)
        .header("content-type", "application/x-protobuf")
        .header("authorization", auth_header)
        .body(body)
    {
        Ok(req) => req,
        Err(e) => {
            eprintln!("Failed to build request: {}", e);
            return Err(e.into());
        }
    };

    // Send the request
    match client.request(req).await {
        Ok(response) => {
            let status = response.status();
            if !status.is_success() {
                eprintln!("Failed to send trace to LMNR: status {}", status);
            }
        }
        Err(e) => {
            eprintln!("Failed to send trace to LMNR: {}", e);
            return Err(e.into());
        }
    };

    Ok(())
}

async fn send_tool_span<T: Into<crate::spans::ToolSpanData>>(
    span: T,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    project_api_key: String,
    laminar_url: String,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let export_request = build_tool_span_request(span.into())?;
    send_trace_to_lmnr(export_request, client, project_api_key, laminar_url).await
}

struct SpanCapturingStream<S> {
    inner: S,
    accumulated: Arc<Mutex<Vec<Bytes>>>,
    request_body: String,
    trace: Option<CurrentTraceAndLaminarContext>,
    start_time_unix_nano: u64,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    background_tasks: Arc<Mutex<JoinSet<()>>>,
    uri_path: String,
    span_processor: Arc<SpanProcessor>,
    nested_context: Option<NestedContext>,
    has_gzip_content_encoding: bool,
    response_status: StatusCode,
}

impl<S> Stream for SpanCapturingStream<S>
where
    S: Stream<Item = Result<Bytes, hyper::Error>> + Unpin,
{
    type Item = Result<Bytes, hyper::Error>;

    fn poll_next(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        match Pin::new(&mut self.inner).poll_next(cx) {
            Poll::Ready(Some(Ok(bytes))) => {
                // Push directly to accumulated using synchronous mutex
                // This ensures all bytes are captured before stream ends
                if let Ok(mut accumulated) = self.accumulated.lock() {
                    accumulated.push(bytes.clone());
                }
                Poll::Ready(Some(Ok(bytes)))
            }
            Poll::Ready(None) => {
                // Stream ended successfully - create span
                if should_create_span(&self.uri_path) {
                    self.create_span_in_background();
                }
                Poll::Ready(None)
            }
            Poll::Ready(Some(Err(e))) => {
                // Stream ended with error - still try to create span with partial data
                if should_create_span(&self.uri_path) {
                    self.create_span_in_background();
                }
                Poll::Ready(Some(Err(e)))
            }
            Poll::Pending => Poll::Pending,
        }
    }
}

impl<S> SpanCapturingStream<S>
where
    S: Stream<Item = Result<Bytes, hyper::Error>> + Unpin,
{
    fn create_span_in_background(&self) {
        // Capture end time right when stream ends
        let end_time_unix_nano = get_unix_nano();
        let accumulated = self.accumulated.clone();
        let request_body = self.request_body.clone();
        let trace = self.trace.clone();
        let start_time_unix_nano = self.start_time_unix_nano;
        let client = self.client.clone();
        let background_tasks = self.background_tasks.clone();
        let span_processor = self.span_processor.clone();
        let nested_context = self.nested_context.clone();
        let has_gzip_content_encoding = self.has_gzip_content_encoding;

        // Extract response body from accumulated chunks synchronously
        // This must be done before spawning to avoid holding MutexGuard across await
        // Keep as bytes to preserve binary data (e.g., gzip)
        let response_bytes = {
            match accumulated.lock() {
                Ok(chunks) => {
                    let total_size: usize = chunks.iter().map(|b| b.len()).sum();
                    let mut bytes = Vec::with_capacity(total_size);
                    for chunk in chunks.iter() {
                        bytes.extend_from_slice(chunk);
                    }
                    bytes
                }
                Err(e) => {
                    eprintln!("Failed to lock accumulated chunks: {}", e);
                    return;
                }
            }
            // MutexGuard is automatically dropped here
        };

        // ============================================================
        // SYNCHRONOUS SECTION: Parse and register spans immediately
        // This prevents race conditions where the next request arrives
        // before registration completes
        // ============================================================

        // Parse the request to check if streaming is enabled
        let parsed_request: Option<PostMessagesRequest> = serde_json::from_str(&request_body).ok();

        // Parse the response - handle both streaming and non-streaming
        let parsed_response: Option<MessageResponse> = parsed_request.as_ref().and_then(|req| {
            if req.stream {
                // Streaming response: parse SSE events
                let response_str = String::from_utf8_lossy(&response_bytes);
                let events = parse_sse_events(&response_str);
                MessageResponse::try_from_stream_events(events).ok()
            } else {
                // Non-streaming response: may be gzip-encoded
                if is_gzip_encoded(&response_bytes, has_gzip_content_encoding) {
                    return None;
                }
                let string_response_body = String::from_utf8_lossy(&response_bytes).to_string();
                serde_json::from_str(&string_response_body).ok()
            }
        });

        // If response contains tool calls, register them with the processor SYNCHRONOUSLY
        let server_tool_spans: Vec<CompletedToolSpan> =
            if let (Some(trace_ctx), Some(response)) = (&trace, &parsed_response) {
                if let (Ok(trace_id_bytes), Ok(span_id_bytes)) = (
                    parse_trace_id(&trace_ctx.trace_id),
                    parse_span_id(&trace_ctx.span_id),
                ) {
                    // Create registration context for this request
                    let reg_ctx = RegistrationContext::new(
                        trace_id_bytes,
                        span_id_bytes,
                        trace_ctx.span_ids_path.clone(),
                        trace_ctx.span_path.clone(),
                        end_time_unix_nano, // Tool starts when response is received
                    );

                    // Register spawning tool calls (Task, WebSearch, Bash) with proper parent context
                    span_processor.register_spawning_tool_calls(
                        response,
                        nested_context.as_ref(),
                        &reg_ctx,
                    );

                    // Also register spawning tools as pending tool spans for timing
                    span_processor.register_spawning_tools_as_pending(response, &reg_ctx);

                    // Register regular tool calls
                    span_processor.register_tool_calls(response, nested_context.as_ref(), &reg_ctx);

                    // Extract completed server tool spans (web_search, etc.)
                    span_processor.extract_server_tool_spans(
                        response,
                        nested_context.as_ref(),
                        &reg_ctx,
                    )
                } else {
                    Vec::new()
                }
            } else {
                Vec::new()
            };

        // Update child end time for spawning tools if this LLM span is in a nested context
        // This ensures spawning tools know when their last child span ended
        if let Some(ref ctx) = nested_context {
            span_processor.update_child_end_time(&ctx.parent_tool_use_id, end_time_unix_nano);
        }

        let response_info = if !self.response_status.is_success() {
            Some(ResponseInfo::Failure(ResponseFailure {
                status_code: self.response_status,
                body: response_bytes,
            }))
        } else {
            parsed_response.map(|resp| ResponseInfo::Success(resp))
        };

        // ============================================================
        // ASYNC SECTION: Only network I/O runs in background
        // ============================================================

        // Spawn background task on the JoinSet for graceful shutdown tracking
        let result = background_tasks.lock().map(|mut join_set| {
            join_set.spawn(async move {
                if let Some(trace) = trace {
                    // If in subagent context, use the Task's span as parent for LLM spans
                    use crate::spans::utils::bytes_to_uuid_like_string;
                    let (effective_parent_span_id, effective_span_ids_path, effective_span_path): (
                        String,
                        Vec<String>,
                        Vec<String>,
                    ) = if let Some(ref ctx) = nested_context {
                        // Convert parent_tool_span_id_bytes to string for parent
                        let parent_id = bytes_to_uuid_like_string(ctx.parent_tool_span_id_bytes())
                            .unwrap_or_else(|_| trace.span_id.clone());
                        (
                            parent_id,
                            ctx.span_ids_path().clone(),
                            ctx.span_path().clone(),
                        )
                    } else {
                        (
                            trace.span_id.clone(),
                            trace.span_ids_path.clone(),
                            trace.span_path.clone(),
                        )
                    };

                    if let (Some(req), Some(response_info)) = (parsed_request, response_info) {
                        match create_span_request(
                            trace.trace_id.clone(),
                            effective_parent_span_id,
                            effective_span_ids_path,
                            start_time_unix_nano,
                            end_time_unix_nano,
                            effective_span_path,
                            req,
                            response_info,
                        ) {
                            Ok(span_request) => {
                                if let Err(e) = send_trace_to_lmnr(
                                    span_request,
                                    client.clone(),
                                    trace.project_api_key.clone(),
                                    trace.laminar_url.clone(),
                                )
                                .await
                                {
                                    eprintln!("Failed to send trace to LMNR: {}", e);
                                }
                            }
                            Err(e) => {
                                eprintln!("Failed to create span request: {}", e);
                            }
                        }
                    }

                    // Send server tool spans (web_search, etc.)
                    for span in server_tool_spans {
                        if let Err(e) = send_tool_span(
                            span,
                            client.clone(),
                            trace.project_api_key.clone(),
                            trace.laminar_url.clone(),
                        )
                        .await
                        {
                            eprintln!("Failed to send server tool span: {}", e);
                        }
                    }
                }
            })
        });
        if let Err(e) = result {
            eprintln!("Failed to lock background task: {}", e);
        }
    }
}

pub async fn handle(
    req: Request<Incoming>,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    target_url: String,
    state: SharedState,
    span_processor: Arc<SpanProcessor>,
    background_tasks: Arc<Mutex<JoinSet<()>>>,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    let method = req.method().clone();
    let uri = req.uri();
    let path = uri.path();

    // Handle internal span context endpoint
    if path == "/lmnr-internal/span-context" && method == Method::POST {
        return handle_span_context(req, state).await;
    }

    if path == "/lmnr-internal/health" && method == Method::GET {
        return handle_health().await;
    }

    forward_request(
        req,
        client,
        target_url,
        state,
        span_processor,
        background_tasks,
    )
    .await
}

async fn handle_health()
-> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    Ok(Response::builder().status(StatusCode::OK).body(
        Full::new(Bytes::from("{\"status\":\"ok\"}"))
            .map_err(|never| match never {})
            .boxed(),
    )?)
}
async fn handle_span_context(
    req: Request<Incoming>,
    state: SharedState,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    let body_bytes = req.collect().await?.to_bytes();

    match serde_json::from_slice::<CurrentTraceAndLaminarContext>(&body_bytes) {
        Ok(trace) => {
            let state_guard = state.lock();
            if let Ok(mut state_guard) = state_guard {
                state_guard.trace_context = Some(trace.clone());
                drop(state_guard);
            } else {
                eprintln!("Failed to lock state for span context");
            }

            let response = Response::builder().status(StatusCode::OK).body(
                Full::new(Bytes::from("{\"status\":\"ok\"}"))
                    .map_err(|never| match never {})
                    .boxed(),
            )?;
            Ok(response)
        }
        Err(e) => {
            let error_msg = format!("{{\"error\":\"Invalid JSON: {}\"}}", e);
            let response = Response::builder().status(StatusCode::BAD_REQUEST).body(
                Full::new(Bytes::from(error_msg))
                    .map_err(|never| match never {})
                    .boxed(),
            )?;
            Ok(response)
        }
    }
}

/// Attempts to infer the correct scheme (http or https) for a URL without a scheme.
/// Tries HTTPS first (preferred), then HTTP if HTTPS fails with a connection error.
///
/// Returns the successful scheme and response, or an error if both fail.
async fn try_infer_scheme(
    parts: hyper::http::request::Parts,
    body_bytes: Bytes,
    base_url: &str,
    path_and_query: &str,
    client: &Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
) -> Result<(String, Response<hyper::body::Incoming>), Box<dyn std::error::Error + Send + Sync>> {
    // Try HTTPS first (preferred)
    let https_url = format!("https://{}", base_url);
    let https_uri = format!("{}{}", https_url, path_and_query).parse();

    if let Ok(https_uri) = https_uri {
        let mut https_parts = parts.clone();
        https_parts.uri = https_uri;

        // Recreate body for HTTPS attempt
        let https_body = Full::new(body_bytes.clone())
            .map_err(|never| match never {})
            .boxed();

        if is_azure_endpoint(&https_url) {
            https_parts.version = hyper::Version::HTTP_2;
            https_parts.headers.remove(hyper::header::HOST);
            https_parts.headers.remove(hyper::header::CONNECTION);
        }

        let https_req = Request::from_parts(https_parts, https_body);

        if let Ok(response) = client.request(https_req).await {
            return Ok(("https".to_string(), response));
        }
        // else fall through to try HTTP
    }

    // Try HTTP as fallback
    let http_url = format!("http://{}", base_url);
    let http_uri = format!("{}{}", http_url, path_and_query)
        .parse()
        .map_err(|e| {
            eprintln!("Failed to parse HTTP URI: {}", e);
            e
        })?;

    let mut http_parts = parts;
    http_parts.uri = http_uri;

    let http_body = Full::new(body_bytes)
        .map_err(|never| match never {})
        .boxed();

    if is_azure_endpoint(&http_url) {
        http_parts.version = hyper::Version::HTTP_2;
        http_parts.headers.remove(hyper::header::HOST);
        http_parts.headers.remove(hyper::header::CONNECTION);
    }

    let http_req = Request::from_parts(http_parts, http_body);

    match client.request(http_req).await {
        Ok(response) => {
            // HTTP worked! Return it.
            Ok(("http".to_string(), response))
        }
        Err(e) => {
            // Both HTTPS and HTTP failed with connection errors.
            // Return the HTTP error (most recent one)
            Err(e.into())
        }
    }
}

async fn forward_request(
    req: Request<Incoming>,
    client: Client<HttpsConnector<HttpConnector>, BoxBody<Bytes, hyper::Error>>,
    target_url: String,
    state: SharedState,
    span_processor: Arc<SpanProcessor>,
    background_tasks: Arc<Mutex<JoinSet<()>>>,
) -> Result<Response<BoxBody<Bytes, hyper::Error>>, Box<dyn std::error::Error + Send + Sync>> {
    let (parts, body) = req.into_parts();
    let uri = &parts.uri;
    let path_and_query = uri.path_and_query().map(|x| x.as_str()).unwrap_or("/");
    let uri_path = uri.path().to_string();

    // Determine if we need to infer the scheme
    let needs_scheme_inference = !(target_url.to_lowercase().starts_with("http://")
        || target_url.to_lowercase().starts_with("https://"));

    // Collect request body early as we might need it for scheme inference
    let req_body_bytes = body.collect().await?.to_bytes();
    let req_body_str = String::from_utf8_lossy(&req_body_bytes).to_string();

    // Parse request to check for tool results and subagent context
    let parsed_request: Option<PostMessagesRequest> = serde_json::from_str(&req_body_str).ok();

    // Check if this request belongs to a subagent
    let nested_context = parsed_request
        .as_ref()
        .and_then(|req| span_processor.find_nested_context(req));

    // Get the current time for completing any tool spans
    let tool_result_time = get_unix_nano();

    // Complete any pending tool spans from tool_results in this request
    let completed_tool_spans: Vec<CompletedToolSpan> = parsed_request
        .as_ref()
        .map(|req| span_processor.complete_tool_spans(req, tool_result_time))
        .unwrap_or_default();

    // Complete any pending task spans from Task tool_results in this request
    let completed_spawning_tool_spans: Vec<CompletedSpawningToolSpan> = parsed_request
        .as_ref()
        .map(|req| span_processor.complete_spawning_tool_spans(req, tool_result_time))
        .unwrap_or_default();

    // Capture start time right before sending request
    let start_time_unix_nano = get_unix_nano();

    // Handle scheme inference or use provided URL
    let resp = if needs_scheme_inference {
        // Check cache first
        let cached_scheme = {
            let state_guard = state.lock();
            match state_guard {
                Ok(state) => state
                    .inferred_schemes
                    .get(&target_url)
                    .map(|x| x.value().clone()),
                Err(e) => {
                    eprintln!("Failed to lock state for scheme cache: {}", e);
                    None
                }
            }
        };

        if let Some(scheme) = cached_scheme {
            // Use cached scheme
            let url_with_scheme = format!("{}://{}", scheme, target_url);
            let target_uri = format!("{}{}", url_with_scheme, path_and_query)
                .parse()
                .map_err(|e| {
                    eprintln!("Failed to parse target URI: {}", e);
                    e
                })?;

            let mut parts_clone = parts.clone();
            parts_clone.uri = target_uri;

            let new_body = Full::new(req_body_bytes.clone())
                .map_err(|never| match never {})
                .boxed();

            if is_azure_endpoint(&url_with_scheme) {
                parts_clone.version = hyper::Version::HTTP_2;
                parts_clone.headers.remove(hyper::header::HOST);
                parts_clone.headers.remove(hyper::header::CONNECTION);
            }

            let proxy_req = Request::from_parts(parts_clone, new_body);
            client.request(proxy_req).await?
        } else {
            eprintln!("Inferring scheme for target URL: {}", target_url);
            // Need to infer the scheme
            let (inferred_scheme, resp) = try_infer_scheme(
                parts.clone(),
                req_body_bytes.clone(),
                &target_url,
                path_and_query,
                &client,
            )
            .await?;

            // Cache the inferred scheme (only if not already cached to avoid race conditions)
            // Use entry().or_insert() to ensure first successful inference wins
            let state_guard = state.lock();
            if let Ok(mut state) = state_guard {
                state
                    .inferred_schemes
                    .entry(target_url.clone())
                    .or_insert(inferred_scheme.clone());
            } else {
                eprintln!("Failed to lock state to cache inferred scheme");
            }

            resp
        }
    } else {
        // URL already has scheme, use it directly
        let target_uri = format!("{}{}", target_url, path_and_query)
            .parse()
            .map_err(|e| {
                eprintln!("Failed to parse target URI: {}", e);
                e
            })?;

        let mut parts_clone = parts.clone();
        parts_clone.uri = target_uri;

        let new_body = Full::new(req_body_bytes.clone())
            .map_err(|never| match never {})
            .boxed();

        if is_azure_endpoint(&target_url) {
            parts_clone.version = hyper::Version::HTTP_2;
            parts_clone.headers.remove(hyper::header::HOST);
            parts_clone.headers.remove(hyper::header::CONNECTION);
        }

        let proxy_req = Request::from_parts(parts_clone, new_body);
        client.request(proxy_req).await?
    };

    let (parts, body) = resp.into_parts();

    // Check if response is gzip-encoded
    let is_gzip_encoded = parts
        .headers
        .get(hyper::header::CONTENT_ENCODING)
        .and_then(|v| v.to_str().ok())
        .map(|v| v.eq_ignore_ascii_case("gzip"))
        .unwrap_or(false);

    let response_status = parts.status;

    // Get trace context
    let trace = match state.lock() {
        Ok(state) => state.trace_context.clone(),
        Err(e) => {
            eprintln!("Failed to lock state for trace context: {}", e);
            None
        }
    };

    // Send completed tool spans in background
    let all_tool_spans: Vec<crate::spans::ToolSpanData> = completed_tool_spans
        .into_iter()
        .map(Into::into)
        .chain(completed_spawning_tool_spans.into_iter().map(Into::into))
        .collect();

    if !all_tool_spans.is_empty() {
        if let Some(ref trace_ctx) = trace {
            let client_clone = client.clone();
            let trace_ctx_clone = trace_ctx.clone();
            let background_tasks_clone = background_tasks.clone();

            if let Ok(mut join_set) = background_tasks_clone.lock() {
                join_set.spawn(async move {
                    for span in all_tool_spans {
                        if let Err(e) = send_tool_span(
                            span,
                            client_clone.clone(),
                            trace_ctx_clone.project_api_key.clone(),
                            trace_ctx_clone.laminar_url.clone(),
                        )
                        .await
                        {
                            eprintln!("Failed to send tool span: {}", e);
                        }
                    }
                });
            }
        }
    }

    // Wrap the response body in a stream that captures chunks while forwarding them
    let body_stream = body.into_data_stream();
    let capturing_stream = SpanCapturingStream {
        inner: body_stream,
        accumulated: Arc::new(Mutex::new(Vec::new())),
        request_body: req_body_str,
        trace,
        start_time_unix_nano,
        client: client.clone(),
        background_tasks,
        uri_path,
        span_processor,
        nested_context,
        has_gzip_content_encoding: is_gzip_encoded,
        response_status,
    };

    let streaming_body =
        StreamBody::new(capturing_stream.map(|result| result.map(|bytes| Frame::data(bytes))));

    Ok(Response::from_parts(parts, BodyExt::boxed(streaming_body)))
}
