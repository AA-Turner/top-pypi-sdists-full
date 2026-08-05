pub use interned_store::{
    InternedStore, MmapArtifactSnapshot, MmapArtifactState, MmapPreloadFailure, MmapPreloadOptions,
    MmapPreloadReport, MmapReaderMemorySnapshot, MmapSyncCursor, MmapWriteOutcome,
};

/// Current full-graph interned mmap format emitted by the SDK writer.
///
/// Readers require this format. Preload reports expose it for telemetry.
pub const INTERNED_MMAP_FORMAT_VERSION: u32 = mmap_data_v2::MmapDataV2::FORMAT_VERSION;

pub mod interned_store;
pub(crate) mod mmap_data_v2;
mod mmap_sync;

#[cfg(test)]
mod __tests__;
