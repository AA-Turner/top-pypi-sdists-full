// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles
parcelRequire = (function (modules, cache, entry, globalName) {
  // Save the require from previous bundle to this closure if any
  var previousRequire = typeof parcelRequire === 'function' && parcelRequire;
  var nodeRequire = typeof require === 'function' && require;

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire = typeof parcelRequire === 'function' && parcelRequire;
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error('Cannot find module \'' + name + '\'');
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = cache[name] = new newRequire.Module(name);

      modules[name][0].call(module.exports, localRequire, module, module.exports, this);
    }

    return cache[name].exports;

    function localRequire(x){
      return newRequire(localRequire.resolve(x));
    }

    function resolve(x){
      return modules[name][1][x] || x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [function (require, module) {
      module.exports = exports;
    }, {}];
  };

  var error;
  for (var i = 0; i < entry.length; i++) {
    try {
      newRequire(entry[i]);
    } catch (e) {
      // Save first error but execute all entries
      if (!error) {
        error = e;
      }
    }
  }

  if (entry.length) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(entry[entry.length - 1]);

    // CommonJS
    if (typeof exports === "object" && typeof module !== "undefined") {
      module.exports = mainExports;

    // RequireJS
    } else if (typeof define === "function" && define.amd) {
     define(function () {
       return mainExports;
     });

    // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }

  // Override the current require with this new one
  parcelRequire = newRequire;

  if (error) {
    // throw error from earlier, _after updating parcelRequire_
    throw error;
  }

  return newRequire;
})({"UALh":[function(require,module,exports) {
'use strict';

module.exports = value => {
  if (!value) {
    return false;
  }

  // eslint-disable-next-line no-use-extend-native/no-use-extend-native
  if (typeof Symbol.observable === 'symbol' && typeof value[Symbol.observable] === 'function') {
    // eslint-disable-next-line no-use-extend-native/no-use-extend-native
    return value === value[Symbol.observable]();
  }
  if (typeof value['@@observable'] === 'function') {
    return value === value['@@observable']();
  }
  return false;
};
},{}],"huOx":[function(require,module,exports) {
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DefaultSerializer = exports.extendSerializer = void 0;
function extendSerializer(extend, implementation) {
    const fallbackDeserializer = extend.deserialize.bind(extend);
    const fallbackSerializer = extend.serialize.bind(extend);
    return {
        deserialize(message) {
            return implementation.deserialize(message, fallbackDeserializer);
        },
        serialize(input) {
            return implementation.serialize(input, fallbackSerializer);
        }
    };
}
exports.extendSerializer = extendSerializer;
const DefaultErrorSerializer = {
    deserialize(message) {
        return Object.assign(Error(message.message), {
            name: message.name,
            stack: message.stack
        });
    },
    serialize(error) {
        return {
            __error_marker: "$$error",
            message: error.message,
            name: error.name,
            stack: error.stack
        };
    }
};
const isSerializedError = (thing) => thing && typeof thing === "object" && "__error_marker" in thing && thing.__error_marker === "$$error";
exports.DefaultSerializer = {
    deserialize(message) {
        if (isSerializedError(message)) {
            return DefaultErrorSerializer.deserialize(message);
        }
        else {
            return message;
        }
    },
    serialize(input) {
        if (input instanceof Error) {
            return DefaultErrorSerializer.serialize(input);
        }
        else {
            return input;
        }
    }
};

},{}],"ujDW":[function(require,module,exports) {
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.serialize = exports.deserialize = exports.registerSerializer = void 0;
const serializers_1 = require("./serializers");
let registeredSerializer = serializers_1.DefaultSerializer;
function registerSerializer(serializer) {
    registeredSerializer = serializers_1.extendSerializer(registeredSerializer, serializer);
}
exports.registerSerializer = registerSerializer;
function deserialize(message) {
    return registeredSerializer.deserialize(message);
}
exports.deserialize = deserialize;
function serialize(input) {
    return registeredSerializer.serialize(input);
}
exports.serialize = serialize;

},{"./serializers":"huOx"}],"NcLz":[function(require,module,exports) {
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.$worker = exports.$transferable = exports.$terminate = exports.$events = exports.$errors = void 0;
exports.$errors = Symbol("thread.errors");
exports.$events = Symbol("thread.events");
exports.$terminate = Symbol("thread.terminate");
exports.$transferable = Symbol("thread.transferable");
exports.$worker = Symbol("thread.worker");

},{}],"HnZs":[function(require,module,exports) {
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Transfer = exports.isTransferDescriptor = void 0;
const symbols_1 = require("./symbols");
function isTransferable(thing) {
    if (!thing || typeof thing !== "object")
        return false;
    // Don't check too thoroughly, since the list of transferable things in JS might grow over time
    return true;
}
function isTransferDescriptor(thing) {
    return thing && typeof thing === "object" && thing[symbols_1.$transferable];
}
exports.isTransferDescriptor = isTransferDescriptor;
function Transfer(payload, transferables) {
    if (!transferables) {
        if (!isTransferable(payload))
            throw Error();
        transferables = [payload];
    }
    return {
        [symbols_1.$transferable]: true,
        send: payload,
        transferables
    };
}
exports.Transfer = Transfer;

},{"./symbols":"NcLz"}],"No47":[function(require,module,exports) {
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WorkerMessageType = exports.MasterMessageType = void 0;
/////////////////////////////
// Messages sent by master:
var MasterMessageType;
(function (MasterMessageType) {
    MasterMessageType["cancel"] = "cancel";
    MasterMessageType["run"] = "run";
})(MasterMessageType = exports.MasterMessageType || (exports.MasterMessageType = {}));
////////////////////////////
// Messages sent by worker:
var WorkerMessageType;
(function (WorkerMessageType) {
    WorkerMessageType["error"] = "error";
    WorkerMessageType["init"] = "init";
    WorkerMessageType["result"] = "result";
    WorkerMessageType["running"] = "running";
    WorkerMessageType["uncaughtError"] = "uncaughtError";
})(WorkerMessageType = exports.WorkerMessageType || (exports.WorkerMessageType = {}));

},{}],"Oz27":[function(require,module,exports) {
"use strict";
/// <reference lib="dom" />
// tslint:disable no-shadowed-variable
Object.defineProperty(exports, "__esModule", { value: true });
const isWorkerRuntime = function isWorkerRuntime() {
    const isWindowContext = typeof self !== "undefined" && typeof Window !== "undefined" && self instanceof Window;
    return typeof self !== "undefined" && self.postMessage && !isWindowContext ? true : false;
};
const postMessageToMaster = function postMessageToMaster(data, transferList) {
    self.postMessage(data, transferList);
};
const subscribeToMasterMessages = function subscribeToMasterMessages(onMessage) {
    const messageHandler = (messageEvent) => {
        onMessage(messageEvent.data);
    };
    const unsubscribe = () => {
        self.removeEventListener("message", messageHandler);
    };
    self.addEventListener("message", messageHandler);
    return unsubscribe;
};
exports.default = {
    isWorkerRuntime,
    postMessageToMaster,
    subscribeToMasterMessages
};

},{}],"pBGv":[function(require,module,exports) {

// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;
function defaultSetTimout() {
  throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout() {
  throw new Error('clearTimeout has not been defined');
}
(function () {
  try {
    if (typeof setTimeout === 'function') {
      cachedSetTimeout = setTimeout;
    } else {
      cachedSetTimeout = defaultSetTimout;
    }
  } catch (e) {
    cachedSetTimeout = defaultSetTimout;
  }
  try {
    if (typeof clearTimeout === 'function') {
      cachedClearTimeout = clearTimeout;
    } else {
      cachedClearTimeout = defaultClearTimeout;
    }
  } catch (e) {
    cachedClearTimeout = defaultClearTimeout;
  }
})();
function runTimeout(fun) {
  if (cachedSetTimeout === setTimeout) {
    //normal enviroments in sane situations
    return setTimeout(fun, 0);
  }
  // if setTimeout wasn't available but was latter defined
  if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
    cachedSetTimeout = setTimeout;
    return setTimeout(fun, 0);
  }
  try {
    // when when somebody has screwed with setTimeout but no I.E. maddness
    return cachedSetTimeout(fun, 0);
  } catch (e) {
    try {
      // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
      return cachedSetTimeout.call(null, fun, 0);
    } catch (e) {
      // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
      return cachedSetTimeout.call(this, fun, 0);
    }
  }
}
function runClearTimeout(marker) {
  if (cachedClearTimeout === clearTimeout) {
    //normal enviroments in sane situations
    return clearTimeout(marker);
  }
  // if clearTimeout wasn't available but was latter defined
  if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
    cachedClearTimeout = clearTimeout;
    return clearTimeout(marker);
  }
  try {
    // when when somebody has screwed with setTimeout but no I.E. maddness
    return cachedClearTimeout(marker);
  } catch (e) {
    try {
      // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
      return cachedClearTimeout.call(null, marker);
    } catch (e) {
      // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
      // Some versions of I.E. have different rules for clearTimeout vs setTimeout
      return cachedClearTimeout.call(this, marker);
    }
  }
}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;
function cleanUpNextTick() {
  if (!draining || !currentQueue) {
    return;
  }
  draining = false;
  if (currentQueue.length) {
    queue = currentQueue.concat(queue);
  } else {
    queueIndex = -1;
  }
  if (queue.length) {
    drainQueue();
  }
}
function drainQueue() {
  if (draining) {
    return;
  }
  var timeout = runTimeout(cleanUpNextTick);
  draining = true;
  var len = queue.length;
  while (len) {
    currentQueue = queue;
    queue = [];
    while (++queueIndex < len) {
      if (currentQueue) {
        currentQueue[queueIndex].run();
      }
    }
    queueIndex = -1;
    len = queue.length;
  }
  currentQueue = null;
  draining = false;
  runClearTimeout(timeout);
}
process.nextTick = function (fun) {
  var args = new Array(arguments.length - 1);
  if (arguments.length > 1) {
    for (var i = 1; i < arguments.length; i++) {
      args[i - 1] = arguments[i];
    }
  }
  queue.push(new Item(fun, args));
  if (queue.length === 1 && !draining) {
    runTimeout(drainQueue);
  }
};

// v8 likes predictible objects
function Item(fun, array) {
  this.fun = fun;
  this.array = array;
}
Item.prototype.run = function () {
  this.fun.apply(null, this.array);
};
process.title = 'browser';
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};
function noop() {}
process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;
process.listeners = function (name) {
  return [];
};
process.binding = function (name) {
  throw new Error('process.binding is not supported');
};
process.cwd = function () {
  return '/';
};
process.chdir = function (dir) {
  throw new Error('process.chdir is not supported');
};
process.umask = function () {
  return 0;
};
},{}],"DwFB":[function(require,module,exports) {
var process = require("process");
"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.expose = exports.isWorkerRuntime = exports.Transfer = exports.registerSerializer = void 0;
const is_observable_1 = __importDefault(require("is-observable"));
const common_1 = require("../common");
const transferable_1 = require("../transferable");
const messages_1 = require("../types/messages");
const implementation_1 = __importDefault(require("./implementation"));
var common_2 = require("../common");
Object.defineProperty(exports, "registerSerializer", { enumerable: true, get: function () { return common_2.registerSerializer; } });
var transferable_2 = require("../transferable");
Object.defineProperty(exports, "Transfer", { enumerable: true, get: function () { return transferable_2.Transfer; } });
/** Returns `true` if this code is currently running in a worker. */
exports.isWorkerRuntime = implementation_1.default.isWorkerRuntime;
let exposeCalled = false;
const activeSubscriptions = new Map();
const isMasterJobCancelMessage = (thing) => thing && thing.type === messages_1.MasterMessageType.cancel;
const isMasterJobRunMessage = (thing) => thing && thing.type === messages_1.MasterMessageType.run;
/**
 * There are issues with `is-observable` not recognizing zen-observable's instances.
 * We are using `observable-fns`, but it's based on zen-observable, too.
 */
const isObservable = (thing) => is_observable_1.default(thing) || isZenObservable(thing);
function isZenObservable(thing) {
    return thing && typeof thing === "object" && typeof thing.subscribe === "function";
}
function deconstructTransfer(thing) {
    return transferable_1.isTransferDescriptor(thing)
        ? { payload: thing.send, transferables: thing.transferables }
        : { payload: thing, transferables: undefined };
}
function postFunctionInitMessage() {
    const initMessage = {
        type: messages_1.WorkerMessageType.init,
        exposed: {
            type: "function"
        }
    };
    implementation_1.default.postMessageToMaster(initMessage);
}
function postModuleInitMessage(methodNames) {
    const initMessage = {
        type: messages_1.WorkerMessageType.init,
        exposed: {
            type: "module",
            methods: methodNames
        }
    };
    implementation_1.default.postMessageToMaster(initMessage);
}
function postJobErrorMessage(uid, rawError) {
    const { payload: error, transferables } = deconstructTransfer(rawError);
    const errorMessage = {
        type: messages_1.WorkerMessageType.error,
        uid,
        error: common_1.serialize(error)
    };
    implementation_1.default.postMessageToMaster(errorMessage, transferables);
}
function postJobResultMessage(uid, completed, resultValue) {
    const { payload, transferables } = deconstructTransfer(resultValue);
    const resultMessage = {
        type: messages_1.WorkerMessageType.result,
        uid,
        complete: completed ? true : undefined,
        payload
    };
    implementation_1.default.postMessageToMaster(resultMessage, transferables);
}
function postJobStartMessage(uid, resultType) {
    const startMessage = {
        type: messages_1.WorkerMessageType.running,
        uid,
        resultType
    };
    implementation_1.default.postMessageToMaster(startMessage);
}
function postUncaughtErrorMessage(error) {
    try {
        const errorMessage = {
            type: messages_1.WorkerMessageType.uncaughtError,
            error: common_1.serialize(error)
        };
        implementation_1.default.postMessageToMaster(errorMessage);
    }
    catch (subError) {
        // tslint:disable-next-line no-console
        console.error("Not reporting uncaught error back to master thread as it " +
            "occured while reporting an uncaught error already." +
            "\nLatest error:", subError, "\nOriginal error:", error);
    }
}
function runFunction(jobUID, fn, args) {
    return __awaiter(this, void 0, void 0, function* () {
        let syncResult;
        try {
            syncResult = fn(...args);
        }
        catch (error) {
            return postJobErrorMessage(jobUID, error);
        }
        const resultType = isObservable(syncResult) ? "observable" : "promise";
        postJobStartMessage(jobUID, resultType);
        if (isObservable(syncResult)) {
            const subscription = syncResult.subscribe(value => postJobResultMessage(jobUID, false, common_1.serialize(value)), error => {
                postJobErrorMessage(jobUID, common_1.serialize(error));
                activeSubscriptions.delete(jobUID);
            }, () => {
                postJobResultMessage(jobUID, true);
                activeSubscriptions.delete(jobUID);
            });
            activeSubscriptions.set(jobUID, subscription);
        }
        else {
            try {
                const result = yield syncResult;
                postJobResultMessage(jobUID, true, common_1.serialize(result));
            }
            catch (error) {
                postJobErrorMessage(jobUID, common_1.serialize(error));
            }
        }
    });
}
/**
 * Expose a function or a module (an object whose values are functions)
 * to the main thread. Must be called exactly once in every worker thread
 * to signal its API to the main thread.
 *
 * @param exposed Function or object whose values are functions
 */
function expose(exposed) {
    if (!implementation_1.default.isWorkerRuntime()) {
        throw Error("expose() called in the master thread.");
    }
    if (exposeCalled) {
        throw Error("expose() called more than once. This is not possible. Pass an object to expose() if you want to expose multiple functions.");
    }
    exposeCalled = true;
    if (typeof exposed === "function") {
        implementation_1.default.subscribeToMasterMessages(messageData => {
            if (isMasterJobRunMessage(messageData) && !messageData.method) {
                runFunction(messageData.uid, exposed, messageData.args.map(common_1.deserialize));
            }
        });
        postFunctionInitMessage();
    }
    else if (typeof exposed === "object" && exposed) {
        implementation_1.default.subscribeToMasterMessages(messageData => {
            if (isMasterJobRunMessage(messageData) && messageData.method) {
                runFunction(messageData.uid, exposed[messageData.method], messageData.args.map(common_1.deserialize));
            }
        });
        const methodNames = Object.keys(exposed).filter(key => typeof exposed[key] === "function");
        postModuleInitMessage(methodNames);
    }
    else {
        throw Error(`Invalid argument passed to expose(). Expected a function or an object, got: ${exposed}`);
    }
    implementation_1.default.subscribeToMasterMessages(messageData => {
        if (isMasterJobCancelMessage(messageData)) {
            const jobUID = messageData.uid;
            const subscription = activeSubscriptions.get(jobUID);
            if (subscription) {
                subscription.unsubscribe();
                activeSubscriptions.delete(jobUID);
            }
        }
    });
}
exports.expose = expose;
if (typeof self !== "undefined" && typeof self.addEventListener === "function" && implementation_1.default.isWorkerRuntime()) {
    self.addEventListener("error", event => {
        // Post with some delay, so the master had some time to subscribe to messages
        setTimeout(() => postUncaughtErrorMessage(event.error || event), 250);
    });
    self.addEventListener("unhandledrejection", event => {
        const error = event.reason;
        if (error && typeof error.message === "string") {
            // Post with some delay, so the master had some time to subscribe to messages
            setTimeout(() => postUncaughtErrorMessage(error), 250);
        }
    });
}
if (typeof process !== "undefined" && typeof process.on === "function" && implementation_1.default.isWorkerRuntime()) {
    process.on("uncaughtException", (error) => {
        // Post with some delay, so the master had some time to subscribe to messages
        setTimeout(() => postUncaughtErrorMessage(error), 250);
    });
    process.on("unhandledRejection", (error) => {
        if (error && typeof error.message === "string") {
            // Post with some delay, so the master had some time to subscribe to messages
            setTimeout(() => postUncaughtErrorMessage(error), 250);
        }
    });
}

},{"is-observable":"UALh","../common":"ujDW","../transferable":"HnZs","../types/messages":"No47","./implementation":"Oz27","process":"pBGv"}],"g6uu":[function(require,module,exports) {
module.exports = require("./dist/worker/index")

},{"./dist/worker/index":"DwFB"}],"Slw0":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.checkIfBadgeEarned = checkIfBadgeEarned;
// /* eslint-env worker */
// import ComputedTurnResult from './computedTurnResult'
// import fetch from 'node-fetch'

// interface TestReport {
//   task_id: number // eslint-disable-line
// }

// export async function checkIfBadgeEarned(
//   badges: string,
//   result: ComputedTurnResult,
//   userCode: string,
//   gameState: any,
//   currentAvatarID: number
// ): Promise<string> {
//   // TODO: fix loading of environment variables. 
//   let serviceUrl = process.env.REACT_APP_KURONO_BADGES_URL;
//   if (serviceUrl === undefined) {
//     serviceUrl = "https://production-kurono-badges-dot-decent-digit-629.appspot.com"
//   }

//   const response = await fetch(serviceUrl, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({
//       source: { code: userCode },
//       current_avatar_id: currentAvatarID,
//       game_state: gameState
//     })
//   });

//   const responseJson: {
//     passed: TestReport[]
//     failed: TestReport[]
//     xfailed: TestReport[]
//     skipped: TestReport[]
//   } = await response.json();

//   for (let i = 0; i < responseJson.passed.length; i++) {
//     const badgeWorksheetPair = `${gameState.worksheetID}:${responseJson.passed[i].task_id}`;
//     if (!badges.includes(badgeWorksheetPair)) {
//       badges += `${badgeWorksheetPair},`
//     }
//   }

//   return badges;
// }

/* eslint-env worker */

function checkIfBadgeEarned(badges, result, userCode, gameState) {
  const userPythonCode = userCode.replace(/\s*#.*/gm, ''); // Remove all comment lines from the user's code
  const badgesPerWorksheet = [{
    id: 1,
    worksheetID: 1,
    trigger: badge1Trigger(result)
  }, {
    id: 2,
    worksheetID: 1,
    trigger: badge2Trigger(result, userPythonCode)
  }, {
    id: 3,
    worksheetID: 1,
    trigger: badge3Trigger(result, userPythonCode)
  }];
  for (const badge of badgesPerWorksheet) {
    const badgeWorksheetPair = `${badge.worksheetID}:${badge.id}`;
    if (!badges.includes(badgeWorksheetPair) && badge.worksheetID === gameState.worksheetID && badge.trigger) {
      // Here is when a new badge is earned
      // TODO on worksheet 2: This might have to order the badges, in case user does not do the worksheet in order
      badges += `${badgeWorksheetPair},`;
    }
  }
  return badges;
}
function badge1Trigger(result) {
  // Check the code returns a move action other than NORTH
  return result.action.action_type === 'move' && JSON.stringify(result.action.options.direction) !== JSON.stringify({
    x: 0,
    y: 1
  });
}
function badge2Trigger(result, userPythonCode) {
  // Check code contains keywords to move in random directions
  const substrings = ['import random', 'randint(', 'direction.NORTH', 'direction.EAST', 'direction.SOUTH', 'direction.WEST', 'if ', 'elif ', 'else:'];
  // Check the code contains certain keywords about moving in a random direction
  const codeContainsKeywords = substrings.every(substring => userPythonCode.includes(substring));

  // And check it returns a move action
  return result.action.action_type === 'move' && codeContainsKeywords;
}
function badge3Trigger(result, userPythonCode) {
  // Check the code contains certain keywords about moving to a cell
  const substrings = ['world_state.can_move_to(', 'print(', 'if '];
  const codeContainsKeywords = substrings.every(substring => userPythonCode.includes(substring));

  // And check it returns a move action
  return result.action.action_type === 'move' && codeContainsKeywords;
}
},{}],"aAPp":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.funcPattern = funcPattern;
exports.matchFromImports = matchFromImports;
exports.matchImports = matchImports;
const namePattern = '[{base}][{base}0-9]*'.replace(/{base}/g, '_a-zA-Z');
const modulePattern = '{name}(?:\\.{name})*'.replace(/{name}/g, namePattern);
function funcPattern(_ref) {
  let {
    lineStart,
    captureName,
    captureArgs
  } = _ref;
  let pattern = ' *def +{name} *\\({args}\\) *:';
  if (lineStart) pattern = '^' + pattern;

  // TODO: refine
  const argsPattern = '.*';
  pattern = pattern.replace(/{name}/g, captureName ? `(${namePattern})` : namePattern);
  pattern = pattern.replace(/{args}/g, captureArgs ? `(${argsPattern})` : argsPattern);
  return pattern;
}
function splitImports(imports) {
  return new Set(imports.split(',').map(_import => _import.trim()));
}
function matchImports(code) {
  const pattern = new RegExp(['^', '(?:{func})?'.replace(/{func}/g, funcPattern({
    lineStart: false,
    captureName: false,
    captureArgs: false
  })), ' *import +({module}(?: *, *{module})*)'.replace(/{module}/g, modulePattern), ' *(?:#.*)?', '$'].join(''), 'gm');
  const imports = new Set();
  for (const match of code.matchAll(pattern)) {
    splitImports(match[1]).forEach(_import => {
      imports.add(_import);
    });
  }
  return imports;
}
function matchFromImports(code) {
  const pattern = new RegExp(['^', '(?:{func})?'.replace(/{func}/g, funcPattern({
    lineStart: false,
    captureName: false,
    captureArgs: false
  })), ' *from +({module}) +import'.replace(/{module}/g, modulePattern), '(?: *\\(([^)]+)\\)| +({name}(?: *, *{name})*))'.replace(/{name}/g, namePattern), ' *(?:#.*)?', '$'].join(''), 'gm');
  const fromImports = {};
  for (const match of code.matchAll(pattern)) {
    let imports;
    if (match[3] === undefined) {
      // Get imports as string and remove comments.
      let importsString = match[2].replace(/#.*(\r|\n|\r\n|$)/g, '');

      // If imports have a trailing comma, remove it.
      importsString = importsString.trim();
      if (importsString.endsWith(',')) {
        importsString = importsString.slice(0, -1);
      }

      // Split imports by comma.
      imports = splitImports(importsString);

      // If any imports are invalid, don't save them.
      const importPattern = new RegExp(`^${namePattern}$`, 'gm');
      if (imports.has('') || [...imports].every(_import => importPattern.test(_import))) {
        continue;
      }
    } else {
      imports = splitImports(match[3]);
    }
    fromImports[match[1]] = imports;
  }
  return fromImports;
}
},{}],"rgp3":[function(require,module,exports) {
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.computeNextAction = computeNextAction;
exports.simplifyErrorMessageInLog = simplifyErrorMessageInLog;
exports.updateAvatarCode = updateAvatarCode;
var _worker = require("threads/worker");
var _badges = require("./badges");
var _syntax = require("./syntax");
/* eslint-env worker */

let pyodide;
function getAvatarStateFromGameState(gameState, playerAvatarID) {
  return gameState.players.find(player => player.id === playerAvatarID);
}
async function initializePyodide() {
  importScripts('https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js');
  pyodide = await loadPyodide();
  await pyodide.loadPackage(['micropip']);
  await pyodide.runPythonAsync(`
import micropip

micropip.install("${self.location.origin}/static/worker/aimmo_game_worker-0.0.0-py3-none-any.whl")
  `);
  await pyodide.runPythonAsync(`
import contextlib
import sys

from js import Object
from io import StringIO
from pyodide import to_js

from simulation import direction, location
from simulation.action import MoveAction, PickupAction, WaitAction, MoveTowardsAction, DropAction
from simulation.avatar_state import create_avatar_state
from simulation.world_map import WorldMapCreator


@contextlib.contextmanager
def capture_output(stdout=None, stderr=None):
  """Temporarily switches stdout and stderr to stringIO objects or variable."""
  old_out = sys.stdout
  old_err = sys.stderr

  if stdout is None:
      stdout = StringIO()
  if stderr is None:
      stderr = StringIO()
  sys.stdout = stdout
  sys.stderr = stderr
  yield stdout, stderr

  sys.stdout = old_out
  sys.stderr = old_err
`);
}
async function computeNextAction(gameState, playerAvatarID, gamePaused) {
  const avatarState = getAvatarStateFromGameState(gameState, playerAvatarID);
  if (gamePaused) {
    return Promise.resolve({
      action: {
        action_type: 'wait'
      },
      log: '',
      turnCount: gameState.turnCount + 1
    });
  }
  try {
    return await pyodide.runPythonAsync(`
game_state = ${JSON.stringify(gameState)}
world_map = WorldMapCreator.generate_world_map_from_game_state(game_state)
avatar_state = create_avatar_state(${JSON.stringify(avatarState)})
serialized_action = {"action_type": "wait"}
with capture_output() as output:
    action = next_turn(world_map, avatar_state)
    if action is None:
        raise Exception("Make sure you are returning an action")
    serialized_action = action.serialise()
stdout, stderr = output
logs = stdout.getvalue() + stderr.getvalue()
to_js({"action": serialized_action, "log": logs, "turnCount": game_state["turnCount"] + 1}, dict_converter=Object.fromEntries)
    `);
  } catch (error) {
    return Promise.resolve({
      action: {
        action_type: 'wait'
      },
      log: simplifyErrorMessageInLog(error.toString()),
      turnCount: gameState.turnCount + 1
    });
  }
}
function simplifyErrorMessageInLog(log) {
  const regexToFindNextTurnErrors = /.*line (\d+), in next_turn\n((?:.|\n)*)/;
  const matches = log.match(regexToFindNextTurnErrors);
  if (matches?.length >= 2) {
    // get only the exception message line, removing potential traceback
    const simpleError = matches[2].split('\n').slice(-2).join('');
    return `Uh oh! Something isn't correct on line ${matches[1]}. Here's the error we got:\n${simpleError}`;
  }
  // error not in next_turn function
  return log.split('\n').slice(-2).join('\n');
}
const IMPORT_WHITE_LIST = [{
  name: 'random',
  allowAnySubmodule: true
}];
function validateImportInWhiteList(_import, turnCount) {
  if (IMPORT_WHITE_LIST.every(_ref => {
    let {
      name,
      allowAnySubmodule
    } = _ref;
    return _import !== name || _import.startsWith(name) && !allowAnySubmodule;
  })) {
    return Promise.resolve({
      action: {
        action_type: 'wait'
      },
      log: `Import "${_import}" is not allowed.`,
      turnCount: turnCount
    });
  }
  return undefined;
}
async function updateAvatarCode(userCode, gameState) {
  let playerAvatarID = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : 0;
  let turnCount = 0;
  if (gameState) {
    turnCount = gameState.turnCount + 1;
  }
  try {
    for (const _import of (0, _syntax.matchImports)(userCode)) {
      const promise = validateImportInWhiteList(_import, turnCount);
      if (promise) return promise;
    }
    for (const _import in (0, _syntax.matchFromImports)(userCode)) {
      const promise = validateImportInWhiteList(_import, turnCount);
      if (promise) return promise;
      // TODO: validate from imports
    }

    await pyodide.runPythonAsync(userCode);
    if (gameState) {
      return computeNextAction(gameState, playerAvatarID, false);
    }
    return Promise.resolve({
      action: {
        action_type: 'wait'
      },
      log: '',
      turnCount: turnCount
    });
  } catch (error) {
    await setAvatarCodeToWaitActionOnError();
    return Promise.resolve({
      action: {
        action_type: 'wait'
      },
      log: simplifyErrorMessageInLog(error.toString()),
      turnCount: turnCount
    });
  }
}
async function setAvatarCodeToWaitActionOnError() {
  await pyodide.runPythonAsync(`def next_turn(world_map, avatar_state):
    return WaitAction()`);
}
const pyodideWorker = {
  initializePyodide,
  computeNextAction,
  updateAvatarCode,
  checkIfBadgeEarned: _badges.checkIfBadgeEarned,
  filterByWorksheet: _badges.filterByWorksheet
};
(0, _worker.expose)(pyodideWorker);
},{"threads/worker":"g6uu","./badges":"Slw0","./syntax":"aAPp"}]},{},["rgp3"], null)
//# sourceMappingURL=/static/react/webWorker.62af4eab.js.map