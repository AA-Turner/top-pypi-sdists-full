import { ReactElement } from "react";
interface IInitModalInfo {
    total: number;
    curIndex: number;
    title: string;
}
export interface INotification {
    title: string;
    message: string | ReactElement;
    type: "success" | "error" | "info" | "warning";
}
declare class CommonStore {
    _notifyTimeoutFunc: NodeJS.Timeout;
    initModalOpen: boolean;
    initModalInfo: IInitModalInfo;
    showCloudTool: boolean;
    version: string;
    notification: INotification | null;
    uploadSpecModalOpen: boolean;
    uploadChartModalOpen: boolean;
    isStreamlitComponent: boolean;
    setInitModalOpen(value: boolean): void;
    setInitModalInfo(info: IInitModalInfo): void;
    setShowCloudTool(value: boolean): void;
    setVersion(value: string): void;
    setNotification(value: INotification | null, timeout?: number): void;
    setUploadSpecModalOpen(value: boolean): void;
    setUploadChartModalOpen(value: boolean): void;
    setIsStreamlitComponent(value: boolean): void;
    constructor();
}
declare const commonStore: CommonStore;
export default commonStore;
