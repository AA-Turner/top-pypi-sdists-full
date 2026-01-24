import { WaitWrite } from './wait_write.js';
import { StreamWrite } from './stream_write.js';
import { Assistant } from './assistant.js';
import { Thread } from './thread.js';

export class Benchmarks {
    static getRunner(type) {
        switch (type) {
            case WaitWrite.toString():
                return WaitWrite;
            case StreamWrite.toString():
                return StreamWrite;
            case Assistant.toString():
                return Assistant;
            case Thread.toString():
                return Thread;
            default:
                throw new Error(`Unknown benchmark type: ${type}`);
        }
    }
}
