import { ActionTool, ActionToolView } from "@bokehjs/models/tools/actions/action_tool";
import { ColumnDataSource } from "@bokehjs/models/sources/column_data_source";
import { tool_icon_reset } from "@bokehjs/styles/icons.css";
export class ClearToolView extends ActionToolView {
    static __name__ = "ClearToolView";
    doit() {
        for (const source of this.model.sources) {
            source.clear();
        }
    }
}
export class ClearTool extends ActionTool {
    static __name__ = "ClearTool";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "geoviews.models.custom_tools";
    static {
        this.prototype.default_view = ClearToolView;
        this.define(({ List, Ref }) => ({
            sources: [List(Ref(ColumnDataSource)), []],
        }));
    }
    tool_name = "Clear data";
    tool_icon = tool_icon_reset;
}
//# sourceMappingURL=clear_tool.js.map