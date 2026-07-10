import asyncio
import base64
import os
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union
from urllib.parse import unquote, urljoin, urlparse
from uuid import uuid4

import playwright.sync_api
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from abstra_internals.agents import lifecycle
from abstra_internals.constants import get_persistent_dir
from abstra_internals.services.audit import FileScanAuditEvent
from abstra_internals.services.clamav import default_scanner

from .base import AgentTools


class _ThreadDriverState(threading.local):
    context: Optional[Any] = None
    driver: Optional[playwright.sync_api.Playwright] = None
    refcount: int = 0


_thread_driver = _ThreadDriverState()


def _acquire_playwright(debug_mode: bool = False) -> playwright.sync_api.Playwright:
    """Start (or reuse) this thread's shared sync playwright driver.

    Playwright's sync API keeps an asyncio loop marked as running on the
    thread for the driver's whole lifetime, so starting a second driver on
    the same thread trips its "Sync API inside the asyncio loop" guard and
    stacks a second driver process. One refcounted driver per thread avoids
    both; `_release_playwright` stops it when the last holder closes.
    """
    if _thread_driver.refcount > 0 and _thread_driver.driver is not None:
        _thread_driver.refcount += 1
        return _thread_driver.driver

    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            # A loop we don't own is marked as running (e.g. a notebook
            # kernel). Unset the marker so the sync API can start — same
            # behavior BrowserTools always had for this case.
            if debug_mode:
                print("[DEBUG][BrowserTools] Found running event loop, unsetting it")
            asyncio._set_running_loop(None)
    except RuntimeError:
        pass

    context = playwright.sync_api.sync_playwright()
    _thread_driver.driver = context.start()
    _thread_driver.context = context
    _thread_driver.refcount = 1
    return _thread_driver.driver


def _release_playwright() -> None:
    """Drop one reference to the thread's shared driver, stopping it at zero."""
    if _thread_driver.refcount <= 0:
        return
    _thread_driver.refcount -= 1
    if _thread_driver.refcount > 0:
        return
    context = _thread_driver.context
    _thread_driver.context = None
    _thread_driver.driver = None
    if context is not None:
        context.__exit__(None, None, None)


def _default_download_dir() -> Path:
    base = get_persistent_dir() / "browser_tools" / "downloads"
    try:
        from abstra_internals.execution import get_execution_id

        exec_id = get_execution_id()
        if exec_id:
            return base / exec_id
    except Exception:
        pass
    return base


class ClientCertificate(TypedDict):
    origin: str
    pfx_base64: str
    passphrase: str


class ElementExtractor:
    def __init__(self):
        self.interactive_selectors = [
            "a[href]",
            "button",
            "input",
            "textarea",
            "select",
            "input[type='button']",
            "input[type='submit']",
            "[role='button']",
            "[onclick]",
            "[tabindex]:not([tabindex='-1'])",
        ]

    def extract_elements(self, page: Page) -> List[Dict[str, Any]]:
        elements = []

        js_code = r"""
        () => {
            const elements = [];
            const selectors = [
                'a[href]',
                'button',
                'input',
                'textarea',
                'select',
                '[role="button"]',
                '[onclick]',
                '[tabindex]:not([tabindex="-1"])'
            ];

            const seen = new Set();

            function getLabel(el) {
                const ariaLabel = el.getAttribute('aria-label');
                if (ariaLabel) return ariaLabel;

                const title = el.getAttribute('title');
                if (title) return title;

                if (el.id) {
                    const label = document.querySelector(`label[for="${CSS.escape(el.id)}"]`);
                    if (label) return label.innerText.trim();
                }

                const parentLabel = el.closest('label');
                if (parentLabel) return parentLabel.innerText.trim();

                const placeholder = el.getAttribute('placeholder');
                if (placeholder) return `[${placeholder}]`;

                return '';
            }

            function getParentContext(el) {
                const semanticParents = [
                    'form', 'nav', 'header', 'footer', 'main', 'aside', 'section', 'article', 'dialog',
                    '[role="dialog"]', '[role="navigation"]', '[role="form"]', '[role="banner"]', '[role="contentinfo"]'
                ];

                const parent = el.closest(semanticParents.join(','));
                if (!parent) return 'BODY';

                let context = parent.tagName.toLowerCase();

                if (parent.getAttribute('aria-label')) context += ` (${parent.getAttribute('aria-label')})`;
                else if (parent.id) context += ` (#${parent.id})`;
                else if (parent.getAttribute('role')) context += ` [role="${parent.getAttribute('role')}"]`;

                return context.toUpperCase();
            }

            selectors.forEach(selector => {
                document.querySelectorAll(selector).forEach((el, idx) => {
                    if (seen.has(el)) return;
                    seen.add(el);

                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);

                    const isVisible = rect.width > 0 &&
                                    rect.height > 0 &&
                                    style.visibility !== 'hidden' &&
                                    style.display !== 'none' &&
                                    style.opacity !== '0';

                    if (!isVisible) return;

                    const vw = window.innerWidth;
                    const vh = window.innerHeight;
                    const isOnScreen = rect.right > 0 &&
                                       rect.bottom > 0 &&
                                       rect.left < vw &&
                                       rect.top < vh;

                    // Check if element is actually the topmost at its center.
                    // Filters elements hidden behind sticky headers, overlays,
                    // or positioned at (0,0) behind page chrome.
                    let isTopmost = true;
                    if (isOnScreen) {
                        const cx = rect.left + rect.width / 2;
                        const cy = rect.top + rect.height / 2;
                        if (cx >= 0 && cy >= 0 && cx < vw && cy < vh) {
                            const topEl = document.elementFromPoint(cx, cy);
                            isTopmost = !topEl || topEl === el || el.contains(topEl);
                        }
                    }

                    let uniqueSelector = '';
                    if (el.id) {
                        uniqueSelector = `#${CSS.escape(el.id)}`;
                    } else {
                        let path = [];
                        let current = el;
                        while (current && current !== document.body) {
                            let selector = current.tagName.toLowerCase();

                            if (current.className && typeof current.className === 'string') {
                                const classes = current.className.split(' ')
                                    .filter(c => c && !c.startsWith('css-'))
                                    .slice(0, 2)
                                    .map(c => CSS.escape(c));
                                if (classes.length > 0) {
                                    selector += '.' + classes.join('.');
                                }
                            }

                            if (current.parentElement) {
                                const siblings = Array.from(current.parentElement.children);
                                const sameTagSiblings = siblings.filter(s => s.tagName === current.tagName);
                                if (sameTagSiblings.length > 1) {
                                    const index = sameTagSiblings.indexOf(current) + 1;
                                    selector += `:nth-of-type(${index})`;
                                }
                            }

                            path.unshift(selector);
                            current = current.parentElement;
                        }
                        uniqueSelector = path.join(' > ');
                    }

                    const label = getLabel(el);
                    const parentContext = getParentContext(el);

                    let text = el.innerText?.trim().substring(0, 100) ||
                               el.getAttribute('aria-label') ||
                               el.getAttribute('title') ||
                               el.value ||
                               el.alt ||
                               label ||
                               '';

                    const pageX = rect.x + window.scrollX;
                    const pageY = rect.y + window.scrollY;

                    let category;
                    const isInDropdown = el.closest('.dropdown-menu, [role="listbox"], [role="menu"]');
                    if (isInDropdown) {
                        category = 'dropdown-option';
                    } else if (el.tagName === 'BUTTON' || el.type === 'submit' || el.type === 'button' || el.getAttribute('role') === 'button') {
                        category = 'action-button';
                    } else if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT') {
                        category = 'form-input';
                    } else if (el.tagName === 'A' && el.href) {
                        category = 'navigation-link';
                    } else {
                        category = 'other';
                    }

                    elements.push({
                        selector: uniqueSelector,
                        text: text,
                        tag: el.tagName.toLowerCase(),
                        category: category,
                        parent_context: parentContext,
                        attributes: {
                            href: el.href || '',
                            onclick: el.onclick ? 'yes' : '',
                            role: el.getAttribute('role') || '',
                            type: el.type || '',
                            tabindex: el.tabIndex || 0,
                            placeholder: el.getAttribute('placeholder') || '',
                            name: el.name || '',
                            ariaLabel: el.getAttribute('aria-label') || '',
                            title: el.getAttribute('title') || '',
                            dataTestId: el.getAttribute('data-testid') || '',
                            label: label
                        },
                        bbox: {
                            x: Math.round(pageX),
                            y: Math.round(pageY),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        },
                        viewport_bbox: {
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height)
                        },
                        isVisible: rect.width > 0 && rect.height > 0,
                        isOnScreen: isOnScreen,
                        isTopmost: isTopmost
                    });
                });
            });

            const visible = elements.filter(e => e.isVisible && e.isOnScreen && e.isTopmost);

            // Keep DOM order but move dropdown options to the end.
            // Dropdown items (e.g. 88 currency options) bury critical
            // elements like submit buttons when listed inline.
            const main = visible.filter(e => e.category !== 'dropdown-option');
            const dropdown = visible.filter(e => e.category === 'dropdown-option');
            return main.concat(dropdown);
        }
        """

        try:
            raw_elements = page.evaluate(js_code)

            for idx, elem in enumerate(raw_elements):
                elem["index"] = idx
                elements.append(elem)

        except Exception as e:
            print(f"[WARN][ElementExtractor] Error extracting elements: {e}")

        return elements

    def get_element_by_index(
        self, elements: List[Dict[str, Any]], index: int
    ) -> Optional[Dict[str, Any]]:
        for elem in elements:
            if elem["index"] == index:
                return elem
        return None


def _slim_element(element: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "index": element["index"],
        "selector": element["selector"],
        "text": element["text"],
        "tag": element["tag"],
        "category": element["category"],
        "parent_context": element["parent_context"],
        "type": element.get("attributes", {}).get("type", ""),
        "href": element.get("attributes", {}).get("href", ""),
    }


def to_urls(u: Optional[Union[str, Iterable[str]]] = None) -> Optional[Iterable[str]]:
    if u is None:
        return None
    if isinstance(u, str):
        return [u]
    return u


# JS helper that walks the agent's evaluate() result and drops references that
# break JSON serialization downstream (window/self/document/parent are
# self-referential; DOM nodes hold cycles via parentElement/childNodes).
# Without this, scripts like `window.open(...)` return an object that crashes
# the e2e harness with "ValueError: Circular reference detected" when it
# json.dumps the agent step body.
_SAFE_EVAL_WRAPPER = r"""
async () => {
  let __raw;
  try {
    __raw = await (async () => { __SCRIPT__ })();
  } catch (e) {
    return { __scriptError: e && typeof e.message === 'string' ? e.message : String(e) };
  }

  // Opções (com defaults razoáveis para automação de browser).
  const __o = (typeof __opts !== 'undefined' && __opts) || {};
  const MAX_DEPTH = typeof __o.maxDepth === 'number' && isFinite(__o.maxDepth)
    ? Math.max(0, Math.min(__o.maxDepth, 500)) : 8;
  const MAX_ARRAY = typeof __o.maxArrayLength === 'number' && isFinite(__o.maxArrayLength)
    ? Math.max(0, __o.maxArrayLength) : 1000;
  const MAX_KEYS = typeof __o.maxKeys === 'number' && isFinite(__o.maxKeys)
    ? Math.max(0, __o.maxKeys) : 500;
  const MAX_STRING = typeof __o.maxString === 'number' && isFinite(__o.maxString)
    ? Math.max(0, __o.maxString) : 50000;
  const includeNonEnumerable = !!__o.includeNonEnumerable;
  const ancestors = new WeakMap();

  const safeRead = (fn, fb) => { try { return fn(); } catch (e) { return fb; } };
  const safeStr = (v, fb) => (typeof v === 'string' ? v : fb);
  const safeNum = (v, fb) => (typeof v === 'number' && isFinite(v) ? v : fb);

  const describeNode = (n) => {
    const name = safeStr(safeRead(() => n.nodeName, ''), 'Node');
    const id = safeStr(safeRead(() => n.id, ''), '');
    const cls = safeStr(safeRead(() => n.className, ''), '');
    let s = '<' + name.toLowerCase();
    if (id) s += '#' + id;
    if (cls && typeof cls === 'string') s += '.' + cls.split(/\s+/).filter(Boolean).join('.');
    return s + '>';
  };

  const describeFn = (fn) => {
    const name = safeStr(safeRead(() => fn.name, ''), 'anonymous') || 'anonymous';
    const ctorName = safeStr(safeRead(() => fn.constructor && fn.constructor.name, ''), '');
    let kind = 'Function';
    if (ctorName === 'AsyncFunction') kind = 'AsyncFunction';
    else if (ctorName === 'GeneratorFunction') kind = 'GeneratorFunction';
    else if (ctorName === 'AsyncGeneratorFunction') kind = 'AsyncGeneratorFunction';
    return '[' + kind + ': ' + name + ']';
  };

  const describeError = (err, depth, path, walk) => {
    const out = {};
    const rawName = safeRead(() => err.name, '');
    out.__type = safeStr(rawName, '') || 'Error';
    const rawMsg = safeRead(() => err.message, '');
    out.message = typeof rawMsg === 'string' ? rawMsg : walk(rawMsg, depth + 1, path + '.message');
    const stack = safeRead(() => err.stack, '');
    if (typeof stack === 'string') out.stack = stack.length > MAX_STRING ? stack.slice(0, MAX_STRING) + '…' : stack;
    if (safeRead(() => Object.prototype.hasOwnProperty.call(err, 'cause'), false)) {
      out.cause = walk(safeRead(() => err.cause), depth + 1, path + '.cause');
    }
    const errs = safeRead(() => err.errors, undefined);
    if (Array.isArray(errs)) {
      out.errors = errs.slice(0, MAX_ARRAY).map((e, i) => walk(e, depth + 1, path + '.errors[' + i + ']'));
    }
    let ownKeys = [];
    try { ownKeys = Object.getOwnPropertyNames(err); } catch (e) {}
    const skip = { name: 1, message: 1, stack: 1, cause: 1, errors: 1 };
    for (const key of ownKeys) {
      if (skip[key] || key in out) continue;
      out[key] = walk(safeRead(() => err[key], '[Unreadable]'), depth + 1, path + '.' + key);
    }
    let errSymKeys = [];
    try { errSymKeys = Object.getOwnPropertySymbols(err); } catch (e) {}
    for (const sym of errSymKeys) {
      const k = sym.toString();
      if (k in out) continue;
      out[k] = walk(safeRead(() => err[sym], '[Unreadable]'), depth + 1, path + '.' + k);
    }
    return out;
  };

  const walk = (value, depth, path) => {
    if (depth > MAX_DEPTH) return '[MaxDepth]';
    if (value === null) return null;
    if (value === undefined) return '[undefined]';
    const t = typeof value;
    if (t === 'string') return value.length > MAX_STRING ? value.slice(0, MAX_STRING) + '…' : value;
    if (t === 'boolean') return value;
    if (t === 'number') {
      if (value !== value) return '[NaN]';
      if (value === Infinity) return '[Infinity]';
      if (value === -Infinity) return '[-Infinity]';
      return value;
    }
    if (t === 'bigint') return value.toString() + 'n';
    if (t === 'symbol') return value.toString();
    if (t === 'function') {
      let extras = [];
      let extraSyms = [];
      try {
        const skip = { length: 1, name: 1, prototype: 1, arguments: 1, caller: 1 };
        extras = Object.getOwnPropertyNames(value).filter((k) => !skip[k]);
      } catch (e) {}
      try { extraSyms = Object.getOwnPropertySymbols(value); } catch (e) {}
      if (extras.length === 0 && extraSyms.length === 0) return describeFn(value);
      const out = { __type: 'Function', __signature: describeFn(value) };
      ancestors.set(value, path);
      try {
        for (const k of extras.slice(0, MAX_KEYS)) {
          out[k] = walk(safeRead(() => value[k], '[Unreadable]'), depth + 1, path + '.' + k);
        }
        for (const s of extraSyms.slice(0, MAX_KEYS)) {
          out[s.toString()] = walk(safeRead(() => value[s], '[Unreadable]'), depth + 1, path + '.' + s.toString());
        }
      } finally { ancestors.delete(value); }
      return out;
    }
    if (t !== 'object') return String(value);

    if (ancestors.has(value)) return '[Circular -> ' + (ancestors.get(value) || 'root') + ']';

    // DOM / browser globals
    if (typeof Node !== 'undefined' && safeRead(() => value instanceof Node, false)) return describeNode(value);
    if (typeof Window !== 'undefined' && safeRead(() => value instanceof Window, false)) return '[Window]';
    if (typeof Document !== 'undefined' && safeRead(() => value instanceof Document, false)) return '[Document]';
    if (typeof Event !== 'undefined' && safeRead(() => value instanceof Event, false)) {
      return { __type: safeStr(safeRead(() => value.constructor && value.constructor.name, ''), 'Event'), type: safeStr(safeRead(() => value.type, ''), '') };
    }

    if (safeRead(() => value instanceof Date, false)) {
      const time = safeRead(() => value.getTime(), NaN);
      if (time !== time) return '[Invalid Date]';
      return safeStr(safeRead(() => value.toISOString(), ''), '[Invalid Date]');
    }
    if (safeRead(() => value instanceof RegExp, false)) {
      return safeStr(safeRead(() => value.toString(), ''), '[RegExp]');
    }
    if (safeRead(() => value instanceof Error, false)) {
      ancestors.set(value, path);
      try { return describeError(value, depth, path, walk); }
      finally { ancestors.delete(value); }
    }
    if (typeof URL !== 'undefined' && safeRead(() => value instanceof URL, false)) {
      return safeStr(safeRead(() => value.toString(), ''), '[URL]');
    }
    if (safeRead(() => value instanceof Map, false)) {
      ancestors.set(value, path);
      const entries = [];
      let truncated = 0;
      try {
        let i = 0;
        for (const pair of value) {
          if (i >= MAX_ARRAY) { truncated++; continue; }
          const k = pair && safeRead(() => pair[0]);
          const v = pair && safeRead(() => pair[1]);
          entries.push([walk(k, depth + 1, path + '.<k:' + i + '>'), walk(v, depth + 1, path + '.<v:' + i + '>')]);
          i++;
        }
      } catch (e) {}
      ancestors.delete(value);
      const out = { __type: 'Map', entries };
      if (truncated) out.truncated = truncated;
      return out;
    }
    if (safeRead(() => value instanceof Set, false)) {
      ancestors.set(value, path);
      const values = [];
      let truncated = 0;
      try {
        let i = 0;
        for (const v of value) {
          if (i >= MAX_ARRAY) { truncated++; continue; }
          values.push(walk(v, depth + 1, path + '.<i:' + i + '>'));
          i++;
        }
      } catch (e) {}
      ancestors.delete(value);
      const out = { __type: 'Set', values };
      if (truncated) out.truncated = truncated;
      return out;
    }
    if (safeRead(() => value instanceof WeakMap, false)) return '[WeakMap]';
    if (safeRead(() => value instanceof WeakSet, false)) return '[WeakSet]';
    if (safeRead(() => value instanceof Promise, false)) return '[Promise]';
    if (typeof WeakRef !== 'undefined' && safeRead(() => value instanceof WeakRef, false)) return '[WeakRef]';

    if (typeof Blob !== 'undefined' && safeRead(() => value instanceof Blob, false)) {
      return { __type: 'Blob', size: safeNum(safeRead(() => value.size, 0), 0), type: safeStr(safeRead(() => value.type, ''), '') };
    }
    if (typeof File !== 'undefined' && safeRead(() => value instanceof File, false)) {
      return { __type: 'File', name: safeStr(safeRead(() => value.name, ''), ''), size: safeNum(safeRead(() => value.size, 0), 0), type: safeStr(safeRead(() => value.type, ''), '') };
    }
    if (typeof FormData !== 'undefined' && safeRead(() => value instanceof FormData, false)) {
      const out = { __type: 'FormData', entries: [] };
      try {
        let i = 0;
        for (const [k, v] of value.entries()) {
          if (i++ >= MAX_ARRAY) break;
          out.entries.push([k, walk(v, depth + 1, path + '.<fd:' + i + '>')]);
        }
      } catch (e) {}
      return out;
    }
    if (typeof Headers !== 'undefined' && safeRead(() => value instanceof Headers, false)) {
      const out = {};
      try { for (const [k, v] of value.entries()) out[k] = v; } catch (e) {}
      return { __type: 'Headers', values: out };
    }
    if (typeof URLSearchParams !== 'undefined' && safeRead(() => value instanceof URLSearchParams, false)) {
      return safeStr(safeRead(() => value.toString(), ''), '[URLSearchParams]');
    }

    if (typeof Buffer !== 'undefined' && Buffer.isBuffer
        && safeRead(() => Buffer.isBuffer(value), false)) {
      return {
        __type: 'Buffer',
        base64: safeStr(safeRead(() => value.toString('base64'), ''), ''),
        length: safeNum(safeRead(() => value.length, 0), 0),
      };
    }
    if (safeRead(() => value instanceof DataView, false)) {
      const byteLength = safeNum(safeRead(() => value.byteLength, 0), 0);
      const cap = Math.min(byteLength, MAX_ARRAY);
      const bytes = [];
      for (let i = 0; i < cap; i++) bytes.push(safeRead(() => value.getUint8(i), 0));
      const out = { __type: 'DataView', byteLength, byteOffset: safeNum(safeRead(() => value.byteOffset, 0), 0), bytes };
      if (byteLength > cap) out.truncated = byteLength - cap;
      return out;
    }
    if (safeRead(() => ArrayBuffer.isView(value), false)) {
      const length = safeNum(safeRead(() => value.length, 0), 0);
      const cap = Math.min(length, MAX_ARRAY);
      const values = [];
      for (let i = 0; i < cap; i++) values.push(walk(safeRead(() => value[i]), depth + 1, path + '[' + i + ']'));
      const ctor = safeStr(safeRead(() => value.constructor && value.constructor.name, ''), 'TypedArray');
      const out = { __type: ctor, length, values };
      if (length > cap) out.truncated = length - cap;
      return out;
    }
    if (safeRead(() => value instanceof ArrayBuffer, false)) {
      return { __type: 'ArrayBuffer', byteLength: safeNum(safeRead(() => value.byteLength, 0), 0) };
    }

    // toJSON em objetos comuns (consistente com JSON.stringify). Aplicado
    // depois dos branches especiais para que Date/Buffer/TypedArray/etc.
    // mantenham seu tratamento dedicado.
    const toJSON = safeRead(() => value.toJSON, undefined);
    if (typeof toJSON === 'function') {
      const replaced = safeRead(() => toJSON.call(value), value);
      if (replaced !== value) return walk(replaced, depth, path);
    }

    const isArray = safeRead(() => Array.isArray(value), false);
    ancestors.set(value, path);
    try {
      if (isArray) {
        const length = safeNum(safeRead(() => value.length, 0), 0);
        const cap = Math.min(length, MAX_ARRAY);
        const arrCtor = safeStr(safeRead(() => value.constructor && value.constructor.name, ''), '');
        if (arrCtor && arrCtor !== 'Array') {
          const out = { __type: arrCtor, length, items: [] };
          for (let i = 0; i < cap; i++) out.items.push(walk(safeRead(() => value[i]), depth + 1, path + '[' + i + ']'));
          if (length > cap) out.truncated = length - cap;
          return out;
        }
        const out = new Array(cap);
        for (let i = 0; i < cap; i++) out[i] = walk(safeRead(() => value[i]), depth + 1, path + '[' + i + ']');
        if (length > cap) out.push('[+' + (length - cap) + ' truncated]');
        return out;
      }

      let keys = [];
      try {
        keys = includeNonEnumerable
          ? Object.getOwnPropertyNames(value)
          : Object.keys(value);
      } catch (e) {}
      let symKeys = [];
      try {
        const all = Object.getOwnPropertySymbols(value);
        symKeys = includeNonEnumerable ? all : all.filter((s) => {
          const d = safeRead(() => Object.getOwnPropertyDescriptor(value, s), null);
          return d && d.enumerable;
        });
      } catch (e) {}

      // Object.create(null) evita que escrever out['__proto__'] altere o prototype
      // em vez de criar a propriedade.
      const out = Object.create(null);
      const userHasType = keys.indexOf('__type') !== -1;
      const ctorName = safeStr(safeRead(() => value.constructor && value.constructor.name, ''), '');
      if (!userHasType && ctorName && ctorName !== 'Object') out.__type = ctorName;

      const cap = Math.min(keys.length, MAX_KEYS);
      for (let i = 0; i < cap; i++) {
        const k = keys[i];
        out[k] = walk(safeRead(() => value[k], '[Unreadable]'), depth + 1, path + '.' + k);
      }
      if (keys.length > cap) out.__truncatedKeys = keys.length - cap;

      const used = {};
      for (const sym of symKeys.slice(0, MAX_KEYS)) {
        let key = sym.toString();
        if (Object.prototype.hasOwnProperty.call(out, key) || used[key]) {
          let n = 2;
          let cand = key + '#' + n;
          while (Object.prototype.hasOwnProperty.call(out, cand) || used[cand]) cand = key + '#' + (++n);
          key = cand;
        }
        used[key] = 1;
        out[key] = walk(safeRead(() => value[sym], '[Unreadable]'), depth + 1, path + '.' + key);
      }
      return out;
    } finally { ancestors.delete(value); }
  };

  try {
    return walk(__raw, 0, 'root');
  } catch (e) {
    return { __unserializable: e && typeof e.message === 'string' ? e.message : 'unknown' };
  }
}
"""


def _wrap_for_safe_eval(script: str) -> str:
    """Wrap a user script so its result is JSON-safe.

    The script is injected verbatim into `(async () => { __SCRIPT__ })()`,
    so the agent MUST use `return X;` to surface a value. Without `return`
    the result is `undefined` (the script ran for side effects only).

    We deliberately do not try to detect whether the snippet is a
    statement or an expression — earlier heuristics flipped between
    different wrappings depending on whitespace/semicolons (`42` vs `42;`
    vs `let x = 42;`) and that produced silent, hard-to-trace bugs. A
    strict contract surfaces clearly via the SyntaxError feedback in
    `execute_javascript`.
    """
    return "(" + _SAFE_EVAL_WRAPPER.replace("__SCRIPT__", script) + ")()"


def _is_target_closed(e: Exception) -> bool:
    msg = str(e)
    return "Target" in msg and "closed" in msg


def _choose_select_option(target, selector: str, value: str) -> None:
    """Pick an option on a <select> by its value, falling back to its visible
    label. `target` is a Playwright Page or Frame (both expose select_option)."""
    try:
        target.select_option(selector, value=value, timeout=5000)
    except PlaywrightTimeoutError:
        target.select_option(selector, label=value, timeout=5000)


def _safe_download_filename(filename: Optional[str]) -> str:
    if not filename:
        return "download"
    name = Path(unquote(filename)).name.strip()
    return name or "download"


def _filename_from_url(url: str) -> str:
    parsed = urlparse(url)
    return _safe_download_filename(parsed.path)


def _same_origin(left: str, right: str) -> bool:
    left_parsed = urlparse(left)
    right_parsed = urlparse(right)

    def port(parsed):
        if parsed.port is not None:
            return parsed.port
        if parsed.scheme == "https":
            return 443
        if parsed.scheme == "http":
            return 80
        return None

    return (left_parsed.scheme, left_parsed.hostname, port(left_parsed)) == (
        right_parsed.scheme,
        right_parsed.hostname,
        port(right_parsed),
    )


def _resolve_download_path(
    output_path: Optional[str],
    suggested_filename: Optional[str],
    overwrite: bool,
) -> Path:
    filename = _safe_download_filename(suggested_filename)
    if output_path is None:
        download_dir = _default_download_dir()
        download_dir.mkdir(parents=True, exist_ok=True)
        path = download_dir / filename
        if path.exists() and not overwrite:
            raise FileExistsError(
                f"File '{path}' already exists. Pass overwrite=True to replace it."
            )
        return path

    raw_output_path = os.path.expanduser(output_path)
    path = Path(raw_output_path)

    if raw_output_path.endswith((os.sep, "/")) or (path.exists() and path.is_dir()):
        path = path / filename

    if path.exists() and not overwrite:
        raise FileExistsError(
            f"File '{path}' already exists. Pass overwrite=True to replace it."
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class BrowserTools(AgentTools):
    """
    Toolkit that gives an agent a headless Chromium browser via Playwright. The agent gets tools for navigation, clicking, filling forms, downloading files, screenshotting, and extracting page content; optional flags add network, console, and WebSocket capture tools.
    """

    urls: Optional[Iterable[str]]
    browser: playwright.sync_api.Browser
    pages: Dict[str, playwright.sync_api.Page]
    listen_network: bool
    listen_console: bool
    listen_websocket: bool
    network_requests: Dict[str, List[playwright.sync_api.Request]]
    console_logs: Dict[str, List[playwright.sync_api.ConsoleMessage]]
    websocket_frames: Dict[str, List[dict]]
    debug_mode: bool
    allow_close_page: bool
    headless: bool
    _closed: bool

    def __init__(
        self,
        url: Optional[Union[str, Iterable[str]]] = None,
        listen_network: bool = False,
        listen_console: bool = False,
        listen_websocket: bool = False,
        debug_mode: bool = False,
        allow_close_page: bool = True,
        headless: bool = True,
        client_certificate: Optional[ClientCertificate] = None,
    ):
        """
        Build a BrowserTools toolkit, optionally scoped to specific URLs and with optional capture of network, console, and WebSocket activity.

        Args:
            url (Optional): Restrict navigation to one URL or a list of allowed URLs. `None` allows any URL. Defaults to None.
            listen_network (bool): If True, capture all HTTP requests made by the page and expose `get_network_requests` to the agent. Defaults to False.
            listen_console (bool): If True, capture browser console messages and expose `get_console_logs` to the agent. Defaults to False.
            listen_websocket (bool): If True, capture WebSocket frames and expose `get_websocket_frames` to the agent. Defaults to False.
            debug_mode (bool): If True, print verbose debug output for every browser action (navigation, clicks, fills, etc.). Useful for local development. Defaults to False.
            allow_close_page (bool): If True, expose a `close_page` tool to the agent. Defaults to True.
            headless (bool): Run Chromium in headless mode. Set to False to see the browser window during local development. Defaults to True.
            client_certificate (Optional): Optional mTLS client certificate to present on requests, as a dict with keys `origin`, `pfx_base64`, and `passphrase`. Defaults to None.
        """
        self.urls = to_urls(url)
        self.debug_mode = debug_mode
        self.allow_close_page = allow_close_page
        self.headless = headless
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.__init__] url={url}, listen_network={listen_network}, listen_console={listen_console}, debug_mode={debug_mode}, allow_close_page={allow_close_page}"
            )
            print(f"[DEBUG][BrowserTools.__init__] resolved urls={self.urls}")
        self._closed = False
        pw = _acquire_playwright(debug_mode=self.debug_mode)
        lifecycle.register_tool(self)
        try:
            selenium_remote_url = os.environ.get("SELENIUM_REMOTE_URL")
            self._is_remote = bool(selenium_remote_url)
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.__init__] Launching chromium (headless={self.headless}, remote={self._is_remote})"
                )
            if not self._is_remote:
                # Local only: auto-install Chromium if missing
                # Web editor uses remote Selenium via SELENIUM_REMOTE_URL
                if not os.path.exists(pw.chromium.executable_path):
                    if self.debug_mode:
                        print(
                            "[DEBUG][BrowserTools.__init__] Chromium not found, installing..."
                        )
                    subprocess.run(
                        [sys.executable, "-m", "playwright", "install", "chromium"],
                        check=True,
                    )
            # When SELENIUM_REMOTE_URL is set, Playwright automatically routes
            # through Selenium Grid (supported since Playwright 1.28)
            self.browser = pw.chromium.launch(headless=self.headless)
            self._browser_context = self._build_browser_context(client_certificate)
            if self.debug_mode:
                print("[DEBUG][BrowserTools.__init__] Browser launched successfully")
            self.pages = {}
            self.listen_network = listen_network
            self.listen_console = listen_console
            self.listen_websocket = listen_websocket
            self.network_requests = {}
            self.console_logs = {}
            self.websocket_frames = {}
            self._extracted_elements: Dict[str, List[Dict[str, Any]]] = {}
            self.extractor = ElementExtractor()
        except BaseException:
            self.close()
            raise

    def _build_browser_context(
        self, client_certificate: Optional[ClientCertificate]
    ) -> playwright.sync_api.BrowserContext:
        context_options: Dict[str, Any] = {"accept_downloads": True}

        if client_certificate is not None:
            origin: str = client_certificate["origin"]
            pfx_base64: str = client_certificate["pfx_base64"]
            passphrase: str = client_certificate["passphrase"]

            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools._build_browser_context] Using client certificate for origin={origin}"
                )

            context_options["client_certificates"] = [
                {
                    "origin": origin,
                    "pfx": base64.b64decode(pfx_base64),
                    "passphrase": passphrase,
                }
            ]
            context_options["ignore_https_errors"] = True

        return self.browser.new_context(**context_options)

    def close(self):
        # Idempotent and tolerant of partially-built instances: the executor
        # teardown closes leaked tools, and __init__ closes itself on failure.
        if self._closed:
            return
        self._closed = True

        # The driver release and registry removal run in a finally: the
        # executor's SIGTERM handler raises ClientAbandoned (a BaseException),
        # and if it lands mid-close the shared driver refcount must still be
        # dropped — otherwise it stays pinned for the life of the warm
        # executor.
        try:
            pages = getattr(self, "pages", {})
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.close] Closing {len(pages)} pages")
            for page_id, page in list(pages.items()):
                try:
                    if self.debug_mode:
                        print(f"[DEBUG][BrowserTools.close] Closing page {page_id}")
                    page.close()
                except Exception as e:
                    if self.debug_mode:
                        print(
                            f"[DEBUG][BrowserTools.close] Error closing page {page_id}: {e}"
                        )
            pages.clear()

            browser_context = getattr(self, "_browser_context", None)
            if browser_context is not None:
                try:
                    if self.debug_mode:
                        print("[DEBUG][BrowserTools.close] Closing browser context")
                    browser_context.close()
                except Exception as e:
                    if self.debug_mode:
                        print(
                            f"[DEBUG][BrowserTools.close] Error closing browser context: {e}"
                        )

            browser = getattr(self, "browser", None)
            if browser is not None and not getattr(self, "_is_remote", False):
                # Only close the browser for local launches;
                # remote CDP connections share the browser with other clients
                try:
                    if self.debug_mode:
                        print("[DEBUG][BrowserTools.close] Closing browser")
                    browser.close()
                except Exception as e:
                    if self.debug_mode:
                        print(f"[DEBUG][BrowserTools.close] Error closing browser: {e}")
        finally:
            try:
                if self.debug_mode:
                    print("[DEBUG][BrowserTools.close] Releasing playwright driver")
                _release_playwright()
            except Exception as e:
                if self.debug_mode:
                    print(
                        f"[DEBUG][BrowserTools.close] Error releasing playwright driver: {e}"
                    )
            lifecycle.unregister_tool(self)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def _get_page(self, page_id: str) -> Page:
        if page_id not in self.pages:
            raise ValueError(f"Page '{page_id}' does not exist.")
        return self.pages[page_id]

    def _handle_page_crash(self, page_id: str):
        self.pages.pop(page_id, None)
        self._extracted_elements.pop(page_id, None)
        raise RuntimeError(
            "Browser page has closed or crashed. "
            "Call navigate_to_url to start a new session."
        )

    def _resolve_active_page(self, page_id: Optional[str]):
        """Return (page_id, page) for the requested page, falling back to the
        most recently opened page when page_id is omitted or unknown. Raises a
        clear error when no pages are open."""
        if page_id and page_id in self.pages:
            return page_id, self.pages[page_id]
        if not self.pages:
            raise ValueError(
                "No open browser pages. Call navigate_to_url (or open a page) first."
            )
        # dicts preserve insertion order, so the last entry is the newest page
        last_id = next(reversed(self.pages))
        return last_id, self.pages[last_id]

    def _get_page_id_by_request(
        self, request: playwright.sync_api.Request
    ) -> Optional[str]:
        for page_id, page in self.pages.items():
            if request.frame.page == page:
                return page_id
        return None

    def _get_page_id_by_console_message(
        self, msg: playwright.sync_api.ConsoleMessage
    ) -> Optional[str]:
        for page_id, page in self.pages.items():
            if msg.page == page:
                return page_id
        return None

    def _attach_listeners(self, page: playwright.sync_api.Page):
        if self.listen_network:

            def on_request(request: playwright.sync_api.Request):
                page_id = self._get_page_id_by_request(request)
                if page_id:
                    if page_id not in self.network_requests:
                        self.network_requests[page_id] = []
                    self.network_requests[page_id].append(request)

            page.on("request", on_request)

        if self.listen_console:

            def on_console_message(msg: playwright.sync_api.ConsoleMessage):
                page_id = self._get_page_id_by_console_message(msg)
                if page_id:
                    if page_id not in self.console_logs:
                        self.console_logs[page_id] = []
                    self.console_logs[page_id].append(msg)

            page.on("console", on_console_message)

        if self.listen_websocket:
            # Playwright's WebSocket class does not expose a `.page`
            # attribute, so we cannot look up the page from the ws
            # object the way we do for Request/ConsoleMessage. Capture
            # the page reference via closure instead.
            captured_page = page

            def on_websocket(ws: "playwright.sync_api.WebSocket"):
                page_id = next(
                    (pid for pid, p in self.pages.items() if p == captured_page),
                    None,
                )
                if page_id is None:
                    return
                if page_id not in self.websocket_frames:
                    self.websocket_frames[page_id] = []

                ws_url = ws.url
                bound_page_id = page_id

                def record(direction: str):
                    def cb(payload):
                        # payload is str (text frame) or bytes (binary frame)
                        if isinstance(payload, (bytes, bytearray)):
                            self.websocket_frames[bound_page_id].append(
                                {
                                    "url": ws_url,
                                    "direction": direction,
                                    "binary": True,
                                    "payload_b64": base64.b64encode(
                                        bytes(payload)
                                    ).decode("ascii"),
                                }
                            )
                        else:
                            self.websocket_frames[bound_page_id].append(
                                {
                                    "url": ws_url,
                                    "direction": direction,
                                    "binary": False,
                                    "payload": payload,
                                }
                            )

                    return cb

                ws.on("framesent", record("sent"))
                ws.on("framereceived", record("received"))

            page.on("websocket", on_websocket)

    def navigate_to_url(
        self, url: str, page_id: Optional[str] = None
    ) -> Dict[str, str]:
        """Navigate to a URL. If page_id is provided, reuses that page; otherwise creates a new page. Returns page_id, final url, and title. After navigation, call get_page_summary to discover interactive elements on the new page."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.navigate_to_url] url={url}, page_id={page_id}")
        if self.urls is not None and url not in self.urls:
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] URL not allowed. allowed_urls={list(self.urls)}"
                )
            raise PermissionError(f"URL '{url}' is not allowed.")

        if page_id is None:
            page_id = str(uuid4())
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] Creating new page with id={page_id}"
                )
            try:
                page = self._browser_context.new_page()
            except Exception as e:
                if _is_target_closed(e):
                    raise RuntimeError(
                        "Browser has closed. Cannot create new pages. "
                        "The browser session may have expired."
                    )
                raise
            if page is None:
                raise RuntimeError("Failed to create a new browser page.")
            self.pages[page_id] = page
            self._attach_listeners(page)
        else:
            page = self._get_page(page_id)
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.navigate_to_url] Reusing existing page {page_id}"
                )

        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.navigate_to_url] Navigating to {url}")

        try:
            page.goto(url)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        self._extracted_elements.pop(page_id, None)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.navigate_to_url] Navigation complete. page.url={page.url}, title={page.title()}"
            )
        return dict(tab_id=page_id, url=page.url, title=page.title())

    def click(
        self,
        page_id: str,
        selector: Optional[str] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
    ):
        """Click an element by CSS selector, or click at specific x,y coordinates. Provide either selector OR both x and y. IMPORTANT: Use selectors from get_page_summary or get_element_by_summary_index. Prefer click_element(page_id, index) to avoid selector errors."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.click] page_id={page_id}, selector={selector}, x={x}, y={y}"
            )
        page = self._get_page(page_id)

        try:
            if selector is not None:
                element = page.query_selector(selector)
                if element is None:
                    available = self._get_available_selectors_hint(page_id)
                    raise ValueError(
                        f"Selector '{selector}' not found on the page. "
                        f"Use click_element(page_id, index) with an index from get_page_summary instead. "
                        f"{available}"
                    )
                page.click(selector, timeout=5000)
            elif x is not None and y is not None:
                page.mouse.click(x, y)
            else:
                raise ValueError(
                    "Provide either 'selector' OR both 'x' and 'y' coordinates."
                )
        except ValueError:
            raise
        except PlaywrightTimeoutError:
            available = self._get_available_selectors_hint(page_id)
            raise ValueError(
                f"Element '{selector}' found but not clickable (timeout). "
                f"Use click_element(page_id, index) with an index from get_page_summary. "
                f"{available}"
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.click] Click complete. Current url={page.url}")

    def click_element(self, page_id: str, index: int):
        """Click an interactive element by its index from the last get_page_summary. This is the preferred way to click — pass the index number directly instead of a CSS selector. Call get_page_summary first to see available elements and their indices."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.click_element] page_id={page_id}, index={index}"
            )
        element = self._resolve_element(page_id, index)
        self.click(page_id, selector=element["selector"])
        return element

    def _resolve_element(self, page_id: str, index: int) -> Dict[str, Any]:
        page = self._get_page(page_id)
        cached = self._extracted_elements.get(page_id)
        if cached is None:
            cached = self.extractor.extract_elements(page)
            self._extracted_elements[page_id] = cached

        element = self.extractor.get_element_by_index(cached, index)

        if element is not None:
            selector = element.get("selector", "")
            try:
                if selector and not page.query_selector(selector):
                    if self.debug_mode:
                        print(
                            f"[DEBUG][BrowserTools._resolve_element] Stale selector at index {index}, re-extracting"
                        )
                    cached = self.extractor.extract_elements(page)
                    self._extracted_elements[page_id] = cached
                    element = self.extractor.get_element_by_index(cached, index)
            except Exception as e:
                if _is_target_closed(e):
                    self._handle_page_crash(page_id)
                raise

        if element is None:
            count = len(cached)
            raise ValueError(
                f"No element at index {index}. "
                f"Page has {count} elements (indices 0-{count - 1}). "
                f"Call get_page_summary to see current elements."
            )
        return element

    def _get_available_selectors_hint(self, page_id: str) -> str:
        cached = self._extracted_elements.get(page_id)
        if cached is None:
            return ""
        selectors = [
            e["selector"]
            for e in cached
            if e.get("selector") and not e["selector"].startswith("form.")
        ]
        if not selectors:
            return ""
        preview = selectors[:10]
        hint = "Available selectors from last page summary: " + ", ".join(preview)
        if len(selectors) > 10:
            hint += f" ... and {len(selectors) - 10} more"
        return hint

    def fill(self, page_id: str, selector: str, value: str):
        """Fill a form field with a value using a CSS selector. IMPORTANT: Use selectors from get_page_summary or get_element_by_summary_index. Prefer fill_element(page_id, index, value) to avoid selector errors."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.fill] page_id={page_id}, selector={selector}, value={value!r}"
            )
        page = self._get_page(page_id)

        try:
            element = page.query_selector(selector)
            if element is None:
                available = self._get_available_selectors_hint(page_id)
                raise ValueError(
                    f"Selector '{selector}' not found on the page. "
                    f"Use fill_element(page_id, index, value) with an index from get_page_summary instead. "
                    f"{available}"
                )
            page.fill(selector, value, timeout=5000)
        except ValueError:
            raise
        except PlaywrightTimeoutError:
            available = self._get_available_selectors_hint(page_id)
            raise ValueError(
                f"Element '{selector}' found but not fillable (timeout). "
                f"Use fill_element(page_id, index, value) with an index from get_page_summary. "
                f"{available}"
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        if self.debug_mode:
            print("[DEBUG][BrowserTools.fill] Fill complete")

    def fill_element(self, page_id: str, index: int, value: str):
        """Fill a form field by its index from the last get_page_summary. This is the preferred way to fill — pass the index number directly instead of a CSS selector. Call get_page_summary first to see available elements and their indices. Works for text inputs and for <select> dropdowns (pass the option's visible text or its value)."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.fill_element] page_id={page_id}, index={index}, value={value!r}"
            )
        element = self._resolve_element(page_id, index)
        if (element.get("tag") or "").lower() == "select":
            # page.fill() rejects <select> elements; use select_option instead.
            self._select_option(page_id, element["selector"], value)
            return element
        self.fill(page_id, selector=element["selector"], value=value)
        return element

    def _select_option(self, page_id: str, selector: str, value: str):
        """Choose an option in a <select> by its value attribute, falling back
        to its visible label."""
        page = self._get_page(page_id)
        try:
            _choose_select_option(page, selector, value)
        except PlaywrightTimeoutError:
            available = self._get_available_selectors_hint(page_id)
            raise ValueError(
                f"Could not select {value!r} in dropdown '{selector}'. "
                f"Pass the option's exact visible text or its value attribute. {available}"
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

    def get_html(self, page_id: str) -> str:
        """Get the full HTML content of the page. Prefer get_page_summary for identifying interactive elements — use this only when you need raw HTML inspection."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_html] page_id={page_id}")
        page = self._get_page(page_id)
        try:
            content = page.content()
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_html] Got HTML content, length={len(content)}"
            )
        return content

    def get_element_html(self, page_id: str, selector: str) -> str:
        """Get the outer HTML of a specific element by CSS selector."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_element_html] page_id={page_id}, selector={selector}"
            )
        page = self._get_page(page_id)
        el = page.query_selector(selector)
        if not el:
            raise ValueError(f"Selector '{selector}' not found on the page")
        return el.evaluate("el => el.outerHTML")

    def get_text(self, page_id: str, selector: str) -> str:
        """Get the inner text content of an element by CSS selector."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_text] page_id={page_id}, selector={selector}"
            )
        page = self._get_page(page_id)
        try:
            element = page.query_selector(selector)
            if element is None:
                raise ValueError(
                    f"Selector '{selector}' not found. "
                    f"Call get_page_summary to see current elements."
                )
            text = page.inner_text(selector)
        except ValueError:
            raise
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_text] Got text, length={len(text)}, preview={text[:200]!r}"
            )
        return text

    def get_attribute(
        self, page_id: str, selector: str, attribute: str
    ) -> Optional[str]:
        """Get a single HTML attribute value from an element by CSS selector."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attribute] page_id={page_id}, selector={selector}, attribute={attribute}"
            )
        page = self._get_page(page_id)
        try:
            element = page.query_selector(selector)
            if element is None:
                raise ValueError(
                    f"Selector '{selector}' not found. "
                    f"Call get_page_summary to see current elements."
                )
            value = page.get_attribute(selector, attribute)
        except ValueError:
            raise
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_attribute] Result: {value!r}")
        return value

    def get_attributes(self, page_id: str, selector: str) -> Dict[str, Optional[str]]:
        """Get all HTML attributes of an element by CSS selector. Returns a dict of attribute name to value."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attributes] page_id={page_id}, selector={selector}"
            )
        page = self._get_page(page_id)
        try:
            element_handle = page.query_selector(selector)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if element_handle is None:
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.get_attributes] No element found for selector={selector}"
                )
            raise ValueError(f"Selector '{selector}' did not match any elements.")
        attrs = element_handle.evaluate(
            "el => { const attrs = {}; for (let attr of el.attributes) { attrs[attr.name] = attr.value; } return attrs; }"
        )
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_attributes] Found {len(attrs)} attributes: {list(attrs.keys())}"
            )
        return attrs

    def get_all_links(self, page_id: str) -> List[Dict[str, str]]:
        """Get all links on the page as a list of {text, href} objects."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_all_links] page_id={page_id}")
        page = self._get_page(page_id)
        try:
            links = page.query_selector_all("a")
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_all_links] Found {len(links)} <a> elements"
            )
        result = []
        for link in links:
            href = link.get_attribute("href")
            if href is not None:
                result.append({"text": link.inner_text(), "href": href})
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_all_links] Returning {len(result)} links with href"
            )
        return result

    def download_file(
        self,
        page_id: str,
        selector: Optional[str] = None,
        index: Optional[int] = None,
        output_path: Optional[str] = None,
        overwrite: bool = False,
        timeout_ms: int = 30000,
    ) -> Dict[str, Any]:
        """Download a file by clicking an element that triggers a real browser download event (Blob URLs, server endpoints responding with Content-Disposition: attachment, or <a download> links to binary files the browser does not preview inline). It does NOT work for clicks that merely navigate to a URL the browser renders inline (SVG, HTML, plain text, images) — for those, get the URL and use download_url instead. The selector must resolve in the main document; iframes are not traversed automatically. Provide either selector OR index from get_page_summary. The file is saved to output_path when provided; if output_path is a directory, the browser's suggested filename is used inside it. If output_path is omitted, the file is saved inside the project's persistent files folder under `browser_tools/downloads/<execution_id>/<filename>` so it survives across tool calls and can be read back later with FilesTools or fed into upload_file. If a file already exists at the resolved path (e.g. on retry), pass overwrite=True. Returns {path, suggested_filename, url, size_bytes}; the returned `path` is the absolute location of the saved file."""
        if timeout_ms <= 0 or timeout_ms > 120000:
            raise ValueError("timeout_ms must be between 1 and 120000.")
        if selector is not None and index is not None:
            raise ValueError("Provide either selector OR index, not both.")
        if selector is None and index is None:
            raise ValueError("Provide either selector OR index.")

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.download_file] page_id={page_id}, selector={selector}, index={index}, output_path={output_path}, overwrite={overwrite}, timeout_ms={timeout_ms}"
            )

        if index is not None:
            element = self._resolve_element(page_id, index)
            selector = element["selector"]

        assert selector is not None
        page = self._get_page(page_id)

        try:
            element_handle = page.query_selector(selector)
            if element_handle is None:
                available = self._get_available_selectors_hint(page_id)
                raise ValueError(
                    f"Selector '{selector}' not found on the page. "
                    f"Use download_file(page_id, index=...) with an index from get_page_summary instead. "
                    f"{available}"
                )

            with page.expect_download(timeout=timeout_ms) as download_info:
                page.click(selector, timeout=timeout_ms)
            download = download_info.value

            suggested_filename = _safe_download_filename(download.suggested_filename)
            path = _resolve_download_path(output_path, suggested_filename, overwrite)
            download.save_as(str(path))
            scan_started = time.monotonic()
            scan = default_scanner.scan_file(path)
            FileScanAuditEvent(
                scan,
                source_url=download.url,
                filename=path.name,
                file_size_bytes=path.stat().st_size,
                scan_duration_ms=int((time.monotonic() - scan_started) * 1000),
            ).register()
            if scan.is_infected:
                path.unlink(missing_ok=True)
                raise RuntimeError(scan.message or "Download blocked by virus scan.")

            result = {
                "path": str(path),
                "suggested_filename": suggested_filename,
                "url": download.url,
                "size_bytes": path.stat().st_size,
            }
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.download_file] Result: {result}")
            return result
        except ValueError:
            raise
        except PlaywrightTimeoutError:
            raise ValueError(
                f"Clicking '{selector}' did not trigger a download within {timeout_ms}ms. "
                "If the target is a regular URL, use download_url(page_id, url) instead."
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

    def solve_captcha(
        self,
        page_id: str,
        image_selector: str,
        answer_selector: Optional[str] = None,
    ) -> str:
        """Solve an image CAPTCHA (distorted text that must be typed) using Abstra's managed CAPTCHA service. Provide image_selector, the CSS selector of the CAPTCHA <img> element. Optionally provide answer_selector, the CSS selector of the input field where the answer goes; when given, this tool fills it automatically. Returns the solved text. The image is captured directly from the live page (so it matches exactly what is displayed) and never passes through the language model. Do NOT try to read the CAPTCHA yourself from a screenshot and never guess the text — always use this tool. If the solution is rejected by the site, reload/refresh the CAPTCHA and call this tool again (up to a few attempts)."""
        from abstra_internals.controllers.sdk.sdk_context import SDKContextStore

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.solve_captcha] page_id={page_id}, image_selector={image_selector}, answer_selector={answer_selector}"
            )

        page = self._get_page(page_id)
        try:
            element = page.query_selector(image_selector)
            if element is None:
                available = self._get_available_selectors_hint(page_id)
                raise ValueError(
                    f"CAPTCHA image not found with selector '{image_selector}'. {available}"
                )
            # Screenshot the element = exactly the image shown in this session. Works for
            # both data-URI and URL-served CAPTCHAs and keeps the base64 out of the LLM loop.
            image_base64 = base64.b64encode(element.screenshot()).decode("utf-8")
        except ValueError:
            raise
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        text = SDKContextStore.get_by_thread().ai_sdk.solve_captcha(image_base64)

        if answer_selector:
            self.fill(page_id, answer_selector, text)
        return text

    def download_url(
        self,
        page_id: str,
        url: str,
        output_path: Optional[str] = None,
        overwrite: bool = False,
        timeout_ms: int = 30000,
    ) -> Dict[str, Any]:
        """Download a URL using the browser context's authenticated request state (preserves cookies and session). Relative URLs are resolved against the page URL. Prefer this over download_file whenever you already know the URL of the file — it is more robust than driving a click. The file is saved to output_path when provided; if output_path is a directory, the filename from the URL is used inside it. If output_path is omitted, the file is saved inside the project's persistent files folder under `browser_tools/downloads/<execution_id>/<filename>` so it survives across tool calls and can be read back later with FilesTools or fed into upload_file. If a file already exists at the resolved path (e.g. on retry), pass overwrite=True. Returns {path, url, status, headers, size_bytes}; the returned `path` is the absolute location of the saved file. Use download_file() instead only when the URL is unknown ahead of time and only revealed after a click (blob URLs created in-page, POST-triggered downloads, etc.)."""
        if timeout_ms <= 0 or timeout_ms > 120000:
            raise ValueError("timeout_ms must be between 1 and 120000.")

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.download_url] page_id={page_id}, url={url}, output_path={output_path}, overwrite={overwrite}, timeout_ms={timeout_ms}"
            )

        page = self._get_page(page_id)
        resolved_url = urljoin(page.url, url)
        if self.urls is not None and resolved_url not in self.urls:
            if not _same_origin(page.url, resolved_url):
                raise PermissionError(
                    f"URL '{resolved_url}' is not allowed. Direct downloads from a scoped browser session must be same-origin with the current page or explicitly listed in BrowserTools(url=...)."
                )

        path = _resolve_download_path(
            output_path, _filename_from_url(resolved_url), overwrite
        )

        try:
            response = self._browser_context.request.get(
                resolved_url, timeout=timeout_ms
            )
            if not response.ok:
                raise RuntimeError(
                    f"Download failed with HTTP {response.status} {response.status_text} for {resolved_url}"
                )

            body = response.body()
            scan_started = time.monotonic()
            scan = default_scanner.scan_bytes(body, filename=path.name)
            FileScanAuditEvent(
                scan,
                source_url=resolved_url,
                filename=path.name,
                file_size_bytes=len(body),
                scan_duration_ms=int((time.monotonic() - scan_started) * 1000),
            ).register()
            if scan.is_infected:
                raise RuntimeError(scan.message or "Download blocked by virus scan.")
            path.write_bytes(body)

            result = {
                "path": str(path),
                "url": resolved_url,
                "status": response.status,
                "headers": dict(response.headers),
                "size_bytes": len(body),
            }
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.download_url] Result: {result}")
            return result
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

    def upload_file(
        self,
        page_id: str,
        file_path: str,
        selector: Optional[str] = None,
        index: Optional[int] = None,
        timeout_ms: int = 30000,
    ) -> Dict[str, Any]:
        """Upload a file into an <input type=file> on the page. The selector must resolve in the main document — iframes are not traversed automatically. Provide either selector OR index from get_page_summary. file_path must be an absolute path inside the project's persistent files folder; this is the same folder where download_file and download_url save by default, so the natural pattern is: download → reuse the returned `path` here. Paths outside the persistent folder are rejected, and symlinks pointing outside are also rejected (file_path is resolved before validation). Returns {path, size_bytes, selector}."""
        if timeout_ms <= 0 or timeout_ms > 120000:
            raise ValueError("timeout_ms must be between 1 and 120000.")
        if selector is not None and index is not None:
            raise ValueError("Provide either selector OR index, not both.")
        if selector is None and index is None:
            raise ValueError("Provide either selector OR index.")

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.upload_file] page_id={page_id}, selector={selector}, index={index}, file_path={file_path}, timeout_ms={timeout_ms}"
            )

        try:
            resolved = Path(os.path.expanduser(file_path)).resolve(strict=True)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        persisted = get_persistent_dir().resolve()
        if not resolved.is_relative_to(persisted):
            raise PermissionError(
                f"File '{resolved}' is outside the project's persistent folder ('{persisted}'). Only files inside it can be uploaded."
            )

        if index is not None:
            element = self._resolve_element(page_id, index)
            selector = element["selector"]

        assert selector is not None
        page = self._get_page(page_id)

        try:
            element_handle = page.query_selector(selector)
            if element_handle is None:
                available = self._get_available_selectors_hint(page_id)
                raise ValueError(
                    f"Selector '{selector}' not found on the page. "
                    f"Use upload_file(page_id, index=..., file_path=...) with an index from get_page_summary instead. "
                    f"{available}"
                )

            page.set_input_files(selector, str(resolved), timeout=timeout_ms)

            result = {
                "path": str(resolved),
                "size_bytes": resolved.stat().st_size,
                "selector": selector,
            }
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.upload_file] Result: {result}")
            return result
        except ValueError:
            raise
        except PlaywrightTimeoutError:
            raise ValueError(
                f"Setting file on '{selector}' did not complete within {timeout_ms}ms."
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

    def get_network_requests(self, page_id: str) -> Iterable[dict]:
        """Get all captured network requests for a page. Requires listen_network=True on initialization."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_network_requests] page_id={page_id}")
        self._get_page(page_id)

        requests = self.network_requests.get(page_id, [])
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_network_requests] Found {len(requests)} requests for page {page_id}"
            )
            for r in requests:
                print(
                    f"[DEBUG][BrowserTools.get_network_requests]   {r.method} {r.url}"
                )

        result = []
        for request in requests:
            try:
                res = request.response()
            except Exception:
                res = None
            res_data: dict = {"status": None, "headers": None, "body": None}
            if res:
                try:
                    res_data["status"] = res.status
                except Exception:
                    pass
                try:
                    res_data["headers"] = dict(res.headers)
                except Exception:
                    pass
                try:
                    res_data["body"] = res.text()
                except Exception:
                    pass
            result.append(
                {
                    "request": {
                        "url": request.url,
                        "method": request.method,
                        "headers": dict(request.headers),
                        "post_data": request.post_data,
                    },
                    "response": res_data,
                }
            )
        return result

    def get_websocket_frames(self, page_id: str) -> Iterable[dict]:
        """Get all captured WebSocket frames for a page. Requires listen_websocket=True on initialization. Returns a list of {url, direction, binary, payload|payload_b64} dicts in send/receive order. `direction` is "sent" or "received". Text frames carry `payload` (str); binary frames carry `payload_b64` (base64) and have `binary=True`."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_websocket_frames] page_id={page_id}")
        self._get_page(page_id)

        frames = self.websocket_frames.get(page_id, [])
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_websocket_frames] {len(frames)} frames for page {page_id}"
            )

        return list(frames)

    def get_console_logs(self, page_id: str) -> Iterable[dict]:
        """Get all captured console log messages for a page. Requires listen_console=True on initialization."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_console_logs] page_id={page_id}")
        self._get_page(page_id)

        logs = self.console_logs.get(page_id, [])
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_console_logs] Found {len(logs)} console messages for page {page_id}"
            )

        return [
            {
                "type": msg.type,
                "text": msg.text,
                "location": {
                    "url": msg.location["url"],
                    "lineNumber": msg.location["lineNumber"],
                    "columnNumber": msg.location["columnNumber"],
                }
                if msg.location
                else None,
            }
            for msg in logs
        ]

    def list_pages(self) -> Iterable[dict]:
        """List all open browser pages with their page_id, URL, and title."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.list_pages] Total pages: {len(self.pages)}")
        pages: List[dict] = []
        for page_id, page in list(self.pages.items()):
            try:
                pages.append(
                    {"tab_id": page_id, "url": page.url, "title": page.title()}
                )
            except Exception:
                # The page/context/browser was closed underneath us; drop the
                # stale handle instead of failing the entire listing.
                self.pages.pop(page_id, None)
                self._extracted_elements.pop(page_id, None)
        return pages

    def wait(self, page_id: Optional[str] = None, milliseconds: int = 1000):
        """Wait for a number of milliseconds. Use this instead of execute_javascript with setTimeout — it does NOT invalidate the element cache. Useful for waiting after clicks, form submissions, or page transitions before taking a screenshot or calling get_page_summary. If page_id is omitted or unknown, waits on the most recently opened page. milliseconds is clamped to the 0-30000 range."""
        try:
            milliseconds = int(milliseconds)
        except (TypeError, ValueError):
            milliseconds = 1000
        milliseconds = max(0, min(milliseconds, 30000))
        page_id, page = self._resolve_active_page(page_id)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.wait] page_id={page_id}, milliseconds={milliseconds}"
            )
        try:
            page.wait_for_timeout(milliseconds)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        if self.debug_mode:
            print("[DEBUG][BrowserTools.wait] Wait complete")

    def close_page(self, page_id: str):
        """Close a browser page by its page_id."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.close_page] page_id={page_id}")
        if page_id in self.pages:
            page = self.pages[page_id]
            page.close()
            del self.pages[page_id]
            self._extracted_elements.pop(page_id, None)
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.close_page] Page closed. Remaining pages: {list(self.pages.keys())}"
                )
        else:
            raise ValueError(f"Page '{page_id}' does not exist.")

    def execute_javascript(self, page_id: str, script: str):
        """Execute JavaScript code on the page and return the result.

        The script runs inside `(async () => { ... })()`, so to return a
        value you MUST use `return X;`. A script without `return` will
        execute for its side effects but the result is `undefined`.

        Examples:
          - `return document.title;`
          - `return Array.from(document.querySelectorAll('a')).map(a => a.href);`
          - `return await fetch('/api').then(r => r.json());`
          - `setInterval(fn, 50);`  // side-effect only, returns undefined

        WARNING: JavaScript execution may change the DOM. After calling
        this, the cached page summary is invalidated — call get_page_summary
        before using any selectors from a previous summary.
        """
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.execute_javascript] page_id={page_id}, script={script[:200]!r}"
            )
        page = self._get_page(page_id)
        script = _wrap_for_safe_eval(script)
        try:
            result = page.evaluate(script)
        except PlaywrightTimeoutError:
            raise ValueError(
                "JavaScript execution timed out. "
                "Simplify the script or check for infinite loops."
            )
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            error_str = str(e)
            if "SyntaxError" in error_str:
                raise ValueError(
                    f"JavaScript syntax error: {error_str}. "
                    f"The script runs inside `(async () => {{ ... }})()`; "
                    f"use `return X;` to surface a value, or wrap multiple "
                    f"statements as plain statements (no extra parentheses)."
                )
            raise
        self._extracted_elements.pop(page_id, None)
        if self.debug_mode:
            result_preview = repr(result)[:500] if result is not None else "None"
            print(f"[DEBUG][BrowserTools.execute_javascript] Result: {result_preview}")
        return result

    def get_page_summary(self, page_id: str, max_elements: int = 50):
        """Return a list of interactive elements visible on the page (up to max_elements, default 50). Each element has: index, selector, text, tag, category, parent_context, type, href. Use the index with click_element(page_id, index) or fill_element(page_id, index, value) to interact. Call this after ANY action that changes the DOM to get fresh data."""
        if self.debug_mode:
            print(f"[DEBUG][BrowserTools.get_page_summary] page_id={page_id}")
        page = self._get_page(page_id)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_page_summary] Extracting elements from page url={page.url}"
            )
        try:
            full_elements = self.extractor.extract_elements(page)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise
        self._extracted_elements[page_id] = full_elements
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_page_summary] Extracted {len(full_elements)} elements"
            )
            for elem in full_elements:
                print(
                    f"[DEBUG][BrowserTools.get_page_summary]   [{elem['index']}] <{elem['tag']}> text={elem['text'][:50]!r} bbox={elem['viewport_bbox']} selector={elem['selector'][:80]}"
                )
        slim = [_slim_element(e) for e in full_elements]
        total = len(slim)
        if total > max_elements:
            slim = slim[:max_elements]
            slim.append(
                {
                    "note": (
                        f"{total - max_elements} more elements not shown (total: {total}). "
                        f"click_element/fill_element still work with any index 0-{total - 1}. "
                        f"Call get_page_summary(page_id, max_elements={total}) to see all."
                    )
                }
            )
        return slim

    def get_element_by_summary_index(self, page_id: str, index: int):
        """Get detailed information about a specific element by its index from the last get_page_summary result. Returns the full element data including selector, text, tag, bbox, attributes. Use this when you need details beyond what get_page_summary shows (e.g., coordinates, attributes)."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_element_by_summary_index] page_id={page_id}, index={index}"
            )
        element = self._resolve_element(page_id, index)
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.get_element_by_summary_index] Found element: <{element['tag']}> text={element['text'][:50]!r}"
            )
        return element

    def screenshot(
        self,
        page_id: str,
        show_markers: bool = False,
        highlight_element: Optional[str] = None,
    ) -> Path:
        """Take a screenshot of the page for visual analysis. Use show_markers=True to overlay numbered labels on all interactive elements (buttons, links, inputs). Use highlight_element with a CSS selector to highlight a specific element with a red border."""
        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] page_id={page_id}, show_markers={show_markers}, highlight_element={highlight_element}"
            )
        page = self._get_page(page_id)

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] Taking screenshot of url={page.url}"
            )

        if show_markers:
            try:
                full_elements = self.extractor.extract_elements(page)
            except Exception as e:
                if _is_target_closed(e):
                    self._handle_page_crash(page_id)
                raise
            self._extracted_elements[page_id] = full_elements
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.screenshot] Injecting markers for {len(full_elements)} elements"
                )
            marker_js = """
            (elements) => {
                const container = document.createElement('div');
                container.id = '__abstra_markers__';
                container.style.pointerEvents = 'none';
                container.style.position = 'absolute';
                container.style.top = '0';
                container.style.left = '0';
                container.style.zIndex = '2147483647';
                document.body.appendChild(container);

                elements.forEach((elem) => {
                    const border = document.createElement('div');
                    border.style.position = 'absolute';
                    border.style.left = elem.bbox.x + 'px';
                    border.style.top = elem.bbox.y + 'px';
                    border.style.width = elem.bbox.width + 'px';
                    border.style.height = elem.bbox.height + 'px';
                    border.style.border = '2px solid rgba(255, 0, 0, 0.7)';
                    border.style.borderRadius = '2px';
                    border.style.pointerEvents = 'none';
                    container.appendChild(border);

                    const label = document.createElement('div');
                    label.textContent = elem.index;
                    label.style.position = 'absolute';
                    label.style.left = elem.bbox.x + 'px';
                    label.style.top = (elem.bbox.y - 24) + 'px';
                    label.style.background = 'rgba(255, 0, 0, 0.85)';
                    label.style.color = 'white';
                    label.style.fontSize = '16px';
                    label.style.fontWeight = 'bold';
                    label.style.fontFamily = 'monospace';
                    label.style.padding = '2px 6px';
                    label.style.borderRadius = '4px';
                    label.style.lineHeight = '20px';
                    label.style.pointerEvents = 'none';
                    label.style.whiteSpace = 'nowrap';
                    container.appendChild(label);
                });
            }
            """
            page.evaluate(marker_js, full_elements)

        highlight_css = None
        if highlight_element:
            safe_selector = highlight_element.replace("\\", "\\\\").replace('"', '\\"')
            highlight_css = f"{safe_selector} {{ outline: 3px solid red !important; box-shadow: 0 0 8px rgba(255,0,0,0.6) !important; }}"
            if self.debug_mode:
                print(
                    f"[DEBUG][BrowserTools.screenshot] Highlight CSS for selector: {highlight_element}"
                )

        screenshot_kwargs: Dict[str, Any] = {"type": "jpeg", "full_page": show_markers}
        if highlight_css:
            screenshot_kwargs["style"] = highlight_css

        try:
            image_data = page.screenshot(**screenshot_kwargs)
        except Exception as e:
            if _is_target_closed(e):
                self._handle_page_crash(page_id)
            raise

        if self.debug_mode:
            print(
                f"[DEBUG][BrowserTools.screenshot] Screenshot taken, size={len(image_data)} bytes"
            )

        if show_markers:
            page.evaluate(
                "() => { const el = document.getElementById('__abstra_markers__'); if (el) el.remove(); }"
            )
            if self.debug_mode:
                print("[DEBUG][BrowserTools.screenshot] Marker overlays removed")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            image_path = Path(f.name)
            if self.debug_mode:
                print(f"[DEBUG][BrowserTools.screenshot] Saving to {image_path}")
            image_path.write_bytes(image_data)

        return image_path

    def __tools__(self):
        tools = [
            self.navigate_to_url.__name__,
            self.list_pages.__name__,
            self.click.__name__,
            self.click_element.__name__,
            self.fill.__name__,
            self.fill_element.__name__,
            self.get_html.__name__,
            self.get_text.__name__,
            self.get_page_summary.__name__,
            self.get_element_by_summary_index.__name__,
            self.get_attribute.__name__,
            self.get_attributes.__name__,
            self.get_all_links.__name__,
            self.download_file.__name__,
            self.download_url.__name__,
            self.upload_file.__name__,
            self.execute_javascript.__name__,
            self.wait.__name__,
            self.screenshot.__name__,
            self.solve_captcha.__name__,
        ]

        if self.allow_close_page:
            tools.append(self.close_page.__name__)
        if self.listen_network:
            tools.append(self.get_network_requests.__name__)
        if self.listen_console:
            tools.append(self.get_console_logs.__name__)
        if self.listen_websocket:
            tools.append(self.get_websocket_frames.__name__)

        return tools
