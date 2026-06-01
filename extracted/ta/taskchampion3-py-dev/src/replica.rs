use crate::task::TaskData;
use crate::util::{into_runtime_error, uuid2tc};
use crate::{AccessMode, DependencyMap, Operations, Task, WorkingSet};
use pyo3::prelude::*;
use std::collections::HashMap;
use taskchampion::storage::AccessMode as TCAccessMode;
use taskchampion::{Replica as TCReplica, ServerConfig, SqliteStorage};

type TCReplicaSqlite = TCReplica<SqliteStorage>;

#[pyclass(unsendable)]
/// A replica represents an instance of a user's task data, providing an easy interface
/// for querying and modifying that data.
///
/// A replica can only be used in the thread in which it was created. Use from any other
/// thread will panic.
///
/// All Rust `Replica` methods are async; this binding bridges them synchronously using a
/// dedicated single-threaded Tokio runtime (`block_on`). This keeps the Python API simple
/// and avoids requiring `asyncio` on the caller side.
///
/// `Task` and `TaskData` objects returned by the replica are independent snapshots: a
/// mutation made via one handle (e.g. `task.set_status(...)` followed by
/// `replica.commit_operations(...)`) is not reflected in other handles to the same UUID
/// until they are re-fetched (e.g. with `replica.get_task(uuid)`).
pub struct Replica {
    inner: TCReplicaSqlite,
    rt: tokio::runtime::Runtime,
    _temp_dir: Option<tempfile::TempDir>,
}

fn build_runtime() -> PyResult<tokio::runtime::Runtime> {
    tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))
}

#[pymethods]
impl Replica {
    #[staticmethod]
    /// Create a Replica with on-disk storage.
    ///
    /// Raises `RuntimeError` if the database does not exist and `create_if_missing` is false.
    #[pyo3(signature=(path, create_if_missing, access_mode=AccessMode::ReadWrite))]
    pub fn new_on_disk(
        path: String,
        create_if_missing: bool,
        access_mode: AccessMode,
    ) -> PyResult<Replica> {
        let rt = build_runtime()?;
        let storage = rt
            .block_on(SqliteStorage::new(
                path,
                access_mode.into(),
                create_if_missing,
            ))
            .map_err(into_runtime_error)?;
        Ok(Replica {
            inner: TCReplica::new(storage),
            rt,
            _temp_dir: None,
        })
    }

    #[staticmethod]
    /// Create a Replica with isolated in-memory storage (backed by a temporary SQLite file).
    ///
    /// The temporary directory is removed when the Replica is dropped.
    pub fn new_in_memory() -> PyResult<Self> {
        let rt = build_runtime()?;
        let temp_dir = tempfile::tempdir()
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?;
        let storage = rt
            .block_on(SqliteStorage::new(
                temp_dir.path(),
                TCAccessMode::ReadWrite,
                true,
            ))
            .map_err(into_runtime_error)?;
        Ok(Replica {
            inner: TCReplica::new(storage),
            rt,
            _temp_dir: Some(temp_dir),
        })
    }

    /// Create a new task with the given UUID, appending a `Create` operation to `ops`.
    pub fn create_task(&mut self, uuid: String, ops: &mut Operations) -> PyResult<Task> {
        let rt = &self.rt;
        let task = rt
            .block_on(self.inner.create_task(uuid2tc(uuid)?, ops.as_mut()))
            .map_err(into_runtime_error)?
            .into();
        Ok(task)
    }

    /// Get all tasks as a UUID-keyed map.
    pub fn all_tasks(&mut self) -> PyResult<HashMap<String, Task>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.all_tasks())
            .map_err(into_runtime_error)?
            .into_iter()
            .map(|(key, value)| (key.to_string(), value.into()))
            .collect())
    }

    /// Get all tasks as a UUID-keyed map of `TaskData`.
    pub fn all_task_data(&mut self) -> PyResult<HashMap<String, TaskData>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.all_task_data())
            .map_err(into_runtime_error)?
            .into_iter()
            .map(|(key, value)| (key.to_string(), TaskData::from(value)))
            .collect())
    }

    /// Get the UUIDs of all tasks.
    pub fn all_task_uuids(&mut self) -> PyResult<Vec<String>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.all_task_uuids())
            .map_err(into_runtime_error)?
            .iter()
            .map(|item| item.to_string())
            .collect())
    }

    /// Get all pending tasks.
    pub fn pending_tasks(&mut self) -> PyResult<Vec<Task>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.pending_tasks())
            .map_err(into_runtime_error)?
            .into_iter()
            .map(|t| t.into())
            .collect())
    }

    /// Get all pending tasks as `TaskData`.
    pub fn pending_task_data(&mut self) -> PyResult<Vec<TaskData>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.pending_task_data())
            .map_err(into_runtime_error)?
            .into_iter()
            .map(TaskData::from)
            .collect())
    }

    /// Get the current working set.
    pub fn working_set(&mut self) -> PyResult<WorkingSet> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.working_set())
            .map_err(into_runtime_error)?
            .into())
    }

    /// Get the dependency map for all pending tasks.
    ///
    /// If `force` is true the map is re-calculated from scratch; otherwise a cached copy
    /// may be returned.
    pub fn dependency_map(&mut self, force: bool) -> PyResult<DependencyMap> {
        let rt = &self.rt;
        let dm = rt
            .block_on(self.inner.dependency_map(force))
            .map_err(into_runtime_error)?;
        Ok(dm.into())
    }

    /// Get an existing task by UUID, returning `None` if it does not exist.
    pub fn get_task(&mut self, uuid: String) -> PyResult<Option<Task>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.get_task(uuid2tc(uuid)?))
            .map_err(into_runtime_error)?
            .map(|t| t.into()))
    }

    /// Get an existing task as `TaskData` by UUID, returning `None` if it does not exist.
    pub fn get_task_data(&mut self, uuid: String) -> PyResult<Option<TaskData>> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.get_task_data(uuid2tc(uuid)?))
            .map_err(into_runtime_error)?
            .map(TaskData::from))
    }

    /// Get the operations that led to the given task.
    pub fn get_task_operations(&mut self, uuid: String) -> PyResult<Operations> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.get_task_operations(uuid2tc(uuid)?))
            .map_err(into_runtime_error)?
            .into())
    }

    /// Commit a set of operations to the replica.
    pub fn commit_operations(&mut self, ops: Operations) -> PyResult<()> {
        let rt = &self.rt;
        rt.block_on(self.inner.commit_operations(ops.into()))
            .map_err(into_runtime_error)
    }

    /// Sync with a server created from `ServerConfig::Local`.
    #[cfg(feature = "server-local")]
    pub fn sync_to_local(&mut self, server_dir: String, avoid_snapshots: bool) -> PyResult<()> {
        let rt = &self.rt;
        let mut server = rt
            .block_on(
                ServerConfig::Local {
                    server_dir: server_dir.into(),
                }
                .into_server(),
            )
            .map_err(into_runtime_error)?;
        rt.block_on(self.inner.sync(&mut server, avoid_snapshots))
            .map_err(into_runtime_error)
    }

    /// Sync with a server created from `ServerConfig::Remote`.
    #[cfg(feature = "server-sync")]
    pub fn sync_to_remote(
        &mut self,
        url: String,
        client_id: String,
        encryption_secret: String,
        avoid_snapshots: bool,
    ) -> PyResult<()> {
        let rt = &self.rt;
        let mut server = rt
            .block_on(
                ServerConfig::Remote {
                    url,
                    client_id: uuid2tc(client_id)?,
                    encryption_secret: encryption_secret.into(),
                }
                .into_server(),
            )
            .map_err(into_runtime_error)?;
        rt.block_on(self.inner.sync(&mut server, avoid_snapshots))
            .map_err(into_runtime_error)
    }

    /// Sync with a server created from `ServerConfig::Gcp`.
    #[cfg(feature = "server-gcp")]
    #[pyo3(signature=(bucket, credential_path, encryption_secret, avoid_snapshots))]
    pub fn sync_to_gcp(
        &mut self,
        bucket: String,
        credential_path: Option<String>,
        encryption_secret: String,
        avoid_snapshots: bool,
    ) -> PyResult<()> {
        let rt = &self.rt;
        let mut server = rt
            .block_on(
                ServerConfig::Gcp {
                    bucket,
                    credential_path,
                    encryption_secret: encryption_secret.into(),
                }
                .into_server(),
            )
            .map_err(into_runtime_error)?;
        rt.block_on(self.inner.sync(&mut server, avoid_snapshots))
            .map_err(into_runtime_error)
    }

    /// Rebuild the working set. If `renumber` is true, tasks may be assigned new indices.
    pub fn rebuild_working_set(&mut self, renumber: bool) -> PyResult<()> {
        let rt = &self.rt;
        rt.block_on(self.inner.rebuild_working_set(renumber))
            .map_err(into_runtime_error)
    }

    /// Get the number of operations local to this replica and not yet synced to the server.
    pub fn num_local_operations(&mut self) -> PyResult<usize> {
        let rt = &self.rt;
        rt.block_on(self.inner.num_local_operations())
            .map_err(into_runtime_error)
    }

    /// Get the number of available undo points.
    pub fn num_undo_points(&mut self) -> PyResult<usize> {
        let rt = &self.rt;
        rt.block_on(self.inner.num_undo_points())
            .map_err(into_runtime_error)
    }

    /// Return the operations back to and including the last undo point.
    pub fn get_undo_operations(&mut self) -> PyResult<Operations> {
        let rt = &self.rt;
        Ok(rt
            .block_on(self.inner.get_undo_operations())
            .map_err(into_runtime_error)?
            .into())
    }

    /// Commit the reverse of the given operations. Returns `true` on success.
    pub fn commit_reversed_operations(&mut self, operations: Operations) -> PyResult<bool> {
        let rt = &self.rt;
        rt.block_on(self.inner.commit_reversed_operations(operations.into()))
            .map_err(into_runtime_error)
    }

    /// Expire old deleted tasks (deleted for more than 180 days).
    pub fn expire_tasks(&mut self) -> PyResult<()> {
        let rt = &self.rt;
        rt.block_on(self.inner.expire_tasks())
            .map_err(into_runtime_error)
    }
}
