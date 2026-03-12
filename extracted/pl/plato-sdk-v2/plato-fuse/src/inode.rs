use crate::config::FileEntry;
use libc::EINVAL;
use std::collections::HashMap;
use std::os::unix::fs::MetadataExt;
use std::path::Path;

pub const ROOT_INODE: u64 = 1;

#[derive(Debug, Clone)]
pub struct InodeInfo {
    pub ino: u64,
    pub name: String,
    pub parent: u64,
    pub backing_relpath: String,
    pub is_dir: bool,
    pub md5: Option<String>,
    pub size: u64,
    pub mode: u32,
    pub is_symlink: bool,
    pub symlink_target: Option<String>,
    pub nlink: u32,
    pub overlay: bool,
    pub deleted: bool,
}

pub struct InodeTree {
    inodes: HashMap<u64, InodeInfo>,
    children: HashMap<u64, HashMap<String, u64>>,
    relpath_cache: HashMap<u64, String>,
    next_inode: u64,
    manifest_relpaths: std::collections::HashSet<String>,
}

impl InodeTree {
    pub fn new() -> Self {
        let mut tree = InodeTree {
            inodes: HashMap::new(),
            children: HashMap::new(),
            relpath_cache: HashMap::new(),
            next_inode: ROOT_INODE + 1,
            manifest_relpaths: std::collections::HashSet::new(),
        };
        let root = InodeInfo {
            ino: ROOT_INODE,
            name: String::new(),
            parent: 0,
            backing_relpath: String::new(),
            is_dir: true,
            md5: None,
            size: 0,
            mode: 0o755,
            is_symlink: false,
            symlink_target: None,
            nlink: 2,
            overlay: false,
            deleted: false,
        };
        tree.inodes.insert(ROOT_INODE, root);
        tree.children.insert(ROOT_INODE, HashMap::new());
        tree
    }

    fn alloc_inode(&mut self) -> u64 {
        let ino = self.next_inode;
        self.next_inode += 1;
        ino
    }

    pub fn build_from_manifest(&mut self, entries: &[FileEntry]) {
        for entry in entries {
            self.manifest_relpaths.insert(entry.relpath.clone());
        }

        let mut dir_entries = entries
            .iter()
            .filter(|entry| entry.is_dir())
            .collect::<Vec<_>>();
        dir_entries.sort_by_key(|entry| (entry.relpath.split('/').count(), entry.relpath.clone()));
        for entry in dir_entries {
            let _ = self.insert_manifest_dir_entry(entry);
        }

        let mut file_entries = entries
            .iter()
            .filter(|entry| !entry.is_dir())
            .collect::<Vec<_>>();
        file_entries.sort_by_key(|entry| (entry.relpath.split('/').count(), entry.relpath.clone()));
        for entry in file_entries {
            let _ = self.insert_manifest_file_entry(entry);
        }
    }

    fn insert_manifest_dir_entry(&mut self, entry: &FileEntry) -> Option<u64> {
        let parts = Self::path_parts(&entry.relpath)?;
        let mut parent_ino = ROOT_INODE;
        for &part in &parts[..parts.len() - 1] {
            parent_ino = self.ensure_manifest_dir(parent_ino, part, None, 0o755)?;
        }

        self.ensure_manifest_dir(
            parent_ino,
            parts[parts.len() - 1],
            Some(entry.relpath.clone()),
            entry.manifest_mode(),
        )
    }

    fn insert_manifest_file_entry(&mut self, entry: &FileEntry) -> Option<u64> {
        let parts = Self::path_parts(&entry.relpath)?;
        let mut parent_ino = ROOT_INODE;
        for &part in &parts[..parts.len() - 1] {
            parent_ino = self.ensure_manifest_dir(parent_ino, part, None, 0o755)?;
        }

        let name = parts[parts.len() - 1];
        if let Some(&existing) = self.children.entry(parent_ino).or_default().get(name) {
            if self
                .inodes
                .get(&existing)
                .map(|info| info.is_dir)
                .unwrap_or(false)
            {
                log::warn!(
                    "ignoring manifest file entry {} because a directory already exists at that path",
                    entry.relpath
                );
                return None;
            }

            if let Some(info) = self.inodes.get_mut(&existing) {
                info.backing_relpath = entry.relpath.clone();
                info.md5 = entry.md5.clone();
                info.size = entry.size;
                info.mode = entry.manifest_mode();
                info.is_symlink = entry.islink;
                info.symlink_target = if entry.islink {
                    entry.symlink_target.clone()
                } else {
                    None
                };
                info.overlay = false;
                info.deleted = false;
            }
            return Some(existing);
        }

        let ino = self.alloc_inode();
        let info = InodeInfo {
            ino,
            name: name.to_string(),
            parent: parent_ino,
            backing_relpath: entry.relpath.clone(),
            is_dir: false,
            md5: entry.md5.clone(),
            size: entry.size,
            mode: entry.manifest_mode(),
            is_symlink: entry.islink,
            symlink_target: if entry.islink {
                entry.symlink_target.clone()
            } else {
                None
            },
            nlink: 1,
            overlay: false,
            deleted: false,
        };
        self.inodes.insert(ino, info);
        self.children
            .entry(parent_ino)
            .or_default()
            .insert(name.to_string(), ino);
        Some(ino)
    }

    fn ensure_manifest_dir(
        &mut self,
        parent_ino: u64,
        name: &str,
        backing_relpath: Option<String>,
        mode: u32,
    ) -> Option<u64> {
        if let Some(&existing) = self.children.entry(parent_ino).or_default().get(name) {
            if !self
                .inodes
                .get(&existing)
                .map(|info| info.is_dir)
                .unwrap_or(false)
            {
                log::warn!(
                    "ignoring manifest directory entry {} because a file already exists at that path",
                    backing_relpath.as_deref().unwrap_or(name)
                );
                return None;
            }
            if let Some(info) = self.inodes.get_mut(&existing) {
                if let Some(relpath) = backing_relpath {
                    info.backing_relpath = relpath;
                    info.mode = mode;
                }
            }
            return Some(existing);
        }

        let ino = self.alloc_inode();
        let info = InodeInfo {
            ino,
            name: name.to_string(),
            parent: parent_ino,
            backing_relpath: backing_relpath.unwrap_or_default(),
            is_dir: true,
            md5: None,
            size: 0,
            mode,
            is_symlink: false,
            symlink_target: None,
            nlink: 2,
            overlay: false,
            deleted: false,
        };
        self.inodes.insert(ino, info);
        self.children.insert(ino, HashMap::new());
        self.children
            .get_mut(&parent_ino)
            .unwrap()
            .insert(name.to_string(), ino);
        Some(ino)
    }

    fn path_parts(relpath: &str) -> Option<Vec<&str>> {
        let parts = relpath
            .split('/')
            .filter(|part| !part.is_empty())
            .collect::<Vec<_>>();
        if parts.is_empty() {
            log::warn!("ignoring empty manifest relpath");
            None
        } else {
            Some(parts)
        }
    }

    pub fn scan_overlay(&mut self, overlay_dir: &Path) {
        if !overlay_dir.exists() {
            return;
        }
        self.scan_overlay_dir(overlay_dir, overlay_dir, ROOT_INODE);
    }

    fn scan_overlay_dir(&mut self, base: &Path, dir: &Path, parent_ino: u64) {
        let entries = match std::fs::read_dir(dir) {
            Ok(e) => e,
            Err(e) => {
                log::warn!("Failed to read overlay dir {}: {}", dir.display(), e);
                return;
            }
        };
        for entry in entries.flatten() {
            let name = entry.file_name().to_string_lossy().to_string();
            let path = entry.path();
            let meta = match std::fs::symlink_metadata(&path) {
                Ok(m) => m,
                Err(e) => {
                    log::warn!("Failed to stat overlay entry {}: {}", path.display(), e);
                    continue;
                }
            };

            if meta.is_dir() {
                if std::fs::read_dir(&path).is_err() {
                    continue;
                }
                let mode = (meta.mode() & 0o777) as u32;
                let ino = if let Some(&existing) =
                    self.children.entry(parent_ino).or_default().get(&name)
                {
                    if !self
                        .inodes
                        .get(&existing)
                        .map(|info| info.is_dir)
                        .unwrap_or(false)
                    {
                        log::warn!(
                            "overlay scan skipping directory {} because a file already exists at that path",
                            path.display()
                        );
                        continue;
                    }
                    if let Some(info) = self.inodes.get_mut(&existing) {
                        info.overlay = true;
                        info.mode = mode;
                        info.nlink = meta.nlink() as u32;
                    }
                    existing
                } else {
                    let ino = self.alloc_inode();
                    let info = InodeInfo {
                        ino,
                        name: name.clone(),
                        parent: parent_ino,
                        backing_relpath: String::new(),
                        is_dir: true,
                        md5: None,
                        size: 0,
                        mode,
                        is_symlink: false,
                        symlink_target: None,
                        nlink: 2,
                        overlay: true,
                        deleted: false,
                    };
                    self.inodes.insert(ino, info);
                    self.children.insert(ino, HashMap::new());
                    self.children
                        .get_mut(&parent_ino)
                        .unwrap()
                        .insert(name.clone(), ino);
                    ino
                };
                self.scan_overlay_dir(base, &path, ino);
            } else {
                // Skip if already in tree (from manifest)
                if let Some(&ino) = self.children.entry(parent_ino).or_default().get(&name) {
                    if self
                        .inodes
                        .get(&ino)
                        .map(|info| info.is_dir)
                        .unwrap_or(false)
                    {
                        log::warn!(
                            "overlay scan skipping file {} because a directory already exists at that path",
                            path.display()
                        );
                        continue;
                    }
                    if let Some(info) = self.inodes.get_mut(&ino) {
                        info.overlay = true;
                        info.size = meta.len();
                        info.nlink = meta.nlink() as u32;
                    }
                    continue;
                }
                let is_sym = meta.file_type().is_symlink();
                let target = if is_sym {
                    match std::fs::read_link(&path) {
                        Ok(p) => p.to_string_lossy().to_string(),
                        Err(e) => {
                            log::warn!("Failed to read symlink {}: {}", path.display(), e);
                            continue;
                        }
                    }
                } else {
                    String::new()
                };
                let rel = path.strip_prefix(base).unwrap_or(&path).to_path_buf();
                let ino = self.alloc_inode();
                let info = InodeInfo {
                    ino,
                    name: name.clone(),
                    parent: parent_ino,
                    backing_relpath: rel.to_string_lossy().to_string(),
                    is_dir: false,
                    md5: None,
                    size: meta.len(),
                    mode: (meta.mode() & 0o777) as u32,
                    is_symlink: is_sym,
                    symlink_target: is_sym.then_some(target),
                    nlink: meta.nlink() as u32,
                    overlay: true,
                    deleted: false,
                };
                self.inodes.insert(ino, info);
                self.children
                    .get_mut(&parent_ino)
                    .unwrap()
                    .insert(name, ino);
            }
        }
    }

    pub fn get(&self, ino: u64) -> Option<&InodeInfo> {
        self.inodes.get(&ino)
    }

    pub fn get_mut(&mut self, ino: u64) -> Option<&mut InodeInfo> {
        self.inodes.get_mut(&ino)
    }

    pub fn get_children(&self, ino: u64) -> Option<&HashMap<String, u64>> {
        self.children.get(&ino)
    }

    pub fn lookup_child(&self, parent: u64, name: &str) -> Option<u64> {
        self.children.get(&parent)?.get(name).copied()
    }

    pub fn get_relpath(&mut self, ino: u64) -> String {
        if let Some(cached) = self.relpath_cache.get(&ino) {
            return cached.clone();
        }
        let result = self.compute_relpath(ino);
        self.relpath_cache.insert(ino, result.clone());
        result
    }

    fn compute_relpath(&self, ino: u64) -> String {
        let mut parts = Vec::new();
        let mut cur = ino;
        let mut depth = 0;
        while cur != 0 {
            if let Some(info) = self.inodes.get(&cur) {
                if info.parent == 0 {
                    break;
                }
                parts.push(info.name.clone());
                cur = info.parent;
                depth += 1;
                if depth > 256 {
                    // Cycle detected — return what we have
                    break;
                }
            } else {
                break;
            }
        }
        parts.reverse();
        parts.join("/")
    }

    pub fn is_in_manifest(&self, relpath: &str) -> bool {
        self.manifest_relpaths.contains(relpath)
    }

    pub fn add_file(
        &mut self,
        parent: u64,
        name: &str,
        mode: u32,
        is_symlink: bool,
        symlink_target: &str,
    ) -> u64 {
        let ino = self.alloc_inode();
        let parent_relpath = self.get_relpath(parent);
        let backing_relpath = if parent_relpath.is_empty() {
            name.to_string()
        } else {
            format!("{}/{}", parent_relpath, name)
        };
        let info = InodeInfo {
            ino,
            name: name.to_string(),
            parent,
            backing_relpath,
            is_dir: false,
            md5: None,
            size: 0,
            mode,
            is_symlink,
            symlink_target: is_symlink.then_some(symlink_target.to_string()),
            nlink: 1,
            overlay: true,
            deleted: false,
        };
        self.inodes.insert(ino, info);
        self.children
            .entry(parent)
            .or_default()
            .insert(name.to_string(), ino);
        ino
    }

    #[cfg(test)]
    pub fn add_dir(&mut self, parent: u64, name: &str) -> u64 {
        self.add_dir_with_mode(parent, name, 0o755)
    }

    pub fn add_dir_with_mode(&mut self, parent: u64, name: &str, mode: u32) -> u64 {
        let ino = self.alloc_inode();
        let info = InodeInfo {
            ino,
            name: name.to_string(),
            parent,
            backing_relpath: String::new(),
            is_dir: true,
            md5: None,
            size: 0,
            mode,
            is_symlink: false,
            symlink_target: None,
            nlink: 2,
            overlay: true,
            deleted: false,
        };
        self.inodes.insert(ino, info);
        self.children.insert(ino, HashMap::new());
        self.children
            .entry(parent)
            .or_default()
            .insert(name.to_string(), ino);
        ino
    }

    pub fn remove_child(&mut self, parent: u64, name: &str) {
        if let Some(children) = self.children.get_mut(&parent) {
            children.remove(name);
        }
    }

    pub fn add_link(&mut self, ino: u64, parent: u64, name: &str) -> Result<(), i32> {
        if self.get(parent).map(|info| !info.is_dir).unwrap_or(true) {
            return Err(EINVAL);
        }
        self.children
            .entry(parent)
            .or_default()
            .insert(name.to_string(), ino);
        if let Some(info) = self.inodes.get_mut(&ino) {
            info.nlink += 1;
        }
        Ok(())
    }

    fn find_link(
        &self,
        ino: u64,
        exclude_parent: u64,
        exclude_name: &str,
    ) -> Option<(u64, String)> {
        for (parent, children) in &self.children {
            for (name, child_ino) in children {
                if *child_ino == ino && !(*parent == exclude_parent && name == exclude_name) {
                    return Some((*parent, name.clone()));
                }
            }
        }
        None
    }

    pub fn remove_file_link(&mut self, parent: u64, name: &str) -> Result<(u64, bool), i32> {
        let ino = self.lookup_child(parent, name).ok_or(EINVAL)?;
        let was_primary = self
            .inodes
            .get(&ino)
            .map(|info| info.parent == parent && info.name == name)
            .unwrap_or(false);
        let replacement = if was_primary {
            self.find_link(ino, parent, name)
        } else {
            None
        };
        self.remove_child(parent, name);
        self.relpath_cache.remove(&ino);

        if let Some(info) = self.inodes.get_mut(&ino) {
            if info.nlink > 1 {
                info.nlink -= 1;
                if was_primary {
                    if let Some((next_parent, next_name)) = replacement {
                        info.parent = next_parent;
                        info.name = next_name;
                    }
                }
                return Ok((ino, false));
            }
        }

        self.remove_inode_subtree(ino);
        Ok((ino, true))
    }

    pub fn remove_inode_subtree(&mut self, ino: u64) {
        let child_inos: Vec<u64> = self
            .children
            .remove(&ino)
            .map(|children| children.into_values().collect())
            .unwrap_or_default();
        for child in child_inos {
            self.remove_inode_subtree(child);
        }
        self.relpath_cache.remove(&ino);
        self.inodes.remove(&ino);
    }

    fn is_descendant_or_self(&self, ino: u64, candidate_parent: u64) -> bool {
        let mut cur = candidate_parent;
        while cur != 0 {
            if cur == ino {
                return true;
            }
            cur = self.inodes.get(&cur).map(|info| info.parent).unwrap_or(0);
        }
        false
    }

    pub fn rename(&mut self, ino: u64, new_parent: u64, new_name: &str) -> Result<(), i32> {
        if self.is_descendant_or_self(ino, new_parent) {
            return Err(EINVAL);
        }

        // Invalidate relpath cache for this inode and all descendants
        self.relpath_cache.remove(&ino);
        self.invalidate_descendant_paths(ino);

        if let Some(info) = self.inodes.get_mut(&ino) {
            let old_parent = info.parent;
            let old_name = info.name.clone();
            info.name = new_name.to_string();
            info.parent = new_parent;

            // Remove from old parent
            if let Some(children) = self.children.get_mut(&old_parent) {
                children.remove(&old_name);
            }
            // Add to new parent
            self.children
                .entry(new_parent)
                .or_default()
                .insert(new_name.to_string(), ino);
        }
        Ok(())
    }

    pub fn rename_link(
        &mut self,
        ino: u64,
        old_parent: u64,
        old_name: &str,
        new_parent: u64,
        new_name: &str,
    ) -> Result<(), i32> {
        if self.is_descendant_or_self(ino, new_parent) {
            return Err(EINVAL);
        }

        if let Some(children) = self.children.get_mut(&old_parent) {
            children.remove(old_name);
        }
        self.children
            .entry(new_parent)
            .or_default()
            .insert(new_name.to_string(), ino);

        let is_primary = self
            .inodes
            .get(&ino)
            .map(|info| info.parent == old_parent && info.name == old_name)
            .unwrap_or(false);
        if is_primary {
            self.relpath_cache.remove(&ino);
            self.invalidate_descendant_paths(ino);
            if let Some(info) = self.inodes.get_mut(&ino) {
                info.parent = new_parent;
                info.name = new_name.to_string();
            }
        }
        Ok(())
    }

    fn invalidate_descendant_paths(&mut self, ino: u64) {
        let child_inos: Vec<u64> = self
            .children
            .get(&ino)
            .map(|c| c.values().copied().collect())
            .unwrap_or_default();
        for child in child_inos {
            self.relpath_cache.remove(&child);
            self.invalidate_descendant_paths(child);
        }
    }

    pub fn has_active_children(&self, ino: u64) -> bool {
        self.children
            .get(&ino)
            .map(|c| {
                c.values().any(|&child_ino| {
                    self.inodes
                        .get(&child_ino)
                        .map(|i| !i.deleted)
                        .unwrap_or(false)
                })
            })
            .unwrap_or(false)
    }

    pub fn active_directories_readonly(&self) -> Vec<(String, u32)> {
        let mut dirs = self
            .inodes
            .iter()
            .filter_map(|(&ino, info)| {
                if ino != ROOT_INODE && info.is_dir && !info.deleted {
                    Some((self.compute_relpath(ino), info.mode))
                } else {
                    None
                }
            })
            .collect::<Vec<_>>();
        dirs.sort_by(|a, b| a.0.cmp(&b.0));
        dirs
    }

    #[cfg(test)]
    pub fn inode_count(&self) -> usize {
        self.inodes.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::config::FileEntry;
    use std::fs;
    use std::os::unix::fs::PermissionsExt;
    use tempfile::TempDir;

    fn regular_entry(relpath: &str, md5: &str, size: u64) -> FileEntry {
        FileEntry {
            relpath: relpath.to_string(),
            md5: Some(md5.to_string()),
            size,
            isexec: false,
            islink: false,
            symlink_target: None,
            isdir: false,
            mode: None,
        }
    }

    fn exec_entry(relpath: &str, md5: &str, size: u64) -> FileEntry {
        FileEntry {
            isexec: true,
            ..regular_entry(relpath, md5, size)
        }
    }

    fn dir_entry(relpath: &str, mode: u32) -> FileEntry {
        FileEntry {
            relpath: relpath.to_string(),
            md5: None,
            size: 0,
            isexec: false,
            islink: false,
            symlink_target: None,
            isdir: true,
            mode: Some(mode),
        }
    }

    #[test]
    fn test_build_tree() {
        let mut tree = InodeTree::new();
        let entries = vec![
            regular_entry("a/b/file.txt", "abc", 100),
            exec_entry("a/other.txt", "def", 50),
        ];
        tree.build_from_manifest(&entries);

        // Root should have child "a"
        let root_children = tree.get_children(ROOT_INODE).unwrap();
        assert!(root_children.contains_key("a"));

        let a_ino = *root_children.get("a").unwrap();
        let a_children = tree.get_children(a_ino).unwrap();
        assert!(a_children.contains_key("b"));
        assert!(a_children.contains_key("other.txt"));

        // Check file attributes
        let other_ino = *a_children.get("other.txt").unwrap();
        let other = tree.get(other_ino).unwrap();
        assert_eq!(other.mode, 0o755); // isexec
        assert_eq!(other.size, 50);
    }

    #[test]
    fn test_regular_manifest_entry_ignores_symlink_target_metadata() {
        let mut tree = InodeTree::new();
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: Some("abc123".to_string()),
            size: 12,
            isexec: false,
            islink: false,
            symlink_target: Some("wrong-target".to_string()),
            isdir: false,
            mode: None,
        }];

        tree.build_from_manifest(&entries);

        let ino = tree.lookup_child(ROOT_INODE, "file.txt").unwrap();
        let info = tree.get(ino).unwrap();
        assert!(!info.is_symlink);
        assert_eq!(info.symlink_target, None);
    }

    #[test]
    fn test_relpath() {
        let mut tree = InodeTree::new();
        let entries = vec![regular_entry("a/b/c.txt", "x", 10)];
        tree.build_from_manifest(&entries);

        let root_children = tree.get_children(ROOT_INODE).unwrap();
        let a_ino = *root_children.get("a").unwrap();
        let a_children = tree.get_children(a_ino).unwrap();
        let b_ino = *a_children.get("b").unwrap();
        let b_children = tree.get_children(b_ino).unwrap();
        let c_ino = *b_children.get("c.txt").unwrap();

        assert_eq!(tree.get_relpath(c_ino), "a/b/c.txt");
        // Second call should use cache
        assert_eq!(tree.get_relpath(c_ino), "a/b/c.txt");
    }

    #[test]
    fn test_add_file_and_dir() {
        let mut tree = InodeTree::new();
        let dir_ino = tree.add_dir(ROOT_INODE, "mydir");
        let file_ino = tree.add_file(dir_ino, "test.txt", 0o644, false, "");

        assert_eq!(tree.get_relpath(file_ino), "mydir/test.txt");
        assert!(tree.get(dir_ino).unwrap().is_dir);
        assert!(!tree.get(file_ino).unwrap().is_dir);
    }

    #[test]
    fn test_manifest_lookup() {
        let mut tree = InodeTree::new();
        let entries = vec![regular_entry("data/file.bin", "hash", 1024)];
        tree.build_from_manifest(&entries);
        assert!(tree.is_in_manifest("data/file.bin"));
        assert!(!tree.is_in_manifest("data/other.bin"));
    }

    #[test]
    fn test_duplicate_manifest_paths_should_not_allocate_hidden_inodes() {
        let mut tree = InodeTree::new();
        let entries = vec![
            regular_entry("dup.txt", "hash-a", 1),
            regular_entry("dup.txt", "hash-b", 2),
        ];

        tree.build_from_manifest(&entries);

        assert_eq!(
            tree.inodes.len(),
            2,
            "duplicate manifest paths should be rejected instead of leaking hidden inodes"
        );
    }

    #[test]
    fn test_scan_overlay_should_not_add_children_under_manifest_file() {
        let tempdir = TempDir::new().unwrap();
        let overlay_dir = tempdir.path();
        fs::create_dir_all(overlay_dir.join("foo")).unwrap();
        fs::write(overlay_dir.join("foo").join("bar.txt"), b"hello").unwrap();

        let mut tree = InodeTree::new();
        tree.build_from_manifest(&[regular_entry("foo", "hash", 5)]);

        let foo_ino = tree.lookup_child(ROOT_INODE, "foo").unwrap();
        tree.scan_overlay(overlay_dir);

        assert!(
            tree.get_children(foo_ino).is_none(),
            "overlay scan should reject file/dir conflicts instead of attaching children to file inodes"
        );
    }

    #[test]
    fn test_scan_overlay_should_not_partially_add_unreadable_directories() {
        let tempdir = TempDir::new().unwrap();
        let overlay_dir = tempdir.path();
        let unreadable = overlay_dir.join("secret");
        fs::create_dir_all(&unreadable).unwrap();
        fs::set_permissions(&unreadable, fs::Permissions::from_mode(0)).unwrap();

        let mut tree = InodeTree::new();
        tree.scan_overlay(overlay_dir);

        fs::set_permissions(&unreadable, fs::Permissions::from_mode(0o755)).unwrap();

        assert!(
            tree.lookup_child(ROOT_INODE, "secret").is_none(),
            "overlay scan should error instead of partially adding unreadable directories"
        );
    }

    #[test]
    fn test_scan_overlay_should_preserve_directory_mode() {
        let tempdir = TempDir::new().unwrap();
        let overlay_dir = tempdir.path();
        let secret = overlay_dir.join("secret");
        fs::create_dir_all(&secret).unwrap();
        fs::set_permissions(&secret, fs::Permissions::from_mode(0o700)).unwrap();

        let mut tree = InodeTree::new();
        tree.scan_overlay(overlay_dir);

        let secret_ino = tree.lookup_child(ROOT_INODE, "secret").unwrap();
        let secret_info = tree.get(secret_ino).unwrap();
        assert!(secret_info.is_dir);
        assert_eq!(secret_info.mode, 0o700);
    }

    #[test]
    fn test_rename_should_not_move_directory_into_descendant() {
        let mut tree = InodeTree::new();
        let a_ino = tree.add_dir(ROOT_INODE, "a");
        let b_ino = tree.add_dir(a_ino, "b");

        assert_eq!(tree.rename(a_ino, b_ino, "newa"), Err(EINVAL));
        assert_eq!(tree.get(a_ino).unwrap().parent, ROOT_INODE);
    }

    #[test]
    fn test_build_tree_with_explicit_directory_entries_preserves_modes() {
        let mut tree = InodeTree::new();
        tree.build_from_manifest(&[
            dir_entry("runtime", 0o750),
            dir_entry("runtime/postgres", 0o700),
            regular_entry("runtime/postgres/PG_VERSION", "hash", 2),
        ]);

        let runtime_ino = tree.lookup_child(ROOT_INODE, "runtime").unwrap();
        let runtime = tree.get(runtime_ino).unwrap();
        assert!(runtime.is_dir);
        assert_eq!(runtime.mode, 0o750);
        assert_eq!(runtime.backing_relpath, "runtime");

        let postgres_ino = tree.lookup_child(runtime_ino, "postgres").unwrap();
        let postgres = tree.get(postgres_ino).unwrap();
        assert!(postgres.is_dir);
        assert_eq!(postgres.mode, 0o700);
        assert_eq!(postgres.backing_relpath, "runtime/postgres");
    }

    #[test]
    fn test_build_tree_with_legacy_file_manifest_still_synthesizes_parents() {
        let mut tree = InodeTree::new();
        tree.build_from_manifest(&[regular_entry("runtime/postgres/PG_VERSION", "hash", 2)]);

        let runtime_ino = tree.lookup_child(ROOT_INODE, "runtime").unwrap();
        let runtime = tree.get(runtime_ino).unwrap();
        assert!(runtime.is_dir);
        assert_eq!(runtime.mode, 0o755);
        assert_eq!(runtime.backing_relpath, "");
    }

    #[test]
    fn test_explicit_directory_entry_overrides_synthesized_parent_defaults() {
        let mut tree = InodeTree::new();
        tree.build_from_manifest(&[
            regular_entry("runtime/postgres/PG_VERSION", "hash", 2),
            dir_entry("runtime", 0o750),
        ]);

        let runtime_ino = tree.lookup_child(ROOT_INODE, "runtime").unwrap();
        let runtime = tree.get(runtime_ino).unwrap();
        assert!(runtime.is_dir);
        assert_eq!(runtime.mode, 0o750);
        assert_eq!(runtime.backing_relpath, "runtime");
    }

    #[test]
    fn test_active_directories_returns_sorted_non_root_dirs() {
        let mut tree = InodeTree::new();
        let runtime = tree.add_dir_with_mode(ROOT_INODE, "runtime", 0o750);
        let _postgres = tree.add_dir_with_mode(runtime, "postgres", 0o700);

        assert_eq!(
            tree.active_directories_readonly(),
            vec![
                ("runtime".to_string(), 0o750),
                ("runtime/postgres".to_string(), 0o700),
            ]
        );
    }

    #[test]
    fn test_directory_manifest_entry_wins_over_conflicting_file_entry() {
        let mut tree = InodeTree::new();
        tree.build_from_manifest(&[
            dir_entry("runtime", 0o750),
            regular_entry("runtime", "hash", 2),
        ]);

        let runtime_ino = tree.lookup_child(ROOT_INODE, "runtime").unwrap();
        let runtime = tree.get(runtime_ino).unwrap();
        assert!(runtime.is_dir);
        assert_eq!(runtime.mode, 0o750);
        assert_eq!(tree.inode_count(), 2);
    }
}
