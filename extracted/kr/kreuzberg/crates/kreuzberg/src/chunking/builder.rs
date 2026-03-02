//! Chunk construction and building logic.
//!
//! This module handles the construction of individual chunks from text segments,
//! including overlap calculation, offset tracking, and metadata assembly.

use crate::error::{KreuzbergError, Result};
use crate::types::{Chunk, ChunkMetadata, PageBoundary};
use text_splitter::{Characters, ChunkCapacity, ChunkConfig};

use super::boundaries::calculate_page_range;

/// Build a ChunkConfig from chunking parameters.
///
/// # Arguments
///
/// * `max_characters` - Maximum characters per chunk
/// * `overlap` - Character overlap between consecutive chunks
/// * `trim` - Whether to trim whitespace from boundaries
///
/// # Returns
///
/// A configured ChunkConfig ready for use with text splitters.
///
/// # Errors
///
/// Returns `KreuzbergError::Validation` if configuration is invalid.
pub fn build_chunk_config(max_characters: usize, overlap: usize, trim: bool) -> Result<ChunkConfig<Characters>> {
    ChunkConfig::new(ChunkCapacity::new(max_characters))
        .with_overlap(overlap)
        .map(|config| config.with_trim(trim))
        .map_err(|e| KreuzbergError::validation(format!("Invalid chunking configuration: {}", e)))
}

/// Build chunks from text segments with optional page boundary tracking.
///
/// This function takes a collection of text segments (produced by a text splitter)
/// and constructs Chunk objects with proper metadata, including:
/// - Byte offsets accounting for overlap
/// - Chunk indices and total count
/// - Page boundary information (if provided)
///
/// # Arguments
///
/// * `text_chunks` - Iterator of text segments to convert into chunks
/// * `overlap` - Number of characters to overlap between chunks
/// * `page_boundaries` - Optional page boundary markers for mapping chunks to pages
///
/// # Returns
///
/// A vector of Chunk objects with complete metadata.
///
/// # Errors
///
/// Returns an error if page boundary calculation fails.
pub fn build_chunks<'a, I>(
    text_chunks: I,
    overlap: usize,
    page_boundaries: Option<&[PageBoundary]>,
) -> Result<Vec<Chunk>>
where
    I: IntoIterator<Item = &'a str>,
{
    let chunks_vec: Vec<&str> = text_chunks.into_iter().collect();
    let total_chunks = chunks_vec.len();
    let mut byte_offset = 0;
    let mut chunks = Vec::with_capacity(total_chunks);

    for (index, chunk_text) in chunks_vec.into_iter().enumerate() {
        let chunk = build_single_chunk(
            chunk_text,
            index,
            total_chunks,
            &mut byte_offset,
            overlap,
            page_boundaries,
        )?;
        chunks.push(chunk);
    }

    Ok(chunks)
}

/// Build a single chunk with metadata.
///
/// # Arguments
///
/// * `chunk_text` - The text content for this chunk
/// * `index` - Zero-based index of this chunk
/// * `total_chunks` - Total number of chunks in the collection
/// * `byte_offset` - Mutable reference to current byte offset (will be updated)
/// * `overlap` - Number of characters to overlap between chunks
/// * `page_boundaries` - Optional page boundary markers
///
/// # Returns
///
/// A complete Chunk object with all metadata filled in.
///
/// # Errors
///
/// Returns an error if page boundary calculation fails.
fn build_single_chunk(
    chunk_text: &str,
    index: usize,
    total_chunks: usize,
    byte_offset: &mut usize,
    overlap: usize,
    page_boundaries: Option<&[PageBoundary]>,
) -> Result<Chunk> {
    let byte_start = *byte_offset;
    let chunk_length = chunk_text.len();
    let byte_end = byte_start + chunk_length;

    // Calculate overlap for next chunk (not applicable to last chunk)
    let overlap_chars = if index < total_chunks - 1 {
        overlap.min(chunk_length)
    } else {
        0
    };

    // Update offset for next chunk, accounting for overlap
    *byte_offset = byte_end - overlap_chars;

    // Calculate page range if boundaries are provided
    let (first_page, last_page) = if let Some(boundaries) = page_boundaries {
        calculate_page_range(byte_start, byte_end, boundaries)?
    } else {
        (None, None)
    };

    Ok(Chunk {
        content: chunk_text.to_string(),
        embedding: None,
        metadata: ChunkMetadata {
            byte_start,
            byte_end,
            token_count: None,
            chunk_index: index,
            total_chunks,
            first_page,
            last_page,
        },
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_build_chunk_config_valid() {
        let result = build_chunk_config(100, 10, true);
        assert!(result.is_ok());
    }

    #[test]
    fn test_build_chunk_config_invalid_overlap() {
        let result = build_chunk_config(10, 20, true);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(matches!(err, KreuzbergError::Validation { .. }));
    }

    #[test]
    fn test_build_chunks_empty() {
        let text_chunks: Vec<&str> = vec![];
        let result = build_chunks(text_chunks, 5, None).unwrap();
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_build_chunks_single() {
        let text_chunks = vec!["Single chunk"];
        let result = build_chunks(text_chunks, 5, None).unwrap();
        assert_eq!(result.len(), 1);
        assert_eq!(result[0].content, "Single chunk");
        assert_eq!(result[0].metadata.chunk_index, 0);
        assert_eq!(result[0].metadata.total_chunks, 1);
        assert_eq!(result[0].metadata.byte_start, 0);
        assert_eq!(result[0].metadata.byte_end, 12);
    }

    #[test]
    fn test_build_chunks_multiple_with_overlap() {
        let text_chunks = vec!["First chunk here", "Second chunk here", "Third chunk here"];
        let overlap = 5;
        let result = build_chunks(text_chunks, overlap, None).unwrap();

        assert_eq!(result.len(), 3);

        // First chunk
        assert_eq!(result[0].content, "First chunk here");
        assert_eq!(result[0].metadata.byte_start, 0);
        assert_eq!(result[0].metadata.byte_end, 16);

        // Second chunk should start before first ends (overlap)
        assert!(result[1].metadata.byte_start < result[0].metadata.byte_end);

        // Third chunk should start before second ends (overlap)
        assert!(result[2].metadata.byte_start < result[1].metadata.byte_end);
    }

    #[test]
    fn test_build_chunks_with_page_boundaries() {
        let text_chunks = vec!["First chunk", "Second chunk"];
        let boundaries = vec![
            PageBoundary {
                byte_start: 0,
                byte_end: 11,
                page_number: 1,
            },
            PageBoundary {
                byte_start: 11,
                byte_end: 23,
                page_number: 2,
            },
        ];

        let result = build_chunks(text_chunks, 0, Some(&boundaries)).unwrap();

        assert_eq!(result.len(), 2);
        assert_eq!(result[0].metadata.first_page, Some(1));
        assert_eq!(result[1].metadata.first_page, Some(2));
    }

    #[test]
    fn test_build_chunks_offset_tracking() {
        let text_chunks = vec!["AAAAA", "BBBBB", "CCCCC"];
        let overlap = 2;
        let result = build_chunks(text_chunks, overlap, None).unwrap();

        assert_eq!(result.len(), 3);

        // First chunk: 0-5
        assert_eq!(result[0].metadata.byte_start, 0);
        assert_eq!(result[0].metadata.byte_end, 5);

        // Second chunk: 3-8 (overlap of 2)
        assert_eq!(result[1].metadata.byte_start, 3);
        assert_eq!(result[1].metadata.byte_end, 8);

        // Third chunk: 6-11 (overlap of 2, but last chunk so no further adjustment)
        assert_eq!(result[2].metadata.byte_start, 6);
        assert_eq!(result[2].metadata.byte_end, 11);
    }

    #[test]
    fn test_build_single_chunk_metadata() {
        let mut offset = 0;
        let chunk = build_single_chunk("Test content", 0, 1, &mut offset, 5, None).unwrap();

        assert_eq!(chunk.content, "Test content");
        assert_eq!(chunk.metadata.byte_start, 0);
        assert_eq!(chunk.metadata.byte_end, 12);
        assert_eq!(chunk.metadata.chunk_index, 0);
        assert_eq!(chunk.metadata.total_chunks, 1);
        assert_eq!(chunk.metadata.first_page, None);
        assert_eq!(chunk.metadata.last_page, None);
    }

    #[test]
    fn test_build_single_chunk_with_overlap() {
        let mut offset = 0;

        // First chunk
        let chunk1 = build_single_chunk("0123456789", 0, 2, &mut offset, 3, None).unwrap();
        assert_eq!(chunk1.metadata.byte_start, 0);
        assert_eq!(chunk1.metadata.byte_end, 10);
        assert_eq!(offset, 7); // 10 - 3 (overlap)

        // Second chunk
        let chunk2 = build_single_chunk("ABCDEFGHIJ", 1, 2, &mut offset, 3, None).unwrap();
        assert_eq!(chunk2.metadata.byte_start, 7);
        assert_eq!(chunk2.metadata.byte_end, 17);
        assert_eq!(offset, 17); // Last chunk, no overlap subtracted
    }

    #[test]
    fn test_build_chunks_no_overlap() {
        let text_chunks = vec!["AAAAA", "BBBBB", "CCCCC"];
        let result = build_chunks(text_chunks, 0, None).unwrap();

        assert_eq!(result.len(), 3);

        // Chunks should be contiguous with no overlap
        assert_eq!(result[0].metadata.byte_start, 0);
        assert_eq!(result[0].metadata.byte_end, 5);

        assert_eq!(result[1].metadata.byte_start, 5);
        assert_eq!(result[1].metadata.byte_end, 10);

        assert_eq!(result[2].metadata.byte_start, 10);
        assert_eq!(result[2].metadata.byte_end, 15);
    }
}
