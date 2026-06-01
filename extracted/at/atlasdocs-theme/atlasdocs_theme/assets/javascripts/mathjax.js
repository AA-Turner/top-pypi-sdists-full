window.MathJax = {
    tex: {
        inlineMath: [["\\(", "\\)"]],
        displayMath: [["\\[", "\\]"]],
        processEscapes: true,
        processEnvironments: true
    },
    options: {
        ignoreHtmlClass: ".*|",
        processHtmlClass: "arithmatex"
    },
    chtml: {
        fontURL: '/assets/javascripts/output/chtml/fonts/woff-v2'
    }
};

if (typeof document$ !== 'undefined' && document$ && typeof document$.subscribe === 'function') {
    document$.subscribe(() => {
        MathJax.startup.output.clearCache()
        MathJax.typesetClear()
        MathJax.texReset()
        MathJax.typesetPromise()
    })
}