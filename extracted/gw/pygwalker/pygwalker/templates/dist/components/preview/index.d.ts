import React from "react";
import { IRow } from '@kanaries/graphic-walker';
import type { IDarkMode } from '@kanaries/graphic-walker/interfaces';
interface IPreviewProps {
    gid: string;
    themeKey: string;
    dark: IDarkMode;
    charts: {
        visSpec: any;
        data: IRow[];
    }[];
}
declare const Preview: React.FC<IPreviewProps>;
interface IChartPreviewProps {
    themeKey: string;
    dark: IDarkMode;
    visSpec: any;
    data: IRow[];
    title: string;
    desc: string;
}
declare const ChartPreview: React.FC<IChartPreviewProps>;
export { Preview, ChartPreview, };
export type { IPreviewProps, IChartPreviewProps };
