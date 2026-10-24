import { spawnWorker } from "#spawn-worker";
import { loadModule } from "../init.js";
import { INIT, PARSE, awaitMessage } from "./async/messages.js";

export { Syntax } from "@discord/markdown-types";

let workerPromise = null;

function createWorker() {
	workerPromise = loadModule()
		.then(async (wasmModule) => {
			const worker = spawnWorker();
			worker.postMessage({ type: INIT, module: wasmModule });
			await awaitMessage(worker, INIT);
			return worker;
		})
		.catch((e) => {
			workerPromise = null;
			throw e;
		});
	return workerPromise;
}

function getWorker() {
	return workerPromise ?? createWorker();
}

let tail = Promise.resolve();

export function parse(content, flags, { signal } = {}) {
	const result = tail.then(async () => {
		if (signal?.aborted) throw signal.reason;

		const worker = await getWorker();
		worker.postMessage({ type: PARSE, content, flags });

		const { result } = await awaitMessage(worker, PARSE, signal).catch((e) => {
			workerPromise = null;
			throw e;
		});
		return result;
	});

	tail = result.catch(() => {});
	return result;
}
