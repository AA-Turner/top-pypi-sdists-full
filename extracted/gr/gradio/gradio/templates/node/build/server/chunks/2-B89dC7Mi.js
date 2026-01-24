import { a, t } from './index5-BoOEKc6P.js';
import { cJ as derived, w as writable, d as get, g as getContext, f as fallback, e as escape_html, s as setContext } from './async-Mo2Ia14K.js';
import { y as snapshot, d as attr_style, g as stringify, s as store_get, e as ensure_array_like, u as unsubscribe_stores, c as bind_props, f as attr_class, k as html, a as attr, i as slot, G as element, o as attributes, j as clsx, b as spread_props, h as head } from './index-D1Ptw7Az.js';
import require$$1 from 'path';
import require$$3 from 'url';
import require$$0 from 'fs';
import { s as spring, t as tick } from './spring-DE8vsW2o.js';

var us=typeof globalThis<"u"?globalThis:typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{};function sn(e){return e&&e.__esModule&&Object.prototype.hasOwnProperty.call(e,"default")?e.default:e}var Me$2,gt$1;function an(){if(gt$1)return Me$2;gt$1=1;var e=function(m){return t(m)&&!r(m)};function t(p){return !!p&&typeof p=="object"}function r(p){var m=Object.prototype.toString.call(p);return m==="[object RegExp]"||m==="[object Date]"||i(p)}var n=typeof Symbol=="function"&&Symbol.for,o=n?Symbol.for("react.element"):60103;function i(p){return p.$$typeof===o}function s(p){return Array.isArray(p)?[]:{}}function a(p,m){return m.clone!==false&&m.isMergeableObject(p)?d(s(p),p,m):p}function h(p,m,g){return p.concat(m).map(function(H){return a(H,g)})}function c(p,m){if(!m.customMerge)return d;var g=m.customMerge(p);return typeof g=="function"?g:d}function l(p){return Object.getOwnPropertySymbols?Object.getOwnPropertySymbols(p).filter(function(m){return Object.propertyIsEnumerable.call(p,m)}):[]}function u(p){return Object.keys(p).concat(l(p))}function f(p,m){try{return m in p}catch{return  false}}function _(p,m){return f(p,m)&&!(Object.hasOwnProperty.call(p,m)&&Object.propertyIsEnumerable.call(p,m))}function P(p,m,g){var H={};return g.isMergeableObject(p)&&u(p).forEach(function(S){H[S]=a(p[S],g);}),u(m).forEach(function(S){_(p,S)||(f(p,S)&&g.isMergeableObject(m[S])?H[S]=c(S,g)(p[S],m[S],g):H[S]=a(m[S],g));}),H}function d(p,m,g){g=g||{},g.arrayMerge=g.arrayMerge||h,g.isMergeableObject=g.isMergeableObject||e,g.cloneUnlessOtherwiseSpecified=a;var H=Array.isArray(m),S=Array.isArray(p),M=H===S;return M?H?g.arrayMerge(p,m,g):P(p,m,g):a(m,g)}d.all=function(m,g){if(!Array.isArray(m))throw new Error("first argument should be an array");return m.reduce(function(H,S){return d(H,S,g)},{})};var E=d;return Me$2=E,Me$2}var cn=an();const un=sn(cn);var qe$2=function(e,t){return qe$2=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(r,n){r.__proto__=n;}||function(r,n){for(var o in n)Object.prototype.hasOwnProperty.call(n,o)&&(r[o]=n[o]);},qe$2(e,t)};function Oe$2(e,t){if(typeof t!="function"&&t!==null)throw new TypeError("Class extends value "+String(t)+" is not a constructor or null");qe$2(e,t);function r(){this.constructor=e;}e.prototype=t===null?Object.create(t):(r.prototype=t.prototype,new r);}var w$3=function(){return w$3=Object.assign||function(t){for(var r,n=1,o=arguments.length;n<o;n++){r=arguments[n];for(var i in r)Object.prototype.hasOwnProperty.call(r,i)&&(t[i]=r[i]);}return t},w$3.apply(this,arguments)};function ln(e,t){var r={};for(var n in e)Object.prototype.hasOwnProperty.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&typeof Object.getOwnPropertySymbols=="function")for(var o=0,n=Object.getOwnPropertySymbols(e);o<n.length;o++)t.indexOf(n[o])<0&&Object.prototype.propertyIsEnumerable.call(e,n[o])&&(r[n[o]]=e[n[o]]);return r}function De$2(e,t,r){if(arguments.length===2)for(var n=0,o=t.length,i;n<o;n++)(i||!(n in t))&&(i||(i=Array.prototype.slice.call(t,0,n)),i[n]=t[n]);return e.concat(i||Array.prototype.slice.call(t))}function ke$2(e,t){var r=t&&t.cache?t.cache:gn,n=t&&t.serializer?t.serializer:mn,o=t&&t.strategy?t.strategy:pn;return o(e,{cache:r,serializer:n})}function hn(e){return e==null||typeof e=="number"||typeof e=="boolean"}function fn(e,t,r,n){var o=hn(n)?n:r(n),i=t.get(o);return typeof i>"u"&&(i=e.call(this,n),t.set(o,i)),i}function Vt(e,t,r){var n=Array.prototype.slice.call(arguments,3),o=r(n),i=t.get(o);return typeof i>"u"&&(i=e.apply(this,n),t.set(o,i)),i}function Xt(e,t,r,n,o){return r.bind(t,e,n,o)}function pn(e,t){var r=e.length===1?fn:Vt;return Xt(e,this,r,t.cache.create(),t.serializer)}function dn(e,t){return Xt(e,this,Vt,t.cache.create(),t.serializer)}var mn=function(){return JSON.stringify(arguments)},_n=(function(){function e(){this.cache=Object.create(null);}return e.prototype.get=function(t){return this.cache[t]},e.prototype.set=function(t,r){this.cache[t]=r;},e})(),gn={create:function(){return new _n}},Ue$2={variadic:dn},b$2;(function(e){e[e.EXPECT_ARGUMENT_CLOSING_BRACE=1]="EXPECT_ARGUMENT_CLOSING_BRACE",e[e.EMPTY_ARGUMENT=2]="EMPTY_ARGUMENT",e[e.MALFORMED_ARGUMENT=3]="MALFORMED_ARGUMENT",e[e.EXPECT_ARGUMENT_TYPE=4]="EXPECT_ARGUMENT_TYPE",e[e.INVALID_ARGUMENT_TYPE=5]="INVALID_ARGUMENT_TYPE",e[e.EXPECT_ARGUMENT_STYLE=6]="EXPECT_ARGUMENT_STYLE",e[e.INVALID_NUMBER_SKELETON=7]="INVALID_NUMBER_SKELETON",e[e.INVALID_DATE_TIME_SKELETON=8]="INVALID_DATE_TIME_SKELETON",e[e.EXPECT_NUMBER_SKELETON=9]="EXPECT_NUMBER_SKELETON",e[e.EXPECT_DATE_TIME_SKELETON=10]="EXPECT_DATE_TIME_SKELETON",e[e.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE=11]="UNCLOSED_QUOTE_IN_ARGUMENT_STYLE",e[e.EXPECT_SELECT_ARGUMENT_OPTIONS=12]="EXPECT_SELECT_ARGUMENT_OPTIONS",e[e.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE=13]="EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE",e[e.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE=14]="INVALID_PLURAL_ARGUMENT_OFFSET_VALUE",e[e.EXPECT_SELECT_ARGUMENT_SELECTOR=15]="EXPECT_SELECT_ARGUMENT_SELECTOR",e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR=16]="EXPECT_PLURAL_ARGUMENT_SELECTOR",e[e.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT=17]="EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT",e[e.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT=18]="EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT",e[e.INVALID_PLURAL_ARGUMENT_SELECTOR=19]="INVALID_PLURAL_ARGUMENT_SELECTOR",e[e.DUPLICATE_PLURAL_ARGUMENT_SELECTOR=20]="DUPLICATE_PLURAL_ARGUMENT_SELECTOR",e[e.DUPLICATE_SELECT_ARGUMENT_SELECTOR=21]="DUPLICATE_SELECT_ARGUMENT_SELECTOR",e[e.MISSING_OTHER_CLAUSE=22]="MISSING_OTHER_CLAUSE",e[e.INVALID_TAG=23]="INVALID_TAG",e[e.INVALID_TAG_NAME=25]="INVALID_TAG_NAME",e[e.UNMATCHED_CLOSING_TAG=26]="UNMATCHED_CLOSING_TAG",e[e.UNCLOSED_TAG=27]="UNCLOSED_TAG";})(b$2||(b$2={}));var A$1;(function(e){e[e.literal=0]="literal",e[e.argument=1]="argument",e[e.number=2]="number",e[e.date=3]="date",e[e.time=4]="time",e[e.select=5]="select",e[e.plural=6]="plural",e[e.pound=7]="pound",e[e.tag=8]="tag";})(A$1||(A$1={}));var te$2;(function(e){e[e.number=0]="number",e[e.dateTime=1]="dateTime";})(te$2||(te$2={}));function bt$1(e){return e.type===A$1.literal}function bn(e){return e.type===A$1.argument}function Wt(e){return e.type===A$1.number}function Zt(e){return e.type===A$1.date}function Jt(e){return e.type===A$1.time}function Qt(e){return e.type===A$1.select}function Yt(e){return e.type===A$1.plural}function yn(e){return e.type===A$1.pound}function Kt(e){return e.type===A$1.tag}function er(e){return !!(e&&typeof e=="object"&&e.type===te$2.number)}function Ve$2(e){return !!(e&&typeof e=="object"&&e.type===te$2.dateTime)}var tr=/[ \xA0\u1680\u2000-\u200A\u202F\u205F\u3000]/,wn=/(?:[Eec]{1,6}|G{1,5}|[Qq]{1,5}|(?:[yYur]+|U{1,5})|[ML]{1,5}|d{1,2}|D{1,3}|F{1}|[abB]{1,5}|[hkHK]{1,2}|w{1,2}|W{1}|m{1,2}|s{1,2}|[zZOvVxX]{1,4})(?=([^']*'[^']*')*[^']*$)/g;function En(e){var t={};return e.replace(wn,function(r){var n=r.length;switch(r[0]){case "G":t.era=n===4?"long":n===5?"narrow":"short";break;case "y":t.year=n===2?"2-digit":"numeric";break;case "Y":case "u":case "U":case "r":throw new RangeError("`Y/u/U/r` (year) patterns are not supported, use `y` instead");case "q":case "Q":throw new RangeError("`q/Q` (quarter) patterns are not supported");case "M":case "L":t.month=["numeric","2-digit","short","long","narrow"][n-1];break;case "w":case "W":throw new RangeError("`w/W` (week) patterns are not supported");case "d":t.day=["numeric","2-digit"][n-1];break;case "D":case "F":case "g":throw new RangeError("`D/F/g` (day) patterns are not supported, use `d` instead");case "E":t.weekday=n===4?"long":n===5?"narrow":"short";break;case "e":if(n<4)throw new RangeError("`e..eee` (weekday) patterns are not supported");t.weekday=["short","long","narrow","short"][n-4];break;case "c":if(n<4)throw new RangeError("`c..ccc` (weekday) patterns are not supported");t.weekday=["short","long","narrow","short"][n-4];break;case "a":t.hour12=true;break;case "b":case "B":throw new RangeError("`b/B` (period) patterns are not supported, use `a` instead");case "h":t.hourCycle="h12",t.hour=["numeric","2-digit"][n-1];break;case "H":t.hourCycle="h23",t.hour=["numeric","2-digit"][n-1];break;case "K":t.hourCycle="h11",t.hour=["numeric","2-digit"][n-1];break;case "k":t.hourCycle="h24",t.hour=["numeric","2-digit"][n-1];break;case "j":case "J":case "C":throw new RangeError("`j/J/C` (hour) patterns are not supported, use `h/H/K/k` instead");case "m":t.minute=["numeric","2-digit"][n-1];break;case "s":t.second=["numeric","2-digit"][n-1];break;case "S":case "A":throw new RangeError("`S/A` (second) patterns are not supported, use `s` instead");case "z":t.timeZoneName=n<4?"short":"long";break;case "Z":case "O":case "v":case "V":case "X":case "x":throw new RangeError("`Z/O/v/V/X/x` (timeZone) patterns are not supported, use `z` instead")}return ""}),t}var vn=/[\t-\r \x85\u200E\u200F\u2028\u2029]/i;function xn(e){if(e.length===0)throw new Error("Number skeleton cannot be empty");for(var t=e.split(vn).filter(function(f){return f.length>0}),r=[],n=0,o=t;n<o.length;n++){var i=o[n],s=i.split("/");if(s.length===0)throw new Error("Invalid number skeleton");for(var a=s[0],h=s.slice(1),c=0,l=h;c<l.length;c++){var u=l[c];if(u.length===0)throw new Error("Invalid number skeleton")}r.push({stem:a,options:h});}return r}function Sn(e){return e.replace(/^(.*?)-/,"")}var yt$1=/^\.(?:(0+)(\*)?|(#+)|(0+)(#+))$/g,rr=/^(@+)?(\+|#+)?[rs]?$/g,Tn=/(\*)(0+)|(#+)(0+)|(0+)/g,nr=/^(0+)$/;function wt$1(e){var t={};return e[e.length-1]==="r"?t.roundingPriority="morePrecision":e[e.length-1]==="s"&&(t.roundingPriority="lessPrecision"),e.replace(rr,function(r,n,o){return typeof o!="string"?(t.minimumSignificantDigits=n.length,t.maximumSignificantDigits=n.length):o==="+"?t.minimumSignificantDigits=n.length:n[0]==="#"?t.maximumSignificantDigits=n.length:(t.minimumSignificantDigits=n.length,t.maximumSignificantDigits=n.length+(typeof o=="string"?o.length:0)),""}),t}function or(e){switch(e){case "sign-auto":return {signDisplay:"auto"};case "sign-accounting":case "()":return {currencySign:"accounting"};case "sign-always":case "+!":return {signDisplay:"always"};case "sign-accounting-always":case "()!":return {signDisplay:"always",currencySign:"accounting"};case "sign-except-zero":case "+?":return {signDisplay:"exceptZero"};case "sign-accounting-except-zero":case "()?":return {signDisplay:"exceptZero",currencySign:"accounting"};case "sign-never":case "+_":return {signDisplay:"never"}}}function An(e){var t;if(e[0]==="E"&&e[1]==="E"?(t={notation:"engineering"},e=e.slice(2)):e[0]==="E"&&(t={notation:"scientific"},e=e.slice(1)),t){var r=e.slice(0,2);if(r==="+!"?(t.signDisplay="always",e=e.slice(2)):r==="+?"&&(t.signDisplay="exceptZero",e=e.slice(2)),!nr.test(e))throw new Error("Malformed concise eng/scientific notation");t.minimumIntegerDigits=e.length;}return t}function Et$1(e){var t={},r=or(e);return r||t}function Pn(e){for(var t={},r=0,n=e;r<n.length;r++){var o=n[r];switch(o.stem){case "percent":case "%":t.style="percent";continue;case "%x100":t.style="percent",t.scale=100;continue;case "currency":t.style="currency",t.currency=o.options[0];continue;case "group-off":case ",_":t.useGrouping=false;continue;case "precision-integer":case ".":t.maximumFractionDigits=0;continue;case "measure-unit":case "unit":t.style="unit",t.unit=Sn(o.options[0]);continue;case "compact-short":case "K":t.notation="compact",t.compactDisplay="short";continue;case "compact-long":case "KK":t.notation="compact",t.compactDisplay="long";continue;case "scientific":t=w$3(w$3(w$3({},t),{notation:"scientific"}),o.options.reduce(function(h,c){return w$3(w$3({},h),Et$1(c))},{}));continue;case "engineering":t=w$3(w$3(w$3({},t),{notation:"engineering"}),o.options.reduce(function(h,c){return w$3(w$3({},h),Et$1(c))},{}));continue;case "notation-simple":t.notation="standard";continue;case "unit-width-narrow":t.currencyDisplay="narrowSymbol",t.unitDisplay="narrow";continue;case "unit-width-short":t.currencyDisplay="code",t.unitDisplay="short";continue;case "unit-width-full-name":t.currencyDisplay="name",t.unitDisplay="long";continue;case "unit-width-iso-code":t.currencyDisplay="symbol";continue;case "scale":t.scale=parseFloat(o.options[0]);continue;case "rounding-mode-floor":t.roundingMode="floor";continue;case "rounding-mode-ceiling":t.roundingMode="ceil";continue;case "rounding-mode-down":t.roundingMode="trunc";continue;case "rounding-mode-up":t.roundingMode="expand";continue;case "rounding-mode-half-even":t.roundingMode="halfEven";continue;case "rounding-mode-half-down":t.roundingMode="halfTrunc";continue;case "rounding-mode-half-up":t.roundingMode="halfExpand";continue;case "integer-width":if(o.options.length>1)throw new RangeError("integer-width stems only accept a single optional option");o.options[0].replace(Tn,function(h,c,l,u,f,_){if(c)t.minimumIntegerDigits=l.length;else {if(u&&f)throw new Error("We currently do not support maximum integer digits");if(_)throw new Error("We currently do not support exact integer digits")}return ""});continue}if(nr.test(o.stem)){t.minimumIntegerDigits=o.stem.length;continue}if(yt$1.test(o.stem)){if(o.options.length>1)throw new RangeError("Fraction-precision stems only accept a single optional option");o.stem.replace(yt$1,function(h,c,l,u,f,_){return l==="*"?t.minimumFractionDigits=c.length:u&&u[0]==="#"?t.maximumFractionDigits=u.length:f&&_?(t.minimumFractionDigits=f.length,t.maximumFractionDigits=f.length+_.length):(t.minimumFractionDigits=c.length,t.maximumFractionDigits=c.length),""});var i=o.options[0];i==="w"?t=w$3(w$3({},t),{trailingZeroDisplay:"stripIfInteger"}):i&&(t=w$3(w$3({},t),wt$1(i)));continue}if(rr.test(o.stem)){t=w$3(w$3({},t),wt$1(o.stem));continue}var s=or(o.stem);s&&(t=w$3(w$3({},t),s));var a=An(o.stem);a&&(t=w$3(w$3({},t),a));}return t}var Ee$1={"001":["H","h"],419:["h","H","hB","hb"],AC:["H","h","hb","hB"],AD:["H","hB"],AE:["h","hB","hb","H"],AF:["H","hb","hB","h"],AG:["h","hb","H","hB"],AI:["H","h","hb","hB"],AL:["h","H","hB"],AM:["H","hB"],AO:["H","hB"],AR:["h","H","hB","hb"],AS:["h","H"],AT:["H","hB"],AU:["h","hb","H","hB"],AW:["H","hB"],AX:["H"],AZ:["H","hB","h"],BA:["H","hB","h"],BB:["h","hb","H","hB"],BD:["h","hB","H"],BE:["H","hB"],BF:["H","hB"],BG:["H","hB","h"],BH:["h","hB","hb","H"],BI:["H","h"],BJ:["H","hB"],BL:["H","hB"],BM:["h","hb","H","hB"],BN:["hb","hB","h","H"],BO:["h","H","hB","hb"],BQ:["H"],BR:["H","hB"],BS:["h","hb","H","hB"],BT:["h","H"],BW:["H","h","hb","hB"],BY:["H","h"],BZ:["H","h","hb","hB"],CA:["h","hb","H","hB"],CC:["H","h","hb","hB"],CD:["hB","H"],CF:["H","h","hB"],CG:["H","hB"],CH:["H","hB","h"],CI:["H","hB"],CK:["H","h","hb","hB"],CL:["h","H","hB","hb"],CM:["H","h","hB"],CN:["H","hB","hb","h"],CO:["h","H","hB","hb"],CP:["H"],CR:["h","H","hB","hb"],CU:["h","H","hB","hb"],CV:["H","hB"],CW:["H","hB"],CX:["H","h","hb","hB"],CY:["h","H","hb","hB"],CZ:["H"],DE:["H","hB"],DG:["H","h","hb","hB"],DJ:["h","H"],DK:["H"],DM:["h","hb","H","hB"],DO:["h","H","hB","hb"],DZ:["h","hB","hb","H"],EA:["H","h","hB","hb"],EC:["h","H","hB","hb"],EE:["H","hB"],EG:["h","hB","hb","H"],EH:["h","hB","hb","H"],ER:["h","H"],ES:["H","hB","h","hb"],ET:["hB","hb","h","H"],FI:["H"],FJ:["h","hb","H","hB"],FK:["H","h","hb","hB"],FM:["h","hb","H","hB"],FO:["H","h"],FR:["H","hB"],GA:["H","hB"],GB:["H","h","hb","hB"],GD:["h","hb","H","hB"],GE:["H","hB","h"],GF:["H","hB"],GG:["H","h","hb","hB"],GH:["h","H"],GI:["H","h","hb","hB"],GL:["H","h"],GM:["h","hb","H","hB"],GN:["H","hB"],GP:["H","hB"],GQ:["H","hB","h","hb"],GR:["h","H","hb","hB"],GT:["h","H","hB","hb"],GU:["h","hb","H","hB"],GW:["H","hB"],GY:["h","hb","H","hB"],HK:["h","hB","hb","H"],HN:["h","H","hB","hb"],HR:["H","hB"],HU:["H","h"],IC:["H","h","hB","hb"],ID:["H"],IE:["H","h","hb","hB"],IL:["H","hB"],IM:["H","h","hb","hB"],IN:["h","H"],IO:["H","h","hb","hB"],IQ:["h","hB","hb","H"],IR:["hB","H"],IS:["H"],IT:["H","hB"],JE:["H","h","hb","hB"],JM:["h","hb","H","hB"],JO:["h","hB","hb","H"],JP:["H","K","h"],KE:["hB","hb","H","h"],KG:["H","h","hB","hb"],KH:["hB","h","H","hb"],KI:["h","hb","H","hB"],KM:["H","h","hB","hb"],KN:["h","hb","H","hB"],KP:["h","H","hB","hb"],KR:["h","H","hB","hb"],KW:["h","hB","hb","H"],KY:["h","hb","H","hB"],KZ:["H","hB"],LA:["H","hb","hB","h"],LB:["h","hB","hb","H"],LC:["h","hb","H","hB"],LI:["H","hB","h"],LK:["H","h","hB","hb"],LR:["h","hb","H","hB"],LS:["h","H"],LT:["H","h","hb","hB"],LU:["H","h","hB"],LV:["H","hB","hb","h"],LY:["h","hB","hb","H"],MA:["H","h","hB","hb"],MC:["H","hB"],MD:["H","hB"],ME:["H","hB","h"],MF:["H","hB"],MG:["H","h"],MH:["h","hb","H","hB"],MK:["H","h","hb","hB"],ML:["H"],MM:["hB","hb","H","h"],MN:["H","h","hb","hB"],MO:["h","hB","hb","H"],MP:["h","hb","H","hB"],MQ:["H","hB"],MR:["h","hB","hb","H"],MS:["H","h","hb","hB"],MT:["H","h"],MU:["H","h"],MV:["H","h"],MW:["h","hb","H","hB"],MX:["h","H","hB","hb"],MY:["hb","hB","h","H"],MZ:["H","hB"],NA:["h","H","hB","hb"],NC:["H","hB"],NE:["H"],NF:["H","h","hb","hB"],NG:["H","h","hb","hB"],NI:["h","H","hB","hb"],NL:["H","hB"],NO:["H","h"],NP:["H","h","hB"],NR:["H","h","hb","hB"],NU:["H","h","hb","hB"],NZ:["h","hb","H","hB"],OM:["h","hB","hb","H"],PA:["h","H","hB","hb"],PE:["h","H","hB","hb"],PF:["H","h","hB"],PG:["h","H"],PH:["h","hB","hb","H"],PK:["h","hB","H"],PL:["H","h"],PM:["H","hB"],PN:["H","h","hb","hB"],PR:["h","H","hB","hb"],PS:["h","hB","hb","H"],PT:["H","hB"],PW:["h","H"],PY:["h","H","hB","hb"],QA:["h","hB","hb","H"],RE:["H","hB"],RO:["H","hB"],RS:["H","hB","h"],RU:["H"],RW:["H","h"],SA:["h","hB","hb","H"],SB:["h","hb","H","hB"],SC:["H","h","hB"],SD:["h","hB","hb","H"],SE:["H"],SG:["h","hb","H","hB"],SH:["H","h","hb","hB"],SI:["H","hB"],SJ:["H"],SK:["H"],SL:["h","hb","H","hB"],SM:["H","h","hB"],SN:["H","h","hB"],SO:["h","H"],SR:["H","hB"],SS:["h","hb","H","hB"],ST:["H","hB"],SV:["h","H","hB","hb"],SX:["H","h","hb","hB"],SY:["h","hB","hb","H"],SZ:["h","hb","H","hB"],TA:["H","h","hb","hB"],TC:["h","hb","H","hB"],TD:["h","H","hB"],TF:["H","h","hB"],TG:["H","hB"],TH:["H","h"],TJ:["H","h"],TL:["H","hB","hb","h"],TM:["H","h"],TN:["h","hB","hb","H"],TO:["h","H"],TR:["H","hB"],TT:["h","hb","H","hB"],TW:["hB","hb","h","H"],TZ:["hB","hb","H","h"],UA:["H","hB","h"],UG:["hB","hb","H","h"],UM:["h","hb","H","hB"],US:["h","hb","H","hB"],UY:["h","H","hB","hb"],UZ:["H","hB","h"],VA:["H","h","hB"],VC:["h","hb","H","hB"],VE:["h","H","hB","hb"],VG:["h","hb","H","hB"],VI:["h","hb","H","hB"],VN:["H","h"],VU:["h","H"],WF:["H","hB"],WS:["h","H"],XK:["H","hB","h"],YE:["h","hB","hb","H"],YT:["H","hB"],ZA:["H","h","hb","hB"],ZM:["h","hb","H","hB"],ZW:["H","h"],"af-ZA":["H","h","hB","hb"],"ar-001":["h","hB","hb","H"],"ca-ES":["H","h","hB"],"en-001":["h","hb","H","hB"],"en-HK":["h","hb","H","hB"],"en-IL":["H","h","hb","hB"],"en-MY":["h","hb","H","hB"],"es-BR":["H","h","hB","hb"],"es-ES":["H","h","hB","hb"],"es-GQ":["H","h","hB","hb"],"fr-CA":["H","h","hB"],"gl-ES":["H","h","hB"],"gu-IN":["hB","hb","h","H"],"hi-IN":["hB","h","H"],"it-CH":["H","h","hB"],"it-IT":["H","h","hB"],"kn-IN":["hB","h","H"],"ml-IN":["hB","h","H"],"mr-IN":["hB","hb","h","H"],"pa-IN":["hB","hb","h","H"],"ta-IN":["hB","h","hb","H"],"te-IN":["hB","h","H"],"zu-ZA":["H","hB","hb","h"]};function Hn(e,t){for(var r="",n=0;n<e.length;n++){var o=e.charAt(n);if(o==="j"){for(var i=0;n+1<e.length&&e.charAt(n+1)===o;)i++,n++;var s=1+(i&1),a=i<2?1:3+(i>>1),h="a",c=On(t);for((c=="H"||c=="k")&&(a=0);a-- >0;)r+=h;for(;s-- >0;)r=c+r;}else o==="J"?r+="H":r+=o;}return r}function On(e){var t=e.hourCycle;if(t===void 0&&e.hourCycles&&e.hourCycles.length&&(t=e.hourCycles[0]),t)switch(t){case "h24":return "k";case "h23":return "H";case "h12":return "h";case "h11":return "K";default:throw new Error("Invalid hourCycle")}var r=e.language,n;r!=="root"&&(n=e.maximize().region);var o=Ee$1[n||""]||Ee$1[r||""]||Ee$1["".concat(r,"-001")]||Ee$1["001"];return o[0]}var je$2,Bn=new RegExp("^".concat(tr.source,"*")),Cn=new RegExp("".concat(tr.source,"*$"));function y$4(e,t){return {start:e,end:t}}var Nn=!!String.prototype.startsWith&&"_a".startsWith("a",1),In=!!String.fromCodePoint,Ln=!!Object.fromEntries,Rn=!!String.prototype.codePointAt,Mn=!!String.prototype.trimStart,Dn=!!String.prototype.trimEnd,kn=!!Number.isSafeInteger,Un=kn?Number.isSafeInteger:function(e){return typeof e=="number"&&isFinite(e)&&Math.floor(e)===e&&Math.abs(e)<=9007199254740991},Xe$1=true;try{var jn=sr("([^\\p{White_Space}\\p{Pattern_Syntax}]*)","yu");Xe$1=((je$2=jn.exec("a"))===null||je$2===void 0?void 0:je$2[0])==="a";}catch{Xe$1=false;}var vt$1=Nn?function(t,r,n){return t.startsWith(r,n)}:function(t,r,n){return t.slice(n,n+r.length)===r},We$1=In?String.fromCodePoint:function(){for(var t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];for(var n="",o=t.length,i=0,s;o>i;){if(s=t[i++],s>1114111)throw RangeError(s+" is not a valid code point");n+=s<65536?String.fromCharCode(s):String.fromCharCode(((s-=65536)>>10)+55296,s%1024+56320);}return n},xt$1=Ln?Object.fromEntries:function(t){for(var r={},n=0,o=t;n<o.length;n++){var i=o[n],s=i[0],a=i[1];r[s]=a;}return r},ir=Rn?function(t,r){return t.codePointAt(r)}:function(t,r){var n=t.length;if(!(r<0||r>=n)){var o=t.charCodeAt(r),i;return o<55296||o>56319||r+1===n||(i=t.charCodeAt(r+1))<56320||i>57343?o:(o-55296<<10)+(i-56320)+65536}},$n=Mn?function(t){return t.trimStart()}:function(t){return t.replace(Bn,"")},Gn=Dn?function(t){return t.trimEnd()}:function(t){return t.replace(Cn,"")};function sr(e,t){return new RegExp(e,t)}var Ze$2;if(Xe$1){var St$1=sr("([^\\p{White_Space}\\p{Pattern_Syntax}]*)","yu");Ze$2=function(t,r){var n;St$1.lastIndex=r;var o=St$1.exec(t);return (n=o[1])!==null&&n!==void 0?n:""};}else Ze$2=function(t,r){for(var n=[];;){var o=ir(t,r);if(o===void 0||ar(o)||Vn(o))break;n.push(o),r+=o>=65536?2:1;}return We$1.apply(void 0,n)};var Fn=(function(){function e(t,r){r===void 0&&(r={}),this.message=t,this.position={offset:0,line:1,column:1},this.ignoreTag=!!r.ignoreTag,this.locale=r.locale,this.requiresOtherClause=!!r.requiresOtherClause,this.shouldParseSkeletons=!!r.shouldParseSkeletons;}return e.prototype.parse=function(){if(this.offset()!==0)throw Error("parser can only be used once");return this.parseMessage(0,"",false)},e.prototype.parseMessage=function(t,r,n){for(var o=[];!this.isEOF();){var i=this.char();if(i===123){var s=this.parseArgument(t,n);if(s.err)return s;o.push(s.val);}else {if(i===125&&t>0)break;if(i===35&&(r==="plural"||r==="selectordinal")){var a=this.clonePosition();this.bump(),o.push({type:A$1.pound,location:y$4(a,this.clonePosition())});}else if(i===60&&!this.ignoreTag&&this.peek()===47){if(n)break;return this.error(b$2.UNMATCHED_CLOSING_TAG,y$4(this.clonePosition(),this.clonePosition()))}else if(i===60&&!this.ignoreTag&&Je$1(this.peek()||0)){var s=this.parseTag(t,r);if(s.err)return s;o.push(s.val);}else {var s=this.parseLiteral(t,r);if(s.err)return s;o.push(s.val);}}}return {val:o,err:null}},e.prototype.parseTag=function(t,r){var n=this.clonePosition();this.bump();var o=this.parseTagName();if(this.bumpSpace(),this.bumpIf("/>"))return {val:{type:A$1.literal,value:"<".concat(o,"/>"),location:y$4(n,this.clonePosition())},err:null};if(this.bumpIf(">")){var i=this.parseMessage(t+1,r,true);if(i.err)return i;var s=i.val,a=this.clonePosition();if(this.bumpIf("</")){if(this.isEOF()||!Je$1(this.char()))return this.error(b$2.INVALID_TAG,y$4(a,this.clonePosition()));var h=this.clonePosition(),c=this.parseTagName();return o!==c?this.error(b$2.UNMATCHED_CLOSING_TAG,y$4(h,this.clonePosition())):(this.bumpSpace(),this.bumpIf(">")?{val:{type:A$1.tag,value:o,children:s,location:y$4(n,this.clonePosition())},err:null}:this.error(b$2.INVALID_TAG,y$4(a,this.clonePosition())))}else return this.error(b$2.UNCLOSED_TAG,y$4(n,this.clonePosition()))}else return this.error(b$2.INVALID_TAG,y$4(n,this.clonePosition()))},e.prototype.parseTagName=function(){var t=this.offset();for(this.bump();!this.isEOF()&&qn(this.char());)this.bump();return this.message.slice(t,this.offset())},e.prototype.parseLiteral=function(t,r){for(var n=this.clonePosition(),o="";;){var i=this.tryParseQuote(r);if(i){o+=i;continue}var s=this.tryParseUnquoted(t,r);if(s){o+=s;continue}var a=this.tryParseLeftAngleBracket();if(a){o+=a;continue}break}var h=y$4(n,this.clonePosition());return {val:{type:A$1.literal,value:o,location:h},err:null}},e.prototype.tryParseLeftAngleBracket=function(){return !this.isEOF()&&this.char()===60&&(this.ignoreTag||!zn(this.peek()||0))?(this.bump(),"<"):null},e.prototype.tryParseQuote=function(t){if(this.isEOF()||this.char()!==39)return null;switch(this.peek()){case 39:return this.bump(),this.bump(),"'";case 123:case 60:case 62:case 125:break;case 35:if(t==="plural"||t==="selectordinal")break;return null;default:return null}this.bump();var r=[this.char()];for(this.bump();!this.isEOF();){var n=this.char();if(n===39)if(this.peek()===39)r.push(39),this.bump();else {this.bump();break}else r.push(n);this.bump();}return We$1.apply(void 0,r)},e.prototype.tryParseUnquoted=function(t,r){if(this.isEOF())return null;var n=this.char();return n===60||n===123||n===35&&(r==="plural"||r==="selectordinal")||n===125&&t>0?null:(this.bump(),We$1(n))},e.prototype.parseArgument=function(t,r){var n=this.clonePosition();if(this.bump(),this.bumpSpace(),this.isEOF())return this.error(b$2.EXPECT_ARGUMENT_CLOSING_BRACE,y$4(n,this.clonePosition()));if(this.char()===125)return this.bump(),this.error(b$2.EMPTY_ARGUMENT,y$4(n,this.clonePosition()));var o=this.parseIdentifierIfPossible().value;if(!o)return this.error(b$2.MALFORMED_ARGUMENT,y$4(n,this.clonePosition()));if(this.bumpSpace(),this.isEOF())return this.error(b$2.EXPECT_ARGUMENT_CLOSING_BRACE,y$4(n,this.clonePosition()));switch(this.char()){case 125:return this.bump(),{val:{type:A$1.argument,value:o,location:y$4(n,this.clonePosition())},err:null};case 44:return this.bump(),this.bumpSpace(),this.isEOF()?this.error(b$2.EXPECT_ARGUMENT_CLOSING_BRACE,y$4(n,this.clonePosition())):this.parseArgumentOptions(t,r,o,n);default:return this.error(b$2.MALFORMED_ARGUMENT,y$4(n,this.clonePosition()))}},e.prototype.parseIdentifierIfPossible=function(){var t=this.clonePosition(),r=this.offset(),n=Ze$2(this.message,r),o=r+n.length;this.bumpTo(o);var i=this.clonePosition(),s=y$4(t,i);return {value:n,location:s}},e.prototype.parseArgumentOptions=function(t,r,n,o){var i,s=this.clonePosition(),a=this.parseIdentifierIfPossible().value,h=this.clonePosition();switch(a){case "":return this.error(b$2.EXPECT_ARGUMENT_TYPE,y$4(s,h));case "number":case "date":case "time":{this.bumpSpace();var c=null;if(this.bumpIf(",")){this.bumpSpace();var l=this.clonePosition(),u=this.parseSimpleArgStyleIfPossible();if(u.err)return u;var f=Gn(u.val);if(f.length===0)return this.error(b$2.EXPECT_ARGUMENT_STYLE,y$4(this.clonePosition(),this.clonePosition()));var _=y$4(l,this.clonePosition());c={style:f,styleLocation:_};}var P=this.tryParseArgumentClose(o);if(P.err)return P;var d=y$4(o,this.clonePosition());if(c&&vt$1(c?.style,"::",0)){var E=$n(c.style.slice(2));if(a==="number"){var u=this.parseNumberSkeletonFromString(E,c.styleLocation);return u.err?u:{val:{type:A$1.number,value:n,location:d,style:u.val},err:null}}else {if(E.length===0)return this.error(b$2.EXPECT_DATE_TIME_SKELETON,d);var p=E;this.locale&&(p=Hn(E,this.locale));var f={type:te$2.dateTime,pattern:p,location:c.styleLocation,parsedOptions:this.shouldParseSkeletons?En(p):{}},m=a==="date"?A$1.date:A$1.time;return {val:{type:m,value:n,location:d,style:f},err:null}}}return {val:{type:a==="number"?A$1.number:a==="date"?A$1.date:A$1.time,value:n,location:d,style:(i=c?.style)!==null&&i!==void 0?i:null},err:null}}case "plural":case "selectordinal":case "select":{var g=this.clonePosition();if(this.bumpSpace(),!this.bumpIf(","))return this.error(b$2.EXPECT_SELECT_ARGUMENT_OPTIONS,y$4(g,w$3({},g)));this.bumpSpace();var H=this.parseIdentifierIfPossible(),S=0;if(a!=="select"&&H.value==="offset"){if(!this.bumpIf(":"))return this.error(b$2.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE,y$4(this.clonePosition(),this.clonePosition()));this.bumpSpace();var u=this.tryParseDecimalInteger(b$2.EXPECT_PLURAL_ARGUMENT_OFFSET_VALUE,b$2.INVALID_PLURAL_ARGUMENT_OFFSET_VALUE);if(u.err)return u;this.bumpSpace(),H=this.parseIdentifierIfPossible(),S=u.val;}var M=this.tryParsePluralOrSelectOptions(t,a,r,H);if(M.err)return M;var P=this.tryParseArgumentClose(o);if(P.err)return P;var ge=y$4(o,this.clonePosition());return a==="select"?{val:{type:A$1.select,value:n,options:xt$1(M.val),location:ge},err:null}:{val:{type:A$1.plural,value:n,options:xt$1(M.val),offset:S,pluralType:a==="plural"?"cardinal":"ordinal",location:ge},err:null}}default:return this.error(b$2.INVALID_ARGUMENT_TYPE,y$4(s,h))}},e.prototype.tryParseArgumentClose=function(t){return this.isEOF()||this.char()!==125?this.error(b$2.EXPECT_ARGUMENT_CLOSING_BRACE,y$4(t,this.clonePosition())):(this.bump(),{val:true,err:null})},e.prototype.parseSimpleArgStyleIfPossible=function(){for(var t=0,r=this.clonePosition();!this.isEOF();){var n=this.char();switch(n){case 39:{this.bump();var o=this.clonePosition();if(!this.bumpUntil("'"))return this.error(b$2.UNCLOSED_QUOTE_IN_ARGUMENT_STYLE,y$4(o,this.clonePosition()));this.bump();break}case 123:{t+=1,this.bump();break}case 125:{if(t>0)t-=1;else return {val:this.message.slice(r.offset,this.offset()),err:null};break}default:this.bump();break}}return {val:this.message.slice(r.offset,this.offset()),err:null}},e.prototype.parseNumberSkeletonFromString=function(t,r){var n=[];try{n=xn(t);}catch{return this.error(b$2.INVALID_NUMBER_SKELETON,r)}return {val:{type:te$2.number,tokens:n,location:r,parsedOptions:this.shouldParseSkeletons?Pn(n):{}},err:null}},e.prototype.tryParsePluralOrSelectOptions=function(t,r,n,o){for(var i,s=false,a=[],h=new Set,c=o.value,l=o.location;;){if(c.length===0){var u=this.clonePosition();if(r!=="select"&&this.bumpIf("=")){var f=this.tryParseDecimalInteger(b$2.EXPECT_PLURAL_ARGUMENT_SELECTOR,b$2.INVALID_PLURAL_ARGUMENT_SELECTOR);if(f.err)return f;l=y$4(u,this.clonePosition()),c=this.message.slice(u.offset,this.offset());}else break}if(h.has(c))return this.error(r==="select"?b$2.DUPLICATE_SELECT_ARGUMENT_SELECTOR:b$2.DUPLICATE_PLURAL_ARGUMENT_SELECTOR,l);c==="other"&&(s=true),this.bumpSpace();var _=this.clonePosition();if(!this.bumpIf("{"))return this.error(r==="select"?b$2.EXPECT_SELECT_ARGUMENT_SELECTOR_FRAGMENT:b$2.EXPECT_PLURAL_ARGUMENT_SELECTOR_FRAGMENT,y$4(this.clonePosition(),this.clonePosition()));var P=this.parseMessage(t+1,r,n);if(P.err)return P;var d=this.tryParseArgumentClose(_);if(d.err)return d;a.push([c,{value:P.val,location:y$4(_,this.clonePosition())}]),h.add(c),this.bumpSpace(),i=this.parseIdentifierIfPossible(),c=i.value,l=i.location;}return a.length===0?this.error(r==="select"?b$2.EXPECT_SELECT_ARGUMENT_SELECTOR:b$2.EXPECT_PLURAL_ARGUMENT_SELECTOR,y$4(this.clonePosition(),this.clonePosition())):this.requiresOtherClause&&!s?this.error(b$2.MISSING_OTHER_CLAUSE,y$4(this.clonePosition(),this.clonePosition())):{val:a,err:null}},e.prototype.tryParseDecimalInteger=function(t,r){var n=1,o=this.clonePosition();this.bumpIf("+")||this.bumpIf("-")&&(n=-1);for(var i=false,s=0;!this.isEOF();){var a=this.char();if(a>=48&&a<=57)i=true,s=s*10+(a-48),this.bump();else break}var h=y$4(o,this.clonePosition());return i?(s*=n,Un(s)?{val:s,err:null}:this.error(r,h)):this.error(t,h)},e.prototype.offset=function(){return this.position.offset},e.prototype.isEOF=function(){return this.offset()===this.message.length},e.prototype.clonePosition=function(){return {offset:this.position.offset,line:this.position.line,column:this.position.column}},e.prototype.char=function(){var t=this.position.offset;if(t>=this.message.length)throw Error("out of bound");var r=ir(this.message,t);if(r===void 0)throw Error("Offset ".concat(t," is at invalid UTF-16 code unit boundary"));return r},e.prototype.error=function(t,r){return {val:null,err:{kind:t,message:this.message,location:r}}},e.prototype.bump=function(){if(!this.isEOF()){var t=this.char();t===10?(this.position.line+=1,this.position.column=1,this.position.offset+=1):(this.position.column+=1,this.position.offset+=t<65536?1:2);}},e.prototype.bumpIf=function(t){if(vt$1(this.message,t,this.offset())){for(var r=0;r<t.length;r++)this.bump();return  true}return  false},e.prototype.bumpUntil=function(t){var r=this.offset(),n=this.message.indexOf(t,r);return n>=0?(this.bumpTo(n),true):(this.bumpTo(this.message.length),false)},e.prototype.bumpTo=function(t){if(this.offset()>t)throw Error("targetOffset ".concat(t," must be greater than or equal to the current offset ").concat(this.offset()));for(t=Math.min(t,this.message.length);;){var r=this.offset();if(r===t)break;if(r>t)throw Error("targetOffset ".concat(t," is at invalid UTF-16 code unit boundary"));if(this.bump(),this.isEOF())break}},e.prototype.bumpSpace=function(){for(;!this.isEOF()&&ar(this.char());)this.bump();},e.prototype.peek=function(){if(this.isEOF())return null;var t=this.char(),r=this.offset(),n=this.message.charCodeAt(r+(t>=65536?2:1));return n??null},e})();function Je$1(e){return e>=97&&e<=122||e>=65&&e<=90}function zn(e){return Je$1(e)||e===47}function qn(e){return e===45||e===46||e>=48&&e<=57||e===95||e>=97&&e<=122||e>=65&&e<=90||e==183||e>=192&&e<=214||e>=216&&e<=246||e>=248&&e<=893||e>=895&&e<=8191||e>=8204&&e<=8205||e>=8255&&e<=8256||e>=8304&&e<=8591||e>=11264&&e<=12271||e>=12289&&e<=55295||e>=63744&&e<=64975||e>=65008&&e<=65533||e>=65536&&e<=983039}function ar(e){return e>=9&&e<=13||e===32||e===133||e>=8206&&e<=8207||e===8232||e===8233}function Vn(e){return e>=33&&e<=35||e===36||e>=37&&e<=39||e===40||e===41||e===42||e===43||e===44||e===45||e>=46&&e<=47||e>=58&&e<=59||e>=60&&e<=62||e>=63&&e<=64||e===91||e===92||e===93||e===94||e===96||e===123||e===124||e===125||e===126||e===161||e>=162&&e<=165||e===166||e===167||e===169||e===171||e===172||e===174||e===176||e===177||e===182||e===187||e===191||e===215||e===247||e>=8208&&e<=8213||e>=8214&&e<=8215||e===8216||e===8217||e===8218||e>=8219&&e<=8220||e===8221||e===8222||e===8223||e>=8224&&e<=8231||e>=8240&&e<=8248||e===8249||e===8250||e>=8251&&e<=8254||e>=8257&&e<=8259||e===8260||e===8261||e===8262||e>=8263&&e<=8273||e===8274||e===8275||e>=8277&&e<=8286||e>=8592&&e<=8596||e>=8597&&e<=8601||e>=8602&&e<=8603||e>=8604&&e<=8607||e===8608||e>=8609&&e<=8610||e===8611||e>=8612&&e<=8613||e===8614||e>=8615&&e<=8621||e===8622||e>=8623&&e<=8653||e>=8654&&e<=8655||e>=8656&&e<=8657||e===8658||e===8659||e===8660||e>=8661&&e<=8691||e>=8692&&e<=8959||e>=8960&&e<=8967||e===8968||e===8969||e===8970||e===8971||e>=8972&&e<=8991||e>=8992&&e<=8993||e>=8994&&e<=9e3||e===9001||e===9002||e>=9003&&e<=9083||e===9084||e>=9085&&e<=9114||e>=9115&&e<=9139||e>=9140&&e<=9179||e>=9180&&e<=9185||e>=9186&&e<=9254||e>=9255&&e<=9279||e>=9280&&e<=9290||e>=9291&&e<=9311||e>=9472&&e<=9654||e===9655||e>=9656&&e<=9664||e===9665||e>=9666&&e<=9719||e>=9720&&e<=9727||e>=9728&&e<=9838||e===9839||e>=9840&&e<=10087||e===10088||e===10089||e===10090||e===10091||e===10092||e===10093||e===10094||e===10095||e===10096||e===10097||e===10098||e===10099||e===10100||e===10101||e>=10132&&e<=10175||e>=10176&&e<=10180||e===10181||e===10182||e>=10183&&e<=10213||e===10214||e===10215||e===10216||e===10217||e===10218||e===10219||e===10220||e===10221||e===10222||e===10223||e>=10224&&e<=10239||e>=10240&&e<=10495||e>=10496&&e<=10626||e===10627||e===10628||e===10629||e===10630||e===10631||e===10632||e===10633||e===10634||e===10635||e===10636||e===10637||e===10638||e===10639||e===10640||e===10641||e===10642||e===10643||e===10644||e===10645||e===10646||e===10647||e===10648||e>=10649&&e<=10711||e===10712||e===10713||e===10714||e===10715||e>=10716&&e<=10747||e===10748||e===10749||e>=10750&&e<=11007||e>=11008&&e<=11055||e>=11056&&e<=11076||e>=11077&&e<=11078||e>=11079&&e<=11084||e>=11085&&e<=11123||e>=11124&&e<=11125||e>=11126&&e<=11157||e===11158||e>=11159&&e<=11263||e>=11776&&e<=11777||e===11778||e===11779||e===11780||e===11781||e>=11782&&e<=11784||e===11785||e===11786||e===11787||e===11788||e===11789||e>=11790&&e<=11798||e===11799||e>=11800&&e<=11801||e===11802||e===11803||e===11804||e===11805||e>=11806&&e<=11807||e===11808||e===11809||e===11810||e===11811||e===11812||e===11813||e===11814||e===11815||e===11816||e===11817||e>=11818&&e<=11822||e===11823||e>=11824&&e<=11833||e>=11834&&e<=11835||e>=11836&&e<=11839||e===11840||e===11841||e===11842||e>=11843&&e<=11855||e>=11856&&e<=11857||e===11858||e>=11859&&e<=11903||e>=12289&&e<=12291||e===12296||e===12297||e===12298||e===12299||e===12300||e===12301||e===12302||e===12303||e===12304||e===12305||e>=12306&&e<=12307||e===12308||e===12309||e===12310||e===12311||e===12312||e===12313||e===12314||e===12315||e===12316||e===12317||e>=12318&&e<=12319||e===12320||e===12336||e===64830||e===64831||e>=65093&&e<=65094}function Qe$1(e){e.forEach(function(t){if(delete t.location,Qt(t)||Yt(t))for(var r in t.options)delete t.options[r].location,Qe$1(t.options[r].value);else Wt(t)&&er(t.style)||(Zt(t)||Jt(t))&&Ve$2(t.style)?delete t.style.location:Kt(t)&&Qe$1(t.children);});}function Xn(e,t){t===void 0&&(t={}),t=w$3({shouldParseSkeletons:true,requiresOtherClause:true},t);var r=new Fn(e,t).parse();if(r.err){var n=SyntaxError(b$2[r.err.kind]);throw n.location=r.err.location,n.originalMessage=r.err.message,n}return t?.captureLocation||Qe$1(r.val),r.val}var re$3;(function(e){e.MISSING_VALUE="MISSING_VALUE",e.INVALID_VALUE="INVALID_VALUE",e.MISSING_INTL_API="MISSING_INTL_API";})(re$3||(re$3={}));var Be$2=(function(e){Oe$2(t,e);function t(r,n,o){var i=e.call(this,r)||this;return i.code=n,i.originalMessage=o,i}return t.prototype.toString=function(){return "[formatjs Error: ".concat(this.code,"] ").concat(this.message)},t})(Error),Tt$2=(function(e){Oe$2(t,e);function t(r,n,o,i){return e.call(this,'Invalid values for "'.concat(r,'": "').concat(n,'". Options are "').concat(Object.keys(o).join('", "'),'"'),re$3.INVALID_VALUE,i)||this}return t})(Be$2),Wn=(function(e){Oe$2(t,e);function t(r,n,o){return e.call(this,'Value for "'.concat(r,'" must be of type ').concat(n),re$3.INVALID_VALUE,o)||this}return t})(Be$2),Zn=(function(e){Oe$2(t,e);function t(r,n){return e.call(this,'The intl string context variable "'.concat(r,'" was not provided to the string "').concat(n,'"'),re$3.MISSING_VALUE,n)||this}return t})(Be$2),C$2;(function(e){e[e.literal=0]="literal",e[e.object=1]="object";})(C$2||(C$2={}));function Jn(e){return e.length<2?e:e.reduce(function(t,r){var n=t[t.length-1];return !n||n.type!==C$2.literal||r.type!==C$2.literal?t.push(r):n.value+=r.value,t},[])}function Qn(e){return typeof e=="function"}function xe$2(e,t,r,n,o,i,s){if(e.length===1&&bt$1(e[0]))return [{type:C$2.literal,value:e[0].value}];for(var a=[],h=0,c=e;h<c.length;h++){var l=c[h];if(bt$1(l)){a.push({type:C$2.literal,value:l.value});continue}if(yn(l)){typeof i=="number"&&a.push({type:C$2.literal,value:r.getNumberFormat(t).format(i)});continue}var u=l.value;if(!(o&&u in o))throw new Zn(u,s);var f=o[u];if(bn(l)){(!f||typeof f=="string"||typeof f=="number")&&(f=typeof f=="string"||typeof f=="number"?String(f):""),a.push({type:typeof f=="string"?C$2.literal:C$2.object,value:f});continue}if(Zt(l)){var _=typeof l.style=="string"?n.date[l.style]:Ve$2(l.style)?l.style.parsedOptions:void 0;a.push({type:C$2.literal,value:r.getDateTimeFormat(t,_).format(f)});continue}if(Jt(l)){var _=typeof l.style=="string"?n.time[l.style]:Ve$2(l.style)?l.style.parsedOptions:n.time.medium;a.push({type:C$2.literal,value:r.getDateTimeFormat(t,_).format(f)});continue}if(Wt(l)){var _=typeof l.style=="string"?n.number[l.style]:er(l.style)?l.style.parsedOptions:void 0;_&&_.scale&&(f=f*(_.scale||1)),a.push({type:C$2.literal,value:r.getNumberFormat(t,_).format(f)});continue}if(Kt(l)){var P=l.children,d=l.value,E=o[d];if(!Qn(E))throw new Wn(d,"function",s);var p=xe$2(P,t,r,n,o,i),m=E(p.map(function(S){return S.value}));Array.isArray(m)||(m=[m]),a.push.apply(a,m.map(function(S){return {type:typeof S=="string"?C$2.literal:C$2.object,value:S}}));}if(Qt(l)){var g=l.options[f]||l.options.other;if(!g)throw new Tt$2(l.value,f,Object.keys(l.options),s);a.push.apply(a,xe$2(g.value,t,r,n,o));continue}if(Yt(l)){var g=l.options["=".concat(f)];if(!g){if(!Intl.PluralRules)throw new Be$2(`Intl.PluralRules is not available in this environment.
Try polyfilling it using "@formatjs/intl-pluralrules"
`,re$3.MISSING_INTL_API,s);var H=r.getPluralRules(t,{type:l.pluralType}).select(f-(l.offset||0));g=l.options[H]||l.options.other;}if(!g)throw new Tt$2(l.value,f,Object.keys(l.options),s);a.push.apply(a,xe$2(g.value,t,r,n,o,f-(l.offset||0)));continue}}return Jn(a)}function Yn(e,t){return t?w$3(w$3(w$3({},e||{}),t||{}),Object.keys(e).reduce(function(r,n){return r[n]=w$3(w$3({},e[n]),t[n]||{}),r},{})):e}function Kn(e,t){return t?Object.keys(e).reduce(function(r,n){return r[n]=Yn(e[n],t[n]),r},w$3({},e)):e}function $e$1(e){return {create:function(){return {get:function(t){return e[t]},set:function(t,r){e[t]=r;}}}}}function eo(e){return e===void 0&&(e={number:{},dateTime:{},pluralRules:{}}),{getNumberFormat:ke$2(function(){for(var t,r=[],n=0;n<arguments.length;n++)r[n]=arguments[n];return new((t=Intl.NumberFormat).bind.apply(t,De$2([void 0],r,false)))},{cache:$e$1(e.number),strategy:Ue$2.variadic}),getDateTimeFormat:ke$2(function(){for(var t,r=[],n=0;n<arguments.length;n++)r[n]=arguments[n];return new((t=Intl.DateTimeFormat).bind.apply(t,De$2([void 0],r,false)))},{cache:$e$1(e.dateTime),strategy:Ue$2.variadic}),getPluralRules:ke$2(function(){for(var t,r=[],n=0;n<arguments.length;n++)r[n]=arguments[n];return new((t=Intl.PluralRules).bind.apply(t,De$2([void 0],r,false)))},{cache:$e$1(e.pluralRules),strategy:Ue$2.variadic})}}var cr=(function(){function e(t,r,n,o){r===void 0&&(r=e.defaultLocale);var i=this;if(this.formatterCache={number:{},dateTime:{},pluralRules:{}},this.format=function(h){var c=i.formatToParts(h);if(c.length===1)return c[0].value;var l=c.reduce(function(u,f){return !u.length||f.type!==C$2.literal||typeof u[u.length-1]!="string"?u.push(f.value):u[u.length-1]+=f.value,u},[]);return l.length<=1?l[0]||"":l},this.formatToParts=function(h){return xe$2(i.ast,i.locales,i.formatters,i.formats,h,void 0,i.message)},this.resolvedOptions=function(){var h;return {locale:((h=i.resolvedLocale)===null||h===void 0?void 0:h.toString())||Intl.NumberFormat.supportedLocalesOf(i.locales)[0]}},this.getAst=function(){return i.ast},this.locales=r,this.resolvedLocale=e.resolveLocale(r),typeof t=="string"){if(this.message=t,!e.__parse)throw new TypeError("IntlMessageFormat.__parse must be set to process `message` of type `string`");var s=o||{};s.formatters;var a=ln(s,["formatters"]);this.ast=e.__parse(t,w$3(w$3({},a),{locale:this.resolvedLocale}));}else this.ast=t;if(!Array.isArray(this.ast))throw new TypeError("A message must be provided as a String or AST.");this.formats=Kn(e.formats,n),this.formatters=o&&o.formatters||eo(this.formatterCache);}return Object.defineProperty(e,"defaultLocale",{get:function(){return e.memoizedDefaultLocale||(e.memoizedDefaultLocale=new Intl.NumberFormat().resolvedOptions().locale),e.memoizedDefaultLocale},enumerable:false,configurable:true}),e.memoizedDefaultLocale=null,e.resolveLocale=function(t){if(!(typeof Intl.Locale>"u")){var r=Intl.NumberFormat.supportedLocalesOf(t);return r.length>0?new Intl.Locale(r[0]):new Intl.Locale(typeof t=="string"?t:t[0])}},e.__parse=Xn,e.formats={number:{integer:{maximumFractionDigits:0},currency:{style:"currency"},percent:{style:"percent"}},date:{short:{month:"numeric",day:"numeric",year:"2-digit"},medium:{month:"short",day:"numeric",year:"numeric"},long:{month:"long",day:"numeric",year:"numeric"},full:{weekday:"long",month:"long",day:"numeric",year:"numeric"}},time:{short:{hour:"numeric",minute:"numeric"},medium:{hour:"numeric",minute:"numeric",second:"numeric"},long:{hour:"numeric",minute:"numeric",second:"numeric",timeZoneName:"short"},full:{hour:"numeric",minute:"numeric",second:"numeric",timeZoneName:"short"}}},e})();function to(e,t){if(t==null)return;if(t in e)return e[t];const r=t.split(".");let n=e;for(let o=0;o<r.length;o++)if(typeof n=="object"){if(o>0){const i=r.slice(o,r.length).join(".");if(i in n){n=n[i];break}}n=n[r[o]];}else n=void 0;return n}const q$3={},ro=(e,t,r)=>r&&(t in q$3||(q$3[t]={}),e in q$3[t]||(q$3[t][e]=r),r),ur=(e,t)=>{if(t==null)return;if(t in q$3&&e in q$3[t])return q$3[t][e];const r=me$2(t);for(let n=0;n<r.length;n++){const o=r[n],i=oo(o,e);if(i)return ro(e,t,i)}};let tt$2;const oe$2=writable({});function no(e){return tt$2[e]||null}function rt$1(e){return e in tt$2}function oo(e,t){if(!rt$1(e))return null;const r=no(e);return to(r,t)}function io(e){if(e==null)return;const t=me$2(e);for(let r=0;r<t.length;r++){const n=t[r];if(rt$1(n))return n}}function Se$1(e,...t){delete q$3[e],oe$2.update(r=>(r[e]=un.all([r[e]||{},...t]),r));}derived([oe$2],([e])=>Object.keys(e));oe$2.subscribe(e=>tt$2=e);const he$2={};function so(e){he$2[e]=new Set;}function ao(e,t){he$2[e].delete(t),he$2[e].size===0&&delete he$2[e];}function fe$2(e){return he$2[e]}function co(e){return me$2(e).map(t=>{const r=fe$2(t);return [t,r?[...r]:[]]}).filter(([,t])=>t.length>0)}function Te$1(e){return e==null?false:me$2(e).some(t=>{var r;return (r=fe$2(t))==null?void 0:r.size})}function uo(e,t){return Promise.all(t.map(n=>(ao(e,n),n().then(o=>o.default||o)))).then(n=>Se$1(e,...n))}const ue$2={};function lr(e){if(!Te$1(e))return e in ue$2?ue$2[e]:Promise.resolve();const t=co(e);return ue$2[e]=Promise.all(t.map(([r,n])=>uo(r,n))).then(()=>{if(Te$1(e))return lr(e);delete ue$2[e];}),ue$2[e]}function lo(e,t){fe$2(e)||so(e);const r=fe$2(e);fe$2(e).has(t)||(rt$1(e)||oe$2.update(n=>(n[e]={},n)),r.add(t));}var At$2=Object.getOwnPropertySymbols,ho=Object.prototype.hasOwnProperty,fo=Object.prototype.propertyIsEnumerable,po=(e,t)=>{var r={};for(var n in e)ho.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&At$2)for(var n of At$2(e))t.indexOf(n)<0&&fo.call(e,n)&&(r[n]=e[n]);return r};const mo={number:{scientific:{notation:"scientific"},engineering:{notation:"engineering"},compactLong:{notation:"compact",compactDisplay:"long"},compactShort:{notation:"compact",compactDisplay:"short"}},date:{short:{month:"numeric",day:"numeric",year:"2-digit"},medium:{month:"short",day:"numeric",year:"numeric"},long:{month:"long",day:"numeric",year:"numeric"},full:{weekday:"long",month:"long",day:"numeric",year:"numeric"}},time:{short:{hour:"numeric",minute:"numeric"},medium:{hour:"numeric",minute:"numeric",second:"numeric"},long:{hour:"numeric",minute:"numeric",second:"numeric",timeZoneName:"short"},full:{hour:"numeric",minute:"numeric",second:"numeric",timeZoneName:"short"}}};function _o({locale:e,id:t}){console.warn(`[svelte-i18n] The message "${t}" was not found in "${me$2(e).join('", "')}".${Te$1(V())?`

Note: there are at least one loader still registered to this locale that wasn't executed.`:""}`);}const go={fallbackLocale:null,loadingDelay:200,formats:mo,warnOnMissingMessages:true,handleMissingMessage:void 0,ignoreTag:true},le$2=go;function ne$3(){return le$2}function bo(e){const t=e,{formats:r}=t,n=po(t,["formats"]);let o=e.fallbackLocale;if(e.initialLocale)try{cr.resolveLocale(e.initialLocale)&&(o=e.initialLocale);}catch{console.warn(`[svelte-i18n] The initial locale "${e.initialLocale}" is not a valid locale.`);}return n.warnOnMissingMessages&&(delete n.warnOnMissingMessages,n.handleMissingMessage==null?n.handleMissingMessage=_o:console.warn('[svelte-i18n] The "warnOnMissingMessages" option is deprecated. Please use the "handleMissingMessage" option instead.')),Object.assign(le$2,n,{initialLocale:o}),r&&("number"in r&&Object.assign(le$2.formats.number,r.number),"date"in r&&Object.assign(le$2.formats.date,r.date),"time"in r&&Object.assign(le$2.formats.time,r.time)),Y$3.set(o)}const Ge$2=writable(false);var yo=Object.defineProperty,wo=Object.defineProperties,Eo=Object.getOwnPropertyDescriptors,Pt=Object.getOwnPropertySymbols,vo=Object.prototype.hasOwnProperty,xo=Object.prototype.propertyIsEnumerable,Ht=(e,t,r)=>t in e?yo(e,t,{enumerable:true,configurable:true,writable:true,value:r}):e[t]=r,So=(e,t)=>{for(var r in t||(t={}))vo.call(t,r)&&Ht(e,r,t[r]);if(Pt)for(var r of Pt(t))xo.call(t,r)&&Ht(e,r,t[r]);return e},To=(e,t)=>wo(e,Eo(t));let Ye$1;const Ae$1=writable(null);function Ot$2(e){return e.split("-").map((t,r,n)=>n.slice(0,r+1).join("-")).reverse()}function me$2(e,t=ne$3().fallbackLocale){const r=Ot$2(e);return t?[...new Set([...r,...Ot$2(t)])]:r}function V(){return Ye$1??void 0}Ae$1.subscribe(e=>{Ye$1=e??void 0,typeof window<"u"&&e!=null&&document.documentElement.setAttribute("lang",e);});const Ao=e=>{if(e&&io(e)&&Te$1(e)){const{loadingDelay:t}=ne$3();let r;return typeof window<"u"&&V()!=null&&t?r=window.setTimeout(()=>Ge$2.set(true),t):Ge$2.set(true),lr(e).then(()=>{Ae$1.set(e);}).finally(()=>{clearTimeout(r),Ge$2.set(false);})}return Ae$1.set(e)},Y$3=To(So({},Ae$1),{set:Ao}),Po=()=>typeof window>"u"?null:window.navigator.language||window.navigator.languages[0],Ce$2=e=>{const t=Object.create(null);return n=>{const o=JSON.stringify(n);return o in t?t[o]:t[o]=e(n)}};var Ho=Object.defineProperty,Pe$2=Object.getOwnPropertySymbols,hr=Object.prototype.hasOwnProperty,fr=Object.prototype.propertyIsEnumerable,Bt$2=(e,t,r)=>t in e?Ho(e,t,{enumerable:true,configurable:true,writable:true,value:r}):e[t]=r,nt$1=(e,t)=>{for(var r in t||(t={}))hr.call(t,r)&&Bt$2(e,r,t[r]);if(Pe$2)for(var r of Pe$2(t))fr.call(t,r)&&Bt$2(e,r,t[r]);return e},ie$2=(e,t)=>{var r={};for(var n in e)hr.call(e,n)&&t.indexOf(n)<0&&(r[n]=e[n]);if(e!=null&&Pe$2)for(var n of Pe$2(e))t.indexOf(n)<0&&fr.call(e,n)&&(r[n]=e[n]);return r};const de$2=(e,t)=>{const{formats:r}=ne$3();if(e in r&&t in r[e])return r[e][t];throw new Error(`[svelte-i18n] Unknown "${t}" ${e} format.`)},Oo=Ce$2(e=>{var t=e,{locale:r,format:n}=t,o=ie$2(t,["locale","format"]);if(r==null)throw new Error('[svelte-i18n] A "locale" must be set to format numbers');return n&&(o=de$2("number",n)),new Intl.NumberFormat(r,o)}),Bo=Ce$2(e=>{var t=e,{locale:r,format:n}=t,o=ie$2(t,["locale","format"]);if(r==null)throw new Error('[svelte-i18n] A "locale" must be set to format dates');return n?o=de$2("date",n):Object.keys(o).length===0&&(o=de$2("date","short")),new Intl.DateTimeFormat(r,o)}),Co=Ce$2(e=>{var t=e,{locale:r,format:n}=t,o=ie$2(t,["locale","format"]);if(r==null)throw new Error('[svelte-i18n] A "locale" must be set to format time values');return n?o=de$2("time",n):Object.keys(o).length===0&&(o=de$2("time","short")),new Intl.DateTimeFormat(r,o)}),No=(e={})=>{var t=e,{locale:r=V()}=t,n=ie$2(t,["locale"]);return Oo(nt$1({locale:r},n))},Io=(e={})=>{var t=e,{locale:r=V()}=t,n=ie$2(t,["locale"]);return Bo(nt$1({locale:r},n))},Lo=(e={})=>{var t=e,{locale:r=V()}=t,n=ie$2(t,["locale"]);return Co(nt$1({locale:r},n))},Ro=Ce$2((e,t=V())=>new cr(e,t,ne$3().formats,{ignoreTag:ne$3().ignoreTag})),Mo=(e,t={})=>{var r,n,o,i;let s=t;typeof e=="object"&&(s=e,e=s.id);const{values:a,locale:h=V(),default:c}=s;if(h==null)throw new Error("[svelte-i18n] Cannot format a message without first setting the initial locale.");let l=ur(e,h);if(!l)l=(i=(o=(n=(r=ne$3()).handleMissingMessage)==null?void 0:n.call(r,{locale:h,id:e,defaultValue:c}))!=null?o:c)!=null?i:e;else if(typeof l!="string")return console.warn(`[svelte-i18n] Message with id "${e}" must be of type "string", found: "${typeof l}". Gettin its value through the "$format" method is deprecated; use the "json" method instead.`),l;if(!a)return l;let u=l;try{u=Ro(l,h).format(a);}catch(f){f instanceof Error&&console.warn(`[svelte-i18n] Message "${e}" has syntax error:`,f.message);}return u},Do=(e,t)=>Lo(t).format(e),ko=(e,t)=>Io(t).format(e),Uo=(e,t)=>No(t).format(e),jo=(e,t=V())=>ur(e,t),pr=derived([Y$3,oe$2],()=>Mo);derived([Y$3],()=>Do);derived([Y$3],()=>ko);derived([Y$3],()=>Uo);derived([Y$3,oe$2],()=>jo);const ls=writable(null);let dr=false;typeof window<"u"&&"attachShadow"in Element.prototype&&"adoptedStyleSheets"in Document.prototype&&(dr="adoptedStyleSheets"in document.createElement("div").attachShadow({mode:"open"}));function hs(e,t){const r=new URL(import.meta.url).origin;var n=e;if(window.location.origin!==r&&(n=new URL(e,r).href),document.querySelector(`link[href='${n}']`))return Promise.resolve();const i=document.createElement("link");return i.rel="stylesheet",i.href=n,new Promise((s,a)=>{i.addEventListener("load",()=>s()),i.addEventListener("error",()=>{console.error(`Unable to preload CSS for ${n}`),s();}),t.appendChild(i);})}function fs(e,t,r){if(!dr)return e;r||(r=document.createElement("style")),r.remove();const n=new CSSStyleSheet;n.replaceSync(e);let o="";e=e.replace(/@import\s+url\((.*?)\);\s*/g,(h,c)=>(o+=`@import url(${c});
`,""));const i=n.cssRules;let s="",a=`.gradio-container.gradio-container-${t} .contain `;for(let h=0;h<i.length;h++){const c=i[h];let l=c.cssText.includes(".dark");if(c instanceof CSSStyleRule){const u=c.selectorText;if(u){const f=u.replace(".dark","").split(",").map(_=>`${l?".dark":""} ${a} ${_.trim()} `).join(",");s+=c.cssText,s+=c.cssText.replace(u,f);}}else if(c instanceof CSSMediaRule){let u=`@media ${c.media.mediaText} {`;for(let f=0;f<c.cssRules.length;f++){const _=c.cssRules[f];if(_ instanceof CSSStyleRule){let P=_.cssText.includes(".dark ");const d=_.selectorText,E=d.replace(".dark","").split(",").map(p=>`${P?".dark":""} ${a} ${p.trim()} `).join(",");u+=_.cssText.replace(d,E);}}u+="}",s+=u;}else if(c instanceof CSSKeyframesRule){s+=`@keyframes ${c.name} {`;for(let u=0;u<c.cssRules.length;u++){const f=c.cssRules[u];f instanceof CSSKeyframeRule&&(s+=`${f.keyText} { ${f.style.cssText} }`);}s+="}";}else c instanceof CSSFontFaceRule&&(s+=`@font-face { ${c.style.cssText} }`);}return o+s}const $o={accordion:{component:()=>import('./Index44-BgXhyvCF.js')},annotatedimage:{component:()=>import('./Index24-CxhRqMaV.js')},audio:{base:()=>import('./StaticAudio-C0Rh10dO.js').then(e=>e.a),example:()=>import('./Example-C4U47Phv.js'),component:()=>import('./index62-DuEQvb8F.js')},box:{component:()=>import('./Index7-DJleAqHc.js')},browserstate:{component:()=>import('./Index66-XDD3kKDy.js')},button:{component:()=>import('./Index8-B-BTbxXS.js')},chatbot:{component:()=>import('./Index65-GNB5DZ2h.js')},checkbox:{example:()=>import('./Example12-Laho8TuN.js'),component:()=>import('./Index10-DgvM6iyV.js')},checkboxgroup:{example:()=>import('./Example13-y_4tvsVn.js'),component:()=>import('./Index25-CG0VltJm.js')},code:{example:()=>import('./Example2-C1QB7oes.js'),component:()=>import('./Index64-Djt3Hnkl.js')},colorpicker:{example:()=>import('./Example14-vkLMcQAb.js'),component:()=>import('./Index52-B32t5vuK.js')},column:{component:()=>import('./Index12-CydRcvS7.js')},core:{component:()=>import('./index-Botgtvpr.js')},dataframe:{example:()=>import('./Example15-CREytteg.js'),component:()=>import('./Index23-qsZJSr9Z.js').then(e=>e.I)},dataset:{component:()=>import('./Index53-BhJYcLYR.js')},datetime:{example:()=>import('./Example4-DmtsMWW6.js'),component:()=>import('./Index57-CDWQC3pK.js')},dialogue:{example:()=>import('./Example16-Bo9R9byT.js'),component:()=>import('./Index58-Cj2Tqc_7.js')},downloadbutton:{component:()=>import('./Index45-ClI7aRtD.js')},draggable:{component:()=>import('./Index26-h1OuDXq2.js')},dropdown:{example:()=>import('./Example5-B47CTqpN.js'),component:()=>import('./Index54-BATUlv2u.js')},file:{example:()=>import('./Example6-B-ItDYQm.js'),component:()=>import('./Index27-DOkf9GKx.js')},fileexplorer:{example:()=>import('./Example17--6WHhLSK.js'),component:()=>import('./Index63-Dwm7l6sb.js')},form:{component:()=>import('./Index13-DnJSRo8D.js')},gallery:{base:()=>import('./Gallery-BtyraTcF.js'),example:()=>import('./Example7-EhqFPUU1.js'),component:()=>import('./Index14-D8A-ecR4.js')},group:{component:()=>import('./Index28-Bd05MZKN.js')},highlightedtext:{component:()=>import('./Index60-DdGuyE1U.js')},html:{base:()=>import('./HTML-Dc8oCSHH.js'),example:()=>import('./Example18-2bBU3g9W.js'),component:()=>import('./Index29-Brf1TYj-.js')},image:{base:()=>import('./ImagePreview-DZORK30D.js'),example:()=>import('./Example8-CMemDGYH.js'),component:()=>import('./Index30-DYkBZnhU.js')},imageeditor:{example:()=>import('./Example19-lbzqLtc3.js'),component:()=>import('./Index4-CDgtjC10.js').then(e=>e.au)},imageslider:{example:()=>import('./Example20-BCkQjF0N.js'),component:()=>import('./Index67-DjpdXbZK.js')},json:{example:()=>import('./Example21-_Eh83TuR.js'),component:()=>import('./Index15-D01tw-9l.js')},label:{component:()=>import('./Index46-BaGsmR6M.js')},markdown:{example:()=>import('./Example9-C8NOOGsI.js'),component:()=>import('./Index16-BlWsTLbE.js')},model3d:{base:()=>import('./Model3D-Dq15i0_K.js'),example:()=>import('./Example22-CrVGMh2p.js'),component:()=>import('./Index47-C9vr7BDV.js')},multimodaltextbox:{example:()=>import('./Example23-tcbzMCSz.js'),component:()=>import('./Index59-DMZvSVOM.js')},nativeplot:{example:()=>import('./Example10-BlDKE0uv.js'),component:()=>import('./Index31-HjhAizwP.js')},navbar:{base:()=>import('./Index17-CbD_JXKx.js'),example:()=>import('./Example11-d-lsg9iW.js'),component:()=>import('./Index17-CbD_JXKx.js')},number:{example:()=>import('./Example24-DKlEDgNZ.js'),component:()=>import('./Index32-QQ2zchkg.js')},paramviewer:{example:()=>import('./Example25-COOHOmqI.js'),component:()=>import('./Index61-BLN0BqVy.js')},plot:{base:()=>import('./Plot-DB-BsHV0.js').then(e=>e.b),component:()=>import('./Index18-_y4-YhJj.js')},radio:{example:()=>import('./Example26-DmJOI45Y.js'),component:()=>import('./Index55-BGGFWxim.js')},row:{component:()=>import('./Index33-kvAZVDav.js')},sidebar:{component:()=>import('./Index48-DXE9LO6p.js')},slider:{example:()=>import('./Example27-DIwEd4NY.js'),component:()=>import('./Index34-D1xlO_Ad.js')},state:{component:()=>import('./Index19-PnAHp94D.js')},statustracker:{component:()=>import('./index2-B9mMBFZ5.js')},tabitem:{component:()=>import('./Index49-BRqgQjDI.js')},tabs:{component:()=>import('./Index35-BRpes2ct.js')},textbox:{example:()=>import('./Example3-W13oz660.js'),component:()=>import('./Index20-B4-tSOPR.js')},timer:{component:()=>import('./Index21-D5SRTCXo.js')},uploadbutton:{component:()=>import('./Index50-CdPD7yKG.js')},vibeeditor:{component:()=>import('./Index36-CKhsKJNJ.js')},video:{base:()=>import('./VideoPreview-DvvBit-H.js').then(e=>e.b),example:()=>import('./Example28-WErkdcJM.js'),component:()=>import('./index56-6s_71fec.js')},walkthrough:{component:()=>import('./Index35-BRpes2ct.js')},walkthroughstep:{component:()=>import('./Index49-BRqgQjDI.js')}},z$2={},ot$1=typeof window<"u";function Go({api_url:e,name:t,id:r,variant:n}){const o=ot$1&&window.__GRADIO__CC__,i={...$o,...o||{}};let s=r||t;if(z$2[`${s}-${n}`])return {component:z$2[`${s}-${n}`],name:t};try{if(!i?.[s]?.[n]&&!i?.[t]?.[n])throw new Error;return z$2[`${s}-${n}`]=(i?.[s]?.[n]||i?.[t]?.[n])(),{name:t,component:z$2[`${s}-${n}`]}}catch{if(!s)throw new Error(`Component not found: ${t}`);try{return z$2[`${s}-${n}`]=Fo(e,s,n),{name:t,component:z$2[`${s}-${n}`]}}catch(h){if(n==="example")return z$2[`${s}-${n}`]=import('./Example29-CGZsS-M8.js'),{name:t,component:z$2[`${s}-${n}`]};throw console.error(`failed to load: ${t}`),console.error(h),h}}}function Ct$1(e){return ot$1?new Promise((t,r)=>{const n=document.createElement("link");n.rel="stylesheet",n.href=e,document.head.appendChild(n),n.onload=()=>t(),n.onerror=()=>r();}):Promise.resolve()}function Fo(e,t,r){const n=ot$1?"client":"server";let o;return n==="server"?Promise.all([Ct$1(`${e}/custom_component/${t}/${r}/style.css`),import('./Index51-Cw4oMYS2.js')]).then(([i,s])=>s):(o=`${e}/custom_component/${t}/${n}/${r}/index.js`,Promise.all([Ct$1(`${e}/custom_component/${t}/${n}/${r}/style.css`),import(o)]).then(([i,s])=>s))}function ps(e,t,r,n="component"){return e==="api"&&(e="state"),Go({api_url:r,name:e,id:t,variant:n}).component}function ds(e){const t=new Set,r=new Set;for(const n of e)n.inputs.forEach(o=>t.add(o)),n.outputs.forEach(o=>r.add(o));return [t,r]}function ms(e,t,r,n){const[o,i]=n;return t===false?false:t===true?true:!!(o.has(e)||!i.has(e)&&zo(r))}function zo(e){return Array.isArray(e)&&e.length===0||e===""||e===0||!e}const _s=Object.getPrototypeOf(async function(){}).constructor,qo=[{color:"red",primary:600,secondary:100},{color:"green",primary:600,secondary:100},{color:"blue",primary:600,secondary:100},{color:"yellow",primary:500,secondary:100},{color:"purple",primary:600,secondary:100},{color:"teal",primary:600,secondary:100},{color:"orange",primary:600,secondary:100},{color:"cyan",primary:600,secondary:100},{color:"lime",primary:500,secondary:100},{color:"pink",primary:600,secondary:100}],Nt$2={inherit:"inherit",current:"currentColor",transparent:"transparent",black:"#000",white:"#fff",slate:{50:"#f8fafc",100:"#f1f5f9",200:"#e2e8f0",300:"#cbd5e1",400:"#94a3b8",500:"#64748b",600:"#475569",700:"#334155",800:"#1e293b",900:"#0f172a",950:"#020617"},gray:{50:"#f9fafb",100:"#f3f4f6",200:"#e5e7eb",300:"#d1d5db",400:"#9ca3af",500:"#6b7280",600:"#4b5563",700:"#374151",800:"#1f2937",900:"#111827",950:"#030712"},zinc:{50:"#fafafa",100:"#f4f4f5",200:"#e4e4e7",300:"#d4d4d8",400:"#a1a1aa",500:"#71717a",600:"#52525b",700:"#3f3f46",800:"#27272a",900:"#18181b",950:"#09090b"},neutral:{50:"#fafafa",100:"#f5f5f5",200:"#e5e5e5",300:"#d4d4d4",400:"#a3a3a3",500:"#737373",600:"#525252",700:"#404040",800:"#262626",900:"#171717",950:"#0a0a0a"},stone:{50:"#fafaf9",100:"#f5f5f4",200:"#e7e5e4",300:"#d6d3d1",400:"#a8a29e",500:"#78716c",600:"#57534e",700:"#44403c",800:"#292524",900:"#1c1917",950:"#0c0a09"},red:{50:"#fef2f2",100:"#fee2e2",200:"#fecaca",300:"#fca5a5",400:"#f87171",500:"#ef4444",600:"#dc2626",700:"#b91c1c",800:"#991b1b",900:"#7f1d1d",950:"#450a0a"},orange:{50:"#fff7ed",100:"#ffedd5",200:"#fed7aa",300:"#fdba74",400:"#fb923c",500:"#f97316",600:"#ea580c",700:"#c2410c",800:"#9a3412",900:"#7c2d12",950:"#431407"},amber:{50:"#fffbeb",100:"#fef3c7",200:"#fde68a",300:"#fcd34d",400:"#fbbf24",500:"#f59e0b",600:"#d97706",700:"#b45309",800:"#92400e",900:"#78350f",950:"#451a03"},yellow:{50:"#fefce8",100:"#fef9c3",200:"#fef08a",300:"#fde047",400:"#facc15",500:"#eab308",600:"#ca8a04",700:"#a16207",800:"#854d0e",900:"#713f12",950:"#422006"},lime:{50:"#f7fee7",100:"#ecfccb",200:"#d9f99d",300:"#bef264",400:"#a3e635",500:"#84cc16",600:"#65a30d",700:"#4d7c0f",800:"#3f6212",900:"#365314",950:"#1a2e05"},green:{50:"#f0fdf4",100:"#dcfce7",200:"#bbf7d0",300:"#86efac",400:"#4ade80",500:"#22c55e",600:"#16a34a",700:"#15803d",800:"#166534",900:"#14532d",950:"#052e16"},emerald:{50:"#ecfdf5",100:"#d1fae5",200:"#a7f3d0",300:"#6ee7b7",400:"#34d399",500:"#10b981",600:"#059669",700:"#047857",800:"#065f46",900:"#064e3b",950:"#022c22"},teal:{50:"#f0fdfa",100:"#ccfbf1",200:"#99f6e4",300:"#5eead4",400:"#2dd4bf",500:"#14b8a6",600:"#0d9488",700:"#0f766e",800:"#115e59",900:"#134e4a",950:"#042f2e"},cyan:{50:"#ecfeff",100:"#cffafe",200:"#a5f3fc",300:"#67e8f9",400:"#22d3ee",500:"#06b6d4",600:"#0891b2",700:"#0e7490",800:"#155e75",900:"#164e63",950:"#083344"},sky:{50:"#f0f9ff",100:"#e0f2fe",200:"#bae6fd",300:"#7dd3fc",400:"#38bdf8",500:"#0ea5e9",600:"#0284c7",700:"#0369a1",800:"#075985",900:"#0c4a6e",950:"#082f49"},blue:{50:"#eff6ff",100:"#dbeafe",200:"#bfdbfe",300:"#93c5fd",400:"#60a5fa",500:"#3b82f6",600:"#2563eb",700:"#1d4ed8",800:"#1e40af",900:"#1e3a8a",950:"#172554"},indigo:{50:"#eef2ff",100:"#e0e7ff",200:"#c7d2fe",300:"#a5b4fc",400:"#818cf8",500:"#6366f1",600:"#4f46e5",700:"#4338ca",800:"#3730a3",900:"#312e81",950:"#1e1b4b"},violet:{50:"#f5f3ff",100:"#ede9fe",200:"#ddd6fe",300:"#c4b5fd",400:"#a78bfa",500:"#8b5cf6",600:"#7c3aed",700:"#6d28d9",800:"#5b21b6",900:"#4c1d95",950:"#2e1065"},purple:{50:"#faf5ff",100:"#f3e8ff",200:"#e9d5ff",300:"#d8b4fe",400:"#c084fc",500:"#a855f7",600:"#9333ea",700:"#7e22ce",800:"#6b21a8",900:"#581c87",950:"#3b0764"},fuchsia:{50:"#fdf4ff",100:"#fae8ff",200:"#f5d0fe",300:"#f0abfc",400:"#e879f9",500:"#d946ef",600:"#c026d3",700:"#a21caf",800:"#86198f",900:"#701a75",950:"#4a044e"},pink:{50:"#fdf2f8",100:"#fce7f3",200:"#fbcfe8",300:"#f9a8d4",400:"#f472b6",500:"#ec4899",600:"#db2777",700:"#be185d",800:"#9d174d",900:"#831843",950:"#500724"},rose:{50:"#fff1f2",100:"#ffe4e6",200:"#fecdd3",300:"#fda4af",400:"#fb7185",500:"#f43f5e",600:"#e11d48",700:"#be123c",800:"#9f1239",900:"#881337",950:"#4c0519"}};qo.reduce((e,{color:t,primary:r,secondary:n})=>({...e,[t]:{primary:Nt$2[t][r],secondary:Nt$2[t][n]}}),{});function mr(e){if(e==null)return "";const t=String(e),r=get(pr);let n=r(t);if(n!==t)return n;const o=t.toLowerCase();for(const i of Jo){const s=i.substring(i.indexOf(".")+1);if(o===s){const a=r(i);if(a!==i)return a;break}}return t}const gs=derived(pr,()=>mr),It$2={ar:"جاري التحميل",ca:"S'està carregant",ckb:"بارکردن",de:"Laden",en:"Loading",es:"Cargando",eu:"Kargatzen",fa:"در حال بارگذاری",fi:"Ladataan",fr:"Chargement",he:"טוען",hi:"लोड हो रहा है",ja:"読み込み中",ko:"로딩 중",lt:"Kraunama",nb:"Laster",nl:"Laden",pl:"Ładowanie","pt-BR":"Carregando",pt:"A carregar",ro:"Se încarcă",ru:"Загрузка",sv:"Laddar",ta:"ஏற்றுகிறது",th:"กำลังโหลด",tr:"Yükleniyor",uk:"Завантаження",ur:"لوڈ ہو رہا ہے",uz:"Yuklanmoqda","zh-CN":"加载中","zh-TW":"載入中"},_r="English",gr={annotated_image:"Annotated Image"},br={allow_recording_access:"Please allow access to the microphone for recording.",audio:"Audio",drop_to_upload:"Drop an audio file here to upload",record_from_microphone:"Record from microphone",stop_recording:"Stop recording",no_device_support:"Media devices could not be accessed. Check that you are running on a secure origin (https) or localhost (or you have passed a valid SSL certificate to ssl_verify), and you have allowed browser access to your device.",stop:"Stop",resume:"Resume",record:"Record",no_microphone:"No microphone found",pause:"Pause",play:"Play",waiting:"Waiting"},yr={connection_can_break:"On mobile, the connection can break if this tab is unfocused or the device sleeps, losing your position in queue.",long_requests_queue:"There is a long queue of requests pending. Duplicate this Space to skip.",lost_connection:"Lost connection due to leaving page. Rejoining queue...",waiting_for_inputs:"Waiting for file(s) to finish uploading, please retry."},wr={edit:"Edit",retry:"Retry",undo:"Undo",submit:"Submit",cancel:"Cancel",like:"Like",dislike:"Dislike",clear:"Clear",copy_message:"Copy message",copied_message:"Copied message"},Er={new_chat:"New chat",message_placeholder:"Type a message...",additional_inputs:"Additional inputs",chatbot:"Chatbot",conversation:"Conversation"},vr={checkbox:"Checkbox",checkbox_group:"Checkbox Group"},xr={code:"Code"},Sr={color_picker:"Color Picker"},Tr={built_with:"built with",built_with_gradio:"Built with Gradio",clear:"Clear",download:"Download",edit:"Edit",empty:"Empty",error:"Error",hosted_on:"Hosted on",loading:"Loading",logo:"logo",or:"or",remove:"Remove",settings:"Settings",share:"Share",submit:"Submit",undo:"Undo",no_devices:"No devices found",language:"Language",display_theme:"Display Theme",pwa:"Progressive Web App",record:"Record",stop_recording:"Stop Recording",screen_studio:"Screen Studio",share_gradio_tab:"[Sharing] Gradio Tab",run:"Run"},Ar={incorrect_format:"Incorrect format, only CSV and TSV files are supported",new_column:"Add column",new_row:"New row",add_row_above:"Add row above",add_row_below:"Add row below",delete_row:"Delete row",delete_column:"Delete column",add_column_left:"Add column to the left",add_column_right:"Add column to the right",sort_column:"Sort column",sort_ascending:"Sort ascending",sort_descending:"Sort descending",drop_to_upload:"Drop CSV or TSV files here to import data into dataframe",clear_sort:"Clear sort",filter:"Filter",clear_filter:"Clear filters"},Pr={dropdown:"Dropdown"},Hr={build_error:"there is a build error",config_error:"there is a config error",contact_page_author:"Please contact the author of the page to let them know.",no_app_file:"there is no app file",runtime_error:"there is a runtime error",space_not_working:`"Space isn't working because" {0}`,space_paused:"the space is paused",use_via_api:"Use via API",use_via_api_or_mcp:"Use via API or MCP"},Or={uploading:"Uploading..."},Br={highlighted_text:"Highlighted Text"},Cr={allow_webcam_access:"Please allow access to the webcam for recording.",brush_color:"Brush color",brush_radius:"Brush radius",image:"Image",remove_image:"Remove Image",select_brush_color:"Select brush color",start_drawing:"Start drawing",use_brush:"Use brush",drop_to_upload:"Drop an image file here to upload"},Nr={label:"Label"},Ir={enable_cookies:"If you are visiting a HuggingFace Space in Incognito mode, you must enable third party cookies.",incorrect_credentials:"Incorrect Credentials",username:"username",password:"password",login:"Login"},Lr={number:"Number"},Rr={plot:"Plot"},Mr={radio:"Radio"},Dr={slider:"Slider"},kr={click_to_upload:"Click to Upload",drop_audio:"Drop Audio Here",drop_csv:"Drop CSV Here",drop_file:"Drop File Here",drop_image:"Drop Image Here",drop_video:"Drop Video Here",drop_gallery:"Drop Media Here",paste_clipboard:"Paste from Clipboard"},Ur={drop_to_upload:"Drop a video file here to upload"},it$1={_name:_r,"3D_model":{"3d_model":"3D Model",drop_to_upload:"Drop a 3D model (.obj, .glb, .stl, .gltf, .splat, or .ply) file here to upload"},annotated_image:gr,audio:br,blocks:yr,chatbot:wr,chat_interface:Er,checkbox:vr,code:xr,color_picker:Sr,common:Tr,dataframe:Ar,dropdown:Pr,errors:Hr,file:Or,highlighted_text:Br,image:Cr,label:Nr,login:Ir,number:Lr,plot:Rr,radio:Mr,slider:Dr,upload_text:kr,video:Ur},Vo=Object.freeze(Object.defineProperty({__proto__:null,_name:_r,annotated_image:gr,audio:br,blocks:yr,chat_interface:Er,chatbot:wr,checkbox:vr,code:xr,color_picker:Sr,common:Tr,dataframe:Ar,default:it$1,dropdown:Pr,errors:Hr,file:Or,highlighted_text:Br,image:Cr,label:Nr,login:Ir,number:Lr,plot:Rr,radio:Mr,slider:Dr,upload_text:kr,video:Ur},Symbol.toStringTag,{value:"Module"})),Xo={ar:"العربية",ca:"Català",ckb:"کوردی",de:"Deutsch",en:"English",es:"Español",eu:"Euskara",fa:"فارسی",fi:"Suomi",fr:"Français",he:"עברית",hi:"हिंदी",ja:"日本語",ko:"한국어",lt:"Lietuvių",nb:"Norsk bokmål",nl:"Nederlands",pl:"Polski","pt-BR":"Português do Brasil",pt:"Português",ro:"Română",ru:"Русский",sv:"Svenska",ta:"தமிழ்",th:"ภาษาไทย",tr:"Türkçe",uk:"Українська",ur:"اردو",uz:"O'zbek","zh-CN":"简体中文","zh-TW":"繁體中文"},Wo=Object.assign({"./lang/ar.json":()=>import('./ar-oZrlju6V.js'),"./lang/ca.json":()=>import('./ca-D4CQWB70.js'),"./lang/ckb.json":()=>import('./ckb-Cf76uBEO.js'),"./lang/de.json":()=>import('./de-CHgt1urw.js'),"./lang/en.json":()=>Promise.resolve().then(()=>Vo),"./lang/es.json":()=>import('./es-CHrrrvnD.js'),"./lang/eu.json":()=>import('./eu-B4ttIBss.js'),"./lang/fa.json":()=>import('./fa-Cftza7v_.js'),"./lang/fi.json":()=>import('./fi-CsmdXgQC.js'),"./lang/fr.json":()=>import('./fr-DpHhFOlo.js'),"./lang/he.json":()=>import('./he-BDmdmDW-.js'),"./lang/hi.json":()=>import('./hi-BEwoCZ2B.js'),"./lang/id.json":()=>import('./id-B4bhjheo.js'),"./lang/ja.json":()=>import('./ja-v-GO49IA.js'),"./lang/ko.json":()=>import('./ko-xc08dXGA.js'),"./lang/lt.json":()=>import('./lt-BSuzG0gL.js'),"./lang/nb.json":()=>import('./nb-vetOmdmu.js'),"./lang/nl.json":()=>import('./nl-B32Jky1V.js'),"./lang/pl.json":()=>import('./pl-BGo_kgCP.js'),"./lang/pt-BR.json":()=>import('./pt-BR-dOf4BQE4.js'),"./lang/pt.json":()=>import('./pt-CFijILHh.js'),"./lang/ro.json":()=>import('./ro-BeOmQJCE.js'),"./lang/ru.json":()=>import('./ru-D4j7Vj8W.js'),"./lang/sv.json":()=>import('./sv-B36J5JTf.js'),"./lang/ta.json":()=>import('./ta-DmpZJUPn.js'),"./lang/th.json":()=>import('./th-DateLXqZ.js'),"./lang/tr.json":()=>import('./tr-DlXBx-Zg.js'),"./lang/uk.json":()=>import('./uk-DwKiM4Np.js'),"./lang/ur.json":()=>import('./ur-7BCsXLxH.js'),"./lang/uz.json":()=>import('./uz-D7FUtAO1.js'),"./lang/zh-CN.json":()=>import('./zh-CN-DFscmJOp.js'),"./lang/zh-TW.json":()=>import('./zh-TW-DZ2Xs7L6.js')});function bs(e){return e&&typeof e=="object"&&e.__type__==="translation_metadata"&&typeof e.key=="string"}const Lt$1="__i18n__";function ys(e){if(typeof e!="string")return e;const t=e.indexOf(Lt$1);if(t===-1)return e;try{const r=t>0?e.substring(0,t):"",n=t+Lt$1.length,o=e.indexOf("{",n);let i=-1,s=0;for(let c=o;c<e.length;c++)if(e[c]==="{"&&s++,e[c]==="}"&&s--,s===0){i=c+1;break}if(i===-1)return console.error("Could not find end of JSON in i18n string"),e;const a=e.substring(o,i),h=i<e.length?e.substring(i):"";try{const c=JSON.parse(a);if(c&&c.key){const l=mr(c.key);return r+l+h}}catch(c){console.error("Error parsing i18n JSON:",c);}return e}catch(r){return console.error("Error processing translation:",r),e}}function Zo(){return {...Object.fromEntries(Object.entries(Wo).map(([t,r])=>[t.split("/").pop().split(".")[0],{type:"lazy",data:r}])),en:{type:"static",data:it$1}}}const st$2=Zo(),Ke$1=Object.keys(st$2),ws=Object.entries(st$2).map(([e])=>[Xo[e]||e,e]);let Jo=new Set,Fe$2=false,Rt$2;function Qo(e){const t=e.split(",").map(r=>r.includes(";")?r.split(";").slice(0,2):[r,1]);t.sort((r,n)=>parseFloat(n[1])-parseFloat(r[1]));for(const[r,n]of t)if(Ke$1.includes(r))return r;return null}async function Es(e,t){if(Fe$2&&!(Fe$2&&e!==Rt$2))return;Rt$2=e,Yo({processed_langs:st$2,custom_translations:e??{}});let n=null;const o=Po();if(t?n=Qo(t):n=o&&Ke$1.includes(o)?o:null,!n){const i=o?.split("-")[0];n=i&&Ke$1.includes(i)?i:"en";}await bo({fallbackLocale:"en",initialLocale:n}),Fe$2=true;}function vs(e){Y$3.set(e);}function xs(e,t,r="en"){return e&&t.includes(e)?e:r}function Yo(e){if(e){try{for(const t in e.custom_translations)Se$1(t,e.custom_translations[t]);for(const t in e.processed_langs)t==="en"&&e.processed_langs[t].type==="static"?Se$1(t,it$1):e.processed_langs[t].type==="lazy"&&lo(t,e.processed_langs[t].data);}catch(t){console.error("Error loading translations:",t);}for(const t in It$2)Se$1(t,{common:{loading:It$2[t]}});}}const Ko="host",jr="queue/data",ei="queue/join",Mt="upload",ti="login",Dt$2="config",ri="info",ni="runtime",oi="sleeptime",ii="heartbeat",si="component_server",ai="reset",ci="cancel",ui="app_id",$r="This application is currently busy. Please try again. ",_e$2="Connection errored out. ",J$3="Could not resolve app config. ",li="Could not get space status. ",hi="Could not get API info. ",at$1="Space metadata could not be loaded. ",fi="Invalid URL. A full URL path is required.",pi="Not authorized to access this space. ",Gr="Invalid credentials. Could not login. ",di="Login credentials are required to access this space.",mi="File system access is only available in Node.js environments",Fr="Root URL not found in client config",_i="Error uploading file";async function kt$1(e,t,r){try{return (await(await fetch(`https://huggingface.co/api/spaces/${e}/jwt`,{headers:{Authorization:`Bearer ${t}`,...r?{Cookie:r}:{}}})).json()).token||!1}catch{return  false}}function gi(e){let t={};return e.forEach(({api_name:r,id:n})=>{r&&(t[r]=n);}),t}async function bi(e){const t=this.options.token?{Authorization:`Bearer ${this.options.token}`}:{};t["Content-Type"]="application/json",typeof window<"u"&&window?.gradio_config?.current_page&&(e=e.substring(0,e.lastIndexOf("/")));let r=Vr(e,this.deep_link?Dt$2+"?deep_link="+this.deep_link:Dt$2);const n=await this.fetch(r,{headers:t,credentials:"include"}),o=await yi(n,!!this.options.auth);return typeof window<"u"&&window?.BUILD_MODE==="dev"&&(o.root=e||o.root),o}async function yi(e,t){if(e?.status===401&&!t){const n=(await e.json())?.detail?.auth_message;throw new Error(n||di)}else if(e?.status===401&&t)throw new Error(Gr);if(e?.status===200){let r=await e.json();return r.dependencies?.forEach((n,o)=>{n.id===void 0&&(n.id=o);}),r}else if(e?.status===401)throw new Error(pi);throw new Error(J$3)}async function wi(){const{http_protocol:e,host:t}=await ut$1(this.app_reference,this.options.token);try{if(this.options.auth){const r=await zr(e,t,this.options.auth,this.fetch,this.options.token);r&&this.set_cookies(r);}}catch(r){throw Error(r.message)}}async function zr(e,t,r,n,o){const i=new FormData;i.append("username",r?.[0]),i.append("password",r?.[1]);let s={};o&&(s.Authorization=`Bearer ${o}`);const a=await n(`${e}//${t}/${ti}`,{headers:s,method:"POST",body:i,credentials:"include"});if(a.status===200)return a.headers.get("set-cookie");throw a.status===401?new Error(Gr):new Error(at$1)}function ze$1(e){if(e.startsWith("http")){const{protocol:t,host:r,pathname:n}=new URL(e);return {ws_protocol:t==="https:"?"wss":"ws",http_protocol:t,host:r+(n!=="/"?n:"")}}return {ws_protocol:"wss",http_protocol:"https:",host:new URL(e).host}}const qr=e=>{let t=[];return e.split(/,(?=\s*[^\s=;]+=[^\s=;]+)/).forEach(n=>{const[o,i]=n.split(";")[0].split("=");o&&i&&t.push(`${o.trim()}=${i.trim()}`);}),t},ct$1=/^[a-zA-Z0-9_\-\.]+\/[a-zA-Z0-9_\-\.]+$/,Ei=/.*hf\.space\/{0,1}.*$/;async function ut$1(e,t){const r={};t&&(r.Authorization=`Bearer ${t}`);const n=e.trim().replace(/\/$/,"");if(ct$1.test(n))try{const i=(await(await fetch(`https://huggingface.co/api/spaces/${n}/${Ko}`,{headers:r})).json()).host;return {space_id:e,...ze$1(i)}}catch{throw new Error(at$1)}if(Ei.test(n)){const{ws_protocol:o,http_protocol:i,host:s}=ze$1(n);return {space_id:s.split("/")[0].replace(".hf.space",""),ws_protocol:o,http_protocol:i,host:s}}return {space_id:false,...ze$1(n)}}const Vr=(...e)=>{try{return e.reduce((t,r)=>(t=t.replace(/\/+$/,""),r=r.replace(/^\/+/,""),new URL(r,t+"/").toString()))}catch{throw new Error(fi)}};function vi(e,t,r){const n={named_endpoints:{},unnamed_endpoints:{}};return Object.keys(e).forEach(o=>{(o==="named_endpoints"||o==="unnamed_endpoints")&&(n[o]={},Object.entries(e[o]).forEach(([i,{parameters:s,returns:a}])=>{const h=t.dependencies.find(u=>u.api_name===i||u.api_name===i.replace("/",""))?.id||r[i.replace("/","")]||-1,c=h!==-1?t.dependencies.find(u=>u.id==h)?.types:{generator:false,cancel:false};if(h!==-1&&t.dependencies.find(u=>u.id==h)?.inputs?.length!==s.length){const u=t.dependencies.find(f=>f.id==h).inputs.map(f=>t.components.find(_=>_.id===f)?.type);try{u.forEach((f,_)=>{if(f==="state"){const P={component:"state",example:null,parameter_default:null,parameter_has_default:!0,parameter_name:null,hidden:!0};s.splice(_,0,P);}});}catch(f){console.error(f);}}const l=(u,f,_,P)=>({...u,description:Si(u?.type,_),type:xi(u?.type,f,_,P)||""});n[o][i]={parameters:s.map(u=>l(u,u?.component,u?.serializer,"parameter")),returns:a.map(u=>l(u,u?.component,u?.serializer,"return")),type:c};}));}),n}function xi(e,t,r,n){if(t==="Api")return e.type;switch(e?.type){case "string":return "string";case "boolean":return "boolean";case "number":return "number"}if(r==="JSONSerializable"||r==="StringSerializable")return "any";if(r==="ListStringSerializable")return "string[]";if(t==="Image")return n==="parameter"?"Blob | File | Buffer":"string";if(r==="FileSerializable")return e?.type==="array"?n==="parameter"?"(Blob | File | Buffer)[]":"{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}[]":n==="parameter"?"Blob | File | Buffer":"{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}";if(r==="GallerySerializable")return n==="parameter"?"[(Blob | File | Buffer), (string | null)][]":"[{ name: string; data: string; size?: number; is_file?: boolean; orig_name?: string}, (string | null))][]"}function Si(e,t){return t==="GallerySerializable"?"array of [file, label] tuples":t==="ListStringSerializable"?"array of strings":t==="FileSerializable"?"array of files or single file":e?.description}function Ut$1(e,t){switch(e.msg){case "send_data":return {type:"data"};case "send_hash":return {type:"hash"};case "queue_full":return {type:"update",status:{queue:true,message:$r,stage:"error",code:e.code,success:e.success}};case "heartbeat":return {type:"heartbeat"};case "unexpected_error":return {type:"unexpected_error",status:{queue:true,message:e.message,session_not_found:e.session_not_found,stage:"error",success:false}};case "broken_connection":return {type:"broken_connection",status:{queue:true,message:e.message,stage:"error",success:false}};case "estimation":return {type:"update",status:{queue:true,stage:t||"pending",code:e.code,size:e.queue_size,position:e.rank,eta:e.rank_eta,success:e.success}};case "progress":return {type:"update",status:{queue:true,stage:"pending",code:e.code,progress_data:e.progress_data,success:e.success}};case "log":return {type:"log",data:e};case "process_generating":return {type:"generating",status:{queue:true,message:e.success?null:e.output.error,stage:e.success?"generating":"error",code:e.code,progress_data:e.progress_data,eta:e.average_duration,changed_state_ids:e.success?e.output.changed_state_ids:void 0},data:e.success?e.output:null};case "process_streaming":return {type:"streaming",status:{queue:true,message:e.output.error,stage:"streaming",time_limit:e.time_limit,code:e.code,progress_data:e.progress_data,eta:e.eta},data:e.output};case "process_completed":return "error"in e.output?{type:"update",status:{queue:true,title:e.output.title??"Error",message:e.output.error??"An error occurred",visible:e.output.visible,duration:e.output.duration,stage:"error",code:e.code,success:e.success}}:{type:"complete",status:{queue:true,message:e.success?void 0:e.output.error,stage:e.success?"complete":"error",code:e.code,progress_data:e.progress_data,changed_state_ids:e.success?e.output.changed_state_ids:void 0},data:e.success?e.output:null};case "process_starts":return {type:"update",status:{queue:true,stage:"pending",code:e.code,size:e.rank,position:0,success:e.success,eta:e.eta},original_msg:"process_starts"}}return {type:"none",status:{stage:"error",queue:true}}}const Ti=(e=[],t)=>{const r=t?t.parameters:[];if(Array.isArray(e))return t&&r.length>0&&e.length>r.length&&console.warn("Too many arguments provided for the endpoint."),e;const n=[],o=Object.keys(e);return r.forEach((i,s)=>{if(e.hasOwnProperty(i.parameter_name))n[s]=e[i.parameter_name];else if(i.parameter_has_default)n[s]=i.parameter_default;else throw new Error(`No value provided for required parameter: ${i.parameter_name}`)}),o.forEach(i=>{if(!r.some(s=>s.parameter_name===i))throw new Error(`Parameter \`${i}\` is not a valid keyword argument. Please refer to the API for usage.`)}),n.forEach((i,s)=>{if(i===void 0&&!r[s].parameter_has_default)throw new Error(`No value provided for required parameter: ${r[s].parameter_name}`)}),n};async function Ai(){if(this.api_info)return this.api_info;const{token:e}=this.options,{config:t}=this,r={"Content-Type":"application/json"};if(e&&(r.Authorization=`Bearer ${e}`),!!t)try{let n,o;if(typeof window<"u"&&window.gradio_api_info)o=window.gradio_api_info;else {const i=Vr(t.root,this.api_prefix,ri);if(n=await this.fetch(i,{headers:r,credentials:"include"}),!n.ok)throw new Error(_e$2);o=await n.json();}return "api"in o&&(o=o.api),o.named_endpoints["/predict"]&&!o.unnamed_endpoints[0]&&(o.unnamed_endpoints[0]=o.named_endpoints["/predict"]),vi(o,t,this.api_map)}catch(n){throw new Error("Could not get API info. "+n.message)}}async function Pi(e,t,r){const n={};this?.options?.token&&(n.Authorization=`Bearer ${this.options.token}`);const o=1e3,i=[];let s;for(let a=0;a<t.length;a+=o){const h=t.slice(a,a+o),c=new FormData;h.forEach(u=>{c.append("files",u);});try{const u=r?`${e}${this.api_prefix}/${Mt}?upload_id=${r}`:`${e}${this.api_prefix}/${Mt}`;s=await this.fetch(u,{method:"POST",body:c,headers:n,credentials:"include"});}catch(u){throw new Error(_e$2+u.message)}if(!s.ok){const u=await s.text();return {error:`HTTP ${s.status}: ${u}`}}const l=await s.json();l&&i.push(...l);}return {files:i}}const Hi={radix:1e3,unit:["b","kb","Mb","Gb","Tb","Pb","Eb","Zb","Yb"]},Oi={radix:1024,unit:["b","Kib","Mib","Gib","Tib","Pib","Eib","Zib","Yib"]},Bi={radix:1024,unit:["b","Kb","Mb","Gb","Tb","Pb","Eb","Zb","Yb"]},jt={si:Hi,iec:Oi,jedec:Bi};function Ci(e,t=1,r="jedec"){e=Math.abs(e);const{radix:n,unit:o}=jt[r]||jt.jedec;let i=0;for(;e>=n;)e/=n,++i;return `${e.toFixed(t)} ${o[i]}`}async function Ni(e,t,r,n){let o=(Array.isArray(e)?e:[e]).map(s=>s.blob);const i=o.filter(s=>s.size>(n??1/0));if(i.length)throw new Error(`File(s) exceed the maximum allowed size of ${Ci(n||1/0)}: ${i.map(s=>`"${s.name}"`).join(", ")}`);return await Promise.all(await this.upload_files(t,o,r).then(async s=>{if(s.error)throw new Error(s.error);return s.files?s.files.map((a,h)=>new Ne$1({...e[h],path:a,url:`${t}${this.api_prefix}/file=${a}`})):[]}))}async function Ss(e,t){return e.map(r=>new Ne$1({path:r.name,orig_name:r.name,blob:r,size:r.size,mime_type:r.type,is_stream:t}))}let Ne$1 = class Ne{path;url;orig_name;size;blob;is_stream;mime_type;alt_text;b64;meta={_type:"gradio.FileData"};constructor({path:t,url:r,orig_name:n,size:o,blob:i,is_stream:s,mime_type:a,alt_text:h,b64:c}){this.path=t,this.url=r,this.orig_name=n,this.size=o,this.blob=r?void 0:i,this.is_stream=s,this.mime_type=a,this.alt_text=h,this.b64=c;}};class Ii{type;command;meta;fileData;constructor(t,r){this.type="command",this.command=t,this.meta=r;}}typeof process<"u"&&process.versions&&process.versions.node;function $t(e,t,r){for(;r.length>1;){const o=r.shift();if(typeof o=="string"||typeof o=="number")e=e[o];else throw new Error("Invalid key type")}const n=r.shift();if(typeof n=="string"||typeof n=="number")e[n]=t;else throw new Error("Invalid key type")}async function et$1(e,t=void 0,r=[],n=false,o=void 0){if(Array.isArray(e)){let i=[];return await Promise.all(e.map(async(s,a)=>{let h=r.slice();h.push(String(a));const c=await et$1(e[a],n?o?.parameters[a]?.component||void 0:t,h,false,o);i=i.concat(c);})),i}else {if(globalThis.Buffer&&e instanceof globalThis.Buffer||e instanceof Blob)return [{path:r,blob:new Blob([e]),type:t}];if(typeof e=="object"&&e!==null){let i=[];for(const s of Object.keys(e)){const a=[...r,s],h=e[s];i=i.concat(await et$1(h,void 0,a,false,o));}return i}}return []}function Li(e,t){let r=t?.dependencies?.find(n=>n.id==e)?.queue;return r!=null?!r:!t.enable_queue}function Ri(e,t){return new Promise((r,n)=>{const o=new MessageChannel;o.port1.onmessage=(({data:i})=>{o.port1.close(),r(i);}),window.parent.postMessage(e,t,[o.port2]);})}function ve$2(e,t,r,n,o=false){if(n==="input"&&!o)throw new Error("Invalid code path. Cannot skip state inputs for input.");if(n==="output"&&o)return e;let i=[],s=0;const a=n==="input"?t.inputs:t.outputs;for(let h=0;h<a.length;h++){const c=a[h];if(r.find(u=>u.id===c)?.type==="state"){if(o)if(e.length===a.length){const u=e[s];i.push(u),s++;}else i.push(null);else {s++;continue}continue}else {const u=e[s];i.push(u),s++;}}return i}async function Mi(e,t,r){const n=this;await Di(n,t);const o=await et$1(t,void 0,[],true,r);return (await Promise.all(o.map(async({path:s,blob:a,type:h})=>{if(!a)return {path:s,type:h};const c=await n.upload_files(e,[a]),l=c.files&&c.files[0];return {path:s,file_url:l,type:h,name:typeof File<"u"&&a instanceof File?a?.name:void 0}}))).forEach(({path:s,file_url:a,type:h,name:c})=>{if(h==="Gallery")$t(t,a,s);else if(a){const l=new Ne$1({path:a,orig_name:c});$t(t,l,s);}}),t}async function Di(e,t){if(!(e.config?.root||e.config?.root_url))throw new Error(Fr);await Xr(e,t);}async function Xr(e,t,r=[]){for(const n in t)t[n]instanceof Ii?await ki(e,t,n):typeof t[n]=="object"&&t[n]!==null&&await Xr(e,t[n],[...r,n]);}async function ki(e,t,r){let n=t[r];const o=e.config?.root||e.config?.root_url;if(!o)throw new Error(Fr);try{let i,s;if(typeof process<"u"&&process.versions&&process.versions.node){const l=await import('fs/promises');s=(await import('path')).resolve(process.cwd(),n.meta.path),i=await l.readFile(s);}else throw new Error(mi);const a=new Blob([i],{type:"application/octet-stream"}),h=await e.upload_files(o,[a]),c=h.files&&h.files[0];if(c){const l=new Ne$1({path:c,orig_name:n.meta.name||""});t[r]=l;}}catch(i){console.error(_i,i);}}async function Ui(e,t,r){const n={"Content-Type":"application/json"};this.options.token&&(n.Authorization=`Bearer ${this.options.token}`);try{var o=await this.fetch(e,{method:"POST",body:JSON.stringify(t),headers:{...n,...r},credentials:"include"});}catch{return [{error:_e$2},500]}let i,s;try{i=await o.json(),s=o.status;}catch(a){i={error:`Could not parse server response: ${a}`},s=500;}return [i,s]}async function ji(e,t={}){let r=false,n=false;if(!this.config)throw new Error("Could not resolve app config");if(typeof e=="number")this.config.dependencies.find(o=>o.id==e);else {const o=e.replace(/^\//,"");this.config.dependencies.find(i=>i.id==this.api_map[o]);}return new Promise(async(o,i)=>{const s=this.submit(e,t,null,null,true);let a;for await(const h of s)h.type==="data"&&(n&&o(a),r=true,a=h),h.type==="status"&&(h.stage==="error"&&i(h),h.stage==="complete"&&(n=true,r&&o(a)));})}async function pe$2(e,t,r){let n=t==="subdomain"?`https://huggingface.co/api/spaces/by-subdomain/${e}`:`https://huggingface.co/api/spaces/${e}`,o,i;try{if(o=await fetch(n),i=o.status,i!==200)throw new Error;o=await o.json();}catch{r({status:"error",load_status:"error",message:li,detail:"NOT_FOUND"});return}if(!o||i!==200)return;const{runtime:{stage:s},id:a}=o;switch(s){case "STOPPED":case "SLEEPING":r({status:"sleeping",load_status:"pending",message:"Space is asleep. Waking it up...",detail:s}),setTimeout(()=>{pe$2(e,t,r);},1e3);break;case "PAUSED":r({status:"paused",load_status:"error",message:"This space has been paused by the author. If you would like to try this demo, consider duplicating the space.",detail:s,discussions_enabled:await Gt$1(a)});break;case "RUNNING":case "RUNNING_BUILDING":r({status:"running",load_status:"complete",message:"Space is running.",detail:s});break;case "BUILDING":r({status:"building",load_status:"pending",message:"Space is building...",detail:s}),setTimeout(()=>{pe$2(e,t,r);},1e3);break;case "APP_STARTING":r({status:"starting",load_status:"pending",message:"Space is starting...",detail:s}),setTimeout(()=>{pe$2(e,t,r);},1e3);break;default:r({status:"space_error",load_status:"error",message:"This space is experiencing an issue.",detail:s,discussions_enabled:await Gt$1(a)});break}}const Wr=async(e,t)=>{let r=0;const n=12,o=5e3;return new Promise(i=>{pe$2(e,ct$1.test(e)?"space_name":"subdomain",s=>{t(s),s.status==="running"||s.status==="error"||s.status==="paused"||s.status==="space_error"?i():(s.status==="sleeping"||s.status==="building")&&(r<n?(r++,setTimeout(()=>{Wr(e,t).then(i);},o)):i());});})},$i=/^(?=[^]*\b[dD]iscussions{0,1}\b)(?=[^]*\b[dD]isabled\b)[^]*$/;async function Gt$1(e){try{const t=await fetch(`https://huggingface.co/api/spaces/${e}/discussions`,{method:"HEAD"}),r=t.headers.get("x-error-message");return !(!t.ok||r&&$i.test(r))}catch{return  false}}async function Gi(e,t){const r={};t&&(r.Authorization=`Bearer ${t}`);try{const n=await fetch(`https://huggingface.co/api/spaces/${e}/${ni}`,{headers:r});if(n.status!==200)throw new Error("Space hardware could not be obtained.");const{hardware:o}=await n.json();return o.current}catch(n){throw new Error(n.message)}}async function Fi(e,t,r){const n={};r&&(n.Authorization=`Bearer ${r}`);const o={seconds:t};try{const i=await fetch(`https://huggingface.co/api/spaces/${e}/${oi}`,{method:"POST",headers:{"Content-Type":"application/json",...n},body:JSON.stringify(o)});if(i.status!==200)throw new Error("Could not set sleep timeout on duplicated Space. Please visit *ADD HF LINK TO SETTINGS* to set a timeout manually to reduce billing charges.");return await i.json()}catch(i){throw new Error(i.message)}}const Ft$2=["cpu-basic","cpu-upgrade","cpu-xl","t4-small","t4-medium","a10g-small","a10g-large","a10g-largex2","a10g-largex4","a100-large","zero-a10g","h100","h100x8"];async function zi(e,t){const{token:r,private:n,hardware:o,timeout:i,auth:s}=t;if(o&&!Ft$2.includes(o))throw new Error(`Invalid hardware type provided. Valid types are: ${Ft$2.map(E=>`"${E}"`).join(",")}.`);const{http_protocol:a,host:h}=await ut$1(e,r);let c=null;if(s){const E=await zr(a,h,s,fetch);E&&(c=qr(E));}const l={Authorization:`Bearer ${r}`,"Content-Type":"application/json",...c?{Cookie:c.join("; ")}:{}},u=(await(await fetch("https://huggingface.co/api/whoami-v2",{headers:l})).json()).name,f=e.split("/")[1],_={repository:`${u}/${f}`};n&&(_.private=true);let P;try{o||(P=await Gi(e,r));}catch(E){throw Error(at$1+E.message)}const d=o||P||"cpu-basic";_.hardware=d;try{const E=await fetch(`https://huggingface.co/api/spaces/${e}/duplicate`,{method:"POST",headers:l,body:JSON.stringify(_)});if(E.status===409)try{return await qt$1.connect(`${u}/${f}`,t)}catch(m){throw console.error("Failed to connect Client instance:",m),m}else if(E.status!==200)throw new Error(E.statusText);const p=await E.json();return await Fi(`${u}/${f}`,i||300,r),await qt$1.connect(qi(p.url),t)}catch(E){throw new Error(E)}}function qi(e){const t=/https:\/\/huggingface.co\/spaces\/([^/]+\/[^/]+)/,r=e.match(t);if(r)return r[1]}class Vi extends TransformStream{#e="";constructor(t={allowCR:false}){super({transform:(r,n)=>{for(r=this.#e+r;;){const o=r.indexOf(`
`),i=t.allowCR?r.indexOf("\r"):-1;if(i!==-1&&i!==r.length-1&&(o===-1||o-1>i)){n.enqueue(r.slice(0,i)),r=r.slice(i+1);continue}if(o===-1)break;const s=r[o-1]==="\r"?o-1:o;n.enqueue(r.slice(0,s)),r=r.slice(o+1);}this.#e=r;},flush:r=>{if(this.#e==="")return;const n=t.allowCR&&this.#e.endsWith("\r")?this.#e.slice(0,-1):this.#e;r.enqueue(n);}});}}function Xi(e){let t=new TextDecoderStream,r=new Vi({allowCR:true});return e.pipeThrough(t).pipeThrough(r)}function Wi(e){let r=/[:]\s*/.exec(e),n=r&&r.index;if(n)return [e.substring(0,n),e.substring(n+r[0].length)]}function zt(e,t,r){e.get(t)||e.set(t,r);}async function*Zi(e,t){if(!e.body)return;let r=Xi(e.body),n,o=r.getReader(),i;for(;;){if(t&&t.aborted)return o.cancel();if(n=await o.read(),n.done)return;if(!n.value){i&&(yield i),i=void 0;continue}let[s,a]=Wi(n.value)||[];s==="data"?(i||={},i[s]=i[s]?i[s]+`
`+a:a):s==="event"?(i||={},i[s]=a):s==="id"?(i||={},i[s]=String(+a)===a?+a:a):s==="retry"&&(i||={},i[s]=+a||void 0);}}async function Ji(e,t){let r=new Request(e,t);zt(r.headers,"Accept","text/event-stream"),zt(r.headers,"Content-Type","application/json");let n=await fetch(r);if(!n.ok)throw n;return Zi(n,r.signal)}async function Qi(){let{event_callbacks:e,unclosed_events:t,pending_stream_messages:r,stream_status:n,config:o,jwt:i}=this;const s=this;if(!o)throw new Error("Could not resolve app config");n.open=true;let a=null,h=new URLSearchParams({session_hash:this.session_hash}).toString(),c=new URL(`${o.root}${this.api_prefix}/${jr}?${h}`);if(i&&c.searchParams.set("__sign",i),a=this.stream(c),!a){console.warn("Cannot connect to SSE endpoint: "+c.toString());return}a.onmessage=async function(l){let u=JSON.parse(l.data);if(u.msg==="close_stream"){lt$1(n,s.abort_controller);return}const f=u.event_id;if(!f)await Promise.all(Object.keys(e).map(_=>e[_](u)));else if(e[f]&&o){u.msg==="process_completed"&&["sse","sse_v1","sse_v2","sse_v2.1","sse_v3"].includes(o.protocol)&&t.delete(f);let _=e[f];typeof window<"u"&&typeof document<"u"?setTimeout(_,0,u):_(u);}else r[f]||(r[f]=[]),r[f].push(u);},a.onerror=async function(l){console.error(l),await Promise.all(Object.keys(e).map(u=>e[u]({msg:"broken_connection",message:_e$2})));};}function lt$1(e,t){e&&(e.open=false,t?.abort());}function Yi(e,t,r){!e[t]?(e[t]=[],r.data.forEach((o,i)=>{e[t][i]=o;})):r.data.forEach((o,i)=>{let s=Ki(e[t][i],o);e[t][i]=s,r.data[i]=s;});}function Ki(e,t){return t.forEach(([r,n,o])=>{e=es(e,n,r,o);}),e}function es(e,t,r,n){if(t.length===0){if(r==="replace")return n;if(r==="append")return e+n;throw new Error(`Unsupported action: ${r}`)}let o=e;for(let s=0;s<t.length-1;s++)o=o[t[s]];const i=t[t.length-1];switch(r){case "replace":o[i]=n;break;case "append":o[i]+=n;break;case "add":Array.isArray(o)?o.splice(Number(i),0,n):o[i]=n;break;case "delete":Array.isArray(o)?o.splice(Number(i),1):delete o[i];break;default:throw new Error(`Unknown action: ${r}`)}return e}function ts(e,t={}){const r={close:()=>{console.warn("Method not implemented.");},onerror:null,onmessage:null,onopen:null,readyState:0,url:e.toString(),withCredentials:false,CONNECTING:0,OPEN:1,CLOSED:2,addEventListener:()=>{throw new Error("Method not implemented.")},dispatchEvent:()=>{throw new Error("Method not implemented.")},removeEventListener:()=>{throw new Error("Method not implemented.")}};return Ji(e,t).then(async n=>{r.readyState=r.OPEN;try{for await(const o of n)r.onmessage&&r.onmessage(o);r.readyState=r.CLOSED;}catch(o){r.onerror&&r.onerror(o),r.readyState=r.CLOSED;}}).catch(n=>{console.error(n),r.onerror&&r.onerror(n),r.readyState=r.CLOSED;}),r}function rs(e,t={},r,n,o,i){try{let s=function(x){(o||Qr[x.type])&&l(x);},a=function(){for(tn=!0;ce.length>0;)ce.shift()({value:void 0,done:!0});},h=function(x){ce.length>0?ce.shift()(x):Le.push(x);},c=function(x){h(ns(x)),a();},l=function(x){h({value:x,done:!1});},u=function(){return Le.length>0?Promise.resolve(Le.shift()):new Promise(x=>ce.push(x))};const{token:f}=this.options,{fetch:_,app_reference:P,config:d,session_hash:E,api_info:p,api_map:m,stream_status:g,pending_stream_messages:H,pending_diff_streams:S,event_callbacks:M,unclosed_events:ge,post_data:Ie,options:be,api_prefix:k}=this,ht=i||{"x-gradio-user":"api"},Zr=this;if(!p)throw new Error("No API found");if(!d)throw new Error("Could not resolve app config");let{fn_index:v,endpoint_info:ft,dependency:se}=os(p,e,m,d),Jr=Ti(t,ft),K,U=d.protocol??"ws";if(U==="ws")throw new Error("WebSocket protocol is not supported in this version");let ee="",is=()=>ee;const T=typeof e=="number"?"/predict":e;let ye,B=null,j=!1,pt={},ae=typeof window<"u"&&typeof document<"u"?new URLSearchParams(window.location.search).toString():"";const Qr=be?.events?.reduce((x,D)=>(x[D]=!0,x),{})||{};async function Yr(){let x={},D={};x={event_id:B},D={event_id:B,session_hash:E,fn_index:v};try{if(!d)throw new Error("Could not resolve app config");"event_id"in D&&await _(`${d.root}${k}/${ci}`,{headers:{"Content-Type":"application/json"},method:"POST",body:JSON.stringify(D)}),await _(`${d.root}${k}/${ai}`,{headers:{"Content-Type":"application/json"},method:"POST",body:JSON.stringify(x)});}catch{console.warn("The `/reset` endpoint could not be called. Subsequent endpoint results may be unreliable.");}}const Kr=async x=>{await this._resolve_heartbeat(x);};async function dt(x){if(!d)return;let D=x.render_id;d.components=[...d.components.filter(N=>N.props.rendered_in!==D),...x.components],d.dependencies=[...d.dependencies.filter(N=>N.rendered_in!==D),...x.dependencies];const we=d.components.some(N=>N.type==="state"),O=d.dependencies.some(N=>N.targets.some(X=>X[1]==="unload"));d.connect_heartbeat=we||O,await Kr(d),s({type:"render",data:x,endpoint:T,fn_index:v});}const en=this.handle_blob(d.root,Jr,ft).then(async x=>{if(ye={data:ve$2(x,se,d.components,"input",!0)||[],event_data:r,fn_index:v,trigger_id:n},Li(v,d))s({type:"status",endpoint:T,stage:"pending",queue:!1,fn_index:v,time:new Date}),Ie(`${d.root}${k}/run${T.startsWith("/")?T:`/${T}`}${ae?"?"+ae:""}`,{...ye,session_hash:E},ht).then(async([O,N])=>{const X=O.data;N==200?(s({type:"data",endpoint:T,fn_index:v,data:ve$2(X,se,d.components,"output",be.with_null_state),time:new Date,event_data:r,trigger_id:n}),O.render_config&&await dt(O.render_config),s({type:"status",endpoint:T,fn_index:v,stage:"complete",eta:O.average_duration,queue:!1,time:new Date})):s({type:"status",stage:"error",endpoint:T,fn_index:v,message:O.error,queue:!1,time:new Date});}).catch(O=>{s({type:"status",stage:"error",message:O.message,endpoint:T,fn_index:v,queue:!1,time:new Date});});else if(U=="sse"){s({type:"status",stage:"pending",queue:!0,endpoint:T,fn_index:v,time:new Date});var we=new URLSearchParams({fn_index:v.toString(),session_hash:E}).toString();let O=new URL(`${d.root}${k}/${jr}?${ae?ae+"&":""}${we}`);if(this.jwt&&O.searchParams.set("__sign",this.jwt),K=this.stream(O),!K)return Promise.reject(new Error("Cannot connect to SSE endpoint: "+O.toString()));K.onmessage=async function(N){const X=JSON.parse(N.data),{type:W,status:$,data:G}=Ut$1(X,pt[v]);if(W==="update"&&$&&!j)s({type:"status",endpoint:T,fn_index:v,time:new Date,...$}),$.stage==="error"&&(K?.close(),a());else if(W==="data"){let[F,Z]=await Ie(`${d.root}${k}/queue/data`,{...ye,session_hash:E,event_id:B});Z!==200&&(s({type:"status",stage:"error",message:_e$2,queue:!0,endpoint:T,fn_index:v,time:new Date}),K?.close(),a());}else W==="complete"?j=$:W==="log"?s({type:"log",title:G.title,log:G.log,level:G.level,endpoint:T,duration:G.duration,visible:G.visible,fn_index:v}):(W==="generating"||W==="streaming")&&s({type:"status",time:new Date,...$,stage:$?.stage,queue:!0,endpoint:T,fn_index:v});G&&(s({type:"data",time:new Date,data:ve$2(G.data,se,d.components,"output",be.with_null_state),endpoint:T,fn_index:v,event_data:r,trigger_id:n}),j&&(s({type:"status",time:new Date,...j,stage:$?.stage,queue:!0,endpoint:T,fn_index:v}),K?.close(),a()));};}else if(U=="sse_v1"||U=="sse_v2"||U=="sse_v2.1"||U=="sse_v3"){s({type:"status",stage:"pending",queue:!0,endpoint:T,fn_index:v,time:new Date});let O="";typeof window<"u"&&typeof document<"u"&&(O=window?.location?.hostname);const X=O.includes(".dev.")?`https://moon-${O.split(".")[1]}.dev.spaces.huggingface.tech`:"https://huggingface.co";return (typeof window<"u"&&typeof document<"u"&&window.parent!=window&&window.supports_zerogpu_headers?Ri("zerogpu-headers",X):Promise.resolve(null)).then(F=>{const Z={...ht,...F||{}};return Ie(`${d.root}${k}/${ei}?${ae}`,{...ye,session_hash:E},Z)}).then(async([F,Z])=>{if(F.event_id&&(ee=F.event_id),Z===503)s({type:"status",stage:"error",message:$r,queue:!0,endpoint:T,fn_index:v,time:new Date,visible:!0});else if(Z===422)s({type:"status",stage:"error",message:F.detail,queue:!0,endpoint:T,fn_index:v,code:"validation_error",time:new Date,visible:!0}),a();else if(Z!==200)s({type:"status",stage:"error",broken:!1,message:F.detail,queue:!0,endpoint:T,fn_index:v,time:new Date,visible:!0});else {B=F.event_id,ee=B;let _t=async function(Re){try{const{type:I,status:L,data:R,original_msg:rn}=Ut$1(Re,pt[v]);if(I=="heartbeat")return;if(I==="update"&&L&&!j)s({type:"status",endpoint:T,fn_index:v,time:new Date,original_msg:rn,...L});else if(I==="complete")j=L;else if(I=="unexpected_error"||I=="broken_connection"){console.error("Unexpected error",L?.message);const nn=I==="broken_connection";s({type:"status",stage:"error",message:L?.message||"An Unexpected Error Occurred!",queue:!0,endpoint:T,broken:nn,session_not_found:L?.session_not_found,fn_index:v,time:new Date});}else if(I==="log"){s({type:"log",title:R.title,log:R.log,level:R.level,endpoint:T,duration:R.duration,visible:R.visible,fn_index:v});return}else (I==="generating"||I==="streaming")&&(s({type:"status",time:new Date,...L,stage:L?.stage,queue:!0,endpoint:T,fn_index:v}),R&&se.connection!=="stream"&&["sse_v2","sse_v2.1","sse_v3"].includes(U)&&Yi(S,B,R));R&&(s({type:"data",time:new Date,data:ve$2(R.data,se,d.components,"output",be.with_null_state),endpoint:T,fn_index:v}),R.render_config&&await dt(R.render_config),j&&(s({type:"status",time:new Date,...j,stage:L?.stage,queue:!0,endpoint:T,fn_index:v}),a())),(L?.stage==="complete"||L?.stage==="error")&&(M[B]&&delete M[B],B in S&&delete S[B]);}catch(I){console.error("Unexpected client exception",I),s({type:"status",stage:"error",message:"An Unexpected Error Occurred!",queue:!0,endpoint:T,fn_index:v,time:new Date}),["sse_v2","sse_v2.1","sse_v3"].includes(U)&&(lt$1(g,Zr.abort_controller),g.open=!1,a());}};B in H&&(H[B].forEach(Re=>_t(Re)),delete H[B]),M[B]=_t,ge.add(B),g.open||await this.open_stream();}})}});let tn=!1;const Le=[],ce=[],mt={[Symbol.asyncIterator]:()=>mt,next:u,throw:async x=>(c(x),u()),return:async()=>(a(),{value:void 0,done:!0}),cancel:Yr,send_chunk:x=>{this.post_data(`${d.root}${k}/stream/${ee}`,{...x,session_hash:this.session_hash});},close_stream:()=>{this.post_data(`${d.root}${k}/stream/${ee}/close`,{}),a();},event_id:()=>ee,wait_for_id:async()=>(await en,B)};return mt}catch(s){throw console.error("Submit function encountered an error:",s),s}}function ns(e){return {then:(t,r)=>r(e)}}function os(e,t,r,n){let o,i,s;if(typeof t=="number")o=t,i=e.unnamed_endpoints[o],s=n.dependencies.find(a=>a.id==t);else {const a=t.replace(/^\//,"");o=r[a],i=e.named_endpoints[t.trim()],s=n.dependencies.find(h=>h.id==r[a]);}if(typeof o!="number")throw new Error("There is no endpoint matching that name of fn_index matching that number.");return {fn_index:o,endpoint_info:i,dependency:s}}let qt$1 = class qt{app_reference;options;deep_link=null;config;api_prefix="";api_info;api_map={};session_hash=Math.random().toString(36).substring(2);jwt=false;last_status={};cookies=null;stream_status={open:false};closed=false;pending_stream_messages={};pending_diff_streams={};event_callbacks={};unclosed_events=new Set;heartbeat_event=null;abort_controller=null;stream_instance=null;current_payload;get_url_config(t=null){if(!this.config)throw new Error(J$3);t===null&&(t=window.location.href);const r=s=>s.replace(/^\/+|\/+$/g,"");let n=r(new URL(this.config.root).pathname),o=r(new URL(t).pathname),i;return o.startsWith(n)?i=r(o.substring(n.length)):i="",this.get_page_config(i)}get_page_config(t){if(!this.config)throw new Error(J$3);let r=this.config;return t in r.page||(t=""),{...r,current_page:t,layout:r.page[t].layout,components:r.components.filter(n=>r.page[t].components.includes(n.id)),dependencies:this.config.dependencies.filter(n=>r.page[t].dependencies.includes(n.id))}}fetch(t,r){const n=new Headers(r?.headers||{});return this&&this.cookies&&n.append("Cookie",this.cookies),this&&this.options.headers&&new Headers(this.options.headers).forEach((i,s)=>{n.append(s,i);}),fetch(t,{...r,headers:n})}stream(t){const r=new Headers;return this&&this.cookies&&r.append("Cookie",this.cookies),this&&this.options.headers&&new Headers(this.options.headers).forEach((o,i)=>{r.append(i,o);}),this&&this.options.token&&r.append("Authorization",`Bearer ${this.options.token}`),this.abort_controller=new AbortController,this.stream_instance=ts(t.toString(),{credentials:"include",headers:r,signal:this.abort_controller.signal}),this.stream_instance}view_api;upload_files;upload;handle_blob;post_data;submit;predict;open_stream;resolve_config;resolve_cookies;constructor(t,r={events:["data"]}){this.app_reference=t,this.deep_link=r.query_params?.deep_link||null,r.events||(r.events=["data"]),this.options=r,this.current_payload={},this.view_api=Ai.bind(this),this.upload_files=Pi.bind(this),this.handle_blob=Mi.bind(this),this.post_data=Ui.bind(this),this.submit=rs.bind(this),this.predict=ji.bind(this),this.open_stream=Qi.bind(this),this.resolve_config=bi.bind(this),this.resolve_cookies=wi.bind(this),this.upload=Ni.bind(this),this.fetch=this.fetch.bind(this),this.handle_space_success=this.handle_space_success.bind(this),this.stream=this.stream.bind(this);}async init(){this.options.auth&&await this.resolve_cookies(),await this._resolve_config().then(({config:t})=>this._resolve_heartbeat(t)),this.api_info=await this.view_api(),this.api_map=gi(this.config?.dependencies||[]);}async _resolve_heartbeat(t){if(t&&(this.config=t,this.api_prefix=t.api_prefix||"",this.config&&this.config.connect_heartbeat&&this.config.space_id&&this.options.token&&(this.jwt=await kt$1(this.config.space_id,this.options.token,this.cookies))),t.space_id&&this.options.token&&(this.jwt=await kt$1(t.space_id,this.options.token)),this.config&&this.config.connect_heartbeat){const r=new URL(`${this.config.root}${this.api_prefix}/${ii}/${this.session_hash}`);this.jwt&&r.searchParams.set("__sign",this.jwt),this.heartbeat_event||(this.heartbeat_event=this.stream(r));}}static async connect(t,r={events:["data"]}){const n=new this(t,r);return r.session_hash&&(n.session_hash=r.session_hash),await n.init(),n}async reconnect(){const t=new URL(`${this.config.root}${this.api_prefix}/${ui}`);let r;try{const n=await this.fetch(t);if(!n.ok)throw new Error;r=(await n.json()).app_id;}catch{return "broken"}return r!==this.config.app_id?"changed":"connected"}close(){this.closed=true,lt$1(this.stream_status,this.abort_controller);}set_current_payload(t){this.current_payload=t;}static async duplicate(t,r={events:["data"]}){return zi(t,r)}async _resolve_config(){const{http_protocol:t,host:r,space_id:n}=await ut$1(this.app_reference,this.options.token),{status_callback:o}=this.options;n&&o&&await Wr(n,o);let i;try{let s=`${t}//${r}`;if(i=await this.resolve_config(s),!i)throw new Error(J$3);return this.config_success(i)}catch(s){if(n&&o)pe$2(n,ct$1.test(n)?"space_name":"subdomain",this.handle_space_success);else throw o&&o({status:"error",message:"Could not load this space.",load_status:"error",detail:"NOT_FOUND"}),Error(s)}}async config_success(t){if(this.config=t,this.api_prefix=t.api_prefix||"",this.config.auth_required)return this.prepare_return_obj();try{this.api_info=await this.view_api();}catch(r){console.error(hi+r.message);}return this.prepare_return_obj()}async handle_space_success(t){if(!this)throw new Error(J$3);const{status_callback:r}=this.options;if(r&&r(t),t.status==="running")try{if(this.config=await this._resolve_config(),this.api_prefix=this?.config?.api_prefix||"",!this.config)throw new Error(J$3);return await this.config_success(this.config)}catch(n){throw r&&r({status:"error",message:"Could not load this space.",load_status:"error",detail:"NOT_FOUND"}),n}}async component_server(t,r,n){if(!this.config)throw new Error(J$3);const o={},{token:i}=this.options,{session_hash:s}=this;i&&(o.Authorization=`Bearer ${this.options.token}`);let a,h=this.config.components.find(l=>l.id===t);h?.props?.root_url?a=h.props.root_url:a=this.config.root;let c;if("binary"in n){c=new FormData;for(const l in n.data)l!=="binary"&&c.append(l,n.data[l]);c.set("component_id",t.toString()),c.set("fn_name",r),c.set("session_hash",s);}else c=JSON.stringify({data:n,component_id:t,fn_name:r,session_hash:s}),o["Content-Type"]="application/json";i&&(o.Authorization=`Bearer ${i}`);try{const l=await this.fetch(`${a}${this.api_prefix}/${si}/`,{method:"POST",body:c,headers:o,credentials:"include"});if(!l.ok)throw new Error("Could not connect to component server: "+l.statusText);return await l.json()}catch(l){console.warn(l);}}set_cookies(t){this.cookies=qr(t).join("; ");}prepare_return_obj(){return {config:this.config,predict:this.predict,submit:this.submit,view_api:this.view_api,component_server:this.component_server}}};

var O$2={exports:{}},X$1;function ae$2(){return X$1||(X$1=1,(function(G){var N=typeof window<"u"?window:typeof WorkerGlobalScope<"u"&&self instanceof WorkerGlobalScope?self:{};var i=(function(g){var h=/(?:^|\s)lang(?:uage)?-([\w-]+)(?=\s|$)/i,y=0,F={},s={manual:g.Prism&&g.Prism.manual,disableWorkerMessageHandler:g.Prism&&g.Prism.disableWorkerMessageHandler,util:{encode:function t(e){return e instanceof b?new b(e.type,t(e.content),e.alias):Array.isArray(e)?e.map(t):e.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/\u00a0/g," ")},type:function(t){return Object.prototype.toString.call(t).slice(8,-1)},objId:function(t){return t.__id||Object.defineProperty(t,"__id",{value:++y}),t.__id},clone:function t(e,a){a=a||{};var n,r;switch(s.util.type(e)){case "Object":if(r=s.util.objId(e),a[r])return a[r];n={},a[r]=n;for(var l in e)e.hasOwnProperty(l)&&(n[l]=t(e[l],a));return n;case "Array":return r=s.util.objId(e),a[r]?a[r]:(n=[],a[r]=n,e.forEach(function(o,u){n[u]=t(o,a);}),n);default:return e}},getLanguage:function(t){for(;t;){var e=h.exec(t.className);if(e)return e[1].toLowerCase();t=t.parentElement;}return "none"},setLanguage:function(t,e){t.className=t.className.replace(RegExp(h,"gi"),""),t.classList.add("language-"+e);},currentScript:function(){if(typeof document>"u")return null;if(document.currentScript&&document.currentScript.tagName==="SCRIPT")return document.currentScript;try{throw new Error}catch(n){var t=(/at [^(\r\n]*\((.*):[^:]+:[^:]+\)$/i.exec(n.stack)||[])[1];if(t){var e=document.getElementsByTagName("script");for(var a in e)if(e[a].src==t)return e[a]}return null}},isActive:function(t,e,a){for(var n="no-"+e;t;){var r=t.classList;if(r.contains(e))return  true;if(r.contains(n))return  false;t=t.parentElement;}return !!a}},languages:{plain:F,plaintext:F,text:F,txt:F,extend:function(t,e){var a=s.util.clone(s.languages[t]);for(var n in e)a[n]=e[n];return a},insertBefore:function(t,e,a,n){n=n||s.languages;var r=n[t],l={};for(var o in r)if(r.hasOwnProperty(o)){if(o==e)for(var u in a)a.hasOwnProperty(u)&&(l[u]=a[u]);a.hasOwnProperty(o)||(l[o]=r[o]);}var d=n[t];return n[t]=l,s.languages.DFS(s.languages,function(m,A){A===d&&m!=t&&(this[m]=l);}),l},DFS:function t(e,a,n,r){r=r||{};var l=s.util.objId;for(var o in e)if(e.hasOwnProperty(o)){a.call(e,o,e[o],n||o);var u=e[o],d=s.util.type(u);d==="Object"&&!r[l(u)]?(r[l(u)]=true,t(u,a,null,r)):d==="Array"&&!r[l(u)]&&(r[l(u)]=true,t(u,a,o,r));}}},plugins:{},highlightAll:function(t,e){s.highlightAllUnder(document,t,e);},highlightAllUnder:function(t,e,a){var n={callback:a,container:t,selector:'code[class*="language-"], [class*="language-"] code, code[class*="lang-"], [class*="lang-"] code'};s.hooks.run("before-highlightall",n),n.elements=Array.prototype.slice.apply(n.container.querySelectorAll(n.selector)),s.hooks.run("before-all-elements-highlight",n);for(var r=0,l;l=n.elements[r++];)s.highlightElement(l,e===true,n.callback);},highlightElement:function(t,e,a){var n=s.util.getLanguage(t),r=s.languages[n];s.util.setLanguage(t,n);var l=t.parentElement;l&&l.nodeName.toLowerCase()==="pre"&&s.util.setLanguage(l,n);var o=t.textContent,u={element:t,language:n,grammar:r,code:o};function d(A){u.highlightedCode=A,s.hooks.run("before-insert",u),u.element.innerHTML=u.highlightedCode,s.hooks.run("after-highlight",u),s.hooks.run("complete",u),a&&a.call(u.element);}if(s.hooks.run("before-sanity-check",u),l=u.element.parentElement,l&&l.nodeName.toLowerCase()==="pre"&&!l.hasAttribute("tabindex")&&l.setAttribute("tabindex","0"),!u.code){s.hooks.run("complete",u),a&&a.call(u.element);return}if(s.hooks.run("before-highlight",u),!u.grammar){d(s.util.encode(u.code));return}if(e&&g.Worker){var m=new Worker(s.filename);m.onmessage=function(A){d(A.data);},m.postMessage(JSON.stringify({language:u.language,code:u.code,immediateClose:true}));}else d(s.highlight(u.code,u.grammar,u.language));},highlight:function(t,e,a){var n={code:t,grammar:e,language:a};if(s.hooks.run("before-tokenize",n),!n.grammar)throw new Error('The language "'+n.language+'" has no grammar.');return n.tokens=s.tokenize(n.code,n.grammar),s.hooks.run("after-tokenize",n),b.stringify(s.util.encode(n.tokens),n.language)},tokenize:function(t,e){var a=e.rest;if(a){for(var n in a)e[n]=a[n];delete e.rest;}var r=new _;return S(r,r.head,t),T(t,r,e,r.head,0),C(r)},hooks:{all:{},add:function(t,e){var a=s.hooks.all;a[t]=a[t]||[],a[t].push(e);},run:function(t,e){var a=s.hooks.all[t];if(!(!a||!a.length))for(var n=0,r;r=a[n++];)r(e);}},Token:b};g.Prism=s;function b(t,e,a,n){this.type=t,this.content=e,this.alias=a,this.length=(n||"").length|0;}b.stringify=function t(e,a){if(typeof e=="string")return e;if(Array.isArray(e)){var n="";return e.forEach(function(d){n+=t(d,a);}),n}var r={type:e.type,content:t(e.content,a),tag:"span",classes:["token",e.type],attributes:{},language:a},l=e.alias;l&&(Array.isArray(l)?Array.prototype.push.apply(r.classes,l):r.classes.push(l)),s.hooks.run("wrap",r);var o="";for(var u in r.attributes)o+=" "+u+'="'+(r.attributes[u]||"").replace(/"/g,"&quot;")+'"';return "<"+r.tag+' class="'+r.classes.join(" ")+'"'+o+">"+r.content+"</"+r.tag+">"};function E(t,e,a,n){t.lastIndex=e;var r=t.exec(a);if(r&&n&&r[1]){var l=r[1].length;r.index+=l,r[0]=r[0].slice(l);}return r}function T(t,e,a,n,r,l){for(var o in a)if(!(!a.hasOwnProperty(o)||!a[o])){var u=a[o];u=Array.isArray(u)?u:[u];for(var d=0;d<u.length;++d){if(l&&l.cause==o+","+d)return;var m=u[d],A=m.inside,H=!!m.lookbehind,Z=!!m.greedy,K=m.alias;if(Z&&!m.pattern.global){var Q=m.pattern.toString().match(/[imsuy]*$/)[0];m.pattern=RegExp(m.pattern.source,Q+"g");}for(var B=m.pattern||m,v=n.next,w=r;v!==e.tail&&!(l&&w>=l.reach);w+=v.value.length,v=v.next){var $=v.value;if(e.length>t.length)return;if(!($ instanceof b)){var z=1,x;if(Z){if(x=E(B,w,t,H),!x||x.index>=t.length)break;var L=x.index,V=x.index+x[0].length,k=w;for(k+=v.value.length;L>=k;)v=v.next,k+=v.value.length;if(k-=v.value.length,w=k,v.value instanceof b)continue;for(var P=v;P!==e.tail&&(k<V||typeof P.value=="string");P=P.next)z++,k+=P.value.length;z--,$=t.slice(w,k),x.index-=w;}else if(x=E(B,0,$,H),!x)continue;var L=x.index,I=x[0],M=$.slice(0,L),U=$.slice(L+I.length),R=w+$.length;l&&R>l.reach&&(l.reach=R);var D=v.prev;M&&(D=S(e,D,M),w+=M.length),j(e,D,z);var ee=new b(o,A?s.tokenize(I,A):I,K,I);if(v=S(e,D,ee),U&&S(e,v,U),z>1){var q={cause:o+","+d,reach:R};T(t,e,a,v.prev,w,q),l&&q.reach>l.reach&&(l.reach=q.reach);}}}}}}function _(){var t={value:null,prev:null,next:null},e={value:null,prev:t,next:null};t.next=e,this.head=t,this.tail=e,this.length=0;}function S(t,e,a){var n=e.next,r={value:a,prev:e,next:n};return e.next=r,n.prev=r,t.length++,r}function j(t,e,a){for(var n=e.next,r=0;r<a&&n!==t.tail;r++)n=n.next;e.next=n,n.prev=e,t.length-=r;}function C(t){for(var e=[],a=t.head.next;a!==t.tail;)e.push(a.value),a=a.next;return e}if(!g.document)return g.addEventListener&&(s.disableWorkerMessageHandler||g.addEventListener("message",function(t){var e=JSON.parse(t.data),a=e.language,n=e.code,r=e.immediateClose;g.postMessage(s.highlight(n,s.languages[a],a)),r&&g.close();},false)),s;var p=s.util.currentScript();p&&(s.filename=p.src,p.hasAttribute("data-manual")&&(s.manual=true));function c(){s.manual||s.highlightAll();}if(!s.manual){var f=document.readyState;f==="loading"||f==="interactive"&&p&&p.defer?document.addEventListener("DOMContentLoaded",c):window.requestAnimationFrame?window.requestAnimationFrame(c):window.setTimeout(c,16);}return s})(N);G.exports&&(G.exports=i),typeof us<"u"&&(us.Prism=i),i.languages.markup={comment:{pattern:/<!--(?:(?!<!--)[\s\S])*?-->/,greedy:true},prolog:{pattern:/<\?[\s\S]+?\?>/,greedy:true},doctype:{pattern:/<!DOCTYPE(?:[^>"'[\]]|"[^"]*"|'[^']*')+(?:\[(?:[^<"'\]]|"[^"]*"|'[^']*'|<(?!!--)|<!--(?:[^-]|-(?!->))*-->)*\]\s*)?>/i,greedy:true,inside:{"internal-subset":{pattern:/(^[^\[]*\[)[\s\S]+(?=\]>$)/,lookbehind:true,greedy:true,inside:null},string:{pattern:/"[^"]*"|'[^']*'/,greedy:true},punctuation:/^<!|>$|[[\]]/,"doctype-tag":/^DOCTYPE/i,name:/[^\s<>'"]+/}},cdata:{pattern:/<!\[CDATA\[[\s\S]*?\]\]>/i,greedy:true},tag:{pattern:/<\/?(?!\d)[^\s>\/=$<%]+(?:\s(?:\s*[^\s>\/=]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))|(?=[\s/>])))+)?\s*\/?>/,greedy:true,inside:{tag:{pattern:/^<\/?[^\s>\/]+/,inside:{punctuation:/^<\/?/,namespace:/^[^\s>\/:]+:/}},"special-attr":[],"attr-value":{pattern:/=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+)/,inside:{punctuation:[{pattern:/^=/,alias:"attr-equals"},{pattern:/^(\s*)["']|["']$/,lookbehind:true}]}},punctuation:/\/?>/,"attr-name":{pattern:/[^\s>\/]+/,inside:{namespace:/^[^\s>\/:]+:/}}}},entity:[{pattern:/&[\da-z]{1,8};/i,alias:"named-entity"},/&#x?[\da-f]{1,8};/i]},i.languages.markup.tag.inside["attr-value"].inside.entity=i.languages.markup.entity,i.languages.markup.doctype.inside["internal-subset"].inside=i.languages.markup,i.hooks.add("wrap",function(g){g.type==="entity"&&(g.attributes.title=g.content.replace(/&amp;/,"&"));}),Object.defineProperty(i.languages.markup.tag,"addInlined",{value:function(h,y){var F={};F["language-"+y]={pattern:/(^<!\[CDATA\[)[\s\S]+?(?=\]\]>$)/i,lookbehind:true,inside:i.languages[y]},F.cdata=/^<!\[CDATA\[|\]\]>$/i;var s={"included-cdata":{pattern:/<!\[CDATA\[[\s\S]*?\]\]>/i,inside:F}};s["language-"+y]={pattern:/[\s\S]+/,inside:i.languages[y]};var b={};b[h]={pattern:RegExp(/(<__[^>]*>)(?:<!\[CDATA\[(?:[^\]]|\](?!\]>))*\]\]>|(?!<!\[CDATA\[)[\s\S])*?(?=<\/__>)/.source.replace(/__/g,function(){return h}),"i"),lookbehind:true,greedy:true,inside:s},i.languages.insertBefore("markup","cdata",b);}}),Object.defineProperty(i.languages.markup.tag,"addAttribute",{value:function(g,h){i.languages.markup.tag.inside["special-attr"].push({pattern:RegExp(/(^|["'\s])/.source+"(?:"+g+")"+/\s*=\s*(?:"[^"]*"|'[^']*'|[^\s'">=]+(?=[\s>]))/.source,"i"),lookbehind:true,inside:{"attr-name":/^[^\s=]+/,"attr-value":{pattern:/=[\s\S]+/,inside:{value:{pattern:/(^=\s*(["']|(?!["'])))\S[\s\S]*(?=\2$)/,lookbehind:true,alias:[h,"language-"+h],inside:i.languages[h]},punctuation:[{pattern:/^=/,alias:"attr-equals"},/"|'/]}}}});}}),i.languages.html=i.languages.markup,i.languages.mathml=i.languages.markup,i.languages.svg=i.languages.markup,i.languages.xml=i.languages.extend("markup",{}),i.languages.ssml=i.languages.xml,i.languages.atom=i.languages.xml,i.languages.rss=i.languages.xml,(function(g){var h=/(?:"(?:\\(?:\r\n|[\s\S])|[^"\\\r\n])*"|'(?:\\(?:\r\n|[\s\S])|[^'\\\r\n])*')/;g.languages.css={comment:/\/\*[\s\S]*?\*\//,atrule:{pattern:RegExp("@[\\w-](?:"+/[^;{\s"']|\s+(?!\s)/.source+"|"+h.source+")*?"+/(?:;|(?=\s*\{))/.source),inside:{rule:/^@[\w-]+/,"selector-function-argument":{pattern:/(\bselector\s*\(\s*(?![\s)]))(?:[^()\s]|\s+(?![\s)])|\((?:[^()]|\([^()]*\))*\))+(?=\s*\))/,lookbehind:true,alias:"selector"},keyword:{pattern:/(^|[^\w-])(?:and|not|only|or)(?![\w-])/,lookbehind:true}}},url:{pattern:RegExp("\\burl\\((?:"+h.source+"|"+/(?:[^\\\r\n()"']|\\[\s\S])*/.source+")\\)","i"),greedy:true,inside:{function:/^url/i,punctuation:/^\(|\)$/,string:{pattern:RegExp("^"+h.source+"$"),alias:"url"}}},selector:{pattern:RegExp(`(^|[{}\\s])[^{}\\s](?:[^{};"'\\s]|\\s+(?![\\s{])|`+h.source+")*(?=\\s*\\{)"),lookbehind:true},string:{pattern:h,greedy:true},property:{pattern:/(^|[^-\w\xA0-\uFFFF])(?!\s)[-_a-z\xA0-\uFFFF](?:(?!\s)[-\w\xA0-\uFFFF])*(?=\s*:)/i,lookbehind:true},important:/!important\b/i,function:{pattern:/(^|[^-a-z0-9])[-a-z0-9]+(?=\()/i,lookbehind:true},punctuation:/[(){};:,]/},g.languages.css.atrule.inside.rest=g.languages.css;var y=g.languages.markup;y&&(y.tag.addInlined("style","css"),y.tag.addAttribute("style","css"));})(i),i.languages.clike={comment:[{pattern:/(^|[^\\])\/\*[\s\S]*?(?:\*\/|$)/,lookbehind:true,greedy:true},{pattern:/(^|[^\\:])\/\/.*/,lookbehind:true,greedy:true}],string:{pattern:/(["'])(?:\\(?:\r\n|[\s\S])|(?!\1)[^\\\r\n])*\1/,greedy:true},"class-name":{pattern:/(\b(?:class|extends|implements|instanceof|interface|new|trait)\s+|\bcatch\s+\()[\w.\\]+/i,lookbehind:true,inside:{punctuation:/[.\\]/}},keyword:/\b(?:break|catch|continue|do|else|finally|for|function|if|in|instanceof|new|null|return|throw|try|while)\b/,boolean:/\b(?:false|true)\b/,function:/\b\w+(?=\()/,number:/\b0x[\da-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e[+-]?\d+)?/i,operator:/[<>]=?|[!=]=?=?|--?|\+\+?|&&?|\|\|?|[?*/~^%]/,punctuation:/[{}[\];(),.:]/},i.languages.javascript=i.languages.extend("clike",{"class-name":[i.languages.clike["class-name"],{pattern:/(^|[^$\w\xA0-\uFFFF])(?!\s)[_$A-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\.(?:constructor|prototype))/,lookbehind:true}],keyword:[{pattern:/((?:^|\})\s*)catch\b/,lookbehind:true},{pattern:/(^|[^.]|\.\.\.\s*)\b(?:as|assert(?=\s*\{)|async(?=\s*(?:function\b|\(|[$\w\xA0-\uFFFF]|$))|await|break|case|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally(?=\s*(?:\{|$))|for|from(?=\s*(?:['"]|$))|function|(?:get|set)(?=\s*(?:[#\[$\w\xA0-\uFFFF]|$))|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)\b/,lookbehind:true}],function:/#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*(?:\.\s*(?:apply|bind|call)\s*)?\()/,number:{pattern:RegExp(/(^|[^\w$])/.source+"(?:"+(/NaN|Infinity/.source+"|"+/0[bB][01]+(?:_[01]+)*n?/.source+"|"+/0[oO][0-7]+(?:_[0-7]+)*n?/.source+"|"+/0[xX][\dA-Fa-f]+(?:_[\dA-Fa-f]+)*n?/.source+"|"+/\d+(?:_\d+)*n/.source+"|"+/(?:\d+(?:_\d+)*(?:\.(?:\d+(?:_\d+)*)?)?|\.\d+(?:_\d+)*)(?:[Ee][+-]?\d+(?:_\d+)*)?/.source)+")"+/(?![\w$])/.source),lookbehind:true},operator:/--|\+\+|\*\*=?|=>|&&=?|\|\|=?|[!=]==|<<=?|>>>?=?|[-+*/%&|^!=<>]=?|\.{3}|\?\?=?|\?\.?|[~:]/}),i.languages.javascript["class-name"][0].pattern=/(\b(?:class|extends|implements|instanceof|interface|new)\s+)[\w.\\]+/,i.languages.insertBefore("javascript","keyword",{regex:{pattern:RegExp(/((?:^|[^$\w\xA0-\uFFFF."'\])\s]|\b(?:return|yield))\s*)/.source+/\//.source+"(?:"+/(?:\[(?:[^\]\\\r\n]|\\.)*\]|\\.|[^/\\\[\r\n])+\/[dgimyus]{0,7}/.source+"|"+/(?:\[(?:[^[\]\\\r\n]|\\.|\[(?:[^[\]\\\r\n]|\\.|\[(?:[^[\]\\\r\n]|\\.)*\])*\])*\]|\\.|[^/\\\[\r\n])+\/[dgimyus]{0,7}v[dgimyus]{0,7}/.source+")"+/(?=(?:\s|\/\*(?:[^*]|\*(?!\/))*\*\/)*(?:$|[\r\n,.;:})\]]|\/\/))/.source),lookbehind:true,greedy:true,inside:{"regex-source":{pattern:/^(\/)[\s\S]+(?=\/[a-z]*$)/,lookbehind:true,alias:"language-regex",inside:i.languages.regex},"regex-delimiter":/^\/|\/$/,"regex-flags":/^[a-z]+$/}},"function-variable":{pattern:/#?(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*[=:]\s*(?:async\s*)?(?:\bfunction\b|(?:\((?:[^()]|\([^()]*\))*\)|(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)\s*=>))/,alias:"function"},parameter:[{pattern:/(function(?:\s+(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*)?\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\))/,lookbehind:true,inside:i.languages.javascript},{pattern:/(^|[^$\w\xA0-\uFFFF])(?!\s)[_$a-z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*=>)/i,lookbehind:true,inside:i.languages.javascript},{pattern:/(\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*=>)/,lookbehind:true,inside:i.languages.javascript},{pattern:/((?:\b|\s|^)(?!(?:as|async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|enum|export|extends|finally|for|from|function|get|if|implements|import|in|instanceof|interface|let|new|null|of|package|private|protected|public|return|set|static|super|switch|this|throw|try|typeof|undefined|var|void|while|with|yield)(?![$\w\xA0-\uFFFF]))(?:(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*\s*)\(\s*|\]\s*\(\s*)(?!\s)(?:[^()\s]|\s+(?![\s)])|\([^()]*\))+(?=\s*\)\s*\{)/,lookbehind:true,inside:i.languages.javascript}],constant:/\b[A-Z](?:[A-Z_]|\dx?)*\b/}),i.languages.insertBefore("javascript","string",{hashbang:{pattern:/^#!.*/,greedy:true,alias:"comment"},"template-string":{pattern:/`(?:\\[\s\S]|\$\{(?:[^{}]|\{(?:[^{}]|\{[^}]*\})*\})+\}|(?!\$\{)[^\\`])*`/,greedy:true,inside:{"template-punctuation":{pattern:/^`|`$/,alias:"string"},interpolation:{pattern:/((?:^|[^\\])(?:\\{2})*)\$\{(?:[^{}]|\{(?:[^{}]|\{[^}]*\})*\})+\}/,lookbehind:true,inside:{"interpolation-punctuation":{pattern:/^\$\{|\}$/,alias:"punctuation"},rest:i.languages.javascript}},string:/[\s\S]+/}},"string-property":{pattern:/((?:^|[,{])[ \t]*)(["'])(?:\\(?:\r\n|[\s\S])|(?!\2)[^\\\r\n])*\2(?=\s*:)/m,lookbehind:true,greedy:true,alias:"property"}}),i.languages.insertBefore("javascript","operator",{"literal-property":{pattern:/((?:^|[,{])[ \t]*)(?!\s)[_$a-zA-Z\xA0-\uFFFF](?:(?!\s)[$\w\xA0-\uFFFF])*(?=\s*:)/m,lookbehind:true,alias:"property"}}),i.languages.markup&&(i.languages.markup.tag.addInlined("script","javascript"),i.languages.markup.tag.addAttribute(/on(?:abort|blur|change|click|composition(?:end|start|update)|dblclick|error|focus(?:in|out)?|key(?:down|up)|load|mouse(?:down|enter|leave|move|out|over|up)|reset|resize|scroll|select|slotchange|submit|unload|wheel)/.source,"javascript")),i.languages.js=i.languages.javascript,(function(){if(typeof i>"u"||typeof document>"u")return;Element.prototype.matches||(Element.prototype.matches=Element.prototype.msMatchesSelector||Element.prototype.webkitMatchesSelector);var g="Loading…",h=function(p,c){return "✖ Error "+p+" while fetching file: "+c},y="✖ Error: File does not exist or is empty",F={js:"javascript",py:"python",rb:"ruby",ps1:"powershell",psm1:"powershell",sh:"bash",bat:"batch",h:"c",tex:"latex"},s="data-src-status",b="loading",E="loaded",T="failed",_="pre[data-src]:not(["+s+'="'+E+'"]):not(['+s+'="'+b+'"])';function S(p,c,f){var t=new XMLHttpRequest;t.open("GET",p,true),t.onreadystatechange=function(){t.readyState==4&&(t.status<400&&t.responseText?c(t.responseText):t.status>=400?f(h(t.status,t.statusText)):f(y));},t.send(null);}function j(p){var c=/^\s*(\d+)\s*(?:(,)\s*(?:(\d+)\s*)?)?$/.exec(p||"");if(c){var f=Number(c[1]),t=c[2],e=c[3];return t?e?[f,Number(e)]:[f,void 0]:[f,f]}}i.hooks.add("before-highlightall",function(p){p.selector+=", "+_;}),i.hooks.add("before-sanity-check",function(p){var c=p.element;if(c.matches(_)){p.code="",c.setAttribute(s,b);var f=c.appendChild(document.createElement("CODE"));f.textContent=g;var t=c.getAttribute("data-src"),e=p.language;if(e==="none"){var a=(/\.(\w+)$/.exec(t)||[,"none"])[1];e=F[a]||a;}i.util.setLanguage(f,e),i.util.setLanguage(c,e);var n=i.plugins.autoloader;n&&n.loadLanguages(e),S(t,function(r){c.setAttribute(s,E);var l=j(c.getAttribute("data-range"));if(l){var o=r.split(/\r\n?|\n/g),u=l[0],d=l[1]==null?o.length:l[1];u<0&&(u+=o.length),u=Math.max(0,Math.min(u-1,o.length)),d<0&&(d+=o.length),d=Math.max(0,Math.min(d,o.length)),r=o.slice(u,d).join(`
`),c.hasAttribute("data-start")||c.setAttribute("data-start",String(u+1));}f.textContent=r,i.highlightElement(f);},function(r){c.setAttribute(s,T),f.textContent=r;});}}),i.plugins.fileHighlight={highlight:function(c){for(var f=(c||document).querySelectorAll(_),t=0,e;e=f[t++];)i.highlightElement(e);}};var C=false;i.fileHighlight=function(){C||(console.warn("Prism.fileHighlight is deprecated. Use `Prism.plugins.fileHighlight.highlight` instead."),C=true),i.plugins.fileHighlight.highlight.apply(this,arguments);};})();})(O$2)),O$2.exports}var ne$2=ae$2();const se$2=sn(ne$2);var Y$2={},J$2;function re$2(){return J$2||(J$2=1,Prism.languages.python={comment:{pattern:/(^|[^\\])#.*/,lookbehind:true,greedy:true},"string-interpolation":{pattern:/(?:f|fr|rf)(?:("""|''')[\s\S]*?\1|("|')(?:\\.|(?!\2)[^\\\r\n])*\2)/i,greedy:true,inside:{interpolation:{pattern:/((?:^|[^{])(?:\{\{)*)\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}]|\{(?!\{)(?:[^{}])+\})+\})+\}/,lookbehind:true,inside:{"format-spec":{pattern:/(:)[^:(){}]+(?=\}$)/,lookbehind:true},"conversion-option":{pattern:/![sra](?=[:}]$)/,alias:"punctuation"},rest:null}},string:/[\s\S]+/}},"triple-quoted-string":{pattern:/(?:[rub]|br|rb)?("""|''')[\s\S]*?\1/i,greedy:true,alias:"string"},string:{pattern:/(?:[rub]|br|rb)?("|')(?:\\.|(?!\1)[^\\\r\n])*\1/i,greedy:true},function:{pattern:/((?:^|\s)def[ \t]+)[a-zA-Z_]\w*(?=\s*\()/g,lookbehind:true},"class-name":{pattern:/(\bclass\s+)\w+/i,lookbehind:true},decorator:{pattern:/(^[\t ]*)@\w+(?:\.\w+)*/m,lookbehind:true,alias:["annotation","punctuation"],inside:{punctuation:/\./}},keyword:/\b(?:_(?=\s*:)|and|as|assert|async|await|break|case|class|continue|def|del|elif|else|except|exec|finally|for|from|global|if|import|in|is|lambda|match|nonlocal|not|or|pass|print|raise|return|try|while|with|yield)\b/,builtin:/\b(?:__import__|abs|all|any|apply|ascii|basestring|bin|bool|buffer|bytearray|bytes|callable|chr|classmethod|cmp|coerce|compile|complex|delattr|dict|dir|divmod|enumerate|eval|execfile|file|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|intern|isinstance|issubclass|iter|len|list|locals|long|map|max|memoryview|min|next|object|oct|open|ord|pow|property|range|raw_input|reduce|reload|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|unichr|unicode|vars|xrange|zip)\b/,boolean:/\b(?:False|None|True)\b/,number:/\b0(?:b(?:_?[01])+|o(?:_?[0-7])+|x(?:_?[a-f0-9])+)\b|(?:\b\d+(?:_\d+)*(?:\.(?:\d+(?:_\d+)*)?)?|\B\.\d+(?:_\d+)*)(?:e[+-]?\d+(?:_\d+)*)?j?(?!\w)/i,operator:/[-+%=]=?|!=|:=|\*\*?=?|\/\/?=?|<[<=>]?|>[=>]?|[&|^~]/,punctuation:/[{}[\];(),.:]/},Prism.languages.python["string-interpolation"].inside.interpolation.inside.rest=Prism.languages.python,Prism.languages.py=Prism.languages.python),Y$2}re$2();

function M$2(){return {async:false,breaks:false,extensions:null,gfm:true,hooks:null,pedantic:false,renderer:null,silent:false,tokenizer:null,walkTokens:null}}let w$2=M$2();function fe$1(i){w$2=i;}const Ee=/[&<>"']/,Ne=new RegExp(Ee.source,"g"),Fe$1=/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,Oe$1=new RegExp(Fe$1.source,"g"),Le$1={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"},W$1=i=>Le$1[i];function E$2(i,t){if(t){if(Ee.test(i))return i.replace(Ne,W$1)}else if(Fe$1.test(i))return i.replace(Oe$1,W$1);return i}const $e=/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/ig;function ve$1(i){return i.replace($e,(t,e)=>(e=e.toLowerCase(),e==="colon"?":":e.charAt(0)==="#"?e.charAt(1)==="x"?String.fromCharCode(parseInt(e.substring(2),16)):String.fromCharCode(+e.substring(1)):""))}const ze=/(^|[^\[])\^/g;function g$3(i,t){let e=typeof i=="string"?i:i.source;t=t||"";const n={replace:(u,s)=>{let r=typeof s=="string"?s:s.source;return r=r.replace(ze,"$1"),e=e.replace(u,r),n},getRegex:()=>new RegExp(e,t)};return n}function Q(i){try{i=encodeURI(i).replace(/%25/g,"%");}catch{return null}return i}const S$2={exec:()=>null};function J$1(i,t){const e=i.replace(/\|/g,(s,r,a)=>{let o=false,l=r;for(;--l>=0&&a[l]==="\\";)o=!o;return o?"|":" |"}),n=e.split(/ \|/);let u=0;if(n[0].trim()||n.shift(),n.length>0&&!n[n.length-1].trim()&&n.pop(),t)if(n.length>t)n.splice(t);else for(;n.length<t;)n.push("");for(;u<n.length;u++)n[u]=n[u].trim().replace(/\\\|/g,"|");return n}function _$2(i,t,e){const n=i.length;if(n===0)return "";let u=0;for(;u<n&&i.charAt(n-u-1)===t;)u++;return i.slice(0,n-u)}function Pe$1(i,t){if(i.indexOf(t[1])===-1)return  -1;let e=0;for(let n=0;n<i.length;n++)if(i[n]==="\\")n++;else if(i[n]===t[0])e++;else if(i[n]===t[1]&&(e--,e<0))return n;return  -1}function ee$1(i,t,e,n){const u=t.href,s=t.title?E$2(t.title):null,r=i[1].replace(/\\([\[\]])/g,"$1");if(i[0].charAt(0)!=="!"){n.state.inLink=true;const a={type:"link",raw:e,href:u,title:s,text:r,tokens:n.inlineTokens(r)};return n.state.inLink=false,a}return {type:"image",raw:e,href:u,title:s,text:E$2(r)}}function Ue$1(i,t){const e=i.match(/^(\s+)(?:```)/);if(e===null)return t;const n=e[1];return t.split(`
`).map(u=>{const s=u.match(/^\s+/);if(s===null)return u;const[r]=s;return r.length>=n.length?u.slice(n.length):u}).join(`
`)}class N{options;rules;lexer;constructor(t){this.options=t||w$2;}space(t){const e=this.rules.block.newline.exec(t);if(e&&e[0].length>0)return {type:"space",raw:e[0]}}code(t){const e=this.rules.block.code.exec(t);if(e){const n=e[0].replace(/^ {1,4}/gm,"");return {type:"code",raw:e[0],codeBlockStyle:"indented",text:this.options.pedantic?n:_$2(n,`
`)}}}fences(t){const e=this.rules.block.fences.exec(t);if(e){const n=e[0],u=Ue$1(n,e[3]||"");return {type:"code",raw:n,lang:e[2]?e[2].trim().replace(this.rules.inline.anyPunctuation,"$1"):e[2],text:u}}}heading(t){const e=this.rules.block.heading.exec(t);if(e){let n=e[2].trim();if(/#$/.test(n)){const u=_$2(n,"#");(this.options.pedantic||!u||/ $/.test(u))&&(n=u.trim());}return {type:"heading",raw:e[0],depth:e[1].length,text:n,tokens:this.lexer.inline(n)}}}hr(t){const e=this.rules.block.hr.exec(t);if(e)return {type:"hr",raw:e[0]}}blockquote(t){const e=this.rules.block.blockquote.exec(t);if(e){let n=e[0].replace(/\n {0,3}((?:=+|-+) *)(?=\n|$)/g,`
    $1`);n=_$2(n.replace(/^ *>[ \t]?/gm,""),`
`);const u=this.lexer.state.top;this.lexer.state.top=true;const s=this.lexer.blockTokens(n);return this.lexer.state.top=u,{type:"blockquote",raw:e[0],tokens:s,text:n}}}list(t){let e=this.rules.block.list.exec(t);if(e){let n=e[1].trim();const u=n.length>1,s={type:"list",raw:"",ordered:u,start:u?+n.slice(0,-1):"",loose:false,items:[]};n=u?`\\d{1,9}\\${n.slice(-1)}`:`\\${n}`,this.options.pedantic&&(n=u?n:"[*+-]");const r=new RegExp(`^( {0,3}${n})((?:[	 ][^\\n]*)?(?:\\n|$))`);let a="",o="",l=false;for(;t;){let c=false;if(!(e=r.exec(t))||this.rules.block.hr.test(t))break;a=e[0],t=t.substring(a.length);let D=e[2].split(`
`,1)[0].replace(/^\t+/,x=>" ".repeat(3*x.length)),p=t.split(`
`,1)[0],d=0;this.options.pedantic?(d=2,o=D.trimStart()):(d=e[2].search(/[^ ]/),d=d>4?1:d,o=D.slice(d),d+=e[1].length);let F=false;if(!D&&/^ *$/.test(p)&&(a+=p+`
`,t=t.substring(p.length+1),c=true),!c){const x=new RegExp(`^ {0,${Math.min(3,d-1)}}(?:[*+-]|\\d{1,9}[.)])((?:[ 	][^\\n]*)?(?:\\n|$))`),b=new RegExp(`^ {0,${Math.min(3,d-1)}}((?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$)`),V=new RegExp(`^ {0,${Math.min(3,d-1)}}(?:\`\`\`|~~~)`),j=new RegExp(`^ {0,${Math.min(3,d-1)}}#`);for(;t;){const v=t.split(`
`,1)[0];if(p=v,this.options.pedantic&&(p=p.replace(/^ {1,4}(?=( {4})*[^ ])/g,"  ")),V.test(p)||j.test(p)||x.test(p)||b.test(t))break;if(p.search(/[^ ]/)>=d||!p.trim())o+=`
`+p.slice(d);else {if(F||D.search(/[^ ]/)>=4||V.test(D)||j.test(D)||b.test(D))break;o+=`
`+p;}!F&&!p.trim()&&(F=true),a+=v+`
`,t=t.substring(v.length+1),D=p.slice(d);}}s.loose||(l?s.loose=true:/\n *\n *$/.test(a)&&(l=true));let f=null,m;this.options.gfm&&(f=/^\[[ xX]\] /.exec(o),f&&(m=f[0]!=="[ ] ",o=o.replace(/^\[[ xX]\] +/,""))),s.items.push({type:"list_item",raw:a,task:!!f,checked:m,loose:false,text:o,tokens:[]}),s.raw+=a;}s.items[s.items.length-1].raw=a.trimEnd(),s.items[s.items.length-1].text=o.trimEnd(),s.raw=s.raw.trimEnd();for(let c=0;c<s.items.length;c++)if(this.lexer.state.top=false,s.items[c].tokens=this.lexer.blockTokens(s.items[c].text,[]),!s.loose){const D=s.items[c].tokens.filter(d=>d.type==="space"),p=D.length>0&&D.some(d=>/\n.*\n/.test(d.raw));s.loose=p;}if(s.loose)for(let c=0;c<s.items.length;c++)s.items[c].loose=true;return s}}html(t){const e=this.rules.block.html.exec(t);if(e)return {type:"html",block:true,raw:e[0],pre:e[1]==="pre"||e[1]==="script"||e[1]==="style",text:e[0]}}def(t){const e=this.rules.block.def.exec(t);if(e){const n=e[1].toLowerCase().replace(/\s+/g," "),u=e[2]?e[2].replace(/^<(.*)>$/,"$1").replace(this.rules.inline.anyPunctuation,"$1"):"",s=e[3]?e[3].substring(1,e[3].length-1).replace(this.rules.inline.anyPunctuation,"$1"):e[3];return {type:"def",tag:n,raw:e[0],href:u,title:s}}}table(t){const e=this.rules.block.table.exec(t);if(!e||!/[:|]/.test(e[2]))return;const n=J$1(e[1]),u=e[2].replace(/^\||\| *$/g,"").split("|"),s=e[3]&&e[3].trim()?e[3].replace(/\n[ \t]*$/,"").split(`
`):[],r={type:"table",raw:e[0],header:[],align:[],rows:[]};if(n.length===u.length){for(const a of u)/^ *-+: *$/.test(a)?r.align.push("right"):/^ *:-+: *$/.test(a)?r.align.push("center"):/^ *:-+ *$/.test(a)?r.align.push("left"):r.align.push(null);for(const a of n)r.header.push({text:a,tokens:this.lexer.inline(a)});for(const a of s)r.rows.push(J$1(a,r.header.length).map(o=>({text:o,tokens:this.lexer.inline(o)})));return r}}lheading(t){const e=this.rules.block.lheading.exec(t);if(e)return {type:"heading",raw:e[0],depth:e[2].charAt(0)==="="?1:2,text:e[1],tokens:this.lexer.inline(e[1])}}paragraph(t){const e=this.rules.block.paragraph.exec(t);if(e){const n=e[1].charAt(e[1].length-1)===`
`?e[1].slice(0,-1):e[1];return {type:"paragraph",raw:e[0],text:n,tokens:this.lexer.inline(n)}}}text(t){const e=this.rules.block.text.exec(t);if(e)return {type:"text",raw:e[0],text:e[0],tokens:this.lexer.inline(e[0])}}escape(t){const e=this.rules.inline.escape.exec(t);if(e)return {type:"escape",raw:e[0],text:E$2(e[1])}}tag(t){const e=this.rules.inline.tag.exec(t);if(e)return !this.lexer.state.inLink&&/^<a /i.test(e[0])?this.lexer.state.inLink=true:this.lexer.state.inLink&&/^<\/a>/i.test(e[0])&&(this.lexer.state.inLink=false),!this.lexer.state.inRawBlock&&/^<(pre|code|kbd|script)(\s|>)/i.test(e[0])?this.lexer.state.inRawBlock=true:this.lexer.state.inRawBlock&&/^<\/(pre|code|kbd|script)(\s|>)/i.test(e[0])&&(this.lexer.state.inRawBlock=false),{type:"html",raw:e[0],inLink:this.lexer.state.inLink,inRawBlock:this.lexer.state.inRawBlock,block:false,text:e[0]}}link(t){const e=this.rules.inline.link.exec(t);if(e){const n=e[2].trim();if(!this.options.pedantic&&/^</.test(n)){if(!/>$/.test(n))return;const r=_$2(n.slice(0,-1),"\\");if((n.length-r.length)%2===0)return}else {const r=Pe$1(e[2],"()");if(r>-1){const o=(e[0].indexOf("!")===0?5:4)+e[1].length+r;e[2]=e[2].substring(0,r),e[0]=e[0].substring(0,o).trim(),e[3]="";}}let u=e[2],s="";if(this.options.pedantic){const r=/^([^'"]*[^\s])\s+(['"])(.*)\2/.exec(u);r&&(u=r[1],s=r[3]);}else s=e[3]?e[3].slice(1,-1):"";return u=u.trim(),/^</.test(u)&&(this.options.pedantic&&!/>$/.test(n)?u=u.slice(1):u=u.slice(1,-1)),ee$1(e,{href:u&&u.replace(this.rules.inline.anyPunctuation,"$1"),title:s&&s.replace(this.rules.inline.anyPunctuation,"$1")},e[0],this.lexer)}}reflink(t,e){let n;if((n=this.rules.inline.reflink.exec(t))||(n=this.rules.inline.nolink.exec(t))){const u=(n[2]||n[1]).replace(/\s+/g," "),s=e[u.toLowerCase()];if(!s){const r=n[0].charAt(0);return {type:"text",raw:r,text:r}}return ee$1(n,s,n[0],this.lexer)}}emStrong(t,e,n=""){let u=this.rules.inline.emStrongLDelim.exec(t);if(!u||u[3]&&n.match(/[\p{L}\p{N}]/u))return;if(!(u[1]||u[2]||"")||!n||this.rules.inline.punctuation.exec(n)){const r=[...u[0]].length-1;let a,o,l=r,c=0;const D=u[0][0]==="*"?this.rules.inline.emStrongRDelimAst:this.rules.inline.emStrongRDelimUnd;for(D.lastIndex=0,e=e.slice(-1*t.length+r);(u=D.exec(e))!=null;){if(a=u[1]||u[2]||u[3]||u[4]||u[5]||u[6],!a)continue;if(o=[...a].length,u[3]||u[4]){l+=o;continue}else if((u[5]||u[6])&&r%3&&!((r+o)%3)){c+=o;continue}if(l-=o,l>0)continue;o=Math.min(o,o+l+c);const p=[...u[0]][0].length,d=t.slice(0,r+u.index+p+o);if(Math.min(r,o)%2){const f=d.slice(1,-1);return {type:"em",raw:d,text:f,tokens:this.lexer.inlineTokens(f)}}const F=d.slice(2,-2);return {type:"strong",raw:d,text:F,tokens:this.lexer.inlineTokens(F)}}}}codespan(t){const e=this.rules.inline.code.exec(t);if(e){let n=e[2].replace(/\n/g," ");const u=/[^ ]/.test(n),s=/^ /.test(n)&&/ $/.test(n);return u&&s&&(n=n.substring(1,n.length-1)),n=E$2(n,true),{type:"codespan",raw:e[0],text:n}}}br(t){const e=this.rules.inline.br.exec(t);if(e)return {type:"br",raw:e[0]}}del(t){const e=this.rules.inline.del.exec(t);if(e)return {type:"del",raw:e[0],text:e[2],tokens:this.lexer.inlineTokens(e[2])}}autolink(t){const e=this.rules.inline.autolink.exec(t);if(e){let n,u;return e[2]==="@"?(n=E$2(e[1]),u="mailto:"+n):(n=E$2(e[1]),u=n),{type:"link",raw:e[0],text:n,href:u,tokens:[{type:"text",raw:n,text:n}]}}}url(t){let e;if(e=this.rules.inline.url.exec(t)){let n,u;if(e[2]==="@")n=E$2(e[0]),u="mailto:"+n;else {let s;do s=e[0],e[0]=this.rules.inline._backpedal.exec(e[0])?.[0]??"";while(s!==e[0]);n=E$2(e[0]),e[1]==="www."?u="http://"+e[0]:u=e[0];}return {type:"link",raw:e[0],text:n,href:u,tokens:[{type:"text",raw:n,text:n}]}}}inlineText(t){const e=this.rules.inline.text.exec(t);if(e){let n;return this.lexer.state.inRawBlock?n=e[0]:n=E$2(e[0]),{type:"text",raw:e[0],text:n}}}}const Me$1=/^(?: *(?:\n|$))+/,He$1=/^( {4}[^\n]+(?:\n(?: *(?:\n|$))*)?)+/,Ge$1=/^ {0,3}(`{3,}(?=[^`\n]*(?:\n|$))|~{3,})([^\n]*)(?:\n|$)(?:|([\s\S]*?)(?:\n|$))(?: {0,3}\1[~`]* *(?=\n|$)|$)/,B$4=/^ {0,3}((?:-[\t ]*){3,}|(?:_[ \t]*){3,}|(?:\*[ \t]*){3,})(?:\n+|$)/,qe$1=/^ {0,3}(#{1,6})(?=\s|$)(.*)(?:\n+|$)/,be$1=/(?:[*+-]|\d{1,9}[.)])/,Ae=g$3(/^(?!bull |blockCode|fences|blockquote|heading|html)((?:.|\n(?!\s*?\n|bull |blockCode|fences|blockquote|heading|html))+?)\n {0,3}(=+|-+) *(?:\n+|$)/).replace(/bull/g,be$1).replace(/blockCode/g,/ {4}/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).getRegex(),H=/^([^\n]+(?:\n(?!hr|heading|lheading|blockquote|fences|list|html|table| +\n)[^\n]+)*)/,Ze$1=/^[^\n]+/,G$2=/(?!\s*\])(?:\\.|[^\[\]\\])+/,Xe=g$3(/^ {0,3}\[(label)\]: *(?:\n *)?([^<\s][^\s]*|<.*?>)(?:(?: +(?:\n *)?| *\n *)(title))? *(?:\n+|$)/).replace("label",G$2).replace("title",/(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/).getRegex(),Ye=g$3(/^( {0,3}bull)([ \t][^\n]+?)?(?:\n|$)/).replace(/bull/g,be$1).getRegex(),$$2="address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul",q$2=/<!--(?:-?>|[\s\S]*?(?:-->|$))/,Ke=g$3("^ {0,3}(?:<(script|pre|style|textarea)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?(?:\\?>\\n*|$)|<![A-Z][\\s\\S]*?(?:>\\n*|$)|<!\\[CDATA\\[[\\s\\S]*?(?:\\]\\]>\\n*|$)|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:(?:\\n *)+\\n|$)|<(?!script|pre|style|textarea)([a-z][\\w-]*)(?:attribute)*? */?>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n *)+\\n|$)|</(?!script|pre|style|textarea)[a-z][\\w-]*\\s*>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n *)+\\n|$))","i").replace("comment",q$2).replace("tag",$$2).replace("attribute",/ +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(),ke$1=g$3(H).replace("hr",B$4).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("|table","").replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",$$2).getRegex(),Ve$1=g$3(/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/).replace("paragraph",ke$1).getRegex(),Z={blockquote:Ve$1,code:He$1,def:Xe,fences:Ge$1,heading:qe$1,hr:B$4,html:Ke,lheading:Ae,list:Ye,newline:Me$1,paragraph:ke$1,table:S$2,text:Ze$1},te$1=g$3("^ *([^\\n ].*)\\n {0,3}((?:\\| *)?:?-+:? *(?:\\| *:?-+:? *)*(?:\\| *)?)(?:\\n((?:(?! *\\n|hr|heading|blockquote|code|fences|list|html).*(?:\\n|$))*)\\n*|$)").replace("hr",B$4).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("blockquote"," {0,3}>").replace("code"," {4}[^\\n]").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",$$2).getRegex(),je$1={...Z,table:te$1,paragraph:g$3(H).replace("hr",B$4).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("table",te$1).replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",$$2).getRegex()},We={...Z,html:g$3(`^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:"[^"]*"|'[^']*'|\\s[^'"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))`).replace("comment",q$2).replace(/tag/g,"(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/,heading:/^(#{1,6})(.*)(?:\n+|$)/,fences:S$2,lheading:/^(.+?)\n {0,3}(=+|-+) *(?:\n+|$)/,paragraph:g$3(H).replace("hr",B$4).replace("heading",` *#{1,6} *[^
]`).replace("lheading",Ae).replace("|table","").replace("blockquote"," {0,3}>").replace("|fences","").replace("|list","").replace("|html","").replace("|tag","").getRegex()},me$1=/^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/,Qe=/^(`+)([^`]|[^`][\s\S]*?[^`])\1(?!`)/,Ce$1=/^( {2,}|\\)\n(?!\s*$)/,Je=/^(`+|[^`])(?:(?= {2,}\n)|[\s\S]*?(?:(?=[\\<!\[`*_]|\b_|$)|[^ ](?= {2,}\n)))/,y$3="\\p{P}\\p{S}",et=g$3(/^((?![*_])[\spunctuation])/,"u").replace(/punctuation/g,y$3).getRegex(),tt$1=/\[[^[\]]*?\]\([^\(\)]*?\)|`[^`]*?`|<[^<>]*?>/g,nt=g$3(/^(?:\*+(?:((?!\*)[punct])|[^\s*]))|^_+(?:((?!_)[punct])|([^\s_]))/,"u").replace(/punct/g,y$3).getRegex(),rt=g$3("^[^_*]*?__[^_*]*?\\*[^_*]*?(?=__)|[^*]+(?=[^*])|(?!\\*)[punct](\\*+)(?=[\\s]|$)|[^punct\\s](\\*+)(?!\\*)(?=[punct\\s]|$)|(?!\\*)[punct\\s](\\*+)(?=[^punct\\s])|[\\s](\\*+)(?!\\*)(?=[punct])|(?!\\*)[punct](\\*+)(?!\\*)(?=[punct])|[^punct\\s](\\*+)(?=[^punct\\s])","gu").replace(/punct/g,y$3).getRegex(),ut=g$3("^[^_*]*?\\*\\*[^_*]*?_[^_*]*?(?=\\*\\*)|[^_]+(?=[^_])|(?!_)[punct](_+)(?=[\\s]|$)|[^punct\\s](_+)(?!_)(?=[punct\\s]|$)|(?!_)[punct\\s](_+)(?=[^punct\\s])|[\\s](_+)(?!_)(?=[punct])|(?!_)[punct](_+)(?!_)(?=[punct])","gu").replace(/punct/g,y$3).getRegex(),st$1=g$3(/\\([punct])/,"gu").replace(/punct/g,y$3).getRegex(),it=g$3(/^<(scheme:[^\s\x00-\x1f<>]*|email)>/).replace("scheme",/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/).replace("email",/[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/).getRegex(),at=g$3(q$2).replace("(?:-->|$)","-->").getRegex(),ot=g$3("^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>").replace("comment",at).replace("attribute",/\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/).getRegex(),O$1=/(?:\[(?:\\.|[^\[\]\\])*\]|\\.|`[^`]*`|[^\[\]\\`])*?/,lt=g$3(/^!?\[(label)\]\(\s*(href)(?:\s+(title))?\s*\)/).replace("label",O$1).replace("href",/<(?:\\.|[^\n<>\\])+>|[^\s\x00-\x1f]*/).replace("title",/"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/).getRegex(),we=g$3(/^!?\[(label)\]\[(ref)\]/).replace("label",O$1).replace("ref",G$2).getRegex(),xe$1=g$3(/^!?\[(ref)\](?:\[\])?/).replace("ref",G$2).getRegex(),ct=g$3("reflink|nolink(?!\\()","g").replace("reflink",we).replace("nolink",xe$1).getRegex(),X={_backpedal:S$2,anyPunctuation:st$1,autolink:it,blockSkip:tt$1,br:Ce$1,code:Qe,del:S$2,emStrongLDelim:nt,emStrongRDelimAst:rt,emStrongRDelimUnd:ut,escape:me$1,link:lt,nolink:xe$1,punctuation:et,reflink:we,reflinkSearch:ct,tag:ot,text:Je,url:S$2},pt$1={...X,link:g$3(/^!?\[(label)\]\((.*?)\)/).replace("label",O$1).getRegex(),reflink:g$3(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label",O$1).getRegex()},U$3={...X,escape:g$3(me$1).replace("])","~|])").getRegex(),url:g$3(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/,"i").replace("email",/[A-Za-z0-9._+-]+(@)[a-zA-Z0-9-_]+(?:\.[a-zA-Z0-9-_]*[a-zA-Z0-9])+(?![-_])/).getRegex(),_backpedal:/(?:[^?!.,:;*_'"~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_'"~)]+(?!$))+/,del:/^(~~?)(?=[^\s~])([\s\S]*?[^\s~])\1(?=[^~]|$)/,text:/^([`~]+|[^`~])(?:(?= {2,}\n)|(?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)|[\s\S]*?(?:(?=[\\<!\[`*~_]|\b_|https?:\/\/|ftp:\/\/|www\.|$)|[^ ](?= {2,}\n)|[^a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-](?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)))/},Dt$1={...U$3,br:g$3(Ce$1).replace("{2,}","*").getRegex(),text:g$3(U$3.text).replace("\\b_","\\b_| {2,}\\n").replace(/\{2,\}/g,"*").getRegex()},R$1={normal:Z,gfm:je$1,pedantic:We},T$1={normal:X,gfm:U$3,breaks:Dt$1,pedantic:pt$1};class A{tokens;options;state;tokenizer;inlineQueue;constructor(t){this.tokens=[],this.tokens.links=Object.create(null),this.options=t||w$2,this.options.tokenizer=this.options.tokenizer||new N,this.tokenizer=this.options.tokenizer,this.tokenizer.options=this.options,this.tokenizer.lexer=this,this.inlineQueue=[],this.state={inLink:false,inRawBlock:false,top:true};const e={block:R$1.normal,inline:T$1.normal};this.options.pedantic?(e.block=R$1.pedantic,e.inline=T$1.pedantic):this.options.gfm&&(e.block=R$1.gfm,this.options.breaks?e.inline=T$1.breaks:e.inline=T$1.gfm),this.tokenizer.rules=e;}static get rules(){return {block:R$1,inline:T$1}}static lex(t,e){return new A(e).lex(t)}static lexInline(t,e){return new A(e).inlineTokens(t)}lex(t){t=t.replace(/\r\n|\r/g,`
`),this.blockTokens(t,this.tokens);for(let e=0;e<this.inlineQueue.length;e++){const n=this.inlineQueue[e];this.inlineTokens(n.src,n.tokens);}return this.inlineQueue=[],this.tokens}blockTokens(t,e=[]){this.options.pedantic?t=t.replace(/\t/g,"    ").replace(/^ +$/gm,""):t=t.replace(/^( *)(\t+)/gm,(a,o,l)=>o+"    ".repeat(l.length));let n,u,s,r;for(;t;)if(!(this.options.extensions&&this.options.extensions.block&&this.options.extensions.block.some(a=>(n=a.call({lexer:this},t,e))?(t=t.substring(n.raw.length),e.push(n),true):false))){if(n=this.tokenizer.space(t)){t=t.substring(n.raw.length),n.raw.length===1&&e.length>0?e[e.length-1].raw+=`
`:e.push(n);continue}if(n=this.tokenizer.code(t)){t=t.substring(n.raw.length),u=e[e.length-1],u&&(u.type==="paragraph"||u.type==="text")?(u.raw+=`
`+n.raw,u.text+=`
`+n.text,this.inlineQueue[this.inlineQueue.length-1].src=u.text):e.push(n);continue}if(n=this.tokenizer.fences(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.heading(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.hr(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.blockquote(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.list(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.html(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.def(t)){t=t.substring(n.raw.length),u=e[e.length-1],u&&(u.type==="paragraph"||u.type==="text")?(u.raw+=`
`+n.raw,u.text+=`
`+n.raw,this.inlineQueue[this.inlineQueue.length-1].src=u.text):this.tokens.links[n.tag]||(this.tokens.links[n.tag]={href:n.href,title:n.title});continue}if(n=this.tokenizer.table(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.lheading(t)){t=t.substring(n.raw.length),e.push(n);continue}if(s=t,this.options.extensions&&this.options.extensions.startBlock){let a=1/0;const o=t.slice(1);let l;this.options.extensions.startBlock.forEach(c=>{l=c.call({lexer:this},o),typeof l=="number"&&l>=0&&(a=Math.min(a,l));}),a<1/0&&a>=0&&(s=t.substring(0,a+1));}if(this.state.top&&(n=this.tokenizer.paragraph(s))){u=e[e.length-1],r&&u.type==="paragraph"?(u.raw+=`
`+n.raw,u.text+=`
`+n.text,this.inlineQueue.pop(),this.inlineQueue[this.inlineQueue.length-1].src=u.text):e.push(n),r=s.length!==t.length,t=t.substring(n.raw.length);continue}if(n=this.tokenizer.text(t)){t=t.substring(n.raw.length),u=e[e.length-1],u&&u.type==="text"?(u.raw+=`
`+n.raw,u.text+=`
`+n.text,this.inlineQueue.pop(),this.inlineQueue[this.inlineQueue.length-1].src=u.text):e.push(n);continue}if(t){const a="Infinite loop on byte: "+t.charCodeAt(0);if(this.options.silent){console.error(a);break}else throw new Error(a)}}return this.state.top=true,e}inline(t,e=[]){return this.inlineQueue.push({src:t,tokens:e}),e}inlineTokens(t,e=[]){let n,u,s,r=t,a,o,l;if(this.tokens.links){const c=Object.keys(this.tokens.links);if(c.length>0)for(;(a=this.tokenizer.rules.inline.reflinkSearch.exec(r))!=null;)c.includes(a[0].slice(a[0].lastIndexOf("[")+1,-1))&&(r=r.slice(0,a.index)+"["+"a".repeat(a[0].length-2)+"]"+r.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex));}for(;(a=this.tokenizer.rules.inline.blockSkip.exec(r))!=null;)r=r.slice(0,a.index)+"["+"a".repeat(a[0].length-2)+"]"+r.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);for(;(a=this.tokenizer.rules.inline.anyPunctuation.exec(r))!=null;)r=r.slice(0,a.index)+"++"+r.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);for(;t;)if(o||(l=""),o=false,!(this.options.extensions&&this.options.extensions.inline&&this.options.extensions.inline.some(c=>(n=c.call({lexer:this},t,e))?(t=t.substring(n.raw.length),e.push(n),true):false))){if(n=this.tokenizer.escape(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.tag(t)){t=t.substring(n.raw.length),u=e[e.length-1],u&&n.type==="text"&&u.type==="text"?(u.raw+=n.raw,u.text+=n.text):e.push(n);continue}if(n=this.tokenizer.link(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.reflink(t,this.tokens.links)){t=t.substring(n.raw.length),u=e[e.length-1],u&&n.type==="text"&&u.type==="text"?(u.raw+=n.raw,u.text+=n.text):e.push(n);continue}if(n=this.tokenizer.emStrong(t,r,l)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.codespan(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.br(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.del(t)){t=t.substring(n.raw.length),e.push(n);continue}if(n=this.tokenizer.autolink(t)){t=t.substring(n.raw.length),e.push(n);continue}if(!this.state.inLink&&(n=this.tokenizer.url(t))){t=t.substring(n.raw.length),e.push(n);continue}if(s=t,this.options.extensions&&this.options.extensions.startInline){let c=1/0;const D=t.slice(1);let p;this.options.extensions.startInline.forEach(d=>{p=d.call({lexer:this},D),typeof p=="number"&&p>=0&&(c=Math.min(c,p));}),c<1/0&&c>=0&&(s=t.substring(0,c+1));}if(n=this.tokenizer.inlineText(s)){t=t.substring(n.raw.length),n.raw.slice(-1)!=="_"&&(l=n.raw.slice(-1)),o=true,u=e[e.length-1],u&&u.type==="text"?(u.raw+=n.raw,u.text+=n.text):e.push(n);continue}if(t){const c="Infinite loop on byte: "+t.charCodeAt(0);if(this.options.silent){console.error(c);break}else throw new Error(c)}}return e}}let L$2 = class L{options;constructor(t){this.options=t||w$2;}code(t,e,n){const u=(e||"").match(/^\S*/)?.[0];return t=t.replace(/\n$/,"")+`
`,u?'<pre><code class="language-'+E$2(u)+'">'+(n?t:E$2(t,true))+`</code></pre>
`:"<pre><code>"+(n?t:E$2(t,true))+`</code></pre>
`}blockquote(t){return `<blockquote>
${t}</blockquote>
`}html(t,e){return t}heading(t,e,n){return `<h${e}>${t}</h${e}>
`}hr(){return `<hr>
`}list(t,e,n){const u=e?"ol":"ul",s=e&&n!==1?' start="'+n+'"':"";return "<"+u+s+`>
`+t+"</"+u+`>
`}listitem(t,e,n){return `<li>${t}</li>
`}checkbox(t){return "<input "+(t?'checked="" ':"")+'disabled="" type="checkbox">'}paragraph(t){return `<p>${t}</p>
`}table(t,e){return e&&(e=`<tbody>${e}</tbody>`),`<table>
<thead>
`+t+`</thead>
`+e+`</table>
`}tablerow(t){return `<tr>
${t}</tr>
`}tablecell(t,e){const n=e.header?"th":"td";return (e.align?`<${n} align="${e.align}">`:`<${n}>`)+t+`</${n}>
`}strong(t){return `<strong>${t}</strong>`}em(t){return `<em>${t}</em>`}codespan(t){return `<code>${t}</code>`}br(){return "<br>"}del(t){return `<del>${t}</del>`}link(t,e,n){const u=Q(t);if(u===null)return n;t=u;let s='<a href="'+t+'"';return e&&(s+=' title="'+e+'"'),s+=">"+n+"</a>",s}image(t,e,n){const u=Q(t);if(u===null)return n;t=u;let s=`<img src="${t}" alt="${n}"`;return e&&(s+=` title="${e}"`),s+=">",s}text(t){return t}};let Y$1 = class Y{strong(t){return t}em(t){return t}codespan(t){return t}del(t){return t}html(t){return t}text(t){return t}link(t,e,n){return ""+n}image(t,e,n){return ""+n}br(){return ""}};let k$2 = class k{options;renderer;textRenderer;constructor(t){this.options=t||w$2,this.options.renderer=this.options.renderer||new L$2,this.renderer=this.options.renderer,this.renderer.options=this.options,this.textRenderer=new Y$1;}static parse(t,e){return new k(e).parse(t)}static parseInline(t,e){return new k(e).parseInline(t)}parse(t,e=true){let n="";for(let u=0;u<t.length;u++){const s=t[u];if(this.options.extensions&&this.options.extensions.renderers&&this.options.extensions.renderers[s.type]){const r=s,a=this.options.extensions.renderers[r.type].call({parser:this},r);if(a!==false||!["space","hr","heading","code","table","blockquote","list","html","paragraph","text"].includes(r.type)){n+=a||"";continue}}switch(s.type){case "space":continue;case "hr":{n+=this.renderer.hr();continue}case "heading":{const r=s;n+=this.renderer.heading(this.parseInline(r.tokens),r.depth,ve$1(this.parseInline(r.tokens,this.textRenderer)));continue}case "code":{const r=s;n+=this.renderer.code(r.text,r.lang,!!r.escaped);continue}case "table":{const r=s;let a="",o="";for(let c=0;c<r.header.length;c++)o+=this.renderer.tablecell(this.parseInline(r.header[c].tokens),{header:true,align:r.align[c]});a+=this.renderer.tablerow(o);let l="";for(let c=0;c<r.rows.length;c++){const D=r.rows[c];o="";for(let p=0;p<D.length;p++)o+=this.renderer.tablecell(this.parseInline(D[p].tokens),{header:false,align:r.align[p]});l+=this.renderer.tablerow(o);}n+=this.renderer.table(a,l);continue}case "blockquote":{const r=s,a=this.parse(r.tokens);n+=this.renderer.blockquote(a);continue}case "list":{const r=s,a=r.ordered,o=r.start,l=r.loose;let c="";for(let D=0;D<r.items.length;D++){const p=r.items[D],d=p.checked,F=p.task;let f="";if(p.task){const m=this.renderer.checkbox(!!d);l?p.tokens.length>0&&p.tokens[0].type==="paragraph"?(p.tokens[0].text=m+" "+p.tokens[0].text,p.tokens[0].tokens&&p.tokens[0].tokens.length>0&&p.tokens[0].tokens[0].type==="text"&&(p.tokens[0].tokens[0].text=m+" "+p.tokens[0].tokens[0].text)):p.tokens.unshift({type:"text",text:m+" "}):f+=m+" ";}f+=this.parse(p.tokens,l),c+=this.renderer.listitem(f,F,!!d);}n+=this.renderer.list(c,a,o);continue}case "html":{const r=s;n+=this.renderer.html(r.text,r.block);continue}case "paragraph":{const r=s;n+=this.renderer.paragraph(this.parseInline(r.tokens));continue}case "text":{let r=s,a=r.tokens?this.parseInline(r.tokens):r.text;for(;u+1<t.length&&t[u+1].type==="text";)r=t[++u],a+=`
`+(r.tokens?this.parseInline(r.tokens):r.text);n+=e?this.renderer.paragraph(a):a;continue}default:{const r='Token with "'+s.type+'" type was not found.';if(this.options.silent)return console.error(r),"";throw new Error(r)}}}return n}parseInline(t,e){e=e||this.renderer;let n="";for(let u=0;u<t.length;u++){const s=t[u];if(this.options.extensions&&this.options.extensions.renderers&&this.options.extensions.renderers[s.type]){const r=this.options.extensions.renderers[s.type].call({parser:this},s);if(r!==false||!["escape","html","link","image","strong","em","codespan","br","del","text"].includes(s.type)){n+=r||"";continue}}switch(s.type){case "escape":{const r=s;n+=e.text(r.text);break}case "html":{const r=s;n+=e.html(r.text);break}case "link":{const r=s;n+=e.link(r.href,r.title,this.parseInline(r.tokens,e));break}case "image":{const r=s;n+=e.image(r.href,r.title,r.text);break}case "strong":{const r=s;n+=e.strong(this.parseInline(r.tokens,e));break}case "em":{const r=s;n+=e.em(this.parseInline(r.tokens,e));break}case "codespan":{const r=s;n+=e.codespan(r.text);break}case "br":{n+=e.br();break}case "del":{const r=s;n+=e.del(this.parseInline(r.tokens,e));break}case "text":{const r=s;n+=e.text(r.text);break}default:{const r='Token with "'+s.type+'" type was not found.';if(this.options.silent)return console.error(r),"";throw new Error(r)}}}return n}};class I{options;constructor(t){this.options=t||w$2;}static passThroughHooks=new Set(["preprocess","postprocess","processAllTokens"]);preprocess(t){return t}postprocess(t){return t}processAllTokens(t){return t}}class Te{defaults=M$2();options=this.setOptions;parse=this.#e(A.lex,k$2.parse);parseInline=this.#e(A.lexInline,k$2.parseInline);Parser=k$2;Renderer=L$2;TextRenderer=Y$1;Lexer=A;Tokenizer=N;Hooks=I;constructor(...t){this.use(...t);}walkTokens(t,e){let n=[];for(const u of t)switch(n=n.concat(e.call(this,u)),u.type){case "table":{const s=u;for(const r of s.header)n=n.concat(this.walkTokens(r.tokens,e));for(const r of s.rows)for(const a of r)n=n.concat(this.walkTokens(a.tokens,e));break}case "list":{const s=u;n=n.concat(this.walkTokens(s.items,e));break}default:{const s=u;this.defaults.extensions?.childTokens?.[s.type]?this.defaults.extensions.childTokens[s.type].forEach(r=>{const a=s[r].flat(1/0);n=n.concat(this.walkTokens(a,e));}):s.tokens&&(n=n.concat(this.walkTokens(s.tokens,e)));}}return n}use(...t){const e=this.defaults.extensions||{renderers:{},childTokens:{}};return t.forEach(n=>{const u={...n};if(u.async=this.defaults.async||u.async||false,n.extensions&&(n.extensions.forEach(s=>{if(!s.name)throw new Error("extension name required");if("renderer"in s){const r=e.renderers[s.name];r?e.renderers[s.name]=function(...a){let o=s.renderer.apply(this,a);return o===false&&(o=r.apply(this,a)),o}:e.renderers[s.name]=s.renderer;}if("tokenizer"in s){if(!s.level||s.level!=="block"&&s.level!=="inline")throw new Error("extension level must be 'block' or 'inline'");const r=e[s.level];r?r.unshift(s.tokenizer):e[s.level]=[s.tokenizer],s.start&&(s.level==="block"?e.startBlock?e.startBlock.push(s.start):e.startBlock=[s.start]:s.level==="inline"&&(e.startInline?e.startInline.push(s.start):e.startInline=[s.start]));}"childTokens"in s&&s.childTokens&&(e.childTokens[s.name]=s.childTokens);}),u.extensions=e),n.renderer){const s=this.defaults.renderer||new L$2(this.defaults);for(const r in n.renderer){if(!(r in s))throw new Error(`renderer '${r}' does not exist`);if(r==="options")continue;const a=r,o=n.renderer[a],l=s[a];s[a]=(...c)=>{let D=o.apply(s,c);return D===false&&(D=l.apply(s,c)),D||""};}u.renderer=s;}if(n.tokenizer){const s=this.defaults.tokenizer||new N(this.defaults);for(const r in n.tokenizer){if(!(r in s))throw new Error(`tokenizer '${r}' does not exist`);if(["options","rules","lexer"].includes(r))continue;const a=r,o=n.tokenizer[a],l=s[a];s[a]=(...c)=>{let D=o.apply(s,c);return D===false&&(D=l.apply(s,c)),D};}u.tokenizer=s;}if(n.hooks){const s=this.defaults.hooks||new I;for(const r in n.hooks){if(!(r in s))throw new Error(`hook '${r}' does not exist`);if(r==="options")continue;const a=r,o=n.hooks[a],l=s[a];I.passThroughHooks.has(r)?s[a]=c=>{if(this.defaults.async)return Promise.resolve(o.call(s,c)).then(p=>l.call(s,p));const D=o.call(s,c);return l.call(s,D)}:s[a]=(...c)=>{let D=o.apply(s,c);return D===false&&(D=l.apply(s,c)),D};}u.hooks=s;}if(n.walkTokens){const s=this.defaults.walkTokens,r=n.walkTokens;u.walkTokens=function(a){let o=[];return o.push(r.call(this,a)),s&&(o=o.concat(s.call(this,a))),o};}this.defaults={...this.defaults,...u};}),this}setOptions(t){return this.defaults={...this.defaults,...t},this}lexer(t,e){return A.lex(t,e??this.defaults)}parser(t,e){return k$2.parse(t,e??this.defaults)}#e(t,e){return (n,u)=>{const s={...u},r={...this.defaults,...s};this.defaults.async===true&&s.async===false&&(r.silent||console.warn("marked(): The async option was set to true by an extension. The async: false option sent to parse will be ignored."),r.async=true);const a=this.#t(!!r.silent,!!r.async);if(typeof n>"u"||n===null)return a(new Error("marked(): input parameter is undefined or null"));if(typeof n!="string")return a(new Error("marked(): input parameter is of type "+Object.prototype.toString.call(n)+", string expected"));if(r.hooks&&(r.hooks.options=r),r.async)return Promise.resolve(r.hooks?r.hooks.preprocess(n):n).then(o=>t(o,r)).then(o=>r.hooks?r.hooks.processAllTokens(o):o).then(o=>r.walkTokens?Promise.all(this.walkTokens(o,r.walkTokens)).then(()=>o):o).then(o=>e(o,r)).then(o=>r.hooks?r.hooks.postprocess(o):o).catch(a);try{r.hooks&&(n=r.hooks.preprocess(n));let o=t(n,r);r.hooks&&(o=r.hooks.processAllTokens(o)),r.walkTokens&&this.walkTokens(o,r.walkTokens);let l=e(o,r);return r.hooks&&(l=r.hooks.postprocess(l)),l}catch(o){return a(o)}}}#t(t,e){return n=>{if(n.message+=`
Please report this to https://github.com/markedjs/marked.`,t){const u="<p>An error occurred:</p><pre>"+E$2(n.message+"",true)+"</pre>";return e?Promise.resolve(u):u}if(e)return Promise.reject(n);throw n}}}const C$1=new Te;function h$2(i,t){return C$1.parse(i,t)}h$2.options=h$2.setOptions=function(i){return C$1.setOptions(i),h$2.defaults=C$1.defaults,fe$1(h$2.defaults),h$2};h$2.getDefaults=M$2;h$2.defaults=w$2;h$2.use=function(...i){return C$1.use(...i),h$2.defaults=C$1.defaults,fe$1(h$2.defaults),h$2};h$2.walkTokens=function(i,t){return C$1.walkTokens(i,t)};h$2.parseInline=C$1.parseInline;h$2.Parser=k$2;h$2.parser=k$2.parse;h$2.Renderer=L$2;h$2.TextRenderer=Y$1;h$2.Lexer=A;h$2.lexer=A.lex;h$2.Tokenizer=N;h$2.Hooks=I;h$2.parse=h$2;h$2.options;h$2.setOptions;h$2.use;h$2.walkTokens;h$2.parseInline;k$2.parse;A.lex;function dt(i){if(typeof i=="function"&&(i={highlight:i}),!i||typeof i.highlight!="function")throw new Error("Must provide highlight function");return typeof i.langPrefix!="string"&&(i.langPrefix="language-"),typeof i.emptyLangClass!="string"&&(i.emptyLangClass=""),{async:!!i.async,walkTokens(t){if(t.type!=="code")return;const e=ne$1(t.lang);if(i.async)return Promise.resolve(i.highlight(t.text,e,t.lang||"")).then(re$1(t));const n=i.highlight(t.text,e,t.lang||"");if(n instanceof Promise)throw new Error("markedHighlight is not set to async but the highlight function is async. Set the async option to true on markedHighlight to await the async highlight function.");re$1(t)(n);},useNewRenderer:true,renderer:{code(t,e,n){typeof t=="object"&&(n=t.escaped,e=t.lang,t=t.text);const u=ne$1(e),s=u?i.langPrefix+se$1(u):i.emptyLangClass,r=s?` class="${s}"`:"";return t=t.replace(/\n$/,""),`<pre><code${r}>${n?t:se$1(t,true)}
</code></pre>`}}}}function ne$1(i){return (i||"").match(/\S*/)[0]}function re$1(i){return t=>{typeof t=="string"&&t!==i.text&&(i.escaped=true,i.text=t);}}const Se=/[&<>"']/,ht=new RegExp(Se.source,"g"),Be$1=/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,gt=new RegExp(Be$1.source,"g"),ft={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"},ue$1=i=>ft[i];function se$1(i,t){if(t){if(Se.test(i))return i.replace(ht,ue$1)}else if(Be$1.test(i))return i.replace(gt,ue$1);return i}const Et=/[\0-\x1F!-,\.\/:-@\[-\^`\{-\xA9\xAB-\xB4\xB6-\xB9\xBB-\xBF\xD7\xF7\u02C2-\u02C5\u02D2-\u02DF\u02E5-\u02EB\u02ED\u02EF-\u02FF\u0375\u0378\u0379\u037E\u0380-\u0385\u0387\u038B\u038D\u03A2\u03F6\u0482\u0530\u0557\u0558\u055A-\u055F\u0589-\u0590\u05BE\u05C0\u05C3\u05C6\u05C8-\u05CF\u05EB-\u05EE\u05F3-\u060F\u061B-\u061F\u066A-\u066D\u06D4\u06DD\u06DE\u06E9\u06FD\u06FE\u0700-\u070F\u074B\u074C\u07B2-\u07BF\u07F6-\u07F9\u07FB\u07FC\u07FE\u07FF\u082E-\u083F\u085C-\u085F\u086B-\u089F\u08B5\u08C8-\u08D2\u08E2\u0964\u0965\u0970\u0984\u098D\u098E\u0991\u0992\u09A9\u09B1\u09B3-\u09B5\u09BA\u09BB\u09C5\u09C6\u09C9\u09CA\u09CF-\u09D6\u09D8-\u09DB\u09DE\u09E4\u09E5\u09F2-\u09FB\u09FD\u09FF\u0A00\u0A04\u0A0B-\u0A0E\u0A11\u0A12\u0A29\u0A31\u0A34\u0A37\u0A3A\u0A3B\u0A3D\u0A43-\u0A46\u0A49\u0A4A\u0A4E-\u0A50\u0A52-\u0A58\u0A5D\u0A5F-\u0A65\u0A76-\u0A80\u0A84\u0A8E\u0A92\u0AA9\u0AB1\u0AB4\u0ABA\u0ABB\u0AC6\u0ACA\u0ACE\u0ACF\u0AD1-\u0ADF\u0AE4\u0AE5\u0AF0-\u0AF8\u0B00\u0B04\u0B0D\u0B0E\u0B11\u0B12\u0B29\u0B31\u0B34\u0B3A\u0B3B\u0B45\u0B46\u0B49\u0B4A\u0B4E-\u0B54\u0B58-\u0B5B\u0B5E\u0B64\u0B65\u0B70\u0B72-\u0B81\u0B84\u0B8B-\u0B8D\u0B91\u0B96-\u0B98\u0B9B\u0B9D\u0BA0-\u0BA2\u0BA5-\u0BA7\u0BAB-\u0BAD\u0BBA-\u0BBD\u0BC3-\u0BC5\u0BC9\u0BCE\u0BCF\u0BD1-\u0BD6\u0BD8-\u0BE5\u0BF0-\u0BFF\u0C0D\u0C11\u0C29\u0C3A-\u0C3C\u0C45\u0C49\u0C4E-\u0C54\u0C57\u0C5B-\u0C5F\u0C64\u0C65\u0C70-\u0C7F\u0C84\u0C8D\u0C91\u0CA9\u0CB4\u0CBA\u0CBB\u0CC5\u0CC9\u0CCE-\u0CD4\u0CD7-\u0CDD\u0CDF\u0CE4\u0CE5\u0CF0\u0CF3-\u0CFF\u0D0D\u0D11\u0D45\u0D49\u0D4F-\u0D53\u0D58-\u0D5E\u0D64\u0D65\u0D70-\u0D79\u0D80\u0D84\u0D97-\u0D99\u0DB2\u0DBC\u0DBE\u0DBF\u0DC7-\u0DC9\u0DCB-\u0DCE\u0DD5\u0DD7\u0DE0-\u0DE5\u0DF0\u0DF1\u0DF4-\u0E00\u0E3B-\u0E3F\u0E4F\u0E5A-\u0E80\u0E83\u0E85\u0E8B\u0EA4\u0EA6\u0EBE\u0EBF\u0EC5\u0EC7\u0ECE\u0ECF\u0EDA\u0EDB\u0EE0-\u0EFF\u0F01-\u0F17\u0F1A-\u0F1F\u0F2A-\u0F34\u0F36\u0F38\u0F3A-\u0F3D\u0F48\u0F6D-\u0F70\u0F85\u0F98\u0FBD-\u0FC5\u0FC7-\u0FFF\u104A-\u104F\u109E\u109F\u10C6\u10C8-\u10CC\u10CE\u10CF\u10FB\u1249\u124E\u124F\u1257\u1259\u125E\u125F\u1289\u128E\u128F\u12B1\u12B6\u12B7\u12BF\u12C1\u12C6\u12C7\u12D7\u1311\u1316\u1317\u135B\u135C\u1360-\u137F\u1390-\u139F\u13F6\u13F7\u13FE-\u1400\u166D\u166E\u1680\u169B-\u169F\u16EB-\u16ED\u16F9-\u16FF\u170D\u1715-\u171F\u1735-\u173F\u1754-\u175F\u176D\u1771\u1774-\u177F\u17D4-\u17D6\u17D8-\u17DB\u17DE\u17DF\u17EA-\u180A\u180E\u180F\u181A-\u181F\u1879-\u187F\u18AB-\u18AF\u18F6-\u18FF\u191F\u192C-\u192F\u193C-\u1945\u196E\u196F\u1975-\u197F\u19AC-\u19AF\u19CA-\u19CF\u19DA-\u19FF\u1A1C-\u1A1F\u1A5F\u1A7D\u1A7E\u1A8A-\u1A8F\u1A9A-\u1AA6\u1AA8-\u1AAF\u1AC1-\u1AFF\u1B4C-\u1B4F\u1B5A-\u1B6A\u1B74-\u1B7F\u1BF4-\u1BFF\u1C38-\u1C3F\u1C4A-\u1C4C\u1C7E\u1C7F\u1C89-\u1C8F\u1CBB\u1CBC\u1CC0-\u1CCF\u1CD3\u1CFB-\u1CFF\u1DFA\u1F16\u1F17\u1F1E\u1F1F\u1F46\u1F47\u1F4E\u1F4F\u1F58\u1F5A\u1F5C\u1F5E\u1F7E\u1F7F\u1FB5\u1FBD\u1FBF-\u1FC1\u1FC5\u1FCD-\u1FCF\u1FD4\u1FD5\u1FDC-\u1FDF\u1FED-\u1FF1\u1FF5\u1FFD-\u203E\u2041-\u2053\u2055-\u2070\u2072-\u207E\u2080-\u208F\u209D-\u20CF\u20F1-\u2101\u2103-\u2106\u2108\u2109\u2114\u2116-\u2118\u211E-\u2123\u2125\u2127\u2129\u212E\u213A\u213B\u2140-\u2144\u214A-\u214D\u214F-\u215F\u2189-\u24B5\u24EA-\u2BFF\u2C2F\u2C5F\u2CE5-\u2CEA\u2CF4-\u2CFF\u2D26\u2D28-\u2D2C\u2D2E\u2D2F\u2D68-\u2D6E\u2D70-\u2D7E\u2D97-\u2D9F\u2DA7\u2DAF\u2DB7\u2DBF\u2DC7\u2DCF\u2DD7\u2DDF\u2E00-\u2E2E\u2E30-\u3004\u3008-\u3020\u3030\u3036\u3037\u303D-\u3040\u3097\u3098\u309B\u309C\u30A0\u30FB\u3100-\u3104\u3130\u318F-\u319F\u31C0-\u31EF\u3200-\u33FF\u4DC0-\u4DFF\u9FFD-\u9FFF\uA48D-\uA4CF\uA4FE\uA4FF\uA60D-\uA60F\uA62C-\uA63F\uA673\uA67E\uA6F2-\uA716\uA720\uA721\uA789\uA78A\uA7C0\uA7C1\uA7CB-\uA7F4\uA828-\uA82B\uA82D-\uA83F\uA874-\uA87F\uA8C6-\uA8CF\uA8DA-\uA8DF\uA8F8-\uA8FA\uA8FC\uA92E\uA92F\uA954-\uA95F\uA97D-\uA97F\uA9C1-\uA9CE\uA9DA-\uA9DF\uA9FF\uAA37-\uAA3F\uAA4E\uAA4F\uAA5A-\uAA5F\uAA77-\uAA79\uAAC3-\uAADA\uAADE\uAADF\uAAF0\uAAF1\uAAF7-\uAB00\uAB07\uAB08\uAB0F\uAB10\uAB17-\uAB1F\uAB27\uAB2F\uAB5B\uAB6A-\uAB6F\uABEB\uABEE\uABEF\uABFA-\uABFF\uD7A4-\uD7AF\uD7C7-\uD7CA\uD7FC-\uD7FF\uE000-\uF8FF\uFA6E\uFA6F\uFADA-\uFAFF\uFB07-\uFB12\uFB18-\uFB1C\uFB29\uFB37\uFB3D\uFB3F\uFB42\uFB45\uFBB2-\uFBD2\uFD3E-\uFD4F\uFD90\uFD91\uFDC8-\uFDEF\uFDFC-\uFDFF\uFE10-\uFE1F\uFE30-\uFE32\uFE35-\uFE4C\uFE50-\uFE6F\uFE75\uFEFD-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF3E\uFF40\uFF5B-\uFF65\uFFBF-\uFFC1\uFFC8\uFFC9\uFFD0\uFFD1\uFFD8\uFFD9\uFFDD-\uFFFF]|\uD800[\uDC0C\uDC27\uDC3B\uDC3E\uDC4E\uDC4F\uDC5E-\uDC7F\uDCFB-\uDD3F\uDD75-\uDDFC\uDDFE-\uDE7F\uDE9D-\uDE9F\uDED1-\uDEDF\uDEE1-\uDEFF\uDF20-\uDF2C\uDF4B-\uDF4F\uDF7B-\uDF7F\uDF9E\uDF9F\uDFC4-\uDFC7\uDFD0\uDFD6-\uDFFF]|\uD801[\uDC9E\uDC9F\uDCAA-\uDCAF\uDCD4-\uDCD7\uDCFC-\uDCFF\uDD28-\uDD2F\uDD64-\uDDFF\uDF37-\uDF3F\uDF56-\uDF5F\uDF68-\uDFFF]|\uD802[\uDC06\uDC07\uDC09\uDC36\uDC39-\uDC3B\uDC3D\uDC3E\uDC56-\uDC5F\uDC77-\uDC7F\uDC9F-\uDCDF\uDCF3\uDCF6-\uDCFF\uDD16-\uDD1F\uDD3A-\uDD7F\uDDB8-\uDDBD\uDDC0-\uDDFF\uDE04\uDE07-\uDE0B\uDE14\uDE18\uDE36\uDE37\uDE3B-\uDE3E\uDE40-\uDE5F\uDE7D-\uDE7F\uDE9D-\uDEBF\uDEC8\uDEE7-\uDEFF\uDF36-\uDF3F\uDF56-\uDF5F\uDF73-\uDF7F\uDF92-\uDFFF]|\uD803[\uDC49-\uDC7F\uDCB3-\uDCBF\uDCF3-\uDCFF\uDD28-\uDD2F\uDD3A-\uDE7F\uDEAA\uDEAD-\uDEAF\uDEB2-\uDEFF\uDF1D-\uDF26\uDF28-\uDF2F\uDF51-\uDFAF\uDFC5-\uDFDF\uDFF7-\uDFFF]|\uD804[\uDC47-\uDC65\uDC70-\uDC7E\uDCBB-\uDCCF\uDCE9-\uDCEF\uDCFA-\uDCFF\uDD35\uDD40-\uDD43\uDD48-\uDD4F\uDD74\uDD75\uDD77-\uDD7F\uDDC5-\uDDC8\uDDCD\uDDDB\uDDDD-\uDDFF\uDE12\uDE38-\uDE3D\uDE3F-\uDE7F\uDE87\uDE89\uDE8E\uDE9E\uDEA9-\uDEAF\uDEEB-\uDEEF\uDEFA-\uDEFF\uDF04\uDF0D\uDF0E\uDF11\uDF12\uDF29\uDF31\uDF34\uDF3A\uDF45\uDF46\uDF49\uDF4A\uDF4E\uDF4F\uDF51-\uDF56\uDF58-\uDF5C\uDF64\uDF65\uDF6D-\uDF6F\uDF75-\uDFFF]|\uD805[\uDC4B-\uDC4F\uDC5A-\uDC5D\uDC62-\uDC7F\uDCC6\uDCC8-\uDCCF\uDCDA-\uDD7F\uDDB6\uDDB7\uDDC1-\uDDD7\uDDDE-\uDDFF\uDE41-\uDE43\uDE45-\uDE4F\uDE5A-\uDE7F\uDEB9-\uDEBF\uDECA-\uDEFF\uDF1B\uDF1C\uDF2C-\uDF2F\uDF3A-\uDFFF]|\uD806[\uDC3B-\uDC9F\uDCEA-\uDCFE\uDD07\uDD08\uDD0A\uDD0B\uDD14\uDD17\uDD36\uDD39\uDD3A\uDD44-\uDD4F\uDD5A-\uDD9F\uDDA8\uDDA9\uDDD8\uDDD9\uDDE2\uDDE5-\uDDFF\uDE3F-\uDE46\uDE48-\uDE4F\uDE9A-\uDE9C\uDE9E-\uDEBF\uDEF9-\uDFFF]|\uD807[\uDC09\uDC37\uDC41-\uDC4F\uDC5A-\uDC71\uDC90\uDC91\uDCA8\uDCB7-\uDCFF\uDD07\uDD0A\uDD37-\uDD39\uDD3B\uDD3E\uDD48-\uDD4F\uDD5A-\uDD5F\uDD66\uDD69\uDD8F\uDD92\uDD99-\uDD9F\uDDAA-\uDEDF\uDEF7-\uDFAF\uDFB1-\uDFFF]|\uD808[\uDF9A-\uDFFF]|\uD809[\uDC6F-\uDC7F\uDD44-\uDFFF]|[\uD80A\uD80B\uD80E-\uD810\uD812-\uD819\uD824-\uD82B\uD82D\uD82E\uD830-\uD833\uD837\uD839\uD83D\uD83F\uD87B-\uD87D\uD87F\uD885-\uDB3F\uDB41-\uDBFF][\uDC00-\uDFFF]|\uD80D[\uDC2F-\uDFFF]|\uD811[\uDE47-\uDFFF]|\uD81A[\uDE39-\uDE3F\uDE5F\uDE6A-\uDECF\uDEEE\uDEEF\uDEF5-\uDEFF\uDF37-\uDF3F\uDF44-\uDF4F\uDF5A-\uDF62\uDF78-\uDF7C\uDF90-\uDFFF]|\uD81B[\uDC00-\uDE3F\uDE80-\uDEFF\uDF4B-\uDF4E\uDF88-\uDF8E\uDFA0-\uDFDF\uDFE2\uDFE5-\uDFEF\uDFF2-\uDFFF]|\uD821[\uDFF8-\uDFFF]|\uD823[\uDCD6-\uDCFF\uDD09-\uDFFF]|\uD82C[\uDD1F-\uDD4F\uDD53-\uDD63\uDD68-\uDD6F\uDEFC-\uDFFF]|\uD82F[\uDC6B-\uDC6F\uDC7D-\uDC7F\uDC89-\uDC8F\uDC9A-\uDC9C\uDC9F-\uDFFF]|\uD834[\uDC00-\uDD64\uDD6A-\uDD6C\uDD73-\uDD7A\uDD83\uDD84\uDD8C-\uDDA9\uDDAE-\uDE41\uDE45-\uDFFF]|\uD835[\uDC55\uDC9D\uDCA0\uDCA1\uDCA3\uDCA4\uDCA7\uDCA8\uDCAD\uDCBA\uDCBC\uDCC4\uDD06\uDD0B\uDD0C\uDD15\uDD1D\uDD3A\uDD3F\uDD45\uDD47-\uDD49\uDD51\uDEA6\uDEA7\uDEC1\uDEDB\uDEFB\uDF15\uDF35\uDF4F\uDF6F\uDF89\uDFA9\uDFC3\uDFCC\uDFCD]|\uD836[\uDC00-\uDDFF\uDE37-\uDE3A\uDE6D-\uDE74\uDE76-\uDE83\uDE85-\uDE9A\uDEA0\uDEB0-\uDFFF]|\uD838[\uDC07\uDC19\uDC1A\uDC22\uDC25\uDC2B-\uDCFF\uDD2D-\uDD2F\uDD3E\uDD3F\uDD4A-\uDD4D\uDD4F-\uDEBF\uDEFA-\uDFFF]|\uD83A[\uDCC5-\uDCCF\uDCD7-\uDCFF\uDD4C-\uDD4F\uDD5A-\uDFFF]|\uD83B[\uDC00-\uDDFF\uDE04\uDE20\uDE23\uDE25\uDE26\uDE28\uDE33\uDE38\uDE3A\uDE3C-\uDE41\uDE43-\uDE46\uDE48\uDE4A\uDE4C\uDE50\uDE53\uDE55\uDE56\uDE58\uDE5A\uDE5C\uDE5E\uDE60\uDE63\uDE65\uDE66\uDE6B\uDE73\uDE78\uDE7D\uDE7F\uDE8A\uDE9C-\uDEA0\uDEA4\uDEAA\uDEBC-\uDFFF]|\uD83C[\uDC00-\uDD2F\uDD4A-\uDD4F\uDD6A-\uDD6F\uDD8A-\uDFFF]|\uD83E[\uDC00-\uDFEF\uDFFA-\uDFFF]|\uD869[\uDEDE-\uDEFF]|\uD86D[\uDF35-\uDF3F]|\uD86E[\uDC1E\uDC1F]|\uD873[\uDEA2-\uDEAF]|\uD87A[\uDFE1-\uDFFF]|\uD87E[\uDE1E-\uDFFF]|\uD884[\uDF4B-\uDFFF]|\uDB40[\uDC00-\uDCFF\uDDF0-\uDFFF]/g,Ft$1=Object.hasOwnProperty;let K$1 = class K{constructor(){this.occurrences,this.reset();}slug(t,e){const n=this;let u=bt(t,e===true);const s=u;for(;Ft$1.call(n.occurrences,u);)n.occurrences[s]++,u=s+"-"+n.occurrences[s];return n.occurrences[u]=0,u}reset(){this.occurrences=Object.create(null);}};function bt(i,t){return typeof i!="string"?"":(t||(i=i.toLowerCase()),i.replace(Et,"").replace(/ /g,"-"))}let ye=new K$1,_e$1=[];function At$1({prefix:i="",globalSlugs:t=false}={}){return {headerIds:false,hooks:{preprocess(e){return t||kt(),e}},renderer:{heading(e,n,u){u=u.toLowerCase().trim().replace(/<[!\/a-z].*?>/gi,"");const s=`${i}${ye.slug(u)}`,r={level:n,text:e,id:s};return _e$1.push(r),`<h${n} id="${s}">${e}</h${n}>
`}}}}function kt(){_e$1=[],ye=new K$1;}(function(i){var t=/\\(?:[^a-z()[\]]|[a-z*]+)/i,e={"equation-command":{pattern:t,alias:"regex"}};i.languages.latex={comment:/%.*/,cdata:{pattern:/(\\begin\{((?:lstlisting|verbatim)\*?)\})[\s\S]*?(?=\\end\{\2\})/,lookbehind:true},equation:[{pattern:/\$\$(?:\\[\s\S]|[^\\$])+\$\$|\$(?:\\[\s\S]|[^\\$])+\$|\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]/,inside:e,alias:"string"},{pattern:/(\\begin\{((?:align|eqnarray|equation|gather|math|multline)\*?)\})[\s\S]*?(?=\\end\{\2\})/,lookbehind:true,inside:e,alias:"string"}],keyword:{pattern:/(\\(?:begin|cite|documentclass|end|label|ref|usepackage)(?:\[[^\]]+\])?\{)[^}]+(?=\})/,lookbehind:true},url:{pattern:/(\\url\{)[^}]+(?=\})/,lookbehind:true},headline:{pattern:/(\\(?:chapter|frametitle|paragraph|part|section|subparagraph|subsection|subsubparagraph|subsubsection|subsubsubparagraph)\*?(?:\[[^\]]+\])?\{)[^}]+(?=\})/,lookbehind:true,alias:"class-name"},function:{pattern:t,alias:"selector"},punctuation:/[[\]{}&]/},i.languages.tex=i.languages.latex,i.languages.context=i.languages.latex;})(Prism);(function(i){var t="\\b(?:BASH|BASHOPTS|BASH_ALIASES|BASH_ARGC|BASH_ARGV|BASH_CMDS|BASH_COMPLETION_COMPAT_DIR|BASH_LINENO|BASH_REMATCH|BASH_SOURCE|BASH_VERSINFO|BASH_VERSION|COLORTERM|COLUMNS|COMP_WORDBREAKS|DBUS_SESSION_BUS_ADDRESS|DEFAULTS_PATH|DESKTOP_SESSION|DIRSTACK|DISPLAY|EUID|GDMSESSION|GDM_LANG|GNOME_KEYRING_CONTROL|GNOME_KEYRING_PID|GPG_AGENT_INFO|GROUPS|HISTCONTROL|HISTFILE|HISTFILESIZE|HISTSIZE|HOME|HOSTNAME|HOSTTYPE|IFS|INSTANCE|JOB|LANG|LANGUAGE|LC_ADDRESS|LC_ALL|LC_IDENTIFICATION|LC_MEASUREMENT|LC_MONETARY|LC_NAME|LC_NUMERIC|LC_PAPER|LC_TELEPHONE|LC_TIME|LESSCLOSE|LESSOPEN|LINES|LOGNAME|LS_COLORS|MACHTYPE|MAILCHECK|MANDATORY_PATH|NO_AT_BRIDGE|OLDPWD|OPTERR|OPTIND|ORBIT_SOCKETDIR|OSTYPE|PAPERSIZE|PATH|PIPESTATUS|PPID|PS1|PS2|PS3|PS4|PWD|RANDOM|REPLY|SECONDS|SELINUX_INIT|SESSION|SESSIONTYPE|SESSION_MANAGER|SHELL|SHELLOPTS|SHLVL|SSH_AUTH_SOCK|TERM|UID|UPSTART_EVENTS|UPSTART_INSTANCE|UPSTART_JOB|UPSTART_SESSION|USER|WINDOWID|XAUTHORITY|XDG_CONFIG_DIRS|XDG_CURRENT_DESKTOP|XDG_DATA_DIRS|XDG_GREETER_DATA_DIR|XDG_MENU_PREFIX|XDG_RUNTIME_DIR|XDG_SEAT|XDG_SEAT_PATH|XDG_SESSION_DESKTOP|XDG_SESSION_ID|XDG_SESSION_PATH|XDG_SESSION_TYPE|XDG_VTNR|XMODIFIERS)\\b",e={pattern:/(^(["']?)\w+\2)[ \t]+\S.*/,lookbehind:true,alias:"punctuation",inside:null},n={bash:e,environment:{pattern:RegExp("\\$"+t),alias:"constant"},variable:[{pattern:/\$?\(\([\s\S]+?\)\)/,greedy:true,inside:{variable:[{pattern:/(^\$\(\([\s\S]+)\)\)/,lookbehind:true},/^\$\(\(/],number:/\b0x[\dA-Fa-f]+\b|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:[Ee]-?\d+)?/,operator:/--|\+\+|\*\*=?|<<=?|>>=?|&&|\|\||[=!+\-*/%<>^&|]=?|[?~:]/,punctuation:/\(\(?|\)\)?|,|;/}},{pattern:/\$\((?:\([^)]+\)|[^()])+\)|`[^`]+`/,greedy:true,inside:{variable:/^\$\(|^`|\)$|`$/}},{pattern:/\$\{[^}]+\}/,greedy:true,inside:{operator:/:[-=?+]?|[!\/]|##?|%%?|\^\^?|,,?/,punctuation:/[\[\]]/,environment:{pattern:RegExp("(\\{)"+t),lookbehind:true,alias:"constant"}}},/\$(?:\w+|[#?*!@$])/],entity:/\\(?:[abceEfnrtv\\"]|O?[0-7]{1,3}|U[0-9a-fA-F]{8}|u[0-9a-fA-F]{4}|x[0-9a-fA-F]{1,2})/};i.languages.bash={shebang:{pattern:/^#!\s*\/.*/,alias:"important"},comment:{pattern:/(^|[^"{\\$])#.*/,lookbehind:true},"function-name":[{pattern:/(\bfunction\s+)[\w-]+(?=(?:\s*\(?:\s*\))?\s*\{)/,lookbehind:true,alias:"function"},{pattern:/\b[\w-]+(?=\s*\(\s*\)\s*\{)/,alias:"function"}],"for-or-select":{pattern:/(\b(?:for|select)\s+)\w+(?=\s+in\s)/,alias:"variable",lookbehind:true},"assign-left":{pattern:/(^|[\s;|&]|[<>]\()\w+(?:\.\w+)*(?=\+?=)/,inside:{environment:{pattern:RegExp("(^|[\\s;|&]|[<>]\\()"+t),lookbehind:true,alias:"constant"}},alias:"variable",lookbehind:true},parameter:{pattern:/(^|\s)-{1,2}(?:\w+:[+-]?)?\w+(?:\.\w+)*(?=[=\s]|$)/,alias:"variable",lookbehind:true},string:[{pattern:/((?:^|[^<])<<-?\s*)(\w+)\s[\s\S]*?(?:\r?\n|\r)\2/,lookbehind:true,greedy:true,inside:n},{pattern:/((?:^|[^<])<<-?\s*)(["'])(\w+)\2\s[\s\S]*?(?:\r?\n|\r)\3/,lookbehind:true,greedy:true,inside:{bash:e}},{pattern:/(^|[^\\](?:\\\\)*)"(?:\\[\s\S]|\$\([^)]+\)|\$(?!\()|`[^`]+`|[^"\\`$])*"/,lookbehind:true,greedy:true,inside:n},{pattern:/(^|[^$\\])'[^']*'/,lookbehind:true,greedy:true},{pattern:/\$'(?:[^'\\]|\\[\s\S])*'/,greedy:true,inside:{entity:n.entity}}],environment:{pattern:RegExp("\\$?"+t),alias:"constant"},variable:n.variable,function:{pattern:/(^|[\s;|&]|[<>]\()(?:add|apropos|apt|apt-cache|apt-get|aptitude|aspell|automysqlbackup|awk|basename|bash|bc|bconsole|bg|bzip2|cal|cargo|cat|cfdisk|chgrp|chkconfig|chmod|chown|chroot|cksum|clear|cmp|column|comm|composer|cp|cron|crontab|csplit|curl|cut|date|dc|dd|ddrescue|debootstrap|df|diff|diff3|dig|dir|dircolors|dirname|dirs|dmesg|docker|docker-compose|du|egrep|eject|env|ethtool|expand|expect|expr|fdformat|fdisk|fg|fgrep|file|find|fmt|fold|format|free|fsck|ftp|fuser|gawk|git|gparted|grep|groupadd|groupdel|groupmod|groups|grub-mkconfig|gzip|halt|head|hg|history|host|hostname|htop|iconv|id|ifconfig|ifdown|ifup|import|install|ip|java|jobs|join|kill|killall|less|link|ln|locate|logname|logrotate|look|lpc|lpr|lprint|lprintd|lprintq|lprm|ls|lsof|lynx|make|man|mc|mdadm|mkconfig|mkdir|mke2fs|mkfifo|mkfs|mkisofs|mknod|mkswap|mmv|more|most|mount|mtools|mtr|mutt|mv|nano|nc|netstat|nice|nl|node|nohup|notify-send|npm|nslookup|op|open|parted|passwd|paste|pathchk|ping|pkill|pnpm|podman|podman-compose|popd|pr|printcap|printenv|ps|pushd|pv|quota|quotacheck|quotactl|ram|rar|rcp|reboot|remsync|rename|renice|rev|rm|rmdir|rpm|rsync|scp|screen|sdiff|sed|sendmail|seq|service|sftp|sh|shellcheck|shuf|shutdown|sleep|slocate|sort|split|ssh|stat|strace|su|sudo|sum|suspend|swapon|sync|sysctl|tac|tail|tar|tee|time|timeout|top|touch|tr|traceroute|tsort|tty|umount|uname|unexpand|uniq|units|unrar|unshar|unzip|update-grub|uptime|useradd|userdel|usermod|users|uudecode|uuencode|v|vcpkg|vdir|vi|vim|virsh|vmstat|wait|watch|wc|wget|whereis|which|who|whoami|write|xargs|xdg-open|yarn|yes|zenity|zip|zsh|zypper)(?=$|[)\s;|&])/,lookbehind:true},keyword:{pattern:/(^|[\s;|&]|[<>]\()(?:case|do|done|elif|else|esac|fi|for|function|if|in|select|then|until|while)(?=$|[)\s;|&])/,lookbehind:true},builtin:{pattern:/(^|[\s;|&]|[<>]\()(?:\.|:|alias|bind|break|builtin|caller|cd|command|continue|declare|echo|enable|eval|exec|exit|export|getopts|hash|help|let|local|logout|mapfile|printf|pwd|read|readarray|readonly|return|set|shift|shopt|source|test|times|trap|type|typeset|ulimit|umask|unalias|unset)(?=$|[)\s;|&])/,lookbehind:true,alias:"class-name"},boolean:{pattern:/(^|[\s;|&]|[<>]\()(?:false|true)(?=$|[)\s;|&])/,lookbehind:true},"file-descriptor":{pattern:/\B&\d\b/,alias:"important"},operator:{pattern:/\d?<>|>\||\+=|=[=~]?|!=?|<<[<-]?|[&\d]?>>|\d[<>]&?|[<>][&=]?|&[>&]?|\|[&|]?/,inside:{"file-descriptor":{pattern:/^\d/,alias:"important"}}},punctuation:/\$?\(\(?|\)\)?|\.\.|[{}[\];\\]/,number:{pattern:/(^|\s)(?:[1-9]\d*|0)(?:[.,]\d+)?\b/,lookbehind:true}},e.inside=i.languages.bash;for(var u=["comment","function-name","for-or-select","assign-left","parameter","string","environment","function","keyword","builtin","boolean","file-descriptor","operator","punctuation","number"],s=n.variable[1].inside,r=0;r<u.length;r++)s[u[r]]=i.languages.bash[u[r]];i.languages.sh=i.languages.bash,i.languages.shell=i.languages.bash;})(Prism);Prism.languages.c=Prism.languages.extend("clike",{comment:{pattern:/\/\/(?:[^\r\n\\]|\\(?:\r\n?|\n|(?![\r\n])))*|\/\*[\s\S]*?(?:\*\/|$)/,greedy:true},string:{pattern:/"(?:\\(?:\r\n|[\s\S])|[^"\\\r\n])*"/,greedy:true},"class-name":{pattern:/(\b(?:enum|struct)\s+(?:__attribute__\s*\(\([\s\S]*?\)\)\s*)?)\w+|\b[a-z]\w*_t\b/,lookbehind:true},keyword:/\b(?:_Alignas|_Alignof|_Atomic|_Bool|_Complex|_Generic|_Imaginary|_Noreturn|_Static_assert|_Thread_local|__attribute__|asm|auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|inline|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|typeof|union|unsigned|void|volatile|while)\b/,function:/\b[a-z_]\w*(?=\s*\()/i,number:/(?:\b0x(?:[\da-f]+(?:\.[\da-f]*)?|\.[\da-f]+)(?:p[+-]?\d+)?|(?:\b\d+(?:\.\d*)?|\B\.\d+)(?:e[+-]?\d+)?)[ful]{0,4}/i,operator:/>>=?|<<=?|->|([-+&|:])\1|[?:~]|[-+*/%&|^!=<>]=?/});Prism.languages.insertBefore("c","string",{char:{pattern:/'(?:\\(?:\r\n|[\s\S])|[^'\\\r\n]){0,32}'/,greedy:true}});Prism.languages.insertBefore("c","string",{macro:{pattern:/(^[\t ]*)#\s*[a-z](?:[^\r\n\\/]|\/(?!\*)|\/\*(?:[^*]|\*(?!\/))*\*\/|\\(?:\r\n|[\s\S]))*/im,lookbehind:true,greedy:true,alias:"property",inside:{string:[{pattern:/^(#\s*include\s*)<[^>]+>/,lookbehind:true},Prism.languages.c.string],char:Prism.languages.c.char,comment:Prism.languages.c.comment,"macro-name":[{pattern:/(^#\s*define\s+)\w+\b(?!\()/i,lookbehind:true},{pattern:/(^#\s*define\s+)\w+\b(?=\()/i,lookbehind:true,alias:"function"}],directive:{pattern:/^(#\s*)[a-z]+/,lookbehind:true,alias:"keyword"},"directive-hash":/^#/,punctuation:/##|\\(?=[\r\n])/,expression:{pattern:/\S[\s\S]*/,inside:Prism.languages.c}}}});Prism.languages.insertBefore("c","function",{constant:/\b(?:EOF|NULL|SEEK_CUR|SEEK_END|SEEK_SET|__DATE__|__FILE__|__LINE__|__TIMESTAMP__|__TIME__|__func__|stderr|stdin|stdout)\b/});delete Prism.languages.c.boolean;var ie$1={},ae$1;function mt(){return ae$1||(ae$1=1,(function(i){var t=/\b(?:alignas|alignof|asm|auto|bool|break|case|catch|char|char16_t|char32_t|char8_t|class|co_await|co_return|co_yield|compl|concept|const|const_cast|consteval|constexpr|constinit|continue|decltype|default|delete|do|double|dynamic_cast|else|enum|explicit|export|extern|final|float|for|friend|goto|if|import|inline|int|int16_t|int32_t|int64_t|int8_t|long|module|mutable|namespace|new|noexcept|nullptr|operator|override|private|protected|public|register|reinterpret_cast|requires|return|short|signed|sizeof|static|static_assert|static_cast|struct|switch|template|this|thread_local|throw|try|typedef|typeid|typename|uint16_t|uint32_t|uint64_t|uint8_t|union|unsigned|using|virtual|void|volatile|wchar_t|while)\b/,e=/\b(?!<keyword>)\w+(?:\s*\.\s*\w+)*\b/.source.replace(/<keyword>/g,function(){return t.source});i.languages.cpp=i.languages.extend("c",{"class-name":[{pattern:RegExp(/(\b(?:class|concept|enum|struct|typename)\s+)(?!<keyword>)\w+/.source.replace(/<keyword>/g,function(){return t.source})),lookbehind:true},/\b[A-Z]\w*(?=\s*::\s*\w+\s*\()/,/\b[A-Z_]\w*(?=\s*::\s*~\w+\s*\()/i,/\b\w+(?=\s*<(?:[^<>]|<(?:[^<>]|<[^<>]*>)*>)*>\s*::\s*\w+\s*\()/],keyword:t,number:{pattern:/(?:\b0b[01']+|\b0x(?:[\da-f']+(?:\.[\da-f']*)?|\.[\da-f']+)(?:p[+-]?[\d']+)?|(?:\b[\d']+(?:\.[\d']*)?|\B\.[\d']+)(?:e[+-]?[\d']+)?)[ful]{0,4}/i,greedy:true},operator:/>>=?|<<=?|->|--|\+\+|&&|\|\||[?:~]|<=>|[-+*/%&|^!=<>]=?|\b(?:and|and_eq|bitand|bitor|not|not_eq|or|or_eq|xor|xor_eq)\b/,boolean:/\b(?:false|true)\b/}),i.languages.insertBefore("cpp","string",{module:{pattern:RegExp(/(\b(?:import|module)\s+)/.source+"(?:"+/"(?:\\(?:\r\n|[\s\S])|[^"\\\r\n])*"|<[^<>\r\n]*>/.source+"|"+/<mod-name>(?:\s*:\s*<mod-name>)?|:\s*<mod-name>/.source.replace(/<mod-name>/g,function(){return e})+")"),lookbehind:true,greedy:true,inside:{string:/^[<"][\s\S]+/,operator:/:/,punctuation:/\./}},"raw-string":{pattern:/R"([^()\\ ]{0,16})\([\s\S]*?\)\1"/,alias:"string",greedy:true}}),i.languages.insertBefore("cpp","keyword",{"generic-function":{pattern:/\b(?!operator\b)[a-z_]\w*\s*<(?:[^<>]|<[^<>]*>)*>(?=\s*\()/i,inside:{function:/^\w+/,generic:{pattern:/<[\s\S]+/,alias:"class-name",inside:i.languages.cpp}}}}),i.languages.insertBefore("cpp","operator",{"double-colon":{pattern:/::/,alias:"punctuation"}}),i.languages.insertBefore("cpp","class-name",{"base-clause":{pattern:/(\b(?:class|struct)\s+\w+\s*:\s*)[^;{}"'\s]+(?:\s+[^;{}"'\s]+)*(?=\s*[;{])/,lookbehind:true,greedy:true,inside:i.languages.extend("cpp",{})}}),i.languages.insertBefore("inside","double-colon",{"class-name":/\b[a-z_]\w*\b(?!\s*::)/i},i.languages.cpp["base-clause"]);})(Prism)),ie$1}mt();Prism.languages.json={property:{pattern:/(^|[^\\])"(?:\\.|[^\\"\r\n])*"(?=\s*:)/,lookbehind:true,greedy:true},string:{pattern:/(^|[^\\])"(?:\\.|[^\\"\r\n])*"(?!\s*:)/,lookbehind:true,greedy:true},comment:{pattern:/\/\/.*|\/\*[\s\S]*?(?:\*\/|$)/,greedy:true},number:/-?\b\d+(?:\.\d+)?(?:e[+-]?\d+)?\b/i,punctuation:/[{}[\],]/,operator:/:/,boolean:/\b(?:false|true)\b/,null:{pattern:/\bnull\b/,alias:"keyword"}};Prism.languages.webmanifest=Prism.languages.json;Prism.languages.sql={comment:{pattern:/(^|[^\\])(?:\/\*[\s\S]*?\*\/|(?:--|\/\/|#).*)/,lookbehind:true},variable:[{pattern:/@(["'`])(?:\\[\s\S]|(?!\1)[^\\])+\1/,greedy:true},/@[\w.$]+/],string:{pattern:/(^|[^@\\])("|')(?:\\[\s\S]|(?!\2)[^\\]|\2\2)*\2/,greedy:true,lookbehind:true},identifier:{pattern:/(^|[^@\\])`(?:\\[\s\S]|[^`\\]|``)*`/,greedy:true,lookbehind:true,inside:{punctuation:/^`|`$/}},function:/\b(?:AVG|COUNT|FIRST|FORMAT|LAST|LCASE|LEN|MAX|MID|MIN|MOD|NOW|ROUND|SUM|UCASE)(?=\s*\()/i,keyword:/\b(?:ACTION|ADD|AFTER|ALGORITHM|ALL|ALTER|ANALYZE|ANY|APPLY|AS|ASC|AUTHORIZATION|AUTO_INCREMENT|BACKUP|BDB|BEGIN|BERKELEYDB|BIGINT|BINARY|BIT|BLOB|BOOL|BOOLEAN|BREAK|BROWSE|BTREE|BULK|BY|CALL|CASCADED?|CASE|CHAIN|CHAR(?:ACTER|SET)?|CHECK(?:POINT)?|CLOSE|CLUSTERED|COALESCE|COLLATE|COLUMNS?|COMMENT|COMMIT(?:TED)?|COMPUTE|CONNECT|CONSISTENT|CONSTRAINT|CONTAINS(?:TABLE)?|CONTINUE|CONVERT|CREATE|CROSS|CURRENT(?:_DATE|_TIME|_TIMESTAMP|_USER)?|CURSOR|CYCLE|DATA(?:BASES?)?|DATE(?:TIME)?|DAY|DBCC|DEALLOCATE|DEC|DECIMAL|DECLARE|DEFAULT|DEFINER|DELAYED|DELETE|DELIMITERS?|DENY|DESC|DESCRIBE|DETERMINISTIC|DISABLE|DISCARD|DISK|DISTINCT|DISTINCTROW|DISTRIBUTED|DO|DOUBLE|DROP|DUMMY|DUMP(?:FILE)?|DUPLICATE|ELSE(?:IF)?|ENABLE|ENCLOSED|END|ENGINE|ENUM|ERRLVL|ERRORS|ESCAPED?|EXCEPT|EXEC(?:UTE)?|EXISTS|EXIT|EXPLAIN|EXTENDED|FETCH|FIELDS|FILE|FILLFACTOR|FIRST|FIXED|FLOAT|FOLLOWING|FOR(?: EACH ROW)?|FORCE|FOREIGN|FREETEXT(?:TABLE)?|FROM|FULL|FUNCTION|GEOMETRY(?:COLLECTION)?|GLOBAL|GOTO|GRANT|GROUP|HANDLER|HASH|HAVING|HOLDLOCK|HOUR|IDENTITY(?:COL|_INSERT)?|IF|IGNORE|IMPORT|INDEX|INFILE|INNER|INNODB|INOUT|INSERT|INT|INTEGER|INTERSECT|INTERVAL|INTO|INVOKER|ISOLATION|ITERATE|JOIN|KEYS?|KILL|LANGUAGE|LAST|LEAVE|LEFT|LEVEL|LIMIT|LINENO|LINES|LINESTRING|LOAD|LOCAL|LOCK|LONG(?:BLOB|TEXT)|LOOP|MATCH(?:ED)?|MEDIUM(?:BLOB|INT|TEXT)|MERGE|MIDDLEINT|MINUTE|MODE|MODIFIES|MODIFY|MONTH|MULTI(?:LINESTRING|POINT|POLYGON)|NATIONAL|NATURAL|NCHAR|NEXT|NO|NONCLUSTERED|NULLIF|NUMERIC|OFF?|OFFSETS?|ON|OPEN(?:DATASOURCE|QUERY|ROWSET)?|OPTIMIZE|OPTION(?:ALLY)?|ORDER|OUT(?:ER|FILE)?|OVER|PARTIAL|PARTITION|PERCENT|PIVOT|PLAN|POINT|POLYGON|PRECEDING|PRECISION|PREPARE|PREV|PRIMARY|PRINT|PRIVILEGES|PROC(?:EDURE)?|PUBLIC|PURGE|QUICK|RAISERROR|READS?|REAL|RECONFIGURE|REFERENCES|RELEASE|RENAME|REPEAT(?:ABLE)?|REPLACE|REPLICATION|REQUIRE|RESIGNAL|RESTORE|RESTRICT|RETURN(?:ING|S)?|REVOKE|RIGHT|ROLLBACK|ROUTINE|ROW(?:COUNT|GUIDCOL|S)?|RTREE|RULE|SAVE(?:POINT)?|SCHEMA|SECOND|SELECT|SERIAL(?:IZABLE)?|SESSION(?:_USER)?|SET(?:USER)?|SHARE|SHOW|SHUTDOWN|SIMPLE|SMALLINT|SNAPSHOT|SOME|SONAME|SQL|START(?:ING)?|STATISTICS|STATUS|STRIPED|SYSTEM_USER|TABLES?|TABLESPACE|TEMP(?:ORARY|TABLE)?|TERMINATED|TEXT(?:SIZE)?|THEN|TIME(?:STAMP)?|TINY(?:BLOB|INT|TEXT)|TOP?|TRAN(?:SACTIONS?)?|TRIGGER|TRUNCATE|TSEQUAL|TYPES?|UNBOUNDED|UNCOMMITTED|UNDEFINED|UNION|UNIQUE|UNLOCK|UNPIVOT|UNSIGNED|UPDATE(?:TEXT)?|USAGE|USE|USER|USING|VALUES?|VAR(?:BINARY|CHAR|CHARACTER|YING)|VIEW|WAITFOR|WARNINGS|WHEN|WHERE|WHILE|WITH(?: ROLLUP|IN)?|WORK|WRITE(?:TEXT)?|YEAR)\b/i,boolean:/\b(?:FALSE|NULL|TRUE)\b/i,number:/\b0x[\da-f]+\b|\b\d+(?:\.\d*)?|\B\.\d+\b/i,operator:/[-+*\/=%^~]|&&?|\|\|?|!=?|<(?:=>?|<|>)?|>[>=]?|\b(?:AND|BETWEEN|DIV|ILIKE|IN|IS|LIKE|NOT|OR|REGEXP|RLIKE|SOUNDS LIKE|XOR)\b/i,punctuation:/[;[\]()`,.]/};var oe$1={},le$1;function Ct(){return le$1||(le$1=1,(function(i){var t=/\b(?:abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|exports|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|module|native|new|non-sealed|null|open|opens|package|permits|private|protected|provides|public|record(?!\s*[(){}[\]<>=%~.:,;?+\-*/&|^])|requires|return|sealed|short|static|strictfp|super|switch|synchronized|this|throw|throws|to|transient|transitive|try|uses|var|void|volatile|while|with|yield)\b/,e=/(?:[a-z]\w*\s*\.\s*)*(?:[A-Z]\w*\s*\.\s*)*/.source,n={pattern:RegExp(/(^|[^\w.])/.source+e+/[A-Z](?:[\d_A-Z]*[a-z]\w*)?\b/.source),lookbehind:true,inside:{namespace:{pattern:/^[a-z]\w*(?:\s*\.\s*[a-z]\w*)*(?:\s*\.)?/,inside:{punctuation:/\./}},punctuation:/\./}};i.languages.java=i.languages.extend("clike",{string:{pattern:/(^|[^\\])"(?:\\.|[^"\\\r\n])*"/,lookbehind:true,greedy:true},"class-name":[n,{pattern:RegExp(/(^|[^\w.])/.source+e+/[A-Z]\w*(?=\s+\w+\s*[;,=()]|\s*(?:\[[\s,]*\]\s*)?::\s*new\b)/.source),lookbehind:true,inside:n.inside},{pattern:RegExp(/(\b(?:class|enum|extends|implements|instanceof|interface|new|record|throws)\s+)/.source+e+/[A-Z]\w*\b/.source),lookbehind:true,inside:n.inside}],keyword:t,function:[i.languages.clike.function,{pattern:/(::\s*)[a-z_]\w*/,lookbehind:true}],number:/\b0b[01][01_]*L?\b|\b0x(?:\.[\da-f_p+-]+|[\da-f_]+(?:\.[\da-f_p+-]+)?)\b|(?:\b\d[\d_]*(?:\.[\d_]*)?|\B\.\d[\d_]*)(?:e[+-]?\d[\d_]*)?[dfl]?/i,operator:{pattern:/(^|[^.])(?:<<=?|>>>?=?|->|--|\+\+|&&|\|\||::|[?:~]|[-+*/%&|^!=<>]=?)/m,lookbehind:true},constant:/\b[A-Z][A-Z_\d]+\b/}),i.languages.insertBefore("java","string",{"triple-quoted-string":{pattern:/"""[ \t]*[\r\n](?:(?:"|"")?(?:\\.|[^"\\]))*"""/,greedy:true,alias:"string"},char:{pattern:/'(?:\\.|[^'\\\r\n]){1,6}'/,greedy:true}}),i.languages.insertBefore("java","class-name",{annotation:{pattern:/(^|[^.])@\w+(?:\s*\.\s*\w+)*/,lookbehind:true,alias:"punctuation"},generics:{pattern:/<(?:[\w\s,.?]|&(?!&)|<(?:[\w\s,.?]|&(?!&)|<(?:[\w\s,.?]|&(?!&)|<(?:[\w\s,.?]|&(?!&))*>)*>)*>)*>/,inside:{"class-name":n,keyword:t,punctuation:/[<>(),.:]/,operator:/[?&|]/}},import:[{pattern:RegExp(/(\bimport\s+)/.source+e+/(?:[A-Z]\w*|\*)(?=\s*;)/.source),lookbehind:true,inside:{namespace:n.inside.namespace,punctuation:/\./,operator:/\*/,"class-name":/\w+/}},{pattern:RegExp(/(\bimport\s+static\s+)/.source+e+/(?:\w+|\*)(?=\s*;)/.source),lookbehind:true,alias:"static",inside:{namespace:n.inside.namespace,static:/\b\w+$/,punctuation:/\./,operator:/\*/,"class-name":/\w+/}}],namespace:{pattern:RegExp(/(\b(?:exports|import(?:\s+static)?|module|open|opens|package|provides|requires|to|transitive|uses|with)\s+)(?!<keyword>)[a-z]\w*(?:\.[a-z]\w*)*\.?/.source.replace(/<keyword>/g,function(){return t.source})),lookbehind:true,inside:{punctuation:/\./}}});})(Prism)),oe$1}Ct();Prism.languages.go=Prism.languages.extend("clike",{string:{pattern:/(^|[^\\])"(?:\\.|[^"\\\r\n])*"|`[^`]*`/,lookbehind:true,greedy:true},keyword:/\b(?:break|case|chan|const|continue|default|defer|else|fallthrough|for|func|go(?:to)?|if|import|interface|map|package|range|return|select|struct|switch|type|var)\b/,boolean:/\b(?:_|false|iota|nil|true)\b/,number:[/\b0(?:b[01_]+|o[0-7_]+)i?\b/i,/\b0x(?:[a-f\d_]+(?:\.[a-f\d_]*)?|\.[a-f\d_]+)(?:p[+-]?\d+(?:_\d+)*)?i?(?!\w)/i,/(?:\b\d[\d_]*(?:\.[\d_]*)?|\B\.\d[\d_]*)(?:e[+-]?[\d_]+)?i?(?!\w)/i],operator:/[*\/%^!=]=?|\+[=+]?|-[=-]?|\|[=|]?|&(?:=|&|\^=?)?|>(?:>=?|=)?|<(?:<=?|=|-)?|:=|\.\.\./,builtin:/\b(?:append|bool|byte|cap|close|complex|complex(?:64|128)|copy|delete|error|float(?:32|64)|u?int(?:8|16|32|64)?|imag|len|make|new|panic|print(?:ln)?|real|recover|rune|string|uintptr)\b/});Prism.languages.insertBefore("go","string",{char:{pattern:/'(?:\\.|[^'\\\r\n]){0,10}'/,greedy:true}});delete Prism.languages.go["class-name"];var ce$2={},pe$1;function wt(){return pe$1||(pe$1=1,(function(i){for(var t=/\/\*(?:[^*/]|\*(?!\/)|\/(?!\*)|<self>)*\*\//.source,e=0;e<2;e++)t=t.replace(/<self>/g,function(){return t});t=t.replace(/<self>/g,function(){return /[^\s\S]/.source}),i.languages.rust={comment:[{pattern:RegExp(/(^|[^\\])/.source+t),lookbehind:true,greedy:true},{pattern:/(^|[^\\:])\/\/.*/,lookbehind:true,greedy:true}],string:{pattern:/b?"(?:\\[\s\S]|[^\\"])*"|b?r(#*)"(?:[^"]|"(?!\1))*"\1/,greedy:true},char:{pattern:/b?'(?:\\(?:x[0-7][\da-fA-F]|u\{(?:[\da-fA-F]_*){1,6}\}|.)|[^\\\r\n\t'])'/,greedy:true},attribute:{pattern:/#!?\[(?:[^\[\]"]|"(?:\\[\s\S]|[^\\"])*")*\]/,greedy:true,alias:"attr-name",inside:{string:null}},"closure-params":{pattern:/([=(,:]\s*|\bmove\s*)\|[^|]*\||\|[^|]*\|(?=\s*(?:\{|->))/,lookbehind:true,greedy:true,inside:{"closure-punctuation":{pattern:/^\||\|$/,alias:"punctuation"},rest:null}},"lifetime-annotation":{pattern:/'\w+/,alias:"symbol"},"fragment-specifier":{pattern:/(\$\w+:)[a-z]+/,lookbehind:true,alias:"punctuation"},variable:/\$\w+/,"function-definition":{pattern:/(\bfn\s+)\w+/,lookbehind:true,alias:"function"},"type-definition":{pattern:/(\b(?:enum|struct|trait|type|union)\s+)\w+/,lookbehind:true,alias:"class-name"},"module-declaration":[{pattern:/(\b(?:crate|mod)\s+)[a-z][a-z_\d]*/,lookbehind:true,alias:"namespace"},{pattern:/(\b(?:crate|self|super)\s*)::\s*[a-z][a-z_\d]*\b(?:\s*::(?:\s*[a-z][a-z_\d]*\s*::)*)?/,lookbehind:true,alias:"namespace",inside:{punctuation:/::/}}],keyword:[/\b(?:Self|abstract|as|async|await|become|box|break|const|continue|crate|do|dyn|else|enum|extern|final|fn|for|if|impl|in|let|loop|macro|match|mod|move|mut|override|priv|pub|ref|return|self|static|struct|super|trait|try|type|typeof|union|unsafe|unsized|use|virtual|where|while|yield)\b/,/\b(?:bool|char|f(?:32|64)|[ui](?:8|16|32|64|128|size)|str)\b/],function:/\b[a-z_]\w*(?=\s*(?:::\s*<|\())/,macro:{pattern:/\b\w+!/,alias:"property"},constant:/\b[A-Z_][A-Z_\d]+\b/,"class-name":/\b[A-Z]\w*\b/,namespace:{pattern:/(?:\b[a-z][a-z_\d]*\s*::\s*)*\b[a-z][a-z_\d]*\s*::(?!\s*<)/,inside:{punctuation:/::/}},number:/\b(?:0x[\dA-Fa-f](?:_?[\dA-Fa-f])*|0o[0-7](?:_?[0-7])*|0b[01](?:_?[01])*|(?:(?:\d(?:_?\d)*)?\.)?\d(?:_?\d)*(?:[Ee][+-]?\d+)?)(?:_?(?:f32|f64|[iu](?:8|16|32|64|size)?))?\b/,boolean:/\b(?:false|true)\b/,punctuation:/->|\.\.=|\.{1,3}|::|[{}[\];(),:]/,operator:/[-+*\/%!^]=?|=[=>]?|&[&=]?|\|[|=]?|<<?=?|>>?=?|[@?]/},i.languages.rust["closure-params"].inside.rest=i.languages.rust,i.languages.rust.attribute.inside.string=i.languages.rust.string;})(Prism)),ce$2}wt();var De$1={},de$1;function xt(){return de$1||(de$1=1,(function(i){var t=/\/\*[\s\S]*?\*\/|\/\/.*|#(?!\[).*/,e=[{pattern:/\b(?:false|true)\b/i,alias:"boolean"},{pattern:/(::\s*)\b[a-z_]\w*\b(?!\s*\()/i,greedy:true,lookbehind:true},{pattern:/(\b(?:case|const)\s+)\b[a-z_]\w*(?=\s*[;=])/i,greedy:true,lookbehind:true},/\b(?:null)\b/i,/\b[A-Z_][A-Z0-9_]*\b(?!\s*\()/],n=/\b0b[01]+(?:_[01]+)*\b|\b0o[0-7]+(?:_[0-7]+)*\b|\b0x[\da-f]+(?:_[\da-f]+)*\b|(?:\b\d+(?:_\d+)*\.?(?:\d+(?:_\d+)*)?|\B\.\d+)(?:e[+-]?\d+)?/i,u=/<?=>|\?\?=?|\.{3}|\??->|[!=]=?=?|::|\*\*=?|--|\+\+|&&|\|\||<<|>>|[?~]|[/^|%*&<>.+-]=?/,s=/[{}\[\](),:;]/;i.languages.php={delimiter:{pattern:/\?>$|^<\?(?:php(?=\s)|=)?/i,alias:"important"},comment:t,variable:/\$+(?:\w+\b|(?=\{))/,package:{pattern:/(namespace\s+|use\s+(?:function\s+)?)(?:\\?\b[a-z_]\w*)+\b(?!\\)/i,lookbehind:true,inside:{punctuation:/\\/}},"class-name-definition":{pattern:/(\b(?:class|enum|interface|trait)\s+)\b[a-z_]\w*(?!\\)\b/i,lookbehind:true,alias:"class-name"},"function-definition":{pattern:/(\bfunction\s+)[a-z_]\w*(?=\s*\()/i,lookbehind:true,alias:"function"},keyword:[{pattern:/(\(\s*)\b(?:array|bool|boolean|float|int|integer|object|string)\b(?=\s*\))/i,alias:"type-casting",greedy:true,lookbehind:true},{pattern:/([(,?]\s*)\b(?:array(?!\s*\()|bool|callable|(?:false|null)(?=\s*\|)|float|int|iterable|mixed|object|self|static|string)\b(?=\s*\$)/i,alias:"type-hint",greedy:true,lookbehind:true},{pattern:/(\)\s*:\s*(?:\?\s*)?)\b(?:array(?!\s*\()|bool|callable|(?:false|null)(?=\s*\|)|float|int|iterable|mixed|never|object|self|static|string|void)\b/i,alias:"return-type",greedy:true,lookbehind:true},{pattern:/\b(?:array(?!\s*\()|bool|float|int|iterable|mixed|object|string|void)\b/i,alias:"type-declaration",greedy:true},{pattern:/(\|\s*)(?:false|null)\b|\b(?:false|null)(?=\s*\|)/i,alias:"type-declaration",greedy:true,lookbehind:true},{pattern:/\b(?:parent|self|static)(?=\s*::)/i,alias:"static-context",greedy:true},{pattern:/(\byield\s+)from\b/i,lookbehind:true},/\bclass\b/i,{pattern:/((?:^|[^\s>:]|(?:^|[^-])>|(?:^|[^:]):)\s*)\b(?:abstract|and|array|as|break|callable|case|catch|clone|const|continue|declare|default|die|do|echo|else|elseif|empty|enddeclare|endfor|endforeach|endif|endswitch|endwhile|enum|eval|exit|extends|final|finally|fn|for|foreach|function|global|goto|if|implements|include|include_once|instanceof|insteadof|interface|isset|list|match|namespace|never|new|or|parent|print|private|protected|public|readonly|require|require_once|return|self|static|switch|throw|trait|try|unset|use|var|while|xor|yield|__halt_compiler)\b/i,lookbehind:true}],"argument-name":{pattern:/([(,]\s*)\b[a-z_]\w*(?=\s*:(?!:))/i,lookbehind:true},"class-name":[{pattern:/(\b(?:extends|implements|instanceof|new(?!\s+self|\s+static))\s+|\bcatch\s*\()\b[a-z_]\w*(?!\\)\b/i,greedy:true,lookbehind:true},{pattern:/(\|\s*)\b[a-z_]\w*(?!\\)\b/i,greedy:true,lookbehind:true},{pattern:/\b[a-z_]\w*(?!\\)\b(?=\s*\|)/i,greedy:true},{pattern:/(\|\s*)(?:\\?\b[a-z_]\w*)+\b/i,alias:"class-name-fully-qualified",greedy:true,lookbehind:true,inside:{punctuation:/\\/}},{pattern:/(?:\\?\b[a-z_]\w*)+\b(?=\s*\|)/i,alias:"class-name-fully-qualified",greedy:true,inside:{punctuation:/\\/}},{pattern:/(\b(?:extends|implements|instanceof|new(?!\s+self\b|\s+static\b))\s+|\bcatch\s*\()(?:\\?\b[a-z_]\w*)+\b(?!\\)/i,alias:"class-name-fully-qualified",greedy:true,lookbehind:true,inside:{punctuation:/\\/}},{pattern:/\b[a-z_]\w*(?=\s*\$)/i,alias:"type-declaration",greedy:true},{pattern:/(?:\\?\b[a-z_]\w*)+(?=\s*\$)/i,alias:["class-name-fully-qualified","type-declaration"],greedy:true,inside:{punctuation:/\\/}},{pattern:/\b[a-z_]\w*(?=\s*::)/i,alias:"static-context",greedy:true},{pattern:/(?:\\?\b[a-z_]\w*)+(?=\s*::)/i,alias:["class-name-fully-qualified","static-context"],greedy:true,inside:{punctuation:/\\/}},{pattern:/([(,?]\s*)[a-z_]\w*(?=\s*\$)/i,alias:"type-hint",greedy:true,lookbehind:true},{pattern:/([(,?]\s*)(?:\\?\b[a-z_]\w*)+(?=\s*\$)/i,alias:["class-name-fully-qualified","type-hint"],greedy:true,lookbehind:true,inside:{punctuation:/\\/}},{pattern:/(\)\s*:\s*(?:\?\s*)?)\b[a-z_]\w*(?!\\)\b/i,alias:"return-type",greedy:true,lookbehind:true},{pattern:/(\)\s*:\s*(?:\?\s*)?)(?:\\?\b[a-z_]\w*)+\b(?!\\)/i,alias:["class-name-fully-qualified","return-type"],greedy:true,lookbehind:true,inside:{punctuation:/\\/}}],constant:e,function:{pattern:/(^|[^\\\w])\\?[a-z_](?:[\w\\]*\w)?(?=\s*\()/i,lookbehind:true,inside:{punctuation:/\\/}},property:{pattern:/(->\s*)\w+/,lookbehind:true},number:n,operator:u,punctuation:s};var r={pattern:/\{\$(?:\{(?:\{[^{}]+\}|[^{}]+)\}|[^{}])+\}|(^|[^\\{])\$+(?:\w+(?:\[[^\r\n\[\]]+\]|->\w+)?)/,lookbehind:true,inside:i.languages.php},a=[{pattern:/<<<'([^']+)'[\r\n](?:.*[\r\n])*?\1;/,alias:"nowdoc-string",greedy:true,inside:{delimiter:{pattern:/^<<<'[^']+'|[a-z_]\w*;$/i,alias:"symbol",inside:{punctuation:/^<<<'?|[';]$/}}}},{pattern:/<<<(?:"([^"]+)"[\r\n](?:.*[\r\n])*?\1;|([a-z_]\w*)[\r\n](?:.*[\r\n])*?\2;)/i,alias:"heredoc-string",greedy:true,inside:{delimiter:{pattern:/^<<<(?:"[^"]+"|[a-z_]\w*)|[a-z_]\w*;$/i,alias:"symbol",inside:{punctuation:/^<<<"?|[";]$/}},interpolation:r}},{pattern:/`(?:\\[\s\S]|[^\\`])*`/,alias:"backtick-quoted-string",greedy:true},{pattern:/'(?:\\[\s\S]|[^\\'])*'/,alias:"single-quoted-string",greedy:true},{pattern:/"(?:\\[\s\S]|[^\\"])*"/,alias:"double-quoted-string",greedy:true,inside:{interpolation:r}}];i.languages.insertBefore("php","variable",{string:a,attribute:{pattern:/#\[(?:[^"'\/#]|\/(?![*/])|\/\/.*$|#(?!\[).*$|\/\*(?:[^*]|\*(?!\/))*\*\/|"(?:\\[\s\S]|[^\\"])*"|'(?:\\[\s\S]|[^\\'])*')+\](?=\s*[a-z$#])/im,greedy:true,inside:{"attribute-content":{pattern:/^(#\[)[\s\S]+(?=\]$)/,lookbehind:true,inside:{comment:t,string:a,"attribute-class-name":[{pattern:/([^:]|^)\b[a-z_]\w*(?!\\)\b/i,alias:"class-name",greedy:true,lookbehind:true},{pattern:/([^:]|^)(?:\\?\b[a-z_]\w*)+/i,alias:["class-name","class-name-fully-qualified"],greedy:true,lookbehind:true,inside:{punctuation:/\\/}}],constant:e,number:n,operator:u,punctuation:s}},delimiter:{pattern:/^#\[|\]$/,alias:"punctuation"}}}}),i.hooks.add("before-tokenize",function(o){if(/<\?/.test(o.code)){var l=/<\?(?:[^"'/#]|\/(?![*/])|("|')(?:\\[\s\S]|(?!\1)[^\\])*\1|(?:\/\/|#(?!\[))(?:[^?\n\r]|\?(?!>))*(?=$|\?>|[\r\n])|#\[|\/\*(?:[^*]|\*(?!\/))*(?:\*\/|$))*?(?:\?>|$)/g;i.languages["markup-templating"].buildPlaceholders(o,"php",l);}}),i.hooks.add("after-tokenize",function(o){i.languages["markup-templating"].tokenizePlaceholders(o,"php");});})(Prism)),De$1}xt();(function(i){var t=/[*&][^\s[\]{},]+/,e=/!(?:<[\w\-%#;/?:@&=+$,.!~*'()[\]]+>|(?:[a-zA-Z\d-]*!)?[\w\-%#;/?:@&=+$.~*'()]+)?/,n="(?:"+e.source+"(?:[ 	]+"+t.source+")?|"+t.source+"(?:[ 	]+"+e.source+")?)",u=/(?:[^\s\x00-\x08\x0e-\x1f!"#%&'*,\-:>?@[\]`{|}\x7f-\x84\x86-\x9f\ud800-\udfff\ufffe\uffff]|[?:-]<PLAIN>)(?:[ \t]*(?:(?![#:])<PLAIN>|:<PLAIN>))*/.source.replace(/<PLAIN>/g,function(){return /[^\s\x00-\x08\x0e-\x1f,[\]{}\x7f-\x84\x86-\x9f\ud800-\udfff\ufffe\uffff]/.source}),s=/"(?:[^"\\\r\n]|\\.)*"|'(?:[^'\\\r\n]|\\.)*'/.source;function r(a,o){o=(o||"").replace(/m/g,"")+"m";var l=/([:\-,[{]\s*(?:\s<<prop>>[ \t]+)?)(?:<<value>>)(?=[ \t]*(?:$|,|\]|\}|(?:[\r\n]\s*)?#))/.source.replace(/<<prop>>/g,function(){return n}).replace(/<<value>>/g,function(){return a});return RegExp(l,o)}i.languages.yaml={scalar:{pattern:RegExp(/([\-:]\s*(?:\s<<prop>>[ \t]+)?[|>])[ \t]*(?:((?:\r?\n|\r)[ \t]+)\S[^\r\n]*(?:\2[^\r\n]+)*)/.source.replace(/<<prop>>/g,function(){return n})),lookbehind:true,alias:"string"},comment:/#.*/,key:{pattern:RegExp(/((?:^|[:\-,[{\r\n?])[ \t]*(?:<<prop>>[ \t]+)?)<<key>>(?=\s*:\s)/.source.replace(/<<prop>>/g,function(){return n}).replace(/<<key>>/g,function(){return "(?:"+u+"|"+s+")"})),lookbehind:true,greedy:true,alias:"atrule"},directive:{pattern:/(^[ \t]*)%.+/m,lookbehind:true,alias:"important"},datetime:{pattern:r(/\d{4}-\d\d?-\d\d?(?:[tT]|[ \t]+)\d\d?:\d{2}:\d{2}(?:\.\d*)?(?:[ \t]*(?:Z|[-+]\d\d?(?::\d{2})?))?|\d{4}-\d{2}-\d{2}|\d\d?:\d{2}(?::\d{2}(?:\.\d*)?)?/.source),lookbehind:true,alias:"number"},boolean:{pattern:r(/false|true/.source,"i"),lookbehind:true,alias:"important"},null:{pattern:r(/null|~/.source,"i"),lookbehind:true,alias:"important"},string:{pattern:r(s),lookbehind:true,greedy:true},number:{pattern:r(/[+-]?(?:0x[\da-f]+|0o[0-7]+|(?:\d+(?:\.\d*)?|\.\d+)(?:e[+-]?\d+)?|\.inf|\.nan)/.source,"i"),lookbehind:true},tag:e,important:t,punctuation:/---|[:[\]{}\-,|>?]|\.\.\./},i.languages.yml=i.languages.yaml;})(Prism);(function(i){function t(e,n){return "___"+e.toUpperCase()+n+"___"}Object.defineProperties(i.languages["markup-templating"]={},{buildPlaceholders:{value:function(e,n,u,s){if(e.language===n){var r=e.tokenStack=[];e.code=e.code.replace(u,function(a){if(typeof s=="function"&&!s(a))return a;for(var o=r.length,l;e.code.indexOf(l=t(n,o))!==-1;)++o;return r[o]=a,l}),e.grammar=i.languages.markup;}}},tokenizePlaceholders:{value:function(e,n){if(e.language!==n||!e.tokenStack)return;e.grammar=i.languages[n];var u=0,s=Object.keys(e.tokenStack);function r(a){for(var o=0;o<a.length&&!(u>=s.length);o++){var l=a[o];if(typeof l=="string"||l.content&&typeof l.content=="string"){var c=s[u],D=e.tokenStack[c],p=typeof l=="string"?l:l.content,d=t(n,c),F=p.indexOf(d);if(F>-1){++u;var f=p.substring(0,F),m=new i.Token(n,i.tokenize(D,e.grammar),"language-"+n,D),x=p.substring(F+d.length),b=[];f&&b.push.apply(b,r([f])),b.push(m),x&&b.push.apply(b,r([x])),typeof l=="string"?a.splice.apply(a,[o,1].concat(b)):l.content=b;}}else l.content&&r(l.content);}return a}r(e.tokens);}}});})(Prism);const Tt$1='<svg class="md-link-icon" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="m7.775 3.275 1.25-1.25a3.5 3.5 0 1 1 4.95 4.95l-2.5 2.5a3.5 3.5 0 0 1-4.95 0 .751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018 1.998 1.998 0 0 0 2.83 0l2.5-2.5a2.002 2.002 0 0 0-2.83-2.83l-1.25 1.25a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042Zm-4.69 9.64a1.998 1.998 0 0 0 2.83 0l1.25-1.25a.751.751 0 0 1 1.042.018.751.751 0 0 1 .018 1.042l-1.25 1.25a3.5 3.5 0 1 1-4.95-4.95l2.5-2.5a3.5 3.5 0 0 1 4.95 0 .751.751 0 0 1-.018 1.042.751.751 0 0 1-1.042.018 1.998 1.998 0 0 0-2.83 0l-2.5 2.5a1.998 1.998 0 0 0 0 2.83Z"></path></svg>',St=`
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 15 15" color="currentColor" aria-hidden="true" aria-label="Copy" stroke-width="1.3" width="15" height="15">
  <path fill="currentColor" d="M12.728 4.545v8.182H4.545V4.545zm0 -0.909H4.545a0.909 0.909 0 0 0 -0.909 0.909v8.182a0.909 0.909 0 0 0 0.909 0.909h8.182a0.909 0.909 0 0 0 0.909 -0.909V4.545a0.909 0.909 0 0 0 -0.909 -0.909"/>
  <path fill="currentColor" d="M1.818 8.182H0.909V1.818a0.909 0.909 0 0 1 0.909 -0.909h6.364v0.909H1.818Z"/>
</svg>

`,Bt$1=`<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 17 17" aria-hidden="true" aria-label="Copied" fill="none" stroke="currentColor" stroke-width="1.3">
  <path d="m13.813 4.781 -7.438 7.438 -3.188 -3.188"/>
</svg>
`,he$1=`<button title="copy" class="copy_code_button">
  <span class="copy-text">${St}</span>
  <span class="check">${Bt$1}</span>
</button>`,Re$1=/[&<>"']/,yt=new RegExp(Re$1.source,"g"),Ie$1=/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,_t=new RegExp(Ie$1.source,"g"),Rt$1={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"},ge$1=i=>Rt$1[i]||"";function P$3(i,t){if(t){if(Re$1.test(i))return i.replace(yt,ge$1)}else if(Ie$1.test(i))return i.replace(_t,ge$1);return i}function It$1(i){const t=i.map(e=>({start:new RegExp(e.left.replace(/[-\/\\^$*+?.()|[\]{}]/g,"\\$&")),end:new RegExp(e.right.replace(/[-\/\\^$*+?.()|[\]{}]/g,"\\$&"))}));return {name:"latex",level:"block",start(e){for(const n of t){const u=e.match(n.start);if(u)return u.index}return  -1},tokenizer(e,n){for(const u of t){const s=new RegExp(`${u.start.source}([\\s\\S]+?)${u.end.source}`).exec(e);if(s)return {type:"latex",raw:s[0],text:s[1].trim()}}},renderer(e){return `<div class="latex-block">${e.text}</div>`}}}function Nt$1(){return {name:"mermaid",level:"block",start(i){return i.match(/^```mermaid\s*\n/)?.index},tokenizer(i){const t=/^```mermaid\s*\n([\s\S]*?)```\s*(?:\n|$)/.exec(i);if(t)return {type:"mermaid",raw:t[0],text:t[1].trim()}},renderer(i){return `<div class="mermaid">${i.text}</div>
`}}}const Ot$1={code(i,t,e){const n=(t??"").match(/\S*/)?.[0]??"";return i=i.replace(/\n$/,"")+`
`,!n||n==="mermaid"?'<div class="code_wrap">'+he$1+"<pre><code>"+(e?i:P$3(i,true))+`</code></pre></div>
`:'<div class="code_wrap">'+he$1+'<pre><code class="language-'+P$3(n)+'">'+(e?i:P$3(i,true))+`</code></pre></div>
`}},Lt=new K$1;function vt({header_links:i,line_breaks:t,latex_delimiters:e}){const n=new Te;n.use({gfm:true,pedantic:false,breaks:t},dt({highlight:(r,a)=>ne$2.languages?.[a]?ne$2.highlight(r,ne$2.languages[a],a):r}),{renderer:Ot$1}),i&&(n.use(At$1()),n.use({extensions:[{name:"heading",level:"block",renderer(r){const a=r.raw.toLowerCase().trim().replace(/<[!\/a-z].*?>/gi,""),o="h"+Lt.slug(a),l=r.depth,c=this.parser.parseInline(r.tokens);return `<h${l} id="${o}"><a class="md-header-anchor" href="#${o}">${Tt$1}</a>${c}</h${l}>
`}}]}));const u=Nt$1(),s=It$1(e);return n.use({extensions:[u,s]}),n}

const l="GRADIO_ROOT";let d$1 = class d extends Error{constructor(t){super(t),this.name="ShareError";}};async function w$1(s,t){if(window.__gradio_space__==null)throw new d$1("Must be on Spaces to share.");let e,r,n;{let i;if(typeof s=="object"&&s.url)i=s.url;else if(typeof s=="string")i=s;else throw new Error("Invalid data format for URL type");const p=await fetch(i);e=await p.blob(),r=p.headers.get("content-type")||"",n=p.headers.get("content-disposition")||"";}const o=new File([e],n,{type:r}),a=await fetch("https://huggingface.co/uploads",{method:"POST",body:o,headers:{"Content-Type":o.type,"X-Requested-With":"XMLHttpRequest"}});if(!a.ok){if(a.headers.get("content-type")?.includes("application/json")){const i=await a.json();throw new d$1(`Upload failed: ${i.error}`)}throw new d$1("Upload failed.")}return await a.text()}const y$2=s=>{const t=Math.floor(s/3600),e=Math.floor(s%3600/60),r=Math.round(s)%60,n=`${e<10?"0":""}${e}`,o=`${r<10?"0":""}${r}`;return t>0?`${t}:${n}:${o}`:`${e}:${o}`},_$1=typeof window<"u",f$2=["elem_id","elem_classes","visible","interactive","server_fns","server","id","target","theme_mode","version","root","autoscroll","max_file_size","formatter","client","load_component","scale","min_width","theme","padding","loading_status","label","show_label","validation_error","show_progress","api_prefix","container","attached_events"];let g$2 = class g{load_component;shared={};props={};i18n={};dispatcher;last_update=null;shared_props=f$2;constructor(t,e){for(const o in t.shared_props)this.shared[o]=t.shared_props[o];for(const o in t.props)this.props[o]=t.props[o];if(e)for(const o in e)this.props[o]===void 0&&(this.props[o]=e[o]);if(this.i18n=this.props.i18n,this.load_component=this.shared.load_component,!_$1||t.props?.__GRADIO_BROWSER_TEST__){this.dispatcher=()=>{};return}const{register:r,dispatcher:n}=getContext(l);r(t.shared_props.id,this.set_data.bind(this),this.get_data.bind(this)),this.dispatcher=n;}dispatch(t,e){this.dispatcher(this.shared.id,t,e);}async get_data(){return snapshot(this.props)}update(t){this.set_data(t);}set_data(t){for(const e in t)if(this.shared_props.includes(e)){const r=e;this.shared[r]=t[r];continue}else this.props[e]=t[e];}};const b$1=s=>typeof s=="number"?s+"px":s;

function getDefaultExportFromCjs (x) {
	return x && x.__esModule && Object.prototype.hasOwnProperty.call(x, 'default') ? x['default'] : x;
}

var picocolors = {exports: {}};

var hasRequiredPicocolors;

function requirePicocolors () {
	if (hasRequiredPicocolors) return picocolors.exports;
	hasRequiredPicocolors = 1;
	let p = process || {}, argv = p.argv || [], env = p.env || {};
	let isColorSupported =
		!(!!env.NO_COLOR || argv.includes("--no-color")) &&
		(!!env.FORCE_COLOR || argv.includes("--color") || p.platform === "win32" || ((p.stdout || {}).isTTY && env.TERM !== "dumb") || !!env.CI);

	let formatter = (open, close, replace = open) =>
		input => {
			let string = "" + input, index = string.indexOf(close, open.length);
			return ~index ? open + replaceClose(string, close, replace, index) + close : open + string + close
		};

	let replaceClose = (string, close, replace, index) => {
		let result = "", cursor = 0;
		do {
			result += string.substring(cursor, index) + replace;
			cursor = index + close.length;
			index = string.indexOf(close, cursor);
		} while (~index)
		return result + string.substring(cursor)
	};

	let createColors = (enabled = isColorSupported) => {
		let f = enabled ? formatter : () => String;
		return {
			isColorSupported: enabled,
			reset: f("\x1b[0m", "\x1b[0m"),
			bold: f("\x1b[1m", "\x1b[22m", "\x1b[22m\x1b[1m"),
			dim: f("\x1b[2m", "\x1b[22m", "\x1b[22m\x1b[2m"),
			italic: f("\x1b[3m", "\x1b[23m"),
			underline: f("\x1b[4m", "\x1b[24m"),
			inverse: f("\x1b[7m", "\x1b[27m"),
			hidden: f("\x1b[8m", "\x1b[28m"),
			strikethrough: f("\x1b[9m", "\x1b[29m"),

			black: f("\x1b[30m", "\x1b[39m"),
			red: f("\x1b[31m", "\x1b[39m"),
			green: f("\x1b[32m", "\x1b[39m"),
			yellow: f("\x1b[33m", "\x1b[39m"),
			blue: f("\x1b[34m", "\x1b[39m"),
			magenta: f("\x1b[35m", "\x1b[39m"),
			cyan: f("\x1b[36m", "\x1b[39m"),
			white: f("\x1b[37m", "\x1b[39m"),
			gray: f("\x1b[90m", "\x1b[39m"),

			bgBlack: f("\x1b[40m", "\x1b[49m"),
			bgRed: f("\x1b[41m", "\x1b[49m"),
			bgGreen: f("\x1b[42m", "\x1b[49m"),
			bgYellow: f("\x1b[43m", "\x1b[49m"),
			bgBlue: f("\x1b[44m", "\x1b[49m"),
			bgMagenta: f("\x1b[45m", "\x1b[49m"),
			bgCyan: f("\x1b[46m", "\x1b[49m"),
			bgWhite: f("\x1b[47m", "\x1b[49m"),

			blackBright: f("\x1b[90m", "\x1b[39m"),
			redBright: f("\x1b[91m", "\x1b[39m"),
			greenBright: f("\x1b[92m", "\x1b[39m"),
			yellowBright: f("\x1b[93m", "\x1b[39m"),
			blueBright: f("\x1b[94m", "\x1b[39m"),
			magentaBright: f("\x1b[95m", "\x1b[39m"),
			cyanBright: f("\x1b[96m", "\x1b[39m"),
			whiteBright: f("\x1b[97m", "\x1b[39m"),

			bgBlackBright: f("\x1b[100m", "\x1b[49m"),
			bgRedBright: f("\x1b[101m", "\x1b[49m"),
			bgGreenBright: f("\x1b[102m", "\x1b[49m"),
			bgYellowBright: f("\x1b[103m", "\x1b[49m"),
			bgBlueBright: f("\x1b[104m", "\x1b[49m"),
			bgMagentaBright: f("\x1b[105m", "\x1b[49m"),
			bgCyanBright: f("\x1b[106m", "\x1b[49m"),
			bgWhiteBright: f("\x1b[107m", "\x1b[49m"),
		}
	};

	picocolors.exports = createColors();
	picocolors.exports.createColors = createColors;
	return picocolors.exports;
}

var tokenize;
var hasRequiredTokenize;

function requireTokenize () {
	if (hasRequiredTokenize) return tokenize;
	hasRequiredTokenize = 1;

	const SINGLE_QUOTE = "'".charCodeAt(0);
	const DOUBLE_QUOTE = '"'.charCodeAt(0);
	const BACKSLASH = '\\'.charCodeAt(0);
	const SLASH = '/'.charCodeAt(0);
	const NEWLINE = '\n'.charCodeAt(0);
	const SPACE = ' '.charCodeAt(0);
	const FEED = '\f'.charCodeAt(0);
	const TAB = '\t'.charCodeAt(0);
	const CR = '\r'.charCodeAt(0);
	const OPEN_SQUARE = '['.charCodeAt(0);
	const CLOSE_SQUARE = ']'.charCodeAt(0);
	const OPEN_PARENTHESES = '('.charCodeAt(0);
	const CLOSE_PARENTHESES = ')'.charCodeAt(0);
	const OPEN_CURLY = '{'.charCodeAt(0);
	const CLOSE_CURLY = '}'.charCodeAt(0);
	const SEMICOLON = ';'.charCodeAt(0);
	const ASTERISK = '*'.charCodeAt(0);
	const COLON = ':'.charCodeAt(0);
	const AT = '@'.charCodeAt(0);

	const RE_AT_END = /[\t\n\f\r "#'()/;[\\\]{}]/g;
	const RE_WORD_END = /[\t\n\f\r !"#'():;@[\\\]{}]|\/(?=\*)/g;
	const RE_BAD_BRACKET = /.[\r\n"'(/\\]/;
	const RE_HEX_ESCAPE = /[\da-f]/i;

	tokenize = function tokenizer(input, options = {}) {
	  let css = input.css.valueOf();
	  let ignore = options.ignoreErrors;

	  let code, content, escape, next, quote;
	  let currentToken, escaped, escapePos, n, prev;

	  let length = css.length;
	  let pos = 0;
	  let buffer = [];
	  let returned = [];

	  function position() {
	    return pos
	  }

	  function unclosed(what) {
	    throw input.error('Unclosed ' + what, pos)
	  }

	  function endOfFile() {
	    return returned.length === 0 && pos >= length
	  }

	  function nextToken(opts) {
	    if (returned.length) return returned.pop()
	    if (pos >= length) return

	    let ignoreUnclosed = opts ? opts.ignoreUnclosed : false;

	    code = css.charCodeAt(pos);

	    switch (code) {
	      case NEWLINE:
	      case SPACE:
	      case TAB:
	      case CR:
	      case FEED: {
	        next = pos;
	        do {
	          next += 1;
	          code = css.charCodeAt(next);
	        } while (
	          code === SPACE ||
	          code === NEWLINE ||
	          code === TAB ||
	          code === CR ||
	          code === FEED
	        )

	        currentToken = ['space', css.slice(pos, next)];
	        pos = next - 1;
	        break
	      }

	      case OPEN_SQUARE:
	      case CLOSE_SQUARE:
	      case OPEN_CURLY:
	      case CLOSE_CURLY:
	      case COLON:
	      case SEMICOLON:
	      case CLOSE_PARENTHESES: {
	        let controlChar = String.fromCharCode(code);
	        currentToken = [controlChar, controlChar, pos];
	        break
	      }

	      case OPEN_PARENTHESES: {
	        prev = buffer.length ? buffer.pop()[1] : '';
	        n = css.charCodeAt(pos + 1);
	        if (
	          prev === 'url' &&
	          n !== SINGLE_QUOTE &&
	          n !== DOUBLE_QUOTE &&
	          n !== SPACE &&
	          n !== NEWLINE &&
	          n !== TAB &&
	          n !== FEED &&
	          n !== CR
	        ) {
	          next = pos;
	          do {
	            escaped = false;
	            next = css.indexOf(')', next + 1);
	            if (next === -1) {
	              if (ignore || ignoreUnclosed) {
	                next = pos;
	                break
	              } else {
	                unclosed('bracket');
	              }
	            }
	            escapePos = next;
	            while (css.charCodeAt(escapePos - 1) === BACKSLASH) {
	              escapePos -= 1;
	              escaped = !escaped;
	            }
	          } while (escaped)

	          currentToken = ['brackets', css.slice(pos, next + 1), pos, next];

	          pos = next;
	        } else {
	          next = css.indexOf(')', pos + 1);
	          content = css.slice(pos, next + 1);

	          if (next === -1 || RE_BAD_BRACKET.test(content)) {
	            currentToken = ['(', '(', pos];
	          } else {
	            currentToken = ['brackets', content, pos, next];
	            pos = next;
	          }
	        }

	        break
	      }

	      case SINGLE_QUOTE:
	      case DOUBLE_QUOTE: {
	        quote = code === SINGLE_QUOTE ? "'" : '"';
	        next = pos;
	        do {
	          escaped = false;
	          next = css.indexOf(quote, next + 1);
	          if (next === -1) {
	            if (ignore || ignoreUnclosed) {
	              next = pos + 1;
	              break
	            } else {
	              unclosed('string');
	            }
	          }
	          escapePos = next;
	          while (css.charCodeAt(escapePos - 1) === BACKSLASH) {
	            escapePos -= 1;
	            escaped = !escaped;
	          }
	        } while (escaped)

	        currentToken = ['string', css.slice(pos, next + 1), pos, next];
	        pos = next;
	        break
	      }

	      case AT: {
	        RE_AT_END.lastIndex = pos + 1;
	        RE_AT_END.test(css);
	        if (RE_AT_END.lastIndex === 0) {
	          next = css.length - 1;
	        } else {
	          next = RE_AT_END.lastIndex - 2;
	        }

	        currentToken = ['at-word', css.slice(pos, next + 1), pos, next];

	        pos = next;
	        break
	      }

	      case BACKSLASH: {
	        next = pos;
	        escape = true;
	        while (css.charCodeAt(next + 1) === BACKSLASH) {
	          next += 1;
	          escape = !escape;
	        }
	        code = css.charCodeAt(next + 1);
	        if (
	          escape &&
	          code !== SLASH &&
	          code !== SPACE &&
	          code !== NEWLINE &&
	          code !== TAB &&
	          code !== CR &&
	          code !== FEED
	        ) {
	          next += 1;
	          if (RE_HEX_ESCAPE.test(css.charAt(next))) {
	            while (RE_HEX_ESCAPE.test(css.charAt(next + 1))) {
	              next += 1;
	            }
	            if (css.charCodeAt(next + 1) === SPACE) {
	              next += 1;
	            }
	          }
	        }

	        currentToken = ['word', css.slice(pos, next + 1), pos, next];

	        pos = next;
	        break
	      }

	      default: {
	        if (code === SLASH && css.charCodeAt(pos + 1) === ASTERISK) {
	          next = css.indexOf('*/', pos + 2) + 1;
	          if (next === 0) {
	            if (ignore || ignoreUnclosed) {
	              next = css.length;
	            } else {
	              unclosed('comment');
	            }
	          }

	          currentToken = ['comment', css.slice(pos, next + 1), pos, next];
	          pos = next;
	        } else {
	          RE_WORD_END.lastIndex = pos + 1;
	          RE_WORD_END.test(css);
	          if (RE_WORD_END.lastIndex === 0) {
	            next = css.length - 1;
	          } else {
	            next = RE_WORD_END.lastIndex - 2;
	          }

	          currentToken = ['word', css.slice(pos, next + 1), pos, next];
	          buffer.push(currentToken);
	          pos = next;
	        }

	        break
	      }
	    }

	    pos++;
	    return currentToken
	  }

	  function back(token) {
	    returned.push(token);
	  }

	  return {
	    back,
	    endOfFile,
	    nextToken,
	    position
	  }
	};
	return tokenize;
}

var terminalHighlight_1;
var hasRequiredTerminalHighlight;

function requireTerminalHighlight () {
	if (hasRequiredTerminalHighlight) return terminalHighlight_1;
	hasRequiredTerminalHighlight = 1;

	let pico = /*@__PURE__*/ requirePicocolors();

	let tokenizer = requireTokenize();

	let Input;

	function registerInput(dependant) {
	  Input = dependant;
	}

	const HIGHLIGHT_THEME = {
	  ';': pico.yellow,
	  ':': pico.yellow,
	  '(': pico.cyan,
	  ')': pico.cyan,
	  '[': pico.yellow,
	  ']': pico.yellow,
	  '{': pico.yellow,
	  '}': pico.yellow,
	  'at-word': pico.cyan,
	  'brackets': pico.cyan,
	  'call': pico.cyan,
	  'class': pico.yellow,
	  'comment': pico.gray,
	  'hash': pico.magenta,
	  'string': pico.green
	};

	function getTokenType([type, value], processor) {
	  if (type === 'word') {
	    if (value[0] === '.') {
	      return 'class'
	    }
	    if (value[0] === '#') {
	      return 'hash'
	    }
	  }

	  if (!processor.endOfFile()) {
	    let next = processor.nextToken();
	    processor.back(next);
	    if (next[0] === 'brackets' || next[0] === '(') return 'call'
	  }

	  return type
	}

	function terminalHighlight(css) {
	  let processor = tokenizer(new Input(css), { ignoreErrors: true });
	  let result = '';
	  while (!processor.endOfFile()) {
	    let token = processor.nextToken();
	    let color = HIGHLIGHT_THEME[getTokenType(token, processor)];
	    if (color) {
	      result += token[1]
	        .split(/\r?\n/)
	        .map(i => color(i))
	        .join('\n');
	    } else {
	      result += token[1];
	    }
	  }
	  return result
	}

	terminalHighlight.registerInput = registerInput;

	terminalHighlight_1 = terminalHighlight;
	return terminalHighlight_1;
}

var cssSyntaxError;
var hasRequiredCssSyntaxError;

function requireCssSyntaxError () {
	if (hasRequiredCssSyntaxError) return cssSyntaxError;
	hasRequiredCssSyntaxError = 1;

	let pico = /*@__PURE__*/ requirePicocolors();

	let terminalHighlight = requireTerminalHighlight();

	class CssSyntaxError extends Error {
	  constructor(message, line, column, source, file, plugin) {
	    super(message);
	    this.name = 'CssSyntaxError';
	    this.reason = message;

	    if (file) {
	      this.file = file;
	    }
	    if (source) {
	      this.source = source;
	    }
	    if (plugin) {
	      this.plugin = plugin;
	    }
	    if (typeof line !== 'undefined' && typeof column !== 'undefined') {
	      if (typeof line === 'number') {
	        this.line = line;
	        this.column = column;
	      } else {
	        this.line = line.line;
	        this.column = line.column;
	        this.endLine = column.line;
	        this.endColumn = column.column;
	      }
	    }

	    this.setMessage();

	    if (Error.captureStackTrace) {
	      Error.captureStackTrace(this, CssSyntaxError);
	    }
	  }

	  setMessage() {
	    this.message = this.plugin ? this.plugin + ': ' : '';
	    this.message += this.file ? this.file : '<css input>';
	    if (typeof this.line !== 'undefined') {
	      this.message += ':' + this.line + ':' + this.column;
	    }
	    this.message += ': ' + this.reason;
	  }

	  showSourceCode(color) {
	    if (!this.source) return ''

	    let css = this.source;
	    if (color == null) color = pico.isColorSupported;

	    let aside = text => text;
	    let mark = text => text;
	    let highlight = text => text;
	    if (color) {
	      let { bold, gray, red } = pico.createColors(true);
	      mark = text => bold(red(text));
	      aside = text => gray(text);
	      if (terminalHighlight) {
	        highlight = text => terminalHighlight(text);
	      }
	    }

	    let lines = css.split(/\r?\n/);
	    let start = Math.max(this.line - 3, 0);
	    let end = Math.min(this.line + 2, lines.length);
	    let maxWidth = String(end).length;

	    return lines
	      .slice(start, end)
	      .map((line, index) => {
	        let number = start + 1 + index;
	        let gutter = ' ' + (' ' + number).slice(-maxWidth) + ' | ';
	        if (number === this.line) {
	          if (line.length > 160) {
	            let padding = 20;
	            let subLineStart = Math.max(0, this.column - padding);
	            let subLineEnd = Math.max(
	              this.column + padding,
	              this.endColumn + padding
	            );
	            let subLine = line.slice(subLineStart, subLineEnd);

	            let spacing =
	              aside(gutter.replace(/\d/g, ' ')) +
	              line
	                .slice(0, Math.min(this.column - 1, padding - 1))
	                .replace(/[^\t]/g, ' ');

	            return (
	              mark('>') +
	              aside(gutter) +
	              highlight(subLine) +
	              '\n ' +
	              spacing +
	              mark('^')
	            )
	          }

	          let spacing =
	            aside(gutter.replace(/\d/g, ' ')) +
	            line.slice(0, this.column - 1).replace(/[^\t]/g, ' ');

	          return (
	            mark('>') +
	            aside(gutter) +
	            highlight(line) +
	            '\n ' +
	            spacing +
	            mark('^')
	          )
	        }

	        return ' ' + aside(gutter) + highlight(line)
	      })
	      .join('\n')
	  }

	  toString() {
	    let code = this.showSourceCode();
	    if (code) {
	      code = '\n\n' + code + '\n';
	    }
	    return this.name + ': ' + this.message + code
	  }
	}

	cssSyntaxError = CssSyntaxError;
	CssSyntaxError.default = CssSyntaxError;
	return cssSyntaxError;
}

var stringifier;
var hasRequiredStringifier;

function requireStringifier () {
	if (hasRequiredStringifier) return stringifier;
	hasRequiredStringifier = 1;

	const DEFAULT_RAW = {
	  after: '\n',
	  beforeClose: '\n',
	  beforeComment: '\n',
	  beforeDecl: '\n',
	  beforeOpen: ' ',
	  beforeRule: '\n',
	  colon: ': ',
	  commentLeft: ' ',
	  commentRight: ' ',
	  emptyBody: '',
	  indent: '    ',
	  semicolon: false
	};

	function capitalize(str) {
	  return str[0].toUpperCase() + str.slice(1)
	}

	class Stringifier {
	  constructor(builder) {
	    this.builder = builder;
	  }

	  atrule(node, semicolon) {
	    let name = '@' + node.name;
	    let params = node.params ? this.rawValue(node, 'params') : '';

	    if (typeof node.raws.afterName !== 'undefined') {
	      name += node.raws.afterName;
	    } else if (params) {
	      name += ' ';
	    }

	    if (node.nodes) {
	      this.block(node, name + params);
	    } else {
	      let end = (node.raws.between || '') + (semicolon ? ';' : '');
	      this.builder(name + params + end, node);
	    }
	  }

	  beforeAfter(node, detect) {
	    let value;
	    if (node.type === 'decl') {
	      value = this.raw(node, null, 'beforeDecl');
	    } else if (node.type === 'comment') {
	      value = this.raw(node, null, 'beforeComment');
	    } else if (detect === 'before') {
	      value = this.raw(node, null, 'beforeRule');
	    } else {
	      value = this.raw(node, null, 'beforeClose');
	    }

	    let buf = node.parent;
	    let depth = 0;
	    while (buf && buf.type !== 'root') {
	      depth += 1;
	      buf = buf.parent;
	    }

	    if (value.includes('\n')) {
	      let indent = this.raw(node, null, 'indent');
	      if (indent.length) {
	        for (let step = 0; step < depth; step++) value += indent;
	      }
	    }

	    return value
	  }

	  block(node, start) {
	    let between = this.raw(node, 'between', 'beforeOpen');
	    this.builder(start + between + '{', node, 'start');

	    let after;
	    if (node.nodes && node.nodes.length) {
	      this.body(node);
	      after = this.raw(node, 'after');
	    } else {
	      after = this.raw(node, 'after', 'emptyBody');
	    }

	    if (after) this.builder(after);
	    this.builder('}', node, 'end');
	  }

	  body(node) {
	    let last = node.nodes.length - 1;
	    while (last > 0) {
	      if (node.nodes[last].type !== 'comment') break
	      last -= 1;
	    }

	    let semicolon = this.raw(node, 'semicolon');
	    for (let i = 0; i < node.nodes.length; i++) {
	      let child = node.nodes[i];
	      let before = this.raw(child, 'before');
	      if (before) this.builder(before);
	      this.stringify(child, last !== i || semicolon);
	    }
	  }

	  comment(node) {
	    let left = this.raw(node, 'left', 'commentLeft');
	    let right = this.raw(node, 'right', 'commentRight');
	    this.builder('/*' + left + node.text + right + '*/', node);
	  }

	  decl(node, semicolon) {
	    let between = this.raw(node, 'between', 'colon');
	    let string = node.prop + between + this.rawValue(node, 'value');

	    if (node.important) {
	      string += node.raws.important || ' !important';
	    }

	    if (semicolon) string += ';';
	    this.builder(string, node);
	  }

	  document(node) {
	    this.body(node);
	  }

	  raw(node, own, detect) {
	    let value;
	    if (!detect) detect = own;

	    // Already had
	    if (own) {
	      value = node.raws[own];
	      if (typeof value !== 'undefined') return value
	    }

	    let parent = node.parent;

	    if (detect === 'before') {
	      // Hack for first rule in CSS
	      if (!parent || (parent.type === 'root' && parent.first === node)) {
	        return ''
	      }

	      // `root` nodes in `document` should use only their own raws
	      if (parent && parent.type === 'document') {
	        return ''
	      }
	    }

	    // Floating child without parent
	    if (!parent) return DEFAULT_RAW[detect]

	    // Detect style by other nodes
	    let root = node.root();
	    if (!root.rawCache) root.rawCache = {};
	    if (typeof root.rawCache[detect] !== 'undefined') {
	      return root.rawCache[detect]
	    }

	    if (detect === 'before' || detect === 'after') {
	      return this.beforeAfter(node, detect)
	    } else {
	      let method = 'raw' + capitalize(detect);
	      if (this[method]) {
	        value = this[method](root, node);
	      } else {
	        root.walk(i => {
	          value = i.raws[own];
	          if (typeof value !== 'undefined') return false
	        });
	      }
	    }

	    if (typeof value === 'undefined') value = DEFAULT_RAW[detect];

	    root.rawCache[detect] = value;
	    return value
	  }

	  rawBeforeClose(root) {
	    let value;
	    root.walk(i => {
	      if (i.nodes && i.nodes.length > 0) {
	        if (typeof i.raws.after !== 'undefined') {
	          value = i.raws.after;
	          if (value.includes('\n')) {
	            value = value.replace(/[^\n]+$/, '');
	          }
	          return false
	        }
	      }
	    });
	    if (value) value = value.replace(/\S/g, '');
	    return value
	  }

	  rawBeforeComment(root, node) {
	    let value;
	    root.walkComments(i => {
	      if (typeof i.raws.before !== 'undefined') {
	        value = i.raws.before;
	        if (value.includes('\n')) {
	          value = value.replace(/[^\n]+$/, '');
	        }
	        return false
	      }
	    });
	    if (typeof value === 'undefined') {
	      value = this.raw(node, null, 'beforeDecl');
	    } else if (value) {
	      value = value.replace(/\S/g, '');
	    }
	    return value
	  }

	  rawBeforeDecl(root, node) {
	    let value;
	    root.walkDecls(i => {
	      if (typeof i.raws.before !== 'undefined') {
	        value = i.raws.before;
	        if (value.includes('\n')) {
	          value = value.replace(/[^\n]+$/, '');
	        }
	        return false
	      }
	    });
	    if (typeof value === 'undefined') {
	      value = this.raw(node, null, 'beforeRule');
	    } else if (value) {
	      value = value.replace(/\S/g, '');
	    }
	    return value
	  }

	  rawBeforeOpen(root) {
	    let value;
	    root.walk(i => {
	      if (i.type !== 'decl') {
	        value = i.raws.between;
	        if (typeof value !== 'undefined') return false
	      }
	    });
	    return value
	  }

	  rawBeforeRule(root) {
	    let value;
	    root.walk(i => {
	      if (i.nodes && (i.parent !== root || root.first !== i)) {
	        if (typeof i.raws.before !== 'undefined') {
	          value = i.raws.before;
	          if (value.includes('\n')) {
	            value = value.replace(/[^\n]+$/, '');
	          }
	          return false
	        }
	      }
	    });
	    if (value) value = value.replace(/\S/g, '');
	    return value
	  }

	  rawColon(root) {
	    let value;
	    root.walkDecls(i => {
	      if (typeof i.raws.between !== 'undefined') {
	        value = i.raws.between.replace(/[^\s:]/g, '');
	        return false
	      }
	    });
	    return value
	  }

	  rawEmptyBody(root) {
	    let value;
	    root.walk(i => {
	      if (i.nodes && i.nodes.length === 0) {
	        value = i.raws.after;
	        if (typeof value !== 'undefined') return false
	      }
	    });
	    return value
	  }

	  rawIndent(root) {
	    if (root.raws.indent) return root.raws.indent
	    let value;
	    root.walk(i => {
	      let p = i.parent;
	      if (p && p !== root && p.parent && p.parent === root) {
	        if (typeof i.raws.before !== 'undefined') {
	          let parts = i.raws.before.split('\n');
	          value = parts[parts.length - 1];
	          value = value.replace(/\S/g, '');
	          return false
	        }
	      }
	    });
	    return value
	  }

	  rawSemicolon(root) {
	    let value;
	    root.walk(i => {
	      if (i.nodes && i.nodes.length && i.last.type === 'decl') {
	        value = i.raws.semicolon;
	        if (typeof value !== 'undefined') return false
	      }
	    });
	    return value
	  }

	  rawValue(node, prop) {
	    let value = node[prop];
	    let raw = node.raws[prop];
	    if (raw && raw.value === value) {
	      return raw.raw
	    }

	    return value
	  }

	  root(node) {
	    this.body(node);
	    if (node.raws.after) this.builder(node.raws.after);
	  }

	  rule(node) {
	    this.block(node, this.rawValue(node, 'selector'));
	    if (node.raws.ownSemicolon) {
	      this.builder(node.raws.ownSemicolon, node, 'end');
	    }
	  }

	  stringify(node, semicolon) {
	    /* c8 ignore start */
	    if (!this[node.type]) {
	      throw new Error(
	        'Unknown AST node type ' +
	          node.type +
	          '. ' +
	          'Maybe you need to change PostCSS stringifier.'
	      )
	    }
	    /* c8 ignore stop */
	    this[node.type](node, semicolon);
	  }
	}

	stringifier = Stringifier;
	Stringifier.default = Stringifier;
	return stringifier;
}

var stringify_1;
var hasRequiredStringify;

function requireStringify () {
	if (hasRequiredStringify) return stringify_1;
	hasRequiredStringify = 1;

	let Stringifier = requireStringifier();

	function stringify(node, builder) {
	  let str = new Stringifier(builder);
	  str.stringify(node);
	}

	stringify_1 = stringify;
	stringify.default = stringify;
	return stringify_1;
}

var symbols = {};

var hasRequiredSymbols;

function requireSymbols () {
	if (hasRequiredSymbols) return symbols;
	hasRequiredSymbols = 1;

	symbols.isClean = Symbol('isClean');

	symbols.my = Symbol('my');
	return symbols;
}

var node;
var hasRequiredNode;

function requireNode () {
	if (hasRequiredNode) return node;
	hasRequiredNode = 1;

	let CssSyntaxError = requireCssSyntaxError();
	let Stringifier = requireStringifier();
	let stringify = requireStringify();
	let { isClean, my } = requireSymbols();

	function cloneNode(obj, parent) {
	  let cloned = new obj.constructor();

	  for (let i in obj) {
	    if (!Object.prototype.hasOwnProperty.call(obj, i)) {
	      /* c8 ignore next 2 */
	      continue
	    }
	    if (i === 'proxyCache') continue
	    let value = obj[i];
	    let type = typeof value;

	    if (i === 'parent' && type === 'object') {
	      if (parent) cloned[i] = parent;
	    } else if (i === 'source') {
	      cloned[i] = value;
	    } else if (Array.isArray(value)) {
	      cloned[i] = value.map(j => cloneNode(j, cloned));
	    } else {
	      if (type === 'object' && value !== null) value = cloneNode(value);
	      cloned[i] = value;
	    }
	  }

	  return cloned
	}

	function sourceOffset(inputCSS, position) {
	  // Not all custom syntaxes support `offset` in `source.start` and `source.end`
	  if (position && typeof position.offset !== 'undefined') {
	    return position.offset
	  }

	  let column = 1;
	  let line = 1;
	  let offset = 0;

	  for (let i = 0; i < inputCSS.length; i++) {
	    if (line === position.line && column === position.column) {
	      offset = i;
	      break
	    }

	    if (inputCSS[i] === '\n') {
	      column = 1;
	      line += 1;
	    } else {
	      column += 1;
	    }
	  }

	  return offset
	}

	class Node {
	  get proxyOf() {
	    return this
	  }

	  constructor(defaults = {}) {
	    this.raws = {};
	    this[isClean] = false;
	    this[my] = true;

	    for (let name in defaults) {
	      if (name === 'nodes') {
	        this.nodes = [];
	        for (let node of defaults[name]) {
	          if (typeof node.clone === 'function') {
	            this.append(node.clone());
	          } else {
	            this.append(node);
	          }
	        }
	      } else {
	        this[name] = defaults[name];
	      }
	    }
	  }

	  addToError(error) {
	    error.postcssNode = this;
	    if (error.stack && this.source && /\n\s{4}at /.test(error.stack)) {
	      let s = this.source;
	      error.stack = error.stack.replace(
	        /\n\s{4}at /,
	        `$&${s.input.from}:${s.start.line}:${s.start.column}$&`
	      );
	    }
	    return error
	  }

	  after(add) {
	    this.parent.insertAfter(this, add);
	    return this
	  }

	  assign(overrides = {}) {
	    for (let name in overrides) {
	      this[name] = overrides[name];
	    }
	    return this
	  }

	  before(add) {
	    this.parent.insertBefore(this, add);
	    return this
	  }

	  cleanRaws(keepBetween) {
	    delete this.raws.before;
	    delete this.raws.after;
	    if (!keepBetween) delete this.raws.between;
	  }

	  clone(overrides = {}) {
	    let cloned = cloneNode(this);
	    for (let name in overrides) {
	      cloned[name] = overrides[name];
	    }
	    return cloned
	  }

	  cloneAfter(overrides = {}) {
	    let cloned = this.clone(overrides);
	    this.parent.insertAfter(this, cloned);
	    return cloned
	  }

	  cloneBefore(overrides = {}) {
	    let cloned = this.clone(overrides);
	    this.parent.insertBefore(this, cloned);
	    return cloned
	  }

	  error(message, opts = {}) {
	    if (this.source) {
	      let { end, start } = this.rangeBy(opts);
	      return this.source.input.error(
	        message,
	        { column: start.column, line: start.line },
	        { column: end.column, line: end.line },
	        opts
	      )
	    }
	    return new CssSyntaxError(message)
	  }

	  getProxyProcessor() {
	    return {
	      get(node, prop) {
	        if (prop === 'proxyOf') {
	          return node
	        } else if (prop === 'root') {
	          return () => node.root().toProxy()
	        } else {
	          return node[prop]
	        }
	      },

	      set(node, prop, value) {
	        if (node[prop] === value) return true
	        node[prop] = value;
	        if (
	          prop === 'prop' ||
	          prop === 'value' ||
	          prop === 'name' ||
	          prop === 'params' ||
	          prop === 'important' ||
	          /* c8 ignore next */
	          prop === 'text'
	        ) {
	          node.markDirty();
	        }
	        return true
	      }
	    }
	  }

	  /* c8 ignore next 3 */
	  markClean() {
	    this[isClean] = true;
	  }

	  markDirty() {
	    if (this[isClean]) {
	      this[isClean] = false;
	      let next = this;
	      while ((next = next.parent)) {
	        next[isClean] = false;
	      }
	    }
	  }

	  next() {
	    if (!this.parent) return undefined
	    let index = this.parent.index(this);
	    return this.parent.nodes[index + 1]
	  }

	  positionBy(opts = {}) {
	    let pos = this.source.start;
	    if (opts.index) {
	      pos = this.positionInside(opts.index);
	    } else if (opts.word) {
	      let inputString =
	        'document' in this.source.input
	          ? this.source.input.document
	          : this.source.input.css;
	      let stringRepresentation = inputString.slice(
	        sourceOffset(inputString, this.source.start),
	        sourceOffset(inputString, this.source.end)
	      );
	      let index = stringRepresentation.indexOf(opts.word);
	      if (index !== -1) pos = this.positionInside(index);
	    }
	    return pos
	  }

	  positionInside(index) {
	    let column = this.source.start.column;
	    let line = this.source.start.line;
	    let inputString =
	      'document' in this.source.input
	        ? this.source.input.document
	        : this.source.input.css;
	    let offset = sourceOffset(inputString, this.source.start);
	    let end = offset + index;

	    for (let i = offset; i < end; i++) {
	      if (inputString[i] === '\n') {
	        column = 1;
	        line += 1;
	      } else {
	        column += 1;
	      }
	    }

	    return { column, line, offset: end }
	  }

	  prev() {
	    if (!this.parent) return undefined
	    let index = this.parent.index(this);
	    return this.parent.nodes[index - 1]
	  }

	  rangeBy(opts = {}) {
	    let inputString =
	      'document' in this.source.input
	        ? this.source.input.document
	        : this.source.input.css;
	    let start = {
	      column: this.source.start.column,
	      line: this.source.start.line,
	      offset: sourceOffset(inputString, this.source.start)
	    };
	    let end = this.source.end
	      ? {
	          column: this.source.end.column + 1,
	          line: this.source.end.line,
	          offset:
	            typeof this.source.end.offset === 'number'
	              ? // `source.end.offset` is exclusive, so we don't need to add 1
	                this.source.end.offset
	              : // Since line/column in this.source.end is inclusive,
	                // the `sourceOffset(... , this.source.end)` returns an inclusive offset.
	                // So, we add 1 to convert it to exclusive.
	                sourceOffset(inputString, this.source.end) + 1
	        }
	      : {
	          column: start.column + 1,
	          line: start.line,
	          offset: start.offset + 1
	        };

	    if (opts.word) {
	      let stringRepresentation = inputString.slice(
	        sourceOffset(inputString, this.source.start),
	        sourceOffset(inputString, this.source.end)
	      );
	      let index = stringRepresentation.indexOf(opts.word);
	      if (index !== -1) {
	        start = this.positionInside(index);
	        end = this.positionInside(index + opts.word.length);
	      }
	    } else {
	      if (opts.start) {
	        start = {
	          column: opts.start.column,
	          line: opts.start.line,
	          offset: sourceOffset(inputString, opts.start)
	        };
	      } else if (opts.index) {
	        start = this.positionInside(opts.index);
	      }

	      if (opts.end) {
	        end = {
	          column: opts.end.column,
	          line: opts.end.line,
	          offset: sourceOffset(inputString, opts.end)
	        };
	      } else if (typeof opts.endIndex === 'number') {
	        end = this.positionInside(opts.endIndex);
	      } else if (opts.index) {
	        end = this.positionInside(opts.index + 1);
	      }
	    }

	    if (
	      end.line < start.line ||
	      (end.line === start.line && end.column <= start.column)
	    ) {
	      end = {
	        column: start.column + 1,
	        line: start.line,
	        offset: start.offset + 1
	      };
	    }

	    return { end, start }
	  }

	  raw(prop, defaultType) {
	    let str = new Stringifier();
	    return str.raw(this, prop, defaultType)
	  }

	  remove() {
	    if (this.parent) {
	      this.parent.removeChild(this);
	    }
	    this.parent = undefined;
	    return this
	  }

	  replaceWith(...nodes) {
	    if (this.parent) {
	      let bookmark = this;
	      let foundSelf = false;
	      for (let node of nodes) {
	        if (node === this) {
	          foundSelf = true;
	        } else if (foundSelf) {
	          this.parent.insertAfter(bookmark, node);
	          bookmark = node;
	        } else {
	          this.parent.insertBefore(bookmark, node);
	        }
	      }

	      if (!foundSelf) {
	        this.remove();
	      }
	    }

	    return this
	  }

	  root() {
	    let result = this;
	    while (result.parent && result.parent.type !== 'document') {
	      result = result.parent;
	    }
	    return result
	  }

	  toJSON(_, inputs) {
	    let fixed = {};
	    let emitInputs = inputs == null;
	    inputs = inputs || new Map();
	    let inputsNextIndex = 0;

	    for (let name in this) {
	      if (!Object.prototype.hasOwnProperty.call(this, name)) {
	        /* c8 ignore next 2 */
	        continue
	      }
	      if (name === 'parent' || name === 'proxyCache') continue
	      let value = this[name];

	      if (Array.isArray(value)) {
	        fixed[name] = value.map(i => {
	          if (typeof i === 'object' && i.toJSON) {
	            return i.toJSON(null, inputs)
	          } else {
	            return i
	          }
	        });
	      } else if (typeof value === 'object' && value.toJSON) {
	        fixed[name] = value.toJSON(null, inputs);
	      } else if (name === 'source') {
	        if (value == null) continue
	        let inputId = inputs.get(value.input);
	        if (inputId == null) {
	          inputId = inputsNextIndex;
	          inputs.set(value.input, inputsNextIndex);
	          inputsNextIndex++;
	        }
	        fixed[name] = {
	          end: value.end,
	          inputId,
	          start: value.start
	        };
	      } else {
	        fixed[name] = value;
	      }
	    }

	    if (emitInputs) {
	      fixed.inputs = [...inputs.keys()].map(input => input.toJSON());
	    }

	    return fixed
	  }

	  toProxy() {
	    if (!this.proxyCache) {
	      this.proxyCache = new Proxy(this, this.getProxyProcessor());
	    }
	    return this.proxyCache
	  }

	  toString(stringifier = stringify) {
	    if (stringifier.stringify) stringifier = stringifier.stringify;
	    let result = '';
	    stringifier(this, i => {
	      result += i;
	    });
	    return result
	  }

	  warn(result, text, opts = {}) {
	    let data = { node: this };
	    for (let i in opts) data[i] = opts[i];
	    return result.warn(text, data)
	  }
	}

	node = Node;
	Node.default = Node;
	return node;
}

var comment;
var hasRequiredComment;

function requireComment () {
	if (hasRequiredComment) return comment;
	hasRequiredComment = 1;

	let Node = requireNode();

	class Comment extends Node {
	  constructor(defaults) {
	    super(defaults);
	    this.type = 'comment';
	  }
	}

	comment = Comment;
	Comment.default = Comment;
	return comment;
}

var declaration;
var hasRequiredDeclaration;

function requireDeclaration () {
	if (hasRequiredDeclaration) return declaration;
	hasRequiredDeclaration = 1;

	let Node = requireNode();

	class Declaration extends Node {
	  get variable() {
	    return this.prop.startsWith('--') || this.prop[0] === '$'
	  }

	  constructor(defaults) {
	    if (
	      defaults &&
	      typeof defaults.value !== 'undefined' &&
	      typeof defaults.value !== 'string'
	    ) {
	      defaults = { ...defaults, value: String(defaults.value) };
	    }
	    super(defaults);
	    this.type = 'decl';
	  }
	}

	declaration = Declaration;
	Declaration.default = Declaration;
	return declaration;
}

var container;
var hasRequiredContainer;

function requireContainer () {
	if (hasRequiredContainer) return container;
	hasRequiredContainer = 1;

	let Comment = requireComment();
	let Declaration = requireDeclaration();
	let Node = requireNode();
	let { isClean, my } = requireSymbols();

	let AtRule, parse, Root, Rule;

	function cleanSource(nodes) {
	  return nodes.map(i => {
	    if (i.nodes) i.nodes = cleanSource(i.nodes);
	    delete i.source;
	    return i
	  })
	}

	function markTreeDirty(node) {
	  node[isClean] = false;
	  if (node.proxyOf.nodes) {
	    for (let i of node.proxyOf.nodes) {
	      markTreeDirty(i);
	    }
	  }
	}

	class Container extends Node {
	  get first() {
	    if (!this.proxyOf.nodes) return undefined
	    return this.proxyOf.nodes[0]
	  }

	  get last() {
	    if (!this.proxyOf.nodes) return undefined
	    return this.proxyOf.nodes[this.proxyOf.nodes.length - 1]
	  }

	  append(...children) {
	    for (let child of children) {
	      let nodes = this.normalize(child, this.last);
	      for (let node of nodes) this.proxyOf.nodes.push(node);
	    }

	    this.markDirty();

	    return this
	  }

	  cleanRaws(keepBetween) {
	    super.cleanRaws(keepBetween);
	    if (this.nodes) {
	      for (let node of this.nodes) node.cleanRaws(keepBetween);
	    }
	  }

	  each(callback) {
	    if (!this.proxyOf.nodes) return undefined
	    let iterator = this.getIterator();

	    let index, result;
	    while (this.indexes[iterator] < this.proxyOf.nodes.length) {
	      index = this.indexes[iterator];
	      result = callback(this.proxyOf.nodes[index], index);
	      if (result === false) break

	      this.indexes[iterator] += 1;
	    }

	    delete this.indexes[iterator];
	    return result
	  }

	  every(condition) {
	    return this.nodes.every(condition)
	  }

	  getIterator() {
	    if (!this.lastEach) this.lastEach = 0;
	    if (!this.indexes) this.indexes = {};

	    this.lastEach += 1;
	    let iterator = this.lastEach;
	    this.indexes[iterator] = 0;

	    return iterator
	  }

	  getProxyProcessor() {
	    return {
	      get(node, prop) {
	        if (prop === 'proxyOf') {
	          return node
	        } else if (!node[prop]) {
	          return node[prop]
	        } else if (
	          prop === 'each' ||
	          (typeof prop === 'string' && prop.startsWith('walk'))
	        ) {
	          return (...args) => {
	            return node[prop](
	              ...args.map(i => {
	                if (typeof i === 'function') {
	                  return (child, index) => i(child.toProxy(), index)
	                } else {
	                  return i
	                }
	              })
	            )
	          }
	        } else if (prop === 'every' || prop === 'some') {
	          return cb => {
	            return node[prop]((child, ...other) =>
	              cb(child.toProxy(), ...other)
	            )
	          }
	        } else if (prop === 'root') {
	          return () => node.root().toProxy()
	        } else if (prop === 'nodes') {
	          return node.nodes.map(i => i.toProxy())
	        } else if (prop === 'first' || prop === 'last') {
	          return node[prop].toProxy()
	        } else {
	          return node[prop]
	        }
	      },

	      set(node, prop, value) {
	        if (node[prop] === value) return true
	        node[prop] = value;
	        if (prop === 'name' || prop === 'params' || prop === 'selector') {
	          node.markDirty();
	        }
	        return true
	      }
	    }
	  }

	  index(child) {
	    if (typeof child === 'number') return child
	    if (child.proxyOf) child = child.proxyOf;
	    return this.proxyOf.nodes.indexOf(child)
	  }

	  insertAfter(exist, add) {
	    let existIndex = this.index(exist);
	    let nodes = this.normalize(add, this.proxyOf.nodes[existIndex]).reverse();
	    existIndex = this.index(exist);
	    for (let node of nodes) this.proxyOf.nodes.splice(existIndex + 1, 0, node);

	    let index;
	    for (let id in this.indexes) {
	      index = this.indexes[id];
	      if (existIndex < index) {
	        this.indexes[id] = index + nodes.length;
	      }
	    }

	    this.markDirty();

	    return this
	  }

	  insertBefore(exist, add) {
	    let existIndex = this.index(exist);
	    let type = existIndex === 0 ? 'prepend' : false;
	    let nodes = this.normalize(
	      add,
	      this.proxyOf.nodes[existIndex],
	      type
	    ).reverse();
	    existIndex = this.index(exist);
	    for (let node of nodes) this.proxyOf.nodes.splice(existIndex, 0, node);

	    let index;
	    for (let id in this.indexes) {
	      index = this.indexes[id];
	      if (existIndex <= index) {
	        this.indexes[id] = index + nodes.length;
	      }
	    }

	    this.markDirty();

	    return this
	  }

	  normalize(nodes, sample) {
	    if (typeof nodes === 'string') {
	      nodes = cleanSource(parse(nodes).nodes);
	    } else if (typeof nodes === 'undefined') {
	      nodes = [];
	    } else if (Array.isArray(nodes)) {
	      nodes = nodes.slice(0);
	      for (let i of nodes) {
	        if (i.parent) i.parent.removeChild(i, 'ignore');
	      }
	    } else if (nodes.type === 'root' && this.type !== 'document') {
	      nodes = nodes.nodes.slice(0);
	      for (let i of nodes) {
	        if (i.parent) i.parent.removeChild(i, 'ignore');
	      }
	    } else if (nodes.type) {
	      nodes = [nodes];
	    } else if (nodes.prop) {
	      if (typeof nodes.value === 'undefined') {
	        throw new Error('Value field is missed in node creation')
	      } else if (typeof nodes.value !== 'string') {
	        nodes.value = String(nodes.value);
	      }
	      nodes = [new Declaration(nodes)];
	    } else if (nodes.selector || nodes.selectors) {
	      nodes = [new Rule(nodes)];
	    } else if (nodes.name) {
	      nodes = [new AtRule(nodes)];
	    } else if (nodes.text) {
	      nodes = [new Comment(nodes)];
	    } else {
	      throw new Error('Unknown node type in node creation')
	    }

	    let processed = nodes.map(i => {
	      /* c8 ignore next */
	      if (!i[my]) Container.rebuild(i);
	      i = i.proxyOf;
	      if (i.parent) i.parent.removeChild(i);
	      if (i[isClean]) markTreeDirty(i);

	      if (!i.raws) i.raws = {};
	      if (typeof i.raws.before === 'undefined') {
	        if (sample && typeof sample.raws.before !== 'undefined') {
	          i.raws.before = sample.raws.before.replace(/\S/g, '');
	        }
	      }
	      i.parent = this.proxyOf;
	      return i
	    });

	    return processed
	  }

	  prepend(...children) {
	    children = children.reverse();
	    for (let child of children) {
	      let nodes = this.normalize(child, this.first, 'prepend').reverse();
	      for (let node of nodes) this.proxyOf.nodes.unshift(node);
	      for (let id in this.indexes) {
	        this.indexes[id] = this.indexes[id] + nodes.length;
	      }
	    }

	    this.markDirty();

	    return this
	  }

	  push(child) {
	    child.parent = this;
	    this.proxyOf.nodes.push(child);
	    return this
	  }

	  removeAll() {
	    for (let node of this.proxyOf.nodes) node.parent = undefined;
	    this.proxyOf.nodes = [];

	    this.markDirty();

	    return this
	  }

	  removeChild(child) {
	    child = this.index(child);
	    this.proxyOf.nodes[child].parent = undefined;
	    this.proxyOf.nodes.splice(child, 1);

	    let index;
	    for (let id in this.indexes) {
	      index = this.indexes[id];
	      if (index >= child) {
	        this.indexes[id] = index - 1;
	      }
	    }

	    this.markDirty();

	    return this
	  }

	  replaceValues(pattern, opts, callback) {
	    if (!callback) {
	      callback = opts;
	      opts = {};
	    }

	    this.walkDecls(decl => {
	      if (opts.props && !opts.props.includes(decl.prop)) return
	      if (opts.fast && !decl.value.includes(opts.fast)) return

	      decl.value = decl.value.replace(pattern, callback);
	    });

	    this.markDirty();

	    return this
	  }

	  some(condition) {
	    return this.nodes.some(condition)
	  }

	  walk(callback) {
	    return this.each((child, i) => {
	      let result;
	      try {
	        result = callback(child, i);
	      } catch (e) {
	        throw child.addToError(e)
	      }
	      if (result !== false && child.walk) {
	        result = child.walk(callback);
	      }

	      return result
	    })
	  }

	  walkAtRules(name, callback) {
	    if (!callback) {
	      callback = name;
	      return this.walk((child, i) => {
	        if (child.type === 'atrule') {
	          return callback(child, i)
	        }
	      })
	    }
	    if (name instanceof RegExp) {
	      return this.walk((child, i) => {
	        if (child.type === 'atrule' && name.test(child.name)) {
	          return callback(child, i)
	        }
	      })
	    }
	    return this.walk((child, i) => {
	      if (child.type === 'atrule' && child.name === name) {
	        return callback(child, i)
	      }
	    })
	  }

	  walkComments(callback) {
	    return this.walk((child, i) => {
	      if (child.type === 'comment') {
	        return callback(child, i)
	      }
	    })
	  }

	  walkDecls(prop, callback) {
	    if (!callback) {
	      callback = prop;
	      return this.walk((child, i) => {
	        if (child.type === 'decl') {
	          return callback(child, i)
	        }
	      })
	    }
	    if (prop instanceof RegExp) {
	      return this.walk((child, i) => {
	        if (child.type === 'decl' && prop.test(child.prop)) {
	          return callback(child, i)
	        }
	      })
	    }
	    return this.walk((child, i) => {
	      if (child.type === 'decl' && child.prop === prop) {
	        return callback(child, i)
	      }
	    })
	  }

	  walkRules(selector, callback) {
	    if (!callback) {
	      callback = selector;

	      return this.walk((child, i) => {
	        if (child.type === 'rule') {
	          return callback(child, i)
	        }
	      })
	    }
	    if (selector instanceof RegExp) {
	      return this.walk((child, i) => {
	        if (child.type === 'rule' && selector.test(child.selector)) {
	          return callback(child, i)
	        }
	      })
	    }
	    return this.walk((child, i) => {
	      if (child.type === 'rule' && child.selector === selector) {
	        return callback(child, i)
	      }
	    })
	  }
	}

	Container.registerParse = dependant => {
	  parse = dependant;
	};

	Container.registerRule = dependant => {
	  Rule = dependant;
	};

	Container.registerAtRule = dependant => {
	  AtRule = dependant;
	};

	Container.registerRoot = dependant => {
	  Root = dependant;
	};

	container = Container;
	Container.default = Container;

	/* c8 ignore start */
	Container.rebuild = node => {
	  if (node.type === 'atrule') {
	    Object.setPrototypeOf(node, AtRule.prototype);
	  } else if (node.type === 'rule') {
	    Object.setPrototypeOf(node, Rule.prototype);
	  } else if (node.type === 'decl') {
	    Object.setPrototypeOf(node, Declaration.prototype);
	  } else if (node.type === 'comment') {
	    Object.setPrototypeOf(node, Comment.prototype);
	  } else if (node.type === 'root') {
	    Object.setPrototypeOf(node, Root.prototype);
	  }

	  node[my] = true;

	  if (node.nodes) {
	    node.nodes.forEach(child => {
	      Container.rebuild(child);
	    });
	  }
	};
	/* c8 ignore stop */
	return container;
}

var atRule;
var hasRequiredAtRule;

function requireAtRule () {
	if (hasRequiredAtRule) return atRule;
	hasRequiredAtRule = 1;

	let Container = requireContainer();

	class AtRule extends Container {
	  constructor(defaults) {
	    super(defaults);
	    this.type = 'atrule';
	  }

	  append(...children) {
	    if (!this.proxyOf.nodes) this.nodes = [];
	    return super.append(...children)
	  }

	  prepend(...children) {
	    if (!this.proxyOf.nodes) this.nodes = [];
	    return super.prepend(...children)
	  }
	}

	atRule = AtRule;
	AtRule.default = AtRule;

	Container.registerAtRule(AtRule);
	return atRule;
}

var document$1;
var hasRequiredDocument;

function requireDocument () {
	if (hasRequiredDocument) return document$1;
	hasRequiredDocument = 1;

	let Container = requireContainer();

	let LazyResult, Processor;

	class Document extends Container {
	  constructor(defaults) {
	    // type needs to be passed to super, otherwise child roots won't be normalized correctly
	    super({ type: 'document', ...defaults });

	    if (!this.nodes) {
	      this.nodes = [];
	    }
	  }

	  toResult(opts = {}) {
	    let lazy = new LazyResult(new Processor(), this, opts);

	    return lazy.stringify()
	  }
	}

	Document.registerLazyResult = dependant => {
	  LazyResult = dependant;
	};

	Document.registerProcessor = dependant => {
	  Processor = dependant;
	};

	document$1 = Document;
	Document.default = Document;
	return document$1;
}

var nonSecure;
var hasRequiredNonSecure;

function requireNonSecure () {
	if (hasRequiredNonSecure) return nonSecure;
	hasRequiredNonSecure = 1;
	// This alphabet uses `A-Za-z0-9_-` symbols.
	// The order of characters is optimized for better gzip and brotli compression.
	// References to the same file (works both for gzip and brotli):
	// `'use`, `andom`, and `rict'`
	// References to the brotli default dictionary:
	// `-26T`, `1983`, `40px`, `75px`, `bush`, `jack`, `mind`, `very`, and `wolf`
	let urlAlphabet =
	  'useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict';

	let customAlphabet = (alphabet, defaultSize = 21) => {
	  return (size = defaultSize) => {
	    let id = '';
	    // A compact alternative for `for (var i = 0; i < step; i++)`.
	    let i = size | 0;
	    while (i--) {
	      // `| 0` is more compact and faster than `Math.floor()`.
	      id += alphabet[(Math.random() * alphabet.length) | 0];
	    }
	    return id
	  }
	};

	let nanoid = (size = 21) => {
	  let id = '';
	  // A compact alternative for `for (var i = 0; i < step; i++)`.
	  let i = size | 0;
	  while (i--) {
	    // `| 0` is more compact and faster than `Math.floor()`.
	    id += urlAlphabet[(Math.random() * 64) | 0];
	  }
	  return id
	};

	nonSecure = { nanoid, customAlphabet };
	return nonSecure;
}

var sourceMap = {};

var sourceMapGenerator = {};

var base64Vlq = {};

var base64 = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredBase64;

function requireBase64 () {
	if (hasRequiredBase64) return base64;
	hasRequiredBase64 = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	var intToCharMap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'.split('');

	/**
	 * Encode an integer in the range of 0 to 63 to a single base 64 digit.
	 */
	base64.encode = function (number) {
	  if (0 <= number && number < intToCharMap.length) {
	    return intToCharMap[number];
	  }
	  throw new TypeError("Must be between 0 and 63: " + number);
	};

	/**
	 * Decode a single base 64 character code digit to an integer. Returns -1 on
	 * failure.
	 */
	base64.decode = function (charCode) {
	  var bigA = 65;     // 'A'
	  var bigZ = 90;     // 'Z'

	  var littleA = 97;  // 'a'
	  var littleZ = 122; // 'z'

	  var zero = 48;     // '0'
	  var nine = 57;     // '9'

	  var plus = 43;     // '+'
	  var slash = 47;    // '/'

	  var littleOffset = 26;
	  var numberOffset = 52;

	  // 0 - 25: ABCDEFGHIJKLMNOPQRSTUVWXYZ
	  if (bigA <= charCode && charCode <= bigZ) {
	    return (charCode - bigA);
	  }

	  // 26 - 51: abcdefghijklmnopqrstuvwxyz
	  if (littleA <= charCode && charCode <= littleZ) {
	    return (charCode - littleA + littleOffset);
	  }

	  // 52 - 61: 0123456789
	  if (zero <= charCode && charCode <= nine) {
	    return (charCode - zero + numberOffset);
	  }

	  // 62: +
	  if (charCode == plus) {
	    return 62;
	  }

	  // 63: /
	  if (charCode == slash) {
	    return 63;
	  }

	  // Invalid base64 digit.
	  return -1;
	};
	return base64;
}

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredBase64Vlq;

function requireBase64Vlq () {
	if (hasRequiredBase64Vlq) return base64Vlq;
	hasRequiredBase64Vlq = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 *
	 * Based on the Base 64 VLQ implementation in Closure Compiler:
	 * https://code.google.com/p/closure-compiler/source/browse/trunk/src/com/google/debugging/sourcemap/Base64VLQ.java
	 *
	 * Copyright 2011 The Closure Compiler Authors. All rights reserved.
	 * Redistribution and use in source and binary forms, with or without
	 * modification, are permitted provided that the following conditions are
	 * met:
	 *
	 *  * Redistributions of source code must retain the above copyright
	 *    notice, this list of conditions and the following disclaimer.
	 *  * Redistributions in binary form must reproduce the above
	 *    copyright notice, this list of conditions and the following
	 *    disclaimer in the documentation and/or other materials provided
	 *    with the distribution.
	 *  * Neither the name of Google Inc. nor the names of its
	 *    contributors may be used to endorse or promote products derived
	 *    from this software without specific prior written permission.
	 *
	 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
	 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
	 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
	 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
	 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
	 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
	 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
	 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	 */

	var base64 = requireBase64();

	// A single base 64 digit can contain 6 bits of data. For the base 64 variable
	// length quantities we use in the source map spec, the first bit is the sign,
	// the next four bits are the actual value, and the 6th bit is the
	// continuation bit. The continuation bit tells us whether there are more
	// digits in this value following this digit.
	//
	//   Continuation
	//   |    Sign
	//   |    |
	//   V    V
	//   101011

	var VLQ_BASE_SHIFT = 5;

	// binary: 100000
	var VLQ_BASE = 1 << VLQ_BASE_SHIFT;

	// binary: 011111
	var VLQ_BASE_MASK = VLQ_BASE - 1;

	// binary: 100000
	var VLQ_CONTINUATION_BIT = VLQ_BASE;

	/**
	 * Converts from a two-complement value to a value where the sign bit is
	 * placed in the least significant bit.  For example, as decimals:
	 *   1 becomes 2 (10 binary), -1 becomes 3 (11 binary)
	 *   2 becomes 4 (100 binary), -2 becomes 5 (101 binary)
	 */
	function toVLQSigned(aValue) {
	  return aValue < 0
	    ? ((-aValue) << 1) + 1
	    : (aValue << 1) + 0;
	}

	/**
	 * Converts to a two-complement value from a value where the sign bit is
	 * placed in the least significant bit.  For example, as decimals:
	 *   2 (10 binary) becomes 1, 3 (11 binary) becomes -1
	 *   4 (100 binary) becomes 2, 5 (101 binary) becomes -2
	 */
	function fromVLQSigned(aValue) {
	  var isNegative = (aValue & 1) === 1;
	  var shifted = aValue >> 1;
	  return isNegative
	    ? -shifted
	    : shifted;
	}

	/**
	 * Returns the base 64 VLQ encoded value.
	 */
	base64Vlq.encode = function base64VLQ_encode(aValue) {
	  var encoded = "";
	  var digit;

	  var vlq = toVLQSigned(aValue);

	  do {
	    digit = vlq & VLQ_BASE_MASK;
	    vlq >>>= VLQ_BASE_SHIFT;
	    if (vlq > 0) {
	      // There are still more digits in this value, so we must make sure the
	      // continuation bit is marked.
	      digit |= VLQ_CONTINUATION_BIT;
	    }
	    encoded += base64.encode(digit);
	  } while (vlq > 0);

	  return encoded;
	};

	/**
	 * Decodes the next base 64 VLQ value from the given string and returns the
	 * value and the rest of the string via the out parameter.
	 */
	base64Vlq.decode = function base64VLQ_decode(aStr, aIndex, aOutParam) {
	  var strLen = aStr.length;
	  var result = 0;
	  var shift = 0;
	  var continuation, digit;

	  do {
	    if (aIndex >= strLen) {
	      throw new Error("Expected more digits in base 64 VLQ value.");
	    }

	    digit = base64.decode(aStr.charCodeAt(aIndex++));
	    if (digit === -1) {
	      throw new Error("Invalid base64 digit: " + aStr.charAt(aIndex - 1));
	    }

	    continuation = !!(digit & VLQ_CONTINUATION_BIT);
	    digit &= VLQ_BASE_MASK;
	    result = result + (digit << shift);
	    shift += VLQ_BASE_SHIFT;
	  } while (continuation);

	  aOutParam.value = fromVLQSigned(result);
	  aOutParam.rest = aIndex;
	};
	return base64Vlq;
}

var util = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredUtil;

function requireUtil () {
	if (hasRequiredUtil) return util;
	hasRequiredUtil = 1;
	(function (exports$1) {
		/*
		 * Copyright 2011 Mozilla Foundation and contributors
		 * Licensed under the New BSD license. See LICENSE or:
		 * http://opensource.org/licenses/BSD-3-Clause
		 */

		/**
		 * This is a helper function for getting values from parameter/options
		 * objects.
		 *
		 * @param args The object we are extracting values from
		 * @param name The name of the property we are getting.
		 * @param defaultValue An optional value to return if the property is missing
		 * from the object. If this is not specified and the property is missing, an
		 * error will be thrown.
		 */
		function getArg(aArgs, aName, aDefaultValue) {
		  if (aName in aArgs) {
		    return aArgs[aName];
		  } else if (arguments.length === 3) {
		    return aDefaultValue;
		  } else {
		    throw new Error('"' + aName + '" is a required argument.');
		  }
		}
		exports$1.getArg = getArg;

		var urlRegexp = /^(?:([\w+\-.]+):)?\/\/(?:(\w+:\w+)@)?([\w.-]*)(?::(\d+))?(.*)$/;
		var dataUrlRegexp = /^data:.+\,.+$/;

		function urlParse(aUrl) {
		  var match = aUrl.match(urlRegexp);
		  if (!match) {
		    return null;
		  }
		  return {
		    scheme: match[1],
		    auth: match[2],
		    host: match[3],
		    port: match[4],
		    path: match[5]
		  };
		}
		exports$1.urlParse = urlParse;

		function urlGenerate(aParsedUrl) {
		  var url = '';
		  if (aParsedUrl.scheme) {
		    url += aParsedUrl.scheme + ':';
		  }
		  url += '//';
		  if (aParsedUrl.auth) {
		    url += aParsedUrl.auth + '@';
		  }
		  if (aParsedUrl.host) {
		    url += aParsedUrl.host;
		  }
		  if (aParsedUrl.port) {
		    url += ":" + aParsedUrl.port;
		  }
		  if (aParsedUrl.path) {
		    url += aParsedUrl.path;
		  }
		  return url;
		}
		exports$1.urlGenerate = urlGenerate;

		var MAX_CACHED_INPUTS = 32;

		/**
		 * Takes some function `f(input) -> result` and returns a memoized version of
		 * `f`.
		 *
		 * We keep at most `MAX_CACHED_INPUTS` memoized results of `f` alive. The
		 * memoization is a dumb-simple, linear least-recently-used cache.
		 */
		function lruMemoize(f) {
		  var cache = [];

		  return function(input) {
		    for (var i = 0; i < cache.length; i++) {
		      if (cache[i].input === input) {
		        var temp = cache[0];
		        cache[0] = cache[i];
		        cache[i] = temp;
		        return cache[0].result;
		      }
		    }

		    var result = f(input);

		    cache.unshift({
		      input,
		      result,
		    });

		    if (cache.length > MAX_CACHED_INPUTS) {
		      cache.pop();
		    }

		    return result;
		  };
		}

		/**
		 * Normalizes a path, or the path portion of a URL:
		 *
		 * - Replaces consecutive slashes with one slash.
		 * - Removes unnecessary '.' parts.
		 * - Removes unnecessary '<dir>/..' parts.
		 *
		 * Based on code in the Node.js 'path' core module.
		 *
		 * @param aPath The path or url to normalize.
		 */
		var normalize = lruMemoize(function normalize(aPath) {
		  var path = aPath;
		  var url = urlParse(aPath);
		  if (url) {
		    if (!url.path) {
		      return aPath;
		    }
		    path = url.path;
		  }
		  var isAbsolute = exports$1.isAbsolute(path);
		  // Split the path into parts between `/` characters. This is much faster than
		  // using `.split(/\/+/g)`.
		  var parts = [];
		  var start = 0;
		  var i = 0;
		  while (true) {
		    start = i;
		    i = path.indexOf("/", start);
		    if (i === -1) {
		      parts.push(path.slice(start));
		      break;
		    } else {
		      parts.push(path.slice(start, i));
		      while (i < path.length && path[i] === "/") {
		        i++;
		      }
		    }
		  }

		  for (var part, up = 0, i = parts.length - 1; i >= 0; i--) {
		    part = parts[i];
		    if (part === '.') {
		      parts.splice(i, 1);
		    } else if (part === '..') {
		      up++;
		    } else if (up > 0) {
		      if (part === '') {
		        // The first part is blank if the path is absolute. Trying to go
		        // above the root is a no-op. Therefore we can remove all '..' parts
		        // directly after the root.
		        parts.splice(i + 1, up);
		        up = 0;
		      } else {
		        parts.splice(i, 2);
		        up--;
		      }
		    }
		  }
		  path = parts.join('/');

		  if (path === '') {
		    path = isAbsolute ? '/' : '.';
		  }

		  if (url) {
		    url.path = path;
		    return urlGenerate(url);
		  }
		  return path;
		});
		exports$1.normalize = normalize;

		/**
		 * Joins two paths/URLs.
		 *
		 * @param aRoot The root path or URL.
		 * @param aPath The path or URL to be joined with the root.
		 *
		 * - If aPath is a URL or a data URI, aPath is returned, unless aPath is a
		 *   scheme-relative URL: Then the scheme of aRoot, if any, is prepended
		 *   first.
		 * - Otherwise aPath is a path. If aRoot is a URL, then its path portion
		 *   is updated with the result and aRoot is returned. Otherwise the result
		 *   is returned.
		 *   - If aPath is absolute, the result is aPath.
		 *   - Otherwise the two paths are joined with a slash.
		 * - Joining for example 'http://' and 'www.example.com' is also supported.
		 */
		function join(aRoot, aPath) {
		  if (aRoot === "") {
		    aRoot = ".";
		  }
		  if (aPath === "") {
		    aPath = ".";
		  }
		  var aPathUrl = urlParse(aPath);
		  var aRootUrl = urlParse(aRoot);
		  if (aRootUrl) {
		    aRoot = aRootUrl.path || '/';
		  }

		  // `join(foo, '//www.example.org')`
		  if (aPathUrl && !aPathUrl.scheme) {
		    if (aRootUrl) {
		      aPathUrl.scheme = aRootUrl.scheme;
		    }
		    return urlGenerate(aPathUrl);
		  }

		  if (aPathUrl || aPath.match(dataUrlRegexp)) {
		    return aPath;
		  }

		  // `join('http://', 'www.example.com')`
		  if (aRootUrl && !aRootUrl.host && !aRootUrl.path) {
		    aRootUrl.host = aPath;
		    return urlGenerate(aRootUrl);
		  }

		  var joined = aPath.charAt(0) === '/'
		    ? aPath
		    : normalize(aRoot.replace(/\/+$/, '') + '/' + aPath);

		  if (aRootUrl) {
		    aRootUrl.path = joined;
		    return urlGenerate(aRootUrl);
		  }
		  return joined;
		}
		exports$1.join = join;

		exports$1.isAbsolute = function (aPath) {
		  return aPath.charAt(0) === '/' || urlRegexp.test(aPath);
		};

		/**
		 * Make a path relative to a URL or another path.
		 *
		 * @param aRoot The root path or URL.
		 * @param aPath The path or URL to be made relative to aRoot.
		 */
		function relative(aRoot, aPath) {
		  if (aRoot === "") {
		    aRoot = ".";
		  }

		  aRoot = aRoot.replace(/\/$/, '');

		  // It is possible for the path to be above the root. In this case, simply
		  // checking whether the root is a prefix of the path won't work. Instead, we
		  // need to remove components from the root one by one, until either we find
		  // a prefix that fits, or we run out of components to remove.
		  var level = 0;
		  while (aPath.indexOf(aRoot + '/') !== 0) {
		    var index = aRoot.lastIndexOf("/");
		    if (index < 0) {
		      return aPath;
		    }

		    // If the only part of the root that is left is the scheme (i.e. http://,
		    // file:///, etc.), one or more slashes (/), or simply nothing at all, we
		    // have exhausted all components, so the path is not relative to the root.
		    aRoot = aRoot.slice(0, index);
		    if (aRoot.match(/^([^\/]+:\/)?\/*$/)) {
		      return aPath;
		    }

		    ++level;
		  }

		  // Make sure we add a "../" for each component we removed from the root.
		  return Array(level + 1).join("../") + aPath.substr(aRoot.length + 1);
		}
		exports$1.relative = relative;

		var supportsNullProto = (function () {
		  var obj = Object.create(null);
		  return !('__proto__' in obj);
		}());

		function identity (s) {
		  return s;
		}

		/**
		 * Because behavior goes wacky when you set `__proto__` on objects, we
		 * have to prefix all the strings in our set with an arbitrary character.
		 *
		 * See https://github.com/mozilla/source-map/pull/31 and
		 * https://github.com/mozilla/source-map/issues/30
		 *
		 * @param String aStr
		 */
		function toSetString(aStr) {
		  if (isProtoString(aStr)) {
		    return '$' + aStr;
		  }

		  return aStr;
		}
		exports$1.toSetString = supportsNullProto ? identity : toSetString;

		function fromSetString(aStr) {
		  if (isProtoString(aStr)) {
		    return aStr.slice(1);
		  }

		  return aStr;
		}
		exports$1.fromSetString = supportsNullProto ? identity : fromSetString;

		function isProtoString(s) {
		  if (!s) {
		    return false;
		  }

		  var length = s.length;

		  if (length < 9 /* "__proto__".length */) {
		    return false;
		  }

		  if (s.charCodeAt(length - 1) !== 95  /* '_' */ ||
		      s.charCodeAt(length - 2) !== 95  /* '_' */ ||
		      s.charCodeAt(length - 3) !== 111 /* 'o' */ ||
		      s.charCodeAt(length - 4) !== 116 /* 't' */ ||
		      s.charCodeAt(length - 5) !== 111 /* 'o' */ ||
		      s.charCodeAt(length - 6) !== 114 /* 'r' */ ||
		      s.charCodeAt(length - 7) !== 112 /* 'p' */ ||
		      s.charCodeAt(length - 8) !== 95  /* '_' */ ||
		      s.charCodeAt(length - 9) !== 95  /* '_' */) {
		    return false;
		  }

		  for (var i = length - 10; i >= 0; i--) {
		    if (s.charCodeAt(i) !== 36 /* '$' */) {
		      return false;
		    }
		  }

		  return true;
		}

		/**
		 * Comparator between two mappings where the original positions are compared.
		 *
		 * Optionally pass in `true` as `onlyCompareGenerated` to consider two
		 * mappings with the same original source/line/column, but different generated
		 * line and column the same. Useful when searching for a mapping with a
		 * stubbed out mapping.
		 */
		function compareByOriginalPositions(mappingA, mappingB, onlyCompareOriginal) {
		  var cmp = strcmp(mappingA.source, mappingB.source);
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalLine - mappingB.originalLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalColumn - mappingB.originalColumn;
		  if (cmp !== 0 || onlyCompareOriginal) {
		    return cmp;
		  }

		  cmp = mappingA.generatedColumn - mappingB.generatedColumn;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.generatedLine - mappingB.generatedLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  return strcmp(mappingA.name, mappingB.name);
		}
		exports$1.compareByOriginalPositions = compareByOriginalPositions;

		function compareByOriginalPositionsNoSource(mappingA, mappingB, onlyCompareOriginal) {
		  var cmp;

		  cmp = mappingA.originalLine - mappingB.originalLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalColumn - mappingB.originalColumn;
		  if (cmp !== 0 || onlyCompareOriginal) {
		    return cmp;
		  }

		  cmp = mappingA.generatedColumn - mappingB.generatedColumn;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.generatedLine - mappingB.generatedLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  return strcmp(mappingA.name, mappingB.name);
		}
		exports$1.compareByOriginalPositionsNoSource = compareByOriginalPositionsNoSource;

		/**
		 * Comparator between two mappings with deflated source and name indices where
		 * the generated positions are compared.
		 *
		 * Optionally pass in `true` as `onlyCompareGenerated` to consider two
		 * mappings with the same generated line and column, but different
		 * source/name/original line and column the same. Useful when searching for a
		 * mapping with a stubbed out mapping.
		 */
		function compareByGeneratedPositionsDeflated(mappingA, mappingB, onlyCompareGenerated) {
		  var cmp = mappingA.generatedLine - mappingB.generatedLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.generatedColumn - mappingB.generatedColumn;
		  if (cmp !== 0 || onlyCompareGenerated) {
		    return cmp;
		  }

		  cmp = strcmp(mappingA.source, mappingB.source);
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalLine - mappingB.originalLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalColumn - mappingB.originalColumn;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  return strcmp(mappingA.name, mappingB.name);
		}
		exports$1.compareByGeneratedPositionsDeflated = compareByGeneratedPositionsDeflated;

		function compareByGeneratedPositionsDeflatedNoLine(mappingA, mappingB, onlyCompareGenerated) {
		  var cmp = mappingA.generatedColumn - mappingB.generatedColumn;
		  if (cmp !== 0 || onlyCompareGenerated) {
		    return cmp;
		  }

		  cmp = strcmp(mappingA.source, mappingB.source);
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalLine - mappingB.originalLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalColumn - mappingB.originalColumn;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  return strcmp(mappingA.name, mappingB.name);
		}
		exports$1.compareByGeneratedPositionsDeflatedNoLine = compareByGeneratedPositionsDeflatedNoLine;

		function strcmp(aStr1, aStr2) {
		  if (aStr1 === aStr2) {
		    return 0;
		  }

		  if (aStr1 === null) {
		    return 1; // aStr2 !== null
		  }

		  if (aStr2 === null) {
		    return -1; // aStr1 !== null
		  }

		  if (aStr1 > aStr2) {
		    return 1;
		  }

		  return -1;
		}

		/**
		 * Comparator between two mappings with inflated source and name strings where
		 * the generated positions are compared.
		 */
		function compareByGeneratedPositionsInflated(mappingA, mappingB) {
		  var cmp = mappingA.generatedLine - mappingB.generatedLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.generatedColumn - mappingB.generatedColumn;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = strcmp(mappingA.source, mappingB.source);
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalLine - mappingB.originalLine;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  cmp = mappingA.originalColumn - mappingB.originalColumn;
		  if (cmp !== 0) {
		    return cmp;
		  }

		  return strcmp(mappingA.name, mappingB.name);
		}
		exports$1.compareByGeneratedPositionsInflated = compareByGeneratedPositionsInflated;

		/**
		 * Strip any JSON XSSI avoidance prefix from the string (as documented
		 * in the source maps specification), and then parse the string as
		 * JSON.
		 */
		function parseSourceMapInput(str) {
		  return JSON.parse(str.replace(/^\)]}'[^\n]*\n/, ''));
		}
		exports$1.parseSourceMapInput = parseSourceMapInput;

		/**
		 * Compute the URL of a source given the the source root, the source's
		 * URL, and the source map's URL.
		 */
		function computeSourceURL(sourceRoot, sourceURL, sourceMapURL) {
		  sourceURL = sourceURL || '';

		  if (sourceRoot) {
		    // This follows what Chrome does.
		    if (sourceRoot[sourceRoot.length - 1] !== '/' && sourceURL[0] !== '/') {
		      sourceRoot += '/';
		    }
		    // The spec says:
		    //   Line 4: An optional source root, useful for relocating source
		    //   files on a server or removing repeated values in the
		    //   “sources” entry.  This value is prepended to the individual
		    //   entries in the “source” field.
		    sourceURL = sourceRoot + sourceURL;
		  }

		  // Historically, SourceMapConsumer did not take the sourceMapURL as
		  // a parameter.  This mode is still somewhat supported, which is why
		  // this code block is conditional.  However, it's preferable to pass
		  // the source map URL to SourceMapConsumer, so that this function
		  // can implement the source URL resolution algorithm as outlined in
		  // the spec.  This block is basically the equivalent of:
		  //    new URL(sourceURL, sourceMapURL).toString()
		  // ... except it avoids using URL, which wasn't available in the
		  // older releases of node still supported by this library.
		  //
		  // The spec says:
		  //   If the sources are not absolute URLs after prepending of the
		  //   “sourceRoot”, the sources are resolved relative to the
		  //   SourceMap (like resolving script src in a html document).
		  if (sourceMapURL) {
		    var parsed = urlParse(sourceMapURL);
		    if (!parsed) {
		      throw new Error("sourceMapURL could not be parsed");
		    }
		    if (parsed.path) {
		      // Strip the last path component, but keep the "/".
		      var index = parsed.path.lastIndexOf('/');
		      if (index >= 0) {
		        parsed.path = parsed.path.substring(0, index + 1);
		      }
		    }
		    sourceURL = join(urlGenerate(parsed), sourceURL);
		  }

		  return normalize(sourceURL);
		}
		exports$1.computeSourceURL = computeSourceURL; 
	} (util));
	return util;
}

var arraySet = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredArraySet;

function requireArraySet () {
	if (hasRequiredArraySet) return arraySet;
	hasRequiredArraySet = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	var util = requireUtil();
	var has = Object.prototype.hasOwnProperty;
	var hasNativeMap = typeof Map !== "undefined";

	/**
	 * A data structure which is a combination of an array and a set. Adding a new
	 * member is O(1), testing for membership is O(1), and finding the index of an
	 * element is O(1). Removing elements from the set is not supported. Only
	 * strings are supported for membership.
	 */
	function ArraySet() {
	  this._array = [];
	  this._set = hasNativeMap ? new Map() : Object.create(null);
	}

	/**
	 * Static method for creating ArraySet instances from an existing array.
	 */
	ArraySet.fromArray = function ArraySet_fromArray(aArray, aAllowDuplicates) {
	  var set = new ArraySet();
	  for (var i = 0, len = aArray.length; i < len; i++) {
	    set.add(aArray[i], aAllowDuplicates);
	  }
	  return set;
	};

	/**
	 * Return how many unique items are in this ArraySet. If duplicates have been
	 * added, than those do not count towards the size.
	 *
	 * @returns Number
	 */
	ArraySet.prototype.size = function ArraySet_size() {
	  return hasNativeMap ? this._set.size : Object.getOwnPropertyNames(this._set).length;
	};

	/**
	 * Add the given string to this set.
	 *
	 * @param String aStr
	 */
	ArraySet.prototype.add = function ArraySet_add(aStr, aAllowDuplicates) {
	  var sStr = hasNativeMap ? aStr : util.toSetString(aStr);
	  var isDuplicate = hasNativeMap ? this.has(aStr) : has.call(this._set, sStr);
	  var idx = this._array.length;
	  if (!isDuplicate || aAllowDuplicates) {
	    this._array.push(aStr);
	  }
	  if (!isDuplicate) {
	    if (hasNativeMap) {
	      this._set.set(aStr, idx);
	    } else {
	      this._set[sStr] = idx;
	    }
	  }
	};

	/**
	 * Is the given string a member of this set?
	 *
	 * @param String aStr
	 */
	ArraySet.prototype.has = function ArraySet_has(aStr) {
	  if (hasNativeMap) {
	    return this._set.has(aStr);
	  } else {
	    var sStr = util.toSetString(aStr);
	    return has.call(this._set, sStr);
	  }
	};

	/**
	 * What is the index of the given string in the array?
	 *
	 * @param String aStr
	 */
	ArraySet.prototype.indexOf = function ArraySet_indexOf(aStr) {
	  if (hasNativeMap) {
	    var idx = this._set.get(aStr);
	    if (idx >= 0) {
	        return idx;
	    }
	  } else {
	    var sStr = util.toSetString(aStr);
	    if (has.call(this._set, sStr)) {
	      return this._set[sStr];
	    }
	  }

	  throw new Error('"' + aStr + '" is not in the set.');
	};

	/**
	 * What is the element at the given index?
	 *
	 * @param Number aIdx
	 */
	ArraySet.prototype.at = function ArraySet_at(aIdx) {
	  if (aIdx >= 0 && aIdx < this._array.length) {
	    return this._array[aIdx];
	  }
	  throw new Error('No element indexed by ' + aIdx);
	};

	/**
	 * Returns the array representation of this set (which has the proper indices
	 * indicated by indexOf). Note that this is a copy of the internal array used
	 * for storing the members so that no one can mess with internal state.
	 */
	ArraySet.prototype.toArray = function ArraySet_toArray() {
	  return this._array.slice();
	};

	arraySet.ArraySet = ArraySet;
	return arraySet;
}

var mappingList = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredMappingList;

function requireMappingList () {
	if (hasRequiredMappingList) return mappingList;
	hasRequiredMappingList = 1;
	/*
	 * Copyright 2014 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	var util = requireUtil();

	/**
	 * Determine whether mappingB is after mappingA with respect to generated
	 * position.
	 */
	function generatedPositionAfter(mappingA, mappingB) {
	  // Optimized for most common case
	  var lineA = mappingA.generatedLine;
	  var lineB = mappingB.generatedLine;
	  var columnA = mappingA.generatedColumn;
	  var columnB = mappingB.generatedColumn;
	  return lineB > lineA || lineB == lineA && columnB >= columnA ||
	         util.compareByGeneratedPositionsInflated(mappingA, mappingB) <= 0;
	}

	/**
	 * A data structure to provide a sorted view of accumulated mappings in a
	 * performance conscious manner. It trades a neglibable overhead in general
	 * case for a large speedup in case of mappings being added in order.
	 */
	function MappingList() {
	  this._array = [];
	  this._sorted = true;
	  // Serves as infimum
	  this._last = {generatedLine: -1, generatedColumn: 0};
	}

	/**
	 * Iterate through internal items. This method takes the same arguments that
	 * `Array.prototype.forEach` takes.
	 *
	 * NOTE: The order of the mappings is NOT guaranteed.
	 */
	MappingList.prototype.unsortedForEach =
	  function MappingList_forEach(aCallback, aThisArg) {
	    this._array.forEach(aCallback, aThisArg);
	  };

	/**
	 * Add the given source mapping.
	 *
	 * @param Object aMapping
	 */
	MappingList.prototype.add = function MappingList_add(aMapping) {
	  if (generatedPositionAfter(this._last, aMapping)) {
	    this._last = aMapping;
	    this._array.push(aMapping);
	  } else {
	    this._sorted = false;
	    this._array.push(aMapping);
	  }
	};

	/**
	 * Returns the flat, sorted array of mappings. The mappings are sorted by
	 * generated position.
	 *
	 * WARNING: This method returns internal data without copying, for
	 * performance. The return value must NOT be mutated, and should be treated as
	 * an immutable borrow. If you want to take ownership, you must make your own
	 * copy.
	 */
	MappingList.prototype.toArray = function MappingList_toArray() {
	  if (!this._sorted) {
	    this._array.sort(util.compareByGeneratedPositionsInflated);
	    this._sorted = true;
	  }
	  return this._array;
	};

	mappingList.MappingList = MappingList;
	return mappingList;
}

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredSourceMapGenerator;

function requireSourceMapGenerator () {
	if (hasRequiredSourceMapGenerator) return sourceMapGenerator;
	hasRequiredSourceMapGenerator = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	var base64VLQ = requireBase64Vlq();
	var util = requireUtil();
	var ArraySet = requireArraySet().ArraySet;
	var MappingList = requireMappingList().MappingList;

	/**
	 * An instance of the SourceMapGenerator represents a source map which is
	 * being built incrementally. You may pass an object with the following
	 * properties:
	 *
	 *   - file: The filename of the generated source.
	 *   - sourceRoot: A root for all relative URLs in this source map.
	 */
	function SourceMapGenerator(aArgs) {
	  if (!aArgs) {
	    aArgs = {};
	  }
	  this._file = util.getArg(aArgs, 'file', null);
	  this._sourceRoot = util.getArg(aArgs, 'sourceRoot', null);
	  this._skipValidation = util.getArg(aArgs, 'skipValidation', false);
	  this._ignoreInvalidMapping = util.getArg(aArgs, 'ignoreInvalidMapping', false);
	  this._sources = new ArraySet();
	  this._names = new ArraySet();
	  this._mappings = new MappingList();
	  this._sourcesContents = null;
	}

	SourceMapGenerator.prototype._version = 3;

	/**
	 * Creates a new SourceMapGenerator based on a SourceMapConsumer
	 *
	 * @param aSourceMapConsumer The SourceMap.
	 */
	SourceMapGenerator.fromSourceMap =
	  function SourceMapGenerator_fromSourceMap(aSourceMapConsumer, generatorOps) {
	    var sourceRoot = aSourceMapConsumer.sourceRoot;
	    var generator = new SourceMapGenerator(Object.assign(generatorOps || {}, {
	      file: aSourceMapConsumer.file,
	      sourceRoot: sourceRoot
	    }));
	    aSourceMapConsumer.eachMapping(function (mapping) {
	      var newMapping = {
	        generated: {
	          line: mapping.generatedLine,
	          column: mapping.generatedColumn
	        }
	      };

	      if (mapping.source != null) {
	        newMapping.source = mapping.source;
	        if (sourceRoot != null) {
	          newMapping.source = util.relative(sourceRoot, newMapping.source);
	        }

	        newMapping.original = {
	          line: mapping.originalLine,
	          column: mapping.originalColumn
	        };

	        if (mapping.name != null) {
	          newMapping.name = mapping.name;
	        }
	      }

	      generator.addMapping(newMapping);
	    });
	    aSourceMapConsumer.sources.forEach(function (sourceFile) {
	      var sourceRelative = sourceFile;
	      if (sourceRoot !== null) {
	        sourceRelative = util.relative(sourceRoot, sourceFile);
	      }

	      if (!generator._sources.has(sourceRelative)) {
	        generator._sources.add(sourceRelative);
	      }

	      var content = aSourceMapConsumer.sourceContentFor(sourceFile);
	      if (content != null) {
	        generator.setSourceContent(sourceFile, content);
	      }
	    });
	    return generator;
	  };

	/**
	 * Add a single mapping from original source line and column to the generated
	 * source's line and column for this source map being created. The mapping
	 * object should have the following properties:
	 *
	 *   - generated: An object with the generated line and column positions.
	 *   - original: An object with the original line and column positions.
	 *   - source: The original source file (relative to the sourceRoot).
	 *   - name: An optional original token name for this mapping.
	 */
	SourceMapGenerator.prototype.addMapping =
	  function SourceMapGenerator_addMapping(aArgs) {
	    var generated = util.getArg(aArgs, 'generated');
	    var original = util.getArg(aArgs, 'original', null);
	    var source = util.getArg(aArgs, 'source', null);
	    var name = util.getArg(aArgs, 'name', null);

	    if (!this._skipValidation) {
	      if (this._validateMapping(generated, original, source, name) === false) {
	        return;
	      }
	    }

	    if (source != null) {
	      source = String(source);
	      if (!this._sources.has(source)) {
	        this._sources.add(source);
	      }
	    }

	    if (name != null) {
	      name = String(name);
	      if (!this._names.has(name)) {
	        this._names.add(name);
	      }
	    }

	    this._mappings.add({
	      generatedLine: generated.line,
	      generatedColumn: generated.column,
	      originalLine: original != null && original.line,
	      originalColumn: original != null && original.column,
	      source: source,
	      name: name
	    });
	  };

	/**
	 * Set the source content for a source file.
	 */
	SourceMapGenerator.prototype.setSourceContent =
	  function SourceMapGenerator_setSourceContent(aSourceFile, aSourceContent) {
	    var source = aSourceFile;
	    if (this._sourceRoot != null) {
	      source = util.relative(this._sourceRoot, source);
	    }

	    if (aSourceContent != null) {
	      // Add the source content to the _sourcesContents map.
	      // Create a new _sourcesContents map if the property is null.
	      if (!this._sourcesContents) {
	        this._sourcesContents = Object.create(null);
	      }
	      this._sourcesContents[util.toSetString(source)] = aSourceContent;
	    } else if (this._sourcesContents) {
	      // Remove the source file from the _sourcesContents map.
	      // If the _sourcesContents map is empty, set the property to null.
	      delete this._sourcesContents[util.toSetString(source)];
	      if (Object.keys(this._sourcesContents).length === 0) {
	        this._sourcesContents = null;
	      }
	    }
	  };

	/**
	 * Applies the mappings of a sub-source-map for a specific source file to the
	 * source map being generated. Each mapping to the supplied source file is
	 * rewritten using the supplied source map. Note: The resolution for the
	 * resulting mappings is the minimium of this map and the supplied map.
	 *
	 * @param aSourceMapConsumer The source map to be applied.
	 * @param aSourceFile Optional. The filename of the source file.
	 *        If omitted, SourceMapConsumer's file property will be used.
	 * @param aSourceMapPath Optional. The dirname of the path to the source map
	 *        to be applied. If relative, it is relative to the SourceMapConsumer.
	 *        This parameter is needed when the two source maps aren't in the same
	 *        directory, and the source map to be applied contains relative source
	 *        paths. If so, those relative source paths need to be rewritten
	 *        relative to the SourceMapGenerator.
	 */
	SourceMapGenerator.prototype.applySourceMap =
	  function SourceMapGenerator_applySourceMap(aSourceMapConsumer, aSourceFile, aSourceMapPath) {
	    var sourceFile = aSourceFile;
	    // If aSourceFile is omitted, we will use the file property of the SourceMap
	    if (aSourceFile == null) {
	      if (aSourceMapConsumer.file == null) {
	        throw new Error(
	          'SourceMapGenerator.prototype.applySourceMap requires either an explicit source file, ' +
	          'or the source map\'s "file" property. Both were omitted.'
	        );
	      }
	      sourceFile = aSourceMapConsumer.file;
	    }
	    var sourceRoot = this._sourceRoot;
	    // Make "sourceFile" relative if an absolute Url is passed.
	    if (sourceRoot != null) {
	      sourceFile = util.relative(sourceRoot, sourceFile);
	    }
	    // Applying the SourceMap can add and remove items from the sources and
	    // the names array.
	    var newSources = new ArraySet();
	    var newNames = new ArraySet();

	    // Find mappings for the "sourceFile"
	    this._mappings.unsortedForEach(function (mapping) {
	      if (mapping.source === sourceFile && mapping.originalLine != null) {
	        // Check if it can be mapped by the source map, then update the mapping.
	        var original = aSourceMapConsumer.originalPositionFor({
	          line: mapping.originalLine,
	          column: mapping.originalColumn
	        });
	        if (original.source != null) {
	          // Copy mapping
	          mapping.source = original.source;
	          if (aSourceMapPath != null) {
	            mapping.source = util.join(aSourceMapPath, mapping.source);
	          }
	          if (sourceRoot != null) {
	            mapping.source = util.relative(sourceRoot, mapping.source);
	          }
	          mapping.originalLine = original.line;
	          mapping.originalColumn = original.column;
	          if (original.name != null) {
	            mapping.name = original.name;
	          }
	        }
	      }

	      var source = mapping.source;
	      if (source != null && !newSources.has(source)) {
	        newSources.add(source);
	      }

	      var name = mapping.name;
	      if (name != null && !newNames.has(name)) {
	        newNames.add(name);
	      }

	    }, this);
	    this._sources = newSources;
	    this._names = newNames;

	    // Copy sourcesContents of applied map.
	    aSourceMapConsumer.sources.forEach(function (sourceFile) {
	      var content = aSourceMapConsumer.sourceContentFor(sourceFile);
	      if (content != null) {
	        if (aSourceMapPath != null) {
	          sourceFile = util.join(aSourceMapPath, sourceFile);
	        }
	        if (sourceRoot != null) {
	          sourceFile = util.relative(sourceRoot, sourceFile);
	        }
	        this.setSourceContent(sourceFile, content);
	      }
	    }, this);
	  };

	/**
	 * A mapping can have one of the three levels of data:
	 *
	 *   1. Just the generated position.
	 *   2. The Generated position, original position, and original source.
	 *   3. Generated and original position, original source, as well as a name
	 *      token.
	 *
	 * To maintain consistency, we validate that any new mapping being added falls
	 * in to one of these categories.
	 */
	SourceMapGenerator.prototype._validateMapping =
	  function SourceMapGenerator_validateMapping(aGenerated, aOriginal, aSource,
	                                              aName) {
	    // When aOriginal is truthy but has empty values for .line and .column,
	    // it is most likely a programmer error. In this case we throw a very
	    // specific error message to try to guide them the right way.
	    // For example: https://github.com/Polymer/polymer-bundler/pull/519
	    if (aOriginal && typeof aOriginal.line !== 'number' && typeof aOriginal.column !== 'number') {
	      var message = 'original.line and original.column are not numbers -- you probably meant to omit ' +
	      'the original mapping entirely and only map the generated position. If so, pass ' +
	      'null for the original mapping instead of an object with empty or null values.';

	      if (this._ignoreInvalidMapping) {
	        if (typeof console !== 'undefined' && console.warn) {
	          console.warn(message);
	        }
	        return false;
	      } else {
	        throw new Error(message);
	      }
	    }

	    if (aGenerated && 'line' in aGenerated && 'column' in aGenerated
	        && aGenerated.line > 0 && aGenerated.column >= 0
	        && !aOriginal && !aSource && !aName) {
	      // Case 1.
	      return;
	    }
	    else if (aGenerated && 'line' in aGenerated && 'column' in aGenerated
	             && aOriginal && 'line' in aOriginal && 'column' in aOriginal
	             && aGenerated.line > 0 && aGenerated.column >= 0
	             && aOriginal.line > 0 && aOriginal.column >= 0
	             && aSource) {
	      // Cases 2 and 3.
	      return;
	    }
	    else {
	      var message = 'Invalid mapping: ' + JSON.stringify({
	        generated: aGenerated,
	        source: aSource,
	        original: aOriginal,
	        name: aName
	      });

	      if (this._ignoreInvalidMapping) {
	        if (typeof console !== 'undefined' && console.warn) {
	          console.warn(message);
	        }
	        return false;
	      } else {
	        throw new Error(message)
	      }
	    }
	  };

	/**
	 * Serialize the accumulated mappings in to the stream of base 64 VLQs
	 * specified by the source map format.
	 */
	SourceMapGenerator.prototype._serializeMappings =
	  function SourceMapGenerator_serializeMappings() {
	    var previousGeneratedColumn = 0;
	    var previousGeneratedLine = 1;
	    var previousOriginalColumn = 0;
	    var previousOriginalLine = 0;
	    var previousName = 0;
	    var previousSource = 0;
	    var result = '';
	    var next;
	    var mapping;
	    var nameIdx;
	    var sourceIdx;

	    var mappings = this._mappings.toArray();
	    for (var i = 0, len = mappings.length; i < len; i++) {
	      mapping = mappings[i];
	      next = '';

	      if (mapping.generatedLine !== previousGeneratedLine) {
	        previousGeneratedColumn = 0;
	        while (mapping.generatedLine !== previousGeneratedLine) {
	          next += ';';
	          previousGeneratedLine++;
	        }
	      }
	      else {
	        if (i > 0) {
	          if (!util.compareByGeneratedPositionsInflated(mapping, mappings[i - 1])) {
	            continue;
	          }
	          next += ',';
	        }
	      }

	      next += base64VLQ.encode(mapping.generatedColumn
	                                 - previousGeneratedColumn);
	      previousGeneratedColumn = mapping.generatedColumn;

	      if (mapping.source != null) {
	        sourceIdx = this._sources.indexOf(mapping.source);
	        next += base64VLQ.encode(sourceIdx - previousSource);
	        previousSource = sourceIdx;

	        // lines are stored 0-based in SourceMap spec version 3
	        next += base64VLQ.encode(mapping.originalLine - 1
	                                   - previousOriginalLine);
	        previousOriginalLine = mapping.originalLine - 1;

	        next += base64VLQ.encode(mapping.originalColumn
	                                   - previousOriginalColumn);
	        previousOriginalColumn = mapping.originalColumn;

	        if (mapping.name != null) {
	          nameIdx = this._names.indexOf(mapping.name);
	          next += base64VLQ.encode(nameIdx - previousName);
	          previousName = nameIdx;
	        }
	      }

	      result += next;
	    }

	    return result;
	  };

	SourceMapGenerator.prototype._generateSourcesContent =
	  function SourceMapGenerator_generateSourcesContent(aSources, aSourceRoot) {
	    return aSources.map(function (source) {
	      if (!this._sourcesContents) {
	        return null;
	      }
	      if (aSourceRoot != null) {
	        source = util.relative(aSourceRoot, source);
	      }
	      var key = util.toSetString(source);
	      return Object.prototype.hasOwnProperty.call(this._sourcesContents, key)
	        ? this._sourcesContents[key]
	        : null;
	    }, this);
	  };

	/**
	 * Externalize the source map.
	 */
	SourceMapGenerator.prototype.toJSON =
	  function SourceMapGenerator_toJSON() {
	    var map = {
	      version: this._version,
	      sources: this._sources.toArray(),
	      names: this._names.toArray(),
	      mappings: this._serializeMappings()
	    };
	    if (this._file != null) {
	      map.file = this._file;
	    }
	    if (this._sourceRoot != null) {
	      map.sourceRoot = this._sourceRoot;
	    }
	    if (this._sourcesContents) {
	      map.sourcesContent = this._generateSourcesContent(map.sources, map.sourceRoot);
	    }

	    return map;
	  };

	/**
	 * Render the source map being generated to a string.
	 */
	SourceMapGenerator.prototype.toString =
	  function SourceMapGenerator_toString() {
	    return JSON.stringify(this.toJSON());
	  };

	sourceMapGenerator.SourceMapGenerator = SourceMapGenerator;
	return sourceMapGenerator;
}

var sourceMapConsumer = {};

var binarySearch = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredBinarySearch;

function requireBinarySearch () {
	if (hasRequiredBinarySearch) return binarySearch;
	hasRequiredBinarySearch = 1;
	(function (exports$1) {
		/*
		 * Copyright 2011 Mozilla Foundation and contributors
		 * Licensed under the New BSD license. See LICENSE or:
		 * http://opensource.org/licenses/BSD-3-Clause
		 */

		exports$1.GREATEST_LOWER_BOUND = 1;
		exports$1.LEAST_UPPER_BOUND = 2;

		/**
		 * Recursive implementation of binary search.
		 *
		 * @param aLow Indices here and lower do not contain the needle.
		 * @param aHigh Indices here and higher do not contain the needle.
		 * @param aNeedle The element being searched for.
		 * @param aHaystack The non-empty array being searched.
		 * @param aCompare Function which takes two elements and returns -1, 0, or 1.
		 * @param aBias Either 'binarySearch.GREATEST_LOWER_BOUND' or
		 *     'binarySearch.LEAST_UPPER_BOUND'. Specifies whether to return the
		 *     closest element that is smaller than or greater than the one we are
		 *     searching for, respectively, if the exact element cannot be found.
		 */
		function recursiveSearch(aLow, aHigh, aNeedle, aHaystack, aCompare, aBias) {
		  // This function terminates when one of the following is true:
		  //
		  //   1. We find the exact element we are looking for.
		  //
		  //   2. We did not find the exact element, but we can return the index of
		  //      the next-closest element.
		  //
		  //   3. We did not find the exact element, and there is no next-closest
		  //      element than the one we are searching for, so we return -1.
		  var mid = Math.floor((aHigh - aLow) / 2) + aLow;
		  var cmp = aCompare(aNeedle, aHaystack[mid], true);
		  if (cmp === 0) {
		    // Found the element we are looking for.
		    return mid;
		  }
		  else if (cmp > 0) {
		    // Our needle is greater than aHaystack[mid].
		    if (aHigh - mid > 1) {
		      // The element is in the upper half.
		      return recursiveSearch(mid, aHigh, aNeedle, aHaystack, aCompare, aBias);
		    }

		    // The exact needle element was not found in this haystack. Determine if
		    // we are in termination case (3) or (2) and return the appropriate thing.
		    if (aBias == exports$1.LEAST_UPPER_BOUND) {
		      return aHigh < aHaystack.length ? aHigh : -1;
		    } else {
		      return mid;
		    }
		  }
		  else {
		    // Our needle is less than aHaystack[mid].
		    if (mid - aLow > 1) {
		      // The element is in the lower half.
		      return recursiveSearch(aLow, mid, aNeedle, aHaystack, aCompare, aBias);
		    }

		    // we are in termination case (3) or (2) and return the appropriate thing.
		    if (aBias == exports$1.LEAST_UPPER_BOUND) {
		      return mid;
		    } else {
		      return aLow < 0 ? -1 : aLow;
		    }
		  }
		}

		/**
		 * This is an implementation of binary search which will always try and return
		 * the index of the closest element if there is no exact hit. This is because
		 * mappings between original and generated line/col pairs are single points,
		 * and there is an implicit region between each of them, so a miss just means
		 * that you aren't on the very start of a region.
		 *
		 * @param aNeedle The element you are looking for.
		 * @param aHaystack The array that is being searched.
		 * @param aCompare A function which takes the needle and an element in the
		 *     array and returns -1, 0, or 1 depending on whether the needle is less
		 *     than, equal to, or greater than the element, respectively.
		 * @param aBias Either 'binarySearch.GREATEST_LOWER_BOUND' or
		 *     'binarySearch.LEAST_UPPER_BOUND'. Specifies whether to return the
		 *     closest element that is smaller than or greater than the one we are
		 *     searching for, respectively, if the exact element cannot be found.
		 *     Defaults to 'binarySearch.GREATEST_LOWER_BOUND'.
		 */
		exports$1.search = function search(aNeedle, aHaystack, aCompare, aBias) {
		  if (aHaystack.length === 0) {
		    return -1;
		  }

		  var index = recursiveSearch(-1, aHaystack.length, aNeedle, aHaystack,
		                              aCompare, aBias || exports$1.GREATEST_LOWER_BOUND);
		  if (index < 0) {
		    return -1;
		  }

		  // We have found either the exact element, or the next-closest element than
		  // the one we are searching for. However, there may be more than one such
		  // element. Make sure we always return the smallest of these.
		  while (index - 1 >= 0) {
		    if (aCompare(aHaystack[index], aHaystack[index - 1], true) !== 0) {
		      break;
		    }
		    --index;
		  }

		  return index;
		}; 
	} (binarySearch));
	return binarySearch;
}

var quickSort = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredQuickSort;

function requireQuickSort () {
	if (hasRequiredQuickSort) return quickSort;
	hasRequiredQuickSort = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	// It turns out that some (most?) JavaScript engines don't self-host
	// `Array.prototype.sort`. This makes sense because C++ will likely remain
	// faster than JS when doing raw CPU-intensive sorting. However, when using a
	// custom comparator function, calling back and forth between the VM's C++ and
	// JIT'd JS is rather slow *and* loses JIT type information, resulting in
	// worse generated code for the comparator function than would be optimal. In
	// fact, when sorting with a comparator, these costs outweigh the benefits of
	// sorting in C++. By using our own JS-implemented Quick Sort (below), we get
	// a ~3500ms mean speed-up in `bench/bench.html`.

	function SortTemplate(comparator) {

	/**
	 * Swap the elements indexed by `x` and `y` in the array `ary`.
	 *
	 * @param {Array} ary
	 *        The array.
	 * @param {Number} x
	 *        The index of the first item.
	 * @param {Number} y
	 *        The index of the second item.
	 */
	function swap(ary, x, y) {
	  var temp = ary[x];
	  ary[x] = ary[y];
	  ary[y] = temp;
	}

	/**
	 * Returns a random integer within the range `low .. high` inclusive.
	 *
	 * @param {Number} low
	 *        The lower bound on the range.
	 * @param {Number} high
	 *        The upper bound on the range.
	 */
	function randomIntInRange(low, high) {
	  return Math.round(low + (Math.random() * (high - low)));
	}

	/**
	 * The Quick Sort algorithm.
	 *
	 * @param {Array} ary
	 *        An array to sort.
	 * @param {function} comparator
	 *        Function to use to compare two items.
	 * @param {Number} p
	 *        Start index of the array
	 * @param {Number} r
	 *        End index of the array
	 */
	function doQuickSort(ary, comparator, p, r) {
	  // If our lower bound is less than our upper bound, we (1) partition the
	  // array into two pieces and (2) recurse on each half. If it is not, this is
	  // the empty array and our base case.

	  if (p < r) {
	    // (1) Partitioning.
	    //
	    // The partitioning chooses a pivot between `p` and `r` and moves all
	    // elements that are less than or equal to the pivot to the before it, and
	    // all the elements that are greater than it after it. The effect is that
	    // once partition is done, the pivot is in the exact place it will be when
	    // the array is put in sorted order, and it will not need to be moved
	    // again. This runs in O(n) time.

	    // Always choose a random pivot so that an input array which is reverse
	    // sorted does not cause O(n^2) running time.
	    var pivotIndex = randomIntInRange(p, r);
	    var i = p - 1;

	    swap(ary, pivotIndex, r);
	    var pivot = ary[r];

	    // Immediately after `j` is incremented in this loop, the following hold
	    // true:
	    //
	    //   * Every element in `ary[p .. i]` is less than or equal to the pivot.
	    //
	    //   * Every element in `ary[i+1 .. j-1]` is greater than the pivot.
	    for (var j = p; j < r; j++) {
	      if (comparator(ary[j], pivot, false) <= 0) {
	        i += 1;
	        swap(ary, i, j);
	      }
	    }

	    swap(ary, i + 1, j);
	    var q = i + 1;

	    // (2) Recurse on each half.

	    doQuickSort(ary, comparator, p, q - 1);
	    doQuickSort(ary, comparator, q + 1, r);
	  }
	}

	  return doQuickSort;
	}

	function cloneSort(comparator) {
	  let template = SortTemplate.toString();
	  let templateFn = new Function(`return ${template}`)();
	  return templateFn(comparator);
	}

	/**
	 * Sort the given array in-place with the given comparator function.
	 *
	 * @param {Array} ary
	 *        An array to sort.
	 * @param {function} comparator
	 *        Function to use to compare two items.
	 */

	let sortCache = new WeakMap();
	quickSort.quickSort = function (ary, comparator, start = 0) {
	  let doQuickSort = sortCache.get(comparator);
	  if (doQuickSort === void 0) {
	    doQuickSort = cloneSort(comparator);
	    sortCache.set(comparator, doQuickSort);
	  }
	  doQuickSort(ary, comparator, start, ary.length - 1);
	};
	return quickSort;
}

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredSourceMapConsumer;

function requireSourceMapConsumer () {
	if (hasRequiredSourceMapConsumer) return sourceMapConsumer;
	hasRequiredSourceMapConsumer = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	var util = requireUtil();
	var binarySearch = requireBinarySearch();
	var ArraySet = requireArraySet().ArraySet;
	var base64VLQ = requireBase64Vlq();
	var quickSort = requireQuickSort().quickSort;

	function SourceMapConsumer(aSourceMap, aSourceMapURL) {
	  var sourceMap = aSourceMap;
	  if (typeof aSourceMap === 'string') {
	    sourceMap = util.parseSourceMapInput(aSourceMap);
	  }

	  return sourceMap.sections != null
	    ? new IndexedSourceMapConsumer(sourceMap, aSourceMapURL)
	    : new BasicSourceMapConsumer(sourceMap, aSourceMapURL);
	}

	SourceMapConsumer.fromSourceMap = function(aSourceMap, aSourceMapURL) {
	  return BasicSourceMapConsumer.fromSourceMap(aSourceMap, aSourceMapURL);
	};

	/**
	 * The version of the source mapping spec that we are consuming.
	 */
	SourceMapConsumer.prototype._version = 3;

	// `__generatedMappings` and `__originalMappings` are arrays that hold the
	// parsed mapping coordinates from the source map's "mappings" attribute. They
	// are lazily instantiated, accessed via the `_generatedMappings` and
	// `_originalMappings` getters respectively, and we only parse the mappings
	// and create these arrays once queried for a source location. We jump through
	// these hoops because there can be many thousands of mappings, and parsing
	// them is expensive, so we only want to do it if we must.
	//
	// Each object in the arrays is of the form:
	//
	//     {
	//       generatedLine: The line number in the generated code,
	//       generatedColumn: The column number in the generated code,
	//       source: The path to the original source file that generated this
	//               chunk of code,
	//       originalLine: The line number in the original source that
	//                     corresponds to this chunk of generated code,
	//       originalColumn: The column number in the original source that
	//                       corresponds to this chunk of generated code,
	//       name: The name of the original symbol which generated this chunk of
	//             code.
	//     }
	//
	// All properties except for `generatedLine` and `generatedColumn` can be
	// `null`.
	//
	// `_generatedMappings` is ordered by the generated positions.
	//
	// `_originalMappings` is ordered by the original positions.

	SourceMapConsumer.prototype.__generatedMappings = null;
	Object.defineProperty(SourceMapConsumer.prototype, '_generatedMappings', {
	  configurable: true,
	  enumerable: true,
	  get: function () {
	    if (!this.__generatedMappings) {
	      this._parseMappings(this._mappings, this.sourceRoot);
	    }

	    return this.__generatedMappings;
	  }
	});

	SourceMapConsumer.prototype.__originalMappings = null;
	Object.defineProperty(SourceMapConsumer.prototype, '_originalMappings', {
	  configurable: true,
	  enumerable: true,
	  get: function () {
	    if (!this.__originalMappings) {
	      this._parseMappings(this._mappings, this.sourceRoot);
	    }

	    return this.__originalMappings;
	  }
	});

	SourceMapConsumer.prototype._charIsMappingSeparator =
	  function SourceMapConsumer_charIsMappingSeparator(aStr, index) {
	    var c = aStr.charAt(index);
	    return c === ";" || c === ",";
	  };

	/**
	 * Parse the mappings in a string in to a data structure which we can easily
	 * query (the ordered arrays in the `this.__generatedMappings` and
	 * `this.__originalMappings` properties).
	 */
	SourceMapConsumer.prototype._parseMappings =
	  function SourceMapConsumer_parseMappings(aStr, aSourceRoot) {
	    throw new Error("Subclasses must implement _parseMappings");
	  };

	SourceMapConsumer.GENERATED_ORDER = 1;
	SourceMapConsumer.ORIGINAL_ORDER = 2;

	SourceMapConsumer.GREATEST_LOWER_BOUND = 1;
	SourceMapConsumer.LEAST_UPPER_BOUND = 2;

	/**
	 * Iterate over each mapping between an original source/line/column and a
	 * generated line/column in this source map.
	 *
	 * @param Function aCallback
	 *        The function that is called with each mapping.
	 * @param Object aContext
	 *        Optional. If specified, this object will be the value of `this` every
	 *        time that `aCallback` is called.
	 * @param aOrder
	 *        Either `SourceMapConsumer.GENERATED_ORDER` or
	 *        `SourceMapConsumer.ORIGINAL_ORDER`. Specifies whether you want to
	 *        iterate over the mappings sorted by the generated file's line/column
	 *        order or the original's source/line/column order, respectively. Defaults to
	 *        `SourceMapConsumer.GENERATED_ORDER`.
	 */
	SourceMapConsumer.prototype.eachMapping =
	  function SourceMapConsumer_eachMapping(aCallback, aContext, aOrder) {
	    var context = aContext || null;
	    var order = aOrder || SourceMapConsumer.GENERATED_ORDER;

	    var mappings;
	    switch (order) {
	    case SourceMapConsumer.GENERATED_ORDER:
	      mappings = this._generatedMappings;
	      break;
	    case SourceMapConsumer.ORIGINAL_ORDER:
	      mappings = this._originalMappings;
	      break;
	    default:
	      throw new Error("Unknown order of iteration.");
	    }

	    var sourceRoot = this.sourceRoot;
	    var boundCallback = aCallback.bind(context);
	    var names = this._names;
	    var sources = this._sources;
	    var sourceMapURL = this._sourceMapURL;

	    for (var i = 0, n = mappings.length; i < n; i++) {
	      var mapping = mappings[i];
	      var source = mapping.source === null ? null : sources.at(mapping.source);
	      if(source !== null) {
	        source = util.computeSourceURL(sourceRoot, source, sourceMapURL);
	      }
	      boundCallback({
	        source: source,
	        generatedLine: mapping.generatedLine,
	        generatedColumn: mapping.generatedColumn,
	        originalLine: mapping.originalLine,
	        originalColumn: mapping.originalColumn,
	        name: mapping.name === null ? null : names.at(mapping.name)
	      });
	    }
	  };

	/**
	 * Returns all generated line and column information for the original source,
	 * line, and column provided. If no column is provided, returns all mappings
	 * corresponding to a either the line we are searching for or the next
	 * closest line that has any mappings. Otherwise, returns all mappings
	 * corresponding to the given line and either the column we are searching for
	 * or the next closest column that has any offsets.
	 *
	 * The only argument is an object with the following properties:
	 *
	 *   - source: The filename of the original source.
	 *   - line: The line number in the original source.  The line number is 1-based.
	 *   - column: Optional. the column number in the original source.
	 *    The column number is 0-based.
	 *
	 * and an array of objects is returned, each with the following properties:
	 *
	 *   - line: The line number in the generated source, or null.  The
	 *    line number is 1-based.
	 *   - column: The column number in the generated source, or null.
	 *    The column number is 0-based.
	 */
	SourceMapConsumer.prototype.allGeneratedPositionsFor =
	  function SourceMapConsumer_allGeneratedPositionsFor(aArgs) {
	    var line = util.getArg(aArgs, 'line');

	    // When there is no exact match, BasicSourceMapConsumer.prototype._findMapping
	    // returns the index of the closest mapping less than the needle. By
	    // setting needle.originalColumn to 0, we thus find the last mapping for
	    // the given line, provided such a mapping exists.
	    var needle = {
	      source: util.getArg(aArgs, 'source'),
	      originalLine: line,
	      originalColumn: util.getArg(aArgs, 'column', 0)
	    };

	    needle.source = this._findSourceIndex(needle.source);
	    if (needle.source < 0) {
	      return [];
	    }

	    var mappings = [];

	    var index = this._findMapping(needle,
	                                  this._originalMappings,
	                                  "originalLine",
	                                  "originalColumn",
	                                  util.compareByOriginalPositions,
	                                  binarySearch.LEAST_UPPER_BOUND);
	    if (index >= 0) {
	      var mapping = this._originalMappings[index];

	      if (aArgs.column === undefined) {
	        var originalLine = mapping.originalLine;

	        // Iterate until either we run out of mappings, or we run into
	        // a mapping for a different line than the one we found. Since
	        // mappings are sorted, this is guaranteed to find all mappings for
	        // the line we found.
	        while (mapping && mapping.originalLine === originalLine) {
	          mappings.push({
	            line: util.getArg(mapping, 'generatedLine', null),
	            column: util.getArg(mapping, 'generatedColumn', null),
	            lastColumn: util.getArg(mapping, 'lastGeneratedColumn', null)
	          });

	          mapping = this._originalMappings[++index];
	        }
	      } else {
	        var originalColumn = mapping.originalColumn;

	        // Iterate until either we run out of mappings, or we run into
	        // a mapping for a different line than the one we were searching for.
	        // Since mappings are sorted, this is guaranteed to find all mappings for
	        // the line we are searching for.
	        while (mapping &&
	               mapping.originalLine === line &&
	               mapping.originalColumn == originalColumn) {
	          mappings.push({
	            line: util.getArg(mapping, 'generatedLine', null),
	            column: util.getArg(mapping, 'generatedColumn', null),
	            lastColumn: util.getArg(mapping, 'lastGeneratedColumn', null)
	          });

	          mapping = this._originalMappings[++index];
	        }
	      }
	    }

	    return mappings;
	  };

	sourceMapConsumer.SourceMapConsumer = SourceMapConsumer;

	/**
	 * A BasicSourceMapConsumer instance represents a parsed source map which we can
	 * query for information about the original file positions by giving it a file
	 * position in the generated source.
	 *
	 * The first parameter is the raw source map (either as a JSON string, or
	 * already parsed to an object). According to the spec, source maps have the
	 * following attributes:
	 *
	 *   - version: Which version of the source map spec this map is following.
	 *   - sources: An array of URLs to the original source files.
	 *   - names: An array of identifiers which can be referrenced by individual mappings.
	 *   - sourceRoot: Optional. The URL root from which all sources are relative.
	 *   - sourcesContent: Optional. An array of contents of the original source files.
	 *   - mappings: A string of base64 VLQs which contain the actual mappings.
	 *   - file: Optional. The generated file this source map is associated with.
	 *
	 * Here is an example source map, taken from the source map spec[0]:
	 *
	 *     {
	 *       version : 3,
	 *       file: "out.js",
	 *       sourceRoot : "",
	 *       sources: ["foo.js", "bar.js"],
	 *       names: ["src", "maps", "are", "fun"],
	 *       mappings: "AA,AB;;ABCDE;"
	 *     }
	 *
	 * The second parameter, if given, is a string whose value is the URL
	 * at which the source map was found.  This URL is used to compute the
	 * sources array.
	 *
	 * [0]: https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit?pli=1#
	 */
	function BasicSourceMapConsumer(aSourceMap, aSourceMapURL) {
	  var sourceMap = aSourceMap;
	  if (typeof aSourceMap === 'string') {
	    sourceMap = util.parseSourceMapInput(aSourceMap);
	  }

	  var version = util.getArg(sourceMap, 'version');
	  var sources = util.getArg(sourceMap, 'sources');
	  // Sass 3.3 leaves out the 'names' array, so we deviate from the spec (which
	  // requires the array) to play nice here.
	  var names = util.getArg(sourceMap, 'names', []);
	  var sourceRoot = util.getArg(sourceMap, 'sourceRoot', null);
	  var sourcesContent = util.getArg(sourceMap, 'sourcesContent', null);
	  var mappings = util.getArg(sourceMap, 'mappings');
	  var file = util.getArg(sourceMap, 'file', null);

	  // Once again, Sass deviates from the spec and supplies the version as a
	  // string rather than a number, so we use loose equality checking here.
	  if (version != this._version) {
	    throw new Error('Unsupported version: ' + version);
	  }

	  if (sourceRoot) {
	    sourceRoot = util.normalize(sourceRoot);
	  }

	  sources = sources
	    .map(String)
	    // Some source maps produce relative source paths like "./foo.js" instead of
	    // "foo.js".  Normalize these first so that future comparisons will succeed.
	    // See bugzil.la/1090768.
	    .map(util.normalize)
	    // Always ensure that absolute sources are internally stored relative to
	    // the source root, if the source root is absolute. Not doing this would
	    // be particularly problematic when the source root is a prefix of the
	    // source (valid, but why??). See github issue #199 and bugzil.la/1188982.
	    .map(function (source) {
	      return sourceRoot && util.isAbsolute(sourceRoot) && util.isAbsolute(source)
	        ? util.relative(sourceRoot, source)
	        : source;
	    });

	  // Pass `true` below to allow duplicate names and sources. While source maps
	  // are intended to be compressed and deduplicated, the TypeScript compiler
	  // sometimes generates source maps with duplicates in them. See Github issue
	  // #72 and bugzil.la/889492.
	  this._names = ArraySet.fromArray(names.map(String), true);
	  this._sources = ArraySet.fromArray(sources, true);

	  this._absoluteSources = this._sources.toArray().map(function (s) {
	    return util.computeSourceURL(sourceRoot, s, aSourceMapURL);
	  });

	  this.sourceRoot = sourceRoot;
	  this.sourcesContent = sourcesContent;
	  this._mappings = mappings;
	  this._sourceMapURL = aSourceMapURL;
	  this.file = file;
	}

	BasicSourceMapConsumer.prototype = Object.create(SourceMapConsumer.prototype);
	BasicSourceMapConsumer.prototype.consumer = SourceMapConsumer;

	/**
	 * Utility function to find the index of a source.  Returns -1 if not
	 * found.
	 */
	BasicSourceMapConsumer.prototype._findSourceIndex = function(aSource) {
	  var relativeSource = aSource;
	  if (this.sourceRoot != null) {
	    relativeSource = util.relative(this.sourceRoot, relativeSource);
	  }

	  if (this._sources.has(relativeSource)) {
	    return this._sources.indexOf(relativeSource);
	  }

	  // Maybe aSource is an absolute URL as returned by |sources|.  In
	  // this case we can't simply undo the transform.
	  var i;
	  for (i = 0; i < this._absoluteSources.length; ++i) {
	    if (this._absoluteSources[i] == aSource) {
	      return i;
	    }
	  }

	  return -1;
	};

	/**
	 * Create a BasicSourceMapConsumer from a SourceMapGenerator.
	 *
	 * @param SourceMapGenerator aSourceMap
	 *        The source map that will be consumed.
	 * @param String aSourceMapURL
	 *        The URL at which the source map can be found (optional)
	 * @returns BasicSourceMapConsumer
	 */
	BasicSourceMapConsumer.fromSourceMap =
	  function SourceMapConsumer_fromSourceMap(aSourceMap, aSourceMapURL) {
	    var smc = Object.create(BasicSourceMapConsumer.prototype);

	    var names = smc._names = ArraySet.fromArray(aSourceMap._names.toArray(), true);
	    var sources = smc._sources = ArraySet.fromArray(aSourceMap._sources.toArray(), true);
	    smc.sourceRoot = aSourceMap._sourceRoot;
	    smc.sourcesContent = aSourceMap._generateSourcesContent(smc._sources.toArray(),
	                                                            smc.sourceRoot);
	    smc.file = aSourceMap._file;
	    smc._sourceMapURL = aSourceMapURL;
	    smc._absoluteSources = smc._sources.toArray().map(function (s) {
	      return util.computeSourceURL(smc.sourceRoot, s, aSourceMapURL);
	    });

	    // Because we are modifying the entries (by converting string sources and
	    // names to indices into the sources and names ArraySets), we have to make
	    // a copy of the entry or else bad things happen. Shared mutable state
	    // strikes again! See github issue #191.

	    var generatedMappings = aSourceMap._mappings.toArray().slice();
	    var destGeneratedMappings = smc.__generatedMappings = [];
	    var destOriginalMappings = smc.__originalMappings = [];

	    for (var i = 0, length = generatedMappings.length; i < length; i++) {
	      var srcMapping = generatedMappings[i];
	      var destMapping = new Mapping;
	      destMapping.generatedLine = srcMapping.generatedLine;
	      destMapping.generatedColumn = srcMapping.generatedColumn;

	      if (srcMapping.source) {
	        destMapping.source = sources.indexOf(srcMapping.source);
	        destMapping.originalLine = srcMapping.originalLine;
	        destMapping.originalColumn = srcMapping.originalColumn;

	        if (srcMapping.name) {
	          destMapping.name = names.indexOf(srcMapping.name);
	        }

	        destOriginalMappings.push(destMapping);
	      }

	      destGeneratedMappings.push(destMapping);
	    }

	    quickSort(smc.__originalMappings, util.compareByOriginalPositions);

	    return smc;
	  };

	/**
	 * The version of the source mapping spec that we are consuming.
	 */
	BasicSourceMapConsumer.prototype._version = 3;

	/**
	 * The list of original sources.
	 */
	Object.defineProperty(BasicSourceMapConsumer.prototype, 'sources', {
	  get: function () {
	    return this._absoluteSources.slice();
	  }
	});

	/**
	 * Provide the JIT with a nice shape / hidden class.
	 */
	function Mapping() {
	  this.generatedLine = 0;
	  this.generatedColumn = 0;
	  this.source = null;
	  this.originalLine = null;
	  this.originalColumn = null;
	  this.name = null;
	}

	/**
	 * Parse the mappings in a string in to a data structure which we can easily
	 * query (the ordered arrays in the `this.__generatedMappings` and
	 * `this.__originalMappings` properties).
	 */

	const compareGenerated = util.compareByGeneratedPositionsDeflatedNoLine;
	function sortGenerated(array, start) {
	  let l = array.length;
	  let n = array.length - start;
	  if (n <= 1) {
	    return;
	  } else if (n == 2) {
	    let a = array[start];
	    let b = array[start + 1];
	    if (compareGenerated(a, b) > 0) {
	      array[start] = b;
	      array[start + 1] = a;
	    }
	  } else if (n < 20) {
	    for (let i = start; i < l; i++) {
	      for (let j = i; j > start; j--) {
	        let a = array[j - 1];
	        let b = array[j];
	        if (compareGenerated(a, b) <= 0) {
	          break;
	        }
	        array[j - 1] = b;
	        array[j] = a;
	      }
	    }
	  } else {
	    quickSort(array, compareGenerated, start);
	  }
	}
	BasicSourceMapConsumer.prototype._parseMappings =
	  function SourceMapConsumer_parseMappings(aStr, aSourceRoot) {
	    var generatedLine = 1;
	    var previousGeneratedColumn = 0;
	    var previousOriginalLine = 0;
	    var previousOriginalColumn = 0;
	    var previousSource = 0;
	    var previousName = 0;
	    var length = aStr.length;
	    var index = 0;
	    var temp = {};
	    var originalMappings = [];
	    var generatedMappings = [];
	    var mapping, segment, end, value;

	    let subarrayStart = 0;
	    while (index < length) {
	      if (aStr.charAt(index) === ';') {
	        generatedLine++;
	        index++;
	        previousGeneratedColumn = 0;

	        sortGenerated(generatedMappings, subarrayStart);
	        subarrayStart = generatedMappings.length;
	      }
	      else if (aStr.charAt(index) === ',') {
	        index++;
	      }
	      else {
	        mapping = new Mapping();
	        mapping.generatedLine = generatedLine;

	        for (end = index; end < length; end++) {
	          if (this._charIsMappingSeparator(aStr, end)) {
	            break;
	          }
	        }
	        aStr.slice(index, end);

	        segment = [];
	        while (index < end) {
	          base64VLQ.decode(aStr, index, temp);
	          value = temp.value;
	          index = temp.rest;
	          segment.push(value);
	        }

	        if (segment.length === 2) {
	          throw new Error('Found a source, but no line and column');
	        }

	        if (segment.length === 3) {
	          throw new Error('Found a source and line, but no column');
	        }

	        // Generated column.
	        mapping.generatedColumn = previousGeneratedColumn + segment[0];
	        previousGeneratedColumn = mapping.generatedColumn;

	        if (segment.length > 1) {
	          // Original source.
	          mapping.source = previousSource + segment[1];
	          previousSource += segment[1];

	          // Original line.
	          mapping.originalLine = previousOriginalLine + segment[2];
	          previousOriginalLine = mapping.originalLine;
	          // Lines are stored 0-based
	          mapping.originalLine += 1;

	          // Original column.
	          mapping.originalColumn = previousOriginalColumn + segment[3];
	          previousOriginalColumn = mapping.originalColumn;

	          if (segment.length > 4) {
	            // Original name.
	            mapping.name = previousName + segment[4];
	            previousName += segment[4];
	          }
	        }

	        generatedMappings.push(mapping);
	        if (typeof mapping.originalLine === 'number') {
	          let currentSource = mapping.source;
	          while (originalMappings.length <= currentSource) {
	            originalMappings.push(null);
	          }
	          if (originalMappings[currentSource] === null) {
	            originalMappings[currentSource] = [];
	          }
	          originalMappings[currentSource].push(mapping);
	        }
	      }
	    }

	    sortGenerated(generatedMappings, subarrayStart);
	    this.__generatedMappings = generatedMappings;

	    for (var i = 0; i < originalMappings.length; i++) {
	      if (originalMappings[i] != null) {
	        quickSort(originalMappings[i], util.compareByOriginalPositionsNoSource);
	      }
	    }
	    this.__originalMappings = [].concat(...originalMappings);
	  };

	/**
	 * Find the mapping that best matches the hypothetical "needle" mapping that
	 * we are searching for in the given "haystack" of mappings.
	 */
	BasicSourceMapConsumer.prototype._findMapping =
	  function SourceMapConsumer_findMapping(aNeedle, aMappings, aLineName,
	                                         aColumnName, aComparator, aBias) {
	    // To return the position we are searching for, we must first find the
	    // mapping for the given position and then return the opposite position it
	    // points to. Because the mappings are sorted, we can use binary search to
	    // find the best mapping.

	    if (aNeedle[aLineName] <= 0) {
	      throw new TypeError('Line must be greater than or equal to 1, got '
	                          + aNeedle[aLineName]);
	    }
	    if (aNeedle[aColumnName] < 0) {
	      throw new TypeError('Column must be greater than or equal to 0, got '
	                          + aNeedle[aColumnName]);
	    }

	    return binarySearch.search(aNeedle, aMappings, aComparator, aBias);
	  };

	/**
	 * Compute the last column for each generated mapping. The last column is
	 * inclusive.
	 */
	BasicSourceMapConsumer.prototype.computeColumnSpans =
	  function SourceMapConsumer_computeColumnSpans() {
	    for (var index = 0; index < this._generatedMappings.length; ++index) {
	      var mapping = this._generatedMappings[index];

	      // Mappings do not contain a field for the last generated columnt. We
	      // can come up with an optimistic estimate, however, by assuming that
	      // mappings are contiguous (i.e. given two consecutive mappings, the
	      // first mapping ends where the second one starts).
	      if (index + 1 < this._generatedMappings.length) {
	        var nextMapping = this._generatedMappings[index + 1];

	        if (mapping.generatedLine === nextMapping.generatedLine) {
	          mapping.lastGeneratedColumn = nextMapping.generatedColumn - 1;
	          continue;
	        }
	      }

	      // The last mapping for each line spans the entire line.
	      mapping.lastGeneratedColumn = Infinity;
	    }
	  };

	/**
	 * Returns the original source, line, and column information for the generated
	 * source's line and column positions provided. The only argument is an object
	 * with the following properties:
	 *
	 *   - line: The line number in the generated source.  The line number
	 *     is 1-based.
	 *   - column: The column number in the generated source.  The column
	 *     number is 0-based.
	 *   - bias: Either 'SourceMapConsumer.GREATEST_LOWER_BOUND' or
	 *     'SourceMapConsumer.LEAST_UPPER_BOUND'. Specifies whether to return the
	 *     closest element that is smaller than or greater than the one we are
	 *     searching for, respectively, if the exact element cannot be found.
	 *     Defaults to 'SourceMapConsumer.GREATEST_LOWER_BOUND'.
	 *
	 * and an object is returned with the following properties:
	 *
	 *   - source: The original source file, or null.
	 *   - line: The line number in the original source, or null.  The
	 *     line number is 1-based.
	 *   - column: The column number in the original source, or null.  The
	 *     column number is 0-based.
	 *   - name: The original identifier, or null.
	 */
	BasicSourceMapConsumer.prototype.originalPositionFor =
	  function SourceMapConsumer_originalPositionFor(aArgs) {
	    var needle = {
	      generatedLine: util.getArg(aArgs, 'line'),
	      generatedColumn: util.getArg(aArgs, 'column')
	    };

	    var index = this._findMapping(
	      needle,
	      this._generatedMappings,
	      "generatedLine",
	      "generatedColumn",
	      util.compareByGeneratedPositionsDeflated,
	      util.getArg(aArgs, 'bias', SourceMapConsumer.GREATEST_LOWER_BOUND)
	    );

	    if (index >= 0) {
	      var mapping = this._generatedMappings[index];

	      if (mapping.generatedLine === needle.generatedLine) {
	        var source = util.getArg(mapping, 'source', null);
	        if (source !== null) {
	          source = this._sources.at(source);
	          source = util.computeSourceURL(this.sourceRoot, source, this._sourceMapURL);
	        }
	        var name = util.getArg(mapping, 'name', null);
	        if (name !== null) {
	          name = this._names.at(name);
	        }
	        return {
	          source: source,
	          line: util.getArg(mapping, 'originalLine', null),
	          column: util.getArg(mapping, 'originalColumn', null),
	          name: name
	        };
	      }
	    }

	    return {
	      source: null,
	      line: null,
	      column: null,
	      name: null
	    };
	  };

	/**
	 * Return true if we have the source content for every source in the source
	 * map, false otherwise.
	 */
	BasicSourceMapConsumer.prototype.hasContentsOfAllSources =
	  function BasicSourceMapConsumer_hasContentsOfAllSources() {
	    if (!this.sourcesContent) {
	      return false;
	    }
	    return this.sourcesContent.length >= this._sources.size() &&
	      !this.sourcesContent.some(function (sc) { return sc == null; });
	  };

	/**
	 * Returns the original source content. The only argument is the url of the
	 * original source file. Returns null if no original source content is
	 * available.
	 */
	BasicSourceMapConsumer.prototype.sourceContentFor =
	  function SourceMapConsumer_sourceContentFor(aSource, nullOnMissing) {
	    if (!this.sourcesContent) {
	      return null;
	    }

	    var index = this._findSourceIndex(aSource);
	    if (index >= 0) {
	      return this.sourcesContent[index];
	    }

	    var relativeSource = aSource;
	    if (this.sourceRoot != null) {
	      relativeSource = util.relative(this.sourceRoot, relativeSource);
	    }

	    var url;
	    if (this.sourceRoot != null
	        && (url = util.urlParse(this.sourceRoot))) {
	      // XXX: file:// URIs and absolute paths lead to unexpected behavior for
	      // many users. We can help them out when they expect file:// URIs to
	      // behave like it would if they were running a local HTTP server. See
	      // https://bugzilla.mozilla.org/show_bug.cgi?id=885597.
	      var fileUriAbsPath = relativeSource.replace(/^file:\/\//, "");
	      if (url.scheme == "file"
	          && this._sources.has(fileUriAbsPath)) {
	        return this.sourcesContent[this._sources.indexOf(fileUriAbsPath)]
	      }

	      if ((!url.path || url.path == "/")
	          && this._sources.has("/" + relativeSource)) {
	        return this.sourcesContent[this._sources.indexOf("/" + relativeSource)];
	      }
	    }

	    // This function is used recursively from
	    // IndexedSourceMapConsumer.prototype.sourceContentFor. In that case, we
	    // don't want to throw if we can't find the source - we just want to
	    // return null, so we provide a flag to exit gracefully.
	    if (nullOnMissing) {
	      return null;
	    }
	    else {
	      throw new Error('"' + relativeSource + '" is not in the SourceMap.');
	    }
	  };

	/**
	 * Returns the generated line and column information for the original source,
	 * line, and column positions provided. The only argument is an object with
	 * the following properties:
	 *
	 *   - source: The filename of the original source.
	 *   - line: The line number in the original source.  The line number
	 *     is 1-based.
	 *   - column: The column number in the original source.  The column
	 *     number is 0-based.
	 *   - bias: Either 'SourceMapConsumer.GREATEST_LOWER_BOUND' or
	 *     'SourceMapConsumer.LEAST_UPPER_BOUND'. Specifies whether to return the
	 *     closest element that is smaller than or greater than the one we are
	 *     searching for, respectively, if the exact element cannot be found.
	 *     Defaults to 'SourceMapConsumer.GREATEST_LOWER_BOUND'.
	 *
	 * and an object is returned with the following properties:
	 *
	 *   - line: The line number in the generated source, or null.  The
	 *     line number is 1-based.
	 *   - column: The column number in the generated source, or null.
	 *     The column number is 0-based.
	 */
	BasicSourceMapConsumer.prototype.generatedPositionFor =
	  function SourceMapConsumer_generatedPositionFor(aArgs) {
	    var source = util.getArg(aArgs, 'source');
	    source = this._findSourceIndex(source);
	    if (source < 0) {
	      return {
	        line: null,
	        column: null,
	        lastColumn: null
	      };
	    }

	    var needle = {
	      source: source,
	      originalLine: util.getArg(aArgs, 'line'),
	      originalColumn: util.getArg(aArgs, 'column')
	    };

	    var index = this._findMapping(
	      needle,
	      this._originalMappings,
	      "originalLine",
	      "originalColumn",
	      util.compareByOriginalPositions,
	      util.getArg(aArgs, 'bias', SourceMapConsumer.GREATEST_LOWER_BOUND)
	    );

	    if (index >= 0) {
	      var mapping = this._originalMappings[index];

	      if (mapping.source === needle.source) {
	        return {
	          line: util.getArg(mapping, 'generatedLine', null),
	          column: util.getArg(mapping, 'generatedColumn', null),
	          lastColumn: util.getArg(mapping, 'lastGeneratedColumn', null)
	        };
	      }
	    }

	    return {
	      line: null,
	      column: null,
	      lastColumn: null
	    };
	  };

	sourceMapConsumer.BasicSourceMapConsumer = BasicSourceMapConsumer;

	/**
	 * An IndexedSourceMapConsumer instance represents a parsed source map which
	 * we can query for information. It differs from BasicSourceMapConsumer in
	 * that it takes "indexed" source maps (i.e. ones with a "sections" field) as
	 * input.
	 *
	 * The first parameter is a raw source map (either as a JSON string, or already
	 * parsed to an object). According to the spec for indexed source maps, they
	 * have the following attributes:
	 *
	 *   - version: Which version of the source map spec this map is following.
	 *   - file: Optional. The generated file this source map is associated with.
	 *   - sections: A list of section definitions.
	 *
	 * Each value under the "sections" field has two fields:
	 *   - offset: The offset into the original specified at which this section
	 *       begins to apply, defined as an object with a "line" and "column"
	 *       field.
	 *   - map: A source map definition. This source map could also be indexed,
	 *       but doesn't have to be.
	 *
	 * Instead of the "map" field, it's also possible to have a "url" field
	 * specifying a URL to retrieve a source map from, but that's currently
	 * unsupported.
	 *
	 * Here's an example source map, taken from the source map spec[0], but
	 * modified to omit a section which uses the "url" field.
	 *
	 *  {
	 *    version : 3,
	 *    file: "app.js",
	 *    sections: [{
	 *      offset: {line:100, column:10},
	 *      map: {
	 *        version : 3,
	 *        file: "section.js",
	 *        sources: ["foo.js", "bar.js"],
	 *        names: ["src", "maps", "are", "fun"],
	 *        mappings: "AAAA,E;;ABCDE;"
	 *      }
	 *    }],
	 *  }
	 *
	 * The second parameter, if given, is a string whose value is the URL
	 * at which the source map was found.  This URL is used to compute the
	 * sources array.
	 *
	 * [0]: https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#heading=h.535es3xeprgt
	 */
	function IndexedSourceMapConsumer(aSourceMap, aSourceMapURL) {
	  var sourceMap = aSourceMap;
	  if (typeof aSourceMap === 'string') {
	    sourceMap = util.parseSourceMapInput(aSourceMap);
	  }

	  var version = util.getArg(sourceMap, 'version');
	  var sections = util.getArg(sourceMap, 'sections');

	  if (version != this._version) {
	    throw new Error('Unsupported version: ' + version);
	  }

	  this._sources = new ArraySet();
	  this._names = new ArraySet();

	  var lastOffset = {
	    line: -1,
	    column: 0
	  };
	  this._sections = sections.map(function (s) {
	    if (s.url) {
	      // The url field will require support for asynchronicity.
	      // See https://github.com/mozilla/source-map/issues/16
	      throw new Error('Support for url field in sections not implemented.');
	    }
	    var offset = util.getArg(s, 'offset');
	    var offsetLine = util.getArg(offset, 'line');
	    var offsetColumn = util.getArg(offset, 'column');

	    if (offsetLine < lastOffset.line ||
	        (offsetLine === lastOffset.line && offsetColumn < lastOffset.column)) {
	      throw new Error('Section offsets must be ordered and non-overlapping.');
	    }
	    lastOffset = offset;

	    return {
	      generatedOffset: {
	        // The offset fields are 0-based, but we use 1-based indices when
	        // encoding/decoding from VLQ.
	        generatedLine: offsetLine + 1,
	        generatedColumn: offsetColumn + 1
	      },
	      consumer: new SourceMapConsumer(util.getArg(s, 'map'), aSourceMapURL)
	    }
	  });
	}

	IndexedSourceMapConsumer.prototype = Object.create(SourceMapConsumer.prototype);
	IndexedSourceMapConsumer.prototype.constructor = SourceMapConsumer;

	/**
	 * The version of the source mapping spec that we are consuming.
	 */
	IndexedSourceMapConsumer.prototype._version = 3;

	/**
	 * The list of original sources.
	 */
	Object.defineProperty(IndexedSourceMapConsumer.prototype, 'sources', {
	  get: function () {
	    var sources = [];
	    for (var i = 0; i < this._sections.length; i++) {
	      for (var j = 0; j < this._sections[i].consumer.sources.length; j++) {
	        sources.push(this._sections[i].consumer.sources[j]);
	      }
	    }
	    return sources;
	  }
	});

	/**
	 * Returns the original source, line, and column information for the generated
	 * source's line and column positions provided. The only argument is an object
	 * with the following properties:
	 *
	 *   - line: The line number in the generated source.  The line number
	 *     is 1-based.
	 *   - column: The column number in the generated source.  The column
	 *     number is 0-based.
	 *
	 * and an object is returned with the following properties:
	 *
	 *   - source: The original source file, or null.
	 *   - line: The line number in the original source, or null.  The
	 *     line number is 1-based.
	 *   - column: The column number in the original source, or null.  The
	 *     column number is 0-based.
	 *   - name: The original identifier, or null.
	 */
	IndexedSourceMapConsumer.prototype.originalPositionFor =
	  function IndexedSourceMapConsumer_originalPositionFor(aArgs) {
	    var needle = {
	      generatedLine: util.getArg(aArgs, 'line'),
	      generatedColumn: util.getArg(aArgs, 'column')
	    };

	    // Find the section containing the generated position we're trying to map
	    // to an original position.
	    var sectionIndex = binarySearch.search(needle, this._sections,
	      function(needle, section) {
	        var cmp = needle.generatedLine - section.generatedOffset.generatedLine;
	        if (cmp) {
	          return cmp;
	        }

	        return (needle.generatedColumn -
	                section.generatedOffset.generatedColumn);
	      });
	    var section = this._sections[sectionIndex];

	    if (!section) {
	      return {
	        source: null,
	        line: null,
	        column: null,
	        name: null
	      };
	    }

	    return section.consumer.originalPositionFor({
	      line: needle.generatedLine -
	        (section.generatedOffset.generatedLine - 1),
	      column: needle.generatedColumn -
	        (section.generatedOffset.generatedLine === needle.generatedLine
	         ? section.generatedOffset.generatedColumn - 1
	         : 0),
	      bias: aArgs.bias
	    });
	  };

	/**
	 * Return true if we have the source content for every source in the source
	 * map, false otherwise.
	 */
	IndexedSourceMapConsumer.prototype.hasContentsOfAllSources =
	  function IndexedSourceMapConsumer_hasContentsOfAllSources() {
	    return this._sections.every(function (s) {
	      return s.consumer.hasContentsOfAllSources();
	    });
	  };

	/**
	 * Returns the original source content. The only argument is the url of the
	 * original source file. Returns null if no original source content is
	 * available.
	 */
	IndexedSourceMapConsumer.prototype.sourceContentFor =
	  function IndexedSourceMapConsumer_sourceContentFor(aSource, nullOnMissing) {
	    for (var i = 0; i < this._sections.length; i++) {
	      var section = this._sections[i];

	      var content = section.consumer.sourceContentFor(aSource, true);
	      if (content || content === '') {
	        return content;
	      }
	    }
	    if (nullOnMissing) {
	      return null;
	    }
	    else {
	      throw new Error('"' + aSource + '" is not in the SourceMap.');
	    }
	  };

	/**
	 * Returns the generated line and column information for the original source,
	 * line, and column positions provided. The only argument is an object with
	 * the following properties:
	 *
	 *   - source: The filename of the original source.
	 *   - line: The line number in the original source.  The line number
	 *     is 1-based.
	 *   - column: The column number in the original source.  The column
	 *     number is 0-based.
	 *
	 * and an object is returned with the following properties:
	 *
	 *   - line: The line number in the generated source, or null.  The
	 *     line number is 1-based. 
	 *   - column: The column number in the generated source, or null.
	 *     The column number is 0-based.
	 */
	IndexedSourceMapConsumer.prototype.generatedPositionFor =
	  function IndexedSourceMapConsumer_generatedPositionFor(aArgs) {
	    for (var i = 0; i < this._sections.length; i++) {
	      var section = this._sections[i];

	      // Only consider this section if the requested source is in the list of
	      // sources of the consumer.
	      if (section.consumer._findSourceIndex(util.getArg(aArgs, 'source')) === -1) {
	        continue;
	      }
	      var generatedPosition = section.consumer.generatedPositionFor(aArgs);
	      if (generatedPosition) {
	        var ret = {
	          line: generatedPosition.line +
	            (section.generatedOffset.generatedLine - 1),
	          column: generatedPosition.column +
	            (section.generatedOffset.generatedLine === generatedPosition.line
	             ? section.generatedOffset.generatedColumn - 1
	             : 0)
	        };
	        return ret;
	      }
	    }

	    return {
	      line: null,
	      column: null
	    };
	  };

	/**
	 * Parse the mappings in a string in to a data structure which we can easily
	 * query (the ordered arrays in the `this.__generatedMappings` and
	 * `this.__originalMappings` properties).
	 */
	IndexedSourceMapConsumer.prototype._parseMappings =
	  function IndexedSourceMapConsumer_parseMappings(aStr, aSourceRoot) {
	    this.__generatedMappings = [];
	    this.__originalMappings = [];
	    for (var i = 0; i < this._sections.length; i++) {
	      var section = this._sections[i];
	      var sectionMappings = section.consumer._generatedMappings;
	      for (var j = 0; j < sectionMappings.length; j++) {
	        var mapping = sectionMappings[j];

	        var source = section.consumer._sources.at(mapping.source);
	        if(source !== null) {
	          source = util.computeSourceURL(section.consumer.sourceRoot, source, this._sourceMapURL);
	        }
	        this._sources.add(source);
	        source = this._sources.indexOf(source);

	        var name = null;
	        if (mapping.name) {
	          name = section.consumer._names.at(mapping.name);
	          this._names.add(name);
	          name = this._names.indexOf(name);
	        }

	        // The mappings coming from the consumer for the section have
	        // generated positions relative to the start of the section, so we
	        // need to offset them to be relative to the start of the concatenated
	        // generated file.
	        var adjustedMapping = {
	          source: source,
	          generatedLine: mapping.generatedLine +
	            (section.generatedOffset.generatedLine - 1),
	          generatedColumn: mapping.generatedColumn +
	            (section.generatedOffset.generatedLine === mapping.generatedLine
	            ? section.generatedOffset.generatedColumn - 1
	            : 0),
	          originalLine: mapping.originalLine,
	          originalColumn: mapping.originalColumn,
	          name: name
	        };

	        this.__generatedMappings.push(adjustedMapping);
	        if (typeof adjustedMapping.originalLine === 'number') {
	          this.__originalMappings.push(adjustedMapping);
	        }
	      }
	    }

	    quickSort(this.__generatedMappings, util.compareByGeneratedPositionsDeflated);
	    quickSort(this.__originalMappings, util.compareByOriginalPositions);
	  };

	sourceMapConsumer.IndexedSourceMapConsumer = IndexedSourceMapConsumer;
	return sourceMapConsumer;
}

var sourceNode = {};

/* -*- Mode: js; js-indent-level: 2; -*- */

var hasRequiredSourceNode;

function requireSourceNode () {
	if (hasRequiredSourceNode) return sourceNode;
	hasRequiredSourceNode = 1;
	/*
	 * Copyright 2011 Mozilla Foundation and contributors
	 * Licensed under the New BSD license. See LICENSE or:
	 * http://opensource.org/licenses/BSD-3-Clause
	 */

	var SourceMapGenerator = requireSourceMapGenerator().SourceMapGenerator;
	var util = requireUtil();

	// Matches a Windows-style `\r\n` newline or a `\n` newline used by all other
	// operating systems these days (capturing the result).
	var REGEX_NEWLINE = /(\r?\n)/;

	// Newline character code for charCodeAt() comparisons
	var NEWLINE_CODE = 10;

	// Private symbol for identifying `SourceNode`s when multiple versions of
	// the source-map library are loaded. This MUST NOT CHANGE across
	// versions!
	var isSourceNode = "$$$isSourceNode$$$";

	/**
	 * SourceNodes provide a way to abstract over interpolating/concatenating
	 * snippets of generated JavaScript source code while maintaining the line and
	 * column information associated with the original source code.
	 *
	 * @param aLine The original line number.
	 * @param aColumn The original column number.
	 * @param aSource The original source's filename.
	 * @param aChunks Optional. An array of strings which are snippets of
	 *        generated JS, or other SourceNodes.
	 * @param aName The original identifier.
	 */
	function SourceNode(aLine, aColumn, aSource, aChunks, aName) {
	  this.children = [];
	  this.sourceContents = {};
	  this.line = aLine == null ? null : aLine;
	  this.column = aColumn == null ? null : aColumn;
	  this.source = aSource == null ? null : aSource;
	  this.name = aName == null ? null : aName;
	  this[isSourceNode] = true;
	  if (aChunks != null) this.add(aChunks);
	}

	/**
	 * Creates a SourceNode from generated code and a SourceMapConsumer.
	 *
	 * @param aGeneratedCode The generated code
	 * @param aSourceMapConsumer The SourceMap for the generated code
	 * @param aRelativePath Optional. The path that relative sources in the
	 *        SourceMapConsumer should be relative to.
	 */
	SourceNode.fromStringWithSourceMap =
	  function SourceNode_fromStringWithSourceMap(aGeneratedCode, aSourceMapConsumer, aRelativePath) {
	    // The SourceNode we want to fill with the generated code
	    // and the SourceMap
	    var node = new SourceNode();

	    // All even indices of this array are one line of the generated code,
	    // while all odd indices are the newlines between two adjacent lines
	    // (since `REGEX_NEWLINE` captures its match).
	    // Processed fragments are accessed by calling `shiftNextLine`.
	    var remainingLines = aGeneratedCode.split(REGEX_NEWLINE);
	    var remainingLinesIndex = 0;
	    var shiftNextLine = function() {
	      var lineContents = getNextLine();
	      // The last line of a file might not have a newline.
	      var newLine = getNextLine() || "";
	      return lineContents + newLine;

	      function getNextLine() {
	        return remainingLinesIndex < remainingLines.length ?
	            remainingLines[remainingLinesIndex++] : undefined;
	      }
	    };

	    // We need to remember the position of "remainingLines"
	    var lastGeneratedLine = 1, lastGeneratedColumn = 0;

	    // The generate SourceNodes we need a code range.
	    // To extract it current and last mapping is used.
	    // Here we store the last mapping.
	    var lastMapping = null;

	    aSourceMapConsumer.eachMapping(function (mapping) {
	      if (lastMapping !== null) {
	        // We add the code from "lastMapping" to "mapping":
	        // First check if there is a new line in between.
	        if (lastGeneratedLine < mapping.generatedLine) {
	          // Associate first line with "lastMapping"
	          addMappingWithCode(lastMapping, shiftNextLine());
	          lastGeneratedLine++;
	          lastGeneratedColumn = 0;
	          // The remaining code is added without mapping
	        } else {
	          // There is no new line in between.
	          // Associate the code between "lastGeneratedColumn" and
	          // "mapping.generatedColumn" with "lastMapping"
	          var nextLine = remainingLines[remainingLinesIndex] || '';
	          var code = nextLine.substr(0, mapping.generatedColumn -
	                                        lastGeneratedColumn);
	          remainingLines[remainingLinesIndex] = nextLine.substr(mapping.generatedColumn -
	                                              lastGeneratedColumn);
	          lastGeneratedColumn = mapping.generatedColumn;
	          addMappingWithCode(lastMapping, code);
	          // No more remaining code, continue
	          lastMapping = mapping;
	          return;
	        }
	      }
	      // We add the generated code until the first mapping
	      // to the SourceNode without any mapping.
	      // Each line is added as separate string.
	      while (lastGeneratedLine < mapping.generatedLine) {
	        node.add(shiftNextLine());
	        lastGeneratedLine++;
	      }
	      if (lastGeneratedColumn < mapping.generatedColumn) {
	        var nextLine = remainingLines[remainingLinesIndex] || '';
	        node.add(nextLine.substr(0, mapping.generatedColumn));
	        remainingLines[remainingLinesIndex] = nextLine.substr(mapping.generatedColumn);
	        lastGeneratedColumn = mapping.generatedColumn;
	      }
	      lastMapping = mapping;
	    }, this);
	    // We have processed all mappings.
	    if (remainingLinesIndex < remainingLines.length) {
	      if (lastMapping) {
	        // Associate the remaining code in the current line with "lastMapping"
	        addMappingWithCode(lastMapping, shiftNextLine());
	      }
	      // and add the remaining lines without any mapping
	      node.add(remainingLines.splice(remainingLinesIndex).join(""));
	    }

	    // Copy sourcesContent into SourceNode
	    aSourceMapConsumer.sources.forEach(function (sourceFile) {
	      var content = aSourceMapConsumer.sourceContentFor(sourceFile);
	      if (content != null) {
	        if (aRelativePath != null) {
	          sourceFile = util.join(aRelativePath, sourceFile);
	        }
	        node.setSourceContent(sourceFile, content);
	      }
	    });

	    return node;

	    function addMappingWithCode(mapping, code) {
	      if (mapping === null || mapping.source === undefined) {
	        node.add(code);
	      } else {
	        var source = aRelativePath
	          ? util.join(aRelativePath, mapping.source)
	          : mapping.source;
	        node.add(new SourceNode(mapping.originalLine,
	                                mapping.originalColumn,
	                                source,
	                                code,
	                                mapping.name));
	      }
	    }
	  };

	/**
	 * Add a chunk of generated JS to this source node.
	 *
	 * @param aChunk A string snippet of generated JS code, another instance of
	 *        SourceNode, or an array where each member is one of those things.
	 */
	SourceNode.prototype.add = function SourceNode_add(aChunk) {
	  if (Array.isArray(aChunk)) {
	    aChunk.forEach(function (chunk) {
	      this.add(chunk);
	    }, this);
	  }
	  else if (aChunk[isSourceNode] || typeof aChunk === "string") {
	    if (aChunk) {
	      this.children.push(aChunk);
	    }
	  }
	  else {
	    throw new TypeError(
	      "Expected a SourceNode, string, or an array of SourceNodes and strings. Got " + aChunk
	    );
	  }
	  return this;
	};

	/**
	 * Add a chunk of generated JS to the beginning of this source node.
	 *
	 * @param aChunk A string snippet of generated JS code, another instance of
	 *        SourceNode, or an array where each member is one of those things.
	 */
	SourceNode.prototype.prepend = function SourceNode_prepend(aChunk) {
	  if (Array.isArray(aChunk)) {
	    for (var i = aChunk.length-1; i >= 0; i--) {
	      this.prepend(aChunk[i]);
	    }
	  }
	  else if (aChunk[isSourceNode] || typeof aChunk === "string") {
	    this.children.unshift(aChunk);
	  }
	  else {
	    throw new TypeError(
	      "Expected a SourceNode, string, or an array of SourceNodes and strings. Got " + aChunk
	    );
	  }
	  return this;
	};

	/**
	 * Walk over the tree of JS snippets in this node and its children. The
	 * walking function is called once for each snippet of JS and is passed that
	 * snippet and the its original associated source's line/column location.
	 *
	 * @param aFn The traversal function.
	 */
	SourceNode.prototype.walk = function SourceNode_walk(aFn) {
	  var chunk;
	  for (var i = 0, len = this.children.length; i < len; i++) {
	    chunk = this.children[i];
	    if (chunk[isSourceNode]) {
	      chunk.walk(aFn);
	    }
	    else {
	      if (chunk !== '') {
	        aFn(chunk, { source: this.source,
	                     line: this.line,
	                     column: this.column,
	                     name: this.name });
	      }
	    }
	  }
	};

	/**
	 * Like `String.prototype.join` except for SourceNodes. Inserts `aStr` between
	 * each of `this.children`.
	 *
	 * @param aSep The separator.
	 */
	SourceNode.prototype.join = function SourceNode_join(aSep) {
	  var newChildren;
	  var i;
	  var len = this.children.length;
	  if (len > 0) {
	    newChildren = [];
	    for (i = 0; i < len-1; i++) {
	      newChildren.push(this.children[i]);
	      newChildren.push(aSep);
	    }
	    newChildren.push(this.children[i]);
	    this.children = newChildren;
	  }
	  return this;
	};

	/**
	 * Call String.prototype.replace on the very right-most source snippet. Useful
	 * for trimming whitespace from the end of a source node, etc.
	 *
	 * @param aPattern The pattern to replace.
	 * @param aReplacement The thing to replace the pattern with.
	 */
	SourceNode.prototype.replaceRight = function SourceNode_replaceRight(aPattern, aReplacement) {
	  var lastChild = this.children[this.children.length - 1];
	  if (lastChild[isSourceNode]) {
	    lastChild.replaceRight(aPattern, aReplacement);
	  }
	  else if (typeof lastChild === 'string') {
	    this.children[this.children.length - 1] = lastChild.replace(aPattern, aReplacement);
	  }
	  else {
	    this.children.push(''.replace(aPattern, aReplacement));
	  }
	  return this;
	};

	/**
	 * Set the source content for a source file. This will be added to the SourceMapGenerator
	 * in the sourcesContent field.
	 *
	 * @param aSourceFile The filename of the source file
	 * @param aSourceContent The content of the source file
	 */
	SourceNode.prototype.setSourceContent =
	  function SourceNode_setSourceContent(aSourceFile, aSourceContent) {
	    this.sourceContents[util.toSetString(aSourceFile)] = aSourceContent;
	  };

	/**
	 * Walk over the tree of SourceNodes. The walking function is called for each
	 * source file content and is passed the filename and source content.
	 *
	 * @param aFn The traversal function.
	 */
	SourceNode.prototype.walkSourceContents =
	  function SourceNode_walkSourceContents(aFn) {
	    for (var i = 0, len = this.children.length; i < len; i++) {
	      if (this.children[i][isSourceNode]) {
	        this.children[i].walkSourceContents(aFn);
	      }
	    }

	    var sources = Object.keys(this.sourceContents);
	    for (var i = 0, len = sources.length; i < len; i++) {
	      aFn(util.fromSetString(sources[i]), this.sourceContents[sources[i]]);
	    }
	  };

	/**
	 * Return the string representation of this source node. Walks over the tree
	 * and concatenates all the various snippets together to one string.
	 */
	SourceNode.prototype.toString = function SourceNode_toString() {
	  var str = "";
	  this.walk(function (chunk) {
	    str += chunk;
	  });
	  return str;
	};

	/**
	 * Returns the string representation of this source node along with a source
	 * map.
	 */
	SourceNode.prototype.toStringWithSourceMap = function SourceNode_toStringWithSourceMap(aArgs) {
	  var generated = {
	    code: "",
	    line: 1,
	    column: 0
	  };
	  var map = new SourceMapGenerator(aArgs);
	  var sourceMappingActive = false;
	  var lastOriginalSource = null;
	  var lastOriginalLine = null;
	  var lastOriginalColumn = null;
	  var lastOriginalName = null;
	  this.walk(function (chunk, original) {
	    generated.code += chunk;
	    if (original.source !== null
	        && original.line !== null
	        && original.column !== null) {
	      if(lastOriginalSource !== original.source
	         || lastOriginalLine !== original.line
	         || lastOriginalColumn !== original.column
	         || lastOriginalName !== original.name) {
	        map.addMapping({
	          source: original.source,
	          original: {
	            line: original.line,
	            column: original.column
	          },
	          generated: {
	            line: generated.line,
	            column: generated.column
	          },
	          name: original.name
	        });
	      }
	      lastOriginalSource = original.source;
	      lastOriginalLine = original.line;
	      lastOriginalColumn = original.column;
	      lastOriginalName = original.name;
	      sourceMappingActive = true;
	    } else if (sourceMappingActive) {
	      map.addMapping({
	        generated: {
	          line: generated.line,
	          column: generated.column
	        }
	      });
	      lastOriginalSource = null;
	      sourceMappingActive = false;
	    }
	    for (var idx = 0, length = chunk.length; idx < length; idx++) {
	      if (chunk.charCodeAt(idx) === NEWLINE_CODE) {
	        generated.line++;
	        generated.column = 0;
	        // Mappings end at eol
	        if (idx + 1 === length) {
	          lastOriginalSource = null;
	          sourceMappingActive = false;
	        } else if (sourceMappingActive) {
	          map.addMapping({
	            source: original.source,
	            original: {
	              line: original.line,
	              column: original.column
	            },
	            generated: {
	              line: generated.line,
	              column: generated.column
	            },
	            name: original.name
	          });
	        }
	      } else {
	        generated.column++;
	      }
	    }
	  });
	  this.walkSourceContents(function (sourceFile, sourceContent) {
	    map.setSourceContent(sourceFile, sourceContent);
	  });

	  return { code: generated.code, map: map };
	};

	sourceNode.SourceNode = SourceNode;
	return sourceNode;
}

/*
 * Copyright 2009-2011 Mozilla Foundation and contributors
 * Licensed under the New BSD license. See LICENSE.txt or:
 * http://opensource.org/licenses/BSD-3-Clause
 */

var hasRequiredSourceMap;

function requireSourceMap () {
	if (hasRequiredSourceMap) return sourceMap;
	hasRequiredSourceMap = 1;
	sourceMap.SourceMapGenerator = requireSourceMapGenerator().SourceMapGenerator;
	sourceMap.SourceMapConsumer = requireSourceMapConsumer().SourceMapConsumer;
	sourceMap.SourceNode = requireSourceNode().SourceNode;
	return sourceMap;
}

var previousMap;
var hasRequiredPreviousMap;

function requirePreviousMap () {
	if (hasRequiredPreviousMap) return previousMap;
	hasRequiredPreviousMap = 1;

	let { existsSync, readFileSync } = require$$0;
	let { dirname, join } = require$$1;
	let { SourceMapConsumer, SourceMapGenerator } = requireSourceMap();

	function fromBase64(str) {
	  if (Buffer) {
	    return Buffer.from(str, 'base64').toString()
	  } else {
	    /* c8 ignore next 2 */
	    return window.atob(str)
	  }
	}

	class PreviousMap {
	  constructor(css, opts) {
	    if (opts.map === false) return
	    this.loadAnnotation(css);
	    this.inline = this.startWith(this.annotation, 'data:');

	    let prev = opts.map ? opts.map.prev : undefined;
	    let text = this.loadMap(opts.from, prev);
	    if (!this.mapFile && opts.from) {
	      this.mapFile = opts.from;
	    }
	    if (this.mapFile) this.root = dirname(this.mapFile);
	    if (text) this.text = text;
	  }

	  consumer() {
	    if (!this.consumerCache) {
	      this.consumerCache = new SourceMapConsumer(this.text);
	    }
	    return this.consumerCache
	  }

	  decodeInline(text) {
	    let baseCharsetUri = /^data:application\/json;charset=utf-?8;base64,/;
	    let baseUri = /^data:application\/json;base64,/;
	    let charsetUri = /^data:application\/json;charset=utf-?8,/;
	    let uri = /^data:application\/json,/;

	    let uriMatch = text.match(charsetUri) || text.match(uri);
	    if (uriMatch) {
	      return decodeURIComponent(text.substr(uriMatch[0].length))
	    }

	    let baseUriMatch = text.match(baseCharsetUri) || text.match(baseUri);
	    if (baseUriMatch) {
	      return fromBase64(text.substr(baseUriMatch[0].length))
	    }

	    let encoding = text.match(/data:application\/json;([^,]+),/)[1];
	    throw new Error('Unsupported source map encoding ' + encoding)
	  }

	  getAnnotationURL(sourceMapString) {
	    return sourceMapString.replace(/^\/\*\s*# sourceMappingURL=/, '').trim()
	  }

	  isMap(map) {
	    if (typeof map !== 'object') return false
	    return (
	      typeof map.mappings === 'string' ||
	      typeof map._mappings === 'string' ||
	      Array.isArray(map.sections)
	    )
	  }

	  loadAnnotation(css) {
	    let comments = css.match(/\/\*\s*# sourceMappingURL=/g);
	    if (!comments) return

	    // sourceMappingURLs from comments, strings, etc.
	    let start = css.lastIndexOf(comments.pop());
	    let end = css.indexOf('*/', start);

	    if (start > -1 && end > -1) {
	      // Locate the last sourceMappingURL to avoid pickin
	      this.annotation = this.getAnnotationURL(css.substring(start, end));
	    }
	  }

	  loadFile(path) {
	    this.root = dirname(path);
	    if (existsSync(path)) {
	      this.mapFile = path;
	      return readFileSync(path, 'utf-8').toString().trim()
	    }
	  }

	  loadMap(file, prev) {
	    if (prev === false) return false

	    if (prev) {
	      if (typeof prev === 'string') {
	        return prev
	      } else if (typeof prev === 'function') {
	        let prevPath = prev(file);
	        if (prevPath) {
	          let map = this.loadFile(prevPath);
	          if (!map) {
	            throw new Error(
	              'Unable to load previous source map: ' + prevPath.toString()
	            )
	          }
	          return map
	        }
	      } else if (prev instanceof SourceMapConsumer) {
	        return SourceMapGenerator.fromSourceMap(prev).toString()
	      } else if (prev instanceof SourceMapGenerator) {
	        return prev.toString()
	      } else if (this.isMap(prev)) {
	        return JSON.stringify(prev)
	      } else {
	        throw new Error(
	          'Unsupported previous source map format: ' + prev.toString()
	        )
	      }
	    } else if (this.inline) {
	      return this.decodeInline(this.annotation)
	    } else if (this.annotation) {
	      let map = this.annotation;
	      if (file) map = join(dirname(file), map);
	      return this.loadFile(map)
	    }
	  }

	  startWith(string, start) {
	    if (!string) return false
	    return string.substr(0, start.length) === start
	  }

	  withContent() {
	    return !!(
	      this.consumer().sourcesContent &&
	      this.consumer().sourcesContent.length > 0
	    )
	  }
	}

	previousMap = PreviousMap;
	PreviousMap.default = PreviousMap;
	return previousMap;
}

var input;
var hasRequiredInput;

function requireInput () {
	if (hasRequiredInput) return input;
	hasRequiredInput = 1;

	let { nanoid } = /*@__PURE__*/ requireNonSecure();
	let { isAbsolute, resolve } = require$$1;
	let { SourceMapConsumer, SourceMapGenerator } = requireSourceMap();
	let { fileURLToPath, pathToFileURL } = require$$3;

	let CssSyntaxError = requireCssSyntaxError();
	let PreviousMap = requirePreviousMap();
	let terminalHighlight = requireTerminalHighlight();

	let lineToIndexCache = Symbol('lineToIndexCache');

	let sourceMapAvailable = Boolean(SourceMapConsumer && SourceMapGenerator);
	let pathAvailable = Boolean(resolve && isAbsolute);

	function getLineToIndex(input) {
	  if (input[lineToIndexCache]) return input[lineToIndexCache]
	  let lines = input.css.split('\n');
	  let lineToIndex = new Array(lines.length);
	  let prevIndex = 0;

	  for (let i = 0, l = lines.length; i < l; i++) {
	    lineToIndex[i] = prevIndex;
	    prevIndex += lines[i].length + 1;
	  }

	  input[lineToIndexCache] = lineToIndex;
	  return lineToIndex
	}

	class Input {
	  get from() {
	    return this.file || this.id
	  }

	  constructor(css, opts = {}) {
	    if (
	      css === null ||
	      typeof css === 'undefined' ||
	      (typeof css === 'object' && !css.toString)
	    ) {
	      throw new Error(`PostCSS received ${css} instead of CSS string`)
	    }

	    this.css = css.toString();

	    if (this.css[0] === '\uFEFF' || this.css[0] === '\uFFFE') {
	      this.hasBOM = true;
	      this.css = this.css.slice(1);
	    } else {
	      this.hasBOM = false;
	    }

	    this.document = this.css;
	    if (opts.document) this.document = opts.document.toString();

	    if (opts.from) {
	      if (
	        !pathAvailable ||
	        /^\w+:\/\//.test(opts.from) ||
	        isAbsolute(opts.from)
	      ) {
	        this.file = opts.from;
	      } else {
	        this.file = resolve(opts.from);
	      }
	    }

	    if (pathAvailable && sourceMapAvailable) {
	      let map = new PreviousMap(this.css, opts);
	      if (map.text) {
	        this.map = map;
	        let file = map.consumer().file;
	        if (!this.file && file) this.file = this.mapResolve(file);
	      }
	    }

	    if (!this.file) {
	      this.id = '<input css ' + nanoid(6) + '>';
	    }
	    if (this.map) this.map.file = this.from;
	  }

	  error(message, line, column, opts = {}) {
	    let endColumn, endLine, endOffset, offset, result;

	    if (line && typeof line === 'object') {
	      let start = line;
	      let end = column;
	      if (typeof start.offset === 'number') {
	        offset = start.offset;
	        let pos = this.fromOffset(offset);
	        line = pos.line;
	        column = pos.col;
	      } else {
	        line = start.line;
	        column = start.column;
	        offset = this.fromLineAndColumn(line, column);
	      }
	      if (typeof end.offset === 'number') {
	        endOffset = end.offset;
	        let pos = this.fromOffset(endOffset);
	        endLine = pos.line;
	        endColumn = pos.col;
	      } else {
	        endLine = end.line;
	        endColumn = end.column;
	        endOffset = this.fromLineAndColumn(end.line, end.column);
	      }
	    } else if (!column) {
	      offset = line;
	      let pos = this.fromOffset(offset);
	      line = pos.line;
	      column = pos.col;
	    } else {
	      offset = this.fromLineAndColumn(line, column);
	    }

	    let origin = this.origin(line, column, endLine, endColumn);
	    if (origin) {
	      result = new CssSyntaxError(
	        message,
	        origin.endLine === undefined
	          ? origin.line
	          : { column: origin.column, line: origin.line },
	        origin.endLine === undefined
	          ? origin.column
	          : { column: origin.endColumn, line: origin.endLine },
	        origin.source,
	        origin.file,
	        opts.plugin
	      );
	    } else {
	      result = new CssSyntaxError(
	        message,
	        endLine === undefined ? line : { column, line },
	        endLine === undefined ? column : { column: endColumn, line: endLine },
	        this.css,
	        this.file,
	        opts.plugin
	      );
	    }

	    result.input = { column, endColumn, endLine, endOffset, line, offset, source: this.css };
	    if (this.file) {
	      if (pathToFileURL) {
	        result.input.url = pathToFileURL(this.file).toString();
	      }
	      result.input.file = this.file;
	    }

	    return result
	  }

	  fromLineAndColumn(line, column) {
	    let lineToIndex = getLineToIndex(this);
	    let index = lineToIndex[line - 1];
	    return index + column - 1
	  }

	  fromOffset(offset) {
	    let lineToIndex = getLineToIndex(this);
	    let lastLine = lineToIndex[lineToIndex.length - 1];

	    let min = 0;
	    if (offset >= lastLine) {
	      min = lineToIndex.length - 1;
	    } else {
	      let max = lineToIndex.length - 2;
	      let mid;
	      while (min < max) {
	        mid = min + ((max - min) >> 1);
	        if (offset < lineToIndex[mid]) {
	          max = mid - 1;
	        } else if (offset >= lineToIndex[mid + 1]) {
	          min = mid + 1;
	        } else {
	          min = mid;
	          break
	        }
	      }
	    }
	    return {
	      col: offset - lineToIndex[min] + 1,
	      line: min + 1
	    }
	  }

	  mapResolve(file) {
	    if (/^\w+:\/\//.test(file)) {
	      return file
	    }
	    return resolve(this.map.consumer().sourceRoot || this.map.root || '.', file)
	  }

	  origin(line, column, endLine, endColumn) {
	    if (!this.map) return false
	    let consumer = this.map.consumer();

	    let from = consumer.originalPositionFor({ column, line });
	    if (!from.source) return false

	    let to;
	    if (typeof endLine === 'number') {
	      to = consumer.originalPositionFor({ column: endColumn, line: endLine });
	    }

	    let fromUrl;

	    if (isAbsolute(from.source)) {
	      fromUrl = pathToFileURL(from.source);
	    } else {
	      fromUrl = new URL(
	        from.source,
	        this.map.consumer().sourceRoot || pathToFileURL(this.map.mapFile)
	      );
	    }

	    let result = {
	      column: from.column,
	      endColumn: to && to.column,
	      endLine: to && to.line,
	      line: from.line,
	      url: fromUrl.toString()
	    };

	    if (fromUrl.protocol === 'file:') {
	      if (fileURLToPath) {
	        result.file = fileURLToPath(fromUrl);
	      } else {
	        /* c8 ignore next 2 */
	        throw new Error(`file: protocol is not available in this PostCSS build`)
	      }
	    }

	    let source = consumer.sourceContentFor(from.source);
	    if (source) result.source = source;

	    return result
	  }

	  toJSON() {
	    let json = {};
	    for (let name of ['hasBOM', 'css', 'file', 'id']) {
	      if (this[name] != null) {
	        json[name] = this[name];
	      }
	    }
	    if (this.map) {
	      json.map = { ...this.map };
	      if (json.map.consumerCache) {
	        json.map.consumerCache = undefined;
	      }
	    }
	    return json
	  }
	}

	input = Input;
	Input.default = Input;

	if (terminalHighlight && terminalHighlight.registerInput) {
	  terminalHighlight.registerInput(Input);
	}
	return input;
}

var root;
var hasRequiredRoot;

function requireRoot () {
	if (hasRequiredRoot) return root;
	hasRequiredRoot = 1;

	let Container = requireContainer();

	let LazyResult, Processor;

	class Root extends Container {
	  constructor(defaults) {
	    super(defaults);
	    this.type = 'root';
	    if (!this.nodes) this.nodes = [];
	  }

	  normalize(child, sample, type) {
	    let nodes = super.normalize(child);

	    if (sample) {
	      if (type === 'prepend') {
	        if (this.nodes.length > 1) {
	          sample.raws.before = this.nodes[1].raws.before;
	        } else {
	          delete sample.raws.before;
	        }
	      } else if (this.first !== sample) {
	        for (let node of nodes) {
	          node.raws.before = sample.raws.before;
	        }
	      }
	    }

	    return nodes
	  }

	  removeChild(child, ignore) {
	    let index = this.index(child);

	    if (!ignore && index === 0 && this.nodes.length > 1) {
	      this.nodes[1].raws.before = this.nodes[index].raws.before;
	    }

	    return super.removeChild(child)
	  }

	  toResult(opts = {}) {
	    let lazy = new LazyResult(new Processor(), this, opts);
	    return lazy.stringify()
	  }
	}

	Root.registerLazyResult = dependant => {
	  LazyResult = dependant;
	};

	Root.registerProcessor = dependant => {
	  Processor = dependant;
	};

	root = Root;
	Root.default = Root;

	Container.registerRoot(Root);
	return root;
}

var list_1;
var hasRequiredList;

function requireList () {
	if (hasRequiredList) return list_1;
	hasRequiredList = 1;

	let list = {
	  comma(string) {
	    return list.split(string, [','], true)
	  },

	  space(string) {
	    let spaces = [' ', '\n', '\t'];
	    return list.split(string, spaces)
	  },

	  split(string, separators, last) {
	    let array = [];
	    let current = '';
	    let split = false;

	    let func = 0;
	    let inQuote = false;
	    let prevQuote = '';
	    let escape = false;

	    for (let letter of string) {
	      if (escape) {
	        escape = false;
	      } else if (letter === '\\') {
	        escape = true;
	      } else if (inQuote) {
	        if (letter === prevQuote) {
	          inQuote = false;
	        }
	      } else if (letter === '"' || letter === "'") {
	        inQuote = true;
	        prevQuote = letter;
	      } else if (letter === '(') {
	        func += 1;
	      } else if (letter === ')') {
	        if (func > 0) func -= 1;
	      } else if (func === 0) {
	        if (separators.includes(letter)) split = true;
	      }

	      if (split) {
	        if (current !== '') array.push(current.trim());
	        current = '';
	        split = false;
	      } else {
	        current += letter;
	      }
	    }

	    if (last || current !== '') array.push(current.trim());
	    return array
	  }
	};

	list_1 = list;
	list.default = list;
	return list_1;
}

var rule;
var hasRequiredRule;

function requireRule () {
	if (hasRequiredRule) return rule;
	hasRequiredRule = 1;

	let Container = requireContainer();
	let list = requireList();

	class Rule extends Container {
	  get selectors() {
	    return list.comma(this.selector)
	  }

	  set selectors(values) {
	    let match = this.selector ? this.selector.match(/,\s*/) : null;
	    let sep = match ? match[0] : ',' + this.raw('between', 'beforeOpen');
	    this.selector = values.join(sep);
	  }

	  constructor(defaults) {
	    super(defaults);
	    this.type = 'rule';
	    if (!this.nodes) this.nodes = [];
	  }
	}

	rule = Rule;
	Rule.default = Rule;

	Container.registerRule(Rule);
	return rule;
}

var fromJSON_1;
var hasRequiredFromJSON;

function requireFromJSON () {
	if (hasRequiredFromJSON) return fromJSON_1;
	hasRequiredFromJSON = 1;

	let AtRule = requireAtRule();
	let Comment = requireComment();
	let Declaration = requireDeclaration();
	let Input = requireInput();
	let PreviousMap = requirePreviousMap();
	let Root = requireRoot();
	let Rule = requireRule();

	function fromJSON(json, inputs) {
	  if (Array.isArray(json)) return json.map(n => fromJSON(n))

	  let { inputs: ownInputs, ...defaults } = json;
	  if (ownInputs) {
	    inputs = [];
	    for (let input of ownInputs) {
	      let inputHydrated = { ...input, __proto__: Input.prototype };
	      if (inputHydrated.map) {
	        inputHydrated.map = {
	          ...inputHydrated.map,
	          __proto__: PreviousMap.prototype
	        };
	      }
	      inputs.push(inputHydrated);
	    }
	  }
	  if (defaults.nodes) {
	    defaults.nodes = json.nodes.map(n => fromJSON(n, inputs));
	  }
	  if (defaults.source) {
	    let { inputId, ...source } = defaults.source;
	    defaults.source = source;
	    if (inputId != null) {
	      defaults.source.input = inputs[inputId];
	    }
	  }
	  if (defaults.type === 'root') {
	    return new Root(defaults)
	  } else if (defaults.type === 'decl') {
	    return new Declaration(defaults)
	  } else if (defaults.type === 'rule') {
	    return new Rule(defaults)
	  } else if (defaults.type === 'comment') {
	    return new Comment(defaults)
	  } else if (defaults.type === 'atrule') {
	    return new AtRule(defaults)
	  } else {
	    throw new Error('Unknown node type: ' + json.type)
	  }
	}

	fromJSON_1 = fromJSON;
	fromJSON.default = fromJSON;
	return fromJSON_1;
}

var mapGenerator;
var hasRequiredMapGenerator;

function requireMapGenerator () {
	if (hasRequiredMapGenerator) return mapGenerator;
	hasRequiredMapGenerator = 1;

	let { dirname, relative, resolve, sep } = require$$1;
	let { SourceMapConsumer, SourceMapGenerator } = requireSourceMap();
	let { pathToFileURL } = require$$3;

	let Input = requireInput();

	let sourceMapAvailable = Boolean(SourceMapConsumer && SourceMapGenerator);
	let pathAvailable = Boolean(dirname && resolve && relative && sep);

	class MapGenerator {
	  constructor(stringify, root, opts, cssString) {
	    this.stringify = stringify;
	    this.mapOpts = opts.map || {};
	    this.root = root;
	    this.opts = opts;
	    this.css = cssString;
	    this.originalCSS = cssString;
	    this.usesFileUrls = !this.mapOpts.from && this.mapOpts.absolute;

	    this.memoizedFileURLs = new Map();
	    this.memoizedPaths = new Map();
	    this.memoizedURLs = new Map();
	  }

	  addAnnotation() {
	    let content;

	    if (this.isInline()) {
	      content =
	        'data:application/json;base64,' + this.toBase64(this.map.toString());
	    } else if (typeof this.mapOpts.annotation === 'string') {
	      content = this.mapOpts.annotation;
	    } else if (typeof this.mapOpts.annotation === 'function') {
	      content = this.mapOpts.annotation(this.opts.to, this.root);
	    } else {
	      content = this.outputFile() + '.map';
	    }
	    let eol = '\n';
	    if (this.css.includes('\r\n')) eol = '\r\n';

	    this.css += eol + '/*# sourceMappingURL=' + content + ' */';
	  }

	  applyPrevMaps() {
	    for (let prev of this.previous()) {
	      let from = this.toUrl(this.path(prev.file));
	      let root = prev.root || dirname(prev.file);
	      let map;

	      if (this.mapOpts.sourcesContent === false) {
	        map = new SourceMapConsumer(prev.text);
	        if (map.sourcesContent) {
	          map.sourcesContent = null;
	        }
	      } else {
	        map = prev.consumer();
	      }

	      this.map.applySourceMap(map, from, this.toUrl(this.path(root)));
	    }
	  }

	  clearAnnotation() {
	    if (this.mapOpts.annotation === false) return

	    if (this.root) {
	      let node;
	      for (let i = this.root.nodes.length - 1; i >= 0; i--) {
	        node = this.root.nodes[i];
	        if (node.type !== 'comment') continue
	        if (node.text.startsWith('# sourceMappingURL=')) {
	          this.root.removeChild(i);
	        }
	      }
	    } else if (this.css) {
	      this.css = this.css.replace(/\n*\/\*#[\S\s]*?\*\/$/gm, '');
	    }
	  }

	  generate() {
	    this.clearAnnotation();
	    if (pathAvailable && sourceMapAvailable && this.isMap()) {
	      return this.generateMap()
	    } else {
	      let result = '';
	      this.stringify(this.root, i => {
	        result += i;
	      });
	      return [result]
	    }
	  }

	  generateMap() {
	    if (this.root) {
	      this.generateString();
	    } else if (this.previous().length === 1) {
	      let prev = this.previous()[0].consumer();
	      prev.file = this.outputFile();
	      this.map = SourceMapGenerator.fromSourceMap(prev, {
	        ignoreInvalidMapping: true
	      });
	    } else {
	      this.map = new SourceMapGenerator({
	        file: this.outputFile(),
	        ignoreInvalidMapping: true
	      });
	      this.map.addMapping({
	        generated: { column: 0, line: 1 },
	        original: { column: 0, line: 1 },
	        source: this.opts.from
	          ? this.toUrl(this.path(this.opts.from))
	          : '<no source>'
	      });
	    }

	    if (this.isSourcesContent()) this.setSourcesContent();
	    if (this.root && this.previous().length > 0) this.applyPrevMaps();
	    if (this.isAnnotation()) this.addAnnotation();

	    if (this.isInline()) {
	      return [this.css]
	    } else {
	      return [this.css, this.map]
	    }
	  }

	  generateString() {
	    this.css = '';
	    this.map = new SourceMapGenerator({
	      file: this.outputFile(),
	      ignoreInvalidMapping: true
	    });

	    let line = 1;
	    let column = 1;

	    let noSource = '<no source>';
	    let mapping = {
	      generated: { column: 0, line: 0 },
	      original: { column: 0, line: 0 },
	      source: ''
	    };

	    let last, lines;
	    this.stringify(this.root, (str, node, type) => {
	      this.css += str;

	      if (node && type !== 'end') {
	        mapping.generated.line = line;
	        mapping.generated.column = column - 1;
	        if (node.source && node.source.start) {
	          mapping.source = this.sourcePath(node);
	          mapping.original.line = node.source.start.line;
	          mapping.original.column = node.source.start.column - 1;
	          this.map.addMapping(mapping);
	        } else {
	          mapping.source = noSource;
	          mapping.original.line = 1;
	          mapping.original.column = 0;
	          this.map.addMapping(mapping);
	        }
	      }

	      lines = str.match(/\n/g);
	      if (lines) {
	        line += lines.length;
	        last = str.lastIndexOf('\n');
	        column = str.length - last;
	      } else {
	        column += str.length;
	      }

	      if (node && type !== 'start') {
	        let p = node.parent || { raws: {} };
	        let childless =
	          node.type === 'decl' || (node.type === 'atrule' && !node.nodes);
	        if (!childless || node !== p.last || p.raws.semicolon) {
	          if (node.source && node.source.end) {
	            mapping.source = this.sourcePath(node);
	            mapping.original.line = node.source.end.line;
	            mapping.original.column = node.source.end.column - 1;
	            mapping.generated.line = line;
	            mapping.generated.column = column - 2;
	            this.map.addMapping(mapping);
	          } else {
	            mapping.source = noSource;
	            mapping.original.line = 1;
	            mapping.original.column = 0;
	            mapping.generated.line = line;
	            mapping.generated.column = column - 1;
	            this.map.addMapping(mapping);
	          }
	        }
	      }
	    });
	  }

	  isAnnotation() {
	    if (this.isInline()) {
	      return true
	    }
	    if (typeof this.mapOpts.annotation !== 'undefined') {
	      return this.mapOpts.annotation
	    }
	    if (this.previous().length) {
	      return this.previous().some(i => i.annotation)
	    }
	    return true
	  }

	  isInline() {
	    if (typeof this.mapOpts.inline !== 'undefined') {
	      return this.mapOpts.inline
	    }

	    let annotation = this.mapOpts.annotation;
	    if (typeof annotation !== 'undefined' && annotation !== true) {
	      return false
	    }

	    if (this.previous().length) {
	      return this.previous().some(i => i.inline)
	    }
	    return true
	  }

	  isMap() {
	    if (typeof this.opts.map !== 'undefined') {
	      return !!this.opts.map
	    }
	    return this.previous().length > 0
	  }

	  isSourcesContent() {
	    if (typeof this.mapOpts.sourcesContent !== 'undefined') {
	      return this.mapOpts.sourcesContent
	    }
	    if (this.previous().length) {
	      return this.previous().some(i => i.withContent())
	    }
	    return true
	  }

	  outputFile() {
	    if (this.opts.to) {
	      return this.path(this.opts.to)
	    } else if (this.opts.from) {
	      return this.path(this.opts.from)
	    } else {
	      return 'to.css'
	    }
	  }

	  path(file) {
	    if (this.mapOpts.absolute) return file
	    if (file.charCodeAt(0) === 60 /* `<` */) return file
	    if (/^\w+:\/\//.test(file)) return file
	    let cached = this.memoizedPaths.get(file);
	    if (cached) return cached

	    let from = this.opts.to ? dirname(this.opts.to) : '.';

	    if (typeof this.mapOpts.annotation === 'string') {
	      from = dirname(resolve(from, this.mapOpts.annotation));
	    }

	    let path = relative(from, file);
	    this.memoizedPaths.set(file, path);

	    return path
	  }

	  previous() {
	    if (!this.previousMaps) {
	      this.previousMaps = [];
	      if (this.root) {
	        this.root.walk(node => {
	          if (node.source && node.source.input.map) {
	            let map = node.source.input.map;
	            if (!this.previousMaps.includes(map)) {
	              this.previousMaps.push(map);
	            }
	          }
	        });
	      } else {
	        let input = new Input(this.originalCSS, this.opts);
	        if (input.map) this.previousMaps.push(input.map);
	      }
	    }

	    return this.previousMaps
	  }

	  setSourcesContent() {
	    let already = {};
	    if (this.root) {
	      this.root.walk(node => {
	        if (node.source) {
	          let from = node.source.input.from;
	          if (from && !already[from]) {
	            already[from] = true;
	            let fromUrl = this.usesFileUrls
	              ? this.toFileUrl(from)
	              : this.toUrl(this.path(from));
	            this.map.setSourceContent(fromUrl, node.source.input.css);
	          }
	        }
	      });
	    } else if (this.css) {
	      let from = this.opts.from
	        ? this.toUrl(this.path(this.opts.from))
	        : '<no source>';
	      this.map.setSourceContent(from, this.css);
	    }
	  }

	  sourcePath(node) {
	    if (this.mapOpts.from) {
	      return this.toUrl(this.mapOpts.from)
	    } else if (this.usesFileUrls) {
	      return this.toFileUrl(node.source.input.from)
	    } else {
	      return this.toUrl(this.path(node.source.input.from))
	    }
	  }

	  toBase64(str) {
	    if (Buffer) {
	      return Buffer.from(str).toString('base64')
	    } else {
	      return window.btoa(unescape(encodeURIComponent(str)))
	    }
	  }

	  toFileUrl(path) {
	    let cached = this.memoizedFileURLs.get(path);
	    if (cached) return cached

	    if (pathToFileURL) {
	      let fileURL = pathToFileURL(path).toString();
	      this.memoizedFileURLs.set(path, fileURL);

	      return fileURL
	    } else {
	      throw new Error(
	        '`map.absolute` option is not available in this PostCSS build'
	      )
	    }
	  }

	  toUrl(path) {
	    let cached = this.memoizedURLs.get(path);
	    if (cached) return cached

	    if (sep === '\\') {
	      path = path.replace(/\\/g, '/');
	    }

	    let url = encodeURI(path).replace(/[#?]/g, encodeURIComponent);
	    this.memoizedURLs.set(path, url);

	    return url
	  }
	}

	mapGenerator = MapGenerator;
	return mapGenerator;
}

var parser;
var hasRequiredParser;

function requireParser () {
	if (hasRequiredParser) return parser;
	hasRequiredParser = 1;

	let AtRule = requireAtRule();
	let Comment = requireComment();
	let Declaration = requireDeclaration();
	let Root = requireRoot();
	let Rule = requireRule();
	let tokenizer = requireTokenize();

	const SAFE_COMMENT_NEIGHBOR = {
	  empty: true,
	  space: true
	};

	function findLastWithPosition(tokens) {
	  for (let i = tokens.length - 1; i >= 0; i--) {
	    let token = tokens[i];
	    let pos = token[3] || token[2];
	    if (pos) return pos
	  }
	}

	class Parser {
	  constructor(input) {
	    this.input = input;

	    this.root = new Root();
	    this.current = this.root;
	    this.spaces = '';
	    this.semicolon = false;

	    this.createTokenizer();
	    this.root.source = { input, start: { column: 1, line: 1, offset: 0 } };
	  }

	  atrule(token) {
	    let node = new AtRule();
	    node.name = token[1].slice(1);
	    if (node.name === '') {
	      this.unnamedAtrule(node, token);
	    }
	    this.init(node, token[2]);

	    let type;
	    let prev;
	    let shift;
	    let last = false;
	    let open = false;
	    let params = [];
	    let brackets = [];

	    while (!this.tokenizer.endOfFile()) {
	      token = this.tokenizer.nextToken();
	      type = token[0];

	      if (type === '(' || type === '[') {
	        brackets.push(type === '(' ? ')' : ']');
	      } else if (type === '{' && brackets.length > 0) {
	        brackets.push('}');
	      } else if (type === brackets[brackets.length - 1]) {
	        brackets.pop();
	      }

	      if (brackets.length === 0) {
	        if (type === ';') {
	          node.source.end = this.getPosition(token[2]);
	          node.source.end.offset++;
	          this.semicolon = true;
	          break
	        } else if (type === '{') {
	          open = true;
	          break
	        } else if (type === '}') {
	          if (params.length > 0) {
	            shift = params.length - 1;
	            prev = params[shift];
	            while (prev && prev[0] === 'space') {
	              prev = params[--shift];
	            }
	            if (prev) {
	              node.source.end = this.getPosition(prev[3] || prev[2]);
	              node.source.end.offset++;
	            }
	          }
	          this.end(token);
	          break
	        } else {
	          params.push(token);
	        }
	      } else {
	        params.push(token);
	      }

	      if (this.tokenizer.endOfFile()) {
	        last = true;
	        break
	      }
	    }

	    node.raws.between = this.spacesAndCommentsFromEnd(params);
	    if (params.length) {
	      node.raws.afterName = this.spacesAndCommentsFromStart(params);
	      this.raw(node, 'params', params);
	      if (last) {
	        token = params[params.length - 1];
	        node.source.end = this.getPosition(token[3] || token[2]);
	        node.source.end.offset++;
	        this.spaces = node.raws.between;
	        node.raws.between = '';
	      }
	    } else {
	      node.raws.afterName = '';
	      node.params = '';
	    }

	    if (open) {
	      node.nodes = [];
	      this.current = node;
	    }
	  }

	  checkMissedSemicolon(tokens) {
	    let colon = this.colon(tokens);
	    if (colon === false) return

	    let founded = 0;
	    let token;
	    for (let j = colon - 1; j >= 0; j--) {
	      token = tokens[j];
	      if (token[0] !== 'space') {
	        founded += 1;
	        if (founded === 2) break
	      }
	    }
	    // If the token is a word, e.g. `!important`, `red` or any other valid property's value.
	    // Then we need to return the colon after that word token. [3] is the "end" colon of that word.
	    // And because we need it after that one we do +1 to get the next one.
	    throw this.input.error(
	      'Missed semicolon',
	      token[0] === 'word' ? token[3] + 1 : token[2]
	    )
	  }

	  colon(tokens) {
	    let brackets = 0;
	    let prev, token, type;
	    for (let [i, element] of tokens.entries()) {
	      token = element;
	      type = token[0];

	      if (type === '(') {
	        brackets += 1;
	      }
	      if (type === ')') {
	        brackets -= 1;
	      }
	      if (brackets === 0 && type === ':') {
	        if (!prev) {
	          this.doubleColon(token);
	        } else if (prev[0] === 'word' && prev[1] === 'progid') {
	          continue
	        } else {
	          return i
	        }
	      }

	      prev = token;
	    }
	    return false
	  }

	  comment(token) {
	    let node = new Comment();
	    this.init(node, token[2]);
	    node.source.end = this.getPosition(token[3] || token[2]);
	    node.source.end.offset++;

	    let text = token[1].slice(2, -2);
	    if (/^\s*$/.test(text)) {
	      node.text = '';
	      node.raws.left = text;
	      node.raws.right = '';
	    } else {
	      let match = text.match(/^(\s*)([^]*\S)(\s*)$/);
	      node.text = match[2];
	      node.raws.left = match[1];
	      node.raws.right = match[3];
	    }
	  }

	  createTokenizer() {
	    this.tokenizer = tokenizer(this.input);
	  }

	  decl(tokens, customProperty) {
	    let node = new Declaration();
	    this.init(node, tokens[0][2]);

	    let last = tokens[tokens.length - 1];
	    if (last[0] === ';') {
	      this.semicolon = true;
	      tokens.pop();
	    }

	    node.source.end = this.getPosition(
	      last[3] || last[2] || findLastWithPosition(tokens)
	    );
	    node.source.end.offset++;

	    while (tokens[0][0] !== 'word') {
	      if (tokens.length === 1) this.unknownWord(tokens);
	      node.raws.before += tokens.shift()[1];
	    }
	    node.source.start = this.getPosition(tokens[0][2]);

	    node.prop = '';
	    while (tokens.length) {
	      let type = tokens[0][0];
	      if (type === ':' || type === 'space' || type === 'comment') {
	        break
	      }
	      node.prop += tokens.shift()[1];
	    }

	    node.raws.between = '';

	    let token;
	    while (tokens.length) {
	      token = tokens.shift();

	      if (token[0] === ':') {
	        node.raws.between += token[1];
	        break
	      } else {
	        if (token[0] === 'word' && /\w/.test(token[1])) {
	          this.unknownWord([token]);
	        }
	        node.raws.between += token[1];
	      }
	    }

	    if (node.prop[0] === '_' || node.prop[0] === '*') {
	      node.raws.before += node.prop[0];
	      node.prop = node.prop.slice(1);
	    }

	    let firstSpaces = [];
	    let next;
	    while (tokens.length) {
	      next = tokens[0][0];
	      if (next !== 'space' && next !== 'comment') break
	      firstSpaces.push(tokens.shift());
	    }

	    this.precheckMissedSemicolon(tokens);

	    for (let i = tokens.length - 1; i >= 0; i--) {
	      token = tokens[i];
	      if (token[1].toLowerCase() === '!important') {
	        node.important = true;
	        let string = this.stringFrom(tokens, i);
	        string = this.spacesFromEnd(tokens) + string;
	        if (string !== ' !important') node.raws.important = string;
	        break
	      } else if (token[1].toLowerCase() === 'important') {
	        let cache = tokens.slice(0);
	        let str = '';
	        for (let j = i; j > 0; j--) {
	          let type = cache[j][0];
	          if (str.trim().startsWith('!') && type !== 'space') {
	            break
	          }
	          str = cache.pop()[1] + str;
	        }
	        if (str.trim().startsWith('!')) {
	          node.important = true;
	          node.raws.important = str;
	          tokens = cache;
	        }
	      }

	      if (token[0] !== 'space' && token[0] !== 'comment') {
	        break
	      }
	    }

	    let hasWord = tokens.some(i => i[0] !== 'space' && i[0] !== 'comment');

	    if (hasWord) {
	      node.raws.between += firstSpaces.map(i => i[1]).join('');
	      firstSpaces = [];
	    }
	    this.raw(node, 'value', firstSpaces.concat(tokens), customProperty);

	    if (node.value.includes(':') && !customProperty) {
	      this.checkMissedSemicolon(tokens);
	    }
	  }

	  doubleColon(token) {
	    throw this.input.error(
	      'Double colon',
	      { offset: token[2] },
	      { offset: token[2] + token[1].length }
	    )
	  }

	  emptyRule(token) {
	    let node = new Rule();
	    this.init(node, token[2]);
	    node.selector = '';
	    node.raws.between = '';
	    this.current = node;
	  }

	  end(token) {
	    if (this.current.nodes && this.current.nodes.length) {
	      this.current.raws.semicolon = this.semicolon;
	    }
	    this.semicolon = false;

	    this.current.raws.after = (this.current.raws.after || '') + this.spaces;
	    this.spaces = '';

	    if (this.current.parent) {
	      this.current.source.end = this.getPosition(token[2]);
	      this.current.source.end.offset++;
	      this.current = this.current.parent;
	    } else {
	      this.unexpectedClose(token);
	    }
	  }

	  endFile() {
	    if (this.current.parent) this.unclosedBlock();
	    if (this.current.nodes && this.current.nodes.length) {
	      this.current.raws.semicolon = this.semicolon;
	    }
	    this.current.raws.after = (this.current.raws.after || '') + this.spaces;
	    this.root.source.end = this.getPosition(this.tokenizer.position());
	  }

	  freeSemicolon(token) {
	    this.spaces += token[1];
	    if (this.current.nodes) {
	      let prev = this.current.nodes[this.current.nodes.length - 1];
	      if (prev && prev.type === 'rule' && !prev.raws.ownSemicolon) {
	        prev.raws.ownSemicolon = this.spaces;
	        this.spaces = '';
	        prev.source.end = this.getPosition(token[2]);
	        prev.source.end.offset += prev.raws.ownSemicolon.length;
	      }
	    }
	  }

	  // Helpers

	  getPosition(offset) {
	    let pos = this.input.fromOffset(offset);
	    return {
	      column: pos.col,
	      line: pos.line,
	      offset
	    }
	  }

	  init(node, offset) {
	    this.current.push(node);
	    node.source = {
	      input: this.input,
	      start: this.getPosition(offset)
	    };
	    node.raws.before = this.spaces;
	    this.spaces = '';
	    if (node.type !== 'comment') this.semicolon = false;
	  }

	  other(start) {
	    let end = false;
	    let type = null;
	    let colon = false;
	    let bracket = null;
	    let brackets = [];
	    let customProperty = start[1].startsWith('--');

	    let tokens = [];
	    let token = start;
	    while (token) {
	      type = token[0];
	      tokens.push(token);

	      if (type === '(' || type === '[') {
	        if (!bracket) bracket = token;
	        brackets.push(type === '(' ? ')' : ']');
	      } else if (customProperty && colon && type === '{') {
	        if (!bracket) bracket = token;
	        brackets.push('}');
	      } else if (brackets.length === 0) {
	        if (type === ';') {
	          if (colon) {
	            this.decl(tokens, customProperty);
	            return
	          } else {
	            break
	          }
	        } else if (type === '{') {
	          this.rule(tokens);
	          return
	        } else if (type === '}') {
	          this.tokenizer.back(tokens.pop());
	          end = true;
	          break
	        } else if (type === ':') {
	          colon = true;
	        }
	      } else if (type === brackets[brackets.length - 1]) {
	        brackets.pop();
	        if (brackets.length === 0) bracket = null;
	      }

	      token = this.tokenizer.nextToken();
	    }

	    if (this.tokenizer.endOfFile()) end = true;
	    if (brackets.length > 0) this.unclosedBracket(bracket);

	    if (end && colon) {
	      if (!customProperty) {
	        while (tokens.length) {
	          token = tokens[tokens.length - 1][0];
	          if (token !== 'space' && token !== 'comment') break
	          this.tokenizer.back(tokens.pop());
	        }
	      }
	      this.decl(tokens, customProperty);
	    } else {
	      this.unknownWord(tokens);
	    }
	  }

	  parse() {
	    let token;
	    while (!this.tokenizer.endOfFile()) {
	      token = this.tokenizer.nextToken();

	      switch (token[0]) {
	        case 'space':
	          this.spaces += token[1];
	          break

	        case ';':
	          this.freeSemicolon(token);
	          break

	        case '}':
	          this.end(token);
	          break

	        case 'comment':
	          this.comment(token);
	          break

	        case 'at-word':
	          this.atrule(token);
	          break

	        case '{':
	          this.emptyRule(token);
	          break

	        default:
	          this.other(token);
	          break
	      }
	    }
	    this.endFile();
	  }

	  precheckMissedSemicolon(/* tokens */) {
	    // Hook for Safe Parser
	  }

	  raw(node, prop, tokens, customProperty) {
	    let token, type;
	    let length = tokens.length;
	    let value = '';
	    let clean = true;
	    let next, prev;

	    for (let i = 0; i < length; i += 1) {
	      token = tokens[i];
	      type = token[0];
	      if (type === 'space' && i === length - 1 && !customProperty) {
	        clean = false;
	      } else if (type === 'comment') {
	        prev = tokens[i - 1] ? tokens[i - 1][0] : 'empty';
	        next = tokens[i + 1] ? tokens[i + 1][0] : 'empty';
	        if (!SAFE_COMMENT_NEIGHBOR[prev] && !SAFE_COMMENT_NEIGHBOR[next]) {
	          if (value.slice(-1) === ',') {
	            clean = false;
	          } else {
	            value += token[1];
	          }
	        } else {
	          clean = false;
	        }
	      } else {
	        value += token[1];
	      }
	    }
	    if (!clean) {
	      let raw = tokens.reduce((all, i) => all + i[1], '');
	      node.raws[prop] = { raw, value };
	    }
	    node[prop] = value;
	  }

	  rule(tokens) {
	    tokens.pop();

	    let node = new Rule();
	    this.init(node, tokens[0][2]);

	    node.raws.between = this.spacesAndCommentsFromEnd(tokens);
	    this.raw(node, 'selector', tokens);
	    this.current = node;
	  }

	  spacesAndCommentsFromEnd(tokens) {
	    let lastTokenType;
	    let spaces = '';
	    while (tokens.length) {
	      lastTokenType = tokens[tokens.length - 1][0];
	      if (lastTokenType !== 'space' && lastTokenType !== 'comment') break
	      spaces = tokens.pop()[1] + spaces;
	    }
	    return spaces
	  }

	  // Errors

	  spacesAndCommentsFromStart(tokens) {
	    let next;
	    let spaces = '';
	    while (tokens.length) {
	      next = tokens[0][0];
	      if (next !== 'space' && next !== 'comment') break
	      spaces += tokens.shift()[1];
	    }
	    return spaces
	  }

	  spacesFromEnd(tokens) {
	    let lastTokenType;
	    let spaces = '';
	    while (tokens.length) {
	      lastTokenType = tokens[tokens.length - 1][0];
	      if (lastTokenType !== 'space') break
	      spaces = tokens.pop()[1] + spaces;
	    }
	    return spaces
	  }

	  stringFrom(tokens, from) {
	    let result = '';
	    for (let i = from; i < tokens.length; i++) {
	      result += tokens[i][1];
	    }
	    tokens.splice(from, tokens.length - from);
	    return result
	  }

	  unclosedBlock() {
	    let pos = this.current.source.start;
	    throw this.input.error('Unclosed block', pos.line, pos.column)
	  }

	  unclosedBracket(bracket) {
	    throw this.input.error(
	      'Unclosed bracket',
	      { offset: bracket[2] },
	      { offset: bracket[2] + 1 }
	    )
	  }

	  unexpectedClose(token) {
	    throw this.input.error(
	      'Unexpected }',
	      { offset: token[2] },
	      { offset: token[2] + 1 }
	    )
	  }

	  unknownWord(tokens) {
	    throw this.input.error(
	      'Unknown word ' + tokens[0][1],
	      { offset: tokens[0][2] },
	      { offset: tokens[0][2] + tokens[0][1].length }
	    )
	  }

	  unnamedAtrule(node, token) {
	    throw this.input.error(
	      'At-rule without name',
	      { offset: token[2] },
	      { offset: token[2] + token[1].length }
	    )
	  }
	}

	parser = Parser;
	return parser;
}

var parse_1;
var hasRequiredParse;

function requireParse () {
	if (hasRequiredParse) return parse_1;
	hasRequiredParse = 1;

	let Container = requireContainer();
	let Input = requireInput();
	let Parser = requireParser();

	function parse(css, opts) {
	  let input = new Input(css, opts);
	  let parser = new Parser(input);
	  try {
	    parser.parse();
	  } catch (e) {
	    if (process.env.NODE_ENV !== 'production') {
	      if (e.name === 'CssSyntaxError' && opts && opts.from) {
	        if (/\.scss$/i.test(opts.from)) {
	          e.message +=
	            '\nYou tried to parse SCSS with ' +
	            'the standard CSS parser; ' +
	            'try again with the postcss-scss parser';
	        } else if (/\.sass/i.test(opts.from)) {
	          e.message +=
	            '\nYou tried to parse Sass with ' +
	            'the standard CSS parser; ' +
	            'try again with the postcss-sass parser';
	        } else if (/\.less$/i.test(opts.from)) {
	          e.message +=
	            '\nYou tried to parse Less with ' +
	            'the standard CSS parser; ' +
	            'try again with the postcss-less parser';
	        }
	      }
	    }
	    throw e
	  }

	  return parser.root
	}

	parse_1 = parse;
	parse.default = parse;

	Container.registerParse(parse);
	return parse_1;
}

var warning;
var hasRequiredWarning;

function requireWarning () {
	if (hasRequiredWarning) return warning;
	hasRequiredWarning = 1;

	class Warning {
	  constructor(text, opts = {}) {
	    this.type = 'warning';
	    this.text = text;

	    if (opts.node && opts.node.source) {
	      let range = opts.node.rangeBy(opts);
	      this.line = range.start.line;
	      this.column = range.start.column;
	      this.endLine = range.end.line;
	      this.endColumn = range.end.column;
	    }

	    for (let opt in opts) this[opt] = opts[opt];
	  }

	  toString() {
	    if (this.node) {
	      return this.node.error(this.text, {
	        index: this.index,
	        plugin: this.plugin,
	        word: this.word
	      }).message
	    }

	    if (this.plugin) {
	      return this.plugin + ': ' + this.text
	    }

	    return this.text
	  }
	}

	warning = Warning;
	Warning.default = Warning;
	return warning;
}

var result;
var hasRequiredResult;

function requireResult () {
	if (hasRequiredResult) return result;
	hasRequiredResult = 1;

	let Warning = requireWarning();

	class Result {
	  get content() {
	    return this.css
	  }

	  constructor(processor, root, opts) {
	    this.processor = processor;
	    this.messages = [];
	    this.root = root;
	    this.opts = opts;
	    this.css = '';
	    this.map = undefined;
	  }

	  toString() {
	    return this.css
	  }

	  warn(text, opts = {}) {
	    if (!opts.plugin) {
	      if (this.lastPlugin && this.lastPlugin.postcssPlugin) {
	        opts.plugin = this.lastPlugin.postcssPlugin;
	      }
	    }

	    let warning = new Warning(text, opts);
	    this.messages.push(warning);

	    return warning
	  }

	  warnings() {
	    return this.messages.filter(i => i.type === 'warning')
	  }
	}

	result = Result;
	Result.default = Result;
	return result;
}

/* eslint-disable no-console */

var warnOnce;
var hasRequiredWarnOnce;

function requireWarnOnce () {
	if (hasRequiredWarnOnce) return warnOnce;
	hasRequiredWarnOnce = 1;

	let printed = {};

	warnOnce = function warnOnce(message) {
	  if (printed[message]) return
	  printed[message] = true;

	  if (typeof console !== 'undefined' && console.warn) {
	    console.warn(message);
	  }
	};
	return warnOnce;
}

var lazyResult;
var hasRequiredLazyResult;

function requireLazyResult () {
	if (hasRequiredLazyResult) return lazyResult;
	hasRequiredLazyResult = 1;

	let Container = requireContainer();
	let Document = requireDocument();
	let MapGenerator = requireMapGenerator();
	let parse = requireParse();
	let Result = requireResult();
	let Root = requireRoot();
	let stringify = requireStringify();
	let { isClean, my } = requireSymbols();
	let warnOnce = requireWarnOnce();

	const TYPE_TO_CLASS_NAME = {
	  atrule: 'AtRule',
	  comment: 'Comment',
	  decl: 'Declaration',
	  document: 'Document',
	  root: 'Root',
	  rule: 'Rule'
	};

	const PLUGIN_PROPS = {
	  AtRule: true,
	  AtRuleExit: true,
	  Comment: true,
	  CommentExit: true,
	  Declaration: true,
	  DeclarationExit: true,
	  Document: true,
	  DocumentExit: true,
	  Once: true,
	  OnceExit: true,
	  postcssPlugin: true,
	  prepare: true,
	  Root: true,
	  RootExit: true,
	  Rule: true,
	  RuleExit: true
	};

	const NOT_VISITORS = {
	  Once: true,
	  postcssPlugin: true,
	  prepare: true
	};

	const CHILDREN = 0;

	function isPromise(obj) {
	  return typeof obj === 'object' && typeof obj.then === 'function'
	}

	function getEvents(node) {
	  let key = false;
	  let type = TYPE_TO_CLASS_NAME[node.type];
	  if (node.type === 'decl') {
	    key = node.prop.toLowerCase();
	  } else if (node.type === 'atrule') {
	    key = node.name.toLowerCase();
	  }

	  if (key && node.append) {
	    return [
	      type,
	      type + '-' + key,
	      CHILDREN,
	      type + 'Exit',
	      type + 'Exit-' + key
	    ]
	  } else if (key) {
	    return [type, type + '-' + key, type + 'Exit', type + 'Exit-' + key]
	  } else if (node.append) {
	    return [type, CHILDREN, type + 'Exit']
	  } else {
	    return [type, type + 'Exit']
	  }
	}

	function toStack(node) {
	  let events;
	  if (node.type === 'document') {
	    events = ['Document', CHILDREN, 'DocumentExit'];
	  } else if (node.type === 'root') {
	    events = ['Root', CHILDREN, 'RootExit'];
	  } else {
	    events = getEvents(node);
	  }

	  return {
	    eventIndex: 0,
	    events,
	    iterator: 0,
	    node,
	    visitorIndex: 0,
	    visitors: []
	  }
	}

	function cleanMarks(node) {
	  node[isClean] = false;
	  if (node.nodes) node.nodes.forEach(i => cleanMarks(i));
	  return node
	}

	let postcss = {};

	class LazyResult {
	  get content() {
	    return this.stringify().content
	  }

	  get css() {
	    return this.stringify().css
	  }

	  get map() {
	    return this.stringify().map
	  }

	  get messages() {
	    return this.sync().messages
	  }

	  get opts() {
	    return this.result.opts
	  }

	  get processor() {
	    return this.result.processor
	  }

	  get root() {
	    return this.sync().root
	  }

	  get [Symbol.toStringTag]() {
	    return 'LazyResult'
	  }

	  constructor(processor, css, opts) {
	    this.stringified = false;
	    this.processed = false;

	    let root;
	    if (
	      typeof css === 'object' &&
	      css !== null &&
	      (css.type === 'root' || css.type === 'document')
	    ) {
	      root = cleanMarks(css);
	    } else if (css instanceof LazyResult || css instanceof Result) {
	      root = cleanMarks(css.root);
	      if (css.map) {
	        if (typeof opts.map === 'undefined') opts.map = {};
	        if (!opts.map.inline) opts.map.inline = false;
	        opts.map.prev = css.map;
	      }
	    } else {
	      let parser = parse;
	      if (opts.syntax) parser = opts.syntax.parse;
	      if (opts.parser) parser = opts.parser;
	      if (parser.parse) parser = parser.parse;

	      try {
	        root = parser(css, opts);
	      } catch (error) {
	        this.processed = true;
	        this.error = error;
	      }

	      if (root && !root[my]) {
	        /* c8 ignore next 2 */
	        Container.rebuild(root);
	      }
	    }

	    this.result = new Result(processor, root, opts);
	    this.helpers = { ...postcss, postcss, result: this.result };
	    this.plugins = this.processor.plugins.map(plugin => {
	      if (typeof plugin === 'object' && plugin.prepare) {
	        return { ...plugin, ...plugin.prepare(this.result) }
	      } else {
	        return plugin
	      }
	    });
	  }

	  async() {
	    if (this.error) return Promise.reject(this.error)
	    if (this.processed) return Promise.resolve(this.result)
	    if (!this.processing) {
	      this.processing = this.runAsync();
	    }
	    return this.processing
	  }

	  catch(onRejected) {
	    return this.async().catch(onRejected)
	  }

	  finally(onFinally) {
	    return this.async().then(onFinally, onFinally)
	  }

	  getAsyncError() {
	    throw new Error('Use process(css).then(cb) to work with async plugins')
	  }

	  handleError(error, node) {
	    let plugin = this.result.lastPlugin;
	    try {
	      if (node) node.addToError(error);
	      this.error = error;
	      if (error.name === 'CssSyntaxError' && !error.plugin) {
	        error.plugin = plugin.postcssPlugin;
	        error.setMessage();
	      } else if (plugin.postcssVersion) {
	        if (process.env.NODE_ENV !== 'production') {
	          let pluginName = plugin.postcssPlugin;
	          let pluginVer = plugin.postcssVersion;
	          let runtimeVer = this.result.processor.version;
	          let a = pluginVer.split('.');
	          let b = runtimeVer.split('.');

	          if (a[0] !== b[0] || parseInt(a[1]) > parseInt(b[1])) {
	            // eslint-disable-next-line no-console
	            console.error(
	              'Unknown error from PostCSS plugin. Your current PostCSS ' +
	                'version is ' +
	                runtimeVer +
	                ', but ' +
	                pluginName +
	                ' uses ' +
	                pluginVer +
	                '. Perhaps this is the source of the error below.'
	            );
	          }
	        }
	      }
	    } catch (err) {
	      /* c8 ignore next 3 */
	      // eslint-disable-next-line no-console
	      if (console && console.error) console.error(err);
	    }
	    return error
	  }

	  prepareVisitors() {
	    this.listeners = {};
	    let add = (plugin, type, cb) => {
	      if (!this.listeners[type]) this.listeners[type] = [];
	      this.listeners[type].push([plugin, cb]);
	    };
	    for (let plugin of this.plugins) {
	      if (typeof plugin === 'object') {
	        for (let event in plugin) {
	          if (!PLUGIN_PROPS[event] && /^[A-Z]/.test(event)) {
	            throw new Error(
	              `Unknown event ${event} in ${plugin.postcssPlugin}. ` +
	                `Try to update PostCSS (${this.processor.version} now).`
	            )
	          }
	          if (!NOT_VISITORS[event]) {
	            if (typeof plugin[event] === 'object') {
	              for (let filter in plugin[event]) {
	                if (filter === '*') {
	                  add(plugin, event, plugin[event][filter]);
	                } else {
	                  add(
	                    plugin,
	                    event + '-' + filter.toLowerCase(),
	                    plugin[event][filter]
	                  );
	                }
	              }
	            } else if (typeof plugin[event] === 'function') {
	              add(plugin, event, plugin[event]);
	            }
	          }
	        }
	      }
	    }
	    this.hasListener = Object.keys(this.listeners).length > 0;
	  }

	  async runAsync() {
	    this.plugin = 0;
	    for (let i = 0; i < this.plugins.length; i++) {
	      let plugin = this.plugins[i];
	      let promise = this.runOnRoot(plugin);
	      if (isPromise(promise)) {
	        try {
	          await promise;
	        } catch (error) {
	          throw this.handleError(error)
	        }
	      }
	    }

	    this.prepareVisitors();
	    if (this.hasListener) {
	      let root = this.result.root;
	      while (!root[isClean]) {
	        root[isClean] = true;
	        let stack = [toStack(root)];
	        while (stack.length > 0) {
	          let promise = this.visitTick(stack);
	          if (isPromise(promise)) {
	            try {
	              await promise;
	            } catch (e) {
	              let node = stack[stack.length - 1].node;
	              throw this.handleError(e, node)
	            }
	          }
	        }
	      }

	      if (this.listeners.OnceExit) {
	        for (let [plugin, visitor] of this.listeners.OnceExit) {
	          this.result.lastPlugin = plugin;
	          try {
	            if (root.type === 'document') {
	              let roots = root.nodes.map(subRoot =>
	                visitor(subRoot, this.helpers)
	              );

	              await Promise.all(roots);
	            } else {
	              await visitor(root, this.helpers);
	            }
	          } catch (e) {
	            throw this.handleError(e)
	          }
	        }
	      }
	    }

	    this.processed = true;
	    return this.stringify()
	  }

	  runOnRoot(plugin) {
	    this.result.lastPlugin = plugin;
	    try {
	      if (typeof plugin === 'object' && plugin.Once) {
	        if (this.result.root.type === 'document') {
	          let roots = this.result.root.nodes.map(root =>
	            plugin.Once(root, this.helpers)
	          );

	          if (isPromise(roots[0])) {
	            return Promise.all(roots)
	          }

	          return roots
	        }

	        return plugin.Once(this.result.root, this.helpers)
	      } else if (typeof plugin === 'function') {
	        return plugin(this.result.root, this.result)
	      }
	    } catch (error) {
	      throw this.handleError(error)
	    }
	  }

	  stringify() {
	    if (this.error) throw this.error
	    if (this.stringified) return this.result
	    this.stringified = true;

	    this.sync();

	    let opts = this.result.opts;
	    let str = stringify;
	    if (opts.syntax) str = opts.syntax.stringify;
	    if (opts.stringifier) str = opts.stringifier;
	    if (str.stringify) str = str.stringify;

	    let map = new MapGenerator(str, this.result.root, this.result.opts);
	    let data = map.generate();
	    this.result.css = data[0];
	    this.result.map = data[1];

	    return this.result
	  }

	  sync() {
	    if (this.error) throw this.error
	    if (this.processed) return this.result
	    this.processed = true;

	    if (this.processing) {
	      throw this.getAsyncError()
	    }

	    for (let plugin of this.plugins) {
	      let promise = this.runOnRoot(plugin);
	      if (isPromise(promise)) {
	        throw this.getAsyncError()
	      }
	    }

	    this.prepareVisitors();
	    if (this.hasListener) {
	      let root = this.result.root;
	      while (!root[isClean]) {
	        root[isClean] = true;
	        this.walkSync(root);
	      }
	      if (this.listeners.OnceExit) {
	        if (root.type === 'document') {
	          for (let subRoot of root.nodes) {
	            this.visitSync(this.listeners.OnceExit, subRoot);
	          }
	        } else {
	          this.visitSync(this.listeners.OnceExit, root);
	        }
	      }
	    }

	    return this.result
	  }

	  then(onFulfilled, onRejected) {
	    if (process.env.NODE_ENV !== 'production') {
	      if (!('from' in this.opts)) {
	        warnOnce(
	          'Without `from` option PostCSS could generate wrong source map ' +
	            'and will not find Browserslist config. Set it to CSS file path ' +
	            'or to `undefined` to prevent this warning.'
	        );
	      }
	    }
	    return this.async().then(onFulfilled, onRejected)
	  }

	  toString() {
	    return this.css
	  }

	  visitSync(visitors, node) {
	    for (let [plugin, visitor] of visitors) {
	      this.result.lastPlugin = plugin;
	      let promise;
	      try {
	        promise = visitor(node, this.helpers);
	      } catch (e) {
	        throw this.handleError(e, node.proxyOf)
	      }
	      if (node.type !== 'root' && node.type !== 'document' && !node.parent) {
	        return true
	      }
	      if (isPromise(promise)) {
	        throw this.getAsyncError()
	      }
	    }
	  }

	  visitTick(stack) {
	    let visit = stack[stack.length - 1];
	    let { node, visitors } = visit;

	    if (node.type !== 'root' && node.type !== 'document' && !node.parent) {
	      stack.pop();
	      return
	    }

	    if (visitors.length > 0 && visit.visitorIndex < visitors.length) {
	      let [plugin, visitor] = visitors[visit.visitorIndex];
	      visit.visitorIndex += 1;
	      if (visit.visitorIndex === visitors.length) {
	        visit.visitors = [];
	        visit.visitorIndex = 0;
	      }
	      this.result.lastPlugin = plugin;
	      try {
	        return visitor(node.toProxy(), this.helpers)
	      } catch (e) {
	        throw this.handleError(e, node)
	      }
	    }

	    if (visit.iterator !== 0) {
	      let iterator = visit.iterator;
	      let child;
	      while ((child = node.nodes[node.indexes[iterator]])) {
	        node.indexes[iterator] += 1;
	        if (!child[isClean]) {
	          child[isClean] = true;
	          stack.push(toStack(child));
	          return
	        }
	      }
	      visit.iterator = 0;
	      delete node.indexes[iterator];
	    }

	    let events = visit.events;
	    while (visit.eventIndex < events.length) {
	      let event = events[visit.eventIndex];
	      visit.eventIndex += 1;
	      if (event === CHILDREN) {
	        if (node.nodes && node.nodes.length) {
	          node[isClean] = true;
	          visit.iterator = node.getIterator();
	        }
	        return
	      } else if (this.listeners[event]) {
	        visit.visitors = this.listeners[event];
	        return
	      }
	    }
	    stack.pop();
	  }

	  walkSync(node) {
	    node[isClean] = true;
	    let events = getEvents(node);
	    for (let event of events) {
	      if (event === CHILDREN) {
	        if (node.nodes) {
	          node.each(child => {
	            if (!child[isClean]) this.walkSync(child);
	          });
	        }
	      } else {
	        let visitors = this.listeners[event];
	        if (visitors) {
	          if (this.visitSync(visitors, node.toProxy())) return
	        }
	      }
	    }
	  }

	  warnings() {
	    return this.sync().warnings()
	  }
	}

	LazyResult.registerPostcss = dependant => {
	  postcss = dependant;
	};

	lazyResult = LazyResult;
	LazyResult.default = LazyResult;

	Root.registerLazyResult(LazyResult);
	Document.registerLazyResult(LazyResult);
	return lazyResult;
}

var noWorkResult;
var hasRequiredNoWorkResult;

function requireNoWorkResult () {
	if (hasRequiredNoWorkResult) return noWorkResult;
	hasRequiredNoWorkResult = 1;

	let MapGenerator = requireMapGenerator();
	let parse = requireParse();
	const Result = requireResult();
	let stringify = requireStringify();
	let warnOnce = requireWarnOnce();

	class NoWorkResult {
	  get content() {
	    return this.result.css
	  }

	  get css() {
	    return this.result.css
	  }

	  get map() {
	    return this.result.map
	  }

	  get messages() {
	    return []
	  }

	  get opts() {
	    return this.result.opts
	  }

	  get processor() {
	    return this.result.processor
	  }

	  get root() {
	    if (this._root) {
	      return this._root
	    }

	    let root;
	    let parser = parse;

	    try {
	      root = parser(this._css, this._opts);
	    } catch (error) {
	      this.error = error;
	    }

	    if (this.error) {
	      throw this.error
	    } else {
	      this._root = root;
	      return root
	    }
	  }

	  get [Symbol.toStringTag]() {
	    return 'NoWorkResult'
	  }

	  constructor(processor, css, opts) {
	    css = css.toString();
	    this.stringified = false;

	    this._processor = processor;
	    this._css = css;
	    this._opts = opts;
	    this._map = undefined;
	    let root;

	    let str = stringify;
	    this.result = new Result(this._processor, root, this._opts);
	    this.result.css = css;

	    let self = this;
	    Object.defineProperty(this.result, 'root', {
	      get() {
	        return self.root
	      }
	    });

	    let map = new MapGenerator(str, root, this._opts, css);
	    if (map.isMap()) {
	      let [generatedCSS, generatedMap] = map.generate();
	      if (generatedCSS) {
	        this.result.css = generatedCSS;
	      }
	      if (generatedMap) {
	        this.result.map = generatedMap;
	      }
	    } else {
	      map.clearAnnotation();
	      this.result.css = map.css;
	    }
	  }

	  async() {
	    if (this.error) return Promise.reject(this.error)
	    return Promise.resolve(this.result)
	  }

	  catch(onRejected) {
	    return this.async().catch(onRejected)
	  }

	  finally(onFinally) {
	    return this.async().then(onFinally, onFinally)
	  }

	  sync() {
	    if (this.error) throw this.error
	    return this.result
	  }

	  then(onFulfilled, onRejected) {
	    if (process.env.NODE_ENV !== 'production') {
	      if (!('from' in this._opts)) {
	        warnOnce(
	          'Without `from` option PostCSS could generate wrong source map ' +
	            'and will not find Browserslist config. Set it to CSS file path ' +
	            'or to `undefined` to prevent this warning.'
	        );
	      }
	    }

	    return this.async().then(onFulfilled, onRejected)
	  }

	  toString() {
	    return this._css
	  }

	  warnings() {
	    return []
	  }
	}

	noWorkResult = NoWorkResult;
	NoWorkResult.default = NoWorkResult;
	return noWorkResult;
}

var processor;
var hasRequiredProcessor;

function requireProcessor () {
	if (hasRequiredProcessor) return processor;
	hasRequiredProcessor = 1;

	let Document = requireDocument();
	let LazyResult = requireLazyResult();
	let NoWorkResult = requireNoWorkResult();
	let Root = requireRoot();

	class Processor {
	  constructor(plugins = []) {
	    this.version = '8.5.6';
	    this.plugins = this.normalize(plugins);
	  }

	  normalize(plugins) {
	    let normalized = [];
	    for (let i of plugins) {
	      if (i.postcss === true) {
	        i = i();
	      } else if (i.postcss) {
	        i = i.postcss;
	      }

	      if (typeof i === 'object' && Array.isArray(i.plugins)) {
	        normalized = normalized.concat(i.plugins);
	      } else if (typeof i === 'object' && i.postcssPlugin) {
	        normalized.push(i);
	      } else if (typeof i === 'function') {
	        normalized.push(i);
	      } else if (typeof i === 'object' && (i.parse || i.stringify)) {
	        if (process.env.NODE_ENV !== 'production') {
	          throw new Error(
	            'PostCSS syntaxes cannot be used as plugins. Instead, please use ' +
	              'one of the syntax/parser/stringifier options as outlined ' +
	              'in your PostCSS runner documentation.'
	          )
	        }
	      } else {
	        throw new Error(i + ' is not a PostCSS plugin')
	      }
	    }
	    return normalized
	  }

	  process(css, opts = {}) {
	    if (
	      !this.plugins.length &&
	      !opts.parser &&
	      !opts.stringifier &&
	      !opts.syntax
	    ) {
	      return new NoWorkResult(this, css, opts)
	    } else {
	      return new LazyResult(this, css, opts)
	    }
	  }

	  use(plugin) {
	    this.plugins = this.plugins.concat(this.normalize([plugin]));
	    return this
	  }
	}

	processor = Processor;
	Processor.default = Processor;

	Root.registerProcessor(Processor);
	Document.registerProcessor(Processor);
	return processor;
}

var postcss_1;
var hasRequiredPostcss;

function requirePostcss () {
	if (hasRequiredPostcss) return postcss_1;
	hasRequiredPostcss = 1;

	let AtRule = requireAtRule();
	let Comment = requireComment();
	let Container = requireContainer();
	let CssSyntaxError = requireCssSyntaxError();
	let Declaration = requireDeclaration();
	let Document = requireDocument();
	let fromJSON = requireFromJSON();
	let Input = requireInput();
	let LazyResult = requireLazyResult();
	let list = requireList();
	let Node = requireNode();
	let parse = requireParse();
	let Processor = requireProcessor();
	let Result = requireResult();
	let Root = requireRoot();
	let Rule = requireRule();
	let stringify = requireStringify();
	let Warning = requireWarning();

	function postcss(...plugins) {
	  if (plugins.length === 1 && Array.isArray(plugins[0])) {
	    plugins = plugins[0];
	  }
	  return new Processor(plugins)
	}

	postcss.plugin = function plugin(name, initializer) {
	  let warningPrinted = false;
	  function creator(...args) {
	    // eslint-disable-next-line no-console
	    if (console && console.warn && !warningPrinted) {
	      warningPrinted = true;
	      // eslint-disable-next-line no-console
	      console.warn(
	        name +
	          ': postcss.plugin was deprecated. Migration guide:\n' +
	          'https://evilmartians.com/chronicles/postcss-8-plugin-migration'
	      );
	      if (process.env.LANG && process.env.LANG.startsWith('cn')) {
	        /* c8 ignore next 7 */
	        // eslint-disable-next-line no-console
	        console.warn(
	          name +
	            ': 里面 postcss.plugin 被弃用. 迁移指南:\n' +
	            'https://www.w3ctech.com/topic/2226'
	        );
	      }
	    }
	    let transformer = initializer(...args);
	    transformer.postcssPlugin = name;
	    transformer.postcssVersion = new Processor().version;
	    return transformer
	  }

	  let cache;
	  Object.defineProperty(creator, 'postcss', {
	    get() {
	      if (!cache) cache = creator();
	      return cache
	    }
	  });

	  creator.process = function (css, processOpts, pluginOpts) {
	    return postcss([creator(pluginOpts)]).process(css, processOpts)
	  };

	  return creator
	};

	postcss.stringify = stringify;
	postcss.parse = parse;
	postcss.fromJSON = fromJSON;
	postcss.list = list;

	postcss.comment = defaults => new Comment(defaults);
	postcss.atRule = defaults => new AtRule(defaults);
	postcss.decl = defaults => new Declaration(defaults);
	postcss.rule = defaults => new Rule(defaults);
	postcss.root = defaults => new Root(defaults);
	postcss.document = defaults => new Document(defaults);

	postcss.CssSyntaxError = CssSyntaxError;
	postcss.Declaration = Declaration;
	postcss.Container = Container;
	postcss.Processor = Processor;
	postcss.Document = Document;
	postcss.Comment = Comment;
	postcss.Warning = Warning;
	postcss.AtRule = AtRule;
	postcss.Result = Result;
	postcss.Input = Input;
	postcss.Rule = Rule;
	postcss.Root = Root;
	postcss.Node = Node;

	LazyResult.registerPostcss(postcss);

	postcss_1 = postcss;
	postcss.default = postcss;
	return postcss_1;
}

var postcssExports = requirePostcss();
var postcss = /*@__PURE__*/getDefaultExportFromCjs(postcssExports);

postcss.stringify;
postcss.fromJSON;
postcss.plugin;
postcss.parse;
postcss.list;

postcss.document;
postcss.comment;
postcss.atRule;
postcss.rule;
postcss.decl;
postcss.root;

postcss.CssSyntaxError;
postcss.Declaration;
postcss.Container;
postcss.Processor;
postcss.Document;
postcss.Comment;
postcss.Warning;
postcss.AtRule;
postcss.Result;
postcss.Input;
postcss.Rule;
postcss.Root;
postcss.Node;

var J={},Y={},Eu={},K={},pu={},Bu;function qe(){return Bu||(Bu=1,Object.defineProperty(pu,"__esModule",{value:true}),pu.default=new Uint16Array('ᵁ<Õıʊҝջאٵ۞ޢߖࠏ੊ઑඡ๭༉༦჊ረዡᐕᒝᓃᓟᔥ\0\0\0\0\0\0ᕫᛍᦍᰒᷝ὾⁠↰⊍⏀⏻⑂⠤⤒ⴈ⹈⿎〖㊺㘹㞬㣾㨨㩱㫠㬮ࠀEMabcfglmnoprstu\\bfms¦³¹ÈÏlig耻Æ䃆P耻&䀦cute耻Á䃁reve;䄂Āiyx}rc耻Â䃂;䐐r;쀀𝔄rave耻À䃀pha;䎑acr;䄀d;橓Āgp¡on;䄄f;쀀𝔸plyFunction;恡ing耻Å䃅Ācs¾Ãr;쀀𝒜ign;扔ilde耻Ã䃃ml耻Ä䃄ЀaceforsuåûþėĜĢħĪĀcrêòkslash;或Ŷöø;櫧ed;挆y;䐑ƀcrtąċĔause;戵noullis;愬a;䎒r;쀀𝔅pf;쀀𝔹eve;䋘còēmpeq;扎܀HOacdefhilorsuōőŖƀƞƢƵƷƺǜȕɳɸɾcy;䐧PY耻©䂩ƀcpyŝŢźute;䄆Ā;iŧŨ拒talDifferentialD;慅leys;愭ȀaeioƉƎƔƘron;䄌dil耻Ç䃇rc;䄈nint;戰ot;䄊ĀdnƧƭilla;䂸terDot;䂷òſi;䎧rcleȀDMPTǇǋǑǖot;抙inus;抖lus;投imes;抗oĀcsǢǸkwiseContourIntegral;戲eCurlyĀDQȃȏoubleQuote;思uote;怙ȀlnpuȞȨɇɕonĀ;eȥȦ户;橴ƀgitȯȶȺruent;扡nt;戯ourIntegral;戮ĀfrɌɎ;愂oduct;成nterClockwiseContourIntegral;戳oss;樯cr;쀀𝒞pĀ;Cʄʅ拓ap;才րDJSZacefiosʠʬʰʴʸˋ˗ˡ˦̳ҍĀ;oŹʥtrahd;椑cy;䐂cy;䐅cy;䐏ƀgrsʿ˄ˇger;怡r;憡hv;櫤Āayː˕ron;䄎;䐔lĀ;t˝˞戇a;䎔r;쀀𝔇Āaf˫̧Ācm˰̢riticalȀADGT̖̜̀̆cute;䂴oŴ̋̍;䋙bleAcute;䋝rave;䁠ilde;䋜ond;拄ferentialD;慆Ѱ̽\0\0\0͔͂\0Ѕf;쀀𝔻ƀ;DE͈͉͍䂨ot;惜qual;扐blèCDLRUVͣͲ΂ϏϢϸontourIntegraìȹoɴ͹\0\0ͻ»͉nArrow;懓Āeo·ΤftƀARTΐΖΡrrow;懐ightArrow;懔eåˊngĀLRΫτeftĀARγιrrow;柸ightArrow;柺ightArrow;柹ightĀATϘϞrrow;懒ee;抨pɁϩ\0\0ϯrrow;懑ownArrow;懕erticalBar;戥ǹABLRTaВЪаўѿͼrrowƀ;BUНОТ憓ar;椓pArrow;懵reve;䌑eft˒к\0ц\0ѐightVector;楐eeVector;楞ectorĀ;Bљњ憽ar;楖ightǔѧ\0ѱeeVector;楟ectorĀ;BѺѻ懁ar;楗eeĀ;A҆҇护rrow;憧ĀctҒҗr;쀀𝒟rok;䄐ࠀNTacdfglmopqstuxҽӀӄӋӞӢӧӮӵԡԯԶՒ՝ՠեG;䅊H耻Ð䃐cute耻É䃉ƀaiyӒӗӜron;䄚rc耻Ê䃊;䐭ot;䄖r;쀀𝔈rave耻È䃈ement;戈ĀapӺӾcr;䄒tyɓԆ\0\0ԒmallSquare;旻erySmallSquare;斫ĀgpԦԪon;䄘f;쀀𝔼silon;䎕uĀaiԼՉlĀ;TՂՃ橵ilde;扂librium;懌Āci՗՚r;愰m;橳a;䎗ml耻Ë䃋Āipժկsts;戃onentialE;慇ʀcfiosօֈ֍ֲ׌y;䐤r;쀀𝔉lledɓ֗\0\0֣mallSquare;旼erySmallSquare;斪Ͱֺ\0ֿ\0\0ׄf;쀀𝔽All;戀riertrf;愱cò׋؀JTabcdfgorstר׬ׯ׺؀ؒؖ؛؝أ٬ٲcy;䐃耻>䀾mmaĀ;d׷׸䎓;䏜reve;䄞ƀeiy؇،ؐdil;䄢rc;䄜;䐓ot;䄠r;쀀𝔊;拙pf;쀀𝔾eater̀EFGLSTصلَٖٛ٦qualĀ;Lؾؿ扥ess;招ullEqual;执reater;檢ess;扷lantEqual;橾ilde;扳cr;쀀𝒢;扫ЀAacfiosuڅڋږڛڞڪھۊRDcy;䐪Āctڐڔek;䋇;䁞irc;䄤r;愌lbertSpace;愋ǰگ\0ڲf;愍izontalLine;攀Āctۃۅòکrok;䄦mpńېۘownHumðįqual;扏܀EJOacdfgmnostuۺ۾܃܇܎ܚܞܡܨ݄ݸދޏޕcy;䐕lig;䄲cy;䐁cute耻Í䃍Āiyܓܘrc耻Î䃎;䐘ot;䄰r;愑rave耻Ì䃌ƀ;apܠܯܿĀcgܴܷr;䄪inaryI;慈lieóϝǴ݉\0ݢĀ;eݍݎ戬Āgrݓݘral;戫section;拂isibleĀCTݬݲomma;恣imes;恢ƀgptݿރވon;䄮f;쀀𝕀a;䎙cr;愐ilde;䄨ǫޚ\0ޞcy;䐆l耻Ï䃏ʀcfosuެ޷޼߂ߐĀiyޱ޵rc;䄴;䐙r;쀀𝔍pf;쀀𝕁ǣ߇\0ߌr;쀀𝒥rcy;䐈kcy;䐄΀HJacfosߤߨ߽߬߱ࠂࠈcy;䐥cy;䐌ppa;䎚Āey߶߻dil;䄶;䐚r;쀀𝔎pf;쀀𝕂cr;쀀𝒦րJTaceflmostࠥࠩࠬࡐࡣ঳সে্਷ੇcy;䐉耻<䀼ʀcmnpr࠷࠼ࡁࡄࡍute;䄹bda;䎛g;柪lacetrf;愒r;憞ƀaeyࡗ࡜ࡡron;䄽dil;䄻;䐛Āfsࡨ॰tԀACDFRTUVarࡾࢩࢱࣦ࣠ࣼयज़ΐ४Ānrࢃ࢏gleBracket;柨rowƀ;BR࢙࢚࢞憐ar;懤ightArrow;懆eiling;挈oǵࢷ\0ࣃbleBracket;柦nǔࣈ\0࣒eeVector;楡ectorĀ;Bࣛࣜ懃ar;楙loor;挊ightĀAV࣯ࣵrrow;憔ector;楎Āerँगeƀ;AVउऊऐ抣rrow;憤ector;楚iangleƀ;BEतथऩ抲ar;槏qual;抴pƀDTVषूौownVector;楑eeVector;楠ectorĀ;Bॖॗ憿ar;楘ectorĀ;B॥०憼ar;楒ightáΜs̀EFGLSTॾঋকঝঢভqualGreater;拚ullEqual;扦reater;扶ess;檡lantEqual;橽ilde;扲r;쀀𝔏Ā;eঽা拘ftarrow;懚idot;䄿ƀnpw৔ਖਛgȀLRlr৞৷ਂਐeftĀAR০৬rrow;柵ightArrow;柷ightArrow;柶eftĀarγਊightáοightáϊf;쀀𝕃erĀLRਢਬeftArrow;憙ightArrow;憘ƀchtਾੀੂòࡌ;憰rok;䅁;扪Ѐacefiosuਗ਼੝੠੷੼અઋ઎p;椅y;䐜Ādl੥੯iumSpace;恟lintrf;愳r;쀀𝔐nusPlus;戓pf;쀀𝕄cò੶;䎜ҀJacefostuણધભીଔଙඑ඗ඞcy;䐊cute;䅃ƀaey઴હાron;䅇dil;䅅;䐝ƀgswે૰଎ativeƀMTV૓૟૨ediumSpace;怋hiĀcn૦૘ë૙eryThiî૙tedĀGL૸ଆreaterGreateòٳessLesóੈLine;䀊r;쀀𝔑ȀBnptଢନଷ଺reak;恠BreakingSpace;䂠f;愕ڀ;CDEGHLNPRSTV୕ୖ୪୼஡௫ఄ౞಄ದ೘ൡඅ櫬Āou୛୤ngruent;扢pCap;扭oubleVerticalBar;戦ƀlqxஃஊ஛ement;戉ualĀ;Tஒஓ扠ilde;쀀≂̸ists;戄reater΀;EFGLSTஶஷ஽௉௓௘௥扯qual;扱ullEqual;쀀≧̸reater;쀀≫̸ess;批lantEqual;쀀⩾̸ilde;扵umpń௲௽ownHump;쀀≎̸qual;쀀≏̸eĀfsఊధtTriangleƀ;BEచఛడ拪ar;쀀⧏̸qual;括s̀;EGLSTవశ఼ౄోౘ扮qual;扰reater;扸ess;쀀≪̸lantEqual;쀀⩽̸ilde;扴estedĀGL౨౹reaterGreater;쀀⪢̸essLess;쀀⪡̸recedesƀ;ESಒಓಛ技qual;쀀⪯̸lantEqual;拠ĀeiಫಹverseElement;戌ghtTriangleƀ;BEೋೌ೒拫ar;쀀⧐̸qual;拭ĀquೝഌuareSuĀbp೨೹setĀ;E೰ೳ쀀⊏̸qual;拢ersetĀ;Eഃആ쀀⊐̸qual;拣ƀbcpഓതൎsetĀ;Eഛഞ쀀⊂⃒qual;抈ceedsȀ;ESTലള഻െ抁qual;쀀⪰̸lantEqual;拡ilde;쀀≿̸ersetĀ;E൘൛쀀⊃⃒qual;抉ildeȀ;EFT൮൯൵ൿ扁qual;扄ullEqual;扇ilde;扉erticalBar;戤cr;쀀𝒩ilde耻Ñ䃑;䎝܀Eacdfgmoprstuvලෂ෉෕ෛ෠෧෼ขภยา฿ไlig;䅒cute耻Ó䃓Āiy෎ීrc耻Ô䃔;䐞blac;䅐r;쀀𝔒rave耻Ò䃒ƀaei෮ෲ෶cr;䅌ga;䎩cron;䎟pf;쀀𝕆enCurlyĀDQฎบoubleQuote;怜uote;怘;橔Āclวฬr;쀀𝒪ash耻Ø䃘iŬื฼de耻Õ䃕es;樷ml耻Ö䃖erĀBP๋๠Āar๐๓r;怾acĀek๚๜;揞et;掴arenthesis;揜Ҁacfhilors๿ງຊຏຒດຝະ໼rtialD;戂y;䐟r;쀀𝔓i;䎦;䎠usMinus;䂱Āipຢອncareplanåڝf;愙Ȁ;eio຺ູ໠໤檻cedesȀ;EST່້໏໚扺qual;檯lantEqual;扼ilde;找me;怳Ādp໩໮uct;戏ortionĀ;aȥ໹l;戝Āci༁༆r;쀀𝒫;䎨ȀUfos༑༖༛༟OT耻"䀢r;쀀𝔔pf;愚cr;쀀𝒬؀BEacefhiorsu༾གྷཇའཱིྦྷྪྭ႖ႩႴႾarr;椐G耻®䂮ƀcnrཎནབute;䅔g;柫rĀ;tཛྷཝ憠l;椖ƀaeyཧཬཱron;䅘dil;䅖;䐠Ā;vླྀཹ愜erseĀEUྂྙĀlq྇ྎement;戋uilibrium;懋pEquilibrium;楯r»ཹo;䎡ghtЀACDFTUVa࿁࿫࿳ဢဨၛႇϘĀnr࿆࿒gleBracket;柩rowƀ;BL࿜࿝࿡憒ar;懥eftArrow;懄eiling;按oǵ࿹\0စbleBracket;柧nǔည\0နeeVector;楝ectorĀ;Bဝသ懂ar;楕loor;挋Āerိ၃eƀ;AVဵံြ抢rrow;憦ector;楛iangleƀ;BEၐၑၕ抳ar;槐qual;抵pƀDTVၣၮၸownVector;楏eeVector;楜ectorĀ;Bႂႃ憾ar;楔ectorĀ;B႑႒懀ar;楓Āpuႛ႞f;愝ndImplies;楰ightarrow;懛ĀchႹႼr;愛;憱leDelayed;槴ڀHOacfhimoqstuფჱჷჽᄙᄞᅑᅖᅡᅧᆵᆻᆿĀCcჩხHcy;䐩y;䐨FTcy;䐬cute;䅚ʀ;aeiyᄈᄉᄎᄓᄗ檼ron;䅠dil;䅞rc;䅜;䐡r;쀀𝔖ortȀDLRUᄪᄴᄾᅉownArrow»ОeftArrow»࢚ightArrow»࿝pArrow;憑gma;䎣allCircle;战pf;쀀𝕊ɲᅭ\0\0ᅰt;戚areȀ;ISUᅻᅼᆉᆯ斡ntersection;抓uĀbpᆏᆞsetĀ;Eᆗᆘ抏qual;抑ersetĀ;Eᆨᆩ抐qual;抒nion;抔cr;쀀𝒮ar;拆ȀbcmpᇈᇛሉላĀ;sᇍᇎ拐etĀ;Eᇍᇕqual;抆ĀchᇠህeedsȀ;ESTᇭᇮᇴᇿ扻qual;檰lantEqual;扽ilde;承Tháྌ;我ƀ;esሒሓሣ拑rsetĀ;Eሜም抃qual;抇et»ሓրHRSacfhiorsሾቄ቉ቕ቞ቱቶኟዂወዑORN耻Þ䃞ADE;愢ĀHc቎ቒcy;䐋y;䐦Ābuቚቜ;䀉;䎤ƀaeyብቪቯron;䅤dil;䅢;䐢r;쀀𝔗Āeiቻ኉ǲኀ\0ኇefore;戴a;䎘Ācn኎ኘkSpace;쀀  Space;怉ldeȀ;EFTካኬኲኼ戼qual;扃ullEqual;扅ilde;扈pf;쀀𝕋ipleDot;惛Āctዖዛr;쀀𝒯rok;䅦ૡዷጎጚጦ\0ጬጱ\0\0\0\0\0ጸጽ፷ᎅ\0᏿ᐄᐊᐐĀcrዻጁute耻Ú䃚rĀ;oጇገ憟cir;楉rǣጓ\0጖y;䐎ve;䅬Āiyጞጣrc耻Û䃛;䐣blac;䅰r;쀀𝔘rave耻Ù䃙acr;䅪Ādiፁ፩erĀBPፈ፝Āarፍፐr;䁟acĀekፗፙ;揟et;掵arenthesis;揝onĀ;P፰፱拃lus;抎Āgp፻፿on;䅲f;쀀𝕌ЀADETadps᎕ᎮᎸᏄϨᏒᏗᏳrrowƀ;BDᅐᎠᎤar;椒ownArrow;懅ownArrow;憕quilibrium;楮eeĀ;AᏋᏌ报rrow;憥ownáϳerĀLRᏞᏨeftArrow;憖ightArrow;憗iĀ;lᏹᏺ䏒on;䎥ing;䅮cr;쀀𝒰ilde;䅨ml耻Ü䃜ҀDbcdefosvᐧᐬᐰᐳᐾᒅᒊᒐᒖash;披ar;櫫y;䐒ashĀ;lᐻᐼ抩;櫦Āerᑃᑅ;拁ƀbtyᑌᑐᑺar;怖Ā;iᑏᑕcalȀBLSTᑡᑥᑪᑴar;戣ine;䁼eparator;杘ilde;所ThinSpace;怊r;쀀𝔙pf;쀀𝕍cr;쀀𝒱dash;抪ʀcefosᒧᒬᒱᒶᒼirc;䅴dge;拀r;쀀𝔚pf;쀀𝕎cr;쀀𝒲Ȁfiosᓋᓐᓒᓘr;쀀𝔛;䎞pf;쀀𝕏cr;쀀𝒳ҀAIUacfosuᓱᓵᓹᓽᔄᔏᔔᔚᔠcy;䐯cy;䐇cy;䐮cute耻Ý䃝Āiyᔉᔍrc;䅶;䐫r;쀀𝔜pf;쀀𝕐cr;쀀𝒴ml;䅸ЀHacdefosᔵᔹᔿᕋᕏᕝᕠᕤcy;䐖cute;䅹Āayᕄᕉron;䅽;䐗ot;䅻ǲᕔ\0ᕛoWidtè૙a;䎖r;愨pf;愤cr;쀀𝒵௡ᖃᖊᖐ\0ᖰᖶᖿ\0\0\0\0ᗆᗛᗫᙟ᙭\0ᚕ᚛ᚲᚹ\0ᚾcute耻á䃡reve;䄃̀;Ediuyᖜᖝᖡᖣᖨᖭ戾;쀀∾̳;房rc耻â䃢te肻´̆;䐰lig耻æ䃦Ā;r²ᖺ;쀀𝔞rave耻à䃠ĀepᗊᗖĀfpᗏᗔsym;愵èᗓha;䎱ĀapᗟcĀclᗤᗧr;䄁g;樿ɤᗰ\0\0ᘊʀ;adsvᗺᗻᗿᘁᘇ戧nd;橕;橜lope;橘;橚΀;elmrszᘘᘙᘛᘞᘿᙏᙙ戠;榤e»ᘙsdĀ;aᘥᘦ戡ѡᘰᘲᘴᘶᘸᘺᘼᘾ;榨;榩;榪;榫;榬;榭;榮;榯tĀ;vᙅᙆ戟bĀ;dᙌᙍ抾;榝Āptᙔᙗh;戢»¹arr;捼Āgpᙣᙧon;䄅f;쀀𝕒΀;Eaeiop዁ᙻᙽᚂᚄᚇᚊ;橰cir;橯;扊d;手s;䀧roxĀ;e዁ᚒñᚃing耻å䃥ƀctyᚡᚦᚨr;쀀𝒶;䀪mpĀ;e዁ᚯñʈilde耻ã䃣ml耻ä䃤Āciᛂᛈoninôɲnt;樑ࠀNabcdefiklnoprsu᛭ᛱᜰ᜼ᝃᝈ᝸᝽០៦ᠹᡐᜍ᤽᥈ᥰot;櫭Ācrᛶ᜞kȀcepsᜀᜅᜍᜓong;扌psilon;䏶rime;怵imĀ;e᜚᜛戽q;拍Ŷᜢᜦee;抽edĀ;gᜬᜭ挅e»ᜭrkĀ;t፜᜷brk;掶Āoyᜁᝁ;䐱quo;怞ʀcmprtᝓ᝛ᝡᝤᝨausĀ;eĊĉptyv;榰séᜌnoõēƀahwᝯ᝱ᝳ;䎲;愶een;扬r;쀀𝔟g΀costuvwឍឝឳេ៕៛៞ƀaiuបពរðݠrc;旯p»፱ƀdptឤឨឭot;樀lus;樁imes;樂ɱឹ\0\0ើcup;樆ar;昅riangleĀdu៍្own;施p;斳plus;樄eåᑄåᒭarow;植ƀako៭ᠦᠵĀcn៲ᠣkƀlst៺֫᠂ozenge;槫riangleȀ;dlr᠒᠓᠘᠝斴own;斾eft;旂ight;斸k;搣Ʊᠫ\0ᠳƲᠯ\0ᠱ;斒;斑4;斓ck;斈ĀeoᠾᡍĀ;qᡃᡆ쀀=⃥uiv;쀀≡⃥t;挐Ȁptwxᡙᡞᡧᡬf;쀀𝕓Ā;tᏋᡣom»Ꮜtie;拈؀DHUVbdhmptuvᢅᢖᢪᢻᣗᣛᣬ᣿ᤅᤊᤐᤡȀLRlrᢎᢐᢒᢔ;敗;敔;敖;敓ʀ;DUduᢡᢢᢤᢦᢨ敐;敦;敩;敤;敧ȀLRlrᢳᢵᢷᢹ;敝;敚;敜;教΀;HLRhlrᣊᣋᣍᣏᣑᣓᣕ救;敬;散;敠;敫;敢;敟ox;槉ȀLRlrᣤᣦᣨᣪ;敕;敒;攐;攌ʀ;DUduڽ᣷᣹᣻᣽;敥;敨;攬;攴inus;抟lus;択imes;抠ȀLRlrᤙᤛᤝ᤟;敛;敘;攘;攔΀;HLRhlrᤰᤱᤳᤵᤷ᤻᤹攂;敪;敡;敞;攼;攤;攜Āevģ᥂bar耻¦䂦Ȁceioᥑᥖᥚᥠr;쀀𝒷mi;恏mĀ;e᜚᜜lƀ;bhᥨᥩᥫ䁜;槅sub;柈Ŭᥴ᥾lĀ;e᥹᥺怢t»᥺pƀ;Eeįᦅᦇ;檮Ā;qۜۛೡᦧ\0᧨ᨑᨕᨲ\0ᨷᩐ\0\0᪴\0\0᫁\0\0ᬡᬮ᭍᭒\0᯽\0ᰌƀcpr᦭ᦲ᧝ute;䄇̀;abcdsᦿᧀᧄ᧊᧕᧙戩nd;橄rcup;橉Āau᧏᧒p;橋p;橇ot;橀;쀀∩︀Āeo᧢᧥t;恁îړȀaeiu᧰᧻ᨁᨅǰ᧵\0᧸s;橍on;䄍dil耻ç䃧rc;䄉psĀ;sᨌᨍ橌m;橐ot;䄋ƀdmnᨛᨠᨦil肻¸ƭptyv;榲t脀¢;eᨭᨮ䂢räƲr;쀀𝔠ƀceiᨽᩀᩍy;䑇ckĀ;mᩇᩈ朓ark»ᩈ;䏇r΀;Ecefms᩟᩠ᩢᩫ᪤᪪᪮旋;槃ƀ;elᩩᩪᩭ䋆q;扗eɡᩴ\0\0᪈rrowĀlr᩼᪁eft;憺ight;憻ʀRSacd᪒᪔᪖᪚᪟»ཇ;擈st;抛irc;抚ash;抝nint;樐id;櫯cir;槂ubsĀ;u᪻᪼晣it»᪼ˬ᫇᫔᫺\0ᬊonĀ;eᫍᫎ䀺Ā;qÇÆɭ᫙\0\0᫢aĀ;t᫞᫟䀬;䁀ƀ;fl᫨᫩᫫戁îᅠeĀmx᫱᫶ent»᫩eóɍǧ᫾\0ᬇĀ;dኻᬂot;橭nôɆƀfryᬐᬔᬗ;쀀𝕔oäɔ脀©;sŕᬝr;愗Āaoᬥᬩrr;憵ss;朗Ācuᬲᬷr;쀀𝒸Ābpᬼ᭄Ā;eᭁᭂ櫏;櫑Ā;eᭉᭊ櫐;櫒dot;拯΀delprvw᭠᭬᭷ᮂᮬᯔ᯹arrĀlr᭨᭪;椸;椵ɰ᭲\0\0᭵r;拞c;拟arrĀ;p᭿ᮀ憶;椽̀;bcdosᮏᮐᮖᮡᮥᮨ截rcap;橈Āauᮛᮞp;橆p;橊ot;抍r;橅;쀀∪︀Ȁalrv᮵ᮿᯞᯣrrĀ;mᮼᮽ憷;椼yƀevwᯇᯔᯘqɰᯎ\0\0ᯒreã᭳uã᭵ee;拎edge;拏en耻¤䂤earrowĀlrᯮ᯳eft»ᮀight»ᮽeäᯝĀciᰁᰇoninôǷnt;戱lcty;挭ঀAHabcdefhijlorstuwz᰸᰻᰿ᱝᱩᱵᲊᲞᲬᲷ᳻᳿ᴍᵻᶑᶫᶻ᷆᷍rò΁ar;楥Ȁglrs᱈ᱍ᱒᱔ger;怠eth;愸òᄳhĀ;vᱚᱛ怐»ऊūᱡᱧarow;椏aã̕Āayᱮᱳron;䄏;䐴ƀ;ao̲ᱼᲄĀgrʿᲁr;懊tseq;橷ƀglmᲑᲔᲘ耻°䂰ta;䎴ptyv;榱ĀirᲣᲨsht;楿;쀀𝔡arĀlrᲳᲵ»ࣜ»သʀaegsv᳂͸᳖᳜᳠mƀ;oș᳊᳔ndĀ;ș᳑uit;晦amma;䏝in;拲ƀ;io᳧᳨᳸䃷de脀÷;o᳧ᳰntimes;拇nø᳷cy;䑒cɯᴆ\0\0ᴊrn;挞op;挍ʀlptuwᴘᴝᴢᵉᵕlar;䀤f;쀀𝕕ʀ;emps̋ᴭᴷᴽᵂqĀ;d͒ᴳot;扑inus;戸lus;戔quare;抡blebarwedgåúnƀadhᄮᵝᵧownarrowóᲃarpoonĀlrᵲᵶefôᲴighôᲶŢᵿᶅkaro÷གɯᶊ\0\0ᶎrn;挟op;挌ƀcotᶘᶣᶦĀryᶝᶡ;쀀𝒹;䑕l;槶rok;䄑Ādrᶰᶴot;拱iĀ;fᶺ᠖斿Āah᷀᷃ròЩaòྦangle;榦Āci᷒ᷕy;䑟grarr;柿ऀDacdefglmnopqrstuxḁḉḙḸոḼṉṡṾấắẽỡἪἷὄ὎὚ĀDoḆᴴoôᲉĀcsḎḔute耻é䃩ter;橮ȀaioyḢḧḱḶron;䄛rĀ;cḭḮ扖耻ê䃪lon;払;䑍ot;䄗ĀDrṁṅot;扒;쀀𝔢ƀ;rsṐṑṗ檚ave耻è䃨Ā;dṜṝ檖ot;檘Ȁ;ilsṪṫṲṴ檙nters;揧;愓Ā;dṹṺ檕ot;檗ƀapsẅẉẗcr;䄓tyƀ;svẒẓẕ戅et»ẓpĀ1;ẝẤĳạả;怄;怅怃ĀgsẪẬ;䅋p;怂ĀgpẴẸon;䄙f;쀀𝕖ƀalsỄỎỒrĀ;sỊị拕l;槣us;橱iƀ;lvỚớở䎵on»ớ;䏵ȀcsuvỪỳἋἣĀioữḱrc»Ḯɩỹ\0\0ỻíՈantĀglἂἆtr»ṝess»Ṻƀaeiἒ἖Ἒls;䀽st;扟vĀ;DȵἠD;橸parsl;槥ĀDaἯἳot;打rr;楱ƀcdiἾὁỸr;愯oô͒ĀahὉὋ;䎷耻ð䃰Āmrὓὗl耻ë䃫o;悬ƀcipὡὤὧl;䀡sôծĀeoὬὴctatioîՙnentialåչৡᾒ\0ᾞ\0ᾡᾧ\0\0ῆῌ\0ΐ\0ῦῪ \0 ⁚llingdotseñṄy;䑄male;晀ƀilrᾭᾳ῁lig;耀ﬃɩᾹ\0\0᾽g;耀ﬀig;耀ﬄ;쀀𝔣lig;耀ﬁlig;쀀fjƀaltῙ῜ῡt;晭ig;耀ﬂns;斱of;䆒ǰ΅\0ῳf;쀀𝕗ĀakֿῷĀ;vῼ´拔;櫙artint;樍Āao‌⁕Ācs‑⁒α‚‰‸⁅⁈\0⁐β•‥‧‪‬\0‮耻½䂽;慓耻¼䂼;慕;慙;慛Ƴ‴\0‶;慔;慖ʴ‾⁁\0\0⁃耻¾䂾;慗;慜5;慘ƶ⁌\0⁎;慚;慝8;慞l;恄wn;挢cr;쀀𝒻ࢀEabcdefgijlnorstv₂₉₟₥₰₴⃰⃵⃺⃿℃ℒℸ̗ℾ⅒↞Ā;lٍ₇;檌ƀcmpₐₕ₝ute;䇵maĀ;dₜ᳚䎳;檆reve;䄟Āiy₪₮rc;䄝;䐳ot;䄡Ȁ;lqsؾق₽⃉ƀ;qsؾٌ⃄lanô٥Ȁ;cdl٥⃒⃥⃕c;檩otĀ;o⃜⃝檀Ā;l⃢⃣檂;檄Ā;e⃪⃭쀀⋛︀s;檔r;쀀𝔤Ā;gٳ؛mel;愷cy;䑓Ȁ;Eajٚℌℎℐ;檒;檥;檤ȀEaesℛℝ℩ℴ;扩pĀ;p℣ℤ檊rox»ℤĀ;q℮ℯ檈Ā;q℮ℛim;拧pf;쀀𝕘Āci⅃ⅆr;愊mƀ;el٫ⅎ⅐;檎;檐茀>;cdlqr׮ⅠⅪⅮⅳⅹĀciⅥⅧ;檧r;橺ot;拗Par;榕uest;橼ʀadelsↄⅪ←ٖ↛ǰ↉\0↎proø₞r;楸qĀlqؿ↖lesó₈ií٫Āen↣↭rtneqq;쀀≩︀Å↪ԀAabcefkosy⇄⇇⇱⇵⇺∘∝∯≨≽ròΠȀilmr⇐⇔⇗⇛rsðᒄf»․ilôکĀdr⇠⇤cy;䑊ƀ;cwࣴ⇫⇯ir;楈;憭ar;意irc;䄥ƀalr∁∎∓rtsĀ;u∉∊晥it»∊lip;怦con;抹r;쀀𝔥sĀew∣∩arow;椥arow;椦ʀamopr∺∾≃≞≣rr;懿tht;戻kĀlr≉≓eftarrow;憩ightarrow;憪f;쀀𝕙bar;怕ƀclt≯≴≸r;쀀𝒽asè⇴rok;䄧Ābp⊂⊇ull;恃hen»ᱛૡ⊣\0⊪\0⊸⋅⋎\0⋕⋳\0\0⋸⌢⍧⍢⍿\0⎆⎪⎴cute耻í䃭ƀ;iyݱ⊰⊵rc耻î䃮;䐸Ācx⊼⊿y;䐵cl耻¡䂡ĀfrΟ⋉;쀀𝔦rave耻ì䃬Ȁ;inoܾ⋝⋩⋮Āin⋢⋦nt;樌t;戭fin;槜ta;愩lig;䄳ƀaop⋾⌚⌝ƀcgt⌅⌈⌗r;䄫ƀelpܟ⌏⌓inåގarôܠh;䄱f;抷ed;䆵ʀ;cfotӴ⌬⌱⌽⍁are;愅inĀ;t⌸⌹戞ie;槝doô⌙ʀ;celpݗ⍌⍐⍛⍡al;抺Āgr⍕⍙eróᕣã⍍arhk;樗rod;樼Ȁcgpt⍯⍲⍶⍻y;䑑on;䄯f;쀀𝕚a;䎹uest耻¿䂿Āci⎊⎏r;쀀𝒾nʀ;EdsvӴ⎛⎝⎡ӳ;拹ot;拵Ā;v⎦⎧拴;拳Ā;iݷ⎮lde;䄩ǫ⎸\0⎼cy;䑖l耻ï䃯̀cfmosu⏌⏗⏜⏡⏧⏵Āiy⏑⏕rc;䄵;䐹r;쀀𝔧ath;䈷pf;쀀𝕛ǣ⏬\0⏱r;쀀𝒿rcy;䑘kcy;䑔Ѐacfghjos␋␖␢␧␭␱␵␻ppaĀ;v␓␔䎺;䏰Āey␛␠dil;䄷;䐺r;쀀𝔨reen;䄸cy;䑅cy;䑜pf;쀀𝕜cr;쀀𝓀஀ABEHabcdefghjlmnoprstuv⑰⒁⒆⒍⒑┎┽╚▀♎♞♥♹♽⚚⚲⛘❝❨➋⟀⠁⠒ƀart⑷⑺⑼rò৆òΕail;椛arr;椎Ā;gঔ⒋;檋ar;楢ॣ⒥\0⒪\0⒱\0\0\0\0\0⒵Ⓔ\0ⓆⓈⓍ\0⓹ute;䄺mptyv;榴raîࡌbda;䎻gƀ;dlࢎⓁⓃ;榑åࢎ;檅uo耻«䂫rЀ;bfhlpst࢙ⓞⓦⓩ⓫⓮⓱⓵Ā;f࢝ⓣs;椟s;椝ë≒p;憫l;椹im;楳l;憢ƀ;ae⓿─┄檫il;椙Ā;s┉┊檭;쀀⪭︀ƀabr┕┙┝rr;椌rk;杲Āak┢┬cĀek┨┪;䁻;䁛Āes┱┳;榋lĀdu┹┻;榏;榍Ȁaeuy╆╋╖╘ron;䄾Ādi═╔il;䄼ìࢰâ┩;䐻Ȁcqrs╣╦╭╽a;椶uoĀ;rนᝆĀdu╲╷har;楧shar;楋h;憲ʀ;fgqs▋▌উ◳◿扤tʀahlrt▘▤▷◂◨rrowĀ;t࢙□aé⓶arpoonĀdu▯▴own»њp»०eftarrows;懇ightƀahs◍◖◞rrowĀ;sࣴࢧarpoonó྘quigarro÷⇰hreetimes;拋ƀ;qs▋ও◺lanôবʀ;cdgsব☊☍☝☨c;檨otĀ;o☔☕橿Ā;r☚☛檁;檃Ā;e☢☥쀀⋚︀s;檓ʀadegs☳☹☽♉♋pproøⓆot;拖qĀgq♃♅ôউgtò⒌ôছiíলƀilr♕࣡♚sht;楼;쀀𝔩Ā;Eজ♣;檑š♩♶rĀdu▲♮Ā;l॥♳;楪lk;斄cy;䑙ʀ;achtੈ⚈⚋⚑⚖rò◁orneòᴈard;楫ri;旺Āio⚟⚤dot;䅀ustĀ;a⚬⚭掰che»⚭ȀEaes⚻⚽⛉⛔;扨pĀ;p⛃⛄檉rox»⛄Ā;q⛎⛏檇Ā;q⛎⚻im;拦Ѐabnoptwz⛩⛴⛷✚✯❁❇❐Ānr⛮⛱g;柬r;懽rëࣁgƀlmr⛿✍✔eftĀar০✇ightá৲apsto;柼ightá৽parrowĀlr✥✩efô⓭ight;憬ƀafl✶✹✽r;榅;쀀𝕝us;樭imes;樴š❋❏st;戗áፎƀ;ef❗❘᠀旊nge»❘arĀ;l❤❥䀨t;榓ʀachmt❳❶❼➅➇ròࢨorneòᶌarĀ;d྘➃;業;怎ri;抿̀achiqt➘➝ੀ➢➮➻quo;怹r;쀀𝓁mƀ;egল➪➬;檍;檏Ābu┪➳oĀ;rฟ➹;怚rok;䅂萀<;cdhilqrࠫ⟒☹⟜⟠⟥⟪⟰Āci⟗⟙;檦r;橹reå◲mes;拉arr;楶uest;橻ĀPi⟵⟹ar;榖ƀ;ef⠀भ᠛旃rĀdu⠇⠍shar;楊har;楦Āen⠗⠡rtneqq;쀀≨︀Å⠞܀Dacdefhilnopsu⡀⡅⢂⢎⢓⢠⢥⢨⣚⣢⣤ઃ⣳⤂Dot;戺Ȁclpr⡎⡒⡣⡽r耻¯䂯Āet⡗⡙;時Ā;e⡞⡟朠se»⡟Ā;sျ⡨toȀ;dluျ⡳⡷⡻owîҌefôएðᏑker;斮Āoy⢇⢌mma;権;䐼ash;怔asuredangle»ᘦr;쀀𝔪o;愧ƀcdn⢯⢴⣉ro耻µ䂵Ȁ;acdᑤ⢽⣀⣄sôᚧir;櫰ot肻·Ƶusƀ;bd⣒ᤃ⣓戒Ā;uᴼ⣘;横ţ⣞⣡p;櫛ò−ðઁĀdp⣩⣮els;抧f;쀀𝕞Āct⣸⣽r;쀀𝓂pos»ᖝƀ;lm⤉⤊⤍䎼timap;抸ఀGLRVabcdefghijlmoprstuvw⥂⥓⥾⦉⦘⧚⧩⨕⨚⩘⩝⪃⪕⪤⪨⬄⬇⭄⭿⮮ⰴⱧⱼ⳩Āgt⥇⥋;쀀⋙̸Ā;v⥐௏쀀≫⃒ƀelt⥚⥲⥶ftĀar⥡⥧rrow;懍ightarrow;懎;쀀⋘̸Ā;v⥻ే쀀≪⃒ightarrow;懏ĀDd⦎⦓ash;抯ash;抮ʀbcnpt⦣⦧⦬⦱⧌la»˞ute;䅄g;쀀∠⃒ʀ;Eiop඄⦼⧀⧅⧈;쀀⩰̸d;쀀≋̸s;䅉roø඄urĀ;a⧓⧔普lĀ;s⧓ସǳ⧟\0⧣p肻 ଷmpĀ;e௹ఀʀaeouy⧴⧾⨃⨐⨓ǰ⧹\0⧻;橃on;䅈dil;䅆ngĀ;dൾ⨊ot;쀀⩭̸p;橂;䐽ash;怓΀;Aadqsxஒ⨩⨭⨻⩁⩅⩐rr;懗rĀhr⨳⨶k;椤Ā;oᏲᏰot;쀀≐̸uiöୣĀei⩊⩎ar;椨í஘istĀ;s஠டr;쀀𝔫ȀEest௅⩦⩹⩼ƀ;qs஼⩭௡ƀ;qs஼௅⩴lanô௢ií௪Ā;rஶ⪁»ஷƀAap⪊⪍⪑rò⥱rr;憮ar;櫲ƀ;svྍ⪜ྌĀ;d⪡⪢拼;拺cy;䑚΀AEadest⪷⪺⪾⫂⫅⫶⫹rò⥦;쀀≦̸rr;憚r;急Ȁ;fqs఻⫎⫣⫯tĀar⫔⫙rro÷⫁ightarro÷⪐ƀ;qs఻⪺⫪lanôౕĀ;sౕ⫴»శiíౝĀ;rవ⫾iĀ;eచథiäඐĀpt⬌⬑f;쀀𝕟膀¬;in⬙⬚⬶䂬nȀ;Edvஉ⬤⬨⬮;쀀⋹̸ot;쀀⋵̸ǡஉ⬳⬵;拷;拶iĀ;vಸ⬼ǡಸ⭁⭃;拾;拽ƀaor⭋⭣⭩rȀ;ast୻⭕⭚⭟lleì୻l;쀀⫽⃥;쀀∂̸lint;樔ƀ;ceಒ⭰⭳uåಥĀ;cಘ⭸Ā;eಒ⭽ñಘȀAait⮈⮋⮝⮧rò⦈rrƀ;cw⮔⮕⮙憛;쀀⤳̸;쀀↝̸ghtarrow»⮕riĀ;eೋೖ΀chimpqu⮽⯍⯙⬄୸⯤⯯Ȁ;cerല⯆ഷ⯉uå൅;쀀𝓃ortɭ⬅\0\0⯖ará⭖mĀ;e൮⯟Ā;q൴൳suĀbp⯫⯭å೸åഋƀbcp⯶ⰑⰙȀ;Ees⯿ⰀഢⰄ抄;쀀⫅̸etĀ;eഛⰋqĀ;qണⰀcĀ;eലⰗñസȀ;EesⰢⰣൟⰧ抅;쀀⫆̸etĀ;e൘ⰮqĀ;qൠⰣȀgilrⰽⰿⱅⱇìௗlde耻ñ䃱çృiangleĀlrⱒⱜeftĀ;eచⱚñదightĀ;eೋⱥñ೗Ā;mⱬⱭ䎽ƀ;esⱴⱵⱹ䀣ro;愖p;怇ҀDHadgilrsⲏⲔⲙⲞⲣⲰⲶⳓⳣash;抭arr;椄p;쀀≍⃒ash;抬ĀetⲨⲬ;쀀≥⃒;쀀>⃒nfin;槞ƀAetⲽⳁⳅrr;椂;쀀≤⃒Ā;rⳊⳍ쀀<⃒ie;쀀⊴⃒ĀAtⳘⳜrr;椃rie;쀀⊵⃒im;쀀∼⃒ƀAan⳰⳴ⴂrr;懖rĀhr⳺⳽k;椣Ā;oᏧᏥear;椧ቓ᪕\0\0\0\0\0\0\0\0\0\0\0\0\0ⴭ\0ⴸⵈⵠⵥ⵲ⶄᬇ\0\0ⶍⶫ\0ⷈⷎ\0ⷜ⸙⸫⸾⹃Ācsⴱ᪗ute耻ó䃳ĀiyⴼⵅrĀ;c᪞ⵂ耻ô䃴;䐾ʀabios᪠ⵒⵗǈⵚlac;䅑v;樸old;榼lig;䅓Ācr⵩⵭ir;榿;쀀𝔬ͯ⵹\0\0⵼\0ⶂn;䋛ave耻ò䃲;槁Ābmⶈ෴ar;榵Ȁacitⶕ⶘ⶥⶨrò᪀Āir⶝ⶠr;榾oss;榻nå๒;槀ƀaeiⶱⶵⶹcr;䅍ga;䏉ƀcdnⷀⷅǍron;䎿;榶pf;쀀𝕠ƀaelⷔ⷗ǒr;榷rp;榹΀;adiosvⷪⷫⷮ⸈⸍⸐⸖戨rò᪆Ȁ;efmⷷⷸ⸂⸅橝rĀ;oⷾⷿ愴f»ⷿ耻ª䂪耻º䂺gof;抶r;橖lope;橗;橛ƀclo⸟⸡⸧ò⸁ash耻ø䃸l;折iŬⸯ⸴de耻õ䃵esĀ;aǛ⸺s;樶ml耻ö䃶bar;挽ૡ⹞\0⹽\0⺀⺝\0⺢⺹\0\0⻋ຜ\0⼓\0\0⼫⾼\0⿈rȀ;astЃ⹧⹲຅脀¶;l⹭⹮䂶leìЃɩ⹸\0\0⹻m;櫳;櫽y;䐿rʀcimpt⺋⺏⺓ᡥ⺗nt;䀥od;䀮il;怰enk;怱r;쀀𝔭ƀimo⺨⺰⺴Ā;v⺭⺮䏆;䏕maô੶ne;明ƀ;tv⺿⻀⻈䏀chfork»´;䏖Āau⻏⻟nĀck⻕⻝kĀ;h⇴⻛;愎ö⇴sҀ;abcdemst⻳⻴ᤈ⻹⻽⼄⼆⼊⼎䀫cir;樣ir;樢Āouᵀ⼂;樥;橲n肻±ຝim;樦wo;樧ƀipu⼙⼠⼥ntint;樕f;쀀𝕡nd耻£䂣Ԁ;Eaceinosu່⼿⽁⽄⽇⾁⾉⾒⽾⾶;檳p;檷uå໙Ā;c໎⽌̀;acens່⽙⽟⽦⽨⽾pproø⽃urlyeñ໙ñ໎ƀaes⽯⽶⽺pprox;檹qq;檵im;拨iíໟmeĀ;s⾈ຮ怲ƀEas⽸⾐⽺ð⽵ƀdfp໬⾙⾯ƀals⾠⾥⾪lar;挮ine;挒urf;挓Ā;t໻⾴ï໻rel;抰Āci⿀⿅r;쀀𝓅;䏈ncsp;怈̀fiopsu⿚⋢⿟⿥⿫⿱r;쀀𝔮pf;쀀𝕢rime;恗cr;쀀𝓆ƀaeo⿸〉〓tĀei⿾々rnionóڰnt;樖stĀ;e【】䀿ñἙô༔઀ABHabcdefhilmnoprstux぀けさすムㄎㄫㅇㅢㅲㆎ㈆㈕㈤㈩㉘㉮㉲㊐㊰㊷ƀartぇおがròႳòϝail;検aròᱥar;楤΀cdenqrtとふへみわゔヌĀeuねぱ;쀀∽̱te;䅕iãᅮmptyv;榳gȀ;del࿑らるろ;榒;榥å࿑uo耻»䂻rր;abcfhlpstw࿜ガクシスゼゾダッデナp;極Ā;f࿠ゴs;椠;椳s;椞ë≝ð✮l;楅im;楴l;憣;憝Āaiパフil;椚oĀ;nホボ戶aló༞ƀabrョリヮrò៥rk;杳ĀakンヽcĀekヹ・;䁽;䁝Āes㄂㄄;榌lĀduㄊㄌ;榎;榐Ȁaeuyㄗㄜㄧㄩron;䅙Ādiㄡㄥil;䅗ì࿲âヺ;䑀Ȁclqsㄴㄷㄽㅄa;椷dhar;楩uoĀ;rȎȍh;憳ƀacgㅎㅟངlȀ;ipsླྀㅘㅛႜnåႻarôྩt;断ƀilrㅩဣㅮsht;楽;쀀𝔯ĀaoㅷㆆrĀduㅽㅿ»ѻĀ;l႑ㆄ;楬Ā;vㆋㆌ䏁;䏱ƀgns㆕ㇹㇼht̀ahlrstㆤㆰ㇂㇘㇤㇮rrowĀ;t࿜ㆭaéトarpoonĀduㆻㆿowîㅾp»႒eftĀah㇊㇐rrowó࿪arpoonóՑightarrows;應quigarro÷ニhreetimes;拌g;䋚ingdotseñἲƀahm㈍㈐㈓rò࿪aòՑ;怏oustĀ;a㈞㈟掱che»㈟mid;櫮Ȁabpt㈲㈽㉀㉒Ānr㈷㈺g;柭r;懾rëဃƀafl㉇㉊㉎r;榆;쀀𝕣us;樮imes;樵Āap㉝㉧rĀ;g㉣㉤䀩t;榔olint;樒arò㇣Ȁachq㉻㊀Ⴜ㊅quo;怺r;쀀𝓇Ābu・㊊oĀ;rȔȓƀhir㊗㊛㊠reåㇸmes;拊iȀ;efl㊪ၙᠡ㊫方tri;槎luhar;楨;愞ൡ㋕㋛㋟㌬㌸㍱\0㍺㎤\0\0㏬㏰\0㐨㑈㑚㒭㒱㓊㓱\0㘖\0\0㘳cute;䅛quï➺Ԁ;Eaceinpsyᇭ㋳㋵㋿㌂㌋㌏㌟㌦㌩;檴ǰ㋺\0㋼;檸on;䅡uåᇾĀ;dᇳ㌇il;䅟rc;䅝ƀEas㌖㌘㌛;檶p;檺im;择olint;樓iíሄ;䑁otƀ;be㌴ᵇ㌵担;橦΀Aacmstx㍆㍊㍗㍛㍞㍣㍭rr;懘rĀhr㍐㍒ë∨Ā;oਸ਼਴t耻§䂧i;䀻war;椩mĀin㍩ðnuóñt;朶rĀ;o㍶⁕쀀𝔰Ȁacoy㎂㎆㎑㎠rp;景Āhy㎋㎏cy;䑉;䑈rtɭ㎙\0\0㎜iäᑤaraì⹯耻­䂭Āgm㎨㎴maƀ;fv㎱㎲㎲䏃;䏂Ѐ;deglnprካ㏅㏉㏎㏖㏞㏡㏦ot;橪Ā;q኱ኰĀ;E㏓㏔檞;檠Ā;E㏛㏜檝;檟e;扆lus;樤arr;楲aròᄽȀaeit㏸㐈㐏㐗Āls㏽㐄lsetmé㍪hp;樳parsl;槤Ādlᑣ㐔e;挣Ā;e㐜㐝檪Ā;s㐢㐣檬;쀀⪬︀ƀflp㐮㐳㑂tcy;䑌Ā;b㐸㐹䀯Ā;a㐾㐿槄r;挿f;쀀𝕤aĀdr㑍ЂesĀ;u㑔㑕晠it»㑕ƀcsu㑠㑹㒟Āau㑥㑯pĀ;sᆈ㑫;쀀⊓︀pĀ;sᆴ㑵;쀀⊔︀uĀbp㑿㒏ƀ;esᆗᆜ㒆etĀ;eᆗ㒍ñᆝƀ;esᆨᆭ㒖etĀ;eᆨ㒝ñᆮƀ;afᅻ㒦ְrť㒫ֱ»ᅼaròᅈȀcemt㒹㒾㓂㓅r;쀀𝓈tmîñiì㐕aræᆾĀar㓎㓕rĀ;f㓔ឿ昆Āan㓚㓭ightĀep㓣㓪psiloîỠhé⺯s»⡒ʀbcmnp㓻㕞ሉ㖋㖎Ҁ;Edemnprs㔎㔏㔑㔕㔞㔣㔬㔱㔶抂;櫅ot;檽Ā;dᇚ㔚ot;櫃ult;櫁ĀEe㔨㔪;櫋;把lus;檿arr;楹ƀeiu㔽㕒㕕tƀ;en㔎㕅㕋qĀ;qᇚ㔏eqĀ;q㔫㔨m;櫇Ābp㕚㕜;櫕;櫓c̀;acensᇭ㕬㕲㕹㕻㌦pproø㋺urlyeñᇾñᇳƀaes㖂㖈㌛pproø㌚qñ㌗g;晪ڀ123;Edehlmnps㖩㖬㖯ሜ㖲㖴㗀㗉㗕㗚㗟㗨㗭耻¹䂹耻²䂲耻³䂳;櫆Āos㖹㖼t;檾ub;櫘Ā;dሢ㗅ot;櫄sĀou㗏㗒l;柉b;櫗arr;楻ult;櫂ĀEe㗤㗦;櫌;抋lus;櫀ƀeiu㗴㘉㘌tƀ;enሜ㗼㘂qĀ;qሢ㖲eqĀ;q㗧㗤m;櫈Ābp㘑㘓;櫔;櫖ƀAan㘜㘠㘭rr;懙rĀhr㘦㘨ë∮Ā;oਫ਩war;椪lig耻ß䃟௡㙑㙝㙠ዎ㙳㙹\0㙾㛂\0\0\0\0\0㛛㜃\0㜉㝬\0\0\0㞇ɲ㙖\0\0㙛get;挖;䏄rë๟ƀaey㙦㙫㙰ron;䅥dil;䅣;䑂lrec;挕r;쀀𝔱Ȁeiko㚆㚝㚵㚼ǲ㚋\0㚑eĀ4fኄኁaƀ;sv㚘㚙㚛䎸ym;䏑Ācn㚢㚲kĀas㚨㚮pproø዁im»ኬsðኞĀas㚺㚮ð዁rn耻þ䃾Ǭ̟㛆⋧es膀×;bd㛏㛐㛘䃗Ā;aᤏ㛕r;樱;樰ƀeps㛡㛣㜀á⩍Ȁ;bcf҆㛬㛰㛴ot;挶ir;櫱Ā;o㛹㛼쀀𝕥rk;櫚á㍢rime;怴ƀaip㜏㜒㝤dåቈ΀adempst㜡㝍㝀㝑㝗㝜㝟ngleʀ;dlqr㜰㜱㜶㝀㝂斵own»ᶻeftĀ;e⠀㜾ñम;扜ightĀ;e㊪㝋ñၚot;旬inus;樺lus;樹b;槍ime;樻ezium;揢ƀcht㝲㝽㞁Āry㝷㝻;쀀𝓉;䑆cy;䑛rok;䅧Āio㞋㞎xô᝷headĀlr㞗㞠eftarro÷ࡏightarrow»ཝऀAHabcdfghlmoprstuw㟐㟓㟗㟤㟰㟼㠎㠜㠣㠴㡑㡝㡫㢩㣌㣒㣪㣶ròϭar;楣Ācr㟜㟢ute耻ú䃺òᅐrǣ㟪\0㟭y;䑞ve;䅭Āiy㟵㟺rc耻û䃻;䑃ƀabh㠃㠆㠋ròᎭlac;䅱aòᏃĀir㠓㠘sht;楾;쀀𝔲rave耻ù䃹š㠧㠱rĀlr㠬㠮»ॗ»ႃlk;斀Āct㠹㡍ɯ㠿\0\0㡊rnĀ;e㡅㡆挜r»㡆op;挏ri;旸Āal㡖㡚cr;䅫肻¨͉Āgp㡢㡦on;䅳f;쀀𝕦̀adhlsuᅋ㡸㡽፲㢑㢠ownáᎳarpoonĀlr㢈㢌efô㠭ighô㠯iƀ;hl㢙㢚㢜䏅»ᏺon»㢚parrows;懈ƀcit㢰㣄㣈ɯ㢶\0\0㣁rnĀ;e㢼㢽挝r»㢽op;挎ng;䅯ri;旹cr;쀀𝓊ƀdir㣙㣝㣢ot;拰lde;䅩iĀ;f㜰㣨»᠓Āam㣯㣲rò㢨l耻ü䃼angle;榧ހABDacdeflnoprsz㤜㤟㤩㤭㦵㦸㦽㧟㧤㧨㧳㧹㧽㨁㨠ròϷarĀ;v㤦㤧櫨;櫩asèϡĀnr㤲㤷grt;榜΀eknprst㓣㥆㥋㥒㥝㥤㦖appá␕othinçẖƀhir㓫⻈㥙opô⾵Ā;hᎷ㥢ïㆍĀiu㥩㥭gmá㎳Ābp㥲㦄setneqĀ;q㥽㦀쀀⊊︀;쀀⫋︀setneqĀ;q㦏㦒쀀⊋︀;쀀⫌︀Āhr㦛㦟etá㚜iangleĀlr㦪㦯eft»थight»ၑy;䐲ash»ံƀelr㧄㧒㧗ƀ;beⷪ㧋㧏ar;抻q;扚lip;拮Ābt㧜ᑨaòᑩr;쀀𝔳tré㦮suĀbp㧯㧱»ജ»൙pf;쀀𝕧roð໻tré㦴Ācu㨆㨋r;쀀𝓋Ābp㨐㨘nĀEe㦀㨖»㥾nĀEe㦒㨞»㦐igzag;榚΀cefoprs㨶㨻㩖㩛㩔㩡㩪irc;䅵Ādi㩀㩑Ābg㩅㩉ar;機eĀ;qᗺ㩏;扙erp;愘r;쀀𝔴pf;쀀𝕨Ā;eᑹ㩦atèᑹcr;쀀𝓌ૣណ㪇\0㪋\0㪐㪛\0\0㪝㪨㪫㪯\0\0㫃㫎\0㫘ៜ៟tré៑r;쀀𝔵ĀAa㪔㪗ròσrò৶;䎾ĀAa㪡㪤ròθrò৫að✓is;拻ƀdptឤ㪵㪾Āfl㪺ឩ;쀀𝕩imåឲĀAa㫇㫊ròώròਁĀcq㫒ីr;쀀𝓍Āpt៖㫜ré។Ѐacefiosu㫰㫽㬈㬌㬑㬕㬛㬡cĀuy㫶㫻te耻ý䃽;䑏Āiy㬂㬆rc;䅷;䑋n耻¥䂥r;쀀𝔶cy;䑗pf;쀀𝕪cr;쀀𝓎Ācm㬦㬩y;䑎l耻ÿ䃿Ԁacdefhiosw㭂㭈㭔㭘㭤㭩㭭㭴㭺㮀cute;䅺Āay㭍㭒ron;䅾;䐷ot;䅼Āet㭝㭡træᕟa;䎶r;쀀𝔷cy;䐶grarr;懝pf;쀀𝕫cr;쀀𝓏Ājn㮅㮇;怍j;怌'.split("").map(function(t){return t.charCodeAt(0)}))),pu}var gu={},ju;function De(){return ju||(ju=1,Object.defineProperty(gu,"__esModule",{value:true}),gu.default=new Uint16Array("Ȁaglq	\x1Bɭ\0\0p;䀦os;䀧t;䀾t;䀼uot;䀢".split("").map(function(t){return t.charCodeAt(0)}))),gu}var Au={},Hu;function Uu(){return Hu||(Hu=1,(function(t){var w;Object.defineProperty(t,"__esModule",{value:true}),t.replaceCodePoint=t.fromCodePoint=void 0;var o=new Map([[0,65533],[128,8364],[130,8218],[131,402],[132,8222],[133,8230],[134,8224],[135,8225],[136,710],[137,8240],[138,352],[139,8249],[140,338],[142,381],[145,8216],[146,8217],[147,8220],[148,8221],[149,8226],[150,8211],[151,8212],[152,732],[153,8482],[154,353],[155,8250],[156,339],[158,382],[159,376]]);t.fromCodePoint=(w=String.fromCodePoint)!==null&&w!==void 0?w:function(y){var b="";return y>65535&&(y-=65536,b+=String.fromCharCode(y>>>10&1023|55296),y=56320|y&1023),b+=String.fromCharCode(y),b};function n(y){var b;return y>=55296&&y<=57343||y>1114111?65533:(b=o.get(y))!==null&&b!==void 0?b:y}t.replaceCodePoint=n;function A(y){return (0, t.fromCodePoint)(n(y))}t.default=A;})(Au)),Au}var Vu;function Tu(){return Vu||(Vu=1,(function(t){var w=K&&K.__createBinding||(Object.create?(function(p,_,D,O){O===void 0&&(O=D);var P=Object.getOwnPropertyDescriptor(_,D);(!P||("get"in P?!_.__esModule:P.writable||P.configurable))&&(P={enumerable:true,get:function(){return _[D]}}),Object.defineProperty(p,O,P);}):(function(p,_,D,O){O===void 0&&(O=D),p[O]=_[D];})),o=K&&K.__setModuleDefault||(Object.create?(function(p,_){Object.defineProperty(p,"default",{enumerable:true,value:_});}):function(p,_){p.default=_;}),n=K&&K.__importStar||function(p){if(p&&p.__esModule)return p;var _={};if(p!=null)for(var D in p)D!=="default"&&Object.prototype.hasOwnProperty.call(p,D)&&w(_,p,D);return o(_,p),_},A=K&&K.__importDefault||function(p){return p&&p.__esModule?p:{default:p}};Object.defineProperty(t,"__esModule",{value:true}),t.decodeXML=t.decodeHTMLStrict=t.decodeHTMLAttribute=t.decodeHTML=t.determineBranch=t.EntityDecoder=t.DecodingMode=t.BinTrieFlags=t.fromCodePoint=t.replaceCodePoint=t.decodeCodePoint=t.xmlDecodeTree=t.htmlDecodeTree=void 0;var y=A(qe());t.htmlDecodeTree=y.default;var b=A(De());t.xmlDecodeTree=b.default;var f=n(Uu());t.decodeCodePoint=f.default;var c=Uu();Object.defineProperty(t,"replaceCodePoint",{enumerable:true,get:function(){return c.replaceCodePoint}}),Object.defineProperty(t,"fromCodePoint",{enumerable:true,get:function(){return c.fromCodePoint}});var a;(function(p){p[p.NUM=35]="NUM",p[p.SEMI=59]="SEMI",p[p.EQUALS=61]="EQUALS",p[p.ZERO=48]="ZERO",p[p.NINE=57]="NINE",p[p.LOWER_A=97]="LOWER_A",p[p.LOWER_F=102]="LOWER_F",p[p.LOWER_X=120]="LOWER_X",p[p.LOWER_Z=122]="LOWER_Z",p[p.UPPER_A=65]="UPPER_A",p[p.UPPER_F=70]="UPPER_F",p[p.UPPER_Z=90]="UPPER_Z";})(a||(a={}));var v=32,T;(function(p){p[p.VALUE_LENGTH=49152]="VALUE_LENGTH",p[p.BRANCH_LENGTH=16256]="BRANCH_LENGTH",p[p.JUMP_TABLE=127]="JUMP_TABLE";})(T=t.BinTrieFlags||(t.BinTrieFlags={}));function u(p){return p>=a.ZERO&&p<=a.NINE}function e(p){return p>=a.UPPER_A&&p<=a.UPPER_F||p>=a.LOWER_A&&p<=a.LOWER_F}function l(p){return p>=a.UPPER_A&&p<=a.UPPER_Z||p>=a.LOWER_A&&p<=a.LOWER_Z||u(p)}function S(p){return p===a.EQUALS||l(p)}var m;(function(p){p[p.EntityStart=0]="EntityStart",p[p.NumericStart=1]="NumericStart",p[p.NumericDecimal=2]="NumericDecimal",p[p.NumericHex=3]="NumericHex",p[p.NamedEntity=4]="NamedEntity";})(m||(m={}));var r;(function(p){p[p.Legacy=0]="Legacy",p[p.Strict=1]="Strict",p[p.Attribute=2]="Attribute";})(r=t.DecodingMode||(t.DecodingMode={}));var h=(function(){function p(_,D,O){this.decodeTree=_,this.emitCodePoint=D,this.errors=O,this.state=m.EntityStart,this.consumed=1,this.result=0,this.treeIndex=0,this.excess=1,this.decodeMode=r.Strict;}return p.prototype.startEntity=function(_){this.decodeMode=_,this.state=m.EntityStart,this.result=0,this.treeIndex=0,this.excess=1,this.consumed=1;},p.prototype.write=function(_,D){switch(this.state){case m.EntityStart:return _.charCodeAt(D)===a.NUM?(this.state=m.NumericStart,this.consumed+=1,this.stateNumericStart(_,D+1)):(this.state=m.NamedEntity,this.stateNamedEntity(_,D));case m.NumericStart:return this.stateNumericStart(_,D);case m.NumericDecimal:return this.stateNumericDecimal(_,D);case m.NumericHex:return this.stateNumericHex(_,D);case m.NamedEntity:return this.stateNamedEntity(_,D)}},p.prototype.stateNumericStart=function(_,D){return D>=_.length?-1:(_.charCodeAt(D)|v)===a.LOWER_X?(this.state=m.NumericHex,this.consumed+=1,this.stateNumericHex(_,D+1)):(this.state=m.NumericDecimal,this.stateNumericDecimal(_,D))},p.prototype.addToNumericResult=function(_,D,O,P){if(D!==O){var R=O-D;this.result=this.result*Math.pow(P,R)+parseInt(_.substr(D,R),P),this.consumed+=R;}},p.prototype.stateNumericHex=function(_,D){for(var O=D;D<_.length;){var P=_.charCodeAt(D);if(u(P)||e(P))D+=1;else return this.addToNumericResult(_,O,D,16),this.emitNumericEntity(P,3)}return this.addToNumericResult(_,O,D,16),-1},p.prototype.stateNumericDecimal=function(_,D){for(var O=D;D<_.length;){var P=_.charCodeAt(D);if(u(P))D+=1;else return this.addToNumericResult(_,O,D,10),this.emitNumericEntity(P,2)}return this.addToNumericResult(_,O,D,10),-1},p.prototype.emitNumericEntity=function(_,D){var O;if(this.consumed<=D)return (O=this.errors)===null||O===void 0||O.absenceOfDigitsInNumericCharacterReference(this.consumed),0;if(_===a.SEMI)this.consumed+=1;else if(this.decodeMode===r.Strict)return 0;return this.emitCodePoint((0, f.replaceCodePoint)(this.result),this.consumed),this.errors&&(_!==a.SEMI&&this.errors.missingSemicolonAfterCharacterReference(),this.errors.validateNumericCharacterReference(this.result)),this.consumed},p.prototype.stateNamedEntity=function(_,D){for(var O=this.decodeTree,P=O[this.treeIndex],R=(P&T.VALUE_LENGTH)>>14;D<_.length;D++,this.excess++){var V=_.charCodeAt(D);if(this.treeIndex=s(O,P,this.treeIndex+Math.max(1,R),V),this.treeIndex<0)return this.result===0||this.decodeMode===r.Attribute&&(R===0||S(V))?0:this.emitNotTerminatedNamedEntity();if(P=O[this.treeIndex],R=(P&T.VALUE_LENGTH)>>14,R!==0){if(V===a.SEMI)return this.emitNamedEntityData(this.treeIndex,R,this.consumed+this.excess);this.decodeMode!==r.Strict&&(this.result=this.treeIndex,this.consumed+=this.excess,this.excess=0);}}return  -1},p.prototype.emitNotTerminatedNamedEntity=function(){var _,D=this,O=D.result,P=D.decodeTree,R=(P[O]&T.VALUE_LENGTH)>>14;return this.emitNamedEntityData(O,R,this.consumed),(_=this.errors)===null||_===void 0||_.missingSemicolonAfterCharacterReference(),this.consumed},p.prototype.emitNamedEntityData=function(_,D,O){var P=this.decodeTree;return this.emitCodePoint(D===1?P[_]&~T.VALUE_LENGTH:P[_+1],O),D===3&&this.emitCodePoint(P[_+2],O),O},p.prototype.end=function(){var _;switch(this.state){case m.NamedEntity:return this.result!==0&&(this.decodeMode!==r.Attribute||this.result===this.treeIndex)?this.emitNotTerminatedNamedEntity():0;case m.NumericDecimal:return this.emitNumericEntity(0,2);case m.NumericHex:return this.emitNumericEntity(0,3);case m.NumericStart:return (_=this.errors)===null||_===void 0||_.absenceOfDigitsInNumericCharacterReference(this.consumed),0;case m.EntityStart:return 0}},p})();t.EntityDecoder=h;function d(p){var _="",D=new h(p,function(O){return _+=(0, f.fromCodePoint)(O)});return function(P,R){for(var V=0,F=0;(F=P.indexOf("&",F))>=0;){_+=P.slice(V,F),D.startEntity(R);var z=D.write(P,F+1);if(z<0){V=F+D.end();break}V=F+z,F=z===0?V+1:V;}var Q=_+P.slice(V);return _="",Q}}function s(p,_,D,O){var P=(_&T.BRANCH_LENGTH)>>7,R=_&T.JUMP_TABLE;if(P===0)return R!==0&&O===R?D:-1;if(R){var V=O-R;return V<0||V>=P?-1:p[D+V]-1}for(var F=D,z=F+P-1;F<=z;){var Q=F+z>>>1,su=p[Q];if(su<O)F=Q+1;else if(su>O)z=Q-1;else return p[Q+P]}return  -1}t.determineBranch=s;var i=d(y.default),g=d(b.default);function x(p,_){return _===void 0&&(_=r.Legacy),i(p,_)}t.decodeHTML=x;function N(p){return i(p,r.Attribute)}t.decodeHTMLAttribute=N;function L(p){return i(p,r.Strict)}t.decodeHTMLStrict=L;function C(p){return g(p,r.Strict)}t.decodeXML=C;})(K)),K}var Fu;function ge(){return Fu||(Fu=1,(function(t){Object.defineProperty(t,"__esModule",{value:true}),t.QuoteType=void 0;var w=Tu(),o;(function(u){u[u.Tab=9]="Tab",u[u.NewLine=10]="NewLine",u[u.FormFeed=12]="FormFeed",u[u.CarriageReturn=13]="CarriageReturn",u[u.Space=32]="Space",u[u.ExclamationMark=33]="ExclamationMark",u[u.Number=35]="Number",u[u.Amp=38]="Amp",u[u.SingleQuote=39]="SingleQuote",u[u.DoubleQuote=34]="DoubleQuote",u[u.Dash=45]="Dash",u[u.Slash=47]="Slash",u[u.Zero=48]="Zero",u[u.Nine=57]="Nine",u[u.Semi=59]="Semi",u[u.Lt=60]="Lt",u[u.Eq=61]="Eq",u[u.Gt=62]="Gt",u[u.Questionmark=63]="Questionmark",u[u.UpperA=65]="UpperA",u[u.LowerA=97]="LowerA",u[u.UpperF=70]="UpperF",u[u.LowerF=102]="LowerF",u[u.UpperZ=90]="UpperZ",u[u.LowerZ=122]="LowerZ",u[u.LowerX=120]="LowerX",u[u.OpeningSquareBracket=91]="OpeningSquareBracket";})(o||(o={}));var n;(function(u){u[u.Text=1]="Text",u[u.BeforeTagName=2]="BeforeTagName",u[u.InTagName=3]="InTagName",u[u.InSelfClosingTag=4]="InSelfClosingTag",u[u.BeforeClosingTagName=5]="BeforeClosingTagName",u[u.InClosingTagName=6]="InClosingTagName",u[u.AfterClosingTagName=7]="AfterClosingTagName",u[u.BeforeAttributeName=8]="BeforeAttributeName",u[u.InAttributeName=9]="InAttributeName",u[u.AfterAttributeName=10]="AfterAttributeName",u[u.BeforeAttributeValue=11]="BeforeAttributeValue",u[u.InAttributeValueDq=12]="InAttributeValueDq",u[u.InAttributeValueSq=13]="InAttributeValueSq",u[u.InAttributeValueNq=14]="InAttributeValueNq",u[u.BeforeDeclaration=15]="BeforeDeclaration",u[u.InDeclaration=16]="InDeclaration",u[u.InProcessingInstruction=17]="InProcessingInstruction",u[u.BeforeComment=18]="BeforeComment",u[u.CDATASequence=19]="CDATASequence",u[u.InSpecialComment=20]="InSpecialComment",u[u.InCommentLike=21]="InCommentLike",u[u.BeforeSpecialS=22]="BeforeSpecialS",u[u.SpecialStartSequence=23]="SpecialStartSequence",u[u.InSpecialTag=24]="InSpecialTag",u[u.BeforeEntity=25]="BeforeEntity",u[u.BeforeNumericEntity=26]="BeforeNumericEntity",u[u.InNamedEntity=27]="InNamedEntity",u[u.InNumericEntity=28]="InNumericEntity",u[u.InHexEntity=29]="InHexEntity";})(n||(n={}));function A(u){return u===o.Space||u===o.NewLine||u===o.Tab||u===o.FormFeed||u===o.CarriageReturn}function y(u){return u===o.Slash||u===o.Gt||A(u)}function b(u){return u>=o.Zero&&u<=o.Nine}function f(u){return u>=o.LowerA&&u<=o.LowerZ||u>=o.UpperA&&u<=o.UpperZ}function c(u){return u>=o.UpperA&&u<=o.UpperF||u>=o.LowerA&&u<=o.LowerF}var a;(function(u){u[u.NoValue=0]="NoValue",u[u.Unquoted=1]="Unquoted",u[u.Single=2]="Single",u[u.Double=3]="Double";})(a=t.QuoteType||(t.QuoteType={}));var v={Cdata:new Uint8Array([67,68,65,84,65,91]),CdataEnd:new Uint8Array([93,93,62]),CommentEnd:new Uint8Array([45,45,62]),ScriptEnd:new Uint8Array([60,47,115,99,114,105,112,116]),StyleEnd:new Uint8Array([60,47,115,116,121,108,101]),TitleEnd:new Uint8Array([60,47,116,105,116,108,101])},T=(function(){function u(e,l){var S=e.xmlMode,m=S===void 0?false:S,r=e.decodeEntities,h=r===void 0?true:r;this.cbs=l,this.state=n.Text,this.buffer="",this.sectionStart=0,this.index=0,this.baseState=n.Text,this.isSpecial=false,this.running=true,this.offset=0,this.currentSequence=void 0,this.sequenceIndex=0,this.trieIndex=0,this.trieCurrent=0,this.entityResult=0,this.entityExcess=0,this.xmlMode=m,this.decodeEntities=h,this.entityTrie=m?w.xmlDecodeTree:w.htmlDecodeTree;}return u.prototype.reset=function(){this.state=n.Text,this.buffer="",this.sectionStart=0,this.index=0,this.baseState=n.Text,this.currentSequence=void 0,this.running=true,this.offset=0;},u.prototype.write=function(e){this.offset+=this.buffer.length,this.buffer=e,this.parse();},u.prototype.end=function(){this.running&&this.finish();},u.prototype.pause=function(){this.running=false;},u.prototype.resume=function(){this.running=true,this.index<this.buffer.length+this.offset&&this.parse();},u.prototype.getIndex=function(){return this.index},u.prototype.getSectionStart=function(){return this.sectionStart},u.prototype.stateText=function(e){e===o.Lt||!this.decodeEntities&&this.fastForwardTo(o.Lt)?(this.index>this.sectionStart&&this.cbs.ontext(this.sectionStart,this.index),this.state=n.BeforeTagName,this.sectionStart=this.index):this.decodeEntities&&e===o.Amp&&(this.state=n.BeforeEntity);},u.prototype.stateSpecialStartSequence=function(e){var l=this.sequenceIndex===this.currentSequence.length,S=l?y(e):(e|32)===this.currentSequence[this.sequenceIndex];if(!S)this.isSpecial=false;else if(!l){this.sequenceIndex++;return}this.sequenceIndex=0,this.state=n.InTagName,this.stateInTagName(e);},u.prototype.stateInSpecialTag=function(e){if(this.sequenceIndex===this.currentSequence.length){if(e===o.Gt||A(e)){var l=this.index-this.currentSequence.length;if(this.sectionStart<l){var S=this.index;this.index=l,this.cbs.ontext(this.sectionStart,l),this.index=S;}this.isSpecial=false,this.sectionStart=l+2,this.stateInClosingTagName(e);return}this.sequenceIndex=0;}(e|32)===this.currentSequence[this.sequenceIndex]?this.sequenceIndex+=1:this.sequenceIndex===0?this.currentSequence===v.TitleEnd?this.decodeEntities&&e===o.Amp&&(this.state=n.BeforeEntity):this.fastForwardTo(o.Lt)&&(this.sequenceIndex=1):this.sequenceIndex=+(e===o.Lt);},u.prototype.stateCDATASequence=function(e){e===v.Cdata[this.sequenceIndex]?++this.sequenceIndex===v.Cdata.length&&(this.state=n.InCommentLike,this.currentSequence=v.CdataEnd,this.sequenceIndex=0,this.sectionStart=this.index+1):(this.sequenceIndex=0,this.state=n.InDeclaration,this.stateInDeclaration(e));},u.prototype.fastForwardTo=function(e){for(;++this.index<this.buffer.length+this.offset;)if(this.buffer.charCodeAt(this.index-this.offset)===e)return  true;return this.index=this.buffer.length+this.offset-1,false},u.prototype.stateInCommentLike=function(e){e===this.currentSequence[this.sequenceIndex]?++this.sequenceIndex===this.currentSequence.length&&(this.currentSequence===v.CdataEnd?this.cbs.oncdata(this.sectionStart,this.index,2):this.cbs.oncomment(this.sectionStart,this.index,2),this.sequenceIndex=0,this.sectionStart=this.index+1,this.state=n.Text):this.sequenceIndex===0?this.fastForwardTo(this.currentSequence[0])&&(this.sequenceIndex=1):e!==this.currentSequence[this.sequenceIndex-1]&&(this.sequenceIndex=0);},u.prototype.isTagStartChar=function(e){return this.xmlMode?!y(e):f(e)},u.prototype.startSpecial=function(e,l){this.isSpecial=true,this.currentSequence=e,this.sequenceIndex=l,this.state=n.SpecialStartSequence;},u.prototype.stateBeforeTagName=function(e){if(e===o.ExclamationMark)this.state=n.BeforeDeclaration,this.sectionStart=this.index+1;else if(e===o.Questionmark)this.state=n.InProcessingInstruction,this.sectionStart=this.index+1;else if(this.isTagStartChar(e)){var l=e|32;this.sectionStart=this.index,!this.xmlMode&&l===v.TitleEnd[2]?this.startSpecial(v.TitleEnd,3):this.state=!this.xmlMode&&l===v.ScriptEnd[2]?n.BeforeSpecialS:n.InTagName;}else e===o.Slash?this.state=n.BeforeClosingTagName:(this.state=n.Text,this.stateText(e));},u.prototype.stateInTagName=function(e){y(e)&&(this.cbs.onopentagname(this.sectionStart,this.index),this.sectionStart=-1,this.state=n.BeforeAttributeName,this.stateBeforeAttributeName(e));},u.prototype.stateBeforeClosingTagName=function(e){A(e)||(e===o.Gt?this.state=n.Text:(this.state=this.isTagStartChar(e)?n.InClosingTagName:n.InSpecialComment,this.sectionStart=this.index));},u.prototype.stateInClosingTagName=function(e){(e===o.Gt||A(e))&&(this.cbs.onclosetag(this.sectionStart,this.index),this.sectionStart=-1,this.state=n.AfterClosingTagName,this.stateAfterClosingTagName(e));},u.prototype.stateAfterClosingTagName=function(e){(e===o.Gt||this.fastForwardTo(o.Gt))&&(this.state=n.Text,this.baseState=n.Text,this.sectionStart=this.index+1);},u.prototype.stateBeforeAttributeName=function(e){e===o.Gt?(this.cbs.onopentagend(this.index),this.isSpecial?(this.state=n.InSpecialTag,this.sequenceIndex=0):this.state=n.Text,this.baseState=this.state,this.sectionStart=this.index+1):e===o.Slash?this.state=n.InSelfClosingTag:A(e)||(this.state=n.InAttributeName,this.sectionStart=this.index);},u.prototype.stateInSelfClosingTag=function(e){e===o.Gt?(this.cbs.onselfclosingtag(this.index),this.state=n.Text,this.baseState=n.Text,this.sectionStart=this.index+1,this.isSpecial=false):A(e)||(this.state=n.BeforeAttributeName,this.stateBeforeAttributeName(e));},u.prototype.stateInAttributeName=function(e){(e===o.Eq||y(e))&&(this.cbs.onattribname(this.sectionStart,this.index),this.sectionStart=-1,this.state=n.AfterAttributeName,this.stateAfterAttributeName(e));},u.prototype.stateAfterAttributeName=function(e){e===o.Eq?this.state=n.BeforeAttributeValue:e===o.Slash||e===o.Gt?(this.cbs.onattribend(a.NoValue,this.index),this.state=n.BeforeAttributeName,this.stateBeforeAttributeName(e)):A(e)||(this.cbs.onattribend(a.NoValue,this.index),this.state=n.InAttributeName,this.sectionStart=this.index);},u.prototype.stateBeforeAttributeValue=function(e){e===o.DoubleQuote?(this.state=n.InAttributeValueDq,this.sectionStart=this.index+1):e===o.SingleQuote?(this.state=n.InAttributeValueSq,this.sectionStart=this.index+1):A(e)||(this.sectionStart=this.index,this.state=n.InAttributeValueNq,this.stateInAttributeValueNoQuotes(e));},u.prototype.handleInAttributeValue=function(e,l){e===l||!this.decodeEntities&&this.fastForwardTo(l)?(this.cbs.onattribdata(this.sectionStart,this.index),this.sectionStart=-1,this.cbs.onattribend(l===o.DoubleQuote?a.Double:a.Single,this.index),this.state=n.BeforeAttributeName):this.decodeEntities&&e===o.Amp&&(this.baseState=this.state,this.state=n.BeforeEntity);},u.prototype.stateInAttributeValueDoubleQuotes=function(e){this.handleInAttributeValue(e,o.DoubleQuote);},u.prototype.stateInAttributeValueSingleQuotes=function(e){this.handleInAttributeValue(e,o.SingleQuote);},u.prototype.stateInAttributeValueNoQuotes=function(e){A(e)||e===o.Gt?(this.cbs.onattribdata(this.sectionStart,this.index),this.sectionStart=-1,this.cbs.onattribend(a.Unquoted,this.index),this.state=n.BeforeAttributeName,this.stateBeforeAttributeName(e)):this.decodeEntities&&e===o.Amp&&(this.baseState=this.state,this.state=n.BeforeEntity);},u.prototype.stateBeforeDeclaration=function(e){e===o.OpeningSquareBracket?(this.state=n.CDATASequence,this.sequenceIndex=0):this.state=e===o.Dash?n.BeforeComment:n.InDeclaration;},u.prototype.stateInDeclaration=function(e){(e===o.Gt||this.fastForwardTo(o.Gt))&&(this.cbs.ondeclaration(this.sectionStart,this.index),this.state=n.Text,this.sectionStart=this.index+1);},u.prototype.stateInProcessingInstruction=function(e){(e===o.Gt||this.fastForwardTo(o.Gt))&&(this.cbs.onprocessinginstruction(this.sectionStart,this.index),this.state=n.Text,this.sectionStart=this.index+1);},u.prototype.stateBeforeComment=function(e){e===o.Dash?(this.state=n.InCommentLike,this.currentSequence=v.CommentEnd,this.sequenceIndex=2,this.sectionStart=this.index+1):this.state=n.InDeclaration;},u.prototype.stateInSpecialComment=function(e){(e===o.Gt||this.fastForwardTo(o.Gt))&&(this.cbs.oncomment(this.sectionStart,this.index,0),this.state=n.Text,this.sectionStart=this.index+1);},u.prototype.stateBeforeSpecialS=function(e){var l=e|32;l===v.ScriptEnd[3]?this.startSpecial(v.ScriptEnd,4):l===v.StyleEnd[3]?this.startSpecial(v.StyleEnd,4):(this.state=n.InTagName,this.stateInTagName(e));},u.prototype.stateBeforeEntity=function(e){this.entityExcess=1,this.entityResult=0,e===o.Number?this.state=n.BeforeNumericEntity:e===o.Amp||(this.trieIndex=0,this.trieCurrent=this.entityTrie[0],this.state=n.InNamedEntity,this.stateInNamedEntity(e));},u.prototype.stateInNamedEntity=function(e){if(this.entityExcess+=1,this.trieIndex=(0, w.determineBranch)(this.entityTrie,this.trieCurrent,this.trieIndex+1,e),this.trieIndex<0){this.emitNamedEntity(),this.index--;return}this.trieCurrent=this.entityTrie[this.trieIndex];var l=this.trieCurrent&w.BinTrieFlags.VALUE_LENGTH;if(l){var S=(l>>14)-1;if(!this.allowLegacyEntity()&&e!==o.Semi)this.trieIndex+=S;else {var m=this.index-this.entityExcess+1;m>this.sectionStart&&this.emitPartial(this.sectionStart,m),this.entityResult=this.trieIndex,this.trieIndex+=S,this.entityExcess=0,this.sectionStart=this.index+1,S===0&&this.emitNamedEntity();}}},u.prototype.emitNamedEntity=function(){if(this.state=this.baseState,this.entityResult!==0){var e=(this.entityTrie[this.entityResult]&w.BinTrieFlags.VALUE_LENGTH)>>14;switch(e){case 1:{this.emitCodePoint(this.entityTrie[this.entityResult]&~w.BinTrieFlags.VALUE_LENGTH);break}case 2:{this.emitCodePoint(this.entityTrie[this.entityResult+1]);break}case 3:this.emitCodePoint(this.entityTrie[this.entityResult+1]),this.emitCodePoint(this.entityTrie[this.entityResult+2]);}}},u.prototype.stateBeforeNumericEntity=function(e){(e|32)===o.LowerX?(this.entityExcess++,this.state=n.InHexEntity):(this.state=n.InNumericEntity,this.stateInNumericEntity(e));},u.prototype.emitNumericEntity=function(e){var l=this.index-this.entityExcess-1,S=l+2+ +(this.state===n.InHexEntity);S!==this.index&&(l>this.sectionStart&&this.emitPartial(this.sectionStart,l),this.sectionStart=this.index+Number(e),this.emitCodePoint((0, w.replaceCodePoint)(this.entityResult))),this.state=this.baseState;},u.prototype.stateInNumericEntity=function(e){e===o.Semi?this.emitNumericEntity(true):b(e)?(this.entityResult=this.entityResult*10+(e-o.Zero),this.entityExcess++):(this.allowLegacyEntity()?this.emitNumericEntity(false):this.state=this.baseState,this.index--);},u.prototype.stateInHexEntity=function(e){e===o.Semi?this.emitNumericEntity(true):b(e)?(this.entityResult=this.entityResult*16+(e-o.Zero),this.entityExcess++):c(e)?(this.entityResult=this.entityResult*16+((e|32)-o.LowerA+10),this.entityExcess++):(this.allowLegacyEntity()?this.emitNumericEntity(false):this.state=this.baseState,this.index--);},u.prototype.allowLegacyEntity=function(){return !this.xmlMode&&(this.baseState===n.Text||this.baseState===n.InSpecialTag)},u.prototype.cleanup=function(){this.running&&this.sectionStart!==this.index&&(this.state===n.Text||this.state===n.InSpecialTag&&this.sequenceIndex===0?(this.cbs.ontext(this.sectionStart,this.index),this.sectionStart=this.index):(this.state===n.InAttributeValueDq||this.state===n.InAttributeValueSq||this.state===n.InAttributeValueNq)&&(this.cbs.onattribdata(this.sectionStart,this.index),this.sectionStart=this.index));},u.prototype.shouldContinue=function(){return this.index<this.buffer.length+this.offset&&this.running},u.prototype.parse=function(){for(;this.shouldContinue();){var e=this.buffer.charCodeAt(this.index-this.offset);switch(this.state){case n.Text:{this.stateText(e);break}case n.SpecialStartSequence:{this.stateSpecialStartSequence(e);break}case n.InSpecialTag:{this.stateInSpecialTag(e);break}case n.CDATASequence:{this.stateCDATASequence(e);break}case n.InAttributeValueDq:{this.stateInAttributeValueDoubleQuotes(e);break}case n.InAttributeName:{this.stateInAttributeName(e);break}case n.InCommentLike:{this.stateInCommentLike(e);break}case n.InSpecialComment:{this.stateInSpecialComment(e);break}case n.BeforeAttributeName:{this.stateBeforeAttributeName(e);break}case n.InTagName:{this.stateInTagName(e);break}case n.InClosingTagName:{this.stateInClosingTagName(e);break}case n.BeforeTagName:{this.stateBeforeTagName(e);break}case n.AfterAttributeName:{this.stateAfterAttributeName(e);break}case n.InAttributeValueSq:{this.stateInAttributeValueSingleQuotes(e);break}case n.BeforeAttributeValue:{this.stateBeforeAttributeValue(e);break}case n.BeforeClosingTagName:{this.stateBeforeClosingTagName(e);break}case n.AfterClosingTagName:{this.stateAfterClosingTagName(e);break}case n.BeforeSpecialS:{this.stateBeforeSpecialS(e);break}case n.InAttributeValueNq:{this.stateInAttributeValueNoQuotes(e);break}case n.InSelfClosingTag:{this.stateInSelfClosingTag(e);break}case n.InDeclaration:{this.stateInDeclaration(e);break}case n.BeforeDeclaration:{this.stateBeforeDeclaration(e);break}case n.BeforeComment:{this.stateBeforeComment(e);break}case n.InProcessingInstruction:{this.stateInProcessingInstruction(e);break}case n.InNamedEntity:{this.stateInNamedEntity(e);break}case n.BeforeEntity:{this.stateBeforeEntity(e);break}case n.InHexEntity:{this.stateInHexEntity(e);break}case n.InNumericEntity:{this.stateInNumericEntity(e);break}default:this.stateBeforeNumericEntity(e);}this.index++;}this.cleanup();},u.prototype.finish=function(){this.state===n.InNamedEntity&&this.emitNamedEntity(),this.sectionStart<this.index&&this.handleTrailingData(),this.cbs.onend();},u.prototype.handleTrailingData=function(){var e=this.buffer.length+this.offset;this.state===n.InCommentLike?this.currentSequence===v.CdataEnd?this.cbs.oncdata(this.sectionStart,e,0):this.cbs.oncomment(this.sectionStart,e,0):this.state===n.InNumericEntity&&this.allowLegacyEntity()?this.emitNumericEntity(false):this.state===n.InHexEntity&&this.allowLegacyEntity()?this.emitNumericEntity(false):this.state===n.InTagName||this.state===n.BeforeAttributeName||this.state===n.BeforeAttributeValue||this.state===n.AfterAttributeName||this.state===n.InAttributeName||this.state===n.InAttributeValueSq||this.state===n.InAttributeValueDq||this.state===n.InAttributeValueNq||this.state===n.InClosingTagName||this.cbs.ontext(this.sectionStart,e);},u.prototype.emitPartial=function(e,l){this.baseState!==n.Text&&this.baseState!==n.InSpecialTag?this.cbs.onattribdata(e,l):this.cbs.ontext(e,l);},u.prototype.emitCodePoint=function(e){this.baseState!==n.Text&&this.baseState!==n.InSpecialTag?this.cbs.onattribentity(e):this.cbs.ontextentity(e);},u})();t.default=T;})(Eu)),Eu}var Gu;function zu(){if(Gu)return Y;Gu=1;var t=Y&&Y.__createBinding||(Object.create?(function(m,r,h,d){d===void 0&&(d=h);var s=Object.getOwnPropertyDescriptor(r,h);(!s||("get"in s?!r.__esModule:s.writable||s.configurable))&&(s={enumerable:true,get:function(){return r[h]}}),Object.defineProperty(m,d,s);}):(function(m,r,h,d){d===void 0&&(d=h),m[d]=r[h];})),w=Y&&Y.__setModuleDefault||(Object.create?(function(m,r){Object.defineProperty(m,"default",{enumerable:true,value:r});}):function(m,r){m.default=r;}),o=Y&&Y.__importStar||function(m){if(m&&m.__esModule)return m;var r={};if(m!=null)for(var h in m)h!=="default"&&Object.prototype.hasOwnProperty.call(m,h)&&t(r,m,h);return w(r,m),r};Object.defineProperty(Y,"__esModule",{value:true}),Y.Parser=void 0;var n=o(ge()),A=Tu(),y=new Set(["input","option","optgroup","select","button","datalist","textarea"]),b=new Set(["p"]),f=new Set(["thead","tbody"]),c=new Set(["dd","dt"]),a=new Set(["rt","rp"]),v=new Map([["tr",new Set(["tr","th","td"])],["th",new Set(["th"])],["td",new Set(["thead","th","td"])],["body",new Set(["head","link","script"])],["li",new Set(["li"])],["p",b],["h1",b],["h2",b],["h3",b],["h4",b],["h5",b],["h6",b],["select",y],["input",y],["output",y],["button",y],["datalist",y],["textarea",y],["option",new Set(["option"])],["optgroup",new Set(["optgroup","option"])],["dd",c],["dt",c],["address",b],["article",b],["aside",b],["blockquote",b],["details",b],["div",b],["dl",b],["fieldset",b],["figcaption",b],["figure",b],["footer",b],["form",b],["header",b],["hr",b],["main",b],["nav",b],["ol",b],["pre",b],["section",b],["table",b],["ul",b],["rt",a],["rp",a],["tbody",f],["tfoot",f]]),T=new Set(["area","base","basefont","br","col","command","embed","frame","hr","img","input","isindex","keygen","link","meta","param","source","track","wbr"]),u=new Set(["math","svg"]),e=new Set(["mi","mo","mn","ms","mtext","annotation-xml","foreignobject","desc","title"]),l=/\s|\//,S=(function(){function m(r,h){h===void 0&&(h={});var d,s,i,g,x;this.options=h,this.startIndex=0,this.endIndex=0,this.openTagStart=0,this.tagname="",this.attribname="",this.attribvalue="",this.attribs=null,this.stack=[],this.foreignContext=[],this.buffers=[],this.bufferOffset=0,this.writeIndex=0,this.ended=false,this.cbs=r??{},this.lowerCaseTagNames=(d=h.lowerCaseTags)!==null&&d!==void 0?d:!h.xmlMode,this.lowerCaseAttributeNames=(s=h.lowerCaseAttributeNames)!==null&&s!==void 0?s:!h.xmlMode,this.tokenizer=new((i=h.Tokenizer)!==null&&i!==void 0?i:n.default)(this.options,this),(x=(g=this.cbs).onparserinit)===null||x===void 0||x.call(g,this);}return m.prototype.ontext=function(r,h){var d,s,i=this.getSlice(r,h);this.endIndex=h-1,(s=(d=this.cbs).ontext)===null||s===void 0||s.call(d,i),this.startIndex=h;},m.prototype.ontextentity=function(r){var h,d,s=this.tokenizer.getSectionStart();this.endIndex=s-1,(d=(h=this.cbs).ontext)===null||d===void 0||d.call(h,(0, A.fromCodePoint)(r)),this.startIndex=s;},m.prototype.isVoidElement=function(r){return !this.options.xmlMode&&T.has(r)},m.prototype.onopentagname=function(r,h){this.endIndex=h;var d=this.getSlice(r,h);this.lowerCaseTagNames&&(d=d.toLowerCase()),this.emitOpenTag(d);},m.prototype.emitOpenTag=function(r){var h,d,s,i;this.openTagStart=this.startIndex,this.tagname=r;var g=!this.options.xmlMode&&v.get(r);if(g)for(;this.stack.length>0&&g.has(this.stack[this.stack.length-1]);){var x=this.stack.pop();(d=(h=this.cbs).onclosetag)===null||d===void 0||d.call(h,x,true);}this.isVoidElement(r)||(this.stack.push(r),u.has(r)?this.foreignContext.push(true):e.has(r)&&this.foreignContext.push(false)),(i=(s=this.cbs).onopentagname)===null||i===void 0||i.call(s,r),this.cbs.onopentag&&(this.attribs={});},m.prototype.endOpenTag=function(r){var h,d;this.startIndex=this.openTagStart,this.attribs&&((d=(h=this.cbs).onopentag)===null||d===void 0||d.call(h,this.tagname,this.attribs,r),this.attribs=null),this.cbs.onclosetag&&this.isVoidElement(this.tagname)&&this.cbs.onclosetag(this.tagname,true),this.tagname="";},m.prototype.onopentagend=function(r){this.endIndex=r,this.endOpenTag(false),this.startIndex=r+1;},m.prototype.onclosetag=function(r,h){var d,s,i,g,x,N;this.endIndex=h;var L=this.getSlice(r,h);if(this.lowerCaseTagNames&&(L=L.toLowerCase()),(u.has(L)||e.has(L))&&this.foreignContext.pop(),this.isVoidElement(L))!this.options.xmlMode&&L==="br"&&((s=(d=this.cbs).onopentagname)===null||s===void 0||s.call(d,"br"),(g=(i=this.cbs).onopentag)===null||g===void 0||g.call(i,"br",{},true),(N=(x=this.cbs).onclosetag)===null||N===void 0||N.call(x,"br",false));else {var C=this.stack.lastIndexOf(L);if(C!==-1)if(this.cbs.onclosetag)for(var p=this.stack.length-C;p--;)this.cbs.onclosetag(this.stack.pop(),p!==0);else this.stack.length=C;else !this.options.xmlMode&&L==="p"&&(this.emitOpenTag("p"),this.closeCurrentTag(true));}this.startIndex=h+1;},m.prototype.onselfclosingtag=function(r){this.endIndex=r,this.options.xmlMode||this.options.recognizeSelfClosing||this.foreignContext[this.foreignContext.length-1]?(this.closeCurrentTag(false),this.startIndex=r+1):this.onopentagend(r);},m.prototype.closeCurrentTag=function(r){var h,d,s=this.tagname;this.endOpenTag(r),this.stack[this.stack.length-1]===s&&((d=(h=this.cbs).onclosetag)===null||d===void 0||d.call(h,s,!r),this.stack.pop());},m.prototype.onattribname=function(r,h){this.startIndex=r;var d=this.getSlice(r,h);this.attribname=this.lowerCaseAttributeNames?d.toLowerCase():d;},m.prototype.onattribdata=function(r,h){this.attribvalue+=this.getSlice(r,h);},m.prototype.onattribentity=function(r){this.attribvalue+=(0, A.fromCodePoint)(r);},m.prototype.onattribend=function(r,h){var d,s;this.endIndex=h,(s=(d=this.cbs).onattribute)===null||s===void 0||s.call(d,this.attribname,this.attribvalue,r===n.QuoteType.Double?'"':r===n.QuoteType.Single?"'":r===n.QuoteType.NoValue?void 0:null),this.attribs&&!Object.prototype.hasOwnProperty.call(this.attribs,this.attribname)&&(this.attribs[this.attribname]=this.attribvalue),this.attribvalue="";},m.prototype.getInstructionName=function(r){var h=r.search(l),d=h<0?r:r.substr(0,h);return this.lowerCaseTagNames&&(d=d.toLowerCase()),d},m.prototype.ondeclaration=function(r,h){this.endIndex=h;var d=this.getSlice(r,h);if(this.cbs.onprocessinginstruction){var s=this.getInstructionName(d);this.cbs.onprocessinginstruction("!".concat(s),"!".concat(d));}this.startIndex=h+1;},m.prototype.onprocessinginstruction=function(r,h){this.endIndex=h;var d=this.getSlice(r,h);if(this.cbs.onprocessinginstruction){var s=this.getInstructionName(d);this.cbs.onprocessinginstruction("?".concat(s),"?".concat(d));}this.startIndex=h+1;},m.prototype.oncomment=function(r,h,d){var s,i,g,x;this.endIndex=h,(i=(s=this.cbs).oncomment)===null||i===void 0||i.call(s,this.getSlice(r,h-d)),(x=(g=this.cbs).oncommentend)===null||x===void 0||x.call(g),this.startIndex=h+1;},m.prototype.oncdata=function(r,h,d){var s,i,g,x,N,L,C,p,_,D;this.endIndex=h;var O=this.getSlice(r,h-d);this.options.xmlMode||this.options.recognizeCDATA?((i=(s=this.cbs).oncdatastart)===null||i===void 0||i.call(s),(x=(g=this.cbs).ontext)===null||x===void 0||x.call(g,O),(L=(N=this.cbs).oncdataend)===null||L===void 0||L.call(N)):((p=(C=this.cbs).oncomment)===null||p===void 0||p.call(C,"[CDATA[".concat(O,"]]")),(D=(_=this.cbs).oncommentend)===null||D===void 0||D.call(_)),this.startIndex=h+1;},m.prototype.onend=function(){var r,h;if(this.cbs.onclosetag){this.endIndex=this.startIndex;for(var d=this.stack.length;d>0;this.cbs.onclosetag(this.stack[--d],true));}(h=(r=this.cbs).onend)===null||h===void 0||h.call(r);},m.prototype.reset=function(){var r,h,d,s;(h=(r=this.cbs).onreset)===null||h===void 0||h.call(r),this.tokenizer.reset(),this.tagname="",this.attribname="",this.attribs=null,this.stack.length=0,this.startIndex=0,this.endIndex=0,(s=(d=this.cbs).onparserinit)===null||s===void 0||s.call(d,this),this.buffers.length=0,this.bufferOffset=0,this.writeIndex=0,this.ended=false;},m.prototype.parseComplete=function(r){this.reset(),this.end(r);},m.prototype.getSlice=function(r,h){for(;r-this.bufferOffset>=this.buffers[0].length;)this.shiftBuffer();for(var d=this.buffers[0].slice(r-this.bufferOffset,h-this.bufferOffset);h-this.bufferOffset>this.buffers[0].length;)this.shiftBuffer(),d+=this.buffers[0].slice(0,h-this.bufferOffset);return d},m.prototype.shiftBuffer=function(){this.bufferOffset+=this.buffers[0].length,this.writeIndex--,this.buffers.shift();},m.prototype.write=function(r){var h,d;if(this.ended){(d=(h=this.cbs).onerror)===null||d===void 0||d.call(h,new Error(".write() after done!"));return}this.buffers.push(r),this.tokenizer.running&&(this.tokenizer.write(r),this.writeIndex++);},m.prototype.end=function(r){var h,d;if(this.ended){(d=(h=this.cbs).onerror)===null||d===void 0||d.call(h,new Error(".end() after done!"));return}r&&this.write(r),this.ended=true,this.tokenizer.end();},m.prototype.pause=function(){this.tokenizer.pause();},m.prototype.resume=function(){for(this.tokenizer.resume();this.tokenizer.running&&this.writeIndex<this.buffers.length;)this.tokenizer.write(this.buffers[this.writeIndex++]);this.ended&&this.tokenizer.end();},m.prototype.parseChunk=function(r){this.write(r);},m.prototype.done=function(r){this.end(r);},m})();return Y.Parser=S,Y}var fu={},Su={},Xu;function hu(){return Xu||(Xu=1,(function(t){Object.defineProperty(t,"__esModule",{value:true}),t.Doctype=t.CDATA=t.Tag=t.Style=t.Script=t.Comment=t.Directive=t.Text=t.Root=t.isTag=t.ElementType=void 0;var w;(function(n){n.Root="root",n.Text="text",n.Directive="directive",n.Comment="comment",n.Script="script",n.Style="style",n.Tag="tag",n.CDATA="cdata",n.Doctype="doctype";})(w=t.ElementType||(t.ElementType={}));function o(n){return n.type===w.Tag||n.type===w.Script||n.type===w.Style}t.isTag=o,t.Root=w.Root,t.Text=w.Text,t.Directive=w.Directive,t.Comment=w.Comment,t.Script=w.Script,t.Style=w.Style,t.Tag=w.Tag,t.CDATA=w.CDATA,t.Doctype=w.Doctype;})(Su)),Su}var k$1={},Wu;function Qu(){if(Wu)return k$1;Wu=1;var t=k$1&&k$1.__extends||(function(){var i=function(g,x){return i=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(N,L){N.__proto__=L;}||function(N,L){for(var C in L)Object.prototype.hasOwnProperty.call(L,C)&&(N[C]=L[C]);},i(g,x)};return function(g,x){if(typeof x!="function"&&x!==null)throw new TypeError("Class extends value "+String(x)+" is not a constructor or null");i(g,x);function N(){this.constructor=g;}g.prototype=x===null?Object.create(x):(N.prototype=x.prototype,new N);}})(),w=k$1&&k$1.__assign||function(){return w=Object.assign||function(i){for(var g,x=1,N=arguments.length;x<N;x++){g=arguments[x];for(var L in g)Object.prototype.hasOwnProperty.call(g,L)&&(i[L]=g[L]);}return i},w.apply(this,arguments)};Object.defineProperty(k$1,"__esModule",{value:true}),k$1.cloneNode=k$1.hasChildren=k$1.isDocument=k$1.isDirective=k$1.isComment=k$1.isText=k$1.isCDATA=k$1.isTag=k$1.Element=k$1.Document=k$1.CDATA=k$1.NodeWithChildren=k$1.ProcessingInstruction=k$1.Comment=k$1.Text=k$1.DataNode=k$1.Node=void 0;var o=hu(),n=(function(){function i(){this.parent=null,this.prev=null,this.next=null,this.startIndex=null,this.endIndex=null;}return Object.defineProperty(i.prototype,"parentNode",{get:function(){return this.parent},set:function(g){this.parent=g;},enumerable:false,configurable:true}),Object.defineProperty(i.prototype,"previousSibling",{get:function(){return this.prev},set:function(g){this.prev=g;},enumerable:false,configurable:true}),Object.defineProperty(i.prototype,"nextSibling",{get:function(){return this.next},set:function(g){this.next=g;},enumerable:false,configurable:true}),i.prototype.cloneNode=function(g){return g===void 0&&(g=false),d(this,g)},i})();k$1.Node=n;var A=(function(i){t(g,i);function g(x){var N=i.call(this)||this;return N.data=x,N}return Object.defineProperty(g.prototype,"nodeValue",{get:function(){return this.data},set:function(x){this.data=x;},enumerable:false,configurable:true}),g})(n);k$1.DataNode=A;var y=(function(i){t(g,i);function g(){var x=i!==null&&i.apply(this,arguments)||this;return x.type=o.ElementType.Text,x}return Object.defineProperty(g.prototype,"nodeType",{get:function(){return 3},enumerable:false,configurable:true}),g})(A);k$1.Text=y;var b=(function(i){t(g,i);function g(){var x=i!==null&&i.apply(this,arguments)||this;return x.type=o.ElementType.Comment,x}return Object.defineProperty(g.prototype,"nodeType",{get:function(){return 8},enumerable:false,configurable:true}),g})(A);k$1.Comment=b;var f=(function(i){t(g,i);function g(x,N){var L=i.call(this,N)||this;return L.name=x,L.type=o.ElementType.Directive,L}return Object.defineProperty(g.prototype,"nodeType",{get:function(){return 1},enumerable:false,configurable:true}),g})(A);k$1.ProcessingInstruction=f;var c=(function(i){t(g,i);function g(x){var N=i.call(this)||this;return N.children=x,N}return Object.defineProperty(g.prototype,"firstChild",{get:function(){var x;return (x=this.children[0])!==null&&x!==void 0?x:null},enumerable:false,configurable:true}),Object.defineProperty(g.prototype,"lastChild",{get:function(){return this.children.length>0?this.children[this.children.length-1]:null},enumerable:false,configurable:true}),Object.defineProperty(g.prototype,"childNodes",{get:function(){return this.children},set:function(x){this.children=x;},enumerable:false,configurable:true}),g})(n);k$1.NodeWithChildren=c;var a=(function(i){t(g,i);function g(){var x=i!==null&&i.apply(this,arguments)||this;return x.type=o.ElementType.CDATA,x}return Object.defineProperty(g.prototype,"nodeType",{get:function(){return 4},enumerable:false,configurable:true}),g})(c);k$1.CDATA=a;var v=(function(i){t(g,i);function g(){var x=i!==null&&i.apply(this,arguments)||this;return x.type=o.ElementType.Root,x}return Object.defineProperty(g.prototype,"nodeType",{get:function(){return 9},enumerable:false,configurable:true}),g})(c);k$1.Document=v;var T=(function(i){t(g,i);function g(x,N,L,C){L===void 0&&(L=[]),C===void 0&&(C=x==="script"?o.ElementType.Script:x==="style"?o.ElementType.Style:o.ElementType.Tag);var p=i.call(this,L)||this;return p.name=x,p.attribs=N,p.type=C,p}return Object.defineProperty(g.prototype,"nodeType",{get:function(){return 1},enumerable:false,configurable:true}),Object.defineProperty(g.prototype,"tagName",{get:function(){return this.name},set:function(x){this.name=x;},enumerable:false,configurable:true}),Object.defineProperty(g.prototype,"attributes",{get:function(){var x=this;return Object.keys(this.attribs).map(function(N){var L,C;return {name:N,value:x.attribs[N],namespace:(L=x["x-attribsNamespace"])===null||L===void 0?void 0:L[N],prefix:(C=x["x-attribsPrefix"])===null||C===void 0?void 0:C[N]}})},enumerable:false,configurable:true}),g})(c);k$1.Element=T;function u(i){return (0, o.isTag)(i)}k$1.isTag=u;function e(i){return i.type===o.ElementType.CDATA}k$1.isCDATA=e;function l(i){return i.type===o.ElementType.Text}k$1.isText=l;function S(i){return i.type===o.ElementType.Comment}k$1.isComment=S;function m(i){return i.type===o.ElementType.Directive}k$1.isDirective=m;function r(i){return i.type===o.ElementType.Root}k$1.isDocument=r;function h(i){return Object.prototype.hasOwnProperty.call(i,"children")}k$1.hasChildren=h;function d(i,g){g===void 0&&(g=false);var x;if(l(i))x=new y(i.data);else if(S(i))x=new b(i.data);else if(u(i)){var N=g?s(i.children):[],L=new T(i.name,w({},i.attribs),N);N.forEach(function(D){return D.parent=L}),i.namespace!=null&&(L.namespace=i.namespace),i["x-attribsNamespace"]&&(L["x-attribsNamespace"]=w({},i["x-attribsNamespace"])),i["x-attribsPrefix"]&&(L["x-attribsPrefix"]=w({},i["x-attribsPrefix"])),x=L;}else if(e(i)){var N=g?s(i.children):[],C=new a(N);N.forEach(function(O){return O.parent=C}),x=C;}else if(r(i)){var N=g?s(i.children):[],p=new v(N);N.forEach(function(O){return O.parent=p}),i["x-mode"]&&(p["x-mode"]=i["x-mode"]),x=p;}else if(m(i)){var _=new f(i.name,i.data);i["x-name"]!=null&&(_["x-name"]=i["x-name"],_["x-publicId"]=i["x-publicId"],_["x-systemId"]=i["x-systemId"]),x=_;}else throw new Error("Not implemented yet: ".concat(i.type));return x.startIndex=i.startIndex,x.endIndex=i.endIndex,i.sourceCodeLocation!=null&&(x.sourceCodeLocation=i.sourceCodeLocation),x}k$1.cloneNode=d;function s(i){for(var g=i.map(function(N){return d(N,true)}),x=1;x<g.length;x++)g[x].prev=g[x-1],g[x-1].next=g[x];return g}return k$1}var Zu;function cu(){return Zu||(Zu=1,(function(t){var w=fu&&fu.__createBinding||(Object.create?(function(f,c,a,v){v===void 0&&(v=a);var T=Object.getOwnPropertyDescriptor(c,a);(!T||("get"in T?!c.__esModule:T.writable||T.configurable))&&(T={enumerable:true,get:function(){return c[a]}}),Object.defineProperty(f,v,T);}):(function(f,c,a,v){v===void 0&&(v=a),f[v]=c[a];})),o=fu&&fu.__exportStar||function(f,c){for(var a in f)a!=="default"&&!Object.prototype.hasOwnProperty.call(c,a)&&w(c,f,a);};Object.defineProperty(t,"__esModule",{value:true}),t.DomHandler=void 0;var n=hu(),A=Qu();o(Qu(),t);var y={withStartIndices:false,withEndIndices:false,xmlMode:false},b=(function(){function f(c,a,v){this.dom=[],this.root=new A.Document(this.dom),this.done=false,this.tagStack=[this.root],this.lastNode=null,this.parser=null,typeof a=="function"&&(v=a,a=y),typeof c=="object"&&(a=c,c=void 0),this.callback=c??null,this.options=a??y,this.elementCB=v??null;}return f.prototype.onparserinit=function(c){this.parser=c;},f.prototype.onreset=function(){this.dom=[],this.root=new A.Document(this.dom),this.done=false,this.tagStack=[this.root],this.lastNode=null,this.parser=null;},f.prototype.onend=function(){this.done||(this.done=true,this.parser=null,this.handleCallback(null));},f.prototype.onerror=function(c){this.handleCallback(c);},f.prototype.onclosetag=function(){this.lastNode=null;var c=this.tagStack.pop();this.options.withEndIndices&&(c.endIndex=this.parser.endIndex),this.elementCB&&this.elementCB(c);},f.prototype.onopentag=function(c,a){var v=this.options.xmlMode?n.ElementType.Tag:void 0,T=new A.Element(c,a,void 0,v);this.addNode(T),this.tagStack.push(T);},f.prototype.ontext=function(c){var a=this.lastNode;if(a&&a.type===n.ElementType.Text)a.data+=c,this.options.withEndIndices&&(a.endIndex=this.parser.endIndex);else {var v=new A.Text(c);this.addNode(v),this.lastNode=v;}},f.prototype.oncomment=function(c){if(this.lastNode&&this.lastNode.type===n.ElementType.Comment){this.lastNode.data+=c;return}var a=new A.Comment(c);this.addNode(a),this.lastNode=a;},f.prototype.oncommentend=function(){this.lastNode=null;},f.prototype.oncdatastart=function(){var c=new A.Text(""),a=new A.CDATA([c]);this.addNode(a),c.parent=a,this.lastNode=c;},f.prototype.oncdataend=function(){this.lastNode=null;},f.prototype.onprocessinginstruction=function(c,a){var v=new A.ProcessingInstruction(c,a);this.addNode(v);},f.prototype.handleCallback=function(c){if(typeof this.callback=="function")this.callback(c,this.dom);else if(c)throw c},f.prototype.addNode=function(c){var a=this.tagStack[this.tagStack.length-1],v=a.children[a.children.length-1];this.options.withStartIndices&&(c.startIndex=this.parser.startIndex),this.options.withEndIndices&&(c.endIndex=this.parser.endIndex),a.children.push(c),v&&(c.prev=v,v.next=c),c.parent=a,this.lastNode=null;},f})();t.DomHandler=b,t.default=b;})(fu)),fu}var lu={},uu={},W={},Nu={},tu={},mu={},Ju;function Ie(){if(Ju)return mu;Ju=1,Object.defineProperty(mu,"__esModule",{value:true});function t(w){for(var o=1;o<w.length;o++)w[o][0]+=w[o-1][0]+1;return w}return mu.default=new Map(t([[9,"&Tab;"],[0,"&NewLine;"],[22,"&excl;"],[0,"&quot;"],[0,"&num;"],[0,"&dollar;"],[0,"&percnt;"],[0,"&amp;"],[0,"&apos;"],[0,"&lpar;"],[0,"&rpar;"],[0,"&ast;"],[0,"&plus;"],[0,"&comma;"],[1,"&period;"],[0,"&sol;"],[10,"&colon;"],[0,"&semi;"],[0,{v:"&lt;",n:8402,o:"&nvlt;"}],[0,{v:"&equals;",n:8421,o:"&bne;"}],[0,{v:"&gt;",n:8402,o:"&nvgt;"}],[0,"&quest;"],[0,"&commat;"],[26,"&lbrack;"],[0,"&bsol;"],[0,"&rbrack;"],[0,"&Hat;"],[0,"&lowbar;"],[0,"&DiacriticalGrave;"],[5,{n:106,o:"&fjlig;"}],[20,"&lbrace;"],[0,"&verbar;"],[0,"&rbrace;"],[34,"&nbsp;"],[0,"&iexcl;"],[0,"&cent;"],[0,"&pound;"],[0,"&curren;"],[0,"&yen;"],[0,"&brvbar;"],[0,"&sect;"],[0,"&die;"],[0,"&copy;"],[0,"&ordf;"],[0,"&laquo;"],[0,"&not;"],[0,"&shy;"],[0,"&circledR;"],[0,"&macr;"],[0,"&deg;"],[0,"&PlusMinus;"],[0,"&sup2;"],[0,"&sup3;"],[0,"&acute;"],[0,"&micro;"],[0,"&para;"],[0,"&centerdot;"],[0,"&cedil;"],[0,"&sup1;"],[0,"&ordm;"],[0,"&raquo;"],[0,"&frac14;"],[0,"&frac12;"],[0,"&frac34;"],[0,"&iquest;"],[0,"&Agrave;"],[0,"&Aacute;"],[0,"&Acirc;"],[0,"&Atilde;"],[0,"&Auml;"],[0,"&angst;"],[0,"&AElig;"],[0,"&Ccedil;"],[0,"&Egrave;"],[0,"&Eacute;"],[0,"&Ecirc;"],[0,"&Euml;"],[0,"&Igrave;"],[0,"&Iacute;"],[0,"&Icirc;"],[0,"&Iuml;"],[0,"&ETH;"],[0,"&Ntilde;"],[0,"&Ograve;"],[0,"&Oacute;"],[0,"&Ocirc;"],[0,"&Otilde;"],[0,"&Ouml;"],[0,"&times;"],[0,"&Oslash;"],[0,"&Ugrave;"],[0,"&Uacute;"],[0,"&Ucirc;"],[0,"&Uuml;"],[0,"&Yacute;"],[0,"&THORN;"],[0,"&szlig;"],[0,"&agrave;"],[0,"&aacute;"],[0,"&acirc;"],[0,"&atilde;"],[0,"&auml;"],[0,"&aring;"],[0,"&aelig;"],[0,"&ccedil;"],[0,"&egrave;"],[0,"&eacute;"],[0,"&ecirc;"],[0,"&euml;"],[0,"&igrave;"],[0,"&iacute;"],[0,"&icirc;"],[0,"&iuml;"],[0,"&eth;"],[0,"&ntilde;"],[0,"&ograve;"],[0,"&oacute;"],[0,"&ocirc;"],[0,"&otilde;"],[0,"&ouml;"],[0,"&div;"],[0,"&oslash;"],[0,"&ugrave;"],[0,"&uacute;"],[0,"&ucirc;"],[0,"&uuml;"],[0,"&yacute;"],[0,"&thorn;"],[0,"&yuml;"],[0,"&Amacr;"],[0,"&amacr;"],[0,"&Abreve;"],[0,"&abreve;"],[0,"&Aogon;"],[0,"&aogon;"],[0,"&Cacute;"],[0,"&cacute;"],[0,"&Ccirc;"],[0,"&ccirc;"],[0,"&Cdot;"],[0,"&cdot;"],[0,"&Ccaron;"],[0,"&ccaron;"],[0,"&Dcaron;"],[0,"&dcaron;"],[0,"&Dstrok;"],[0,"&dstrok;"],[0,"&Emacr;"],[0,"&emacr;"],[2,"&Edot;"],[0,"&edot;"],[0,"&Eogon;"],[0,"&eogon;"],[0,"&Ecaron;"],[0,"&ecaron;"],[0,"&Gcirc;"],[0,"&gcirc;"],[0,"&Gbreve;"],[0,"&gbreve;"],[0,"&Gdot;"],[0,"&gdot;"],[0,"&Gcedil;"],[1,"&Hcirc;"],[0,"&hcirc;"],[0,"&Hstrok;"],[0,"&hstrok;"],[0,"&Itilde;"],[0,"&itilde;"],[0,"&Imacr;"],[0,"&imacr;"],[2,"&Iogon;"],[0,"&iogon;"],[0,"&Idot;"],[0,"&imath;"],[0,"&IJlig;"],[0,"&ijlig;"],[0,"&Jcirc;"],[0,"&jcirc;"],[0,"&Kcedil;"],[0,"&kcedil;"],[0,"&kgreen;"],[0,"&Lacute;"],[0,"&lacute;"],[0,"&Lcedil;"],[0,"&lcedil;"],[0,"&Lcaron;"],[0,"&lcaron;"],[0,"&Lmidot;"],[0,"&lmidot;"],[0,"&Lstrok;"],[0,"&lstrok;"],[0,"&Nacute;"],[0,"&nacute;"],[0,"&Ncedil;"],[0,"&ncedil;"],[0,"&Ncaron;"],[0,"&ncaron;"],[0,"&napos;"],[0,"&ENG;"],[0,"&eng;"],[0,"&Omacr;"],[0,"&omacr;"],[2,"&Odblac;"],[0,"&odblac;"],[0,"&OElig;"],[0,"&oelig;"],[0,"&Racute;"],[0,"&racute;"],[0,"&Rcedil;"],[0,"&rcedil;"],[0,"&Rcaron;"],[0,"&rcaron;"],[0,"&Sacute;"],[0,"&sacute;"],[0,"&Scirc;"],[0,"&scirc;"],[0,"&Scedil;"],[0,"&scedil;"],[0,"&Scaron;"],[0,"&scaron;"],[0,"&Tcedil;"],[0,"&tcedil;"],[0,"&Tcaron;"],[0,"&tcaron;"],[0,"&Tstrok;"],[0,"&tstrok;"],[0,"&Utilde;"],[0,"&utilde;"],[0,"&Umacr;"],[0,"&umacr;"],[0,"&Ubreve;"],[0,"&ubreve;"],[0,"&Uring;"],[0,"&uring;"],[0,"&Udblac;"],[0,"&udblac;"],[0,"&Uogon;"],[0,"&uogon;"],[0,"&Wcirc;"],[0,"&wcirc;"],[0,"&Ycirc;"],[0,"&ycirc;"],[0,"&Yuml;"],[0,"&Zacute;"],[0,"&zacute;"],[0,"&Zdot;"],[0,"&zdot;"],[0,"&Zcaron;"],[0,"&zcaron;"],[19,"&fnof;"],[34,"&imped;"],[63,"&gacute;"],[65,"&jmath;"],[142,"&circ;"],[0,"&caron;"],[16,"&breve;"],[0,"&DiacriticalDot;"],[0,"&ring;"],[0,"&ogon;"],[0,"&DiacriticalTilde;"],[0,"&dblac;"],[51,"&DownBreve;"],[127,"&Alpha;"],[0,"&Beta;"],[0,"&Gamma;"],[0,"&Delta;"],[0,"&Epsilon;"],[0,"&Zeta;"],[0,"&Eta;"],[0,"&Theta;"],[0,"&Iota;"],[0,"&Kappa;"],[0,"&Lambda;"],[0,"&Mu;"],[0,"&Nu;"],[0,"&Xi;"],[0,"&Omicron;"],[0,"&Pi;"],[0,"&Rho;"],[1,"&Sigma;"],[0,"&Tau;"],[0,"&Upsilon;"],[0,"&Phi;"],[0,"&Chi;"],[0,"&Psi;"],[0,"&ohm;"],[7,"&alpha;"],[0,"&beta;"],[0,"&gamma;"],[0,"&delta;"],[0,"&epsi;"],[0,"&zeta;"],[0,"&eta;"],[0,"&theta;"],[0,"&iota;"],[0,"&kappa;"],[0,"&lambda;"],[0,"&mu;"],[0,"&nu;"],[0,"&xi;"],[0,"&omicron;"],[0,"&pi;"],[0,"&rho;"],[0,"&sigmaf;"],[0,"&sigma;"],[0,"&tau;"],[0,"&upsi;"],[0,"&phi;"],[0,"&chi;"],[0,"&psi;"],[0,"&omega;"],[7,"&thetasym;"],[0,"&Upsi;"],[2,"&phiv;"],[0,"&piv;"],[5,"&Gammad;"],[0,"&digamma;"],[18,"&kappav;"],[0,"&rhov;"],[3,"&epsiv;"],[0,"&backepsilon;"],[10,"&IOcy;"],[0,"&DJcy;"],[0,"&GJcy;"],[0,"&Jukcy;"],[0,"&DScy;"],[0,"&Iukcy;"],[0,"&YIcy;"],[0,"&Jsercy;"],[0,"&LJcy;"],[0,"&NJcy;"],[0,"&TSHcy;"],[0,"&KJcy;"],[1,"&Ubrcy;"],[0,"&DZcy;"],[0,"&Acy;"],[0,"&Bcy;"],[0,"&Vcy;"],[0,"&Gcy;"],[0,"&Dcy;"],[0,"&IEcy;"],[0,"&ZHcy;"],[0,"&Zcy;"],[0,"&Icy;"],[0,"&Jcy;"],[0,"&Kcy;"],[0,"&Lcy;"],[0,"&Mcy;"],[0,"&Ncy;"],[0,"&Ocy;"],[0,"&Pcy;"],[0,"&Rcy;"],[0,"&Scy;"],[0,"&Tcy;"],[0,"&Ucy;"],[0,"&Fcy;"],[0,"&KHcy;"],[0,"&TScy;"],[0,"&CHcy;"],[0,"&SHcy;"],[0,"&SHCHcy;"],[0,"&HARDcy;"],[0,"&Ycy;"],[0,"&SOFTcy;"],[0,"&Ecy;"],[0,"&YUcy;"],[0,"&YAcy;"],[0,"&acy;"],[0,"&bcy;"],[0,"&vcy;"],[0,"&gcy;"],[0,"&dcy;"],[0,"&iecy;"],[0,"&zhcy;"],[0,"&zcy;"],[0,"&icy;"],[0,"&jcy;"],[0,"&kcy;"],[0,"&lcy;"],[0,"&mcy;"],[0,"&ncy;"],[0,"&ocy;"],[0,"&pcy;"],[0,"&rcy;"],[0,"&scy;"],[0,"&tcy;"],[0,"&ucy;"],[0,"&fcy;"],[0,"&khcy;"],[0,"&tscy;"],[0,"&chcy;"],[0,"&shcy;"],[0,"&shchcy;"],[0,"&hardcy;"],[0,"&ycy;"],[0,"&softcy;"],[0,"&ecy;"],[0,"&yucy;"],[0,"&yacy;"],[1,"&iocy;"],[0,"&djcy;"],[0,"&gjcy;"],[0,"&jukcy;"],[0,"&dscy;"],[0,"&iukcy;"],[0,"&yicy;"],[0,"&jsercy;"],[0,"&ljcy;"],[0,"&njcy;"],[0,"&tshcy;"],[0,"&kjcy;"],[1,"&ubrcy;"],[0,"&dzcy;"],[7074,"&ensp;"],[0,"&emsp;"],[0,"&emsp13;"],[0,"&emsp14;"],[1,"&numsp;"],[0,"&puncsp;"],[0,"&ThinSpace;"],[0,"&hairsp;"],[0,"&NegativeMediumSpace;"],[0,"&zwnj;"],[0,"&zwj;"],[0,"&lrm;"],[0,"&rlm;"],[0,"&dash;"],[2,"&ndash;"],[0,"&mdash;"],[0,"&horbar;"],[0,"&Verbar;"],[1,"&lsquo;"],[0,"&CloseCurlyQuote;"],[0,"&lsquor;"],[1,"&ldquo;"],[0,"&CloseCurlyDoubleQuote;"],[0,"&bdquo;"],[1,"&dagger;"],[0,"&Dagger;"],[0,"&bull;"],[2,"&nldr;"],[0,"&hellip;"],[9,"&permil;"],[0,"&pertenk;"],[0,"&prime;"],[0,"&Prime;"],[0,"&tprime;"],[0,"&backprime;"],[3,"&lsaquo;"],[0,"&rsaquo;"],[3,"&oline;"],[2,"&caret;"],[1,"&hybull;"],[0,"&frasl;"],[10,"&bsemi;"],[7,"&qprime;"],[7,{v:"&MediumSpace;",n:8202,o:"&ThickSpace;"}],[0,"&NoBreak;"],[0,"&af;"],[0,"&InvisibleTimes;"],[0,"&ic;"],[72,"&euro;"],[46,"&tdot;"],[0,"&DotDot;"],[37,"&complexes;"],[2,"&incare;"],[4,"&gscr;"],[0,"&hamilt;"],[0,"&Hfr;"],[0,"&Hopf;"],[0,"&planckh;"],[0,"&hbar;"],[0,"&imagline;"],[0,"&Ifr;"],[0,"&lagran;"],[0,"&ell;"],[1,"&naturals;"],[0,"&numero;"],[0,"&copysr;"],[0,"&weierp;"],[0,"&Popf;"],[0,"&Qopf;"],[0,"&realine;"],[0,"&real;"],[0,"&reals;"],[0,"&rx;"],[3,"&trade;"],[1,"&integers;"],[2,"&mho;"],[0,"&zeetrf;"],[0,"&iiota;"],[2,"&bernou;"],[0,"&Cayleys;"],[1,"&escr;"],[0,"&Escr;"],[0,"&Fouriertrf;"],[1,"&Mellintrf;"],[0,"&order;"],[0,"&alefsym;"],[0,"&beth;"],[0,"&gimel;"],[0,"&daleth;"],[12,"&CapitalDifferentialD;"],[0,"&dd;"],[0,"&ee;"],[0,"&ii;"],[10,"&frac13;"],[0,"&frac23;"],[0,"&frac15;"],[0,"&frac25;"],[0,"&frac35;"],[0,"&frac45;"],[0,"&frac16;"],[0,"&frac56;"],[0,"&frac18;"],[0,"&frac38;"],[0,"&frac58;"],[0,"&frac78;"],[49,"&larr;"],[0,"&ShortUpArrow;"],[0,"&rarr;"],[0,"&darr;"],[0,"&harr;"],[0,"&updownarrow;"],[0,"&nwarr;"],[0,"&nearr;"],[0,"&LowerRightArrow;"],[0,"&LowerLeftArrow;"],[0,"&nlarr;"],[0,"&nrarr;"],[1,{v:"&rarrw;",n:824,o:"&nrarrw;"}],[0,"&Larr;"],[0,"&Uarr;"],[0,"&Rarr;"],[0,"&Darr;"],[0,"&larrtl;"],[0,"&rarrtl;"],[0,"&LeftTeeArrow;"],[0,"&mapstoup;"],[0,"&map;"],[0,"&DownTeeArrow;"],[1,"&hookleftarrow;"],[0,"&hookrightarrow;"],[0,"&larrlp;"],[0,"&looparrowright;"],[0,"&harrw;"],[0,"&nharr;"],[1,"&lsh;"],[0,"&rsh;"],[0,"&ldsh;"],[0,"&rdsh;"],[1,"&crarr;"],[0,"&cularr;"],[0,"&curarr;"],[2,"&circlearrowleft;"],[0,"&circlearrowright;"],[0,"&leftharpoonup;"],[0,"&DownLeftVector;"],[0,"&RightUpVector;"],[0,"&LeftUpVector;"],[0,"&rharu;"],[0,"&DownRightVector;"],[0,"&dharr;"],[0,"&dharl;"],[0,"&RightArrowLeftArrow;"],[0,"&udarr;"],[0,"&LeftArrowRightArrow;"],[0,"&leftleftarrows;"],[0,"&upuparrows;"],[0,"&rightrightarrows;"],[0,"&ddarr;"],[0,"&leftrightharpoons;"],[0,"&Equilibrium;"],[0,"&nlArr;"],[0,"&nhArr;"],[0,"&nrArr;"],[0,"&DoubleLeftArrow;"],[0,"&DoubleUpArrow;"],[0,"&DoubleRightArrow;"],[0,"&dArr;"],[0,"&DoubleLeftRightArrow;"],[0,"&DoubleUpDownArrow;"],[0,"&nwArr;"],[0,"&neArr;"],[0,"&seArr;"],[0,"&swArr;"],[0,"&lAarr;"],[0,"&rAarr;"],[1,"&zigrarr;"],[6,"&larrb;"],[0,"&rarrb;"],[15,"&DownArrowUpArrow;"],[7,"&loarr;"],[0,"&roarr;"],[0,"&hoarr;"],[0,"&forall;"],[0,"&comp;"],[0,{v:"&part;",n:824,o:"&npart;"}],[0,"&exist;"],[0,"&nexist;"],[0,"&empty;"],[1,"&Del;"],[0,"&Element;"],[0,"&NotElement;"],[1,"&ni;"],[0,"&notni;"],[2,"&prod;"],[0,"&coprod;"],[0,"&sum;"],[0,"&minus;"],[0,"&MinusPlus;"],[0,"&dotplus;"],[1,"&Backslash;"],[0,"&lowast;"],[0,"&compfn;"],[1,"&radic;"],[2,"&prop;"],[0,"&infin;"],[0,"&angrt;"],[0,{v:"&ang;",n:8402,o:"&nang;"}],[0,"&angmsd;"],[0,"&angsph;"],[0,"&mid;"],[0,"&nmid;"],[0,"&DoubleVerticalBar;"],[0,"&NotDoubleVerticalBar;"],[0,"&and;"],[0,"&or;"],[0,{v:"&cap;",n:65024,o:"&caps;"}],[0,{v:"&cup;",n:65024,o:"&cups;"}],[0,"&int;"],[0,"&Int;"],[0,"&iiint;"],[0,"&conint;"],[0,"&Conint;"],[0,"&Cconint;"],[0,"&cwint;"],[0,"&ClockwiseContourIntegral;"],[0,"&awconint;"],[0,"&there4;"],[0,"&becaus;"],[0,"&ratio;"],[0,"&Colon;"],[0,"&dotminus;"],[1,"&mDDot;"],[0,"&homtht;"],[0,{v:"&sim;",n:8402,o:"&nvsim;"}],[0,{v:"&backsim;",n:817,o:"&race;"}],[0,{v:"&ac;",n:819,o:"&acE;"}],[0,"&acd;"],[0,"&VerticalTilde;"],[0,"&NotTilde;"],[0,{v:"&eqsim;",n:824,o:"&nesim;"}],[0,"&sime;"],[0,"&NotTildeEqual;"],[0,"&cong;"],[0,"&simne;"],[0,"&ncong;"],[0,"&ap;"],[0,"&nap;"],[0,"&ape;"],[0,{v:"&apid;",n:824,o:"&napid;"}],[0,"&backcong;"],[0,{v:"&asympeq;",n:8402,o:"&nvap;"}],[0,{v:"&bump;",n:824,o:"&nbump;"}],[0,{v:"&bumpe;",n:824,o:"&nbumpe;"}],[0,{v:"&doteq;",n:824,o:"&nedot;"}],[0,"&doteqdot;"],[0,"&efDot;"],[0,"&erDot;"],[0,"&Assign;"],[0,"&ecolon;"],[0,"&ecir;"],[0,"&circeq;"],[1,"&wedgeq;"],[0,"&veeeq;"],[1,"&triangleq;"],[2,"&equest;"],[0,"&ne;"],[0,{v:"&Congruent;",n:8421,o:"&bnequiv;"}],[0,"&nequiv;"],[1,{v:"&le;",n:8402,o:"&nvle;"}],[0,{v:"&ge;",n:8402,o:"&nvge;"}],[0,{v:"&lE;",n:824,o:"&nlE;"}],[0,{v:"&gE;",n:824,o:"&ngE;"}],[0,{v:"&lnE;",n:65024,o:"&lvertneqq;"}],[0,{v:"&gnE;",n:65024,o:"&gvertneqq;"}],[0,{v:"&ll;",n:new Map(t([[824,"&nLtv;"],[7577,"&nLt;"]]))}],[0,{v:"&gg;",n:new Map(t([[824,"&nGtv;"],[7577,"&nGt;"]]))}],[0,"&between;"],[0,"&NotCupCap;"],[0,"&nless;"],[0,"&ngt;"],[0,"&nle;"],[0,"&nge;"],[0,"&lesssim;"],[0,"&GreaterTilde;"],[0,"&nlsim;"],[0,"&ngsim;"],[0,"&LessGreater;"],[0,"&gl;"],[0,"&NotLessGreater;"],[0,"&NotGreaterLess;"],[0,"&pr;"],[0,"&sc;"],[0,"&prcue;"],[0,"&sccue;"],[0,"&PrecedesTilde;"],[0,{v:"&scsim;",n:824,o:"&NotSucceedsTilde;"}],[0,"&NotPrecedes;"],[0,"&NotSucceeds;"],[0,{v:"&sub;",n:8402,o:"&NotSubset;"}],[0,{v:"&sup;",n:8402,o:"&NotSuperset;"}],[0,"&nsub;"],[0,"&nsup;"],[0,"&sube;"],[0,"&supe;"],[0,"&NotSubsetEqual;"],[0,"&NotSupersetEqual;"],[0,{v:"&subne;",n:65024,o:"&varsubsetneq;"}],[0,{v:"&supne;",n:65024,o:"&varsupsetneq;"}],[1,"&cupdot;"],[0,"&UnionPlus;"],[0,{v:"&sqsub;",n:824,o:"&NotSquareSubset;"}],[0,{v:"&sqsup;",n:824,o:"&NotSquareSuperset;"}],[0,"&sqsube;"],[0,"&sqsupe;"],[0,{v:"&sqcap;",n:65024,o:"&sqcaps;"}],[0,{v:"&sqcup;",n:65024,o:"&sqcups;"}],[0,"&CirclePlus;"],[0,"&CircleMinus;"],[0,"&CircleTimes;"],[0,"&osol;"],[0,"&CircleDot;"],[0,"&circledcirc;"],[0,"&circledast;"],[1,"&circleddash;"],[0,"&boxplus;"],[0,"&boxminus;"],[0,"&boxtimes;"],[0,"&dotsquare;"],[0,"&RightTee;"],[0,"&dashv;"],[0,"&DownTee;"],[0,"&bot;"],[1,"&models;"],[0,"&DoubleRightTee;"],[0,"&Vdash;"],[0,"&Vvdash;"],[0,"&VDash;"],[0,"&nvdash;"],[0,"&nvDash;"],[0,"&nVdash;"],[0,"&nVDash;"],[0,"&prurel;"],[1,"&LeftTriangle;"],[0,"&RightTriangle;"],[0,{v:"&LeftTriangleEqual;",n:8402,o:"&nvltrie;"}],[0,{v:"&RightTriangleEqual;",n:8402,o:"&nvrtrie;"}],[0,"&origof;"],[0,"&imof;"],[0,"&multimap;"],[0,"&hercon;"],[0,"&intcal;"],[0,"&veebar;"],[1,"&barvee;"],[0,"&angrtvb;"],[0,"&lrtri;"],[0,"&bigwedge;"],[0,"&bigvee;"],[0,"&bigcap;"],[0,"&bigcup;"],[0,"&diam;"],[0,"&sdot;"],[0,"&sstarf;"],[0,"&divideontimes;"],[0,"&bowtie;"],[0,"&ltimes;"],[0,"&rtimes;"],[0,"&leftthreetimes;"],[0,"&rightthreetimes;"],[0,"&backsimeq;"],[0,"&curlyvee;"],[0,"&curlywedge;"],[0,"&Sub;"],[0,"&Sup;"],[0,"&Cap;"],[0,"&Cup;"],[0,"&fork;"],[0,"&epar;"],[0,"&lessdot;"],[0,"&gtdot;"],[0,{v:"&Ll;",n:824,o:"&nLl;"}],[0,{v:"&Gg;",n:824,o:"&nGg;"}],[0,{v:"&leg;",n:65024,o:"&lesg;"}],[0,{v:"&gel;",n:65024,o:"&gesl;"}],[2,"&cuepr;"],[0,"&cuesc;"],[0,"&NotPrecedesSlantEqual;"],[0,"&NotSucceedsSlantEqual;"],[0,"&NotSquareSubsetEqual;"],[0,"&NotSquareSupersetEqual;"],[2,"&lnsim;"],[0,"&gnsim;"],[0,"&precnsim;"],[0,"&scnsim;"],[0,"&nltri;"],[0,"&NotRightTriangle;"],[0,"&nltrie;"],[0,"&NotRightTriangleEqual;"],[0,"&vellip;"],[0,"&ctdot;"],[0,"&utdot;"],[0,"&dtdot;"],[0,"&disin;"],[0,"&isinsv;"],[0,"&isins;"],[0,{v:"&isindot;",n:824,o:"&notindot;"}],[0,"&notinvc;"],[0,"&notinvb;"],[1,{v:"&isinE;",n:824,o:"&notinE;"}],[0,"&nisd;"],[0,"&xnis;"],[0,"&nis;"],[0,"&notnivc;"],[0,"&notnivb;"],[6,"&barwed;"],[0,"&Barwed;"],[1,"&lceil;"],[0,"&rceil;"],[0,"&LeftFloor;"],[0,"&rfloor;"],[0,"&drcrop;"],[0,"&dlcrop;"],[0,"&urcrop;"],[0,"&ulcrop;"],[0,"&bnot;"],[1,"&profline;"],[0,"&profsurf;"],[1,"&telrec;"],[0,"&target;"],[5,"&ulcorn;"],[0,"&urcorn;"],[0,"&dlcorn;"],[0,"&drcorn;"],[2,"&frown;"],[0,"&smile;"],[9,"&cylcty;"],[0,"&profalar;"],[7,"&topbot;"],[6,"&ovbar;"],[1,"&solbar;"],[60,"&angzarr;"],[51,"&lmoustache;"],[0,"&rmoustache;"],[2,"&OverBracket;"],[0,"&bbrk;"],[0,"&bbrktbrk;"],[37,"&OverParenthesis;"],[0,"&UnderParenthesis;"],[0,"&OverBrace;"],[0,"&UnderBrace;"],[2,"&trpezium;"],[4,"&elinters;"],[59,"&blank;"],[164,"&circledS;"],[55,"&boxh;"],[1,"&boxv;"],[9,"&boxdr;"],[3,"&boxdl;"],[3,"&boxur;"],[3,"&boxul;"],[3,"&boxvr;"],[7,"&boxvl;"],[7,"&boxhd;"],[7,"&boxhu;"],[7,"&boxvh;"],[19,"&boxH;"],[0,"&boxV;"],[0,"&boxdR;"],[0,"&boxDr;"],[0,"&boxDR;"],[0,"&boxdL;"],[0,"&boxDl;"],[0,"&boxDL;"],[0,"&boxuR;"],[0,"&boxUr;"],[0,"&boxUR;"],[0,"&boxuL;"],[0,"&boxUl;"],[0,"&boxUL;"],[0,"&boxvR;"],[0,"&boxVr;"],[0,"&boxVR;"],[0,"&boxvL;"],[0,"&boxVl;"],[0,"&boxVL;"],[0,"&boxHd;"],[0,"&boxhD;"],[0,"&boxHD;"],[0,"&boxHu;"],[0,"&boxhU;"],[0,"&boxHU;"],[0,"&boxvH;"],[0,"&boxVh;"],[0,"&boxVH;"],[19,"&uhblk;"],[3,"&lhblk;"],[3,"&block;"],[8,"&blk14;"],[0,"&blk12;"],[0,"&blk34;"],[13,"&square;"],[8,"&blacksquare;"],[0,"&EmptyVerySmallSquare;"],[1,"&rect;"],[0,"&marker;"],[2,"&fltns;"],[1,"&bigtriangleup;"],[0,"&blacktriangle;"],[0,"&triangle;"],[2,"&blacktriangleright;"],[0,"&rtri;"],[3,"&bigtriangledown;"],[0,"&blacktriangledown;"],[0,"&dtri;"],[2,"&blacktriangleleft;"],[0,"&ltri;"],[6,"&loz;"],[0,"&cir;"],[32,"&tridot;"],[2,"&bigcirc;"],[8,"&ultri;"],[0,"&urtri;"],[0,"&lltri;"],[0,"&EmptySmallSquare;"],[0,"&FilledSmallSquare;"],[8,"&bigstar;"],[0,"&star;"],[7,"&phone;"],[49,"&female;"],[1,"&male;"],[29,"&spades;"],[2,"&clubs;"],[1,"&hearts;"],[0,"&diamondsuit;"],[3,"&sung;"],[2,"&flat;"],[0,"&natural;"],[0,"&sharp;"],[163,"&check;"],[3,"&cross;"],[8,"&malt;"],[21,"&sext;"],[33,"&VerticalSeparator;"],[25,"&lbbrk;"],[0,"&rbbrk;"],[84,"&bsolhsub;"],[0,"&suphsol;"],[28,"&LeftDoubleBracket;"],[0,"&RightDoubleBracket;"],[0,"&lang;"],[0,"&rang;"],[0,"&Lang;"],[0,"&Rang;"],[0,"&loang;"],[0,"&roang;"],[7,"&longleftarrow;"],[0,"&longrightarrow;"],[0,"&longleftrightarrow;"],[0,"&DoubleLongLeftArrow;"],[0,"&DoubleLongRightArrow;"],[0,"&DoubleLongLeftRightArrow;"],[1,"&longmapsto;"],[2,"&dzigrarr;"],[258,"&nvlArr;"],[0,"&nvrArr;"],[0,"&nvHarr;"],[0,"&Map;"],[6,"&lbarr;"],[0,"&bkarow;"],[0,"&lBarr;"],[0,"&dbkarow;"],[0,"&drbkarow;"],[0,"&DDotrahd;"],[0,"&UpArrowBar;"],[0,"&DownArrowBar;"],[2,"&Rarrtl;"],[2,"&latail;"],[0,"&ratail;"],[0,"&lAtail;"],[0,"&rAtail;"],[0,"&larrfs;"],[0,"&rarrfs;"],[0,"&larrbfs;"],[0,"&rarrbfs;"],[2,"&nwarhk;"],[0,"&nearhk;"],[0,"&hksearow;"],[0,"&hkswarow;"],[0,"&nwnear;"],[0,"&nesear;"],[0,"&seswar;"],[0,"&swnwar;"],[8,{v:"&rarrc;",n:824,o:"&nrarrc;"}],[1,"&cudarrr;"],[0,"&ldca;"],[0,"&rdca;"],[0,"&cudarrl;"],[0,"&larrpl;"],[2,"&curarrm;"],[0,"&cularrp;"],[7,"&rarrpl;"],[2,"&harrcir;"],[0,"&Uarrocir;"],[0,"&lurdshar;"],[0,"&ldrushar;"],[2,"&LeftRightVector;"],[0,"&RightUpDownVector;"],[0,"&DownLeftRightVector;"],[0,"&LeftUpDownVector;"],[0,"&LeftVectorBar;"],[0,"&RightVectorBar;"],[0,"&RightUpVectorBar;"],[0,"&RightDownVectorBar;"],[0,"&DownLeftVectorBar;"],[0,"&DownRightVectorBar;"],[0,"&LeftUpVectorBar;"],[0,"&LeftDownVectorBar;"],[0,"&LeftTeeVector;"],[0,"&RightTeeVector;"],[0,"&RightUpTeeVector;"],[0,"&RightDownTeeVector;"],[0,"&DownLeftTeeVector;"],[0,"&DownRightTeeVector;"],[0,"&LeftUpTeeVector;"],[0,"&LeftDownTeeVector;"],[0,"&lHar;"],[0,"&uHar;"],[0,"&rHar;"],[0,"&dHar;"],[0,"&luruhar;"],[0,"&ldrdhar;"],[0,"&ruluhar;"],[0,"&rdldhar;"],[0,"&lharul;"],[0,"&llhard;"],[0,"&rharul;"],[0,"&lrhard;"],[0,"&udhar;"],[0,"&duhar;"],[0,"&RoundImplies;"],[0,"&erarr;"],[0,"&simrarr;"],[0,"&larrsim;"],[0,"&rarrsim;"],[0,"&rarrap;"],[0,"&ltlarr;"],[1,"&gtrarr;"],[0,"&subrarr;"],[1,"&suplarr;"],[0,"&lfisht;"],[0,"&rfisht;"],[0,"&ufisht;"],[0,"&dfisht;"],[5,"&lopar;"],[0,"&ropar;"],[4,"&lbrke;"],[0,"&rbrke;"],[0,"&lbrkslu;"],[0,"&rbrksld;"],[0,"&lbrksld;"],[0,"&rbrkslu;"],[0,"&langd;"],[0,"&rangd;"],[0,"&lparlt;"],[0,"&rpargt;"],[0,"&gtlPar;"],[0,"&ltrPar;"],[3,"&vzigzag;"],[1,"&vangrt;"],[0,"&angrtvbd;"],[6,"&ange;"],[0,"&range;"],[0,"&dwangle;"],[0,"&uwangle;"],[0,"&angmsdaa;"],[0,"&angmsdab;"],[0,"&angmsdac;"],[0,"&angmsdad;"],[0,"&angmsdae;"],[0,"&angmsdaf;"],[0,"&angmsdag;"],[0,"&angmsdah;"],[0,"&bemptyv;"],[0,"&demptyv;"],[0,"&cemptyv;"],[0,"&raemptyv;"],[0,"&laemptyv;"],[0,"&ohbar;"],[0,"&omid;"],[0,"&opar;"],[1,"&operp;"],[1,"&olcross;"],[0,"&odsold;"],[1,"&olcir;"],[0,"&ofcir;"],[0,"&olt;"],[0,"&ogt;"],[0,"&cirscir;"],[0,"&cirE;"],[0,"&solb;"],[0,"&bsolb;"],[3,"&boxbox;"],[3,"&trisb;"],[0,"&rtriltri;"],[0,{v:"&LeftTriangleBar;",n:824,o:"&NotLeftTriangleBar;"}],[0,{v:"&RightTriangleBar;",n:824,o:"&NotRightTriangleBar;"}],[11,"&iinfin;"],[0,"&infintie;"],[0,"&nvinfin;"],[4,"&eparsl;"],[0,"&smeparsl;"],[0,"&eqvparsl;"],[5,"&blacklozenge;"],[8,"&RuleDelayed;"],[1,"&dsol;"],[9,"&bigodot;"],[0,"&bigoplus;"],[0,"&bigotimes;"],[1,"&biguplus;"],[1,"&bigsqcup;"],[5,"&iiiint;"],[0,"&fpartint;"],[2,"&cirfnint;"],[0,"&awint;"],[0,"&rppolint;"],[0,"&scpolint;"],[0,"&npolint;"],[0,"&pointint;"],[0,"&quatint;"],[0,"&intlarhk;"],[10,"&pluscir;"],[0,"&plusacir;"],[0,"&simplus;"],[0,"&plusdu;"],[0,"&plussim;"],[0,"&plustwo;"],[1,"&mcomma;"],[0,"&minusdu;"],[2,"&loplus;"],[0,"&roplus;"],[0,"&Cross;"],[0,"&timesd;"],[0,"&timesbar;"],[1,"&smashp;"],[0,"&lotimes;"],[0,"&rotimes;"],[0,"&otimesas;"],[0,"&Otimes;"],[0,"&odiv;"],[0,"&triplus;"],[0,"&triminus;"],[0,"&tritime;"],[0,"&intprod;"],[2,"&amalg;"],[0,"&capdot;"],[1,"&ncup;"],[0,"&ncap;"],[0,"&capand;"],[0,"&cupor;"],[0,"&cupcap;"],[0,"&capcup;"],[0,"&cupbrcap;"],[0,"&capbrcup;"],[0,"&cupcup;"],[0,"&capcap;"],[0,"&ccups;"],[0,"&ccaps;"],[2,"&ccupssm;"],[2,"&And;"],[0,"&Or;"],[0,"&andand;"],[0,"&oror;"],[0,"&orslope;"],[0,"&andslope;"],[1,"&andv;"],[0,"&orv;"],[0,"&andd;"],[0,"&ord;"],[1,"&wedbar;"],[6,"&sdote;"],[3,"&simdot;"],[2,{v:"&congdot;",n:824,o:"&ncongdot;"}],[0,"&easter;"],[0,"&apacir;"],[0,{v:"&apE;",n:824,o:"&napE;"}],[0,"&eplus;"],[0,"&pluse;"],[0,"&Esim;"],[0,"&Colone;"],[0,"&Equal;"],[1,"&ddotseq;"],[0,"&equivDD;"],[0,"&ltcir;"],[0,"&gtcir;"],[0,"&ltquest;"],[0,"&gtquest;"],[0,{v:"&leqslant;",n:824,o:"&nleqslant;"}],[0,{v:"&geqslant;",n:824,o:"&ngeqslant;"}],[0,"&lesdot;"],[0,"&gesdot;"],[0,"&lesdoto;"],[0,"&gesdoto;"],[0,"&lesdotor;"],[0,"&gesdotol;"],[0,"&lap;"],[0,"&gap;"],[0,"&lne;"],[0,"&gne;"],[0,"&lnap;"],[0,"&gnap;"],[0,"&lEg;"],[0,"&gEl;"],[0,"&lsime;"],[0,"&gsime;"],[0,"&lsimg;"],[0,"&gsiml;"],[0,"&lgE;"],[0,"&glE;"],[0,"&lesges;"],[0,"&gesles;"],[0,"&els;"],[0,"&egs;"],[0,"&elsdot;"],[0,"&egsdot;"],[0,"&el;"],[0,"&eg;"],[2,"&siml;"],[0,"&simg;"],[0,"&simlE;"],[0,"&simgE;"],[0,{v:"&LessLess;",n:824,o:"&NotNestedLessLess;"}],[0,{v:"&GreaterGreater;",n:824,o:"&NotNestedGreaterGreater;"}],[1,"&glj;"],[0,"&gla;"],[0,"&ltcc;"],[0,"&gtcc;"],[0,"&lescc;"],[0,"&gescc;"],[0,"&smt;"],[0,"&lat;"],[0,{v:"&smte;",n:65024,o:"&smtes;"}],[0,{v:"&late;",n:65024,o:"&lates;"}],[0,"&bumpE;"],[0,{v:"&PrecedesEqual;",n:824,o:"&NotPrecedesEqual;"}],[0,{v:"&sce;",n:824,o:"&NotSucceedsEqual;"}],[2,"&prE;"],[0,"&scE;"],[0,"&precneqq;"],[0,"&scnE;"],[0,"&prap;"],[0,"&scap;"],[0,"&precnapprox;"],[0,"&scnap;"],[0,"&Pr;"],[0,"&Sc;"],[0,"&subdot;"],[0,"&supdot;"],[0,"&subplus;"],[0,"&supplus;"],[0,"&submult;"],[0,"&supmult;"],[0,"&subedot;"],[0,"&supedot;"],[0,{v:"&subE;",n:824,o:"&nsubE;"}],[0,{v:"&supE;",n:824,o:"&nsupE;"}],[0,"&subsim;"],[0,"&supsim;"],[2,{v:"&subnE;",n:65024,o:"&varsubsetneqq;"}],[0,{v:"&supnE;",n:65024,o:"&varsupsetneqq;"}],[2,"&csub;"],[0,"&csup;"],[0,"&csube;"],[0,"&csupe;"],[0,"&subsup;"],[0,"&supsub;"],[0,"&subsub;"],[0,"&supsup;"],[0,"&suphsub;"],[0,"&supdsub;"],[0,"&forkv;"],[0,"&topfork;"],[0,"&mlcp;"],[8,"&Dashv;"],[1,"&Vdashl;"],[0,"&Barv;"],[0,"&vBar;"],[0,"&vBarv;"],[1,"&Vbar;"],[0,"&Not;"],[0,"&bNot;"],[0,"&rnmid;"],[0,"&cirmid;"],[0,"&midcir;"],[0,"&topcir;"],[0,"&nhpar;"],[0,"&parsim;"],[9,{v:"&parsl;",n:8421,o:"&nparsl;"}],[44343,{n:new Map(t([[56476,"&Ascr;"],[1,"&Cscr;"],[0,"&Dscr;"],[2,"&Gscr;"],[2,"&Jscr;"],[0,"&Kscr;"],[2,"&Nscr;"],[0,"&Oscr;"],[0,"&Pscr;"],[0,"&Qscr;"],[1,"&Sscr;"],[0,"&Tscr;"],[0,"&Uscr;"],[0,"&Vscr;"],[0,"&Wscr;"],[0,"&Xscr;"],[0,"&Yscr;"],[0,"&Zscr;"],[0,"&ascr;"],[0,"&bscr;"],[0,"&cscr;"],[0,"&dscr;"],[1,"&fscr;"],[1,"&hscr;"],[0,"&iscr;"],[0,"&jscr;"],[0,"&kscr;"],[0,"&lscr;"],[0,"&mscr;"],[0,"&nscr;"],[1,"&pscr;"],[0,"&qscr;"],[0,"&rscr;"],[0,"&sscr;"],[0,"&tscr;"],[0,"&uscr;"],[0,"&vscr;"],[0,"&wscr;"],[0,"&xscr;"],[0,"&yscr;"],[0,"&zscr;"],[52,"&Afr;"],[0,"&Bfr;"],[1,"&Dfr;"],[0,"&Efr;"],[0,"&Ffr;"],[0,"&Gfr;"],[2,"&Jfr;"],[0,"&Kfr;"],[0,"&Lfr;"],[0,"&Mfr;"],[0,"&Nfr;"],[0,"&Ofr;"],[0,"&Pfr;"],[0,"&Qfr;"],[1,"&Sfr;"],[0,"&Tfr;"],[0,"&Ufr;"],[0,"&Vfr;"],[0,"&Wfr;"],[0,"&Xfr;"],[0,"&Yfr;"],[1,"&afr;"],[0,"&bfr;"],[0,"&cfr;"],[0,"&dfr;"],[0,"&efr;"],[0,"&ffr;"],[0,"&gfr;"],[0,"&hfr;"],[0,"&ifr;"],[0,"&jfr;"],[0,"&kfr;"],[0,"&lfr;"],[0,"&mfr;"],[0,"&nfr;"],[0,"&ofr;"],[0,"&pfr;"],[0,"&qfr;"],[0,"&rfr;"],[0,"&sfr;"],[0,"&tfr;"],[0,"&ufr;"],[0,"&vfr;"],[0,"&wfr;"],[0,"&xfr;"],[0,"&yfr;"],[0,"&zfr;"],[0,"&Aopf;"],[0,"&Bopf;"],[1,"&Dopf;"],[0,"&Eopf;"],[0,"&Fopf;"],[0,"&Gopf;"],[1,"&Iopf;"],[0,"&Jopf;"],[0,"&Kopf;"],[0,"&Lopf;"],[0,"&Mopf;"],[1,"&Oopf;"],[3,"&Sopf;"],[0,"&Topf;"],[0,"&Uopf;"],[0,"&Vopf;"],[0,"&Wopf;"],[0,"&Xopf;"],[0,"&Yopf;"],[1,"&aopf;"],[0,"&bopf;"],[0,"&copf;"],[0,"&dopf;"],[0,"&eopf;"],[0,"&fopf;"],[0,"&gopf;"],[0,"&hopf;"],[0,"&iopf;"],[0,"&jopf;"],[0,"&kopf;"],[0,"&lopf;"],[0,"&mopf;"],[0,"&nopf;"],[0,"&oopf;"],[0,"&popf;"],[0,"&qopf;"],[0,"&ropf;"],[0,"&sopf;"],[0,"&topf;"],[0,"&uopf;"],[0,"&vopf;"],[0,"&wopf;"],[0,"&xopf;"],[0,"&yopf;"],[0,"&zopf;"]]))}],[8906,"&fflig;"],[0,"&filig;"],[0,"&fllig;"],[0,"&ffilig;"],[0,"&ffllig;"]])),mu}var _u={},Yu;function Lu(){return Yu||(Yu=1,(function(t){Object.defineProperty(t,"__esModule",{value:true}),t.escapeText=t.escapeAttribute=t.escapeUTF8=t.escape=t.encodeXML=t.getCodePoint=t.xmlReplacer=void 0,t.xmlReplacer=/["&'<>$\x80-\uFFFF]/g;var w=new Map([[34,"&quot;"],[38,"&amp;"],[39,"&apos;"],[60,"&lt;"],[62,"&gt;"]]);t.getCodePoint=String.prototype.codePointAt!=null?function(A,y){return A.codePointAt(y)}:function(A,y){return (A.charCodeAt(y)&64512)===55296?(A.charCodeAt(y)-55296)*1024+A.charCodeAt(y+1)-56320+65536:A.charCodeAt(y)};function o(A){for(var y="",b=0,f;(f=t.xmlReplacer.exec(A))!==null;){var c=f.index,a=A.charCodeAt(c),v=w.get(a);v!==void 0?(y+=A.substring(b,c)+v,b=c+1):(y+="".concat(A.substring(b,c),"&#x").concat((0, t.getCodePoint)(A,c).toString(16),";"),b=t.xmlReplacer.lastIndex+=+((a&64512)===55296));}return y+A.substr(b)}t.encodeXML=o,t.escape=o;function n(A,y){return function(f){for(var c,a=0,v="";c=A.exec(f);)a!==c.index&&(v+=f.substring(a,c.index)),v+=y.get(c[0].charCodeAt(0)),a=c.index+1;return v+f.substring(a)}}t.escapeUTF8=n(/[&<>'"]/g,w),t.escapeAttribute=n(/["&\u00A0]/g,new Map([[34,"&quot;"],[38,"&amp;"],[160,"&nbsp;"]])),t.escapeText=n(/[&<>\u00A0]/g,new Map([[38,"&amp;"],[60,"&lt;"],[62,"&gt;"],[160,"&nbsp;"]]));})(_u)),_u}var Ku;function $u(){if(Ku)return tu;Ku=1;var t=tu&&tu.__importDefault||function(f){return f&&f.__esModule?f:{default:f}};Object.defineProperty(tu,"__esModule",{value:true}),tu.encodeNonAsciiHTML=tu.encodeHTML=void 0;var w=t(Ie()),o=Lu(),n=/[\t\n!-,./:-@[-`\f{-}$\x80-\uFFFF]/g;function A(f){return b(n,f)}tu.encodeHTML=A;function y(f){return b(o.xmlReplacer,f)}tu.encodeNonAsciiHTML=y;function b(f,c){for(var a="",v=0,T;(T=f.exec(c))!==null;){var u=T.index;a+=c.substring(v,u);var e=c.charCodeAt(u),l=w.default.get(e);if(typeof l=="object"){if(u+1<c.length){var S=c.charCodeAt(u+1),m=typeof l.n=="number"?l.n===S?l.o:void 0:l.n.get(S);if(m!==void 0){a+=m,v=f.lastIndex+=1;continue}}l=l.v;}if(l!==void 0)a+=l,v=u+1;else {var r=(0, o.getCodePoint)(c,u);a+="&#x".concat(r.toString(16),";"),v=f.lastIndex+=+(r!==e);}}return a+c.substr(v)}return tu}var ue;function Le(){return ue||(ue=1,(function(t){Object.defineProperty(t,"__esModule",{value:true}),t.decodeXMLStrict=t.decodeHTML5Strict=t.decodeHTML4Strict=t.decodeHTML5=t.decodeHTML4=t.decodeHTMLAttribute=t.decodeHTMLStrict=t.decodeHTML=t.decodeXML=t.DecodingMode=t.EntityDecoder=t.encodeHTML5=t.encodeHTML4=t.encodeNonAsciiHTML=t.encodeHTML=t.escapeText=t.escapeAttribute=t.escapeUTF8=t.escape=t.encodeXML=t.encode=t.decodeStrict=t.decode=t.EncodingMode=t.EntityLevel=void 0;var w=Tu(),o=$u(),n=Lu(),A;(function(u){u[u.XML=0]="XML",u[u.HTML=1]="HTML";})(A=t.EntityLevel||(t.EntityLevel={}));var y;(function(u){u[u.UTF8=0]="UTF8",u[u.ASCII=1]="ASCII",u[u.Extensive=2]="Extensive",u[u.Attribute=3]="Attribute",u[u.Text=4]="Text";})(y=t.EncodingMode||(t.EncodingMode={}));function b(u,e){e===void 0&&(e=A.XML);var l=typeof e=="number"?e:e.level;if(l===A.HTML){var S=typeof e=="object"?e.mode:void 0;return (0, w.decodeHTML)(u,S)}return (0, w.decodeXML)(u)}t.decode=b;function f(u,e){var l;e===void 0&&(e=A.XML);var S=typeof e=="number"?{level:e}:e;return (l=S.mode)!==null&&l!==void 0||(S.mode=w.DecodingMode.Strict),b(u,S)}t.decodeStrict=f;function c(u,e){e===void 0&&(e=A.XML);var l=typeof e=="number"?{level:e}:e;return l.mode===y.UTF8?(0, n.escapeUTF8)(u):l.mode===y.Attribute?(0, n.escapeAttribute)(u):l.mode===y.Text?(0, n.escapeText)(u):l.level===A.HTML?l.mode===y.ASCII?(0, o.encodeNonAsciiHTML)(u):(0, o.encodeHTML)(u):(0, n.encodeXML)(u)}t.encode=c;var a=Lu();Object.defineProperty(t,"encodeXML",{enumerable:true,get:function(){return a.encodeXML}}),Object.defineProperty(t,"escape",{enumerable:true,get:function(){return a.escape}}),Object.defineProperty(t,"escapeUTF8",{enumerable:true,get:function(){return a.escapeUTF8}}),Object.defineProperty(t,"escapeAttribute",{enumerable:true,get:function(){return a.escapeAttribute}}),Object.defineProperty(t,"escapeText",{enumerable:true,get:function(){return a.escapeText}});var v=$u();Object.defineProperty(t,"encodeHTML",{enumerable:true,get:function(){return v.encodeHTML}}),Object.defineProperty(t,"encodeNonAsciiHTML",{enumerable:true,get:function(){return v.encodeNonAsciiHTML}}),Object.defineProperty(t,"encodeHTML4",{enumerable:true,get:function(){return v.encodeHTML}}),Object.defineProperty(t,"encodeHTML5",{enumerable:true,get:function(){return v.encodeHTML}});var T=Tu();Object.defineProperty(t,"EntityDecoder",{enumerable:true,get:function(){return T.EntityDecoder}}),Object.defineProperty(t,"DecodingMode",{enumerable:true,get:function(){return T.DecodingMode}}),Object.defineProperty(t,"decodeXML",{enumerable:true,get:function(){return T.decodeXML}}),Object.defineProperty(t,"decodeHTML",{enumerable:true,get:function(){return T.decodeHTML}}),Object.defineProperty(t,"decodeHTMLStrict",{enumerable:true,get:function(){return T.decodeHTMLStrict}}),Object.defineProperty(t,"decodeHTMLAttribute",{enumerable:true,get:function(){return T.decodeHTMLAttribute}}),Object.defineProperty(t,"decodeHTML4",{enumerable:true,get:function(){return T.decodeHTML}}),Object.defineProperty(t,"decodeHTML5",{enumerable:true,get:function(){return T.decodeHTML}}),Object.defineProperty(t,"decodeHTML4Strict",{enumerable:true,get:function(){return T.decodeHTMLStrict}}),Object.defineProperty(t,"decodeHTML5Strict",{enumerable:true,get:function(){return T.decodeHTMLStrict}}),Object.defineProperty(t,"decodeXMLStrict",{enumerable:true,get:function(){return T.decodeXML}});})(Nu)),Nu}var bu={},ee;function Oe(){return ee||(ee=1,Object.defineProperty(bu,"__esModule",{value:true}),bu.attributeNames=bu.elementNames=void 0,bu.elementNames=new Map(["altGlyph","altGlyphDef","altGlyphItem","animateColor","animateMotion","animateTransform","clipPath","feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feDropShadow","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence","foreignObject","glyphRef","linearGradient","radialGradient","textPath"].map(function(t){return [t.toLowerCase(),t]})),bu.attributeNames=new Map(["definitionURL","attributeName","attributeType","baseFrequency","baseProfile","calcMode","clipPathUnits","diffuseConstant","edgeMode","filterUnits","glyphRef","gradientTransform","gradientUnits","kernelMatrix","kernelUnitLength","keyPoints","keySplines","keyTimes","lengthAdjust","limitingConeAngle","markerHeight","markerUnits","markerWidth","maskContentUnits","maskUnits","numOctaves","pathLength","patternContentUnits","patternTransform","patternUnits","pointsAtX","pointsAtY","pointsAtZ","preserveAlpha","preserveAspectRatio","primitiveUnits","refX","refY","repeatCount","repeatDur","requiredExtensions","requiredFeatures","specularConstant","specularExponent","spreadMethod","startOffset","stdDeviation","stitchTiles","surfaceScale","systemLanguage","tableValues","targetX","targetY","textLength","viewBox","viewTarget","xChannelSelector","yChannelSelector","zoomAndPan"].map(function(t){return [t.toLowerCase(),t]}))),bu}var te;function Pe(){if(te)return W;te=1;var t=W&&W.__assign||function(){return t=Object.assign||function(s){for(var i,g=1,x=arguments.length;g<x;g++){i=arguments[g];for(var N in i)Object.prototype.hasOwnProperty.call(i,N)&&(s[N]=i[N]);}return s},t.apply(this,arguments)},w=W&&W.__createBinding||(Object.create?(function(s,i,g,x){x===void 0&&(x=g);var N=Object.getOwnPropertyDescriptor(i,g);(!N||("get"in N?!i.__esModule:N.writable||N.configurable))&&(N={enumerable:true,get:function(){return i[g]}}),Object.defineProperty(s,x,N);}):(function(s,i,g,x){x===void 0&&(x=g),s[x]=i[g];})),o=W&&W.__setModuleDefault||(Object.create?(function(s,i){Object.defineProperty(s,"default",{enumerable:true,value:i});}):function(s,i){s.default=i;}),n=W&&W.__importStar||function(s){if(s&&s.__esModule)return s;var i={};if(s!=null)for(var g in s)g!=="default"&&Object.prototype.hasOwnProperty.call(s,g)&&w(i,s,g);return o(i,s),i};Object.defineProperty(W,"__esModule",{value:true}),W.render=void 0;var A=n(hu()),y=Le(),b=Oe(),f=new Set(["style","script","xmp","iframe","noembed","noframes","plaintext","noscript"]);function c(s){return s.replace(/"/g,"&quot;")}function a(s,i){var g;if(s){var x=((g=i.encodeEntities)!==null&&g!==void 0?g:i.decodeEntities)===false?c:i.xmlMode||i.encodeEntities!=="utf8"?y.encodeXML:y.escapeAttribute;return Object.keys(s).map(function(N){var L,C,p=(L=s[N])!==null&&L!==void 0?L:"";return i.xmlMode==="foreign"&&(N=(C=b.attributeNames.get(N))!==null&&C!==void 0?C:N),!i.emptyAttrs&&!i.xmlMode&&p===""?N:"".concat(N,'="').concat(x(p),'"')}).join(" ")}}var v=new Set(["area","base","basefont","br","col","command","embed","frame","hr","img","input","isindex","keygen","link","meta","param","source","track","wbr"]);function T(s,i){i===void 0&&(i={});for(var g=("length"in s)?s:[s],x="",N=0;N<g.length;N++)x+=u(g[N],i);return x}W.render=T,W.default=T;function u(s,i){switch(s.type){case A.Root:return T(s.children,i);case A.Doctype:case A.Directive:return m(s);case A.Comment:return d(s);case A.CDATA:return h(s);case A.Script:case A.Style:case A.Tag:return S(s,i);case A.Text:return r(s,i)}}var e=new Set(["mi","mo","mn","ms","mtext","annotation-xml","foreignObject","desc","title"]),l=new Set(["svg","math"]);function S(s,i){var g;i.xmlMode==="foreign"&&(s.name=(g=b.elementNames.get(s.name))!==null&&g!==void 0?g:s.name,s.parent&&e.has(s.parent.name)&&(i=t(t({},i),{xmlMode:false}))),!i.xmlMode&&l.has(s.name)&&(i=t(t({},i),{xmlMode:"foreign"}));var x="<".concat(s.name),N=a(s.attribs,i);return N&&(x+=" ".concat(N)),s.children.length===0&&(i.xmlMode?i.selfClosingTags!==false:i.selfClosingTags&&v.has(s.name))?(i.xmlMode||(x+=" "),x+="/>"):(x+=">",s.children.length>0&&(x+=T(s.children,i)),(i.xmlMode||!v.has(s.name))&&(x+="</".concat(s.name,">"))),x}function m(s){return "<".concat(s.data,">")}function r(s,i){var g,x=s.data||"";return ((g=i.encodeEntities)!==null&&g!==void 0?g:i.decodeEntities)!==false&&!(!i.xmlMode&&s.parent&&f.has(s.parent.name))&&(x=i.xmlMode||i.encodeEntities!=="utf8"?(0, y.encodeXML)(x):(0, y.escapeText)(x)),x}function h(s){return "<![CDATA[".concat(s.children[0].data,"]]>")}function d(s){return "<!--".concat(s.data,"-->")}return W}var re;function me(){if(re)return uu;re=1;var t=uu&&uu.__importDefault||function(a){return a&&a.__esModule?a:{default:a}};Object.defineProperty(uu,"__esModule",{value:true}),uu.getOuterHTML=A,uu.getInnerHTML=y,uu.getText=b,uu.textContent=f,uu.innerText=c;var w=cu(),o=t(Pe()),n=hu();function A(a,v){return (0, o.default)(a,v)}function y(a,v){return (0, w.hasChildren)(a)?a.children.map(function(T){return A(T,v)}).join(""):""}function b(a){return Array.isArray(a)?a.map(b).join(""):(0, w.isTag)(a)?a.name==="br"?`
`:b(a.children):(0, w.isCDATA)(a)?b(a.children):(0, w.isText)(a)?a.data:""}function f(a){return Array.isArray(a)?a.map(f).join(""):(0, w.hasChildren)(a)&&!(0, w.isComment)(a)?f(a.children):(0, w.isText)(a)?a.data:""}function c(a){return Array.isArray(a)?a.map(c).join(""):(0, w.hasChildren)(a)&&(a.type===n.ElementType.Tag||(0, w.isCDATA)(a))?c(a.children):(0, w.isText)(a)?a.data:""}return uu}var $$1={},ae;function Me(){if(ae)return $$1;ae=1,Object.defineProperty($$1,"__esModule",{value:true}),$$1.getChildren=w,$$1.getParent=o,$$1.getSiblings=n,$$1.getAttributeValue=A,$$1.hasAttrib=y,$$1.getName=b,$$1.nextElementSibling=f,$$1.prevElementSibling=c;var t=cu();function w(a){return (0, t.hasChildren)(a)?a.children:[]}function o(a){return a.parent||null}function n(a){var v,T,u=o(a);if(u!=null)return w(u);for(var e=[a],l=a.prev,S=a.next;l!=null;)e.unshift(l),v=l,l=v.prev;for(;S!=null;)e.push(S),T=S,S=T.next;return e}function A(a,v){var T;return (T=a.attribs)===null||T===void 0?void 0:T[v]}function y(a,v){return a.attribs!=null&&Object.prototype.hasOwnProperty.call(a.attribs,v)&&a.attribs[v]!=null}function b(a){return a.name}function f(a){for(var v,T=a.next;T!==null&&!(0, t.isTag)(T);)v=T,T=v.next;return T}function c(a){for(var v,T=a.prev;T!==null&&!(0, t.isTag)(T);)v=T,T=v.prev;return T}return $$1}var ru={},ie;function ke(){if(ie)return ru;ie=1,Object.defineProperty(ru,"__esModule",{value:true}),ru.removeElement=t,ru.replaceElement=w,ru.appendChild=o,ru.append=n,ru.prependChild=A,ru.prepend=y;function t(b){if(b.prev&&(b.prev.next=b.next),b.next&&(b.next.prev=b.prev),b.parent){var f=b.parent.children,c=f.lastIndexOf(b);c>=0&&f.splice(c,1);}b.next=null,b.prev=null,b.parent=null;}function w(b,f){var c=f.prev=b.prev;c&&(c.next=f);var a=f.next=b.next;a&&(a.prev=f);var v=f.parent=b.parent;if(v){var T=v.children;T[T.lastIndexOf(b)]=f,b.parent=null;}}function o(b,f){if(t(f),f.next=null,f.parent=b,b.children.push(f)>1){var c=b.children[b.children.length-2];c.next=f,f.prev=c;}else f.prev=null;}function n(b,f){t(f);var c=b.parent,a=b.next;if(f.next=a,f.prev=b,b.next=f,f.parent=c,a){if(a.prev=f,c){var v=c.children;v.splice(v.lastIndexOf(a),0,f);}}else c&&c.children.push(f);}function A(b,f){if(t(f),f.parent=b,f.prev=null,b.children.unshift(f)!==1){var c=b.children[1];c.prev=f,f.next=c;}else f.next=null;}function y(b,f){t(f);var c=b.parent;if(c){var a=c.children;a.splice(a.indexOf(b),0,f);}b.prev&&(b.prev.next=f),f.parent=c,f.prev=b.prev,f.next=b,b.prev=f;}return ru}var au={},ne;function ve(){if(ne)return au;ne=1,Object.defineProperty(au,"__esModule",{value:true}),au.filter=w,au.find=o,au.findOneChild=n,au.findOne=A,au.existsOne=y,au.findAll=b;var t=cu();function w(f,c,a,v){return a===void 0&&(a=true),v===void 0&&(v=1/0),o(f,Array.isArray(c)?c:[c],a,v)}function o(f,c,a,v){for(var T=[],u=[Array.isArray(c)?c:[c]],e=[0];;){if(e[0]>=u[0].length){if(e.length===1)return T;u.shift(),e.shift();continue}var l=u[0][e[0]++];if(f(l)&&(T.push(l),--v<=0))return T;a&&(0, t.hasChildren)(l)&&l.children.length>0&&(e.unshift(0),u.unshift(l.children));}}function n(f,c){return c.find(f)}function A(f,c,a){a===void 0&&(a=true);for(var v=Array.isArray(c)?c:[c],T=0;T<v.length;T++){var u=v[T];if((0, t.isTag)(u)&&f(u))return u;if(a&&(0, t.hasChildren)(u)&&u.children.length>0){var e=A(f,u.children,true);if(e)return e}}return null}function y(f,c){return (Array.isArray(c)?c:[c]).some(function(a){return (0, t.isTag)(a)&&f(a)||(0, t.hasChildren)(a)&&y(f,a.children)})}function b(f,c){for(var a=[],v=[Array.isArray(c)?c:[c]],T=[0];;){if(T[0]>=v[0].length){if(v.length===1)return a;v.shift(),T.shift();continue}var u=v[0][T[0]++];(0, t.isTag)(u)&&f(u)&&a.push(u),(0, t.hasChildren)(u)&&u.children.length>0&&(T.unshift(0),v.unshift(u.children));}}return au}var iu={},ce$1;function xe(){if(ce$1)return iu;ce$1=1,Object.defineProperty(iu,"__esModule",{value:true}),iu.testElement=b,iu.getElements=f,iu.getElementById=c,iu.getElementsByTagName=a,iu.getElementsByClassName=v,iu.getElementsByTagType=T;var t=cu(),w=ve(),o={tag_name:function(u){return typeof u=="function"?function(e){return (0, t.isTag)(e)&&u(e.name)}:u==="*"?t.isTag:function(e){return (0, t.isTag)(e)&&e.name===u}},tag_type:function(u){return typeof u=="function"?function(e){return u(e.type)}:function(e){return e.type===u}},tag_contains:function(u){return typeof u=="function"?function(e){return (0, t.isText)(e)&&u(e.data)}:function(e){return (0, t.isText)(e)&&e.data===u}}};function n(u,e){return typeof e=="function"?function(l){return (0, t.isTag)(l)&&e(l.attribs[u])}:function(l){return (0, t.isTag)(l)&&l.attribs[u]===e}}function A(u,e){return function(l){return u(l)||e(l)}}function y(u){var e=Object.keys(u).map(function(l){var S=u[l];return Object.prototype.hasOwnProperty.call(o,l)?o[l](S):n(l,S)});return e.length===0?null:e.reduce(A)}function b(u,e){var l=y(u);return l?l(e):true}function f(u,e,l,S){S===void 0&&(S=1/0);var m=y(u);return m?(0, w.filter)(m,e,l,S):[]}function c(u,e,l){return l===void 0&&(l=true),Array.isArray(e)||(e=[e]),(0, w.findOne)(n("id",u),e,l)}function a(u,e,l,S){return l===void 0&&(l=true),S===void 0&&(S=1/0),(0, w.filter)(o.tag_name(u),e,l,S)}function v(u,e,l,S){return l===void 0&&(l=true),S===void 0&&(S=1/0),(0, w.filter)(n("class",u),e,l,S)}function T(u,e,l,S){return l===void 0&&(l=true),S===void 0&&(S=1/0),(0, w.filter)(o.tag_type(u),e,l,S)}return iu}var nu={},se;function Ce(){if(se)return nu;se=1,Object.defineProperty(nu,"__esModule",{value:true}),nu.DocumentPosition=void 0,nu.removeSubsets=w,nu.compareDocumentPosition=n,nu.uniqueSort=A;var t=cu();function w(y){for(var b=y.length;--b>=0;){var f=y[b];if(b>0&&y.lastIndexOf(f,b-1)>=0){y.splice(b,1);continue}for(var c=f.parent;c;c=c.parent)if(y.includes(c)){y.splice(b,1);break}}return y}var o;(function(y){y[y.DISCONNECTED=1]="DISCONNECTED",y[y.PRECEDING=2]="PRECEDING",y[y.FOLLOWING=4]="FOLLOWING",y[y.CONTAINS=8]="CONTAINS",y[y.CONTAINED_BY=16]="CONTAINED_BY";})(o||(nu.DocumentPosition=o={}));function n(y,b){var f=[],c=[];if(y===b)return 0;for(var a=(0, t.hasChildren)(y)?y:y.parent;a;)f.unshift(a),a=a.parent;for(a=(0, t.hasChildren)(b)?b:b.parent;a;)c.unshift(a),a=a.parent;for(var v=Math.min(f.length,c.length),T=0;T<v&&f[T]===c[T];)T++;if(T===0)return o.DISCONNECTED;var u=f[T-1],e=u.children,l=f[T],S=c[T];return e.indexOf(l)>e.indexOf(S)?u===b?o.FOLLOWING|o.CONTAINED_BY:o.FOLLOWING:u===y?o.PRECEDING|o.CONTAINS:o.PRECEDING}function A(y){return y=y.filter(function(b,f,c){return !c.includes(b,f+1)}),y.sort(function(b,f){var c=n(b,f);return c&o.PRECEDING?-1:c&o.FOLLOWING?1:0}),y}return nu}var vu={},oe;function Re(){if(oe)return vu;oe=1,Object.defineProperty(vu,"__esModule",{value:true}),vu.getFeed=o;var t=me(),w=xe();function o(u){var e=c(T,u);return e?e.name==="feed"?n(e):A(e):null}function n(u){var e,l=u.children,S={type:"atom",items:(0, w.getElementsByTagName)("entry",l).map(function(h){var d,s=h.children,i={media:f(s)};v(i,"id","id",s),v(i,"title","title",s);var g=(d=c("link",s))===null||d===void 0?void 0:d.attribs.href;g&&(i.link=g);var x=a("summary",s)||a("content",s);x&&(i.description=x);var N=a("updated",s);return N&&(i.pubDate=new Date(N)),i})};v(S,"id","id",l),v(S,"title","title",l);var m=(e=c("link",l))===null||e===void 0?void 0:e.attribs.href;m&&(S.link=m),v(S,"description","subtitle",l);var r=a("updated",l);return r&&(S.updated=new Date(r)),v(S,"author","email",l,true),S}function A(u){var e,l,S=(l=(e=c("channel",u.children))===null||e===void 0?void 0:e.children)!==null&&l!==void 0?l:[],m={type:u.name.substr(0,3),id:"",items:(0, w.getElementsByTagName)("item",u.children).map(function(h){var d=h.children,s={media:f(d)};v(s,"id","guid",d),v(s,"title","title",d),v(s,"link","link",d),v(s,"description","description",d);var i=a("pubDate",d)||a("dc:date",d);return i&&(s.pubDate=new Date(i)),s})};v(m,"title","title",S),v(m,"link","link",S),v(m,"description","description",S);var r=a("lastBuildDate",S);return r&&(m.updated=new Date(r)),v(m,"author","managingEditor",S,true),m}var y=["url","type","lang"],b=["fileSize","bitrate","framerate","samplingrate","channels","duration","height","width"];function f(u){return (0, w.getElementsByTagName)("media:content",u).map(function(e){for(var l=e.attribs,S={medium:l.medium,isDefault:!!l.isDefault},m=0,r=y;m<r.length;m++){var h=r[m];l[h]&&(S[h]=l[h]);}for(var d=0,s=b;d<s.length;d++){var h=s[d];l[h]&&(S[h]=parseInt(l[h],10));}return l.expression&&(S.expression=l.expression),S})}function c(u,e){return (0, w.getElementsByTagName)(u,e,true,1)[0]}function a(u,e,l){return l===void 0&&(l=false),(0, t.textContent)((0, w.getElementsByTagName)(u,e,l,1)).trim()}function v(u,e,l,S,m){m===void 0&&(m=false);var r=a(l,S,m);r&&(u[e]=r);}function T(u){return u==="rss"||u==="feed"||u==="rdf:RDF"}return vu}var de;function qu(){return de||(de=1,(function(t){var w=lu&&lu.__createBinding||(Object.create?(function(A,y,b,f){f===void 0&&(f=b);var c=Object.getOwnPropertyDescriptor(y,b);(!c||("get"in c?!y.__esModule:c.writable||c.configurable))&&(c={enumerable:true,get:function(){return y[b]}}),Object.defineProperty(A,f,c);}):(function(A,y,b,f){f===void 0&&(f=b),A[f]=y[b];})),o=lu&&lu.__exportStar||function(A,y){for(var b in A)b!=="default"&&!Object.prototype.hasOwnProperty.call(y,b)&&w(y,A,b);};Object.defineProperty(t,"__esModule",{value:true}),t.hasChildren=t.isDocument=t.isComment=t.isText=t.isCDATA=t.isTag=void 0,o(me(),t),o(Me(),t),o(ke(),t),o(ve(),t),o(xe(),t),o(Ce(),t),o(Re(),t);var n=cu();Object.defineProperty(t,"isTag",{enumerable:true,get:function(){return n.isTag}}),Object.defineProperty(t,"isCDATA",{enumerable:true,get:function(){return n.isCDATA}}),Object.defineProperty(t,"isText",{enumerable:true,get:function(){return n.isText}}),Object.defineProperty(t,"isComment",{enumerable:true,get:function(){return n.isComment}}),Object.defineProperty(t,"isDocument",{enumerable:true,get:function(){return n.isDocument}}),Object.defineProperty(t,"hasChildren",{enumerable:true,get:function(){return n.hasChildren}});})(lu)),lu}var fe;function Be(){return fe||(fe=1,(function(t){var w=J&&J.__createBinding||(Object.create?(function(r,h,d,s){s===void 0&&(s=d);var i=Object.getOwnPropertyDescriptor(h,d);(!i||("get"in i?!h.__esModule:i.writable||i.configurable))&&(i={enumerable:true,get:function(){return h[d]}}),Object.defineProperty(r,s,i);}):(function(r,h,d,s){s===void 0&&(s=d),r[s]=h[d];})),o=J&&J.__setModuleDefault||(Object.create?(function(r,h){Object.defineProperty(r,"default",{enumerable:true,value:h});}):function(r,h){r.default=h;}),n=J&&J.__importStar||function(r){if(r&&r.__esModule)return r;var h={};if(r!=null)for(var d in r)d!=="default"&&Object.prototype.hasOwnProperty.call(r,d)&&w(h,r,d);return o(h,r),h},A=J&&J.__importDefault||function(r){return r&&r.__esModule?r:{default:r}};Object.defineProperty(t,"__esModule",{value:true}),t.DomUtils=t.parseFeed=t.getFeed=t.ElementType=t.Tokenizer=t.createDomStream=t.parseDOM=t.parseDocument=t.DefaultHandler=t.DomHandler=t.Parser=void 0;var y=zu(),b=zu();Object.defineProperty(t,"Parser",{enumerable:true,get:function(){return b.Parser}});var f=cu(),c=cu();Object.defineProperty(t,"DomHandler",{enumerable:true,get:function(){return c.DomHandler}}),Object.defineProperty(t,"DefaultHandler",{enumerable:true,get:function(){return c.DomHandler}});function a(r,h){var d=new f.DomHandler(void 0,h);return new y.Parser(d,h).end(r),d.root}t.parseDocument=a;function v(r,h){return a(r,h).children}t.parseDOM=v;function T(r,h,d){var s=new f.DomHandler(r,h,d);return new y.Parser(s,h)}t.createDomStream=T;var u=ge();Object.defineProperty(t,"Tokenizer",{enumerable:true,get:function(){return A(u).default}}),t.ElementType=n(hu());var e=qu(),l=qu();Object.defineProperty(t,"getFeed",{enumerable:true,get:function(){return l.getFeed}});var S={xmlMode:true};function m(r,h){return h===void 0&&(h=S),(0, e.getFeed)(v(r,h))}t.parseFeed=m,t.DomUtils=n(qu());})(J)),J}var Du,le;function je(){return le||(le=1,Du=t=>{if(typeof t!="string")throw new TypeError("Expected a string");return t.replace(/[|\\{}()[\]^$+*?.]/g,"\\$&").replace(/-/g,"\\x2d")}),Du}var xu={},be;function He(){if(be)return xu;be=1,Object.defineProperty(xu,"__esModule",{value:true});function t(o){return Object.prototype.toString.call(o)==="[object Object]"}function w(o){var n,A;return t(o)===false?false:(n=o.constructor,n===void 0?true:(A=n.prototype,!(t(A)===false||A.hasOwnProperty("isPrototypeOf")===false)))}return xu.isPlainObject=w,xu}var yu={exports:{}},Ue=yu.exports,he;function Ve(){return he||(he=1,(function(t){(function(w,o){t.exports?t.exports=o():w.parseSrcset=o();})(Ue,function(){return function(w){function o(s){return s===" "||s==="	"||s===`
`||s==="\f"||s==="\r"}function n(s){var i,g=s.exec(w.substring(m));if(g)return i=g[0],m+=i.length,i}for(var A=w.length,y=/^[ \t\n\r\u000c]+/,b=/^[, \t\n\r\u000c]+/,f=/^[^ \t\n\r\u000c]+/,c=/[,]+$/,a=/^\d+$/,v=/^-?(?:[0-9]+|[0-9]*\.[0-9]+)(?:[eE][+-]?[0-9]+)?$/,T,u,e,l,S,m=0,r=[];;){if(n(b),m>=A)return r;T=n(f),u=[],T.slice(-1)===","?(T=T.replace(c,""),d()):h();}function h(){for(n(y),e="",l="in descriptor";;){if(S=w.charAt(m),l==="in descriptor")if(o(S))e&&(u.push(e),e="",l="after descriptor");else if(S===","){m+=1,e&&u.push(e),d();return}else if(S==="(")e=e+S,l="in parens";else if(S===""){e&&u.push(e),d();return}else e=e+S;else if(l==="in parens")if(S===")")e=e+S,l="in descriptor";else if(S===""){u.push(e),d();return}else e=e+S;else if(l==="after descriptor"&&!o(S))if(S===""){d();return}else l="in descriptor",m-=1;m+=1;}}function d(){var s=false,i,g,x,N,L={},C,p,_,D,O;for(N=0;N<u.length;N++)C=u[N],p=C[C.length-1],_=C.substring(0,C.length-1),D=parseInt(_,10),O=parseFloat(_),a.test(_)&&p==="w"?((i||g)&&(s=true),D===0?s=true:i=D):v.test(_)&&p==="x"?((i||g||x)&&(s=true),O<0?s=true:g=O):a.test(_)&&p==="h"?((x||g)&&(s=true),D===0?s=true:x=D):s=true;s?console&&console.log&&console.log("Invalid srcset descriptor found in '"+w+"' at '"+C+"'."):(L.url=T,i&&(L.w=i),g&&(L.d=g),x&&(L.h=x),r.push(L));}}});})(yu)),yu.exports}var Iu,pe;function Fe(){if(pe)return Iu;pe=1;const t=Be(),w=je(),{isPlainObject:o}=He(),n=an(),A=Ve(),{parse:y}=postcss,b=["img","audio","video","picture","svg","object","map","iframe","embed"],f=["script","style"];function c(m,r){m&&Object.keys(m).forEach(function(h){r(m[h],h);});}function a(m,r){return {}.hasOwnProperty.call(m,r)}function v(m,r){const h=[];return c(m,function(d){r(d)&&h.push(d);}),h}function T(m){for(const r in m)if(a(m,r))return  false;return  true}function u(m){return m.map(function(r){if(!r.url)throw new Error("URL missing");return r.url+(r.w?` ${r.w}w`:"")+(r.h?` ${r.h}h`:"")+(r.d?` ${r.d}x`:"")}).join(", ")}Iu=l;const e=/^[^\0\t\n\f\r /<=>]+$/;function l(m,r,h){if(m==null)return "";typeof m=="number"&&(m=m.toString());let d="",s="";function i(E,I){const q=this;this.tag=E,this.attribs=I||{},this.tagPosition=d.length,this.text="",this.openingTagLength=0,this.mediaChildren=[],this.updateParentNodeText=function(){if(R.length){const M=R[R.length-1];M.text+=q.text;}},this.updateParentNodeMediaChildren=function(){R.length&&b.includes(this.tag)&&R[R.length-1].mediaChildren.push(this.tag);};}r=Object.assign({},l.defaults,r),r.parser=Object.assign({},S,r.parser);const g=function(E){return r.allowedTags===false||(r.allowedTags||[]).indexOf(E)>-1};f.forEach(function(E){g(E)&&!r.allowVulnerableTags&&console.warn(`

⚠️ Your \`allowedTags\` option includes, \`${E}\`, which is inherently
vulnerable to XSS attacks. Please remove it from \`allowedTags\`.
Or, to disable this warning, add the \`allowVulnerableTags\` option
and ensure you are accounting for this risk.

`);});const x=r.nonTextTags||["script","style","textarea","option"];let N,L;r.allowedAttributes&&(N={},L={},c(r.allowedAttributes,function(E,I){N[I]=[];const q=[];E.forEach(function(M){typeof M=="string"&&M.indexOf("*")>=0?q.push(w(M).replace(/\\\*/g,".*")):N[I].push(M);}),q.length&&(L[I]=new RegExp("^("+q.join("|")+")$"));}));const C={},p={},_={};c(r.allowedClasses,function(E,I){if(N&&(a(N,I)||(N[I]=[]),N[I].push("class")),C[I]=E,Array.isArray(E)){const q=[];C[I]=[],_[I]=[],E.forEach(function(M){typeof M=="string"&&M.indexOf("*")>=0?q.push(w(M).replace(/\\\*/g,".*")):M instanceof RegExp?_[I].push(M):C[I].push(M);}),q.length&&(p[I]=new RegExp("^("+q.join("|")+")$"));}});const D={};let O;c(r.transformTags,function(E,I){let q;typeof E=="function"?q=E:typeof E=="string"&&(q=l.simpleTransform(E)),I==="*"?O=q:D[I]=q;});let P,R,V,F,z,Q,su=false;Pu();const Ou=new t.Parser({onopentag:function(E,I){if(r.onOpenTag&&r.onOpenTag(E,I),r.enforceHtmlBoundary&&E==="html"&&Pu(),z){Q++;return}const q=new i(E,I);R.push(q);let M=false;const G=!!q.text;let X;if(a(D,E)&&(X=D[E](E,I),q.attribs=I=X.attribs,X.text!==void 0&&(q.innerText=X.text),E!==X.tagName&&(q.name=E=X.tagName,F[P]=X.tagName)),O&&(X=O(E,I),q.attribs=I=X.attribs,E!==X.tagName&&(q.name=E=X.tagName,F[P]=X.tagName)),(!g(E)||r.disallowedTagsMode==="recursiveEscape"&&!T(V)||r.nestingLimit!=null&&P>=r.nestingLimit)&&(M=true,V[P]=true,(r.disallowedTagsMode==="discard"||r.disallowedTagsMode==="completelyDiscard")&&x.indexOf(E)!==-1&&(z=true,Q=1)),P++,M){if(r.disallowedTagsMode==="discard"||r.disallowedTagsMode==="completelyDiscard"){if(q.innerText&&!G){const U=ou(q.innerText);r.textFilter?d+=r.textFilter(U,E):d+=U,su=true;}return}s=d,d="";}d+="<"+E,E==="script"&&(r.allowedScriptHostnames||r.allowedScriptDomains)&&(q.innerText=""),M&&(r.disallowedTagsMode==="escape"||r.disallowedTagsMode==="recursiveEscape")&&r.preserveEscapedAttributes?c(I,function(U,B){d+=" "+B+'="'+ou(U||"",true)+'"';}):(!N||a(N,E)||N["*"])&&c(I,function(U,B){if(!e.test(B)){delete q.attribs[B];return}if(U===""&&!r.allowedEmptyAttributes.includes(B)&&(r.nonBooleanAttributes.includes(B)||r.nonBooleanAttributes.includes("*"))){delete q.attribs[B];return}let wu=false;if(!N||a(N,E)&&N[E].indexOf(B)!==-1||N["*"]&&N["*"].indexOf(B)!==-1||a(L,E)&&L[E].test(B)||L["*"]&&L["*"].test(B))wu=true;else if(N&&N[E]){for(const j of N[E])if(o(j)&&j.name&&j.name===B){wu=true;let H="";if(j.multiple===true){const du=U.split(" ");for(const eu of du)j.values.indexOf(eu)!==-1&&(H===""?H=eu:H+=" "+eu);}else j.values.indexOf(U)>=0&&(H=U);U=H;}}if(wu){if(r.allowedSchemesAppliedToAttributes.indexOf(B)!==-1&&Mu(E,U)){delete q.attribs[B];return}if(E==="script"&&B==="src"){let j=true;try{const H=ku(U);if(r.allowedScriptHostnames||r.allowedScriptDomains){const du=(r.allowedScriptHostnames||[]).find(function(Z){return Z===H.url.hostname}),eu=(r.allowedScriptDomains||[]).find(function(Z){return H.url.hostname===Z||H.url.hostname.endsWith(`.${Z}`)});j=du||eu;}}catch{j=false;}if(!j){delete q.attribs[B];return}}if(E==="iframe"&&B==="src"){let j=true;try{const H=ku(U);if(H.isRelativeUrl)j=a(r,"allowIframeRelativeUrls")?r.allowIframeRelativeUrls:!r.allowedIframeHostnames&&!r.allowedIframeDomains;else if(r.allowedIframeHostnames||r.allowedIframeDomains){const du=(r.allowedIframeHostnames||[]).find(function(Z){return Z===H.url.hostname}),eu=(r.allowedIframeDomains||[]).find(function(Z){return H.url.hostname===Z||H.url.hostname.endsWith(`.${Z}`)});j=du||eu;}}catch{j=false;}if(!j){delete q.attribs[B];return}}if(B==="srcset")try{let j=A(U);if(j.forEach(function(H){Mu("srcset",H.url)&&(H.evil=!0);}),j=v(j,function(H){return !H.evil}),j.length)U=u(v(j,function(H){return !H.evil})),q.attribs[B]=U;else {delete q.attribs[B];return}}catch{delete q.attribs[B];return}if(B==="class"){const j=C[E],H=C["*"],du=p[E],eu=_[E],Z=_["*"],Ee=p["*"],Ru=[du,Ee].concat(eu,Z).filter(function(Ae){return Ae});if(j&&H?U=Cu(U,n(j,H),Ru):U=Cu(U,j||H,Ru),!U.length){delete q.attribs[B];return}}if(B==="style"){if(r.parseStyleAttributes)try{const j=y(E+" {"+U+"}",{map:!1}),H=ye(j,r.allowedStyles);if(U=Te(H),U.length===0){delete q.attribs[B];return}}catch{typeof window<"u"&&console.warn('Failed to parse "'+E+" {"+U+`}", If you're running this in a browser, we recommend to disable style parsing: options.parseStyleAttributes: false, since this only works in a node environment due to a postcss dependency, More info: https://github.com/apostrophecms/sanitize-html/issues/547`),delete q.attribs[B];return}else if(r.allowedStyles)throw new Error("allowedStyles option cannot be used together with parseStyleAttributes: false.")}d+=" "+B,U&&U.length?d+='="'+ou(U,true)+'"':r.allowedEmptyAttributes.includes(B)&&(d+='=""');}else delete q.attribs[B];}),r.selfClosing.indexOf(E)!==-1?d+=" />":(d+=">",q.innerText&&!G&&!r.textFilter&&(d+=ou(q.innerText),su=true)),M&&(d=s+ou(d),s=""),q.openingTagLength=d.length-q.tagPosition;},ontext:function(E){if(z)return;const I=R[R.length-1];let q;if(I&&(q=I.tag,E=I.innerText!==void 0?I.innerText:E),r.disallowedTagsMode==="completelyDiscard"&&!g(q))E="";else if((r.disallowedTagsMode==="discard"||r.disallowedTagsMode==="completelyDiscard")&&(q==="script"||q==="style"))d+=E;else if(!su){const M=ou(E,false);r.textFilter?d+=r.textFilter(M,q):d+=M;}if(R.length){const M=R[R.length-1];M.text+=E;}},onclosetag:function(E,I){if(r.onCloseTag&&r.onCloseTag(E,I),z)if(Q--,!Q)z=false;else return;const q=R.pop();if(!q)return;if(q.tag!==E){R.push(q);return}z=r.enforceHtmlBoundary?E==="html":false,P--;const M=V[P];if(M){if(delete V[P],r.disallowedTagsMode==="discard"||r.disallowedTagsMode==="completelyDiscard"){q.updateParentNodeText();return}s=d,d="";}if(F[P]&&(E=F[P],delete F[P]),r.exclusiveFilter){const G=r.exclusiveFilter(q);if(G==="excludeTag"){M&&(d=s,s=""),d=d.substring(0,q.tagPosition)+d.substring(q.tagPosition+q.openingTagLength);return}else if(G){d=d.substring(0,q.tagPosition);return}}if(q.updateParentNodeMediaChildren(),q.updateParentNodeText(),r.selfClosing.indexOf(E)!==-1||I&&!g(E)&&["escape","recursiveEscape"].indexOf(r.disallowedTagsMode)>=0){M&&(d=s,s="");return}d+="</"+E+">",M&&(d=s+ou(d),s=""),su=false;}},r.parser);return Ou.write(m),Ou.end(),d;function Pu(){d="",P=0,R=[],V={},F={},z=false,Q=0;}function ou(E,I){return typeof E!="string"&&(E=E+""),r.parser.decodeEntities&&(E=E.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"),I&&(E=E.replace(/"/g,"&quot;"))),E=E.replace(/&(?![a-zA-Z0-9#]{1,20};)/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;"),I&&(E=E.replace(/"/g,"&quot;")),E}function Mu(E,I){for(I=I.replace(/[\x00-\x20]+/g,"");;){const G=I.indexOf("<!--");if(G===-1)break;const X=I.indexOf("-->",G+4);if(X===-1)break;I=I.substring(0,G)+I.substring(X+3);}const q=I.match(/^([a-zA-Z][a-zA-Z0-9.\-+]*):/);if(!q)return I.match(/^[/\\]{2}/)?!r.allowProtocolRelative:false;const M=q[1].toLowerCase();return a(r.allowedSchemesByTag,E)?r.allowedSchemesByTag[E].indexOf(M)===-1:!r.allowedSchemes||r.allowedSchemes.indexOf(M)===-1}function ku(E){if(E=E.replace(/^(\w+:)?\s*[\\/]\s*[\\/]/,"$1//"),E.startsWith("relative:"))throw new Error("relative: exploit attempt");let I="relative://relative-site";for(let G=0;G<100;G++)I+=`/${G}`;const q=new URL(E,I);return {isRelativeUrl:q&&q.hostname==="relative-site"&&q.protocol==="relative:",url:q}}function ye(E,I){if(!I)return E;const q=E.nodes[0];let M;return I[q.selector]&&I["*"]?M=n(I[q.selector],I["*"]):M=I[q.selector]||I["*"],M&&(E.nodes[0].nodes=q.nodes.reduce(we(M),[])),E}function Te(E){return E.nodes[0].nodes.reduce(function(I,q){return I.push(`${q.prop}:${q.value}${q.important?" !important":""}`),I},[]).join(";")}function we(E){return function(I,q){return a(E,q.prop)&&E[q.prop].some(function(G){return G.test(q.value)})&&I.push(q),I}}function Cu(E,I,q){return I?(E=E.split(/\s+/),E.filter(function(M){return I.indexOf(M)!==-1||q.some(function(G){return G.test(M)})}).join(" ")):E}}const S={decodeEntities:true};return l.defaults={allowedTags:["address","article","aside","footer","header","h1","h2","h3","h4","h5","h6","hgroup","main","nav","section","blockquote","dd","div","dl","dt","figcaption","figure","hr","li","menu","ol","p","pre","ul","a","abbr","b","bdi","bdo","br","cite","code","data","dfn","em","i","kbd","mark","q","rb","rp","rt","rtc","ruby","s","samp","small","span","strong","sub","sup","time","u","var","wbr","caption","col","colgroup","table","tbody","td","tfoot","th","thead","tr"],nonBooleanAttributes:["abbr","accept","accept-charset","accesskey","action","allow","alt","as","autocapitalize","autocomplete","blocking","charset","cite","class","color","cols","colspan","content","contenteditable","coords","crossorigin","data","datetime","decoding","dir","dirname","download","draggable","enctype","enterkeyhint","fetchpriority","for","form","formaction","formenctype","formmethod","formtarget","headers","height","hidden","high","href","hreflang","http-equiv","id","imagesizes","imagesrcset","inputmode","integrity","is","itemid","itemprop","itemref","itemtype","kind","label","lang","list","loading","low","max","maxlength","media","method","min","minlength","name","nonce","optimum","pattern","ping","placeholder","popover","popovertarget","popovertargetaction","poster","preload","referrerpolicy","rel","rows","rowspan","sandbox","scope","shape","size","sizes","slot","span","spellcheck","src","srcdoc","srclang","srcset","start","step","style","tabindex","target","title","translate","type","usemap","value","width","wrap","onauxclick","onafterprint","onbeforematch","onbeforeprint","onbeforeunload","onbeforetoggle","onblur","oncancel","oncanplay","oncanplaythrough","onchange","onclick","onclose","oncontextlost","oncontextmenu","oncontextrestored","oncopy","oncuechange","oncut","ondblclick","ondrag","ondragend","ondragenter","ondragleave","ondragover","ondragstart","ondrop","ondurationchange","onemptied","onended","onerror","onfocus","onformdata","onhashchange","oninput","oninvalid","onkeydown","onkeypress","onkeyup","onlanguagechange","onload","onloadeddata","onloadedmetadata","onloadstart","onmessage","onmessageerror","onmousedown","onmouseenter","onmouseleave","onmousemove","onmouseout","onmouseover","onmouseup","onoffline","ononline","onpagehide","onpageshow","onpaste","onpause","onplay","onplaying","onpopstate","onprogress","onratechange","onreset","onresize","onrejectionhandled","onscroll","onscrollend","onsecuritypolicyviolation","onseeked","onseeking","onselect","onslotchange","onstalled","onstorage","onsubmit","onsuspend","ontimeupdate","ontoggle","onunhandledrejection","onunload","onvolumechange","onwaiting","onwheel"],disallowedTagsMode:"discard",allowedAttributes:{a:["href","name","target"],img:["src","srcset","alt","title","width","height","loading"]},allowedEmptyAttributes:["alt"],selfClosing:["img","br","hr","area","base","basefont","input","link","meta"],allowedSchemes:["http","https","ftp","mailto","tel"],allowedSchemesByTag:{},allowedSchemesAppliedToAttributes:["href","src","cite"],allowProtocolRelative:true,enforceHtmlBoundary:false,parseStyleAttributes:true,preserveEscapedAttributes:false},l.simpleTransform=function(m,r,h){return h=h===void 0?true:h,r=r||{},function(d,s){let i;if(h)for(i in r)s[i]=r[i];else s=r;return {tagName:m,attribs:s}}},Iu}var Ge=Fe();const Ze=sn(Ge);

function z$1(a){a.push('<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6L8 10L12 6"></path></svg>');}function j(a){a.push('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z"></path></svg>');}function C(a){a.push('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke-linecap="round" stroke-linejoin="round" d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"></path></svg>');}function T(a){a.push('<svg fill="none" stroke="currentColor" viewBox="0 0 24 24" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>');}function L$1(a){a.push('<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" stroke-linecap="round" stroke-linejoin="round"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"></path></svg>');}function q$1(a){return Ze(a)}function B$3(a,i){a.component(t=>{let n,u,v,r,d,e=i.type,p=fallback(i.messages,()=>[],true),g=fallback(i.expanded,true);let o=0;if(n=p.length,u=p[0],v=e.charAt(0).toUpperCase()+e.slice(1),r=u?.duration!==null,d=r?`${u.duration}s`:"0s",t.push(`<div${attr_class(`toast-body ${stringify(e)}`,"svelte-irmu64")} role="status" aria-live="polite" data-testid="toast-body"${attr_style(`transform: translateX(${stringify(o)}px); opacity: ${stringify(1-Math.abs(o)/300)};`)}><div class="toast-header svelte-irmu64" role="button" tabindex="0"><div${attr_class(`toast-icon ${stringify(e)}`,"svelte-irmu64")}>`),e==="warning"?(t.push("<!--[-->"),L$1(t)):(t.push("<!--[!-->"),e==="info"?(t.push("<!--[-->"),C(t)):(t.push("<!--[!-->"),e==="success"?(t.push("<!--[-->"),T(t)):(t.push("<!--[!-->"),e==="error"?(t.push("<!--[-->"),j(t)):t.push("<!--[!-->"),t.push("<!--]-->")),t.push("<!--]-->")),t.push("<!--]-->")),t.push(`<!--]--></div> <div class="toast-title-row svelte-irmu64"><span${attr_class(`toast-title ${stringify(e)}`,"svelte-irmu64")}>${escape_html(v)} `),n>1?(t.push("<!--[-->"),t.push(`<span class="toast-count svelte-irmu64">(${escape_html(n)})</span>`)):t.push("<!--[!-->"),t.push(`<!--]--></span> <div${attr_class("chevron svelte-irmu64",void 0,{expanded:g,visible:n>0})}>`),z$1(t),t.push(`<!----></div></div> <button${attr_class(`toast-close ${stringify(e)}`,"svelte-irmu64")} type="button" aria-label="Close" data-testid="toast-close"><span aria-hidden="true">×</span></button></div> `),g){t.push("<!--[-->"),t.push('<div class="toast-messages svelte-irmu64"><!--[-->');const f=ensure_array_like(p);for(let h=0,m=f.length;h<m;h++){let _=f[h];t.push(`<div${attr_class(`toast-message-item ${stringify(e)}`,"svelte-irmu64")}><div${attr_class(`toast-message-text ${stringify(e)}`,"svelte-irmu64")} data-testid="toast-text">${html(q$1(_.message))}</div></div> `),h<p.length-1?(t.push("<!--[-->"),t.push('<div class="toast-separator svelte-irmu64"></div>')):t.push("<!--[!-->"),t.push("<!--]-->");}t.push("<!--]--></div>");}else t.push("<!--[!-->");t.push("<!--]--> "),r?(t.push("<!--[-->"),t.push(`<div${attr_class(`timer ${stringify(e)}`,"svelte-irmu64")}${attr_style(`animation-duration: ${stringify(d)}`)}></div>`)):t.push("<!--[!-->"),t.push("<!--]--></div>"),bind_props(i,{type:e,messages:p,expanded:g});});}function P$2(a,i){a.component(t=>{var n;let u=fallback(i.messages,()=>[],true),v=i.on_close;const r=spring(0,{stiffness:.4,damping:.5});let d=[];function e(l){const o=new Map;return l.forEach(c=>{const f=c.type;o.has(f)||o.set(f,{type:c.type,messages:[],expanded:true}),o.get(f).messages.push(c);}),Array.from(o.values())}function p(l){l.length>0&&"parentIFrame"in window&&window.parentIFrame?.getPageInfo(o=>{o.scrollTop<o.offsetTop?r.set(0):r.set(o.scrollTop-o.offsetTop);});}p(u),d=e(u),t.push(`<div class="toast-wrap svelte-1qhecvt"${attr_style(`--toast-top: ${stringify(store_get(n??={},"$top",r))}px;`)}><!--[-->`);const g=ensure_array_like(d);for(let l=0,o=g.length;l<o;l++){let c=g[l];t.push('<div class="toast-item svelte-1qhecvt">'),B$3(t,{type:c.type,messages:c.messages,expanded:c.expanded}),t.push("<!----></div>");}t.push("<!--]--></div>"),n&&unsubscribe_stores(n),bind_props(i,{messages:u,on_close:v});});}let U$2 = class U{current={};fn_outputs={};fn_inputs={};pending_outputs=new Map;fn_status={};show_progress={};register(i,t,n,u){this.fn_outputs[i]=t,this.fn_inputs[i]=n,this.show_progress[i]=u;}clear(i){i in this.current&&(this.current[i]={});}update(i){this.resolve_args(i).forEach(({id:n,queue_position:u,queue_size:v,eta:r,status:d,message:e,progress:p,stream_state:g,time_limit:l,type:o})=>{this.current[n]={queue:i.queue||false,queue_size:v,queue_position:u,eta:r,stream_state:g,message:e,progress:p||void 0,status:d,fn_index:i.fn_index,time_limit:l,type:o,show_progress:this.show_progress[i.fn_index]};});}set_status(i,t){this.current[i].status=t;}resolve_args(i){const{fn_index:t,status:n,size:u=void 0,position:v=null,eta:r=null,message:d=null,stream_state:e=null,time_limit:p=null,progress_data:g=null}=i,l=this.fn_outputs[t],o=this.fn_status[t],c=this.fn_inputs[t];return l.concat(c).map(h=>{let m;const _=this.pending_outputs.get(h)||0;if(o==="pending"&&n!=="pending"){let w=_-1;this.pending_outputs.set(h,w<0?0:w),m=w>0?"pending":n;}else o==="pending"&&n==="pending"?m="pending":o!=="pending"&&n==="pending"?(m="pending",this.pending_outputs.set(h,_+1)):m=n;const k=c.includes(h)&&e?"input":l.includes(h)?"output":"skip";return {id:h,queue_position:v,queue_size:u,eta:r,status:m,message:d,progress:g,stream_state:e,time_limit:p,type:k}}).filter(h=>h.type!=="skip")}};

var f$1=Object.prototype.hasOwnProperty;function s$1(t,e,r){for(r of t.keys())if(u$1(r,e))return r}function u$1(t,e){var r,i,n;if(t===e)return  true;if(t&&e&&(r=t.constructor)===e.constructor){if(r===Date)return t.getTime()===e.getTime();if(r===RegExp)return t.toString()===e.toString();if(r===Array){if((i=t.length)===e.length)for(;i--&&u$1(t[i],e[i]););return i===-1}if(r===Set){if(t.size!==e.size)return  false;for(i of t)if(n=i,n&&typeof n=="object"&&(n=s$1(e,n),!n)||!e.has(n))return  false;return  true}if(r===Map){if(t.size!==e.size)return  false;for(i of t)if(n=i[0],n&&typeof n=="object"&&(n=s$1(e,n),!n)||!u$1(i[1],e.get(n)))return  false;return  true}if(r===ArrayBuffer)t=new Uint8Array(t),e=new Uint8Array(e);else if(r===DataView){if((i=t.byteLength)===e.byteLength)for(;i--&&t.getInt8(i)===e.getInt8(i););return i===-1}if(ArrayBuffer.isView(t)){if((i=t.byteLength)===e.byteLength)for(;i--&&t[i]===e[i];);return i===-1}if(!r||typeof t=="object"){i=0;for(r in t)if(f$1.call(t,r)&&++i&&!f$1.call(e,r)||!(r in e)||!u$1(t[r],e[r]))return  false;return Object.keys(e).length===i}}return t!==t&&e!==e}

const R={walkthrough:"tabs",walkthroughstep:"tabitem"};let G$1 = class G{#s;#t;#e;reactive_formatter=e=>e;#r;client;root;root_untracked;#o=new Set;#p=new Set;#c=[];#n=new Map;#i=new Map;#a;component_ids;initial_tabs={};components_to_register=new Set;ready;ready_resolve;resolved=false;#l=new Set;constructor(e,t,i,s,o,p,n){this.ready=new Promise(l=>{this.ready_resolve=l;}),this.reactive_formatter=p,this.#r={...s,api_url:new URL(s.api_prefix,s.root).toString()},this.#s=e,this.#t=t,this.#e=i,this.root=this.create_node({id:t.id,children:[]},new Map,true);for(const l of e)l.props.visible!=false&&this.components_to_register.add(l.id);this.client=o,this.prepare();const a=e.reduce((l,c)=>(l.set(c.id,c),l),new Map);this.root.children=this.#t.children.map(l=>this.traverse(l,c=>this.create_node(c,a,false,this.reactive_formatter))),this.component_ids=e.map(l=>l.id),this.initial_tabs={},f(this.root,this.initial_tabs),this.postprocess(this.root),this.#a=n,this.root_untracked=this.root;}reload(e,t,i,s){this.#t=t,this.#s=e,this.#r={...s,api_url:new URL(s.api_prefix,s.root).toString()},this.#e=i,this.root=this.create_node({id:t.id,children:[]},new Map,true);for(const p of e)p.props.visible!=false&&this.components_to_register.add(p.id);this.prepare();const o=e.reduce((p,n)=>(p.set(n.id,n),p),new Map);this.root.children=this.#t.children.map(p=>this.traverse(p,n=>this.create_node(n,o,false,this.reactive_formatter))),this.component_ids=e.map(p=>p.id),this.initial_tabs={},f(this.root,this.initial_tabs),this.postprocess(this.root);}register_component(e,t,i){this.#i.set(e,t),this.#n.set(e,i),this.components_to_register.delete(e),this.components_to_register.size===0&&!this.resolved&&(this.resolved=true,this.ready_resolve());}prepare(){const[e,t]=ds(this.#e);this.#o=e,this.#p=t;}process(){}postprocess(e){this.root=this.traverse(e,[t=>h$1(t,this.#r.api_url),t=>U$1(t,this.components_to_register),t=>z(t,this.components_to_register),t=>B$2(t),t=>g$1(t,this.initial_tabs),t=>this.find_attached_events(t,this.#e),t=>q(t,this.components_to_register,this.#l)]);}find_attached_events(e,t){const i=t.filter(s=>s.targets.find(([o])=>o===e.id)).map(s=>{const o=s.targets.find(([p])=>p===e.id);return o?o[1]:null}).filter(Boolean);return e.props.shared_props.attached_events=i,e}traverse(e,t){function i(s,o,p){const n=o(s);return "children"in s&&s.children.length>0&&(n.children=s.children?.map(a=>p(a,o))||[]),n}if(Array.isArray(t)){let s=e;for(const o of t)s=i(s,o,this.traverse.bind(this));return s}else return i(e,t,this.traverse.bind(this))}create_node(e,t,i=false,s){let o;if(i?o={type:"column",id:e.id,props:{visible:true,root:"",theme_mode:"light"},component_class_id:"column",key:null}:o=t.get(e.id),!o)throw new Error(`Component with ID ${e.id} not found`);s&&(o.props.i18n=s);const p=O(e.id,o.props,[this.#o,this.#p],this.client,this.#r.api_url,{...this.#r}),n=R[o.type]||o.type;return {id:e.id,type:n,props:p,children:[],show_progress_on:null,component_class_id:o.component_class_id||o.type,component:p.shared_props.visible!==false?ps(o.type,o.component_class_id,this.#r.api_url||""):null,key:o.key,rendered_in:o.rendered_in,documentation:o.documentation,original_visibility:p.shared_props.visible}}rerender(e,t){const i=e.reduce((n,a)=>(n.set(a.id,a),n),new Map),s=this.traverse(t,n=>this.create_node(n,i,false,this.reactive_formatter));f(s,this.initial_tabs);const o=this.traverse(s,n=>g$1(n,this.initial_tabs)),p=_(this.root,o.id);if(!p)throw new Error("Rerender failed: root node not found in current tree");p.children=o.children;}async update_visibility(e,t){e.children.forEach(i=>{const s=this.#i.get(i.id);s&&s(t),this.update_visibility(i,t);});}async update_state(e,t,i=true){const s=_(this.root,e);let o=false;i&&!s?.component&&(await tick(),this.root=this.traverse(this.root,[a=>P$1(a,e,t.visible),a=>y$1(a,e,t.visible),a=>h$1(a,this.#r.api_url)]),await tick(),o=true);const p=this.#i.get(e);if(p)p&&p(t);else {const a=s?.props.props.value,l=E$1(t);s.props.shared_props={...s?.props.shared_props,...l.shared_props},s.props.props={...s?.props.props,...l.props},"value"in t&&!u$1(a,t.value)&&this.#a(e,"change",null);}if(!i||o)return;await tick(),await this.update_visibility(s,t);const n=S$1(this.root,e);n&&y$1(n,e,t.visible);}async get_state(e){const t=this.#n.get(e),i=_(this.root,e);return !t&&!i?null:t?await t():i?Promise.resolve({value:i.props.props.value}):null}async render_previously_invisible_children(e){this.root=this.traverse(this.root,[t=>(t.id===e&&k(t,this.#l),t),t=>h$1(t,this.#r.api_url)]);}};function k(r,e){r.props.shared_props.visible=e.has(r.id)?true:r.props.shared_props.visible,r.children.forEach(t=>{k(t,e);});}function L(r,e,t){return e?e.reduce((i,s)=>(i[s]=async(...o)=>(o.length===1&&(o=o[0]),await t.component_server(r,s,o)),i),{}):{}}function E$1(r){const e={},t={};for(const i in r)if(i==="id"||i==="autoscroll")t[i]=r[i];else if(f$2.includes(i)){const s=i;e[s]=r[i];}else t[i]=r[i];return {shared_props:e,props:t}}function O(r,e,t,i,s,o={}){const{shared_props:p,props:n}=E$1(e);p.server=L(r,e.server_fns,i);for(const a in o)if(f$2.includes(a)){const l=a;p[l]=o[a];}else n[a]=o[a];return p.client=i,p.id=r,p.interactive=ms(r,p.interactive,n.value,t),p.load_component=(a,l)=>ps(a,"",s,l),p.visible=p.visible===void 0?true:p.visible,p.loading_status={},{shared_props:p,props:n}}function h$1(r,e){if(r.props.shared_props.visible&&!r.component){const t={...r,component:ps(r.type,r.component_class_id,e),children:[]};return r.children&&(t.children=r.children.map(i=>h$1(i,e))),t}else return r}function P$1(r,e,t){return r.id==e&&(r.props.shared_props.visible=t),r}function u(r,e){e.delete(r.id),r.children&&r.children.forEach(t=>u(t,e));}function U$1(r,e){return r.props.shared_props.visible!==true&&u(r,e),r}function v$1(r,e){return r.props.shared_props.visible===true&&(e.add(r.id),r.props.shared_props.visible=false),r.children.forEach(t=>{v$1(t,e);}),r}function q(r,e,t){return r.type==="accordion"&&r.props.props.open===false&&(u(r,e),r.children&&r.children.forEach(i=>{v$1(i,t);})),r.type==="tabs"&&r.children.forEach(i=>{i.type==="tabitem"&&i.props.props.id!==(r.props.props.selected||r.props.props.initial_tabs[0].id)&&(u(i,e),v$1(i,t));}),r}function z(r,e){return r.type==="form"&&r.children.every(i=>i.props.shared_props.visible===false)&&(r.props.shared_props.visible=false,e.delete(r.id)),r}function y$1(r,e,t){return r.type==="form"&&r.children.length&&r.children.some(i=>i.id===e)&&(t===true?r.props.shared_props.visible=true:!t&&r.children.length===1&&(r.props.shared_props.visible="hidden")),r}function B$2(r){const e=["description","info","title","placeholder","value","label"];for(const t of Object.keys(r.props.shared_props))e.includes(t)&&(r.props.shared_props[t]=ys(r.props.shared_props[t]));for(const t of Object.keys(r.props.props))e.includes(t)&&(r.props.props[t]=ys(r.props.props[t]));return r}function g$1(r,e){if(r.type==="tabs"&&r.id in e){const t=e[r.id].sort((i,s)=>i.order-s.order);r.props.props.initial_tabs=t;}else r.type==="tabitem"&&(r.props.props.component_id=r.id);return r}function M$1(r,e,t,i){t!==null&&r.type==="tabitem"&&(t in e||(e[t]=[]),"id"in r.props.props||(r.props.props.id=r.id),e[t].push({label:r.props.shared_props.label,id:r.props.props.id,elem_id:r.props.shared_props.elem_id,visible:r.props.shared_props.visible,interactive:r.props.shared_props.interactive,scale:r.props.shared_props.scale||null,component_id:r.id}),r.props.props.order=i),r.children&&r.children.forEach((s,o)=>{M$1(s,e,r.type==="tabs"?r.id:null,r.type==="tabs"?o:null);});}function f(r,e){function t(i){"children"in i&&i.children.length>0&&i.children?.forEach(s=>M$1(s,e,i.type==="tabs"?i.id:null,null));}return t(r)}function _(r,e){if(r.id===e)return r;if(r.children)for(const t of r.children){const i=_(t,e);if(i)return i}return null}function S$1(r,e){if(r.children)for(const t of r.children){if(t.id===e)return r;const i=S$1(t,e);if(i)return i}return null}

function o$1(t,l){let{visible:a,scale:e,min_width:s$1,label:d=void 0}=l;t.push(`<div${attr_class("form svelte-d5xbca",void 0,{hidden:a===false,"hidden-css":a==="hidden"})}${attr("role",d?"group":void 0)}${attr("aria-label",d)}${attr_style("",{"flex-grow":e,"min-width":`calc(min(${s$1}px, 100%))`})}><!--[-->`),slot(t,l,"default",{},null),t.push("<!--]--></div>");}

function d(n){return Ze(n)}const g=["!--","!doctype","a","abbr","acronym","address","applet","area","article","aside","audio","b","base","basefont","bdi","bdo","big","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","data","datalist","dd","del","details","dfn","dialog","dir","div","dl","dt","em","embed","fieldset","figcaption","figure","font","footer","form","frame","frameset","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","iframe","img","input","ins","kbd","label","legend","li","link","main","map","mark","menu","meta","meter","nav","noframes","noscript","object","ol","optgroup","option","output","p","param","picture","pre","progress","q","rp","rt","ruby","s","samp","script","search","section","select","small","source","span","strike","strong","style","sub","summary","sup","svg","table","tbody","td","template","textarea","tfoot","th","thead","time","title","tr","track","tt","u","ul","var","video","wbr"],B$1=["g","defs","use","symbol","rect","circle","ellipse","line","polyline","polygon","path","image","text","tspan","textPath","linearGradient","radialGradient","stop","pattern","clipPath","mask","filter","feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feGaussianBlur","feMerge","feMorphology","feOffset","feSpecularLighting","feTurbulence","feMergeNode","feFuncR","feFuncG","feFuncB","feFuncA","feDistantLight","fePointLight","feSpotLight","feFlood","feTile","animate","animateTransform","animateMotion","mpath","set","view","cursor","foreignObject","desc","title","metadata","switch"],E=[...g,...B$1.filter(n=>!g.includes(n))];function P(n,u){n.component(h=>{let{chatbot:b=true,message:o,sanitize_html:_=true,latex_delimiters:l=[],render_markdown:p=true,line_breaks:x=true,header_links:k=false,allow_tags:c=false,theme_mode:R="system"}=u;const y=vt({header_links:k,line_breaks:x,latex_delimiters:l||[]});let v=o&&o.trim()?L(o):"";function f(a){return a.replace(/[.*+?^${}()|[\]\\]/g,"\\$&")}function w(a,e){if(e===true){const s=/<\/?([a-zA-Z][a-zA-Z0-9-]*)([\s>])/g;return a.replace(s,(t,r,i)=>E.includes(r.toLowerCase())?t:t.replace(/</g,"&lt;").replace(/>/g,"&gt;"))}if(Array.isArray(e)){const s=e.map(r=>({open:new RegExp(`<(${r})(\\s+[^>]*)?>`,"gi"),close:new RegExp(`</(${r})>`,"gi")}));let t=a;return s.forEach(r=>{t=t.replace(r.open,i=>i.replace(/</g,"&lt;").replace(/>/g,"&gt;")),t=t.replace(r.close,i=>i.replace(/</g,"&lt;").replace(/>/g,"&gt;"));}),t}return a}function L(a){let e=a;if(p){const s=[];l.forEach((t,r)=>{const i=f(t.left),$=f(t.right),C=new RegExp(`${i}([\\s\\S]+?)${$}`,"g");e=e.replace(C,(M,z)=>(s.push(M),`%%%LATEX_BLOCK_${s.length-1}%%%`));}),e=y.parse(e),e=e.replace(/%%%LATEX_BLOCK_(\d+)%%%/g,(t,r)=>s[parseInt(r,10)]);}return c&&(e=w(e,c)),_&&d&&(e=d(e)),e}h.push(`<span${attr_class("md svelte-1hf8a14",void 0,{chatbot:b,prose:p})}>${html(v)}</span>`);});}

/* empty css                                        */function n(o,i){let s$1=i.info;o.push('<div class="svelte-9hc4ua">'),P(o,{message:s$1,sanitize_html:true}),o.push("<!----></div>"),bind_props(i,{info:s$1});}

/* empty css                                        */function c$1(l,a){let i=fallback(a.show_label,true),s$1=fallback(a.info,void 0),o=fallback(a.rtl,false);l.push(`<span data-testid="block-info"${attr("dir",o?"rtl":"ltr")}${attr_class("svelte-jdcl7l",void 0,{hide:!i,"has-info":s$1!=null,"sr-only":!i})}><!--[-->`),slot(l,a,"default",{},null),l.push("<!--]--></span> "),s$1?(l.push("<!--[-->"),n(l,{info:s$1})):l.push("<!--[!-->"),l.push("<!--]-->"),bind_props(a,{show_label:i,info:s$1,rtl:o});}

/* empty css                                        */function w(l,u){let{Icon:h,label:s$1="",show_label:b=false,pending:e=false,size:t="small",padded:n=true,highlight:p=false,disabled:o=false,hasPopup:m=false,color:d="var(--block-label-text-color)",transparent:f=false,background:g="var(--block-background-fill)",border:r="transparent",onclick:v,children:i}=u,c=p?"var(--color-accent)":d;l.push(`<button${attr_class("icon-button svelte-3jwzs9",void 0,{pending:e,padded:n,highlight:p,transparent:f})}${attr("disabled",o,true)}${attr("aria-label",s$1)}${attr("aria-haspopup",m)}${attr("title",s$1)}${attr_style("",{"--border-color":r,color:!o&&c?c:"var(--block-label-text-color)","--bg-color":o?"auto":g})}>`),b?(l.push("<!--[-->"),l.push(`<span class="svelte-3jwzs9">${escape_html(s$1)}</span>`)):l.push("<!--[!-->"),l.push(`<!--]--> <div${attr_class("svelte-3jwzs9",void 0,{"x-small":t==="x-small",small:t==="small",large:t==="large",medium:t==="medium"})}><!---->`),h(l,{}),l.push("<!----> "),i?(l.push("<!--[-->"),i(l),l.push("<!---->")):l.push("<!--[!-->"),l.push("<!--]--></div></button>");}

function e(o){o.push('<svg width="100%" height="100%" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentColor"><path d="M5 13L9 17L19 7" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>');}

function h(r){r.push('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 33 33" color="currentColor" aria-hidden="true" width="100%" height="100%"><path fill="currentColor" d="M28 10v18H10V10h18m0-2H10a2 2 0 0 0-2 2v18a2 2 0 0 0 2 2h18a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2Z"></path><path fill="currentColor" d="M4 18H2V4a2 2 0 0 1 2-2h14v2H4Z"></path></svg>');}

function M(L){L.push('<svg viewBox="0 0 22 24" width="100%" height="100%" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M19.1168 12.1484C19.474 12.3581 19.9336 12.2384 20.1432 11.8811C20.3528 11.5238 20.2331 11.0643 19.8758 10.8547L19.1168 12.1484ZM6.94331 4.13656L6.55624 4.77902L6.56378 4.78344L6.94331 4.13656ZM5.92408 4.1598L5.50816 3.5357L5.50816 3.5357L5.92408 4.1598ZM5.51031 5.09156L4.76841 5.20151C4.77575 5.25101 4.78802 5.29965 4.80505 5.34671L5.51031 5.09156ZM7.12405 11.7567C7.26496 12.1462 7.69495 12.3477 8.08446 12.2068C8.47397 12.0659 8.67549 11.6359 8.53458 11.2464L7.12405 11.7567ZM19.8758 12.1484C20.2331 11.9388 20.3528 11.4793 20.1432 11.122C19.9336 10.7648 19.474 10.6451 19.1168 10.8547L19.8758 12.1484ZM6.94331 18.8666L6.56375 18.2196L6.55627 18.2241L6.94331 18.8666ZM5.92408 18.8433L5.50815 19.4674H5.50815L5.92408 18.8433ZM5.51031 17.9116L4.80505 17.6564C4.78802 17.7035 4.77575 17.7521 4.76841 17.8016L5.51031 17.9116ZM8.53458 11.7567C8.67549 11.3672 8.47397 10.9372 8.08446 10.7963C7.69495 10.6554 7.26496 10.8569 7.12405 11.2464L8.53458 11.7567ZM19.4963 12.2516C19.9105 12.2516 20.2463 11.9158 20.2463 11.5016C20.2463 11.0873 19.9105 10.7516 19.4963 10.7516V12.2516ZM7.82931 10.7516C7.4151 10.7516 7.07931 11.0873 7.07931 11.5016C7.07931 11.9158 7.4151 12.2516 7.82931 12.2516V10.7516ZM19.8758 10.8547L7.32284 3.48968L6.56378 4.78344L19.1168 12.1484L19.8758 10.8547ZM7.33035 3.49414C6.76609 3.15419 6.05633 3.17038 5.50816 3.5357L6.34 4.78391C6.40506 4.74055 6.4893 4.73863 6.55627 4.77898L7.33035 3.49414ZM5.50816 3.5357C4.95998 3.90102 4.67184 4.54987 4.76841 5.20151L6.25221 4.98161C6.24075 4.90427 6.27494 4.82727 6.34 4.78391L5.50816 3.5357ZM4.80505 5.34671L7.12405 11.7567L8.53458 11.2464L6.21558 4.83641L4.80505 5.34671ZM19.1168 10.8547L6.56378 18.2197L7.32284 19.5134L19.8758 12.1484L19.1168 10.8547ZM6.55627 18.2241C6.4893 18.2645 6.40506 18.2626 6.34 18.2192L5.50815 19.4674C6.05633 19.8327 6.76609 19.8489 7.33035 19.509L6.55627 18.2241ZM6.34 18.2192C6.27494 18.1759 6.24075 18.0988 6.25221 18.0215L4.76841 17.8016C4.67184 18.4532 4.95998 19.1021 5.50815 19.4674L6.34 18.2192ZM6.21558 18.1667L8.53458 11.7567L7.12405 11.2464L4.80505 17.6564L6.21558 18.1667ZM19.4963 10.7516H7.82931V12.2516H19.4963V10.7516Z" fill="currentColor"></path></g></svg>');}

function s(i,r){let e=fallback(r.fill,"currentColor"),o=fallback(r.stroke_width,1.5);i.push(`<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 24 24"${attr("fill",e)} stroke="currentColor"${attr("stroke-width",`${o}`)} stroke-linecap="round" stroke-linejoin="round" class="feather feather-square"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect></svg>`),bind_props(r,{fill:e,stroke_width:o});}

/* empty css                                        */function v(l,u){l.component(t=>{let o=u.button,p=u.on_click;t.push(`<button class="custom-button svelte-gnx6f7"${attr("title",o.value||"")}${attr("aria-label",o.value||"Custom action")}>`),o.value?(t.push("<!--[-->"),t.push(`<span class="custom-button-label svelte-gnx6f7">${escape_html(o.value)}</span>`)):t.push("<!--[!-->"),t.push("<!--]--></button>"),bind_props(u,{button:o,on_click:p});});}function y(l,u){l.component(t=>{let{top_panel:o=true,display_top_corner:p=false,show_background:_=true,buttons:n=null,on_custom_button_click:c=null,children:i}=u;if(t.push(`<div${attr_class(`icon-button-wrapper ${o?"top-panel":""} ${p?"display-top-corner":"hide-top-corner"} ${_?"":"no-background"}`,"svelte-1pnho82")}>`),i?(t.push("<!--[-->"),i(t),t.push("<!---->")):t.push("<!--[!-->"),t.push("<!--]--> "),n){t.push("<!--[-->"),t.push("<!--[-->");const h=ensure_array_like(n);for(let a=0,f=h.length;a<f;a++){let b=h[a];typeof b!="string"?(t.push("<!--[-->"),v(t,{button:b,on_click:m=>{c&&c(m);}})):t.push("<!--[!-->"),t.push("<!--]-->");}t.push("<!--]-->");}else t.push("<!--[!-->");t.push("<!--]--></div>");});}

/* empty css                                     */function pt(y$1,v){y$1.component(a=>{let{value:s$1="",value_is_output:w$1=false,lines:k=1,placeholder:p="",label:z,info:C=void 0,disabled:c=false,show_label:d=true,container:T=true,max_lines:J=void 0,type:r="text",buttons:h$1=null,oncustombuttonclick:K=null,submit_btn:i=null,stop_btn:e$1=null,rtl:g=false,autofocus:n=false,text_align:b=void 0,autoscroll:L=true,max_length:m=void 0,html_attributes:o=null,validation_error:u=void 0,onchange:M$1,onsubmit:N,onstop:O,onblur:P,onselect:Q,oninput:R,onfocus:U,oncopy:I}=v,f=false,x,B=1;const S=!i;async function q(){"clipboard"in navigator&&(await navigator.clipboard.writeText(s$1),I?.({value:s$1}),W());}function W(){f=true,x&&clearTimeout(x),x=setTimeout(()=>{f=false;},1e3);}if(a.push(`<label${attr_class("svelte-1hguek3",void 0,{container:T,show_textbox_border:S})}>`),d&&h$1&&h$1.length>0?(a.push("<!--[-->"),y(a,{buttons:h$1,children:l=>{h$1.some(_=>typeof _=="string"&&_==="copy")?(l.push("<!--[-->"),w(l,{Icon:f?e:h,onclick:q,label:f?"Copied":"Copy"})):l.push("<!--[!-->"),l.push("<!--]-->");}})):a.push("<!--[!-->"),a.push("<!--]--> "),c$1(a,{show_label:u?true:d,info:C,children:l=>{l.push(`<!---->${escape_html(z)} `),u?(l.push("<!--[-->"),l.push(`<div class="validation-error svelte-1hguek3">${escape_html(u)}</div>`)):l.push("<!--[!-->"),l.push("<!--]-->");},$$slots:{default:true}}),a.push('<!----> <div class="input-container svelte-1hguek3">'),k===1&&B===1)a.push("<!--[-->"),r==="text"?(a.push("<!--[-->"),a.push(`<input data-testid="textbox" type="text"${attr_class("scroll-hide svelte-1hguek3",void 0,{"validation-error":u})}${attr("dir",g?"rtl":"ltr")}${attr("value",s$1)}${attr("placeholder",p)}${attr("disabled",c,true)}${attr("autofocus",n,true)}${attr("maxlength",m)}${attr_style(b?"text-align: "+b:"")}${attr("autocapitalize",o?.autocapitalize)}${attr("autocorrect",o?.autocorrect)}${attr("spellcheck",o?.spellcheck)}${attr("autocomplete",o?.autocomplete)}${attr("tabindex",o?.tabindex)}${attr("enterkeyhint",o?.enterkeyhint)}${attr("lang",o?.lang)}/>`)):(a.push("<!--[!-->"),r==="password"?(a.push("<!--[-->"),a.push(`<input data-testid="password" type="password"${attr_class("scroll-hide svelte-1hguek3",void 0,{"validation-error":u})}${attr("value",s$1)}${attr("placeholder",p)}${attr("disabled",c,true)}${attr("autofocus",n,true)}${attr("maxlength",m)} autocomplete=""${attr("autocapitalize",o?.autocapitalize)}${attr("autocorrect",o?.autocorrect)}${attr("spellcheck",o?.spellcheck)}${attr("tabindex",o?.tabindex)}${attr("enterkeyhint",o?.enterkeyhint)}${attr("lang",o?.lang)}/>`)):(a.push("<!--[!-->"),r==="email"?(a.push("<!--[-->"),a.push(`<input data-testid="textbox" type="email"${attr_class("scroll-hide svelte-1hguek3",void 0,{"validation-error":u})}${attr("value",s$1)}${attr("placeholder",p)}${attr("disabled",c,true)}${attr("autofocus",n,true)}${attr("maxlength",m)} autocomplete="email"${attr("autocapitalize",o?.autocapitalize)}${attr("autocorrect",o?.autocorrect)}${attr("spellcheck",o?.spellcheck)}${attr("tabindex",o?.tabindex)}${attr("enterkeyhint",o?.enterkeyhint)}${attr("lang",o?.lang)}/>`)):a.push("<!--[!-->"),a.push("<!--]-->")),a.push("<!--]-->")),a.push("<!--]-->");else {a.push("<!--[!-->"),a.push(`<textarea data-testid="textbox"${attr("dir",g?"rtl":"ltr")}${attr("placeholder",p)}${attr("rows",k)}${attr("disabled",c,true)}${attr("autofocus",n,true)}${attr("maxlength",m)}${attr_style(b?"text-align: "+b:"")}${attr("autocapitalize",o?.autocapitalize)}${attr("autocorrect",o?.autocorrect)}${attr("spellcheck",o?.spellcheck)}${attr("autocomplete",o?.autocomplete)}${attr("tabindex",o?.tabindex)}${attr("enterkeyhint",o?.enterkeyhint)}${attr("lang",o?.lang)}${attr_class("svelte-1hguek3",void 0,{"no-label":!d&&(i||e$1),"validation-error":u})}>`);const l=escape_html(s$1);l&&a.push(`${l}`),a.push("</textarea>");}a.push("<!--]--> "),i?(a.push("<!--[-->"),a.push(`<button${attr_class("submit-button svelte-1hguek3",void 0,{"padded-button":i!==true})}>`),i===true?(a.push("<!--[-->"),M(a)):(a.push("<!--[!-->"),a.push(`${escape_html(i)}`)),a.push("<!--]--></button>")):a.push("<!--[!-->"),a.push("<!--]--> "),e$1?(a.push("<!--[-->"),a.push(`<button${attr_class("stop-button svelte-1hguek3",void 0,{"padded-button":e$1!==true})}>`),e$1===true?(a.push("<!--[-->"),s(a,{fill:"none",stroke_width:2.5})):(a.push("<!--[!-->"),a.push(`${escape_html(e$1)}`)),a.push("<!--]--></button>")):a.push("<!--[!-->"),a.push("<!--]--></div></label>"),bind_props(v,{value:s$1,value_is_output:w$1});});}

/* empty css                                        */function G(q,e){q.component(t=>{let b=fallback(e.height,void 0),w=fallback(e.min_height,void 0),k=fallback(e.max_height,void 0),d=fallback(e.width,void 0),g=fallback(e.elem_id,""),x=fallback(e.elem_classes,()=>[],true),m=fallback(e.variant,"solid"),h=fallback(e.border_mode,"base"),_=fallback(e.padding,true),y=fallback(e.type,"normal"),v=fallback(e.test_id,void 0),r=fallback(e.explicit_call,false),p=fallback(e.container,true),n=fallback(e.visible,true),B=fallback(e.allow_overflow,true),z=fallback(e.overflow_behavior,"auto"),c=fallback(e.scale,null),E=fallback(e.min_width,0),u=fallback(e.flex,false),L=fallback(e.resizable,false),R=fallback(e.rtl,false),a=fallback(e.fullscreen,false),j=fallback(e.label,void 0),C=a,o,A=y==="fieldset"?"fieldset":"div",H=0,K=0,i=null;function W(f){a&&f.key==="Escape"&&(a=false);}const s$1=f=>{if(f!==void 0){if(typeof f=="number")return f+"px";if(typeof f=="string")return f}};a!==C&&(C=a,a?(i=o.getBoundingClientRect(),H=o.offsetHeight,K=o.offsetWidth,window.addEventListener("keydown",W)):(i=null,window.removeEventListener("keydown",W))),n||(u=false),n===true||n==="hidden"?(t.push("<!--[-->"),element(t,A,()=>{t.push(`${attr("data-testid",v)}${attr("id",g)}${attr_class(`block ${stringify(x?.join(" ")||"")}`,"svelte-1plpy97",{hidden:n==="hidden",padded:_,flex:u,border_focus:h==="focus",border_contrast:h==="contrast","hide-container":!r&&!p,fullscreen:a,animating:a&&i!==null,"auto-margin":c===null})}${attr("dir",R?"rtl":"ltr")}${attr("aria-label",j)}${attr_style("",{height:a?void 0:s$1(b),"min-height":a?void 0:s$1(w),"max-height":a?void 0:s$1(k),"--start-top":i?`${i.top}px`:"0px","--start-left":i?`${i.left}px`:"0px","--start-width":i?`${i.width}px`:"0px","--start-height":i?`${i.height}px`:"0px",width:a?void 0:typeof d=="number"?`calc(min(${d}px, 100%))`:s$1(d),"border-style":m,overflow:B?z:"hidden","flex-grow":c,"min-width":`calc(min(${E}px, 100%))`,"border-width":"var(--block-border-width)"})}`);},()=>{t.push("<!--[-->"),slot(t,e,"default",{},null),t.push("<!--]--> "),L?(t.push("<!--[-->"),t.push('<svg class="resize-handle svelte-1plpy97" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><line x1="1" y1="9" x2="9" y2="1" stroke="gray" stroke-width="0.5" class="svelte-1plpy97"></line><line x1="5" y1="9" x2="9" y2="5" stroke="gray" stroke-width="0.5" class="svelte-1plpy97"></line></svg>')):t.push("<!--[!-->"),t.push("<!--]-->");}),t.push(" "),a?(t.push("<!--[-->"),t.push(`<div class="placeholder svelte-1plpy97"${attr_style("",{height:H+"px",width:K+"px"})}></div>`)):t.push("<!--[!-->"),t.push("<!--]-->")):t.push("<!--[!-->"),t.push("<!--]-->"),bind_props(e,{height:b,min_height:w,max_height:k,width:d,elem_id:g,elem_classes:x,variant:m,border_mode:h,padding:_,type:y,test_id:v,explicit_call:r,container:p,visible:n,allow_overflow:B,overflow_behavior:z,scale:c,min_width:E,flex:u,resizable:L,rtl:R,fullscreen:a,label:j});});}

/* empty css                                   */function c(e,s$1){e.component(o=>{let{src:a,restProps:r,data_testid:i,class_names:n}=s$1;o.push(`<img${attributes({src:a,class:clsx((n||[]).join(" ")),"data-testid":i,...r},"svelte-1jk6tax")} onload="this.__e=event" onerror="this.__e=event"/>`);});}

/* empty css                                          */function B(_,d){_.component(t=>{let{elem_id:f,elem_classes:c$1=[],visible:s$1,variant:m,size:g,value:u,link:h,link_target:b,icon:l,disabled:a,scale:o,min_width:p,onclick:w=()=>{},children:n}=d;h&&h.length>0?(t.push("<!--[-->"),t.push(`<a${attr("href",h)}${attr("target",b)}${attr("rel",b==="_blank"?"noopener noreferrer":void 0)}${attr("aria-disabled",a)}${attr_class(`${stringify(g)} ${stringify(m)} ${stringify(c$1.join(" "))}`,"svelte-xzq5jh",{hidden:s$1===false||s$1==="hidden",disabled:a})}${attr("id",f)}${attr_style("",{"flex-grow":o,"pointer-events":a?"none":null,width:o===0?"fit-content":null,"min-width":typeof p=="number"?`calc(min(${p}px, 100%))`:null})}>`),l?(t.push("<!--[-->"),c(t,{src:l.url,restProps:{alt:`${u} icon`,class:"button-icon"}})):t.push("<!--[!-->"),t.push("<!--]--> "),n?(t.push("<!--[-->"),n(t),t.push("<!---->")):t.push("<!--[!-->"),t.push("<!--]--></a>")):(t.push("<!--[!-->"),t.push(`<button${attr_class(`${stringify(g)} ${stringify(m)} ${stringify(c$1.join(" "))}`,"svelte-xzq5jh",{hidden:s$1===false||s$1==="hidden"})}${attr("id",f)}${attr("disabled",a,true)}${attr_style("",{"flex-grow":o,width:o===0?"fit-content":null,"min-width":typeof p=="number"?`calc(min(${p}px, 100%))`:null})}>`),l?(t.push("<!--[-->"),c(t,{restProps:{alt:`${u} icon`},class_names:[`button-icon ${u?"right-padded":""}`],src:l.url})):t.push("<!--[!-->"),t.push("<!--]--> "),n?(t.push("<!--[-->"),n(t),t.push("<!---->")):t.push("<!--[!-->"),t.push("<!--]--></button>")),t.push("<!--]-->");});}

function o(e){e.push('<svg width="100%" height="100%" viewBox="0 0 24 24" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" stroke="currentColor" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;"><g transform="matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"><path d="M18,6L6.087,17.913" style="fill:none;fill-rule:nonzero;stroke-width:2px;"></path></g><path d="M4.364,4.364L19.636,19.636" style="fill:none;fill-rule:nonzero;stroke-width:2px;"></path></svg>');}

function S(e,n){e.component(s$1=>{var a;let y=fallback(n.margin,true);const u=spring([0,0]),h=spring([0,0]);s$1.push(`<div${attr_class("svelte-1vhirvf",void 0,{margin:y})}><svg viewBox="-1200 -1200 3000 3000" fill="none" xmlns="http://www.w3.org/2000/svg" class="svelte-1vhirvf"><g${attr_style(`transform: translate(${stringify(store_get(a??={},"$top",u)[0])}px, ${stringify(store_get(a??={},"$top",u)[1])}px);`)}><path d="M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z" fill="#FF7C00" fill-opacity="0.4" class="svelte-1vhirvf"></path><path d="M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z" fill="#FF7C00" class="svelte-1vhirvf"></path><path d="M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z" fill="#FF7C00" fill-opacity="0.4" class="svelte-1vhirvf"></path><path d="M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z" fill="#FF7C00" class="svelte-1vhirvf"></path></g><g${attr_style(`transform: translate(${stringify(store_get(a??={},"$bottom",h)[0])}px, ${stringify(store_get(a??={},"$bottom",h)[1])}px);`)}><path d="M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z" fill="#FF7C00" fill-opacity="0.4" class="svelte-1vhirvf"></path><path d="M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z" fill="#FF7C00" class="svelte-1vhirvf"></path><path d="M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z" fill="#FF7C00" fill-opacity="0.4" class="svelte-1vhirvf"></path><path d="M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z" fill="#FF7C00" class="svelte-1vhirvf"></path></g></svg></div>`),a&&unsubscribe_stores(a),bind_props(n,{margin:y});});}function F(e){let n=["","k","M","G","T","P","E","Z"],s=0;for(;e>1e3&&s<n.length-1;)e/=1e3,s++;let a=n[s];return (Number.isInteger(e)?e:e.toFixed(1))+a}function U(e,n){e.component(s$1=>{let{i18n:a,eta:y=null,queue_position:u,queue_size:h,status:o$1,scroll_to_output:L=false,timer:b=true,show_progress:c="full",message:E=null,progress:v=null,variant:_="default",loading_text:d="Loading...",absolute:w$1=true,translucent:k=false,border:M=false,autoscroll:G,validation_error:m=null,show_validation_error:x=true,type:Z=null,on_clear_status:N}=n,P=null;const I=Z==="input"||!o$1||o$1==="complete"||c==="hidden"||o$1=="streaming"||!!(x&&m),q=0 .toFixed(1);let z=v==null,f=(()=>{let p=null;v!=null?p=v.map(t=>{if(t.index!=null&&t.length!=null)return t.index/t.length;if(t.progress!=null)return t.progress}):p=null;let i,g="";return p?(i=p[p.length-1],i===0?g="0":g="150ms"):i=void 0,{progress_level:p,last_progress_level:i,progress_bar_transition:g}})();if(s$1.push(`<div${attr_class(`wrap ${stringify(_)} ${stringify(c)}`,"svelte-1uj8rng",{"no-click":m&&x,hide:I,translucent:_==="center"&&(o$1==="pending"||o$1==="error")||k||c==="minimal"||m,generating:o$1==="generating"&&c==="full",border:M})} data-testid="status-tracker"${attr_style("",{position:w$1?"absolute":"static",padding:w$1?"0":"var(--size-8) 0"})}>`),m&&x?(s$1.push("<!--[-->"),s$1.push(`<div class="validation-error svelte-1uj8rng">${escape_html(m)} <button class="svelte-1uj8rng">`),w(s$1,{Icon:o,label:a?a("common.clear"):"Clear",disabled:false,size:"x-small",background:"var(--background-fill-primary)",color:"var(--error-background-text)",border:"var(--border-color-primary)",onclick:()=>m=null}),s$1.push("<!----></button></div>")):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),o$1==="pending"){if(s$1.push("<!--[-->"),_==="default"&&z&&c==="full"?(s$1.push("<!--[-->"),s$1.push(`<div class="eta-bar svelte-1uj8rng"${attr_style("",{transform:`translateX(${stringify(-100)}%)`})}></div>`)):s$1.push("<!--[!-->"),s$1.push(`<!--]--> <div${attr_class("progress-text svelte-1uj8rng",void 0,{"meta-text-center":_==="center","meta-text":_==="default"})}>`),v){s$1.push("<!--[-->"),s$1.push("<!--[-->");const p=ensure_array_like(v);for(let i=0,g=p.length;i<g;i++){let t=p[i];t.index!=null?(s$1.push("<!--[-->"),t.length!=null?(s$1.push("<!--[-->"),s$1.push(`${escape_html(F(t.index||0))}/${escape_html(F(t.length))}`)):(s$1.push("<!--[!-->"),s$1.push(`${escape_html(F(t.index||0))}`)),s$1.push(`<!--]--> ${escape_html(t.unit)} |  `)):s$1.push("<!--[!-->"),s$1.push("<!--]-->");}s$1.push("<!--]-->");}else s$1.push("<!--[!-->"),u!==null&&h!==void 0&&u>=0?(s$1.push("<!--[-->"),s$1.push(`queue: ${escape_html(u+1)}/${escape_html(h)} |`)):(s$1.push("<!--[!-->"),u===0?(s$1.push("<!--[-->"),s$1.push("processing |")):s$1.push("<!--[!-->"),s$1.push("<!--]-->")),s$1.push("<!--]-->");if(s$1.push("<!--]--> "),b?(s$1.push("<!--[-->"),s$1.push(`${escape_html(q)}${escape_html(y?`/${P}`:"")}s`)):s$1.push("<!--[!-->"),s$1.push("<!--]--></div> "),f.last_progress_level!=null){if(s$1.push("<!--[-->"),s$1.push('<div class="progress-level svelte-1uj8rng"><div class="progress-level-inner svelte-1uj8rng">'),v!=null){s$1.push("<!--[-->"),s$1.push("<!--[-->");const p=ensure_array_like(v);for(let i=0,g=p.length;i<g;i++){let t=p[i];t.desc!=null||f.progress_level&&f.progress_level[i]!=null?(s$1.push("<!--[-->"),i!==0?(s$1.push("<!--[-->"),s$1.push(" /")):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),t.desc!=null?(s$1.push("<!--[-->"),s$1.push(`${escape_html(t.desc)}`)):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),t.desc!=null&&f.progress_level&&f.progress_level[i]!=null?(s$1.push("<!--[-->"),s$1.push("-")):s$1.push("<!--[!-->"),s$1.push("<!--]--> "),f.progress_level!=null?(s$1.push("<!--[-->"),s$1.push(`${escape_html((100*(f.progress_level[i]||0)).toFixed(1))}%`)):s$1.push("<!--[!-->"),s$1.push("<!--]-->")):s$1.push("<!--[!-->"),s$1.push("<!--]-->");}s$1.push("<!--]-->");}else s$1.push("<!--[!-->");s$1.push(`<!--]--></div> <div class="progress-bar-wrap svelte-1uj8rng"><div class="progress-bar svelte-1uj8rng"${attr_style("",{width:`${stringify(f.last_progress_level*100)}%`,transition:f.progress_bar_transition})}></div></div></div>`);}else s$1.push("<!--[!-->"),c==="full"?(s$1.push("<!--[-->"),S(s$1,{margin:_==="default"})):s$1.push("<!--[!-->"),s$1.push("<!--]-->");s$1.push("<!--]--> "),b?s$1.push("<!--[!-->"):(s$1.push("<!--[-->"),s$1.push(`<p class="loading svelte-1uj8rng">${escape_html(d)}</p> <!--[-->`),slot(s$1,n,"additional-loading-text",{},null),s$1.push("<!--]-->")),s$1.push("<!--]-->");}else s$1.push("<!--[!-->"),o$1==="error"?(s$1.push("<!--[-->"),s$1.push('<div class="clear-status svelte-1uj8rng">'),w(s$1,{Icon:o,label:a("common.clear"),disabled:false}),s$1.push(`<!----></div> <span class="error svelte-1uj8rng">${escape_html(a("common.error"))}</span> <!--[-->`),slot(s$1,n,"error",{},null),s$1.push("<!--]-->")):s$1.push("<!--[!-->"),s$1.push("<!--]-->");s$1.push("<!--]--></div>");});}

function b(e,a){e.component(s$1=>{let{$$slots:h,$$events:r,...t}=a,p=t.scale??null,m=t.min_width??0,n=t.elem_id??"",u=t.elem_classes??[],c=t.visible??true,o=t.variant??"default",i=t.loading_status;t.show_progress,s$1.push(`<div${attr("id",n)}${attr_class(`column ${stringify(u.join(" "))}`,"svelte-siq5d6",{compact:o==="compact",panel:o==="panel",hide:!c})}${attr_style("",{"flex-grow":p,"min-width":`calc(min(${stringify(m)}px, 100%))`})}>`),i&&i.show_progress?(s$1.push("<!--[-->"),U(s$1,spread_props([{autoscroll:t.autoscroll,i18n:t.i18n},i,{status:i?i.status=="pending"?"generating":i.status:null}]))):s$1.push("<!--[!-->"),s$1.push("<!--]--> <!--[-->"),slot(s$1,a,"default",{},null),s$1.push("<!--]--></div>");});}

function st(f,t){f.component(i=>{let{node:e}=t;var s$1,n=i.run([async()=>s$1=await e.component]);i.async_block([n[0]],c=>{e&&s$1?(c.push("<!--[-->"),c.async_block([n[0]],r=>{e.props.shared_props.visible?(r.push("<!--[-->"),r.async_block([n[0]],u=>{u.push("<!---->"),s$1.default?.(u,{shared_props:e.props.shared_props,props:e.props.props,children:g=>{g.async_block([n[0]],b=>{e.children&&e.children.length?(b.push("<!--[-->"),b.push("<!--[-->"),b.async_block([n[0]],p=>{const v=ensure_array_like(e.children);for(let h=0,C=v.length;h<C;h++){let l=v[h];st(p,{node:l});}}),b.push("<!--]-->")):b.push("<!--[!-->");}),g.push("<!--]-->");},$$slots:{default:true}});})):r.push("<!--[!-->");}),c.push("<!--]-->")):c.push("<!--[!-->");}),i.push("<!--]-->");});}const At="data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='576'%20height='576'%20viewBox='0%200%20576%20576'%20fill='none'%3e%3cpath%20d='M287.5%20229L86%20344.5L287.5%20460L489%20344.5L287.5%20229Z'%20stroke='url(%23paint0_linear_102_7)'%20stroke-width='59'%20stroke-linejoin='round'/%3e%3cpath%20d='M287.5%20116L86%20231.5L287.5%20347L489%20231.5L287.5%20116Z'%20stroke='url(%23paint1_linear_102_7)'%20stroke-width='59'%20stroke-linejoin='round'/%3e%3cpath%20d='M86%20344L288%20229'%20stroke='url(%23paint2_linear_102_7)'%20stroke-width='59'%20stroke-linejoin='bevel'/%3e%3cdefs%3e%3clinearGradient%20id='paint0_linear_102_7'%20x1='60'%20y1='341'%20x2='429.5'%20y2='344'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%23F9D100'/%3e%3cstop%20offset='1'%20stop-color='%23F97700'/%3e%3c/linearGradient%3e%3clinearGradient%20id='paint1_linear_102_7'%20x1='513.5'%20y1='231'%20x2='143.5'%20y2='231'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%23F9D100'/%3e%3cstop%20offset='1'%20stop-color='%23F97700'/%3e%3c/linearGradient%3e%3clinearGradient%20id='paint2_linear_102_7'%20x1='60'%20y1='344'%20x2='428.987'%20y2='341.811'%20gradientUnits='userSpaceOnUse'%3e%3cstop%20stop-color='%23F9D100'/%3e%3cstop%20offset='1'%20stop-color='%23F97700'/%3e%3c/linearGradient%3e%3c/defs%3e%3c/svg%3e",Ft="data:image/svg+xml,%3csvg%20width='28'%20height='28'%20viewBox='0%200%2028%2028'%20fill='none'%20xmlns='http://www.w3.org/2000/svg'%3e%3cpath%20fill-rule='evenodd'%20clip-rule='evenodd'%20d='M26.9425%202.94265C27.4632%202.42195%2027.4632%201.57773%2026.9425%201.05703C26.4218%200.536329%2025.5776%200.536329%2025.0569%201.05703L22.5713%203.54256C21.1213%202.59333%2019.5367%202.43378%2018.1753%202.64006C16.5495%202.88638%2015.1127%203.66838%2014.3905%204.39053L12.3905%206.39053C12.1405%206.64058%2012%206.97972%2012%207.33334C12%207.68697%2012.1405%208.0261%2012.3905%208.27615L19.7239%2015.6095C20.2446%2016.1302%2021.0888%2016.1302%2021.6095%2015.6095L23.6095%2013.6095C24.3316%2012.8873%2025.1136%2011.4505%2025.36%209.82475C25.5663%208.46312%2025.4066%206.87827%2024.4571%205.42807L26.9425%202.94265Z'%20fill='%233c4555'/%3e%3cpath%20fill-rule='evenodd'%20clip-rule='evenodd'%20d='M12.276%2012.9426C12.7967%2012.4219%2012.7967%2011.5777%2012.276%2011.057C11.7553%2010.5363%2010.9111%2010.5363%2010.3904%2011.057L8.66651%2012.7809L8.27615%2012.3905C8.0261%2012.1405%207.68697%2012%207.33334%2012C6.97972%2012%206.64058%2012.1405%206.39053%2012.3905L4.39053%2014.3905C3.66838%2015.1127%202.88638%2016.5495%202.64006%2018.1753C2.43377%2019.5367%202.59333%2021.1214%203.54262%2022.5714L1.05703%2025.057C0.536329%2025.5777%200.536329%2026.4219%201.05703%2026.9426C1.57773%2027.4633%202.42195%2027.4633%202.94265%2026.9426L5.42817%2024.4571C6.87835%2025.4066%208.46315%2025.5663%209.82475%2025.36C11.4505%2025.1136%2012.8873%2024.3316%2013.6095%2023.6095L15.6095%2021.6095C16.1302%2021.0888%2016.1302%2020.2446%2015.6095%2019.7239L15.2188%2019.3332L16.9426%2017.6093C17.4633%2017.0886%2017.4633%2016.2444%2016.9426%2015.7237C16.4219%2015.203%2015.5777%2015.203%2015.057%2015.7237L13.3332%2017.4475L10.5521%2014.6665L12.276%2012.9426Z'%20fill='%23FF7C00'/%3e%3c/svg%3e",Ot="data:image/svg+xml,%3csvg%20width='24'%20height='24'%20viewBox='0%200%2024%2024'%20xmlns='http://www.w3.org/2000/svg'%3e%3c!--%20Outer%20gear%20teeth%20(gray)%20--%3e%3cpath%20d='M19.14%2012.94c.04-.3.06-.61.06-.94%200-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24%200-.43.17-.47.41l-.36%202.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47%200-.59.22L2.74%208.87c-.12.21-.08.47.12.61l2.03%201.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03%201.58c-.18.14-.23.41-.12.61l1.92%203.32c.12.22.37.29.59.22l2.39-.96c.5.38%201.03.7%201.62.94l.36%202.54c.05.24.24.41.48.41h3.84c.24%200%20.44-.17.47-.41l.36-2.54c.59-.24%201.13-.56%201.62-.94l2.39.96c.22.08.47%200%20.59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12%2015.6c-1.98%200-3.6-1.62-3.6-3.6s1.62-3.6%203.6-3.6%203.6%201.62%203.6%203.6-1.62%203.6-3.6%203.6z'%20fill='%23808080'/%3e%3c!--%20Inner%20circle%20(now%20gray)%20--%3e%3ccircle%20cx='12'%20cy='12'%20r='2.5'%20fill='%23808080'/%3e%3c/svg%3e",qt="data:image/svg+xml,%3csvg%20viewBox='0%200%2020%2020'%20version='1.1'%20xmlns='http://www.w3.org/2000/svg'%20xmlns:xlink='http://www.w3.org/1999/xlink'%20fill='%23000000'%3e%3cg%20id='SVGRepo_bgCarrier'%20stroke-width='0'%3e%3c/g%3e%3cg%20id='SVGRepo_tracerCarrier'%20stroke-linecap='round'%20stroke-linejoin='round'%3e%3c/g%3e%3cg%20id='SVGRepo_iconCarrier'%3e%3ctitle%3erecord%20[%23982]%3c/title%3e%3cdesc%3eCreated%20with%20Sketch.%3c/desc%3e%3cdefs%3e%3c/defs%3e%3cg%20id='Page-1'%20stroke='none'%20stroke-width='1'%20fill='none'%20fill-rule='evenodd'%3e%3cg%20id='Dribbble-Light-Preview'%20transform='translate(-380.000000,%20-3839.000000)'%20fill='%23FF0000'%3e%3cg%20id='icons'%20transform='translate(56.000000,%20160.000000)'%3e%3cpath%20d='M338,3689%20C338,3691.209%20336.209,3693%20334,3693%20C331.791,3693%20330,3691.209%20330,3689%20C330,3686.791%20331.791,3685%20334,3685%20C336.209,3685%20338,3686.791%20338,3689%20M334,3697%20C329.589,3697%20326,3693.411%20326,3689%20C326,3684.589%20329.589,3681%20334,3681%20C338.411,3681%20342,3684.589%20342,3689%20C342,3693.411%20338.411,3697%20334,3697%20M334,3679%20C328.477,3679%20324,3683.477%20324,3689%20C324,3694.523%20328.477,3699%20334,3699%20C339.523,3699%20344,3694.523%20344,3689%20C344,3683.477%20339.523,3679%20334,3679'%20id='record-[%23982]'%3e%3c/path%3e%3c/g%3e%3c/g%3e%3c/g%3e%3c/g%3e%3c/svg%3e",Bt=/^'([^]+)'$/,$=Symbol("NOVALUE");class Gt{id;inputs;outputs;cancels;pending=false;trigger_modes;event_args={};targets=[];connection_type;triggers=[];original_trigger_id=null;show_progress_on=null;component_prop_inputs=[];show_progress;functions;constructor(t){this.id=t.id,this.original_trigger_id=t.id,this.inputs=t.inputs,this.outputs=t.outputs,this.connection_type=t.connection,this.show_progress=t.show_progress,this.functions={frontend:t.js?It(t.js,t.backend_fn,t.inputs.length,t.outputs.length):void 0,backend:t.backend_fn,backend_js:t.js_implementation?new _s(`let result = await (${t.js_implementation})(...arguments);
						return (!Array.isArray(result)) ? [result] : result;`):void 0},this.targets=t.targets,this.cancels=t.cancels,this.trigger_modes=t.trigger_mode,this.show_progress_on=t.show_progress_on||null,this.component_prop_inputs=t.component_prop_inputs||[];for(let i=0;i<t.event_specific_args?.length;i++){const e=t.event_specific_args[i];this.event_args[e]=t[e]??null;}}async run(t,i,e,s){let n=i;return this.functions.backend_js?{type:"data",data:await this.functions.backend_js(...n)}:(this.functions.frontend&&(n=await this.functions.frontend(i)),this.functions.backend?{type:"submit",data:t.submit(this.id,n,e,s,void 0,{"x-gradio-user":"app"})}:this.functions.frontend?{type:"data",data:n}:{type:"void",data:null})}add_trigger(t,i){this.triggers.push([t,i]);}get_triggers(){return {success:this.triggers.filter(([,t])=>t==="success").map(([t])=>t),failure:this.triggers.filter(([,t])=>t==="failure").map(([t])=>t),all:this.triggers.filter(([,t])=>t==="all").map(([t])=>t)}}}class Rt{dependencies_by_fn=new Map;dependencies_by_event=new Map;render_id_deps=new Map;submissions=new Map;client;queue=new Set;add_to_api_calls;update_state_cb;get_state_cb;rerender_cb;log_cb;loading_stati=new U$2;constructor(t,i,e,s,n,c,r){this.add_to_api_calls=r,this.log_cb=c,this.update_state_cb=e,this.get_state_cb=s,this.rerender_cb=n,this.client=i,this.reload(t,e,s,n,i);}reload(t,i,e,s,n){const{by_id:c,by_event:r}=this.create(t);this.dependencies_by_event=r,this.dependencies_by_fn=c,this.client=n,this.update_state_cb=i,this.get_state_cb=e,this.rerender_cb=s;for(const[u,g]of this.dependencies_by_fn)for(const[b]of g.targets)this.set_event_args(b,g.event_args);this.register_loading_stati(c);}register_loading_stati(t){for(const[i,e]of t)this.loading_stati.register(e.id,e.show_progress_on||e.outputs,e.inputs,e.show_progress);}clear_loading_status(t){this.loading_stati.clear(t);}async update_loading_stati_state(){for(const[t,i]of Object.entries(this.loading_stati.current))this.update_state_cb(Number(t),{loading_status:i},false);}dispatch_state_change_events(t){if(t.changed_state_ids)for(const i of t.changed_state_ids)this.dependencies_by_event.get("change-"+i)?.forEach(s=>{this.dispatch({type:"fn",fn_index:s.id,target_id:i,event_data:null});});}async dispatch(t){let i;if(t.type==="fn"){const e=this.dependencies_by_fn.get(t.fn_index);e&&(i=[e]);}else i=this.dependencies_by_event.get(`${t.event_name}-${t.target_id}`);for(let e=0;e<(i?.length||0);e++){const s=i?i[e]:void 0;if(s){this.cancel(s.cancels);const n=Ut(s.trigger_modes,this.submissions.has(s.id));if(n==="skip")continue;if(n==="defer"){this.queue.add(s.id);continue}s.functions.backend&&(this.loading_stati.update({status:"pending",fn_index:s.id,stream_state:null}),this.update_loading_stati_state());const c=await this.gather_state(s.inputs,s.component_prop_inputs),r=await Promise.all(s.targets.map(([p])=>this.set_event_args(p,s.event_args))),{success:u,failure:g,all:b}=s.get_triggers();try{let p=null;if(t.target_id!==void 0||t.type==="event"?p=t.target_id||null:p=s.original_trigger_id,s.connection_type==="stream"&&this.submissions.has(s.id)){const h=this.submissions.get(s.id);let C={fn_index:s.id,data:c,event_data:t.event_data};h.send_chunk(C),r.forEach(l=>l());continue}this.add_to_api_calls({fn_index:s.id,data:c,event_data:t.event_data,trigger_id:p});const v=await s.run(this.client,c,t.event_data,p);if(v.type==="void")r.forEach(h=>h());else if(v.type==="data")await this.handle_data(s.outputs,v.data),r.forEach(h=>h());else {let h=null;s.connection_type==="stream"&&!this.submissions.has(s.id)&&(h="waiting"),this.submissions.set(s.id,v.data);let C=0;t:for await(const l of v.data)if(C===0&&s.inputs.forEach(d=>{this.update_state_cb(d,{loading_status:{validation_error:null}},!1);}),C+=1,l!==null){if(l.type==="data"&&await this.handle_data(s.outputs,l.data),l.type==="status"){l.original_msg==="process_starts"&&s.connection_type==="stream"&&(h="open");const{fn_index:d,...m}=l;if(l.stage==="complete"){h="closed",u.forEach(L=>{this.dispatch({type:"fn",fn_index:L,event_data:null,target_id:p});}),this.dispatch_state_change_events(l),this.loading_stati.update({...m,status:m.stage,fn_index:s.id,stream_state:h}),this.update_loading_stati_state();break t}else if(l.stage==="generating")this.dispatch_state_change_events(l),this.loading_stati.update({...m,status:m.stage,fn_index:s.id,stream_state:h}),this.update_loading_stati_state();else if(l.stage==="error"){if(Array.isArray(l?.message)){l.message.forEach((w,E)=>{this.update_state_cb(s.inputs[E],{loading_status:{validation_error:w.is_valid?null:w.message,show_validation_error:!0}},!1);}),s.outputs.forEach(w=>{s.inputs.includes(w)||this.update_state_cb(w,{loading_status:{status:null}},!1);}),r.forEach(w=>w()),this.submissions.delete(s.id),this.queue.has(s.id)&&(this.queue.delete(s.id),this.dispatch(t));return}const L=l?.message?.replace(Bt,(w,E)=>E);throw this.log_cb(l?._title??"Error",L||"",d,"error",m.duration,m.visible),new Error("Dependency function failed")}else this.loading_stati.update({...m,status:m.stage,fn_index:s.id,stream_state:h}),this.update_loading_stati_state();}if(l.type==="render"){this.loading_stati.update({status:"complete",fn_index:s.id,stream_state:null}),this.update_loading_stati_state();const{layout:d,components:m,render_id:L,dependencies:w}=l.data;this.rerender_cb(m,d);const{by_id:E,by_event:B}=this.create(w);this.register_loading_stati(E),E.forEach(M=>this.dependencies_by_fn.set(M.id,M)),B.forEach((M,O)=>this.dependencies_by_event.set(O,M));const F=this.render_id_deps.get(L);F&&F.forEach(M=>{E.has(M)||this.dependencies_by_fn.delete(M);}),this.render_id_deps.set(L,new Set(Array.from(E.keys()))),this.register_loading_stati(E);break t}l.type==="log"&&this.handle_log(l);}b.forEach(l=>{this.dispatch({type:"fn",fn_index:l,event_data:null,target_id:p});}),r.forEach(l=>l()),this.submissions.delete(s.id),this.queue.has(s.id)&&(this.queue.delete(s.id),this.dispatch(t));}}catch{this.loading_stati.update({status:"error",fn_index:s.id,eta:0,queue:false,stream_state:null}),this.update_loading_stati_state(),this.submissions.delete(s.id),g.forEach(v=>{this.dispatch({type:"fn",fn_index:v,event_data:null});});}}}}create(t){const i=new Map,e=new Map,s=[];for(const n of t){const c=new Gt(n);for(const[r,u]of n.targets)e.has(`${u}-${r}`)||e.set(`${u}-${r}`,[]),e.get(`${u}-${r}`)?.push(c);if(i.set(n.id,c),n.trigger_after!==void 0){const r=n.trigger_only_on_failure?"failure":n.trigger_only_on_success?"success":"all";s.push([n.id,n.trigger_after,r]);}}for(const[n,c,r]of s){const u=i.get(c);u&&(u.add_trigger(n,r),u.original_trigger_id=Tt(t,c));}return {by_id:i,by_event:e}}handle_log(t){const{title:i,log:e,fn_index:s,level:n,duration:c,visible:r}=t;this.log_cb(i,e,s,n,c,r);}async handle_data(t,i){await Promise.all(t.map(async(e,s)=>{const n=i[s]===void 0?$:i[s];if(n!==$)if(Dt(n)){let c=false,r=null;for(const[u,g]of Object.entries(n))if(u!=="__type__"){if(u==="visible"){c=true,r=g;continue}await this.update_state_cb(t[s],{[u]:g},false);}c&&await this.update_state_cb(t[s],{visible:r},true);}else await this.update_state_cb(e,{value:n},false);}));}async gather_state(t,i=[]){return (await Promise.all(t.map(e=>this.get_state_cb(e)))).map((e,s)=>i.includes(s)?e??null:e?.value??null)}async set_event_args(t,i){let e={};const s=await this.get_state_cb?.(t);if(!s)return ()=>{};for(const[n]of Object.entries(i))e[n]=s?.[n]??null;return Object.keys(i).length===0?()=>{}:(await this.update_state_cb(t,i,false),()=>{this.update_state_cb(t,e,false);})}async cancel(t){if(t)for(const i of t){const e=this.submissions.get(i);e&&(await e.cancel(),this.loading_stati.update({status:"complete",fn_index:i,eta:0,queue:false,stream_state:null}),this.update_loading_stati_state(),this.submissions.delete(i));}}dispatch_load_events(){this.dependencies_by_fn.forEach(t=>{t.targets.forEach(([i,e])=>{e==="load"&&this.dispatch({type:"fn",fn_index:t.id,event_data:null,target_id:i});});});}get_fns_from_targets(t){const i=[];return this.dependencies_by_event.forEach((e,s)=>{const[,n]=s.split("-");Number(n)===t&&e.forEach(c=>{i.push(c.id);});}),i}close_stream(t){const i=this.get_fns_from_targets(t);for(const e of i){const s=this.submissions.get(e);s&&(s.close_stream(),this.submissions.delete(e)),this.loading_stati.update({status:"complete",fn_index:e,eta:0,queue:false,stream_state:"closed"});}this.update_loading_stati_state();}}function Dt(f){return typeof f=="object"&&f!==null&&"__type__"in f&&f?.__type__==="update"}function Ut(f,t){return t?f==="always_last"?"defer":f==="multiple"?"run":f==="once"?"skip":"run":"run"}function It(f,t,i,e){const s=t?i===1:e===1;try{return new _s("__fn_args",`  let result = await (${f})(...__fn_args);
  if (typeof result === "undefined") return [];
  return (${s} && !Array.isArray(result)) ? [result] : result;`)}catch(n){throw n}}function Tt(f,t){let i=new Map,e=t,s=0;for(;s<100;){const n=i.get(e)||f.find(c=>c.id===e);if(!n||(i.set(n.id,n),n.trigger_after===null||n.trigger_after===void 0))break;e=n.trigger_after,s+=1;}return e}function Nt(f,t){f.component(i=>{var e;let{root:s$1,components:n,layout:c,dependencies:r,title:u,target:g,autoscroll:b,footer_links:p,control_page_title:v,app_mode:h,theme_mode:C,app:l$1,space_id:d,version:m,js:L,fill_height:w,username:E,api_prefix:B,max_file_size:F,initial_layout:M,css:O,vibe_mode:G,search_params:R,render_complete:Pt=false,ready:I=false,reload_count:it=0,add_new_message:T=void 0}=t;n.forEach(a=>{a.props.i18n||(a.props.i18n=store_get(e??={},"$reactive_formatter",gs));});let S=[];function N(a,_,x){if(_==="share"){const{title:z,description:W}=x;}else if(_==="error")A("Error",x,-1,_,10,true);else if(_==="warning")A("Warning",x,-1,_,10,true);else if(_==="info")A("Info",x,-1,_,10,true);else if(_==="gradio_expand"||_==="gradio_tab_select"){const z=_==="gradio_expand"?a:x.component_id;y.render_previously_invisible_children(z);}else if(_=="clear_status")y.update_state(a,{loading_status:{}},false),j.clear_loading_status(a);else if(_=="close_stream")j.close_stream(a);else if(_==="custom_button_click"){const z=x.id;at(z,"click",null);}else _==="select"&&a in y.initial_tabs&&(a=x.id),j.dispatch({type:"event",event_name:_,target_id:a,event_data:x});}let y=new G$1(n,c,r,{root:s$1,theme:C,version:m,api_prefix:B,max_file_size:F,autoscroll:b},l$1,store_get(e??={},"$reactive_formatter",gs),N);function at(a,_,x){j.dispatch({type:"event",event_name:_,target_id:a,event_data:x});}setContext(l,{register:y.register_component.bind(y),dispatcher:N});let P=[],V=null,nt=a=>{V=a,ct&&(P=[...P,V]);},j=new Rt(r,l$1,y.update_state.bind(y),y.get_state.bind(y),y.rerender.bind(y),A,nt),ot=350,lt=R.get("view")==="api"&&p.includes("api"),rt=R.get("view")==="settings",ct=R.get("view")==="api-recorder"&&p.includes("api"),_t=null,ut=null;function A(a,_,x,z,W=10,J=false){J&&S.push({title:a,message:_,fn_index:x,type:z,id:++pt,duration:W,visible:J});}T=A;let pt=-1;store_get(e??={},"$reactive_formatter",gs)("blocks.long_requests_queue"),store_get(e??={},"$reactive_formatter",gs)("blocks.connection_can_break"),store_get(e??={},"$reactive_formatter",gs)("blocks.waiting_for_inputs");let Z=writable(false);function ft(a){S=S.filter(_=>_.id!==a);}let Q=true,U;function gt(a){head("zxu34v",a,_=>{v?(_.push("<!--[-->"),_.title(x=>{x.push(`<title>${escape_html(u)}</title>`);})):_.push("<!--[!-->"),_.push("<!--]--> "),O?(_.push("<!--[-->"),_.push(`${html(`<style>${fs(O,m)}</style>`)}`)):_.push("<!--[!-->"),_.push("<!--]-->");}),a.push(`<div class="wrap svelte-zxu34v"${attr_style("",{"min-height":h?"100%":"auto"})}><main class="contain svelte-zxu34v"${attr_style("",{"flex-grow":h?"1":"auto","margin-right":G?`${ot}px`:"0"})}>`),st(a,{node:y.root}),a.push("<!----></main> "),p.length>0?(a.push("<!--[-->"),a.push('<footer aria-label="Gradio footer navigation" class="svelte-zxu34v">'),p.includes("api")?(a.push("<!--[-->"),a.push('<button class="show-api svelte-zxu34v">'),l$1.config?.mcp_server?(a.push("<!--[-->"),a.push(`${escape_html(store_get(e??={},"$reactive_formatter",gs)("errors.use_via_api_or_mcp"))}`)):(a.push("<!--[!-->"),a.push(`${escape_html(store_get(e??={},"$reactive_formatter",gs)("errors.use_via_api"))}`)),a.push(`<!--]--> <img${attr("src",Ft)}${attr("alt",store_get(e??={},"$reactive_formatter",gs)("common.logo"))} class="svelte-zxu34v"/></button>`)):a.push("<!--[!-->"),a.push("<!--]--> "),p.includes("gradio")?(a.push("<!--[-->"),a.push(`<div class="divider show-api-divider svelte-zxu34v">·</div> <a href="https://gradio.app" class="built-with svelte-zxu34v" target="_blank" rel="noreferrer">${escape_html(store_get(e??={},"$reactive_formatter",gs)("common.built_with_gradio"))} <img${attr("src",At)}${attr("alt",store_get(e??={},"$reactive_formatter",gs)("common.logo"))} class="svelte-zxu34v"/></a>`)):a.push("<!--[!-->"),a.push(`<!--]--> <button${attr_class("record svelte-zxu34v",void 0,{hidden:!store_get(e??={},"$is_screen_recording",Z)})}>${escape_html(store_get(e??={},"$reactive_formatter",gs)("common.stop_recording"))} <img${attr("src",qt)}${attr("alt",store_get(e??={},"$reactive_formatter",gs)("common.stop_recording"))} class="svelte-zxu34v"/></button> <div class="divider svelte-zxu34v">·</div> `),p.includes("settings")?(a.push("<!--[-->"),a.push(`<div${attr_class("divider svelte-zxu34v",void 0,{hidden:!store_get(e??={},"$is_screen_recording",Z)})}>·</div> <button class="settings svelte-zxu34v">${escape_html(store_get(e??={},"$reactive_formatter",gs)("common.settings"))} <img${attr("src",Ot)}${attr("alt",store_get(e??={},"$reactive_formatter",gs)("common.settings"))} class="svelte-zxu34v"/></button>`)):a.push("<!--[!-->"),a.push("<!--]--></footer>")):a.push("<!--[!-->"),a.push("<!--]--> "),a.push("<!--[!-->"),a.push("<!--]--> "),lt&&y.root&&_t||a.push("<!--[!-->"),a.push("<!--]--> "),rt&&l$1.config&&y.root&&ut||a.push("<!--[!-->"),a.push("<!--]--> "),a.push("<!--[!-->"),a.push("<!--]--></div> "),S?(a.push("<!--[-->"),P$2(a,{messages:S,on_close:ft})):a.push("<!--[!-->"),a.push("<!--]-->");}do Q=true,U=i.copy(),gt(U);while(!Q);i.subsume(U),e&&unsubscribe_stores(e),bind_props(t,{ready:I,reload_count:it,add_new_message:T});});}function tt(f,t){f.component(i=>{let e=t.root,s$1=t.auth_message,n=t.app_mode,c=t.space_id,r=t.i18n,u="",g="",b$1=false;const p=async()=>{const l=new FormData;l.append("username",u),l.append("password",g);let d=await fetch(e+"/login",{method:"POST",body:l});d.status===400?(b$1=true,u="",g=""):d.status==200&&location.reload();};let v=true,h;function C(l){l.push(`<div${attr_class("wrap svelte-14xt79u",void 0,{"min-h-screen":n})}>`),b(l,{variant:"panel",min_width:480,children:d=>{d.push(`<h2 class="svelte-14xt79u">${escape_html(r("login.login"))}</h2> `),s$1?(d.push("<!--[-->"),d.push(`<p class="auth svelte-14xt79u">${html(s$1)}</p>`)):d.push("<!--[!-->"),d.push("<!--]--> "),c?(d.push("<!--[-->"),d.push(`<p class="auth svelte-14xt79u">${escape_html(r("login.enable_cookies"))}</p>`)):d.push("<!--[!-->"),d.push("<!--]--> "),b$1?(d.push("<!--[-->"),d.push(`<p class="creds svelte-14xt79u">${escape_html(r("login.incorrect_credentials"))}</p>`)):d.push("<!--[!-->"),d.push("<!--]--> "),o$1(d,{children:m=>{G(m,{children:L=>{pt(L,{label:r("login.username"),lines:1,show_label:true,max_lines:1,onsubmit:p,get value(){return u},set value(w){u=w,v=false;}});},$$slots:{default:true}}),m.push("<!----> "),G(m,{children:L=>{pt(L,{label:r("login.password"),lines:1,show_label:true,max_lines:1,type:"password",onsubmit:p,get value(){return g},set value(w){g=w,v=false;}});},$$slots:{default:true}}),m.push("<!---->");},$$slots:{default:true}}),d.push("<!----> "),B(d,{size:"lg",variant:"primary",onclick:p,children:m=>{m.push(`<!---->${escape_html(r("login.login"))}`);}}),d.push("<!---->");},$$slots:{default:true}}),l.push("<!----></div>");}do v=true,h=i.copy(),C(h);while(!v);i.subsume(h),bind_props(t,{root:e,auth_message:s$1,app_mode:n,space_id:c,i18n:r});});}let ce=true;async function _e({url:f,data:{server:t,port:i,local_dev_mode:e,accept_language:s,root_url:n,mount_path:c},route:r}){let u;const g=a&&!e&&n?new URL(c||"/",n).href:t,b=f.searchParams.get("deep_link"),p=new Headers;a?p.append("x-gradio-server",new URL(c,location.origin).href):p.append("x-gradio-server",n);try{u=await qt$1.connect(g,{with_null_state:!0,events:["data","log","status","render"],query_params:b?{deep_link:b}:void 0,headers:p});}catch(h){const C=h.message||"";let l="";return C.includes(di)||(l=C.replace(/^Error:?\s*/,"")),{Render:tt,config:{auth_message:l,auth_required:true,components:[],current_page:"",dependencies:[],layout:{},pages:[],page:{},root:f.origin,space_id:null,analytics_enabled:false,connect_heartbeat:false,css:"",js:"",theme_hash:0,head:"",dev_mode:false,enable_queue:false,show_error:false,fill_height:false,fill_width:false,mode:"blocks",theme:"default",title:"",version:"",api_prefix:"",is_space:false,is_colab:false,footer_links:["gradio","settings"],stylesheets:[],protocol:"sse_v3",username:""},api_url:g,layout:{},app:null}}if(!u.config)throw new Error("No config found");let v=u.get_url_config(f.toString());return await Es(u.config?.i18n_translations||void 0,s),{Render:u.config?.auth_required?tt:Nt,config:v,api_url:g,app:u}}

var _page_ts = /*#__PURE__*/Object.freeze({
  __proto__: null,
  load: _e,
  ssr: ce
});

async function i({request:e}){const o=e.headers.get("x-gradio-server")||"http://127.0.0.1:7860",r=e.headers.get("x-gradio-port")||"7860",t$1=e.headers.get("x-gradio-local-dev-mode")||t?"true":void 0,d=e.headers.get("accept-language")||"en",a=e.headers.get("x-gradio-mounted-path")||"/",n=new URL(e.headers.get("x-gradio-original-url")||o).origin;return {server:o,root_url:new URL(a,n).href,mount_path:a,port:r,local_dev_mode:t$1,accept_language:d}}

var _page_server_ts = /*#__PURE__*/Object.freeze({
  __proto__: null,
  load: i
});

const index = 2;
let component_cache;
const component = async () => component_cache ??= (await import('./_page.svelte-BkdspukR.js')).default;
const universal_id = "src/routes/[...catchall]/+page.ts";
const server_id = "src/routes/[...catchall]/+page.server.ts";
const imports = ["_app/immutable/nodes/2.D5nXHu-Z.js","_app/immutable/chunks/7I93MIQG.js","_app/immutable/chunks/PPVm8Dsz.js","_app/immutable/chunks/Bm21-Y_h.js"];
const stylesheets = ["_app/immutable/assets/2.DQG8VgAX.css","_app/immutable/assets/Index.DHz84ApK.css","_app/immutable/assets/Index.DIMxqS5W.css","_app/immutable/assets/Example.PnzFsODt.css","_app/immutable/assets/ModifyUpload.C2I0h_eD.css","_app/immutable/assets/Index.GQZxeo40.css","_app/immutable/assets/Index.B80bIer5.css","_app/immutable/assets/Example.Cpi22WGa.css","_app/immutable/assets/Index.B2BpVHOS.css","_app/immutable/assets/Example.QWdMqwA5.css","_app/immutable/assets/Index.Czv6Lgei.css","_app/immutable/assets/Example.BK-tWmkG.css","_app/immutable/assets/Example.bHSd0VUC.css","_app/immutable/assets/Index.Ci-0XPiC.css","_app/immutable/assets/Example.jts6u4zx.css","_app/immutable/assets/Index.DpH7sR6h.css","_app/immutable/assets/Index.EYuwUe6R.css","_app/immutable/assets/Example.BUUMH8K0.css","_app/immutable/assets/Example.BeU1J4ps.css","_app/immutable/assets/Index.-Uz_kS2s.css","_app/immutable/assets/Index.Bn0zLMEj.css","_app/immutable/assets/Index.3FqI08xq.css","_app/immutable/assets/Index.CioP8lnm.css","_app/immutable/assets/Example.CbN4r5yx.css","_app/immutable/assets/Index.BDarcd0p.css","_app/immutable/assets/Example.-V2chS2k.css","_app/immutable/assets/Index.CEhk7M0s.css","_app/immutable/assets/Video.emdvV6JL.css","_app/immutable/assets/Gallery.DJhld1Jx.css","_app/immutable/assets/Example.CA1DPrcM.css","_app/immutable/assets/Index.BPmhhU8b.css","_app/immutable/assets/Index.Dg9ut_M4.css","_app/immutable/assets/HTML.BeG9Dlb0.css","_app/immutable/assets/Example.BG5zdIqX.css","_app/immutable/assets/Index.5RnUXY9l.css","_app/immutable/assets/Example.CZSJmqDf.css","_app/immutable/assets/Index.Dpdel1G9.css","_app/immutable/assets/Example.C7vkYQeg.css","_app/immutable/assets/Example.CD_WZEqN.css","_app/immutable/assets/Index.BpcA6Nec.css","_app/immutable/assets/JSON.BXT8NU56.css","_app/immutable/assets/Example.BlpJt4zj.css","_app/immutable/assets/Index.-e-Yppt2.css","_app/immutable/assets/Example.CgIc4GLa.css","_app/immutable/assets/Index.cY7HT1Ac.css","_app/immutable/assets/Model3D.CvGLqGnb.css","_app/immutable/assets/Example.RXDI_Ar6.css","_app/immutable/assets/Index.CvyxbOJU.css","_app/immutable/assets/Example.BIrWl-Kd.css","_app/immutable/assets/Index.CFFjrWXb.css","_app/immutable/assets/Index.fPjHowzi.css","_app/immutable/assets/Example.guFL0Sj1.css","_app/immutable/assets/Index.CTDY4JGM.css","_app/immutable/assets/Example.Do5iR6B9.css","_app/immutable/assets/Index.Bk2NH8dC.css","_app/immutable/assets/Example.DWDv4qx4.css","_app/immutable/assets/Index.BL_HMluy.css","_app/immutable/assets/Index.BijVyRsD.css","_app/immutable/assets/Index.DMaj38-p.css","_app/immutable/assets/Example.DSMNiXnn.css","_app/immutable/assets/Index.CwinLc1f.css","_app/immutable/assets/Walkthrough.CJf9hODv.css","_app/immutable/assets/Index.Ds3FAhOq.css","_app/immutable/assets/Index.Xhg3Ucw_.css","_app/immutable/assets/Index.DP8ihX8q.css","_app/immutable/assets/Example.4NTZ2aku.css","_app/immutable/assets/index.uLojFN0n.css","_app/immutable/assets/Example.D2nbjfVb.css","_app/immutable/assets/Index.BZR-ZeTY.css"];
const fonts = [];

var _2 = /*#__PURE__*/Object.freeze({
  __proto__: null,
  component: component,
  fonts: fonts,
  imports: imports,
  index: index,
  server: _page_server_ts,
  server_id: server_id,
  stylesheets: stylesheets,
  universal: _page_ts,
  universal_id: universal_id
});

export { n as A, B, c$1 as C, ls as D, Es as E, u$1 as F, G$1 as G, b$1 as H, o$1 as I, Jo as J, se$2 as K, Lt$1 as L, pt as M, Ne$1 as N, M as O, P$2 as P, s as Q, S, U$2 as U, Yo as Y, Zo as Z, _2 as _, U as a, bs as b, G as c, b as d, y as e, fs as f, g$2 as g, hs as h, Ss as i, w$1 as j, v as k, w as l, y$2 as m, d$1 as n, h as o, pr as p, c as q, P as r, sn as s, e as t, us as u, vs as v, ws as w, xs as x, ys as y, o as z };
//# sourceMappingURL=2-B89dC7Mi.js.map
