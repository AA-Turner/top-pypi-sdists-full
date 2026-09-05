use crate::StatsigErr;
#[cfg(not(feature = "with_zstd"))]
use std::io::Write;

const BUILD_DEFAULT_ZSTD_LEVEL: i32 = 4;

#[cfg(feature = "with_zstd")]
pub fn get_compression_format() -> String {
    "zstd".to_string()
}

#[cfg(not(feature = "with_zstd"))]
pub fn get_compression_format() -> String {
    "gzip".to_string()
}

#[cfg(feature = "with_zstd")]
pub fn compress_data(data: &[u8]) -> Result<Vec<u8>, StatsigErr> {
    compress_zstd_data(data)
}

#[cfg(not(feature = "with_zstd"))]
pub fn compress_data(data: &[u8]) -> Result<Vec<u8>, StatsigErr> {
    let mut compressed = Vec::new();
    let mut encoder = flate2::write::GzEncoder::new(&mut compressed, flate2::Compression::new(6));
    encoder
        .write_all(data)
        .map_err(|e| StatsigErr::GzipError(e.to_string()))?;
    encoder
        .finish()
        .map_err(|e| StatsigErr::GzipError(e.to_string()))?;
    Ok(compressed)
}

pub(crate) fn compress_zstd_data(data: &[u8]) -> Result<Vec<u8>, StatsigErr> {
    zstd::bulk::compress(data, BUILD_DEFAULT_ZSTD_LEVEL)
        .map_err(|e| StatsigErr::ZstdError(e.to_string()))
}
