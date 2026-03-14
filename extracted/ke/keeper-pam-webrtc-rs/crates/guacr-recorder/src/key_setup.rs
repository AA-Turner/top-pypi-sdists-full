// Key derivation and metadata encryption matching the Python gateway.
//
// Python derive_key:
//   HKDF(SHA256, length=32, salt=salt, info=info).derive(secret_bytes)
//
// Python tunnel_encrypt:
//   nonce = os.urandom(12)
//   base64(nonce + AESGCM(key).encrypt(nonce, data, None))
//
// Python key_info:
//   endpoint_name.encode() + b"_RECORDING-SESSION_AES-GCM-256"
//
// Python recording_associated (meta_js):
//   {
//     "conversationUid": endpoint_name,
//     "resourceUid": resource_record.uid,
//     "resourceKeysSalt": base64(resource_key_salt),
//     "resourceData": tunnel_encrypt(derive_key(resource_key_bytes, salt, info), private_meta),
//     "userUid": user_uid | null,
//     "userKeySalt": base64(user_key_salt),
//     "userData": tunnel_encrypt(derive_key(user_key_bytes, salt, info), private_meta) | null,
//     "recordingType": "mp4"
//   }

use aes_gcm::aead::{Aead, KeyInit};
use aes_gcm::{Aes256Gcm, Nonce};
use base64::Engine;
use hkdf::Hkdf;
use rand::RngCore;
use sha2::Sha256;
use std::time::{SystemTime, UNIX_EPOCH};

/// Derive a 32-byte key from secret bytes using HKDF-SHA256.
/// Matches Python's `derive_key(secret_bytes, salt, info)`.
pub fn derive_key(secret_bytes: &[u8], salt: &[u8], info: &[u8]) -> [u8; 32] {
    let hk = Hkdf::<Sha256>::new(Some(salt), secret_bytes);
    let mut okm = [0u8; 32];
    hk.expand(info, &mut okm).expect("HKDF expand failed");
    okm
}

/// Encrypt data and return base64(nonce + ciphertext + tag).
/// Matches Python's `tunnel_encrypt(AESGCM(key), data)`.
pub fn tunnel_encrypt(key: &[u8; 32], plaintext: &[u8]) -> String {
    let mut nonce_bytes = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut nonce_bytes);

    let cipher = Aes256Gcm::new_from_slice(key).expect("valid 32-byte key");
    let nonce = Nonce::from_slice(&nonce_bytes);
    // encrypt() returns ciphertext + 16-byte GCM tag appended
    let ciphertext = cipher.encrypt(nonce, plaintext).expect("AES-GCM encrypt");

    let mut combined = Vec::with_capacity(12 + ciphertext.len());
    combined.extend_from_slice(&nonce_bytes);
    combined.extend_from_slice(&ciphertext);

    base64::engine::general_purpose::STANDARD.encode(&combined)
}

/// Build the complete `recording_associated` JSON and a fresh `recording_secret`,
/// given the raw Vault record key bytes.
///
/// This performs in Rust exactly what the Python gateway does for guacd recordings.
///
/// Returns `(recording_secret, recording_nonce, recording_associated_bytes)`.
#[allow(clippy::too_many_arguments)]
pub fn build_recording_params(
    resource_key_bytes: &[u8],
    user_key_bytes: Option<&[u8]>,
    conversation_uid: &str,
    resource_uid: &str,
    user_uid: Option<&str>,
    hostname: &str,
    port: &str,
    username: &str,
    recording_type: &str,
) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
    let b64 = base64::engine::general_purpose::STANDARD;

    // Generate fresh random key and nonce for this session's stream encryption
    let mut recording_secret = vec![0u8; 32];
    let mut recording_nonce = vec![0u8; 12];
    rand::thread_rng().fill_bytes(&mut recording_secret);
    rand::thread_rng().fill_bytes(&mut recording_nonce);

    // key_info matches Python: endpoint_name + "_RECORDING-SESSION_AES-GCM-256"
    let key_info = format!("{}_RECORDING-SESSION_AES-GCM-256", conversation_uid);
    let key_info_bytes = key_info.as_bytes();

    let start_time = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();

    // private_meta: contains the recording_secret encrypted for vault key holders
    let private_meta = serde_json::json!({
        "startTime": start_time,
        "userName": username,
        "resourceIp": hostname,
        "resourcePort": port,
        "recordingSecret": b64.encode(&recording_secret),
    });
    let private_meta_bytes = serde_json::to_vec(&private_meta).expect("private_meta serialization");

    // Derive resource key and encrypt private_meta
    let mut resource_key_salt = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut resource_key_salt);
    let resource_key = derive_key(resource_key_bytes, &resource_key_salt, key_info_bytes);
    let resource_data = tunnel_encrypt(&resource_key, &private_meta_bytes);

    // Optionally derive user key and encrypt private_meta
    let (user_key_salt_b64, user_data) = if let Some(ukb) = user_key_bytes {
        let mut salt = [0u8; 12];
        rand::thread_rng().fill_bytes(&mut salt);
        let ukey = derive_key(ukb, &salt, key_info_bytes);
        (
            Some(b64.encode(salt)),
            Some(tunnel_encrypt(&ukey, &private_meta_bytes)),
        )
    } else {
        (None, None)
    };

    // Assemble recording_associated (meta_js) — authenticated as GCM AAD
    let meta_js = serde_json::json!({
        "conversationUid": conversation_uid,
        "resourceUid": resource_uid,
        "resourceKeysSalt": b64.encode(resource_key_salt),
        "resourceData": resource_data,
        "userUid": user_uid,
        "userKeySalt": user_key_salt_b64,
        "userData": user_data,
        "recordingType": recording_type,
    });

    // Sort keys to match Python's json.dumps(..., sort_keys=True)
    let recording_associated =
        serde_json::to_vec(&sort_json_keys(meta_js)).expect("meta_js serialization");

    (recording_secret, recording_nonce, recording_associated)
}

/// Sort a serde_json::Value's object keys recursively.
/// Matches Python's `json.dumps(..., sort_keys=True)`.
fn sort_json_keys(v: serde_json::Value) -> serde_json::Value {
    match v {
        serde_json::Value::Object(map) => {
            let mut sorted: serde_json::Map<String, serde_json::Value> = serde_json::Map::new();
            let mut keys: Vec<String> = map.keys().cloned().collect();
            keys.sort();
            for k in keys {
                let val = map[&k].clone();
                sorted.insert(k, sort_json_keys(val));
            }
            serde_json::Value::Object(sorted)
        }
        other => other,
    }
}
