#[cfg(feature = "metadata")]
use html_to_markdown_rs::metadata::{
    DEFAULT_MAX_STRUCTURED_DATA_SIZE, DocumentMetadata as RustDocumentMetadata,
    ExtendedMetadata as RustExtendedMetadata, HeaderMetadata as RustHeaderMetadata, ImageMetadata as RustImageMetadata,
    LinkMetadata as RustLinkMetadata, MetadataConfig as RustMetadataConfig, StructuredData as RustStructuredData,
    TextDirection as RustTextDirection,
};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyTuple};

/// Python wrapper for metadata extraction configuration
#[cfg(feature = "metadata")]
#[pyclass]
#[derive(Clone)]
pub struct MetadataConfig {
    #[pyo3(get, set)]
    pub extract_document: bool,
    #[pyo3(get, set)]
    pub extract_headers: bool,
    #[pyo3(get, set)]
    pub extract_links: bool,
    #[pyo3(get, set)]
    pub extract_images: bool,
    #[pyo3(get, set)]
    pub extract_structured_data: bool,
    #[pyo3(get, set)]
    pub max_structured_data_size: usize,
}

#[cfg(feature = "metadata")]
#[pymethods]
impl MetadataConfig {
    #[new]
    #[pyo3(signature = (
        extract_document=true,
        extract_headers=true,
        extract_links=true,
        extract_images=true,
        extract_structured_data=true,
        max_structured_data_size=DEFAULT_MAX_STRUCTURED_DATA_SIZE
    ))]
    pub const fn new(
        extract_document: bool,
        extract_headers: bool,
        extract_links: bool,
        extract_images: bool,
        extract_structured_data: bool,
        max_structured_data_size: usize,
    ) -> Self {
        Self {
            extract_document,
            extract_headers,
            extract_links,
            extract_images,
            extract_structured_data,
            max_structured_data_size,
        }
    }
}

#[cfg(feature = "metadata")]
impl MetadataConfig {
    pub const fn to_rust(&self) -> RustMetadataConfig {
        RustMetadataConfig {
            extract_document: self.extract_document,
            extract_headers: self.extract_headers,
            extract_links: self.extract_links,
            extract_images: self.extract_images,
            extract_structured_data: self.extract_structured_data,
            max_structured_data_size: self.max_structured_data_size,
        }
    }
}

/// Helper: Convert Option<String> to Python
#[cfg(feature = "metadata")]
pub fn opt_string_to_py<'py>(py: Python<'py>, opt: Option<String>) -> PyResult<Py<PyAny>> {
    match opt {
        Some(val) => {
            let str_obj = pyo3::types::PyString::new(py, &val);
            Ok(str_obj.into())
        }
        None => Ok(py.None()),
    }
}

/// Helper: Convert BTreeMap to Python dict
#[cfg(feature = "metadata")]
pub fn btreemap_to_py<'py>(py: Python<'py>, map: std::collections::BTreeMap<String, String>) -> PyResult<Py<PyAny>> {
    let dict = PyDict::new(py);
    for (k, v) in map {
        dict.set_item(k, v)?;
    }
    Ok(dict.into())
}

/// Helper: Convert TextDirection to string
#[cfg(feature = "metadata")]
pub fn text_direction_to_str<'py>(py: Python<'py>, text_direction: Option<RustTextDirection>) -> Py<PyAny> {
    match text_direction {
        Some(direction) => pyo3::types::PyString::new(py, &direction.to_string())
            .as_any()
            .to_owned()
            .into(),
        None => py.None(),
    }
}

/// Helper: Convert DocumentMetadata to Python dict
#[cfg(feature = "metadata")]
pub fn document_metadata_to_py<'py>(py: Python<'py>, doc: RustDocumentMetadata) -> PyResult<Py<PyAny>> {
    let dict = PyDict::new(py);

    dict.set_item("title", opt_string_to_py(py, doc.title)?)?;
    dict.set_item("description", opt_string_to_py(py, doc.description)?)?;
    dict.set_item("keywords", doc.keywords)?;
    dict.set_item("author", opt_string_to_py(py, doc.author)?)?;
    dict.set_item("canonical_url", opt_string_to_py(py, doc.canonical_url)?)?;
    dict.set_item("base_href", opt_string_to_py(py, doc.base_href)?)?;
    dict.set_item("language", opt_string_to_py(py, doc.language)?)?;
    dict.set_item("text_direction", text_direction_to_str(py, doc.text_direction))?;
    dict.set_item("open_graph", btreemap_to_py(py, doc.open_graph)?)?;
    dict.set_item("twitter_card", btreemap_to_py(py, doc.twitter_card)?)?;
    dict.set_item("meta_tags", btreemap_to_py(py, doc.meta_tags)?)?;

    Ok(dict.into())
}

/// Helper: Convert headers to Python list
#[cfg(feature = "metadata")]
pub fn headers_to_py<'py>(py: Python<'py>, headers: Vec<RustHeaderMetadata>) -> PyResult<Py<PyAny>> {
    let list = PyList::empty(py);
    for header in headers {
        let dict = PyDict::new(py);
        dict.set_item("level", header.level)?;
        dict.set_item("text", header.text)?;
        dict.set_item("id", opt_string_to_py(py, header.id)?)?;
        dict.set_item("depth", header.depth)?;
        dict.set_item("html_offset", header.html_offset)?;
        list.append(dict)?;
    }
    Ok(list.into())
}

/// Helper: Convert links to Python list
#[cfg(feature = "metadata")]
pub fn links_to_py<'py>(py: Python<'py>, links: Vec<RustLinkMetadata>) -> PyResult<Py<PyAny>> {
    let list = PyList::empty(py);
    for link in links {
        let dict = PyDict::new(py);
        dict.set_item("href", link.href)?;
        dict.set_item("text", link.text)?;
        dict.set_item("title", opt_string_to_py(py, link.title)?)?;
        dict.set_item("link_type", link.link_type.to_string())?;
        dict.set_item("rel", link.rel)?;
        dict.set_item("attributes", btreemap_to_py(py, link.attributes)?)?;
        list.append(dict)?;
    }
    Ok(list.into())
}

/// Helper: Convert images to Python list
#[cfg(feature = "metadata")]
pub fn images_to_py<'py>(py: Python<'py>, images: Vec<RustImageMetadata>) -> PyResult<Py<PyAny>> {
    let list = PyList::empty(py);
    for image in images {
        let dict = PyDict::new(py);
        dict.set_item("src", image.src)?;
        dict.set_item("alt", opt_string_to_py(py, image.alt)?)?;
        dict.set_item("title", opt_string_to_py(py, image.title)?)?;

        let dims = match image.dimensions {
            Some((width, height)) => {
                let tuple = PyTuple::new(py, [width, height])?;
                tuple.into()
            }
            None => py.None(),
        };
        dict.set_item("dimensions", dims)?;

        dict.set_item("image_type", image.image_type.to_string())?;
        dict.set_item("attributes", btreemap_to_py(py, image.attributes)?)?;
        list.append(dict)?;
    }
    Ok(list.into())
}

/// Helper: Convert structured data to Python list
#[cfg(feature = "metadata")]
pub fn structured_data_to_py<'py>(py: Python<'py>, data: Vec<RustStructuredData>) -> PyResult<Py<PyAny>> {
    let list = PyList::empty(py);
    for item in data {
        let dict = PyDict::new(py);
        dict.set_item("data_type", item.data_type.to_string())?;
        dict.set_item("raw_json", item.raw_json)?;
        dict.set_item("schema_type", opt_string_to_py(py, item.schema_type)?)?;
        list.append(dict)?;
    }
    Ok(list.into())
}

/// Helper: Convert extended metadata to Python dict
#[cfg(feature = "metadata")]
pub fn extended_metadata_to_py<'py>(py: Python<'py>, metadata: RustExtendedMetadata) -> PyResult<Py<PyAny>> {
    let dict = PyDict::new(py);
    dict.set_item("document", document_metadata_to_py(py, metadata.document)?)?;
    dict.set_item("headers", headers_to_py(py, metadata.headers)?)?;
    dict.set_item("links", links_to_py(py, metadata.links)?)?;
    dict.set_item("images", images_to_py(py, metadata.images)?)?;
    dict.set_item("structured_data", structured_data_to_py(py, metadata.structured_data)?)?;
    Ok(dict.into())
}
