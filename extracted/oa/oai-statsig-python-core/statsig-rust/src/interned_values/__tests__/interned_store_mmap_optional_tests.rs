use crate::{
    interned_values::{
        InternedStore, MmapPreloadOptions,
        interned_store::{
            MmapProjectId, mmap_manifest_path_for_sdk_key, mmap_v2_path_for_sdk_key,
            write_mmap_manifest_for_test, write_mmap_v2_for_test,
        },
    },
    specs_response::spec_types::SpecsResponseFull,
};
use rusty_fork::rusty_fork_test;
use std::fs;

const SPECS: &str = include_str!("../../../tests/data/eval_proj_dcs.json");

struct Artifact(String);

impl Artifact {
    fn new() -> Self {
        Self(format!("optional-preload-{}", uuid::Uuid::new_v4()))
    }

    fn publish(&self) {
        let path = mmap_v2_path_for_sdk_key(&self.0);
        fs::create_dir_all(path.parent().unwrap()).unwrap();
        write_mmap_v2_for_test(SPECS.as_bytes(), &path).unwrap();
        write_mmap_manifest_for_test(&mmap_manifest_path_for_sdk_key(&self.0), &path).unwrap();
    }
}

impl Drop for Artifact {
    fn drop(&mut self) {
        let _ = fs::remove_file(mmap_manifest_path_for_sdk_key(&self.0));
        let _ = fs::remove_file(mmap_v2_path_for_sdk_key(&self.0));
    }
}

rusty_fork_test! {
    #[test]
    fn optional_mmap_empty_input_is_invalid() {
        assert!(InternedStore::preload_mmap(&[], &[], &MmapPreloadOptions::default()).is_err());
        assert!(InternedStore::mmap_reader_memory_snapshot().unwrap().is_none());
    }

    #[test]
    fn optional_mmap_zero_loaded_allows_retry() {
        let artifact = Artifact::new();
        let options = MmapPreloadOptions::default();
        let report = InternedStore::preload_mmap(&[], &[&artifact.0], &options).unwrap();
        assert_eq!(report.loaded, 0);
        assert_eq!(report.skipped_optional.len(), 1);
        assert_eq!(report.skipped_optional[0].index, 0);
        assert!(InternedStore::mmap_reader_memory_snapshot().unwrap().is_none());
        artifact.publish();
        let report = InternedStore::preload_mmap(&[], &[&artifact.0], &options).unwrap();
        assert_eq!(report.loaded, 1);
        assert!(report.skipped_optional.is_empty());
        assert!(InternedStore::has_preloaded_mmap_project(&artifact.0));
        assert!(InternedStore::preload_mmap(&[], &[&artifact.0], &options).is_err());
    }

    #[test]
    fn optional_mmap_partial_success_preserves_project_scope() {
        let loaded = Artifact::new();
        let missing = Artifact::new();
        loaded.publish();
        let report = InternedStore::preload_mmap(
            &[],
            &[&missing.0, &loaded.0],
            &MmapPreloadOptions { precompute_returnable_stable_hashes: true },
        ).unwrap();
        assert_eq!(report.loaded, 1);
        assert_eq!(report.skipped_optional.len(), 1);
        assert_eq!(report.skipped_optional[0].index, 0);
        for (key, expected_mmap) in [(&loaded.0, true), (&missing.0, false)] {
            let specs: SpecsResponseFull = InternedStore::with_mmap_project(
                MmapProjectId::for_sdk_key(key),
                || serde_json::from_str(SPECS).unwrap(),
            );
            assert!(!specs.feature_gates.0.is_empty());
            assert!(specs.feature_gates.0.values().all(|spec| spec.is_mmap() == expected_mmap));
        }
    }

    #[test]
    fn optional_mmap_required_failure_rolls_back_successful_candidates() {
        let valid = Artifact::new();
        let missing = Artifact::new();
        let optional = Artifact::new();
        valid.publish();
        optional.publish();
        let options = MmapPreloadOptions::default();
        assert!(InternedStore::preload_mmap(&[&valid.0, &missing.0], &[&optional.0], &options).is_err());
        assert!(InternedStore::mmap_reader_memory_snapshot().unwrap().is_none());
        let report = InternedStore::preload_mmap(&[&valid.0], &[&optional.0], &options).unwrap();
        assert_eq!(report.loaded, 2);
        assert!(report.skipped_optional.is_empty());
    }

    #[test]
    fn optional_mmap_skips_invalid_and_duplicate_candidates() {
        let valid = Artifact::new();
        let corrupt = Artifact::new();
        valid.publish();
        let path = mmap_v2_path_for_sdk_key(&corrupt.0);
        fs::write(&path, b"invalid archive").unwrap();
        write_mmap_manifest_for_test(&mmap_manifest_path_for_sdk_key(&corrupt.0), &path).unwrap();
        let report = InternedStore::preload_mmap(
            &[],
            &[&corrupt.0, &valid.0, &valid.0],
            &MmapPreloadOptions::default(),
        ).unwrap();
        assert_eq!(report.loaded, 1);
        let skipped_indexes: Vec<_> = report.skipped_optional.iter().map(|failure| failure.index).collect();
        assert_eq!(skipped_indexes, [0, 2]);
        assert!(report.skipped_optional.iter().all(|failure| !failure.error.is_empty()));
    }
}
