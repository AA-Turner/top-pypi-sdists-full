use std::collections::HashMap;
use std::io;
use std::path::{Path, PathBuf};
use std::sync::{Arc, Mutex, RwLock};

use ruff_python_ast::Stmt;
use ruff_python_parser::parse_module;
use ruff_python_trivia::CommentRanges;

mod ast_filesystem;
mod ast_types;
mod parser_cache_types;
mod project_index;
mod type_parsing;

pub use ast_filesystem::{AstFileSystem, StdAstFileSystem};
pub use ast_types::{FeatureClassAST, FeatureFieldAST, FunctionArgAST, ParsedAstFile, ResolverAST};
pub use parser_cache_types::{ImportAliasMap, KwargLocationMap, ParsedFileCache};
pub use project_index::AstProjectIndex;
pub use type_parsing::parse_ast_file_with_feature_module;

#[derive(Default)]
struct FileParseEntry {
    parsed: Mutex<Option<Result<Arc<ParsedFileCache>, String>>>,
}

struct AstFileParserCacheInner {
    fs: Arc<dyn AstFileSystem>,
    project_root: PathBuf,
    module_names: HashMap<PathBuf, String>,
    entries: RwLock<HashMap<String, Arc<FileParseEntry>>>,
}

#[derive(Clone)]
pub struct AstFileParserCache {
    inner: Arc<AstFileParserCacheInner>,
}

impl std::fmt::Debug for AstFileParserCache {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let entry_count = self
            .inner
            .entries
            .read()
            .map(|entries| entries.len())
            .unwrap_or(0);
        f.debug_struct("AstFileParserCache")
            .field("project_root", &self.inner.project_root)
            .field("module_name_count", &self.inner.module_names.len())
            .field("entry_count", &entry_count)
            .finish()
    }
}

impl AstFileParserCache {
    pub fn new(project_root: std::path::PathBuf, files: Vec<String>) -> Self {
        Self::with_filesystem(project_root, Arc::new(StdAstFileSystem::new(files)))
    }

    pub fn with_filesystem(project_root: std::path::PathBuf, fs: Arc<dyn AstFileSystem>) -> Self {
        let module_names = fs
            .all_files()
            .unwrap_or_default()
            .into_iter()
            .map(|path| {
                let absolute_path = absolutize(Path::new(&path), &project_root);
                let module_name = module_name_for_absolute_path(&absolute_path, &project_root);
                (absolute_path, module_name)
            })
            .collect();
        Self {
            inner: Arc::new(AstFileParserCacheInner {
                fs,
                project_root,
                module_names,
                entries: RwLock::new(HashMap::new()),
            }),
        }
    }

    pub fn get_parsed_file(&self, path: &str) -> Result<Arc<ParsedFileCache>, String> {
        let entry = self.entry_for_path(path)?;
        let mut parsed_guard = entry
            .parsed
            .lock()
            .map_err(|_| format!("AST parse cache lock poisoned for {}", path))?;

        if let Some(result) = parsed_guard.as_ref() {
            return result.clone();
        }

        let result = (|| {
            let source = self
                .inner
                .fs
                .read_to_string(path)
                .map_err(|err| format!("Failed to read {}: {}", path, err))?;
            let parsed = parse_module(&source)
                .map_err(|err| format!("Failed to parse {}: {}", path, err))?;
            let stmts = parsed.suite().to_vec();
            let imports = collect_import_alias_map(&stmts);
            let comment_ranges = CommentRanges::from(parsed.tokens());
            Ok(Arc::new(ParsedFileCache {
                path: path.to_string(),
                source,
                stmts,
                imports,
                comment_ranges,
            }))
        })();
        *parsed_guard = Some(result.clone());
        result
    }

    pub fn all_files(&self) -> io::Result<Vec<String>> {
        self.inner.fs.all_files()
    }

    pub fn module_name_for_path(&self, path: &str) -> String {
        let absolute_path = absolutize(Path::new(path), &self.inner.project_root);
        self.inner
            .module_names
            .get(&absolute_path)
            .cloned()
            .unwrap_or_else(|| {
                module_name_for_absolute_path(&absolute_path, &self.inner.project_root)
            })
    }

    fn entry_for_path(&self, path: &str) -> Result<Arc<FileParseEntry>, String> {
        if let Some(entry) = self
            .inner
            .entries
            .read()
            .map_err(|_| "AST file entry map lock poisoned".to_string())?
            .get(path)
            .cloned()
        {
            return Ok(entry);
        }

        let mut entries = self
            .inner
            .entries
            .write()
            .map_err(|_| "AST file entry map lock poisoned".to_string())?;
        Ok(entries
            .entry(path.to_string())
            .or_insert_with(|| Arc::new(FileParseEntry::default()))
            .clone())
    }
}

fn absolutize(path: &Path, base_dir: &Path) -> PathBuf {
    if path.is_absolute() {
        path.to_path_buf()
    } else {
        base_dir.join(path)
    }
}

fn module_name_for_absolute_path(path: &Path, project_root: &Path) -> String {
    if let Some(module_name) = relative_module_name(path, project_root) {
        return module_name;
    }

    fallback_module_name(path)
}

fn fallback_module_name(path: &Path) -> String {
    path.file_stem()
        .and_then(|stem| stem.to_str())
        .map(str::to_string)
        .unwrap_or_else(|| path.to_string_lossy().to_string())
}

pub(crate) fn relative_module_name(path: &Path, project_root: &Path) -> Option<String> {
    let relative_path = path.strip_prefix(project_root).ok()?;
    let mut parts = Vec::new();

    for component in relative_path.components() {
        let std::path::Component::Normal(part) = component else {
            continue;
        };
        let part = part.to_str()?;
        if let Some(stem) = part.strip_suffix(".py") {
            if stem != "__init__" {
                parts.push(stem.to_string());
            }
        } else {
            parts.push(part.to_string());
        }
    }

    (!parts.is_empty()).then(|| parts.join("."))
}

pub(crate) fn collect_import_alias_map(stmts: &[Stmt]) -> ImportAliasMap {
    let mut imports: ImportAliasMap = HashMap::new();

    for stmt in stmts {
        let Stmt::ImportFrom(import_from) = stmt else {
            continue;
        };

        if import_from.level > 0 {
            continue;
        }
        let Some(module) = import_from.module.as_ref() else {
            continue;
        };

        let symbol_map = imports.entry(module.as_str().to_string()).or_default();
        for alias in &*import_from.names {
            let local_name = alias.asname.as_ref().map_or_else(
                || alias.name.as_str().to_string(),
                |asname| asname.as_str().to_string(),
            );
            symbol_map
                .entry(alias.name.as_str().to_string())
                .or_default()
                .insert(local_name);
        }
    }

    imports
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::io;
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::sync::{Arc, Barrier, Mutex};
    use std::time::Duration;

    use super::AstFileParserCache;
    use crate::ast_filesystem::{AstFileSystem, StdAstFileSystem};

    struct MockFileSystem {
        files: HashMap<String, String>,
        reads: Mutex<HashMap<String, usize>>,
        total_reads: AtomicUsize,
        delay: Duration,
    }

    impl MockFileSystem {
        fn new(files: HashMap<String, String>) -> Self {
            Self {
                files,
                reads: Mutex::new(HashMap::new()),
                total_reads: AtomicUsize::new(0),
                delay: Duration::from_millis(0),
            }
        }

        fn with_delay(files: HashMap<String, String>, delay: Duration) -> Self {
            Self {
                files,
                reads: Mutex::new(HashMap::new()),
                total_reads: AtomicUsize::new(0),
                delay,
            }
        }

        fn read_count(&self, path: &str) -> usize {
            self.reads
                .lock()
                .expect("read map lock should not be poisoned")
                .get(path)
                .copied()
                .unwrap_or(0)
        }

        fn total_reads(&self) -> usize {
            self.total_reads.load(Ordering::SeqCst)
        }
    }

    impl AstFileSystem for MockFileSystem {
        fn read_to_string(&self, path: &str) -> io::Result<String> {
            if self.delay > Duration::from_millis(0) {
                std::thread::sleep(self.delay);
            }

            {
                let mut reads = self
                    .reads
                    .lock()
                    .expect("read map lock should not be poisoned");
                *reads.entry(path.to_string()).or_insert(0) += 1;
            }
            self.total_reads.fetch_add(1, Ordering::SeqCst);

            self.files
                .get(path)
                .cloned()
                .ok_or_else(|| io::Error::new(io::ErrorKind::NotFound, "missing file"))
        }

        fn all_files(&self) -> io::Result<Vec<String>> {
            let mut files: Vec<String> = self.files.keys().cloned().collect();
            files.sort();
            Ok(files)
        }
    }

    #[test]
    fn parses_lazily_and_caches_result() {
        let path = "example.py";
        let project_root = PathBuf::from("/tmp");
        let fs = Arc::new(MockFileSystem::new(HashMap::from([(
            path.to_string(),
            "from chalk.features import features as feat\n".to_string(),
        )])));
        let cache = AstFileParserCache::with_filesystem(project_root, fs.clone());

        assert_eq!(fs.total_reads(), 0);

        let parsed = cache
            .get_parsed_file(path)
            .expect("parse should succeed on first access");
        assert_eq!(fs.read_count(path), 1);
        assert_eq!(parsed.path, path);
        assert_eq!(
            parsed
                .imports
                .get("chalk.features")
                .and_then(|symbol_map| symbol_map.get("features"))
                .map(|names| names.contains("feat")),
            Some(true)
        );

        let parsed_again = cache
            .get_parsed_file(path)
            .expect("parse should use cache on second access");
        assert!(Arc::ptr_eq(&parsed, &parsed_again));
        assert_eq!(fs.read_count(path), 1);
    }

    #[test]
    fn concurrent_requests_share_single_parse() {
        let path = "concurrent.py";
        let project_root = PathBuf::from("/tmp");
        let fs = Arc::new(MockFileSystem::with_delay(
            HashMap::from([(
                path.to_string(),
                "from chalk.features import features\n".to_string(),
            )]),
            Duration::from_millis(50),
        ));
        let cache = Arc::new(AstFileParserCache::with_filesystem(
            project_root,
            fs.clone(),
        ));
        let barrier = Arc::new(Barrier::new(4));
        let mut handles = Vec::new();

        for _ in 0..4 {
            let cache = cache.clone();
            let barrier = barrier.clone();
            handles.push(std::thread::spawn(move || {
                barrier.wait();
                cache
                    .get_parsed_file(path)
                    .expect("parse should succeed concurrently")
            }));
        }

        let mut first = None;
        for handle in handles {
            let parsed = handle.join().expect("thread should join cleanly");
            if let Some(existing) = &first {
                assert!(Arc::ptr_eq(existing, &parsed));
            } else {
                first = Some(parsed);
            }
        }

        assert_eq!(fs.read_count(path), 1);
        assert_eq!(fs.total_reads(), 1);
    }

    #[test]
    fn std_filesystem_all_files_returns_sorted_unique_paths() {
        let fs = StdAstFileSystem::new(vec![
            "b.py".to_string(),
            "notes.txt".to_string(),
            "a.py".to_string(),
            "b.py".to_string(),
        ]);

        assert_eq!(
            fs.all_files().expect("all_files should succeed"),
            vec!["a.py", "b.py"]
        );
    }

    #[test]
    fn module_name_for_path_uses_project_root_from_cache() {
        let project_root = PathBuf::from("/tmp/project");
        let fs = Arc::new(MockFileSystem::new(HashMap::from([(
            "/tmp/project/nested/deeper/models.py".to_string(),
            "from chalk.features import features\n".to_string(),
        )])));
        let cache = AstFileParserCache::with_filesystem(project_root, fs);

        assert_eq!(
            cache.module_name_for_path("/tmp/project/nested/deeper/models.py"),
            "nested.deeper.models"
        );
        assert_eq!(
            cache.module_name_for_path("nested/deeper/models.py"),
            "nested.deeper.models"
        );
    }
}
