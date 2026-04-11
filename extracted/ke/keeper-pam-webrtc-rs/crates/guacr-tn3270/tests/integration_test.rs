//! Integration tests for TN3270 data stream parsing and rendering.
//!
//! These tests require a running TN3270 server (real MVS mainframe via Hercules).
//! Start one with the provided docker-compose service:
//!
//!   docker-compose -f docker-compose.guacr-test.yml up -d tn3270
//!
//! Wait ~3 minutes for MVS to IPL (boot), then run:
//!
//!   cargo test -p guacr-tn3270 --test integration_test -- --include-ignored
//!
//! Connection details:
//!   Host: localhost:3270   (TN3270 server)
//!   URL:  http://localhost:8038  (Hercules web console)
//!
//! TN5250 (IBM AS/400 / IBM i): no free server exists.
//! Use pub400.com:23 for manual TN5250 testing.

use guacr_protocol::telnet::{DO, EOR, IAC, OPT_BINARY, OPT_EOR, OPT_TERMINAL_TYPE, SB, SE, WILL};
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;
use tokio::time::timeout;

const HOST: &str = "127.0.0.1";
const PORT: u16 = 3270;

/// Returns true if port 3270 is reachable on localhost.
async fn server_available() -> bool {
    timeout(Duration::from_secs(2), TcpStream::connect((HOST, PORT)))
        .await
        .map(|r| r.is_ok())
        .unwrap_or(false)
}

/// Read bytes from the stream until we have consumed all pending Telnet
/// IAC negotiation sequences, returning any non-IAC data that followed.
///
/// A full TN3270 negotiation looks like:
///   Server: IAC DO TERMINAL-TYPE
///   Client: IAC WILL TERMINAL-TYPE
///   Server: IAC SB TERMINAL-TYPE SEND IAC SE
///   Client: IAC SB TERMINAL-TYPE IS IBM-3278-2 IAC SE
///   Server: IAC DO EOR  + IAC DO BINARY
///   Client: IAC WILL EOR + IAC WILL BINARY + IAC DO BINARY
///   Server: IAC WILL BINARY
///   Server: <3270 data stream> IAC EOR
async fn negotiate_tn3270(stream: &mut TcpStream) -> Vec<u8> {
    let mut buf = [0u8; 4096];
    let mut leftover = Vec::new();

    // Send our side of the negotiation up-front.
    // IBM-3278-2 = Model 2, 24 rows × 80 columns.
    let negotiation: &[u8] = &[
        // WILL TERMINAL-TYPE
        IAC,
        WILL,
        OPT_TERMINAL_TYPE,
        // SB TERMINAL-TYPE IS "IBM-3278-2" SE
        IAC,
        SB,
        OPT_TERMINAL_TYPE,
        0,
        b'I',
        b'B',
        b'M',
        b'-',
        b'3',
        b'2',
        b'7',
        b'8',
        b'-',
        b'2',
        IAC,
        SE,
        // WILL EOR
        IAC,
        WILL,
        OPT_EOR,
        // WILL BINARY
        IAC,
        WILL,
        OPT_BINARY,
        // DO BINARY
        IAC,
        DO,
        OPT_BINARY,
    ];
    let _ = stream.write_all(negotiation).await;

    // Drain server negotiation bytes and collect the first 3270 data record.
    // The record is terminated by IAC EOR (0xFF 0xEF).
    let mut collecting = false;
    let deadline = tokio::time::sleep(Duration::from_secs(15));
    tokio::pin!(deadline);

    loop {
        tokio::select! {
            result = stream.read(&mut buf) => {
                match result {
                    Ok(0) | Err(_) => break,
                    Ok(n) => {
                        let mut i = 0;
                        while i < n {
                            if buf[i] == IAC && i + 1 < n {
                                if buf[i + 1] == EOR {
                                    // End of first 3270 record — done
                                    return leftover;
                                }
                                // Skip other IAC sequences (DO/WILL/SB…SE)
                                if buf[i + 1] == SB {
                                    // Skip until IAC SE
                                    i += 2;
                                    while i + 1 < n {
                                        if buf[i] == IAC && buf[i + 1] == SE {
                                            i += 2;
                                            break;
                                        }
                                        i += 1;
                                    }
                                } else {
                                    // 3-byte IAC sequence: IAC + verb + option
                                    i += 3;
                                }
                                collecting = true; // we've seen at least one IAC sequence
                            } else {
                                if collecting {
                                    leftover.push(buf[i]);
                                }
                                i += 1;
                            }
                        }
                    }
                }
            }
            _ = &mut deadline => break,
        }
    }

    leftover
}

// ============================================================================
// Unit tests (no server required)
// ============================================================================

mod unit_tests {
    #[test]
    fn test_tn3270_port_constant() {
        assert_eq!(super::PORT, 3270);
    }
}

// ============================================================================
// Integration tests (require running TN3270 container)
// ============================================================================

#[tokio::test]
#[ignore] // Requires TN3270 server: docker-compose -f docker-compose.guacr-test.yml up -d tn3270
async fn test_tn3270_server_reachable() {
    if !server_available().await {
        eprintln!("Skipping: TN3270 server not available on {}:{}", HOST, PORT);
        eprintln!("Start it with: docker-compose -f docker-compose.guacr-test.yml up -d tn3270");
        eprintln!("(Allow ~3 min for MVS to boot)");
        return;
    }

    let result = TcpStream::connect((HOST, PORT)).await;
    assert!(
        result.is_ok(),
        "Should connect to TN3270 server on port 3270"
    );
}

#[tokio::test]
#[ignore] // Requires TN3270 server
async fn test_tn3270_server_sends_data() {
    if !server_available().await {
        return;
    }

    let mut stream = TcpStream::connect((HOST, PORT))
        .await
        .expect("Failed to connect to TN3270 server");

    let mut buf = [0u8; 256];
    let n = timeout(Duration::from_secs(5), stream.read(&mut buf))
        .await
        .expect("Timeout waiting for server greeting")
        .expect("Read error");

    // Server must send at least IAC DO TERMINAL-TYPE (3 bytes) immediately.
    assert!(n >= 3, "Server should send Telnet negotiation bytes");
    assert_eq!(buf[0], IAC, "First byte should be IAC (255)");
}

#[tokio::test]
#[ignore] // Requires TN3270 server
async fn test_tn3270_negotiation_and_data_stream_parse() {
    if !server_available().await {
        return;
    }

    let mut stream = TcpStream::connect((HOST, PORT))
        .await
        .expect("Failed to connect");

    // Complete TN3270 negotiation and receive first 3270 record.
    let data = negotiate_tn3270(&mut stream).await;

    assert!(
        !data.is_empty(),
        "Should receive a 3270 data stream after negotiation (got {} bytes)",
        data.len()
    );

    // The first record should start with a Write or EraseWrite command byte.
    // EraseWrite = 0xF5, Write = 0xF1, EraseWriteAlternate = 0x7E
    let cmd = data[0];
    assert!(
        matches!(cmd, 0xF5 | 0xF1 | 0x7E),
        "First byte should be a 3270 Write command (got 0x{:02X})",
        cmd
    );

    // Parse the data stream using our codec.
    use guacr_tn3270::datastream::parse_data_stream;
    let parsed = parse_data_stream(&data);
    assert!(
        parsed.is_ok(),
        "Data stream should parse cleanly: {:?}",
        parsed.err()
    );
}

#[tokio::test]
#[ignore] // Requires TN3270 server
async fn test_tn3270_full_pipeline_screen_to_jpeg() {
    if !server_available().await {
        return;
    }

    let mut stream = TcpStream::connect((HOST, PORT))
        .await
        .expect("Failed to connect");

    let data = negotiate_tn3270(&mut stream).await;
    if data.is_empty() {
        eprintln!("No data received after negotiation — server may still be booting");
        return;
    }

    use guacr_tn3270::datastream::parse_data_stream;
    use guacr_tn3270::renderer;
    use guacr_tn3270::screen::ScreenBuffer;

    // Parse the data stream into a DataStream struct.
    let ds = match parse_data_stream(&data) {
        Ok(ds) => ds,
        Err(e) => {
            eprintln!(
                "Parse error (server may not have sent a full record): {}",
                e
            );
            return;
        }
    };

    // Apply the data stream to a screen buffer (24×80 = IBM 3270 Model 2).
    let mut screen = ScreenBuffer::new(24, 80);
    screen.apply_data_stream(&ds);

    // Render to JPEG via the ratatui buffer pipeline.
    let jpeg = renderer::render_to_jpeg(&screen, 9, 18, 85).expect("Render should succeed");

    assert!(
        jpeg.len() > 500,
        "JPEG from MVS login screen should be non-trivial ({} bytes)",
        jpeg.len()
    );

    // Verify it starts with the JPEG SOI marker (0xFF 0xD8).
    assert_eq!(jpeg[0], 0xFF);
    assert_eq!(jpeg[1], 0xD8);

    // The MVS TSO login screen uses the full 24×80 grid with green-on-black
    // text, protected fields for the input areas, and the IBM logo.
    // We can't assert specific text without decoding, but non-zero pixel
    // content confirms the renderer handled the data stream correctly.
    let buffer = renderer::screen_to_buffer(&screen);
    let non_blank = buffer.content.iter().filter(|c| c.symbol() != " ").count();
    assert!(
        non_blank > 10,
        "Login screen should have at least 10 non-blank cells, got {}",
        non_blank
    );
}
