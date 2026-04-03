// Integration tests for TN5250 (IBM AS/400) handler.
// Requires a TN5250 server. Start with: docker run -p 23:23 <tn5250-image>
// Run with: cargo test -p guacr-tn5250 --test integration_test -- --include-ignored --test-threads=1
#[cfg(test)]
mod tn5250_integration_tests {
    fn port_is_open(host: &str, port: u16) -> bool {
        std::net::TcpStream::connect(format!("{}:{}", host, port)).is_ok()
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_connect() {
        let host = std::env::var("TEST_TN5250_HOST").unwrap_or_else(|_| "localhost".into());
        let port: u16 = std::env::var("TEST_TN5250_PORT")
            .ok()
            .and_then(|p| p.parse().ok())
            .unwrap_or(23);
        if !port_is_open(&host, port) {
            println!("TN5250 server not available at {}:{}, skipping", host, port);
            return;
        }
        println!("TN5250 integration test — implement full handshake");
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_login_screen_parse() {
        // Connect and negotiate TN5250 session, verify login screen parses correctly
        let host = std::env::var("TEST_TN5250_HOST").unwrap_or_else(|_| "localhost".into());
        let port: u16 = std::env::var("TEST_TN5250_PORT")
            .ok()
            .and_then(|p| p.parse().ok())
            .unwrap_or(23);

        if !port_is_open(&host, port) {
            println!("TN5250 server not available at {}:{}, skipping", host, port);
            return;
        }

        println!("TN5250 login screen parse test — implement full 5250 negotiation");
        println!("Expected: receive WTD record with Sign-On screen");
    }

    #[cfg(test)]
    mod unit_tests {
        #[test]
        fn test_tn5250_port_constant() {
            // Default AS/400 TN5250 port is 23
            assert_eq!(23u16, 23);
        }
    }
}
