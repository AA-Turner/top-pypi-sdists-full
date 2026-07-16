use std::{fs::File, path::Path, sync::OnceLock};

use ahash::AHashMap;
use fancy_regex::Regex as FancyRegex;
use memmap2::Mmap;
use ouroboros::self_referencing;
use rkyv::{collections::swiss_table::ArchivedHashMap, string::ArchivedString};

use crate::{
    evaluation::rkyv_value::ArchivedRkyvValue,
    interned_values::mmap_data_v2::{
        ArchivedMmapDataV2, ArchivedMmapEvaluatorValue, ArchivedMmapReturnable, ArchivedMmapSpec,
        MmapDataV2,
    },
    specs_response::explicit_params::ExplicitParameters,
    StatsigErr,
};

use super::{ArchivedMmapDataV1, MmapDataV1};

mod materialize;

#[self_referencing]
struct LoadedMmapDataV1 {
    file: File,
    mmap: Mmap,

    #[borrows(mmap)]
    archived: &'this ArchivedMmapDataV1,
}

#[self_referencing]
struct LoadedMmapArchiveV2 {
    file: File,
    mmap: Mmap,

    #[borrows(mmap)]
    archived: &'this ArchivedMmapDataV2,
}

struct LoadedMmapDataV2 {
    archive: LoadedMmapArchiveV2,
    regexes: AHashMap<u64, FancyRegex>,
    explicit_parameters: OnceLock<AHashMap<usize, ExplicitParameters>>,
}

enum LoadedMmapData {
    V1(LoadedMmapDataV1),
    #[cfg_attr(not(test), allow(dead_code))]
    V2(LoadedMmapDataV2),
}

static MMAP_DATA: OnceLock<LoadedMmapData> = OnceLock::new();

pub(super) fn has_v2() -> bool {
    matches!(MMAP_DATA.get(), Some(LoadedMmapData::V2(_)))
}

pub(super) fn preload_v1(path: &Path) -> Result<(), StatsigErr> {
    let file = File::open(path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let mmap =
        unsafe { Mmap::map(&file).map_err(|error| StatsigErr::FileError(error.to_string()))? };

    let loaded = LoadedMmapDataV1TryBuilder {
        file,
        mmap,
        archived_builder: |mmap| rkyv::access::<ArchivedMmapDataV1, rkyv::rancor::Error>(mmap),
    }
    .try_build()
    .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;

    let format_version = loaded.borrow_archived().format_version();
    if format_version != MmapDataV1::FORMAT_VERSION {
        return Err(StatsigErr::SerializationError(format!(
            "Unsupported interned mmap format version {format_version}; expected {}",
            MmapDataV1::FORMAT_VERSION
        )));
    }

    MMAP_DATA
        .set(LoadedMmapData::V1(loaded))
        .map_err(|_| StatsigErr::LockFailure("Failed to set MMAP_DATA".to_string()))
}

#[cfg_attr(not(test), allow(dead_code))]
pub(super) fn preload_v2(path: &Path) -> Result<(), StatsigErr> {
    let file = File::open(path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    preload_v2_file(file)
}

pub(super) fn preload_v2_file(file: File) -> Result<(), StatsigErr> {
    let mmap =
        unsafe { Mmap::map(&file).map_err(|error| StatsigErr::FileError(error.to_string()))? };

    let archive = LoadedMmapArchiveV2TryBuilder {
        file,
        mmap,
        archived_builder: |mmap| rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(mmap),
    }
    .try_build()
    .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;

    let regexes = validate_archive(archive.borrow_archived())?;
    MMAP_DATA
        .set(LoadedMmapData::V2(LoadedMmapDataV2 {
            archive,
            regexes,
            explicit_parameters: OnceLock::new(),
        }))
        .map_err(|_| StatsigErr::LockFailure("Failed to set MMAP_DATA".to_string()))?;
    materialize::initialize_explicit_parameters();
    Ok(())
}

#[cfg(test)]
pub(super) fn validate_v2(path: &Path) -> Result<(), StatsigErr> {
    let file = File::open(path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let mmap =
        unsafe { Mmap::map(&file).map_err(|error| StatsigErr::FileError(error.to_string()))? };
    let archived = rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&mmap)
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;
    validate_archive(archived).map(|_| ())
}

fn validate_archive(data: &ArchivedMmapDataV2) -> Result<AHashMap<u64, FancyRegex>, StatsigErr> {
    let format_version = data.format_version.to_native();
    if format_version != MmapDataV2::FORMAT_VERSION {
        return Err(StatsigErr::SerializationError(format!(
            "Unsupported interned mmap format version {format_version}; expected {}",
            MmapDataV2::FORMAT_VERSION
        )));
    }

    let regexes = validate_and_compile_evaluator_values(data)?;
    validate_spec_references(data)?;
    Ok(regexes)
}

fn validate_and_compile_evaluator_values(
    data: &ArchivedMmapDataV2,
) -> Result<AHashMap<u64, FancyRegex>, StatsigErr> {
    let require_string = |hash: u64, field: &str| {
        data.strings
            .get(&rkyv::primitive::ArchivedU64::from_native(hash))
            .map(|value| value.as_str())
            .ok_or_else(|| {
                StatsigErr::SerializationError(format!(
                    "Interned mmap v2 {field} references missing string hash {hash}"
                ))
            })
    };

    let mut regexes = AHashMap::new();
    for (value_hash, value) in data.evaluator_values.iter() {
        if let Some(hash) = value.string_value.as_ref() {
            require_string(hash.to_native(), "evaluator string")?;
        }
        if let Some(hash) = value.regex_value.as_ref() {
            let hash = hash.to_native();
            let pattern = require_string(hash, "evaluator regex")?;
            if let Ok(regex) = FancyRegex::new(pattern) {
                regexes.insert(value_hash.to_native(), regex);
            }
        }
        if let Some(object) = value.object_value.as_ref() {
            for (key, value) in object.iter() {
                require_string(key.to_native(), "evaluator object key")?;
                require_string(value.to_native(), "evaluator object value")?;
            }
        }
        if let Some(array) = value.array_value.as_ref() {
            for (lowercase, entry) in array.iter() {
                require_string(lowercase.to_native(), "evaluator array key")?;
                require_string(entry.1.to_native(), "evaluator array value")?;
            }
        }
    }

    Ok(regexes)
}

fn validate_spec_references(data: &ArchivedMmapDataV2) -> Result<(), StatsigErr> {
    for (map_name, specs) in [
        ("feature gate", &data.feature_gates),
        ("dynamic config", &data.dynamic_configs),
        ("layer config", &data.layer_configs),
    ] {
        for (name, spec) in specs.iter() {
            require_string(data, name.to_native(), map_name)?;

            for (hash, field) in [
                (spec.spec_type.to_native(), "spec type"),
                (spec.salt.to_native(), "spec salt"),
                (spec.id_type.to_native(), "spec id type"),
                (spec.entity.to_native(), "spec entity"),
            ] {
                require_string(data, hash, field)?;
            }

            if let Some(checksum) = spec.checksum.as_ref() {
                require_string(data, checksum.to_native(), "spec checksum")?;
            }
            validate_returnable_reference(data, &spec.default_value, "spec default value")?;

            for hashes in [
                spec.explicit_parameters.as_ref(),
                spec.target_app_ids.as_ref(),
                spec.fields_used.as_ref(),
            ]
            .into_iter()
            .flatten()
            {
                for hash in hashes.iter() {
                    require_string(data, hash.to_native(), "spec string list")?;
                }
            }

            for rule in spec.rules.iter() {
                for (hash, field) in [
                    (rule.name.to_native(), "rule name"),
                    (rule.id.to_native(), "rule id"),
                    (rule.id_type.value.to_native(), "rule id type"),
                    (
                        rule.id_type.lowercased_value.to_native(),
                        "lowercase rule id type",
                    ),
                ] {
                    require_string(data, hash, field)?;
                }

                for (hash, field) in [
                    (rule.salt.as_ref(), "rule salt"),
                    (rule.group_name.as_ref(), "rule group name"),
                    (rule.config_delegate.as_ref(), "rule config delegate"),
                ] {
                    if let Some(hash) = hash {
                        require_string(data, hash.to_native(), field)?;
                    }
                }

                for condition in rule.conditions.iter() {
                    require_string(data, condition.to_native(), "rule condition")?;
                }
                validate_returnable_reference(data, &rule.return_value, "rule return value")?;
            }
        }
    }

    Ok(())
}

fn require_string(data: &ArchivedMmapDataV2, hash: u64, field: &str) -> Result<(), StatsigErr> {
    let hash = rkyv::primitive::ArchivedU64::from_native(hash);
    if data.strings.get(&hash).is_some() {
        return Ok(());
    }

    Err(StatsigErr::SerializationError(format!(
        "Interned mmap v2 {field} references missing string hash {}",
        hash.to_native()
    )))
}

fn validate_returnable_reference(
    data: &ArchivedMmapDataV2,
    value: &ArchivedMmapReturnable,
    field: &str,
) -> Result<(), StatsigErr> {
    let ArchivedMmapReturnable::Json(hash) = value else {
        return Ok(());
    };
    if data.returnables.get(hash).is_some() {
        return Ok(());
    }

    Err(StatsigErr::SerializationError(format!(
        "Interned mmap v2 {field} references missing returnable hash {}",
        hash.to_native()
    )))
}

pub(super) fn get_string(hash: u64) -> Option<&'static str> {
    let data = MMAP_DATA.get()?;
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    match data {
        LoadedMmapData::V1(data) => data
            .borrow_archived()
            .strings
            .get(&archived_hash)
            .map(|value| value.as_str()),
        LoadedMmapData::V2(data) => data
            .archive
            .borrow_archived()
            .strings
            .get(&archived_hash)
            .map(|value| value.as_str()),
    }
}

pub(super) fn get_returnable(
    hash: u64,
) -> Option<&'static ArchivedHashMap<ArchivedString, ArchivedRkyvValue>> {
    let data = MMAP_DATA.get()?;
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    match data {
        LoadedMmapData::V1(data) => data.borrow_archived().returnables.get(&archived_hash),
        LoadedMmapData::V2(data) => data
            .archive
            .borrow_archived()
            .returnables
            .get(&archived_hash),
    }
}

#[derive(Clone, Copy)]
pub(super) enum MmapSpecKind {
    FeatureGate,
    DynamicConfig,
    LayerConfig,
}

pub(super) fn get_spec(kind: MmapSpecKind, hash: u64) -> Option<&'static ArchivedMmapSpec> {
    let LoadedMmapData::V2(data) = MMAP_DATA.get()? else {
        return None;
    };
    let hash = rkyv::primitive::ArchivedU64::from_native(hash);
    let data = data.archive.borrow_archived();
    match kind {
        MmapSpecKind::FeatureGate => data.feature_gates.get(&hash),
        MmapSpecKind::DynamicConfig => data.dynamic_configs.get(&hash),
        MmapSpecKind::LayerConfig => data.layer_configs.get(&hash),
    }
}

pub(super) fn get_evaluator_value(
    hash: u64,
) -> Option<(
    &'static ArchivedMmapEvaluatorValue,
    Option<&'static FancyRegex>,
)> {
    let LoadedMmapData::V2(data) = MMAP_DATA.get()? else {
        return None;
    };
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    let value = data
        .archive
        .borrow_archived()
        .evaluator_values
        .get(&archived_hash)?;
    Some((value, data.regexes.get(&hash)))
}
