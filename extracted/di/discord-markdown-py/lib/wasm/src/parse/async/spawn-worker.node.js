import { Worker } from "node:worker_threads";

// worker_threads.Worker is an EventEmitter; adapt it to the EventTarget
// interface awaitMessage expects.
export function spawnWorker() {
	const worker = new Worker(new URL("./worker.js", import.meta.url));
	const target = new EventTarget();

	// Only hold the process open while a request is in flight: ref on
	// postMessage, unref once the response arrives.
	worker.unref();

	worker.on("message", (data) => {
		worker.unref();
		target.dispatchEvent(new MessageEvent("message", { data }));
	});

	worker.on("error", (error) => {
		worker.unref();
		target.dispatchEvent(new MessageEvent("error", { data: error.message }));
	});

	return {
		postMessage(message) {
			worker.ref();
			worker.postMessage(message);
		},
		addEventListener: target.addEventListener.bind(target),
		removeEventListener: target.removeEventListener.bind(target),
	};
}
