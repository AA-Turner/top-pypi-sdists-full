import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List


class StreamDebugLogger:
    """Debug logging component for stream processing pipeline."""
    
    def __init__(self, enabled: bool = False, log_interval: float = 30.0):
        """Initialize debug logger.
        
        Args:
            enabled: Whether debug logging is enabled
            log_interval: Interval between debug log messages in seconds
        """
        self.enabled = enabled
        self.log_interval = log_interval
        self.logger = logging.getLogger(f"{__name__}.DebugLogger")
        self.last_log_time = 0
        self.start_time = time.time()
        
        # Metrics tracking
        self.log_count = 0
        self.metric_snapshots: List[Dict] = []
        
    def enable(self):
        """Enable debug logging."""
        self.enabled = True
        self.logger.info("Stream debug logging ENABLED")
        
    def disable(self):
        """Disable debug logging."""
        self.enabled = False
        self.logger.info("Stream debug logging DISABLED")
        
    def should_log(self) -> bool:
        """Check if we should log based on interval."""
        if not self.enabled:
            return False
            
        current_time = time.time()
        if current_time - self.last_log_time >= self.log_interval:
            self.last_log_time = current_time
            return True
        return False
        
    def log_pipeline_status(self, stream_manager):
        """Log pipeline status if enabled and interval passed."""
        if not self.should_log():
            return
            
        try:
            self.log_count += 1
            runtime = time.time() - self.start_time
            
            metrics = stream_manager.get_metrics()
            
            # Extract key metrics
            worker_counts = metrics.get('worker_counts', {})
            queue_sizes = metrics.get('queue_sizes', {})
            worker_metrics = metrics.get('worker_metrics', {})
            
            # Calculate totals
            consumers = worker_metrics.get('consumers', {})
            inference = worker_metrics.get('inference', {})
            producers = worker_metrics.get('producers', {})
            
            total_consumed = sum(w.get('messages_consumed', 0) for w in consumers.values())
            total_processed = sum(w.get('messages_processed', 0) for w in inference.values())
            total_output = sum(w.get('messages_output', 0) for w in inference.values())
            total_produced = sum(w.get('messages_produced', 0) for w in producers.values())
            
            running_consumers = sum(1 for w in consumers.values() if w.get('is_running'))
            running_inference = sum(1 for w in inference.values() if w.get('is_running'))
            running_producers = sum(1 for w in producers.values() if w.get('is_running'))
            
            # Log comprehensive status
            self.logger.info(
                f"🔄 PIPELINE STATUS #{self.log_count} (T+{runtime:.1f}s) | "
                f"Workers: C:{running_consumers}/{worker_counts.get('consumers', 0)} "
                f"I:{running_inference}/{worker_counts.get('inference_workers', 0)} "
                f"P:{running_producers}/{worker_counts.get('producers', 0)} | "
                f"Queues: IN:{queue_sizes.get('input_queue', 0)} OUT:{queue_sizes.get('output_queue', 0)} | "
                f"Flow: {total_consumed}→{total_processed}→{total_output}→{total_produced}"
            )
            
            # Store snapshot for trend analysis
            snapshot = {
                'timestamp': datetime.now(timezone.utc),
                'runtime': runtime,
                'total_consumed': total_consumed,
                'total_processed': total_processed,
                'total_output': total_output,
                'total_produced': total_produced,
                'input_queue_size': queue_sizes.get('input_queue', 0),
                'output_queue_size': queue_sizes.get('output_queue', 0),
                'running_workers': {
                    'consumers': running_consumers,
                    'inference': running_inference,
                    'producers': running_producers
                }
            }
            self.metric_snapshots.append(snapshot)
            
            # Keep only last 50 snapshots
            if len(self.metric_snapshots) > 50:
                self.metric_snapshots = self.metric_snapshots[-50:]
                
            # Detect issues
            self._detect_and_log_issues(snapshot, metrics)
            
        except Exception as exc:
            self.logger.error(f"Error in debug logging: {str(exc)}")
            
    def _detect_and_log_issues(self, snapshot: Dict, full_metrics: Dict):
        """Detect and log potential issues."""
        issues = []
        
        # Check for stopped workers
        running = snapshot['running_workers']
        if running['consumers'] == 0:
            issues.append("❌ NO CONSUMERS")
        if running['inference'] == 0:
            issues.append("❌ NO INFERENCE")
        if running['producers'] == 0:
            issues.append("❌ NO PRODUCERS")
            
        # Check for flow issues
        consumed = snapshot['total_consumed']
        processed = snapshot['total_processed']
        output = snapshot['total_output']
        produced = snapshot['total_produced']
        
        if consumed > processed + 10:  # Allow some buffer
            issues.append(f"⚠️ INPUT BACKLOG ({consumed - processed})")
        if output > produced + 10:
            issues.append(f"⚠️ OUTPUT BACKLOG ({output - produced})")
            
        # Check queue sizes
        if snapshot['input_queue_size'] > 100:
            issues.append(f"⚠️ INPUT QUEUE LARGE ({snapshot['input_queue_size']})")
        if snapshot['output_queue_size'] > 100:
            issues.append(f"⚠️ OUTPUT QUEUE LARGE ({snapshot['output_queue_size']})")
            
        # Check for dropped messages
        worker_metrics = full_metrics.get('worker_metrics', {})
        total_dropped = 0
        total_failed = 0
        
        for w in worker_metrics.get('consumers', {}).values():
            total_dropped += w.get('messages_dropped', 0)
        for w in worker_metrics.get('inference', {}).values():
            total_dropped += w.get('messages_dropped_output', 0)
        for w in worker_metrics.get('producers', {}).values():
            total_failed += w.get('messages_failed', 0)
            
        if total_dropped > 0:
            issues.append(f"⚠️ DROPPED ({total_dropped})")
        if total_failed > 0:
            issues.append(f"⚠️ FAILED ({total_failed})")
            
        # Log issues if found
        if issues:
            self.logger.warning(f"🚨 ISSUES DETECTED: {' | '.join(issues)}")
            
    def get_debug_summary(self) -> Dict[str, Any]:
        """Get debug logging summary."""
        runtime = time.time() - self.start_time
        return {
            'enabled': self.enabled,
            'log_interval': self.log_interval,
            'log_count': self.log_count,
            'runtime_seconds': runtime,
            'snapshots_stored': len(self.metric_snapshots),
            'last_log_time': self.last_log_time,
        }
