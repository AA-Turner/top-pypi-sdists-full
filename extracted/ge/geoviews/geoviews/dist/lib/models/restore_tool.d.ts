import type * as p from "@bokehjs/core/properties";
import { ActionTool, ActionToolView } from "@bokehjs/models/tools/actions/action_tool";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare class RestoreToolView extends ActionToolView {
    model: RestoreTool;
    doit(): void;
}
export declare namespace RestoreTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = ActionTool.Props & {
        sources: p.Property<ColumnDataSource[]>;
    };
}
export interface RestoreTool extends RestoreTool.Attrs {
}
export declare class RestoreTool extends ActionTool {
    properties: RestoreTool.Props;
    constructor(attrs?: Partial<RestoreTool.Attrs>);
    static __module__: string;
    tool_name: string;
    tool_icon: string;
}
//# sourceMappingURL=restore_tool.d.ts.map