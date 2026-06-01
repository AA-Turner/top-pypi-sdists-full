use std::collections::HashMap;
use std::fs;
use std::io;
use std::path::{Component, Path, PathBuf};

use serde::{Deserialize, Serialize};
use thiserror::Error;

pub const DEFAULT_REQUIREMENTS: &str = "pyproject.toml";
pub const DEFAULT_CHALKIGNORE: &str = ".chalkignore";
pub const PROJECT_CONFIG_FILENAMES: [&str; 2] = ["chalk.yaml", "chalk.yml"];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Default)]
pub struct EnvironmentSettings {
    pub runtime: Option<String>,
    pub platform_version: Option<String>,
    pub requirements: Option<String>,
    pub dockerfile: Option<String>,
    #[serde(rename = "chalkignore")]
    pub chalkignore: Option<PathBuf>,
}

impl EnvironmentSettings {
    fn with_fallbacks_from(&self, defaults: &EnvironmentSettings) -> EnvironmentSettings {
        EnvironmentSettings {
            runtime: self.runtime.clone().or_else(|| defaults.runtime.clone()),
            platform_version: self
                .platform_version
                .clone()
                .or_else(|| defaults.platform_version.clone()),
            requirements: self
                .requirements
                .clone()
                .or_else(|| defaults.requirements.clone()),
            dockerfile: self
                .dockerfile
                .clone()
                .or_else(|| defaults.dockerfile.clone()),
            chalkignore: self
                .chalkignore
                .clone()
                .or_else(|| defaults.chalkignore.clone()),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize, Default)]
pub struct ProjectSettings {
    #[serde(default)]
    pub project: String,
    #[serde(default)]
    pub environments: HashMap<String, EnvironmentSettings>,
    #[serde(skip)]
    pub local_directory: PathBuf,
    #[serde(skip)]
    pub filename: PathBuf,
    #[serde(default, rename = "chalkignore")]
    pub chalkignore: Option<PathBuf>,
}

impl ProjectSettings {
    pub fn default_environment_settings(&self) -> Option<&EnvironmentSettings> {
        self.environments.get("default")
    }

    pub fn resolved_environment_settings(
        &self,
        environment_name: Option<&str>,
    ) -> EnvironmentSettings {
        let default_settings = self
            .default_environment_settings()
            .cloned()
            .unwrap_or_default();

        let mut settings = match environment_name.filter(|name| !name.is_empty()) {
            None | Some("default") => default_settings,
            Some(name) => self
                .environments
                .get(name)
                .map(|settings| settings.with_fallbacks_from(&default_settings))
                .unwrap_or(default_settings),
        };

        if settings.chalkignore.is_none() {
            settings.chalkignore = self.chalkignore.clone();
        }

        settings
    }
}

#[derive(Debug, Error)]
pub enum ProjectError {
    #[error(transparent)]
    Io(#[from] io::Error),
    #[error(transparent)]
    Yaml(#[from] serde_yaml::Error),
    #[error("Failed to find chalk.yaml or chalk.yml in this directory or any parent directory.")]
    NotFound,
}

pub fn load_project_config() -> Result<ProjectSettings, ProjectError> {
    find_project_config(std::env::current_dir()?)
}

pub fn find_project_config<P: AsRef<Path>>(start: P) -> Result<ProjectSettings, ProjectError> {
    let mut current = normalize_path(&absolutize(start.as_ref())?);

    loop {
        for filename in PROJECT_CONFIG_FILENAMES {
            if let Some(settings) = check_directory(&current, filename)? {
                return Ok(settings);
            }
        }
        if !current.pop() {
            break;
        }
    }

    Err(ProjectError::NotFound)
}

pub fn load_project_config_from_root<P: AsRef<Path>>(
    root: P,
) -> Result<ProjectSettings, ProjectError> {
    let root = normalize_path(&absolutize(root.as_ref())?);

    for filename in PROJECT_CONFIG_FILENAMES {
        if let Some(settings) = check_directory(&root, filename)? {
            return Ok(settings);
        }
    }

    Err(ProjectError::NotFound)
}

pub fn check_directory<P: AsRef<Path>>(
    directory: P,
    filename: &str,
) -> Result<Option<ProjectSettings>, ProjectError> {
    let directory = normalize_path(&absolutize(directory.as_ref())?);
    let config_filename = directory.join(filename);
    if !config_filename.exists() {
        return Ok(None);
    }

    let has_default_requirements = directory.join(DEFAULT_REQUIREMENTS).exists();
    let contents = fs::read_to_string(&config_filename)?;

    let mut settings: ProjectSettings = serde_yaml::from_str(&contents)?;
    settings.local_directory = directory.clone();
    settings.filename = config_filename;

    let project_chalkignore =
        resolve_project_chalkignore(&directory, settings.chalkignore.as_deref());

    for environment in settings.environments.values_mut() {
        if environment
            .requirements
            .as_deref()
            .is_none_or(str::is_empty)
            && has_default_requirements
        {
            environment.requirements = Some(DEFAULT_REQUIREMENTS.to_owned());
        }

        environment.chalkignore = match environment.chalkignore.as_deref() {
            Some(path) if !path.as_os_str().is_empty() => {
                Some(resolve_explicit_path(&directory, path))
            }
            _ => project_chalkignore.clone(),
        };
    }

    settings.chalkignore = project_chalkignore;

    Ok(Some(settings))
}

fn resolve_project_chalkignore(directory: &Path, configured: Option<&Path>) -> Option<PathBuf> {
    let candidate = match configured {
        Some(path) if !path.as_os_str().is_empty() => resolve_explicit_path(directory, path),
        _ => directory.join(DEFAULT_CHALKIGNORE),
    };

    candidate.exists().then_some(candidate)
}

fn resolve_explicit_path(directory: &Path, path: &Path) -> PathBuf {
    if path.is_absolute() {
        normalize_path(path)
    } else {
        normalize_path(&directory.join(path))
    }
}

fn absolutize(path: &Path) -> io::Result<PathBuf> {
    if path.is_absolute() {
        Ok(path.to_path_buf())
    } else {
        Ok(std::env::current_dir()?.join(path))
    }
}

fn normalize_path(path: &Path) -> PathBuf {
    let mut normalized = PathBuf::new();

    for component in path.components() {
        match component {
            Component::Prefix(prefix) => normalized.push(prefix.as_os_str()),
            Component::RootDir => normalized.push(component.as_os_str()),
            Component::CurDir => {}
            Component::ParentDir => {
                normalized.pop();
            }
            Component::Normal(part) => normalized.push(part),
        }
    }

    if normalized.as_os_str().is_empty() {
        PathBuf::from(".")
    } else {
        normalized
    }
}

#[cfg(test)]
mod tests {
    use super::{
        check_directory, find_project_config, load_project_config_from_root, EnvironmentSettings,
        ProjectSettings, DEFAULT_REQUIREMENTS,
    };
    use std::fs;
    use std::path::Path;

    use tempfile::TempDir;

    fn write_file(root: &Path, relative_path: &str, contents: &str) {
        let path = root.join(relative_path);
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).unwrap();
        }
        fs::write(path, contents).unwrap();
    }

    #[test]
    fn resolves_environment_specific_chalkignores() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(
            root,
            "chalk.yaml",
            r#"project: test-project
environments:
  dev:
    runtime: python312
    chalkignore: .chalkignore.dev
  prod:
    runtime: python312
    chalkignore: .chalkignore.prod
  default:
    runtime: python312
"#,
        );
        write_file(root, ".chalkignore.dev", "dev_specific\n");
        write_file(root, ".chalkignore.prod", "prod_specific\n");
        write_file(root, ".chalkignore", "default_ignore\n");

        let settings = check_directory(root, "chalk.yaml").unwrap().unwrap();

        assert_eq!(
            settings.environments["dev"].chalkignore.as_deref(),
            Some(root.join(".chalkignore.dev").as_path())
        );
        assert_eq!(
            settings.environments["prod"].chalkignore.as_deref(),
            Some(root.join(".chalkignore.prod").as_path())
        );
        assert_eq!(
            settings.environments["default"].chalkignore.as_deref(),
            Some(root.join(".chalkignore").as_path())
        );
    }

    #[test]
    fn defaults_environment_chalkignore_to_project_level_file() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(
            root,
            "chalk.yaml",
            r#"project: test-project
environments:
  dev:
    runtime: python312
"#,
        );
        write_file(root, ".chalkignore", "default_ignore\n");

        let settings = check_directory(root, "chalk.yaml").unwrap().unwrap();

        assert_eq!(
            settings.environments["dev"].chalkignore.as_deref(),
            Some(root.join(".chalkignore").as_path())
        );
    }

    #[test]
    fn default_environment_settings_returns_default_environment() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(
            root,
            "chalk.yaml",
            r#"project: test-project
environments:
  default:
    runtime: python312
    dockerfile: Dockerfile
"#,
        );

        let settings = check_directory(root, "chalk.yaml").unwrap().unwrap();
        let default_settings = settings.default_environment_settings().unwrap();

        assert_eq!(default_settings.runtime.as_deref(), Some("python312"));
        assert_eq!(default_settings.dockerfile.as_deref(), Some("Dockerfile"));
    }

    #[test]
    fn resolved_environment_settings_merges_with_default_environment() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(
            root,
            "chalk.yaml",
            r#"project: test-project
environments:
  default:
    runtime: python312
    requirements: requirements-default.txt
    chalkignore: .chalkignore
  dev:
    dockerfile: Dockerfile.dev
"#,
        );
        write_file(root, ".chalkignore", "default_ignore\n");

        let settings = check_directory(root, "chalk.yaml").unwrap().unwrap();
        let resolved = settings.resolved_environment_settings(Some("dev"));

        assert_eq!(resolved.runtime.as_deref(), Some("python312"));
        assert_eq!(
            resolved.requirements.as_deref(),
            Some("requirements-default.txt")
        );
        assert_eq!(resolved.dockerfile.as_deref(), Some("Dockerfile.dev"));
        assert_eq!(
            resolved.chalkignore.as_deref(),
            Some(root.join(".chalkignore").as_path())
        );
    }

    #[test]
    fn resolved_environment_settings_falls_back_to_project_chalkignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(
            root,
            "chalk.yaml",
            "project: test-project\nchalkignore: .chalkignore.dev\n",
        );
        write_file(root, ".chalkignore.dev", "default_ignore\n");

        let settings = check_directory(root, "chalk.yaml").unwrap().unwrap();
        let resolved = settings.resolved_environment_settings(Some("dev"));

        assert_eq!(
            resolved.chalkignore.as_deref(),
            Some(root.join(".chalkignore.dev").as_path())
        );
    }

    #[test]
    fn preserves_chalkignore_when_round_tripping_yaml() {
        let env = EnvironmentSettings {
            runtime: Some("python312".to_owned()),
            chalkignore: Some(Path::new(".chalkignore.custom").to_path_buf()),
            ..EnvironmentSettings::default()
        };

        let yaml = serde_yaml::to_string(&env).unwrap();
        let unmarshaled: EnvironmentSettings = serde_yaml::from_str(&yaml).unwrap();

        assert_eq!(
            unmarshaled.chalkignore.as_deref(),
            Some(Path::new(".chalkignore.custom"))
        );
    }

    #[test]
    fn walks_up_parent_directories_to_find_project_config() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();
        let nested = root.join("src/lib/module");
        fs::create_dir_all(&nested).unwrap();

        write_file(root, "chalk.yaml", "project: sandbox\n");

        let settings = find_project_config(&nested).unwrap();

        assert_eq!(settings.filename, root.join("chalk.yaml"));
        assert_eq!(settings.local_directory, root);
    }

    #[test]
    fn finds_chalk_yml_from_root() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, "chalk.yml", "project: sandbox\n");

        let settings = load_project_config_from_root(root).unwrap();

        assert_eq!(settings.filename, root.join("chalk.yml"));
        assert_eq!(settings.project, "sandbox");
    }

    #[test]
    fn fills_in_default_requirements_when_pyproject_exists() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(
            root,
            "chalk.yaml",
            r#"project: sandbox
environments:
  dev:
    runtime: python312
"#,
        );
        write_file(root, DEFAULT_REQUIREMENTS, "[project]\nname = 'sandbox'\n");

        let settings: ProjectSettings = check_directory(root, "chalk.yaml").unwrap().unwrap();

        assert_eq!(
            settings.environments["dev"].requirements.as_deref(),
            Some(DEFAULT_REQUIREMENTS)
        );
    }
}
