use std::fmt;
use std::path::{Path, PathBuf};
use std::fs::File;

use memmap2::Mmap;

use crate::snappy;
use crate::types::{BlockHandle, RawBlockEntry, Record};
use crate::varint::SliceCursor;

#[derive(Debug)]
pub enum LdbError {
    Io(std::io::Error),
    InvalidMagic(PathBuf),
    InvalidBlock(String),
    Snappy(snappy::SnappyError),
    FileTooSmall,
}

impl fmt::Display for LdbError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LdbError::Io(e) => write!(f, "IO error: {e}"),
            LdbError::InvalidMagic(path) => {
                write!(f, "Invalid magic number in {}", path.display())
            }
            LdbError::InvalidBlock(msg) => write!(f, "Invalid block: {msg}"),
            LdbError::Snappy(e) => write!(f, "Snappy decompression error: {e}"),
            LdbError::FileTooSmall => write!(f, "File too small to contain a valid footer"),
        }
    }
}

impl std::error::Error for LdbError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            LdbError::Io(e) => Some(e),
            LdbError::Snappy(e) => Some(e),
            _ => None,
        }
    }
}

impl From<std::io::Error> for LdbError {
    fn from(e: std::io::Error) -> Self {
        LdbError::Io(e)
    }
}

impl From<snappy::SnappyError> for LdbError {
    fn from(e: snappy::SnappyError) -> Self {
        LdbError::Snappy(e)
    }
}

struct Block {
    raw: Vec<u8>,
    was_compressed: bool,
    offset: u64,
    #[allow(dead_code)]
    restart_array_count: u32,
    restart_array_offset: usize,
}

impl Block {
    fn new(raw: Vec<u8>, was_compressed: bool, offset: u64) -> Self {
        let len = raw.len();
        let restart_array_count =
            u32::from_le_bytes(raw[len - 4..].try_into().unwrap());
        let restart_array_offset = len - (restart_array_count as usize + 1) * 4;
        Self {
            raw,
            was_compressed,
            offset,
            restart_array_count,
            restart_array_offset,
        }
    }

    fn get_restart_offset(&self, index: usize) -> usize {
        let off = self.restart_array_offset + index * 4;
        i32::from_le_bytes(self.raw[off..off + 4].try_into().unwrap()) as usize
    }

    fn entries(&self) -> Vec<RawBlockEntry> {
        let mut result = Vec::new();
        let start = self.get_restart_offset(0);
        let mut cursor = SliceCursor::new(&self.raw);
        cursor.seek(start);
        let mut key = Vec::new();

        while cursor.position() < self.restart_array_offset {
            let start_offset = cursor.position();
            let shared_length = match cursor.read_varint(true) {
                Some(v) => v as usize,
                None => break,
            };
            let non_shared_length = match cursor.read_varint(true) {
                Some(v) => v as usize,
                None => break,
            };
            let value_length = match cursor.read_varint(true) {
                Some(v) => v as usize,
                None => break,
            };

            if shared_length > key.len() {
                break;
            }

            key.truncate(shared_length);
            if let Some(non_shared) = cursor.read_bytes(non_shared_length) {
                key.extend_from_slice(non_shared);
            } else {
                break;
            }

            let value = match cursor.read_bytes(value_length) {
                Some(v) => v.to_vec(),
                None => break,
            };

            result.push(RawBlockEntry {
                key: key.clone(),
                value,
                block_offset: start_offset,
            });
        }
        result
    }
}

pub struct LdbFile {
    pub path: PathBuf,
    pub file_no: u64,
    _file: File,
    mmap: Option<Mmap>,
    index: Vec<(Vec<u8>, BlockHandle)>,
}

impl LdbFile {
    const BLOCK_TRAILER_SIZE: usize = 5;
    const FOOTER_SIZE: usize = 48;
    const MAGIC: u64 = 0xDB4775248B80FB57;

    pub fn open(path: &Path) -> Result<Self, LdbError> {
        let file = File::open(path)?;
        let metadata = file.metadata()?;
        let file_size = metadata.len() as usize;

        let file_no = path
            .file_stem()
            .and_then(|s| s.to_str())
            .and_then(|s| u64::from_str_radix(s, 16).ok())
            .unwrap_or(0);

        if file_size < Self::FOOTER_SIZE {
            return Ok(Self {
                path: path.to_path_buf(),
                file_no,
                _file: file,
                mmap: None,
                index: Vec::new(),
            });
        }

        let mmap = unsafe { Mmap::map(&file)? };

        // Read footer
        let footer_start = file_size - Self::FOOTER_SIZE;
        let mut cursor = SliceCursor::new(&mmap[footer_start..file_size]);
        let _meta_index_handle = BlockHandle::from_cursor(&mut cursor)
            .ok_or_else(|| {
                LdbError::InvalidBlock("Failed to read meta index handle".into())
            })?;
        let index_handle = BlockHandle::from_cursor(&mut cursor)
            .ok_or_else(|| {
                LdbError::InvalidBlock("Failed to read index handle".into())
            })?;

        // Check magic
        let magic_bytes: [u8; 8] =
            mmap[file_size - 8..file_size].try_into().unwrap();
        let magic = u64::from_le_bytes(magic_bytes);
        if magic != Self::MAGIC {
            return Err(LdbError::InvalidMagic(path.to_path_buf()));
        }

        let mut ldb = Self {
            path: path.to_path_buf(),
            file_no,
            _file: file,
            mmap: Some(mmap),
            index: Vec::new(),
        };

        // Read index
        let index_block = ldb.read_block(&index_handle)?;
        ldb.index = index_block
            .entries()
            .into_iter()
            .filter_map(|entry| {
                let handle = BlockHandle::from_bytes(&entry.value)?;
                Some((entry.key, handle))
            })
            .collect();

        Ok(ldb)
    }

    fn read_block(&self, handle: &BlockHandle) -> Result<Block, LdbError> {
        let mmap = self.mmap.as_ref().ok_or(LdbError::FileTooSmall)?;
        let block_start = handle.offset as usize;
        let block_end = block_start + handle.length as usize;
        let trailer_end = block_end + Self::BLOCK_TRAILER_SIZE;

        if trailer_end > mmap.len() {
            return Err(LdbError::InvalidBlock(format!(
                "Block extends past end of file at offset {} in {}",
                handle.offset,
                self.path.display()
            )));
        }

        let raw_block = &mmap[block_start..block_end];
        let trailer = &mmap[block_end..trailer_end];

        let is_compressed = trailer[0] != 0;
        let block_data = if is_compressed {
            snappy::decompress(raw_block)?
        } else {
            raw_block.to_vec()
        };

        Ok(Block::new(block_data, is_compressed, handle.offset))
    }

    pub fn records(&self) -> Vec<Record> {
        let mut records = Vec::new();
        for (_block_key, handle) in &self.index {
            if let Ok(block) = self.read_block(handle) {
                for entry in block.entries() {
                    let offset = if block.was_compressed {
                        block.offset
                    } else {
                        block.offset + entry.block_offset as u64
                    };
                    records.push(Record::ldb_record(
                        entry.key,
                        entry.value,
                        self.path.clone(),
                        offset,
                        block.was_compressed,
                    ));
                }
            }
        }
        records
    }
}
