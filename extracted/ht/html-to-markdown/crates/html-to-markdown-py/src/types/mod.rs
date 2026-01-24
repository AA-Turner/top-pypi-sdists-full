#[cfg(feature = "inline-images")]
pub mod inline_image;

#[cfg(feature = "metadata")]
pub mod metadata;

#[cfg(feature = "inline-images")]
pub use inline_image::{InlineImageConfig, inline_image_to_py, warning_to_py};

#[cfg(feature = "metadata")]
pub use metadata::{
    MetadataConfig, btreemap_to_py, document_metadata_to_py, extended_metadata_to_py, headers_to_py, images_to_py,
    links_to_py, opt_string_to_py, structured_data_to_py, text_direction_to_str,
};
