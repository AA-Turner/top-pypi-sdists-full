use std::fs;
use std::io;
use std::path::{Component, Path, PathBuf};

use chalk_project::{load_project_config_from_root, ProjectError};
use ignore::gitignore::GitignoreBuilder;
use ignore::Match;
use thiserror::Error;

pub const MANUAL_IGNORED: &[&str] = &[
    "*.egg*",
    "*.iml",
    "*.ipynb_checkpoints*",
    "*.pyc",
    "*.py~",
    "*venv",
    ".DS_Store",
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "venv",
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchKind {
    Ignore,
    Whitelist,
}

#[derive(Debug, Error)]
pub enum IgnoreError {
    #[error(transparent)]
    Io(#[from] io::Error),
    #[error(transparent)]
    Pattern(#[from] ignore::Error),
    #[error(transparent)]
    Project(#[from] ProjectError),
}

#[derive(Debug)]
pub struct ProjectIgnoreMatcher {
    root: PathBuf,
    gitignores: Vec<GitignoreEntry>,
    chalkignore: ignore::gitignore::Gitignore,
    manual: ignore::gitignore::Gitignore,
}

#[derive(Clone, Debug)]
struct GitignoreEntry {
    directory: PathBuf,
    matcher: ignore::gitignore::Gitignore,
}

impl ProjectIgnoreMatcher {
    pub fn with_chalkignore<P, Q>(
        root: P,
        chalkignore_path: Option<Q>,
        also_ignore: &[&str],
    ) -> Result<Self, IgnoreError>
    where
        P: AsRef<Path>,
        Q: AsRef<Path>,
    {
        let root = normalize_path(&absolutize(root.as_ref())?);
        let gitignores = load_gitignores(&root)?;
        let chalkignore = build_project_relative_ignore(
            &root,
            chalkignore_path.as_ref().map(|path| path.as_ref()),
        )?;
        let manual = build_manual_ignore(&root, also_ignore)?;

        Ok(Self {
            root,
            gitignores,
            chalkignore,
            manual,
        })
    }

    pub fn matched<P: AsRef<Path>>(
        &self,
        path: P,
        is_dir: bool,
    ) -> Result<Option<MatchKind>, IgnoreError> {
        let path = normalize_path(&self.resolve_candidate(path.as_ref())?);
        if !path.starts_with(&self.root) {
            return Ok(None);
        }

        let mut result = match_gitignore_entries(&self.gitignores, &path, is_dir);

        result = fold_match(
            result,
            self.chalkignore.matched_path_or_any_parents(&path, is_dir),
        );
        result = fold_match(
            result,
            self.manual.matched_path_or_any_parents(&path, is_dir),
        );

        Ok(result)
    }

    pub fn is_ignored<P: AsRef<Path>>(&self, path: P, is_dir: bool) -> Result<bool, IgnoreError> {
        Ok(matches!(
            self.matched(path, is_dir)?,
            Some(MatchKind::Ignore)
        ))
    }

    pub fn walk_project_files<F>(&self, mut visitor: F) -> Result<(), IgnoreError>
    where
        F: FnMut(&Path) -> Result<(), IgnoreError>,
    {
        self.walk_directory(&self.root, &mut visitor)
    }

    fn walk_directory<F>(&self, directory: &Path, visitor: &mut F) -> Result<(), IgnoreError>
    where
        F: FnMut(&Path) -> Result<(), IgnoreError>,
    {
        let mut entries = fs::read_dir(directory)?.collect::<Result<Vec<_>, io::Error>>()?;
        entries.sort_by_key(|entry| entry.path());

        for entry in entries {
            let path = entry.path();
            let file_type = entry.file_type()?;
            let is_dir = file_type.is_dir();

            if self.is_ignored(&path, is_dir)? {
                continue;
            }

            if is_dir {
                self.walk_directory(&path, visitor)?;
            } else {
                visitor(&path)?;
            }
        }

        Ok(())
    }

    fn resolve_candidate(&self, path: &Path) -> io::Result<PathBuf> {
        if path.is_absolute() {
            Ok(path.to_path_buf())
        } else {
            Ok(self.root.join(path))
        }
    }
}

pub fn get_matcher_for_project<P: AsRef<Path>>(
    root: P,
    also_ignore: &[&str],
) -> Result<ProjectIgnoreMatcher, IgnoreError> {
    ProjectIgnoreMatcher::with_chalkignore(root, None::<&Path>, also_ignore)
}

pub fn get_matcher_for_project_with_chalkignore<P, Q>(
    root: P,
    chalkignore_path: Option<Q>,
    also_ignore: &[&str],
) -> Result<ProjectIgnoreMatcher, IgnoreError>
where
    P: AsRef<Path>,
    Q: AsRef<Path>,
{
    ProjectIgnoreMatcher::with_chalkignore(root, chalkignore_path, also_ignore)
}

pub fn get_chalkignore_path<P: AsRef<Path>>(
    root: P,
    environment_name: Option<&str>,
) -> Result<Option<PathBuf>, IgnoreError> {
    match load_project_config_from_root(root) {
        Ok(settings) => Ok(settings
            .resolved_environment_settings(environment_name)
            .chalkignore),
        Err(ProjectError::NotFound) => Ok(None),
        Err(error) => Err(error.into()),
    }
}

pub fn walk_project_files<P, Q, F>(
    root: P,
    chalkignore_path: Option<Q>,
    also_ignore: &[&str],
    visitor: F,
) -> Result<(), IgnoreError>
where
    P: AsRef<Path>,
    Q: AsRef<Path>,
    F: FnMut(&Path) -> Result<(), IgnoreError>,
{
    ProjectIgnoreMatcher::with_chalkignore(root, chalkignore_path, also_ignore)?
        .walk_project_files(visitor)
}

pub fn get_project_files<P, Q>(
    root: P,
    chalkignore_path: Option<Q>,
    also_ignore: &[&str],
) -> Result<Vec<PathBuf>, IgnoreError>
where
    P: AsRef<Path>,
    Q: AsRef<Path>,
{
    let matcher = ProjectIgnoreMatcher::with_chalkignore(root, chalkignore_path, also_ignore)?;
    let mut paths = Vec::new();
    matcher.walk_project_files(|path| {
        paths.push(path.to_path_buf());
        Ok(())
    })?;
    Ok(paths)
}

fn load_gitignores(root: &Path) -> Result<Vec<GitignoreEntry>, IgnoreError> {
    let mut active_entries = Vec::new();
    let mut entries = Vec::new();
    collect_gitignores(root, &mut active_entries, &mut entries)?;
    Ok(entries)
}

fn collect_gitignores(
    directory: &Path,
    active_entries: &mut Vec<GitignoreEntry>,
    all_entries: &mut Vec<GitignoreEntry>,
) -> Result<(), IgnoreError> {
    let mut should_pop = false;
    if let Some(entry) = read_directory_gitignore(directory)? {
        active_entries.push(entry.clone());
        all_entries.push(entry);
        should_pop = true;
    }

    let mut entries = fs::read_dir(directory)?.collect::<Result<Vec<_>, io::Error>>()?;
    entries.sort_by_key(|entry| entry.path());

    for entry in entries {
        let path = entry.path();
        let file_type = entry.file_type()?;
        if file_type.is_dir() {
            if path.file_name().is_some_and(|name| name == ".git") {
                continue;
            }
            if matches!(
                match_gitignore_entries(active_entries, &path, true),
                Some(MatchKind::Ignore)
            ) {
                continue;
            }
            collect_gitignores(&path, active_entries, all_entries)?;
        }
    }

    if should_pop {
        active_entries.pop();
    }

    Ok(())
}

fn read_directory_gitignore(directory: &Path) -> Result<Option<GitignoreEntry>, IgnoreError> {
    let path = directory.join(".gitignore");
    if !path.is_file() {
        return Ok(None);
    }

    let mut builder = GitignoreBuilder::new(directory);
    add_ignore_file_lines(&mut builder, &path)?;
    let matcher = builder.build()?;

    Ok(Some(GitignoreEntry {
        directory: directory.to_path_buf(),
        matcher,
    }))
}

fn build_project_relative_ignore(
    root: &Path,
    ignore_path: Option<&Path>,
) -> Result<ignore::gitignore::Gitignore, IgnoreError> {
    let path = ignore_path
        .map(|path| {
            if path.is_absolute() {
                path.to_path_buf()
            } else {
                root.join(path)
            }
        })
        .unwrap_or_else(|| root.join(".chalkignore"));

    let mut builder = GitignoreBuilder::new(root);
    add_ignore_file_lines(&mut builder, &path)?;
    Ok(builder.build()?)
}

fn build_manual_ignore(
    root: &Path,
    also_ignore: &[&str],
) -> Result<ignore::gitignore::Gitignore, IgnoreError> {
    let mut builder = GitignoreBuilder::new(root);
    for pattern in MANUAL_IGNORED.iter().chain(also_ignore.iter()) {
        builder.add_line(None, pattern)?;
    }
    Ok(builder.build()?)
}

fn add_ignore_file_lines(builder: &mut GitignoreBuilder, path: &Path) -> Result<(), IgnoreError> {
    let contents = match fs::read_to_string(path) {
        Ok(contents) => contents,
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(()),
        Err(error) => return Err(error.into()),
    };

    for line in contents.lines() {
        builder.add_line(Some(path.to_path_buf()), line)?;
    }

    Ok(())
}

fn fold_match(
    current: Option<MatchKind>,
    next: Match<&ignore::gitignore::Glob>,
) -> Option<MatchKind> {
    match next {
        Match::None => current,
        Match::Ignore(_) => Some(MatchKind::Ignore),
        Match::Whitelist(_) => Some(MatchKind::Whitelist),
    }
}

fn match_gitignore_entries(
    entries: &[GitignoreEntry],
    path: &Path,
    is_dir: bool,
) -> Option<MatchKind> {
    let mut result = None;

    for entry in entries {
        if path.starts_with(&entry.directory) {
            result = fold_match(
                result,
                entry.matcher.matched_path_or_any_parents(path, is_dir),
            );
        }
    }

    result
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
    use super::{get_chalkignore_path, get_project_files, MatchKind, ProjectIgnoreMatcher};
    use std::fs;
    use std::path::{Path, PathBuf};

    use tempfile::TempDir;

    fn write_file(root: &Path, relative_path: &str, contents: &str) {
        let path = root.join(relative_path);
        if let Some(parent) = path.parent() {
            fs::create_dir_all(parent).unwrap();
        }
        fs::write(path, contents).unwrap();
    }

    fn create_test_files(root: &Path, paths: &[&str]) {
        for path in paths {
            write_file(root, path, "");
        }
    }

    fn relative_paths(root: &Path, paths: Vec<PathBuf>) -> Vec<String> {
        let mut paths = paths
            .into_iter()
            .map(|path| {
                path.strip_prefix(root)
                    .unwrap()
                    .to_string_lossy()
                    .replace('\\', "/")
            })
            .collect::<Vec<_>>();
        paths.sort();
        paths
    }

    #[test]
    fn respects_project_chalkignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".chalkignore", "excludeplz\n");
        create_test_files(
            root,
            &[
                "nice/excludeplz/wow",
                "excludeplz/wow",
                "wow/excludeplz",
                "sweet",
            ],
        );

        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert_eq!(actual, vec![".chalkignore", "sweet"]);
    }

    #[test]
    fn supports_single_star_in_chalkignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".chalkignore", "scripts/*\n");
        create_test_files(root, &["scripts/wow.py", "sweet"]);

        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert_eq!(actual, vec![".chalkignore", "sweet"]);
    }

    #[test]
    fn supports_double_star_in_chalkignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".chalkignore", "scripts/**\n");
        create_test_files(root, &["scripts/nice/wow.py", "sweet"]);

        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert_eq!(actual, vec![".chalkignore", "sweet"]);
    }

    #[test]
    fn respects_project_gitignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".gitignore", "excludeplz\n");
        create_test_files(
            root,
            &[
                "nice/excludeplz/wow",
                "excludeplz/wow",
                "wow/excludeplz",
                "sweet",
            ],
        );

        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert_eq!(actual, vec![".gitignore", "sweet"]);
    }

    #[test]
    fn respects_manual_ignore_patterns() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        create_test_files(root, &["nice/wow.pyc", "hello.py~"]);

        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert!(actual.is_empty());
    }

    #[test]
    fn combines_nested_gitignore_chalkignore_and_manual_ignores() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".gitignore", "nothanks.py\n");
        write_file(root, "sweet/.gitignore", "sweetignore\n");
        write_file(root, ".chalkignore", "excludeplz\n");
        create_test_files(
            root,
            &[
                "nice/excludeplz/wow",
                "excludeplz/wow",
                "wow/excludeplz",
                "wow/nothanks.py",
                "sweetignore/nice",
                "sweet/sweetignore/hello",
                "nice/wow.pyc",
                "hello.py~",
                "nothanks.py",
            ],
        );

        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert_eq!(
            actual,
            vec![
                ".chalkignore",
                ".gitignore",
                "sweet/.gitignore",
                "sweetignore/nice"
            ]
        );
    }

    #[test]
    fn does_not_read_gitignores_inside_ignored_directories() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".gitignore", "ignored_dir\n");
        write_file(root, "ignored_dir/.gitignore", "!file.txt\n");
        create_test_files(root, &["ignored_dir/file.txt", "keep.txt"]);

        let matcher = ProjectIgnoreMatcher::with_chalkignore(root, None::<&Path>, &[]).unwrap();
        let actual = relative_paths(root, get_project_files(root, None::<&Path>, &[]).unwrap());

        assert_eq!(
            matcher
                .matched(root.join("ignored_dir/file.txt"), false)
                .unwrap(),
            Some(MatchKind::Ignore)
        );
        assert_eq!(actual, vec![".gitignore", "keep.txt"]);
    }

    #[test]
    fn selects_environment_specific_chalkignore_from_project_config() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".gitignore", "nothanks.py\n");
        write_file(root, "sweet/.gitignore", "sweetignore\n");
        write_file(root, ".chalkignore", "excludeplz\n");
        write_file(root, ".chalkignore.dev", "excludeplz\nnice\n");
        write_file(
            root,
            "chalk.yaml",
            r#"environments:
  dev:
    chalkignore: .chalkignore.dev
"#,
        );
        create_test_files(
            root,
            &[
                "nice/excludeplz/wow",
                "excludeplz/wow",
                "wow/excludeplz",
                "wow/nothanks.py",
                "sweetignore/nice",
                "sweet/sweetignore/hello",
                "nice/wow.pyc",
                "hello.py~",
                "nothanks.py",
            ],
        );

        let chalkignore_path = get_chalkignore_path(root, Some("dev")).unwrap();
        let actual = relative_paths(
            root,
            get_project_files(root, chalkignore_path.as_deref(), &[]).unwrap(),
        );

        assert_eq!(
            actual,
            vec![
                ".chalkignore",
                ".chalkignore.dev",
                ".gitignore",
                "chalk.yaml",
                "sweet/.gitignore",
            ]
        );
    }

    #[test]
    fn falls_back_to_default_environment_chalkignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".gitignore", "nothanks.py\n");
        write_file(root, "sweet/.gitignore", "sweetignore\n");
        write_file(root, ".chalkignore", "excludeplz\n");
        write_file(root, ".chalkignore.dev", "excludeplz\nnice\n");
        write_file(
            root,
            "chalk.yaml",
            r#"environments:
  random:
    chalkignore: .chalkignore
  default:
    chalkignore: .chalkignore.dev
"#,
        );
        create_test_files(
            root,
            &[
                "nice/excludeplz/wow",
                "excludeplz/wow",
                "wow/excludeplz",
                "wow/nothanks.py",
                "sweetignore/nice",
                "sweet/sweetignore/hello",
                "nice/wow.pyc",
                "hello.py~",
                "nothanks.py",
            ],
        );

        let chalkignore_path = get_chalkignore_path(root, Some("dev")).unwrap();
        let actual = relative_paths(
            root,
            get_project_files(root, chalkignore_path.as_deref(), &[]).unwrap(),
        );

        assert_eq!(
            actual,
            vec![
                ".chalkignore",
                ".chalkignore.dev",
                ".gitignore",
                "chalk.yaml",
                "sweet/.gitignore",
            ]
        );
    }

    #[test]
    fn falls_back_to_project_level_chalkignore() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".gitignore", "nothanks.py\n");
        write_file(root, "sweet/.gitignore", "sweetignore\n");
        write_file(root, ".chalkignore", "excludeplz\n");
        write_file(root, ".chalkignore.dev", "excludeplz\nnice\n");
        write_file(root, "chalk.yaml", "chalkignore: .chalkignore.dev\n");
        create_test_files(
            root,
            &[
                "nice/excludeplz/wow",
                "excludeplz/wow",
                "wow/excludeplz",
                "wow/nothanks.py",
                "sweetignore/nice",
                "sweet/sweetignore/hello",
                "nice/wow.pyc",
                "hello.py~",
                "nothanks.py",
            ],
        );

        let chalkignore_path = get_chalkignore_path(root, Some("dev")).unwrap();
        let actual = relative_paths(
            root,
            get_project_files(root, chalkignore_path.as_deref(), &[]).unwrap(),
        );

        assert_eq!(
            actual,
            vec![
                ".chalkignore",
                ".chalkignore.dev",
                ".gitignore",
                "chalk.yaml",
                "sweet/.gitignore",
            ]
        );
    }

    #[test]
    fn reports_whitelist_matches() {
        let tempdir = TempDir::new().unwrap();
        let root = tempdir.path();

        write_file(root, ".chalkignore", "*.py\n!keep.py\n");
        create_test_files(root, &["drop.py", "keep.py"]);
        let matcher = ProjectIgnoreMatcher::with_chalkignore(root, None::<&Path>, &[]).unwrap();

        assert_eq!(
            matcher.matched(root.join("keep.py"), false).unwrap(),
            Some(MatchKind::Whitelist)
        );
        assert_eq!(
            matcher.matched(root.join("drop.py"), false).unwrap(),
            Some(MatchKind::Ignore)
        );
    }
}
