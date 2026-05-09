//! Image extraction using the pdf_oxide backend.
//!
//! Extracts embedded image positions from PDF pages via pdf_oxide for use
//! in the assembly pipeline.

use super::OxideDocument;
use crate::pdf::error::{PdfError, Result};

/// Extract image positions from all pages for interleaving into the assembly pipeline.
///
/// Calls `doc.doc.extract_images(page_idx)` for each page and creates an
/// `(page_number, image_index)` pair for each image found. These positions
/// are used by the assembly pipeline to insert image placeholders into the
/// document structure.
///
/// # Arguments
///
/// * `doc` - Mutable reference to the oxide document
///
/// # Returns
///
/// A `Vec<(usize, usize)>` of (1-indexed page number, global image index) pairs.
pub(crate) fn extract_image_positions(doc: &mut OxideDocument) -> Result<Vec<(usize, usize)>> {
    let page_count = doc
        .doc
        .page_count()
        .map_err(|e| PdfError::MetadataExtractionFailed(format!("pdf_oxide: failed to get page count: {e}")))?;

    let mut positions = Vec::new();
    let mut global_index = 0usize;

    for page_idx in 0..page_count {
        let oxide_images = match doc.doc.extract_images(page_idx) {
            Ok(images) => images,
            Err(e) => {
                tracing::debug!(
                    page = page_idx,
                    "pdf_oxide: failed to extract images for positions: {e}"
                );
                continue;
            }
        };

        let page_number = page_idx + 1; // Kreuzberg uses 1-indexed page numbers

        for _img in &oxide_images {
            positions.push((page_number, global_index));
            global_index += 1;
        }
    }

    Ok(positions)
}
