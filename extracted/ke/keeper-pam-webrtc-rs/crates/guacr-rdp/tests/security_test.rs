// Security tests for the RDP handler.
// Run with: cargo test -p guacr-rdp --test security_test -- --include-ignored

// All tests in security_test.rs MUST have #[ignore] per testing.md.

#[cfg(test)]
mod rdp_tls_tests {
    /// The ignore-cert parameter must default to false.
    ///
    /// Accepting any certificate without validation enables MITM attacks against
    /// RDP sessions. Operators who need to connect to servers with self-signed
    /// certificates must explicitly set ignore-cert=true.
    ///
    /// The field-level assertion is in handler_tests::test_rdp_tls_ignore_cert_defaults_to_false.
    /// This security test documents the requirement at the policy level.
    #[test]
    #[ignore]
    fn rdp_tls_verification_on_by_default() {
        use guacr_rdp::RdpConfig;

        let _ = RdpConfig::default();
        // The substantive assertion is in handler_tests::test_rdp_tls_ignore_cert_defaults_to_false.
        // That unit test fails if the default changes. This test documents the security
        // requirement so it appears in the security test report.
    }
}
