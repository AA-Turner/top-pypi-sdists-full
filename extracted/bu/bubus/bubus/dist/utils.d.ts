/**
 * Utility functions for the event system
 */
import { uuidv7 } from 'uuidv7';
import type { Deferred, EventResult, SerializedEvent } from './types.js';
export { uuidv7 };
/**
 * Creates a deferred promise
 */
export declare function createDeferred<T>(): Deferred<T>;
export declare const runWithParent: <T>(parentId: string, fn: () => T) => T;
export declare const getCurrentParentId: () => string | undefined;
/**
 * Creates an EventResult object
 */
export declare function createEventResult(handlerId: string, handlerName: string, eventbusId: string, eventbusName: string, eventParentId: string, timeout?: number): EventResult;
/**
 * Converts a Map to a plain object for serialization
 */
export declare function mapToObject<K extends string | number | symbol, V>(map: Map<K, V>): Record<K, V>;
/**
 * Converts a plain object to a Map
 */
export declare function objectToMap<K extends string | number | symbol, V>(obj: Record<K, V>): Map<K, V>;
/**
 * Serializes an event to a JSON-compatible format
 */
export declare function serializeEvent(event: any): SerializedEvent;
/**
 * Run a function with a timeout
 */
export declare function withTimeout<T>(promise: Promise<T>, timeoutMs: number, message?: string): Promise<T>;
//# sourceMappingURL=utils.d.ts.map