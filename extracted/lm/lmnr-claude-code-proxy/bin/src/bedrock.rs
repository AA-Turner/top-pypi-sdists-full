use base64::Engine;
use hyper::body::Bytes;
use std::time::SystemTime;

use crate::anthropic::stream::StreamEvent;

const BEDROCK_INVOKE_SUFFIX: &str = "/invoke";
const BEDROCK_INVOKE_STREAM_SUFFIX: &str = "/invoke-with-response-stream";

pub fn is_bedrock_path(path: &str) -> bool {
    path.starts_with("/model/")
        && (path.ends_with(BEDROCK_INVOKE_SUFFIX) || path.ends_with(BEDROCK_INVOKE_STREAM_SUFFIX))
}

pub fn is_bedrock_endpoint(host: &str) -> bool {
    host.contains("bedrock-runtime") && host.contains("amazonaws.com")
}

fn load_aws_credentials()
-> Result<(String, String, Option<String>), Box<dyn std::error::Error + Send + Sync>> {
    if let (Ok(ak), Ok(sk)) = (
        std::env::var("AWS_ACCESS_KEY_ID"),
        std::env::var("AWS_SECRET_ACCESS_KEY"),
    ) {
        return Ok((ak, sk, std::env::var("AWS_SESSION_TOKEN").ok()));
    }

    // Fall back to ~/.aws/credentials
    let profile = std::env::var("AWS_PROFILE").unwrap_or_else(|_| "default".to_string());

    let credentials_path = std::env::var("AWS_SHARED_CREDENTIALS_FILE")
        .map(std::path::PathBuf::from)
        .unwrap_or_else(|_| {
            std::env::var("HOME")
                .or_else(|_| std::env::var("USERPROFILE"))
                .map(std::path::PathBuf::from)
                .unwrap_or_default()
                .join(".aws")
                .join("credentials")
        });

    let contents = std::fs::read_to_string(&credentials_path).map_err(|e| {
        format!(
            "cannot read credentials file {}: {e}",
            credentials_path.display()
        )
    })?;

    // Parse INI: find [profile] section then extract key = value pairs
    let mut in_section = false;
    let mut access_key: Option<String> = None;
    let mut secret_key: Option<String> = None;
    let mut session_token: Option<String> = None;

    for line in contents.lines() {
        let line = line.trim();
        if line.starts_with('[') {
            let section = line.trim_start_matches('[').trim_end_matches(']').trim();
            in_section = section == profile;
            if access_key.is_some() && secret_key.is_some() {
                break; // already have what we need from a previous section
            }
            continue;
        }
        if !in_section {
            continue;
        }
        if let Some((key, val)) = line.split_once('=') {
            match key.trim() {
                "aws_access_key_id" => access_key = Some(val.trim().to_string()),
                "aws_secret_access_key" => secret_key = Some(val.trim().to_string()),
                "aws_session_token" => session_token = Some(val.trim().to_string()),
                _ => {}
            }
        }
    }

    match (access_key, secret_key) {
        (Some(ak), Some(sk)) => Ok((ak, sk, session_token)),
        _ => Err(format!(
            "profile [{profile}] not found or missing credentials in {}",
            credentials_path.display()
        )
        .into()),
    }
}

pub async fn update_bedrock_signature(
    parts: &mut hyper::http::request::Parts,
    body: &Bytes,
    target_url: &str,
    path_and_query: &str,
) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    use aws_credential_types::Credentials;
    use aws_sigv4::http_request::{SignableBody, SignableRequest, SigningSettings, sign};
    use aws_sigv4::sign::v4;

    let (access_key, secret_key, session_token) = load_aws_credentials()?;

    // "https://bedrock-runtime.us-east-1.amazonaws.com" → "bedrock-runtime.us-east-1.amazonaws.com"
    let bedrock_host = target_url
        .trim_start_matches("https://")
        .trim_start_matches("http://")
        .trim_end_matches('/')
        .to_string();

    // "bedrock-runtime.us-east-1.amazonaws.com" → "us-east-1"
    let region = bedrock_host
        .split('.')
        .nth(1)
        .ok_or("cannot extract region from Bedrock host")?
        .to_string();

    // Strip existing AWS auth headers so the new signature is clean
    parts.headers.remove("authorization");
    parts.headers.remove("x-amz-date");
    parts.headers.remove("x-amz-security-token");
    parts.headers.remove("x-amz-content-sha256");

    // Set the Host to the real Bedrock endpoint so it's included in the signature
    parts.headers.insert(
        hyper::header::HOST,
        hyper::header::HeaderValue::from_str(&bedrock_host)
            .map_err(|e| format!("invalid Bedrock host: {e}"))?,
    );

    let real_url = format!("https://{bedrock_host}{path_and_query}");

    let credentials = Credentials::new(&access_key, &secret_key, session_token, None, "env");
    let identity = credentials.into();

    let signing_params = v4::SigningParams::builder()
        .identity(&identity)
        .region(&region)
        .name("bedrock")
        .time(SystemTime::now())
        .settings(SigningSettings::default())
        .build()?
        .into();

    // Collect owned strings to avoid a borrow of parts.headers while we mutate it below
    let header_pairs: Vec<(String, String)> = parts
        .headers
        .iter()
        .filter_map(|(k, v)| v.to_str().ok().map(|vs| (k.to_string(), vs.to_string())))
        .collect();

    let signable = SignableRequest::new(
        parts.method.as_str(),
        &real_url,
        header_pairs.iter().map(|(k, v)| (k.as_str(), v.as_str())),
        SignableBody::Bytes(body),
    )?;

    let (instructions, _) = sign(signable, &signing_params)?.into_parts();

    for (name, value) in instructions.headers() {
        if let Ok(name) = hyper::header::HeaderName::from_bytes(name.as_bytes()) {
            parts.headers.insert(
                name,
                hyper::header::HeaderValue::from_str(value)
                    .map_err(|e| format!("invalid signing header value: {e}"))?,
            );
        }
    }

    Ok(())
}

/// Parse an AWS event stream binary response (from `/invoke-with-response-stream`) into
/// Anthropic `StreamEvent`s.
///
/// Wire format per message:
///   [4] total_byte_length  (big-endian u32, includes itself)
///   [4] headers_byte_length (big-endian u32)
///   [4] prelude_crc         (big-endian u32, ignored)
///   [headers_byte_length] headers
///   [payload_length] payload   where payload_length = total - headers - 16
///   [4] message_crc         (big-endian u32, ignored)
///
/// Each payload is JSON `{"bytes":"<base64>","p":"<padding>"}` where the base64
/// decodes to a regular Anthropic streaming event JSON object.
pub fn parse_bedrock_event_stream(data: &[u8]) -> Vec<StreamEvent> {
    let mut events = Vec::new();
    let mut pos = 0;

    while pos + 12 <= data.len() {
        let total_len =
            u32::from_be_bytes([data[pos], data[pos + 1], data[pos + 2], data[pos + 3]]) as usize;

        // Sanity check: minimum valid frame is 16 bytes (no headers, no payload)
        if total_len < 16 || pos + total_len > data.len() {
            break;
        }

        let headers_len =
            u32::from_be_bytes([data[pos + 4], data[pos + 5], data[pos + 6], data[pos + 7]])
                as usize;

        // prelude CRC is at pos+8..pos+12 (skipped)
        let payload_start = pos + 12 + headers_len;
        let payload_end = pos + total_len - 4; // strip trailing message CRC

        if payload_start > payload_end || payload_end > data.len() {
            pos += total_len;
            continue;
        }

        let payload = &data[payload_start..payload_end];

        if let Ok(json) = serde_json::from_slice::<serde_json::Value>(payload) {
            if let Some(b64) = json.get("bytes").and_then(|v| v.as_str()) {
                if let Ok(decoded) = base64::engine::general_purpose::STANDARD.decode(b64) {
                    if let Ok(event) = serde_json::from_slice::<StreamEvent>(&decoded) {
                        events.push(event);
                    }
                }
            }
        }

        pos += total_len;
    }

    events
}
