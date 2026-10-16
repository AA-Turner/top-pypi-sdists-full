use ruff_db::system::walk_directory::WalkDirectoryBuilder;
use ruff_db::system::{
    DirectoryEntry, Metadata, OsSystem, System, SystemPath, SystemPathBuf, SystemVirtualPath,
    WhichResult, WritableSystem,
};
use ruff_notebook::{Notebook, NotebookError};

const MAX_ANALYZED_FILE_BYTES: u64 = 1_000_000;

#[derive(Clone, Debug)]
pub(crate) struct BoundedSystem {
    inner: OsSystem,
}

impl BoundedSystem {
    pub(crate) fn new(inner: OsSystem) -> Self {
        Self { inner }
    }

    fn should_stub_source(&self, path: &SystemPath) -> bool {
        let path = path.as_std_path();
        let is_python_source = path
            .extension()
            .and_then(|extension| extension.to_str())
            .is_some_and(|extension| matches!(extension, "py" | "pyi"));
        is_python_source
            && path
                .metadata()
                .is_ok_and(|metadata| metadata.len() > MAX_ANALYZED_FILE_BYTES)
    }
}

impl System for BoundedSystem {
    fn path_metadata(&self, path: &SystemPath) -> std::io::Result<Metadata> {
        self.inner.path_metadata(path)
    }

    fn canonicalize_path(&self, path: &SystemPath) -> std::io::Result<SystemPathBuf> {
        self.inner.canonicalize_path(path)
    }

    fn is_same_file(&self, first: &SystemPath, second: &SystemPath) -> std::io::Result<bool> {
        self.inner.is_same_file(first, second)
    }

    fn source_type(&self, path: &SystemPath) -> Option<ruff_python_ast::PySourceType> {
        self.inner.source_type(path)
    }

    fn virtual_path_source_type(
        &self,
        path: &SystemVirtualPath,
    ) -> Option<ruff_python_ast::PySourceType> {
        self.inner.virtual_path_source_type(path)
    }

    fn which(&self, binary_name: &str) -> WhichResult {
        self.inner.which(binary_name)
    }

    fn read_to_string(&self, path: &SystemPath) -> std::io::Result<String> {
        if self.should_stub_source(path) {
            return Ok("# chalk-analyze stubbed oversized Python source\n".to_string());
        }
        self.inner.read_to_string(path)
    }

    fn read_to_notebook(&self, path: &SystemPath) -> std::result::Result<Notebook, NotebookError> {
        self.inner.read_to_notebook(path)
    }

    fn read_virtual_path_to_string(&self, path: &SystemVirtualPath) -> std::io::Result<String> {
        self.inner.read_virtual_path_to_string(path)
    }

    fn read_virtual_path_to_notebook(
        &self,
        path: &SystemVirtualPath,
    ) -> std::result::Result<Notebook, NotebookError> {
        self.inner.read_virtual_path_to_notebook(path)
    }

    fn path_exists(&self, path: &SystemPath) -> bool {
        self.inner.path_exists(path)
    }

    fn is_directory(&self, path: &SystemPath) -> bool {
        self.inner.is_directory(path)
    }

    fn is_file(&self, path: &SystemPath) -> bool {
        self.inner.is_file(path)
    }

    fn current_directory(&self) -> &SystemPath {
        self.inner.current_directory()
    }

    fn user_config_directory(&self) -> Option<SystemPathBuf> {
        self.inner.user_config_directory()
    }

    fn cache_dir(&self) -> Option<SystemPathBuf> {
        self.inner.cache_dir()
    }

    fn read_directory<'a>(
        &'a self,
        path: &SystemPath,
    ) -> std::io::Result<Box<dyn Iterator<Item = std::io::Result<DirectoryEntry>> + 'a>> {
        self.inner.read_directory(path)
    }

    fn walk_directory(&self, path: &SystemPath) -> WalkDirectoryBuilder {
        self.inner.walk_directory(path)
    }

    fn env_var(&self, name: &str) -> std::result::Result<String, std::env::VarError> {
        self.inner.env_var(name)
    }

    fn as_writable(&self) -> Option<&dyn WritableSystem> {
        self.inner.as_writable()
    }

    fn as_any(&self) -> &dyn std::any::Any {
        self
    }

    fn as_any_mut(&mut self) -> &mut dyn std::any::Any {
        self
    }

    fn dyn_clone(&self) -> Box<dyn System> {
        Box::new(self.clone())
    }
}
