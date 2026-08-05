const MAX_REQUEST_PATH_LENGTH: usize = 64;

const DOWNLOAD_CONFIG_SPECS_ENDPOINT: &str = "download_config_specs";
const GET_ID_LISTS_ENDPOINT: &str = "get_id_lists";
const DOWNLOAD_ID_LIST_FILE_ENDPOINT: &str = "download_id_list_file";
const LOG_EVENT_ENDPOINT: &str = "log_event";

// StatsigOptions accepts client-provided endpoint strings for compatibility.
// Parse those strings here, then normalize SDK-owned endpoint forms centrally.
pub(crate) const DEFAULT_CDN_URL: &str = "https://statsigcdn.openai.com";
pub(crate) const DEFAULT_CDN_SPECS_URL: &str =
    "https://statsigcdn.openai.com/v2/download_config_specs";
pub(crate) const DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX: &str =
    "https://statsigcdn.openai.com/v1/get_id_lists";

struct StatsigUrl<'a> {
    raw_url: &'a str,
    scheme: Option<&'a str>,
    host: Option<&'a str>,
    host_prefix: &'a str,
    path: &'a str,
}

impl<'a> StatsigUrl<'a> {
    fn new(url: &'a str) -> Self {
        if let Some((scheme, after_scheme)) = url.split_once("://") {
            let authority_end = after_scheme
                .find(['/', '?', '#'])
                .unwrap_or(after_scheme.len());
            let host = &after_scheme[..authority_end];
            let host_prefix = &url[..scheme.len() + 3 + authority_end];
            let path = after_scheme[authority_end..].trim_start_matches('/');
            return Self {
                raw_url: url,
                scheme: Some(scheme),
                host: Some(host),
                host_prefix,
                path,
            };
        }

        Self {
            raw_url: url,
            scheme: None,
            host: None,
            host_prefix: "",
            path: url,
        }
    }

    fn path_segments(&self) -> Vec<&str> {
        strip_query_and_fragment(self.path)
            .split('/')
            .filter(|segment| !segment.is_empty())
            .collect()
    }

    fn api_base(&self) -> String {
        if self.host_prefix.is_empty() {
            return self.raw_url.to_string();
        }

        let path_segments = self.path_segments();
        if let Some(version_segment) = path_segments.first().copied() {
            if is_version_segment(version_segment) {
                return join_url(self.host_prefix.trim_end_matches('/'), version_segment);
            }
        }

        self.host_prefix.trim_end_matches('/').to_string()
    }

    fn source_service(&self, path_segments: &[&str]) -> String {
        let source_service_suffix = path_segments.join("/");
        let source_service = if self.host_prefix.is_empty() {
            source_service_suffix
        } else {
            join_url(
                self.host_prefix.trim_end_matches('/'),
                &source_service_suffix,
            )
        };

        source_service.trim_end_matches('/').to_string()
    }

    fn has_same_origin_host(&self, other: &Self) -> bool {
        match (self.scheme, self.host, other.scheme, other.host) {
            (Some(scheme), Some(host), Some(other_scheme), Some(other_host)) => {
                scheme == other_scheme && host_matches(host, other_host)
            }
            _ => false,
        }
    }
}

fn append_sdk_key_json(url: &str, sdk_key: &str) -> String {
    format!("{}/{sdk_key}.json", url.trim_end_matches('/'))
}

pub(crate) fn config_specs_url(specs_url: &str, sdk_key: &str) -> String {
    append_sdk_key_json(specs_url, sdk_key)
}

pub(crate) fn default_cdn_id_lists_manifest_url(sdk_key: &str) -> String {
    append_sdk_key_json(DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX, sdk_key)
}

pub(crate) fn normalize_default_cdn_id_lists_manifest_url(
    sdk_key: &str,
    id_lists_url: Option<&str>,
) -> String {
    // Some SDK adapters pass the default CDN manifest prefix as id_lists_url.
    // Append the SDK key before trying to fetch it as a CDN manifest.
    match id_lists_url {
        Some(url) if !is_default_cdn_id_lists_manifest_url_prefix(url) => url.to_string(),
        _ => default_cdn_id_lists_manifest_url(sdk_key),
    }
}

pub(crate) fn is_default_cdn_id_lists_manifest_url(url: &str) -> bool {
    has_url_prefix(url, DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX)
}

pub(crate) fn is_default_cdn_url(url: &str) -> bool {
    has_url_prefix(url, DEFAULT_CDN_URL)
}

pub(crate) fn replace_url_base(base_url: &str, url: &str) -> String {
    let parsed_url = StatsigUrl::new(url);
    if parsed_url.path.is_empty() {
        return base_url.to_string();
    }

    join_url(base_url, parsed_url.path)
}

#[cfg(any(test, not(feature = "custom_network_provider")))]
pub(crate) fn url_path_has_suffix(url: &str, expected_suffix: &[&str]) -> bool {
    StatsigUrl::new(url)
        .path_segments()
        .ends_with(expected_suffix)
}

pub(crate) fn api_from_url(url: &str) -> String {
    StatsigUrl::new(url).api_base()
}

pub(crate) fn should_log_network_request_latency(url: &str) -> bool {
    get_version_and_endpoint_for_latency(&StatsigUrl::new(url).path_segments()).is_some()
}

pub(crate) fn get_source_service_and_request_path(url: &str) -> (String, String) {
    let parsed_url = StatsigUrl::new(url);
    let segments = parsed_url.path_segments();

    if let Some((version_index, version_segment, endpoint_segment)) =
        get_version_and_endpoint_for_latency(&segments)
    {
        return (
            parsed_url.source_service(&segments[..version_index]),
            format!("/{version_segment}/{endpoint_segment}"),
        );
    }

    let fallback_request_path: String = strip_query_and_fragment(parsed_url.path)
        .trim_start_matches('/')
        .chars()
        .take(MAX_REQUEST_PATH_LENGTH)
        .collect();
    let request_path = if fallback_request_path.is_empty() {
        "/".to_string()
    } else {
        format!("/{fallback_request_path}")
    };

    (parsed_url.source_service(&[]), request_path)
}

fn get_version_and_endpoint_for_latency<'a>(
    segments: &'a [&'a str],
) -> Option<(usize, &'a str, &'a str)> {
    segments
        .iter()
        .enumerate()
        .find_map(|(endpoint_index, endpoint_segment)| {
            if !is_latency_loggable_endpoint(endpoint_segment) || endpoint_index == 0 {
                return None;
            }

            let version_index = endpoint_index - 1;
            let version_segment = segments[version_index];
            is_version_segment(version_segment).then_some((
                version_index,
                version_segment,
                *endpoint_segment,
            ))
        })
}

fn is_latency_loggable_endpoint(endpoint: &str) -> bool {
    endpoint == DOWNLOAD_CONFIG_SPECS_ENDPOINT
        || endpoint == GET_ID_LISTS_ENDPOINT
        || endpoint == DOWNLOAD_ID_LIST_FILE_ENDPOINT
        || endpoint == LOG_EVENT_ENDPOINT
}

fn has_url_prefix(url: &str, prefix: &str) -> bool {
    let parsed_url = StatsigUrl::new(url);
    let parsed_prefix = StatsigUrl::new(prefix);
    if parsed_url.has_same_origin_host(&parsed_prefix) {
        return has_path_prefix(parsed_url.path, parsed_prefix.path);
    }

    let Some(suffix) = url.strip_prefix(prefix) else {
        return false;
    };

    suffix.is_empty()
        || suffix.starts_with('/')
        || suffix.starts_with('?')
        || suffix.starts_with('#')
}

fn has_path_prefix(path: &str, prefix_path: &str) -> bool {
    let path = strip_query_and_fragment(path).trim_end_matches('/');
    let prefix_path = strip_query_and_fragment(prefix_path).trim_end_matches('/');
    if prefix_path.is_empty() {
        return true;
    }

    let Some(suffix) = path.strip_prefix(prefix_path) else {
        return false;
    };

    suffix.is_empty() || suffix.starts_with('/')
}

fn host_matches(host: &str, expected_host: &str) -> bool {
    host == expected_host
        || host
            .strip_prefix(expected_host)
            .is_some_and(|suffix| suffix == ":443")
}

fn join_url(base_url: &str, path: &str) -> String {
    let path = path.trim_start_matches('/');
    if path.is_empty() {
        return base_url.trim_end_matches('/').to_string();
    }

    format!("{}/{}", base_url.trim_end_matches('/'), path)
}

fn strip_query_and_fragment(path: &str) -> &str {
    let no_query = path.split_once('?').map(|(path, _)| path).unwrap_or(path);
    no_query
        .split_once('#')
        .map(|(path, _)| path)
        .unwrap_or(no_query)
}

fn is_default_cdn_id_lists_manifest_url_prefix(url: &str) -> bool {
    let parsed_url = StatsigUrl::new(url);
    let parsed_prefix = StatsigUrl::new(DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX);

    parsed_url.has_same_origin_host(&parsed_prefix)
        && parsed_url.path.trim_end_matches('/') == parsed_prefix.path
}

fn is_version_segment(segment: &str) -> bool {
    segment.len() > 1
        && segment.starts_with('v')
        && segment[1..]
            .chars()
            .all(|character| character.is_ascii_digit())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_url_path_has_suffix() {
        assert!(url_path_has_suffix(
            "https://api.example.com/v1/log_event",
            &["v1", "log_event"]
        ));
        assert!(url_path_has_suffix(
            "https://api.example.com/prefix/v1/log_event?foo=bar",
            &["v1", "log_event"]
        ));
        assert!(url_path_has_suffix(
            "https://api.example.com/v1/log_event/",
            &["v1", "log_event"]
        ));

        assert!(!url_path_has_suffix(
            "https://api.example.com/v1/log_event/extra",
            &["v1", "log_event"]
        ));
        assert!(!url_path_has_suffix(
            "https://api.example.com/v1/log_events",
            &["v1", "log_event"]
        ));
    }

    #[test]
    fn test_api_from_url() {
        assert_eq!(
            api_from_url("http://localhost:8080/v1/endpoint"),
            "http://localhost:8080/v1"
        );
        assert_eq!(
            api_from_url("http://localhost:8080/v2/download_config_specs"),
            "http://localhost:8080/v2"
        );
        assert_eq!(
            api_from_url("http://localhost:8080"),
            "http://localhost:8080"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v1/specs"),
            "https://api.example.com/v1"
        );
        assert_eq!(
            api_from_url("https://api.oaistatsig.com/v1/get_id_lists"),
            "https://api.oaistatsig.com/v1"
        );
        assert_eq!(
            api_from_url("https://statsigcdn.openai.com/v1/download_id_list_file"),
            "https://statsigcdn.openai.com/v1"
        );
        assert_eq!(
            api_from_url("https://api.oaistatsig.com/get_id_lists"),
            "https://api.oaistatsig.com"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v10/specs"),
            "https://api.example.com/v10"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v1beta/specs"),
            "https://api.example.com"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v1/specs?x=1"),
            "https://api.example.com/v1"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v1/specs#frag"),
            "https://api.example.com/v1"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v1/foo/v2/bar"),
            "https://api.example.com/v1"
        );
        assert_eq!(
            api_from_url("http://[::1]:8080/v1/specs"),
            "http://[::1]:8080/v1"
        );
        assert_eq!(
            api_from_url("https://api.example.com/v1/"),
            "https://api.example.com/v1"
        );
        assert_eq!(api_from_url(""), "");
    }

    #[test]
    fn test_replace_url_base_preserves_path() {
        assert_eq!(
            replace_url_base(
                "https://download-proxy.example",
                "https://fake-id-list-host/v1/download_id_list_file/3wHgh0FhoQH0p"
            ),
            "https://download-proxy.example/v1/download_id_list_file/3wHgh0FhoQH0p"
        );
    }

    #[test]
    fn test_normalize_default_cdn_id_lists_manifest_url() {
        for id_lists_url in [
            None,
            Some(DEFAULT_CDN_ID_LISTS_MANIFEST_URL_PREFIX),
            Some("https://statsigcdn.openai.com/v1/get_id_lists/"),
            Some("https://statsigcdn.openai.com:443/v1/get_id_lists"),
            Some("https://statsigcdn.openai.com:443/v1/get_id_lists/"),
        ] {
            assert_eq!(
                normalize_default_cdn_id_lists_manifest_url("secret-test", id_lists_url),
                "https://statsigcdn.openai.com/v1/get_id_lists/secret-test.json",
                "failed to normalize {id_lists_url:?}"
            );
        }
    }

    #[test]
    fn test_preserve_client_id_lists_manifest_url() {
        for id_lists_url in [
            "https://api.oaistatsig.com/v1/get_id_lists",
            "https://statsigcdn.openai.com/v1/get_id_lists/secret-existing.json",
            "https://statsigcdn.openai.com/v1/get_id_lists#custom",
            "https://statsigcdn.openai.com:8443/v1/get_id_lists",
            "https://statsigcdn.openai.com:443@proxy.example/v1/get_id_lists",
        ] {
            assert_eq!(
                normalize_default_cdn_id_lists_manifest_url("secret-test", Some(id_lists_url)),
                id_lists_url,
                "unexpectedly rewrote {id_lists_url}"
            );
        }
    }

    #[test]
    fn test_preserve_query_bearing_default_cdn_id_lists_manifest_url() {
        let id_lists_url = "https://statsigcdn.openai.com/v1/get_id_lists?token=x";

        assert_eq!(
            normalize_default_cdn_id_lists_manifest_url("secret-test", Some(id_lists_url)),
            id_lists_url
        );
        assert!(is_default_cdn_id_lists_manifest_url(id_lists_url));
    }

    #[test]
    fn test_default_cdn_url_accepts_only_trusted_https_authority() {
        for url in [
            "https://statsigcdn.openai.com/v1/download_id_list_file/list-id",
            "https://statsigcdn.openai.com:443/v1/download_id_list_file/list-id",
        ] {
            assert!(is_default_cdn_url(url), "failed to recognize {url}");
        }

        for url in [
            "https://statsigcdn.openai.com.evil/v1/download_id_list_file/list-id",
            "https://statsigcdn.openai.com:443@evil.example/v1/download_id_list_file/list-id",
            "https://statsigcdn.openai.com:8443/v1/download_id_list_file/list-id",
            "http://statsigcdn.openai.com/v1/download_id_list_file/list-id",
        ] {
            assert!(!is_default_cdn_url(url), "incorrectly trusted {url}");
        }
    }

    #[test]
    fn test_default_cdn_manifest_url_requires_trusted_host_and_path() {
        for url in [
            "https://statsigcdn.openai.com/v1/get_id_lists/secret-test.json",
            "https://statsigcdn.openai.com:443/v1/get_id_lists/secret-test.json",
        ] {
            assert!(
                is_default_cdn_id_lists_manifest_url(url),
                "failed to recognize {url}"
            );
        }

        for url in [
            "https://statsigcdn.openai.com/v1/get_id_lists_extra/secret-test.json",
            "https://statsigcdn.openai.com.evil/v1/get_id_lists/secret-test.json",
            "https://statsigcdn.openai.com:443@evil.example/v1/get_id_lists/secret-test.json",
            "https://statsigcdn.openai.com:8443/v1/get_id_lists/secret-test.json",
        ] {
            assert!(
                !is_default_cdn_id_lists_manifest_url(url),
                "incorrectly trusted {url}"
            );
        }
    }

    #[test]
    fn test_config_specs_url_normalizes_trailing_slash() {
        for specs_url in [
            "https://statsigcdn.openai.com/v2/download_config_specs",
            "https://statsigcdn.openai.com/v2/download_config_specs/",
        ] {
            assert_eq!(
                config_specs_url(specs_url, "secret-test"),
                "https://statsigcdn.openai.com/v2/download_config_specs/secret-test.json"
            );
        }
    }
}
