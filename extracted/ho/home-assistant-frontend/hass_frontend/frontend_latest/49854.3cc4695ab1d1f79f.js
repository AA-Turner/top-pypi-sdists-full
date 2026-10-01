export const __rspack_esm_id=49854;export const __rspack_esm_ids=[49854];export const __webpack_modules__={60057(t,e,i){var a=i(97377);i.d(e,{},{H:(t,e)=>{const{latitude:i,longitude:o,gps_accuracy:r}=t.attributes;if("number"==typeof i&&"number"==typeof o)return{latitude:i,longitude:o,gpsAccuracy:r};if("person"!==(0,a.t)(t))return;const n=t.attributes.in_zones;if(!Array.isArray(n)||0===n.length)return;const s=((t,e)=>{for(const i of t){const t=e[i];if(t&&!t.attributes.passive&&"number"==typeof t.attributes.latitude&&"number"==typeof t.attributes.longitude)return t}})(n,e);return s?{latitude:s.attributes.latitude,longitude:s.attributes.longitude}:void 0}})},51139(t,e,i){i(47144),i(8021),i(89542);var a=i(25071),o=i(5792);const r={light:"/static/map/light.json",dark:"/static/map/dark.json"},n=`${o.ZV}/raster/{z}/{x}/{y}.png?token={token}`;let s;const l=()=>(()=>{if(void 0===s)try{const t=document.createElement("canvas").getContext("webgl2");s=Boolean(t),t?.getExtension("WEBGL_lose_context")?.loseContext()}catch{s=!1}return s})()&&"function"==typeof BigInt,c=t=>new URL(t,location.href).href,d=async t=>{const e=t.shipped&&r[t.shipped],a=e?await(await fetch(e)).json():await(await i.e(60532).then(i.bind(i,94335))).buildMapStyle(t.palette,t.options??{},t.baseColors);return"string"==typeof a.sprite?a.sprite=c(a.sprite):Array.isArray(a.sprite)&&(a.sprite=a.sprite.map(t=>({...t,url:c(t.url)}))),a};let h=!1;const u=t=>{h||(h=!0,t(new URL("/frontend_latest/maplibre-gl-worker.20260930.0.js",location.href).href))};let p=!1;const b=t=>{p||(p=!0,t(new URL("/static/map/mapbox-gl-rtl-text.js",location.href).href,!0).catch(()=>{}))},m=(t,e,i)=>{const a=t.tileLayer((0,o.bK)(n),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',maxZoom:20,maxNativeZoom:19,referrerPolicy:void 0,token:i??""}).addTo(e),r=(0,o.Xx)(t=>{a.options.token=t,a.redraw()});return e.on("unload",r),{setMapStyle:()=>{}}};i.d(e,{},{MK:d,V4:async(t,e,r,n,s=!1)=>{if(!s&&l()){let s;try{const[{maplibreGL:l},c]=await Promise.all([Promise.all([i.e(79871),i.e(54730),i.e(35166),i.e(88580)]).then(i.bind(i,2797)),Promise.all([i.e(79871),i.e(54730),i.e(69688)]).then(i.bind(i,46513))]);u(c.setWorkerUrl),b(c.setRTLTextPlugin),s=await(async(t,e,i,r,n)=>{let s;try{s=t({style:await d(r),transformRequest:t=>({...(0,o.rG)(t),referrerPolicy:void 0})}),s.addTo(i)}catch{if(s)try{s.remove()}catch{}return}let l=r,c=r,h=0,u=!0,p=!1;const b=s.getMaplibreMap();let g,f=!1;const y=()=>{f&&v()},_=()=>{u=!1,document.removeEventListener("visibilitychange",y);try{s.remove()}catch{}m(e,i,n)},v=()=>{clearTimeout(g),u&&!document.hidden&&(g=window.setTimeout(_,2e3))};b.on("webglcontextlost",()=>{f=!0,v()}),b.on("webglcontextrestored",()=>{f=!1,clearTimeout(g)}),document.addEventListener("visibilitychange",y),i.on("unload",()=>{clearTimeout(g),document.removeEventListener("visibilitychange",y)});const k=t=>{const e=++h;d(t).then(i=>{e===h&&(l=t,s.getMaplibreMap()?.setStyle(i))}).catch(()=>{e===h&&(c=l)})};let w=0;b.on("error",t=>{const e=t.error?.status;void 0!==e&&403!==e&&404!==e||Date.now()-w<3e4||(w=Date.now(),p=!0,(0,o.Oc)())});const M=(0,o.Xx)(()=>{u&&p&&(p=!1,k(c))});return i.on("unload",M),{setMapStyle:t=>{u&&!(0,a.b)(t,c)&&(c=t,k(t))}}})(l,t,e,r,n)}catch{}if(s)return s}return m(t,e,n)},W$:u,jV:l,vM:b})},55659(t,e,i){i.d(e,{},{rx:t=>{const e=document.createElement("div");e.className="editable-circle-resize",e.tabIndex=0,e.setAttribute("role","slider"),e.setAttribute("aria-valuemin","1"),e.setAttribute("aria-valuemax",String(1e5)),t&&e.setAttribute("aria-label",t);const i=document.createElement("div");return i.className="editable-circle-resize-dot",e.appendChild(i),e},xr:"\n  .editable-circle-center {\n    width: 16px;\n    height: 16px;\n    border-radius: 50%;\n    background: var(--primary-color);\n    border: 2px solid var(--card-background-color, #fff);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n  .editable-circle-resize {\n    width: 24px;\n    height: 24px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    cursor: ew-resize;\n  }\n  .editable-circle-resize-dot {\n    width: 12px;\n    height: 12px;\n    border-radius: 50%;\n    background: var(--card-background-color, #fff);\n    border: 2px solid var(--primary-color);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n"})},86233(t,e,i){const a=6371008.8,o=t=>t*Math.PI/180,r=t=>180*t/Math.PI,n=(t,e,i)=>{const n=e/a,s=o(t[0]),l=o(i),c=Math.asin(Math.sin(s)*Math.cos(n)+Math.cos(s)*Math.sin(n)*Math.cos(l)),d=Math.atan2(Math.sin(l)*Math.sin(n)*Math.cos(s),Math.cos(n)-Math.sin(s)*Math.sin(c));return[r(c),t[1]+r(d)]};i.d(e,{},{RO:(t,e)=>n(t,e,90),Rn:(t,e)=>{const i=e/a,n=Math.max(-90,t[0]-r(i)),s=Math.min(90,t[0]+r(i)),l=Math.sin(i)/Math.cos(o(t[0]));if(n<=-90||s>=90||Math.abs(l)>=1)return[[n,-180],[s,180]];const c=r(Math.asin(l));return[[n,t[1]-c],[s,t[1]+c]]},S_:(t,e)=>{const i=o(e[0]-t[0]),a=o(e[1]-t[1]),r=Math.sin(i/2)**2+Math.cos(o(t[0]))*Math.cos(o(e[0]))*Math.sin(a/2)**2;return 12742017.6*Math.asin(Math.sqrt(r))},bM:n})},28006(t,e,i){i.d(e,{jJ:()=>o,u8:()=>a,l6:()=>s,kR:()=>u,vA:()=>h});i(97700),i(47144),i(89542);const a=["default","colorful","natural","muted","gray","toner"],o="default",r={default:{palette:"colorful",colors:{background:"#f4efe6",land:"#f4efe6",water:"#bcd9e8",labelWater:"#5b86a3",natureWood:"#cfe1bf",natureGrass:"#e2ecda",naturePark:"#cfe1bf",natureLeisure:"#e2ecda",natureAgriculture:"#e8eee2",natureWetland:"#e5ebe0",natureSand:"#f1eadf",natureRock:"#f1eadf",glacier:"#f9f6f1",areaResidential:"#efe8dc",areaCommercial:"#f4e1db",areaIndustrial:"#ede5ce",areaWaste:"#ece3d5",areaBurial:"#efe8dc",siteParking:"#ede6d8",siteSports:"#cfe1bf26",building:"#e7ddca",buildingBg:"#dcccb2",roadStreet:"#fcfaf8",roadStreetBg:"#e6dac7",roadTrunk:"#fbe6c2",roadTrunkBg:"#e5cea5",roadMotorway:"#ebd4ab",roadMotorwayBg:"#deba78",transitRail:"#e9dfce",transitSubway:"#eae1d1",transitCycle:"#f2ede3",transitFoot:"#f2ede3",boundary:"#d6c3a4",boundaryDisputed:"#e2d6c0",label:"#4a463d",labelHalo:"#faf8f5cc",labelSymbol:"#8d8676",labelPoi:"#8d867666",labelShield:"#faf8f4",labelHousenumber:"#8d86764d"},colorsDark:{background:"#191b2c",land:"#191b2c",water:"#27357a",labelWater:"#9cc0f0",natureWood:"#254948",natureGrass:"#213b39",naturePark:"#28504b",natureLeisure:"#213532",natureAgriculture:"#203233",natureWetland:"#253337",natureSand:"#2a2c3d",natureRock:"#2a2c3d",glacier:"#2a2c3d",areaResidential:"#1d2034",areaCommercial:"#29213a",areaIndustrial:"#242431",areaWaste:"#1d2034",areaBurial:"#1d2034",siteParking:"#1d2034",siteSports:"#25413926",building:"#21243c",buildingBg:"#2a2e4a",roadStreet:"#2b3052",roadStreetBg:"#1a1d33",roadTrunk:"#383e67",roadTrunkBg:"#22263f",roadMotorway:"#454d7d",roadMotorwayBg:"#2a2f4c",transitRail:"#2c3150",transitSubway:"#2c3150",transitCycle:"#2b3052",transitFoot:"#2b3052",boundary:"#3b4068",boundaryDisputed:"#3b4068",label:"#e7ecf8",labelHalo:"#12141fcc",labelSymbol:"#959dbd",labelPoi:"#959dbd66",labelShield:"#191b2c",labelHousenumber:"#959dbd4d"}},colorful:{palette:"colorful"},natural:{palette:"natural"},muted:{palette:"muted"},gray:{palette:"gray"},toner:{palette:"toner"}},n=t=>a.includes(t),s=t=>"object"==typeof t&&null!==t,l=["colors","recolor","text","icon","layers"],c=t=>t.replace(/_([a-z])/g,(t,e)=>e.toUpperCase()),d=t=>Array.isArray(t)?t.map(d):t&&"object"==typeof t?Object.fromEntries(Object.entries(t).map(([t,e])=>[c(t),d(e)])):t,h=(t,e)=>{const i=n(e)&&e!==o?e:void 0,a=s(t)?{...t}:{};return delete a.base,Object.keys(a).length?{...i&&{base:i},...a}:i},u=(t,e,i)=>{const a=s(t)?t:void 0,h=a?a.base:t,u=n(h)?h:o,p=((t,e)=>{const{palette:i}=r[t];return e?`${i}-dark`:i})(u,e),b=a?((t,e)=>{const i=t,a={};for(const t of l){const e=i[t]??i[c(t)];void 0!==e&&(a[c(t)]=d(e))}const o=i.colors_dark;return e&&void 0!==o&&(a.colors=d(o)),a})(a,e):{},m=Object.keys(b).length>0,{colors:g,colorsDark:f}=r[u],y=(e?f:g)??g;if((y||i)&&(b.colors={...y,...i,...b.colors}),!Object.keys(b).length)return{palette:p};const _=y?{baseColors:y}:{};return u===o&&(!i&&!m)?{palette:p,options:b,..._,shipped:e?"dark":"light"}:{palette:p,options:b,..._}}},71760(t,e,i){i(47144),i(21927),i(25744),i(89542),i(99686);const a={"--ha-color-map-land":["background","land"],"--ha-color-map-water":["water"],"--ha-color-map-green":["naturePark","natureWood","natureGrass","natureLeisure","natureWetland","siteSports"],"--ha-color-map-area":["areaResidential","areaCommercial","areaIndustrial","areaWaste","areaBurial","siteParking","natureAgriculture","natureSand","natureRock"],"--ha-color-map-building":["building"],"--ha-color-map-building-outline":["buildingBg"],"--ha-color-map-road":["roadStreet"],"--ha-color-map-road-major":["roadMotorway","roadTrunk"],"--ha-color-map-road-outline":["roadStreetBg","roadTrunkBg","roadMotorwayBg"],"--ha-color-map-transit":["transitRail","transitSubway","transitCycle","transitFoot"],"--ha-color-map-boundary":["boundary","boundaryDisputed"],"--ha-color-map-label":["label"],"--ha-color-map-label-halo":["labelHalo"],"--ha-color-map-label-secondary":["labelSymbol","labelPoi","labelHousenumber"]},o={siteSports:.15,labelHalo:.8,labelPoi:.4,labelHousenumber:.3},r=/^#([0-9a-f]{3,8})$/i,n=/^rgba?\(([^)]+)\)$/i,s=/^color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\s*\)$/i,l=t=>{const e=t.match(r);if(e){const t=e[1],i=3===t.length||4===t.length,a=e=>i?parseInt(t[e]+t[e],16):parseInt(t.slice(2*e,2*e+2),16);if(3===t.length||4===t.length||6===t.length||8===t.length){const e=4===t.length||8===t.length?a(3)/255:1;return[a(0),a(1),a(2),e]}return}const i=t.match(n);if(i){const t=i[1].split(/[,\s/]+/).filter(Boolean).map(Number);if(t.length<3||t.slice(0,3).some(Number.isNaN))return;return[t[0],t[1],t[2],t[3]??1]}const a=t.match(s);if(a){const t=t=>Math.round(255*Number(t));return[t(a[1]),t(a[2]),t(a[3]),Number(a[4]??1)]}},c=[1,2,3,1],d=(t,e)=>{const i=document.createElement("span");i.style.cssText="display:none;color:rgb(1, 2, 3)";const a=document.createElement("span");a.style.color=`var(${e})`,i.append(a),t.append(i);const o=l(getComputedStyle(a).color);return i.remove(),o&&o.every((t,e)=>t===c[e])?void 0:o};i.d(e,{},{Q:t=>{const e=getComputedStyle(t);let i;for(const[r,n]of Object.entries(a)){const a=e.getPropertyValue(r).trim();if(!a)continue;const s=l(a)??d(t,r);if(!s)continue;i??={};const[c,h,u,p]=s;for(const t of n){const e=Math.round(p*(o[t]??1)*1e3)/1e3;i[t]=`rgba(${c},${h},${u},${e})`}}return i}})},52573(t,e,i){i(47144),i(25744),i(8021);const a="haMapA11y",o=t=>{const e=t.dataset[a];void 0!==e&&(e.split(" ").filter(Boolean).forEach(e=>t.removeAttribute(e)),delete t.dataset[a])};i.d(e,{},{I:o,l:(t,e,i)=>{o(t);const r=[];!e||t.hasAttribute("aria-label")||t.hasAttribute("aria-labelledby")||(t.setAttribute("aria-label",e),r.push("aria-label")),t.hasAttribute("role")||(i?(t.setAttribute("role","button"),r.push("role")):e?(t.setAttribute("role","img"),r.push("role")):(t.setAttribute("aria-hidden","true"),r.push("aria-hidden"))),i&&!t.hasAttribute("tabindex")&&(t.tabIndex=0,r.push("tabindex")),t.dataset[a]=r.join(" ")}})},7952(t,e,i){var a=i(65541),o=i.n(a);i.d(e,{},{D:t=>o()(t,{whiteList:{},stripIgnoreTag:!0,stripIgnoreTagBody:!0})})},14279(t,e,i){i.a(t,async function(t,e){try{var a=i(89797),o=i(20686),r=i(32379),n=i(66543),s=i(70465),l=i(86075),c=i(32323),d=t([c]);c=(d.then?(await d)():d)[0];class h extends o.WF{render(){return o.qy` <div part="marker" class="marker ${this.entityPicture?"picture":""}" style=${(0,n.W)({"--ha-marker-selected-color":this.entityColor})}; @click=${this._badgeTap}> ${this.entityPicture?o.qy`<div part="picture" class="entity-picture" style=${(0,n.W)({"background-image":`url(${this.entityPicture})`})};></div>`:this.showIcon&&this.entityId?o.qy`<ha-state-icon .stateObj=${this._stateObj}></ha-state-icon>`:this.entityUnit?o.qy` ${this.entityName} <span class="unit" style="display:${this.entityUnit?"initial":"none"}">${this.entityUnit}</span> `:this.entityName} </div> `}connectedCallback(){super.connectedCallback(),this.addEventListener("keydown",this._handleKeydown)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("keydown",this._handleKeydown)}_badgeTap(t){t.stopPropagation(),this.entityId&&(0,l.r)(this,"hass-more-info",{entityId:this.entityId})}constructor(...t){super(...t),this.showIcon=!1,this.selected=!1,this._handleKeydown=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._badgeTap(t))}}}h.styles=o.AH`.marker{text-align:center;box-sizing:border-box;width:var(--ha-marker-size,48px);height:var(--ha-marker-size,48px);font-size:var(--ha-marker-font-size,var(--ha-font-size-xl));border-radius:var(--ha-marker-border-radius,50%);border:var(--ha-marker-border-width,3px) solid var(--ha-marker-color,var(--card-background-color,#fff));box-shadow:var(--ha-marker-shadow,var(--ha-box-shadow-s));color:var(--primary-text-color);background-color:var(--ha-marker-background,var(--card-background-color));justify-content:center;align-items:center;display:flex}.marker.picture{overflow:hidden}:host([selected]) .marker{outline:3px solid var(--ha-marker-selected-color,var(--primary-color))}.entity-picture{background-size:cover;width:100%;height:100%}.unit{margin-left:2px}`,(0,a.Cg)([(0,r.MZ)({attribute:"entity-id",reflect:!0})],h.prototype,"entityId",void 0),(0,a.Cg)([(0,r.wk)(),(0,s.fI)({entityIdPath:["entityId"]})],h.prototype,"_stateObj",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-name"})],h.prototype,"entityName",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-unit"})],h.prototype,"entityUnit",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-picture"})],h.prototype,"entityPicture",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"entity-color"})],h.prototype,"entityColor",void 0),(0,a.Cg)([(0,r.MZ)({attribute:"show-icon",type:Boolean})],h.prototype,"showIcon",void 0),(0,a.Cg)([(0,r.MZ)({type:Boolean,reflect:!0})],h.prototype,"selected",void 0),h=(0,a.Cg)([(0,r.EM)("ha-entity-marker")],h),e()}catch(t){e(t)}})},25581(t,e,i){i.a(t,async function(t,a){try{i(97700),i(47144),i(8021),i(89542),i(25102),i(47508),i(24791),i(77809),i(92653);var o=i(89797),r=i(58012),n=i(20686),s=i(32379),l=i(19741),c=i(98878),d=i(37151),h=i(6694),u=(i(60666),i(11808)),p=i(86075),b=i(97377),m=i(65942),g=i(60057),f=i(51139),y=i(86233),_=i(28006),v=i(71760),k=i(55659),w=i(89275),M=i(52573),x=i(62727),z=i(25071),C=i(7952),E=i(66572),P=i(5792),L=i(14279),S=t([L,d,h]);[L,d,h]=S.then?(await S)():S;const F=250,A=t=>"string"==typeof t?t:t.entity_id,R=["name","state","attribute","icon"],Z=(t,e)=>t.element===e.element&&t.title===e.title&&t.color===e.color&&t.locationEditable===e.locationEditable&&t.radiusEditable===e.radiusEditable&&t.activatable===e.activatable&&t.elementSize?.[0]===e.elementSize?.[0]&&t.elementSize?.[1]===e.elementSize?.[1],I=t=>({addDraggableMarker:(e,i,a)=>{let o=i,r=t.addMarker(e,o,a);return{get location(){return o},clusterData:a.clusterData,setLocation:i=>{r.remove(),o=i,r=t.addMarker(e,o,a)},remove:()=>r.remove()}},addEditableCircle:(e,i)=>{const a=i.centerElement??document.createElement("div");let o;if(i.centerElement||(a.className="editable-circle-center"),i.onClick){const t=t=>{t.stopPropagation(),i.onClick()},e=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),i.onClick())};a.addEventListener("click",t),a.addEventListener("keydown",e),o=()=>{a.removeEventListener("click",t),a.removeEventListener("keydown",e)}}let r={center:e,radius:i.radius},n=[];const s=()=>{n=[t.addCircle(r.center,{radius:r.radius,color:i.color}),t.addMarker(a,r.center,{size:i.centerSize??[16,16],interactive:!!i.onClick,title:i.title})]};return s(),{get center(){return r.center},get radius(){return r.radius},update:(t,e)=>{n.forEach(t=>t.remove()),r={center:t,radius:e},s()},remove:()=>{o?.(),n.forEach(t=>t.remove())}}}}),$=32,H=6,B=4,T=12,j=3,O=28,N=99,W=10,D=Math.round(W*Math.SQRT2/2),U=2,V=40,q=160,G=t=>{const e=t.replace(".","-");return`marker, picture, marker: marker-${e}, picture: picture-${e}`},K=(t,e,i=!0)=>{const a=e&&i?t.get(e):void 0;if(a&&!a.isConnected)return a;const o=document.createElement("ha-entity-marker");return e&&(o.setAttribute("exportparts",G(e)),t.set(e,o)),o};class X extends n.mN{connectedCallback(){this._pauseAutoFit=!1,document.addEventListener("visibilitychange",this._handleVisibilityChange),this._handleVisibilityChange(),super.connectedCallback(),this._loadMap(),this._attachObserver()}_watchRegistry(){!this._registryConsumer&&this.entities?.length&&(this._registryConsumer=new c.T(this,E.ih,t=>{this._entityReg=t}))}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("visibilitychange",this._handleVisibilityChange),this._engine?.destroy(),this._engine=void 0,this._setupAttempt++,this._startingEngine?.destroy(),this._startingEngine=void 0,this._loading=!1,this._entityHandles=[],this._entityMarkers.clear(),this._clusterAvatars.clear(),this._zoneHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}update(t){if(super.update(t),!this._loaded)return;let e=!1;const i=t.get("_states");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),e=!this._pauseAutoFit;else if(this._loaded&&i&&this.entities)for(const t of this.entities)if(i[A(t)]!==this._states[A(t)]){this._drawEntities(),e=!this._pauseAutoFit;break}(t.has("clusterMarkers")||t.has("_entityReg"))&&this._drawEntities(),t.has("fitPadding")&&!(0,z.b)(t.get("fitPadding"),this.fitPadding)&&(e=!this._pauseAutoFit),t.has("zoomPosition")&&this._engine?.setZoomControlPosition(this.zoomPosition);const a=t.get("_config");if((t.has("_loaded")||t.has("scaleRuler")||t.has("_config")&&a?.unit_system?.length!==this._config?.unit_system?.length)&&this._drawScaleRuler(),t.has("_loaded")||t.has("paths")){this._drawPaths();const e=t.get("paths");!!e?.length!=!!this.paths?.length&&this._engine?.refreshClusters()}t.has("_loaded")||t.has("editableLocations")?this._drawEditableLocations()&&(e=!0):t.has("_i18n")&&this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()),t.has("_loaded")&&this._pendingFit?this._runPendingFit():(t.has("_loaded")||this.autoFit&&e)&&this.fitMap(),t.has("zoom")&&this._withProgrammaticFit(()=>{this._engine.setZoom(this.zoom)}),t.has("mapStyle")&&this._engine?.setMapStyle(this._resolvedMapStyle);const o=t.get("_ui");(t.has("themeMode")||t.has("_ui")&&(!o||o.themes!==this._ui.themes))&&(this._updateMapAppearance(),this._drawEntities(),this._drawPaths(),this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()))}get _darkMode(){return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(this._ui?.themes?.darkMode)}_readThemeColors(){const t=Boolean(this._ui?.themes?.darkMode),e=this._darkMode===t?(0,v.Q)(this):void 0;(0,z.b)(e,this._themeColors)||(this._themeColors=e)}get _resolvedMapStyle(){return this._resolveMapStyle(this.mapStyle,this._darkMode,this._themeColors)}_updateMapAppearance(){this._readThemeColors();const t=this._mapElement;t.classList.toggle("clickable",this.clickable),t.classList.toggle("dark",this._darkMode),t.classList.toggle("forced-dark","dark"===this.themeMode),t.classList.toggle("forced-light","light"===this.themeMode),this._engine?.setMapStyle(this._resolvedMapStyle)}async _createEngine(){if(this._forceLeaflet||!(0,f.jV)()){return new((await Promise.all([i.e(79871),i.e(35166),i.e(8200)]).then(i.bind(i,859))).LeafletMapEngine)}return new((await i.e(41645).then(i.bind(i,64988))).MapLibreMapEngine)}async _loadMap(){const t=this._forceLeaflet||!(0,f.jV)();try{await this._setUpEngine()}catch(e){if(!this.isConnected)return;if(t)throw e;this._forceLeaflet=!0,await this._loadMap()}}async _setUpEngine(){if(this._loading)return;this.shadowRoot.getElementById("map")?.remove();const t=document.createElement("div");t.id="map",this.shadowRoot.append(t),this._loading=!0;const e=++this._setupAttempt;let i;try{const a=this._connection?await(0,P.pW)(this._connection.connection):void 0;this._readThemeColors();const o=this._forceLeaflet;if(i=await this._createEngine(),e!==this._setupAttempt)return;if(this._startingEngine=i,await i.init(t,{center:[this._config?.latitude??52.3731339,this._config?.longitude??4.8903147],zoom:this.zoom,mapStyle:this._resolvedMapStyle,token:a,rasterOnly:this._forceLeaflet,zoomControlPosition:this.zoomPosition,events:{click:t=>this._handleEngineClick(t),zoomStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},moveStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},fatal:()=>this._handleEngineFatal()}}),!this.isConnected||e!==this._setupAttempt)return;if(this._forceLeaflet&&!o)throw new Error("Map engine failed during setup");this._engine=i,this._updateMapAppearance(),this._loaded=!0,(0,p.r)(this,"editing-available-changed",{available:!!i.editing})}finally{e===this._setupAttempt&&(this._loading=!1,this._startingEngine=void 0),i&&i!==this._engine&&i.destroy()}}_handleEngineFatal(){this._forceLeaflet||(this._forceLeaflet=!0,this._loading?this._startingEngine?.destroy():(this._engine?.destroy(),this._engine=void 0,this._entityHandles=[],this._zoneHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._loadMap()))}_handleEngineClick(t){0===this._clickCount&&setTimeout(()=>{1===this._clickCount&&(0,p.r)(this,"map-clicked",{location:t}),this._clickCount=0},250),this._clickCount++}_withProgrammaticFit(t){this._isProgrammaticFit=!0,t(),setTimeout(()=>{this._isProgrammaticFit=!1},F)}fitMap(t){if(t?.unpause_autofit&&(this._pauseAutoFit=!1),!this._engine||!this._config)return;if(this._deferIfUnsized(()=>this.fitMap(t)))return;if(!this._focusPoints.length&&!this._focusZonePoints.length&&!this.editableLocations?.length)return this._withProgrammaticFit(()=>{this._engine.setView([this._config.latitude,this._config.longitude],t?.zoom||this.zoom)}),void(this._hasFitted=!0);const e=[...this._focusPoints,...this._focusZonePoints];this.editableLocations?.forEach(t=>{t.radius?e.push(...(0,y.Rn)(t.location,t.radius)):e.push(t.location)}),this._withProgrammaticFit(()=>{this._engine.fitBounds(e,{maxZoom:t?.zoom||this.zoom,pad:t?.pad??.5,padding:t?.padding??this.fitPadding,animate:this._hasFitted})}),this._hasFitted=!0}_deferIfUnsized(t){return this._engine.hasUsableSize()?(this._pendingFit=void 0,!1):(this._pendingFit=t,!0)}_runPendingFit(){if(this._pendingFit&&this._engine&&this._engine.hasUsableSize()){const t=this._pendingFit;this._pendingFit=void 0,t()}}panTo(t){this._engine?.panTo(t)}containsLocation(t){return this._engine?.containsLocation(t)??!1}setView(t,e){this._engine?(this._pendingFit=void 0,this._engine.setView(t,e)):this._pendingFit=()=>this.setView(t,e)}fitBounds(t,e){this._pauseAutoFit=!0,this._engine?this._deferIfUnsized(()=>this.fitBounds(t,e))||(this._withProgrammaticFit(()=>{this._engine.fitBounds(t,{maxZoom:e?.zoom||this.zoom,pad:e?.pad??.5,animate:this._hasFitted,padding:e?.padding})}),this._hasFitted=!0):this._pendingFit=()=>this.fitBounds(t,e)}_drawEditableLocations(){const t=this._engine;if(!t)return!1;const e=I(t),i=t.editing??e,a=new Set((this.editableLocations??[]).map(t=>t.id));let o=!1;for(const[t,e]of this._editableHandles)a.has(t)||(e.cleanup?.(),e.handle.remove(),this._editableHandles.delete(t),o=!0);if(!this.editableLocations)return o;const r=getComputedStyle(this).getPropertyValue("--accent-color");for(const t of this.editableLocations){const{id:a}=t,n=t.title??this._i18n?.localize("ui.components.map.location"),s=this._editableHandles.get(a),l=t.radius?"circle":"marker";if(s&&s.kind===l&&Z(s.source,t)){"circle"===s.kind?s.handle.update(t.location,t.radius):s.handle.setLocation(t.location),s.source=t;continue}if(s?(s.cleanup?.(),s.handle.remove()):o=!0,"circle"===l){this._editableHandles.set(a,{kind:l,source:t,handle:i.addEditableCircle(t.location,{radius:t.radius,color:t.color||r,centerElement:t.element,centerSize:t.elementSize,title:n,moveable:t.locationEditable,resizable:t.radiusEditable,resizeLabel:t.title?this._i18n?.localize("ui.components.map.radius_of",{name:t.title}):this._i18n?.localize("ui.components.map.radius"),onMove:t=>(0,p.r)(this,"editable-location-moved",{id:a,location:t}),onResize:t=>(0,p.r)(this,"editable-location-resized",{id:a,radius:t}),onClick:t.activatable?()=>(0,p.r)(this,"editable-location-clicked",{id:a}):void 0})});continue}const c=t.element??document.createElement("div");t.element||(c.className="editable-circle-center");let d,h=!1;if(t.activatable){const t=()=>{h=!1},e=t=>{t.stopPropagation(),h||(0,p.r)(this,"editable-location-clicked",{id:a})},i=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),(0,p.r)(this,"editable-location-clicked",{id:a}))};c.addEventListener("pointerdown",t),c.addEventListener("click",e),c.addEventListener("keydown",i),d=()=>{c.removeEventListener("pointerdown",t),c.removeEventListener("click",e),c.removeEventListener("keydown",i)}}const u=t.locationEditable?i:e;this._editableHandles.set(a,{kind:l,source:t,cleanup:d,handle:u.addDraggableMarker(c,t.location,{size:t.elementSize??[16,16],interactive:!0,focusable:!!t.activatable,title:n,onDragEnd:t=>{h=!0,(0,p.r)(this,"editable-location-moved",{id:a,location:t})}})})}return o}_removeEditableLocations(){for(const t of this._editableHandles.values())t.cleanup?.(),t.handle.remove();this._editableHandles.clear()}_computePathTooltip(t,e){let i;return i=t.fullDatetime?(0,d.r6)(e.timestamp,this._i18n.locale,this._config):(0,r.c)(e.timestamp)?(0,h.ie)(e.timestamp,this._i18n.locale,this._config):(0,h.Xs)(e.timestamp,this._i18n.locale,this._config),`${(0,C.D)(t.name??"")}<br>${i}`}_drawPaths(){if(!this._i18n||!this._config||!this._engine)return;if(this._pathHandles.length&&(this._pathHandles.forEach(t=>t.remove()),this._pathHandles=[]),!this.paths)return;const t=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach(e=>{let i,a;e.gradualOpacity&&(i=e.gradualOpacity/(e.points.length-2),a=1-e.gradualOpacity);const o=[],r=[];for(let t=0;t<e.points.length-1;t++){const n=e.gradualOpacity?a+t*i:void 0,s=e.points[t],l=e.points[t+1];if(r.push({location:s.point,opacity:n,tooltipHtml:this._computePathTooltip(e,s)}),Math.abs(s.point[1]-l.point[1])<=180)o.push({points:[s.point,l.point],opacity:n});else{const t=(l.point[1]-s.point[1]+540)%360-180;let e;e=0===t?(s.point[0]+l.point[0])/2:s.point[0]+(l.point[0]-s.point[0])*(s.point[1]>0?180-s.point[1]:-180-s.point[1])/t;const i=[e,s.point[1]>0?180:-180],a=[e,l.point[1]>0?180:-180];o.push({points:[s.point,i],opacity:n}),o.push({points:[a,l.point],opacity:n})}}const n=e.points.length-1;if(n>=0){const t=e.gradualOpacity?a+n*i:void 0;r.push({location:e.points[n].point,opacity:t,tooltipHtml:this._computePathTooltip(e,e.points[n])})}const s={color:e.color||t,segments:o,markers:r};this._pathHandles.push(this._engine.addPath(s))})}_drawEntities(){const t=this._states,e=this._engine;if(!t||!e)return;if(this._entityHandles.forEach(t=>t.remove()),this._entityHandles=[],this._focusPoints=[],this._zoneHandles.forEach(t=>t.remove()),this._zoneHandles=[],this._focusZonePoints=[],!this.entities)return this._entityMarkers.clear(),this._clusterAvatars.clear(),void e.setClustering(null);this._watchRegistry();const i=getComputedStyle(this),a={};this._zonePositions={},this._zoneRadii={};for(const e of this.entities){const i=t[A(e)];!i||"zone"!==(0,b.t)(i)||!this.renderPassive&&i.attributes.passive||(a["zone.home"===i.entity_id?"home":(0,m.u)(i)]=i.entity_id,"number"==typeof i.attributes.latitude&&"number"==typeof i.attributes.longitude&&(this._zonePositions[i.entity_id]=[i.attributes.latitude,i.attributes.longitude],"number"==typeof i.attributes.radius&&(this._zoneRadii[i.entity_id]=i.attributes.radius)))}const o=new Set;for(const r of this.entities){const n=t[A(r)];if(!n)continue;const s="string"!=typeof r?r.name:void 0,l=s??(0,m.u)(n),{passive:c,icon:d,radius:h,entity_picture:u}=n.attributes,f=(0,g.H)(n,t);if(!f)continue;const{latitude:_,longitude:v,gpsAccuracy:k}=f,M=[_,v];if("zone"===(0,b.t)(n)){if(c&&!this.renderPassive)continue;const t="string"!=typeof r&&r.hide_radius,a=!c&&"string"!=typeof r&&r.color?r.color:(0,w.YG)(n.entity_id,!!c,this._entityReg,i);!t&&h&&this._zoneHandles.push(e.addCircle(M,{radius:h,color:a}));const o=(0,x.x5)({color:a,icon:d,name:l});if(this.interactiveZones){const t=t=>{t.stopPropagation(),(0,p.r)(this,"hass-more-info",{entityId:n.entity_id})};o.addEventListener("click",t),o.addEventListener("keydown",e=>{"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),t(e))})}this._zoneHandles.push(e.addMarker(o,M,{size:[36,36],interactive:this.interactiveZones,title:l})),!this.fitZones||"string"!=typeof r&&!1===r.focus||(!t&&h?this._focusZonePoints.push(...(0,y.Rn)(M,h)):this._focusZonePoints.push(M));continue}const z="string"!=typeof r&&"state"===r.label_mode?this._formatters.formatEntityState(n):"string"!=typeof r&&"attribute"===r.label_mode&&void 0!==r.attribute?this._formatters.formatEntityAttributeValue(n,r.attribute):s??l.split(" ").map(t=>t[0]).join("").substr(0,3),C=A(r),E=K(this._entityMarkers,C,!o.has(C));o.add(C),E.showIcon="string"!=typeof r&&"icon"===r.label_mode,E.entityId=C,E.entityName=z,E.entityUnit="string"!=typeof r&&r.unit&&"attribute"===r.label_mode?r.unit:"",E.entityPicture=!u||"string"!=typeof r&&r.label_mode?"":this._connection.hassUrl(u);const P=("string"!=typeof r?r.color:void 0)||(0,w.lb)(C,this._entityReg,i);E.entityColor=P,E.selected="string"!=typeof r&&(r.selected??!1);const L={entityId:C,title:l,picture:E.entityPicture||void 0,label:z,showIcon:E.showIcon,unit:E.entityUnit??"",color:P,selected:E.selected,zoneId:["person","device_tracker"].includes((0,b.t)(n))?a[n.state]??this._zoneContaining(M):void 0},S=!(!k||"string"!=typeof r&&r.hide_accuracy),F=this._getMarkerSize(i);this._entityHandles.push(e.addMarker(E,M,{size:[F,F],title:l,cluster:!0,clusterData:L,decoration:S?{radius:k,color:P}:void 0})),"string"!=typeof r&&!1===r.focus||this._focusPoints.push(M)}const r=new Set(this.entities.map(A));for(const t of[this._entityMarkers,this._clusterAvatars])for(const e of t.keys())r.has(e)||t.delete(e);e.setClustering(this.clusterMarkers?{radius:V,iconBuilder:this._createClusterBubble,groupKey:t=>t.clusterData?.zoneId,groupRadius:q}:null)}_zoneContaining(t){let e,i=1/0;for(const[a,o]of Object.entries(this._zoneRadii))o<i&&(0,y.S_)(t,this._zonePositions[a])<=o&&(e=a,i=o);return e}_drawScaleRuler(){this._engine?.setScaleRuler(this.scaleRuler?{metric:"km"===this._config?.unit_system?.length}:null)}_getMarkerSize(t){const e=t.getPropertyValue("--ha-marker-size"),i=parseFloat(e);return Number.isNaN(i)?48:i}async _attachObserver(){this._resizeObserver||(this._resizeObserver=new ResizeObserver(()=>{this._engine?.invalidateSize(),this._runPendingFit()})),this._resizeObserver.observe(this)}constructor(...t){super(...t),this.clickable=!1,this.autoFit=!1,this.renderPassive=!1,this.interactiveZones=!1,this.fitZones=!1,this.zoomPosition="topleft",this._zonePositions={},this._zoneRadii={},this.themeMode="auto",this.zoom=14,this.clusterMarkers=!0,this.scaleRuler=!1,this._loaded=!1,this._editableHandles=new Map,this._entityReg=[],this._entityHandles=[],this._entityMarkers=new Map,this._clusterAvatars=new Map,this._zoneHandles=[],this._pathHandles=[],this._focusPoints=[],this._focusZonePoints=[],this._clickCount=0,this._isProgrammaticFit=!1,this._pauseAutoFit=!1,this._handleVisibilityChange=async()=>{document.hidden||setTimeout(()=>{this._pauseAutoFit=!1},500)},this._resolveMapStyle=(0,l.A)(_.kR),this._loading=!1,this._forceLeaflet=!1,this._setupAttempt=0,this._hasFitted=!1,this._createClusterBubble=(t,e,i,a=!1)=>{const o=t.map(t=>t.clusterData),r=a?o:o.slice(0,j),n=o.length-r.length,s=!!this.paths?.length,l=document.createElement("div");l.className="cluster-bubble";const c=new Set;for(const t of r){const e=K(this._clusterAvatars,t?.entityId,!c.has(t?.entityId??""));t?.entityId&&c.add(t.entityId),e.entityId=t?.entityId,e.entityName=t?.label??"",e.entityUnit=t?.unit??"",e.showIcon=t?.showIcon??!1,e.entityPicture=t?.picture??"",e.entityColor=t?.color,s?(e.style.setProperty("--ha-marker-color",t?.color??"var(--primary-color)"),e.style.setProperty("--ha-marker-border-width","2px")):(e.style.removeProperty("--ha-marker-color"),e.style.removeProperty("--ha-marker-border-width")),e.selected=t?.selected??!1,(0,M.I)(e),a&&(0,M.l)(e,t?.title,!0),l.appendChild(e)}const d=a?Math.max(1,Math.floor((this.offsetWidth-2*T-2*H+B)/($+B))):r.length,h=Math.min(r.length,d),u=Math.ceil(r.length/d);let p=h*$+(h-1)*B+2*H;if(n>0){const t=document.createElement("span");t.className="more",t.textContent=n>N?`${N}+`:`+${n}`,l.appendChild(t),p+=O+B}const b=i?this._zonePositions[i]:void 0,m=!!b;let g=u*$+(u-1)*B+2*H,f=l;if(m){f=document.createElement("div"),f.className="cluster-marker";const t=document.createElement("div");t.className="cluster-bubble-tail",f.append(l,t),g+=D}return{element:f,size:[p,g],...m&&b?{location:b,anchor:[p/2,g+18+U]}:{}}}}}X.styles=n.AH`
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
    ${(0,n.iz)(k.xr)}
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
      width: ${W}px;
      height: ${W}px;
      margin-top: ${-W/2}px;
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
      gap: ${B}px;
      padding: ${H}px;
      box-sizing: border-box;
      background: var(--card-background-color, #fff);
      border-radius: 14px;
      filter: var(--ha-cluster-shadow);
      --ha-marker-size: ${$}px;
      --ha-marker-color: transparent;
      --ha-marker-border-width: 1px;
      --ha-marker-shadow: none;
      --ha-marker-font-size: var(--ha-font-size-s);
      /* distinguish letter tiles from the bubble background */
      --ha-marker-background: var(--ha-color-fill-neutral-quiet-resting);
    }
    .cluster-bubble .more {
      flex: none;
      width: ${O}px;
      height: ${$}px;
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
    ${(0,n.iz)(x.Nr)}
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
  `,(0,o.Cg)([(0,s.wk)(),(0,c.F)({context:E.iN,subscribe:!0})],X.prototype,"_states",void 0),(0,o.Cg)([(0,s.wk)(),(0,c.F)({context:E.WF,subscribe:!0}),(0,u.p)({transformer:({config:t})=>t})],X.prototype,"_config",void 0),(0,o.Cg)([(0,s.wk)(),(0,c.F)({context:E.EK,subscribe:!0})],X.prototype,"_ui",void 0),(0,o.Cg)([(0,s.wk)(),(0,c.F)({context:E.D5,subscribe:!0})],X.prototype,"_i18n",void 0),(0,o.Cg)([(0,s.wk)(),(0,c.F)({context:E.p0,subscribe:!0})],X.prototype,"_formatters",void 0),(0,o.Cg)([(0,s.wk)(),(0,c.F)({context:E.Wq,subscribe:!0})],X.prototype,"_connection",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],X.prototype,"entities",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],X.prototype,"paths",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],X.prototype,"editableLocations",void 0),(0,o.Cg)([(0,s.MZ)({type:Boolean})],X.prototype,"clickable",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"auto-fit",type:Boolean})],X.prototype,"autoFit",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"render-passive",type:Boolean})],X.prototype,"renderPassive",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"interactive-zones",type:Boolean})],X.prototype,"interactiveZones",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"fit-zones",type:Boolean})],X.prototype,"fitZones",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],X.prototype,"fitPadding",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"zoom-position"})],X.prototype,"zoomPosition",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"theme-mode",type:String})],X.prototype,"themeMode",void 0),(0,o.Cg)([(0,s.MZ)({attribute:!1})],X.prototype,"mapStyle",void 0),(0,o.Cg)([(0,s.MZ)({type:Number})],X.prototype,"zoom",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"cluster-markers",type:Boolean})],X.prototype,"clusterMarkers",void 0),(0,o.Cg)([(0,s.MZ)({attribute:"scale-ruler",type:Boolean})],X.prototype,"scaleRuler",void 0),(0,o.Cg)([(0,s.wk)()],X.prototype,"_loaded",void 0),(0,o.Cg)([(0,s.P)("#map")],X.prototype,"_mapElement",void 0),(0,o.Cg)([(0,s.wk)()],X.prototype,"_entityReg",void 0),X=(0,o.Cg)([(0,s.EM)("ha-map")],X),i.d(e,{},{$:R}),a()}catch(t){a(t)}})},5792(t,e,i){i(24791),i(77809),i(92653);var a=i(42006),o=i(81541);const r="X-Map-Tiles-Token",n=[0,400,1e3],s=[2e3,5e3,1e4,15e3];let l,c,d,h,u,p,b,m;const g=new Set,f=async t=>{const e=await t.sendMessagePromise({type:"map_tiles/access_token"});e.token!==l&&(l=e.token,g.forEach(t=>t(l)))},y=async(t,e)=>{for(const i of e){if(l)return;i&&await(0,o.l)(i);try{return void await f(t)}catch{}}},_=()=>{if(!b)return;const t=b;f(t).then(()=>v(t)).catch(()=>{})},v=t=>{l&&!u&&(u=setInterval(()=>{f(b??t).catch(()=>{})},12e5)),p!==t&&(p?.removeEventListener("ready",_),p=t,t.addEventListener("ready",_))},k=()=>(c??location.origin).replace(/\/+$/,"");i.d(e,{ZV:()=>a.Z},{Oc:()=>b?(m??=f(b).catch(()=>{}).finally(()=>{m=void 0}),m):Promise.resolve(),Xx:t=>(g.add(t),()=>g.delete(t)),bK:t=>t.startsWith("/")?`${k()}${t}`:t,pW:async t=>{if(b=t,c=t.options.auth?.data.hassUrl,l||(d??=y(t,n).finally(()=>{d=void 0}),await d),l)return v(t),l;h??=y(t,s).then(()=>v(t)).finally(()=>{h=void 0})},rG:t=>{let e;try{e=new URL(t,k())}catch{return{url:t}}if(!e.pathname.startsWith(`${a.Z}/`))return{url:e.href};const i=new URL(`${k()}${e.pathname}${e.search}`);return l?i.origin===location.origin?{url:i.href,headers:{[r]:l}}:(i.searchParams.set("token",l),{url:i.href}):{url:i.href}}})}};
//# sourceMappingURL=49854.3cc4695ab1d1f79f.js.map