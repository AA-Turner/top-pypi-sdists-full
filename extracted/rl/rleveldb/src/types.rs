use std::path::PathBuf;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FileType {
    Ldb,
    Log,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum KeyState {
    Deleted = 0,
    Live = 1,
    Unknown = 2,
}

#[derive(Debug, Clone)]
pub struct Record {
    pub key: Vec<u8>,
    pub value: Vec<u8>,
    pub seq: u64,
    pub state: KeyState,
    pub file_type: FileType,
    pub origin_file: PathBuf,
    pub offset: u64,
    pub was_compressed: bool,
}

impl Record {
    pub fn user_key(&self) -> &[u8] {
        match self.file_type {
            FileType::Ldb => {
                if self.key.len() < 8 {
                    &self.key
                } else {
                    &self.key[..self.key.len() - 8]
                }
            }
            FileType::Log => &self.key,
        }
    }

    pub fn ldb_record(
        key: Vec<u8>,
        value: Vec<u8>,
        origin_file: PathBuf,
        offset: u64,
        was_compressed: bool,
    ) -> Self {
        let (seq, state) = if key.len() >= 8 {
            let seq_bytes: [u8; 8] = key[key.len() - 8..].try_into().unwrap();
            let raw = u64::from_le_bytes(seq_bytes);
            let seq = raw >> 8;
            let state = if key.len() > 8 {
                if key[key.len() - 8] == 0 {
                    KeyState::Deleted
                } else {
                    KeyState::Live
                }
            } else {
                KeyState::Unknown
            };
            (seq, state)
        } else {
            (0, KeyState::Unknown)
        };

        Self {
            key,
            value,
            seq,
            state,
            file_type: FileType::Ldb,
            origin_file,
            offset,
            was_compressed,
        }
    }

    pub fn log_record(
        key: Vec<u8>,
        value: Vec<u8>,
        seq: u64,
        state: KeyState,
        origin_file: PathBuf,
        offset: u64,
    ) -> Self {
        Self {
            key,
            value,
            seq,
            state,
            file_type: FileType::Log,
            origin_file,
            offset,
            was_compressed: false,
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub struct BlockHandle {
    pub offset: u64,
    pub length: u64,
}

impl BlockHandle {
    pub fn from_cursor(cursor: &mut crate::varint::SliceCursor) -> Option<Self> {
        let offset = cursor.read_varint(false)?;
        let length = cursor.read_varint(false)?;
        Some(Self { offset, length })
    }

    pub fn from_bytes(data: &[u8]) -> Option<Self> {
        let mut cursor = crate::varint::SliceCursor::new(data);
        Self::from_cursor(&mut cursor)
    }
}

#[derive(Debug, Clone)]
pub struct RawBlockEntry {
    pub key: Vec<u8>,
    pub value: Vec<u8>,
    pub block_offset: usize,
}
