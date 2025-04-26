#[derive(Debug, Clone)]
pub struct DocumentSource {
    pub source: String,
    pub version: i32,
}

impl DocumentSource {
    pub fn new(source: impl Into<String>, version: i32) -> Self {
        let source = source.into();
        Self { source, version }
    }
}
