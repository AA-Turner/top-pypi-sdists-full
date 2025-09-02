"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9656"],{76499:function(t,e,i){i.a(t,(async function(t,a){try{i.d(e,{WB:function(){return h},p6:function(){return d}});i(81738),i(29981);var o=i(57900),r=i(28105),s=i(43956),n=i(36641),l=t([o,n]);[o,n]=l.then?(await l)():l;(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{weekday:"long",month:"long",day:"numeric",timeZone:(0,n.f)(t.time_zone,e)})));const d=(t,e,i)=>c(e,i.time_zone).format(t),c=(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",timeZone:(0,n.f)(t.time_zone,e)}))),h=((0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"short",day:"numeric",timeZone:(0,n.f)(t.time_zone,e)}))),(t,e,i)=>{var a,o,r,n;const l=u(e,i.time_zone);if(e.date_format===s.t6.language||e.date_format===s.t6.system)return l.format(t);const d=l.formatToParts(t),c=null===(a=d.find((t=>"literal"===t.type)))||void 0===a?void 0:a.value,h=null===(o=d.find((t=>"day"===t.type)))||void 0===o?void 0:o.value,m=null===(r=d.find((t=>"month"===t.type)))||void 0===r?void 0:r.value,p=null===(n=d.find((t=>"year"===t.type)))||void 0===n?void 0:n.value,_=d[d.length-1];let g="literal"===(null==_?void 0:_.type)?null==_?void 0:_.value:"";"bg"===e.language&&e.date_format===s.t6.YMD&&(g="");return{[s.t6.DMY]:`${h}${c}${m}${c}${p}${g}`,[s.t6.MDY]:`${m}${c}${h}${c}${p}${g}`,[s.t6.YMD]:`${p}${c}${m}${c}${h}${g}`}[e.date_format]}),u=(0,r.Z)(((t,e)=>{const i=t.date_format===s.t6.system?void 0:t.language;return t.date_format===s.t6.language||(t.date_format,s.t6.system),new Intl.DateTimeFormat(i,{year:"numeric",month:"numeric",day:"numeric",timeZone:(0,n.f)(t.time_zone,e)})}));(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{day:"numeric",month:"short",timeZone:(0,n.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{month:"long",year:"numeric",timeZone:(0,n.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{month:"long",timeZone:(0,n.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{year:"numeric",timeZone:(0,n.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{weekday:"long",timeZone:(0,n.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{weekday:"short",timeZone:(0,n.f)(t.time_zone,e)})));a()}catch(d){a(d)}}))},40678:function(t,e,i){i.a(t,(async function(t,a){try{i.d(e,{o0:function(){return h}});var o=i(57900),r=i(28105),s=i(76499),n=i(9131),l=i(36641),d=i(13819),c=t([o,s,n,l]);[o,s,n,l]=c.then?(await c)():c;const h=(t,e,i)=>u(e,i.time_zone).format(t),u=(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",hour:(0,d.y)(t)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.y)(t)?"h12":"h23",timeZone:(0,l.f)(t.time_zone,e)})));(0,r.Z)((()=>new Intl.DateTimeFormat(void 0,{year:"numeric",month:"long",day:"numeric",hour:"2-digit",minute:"2-digit"}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"short",day:"numeric",hour:(0,d.y)(t)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.y)(t)?"h12":"h23",timeZone:(0,l.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{month:"short",day:"numeric",hour:(0,d.y)(t)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.y)(t)?"h12":"h23",timeZone:(0,l.f)(t.time_zone,e)}))),(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",hour:(0,d.y)(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,d.y)(t)?"h12":"h23",timeZone:(0,l.f)(t.time_zone,e)})));a()}catch(h){a(h)}}))},9131:function(t,e,i){i.a(t,(async function(t,a){try{i.d(e,{Vu:function(){return h},Zs:function(){return _},mr:function(){return d},xO:function(){return m}});var o=i(57900),r=i(28105),s=i(36641),n=i(13819),l=t([o,s]);[o,s]=l.then?(await l)():l;const d=(t,e,i)=>c(e,i.time_zone).format(t),c=(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,n.y)(t)?"h12":"h23",timeZone:(0,s.f)(t.time_zone,e)}))),h=(t,e,i)=>u(e,i.time_zone).format(t),u=(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{hour:(0,n.y)(t)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,n.y)(t)?"h12":"h23",timeZone:(0,s.f)(t.time_zone,e)}))),m=(t,e,i)=>p(e,i.time_zone).format(t),p=(0,r.Z)(((t,e)=>new Intl.DateTimeFormat(t.language,{weekday:"long",hour:(0,n.y)(t)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.y)(t)?"h12":"h23",timeZone:(0,s.f)(t.time_zone,e)}))),_=(t,e,i)=>g(e,i.time_zone).format(t),g=(0,r.Z)(((t,e)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,s.f)(t.time_zone,e)})));a()}catch(d){a(d)}}))},36641:function(t,e,i){i.a(t,(async function(t,a){try{i.d(e,{f:function(){return u}});var o,r,s,n=i(57900),l=i(43956),d=t([n]);n=(d.then?(await d)():d)[0];const c=null===(o=Intl.DateTimeFormat)||void 0===o||null===(r=(s=o.call(Intl)).resolvedOptions)||void 0===r?void 0:r.call(s).timeZone,h=null!=c?c:"UTC",u=(t,e)=>t===l.c_.local&&c?h:e;a()}catch(c){a(c)}}))},13819:function(t,e,i){i.d(e,{y:function(){return r}});i(39710),i(56389);var a=i(28105),o=i(43956);const r=(0,a.Z)((t=>{if(t.time_format===o.zt.language||t.time_format===o.zt.system){const e=t.time_format===o.zt.language?t.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(e).includes("10")}return t.time_format===o.zt.am_pm}))},94594:function(t,e,i){i.d(e,{F:function(){return a}});i(40777),i(26847),i(81738),i(6989),i(1455),i(27530);const a=async t=>{if(!t.parentNode)throw new Error("Cannot setup Leaflet map on disconnected element");const e=(await Promise.resolve().then(i.t.bind(i,25975,23))).default;e.Icon.Default.imagePath="/static/images/leaflet/images/",await i.e("150").then(i.t.bind(i,63295,23));const a=e.map(t),r=document.createElement("link");r.setAttribute("href","/static/images/leaflet/leaflet.css"),r.setAttribute("rel","stylesheet"),t.parentNode.appendChild(r);const s=document.createElement("link");s.setAttribute("href","/static/images/leaflet/MarkerCluster.css"),s.setAttribute("rel","stylesheet"),t.parentNode.appendChild(s),a.setView([52.3731339,4.8903147],13);return[a,e,o(e).addTo(a)]},o=t=>t.tileLayer("https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}"+(t.Browser.retina?"@2x.png":".png"),{attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attributions">CARTO</a>',subdomains:"abcd",minZoom:0,maxZoom:20})},26966:function(t,e,i){i.d(e,{k:function(){return o}});var a=i(25975);class o extends a.Marker{onAdd(t){var e;return super.onAdd(t),null===(e=this.decorationLayer)||void 0===e||e.addTo(t),this}onRemove(t){var e;return null===(e=this.decorationLayer)||void 0===e||e.remove(),super.onRemove(t)}constructor(t,e,i){super(t,i),this.decorationLayer=e}}},91337:function(t,e,i){i(26847),i(81738),i(22960),i(6989),i(87799),i(1455),i(27530);var a=i(73742),o=i(59048),r=i(7616),s=i(69342),n=i(29740);i(22543),i(32986);let l,d,c,h,u,m,p,_,g,y=t=>t;const f={boolean:()=>i.e("4852").then(i.bind(i,60751)),constant:()=>i.e("177").then(i.bind(i,85184)),float:()=>i.e("2369").then(i.bind(i,94980)),grid:()=>i.e("9219").then(i.bind(i,79998)),expandable:()=>i.e("4020").then(i.bind(i,71781)),integer:()=>i.e("3703").then(i.bind(i,12960)),multi_select:()=>Promise.all([i.e("4458"),i.e("514")]).then(i.bind(i,79298)),positive_time_period_dict:()=>i.e("2010").then(i.bind(i,49058)),select:()=>i.e("3162").then(i.bind(i,64324)),string:()=>i.e("2529").then(i.bind(i,72609)),optional_actions:()=>i.e("1601").then(i.bind(i,67552))},v=(t,e)=>t?!e.name||e.flatten?t:t[e.name]:null;class b extends o.oi{getFormProperties(){return{}}async focus(){await this.updateComplete;const t=this.renderRoot.querySelector(".root");if(t)for(const e of t.children)if("HA-ALERT"!==e.tagName){e instanceof o.fl&&await e.updateComplete,e.focus();break}}willUpdate(t){t.has("schema")&&this.schema&&this.schema.forEach((t=>{var e;"selector"in t||null===(e=f[t.type])||void 0===e||e.call(f)}))}render(){return(0,o.dy)(l||(l=y`
      <div class="root" part="root">
        ${0}
        ${0}
      </div>
    `),this.error&&this.error.base?(0,o.dy)(d||(d=y`
              <ha-alert alert-type="error">
                ${0}
              </ha-alert>
            `),this._computeError(this.error.base,this.schema)):"",this.schema.map((t=>{var e;const i=((t,e)=>t&&e.name?t[e.name]:null)(this.error,t),a=((t,e)=>t&&e.name?t[e.name]:null)(this.warning,t);return(0,o.dy)(c||(c=y`
            ${0}
            ${0}
          `),i?(0,o.dy)(h||(h=y`
                  <ha-alert own-margin alert-type="error">
                    ${0}
                  </ha-alert>
                `),this._computeError(i,t)):a?(0,o.dy)(u||(u=y`
                    <ha-alert own-margin alert-type="warning">
                      ${0}
                    </ha-alert>
                  `),this._computeWarning(a,t)):"","selector"in t?(0,o.dy)(m||(m=y`<ha-selector
                  .schema=${0}
                  .hass=${0}
                  .narrow=${0}
                  .name=${0}
                  .selector=${0}
                  .value=${0}
                  .label=${0}
                  .disabled=${0}
                  .placeholder=${0}
                  .helper=${0}
                  .localizeValue=${0}
                  .required=${0}
                  .context=${0}
                ></ha-selector>`),t,this.hass,this.narrow,t.name,t.selector,v(this.data,t),this._computeLabel(t,this.data),t.disabled||this.disabled||!1,t.required?"":t.default,this._computeHelper(t),this.localizeValue,t.required||!1,this._generateContext(t)):(0,s.h)(this.fieldElementName(t.type),Object.assign({schema:t,data:v(this.data,t),label:this._computeLabel(t,this.data),helper:this._computeHelper(t),disabled:this.disabled||t.disabled||!1,hass:this.hass,localize:null===(e=this.hass)||void 0===e?void 0:e.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(t)},this.getFormProperties())))})))}fieldElementName(t){return`ha-form-${t}`}_generateContext(t){if(!t.context)return;const e={};for(const[i,a]of Object.entries(t.context))e[i]=this.data[a];return e}createRenderRoot(){const t=super.createRenderRoot();return this.addValueChangedListener(t),t}addValueChangedListener(t){t.addEventListener("value-changed",(t=>{t.stopPropagation();const e=t.target.schema;if(t.target===this)return;const i=!e.name||"flatten"in e&&e.flatten?t.detail.value:{[e.name]:t.detail.value};this.data=Object.assign(Object.assign({},this.data),i),(0,n.B)(this,"value-changed",{value:this.data})}))}_computeLabel(t,e){return this.computeLabel?this.computeLabel(t,e):t?t.name:""}_computeHelper(t){return this.computeHelper?this.computeHelper(t):""}_computeError(t,e){return Array.isArray(t)?(0,o.dy)(p||(p=y`<ul>
        ${0}
      </ul>`),t.map((t=>(0,o.dy)(_||(_=y`<li>
              ${0}
            </li>`),this.computeError?this.computeError(t,e):t)))):this.computeError?this.computeError(t,e):t}_computeWarning(t,e){return this.computeWarning?this.computeWarning(t,e):t}constructor(...t){super(...t),this.narrow=!1,this.disabled=!1}}b.styles=(0,o.iv)(g||(g=y`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `)),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],b.prototype,"narrow",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"data",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"schema",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"error",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"warning",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],b.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"computeError",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"computeWarning",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"computeLabel",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"computeHelper",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],b.prototype,"localizeValue",void 0),b=(0,a.__decorate)([(0,r.Mo)("ha-form")],b)},4830:function(t,e,i){i.a(t,(async function(t,a){try{i.r(e),i.d(e,{HaLocationSelector:function(){return p}});i(26847),i(87799),i(27530);var o=i(73742),r=i(59048),s=i(7616),n=i(28105),l=i(29740),d=i(39107),c=(i(91337),t([d]));d=(c.then?(await c)():c)[0];let h,u,m=t=>t;class p extends r.oi{willUpdate(){var t;this.value||(this.value={latitude:this.hass.config.latitude,longitude:this.hass.config.longitude,radius:null!==(t=this.selector.location)&&void 0!==t&&t.radius?1e3:void 0})}render(){var t,e;return(0,r.dy)(h||(h=m`
      <p>${0}</p>
      <ha-locations-editor
        class="flex"
        .hass=${0}
        .helper=${0}
        .locations=${0}
        @location-updated=${0}
        @radius-updated=${0}
        pin-on-click
      ></ha-locations-editor>
      <ha-form
        .hass=${0}
        .schema=${0}
        .data=${0}
        .computeLabel=${0}
        .disabled=${0}
        @value-changed=${0}
      ></ha-form>
    `),this.label?this.label:"",this.hass,this.helper,this._location(this.selector,this.value),this._locationChanged,this._radiusChanged,this.hass,this._schema(this.hass.localize,null===(t=this.selector.location)||void 0===t?void 0:t.radius,null===(e=this.selector.location)||void 0===e?void 0:e.radius_readonly),this.value,this._computeLabel,this.disabled,this._valueChanged)}_locationChanged(t){const[e,i]=t.detail.location;(0,l.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.value),{},{latitude:e,longitude:i})})}_radiusChanged(t){const e=Math.round(t.detail.radius);(0,l.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.value),{},{radius:e})})}_valueChanged(t){var e,i;t.stopPropagation();const a=t.detail.value,o=Math.round(t.detail.value.radius);(0,l.B)(this,"value-changed",{value:Object.assign({latitude:a.latitude,longitude:a.longitude},null===(e=this.selector.location)||void 0===e||!e.radius||null!==(i=this.selector.location)&&void 0!==i&&i.radius_readonly?{}:{radius:o})})}constructor(...t){super(...t),this.disabled=!1,this._schema=(0,n.Z)(((t,e,i)=>[{name:"",type:"grid",schema:[{name:"latitude",required:!0,selector:{number:{step:"any",unit_of_measurement:"°"}}},{name:"longitude",required:!0,selector:{number:{step:"any",unit_of_measurement:"°"}}}]},...e?[{name:"radius",required:!0,default:1e3,disabled:!!i,selector:{number:{min:0,step:1,mode:"box",unit_of_measurement:t("ui.components.selectors.location.radius_meters")}}}]:[]])),this._location=(0,n.Z)(((t,e)=>{var i,a,o,r,s,n;const l=getComputedStyle(this),d=null!==(i=t.location)&&void 0!==i&&i.radius?l.getPropertyValue("--zone-radius-color")||l.getPropertyValue("--accent-color"):void 0;return[{id:"location",latitude:!e||isNaN(e.latitude)?this.hass.config.latitude:e.latitude,longitude:!e||isNaN(e.longitude)?this.hass.config.longitude:e.longitude,radius:null!==(a=t.location)&&void 0!==a&&a.radius?(null==e?void 0:e.radius)||1e3:void 0,radius_color:d,icon:null!==(o=t.location)&&void 0!==o&&o.icon||null!==(r=t.location)&&void 0!==r&&r.radius?"mdi:map-marker-radius":"mdi:map-marker",location_editable:!0,radius_editable:!(null===(s=t.location)||void 0===s||!s.radius||null!==(n=t.location)&&void 0!==n&&n.radius_readonly)}]})),this._computeLabel=t=>t.name?this.hass.localize(`ui.components.selectors.location.${t.name}`):""}}p.styles=(0,r.iv)(u||(u=m`
    ha-locations-editor {
      display: block;
      height: 400px;
      margin-bottom: 16px;
    }
    p {
      margin-top: 0;
    }
  `)),(0,o.__decorate)([(0,s.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,s.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,o.__decorate)([(0,s.Cb)({type:Object})],p.prototype,"value",void 0),(0,o.__decorate)([(0,s.Cb)()],p.prototype,"label",void 0),(0,o.__decorate)([(0,s.Cb)()],p.prototype,"helper",void 0),(0,o.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),p=(0,o.__decorate)([(0,s.Mo)("ha-selector-location")],p),a()}catch(h){a(h)}}))},27882:function(t,e,i){i.a(t,(async function(t,e){try{var a=i(73742),o=i(59048),r=i(7616),s=i(28177),n=i(18088),l=i(54974),d=(i(3847),i(40830),t([l]));l=(d.then?(await d)():d)[0];let c,h,u,m,p=t=>t;class _ extends o.oi{render(){var t,e;const i=this.icon||this.stateObj&&(null===(t=this.hass)||void 0===t||null===(t=t.entities[this.stateObj.entity_id])||void 0===t?void 0:t.icon)||(null===(e=this.stateObj)||void 0===e?void 0:e.attributes.icon);if(i)return(0,o.dy)(c||(c=p`<ha-icon .icon=${0}></ha-icon>`),i);if(!this.stateObj)return o.Ld;if(!this.hass)return this._renderFallback();const a=(0,l.gD)(this.hass,this.stateObj,this.stateValue).then((t=>t?(0,o.dy)(h||(h=p`<ha-icon .icon=${0}></ha-icon>`),t):this._renderFallback()));return(0,o.dy)(u||(u=p`${0}`),(0,s.C)(a))}_renderFallback(){const t=(0,n.N)(this.stateObj);return(0,o.dy)(m||(m=p`
      <ha-svg-icon
        .path=${0}
      ></ha-svg-icon>
    `),l.Ls[t]||l.Rb)}}(0,a.__decorate)([(0,r.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],_.prototype,"stateObj",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],_.prototype,"stateValue",void 0),(0,a.__decorate)([(0,r.Cb)()],_.prototype,"icon",void 0),_=(0,a.__decorate)([(0,r.Mo)("ha-state-icon")],_),e()}catch(c){e(c)}}))},77395:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(27530);var a=i(73742),o=i(59048),r=i(7616),s=i(20480),n=i(29740),l=i(27882),d=t([l]);l=(d.then?(await d)():d)[0];let c,h,u,m,p,_=t=>t;class g extends o.oi{render(){var t;return(0,o.dy)(c||(c=_`
      <div
        class="marker ${0}"
        style=${0}
        @click=${0}
      >
        ${0}
      </div>
    `),this.entityPicture?"picture":"",(0,s.V)({"border-color":this.entityColor}),this._badgeTap,this.entityPicture?(0,o.dy)(h||(h=_`<div
              class="entity-picture"
              style=${0}
            ></div>`),(0,s.V)({"background-image":`url(${this.entityPicture})`})):this.showIcon&&this.entityId?(0,o.dy)(u||(u=_`<ha-state-icon
                .hass=${0}
                .stateObj=${0}
              ></ha-state-icon>`),this.hass,null===(t=this.hass)||void 0===t?void 0:t.states[this.entityId]):this.entityUnit?(0,o.dy)(m||(m=_`
                  ${0}
                  <span
                    class="unit"
                    style="display: ${0}"
                    >${0}</span
                  >
                `),this.entityName,this.entityUnit?"initial":"none",this.entityUnit):this.entityName)}_badgeTap(t){t.stopPropagation(),this.entityId&&(0,n.B)(this,"hass-more-info",{entityId:this.entityId})}constructor(...t){super(...t),this.showIcon=!1}}g.styles=(0,o.iv)(p||(p=_`
    .marker {
      display: flex;
      justify-content: center;
      text-align: center;
      align-items: center;
      box-sizing: border-box;
      width: 48px;
      height: 48px;
      font-size: var(--ha-marker-font-size, var(--ha-font-size-xl));
      border-radius: var(--ha-marker-border-radius, 50%);
      border: 1px solid var(--ha-marker-color, var(--primary-color));
      color: var(--primary-text-color);
      background-color: var(--card-background-color);
    }
    .marker.picture {
      overflow: hidden;
    }
    .entity-picture {
      background-size: cover;
      height: 100%;
      width: 100%;
    }
    .unit {
      margin-left: 2px;
    }
  `)),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"entity-id",reflect:!0})],g.prototype,"entityId",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"entity-name"})],g.prototype,"entityName",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"entity-unit"})],g.prototype,"entityUnit",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"entity-picture"})],g.prototype,"entityPicture",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"entity-color"})],g.prototype,"entityColor",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"show-icon",type:Boolean})],g.prototype,"showIcon",void 0),customElements.define("ha-entity-marker",g),e()}catch(c){e(c)}}))},39107:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(2394),i(81738),i(94814),i(22960),i(6989),i(1455),i(27530);var a=i(73742),o=i(59048),r=i(7616),s=i(28105),n=i(29740),l=(i(42592),i(67146)),d=t([l]);l=(d.then?(await d)():d)[0];let c,h,u,m=t=>t;class p extends o.oi{fitMap(t){this.map.fitMap(t)}fitBounds(t,e){this.map.fitBounds(t,e)}async fitMarker(t,e){if(this.Leaflet||await this._loadPromise,!this.map.leafletMap||!this._locationMarkers)return;const i=this._locationMarkers[t];if(i)if("getBounds"in i)this.map.leafletMap.fitBounds(i.getBounds()),i.bringToFront();else{const a=this._circles[t];a?this.map.leafletMap.fitBounds(a.getBounds()):this.map.leafletMap.setView(i.getLatLng(),(null==e?void 0:e.zoom)||this.zoom)}}render(){return(0,o.dy)(c||(c=m`
      <ha-map
        .hass=${0}
        .layers=${0}
        .zoom=${0}
        .autoFit=${0}
        .themeMode=${0}
        .clickable=${0}
        @map-clicked=${0}
      ></ha-map>
      ${0}
    `),this.hass,this._getLayers(this._circles,this._locationMarkers),this.zoom,this.autoFit,this.themeMode,this.pinOnClick,this._mapClicked,this.helper?(0,o.dy)(h||(h=m`<ha-input-helper-text>${0}</ha-input-helper-text>`),this.helper):"")}willUpdate(t){super.willUpdate(t),this.Leaflet&&t.has("locations")&&this._updateMarkers()}updated(t){if(this.Leaflet&&t.has("locations")){var e;const a=t.get("locations"),o=null===(e=this.locations)||void 0===e?void 0:e.filter(((t,e)=>{var i,o;return!a[e]||(t.latitude!==a[e].latitude||t.longitude!==a[e].longitude)&&(null===(i=this.map.leafletMap)||void 0===i?void 0:i.getBounds().contains({lat:a[e].latitude,lng:a[e].longitude}))&&!(null!==(o=this.map.leafletMap)&&void 0!==o&&o.getBounds().contains({lat:t.latitude,lng:t.longitude}))}));var i;if(1===(null==o?void 0:o.length))null===(i=this.map.leafletMap)||void 0===i||i.panTo({lat:o[0].latitude,lng:o[0].longitude})}}_normalizeLongitude(t){return Math.abs(t)>180?(t%360+540)%360-180:t}_updateLocation(t){const e=t.target,i=e.getLatLng(),a=[i.lat,this._normalizeLongitude(i.lng)];(0,n.B)(this,"location-updated",{id:e.id,location:a},{bubbles:!1})}_updateRadius(t){const e=t.target,i=this._locationMarkers[e.id];(0,n.B)(this,"radius-updated",{id:e.id,radius:i.getRadius()},{bubbles:!1})}_markerClicked(t){const e=t.target;(0,n.B)(this,"marker-clicked",{id:e.id},{bubbles:!1})}_mapClicked(t){if(this.pinOnClick&&this._locationMarkers){const i=Object.keys(this._locationMarkers)[0],a=[t.detail.location[0],this._normalizeLongitude(t.detail.location[1])];var e;if((0,n.B)(this,"location-updated",{id:i,location:a},{bubbles:!1}),a[1]!==t.detail.location[1])null===(e=this.map.leafletMap)||void 0===e||e.panTo({lat:a[0],lng:a[1]})}}_updateMarkers(){if(!this.locations||!this.locations.length)return this._circles={},void(this._locationMarkers=void 0);const t={},e={},i=getComputedStyle(this).getPropertyValue("--accent-color");this.locations.forEach((a=>{let o;if(a.icon||a.iconPath){const t=document.createElement("div");let e;t.className="named-icon",void 0!==a.name&&(t.innerText=a.name),a.icon?(e=document.createElement("ha-icon"),e.setAttribute("icon",a.icon)):(e=document.createElement("ha-svg-icon"),e.setAttribute("path",a.iconPath)),t.prepend(e),o=this.Leaflet.divIcon({html:t.outerHTML,iconSize:[24,24],className:"light"})}if(a.radius){const r=this.Leaflet.circle([a.latitude,a.longitude],{color:a.radius_color||i,radius:a.radius});a.radius_editable||a.location_editable?(r.editing.enable(),r.addEventListener("add",(()=>{const t=r.editing._moveMarker,e=r.editing._resizeMarkers[0];o&&t.setIcon(o),e.id=t.id=a.id,t.addEventListener("dragend",(t=>this._updateLocation(t))).addEventListener("click",(t=>this._markerClicked(t))),a.radius_editable?e.addEventListener("dragend",(t=>this._updateRadius(t))):e.remove()})),t[a.id]=r):e[a.id]=r}if(!a.radius||!a.radius_editable&&!a.location_editable){const e={title:a.name,draggable:a.location_editable};o&&(e.icon=o);const i=this.Leaflet.marker([a.latitude,a.longitude],e).addEventListener("dragend",(t=>this._updateLocation(t))).addEventListener("click",(t=>this._markerClicked(t)));i.id=a.id,t[a.id]=i}})),this._circles=e,this._locationMarkers=t,(0,n.B)(this,"markers-updated")}constructor(){super(),this.autoFit=!1,this.zoom=16,this.themeMode="auto",this.pinOnClick=!1,this._circles={},this._getLayers=(0,s.Z)(((t,e)=>{const i=[];return Array.prototype.push.apply(i,Object.values(t)),e&&Array.prototype.push.apply(i,Object.values(e)),i})),this._loadPromise=Promise.resolve().then(i.t.bind(i,25975,23)).then((t=>i.e("9701").then(i.t.bind(i,99857,23)).then((()=>(this.Leaflet=t.default,this._updateMarkers(),this.updateComplete.then((()=>this.fitMap())))))))}}p.styles=(0,o.iv)(u||(u=m`
    ha-map {
      display: block;
      height: 100%;
    }
  `)),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"locations",void 0),(0,a.__decorate)([(0,r.Cb)()],p.prototype,"helper",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"auto-fit",type:Boolean})],p.prototype,"autoFit",void 0),(0,a.__decorate)([(0,r.Cb)({type:Number})],p.prototype,"zoom",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:"theme-mode",type:String})],p.prototype,"themeMode",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean,attribute:"pin-on-click"})],p.prototype,"pinOnClick",void 0),(0,a.__decorate)([(0,r.SB)()],p.prototype,"_locationMarkers",void 0),(0,a.__decorate)([(0,r.SB)()],p.prototype,"_circles",void 0),(0,a.__decorate)([(0,r.IO)("ha-map",!0)],p.prototype,"map",void 0),p=(0,a.__decorate)([(0,r.Mo)("ha-locations-editor")],p),e()}catch(c){e(c)}}))},67146:function(t,e,i){i.a(t,(async function(t,e){try{var a=i(52128),o=(i(26847),i(2394),i(81738),i(22960),i(6989),i(1455),i(27530),i(73742)),r=i(5870),s=i(59048),n=i(7616),l=i(29740),d=i(40678),c=i(9131),h=i(94594),u=i(18088),m=i(31298),p=i(78001),_=(i(78645),i(77395)),g=i(26966),y=t([a,_,d,c]);[a,_,d,c]=y.then?(await y)():y;let f,v=t=>t;const b=250,k=t=>"string"==typeof t?t:t.entity_id;class C extends s.fl{connectedCallback(){this._pauseAutoFit=!1,document.addEventListener("visibilitychange",this._handleVisibilityChange),this._handleVisibilityChange(),super.connectedCallback(),this._loadMap(),this._attachObserver()}disconnectedCallback(){super.disconnectedCallback(),document.removeEventListener("visibilitychange",this._handleVisibilityChange),this.leafletMap&&(this.leafletMap.remove(),this.leafletMap=void 0,this.Leaflet=void 0),this._loaded=!1,this._resizeObserver&&this._resizeObserver.unobserve(this)}update(t){var e,i;if(super.update(t),!this._loaded)return;let a=!1;const o=t.get("hass");if(t.has("_loaded")||t.has("entities"))this._drawEntities(),a=!this._pauseAutoFit;else if(this._loaded&&o&&this.entities)for(const r of this.entities)if(o.states[k(r)]!==this.hass.states[k(r)]){this._drawEntities(),a=!this._pauseAutoFit;break}t.has("clusterMarkers")&&this._drawEntities(),(t.has("_loaded")||t.has("paths"))&&this._drawPaths(),(t.has("_loaded")||t.has("layers"))&&(this._drawLayers(t.get("layers")),a=!0),(t.has("_loaded")||this.autoFit&&a)&&this.fitMap(),t.has("zoom")&&(this._isProgrammaticFit=!0,this.leafletMap.setZoom(this.zoom),setTimeout((()=>{this._isProgrammaticFit=!1}),b)),(t.has("themeMode")||t.has("hass")&&(!o||(null===(e=o.themes)||void 0===e?void 0:e.darkMode)!==(null===(i=this.hass.themes)||void 0===i?void 0:i.darkMode)))&&this._updateMapStyle()}get _darkMode(){return"dark"===this.themeMode||"auto"===this.themeMode&&Boolean(this.hass.themes.darkMode)}_updateMapStyle(){const t=this.renderRoot.querySelector("#map");t.classList.toggle("clickable",this.clickable),t.classList.toggle("dark",this._darkMode),t.classList.toggle("forced-dark","dark"===this.themeMode),t.classList.toggle("forced-light","light"===this.themeMode)}async _loadMap(){if(this._loading)return;let t=this.shadowRoot.getElementById("map");t||(t=document.createElement("div"),t.id="map",this.shadowRoot.append(t)),this._loading=!0;try{[this.leafletMap,this.Leaflet]=await(0,h.F)(t),this._updateMapStyle(),this.leafletMap.on("click",(t=>{0===this._clickCount&&setTimeout((()=>{1===this._clickCount&&(0,l.B)(this,"map-clicked",{location:[t.latlng.lat,t.latlng.lng]}),this._clickCount=0}),250),this._clickCount++})),this.leafletMap.on("zoomstart",(()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)})),this.leafletMap.on("movestart",(()=>{this._isProgrammaticFit||(this._pauseAutoFit=!0)})),this._loaded=!0}finally{this._loading=!1}}fitMap(t){var e,i,a,o;if(null!=t&&t.unpause_autofit&&(this._pauseAutoFit=!1),!this.leafletMap||!this.Leaflet||!this.hass)return;if(!(this._mapFocusItems.length||this._mapFocusZones.length||null!==(e=this.layers)&&void 0!==e&&e.length))return this._isProgrammaticFit=!0,this.leafletMap.setView(new this.Leaflet.LatLng(this.hass.config.latitude,this.hass.config.longitude),(null==t?void 0:t.zoom)||this.zoom),void setTimeout((()=>{this._isProgrammaticFit=!1}),b);let r=this.Leaflet.latLngBounds(this._mapFocusItems?this._mapFocusItems.map((t=>t.getLatLng())):[]);null===(i=this._mapFocusZones)||void 0===i||i.forEach((t=>{r.extend("getBounds"in t?t.getBounds():t.getLatLng())})),null===(a=this.layers)||void 0===a||a.forEach((t=>{r.extend("getBounds"in t?t.getBounds():t.getLatLng())})),r=r.pad(null!==(o=null==t?void 0:t.pad)&&void 0!==o?o:.5),this._isProgrammaticFit=!0,this.leafletMap.fitBounds(r,{maxZoom:(null==t?void 0:t.zoom)||this.zoom}),setTimeout((()=>{this._isProgrammaticFit=!1}),b)}fitBounds(t,e){var i;if(!this.leafletMap||!this.Leaflet||!this.hass)return;const a=this.Leaflet.latLngBounds(t).pad(null!==(i=null==e?void 0:e.pad)&&void 0!==i?i:.5);this._isProgrammaticFit=!0,this.leafletMap.fitBounds(a,{maxZoom:(null==e?void 0:e.zoom)||this.zoom}),setTimeout((()=>{this._isProgrammaticFit=!1}),b)}_drawLayers(t){if(t&&t.forEach((t=>t.remove())),!this.layers)return;const e=this.leafletMap;this.layers.forEach((t=>{e.addLayer(t)}))}_computePathTooltip(t,e){let i;return i=t.fullDatetime?(0,d.o0)(e.timestamp,this.hass.locale,this.hass.config):(0,r.z)(e.timestamp)?(0,c.Vu)(e.timestamp,this.hass.locale,this.hass.config):(0,c.xO)(e.timestamp,this.hass.locale,this.hass.config),`${t.name}<br>${i}`}_drawPaths(){const t=this.hass,e=this.leafletMap,i=this.Leaflet;if(!t||!e||!i)return;if(this._mapPaths.length&&(this._mapPaths.forEach((t=>t.remove())),this._mapPaths=[]),!this.paths)return;const a=getComputedStyle(this).getPropertyValue("--dark-primary-color");this.paths.forEach((t=>{let o,r;t.gradualOpacity&&(o=t.gradualOpacity/(t.points.length-2),r=1-t.gradualOpacity);for(let e=0;e<t.points.length-1;e++){const s=t.gradualOpacity?r+e*o:void 0;this._mapPaths.push(i.circleMarker(t.points[e].point,{radius:p.T?8:3,color:t.color||a,opacity:s,fillOpacity:s,interactive:!0}).bindTooltip(this._computePathTooltip(t,t.points[e]),{direction:"top"})),this._mapPaths.push(i.polyline([t.points[e].point,t.points[e+1].point],{color:t.color||a,opacity:s,interactive:!1}))}const s=t.points.length-1;if(s>=0){const e=t.gradualOpacity?r+s*o:void 0;this._mapPaths.push(i.circleMarker(t.points[s].point,{radius:p.T?8:3,color:t.color||a,opacity:e,fillOpacity:e,interactive:!0}).bindTooltip(this._computePathTooltip(t,t.points[s]),{direction:"top"}))}this._mapPaths.forEach((t=>e.addLayer(t)))}))}_drawEntities(){const t=this.hass,e=this.leafletMap,i=this.Leaflet;if(!t||!e||!i)return;if(this._mapItems.length&&(this._mapItems.forEach((t=>t.remove())),this._mapItems=[],this._mapFocusItems=[]),this._mapZones.length&&(this._mapZones.forEach((t=>t.remove())),this._mapZones=[],this._mapFocusZones=[]),this._mapCluster&&(this._mapCluster.remove(),this._mapCluster=void 0),!this.entities)return;const a=getComputedStyle(this),o=a.getPropertyValue("--accent-color"),r=a.getPropertyValue("--secondary-text-color"),s=a.getPropertyValue("--dark-primary-color"),n=this._darkMode?"dark":"light";for(const l of this.entities){const e=t.states[k(l)];if(!e)continue;const a="string"!=typeof l?l.name:void 0,d=null!=a?a:(0,m.C)(e),{latitude:c,longitude:h,passive:p,icon:_,radius:y,entity_picture:f,gps_accuracy:v}=e.attributes;if(!c||!h)continue;if("zone"===(0,u.N)(e)){if(p&&!this.renderPassive)continue;let t="";if(_){const e=document.createElement("ha-icon");e.setAttribute("icon",_),t=e.outerHTML}else{const e=document.createElement("span");e.innerHTML=d,t=e.outerHTML}const e=i.circle([c,h],{interactive:!1,color:p?r:o,radius:y}),a=new g.k([c,h],e,{icon:i.divIcon({html:t,iconSize:[24,24],className:n}),interactive:this.interactiveZones,title:d});this._mapZones.push(a),!this.fitZones||"string"!=typeof l&&!1===l.focus||this._mapFocusZones.push(e);continue}const b="string"!=typeof l&&"state"===l.label_mode?this.hass.formatEntityState(e):"string"!=typeof l&&"attribute"===l.label_mode&&void 0!==l.attribute?this.hass.formatEntityAttributeValue(e,l.attribute):null!=a?a:d.split(" ").map((t=>t[0])).join("").substr(0,3),C=document.createElement("ha-entity-marker");C.hass=this.hass,C.showIcon="string"!=typeof l&&"icon"===l.label_mode,C.entityId=k(l),C.entityName=b,C.entityUnit="string"!=typeof l&&l.unit&&"attribute"===l.label_mode?l.unit:"",C.entityPicture=!f||"string"!=typeof l&&l.label_mode?"":this.hass.hassUrl(f),"string"!=typeof l&&(C.entityColor=l.color);const w=new g.k([c,h],void 0,{icon:i.divIcon({html:C,iconSize:[48,48],className:""}),title:d});"string"!=typeof l&&!1===l.focus||this._mapFocusItems.push(w),v&&(w.decorationLayer=i.circle([c,h],{interactive:!1,color:s,radius:v})),this._mapItems.push(w)}this.clusterMarkers?(this._mapCluster=i.markerClusterGroup({showCoverageOnHover:!1,removeOutsideVisibleBounds:!1,maxClusterRadius:40}),this._mapCluster.addLayers(this._mapItems),e.addLayer(this._mapCluster)):this._mapItems.forEach((t=>e.addLayer(t))),this._mapZones.forEach((t=>e.addLayer(t)))}async _attachObserver(){this._resizeObserver||(this._resizeObserver=new ResizeObserver((()=>{var t;null===(t=this.leafletMap)||void 0===t||t.invalidateSize({debounceMoveend:!0})}))),this._resizeObserver.observe(this)}constructor(...t){super(...t),this.clickable=!1,this.autoFit=!1,this.renderPassive=!1,this.interactiveZones=!1,this.fitZones=!1,this.themeMode="auto",this.zoom=14,this.clusterMarkers=!0,this._loaded=!1,this._mapItems=[],this._mapFocusItems=[],this._mapZones=[],this._mapFocusZones=[],this._mapPaths=[],this._clickCount=0,this._isProgrammaticFit=!1,this._pauseAutoFit=!1,this._handleVisibilityChange=async()=>{document.hidden||setTimeout((()=>{this._pauseAutoFit=!1}),500)},this._loading=!1}}C.styles=(0,s.iv)(f||(f=v`
    :host {
      display: block;
      height: 300px;
    }
    #map {
      height: 100%;
    }
    #map.clickable {
      cursor: pointer;
    }
    #map.dark {
      background: #090909;
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
      cursor: -moz-grabbing;
      cursor: -webkit-grabbing;
    }
    .leaflet-tile-pane {
      filter: var(--map-filter);
    }
    .dark .leaflet-bar a {
      background-color: #1c1c1c;
      color: #ffffff;
    }
    .dark .leaflet-bar a:hover {
      background-color: #313131;
    }
    .leaflet-marker-draggable {
      cursor: move !important;
    }
    .leaflet-edit-resize {
      border-radius: 50%;
      cursor: nesw-resize !important;
    }
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
    .leaflet-control,
    .leaflet-top,
    .leaflet-bottom {
      z-index: 1 !important;
    }
    .leaflet-tooltip {
      padding: 8px;
      font-size: var(--ha-font-size-s);
      background: rgba(80, 80, 80, 0.9) !important;
      color: white !important;
      border-radius: 4px;
      box-shadow: none !important;
      text-align: center;
    }

    .marker-cluster div {
      background-clip: padding-box;
      background-color: var(--primary-color);
      border: 3px solid rgba(var(--rgb-primary-color), 0.2);
      width: 32px;
      height: 32px;
      border-radius: 20px;
      text-align: center;
      color: var(--text-primary-color);
      font-size: var(--ha-font-size-m);
    }

    .marker-cluster span {
      line-height: var(--ha-line-height-expanded);
    }
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],C.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],C.prototype,"entities",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],C.prototype,"paths",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],C.prototype,"layers",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],C.prototype,"clickable",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"auto-fit",type:Boolean})],C.prototype,"autoFit",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"render-passive",type:Boolean})],C.prototype,"renderPassive",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"interactive-zones",type:Boolean})],C.prototype,"interactiveZones",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"fit-zones",type:Boolean})],C.prototype,"fitZones",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"theme-mode",type:String})],C.prototype,"themeMode",void 0),(0,o.__decorate)([(0,n.Cb)({type:Number})],C.prototype,"zoom",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:"cluster-markers",type:Boolean})],C.prototype,"clusterMarkers",void 0),(0,o.__decorate)([(0,n.SB)()],C.prototype,"_loaded",void 0),C=(0,o.__decorate)([(0,n.Mo)("ha-map")],C),e()}catch(f){e(f)}}))},78001:function(t,e,i){i.d(e,{T:function(){return a}});const a="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0}}]);
//# sourceMappingURL=9656.552e97b4cdab1989.js.map