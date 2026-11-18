use crate::networking::network_error::NetworkError;
use crate::networking::{HttpMethod, NetworkClient, RequestArgs, ResponseData};
use base64::{Engine, prelude::BASE64_STANDARD};
use serde::de;
use serde::{Deserialize, Deserializer, Serialize};
use std::collections::HashMap;
use std::io::Read;
use std::time::Duration;
use url::Url;

const LOOKUP_PATH: &str = "/v1/id_list_membership";
const TIMEOUT: Duration = Duration::from_millis(200);
const MAX_RESPONSE_BYTES: u64 = 1024;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) enum MembershipLookupError {
    Unavailable,
    Rejected,
}

impl MembershipLookupError {
    fn from_network(error: NetworkError) -> Self {
        match error.status_code() {
            Some(429 | 500..=599) => Self::Unavailable,
            None if matches!(
                error,
                NetworkError::DisableNetworkOn(_)
                    | NetworkError::RequestFailed(..)
                    | NetworkError::RetriesExhausted(..)
            ) =>
            {
                Self::Unavailable
            }
            _ => Self::Rejected,
        }
    }
}

#[derive(Serialize)]
struct IdListMembershipRequest<'a> {
    list_id: &'a str,
    id_type: &'a str,
    id: &'a str,
}

/// Identifies one prefix of an append-only ID-list file across SDK and SFP processes.
pub(crate) type MembershipRevision = [u8; 32];

fn deserialize_revision<'de, D: Deserializer<'de>>(
    deserializer: D,
) -> Result<Option<MembershipRevision>, D::Error> {
    let encoded = String::deserialize(deserializer)?;
    let mut digest = [0; 32];
    match BASE64_STANDARD.decode_slice(encoded, &mut digest) {
        Ok(32) => Ok(Some(digest)),
        _ => Err(de::Error::custom("invalid membership revision")),
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub(crate) struct MembershipAnswer {
    pub(crate) is_member: bool,
    pub(crate) revision: Option<MembershipRevision>,
}

#[derive(Deserialize)]
struct IdListMembershipResponse {
    #[serde(default, deserialize_with = "present")]
    is_member: Option<bool>,
    #[serde(default, deserialize_with = "deserialize_revision")]
    revision: Option<MembershipRevision>,
}

fn present<'de, D: Deserializer<'de>, T: Deserialize<'de>>(d: D) -> Result<Option<T>, D::Error> {
    T::deserialize(d).map(Some)
}

fn decode_membership_reply(
    bytes: &[u8],
) -> Result<Option<MembershipAnswer>, MembershipLookupError> {
    // Serde also accepts positional arrays for derived structs.
    if bytes.len() as u64 > MAX_RESPONSE_BYTES || !bytes.trim_ascii_start().starts_with(b"{") {
        return Err(MembershipLookupError::Rejected);
    }
    let reply: IdListMembershipResponse =
        serde_json::from_slice(bytes).map_err(|_| MembershipLookupError::Rejected)?;
    Ok(reply.is_member.map(|is_member| MembershipAnswer {
        is_member,
        revision: reply.revision,
    }))
}

/// An omitted answer leaves membership unknown.
pub(crate) async fn lookup_membership(
    network: &NetworkClient,
    endpoint: &str,
    list_id: &str,
    id_type: &str,
    id: &str,
) -> Result<Option<MembershipAnswer>, MembershipLookupError> {
    let body = IdListMembershipRequest {
        list_id,
        id_type,
        id,
    };
    let request = RequestArgs {
        url: endpoint.to_owned(),
        headers: Some(HashMap::from([(
            "Content-Type".into(),
            "application/json".into(),
        )])),
        body: Some(serde_json::to_vec(&body).map_err(|_| MembershipLookupError::Rejected)?),
        disable_file_streaming: Some(true),
        timeout_ms: TIMEOUT.as_millis() as u64,
        ..RequestArgs::new()
    };
    // Bound the complete attempt, including custom providers and response body reads.
    let response = tokio::time::timeout(
        TIMEOUT,
        network.request_once_with_redacted_response(HttpMethod::POST, request, MAX_RESPONSE_BYTES),
    )
    .await
    .map_err(|_| MembershipLookupError::Unavailable)?
    .map_err(MembershipLookupError::from_network)?;
    if response.status_code != Some(200) {
        return Err(MembershipLookupError::Rejected);
    }
    decode_membership_body(response.data.ok_or(MembershipLookupError::Rejected)?)
}

fn decode_membership_body(
    mut data: ResponseData,
) -> Result<Option<MembershipAnswer>, MembershipLookupError> {
    if let Some(bytes) = data.shared_bytes() {
        return decode_membership_reply(bytes);
    }
    // A custom provider must buffer the reply before returning. Its stream's
    // synchronous Read/Seek could otherwise block the SDK runtime past TIMEOUT.
    let stream = data
        .buffered_stream()
        .ok_or(MembershipLookupError::Rejected)?;
    stream
        .rewind()
        .map_err(|_| MembershipLookupError::Rejected)?;
    let mut bytes = Vec::new();
    stream
        .take(MAX_RESPONSE_BYTES + 1)
        .read_to_end(&mut bytes)
        .map_err(|_| MembershipLookupError::Rejected)?;
    decode_membership_reply(&bytes)
}

/// Fixed same-origin route. Without a configured primary, only the OpenAI default
/// is trusted; a future change in the SDK default must not silently reroute IDs.
pub(crate) fn membership_url(sdk_key: &str, configured: Option<&str>) -> Option<Url> {
    if !(sdk_key.starts_with("secret-") || sdk_key.starts_with("server-"))
        || sdk_key.len() > 512
        || !sdk_key
            .bytes()
            .all(|byte| byte.is_ascii_graphic() && byte != b',')
    {
        return None;
    }
    let url = http_url(
        configured.unwrap_or(crate::networking::DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX),
    )?;
    if configured.is_none() && url.origin().ascii_serialization() != "https://statsigcdn.openai.com"
    {
        return None;
    }
    url.join(LOOKUP_PATH).ok()
}

fn http_url(input: &str) -> Option<Url> {
    if input
        .bytes()
        .any(|b| b.is_ascii_whitespace() || b.is_ascii_control() || b == b'\\')
    {
        return None;
    }
    input.split_once("://")?;
    let url = Url::parse(input).ok()?;
    (matches!(url.scheme(), "http" | "https")
        && url.host().is_some()
        && url.username().is_empty()
        && url.password().is_none())
    .then_some(url)
}

#[cfg(all(test, feature = "reqwest", not(feature = "custom_network_provider")))]
#[path = "__tests__/membership_client_tests.rs"]
mod tests;
