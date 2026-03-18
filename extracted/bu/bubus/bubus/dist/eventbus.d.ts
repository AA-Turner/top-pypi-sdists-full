/**
 * EventBus - the main event dispatcher and handler
 */
import { BaseEvent } from './event.js';
import type { EventHandler, EventBusOptions } from './types.js';
export declare class EventBus {
    readonly name: string;
    readonly parallel_handlers: boolean;
    readonly event_timeout: number;
    private handlers;
    private wildcardHandlers;
    private queue;
    private processing;
    private running;
    private idleDeferred?;
    private stopDeferred?;
    private eventHistory;
    private maxHistorySize;
    constructor(name: string, options?: EventBusOptions);
    /**
     * Register an event handler
     */
    on<T extends BaseEvent>(eventType: string | (new (...args: any[]) => T) | RegExp, handler: EventHandler<T>): void;
    /**
     * Dispatch an event
     */
    dispatch<T extends BaseEvent>(event: T): Promise<T>;
    /**
     * Process queued events
     */
    private processQueue;
    /**
     * Process a single event
     */
    private processEvent;
    /**
     * Execute a single handler
     */
    private executeHandler;
    /**
     * Stop the event bus
     */
    stop(timeout?: number): Promise<void>;
    /**
     * Wait until the event bus is idle
     */
    wait_until_idle(): Promise<void>;
    /**
     * Wait for a specific event
     */
    expect<T extends BaseEvent>(predicate: (event: BaseEvent) => event is T, timeout?: number): Promise<T>;
    /**
     * Forward events to another bus
     */
    forward_to(other: EventBus, pattern?: string | RegExp): void;
    /**
     * Get event history
     */
    get event_history(): ReadonlyArray<BaseEvent>;
    /**
     * Clear event history
     */
    clear_history(): void;
}
//# sourceMappingURL=eventbus.d.ts.map