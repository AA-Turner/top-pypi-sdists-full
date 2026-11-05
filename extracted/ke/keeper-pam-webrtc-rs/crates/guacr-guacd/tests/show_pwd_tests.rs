//! `show_pwd` debugging opt-in. Lives in its own test binary (own process) because the flag
//! is process-global and the redaction tests in `src/tests` assert the default.
//!
//! With the flag on, ONLY the client `connect` debug line may carry raw values; guacd error
//! text and returned errors stay credential-free.

use guacr_guacd::client::{
    perform_guacd_handshake, set_show_handshake_values, show_handshake_values,
};
use guacr_guacd::get_protocol_arg_names;
use guacr_protocol::{GuacdInstruction, GuacdParser, PeekError};
use log::{Level, LevelFilter, Log, Metadata, Record};
use std::collections::HashMap;
use std::sync::{Arc, Mutex as StdMutex, Once};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::sync::Mutex;

/// Synthetic value only.
const SECRET: &str = "Sy7hetic-Pa55w0rd-DO-NOT-LOG";

static CAPTURED: StdMutex<Vec<(Level, String)>> = StdMutex::new(Vec::new());
static INIT: Once = Once::new();

struct CaptureLogger;
impl Log for CaptureLogger {
    fn enabled(&self, _: &Metadata) -> bool {
        true
    }
    fn log(&self, r: &Record) {
        CAPTURED
            .lock()
            .unwrap()
            .push((r.level(), format!("{}", r.args())));
    }
    fn flush(&self) {}
}

fn lines_for(conv: &str) -> Vec<String> {
    CAPTURED
        .lock()
        .unwrap()
        .iter()
        .filter(|(_, m)| m.contains(conv))
        .map(|(l, m)| format!("[{l}] {m}"))
        .collect()
}

fn encode(opcode: &str, args: &[String]) -> bytes::Bytes {
    GuacdParser::guacd_encode_instruction(&GuacdInstruction::new(opcode.to_string(), args.to_vec()))
}

async fn read_one<R: AsyncReadExt + Unpin>(reader: &mut R, buf: &mut Vec<u8>) -> String {
    loop {
        let peeked = match GuacdParser::peek_instruction(buf) {
            Ok(i) => Some((i.opcode.to_string(), i.total_length_in_buffer)),
            Err(PeekError::Incomplete) => None,
            Err(e) => panic!("mock guacd parse error: {e:?}"),
        };
        if let Some((op, len)) = peeked {
            buf.drain(..len);
            return op;
        }
        let mut chunk = [0u8; 1024];
        let n = reader.read(&mut chunk).await.unwrap();
        assert_ne!(n, 0, "client closed early");
        buf.extend_from_slice(&chunk[..n]);
    }
}

/// `error_echoing_secret`: guacd answers `connect` with an `error` that echoes the password.
async fn run(conv: &str, error_echoing_secret: bool) -> anyhow::Result<()> {
    INIT.call_once(|| {
        log::set_logger(&CaptureLogger).expect("logger");
        log::set_max_level(LevelFilter::Trace);
    });
    let mut map: HashMap<String, String> = HashMap::new();
    map.insert("protocol".into(), "ssh".into());
    map.insert("hostname".into(), "target-host.example.internal".into());
    map.insert("port".into(), "2222".into());
    map.insert("password".into(), SECRET.into());

    let advertised: Vec<String> = get_protocol_arg_names("ssh")
        .iter()
        .map(|n| n.to_string())
        .collect();
    let (client, server) = tokio::io::duplex(64 * 1024);
    let (mut cr, mut cw) = tokio::io::split(client);
    let server_task = tokio::spawn(async move {
        let (mut sr, mut sw) = tokio::io::split(server);
        let mut buf = Vec::new();
        read_one(&mut sr, &mut buf).await; // select
        let mut args = vec!["VERSION_1_5_0".to_string()];
        args.extend(advertised);
        sw.write_all(&encode("args", &args)).await.unwrap();
        while read_one(&mut sr, &mut buf).await != "connect" {}
        let out = if error_echoing_secret {
            encode("error", &[format!("bad login for {SECRET}"), "519".into()])
        } else {
            encode("ready", &["$mock-id".into()])
        };
        sw.write_all(&out).await.unwrap();
        sw.flush().await.unwrap();
    });
    let r = perform_guacd_handshake(
        &mut cr,
        &mut cw,
        "chan-showpwd",
        conv,
        1,
        Arc::new(Mutex::new(map)),
    )
    .await;
    server_task.await.unwrap();
    r
}

// One test body so the process-global flag is toggled in a fixed order.
#[tokio::test]
async fn show_pwd_scope_is_only_the_connect_debug_line() {
    // Default (flag absent): redacted.
    assert!(!show_handshake_values(), "default must be redacted");
    run("conv-sp-default", false).await.expect("handshake");
    let d = lines_for("conv-sp-default").join("\n");
    assert!(d.contains("conv-sp-default"), "nothing captured:\n{d}");
    assert!(!d.contains(SECRET), "default leaked password:\n{d}");

    // show_pwd = true: password appears in the params debug line only.
    set_show_handshake_values(true);
    run("conv-sp-on", false).await.expect("handshake");
    let on = lines_for("conv-sp-on");
    let params: Vec<_> = on
        .iter()
        .filter(|l| l.contains("Guacd Handshake: params"))
        .collect();
    assert_eq!(params.len(), 1, "{on:?}");
    assert!(
        params[0].starts_with("[DEBUG]") && params[0].contains(SECRET),
        "{}",
        params[0]
    );
    for l in on.iter().filter(|l| !l.contains("Guacd Handshake: params")) {
        assert!(!l.contains(SECRET), "password outside the params line: {l}");
    }

    // show_pwd = true, guacd echoes the password in an error: returned error and every
    // non-params log line stay clean.
    let err = run("conv-sp-err", true).await.expect_err("guacd error");
    assert!(
        !format!("{err:#}").contains(SECRET),
        "error leaked: {err:#}"
    );
    for l in lines_for("conv-sp-err")
        .iter()
        .filter(|l| !l.contains("Guacd Handshake: params"))
    {
        assert!(!l.contains(SECRET), "password in non-params line: {l}");
    }

    // Back to default: redacted again.
    set_show_handshake_values(false);
    run("conv-sp-off", false).await.expect("handshake");
    assert!(!lines_for("conv-sp-off").join("\n").contains(SECRET));
}
