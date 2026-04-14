import"./jwt-decode.esm-Di13oRQw.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},n=new Error().stack;n&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[n]="781a462c-7785-42bb-8537-9f11f2572e07",e._sentryDebugIdIdentifier="sentry-dbid-781a462c-7785-42bb-8537-9f11f2572e07")}catch{}})();function s(e,n){const r=window.location.origin;return`<script>
(function() {
  var __logBuffer = [];
  var __flushTimer = null;
  var __execId = ${JSON.stringify(e)};
  var __stageId = ${JSON.stringify(n)};
  var __origin = ${JSON.stringify(r)};

  function __flushLogs() {
    if (__logBuffer.length === 0) return;
    var batch = __logBuffer.splice(0);
    try {
      fetch(__origin + "/_logs/" + __execId, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ logs: batch, stageId: __stageId })
      }).catch(function() {});
    } catch(e) {}
  }

  function __scheduleFlush() {
    if (__flushTimer) return;
    __flushTimer = setTimeout(function() {
      __flushTimer = null;
      __flushLogs();
    }, 500);
  }

  function __capture(level, origFn) {
    return function() {
      var args = Array.prototype.slice.call(arguments);
      var msg = args.map(function(a) {
        if (typeof a === "string") return a;
        try { return JSON.stringify(a); } catch(e) { return String(a); }
      }).join(" ");
      __logBuffer.push({ level: level, message: msg });
      __scheduleFlush();
      return origFn.apply(console, arguments);
    };
  }

  console.log = __capture("log", console.log);
  console.error = __capture("error", console.error);
  console.warn = __capture("warn", console.warn);
  console.info = __capture("info", console.info);

  window.addEventListener("error", function(e) {
    __logBuffer.push({ level: "error", message: e.message + " at " + e.filename + ":" + e.lineno });
    __scheduleFlush();
  });

  window.addEventListener("unhandledrejection", function(e) {
    __logBuffer.push({ level: "error", message: "Unhandled rejection: " + (e.reason && e.reason.message || e.reason || "unknown") });
    __scheduleFlush();
  });

  window.addEventListener("beforeunload", function() { __flushLogs(); });
})();
<\/script>`}export{s as b};
//# sourceMappingURL=consoleCapture-0m24QrWJ.js.map
