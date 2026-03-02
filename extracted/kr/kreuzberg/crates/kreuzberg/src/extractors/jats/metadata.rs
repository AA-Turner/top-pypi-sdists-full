//! JATS metadata extraction (authors, DOI, dates, journal information).

/// Structure to hold extracted JATS metadata.
#[derive(Debug, Clone, Default)]
pub(super) struct JatsMetadataExtracted {
    pub(super) title: String,
    pub(super) subtitle: Option<String>,
    pub(super) authors: Vec<String>,
    pub(super) affiliations: Vec<String>,
    pub(super) doi: Option<String>,
    pub(super) pii: Option<String>,
    pub(super) keywords: Vec<String>,
    pub(super) publication_date: Option<String>,
    pub(super) volume: Option<String>,
    pub(super) issue: Option<String>,
    pub(super) pages: Option<String>,
    pub(super) journal_title: Option<String>,
    pub(super) article_type: Option<String>,
    pub(super) abstract_text: Option<String>,
    pub(super) corresponding_author: Option<String>,
}
