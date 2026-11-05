//! The guacd `connect` instruction carries the target password. It must never reach a
//! log line or an error string, at any log level - not only when a verbose flag is off.
//!
//! These tests install a real `log::Log` implementation at `Trace` level (the most
//! permissive setting any deployment can reach), drive real client-side handshakes against
//! a mock guacd, and assert on everything the crate actually emitted.

use crate::args::get_protocol_arg_names;
use crate::client::perform_guacd_handshake;
use guacr_protocol::{GuacdInstruction, GuacdParser, PeekError};
use log::{Level, LevelFilter, Log, Metadata, Record};
use std::collections::HashMap;
use std::sync::{Arc, Mutex as StdMutex, Once};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::Mutex;

/// Synthetic values only.
const SECRET: &str = "Sy7hetic-Pa55w0rd-DO-NOT-LOG";
const SECRET_KEY: &str = "SYNTHETIC-PRIVATE-KEY-MATERIAL-0001";
const SECRET_PASSPHRASE: &str = "synthetic-passphrase-0002";
const SECRET_GATEWAY: &str = "synthetic-gateway-pw-0003";
const SECRET_SFTP_KEY: &str = "SYNTHETIC-SFTP-KEY-0004";
const HOST: &str = "target-host.example.internal";
const PORT: &str = "33890";

static CAPTURED: StdMutex<Vec<(Level, String)>> = StdMutex::new(Vec::new());
static INIT: Once = Once::new();

struct CaptureLogger;

impl Log for CaptureLogger {
    fn enabled(&self, _: &Metadata) -> bool {
        true
    }
    fn log(&self, record: &Record) {
        CAPTURED
            .lock()
            .unwrap()
            .push((record.level(), format!("{}", record.args())));
    }
    fn flush(&self) {}
}

fn install_logger() {
    INIT.call_once(|| {
        log::set_logger(&CaptureLogger).expect("test logger already set");
        log::set_max_level(LevelFilter::Trace);
    });
}

/// Log lines that mention `conversation_id`. Tests share one process-wide logger and run
/// in parallel, so each test uses its own conversation id and reads only its own lines.
fn captured_text(conversation_id: &str) -> String {
    CAPTURED
        .lock()
        .unwrap()
        .iter()
        .filter(|(_, msg)| msg.contains(conversation_id))
        .map(|(level, msg)| format!("[{level}] {msg}"))
        .collect::<Vec<_>>()
        .join("\n")
}

fn encode(opcode: &str, args: &[String]) -> bytes::Bytes {
    GuacdParser::guacd_encode_instruction(&GuacdInstruction::new(opcode.to_string(), args.to_vec()))
}

async fn read_one<R: AsyncReadExt + Unpin>(reader: &mut R, buf: &mut Vec<u8>) -> (String, usize) {
    loop {
        let peeked = match GuacdParser::peek_instruction(buf) {
            Ok(i) => Some((i.opcode.to_string(), i.total_length_in_buffer)),
            Err(PeekError::Incomplete) => None,
            Err(e) => panic!("mock guacd parse error: {e:?}"),
        };
        if let Some(out) = peeked {
            buf.drain(..out.1);
            return out;
        }
        let mut chunk = [0u8; 1024];
        let n = reader.read(&mut chunk).await.unwrap();
        assert_ne!(n, 0, "client closed early");
        buf.extend_from_slice(&chunk[..n]);
    }
}

#[derive(Clone, Copy)]
enum Reply {
    /// Complete the handshake normally.
    Ready,
    /// Answer `connect` with a guacd `error` instruction.
    ErrorAfterConnect,
    /// Answer `connect` with a guacd `error` that echoes the password, embeds control
    /// characters and is very long.
    ErrorEchoingSecret,
    /// Answer `select` with the wrong opcode, whose args echo the password.
    WrongOpcodeEchoingSecret,
}

/// Run a handshake for RDP with the synthetic credentials; return the client's result.
async fn run_handshake(reply: Reply, conv: &str, protocol: &str) -> anyhow::Result<()> {
    install_logger();
    let arg_names = get_protocol_arg_names(protocol);
    let mut map: HashMap<String, String> = HashMap::new();
    map.insert("protocol".into(), protocol.into());
    map.insert("hostname".into(), HOST.into());
    map.insert("port".into(), PORT.into());
    map.insert("username".into(), "svc-account".into());
    map.insert("password".into(), SECRET.into());
    // SSH advertises private-key and passphrase; RDP advertises gateway-password and the
    // sftp-* credentials. Offer all of them: guacd only takes the ones it advertises.
    map.insert("private-key".into(), SECRET_KEY.into());
    map.insert("passphrase".into(), SECRET_PASSPHRASE.into());
    map.insert("gateway-password".into(), SECRET_GATEWAY.into());
    map.insert("sftp-private-key".into(), SECRET_SFTP_KEY.into());

    let (client, server) = tokio::io::duplex(64 * 1024);
    let (mut cr, mut cw) = tokio::io::split(client);
    let advertised: Vec<String> = arg_names.iter().map(|n| n.to_string()).collect();

    let server_task = tokio::spawn(async move {
        let (mut sr, mut sw) = tokio::io::split(server);
        let mut buf = Vec::new();
        read_one(&mut sr, &mut buf).await; // select
        if let Reply::WrongOpcodeEchoingSecret = reply {
            sw.write_all(&encode("ready", &[SECRET.to_string()]))
                .await
                .unwrap();
            sw.flush().await.unwrap();
            return;
        }
        let mut args = vec!["VERSION_1_5_0".to_string()];
        args.extend(advertised);
        sw.write_all(&encode("args", &args)).await.unwrap();
        sw.flush().await.unwrap();
        loop {
            let (op, _) = read_one(&mut sr, &mut buf).await;
            if op == "connect" {
                break;
            }
        }
        let out = match reply {
            Reply::ErrorAfterConnect => encode("error", &["Upstream refused".into(), "519".into()]),
            Reply::ErrorEchoingSecret => {
                let long = "x".repeat(2000);
                encode(
                    "error",
                    &[
                        format!("bad login for {SECRET}\x1b[31m\nFORGED [INFO] line {long}"),
                        "519".into(),
                    ],
                )
            }
            _ => encode("ready", &["$mock-id".into()]),
        };
        sw.write_all(&out).await.unwrap();
        sw.flush().await.unwrap();
    });

    let result = perform_guacd_handshake(
        &mut cr,
        &mut cw,
        "chan-redact",
        conv,
        1,
        Arc::new(Mutex::new(map)),
    )
    .await;
    server_task.await.unwrap();
    result
}

#[tokio::test]
async fn successful_handshake_never_logs_password_or_private_key() {
    const C: &str = "conv-ok";
    run_handshake(Reply::Ready, C, "ssh")
        .await
        .expect("handshake");
    run_handshake(Reply::Ready, "conv-ok-rdp", "rdp")
        .await
        .expect("handshake");
    let logs = format!("{}\n{}", captured_text(C), captured_text("conv-ok-rdp"));
    assert!(
        logs.contains(C),
        "logger captured nothing for this handshake:\n{logs}"
    );
    assert!(!logs.contains(SECRET), "password leaked into logs:\n{logs}");
    for leaked in [
        SECRET_KEY,
        SECRET_PASSPHRASE,
        SECRET_GATEWAY,
        SECRET_SFTP_KEY,
    ] {
        assert!(!logs.contains(leaked), "{leaked} leaked into logs:\n{logs}");
    }
}

#[tokio::test]
async fn non_secret_handshake_fields_are_still_logged() {
    const C: &str = "conv-fields";
    run_handshake(Reply::Ready, C, "ssh")
        .await
        .expect("handshake");
    let logs = captured_text(C);
    let params_line = logs
        .lines()
        .find(|l| l.contains(C) && l.contains("Guacd Handshake: params"))
        .unwrap_or_else(|| panic!("no connect summary line:\n{logs}"));
    assert!(
        params_line.contains(&format!("hostname={HOST}")),
        "{params_line}"
    );
    assert!(
        params_line.contains(&format!("port={PORT}")),
        "{params_line}"
    );
    // SSH advertises these, so each assertion can fail if redaction regresses.
    for name in ["password", "private-key", "passphrase"] {
        assert!(
            params_line.contains(&format!("{name}=***")),
            "{params_line}"
        );
    }
    assert!(
        logs.lines()
            .any(|l| l.contains(C) && l.contains("protocol: ssh")),
        "protocol no longer logged:\n{logs}"
    );
}

#[tokio::test]
async fn guacd_error_after_connect_does_not_leak_password() {
    const C: &str = "conv-err";
    let err = run_handshake(Reply::ErrorAfterConnect, C, "rdp")
        .await
        .expect_err("guacd error must fail the handshake");
    let rendered = format!("{err} / {err:?}");
    assert!(rendered.contains("Upstream refused"), "{rendered}");
    let logs = captured_text(C);
    assert!(
        !rendered.contains(SECRET),
        "error leaked password: {rendered}"
    );
    assert!(!logs.contains(SECRET), "password leaked into logs:\n{logs}");
}

#[tokio::test]
async fn unexpected_opcode_error_and_logs_withhold_instruction_args() {
    const C: &str = "conv-opcode";
    let err = run_handshake(Reply::WrongOpcodeEchoingSecret, C, "rdp")
        .await
        .expect_err("wrong opcode must fail the handshake");
    let rendered = format!("{err} / {err:?}");
    assert!(!rendered.contains(SECRET), "error leaked args: {rendered}");
    let logs = captured_text(C);
    assert!(
        logs.contains("Unexpected Guacd opcode"),
        "expected error log missing:\n{logs}"
    );
    assert!(!logs.contains(SECRET), "args leaked into logs:\n{logs}");
}

#[tokio::test]
async fn guacd_error_text_is_scrubbed_stripped_and_bounded() {
    const C: &str = "conv-hardened";
    let err = run_handshake(Reply::ErrorEchoingSecret, C, "rdp")
        .await
        .expect_err("guacd error must fail the handshake");
    let rendered = format!("{err}");
    let logs = captured_text(C);
    for text in [&rendered, &logs] {
        assert!(!text.contains(SECRET), "echoed password survived: {text}");
        assert!(text.contains("bad login for ***"), "{text}");
        assert!(
            !text.contains('\x1b'),
            "control character survived: {text:?}"
        );
        assert!(
            !text.contains("\nFORGED"),
            "newline allowed log forging: {text:?}"
        );
    }
    // 2000 chars sent; at most MAX_PEER_TEXT_CHARS (256) plus the message framing remain.
    assert!(
        rendered.len() < 600,
        "error not bounded: {} bytes",
        rendered.len()
    );
    assert!(rendered.contains("519"), "error code lost: {rendered}");
}

#[test]
fn allowlisted_connect_args_never_look_like_credentials() {
    for name in crate::client::LOGGABLE_CONNECT_ARGS {
        for needle in ["pass", "key", "secret", "token", "cert"] {
            // `ignore-cert` is a boolean flag (no certificate material); everything else
            // must stay clear of credential-looking names.
            if *name == "ignore-cert" {
                continue;
            }
            assert!(
                !name.contains(needle),
                "allowlisted name {name} looks like a credential ({needle})"
            );
        }
    }
}
