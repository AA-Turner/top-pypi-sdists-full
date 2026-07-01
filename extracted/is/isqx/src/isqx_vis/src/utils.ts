import type { StrFragment, CanonicalPath } from "./types";

export const niceName = (canonicalPath: CanonicalPath | undefined): string => {
  if (!canonicalPath) return "";
  const text = canonicalPath.split(".").pop()!.toLowerCase().replace(/_/g, " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
};

/**
 * Extracts the first link target ID from a description fragment or array of fragments.
 * @returns null if no link is found.
 */
export const findCanonicalPathInDescription = (
  description: StrFragment | StrFragment[] | undefined
): CanonicalPath | null => {
  if (!description) return null;
  const items = Array.isArray(description) ? description : [description];
  for (const item of items) {
    if (
      typeof item === "object" &&
      item !== null &&
      typeof item.path === "string"
    ) {
      return item.path;
    }
  }
  return null;
};

export const WRAP_LIMIT = 10;

export const wrapText = (
  text: string,
  limit: number = WRAP_LIMIT
): string[] => {
  if (text.length <= limit) return [text];

  const words = text.split(/\s+/);
  const lines: string[] = [];
  let currentLine = "";

  for (const word of words) {
    if (currentLine.length > 0 && (currentLine + " " + word).length > limit) {
      lines.push(currentLine);
      currentLine = word;
    } else {
      currentLine = currentLine ? currentLine + " " + word : word;
    }
  }
  if (currentLine) {
    lines.push(currentLine);
  }
  return lines;
};
