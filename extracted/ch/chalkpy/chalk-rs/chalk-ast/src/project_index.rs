use std::collections::HashMap;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::{Arc, Mutex, RwLock};

use crate::type_parsing::parse_ast_file_with_feature_module;
use crate::{
    AstFileParserCache, AstFileSystem, FeatureClassAST, ParsedAstFile, ResolverAST,
    StdAstFileSystem,
};

#[derive(Default)]
struct TypedAstEntry {
    parsed: Mutex<Option<Result<Arc<ParsedAstFile>, String>>>,
}

struct AstProjectIndexInner {
    file_parser_cache: AstFileParserCache,
    typed_entries: RwLock<HashMap<String, Arc<TypedAstEntry>>>,
    preload_started: AtomicBool,
}

#[derive(Clone)]
pub struct AstProjectIndex {
    file_paths: Arc<Vec<String>>,
    inner: Arc<AstProjectIndexInner>,
}

impl std::fmt::Debug for AstProjectIndex {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let typed_entry_count = self
            .inner
            .typed_entries
            .read()
            .map(|entries| entries.len())
            .unwrap_or(0);
        f.debug_struct("AstProjectIndex")
            .field("file_count", &self.file_paths.len())
            .field("typed_entry_count", &typed_entry_count)
            .finish()
    }
}

impl AstProjectIndex {
    pub fn new(project_root: std::path::PathBuf, files: Vec<String>) -> Result<Self, String> {
        Self::with_filesystem(
            project_root,
            files.clone(),
            Arc::new(StdAstFileSystem::new(files)),
        )
    }

    pub fn with_filesystem(
        project_root: std::path::PathBuf,
        files: Vec<String>,
        fs: Arc<dyn AstFileSystem>,
    ) -> Result<Self, String> {
        Ok(Self {
            file_paths: Arc::new(files),
            inner: Arc::new(AstProjectIndexInner {
                file_parser_cache: AstFileParserCache::with_filesystem(project_root, fs),
                typed_entries: RwLock::new(HashMap::new()),
                preload_started: AtomicBool::new(false),
            }),
        })
    }

    pub fn with_default_filesystem(
        project_root: std::path::PathBuf,
        files: Vec<String>,
    ) -> Result<Self, String> {
        Self::new(project_root, files)
    }

    pub fn feature_class_ast(&self, module: &str, class_name: &str) -> Option<FeatureClassAST> {
        for path in self.file_paths.iter() {
            if let Some(ast) = self.feature_class_ast_in_file(path, class_name) {
                if ast.module != module {
                    continue;
                }
                return Some(ast);
            }
        }
        None
    }

    pub fn feature_class_ast_in_file(
        &self,
        file_path: &str,
        class_name: &str,
    ) -> Option<FeatureClassAST> {
        let Ok(file_asts) = self.get_parsed_ast_file(file_path) else {
            return None;
        };
        file_asts
            .feature_classes
            .iter()
            .find(|ast| ast.class_name == class_name)
            .cloned()
    }

    pub fn resolver_ast(&self, module: &str, resolver_name: &str) -> Option<ResolverAST> {
        for path in self.file_paths.iter() {
            let Ok(file_asts) = self.get_parsed_ast_file(path) else {
                continue;
            };
            if let Some(ast) = file_asts
                .resolvers
                .iter()
                .find(|ast| ast.module == module && ast.resolver_name == resolver_name)
            {
                return Some(ast.clone());
            }
        }
        None
    }

    pub fn resolver_ast_in_file(
        &self,
        file_path: &str,
        resolver_name: &str,
    ) -> Option<ResolverAST> {
        let Ok(file_asts) = self.get_parsed_ast_file(file_path) else {
            return None;
        };
        file_asts
            .resolvers
            .iter()
            .find(|ast| ast.resolver_name == resolver_name)
            .cloned()
    }

    pub fn function_ast(&self, module: &str, function_name: &str) -> Option<ResolverAST> {
        for path in self.file_paths.iter() {
            let Ok(file_asts) = self.get_parsed_ast_file(path) else {
                continue;
            };
            if let Some(ast) = file_asts
                .functions
                .iter()
                .find(|ast| ast.module == module && ast.resolver_name == function_name)
            {
                return Some(ast.clone());
            }
        }
        None
    }

    pub fn function_ast_in_file(
        &self,
        file_path: &str,
        function_name: &str,
    ) -> Option<ResolverAST> {
        let Ok(file_asts) = self.get_parsed_ast_file(file_path) else {
            return None;
        };
        file_asts
            .functions
            .iter()
            .find(|ast| ast.resolver_name == function_name)
            .cloned()
    }

    pub fn nonblocking_start_index(&self) {
        if self.file_paths.is_empty() {
            return;
        }

        if self.inner.preload_started.swap(true, Ordering::AcqRel) {
            return;
        }

        let worker_count = std::thread::available_parallelism()
            .map(|count| count.get())
            .unwrap_or(1)
            .min(self.file_paths.len())
            .max(1);

        for worker_id in 0..worker_count {
            let index = self.clone();
            std::thread::spawn(move || {
                for (file_index, path) in index.file_paths.iter().enumerate() {
                    if file_index % worker_count != worker_id {
                        continue;
                    }
                    let _ = index.get_parsed_ast_file(path);
                }
            });
        }
    }

    fn get_parsed_ast_file(&self, path: &str) -> Result<Arc<ParsedAstFile>, String> {
        let entry = self.entry_for_path(path)?;
        let mut parsed_guard = entry
            .parsed
            .lock()
            .map_err(|_| format!("typed AST cache lock poisoned for {}", path))?;

        if let Some(result) = parsed_guard.as_ref() {
            return result.clone();
        }

        let result = (|| {
            let file = self.inner.file_parser_cache.get_parsed_file(path)?;
            let feature_class_module = self.inner.file_parser_cache.module_name_for_path(path);
            Ok(Arc::new(parse_ast_file_with_feature_module(
                file.as_ref(),
                &feature_class_module,
            )))
        })();
        *parsed_guard = Some(result.clone());
        result
    }

    fn entry_for_path(&self, path: &str) -> Result<Arc<TypedAstEntry>, String> {
        if let Some(entry) = self
            .inner
            .typed_entries
            .read()
            .map_err(|_| "typed AST entry map lock poisoned".to_string())?
            .get(path)
            .cloned()
        {
            return Ok(entry);
        }

        let mut entries = self
            .inner
            .typed_entries
            .write()
            .map_err(|_| "typed AST entry map lock poisoned".to_string())?;
        Ok(entries
            .entry(path.to_string())
            .or_insert_with(|| Arc::new(TypedAstEntry::default()))
            .clone())
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::io;
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::sync::{Arc, Mutex};
    use std::time::Duration;

    use super::AstProjectIndex;
    use crate::AstFileSystem;

    struct MockFileSystem {
        files: HashMap<String, String>,
        total_reads: AtomicUsize,
        reads: Mutex<HashMap<String, usize>>,
        delay: Duration,
    }

    impl MockFileSystem {
        fn new(files: HashMap<String, String>) -> Self {
            Self {
                files,
                total_reads: AtomicUsize::new(0),
                reads: Mutex::new(HashMap::new()),
                delay: Duration::from_millis(0),
            }
        }

        fn with_delay(files: HashMap<String, String>, delay: Duration) -> Self {
            Self {
                files,
                total_reads: AtomicUsize::new(0),
                reads: Mutex::new(HashMap::new()),
                delay,
            }
        }

        fn read_count(&self, path: &str) -> usize {
            self.reads
                .lock()
                .expect("reads lock should not be poisoned")
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
            self.total_reads.fetch_add(1, Ordering::SeqCst);
            if !self.delay.is_zero() {
                std::thread::sleep(self.delay);
            }
            {
                let mut reads = self
                    .reads
                    .lock()
                    .expect("reads lock should not be poisoned");
                *reads.entry(path.to_string()).or_insert(0) += 1;
            }
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
    fn project_index_scans_files_lazily_and_returns_typed_asts() {
        let project_root = PathBuf::from("/tmp");
        let user_path = "/tmp/user_features.py".to_string();
        let resolver_path = "/tmp/user_resolvers.py".to_string();
        let fs = Arc::new(MockFileSystem::new(HashMap::from([
            (
                user_path.clone(),
                r#"
from chalk.features import features

@features(name="user")
class User:
    id: int
"#
                .to_string(),
            ),
            (
                resolver_path.clone(),
                r#"
from chalk import online

@online(cron="0 0 * * *")
def compute_user(message: str):
    return message
"#
                .to_string(),
            ),
        ])));

        let index = AstProjectIndex::with_filesystem(
            project_root,
            vec![user_path.clone(), resolver_path.clone()],
            fs.clone(),
        )
        .expect("index should construct without parsing files");

        assert_eq!(fs.total_reads(), 0);

        let feature_class = index
            .feature_class_ast("user_features", "User")
            .expect("feature class should be found");
        assert_eq!(feature_class.module, "user_features");
        assert_eq!(feature_class.namespace, "user");
        assert_eq!(feature_class.class_name_location.range.start.line, 4);
        assert_eq!(fs.total_reads(), 1);

        let resolver = index
            .resolver_ast_in_file(&resolver_path, "compute_user")
            .expect("resolver should be found");
        assert_eq!(resolver.resolver_name, "compute_user");
        assert_eq!(resolver.resolver_name_location.range.start.line, 4);
        assert_eq!(fs.total_reads(), 2);

        let feature_class_again = index
            .feature_class_ast("user_features", "User")
            .expect("feature class should come from cache");
        assert_eq!(feature_class_again.class_name, "User");
        assert_eq!(fs.total_reads(), 2);
    }

    #[test]
    fn feature_class_ast_in_file_reads_only_requested_path_and_supports_indented_classes() {
        let project_root = PathBuf::from("/tmp");
        let root_path = "/tmp/root_user_features.py".to_string();
        let wrapped_path = "/tmp/wrapped_user_features.py".to_string();
        let fs = Arc::new(MockFileSystem::new(HashMap::from([
            (
                root_path.clone(),
                r#"
from chalk.features import features

@features(name="root_user")
class User:
    id: int
"#
                .to_string(),
            ),
            (
                wrapped_path.clone(),
                r#"
from chalk.features import features
from chalk import feature

if True:
    @features(name="wrapped_user")
    class User:
        # Wrapped user score.
        score: int = feature(default=0)
"#
                .to_string(),
            ),
        ])));

        let index = AstProjectIndex::with_filesystem(
            project_root,
            vec![root_path.clone(), wrapped_path.clone()],
            fs.clone(),
        )
        .expect("index should construct without parsing files");

        let feature_class = index
            .feature_class_ast_in_file(&wrapped_path, "User")
            .expect("feature class should be found in the requested file");

        assert_eq!(feature_class.module, "wrapped_user_features");
        assert_eq!(feature_class.namespace, "wrapped_user");
        assert_eq!(feature_class.class_name_location.range.start.line, 6);
        assert_eq!(
            feature_class.fields["score"].description.as_deref(),
            Some("Wrapped user score.")
        );
        assert_eq!(fs.read_count(&wrapped_path), 1);
        assert_eq!(fs.read_count(&root_path), 0);
        assert_eq!(fs.total_reads(), 1);
    }

    #[test]
    fn function_ast_in_file_finds_plain_functions() {
        let project_root = PathBuf::from("/tmp");
        let function_path = "/tmp/parse_fn.py".to_string();
        let fs = Arc::new(MockFileSystem::new(HashMap::from([(
            function_path.clone(),
            r#"
def parse_message(event: bytes) -> bytes:
    return event
"#
            .to_string(),
        )])));

        let index =
            AstProjectIndex::with_filesystem(project_root, vec![function_path.clone()], fs.clone())
                .expect("index should construct without parsing files");

        let function = index
            .function_ast_in_file(&function_path, "parse_message")
            .expect("plain function should be found in the requested file");

        assert_eq!(function.module, "parse_fn");
        assert_eq!(function.resolver_name, "parse_message");
        assert!(function.decorator_location.is_none());
        assert_eq!(function.args_in_order, vec!["event"]);
        assert!(function.return_annotation.is_some());
        assert_eq!(function.return_statements.len(), 1);
        assert_eq!(fs.total_reads(), 1);
    }

    #[test]
    fn feature_class_ast_uses_class_module_for_package_paths() {
        let project_root = PathBuf::from("/tmp");
        let package_init_path = "/tmp/pkg/__init__.py".to_string();
        let feature_path = "/tmp/pkg/models.py".to_string();
        let fs = Arc::new(MockFileSystem::new(HashMap::from([
            (package_init_path.clone(), String::new()),
            (
                feature_path.clone(),
                r#"
from chalk.features import features

@features
class User:
    id: int
"#
                .to_string(),
            ),
        ])));

        let index = AstProjectIndex::with_filesystem(
            project_root,
            vec![package_init_path, feature_path.clone()],
            fs,
        )
        .expect("index should construct without parsing files");

        let feature_class = index
            .feature_class_ast("pkg.models", "User")
            .expect("feature class should be found by package module");

        assert_eq!(feature_class.module, "pkg.models");
        assert_eq!(feature_class.class_name, "User");
        assert_eq!(
            index
                .feature_class_ast_in_file(&feature_path, "User")
                .expect("feature class should be found in file")
                .module,
            "pkg.models"
        );
    }

    #[test]
    fn feature_class_ast_in_file_preserves_duplicate_annotations() {
        let project_root = PathBuf::from("/tmp");
        let feature_path = "/tmp/user_features.py".to_string();
        let fs = Arc::new(MockFileSystem::new(HashMap::from([(
            feature_path.clone(),
            r#"
from chalk.features import features

@features
class User:
    score: int
    score: int
"#
            .to_string(),
        )])));

        let index = AstProjectIndex::with_filesystem(project_root, vec![feature_path.clone()], fs)
            .expect("index should construct without parsing files");

        let feature_class = index
            .feature_class_ast_in_file(&feature_path, "User")
            .expect("feature class should be found in file");

        assert_eq!(feature_class.fields.len(), 1);
        assert_eq!(
            feature_class
                .annotations
                .iter()
                .map(|field| field.field_name.as_str())
                .collect::<Vec<_>>(),
            vec!["score", "score"]
        );
        assert_eq!(
            feature_class
                .annotations
                .iter()
                .map(|field| field
                    .annotation
                    .as_ref()
                    .map(|location| location.range.start.line))
                .collect::<Vec<_>>(),
            vec![Some(5), Some(6)]
        );
    }

    #[test]
    fn nonblocking_start_index_preloads_files_once() {
        use std::time::{Duration, Instant};

        let project_root = PathBuf::from("/tmp");
        let feature_path = "/tmp/preload_features.py".to_string();
        let resolver_path = "/tmp/preload_resolvers.py".to_string();
        let fs = Arc::new(MockFileSystem::with_delay(
            HashMap::from([
                (
                    feature_path.clone(),
                    r#"
from chalk.features import features

@features
class User:
    id: int
"#
                    .to_string(),
                ),
                (
                    resolver_path.clone(),
                    r#"
from chalk import online

@online
def resolve_user(user_id: int) -> int:
    return user_id
"#
                    .to_string(),
                ),
            ]),
            Duration::from_millis(10),
        ));

        let index = AstProjectIndex::with_filesystem(
            project_root,
            vec![feature_path.clone(), resolver_path.clone()],
            fs.clone(),
        )
        .expect("index should construct without parsing files");

        index.nonblocking_start_index();
        index.nonblocking_start_index();

        let deadline = Instant::now() + Duration::from_secs(2);
        while fs.total_reads() == 0 && Instant::now() < deadline {
            std::thread::sleep(Duration::from_millis(10));
        }

        assert!(
            fs.total_reads() > 0,
            "background indexing should start parsing files before explicit lookups"
        );
        assert_eq!(
            index
                .feature_class_ast_in_file(&feature_path, "User")
                .expect("feature class should be preloaded")
                .class_name,
            "User"
        );
        assert_eq!(
            index
                .resolver_ast_in_file(&resolver_path, "resolve_user")
                .expect("resolver should be preloaded")
                .resolver_name,
            "resolve_user"
        );
        assert_eq!(fs.read_count(&feature_path), 1);
        assert_eq!(fs.read_count(&resolver_path), 1);
        assert_eq!(fs.total_reads(), 2);
    }
}
