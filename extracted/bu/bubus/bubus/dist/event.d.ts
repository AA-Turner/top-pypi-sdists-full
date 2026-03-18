/**
 * BaseEvent class - the foundation of all events
 */
import type { EventMetadata, EventResult, EventStatus } from './types.js';
export declare abstract class BaseEvent implements EventMetadata {
    readonly event_type: string;
    readonly event_id: string;
    readonly event_schema: string;
    readonly event_timeout: number;
    readonly event_path: string[];
    readonly event_parent_id?: string;
    readonly event_created_at: string;
    readonly event_results: Map<string, EventResult>;
    private _deferred;
    private _event_started_at?;
    private _event_completed_at?;
    constructor(metadata?: Partial<EventMetadata>);
    /**
     * Wait for the event to complete
     * Use this instead of await directly on the event to avoid thenable issues
     */
    wait(): Promise<this>;
    /**
     * Get the event status
     */
    get event_status(): EventStatus;
    /**
     * Get when the event started processing
     */
    get event_started_at(): string | undefined;
    /**
     * Get when the event completed processing
     */
    get event_completed_at(): string | undefined;
    /**
     * Mark event as started (called by EventBus)
     */
    _markStarted(): void;
    /**
     * Mark event as completed (called by EventBus)
     */
    _markCompleted(): void;
    /**
     * Mark event as failed (called by EventBus)
     */
    _markFailed(error: Error): void;
    /**
     * Get the first result value
     */
    event_result(): Promise<any>;
    /**
     * Get all result values as an array
     */
    event_results_list(): Promise<any[]>;
    /**
     * Get results as a flat dictionary (for dict results)
     */
    event_results_flat_dict(): Promise<Record<string, any>>;
    /**
     * Get results as a flat array (for array results)
     */
    event_results_flat_list(): Promise<any[]>;
    /**
     * Get results indexed by handler ID
     */
    event_results_by_handler_id(): Promise<Record<string, any>>;
    /**
     * Custom string representation
     */
    toString(): string;
}
/**
 * Helper to create event classes with proper typing
 */
export declare function createEventClass<T extends Record<string, any>>(eventType: string, schema?: string): new (data: T) => BaseEvent & T;
//# sourceMappingURL=event.d.ts.map