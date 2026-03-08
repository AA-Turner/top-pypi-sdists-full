use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Deserialize)]
pub struct Config {
    pub manifest: Manifest,
    pub s3_config: S3Config,
    pub mountpoint: String,
    pub cache_dir: String,
}

#[derive(Debug, Deserialize)]
pub struct Manifest {
    pub entries: Vec<FileEntry>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct FileEntry {
    pub relpath: String,
    pub md5: String,
    #[serde(default)]
    pub size: u64,
    #[serde(default)]
    pub isexec: bool,
    #[serde(default)]
    pub islink: bool,
    #[serde(default)]
    pub symlink_target: String,
}

#[derive(Debug, Deserialize)]
pub struct S3Config {
    pub bucket: String,
    pub prefix: String,
    pub credentials: HashMap<String, String>,
}

impl S3Config {
    pub fn cache_prefix(&self) -> String {
        format!("{}/dvc-cache/files/md5", self.prefix)
    }

    pub fn file_key(&self, md5: &str) -> String {
        assert!(
            md5.len() >= 2,
            "md5 hash must be at least 2 characters, got: {md5:?}"
        );
        format!("{}/{}/{}", self.cache_prefix(), &md5[..2], &md5[2..])
    }
}

impl Config {
    pub fn from_file(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let data = std::fs::read_to_string(path)?;
        let config: Config = serde_json::from_str(&data)?;
        Ok(config)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_config() {
        let json = r#"{
            "manifest": {
                "entries": [
                    {"relpath": "foo/bar.txt", "md5": "abc123", "size": 100},
                    {"relpath": "link.txt", "md5": "def456", "size": 50, "islink": true, "symlink_target": "../target"}
                ],
                "manifest_md5": "manifest123"
            },
            "s3_config": {
                "bucket": "my-bucket",
                "prefix": "workspace-repos/repo-1",
                "credentials": {"AWS_ACCESS_KEY_ID": "key", "AWS_SECRET_ACCESS_KEY": "secret"}
            },
            "mountpoint": "/mnt/test",
            "cache_dir": "/tmp/cache"
        }"#;
        let config: Config = serde_json::from_str(json).unwrap();
        assert_eq!(config.manifest.entries.len(), 2);
        assert_eq!(config.manifest.entries[0].relpath, "foo/bar.txt");
        assert_eq!(config.manifest.entries[1].islink, true);
        assert_eq!(config.manifest.entries[1].symlink_target, "../target");
        assert_eq!(
            config.s3_config.file_key("abcdef"),
            "workspace-repos/repo-1/dvc-cache/files/md5/ab/cdef"
        );
    }

    #[test]
    fn test_empty_manifest() {
        let json = r#"{
            "manifest": {"entries": [], "manifest_md5": ""},
            "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
            "mountpoint": "/mnt/test",
            "cache_dir": "/tmp/cache"
        }"#;
        let config: Config = serde_json::from_str(json).unwrap();
        assert_eq!(config.manifest.entries.len(), 0);
    }

    #[test]
    #[should_panic(expected = "md5 hash must be at least 2 characters")]
    fn test_file_key_rejects_short_md5() {
        let s3 = S3Config {
            bucket: "bucket".to_string(),
            prefix: "prefix".to_string(),
            credentials: HashMap::new(),
        };

        let _ = s3.file_key("a");
    }
}
