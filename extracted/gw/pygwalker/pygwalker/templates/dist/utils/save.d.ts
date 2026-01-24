import type { IChartExportResult } from '@kanaries/graphic-walker/interfaces';
export declare function download(data: string, filename: string, type: string): void;
export declare function formatExportedChartDatas(chartData: IChartExportResult): Promise<{
    singleChart: string;
    mode: "svg" | "data-url";
    title: string;
    nCols: number;
    nRows: number;
    charts: {
        colIndex: number;
        rowIndex: number;
        width: number;
        height: number;
        canvasWidth: number;
        canvasHeight: number;
        data: string;
        canvas(): HTMLCanvasElement | SVGSVGElement | null;
    }[];
    container(): HTMLDivElement | null;
    chartType?: string;
}>;
export declare function getTimezoneOffsetSeconds(): number;
