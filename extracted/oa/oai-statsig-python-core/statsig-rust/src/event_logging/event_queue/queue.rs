use super::{
    batch::{EnqueuedEvent, EventBatch},
    queued_event::QueuedEvent,
};
use crate::{
    event_logging::statsig_event_internal::StatsigEventInternal, log_d, read_lock_or_return,
    write_lock_or_return,
};
use chrono::Utc;
use parking_lot::RwLock;
use std::collections::VecDeque;

const TAG: &str = stringify!(EventQueue);

pub enum QueueAddResult {
    Noop,
    NeedsFlush,
    NeedsFlushAndDropped(u64),
}

pub enum QueueReconcileResult {
    Success,
    DroppedEvents(u64),
    LockFailure,
}

pub struct EventQueue {
    pub batch_size: usize,
    pub max_pending_batches: usize,

    pending_events: RwLock<VecDeque<EnqueuedEvent<QueuedEvent>>>,
    batches: RwLock<VecDeque<EventBatch>>,
    max_pending_events: usize,
}

impl EventQueue {
    pub fn new(batch_size: u32, max_queue_size: u32) -> Self {
        let batch_size = batch_size as usize;
        let max_queue_size = max_queue_size as usize;

        Self {
            pending_events: RwLock::new(VecDeque::new()),
            batches: RwLock::new(VecDeque::new()),
            batch_size,
            max_pending_batches: max_queue_size,
            max_pending_events: batch_size * max_queue_size,
        }
    }

    pub fn approximate_pending_events_count(&self) -> usize {
        let pending_len = read_lock_or_return!(TAG, self.pending_events, 0).len();
        let batches_len = read_lock_or_return!(TAG, self.batches, 0).len();
        pending_len + (batches_len * self.batch_size)
    }

    pub fn add(&self, pending_event: QueuedEvent) -> QueueAddResult {
        self.add_with_enqueue_time(pending_event, Utc::now().timestamp_millis() as u64)
    }

    fn add_with_enqueue_time(
        &self,
        pending_event: QueuedEvent,
        enqueued_at_ms: u64,
    ) -> QueueAddResult {
        let mut pending_events =
            write_lock_or_return!(TAG, self.pending_events, QueueAddResult::Noop);
        pending_events.push_back(EnqueuedEvent::new(pending_event, enqueued_at_ms));

        let mut dropped_events = 0;
        while pending_events.len() > self.max_pending_events {
            pending_events.pop_front();
            dropped_events += 1;
        }

        if dropped_events > 0 {
            return QueueAddResult::NeedsFlushAndDropped(dropped_events);
        }

        if pending_events.len() % self.batch_size == 0 {
            return QueueAddResult::NeedsFlush;
        }

        QueueAddResult::Noop
    }

    pub(crate) fn requeue_batch(&self, batch: EventBatch) -> QueueReconcileResult {
        let len = batch.len() as u64;
        let mut batches =
            write_lock_or_return!(TAG, self.batches, QueueReconcileResult::DroppedEvents(len));

        if batches.len() > self.max_pending_batches {
            return QueueReconcileResult::DroppedEvents(len);
        }

        log_d!(
            TAG,
            "Requeueing batch with {} events and {} attempts to flush",
            batch.len(),
            batch.attempts()
        );

        batches.push_back(batch);
        QueueReconcileResult::Success
    }

    pub fn contains_at_least_one_full_batch(&self) -> bool {
        let pending_events_count = self
            .pending_events
            .try_read_for(std::time::Duration::from_secs(5))
            .map(|e| e.len())
            .unwrap_or(0);
        if pending_events_count >= self.batch_size {
            return true;
        }

        let batches = read_lock_or_return!(TAG, self.batches, false);
        for batch in batches.iter() {
            if batch.len() >= self.batch_size {
                return true;
            }
        }

        false
    }

    pub(crate) fn take_all_batches(&self) -> VecDeque<EventBatch> {
        let mut batches = write_lock_or_return!(TAG, self.batches, VecDeque::new());
        std::mem::take(&mut *batches)
    }

    pub(crate) fn take_next_batch(&self) -> Option<EventBatch> {
        let mut batches = write_lock_or_return!(TAG, self.batches, None);
        batches.pop_front()
    }

    pub fn reconcile_batching(&self) -> QueueReconcileResult {
        let pending_events: VecDeque<EnqueuedEvent<StatsigEventInternal>> = self
            .take_all_pending_events()
            .into_iter()
            .map(|event| event.map(QueuedEvent::into_statsig_event_internal))
            .collect();

        if pending_events.is_empty() {
            return QueueReconcileResult::Success;
        }

        let mut batches =
            write_lock_or_return!(TAG, self.batches, QueueReconcileResult::LockFailure);
        let old_batches = std::mem::take(&mut *batches);

        let (full_batches, partial_batches): (VecDeque<_>, VecDeque<_>) = old_batches
            .into_iter()
            .partition(|batch| batch.len() >= self.batch_size);

        let mut events_to_batch = VecDeque::new();
        for batch in partial_batches {
            events_to_batch.extend(batch.into_events());
        }
        events_to_batch.extend(pending_events);

        let new_batches = self.create_batches(events_to_batch);

        batches.extend(full_batches);
        batches.extend(new_batches);

        let dropped_events_count = self.clamp_batches(&mut batches);
        if dropped_events_count > 0 {
            return QueueReconcileResult::DroppedEvents(dropped_events_count);
        }

        QueueReconcileResult::Success
    }

    fn take_all_pending_events(&self) -> VecDeque<EnqueuedEvent<QueuedEvent>> {
        let mut pending_events = write_lock_or_return!(TAG, self.pending_events, VecDeque::new());
        std::mem::take(&mut *pending_events)
    }

    fn create_batches(
        &self,
        mut pending_events: VecDeque<EnqueuedEvent<StatsigEventInternal>>,
    ) -> Vec<EventBatch> {
        let mut batches = Vec::new();
        while !pending_events.is_empty() {
            let drain_count = self.batch_size.min(pending_events.len());
            let chunk = pending_events.drain(..drain_count).collect::<Vec<_>>();
            batches.push(EventBatch::new(chunk));
        }

        batches
    }

    fn clamp_batches(&self, batches: &mut VecDeque<EventBatch>) -> u64 {
        if batches.len() <= self.max_pending_batches {
            return 0;
        }

        let mut dropped_events_count = 0;
        while batches.len() > self.max_pending_batches {
            if let Some(batch) = batches.pop_front() {
                dropped_events_count += batch.len() as u64;
            }
        }

        dropped_events_count
    }
}

#[cfg(test)]
mod tests {
    use std::borrow::Cow;

    use super::*;
    use crate::event_logging::event_queue::queued_event::{EnqueueOperation, QueuedEvent};
    use crate::event_logging::event_queue::queued_gate_expo::EnqueueGateExpoOp;
    use crate::event_logging::exposure_sampling::EvtSamplingDecision::ForceSampled;
    use crate::{
        EvaluationDetails, StatsigUser,
        event_logging::{
            event_logger::ExposureTrigger, statsig_event::StatsigEvent,
            statsig_event_internal::StatsigEventInternal,
        },
        statsig_types::FeatureGate,
        user::{StatsigUserInternal, StatsigUserLoggable},
    };

    #[test]
    fn test_adding_single_to_queue() {
        let (queue, user, gate) = setup(10, 10);
        let user_internal = StatsigUserInternal::new(&user, None);

        let enqueue_op = EnqueueGateExpoOp {
            exposure_time: 1,
            user: &user_internal,
            queried_gate_name: &gate.name,
            evaluation: gate.__evaluation.as_ref().map(Cow::Borrowed),
            details: EvaluationDetails::unrecognized_no_data(),
            trigger: ExposureTrigger::Auto,
        };

        let queued_event = enqueue_op.into_queued_event(ForceSampled);

        let result = queue.add(queued_event);

        assert!(matches!(result, QueueAddResult::Noop));
        assert_eq!(
            queue
                .pending_events
                .try_read_for(std::time::Duration::from_secs(5))
                .unwrap()
                .len(),
            1
        );
    }

    #[test]
    fn test_adding_multiple_to_queue() {
        let (queue, user, gate) = setup(1000, 20);
        let user_internal = StatsigUserInternal::new(&user, None);

        let mut triggered_count = 0;
        for _ in 0..4567 {
            let enqueue_op = EnqueueGateExpoOp {
                exposure_time: 1,
                user: &user_internal,
                queried_gate_name: &gate.name,
                evaluation: gate.__evaluation.as_ref().map(Cow::Borrowed),
                details: EvaluationDetails::unrecognized_no_data(),
                trigger: ExposureTrigger::Auto,
            };

            let result = queue.add(enqueue_op.into_queued_event(ForceSampled));

            if let QueueAddResult::NeedsFlush = result {
                triggered_count += 1;
            }
        }

        assert_eq!(
            queue
                .pending_events
                .try_read_for(std::time::Duration::from_secs(5))
                .unwrap()
                .len(),
            4567
        );
        assert_eq!(triggered_count, (4567 / 1000) as usize);
    }

    #[test]
    fn test_take_all_batches() {
        let batch_size = 200;
        let max_pending_batches = 40;

        let (queue, user, gate) = setup(batch_size, max_pending_batches);
        let user_internal = StatsigUserInternal::new(&user, None);

        for _ in 0..4567 {
            let enqueue_op = EnqueueGateExpoOp {
                exposure_time: 1,
                user: &user_internal,
                queried_gate_name: &gate.name,
                evaluation: gate.__evaluation.as_ref().map(Cow::Borrowed),
                details: EvaluationDetails::unrecognized_no_data(),
                trigger: ExposureTrigger::Auto,
            };
            queue.add(enqueue_op.into_queued_event(ForceSampled));
        }

        queue.reconcile_batching();
        let batches = queue.take_all_batches();
        assert_eq!(batches.len(), (4567.0 / batch_size as f64).ceil() as usize,);
    }

    #[test]
    fn test_take_next_batch() {
        let batch_size = 200;
        let max_pending_batches = 20;

        let (queue, user, gate) = setup(batch_size, max_pending_batches);
        let user_internal = StatsigUserInternal::new(&user, None);

        for _ in 0..4567 {
            let enqueue_op = EnqueueGateExpoOp {
                exposure_time: 1,
                user: &user_internal,
                queried_gate_name: &gate.name,
                evaluation: gate.__evaluation.as_ref().map(Cow::Borrowed),
                details: EvaluationDetails::unrecognized_no_data(),
                trigger: ExposureTrigger::Auto,
            };
            queue.add(enqueue_op.into_queued_event(ForceSampled));
        }

        queue.reconcile_batching();
        let batch = queue.take_next_batch();
        assert_eq!(batch.unwrap().len(), batch_size as usize);

        assert_eq!(
            queue
                .batches
                .try_read_for(std::time::Duration::from_secs(5))
                .unwrap()
                .len(),
            (max_pending_batches - 1) as usize
        ); // max minus the one we just took
    }

    #[test]
    fn test_queue_time_is_independent_from_payload_event_time() {
        let queue = EventQueue::new(2, 1);
        queue.add_with_enqueue_time(make_passthrough_event(100), 300);
        queue.reconcile_batching();
        queue.add_with_enqueue_time(make_passthrough_event(200), 250);
        queue.reconcile_batching();

        let batch = queue.take_next_batch().unwrap();
        let event_times = batch
            .iter_events()
            .map(|event| event.time)
            .collect::<Vec<_>>();
        assert_eq!(event_times, vec![100, 200]);
        assert_eq!(batch.get_max_event_queue_time_ms(350), 100);
    }

    #[test]
    fn test_requeued_partial_batch_preserves_enqueue_time() {
        let queue = EventQueue::new(2, 2);
        queue.add_with_enqueue_time(make_passthrough_event(100), 250);
        queue.reconcile_batching();

        let batch = queue.take_next_batch().unwrap();
        queue.requeue_batch(batch);
        queue.add_with_enqueue_time(make_passthrough_event(200), 300);
        queue.reconcile_batching();

        let batch = queue.take_next_batch().unwrap();
        let event_times = batch
            .iter_events()
            .map(|event| event.time)
            .collect::<Vec<_>>();
        assert_eq!(event_times, vec![100, 200]);
        assert_eq!(batch.get_max_event_queue_time_ms(350), 100);
    }

    #[test]
    fn test_requeued_full_batch_preserves_enqueue_time_and_attempts() {
        let queue = EventQueue::new(2, 2);
        queue.add_with_enqueue_time(make_passthrough_event(100), 250);
        queue.add_with_enqueue_time(make_passthrough_event(200), 300);
        queue.reconcile_batching();

        let mut batch = queue.take_next_batch().unwrap();
        batch.increment_attempts();
        queue.requeue_batch(batch);

        let batch = queue.take_next_batch().unwrap();
        assert_eq!(batch.attempts(), 1);
        assert_eq!(batch.get_max_event_queue_time_ms(350), 100);
    }

    fn make_passthrough_event(time: u64) -> QueuedEvent {
        QueuedEvent::Passthrough(StatsigEventInternal::new(
            time,
            StatsigUserLoggable::null(),
            StatsigEvent {
                event_name: "test_event".to_string(),
                value: None,
                metadata: None,
                statsig_metadata: None,
            },
            None,
        ))
    }

    fn setup(batch_size: u32, max_queue_size: u32) -> (EventQueue, StatsigUser, FeatureGate) {
        let queue = EventQueue::new(batch_size, max_queue_size);
        let user = StatsigUser::with_user_id("user-id");
        let gate = FeatureGate {
            name: "gate-name".into(),
            value: true,
            rule_id: "rule-id".into(),
            id_type: "user-id".into(),
            details: EvaluationDetails::unrecognized_no_data(),
            __evaluation: None,
        };
        (queue, user, gate)
    }
}
