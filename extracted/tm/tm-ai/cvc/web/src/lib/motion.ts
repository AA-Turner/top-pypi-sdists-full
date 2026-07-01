/**
 * Motion foundation — Wave A of the dashboard UX overhaul.
 *
 * Centralises spring presets, magnetic hover physics, and reduced-motion
 * gating so every animated primitive (ArcButton, ArcChip, page transitions,
 * etc.) speaks the same physical language.
 *
 * Design notes:
 *  - Chip-class motion uses a stiffer spring (snappier, ≤120ms perceived).
 *  - Card-class motion uses a softer spring for a confident, weighty feel.
 *  - Tap feedback is a uniform 0.97 scale — Apple/Linear/Arc convention.
 *  - Magnetic pull is bounded at MAX_PULL px so heavy cursor moves don't
 *    rip the element across the screen; the spring snaps it back on leave.
 *  - All motion respects the OS-level `prefers-reduced-motion` preference.
 */
import { useEffect, useRef, useState } from "react";
import {
  useMotionValue,
  useReducedMotion as useFramerReducedMotion,
  useSpring,
  type Transition,
} from "framer-motion";

/* ─────────────────────────── Spring presets ─────────────────────────── */

/** Snappy spring — buttons, chips, send actions. ~120-150ms perceived. */
export const SPRING_CHIP: Transition = {
  type: "spring",
  stiffness: 400,
  damping: 30,
  mass: 0.7,
};

/** Soft spring — cards, modals, panel reveals. Feels weighty and intentional. */
export const SPRING_CARD: Transition = {
  type: "spring",
  stiffness: 260,
  damping: 24,
  mass: 1,
};

/** Stiff micro-tap spring — for the press-down/release loop. */
export const SPRING_TAP: Transition = {
  type: "spring",
  stiffness: 700,
  damping: 26,
  mass: 0.6,
};

/** Page-level slide+fade transition. ~180ms total, eased. */
export const PAGE_TRANSITION: Transition = {
  duration: 0.18,
  ease: [0.22, 0.61, 0.36, 1],
};

/** Standard tap scale used everywhere clickable. */
export const TAP_SCALE = { scale: 0.97 };

/** Standard hover scale for chips. Subtle — depth comes from the arc border. */
export const HOVER_LIFT = { scale: 1.02 };

/* ─────────────────────────── Reduced-motion gate ─────────────────────────── */

/** Re-export framer's reduced-motion hook so consumers import from one place. */
export function useReducedMotion(): boolean {
  return useFramerReducedMotion() ?? false;
}

/* ─────────────────────────── Magnetic hover ─────────────────────────── */

interface MagneticOptions {
  /** Maximum pull (px) at the centre of the element. Default 8. */
  strength?: number;
  /** Cursor proximity (px) at which the pull engages. Default 80. */
  radius?: number;
  /** Disable entirely (e.g. on touch devices). Default false. */
  disabled?: boolean;
}

interface MagneticReturn<T extends HTMLElement> {
  ref: React.RefObject<T | null>;
  x: ReturnType<typeof useSpring>;
  y: ReturnType<typeof useSpring>;
}

/**
 * Cursor-magnet hover. Element drifts toward the pointer when the cursor
 * enters its proximity halo, then springs back when the cursor leaves.
 *
 * Returns motion values for `x` and `y` — apply via `style={{ x, y }}` on a
 * `motion.button` / `motion.div`. Respects `prefers-reduced-motion` (no-ops).
 */
export function useMagnetic<T extends HTMLElement = HTMLButtonElement>(
  options: MagneticOptions = {},
): MagneticReturn<T> {
  const { strength = 8, radius = 80, disabled = false } = options;
  const ref = useRef<T | null>(null);
  const x = useSpring(useMotionValue(0), SPRING_CHIP);
  const y = useSpring(useMotionValue(0), SPRING_CHIP);
  const reduced = useReducedMotion();

  useEffect(() => {
    if (disabled || reduced) return;
    const el = ref.current;
    if (!el) return;

    let frame = 0;
    const onMove = (e: PointerEvent) => {
      if (frame) return;
      frame = requestAnimationFrame(() => {
        frame = 0;
        const rect = el.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = e.clientX - cx;
        const dy = e.clientY - cy;
        const dist = Math.hypot(dx, dy);
        if (dist > radius) {
          x.set(0);
          y.set(0);
          return;
        }
        // Falloff: full strength at centre, zero at radius.
        const falloff = 1 - dist / radius;
        x.set((dx / radius) * strength * falloff);
        y.set((dy / radius) * strength * falloff);
      });
    };
    const onLeave = () => {
      x.set(0);
      y.set(0);
    };

    window.addEventListener("pointermove", onMove, { passive: true });
    el.addEventListener("pointerleave", onLeave);
    return () => {
      window.removeEventListener("pointermove", onMove);
      el.removeEventListener("pointerleave", onLeave);
      if (frame) cancelAnimationFrame(frame);
    };
  }, [disabled, reduced, radius, strength, x, y]);

  return { ref, x, y };
}

/* ─────────────────────────── Hover state tracker ─────────────────────────── */

/**
 * Tiny hook returning whether an element is currently hovered.
 * Used to gate the arc-border activation so it only animates on hover.
 */
export function useHover<T extends HTMLElement = HTMLElement>(): [
  React.RefObject<T | null>,
  boolean,
] {
  const ref = useRef<T | null>(null);
  const [hovered, setHovered] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const onEnter = () => setHovered(true);
    const onLeave = () => setHovered(false);
    el.addEventListener("pointerenter", onEnter);
    el.addEventListener("pointerleave", onLeave);
    return () => {
      el.removeEventListener("pointerenter", onEnter);
      el.removeEventListener("pointerleave", onLeave);
    };
  }, []);

  return [ref, hovered];
}
