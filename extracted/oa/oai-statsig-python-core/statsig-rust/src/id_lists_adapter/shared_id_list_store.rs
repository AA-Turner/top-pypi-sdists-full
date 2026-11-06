use std::collections::{BTreeMap, HashMap, HashSet};
use std::fs::{self, File, OpenOptions};
use std::io::{self, BufReader, BufWriter, Write};
use std::path::{Path, PathBuf};
use std::sync::{Arc, Weak};

use parking_lot::Mutex;
use serde::{Deserialize, Serialize};

use super::shared_id_list_delta::{MappedDelta, write_delta};
use super::shared_id_list_format::{IdListImage, digest, hex, invalid, write_list_with_format};
use super::{IdList, IdListIds, IdListMetadata, IdListPropagationUpdate};

const FORMAT_VERSION: u32 = 2;
const ELIAS_FANO_DIR: &str = "elias-fano-v1";
const MANIFEST: &str = "manifest.json";
const LOCK: &str = "leader.lock";
const TEMP_PREFIX: &str = "tmp-id-list-";

/// Small per-SDK state. Weak references reuse current files without retaining
/// old snapshot generations or owned writer membership sets.
pub(crate) struct SharedIdListStore {
    directory: PathBuf,
    namespace: [u8; 32],
    elias_fano: bool,
    cache: Mutex<HashMap<String, CachedList>>,
}

pub(super) enum ManifestRead {
    Missing,
    Unchanged,
    Changed(same_file::Handle, SharedIdListCatalog),
}

struct CachedList {
    data_file: String,
    delta_file: Option<String>,
    source: Weak<IdListIds>,
    mapped: Weak<IdListIds>,
}

/// The stable lock-file descriptor remains open for the entire leadership term.
/// Dropping the last owner releases the process lock. Never unlink this file.
pub(crate) struct SharedIdListLease {
    _file: File,
    directory: PathBuf,
}

#[derive(Clone, Copy, Default, Serialize, Deserialize)]
pub(super) struct RefreshStatus {
    pub(super) successful_refresh_ms: u64,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub(super) incomplete_since_ms: Option<u64>,
}

#[derive(Clone, Default)]
pub(crate) struct SharedIdListCatalog {
    pub(crate) lists: HashMap<String, IdList>,
    pub(crate) propagation: HashMap<String, IdListPropagationUpdate>,
    pub(crate) generation: String,
    pub(super) content_digest: [u8; 32],
    pub(super) status: RefreshStatus,
}

#[derive(Serialize, Deserialize)]
struct Manifest {
    format_version: u32,
    namespace: String,
    generation: String,
    #[serde(flatten)]
    status: RefreshStatus,
    lists: BTreeMap<String, ManifestList>,
}

#[derive(Serialize, Deserialize)]
struct ManifestList {
    metadata: IdListMetadata,
    data_file: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    delta_file: Option<String>,
    propagation: Option<IdListPropagationUpdate>,
}

impl SharedIdListStore {
    pub(super) fn new(
        root: &Path,
        sdk_key: &str,
        source_fingerprint: &str,
        elias_fano: bool,
    ) -> io::Result<Self> {
        // Anchor relative roots before creating or opening anything under the lease.
        let mut directory = std::path::absolute(root)?;
        // Old clients use the original digest and directory. The separate digest
        // also prevents an image copied between formats from passing validation.
        let identity = if elias_fano {
            directory.push(ELIAS_FANO_DIR);
            serde_json::to_vec(&(ELIAS_FANO_DIR, sdk_key, source_fingerprint))?
        } else {
            serde_json::to_vec(&(sdk_key, source_fingerprint))?
        };
        let namespace = digest(&identity);
        directory.push(hex(&namespace));
        fs::create_dir_all(&directory)?;
        Ok(Self {
            directory,
            namespace,
            elias_fano,
            cache: Mutex::new(HashMap::new()),
        })
    }

    #[cfg(test)]
    pub(crate) fn directory(&self) -> &Path {
        &self.directory
    }

    pub(crate) fn try_acquire_lease(&self) -> io::Result<Option<SharedIdListLease>> {
        let file = OpenOptions::new()
            .create(true)
            .truncate(false)
            .read(true)
            .write(true)
            .open(self.directory.join(LOCK))?;
        match fs4::FileExt::try_lock(&file) {
            Ok(()) => Ok(Some(SharedIdListLease {
                _file: file,
                directory: self.directory.clone(),
            })),
            Err(fs4::TryLockError::WouldBlock) => Ok(None),
            Err(fs4::TryLockError::Error(error)) => Err(error),
        }
    }

    pub(crate) fn load(&self) -> io::Result<Option<SharedIdListCatalog>> {
        self.load_with_hook(|| {})
    }

    fn load_with_hook(&self, hook: impl FnMut()) -> io::Result<Option<SharedIdListCatalog>> {
        match self.load_if_changed(None, hook)? {
            ManifestRead::Changed(_, catalog) => Ok(Some(catalog)),
            ManifestRead::Missing => Ok(None),
            ManifestRead::Unchanged => unreachable!("unconditional catalog read"),
        }
    }

    pub(super) fn load_if_changed(
        &self,
        installed: Option<&same_file::Handle>,
        mut after_manifest: impl FnMut(),
    ) -> io::Result<ManifestRead> {
        let mut last_missing = None;
        for _ in 0..3 {
            let Some(file) = self.open_manifest()? else {
                return Ok(ManifestRead::Missing);
            };
            let handle = same_file::Handle::from_file(file)?;
            if installed == Some(&handle) {
                return Ok(ManifestRead::Unchanged);
            }
            let manifest = self.parse_manifest(handle.as_file())?;
            after_manifest();
            match self.map_catalog(&manifest) {
                Ok(catalog) => {
                    self.remember(&manifest, &catalog, None);
                    return Ok(ManifestRead::Changed(handle, catalog));
                }
                // A publisher may have committed a new catalog and unlinked old
                // files after this reader read the old manifest. Retry current.
                Err(error) if error.kind() == io::ErrorKind::NotFound => last_missing = Some(error),
                Err(error) => return Err(error),
            }
        }
        Err(last_missing.expect("all catalog attempts encountered a missing file"))
    }

    /// Stages complete immutable files, then replaces the manifest atomically.
    /// No error is returned after that commit point. Cleanup is best-effort and
    /// cannot turn an already-visible committed publication into a failure.
    pub(super) fn publish_with_clock(
        &self,
        lease: &SharedIdListLease,
        lists: &HashMap<String, IdList>,
        propagation: &HashMap<String, IdListPropagationUpdate>,
        incomplete: Option<RefreshStatus>,
        clock: impl FnOnce() -> u64,
    ) -> io::Result<SharedIdListCatalog> {
        self.check_lease(lease)?;
        let mut entries = BTreeMap::new();
        for (name, list) in lists {
            if name != &list.metadata.name {
                return Err(invalid("ID-list metadata name does not match catalog key"));
            }
            let reusable = self.cache.lock().get(name).and_then(|cached| {
                let matches = cached
                    .source
                    .upgrade()
                    .is_some_and(|ids| Arc::ptr_eq(&ids, &list.ids))
                    || cached
                        .mapped
                        .upgrade()
                        .is_some_and(|ids| Arc::ptr_eq(&ids, &list.ids));
                (matches
                    && self.directory.join(&cached.data_file).is_file()
                    && cached
                        .delta_file
                        .as_ref()
                        .is_none_or(|file| self.directory.join(file).is_file()))
                .then(|| (cached.data_file.clone(), cached.delta_file.clone()))
            });
            let (data_file, delta_file) = match reusable {
                Some(files) => files,
                None => self.write_images(name, &list.ids)?,
            };
            entries.insert(
                name.clone(),
                ManifestList {
                    metadata: list.metadata.clone(),
                    data_file,
                    delta_file,
                    propagation: propagation.get(name).cloned(),
                },
            );
        }
        let mut manifest = Manifest {
            format_version: FORMAT_VERSION,
            namespace: hex(&self.namespace),
            // Older readers identify each publication using this on-disk UUID.
            generation: uuid::Uuid::new_v4().to_string(),
            status: RefreshStatus::default(),
            lists: entries,
        };
        // Map and check every referenced image before commit, including files
        // reused from an earlier interrupted publication.
        let mut catalog = self.map_catalog(&manifest)?;
        // This measures successful publication health; it is not an origin timestamp.
        let now = clock();
        manifest.status = match incomplete {
            Some(previous) => RefreshStatus {
                incomplete_since_ms: previous.incomplete_since_ms.or(Some(now)),
                ..previous
            },
            None => RefreshStatus {
                successful_refresh_ms: now,
                incomplete_since_ms: None,
            },
        };
        catalog.status = manifest.status;
        let mut temporary = tempfile::Builder::new()
            .prefix(TEMP_PREFIX)
            .tempfile_in(&self.directory)?;
        {
            let mut writer = BufWriter::new(temporary.as_file_mut());
            serde_json::to_writer(&mut writer, &manifest)?;
            writer.flush()?;
        }
        temporary.as_file().sync_all()?;
        temporary
            .persist(self.directory.join(MANIFEST))
            .map_err(|error| error.error)?;
        // No publisher seed is retained: changed-key state dies with the candidate.
        self.remember(&manifest, &catalog, Some(lists));
        let _ = self.cleanup_manifest_files(&manifest);
        Ok(catalog)
    }

    #[cfg(test)]
    pub(crate) fn publish(
        &self,
        lease: &SharedIdListLease,
        lists: &HashMap<String, IdList>,
        propagation: &HashMap<String, IdListPropagationUpdate>,
        successful_refresh_ms: u64,
    ) -> io::Result<SharedIdListCatalog> {
        self.publish_with_clock(lease, lists, propagation, None, || successful_refresh_ms)
    }

    /// Run after taking the leader lease to remove files left by an interrupted
    /// publication. The committed manifest and stable lock inode are preserved.
    pub(crate) fn cleanup(&self, lease: &SharedIdListLease) -> io::Result<()> {
        self.check_lease(lease)?;
        match self.open_manifest()? {
            Some(file) => self.cleanup_manifest_files(&self.parse_manifest(&file)?),
            None => self.cleanup_unreferenced(&HashSet::new()),
        }
    }

    fn check_lease(&self, lease: &SharedIdListLease) -> io::Result<()> {
        if lease.directory != self.directory {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                "ID-list lease belongs to a different namespace",
            ));
        }
        Ok(())
    }

    fn open_manifest(&self) -> io::Result<Option<File>> {
        match File::open(self.directory.join(MANIFEST)) {
            Ok(file) => Ok(Some(file)),
            Err(error) if error.kind() == io::ErrorKind::NotFound => Ok(None),
            Err(error) => Err(error),
        }
    }

    fn parse_manifest(&self, file: &File) -> io::Result<Manifest> {
        let manifest: Manifest = serde_json::from_reader(BufReader::new(file))
            .map_err(|_| invalid("invalid shared ID-list manifest"))?;
        if manifest.format_version != FORMAT_VERSION || manifest.namespace != hex(&self.namespace) {
            return Err(invalid("unsupported shared ID-list manifest or namespace"));
        }
        for (name, entry) in &manifest.lists {
            if name != &entry.metadata.name
                || !valid_data_file(&entry.data_file)
                || entry
                    .delta_file
                    .as_ref()
                    .is_some_and(|file| !valid_data_file(file))
            {
                return Err(invalid("invalid shared ID-list manifest entry"));
            }
        }
        Ok(manifest)
    }

    fn map_catalog(&self, manifest: &Manifest) -> io::Result<SharedIdListCatalog> {
        let mut lists = HashMap::with_capacity(manifest.lists.len());
        let mut propagation = HashMap::new();
        for (name, entry) in &manifest.lists {
            let cached = self
                .cache
                .lock()
                .get(name)
                .filter(|cached| {
                    cached.data_file == entry.data_file && cached.delta_file == entry.delta_file
                })
                .and_then(|cached| cached.mapped.upgrade());
            let ids = match cached {
                // Cached views came from an image validated before its manifest was committed.
                Some(ids) => ids,
                None => {
                    let base = self
                        .cache
                        .lock()
                        .get(name)
                        .filter(|cached| cached.data_file == entry.data_file)
                        .and_then(|cached| cached.mapped.upgrade())
                        .map(|old| old.base_view().map(Arc::clone).unwrap_or(old));
                    let base = match base {
                        Some(base) => base,
                        None => {
                            let path = self.directory.join(&entry.data_file);
                            let view = IdListImage::open(&path, &self.namespace, name)?;
                            if entry.data_file != format!("list-{}.ids", view.content_digest()) {
                                return Err(invalid("shared ID-list content digest mismatch"));
                            }
                            Arc::new(IdListIds::from_image(view))
                        }
                    };
                    match &entry.delta_file {
                        None => base,
                        Some(file) => {
                            let delta = MappedDelta::open(
                                &self.directory.join(file),
                                &self.namespace,
                                name,
                                &entry.data_file,
                            )?;
                            if *file != format!("delta-{}.ids", delta.content_digest()) {
                                return Err(invalid("shared delta content digest mismatch"));
                            }
                            Arc::new(IdListIds::from_overlay(base, delta))
                        }
                    }
                }
            };
            lists.insert(
                name.clone(),
                IdList {
                    metadata: entry.metadata.clone(),
                    ids,
                },
            );
            if let Some(update) = &entry.propagation {
                propagation.insert(name.clone(), update.clone());
            }
        }
        Ok(SharedIdListCatalog {
            lists,
            propagation,
            generation: manifest.generation.clone(),
            // Local installs depend on images, cursors and delivery proof.
            // Freshness and the publication UUID can advance independently.
            content_digest: digest(&serde_json::to_vec(&manifest.lists)?),
            status: manifest.status,
        })
    }

    fn write_images(&self, name: &str, ids: &IdListIds) -> io::Result<(String, Option<String>)> {
        if ids.is_empty() {
            return Ok((self.write_data(name, &IdListIds::new())?, None));
        }
        let Some(pending) = ids.pending() else {
            return Ok((self.write_data(name, ids)?, None));
        };
        if pending.requires_full_base {
            // Pending.iter() is already exact and unique. Feed it to the
            // canonical base writer without a second full owned hash set.
            return Ok((self.write_data(name, ids)?, None));
        }
        let Some(base_file) = pending.base.base_file() else {
            // A private heap base has no published file to attach a delta to.
            return Ok((self.write_data(name, ids)?, None));
        };
        // A caller can republish a retained snapshot whose file was unlinked.
        if !self.directory.join(&base_file).is_file() {
            let rebuilt = self.write_data(name, &pending.base)?;
            if rebuilt != base_file {
                return Err(invalid("reconstructed base identity differs"));
            }
        }
        if pending.changes.len() == 0 {
            return Ok((base_file, None));
        }
        let mut temporary = tempfile::Builder::new()
            .prefix(TEMP_PREFIX)
            .tempfile_in(&self.directory)?;
        let hash = write_delta(
            temporary.as_file_mut(),
            &self.namespace,
            name,
            &base_file,
            pending,
        )?;
        temporary.as_file().sync_all()?;
        let delta_file = format!("delta-{hash}.ids");
        match temporary.persist_noclobber(self.directory.join(&delta_file)) {
            Ok(_) => {}
            Err(error) if error.error.kind() == io::ErrorKind::AlreadyExists => {}
            Err(error) => return Err(error.error),
        }
        Ok((base_file, Some(delta_file)))
    }

    fn write_data(&self, name: &str, ids: &IdListIds) -> io::Result<String> {
        let mut temporary = tempfile::Builder::new()
            .prefix(TEMP_PREFIX)
            .tempfile_in(&self.directory)?;
        let content_digest = write_list_with_format(
            temporary.as_file_mut(),
            &self.namespace,
            name,
            ids,
            self.elias_fano,
        )?;
        temporary.as_file().sync_all()?;
        let filename = format!("list-{content_digest}.ids");
        match temporary.persist_noclobber(self.directory.join(&filename)) {
            Ok(_) => {}
            Err(error) if error.error.kind() == io::ErrorKind::AlreadyExists => {}
            Err(error) => return Err(error.error),
        }
        Ok(filename)
    }

    fn remember(
        &self,
        manifest: &Manifest,
        catalog: &SharedIdListCatalog,
        sources: Option<&HashMap<String, IdList>>,
    ) {
        let mut cache = self.cache.lock();
        cache.retain(|name, _| manifest.lists.contains_key(name));
        for (name, entry) in &manifest.lists {
            let source = sources
                .map(|sources| Arc::downgrade(&sources[name].ids))
                .or_else(|| {
                    cache
                        .get(name)
                        .filter(|old| {
                            old.data_file == entry.data_file && old.delta_file == entry.delta_file
                        })
                        .map(|old| old.source.clone())
                })
                .unwrap_or_default();
            cache.insert(
                name.clone(),
                CachedList {
                    data_file: entry.data_file.clone(),
                    delta_file: entry.delta_file.clone(),
                    source,
                    mapped: Arc::downgrade(&catalog.lists[name].ids),
                },
            );
        }
    }

    fn cleanup_manifest_files(&self, manifest: &Manifest) -> io::Result<()> {
        let referenced = manifest
            .lists
            .values()
            .flat_map(|entry| {
                std::iter::once(entry.data_file.as_str()).chain(entry.delta_file.as_deref())
            })
            .collect();
        self.cleanup_unreferenced(&referenced)
    }

    fn cleanup_unreferenced(&self, referenced: &HashSet<&str>) -> io::Result<()> {
        for entry in fs::read_dir(&self.directory)? {
            let entry = entry?;
            let name = entry.file_name();
            let Some(name) = name.to_str() else {
                continue;
            };
            if (name.starts_with(TEMP_PREFIX) || valid_data_file(name))
                && !referenced.contains(name)
            {
                match fs::remove_file(entry.path()) {
                    Ok(()) => {}
                    Err(error) if error.kind() == io::ErrorKind::NotFound => {}
                    Err(error) => return Err(error),
                }
            }
        }
        Ok(())
    }

    #[cfg(test)]
    pub(super) fn load_after_manifest_for_test(
        &self,
        hook: impl FnMut(),
    ) -> io::Result<Option<SharedIdListCatalog>> {
        self.load_with_hook(hook)
    }
}

fn valid_data_file(name: &str) -> bool {
    name.strip_prefix("list-")
        .or_else(|| name.strip_prefix("delta-"))
        .and_then(|value| value.strip_suffix(".ids"))
        .is_some_and(|value| {
            value.len() == 64
                && value
                    .bytes()
                    .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
        })
}
