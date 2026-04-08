import { DOMWidgetView, DOMWidgetModel } from "@jupyter-widgets/base";
import * as ndarray from "ndarray";
export declare class TableWidgetModel extends DOMWidgetModel {
    defaults(): {
        _model_name: string;
        _view_name: null;
        _model_module: string;
        _view_module: null;
        _model_module_version: any;
        _view_module_version: string;
        _table: ndarray.NdArray<never[]>;
        _columns: never[];
    };
    static serializers: {
        _table: {
            deserialize: typeof import("./serializers").JSONToTable;
            serialize: typeof import("./serializers").tableToJSON;
        };
    };
}
export declare class EchoTableWidgetModel extends DOMWidgetModel {
    defaults(): {
        _model_name: string;
        _view_name: string;
        _model_module: string;
        _view_module: string;
        _model_module_version: any;
        _view_module_version: any;
        data: never[];
        echo: never[];
    };
    static serializers: {
        data: {
            deserialize: any;
        };
    };
}
export declare class EchoTableWidgetView extends DOMWidgetView {
    render(): Promise<void>;
}
