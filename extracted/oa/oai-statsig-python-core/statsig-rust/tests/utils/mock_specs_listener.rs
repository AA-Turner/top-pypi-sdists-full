use statsig_rust::{SpecsInfo, SpecsUpdate, SpecsUpdateListener, StatsigErr};
use std::sync::Mutex;
use std::time::Duration;
use tokio::sync::Notify;
use tokio::time::error::Elapsed;
use tokio::time::timeout;

#[derive(Default)]
pub struct MockSpecsListener {
    pub received_update: Mutex<Option<SpecsUpdate>>,
    next_update_notify: Notify,
}

impl MockSpecsListener {
    pub async fn wait_for_next_update(&self) -> Result<SpecsUpdate, Elapsed> {
        timeout(Duration::from_secs(10), async {
            loop {
                if let Some(update) = self.nullable_get_most_recent_update() {
                    return update;
                }
                // A stored permit covers updates arriving between the check and wait.
                // Recheck the state after waking because a prior read may leave a permit.
                self.next_update_notify.notified().await;
            }
        })
        .await
    }

    pub fn force_get_most_recent_update(&self) -> SpecsUpdate {
        self.nullable_get_most_recent_update().unwrap()
    }

    pub fn nullable_get_most_recent_update(&self) -> Option<SpecsUpdate> {
        self.received_update.lock().unwrap().take()
    }
}
impl SpecsUpdateListener for MockSpecsListener {
    fn did_receive_specs_update(&self, update: SpecsUpdate) -> Result<(), StatsigErr> {
        *self.received_update.lock().unwrap() = Some(update);

        self.next_update_notify.notify_one();
        Ok(())
    }

    fn get_current_specs_info(&self) -> SpecsInfo {
        SpecsInfo::empty()
    }
}
