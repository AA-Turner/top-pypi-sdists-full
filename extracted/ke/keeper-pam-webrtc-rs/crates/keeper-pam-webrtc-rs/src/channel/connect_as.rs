use aes_gcm::aead::{Aead, AeadCore, OsRng};
use aes_gcm::{Aes256Gcm, KeyInit, Nonce as AesNonce};
use anyhow::{anyhow, Result};
use hkdf::Hkdf;
use p256::{ecdh::diffie_hellman, PublicKey as P256PublicKey, SecretKey as P256SecretKey};
use serde::Deserialize;
use sha2::Sha256;
use std::time::Duration;

// Structs for deserializing connect_as JSON payload
#[derive(Deserialize, Debug, Default)]
pub(crate) struct ConnectAsUser {
    pub(crate) username: Option<String>,
    pub(crate) password: Option<String>,
    #[serde(alias = "privatekey")]
    pub(crate) private_key: Option<String>,
    #[serde(alias = "privatekeypassphrase")]
    pub(crate) private_key_passphrase: Option<String>,
    #[serde(alias = "publickey")]
    pub(crate) public_key: Option<String>,
    pub(crate) passphrase: Option<String>,
    pub(crate) domain: Option<String>,
    #[serde(alias = "connectdatabase", alias = "connectDatabase")]
    pub connect_database: Option<String>,
    pub distinguished_name: Option<String>,
    pub(crate) totp: Option<String>,
    /// STS session token for DynamoDB KeeperDB sessions (PG-459). Only ever
    /// merged into the KeeperDB credentials blob; never a guacd param.
    #[serde(alias = "sessiontoken", alias = "sessionToken")]
    pub(crate) session_token: Option<String>,
}

#[derive(Deserialize, Debug)]
pub(crate) struct ConnectAsPayload {
    pub(crate) user: Option<ConnectAsUser>,
    pub(crate) host: Option<String>,
    pub(crate) port: Option<u16>,
}

/// Decrypts the "connect as" payload.
pub(crate) fn decrypt_connect_as_payload(
    gateway_private_key_hex: &str,
    client_public_key_bytes: &[u8],
    nonce_bytes: &[u8],
    encrypted_data: &[u8],
) -> Result<ConnectAsPayload, anyhow::Error> {
    // 1. Parse gateway's private key (hex to bytes, then to P256SecretKey)
    let private_key_bytes = ::hex::decode(gateway_private_key_hex)
        .map_err(|e| anyhow!("Failed to decode gateway private key hex: {}", e))?;
    let gateway_secret_key = P256SecretKey::from_slice(&private_key_bytes)
        .map_err(|e| anyhow!("Failed to create P256SecretKey from bytes: {}", e))?;

    // 2. Parse client's public key (bytes to P256PublicKey)
    let client_public_key =
        P256PublicKey::from_sec1_bytes(client_public_key_bytes).map_err(|e| {
            anyhow!(
                "Failed to parse client public key using from_sec1_bytes. Input len: {}. Error: {}",
                client_public_key_bytes.len(),
                e
            )
        })?;

    // 3. Perform ECDH to get shared secret
    let shared_secret = diffie_hellman(
        gateway_secret_key.to_nonzero_scalar(),
        client_public_key.as_affine(),
    );

    // 4. Use HKDF (SHA256) to derive a 32-byte symmetric key for AES-256-GCM
    let hk = Hkdf::<Sha256>::new(Some(&[]), shared_secret.raw_secret_bytes().as_ref());
    let mut symmetric_key_bytes = [0u8; 32];
    hk.expand(
        b"KEEPER_CONNECT_AS_ECIES_SECP256R1_HKDF_SHA256",
        &mut symmetric_key_bytes,
    )
    .map_err(|e| anyhow!("HKDF expand error: {}", e))?;

    // 5. Decrypt using AES-256-GCM
    let key = aes_gcm::Key::<Aes256Gcm>::from_slice(&symmetric_key_bytes);
    let cipher = Aes256Gcm::new(key);
    let nonce = AesNonce::from_slice(nonce_bytes);

    let decrypted_bytes = cipher
        .decrypt(nonce, encrypted_data)
        .map_err(|e| anyhow!("AES-GCM decryption error: {}", e))?;

    // 6. Parse decrypted bytes as JSON into ConnectAsPayload struct
    let payload: ConnectAsPayload = ::serde_json::from_slice(&decrypted_bytes)
        .map_err(|e| anyhow!("Failed to deserialize decrypted JSON payload: {}", e))?;

    Ok(payload)
}

const AES_GCM_NONCE_LEN: usize = 12;

/// Decrypt an AES-256-GCM URL-safe no-pad base64 credentials blob and parse it as JSON.
/// Wire format: `nonce(12) || ciphertext+gcm_tag(16)` — matches Python's `_aes_gcm_encrypt`.
fn decrypt_and_parse(encoded: &str, auth_key: Option<&[u8]>) -> Option<serde_json::Value> {
    use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
    let key = auth_key?;
    let wire = URL_SAFE_NO_PAD.decode(encoded).ok()?;
    if wire.len() <= AES_GCM_NONCE_LEN {
        return None;
    }
    let (nonce_bytes, ciphertext) = wire.split_at(AES_GCM_NONCE_LEN);
    let nonce = AesNonce::from_slice(nonce_bytes);
    let cipher = Aes256Gcm::new_from_slice(key).ok()?;
    let plaintext = cipher.decrypt(nonce, ciphertext).ok()?;
    // KDB-98: the Python gateway gzip-compresses the JSON plaintext when that
    // shrinks it (so large tokens fit under the RBI browser's URL limit), and
    // KeeperDB inflates by sniffing the gzip magic (`1f 8b`). Uncompressed JSON
    // begins with `{`, so mirror that: inflate when the magic is present,
    // otherwise parse the plaintext directly.
    let json_bytes = if plaintext.starts_with(&[0x1f, 0x8b]) {
        use std::io::Read as _;
        // Bound inflation to guard against a decompression bomb. A connect-as
        // credentials blob is small (well under this even with large tokens);
        // anything larger is malformed or hostile, so fail the patch (which
        // leaves the URL unchanged) rather than inflate unbounded.
        const MAX_INFLATED_LEN: u64 = 1 << 20; // 1 MiB
        let mut out = Vec::new();
        flate2::read::GzDecoder::new(&plaintext[..])
            .take(MAX_INFLATED_LEN + 1)
            .read_to_end(&mut out)
            .ok()?;
        if out.len() as u64 > MAX_INFLATED_LEN {
            return None;
        }
        out
    } else {
        plaintext
    };
    serde_json::from_slice(&json_bytes).ok()
}

/// AES-256-GCM encrypt a JSON string and return a URL-safe no-pad base64 string.
/// Wire format: `nonce(12) || ciphertext+gcm_tag(16)` — matches Python's `_aes_gcm_encrypt`.
fn encrypt_to_url_param(json: &str, key: &[u8]) -> Option<String> {
    use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
    let cipher = Aes256Gcm::new_from_slice(key).ok()?;
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
    // KDB-98: mirror Python's `_aes_gcm_encrypt` — gzip the JSON when that is
    // smaller than the raw bytes so large payloads stay under the RBI URL limit.
    // KeeperDB sniffs the gzip magic to inflate; uncompressed JSON (`{`) stays
    // backward-compatible, so fall back to raw bytes when compression doesn't help.
    let raw = json.as_bytes();
    let plaintext = {
        use std::io::Write as _;
        let mut encoder = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::best());
        match encoder.write_all(raw).and_then(|_| encoder.finish()) {
            Ok(compressed) if compressed.len() < raw.len() => compressed,
            _ => raw.to_vec(),
        }
    };
    let ciphertext = cipher.encrypt(&nonce, plaintext.as_slice()).ok()?;
    let mut wire = nonce.to_vec();
    wire.extend_from_slice(&ciphertext);
    Some(URL_SAFE_NO_PAD.encode(&wire))
}

/// Splits a KeeperDB auto-login URL into `(base, credentials, other_params)`;
/// `None` if there is no `credentials=` param.
fn split_url_credentials(url: &str) -> Option<(&str, &str, Vec<&str>)> {
    let (base, query) = url.split_once('?')?;

    let mut creds_encoded: Option<&str> = None;
    let mut other_params: Vec<&str> = Vec::new();
    for param in query.split('&') {
        if let Some(val) = param.strip_prefix("credentials=") {
            creds_encoded = Some(val);
        } else {
            other_params.push(param);
        }
    }

    Some((base, creds_encoded?, other_params))
}

/// Patches the `credentials=` base64 JSON blob in a KeeperDB auto-login URL with
/// ConnectAs-supplied username, password, and/or connect_database. Only fields that
/// are `Some` are updated; existing values are preserved for `None` fields. Returns
/// the original URL unchanged if no `credentials=` param is found or decoding fails.
///
/// `session_token` is written to `advanced_options.session_token` only when the
/// blob's `advanced_options.driver` is `"dynamodb"`; it is ignored otherwise.
///
/// Handles two encoding modes produced by the Python gateway:
///   - Plain: standard base64 (percent-encoded), `auth_key` is `None`
///   - Symmetric: AES-256-GCM, URL-safe no-pad base64, `auth_key` is the 32-byte key.
///     Wire format: `nonce(12) || ciphertext+gcm_tag(16)` matches Python's `_aes_gcm_encrypt`.
///
/// Staging the patched blob happens afterwards via [`stage_keeperdb_url_via_handoff`].
pub(crate) fn patch_keeperdb_url_credentials(
    url: &str,
    username: Option<&str>,
    password: Option<&str>,
    connect_database: Option<&str>,
    session_token: Option<&str>,
    auth_key: Option<&[u8]>,
) -> String {
    use base64::{engine::general_purpose::STANDARD as BASE64_STANDARD, Engine as _};

    let (base, creds_encoded, other_params) = match split_url_credentials(url) {
        Some(v) => v,
        None => return url.to_string(),
    };

    // Try to decode and parse the credentials blob. Two formats:
    //   Plain: standard base64, percent-encoded (+→%2B, /→%2F, =→%3D)
    //   Symmetric: URL-safe no-pad base64, no percent-encoding
    // Returns (json_value, is_encrypted).
    let (mut creds, is_encrypted) = {
        // --- Plain mode: percent-decode then standard base64 ---
        let decoded_b64 = creds_encoded
            .replace("%2B", "+")
            .replace("%2b", "+")
            .replace("%2F", "/")
            .replace("%2f", "/")
            .replace("%3D", "=")
            .replace("%3d", "=");

        if let Ok(json_bytes) = BASE64_STANDARD.decode(&decoded_b64) {
            if let Ok(v) = serde_json::from_slice::<serde_json::Value>(&json_bytes) {
                if v.is_object() {
                    (v, false)
                } else {
                    return url.to_string();
                }
            } else {
                // Standard base64 decoded but not JSON — try AES-GCM path below.
                match decrypt_and_parse(creds_encoded, auth_key) {
                    Some(v) => (v, true),
                    None => return url.to_string(),
                }
            }
        } else {
            // Not standard base64 — try AES-GCM (URL-safe no-pad).
            match decrypt_and_parse(creds_encoded, auth_key) {
                Some(v) => (v, true),
                None => return url.to_string(),
            }
        }
    };

    if let Some(u) = username {
        creds["username"] = serde_json::Value::String(u.to_string());
    }
    if let Some(p) = password {
        creds["password"] = serde_json::Value::String(p.to_string());
    }
    if let Some(db) = connect_database {
        creds["database"] = serde_json::Value::String(db.to_string());
    }
    if let Some(token) = session_token {
        match creds
            .get_mut("advanced_options")
            .and_then(|opts| opts.as_object_mut())
        {
            Some(opts)
                if opts.get("driver").and_then(|driver| driver.as_str()) == Some("dynamodb") =>
            {
                opts.insert(
                    "session_token".to_string(),
                    serde_json::Value::String(token.to_string()),
                );
            }
            // Never log the token itself.
            _ => log::debug!(
                "ConnectAs session token ignored: KeeperDB credentials blob is not a DynamoDB session"
            ),
        }
    }

    let new_json = match serde_json::to_string(&creds) {
        Ok(s) => s,
        Err(_) => return url.to_string(),
    };

    let new_creds_param = if is_encrypted {
        match auth_key {
            Some(key) => match encrypt_to_url_param(&new_json, key) {
                Some(s) => s,
                None => return url.to_string(),
            },
            None => return url.to_string(),
        }
    } else {
        let new_b64 = BASE64_STANDARD.encode(new_json.as_bytes());

        new_b64
            .replace('+', "%2B")
            .replace('/', "%2F")
            .replace('=', "%3D")
    };

    let mut new_query = format!("credentials={}", new_creds_param);
    for param in &other_params {
        new_query.push('&');
        new_query.push_str(param);
    }
    format!("{}?{}", base, new_query)
}

/// `<scheme>://<authority>/api/auth/handoff`, derived from the Gateway-authored auto-login URL.
fn derive_handoff_endpoint(url: &str) -> Option<String> {
    let authority_start = url.find("://")? + 3;
    let path_start = authority_start + url[authority_start..].find('/')?;
    Some(format!("{}/api/auth/handoff", &url[..path_start]))
}

/// `<base>?handoff=<token>&<other params>`, percent-encoding the token like the
/// Gateway's `quote(token, safe='')`.
fn build_handoff_url(base: &str, token: &str, other_params: &[&str]) -> String {
    let mut encoded_token = String::with_capacity(token.len());
    for byte in token.as_bytes() {
        match byte {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'-' | b'.' | b'_' | b'~' => {
                encoded_token.push(*byte as char)
            }
            _ => encoded_token.push_str(&format!("%{:02X}", byte)),
        }
    }
    let mut url = format!("{}?handoff={}", base, encoded_token);
    for param in other_params {
        url.push('&');
        url.push_str(param);
    }
    url
}

/// Stages the `credentials=` blob with KeeperDB's handoff endpoint (KDB-183) and
/// returns the `?handoff=<token>` URL, or `None` to keep the original URL. Mirrors
/// the Gateway's own pre-stage in `keeperdb_proc.py` (same endpoint, body, timeout).
/// `auth_key` is only checked for presence: KeeperDB accepts Symmetric-mode blobs only.
/// Never logs the blob, token, or URL.
pub(crate) async fn stage_keeperdb_url_via_handoff(
    url: &str,
    auth_key: Option<&str>,
    timeout: Duration,
    channel_id: &str,
    conversation_id: &str,
) -> Option<String> {
    auth_key?;
    let (base, creds_value, other_params) = split_url_credentials(url)?;
    let endpoint = derive_handoff_endpoint(url)?;

    let client = reqwest::Client::new();
    let response = match client
        .post(&endpoint)
        .json(&serde_json::json!({ "credentials": creds_value }))
        .timeout(timeout)
        .send()
        .await
    {
        Ok(resp) => resp,
        Err(e) => {
            // Never `{}`-format the reqwest error: its Display includes the URL.
            let kind = if e.is_timeout() {
                "timeout"
            } else if e.is_connect() {
                "connect"
            } else {
                "request"
            };
            log::warn!(
                "KeeperDB handoff staging failed ({}); using ?credentials= URL (channel_id: {}, conversation_id: {})",
                kind, channel_id, conversation_id
            );
            return None;
        }
    };

    let status = response.status();
    if status == reqwest::StatusCode::NOT_FOUND || status == reqwest::StatusCode::METHOD_NOT_ALLOWED
    {
        log::info!(
            "KeeperDB build does not support handoff ({}); using ?credentials= URL (channel_id: {}, conversation_id: {})",
            status.as_u16(), channel_id, conversation_id
        );
        return None;
    }
    if !status.is_success() {
        log::warn!(
            "KeeperDB handoff staging returned HTTP {}; using ?credentials= URL (channel_id: {}, conversation_id: {})",
            status.as_u16(), channel_id, conversation_id
        );
        return None;
    }

    let body: Option<serde_json::Value> = response.json().await.ok();
    let token = match body.as_ref().and_then(|b| b.get("token")?.as_str()) {
        Some(t) if !t.is_empty() => t,
        _ => {
            log::warn!(
                "KeeperDB handoff staging response carried no token; using ?credentials= URL (channel_id: {}, conversation_id: {})",
                channel_id, conversation_id
            );
            return None;
        }
    };

    log::debug!(
        "KeeperDB credentials staged via handoff (channel_id: {}, conversation_id: {})",
        channel_id,
        conversation_id
    );
    Some(build_handoff_url(base, token, &other_params))
}

#[cfg(test)]
mod tests {
    use super::*;
    use base64::{engine::general_purpose::STANDARD as BASE64_STANDARD, Engine as _};

    fn make_url(username: &str, password: &str, database: &str) -> String {
        let creds = serde_json::json!({
            "type": "Postgres",
            "username": username,
            "password": password,
            "host": "db.example.com",
            "local": "en_US",
            "database": database,
            "port": 5432
        });
        let b64 = BASE64_STANDARD.encode(creds.to_string().as_bytes());
        let encoded = b64
            .replace('+', "%2B")
            .replace('/', "%2F")
            .replace('=', "%3D");
        format!(
            "http://127.0.0.1:8080/login?credentials={}&login&mode=dark&theme=dark&os=mac",
            encoded
        )
    }

    fn decode_credentials(url: &str) -> serde_json::Value {
        let query = url.split_once('?').unwrap().1;
        let encoded = query
            .split('&')
            .find_map(|p| p.strip_prefix("credentials="))
            .unwrap();
        let b64 = encoded
            .replace("%2B", "+")
            .replace("%2b", "+")
            .replace("%2F", "/")
            .replace("%2f", "/")
            .replace("%3D", "=")
            .replace("%3d", "=");
        let bytes = BASE64_STANDARD.decode(&b64).unwrap();
        serde_json::from_slice(&bytes).unwrap()
    }

    #[test]
    fn patch_applies_all_credential_fields() {
        let url = make_url("", "", "");
        let patched = patch_keeperdb_url_credentials(
            &url,
            Some("dbuser"),
            Some("s3cr3t"),
            Some("mydb"),
            None,
            None,
        );
        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "dbuser");
        assert_eq!(creds["password"], "s3cr3t");
        assert_eq!(creds["database"], "mydb");
    }

    #[test]
    fn patch_only_updates_some_fields() {
        let url = make_url("orig_user", "orig_pass", "orig_db");
        let patched =
            patch_keeperdb_url_credentials(&url, Some("new_user"), None, None, None, None);
        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "new_user");
        assert_eq!(creds["password"], "orig_pass");
        assert_eq!(creds["database"], "orig_db");
    }

    #[test]
    fn patch_preserves_other_query_params() {
        let url = make_url("", "", "");
        let patched = patch_keeperdb_url_credentials(&url, Some("u"), Some("p"), None, None, None);
        let query = patched.split_once('?').unwrap().1;
        let params: Vec<&str> = query.split('&').collect();
        assert!(params.contains(&"login"));
        assert!(params.contains(&"mode=dark"));
        assert!(params.contains(&"theme=dark"));
        assert!(params.contains(&"os=mac"));
    }

    #[test]
    fn patch_preserves_non_credential_json_fields() {
        let url = make_url("", "", "");
        let patched = patch_keeperdb_url_credentials(&url, Some("u"), Some("p"), None, None, None);
        let creds = decode_credentials(&patched);
        assert_eq!(creds["type"], "Postgres");
        assert_eq!(creds["host"], "db.example.com");
        assert_eq!(creds["port"], 5432);
    }

    #[test]
    fn patch_no_credentials_param_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login?login&mode=dark&theme=dark&os=mac";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_no_query_string_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_invalid_base64_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login?credentials=not-valid-base64!!!&mode=dark";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_empty_credentials_value_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login?credentials=&login&mode=dark";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_non_object_json_returns_url_unchanged() {
        // Valid base64 of a JSON non-object — indexing this would panic without the is_object guard
        let b64 = BASE64_STANDARD.encode(b"\"just a string\"");
        let encoded = b64
            .replace('+', "%2B")
            .replace('/', "%2F")
            .replace('=', "%3D");
        let url = format!(
            "http://127.0.0.1:8080/login?credentials={}&mode=dark",
            encoded
        );
        let result = patch_keeperdb_url_credentials(&url, Some("u"), Some("p"), None, None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_all_none_returns_url_with_original_credentials() {
        let url = make_url("orig_user", "orig_pass", "orig_db");
        let patched = patch_keeperdb_url_credentials(&url, None, None, None, None, None);
        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "orig_user");
        assert_eq!(creds["password"], "orig_pass");
        assert_eq!(creds["database"], "orig_db");
    }

    #[test]
    fn connect_as_user_fields_patch_keeperdb_url() {
        // Mirrors the protocol.rs ConnectAs block: clone before move, then patch.
        let user_details = ConnectAsUser {
            username: Some("dbuser".to_string()),
            password: Some("s3cr3t!".to_string()),
            connect_database: Some("mydb".to_string()),
            ..Default::default()
        };

        // Clone before moving into guacd_params (as protocol.rs does)
        let ca_username = user_details.username.clone();
        let ca_password = user_details.password.clone();
        let ca_connect_database = user_details.connect_database.clone();

        // Python-generated URL with empty placeholder credentials
        let url = make_url("", "", "");

        let patched = patch_keeperdb_url_credentials(
            &url,
            ca_username.as_deref(),
            ca_password.as_deref(),
            ca_connect_database.as_deref(),
            None,
            None,
        );

        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "dbuser");
        assert_eq!(creds["password"], "s3cr3t!");
        assert_eq!(creds["database"], "mydb");
        // Non-credential fields survive
        assert_eq!(creds["type"], "Postgres");
        assert_eq!(creds["host"], "db.example.com");
    }

    // --- Encrypted (AES-256-GCM) + gzip blob tests (KDB-98) ---

    fn creds_param(url: &str) -> String {
        url.split_once('?')
            .unwrap()
            .1
            .split('&')
            .find_map(|p| p.strip_prefix("credentials="))
            .unwrap()
            .to_string()
    }

    fn decrypt_raw(param: &str, key: &[u8]) -> Vec<u8> {
        use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
        let wire = URL_SAFE_NO_PAD.decode(param).unwrap();
        let (nonce_bytes, ct) = wire.split_at(AES_GCM_NONCE_LEN);
        let cipher = Aes256Gcm::new_from_slice(key).unwrap();
        cipher
            .decrypt(AesNonce::from_slice(nonce_bytes), ct)
            .unwrap()
    }

    fn inflate_if_gzip(bytes: Vec<u8>) -> Vec<u8> {
        if bytes.starts_with(&[0x1f, 0x8b]) {
            use std::io::Read as _;
            let mut out = Vec::new();
            flate2::read::GzDecoder::new(&bytes[..])
                .read_to_end(&mut out)
                .unwrap();
            out
        } else {
            bytes
        }
    }

    /// Build a URL whose `credentials=` blob is AES-256-GCM over GZIP-compressed
    /// JSON — exactly what the Python gateway's `_aes_gcm_encrypt` emits.
    fn make_encrypted_gzip_url(
        key: &[u8],
        username: &str,
        password: &str,
        database: &str,
    ) -> String {
        use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
        use std::io::Write as _;
        let creds = serde_json::json!({
            "type": "MariaDB",
            "username": username,
            "password": password,
            "host": "127.0.0.1",
            "local": "en_US",
            "database": database,
            "port": 33306,
            // Long, compressible field so gzip is genuinely smaller than raw,
            // guaranteeing the compressed wire format is exercised.
            "user_id": "a".repeat(128)
        });
        let raw = creds.to_string().into_bytes();
        let mut enc = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::best());
        enc.write_all(&raw).unwrap();
        let compressed = enc.finish().unwrap();
        assert!(
            compressed.len() < raw.len(),
            "fixture must exercise gzip path"
        );
        let cipher = Aes256Gcm::new_from_slice(key).unwrap();
        let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
        let ct = cipher.encrypt(&nonce, compressed.as_slice()).unwrap();
        let mut wire = nonce.to_vec();
        wire.extend_from_slice(&ct);
        format!(
            "http://127.0.0.1:8080/login?credentials={}&login&mode=dark",
            URL_SAFE_NO_PAD.encode(&wire)
        )
    }

    #[test]
    fn patch_encrypted_gzip_blob_updates_credentials() {
        // Regression (KDB-98): the Python gateway AES-GCM-encrypts GZIP-compressed
        // JSON. Before the inflate fix, decrypt_and_parse ran serde_json on the raw
        // gzip bytes, failed, and patch returned the URL unchanged -> empty creds
        // reached KeeperDB -> auth failure. Verify the blob is decrypted, inflated,
        // patched with the ConnectAs values, and re-encrypted.
        let key = [7u8; 32];
        let url = make_encrypted_gzip_url(&key, "", "", "");
        let patched = patch_keeperdb_url_credentials(
            &url,
            Some("root"),
            Some("s3cr3t!"),
            Some("mydb"),
            None,
            Some(&key),
        );
        assert_ne!(
            patched, url,
            "encrypted blob must be re-written, not returned unchanged"
        );
        let creds: serde_json::Value =
            serde_json::from_slice(&inflate_if_gzip(decrypt_raw(&creds_param(&patched), &key)))
                .unwrap();
        assert_eq!(creds["username"], "root");
        assert_eq!(creds["password"], "s3cr3t!");
        assert_eq!(creds["database"], "mydb");
        assert_eq!(creds["type"], "MariaDB");
    }

    #[test]
    fn encrypt_to_url_param_uses_gzip_and_roundtrips() {
        // A compressible payload must take the gzip branch, and decrypt_and_parse
        // must inflate it back to the original JSON.
        let key = [9u8; 32];
        let json = serde_json::json!({
            "type": "MariaDB",
            "database": "d",
            "token": "x".repeat(400)
        })
        .to_string();
        let param = encrypt_to_url_param(&json, &key).unwrap();
        // Stored plaintext is gzip (magic present before inflate).
        assert_eq!(&decrypt_raw(&param, &key)[..2], &[0x1f, 0x8b]);
        let round = decrypt_and_parse(&param, Some(&key)).unwrap();
        assert_eq!(round["database"], "d");
        assert_eq!(round["token"], "x".repeat(400));
    }

    #[test]
    fn encrypt_to_url_param_skips_gzip_when_not_smaller() {
        // Tiny payloads don't compress; the plaintext stays raw JSON (`{`) and
        // still round-trips.
        let key = [3u8; 32];
        let param = encrypt_to_url_param(r#"{"a":1}"#, &key).unwrap();
        assert_eq!(decrypt_raw(&param, &key)[0], b'{');
        assert_eq!(decrypt_and_parse(&param, Some(&key)).unwrap()["a"], 1);
    }

    #[test]
    fn connect_as_user_deserializes_connect_database_aliases() {
        // Regression: the vault sends the DB field as `connectdatabase`
        // (lowercase-joined) or `connectDatabase` (camelCase). Without the serde
        // alias these silently deserialized to None and the DB never reached the URL.
        let a: ConnectAsUser =
            serde_json::from_str(r#"{"username":"root","connectdatabase":"mydb"}"#).unwrap();
        assert_eq!(a.connect_database.as_deref(), Some("mydb"));
        let b: ConnectAsUser = serde_json::from_str(r#"{"connectDatabase":"other"}"#).unwrap();
        assert_eq!(b.connect_database.as_deref(), Some("other"));
        let c: ConnectAsUser = serde_json::from_str(r#"{"connect_database":"snake"}"#).unwrap();
        assert_eq!(c.connect_database.as_deref(), Some("snake"));
    }

    #[test]
    fn decrypt_and_parse_rejects_decompression_bomb() {
        use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
        use std::io::Write as _;
        let key = [5u8; 32];
        // 2 MiB of highly compressible data inflates past the 1 MiB cap.
        let huge = vec![b'a'; 2 * 1024 * 1024];
        let mut enc = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::best());
        enc.write_all(&huge).unwrap();
        let compressed = enc.finish().unwrap();
        let cipher = Aes256Gcm::new_from_slice(&key).unwrap();
        let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
        let ct = cipher.encrypt(&nonce, compressed.as_slice()).unwrap();
        let mut wire = nonce.to_vec();
        wire.extend_from_slice(&ct);
        let param = URL_SAFE_NO_PAD.encode(&wire);
        // Exceeds the inflate cap -> None (patch leaves the URL unchanged).
        assert!(decrypt_and_parse(&param, Some(&key)).is_none());
    }

    // --- DynamoDB session token (PG-459) ---

    fn make_url_from_json(creds: serde_json::Value) -> String {
        let encoded = BASE64_STANDARD
            .encode(creds.to_string().as_bytes())
            .replace('+', "%2B")
            .replace('/', "%2F")
            .replace('=', "%3D");
        format!(
            "http://127.0.0.1:8080/login?credentials={}&login&mode=dark",
            encoded
        )
    }

    fn dynamodb_creds() -> serde_json::Value {
        serde_json::json!({
            "type": "DynamoDB",
            "username": "",
            "password": "",
            "host": "dynamodb.us-east-1.amazonaws.com",
            "advanced_options": {"driver": "dynamodb"}
        })
    }

    #[test]
    fn patch_merges_session_token_into_dynamodb_advanced_options() {
        let url = make_url_from_json(dynamodb_creds());
        let patched = patch_keeperdb_url_credentials(
            &url,
            Some("AKIAEXAMPLE"),
            Some("secret-key"),
            None,
            Some("sts-session-token"),
            None,
        );
        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "AKIAEXAMPLE");
        assert_eq!(creds["password"], "secret-key");
        assert_eq!(creds["advanced_options"]["driver"], "dynamodb");
        assert_eq!(
            creds["advanced_options"]["session_token"],
            "sts-session-token"
        );
        // Never leaks to the top level of the blob.
        assert!(creds.get("session_token").is_none());
    }

    #[test]
    fn patch_session_token_overrides_existing_and_keeps_other_options() {
        let mut blob = dynamodb_creds();
        blob["advanced_options"]["session_token"] = "stale".into();
        blob["advanced_options"]["endpoint_url"] = "http://localhost:4566".into();
        let url = make_url_from_json(blob);
        let patched = patch_keeperdb_url_credentials(&url, None, None, None, Some("fresh"), None);
        let creds = decode_credentials(&patched);
        assert_eq!(creds["advanced_options"]["session_token"], "fresh");
        assert_eq!(
            creds["advanced_options"]["endpoint_url"],
            "http://localhost:4566"
        );
    }

    #[test]
    fn patch_encrypted_dynamodb_blob_merges_session_token() {
        let key = [11u8; 32];
        let url = format!(
            "http://127.0.0.1:8080/login?credentials={}&login",
            encrypt_to_url_param(&dynamodb_creds().to_string(), &key).unwrap()
        );
        let patched = patch_keeperdb_url_credentials(
            &url,
            Some("AKIAEXAMPLE"),
            Some("secret-key"),
            None,
            Some("sts-session-token"),
            Some(&key),
        );
        let creds = decrypt_and_parse(&creds_param(&patched), Some(&key)).unwrap();
        assert_eq!(creds["username"], "AKIAEXAMPLE");
        assert_eq!(
            creds["advanced_options"]["session_token"],
            "sts-session-token"
        );
    }

    #[test]
    fn patch_ignores_session_token_for_non_dynamodb_driver() {
        let url = make_url_from_json(serde_json::json!({
            "type": "MSSQL",
            "username": "",
            "advanced_options": {"driver": "mssql", "auth_mode": "aad_token"}
        }));
        let patched = patch_keeperdb_url_credentials(&url, None, None, None, Some("tok"), None);
        let creds = decode_credentials(&patched);
        assert!(creds["advanced_options"].get("session_token").is_none());
        assert_eq!(creds["advanced_options"]["driver"], "mssql");
    }

    #[test]
    fn patch_ignores_session_token_without_advanced_options() {
        let url = make_url("", "", "");
        let patched = patch_keeperdb_url_credentials(&url, None, None, None, Some("tok"), None);
        let creds = decode_credentials(&patched);
        assert!(creds.get("advanced_options").is_none());
        assert!(creds.get("session_token").is_none());
    }

    #[test]
    fn connect_as_user_deserializes_session_token_aliases() {
        let a: ConnectAsUser = serde_json::from_str(r#"{"sessionToken":"camel"}"#).unwrap();
        assert_eq!(a.session_token.as_deref(), Some("camel"));
        let b: ConnectAsUser = serde_json::from_str(r#"{"sessiontoken":"joined"}"#).unwrap();
        assert_eq!(b.session_token.as_deref(), Some("joined"));
        let c: ConnectAsUser = serde_json::from_str(r#"{"session_token":"snake"}"#).unwrap();
        assert_eq!(c.session_token.as_deref(), Some("snake"));
        let d: ConnectAsUser = serde_json::from_str(r#"{"username":"u"}"#).unwrap();
        assert!(d.session_token.is_none());
    }

    // --- KeeperDB handoff staging (PG-459) ---
    //
    // Mock server: a raw `tokio::net::TcpListener` on 127.0.0.1:0 (no
    // axum/wiremock — not a dependency of this crate). Accepts one
    // connection, reads the request (headers + `Content-Length` body),
    // captures it, writes a canned HTTP/1.1 response, closes.

    /// Reads one HTTP/1.1 request (headers + `Content-Length` body) off `stream`
    /// and returns the raw bytes.
    async fn read_http_request(stream: &mut tokio::net::TcpStream) -> Vec<u8> {
        use tokio::io::AsyncReadExt;
        let mut buf = Vec::new();
        let mut chunk = [0u8; 4096];
        let mut headers_end = None;
        loop {
            let n = stream.read(&mut chunk).await.unwrap();
            if n == 0 {
                break;
            }
            buf.extend_from_slice(&chunk[..n]);
            if headers_end.is_none() {
                headers_end = buf
                    .windows(4)
                    .position(|w| w == b"\r\n\r\n")
                    .map(|pos| pos + 4);
            }
            if let Some(end) = headers_end {
                let content_length = String::from_utf8_lossy(&buf[..end])
                    .lines()
                    .find_map(|l| {
                        l.to_lowercase()
                            .strip_prefix("content-length:")
                            .map(|v| v.trim().to_string())
                    })
                    .and_then(|v| v.parse::<usize>().ok())
                    .unwrap_or(0);
                if buf.len() >= end + content_length {
                    break;
                }
            }
        }
        buf
    }

    /// Parses a captured raw HTTP/1.1 request into `(method, path, json_body)`.
    fn parse_mock_request(raw: &[u8]) -> (String, String, serde_json::Value) {
        let text = String::from_utf8_lossy(raw);
        let header_end = text.find("\r\n\r\n").expect("no header/body separator");
        let request_line = text[..header_end]
            .lines()
            .next()
            .expect("empty request line");
        let mut parts = request_line.split_whitespace();
        let method = parts.next().unwrap().to_string();
        let path = parts.next().unwrap().to_string();
        let body: serde_json::Value = serde_json::from_str(&text[header_end + 4..]).unwrap();
        (method, path, body)
    }

    /// A canned `200 OK` HTTP/1.1 response with a JSON body.
    fn http_200_json(body: &str) -> String {
        format!(
            "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {}\r\n\r\n{}",
            body.len(),
            body
        )
    }

    /// A canned HTTP/1.1 response with the given status and no body.
    fn http_status(code: u16, reason: &str) -> String {
        format!("HTTP/1.1 {} {}\r\nContent-Length: 0\r\n\r\n", code, reason)
    }

    /// Binds a mock handoff server on `127.0.0.1:0`, accepts exactly one
    /// connection, captures the raw request, writes `response`, and closes.
    /// Returns the bound port and a `JoinHandle` resolving to the captured
    /// request bytes once the exchange completes. Shared by every test below
    /// so the mock-server plumbing lives in one place.
    async fn spawn_mock_handoff_server(
        response: String,
    ) -> (u16, tokio::task::JoinHandle<Vec<u8>>) {
        use tokio::io::AsyncWriteExt;
        let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let port = listener.local_addr().unwrap().port();
        let handle = tokio::spawn(async move {
            let (mut stream, _) = listener.accept().await.unwrap();
            let raw = read_http_request(&mut stream).await;
            stream.write_all(response.as_bytes()).await.unwrap();
            let _ = stream.shutdown().await;
            raw
        });
        (port, handle)
    }

    /// Binds a listener that accepts a connection but never responds
    /// (simulates a KeeperDB build that accepts the TCP connection and hangs)
    /// — used for the timeout scenario. Returns the port; the accept task is
    /// aborted by the caller once the test is done with it.
    async fn spawn_accept_only_listener() -> (u16, tokio::task::JoinHandle<()>) {
        let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let port = listener.local_addr().unwrap().port();
        let handle = tokio::spawn(async move {
            let (_stream, _) = listener.accept().await.unwrap();
            // Accept the connection but never respond or close — the caller's
            // request should time out.
            std::future::pending::<()>().await
        });
        (port, handle)
    }

    /// Stages `url` in Symmetric mode with the production timeout.
    async fn stage(url: &str) -> Option<String> {
        stage_keeperdb_url_via_handoff(
            url,
            Some("auth-key"),
            Duration::from_secs(5),
            "chan",
            "conv",
        )
        .await
    }

    /// Builds an encrypted `credentials=` param and the full login URL around
    /// it, given a mock server port and the trailing params to keep.
    fn staged_url(port: u16, key: &[u8; 32], trailing: &str) -> (String, String) {
        let creds_param =
            encrypt_to_url_param(&serde_json::json!({"type": "Postgres"}).to_string(), key)
                .unwrap();
        (
            format!(
                "http://127.0.0.1:{}/login?credentials={}{}",
                port, creds_param, trailing
            ),
            creds_param,
        )
    }

    #[tokio::test]
    async fn stage_handoff_success_rewrites_url_and_posts_exact_blob() {
        let key = [42u8; 32];
        let (port, handle) =
            spawn_mock_handoff_server(http_200_json(r#"{"token":"tok_123"}"#)).await;
        let (url, creds_param) = staged_url(port, &key, "&login&mode=dark&theme=dark&os=mac");

        let result = stage(&url).await.expect("expected a staged URL");

        assert_eq!(
            result,
            format!(
                "http://127.0.0.1:{}/login?handoff=tok_123&login&mode=dark&theme=dark&os=mac",
                port
            )
        );

        let raw = handle.await.unwrap();
        let (method, path, body) = parse_mock_request(&raw);
        assert_eq!(method, "POST");
        assert_eq!(path, "/api/auth/handoff");
        assert_eq!(body["credentials"], creds_param);
    }

    #[tokio::test]
    async fn stage_handoff_percent_encodes_reserved_chars_in_token() {
        let key = [1u8; 32];
        let (port, _handle) =
            spawn_mock_handoff_server(http_200_json(r#"{"token":"a+b/c="}"#)).await;
        let (url, _) = staged_url(port, &key, "&login");

        let result = stage(&url).await.expect("expected a staged URL");

        assert_eq!(
            result,
            format!("http://127.0.0.1:{}/login?handoff=a%2Bb%2Fc%3D&login", port)
        );
    }

    #[tokio::test]
    async fn stage_handoff_non_200_status_keeps_original_url() {
        let key = [2u8; 32];
        for (code, reason) in [
            (405, "Method Not Allowed"),
            (404, "Not Found"),
            (500, "Internal Server Error"),
        ] {
            let (port, _handle) = spawn_mock_handoff_server(http_status(code, reason)).await;
            let (url, _) = staged_url(port, &key, "&login");

            let result = stage(&url).await;
            assert!(
                result.is_none(),
                "HTTP {} should keep the original URL",
                code
            );
        }
    }

    #[tokio::test]
    async fn stage_handoff_bad_response_body_keeps_original_url() {
        let key = [10u8; 32];
        let non_json_body = "not json";
        let non_json_response = format!(
            "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}",
            non_json_body.len(),
            non_json_body
        );
        for response in [
            http_200_json("{}"),
            http_200_json(r#"{"token":""}"#),
            non_json_response,
        ] {
            let (port, _handle) = spawn_mock_handoff_server(response).await;
            let (url, _) = staged_url(port, &key, "&login");

            let result = stage(&url).await;
            assert!(
                result.is_none(),
                "bad response body should keep the original URL"
            );
        }
    }

    #[tokio::test]
    async fn stage_handoff_connection_refused_returns_promptly() {
        // Bind then immediately drop, so nothing is listening on this port.
        let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
        let port = listener.local_addr().unwrap().port();
        drop(listener);

        let url = format!("http://127.0.0.1:{}/login?credentials=anything&login", port);

        let start = std::time::Instant::now();
        let result = stage(&url).await;
        assert!(result.is_none());
        assert!(
            start.elapsed() < Duration::from_secs(2),
            "connection-refused should fail promptly, not wait out the timeout"
        );
    }

    #[tokio::test]
    async fn stage_handoff_times_out_without_waiting_full_timeout() {
        let (port, accept_handle) = spawn_accept_only_listener().await;
        let url = format!("http://127.0.0.1:{}/login?credentials=anything&login", port);

        let start = std::time::Instant::now();
        let result = stage_keeperdb_url_via_handoff(
            &url,
            Some("auth-key"),
            Duration::from_millis(200),
            "chan",
            "conv",
        )
        .await;
        let elapsed = start.elapsed();
        assert!(result.is_none());
        assert!(
            elapsed < Duration::from_secs(2),
            "must respect the caller-supplied timeout, not the production 5s default"
        );
        accept_handle.abort();
    }

    #[tokio::test]
    async fn stage_handoff_nothing_to_stage_makes_no_request() {
        // (query string, auth key): already-handoff form (Gateway pre-staged,
        // e.g. Entra), no query string, no `credentials=` key, and Plain mode.
        let cases = [
            ("?handoff=already-staged&login", Some("auth-key")),
            ("", Some("auth-key")),
            ("?login&mode=dark", Some("auth-key")),
            ("?credentials=anything&login", None),
        ];
        for (query, auth_key) in cases {
            let listener = tokio::net::TcpListener::bind("127.0.0.1:0").await.unwrap();
            let port = listener.local_addr().unwrap().port();
            let accept_handle = tokio::spawn(async move { listener.accept().await });
            let url = format!("http://127.0.0.1:{}/login{}", port, query);

            let result = stage_keeperdb_url_via_handoff(
                &url,
                auth_key,
                Duration::from_secs(5),
                "chan",
                "conv",
            )
            .await;
            assert!(result.is_none());
            assert!(
                !accept_handle.is_finished(),
                "no connection should have been attempted for {}",
                query
            );
            accept_handle.abort();
        }
    }

    #[tokio::test]
    async fn stage_handoff_full_chain_dynamodb_session_token() {
        let key = [77u8; 32];
        let (port, handle) =
            spawn_mock_handoff_server(http_200_json(r#"{"token":"tok_chain"}"#)).await;
        let base_creds_param = encrypt_to_url_param(&dynamodb_creds().to_string(), &key).unwrap();
        let base_url = format!(
            "http://127.0.0.1:{}/login?credentials={}&login",
            port, base_creds_param
        );

        // Merge ConnectAs values (as protocol.rs does) before staging.
        let patched_url = patch_keeperdb_url_credentials(
            &base_url,
            Some("AKIAEXAMPLE"),
            Some("secret-key"),
            None,
            Some("sts-session-token"),
            Some(&key),
        );

        let result = stage(&patched_url).await.expect("expected a staged URL");
        assert_eq!(
            result,
            format!("http://127.0.0.1:{}/login?handoff=tok_chain&login", port)
        );

        let raw = handle.await.unwrap();
        let (_, _, body) = parse_mock_request(&raw);
        let posted_creds_param = body["credentials"].as_str().unwrap();
        let decrypted = decrypt_and_parse(posted_creds_param, Some(&key)).unwrap();
        assert_eq!(decrypted["username"], "AKIAEXAMPLE");
        assert_eq!(decrypted["password"], "secret-key");
        assert_eq!(
            decrypted["advanced_options"]["session_token"],
            "sts-session-token"
        );
        assert_eq!(decrypted["advanced_options"]["driver"], "dynamodb");
    }
}
