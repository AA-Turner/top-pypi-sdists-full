import { useCallback, useEffect, useRef, useState } from "react";

export interface UseResizableOptions {
  storageKey: string;
  /** Width used when fully expanded (also the initial restored value). */
  defaultWidth: number;
  /** Smallest width that still renders the full expanded layout (text + icons). */
  minWidth: number;
  maxWidth: number;
  /** "right" = handle on right edge (left sidebar); "left" = handle on left edge (right panel). */
  edge: "right" | "left";
  /**
   * When user drags below `minWidth - collapseSlack`, the panel snaps to its
   * collapsed (icon-rail) state instead of rendering a half-truncated layout.
   * When dragging back above `minWidth`, it re-expands. Set 0 to disable snap.
   */
  collapsedWidth?: number;
  /** How far below `minWidth` the user must drag before snapping to collapsed. */
  collapseSlack?: number;
}

export interface UseResizableState {
  /** Stored expanded width (never less than minWidth). */
  width: number;
  /** Width to actually render (collapsedWidth when collapsed, else `width`). */
  effectiveWidth: number;
  collapsed: boolean;
  dragging: boolean;
  startDrag(e: React.MouseEvent | React.TouchEvent): void;
  reset(): void;
}

function readStored(
  key: string,
  fallback: number,
): { w: number; collapsed: boolean } {
  if (typeof window === "undefined") return { w: fallback, collapsed: false };
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return { w: fallback, collapsed: false };
    const parsed = JSON.parse(raw);
    return {
      w: typeof parsed.w === "number" ? parsed.w : fallback,
      collapsed: !!parsed.collapsed,
    };
  } catch {
    return { w: fallback, collapsed: false };
  }
}

export function useResizable(opts: UseResizableOptions): UseResizableState {
  const {
    storageKey,
    defaultWidth,
    minWidth,
    maxWidth,
    edge,
    collapsedWidth = 64,
    collapseSlack = 24,
  } = opts;

  const initial = readStored(storageKey, defaultWidth);
  // Stored expanded width is always >= minWidth — collapse is a separate flag.
  const [width, setWidth] = useState<number>(
    Math.max(minWidth, Math.min(maxWidth, initial.w)),
  );
  const [collapsed, setCollapsed] = useState<boolean>(initial.collapsed);
  const [dragging, setDragging] = useState(false);
  const startRef = useRef<{ x: number; w: number; collapsed: boolean } | null>(
    null,
  );

  // Persist (debounced via effect dependency — fires once per change).
  useEffect(() => {
    try {
      localStorage.setItem(
        storageKey,
        JSON.stringify({ w: width, collapsed }),
      );
    } catch {
      /* ignore */
    }
  }, [storageKey, width, collapsed]);

  const onMove = useCallback(
    (clientX: number) => {
      if (!startRef.current) return;
      const dx = clientX - startRef.current.x;
      // Drag direction depends on which edge owns the handle.
      // Anchor: when starting from collapsed, treat origin as `collapsedWidth`
      // so the first pixels of outward drag already grow the panel.
      const anchorW = startRef.current.collapsed
        ? collapsedWidth
        : startRef.current.w;
      const next = edge === "right" ? anchorW + dx : anchorW - dx;

      // Snap-to-collapse zone: anything below (minWidth - slack) collapses.
      const snapBelow = minWidth - collapseSlack;
      if (next < snapBelow) {
        if (!collapsed) setCollapsed(true);
        return;
      }
      // Above the snap zone: ensure expanded + clamp into [minWidth, maxWidth].
      if (collapsed) setCollapsed(false);
      const clamped = Math.max(minWidth, Math.min(maxWidth, next));
      setWidth(clamped);
    },
    [edge, minWidth, maxWidth, collapsedWidth, collapseSlack, collapsed],
  );

  useEffect(() => {
    if (!dragging) return;
    const handleMouseMove = (e: MouseEvent) => onMove(e.clientX);
    const handleTouchMove = (e: TouchEvent) => {
      if (e.touches[0]) onMove(e.touches[0].clientX);
    };
    const stop = () => {
      setDragging(false);
      startRef.current = null;
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    };
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", stop);
    window.addEventListener("touchmove", handleTouchMove);
    window.addEventListener("touchend", stop);
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", stop);
      window.removeEventListener("touchmove", handleTouchMove);
      window.removeEventListener("touchend", stop);
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    };
  }, [dragging, onMove]);

  const startDrag = useCallback(
    (e: React.MouseEvent | React.TouchEvent) => {
      e.preventDefault();
      const clientX =
        "touches" in e
          ? e.touches[0]?.clientX ?? 0
          : (e as React.MouseEvent).clientX;
      startRef.current = { x: clientX, w: width, collapsed };
      setDragging(true);
    },
    [width, collapsed],
  );

  const reset = useCallback(() => {
    setWidth(defaultWidth);
    setCollapsed(false);
  }, [defaultWidth]);

  const effectiveWidth = collapsed ? collapsedWidth : width;

  return {
    width,
    effectiveWidth,
    collapsed,
    dragging,
    startDrag,
    reset,
  };
}

/** Visual drag handle utility class. Positioned absolutely on the resizable edge. */
export function resizeHandleClass(
  edge: "right" | "left",
  active: boolean,
): string {
  const base =
    "absolute top-0 z-50 h-full w-1.5 cursor-col-resize select-none transition-colors";
  const pos = edge === "right" ? "-right-0.5" : "-left-0.5";
  const visual = active
    ? "bg-[color:var(--color-warning)]/40"
    : "bg-transparent hover:bg-[color:var(--midground-base)]/20";
  return `${base} ${pos} ${visual}`;
}
