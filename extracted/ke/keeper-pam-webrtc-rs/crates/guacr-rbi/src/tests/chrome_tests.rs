// Chrome integration tests (require Chrome/Chromium installed and the `chrome` feature).
//
// Run with:
//   cargo test -p guacr-rbi --features chrome -- --ignored
//
// Chrome Installation:
//   macOS:   brew install --cask chromium
//   Linux:   apt install chromium-browser
//   Docker:  zenika/alpine-chrome:with-node

#[cfg(feature = "chrome")]
use std::time::Duration;

#[cfg(feature = "chrome")]
use crate::handler::{RbiBackend, RbiConfig, RbiHandler, ResourceLimits};

#[cfg(feature = "chrome")]
use guacr_handlers::ProtocolHandler;

#[cfg(feature = "chrome")]
use std::sync::Mutex;

#[cfg(feature = "chrome")]
static CHROME_TEST_LOCK: Mutex<()> = Mutex::new(());

#[cfg(feature = "chrome")]
fn find_chrome() -> Option<String> {
    let paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/snap/bin/chromium",
    ];

    for path in paths {
        if std::path::Path::new(path).exists() {
            return Some(path.to_string());
        }
    }

    if let Ok(output) = std::process::Command::new("which").arg("chromium").output() {
        if output.status.success() {
            let path = String::from_utf8_lossy(&output.stdout).trim().to_string();
            if !path.is_empty() {
                return Some(path);
            }
        }
    }

    None
}

#[cfg(feature = "chrome")]
fn skip_if_no_chrome() -> bool {
    if find_chrome().is_none() {
        eprintln!("Skipping Chrome test - Chrome/Chromium not found");
        eprintln!("Install with: brew install --cask chromium");
        return true;
    }
    false
}

#[cfg(feature = "chrome")]
#[tokio::test]
#[ignore]
async fn test_chrome_full_session() {
    {
        let _lock = CHROME_TEST_LOCK.lock().unwrap();
        if skip_if_no_chrome() {
            return;
        }
    }

    let chrome_path = find_chrome().unwrap();
    println!("Using Chrome: {}", chrome_path);

    let config = RbiConfig {
        chromium_path: chrome_path,
        backend: RbiBackend::Chrome,
        capture_fps: 15,
        resource_limits: ResourceLimits {
            max_memory_mb: 500,
            max_cpu_percent: 80,
            timeout_seconds: 60,
        },
        ..Default::default()
    };

    let handler = RbiHandler::new(config);
    let (to_client_tx, mut to_client_rx) = tokio::sync::mpsc::channel::<bytes::Bytes>(1024);
    let (from_client_tx, from_client_rx) = tokio::sync::mpsc::channel::<bytes::Bytes>(1024);

    let mut params = std::collections::HashMap::new();
    params.insert("url".to_string(), "https://example.com".to_string());

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
    let mut got_size = false;
    let mut got_image = false;

    for _ in 0..50 {
        match tokio::time::timeout(Duration::from_secs(1), to_client_rx.recv()).await {
            Ok(Some(msg)) => {
                let msg_str = String::from_utf8_lossy(&msg);

                if msg_str.contains("ready") {
                    got_ready = true;
                }
                if msg.len() >= 8 && msg[0] == 0x06 {
                    got_size = true;
                }
                if msg.len() > 100 && (msg[0] == 0x03 || msg.len() > 1000) {
                    got_image = true;
                }

                if got_ready && got_size && got_image {
                    break;
                }
            }
            Ok(None) => break,
            Err(_) => continue,
        }
    }

    assert!(
        got_ready || got_size || got_image,
        "Should receive handshake data"
    );

    drop(from_client_tx);
    let _ = tokio::time::timeout(Duration::from_secs(5), handle).await;
}

#[cfg(feature = "chrome")]
#[tokio::test]
#[ignore]
async fn test_chrome_connection() {
    {
        let _lock = CHROME_TEST_LOCK.lock().unwrap();
        if skip_if_no_chrome() {
            return;
        }
    }

    let chrome_path = find_chrome().unwrap();

    let config = RbiConfig {
        chromium_path: chrome_path,
        backend: RbiBackend::Chrome,
        ..Default::default()
    };

    let handler = RbiHandler::new(config);
    let (to_client_tx, mut to_client_rx) = tokio::sync::mpsc::channel::<bytes::Bytes>(1024);
    let (from_client_tx, from_client_rx) = tokio::sync::mpsc::channel::<bytes::Bytes>(1024);

    let mut params = std::collections::HashMap::new();
    params.insert("url".to_string(), "https://example.com".to_string());

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

    let msg = tokio::time::timeout(Duration::from_secs(30), to_client_rx.recv())
        .await
        .expect("Timeout")
        .expect("Channel closed");

    let msg_str = String::from_utf8_lossy(&msg);
    assert!(
        msg_str.contains("ready") || msg.len() > 100,
        "Expected ready or image data"
    );

    drop(from_client_tx);
    let _ = tokio::time::timeout(Duration::from_secs(10), handle).await;
}

#[cfg(feature = "chrome")]
#[test]
fn test_screencast_mode_enabled() {
    let config_true = RbiConfig {
        use_screencast: Some(true),
        ..RbiConfig::default()
    };
    assert_eq!(config_true.use_screencast, Some(true));
    assert!(config_true.use_screencast.unwrap_or(false));

    let config_false = RbiConfig {
        use_screencast: Some(false),
        ..RbiConfig::default()
    };
    assert_eq!(config_false.use_screencast, Some(false));
    assert!(!config_false.use_screencast.unwrap_or(false));

    let config_none = RbiConfig {
        use_screencast: None,
        ..RbiConfig::default()
    };
    assert_eq!(config_none.use_screencast, None);
    assert!(!config_none.use_screencast.unwrap_or(false));
}

// ---------------------------------------------------------------------------
// SSRF prevention — validate_download_url unit tests
// ---------------------------------------------------------------------------

#[cfg(feature = "chrome")]
use crate::chrome_session::validate_download_url;

#[cfg(feature = "chrome")]
#[test]
fn test_download_url_allows_public_https() {
    assert!(validate_download_url("https://example.com/file.pdf").is_ok());
    assert!(validate_download_url("http://cdn.example.com/data.csv").is_ok());
}

#[cfg(feature = "chrome")]
#[test]
fn test_download_url_blocks_non_http_schemes() {
    assert!(
        validate_download_url("file:///etc/passwd").is_err(),
        "file:// must be blocked"
    );
    assert!(
        validate_download_url("ftp://files.example.com/x").is_err(),
        "ftp:// must be blocked"
    );
    assert!(
        validate_download_url("gopher://evil.com/").is_err(),
        "gopher:// must be blocked"
    );
}

#[cfg(feature = "chrome")]
#[test]
fn test_download_url_blocks_loopback() {
    assert!(validate_download_url("http://127.0.0.1/secret").is_err());
    assert!(validate_download_url("http://127.255.255.255/x").is_err());
    assert!(validate_download_url("http://localhost/admin").is_err());
    assert!(validate_download_url("http://[::1]/v1/creds").is_err());
}

#[cfg(feature = "chrome")]
#[test]
fn test_download_url_blocks_private_ranges() {
    assert!(
        validate_download_url("http://10.0.0.1/internal").is_err(),
        "10.x blocked"
    );
    assert!(
        validate_download_url("http://172.16.0.5/api").is_err(),
        "172.16-31.x blocked"
    );
    assert!(
        validate_download_url("http://192.168.1.1/router").is_err(),
        "192.168.x blocked"
    );
    assert!(
        validate_download_url("http://169.254.169.254/metadata").is_err(),
        "AWS metadata blocked"
    );
}

#[cfg(feature = "chrome")]
use crate::chrome_session::clipboard_write_js;

#[cfg(feature = "chrome")]
#[test]
fn test_clipboard_write_js_escapes_control_and_quotes() {
    let js = clipboard_write_js("a'b\r\nc\"d\\e");
    assert!(!js.contains('\r'), "raw CR must not appear: {js:?}");
    assert!(!js.contains('\n'), "raw LF must not appear: {js:?}");
    assert!(js.starts_with("navigator.clipboard.writeText(\""));
    assert!(js.ends_with("\")"));
    assert!(js.contains("\\r") && js.contains("\\n") && js.contains("\\\""));
}

#[cfg(feature = "chrome")]
#[test]
fn test_clipboard_write_js_cannot_break_out() {
    let js = clipboard_write_js("'); evil(); ('");
    assert_eq!(js.matches("writeText(").count(), 1);
    assert!(
        !js.contains("evil();("),
        "payload must stay inside the string literal"
    );
}

#[cfg(feature = "chrome")]
use crate::chrome_session::format_file_instruction;

#[cfg(feature = "chrome")]
#[test]
fn test_format_file_instruction_uses_codepoint_lengths() {
    let name = "résumé.pdf";
    assert_eq!(name.chars().count(), 10);
    assert_eq!(name.len(), 12);
    let instr = format_file_instruction(1001, "application/pdf", name);
    assert!(
        instr.contains(&format!("{}.{}", name.chars().count(), name)),
        "filename length must be codepoints: {instr}"
    );
    assert!(
        !instr.contains(&format!("12.{name}")),
        "must not use byte length"
    );
    assert!(instr.contains("15.application/pdf"));
    assert!(instr.starts_with("7.file,") && instr.ends_with(';'));
}
