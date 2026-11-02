use std::collections::HashMap;
use std::fmt;
use std::fs::File;
use std::path::{Path, PathBuf};

use memmap2::Mmap;

use crate::varint::SliceCursor;

const LOG_BLOCK_SIZE: usize = 32768;

#[derive(Debug, Clone, Copy, PartialEq)]
#[repr(u8)]
enum LogEntryType {
    Zero = 0,
    Full = 1,
    First = 2,
    Middle = 3,
    Last = 4,
}

impl LogEntryType {
    fn from_u8(v: u8) -> Option<Self> {
        match v {
            0 => Some(Self::Zero),
            1 => Some(Self::Full),
            2 => Some(Self::First),
            3 => Some(Self::Middle),
            4 => Some(Self::Last),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq)]
enum VersionEditTag {
    Comparator = 1,
    LogNumber = 2,
    NextFileNumber = 3,
    LastSequence = 4,
    CompactPointer = 5,
    DeletedFile = 6,
    NewFile = 7,
    PrevLogNumber = 9,
}

impl VersionEditTag {
    fn from_u64(v: u64) -> Option<Self> {
        match v {
            1 => Some(Self::Comparator),
            2 => Some(Self::LogNumber),
            3 => Some(Self::NextFileNumber),
            4 => Some(Self::LastSequence),
            5 => Some(Self::CompactPointer),
            6 => Some(Self::DeletedFile),
            7 => Some(Self::NewFile),
            9 => Some(Self::PrevLogNumber),
            _ => None,
        }
    }
}

#[derive(Debug, Clone)]
pub struct CompactionPointer {
    pub level: u64,
    pub pointer: Vec<u8>,
}

#[derive(Debug, Clone)]
pub struct DeletedFile {
    pub level: u64,
    pub file_no: u64,
}

#[derive(Debug, Clone)]
pub struct NewFile {
    pub level: u64,
    pub file_no: u64,
    pub file_size: u64,
    pub smallest_key: Vec<u8>,
    pub largest_key: Vec<u8>,
}

#[derive(Debug, Clone, Default)]
pub struct VersionEdit {
    pub comparator: Option<String>,
    pub log_number: Option<u64>,
    pub prev_log_number: Option<u64>,
    pub last_sequence: Option<u64>,
    pub next_file_number: Option<u64>,
    pub compaction_pointers: Vec<CompactionPointer>,
    pub deleted_files: Vec<DeletedFile>,
    pub new_files: Vec<NewFile>,
}

impl VersionEdit {
    pub fn from_buffer(buffer: &[u8]) -> Self {
        let mut edit = VersionEdit::default();
        let mut cursor = SliceCursor::new(buffer);

        while cursor.position() < buffer.len().saturating_sub(1) {
            let tag_val = match cursor.read_varint(true) {
                Some(v) => v,
                None => break,
            };
            let tag = match VersionEditTag::from_u64(tag_val) {
                Some(t) => t,
                None => break,
            };

            match tag {
                VersionEditTag::Comparator => {
                    if let Some(blob) = cursor.read_length_prefixed_blob() {
                        edit.comparator = String::from_utf8(blob.to_vec()).ok();
                    }
                }
                VersionEditTag::LogNumber => {
                    edit.log_number = cursor.read_varint(false);
                }
                VersionEditTag::PrevLogNumber => {
                    edit.prev_log_number = cursor.read_varint(false);
                }
                VersionEditTag::NextFileNumber => {
                    edit.next_file_number = cursor.read_varint(false);
                }
                VersionEditTag::LastSequence => {
                    edit.last_sequence = cursor.read_varint(false);
                }
                VersionEditTag::CompactPointer => {
                    let level = cursor.read_varint(true).unwrap_or(0);
                    let pointer = cursor
                        .read_length_prefixed_blob()
                        .unwrap_or(&[])
                        .to_vec();
                    edit.compaction_pointers
                        .push(CompactionPointer { level, pointer });
                }
                VersionEditTag::DeletedFile => {
                    let level = cursor.read_varint(true).unwrap_or(0);
                    let file_no = cursor.read_varint(false).unwrap_or(0);
                    edit.deleted_files.push(DeletedFile { level, file_no });
                }
                VersionEditTag::NewFile => {
                    let level = cursor.read_varint(true).unwrap_or(0);
                    let file_no = cursor.read_varint(false).unwrap_or(0);
                    let file_size = cursor.read_varint(false).unwrap_or(0);
                    let smallest_key = cursor
                        .read_length_prefixed_blob()
                        .unwrap_or(&[])
                        .to_vec();
                    let largest_key = cursor
                        .read_length_prefixed_blob()
                        .unwrap_or(&[])
                        .to_vec();
                    edit.new_files.push(NewFile {
                        level,
                        file_no,
                        file_size,
                        smallest_key,
                        largest_key,
                    });
                }
            }
        }
        edit
    }
}

#[derive(Debug)]
pub enum ManifestError {
    Io(std::io::Error),
    InvalidName,
    InvalidBlock(String),
}

impl fmt::Display for ManifestError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ManifestError::Io(e) => write!(f, "manifest I/O error: {e}"),
            ManifestError::InvalidName => write!(f, "invalid manifest filename"),
            ManifestError::InvalidBlock(msg) => write!(f, "invalid manifest block: {msg}"),
        }
    }
}

impl std::error::Error for ManifestError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            ManifestError::Io(e) => Some(e),
            _ => None,
        }
    }
}

impl From<std::io::Error> for ManifestError {
    fn from(e: std::io::Error) -> Self {
        ManifestError::Io(e)
    }
}

pub struct ManifestFile {
    pub path: PathBuf,
    pub file_no: u64,
    pub file_to_level: HashMap<u64, u64>,
    _file: File,
    mmap: Option<Mmap>,
    file_size: usize,
}

impl ManifestFile {
    pub const MANIFEST_FILENAME_PATTERN: &'static str = r"MANIFEST-([0-9A-Fa-f]{6})";

    pub fn open(path: &Path) -> Result<Self, ManifestError> {
        let name = path
            .file_name()
            .and_then(|n| n.to_str())
            .ok_or(ManifestError::InvalidName)?;
        let file_no = if let Some(hex_part) = name.strip_prefix("MANIFEST-") {
            u64::from_str_radix(hex_part, 16).map_err(|_| ManifestError::InvalidName)?
        } else {
            return Err(ManifestError::InvalidName);
        };

        let file = File::open(path).map_err(ManifestError::Io)?;
        let metadata = file.metadata().map_err(ManifestError::Io)?;
        let file_size = metadata.len() as usize;

        let mmap = if file_size > 0 {
            Some(unsafe { Mmap::map(&file).map_err(ManifestError::Io)? })
        } else {
            None
        };

        let mut manifest = Self {
            path: path.to_path_buf(),
            file_no,
            file_to_level: HashMap::new(),
            _file: file,
            mmap,
            file_size,
        };

        let edits = manifest.version_edits();
        for edit in &edits {
            for nf in &edit.new_files {
                manifest.file_to_level.insert(nf.file_no, nf.level);
            }
        }

        Ok(manifest)
    }

    fn get_batches(&self) -> Vec<(u64, Vec<u8>)> {
        let mmap = match &self.mmap {
            Some(m) => m,
            None => return Vec::new(),
        };

        let mut batches = Vec::new();
        let mut in_record = false;
        let mut start_block_offset: u64 = 0;
        let mut block_data = Vec::new();
        let mut offset = 0;
        let mut idx: usize = 0;

        while offset < self.file_size {
            let end = std::cmp::min(offset + LOG_BLOCK_SIZE, self.file_size);
            let chunk = &mmap[offset..end];
            let mut cursor = SliceCursor::new(chunk);

            while cursor.position() < LOG_BLOCK_SIZE.saturating_sub(6) {
                let header = match cursor.read_bytes(7) {
                    Some(h) => h,
                    None => break,
                };
                let _crc = u32::from_le_bytes(header[0..4].try_into().unwrap());
                let length = u16::from_le_bytes(header[4..6].try_into().unwrap()) as usize;
                let block_type = match LogEntryType::from_u8(header[6]) {
                    Some(t) => t,
                    None => break,
                };

                let data = match cursor.read_bytes(length) {
                    Some(d) => d,
                    None => break,
                };

                match block_type {
                    LogEntryType::Full => {
                        in_record = false;
                        batches.push((
                            (idx * LOG_BLOCK_SIZE + cursor.position()) as u64,
                            data.to_vec(),
                        ));
                    }
                    LogEntryType::First => {
                        start_block_offset =
                            (idx * LOG_BLOCK_SIZE + cursor.position()) as u64;
                        block_data = data.to_vec();
                        in_record = true;
                    }
                    LogEntryType::Middle => {
                        if in_record {
                            block_data.extend_from_slice(data);
                        }
                    }
                    LogEntryType::Last => {
                        if in_record {
                            block_data.extend_from_slice(data);
                            in_record = false;
                            batches.push((
                                start_block_offset * LOG_BLOCK_SIZE as u64,
                                block_data.clone(),
                            ));
                        }
                    }
                    LogEntryType::Zero => {}
                }
            }
            offset = end;
            idx += 1;
        }
        batches
    }

    pub fn version_edits(&self) -> Vec<VersionEdit> {
        self.get_batches()
            .into_iter()
            .map(|(_, batch)| VersionEdit::from_buffer(&batch))
            .collect()
    }
}
