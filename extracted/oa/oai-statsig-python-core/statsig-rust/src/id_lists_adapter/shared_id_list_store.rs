use crate::id_lists_adapter::shared_id_list_format::{
    IdListImage, digest, hex, invalid, write_list_with_format,
};
use crate::id_lists_adapter::{IdList, IdListEncoding, IdListIds, IdListMetadata};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    fs::{self, File, OpenOptions},
    io::{self, BufReader},
    path::{Path, PathBuf},
    sync::Arc,
};

const FORMAT_VERSION: u32 = 2;
const ELIAS_FANO_DIR: &str = "elias-fano-v1";
const MANIFEST: &str = "manifest.json";
// Pilot workers lock the same file during publication.
const LOCK: &str = "leader.lock";
const TEMP_PREFIX: &str = "tmp-id-list-";

pub(super) struct BaseStore {
    directory: PathBuf,
    namespace: [u8; 32],
    elias_fano: bool,
}

// Keep the single-entry manifest compatible with initial-base-v1 readers.
#[derive(Serialize, Deserialize)]
struct Manifest {
    format_version: u32,
    namespace: String,
    generation: String,
    successful_refresh_ms: u64,
    lists: BTreeMap<String, ManifestList>,
}

#[derive(Serialize, Deserialize)]
struct ManifestList {
    metadata: IdListMetadata,
    data_file: String,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    delta_file: Option<String>,
}

impl BaseStore {
    pub(super) fn new(
        root: &Path,
        source: &str,
        name: &str,
        encoding: IdListEncoding,
    ) -> io::Result<Self> {
        let mut directory = root.to_owned();
        let elias_fano = encoding == IdListEncoding::EliasFano;
        let identity = if elias_fano {
            directory.push(ELIAS_FANO_DIR);
            serde_json::to_vec(&(ELIAS_FANO_DIR, source, name))?
        } else {
            serde_json::to_vec(&(source, name))?
        };
        let namespace = digest(&identity);
        directory.push(hex(&namespace));
        Ok(Self {
            directory,
            namespace,
            elias_fano,
        })
    }

    // Bind the generation and raw byte offset to the image to detect cursor corruption.
    fn image_namespace(&self, metadata: &IdListMetadata) -> io::Result<[u8; 32]> {
        let revision = metadata
            .file_version()
            .membership_revision()
            .ok_or_else(|| invalid("missing initial base revision"))?;
        Ok(Sha256::new()
            .chain_update(self.namespace)
            .chain_update(revision)
            .finalize()
            .into())
    }

    #[cfg(test)]
    pub(super) fn directory(&self) -> &Path {
        &self.directory
    }

    pub(super) fn try_lock(&self) -> io::Result<Option<File>> {
        fs::create_dir_all(&self.directory)?;
        let file = OpenOptions::new()
            .create(true)
            .truncate(false)
            .read(true)
            .write(true)
            .open(self.directory.join(LOCK))?;
        match fs4::FileExt::try_lock(&file) {
            Ok(()) => Ok(Some(file)),
            Err(fs4::TryLockError::WouldBlock) => Ok(None),
            Err(fs4::TryLockError::Error(error)) => Err(error),
        }
    }

    fn manifest_entry(&self, name: &str) -> io::Result<Option<ManifestList>> {
        let file = match File::open(self.directory.join(MANIFEST)) {
            Ok(file) => file,
            Err(e) if e.kind() == io::ErrorKind::NotFound => return Ok(None),
            Err(e) => return Err(e),
        };
        let mut manifest: Manifest = serde_json::from_reader(BufReader::new(file))
            .map_err(|_| invalid("invalid initial base manifest"))?;
        if manifest.format_version != FORMAT_VERSION
            || manifest.namespace != hex(&self.namespace)
            || manifest.lists.len() != 1
        {
            return Err(invalid("invalid initial base manifest"));
        }
        let entry = manifest
            .lists
            .remove(name)
            .ok_or_else(|| invalid("missing list"))?;
        if name != entry.metadata.name
            || !valid_data_file(&entry.data_file)
            || entry.delta_file.is_some()
        {
            return Err(invalid("invalid initial base entry"));
        }
        Ok(Some(entry))
    }

    pub(super) fn load(
        &self,
        name: &str,
        accept: impl Fn(&IdListMetadata) -> bool,
    ) -> io::Result<Option<IdList>> {
        let load_once = || -> io::Result<Option<IdList>> {
            let Some(entry) = self.manifest_entry(name)? else {
                return Ok(None);
            };
            if !accept(&entry.metadata) {
                return Ok(None);
            }
            let ids = self.map_ids(&entry)?;
            Ok(Some(IdList {
                metadata: entry.metadata,
                ids,
            }))
        };
        // A rotation can unlink the image after we read the manifest. Retry once.
        match load_once() {
            Err(e) if e.kind() == io::ErrorKind::NotFound => load_once(),
            result => result,
        }
    }

    fn map_ids(&self, entry: &ManifestList) -> io::Result<Arc<IdListIds>> {
        let image = IdListImage::open(
            &self.directory.join(&entry.data_file),
            &self.image_namespace(&entry.metadata)?,
            &entry.metadata.name,
        )?;
        if entry.data_file != format!("list-{}.ids", hex(&image.content_digest())) {
            return Err(invalid("initial base digest mismatch"));
        }
        Ok(Arc::new(IdListIds::from_image(image)))
    }

    fn temporary(&self) -> io::Result<tempfile::NamedTempFile> {
        tempfile::Builder::new()
            .prefix(TEMP_PREFIX)
            .tempfile_in(&self.directory)
    }

    pub(super) fn publish(&self, _lock: &File, candidate: &IdList) -> io::Result<IdList> {
        let mut metadata = candidate.metadata.clone();
        metadata.url.clear();
        let name = metadata.name.clone();
        // Reclaim space from interrupted writes only when we know which image to keep.
        if let Ok(committed) = self.manifest_entry(&name) {
            let referenced = committed.as_ref().map(|entry| entry.data_file.as_str());
            let _ = self.cleanup_unreferenced(referenced);
        }
        let mut image = self.temporary()?;
        let sum = write_list_with_format(
            image.as_file_mut(),
            &self.image_namespace(&metadata)?,
            &name,
            &candidate.ids,
            self.elias_fano,
        )?;
        image.as_file().sync_all()?;
        let data_file = format!("list-{sum}.ids");
        image
            .persist(self.directory.join(&data_file))
            .map_err(|e| e.error)?;
        let entry = ManifestList {
            metadata,
            data_file: data_file.clone(),
            delta_file: None,
        };
        let ids = self.map_ids(&entry)?;
        let manifest = Manifest {
            format_version: FORMAT_VERSION,
            namespace: hex(&self.namespace),
            generation: uuid::Uuid::new_v4().to_string(),
            successful_refresh_ms: 0,
            lists: BTreeMap::from([(name, entry)]),
        };
        let mut temp = self.temporary()?;
        serde_json::to_writer(temp.as_file_mut(), &manifest)?;
        temp.as_file().sync_all()?;
        temp.persist(self.directory.join(MANIFEST))
            .map_err(|e| e.error)?;
        let _ = self.cleanup_unreferenced(Some(&data_file));
        Ok(IdList {
            metadata: candidate.metadata.clone(),
            ids,
        })
    }

    fn cleanup_unreferenced(&self, referenced: Option<&str>) -> io::Result<()> {
        for entry in fs::read_dir(&self.directory)? {
            let entry = entry?;
            let name = entry.file_name();
            let Some(name) = name.to_str() else {
                continue;
            };
            if (name.starts_with(TEMP_PREFIX) || valid_data_file(name)) && referenced != Some(name)
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
}

fn valid_data_file(name: &str) -> bool {
    name.strip_prefix("list-")
        .and_then(|value| value.strip_suffix(".ids"))
        .is_some_and(|value| {
            value.len() == 64
                && value
                    .bytes()
                    .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
        })
}
