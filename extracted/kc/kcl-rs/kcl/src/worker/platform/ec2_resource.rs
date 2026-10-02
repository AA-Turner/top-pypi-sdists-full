//! Port of `software.amazon.kinesis.worker.platform.Ec2Resource`.

use std::sync::Arc;

use crate::worker::platform::{
    ComputePlatform, OperatingRangeDataProvider, ResourceMetadataProvider, UrlOpener,
};

const EC2_INSTANCE_METADATA_TIMEOUT_MILLIS: i32 = 5000;

/// Detects whether the process runs on EC2 by querying the IMDSv2 token +
/// identity-document endpoints. Reports [`OperatingRangeDataProvider::LinuxProc`]
/// when on Linux.
///
/// Mirrors Java: no retries (intentionally absent), broad error catching that
/// returns `false`. Both endpoints go through an injectable [`UrlOpener`] test
/// seam.
///
/// # TODO(port): production `create()`
/// Java's `create()` wires real `UrlOpener`s over `HttpURLConnection`. This port
/// has no HTTP-client dependency, so it exposes only [`Ec2Resource::new`]
/// (inject the openers); production wiring of a real HTTP `UrlOpener` is
/// deferred (coordinator/retrieval wave).
pub struct Ec2Resource {
    identity_document_url: Arc<dyn UrlOpener>,
    token_url: Arc<dyn UrlOpener>,
}

impl Ec2Resource {
    /// Construct with the identity-document and token URL openers (Java
    /// `@VisibleForTesting` ctor).
    pub fn new(identity_document_url: Arc<dyn UrlOpener>, token_url: Arc<dyn UrlOpener>) -> Self {
        Self {
            identity_document_url,
            token_url,
        }
    }

    fn is_ec2(&self) -> bool {
        let result = (|| -> std::io::Result<bool> {
            let mut connection = self.identity_document_url.open_connection()?;
            connection.set_request_method("GET");
            // IMDS v2 requires the token (may be None, mirroring Java's null).
            let token = self.fetch_imds_token();
            connection.set_request_property("X-aws-ec2-metadata-token", token);
            connection.set_connect_timeout(EC2_INSTANCE_METADATA_TIMEOUT_MILLIS);
            connection.set_read_timeout(EC2_INSTANCE_METADATA_TIMEOUT_MILLIS);
            Ok(connection.get_response_code()? == 200)
        })();
        match result {
            Ok(v) => v,
            Err(e) => {
                tracing::error!("Unable to retrieve instance metadata: {}", e);
                false
            }
        }
    }

    fn fetch_imds_token(&self) -> Option<String> {
        let result = (|| -> std::io::Result<Option<String>> {
            let mut connection = self.token_url.open_connection()?;
            connection.set_request_method("PUT");
            connection.set_request_property(
                "X-aws-ec2-metadata-token-ttl-seconds",
                Some("600".to_string()),
            );
            connection.set_connect_timeout(EC2_INSTANCE_METADATA_TIMEOUT_MILLIS);
            connection.set_read_timeout(EC2_INSTANCE_METADATA_TIMEOUT_MILLIS);
            if connection.get_response_code()? == 200 {
                Ok(Some(connection.read_body()?))
            } else {
                Ok(None)
            }
        })();
        match result {
            Ok(v) => v,
            Err(e) => {
                tracing::warn!(
                    "Unable to retrieve IMDS token. It could mean that the instance is not EC2 or is using IMDS V1: {}",
                    e
                );
                None
            }
        }
    }
}

impl ResourceMetadataProvider for Ec2Resource {
    fn is_on_platform(&self) -> bool {
        self.is_ec2()
    }

    fn get_platform(&self) -> ComputePlatform {
        ComputePlatform::Ec2
    }

    fn get_operating_range_data_provider(&self) -> Option<OperatingRangeDataProvider> {
        Some(OperatingRangeDataProvider::LinuxProc).filter(|p| p.is_provider())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::worker::platform::url_opener::HttpConnection as HttpConnectionAlias;
    use crate::worker::platform::url_opener::{MockHttpConnection, MockUrlOpener};
    use std::io;

    fn build(id_code: Option<io::Result<i32>>, token_code: Option<io::Result<i32>>) -> Ec2Resource {
        let mut id_url = MockUrlOpener::new();
        id_url.expect_open_connection().returning(move || {
            let mut c = MockHttpConnection::new();
            c.expect_set_request_method().return_const(());
            c.expect_set_request_property().return_const(());
            c.expect_set_connect_timeout().return_const(());
            c.expect_set_read_timeout().return_const(());
            c.expect_read_body().returning(|| Ok(String::new()));
            match &id_code {
                Some(Ok(code)) => {
                    let code = *code;
                    c.expect_get_response_code().returning(move || Ok(code));
                }
                Some(Err(_)) => {
                    c.expect_get_response_code()
                        .returning(|| Err(io::Error::other("io")));
                }
                None => {
                    c.expect_get_response_code().returning(|| Ok(0));
                }
            }
            Ok(Box::new(c) as Box<dyn HttpConnectionAlias>)
        });

        let mut token_url = MockUrlOpener::new();
        token_url.expect_open_connection().returning(move || {
            let mut c = MockHttpConnection::new();
            c.expect_set_request_method().return_const(());
            c.expect_set_request_property().return_const(());
            c.expect_set_connect_timeout().return_const(());
            c.expect_set_read_timeout().return_const(());
            c.expect_read_body().returning(|| Ok("token".to_string()));
            match &token_code {
                Some(Ok(code)) => {
                    let code = *code;
                    c.expect_get_response_code().returning(move || Ok(code));
                }
                Some(Err(_)) => {
                    c.expect_get_response_code()
                        .returning(|| Err(io::Error::other("io")));
                }
                None => {
                    c.expect_get_response_code().returning(|| Ok(0));
                }
            }
            Ok(Box::new(c) as Box<dyn HttpConnectionAlias>)
        });

        Ec2Resource::new(Arc::new(id_url), Arc::new(token_url))
    }

    #[test]
    fn is_ec2_when_response_code_200() {
        let ec2 = build(Some(Ok(200)), None);
        assert!(ec2.is_on_platform());
        assert_eq!(ec2.get_platform(), ComputePlatform::Ec2);
    }

    #[test]
    fn is_ec2_when_token_connection_throws_because_imds_v1() {
        let ec2 = build(Some(Ok(200)), Some(Err(io::Error::other("io"))));
        assert!(ec2.is_on_platform());
    }

    #[test]
    fn is_not_ec2() {
        let ec2 = build(Some(Ok(403)), None);
        assert!(!ec2.is_on_platform());
    }

    #[test]
    fn is_not_ec2_when_connection_throws() {
        let ec2 = build(Some(Err(io::Error::other("io"))), None);
        assert!(!ec2.is_on_platform());
    }
}
