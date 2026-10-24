import type * as p from "@bokehjs/core/properties";
import { Markup } from "@bokehjs/models/widgets/markup";
import { PanelMarkupView } from "./layout";
import type { ResourceSpec } from "./resources";
export declare class KaTeXView extends PanelMarkupView {
    model: KaTeX;
    connect_signals(): void;
    render(): void;
}
export declare namespace KaTeX {
    type Attrs = p.AttrsOf<Props>;
    type Props = Markup.Props & {
        text: p.Property<string>;
        external_resources: p.Property<ResourceSpec | null>;
    };
}
export interface KaTeX extends KaTeX.Attrs {
}
export declare class KaTeX extends Markup {
    properties: KaTeX.Props;
    constructor(attrs?: Partial<KaTeX.Attrs>);
    static __module__: string;
    initialize(): void;
}
//# sourceMappingURL=katex.d.ts.map