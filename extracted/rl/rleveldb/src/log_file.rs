use std::fmt;
use std::path::{Path, PathBuf};
use std::fs::File;

use memmap2::Mmap;

use crate::types::{KeyState, Record};
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

#[derive(Debug)]
pub enum LogError {
    Io(std::io::Error),
    InvalidBlock(String),
    InvalidBatch(String),
}

impl fmt::Display for LogError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            LogError::Io(e) => write!(f, "IO error: {}", e),
            LogError::InvalidBlock(msg) => write!(f, "Invalid block: {}", msg),
            LogError::InvalidBatch(msg) => write!(f, "Invalid batch: {}", msg),
        }
    }
}

impl std::error::Error for LogError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            LogError::Io(e) => Some(e),
            _ => None,
        }
    }
}

impl From<std::io::Error> for LogError {
    fn from(e: std::io::Error) -> Self {
        LogError::Io(e)
    }
}

#[derive(Debug)]
pub struct LogFile {
    pub path: PathBuf,
    pub file_no: u64,
    _file: File,
    mmap: Option<Mmap>,
    file_size: usize,
}

impl LogFile {
    pub fn open(path: &Path) -> Result<Self, LogError> {
        let file = File::open(path).map_err(LogError::Io)?;
        let metadata = file.metadata().map_err(LogError::Io)?;
        let file_size = metadata.len() as usize;

        let file_no = path
            .file_stem()
            .and_then(|s| s.to_str())
            .and_then(|s| u64::from_str_radix(s, 16).ok())
            .unwrap_or(0);

        let mmap = if file_size > 0 {
            Some(unsafe { Mmap::map(&file).map_err(LogError::Io)? })
        } else {
            None
        };

        Ok(Self {
            path: path.to_path_buf(),
            file_no,
            _file: file,
            mmap,
            file_size,
        })
    }

    fn get_raw_blocks(&self) -> Vec<&[u8]> {
        let mmap = match &self.mmap {
            Some(m) => m,
            None => return Vec::new(),
        };
        let mut blocks = Vec::new();
        let mut offset = 0;
        while offset < self.file_size {
            let end = std::cmp::min(offset + LOG_BLOCK_SIZE, self.file_size);
            blocks.push(&mmap[offset..end]);
            offset = end;
        }
        blocks
    }

    fn get_batches(&self) -> Vec<(u64, Vec<u8>)> {
        let mut batches = Vec::new();
        let mut in_record = false;
        let mut start_block_offset: u64 = 0;
        let mut block_data = Vec::new();

        for (idx, chunk) in self.get_raw_blocks().iter().enumerate() {
            let mut cursor = SliceCursor::new(chunk);

            while cursor.position() < LOG_BLOCK_SIZE.saturating_sub(6) {
                // Read 7-byte header: crc(4) + length(2) + type(1)
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
                        let offset = (idx * LOG_BLOCK_SIZE + cursor.position()) as u64;
                        batches.push((offset, data.to_vec()));
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
                            // NOTE: The Python code has a bug here — `start_block_offset * LOG_BLOCK_SIZE`
                            // We replicate the same behavior for compatibility
                            batches.push((
                                start_block_offset * LOG_BLOCK_SIZE as u64,
                                block_data.clone(),
                            ));
                        }
                    }
                    LogEntryType::Zero => {}
                }
            }
        }
        batches
    }

    pub fn records(&self) -> Vec<Record> {
        let mut records = Vec::new();

        for (batch_offset, batch) in self.get_batches() {
            if batch.len() < 12 {
                continue;
            }

            let seq = u64::from_le_bytes(batch[0..8].try_into().unwrap());
            let count = u32::from_le_bytes(batch[8..12].try_into().unwrap());

            let mut cursor = SliceCursor::new(&batch[12..]);

            for i in 0..count {
                let start_offset = batch_offset + 12 + cursor.position() as u64;

                let state_byte = match cursor.read_byte() {
                    Some(b) => b,
                    None => break,
                };
                let state = match state_byte {
                    0 => KeyState::Deleted,
                    1 => KeyState::Live,
                    _ => KeyState::Unknown,
                };

                let key_length = match cursor.read_varint(true) {
                    Some(v) => v as usize,
                    None => break,
                };
                let key = match cursor.read_bytes(key_length) {
                    Some(k) => k.to_vec(),
                    None => break,
                };

                let value = if state != KeyState::Deleted {
                    let value_length = match cursor.read_varint(true) {
                        Some(v) => v as usize,
                        None => break,
                    };
                    match cursor.read_bytes(value_length) {
                        Some(v) => v.to_vec(),
                        None => break,
                    }
                } else {
                    Vec::new()
                };

                records.push(Record::log_record(
                    key,
                    value,
                    seq + i as u64,
                    state,
                    self.path.clone(),
                    start_offset,
                ));
            }
        }
        records
    }
}
