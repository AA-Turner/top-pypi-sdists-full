"""Auto-generate .capsule/types/ and tsconfig.json for editor DX.

Called by both ``capsule serve`` and ``capsule deploy`` so that React page
authors get type-checking and autocomplete for ``@capsule/page`` hooks,
React itself, and any npm packages declared via ``packages=[...]``.

Produces:
  .capsule/types/capsule-page.d.ts   — @capsule/page hook signatures
  .capsule/types/react.d.ts          — minimal React type declarations
  .capsule/types/packages.d.ts       — stub declarations for npm deps
  .capsule/.gitignore                — keeps generated files out of VCS
  tsconfig.json (project root)       — jsx, paths, module resolution
"""

from __future__ import annotations

import os


def generate_type_stubs(pages: list[dict], npm_packages: list[str] | None = None) -> None:
    has_react = any(p.get("type") == "react" for p in pages)
    if not has_react:
        return

    root = os.getcwd()
    capsule_dir = os.path.join(root, ".capsule")
    types_dir = os.path.join(capsule_dir, "types")
    os.makedirs(types_dir, exist_ok=True)

    _write(os.path.join(types_dir, "capsule-page.d.ts"), _DTS_CAPSULE_PAGE)
    _write(os.path.join(types_dir, "react.d.ts"), _DTS_REACT)

    all_packages: set[str] = set(npm_packages or [])
    for p in pages:
        for pkg in p.get("packages", []):
            at_idx = pkg.rfind("@") if pkg.count("@") > 1 or not pkg.startswith("@") else -1
            name = pkg[:at_idx] if at_idx > 0 else pkg
            all_packages.add(name)
    if all_packages:
        lines = [f'declare module "{pkg}";' for pkg in sorted(all_packages)]
        _write(os.path.join(types_dir, "packages.d.ts"), "\n".join(lines) + "\n")

    gi = os.path.join(capsule_dir, ".gitignore")
    if not os.path.exists(gi):
        _write(gi, "*\n")

    tsconfig_path = os.path.join(root, "tsconfig.json")
    if not os.path.exists(tsconfig_path):
        _write(tsconfig_path, _TSCONFIG)


def _write(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# Template strings
# ---------------------------------------------------------------------------

_DTS_CAPSULE_PAGE = """\
declare module "@capsule/page" {
  import type { ReactNode, CSSProperties, FC } from "react";

  // -----------------------------------------------------------------------
  // Data hooks
  // -----------------------------------------------------------------------

  interface DataResult<T = unknown> {
    data: T | null;
    loading: boolean;
    error: string | null;
    refresh: () => void;
  }

  interface EndpointResult<T = unknown> {
    data: T | null;
    loading: boolean;
    error: string | null;
    call: (body?: unknown) => Promise<T>;
  }

  interface CapsuleContext {
    appId: string;
    user: { email: string } | null;
    pages: CapsulePage[];
    login: () => void;
    navigate: (target: NavigationTarget) => void;
    pageRoute: (target: PageTarget) => string;
    pageHref: (target: PageTarget) => string;
  }

  interface CapsulePage {
    name: string;
    route: string;
    path: string;
    href: string;
    icon: string;
    type: "dsl" | "react";
    access?: "public" | "authenticated";
  }

  type PageTarget = string | { name?: string; page?: string; pageId?: string; route?: string };

  type NavigationTarget =
    | "home"
    | "chat"
    | "api"
    | "docs"
    | "logs"
    | "integrations"
    | "connections"
    | "org"
    | "team"
    | string
    | { kind: "home" }
    | { kind: "chat"; sessionId?: string }
    | { kind: "api" | "docs" | "logs" | "integrations" | "connections" | "org" | "team" }
    | { path: string }
    | { href: string }
    | { kind: "page"; pageId?: string; page?: string; name?: string }
    | { kind: "workflow"; workflowName?: string; workflow?: string; name?: string; sessionId?: string };

  export function useData<T = unknown>(
    name: string,
    opts?: { params?: Record<string, string> },
  ): DataResult<T>;
  export function useEndpoint<T = unknown>(path: string): EndpointResult<T>;

  interface ChatMessage {
    id: string;
    role: "user" | "assistant" | "block";
    text: string;
    ts: number;
    requestId?: string;
    block?: { id: string; type: string; payload: Record<string, unknown> };
    attachments?: unknown[];
  }

  interface ChatState {
    sessionId: string;
    messages: ChatMessage[];
    status: "disabled" | "loading" | "idle" | "sending" | "streaming" | "error";
    connected: boolean;
    error: string | null;
    send: (text: string, opts?: { attachments?: unknown[] }) => Promise<unknown>;
    retry: () => void;
    stop: () => void;
  }

  export function useChat(
    chatName?: string,
    opts?: {
      /** Stable app-defined key for one chat per project, row, object, etc.
       * Passing null disables the hook until a selection exists. */
      threadKey?: string | null;
      sessionId?: string;
      /** Durable creation-time context exposed to the Python session. */
      context?: Record<string, unknown>;
      /** @deprecated Use context. */
      initialData?: Record<string, unknown>;
      /** Named chats default to hidden; default chats default to listed. */
      visibility?: "hidden" | "listed";
      enabled?: boolean;
    },
  ): ChatState;

  interface SessionDataResult<T = unknown> {
    [key: string]: T;
  }

  interface SessionHandle {
    id: string;
    sessionId: string;
    ready: boolean;
    status: "loading" | "ready" | "error";
    error: string | null;
    data<T = unknown>(name: string, initial?: T): T;
    allData<T = Record<string, unknown>>(): T;
    set<T = unknown>(name: string, value: T): Promise<T>;
    publish<T = unknown>(name: string, value: T): Promise<T>;
    action(name: string): ActionState;
    chat(): ChatState;
    integrations(): {
      connect(type: string): Promise<unknown>;
      status(type?: string): Promise<unknown>;
    };
  }

  export function useSession(
    name: string,
    opts?: {
      threadKey?: string;
      initialData?: Record<string, unknown>;
      visibility?: "hidden" | "listed";
      enabled?: boolean;
    },
  ): SessionHandle;

  interface ActionState {
    loading: boolean;
    error: string | null;
    run: (payload?: Record<string, unknown>) => Promise<unknown>;
  }

  export function useAction(
    name: string,
    opts?: { chatName?: string; threadKey?: string },
  ): ActionState;

  export function completeOnboarding(): Promise<void>;
  export function useOnboarding(): {
    complete: () => Promise<void>;
    completing: boolean;
    error: string | null;
  };

  export function useCapsule(): CapsuleContext;
  export function navigate(target: NavigationTarget): void;
  export function useNavigate(): (target: NavigationTarget) => void;
  export function usePages(): CapsulePage[];
  export function pageRoute(target: PageTarget): string;
  export function pageHref(target: PageTarget): string;

  // -----------------------------------------------------------------------
  // Theme
  // -----------------------------------------------------------------------

  interface ThemeColors {
    bg: string;
    fg: string;
    background: string;
    foreground: string;
    muted: string;
    surface: string;
    surfaceHover: string;
    card: string;
    popover: string;
    border: string;
    input: string;
    ring: string;
    primary: string;
    primaryFg: string;
    accent: string;
    accentFg: string;
    accentSubtle: string;
    accentBorder: string;
    sidebar: string;
    sidebarActive: string;
    sidebarFg: string;
    sidebarMuted: string;
    danger: string;
    dangerSubtle: string;
    dangerBorder: string;
    destructive: string;
    success: string;
  }

  interface ThemeRadius {
    sm: string;
    md: string;
    lg: string;
    xl: string;
  }

  interface ThemeFont {
    sans: string;
    mono: string;
  }

  interface Theme {
    mode: "dark" | "light";
    color: ThemeColors;
    radius: ThemeRadius;
    font: ThemeFont;

    /** @deprecated Use color.primary */
    primary: string;
    /** @deprecated Use color.accent */
    accent: string;
    /** @deprecated Use color.background */
    background: string;
    /** @deprecated Use color.foreground */
    foreground: string;
    /** @deprecated Use color.surface */
    surface: string;
    /** @deprecated Use color.border */
    border: string;
    /** @deprecated Use color.muted */
    muted: string;
    /** @deprecated Use color.danger */
    danger: string;
    /** @deprecated Use color.success */
    success: string;
    /** @deprecated Use color.sidebar */
    sidebar: string;
    /** @deprecated Use font.sans */
    font_sans: string;
    /** @deprecated Use font.mono */
    font_mono: string;
  }

  export function useTheme(): Theme;

  // -----------------------------------------------------------------------
  // Helpers
  // -----------------------------------------------------------------------

  /** Apply an alpha channel to a hex color string. */
  export function withAlpha(hex: string, alpha: number): string;

  /** Linearly interpolate between two hex colors. t=0 returns a, t=1 returns b. */
  export function mix(a: string, b: string, t: number): string;

  /** Identity helper — returns the same object with CSSProperties inference. */
  export function css(styles: CSSProperties): CSSProperties;

  /** Build a stable Capsule URL for a file path mounted into the app. */
  export function fileUrl(path: string): string;

  /** React hook variant of fileUrl for render/effect usage. */
  export function useFileUrl(path: string): string;

  // -----------------------------------------------------------------------
  // Collections
  // -----------------------------------------------------------------------

  interface CollectionOpts {
    pageSize?: number;
    sort?: { field: string; dir?: "asc" | "desc" };
    filter?: Record<string, unknown>;
    scope?: "app" | "user" | "owner" | "session";
  }

  interface CollectionColumn {
    key: string;
    type?: "text" | "number" | "currency" | "date" | "link" | "file" | "email" | "status" | "tags" | "boolean";
    label?: string;
    format?: string;
  }

  interface CollectionResult<T = unknown> {
    data: T[];
    total: number;
    columns: (string | CollectionColumn)[];
    page: number;
    totalPages: number;
    loading: boolean;
    error: string | null;
    setPage: (page: number) => void;
    setSort: (field: string, dir?: "asc" | "desc") => void;
    setFilter: (filter: Record<string, unknown>) => void;
    refresh: () => void;
  }

  export function useCollection<T = unknown>(
    name: string,
    opts?: CollectionOpts,
  ): CollectionResult<T>;

  // -----------------------------------------------------------------------
  // Layout primitives
  // -----------------------------------------------------------------------

  interface LayoutRootProps {
    children?: ReactNode;
    style?: CSSProperties;
  }

  interface LayoutSidebarProps {
    width?: number;
    children?: ReactNode;
    style?: CSSProperties;
  }

  interface LayoutListPaneProps {
    width?: number;
    children?: ReactNode;
    style?: CSSProperties;
  }

  interface LayoutDetailProps {
    children?: ReactNode;
    style?: CSSProperties;
  }

  export const Layout: {
    Root: FC<LayoutRootProps>;
    Sidebar: FC<LayoutSidebarProps>;
    ListPane: FC<LayoutListPaneProps>;
    Detail: FC<LayoutDetailProps>;
  };
  export const Shell: FC<LayoutRootProps>;
  export const Pane: {
    Sidebar: FC<LayoutSidebarProps>;
    List: FC<LayoutListPaneProps>;
    Main: FC<LayoutDetailProps>;
    Inspector: FC<LayoutListPaneProps>;
  };
  export const Header: FC<{ title?: ReactNode; subtitle?: ReactNode; action?: ReactNode; children?: ReactNode }>;

  export const Badge: FC<{ children?: ReactNode; tone?: "default" | "success" | "danger" | "accent"; style?: CSSProperties }>;
  export const SectionHeader: FC<{ title: string; subtitle?: string; action?: ReactNode; style?: CSSProperties }>;
  export const Metric: FC<{ label: string; value: ReactNode; hint?: string; style?: CSSProperties }>;
  export const DataTable: FC<{ columns?: (string | CollectionColumn)[]; rows?: Record<string, unknown>[]; style?: CSSProperties }>;
  export const FieldInspector: FC<{ fields?: (string | CollectionColumn | Record<string, unknown>)[]; style?: CSSProperties }>;
  export const MessageList: FC<{ messages?: ChatMessage[]; style?: CSSProperties }>;
  export const Composer: FC<{ value?: string; onChange?: (value: string) => void; onSend?: (text: string) => void; placeholder?: string; disabled?: boolean; style?: CSSProperties }>;
  export const ChatPanel: FC<{ messages?: ChatMessage[]; onSend?: (text: string) => void; status?: string; statusText?: string; style?: CSSProperties }>;
  export const ConversationList: FC<{ items?: Record<string, unknown>[]; activeId?: string; onSelect?: (item: Record<string, unknown>) => void; style?: CSSProperties }>;

  // -----------------------------------------------------------------------
  // UI primitives
  // -----------------------------------------------------------------------

  interface NavItemProps {
    icon?: ReactNode;
    active?: boolean;
    count?: number | string;
    onClick?: () => void;
    children?: ReactNode;
    style?: CSSProperties;
  }
  export const NavItem: FC<NavItemProps>;

  interface ButtonProps {
    variant?: "primary" | "ghost" | "danger";
    size?: "sm" | "md";
    disabled?: boolean;
    onClick?: () => void;
    children?: ReactNode;
    style?: CSSProperties;
  }
  export const Button: FC<ButtonProps>;

  interface CardProps {
    children?: ReactNode;
    style?: CSSProperties;
  }
  export const Card: FC<CardProps>;

  interface RowProps {
    active?: boolean;
    onClick?: () => void;
    children?: ReactNode;
    style?: CSSProperties;
  }
  export const Row: FC<RowProps>;

  interface EmptyStateProps {
    icon?: ReactNode;
    title?: string;
    description?: string;
    action?: ReactNode;
    style?: CSSProperties;
  }
  export const EmptyState: FC<EmptyStateProps>;

  interface SpinnerProps {
    size?: number;
    style?: CSSProperties;
  }
  export const Spinner: FC<SpinnerProps>;

  interface TabItem {
    key: string;
    label: ReactNode;
    count?: ReactNode;
    icon?: ReactNode;
  }
  export const Tabs: FC<{ items: TabItem[]; activeKey: string; onSelect: (key: any) => void; style?: CSSProperties }>;

  interface AvatarProps {
    name: string;
    size?: number;
    style?: CSSProperties;
  }
  export const Avatar: FC<AvatarProps>;

  interface FileLinkProps {
    path: string;
    label?: string;
    target?: string;
    rel?: string;
    children?: ReactNode;
    style?: CSSProperties;
  }
  export const FileLink: FC<FileLinkProps>;

  // -----------------------------------------------------------------------
  // styled-components
  // -----------------------------------------------------------------------

  type StyledTag = {
    <P extends object = {}>(
      strings: TemplateStringsArray,
      ...exprs: Array<string | number | ((p: P & { theme: Theme }) => string | number | undefined)>
    ): FC<P & Record<string, any>>;
  };

  interface StyledInterface {
    (tag: string): StyledTag;
    div: StyledTag;
    span: StyledTag;
    button: StyledTag;
    a: StyledTag;
    p: StyledTag;
    h1: StyledTag;
    h2: StyledTag;
    h3: StyledTag;
    section: StyledTag;
    article: StyledTag;
    nav: StyledTag;
    header: StyledTag;
    footer: StyledTag;
    main: StyledTag;
    input: StyledTag;
    textarea: StyledTag;
    label: StyledTag;
    img: StyledTag;
    ul: StyledTag;
    li: StyledTag;
  }

  export const styled: StyledInterface;
}
"""

_DTS_REACT = """\
// Minimal React type declarations for Capsule pages.
// Auto-generated — do not edit.

declare module "react" {
  type ReactNode =
    | string
    | number
    | boolean
    | null
    | undefined
    | ReactElement
    | ReactNode[];

  interface ReactElement {
    type: any;
    props: any;
    key: string | null;
  }

  type FC<P = {}> = (props: P & { key?: string | number }) => ReactElement | null;
  type PropsWithChildren<P = {}> = P & { children?: ReactNode };
  type CSSProperties = Record<string, string | number>;

  type Dispatch<A> = (value: A) => void;
  type SetStateAction<S> = S | ((prevState: S) => S);
  type DependencyList = readonly unknown[];
  type EffectCallback = () => void | (() => void);
  type Ref<T> = RefObject<T> | ((instance: T | null) => void) | null;

  interface RefObject<T> {
    readonly current: T | null;
  }
  interface MutableRefObject<T> {
    current: T;
  }
  interface Context<T> {
    Provider: FC<{ value: T; children?: ReactNode }>;
    Consumer: FC<{ children: (value: T) => ReactNode }>;
  }

  function useState<S>(initial: S | (() => S)): [S, Dispatch<SetStateAction<S>>];
  function useEffect(effect: EffectCallback, deps?: DependencyList): void;
  function useCallback<T extends (...args: any[]) => any>(cb: T, deps: DependencyList): T;
  function useMemo<T>(factory: () => T, deps: DependencyList): T;
  function useRef<T>(initial: T): MutableRefObject<T>;
  function useRef<T>(initial: T | null): RefObject<T>;
  function useContext<T>(context: Context<T>): T;
  function useReducer<S, A>(reducer: (state: S, action: A) => S, initial: S): [S, Dispatch<A>];

  function createElement(type: any, props?: any, ...children: ReactNode[]): ReactElement;
  function createContext<T>(defaultValue: T): Context<T>;
  function forwardRef<T, P = {}>(
    render: (props: P, ref: Ref<T>) => ReactElement | null,
  ): FC<P & { ref?: Ref<T> }>;
  function memo<P>(component: FC<P>): FC<P>;
  function Fragment(props: { children?: ReactNode }): ReactElement;

  interface SyntheticEvent<T = Element> {
    currentTarget: T;
    target: EventTarget;
    preventDefault(): void;
    stopPropagation(): void;
  }
  interface ChangeEvent<T = Element> extends SyntheticEvent<T> {
    target: EventTarget & T;
  }
  interface MouseEvent<T = Element> extends SyntheticEvent<T> {
    clientX: number;
    clientY: number;
  }
  interface KeyboardEvent<T = Element> extends SyntheticEvent<T> {
    key: string;
    code: string;
  }
  interface FormEvent<T = Element> extends SyntheticEvent<T> {}

  interface HTMLAttributes<T> {
    className?: string;
    id?: string;
    style?: CSSProperties;
    onClick?: (e: MouseEvent<T>) => void;
    onChange?: (e: ChangeEvent<T>) => void;
    onKeyDown?: (e: KeyboardEvent<T>) => void;
    onSubmit?: (e: FormEvent<T>) => void;
    children?: ReactNode;
    key?: string | number;
    ref?: Ref<T>;
    [attr: string]: any;
  }
}

declare module "react/jsx-runtime" {
  export function jsx(type: any, props: any, key?: string): any;
  export function jsxs(type: any, props: any, key?: string): any;
  export const Fragment: any;
}

declare module "react-dom/client" {
  interface Root {
    render(element: any): void;
    unmount(): void;
  }
  function createRoot(container: Element | null): Root;
}
"""

_TSCONFIG = """\
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "module": "esnext",
    "target": "esnext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "strict": false,
    "baseUrl": ".",
    "paths": {
      "@capsule/page": [".capsule/types/capsule-page"],
      "react": [".capsule/types/react"],
      "react/jsx-runtime": [".capsule/types/react"],
      "react-dom/client": [".capsule/types/react"]
    }
  },
  "include": ["**/*.tsx", "**/*.ts", ".capsule/types/*.d.ts"],
  "exclude": ["node_modules"]
}
"""
