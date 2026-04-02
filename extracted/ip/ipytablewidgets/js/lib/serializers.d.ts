import ndarray = require('ndarray');
type NdArray = ndarray.NdArray;
import { WidgetModel, ManagerBase } from '@jupyter-widgets/base';
export interface IReceivedSerializedArray {
    shape: number[];
    dtype: "bool" | "int8" | "int16" | "int32" | "uint8" | "uint16" | "uint32" | "float32" | "float64" | "str";
    buffer: DataView | string[];
    compression?: string;
}
export interface IDict<T> {
    [Key: string]: T;
}
/**
 * The serialized representation of a received Table (i.e. dataframe)
 */
export interface IReceivedSerializedTable {
    columns: string[];
    data: IDict<IReceivedSerializedArray>;
}
export interface ISendSerializedTable {
    columns: string[];
    data: IDict<NdArray | string[]>;
    size: number;
}
export declare function JSONToTable(obj: IReceivedSerializedTable | null, manager?: ManagerBase<any>): ISendSerializedTable | null;
export declare function rowProxy(table: ISendSerializedTable | null): any;
export declare function tableToJSON(obj: IDict<NdArray> | null, widget?: WidgetModel): ISendSerializedTable | null;
/**
 * Serializers for to/from tables/dataframes
 */
export declare const table_serialization: {
    deserialize: typeof JSONToTable;
    serialize: typeof tableToJSON;
};
export {};
