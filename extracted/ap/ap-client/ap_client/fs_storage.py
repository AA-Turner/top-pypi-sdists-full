"""Directory operations using the SDK's scoped OSS authorization and routing."""

from __future__ import annotations

from .fs_transfer import UserDataTransfer, _scope_denied


class UserDataFiles(UserDataTransfer):
    def list(self, uid: str, path: str = "", *, recursive: bool = False):
        from instance_repo._routing import _OperationIntent

        root = self.repo._user_data_prefix(uid)
        prefix = root if path in ("", ".", "/") else self._key(uid, path) + "/"

        def listing(bucket):
            entries = {}
            found = False
            marker = ""
            while True:
                page = bucket.list_objects(
                    prefix=prefix, delimiter="" if recursive else "/", marker=marker, max_keys=1000
                )
                found = found or bool(page.object_list or page.prefix_list)
                for obj in page.object_list:
                    if obj.key == prefix:
                        continue
                    kind = "directory" if obj.key.endswith("/") else "file"
                    entries[obj.key] = dict(
                        path=obj.key[len(root) :],
                        name=obj.key[len(prefix) :],
                        key=obj.key,
                        type=kind,
                        size=obj.size,
                        modified=obj.last_modified,
                    )
                    if recursive:
                        # OSS may have no marker object for a directory. Rebuild
                        # its ancestors so -R --dirs-only includes these too.
                        parts = obj.key[len(prefix) :].split("/")
                        for depth in range(1, len(parts)):
                            name = "/".join(parts[:depth]) + "/"
                            key = prefix + name
                            entries.setdefault(
                                key,
                                dict(
                                    path=key[len(root) :],
                                    name=name,
                                    key=key,
                                    type="directory",
                                    size=None,
                                    modified=None,
                                ),
                            )
                for common in page.prefix_list:
                    entries[common] = dict(
                        path=common[len(root) :],
                        name=common[len(prefix) :],
                        key=common,
                        type="directory",
                        size=None,
                        modified=None,
                    )
                if not page.is_truncated:
                    break
                if not page.next_marker or page.next_marker == marker:
                    raise ValueError("OSS listing did not advance its pagination marker")
                marker = page.next_marker
            return list(entries.values()), found

        try:
            rows, found = self.content._execute_oss(
                _OperationIntent.NON_DOWNLOAD, prefix, None, listing
            )
        except Exception as exc:
            if prefix == root or not _scope_denied(exc):
                raise
            # A file-only grant need not permit listing the same-name directory.
            rows, found = [], False
        if found or prefix == root:
            return rows
        key = prefix.rstrip("/")

        def file_entry(bucket):
            if not bucket.object_exists(key):
                raise FileNotFoundError(f"No such file or directory: {path}")
            meta = bucket.head_object(key)
            return [
                dict(
                    path=key[len(root) :],
                    name=key.rsplit("/", 1)[-1],
                    key=key,
                    type="file",
                    size=meta.content_length,
                    modified=meta.last_modified,
                    explicit=True,
                )
            ]

        if path.endswith("/"):
            raise FileNotFoundError(f"No such directory: {path}")
        return self.content._execute_oss(_OperationIntent.NON_DOWNLOAD, key, None, file_entry)

    def mkdir(self, uid: str, path: str, *, parents: bool = False):
        from instance_repo._routing import _OperationIntent

        clean = self.repo._clean_user_data_subpath(path)
        segments = clean.split("/")
        paths = ["/".join(segments[:i]) for i in range(1, len(segments) + 1)]

        def exists(key):
            return self.content._execute_oss(
                _OperationIntent.NON_DOWNLOAD, key, None, lambda bucket: bucket.object_exists(key)
            )

        def directory_exists(key):
            return self.content._execute_oss(
                _OperationIntent.NON_DOWNLOAD,
                key,
                None,
                lambda bucket: bool(bucket.list_objects(prefix=key, max_keys=1).object_list),
            )

        # Check all ancestors before creating any marker.
        present = []
        for part in paths:
            key = self._key(uid, part)
            if exists(key):
                raise FileExistsError(f"A file already exists at {part}")
            present.append(directory_exists(key + "/"))
        if present[-1] and not parents:
            raise FileExistsError(f"Directory already exists: {clean}; use --parents to keep it")
        if not parents and not all(present[:-1]):
            raise FileNotFoundError("Parent directory does not exist; use --parents/-p")
        created = []
        for part, found in zip(paths, present):
            if found:
                continue
            key = self._key(uid, part) + "/"

            def create(bucket, key=key):
                if not bucket.object_exists(key):
                    bucket.put_object(key, b"", headers={"x-oss-forbid-overwrite": "true"})

            self.content._execute_oss(_OperationIntent.NON_DOWNLOAD, key, None, create)
            created.append(part)
        return {"path": clean, "created": created}
