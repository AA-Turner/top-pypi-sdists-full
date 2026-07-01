import { useEffect, type RefObject } from "react";

/**
 * Click-outside + Escape close hook extracted verbatim from
 * `ThemeSwitcher.tsx` so every composer-bar dropdown shares the same
 * dismissal semantics.
 *
 * Usage:
 *   const ref = useRef<HTMLDivElement>(null);
 *   const [open, setOpen] = useState(false);
 *   useDismissableDropdown(open, () => setOpen(false), ref);
 */
export function useDismissableDropdown(
  open: boolean,
  close: () => void,
  wrapperRef: RefObject<HTMLElement | null>,
): void {
  useEffect(() => {
    if (!open) return;
    const onMouseDown = (e: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        close();
      }
    };
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("mousedown", onMouseDown);
    document.addEventListener("keydown", onKey);
    return () => {
      document.removeEventListener("mousedown", onMouseDown);
      document.removeEventListener("keydown", onKey);
    };
  }, [open, close, wrapperRef]);
}
