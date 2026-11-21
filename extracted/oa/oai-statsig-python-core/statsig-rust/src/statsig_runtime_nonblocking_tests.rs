use super::StatsigRuntime;
use std::future::{pending, ready};
use std::time::Duration;
use tokio::sync::oneshot;

#[tokio::test]
async fn nonblocking_spawn_drops_work_when_the_task_registry_is_busy() {
    let runtime = StatsigRuntime::get_runtime();
    let handle = tokio::runtime::Handle::current();
    let (sent, received) = oneshot::channel();
    {
        let _tasks = runtime.spawned_tasks.lock();
        assert!(!runtime.try_spawn_on(&handle, "test", async move {
            sent.send(()).unwrap();
        }));
    }
    assert!(received.await.is_err());
    assert_eq!(runtime.get_num_active_tasks(), 0);
}

#[tokio::test]
async fn shutdown_cancels_nonblocking_work_and_rejects_new_tasks() {
    let runtime = StatsigRuntime::get_runtime();
    let handle = tokio::runtime::Handle::current();
    let (started, start) = oneshot::channel();
    let (cancelled, cancel) = oneshot::channel();
    assert!(runtime.try_spawn_on(&handle, "test", async move {
        let _cancel = scopeguard::guard(cancelled, |signal| {
            let _ = signal.send(());
        });
        started.send(()).unwrap();
        pending::<()>().await;
    }));

    let timeout = Duration::from_secs(5);
    tokio::time::timeout(timeout, start).await.unwrap().unwrap();
    runtime.shutdown();
    tokio::time::timeout(timeout, cancel)
        .await
        .unwrap()
        .unwrap();

    assert!(!runtime.try_spawn_on(&handle, "test", ready(())));
    assert_eq!(runtime.get_num_active_tasks(), 0);
}
