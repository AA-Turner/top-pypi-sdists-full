//! Integration tests for Telnet handler
//!
//! ALL tests in this file require a running Telnet server (Docker). Per testing.md,
//! ALL tests in integration_test.rs must have #[ignore].
//!
//! Start server with:
//!   docker-compose -f docker-compose.test.yml up -d telnet
//!
//! Run tests with:
//!   cargo test --package guacr-telnet --test integration_test -- --include-ignored
//!
//! Connection details:
//!   Host: localhost:2323
//!   User: test_user (or root)
//!   Password: test_password

use std::collections::HashMap;
use std::time::Duration;
use tokio::time::timeout;

/// Test connection timeout
const CONNECT_TIMEOUT: Duration = Duration::from_secs(15);

/// Check if a port is open (server is running)
async fn port_is_open(host: &str, port: u16) -> bool {
    timeout(
        Duration::from_secs(2),
        tokio::net::TcpStream::connect(format!("{}:{}", host, port)),
    )
    .await
    .map(|r| r.is_ok())
    .unwrap_or(false)
}

mod telnet_handler_tests {
    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_telnet::TelnetHandler;
    use tokio::sync::mpsc;

    const HOST: &str = "127.0.0.1";
    const PORT: u16 = 2323;

    async fn skip_if_not_available() -> bool {
        if !port_is_open(HOST, PORT).await {
            eprintln!(
                "Skipping Telnet tests - server not available on {}:{}",
                HOST, PORT
            );
            eprintln!("Start a test Telnet server with: docker-compose -f docker-compose.test.yml up -d telnet");
            return true;
        }
        false
    }

    #[tokio::test]
    #[ignore] // Requires Telnet server
    async fn test_telnet_connection_basic() {
        if skip_if_not_available().await {
            return;
        }

        let handler = TelnetHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        let msg = timeout(CONNECT_TIMEOUT, to_client_rx.recv())
            .await
            .expect("Timeout waiting for ready")
            .expect("Channel closed");

        let msg_str = String::from_utf8_lossy(&msg);
        println!("Telnet: First message: {}", msg_str);

        assert!(
            msg_str.contains("ready") || msg_str.contains("size"),
            "Expected ready or size instruction"
        );

        let mut received_size = false;
        for _ in 0..10 {
            match timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    if msg_str.contains("size") {
                        received_size = true;
                        break;
                    }
                }
                _ => break,
            }
        }

        assert!(received_size, "Should have received size instruction");

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires Telnet server
    async fn test_telnet_with_pipe_enabled() {
        if skip_if_not_available().await {
            return;
        }

        let handler = TelnetHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("enable-pipe".to_string(), "true".to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        let mut found_pipe = false;
        for _ in 0..10 {
            match timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    if msg_str.contains("pipe") && msg_str.contains("STDOUT") {
                        found_pipe = true;
                        break;
                    }
                }
                _ => break,
            }
        }

        assert!(found_pipe, "Should have received STDOUT pipe instruction");

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires Telnet server
    async fn test_telnet_keyboard_input() {
        if skip_if_not_available().await {
            return;
        }

        let handler = TelnetHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), HOST.to_string());
        params.insert("port".to_string(), PORT.to_string());

        let handle = tokio::spawn(async move {
            handler
                .connect(
                    params,
                    to_client_tx,
                    from_client_rx,
                    None,
                    guacr_handlers::SessionHooks::default(),
                )
                .await
        });

        for _ in 0..10 {
            match timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    if msg_str.contains("size") {
                        break;
                    }
                }
                _ => break,
            }
        }

        let cmd = "ls\n";
        for c in cmd.chars() {
            let keysym = c as u32;
            let key_instr = format!("3.key,{}.{},1.1;", keysym.to_string().len(), keysym);
            from_client_tx
                .send(Bytes::from(key_instr))
                .await
                .expect("Send failed");
        }

        tokio::time::sleep(Duration::from_millis(500)).await;

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }
}
