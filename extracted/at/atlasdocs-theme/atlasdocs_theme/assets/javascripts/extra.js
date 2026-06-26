
let _sourceColors = null;

async function _getSourceColors() {
    if (_sourceColors !== null) return _sourceColors;
    try {
        const base = document.querySelector('base') ? document.querySelector('base').href : '/';
        const url = base.replace(/\/?$/, '/') + 'assets/source-colors.json';
        const resp = await fetch(url);
        _sourceColors = resp.ok ? await resp.json() : {};
    } catch (e) {
        _sourceColors = {};
    }
    return _sourceColors;
}

function _applySourceColors(colors) {
    const path = window.location.pathname;
    for (const [prefix, colorName] of Object.entries(colors)) {
        const seg = '/' + prefix.replace(/^\/|\/$/g, '') + '/';
        if (path.includes(seg) || path.endsWith('/' + prefix.replace(/^\/|\/$/g, ''))) {
            document.body.dataset.sourceColor = colorName;
            return;
        }
    }
    delete document.body.dataset.sourceColor;
}


function initHoverDropdowns() {
    // State stored on the element itself so it survives SPA re-calls.
    document.querySelectorAll('.dropdown-container.is-hover').forEach(function (container) {
        if (container._ddInit) return;
        container._ddInit = true;
        container._ddTimer = null;

        container.addEventListener('mouseenter', function () {
            clearTimeout(container._ddTimer);
            container.classList.add('is-open');
        });
        container.addEventListener('mouseleave', function () {
            clearTimeout(container._ddTimer);
            container._ddTimer = setTimeout(function () {
                container.classList.remove('is-open');
            }, 80);
        });
    });

    // Floating submenus: move to <body> so they are stacking-context siblings
    // of the main dropdown, not children of it.
    document.querySelectorAll('.dropdown-item.has-submenu').forEach(function (item) {
        if (item.dataset.submenuInit) return;
        item.dataset.submenuInit = '1';

        var submenu = item.querySelector('.dropdown-submenu');
        if (!submenu) return;

        // Capture owning container BEFORE detaching from the DOM.
        var container = item.closest('.dropdown-container.is-hover');

        document.body.appendChild(submenu);
        submenu.style.display = 'none';

        var smTimer;

        function positionSubmenu() {
            var rect = item.getBoundingClientRect();
            var smWidth = submenu.offsetWidth || 200;
            var left = rect.left - smWidth;
            if (left < 8) left = rect.right;
            var header = document.querySelector('.md-header');
            var minTop = header ? header.getBoundingClientRect().bottom : 0;
            submenu.style.top  = Math.max(rect.top - 6, minTop) + 'px';
            submenu.style.left = (left - 1) + 'px';
        }

        function keepOpen() {
            clearTimeout(smTimer);
            if (container) clearTimeout(container._ddTimer);
        }

        function hideSubmenu() {
            clearTimeout(smTimer);
            item.classList.remove('is-submenu-open');
            submenu.classList.remove('is-visible');
            submenu.style.display = 'none';
        }

        function openSubmenu() {
            // Instantly close whatever submenu was previously open in this container.
            if (container && container._ddHidePrev) container._ddHidePrev();
            keepOpen();
            if (container) container._ddHidePrev = hideSubmenu;
            item.classList.add('is-submenu-open');
            submenu.style.display = 'flex';
            positionSubmenu();
            requestAnimationFrame(function () { submenu.classList.add('is-visible'); });
        }

        function closeSubmenuOnly() {
            if (container) container._ddHidePrev = null;
            smTimer = setTimeout(function () {
                hideSubmenu();
            }, 20);
        }

        function closeBoth() {
            closeSubmenuOnly();
            if (container) {
                clearTimeout(container._ddTimer);
                container._ddTimer = setTimeout(function () {
                    container.classList.remove('is-open');
                }, 20);
            }
        }

        item.addEventListener('mouseenter', openSubmenu);
        item.addEventListener('mouseleave', closeSubmenuOnly);
        submenu.addEventListener('mouseenter', keepOpen);
        submenu.addEventListener('mouseleave', closeBoth);
    });
}

function _initPage() {
    initHoverDropdowns();

    const repoData = document.getElementById('source-repo-data');
    const repoBtn = document.getElementById('gitlab-repo-button');
    if (repoBtn) {
        const link = repoBtn.querySelector('a');
        const sourceUrl = repoData && repoData.dataset.repoUrl;
        if (sourceUrl && link) {
            link.href = sourceUrl;
            repoBtn.title = 'Go to ' + repoData.dataset.repoLabel + ' repository';
        } else if (link) {
            link.href = repoBtn.dataset.defaultUrl || '#';
            repoBtn.title = 'Go to ' + (repoBtn.dataset.defaultLabel || 'GitLab') + ' repository';
        }
    }
}

if (typeof document$ !== 'undefined' && document$ && typeof document$.subscribe === 'function') {
    document$.subscribe(_initPage);
} else {
    document.addEventListener('DOMContentLoaded', _initPage);
}

// Close all hover dropdowns when focus shifts into a shadow root (e.g. search
// overlay) or when a click lands outside every dropdown container.
function _closeAllDropdowns() {
    document.querySelectorAll('.dropdown-container.is-open').forEach(function (c) {
        c.classList.remove('is-open');
        if (c._ddHidePrev) { c._ddHidePrev(); c._ddHidePrev = null; }
    });
    document.querySelectorAll('.dropdown-submenu.is-visible').forEach(function (sm) {
        sm.classList.remove('is-visible');
        sm.style.display = 'none';
    });
}

document.addEventListener('click', function (e) {
    var path = e.composedPath ? e.composedPath() : [e.target];
    var insideDropdown = path.some(function (el) {
        return el.classList && (el.classList.contains('dropdown-container') || el.classList.contains('dropdown-submenu'));
    });
    if (!insideDropdown) _closeAllDropdowns();
}, true);

// When a shadow root captures focus (search modal, etc.) close any open dropdowns.
document.addEventListener('focusin', function (e) {
    if (e.target && e.target.shadowRoot) _closeAllDropdowns();
}, true);



// ────────────────────────────────────────────────────────────────
// Fix external search result URLs mangled by the search bundle.
//
// The bundle resolves all `location` fields with:
//   new URL('./' + location, base)
// For absolute external URLs (https://twiki.cern.ch/...) this
// produces site.com/https://twiki.cern.ch/... instead of the
// original external URL.  We intercept clicks in capture phase so
// we see them before the bundle's handler and redirect correctly.
//
// e.target.closest() cannot see inside Shadow DOM; composedPath()
// returns the full path including elements inside shadow roots.
// ────────────────────────────────────────────────────────────────
document.addEventListener('click', function (e) {
    var path = e.composedPath ? e.composedPath() : [];
    var a = null;
    for (var i = 0; i < path.length; i++) {
        var el = path[i];
        if (el.tagName === 'A' && el.href) { a = el; break; }
    }
    if (!a) return;

    var href = a.href;
    var mangled = href.match(/\/(https?:\/\/.+)$/);
    if (mangled) href = mangled[1];

    var inSearch = !!(a.closest && a.closest('[data-md-component="search-result"]'));
    var modifier = e.metaKey || e.ctrlKey;

    // Only intercept mangled URLs (always) or search result links with modifier
    if (!mangled && !(inSearch && modifier)) return;

    e.preventDefault();
    e.stopPropagation();
    if (modifier) {
        window.open(href, '_blank', 'noopener');
    } else {
        window.location.href = href;
    }
}, true);




