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
            .connect(params, to_client_tx, from_client_rx, None)
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
            .connect(params, to_client_tx, from_client_rx, None)
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
