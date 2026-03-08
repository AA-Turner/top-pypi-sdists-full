use crate::inode::{InodeInfo, InodeTree, ROOT_INODE};
use crate::s3::S3Downloader;
use fuser::{
    FileAttr, FileType, Filesystem, KernelConfig, ReplyAttr, ReplyCreate, ReplyData,
    ReplyDirectory, ReplyEmpty, ReplyEntry, ReplyOpen, ReplyStatfs, ReplyWrite, Request, TimeOrNow,
};
use libc::{EBADF, EEXIST, EIO, EISDIR, ELOOP, ENOENT, ENOTDIR, ENOTEMPTY};
use log::error;
use std::collections::{HashMap, HashSet};
use std::ffi::OsStr;
use std::os::unix::fs::PermissionsExt;
use std::os::unix::io::RawFd;
use std::path::PathBuf;
use std::sync::{Mutex, RwLock};
use std::time::{Duration, SystemTime};

const TTL: Duration = Duration::from_secs(5);
const BLOCK_SIZE: u32 = 4096;

struct OpenFile {
    fd: Option<RawFd>,
    access_mode: i32,
    /// Snapshot of visible overlay path at open() time — stable across rename/unlink
    overlay_relpath: String,
    /// Snapshot of info at open() time for stable reads
    info_snapshot: InodeInfo,
}

struct CreateOutcome {
    attr: FileAttr,
    fh: u64,
    flags_out: u32,
}

struct OpenOutcome {
    fh: u64,
    flags_out: u32,
}

pub struct LazyDvcFs {
    tree: RwLock<InodeTree>,
    overlay_dir: PathBuf,
    cache_dir: PathBuf,
    s3: Option<S3Downloader>,

    open_files: Mutex<HashMap<u64, OpenFile>>,
    next_fh: Mutex<u64>,

    modified: Mutex<HashSet<String>>,
    deleted: Mutex<HashSet<String>>,
    created: Mutex<HashSet<String>>,
}

impl LazyDvcFs {
    pub fn new(
        tree: InodeTree,
        overlay_dir: PathBuf,
        cache_dir: PathBuf,
        s3: Option<S3Downloader>,
    ) -> Self {
        LazyDvcFs {
            tree: RwLock::new(tree),
            overlay_dir,
            cache_dir,
            s3,
            open_files: Mutex::new(HashMap::new()),
            next_fh: Mutex::new(1),
            modified: Mutex::new(HashSet::new()),
            deleted: Mutex::new(HashSet::new()),
            created: Mutex::new(HashSet::new()),
        }
    }

    fn alloc_fh(&self) -> u64 {
        let mut fh = self.next_fh.lock().unwrap();
        let val = *fh;
        *fh += 1;
        val
    }

    fn access_mode(flags: i32) -> i32 {
        match flags & libc::O_ACCMODE {
            libc::O_WRONLY => libc::O_WRONLY,
            libc::O_RDWR => libc::O_RDWR,
            _ => libc::O_RDONLY,
        }
    }

    fn make_attr(&self, info: &InodeInfo) -> FileAttr {
        let now = SystemTime::now();
        let kind = if info.is_dir {
            FileType::Directory
        } else if info.is_symlink {
            FileType::Symlink
        } else {
            FileType::RegularFile
        };

        let perm = if info.is_symlink {
            0o777
        } else {
            info.mode as u16
        };

        let size = if info.is_dir {
            4096
        } else if info.is_symlink {
            info.symlink_target.len() as u64
        } else {
            info.size
        };

        let nlink = if info.is_dir { 2 } else { info.nlink };

        FileAttr {
            ino: info.ino,
            size,
            blocks: (size + 511) / 512,
            atime: now,
            mtime: now,
            ctime: now,
            crtime: now,
            kind,
            perm,
            nlink,
            uid: 1000,
            gid: 1000,
            rdev: 0,
            blksize: BLOCK_SIZE,
            flags: 0,
        }
    }

    fn visible_attr(&self, ino: u64, info: InodeInfo) -> FileAttr {
        let mut hydrated = info;
        let _ = self.hydrate_unknown_size(ino, &mut hydrated);
        self.make_attr(&hydrated)
    }

    fn overlay_path(&self, relpath: &str) -> PathBuf {
        self.overlay_dir.join(relpath)
    }

    fn cache_path(&self, relpath: &str) -> PathBuf {
        self.cache_dir.join("cache").join(relpath)
    }

    fn io_errno(err: &std::io::Error) -> i32 {
        err.raw_os_error().unwrap_or(libc::EIO)
    }

    fn name_to_string(name: &OsStr) -> Result<String, i32> {
        name.to_str()
            .map(|value| value.to_string())
            .ok_or(libc::EINVAL)
    }

    fn child_relpath(parent_relpath: &str, name: &str) -> String {
        if parent_relpath.is_empty() {
            name.to_string()
        } else {
            format!("{}/{}", parent_relpath, name)
        }
    }

    fn normalize_mode(mode: u32, umask: u32, default: u32) -> u32 {
        let perm = mode & 0o777;
        let perm = if perm == 0 { default } else { perm };
        perm & !umask
    }

    fn remap_tracked_paths(paths: &mut HashSet<String>, old_prefix: &str, new_prefix: &str) {
        let old_dir_prefix = format!("{}/", old_prefix);
        let mut updates = Vec::new();
        for path in paths.iter() {
            if path == old_prefix {
                updates.push((path.clone(), new_prefix.to_string()));
            } else if let Some(suffix) = path.strip_prefix(&old_dir_prefix) {
                updates.push((path.clone(), format!("{}/{}", new_prefix, suffix)));
            }
        }
        for (old, new) in updates {
            paths.remove(&old);
            paths.insert(new);
        }
    }

    fn materialize_overlay(
        &self,
        relpath: &str,
        source_relpath: &str,
        info: &InodeInfo,
    ) -> Result<PathBuf, i32> {
        let overlay = self.overlay_path(relpath);
        if let Some(parent) = overlay.parent() {
            std::fs::create_dir_all(parent).map_err(|e| Self::io_errno(&e))?;
        }
        if overlay.symlink_metadata().is_err() {
            if info.is_symlink {
                std::os::unix::fs::symlink(&info.symlink_target, &overlay)
                    .map_err(|e| Self::io_errno(&e))?;
            } else {
                let data = if !info.md5.is_empty() {
                    self.fetch_data(info, source_relpath)?
                } else {
                    Vec::new()
                };
                std::fs::write(&overlay, &data).map_err(|e| Self::io_errno(&e))?;
                std::fs::set_permissions(&overlay, std::fs::Permissions::from_mode(info.mode))
                    .map_err(|e| Self::io_errno(&e))?;
            }
        }
        Ok(overlay)
    }

    fn maybe_materialized_size(&self, relpath: &str, info: &InodeInfo) -> Option<u64> {
        let overlay = self.overlay_path(relpath);
        if let Ok(meta) = overlay.symlink_metadata() {
            return Some(if meta.file_type().is_symlink() {
                info.symlink_target.len() as u64
            } else {
                meta.len()
            });
        }

        if !info.md5.is_empty() {
            let cache = self.cache_path(relpath);
            if let Ok(meta) = cache.metadata() {
                return Some(meta.len());
            }
        }

        None
    }

    fn hydrate_unknown_size(&self, ino: u64, info: &mut InodeInfo) -> Result<(), i32> {
        if info.size != 0 || info.md5.is_empty() || info.is_symlink {
            return Ok(());
        }

        let actual_size =
            if let Some(size) = self.maybe_materialized_size(&info.backing_relpath, info) {
                size
            } else {
                self.fetch_data(info, &info.backing_relpath)?.len() as u64
            };

        info.size = actual_size;
        if let Some(tree_info) = self.tree.write().unwrap().get_mut(ino) {
            tree_info.size = actual_size;
        }
        Ok(())
    }

    fn fetch_data(&self, info: &InodeInfo, relpath: &str) -> Result<Vec<u8>, i32> {
        if info.is_symlink && !info.symlink_target.is_empty() {
            return Ok(info.symlink_target.as_bytes().to_vec());
        }

        // Check overlay
        let overlay = self.overlay_path(relpath);
        if overlay.symlink_metadata().is_ok() {
            if overlay
                .symlink_metadata()
                .map(|m| m.file_type().is_symlink())
                .unwrap_or(false)
            {
                let target = std::fs::read_link(&overlay)
                    .map_err(|_| EIO)?
                    .to_string_lossy()
                    .to_string();
                return Ok(target.into_bytes());
            }
            return std::fs::read(&overlay).map_err(|_| EIO);
        }

        // Check cache
        let cache = self.cache_path(relpath);
        if cache.exists() {
            return std::fs::read(&cache).map_err(|_| EIO);
        }

        // Download from S3
        if !info.md5.is_empty() {
            if let Some(s3) = &self.s3 {
                match s3.download(&info.md5) {
                    Ok(data) => {
                        if let Some(parent) = cache.parent() {
                            std::fs::create_dir_all(parent).map_err(|e| Self::io_errno(&e))?;
                        }
                        std::fs::write(&cache, &data).map_err(|e| Self::io_errno(&e))?;
                        return Ok(data);
                    }
                    Err(e) => {
                        error!("S3 download failed for {}: {}", info.md5, e);
                        return Err(libc::EIO);
                    }
                }
            }
        }

        Err(libc::EIO)
    }

    fn ensure_overlay_fd(&self, fh: u64, ino: u64) -> Result<RawFd, i32> {
        let mut files = self.open_files.lock().unwrap();
        let file = files.get_mut(&fh).ok_or(EBADF)?;

        if let Some(fd) = file.fd {
            return Ok(fd);
        }

        let relpath = file.overlay_relpath.clone();
        let info = file.info_snapshot.clone();
        let access_mode = file.access_mode;

        let overlay = self.overlay_path(&relpath);
        if let Some(parent) = overlay.parent() {
            std::fs::create_dir_all(parent).map_err(|_| EIO)?;
        }

        // Copy-on-write for manifest files
        if !overlay.exists() && !info.md5.is_empty() {
            drop(files); // Release lock before I/O
            let data = self.fetch_data(&info, &info.backing_relpath)?;
            std::fs::write(&overlay, &data).map_err(|_| EIO)?;
            std::fs::set_permissions(
                &overlay,
                std::os::unix::fs::PermissionsExt::from_mode(info.mode),
            )
            .map_err(|_| EIO)?;

            let mut tree = self.tree.write().unwrap();
            if let Some(i) = tree.get_mut(ino) {
                i.overlay = true;
            }
            if tree.is_in_manifest(&info.backing_relpath) {
                self.modified
                    .lock()
                    .unwrap()
                    .insert(info.backing_relpath.clone());
            } else {
                self.created.lock().unwrap().insert(relpath.clone());
            }
            files = self.open_files.lock().unwrap();
            let file = files.get_mut(&fh).ok_or(EBADF)?;

            let flags = access_mode;
            let fd = unsafe {
                libc::open(
                    std::ffi::CString::new(overlay.to_str().unwrap())
                        .unwrap()
                        .as_ptr(),
                    flags,
                    info.mode as libc::mode_t,
                )
            };
            if fd < 0 {
                return Err(std::io::Error::last_os_error()
                    .raw_os_error()
                    .unwrap_or(EIO));
            }
            file.fd = Some(fd);
            return Ok(fd);
        }

        {
            let mut tree = self.tree.write().unwrap();
            if let Some(i) = tree.get_mut(ino) {
                i.overlay = true;
            }
            if tree.is_in_manifest(&relpath) {
                self.modified.lock().unwrap().insert(relpath.clone());
            } else {
                self.created.lock().unwrap().insert(relpath.clone());
            }
        }

        let flags = if overlay.exists() {
            access_mode
        } else {
            access_mode | libc::O_CREAT
        };
        let fd = unsafe {
            libc::open(
                std::ffi::CString::new(overlay.to_str().unwrap())
                    .unwrap()
                    .as_ptr(),
                flags,
                info.mode as libc::mode_t,
            )
        };
        if fd < 0 {
            return Err(std::io::Error::last_os_error()
                .raw_os_error()
                .unwrap_or(libc::EIO));
        }
        file.fd = Some(fd);
        Ok(fd)
    }

    /// Ensure overlay parent dirs exist, return error on failure.
    fn ensure_overlay_parent(&self, overlay: &std::path::Path) -> Result<(), i32> {
        if let Some(parent) = overlay.parent() {
            std::fs::create_dir_all(parent).map_err(|e| {
                error!(
                    "Failed to create overlay parent dir {}: {}",
                    parent.display(),
                    e
                );
                EIO
            })?;
        }
        Ok(())
    }

    pub fn write_metadata(&self) {
        let meta = serde_json::json!({
            "modified": self.modified.lock().unwrap().iter().collect::<Vec<_>>(),
            "deleted": self.deleted.lock().unwrap().iter().collect::<Vec<_>>(),
            "created": self.created.lock().unwrap().iter().collect::<Vec<_>>(),
        });
        let meta_path = self.cache_dir.join("meta.json");
        if let Err(e) = std::fs::write(&meta_path, serde_json::to_string(&meta).unwrap()) {
            error!("Failed to write meta.json: {}", e);
        }
    }

    fn read_impl(&self, ino: u64, _fh: u64, offset: i64, size: u32) -> Result<Vec<u8>, i32> {
        let file_state = {
            let files = self.open_files.lock().unwrap();
            files.get(&_fh).map(|file| (file.fd, file.access_mode))
        };

        if let Some((fd, access_mode)) = file_state {
            if access_mode == libc::O_WRONLY {
                return Err(EBADF);
            }

            if let Some(fd) = fd {
                let mut buf = vec![0; size as usize];
                let read = unsafe {
                    libc::pread(fd, buf.as_mut_ptr() as *mut libc::c_void, buf.len(), offset)
                };
                if read < 0 {
                    return Err(std::io::Error::last_os_error()
                        .raw_os_error()
                        .unwrap_or(libc::EIO));
                }
                buf.truncate(read as usize);
                return Ok(buf);
            }
        }

        let mut tree = self.tree.write().unwrap();
        let info = tree.get(ino).cloned().ok_or(ENOENT)?;
        let relpath = if info.overlay {
            tree.get_relpath(ino)
        } else {
            info.backing_relpath.clone()
        };
        drop(tree);

        let data = self.fetch_data(&info, &relpath)?;
        if info.size == 0 && !info.md5.is_empty() && !info.is_symlink {
            if let Some(tree_info) = self.tree.write().unwrap().get_mut(ino) {
                if tree_info.size == 0 {
                    tree_info.size = data.len() as u64;
                }
            }
        }
        let start = offset as usize;
        if start >= data.len() {
            Ok(Vec::new())
        } else {
            let end = std::cmp::min(start + size as usize, data.len());
            Ok(data[start..end].to_vec())
        }
    }

    fn open_impl(&self, ino: u64, flags: i32) -> Result<OpenOutcome, i32> {
        let tree = self.tree.write().unwrap();
        let info = match tree.get(ino) {
            Some(i) if !i.deleted => i,
            _ => return Err(ENOENT),
        };
        if info.is_dir {
            return Err(EISDIR);
        }
        if info.is_symlink {
            return Err(ELOOP);
        }

        // Let the kernel cache immutable manifest-backed files when the true
        // size is known. Keep direct I/O only for the sentinel-size fallback.
        let was_unknown_size = !info.overlay && !info.md5.is_empty() && info.size == 0;
        let mut info_snapshot = info.clone();
        drop(tree);
        let _ = self.hydrate_unknown_size(ino, &mut info_snapshot);
        // If the kernel may have already observed the sentinel size for this
        // open, keep direct I/O enabled so readers see EOF instead of zero-padded
        // reads from a stale oversized page-cache view.
        let direct_io = was_unknown_size;
        let keep_cache = info_snapshot.overlay
            || (!was_unknown_size && !info_snapshot.md5.is_empty() && info_snapshot.size > 0);
        let mut tree = self.tree.write().unwrap();
        let relpath = tree.get_relpath(ino);
        drop(tree);

        // Open the overlay file if it exists, so reads/writes use the fast pread/pwrite path
        let fd = if info_snapshot.overlay {
            let overlay = self.overlay_path(&relpath);
            let c_path = std::ffi::CString::new(overlay.to_str().unwrap()).unwrap();
            let access = Self::access_mode(flags);
            let open_flags = if access == libc::O_WRONLY {
                libc::O_WRONLY
            } else if access == libc::O_RDWR {
                libc::O_RDWR
            } else {
                libc::O_RDONLY
            };
            let raw = unsafe { libc::open(c_path.as_ptr(), open_flags) };
            if raw >= 0 {
                Some(raw)
            } else {
                None
            }
        } else {
            None
        };

        let fh = self.alloc_fh();
        self.open_files.lock().unwrap().insert(
            fh,
            OpenFile {
                fd,
                access_mode: Self::access_mode(flags),
                overlay_relpath: relpath,
                info_snapshot,
            },
        );

        let mut flags_out: u32 = 0;
        if direct_io {
            flags_out |= fuser::consts::FOPEN_DIRECT_IO;
        }
        if keep_cache {
            flags_out |= fuser::consts::FOPEN_KEEP_CACHE;
        }

        Ok(OpenOutcome { fh, flags_out })
    }

    fn setattr_impl(
        &self,
        ino: u64,
        mode: Option<u32>,
        size: Option<u64>,
    ) -> Result<FileAttr, i32> {
        let mut tree = self.tree.write().unwrap();
        let info = match tree.get(ino) {
            Some(i) if !i.deleted => i.clone(),
            _ => return Err(ENOENT),
        };

        if info.is_symlink {
            return Ok(self.make_attr(&info));
        }

        let relpath = info.backing_relpath.clone();
        let path_rel = if info.is_dir {
            tree.get_relpath(ino)
        } else {
            relpath.clone()
        };

        if let Some(new_mode) = mode {
            let perm = new_mode & 0o777;
            drop(tree);
            let overlay = if info.is_dir {
                let overlay = self.overlay_path(&path_rel);
                std::fs::create_dir_all(&overlay).map_err(|e| Self::io_errno(&e))?;
                overlay
            } else {
                self.materialize_overlay(&relpath, &info.backing_relpath, &info)?
            };
            std::fs::set_permissions(&overlay, std::fs::Permissions::from_mode(perm))
                .map_err(|e| Self::io_errno(&e))?;
            tree = self.tree.write().unwrap();
            if let Some(i) = tree.get_mut(ino) {
                i.mode = perm;
                i.overlay = true;
            }
            if !info.is_dir && tree.is_in_manifest(&info.backing_relpath) {
                self.modified
                    .lock()
                    .unwrap()
                    .insert(info.backing_relpath.clone());
            } else if !info.is_dir {
                self.created.lock().unwrap().insert(relpath.clone());
            }
        }

        if !info.is_dir {
            if let Some(new_size) = size {
                drop(tree);
                let overlay = self.materialize_overlay(&relpath, &info.backing_relpath, &info)?;
                let file = std::fs::OpenOptions::new()
                    .write(true)
                    .open(&overlay)
                    .map_err(|e| Self::io_errno(&e))?;
                file.set_len(new_size).map_err(|e| Self::io_errno(&e))?;
                tree = self.tree.write().unwrap();
                if let Some(i) = tree.get_mut(ino) {
                    i.size = new_size;
                    i.overlay = true;
                }
                if tree.is_in_manifest(&info.backing_relpath) {
                    self.modified
                        .lock()
                        .unwrap()
                        .insert(info.backing_relpath.clone());
                } else {
                    self.created.lock().unwrap().insert(relpath.clone());
                }
            }
        }

        let updated = tree.get(ino).unwrap();
        Ok(self.make_attr(updated))
    }

    fn create_impl(&self, parent: u64, name: &OsStr, mode: u32) -> Result<CreateOutcome, i32> {
        let name_str = Self::name_to_string(name)?;
        let mut tree = self.tree.write().unwrap();

        if tree.get(parent).map(|i| !i.is_dir).unwrap_or(true) {
            return Err(ENOTDIR);
        }

        if let Some(existing) = tree.lookup_child(parent, &name_str) {
            if tree.get(existing).map(|i| !i.deleted).unwrap_or(false) {
                return Err(EEXIST);
            }
        }

        let perm = (mode & 0o777) as u32;
        let perm = if perm == 0 { 0o644 } else { perm };
        let parent_relpath = tree.get_relpath(parent);
        let relpath = Self::child_relpath(&parent_relpath, &name_str);
        drop(tree);

        let overlay = self.overlay_path(&relpath);
        if let Some(p) = overlay.parent() {
            std::fs::create_dir_all(p).map_err(|e| Self::io_errno(&e))?;
        }
        // Remove stale symlink/dir so open() with O_CREAT succeeds
        if let Ok(meta) = overlay.symlink_metadata() {
            if meta.is_dir() {
                let _ = std::fs::remove_dir_all(&overlay);
            } else if !meta.is_file() {
                let _ = std::fs::remove_file(&overlay);
            }
        }

        let c_path = std::ffi::CString::new(overlay.to_str().unwrap()).unwrap();
        let fd = unsafe {
            libc::open(
                c_path.as_ptr(),
                libc::O_WRONLY | libc::O_CREAT | libc::O_TRUNC,
                perm as libc::mode_t,
            )
        };
        if fd < 0 {
            return Err(std::io::Error::last_os_error()
                .raw_os_error()
                .unwrap_or(libc::EIO));
        }

        let mut tree = self.tree.write().unwrap();
        let ino = tree.add_file(parent, &name_str, perm, false, "");
        let fh = self.alloc_fh();
        let info_snapshot = tree.get(ino).unwrap().clone();
        self.open_files.lock().unwrap().insert(
            fh,
            OpenFile {
                fd: Some(fd),
                access_mode: libc::O_RDWR,
                overlay_relpath: relpath.clone(),
                info_snapshot,
            },
        );
        self.created.lock().unwrap().insert(relpath);

        let info = tree.get(ino).unwrap();
        let attr = self.make_attr(info);
        drop(tree);

        Ok(CreateOutcome {
            attr,
            fh,
            flags_out: fuser::consts::FOPEN_KEEP_CACHE,
        })
    }

    fn symlink_impl(
        &self,
        parent: u64,
        name: &OsStr,
        link: &std::path::Path,
    ) -> Result<FileAttr, i32> {
        let name_str = name.to_string_lossy().to_string();
        let target = link.to_string_lossy().to_string();

        let mut tree = self.tree.write().unwrap();
        if tree.get(parent).map(|i| !i.is_dir).unwrap_or(true) {
            return Err(ENOTDIR);
        }
        if let Some(existing) = tree.lookup_child(parent, &name_str) {
            if tree.get(existing).map(|i| !i.deleted).unwrap_or(false) {
                return Err(EEXIST);
            }
        }

        let ino = tree.add_file(parent, &name_str, 0o777, true, &target);
        let relpath = tree.get(ino).unwrap().backing_relpath.clone();

        let overlay = self.overlay_path(&relpath);
        if let Err(e) = self.ensure_overlay_parent(&overlay) {
            tree.remove_child(parent, &name_str);
            tree.remove_inode_subtree(ino);
            return Err(e);
        }
        // Remove stale overlay entry if it exists (e.g. from a prior unlink/rename)
        if overlay.symlink_metadata().is_ok() {
            if overlay.is_dir() {
                let _ = std::fs::remove_dir_all(&overlay);
            } else {
                let _ = std::fs::remove_file(&overlay);
            }
        }
        if let Err(e) = std::os::unix::fs::symlink(&target, &overlay) {
            error!("symlink failed: {}", e);
            tree.remove_child(parent, &name_str);
            tree.remove_inode_subtree(ino);
            return Err(EIO);
        }

        self.created.lock().unwrap().insert(relpath);
        let info = tree.get(ino).unwrap();
        Ok(self.make_attr(info))
    }

    fn unlink_impl(&self, parent: u64, name: &OsStr) -> Result<(), i32> {
        let name_str = Self::name_to_string(name)?;
        let mut tree = self.tree.write().unwrap();
        let parent_relpath = tree.get_relpath(parent);
        let relpath = Self::child_relpath(&parent_relpath, &name_str);

        let ino = tree.lookup_child(parent, &name_str).ok_or(ENOENT)?;
        let info = tree.get(ino).cloned().ok_or(ENOENT)?;
        if info.is_dir {
            return Err(EISDIR);
        }
        drop(tree);

        let overlay = self.overlay_path(&relpath);
        if overlay.symlink_metadata().is_ok() {
            std::fs::remove_file(&overlay).map_err(|e| Self::io_errno(&e))?;
        }

        let mut tree = self.tree.write().unwrap();
        let _ = tree
            .remove_file_link(parent, &name_str)
            .map_err(|_| ENOENT)?;
        self.created.lock().unwrap().remove(&relpath);
        self.deleted.lock().unwrap().insert(relpath);

        Ok(())
    }

    fn mkdir_impl(
        &self,
        parent: u64,
        name: &OsStr,
        mode: u32,
        umask: u32,
    ) -> Result<FileAttr, i32> {
        let name_str = Self::name_to_string(name)?;
        let mut tree = self.tree.write().unwrap();
        if tree.get(parent).map(|i| !i.is_dir).unwrap_or(true) {
            return Err(ENOTDIR);
        }
        if let Some(existing) = tree.lookup_child(parent, &name_str) {
            if tree.get(existing).map(|i| !i.deleted).unwrap_or(false) {
                return Err(EEXIST);
            }
        }
        let perm = Self::normalize_mode(mode, umask, 0o755);
        let parent_relpath = tree.get_relpath(parent);
        let relpath = Self::child_relpath(&parent_relpath, &name_str);
        drop(tree);

        let overlay = self.overlay_path(&relpath);
        if let Ok(meta) = overlay.symlink_metadata() {
            if !meta.is_dir() {
                if meta.file_type().is_symlink() || meta.is_file() {
                    let _ = std::fs::remove_file(&overlay);
                } else {
                    let _ = std::fs::remove_dir_all(&overlay);
                }
            }
        }
        std::fs::create_dir_all(&overlay).map_err(|e| Self::io_errno(&e))?;
        std::fs::set_permissions(&overlay, std::fs::Permissions::from_mode(perm))
            .map_err(|e| Self::io_errno(&e))?;

        let mut tree = self.tree.write().unwrap();
        let ino = tree.add_dir_with_mode(parent, &name_str, perm);
        let info = tree.get(ino).unwrap();
        Ok(self.make_attr(info))
    }

    fn rename_impl(
        &self,
        parent: u64,
        name: &OsStr,
        newparent: u64,
        newname: &OsStr,
    ) -> Result<(), i32> {
        let old_name = Self::name_to_string(name)?;
        let new_name = Self::name_to_string(newname)?;
        let mut tree = self.tree.write().unwrap();

        let ino = tree.lookup_child(parent, &old_name).ok_or(ENOENT)?;
        if tree.get(newparent).map(|info| !info.is_dir).unwrap_or(true) {
            return Err(ENOTDIR);
        }
        let mut cur = newparent;
        while cur != 0 {
            if cur == ino {
                return Err(libc::EINVAL);
            }
            cur = tree.get(cur).map(|info| info.parent).unwrap_or(0);
        }

        let info = tree.get(ino).cloned().ok_or(ENOENT)?;
        let parent_relpath = tree.get_relpath(parent);
        let old_relpath = Self::child_relpath(&parent_relpath, &old_name);
        let newparent_relpath = tree.get_relpath(newparent);
        let new_relpath = Self::child_relpath(&newparent_relpath, &new_name);
        let target_ino = tree.lookup_child(newparent, &new_name);
        let target_info = target_ino.and_then(|target_ino| tree.get(target_ino).cloned());
        if let Some(target_ino) = target_ino {
            if target_ino != ino
                && target_info
                    .as_ref()
                    .map(|target_info| target_info.is_dir && tree.has_active_children(target_ino))
                    .unwrap_or(false)
            {
                return Err(ENOTEMPTY);
            }
        }
        let in_manifest = tree.is_in_manifest(&info.backing_relpath);
        let move_backing = info.nlink == 1 && info.parent == parent && info.name == old_name;
        let old_backing_relpath = info.backing_relpath.clone();
        drop(tree);

        let old_overlay = self.overlay_path(&old_relpath);
        let new_overlay = self.overlay_path(&new_relpath);
        let had_old_overlay = old_overlay.symlink_metadata().is_ok();
        if had_old_overlay {
            if let Some(p) = new_overlay.parent() {
                std::fs::create_dir_all(p).map_err(|e| Self::io_errno(&e))?;
            }
            // Remove an existing empty target before the rename.
            if new_overlay.symlink_metadata().is_ok() {
                if new_overlay.is_dir() {
                    let _ = std::fs::remove_dir_all(&new_overlay);
                } else {
                    let _ = std::fs::remove_file(&new_overlay);
                }
            }
            std::fs::rename(&old_overlay, &new_overlay).map_err(|e| Self::io_errno(&e))?;
        } else if move_backing && in_manifest {
            self.materialize_overlay(&new_relpath, &old_backing_relpath, &info)?;
        }

        let old_cache = self.cache_path(&old_backing_relpath);
        let new_cache = self.cache_path(&new_relpath);
        if move_backing && old_cache.exists() {
            if let Some(p) = new_cache.parent() {
                std::fs::create_dir_all(p).map_err(|e| Self::io_errno(&e))?;
            }
            std::fs::rename(&old_cache, &new_cache).map_err(|e| Self::io_errno(&e))?;
        }

        let mut tree = self.tree.write().unwrap();
        if let Some(target_ino) = target_ino {
            if target_ino != ino {
                if let Some(target_info) = target_info {
                    if target_info.is_dir {
                        if let Some(target) = tree.get_mut(target_ino) {
                            target.deleted = true;
                        }
                        tree.remove_inode_subtree(target_ino);
                    } else {
                        let _ = tree
                            .remove_file_link(newparent, &new_name)
                            .map_err(|_| ENOENT)?;
                    }
                }
                self.deleted.lock().unwrap().insert(new_relpath.clone());
            }
        }

        if info.nlink > 1 {
            tree.rename_link(ino, parent, &old_name, newparent, &new_name)?;
        } else {
            tree.rename(ino, newparent, &new_name)?;
        }

        {
            let mut created = self.created.lock().unwrap();
            let mut modified = self.modified.lock().unwrap();
            Self::remap_tracked_paths(&mut created, &old_relpath, &new_relpath);
            if move_backing {
                Self::remap_tracked_paths(&mut modified, &old_backing_relpath, &new_relpath);
            }
        }

        if move_backing && in_manifest {
            self.deleted.lock().unwrap().insert(old_backing_relpath);
            self.created.lock().unwrap().insert(new_relpath.clone());
        }
        if let Some(i) = tree.get_mut(ino) {
            i.overlay = info.overlay || in_manifest || had_old_overlay;
            if move_backing {
                i.backing_relpath = new_relpath.clone();
            }
        }

        Ok(())
    }

    fn link_impl(&self, ino: u64, newparent: u64, newname: &OsStr) -> Result<FileAttr, i32> {
        let newname_str = newname.to_string_lossy().to_string();
        let mut tree = self.tree.write().unwrap();

        let src_info = match tree.get(ino) {
            Some(i) if !i.deleted && !i.is_dir => i.clone(),
            _ => return Err(ENOENT),
        };
        if tree.get(newparent).map(|i| !i.is_dir).unwrap_or(true) {
            return Err(ENOTDIR);
        }
        if let Some(existing) = tree.lookup_child(newparent, &newname_str) {
            if tree.get(existing).map(|i| !i.deleted).unwrap_or(false) {
                return Err(EEXIST);
            }
        }

        let src_relpath = tree.get_relpath(ino);
        let parent_relpath = tree.get_relpath(newparent);
        let new_relpath = Self::child_relpath(&parent_relpath, &newname_str);
        drop(tree);

        let src_overlay =
            self.materialize_overlay(&src_relpath, &src_info.backing_relpath, &src_info)?;
        let dst_overlay = self.overlay_path(&new_relpath);
        if let Some(parent) = dst_overlay.parent() {
            std::fs::create_dir_all(parent).map_err(|e| Self::io_errno(&e))?;
        }
        if dst_overlay.symlink_metadata().is_ok() {
            if dst_overlay.is_dir() {
                let _ = std::fs::remove_dir_all(&dst_overlay);
            } else {
                let _ = std::fs::remove_file(&dst_overlay);
            }
        }
        std::fs::hard_link(&src_overlay, &dst_overlay).map_err(|e| Self::io_errno(&e))?;

        let mut tree = self.tree.write().unwrap();
        tree.add_link(ino, newparent, &newname_str)
            .map_err(|_| EIO)?;
        if let Some(info) = tree.get_mut(ino) {
            info.overlay = true;
        }
        self.created.lock().unwrap().insert(new_relpath);
        let info = tree.get(ino).unwrap();
        Ok(self.make_attr(info))
    }
}

impl Filesystem for LazyDvcFs {
    fn init(&mut self, _req: &Request, config: &mut KernelConfig) -> Result<(), libc::c_int> {
        config
            .add_capabilities(fuser::consts::FUSE_WRITEBACK_CACHE)
            .ok();
        Ok(())
    }

    fn destroy(&mut self) {
        self.write_metadata();
        let files = self.open_files.lock().unwrap();
        for (_, file) in files.iter() {
            if let Some(fd) = file.fd {
                unsafe { libc::close(fd) };
            }
        }
    }

    fn lookup(&mut self, _req: &Request, parent: u64, name: &OsStr, reply: ReplyEntry) {
        let name_str = name.to_string_lossy();
        let tree = self.tree.read().unwrap();
        if let Some(ino) = tree.lookup_child(parent, &name_str) {
            if let Some(info) = tree.get(ino).cloned() {
                if info.deleted {
                    reply.error(ENOENT);
                    return;
                }
                drop(tree);
                reply.entry(&TTL, &self.visible_attr(ino, info), 0);
                return;
            }
        }
        reply.error(ENOENT);
    }

    fn mknod(
        &mut self,
        _req: &Request,
        parent: u64,
        name: &OsStr,
        mode: u32,
        _umask: u32,
        _rdev: u32,
        reply: ReplyEntry,
    ) {
        let node_type = mode & libc::S_IFMT;
        if node_type != 0 && node_type != libc::S_IFREG {
            reply.error(libc::EPERM);
            return;
        }

        match self.create_impl(parent, name, mode) {
            Ok(outcome) => {
                if let Some(open_file) = self.open_files.lock().unwrap().remove(&outcome.fh) {
                    if let Some(fd) = open_file.fd {
                        unsafe { libc::close(fd) };
                    }
                }
                reply.entry(&TTL, &outcome.attr, 0);
            }
            Err(e) => reply.error(e),
        }
    }

    fn getattr(&mut self, _req: &Request, ino: u64, _fh: Option<u64>, reply: ReplyAttr) {
        let tree = self.tree.read().unwrap();
        if let Some(info) = tree.get(ino).cloned() {
            if info.deleted {
                reply.error(ENOENT);
                return;
            }
            drop(tree);
            reply.attr(&TTL, &self.visible_attr(ino, info));
        } else {
            reply.error(ENOENT);
        }
    }

    fn setattr(
        &mut self,
        _req: &Request,
        ino: u64,
        mode: Option<u32>,
        _uid: Option<u32>,
        _gid: Option<u32>,
        size: Option<u64>,
        _atime: Option<TimeOrNow>,
        _mtime: Option<TimeOrNow>,
        _ctime: Option<SystemTime>,
        _fh: Option<u64>,
        _crtime: Option<SystemTime>,
        _chgtime: Option<SystemTime>,
        _bkuptime: Option<SystemTime>,
        _flags: Option<u32>,
        reply: ReplyAttr,
    ) {
        match self.setattr_impl(ino, mode, size) {
            Ok(attr) => reply.attr(&TTL, &attr),
            Err(e) => reply.error(e),
        }
    }

    fn readdir(
        &mut self,
        _req: &Request,
        ino: u64,
        _fh: u64,
        offset: i64,
        mut reply: ReplyDirectory,
    ) {
        let tree = self.tree.read().unwrap();
        let dir_info = match tree.get(ino) {
            Some(info) if info.is_dir && !info.deleted => info,
            _ => {
                reply.error(ENOTDIR);
                return;
            }
        };
        let children = match tree.get_children(ino) {
            Some(c) => c,
            None => {
                reply.error(ENOTDIR);
                return;
            }
        };

        let parent_ino = if ino == ROOT_INODE || dir_info.parent == 0 {
            ROOT_INODE
        } else {
            dir_info.parent
        };

        let mut entries: Vec<(String, u64, FileType)> = vec![
            (".".to_string(), ino, FileType::Directory),
            ("..".to_string(), parent_ino, FileType::Directory),
        ];
        entries.extend(
            children
                .iter()
                .filter_map(|(name, &cino)| {
                    tree.get(cino).filter(|i| !i.deleted).map(|info| {
                        let kind = if info.is_dir {
                            FileType::Directory
                        } else if info.is_symlink {
                            FileType::Symlink
                        } else {
                            FileType::RegularFile
                        };
                        (name.clone(), cino, kind)
                    })
                })
                .collect::<Vec<_>>(),
        );
        entries[2..].sort_by(|a, b| a.0.cmp(&b.0));

        for (i, (name, cino, kind)) in entries.iter().enumerate().skip(offset as usize) {
            if reply.add(*cino, (i + 1) as i64, *kind, &name) {
                break;
            }
        }
        reply.ok();
    }

    fn open(&mut self, _req: &Request, ino: u64, flags: i32, reply: ReplyOpen) {
        match self.open_impl(ino, flags) {
            Ok(outcome) => reply.opened(outcome.fh, outcome.flags_out),
            Err(e) => reply.error(e),
        }
    }

    fn read(
        &mut self,
        _req: &Request,
        ino: u64,
        fh: u64,
        offset: i64,
        size: u32,
        _flags: i32,
        _lock_owner: Option<u64>,
        reply: ReplyData,
    ) {
        match self.read_impl(ino, fh, offset, size) {
            Ok(data) => reply.data(&data),
            Err(e) => reply.error(e),
        }
    }

    fn write(
        &mut self,
        _req: &Request,
        ino: u64,
        fh: u64,
        offset: i64,
        data: &[u8],
        _write_flags: u32,
        _flags: i32,
        _lock_owner: Option<u64>,
        reply: ReplyWrite,
    ) {
        let fd = match self.ensure_overlay_fd(fh, ino) {
            Ok(fd) => fd,
            Err(e) => {
                reply.error(e);
                return;
            }
        };

        let written =
            unsafe { libc::pwrite(fd, data.as_ptr() as *const libc::c_void, data.len(), offset) };
        if written < 0 {
            reply.error(
                std::io::Error::last_os_error()
                    .raw_os_error()
                    .unwrap_or(EIO),
            );
            return;
        }

        let written = written as u32;
        let new_size = offset as u64 + written as u64;
        let mut tree = self.tree.write().unwrap();
        if let Some(info) = tree.get_mut(ino) {
            if new_size > info.size {
                info.size = new_size;
            }
        }
        reply.written(written);
    }

    fn create(
        &mut self,
        _req: &Request,
        parent: u64,
        name: &OsStr,
        mode: u32,
        _umask: u32,
        _flags: i32,
        reply: ReplyCreate,
    ) {
        match self.create_impl(parent, name, mode) {
            Ok(outcome) => reply.created(&TTL, &outcome.attr, 0, outcome.fh, outcome.flags_out),
            Err(e) => reply.error(e),
        }
    }

    fn unlink(&mut self, _req: &Request, parent: u64, name: &OsStr, reply: ReplyEmpty) {
        match self.unlink_impl(parent, name) {
            Ok(()) => reply.ok(),
            Err(e) => reply.error(e),
        }
    }

    fn symlink(
        &mut self,
        _req: &Request,
        parent: u64,
        name: &OsStr,
        link: &std::path::Path,
        reply: ReplyEntry,
    ) {
        match self.symlink_impl(parent, name, link) {
            Ok(attr) => reply.entry(&TTL, &attr, 0),
            Err(e) => reply.error(e),
        }
    }

    fn link(
        &mut self,
        _req: &Request,
        ino: u64,
        newparent: u64,
        newname: &OsStr,
        reply: ReplyEntry,
    ) {
        match self.link_impl(ino, newparent, newname) {
            Ok(attr) => reply.entry(&TTL, &attr, 0),
            Err(e) => reply.error(e),
        }
    }

    fn readlink(&mut self, _req: &Request, ino: u64, reply: ReplyData) {
        let tree = self.tree.read().unwrap();
        match tree.get(ino) {
            Some(i) if !i.deleted && i.is_symlink => {
                reply.data(i.symlink_target.as_bytes());
            }
            _ => {
                reply.error(ENOENT);
            }
        }
    }

    fn mkdir(
        &mut self,
        _req: &Request,
        parent: u64,
        name: &OsStr,
        mode: u32,
        umask: u32,
        reply: ReplyEntry,
    ) {
        match self.mkdir_impl(parent, name, mode, umask) {
            Ok(attr) => reply.entry(&TTL, &attr, 0),
            Err(e) => reply.error(e),
        }
    }

    fn rmdir(&mut self, _req: &Request, parent: u64, name: &OsStr, reply: ReplyEmpty) {
        let name_str = name.to_string_lossy().to_string();
        let mut tree = self.tree.write().unwrap();

        let ino = match tree.lookup_child(parent, &name_str) {
            Some(ino) => ino,
            None => {
                reply.error(ENOENT);
                return;
            }
        };

        if tree.get(ino).map(|i| !i.is_dir).unwrap_or(true) {
            reply.error(ENOTDIR);
            return;
        }

        if tree.has_active_children(ino) {
            reply.error(ENOTEMPTY);
            return;
        }

        tree.remove_child(parent, &name_str);
        if let Some(info) = tree.get_mut(ino) {
            info.deleted = true;
        }
        reply.ok();
    }

    fn rename(
        &mut self,
        _req: &Request,
        parent: u64,
        name: &OsStr,
        newparent: u64,
        newname: &OsStr,
        _flags: u32,
        reply: ReplyEmpty,
    ) {
        match self.rename_impl(parent, name, newparent, newname) {
            Ok(()) => reply.ok(),
            Err(e) => reply.error(e),
        }
    }

    fn release(
        &mut self,
        _req: &Request,
        _ino: u64,
        fh: u64,
        _flags: i32,
        _lock_owner: Option<u64>,
        _flush: bool,
        reply: ReplyEmpty,
    ) {
        let file = self.open_files.lock().unwrap().remove(&fh);
        if let Some(f) = file {
            if let Some(fd) = f.fd {
                unsafe { libc::close(fd) };
            }
        }
        reply.ok();
    }

    fn opendir(&mut self, _req: &Request, ino: u64, _flags: i32, reply: ReplyOpen) {
        let tree = self.tree.read().unwrap();
        if tree.get(ino).map(|i| i.is_dir).unwrap_or(false) {
            reply.opened(ino, 0);
        } else {
            reply.error(ENOTDIR);
        }
    }

    fn releasedir(&mut self, _req: &Request, _ino: u64, _fh: u64, _flags: i32, reply: ReplyEmpty) {
        reply.ok();
    }

    fn statfs(&mut self, _req: &Request, _ino: u64, reply: ReplyStatfs) {
        reply.statfs(
            1024 * 1024, // blocks
            512 * 1024,  // bfree
            512 * 1024,  // bavail
            100_000,     // files
            1_000_000,   // ffree
            BLOCK_SIZE,  // bsize
            255,         // namelen
            BLOCK_SIZE,  // frsize
        );
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::config::FileEntry;
    use crate::inode::ROOT_INODE;
    use fuser::{spawn_mount2, BackgroundSession, MountOption};
    use serial_test::serial;
    use std::ffi::OsStr;
    use std::fs::{self, File};
    use std::io::{Read, Seek, SeekFrom};
    use std::os::unix::ffi::OsStrExt;
    use std::os::unix::fs::MetadataExt;
    use std::path::Path;
    use std::process::Command;
    use std::thread;
    use tempfile::TempDir;

    struct MountedFs {
        _state_dir: TempDir,
        mount_dir: TempDir,
        session: Option<BackgroundSession>,
    }

    impl MountedFs {
        fn mount(fs: LazyDvcFs, state_dir: TempDir) -> Self {
            let mount_dir = TempDir::new().unwrap();
            let options = vec![
                MountOption::FSName("plato-fuse-test".to_string()),
                MountOption::RW,
            ];
            let session = spawn_mount2(fs, mount_dir.path(), &options).unwrap();
            MountedFs {
                _state_dir: state_dir,
                mount_dir,
                session: Some(session),
            }
        }

        fn path(&self) -> &Path {
            self.mount_dir.path()
        }

        fn wait_for(&self, relpath: &str) {
            let target = self.path().join(relpath);
            for _ in 0..100 {
                if target.exists() {
                    return;
                }
                thread::sleep(Duration::from_millis(20));
            }
            panic!("mounted path was not ready: {}", target.display());
        }
    }

    impl Drop for MountedFs {
        fn drop(&mut self) {
            if let Some(session) = self.session.take() {
                session.join();
            }
        }
    }

    fn build_fs(
        entries: &[FileEntry],
        setup: impl FnOnce(&Path, &Path),
    ) -> (LazyDvcFs, TempDir, Vec<u64>) {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        tree.build_from_manifest(entries);
        let inos = entries
            .iter()
            .map(|entry| lookup_path(&tree, &entry.relpath))
            .collect::<Vec<_>>();

        setup(&overlay_dir, &cache_dir);
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);
        (fs, state_dir, inos)
    }

    fn lookup_path(tree: &InodeTree, relpath: &str) -> u64 {
        let mut parent = ROOT_INODE;
        for part in relpath.split('/') {
            parent = tree.lookup_child(parent, part).unwrap();
        }
        parent
    }

    fn close_handle(fs: &LazyDvcFs, fh: u64) {
        let file = fs.open_files.lock().unwrap().remove(&fh);
        if let Some(file) = file {
            if let Some(fd) = file.fd {
                unsafe { libc::close(fd) };
            }
        }
    }

    fn fuse_available() -> bool {
        Path::new("/dev/fuse").exists()
    }

    #[test]
    fn fetch_data_without_backing_source_should_error() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, _cache| {});
        let mut tree = fs.tree.write().unwrap();
        let ino = inos[0];
        let info = tree.get(ino).unwrap().clone();
        let relpath = tree.get_relpath(ino);
        drop(tree);

        assert!(fs.fetch_data(&info, &relpath).is_err());
    }

    #[test]
    fn ensure_overlay_fd_should_materialize_manifest_file_and_track_modified() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });
        let ino = inos[0];
        let open = fs.open_impl(ino, libc::O_WRONLY).unwrap();

        let fd = fs.ensure_overlay_fd(open.fh, ino).unwrap();
        let written = unsafe { libc::pwrite(fd, b"YY".as_ptr() as *const libc::c_void, 2, 2) };
        assert_eq!(written, 2);
        close_handle(&fs, open.fh);

        assert_eq!(fs::read(fs.overlay_path("file.txt")).unwrap(), b"heYYo");
        assert!(fs.modified.lock().unwrap().contains("file.txt"));
        assert!(!fs.created.lock().unwrap().contains("file.txt"));
        assert!(fs.tree.read().unwrap().get(ino).unwrap().overlay);
    }

    #[test]
    fn read_impl_should_allow_read_after_write_on_materialized_rdwr_handle() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });
        let ino = inos[0];
        let open = fs.open_impl(ino, libc::O_RDWR).unwrap();

        let fd = fs.ensure_overlay_fd(open.fh, ino).unwrap();
        let written = unsafe { libc::pwrite(fd, b"YY".as_ptr() as *const libc::c_void, 2, 2) };
        assert_eq!(written, 2);

        let data = fs.read_impl(ino, open.fh, 0, 5).unwrap();
        assert_eq!(data, b"heYYo");
        close_handle(&fs, open.fh);
    }

    #[test]
    fn read_impl_should_reject_write_only_materialized_handle() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });
        let ino = inos[0];
        let open = fs.open_impl(ino, libc::O_WRONLY).unwrap();

        let fd = fs.ensure_overlay_fd(open.fh, ino).unwrap();
        let written = unsafe { libc::pwrite(fd, b"YY".as_ptr() as *const libc::c_void, 2, 2) };
        assert_eq!(written, 2);

        assert_eq!(fs.read_impl(ino, open.fh, 0, 5), Err(EBADF));
        close_handle(&fs, open.fh);
    }

    #[test]
    fn open_impl_should_set_expected_flags() {
        let entries = vec![
            FileEntry {
                relpath: "known.txt".to_string(),
                md5: "abcdef".to_string(),
                size: 5,
                isexec: false,
                islink: false,
                symlink_target: String::new(),
            },
            FileEntry {
                relpath: "unknown.txt".to_string(),
                md5: "123456".to_string(),
                size: 0,
                isexec: false,
                islink: false,
                symlink_target: String::new(),
            },
        ];
        let (fs, _state_dir, inos) = build_fs(&entries, |overlay, _cache| {
            fs::write(overlay.join("overlay.txt"), b"data").unwrap();
        });
        let overlay_ino = {
            let mut tree = fs.tree.write().unwrap();
            let ino = tree.add_file(ROOT_INODE, "overlay.txt", 0o644, false, "");
            if let Some(info) = tree.get_mut(ino) {
                info.overlay = true;
                info.size = 4;
            }
            let link_ino = tree.add_file(ROOT_INODE, "link.txt", 0o777, true, "target.txt");
            if let Some(info) = tree.get_mut(link_ino) {
                info.size = "target.txt".len() as u64;
            }
            ino
        };

        let known = fs.open_impl(inos[0], libc::O_RDONLY).unwrap();
        assert_eq!(known.flags_out & fuser::consts::FOPEN_DIRECT_IO, 0);
        assert_ne!(known.flags_out & fuser::consts::FOPEN_KEEP_CACHE, 0);
        close_handle(&fs, known.fh);

        let unknown = fs.open_impl(inos[1], libc::O_RDONLY).unwrap();
        assert_ne!(unknown.flags_out & fuser::consts::FOPEN_DIRECT_IO, 0);
        assert_eq!(unknown.flags_out & fuser::consts::FOPEN_KEEP_CACHE, 0);
        close_handle(&fs, unknown.fh);

        let overlay = fs.open_impl(overlay_ino, libc::O_RDWR).unwrap();
        assert_eq!(overlay.flags_out & fuser::consts::FOPEN_DIRECT_IO, 0);
        assert_ne!(overlay.flags_out & fuser::consts::FOPEN_KEEP_CACHE, 0);
        close_handle(&fs, overlay.fh);

        assert!(matches!(
            fs.open_impl(ROOT_INODE, libc::O_RDONLY),
            Err(EISDIR)
        ));
        let link_ino = lookup_path(&fs.tree.read().unwrap(), "link.txt");
        assert!(matches!(fs.open_impl(link_ino, libc::O_RDONLY), Err(ELOOP)));
    }

    #[test]
    fn open_impl_should_hydrate_cached_unknown_size_manifest_file() {
        let entries = vec![FileEntry {
            relpath: "unknown.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 0,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/unknown.txt"), b"hello world").unwrap();
        });

        let first_open = fs.open_impl(inos[0], libc::O_RDONLY).unwrap();
        assert_ne!(first_open.flags_out & fuser::consts::FOPEN_DIRECT_IO, 0);
        assert_eq!(first_open.flags_out & fuser::consts::FOPEN_KEEP_CACHE, 0);
        close_handle(&fs, first_open.fh);

        assert_eq!(fs.tree.read().unwrap().get(inos[0]).unwrap().size, 11);

        let second_open = fs.open_impl(inos[0], libc::O_RDONLY).unwrap();
        assert_eq!(second_open.flags_out & fuser::consts::FOPEN_DIRECT_IO, 0);
        assert_ne!(second_open.flags_out & fuser::consts::FOPEN_KEEP_CACHE, 0);
        close_handle(&fs, second_open.fh);
    }

    #[test]
    fn visible_attr_should_hydrate_unknown_size_manifest_file() {
        let entries = vec![FileEntry {
            relpath: "unknown.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 0,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/unknown.txt"), b"hello world").unwrap();
        });

        let info = fs.tree.read().unwrap().get(inos[0]).unwrap().clone();
        let attr = fs.visible_attr(inos[0], info);

        assert_eq!(attr.size, 11);
        assert_eq!(fs.tree.read().unwrap().get(inos[0]).unwrap().size, 11);
    }

    #[test]
    fn visible_attr_should_return_zero_when_unknown_size_hydration_fails() {
        let entries = vec![FileEntry {
            relpath: "unknown.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 0,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, _cache| {});

        let info = fs.tree.read().unwrap().get(inos[0]).unwrap().clone();
        let attr = fs.visible_attr(inos[0], info);

        assert_eq!(attr.size, 0);
        assert_eq!(fs.tree.read().unwrap().get(inos[0]).unwrap().size, 0);
    }

    #[test]
    fn create_should_propagate_overlay_creation_failure() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("blocked"), b"not a directory").unwrap();

        let mut tree = InodeTree::new();
        let blocked_ino = tree.add_dir(ROOT_INODE, "blocked");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert!(fs
            .create_impl(blocked_ino, OsStr::new("new.txt"), 0o644)
            .is_err());
    }

    #[test]
    fn setattr_should_propagate_overlay_write_failure() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("blocked"), b"not a directory").unwrap();

        let mut tree = InodeTree::new();
        let blocked_ino = tree.add_dir(ROOT_INODE, "blocked");
        let file_ino = tree.add_file(blocked_ino, "file.txt", 0o644, false, "");
        if let Some(info) = tree.get_mut(file_ino) {
            info.overlay = false;
        }
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert!(fs.setattr_impl(file_ino, None, Some(10)).is_err());
    }

    #[test]
    fn setattr_should_propagate_overlay_permission_failure() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("blocked"), b"not a directory").unwrap();

        let mut tree = InodeTree::new();
        let blocked_ino = tree.add_dir(ROOT_INODE, "blocked");
        let file_ino = tree.add_file(blocked_ino, "file.txt", 0o644, false, "");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert!(fs.setattr_impl(file_ino, Some(0o600), None).is_err());
    }

    #[test]
    fn rename_should_propagate_overlay_move_failure() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("old.txt"), b"hello").unwrap();
        fs::write(overlay_dir.join("blocked"), b"not a directory").unwrap();

        let mut tree = InodeTree::new();
        tree.add_file(ROOT_INODE, "old.txt", 0o644, false, "");
        let blocked_ino = tree.add_dir(ROOT_INODE, "blocked");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert!(fs
            .rename_impl(
                ROOT_INODE,
                OsStr::new("old.txt"),
                blocked_ino,
                OsStr::new("new.txt")
            )
            .is_err());
    }

    #[test]
    fn read_should_follow_open_handle_after_rename() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });
        let ino = inos[0];
        let open = fs.open_impl(ino, 0).unwrap();

        assert_eq!(fs.read_impl(ino, open.fh, 0, 5).unwrap(), b"hello");
        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("file.txt"),
            ROOT_INODE,
            OsStr::new("renamed.txt"),
        )
        .unwrap();
        assert_eq!(fs.read_impl(ino, open.fh, 0, 5).unwrap(), b"hello");
        close_handle(&fs, open.fh);
    }

    #[test]
    fn read_should_follow_open_handle_after_unlink() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("file.txt"), b"hello").unwrap();

        let mut tree = InodeTree::new();
        let ino = tree.add_file(ROOT_INODE, "file.txt", 0o644, false, "");
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        let fd = unsafe {
            libc::open(
                std::ffi::CString::new(overlay_dir.join("file.txt").to_str().unwrap())
                    .unwrap()
                    .as_ptr(),
                libc::O_RDONLY,
            )
        };
        assert!(fd >= 0);
        let fh = fs.alloc_fh();
        fs.open_files.lock().unwrap().insert(
            fh,
            OpenFile {
                fd: Some(fd),
                access_mode: libc::O_RDONLY,
                overlay_relpath: "file.txt".to_string(),
                info_snapshot: InodeInfo {
                    ino,
                    name: "file.txt".to_string(),
                    parent: ROOT_INODE,
                    backing_relpath: "file.txt".to_string(),
                    is_dir: false,
                    md5: String::new(),
                    size: 5,
                    mode: 0o644,
                    is_symlink: false,
                    symlink_target: String::new(),
                    nlink: 1,
                    overlay: true,
                    deleted: false,
                },
            },
        );

        fs.unlink_impl(ROOT_INODE, OsStr::new("file.txt")).unwrap();
        let data = fs.read_impl(ino, fh, 0, 5).unwrap();
        close_handle(&fs, fh);

        assert_eq!(data, b"hello");
    }

    #[test]
    fn unlink_should_reject_directories() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(overlay_dir.join("dir")).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        tree.add_dir(ROOT_INODE, "dir");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert_eq!(fs.unlink_impl(ROOT_INODE, OsStr::new("dir")), Err(EISDIR));
    }

    #[test]
    fn rename_should_update_descendant_metadata_paths() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        let dir_ino = tree.add_dir(ROOT_INODE, "dir");
        tree.add_file(dir_ino, "a.txt", 0o644, false, "");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir.clone(), None);
        fs.created.lock().unwrap().insert("dir/a.txt".to_string());

        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("dir"),
            ROOT_INODE,
            OsStr::new("dir2"),
        )
        .unwrap();
        fs.write_metadata();

        let meta: serde_json::Value =
            serde_json::from_str(&std::fs::read_to_string(cache_dir.join("meta.json")).unwrap())
                .unwrap();
        let created = meta["created"].as_array().unwrap();
        assert!(created.iter().any(|entry| entry == "dir2/a.txt"));
        assert!(!created.iter().any(|entry| entry == "dir/a.txt"));
    }

    #[test]
    fn create_should_reject_non_utf8_names() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        let fs = LazyDvcFs::new(InodeTree::new(), overlay_dir, cache_dir, None);

        assert!(fs
            .create_impl(ROOT_INODE, OsStr::from_bytes(b"\xff"), 0o644)
            .is_err());
    }

    #[test]
    fn deleted_inodes_should_not_accumulate_unbounded() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        let fs = LazyDvcFs::new(InodeTree::new(), overlay_dir, cache_dir, None);

        for _ in 0..5 {
            let created = fs
                .create_impl(ROOT_INODE, OsStr::new("temp.txt"), 0o644)
                .unwrap();
            close_handle(&fs, created.fh);
            fs.unlink_impl(ROOT_INODE, OsStr::new("temp.txt")).unwrap();
        }

        assert!(
            fs.tree.write().unwrap().inode_count() <= 1,
            "repeated delete/recreate should not leak inode table entries"
        );
    }

    #[test]
    fn cache_entries_should_not_be_left_stale_after_rename() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, _inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });

        let old_cache = fs.cache_path("file.txt");
        let new_cache = fs.cache_path("renamed.txt");
        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("file.txt"),
            ROOT_INODE,
            OsStr::new("renamed.txt"),
        )
        .unwrap();

        assert!(
            !old_cache.exists(),
            "stale cache entry was left at {}",
            old_cache.display()
        );
        assert!(
            new_cache.exists(),
            "renamed cache entry was not recreated at {}",
            new_cache.display()
        );
    }

    #[test]
    fn rename_should_replace_existing_target_and_refresh_cache() {
        let entries = vec![
            FileEntry {
                relpath: "old.txt".to_string(),
                md5: "abcdef".to_string(),
                size: 5,
                isexec: false,
                islink: false,
                symlink_target: String::new(),
            },
            FileEntry {
                relpath: "new.txt".to_string(),
                md5: "123456".to_string(),
                size: 6,
                isexec: false,
                islink: false,
                symlink_target: String::new(),
            },
        ];
        let (fs, _state_dir, _inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/old.txt"), b"hello").unwrap();
            fs::write(cache.join("cache/new.txt"), b"target").unwrap();
        });

        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("old.txt"),
            ROOT_INODE,
            OsStr::new("new.txt"),
        )
        .unwrap();

        assert!(!fs.cache_path("old.txt").exists());
        assert_eq!(fs::read(fs.cache_path("new.txt")).unwrap(), b"hello");
        let tree = fs.tree.read().unwrap();
        assert!(tree.lookup_child(ROOT_INODE, "old.txt").is_none());
        let new_ino = tree.lookup_child(ROOT_INODE, "new.txt").unwrap();
        assert!(!tree.get(new_ino).unwrap().deleted);
    }

    #[test]
    fn rename_should_preserve_source_overlay_when_replacing_existing_target() {
        let entries = vec![
            FileEntry {
                relpath: "old.txt".to_string(),
                md5: "abcdef".to_string(),
                size: 5,
                isexec: false,
                islink: false,
                symlink_target: String::new(),
            },
            FileEntry {
                relpath: "new.txt".to_string(),
                md5: "123456".to_string(),
                size: 6,
                isexec: false,
                islink: false,
                symlink_target: String::new(),
            },
        ];
        let (fs, _state_dir, _inos) = build_fs(&entries, |overlay, _cache| {
            fs::write(overlay.join("old.txt"), b"source").unwrap();
            fs::write(overlay.join("new.txt"), b"target").unwrap();
        });

        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("old.txt"),
            ROOT_INODE,
            OsStr::new("new.txt"),
        )
        .unwrap();

        assert!(!fs.overlay_path("old.txt").exists());
        assert_eq!(fs::read(fs.overlay_path("new.txt")).unwrap(), b"source");
    }

    #[test]
    fn rename_should_reject_non_empty_directory_target() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(overlay_dir.join("src")).unwrap();
        fs::create_dir_all(overlay_dir.join("dst")).unwrap();
        fs::write(overlay_dir.join("dst/child.txt"), b"child").unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        let src_ino = tree.add_dir(ROOT_INODE, "src");
        let dst_ino = tree.add_dir(ROOT_INODE, "dst");
        let child_ino = tree.add_file(dst_ino, "child.txt", 0o644, false, "");
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        assert_eq!(
            fs.rename_impl(ROOT_INODE, OsStr::new("src"), ROOT_INODE, OsStr::new("dst")),
            Err(ENOTEMPTY)
        );

        assert!(overlay_dir.join("src").is_dir());
        assert_eq!(
            fs::read(overlay_dir.join("dst/child.txt")).unwrap(),
            b"child"
        );

        let tree = fs.tree.read().unwrap();
        assert_eq!(tree.lookup_child(ROOT_INODE, "src"), Some(src_ino));
        assert_eq!(tree.lookup_child(ROOT_INODE, "dst"), Some(dst_ino));
        assert_eq!(tree.lookup_child(dst_ino, "child.txt"), Some(child_ino));
        assert!(!tree.get(dst_ino).unwrap().deleted);
        assert!(!tree.get(child_ino).unwrap().deleted);
    }

    #[test]
    fn symlink_impl_should_replace_stale_overlay_entry() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(overlay_dir.join("link.txt")).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        let fs = LazyDvcFs::new(InodeTree::new(), overlay_dir.clone(), cache_dir, None);

        fs.symlink_impl(ROOT_INODE, OsStr::new("link.txt"), Path::new("target.txt"))
            .unwrap();

        let link_path = overlay_dir.join("link.txt");
        assert!(link_path
            .symlink_metadata()
            .unwrap()
            .file_type()
            .is_symlink());
        assert_eq!(fs::read_link(link_path).unwrap(), Path::new("target.txt"));
    }

    #[test]
    fn rename_manifest_symlink_should_preserve_symlink_type() {
        let entries = vec![FileEntry {
            relpath: "link.txt".to_string(),
            md5: String::new(),
            size: "target.txt".len() as u64,
            isexec: false,
            islink: true,
            symlink_target: "target.txt".to_string(),
        }];
        let (fs, _state_dir, _inos) = build_fs(&entries, |_overlay, _cache| {});

        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("link.txt"),
            ROOT_INODE,
            OsStr::new("renamed.txt"),
        )
        .unwrap();

        let renamed = fs.overlay_path("renamed.txt");
        assert!(renamed.symlink_metadata().unwrap().file_type().is_symlink());
        assert_eq!(fs::read_link(renamed).unwrap(), Path::new("target.txt"));
    }

    #[test]
    fn link_impl_should_reuse_inode_for_manifest_file() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });

        let attr = fs
            .link_impl(inos[0], ROOT_INODE, OsStr::new("copy.txt"))
            .unwrap();

        assert_eq!(attr.size, 5);
        assert!(fs.created.lock().unwrap().contains("copy.txt"));
        let copy_ino = lookup_path(&fs.tree.read().unwrap(), "copy.txt");
        assert_eq!(copy_ino, inos[0]);
        let info = fs.tree.read().unwrap().get(copy_ino).unwrap().clone();
        assert_eq!(info.nlink, 2);
        assert_eq!(info.backing_relpath, "file.txt");
        let file_meta = fs::symlink_metadata(fs.overlay_path("file.txt")).unwrap();
        let copy_meta = fs::symlink_metadata(fs.overlay_path("copy.txt")).unwrap();
        assert_eq!(file_meta.ino(), copy_meta.ino());
        assert!(file_meta.nlink() >= 2);
    }

    #[test]
    fn link_impl_should_reuse_inode_for_symlink_without_dereferencing() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        let ino = tree.add_file(ROOT_INODE, "link.txt", 0o777, true, "target.txt");
        if let Some(info) = tree.get_mut(ino) {
            info.size = "target.txt".len() as u64;
        }
        std::os::unix::fs::symlink("target.txt", overlay_dir.join("link.txt")).unwrap();
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        let attr = fs
            .link_impl(ino, ROOT_INODE, OsStr::new("copy.txt"))
            .unwrap();

        assert_eq!(attr.size, "target.txt".len() as u64);
        let copy_ino = lookup_path(&fs.tree.read().unwrap(), "copy.txt");
        assert_eq!(copy_ino, ino);
        let info = fs.tree.read().unwrap().get(copy_ino).unwrap().clone();
        assert!(info.is_symlink);
        assert_eq!(info.nlink, 2);
        assert_eq!(
            fs::read_link(overlay_dir.join("link.txt")).unwrap(),
            Path::new("target.txt")
        );
        let file_meta = fs::symlink_metadata(overlay_dir.join("link.txt")).unwrap();
        let copy_meta = fs::symlink_metadata(overlay_dir.join("copy.txt")).unwrap();
        assert_eq!(file_meta.ino(), copy_meta.ino());
        assert!(file_meta.nlink() >= 2);
    }

    #[test]
    fn link_impl_should_reuse_inode_for_dangling_symlink() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        let ino = tree.add_file(ROOT_INODE, "dangling.txt", 0o777, true, "../missing.txt");
        if let Some(info) = tree.get_mut(ino) {
            info.size = "../missing.txt".len() as u64;
        }
        std::os::unix::fs::symlink("../missing.txt", overlay_dir.join("dangling.txt")).unwrap();
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        fs.link_impl(ino, ROOT_INODE, OsStr::new("copy.txt"))
            .unwrap();

        let copy_ino = lookup_path(&fs.tree.read().unwrap(), "copy.txt");
        assert_eq!(copy_ino, ino);
        let info = fs.tree.read().unwrap().get(copy_ino).unwrap().clone();
        assert!(info.is_symlink);
        assert_eq!(info.nlink, 2);
        assert_eq!(
            fs::read_link(overlay_dir.join("dangling.txt")).unwrap(),
            Path::new("../missing.txt")
        );
        let file_meta = fs::symlink_metadata(overlay_dir.join("dangling.txt")).unwrap();
        let copy_meta = fs::symlink_metadata(overlay_dir.join("copy.txt")).unwrap();
        assert_eq!(file_meta.ino(), copy_meta.ino());
        assert!(file_meta.nlink() >= 2);
    }

    #[test]
    fn unlink_should_preserve_backing_file_until_last_hardlink_is_removed() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("file.txt"), b"hello").unwrap();

        let mut tree = InodeTree::new();
        let ino = tree.add_file(ROOT_INODE, "file.txt", 0o644, false, "");
        if let Some(info) = tree.get_mut(ino) {
            info.size = 5;
            info.overlay = true;
        }
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        fs.link_impl(ino, ROOT_INODE, OsStr::new("copy.txt"))
            .unwrap();
        fs.unlink_impl(ROOT_INODE, OsStr::new("copy.txt")).unwrap();

        assert!(overlay_dir.join("file.txt").exists());
        let info = fs.tree.read().unwrap().get(ino).unwrap().clone();
        assert_eq!(info.nlink, 1);
        assert_eq!(lookup_path(&fs.tree.read().unwrap(), "file.txt"), ino);
    }

    #[test]
    fn unlink_should_remove_new_file_from_created_tracking() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        let fs = LazyDvcFs::new(InodeTree::new(), overlay_dir, cache_dir, None);

        let created = fs
            .create_impl(ROOT_INODE, OsStr::new("new.txt"), 0o644)
            .unwrap();
        close_handle(&fs, created.fh);

        assert!(fs.created.lock().unwrap().contains("new.txt"));
        fs.unlink_impl(ROOT_INODE, OsStr::new("new.txt")).unwrap();

        assert!(!fs.created.lock().unwrap().contains("new.txt"));
        assert!(fs.deleted.lock().unwrap().contains("new.txt"));
    }

    #[test]
    fn rename_should_move_hardlink_namespace_without_moving_backing_file() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("file.txt"), b"hello").unwrap();

        let mut tree = InodeTree::new();
        let ino = tree.add_file(ROOT_INODE, "file.txt", 0o644, false, "");
        if let Some(info) = tree.get_mut(ino) {
            info.size = 5;
            info.overlay = true;
        }
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        fs.link_impl(ino, ROOT_INODE, OsStr::new("copy.txt"))
            .unwrap();
        fs.rename_impl(
            ROOT_INODE,
            OsStr::new("copy.txt"),
            ROOT_INODE,
            OsStr::new("moved.txt"),
        )
        .unwrap();

        let tree = fs.tree.read().unwrap();
        assert_eq!(lookup_path(&tree, "file.txt"), ino);
        assert_eq!(lookup_path(&tree, "moved.txt"), ino);
        let info = tree.get(ino).unwrap();
        assert_eq!(info.nlink, 2);
        assert_eq!(info.backing_relpath, "file.txt");
        assert!(overlay_dir.join("file.txt").exists());
        let file_meta = fs::symlink_metadata(overlay_dir.join("file.txt")).unwrap();
        let moved_meta = fs::symlink_metadata(overlay_dir.join("moved.txt")).unwrap();
        assert_eq!(file_meta.ino(), moved_meta.ino());
    }

    #[test]
    #[serial]
    fn mount_hardlink_should_share_inode_nlink_and_data() {
        if !fuse_available() {
            return;
        }
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("file.txt"), b"hello").unwrap();

        let mut tree = InodeTree::new();
        let ino = tree.add_file(ROOT_INODE, "file.txt", 0o644, false, "");
        if let Some(info) = tree.get_mut(ino) {
            info.size = 5;
            info.overlay = true;
        }
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);
        let mounted = MountedFs::mount(fs, state_dir);
        mounted.wait_for("file.txt");

        let file_path = mounted.path().join("file.txt");
        let copy_path = mounted.path().join("copy.txt");

        std::fs::hard_link(&file_path, &copy_path).unwrap();

        let file_meta = std::fs::metadata(&file_path).unwrap();
        let copy_meta = std::fs::metadata(&copy_path).unwrap();
        assert_eq!(file_meta.ino(), copy_meta.ino());
        assert!(file_meta.nlink() >= 2);

        std::fs::write(&copy_path, b"updated").unwrap();
        assert_eq!(std::fs::read(&file_path).unwrap(), b"updated");

        std::fs::remove_file(&copy_path).unwrap();
        assert_eq!(std::fs::read(&file_path).unwrap(), b"updated");
    }

    #[test]
    #[serial]
    fn mount_cat_should_reach_eof_for_unknown_size_manifest_file() {
        if !fuse_available() {
            return;
        }
        let entries = vec![FileEntry {
            relpath: "unknown.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 0,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, state_dir, _inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/unknown.txt"), b"hello world").unwrap();
        });
        let mounted = MountedFs::mount(fs, state_dir);
        mounted.wait_for("unknown.txt");

        let output = Command::new("sh")
            .arg("-lc")
            .arg(format!(
                "timeout 5 cat {}",
                mounted.path().join("unknown.txt").display()
            ))
            .output()
            .unwrap();

        assert!(
            output.status.success(),
            "cat did not terminate cleanly: status={:?} stdout={} stderr={}",
            output.status.code(),
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );
        assert_eq!(output.stdout, b"hello world");
    }

    #[test]
    #[serial]
    fn mount_readdir_should_include_dot_entries_at_root() {
        if !fuse_available() {
            return;
        }
        let entries = vec![FileEntry {
            relpath: "child.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, state_dir, _inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/child.txt"), b"hello").unwrap();
        });
        let mounted = MountedFs::mount(fs, state_dir);
        mounted.wait_for("child.txt");

        let output = Command::new("sh")
            .arg("-lc")
            .arg(format!("cd {} && ls -a", mounted.path().display()))
            .output()
            .unwrap();

        assert!(
            output.status.success(),
            "ls -a failed: status={:?} stdout={} stderr={}",
            output.status.code(),
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );

        let entries = String::from_utf8_lossy(&output.stdout);
        assert!(entries.lines().any(|line| line == "."));
        assert!(entries.lines().any(|line| line == ".."));
        assert!(entries.lines().any(|line| line == "child.txt"));
    }

    #[test]
    #[serial]
    fn mount_readdir_should_include_dot_entries_in_nested_directory() {
        if !fuse_available() {
            return;
        }
        let entries = vec![FileEntry {
            relpath: "dir/child.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, state_dir, _inos) = build_fs(&entries, |_overlay, cache| {
            fs::create_dir_all(cache.join("cache/dir")).unwrap();
            fs::write(cache.join("cache/dir/child.txt"), b"hello").unwrap();
        });
        let mounted = MountedFs::mount(fs, state_dir);
        mounted.wait_for("dir");

        let output = Command::new("sh")
            .arg("-lc")
            .arg(format!("cd {} && ls -a dir", mounted.path().display()))
            .output()
            .unwrap();

        assert!(
            output.status.success(),
            "ls -a dir failed: status={:?} stdout={} stderr={}",
            output.status.code(),
            String::from_utf8_lossy(&output.stdout),
            String::from_utf8_lossy(&output.stderr)
        );

        let entries = String::from_utf8_lossy(&output.stdout);
        assert!(entries.lines().any(|line| line == "."));
        assert!(entries.lines().any(|line| line == ".."));
        assert!(entries.lines().any(|line| line == "child.txt"));
    }

    #[test]
    fn read_impl_should_slice_data_and_return_eof_past_end() {
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });
        let ino = inos[0];

        assert_eq!(fs.read_impl(ino, 0, 1, 3).unwrap(), b"ell");
        assert_eq!(fs.read_impl(ino, 0, 4, 10).unwrap(), b"o");
        assert!(fs.read_impl(ino, 0, 5, 10).unwrap().is_empty());
        assert!(fs.read_impl(ino, 0, 99, 10).unwrap().is_empty());
    }

    #[test]
    fn read_impl_should_hydrate_unknown_size_after_first_fetch() {
        let entries = vec![FileEntry {
            relpath: "unknown.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 0,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, _state_dir, inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/unknown.txt"), b"hello world").unwrap();
        });
        let ino = inos[0];

        assert_eq!(fs.read_impl(ino, 0, 0, 5).unwrap(), b"hello");
        assert_eq!(fs.tree.read().unwrap().get(ino).unwrap().size, 11);
    }

    #[test]
    fn mkdir_should_validate_parent_type() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        let file_ino = tree.add_file(ROOT_INODE, "file.txt", 0o644, false, "");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert_eq!(
            fs.mkdir_impl(file_ino, OsStr::new("child"), 0o755, 0)
                .map(|_| ()),
            Err(ENOTDIR)
        );
    }

    #[test]
    fn mkdir_should_reject_existing_names() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let mut tree = InodeTree::new();
        tree.add_dir(ROOT_INODE, "dir");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);

        assert_eq!(
            fs.mkdir_impl(ROOT_INODE, OsStr::new("dir"), 0o755, 0)
                .map(|_| ()),
            Err(EEXIST)
        );
    }

    #[test]
    fn mkdir_should_honor_requested_directory_mode() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let fs = LazyDvcFs::new(InodeTree::new(), overlay_dir.clone(), cache_dir, None);
        let attr = fs
            .mkdir_impl(ROOT_INODE, OsStr::new("secret"), 0o700, 0)
            .unwrap();

        assert_eq!(attr.perm, 0o700);
        let secret_ino = lookup_path(&fs.tree.read().unwrap(), "secret");
        assert_eq!(fs.tree.read().unwrap().get(secret_ino).unwrap().mode, 0o700);
        assert_eq!(
            fs::metadata(overlay_dir.join("secret"))
                .unwrap()
                .permissions()
                .mode()
                & 0o777,
            0o700
        );
    }

    #[test]
    fn setattr_should_update_directory_mode() {
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(overlay_dir.join("secret")).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::set_permissions(
            overlay_dir.join("secret"),
            fs::Permissions::from_mode(0o700),
        )
        .unwrap();

        let mut tree = InodeTree::new();
        let secret_ino = tree.add_dir_with_mode(ROOT_INODE, "secret", 0o700);
        let fs = LazyDvcFs::new(tree, overlay_dir.clone(), cache_dir, None);

        let attr = fs.setattr_impl(secret_ino, Some(0o750), None).unwrap();

        assert_eq!(attr.perm, 0o750);
        assert_eq!(fs.tree.read().unwrap().get(secret_ino).unwrap().mode, 0o750);
        assert_eq!(
            fs::metadata(overlay_dir.join("secret"))
                .unwrap()
                .permissions()
                .mode()
                & 0o777,
            0o750
        );
    }

    #[test]
    fn rename_should_reject_directory_move_into_descendant() {
        let mut tree = InodeTree::new();
        let a_ino = tree.add_dir(ROOT_INODE, "a");
        let b_ino = tree.add_dir(a_ino, "b");
        assert_eq!(tree.rename(a_ino, b_ino, "newa"), Err(libc::EINVAL));
        assert_eq!(tree.get(a_ino).unwrap().parent, ROOT_INODE);
    }

    #[test]
    #[serial]
    fn mount_create_should_fail_when_overlay_path_is_invalid() {
        if !fuse_available() {
            return;
        }
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();
        fs::write(overlay_dir.join("blocked"), b"not a directory").unwrap();

        let mut tree = InodeTree::new();
        tree.add_dir(ROOT_INODE, "blocked");
        let fs = LazyDvcFs::new(tree, overlay_dir, cache_dir, None);
        let mounted = MountedFs::mount(fs, state_dir);
        mounted.wait_for("blocked");

        assert!(File::create(mounted.path().join("blocked/new.txt")).is_err());
    }

    #[test]
    #[serial]
    fn mount_directory_modes_should_match_requested_permissions() {
        if !fuse_available() {
            return;
        }
        let state_dir = TempDir::new().unwrap();
        let overlay_dir = state_dir.path().join("overlay");
        let cache_dir = state_dir.path().join("cache-root");
        fs::create_dir_all(&overlay_dir).unwrap();
        fs::create_dir_all(cache_dir.join("cache")).unwrap();

        let fs = LazyDvcFs::new(InodeTree::new(), overlay_dir, cache_dir, None);
        let mounted = MountedFs::mount(fs, state_dir);

        let pgdata = mounted.path().join(".runtime/postgres/data");
        std::fs::create_dir_all(pgdata.parent().unwrap()).unwrap();
        std::fs::create_dir(&pgdata).unwrap();
        std::fs::set_permissions(&pgdata, std::fs::Permissions::from_mode(0o700)).unwrap();
        assert_eq!(
            std::fs::metadata(&pgdata).unwrap().permissions().mode() & 0o777,
            0o700
        );

        std::fs::set_permissions(&pgdata, std::fs::Permissions::from_mode(0o750)).unwrap();
        assert_eq!(
            std::fs::metadata(&pgdata).unwrap().permissions().mode() & 0o777,
            0o750
        );
    }

    #[test]
    #[serial]
    fn mount_open_handle_should_survive_rename() {
        if !fuse_available() {
            return;
        }
        let entries = vec![FileEntry {
            relpath: "file.txt".to_string(),
            md5: "abcdef".to_string(),
            size: 5,
            isexec: false,
            islink: false,
            symlink_target: String::new(),
        }];
        let (fs, state_dir, _inos) = build_fs(&entries, |_overlay, cache| {
            fs::write(cache.join("cache/file.txt"), b"hello").unwrap();
        });
        let mounted = MountedFs::mount(fs, state_dir);
        mounted.wait_for("file.txt");

        let mut file = File::open(mounted.path().join("file.txt")).unwrap();
        let mut buf = String::new();
        file.read_to_string(&mut buf).unwrap();
        assert_eq!(buf, "hello");

        std::fs::rename(
            mounted.path().join("file.txt"),
            mounted.path().join("renamed.txt"),
        )
        .unwrap();

        file.seek(SeekFrom::Start(0)).unwrap();
        buf.clear();
        file.read_to_string(&mut buf).unwrap();
        assert_eq!(buf, "hello");
    }
}
