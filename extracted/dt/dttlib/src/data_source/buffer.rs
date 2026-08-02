use std::ops::Deref;

#[cfg(feature = "nds")]
use crate::errors::DTTError;

/// These are the extra fields added to a cache buffer in Buffer
/// It's useful to bring these out as another struct so they can be passed to a function
/// after previously extracting the underlying cache_buffer
#[derive(Debug)]
pub struct Fields {
    /// total number of data points that had to be filled in with gaps.
    pub total_gap_size: usize,
}

/// wrapper arund an nds_cache_rs::Buffer that contains some extra info dttlib needs
#[derive(Debug)]
pub struct Buffer {
    pub cache_buffer: nds_cache_rs::buffer::Buffer,

    pub fields: Fields,
}

impl From<nds_cache_rs::buffer::Buffer> for Buffer {
    fn from(cache_buffer: nds_cache_rs::buffer::Buffer) -> Self {
        Self {
            cache_buffer,
            fields: Fields { total_gap_size: 0 },
        }
    }
}

#[cfg(feature = "nds")]
impl TryFrom<nds2_client_rs::Buffer> for Buffer {
    type Error = DTTError;

    fn try_from(value: nds2_client_rs::Buffer) -> Result<Self, Self::Error> {
        let cache_buffer: nds_cache_rs::buffer::Buffer = value.try_into()?;
        Ok(cache_buffer.into())
    }
}

impl Deref for Buffer {
    type Target = nds_cache_rs::buffer::Buffer;

    fn deref(&self) -> &Self::Target {
        &self.cache_buffer
    }
}

impl PartialEq for Buffer {
    fn eq(&self, other: &Self) -> bool {
        self.cache_buffer == other.cache_buffer
    }
}

impl Eq for Buffer {}

impl PartialOrd for Buffer {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.cache_buffer.partial_cmp(&other.cache_buffer)
    }
}

impl Ord for Buffer {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.cache_buffer.cmp(&other.cache_buffer)
    }
}
