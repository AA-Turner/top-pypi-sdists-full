/**
 * performing symbol highlighting on the client side works most of the time,
 * but comes with many edge cases and performance footguns.
 * 
 * a more robust solution would be to either:
 * - inject `\htmlData` on the python side, so katex can generate `data-id` tags
 *   in the precompiled DOM
 * - adopt manim's approach: precompile formulae into svg and do some tricks to 
 *   "search" for symbols (much like what we're doing here). that way, we don't
 *   need to load katex at all.
 * in both cases a latex distribution will be required, significantly
 * increasing the complexity. the latter is probably the better approach.
 */

import { COLOR_MAP } from "./cmap.mjs";

export function stripTight(s) {
    return s.replaceAll(" mtight", "");
}
/**
 * Extracts the main formula and symbol definitions from a definition block.
 *
 * @param {Element} definition `div.isqx-detail`
 * @returns {{formula: Element, targets: Array<object>}|null} formula and
 * sorted list of targets
 */
function findHighlightTargets(definition) {
    const formula = definition.querySelector(".katex-display .katex-html");
    if (!formula) return null;

    const targets = Array.from(
        definition.querySelectorAll(".isqx-where > .isqx-where-row"),
    )
        .map((row, i) => {
            const katex = row.querySelector(".isqx-symbol .katex");
            const nodes = Array.from(
                katex?.querySelector(".katex-html .base")?.children ?? [],
            ).filter((e) => !e.classList.contains("strut"));

            if (!nodes.length) return null;

            return {
                row,
                originalIndex: i,
                nodes,
                html: nodes.map((n) => stripTight(n.outerHTML)).join(""),
                foundMatches: [],
            };
        })
        .filter(Boolean)
        .sort((a, b) => b.nodes.length - a.nodes.length);

    return targets.length ? { formula, targets } : null;
}

/**
 * Traverses the formula to find all occurrences of the targets.
 *
 * BFS on the KaTeX DOM tree has some limitations:
 * - trying to find $a_b$ in $a_b^c$ fails because KaTeX coalesces
 *   `b` and `c` in the same "column"
 * - trying to find $T$ in $TS$ fails because KaTeX coalesces $T$ and $S$ in the
 *   same `Element`
 *
 * @param {Element} formula The root element of the KaTeX formula.
 * @param {Array<object>} mutTargets The symbol definitions to search for.
 */
function findMatches(formula, mutTargets) {
    const queue = [...formula.children];
    const processedNodes = new Set();

    while (queue.length > 0) {
        const currentNode = queue.shift();
        if (!currentNode.classList) continue;

        let isContained = false;
        for (
            let p = currentNode.parentElement;
            p && p !== formula;
            p = p.parentElement
        ) {
            if (processedNodes.has(p)) {
                isContained = true;
                break;
            }
        }
        if (isContained) continue;

        for (const target of mutTargets) {
            let el = currentNode;
            const matchedNodes = [];
            for (let i = 0; i < target.nodes.length && el; i++) {
                matchedNodes.push(el);
                el = el.nextElementSibling;
            }

            if (
                matchedNodes.length === target.nodes.length &&
                matchedNodes.map((n) => stripTight(n.outerHTML)).join("") ===
                target.html
            ) {
                target.foundMatches.push(matchedNodes);
                matchedNodes.forEach((n) => processedNodes.add(n));
                break;
            }
        }
        queue.push(...currentNode.children);
    }
}

/**
 * Finds and applies interactive highlighting for variables in definition blocks.
 */
export function highlightVariables() {
    const definitions = document.querySelectorAll("div.isqx-detail");

    for (const definition of definitions) {
        const prepared = findHighlightTargets(definition);
        if (!prepared) continue;

        const { formula, targets } = prepared;
        findMatches(formula, targets);

        for (const target of targets) {
            if (!target.foundMatches.length) continue;

            const colorIndex = Math.floor(
                (target.originalIndex / targets.length) *
                (COLOR_MAP.length - 1),
            );
            const [r, g, b] = COLOR_MAP[colorIndex];
            const rgbString = `${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)}`;

            const symbolNode = target.row.querySelector(".isqx-symbol .katex");
            const styledElements = [symbolNode, ...target.foundMatches.flat()];
            const interactiveGroup = [target.row, ...styledElements];

            for (const el of interactiveGroup) {
                el.style.setProperty("--highlight-rgb", rgbString);
                el.addEventListener("mouseenter", () =>
                    interactiveGroup.forEach((el) =>
                        el.classList.add("isqx-hover"),
                    ),
                );
                el.addEventListener("mouseleave", () =>
                    interactiveGroup.forEach((el) =>
                        el.classList.remove("isqx-hover"),
                    ),
                );
            }

            for (const node of styledElements) {
                node.classList.add("isqx-highlight");
            }
        }
    }
}
