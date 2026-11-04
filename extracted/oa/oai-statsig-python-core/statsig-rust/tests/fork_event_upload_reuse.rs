#[cfg(all(unix, not(feature = "custom_network_provider")))]
#[allow(dead_code)]
#[path = "utils/fork_runtime.rs"]
mod fork_runtime;

#[cfg(all(unix, not(feature = "custom_network_provider")))]
mod probe {
    use crate::fork_runtime::{run_probe, wait_for_child};
    use serde_json::json;
    use statsig_rust::log_event_payload::{LogEventPayload, LogEventRequest};
    use statsig_rust::networking::proxy_config::ProxyConfig;
    use statsig_rust::{StatsigHttpEventLoggingAdapter, StatsigOptions};
    use std::io::{BufRead, BufReader, Read, Write};
    use std::net::{TcpListener, TcpStream};
    use std::panic::{AssertUnwindSafe, catch_unwind};
    use std::time::Duration;

    struct Child(Option<libc::pid_t>);

    impl Child {
        fn spawn(task: impl FnOnce()) -> Self {
            let pid = unsafe { libc::fork() };
            assert!(pid >= 0, "fork failed");
            if pid == 0 {
                unsafe { libc::alarm(10) };
                let status = i32::from(catch_unwind(AssertUnwindSafe(task)).is_err());
                unsafe { libc::_exit(status) };
            }
            Self(Some(pid))
        }

        fn wait(mut self) {
            wait_for_child(self.0.take().unwrap());
        }
    }

    impl Drop for Child {
        fn drop(&mut self) {
            if let Some(pid) = self.0 {
                unsafe {
                    libc::kill(pid, libc::SIGKILL);
                    libc::waitpid(pid, std::ptr::null_mut(), 0);
                }
            }
        }
    }

    fn respond(stream: &mut TcpStream, expected_key: &str) {
        stream
            .set_read_timeout(Some(Duration::from_secs(5)))
            .unwrap();
        stream
            .set_write_timeout(Some(Duration::from_secs(5)))
            .unwrap();
        let mut reader = BufReader::new(stream);
        let mut content_length = None;
        let mut api_key = None;
        loop {
            let mut line = String::new();
            assert_ne!(reader.read_line(&mut line).unwrap(), 0);
            if line == "\r\n" {
                break;
            }
            if let Some((name, value)) = line.split_once(':') {
                if name.eq_ignore_ascii_case("content-length") {
                    content_length = Some(value.trim().parse::<u64>().unwrap());
                } else if name.eq_ignore_ascii_case("statsig-api-key") {
                    api_key = Some(value.trim().to_owned());
                }
            }
        }
        assert_eq!(api_key.as_deref(), Some(expected_key));
        let content_length = content_length.expect("event upload includes content-length");
        assert_eq!(
            std::io::copy(
                &mut reader.by_ref().take(content_length),
                &mut std::io::sink()
            )
            .unwrap(),
            content_length
        );
        let body = r#"{"success":true}"#;
        write!(
            reader.get_mut(),
            "HTTP/1.1 200 OK\r\nContent-Length: {}\r\nContent-Type: application/json\r\n\r\n{body}",
            body.len()
        )
        .unwrap();
    }

    fn runtime() -> tokio::runtime::Runtime {
        tokio::runtime::Builder::new_current_thread()
            .enable_all()
            .build()
            .unwrap()
    }

    fn upload(runtime: &tokio::runtime::Runtime, key: &str, options: &StatsigOptions) {
        let adapter = StatsigHttpEventLoggingAdapter::new(key, Some(options));
        runtime
            .block_on(adapter.send_events_over_http(&LogEventRequest {
                payload: LogEventPayload {
                    events: json!([{ "eventName": "fork_test" }]),
                    statsig_metadata: json!({}),
                },
                event_count: 1,
                retries: 0,
            }))
            .unwrap();
    }

    pub fn run() {
        run_probe("test_event_upload_uses_a_new_connection_after_fork", || {
            let listener = TcpListener::bind("127.0.0.1:0").unwrap();
            let address = listener.local_addr().unwrap();
            // Start the server in a separate process before creating a runtime, so
            // neither fork inherits a server thread or an active Tokio worker.
            let server = Child::spawn(|| {
                let (mut parent_connection, _) = listener.accept().unwrap();
                respond(&mut parent_connection, "secret-parent");
                // Keep the first socket open while accepting the child's socket.
                let (mut child_connection, _) = listener.accept().unwrap();
                respond(&mut child_connection, "secret-child");
            });
            drop(listener);

            let options = StatsigOptions {
                log_event_url: Some(format!("http://{address}/v1/log_custom_event")),
                log_event_connection_reuse: Some(true),
                disable_disk_access: Some(true),
                // An explicit loopback proxy prevents ambient proxy settings
                // from sending either request outside the test process tree.
                proxy_config: Some(ProxyConfig {
                    proxy_host: Some(address.ip().to_string()),
                    proxy_port: Some(address.port()),
                    proxy_protocol: Some("http".to_owned()),
                    proxy_auth: None,
                    ca_cert_path: None,
                }),
                ..StatsigOptions::default()
            };
            let parent_runtime = runtime();
            upload(&parent_runtime, "secret-parent", &options);
            let child = Child::spawn(|| upload(&runtime(), "secret-child", &options));
            child.wait();
            server.wait();
        });
    }
}

fn main() {
    #[cfg(all(unix, not(feature = "custom_network_provider")))]
    probe::run();
}
