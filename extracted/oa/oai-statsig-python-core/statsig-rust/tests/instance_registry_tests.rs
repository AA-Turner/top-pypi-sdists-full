use std::sync::mpsc::{self, Receiver, Sender};
use std::sync::{Arc, Mutex, MutexGuard};
use std::thread;
use std::time::Duration;

use lazy_static::lazy_static;
use more_asserts::assert_gt;
use statsig_rust::instance_registry::InstanceRegistry;

lazy_static! {
    static ref TEST_MUTEX: Mutex<()> = Mutex::new(());
}

fn get_test_lock() -> MutexGuard<'static, ()> {
    let guard = TEST_MUTEX.lock().unwrap();

    InstanceRegistry::remove_all();

    guard
}

#[derive(Debug)]
pub struct MyBar {
    pub is_active: bool,
    pub data: String,
}

#[derive(Debug)]
pub struct MyFoo {
    pub name: String,
    pub bar: Arc<MyBar>,
}

struct BlockingDrop {
    started: Sender<()>,
    release: Mutex<Receiver<()>>,
}

impl Drop for BlockingDrop {
    fn drop(&mut self) {
        self.started.send(()).unwrap();
        self.release.lock().unwrap().recv().unwrap();
    }
}

struct WriteRegistryOnDrop {
    registered_id: Arc<Mutex<Option<u64>>>,
}

impl Drop for WriteRegistryOnDrop {
    fn drop(&mut self) {
        let registered_id = InstanceRegistry::register(MyBar {
            is_active: true,
            data: "registered during drop".to_string(),
        });
        *self.registered_id.lock().unwrap() = registered_id;
    }
}

#[test]
fn test_register_and_get() {
    let _lock = get_test_lock();

    let my_bar = MyBar {
        is_active: true,
        data: "bar".to_string(),
    };
    let id = InstanceRegistry::register(my_bar).unwrap();

    let retrieved = InstanceRegistry::get::<MyBar>(&id);
    assert!(retrieved.is_some());
    assert!(retrieved.unwrap().is_active);
}

#[test]
fn test_remove() {
    let _lock = get_test_lock();

    let my_bar = MyBar {
        is_active: true,
        data: "bar".to_string(),
    };
    let id = InstanceRegistry::register(my_bar).unwrap();

    InstanceRegistry::remove(&id);
    let retrieved = InstanceRegistry::get::<MyBar>(&id);
    assert!(retrieved.is_none());
}

#[test]
fn test_remove_drops_instance_after_releasing_registry_lock() {
    let _lock = get_test_lock();

    let target_id = InstanceRegistry::register(MyBar {
        is_active: true,
        data: "target".to_string(),
    })
    .unwrap();
    let (drop_started_tx, drop_started_rx) = mpsc::channel();
    let (release_drop_tx, release_drop_rx) = mpsc::channel();
    let drop_id = InstanceRegistry::register(BlockingDrop {
        started: drop_started_tx,
        release: Mutex::new(release_drop_rx),
    })
    .unwrap();

    let remove_thread = thread::spawn(move || InstanceRegistry::remove(&drop_id));
    drop_started_rx
        .recv_timeout(Duration::from_secs(1))
        .expect("removed instance did not start dropping");

    let (read_result_tx, read_result_rx) = mpsc::channel();
    let read_thread = thread::spawn(move || {
        read_result_tx
            .send(InstanceRegistry::get::<MyBar>(&target_id).is_some())
            .unwrap();
    });
    let read_result = read_result_rx.recv_timeout(Duration::from_secs(1));

    release_drop_tx.send(()).unwrap();
    remove_thread.join().unwrap();
    read_thread.join().unwrap();

    assert!(
        matches!(read_result, Ok(true)),
        "registry read did not complete while removed instance was dropping"
    );
    InstanceRegistry::remove(&target_id);
}

#[test]
fn test_remove_all() {
    let _lock = get_test_lock();

    let my_bar = MyBar {
        is_active: true,
        data: "bar".to_string(),
    };
    let id = InstanceRegistry::register(my_bar).unwrap();

    InstanceRegistry::remove_all();
    let retrieved = InstanceRegistry::get::<MyBar>(&id);
    assert!(retrieved.is_none());
}

#[test]
fn test_remove_all_drops_instances_after_releasing_registry_lock() {
    let _lock = get_test_lock();

    let registered_id = Arc::new(Mutex::new(None));
    InstanceRegistry::register(WriteRegistryOnDrop {
        registered_id: registered_id.clone(),
    })
    .unwrap();

    InstanceRegistry::remove_all();

    let registered_id = registered_id
        .lock()
        .unwrap()
        .take()
        .expect("instance drop could not reenter the registry");
    assert!(InstanceRegistry::get::<MyBar>(&registered_id).is_some());
    InstanceRegistry::remove(&registered_id);
}

#[test]
fn test_register_and_get_nested() {
    let _lock = get_test_lock();

    let my_bar = MyBar {
        is_active: true,
        data: "bar".to_string(),
    };
    let my_foo = MyFoo {
        name: "foo".to_string(),
        bar: Arc::new(my_bar),
    };
    let id = InstanceRegistry::register(my_foo).unwrap();

    let retrieved = InstanceRegistry::get::<MyFoo>(&id).unwrap();
    assert!(retrieved.bar.is_active);
    assert_eq!(retrieved.bar.data, "bar");
    assert_eq!(retrieved.name, "foo");
}

#[test]
fn test_getting_wrong_type() {
    let _lock = get_test_lock();

    let my_bar = MyBar {
        is_active: true,
        data: "bar".to_string(),
    };
    let id = InstanceRegistry::register(my_bar).unwrap();

    let retrieved = InstanceRegistry::get::<MyFoo>(&id);
    assert!(retrieved.is_none());
}

#[test]
fn test_returns_valid_ids() {
    let _lock = get_test_lock();

    let my_bar = Arc::new(MyBar {
        is_active: true,
        data: "bar".to_string(),
    });
    let id = InstanceRegistry::register_arc(my_bar.clone()).unwrap();
    assert_gt!(id, 0);

    let my_foo = MyFoo {
        name: "foo".to_string(),
        bar: my_bar.clone(),
    };
    let id = InstanceRegistry::register(my_foo).unwrap();
    assert_gt!(id, 0);
}
