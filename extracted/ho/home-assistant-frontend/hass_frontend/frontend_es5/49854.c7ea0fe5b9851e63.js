"use strict";(self.rspackChunkhome_assistant_frontend=self.rspackChunkhome_assistant_frontend||[]).push([[49854],{60057(t,e,i){i(19843),i(48);var a=i(97377);i.d(e,{},{H:(t,e)=>{const{latitude:i,longitude:o,gps_accuracy:r}=t.attributes;if("number"==typeof i&&"number"==typeof o)return{latitude:i,longitude:o,gpsAccuracy:r};if("person"!==(0,a.t)(t))return;const n=t.attributes.in_zones;if(!Array.isArray(n)||0===n.length)return;const s=((t,e)=>{for(const i of t){const t=e[i];if(t&&!t.attributes.passive&&"number"==typeof t.attributes.latitude&&"number"==typeof t.attributes.longitude)return t}})(n,e);return s?{latitude:s.attributes.latitude,longitude:s.attributes.longitude}:void 0}})},51139(t,e,i){var a=i(12449),o=(i(19843),i(47144),i(8021),i(89542),i(21323),i(48),i(89199),i(79391),i(43547),i(98434),i(5297),i(61460),i(25071)),r=i(5792);const n={light:"/static/map/light.json",dark:"/static/map/dark.json"},s=`${r.ZV}/raster/{z}/{x}/{y}.png?token={token}`;let l;const d=()=>(()=>{if(void 0===l)try{var t;const e=document.createElement("canvas").getContext("webgl2");l=Boolean(e),null==e||null===(t=e.getExtension("WEBGL_lose_context"))||void 0===t||t.loseContext()}catch(t){l=!1}return l})()&&"function"==typeof BigInt,c=t=>new URL(t,location.href).href,h=async t=>{var e;const o=t.shipped&&n[t.shipped],r=o?await(await fetch(o)).json():await(await i.e(60532).then(i.bind(i,94335))).buildMapStyle(t.palette,null!==(e=t.options)&&void 0!==e?e:{},t.baseColors);return"string"==typeof r.sprite?r.sprite=c(r.sprite):Array.isArray(r.sprite)&&(r.sprite=r.sprite.map(t=>(0,a.A)((0,a.A)({},t),{},{url:c(t.url)}))),r};let u=!1;const p=t=>{u||(u=!0,t(new URL("/frontend_es5/maplibre-gl-worker.20260930.0.js",location.href).href))};let b=!1;const m=t=>{b||(b=!0,t(new URL("/static/map/mapbox-gl-rtl-text.js",location.href).href,!0).catch(()=>{}))},g=(t,e,i)=>{const a=t.tileLayer((0,r.bK)(s),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',maxZoom:20,maxNativeZoom:19,referrerPolicy:void 0,token:null!=i?i:""}).addTo(e),o=(0,r.Xx)(t=>{a.options.token=t,a.redraw()});return e.on("unload",o),{setMapStyle:()=>{}}};i.d(e,{},{MK:h,V4:async(t,e,n,s,l=!1)=>{if(!l&&d()){let l;try{const[{maplibreGL:d},c]=await Promise.all([Promise.all([i.e(16618),i.e(71254),i.e(35166),i.e(70600)]).then(i.bind(i,2797)),Promise.all([i.e(16618),i.e(71254),i.e(75956)]).then(i.bind(i,46513))]);p(c.setWorkerUrl),m(c.setRTLTextPlugin),l=await(async(t,e,i,n,s)=>{let l;try{l=t({style:await h(n),transformRequest:t=>(0,a.A)((0,a.A)({},(0,r.rG)(t)),{},{referrerPolicy:void 0})}),l.addTo(i)}catch(t){if(l)try{l.remove()}catch(t){}return}let d=n,c=n,u=0,p=!0,b=!1;const m=l.getMaplibreMap();let v,f=!1;const y=()=>{f&&k()},_=()=>{p=!1,document.removeEventListener("visibilitychange",y);try{l.remove()}catch(t){}g(e,i,s)},k=()=>{clearTimeout(v),p&&!document.hidden&&(v=window.setTimeout(_,2e3))};m.on("webglcontextlost",()=>{f=!0,k()}),m.on("webglcontextrestored",()=>{f=!1,clearTimeout(v)}),document.addEventListener("visibilitychange",y),i.on("unload",()=>{clearTimeout(v),document.removeEventListener("visibilitychange",y)});const w=t=>{const e=++u;h(t).then(i=>{var a;e===u&&(d=t,null===(a=l.getMaplibreMap())||void 0===a||a.setStyle(i))}).catch(()=>{e===u&&(c=d)})};let M=0;m.on("error",t=>{var e;const i=null===(e=t.error)||void 0===e?void 0:e.status;void 0!==i&&403!==i&&404!==i||Date.now()-M<3e4||(M=Date.now(),b=!0,(0,r.Oc)())});const x=(0,r.Xx)(()=>{p&&b&&(b=!1,w(c))});return i.on("unload",x),{setMapStyle:t=>{p&&!(0,o.b)(t,c)&&(c=t,w(t))}}})(d,t,e,n,s)}catch(t){}if(l)return l}return g(t,e,s)},W$:p,jV:d,vM:m})},55659(t,e,i){i.d(e,{},{rx:t=>{const e=document.createElement("div");e.className="editable-circle-resize",e.tabIndex=0,e.setAttribute("role","slider"),e.setAttribute("aria-valuemin","1"),e.setAttribute("aria-valuemax",String(1e5)),t&&e.setAttribute("aria-label",t);const i=document.createElement("div");return i.className="editable-circle-resize-dot",e.appendChild(i),e},xr:"\n  .editable-circle-center {\n    width: 16px;\n    height: 16px;\n    border-radius: 50%;\n    background: var(--primary-color);\n    border: 2px solid var(--card-background-color, #fff);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n  .editable-circle-resize {\n    width: 24px;\n    height: 24px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    cursor: ew-resize;\n  }\n  .editable-circle-resize-dot {\n    width: 12px;\n    height: 12px;\n    border-radius: 50%;\n    background: var(--card-background-color, #fff);\n    border: 2px solid var(--primary-color);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n"})},86233(t,e,i){const a=6371008.8,o=t=>t*Math.PI/180,r=t=>180*t/Math.PI,n=(t,e,i)=>{const n=e/a,s=o(t[0]),l=o(i),d=Math.asin(Math.sin(s)*Math.cos(n)+Math.cos(s)*Math.sin(n)*Math.cos(l)),c=Math.atan2(Math.sin(l)*Math.sin(n)*Math.cos(s),Math.cos(n)-Math.sin(s)*Math.sin(d));return[r(d),t[1]+r(c)]};i.d(e,{},{RO:(t,e)=>n(t,e,90),Rn:(t,e)=>{const i=e/a,n=Math.max(-90,t[0]-r(i)),s=Math.min(90,t[0]+r(i)),l=Math.sin(i)/Math.cos(o(t[0]));if(n<=-90||s>=90||Math.abs(l)>=1)return[[n,-180],[s,180]];const d=r(Math.asin(l));return[[n,t[1]-d],[s,t[1]+d]]},S_:(t,e)=>{const i=o(e[0]-t[0]),a=o(e[1]-t[1]),r=Math.sin(i/2)**2+Math.cos(o(t[0]))*Math.cos(o(e[0]))*Math.sin(a/2)**2;return 12742017.6*Math.asin(Math.sqrt(r))},bM:n})},28006(t,e,i){i.d(e,{jJ:()=>r,u8:()=>o,l6:()=>l,kR:()=>p,vA:()=>u});var a=i(12449);i(97700),i(19843),i(47144),i(89542),i(29024),i(62758),i(6667),i(48);const o=["default","colorful","natural","muted","gray","toner"],r="default",n={default:{palette:"colorful",colors:{background:"#f4efe6",land:"#f4efe6",water:"#bcd9e8",labelWater:"#5b86a3",natureWood:"#cfe1bf",natureGrass:"#e2ecda",naturePark:"#cfe1bf",natureLeisure:"#e2ecda",natureAgriculture:"#e8eee2",natureWetland:"#e5ebe0",natureSand:"#f1eadf",natureRock:"#f1eadf",glacier:"#f9f6f1",areaResidential:"#efe8dc",areaCommercial:"#f4e1db",areaIndustrial:"#ede5ce",areaWaste:"#ece3d5",areaBurial:"#efe8dc",siteParking:"#ede6d8",siteSports:"#cfe1bf26",building:"#e7ddca",buildingBg:"#dcccb2",roadStreet:"#fcfaf8",roadStreetBg:"#e6dac7",roadTrunk:"#fbe6c2",roadTrunkBg:"#e5cea5",roadMotorway:"#ebd4ab",roadMotorwayBg:"#deba78",transitRail:"#e9dfce",transitSubway:"#eae1d1",transitCycle:"#f2ede3",transitFoot:"#f2ede3",boundary:"#d6c3a4",boundaryDisputed:"#e2d6c0",label:"#4a463d",labelHalo:"#faf8f5cc",labelSymbol:"#8d8676",labelPoi:"#8d867666",labelShield:"#faf8f4",labelHousenumber:"#8d86764d"},colorsDark:{background:"#191b2c",land:"#191b2c",water:"#27357a",labelWater:"#9cc0f0",natureWood:"#254948",natureGrass:"#213b39",naturePark:"#28504b",natureLeisure:"#213532",natureAgriculture:"#203233",natureWetland:"#253337",natureSand:"#2a2c3d",natureRock:"#2a2c3d",glacier:"#2a2c3d",areaResidential:"#1d2034",areaCommercial:"#29213a",areaIndustrial:"#242431",areaWaste:"#1d2034",areaBurial:"#1d2034",siteParking:"#1d2034",siteSports:"#25413926",building:"#21243c",buildingBg:"#2a2e4a",roadStreet:"#2b3052",roadStreetBg:"#1a1d33",roadTrunk:"#383e67",roadTrunkBg:"#22263f",roadMotorway:"#454d7d",roadMotorwayBg:"#2a2f4c",transitRail:"#2c3150",transitSubway:"#2c3150",transitCycle:"#2b3052",transitFoot:"#2b3052",boundary:"#3b4068",boundaryDisputed:"#3b4068",label:"#e7ecf8",labelHalo:"#12141fcc",labelSymbol:"#959dbd",labelPoi:"#959dbd66",labelShield:"#191b2c",labelHousenumber:"#959dbd4d"}},colorful:{palette:"colorful"},natural:{palette:"natural"},muted:{palette:"muted"},gray:{palette:"gray"},toner:{palette:"toner"}},s=t=>o.includes(t),l=t=>"object"==typeof t&&null!==t,d=["colors","recolor","text","icon","layers"],c=t=>t.replace(/_([a-z])/g,(t,e)=>e.toUpperCase()),h=t=>Array.isArray(t)?t.map(h):t&&"object"==typeof t?Object.fromEntries(Object.entries(t).map(([t,e])=>[c(t),h(e)])):t,u=(t,e)=>{const i=s(e)&&e!==r?e:void 0,o=l(t)?(0,a.A)({},t):{};return delete o.base,Object.keys(o).length?(0,a.A)((0,a.A)({},i&&{base:i}),o):i},p=(t,e,i)=>{var o;const u=l(t)?t:void 0,p=u?u.base:t,b=s(p)?p:r,m=((t,e)=>{const{palette:i}=n[t];return e?`${i}-dark`:i})(b,e),g=u?((t,e)=>{const i=t,a={};for(const t of d){var o;const e=null!==(o=i[t])&&void 0!==o?o:i[c(t)];void 0!==e&&(a[c(t)]=h(e))}const r=i.colors_dark;return e&&void 0!==r&&(a.colors=h(r)),a})(u,e):{},v=Object.keys(g).length>0,{colors:f,colorsDark:y}=n[b],_=null!==(o=e?y:f)&&void 0!==o?o:f;if((_||i)&&(g.colors=(0,a.A)((0,a.A)((0,a.A)({},_),i),g.colors)),!Object.keys(g).length)return{palette:m};const k=_?{baseColors:_}:{};return b===r&&(!i&&!v)?(0,a.A)((0,a.A)({palette:m,options:g},k),{},{shipped:e?"dark":"light"}):(0,a.A)({palette:m,options:g},k)}},71760(t,e,i){i(19843),i(47144),i(21927),i(25744),i(89542),i(99686),i(62758),i(20071),i(48);const a={"--ha-color-map-land":["background","land"],"--ha-color-map-water":["water"],"--ha-color-map-green":["naturePark","natureWood","natureGrass","natureLeisure","natureWetland","siteSports"],"--ha-color-map-area":["areaResidential","areaCommercial","areaIndustrial","areaWaste","areaBurial","siteParking","natureAgriculture","natureSand","natureRock"],"--ha-color-map-building":["building"],"--ha-color-map-building-outline":["buildingBg"],"--ha-color-map-road":["roadStreet"],"--ha-color-map-road-major":["roadMotorway","roadTrunk"],"--ha-color-map-road-outline":["roadStreetBg","roadTrunkBg","roadMotorwayBg"],"--ha-color-map-transit":["transitRail","transitSubway","transitCycle","transitFoot"],"--ha-color-map-boundary":["boundary","boundaryDisputed"],"--ha-color-map-label":["label"],"--ha-color-map-label-halo":["labelHalo"],"--ha-color-map-label-secondary":["labelSymbol","labelPoi","labelHousenumber"]},o={siteSports:.15,labelHalo:.8,labelPoi:.4,labelHousenumber:.3},r=/^#([0-9a-f]{3,8})$/i,n=/^rgba?\(([^)]+)\)$/i,s=/^color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\s*\)$/i,l=t=>{const e=t.match(r);if(e){const t=e[1],i=3===t.length||4===t.length,a=e=>i?parseInt(t[e]+t[e],16):parseInt(t.slice(2*e,2*e+2),16);if(3===t.length||4===t.length||6===t.length||8===t.length){const e=4===t.length||8===t.length?a(3)/255:1;return[a(0),a(1),a(2),e]}return}const i=t.match(n);if(i){var a;const t=i[1].split(/[,\s/]+/).filter(Boolean).map(Number);if(t.length<3||t.slice(0,3).some(Number.isNaN))return;return[t[0],t[1],t[2],null!==(a=t[3])&&void 0!==a?a:1]}const o=t.match(s);if(o){var l;const t=t=>Math.round(255*Number(t));return[t(o[1]),t(o[2]),t(o[3]),Number(null!==(l=o[4])&&void 0!==l?l:1)]}},d=[1,2,3,1],c=(t,e)=>{const i=document.createElement("span");i.style.cssText="display:none;color:rgb(1, 2, 3)";const a=document.createElement("span");a.style.color=`var(${e})`,i.append(a),t.append(i);const o=l(getComputedStyle(a).color);return i.remove(),o&&o.every((t,e)=>t===d[e])?void 0:o};i.d(e,{},{Q:t=>{const e=getComputedStyle(t);let i;for(const[s,d]of Object.entries(a)){var r;const a=e.getPropertyValue(s).trim();if(!a)continue;const h=null!==(r=l(a))&&void 0!==r?r:c(t,s);if(!h)continue;null!=i||(i={});const[u,p,b,m]=h;for(const t of d){var n;const e=Math.round(m*(null!==(n=o[t])&&void 0!==n?n:1)*1e3)/1e3;i[t]=`rgba(${u},${p},${b},${e})`}}return i}})},52573(t,e,i){i(99921),i(47144),i(25744),i(8021);const a="haMapA11y",o=t=>{const e=t.dataset[a];void 0!==e&&(e.split(" ").filter(Boolean).forEach(e=>t.removeAttribute(e)),delete t.dataset[a])};i.d(e,{},{I:o,l:(t,e,i)=>{o(t);const r=[];!e||t.hasAttribute("aria-label")||t.hasAttribute("aria-labelledby")||(t.setAttribute("aria-label",e),r.push("aria-label")),t.hasAttribute("role")||(i?(t.setAttribute("role","button"),r.push("role")):e?(t.setAttribute("role","img"),r.push("role")):(t.setAttribute("aria-hidden","true"),r.push("aria-hidden"))),i&&!t.hasAttribute("tabindex")&&(t.tabIndex=0,r.push("tabindex")),t.dataset[a]=r.join(" ")}})},7952(t,e,i){var a=i(65541),o=i.n(a);i.d(e,{},{D:t=>o()(t,{whiteList:{},stripIgnoreTag:!0,stripIgnoreTagBody:!0})})},14279(t,e,i){i.a(t,async function(t,e){try{i(19843),i(48);var a=i(89797),o=i(20686),r=i(65183),n=i(67781),s=i(70465),l=i(86075),d=i(32323),c=t([d]);d=(c.then?(await c)():c)[0];let h,u,p,b,m,g=t=>t;class v extends o.WF{render(){return(0,o.qy)(h||(h=g` <div part="marker" class="marker ${0}" style=${0}; @click=${0}> ${0} </div> `),this.entityPicture?"picture":"",(0,n.W)({"--ha-marker-selected-color":this.entityColor}),this._badgeTap,this.entityPicture?(0,o.qy)(u||(u=g`<div part="picture" class="entity-picture" style=${0};></div>`),(0,n.W)({"background-image":`url(${this.entityPicture})`})):this.showIcon&&this.entityId?(0,o.qy)(p||(p=g`<ha-state-icon .stateObj=${0}></ha-state-icon>`),this._stateObj):this.entityUnit?(0,o.qy)(b||(b=g` ${0} <span class="unit" style="display:${0}">${0}</span> `),this.entityName,this.entityUnit?"initial":"none",this.entityUnit):this.entityName)}connectedCallback(){super.connectedCallback(),this.addEventListener("keydown",this._handleKeydown)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("keydown",this._handleKeydown)}_badgeTap(t){t.stopPropagation(),this.entityId&&(0,l.r)(this,"hass-more-info",{entityId:this.entityId})}constructor(...t){super(...t),this.showIcon=!1,this.selected=!1,this._handleKeydown=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._badgeTap(t))}}}v.styles=(0,o.AH)(m||(m=g`.marker{text-align:center;box-sizing:border-box;width:var(--ha-marker-size,48px);height:var(--ha-marker-size,48px);font-size:var(--ha-marker-font-size,var(--ha-font-size-xl));border-radius:var(--ha-marker-border-radius,50%);border:var(--ha-marker-border-width,3px) solid var(--ha-marker-color,var(--card-background-color,#fff));box-shadow:var(--ha-marker-shadow,var(--ha-box-shadow-s));color:var(--primary-text-color);background-color:var(--ha-marker-background,var(--card-background-color));justify-content:center;align-items:center;display:flex}.marker.picture{overflow:hidden}:host([selected]) .marker{outline:3px solid var(--ha-marker-selected-color,var(--primary-color))}.entity-picture{background-size:cover;width:100%;height:100%}.unit{margin-left:2px}`)),(0,a.Cg)([(0,r.MZ)({attribute:"entity-id",reflect:!0})],v.prototype,"entityId",void 0),(0,a.Cg)([(0,r.wk)(),(0,s.fI)({entityIdPath:["entityId"]})],v.prototype,"_stateObj",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-name"})],v.prototype,"entityName",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-unit"})],v.prototype,"entityUnit",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-picture"})],v.prototype,"entityPicture",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-color"})],v.prototype,"entityColor",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"show-icon",type:Boolean})],v.prototype,"showIcon",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],v.prototype,"selected",void 0),v=(0,a.Cg)([(0,r.EM)("ha-entity-marker")],v),e()}catch(t){e(t)}})},25581(t,e,i){i.a(t,async function(t,a){try{var o=i(12449),r=i(41279),n=(i(63773),i(97700),i(19843),i(99921),i(47144),i(8021),i(89542),i(25102),i(47508),i(21323),i(62758),i(24791),i(53457),i(73532),i(34737),i(4666),i(77809),i(92653),i(6667),i(48),i(89797)),s=i(58012),l=i(20686),d=i(65183),c=i(19741),h=i(98878),u=i(37151),p=i(6694),b=(i(60666),i(11808)),m=i(86075),g=i(97377),v=i(65942),f=i(60057),y=i(51139),_=i(86233),k=i(28006),w=i(71760),M=i(55659),x=i(89275),z=i(52573),C=i(85108),E=i(25071),P=i(7952),L=i(66572),S=i(5792),A=i(14279),F=t([r,A,u,p]);[r,A,u,p]=F.then?(await F)():F;let R,Z=t=>t;const I=250,$=t=>"string"==typeof t?t:t.entity_id,H=["name","state","attribute","icon"],B=(t,e)=>{var i,a,o,r;return t.element===e.element&&t.title===e.title&&t.color===e.color&&t.locationEditable===e.locationEditable&&t.radiusEditable===e.radiusEditable&&t.activatable===e.activatable&&(null===(i=t.elementSize)||void 0===i?void 0:i[0])===(null===(a=e.elementSize)||void 0===a?void 0:a[0])&&(null===(o=t.elementSize)||void 0===o?void 0:o[1])===(null===(r=e.elementSize)||void 0===r?void 0:r[1])},T=t=>({addDraggableMarker:(e,i,a)=>{let o=i,r=t.addMarker(e,o,a);return{get location(){return o},clusterData:a.clusterData,setLocation:i=>{r.remove(),o=i,r=t.addMarker(e,o,a)},remove:()=>r.remove()}},addEditableCircle:(e,i)=>{var a;const o=null!==(a=i.centerElement)&&void 0!==a?a:document.createElement("div");let r;if(i.centerElement||(o.className="editable-circle-center"),i.onClick){const t=t=>{t.stopPropagation(),i.onClick()},e=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),i.onClick())};o.addEventListener("click",t),o.addEventListener("keydown",e),r=()=>{o.removeEventListener("click",t),o.removeEventListener("keydown",e)}}let n={center:e,radius:i.radius},s=[];const l=()=>{var e;s=[t.addCircle(n.center,{radius:n.radius,color:i.color}),t.addMarker(o,n.center,{size:null!==(e=i.centerSize)&&void 0!==e?e:[16,16],interactive:!!i.onClick,title:i.title})]};return l(),{get center(){return n.center},get radius(){return n.radius},update:(t,e)=>{s.forEach(t=>t.remove()),n={center:t,radius:e},l()},remove:()=>{var t;null===(t=r)||void 0===t||t(),s.forEach(t=>t.remove())}}}}),j=32,O=6,N=4,W=12,D=3,U=28,V=99,q=10,G=Math.round(q*Math.SQRT2/2),K=2,X=40,Q=160,J=t=>{const e=t.replace(".","-");return`marker, picture, marker: marker-${e}, picture: picture-${e}`},Y=(t,e,i=!0)=>{const a=e&&i?t.get(e):void 0;if(a&&!a.isConnected)return a;const o=document.createElement("ha-entity-marker");return e&&(o.setAttribute("exportparts",J(e)),t.set(e,o)),o};class tt extends l.mN{connectedCallback(){this._pauseAutoFit=!1,document.addEventListener("visibilitychange",this._handleVisibilityChange),this._handleVisibilityChange(),super.connectedCallback(),this._loadMap(),this._attachObserver()}_watchRegistry(){var t;!this._registryConsumer&&null!==(t=this.entities)&&void 0!==t&&t.length&&(this._registryConsumer=new h.T(this,L.ih,t=>{this._entityReg=t}))}disconnectedCallback(){var t,e;super.disconnectedCallback(),document.removeEventListener("visibilitychange",this._handleVisibilityChange),null===(t=this._engine)||void 0===t||t.destroy(),this._engine=void 0,this._setupAttempt++,null===(e=this._startingEngine)||void 0===e||e.destroy(),this._startingEngine=void 0,this._loading=!1,this._entityHandles=[],this._entityMarkers.clear(),this._clusterAvatars.clear(),this._zoneHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}update(t){var e,i;if(super.update(t),!this._loaded)return;let a=!1;const o=t.get("_states");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),a=!this._pauseAutoFit;else if(this._loaded&&o&&this.entities)for(const t of this.entities)if(o[$(t)]!==this._states[$(t)]){this._drawEntities(),a=!this._pauseAutoFit;break}var r;((t.has("clusterMarkers")||t.has("_entityReg"))&&this._drawEntities(),t.has("fitPadding")&&!(0,E.b)(t.get("fitPadding"),this.fitPadding)&&(a=!this._pauseAutoFit),t.has("zoomPosition"))&&(null===(r=this._engine)||void 0===r||r.setZoomControlPosition(this.zoomPosition));const n=t.get("_config");if((t.has("_loaded")||t.has("scaleRuler")||t.has("_config")&&(null==n||null===(e=n.unit_system)||void 0===e?void 0:e.length)!==(null===(i=this._config)||void 0===i||null===(i=i.unit_system)||void 0===i?void 0:i.length))&&this._drawScaleRuler(),t.has("_loaded")||t.has("paths")){var s;this._drawPaths();const e=t.get("paths");var l;if(!(null==e||!e.length)!=!(null===(s=this.paths)||void 0===s||!s.length))null===(l=this._engine)||void 0===l||l.refreshClusters()}var d;(t.has("_loaded")||t.has("editableLocations")?this._drawEditableLocations()&&(a=!0):t.has("_i18n")&&this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()),t.has("_loaded")&&this._pendingFit?this._runPendingFit():(t.has("_loaded")||this.autoFit&&a)&&this.fitMap(),t.has("zoom")&&this._withProgrammaticFit(()=>{this._engine.setZoom(this.zoom)}),t.has("mapStyle"))&&(null===(d=this._engine)||void 0===d||d.setMapStyle(this._resolvedMapStyle));const c=t.get("_ui");(t.has("themeMode")||t.has("_ui")&&(!c||c.themes!==this._ui.themes))&&(this._updateMapAppearance(),this._drawEntities(),this._drawPaths(),this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()))}get _darkMode(){var t;return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(null===(t=this._ui)||void 0===t||null===(t=t.themes)||void 0===t?void 0:t.darkMode)}_readThemeColors(){var t;const e=Boolean(null===(t=this._ui)||void 0===t||null===(t=t.themes)||void 0===t?void 0:t.darkMode),i=this._darkMode===e?(0,w.Q)(this):void 0;(0,E.b)(i,this._themeColors)||(this._themeColors=i)}get _resolvedMapStyle(){return this._resolveMapStyle(this.mapStyle,this._darkMode,this._themeColors)}_updateMapAppearance(){var t;this._readThemeColors();const e=this._mapElement;e.classList.toggle("clickable",this.clickable),e.classList.toggle("dark",this._darkMode),e.classList.toggle("forced-dark","dark"===this.themeMode),e.classList.toggle("forced-light","light"===this.themeMode),null===(t=this._engine)||void 0===t||t.setMapStyle(this._resolvedMapStyle)}async _createEngine(){if(this._forceLeaflet||!(0,y.jV)()){return new((await Promise.all([i.e(16618),i.e(35166),i.e(59151)]).then(i.bind(i,859))).LeafletMapEngine)}return new((await i.e(41645).then(i.bind(i,64988))).MapLibreMapEngine)}async _loadMap(){const t=this._forceLeaflet||!(0,y.jV)();try{await this._setUpEngine()}catch(e){if(!this.isConnected)return;if(t)throw e;this._forceLeaflet=!0,await this._loadMap()}}async _setUpEngine(){var t;if(this._loading)return;null===(t=this.shadowRoot.getElementById("map"))||void 0===t||t.remove();const e=document.createElement("div");e.id="map",this.shadowRoot.append(e),this._loading=!0;const i=++this._setupAttempt;let a;try{var o,r,n,s;const t=this._connection?await(0,S.pW)(this._connection.connection):void 0;this._readThemeColors();const l=this._forceLeaflet;if(a=await this._createEngine(),i!==this._setupAttempt)return;if(this._startingEngine=a,await a.init(e,{center:[null!==(o=null===(r=this._config)||void 0===r?void 0:r.latitude)&&void 0!==o?o:52.3731339,null!==(n=null===(s=this._config)||void 0===s?void 0:s.longitude)&&void 0!==n?n:4.8903147],zoom:this.zoom,mapStyle:this._resolvedMapStyle,token:t,rasterOnly:this._forceLeaflet,zoomControlPosition:this.zoomPosition,events:{click:t=>this._handleEngineClick(t),zoomStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},moveStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},fatal:()=>this._handleEngineFatal()}}),!this.isConnected||i!==this._setupAttempt)return;if(this._forceLeaflet&&!l)throw new Error("Map engine failed during setup");this._engine=a,this._updateMapAppearance(),this._loaded=!0,(0,m.r)(this,"editing-available-changed",{available:!!a.editing})}finally{i===this._setupAttempt&&(this._loading=!1,this._startingEngine=void 0),a&&a!==this._engine&&a.destroy()}}_handleEngineFatal(){var t,e;this._forceLeaflet||(this._forceLeaflet=!0,this._loading?null===(e=this._startingEngine)||void 0===e||e.destroy():(null===(t=this._engine)||void 0===t||t.destroy(),this._engine=void 0,this._entityHandles=[],this._zoneHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._loadMap()))}_handleEngineClick(t){0===this._clickCount&&setTimeout(()=>{1===this._clickCount&&(0,m.r)(this,"map-clicked",{location:t}),this._clickCount=0},250),this._clickCount++}_withProgrammaticFit(t){this._isProgrammaticFit=!0,t(),setTimeout(()=>{this._isProgrammaticFit=!1},I)}fitMap(t){var e,i;if(null!=t&&t.unpause_autofit&&(this._pauseAutoFit=!1),!this._engine||!this._config)return;if(this._deferIfUnsized(()=>this.fitMap(t)))return;if(!(this._focusPoints.length||this._focusZonePoints.length||null!==(e=this.editableLocations)&&void 0!==e&&e.length))return this._withProgrammaticFit(()=>{this._engine.setView([this._config.latitude,this._config.longitude],(null==t?void 0:t.zoom)||this.zoom)}),void(this._hasFitted=!0);const a=[...this._focusPoints,...this._focusZonePoints];null===(i=this.editableLocations)||void 0===i||i.forEach(t=>{t.radius?a.push(...(0,_.Rn)(t.location,t.radius)):a.push(t.location)}),this._withProgrammaticFit(()=>{var e,i;this._engine.fitBounds(a,{maxZoom:(null==t?void 0:t.zoom)||this.zoom,pad:null!==(e=null==t?void 0:t.pad)&&void 0!==e?e:.5,padding:null!==(i=null==t?void 0:t.padding)&&void 0!==i?i:this.fitPadding,animate:this._hasFitted})}),this._hasFitted=!0}_deferIfUnsized(t){return this._engine.hasUsableSize()?(this._pendingFit=void 0,!1):(this._pendingFit=t,!0)}_runPendingFit(){if(this._pendingFit&&this._engine&&this._engine.hasUsableSize()){const t=this._pendingFit;this._pendingFit=void 0,t()}}panTo(t){var e;null===(e=this._engine)||void 0===e||e.panTo(t)}containsLocation(t){var e,i;return null!==(e=null===(i=this._engine)||void 0===i?void 0:i.containsLocation(t))&&void 0!==e&&e}setView(t,e){this._engine?(this._pendingFit=void 0,this._engine.setView(t,e)):this._pendingFit=()=>this.setView(t,e)}fitBounds(t,e){this._pauseAutoFit=!0,this._engine?this._deferIfUnsized(()=>this.fitBounds(t,e))||(this._withProgrammaticFit(()=>{var i;this._engine.fitBounds(t,{maxZoom:(null==e?void 0:e.zoom)||this.zoom,pad:null!==(i=null==e?void 0:e.pad)&&void 0!==i?i:.5,animate:this._hasFitted,padding:null==e?void 0:e.padding})}),this._hasFitted=!0):this._pendingFit=()=>this.fitBounds(t,e)}_drawEditableLocations(){var t,e;const i=this._engine;if(!i)return!1;const a=T(i),o=null!==(t=i.editing)&&void 0!==t?t:a,r=new Set((null!==(e=this.editableLocations)&&void 0!==e?e:[]).map(t=>t.id));let n=!1;for(const[t,e]of this._editableHandles){var s;if(!r.has(t))null===(s=e.cleanup)||void 0===s||s.call(e),e.handle.remove(),this._editableHandles.delete(t),n=!0}if(!this.editableLocations)return n;const l=getComputedStyle(this).getPropertyValue("--accent-color");for(const t of this.editableLocations){var d,c,h,u;const{id:e}=t,i=null!==(d=t.title)&&void 0!==d?d:null===(c=this._i18n)||void 0===c?void 0:c.localize("ui.components.map.location"),r=this._editableHandles.get(e),s=t.radius?"circle":"marker";if(r&&r.kind===s&&B(r.source,t)){"circle"===r.kind?r.handle.update(t.location,t.radius):r.handle.setLocation(t.location),r.source=t;continue}var p;if(r)null===(p=r.cleanup)||void 0===p||p.call(r),r.handle.remove();else n=!0;if("circle"===s){var b,g;this._editableHandles.set(e,{kind:s,source:t,handle:o.addEditableCircle(t.location,{radius:t.radius,color:t.color||l,centerElement:t.element,centerSize:t.elementSize,title:i,moveable:t.locationEditable,resizable:t.radiusEditable,resizeLabel:t.title?null===(b=this._i18n)||void 0===b?void 0:b.localize("ui.components.map.radius_of",{name:t.title}):null===(g=this._i18n)||void 0===g?void 0:g.localize("ui.components.map.radius"),onMove:t=>(0,m.r)(this,"editable-location-moved",{id:e,location:t}),onResize:t=>(0,m.r)(this,"editable-location-resized",{id:e,radius:t}),onClick:t.activatable?()=>(0,m.r)(this,"editable-location-clicked",{id:e}):void 0})});continue}const v=null!==(h=t.element)&&void 0!==h?h:document.createElement("div");t.element||(v.className="editable-circle-center");let f,y=!1;if(t.activatable){const t=()=>{y=!1},i=t=>{t.stopPropagation(),y||(0,m.r)(this,"editable-location-clicked",{id:e})},a=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),(0,m.r)(this,"editable-location-clicked",{id:e}))};v.addEventListener("pointerdown",t),v.addEventListener("click",i),v.addEventListener("keydown",a),f=()=>{v.removeEventListener("pointerdown",t),v.removeEventListener("click",i),v.removeEventListener("keydown",a)}}const _=t.locationEditable?o:a;this._editableHandles.set(e,{kind:s,source:t,cleanup:f,handle:_.addDraggableMarker(v,t.location,{size:null!==(u=t.elementSize)&&void 0!==u?u:[16,16],interactive:!0,focusable:!!t.activatable,title:i,onDragEnd:t=>{y=!0,(0,m.r)(this,"editable-location-moved",{id:e,location:t})}})})}return n}_removeEditableLocations(){for(const e of this._editableHandles.values()){var t;null===(t=e.cleanup)||void 0===t||t.call(e),e.handle.remove()}this._editableHandles.clear()}_computePathTooltip(t,e){var i;let a;return a=t.fullDatetime?(0,u.r6)(e.timestamp,this._i18n.locale,this._config):(0,s.c)(e.timestamp)?(0,p.ie)(e.timestamp,this._i18n.locale,this._config):(0,p.Xs)(e.timestamp,this._i18n.locale,this._config),`${(0,P.D)(null!==(i=t.name)&&void 0!==i?i:"")}<br>${a}`}_drawPaths(){if(!this._i18n||!this._config||!this._engine)return;if(this._pathHandles.length&&(this._pathHandles.forEach(t=>t.remove()),this._pathHandles=[]),!this.paths)return;const t=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach(e=>{let i,a;e.gradualOpacity&&(i=e.gradualOpacity/(e.points.length-2),a=1-e.gradualOpacity);const o=[],r=[];for(let t=0;t<e.points.length-1;t++){const n=e.gradualOpacity?a+t*i:void 0,s=e.points[t],l=e.points[t+1];if(r.push({location:s.point,opacity:n,tooltipHtml:this._computePathTooltip(e,s)}),Math.abs(s.point[1]-l.point[1])<=180)o.push({points:[s.point,l.point],opacity:n});else{const t=(l.point[1]-s.point[1]+540)%360-180;let e;e=0===t?(s.point[0]+l.point[0])/2:s.point[0]+(l.point[0]-s.point[0])*(s.point[1]>0?180-s.point[1]:-180-s.point[1])/t;const i=[e,s.point[1]>0?180:-180],a=[e,l.point[1]>0?180:-180];o.push({points:[s.point,i],opacity:n}),o.push({points:[a,l.point],opacity:n})}}const n=e.points.length-1;if(n>=0){const t=e.gradualOpacity?a+n*i:void 0;r.push({location:e.points[n].point,opacity:t,tooltipHtml:this._computePathTooltip(e,e.points[n])})}const s={color:e.color||t,segments:o,markers:r};this._pathHandles.push(this._engine.addPath(s))})}_drawEntities(){const t=this._states,e=this._engine;if(!t||!e)return;if(this._entityHandles.forEach(t=>t.remove()),this._entityHandles=[],this._focusPoints=[],this._zoneHandles.forEach(t=>t.remove()),this._zoneHandles=[],this._focusZonePoints=[],!this.entities)return this._entityMarkers.clear(),this._clusterAvatars.clear(),void e.setClustering(null);this._watchRegistry();const i=getComputedStyle(this),a={};this._zonePositions={},this._zoneRadii={};for(const e of this.entities){const i=t[$(e)];!i||"zone"!==(0,g.t)(i)||!this.renderPassive&&i.attributes.passive||(a["zone.home"===i.entity_id?"home":(0,v.u)(i)]=i.entity_id,"number"==typeof i.attributes.latitude&&"number"==typeof i.attributes.longitude&&(this._zonePositions[i.entity_id]=[i.attributes.latitude,i.attributes.longitude],"number"==typeof i.attributes.radius&&(this._zoneRadii[i.entity_id]=i.attributes.radius)))}const o=new Set;for(const l of this.entities){var r,n,s;const d=t[$(l)];if(!d)continue;const c="string"!=typeof l?l.name:void 0,h=null!=c?c:(0,v.u)(d),{passive:u,icon:p,radius:b,entity_picture:y}=d.attributes,k=(0,f.H)(d,t);if(!k)continue;const{latitude:w,longitude:M,gpsAccuracy:z}=k,E=[w,M];if("zone"===(0,g.t)(d)){if(u&&!this.renderPassive)continue;const t="string"!=typeof l&&l.hide_radius,a=!u&&"string"!=typeof l&&l.color?l.color:(0,x.YG)(d.entity_id,!!u,this._entityReg,i);!t&&b&&this._zoneHandles.push(e.addCircle(E,{radius:b,color:a}));const o=(0,C.x5)({color:a,icon:p,name:h});if(this.interactiveZones){const t=t=>{t.stopPropagation(),(0,m.r)(this,"hass-more-info",{entityId:d.entity_id})};o.addEventListener("click",t),o.addEventListener("keydown",e=>{"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),t(e))})}this._zoneHandles.push(e.addMarker(o,E,{size:[36,36],interactive:this.interactiveZones,title:h})),!this.fitZones||"string"!=typeof l&&!1===l.focus||(!t&&b?this._focusZonePoints.push(...(0,_.Rn)(E,b)):this._focusZonePoints.push(E));continue}const P="string"!=typeof l&&"state"===l.label_mode?this._formatters.formatEntityState(d):"string"!=typeof l&&"attribute"===l.label_mode&&void 0!==l.attribute?this._formatters.formatEntityAttributeValue(d,l.attribute):null!=c?c:h.split(" ").map(t=>t[0]).join("").substr(0,3),L=$(l),S=Y(this._entityMarkers,L,!o.has(L));o.add(L),S.showIcon="string"!=typeof l&&"icon"===l.label_mode,S.entityId=L,S.entityName=P,S.entityUnit="string"!=typeof l&&l.unit&&"attribute"===l.label_mode?l.unit:"",S.entityPicture=!y||"string"!=typeof l&&l.label_mode?"":this._connection.hassUrl(y);const A=("string"!=typeof l?l.color:void 0)||(0,x.lb)(L,this._entityReg,i);S.entityColor=A,S.selected="string"!=typeof l&&null!==(r=l.selected)&&void 0!==r&&r;const F={entityId:L,title:h,picture:S.entityPicture||void 0,label:P,showIcon:S.showIcon,unit:null!==(n=S.entityUnit)&&void 0!==n?n:"",color:A,selected:S.selected,zoneId:["person","device_tracker"].includes((0,g.t)(d))?null!==(s=a[d.state])&&void 0!==s?s:this._zoneContaining(E):void 0},R=!(!z||"string"!=typeof l&&l.hide_accuracy),Z=this._getMarkerSize(i);this._entityHandles.push(e.addMarker(S,E,{size:[Z,Z],title:h,cluster:!0,clusterData:F,decoration:R?{radius:z,color:A}:void 0})),"string"!=typeof l&&!1===l.focus||this._focusPoints.push(E)}const l=new Set(this.entities.map($));for(const t of[this._entityMarkers,this._clusterAvatars])for(const e of t.keys())l.has(e)||t.delete(e);e.setClustering(this.clusterMarkers?{radius:X,iconBuilder:this._createClusterBubble,groupKey:t=>{var e;return null===(e=t.clusterData)||void 0===e?void 0:e.zoneId},groupRadius:Q}:null)}_zoneContaining(t){let e,i=1/0;for(const[a,o]of Object.entries(this._zoneRadii))o<i&&(0,_.S_)(t,this._zonePositions[a])<=o&&(e=a,i=o);return e}_drawScaleRuler(){var t,e;null===(t=this._engine)||void 0===t||t.setScaleRuler(this.scaleRuler?{metric:"km"===(null===(e=this._config)||void 0===e||null===(e=e.unit_system)||void 0===e?void 0:e.length)}:null)}_getMarkerSize(t){const e=t.getPropertyValue("--ha-marker-size"),i=parseFloat(e);return Number.isNaN(i)?48:i}async _attachObserver(){this._resizeObserver||(this._resizeObserver=new ResizeObserver(()=>{var t;null===(t=this._engine)||void 0===t||t.invalidateSize(),this._runPendingFit()})),this._resizeObserver.observe(this)}constructor(...t){super(...t),this.clickable=!1,this.autoFit=!1,this.renderPassive=!1,this.interactiveZones=!1,this.fitZones=!1,this.zoomPosition="topleft",this._zonePositions={},this._zoneRadii={},this.themeMode="auto",this.zoom=14,this.clusterMarkers=!0,this.scaleRuler=!1,this._loaded=!1,this._editableHandles=new Map,this._entityReg=[],this._entityHandles=[],this._entityMarkers=new Map,this._clusterAvatars=new Map,this._zoneHandles=[],this._pathHandles=[],this._focusPoints=[],this._focusZonePoints=[],this._clickCount=0,this._isProgrammaticFit=!1,this._pauseAutoFit=!1,this._handleVisibilityChange=async()=>{document.hidden||setTimeout(()=>{this._pauseAutoFit=!1},500)},this._resolveMapStyle=(0,c.A)(k.kR),this._loading=!1,this._forceLeaflet=!1,this._setupAttempt=0,this._hasFitted=!1,this._createClusterBubble=(t,e,i,a=!1)=>{var r;const n=t.map(t=>t.clusterData),s=a?n:n.slice(0,D),l=n.length-s.length,d=!(null===(r=this.paths)||void 0===r||!r.length),c=document.createElement("div");c.className="cluster-bubble";const h=new Set;for(const t of s){var u,p,b,m,g,v;const e=Y(this._clusterAvatars,null==t?void 0:t.entityId,!h.has(null!==(u=null==t?void 0:t.entityId)&&void 0!==u?u:""));var f;if(null!=t&&t.entityId&&h.add(t.entityId),e.entityId=null==t?void 0:t.entityId,e.entityName=null!==(p=null==t?void 0:t.label)&&void 0!==p?p:"",e.entityUnit=null!==(b=null==t?void 0:t.unit)&&void 0!==b?b:"",e.showIcon=null!==(m=null==t?void 0:t.showIcon)&&void 0!==m&&m,e.entityPicture=null!==(g=null==t?void 0:t.picture)&&void 0!==g?g:"",e.entityColor=null==t?void 0:t.color,d)e.style.setProperty("--ha-marker-color",null!==(f=null==t?void 0:t.color)&&void 0!==f?f:"var(--primary-color)"),e.style.setProperty("--ha-marker-border-width","2px");else e.style.removeProperty("--ha-marker-color"),e.style.removeProperty("--ha-marker-border-width");e.selected=null!==(v=null==t?void 0:t.selected)&&void 0!==v&&v,(0,z.I)(e),a&&(0,z.l)(e,null==t?void 0:t.title,!0),c.appendChild(e)}const y=a?Math.max(1,Math.floor((this.offsetWidth-2*W-2*O+N)/(j+N))):s.length,_=Math.min(s.length,y),k=Math.ceil(s.length/y);let w=_*j+(_-1)*N+2*O;if(l>0){const t=document.createElement("span");t.className="more",t.textContent=l>V?`${V}+`:`+${l}`,c.appendChild(t),w+=U+N}const M=i?this._zonePositions[i]:void 0,x=!!M;let C=k*j+(k-1)*N+2*O,E=c;if(x){E=document.createElement("div"),E.className="cluster-marker";const t=document.createElement("div");t.className="cluster-bubble-tail",E.append(c,t),C+=G}return(0,o.A)({element:E,size:[w,C]},x&&M?{location:M,anchor:[w/2,C+18+K]}:{})}}}tt.styles=(0,l.AH)(R||(R=Z`
    :host {
      display: block;
      height: 300px;
    }
    #map {
      height: 100%;
      /* A cluster bubble and its tail cast a single shadow around their
         combined silhouette (drop-shadow on the wrapper), so no shadow seam
         appears between the bubble and its tail. */
      --ha-cluster-shadow: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.08))
        drop-shadow(0 1px 3px rgba(0, 0, 0, 0.12));
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
      background: #090909;
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
    ${0}
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
      width: ${0}px;
      height: ${0}px;
      margin-top: ${0}px;
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
      gap: ${0}px;
      padding: ${0}px;
      box-sizing: border-box;
      background: var(--card-background-color, #fff);
      border-radius: 14px;
      filter: var(--ha-cluster-shadow);
      --ha-marker-size: ${0}px;
      --ha-marker-color: transparent;
      --ha-marker-border-width: 1px;
      --ha-marker-shadow: none;
      --ha-marker-font-size: var(--ha-font-size-s);
      /* distinguish letter tiles from the bubble background */
      --ha-marker-background: var(--ha-color-fill-neutral-quiet-resting);
    }
    .cluster-bubble .more {
      flex: none;
      width: ${0}px;
      height: ${0}px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 10px;
      background: var(--ha-color-fill-neutral-quiet-resting, #f0f0f0);
      color: var(--primary-text-color, #212121);
      font-size: var(--ha-font-size-s);
      font-weight: var(--ha-font-weight-medium);
    }
    /* Markers are rounded squares to match the cluster bubble avatars */
    ha-entity-marker {
      --ha-marker-border-radius: var(--ha-border-radius-lg);
    }
    .cluster-bubble ha-entity-marker {
      flex: none;
      --ha-marker-border-radius: 10px;
    }
    ${0}
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

    ha-icon {
      --mdc-icon-size: calc(var(--ha-marker-size, 48px) / 2);
    }
  `),(0,l.iz)(M.xr),q,q,-q/2,N,O,j,U,j,(0,l.iz)(C.Nr)),(0,n.Cg)([(0,d.wk)(),(0,h.F)({context:L.iN,subscribe:!0})],tt.prototype,"_states",void 0),(0,n.Cg)([(0,d.wk)(),(0,h.F)({context:L.WF,subscribe:!0}),(0,b.p)({transformer:({config:t})=>t})],tt.prototype,"_config",void 0),(0,n.Cg)([(0,d.wk)(),(0,h.F)({context:L.EK,subscribe:!0})],tt.prototype,"_ui",void 0),(0,n.Cg)([(0,d.wk)(),(0,h.F)({context:L.D5,subscribe:!0})],tt.prototype,"_i18n",void 0),(0,n.Cg)([(0,d.wk)(),(0,h.F)({context:L.p0,subscribe:!0})],tt.prototype,"_formatters",void 0),(0,n.Cg)([(0,d.wk)(),(0,h.F)({context:L.Wq,subscribe:!0})],tt.prototype,"_connection",void 0),(0,n.Cg)([(0,d.MZ)({attribute:!1})],tt.prototype,"entities",void 0),(0,n.Cg)([(0,d.MZ)({attribute:!1})],tt.prototype,"paths",void 0),(0,n.Cg)([(0,d.MZ)({attribute:!1})],tt.prototype,"editableLocations",void 0),(0,n.Cg)([(0,d.MZ)({type:Boolean})],tt.prototype,"clickable",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"auto-fit",type:Boolean})],tt.prototype,"autoFit",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"render-passive",type:Boolean})],tt.prototype,"renderPassive",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"interactive-zones",type:Boolean})],tt.prototype,"interactiveZones",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"fit-zones",type:Boolean})],tt.prototype,"fitZones",void 0),(0,n.Cg)([(0,d.MZ)({attribute:!1})],tt.prototype,"fitPadding",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"zoom-position"})],tt.prototype,"zoomPosition",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"theme-mode",type:String})],tt.prototype,"themeMode",void 0),(0,n.Cg)([(0,d.MZ)({attribute:!1})],tt.prototype,"mapStyle",void 0),(0,n.Cg)([(0,d.MZ)({type:Number})],tt.prototype,"zoom",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"cluster-markers",type:Boolean})],tt.prototype,"clusterMarkers",void 0),(0,n.Cg)([(0,d.MZ)({attribute:"scale-ruler",type:Boolean})],tt.prototype,"scaleRuler",void 0),(0,n.Cg)([(0,d.wk)()],tt.prototype,"_loaded",void 0),(0,n.Cg)([(0,d.P)("#map")],tt.prototype,"_mapElement",void 0),(0,n.Cg)([(0,d.wk)()],tt.prototype,"_entityReg",void 0),tt=(0,n.Cg)([(0,d.EM)("ha-map")],tt),i.d(e,{},{$:H}),a()}catch(t){a(t)}})},5792(t,e,i){i(19843),i(21323),i(88642),i(62758),i(24791),i(53457),i(73532),i(34737),i(4666),i(77809),i(92653),i(6667),i(48),i(89199),i(79391),i(43547),i(98434),i(5297),i(61460);var a=i(42006),o=i(81541);const r="X-Map-Tiles-Token",n=[0,400,1e3],s=[2e3,5e3,1e4,15e3];let l,d,c,h,u,p,b,m;const g=new Set,v=async t=>{const e=await t.sendMessagePromise({type:"map_tiles/access_token"});e.token!==l&&(l=e.token,g.forEach(t=>t(l)))},f=async(t,e)=>{for(const i of e){if(l)return;i&&await(0,o.l)(i);try{return void await v(t)}catch(t){}}},y=()=>{if(!b)return;const t=b;v(t).then(()=>_(t)).catch(()=>{})},_=t=>{var e;(l&&!u&&(u=setInterval(()=>{v(null!=b?b:t).catch(()=>{})},12e5)),p!==t)&&(null===(e=p)||void 0===e||e.removeEventListener("ready",y),p=t,t.addEventListener("ready",y))},k=()=>(null!=d?d:location.origin).replace(/\/+$/,"");i.d(e,{ZV:()=>a.Z},{Oc:()=>b?(null!=m||(m=v(b).catch(()=>{}).finally(()=>{m=void 0})),m):Promise.resolve(),Xx:t=>(g.add(t),()=>g.delete(t)),bK:t=>t.startsWith("/")?`${k()}${t}`:t,pW:async t=>{var e;if(b=t,d=null===(e=t.options.auth)||void 0===e?void 0:e.data.hassUrl,l||(null!=c||(c=f(t,n).finally(()=>{c=void 0})),await c),l)return _(t),l;null!=h||(h=f(t,s).then(()=>_(t)).finally(()=>{h=void 0}))},rG:t=>{let e;try{e=new URL(t,k())}catch(e){return{url:t}}if(!e.pathname.startsWith(`${a.Z}/`))return{url:e.href};const i=new URL(`${k()}${e.pathname}${e.search}`);return l?i.origin===location.origin?{url:i.href,headers:{[r]:l}}:(i.searchParams.set("token",l),{url:i.href}):{url:i.href}}})}}]);
//# sourceMappingURL=49854.c7ea0fe5b9851e63.js.map