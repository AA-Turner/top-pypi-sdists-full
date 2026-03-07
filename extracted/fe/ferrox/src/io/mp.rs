//! Materials Project data access — API client and S3 open-data client.
//!
//! Two complementary clients:
//! - [`MPRester`]: authenticated API client with parallel paginated search
//! - [`MPOpenData`]: key-free S3 bulk download with client-side filtering

use std::collections::HashSet;
use std::io::{BufRead, BufReader};

use flate2::read::GzDecoder;
use serde_json::Value;

#[cfg(feature = "mp")]
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};

#[cfg(feature = "rayon")]
use rayon::prelude::*;

#[cfg(feature = "mp")]
const MP_API_BASE: &str = "https://api.materialsproject.org";
#[cfg(feature = "mp")]
const BUILD_BUCKET: &str = "https://materialsproject-build.s3.amazonaws.com";
#[cfg(feature = "mp")]
const PARSED_BUCKET: &str = "https://materialsproject-parsed.s3.amazonaws.com";
#[cfg(feature = "mp")]
const S3_NS: &str = "http://s3.amazonaws.com/doc/2006-03-01/";

/// Errors specific to Materials Project data access.
#[cfg(feature = "mp")]
#[derive(Debug, thiserror::Error)]
pub enum MpError {
    /// HTTP-level error.
    #[error("HTTP {status}: {message}")]
    Http {
        /// HTTP status code
        status: u16,
        /// Human-readable error message
        message: String,
    },
    /// Network / transport error.
    #[error("Network error: {0}")]
    Network(String),
    /// XML parsing error from S3 list response.
    #[error("XML parse error: {0}")]
    Xml(String),
    /// No data files found for a collection.
    #[error(
        "No data files for collection '{collection}' (version '{version}'). Available: {available:?}"
    )]
    NoData {
        /// Requested collection name
        collection: String,
        /// Database version
        version: String,
        /// Collections that do exist
        available: Vec<String>,
    },
    /// No versions found on S3.
    #[error("No collection versions found on S3")]
    NoVersions,
}

/// Client-side filters applied to each document during search.
#[derive(Debug, Clone, Default)]
pub struct SearchFilter {
    /// Chemical system(s), comma-separated. Subsystem matching: a document's
    /// elements must be a subset of at least one system's element set.
    pub chemsys: Option<Vec<HashSet<String>>>,
    /// Required elements — document must contain all of these.
    pub elements: Option<HashSet<String>>,
    /// Excluded elements — document must contain none of these.
    pub exclude_elements: Option<HashSet<String>>,
    /// Allowed material IDs.
    pub material_ids: Option<HashSet<String>>,
    /// Exact match on `formula_pretty`.
    pub formula: Option<String>,
    /// Upper bound on `energy_above_hull`.
    pub energy_above_hull_max: Option<f64>,
    /// Band gap range.
    pub band_gap_min: Option<f64>,
    /// Band gap upper bound.
    pub band_gap_max: Option<f64>,
    /// Minimum number of sites.
    pub nsites_min: Option<u64>,
    /// Maximum number of sites.
    pub nsites_max: Option<u64>,
    /// Generic exact-match filters: `doc[key] == value`.
    pub match_fields: Vec<(String, Value)>,
}

impl SearchFilter {
    /// Parse a chemsys string like `"Li-Fe-O"` or `"Li-Fe-O,Si-O"` into sets.
    pub fn parse_chemsys(chemsys: &str) -> Vec<HashSet<String>> {
        chemsys
            .split(',')
            .map(|cs| cs.trim().split('-').map(|e| e.trim().to_owned()).collect())
            .collect()
    }

    /// Check whether a JSON document passes all active filters.
    pub fn matches(&self, doc: &Value) -> bool {
        if let Some(ref systems) = self.chemsys {
            match Self::extract_elements(doc) {
                Some(ref doc_elems) if !doc_elems.is_empty() => {
                    if !systems.iter().any(|sys| doc_elems.is_subset(sys)) {
                        return false;
                    }
                }
                _ => return false,
            }
        }
        if let Some(ref required) = self.elements {
            match Self::extract_elements(doc) {
                Some(ref doc_elems) => {
                    if !required.is_subset(doc_elems) {
                        return false;
                    }
                }
                None => return false,
            }
        }
        if let Some(ref excluded) = self.exclude_elements {
            if let Some(ref doc_elems) = Self::extract_elements(doc) {
                if !excluded.is_disjoint(doc_elems) {
                    return false;
                }
            }
        }
        if let Some(ref ids) = self.material_ids {
            match doc.get("material_id").and_then(Value::as_str) {
                Some(mid) => {
                    if !ids.contains(mid) {
                        return false;
                    }
                }
                None => return false,
            }
        }
        if let Some(ref formula) = self.formula {
            match doc.get("formula_pretty").and_then(Value::as_str) {
                Some(fp) if fp == formula => {}
                _ => return false,
            }
        }
        if let Some(max) = self.energy_above_hull_max {
            match doc.get("energy_above_hull").and_then(Value::as_f64) {
                Some(val) if val <= max => {}
                _ => return false,
            }
        }
        if let Some(min) = self.band_gap_min {
            match doc.get("band_gap").and_then(Value::as_f64) {
                Some(val) if val >= min => {}
                _ => return false,
            }
        }
        if let Some(max) = self.band_gap_max {
            match doc.get("band_gap").and_then(Value::as_f64) {
                Some(val) if val <= max => {}
                _ => return false,
            }
        }
        if let Some(min) = self.nsites_min {
            match doc.get("nsites").and_then(Value::as_u64) {
                Some(val) if val >= min => {}
                _ => return false,
            }
        }
        if let Some(max) = self.nsites_max {
            match doc.get("nsites").and_then(Value::as_u64) {
                Some(val) if val <= max => {}
                _ => return false,
            }
        }
        for (key, expected) in &self.match_fields {
            match doc.get(key) {
                Some(val) if val == expected => {}
                _ => return false,
            }
        }
        true
    }

    fn extract_elements(doc: &Value) -> Option<HashSet<String>> {
        doc.get("elements").and_then(Value::as_array).map(|arr| {
            arr.iter()
                .filter_map(Value::as_str)
                .map(String::from)
                .collect()
        })
    }
}

/// Select only the requested fields from a JSON document.
fn select_fields(mut doc: Value, fields: &HashSet<String>) -> Value {
    if let Some(obj) = doc.as_object_mut() {
        obj.retain(|key, _| fields.contains(key));
    }
    doc
}

/// Process JSONL lines from a reader, applying filter and field selection.
///
/// Works with any `BufRead` source — plain text, gzip-decompressed stream, etc.
pub fn process_jsonl_reader(
    reader: impl BufRead,
    filter: &SearchFilter,
    fields: Option<&HashSet<String>>,
    limit: Option<usize>,
) -> Vec<Value> {
    let mut results = Vec::new();
    let mut line_buf = String::new();
    let mut buf_reader = reader;

    loop {
        line_buf.clear();
        match buf_reader.read_line(&mut line_buf) {
            Ok(0) | Err(_) => break,
            Ok(_) => {}
        }
        let trimmed = line_buf.trim();
        if trimmed.is_empty() {
            continue;
        }
        let doc: Value = match serde_json::from_str(trimmed) {
            Ok(v) => v,
            Err(_) => continue,
        };
        if !doc.is_object() || !filter.matches(&doc) {
            continue;
        }
        if let Some(cap) = limit {
            if results.len() >= cap {
                break;
            }
        }
        let doc = match fields {
            Some(field_set) => select_fields(doc, field_set),
            None => doc,
        };
        results.push(doc);
    }
    results
}

/// Create a `BufRead` from raw bytes, auto-detecting gzip.
pub fn make_jsonl_reader(data: &[u8], is_gzipped: bool) -> Box<dyn BufRead + '_> {
    if is_gzipped {
        Box::new(BufReader::new(GzDecoder::new(data)))
    } else {
        Box::new(BufReader::new(data))
    }
}

// === HTTP clients (require `mp` feature for ureq + roxmltree) ===

#[cfg(feature = "mp")]
// === MPRester: authenticated API client with parallel pagination ===

/// Materials Project REST API client with parallel paginated search.
///
/// Uses connection pooling (ureq Agent) and parallel page fetches (rayon)
/// for high-throughput queries against `api.materialsproject.org`.
pub struct MPRester {
    api_key: String,
    base_url: String,
    agent: ureq::Agent,
}

impl MPRester {
    /// Create a new API client.
    pub fn new(api_key: String, base_url: Option<String>, timeout_seconds: u64) -> Self {
        let agent: ureq::Agent = ureq::Agent::config_builder()
            .timeout_global(Some(std::time::Duration::from_secs(timeout_seconds)))
            .build()
            .into();
        Self {
            api_key,
            base_url: base_url.unwrap_or_else(|| MP_API_BASE.to_owned()),
            agent,
        }
    }

    /// Send a GET request and return the parsed JSON payload.
    pub fn get(&self, path: &str, params: &[(String, String)]) -> Result<Value, MpError> {
        let sep = if path.starts_with('/') { "" } else { "/" };
        let mut url = format!("{}{sep}{path}", self.base_url);
        if !params.is_empty() {
            url.push('?');
            for (idx, (key, val)) in params.iter().enumerate() {
                if idx > 0 {
                    url.push('&');
                }
                url.push_str(&urlencoded(key));
                url.push('=');
                url.push_str(&urlencoded(val));
            }
        }

        let response = self
            .agent
            .get(&url)
            .header("X-API-KEY", &self.api_key)
            .header("Accept", "application/json")
            .header("User-Agent", "ferrox-mp-client")
            .call()
            .map_err(|err| MpError::Network(format!("{err}")))?;

        let status = response.status().as_u16();
        if status != 200 {
            return Err(MpError::Http {
                status,
                message: format!("API error at {path}"),
            });
        }

        let body = response
            .into_body()
            .with_config()
            .limit(256 * 1024 * 1024)
            .read_to_string()
            .map_err(|err| MpError::Network(format!("Read error: {err}")))?;

        serde_json::from_str(&body)
            .map_err(|err| MpError::Network(format!("JSON parse error: {err}")))
    }

    /// Fetch a single document by ID from an endpoint.
    pub fn get_by_id(&self, path: &str, doc_id: &str) -> Result<Value, MpError> {
        let path = path.trim_end_matches('/');
        self.get(&format!("{path}/{doc_id}"), &[])
    }

    /// Search with parallel paginated fetching.
    ///
    /// When `limit` is set, fires all pages speculatively in parallel without
    /// waiting for the first response. When unlimited, fetches page 0 first
    /// to discover `meta.total_doc`, then fires remaining pages in parallel.
    pub fn search(
        &self,
        path: &str,
        params: &[(String, String)],
        limit: Option<usize>,
        chunk_size: usize,
    ) -> Result<Vec<Value>, MpError> {
        if chunk_size == 0 {
            return Err(MpError::Network("chunk_size must be positive".into()));
        }

        let fetch_page = |offset: usize| -> Result<Vec<Value>, MpError> {
            let mut page_params = params.to_vec();
            page_params.push(("_skip".into(), offset.to_string()));
            page_params.push(("_limit".into(), chunk_size.to_string()));
            let response = self.get(path, &page_params)?;
            extract_data(&response)
        };

        if let Some(cap) = limit {
            // Speculative: fire ALL pages in parallel without waiting for total_doc
            let n_pages = (cap + chunk_size - 1) / chunk_size;
            let offsets: Vec<usize> = (0..n_pages).map(|idx| idx * chunk_size).collect();

            #[cfg(feature = "rayon")]
            let page_results: Vec<Result<Vec<Value>, MpError>> =
                offsets.par_iter().map(|&off| fetch_page(off)).collect();

            #[cfg(not(feature = "rayon"))]
            let page_results: Vec<Result<Vec<Value>, MpError>> =
                offsets.iter().map(|&off| fetch_page(off)).collect();

            let mut all_docs = Vec::with_capacity(cap);
            for result in page_results {
                all_docs.extend(result?);
                if all_docs.len() >= cap {
                    break;
                }
            }
            all_docs.truncate(cap);
            Ok(all_docs)
        } else {
            // No limit: fetch page 0 to discover total, then parallelize the rest
            let first_response = self.get(path, &{
                let mut fp = params.to_vec();
                fp.push(("_skip".into(), "0".into()));
                fp.push(("_limit".into(), chunk_size.to_string()));
                fp
            })?;
            let first_data = extract_data(&first_response)?;
            let total = first_response
                .get("meta")
                .and_then(|m| m.get("total_doc"))
                .and_then(Value::as_u64)
                .unwrap_or(first_data.len() as u64) as usize;

            if first_data.len() >= total {
                return Ok(first_data);
            }

            let fetched = first_data.len();
            let offsets: Vec<usize> = (0..)
                .map(|idx| fetched + idx * chunk_size)
                .take_while(|&off| off < total)
                .collect();

            #[cfg(feature = "rayon")]
            let page_results: Vec<Result<Vec<Value>, MpError>> =
                offsets.par_iter().map(|&off| fetch_page(off)).collect();

            #[cfg(not(feature = "rayon"))]
            let page_results: Vec<Result<Vec<Value>, MpError>> =
                offsets.iter().map(|&off| fetch_page(off)).collect();

            let mut all_docs = first_data;
            for result in page_results {
                all_docs.extend(result?);
            }
            all_docs.truncate(total);
            Ok(all_docs)
        }
    }
}

#[cfg(feature = "mp")]
/// Extract the `data` array from an API response payload.
fn extract_data(response: &Value) -> Result<Vec<Value>, MpError> {
    response
        .get("data")
        .and_then(Value::as_array)
        .map(|arr| arr.to_vec())
        .ok_or_else(|| MpError::Network("Missing 'data' array in API response".into()))
}

#[cfg(feature = "mp")]
// === MPOpenData: key-free S3 bulk download client ===

/// Direct access to Materials Project data on AWS Open Data S3 buckets.
///
/// No API key required.  Downloads gzip-compressed JSONL collection data
/// directly from `s3://materialsproject-build` and applies filters
/// client-side.  Multiple files are fetched in parallel via rayon.
pub struct MPOpenData {
    version: Option<String>,
    timeout_seconds: u64,
    user_agent: String,
}

impl MPOpenData {
    /// Create a new open-data client.
    ///
    /// `version` of `None` auto-detects the latest available version.
    pub fn new(version: Option<String>, timeout_seconds: u64, user_agent: String) -> Self {
        Self {
            version,
            timeout_seconds,
            user_agent,
        }
    }

    /// Resolved database version (auto-detects latest if not set).
    pub fn version(&mut self) -> Result<&str, MpError> {
        if self.version.is_none() {
            let versions = self.list_versions()?;
            let latest = versions
                .into_iter()
                .filter(|v| v.contains('-') && v.chars().next().is_some_and(|c| c.is_ascii_digit()))
                .max()
                .ok_or(MpError::NoVersions)?;
            self.version = Some(latest);
        }
        Ok(self.version.as_ref().unwrap())
    }

    // === S3 transport helpers ===

    fn make_agent(&self) -> ureq::Agent {
        ureq::Agent::config_builder()
            .timeout_global(Some(std::time::Duration::from_secs(self.timeout_seconds)))
            .build()
            .into()
    }

    fn s3_get(&self, url: &str) -> Result<Vec<u8>, MpError> {
        self.s3_get_with_agent(&self.make_agent(), url)
    }

    fn s3_get_with_agent(&self, agent: &ureq::Agent, url: &str) -> Result<Vec<u8>, MpError> {
        let response = agent
            .get(url)
            .header("User-Agent", &self.user_agent)
            .call()
            .map_err(|err| MpError::Network(format!("{err}")))?;

        let status = response.status().as_u16();
        if status != 200 {
            return Err(MpError::Http {
                status,
                message: format!("Unexpected status from {url}"),
            });
        }

        response
            .into_body()
            .with_config()
            .limit(256 * 1024 * 1024) // 256 MB — summary JSONL files can be 30+ MB
            .read_to_vec()
            .map_err(|err| MpError::Network(format!("Read error: {err}")))
    }

    fn s3_list_prefixes(&self, prefix: &str) -> Result<Vec<String>, MpError> {
        self.s3_list_prefixes_in(BUILD_BUCKET, prefix)
    }

    fn s3_list_objects(&self, prefix: &str) -> Result<Vec<(String, usize)>, MpError> {
        let mut results = Vec::new();
        let mut continuation_token: Option<String> = None;

        loop {
            let mut url = format!("{BUILD_BUCKET}?list-type=2&prefix={}", urlencoded(prefix));
            if let Some(ref token) = continuation_token {
                url.push_str(&format!("&continuation-token={}", urlencoded(token)));
            }

            let xml_bytes = self.s3_get(&url)?;
            let xml_str =
                std::str::from_utf8(&xml_bytes).map_err(|e| MpError::Xml(e.to_string()))?;
            let doc =
                roxmltree::Document::parse(xml_str).map_err(|e| MpError::Xml(e.to_string()))?;

            let root = doc.root_element();
            for node in root.children() {
                if node.has_tag_name((S3_NS, "Contents")) {
                    let key = node
                        .children()
                        .find(|c| c.has_tag_name((S3_NS, "Key")))
                        .and_then(|n| n.text())
                        .unwrap_or("")
                        .to_owned();
                    let size: usize = node
                        .children()
                        .find(|c| c.has_tag_name((S3_NS, "Size")))
                        .and_then(|n| n.text())
                        .and_then(|s| s.parse().ok())
                        .unwrap_or(0);
                    if !key.is_empty() {
                        results.push((key, size));
                    }
                }
            }

            if !is_truncated(&root) {
                break;
            }
            continuation_token = next_continuation_token(&root);
            if continuation_token.is_none() {
                break;
            }
        }

        Ok(results)
    }

    // === Public API ===

    /// List available database versions (e.g. `["2022-10-28", "2024-11-14"]`).
    pub fn list_versions(&self) -> Result<Vec<String>, MpError> {
        self.s3_list_prefixes("collections/")
    }

    /// List available collection names for a database version.
    pub fn list_collections(&mut self, version: Option<&str>) -> Result<Vec<String>, MpError> {
        let ver = match version {
            Some(v) => v.to_owned(),
            None => self.version()?.to_owned(),
        };
        self.s3_list_prefixes(&format!("collections/{ver}/"))
    }

    /// Download and filter collection data from S3.
    ///
    /// Fetches gzip-compressed JSONL files from the `materialsproject-build`
    /// bucket and applies all filters client-side. Files are downloaded in
    /// parallel using rayon.
    pub fn search(
        &mut self,
        collection: &str,
        filter: &SearchFilter,
        fields: Option<&HashSet<String>>,
        limit: Option<usize>,
    ) -> Result<Vec<Value>, MpError> {
        if limit == Some(0) {
            return Ok(Vec::new());
        }
        let ver = self.version()?.to_owned();
        let prefix = format!("collections/{ver}/{collection}/");
        let objects = self.s3_list_objects(&prefix)?;

        let data_files: Vec<String> = objects
            .into_iter()
            .filter_map(|(key, _size)| {
                if key.ends_with(".jsonl.gz")
                    || key.ends_with(".jsonl")
                    || key.ends_with(".json.gz")
                    || key.ends_with(".json")
                {
                    Some(key)
                } else {
                    None
                }
            })
            .collect();

        if data_files.is_empty() {
            let available = self.list_collections(Some(&ver))?;
            return Err(MpError::NoData {
                collection: collection.to_owned(),
                version: ver,
                available,
            });
        }

        let done = AtomicBool::new(false);
        let found_count = AtomicUsize::new(0);
        let agent = self.make_agent();

        let process_file = |key: &String| -> Result<Vec<Value>, MpError> {
            if done.load(Ordering::Relaxed) {
                return Ok(Vec::new());
            }

            let url = format!("{BUILD_BUCKET}/{key}");
            let raw = self.s3_get_with_agent(&agent, &url)?;

            let mut results = Vec::new();
            let reader: Box<dyn BufRead> = if key.ends_with(".gz") {
                Box::new(BufReader::new(GzDecoder::new(raw.as_slice())))
            } else {
                Box::new(BufReader::new(raw.as_slice()))
            };

            let mut line_buf = String::new();
            let mut buf_reader = reader;
            loop {
                line_buf.clear();
                match buf_reader.read_line(&mut line_buf) {
                    Ok(0) => break,
                    Ok(_) => {}
                    Err(_) => break,
                }
                let trimmed = line_buf.trim();
                if trimmed.is_empty() {
                    continue;
                }
                let doc: Value = match serde_json::from_str(trimmed) {
                    Ok(v) => v,
                    Err(_) => continue,
                };
                if !doc.is_object() || !filter.matches(&doc) {
                    continue;
                }
                let doc = match fields {
                    Some(ref field_set) => select_fields(doc, field_set),
                    None => doc,
                };
                results.push(doc);

                if let Some(cap) = limit {
                    let total = found_count.fetch_add(1, Ordering::Relaxed) + 1;
                    if total >= cap {
                        done.store(true, Ordering::Relaxed);
                        break;
                    }
                }
            }
            Ok(results)
        };

        #[cfg(feature = "rayon")]
        let file_results: Vec<Result<Vec<Value>, MpError>> =
            data_files.par_iter().map(process_file).collect();

        #[cfg(not(feature = "rayon"))]
        let file_results: Vec<Result<Vec<Value>, MpError>> =
            data_files.iter().map(process_file).collect();

        let mut all_docs = Vec::new();
        for result in file_results {
            all_docs.extend(result?);
        }

        if let Some(cap) = limit {
            all_docs.truncate(cap);
        }

        Ok(all_docs)
    }

    // === Parsed bucket (per-material files: CHGCARs, DOS, bandstructures, etc.) ===

    /// List available data categories in the parsed bucket.
    ///
    /// Returns prefixes like `["bandstructures", "chgcars", "dos", ...]`.
    pub fn list_parsed_categories(&self) -> Result<Vec<String>, MpError> {
        self.s3_list_prefixes_in(PARSED_BUCKET, "")
    }

    /// Download a single parsed document by material ID.
    ///
    /// Files are stored as `{category}/{material_id}.json.gz` in the
    /// `materialsproject-parsed` bucket.
    pub fn get_parsed(&self, category: &str, material_id: &str) -> Result<Value, MpError> {
        let key = format!("{category}/{material_id}.json.gz");
        let url = format!("{PARSED_BUCKET}/{key}");
        let raw = self.s3_get(&url)?;

        let reader = BufReader::new(GzDecoder::new(raw.as_slice()));
        serde_json::from_reader(reader)
            .map_err(|err| MpError::Network(format!("JSON parse error for {key}: {err}")))
    }

    /// Download multiple parsed documents in parallel.
    ///
    /// Returns a vec of `(material_id, doc)` pairs for successful downloads.
    /// Failed downloads are silently skipped (use [`get_parsed`] for
    /// per-document error handling).
    ///
    /// If `progress` is provided, it is incremented (atomically) after each
    /// file completes, enabling external progress tracking.
    pub fn get_parsed_batch(
        &self,
        category: &str,
        material_ids: &[String],
        progress: Option<&AtomicUsize>,
    ) -> Result<Vec<(String, Value)>, MpError> {
        let agent = self.make_agent();

        let fetch_one = |mid: &String| -> Option<(String, Value)> {
            let key = format!("{category}/{mid}.json.gz");
            let url = format!("{PARSED_BUCKET}/{key}");
            let raw = self.s3_get_with_agent(&agent, &url).ok()?;
            let reader = BufReader::new(GzDecoder::new(raw.as_slice()));
            let doc: Value = serde_json::from_reader(reader).ok()?;
            if let Some(counter) = progress {
                counter.fetch_add(1, Ordering::Relaxed);
            }
            Some((mid.clone(), doc))
        };

        #[cfg(feature = "rayon")]
        let results: Vec<(String, Value)> = material_ids.par_iter().filter_map(fetch_one).collect();

        #[cfg(not(feature = "rayon"))]
        let results: Vec<(String, Value)> = material_ids.iter().filter_map(fetch_one).collect();

        Ok(results)
    }

    /// S3 list prefixes in an arbitrary bucket.
    fn s3_list_prefixes_in(&self, bucket_url: &str, prefix: &str) -> Result<Vec<String>, MpError> {
        let mut results = Vec::new();
        let mut continuation_token: Option<String> = None;

        loop {
            let mut url = format!(
                "{bucket_url}?list-type=2&prefix={}&delimiter=/",
                urlencoded(prefix)
            );
            if let Some(ref token) = continuation_token {
                url.push_str(&format!("&continuation-token={}", urlencoded(token)));
            }

            let xml_bytes = self.s3_get(&url)?;
            let xml_str =
                std::str::from_utf8(&xml_bytes).map_err(|err| MpError::Xml(err.to_string()))?;
            let doc =
                roxmltree::Document::parse(xml_str).map_err(|err| MpError::Xml(err.to_string()))?;

            let root = doc.root_element();
            for node in root.children() {
                if node.has_tag_name((S3_NS, "CommonPrefixes")) {
                    if let Some(pfx_node) = node
                        .children()
                        .find(|child| child.has_tag_name((S3_NS, "Prefix")))
                    {
                        if let Some(pfx_text) = pfx_node.text() {
                            let name = pfx_text
                                .strip_prefix(prefix)
                                .unwrap_or(pfx_text)
                                .trim_end_matches('/');
                            if !name.is_empty() {
                                results.push(name.to_owned());
                            }
                        }
                    }
                }
            }

            if !is_truncated(&root) {
                break;
            }
            continuation_token = next_continuation_token(&root);
            if continuation_token.is_none() {
                break;
            }
        }

        results.sort();
        Ok(results)
    }
}

#[cfg(feature = "mp")]
// === XML helpers ===
#[cfg(feature = "mp")]
fn is_truncated(root: &roxmltree::Node) -> bool {
    root.children()
        .find(|c| c.has_tag_name((S3_NS, "IsTruncated")))
        .and_then(|n| n.text())
        .is_some_and(|t| t.eq_ignore_ascii_case("true"))
}

#[cfg(feature = "mp")]
fn next_continuation_token(root: &roxmltree::Node) -> Option<String> {
    root.children()
        .find(|c| c.has_tag_name((S3_NS, "NextContinuationToken")))
        .and_then(|n| n.text())
        .map(String::from)
}

#[cfg(feature = "mp")]
/// Minimal percent-encoding for query parameters.
fn urlencoded(input: &str) -> String {
    let mut out = String::with_capacity(input.len());
    for byte in input.bytes() {
        match byte {
            b'A'..=b'Z' | b'a'..=b'z' | b'0'..=b'9' | b'-' | b'_' | b'.' | b'~' => {
                out.push(byte as char);
            }
            _ => {
                out.push_str(&format!("%{byte:02X}"));
            }
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_doc(elements: &[&str], extra: Vec<(&str, Value)>) -> Value {
        let mut map = serde_json::Map::new();
        map.insert(
            "elements".into(),
            Value::Array(
                elements
                    .iter()
                    .map(|e| Value::String(e.to_string()))
                    .collect(),
            ),
        );
        for (key, val) in extra {
            map.insert(key.into(), val);
        }
        Value::Object(map)
    }

    #[test]
    fn empty_filter_accepts_all() {
        let filter = SearchFilter::default();
        let doc = make_doc(&["Si"], vec![]);
        assert!(filter.matches(&doc));
    }

    #[test]
    fn chemsys_subsystem_matching() {
        let filter = SearchFilter {
            chemsys: Some(SearchFilter::parse_chemsys("Li-Fe-O")),
            ..Default::default()
        };
        // Exact match
        assert!(filter.matches(&make_doc(&["Li", "Fe", "O"], vec![])));
        // Subsystem
        assert!(filter.matches(&make_doc(&["Li", "O"], vec![])));
        // Unary
        assert!(filter.matches(&make_doc(&["Fe"], vec![])));
        // Superset should fail
        assert!(!filter.matches(&make_doc(&["Li", "Fe", "O", "S"], vec![])));
    }

    #[test]
    fn chemsys_comma_separated() {
        let filter = SearchFilter {
            chemsys: Some(SearchFilter::parse_chemsys("Si,Ge-O")),
            ..Default::default()
        };
        assert!(filter.matches(&make_doc(&["Si"], vec![])));
        assert!(filter.matches(&make_doc(&["Ge", "O"], vec![])));
        assert!(filter.matches(&make_doc(&["Ge"], vec![])));
        assert!(!filter.matches(&make_doc(&["Si", "O"], vec![])));
    }

    #[test]
    fn elements_filter() {
        let filter = SearchFilter {
            elements: Some(["Li", "O"].iter().map(|s| s.to_string()).collect()),
            ..Default::default()
        };
        assert!(filter.matches(&make_doc(&["Li", "Fe", "O"], vec![])));
        assert!(!filter.matches(&make_doc(&["Li", "Fe"], vec![])));
    }

    #[test]
    fn exclude_elements_filter() {
        let filter = SearchFilter {
            exclude_elements: Some(["Pb", "Cd"].iter().map(|s| s.to_string()).collect()),
            ..Default::default()
        };
        assert!(filter.matches(&make_doc(&["Li", "O"], vec![])));
        assert!(!filter.matches(&make_doc(&["Li", "Pb"], vec![])));
    }

    #[test]
    fn material_ids_filter() {
        let filter = SearchFilter {
            material_ids: Some(["mp-149", "mp-13"].iter().map(|s| s.to_string()).collect()),
            ..Default::default()
        };
        let pass = make_doc(
            &["Si"],
            vec![("material_id", Value::String("mp-149".into()))],
        );
        let fail = make_doc(
            &["Si"],
            vec![("material_id", Value::String("mp-999".into()))],
        );
        assert!(filter.matches(&pass));
        assert!(!filter.matches(&fail));
    }

    #[test]
    fn numeric_range_filters() {
        let filter = SearchFilter {
            band_gap_min: Some(1.0),
            band_gap_max: Some(3.0),
            nsites_min: Some(2),
            nsites_max: Some(10),
            energy_above_hull_max: Some(0.1),
            ..Default::default()
        };
        let pass = make_doc(
            &["Si"],
            vec![
                ("band_gap", Value::from(2.0)),
                ("nsites", Value::from(5)),
                ("energy_above_hull", Value::from(0.05)),
            ],
        );
        assert!(filter.matches(&pass));

        let fail_bg = make_doc(
            &["Si"],
            vec![
                ("band_gap", Value::from(5.0)),
                ("nsites", Value::from(5)),
                ("energy_above_hull", Value::from(0.05)),
            ],
        );
        assert!(!filter.matches(&fail_bg));
    }

    #[test]
    fn match_fields_exact_equality() {
        let filter = SearchFilter {
            match_fields: vec![
                ("is_stable".into(), Value::Bool(true)),
                ("crystal_system".into(), Value::String("cubic".into())),
            ],
            ..Default::default()
        };
        let pass = make_doc(
            &["Si"],
            vec![
                ("is_stable", Value::Bool(true)),
                ("crystal_system", Value::String("cubic".into())),
            ],
        );
        assert!(filter.matches(&pass));

        let fail = make_doc(
            &["Si"],
            vec![
                ("is_stable", Value::Bool(false)),
                ("crystal_system", Value::String("cubic".into())),
            ],
        );
        assert!(!filter.matches(&fail));
    }

    #[test]
    fn combined_filters() {
        let filter = SearchFilter {
            chemsys: Some(SearchFilter::parse_chemsys("Li-O")),
            energy_above_hull_max: Some(0.05),
            ..Default::default()
        };
        let pass = make_doc(&["Li", "O"], vec![("energy_above_hull", Value::from(0.01))]);
        assert!(filter.matches(&pass));

        let fail_ehull = make_doc(&["Li", "O"], vec![("energy_above_hull", Value::from(0.1))]);
        assert!(!filter.matches(&fail_ehull));

        let fail_chemsys = make_doc(
            &["Li", "Fe", "O"],
            vec![("energy_above_hull", Value::from(0.01))],
        );
        assert!(!filter.matches(&fail_chemsys));
    }

    #[test]
    fn select_fields_retains_only_requested() {
        let doc = make_doc(
            &["Si"],
            vec![
                ("material_id", Value::String("mp-149".into())),
                ("band_gap", Value::from(1.1)),
            ],
        );
        let fields: HashSet<String> = ["material_id"].iter().map(|s| s.to_string()).collect();
        let filtered = select_fields(doc, &fields);
        let obj = filtered.as_object().unwrap();
        assert!(obj.contains_key("material_id"));
        assert!(!obj.contains_key("elements"));
        assert!(!obj.contains_key("band_gap"));
    }

    #[test]
    #[cfg(feature = "mp")]
    fn urlencoded_special_chars() {
        assert_eq!(urlencoded("hello world"), "hello%20world");
        assert_eq!(urlencoded("a/b"), "a%2Fb");
        assert_eq!(urlencoded("simple"), "simple");
    }
}
