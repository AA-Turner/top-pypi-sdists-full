use std::fs::File;
use std::io::{self, Seek, SeekFrom, Write};
use std::path::Path;
use std::sync::Arc;

use memmap2::Mmap;

use super::id_list_ids::PendingDelta;
use super::shared_id_list_format::{
    IdListImage, checked_add, digest, hex, invalid, stable_hash, write_image_keys,
};

const MAGIC: &[u8; 8] = b"STGDELT\0";
const HEADER: usize = 72;

/// One mapped operation bit per physical hash slot; keys and bits share one mmap.
pub(super) struct MappedDelta {
    owner: Arc<Mmap>,
    table: IdListImage,
    bits_start: usize,
    counts: (usize, usize),
}

impl MappedDelta {
    pub(super) fn open(
        path: &Path,
        namespace: &[u8; 32],
        name: &str,
        base_file: &str,
    ) -> io::Result<Self> {
        let file = File::open(path)?;
        if file.metadata()?.len() < HEADER as u64 {
            return Err(invalid("truncated delta header"));
        }
        let owner = Arc::new(unsafe { Mmap::map(&file)? });
        if &owner[..8] != MAGIC
            || owner[8..12] != 1u32.to_le_bytes()
            || owner[12..16] != [0; 4]
            || owner[40..72] != digest(base_file.as_bytes())
        {
            return Err(invalid("delta format or base identity mismatch"));
        }
        let number = |offset| {
            usize::try_from(u64::from_le_bytes(
                owner[offset..offset + 8].try_into().unwrap(),
            ))
            .map_err(|_| invalid("delta size exceeds platform"))
        };
        let table_len = number(16)?;
        let counts = (number(24)?, number(32)?);
        counts
            .0
            .checked_add(counts.1)
            .ok_or_else(|| invalid("delta membership count overflow"))?;
        let bits_start = checked_add(HEADER, table_len)?;
        let table = IdListImage::from_delta_region(
            Arc::clone(&owner),
            HEADER..bits_start,
            namespace,
            name,
        )?;
        if bits_start.checked_add(table.slot_capacity().div_ceil(8)) != Some(owner.len()) {
            return Err(invalid("delta bit table length mismatch"));
        }
        Ok(Self {
            owner,
            table,
            bits_start,
            counts,
        })
    }

    pub(super) fn get_hashed(&self, value: &str, hash: u64) -> Option<bool> {
        self.table
            .lookup_index_hashed(value, hash)
            .map(|slot| self.operation(slot))
    }
    pub(super) fn get(&self, value: &str) -> Option<bool> {
        self.get_hashed(value, stable_hash(value.as_bytes()))
    }
    fn operation(&self, slot: usize) -> bool {
        self.owner[self.bits_start + slot / 8] & (1 << (slot % 8)) != 0
    }
    pub(super) fn next<'a>(&'a self, cursor: &mut usize) -> Option<(&'a str, bool)> {
        self.table
            .next(cursor)
            .map(|key| (key, self.operation(*cursor - 1)))
    }
    pub(super) fn additions(&self) -> impl Iterator<Item = &str> {
        let mut cursor = 0;
        std::iter::from_fn(move || self.next(&mut cursor))
            .filter_map(|(key, added)| added.then_some(key))
    }
    pub(super) fn counts(&self) -> (usize, usize) {
        self.counts
    }
    #[cfg(test)]
    pub(super) fn validate_membership(&self) -> io::Result<()> {
        self.table.validate_membership()
    }

    #[cfg(test)]
    pub(super) fn len(&self) -> usize {
        self.table.len()
    }
    pub(super) fn mapped_bytes(&self) -> usize {
        self.owner.len()
    }
    pub(super) fn content_digest(&self) -> String {
        hex(&digest(&self.owner))
    }
}

pub(super) fn write_delta(
    file: &mut File,
    namespace: &[u8; 32],
    name: &str,
    base_file: &str,
    pending: &PendingDelta,
) -> io::Result<String> {
    file.write_all(&[0; HEADER])?;
    write_image_keys(file, namespace, name, pending.changes.image_keys())?;
    file.flush()?;
    let table_end =
        usize::try_from(file.metadata()?.len()).map_err(|_| invalid("delta too large"))?;
    let table_range = HEADER..table_end;
    let mut header = [0u8; HEADER];
    header[..8].copy_from_slice(MAGIC);
    header[8..12].copy_from_slice(&1u32.to_le_bytes());
    header[16..24].copy_from_slice(&(table_range.len() as u64).to_le_bytes());
    header[24..32].copy_from_slice(&(pending.counts.0 as u64).to_le_bytes());
    header[32..40].copy_from_slice(&(pending.counts.1 as u64).to_le_bytes());
    header[40..72].copy_from_slice(&digest(base_file.as_bytes()));
    file.seek(SeekFrom::Start(0))?;
    file.write_all(&header)?;
    file.flush()?;
    // The temporary inode is not published. Drop its initial mapping before append.
    let bits = {
        let map = Arc::new(unsafe { Mmap::map(&*file)? });
        let table = IdListImage::from_delta_region(map, table_range, namespace, name)?;
        let mut bits = vec![0u8; table.slot_capacity().div_ceil(8)];
        for (key, addition) in pending.changes.iter() {
            if addition {
                let slot = table
                    .lookup_index_hashed(key, stable_hash(key.as_bytes()))
                    .expect("written delta key");
                bits[slot / 8] |= 1 << (slot % 8);
            }
        }
        bits
    };
    file.seek(SeekFrom::End(0))?;
    file.write_all(&bits)?;
    file.flush()?;
    let map = unsafe { Mmap::map(&*file)? };
    Ok(hex(&digest(&map)))
}
