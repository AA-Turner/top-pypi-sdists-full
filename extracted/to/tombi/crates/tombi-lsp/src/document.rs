#[derive(Debug, Clone)]
pub struct DocumentSource {
    pub text: String,
    pub version: i32,
}

impl DocumentSource {
    pub fn new(text: impl Into<String>, version: i32) -> Self {
        Self {
            text: text.into(),
            version,
        }
    }
}
