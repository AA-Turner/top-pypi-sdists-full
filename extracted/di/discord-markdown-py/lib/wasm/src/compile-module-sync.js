// The bytes only arrive over a fetch, and even with bytes in hand a browser caps synchronous
// compilation at 4KB on the main thread. Callers have to init ahead of time instead.
export function compileModuleSync() {
	return null;
}
