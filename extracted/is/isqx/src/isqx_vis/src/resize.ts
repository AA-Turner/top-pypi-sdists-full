import { onCleanup } from "solid-js";
import type { Accessor } from "solid-js";

declare module "solid-js" {
  namespace JSX {
    interface Directives {
      resizable: {
        isMobile: Accessor<boolean>;
        size: Accessor<number>;
        onSizeChange: (size: number) => void;
        minSize?: number;
      };
    }
  }
}

export const resizable = (
  el: HTMLElement,
  accessor: Accessor<{
    isMobile: Accessor<boolean>;
    size: Accessor<number>;
    onSizeChange: (size: number) => void;
    minSize?: number;
  }>
) => {
  const handlePointerDown = (e: PointerEvent) => {
    e.preventDefault();
    el.setPointerCapture(e.pointerId);

    const { isMobile, size, onSizeChange, minSize = 6 } = accessor();
    const startPos = isMobile() ? e.clientY : e.clientX;
    const startSize = size();

    const handlePointerMove = (moveEvent: PointerEvent) => {
      const currentPos = isMobile() ? moveEvent.clientY : moveEvent.clientX;
      const delta = currentPos - startPos;
      const newSize = startSize + (isMobile() ? -delta : delta);

      const maxSize =
        (isMobile() ? window.innerHeight : window.innerWidth) - minSize;
      onSizeChange(Math.max(minSize, Math.min(newSize, maxSize)));
    };

    const handlePointerUp = () => {
      el.releasePointerCapture(e.pointerId);
      window.removeEventListener("pointermove", handlePointerMove);
      window.removeEventListener("pointerup", handlePointerUp);
    };

    window.addEventListener("pointermove", handlePointerMove);
    window.addEventListener("pointerup", handlePointerUp);
  };

  el.addEventListener("pointerdown", handlePointerDown);
  onCleanup(() => el.removeEventListener("pointerdown", handlePointerDown));
};
