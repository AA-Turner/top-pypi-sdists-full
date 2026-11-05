//! Server side: a malformed `connect` from a client must not put the client's password
//! into the `HandshakeError` (which `GuacdServer` / `run_guacd_server` / the QUIC server
//! log at ERROR) or into a `Debug` rendering of the parsed result.

use crate::server::{ConnectResult, GuacdHandshake};
use std::collections::HashMap;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

/// Non-ASCII synthetic password: 29 chars, 31 bytes.
const SECRET: &str = "P\u{e4}ssw\u{f6}rd-SYNTHETIC-DO-NOT-LOG";

fn enc(s: &str) -> String {
    format!("{}.{}", s.chars().count(), s)
}

/// A client that length-prefixes the password in bytes instead of characters (the case
/// `streaming.rs` has a dedicated hint for) sends `connect`. Returns the server's error.
async fn malformed_connect_error() -> crate::server::HandshakeError {
    let (client, server) = tokio::io::duplex(64 * 1024);
    let srv = tokio::spawn(async move {
        let mut hs = GuacdHandshake::new(server);
        hs.read_select().await.expect("select");
        hs.send_args().await.expect("args");
        hs.read_connect().await
    });
    let (mut cr, mut cw) = tokio::io::split(client);
    cw.write_all(b"6.select,3.rdp;").await.unwrap();
    let mut buf = vec![0u8; 16384];
    let _ = cr.read(&mut buf).await.unwrap();
    let connect = format!(
        "7.connect,{},{},{},{},{}.{},{},{};",
        enc("VERSION_1_5_0"),
        enc("target-host.example.internal"),
        enc("3389"),
        enc("svc-account"),
        SECRET.len(), // byte length: the buggy-client case
        SECRET,
        enc("1024"),
        enc("768"),
    );
    cw.write_all(connect.as_bytes()).await.unwrap();
    cw.flush().await.unwrap();
    srv.await.unwrap().expect_err("malformed connect must fail")
}

#[tokio::test]
async fn malformed_connect_error_does_not_contain_password() {
    let err = malformed_connect_error().await;
    for rendered in [format!("{err}"), format!("{err:?}")] {
        assert!(
            !rendered.contains("SYNTHETIC-DO-NOT-LOG") && !rendered.contains("P\u{e4}ssw"),
            "server handshake error leaked the password: {rendered}"
        );
        assert!(
            rendered.contains("buffer position"),
            "error lost its diagnostic position: {rendered}"
        );
    }
}

#[test]
fn connect_result_debug_hides_values() {
    let mut params = HashMap::new();
    params.insert(
        "hostname".to_string(),
        "target-host.example.internal".to_string(),
    );
    params.insert("password".to_string(), SECRET.to_string());
    let rendered = format!("{:?}", ConnectResult { params });
    assert!(!rendered.contains("SYNTHETIC-DO-NOT-LOG"), "{rendered}");
    assert!(!rendered.contains("target-host"), "{rendered}");
    assert!(
        rendered.contains("password"),
        "names stay visible: {rendered}"
    );
}
