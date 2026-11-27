export const __rspack_esm_ids=[29524];export const __webpack_modules__={98615(t,e,a){var i=a(42567);const r=(t,e)=>{for(const a of t){const t=e[a];if(t&&!t.attributes.passive&&"number"==typeof t.attributes.latitude&&"number"==typeof t.attributes.longitude)return t}};a.d(e,{},{H:(t,e)=>{const{latitude:a,longitude:o,gps_accuracy:n}=t.attributes;if("number"==typeof a&&"number"==typeof o)return{latitude:a,longitude:o,gpsAccuracy:n};if("person"!==(0,i.t)(t))return;const s=t.attributes.in_zones;if(!Array.isArray(s)||0===s.length)return;const l=r(s,e);return l?{latitude:l.attributes.latitude,longitude:l.attributes.longitude}:void 0},_:r})},41201(t,e,a){a(65649),a(62922),a(14167),a(59350),a(70425),a(63145);var i=a(58509),r=a(38194);const o={light:"/static/map/light.json",dark:"/static/map/dark.json"},n=`${r.ZV}/raster/{z}/{x}/{y}.png?token={token}`;let s;const l=()=>(()=>{if(void 0===s)try{const t=document.createElement("canvas").getContext("webgl2");s=Boolean(t),t?.getExtension("WEBGL_lose_context")?.loseContext()}catch{s=!1}return s})(),c=()=>new URL(/static/,location.href),d=t=>new URL(t,c()).href,h=new Map,p=async t=>{const e=t.shipped&&o[t.shipped],i=e?JSON.parse(await(t=>{let e=h.get(t);return e||(e=fetch(t).then(t=>t.text()).finally(()=>h.delete(t)),h.set(t,e)),e})(e)):await(await a.e(18990).then(a.bind(a,48189))).buildMapStyle(t.palette,t.options??{},t.styleOptions);return"string"==typeof i.sprite?i.sprite=d(i.sprite):Array.isArray(i.sprite)&&(i.sprite=i.sprite.map(t=>({...t,url:d(t.url)}))),i};let u=!1;const m=t=>{u||(u=!0,t(new URL("/frontend_latest/maplibre-gl-worker.20261125.1.js",c()).href))},b=(t,e,a)=>{const i=t.tileLayer((0,r.bK)(n),{attribution:'<a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',maxZoom:20,maxNativeZoom:19,referrerPolicy:void 0,token:a??""}).addTo(e);let o=!1,s=0;i.on("tileerror",()=>{o=!0,Date.now()-s<3e4||(s=Date.now(),(0,r.Oc)())});const l=(0,r.Xx)(t=>{i.options.token=t,o&&(o=!1,i.redraw())});return e.on("unload",l),{setMapStyle:()=>{}}};a.d(e,{},{MK:p,V4:async(t,e,o,n,s=!1)=>{if(!s&&l()){let s;try{const[{maplibreGL:l},c]=await Promise.all([Promise.all([a.e(52706),a.e(7128),a.e(66722)]).then(a.bind(a,10841)),a.e(52706).then(a.bind(a,68665))]);m(c.setWorkerUrl),s=await(async(t,e,a,o,n)=>{let s;try{s=t({style:await p(o),transformRequest:t=>({...(0,r.rG)(t),referrerPolicy:void 0})}),s.addTo(a)}catch{if(s)try{s.remove()}catch{}return}let l=o,c=o,d=0,h=!0,u=!1,m=n;const f=s.getMaplibreMap();let g,_=!1;const y=()=>{_&&k()},v=()=>{h=!1,document.removeEventListener("visibilitychange",y);try{s.remove()}catch{}b(e,a,m)},k=()=>{clearTimeout(g),h&&!document.hidden&&(g=window.setTimeout(v,2e3))};f.on("webglcontextlost",()=>{_=!0,k()}),f.on("webglcontextrestored",()=>{_=!1,clearTimeout(g)}),document.addEventListener("visibilitychange",y),a.on("unload",()=>{clearTimeout(g),document.removeEventListener("visibilitychange",y)});const w=t=>{const e=++d;p(t).then(a=>{e===d&&(l=t,s.getMaplibreMap()?.setStyle(a))}).catch(()=>{e===d&&(c=l)})};let M=0;f.on("error",t=>{const e=t.error?.status;void 0!==e&&403!==e&&404!==e||Date.now()-M<3e4||(M=Date.now(),u=!0,(0,r.Oc)())});const x=(0,r.Xx)(t=>{m=t,h&&u&&(u=!1,w(c))});return a.on("unload",x),{setMapStyle:t=>{h&&!(0,i.b)(t,c)&&(c=t,w(t))}}})(l,t,e,o,n)}catch{}if(s)return s}return b(t,e,n)},W$:m,jV:l})},70825(t,e,a){a.d(e,{},{rx:t=>{const e=document.createElement("div");e.className="editable-circle-resize",e.tabIndex=0,e.setAttribute("role","slider"),e.setAttribute("aria-valuemin","1"),e.setAttribute("aria-valuemax",String(1e5)),t&&e.setAttribute("aria-label",t);const a=document.createElement("div");return a.className="editable-circle-resize-dot",e.appendChild(a),e},xr:"\n  .editable-circle-center {\n    width: 16px;\n    height: 16px;\n    border-radius: 50%;\n    background: var(--primary-color);\n    border: 2px solid var(--card-background-color, #fff);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n  .editable-circle-resize {\n    width: 24px;\n    height: 24px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    cursor: ew-resize;\n  }\n  .editable-circle-resize-dot {\n    width: 12px;\n    height: 12px;\n    border-radius: 50%;\n    background: var(--card-background-color, #fff);\n    border: 2px solid var(--primary-color);\n    box-sizing: border-box;\n    box-shadow: var(--ha-box-shadow-s);\n  }\n"})},59351(t,e,a){const i=6371008.8,r=t=>t*Math.PI/180,o=t=>180*t/Math.PI,n=(t,e,a)=>{const n=e/i,s=r(t[0]),l=r(a),c=Math.asin(Math.sin(s)*Math.cos(n)+Math.cos(s)*Math.sin(n)*Math.cos(l)),d=Math.atan2(Math.sin(l)*Math.sin(n)*Math.cos(s),Math.cos(n)-Math.sin(s)*Math.sin(c));return[o(c),t[1]+o(d)]},s=85.051129,l=([t,e],a)=>{const i=Math.sin(r(Math.max(-85.051129,Math.min(s,t))));return{x:(e/360+.5)*a,y:(.5-Math.log((1+i)/(1-i))/(4*Math.PI))*a}};a.d(e,{},{RO:(t,e)=>n(t,e,90),Rn:(t,e)=>{const a=e/i,n=Math.max(-90,t[0]-o(a)),s=Math.min(90,t[0]+o(a)),l=Math.sin(a)/Math.cos(r(t[0]));if(n<=-90||s>=90||Math.abs(l)>=1)return[[n,-180],[s,180]];const c=o(Math.asin(l));return[[n,t[1]-c],[s,t[1]+c]]},S_:(t,e)=>{const a=r(e[0]-t[0]),i=r(e[1]-t[1]),o=Math.sin(a/2)**2+Math.cos(r(t[0]))*Math.cos(r(e[0]))*Math.sin(i/2)**2;return 12742017.6*Math.asin(Math.sqrt(o))},bM:n,kb:(t,e,a)=>{const i=256*2**a,r=l(t,i),o=l(e,i),n=Math.abs(r.x-o.x);return Math.hypot(Math.min(n,i-n),r.y-o.y)}})},77e3(t,e,a){a.d(e,{jJ:()=>r,u8:()=>i,l6:()=>s,cE:()=>c,kR:()=>m,vA:()=>u});a(19945),a(65649),a(14167);const i=["default","colorful","natural","muted","gray","toner","neon"],r="default",o={default:{palette:"colorful",colors:{background:"#f5efe5",land:"#f5efe5",water:"#b8daec",labelWater:"#5487aa",natureWood:"#cfe4bc",natureGrass:"#e2eed8",naturePark:"#cfe4bc",natureLeisure:"#e2eed8",natureAgriculture:"#e8efe1",natureWetland:"#e5ecdf",natureSand:"#f3eadd",natureRock:"#f3eadd",glacier:"#faf6f0",areaResidential:"#f1e9da",areaCommercial:"#f7e0d8",areaIndustrial:"#f0e7cb",areaWaste:"#eee3d3",areaBurial:"#f1e9da",siteParking:"#efe7d6",siteSports:"#cfe4bc26",building:"#eadec7",buildingBg:"#e0cdae",roadStreet:"#fcfaf8",roadStreetBg:"#e9dbc4",roadTrunk:"#ffe7be",roadTrunkBg:"#ebd09f",roadMotorway:"#f1d6a5",roadMotorwayBg:"#e8bd6e",transitRail:"#ece0cb",transitSubway:"#ece2cf",transitCycle:"#f3eee2",transitFoot:"#f3eee2",boundary:"#dbc49f",boundaryDisputed:"#e5d7bd",label:"#4b473c",labelHalo:"#faf8f5cc",labelSymbol:"#8f8774",labelPoi:"#8f877466",labelShield:"#fbf8f3",labelHousenumber:"#8f87744d"},colorsDark:{background:"#191b2c",land:"#191b2c",water:"#27357a",labelWater:"#9cc0f0",natureWood:"#254948",natureGrass:"#213b39",naturePark:"#28504b",natureLeisure:"#213532",natureAgriculture:"#203233",natureWetland:"#253337",natureSand:"#2a2c3d",natureRock:"#2a2c3d",glacier:"#2a2c3d",areaResidential:"#1d2034",areaCommercial:"#29213a",areaIndustrial:"#242431",areaWaste:"#1d2034",areaBurial:"#1d2034",siteParking:"#1d2034",siteSports:"#25413926",building:"#21243c",buildingBg:"#2a2e4a",roadStreet:"#2b3052",roadStreetBg:"#1a1d33",roadTrunk:"#383e67",roadTrunkBg:"#22263f",roadMotorway:"#454d7d",roadMotorwayBg:"#2a2f4c",transitRail:"#2c3150",transitSubway:"#2c3150",transitCycle:"#2b3052",transitFoot:"#2b3052",boundary:"#3b4068",boundaryDisputed:"#3b4068",label:"#e7ecf8",labelHalo:"#12141fcc",labelSymbol:"#959dbd",labelPoi:"#959dbd66",labelShield:"#191b2c",labelHousenumber:"#959dbd4d"}},neon:{palette:"colorful",colorsDark:{background:"#07021a",land:"#07021a",water:"#13215e",labelWater:"#00e5ff",glacier:"#1b2a6b",natureWood:"#0d1f2e",natureGrass:"#101a33",naturePark:"#12203a",natureLeisure:"#111a30",natureAgriculture:"#0d1528",natureWetland:"#0e2440",natureSand:"#1a1230",natureRock:"#140c28",areaResidential:"#0c0524",areaCommercial:"#140430",areaIndustrial:"#10062a",areaWaste:"#160a2e",areaBurial:"#0d0a26",siteParking:"#0f0728",siteSports:"#0a1c2c",siteEducation:"#160a34",siteHospital:"#2a0a2a",siteDanger:"#ff1744",sitePrison:"#1c0a28",siteConstruction:"#3a1d5c",building:"#160a33",buildingBg:"#8a2be2",roadStreet:"#00e5ff",roadStreetBg:"#062b52",roadSecondary:"#8f7bff",roadSecondaryBg:"#241058",roadTrunk:"#ff6ec7",roadTrunkBg:"#4a0f38",roadMotorway:"#ff2d95",roadMotorwayBg:"#5c0033",transitRail:"#7b2cff",transitSubway:"#b14cff",transitCycle:"#00ffa3",transitFoot:"#2e2a55",boundary:"#39ff14",boundaryDisputed:"#1f7a0d",label:"#ff9ad5",labelHalo:"rgba(7,2,26,0.9)",labelSymbol:"#ff9ad5",labelPoi:"#00e5ff",labelShield:"#12002a",labelHousenumber:"rgba(0,229,255,0.35)"},options:{recolor:{saturate:.35,contrast:1.15},text:{transform:"uppercase",letterSpacing:.12,haloWidth:2,haloBlur:0}}},colorful:{palette:"colorful"},natural:{palette:"natural"},muted:{palette:"muted"},gray:{palette:"gray"},toner:{palette:"toner"}},n=t=>i.includes(t),s=t=>"object"==typeof t&&null!==t,l=t=>{const e=s(t)?t.base:t;return n(e)?e:r},c=(t,e)=>{const{colors:a,colorsDark:i}=o[l(t)];return Boolean(a)!==Boolean(i)?Boolean(i):e},d=["colors","recolor","text","icon","layers"],h=t=>t.replace(/_([a-z])/g,(t,e)=>e.toUpperCase()),p=t=>Array.isArray(t)?t.map(p):t&&"object"==typeof t?Object.fromEntries(Object.entries(t).map(([t,e])=>[h(t),p(e)])):t,u=(t,e)=>{const a=n(e)&&e!==r?e:void 0,i=s(t)?{...t}:{};return delete i.base,Object.keys(i).length?{...a&&{base:a},...i}:a},m=(t,e,a)=>{const i=s(t)?t:void 0,n=l(t),u=c(t,e),m=((t,e)=>{const{palette:a}=o[t];return e?`${a}-dark`:a})(n,u),b=i?((t,e)=>{const a=t,i={};for(const t of d){const e=a[t]??a[h(t)];void 0!==e&&(i[h(t)]=p(e))}const r=a.colors_dark;return e&&void 0!==r&&(i.colors=p(r)),i})(i,u):{},f=Object.keys(b).length>0,{colors:g,colorsDark:_,options:y}=o[n];for(const[t,e]of Object.entries(y??{}))b[t]={...e,...b[t]};const v=u?_:g;if((v||a)&&(b.colors={...v,...a,...b.colors}),!Object.keys(b).length)return{palette:m};const k=v||y?{styleOptions:{...y,...v&&{colors:v}}}:{};return n===r&&(!a&&!f)?{palette:m,options:b,...k,shipped:u?"dark":"light"}:{palette:m,options:b,...k}}},62377(t,e,a){a(65649),a(16286),a(47399),a(14167),a(70705);const i={"--ha-color-map-land":["background","land"],"--ha-color-map-water":["water"],"--ha-color-map-green":["naturePark","natureWood","natureGrass","natureLeisure","natureWetland","siteSports"],"--ha-color-map-area":["areaResidential","areaCommercial","areaIndustrial","areaWaste","areaBurial","siteParking","natureAgriculture","natureSand","natureRock"],"--ha-color-map-building":["building"],"--ha-color-map-building-outline":["buildingBg"],"--ha-color-map-road":["roadStreet"],"--ha-color-map-road-major":["roadMotorway","roadTrunk"],"--ha-color-map-road-outline":["roadStreetBg","roadTrunkBg","roadMotorwayBg"],"--ha-color-map-transit":["transitRail","transitSubway","transitCycle","transitFoot"],"--ha-color-map-boundary":["boundary","boundaryDisputed"],"--ha-color-map-label":["label"],"--ha-color-map-label-halo":["labelHalo"],"--ha-color-map-label-secondary":["labelSymbol","labelPoi","labelHousenumber"]},r={siteSports:.15,labelHalo:.8,labelPoi:.4,labelHousenumber:.3},o=/^#([0-9a-f]{3,8})$/i,n=/^rgba?\(([^)]+)\)$/i,s=/^color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\s*\)$/i,l=t=>{const e=t.match(o);if(e){const t=e[1],a=3===t.length||4===t.length,i=e=>a?parseInt(t[e]+t[e],16):parseInt(t.slice(2*e,2*e+2),16);if(3===t.length||4===t.length||6===t.length||8===t.length){const e=4===t.length||8===t.length?i(3)/255:1;return[i(0),i(1),i(2),e]}return}const a=t.match(n);if(a){const t=a[1].split(/[,\s/]+/).filter(Boolean).map(Number);if(t.length<3||t.slice(0,3).some(Number.isNaN))return;return[t[0],t[1],t[2],t[3]??1]}const i=t.match(s);if(i){const t=t=>Math.round(255*Number(t));return[t(i[1]),t(i[2]),t(i[3]),Number(i[4]??1)]}},c=[1,2,3,1],d=(t,e)=>{const a=document.createElement("span");a.style.cssText="display:none;color:rgb(1, 2, 3)";const i=document.createElement("span");i.style.color=`var(${e})`,a.append(i),t.append(a);const r=l(getComputedStyle(i).color);return a.remove(),r&&r.every((t,e)=>t===c[e])?void 0:r};a.d(e,{},{Q:t=>{const e=getComputedStyle(t);let a;for(const[o,n]of Object.entries(i)){const i=e.getPropertyValue(o).trim();if(!i)continue;const s=l(i)??d(t,o);if(!s)continue;a??={};const[c,h,p,u]=s;for(const t of n){const e=Math.round(u*(r[t]??1)*1e3)/1e3;a[t]=`rgba(${c},${h},${p},${e})`}}return a}})},98255(t,e,a){a(65649),a(47399),a(62922);const i="haMapA11y",r=t=>{const e=t.dataset[i];void 0!==e&&(e.split(" ").filter(Boolean).forEach(e=>t.removeAttribute(e)),delete t.dataset[i])};a.d(e,{},{I:r,l:(t,e,a)=>{r(t);const o=[];!e||t.hasAttribute("aria-label")||t.hasAttribute("aria-labelledby")||(t.setAttribute("aria-label",e),o.push("aria-label")),t.hasAttribute("role")||(a?(t.setAttribute("role","button"),o.push("role")):e?(t.setAttribute("role","img"),o.push("role")):(t.setAttribute("aria-hidden","true"),o.push("aria-hidden"))),a&&!t.hasAttribute("tabindex")&&(t.tabIndex=0,o.push("tabindex")),t.dataset[i]=o.join(" ")}})},68298(t,e,a){var i=a(19265),r=a.n(i);a.d(e,{},{D:t=>r()(t,{whiteList:{},stripIgnoreTag:!0,stripIgnoreTagBody:!0})})},9945(t,e,a){a.a(t,async function(t,i){try{var r=a(83316),o=a(63560),n=a(98933),s=a(801),l=a(28711),c=a(39077),d=a(51613),h=t([d]);d=(h.then?(await h)():h)[0];const p=1.25,u=12,m=Math.round(u*Math.SQRT2/2),b=4,f=10,g=(t,e)=>{const a=e?Math.round(t*p):t,i=a+m+b+f;return{size:[a,i],anchor:[a/2,i-f/2]}};class _ extends o.WF{render(){return o.qy` <div part="marker" class="marker ${this.entityPicture?"picture":""}" style=${(0,s.W)({"--ha-marker-selected-color":this.entityColor})};> ${this.entityPicture?o.qy`<div part="picture" class="entity-picture" style=${(0,s.W)({"background-image":`url(${this.entityPicture})`})};></div>`:this.showIcon&&this.entityId?o.qy`<ha-state-icon .stateObj=${this._stateObj}></ha-state-icon>`:this.entityUnit?o.qy` ${this.entityName} <span class="unit" style="display:${this.entityUnit?"initial":"none"}">${this.entityUnit}</span> `:this.entityName} </div> ${this.floating?o.qy`<div class="tail"></div> <div class="dot"></div>`:o.s6} `}connectedCallback(){super.connectedCallback(),this.addEventListener("click",this._badgeTap),this.addEventListener("keydown",this._handleKeydown)}disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("click",this._badgeTap),this.removeEventListener("keydown",this._handleKeydown)}constructor(...t){super(...t),this.showIcon=!1,this.selected=!1,this.floating=!1,this._handleKeydown=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),this._badgeTap(t))},this._badgeTap=t=>{t.stopPropagation(),this.entityId&&(0,c.r)(this,"hass-more-info",{entityId:this.entityId})}}}_.styles=o.AH`:host([floating]){filter:var(--ha-cluster-shadow,drop-shadow(0 1px 3px #0000001f));pointer-events:none;flex-direction:column;align-items:center;display:flex}:host([floating]) .marker,:host([floating]) .tail{pointer-events:auto}:host([floating]) .marker{z-index:1;position:relative}.marker{text-align:center;box-sizing:border-box;width:var(--ha-marker-size,48px);height:var(--ha-marker-size,48px);font-size:var(--ha-marker-font-size,var(--ha-font-size-xl));border-radius:var(--ha-picture-border-radius);border:var(--ha-marker-border-width,3px) solid var(--ha-marker-color,var(--card-background-color,#fff));color:var(--primary-text-color);background-color:var(--ha-marker-background,var(--card-background-color));justify-content:center;align-items:center;display:flex}.marker.picture{overflow:hidden}:host([selected]) .marker{width:calc(var(--ha-marker-size,48px) * var(--ha-marker-selected-scale,${p}));height:calc(var(--ha-marker-size,48px) * var(--ha-marker-selected-scale,${p}))}:host([selected]:not([floating])) .marker{outline:3px solid var(--ha-marker-selected-color,var(--primary-color))}.tail{width:${u}px;height:${u}px;margin-top:${-u/2}px;margin-bottom:${m-u/2}px;background:var(--ha-marker-color,var(--card-background-color,#fff));border-radius:2px;transform:rotate(45deg)}.dot{width:${f}px;height:${f}px;margin-top:${b}px;background:var(--ha-marker-color,var(--card-background-color,#fff));border-radius:50%}:host(:not([selected])) .dot{visibility:hidden}.entity-picture{background-size:cover;width:100%;height:100%}.unit{margin-left:2px}`,(0,r._)([(0,n.MZ)({attribute:"entity-id",reflect:!0})],_.prototype,"entityId",void 0),(0,r._)([(0,n.wk)(),(0,l.fI)({entityIdPath:["entityId"]})],_.prototype,"_stateObj",void 0),(0,r._)([(0,n.MZ)({attribute:"entity-name"})],_.prototype,"entityName",void 0),(0,r._)([(0,n.MZ)({attribute:"entity-unit"})],_.prototype,"entityUnit",void 0),(0,r._)([(0,n.MZ)({attribute:"entity-picture"})],_.prototype,"entityPicture",void 0),(0,r._)([(0,n.MZ)({attribute:"entity-color"})],_.prototype,"entityColor",void 0),(0,r._)([(0,n.MZ)({attribute:"show-icon",type:Boolean})],_.prototype,"showIcon",void 0),(0,r._)([(0,n.MZ)({type:Boolean,reflect:!0})],_.prototype,"selected",void 0),(0,r._)([(0,n.MZ)({type:Boolean,reflect:!0})],_.prototype,"floating",void 0),_=(0,r._)([(0,n.EM)("ha-entity-marker")],_),a.d(e,{},{i:g}),i()}catch(t){i(t)}})},42847(t,e,a){a.a(t,async function(t,i){try{a(19945),a(65649),a(47399),a(62922),a(14167),a(70705),a(70425),a(63145),a(9336),a(29170),a(15740);var r=a(83316),o=a(29410),n=a(63560),s=a(98933),l=a(25591),c=a(55904),d=a(17401),h=a(67248),p=(a(8044),a(55658)),u=a(39077),m=a(42567),b=a(98615),f=a(41201),g=a(59351),_=a(77e3),y=a(62377),v=a(70825),k=a(31305),w=a(98255),M=a(18741),x=a(58509),z=a(68298),E=a(43834),P=a(11757),C=a(38194),S=a(39697),L=a(9945),A=t([S,d,h,L]);[S,d,h,L]=A.then?(await A)():A;const F=250,H=3e3,$=t=>"string"==typeof t?t:t.entity_id,T=["name","state","attribute","icon"],B=(t,e)=>t.element===e.element&&t.title===e.title&&t.color===e.color&&t.locationEditable===e.locationEditable&&t.radiusEditable===e.radiusEditable&&t.activatable===e.activatable&&t.elementSize?.[0]===e.elementSize?.[0]&&t.elementSize?.[1]===e.elementSize?.[1],R=t=>({addDraggableMarker:(e,a,i)=>{let r=a,o=t.addMarker(e,r,i);return{get location(){return r},clusterData:i.clusterData,setLocation:a=>{o.remove(),r=a,o=t.addMarker(e,r,i)},remove:()=>o.remove()}},addEditableCircle:(e,a)=>{const i=a.centerElement??document.createElement("div");let r;if(a.centerElement||(i.className="editable-circle-center"),a.onClick){const t=t=>{t.stopPropagation(),a.onClick()},e=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),a.onClick())};i.addEventListener("click",t),i.addEventListener("keydown",e),r=()=>{i.removeEventListener("click",t),i.removeEventListener("keydown",e)}}let o={center:e,radius:a.radius},n=[];const s=()=>{n=[t.addCircle(o.center,{radius:o.radius,color:a.color}),t.addMarker(i,o.center,{size:a.centerSize??[16,16],interactive:!!a.onClick,title:a.title,nativeTitle:a.nativeTitle})]};return s(),{get center(){return o.center},get radius(){return o.radius},update:(t,e)=>{n.forEach(t=>t.remove()),o={center:t,radius:e},s()},remove:()=>{r?.(),n.forEach(t=>t.remove())}}}}),Z=32,I=6,D=4,O=12,N=4,W=28,j=99,U=10,V=Math.round(U*Math.SQRT2/2),q=2,G=40,K=160,X=2.5,Q=10,J=t=>{const e=t.replace(".","-");return`marker, picture, marker: marker-${e}, picture: picture-${e}`},Y=(t,e,a=!0)=>{const i=e&&a?t.get(e):void 0;if(i&&!i.isConnected)return i;const r=document.createElement("ha-entity-marker");return e&&(r.setAttribute("exportparts",J(e)),t.set(e,r)),r};class tt extends n.mN{connectedCallback(){this._pauseAutoFit=!1,document.addEventListener("visibilitychange",this._handleVisibilityChange),this._handleVisibilityChange(),super.connectedCallback(),this._loadMap(),this._attachObserver()}_watchRegistry(){!this._registryConsumer&&this.entities?.length&&(this._registryConsumer=new c.TH(this,E.ih,t=>{this._entityReg=t}))}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("visibilitychange",this._handleVisibilityChange),this._engine?.destroy(),this._engine=void 0,this._setupAttempt++,this._startingEngine?.destroy(),this._startingEngine=void 0,this._loading=!1,clearTimeout(this._drawnFallback),this._entityHandles=[],this._entityMarkers.clear(),this._clusterAvatars.clear(),this._zoneHandles=[],this._zoneCircleHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}update(t){if(super.update(t),!this._loaded)return;let e=!1;const a=t.get("_states");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),e=!this._pauseAutoFit;else if(this._loaded&&a&&this.entities)for(const t of this.entities){const i=$(t),r=this._states[i],o=r?.attributes.in_zones;if(a[i]!==r||r&&["person","device_tracker"].includes((0,m.t)(r))&&Array.isArray(o)&&o.some(t=>a[t]!==this._states[t])){this._drawEntities(),e=!this._pauseAutoFit;break}}(t.has("clusterMarkers")||t.has("_entityReg")||t.has("_formatters"))&&this._drawEntities(),t.has("fitPadding")&&!(0,x.b)(t.get("fitPadding"),this.fitPadding)&&(e=!this._pauseAutoFit),t.has("zoomPosition")&&this._engine?.setZoomControlPosition(this.zoomPosition);const i=t.get("_config");if((t.has("_loaded")||t.has("scaleRuler")||t.has("_config")&&i?.unit_system?.length!==this._config?.unit_system?.length)&&this._drawScaleRuler(),t.has("_loaded")||t.has("paths")){this._drawPaths();const e=t.get("paths");!!e?.length!=!!this.paths?.length&&this._engine?.refreshClusters()}t.has("_loaded")||t.has("editableLocations")?this._drawEditableLocations()&&(e=!0):t.has("_i18n")&&this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations()),t.has("_loaded")&&this._pendingFit?this._runPendingFit():(t.has("_loaded")||this.autoFit&&e)&&this.fitMap(),t.has("zoom")&&this._withProgrammaticFit(()=>{this._engine.setZoom(this.zoom)});const r=t.get("_ui");t.has("themeMode")||t.has("_ui")&&(!r||r.themes!==this._ui.themes)?(this._updateMapAppearance(),this._drawEntities(),this._drawPaths(),this._editableHandles.size&&(this._removeEditableLocations(),this._drawEditableLocations())):t.has("mapStyle")&&this._updateMapAppearance()}get _darkMode(){return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(this._ui?.themes?.darkMode)}get _styleDark(){return(0,_.cE)(this.mapStyle,this._darkMode)}_readThemeColors(){const t=Boolean(this._ui?.themes?.darkMode),e=this._styleDark===t?(0,y.Q)(this):void 0;(0,x.b)(e,this._themeColors)||(this._themeColors=e)}get _resolvedMapStyle(){return this._resolveMapStyle(this.mapStyle,this._darkMode,this._themeColors)}_updateMapAppearance(){this._readThemeColors();const t=this._mapElement;t&&(t.classList.toggle("clickable",this.clickable),t.classList.toggle("dark",this._styleDark),t.classList.toggle("drawn",this._mapDrawn),t.classList.toggle("space",this._vectorEngine&&this._mapDrawn),t.classList.toggle("forced-dark",this._styleDark&&("dark"===this.themeMode||!this._darkMode)),t.classList.toggle("forced-light",!this._styleDark&&("light"===this.themeMode||this._darkMode)),this._engine?.setMapStyle(this._resolvedMapStyle))}_markDrawn(t){t!==this._setupAttempt||this._mapDrawn||(clearTimeout(this._drawnFallback),this._mapDrawn=!0,this._updateMapAppearance())}get _vectorEngine(){return!this._forceLeaflet&&(0,f.jV)()}async _createEngine(){if(!this._vectorEngine){return new((await Promise.all([a.e(7128),a.e(14922)]).then(a.bind(a,49982))).LeafletMapEngine)}return new((await a.e(67279).then(a.bind(a,55954))).MapLibreMapEngine)}async _loadMap(){const t=this._forceLeaflet||!(0,f.jV)();try{await this._setUpEngine()}catch(e){if(!this.isConnected)return;if(t)throw e;this._forceLeaflet=!0,await this._loadMap()}}async _setUpEngine(){if(this._loading)return;this.shadowRoot.getElementById("map")?.remove();const t=document.createElement("div");t.id="map",t.classList.toggle("dark",this._styleDark),this.shadowRoot.append(t),this._loading=!0,this._mapDrawn=!1,clearTimeout(this._drawnFallback);const e=++this._setupAttempt;let a;try{const i=this._connection?await(0,C.pW)(this._connection.connection):void 0;this._readThemeColors();const r=this._forceLeaflet;if(a=await this._createEngine(),e!==this._setupAttempt)return;if(this._startingEngine=a,this._drawnFallback=window.setTimeout(()=>this._markDrawn(e),H),await a.init(t,{center:[this._config?.latitude??52.3731339,this._config?.longitude??4.8903147],zoom:this.zoom,mapStyle:this._resolvedMapStyle,token:i,rasterOnly:this._forceLeaflet,zoomControlPosition:this.zoomPosition,events:{click:t=>this._handleEngineClick(t),zoomStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},moveStart:()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)},fatal:()=>this._handleEngineFatal(),drawn:()=>this._markDrawn(e)}}),!this.isConnected||e!==this._setupAttempt)return;if(this._forceLeaflet&&!r)throw new Error("Map engine failed during setup");this._engine=a,this._updateMapAppearance(),this._loaded=!0,(0,u.r)(this,"editing-available-changed",{available:!!a.editing})}finally{e===this._setupAttempt&&(this._loading=!1,this._startingEngine=void 0),a&&a!==this._engine&&a.destroy()}}_handleEngineFatal(){this._forceLeaflet||(this._forceLeaflet=!0,this._loading?this._startingEngine?.destroy():(this._engine?.destroy(),this._engine=void 0,this._entityHandles=[],this._zoneHandles=[],this._zoneCircleHandles=[],this._pathHandles=[],this._removeEditableLocations(),this._focusPoints=[],this._focusZonePoints=[],this._pendingFit=void 0,this._hasFitted=!1,this._loaded=!1,this._loadMap()))}_handleEngineClick(t){0===this._clickCount&&setTimeout(()=>{1===this._clickCount&&(0,u.r)(this,"map-clicked",{location:t}),this._clickCount=0},250),this._clickCount++}_withProgrammaticFit(t){this._isProgrammaticFit=!0,t(),setTimeout(()=>{this._isProgrammaticFit=!1},F)}fitMap(t){if(t?.unpause_autofit&&(this._pauseAutoFit=!1),!this._engine||!this._config)return;if(this._deferIfUnsized(()=>this.fitMap(t)))return;const e=this.fitZones||!this._focusPoints.length?this._focusZonePoints:[];if(!this._focusPoints.length&&!e.length&&!this.editableLocations?.length)return this._withProgrammaticFit(()=>{this._engine.setView([this._config.latitude,this._config.longitude],t?.zoom||this.zoom)}),void(this._hasFitted=!0);const a=[...this._focusPoints,...e],i=this.editableLocations??[],r=i.filter(t=>!1!==t.fit);(r.length?r:i).forEach(t=>{t.radius?a.push(...(0,g.Rn)(t.location,t.radius)):a.push(t.location)}),this._withProgrammaticFit(()=>{this._engine.fitBounds(a,{maxZoom:t?.zoom||this.zoom,pad:t?.pad??.5,padding:t?.padding??this.fitPadding,animate:this._hasFitted})}),this._hasFitted=!0}_deferIfUnsized(t){return this._engine.hasUsableSize()?(this._pendingFit=void 0,!1):(this._pendingFit=t,!0)}_runPendingFit(){if(this._pendingFit&&this._engine&&this._engine.hasUsableSize()){const t=this._pendingFit;this._pendingFit=void 0,t()}}panTo(t){this._engine?.panTo(t)}containsLocation(t){return this._engine?.containsLocation(t)??!1}setView(t,e){this._engine?(this._pendingFit=void 0,this._engine.setView(t,e)):this._pendingFit=()=>this.setView(t,e)}getView(){return this._engine?.getView()}fitBounds(t,e){this._pauseAutoFit=!0,this._engine?this._deferIfUnsized(()=>this.fitBounds(t,e))||(this._withProgrammaticFit(()=>{this._engine.fitBounds(t,{maxZoom:e?.zoom||this.zoom,pad:e?.pad??.5,animate:this._hasFitted,padding:e?.padding,fly:e?.fly})}),this._hasFitted=!0):this._pendingFit=()=>this.fitBounds(t,e)}_drawEditableLocations(){const t=this._engine;if(!t)return!1;const e=R(t),a=t.editing??e,i=new Set((this.editableLocations??[]).map(t=>t.id));let r=!1;for(const[t,e]of this._editableHandles)i.has(t)||(e.cleanup?.(),e.handle.remove(),this._editableHandles.delete(t),r=!0);if(!this.editableLocations)return r;const o=getComputedStyle(this).getPropertyValue("--accent-color");for(const t of this.editableLocations){const{id:i}=t,n=t.title??this._i18n?.localize("ui.components.map.location"),s=!!t.element&&!!t.title,l=this._editableHandles.get(i),c=t.radius?"circle":"marker";if(l&&l.kind===c&&B(l.source,t)){"circle"===l.kind?l.handle.update(t.location,t.radius):l.handle.setLocation(t.location),l.source=t;continue}if(l?(l.cleanup?.(),l.handle.remove()):r=!0,"circle"===c){const e=a.addEditableCircle(t.location,{radius:t.radius,color:t.color||o,centerElement:t.element,centerSize:t.elementSize,title:n,nativeTitle:!s,moveable:t.locationEditable,resizable:t.radiusEditable,resizeLabel:t.title?this._i18n?.localize("ui.components.map.radius_of",{name:t.title}):this._i18n?.localize("ui.components.map.radius"),onMove:t=>(0,u.r)(this,"editable-location-moved",{id:i,location:t}),onResize:t=>(0,u.r)(this,"editable-location-resized",{id:i,radius:t}),onClick:t.activatable?()=>(0,u.r)(this,"editable-location-clicked",{id:i}):void 0});this._editableHandles.set(i,{kind:c,source:t,handle:e,cleanup:s?this._attachTooltip(t.element,t.title):void 0});continue}const d=t.element??document.createElement("div");t.element||(d.className="editable-circle-center");let h,p=!1;if(t.activatable){const t=()=>{p=!1},e=t=>{t.stopPropagation(),p||(0,u.r)(this,"editable-location-clicked",{id:i})},a=t=>{"Enter"!==t.key&&" "!==t.key||(t.preventDefault(),(0,u.r)(this,"editable-location-clicked",{id:i}))};d.addEventListener("pointerdown",t),d.addEventListener("click",e),d.addEventListener("keydown",a),h=()=>{d.removeEventListener("pointerdown",t),d.removeEventListener("click",e),d.removeEventListener("keydown",a)}}const m=(t.locationEditable?a:e).addDraggableMarker(d,t.location,{size:t.elementSize??[16,16],interactive:!0,focusable:!!t.activatable,title:n,nativeTitle:!s,onDragEnd:t=>{p=!0,(0,u.r)(this,"editable-location-moved",{id:i,location:t})}}),b=s?this._attachTooltip(t.element,t.title):void 0;this._editableHandles.set(i,{kind:c,source:t,cleanup:()=>{h?.(),b?.()},handle:m})}return r}_attachTooltip(t,e){t.id||="ha-map-editable-"+this._tooltipCount++;const a=document.createElement("ha-tooltip");return a.for=t.id,a.textContent=e,this.shadowRoot.append(a),()=>a.remove()}_removeEditableLocations(){for(const t of this._editableHandles.values())t.cleanup?.(),t.handle.remove();this._editableHandles.clear()}_computePathTooltip(t,e){let a;return a=t.fullDatetime?(0,d.r6)(e.timestamp,this._i18n.locale,this._config):(0,o.c)(e.timestamp)?(0,h.ie)(e.timestamp,this._i18n.locale,this._config):(0,h.Xs)(e.timestamp,this._i18n.locale,this._config),`${(0,z.D)(t.name??"")}<br>${a}`}_drawPaths(){if(!this._i18n||!this._config||!this._engine)return;const t=this.paths??[];if(this._pathHandles.splice(t.length).forEach(t=>t.remove()),!t.length)return;const e=getComputedStyle(this).getPropertyValue("--dark-primary-color");t.forEach((t,a)=>{let i,r;t.gradualOpacity&&(i=t.gradualOpacity/(t.points.length-2),r=1-t.gradualOpacity);const o=[],n=[];for(let e=0;e<t.points.length-1;e++){const a=t.gradualOpacity?r+e*i:void 0,s=t.points[e],l=t.points[e+1];if(n.push({location:s.point,opacity:a,tooltipHtml:this._computePathTooltip(t,s)}),Math.abs(s.point[1]-l.point[1])<=180)o.push({points:[s.point,l.point],opacity:a});else{const t=(l.point[1]-s.point[1]+540)%360-180;let e;e=0===t?(s.point[0]+l.point[0])/2:s.point[0]+(l.point[0]-s.point[0])*(s.point[1]>0?180-s.point[1]:-180-s.point[1])/t;const i=[e,s.point[1]>0?180:-180],r=[e,l.point[1]>0?180:-180];o.push({points:[s.point,i],opacity:a}),o.push({points:[r,l.point],opacity:a})}}const s=t.points.length-1;if(s>=0){const e=t.gradualOpacity?r+s*i:void 0;n.push({location:t.points[s].point,opacity:e,tooltipHtml:this._computePathTooltip(t,t.points[s])})}const l={color:t.color||e,segments:o,markers:n},c=this._pathHandles[a];c?c.update(l):this._pathHandles.push(this._engine.addPath(l))})}_drawEntities(){const t=this._states,e=this._engine;if(!t||!e||!this._formatters)return;this._entityHandles.forEach(t=>t.remove()),this._entityHandles=[],this._focusPoints=[],this._zoneHandles.forEach(t=>t.remove()),this._zoneHandles=[],this._focusZonePoints=[];let a=0;if(!this.entities)return this._zoneCircleHandles.splice(0).forEach(t=>t.remove()),this._entityMarkers.clear(),this._clusterAvatars.clear(),void e.setClustering(null);this._watchRegistry();const i=getComputedStyle(this);this._zonePositions={},this._zoneRadii={};for(const e of this.entities){const a=t[$(e)];!a||"zone"!==(0,m.t)(a)||!this.renderPassive&&a.attributes.passive||"number"==typeof a.attributes.latitude&&"number"==typeof a.attributes.longitude&&(this._zonePositions[a.entity_id]=[a.attributes.latitude,a.attributes.longitude],"number"==typeof a.attributes.radius&&(this._zoneRadii[a.entity_id]=a.attributes.radius))}const r=new Set;for(const o of this.entities){const n=t[$(o)];if(!n)continue;const s="string"!=typeof o?o.name:void 0,l=s??this._formatters.formatEntityName(n),{passive:c,icon:d,radius:h,entity_picture:p}=n.attributes,f=(0,b.H)(n,t);if(!f)continue;const{latitude:_,longitude:y,gpsAccuracy:v}=f,w=[_,y];if("zone"===(0,m.t)(n)){if(c&&!this.renderPassive)continue;const t="string"!=typeof o&&o.hide_radius,r=!c&&"string"!=typeof o&&o.color?o.color:(0,k.YG)(n.entity_id,!!c,this._entityReg,i);if(!t&&h){const t={radius:h,color:r},i=this._zoneCircleHandles[a];i?i.update(w,t):this._zoneCircleHandles.push(e.addCircle(w,t)),a++}const s=(0,M.x5)({color:r,icon:d,name:l});if(this.interactiveZones){const t=t=>{t.stopPropagation(),(0,u.r)(this,"hass-more-info",{entityId:n.entity_id})};s.addEventListener("click",t),s.addEventListener("keydown",e=>{"Enter"!==e.key&&" "!==e.key||(e.preventDefault(),t(e))})}this._zoneHandles.push(e.addMarker(s,w,{size:[36,36],interactive:this.interactiveZones,title:l})),"string"!=typeof o&&!1===o.focus||(!t&&h?this._focusZonePoints.push(...(0,g.Rn)(w,h)):this._focusZonePoints.push(w));continue}const x="string"!=typeof o&&"state"===o.label_mode?this._formatters.formatEntityState(n):"string"!=typeof o&&"attribute"===o.label_mode&&void 0!==o.attribute?this._formatters.formatEntityAttributeValue(n,o.attribute):s??l.split(" ").map(t=>t[0]).join("").substr(0,3),z=$(o),E=Y(this._entityMarkers,z,!r.has(z));r.add(z),E.showIcon="string"!=typeof o&&"icon"===o.label_mode,E.entityId=z,E.entityName=x,E.entityUnit="string"!=typeof o&&o.unit&&"attribute"===o.label_mode?o.unit:"",E.entityPicture=!p||"string"!=typeof o&&o.label_mode?"":this._connection.hassUrl(p);const C=("string"!=typeof o?o.color:void 0)||(0,k.lb)(z,this._entityReg,i);let S;if(E.entityColor=C,E.selected="string"!=typeof o&&(o.selected??!1),E.floating=!0,["person","device_tracker"].includes((0,m.t)(n))){const e=n.attributes.in_zones;if(Array.isArray(e)&&e.length>0){const a=(0,b._)(e,t);a&&this._zonePositions[a.entity_id]&&(S=a.entity_id)}else Array.isArray(e)&&["not_home",P.HV,P.Hh].includes(n.state)||(S=this._zoneContaining(w,v))}const A={entityId:z,title:l,picture:E.entityPicture||void 0,label:x,showIcon:E.showIcon,unit:E.entityUnit??"",color:C,selected:E.selected,zoneId:S},F=v||(E.selected?X:0),H=F>0&&!("string"!=typeof o&&o.hide_accuracy);this._entityHandles.push(e.addMarker(E,w,{...(0,L.i)(this._getMarkerSize(i),E.selected),title:l,cluster:!E.selected,raised:E.selected,clusterData:A,decoration:H?{radius:F,color:C,outline:F>Q}:void 0})),"string"!=typeof o&&!1===o.focus||this._focusPoints.push(w)}this._zoneCircleHandles.splice(a).forEach(t=>t.remove());const o=new Set(this.entities.map($));for(const t of[this._entityMarkers,this._clusterAvatars])for(const e of t.keys())o.has(e)||t.delete(e);e.setClustering(this.clusterMarkers?{radius:G,iconBuilder:this._createClusterBubble,groupKey:t=>t.clusterData?.zoneId,groupRadius:K}:null)}_zoneContaining(t,e=0){let a,i=1/0,r=1/0;for(const[o,n]of Object.entries(this._zoneRadii)){if(this._states[o]?.attributes.passive)continue;const s=(0,g.S_)(t,this._zonePositions[o]);s-e<n&&(n<i||n===i&&s<r)&&(a=o,i=n,r=s)}return a}_drawScaleRuler(){this._engine?.setScaleRuler(this.scaleRuler?{metric:"km"===this._config?.unit_system?.length}:null)}_getMarkerSize(t){const e=t.getPropertyValue("--ha-marker-size"),a=parseFloat(e);return Number.isNaN(a)?48:a}async _attachObserver(){this._resizeObserver||(this._resizeObserver=new ResizeObserver(()=>{this._engine?.invalidateSize(),this._runPendingFit()})),this._resizeObserver.observe(this)}constructor(...t){super(...t),this.clickable=!1,this.autoFit=!1,this.renderPassive=!1,this.interactiveZones=!1,this.fitZones=!1,this.zoomPosition="topleft",this._zonePositions={},this._zoneRadii={},this.themeMode="auto",this.zoom=14,this.clusterMarkers=!0,this.scaleRuler=!1,this._loaded=!1,this._editableHandles=new Map,this._entityReg=[],this._entityHandles=[],this._tooltipCount=0,this._entityMarkers=new Map,this._clusterAvatars=new Map,this._zoneHandles=[],this._zoneCircleHandles=[],this._pathHandles=[],this._focusPoints=[],this._focusZonePoints=[],this._clickCount=0,this._isProgrammaticFit=!1,this._pauseAutoFit=!1,this._handleVisibilityChange=async()=>{document.hidden||setTimeout(()=>{this._pauseAutoFit=!1},500)},this._resolveMapStyle=(0,l.A)(_.kR),this._mapDrawn=!1,this._loading=!1,this._forceLeaflet=!1,this._setupAttempt=0,this._hasFitted=!1,this._createClusterBubble=(t,e,a,i=!1)=>{const r=t.map(t=>t.clusterData),o=i||r.length<=N?r:r.slice(0,N-1),n=r.length-o.length,s=!!this.paths?.length,l=document.createElement("div");l.className="cluster-bubble";const c=new Set;for(const t of o){const e=Y(this._clusterAvatars,t?.entityId,!c.has(t?.entityId??""));t?.entityId&&c.add(t.entityId),e.entityId=t?.entityId,e.entityName=t?.label??"",e.entityUnit=t?.unit??"",e.showIcon=t?.showIcon??!1,e.entityPicture=t?.picture??"",e.entityColor=t?.color,s?(e.style.setProperty("--ha-marker-color",t?.color??"var(--primary-color)"),e.style.setProperty("--ha-marker-border-width","2px")):(e.style.removeProperty("--ha-marker-color"),e.style.removeProperty("--ha-marker-border-width")),e.selected=t?.selected??!1,(0,w.I)(e),i&&(0,w.l)(e,t?.title,!0),l.appendChild(e)}const d=i?Math.max(1,Math.floor((this.offsetWidth-2*O-2*I+D)/(Z+D))):o.length,h=Math.min(o.length,d),p=Math.ceil(o.length/d);let u=h*Z+(h-1)*D+2*I;if(n>0){const t=document.createElement("span");t.className="more",t.textContent=n>j?`${j}+`:`+${n}`,l.appendChild(t),u+=W+D}const m=p*Z+(p-1)*D+2*I+V,b=document.createElement("div");b.className="cluster-marker";const f=document.createElement("div");f.className="cluster-bubble-tail",b.append(l,f);const g=a?this._zonePositions[a]:void 0;return{element:b,size:[u,m],location:g,anchor:[u/2,m+(g?18+q:9)]}}}}tt.styles=n.AH`
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
    ${(0,n.iz)(v.xr)}
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
      padding: ${I}px;
      box-sizing: border-box;
      background: var(--card-background-color, #fff);
      border-radius: 14px;
      filter: var(--ha-cluster-shadow);
      --ha-marker-size: ${Z}px;
      --ha-marker-selected-scale: 1;
      --ha-marker-color: transparent;
      --ha-marker-border-width: 1px;
      --ha-marker-font-size: var(--ha-font-size-s);
      /* distinguish letter tiles from the bubble background */
      --ha-marker-background: var(--ha-color-fill-neutral-quiet-resting);
    }
    .cluster-bubble .more {
      flex: none;
      width: ${W}px;
      height: ${Z}px;
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
  `,(0,r._)([(0,s.wk)(),(0,c.Fg)({context:E.iN,subscribe:!0})],tt.prototype,"_states",void 0),(0,r._)([(0,s.wk)(),(0,c.Fg)({context:E.WF,subscribe:!0}),(0,p.p)({transformer:({config:t})=>t})],tt.prototype,"_config",void 0),(0,r._)([(0,s.wk)(),(0,c.Fg)({context:E.EK,subscribe:!0})],tt.prototype,"_ui",void 0),(0,r._)([(0,s.wk)(),(0,c.Fg)({context:E.D5,subscribe:!0})],tt.prototype,"_i18n",void 0),(0,r._)([(0,s.wk)(),(0,c.Fg)({context:E.p0,subscribe:!0})],tt.prototype,"_formatters",void 0),(0,r._)([(0,s.wk)(),(0,c.Fg)({context:E.Wq,subscribe:!0})],tt.prototype,"_connection",void 0),(0,r._)([(0,s.MZ)({attribute:!1})],tt.prototype,"entities",void 0),(0,r._)([(0,s.MZ)({attribute:!1})],tt.prototype,"paths",void 0),(0,r._)([(0,s.MZ)({attribute:!1})],tt.prototype,"editableLocations",void 0),(0,r._)([(0,s.MZ)({type:Boolean})],tt.prototype,"clickable",void 0),(0,r._)([(0,s.MZ)({attribute:"auto-fit",type:Boolean})],tt.prototype,"autoFit",void 0),(0,r._)([(0,s.MZ)({attribute:"render-passive",type:Boolean})],tt.prototype,"renderPassive",void 0),(0,r._)([(0,s.MZ)({attribute:"interactive-zones",type:Boolean})],tt.prototype,"interactiveZones",void 0),(0,r._)([(0,s.MZ)({attribute:"fit-zones",type:Boolean})],tt.prototype,"fitZones",void 0),(0,r._)([(0,s.MZ)({attribute:!1})],tt.prototype,"fitPadding",void 0),(0,r._)([(0,s.MZ)({attribute:"zoom-position"})],tt.prototype,"zoomPosition",void 0),(0,r._)([(0,s.MZ)({attribute:"theme-mode",type:String})],tt.prototype,"themeMode",void 0),(0,r._)([(0,s.MZ)({attribute:!1})],tt.prototype,"mapStyle",void 0),(0,r._)([(0,s.MZ)({type:Number})],tt.prototype,"zoom",void 0),(0,r._)([(0,s.MZ)({attribute:"cluster-markers",type:Boolean})],tt.prototype,"clusterMarkers",void 0),(0,r._)([(0,s.MZ)({attribute:"scale-ruler",type:Boolean})],tt.prototype,"scaleRuler",void 0),(0,r._)([(0,s.wk)()],tt.prototype,"_loaded",void 0),(0,r._)([(0,s.P)("#map")],tt.prototype,"_mapElement",void 0),(0,r._)([(0,s.wk)()],tt.prototype,"_entityReg",void 0),tt=(0,r._)([(0,s.EM)("ha-map")],tt),a.d(e,{},{$:T}),i()}catch(t){i(t)}})},38194(t,e,a){a(9336),a(29170),a(15740);var i=a(16056),r=a(82207);const o="X-Map-Tiles-Token",n=[0,400,1e3],s=[2e3,5e3,1e4,15e3];let l,c,d,h,p,u,m,b;const f=new Set,g=async t=>{const e=await t.sendMessagePromise({type:"map_tiles/access_token"});e.token!==l&&(l=e.token,f.forEach(t=>t(l)))},_=async(t,e)=>{for(const a of e){if(l)return;a&&await(0,r.l)(a);try{return void await g(t)}catch{}}},y=()=>{if(!m)return;const t=m;g(t).then(()=>v(t)).catch(()=>{})},v=t=>{l&&!p&&(p=setInterval(()=>{g(m??t).catch(()=>{})},12e5)),u!==t&&(u?.removeEventListener("ready",y),u=t,t.addEventListener("ready",y))},k=()=>m?(b??=g(m).catch(()=>{}).finally(()=>{b=void 0}),b):Promise.resolve(),w=t=>(f.add(t),()=>f.delete(t)),M=()=>(c??location.origin).replace(/\/+$/,"");a.d(e,{Oc:()=>k,Xx:()=>w,ZV:()=>i.Z},{bK:t=>t.startsWith("/")?`${M()}${t}`:t,pW:async t=>{if(m=t,c=t.options.auth?.data.hassUrl,l||(d??=_(t,n).finally(()=>{d=void 0}),await d),l)return v(t),l;h??=_(t,s).then(()=>v(t)).finally(()=>{h=void 0})},rG:t=>{let e;try{e=new URL(t,M())}catch{return{url:t}}if(!e.pathname.startsWith(`${i.Z}/`))return{url:e.href};const a=new URL(`${M()}${e.pathname}${e.search}`);return l?a.origin===location.origin?{url:a.href,headers:{[o]:l}}:(a.searchParams.set("token",l),{url:a.href}):{url:a.href}}})}};
//# sourceMappingURL=29524.0d265870397c84ad.js.map