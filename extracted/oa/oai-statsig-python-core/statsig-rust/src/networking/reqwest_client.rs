use std::sync::Arc;

use rustls::pki_types::{CertificateDer, pem::PemObject};

pub(crate) fn new_reqwest_client_builder() -> reqwest::ClientBuilder {
    configured_reqwest_client_builder(None, false).expect("default TLS configuration must be valid")
}

pub(crate) fn configured_reqwest_client_builder(
    ca_cert_pem: Option<&[u8]>,
    http2_only: bool,
) -> Result<reqwest::ClientBuilder, String> {
    let tls = tls_config(ca_cert_pem, http2_only)?;
    let builder = reqwest::Client::builder().tls_backend_preconfigured(tls);
    Ok(if http2_only {
        builder.http2_prior_knowledge()
    } else {
        builder
    })
}

fn root_store(
    ca_cert_pem: Option<&[u8]>,
    require_custom_cert: bool,
) -> Result<rustls::RootCertStore, String> {
    // Some of Mozilla's trust constraints aren't in the DER certificates.
    let mut roots = rustls::RootCertStore {
        roots: webpki_roots::TLS_SERVER_ROOTS.to_vec(),
    };
    if let Some(pem) = ca_cert_pem {
        let initial_len = roots.len();
        for certificate in CertificateDer::pem_slice_iter(pem) {
            let certificate =
                certificate.map_err(|error| format!("Failed to parse CA certificate: {error}"))?;
            roots
                .add(certificate)
                .map_err(|error| format!("Invalid CA certificate: {error}"))?;
        }
        if require_custom_cert && roots.len() == initial_len {
            return Err("HTTP/2 CA configuration contains no certificates".to_string());
        }
    }
    Ok(roots)
}

fn tls_config(
    ca_cert_pem: Option<&[u8]>,
    http2_only: bool,
) -> Result<rustls::ClientConfig, String> {
    let roots = root_store(ca_cert_pem, http2_only)?;
    // Honor the app's crypto provider. Use Reqwest's default if none is set.
    let provider = rustls::crypto::CryptoProvider::get_default()
        .cloned()
        .unwrap_or_else(|| Arc::new(rustls::crypto::aws_lc_rs::default_provider()));
    let mut tls = rustls::ClientConfig::builder_with_provider(provider)
        .with_safe_default_protocol_versions()
        .map_err(|error| format!("Invalid TLS versions: {error}"))?
        .with_root_certificates(roots)
        .with_no_client_auth();
    // Reqwest does not set ALPN on a preconfigured rustls ClientConfig.
    tls.alpn_protocols = if http2_only {
        vec![b"h2".to_vec()]
    } else {
        vec![b"h2".to_vec(), b"http/1.1".to_vec()]
    };
    Ok(tls)
}

#[cfg(test)]
#[path = "__tests__/reqwest_client_tests.rs"]
mod tests;
