import re


def normalize_locator_string(js_locator: str) -> str:
    """
    Normalize a JavaScript-style locator string to Python format.

    Examples:
    - getByRole('textbox', { name: 'Customer name:' }) -> get_by_role('textbox', name="Customer name:")
    - getByText('Submit') -> get_by_text('Submit')
    - getByLabel('Email') -> get_by_label('Email')
    - locator('x-details', { hasText: 'Details' }) -> locator('x-details', has_text="Details")
    - getByRole('button', { includeHidden: true }) -> get_by_role('button', include_hidden=True)
    """
    if not js_locator:
        return js_locator

    # Convert camelCase method names to snake_case
    # Handle compound words like TestId first
    js_locator = re.sub(
        r"getBy([A-Z][a-z]+)([A-Z][a-z]+)",
        lambda m: f"get_by_{m.group(1).lower()}_{m.group(2).lower()}",
        js_locator,
    )
    # Handle simple cases
    js_locator = re.sub(
        r"getBy([A-Z][a-z]*)", lambda m: f"get_by_{m.group(1).lower()}", js_locator
    )

    # Convert JavaScript object syntax to Python keyword arguments
    def convert_js_object(match):
        obj_content = match.group(1).strip()

        # Split by commas, but be careful about commas inside strings
        parts = []
        current_part = ""
        in_string = False
        quote_char = None

        for char in obj_content:
            if char in ('"', "'") and not in_string:
                in_string = True
                quote_char = char
                current_part += char
            elif char == quote_char and in_string:
                in_string = False
                quote_char = None
                current_part += char
            elif char == "," and not in_string:
                parts.append(current_part.strip())
                current_part = ""
            else:
                current_part += char

        if current_part.strip():
            parts.append(current_part.strip())

        # Process each part into keyword arguments
        processed_parts = []
        for part in parts:
            part = part.strip()
            # Handle key: value pairs
            if ":" in part:
                key, value = part.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes from key if present
                if key.startswith('"') and key.endswith('"'):
                    key = key[1:-1]
                elif key.startswith("'") and key.endswith("'"):
                    key = key[1:-1]

                # Convert camelCase keys to snake_case
                # Handle common Playwright options
                key = re.sub(r"([a-z])([A-Z])", r"\1_\2", key).lower()

                # Convert single quotes to double quotes for string values
                if value.startswith("'") and value.endswith("'"):
                    value = f'"{value[1:-1]}"'
                elif value == "true":
                    value = "True"
                elif value == "false":
                    value = "False"

                processed_parts.append(f"{key}={value}")
            else:
                processed_parts.append(part)

        return ", ".join(processed_parts)

    # Match JavaScript object literals like { name: 'value', other: 'test' }
    js_locator = re.sub(r"\{\s*([^}]+)\s*\}", convert_js_object, js_locator)

    return js_locator


async def mark_element_for_inspection(context, x: int, y: int, num_ancestors: int):
    """Helper method to mark an element and its ancestors for inspection."""
    await context.evaluate(
        """
    ({x, y, numAncestors}) => {
        const element = document.elementFromPoint(x, y);
        if (element) {
            element.setAttribute("inspected-by", `${x},${y}`);
            var ancestor = element;
            for (let i = 0; i < numAncestors; i++) {
                if (ancestor.parentElement) {
                    ancestor = ancestor.parentElement;
                } else {
                    break;
                }
            }
            // Only set container attribute if it's different from the element
            if (ancestor !== element) {
                ancestor.setAttribute("inspected-by", `${x},${y},${numAncestors}`);
            } else {
                // When num_ancestors=0, element and ancestor are the same
                element.setAttribute("inspected-by-container", `${x},${y},${numAncestors}`);
            }
        }
    }
    """,
        {"x": x, "y": y, "numAncestors": num_ancestors},
    )


async def cleanup_inspection_attributes(context, x: int, y: int, num_ancestors: int):
    """Helper method to clean up inspection attributes."""
    await context.evaluate(
        """
    ({x, y, numAncestors}) => {
        const element = document.querySelector(`[inspected-by="${x},${y}"]`);
        if (element) element.removeAttribute("inspected-by");
        
        if (numAncestors === 0) {
            const container = document.querySelector(`[inspected-by-container="${x},${y},${numAncestors}"]`);
            if (container) container.removeAttribute("inspected-by-container");
        } else {
            const container = document.querySelector(`[inspected-by="${x},${y},${numAncestors}"]`);
            if (container) container.removeAttribute("inspected-by");
        }
    }
    """,
        {"x": x, "y": y, "numAncestors": num_ancestors},
    )


async def get_element_result(context, x: int, y: int, num_ancestors: int):
    """Helper method to get the inspection result from marked elements."""
    locator = context.locator(f'[inspected-by="{x},{y}"]')
    if num_ancestors == 0:
        container = context.locator(
            f'[inspected-by-container="{x},{y},{num_ancestors}"]'
        )
    else:
        container = context.locator(f'[inspected-by="{x},{y},{num_ancestors}"]')

    return condensed_path(
        await container.aria_snapshot(), await locator.aria_snapshot()
    )


async def get_element_html_result(
    context, x: int, y: int, num_ancestors: int, max_characters: int = 1024
):
    """Helper method to get the HTML inspection result from marked elements."""
    if num_ancestors == 0:
        container_selector = f'[inspected-by-container="{x},{y},{num_ancestors}"]'
    else:
        container_selector = f'[inspected-by="{x},{y},{num_ancestors}"]'

    target_selector = f'[inspected-by="{x},{y}"]'

    # Try P1+P2+P3 first
    p1_p2_p3_result = await _get_enhanced_html_result(
        context,
        container_selector,
        target_selector,
        include_p1=True,
        include_p2=True,
        include_p3=True,
    )
    if len(p1_p2_p3_result) <= max_characters:
        return p1_p2_p3_result

    # Try P1+P2 if P1+P2+P3 is too long
    p1_p2_result = await _get_enhanced_html_result(
        context,
        container_selector,
        target_selector,
        include_p1=True,
        include_p2=True,
        include_p3=False,
    )
    if len(p1_p2_result) <= max_characters:
        return p1_p2_result

    # Try P1 only if P1+P2 is too long
    p1_result = await _get_enhanced_html_result(
        context,
        container_selector,
        target_selector,
        include_p1=True,
        include_p2=False,
        include_p3=False,
    )
    if len(p1_result) <= max_characters:
        return p1_result

    # Try P0 (only target descendants + path) if P1 is too long
    p0_result = await _get_enhanced_html_result(
        context,
        container_selector,
        target_selector,
        include_p1=False,
        include_p2=False,
        include_p3=False,
    )
    if len(p0_result) <= max_characters:
        return p0_result

    return await _get_original_html_result(context, container_selector, target_selector)


async def _get_original_html_result(
    context, container_selector: str, target_selector: str
):
    """Original HTML result implementation for backward compatibility."""
    # Get the HTML content with truncation similar to inspect_element
    html_content = await context.evaluate(f"""
    () => {{
        const container = document.querySelector('{container_selector}');
        const target = document.querySelector('{target_selector}');
        
        if (!container || !target) {{
            return null;
        }}
        
        // Create a condensed HTML representation
        const condensedHTML = (containerEl, targetEl) => {{
            const buildPath = (element, targetElement) => {{
                const path = [];
                let current = targetElement;
                
                // Build path from target to container
                while (current && current !== containerEl.parentElement) {{
                    path.unshift(current);
                    current = current.parentElement;
                }}
                
                return path;
            }};
            
            const formatElement = (element, isTarget = false) => {{
                const tag = element.tagName.toLowerCase();
                const attrs = [];
                
                // Add key attributes
                if (element.id) attrs.push(`id="${{element.id}}"`);
                if (element.className) attrs.push(`class="${{element.className}}"`);
                if (element.type) attrs.push(`type="${{element.type}}"`);
                if (element.placeholder) attrs.push(`placeholder="${{element.placeholder}}"`);
                if (element.value) attrs.push(`value="${{element.value}}"`);
                
                const attrStr = attrs.length > 0 ? ' ' + attrs.join(' ') : '';
                
                if (element.children.length === 0 && !element.textContent.trim()) {{
                    return `<${{tag}}${{attrStr}}></${{tag}}>`;
                }} else if (element.children.length === 0) {{
                    return `<${{tag}}${{attrStr}}>${{element.textContent.trim()}}</${{tag}}>`;
                }} else {{
                    return `<${{tag}}${{attrStr}}>...</${{tag}}>`;
                }}
            }};
            
            const path = buildPath(containerEl, targetEl);
            let result = '';
            let indent = 0;
            const tab = '  ';
            
            for (let i = 0; i < path.length; i++) {{
                const element = path[i];
                const isTarget = element === targetEl;
                const isLast = i === path.length - 1;
                
                result += tab.repeat(indent) + formatElement(element, isTarget) + '\\n';
                
                if (!isLast) {{
                    indent++;
                    
                    // Add "..." for skipped siblings if this element has multiple children
                    if (element.children.length > 1) {{
                        result += tab.repeat(indent) + '...\\n';
                    }}
                }} else {{
                    // For the target element, show if it has children
                    if (element.children.length > 0) {{
                        result += tab.repeat(indent + 1) + '...\\n';
                    }}
                }}
            }}
            
            return result.trim();
        }};
        
        return condensedHTML(container, target);
    }}
    """)

    return html_content or "Element not found"


async def _get_enhanced_html_result(
    context,
    container_selector: str,
    target_selector: str,
    include_p1: bool,
    include_p2: bool,
    include_p3: bool,
):
    """Enhanced HTML result that includes P1, P2, P3 elements using tree traversal approach."""
    # Convert Python booleans to JavaScript booleans
    js_p1 = "true" if include_p1 else "false"
    js_p2 = "true" if include_p2 else "false"
    js_p3 = "true" if include_p3 else "false"

    html_content = await context.evaluate(f"""
    () => {{
        const container = document.querySelector('{container_selector}');
        const target = document.querySelector('{target_selector}');
        
        if (!container || !target) {{
            return null;
        }}
        
        // Create an enhanced HTML representation using tree traversal
        const enhancedHTML = (containerEl, targetEl, includeP1, includeP2, includeP3) => {{
            const formatElement = (element, hasIncludedChildren = false) => {{
                const tag = element.tagName.toLowerCase();
                const attrs = [];
                
                // Add key attributes
                if (element.id) attrs.push(`id="${{element.id}}"`);
                if (element.className) attrs.push(`class="${{element.className}}"`);
                if (element.type) attrs.push(`type="${{element.type}}"`);
                if (element.placeholder) attrs.push(`placeholder="${{element.placeholder}}"`);
                if (element.value) attrs.push(`value="${{element.value}}"`);
                
                const attrStr = attrs.length > 0 ? ' ' + attrs.join(' ') : '';
                
                if (element.children.length === 0 && !element.textContent.trim()) {{
                    return `<${{tag}}${{attrStr}}></${{tag}}>`;
                }} else if (element.children.length === 0) {{
                    return `<${{tag}}${{attrStr}}>${{element.textContent.trim()}}</${{tag}}>`;
                }} else if (hasIncludedChildren) {{
                    // Don't show ... if we're going to display the children
                    return `<${{tag}}${{attrStr}}>`;
                }} else {{
                    return `<${{tag}}${{attrStr}}>...</${{tag}}>`;
                }}
            }};
            
            // Build the path from container to target
            const buildPath = (element, targetElement) => {{
                const path = [];
                let current = targetElement;
                
                while (current && current !== containerEl.parentElement) {{
                    path.unshift(current);
                    current = current.parentElement;
                }}
                
                return path;
            }};
            
            const path = buildPath(containerEl, targetEl);
            const pathSet = new Set(path);
            
            // Check if an element should be included based on P0/P1/P2/P3 rules
            const shouldInclude = (element, elementPath, currentDepth) => {{
                // Always include elements in the main path
                if (pathSet.has(element)) {{
                    return true;
                }}
                
                // P0: Only include descendants of target element (no siblings, no ancestor siblings)
                if (!includeP1 && !includeP2 && !includeP3) {{
                    if (elementPath.length > 0) {{
                        const parent = elementPath[elementPath.length - 1];
                        if (parent === targetEl) {{
                            return true; // Direct child of target
                        }}
                        // Check if this is a descendant of target
                        let ancestor = parent;
                        while (ancestor && ancestor !== targetEl) {{
                            ancestor = ancestor.parentElement;
                        }}
                        if (ancestor === targetEl) {{
                            return true; // Descendant of target
                        }}
                    }}
                    return false;
                }}
                
                // P1: Include siblings and descendants of target element
                if (includeP1 && elementPath.length > 0) {{
                    const parent = elementPath[elementPath.length - 1];
                    if (parent === targetEl) {{
                        return true; // Sibling or descendant of target
                    }}
                }}
                
                // P2: Include siblings of ancestors (but not target)
                if (includeP2 && elementPath.length > 0) {{
                    const parent = elementPath[elementPath.length - 1];
                    if (pathSet.has(parent) && parent !== targetEl) {{
                        return true; // Sibling of ancestor
                    }}
                }}
                
                // P3: Include descendants of P2 elements (siblings of ancestors)
                if (includeP3 && elementPath.length > 1) {{
                    const grandParent = elementPath[elementPath.length - 2];
                    if (pathSet.has(grandParent) && grandParent !== targetEl) {{
                        const parent = elementPath[elementPath.length - 1];
                        // Check if parent is a sibling of ancestor
                        if (grandParent.children && Array.from(grandParent.children).includes(parent) && !pathSet.has(parent)) {{
                            return true; // Descendant of sibling of ancestor
                        }}
                    }}
                }}
                
                return false;
            }};
            
            // Traverse tree starting from container
            const traverseTree = (element, elementPath, currentDepth) => {{
                const indent = '  '.repeat(currentDepth);
                let result = '';
                let hasIncludedChildren = false;
                
                // Add current element if it should be included
                if (shouldInclude(element, elementPath, currentDepth)) {{
                    // First check if any children will be included
                    const newPath = [...elementPath, element];
                    const childResults = [];
                    
                    for (const child of element.children) {{
                        const childResult = traverseTree(child, newPath, currentDepth + 1);
                        if (childResult) {{
                            childResults.push(childResult);
                            hasIncludedChildren = true;
                        }}
                    }}
                    
                    // Format element based on whether children will be shown
                    result += indent + formatElement(element, hasIncludedChildren) + '\\n';
                    
                    // Add child results
                    result += childResults.join('');
                    
                    // Add closing tag if we showed children
                    if (hasIncludedChildren) {{
                        const tag = element.tagName.toLowerCase();
                        result += indent + `</${{tag}}>\\n`;
                    }}
                    
                    // Add "..." if element has children but none were included
                    // Only add this if the element itself was supposed to show children (in the path or target)
                    if (!hasIncludedChildren && element.children.length > 0 && (pathSet.has(element) || element === targetEl)) {{
                        result += '  '.repeat(currentDepth + 1) + '...\\n';
                    }}
                }}
                
                return result;
            }};
            
            return traverseTree(containerEl, [], 0).trim();
        }};
        
        return enhancedHTML(container, target, {js_p1}, {js_p2}, {js_p3});
    }}
    """)

    return html_content or "Element not found"


async def inspect_element_recursive(
    frame_or_page,
    x: int,
    y: int,
    num_ancestors: int,
    mode: str = "element",
    max_characters: int = 1024,
) -> str:
    """
    Recursive helper method to handle nested iframe inspection for both element and HTML modes.

    This function handles both regular elements and elements within iframes,
    including nested iframes and cross-origin iframes by using Playwright's frame API.

    Args:
        frame_or_page: The frame or page to inspect within
        x: X coordinate relative to the frame/page
        y: Y coordinate relative to the frame/page
        num_ancestors: Number of ancestors to inspect
        mode: Either "element" or "html" to determine the inspection type
        max_characters: Maximum characters in response (only used for HTML mode)

    Returns:
        Either a condensed path representation (element mode) or raw HTML content (html mode)
    """
    import logging

    log = logging.getLogger("va.playwright.dom_utils")

    try:
        # Check if the coordinates hit an iframe within this frame/page
        iframe_element = await frame_or_page.evaluate(
            """
        ({x, y}) => {
            const element = document.elementFromPoint(x, y);
            if (element && element.tagName === 'IFRAME') {
                return {
                    tagName: element.tagName,
                    src: element.src,
                    rect: element.getBoundingClientRect()
                };
            }
            return null;
        }
        """,
            {"x": x, "y": y},
        )

        if iframe_element:
            # We hit an iframe, find the corresponding frame
            target_frame = None

            # For nested iframes, we need to look at child frames of the current frame
            if hasattr(frame_or_page, "child_frames"):
                frames_to_search = frame_or_page.child_frames
            elif hasattr(frame_or_page, "frames"):
                frames_to_search = frame_or_page.frames
            else:
                frames_to_search = []

            # Find the frame that matches the iframe's src
            for frame in frames_to_search:
                if frame.url == iframe_element["src"]:
                    target_frame = frame
                    break

            if target_frame:
                # Calculate coordinates relative to the nested iframe
                iframe_rect = iframe_element["rect"]
                iframe_x = x - iframe_rect["left"]
                iframe_y = y - iframe_rect["top"]

                # Recursively inspect within the nested iframe
                return await inspect_element_recursive(
                    target_frame,
                    iframe_x,
                    iframe_y,
                    num_ancestors,
                    mode,
                    max_characters,
                )
            else:
                # Fallback to iframe element itself if we can't find the frame
                await mark_element_for_inspection(frame_or_page, x, y, num_ancestors)
                if mode == "html":
                    result = await get_element_html_result(
                        frame_or_page, x, y, num_ancestors, max_characters
                    )
                else:
                    result = await get_element_result(
                        frame_or_page, x, y, num_ancestors
                    )
                await cleanup_inspection_attributes(frame_or_page, x, y, num_ancestors)

                return result
        else:
            # No iframe, proceed with normal element inspection
            await mark_element_for_inspection(frame_or_page, x, y, num_ancestors)
            if mode == "html":
                result = await get_element_html_result(
                    frame_or_page, x, y, num_ancestors, max_characters
                )
            else:
                result = await get_element_result(frame_or_page, x, y, num_ancestors)
            await cleanup_inspection_attributes(frame_or_page, x, y, num_ancestors)

            return result

    except Exception as e:
        log.error(f"Failed to inspect {'HTML' if mode == 'html' else 'element'}: {e}")
        return None


def condensed_path(page: str, target: str) -> str:
    """
    Return the minimal subtree (with `- ...` placeholders) that leads
    from the page root down to `target`.

    Parameters
    ----------
    page   : full page string (one line per node, leading spaces = indent)
    target : exact text of the target node (e.g. '- textbox "Check-in Date *" [ref=e1]')

    Returns
    -------
    str  –  subtree string in the same line-based format
    """
    lines = page.splitlines()

    # helper to get indent width in spaces
    def indent_of(line: str) -> int:
        return len(line) - len(line.lstrip())

    # locate the target line in the page
    tgt_clean = target.strip().splitlines()[0]
    try:
        tgt_idx = next(i for i, ln in enumerate(lines) if ln.strip() == tgt_clean)
    except StopIteration:
        raise ValueError("target line not found")

    # walk upward, collecting (indent, stripped_text)
    path = []
    cur_indent = indent_of(lines[tgt_idx])
    path.append((cur_indent, lines[tgt_idx].lstrip()))

    for i in range(tgt_idx - 1, -1, -1):
        ind = indent_of(lines[i])
        if ind < cur_indent:
            path.append((ind, lines[i].lstrip()))
            cur_indent = ind
            if ind == 0:  # reached page root
                break

    path.reverse()  # now root … target

    # recursive assembler -------------------------------------------------
    def assemble(k: int) -> str:
        indent, text = path[k]
        out = [" " * indent + text]  # node itself

        if k + 1 < len(path):  # has a child in the path
            out.append(assemble(k + 1))

            # insert "- ..." for skipped siblings
            if k > 0:  # DON'T add one for the outermost root
                child_indent = path[k + 1][0]
                out.append(" " * child_indent + "- ...")

        return "\n".join(out)

    return assemble(0)
