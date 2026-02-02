(() => {
    const origin_log = console.log;
    ;
    console_log = function () {
        return origin_log(...arguments)
    }
})();

function makeFunction(name) {
    // 动态创建一个函数
    var func = new Function(`
        return function ${name}() {
            console_log('函数传参.${name}',arguments)
        }
    `)();
    safeFunction(func)
    func.prototype = watch(func.prototype, `方法原型:${name}.prototype`)
    func = watch(func, `方法本身:${name}`)
    return func;
};
;
;


!(function () {
    watch = function (obj, name) {
        return new Proxy(obj, {
            get(target, p, receiver) {
                // 过滤没用的信息，不进行打印
                if (name)
                    if (p === "Math" || p === "Symbol" || p === "Proxy" || p === "Promise" || p === "Array" || p === "isNaN" || p === "encodeURI" || p === "Uint8Array" || p.toString().indexOf("Symbol(") != -1) {
                        var val = Reflect.get(...arguments);
                        return val
                    } else {
                        var val = Reflect.get(...arguments);

                        if (typeof val === 'function') {
                            console_log(`取值:`, name, '.', p, ` =>`, 'function');
                        } else {
                            console_log(`取值:`, name, '.', p, ` =>`, val);
                        }

                        return val
                    }
            },
            set(target, p, value, receiver) {
                var val = Reflect.set(...arguments)
                if (typeof value === 'function') {
                    console_log(`设置值:${name}.${p}=>function `,);
                } else {
                    console_log(`设置值:${name}.${p}=> `, value);
                }
                return val
            },
            has(target, key) {
                console_log(`检查属性存在性: ${name}.${key.toString()}`);
                return key in target;
            },
            ownKeys(target) {
                console_log(`ownKeys检测: ${name}`);
                return Reflect.ownKeys(...arguments)
            }
        })
    }
})();


(() => {
    Function.prototype.$call = Function.prototype.call
    const $toString = Function.toString;
    const myFunction_toString_symbol = Symbol('('.concat('', ')_'));
    const myToString = function toString() {
        return typeof this == 'function' && this[myFunction_toString_symbol] || $toString.$call(this);
    };

    function set_native(func, key, value) {
        Object.defineProperty(func, key, {
            "enumerable": false,
            "configurable": true,
            "writable": true,
            "value": value
        })
    }

    delete Function.prototype['toString'];

    set_native(Function.prototype, "toString", myToString);

    set_native(Function.prototype.toString, myFunction_toString_symbol, "function toString() { [native code] }");

    safeFunction = (func) => {
        set_native(func, myFunction_toString_symbol, `function ${func.name}() { [native code] }`);
    };
    safeFunctionDIY = (func, name) => {
        set_native(func, myFunction_toString_symbol, `function ${name}() { [native code] }`);
    };
})();
;
;


Window = function () {
    return global;
}

window = new Window();

delete global;

window.top = window;
window.self = window;

window.addEventListener = makeFunction("addEventListener")
window.removeEventListener = makeFunction("removeEventListener")
window.postMessage = makeFunction("postMessage")
window.Bluetooth = makeFunction("Bluetooth")
window.BluetoothDevice = makeFunction("BluetoothDevice")
window.BluetoothUUID = makeFunction("BluetoothUUID")
window.Document = makeFunction("Document")
window.getComputedStyle = makeFunction("getComputedStyle")
window.PerformanceEntry = makeFunction("PerformanceEntry")
window.BlobEvent = makeFunction("BlobEvent")
window.Element = makeFunction("Element")
Element.prototype.webkitMatchesSelector = makeFunction("webkitMatchesSelector")
window.webkitRTCPeerConnection = makeFunction("webkitRTCPeerConnection")
window.DOMTokenList = makeFunction("DOMTokenList")
window.PerformanceTiming = makeFunction("PerformanceTiming")
window.HTMLDocument = makeFunction("HTMLDocument")
window.HTMLMediaElement = makeFunction("HTMLMediaElement")
window.OfflineAudioContext = makeFunction("OfflineAudioContext")
window.PointerEvent = makeFunction("PointerEvent")
window.Navigator = makeFunction("Navigator")
window.alert = makeFunction("alert")
window.Screen = makeFunction("Screen")
window.MouseEvent = makeFunction("MouseEvent")
window.TouchEvent = makeFunction("TouchEvent")
window.matchMedia = function (query) {
    return {
        matches: false,
        media: query,
        onchange: null,
    }
}
window.DeviceMotionEvent = makeFunction("DeviceMotionEvent")
window.Image = makeFunction("Image")
window.WebGLRenderingContext = makeFunction("WebGLRenderingContext")

window.origin = 'https://chat.qwen.ai'

window.screenTop = 58;
window.screenLeft = -1440;
window.innerWidth = 1391;
window.innerHeight = 823;
window.outerWidth = 1440;
window.outerHeight = 960;
window.screenX = -1440
window.screenY = 58
window.devicePixelRatio = 1.5

window.chrome = watch({}, 'window.chrome')

var canvas = {
    name: '',
    getContext: function (name) {
        if (name === '' || name === '2d') {
            this.name = '2d'
            return watch({
                fillRect: makeFunction('fillRect'),
                arc: makeFunction('arc'),
                stroke: makeFunction('stroke'),
                fillText: makeFunction('fillText'),
            }, '2d')
        } else {
            return null
        }
        if (name === 'webgl') {
            if (this.name === '' || this.name === 'webgl') {
                this.name = 'webgl'
                return watch({
                    ARRAY_BUFFER: 34962,
                    STATIC_DRAW: 35044,
                    createBuffer: makeFunction('createBuffer'),
                    bindBuffer: makeFunction('bindBuffer'),
                    bufferData: makeFunction('bufferData'),
                }, 'webgl')
            } else {
                return null
            }
        }
    }
}

document = {
    currentScript: null,
    createElement: function (name) {
        if (name === 'canvas') {
            return canvas
        }
        if (name === 'audio') {
            return watch({
                canPlayType: makeFunction('canPlayType'),
            }, 'document.createElement.audio')
        }
        if (name === 'SCRIPT') {
            return watch({}, 'document.createElement.SCRIPT')
        }
        if (name === 'style') {
            return watch({}, 'document.createElement.style')
        }
        debugger

    },
    body: watch({
        clientWidth: 1391,
        clientHeight: 823,
    }, 'document.body'),
    documentElement: watch({
        clientWidth: 1391,
        clientHeight: 823,
        style: watch({
            contentVisibility: '',
        }, 'document.documentElement.style'),
    }, 'document.documentElement'),
    referrer: '',
    getElementsByTagName: function (name) {
        if (name === 'head' || name === 'HEAD') {
            return this.head
        }
        if (name === 'div') {
            return watch({
                length: 100,
            }, 'document.getElementsByTagName.div')
        }
        debugger
    },
    head: watch({
        0: watch({
            appendChild: makeFunction('appendChild'),
        }, 'document.head.0'),
        appendChild: makeFunction('appendChild'),
    }, 'document.head'),
    addEventListener: makeFunction("addEventListener"),
    hidden: false,
    wasDiscarded: false,
    querySelector: function (name) {
        return null
        debugger
    },
    createEvent: makeFunction("createEvent"),
    cookie: "",
    hasFocus: makeFunction("hasFocus"),
    visibilityState: 'visible',
}
location = {
    "ancestorOrigins": {},
    "href": "https://chat.qwen.ai/",
    "origin": "https://chat.qwen.ai",
    "protocol": "https:",
    "host": "chat.qwen.ai",
    "hostname": "chat.qwen.ai",
    "port": "",
    "pathname": "/",
    "search": "",
    "hash": ""
}
navigator = {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    platform: 'Win32',
    plugins: watch({
        "0": {
            "0": {},
            "1": {}
        },
        "1": {
            "0": {},
            "1": {}
        },
        "2": {
            "0": {},
            "1": {}
        },
        "3": {
            "0": {},
            "1": {}
        },
        "4": {
            "0": {},
            "1": {}
        },
        length: 5
    }, "navigator.plugins"),
    hardwareConcurrency: 24,
    cookieEnabled: true,
    appCodeName: 'Mozilla',
    webdriver: false,
    getBattery: makeFunction("getBattery"),
    languages: [
        "zh-CN",
        "en",
        "en-GB",
        "en-US"
    ],
    connection: watch({
        rtt: 50,
        effectiveType: '4g',
    }, 'navigator.connection'),
    appVersion: '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    maxTouchPoints: 15,
    language: 'zh-CN',
}
localStorage = {
    getItem: function (name) {
        if (name in this) {
            return this[name]
        } else {
            debugger
            return null
        }
    },
    setItem: function (name, value) {
        this[name] = value
    },
    lswusea: 'T2gArVHIe2NFGKh-iplWivdyb0Syj0WAMgcIXr5YMQxs0esIcy1072i0wGeIqDOcR2M=@@1766916265',
}

screen = {
    width: 1440,
    availWidth: 1391,
    availHeight: 912,
    height: 960,
    outerHeight: 960,
    outerWidth: 1440,
    colorDepth: 24,
    pixelDepth: 24,
}
history = {}

window = watch(window, 'window');
document = watch(document, 'document');
location = watch(location, 'location');
navigator = watch(navigator, 'navigator');
localStorage = watch(localStorage, 'localStorage');
screen = watch(screen, 'screen');
history = watch(history, 'history');

setTimeout = function () {
}
setInterval = function () {
}


window.fyglobalopt = {
    "location": "sea",
    "MaxMTLog": 20,
    "MaxNGPLog": 10,
    "MaxKSLog": 5,
    "MaxFocusLog": 3,
    "loadTime": 12,
    "timeout": 2000,
    "reqUrl": "/api/v2/chats/new"
}


require('./code')


const_int = 58
ali231 = window.ali(const_int, window.fyglobalopt)
console.log("###" + ali231 + "###");
