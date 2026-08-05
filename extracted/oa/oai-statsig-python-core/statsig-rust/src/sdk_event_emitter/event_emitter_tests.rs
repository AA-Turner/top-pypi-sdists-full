use serde_json::json;

use crate::{
    DynamicReturnable,
    sdk_event_emitter::{SdkEvent, SdkEventEmitter, SubscriptionID},
};
use std::sync::{
    Arc,
    atomic::{AtomicBool, AtomicUsize, Ordering},
    mpsc,
};
use std::time::Duration;

fn sub(
    event_emitter: &mut SdkEventEmitter,
    event_name: &str,
) -> (SubscriptionID, Arc<AtomicUsize>) {
    let counter = Arc::new(AtomicUsize::new(0));
    let counter_clone = counter.clone();
    let id = event_emitter.subscribe(event_name, move |_| {
        counter_clone.fetch_add(1, Ordering::SeqCst);
    });

    (id, counter)
}

fn sub_internal(event_emitter: &mut SdkEventEmitter, event_name: &str) -> Arc<AtomicUsize> {
    let counter = Arc::new(AtomicUsize::new(0));
    let counter_clone = counter.clone();
    event_emitter.subscribe_internal(event_name, move |_| {
        counter_clone.fetch_add(1, Ordering::SeqCst);
        true
    });

    counter
}

fn emit(event_emitter: &mut SdkEventEmitter, event_name: &str) {
    match event_name {
        SdkEvent::GATE_EVALUATED => {
            event_emitter.emit(SdkEvent::GateEvaluated {
                gate_name: "test_gate",
                rule_id: "test_rule_id",
                value: true,
                reason: "test_reason",
            });
        }
        SdkEvent::DYNAMIC_CONFIG_EVALUATED => {
            event_emitter.emit(SdkEvent::DynamicConfigEvaluated {
                config_name: "test_dynamic_config",
                reason: "test_reason",
                rule_id: Some("test_rule_id"),
                value: Some(&DynamicReturnable::from_map(
                    std::collections::HashMap::from([(
                        "test_param".to_string(),
                        json!("test_value"),
                    )]),
                )),
            });
        }
        _ => {
            panic!("Unsupported event: {event_name}");
        }
    }
}

#[test]
fn test_unsub_by_event() {
    let mut event_emitter = SdkEventEmitter::default();

    let (_, first_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let (_, second_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let (_, third_counter) = sub(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);

    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 1);
    assert_eq!(third_counter.load(Ordering::SeqCst), 0);

    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);
    assert_eq!(third_counter.load(Ordering::SeqCst), 1);

    event_emitter.unsubscribe(SdkEvent::GATE_EVALUATED);
    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);

    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 1);
    assert_eq!(third_counter.load(Ordering::SeqCst), 1);

    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);
    assert_eq!(third_counter.load(Ordering::SeqCst), 2);
}

#[test]
fn test_unsub_by_event_and_id() {
    let mut event_emitter = SdkEventEmitter::default();

    let (first_id, first_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let (_, second_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let (_, third_counter) = sub(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 1);
    assert_eq!(third_counter.load(Ordering::SeqCst), 1);

    event_emitter.unsubscribe_by_id(&first_id);
    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 2);
    assert_eq!(third_counter.load(Ordering::SeqCst), 2);
}

#[test]
fn test_unsub_all() {
    let mut event_emitter = SdkEventEmitter::default();

    let (_, first_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let (_, second_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let (_, third_counter) = sub(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 1);
    assert_eq!(third_counter.load(Ordering::SeqCst), 1);

    event_emitter.unsubscribe_all();

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);

    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 1);
    assert_eq!(third_counter.load(Ordering::SeqCst), 1);
}

#[test]
fn test_sub_all() {
    let mut event_emitter = SdkEventEmitter::default();
    let (_, counter) = sub(&mut event_emitter, SdkEvent::ALL);

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(counter.load(Ordering::SeqCst), 1);

    emit(&mut event_emitter, SdkEvent::DYNAMIC_CONFIG_EVALUATED);
    assert_eq!(counter.load(Ordering::SeqCst), 2);
}

#[test]
fn test_internal_listeners_survive_public_unsubscribe_flows() {
    let mut event_emitter = SdkEventEmitter::default();

    let (_, public_counter) = sub(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    let internal_counter = sub_internal(&mut event_emitter, SdkEvent::GATE_EVALUATED);

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(public_counter.load(Ordering::SeqCst), 1);
    assert_eq!(internal_counter.load(Ordering::SeqCst), 1);

    event_emitter.unsubscribe(SdkEvent::GATE_EVALUATED);
    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(public_counter.load(Ordering::SeqCst), 1);
    assert_eq!(internal_counter.load(Ordering::SeqCst), 2);

    event_emitter.unsubscribe_all();
    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(public_counter.load(Ordering::SeqCst), 1);
    assert_eq!(internal_counter.load(Ordering::SeqCst), 3);
}

#[test]
fn test_dead_internal_listeners_are_pruned() {
    let mut event_emitter = SdkEventEmitter::default();
    let counter = Arc::new(AtomicUsize::new(0));
    let counter_clone = counter.clone();
    let alive = Arc::new(AtomicBool::new(true));
    let alive_clone = alive.clone();

    event_emitter.subscribe_internal(SdkEvent::GATE_EVALUATED, move |_| {
        counter_clone.fetch_add(1, Ordering::SeqCst);
        alive_clone.load(Ordering::SeqCst)
    });

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(counter.load(Ordering::SeqCst), 1);

    alive.store(false, Ordering::SeqCst);
    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(counter.load(Ordering::SeqCst), 2);

    emit(&mut event_emitter, SdkEvent::GATE_EVALUATED);
    assert_eq!(counter.load(Ordering::SeqCst), 2);
}

#[test]
fn test_public_listener_can_unsubscribe_during_callback() {
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let callback_emitter = event_emitter.clone();

    event_emitter.subscribe(SdkEvent::GATE_EVALUATED, move |_| {
        callback_emitter.unsubscribe(SdkEvent::GATE_EVALUATED);
    });

    let (completed_tx, completed_rx) = mpsc::channel();
    std::thread::spawn(move || {
        emit_gate(&event_emitter);
        completed_tx.send(()).unwrap();
    });

    assert!(
        completed_rx
            .recv_timeout(Duration::from_millis(500))
            .is_ok(),
        "event callback deadlocked while unsubscribing from its own event"
    );
}

#[test]
fn test_internal_listener_can_subscribe_during_callback_with_snapshot_semantics() {
    let event_emitter = Arc::new(SdkEventEmitter::default());
    let callback_emitter = event_emitter.clone();
    let first_counter = Arc::new(AtomicUsize::new(0));
    let first_counter_clone = first_counter.clone();
    let second_counter = Arc::new(AtomicUsize::new(0));
    let second_counter_clone = second_counter.clone();

    event_emitter.subscribe_internal(SdkEvent::GATE_EVALUATED, move |_| {
        first_counter_clone.fetch_add(1, Ordering::SeqCst);
        let second_counter = second_counter_clone.clone();
        callback_emitter.subscribe_internal(SdkEvent::GATE_EVALUATED, move |_| {
            second_counter.fetch_add(1, Ordering::SeqCst);
            true
        });
        true
    });

    let (completed_tx, completed_rx) = mpsc::channel();
    let emitter = event_emitter.clone();
    std::thread::spawn(move || {
        emit_gate(&emitter);
        completed_tx.send(()).unwrap();
    });

    assert!(
        completed_rx
            .recv_timeout(Duration::from_millis(500))
            .is_ok(),
        "internal event callback deadlocked while subscribing to its own event"
    );
    assert_eq!(first_counter.load(Ordering::SeqCst), 1);
    assert_eq!(second_counter.load(Ordering::SeqCst), 0);

    emit_gate(&event_emitter);
    assert_eq!(first_counter.load(Ordering::SeqCst), 2);
    assert_eq!(second_counter.load(Ordering::SeqCst), 1);
}

fn emit_gate(event_emitter: &SdkEventEmitter) {
    event_emitter.emit(SdkEvent::GateEvaluated {
        gate_name: "test_gate",
        rule_id: "test_rule_id",
        value: true,
        reason: "test_reason",
    });
}
