import { ActionTool, ActionToolView } from "@bokehjs/models/tools/actions/action_tool";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
import { tool_icon_undo } from "@bokehjs/styles/icons.css";
export class RestoreToolView extends ActionToolView {
    static __name__ = "RestoreToolView";
    doit() {
        const sources = this.model.sources;
        for (const source of sources) {
            const new_data = source.buffer?.pop();
            if (new_data == null) {
                continue;
            }
            source.data = new_data;
            source.change.emit();
            source.properties.data.change.emit();
        }
    }
}
export class RestoreTool extends ActionTool {
    static __name__ = "RestoreTool";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "geoviews.models.custom_tools";
    static {
        this.prototype.default_view = RestoreToolView;
        this.define(({ List, Ref }) => ({
            sources: [List(Ref(ColumnDataSource)), []],
        }));
    }
    tool_name = "Restore";
    tool_icon = tool_icon_undo;
}
//# sourceMappingURL=restore_tool.js.map