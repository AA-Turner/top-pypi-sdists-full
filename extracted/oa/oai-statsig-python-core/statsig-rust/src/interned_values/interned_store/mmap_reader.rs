#[cfg(test)]
use std::path::Path;
use std::{cell::Cell, fs::File, sync::OnceLock};

use ahash::AHashMap;
use fancy_regex::Regex as FancyRegex;
use memmap2::Mmap;
use ouroboros::self_referencing;
use rkyv::{collections::swiss_table::ArchivedHashMap, string::ArchivedString};

use crate::{
    StatsigErr,
    evaluation::{
        dynamic_returnable::archived_returnable_stable_hash, rkyv_value::ArchivedRkyvValue,
    },
    interned_values::mmap_data_v2::{
        ArchivedMmapDataV2, ArchivedMmapEvaluatorValue, ArchivedMmapReturnable, ArchivedMmapSpec,
        MmapDataV2,
    },
    specs_response::explicit_params::ExplicitParameters,
};

use super::{MmapPreloadOptions, MmapProjectId};

mod materialize;
mod memory;

pub use memory::MmapReaderMemorySnapshot;

#[self_referencing]
struct LoadedMmapArchiveV2 {
    file: File,
    mmap: Mmap,

    #[borrows(mmap)]
    archived: &'this ArchivedMmapDataV2,
}

struct LoadedMmapProject {
    id: MmapProjectId,
    archive: LoadedMmapArchiveV2,
    regexes: AHashMap<u64, FancyRegex>,
}

struct LoadedMmapRegistry {
    projects: Box<[LoadedMmapProject]>,
    returnable_stable_hashes: Option<AHashMap<u64, u64>>,
    explicit_parameters: OnceLock<AHashMap<usize, ExplicitParameters>>,
}

static MMAP_DATA: OnceLock<LoadedMmapRegistry> = OnceLock::new();

#[derive(Clone, Copy)]
enum MmapProjectSelection {
    Unscoped,
    Missing,
    Index(usize),
}

thread_local! {
    static ACTIVE_MMAP_PROJECT: Cell<MmapProjectSelection> =
        const { Cell::new(MmapProjectSelection::Unscoped) };
}

pub(super) struct MmapRegistryBuilder {
    projects: Vec<LoadedMmapProject>,
}

impl MmapRegistryBuilder {
    pub(super) fn new() -> Self {
        Self {
            projects: Vec::new(),
        }
    }

    pub(super) fn add_file(&mut self, id: MmapProjectId, file: File) -> Result<(), StatsigErr> {
        if self
            .projects
            .iter()
            .any(|project| project.id == id || project.id.aliases_artifact(id))
        {
            return Err(StatsigErr::InvalidOperation(format!(
                "Duplicate or colliding interned mmap SDK key identifier {}",
                id.artifact_id()
            )));
        }

        let project = load_v2_file(id, file)?;
        validate_global_leaf_conflicts(&self.projects, &project)?;
        self.projects.push(project);
        Ok(())
    }

    pub(super) fn install(self, options: &MmapPreloadOptions) -> Result<(), StatsigErr> {
        if self.projects.is_empty() {
            return Err(StatsigErr::InvalidOperation(
                "No interned mmap V2 artifacts were loaded".to_string(),
            ));
        }

        let returnable_stable_hashes = options
            .precompute_returnable_stable_hashes
            .then(|| precompute_returnable_stable_hashes(&self.projects));
        MMAP_DATA
            .set(LoadedMmapRegistry {
                projects: self.projects.into_boxed_slice(),
                returnable_stable_hashes,
                explicit_parameters: OnceLock::new(),
            })
            .map_err(|_| StatsigErr::LockFailure("Failed to set MMAP_DATA".to_string()))?;
        materialize::initialize_explicit_parameters();
        Ok(())
    }
}

struct MmapProjectScopeGuard {
    previous: MmapProjectSelection,
}

impl Drop for MmapProjectScopeGuard {
    fn drop(&mut self) {
        ACTIVE_MMAP_PROJECT.with(|active| active.set(self.previous));
    }
}

pub(super) fn has_v2() -> bool {
    MMAP_DATA
        .get()
        .is_some_and(|registry| !registry.projects.is_empty())
}

pub(super) fn is_installed() -> bool {
    MMAP_DATA.get().is_some()
}

pub(super) fn has_project(id: MmapProjectId) -> bool {
    MMAP_DATA
        .get()
        .is_some_and(|registry| registry.projects.iter().any(|project| project.id == id))
}

pub(super) fn memory_snapshot() -> Result<Option<MmapReaderMemorySnapshot>, StatsigErr> {
    let Some(registry) = MMAP_DATA.get() else {
        return Ok(None);
    };

    memory::aggregate(
        registry
            .projects
            .iter()
            .map(|project| (project.archive.borrow_file(), project.archive.borrow_mmap())),
        MmapDataV2::FORMAT_VERSION,
    )
}

pub(super) fn with_project<T>(id: MmapProjectId, callback: impl FnOnce() -> T) -> T {
    let selection = MMAP_DATA
        .get()
        .and_then(|registry| {
            registry
                .projects
                .iter()
                .position(|project| project.id == id)
        })
        .map_or(MmapProjectSelection::Missing, MmapProjectSelection::Index);
    let previous = ACTIVE_MMAP_PROJECT.with(|active| active.replace(selection));
    let _guard = MmapProjectScopeGuard { previous };
    callback()
}
#[cfg(test)]
pub(super) fn preload_v2(path: &Path, options: &MmapPreloadOptions) -> Result<(), StatsigErr> {
    let file = File::open(path).map_err(|error| StatsigErr::FileError(error.to_string()))?;
    let mut builder = MmapRegistryBuilder::new();
    builder.add_file(
        MmapProjectId::for_sdk_key("interned-mmap-test-project"),
        file,
    )?;
    builder.install(options)
}

fn load_v2_file(id: MmapProjectId, file: File) -> Result<LoadedMmapProject, StatsigErr> {
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
    Ok(LoadedMmapProject {
        id,
        archive,
        regexes,
    })
}

fn validate_global_leaf_conflicts(
    loaded: &[LoadedMmapProject],
    candidate: &LoadedMmapProject,
) -> Result<(), StatsigErr> {
    let candidate_data = candidate.archive.borrow_archived();

    for project in loaded {
        let existing_data = project.archive.borrow_archived();

        for (hash, value) in candidate_data.strings.iter() {
            if existing_data
                .strings
                .get(hash)
                .is_some_and(|existing| existing.as_str() != value.as_str())
            {
                return Err(global_leaf_conflict("string", hash.to_native()));
            }
        }

        for (hash, value) in candidate_data.returnables.iter() {
            if existing_data
                .returnables
                .get(hash)
                .is_some_and(|existing| existing != value)
            {
                return Err(global_leaf_conflict("returnable", hash.to_native()));
            }
        }

        for (hash, value) in candidate_data.evaluator_values.iter() {
            if existing_data
                .evaluator_values
                .get(hash)
                .is_some_and(|existing| !evaluator_values_equal(existing, value))
            {
                return Err(global_leaf_conflict("evaluator value", hash.to_native()));
            }
        }
    }

    Ok(())
}

fn precompute_returnable_stable_hashes(projects: &[LoadedMmapProject]) -> AHashMap<u64, u64> {
    let mut hashes = AHashMap::new();
    for project in projects {
        for (hash, value) in project.archive.borrow_archived().returnables.iter() {
            hashes
                .entry(hash.to_native())
                .or_insert_with(|| archived_returnable_stable_hash(value));
        }
    }
    hashes
}

fn global_leaf_conflict(kind: &str, hash: u64) -> StatsigErr {
    StatsigErr::SerializationError(format!(
        "Interned mmap projects contain conflicting {kind} hash {hash}"
    ))
}

fn evaluator_values_equal(
    left: &ArchivedMmapEvaluatorValue,
    right: &ArchivedMmapEvaluatorValue,
) -> bool {
    evaluator_value_types_equal(&left.value_type, &right.value_type)
        && left.bool_value.as_ref().copied() == right.bool_value.as_ref().copied()
        && left.float_value.as_ref().map(|value| value.to_native())
            == right.float_value.as_ref().map(|value| value.to_native())
        && left.string_value.as_ref().map(|value| value.to_native())
            == right.string_value.as_ref().map(|value| value.to_native())
        && left.timestamp_value.as_ref().map(|value| value.to_native())
            == right
                .timestamp_value
                .as_ref()
                .map(|value| value.to_native())
        && left.object_value.as_ref() == right.object_value.as_ref()
        && left.array_value.as_ref() == right.array_value.as_ref()
}

fn evaluator_value_types_equal(
    left: &crate::interned_values::mmap_data_v2::ArchivedMmapEvaluatorValueType,
    right: &crate::interned_values::mmap_data_v2::ArchivedMmapEvaluatorValueType,
) -> bool {
    use crate::interned_values::mmap_data_v2::ArchivedMmapEvaluatorValueType as ValueType;

    matches!(
        (left, right),
        (ValueType::Null, ValueType::Null)
            | (ValueType::Bool, ValueType::Bool)
            | (ValueType::Number, ValueType::Number)
            | (ValueType::String, ValueType::String)
            | (ValueType::Array, ValueType::Array)
            | (ValueType::Object, ValueType::Object)
    )
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
        let string_hash = value.string_value.as_ref().map(|hash| hash.to_native());
        if let Some(hash) = string_hash {
            require_string(hash, "evaluator string")?;
        }
        if let Some(hash) = value.regex_value.as_ref() {
            let hash = hash.to_native();
            if string_hash != Some(hash) {
                return Err(StatsigErr::SerializationError(format!(
                    "Interned mmap v2 evaluator regex hash {hash} does not match its string value"
                )));
            }
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
    let registry = MMAP_DATA.get()?;
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    registry.projects.iter().find_map(|project| {
        project
            .archive
            .borrow_archived()
            .strings
            .get(&archived_hash)
            .map(|value| value.as_str())
    })
}

pub(super) fn get_returnable(
    hash: u64,
) -> Option<&'static ArchivedHashMap<ArchivedString, ArchivedRkyvValue>> {
    let registry = MMAP_DATA.get()?;
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    registry.projects.iter().find_map(|project| {
        project
            .archive
            .borrow_archived()
            .returnables
            .get(&archived_hash)
    })
}

pub(super) fn get_returnable_stable_hash(hash: u64) -> Option<u64> {
    MMAP_DATA
        .get()?
        .returnable_stable_hashes
        .as_ref()?
        .get(&hash)
        .copied()
}

#[derive(Clone, Copy)]
pub(super) enum MmapSpecKind {
    FeatureGate,
    DynamicConfig,
    LayerConfig,
}

pub(super) fn get_spec(kind: MmapSpecKind, hash: u64) -> Option<&'static ArchivedMmapSpec> {
    let registry = MMAP_DATA.get()?;
    let project = active_project(registry)?;
    let hash = rkyv::primitive::ArchivedU64::from_native(hash);
    let data = project.archive.borrow_archived();
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
    let registry = MMAP_DATA.get()?;
    let archived_hash = rkyv::primitive::ArchivedU64::from_native(hash);
    let value = registry.projects.iter().find_map(|project| {
        project
            .archive
            .borrow_archived()
            .evaluator_values
            .get(&archived_hash)
    })?;
    let regex = registry
        .projects
        .iter()
        .find_map(|project| project.regexes.get(&hash));
    Some((value, regex))
}

fn active_project(registry: &'static LoadedMmapRegistry) -> Option<&'static LoadedMmapProject> {
    let selected = ACTIVE_MMAP_PROJECT.with(Cell::get);
    match selected {
        MmapProjectSelection::Index(index) => registry.projects.get(index),
        MmapProjectSelection::Unscoped if registry.projects.len() == 1 => registry.projects.first(),
        MmapProjectSelection::Unscoped | MmapProjectSelection::Missing => None,
    }
}
