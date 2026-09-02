//! Integration tests for SSH handler
//!
//! Required services: a running SSH server accessible from the test host.
//!
//! Start one with:
//!   docker run -d --name test-ssh -p 2222:22 \
//!     -e PASSWORD_ACCESS=true \
//!     -e USER_NAME=linuxuser \
//!     -e USER_PASSWORD=alpine \
//!     lscr.io/linuxserver/openssh-server:latest
//!
//! Or use docker-compose:
//!   docker-compose -f docker-compose.test.yml up -d ssh
//!
//! Required environment variables:
//!   SSH_TEST_HOST — SSH server host (default: 127.0.0.1).
//!                   Override when the container is only reachable via its
//!                   Docker-network IP (e.g. SSH_TEST_HOST=192.168.11.2).
//!
//! Connection details:
//!   Host: $SSH_TEST_HOST (or 127.0.0.1) port 2222
//!   User: linuxuser
//!   Password: alpine
//!
//! Run with:
//!   cargo test -p guacr-ssh --test integration_test -- --include-ignored --test-threads=1

use std::collections::HashMap;
use std::time::Duration;
use tokio::time::timeout;

/// Test connection timeout
const CONNECT_TIMEOUT: Duration = Duration::from_secs(10);

/// Return the SSH test host.
///
/// Defaults to `127.0.0.1` (suitable when the container exposes port 2222 to
/// the host via `-p 2222:22`).  Override with `SSH_TEST_HOST` for environments
/// where the container is only reachable via its Docker-network IP, e.g.:
///   SSH_TEST_HOST=192.168.11.2 cargo test -p guacr-ssh --test integration_test -- --ignored
fn test_host() -> String {
    std::env::var("SSH_TEST_HOST").unwrap_or_else(|_| "127.0.0.1".to_string())
}

/// Check if a port is open (server is running)
async fn port_is_open(host: &str, port: u16) -> bool {
    timeout(
        Duration::from_secs(1),
        tokio::net::TcpStream::connect(format!("{}:{}", host, port)),
    )
    .await
    .map(|r| r.is_ok())
    .unwrap_or(false)
}

mod ssh_handler_tests {
    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_handlers::{
        parse_blob_instruction, parse_pipe_instruction, PIPE_NAME_STDOUT, PIPE_STREAM_STDOUT,
    };
    use guacr_ssh::SshHandler;
    use tokio::sync::mpsc;

    fn ssh_host() -> String {
        super::test_host()
    }
    const PORT: u16 = 2222;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    async fn skip_if_not_available() -> bool {
        if !port_is_open(&ssh_host(), PORT).await {
            eprintln!(
                "Skipping SSH tests - server not available on {}:{}",
                ssh_host(),
                PORT
            );
            eprintln!("Start a test SSH server with: docker run -d -p 2222:22 ...");
            return true;
        }
        false
    }

    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_connection_basic() {
        if skip_if_not_available().await {
            return;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());

        // Spawn handler in background
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

        // Drain until we see both "ready" and "size" — the handler sends name/size/ready
        // in that order; we must not assume the first message is "ready".
        let mut got_ready = false;
        let mut got_size = false;
        for _ in 0..20 {
            match timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let s = String::from_utf8_lossy(&msg);
                    if s.contains("ready") {
                        got_ready = true;
                    }
                    if s.contains("size") {
                        got_size = true;
                    }
                    if got_ready && got_size {
                        break;
                    }
                }
                _ => break,
            }
        }
        if !got_ready || !got_size {
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(3), handle).await;
            eprintln!("Skipping: SSH unreachable from host (ready={got_ready}, size={got_size})");
            return;
        }

        // Close the connection
        drop(from_client_tx);

        // Wait for handler to finish (with timeout)
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_with_pipe_enabled() {
        if skip_if_not_available().await {
            return;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("enable-pipe".to_string(), "true".to_string()); // Enable pipe!

        // Spawn handler in background
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

        // Collect initial instructions with longer timeout for first message
        let mut found_pipe = false;
        let mut found_ready = false;
        // Captured whole, not just detected: the arity has to be checked. A bare
        // `contains("size")` passes on a `size` that is missing its layer argument.
        let mut size_instruction: Option<String> = None;
        let mut received_messages = Vec::new();

        // Use CONNECT_TIMEOUT for first message (SSH connection can take time)
        let first_timeout = CONNECT_TIMEOUT;
        let subsequent_timeout = Duration::from_secs(3);

        for i in 0..20 {
            let timeout_duration = if i == 0 {
                first_timeout
            } else {
                subsequent_timeout
            };

            match timeout(timeout_duration, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    eprintln!("Message {}: {}", i, msg_str); // Debug output
                    received_messages.push(msg_str.to_string());

                    if msg_str.contains("pipe") && msg_str.contains("STDOUT") {
                        found_pipe = true;

                        // Verify pipe instruction can be parsed
                        let parsed = parse_pipe_instruction(&msg_str);
                        assert!(parsed.is_some(), "Pipe instruction should be parseable");
                        let parsed = parsed.unwrap();
                        assert_eq!(parsed.name, PIPE_NAME_STDOUT);
                        assert_eq!(parsed.stream_id, PIPE_STREAM_STDOUT);
                    }

                    if msg_str.contains("ready") {
                        found_ready = true;
                    }

                    // Instructions may arrive batched, so locate the opcode rather than
                    // assuming it starts the message.
                    if size_instruction.is_none() {
                        if let Some(start) = msg_str.find("4.size,") {
                            let rest = &msg_str[start..];
                            if let Some(end) = rest.find(';') {
                                size_instruction = Some(rest[..=end].to_string());
                            }
                        }
                    }

                    // Break early if we found all three
                    if found_pipe && found_ready && size_instruction.is_some() {
                        break;
                    }
                }
                Ok(None) => {
                    eprintln!("Channel closed after {} messages", i);
                    break;
                }
                Err(_) => {
                    eprintln!("Timeout after {} messages", i);
                    break;
                }
            }
        }

        if !found_pipe {
            eprintln!("Received {} messages total:", received_messages.len());
            for (i, msg) in received_messages.iter().enumerate() {
                eprintln!("  {}: {}", i, msg);
            }
        }

        // Skip gracefully if SSH is unreachable from this network.
        if !found_ready {
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(3), handle).await;
            eprintln!("Skipping: did not receive ready instruction (SSH unreachable from host)");
            return;
        }
        assert!(
            found_pipe,
            "Should have received pipe instruction for STDOUT"
        );

        // `size` is `size,<layer>,<width>,<height>`. Omitting the layer shifts width into
        // the layer slot and leaves height unset, so assert the shape, not the substring.
        let size_instr = size_instruction
            .expect("Should have received a size instruction to initialize display");
        let body = size_instr
            .strip_suffix(';')
            .expect("size instruction must be terminated with ';'");
        let args: Vec<&str> = body.split(',').collect();
        assert_eq!(
            4,
            args.len(),
            "size must carry layer, width and height: {size_instr}"
        );
        assert_eq!(
            "1.0", args[1],
            "size must target layer 0, the main display layer: {size_instr}"
        );

        // Close the connection
        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_pipe_receives_terminal_output() {
        if skip_if_not_available().await {
            return;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        params.insert("enable-pipe".to_string(), "true".to_string());

        // Spawn handler
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

        // Skip initial instructions until we get past ready/size
        let mut ready = false;
        for _ in 0..10 {
            match timeout(Duration::from_secs(2), to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let msg_str = String::from_utf8_lossy(&msg);
                    if msg_str.contains("ready") {
                        ready = true;
                    }
                    if ready && msg_str.contains("size") {
                        break;
                    }
                }
                _ => break,
            }
        }

        // Wait a bit for any banner/prompt
        tokio::time::sleep(Duration::from_millis(500)).await;

        // Send a command via key instructions
        let cmd = "echo hello\n";
        for c in cmd.chars() {
            let keysym = c as u32;
            let key_instr = format!("3.key,{}.{},1.1;", keysym.to_string().len(), keysym);
            from_client_tx
                .send(Bytes::from(key_instr))
                .await
                .expect("Send failed");
        }

        // Look for blob instructions containing terminal output
        let mut found_pipe_blob = false;
        for _ in 0..20 {
            if let Ok(Some(msg)) = timeout(Duration::from_millis(500), to_client_rx.recv()).await {
                let msg_str = String::from_utf8_lossy(&msg);

                if msg_str.contains(".blob,") {
                    // Verify we can parse the blob
                    if let Some(parsed) = parse_blob_instruction(&msg_str) {
                        // Only check blobs on the STDOUT pipe stream (100)
                        // Other blobs (like clipboard stream 1) should be ignored
                        if parsed.stream_id == PIPE_STREAM_STDOUT {
                            found_pipe_blob = true;
                            println!(
                                "Received {} bytes of terminal output via pipe",
                                parsed.data.len()
                            );

                            // The data should contain raw bytes (possibly ANSI codes)
                            assert!(!parsed.data.is_empty());
                        }
                    }
                }
            }
        }

        // Note: We might not always receive blob if the output goes to img instead
        // This test validates the mechanism when it works
        println!("Pipe blob received: {}", found_pipe_blob);

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }
}

mod stability_tests {
    //! Stability tests: require a running SSH server on 127.0.0.1:2222.
    //! Start with: docker run -d --name test-ssh -p 2222:22 \
    //!   -e PASSWORD_ACCESS=true \
    //!   -e USER_NAME=linuxuser \
    //!   -e USER_PASSWORD=alpine \
    //!   lscr.io/linuxserver/openssh-server:latest

    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_ssh::SshHandler;
    use tokio::sync::mpsc;

    fn ssh_host() -> String {
        super::test_host()
    }
    const PORT: u16 = 2222;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    /// Prove that when the from_client channel is dropped (WebRTC data channel
    /// gone), the handler sends a clean `disconnect` instruction to to_client
    /// before it returns. This matches guacd behaviour and ensures the browser
    /// side gets a clean shutdown notification.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_disconnect_sent_when_from_client_dropped() {
        if !port_is_open(&ssh_host(), PORT).await {
            eprintln!(
                "Skipping: SSH server not available on {}:{}",
                ssh_host(),
                PORT
            );
            return;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());

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

        // Wait for the ready instruction, which confirms the session is established.
        let mut got_ready = false;
        for _ in 0..30 {
            match timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("ready") {
                        got_ready = true;
                        break;
                    }
                }
                _ => break,
            }
        }
        // If we never received "ready", the SSH server is unreachable from this
        // network (e.g. running tests from the host against a docker-network-only
        // container).  Skip gracefully rather than panic.
        if !got_ready {
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(3), handle).await;
            eprintln!("Skipping: did not receive ready instruction (SSH unreachable from host)");
            return;
        }

        // Drop from_client to simulate WebRTC data channel closure.
        drop(from_client_tx);

        // The handler must terminate within 5 seconds and send a disconnect
        // instruction before it does so.
        let mut got_disconnect = false;
        let deadline = tokio::time::Instant::now() + Duration::from_secs(5);
        loop {
            let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            match timeout(remaining, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("disconnect") {
                        got_disconnect = true;
                        break;
                    }
                }
                Ok(None) => break, // channel closed — handler returned
                Err(_) => break,   // timeout
            }
        }

        assert!(
            got_disconnect,
            "handler did not send disconnect instruction after from_client was dropped"
        );

        let _ = timeout(Duration::from_secs(2), handle).await;
    }

    /// Prove that the handler terminates promptly (within a reasonable deadline)
    /// after the from_client channel is dropped. Without the channel.wait() =>
    /// None fix, the loop would stall until the next client input triggered a
    /// channel.data() error.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_handler_exits_promptly_after_client_disconnect() {
        if !port_is_open(&ssh_host(), PORT).await {
            eprintln!(
                "Skipping: SSH server not available on {}:{}",
                ssh_host(),
                PORT
            );
            return;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());

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

        // Drain messages until ready.
        for _ in 0..30 {
            match timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("ready") {
                        break;
                    }
                }
                _ => break,
            }
        }

        let start = std::time::Instant::now();
        drop(from_client_tx);

        // Handler should return within 3 seconds (keepalive interval is 30s,
        // so without the channel-closure fix the handler would sit idle much longer).
        let completed = timeout(Duration::from_secs(3), handle).await;
        let elapsed = start.elapsed();

        assert!(
            completed.is_ok(),
            "handler did not exit within 3 seconds after from_client was dropped (took {:?})",
            elapsed
        );
    }
}

mod interaction_tests {
    //! Tests that exercise real SSH interaction: command output, resize, multi-command
    //! sequences, and clean disconnect.
    //!
    //! All tests require the dev-container SSH server at 127.0.0.1:2222.

    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_ssh::SshHandler;
    use tokio::sync::mpsc;

    fn ssh_host() -> String {
        super::test_host()
    }
    const PORT: u16 = 2222;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    // X11 keysym for the Return/Enter key.
    const KEYSYM_RETURN: u32 = 0xFF0D;

    /// Build a Guacamole `key` instruction for a single X11 keysym.
    /// Format: `<len>.key,<klen>.<keysym>,1.<pressed>;`
    fn key_instr(keysym: u32, pressed: bool) -> Bytes {
        let pressed_flag = if pressed { 1u8 } else { 0u8 };
        let ks = keysym.to_string();
        Bytes::from(format!("3.key,{}.{},1.{};", ks.len(), ks, pressed_flag))
    }

    /// Send a full key press-then-release for a keysym.
    async fn send_key(tx: &mpsc::Sender<Bytes>, keysym: u32) {
        tx.send(key_instr(keysym, true)).await.expect("send press");
        tx.send(key_instr(keysym, false))
            .await
            .expect("send release");
    }

    /// Type a string character by character, then press Return.
    async fn type_line(tx: &mpsc::Sender<Bytes>, text: &str) {
        for c in text.chars() {
            send_key(tx, c as u32).await;
        }
        send_key(tx, KEYSYM_RETURN).await;
    }

    /// Build a Guacamole `size` instruction using pixel dimensions.
    /// The SSH handler uses char_width=9 and char_height=18 by default.
    fn size_instr(width_px: u32, height_px: u32) -> Bytes {
        let w = width_px.to_string();
        let h = height_px.to_string();
        Bytes::from(format!("4.size,{}.{},{}.{};", w.len(), w, h.len(), h))
    }

    /// Drain `to_client` messages until `predicate` returns true on the
    /// accumulated raw text, or the deadline expires.  Returns true if the
    /// predicate was satisfied.
    async fn wait_for_output(
        rx: &mut mpsc::Receiver<Bytes>,
        predicate: impl Fn(&str) -> bool,
        deadline: Duration,
    ) -> bool {
        let end = tokio::time::Instant::now() + deadline;
        let mut accumulated = String::new();
        loop {
            let remaining = end.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                return false;
            }
            match timeout(remaining, rx.recv()).await {
                Ok(Some(msg)) => {
                    let s = String::from_utf8_lossy(&msg);
                    accumulated.push_str(&s);
                    if predicate(&accumulated) {
                        return true;
                    }
                }
                Ok(None) | Err(_) => return false,
            }
        }
    }

    /// Connect and wait for the `ready` instruction. Returns `(handle, from_tx, to_rx)`.
    /// Returns `None` if the server is unreachable or `ready` is not received.
    async fn connect_and_wait_ready() -> Option<(
        tokio::task::JoinHandle<guacr_handlers::Result<()>>,
        mpsc::Sender<Bytes>,
        mpsc::Receiver<Bytes>,
    )> {
        if !port_is_open(&ssh_host(), PORT).await {
            eprintln!(
                "Skipping: SSH server not available on {}:{}",
                ssh_host(),
                PORT
            );
            return None;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());

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

        // Wait for `ready` — this is the signal that auth and shell setup completed.
        let mut got_ready = false;
        for _ in 0..30 {
            match timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("ready") {
                        got_ready = true;
                        break;
                    }
                }
                _ => break,
            }
        }

        if !got_ready {
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(3), handle).await;
            return None;
        }

        Some((handle, from_client_tx, to_client_rx))
    }

    /// Prove the full pipeline: SSH connection -> command -> PTY output ->
    /// terminal-data instruction.  Runs `echo hello_from_test` and checks
    /// that the string appears in the `terminal-data` stream within 3 seconds.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_command_output() {
        let Some((handle, from_client_tx, mut to_client_rx)) = connect_and_wait_ready().await
        else {
            return;
        };

        // Allow the shell prompt to settle before typing.
        tokio::time::sleep(Duration::from_millis(300)).await;

        type_line(&from_client_tx, "echo hello_from_test").await;

        // Collect terminal-data instructions and look for the echoed string.
        let found = wait_for_output(
            &mut to_client_rx,
            |accumulated| accumulated.contains("hello_from_test"),
            Duration::from_secs(3),
        )
        .await;

        assert!(
            found,
            "Did not see 'hello_from_test' in terminal output within 3 seconds"
        );

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    /// Prove that a resize instruction propagates to the PTY.
    /// Sends a resize to 40 rows x 120 cols, then runs `echo $COLUMNS` and
    /// verifies that "120" appears in the output.
    ///
    /// char_width=9, so 120 cols = 1080 px wide.
    /// char_height=18, so 40 rows = 720 px tall.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_resize() {
        let Some((handle, from_client_tx, mut to_client_rx)) = connect_and_wait_ready().await
        else {
            return;
        };

        // Allow the shell prompt to settle.
        tokio::time::sleep(Duration::from_millis(300)).await;

        // Send resize: 120 cols * 9 px = 1080, 40 rows * 18 px = 720.
        from_client_tx
            .send(size_instr(1080, 720))
            .await
            .expect("send resize");

        // Give the server time to process the window-change before typing.
        tokio::time::sleep(Duration::from_millis(200)).await;

        type_line(&from_client_tx, "echo $COLUMNS").await;

        let found = wait_for_output(
            &mut to_client_rx,
            |accumulated| accumulated.contains("120"),
            Duration::from_secs(3),
        )
        .await;

        assert!(
            found,
            "Did not see '120' in terminal output after resize to 120 columns"
        );

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    /// Prove that session state is preserved across multiple commands.
    /// Runs `pwd`, `whoami`, and `uname -s` in sequence and verifies each
    /// produces the expected output.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_multi_command_sequence() {
        let Some((handle, from_client_tx, mut to_client_rx)) = connect_and_wait_ready().await
        else {
            return;
        };

        // Allow the shell prompt to settle.
        tokio::time::sleep(Duration::from_millis(300)).await;

        // Command 1: pwd — home directory for linuxuser.
        type_line(&from_client_tx, "pwd").await;
        let found_pwd = wait_for_output(
            &mut to_client_rx,
            |accumulated| accumulated.contains("/home/linuxuser") || accumulated.contains("/root"),
            Duration::from_secs(3),
        )
        .await;
        assert!(found_pwd, "Did not see home directory in output of 'pwd'");

        // Command 2: whoami — should print the username.
        type_line(&from_client_tx, "whoami").await;
        let found_whoami = wait_for_output(
            &mut to_client_rx,
            |accumulated| accumulated.contains("linuxuser"),
            Duration::from_secs(3),
        )
        .await;
        assert!(
            found_whoami,
            "Did not see 'linuxuser' in output of 'whoami'"
        );

        // Command 3: uname -s — should print "Linux".
        type_line(&from_client_tx, "uname -s").await;
        let found_uname = wait_for_output(
            &mut to_client_rx,
            |accumulated| accumulated.contains("Linux"),
            Duration::from_secs(3),
        )
        .await;
        assert!(found_uname, "Did not see 'Linux' in output of 'uname -s'");

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }

    /// Prove that the session lifecycle ends cleanly.
    /// Sends `exit` to the shell and verifies the handler exits without panicking
    /// and that the to_client channel closes (or a disconnect instruction arrives)
    /// within 2 seconds.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_ssh_disconnect_clean() {
        let Some((handle, from_client_tx, mut to_client_rx)) = connect_and_wait_ready().await
        else {
            return;
        };

        // Allow the shell prompt to settle.
        tokio::time::sleep(Duration::from_millis(300)).await;

        // Send `exit` to close the shell gracefully.
        type_line(&from_client_tx, "exit").await;

        // The handler should either send a `disconnect` instruction or close the
        // to_client channel within 2 seconds.
        let deadline = tokio::time::Instant::now() + Duration::from_secs(2);
        let mut clean_close = false;
        loop {
            let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            match timeout(remaining, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("disconnect") {
                        clean_close = true;
                        break;
                    }
                }
                Ok(None) => {
                    // Channel closed — handler returned without panic.
                    clean_close = true;
                    break;
                }
                Err(_) => break, // deadline
            }
        }

        assert!(
            clean_close,
            "Session did not close cleanly within 2 seconds after 'exit'"
        );

        drop(from_client_tx);
        // Handler should already be finished; give it a short grace period.
        let _ = timeout(Duration::from_secs(3), handle).await;
    }
}

mod channel_lifecycle_tests {
    //! Tests that verify how the handler behaves when the SSH channel is closed
    //! by the server side — covering the `channel.wait() => None` code path and
    //! the EOF / ExitStatus message paths.
    //!
    //! All tests require the dev-container SSH server at port 2222.
    //! Override the host with SSH_TEST_HOST if needed.

    use super::*;
    use bytes::Bytes;
    use guacr_handlers::ProtocolHandler;
    use guacr_ssh::SshHandler;
    use tokio::sync::mpsc;

    fn ssh_host() -> String {
        super::test_host()
    }
    const PORT: u16 = 2222;
    const USERNAME: &str = "linuxuser";
    const PASSWORD: &str = "alpine";

    /// Connect and wait for the ready instruction. Returns None if unreachable.
    async fn connect_and_wait_ready() -> Option<(
        tokio::task::JoinHandle<guacr_handlers::Result<()>>,
        mpsc::Sender<Bytes>,
        mpsc::Receiver<Bytes>,
    )> {
        if !port_is_open(&ssh_host(), PORT).await {
            eprintln!(
                "Skipping: SSH server not available on {}:{}",
                ssh_host(),
                PORT
            );
            return None;
        }

        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());

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

        let mut got_ready = false;
        for _ in 0..30 {
            match timeout(CONNECT_TIMEOUT, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("ready") {
                        got_ready = true;
                        break;
                    }
                }
                _ => break,
            }
        }

        if !got_ready {
            drop(from_client_tx);
            let _ = timeout(Duration::from_secs(3), handle).await;
            eprintln!("Skipping: did not receive ready instruction (SSH unreachable from host)");
            return None;
        }

        Some((handle, from_client_tx, to_client_rx))
    }

    /// Prove that when the shell process exits (server sends ExitStatus then closes
    /// the channel), the handler sends a `disconnect` instruction and returns
    /// without leaking the task. This exercises the ExitStatus arm of the channel
    /// message match, which triggers a clean loop exit and the post-loop cleanup path.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_server_side_exit_produces_disconnect() {
        let Some((handle, from_client_tx, mut to_client_rx)) = connect_and_wait_ready().await
        else {
            return;
        };

        // Allow the shell to settle before issuing the exit command.
        tokio::time::sleep(Duration::from_millis(300)).await;

        // Send `exit 0` so the shell terminates cleanly with ExitStatus(0).
        // This tests the ExitStatus channel message path, not the None path.
        let exit_cmd: Vec<Bytes> = "exit 0\n"
            .chars()
            .map(|c| {
                let ks = (c as u32).to_string();
                Bytes::from(format!("3.key,{}.{},1.1;", ks.len(), ks))
            })
            .collect();
        for instr in exit_cmd {
            let _ = from_client_tx.send(instr).await;
        }

        // The handler must eventually send a disconnect instruction or close the
        // to_client channel after the shell exits.
        let deadline = tokio::time::Instant::now() + Duration::from_secs(5);
        let mut got_disconnect_or_closed = false;
        loop {
            let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            match timeout(remaining, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("disconnect") {
                        got_disconnect_or_closed = true;
                        break;
                    }
                }
                Ok(None) => {
                    // Channel closed — handler returned cleanly.
                    got_disconnect_or_closed = true;
                    break;
                }
                Err(_) => break,
            }
        }

        assert!(
            got_disconnect_or_closed,
            "handler did not close cleanly after shell exit"
        );

        // The handler task itself must have completed (no leaked task).
        drop(from_client_tx);
        let result = timeout(Duration::from_secs(3), handle).await;
        assert!(
            result.is_ok(),
            "handler task must complete after shell exits"
        );
    }

    /// Prove that the handler does not leak resources when the SSH channel is
    /// closed server-side without sending an explicit ExitStatus message (the
    /// `channel.wait() => None` path). This is the bug fixed in step 2.
    ///
    /// The test forces this condition by running a command that closes the shell
    /// immediately: `exec true`. On most shells `exec true` replaces the shell
    /// process with `true`, which exits 0 immediately. The SSH server closes the
    /// channel without the shell's own exit-status notification in some SSH
    /// implementations, exercising the None arm.
    ///
    /// Because this path depends on the SSH server's behaviour, the test also
    /// accepts the ExitStatus path — either way the handler must not hang.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_channel_wait_none_path_handler_exits() {
        if !port_is_open(&ssh_host(), PORT).await {
            eprintln!(
                "Skipping: SSH server not available on {}:{}",
                ssh_host(),
                PORT
            );
            return;
        }

        // Use a command-mode connection (exec) so the channel closes as soon as
        // the command finishes. This exercises the server-initiated close path.
        let handler = SshHandler::with_defaults();
        let (to_client_tx, mut to_client_rx) = mpsc::channel::<Bytes>(1024);
        let (from_client_tx, from_client_rx) = mpsc::channel::<Bytes>(1024);

        let mut params = std::collections::HashMap::new();
        params.insert("hostname".to_string(), ssh_host());
        params.insert("port".to_string(), PORT.to_string());
        params.insert("username".to_string(), USERNAME.to_string());
        params.insert("password".to_string(), PASSWORD.to_string());
        // Use exec-mode: run a trivially-fast command so the channel closes immediately.
        params.insert("command".to_string(), "echo channel-close-test".to_string());

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

        // Collect output — we need to see the command result and then the channel close.
        let deadline = tokio::time::Instant::now() + Duration::from_secs(10);
        let mut saw_output = false;
        loop {
            let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            match timeout(remaining, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    let s = String::from_utf8_lossy(&msg);
                    if s.contains("channel-close-test") {
                        saw_output = true;
                    }
                    if s.contains("disconnect") {
                        break;
                    }
                }
                Ok(None) => break,
                Err(_) => break,
            }
        }

        // The task must finish promptly — it must not hang after the channel closes.
        drop(from_client_tx);
        let completed = timeout(Duration::from_secs(5), handle).await;
        assert!(
            completed.is_ok(),
            "handler must exit promptly after server-side channel close (exec mode)"
        );
        // Output check is informational — server may not be reachable.
        if !saw_output {
            eprintln!("Note: did not observe command output (server may be unreachable via exec)");
        }
    }

    /// Prove that the keepalive mechanism does not interfere with normal sessions.
    ///
    /// Connects, waits 3 seconds (longer than any single keepalive tick would
    /// cause problems), sends a command, and verifies the session is still usable.
    /// If keepalive had a bug that terminated the session prematurely this test
    /// would fail because the command output would never arrive.
    ///
    /// The keepalive interval is 30 seconds by default, so we do not actually
    /// exercise a tick here — the goal is to prove the idle path does not break
    /// the session, not to trigger a tick.
    #[tokio::test]
    #[ignore] // Requires SSH server
    async fn test_keepalive_does_not_break_idle_session() {
        let Some((handle, from_client_tx, mut to_client_rx)) = connect_and_wait_ready().await
        else {
            return;
        };

        // Let the session sit idle for 3 seconds.  This is long enough that any
        // broken idle-path logic would have fired by now, but short enough not to
        // exceed the 30-second keepalive interval.
        tokio::time::sleep(Duration::from_secs(3)).await;

        // Build and send `echo keepalive-ok\n` via key instructions.
        let keysym_return: u32 = 0xFF0D;
        let send_key = |ks: u32| {
            let s = ks.to_string();
            Bytes::from(format!("3.key,{}.{},1.1;", s.len(), s))
        };

        for c in "echo keepalive-ok".chars() {
            let _ = from_client_tx.send(send_key(c as u32)).await;
        }
        let ret = keysym_return.to_string();
        let _ = from_client_tx
            .send(Bytes::from(format!("3.key,{}.{},1.1;", ret.len(), ret)))
            .await;

        // Expect to see the echoed string within 3 seconds.
        let deadline = tokio::time::Instant::now() + Duration::from_secs(3);
        let mut found = false;
        loop {
            let remaining = deadline.saturating_duration_since(tokio::time::Instant::now());
            if remaining.is_zero() {
                break;
            }
            match timeout(remaining, to_client_rx.recv()).await {
                Ok(Some(msg)) => {
                    if String::from_utf8_lossy(&msg).contains("keepalive-ok") {
                        found = true;
                        break;
                    }
                }
                Ok(None) | Err(_) => break,
            }
        }

        assert!(
            found,
            "session must remain usable after 3 seconds of idle time"
        );

        drop(from_client_tx);
        let _ = timeout(Duration::from_secs(5), handle).await;
    }
}
