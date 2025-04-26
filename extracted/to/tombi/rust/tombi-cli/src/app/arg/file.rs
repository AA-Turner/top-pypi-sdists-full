use std::path::PathBuf;

use itertools::Itertools;

const DEFAULT_INCLUDE_PATTERNS: &[&str] = &["**/*.toml"];

/// Input source for TOML files.
///
/// Standard input or file paths. Contains a list of files that match the glob pattern.
#[derive(Debug)]
pub enum FileInput {
    Stdin,
    Files(Vec<Result<PathBuf, crate::Error>>),
}

impl FileInput {
    pub fn new<T: AsRef<str>>(
        files: &[T],
        include_patterns: Option<&[&str]>,
        exclude_patterns: Option<&[&str]>,
    ) -> Self {
        let mut matched_paths = Vec::new();
        let include_patterns = include_patterns.unwrap_or(DEFAULT_INCLUDE_PATTERNS);
        let exclude_patterns = exclude_patterns.unwrap_or_default();
        let exclude_matchers: Vec<glob::Pattern> = exclude_patterns
            .iter()
            .filter_map(|p| match glob::Pattern::new(p) {
                Ok(pattern) => Some(pattern),
                Err(e) => {
                    matched_paths.push(Err(crate::Error::GlobPatternInvalid(e.to_string())));
                    None
                }
            })
            .collect();

        match files.len() {
            0 => {
                tracing::debug!("Searching for TOML files using configured patterns...");
                tracing::debug!("Include patterns: {:?}", include_patterns);
                tracing::debug!("Exclude patterns: {:?}", exclude_patterns);

                for pattern in include_patterns {
                    if let Ok(paths) = glob::glob(pattern) {
                        matched_paths.extend(
                            paths
                                .filter_map(|entry| entry.ok())
                                .filter(|path| {
                                    !exclude_matchers
                                        .iter()
                                        .any(|matcher| matcher.matches_path(path))
                                })
                                .map(Ok)
                                .collect_vec(),
                        );
                    } else {
                        matched_paths
                            .push(Err(crate::Error::GlobPatternInvalid(pattern.to_string())));
                    }
                }

                FileInput::Files(matched_paths)
            }
            1 if files[0].as_ref() == "-" => FileInput::Stdin,
            _ => {
                tracing::debug!("Searching for TOML files using user input patterns...");
                tracing::debug!("Exclude patterns: {:?}", exclude_patterns);

                for file in files {
                    if is_glob_pattern(file.as_ref()) {
                        if let Ok(paths) = glob::glob(file.as_ref()) {
                            matched_paths.extend(
                                paths
                                    .filter_map(|entry| entry.ok())
                                    .filter(|path| {
                                        !exclude_matchers
                                            .iter()
                                            .any(|matcher| matcher.matches_path(path))
                                    })
                                    .map(Ok)
                                    .collect_vec(),
                            );
                        } else {
                            matched_paths
                                .push(Err(crate::Error::GlobPatternInvalid(file.as_ref().into())));
                        }
                    } else {
                        let path = PathBuf::from(file.as_ref());
                        if !path.exists() {
                            matched_paths
                                .push(Err(crate::Error::FileNotFound(file.as_ref().into())));
                        } else {
                            matched_paths.push(Ok(path));
                        }
                    }
                }

                FileInput::Files(matched_paths)
            }
        }
    }

    pub fn len(&self) -> usize {
        match self {
            FileInput::Stdin => 1,
            FileInput::Files(files) => files.len(),
        }
    }
}

fn is_glob_pattern(value: &str) -> bool {
    for c in value.chars() {
        if matches!(c, '*' | '?' | '[' | ']') {
            return true;
        }
    }
    false
}
