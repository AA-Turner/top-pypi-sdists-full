//! Compile-time SHA-256 verification table for the Win10 ConPTY sidecar (#447).
//!
//! This generated source is checked in so normal platform builds have no
//! build script, TOML parser, or manifest read. The release workflow derives
//! this file from `conpty-sidecar.sha256.toml` before it builds artifacts; the
//! TOML file is release input, not a compile-time dependency.
//!
//! Pre-release dev checkouts ship with an empty manifest, so every const
//! below is `None` and the runtime falls back to "fetch only, no verify."

#![cfg(windows)]

pub(super) struct ExpectedAsset {
    pub sha256_hex: &'static str,
    pub size_bytes: u64,
}

// This repository checkout intentionally has no released sidecar hashes.
// `ci/render_conpty_sidecar_hashes.py` replaces these constants in the
// release checkout before wheel, binary, and crate builds.

#[allow(dead_code)]
pub(super) const EXPECTED_X64: Option<ExpectedAsset> = Some(ExpectedAsset { sha256_hex: "6848ffee1c5aa6ea59fbf8a3300058ef2af7cb4ca54b1b60eaf0f583e1758398", size_bytes: 353 });
#[allow(dead_code)]
pub(super) const EXPECTED_ARM64: Option<ExpectedAsset> = Some(ExpectedAsset { sha256_hex: "b0db3becfa45578bf0bbad6291edc3d302d05ae5a33495d90ba395eee959d9bf", size_bytes: 353 });
#[allow(dead_code)]
pub(super) const EXPECTED_X86: Option<ExpectedAsset> = Some(ExpectedAsset { sha256_hex: "5015c9642a15d9c19fd8d2828be7851171967e35caa0f6f440678997a0721e85", size_bytes: 352 });
#[allow(dead_code)]
pub(super) const EXPECTED_ARM: Option<ExpectedAsset> = None;

/// Returns the verification baseline for the current build's target arch,
/// if the manifest carried one. `None` means the runtime should fetch
/// without verifying (and log a diagnostic line on opt-in).
pub(super) fn expected_for_current_arch() -> Option<&'static ExpectedAsset> {
    #[cfg(target_arch = "x86_64")]
    {
        EXPECTED_X64.as_ref()
    }
    #[cfg(target_arch = "aarch64")]
    {
        EXPECTED_ARM64.as_ref()
    }
    #[cfg(target_arch = "x86")]
    {
        EXPECTED_X86.as_ref()
    }
    #[cfg(target_arch = "arm")]
    {
        EXPECTED_ARM.as_ref()
    }
    #[cfg(not(any(
        target_arch = "x86_64",
        target_arch = "aarch64",
        target_arch = "x86",
        target_arch = "arm"
    )))]
    {
        None
    }
}
