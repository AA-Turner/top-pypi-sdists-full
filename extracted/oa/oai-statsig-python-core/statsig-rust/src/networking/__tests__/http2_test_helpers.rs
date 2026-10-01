use std::future::Future;
use std::time::Duration;

// Re-exec only this test with proxy-free loopback routing. Changing the parent's
// environment would race parallel tests and reqwest's system-proxy cache.
pub(crate) fn without_proxy<F: Future<Output = ()>>(name: &str, body: impl FnOnce() -> F) {
    rusty_fork::fork(
        name,
        rusty_fork::rusty_fork_id!(),
        |command| {
            for key in [
                "HTTP_PROXY",
                "http_proxy",
                "HTTPS_PROXY",
                "https_proxy",
                "ALL_PROXY",
                "all_proxy",
            ] {
                command.env_remove(key);
            }
            command.env("NO_PROXY", "127.0.0.1,localhost,::1");
            command.env("no_proxy", "127.0.0.1,localhost,::1");
        },
        |child, _| {
            let status = child
                .wait_timeout(Duration::from_secs(30))
                .expect("wait for isolated HTTP/2 test")
                .expect("isolated HTTP/2 test exceeded 30 seconds");
            assert!(status.success(), "isolated HTTP/2 test failed: {status}");
        },
        || {
            tokio::runtime::Builder::new_current_thread()
                .enable_all()
                .build()
                .unwrap()
                .block_on(body());
        },
    )
    .expect("fork isolated HTTP/2 test");
}

macro_rules! isolated_http2_test {
    (async fn $name:ident() $body:block) => {
        #[test]
        fn $name() {
            crate::networking::__tests__::http2_test_helpers::without_proxy(
                rusty_fork::rusty_fork_test_name!($name),
                || async $body,
            );
        }
    };
}

pub(crate) use isolated_http2_test;
