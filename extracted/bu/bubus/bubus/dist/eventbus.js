/**
 * EventBus - the main event dispatcher and handler
 */
import { uuidv7, createEventResult, runWithParent, withTimeout, createDeferred } from './utils.js';
export class EventBus {
    name;
    parallel_handlers;
    event_timeout;
    handlers = new Map();
    wildcardHandlers = [];
    queue = [];
    processing = false;
    running = true;
    idleDeferred;
    stopDeferred;
    // Event history for expect() functionality
    eventHistory = [];
    maxHistorySize = 1000;
    constructor(name, options = {}) {
        this.name = name;
        this.parallel_handlers = options.parallel_handlers ?? false;
        this.event_timeout = options.event_timeout ?? 60;
    }
    /**
     * Register an event handler
     */
    on(eventType, handler) {
        const handlerReg = {
            id: handler.name || uuidv7(),
            name: handler.name || 'anonymous',
            handler: handler,
            pattern: typeof eventType === 'function'
                ? eventType.prototype.event_type || eventType.name
                : eventType,
        };
        if (typeof handlerReg.pattern === 'string') {
            if (handlerReg.pattern === '*') {
                this.wildcardHandlers.push(handlerReg);
            }
            else {
                if (!this.handlers.has(handlerReg.pattern)) {
                    this.handlers.set(handlerReg.pattern, []);
                }
                this.handlers.get(handlerReg.pattern).push(handlerReg);
            }
        }
        else if (handlerReg.pattern instanceof RegExp) {
            this.wildcardHandlers.push(handlerReg);
        }
        // Check for duplicate handler names
        const allHandlers = [
            ...Array.from(this.handlers.values()).flat(),
            ...this.wildcardHandlers,
        ];
        const names = allHandlers.map(h => h.name).filter(n => n !== 'anonymous');
        const duplicates = names.filter((n, i) => names.indexOf(n) !== i);
        if (duplicates.length > 0) {
            console.warn(`Duplicate handler names detected: ${duplicates.join(', ')}`);
        }
    }
    /**
     * Dispatch an event
     */
    async dispatch(event) {
        if (!this.running) {
            throw new Error(`EventBus ${this.name} is stopped`);
        }
        // Check for loops
        if (event.event_path.includes(this.name)) {
            console.warn(`Event ${event.event_type} already processed by ${this.name}, skipping`);
            return event;
        }
        // Add to path
        event.event_path.push(this.name);
        // Queue the event
        this.queue.push({ event, addedAt: Date.now() });
        // Start processing if not already running
        if (!this.processing) {
            this.processing = true;
            queueMicrotask(() => this.processQueue());
        }
        return event;
    }
    /**
     * Process queued events
     */
    async processQueue() {
        while (this.running && this.queue.length > 0) {
            const queued = this.queue.shift();
            try {
                await this.processEvent(queued.event);
                // Add to history
                this.eventHistory.push(queued.event);
                if (this.eventHistory.length > this.maxHistorySize) {
                    this.eventHistory.shift();
                }
            }
            catch (error) {
                console.error(`Error processing event ${queued.event.event_type}:`, error);
                queued.event._markFailed(error);
            }
        }
        this.processing = false;
        // Check if we're idle
        if (this.queue.length === 0 && this.idleDeferred) {
            this.idleDeferred.resolve();
            this.idleDeferred = undefined;
        }
        // Check if we're stopping
        if (!this.running && this.queue.length === 0 && this.stopDeferred) {
            this.stopDeferred.resolve();
            this.stopDeferred = undefined;
        }
    }
    /**
     * Process a single event
     */
    async processEvent(event) {
        event._markStarted();
        // Find matching handlers
        const handlers = [
            ...(this.handlers.get(event.event_type) || []),
            ...this.wildcardHandlers.filter(h => {
                if (typeof h.pattern === 'string')
                    return h.pattern === '*';
                if (h.pattern instanceof RegExp)
                    return h.pattern.test(event.event_type);
                return false;
            }),
        ];
        if (handlers.length === 0) {
            event._markCompleted();
            return;
        }
        // Execute handlers
        if (this.parallel_handlers) {
            // Run all handlers in parallel
            const promises = handlers.map(h => this.executeHandler(h, event));
            await Promise.allSettled(promises);
        }
        else {
            // Run handlers sequentially
            for (const handler of handlers) {
                try {
                    await this.executeHandler(handler, event);
                }
                catch (error) {
                    // Error already recorded in event results
                    console.error(`Handler ${handler.name} failed:`, error);
                }
            }
        }
        event._markCompleted();
    }
    /**
     * Execute a single handler
     */
    async executeHandler(registration, event) {
        const eventResult = createEventResult(registration.id, registration.name, this.name, this.name, event.event_id, this.event_timeout);
        event.event_results.set(eventResult.id, eventResult);
        eventResult.status = 'started';
        eventResult.started_at = new Date().toISOString();
        try {
            // Run handler with parent context
            const handlerPromise = runWithParent(event.event_id, () => Promise.resolve(registration.handler(event)));
            // Add timeout
            const timeout = eventResult.timeout || event.event_timeout || this.event_timeout;
            const result = await withTimeout(handlerPromise, timeout * 1000, `Handler ${registration.name} timed out after ${timeout}s`);
            eventResult.result = result;
            eventResult.status = 'completed';
        }
        catch (error) {
            eventResult.error = error.message;
            eventResult.status = 'error';
            throw error;
        }
        finally {
            eventResult.completed_at = new Date().toISOString();
        }
    }
    /**
     * Stop the event bus
     */
    async stop(timeout) {
        this.running = false;
        if (this.queue.length === 0) {
            return;
        }
        this.stopDeferred = createDeferred();
        if (timeout) {
            try {
                await withTimeout(this.stopDeferred.promise, timeout * 1000, `EventBus ${this.name} stop timed out`);
            }
            catch {
                // Force clear the queue
                this.queue = [];
                if (this.stopDeferred) {
                    this.stopDeferred.resolve();
                }
            }
        }
        else {
            await this.stopDeferred.promise;
        }
    }
    /**
     * Wait until the event bus is idle
     */
    async wait_until_idle() {
        if (this.queue.length === 0 && !this.processing) {
            return;
        }
        this.idleDeferred = createDeferred();
        await this.idleDeferred.promise;
    }
    /**
     * Wait for a specific event
     */
    async expect(predicate, timeout) {
        // Check history first
        for (let i = this.eventHistory.length - 1; i >= 0; i--) {
            if (predicate(this.eventHistory[i])) {
                return this.eventHistory[i];
            }
        }
        // Wait for future event
        const deferred = createDeferred();
        const handler = (event) => {
            if (predicate(event)) {
                deferred.resolve(event);
            }
        };
        // Register temporary wildcard handler
        this.on('*', handler);
        try {
            if (timeout) {
                return await withTimeout(deferred.promise, timeout * 1000, 'expect() timed out');
            }
            else {
                return await deferred.promise;
            }
        }
        finally {
            // Remove the handler
            const index = this.wildcardHandlers.findIndex(h => h.handler === handler);
            if (index !== -1) {
                this.wildcardHandlers.splice(index, 1);
            }
        }
    }
    /**
     * Forward events to another bus
     */
    forward_to(other, pattern) {
        const handler = async (event) => {
            // Avoid infinite loops
            if (!event.event_path.includes(other.name)) {
                await other.dispatch(event);
            }
        };
        if (pattern) {
            this.on(pattern, handler);
        }
        else {
            this.on('*', handler);
        }
    }
    /**
     * Get event history
     */
    get event_history() {
        return [...this.eventHistory];
    }
    /**
     * Clear event history
     */
    clear_history() {
        this.eventHistory = [];
    }
}
//# sourceMappingURL=eventbus.js.map