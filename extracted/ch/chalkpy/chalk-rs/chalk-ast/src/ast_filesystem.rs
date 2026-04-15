use std::io;
use std::path::Path;

pub trait AstFileSystem: Send + Sync {
    fn read_to_string(&self, path: &str) -> io::Result<String>;
    fn all_files(&self) -> io::Result<Vec<String>>;
}

#[derive(Clone, Debug, Default)]
pub struct StdAstFileSystem {
    files: Vec<String>,
}

impl StdAstFileSystem {
    pub fn new(mut files: Vec<String>) -> Self {
        files.retain(|file| is_python_file(Path::new(file)));
        files.sort();
        files.dedup();
        Self { files }
    }
}

fn is_python_file(path: &Path) -> bool {
    path.extension().is_some_and(|ext| ext == "py")
}

impl AstFileSystem for StdAstFileSystem {
    fn read_to_string(&self, path: &str) -> io::Result<String> {
        std::fs::read_to_string(path)
    }

    fn all_files(&self) -> io::Result<Vec<String>> {
        Ok(self.files.clone())
    }
}

#[cfg(test)]
mod tests {
    use super::{AstFileSystem, StdAstFileSystem};

    #[test]
    fn non_python_files_are_filtered_out() {
        let fs = StdAstFileSystem::new(vec![
            "a.py".to_string(),
            "README.md".to_string(),
            "config.yaml".to_string(),
            "pkg/__init__.py".to_string(),
        ]);

        assert_eq!(
            fs.all_files().expect("all_files should succeed"),
            vec!["a.py", "pkg/__init__.py"]
        );
    }
}
