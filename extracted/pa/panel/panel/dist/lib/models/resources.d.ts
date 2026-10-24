/**
 * Client-side registry for external component resources.
 *
 * Both the eager path (`pn.extension`, which renders its script and link
 * tags into the page and then calls `declare`) and the lazy path (a model
 * carrying an `external_resources` spec, which calls `ensure`) write to one
 * registry, so a library is fetched at most once per page no matter how
 * many components, documents or Panel versions ask for it.
 *
 * The registry is installed on `globalThis.__panel_resources__`, outside any
 * version-namespaced object, so two Panel versions sharing a JupyterLab page
 * share it as well. Its shape is therefore a cross-version contract: it
 * carries a `v` field and must stay minimal and backwards compatible.
 */
export declare const REGISTRY_VERSION = 1;
export declare const DEFAULT_TIMEOUT = 15000;
export type Probe = {
    global?: string;
    custom_element?: string;
};
export type ModuleSpec = {
    url: string;
    export?: string;
};
export type LibSpec = {
    name: string;
    js?: string[];
    modules?: ModuleSpec[];
    probe?: Probe;
};
export type ResourceSpec = {
    v: number;
    libs?: LibSpec[];
    css?: string[];
    shim?: string;
    timeout?: number;
    inline_fallback?: boolean;
};
/**
 * Maps a Jupyter extension endpoint url to its CDN equivalent, using the
 * map of endpoint paths to CDN urls the notebook bootstrap publishes
 * (Panel's dist, every extension with a CDN and each BokehJS file). Null
 * if the url is not served by the endpoint or has no CDN equivalent, e.g.
 * in server/served-app contexts, where the bootstrap never runs.
 */
export declare function cdn_url(url: string): string | null;
/**
 * Loads endpoint urls from the CDN where the endpoint cannot serve them:
 * in an exported notebook, or once the bootstrap found the endpoint
 * unreachable.
 */
export declare function resource_url(url: string): string;
export declare class ResourceRegistry {
    readonly v: number;
    /** lib name -> promise resolving once the library is usable */
    readonly libs: Map<string, Promise<void>>;
    /** absolute url -> promise resolving once the url has loaded */
    readonly urls: Map<string, Promise<void>>;
    /** module url -> promise resolving to the module namespace */
    readonly modules: Map<string, Promise<any>>;
    /** lib name -> last seen spec, for `libs` entries given by name only */
    readonly specs: Map<string, LibSpec>;
    /** export name -> resolved module handle */
    readonly exports: Map<string, any>;
    protected _shim: Promise<void> | null;
    /**
     * Records resources that are already on the page, without fetching.
     *
     * Called by the eager path so that "pn.extension already handled it"
     * is a fact rather than an inference. It is the only thing that can
     * get this right for `inline` resources, where the libraries were
     * inlined and there are no urls to compare against.
     */
    declare(declared: LibSpec[] | {
        libs?: LibSpec[];
        css?: string[];
    }): void;
    /**
     * Records that a loader outside the registry (RequireJS, in the classic
     * notebook) is already fetching these libraries. Unlike `declare`, this
     * does not mark them ready immediately: `await_resources` waits on
     * `ready` instead, so a view doesn't read an unassigned global.
     */
    claim(declared: {
        libs?: LibSpec[];
    }, ready: Promise<void>): void;
    /**
     * Whether a library is already available without loading anything.
     *
     * Probes are hints derived from `__js_skip__` and are known to be wrong
     * in places, which is tolerable: the url checks below are what make
     * this correct, a wrong probe only costs a redundant script tag for an
     * already cached file.
     */
    loaded(lib: LibSpec, scripts?: Set<string>): boolean;
    /**
     * Loads everything a resource spec declares, skipping what is present.
     */
    ensure(spec: ResourceSpec | null | undefined): Promise<void>;
    /**
     * Injects stylesheets, matching what pn.extension puts in the head.
     *
     * A stylesheet that never arrives must not keep a component from
     * rendering, so failures are reported and then ignored.
     */
    ensure_css(urls: string[]): Promise<void>;
    /**
     * Ensures es-module-shims is available, in shim mode.
     *
     * Shim mode cannot be enabled after es-module-shims has loaded, so the
     * options marker has to be written before the script is injected. Shim
     * mode is what makes `importShim.addImportMap` available, which the ESM
     * component machinery depends on.
     */
    ensure_shim(url?: string): Promise<void>;
    /**
     * Imports an ES module through es-module-shims, memoized by url.
     */
    import_module(url: string, shim?: string): Promise<any>;
    add_import_map(map: any): void;
    protected _load(js: string[], modules: ModuleSpec[], elements?: string[]): Promise<void>;
    protected _load_scripts(urls: string[]): Promise<void>;
    protected _load_modules(modules: ModuleSpec[]): Promise<void>;
}
export declare const resources: ResourceRegistry;
export interface ExternalResourcesModel {
    external_resources: ResourceSpec | null;
}
/**
 * Bokeh property declaration for models that carry a resource spec.
 *
 * The resource bearing models do not share a single base (`HTMLBox`
 * covers most of them, but `KaTeX` derives from `Markup`, `FileDropper`
 * from `InputWidget` and so on) and TypeScript has no multiple
 * inheritance, so the declaration is applied per class instead.
 */
export declare function define_external_resources(cls: any): void;
/**
 * Starts loading a model's resources.
 *
 * Called from the model's `initialize`, which runs for every model in a
 * document before the first view is built. `build_views` constructs views
 * sequentially, so starting here is what keeps the total wait at roughly
 * the slowest library rather than the sum of all of them.
 */
export declare function load_resources(model: ExternalResourcesModel): void;
/**
 * Awaits a model's resources, resolving to the error if loading failed.
 *
 * Never rejects: an exception out of `lazy_initialize` aborts the whole
 * `build_views` walk and would take unrelated components down with it.
 */
export declare function await_resources(model: ExternalResourcesModel): Promise<Error | null>;
/**
 * Replaces a view's rendering with an error state.
 *
 * `base` (the view baseclass' own render) still runs, so the element keeps
 * its sizing and stylesheets, but the subclass render is skipped entirely.
 * That is the point: its code reads globals the library that failed to load
 * never defined, and letting it throw out of `render` takes the surrounding
 * layout down with it. Installing the override on the instance is what makes
 * it win over the subclass method on the prototype chain.
 */
export declare function render_resource_error(view: any, error: Error, base: () => void): void;
//# sourceMappingURL=resources.d.ts.map