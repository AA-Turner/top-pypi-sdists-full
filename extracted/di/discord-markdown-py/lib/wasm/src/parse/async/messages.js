export const INIT = "INIT";
export const PARSE = "PARSE";

export function awaitMessage(worker, type, signal) {
	return new Promise((resolve, reject) => {
		function handleMessage(event) {
			if (event.data.type === type) {
				resolve(event.data);
				cleanupListeners();
			}
		}

		function handleError(event) {
			reject(new Error(event.data));
			cleanupListeners();
		}

		function handleAbort() {
			reject(new Error("aborted"));
			cleanupListeners();
		}

		function cleanupListeners() {
			worker.removeEventListener("message", handleMessage);
			worker.removeEventListener("error", handleError);
			signal?.removeEventListener("abort", handleAbort);
		}

		worker.addEventListener("message", handleMessage);
		worker.addEventListener("error", handleError);
		signal?.addEventListener("abort", handleAbort);
	});
}
