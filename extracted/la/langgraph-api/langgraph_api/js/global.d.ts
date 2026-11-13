declare namespace NodeJS {
  interface ProcessEnv {
    LANGSERVE_GRAPHS: string;
    LANGGRAPH_UI?: string;
    LANGGRAPH_UI_CONFIG?: string;
    LANGGRAPH_AUTH?: string;
    LANGGRAPH_JS_REMOTE_SOCKET?: string;
    PORT: string;
  }
}
