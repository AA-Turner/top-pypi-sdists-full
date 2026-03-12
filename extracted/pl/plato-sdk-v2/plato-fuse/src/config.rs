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
    #[serde(default)]
    pub md5: Option<String>,
    #[serde(default)]
    pub size: u64,
    #[serde(default)]
    pub isexec: bool,
    #[serde(default)]
    pub islink: bool,
    #[serde(default)]
    pub symlink_target: Option<String>,
    #[serde(default)]
    pub isdir: bool,
    #[serde(default)]
    pub mode: Option<u32>,
}

impl FileEntry {
    pub fn is_dir(&self) -> bool {
        self.isdir
    }

    pub fn manifest_mode(&self) -> u32 {
        if self.is_dir() {
            self.mode.unwrap_or(0o755) & 0o777
        } else if self.isexec {
            0o755
        } else {
            0o644
        }
    }
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
                    {"relpath": "link.txt", "md5": "def456", "size": 50, "islink": true, "symlink_target": "../target"},
                    {"relpath": "foo/runtime", "isdir": true, "mode": 448}
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
        assert_eq!(config.manifest.entries.len(), 3);
        assert_eq!(config.manifest.entries[0].relpath, "foo/bar.txt");
        assert_eq!(config.manifest.entries[1].islink, true);
        assert_eq!(
            config.manifest.entries[1].symlink_target.as_deref(),
            Some("../target")
        );
        assert!(config.manifest.entries[2].is_dir());
        assert_eq!(config.manifest.entries[2].manifest_mode(), 0o700);
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

    #[test]
    fn test_parse_legacy_file_entry_defaults() {
        let json = r#"{
            "manifest": {
                "entries": [{"relpath": "foo.txt", "md5": "abc123", "size": 12}],
                "manifest_md5": "manifest123"
            },
            "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
            "mountpoint": "/mnt/test",
            "cache_dir": "/tmp/cache"
        }"#;

        let config: Config = serde_json::from_str(json).unwrap();
        let entry = &config.manifest.entries[0];
        assert!(!entry.is_dir());
        assert_eq!(entry.manifest_mode(), 0o644);
        assert_eq!(entry.md5.as_deref(), Some("abc123"));
    }

    #[test]
    fn test_parse_directory_entry_without_mode_defaults_to_755() {
        let json = r#"{
            "manifest": {
                "entries": [{"relpath": "foo", "isdir": true}],
                "manifest_md5": "manifest123"
            },
            "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
            "mountpoint": "/mnt/test",
            "cache_dir": "/tmp/cache"
        }"#;

        let config: Config = serde_json::from_str(json).unwrap();
        let entry = &config.manifest.entries[0];
        assert!(entry.is_dir());
        assert_eq!(entry.manifest_mode(), 0o755);
        assert_eq!(entry.md5, None);
        assert_eq!(entry.symlink_target, None);
    }

    #[test]
    fn test_parse_symlink_without_target_defaults_to_none() {
        let json = r#"{
            "manifest": {
                "entries": [{"relpath": "link", "md5": "abc123", "islink": true}],
                "manifest_md5": "manifest123"
            },
            "s3_config": {"bucket": "", "prefix": "", "credentials": {}},
            "mountpoint": "/mnt/test",
            "cache_dir": "/tmp/cache"
        }"#;

        let config: Config = serde_json::from_str(json).unwrap();
        let entry = &config.manifest.entries[0];
        assert!(entry.islink);
        assert_eq!(entry.symlink_target, None);
    }
}
