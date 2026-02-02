import { entries } from "@bokehjs/core/util/object";
import { copy } from "@bokehjs/core/util/array";
import { ActionTool, ActionToolView } from "@bokehjs/models/tools/actions/action_tool";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
import { tool_icon_save } from "@bokehjs/styles/icons.css";
export class CheckpointToolView extends ActionToolView {
    static __name__ = "CheckpointToolView";
    doit() {
        const sources = this.model.sources;
        for (const source of sources) {
            if (source.buffer == null) {
                source.buffer = [];
            }
            const data_copy = {};
            for (const [key, column] of entries(source.data)) {
                const new_column = [];
                for (const arr of column) {
                    if (Array.isArray(arr) || ArrayBuffer.isView(arr)) {
                        new_column.push(copy(arr));
                    }
                    else {
                        new_column.push(arr);
                    }
                }
                data_copy[key] = new_column;
            }
            source.buffer.push(data_copy);
        }
    }
}
export class CheckpointTool extends ActionTool {
    static __name__ = "CheckpointTool";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "geoviews.models.custom_tools";
    static {
        this.prototype.default_view = CheckpointToolView;
        this.define(({ List, Ref }) => ({
            sources: [List(Ref(ColumnDataSource)), []],
        }));
    }
    tool_name = "Checkpoint";
    tool_icon = tool_icon_save;
}
//# sourceMappingURL=checkpoint_tool.js.map