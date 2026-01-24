import { DOMWidgetView, DOMWidgetModel } from "@jupyter-widgets/base";
export declare class TableWidgetModel extends DOMWidgetModel {
    defaults(): any;
    static serializers: {
        _table: {
            deserialize: typeof import("./serializers").JSONToTable;
            serialize: typeof import("./serializers").tableToJSON;
        };
    };
}
export declare class EchoTableWidgetModel extends DOMWidgetModel {
    defaults(): any;
    static serializers: {
        data: {
            deserialize: any;
        };
    };
}
export declare class EchoTableWidgetView extends DOMWidgetView {
    render(): Promise<void>;
}
