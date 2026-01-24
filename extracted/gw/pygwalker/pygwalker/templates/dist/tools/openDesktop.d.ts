import React from "react";
import type { ToolbarButtonItem } from "@kanaries/graphic-walker/components/toolbar/toolbar-button";
import { IAppProps } from "@/interfaces";
import { VizSpecStore } from "@kanaries/graphic-walker";
export declare function getOpenDesktopTool(props: IAppProps, storeRef: React.MutableRefObject<VizSpecStore | null>): ToolbarButtonItem;
