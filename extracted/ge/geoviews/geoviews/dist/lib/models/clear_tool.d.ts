import type * as p from "@bokehjs/core/properties";
import { ActionTool, ActionToolView } from "@bokehjs/models/tools/actions/action_tool";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare class ClearToolView extends ActionToolView {
    model: ClearTool;
    doit(): void;
}
export declare namespace ClearTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = ActionTool.Props & {
        sources: p.Property<ColumnDataSource[]>;
    };
}
export interface ClearTool extends ClearTool.Attrs {
}
export declare class ClearTool extends ActionTool {
    properties: ClearTool.Props;
    constructor(attrs?: Partial<ClearTool.Attrs>);
    static __module__: string;
    tool_name: string;
    tool_icon: string;
}
//# sourceMappingURL=clear_tool.d.ts.map