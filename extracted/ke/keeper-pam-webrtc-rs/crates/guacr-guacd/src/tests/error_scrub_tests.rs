//! Scrubbing of peer-supplied guacd `error` text must neither corrupt guacd's numeric
//! status code nor leave part of a longer secret behind.

use crate::args::get_protocol_arg_names;
use crate::client::perform_guacd_handshake;
use guacr_protocol::{GuacdInstruction, GuacdParser, PeekError};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::Mutex;

fn encode(opcode: &str, args: &[String]) -> bytes::Bytes {
    GuacdParser::guacd_encode_instruction(&GuacdInstruction::new(opcode.to_string(), args.to_vec()))
}

async fn read_one<R: AsyncReadExt + Unpin>(reader: &mut R, buf: &mut Vec<u8>) -> String {
    loop {
        let peeked = match GuacdParser::peek_instruction(buf) {
            Ok(i) => Some((i.opcode.to_string(), i.total_length_in_buffer)),
            Err(PeekError::Incomplete) => None,
            Err(e) => panic!("mock parse error: {e:?}"),
        };
        if let Some((op, n)) = peeked {
            buf.drain(..n);
            return op;
        }
        let mut chunk = [0u8; 4096];
        let n = reader.read(&mut chunk).await.unwrap();
        assert_ne!(n, 0);
        buf.extend_from_slice(&chunk[..n]);
    }
}

/// SSH handshake with the given extra params; guacd answers `connect` with `error`.
async fn ssh_error(extra: &[(&str, &str)], msg: &str, code: &str) -> String {
    let mut map: HashMap<String, String> = HashMap::new();
    map.insert("protocol".into(), "ssh".into());
    map.insert("hostname".into(), "target-host.example.internal".into());
    map.insert("username".into(), "svc-account".into());
    for (k, v) in extra {
        map.insert((*k).into(), (*v).into());
    }
    let advertised: Vec<String> = get_protocol_arg_names("ssh")
        .iter()
        .map(|n| n.to_string())
        .collect();
    let (msg, code) = (msg.to_string(), code.to_string());
    let (client, server) = tokio::io::duplex(64 * 1024);
    let (mut cr, mut cw) = tokio::io::split(client);
    let srv = tokio::spawn(async move {
        let (mut sr, mut sw) = tokio::io::split(server);
        let mut buf = Vec::new();
        read_one(&mut sr, &mut buf).await; // select
        let mut args = vec!["VERSION_1_5_0".to_string()];
        args.extend(advertised);
        sw.write_all(&encode("args", &args)).await.unwrap();
        while read_one(&mut sr, &mut buf).await != "connect" {}
        sw.write_all(&encode("error", &[msg, code])).await.unwrap();
        sw.flush().await.unwrap();
    });
    let err = perform_guacd_handshake(
        &mut cr,
        &mut cw,
        "chan-scrub",
        "conv-scrub",
        1,
        Arc::new(Mutex::new(map)),
    )
    .await
    .expect_err("guacd error must fail the handshake");
    srv.await.unwrap();
    format!("{err}")
}

/// `font-size=12` is a routine SSH setting; guacd's UPSTREAM_ERROR status is 512.
#[tokio::test]
async fn short_sent_value_does_not_corrupt_status_code() {
    let rendered = ssh_error(&[("font-size", "12")], "Upstream error", "512").await;
    assert!(
        rendered.contains("512"),
        "status code corrupted: {rendered}"
    );
    assert!(
        !rendered.contains("5***"),
        "status code corrupted: {rendered}"
    );
}

/// A non-numeric "status code" is not passed through.
#[tokio::test]
async fn non_numeric_status_code_is_redacted() {
    let rendered = ssh_error(&[], "Upstream error", "Sy7hetic-code").await;
    assert!(!rendered.contains("Sy7hetic-code"), "{rendered}");
    assert!(rendered.contains("***"), "{rendered}");
}

/// `password` is a prefix of `passphrase`; echoing the passphrase must leave nothing behind.
#[tokio::test]
async fn prefix_overlapping_secrets_are_fully_scrubbed() {
    let rendered = ssh_error(
        &[
            ("password", "Synth-Pw-0005"),
            ("passphrase", "Synth-Pw-0005-PASSPHRASE-TAIL"),
        ],
        "bad key Synth-Pw-0005-PASSPHRASE-TAIL rejected",
        "519",
    )
    .await;
    assert!(
        !rendered.contains("PASSPHRASE-TAIL"),
        "tail survived: {rendered}"
    );
    assert!(
        !rendered.contains("Synth-Pw"),
        "secret survived: {rendered}"
    );
    assert!(rendered.contains("519"), "{rendered}");
}

#[test]
fn status_code_and_minimum_length_rules() {
    use crate::client::{sanitize_peer_text, sanitize_status_code};
    for ok in ["1", "512", "9999"] {
        assert_eq!(sanitize_status_code(ok), ok);
    }
    for bad in ["", "12345", "5a2", "-1", "\u{661}"] {
        assert_eq!(sanitize_status_code(bad), "***", "{bad:?}");
    }
    // Short secrets are redacted too: any non-empty credential, any length.
    let secrets = vec![
        "12".to_string(),
        "on".to_string(),
        "abcd-secret".to_string(),
    ];
    assert_eq!(
        sanitize_peer_text("12 on abcd-secret", &secrets),
        "*** *** ***"
    );
}

#[test]
fn short_secret_is_redacted() {
    use crate::client::sanitize_peer_text;
    let out = sanitize_peer_text("auth failed for password abc", &["abc".to_string()]);
    assert!(!out.contains("abc"), "{out}");
    assert_eq!(sanitize_peer_text("x", &["".to_string()]), "x");
}

#[test]
fn control_char_stripping_cannot_recreate_secret() {
    use crate::client::sanitize_peer_text;
    let secrets = vec!["secret".to_string()];
    for text in ["abcd-\nsecret", "sec\x1bret", "se\r\ncret", "s\u{0}e\tcret"] {
        let out = sanitize_peer_text(text, &secrets);
        assert!(!out.contains("secret"), "{text:?} -> {out:?}");
    }
    // A secret that itself contains a control character is still matched.
    let out = sanitize_peer_text("bad pw: ab\ncd", &["ab\ncd".to_string()]);
    assert!(!out.contains("abcd") && !out.contains("ab"), "{out:?}");
    // Bound applies after replacement and the result has no control chars.
    let long = format!("{}secret", "x".repeat(1000));
    let out = sanitize_peer_text(&long, &secrets);
    assert!(out.chars().count() <= 256 && !out.contains("secret"));
}

#[test]
fn connect_summary_escapes_log_injection() {
    use crate::client::redacted_connect_summary;
    let names: Vec<String> = ["VERSION", "hostname", "username"]
        .iter()
        .map(|s| s.to_string())
        .collect();
    let args: Vec<String> = ["1.5.0", "evil\nFAKE LOG LINE \x1b[31m", "u\r\nx"]
        .iter()
        .map(|s| s.to_string())
        .collect();
    let out = redacted_connect_summary(&names, &args);
    assert!(!out.chars().any(|c| c.is_control()), "{out:?}");
    assert!(out.contains("\\n") && out.contains("\\u{1b}"), "{out}");
}
