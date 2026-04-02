import type * as p from "@bokehjs/core/properties";
import { ActionTool, ActionToolView } from "@bokehjs/models/tools/actions/action_tool";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
export declare class CheckpointToolView extends ActionToolView {
    model: CheckpointTool;
    doit(): void;
}
export declare namespace CheckpointTool {
    type Attrs = p.AttrsOf<Props>;
    type Props = ActionTool.Props & {
        sources: p.Property<ColumnDataSource[]>;
    };
}
export interface CheckpointTool extends CheckpointTool.Attrs {
}
export declare class CheckpointTool extends ActionTool {
    properties: CheckpointTool.Props;
    constructor(attrs?: Partial<CheckpointTool.Attrs>);
    static __module__: string;
    tool_name: string;
    tool_icon: string;
}
//# sourceMappingURL=checkpoint_tool.d.ts.map