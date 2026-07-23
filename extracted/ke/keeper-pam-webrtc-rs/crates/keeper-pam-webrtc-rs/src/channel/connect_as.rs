use aes_gcm::aead::{Aead, AeadCore, OsRng};
use aes_gcm::{Aes256Gcm, KeyInit, Nonce as AesNonce};
use anyhow::{anyhow, Result};
use hkdf::Hkdf;
use p256::{ecdh::diffie_hellman, PublicKey as P256PublicKey, SecretKey as P256SecretKey};
use serde::Deserialize;
use sha2::Sha256;

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
    pub connect_database: Option<String>,
    pub distinguished_name: Option<String>,
    pub(crate) totp: Option<String>,
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
    serde_json::from_slice(&plaintext).ok()
}

/// AES-256-GCM encrypt a JSON string and return a URL-safe no-pad base64 string.
/// Wire format: `nonce(12) || ciphertext+gcm_tag(16)` — matches Python's `_aes_gcm_encrypt`.
fn encrypt_to_url_param(json: &str, key: &[u8]) -> Option<String> {
    use base64::{engine::general_purpose::URL_SAFE_NO_PAD, Engine as _};
    let cipher = Aes256Gcm::new_from_slice(key).ok()?;
    let nonce = Aes256Gcm::generate_nonce(&mut OsRng);
    let ciphertext = cipher.encrypt(&nonce, json.as_bytes()).ok()?;
    let mut wire = nonce.to_vec();
    wire.extend_from_slice(&ciphertext);
    Some(URL_SAFE_NO_PAD.encode(&wire))
}

/// Patches the `credentials=` base64 JSON blob in a KeeperDB auto-login URL with
/// ConnectAs-supplied username, password, and/or connect_database. Only fields that
/// are `Some` are updated; existing values are preserved for `None` fields. Returns
/// the original URL unchanged if no `credentials=` param is found or decoding fails.
///
/// Handles two encoding modes produced by the Python gateway:
///   - Plain: standard base64 (percent-encoded), `auth_key` is `None`
///   - Symmetric: AES-256-GCM, URL-safe no-pad base64, `auth_key` is the 32-byte key.
///     Wire format: `nonce(12) || ciphertext+gcm_tag(16)` matches Python's `_aes_gcm_encrypt`.
pub(crate) fn patch_keeperdb_url_credentials(
    url: &str,
    username: Option<&str>,
    password: Option<&str>,
    connect_database: Option<&str>,
    auth_key: Option<&[u8]>,
) -> String {
    use base64::{engine::general_purpose::STANDARD as BASE64_STANDARD, Engine as _};

    let (base, query) = match url.split_once('?') {
        Some(parts) => parts,
        None => return url.to_string(),
    };

    let mut creds_encoded: Option<&str> = None;
    let mut other_params: Vec<&str> = Vec::new();
    for param in query.split('&') {
        if let Some(val) = param.strip_prefix("credentials=") {
            creds_encoded = Some(val);
        } else {
            other_params.push(param);
        }
    }

    let creds_encoded = match creds_encoded {
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
        );
        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "dbuser");
        assert_eq!(creds["password"], "s3cr3t");
        assert_eq!(creds["database"], "mydb");
    }

    #[test]
    fn patch_only_updates_some_fields() {
        let url = make_url("orig_user", "orig_pass", "orig_db");
        let patched = patch_keeperdb_url_credentials(&url, Some("new_user"), None, None, None);
        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "new_user");
        assert_eq!(creds["password"], "orig_pass");
        assert_eq!(creds["database"], "orig_db");
    }

    #[test]
    fn patch_preserves_other_query_params() {
        let url = make_url("", "", "");
        let patched = patch_keeperdb_url_credentials(&url, Some("u"), Some("p"), None, None);
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
        let patched = patch_keeperdb_url_credentials(&url, Some("u"), Some("p"), None, None);
        let creds = decode_credentials(&patched);
        assert_eq!(creds["type"], "Postgres");
        assert_eq!(creds["host"], "db.example.com");
        assert_eq!(creds["port"], 5432);
    }

    #[test]
    fn patch_no_credentials_param_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login?login&mode=dark&theme=dark&os=mac";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_no_query_string_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_invalid_base64_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login?credentials=not-valid-base64!!!&mode=dark";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_empty_credentials_value_returns_url_unchanged() {
        let url = "http://127.0.0.1:8080/login?credentials=&login&mode=dark";
        let result = patch_keeperdb_url_credentials(url, Some("u"), Some("p"), None, None);
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
        let result = patch_keeperdb_url_credentials(&url, Some("u"), Some("p"), None, None);
        assert_eq!(result, url);
    }

    #[test]
    fn patch_all_none_returns_url_with_original_credentials() {
        let url = make_url("orig_user", "orig_pass", "orig_db");
        let patched = patch_keeperdb_url_credentials(&url, None, None, None, None);
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
        );

        let creds = decode_credentials(&patched);
        assert_eq!(creds["username"], "dbuser");
        assert_eq!(creds["password"], "s3cr3t!");
        assert_eq!(creds["database"], "mydb");
        // Non-credential fields survive
        assert_eq!(creds["type"], "Postgres");
        assert_eq!(creds["host"], "db.example.com");
    }
}
