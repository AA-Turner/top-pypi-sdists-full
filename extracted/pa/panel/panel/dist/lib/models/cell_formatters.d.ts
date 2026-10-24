export type CellFormatterSpec = {
    type: string;
    [key: string]: any;
};
export type CellFormatterFn = (value: any, data: {
    [key: string]: any;
}) => string | HTMLElement;
export declare function cell_formatter(spec: CellFormatterSpec): CellFormatterFn | null;
//# sourceMappingURL=cell_formatters.d.ts.map