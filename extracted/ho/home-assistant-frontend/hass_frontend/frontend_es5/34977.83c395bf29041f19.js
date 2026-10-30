"use strict";(self.rspackChunkhome_assistant_frontend=self.rspackChunkhome_assistant_frontend||[]).push([[34977],{84032(t,e,i){var a=i(55702);const o=(t,e)=>{for(const i of t){const t=e[i];if(t&&!t.attributes.passive&&"number"==typeof t.attributes.latitude&&"number"==typeof t.attributes.longitude)return t}};i.d(e,{},{H:(t,e)=>{const{latitude:i,longitude:r,gps_accuracy:n}=t.attributes;if("number"==typeof i&&"number"==typeof r)return{latitude:i,longitude:r,gpsAccuracy:n};if("person"!==(0,a.t)(t))return;const s=t.attributes.in_zones;if(!Array.isArray(s)||0===s.length)return;const l=o(s,e);return l?{latitude:l.attributes.latitude,longitude:l.attributes.longitude}:void 0},_:o})},15114(t,e,i){i(65649),i(62922),i(14167),i(59350),i(70425),i(63145),i(53930),i(84345),i(83460),i(11663);var a=i(40308),o=i(15651);const r={light:"/static/map/light.json",dark:"/static/map/dark.json"},n=`${o.ZV}/raster/{z}/{x}/{y}.png?token={token}`;let s;const l=()=>(()=>{if(void 0===s)try{var t;const e=document.createElement("canvas").getContext("webgl2");s=Boolean(e),null==e||null===(t=e.getExtension("WEBGL_lose_context"))||void 0===t||t.loseContext()}catch{s=!1}return s})(),d=t=>new URL(t,location.href).href,c=new Map,h=async t=>{var e;const a=t.shipped&&r[t.shipped],o=a?JSON.parse(await(t=>{let e=c.get(t);return e||(e=fetch(t).then(t=>t.text()).finally(()=>c.delete(t)),c.set(t,e)),e})(a)):await(await i.e(5393).then(i.bind(i,76616))).buildMapStyle(t.palette,null!==(e=t.options)&&void 0!==e?e:{},t.baseColors);return"string"==typeof o.sprite?o.sprite=d(o.sprite):Array.isArray(o.sprite)&&(o.sprite=o.sprite.map(t=>({...t,url:d(t.url)}))),o};let u=!1;const p=t=>{u||(u=!0,t(new URL("/frontend_es5/maplibre-gl-worker.20261028.1.js",location.href).href))},m=(t,e,i)=>{const a=t.tileLayer((0,o.bK)(n),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',maxZoom:20,maxNativeZoom:19,referrerPolicy:void 0,token:null!=i?i:""}).addTo(e);let r=!1,s=0;a.on("tileerror",()=>{r=!0,Date.now()-s<3e4||(s=Date.now(),(0,o.Oc)())});const l=(0,o.Xx)(t=>{a.options.token=t,r&&(r=!1,a.redraw())});return e.on("unload",l),{setMapStyle:()=>{}}};i.d(e,{},{MK:h,V4:async(t,e,r,n,s=!1)=>{if(!s&&l()){let s;try{const[{maplibreGL:l},d]=await Promise.all([Promise.all([i.e(84032),i.e(84259),i.e(13549)]).then(i.bind(i,75483)),Promise.all([i.e(84032),i.e(48261)]).then(i.bind(i,75555))]);p(d.setWorkerUrl),s=await(async(t,e,i,r,n)=>{let s;try{s=t({style:await h(r),transformRequest:t=>({...(0,o.rG)(t),referrerPolicy:void 0})}),s.addTo(i)}catch{if(s)try{s.remove()}catch{}return}let l=r,d=r,c=0,u=!0,p=!1,b=n;const g=s.getMaplibreMap();let v,f=!1;const y=()=>{f&&k()},_=()=>{u=!1,document.removeEventListener("visibilitychange",y);try{s.remove()}catch{}m(e,i,b)},k=()=>{clearTimeout(v),u&&!document.hidden&&(v=window.setTimeout(_,2e3))};g.on("webglcontextlost",()=>{f=!0,k()}),g.on("webglcontextrestored",()=>{f=!1,clearTimeout(v)}),document.addEventListener("visibilitychange",y),i.on("unload",()=>{clearTimeout(v),document.removeEventListener("visibilitychange",y)});const w=t=>{const e=++c;h(t).then(i=>{var a;e===c&&(l=t,null===(a=s.getMaplibreMap())||void 0===a||a.setStyle(i))}).catch(()=>{e===c&&(d=l)})};let M=0;g.on("error",t=>{var e;const i=null===(e=t.error)||void 0===e?void 0:e.status;void 0!==i&&403!==i&&404!==i||Date.now()-M<3e4||(M=Date.now(),p=!0,(0,o.Oc)())});const x=(0,o.Xx)(t=>{b=t,u&&p&&(p=!1,w(d))});return i.on("unload",x),{setMapStyle:t=>{u&&!(0,a.b)(t,d)&&(d=t,w(t))}}})(l,t,e,r,n)}catch{}if(s)return s}return m(t,e,n)},W$:p,jV:l})},2064(t,e,i){i.d(e,{},{rx:t=>{const e=document.createElement("div");e.className="editable-circle-resize",e.tabIndex=0,e.setAttribute("role","slider"),e.setAttribute("aria-valuemin","1"),e.setAttribute("aria-valuemax",String(1e5)),t&&e.setAttribute("aria-label",t);const i=document.createElement("div");return i.className="editable-circle-resize-dot",e.appendChild(i),e},xr:"\n  .editable-circle-center {\n    width: 16px;\n    height: 16px;\n    border-radius: 50%;\n    background: var(--primary-color);\n    border: 2px solid var(--card-background-color, #fff);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n  .editable-circle-resize {\n    width: 24px;\n    height: 24px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    cursor: ew-resize;\n  }\n  .editable-circle-resize-dot {\n    width: 12px;\n    height: 12px;\n    border-radius: 50%;\n    background: var(--card-background-color, #fff);\n    border: 2px solid var(--primary-color);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n"})},74284(t,e,i){i(24407);const a=6371008.8,o=t=>t*Math.PI/180,r=t=>180*t/Math.PI,n=(t,e,i)=>{const n=e/a,s=o(t[0]),l=o(i),d=Math.asin(Math.sin(s)*Math.cos(n)+Math.cos(s)*Math.sin(n)*Math.cos(l)),c=Math.atan2(Math.sin(l)*Math.sin(n)*Math.cos(s),Math.cos(n)-Math.sin(s)*Math.sin(d));return[r(d),t[1]+r(c)]},s=85.051129,l=([t,e],i)=>{const a=Math.sin(o(Math.max(-85.051129,Math.min(s,t))));return{x:(e/360+.5)*i,y:(.5-Math.log((1+a)/(1-a))/(4*Math.PI))*i}};i.d(e,{},{RO:(t,e)=>n(t,e,90),Rn:(t,e)=>{const i=e/a,n=Math.max(-90,t[0]-r(i)),s=Math.min(90,t[0]+r(i)),l=Math.sin(i)/Math.cos(o(t[0]));if(n<=-90||s>=90||Math.abs(l)>=1)return[[n,-180],[s,180]];const d=r(Math.asin(l));return[[n,t[1]-d],[s,t[1]+d]]},S_:(t,e)=>{const i=o(e[0]-t[0]),a=o(e[1]-t[1]),r=Math.sin(i/2)**2+Math.cos(o(t[0]))*Math.cos(o(e[0]))*Math.sin(a/2)**2;return 12742017.6*Math.asin(Math.sqrt(r))},bM:n,kb:(t,e,i)=>{const a=256*2**i,o=l(t,a),r=l(e,a),n=Math.abs(o.x-r.x);return Math.hypot(Math.min(n,a-n),o.y-r.y)}})},62269(t,e,i){i.d(e,{jJ:()=>o,u8:()=>a,l6:()=>s,kR:()=>u,vA:()=>h});i(19945),i(65649),i(14167),i(1339);const a=["default","colorful","natural","muted","gray","toner"],o="default",r={default:{palette:"colorful",colors:{background:"#f5efe5",land:"#f5efe5",water:"#b8daec",labelWater:"#5487aa",natureWood:"#cfe4bc",natureGrass:"#e2eed8",naturePark:"#cfe4bc",natureLeisure:"#e2eed8",natureAgriculture:"#e8efe1",natureWetland:"#e5ecdf",natureSand:"#f3eadd",natureRock:"#f3eadd",glacier:"#faf6f0",areaResidential:"#f1e9da",areaCommercial:"#f7e0d8",areaIndustrial:"#f0e7cb",areaWaste:"#eee3d3",areaBurial:"#f1e9da",siteParking:"#efe7d6",siteSports:"#cfe4bc26",building:"#eadec7",buildingBg:"#e0cdae",roadStreet:"#fcfaf8",roadStreetBg:"#e9dbc4",roadTrunk:"#ffe7be",roadTrunkBg:"#ebd09f",roadMotorway:"#f1d6a5",roadMotorwayBg:"#e8bd6e",transitRail:"#ece0cb",transitSubway:"#ece2cf",transitCycle:"#f3eee2",transitFoot:"#f3eee2",boundary:"#dbc49f",boundaryDisputed:"#e5d7bd",label:"#4b473c",labelHalo:"#faf8f5cc",labelSymbol:"#8f8774",labelPoi:"#8f877466",labelShield:"#fbf8f3",labelHousenumber:"#8f87744d"},colorsDark:{background:"#191b2c",land:"#191b2c",water:"#27357a",labelWater:"#9cc0f0",natureWood:"#254948",natureGrass:"#213b39",naturePark:"#28504b",natureLeisure:"#213532",natureAgriculture:"#203233",natureWetland:"#253337",natureSand:"#2a2c3d",natureRock:"#2a2c3d",glacier:"#2a2c3d",areaResidential:"#1d2034",areaCommercial:"#29213a",areaIndustrial:"#242431",areaWaste:"#1d2034",areaBurial:"#1d2034",siteParking:"#1d2034",siteSports:"#25413926",building:"#21243c",buildingBg:"#2a2e4a",roadStreet:"#2b3052",roadStreetBg:"#1a1d33",roadTrunk:"#383e67",roadTrunkBg:"#22263f",roadMotorway:"#454d7d",roadMotorwayBg:"#2a2f4c",transitRail:"#2c3150",transitSubway:"#2c3150",transitCycle:"#2b3052",transitFoot:"#2b3052",boundary:"#3b4068",boundaryDisputed:"#3b4068",label:"#e7ecf8",labelHalo:"#12141fcc",labelSymbol:"#959dbd",labelPoi:"#959dbd66",labelShield:"#191b2c",labelHousenumber:"#959dbd4d"}},colorful:{palette:"colorful"},natural:{palette:"natural"},muted:{palette:"muted"},gray:{palette:"gray"},toner:{palette:"toner"}},n=t=>a.includes(t),s=t=>"object"==typeof t&&null!==t,l=["colors","recolor","text","icon","layers"],d=t=>t.replace(/_([a-z])/g,(t,e)=>e.toUpperCase()),c=t=>Array.isArray(t)?t.map(c):t&&"object"==typeof t?Object.fromEntries(Object.entries(t).map(([t,e])=>[d(t),c(e)])):t,h=(t,e)=>{const i=n(e)&&e!==o?e:void 0,a=s(t)?{...t}:{};return delete a.base,Object.keys(a).length?{...i&&{base:i},...a}:i},u=(t,e,i)=>{var a;const h=s(t)?t:void 0,u=h?h.base:t,p=n(u)?u:o,m=((t,e)=>{const{palette:i}=r[t];return e?`${i}-dark`:i})(p,e),b=h?((t,e)=>{const i=t,a={};for(const t of l){var o;const e=null!==(o=i[t])&&void 0!==o?o:i[d(t)];void 0!==e&&(a[d(t)]=c(e))}const r=i.colors_dark;return e&&void 0!==r&&(a.colors=c(r)),a})(h,e):{},g=Object.keys(b).length>0,{colors:v,colorsDark:f}=r[p],y=null!==(a=e?f:v)&&void 0!==a?a:v;if((y||i)&&(b.colors={...y,...i,...b.colors}),!Object.keys(b).length)return{palette:m};const _=y?{baseColors:y}:{};return p===o&&(!i&&!g)?{palette:m,options:b,..._,shipped:e?"dark":"light"}:{palette:m,options:b,..._}}},20386(t,e,i){i(65649),i(16286),i(47399),i(14167),i(70705);const a={"--ha-color-map-land":["background","land"],"--ha-color-map-water":["water"],"--ha-color-map-green":["naturePark","natureWood","natureGrass","natureLeisure","natureWetland","siteSports"],"--ha-color-map-area":["areaResidential","areaCommercial","areaIndustrial","areaWaste","areaBurial","siteParking","natureAgriculture","natureSand","natureRock"],"--ha-color-map-building":["building"],"--ha-color-map-building-outline":["buildingBg"],"--ha-color-map-road":["roadStreet"],"--ha-color-map-road-major":["roadMotorway","roadTrunk"],"--ha-color-map-road-outline":["roadStreetBg","roadTrunkBg","roadMotorwayBg"],"--ha-color-map-transit":["transitRail","transitSubway","transitCycle","transitFoot"],"--ha-color-map-boundary":["boundary","boundaryDisputed"],"--ha-color-map-label":["label"],"--ha-color-map-label-halo":["labelHalo"],"--ha-color-map-label-secondary":["labelSymbol","labelPoi","labelHousenumber"]},o={siteSports:.15,labelHalo:.8,labelPoi:.4,labelHousenumber:.3},r=/^#([0-9a-f]{3,8})$/i,n=/^rgba?\(([^)]+)\)$/i,s=/^color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\s*\)$/i,l=t=>{const e=t.match(r);if(e){const t=e[1],i=3===t.length||4===t.length,a=e=>i?parseInt(t[e]+t[e],16):parseInt(t.slice(2*e,2*e+2),16);if(3===t.length||4===t.length||6===t.length||8===t.length){const e=4===t.length||8===t.length?a(3)/255:1;return[a(0),a(1),a(2),e]}return}const i=t.match(n);if(i){var a;const t=i[1].split(/[,\s/]+/).filter(Boolean).map(Number);if(t.length<3||t.slice(0,3).some(Number.isNaN))return;return[t[0],t[1],t[2],null!==(a=t[3])&&void 0!==a?a:1]}const o=t.match(s);if(o){var l;const t=t=>Math.round(255*Number(t));return[t(o[1]),t(o[2]),t(o[3]),Number(null!==(l=o[4])&&void 0!==l?l:1)]}},d=[1,2,3,1],c=(t,e)=>{const i=document.createElement("span");i.style.cssText="display:none;color:rgb(1, 2, 3)";const a=document.createElement("span");a.style.color=`var(${e})`,i.append(a),t.append(i);const o=l(getComputedStyle(a).color);return i.remove(),o&&o.every((t,e)=>t===d[e])?void 0:o};i.d(e,{},{Q:t=>{const e=getComputedStyle(t);let i;for(const[s,d]of Object.entries(a)){var r;const a=e.getPropertyValue(s).trim();if(!a)continue;const h=null!==(r=l(a))&&void 0!==r?r:c(t,s);if(!h)continue;null!=i||(i={});const[u,p,m,b]=h;for(const t of d){var n;const e=Math.round(b*(null!==(n=o[t])&&void 0!==n?n:1)*1e3)/1e3;i[t]=`rgba(${u},${p},${m},${e})`}}return i}})},10096(t,e,i){i(99260),i(65649),i(47399),i(62922);const a="haMapA11y",o=t=>{const e=t.dataset[a];void 0!==e&&(e.split(" ").filter(Boolean).forEach(e=>t.removeAttribute(e)),delete t.dataset[a])};i.d(e,{},{I:o,l:(t,e,i)=>{o(t);const r=[];!e||t.hasAttribute("aria-label")||t.hasAttribute("aria-labelledby")||(t.setAttribute("aria-label",e),r.push("aria-label")),t.hasAttribute("role")||(i?(t.setAttribute("role","button"),r.push("role")):e?(t.setAttribute("role","img"),r.push("role")):(t.setAttribute("aria-hidden","true"),r.push("aria-hidden"))),i&&!t.hasAttribute("tabindex")&&(t.tabIndex=0,r.push("tabindex")),t.dataset[a]=r.join(" ")}})},33853(t,e,i){var a=i(47424),o=i.n(a);i.d(e,{},{D:t=>o()(t,{whiteList:{},stripIgnoreTag:!0,stripIgnoreTagBody:!0})})},12734(t,e,i){i.a(t,async function(t,a){try{var o=i(50026),r=i(70341),n=i(19266),s=i(3284),l=i(98088),d=i(88558),c=i(5732),h=t([c]);c=(h.then?(await h)():h)[0];const u=1.25,p=12,m=Math.round(p*Math.SQRT2/2),b=4,g=10,v=(t,e)=>{const i=e?Math.round(t*u):t,a=i+m+b+g;return{size:[i,a],anchor:[i/2,a-g/2]}};class f extends r.WF{render(){return r.qy` <div part="marker" class="marker ${this.entityPicture?"picture":""}" style=${(0,s.W)({"--ha-marker-selected-color":this.entityColor})};> ${this.entityPicture?r.qy`<div part="picture" class="entity-picture" style=${(0,s.W)({"background-image":`url(${this.entityPicture})`})};></div>`:this.showIcon&&this.entityId?r.qy`<ha-state-icon .stateObj=${this._stateObj}></ha-state-icon>`:this.entityUnit?r.qy` ${this.entityName} <span class="unit" style="display:${this.entityUnit?"initial":"none"}">${this.entityUnit}</span> `:this.entityName} </div> ${this.floating?r.qy`<div class="tail"></div> <div class="dot"></div>`:r.s6} `}connectedCallback(){super.connectedCallback(),this.addEventListener("click",this._badgeTap),this.addEventListener("keydown",this._handleKeydown)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("click",this._badgeTap),this.removeEventListener("keydown",this._handleKeydown)}constructor(...t){super(...t),this.showIcon=!1,this.selected=!1,this.floating=!1,this._handleKeydown=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._badgeTap(t))},this._badgeTap=t=>{t.stopPropagation(),this.entityId&&(0,d.r)(this,"hass-more-info",{entityId:this.entityId})}}}f.styles=r.AH`:host([floating]){filter:var(--ha-cluster-shadow,drop-shadow(0 1px 3px #0000001f));pointer-events:none;flex-direction:column;align-items:center;display:flex}:host([floating]) .marker,:host([floating]) .tail{pointer-events:auto}:host([floating]) .marker{z-index:1;position:relative}.marker{text-align:center;box-sizing:border-box;width:var(--ha-marker-size,48px);height:var(--ha-marker-size,48px);font-size:var(--ha-marker-font-size,var(--ha-font-size-xl));border-radius:var(--ha-picture-border-radius);border:var(--ha-marker-border-width,3px) solid var(--ha-marker-color,var(--card-background-color,#fff));color:var(--primary-text-color);background-color:var(--ha-marker-background,var(--card-background-color));justify-content:center;align-items:center;display:flex}.marker.picture{overflow:hidden}:host([selected]) .marker{width:calc(var(--ha-marker-size,48px) * var(--ha-marker-selected-scale,${u}));height:calc(var(--ha-marker-size,48px) * var(--ha-marker-selected-scale,${u}))}:host([selected]:not([floating])) .marker{outline:3px solid var(--ha-marker-selected-color,var(--primary-color))}.tail{width:${p}px;height:${p}px;margin-top:${-p/2}px;margin-bottom:${m-p/2}px;background:var(--ha-marker-color,var(--card-background-color,#fff));border-radius:2px;transform:rotate(45deg)}.dot{width:${g}px;height:${g}px;margin-top:${b}px;background:var(--ha-marker-color,var(--card-background-color,#fff));border-radius:50%}:host(:not([selected])) .dot{visibility:hidden}.entity-picture{background-size:cover;width:100%;height:100%}.unit{margin-left:2px}`,(0,o.Cg)([(0,n.MZ)({attribute:"entity-id",reflect:!0})],f.prototype,"entityId",void 0),(0,o.Cg)([(0,n.wk)(),(0,l.fI)({entityIdPath:["entityId"]})],f.prototype,"_stateObj",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"entity-name"})],f.prototype,"entityName",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"entity-unit"})],f.prototype,"entityUnit",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"entity-picture"})],f.prototype,"entityPicture",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"entity-color"})],f.prototype,"entityColor",void 0),(0,o.Cg)([(0,n.MZ)({attribute:"show-icon",type:Boolean})],f.prototype,"showIcon",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],f.prototype,"selected",void 0),(0,o.Cg)([(0,n.MZ)({type:Boolean,reflect:!0})],f.prototype,"floating",void 0),f=(0,o.Cg)([(0,n.EM)("ha-entity-marker")],f),i.d(e,{},{i:v}),a()}catch(t){a(t)}})},39960(t,e,i){i.a(t,async function(t,a){try{i(31882),i(19945),i(99260),i(65649),i(47399),i(62922),i(14167),i(70705),i(70425),i(63145),i(9336),i(79846),i(80815),i(34950),i(45453),i(29170),i(15740);var o=i(50026),r=i(87253),n=i(70341),s=i(19266),l=i(18618),d=i(79271),c=i(56468),h=i(36055),u=(i(62517),i(40533)),p=i(88558),m=i(55702),b=i(84032),g=i(15114),v=i(74284),f=i(62269),y=i(20386),_=i(2064),k=i(74976),w=i(10096),M=i(50592),x=i(40308),z=i(33853),C=i(97403),E=i(70728),P=i(15651),L=i(7830),S=i(12734),A=t([L,c,h,S]);[L,c,h,S]=A.then?(await A)():A;const F=250,$=3e3,H=t=>"string"==typeof t?t:t.entity_id,T=["name","state","attribute","icon"],Z=(t,e)=>{var i,a,o,r;return t.element===e.element&&t.title===e.title&&t.color===e.color&&t.locationEditable===e.locationEditable&&t.radiusEditable===e.radiusEditable&&t.activatable===e.activatable&&(null===(i=t.elementSize)||void 0===i?void 0:i[0])===(null===(a=e.elementSize)||void 0===a?void 0:a[0])&&(null===(o=t.elementSize)||void 0===o?void 0:o[1])===(null===(r=e.elementSize)||void 0===r?void 0:r[1])},R=t=>({addDraggableMarker:(e,i,a)=>{let o=i,r=t.addMarker(e,o,a);return{get location(){return o},clusterData:a.clusterData,setLocation:i=>{r.remove(),o=i,r=t.addMarker(e,o,a)},remove:()=>r.remove()}},addEditableCircle:(e,i)=>{var a;const o=null!==(a=i.centerElement)&&void 0!==a?a:document.createElement("div");let r;if(i.centerElement||(o.className="editable-circle-center"),i.onClick){const t=t=>{t.stopPropagation(),i.onClick()},e=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),i.onClick())};o.addEventListener("click",t),o.addEventListener("keydown",e),r=()=>{o.removeEventListener("click",t),o.removeEventListener("keydown",e)}}let n={center:e,radius:i.radius},s=[];const l=()=>{var e;s=[t.addCircle(n.center,{radius:n.radius,color:i.color}),t.addMarker(o,n.center,{size:null!==(e=i.centerSize)&&void 0!==e?e:[16,16],interactive:!!i.onClick,title:i.title,nativeTitle:i.nativeTitle})]};return l(),{get center(){return n.center},get radius(){return n.radius},update:(t,e)=>{s.forEach(t=>t.remove()),n={center:t,radius:e},l()},remove:()=>{var t;null===(t=r)||void 0===t||t(),s.forEach(t=>t.remove())}}}}),I=32,B=6,D=4,O=12,N=4,j=28,W=99,U=10,V=Math.round(U*Math.SQRT2/2),q=2,G=40,K=160,X=2.5,Q=10,J=t=>{const e=t.replace(".","-");return`marker, picture, marker: marker-${e}, picture: picture-${e}`},Y=(t,e,i=!0)=>{const a=e&&i?t.get(e):void 0;if(a&&!a.isConnected)return a;const o=document.createElement("ha-entity-marker");return e&&(o.setAttribute("exportparts",J(e)),t.set(e,o)),o};class tt extends n.mN{connectedCallback(){this._pauseAutoFit=!1,document.addEventListener("visibilitychange",this._handleVisibilityChange),this._handleVisibilityChange(),super.connectedCallback(),this._loadMap(),this._attachObserver()}_watchRegistry(){var t;!this._registryConsumer&&null!==(t=this.entities)&&void 0!==t&&t.length&&(this._registryConsumer=new d.TH(this,C.ih,t=>{this._entityReg=t}))}disconnectedCallback(){var t,e;super.disconnectedCallback(),document.removeEventListener("visibilitychange",this._handleVisibilityChange),null===(t=this._engine)||void 0===t||t.destroy(),this._engine=void 0,this._setupAttempt++,null===(e=this._startingEngine)||void 0===e||e.destroy(),this._startingEngine=void 0,this._loading=!1,clearTimeout(this._drawnFallback),this._entityHandles=[],this._entityMarkers.clear(),this._clusterAvatars.clear(),this._zoneHandles=[],this._zoneCircleHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}update(t){var e,i;if(super.update(t),!this._loaded)return;let a=!1;const o=t.get("_states");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),a=!this._pauseAutoFit;else if(this._loaded&&o&&this.entities)for(const t of this.entities){const e=H(t),i=this._states[e],r=null==i?void 0:i.attributes.in_zones;if(o[e]!==i||i&&["person","device_tracker"].includes((0,m.t)(i))&&Array.isArray(r)&&r.some(t=>o[t]!==this._states[t])){this._drawEntities(),a=!this._pauseAutoFit;break}}var r;((t.has("clusterMarkers")||t.has("_entityReg")||t.has("_formatters"))&&this._drawEntities(),t.has("fitPadding")&&!(0,x.b)(t.get("fitPadding"),this.fitPadding)&&(a=!this._pauseAutoFit),t.has("zoomPosition"))&&(null===(r=this._engine)||void 0===r||r.setZoomControlPosition(this.zoomPosition));const n=t.get("_config");if((t.has("_loaded")||t.has("scaleRuler")||t.has("_config")&&(null==n||null===(e=n.unit_system)||void 0===e?void 0:e.length)!==(null===(i=this._config)||void 0===i||null===(i=i.unit_system)||void 0===i?void 0:i.length))&&this._drawScaleRuler(),t.has("_loaded")||t.has("paths")){var s;this._drawPaths();const e=t.get("paths");var l;if(!(null==e||!e.length)!=!(null===(s=this.paths)||void 0===s||!s.length))null===(l=this._engine)||void 0===l||l.refreshClusters()}var d;(t.has("_loaded")||t.has("editableLocations")?this._drawEditableLocations()&&(a=!0):t.has("_i18n")&&this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()),t.has("_loaded")&&this._pendingFit?this._runPendingFit():(t.has("_loaded")||this.autoFit&&a)&&this.fitMap(),t.has("zoom")&&this._withProgrammaticFit(()=>{this._engine.setZoom(this.zoom)}),t.has("mapStyle"))&&(null===(d=this._engine)||void 0===d||d.setMapStyle(this._resolvedMapStyle));const c=t.get("_ui");(t.has("themeMode")||t.has("_ui")&&(!c||c.themes!==this._ui.themes))&&(this._updateMapAppearance(),this._drawEntities(),this._drawPaths(),this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()))}get _darkMode(){var t;return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(null===(t=this._ui)||void 0===t||null===(t=t.themes)||void 0===t?void 0:t.darkMode)}_readThemeColors(){var t;const e=Boolean(null===(t=this._ui)||void 0===t||null===(t=t.themes)||void 0===t?void 0:t.darkMode),i=this._darkMode===e?(0,y.Q)(this):void 0;(0,x.b)(i,this._themeColors)||(this._themeColors=i)}get _resolvedMapStyle(){return this._resolveMapStyle(this.mapStyle,this._darkMode,this._themeColors)}_updateMapAppearance(){var t;this._readThemeColors();const e=this._mapElement;e&&(e.classList.toggle("clickable",this.clickable),e.classList.toggle("dark",this._darkMode),e.classList.toggle("drawn",this._mapDrawn),e.classList.toggle("space",this._vectorEngine&&this._mapDrawn),e.classList.toggle("forced-dark","dark"===this.themeMode),e.classList.toggle("forced-light","light"===this.themeMode),null===(t=this._engine)||void 0===t||t.setMapStyle(this._resolvedMapStyle))}_markDrawn(t){t!==this._setupAttempt||this._mapDrawn||(clearTimeout(this._drawnFallback),this._mapDrawn=!0,this._updateMapAppearance())}get _vectorEngine(){return!this._forceLeaflet&&(0,g.jV)()}async _createEngine(){if(!this._vectorEngine){return new((await Promise.all([i.e(84259),i.e(62093)]).then(i.bind(i,56956))).LeafletMapEngine)}return new((await i.e(19404).then(i.bind(i,13895))).MapLibreMapEngine)}async _loadMap(){const t=this._forceLeaflet||!(0,g.jV)();try{await this._setUpEngine()}catch(e){if(!this.isConnected)return;if(t)throw e;this._forceLeaflet=!0,await this._loadMap()}}async _setUpEngine(){var t;if(this._loading)return;null===(t=this.shadowRoot.getElementById("map"))||void 0===t||t.remove();const e=document.createElement("div");e.id="map",e.classList.toggle("dark",this._darkMode),this.shadowRoot.append(e),this._loading=!0,this._mapDrawn=!1,clearTimeout(this._drawnFallback);const i=++this._setupAttempt;let a;try{var o,r,n,s;const t=this._connection?await(0,P.pW)(this._connection.connection):void 0;this._readThemeColors();const l=this._forceLeaflet;if(a=await this._createEngine(),i!==this._setupAttempt)return;if(this._startingEngine=a,this._drawnFallback=window.setTimeout(()=>this._markDrawn(i),$),await a.init(e,{center:[null!==(o=null===(r=this._config)||void 0===r?void 0:r.latitude)&&void 0!==o?o:52.3731339,null!==(n=null===(s=this._config)||void 0===s?void 0:s.longitude)&&void 0!==n?n:4.8903147],zoom:this.zoom,mapStyle:this._resolvedMapStyle,token:t,rasterOnly:this._forceLeaflet,zoomControlPosition:this.zoomPosition,events:{click:t=>this._handleEngineClick(t),zoomStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},moveStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},fatal:()=>this._handleEngineFatal(),drawn:()=>this._markDrawn(i)}}),!this.isConnected||i!==this._setupAttempt)return;if(this._forceLeaflet&&!l)throw new Error("Map engine failed during setup");this._engine=a,this._updateMapAppearance(),this._loaded=!0,(0,p.r)(this,"editing-available-changed",{available:!!a.editing})}finally{i===this._setupAttempt&&(this._loading=!1,this._startingEngine=void 0),a&&a!==this._engine&&a.destroy()}}_handleEngineFatal(){var t,e;this._forceLeaflet||(this._forceLeaflet=!0,this._loading?null===(e=this._startingEngine)||void 0===e||e.destroy():(null===(t=this._engine)||void 0===t||t.destroy(),this._engine=void 0,this._entityHandles=[],this._zoneHandles=[],this._zoneCircleHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._loadMap()))}_handleEngineClick(t){0===this._clickCount&&setTimeout(()=>{1===this._clickCount&&(0,p.r)(this,"map-clicked",{location:t}),this._clickCount=0},250),this._clickCount++}_withProgrammaticFit(t){this._isProgrammaticFit=!0,t(),setTimeout(()=>{this._isProgrammaticFit=!1},F)}fitMap(t){var e,i;if(null!=t&&t.unpause_autofit&&(this._pauseAutoFit=!1),!this._engine||!this._config)return;if(this._deferIfUnsized(()=>this.fitMap(t)))return;const a=this.fitZones||!this._focusPoints.length?this._focusZonePoints:[];if(!(this._focusPoints.length||a.length||null!==(e=this.editableLocations)&&void 0!==e&&e.length))return this._withProgrammaticFit(()=>{this._engine.setView([this._config.latitude,this._config.longitude],(null==t?void 0:t.zoom)||this.zoom)}),void(this._hasFitted=!0);const o=[...this._focusPoints,...a],r=null!==(i=this.editableLocations)&&void 0!==i?i:[],n=r.filter(t=>!1!==t.fit);(n.length?n:r).forEach(t=>{t.radius?o.push(...(0,v.Rn)(t.location,t.radius)):o.push(t.location)}),this._withProgrammaticFit(()=>{var e,i;this._engine.fitBounds(o,{maxZoom:(null==t?void 0:t.zoom)||this.zoom,pad:null!==(e=null==t?void 0:t.pad)&&void 0!==e?e:.5,padding:null!==(i=null==t?void 0:t.padding)&&void 0!==i?i:this.fitPadding,animate:this._hasFitted})}),this._hasFitted=!0}_deferIfUnsized(t){return this._engine.hasUsableSize()?(this._pendingFit=void 0,!1):(this._pendingFit=t,!0)}_runPendingFit(){if(this._pendingFit&&this._engine&&this._engine.hasUsableSize()){const t=this._pendingFit;this._pendingFit=void 0,t()}}panTo(t){var e;null===(e=this._engine)||void 0===e||e.panTo(t)}containsLocation(t){var e,i;return null!==(e=null===(i=this._engine)||void 0===i?void 0:i.containsLocation(t))&&void 0!==e&&e}setView(t,e){this._engine?(this._pendingFit=void 0,this._engine.setView(t,e)):this._pendingFit=()=>this.setView(t,e)}getView(){var t;return null===(t=this._engine)||void 0===t?void 0:t.getView()}fitBounds(t,e){this._pauseAutoFit=!0,this._engine?this._deferIfUnsized(()=>this.fitBounds(t,e))||(this._withProgrammaticFit(()=>{var i;this._engine.fitBounds(t,{maxZoom:(null==e?void 0:e.zoom)||this.zoom,pad:null!==(i=null==e?void 0:e.pad)&&void 0!==i?i:.5,animate:this._hasFitted,padding:null==e?void 0:e.padding,fly:null==e?void 0:e.fly})}),this._hasFitted=!0):this._pendingFit=()=>this.fitBounds(t,e)}_drawEditableLocations(){var t,e;const i=this._engine;if(!i)return!1;const a=R(i),o=null!==(t=i.editing)&&void 0!==t?t:a,r=new Set((null!==(e=this.editableLocations)&&void 0!==e?e:[]).map(t=>t.id));let n=!1;for(const[t,e]of this._editableHandles){var s;if(!r.has(t))null===(s=e.cleanup)||void 0===s||s.call(e),e.handle.remove(),this._editableHandles.delete(t),n=!0}if(!this.editableLocations)return n;const l=getComputedStyle(this).getPropertyValue("--accent-color");for(const t of this.editableLocations){var d,c,h,u;const{id:e}=t,i=null!==(d=t.title)&&void 0!==d?d:null===(c=this._i18n)||void 0===c?void 0:c.localize("ui.components.map.location"),r=!!t.element&&!!t.title,s=this._editableHandles.get(e),v=t.radius?"circle":"marker";if(s&&s.kind===v&&Z(s.source,t)){"circle"===s.kind?s.handle.update(t.location,t.radius):s.handle.setLocation(t.location),s.source=t;continue}var m;if(s)null===(m=s.cleanup)||void 0===m||m.call(s),s.handle.remove();else n=!0;if("circle"===v){var b,g;const a=o.addEditableCircle(t.location,{radius:t.radius,color:t.color||l,centerElement:t.element,centerSize:t.elementSize,title:i,nativeTitle:!r,moveable:t.locationEditable,resizable:t.radiusEditable,resizeLabel:t.title?null===(b=this._i18n)||void 0===b?void 0:b.localize("ui.components.map.radius_of",{name:t.title}):null===(g=this._i18n)||void 0===g?void 0:g.localize("ui.components.map.radius"),onMove:t=>(0,p.r)(this,"editable-location-moved",{id:e,location:t}),onResize:t=>(0,p.r)(this,"editable-location-resized",{id:e,radius:t}),onClick:t.activatable?()=>(0,p.r)(this,"editable-location-clicked",{id:e}):void 0});this._editableHandles.set(e,{kind:v,source:t,handle:a,cleanup:r?this._attachTooltip(t.element,t.title):void 0});continue}const f=null!==(h=t.element)&&void 0!==h?h:document.createElement("div");t.element||(f.className="editable-circle-center");let y,_=!1;if(t.activatable){const t=()=>{_=!1},i=t=>{t.stopPropagation(),_||(0,p.r)(this,"editable-location-clicked",{id:e})},a=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),(0,p.r)(this,"editable-location-clicked",{id:e}))};f.addEventListener("pointerdown",t),f.addEventListener("click",i),f.addEventListener("keydown",a),y=()=>{f.removeEventListener("pointerdown",t),f.removeEventListener("click",i),f.removeEventListener("keydown",a)}}const k=(t.locationEditable?o:a).addDraggableMarker(f,t.location,{size:null!==(u=t.elementSize)&&void 0!==u?u:[16,16],interactive:!0,focusable:!!t.activatable,title:i,nativeTitle:!r,onDragEnd:t=>{_=!0,(0,p.r)(this,"editable-location-moved",{id:e,location:t})}}),w=r?this._attachTooltip(t.element,t.title):void 0;this._editableHandles.set(e,{kind:v,source:t,cleanup:()=>{var t;null===(t=y)||void 0===t||t(),null==w||w()},handle:k})}return n}_attachTooltip(t,e){t.id||(t.id="ha-map-editable-"+this._tooltipCount++);const i=document.createElement("ha-tooltip");return i.for=t.id,i.textContent=e,this.shadowRoot.append(i),()=>i.remove()}_removeEditableLocations(){for(const e of this._editableHandles.values()){var t;null===(t=e.cleanup)||void 0===t||t.call(e),e.handle.remove()}this._editableHandles.clear()}_computePathTooltip(t,e){var i;let a;return a=t.fullDatetime?(0,c.r6)(e.timestamp,this._i18n.locale,this._config):(0,r.c)(e.timestamp)?(0,h.ie)(e.timestamp,this._i18n.locale,this._config):(0,h.Xs)(e.timestamp,this._i18n.locale,this._config),`${(0,z.D)(null!==(i=t.name)&&void 0!==i?i:"")}<br>${a}`}_drawPaths(){var t;if(!this._i18n||!this._config||!this._engine)return;const e=null!==(t=this.paths)&&void 0!==t?t:[];if(this._pathHandles.splice(e.length).forEach(t=>t.remove()),!e.length)return;const i=getComputedStyle(this).getPropertyValue("--dark-primary-color");e.forEach((t,e)=>{let a,o;t.gradualOpacity&&(a=t.gradualOpacity/(t.points.length-2),o=1-t.gradualOpacity);const r=[],n=[];for(let e=0;e<t.points.length-1;e++){const i=t.gradualOpacity?o+e*a:void 0,s=t.points[e],l=t.points[e+1];if(n.push({location:s.point,opacity:i,tooltipHtml:this._computePathTooltip(t,s)}),Math.abs(s.point[1]-l.point[1])<=180)r.push({points:[s.point,l.point],opacity:i});else{const t=(l.point[1]-s.point[1]+540)%360-180;let e;e=0===t?(s.point[0]+l.point[0])/2:s.point[0]+(l.point[0]-s.point[0])*(s.point[1]>0?180-s.point[1]:-180-s.point[1])/t;const a=[e,s.point[1]>0?180:-180],o=[e,l.point[1]>0?180:-180];r.push({points:[s.point,a],opacity:i}),r.push({points:[o,l.point],opacity:i})}}const s=t.points.length-1;if(s>=0){const e=t.gradualOpacity?o+s*a:void 0;n.push({location:t.points[s].point,opacity:e,tooltipHtml:this._computePathTooltip(t,t.points[s])})}const l={color:t.color||i,segments:r,markers:n},d=this._pathHandles[e];d?d.update(l):this._pathHandles.push(this._engine.addPath(l))})}_drawEntities(){const t=this._states,e=this._engine;if(!t||!e||!this._formatters)return;this._entityHandles.forEach(t=>t.remove()),this._entityHandles=[],this._focusPoints=[],this._zoneHandles.forEach(t=>t.remove()),this._zoneHandles=[],this._focusZonePoints=[];let i=0;if(!this.entities)return this._zoneCircleHandles.splice(0).forEach(t=>t.remove()),this._entityMarkers.clear(),this._clusterAvatars.clear(),void e.setClustering(null);this._watchRegistry();const a=getComputedStyle(this);this._zonePositions={},this._zoneRadii={};for(const e of this.entities){const i=t[H(e)];!i||"zone"!==(0,m.t)(i)||!this.renderPassive&&i.attributes.passive||"number"==typeof i.attributes.latitude&&"number"==typeof i.attributes.longitude&&(this._zonePositions[i.entity_id]=[i.attributes.latitude,i.attributes.longitude],"number"==typeof i.attributes.radius&&(this._zoneRadii[i.entity_id]=i.attributes.radius))}const o=new Set;for(const s of this.entities){var r,n;const l=t[H(s)];if(!l)continue;const d="string"!=typeof s?s.name:void 0,c=null!=d?d:this._formatters.formatEntityName(l),{passive:h,icon:u,radius:g,entity_picture:f}=l.attributes,y=(0,b.H)(l,t);if(!y)continue;const{latitude:_,longitude:w,gpsAccuracy:x}=y,z=[_,w];if("zone"===(0,m.t)(l)){if(h&&!this.renderPassive)continue;const t="string"!=typeof s&&s.hide_radius,o=!h&&"string"!=typeof s&&s.color?s.color:(0,k.YG)(l.entity_id,!!h,this._entityReg,a);if(!t&&g){const t={radius:g,color:o},a=this._zoneCircleHandles[i];a?a.update(z,t):this._zoneCircleHandles.push(e.addCircle(z,t)),i++}const r=(0,M.x5)({color:o,icon:u,name:c});if(this.interactiveZones){const t=t=>{t.stopPropagation(),(0,p.r)(this,"hass-more-info",{entityId:l.entity_id})};r.addEventListener("click",t),r.addEventListener("keydown",e=>{"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),t(e))})}this._zoneHandles.push(e.addMarker(r,z,{size:[36,36],interactive:this.interactiveZones,title:c})),"string"!=typeof s&&!1===s.focus||(!t&&g?this._focusZonePoints.push(...(0,v.Rn)(z,g)):this._focusZonePoints.push(z));continue}const C="string"!=typeof s&&"state"===s.label_mode?this._formatters.formatEntityState(l):"string"!=typeof s&&"attribute"===s.label_mode&&void 0!==s.attribute?this._formatters.formatEntityAttributeValue(l,s.attribute):null!=d?d:c.split(" ").map(t=>t[0]).join("").substr(0,3),P=H(s),L=Y(this._entityMarkers,P,!o.has(P));o.add(P),L.showIcon="string"!=typeof s&&"icon"===s.label_mode,L.entityId=P,L.entityName=C,L.entityUnit="string"!=typeof s&&s.unit&&"attribute"===s.label_mode?s.unit:"",L.entityPicture=!f||"string"!=typeof s&&s.label_mode?"":this._connection.hassUrl(f);const A=("string"!=typeof s?s.color:void 0)||(0,k.lb)(P,this._entityReg,a);let F;if(L.entityColor=A,L.selected="string"!=typeof s&&null!==(r=s.selected)&&void 0!==r&&r,L.floating=!0,["person","device_tracker"].includes((0,m.t)(l))){const e=l.attributes.in_zones;if(Array.isArray(e)&&e.length>0){const i=(0,b._)(e,t);i&&this._zonePositions[i.entity_id]&&(F=i.entity_id)}else Array.isArray(e)&&["not_home",E.HV,E.Hh].includes(l.state)||(F=this._zoneContaining(z,x))}const $={entityId:P,title:c,picture:L.entityPicture||void 0,label:C,showIcon:L.showIcon,unit:null!==(n=L.entityUnit)&&void 0!==n?n:"",color:A,selected:L.selected,zoneId:F},T=x||(L.selected?X:0),Z=T>0&&!("string"!=typeof s&&s.hide_accuracy);this._entityHandles.push(e.addMarker(L,z,{...(0,S.i)(this._getMarkerSize(a),L.selected),title:c,cluster:!L.selected,raised:L.selected,clusterData:$,decoration:Z?{radius:T,color:A,outline:T>Q}:void 0})),"string"!=typeof s&&!1===s.focus||this._focusPoints.push(z)}this._zoneCircleHandles.splice(i).forEach(t=>t.remove());const s=new Set(this.entities.map(H));for(const t of[this._entityMarkers,this._clusterAvatars])for(const e of t.keys())s.has(e)||t.delete(e);e.setClustering(this.clusterMarkers?{radius:G,iconBuilder:this._createClusterBubble,groupKey:t=>{var e;return null===(e=t.clusterData)||void 0===e?void 0:e.zoneId},groupRadius:K}:null)}_zoneContaining(t,e=0){let i,a=1/0,o=1/0;for(const[n,s]of Object.entries(this._zoneRadii)){var r;if(null!==(r=this._states[n])&&void 0!==r&&r.attributes.passive)continue;const l=(0,v.S_)(t,this._zonePositions[n]);l-e<s&&(s<a||s===a&&l<o)&&(i=n,a=s,o=l)}return i}_drawScaleRuler(){var t,e;null===(t=this._engine)||void 0===t||t.setScaleRuler(this.scaleRuler?{metric:"km"===(null===(e=this._config)||void 0===e||null===(e=e.unit_system)||void 0===e?void 0:e.length)}:null)}_getMarkerSize(t){const e=t.getPropertyValue("--ha-marker-size"),i=parseFloat(e);return Number.isNaN(i)?48:i}async _attachObserver(){this._resizeObserver||(this._resizeObserver=new ResizeObserver(()=>{var t;null===(t=this._engine)||void 0===t||t.invalidateSize(),this._runPendingFit()})),this._resizeObserver.observe(this)}constructor(...t){super(...t),this.clickable=!1,this.autoFit=!1,this.renderPassive=!1,this.interactiveZones=!1,this.fitZones=!1,this.zoomPosition="topleft",this._zonePositions={},this._zoneRadii={},this.themeMode="auto",this.zoom=14,this.clusterMarkers=!0,this.scaleRuler=!1,this._loaded=!1,this._editableHandles=new Map,this._entityReg=[],this._entityHandles=[],this._tooltipCount=0,this._entityMarkers=new Map,this._clusterAvatars=new Map,this._zoneHandles=[],this._zoneCircleHandles=[],this._pathHandles=[],this._focusPoints=[],this._focusZonePoints=[],this._clickCount=0,this._isProgrammaticFit=!1,this._pauseAutoFit=!1,this._handleVisibilityChange=async()=>{document.hidden||setTimeout(()=>{this._pauseAutoFit=!1},500)},this._resolveMapStyle=(0,l.A)(f.kR),this._mapDrawn=!1,this._loading=!1,this._forceLeaflet=!1,this._setupAttempt=0,this._hasFitted=!1,this._createClusterBubble=(t,e,i,a=!1)=>{var o;const r=t.map(t=>t.clusterData),n=a||r.length<=N?r:r.slice(0,N-1),s=r.length-n.length,l=!(null===(o=this.paths)||void 0===o||!o.length),d=document.createElement("div");d.className="cluster-bubble";const c=new Set;for(const t of n){var h,u,p,m,b,g;const e=Y(this._clusterAvatars,null==t?void 0:t.entityId,!c.has(null!==(h=null==t?void 0:t.entityId)&&void 0!==h?h:""));var v;if(null!=t&&t.entityId&&c.add(t.entityId),e.entityId=null==t?void 0:t.entityId,e.entityName=null!==(u=null==t?void 0:t.label)&&void 0!==u?u:"",e.entityUnit=null!==(p=null==t?void 0:t.unit)&&void 0!==p?p:"",e.showIcon=null!==(m=null==t?void 0:t.showIcon)&&void 0!==m&&m,e.entityPicture=null!==(b=null==t?void 0:t.picture)&&void 0!==b?b:"",e.entityColor=null==t?void 0:t.color,l)e.style.setProperty("--ha-marker-color",null!==(v=null==t?void 0:t.color)&&void 0!==v?v:"var(--primary-color)"),e.style.setProperty("--ha-marker-border-width","2px");else e.style.removeProperty("--ha-marker-color"),e.style.removeProperty("--ha-marker-border-width");e.selected=null!==(g=null==t?void 0:t.selected)&&void 0!==g&&g,(0,w.I)(e),a&&(0,w.l)(e,null==t?void 0:t.title,!0),d.appendChild(e)}const f=a?Math.max(1,Math.floor((this.offsetWidth-2*O-2*B+D)/(I+D))):n.length,y=Math.min(n.length,f),_=Math.ceil(n.length/f);let k=y*I+(y-1)*D+2*B;if(s>0){const t=document.createElement("span");t.className="more",t.textContent=s>W?`${W}+`:`+${s}`,d.appendChild(t),k+=j+D}const M=_*I+(_-1)*D+2*B+V,x=document.createElement("div");x.className="cluster-marker";const z=document.createElement("div");z.className="cluster-bubble-tail",x.append(d,z);const C=i?this._zonePositions[i]:void 0;return{element:x,size:[k,M],location:C,anchor:[k/2,M+(C?18+q:9)]}}}}tt.styles=n.AH`
    :host {
      display: block;
      height: 300px;
    }
    #map {
      height: 100%;
      /* The map arrives in one piece: the container carries the cartography's
         own ground, and fades in with the markers once a frame is drawn */
      background-color: #f4efe6;
      /* Hidden rather than transparent: the controls and markers in here are
         not to be clicked or tabbed to before they are on screen */
      visibility: hidden;
      opacity: 0;
      transition: opacity var(--ha-animation-duration-fast, 150ms) ease-in;
      /* A cluster bubble and its tail cast a single shadow around their
         combined silhouette (drop-shadow on the wrapper), so no shadow seam
         appears between the bubble and its tail. */
      --ha-cluster-shadow: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.08))
        drop-shadow(0 1px 3px rgba(0, 0, 0, 0.12));
    }
    #map.drawn {
      visibility: visible;
      opacity: 1;
    }
    #map.clickable {
      cursor: pointer;
    }
    .maplibregl-marker {
      transition:
        opacity var(--ha-animation-duration-fast),
        visibility var(--ha-animation-duration-fast);
    }
    .maplibregl-marker-covered {
      visibility: hidden;
      pointer-events: none;
    }
    /* A zone fades in once the bubble over it is opaque, not through it */
    .zone-circle:not(.maplibregl-marker-covered) {
      transition-delay: var(--ha-animation-duration-fast);
    }
    #map.dark {
      background: #191b2c;
      --ha-cluster-shadow: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.4))
        drop-shadow(0 1px 3px rgba(0, 0, 0, 0.5));
    }
    #map.forced-dark {
      color: #ffffff;
      --map-filter: invert(0.9) hue-rotate(170deg) brightness(1.5) contrast(1.2)
        saturate(0.3);
    }
    #map.forced-light {
      background: #ffffff;
      color: #000000;
      --map-filter: invert(0);
    }
    /* Zoomed out the sky fades out and the globe is left on a transparent
       canvas, so what surrounds it is this element. The same sky in both
       themes, day or night: a glow where the sphere sits at the widest zoom
       out -- MapLibre's own atmosphere carries the edge from there in -- over
       a gradient that lightens towards the top. */
    #map.space {
      --ha-map-space-glow: rgba(255, 255, 255, 0.95);
      --ha-map-space-haze: rgba(255, 255, 255, 0.45);
      --ha-map-space-fade: rgba(255, 255, 255, 0);
      --ha-map-space-high: #dbe8f8;
      --ha-map-space-low: #7aa5d3;
      background-color: var(--ha-map-space-low);
      background-image:
        radial-gradient(
          circle at 50% 50%,
          var(--ha-map-space-glow) 18%,
          var(--ha-map-space-haze) 24%,
          var(--ha-map-space-fade) 34%
        ),
        linear-gradient(
          180deg,
          var(--ha-map-space-high) 0%,
          var(--ha-map-space-low) 100%
        );
      background-repeat: no-repeat;
    }
    #map.space.dark {
      --ha-map-space-glow: rgba(126, 158, 224, 0.5);
      --ha-map-space-haze: rgba(86, 110, 170, 0.22);
      --ha-map-space-fade: rgba(86, 110, 170, 0);
      --ha-map-space-high: #141a30;
      --ha-map-space-low: #05060f;
    }
    #map.clickable:active,
    #map:active {
      cursor: grabbing;
    }
    /* The tail is a rotated square whose upper half sits under the bubble;
       drawn behind it, so it never covers an avatar's frame or selected ring */
    .cluster-bubble-tail {
      position: relative;
      z-index: -1;
    }
    /* Only the raster fallback is inverted for dark mode, the vector style
       ships its own dark cartography. */
    .leaflet-tile-pane .leaflet-tile {
      filter: var(--map-filter);
    }
    /* The Leaflet fallback with WebGL2 renders vectors through the adapter
       without MapLibre's stylesheet; these are the only two rules its canvas
       needs. */
    .maplibregl-map {
      position: relative;
      overflow: hidden;
    }
    .maplibregl-canvas {
      position: absolute;
      top: 0;
      left: 0;
    }
    .maplibregl-ctrl-bottom-left,
    .maplibregl-ctrl-bottom-right {
      /* Lets a card keep the attribution and scale clear of an overlay */
      margin-bottom: var(--ha-map-bottom-inset, 0);
    }
    .maplibregl-ctrl-top-left,
    .maplibregl-ctrl-bottom-left {
      margin-left: var(--ha-map-left-inset, 0);
    }
    .maplibregl-ctrl-top-right,
    .maplibregl-ctrl-bottom-right {
      margin-right: var(--ha-map-right-inset, 0);
    }
    .dark .maplibregl-ctrl.maplibregl-ctrl-group {
      background-color: #1c1c1c;
    }
    .dark .maplibregl-ctrl-group button + button {
      border-top-color: #313131;
    }
    .dark .maplibregl-ctrl button .maplibregl-ctrl-icon {
      filter: invert(1);
    }
    /* Not inherited from the page, which may be in the other mode */
    .maplibregl-ctrl.maplibregl-ctrl-attrib {
      color: #000000;
    }
    .dark .maplibregl-ctrl.maplibregl-ctrl-attrib {
      background-color: rgba(28, 28, 28, 0.6);
      color: #ffffff;
    }
    .dark .maplibregl-ctrl-attrib.maplibregl-compact {
      background-color: #1c1c1c;
    }
    .dark .maplibregl-ctrl-attrib a {
      color: rgba(255, 255, 255, 0.85);
    }
    .dark .maplibregl-ctrl-attrib-button {
      filter: invert(1);
    }
    /* MapLibre's stylesheet, linked into this root, wins on equal specificity */
    .maplibregl-popup-content {
      padding: 8px !important;
      font-size: var(--ha-font-size-s);
      font-family: var(--ha-font-family-body);
      background: rgba(80, 80, 80, 0.9) !important;
      color: white !important;
      border-radius: var(--ha-border-radius-sm) !important;
      box-shadow: none !important;
      text-align: center;
    }
    .maplibregl-popup-anchor-bottom .maplibregl-popup-tip {
      border-top-color: rgba(80, 80, 80, 0.9) !important;
    }
    .maplibregl-popup-anchor-top .maplibregl-popup-tip {
      border-bottom-color: rgba(80, 80, 80, 0.9) !important;
    }
    .maplibregl-ctrl-bottom-left {
      direction: ltr;
    }
    .dark .leaflet-bar a {
      background-color: #1c1c1c;
      color: #ffffff;
    }
    .dark .leaflet-bar a:hover {
      background-color: #313131;
    }
    ${(0,n.iz)(_.xr)}
    .named-icon {
      display: flex;
      align-items: center;
      justify-content: center;
      flex-direction: column;
      text-align: center;
      color: var(--primary-text-color);
    }
    .leaflet-pane {
      z-index: 0 !important;
    }
    .cluster-marker {
      display: flex;
      flex-direction: column;
      align-items: center;
      isolation: isolate;
      filter: var(--ha-cluster-shadow);
    }
    /* The wrapper carries the shadow around the bubble-plus-tail outline, so
       the bubble itself drops its own to avoid a seam at the tail. */
    .cluster-marker .cluster-bubble {
      filter: none;
    }
    .cluster-bubble-tail {
      width: ${U}px;
      height: ${U}px;
      margin-top: ${-U/2}px;
      border-radius: 2px;
      background: var(--card-background-color, #fff);
      transform: rotate(45deg);
    }
    .cluster-bubble {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      max-width: 100%;
      gap: ${D}px;
      padding: ${B}px;
      box-sizing: border-box;
      background: var(--card-background-color, #fff);
      border-radius: 14px;
      filter: var(--ha-cluster-shadow);
      --ha-marker-size: ${I}px;
      --ha-marker-selected-scale: 1;
      --ha-marker-color: transparent;
      --ha-marker-border-width: 1px;
      --ha-marker-font-size: var(--ha-font-size-s);
      /* distinguish letter tiles from the bubble background */
      --ha-marker-background: var(--ha-color-fill-neutral-quiet-resting);
    }
    .cluster-bubble .more {
      flex: none;
      width: ${j}px;
      height: ${I}px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 10px;
      background: var(--ha-color-fill-neutral-quiet-resting, #f0f0f0);
      color: var(--primary-text-color, #212121);
      font-size: var(--ha-font-size-s);
      font-weight: var(--ha-font-weight-medium);
    }
    .cluster-bubble ha-entity-marker {
      flex: none;
    }
    ${(0,n.iz)(M.Nr)}
    .leaflet-bottom {
      /* Lets a card keep the attribution and scale clear of an overlay */
      margin-bottom: var(--ha-map-bottom-inset, 0);
    }
    .leaflet-left {
      margin-left: var(--ha-map-left-inset, 0);
    }
    .leaflet-right {
      margin-right: var(--ha-map-right-inset, 0);
    }
    .leaflet-control,
    .leaflet-top,
    .leaflet-bottom {
      z-index: 1 !important;
    }
    .leaflet-control-scale {
      cursor: unset !important;
    }
    .leaflet-control-scale-line {
      --scale-ruler-color: var(--ha-color-on-surface-default);
      --scale-ruler-surface: var(--ha-color-surface-default);
      font-size: var(--ha-font-size-s);
      font-family: var(--ha-font-family-body);
      color: var(--scale-ruler-color) !important;
      background: color-mix(
        in srgb,
        var(--scale-ruler-surface) 80%,
        transparent
      ) !important;
      text-shadow: none !important;
      direction: ltr;
    }
    /* the theme tokens follow the page, so forced modes need the opposite values */
    #map.forced-light .leaflet-control-scale-line {
      --scale-ruler-color: var(--ha-color-neutral-05);
      --scale-ruler-surface: var(--ha-color-white);
    }
    #map.forced-dark .leaflet-control-scale-line {
      --scale-ruler-color: var(--ha-color-neutral-95);
      --scale-ruler-surface: var(--ha-color-neutral-10);
    }
    .leaflet-left .leaflet-control-scale {
      margin-left: 10px !important;
    }
    .leaflet-bottom .leaflet-control-scale {
      margin-bottom: 10px !important;
    }
    .leaflet-tooltip {
      padding: 8px;
      font-size: var(--ha-font-size-s);
      background: rgba(80, 80, 80, 0.9) !important;
      color: white !important;
      border-radius: var(--ha-border-radius-sm);
      box-shadow: none !important;
      text-align: center;
    }
  `,(0,o.Cg)([(0,s.wk)(),(0,d.Fg)({context:C.iN,subscribe:!0})],tt.prototype,"_states",void 0),(0,o.Cg)([(0,s.wk)(),(0,d.Fg)({context:C.WF,subscribe:!0}),(0,u.p)({transformer:({config:t})=>t})],tt.prototype,"_config",void 0),(0,o.Cg)([(0,s.wk)(),(0,d.Fg)({context:C.EK,subscribe:!0})],tt.prototype,"_ui",void 0),(0,o.Cg)([(0,s.wk)(),(0,d.Fg)({context:C.D5,subscribe:!0})],tt.prototype,"_i18n",void 0),(0,o.Cg)([(0,s.wk)(),(0,d.Fg)({context:C.p0,subscribe:!0})],tt.prototype,"_formatters",void 0),(0,o.Cg)([(0,s.wk)(),(0,d.Fg)({context:C.Wq,subscribe:!0})],tt.prototype,"_connection",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],tt.prototype,"entities",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],tt.prototype,"paths",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],tt.prototype,"editableLocations",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],tt.prototype,"clickable",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"auto-fit",type:Boolean})],tt.prototype,"autoFit",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"render-passive",type:Boolean})],tt.prototype,"renderPassive",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"interactive-zones",type:Boolean})],tt.prototype,"interactiveZones",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"fit-zones",type:Boolean})],tt.prototype,"fitZones",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],tt.prototype,"fitPadding",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"zoom-position"})],tt.prototype,"zoomPosition",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"theme-mode",type:String})],tt.prototype,"themeMode",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],tt.prototype,"mapStyle",void 0),(0,o.Cg)([(0,s.MZ)({type:Number})],tt.prototype,"zoom",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"cluster-markers",type:Boolean})],tt.prototype,"clusterMarkers",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"scale-ruler",type:Boolean})],tt.prototype,"scaleRuler",void 0),(0,o.Cg)([(0,s.wk)()],tt.prototype,"_loaded",void 0),(0,o.Cg)([(0,s.P)("#map")],tt.prototype,"_mapElement",void 0),(0,o.Cg)([(0,s.wk)()],tt.prototype,"_entityReg",void 0),tt=(0,o.Cg)([(0,s.EM)("ha-map")],tt),i.d(e,{},{$:T}),a()}catch(t){a(t)}})},15651(t,e,i){i(9336),i(79846),i(80815),i(34950),i(45453),i(29170),i(15740),i(53930),i(84345),i(83460),i(11663);var a=i(53291),o=i(70174);const r="X-Map-Tiles-Token",n=[0,400,1e3],s=[2e3,5e3,1e4,15e3];let l,d,c,h,u,p,m,b;const g=new Set,v=async t=>{const e=await t.sendMessagePromise({type:"map_tiles/access_token"});e.token!==l&&(l=e.token,g.forEach(t=>t(l)))},f=async(t,e)=>{for(const i of e){if(l)return;i&&await(0,o.l)(i);try{return void await v(t)}catch{}}},y=()=>{if(!m)return;const t=m;v(t).then(()=>_(t)).catch(()=>{})},_=t=>{var e;(l&&!u&&(u=setInterval(()=>{v(null!=m?m:t).catch(()=>{})},12e5)),p!==t)&&(null===(e=p)||void 0===e||e.removeEventListener("ready",y),p=t,t.addEventListener("ready",y))},k=()=>(null!=d?d:location.origin).replace(/\/+$/,"");i.d(e,{ZV:()=>a.Z},{Oc:()=>m?(null!=b||(b=v(m).catch(()=>{}).finally(()=>{b=void 0})),b):Promise.resolve(),Xx:t=>(g.add(t),()=>g.delete(t)),bK:t=>t.startsWith("/")?`${k()}${t}`:t,pW:async t=>{var e;if(m=t,d=null===(e=t.options.auth)||void 0===e?void 0:e.data.hassUrl,l||(null!=c||(c=f(t,n).finally(()=>{c=void 0})),await c),l)return _(t),l;null!=h||(h=f(t,s).then(()=>_(t)).finally(()=>{h=void 0}))},rG:t=>{let e;try{e=new URL(t,k())}catch{return{url:t}}if(!e.pathname.startsWith(`${a.Z}/`))return{url:e.href};const i=new URL(`${k()}${e.pathname}${e.search}`);return l?i.origin===location.origin?{url:i.href,headers:{[r]:l}}:(i.searchParams.set("token",l),{url:i.href}):{url:i.href}}})}}]);
//# sourceMappingURL=34977.83c395bf29041f19.js.map