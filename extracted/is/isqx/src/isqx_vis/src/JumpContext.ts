import { createContext, useContext } from "solid-js";
import type { CanonicalPath } from "./types";

export const JumpContext = createContext<(path: CanonicalPath) => void>();
export const useJumper = () => useContext(JumpContext);
