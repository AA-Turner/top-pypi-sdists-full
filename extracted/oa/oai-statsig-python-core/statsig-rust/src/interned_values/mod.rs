pub use interned_store::{InternedStore, MmapSyncCursor, MmapWriteOutcome};

pub mod interned_store;
pub(crate) mod mmap_data_v2;
mod mmap_sync;

#[cfg(test)]
mod __tests__;
