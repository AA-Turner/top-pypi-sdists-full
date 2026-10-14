import type { HasProps } from "./has_props";
import type { View, ViewOf } from "./view";
import type { ViewManager } from "./view_manager";
export type { IterViews, ViewOf, View, ChildView } from "./view";
export type ViewStorage<T extends HasProps> = Map<T, ViewOf<T>>;
export type Options<T extends View> = {
    parent: T["parent"] | null | ((obj: HasProps) => T["parent"] | null);
    owner?: ViewManager;
};
export declare function build_view<T extends HasProps>(model: T, options?: Options<ViewOf<T>>, cls?: (model: T) => T["default_view"]): Promise<ViewOf<T>>;
export type BuildResult<T extends HasProps> = {
    created: ViewOf<T>[];
    removed: ViewOf<T>[];
};
/**
 * Builds views for `models` into `view_storage` and removes views of models
 * that aren't wanted any more.
 *
 * Overlapping calls on the same `view_storage` cooperate: a model is built at
 * most once, by whichever call got to it first, and a call wanting a model
 * somebody else is already building waits for that build instead of starting a
 * second one. So once this resolves, every requested model that is still wanted
 * has a connected view in `view_storage`.
 *
 * Models are processed in request order, waiting included, so a view is never
 * initialized ahead of a view requested before it.
 *
 * A build belongs to the model, not to the call that started it, and never
 * waits on a call, so waiting can't cycle and a failing model doesn't poison
 * unrelated models: whatever is still wanted can be built by a later call. The
 * one thing this can't support is a view whose (lazy) initialization asks the
 * same `view_storage` for its own model, which would wait for itself.
 */
export declare function build_views<T extends HasProps>(view_storage: ViewStorage<T>, models: T[], options?: Options<ViewOf<T>>, cls?: (model: T) => T["default_view"]): Promise<BuildResult<T>>;
export declare function remove_views(view_storage: ViewStorage<HasProps>): void;
export declare function traverse_views(views: View[], fn: (view: View) => void): void;
//# sourceMappingURL=build_views.d.ts.map