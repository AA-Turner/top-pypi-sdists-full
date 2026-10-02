//! Port of `software.amazon.kinesis.worker.platform.UrlOpener` (+ the
//! `HttpURLConnection` surface it exposes), as injectable traits for testing the
//! EC2 IMDS calls without real network access.
//!
//! Java uses `java.net.URL`/`HttpURLConnection` directly, with `UrlOpener` as a
//! thin test seam. The Rust port keeps a trait ([`UrlOpener`]) plus a connection
//! trait ([`HttpConnection`]) so the Ec2Resource IMDS interaction is mockable
//! (`mockall`), mirroring the Java Mockito test.

use std::io;

/// A minimal HTTP connection surface (subset of `HttpURLConnection` used by
/// [`Ec2Resource`](crate::worker::platform::Ec2Resource)).
#[cfg_attr(test, mockall::automock)]
pub trait HttpConnection: Send + Sync {
    /// Set the request method (GET/PUT).
    fn set_request_method(&mut self, method: &str);
    /// Set a request header. A `None` value mirrors Java's nullable header value.
    fn set_request_property(&mut self, key: &str, value: Option<String>);
    /// Set the connect timeout in millis.
    fn set_connect_timeout(&mut self, millis: i32);
    /// Set the read timeout in millis.
    fn set_read_timeout(&mut self, millis: i32);
    /// The HTTP response code (may error, mirroring `IOException`).
    fn get_response_code(&mut self) -> io::Result<i32>;
    /// Read the response body as a string.
    fn read_body(&mut self) -> io::Result<String>;
}

/// Opens a connection to a URL. Java `UrlOpener`.
#[cfg_attr(test, mockall::automock)]
pub trait UrlOpener: Send + Sync {
    /// Open a new connection (Java `openConnection`).
    fn open_connection(&self) -> io::Result<Box<dyn HttpConnection>>;
}
