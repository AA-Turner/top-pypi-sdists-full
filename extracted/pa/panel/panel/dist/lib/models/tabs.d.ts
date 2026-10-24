import type * as p from "@bokehjs/core/properties";
import { Tabs as BkTabs, TabsView as BkTabsView } from "@bokehjs/models/layouts/tabs";
import type { UIElementView } from "@bokehjs/models/ui/ui_element";
export declare class TabsView extends BkTabsView {
    model: Tabs;
    connect_signals(): void;
    update_active(): void;
    protected _active_child_view(): UIElementView | undefined;
    protected _update_child_visibility(): void;
    get is_visible(): boolean;
    render(): void;
    update_zindex(): void;
    _after_layout(): void;
    _update_layout(): void;
}
export declare namespace Tabs {
    type Attrs = p.AttrsOf<Props>;
    type Props = BkTabs.Props;
}
export interface Tabs extends BkTabs.Attrs {
}
export declare class Tabs extends BkTabs {
    properties: Tabs.Props;
    static __module__: string;
}
//# sourceMappingURL=tabs.d.ts.map