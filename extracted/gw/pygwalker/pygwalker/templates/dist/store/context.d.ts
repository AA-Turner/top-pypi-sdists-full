export declare const portalContainerContext: import("react").Context<HTMLDivElement | null>;
export declare const darkModeContext: import("react").Context<"light" | "dark">;
export declare const AppContext: (props: {
    children?: React.ReactNode | Iterable<React.ReactNode>;
} & {
    portalContainerContext: HTMLDivElement | null;
    darkModeContext: "light" | "dark";
}) => JSX.Element;
