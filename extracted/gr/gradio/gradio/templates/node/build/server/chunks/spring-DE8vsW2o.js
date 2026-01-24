import { n as noop, b as async_mode_flag, l as experimental_async_required, m as ssr_context, o as createContext, p as getAllContexts, g as getContext, q as hasContext, s as setContext, t as run, w as writable, h as state, r as render_effect, i as set, u as deferred, j as get } from './async-Mo2Ia14K.js';
import { q as get_render_context, t as uneval, v as hydratable_serialization_failed, w as lifecycle_function_unavailable, x as getAbortSignal } from './index-D1Ptw7Az.js';

/** @import { Raf } from '#client' */

const now = () => Date.now();

/** @type {Raf} */
const raf = {
	// don't access requestAnimationFrame eagerly outside method
	// this allows basic testing of user code without JSDOM
	// bunder will eval and remove ternary when the user's app is built
	tick: /** @param {any} _ */ (_) => (noop)(),
	now: () => now(),
	tasks: new Set()
};

/** @import { TaskCallback, Task, TaskEntry } from '#client' */

// TODO move this into timing.js where it probably belongs

/**
 * @returns {void}
 */
function run_tasks() {
	// use `raf.now()` instead of the `requestAnimationFrame` callback argument, because
	// otherwise things can get wonky https://github.com/sveltejs/svelte/pull/14541
	const now = raf.now();

	raf.tasks.forEach((task) => {
		if (!task.c(now)) {
			raf.tasks.delete(task);
			task.f();
		}
	});

	if (raf.tasks.size !== 0) {
		raf.tick(run_tasks);
	}
}

/**
 * Creates a new task that runs on each raf frame
 * until it returns a falsy value or is aborted
 * @param {TaskCallback} callback
 * @returns {Task}
 */
function loop(callback) {
	/** @type {TaskEntry} */
	let task;

	if (raf.tasks.size === 0) {
		raf.tick(run_tasks);
	}

	return {
		promise: new Promise((fulfill) => {
			raf.tasks.add((task = { c: callback, f: fulfill }));
		}),
		abort() {
			raf.tasks.delete(task);
		}
	};
}

/** @import { HydratableLookupEntry } from '#server' */

/**
 * @template T
 * @param {string} key
 * @param {() => T} fn
 * @returns {T}
 */
function hydratable(key, fn) {
	if (!async_mode_flag) {
		experimental_async_required();
	}

	const { hydratable } = get_render_context();

	let entry = hydratable.lookup.get(key);

	if (entry !== undefined) {

		return /** @type {T} */ (entry.value);
	}

	const value = fn();

	entry = encode(key, value, hydratable.unresolved_promises);
	hydratable.lookup.set(key, entry);

	return value;
}

/**
 * @param {string} key
 * @param {any} value
 * @param {Map<Promise<any>, string>} [unresolved]
 */
function encode(key, value, unresolved) {
	/** @type {HydratableLookupEntry} */
	const entry = { value, serialized: '' };

	let uid = 1;

	entry.serialized = uneval(entry.value, (value, uneval) => {
		if (is_promise(value)) {
			// we serialize promises as `"${i}"`, because it's impossible for that string
			// to occur 'naturally' (since the quote marks would have to be escaped)
			// this placeholder is returned synchronously from `uneval`, which includes it in the
			// serialized string. Later (at least one microtask from now), when `p.then` runs, it'll
			// be replaced.
			const placeholder = `"${uid++}"`;
			const p = value
				.then((v) => {
					entry.serialized = entry.serialized.replace(placeholder, `r(${uneval(v)})`);
				})
				.catch((devalue_error) =>
					hydratable_serialization_failed(
						key,
						serialization_stack(entry.stack, devalue_error?.stack)
					)
				);

			unresolved?.set(p, key);
			// prevent unhandled rejections from crashing the server, track which promises are still resolving when render is complete
			p.catch(() => {}).finally(() => unresolved?.delete(p));

			(entry.promises ??= []).push(p);
			return placeholder;
		}
	});

	return entry;
}

/**
 * @param {any} value
 * @returns {value is Promise<any>}
 */
function is_promise(value) {
	// we use this check rather than `instanceof Promise`
	// because it works cross-realm
	return Object.prototype.toString.call(value) === '[object Promise]';
}

/**
 * @param {string | undefined} root_stack
 * @param {string | undefined} uneval_stack
 */
function serialization_stack(root_stack, uneval_stack) {
	let out = '';
	if (root_stack) {
		out += root_stack + '\n';
	}
	if (uneval_stack) {
		out += 'Caused by:\n' + uneval_stack + '\n';
	}
	return out || '<missing stack trace>';
}

/** @import { Snippet } from 'svelte' */
/** @import { Renderer } from '../renderer' */
/** @import { Getters } from '#shared' */

/**
 * Create a snippet programmatically
 * @template {unknown[]} Params
 * @param {(...params: Getters<Params>) => {
 *   render: () => string
 *   setup?: (element: Element) => void | (() => void)
 * }} fn
 * @returns {Snippet<Params>}
 */
function createRawSnippet(fn) {
	// @ts-expect-error the types are a lie
	return (/** @type {Renderer} */ renderer, /** @type {Params} */ ...args) => {
		var getters = /** @type {Getters<Params>} */ (args.map((value) => () => value));
		renderer.push(
			fn(...getters)
				.render()
				.trim()
		);
	};
}

/** @import { SSRContext } from '#server' */
/** @import { Renderer } from './internal/server/renderer.js' */

/** @param {() => void} fn */
function onDestroy(fn) {
	/** @type {Renderer} */ (/** @type {SSRContext} */ (ssr_context).r).on_destroy(fn);
}

function createEventDispatcher() {
	return noop;
}

function mount() {
	lifecycle_function_unavailable('mount');
}

function hydrate() {
	lifecycle_function_unavailable('hydrate');
}

function unmount() {
	lifecycle_function_unavailable('unmount');
}

function fork() {
	lifecycle_function_unavailable('fork');
}

async function tick() {}

async function settled() {}

var o = /*#__PURE__*/Object.freeze({
	__proto__: null,
	afterUpdate: noop,
	beforeUpdate: noop,
	createContext: createContext,
	createEventDispatcher: createEventDispatcher,
	createRawSnippet: createRawSnippet,
	flushSync: noop,
	fork: fork,
	getAbortSignal: getAbortSignal,
	getAllContexts: getAllContexts,
	getContext: getContext,
	hasContext: hasContext,
	hydratable: hydratable,
	hydrate: hydrate,
	mount: mount,
	onDestroy: onDestroy,
	onMount: noop,
	setContext: setContext,
	settled: settled,
	tick: tick,
	unmount: unmount,
	untrack: run
});

/**
 * @param {any} obj
 * @returns {obj is Date}
 */
function is_date(obj) {
	return Object.prototype.toString.call(obj) === '[object Date]';
}

/** @import { Task } from '#client' */
/** @import { SpringOpts, SpringUpdateOpts, TickContext } from './private.js' */
/** @import { Spring as SpringStore } from './public.js' */

/**
 * @template T
 * @param {TickContext} ctx
 * @param {T} last_value
 * @param {T} current_value
 * @param {T} target_value
 * @returns {T}
 */
function tick_spring(ctx, last_value, current_value, target_value) {
	if (typeof current_value === 'number' || is_date(current_value)) {
		// @ts-ignore
		const delta = target_value - current_value;
		// @ts-ignore
		const velocity = (current_value - last_value) / (ctx.dt || 1 / 60); // guard div by 0
		const spring = ctx.opts.stiffness * delta;
		const damper = ctx.opts.damping * velocity;
		const acceleration = (spring - damper) * ctx.inv_mass;
		const d = (velocity + acceleration) * ctx.dt;
		if (Math.abs(d) < ctx.opts.precision && Math.abs(delta) < ctx.opts.precision) {
			return target_value; // settled
		} else {
			ctx.settled = false; // signal loop to keep ticking
			// @ts-ignore
			return is_date(current_value) ? new Date(current_value.getTime() + d) : current_value + d;
		}
	} else if (Array.isArray(current_value)) {
		// @ts-ignore
		return current_value.map((_, i) =>
			// @ts-ignore
			tick_spring(ctx, last_value[i], current_value[i], target_value[i])
		);
	} else if (typeof current_value === 'object') {
		const next_value = {};
		for (const k in current_value) {
			// @ts-ignore
			next_value[k] = tick_spring(ctx, last_value[k], current_value[k], target_value[k]);
		}
		// @ts-ignore
		return next_value;
	} else {
		throw new Error(`Cannot spring ${typeof current_value} values`);
	}
}

/**
 * The spring function in Svelte creates a store whose value is animated, with a motion that simulates the behavior of a spring. This means when the value changes, instead of transitioning at a steady rate, it "bounces" like a spring would, depending on the physics parameters provided. This adds a level of realism to the transitions and can enhance the user experience.
 *
 * @deprecated Use [`Spring`](https://svelte.dev/docs/svelte/svelte-motion#Spring) instead
 * @template [T=any]
 * @param {T} [value]
 * @param {SpringOpts} [opts]
 * @returns {SpringStore<T>}
 */
function spring(value, opts = {}) {
	const store = writable(value);
	const { stiffness = 0.15, damping = 0.8, precision = 0.01 } = opts;
	/** @type {number} */
	let last_time;
	/** @type {Task | null} */
	let task;
	/** @type {object} */
	let current_token;

	let last_value = /** @type {T} */ (value);
	let target_value = /** @type {T | undefined} */ (value);

	let inv_mass = 1;
	let inv_mass_recovery_rate = 0;
	let cancel_task = false;
	/**
	 * @param {T} new_value
	 * @param {SpringUpdateOpts} opts
	 * @returns {Promise<void>}
	 */
	function set(new_value, opts = {}) {
		target_value = new_value;
		const token = (current_token = {});
		if (value == null || opts.hard || (spring.stiffness >= 1 && spring.damping >= 1)) {
			cancel_task = true; // cancel any running animation
			last_time = raf.now();
			last_value = new_value;
			store.set((value = target_value));
			return Promise.resolve();
		} else if (opts.soft) {
			const rate = opts.soft === true ? 0.5 : +opts.soft;
			inv_mass_recovery_rate = 1 / (rate * 60);
			inv_mass = 0; // infinite mass, unaffected by spring forces
		}
		if (!task) {
			last_time = raf.now();
			cancel_task = false;
			task = loop((now) => {
				if (cancel_task) {
					cancel_task = false;
					task = null;
					return false;
				}
				inv_mass = Math.min(inv_mass + inv_mass_recovery_rate, 1);

				// clamp elapsed time to 1/30th of a second, so that longer pauses
				// (blocked thread or inactive tab) don't cause the spring to go haywire
				const elapsed = Math.min(now - last_time, 1000 / 30);

				/** @type {TickContext} */
				const ctx = {
					inv_mass,
					opts: spring,
					settled: true,
					dt: (elapsed * 60) / 1000
				};
				// @ts-ignore
				const next_value = tick_spring(ctx, last_value, value, target_value);
				last_time = now;
				last_value = /** @type {T} */ (value);
				store.set((value = /** @type {T} */ (next_value)));
				if (ctx.settled) {
					task = null;
				}
				return !ctx.settled;
			});
		}
		return new Promise((fulfil) => {
			/** @type {Task} */ (task).promise.then(() => {
				if (token === current_token) fulfil();
			});
		});
	}
	/** @type {SpringStore<T>} */
	// @ts-expect-error - class-only properties are missing
	const spring = {
		set,
		update: (fn, opts) => set(fn(/** @type {T} */ (target_value), /** @type {T} */ (value)), opts),
		subscribe: store.subscribe,
		stiffness,
		damping,
		precision
	};
	return spring;
}

/**
 * A wrapper for a value that behaves in a spring-like fashion. Changes to `spring.target` will cause `spring.current` to
 * move towards it over time, taking account of the `spring.stiffness` and `spring.damping` parameters.
 *
 * ```svelte
 * <script>
 * 	import { Spring } from 'svelte/motion';
 *
 * 	const spring = new Spring(0);
 * </script>
 *
 * <input type="range" bind:value={spring.target} />
 * <input type="range" bind:value={spring.current} disabled />
 * ```
 * @template T
 * @since 5.8.0
 */
class Spring {
	#stiffness = state(0.15);
	#damping = state(0.8);
	#precision = state(0.01);

	#current;
	#target;

	#last_value = /** @type {T} */ (undefined);
	#last_time = 0;

	#inverse_mass = 1;
	#momentum = 0;

	/** @type {import('../internal/client/types').Task | null} */
	#task = null;

	/** @type {ReturnType<typeof deferred> | null} */
	#deferred = null;

	/**
	 * @param {T} value
	 * @param {SpringOpts} [options]
	 */
	constructor(value, options = {}) {
		this.#current = state(value);
		this.#target = state(value);

		if (typeof options.stiffness === 'number') this.#stiffness.v = clamp(options.stiffness, 0, 1);
		if (typeof options.damping === 'number') this.#damping.v = clamp(options.damping, 0, 1);
		if (typeof options.precision === 'number') this.#precision.v = options.precision;
	}

	/**
	 * Create a spring whose value is bound to the return value of `fn`. This must be called
	 * inside an effect root (for example, during component initialisation).
	 *
	 * ```svelte
	 * <script>
	 * 	import { Spring } from 'svelte/motion';
	 *
	 * 	let { number } = $props();
	 *
	 * 	const spring = Spring.of(() => number);
	 * </script>
	 * ```
	 * @template U
	 * @param {() => U} fn
	 * @param {SpringOpts} [options]
	 */
	static of(fn, options) {
		const spring = new Spring(fn(), options);

		render_effect(() => {
			spring.set(fn());
		});

		return spring;
	}

	/** @param {T} value */
	#update(value) {
		set(this.#target, value);

		this.#current.v ??= value;
		this.#last_value ??= this.#current.v;

		if (!this.#task) {
			this.#last_time = raf.now();

			var inv_mass_recovery_rate = 1000 / (this.#momentum * 60);

			this.#task ??= loop((now) => {
				this.#inverse_mass = Math.min(this.#inverse_mass + inv_mass_recovery_rate, 1);

				// clamp elapsed time to 1/30th of a second, so that longer pauses
				// (blocked thread or inactive tab) don't cause the spring to go haywire
				const elapsed = Math.min(now - this.#last_time, 1000 / 30);

				/** @type {import('./private').TickContext} */
				const ctx = {
					inv_mass: this.#inverse_mass,
					opts: {
						stiffness: this.#stiffness.v,
						damping: this.#damping.v,
						precision: this.#precision.v
					},
					settled: true,
					dt: (elapsed * 60) / 1000
				};

				var next = tick_spring(ctx, this.#last_value, this.#current.v, this.#target.v);
				this.#last_value = this.#current.v;
				this.#last_time = now;
				set(this.#current, next);

				if (ctx.settled) {
					this.#task = null;
				}

				return !ctx.settled;
			});
		}

		return this.#task.promise;
	}

	/**
	 * Sets `spring.target` to `value` and returns a `Promise` that resolves if and when `spring.current` catches up to it.
	 *
	 * If `options.instant` is `true`, `spring.current` immediately matches `spring.target`.
	 *
	 * If `options.preserveMomentum` is provided, the spring will continue on its current trajectory for
	 * the specified number of milliseconds. This is useful for things like 'fling' gestures.
	 *
	 * @param {T} value
	 * @param {SpringUpdateOpts} [options]
	 */
	set(value, options) {
		this.#deferred?.reject(new Error('Aborted'));

		if (options?.instant || this.#current.v === undefined) {
			this.#task?.abort();
			this.#task = null;
			set(this.#current, set(this.#target, value));
			this.#last_value = value;
			return Promise.resolve();
		}

		if (options?.preserveMomentum) {
			this.#inverse_mass = 0;
			this.#momentum = options.preserveMomentum;
		}

		var d = (this.#deferred = deferred());
		d.promise.catch(noop);

		this.#update(value).then(() => {
			if (d !== this.#deferred) return;
			d.resolve(undefined);
		});

		return d.promise;
	}

	get current() {
		return get(this.#current);
	}

	get damping() {
		return get(this.#damping);
	}

	set damping(v) {
		set(this.#damping, clamp(v, 0, 1));
	}

	get precision() {
		return get(this.#precision);
	}

	set precision(v) {
		set(this.#precision, v);
	}

	get stiffness() {
		return get(this.#stiffness);
	}

	set stiffness(v) {
		set(this.#stiffness, clamp(v, 0, 1));
	}

	get target() {
		return get(this.#target);
	}

	set target(v) {
		this.set(v);
	}
}

/**
 * @param {number} n
 * @param {number} min
 * @param {number} max
 */
function clamp(n, min, max) {
	return Math.max(min, Math.min(max, n));
}

export { Spring as S, o as a, createEventDispatcher as c, is_date as i, loop as l, onDestroy as o, raf as r, spring as s, tick as t };
//# sourceMappingURL=spring-DE8vsW2o.js.map
