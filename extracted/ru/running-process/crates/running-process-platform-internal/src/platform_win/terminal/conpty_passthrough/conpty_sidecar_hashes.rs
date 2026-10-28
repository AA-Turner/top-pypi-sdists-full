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
pub(super) const EXPECTED_X64: Option<ExpectedAsset> = Some(ExpectedAsset { sha256_hex: "461c114c2bd1259e2f281dddd7e5e35b01282184a260cc0785ca2ebbf467e0dd", size_bytes: 351 });
#[allow(dead_code)]
pub(super) const EXPECTED_ARM64: Option<ExpectedAsset> = Some(ExpectedAsset { sha256_hex: "b73bca50762289f4db61c22f2bc697216176175a7ba7c9e2d94e5b220850d533", size_bytes: 352 });
#[allow(dead_code)]
pub(super) const EXPECTED_X86: Option<ExpectedAsset> = Some(ExpectedAsset { sha256_hex: "23d4270c737c4a5d20cbbeb6451dcda64b6619331871a21b2b6a7b3b5a55c6c4", size_bytes: 353 });
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
