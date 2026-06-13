use crate::{
    log_e,
    sdk_event_emitter::{SdkEvent, SdkEventCode},
    statsig_types::{DynamicConfig, Experiment, Layer},
    Statsig,
};
use dashmap::DashMap;
use std::{ops::Deref, sync::Arc};

const TAG: &str = "SdkEventEmitter";

#[derive(Clone)]
struct Listener {
    sub_id_value: String,
    callback: Arc<dyn Fn(SdkEvent) + Send + Sync>,
}

#[derive(Clone)]
struct InternalListener {
    id: String,
    callback: Arc<dyn Fn(SdkEvent) -> bool + Send + Sync>,
}

#[derive(Clone)]
pub struct SubscriptionID {
    value: String,
    event: String,
}

impl SubscriptionID {
    pub fn new(event: &str) -> Self {
        Self {
            value: uuid::Uuid::new_v4().to_string(),
            event: event.to_string(),
        }
    }

    pub fn error() -> Self {
        Self {
            value: "ERROR".to_string(),
            event: "ERROR".to_string(),
        }
    }

    pub fn decode(s: &str) -> Option<Self> {
        let parts: Vec<&str> = s.split('@').collect();
        if parts.len() != 2 {
            return None;
        }

        Some(Self {
            value: parts[0].to_string(),
            event: parts[1].to_string(),
        })
    }

    pub fn encode(self) -> String {
        let mut encoded = self.value;
        encoded.push('@');
        encoded.push_str(&self.event);
        encoded
    }
}

#[derive(Default)]
pub struct SdkEventEmitter {
    listeners: DashMap<u8, Vec<Listener>>,
    internal_listeners: DashMap<u8, Vec<InternalListener>>,
}

impl SdkEventEmitter {
    pub fn subscribe<F>(&self, event: &str, callback: F) -> SubscriptionID
    where
        F: Fn(SdkEvent) + Send + Sync + 'static,
    {
        let code = SdkEventCode::from_name(event).as_raw();
        if code == 0 {
            log_e!(TAG, "Invalid event name: {}", event);
            return SubscriptionID::error();
        }

        let sub_id = SubscriptionID::new(event);

        self.listeners.entry(code).or_default().push(Listener {
            sub_id_value: sub_id.value.clone(),
            callback: Arc::new(callback),
        });

        sub_id
    }

    pub fn subscribe_internal<F>(&self, event: &str, callback: F)
    where
        F: Fn(SdkEvent) -> bool + Send + Sync + 'static,
    {
        let code = SdkEventCode::from_name(event).as_raw();
        if code == 0 {
            log_e!(TAG, "Invalid internal event name: {}", event);
            return;
        }

        self.internal_listeners
            .entry(code)
            .or_default()
            .push(InternalListener {
                id: uuid::Uuid::new_v4().to_string(),
                callback: Arc::new(callback),
            });
    }

    pub fn unsubscribe(&self, event: &str) {
        let code = SdkEventCode::from_name(event).as_raw();
        self.listeners.remove(&code);
    }

    pub fn unsubscribe_by_id(&self, subscription_id: &SubscriptionID) {
        let code = SdkEventCode::from_name(&subscription_id.event).as_raw();
        let mut listeners = match self.listeners.get_mut(&code) {
            Some(listeners) => listeners,
            None => return,
        };

        listeners.retain(|listener| listener.sub_id_value != subscription_id.value);
    }

    pub fn unsubscribe_all(&self) {
        self.listeners.clear();
    }

    pub(crate) fn emit(&self, event: SdkEvent) {
        let all_code = SdkEventCode::from_name(SdkEvent::ALL).as_raw();
        let event_code = event.get_code().as_raw();

        let all_listeners = self.snapshot_listeners(all_code);
        let all_internal_listeners = self.snapshot_internal_listeners(all_code);
        let event_listeners = self.snapshot_listeners(event_code);
        let event_internal_listeners = self.snapshot_internal_listeners(event_code);

        Self::emit_to_listeners(&event, &all_listeners);
        self.emit_to_internal_listeners(&event, all_code, &all_internal_listeners);
        Self::emit_to_listeners(&event, &event_listeners);
        self.emit_to_internal_listeners(&event, event_code, &event_internal_listeners);
    }

    fn snapshot_listeners(&self, code: u8) -> Vec<Listener> {
        self.listeners
            .get(&code)
            .map(|listeners| listeners.value().clone())
            .unwrap_or_default()
    }

    fn snapshot_internal_listeners(&self, code: u8) -> Vec<InternalListener> {
        self.internal_listeners
            .get(&code)
            .map(|listeners| listeners.value().clone())
            .unwrap_or_default()
    }

    fn emit_to_listeners(event: &SdkEvent, listeners: &[Listener]) {
        listeners
            .iter()
            .for_each(|listener| (listener.callback)(event.clone()));
    }

    fn emit_to_internal_listeners(
        &self,
        event: &SdkEvent,
        code: u8,
        listeners: &[InternalListener],
    ) {
        let expired_ids = listeners
            .iter()
            .filter_map(|listener| {
                if (listener.callback)(event.clone()) {
                    None
                } else {
                    Some(listener.id.as_str())
                }
            })
            .collect::<Vec<_>>();

        if expired_ids.is_empty() {
            return;
        }

        // Callback execution has completed and this thread holds no listener-map
        // guard. Wait for the shard so expired one-shot listeners cannot be
        // retained indefinitely under sustained contention.
        if let Some(mut listeners) = self.internal_listeners.get_mut(&code) {
            listeners.retain(|listener| !expired_ids.contains(&listener.id.as_str()));
        }
    }
}

impl Deref for Statsig {
    type Target = SdkEventEmitter;

    fn deref(&self) -> &Self::Target {
        &self.event_emitter
    }
}

impl Statsig {
    pub(crate) fn emit_gate_evaluated(
        &self,
        gate_name: &str,
        rule_id: &str,
        value: bool,
        reason: &str,
    ) {
        self.emit(SdkEvent::GateEvaluated {
            gate_name,
            rule_id,
            value,
            reason,
        });
    }

    pub(crate) fn emit_dynamic_config_evaluated(&self, config: &DynamicConfig) {
        self.emit(SdkEvent::DynamicConfigEvaluated {
            config_name: config.name.as_str(),
            reason: config.details.reason.as_str(),
            rule_id: Some(config.rule_id.as_str()),
            value: config.__evaluation.as_ref().map(|e| &e.value),
        });
    }

    pub(crate) fn emit_experiment_evaluated(&self, experiment: &Experiment) {
        self.emit(SdkEvent::ExperimentEvaluated {
            experiment_name: experiment.name.as_str(),
            reason: experiment.details.reason.as_str(),
            rule_id: Some(experiment.rule_id.as_str()),
            value: experiment.__evaluation.as_ref().map(|e| &e.value),
            group_name: experiment.group_name.as_deref(),
        });
    }

    pub(crate) fn emit_layer_evaluated(&self, layer: &Layer) {
        self.emit(SdkEvent::LayerEvaluated {
            layer_name: layer.name.as_str(),
            reason: layer.details.reason.as_str(),
            rule_id: Some(layer.rule_id.as_str()),
        });
    }
}

#[cfg(feature = "ffi-support")]
impl Statsig {
    pub(crate) fn emit_gate_evaluated_parts(
        &self,
        gate_name: &str,
        reason: &str,
        eval_result: Option<&crate::evaluation::evaluator_result::EvaluatorResult>,
    ) {
        let mut rule_id = None;
        let mut value = false;

        if let Some(eval) = eval_result {
            rule_id = eval.rule_id.as_ref().map(|r| r.as_str());
            value = eval.bool_value;
        }

        self.emit(SdkEvent::GateEvaluated {
            gate_name,
            rule_id: rule_id.unwrap_or_default(),
            value,
            reason,
        });
    }

    pub(crate) fn emit_dynamic_config_evaluated_parts(
        &self,
        config_name: &str,
        reason: &str,
        eval_result: Option<&crate::evaluation::evaluator_result::EvaluatorResult>,
    ) {
        let mut rule_id = None;
        let mut value = None;

        if let Some(eval) = eval_result {
            rule_id = eval.rule_id.as_ref().map(|r| r.as_str());
            value = eval.json_value.as_ref();
        }

        self.emit(SdkEvent::DynamicConfigEvaluated {
            config_name,
            reason,
            rule_id,
            value,
        });
    }

    pub(crate) fn emit_experiment_evaluated_parts(
        &self,
        experiment_name: &str,
        reason: &str,
        eval_result: Option<&crate::evaluation::evaluator_result::EvaluatorResult>,
    ) {
        let mut rule_id = None;
        let mut value = None;
        let mut group_name = None;

        if let Some(eval) = eval_result {
            rule_id = eval.rule_id.as_ref().map(|r| r.as_str());
            value = eval.json_value.as_ref();
            group_name = eval.group_name.as_ref().map(|g| g.as_str());
        }

        self.emit(SdkEvent::ExperimentEvaluated {
            experiment_name,
            reason,
            rule_id,
            value,
            group_name,
        });
    }

    pub(crate) fn emit_layer_evaluated_parts(
        &self,
        layer_name: &str,
        reason: &str,
        eval_result: Option<&crate::evaluation::evaluator_result::EvaluatorResult>,
    ) {
        let mut rule_id = None;

        if let Some(eval) = eval_result {
            rule_id = eval.rule_id.as_ref().map(|r| r.as_str());
        }

        self.emit(SdkEvent::LayerEvaluated {
            layer_name,
            reason,
            rule_id,
        });
    }
}

#[cfg(test)]
mod cleanup_tests {
    use super::*;
    use std::{
        sync::{
            atomic::{AtomicUsize, Ordering},
            mpsc, Arc, Barrier,
        },
        thread,
        time::Duration,
    };

    #[test]
    fn contended_cleanup_waits_and_prunes_dead_internal_listener() {
        let emitter = Arc::new(SdkEventEmitter::default());
        let callback_count = Arc::new(AtomicUsize::new(0));
        let callback_started = Arc::new(Barrier::new(2));
        let callback_can_return = Arc::new(Barrier::new(2));

        let callback_count_clone = Arc::clone(&callback_count);
        let callback_started_clone = Arc::clone(&callback_started);
        let callback_can_return_clone = Arc::clone(&callback_can_return);
        emitter.subscribe_internal(SdkEvent::GATE_EVALUATED, move |_| {
            let invocation = callback_count_clone.fetch_add(1, Ordering::SeqCst);
            if invocation == 0 {
                callback_started_clone.wait();
                callback_can_return_clone.wait();
            }
            false
        });

        let emitter_clone = Arc::clone(&emitter);
        let (emit_done_tx, emit_done_rx) = mpsc::channel();
        let emit_thread = thread::spawn(move || {
            emitter_clone.emit(SdkEvent::GateEvaluated {
                gate_name: "test_gate",
                rule_id: "test_rule_id",
                value: true,
                reason: "test_reason",
            });
            emit_done_tx
                .send(())
                .expect("emit receiver should remain open");
        });

        callback_started.wait();
        let code = SdkEventCode::GateEvaluated.as_raw();
        let shard_guard = emitter
            .internal_listeners
            .get_mut(&code)
            .expect("internal listener should exist");
        callback_can_return.wait();

        assert!(
            emit_done_rx
                .recv_timeout(Duration::from_millis(250))
                .is_err(),
            "emit should wait for contended listener cleanup"
        );

        drop(shard_guard);
        emit_done_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("emit should finish after the shard lock is released");
        emit_thread.join().expect("emit thread should not panic");

        emitter.emit(SdkEvent::GateEvaluated {
            gate_name: "test_gate",
            rule_id: "test_rule_id",
            value: true,
            reason: "test_reason",
        });
        assert_eq!(callback_count.load(Ordering::SeqCst), 1);
    }
}
