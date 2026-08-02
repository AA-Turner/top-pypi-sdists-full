export const __webpack_id__="5864";export const __webpack_ids__=["5864"];export const __webpack_modules__={68006:function(e,t,o){o.d(t,{z:()=>i});const i=e=>{if(void 0===e)return;if("object"!=typeof e){if("string"==typeof e||isNaN(e)){const t=e?.toString().split(":")||[];if(1===t.length)return{seconds:Number(t[0])};if(t.length>3)return;const o=Number(t[2])||0,i=Math.floor(o);return{hours:Number(t[0])||0,minutes:Number(t[1])||0,seconds:i,milliseconds:Math.floor(1e3*Number((o-i).toFixed(4)))}}return{seconds:e}}if(!("days"in e))return e;const{days:t,minutes:o,seconds:i,milliseconds:r}=e;let a=e.hours||0;return a=(a||0)+24*(t||0),{hours:a,minutes:o,seconds:i,milliseconds:r}}},48833:function(e,t,o){o.d(t,{P:()=>n});var i=o(58109),r=o(70076);const a=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],n=e=>e.first_weekday===r.zt.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,i.S)(e.language)%7:a.includes(e.first_weekday)?a.indexOf(e.first_weekday):1},84834:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{Yq:()=>d,zB:()=>u});var r=o(22),a=o(22786),n=o(70076),s=o(74309),l=e([r,s]);[r,s]=l.then?(await l)():l;(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",month:"long",day:"numeric",timeZone:(0,s.w)(e.time_zone,t)}));const d=(e,t,o)=>c(t,o.time_zone).format(e),c=(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",timeZone:(0,s.w)(e.time_zone,t)})),u=((0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"short",day:"numeric",timeZone:(0,s.w)(e.time_zone,t)})),(e,t,o)=>{const i=h(t,o.time_zone);if(t.date_format===n.ow.language||t.date_format===n.ow.system)return i.format(e);const r=i.formatToParts(e),a=r.find(e=>"literal"===e.type)?.value,s=r.find(e=>"day"===e.type)?.value,l=r.find(e=>"month"===e.type)?.value,d=r.find(e=>"year"===e.type)?.value,c=r[r.length-1];let u="literal"===c?.type?c?.value:"";"bg"===t.language&&t.date_format===n.ow.YMD&&(u="");return{[n.ow.DMY]:`${s}${a}${l}${a}${d}${u}`,[n.ow.MDY]:`${l}${a}${s}${a}${d}${u}`,[n.ow.YMD]:`${d}${a}${l}${a}${s}${u}`}[t.date_format]}),h=(0,a.A)((e,t)=>{const o=e.date_format===n.ow.system?void 0:e.language;return e.date_format===n.ow.language||(e.date_format,n.ow.system),new Intl.DateTimeFormat(o,{year:"numeric",month:"numeric",day:"numeric",timeZone:(0,s.w)(e.time_zone,t)})});(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{day:"numeric",month:"short",timeZone:(0,s.w)(e.time_zone,t)})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{month:"long",year:"numeric",timeZone:(0,s.w)(e.time_zone,t)})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{month:"long",timeZone:(0,s.w)(e.time_zone,t)})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",timeZone:(0,s.w)(e.time_zone,t)})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",timeZone:(0,s.w)(e.time_zone,t)})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"short",timeZone:(0,s.w)(e.time_zone,t)}));i()}catch(d){i(d)}})},49284:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{r6:()=>u,yg:()=>p});var r=o(22),a=o(22786),n=o(84834),s=o(4359),l=o(74309),d=o(59006),c=e([r,n,s,l]);[r,n,s,l]=c.then?(await c)():c;const u=(e,t,o)=>h(t,o.time_zone).format(e),h=(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,l.w)(e.time_zone,t)})),p=((0,a.A)(()=>new Intl.DateTimeFormat(void 0,{year:"numeric",month:"long",day:"numeric",hour:"2-digit",minute:"2-digit"})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"short",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,l.w)(e.time_zone,t)})),(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{month:"short",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,l.w)(e.time_zone,t)})),(e,t,o)=>m(t,o.time_zone).format(e)),m=(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{year:"numeric",month:"long",day:"numeric",hour:(0,d.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,d.J)(e)?"h12":"h23",timeZone:(0,l.w)(e.time_zone,t)}));i()}catch(u){i(u)}})},88738:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{i:()=>c,nR:()=>l});var r=o(22),a=o(22786),n=e([r]);r=(n.then?(await n)():n)[0];const s=e=>e<10?`0${e}`:e,l=(e,t)=>{const o=t.days||0,i=t.hours||0,r=t.minutes||0,a=t.seconds||0,n=t.milliseconds||0;return o>0?`${Intl.NumberFormat(e.language,{style:"unit",unit:"day",unitDisplay:"long"}).format(o)} ${i}:${s(r)}:${s(a)}`:i>0?`${i}:${s(r)}:${s(a)}`:r>0?`${r}:${s(a)}`:a>0?Intl.NumberFormat(e.language,{style:"unit",unit:"second",unitDisplay:"long"}).format(a):n>0?Intl.NumberFormat(e.language,{style:"unit",unit:"millisecond",unitDisplay:"long"}).format(n):null},d=(0,a.A)(e=>new Intl.DurationFormat(e.language,{style:"long"})),c=(e,t)=>d(e).format(t);(0,a.A)(e=>new Intl.DurationFormat(e.language,{style:"digital",hoursDisplay:"auto"})),(0,a.A)(e=>new Intl.DurationFormat(e.language,{style:"narrow",daysDisplay:"always"})),(0,a.A)(e=>new Intl.DurationFormat(e.language,{style:"narrow",hoursDisplay:"always"})),(0,a.A)(e=>new Intl.DurationFormat(e.language,{style:"narrow",minutesDisplay:"always"}));i()}catch(s){i(s)}})},4359:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{LW:()=>y,Xs:()=>p,fU:()=>d,ie:()=>u});var r=o(22),a=o(22786),n=o(74309),s=o(59006),l=e([r,n]);[r,n]=l.then?(await l)():l;const d=(e,t,o)=>c(t,o.time_zone).format(e),c=(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,s.J)(e)?"h12":"h23",timeZone:(0,n.w)(e.time_zone,t)})),u=(e,t,o)=>h(t,o.time_zone).format(e),h=(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,s.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,s.J)(e)?"h12":"h23",timeZone:(0,n.w)(e.time_zone,t)})),p=(e,t,o)=>m(t,o.time_zone).format(e),m=(0,a.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,s.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,s.J)(e)?"h12":"h23",timeZone:(0,n.w)(e.time_zone,t)})),y=(e,t,o)=>f(t,o.time_zone).format(e),f=(0,a.A)((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,n.w)(e.time_zone,t)}));i()}catch(d){i(d)}})},74309:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{w:()=>d});var r=o(22),a=o(70076),n=e([r]);r=(n.then?(await n)():n)[0];const s=Intl.DateTimeFormat?.().resolvedOptions?.().timeZone,l=s??"UTC",d=(e,t)=>e===a.Wj.local&&s?l:t;i()}catch(s){i(s)}})},21754:function(e,t,o){o.d(t,{A:()=>r});const i=e=>e<10?`0${e}`:e;function r(e){const t=Math.floor(e/3600),o=Math.floor(e%3600/60),r=Math.floor(e%3600%60);return t>0?`${t}:${i(o)}:${i(r)}`:o>0?`${o}:${i(r)}`:r>0?""+r:null}},59006:function(e,t,o){o.d(t,{J:()=>a});var i=o(22786),r=o(70076);const a=(0,i.A)(e=>{if(e.time_format===r.Hg.language||e.time_format===r.Hg.system){const t=e.time_format===r.Hg.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===r.Hg.am_pm})},42256:function(e,t,o){o.d(t,{I:()=>a});class i{addFromStorage(e){if(!this._storage[e]){const t=this.storage.getItem(e);t&&(this._storage[e]=JSON.parse(t))}}subscribeChanges(e,t){return this._listeners[e]?this._listeners[e].push(t):this._listeners[e]=[t],()=>{this.unsubscribeChanges(e,t)}}unsubscribeChanges(e,t){if(!(e in this._listeners))return;const o=this._listeners[e].indexOf(t);-1!==o&&this._listeners[e].splice(o,1)}hasKey(e){return e in this._storage}getValue(e){return this._storage[e]}setValue(e,t){const o=this._storage[e];this._storage[e]=t;try{void 0===t?this.storage.removeItem(e):this.storage.setItem(e,JSON.stringify(t))}catch(i){}finally{this._listeners[e]&&this._listeners[e].forEach(e=>e(o,t))}}constructor(e=window.localStorage){this._storage={},this._listeners={},this.storage=e,this.storage===window.localStorage&&window.addEventListener("storage",e=>{e.key&&this.hasKey(e.key)&&(this._storage[e.key]=e.newValue?JSON.parse(e.newValue):e.newValue,this._listeners[e.key]&&this._listeners[e.key].forEach(t=>t(e.oldValue?JSON.parse(e.oldValue):e.oldValue,this._storage[e.key])))})}}const r={};function a(e){return(t,o)=>{if("object"==typeof o)throw new Error("This decorator does not support this compilation type.");const a=e.storage||"localStorage";let n;a&&a in r?n=r[a]:(n=new i(window[a]),r[a]=n);const s=e.key||String(o);n.addFromStorage(s);const l=!1!==e.subscribe?e=>n.subscribeChanges(s,(t,i)=>{e.requestUpdate(o,t)}):void 0,d=()=>n.hasKey(s)?e.deserializer?e.deserializer(n.getValue(s)):n.getValue(s):void 0,c=(t,i)=>{let r;e.state&&(r=d()),n.setValue(s,e.serializer?e.serializer(i):i),e.state&&t.requestUpdate(o,r)},u=t.performUpdate;if(t.performUpdate=function(){this.__initialized=!0,u.call(this)},e.subscribe){const e=t.connectedCallback,o=t.disconnectedCallback;t.connectedCallback=function(){e.call(this);const t=this;t.__unbsubLocalStorage||(t.__unbsubLocalStorage=l?.(this))},t.disconnectedCallback=function(){o.call(this);this.__unbsubLocalStorage?.(),this.__unbsubLocalStorage=void 0}}const h=Object.getOwnPropertyDescriptor(t,o);let p;if(void 0===h)p={get(){return d()},set(e){(this.__initialized||void 0===d())&&c(this,e)},configurable:!0,enumerable:!0};else{const e=h.set;p={...h,get(){return d()},set(t){(this.__initialized||void 0===d())&&c(this,t),e?.call(this,t)}}}Object.defineProperty(t,o,p)}}},91737:function(e,t,o){o.d(t,{C:()=>i});const i=e=>{e.preventDefault(),e.stopPropagation()}},48551:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{R:()=>u});var r=o(2654),a=(o(34099),o(84834)),n=o(49284),s=o(20679),l=o(74522),d=(o(24131),o(41144)),c=e([r,a,n,s]);[r,a,n,s]=c.then?(await c)():c;const u=(e,t,o,i)=>{const r=t.entity_id,a=t.attributes.device_class,n=(0,d.m)(r),s=o[r],c=s?.translation_key;return c&&e(`component.${s.platform}.entity.${n}.${c}.state_attributes.${i}.name`)||a&&e(`component.${n}.entity_component.${a}.state_attributes.${i}.name`)||e(`component.${n}.entity_component._.state_attributes.${i}.name`)||(0,l.Z)(i.replace(/_/g," ").replace(/\bid\b/g,"ID").replace(/\bip\b/g,"IP").replace(/\bmac\b/g,"MAC").replace(/\bgps\b/g,"GPS"))};i()}catch(u){i(u)}})},47644:function(e,t,o){o.d(t,{X:()=>i});const i=e=>e.name?.trim()},28724:function(e,t,o){o.d(t,{e:()=>i});const i=e=>"latitude"in e.attributes&&"longitude"in e.attributes},74522:function(e,t,o){o.d(t,{Z:()=>i});const i=e=>e.charAt(0).toUpperCase()+e.slice(1)},39680:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{c:()=>s,q:()=>l});var r=o(22),a=o(22786),n=e([r]);r=(n.then?(await n)():n)[0];const s=(e,t)=>d(e).format(t),l=(e,t)=>c(e).format(t),d=(0,a.A)(e=>new Intl.ListFormat(e.language,{style:"long",type:"conjunction"})),c=(0,a.A)(e=>new Intl.ListFormat(e.language,{style:"long",type:"disjunction"}));i()}catch(s){i(s)}})},24131:function(){const e="^\\d{4}-(0[1-9]|1[0-2])-([12]\\d|0[1-9]|3[01])";new RegExp(e+"$"),new RegExp(e)},91225:function(e,t,o){o.d(t,{_:()=>r});var i=o(63533);const r=(e,t)=>{if(!(t instanceof i.C5))return{warnings:[t.message],errors:void 0};const o=[],r=[];for(const i of t.failures())if(void 0===i.value)o.push(e.localize("ui.errors.config.key_missing",{key:i.path.join(".")}));else if("never"===i.type)r.push(e.localize("ui.errors.config.key_not_expected",{key:i.path.join(".")}));else{if("union"===i.type)continue;"enums"===i.type?r.push(e.localize("ui.errors.config.key_wrong_type",{key:i.path.join("."),type_correct:i.message.replace("Expected ","").split(", ")[0],type_wrong:JSON.stringify(i.value)})):r.push(e.localize("ui.errors.config.key_wrong_type",{key:i.path.join("."),type_correct:i.refinement||i.type,type_wrong:JSON.stringify(i.value)}))}return{warnings:r,errors:o}}},9169:function(e,t,o){o(76679)},7078:function(e,t,o){o.d(t,{V:()=>b});var i=o(62826),r=o(16527),a=o(96196),n=o(77845),s=o(92542),l=o(34972),d=o(74687),c=o(5691),u=o(28522);class h extends c.${}h.styles=[u.R,a.AH`
      :host {
        --ha-icon-display: block;
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-secondary: var(--secondary-text-color);
        --md-sys-color-surface: var(--card-background-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--secondary-text-color);
      }
    `],h=(0,i.__decorate)([(0,n.EM)("ha-md-select-option")],h);var p=o(38048),m=o(7138),y=o(83538);class f extends p.V{}f.styles=[m.R,y.R,a.AH`
      :host {
        --ha-icon-display: block;
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-secondary: var(--secondary-text-color);
        --md-sys-color-surface: var(--card-background-color);
        --md-sys-color-on-surface-variant: var(--secondary-text-color);

        --md-sys-color-surface-container-highest: var(--input-fill-color);
        --md-sys-color-on-surface: var(--input-ink-color);

        --md-sys-color-surface-container: var(--input-fill-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-sys-color-secondary-container: var(--input-fill-color);
        --md-menu-container-color: var(--card-background-color);
      }
    `],f=(0,i.__decorate)([(0,n.EM)("ha-md-select")],f);var g=o(55124);const _="NO_AUTOMATION",v="UNKNOWN_AUTOMATION";class b extends a.WF{get NO_AUTOMATION_TEXT(){return this.hass.localize("ui.panel.config.devices.automation.actions.no_actions")}get UNKNOWN_AUTOMATION_TEXT(){return this.hass.localize("ui.panel.config.devices.automation.actions.unknown_action")}get _value(){if(!this.value)return"";if(!this._automations.length)return _;const e=this._automations.findIndex(e=>(0,d.Po)(this._entityReg,e,this.value));return-1===e?v:`${this._automations[e].device_id}_${e}`}render(){if(this._renderEmpty)return a.s6;const e=this._value;return a.qy`
      <ha-md-select
        .label=${this.label}
        .value=${e}
        @change=${this._automationChanged}
        @closed=${g.d}
        .disabled=${0===this._automations.length}
      >
        ${e===_?a.qy`<ha-md-select-option .value=${_}>
              ${this.NO_AUTOMATION_TEXT}
            </ha-md-select-option>`:a.s6}
        ${e===v?a.qy`<ha-md-select-option .value=${v}>
              ${this.UNKNOWN_AUTOMATION_TEXT}
            </ha-md-select-option>`:a.s6}
        ${this._automations.map((e,t)=>a.qy`
            <ha-md-select-option .value=${`${e.device_id}_${t}`}>
              ${this._localizeDeviceAutomation(this.hass,this._entityReg,e)}
            </ha-md-select-option>
          `)}
      </ha-md-select>
    `}updated(e){super.updated(e),e.has("deviceId")&&this._updateDeviceInfo()}async _updateDeviceInfo(){this._automations=this.deviceId?(await this._fetchDeviceAutomations(this.hass,this.deviceId)).sort(d.RK):[],this.value&&this.value.device_id===this.deviceId||this._setValue(this._automations.length?this._automations[0]:this._createNoAutomation(this.deviceId)),this._renderEmpty=!0,await this.updateComplete,this._renderEmpty=!1}_automationChanged(e){const t=e.target.value;if(!t||[v,_].includes(t))return;const[o,i]=t.split("_"),r=this._automations[i];r.device_id===o&&this._setValue(r)}_setValue(e){if(this.value&&(0,d.Po)(this._entityReg,e,this.value))return;const t={...e};delete t.metadata,(0,s.r)(this,"value-changed",{value:t})}constructor(e,t,o){super(),this._automations=[],this._renderEmpty=!1,this._localizeDeviceAutomation=e,this._fetchDeviceAutomations=t,this._createNoAutomation=o}}b.styles=a.AH`
    ha-select {
      display: block;
    }
  `,(0,i.__decorate)([(0,n.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,i.__decorate)([(0,n.MZ)()],b.prototype,"label",void 0),(0,i.__decorate)([(0,n.MZ)({attribute:!1})],b.prototype,"deviceId",void 0),(0,i.__decorate)([(0,n.MZ)({type:Object})],b.prototype,"value",void 0),(0,i.__decorate)([(0,n.wk)()],b.prototype,"_automations",void 0),(0,i.__decorate)([(0,n.wk)()],b.prototype,"_renderEmpty",void 0),(0,i.__decorate)([(0,n.wk)(),(0,r.Fg)({context:l.ih,subscribe:!0})],b.prototype,"_entityReg",void 0)},60977:function(e,t,o){o.a(e,async function(e,t){try{var i=o(62826),r=o(96196),a=o(77845),n=o(22786),s=o(92542),l=o(56403),d=o(16727),c=o(13877),u=o(3950),h=o(74839),p=o(76681),m=o(96943),y=e([m]);m=(y.then?(await y)():y)[0];class f extends r.WF{firstUpdated(e){super.firstUpdated(e),this._loadConfigEntries()}async _loadConfigEntries(){const e=await(0,u.VN)(this.hass);this._configEntryLookup=Object.fromEntries(e.map(e=>[e.entry_id,e]))}render(){const e=this.placeholder??this.hass.localize("ui.components.device-picker.placeholder"),t=this._valueRenderer(this._configEntryLookup);return r.qy`
      <ha-generic-picker
        .hass=${this.hass}
        .autofocus=${this.autofocus}
        .label=${this.label}
        .searchLabel=${this.searchLabel}
        .notFoundLabel=${this._notFoundLabel}
        .emptyLabel=${this.hass.localize("ui.components.device-picker.no_devices")}
        .placeholder=${e}
        .value=${this.value}
        .rowRenderer=${this._rowRenderer}
        .getItems=${this._getItems}
        .hideClearIcon=${this.hideClearIcon}
        .valueRenderer=${t}
        @value-changed=${this._valueChanged}
      >
      </ha-generic-picker>
    `}async open(){await this.updateComplete,await(this._picker?.open())}_valueChanged(e){e.stopPropagation();const t=e.detail.value;this.value=t,(0,s.r)(this,"value-changed",{value:t})}constructor(...e){super(...e),this.autofocus=!1,this.disabled=!1,this.required=!1,this.hideClearIcon=!1,this._configEntryLookup={},this._getDevicesMemoized=(0,n.A)(h.oG),this._getItems=()=>this._getDevicesMemoized(this.hass,this._configEntryLookup,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeDevices,this.value),this._valueRenderer=(0,n.A)(e=>t=>{const o=t,i=this.hass.devices[o];if(!i)return r.qy`<span slot="headline">${o}</span>`;const{area:a}=(0,c.w)(i,this.hass),n=i?(0,d.xn)(i):void 0,s=a?(0,l.A)(a):void 0,u=i.primary_config_entry?e[i.primary_config_entry]:void 0;return r.qy`
        ${u?r.qy`<img
              slot="start"
              alt=""
              crossorigin="anonymous"
              referrerpolicy="no-referrer"
              src=${(0,p.MR)({domain:u.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}
            />`:r.s6}
        <span slot="headline">${n}</span>
        <span slot="supporting-text">${s}</span>
      `}),this._rowRenderer=e=>r.qy`
    <ha-combo-box-item type="button">
      ${e.domain?r.qy`
            <img
              slot="start"
              alt=""
              crossorigin="anonymous"
              referrerpolicy="no-referrer"
              src=${(0,p.MR)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes.darkMode})}
            />
          `:r.s6}

      <span slot="headline">${e.primary}</span>
      ${e.secondary?r.qy`<span slot="supporting-text">${e.secondary}</span>`:r.s6}
      ${e.domain_name?r.qy`
            <div slot="trailing-supporting-text" class="domain">
              ${e.domain_name}
            </div>
          `:r.s6}
    </ha-combo-box-item>
  `,this._notFoundLabel=e=>this.hass.localize("ui.components.device-picker.no_match",{term:r.qy`<b>‘${e}’</b>`})}}(0,i.__decorate)([(0,a.MZ)({attribute:!1})],f.prototype,"hass",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],f.prototype,"autofocus",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],f.prototype,"disabled",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],f.prototype,"required",void 0),(0,i.__decorate)([(0,a.MZ)()],f.prototype,"label",void 0),(0,i.__decorate)([(0,a.MZ)()],f.prototype,"value",void 0),(0,i.__decorate)([(0,a.MZ)()],f.prototype,"helper",void 0),(0,i.__decorate)([(0,a.MZ)()],f.prototype,"placeholder",void 0),(0,i.__decorate)([(0,a.MZ)({type:String,attribute:"search-label"})],f.prototype,"searchLabel",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:!1,type:Array})],f.prototype,"createDomains",void 0),(0,i.__decorate)([(0,a.MZ)({type:Array,attribute:"include-domains"})],f.prototype,"includeDomains",void 0),(0,i.__decorate)([(0,a.MZ)({type:Array,attribute:"exclude-domains"})],f.prototype,"excludeDomains",void 0),(0,i.__decorate)([(0,a.MZ)({type:Array,attribute:"include-device-classes"})],f.prototype,"includeDeviceClasses",void 0),(0,i.__decorate)([(0,a.MZ)({type:Array,attribute:"exclude-devices"})],f.prototype,"excludeDevices",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:!1})],f.prototype,"deviceFilter",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:!1})],f.prototype,"entityFilter",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"hide-clear-icon",type:Boolean})],f.prototype,"hideClearIcon",void 0),(0,i.__decorate)([(0,a.P)("ha-generic-picker")],f.prototype,"_picker",void 0),(0,i.__decorate)([(0,a.wk)()],f.prototype,"_configEntryLookup",void 0),f=(0,i.__decorate)([(0,a.EM)("ha-device-picker")],f),t()}catch(f){t(f)}})},27639:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845),n=o(92542);o(60733);class s extends r.WF{render(){return r.qy`
      <div
        class="row"
        tabindex="0"
        role="button"
        @keydown=${this._handleKeydown}
      >
        ${this.leftChevron?r.qy`
              <ha-icon-button
                class="expand-button"
                .path=${"M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z"}
                @click=${this._handleExpand}
                @keydown=${this._handleExpand}
              ></ha-icon-button>
            `:r.s6}
        <div class="leading-icon-wrapper">
          <slot name="leading-icon"></slot>
        </div>
        <slot class="header" name="header"></slot>
        <slot name="icons"></slot>
      </div>
    `}async _handleExpand(e){e.defaultPrevented||"keydown"===e.type&&"Enter"!==e.key&&" "!==e.key||(e.stopPropagation(),e.preventDefault(),(0,n.r)(this,"toggle-collapsed"))}async _handleKeydown(e){if(!(e.defaultPrevented||"Enter"!==e.key&&" "!==e.key&&(!this.sortSelected&&!e.altKey||e.ctrlKey||e.metaKey||e.shiftKey||"ArrowUp"!==e.key&&"ArrowDown"!==e.key))){if(e.preventDefault(),e.stopPropagation(),"ArrowUp"===e.key||"ArrowDown"===e.key)return"ArrowUp"===e.key?void(0,n.r)(this,"move-up"):void(0,n.r)(this,"move-down");!this.sortSelected||"Enter"!==e.key&&" "!==e.key?this.click():(0,n.r)(this,"stop-sort-selection")}}focus(){requestAnimationFrame(()=>{this._rowElement?.focus()})}constructor(...e){super(...e),this.leftChevron=!1,this.collapsed=!1,this.selected=!1,this.sortSelected=!1,this.disabled=!1,this.buildingBlock=!1}}s.styles=r.AH`
    :host {
      display: block;
    }
    .row {
      display: flex;
      padding: var(--ha-space-0) var(--ha-space-2);
      min-height: 48px;
      align-items: center;
      cursor: pointer;
      overflow: hidden;
      font-weight: var(--ha-font-weight-medium);
      outline: none;
      border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
    }
    .row:focus {
      outline: var(--wa-focus-ring);
      outline-offset: -2px;
    }
    .expand-button {
      transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
      color: var(--ha-color-on-neutral-quiet);
      margin-left: calc(var(--ha-space-2) * -1);
    }
    :host([building-block]) .leading-icon-wrapper {
      background-color: var(--ha-color-fill-neutral-loud-resting);
      border-radius: var(--ha-border-radius-md);
      padding: var(--ha-space-1);
      display: flex;
      justify-content: center;
      align-items: center;
      transform: rotate(45deg);
    }
    ::slotted([slot="leading-icon"]) {
      color: var(--ha-color-on-neutral-quiet);
    }
    :host([building-block]) ::slotted([slot="leading-icon"]) {
      --mdc-icon-size: var(--ha-space-5);
      color: var(--white-color);
      transform: rotate(-45deg);
    }
    :host([collapsed]) .expand-button {
      transform: rotate(180deg);
    }
    :host([selected]) .row,
    :host([selected]) .row:focus {
      outline: solid;
      outline-color: var(--primary-color);
      outline-offset: -2px;
      outline-width: 2px;
    }
    :host([disabled]) .row {
      border-top-right-radius: var(--ha-border-radius-square);
      border-top-left-radius: var(--ha-border-radius-square);
    }
    ::slotted([slot="header"]) {
      flex: 1;
      overflow-wrap: anywhere;
      margin: var(--ha-space-0) var(--ha-space-3);
    }
    :host([sort-selected]) .row {
      outline: solid;
      outline-color: rgba(var(--rgb-accent-color), 0.6);
      outline-offset: -2px;
      outline-width: 2px;
      background-color: rgba(var(--rgb-accent-color), 0.08);
    }
    .row:hover {
      background-color: rgba(var(--rgb-primary-text-color), 0.04);
    }
    :host([highlight]) .row {
      background-color: rgba(var(--rgb-primary-color), 0.08);
    }
    :host([highlight]) .row:hover {
      background-color: rgba(var(--rgb-primary-color), 0.16);
    }
  `,(0,i.__decorate)([(0,a.MZ)({attribute:"left-chevron",type:Boolean})],s.prototype,"leftChevron",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],s.prototype,"collapsed",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],s.prototype,"selected",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0,attribute:"sort-selected"})],s.prototype,"sortSelected",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],s.prototype,"disabled",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0,attribute:"building-block"})],s.prototype,"buildingBlock",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],s.prototype,"highlight",void 0),(0,i.__decorate)([(0,a.P)(".row")],s.prototype,"_rowElement",void 0),s=(0,i.__decorate)([(0,a.EM)("ha-automation-row")],s)},16857:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845),n=o(76679);o(41742),o(1554);class s extends r.WF{get items(){return this._menu?.items}get selected(){return this._menu?.selected}focus(){this._menu?.open?this._menu.focusItemAtIndex(0):this._triggerButton?.focus()}render(){return r.qy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <ha-menu
        .corner=${this.corner}
        .menuCorner=${this.menuCorner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
        .y=${this.y}
        .x=${this.x}
      >
        <slot></slot>
      </ha-menu>
    `}firstUpdated(e){super.firstUpdated(e),"rtl"===n.G.document.dir&&this.updateComplete.then(()=>{this.querySelectorAll("ha-list-item").forEach(e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)})})}_handleClick(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...e){super(...e),this.corner="BOTTOM_START",this.menuCorner="START",this.x=null,this.y=null,this.multi=!1,this.activatable=!1,this.disabled=!1,this.fixed=!1,this.noAnchor=!1}}s.styles=r.AH`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `,(0,i.__decorate)([(0,a.MZ)()],s.prototype,"corner",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"menu-corner"})],s.prototype,"menuCorner",void 0),(0,i.__decorate)([(0,a.MZ)({type:Number})],s.prototype,"x",void 0),(0,i.__decorate)([(0,a.MZ)({type:Number})],s.prototype,"y",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],s.prototype,"multi",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],s.prototype,"activatable",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],s.prototype,"disabled",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],s.prototype,"fixed",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,attribute:"no-anchor"})],s.prototype,"noAnchor",void 0),(0,i.__decorate)([(0,a.P)("ha-menu",!0)],s.prototype,"_menu",void 0),s=(0,i.__decorate)([(0,a.EM)("ha-button-menu")],s)},95379:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845);class n extends r.WF{render(){return r.qy`
      ${this.header?r.qy`<h1 class="card-header">${this.header}</h1>`:r.s6}
      <slot></slot>
    `}constructor(...e){super(...e),this.raised=!1}}n.styles=r.AH`
    :host {
      background: var(
        --ha-card-background,
        var(--card-background-color, white)
      );
      -webkit-backdrop-filter: var(--ha-card-backdrop-filter, none);
      backdrop-filter: var(--ha-card-backdrop-filter, none);
      box-shadow: var(--ha-card-box-shadow, none);
      box-sizing: border-box;
      border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
      border-width: var(--ha-card-border-width, 1px);
      border-style: solid;
      border-color: var(--ha-card-border-color, var(--divider-color, #e0e0e0));
      color: var(--primary-text-color);
      display: block;
      transition: all 0.3s ease-out;
      position: relative;
    }

    :host([raised]) {
      border: none;
      box-shadow: var(
        --ha-card-box-shadow,
        0px 2px 1px -1px rgba(0, 0, 0, 0.2),
        0px 1px 1px 0px rgba(0, 0, 0, 0.14),
        0px 1px 3px 0px rgba(0, 0, 0, 0.12)
      );
    }

    .card-header,
    :host ::slotted(.card-header) {
      color: var(--ha-card-header-color, var(--primary-text-color));
      font-family: var(--ha-card-header-font-family, inherit);
      font-size: var(--ha-card-header-font-size, var(--ha-font-size-2xl));
      letter-spacing: -0.012em;
      line-height: var(--ha-line-height-expanded);
      padding: var(--ha-space-3) var(--ha-space-4) var(--ha-space-4);
      display: block;
      margin-block-start: var(--ha-space-0);
      margin-block-end: var(--ha-space-0);
      font-weight: var(--ha-font-weight-normal);
    }

    :host ::slotted(.card-content:not(:first-child)),
    slot:not(:first-child)::slotted(.card-content) {
      padding-top: var(--ha-space-0);
      margin-top: calc(var(--ha-space-2) * -1);
    }

    :host ::slotted(.card-content) {
      padding: var(--ha-space-4);
    }

    :host ::slotted(.card-actions) {
      border-top: 1px solid var(--divider-color, #e8e8e8);
      padding: var(--ha-space-2);
    }
  `,(0,i.__decorate)([(0,a.MZ)()],n.prototype,"header",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],n.prototype,"raised",void 0),n=(0,i.__decorate)([(0,a.EM)("ha-card")],n)},34811:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845),n=o(94333),s=o(92542),l=o(99034);o(60961);class d extends r.WF{render(){const e=this.noCollapse?r.s6:r.qy`
          <ha-svg-icon
            .path=${"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"}
            class="summary-icon ${(0,n.H)({expanded:this.expanded})}"
          ></ha-svg-icon>
        `;return r.qy`
      <div class="top ${(0,n.H)({expanded:this.expanded})}">
        <div
          id="summary"
          class=${(0,n.H)({noCollapse:this.noCollapse})}
          @click=${this._toggleContainer}
          @keydown=${this._toggleContainer}
          @focus=${this._focusChanged}
          @blur=${this._focusChanged}
          role="button"
          tabindex=${this.noCollapse?-1:0}
          aria-expanded=${this.expanded}
          aria-controls="sect1"
          part="summary"
        >
          ${this.leftChevron?e:r.s6}
          <slot name="leading-icon"></slot>
          <slot name="header">
            <div class="header">
              ${this.header}
              <slot class="secondary" name="secondary">${this.secondary}</slot>
            </div>
          </slot>
          ${this.leftChevron?r.s6:e}
          <slot name="icons"></slot>
        </div>
      </div>
      <div
        class="container ${(0,n.H)({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?r.qy`<slot></slot>`:""}
      </div>
    `}willUpdate(e){super.willUpdate(e),e.has("expanded")&&(this._showContent=this.expanded,setTimeout(()=>{this._container.style.overflow=this.expanded?"initial":"hidden"},300))}_handleTransitionEnd(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}async _toggleContainer(e){if(e.defaultPrevented)return;if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;if(e.preventDefault(),this.noCollapse)return;const t=!this.expanded;(0,s.r)(this,"expanded-will-change",{expanded:t}),this._container.style.overflow="hidden",t&&(this._showContent=!0,await(0,l.E)());const o=this._container.scrollHeight;this._container.style.height=`${o}px`,t||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=t,(0,s.r)(this,"expanded-changed",{expanded:this.expanded})}_focusChanged(e){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===e.type)}constructor(...e){super(...e),this.expanded=!1,this.outlined=!1,this.leftChevron=!1,this.noCollapse=!1,this._showContent=this.expanded}}d.styles=r.AH`
    :host {
      display: block;
    }

    .top {
      display: flex;
      align-items: center;
      border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
    }

    .top.expanded {
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }

    .top.focused {
      background: var(--input-fill-color);
    }

    :host([outlined]) {
      box-shadow: none;
      border-width: 1px;
      border-style: solid;
      border-color: var(--outline-color);
      border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
    }

    .summary-icon {
      transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
      direction: var(--direction);
      margin-left: 8px;
      margin-inline-start: 8px;
      margin-inline-end: initial;
      border-radius: var(--ha-border-radius-circle);
    }

    #summary:focus-visible ha-svg-icon.summary-icon {
      background-color: var(--ha-color-fill-neutral-normal-active);
    }

    :host([left-chevron]) .summary-icon,
    ::slotted([slot="leading-icon"]) {
      margin-left: 0;
      margin-right: 8px;
      margin-inline-start: 0;
      margin-inline-end: 8px;
    }

    #summary {
      flex: 1;
      display: flex;
      padding: var(--expansion-panel-summary-padding, 0 8px);
      min-height: 48px;
      align-items: center;
      cursor: pointer;
      overflow: hidden;
      font-weight: var(--ha-font-weight-medium);
      outline: none;
    }
    #summary.noCollapse {
      cursor: default;
    }

    .summary-icon.expanded {
      transform: rotate(180deg);
    }

    .header,
    ::slotted([slot="header"]) {
      flex: 1;
      overflow-wrap: anywhere;
      color: var(--primary-text-color);
    }

    .container {
      padding: var(--expansion-panel-content-padding, 0 8px);
      overflow: hidden;
      transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
    }

    .container.expanded {
      height: auto;
    }

    .secondary {
      display: block;
      color: var(--secondary-text-color);
      font-size: var(--ha-font-size-s);
    }
  `,(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],d.prototype,"expanded",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,reflect:!0})],d.prototype,"outlined",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"left-chevron",type:Boolean,reflect:!0})],d.prototype,"leftChevron",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"no-collapse",type:Boolean,reflect:!0})],d.prototype,"noCollapse",void 0),(0,i.__decorate)([(0,a.MZ)()],d.prototype,"header",void 0),(0,i.__decorate)([(0,a.MZ)()],d.prototype,"secondary",void 0),(0,i.__decorate)([(0,a.wk)()],d.prototype,"_showContent",void 0),(0,i.__decorate)([(0,a.P)(".container")],d.prototype,"_container",void 0),d=(0,i.__decorate)([(0,a.EM)("ha-expansion-panel")],d)},63419:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845),n=o(92542),s=(o(41742),o(26139)),l=o(8889),d=o(63374);class c extends s.W1{connectedCallback(){super.connectedCallback(),this.addEventListener("close-menu",this._handleCloseMenu)}_handleCloseMenu(e){e.detail.reason.kind===d.fi.KEYDOWN&&e.detail.reason.key===d.NV.ESCAPE||e.detail.initiator.clickAction?.(e.detail.initiator)}}c.styles=[l.R,r.AH`
      :host {
        --md-sys-color-surface-container: var(--card-background-color);
      }
    `],c=(0,i.__decorate)([(0,a.EM)("ha-md-menu")],c);class u extends r.WF{get items(){return this._menu.items}focus(){this._menu.open?this._menu.focus():this._triggerButton?.focus()}render(){return r.qy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <ha-md-menu
        .quick=${this.quick}
        .positioning=${this.positioning}
        .hasOverflow=${this.hasOverflow}
        .anchorCorner=${this.anchorCorner}
        .menuCorner=${this.menuCorner}
        @opening=${this._handleOpening}
        @closing=${this._handleClosing}
      >
        <slot></slot>
      </ha-md-menu>
    `}_handleOpening(){(0,n.r)(this,"opening",void 0,{composed:!1})}_handleClosing(){(0,n.r)(this,"closing",void 0,{composed:!1})}_handleClick(){this.disabled||(this._menu.anchorElement=this,this._menu.open?this._menu.close():this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"], ha-assist-chip[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...e){super(...e),this.disabled=!1,this.anchorCorner="end-start",this.menuCorner="start-start",this.hasOverflow=!1,this.quick=!1}}u.styles=r.AH`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `,(0,i.__decorate)([(0,a.MZ)({type:Boolean})],u.prototype,"disabled",void 0),(0,i.__decorate)([(0,a.MZ)()],u.prototype,"positioning",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"anchor-corner"})],u.prototype,"anchorCorner",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"menu-corner"})],u.prototype,"menuCorner",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,attribute:"has-overflow"})],u.prototype,"hasOverflow",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],u.prototype,"quick",void 0),(0,i.__decorate)([(0,a.P)("ha-md-menu",!0)],u.prototype,"_menu",void 0),u=(0,i.__decorate)([(0,a.EM)("ha-md-button-menu")],u)},32072:function(e,t,o){var i=o(62826),r=o(10414),a=o(18989),n=o(96196),s=o(77845);class l extends r.c{}l.styles=[a.R,n.AH`
      :host {
        --md-divider-color: var(--divider-color);
      }
    `],l=(0,i.__decorate)([(0,s.EM)("ha-md-divider")],l)},99892:function(e,t,o){var i=o(62826),r=o(54407),a=o(28522),n=o(96196),s=o(77845);class l extends r.K{}l.styles=[a.R,n.AH`
      :host {
        --ha-icon-display: block;
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-primary: var(--primary-text-color);
        --md-sys-color-secondary: var(--secondary-text-color);
        --md-sys-color-surface: var(--card-background-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--secondary-text-color);
        --md-sys-color-secondary-container: rgba(
          var(--rgb-primary-color),
          0.15
        );
        --md-sys-color-on-secondary-container: var(--text-primary-color);
        --mdc-icon-size: 16px;

        --md-sys-color-on-primary-container: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-menu-item-label-text-font: Roboto, sans-serif;
      }
      :host(.warning) {
        --md-menu-item-label-text-color: var(--error-color);
        --md-menu-item-leading-icon-color: var(--error-color);
      }
      ::slotted([slot="headline"]) {
        text-wrap: nowrap;
      }
      :host([disabled]) {
        opacity: 1;
        --md-menu-item-label-text-color: var(--disabled-text-color);
        --md-menu-item-leading-icon-color: var(--disabled-text-color);
      }
    `],(0,i.__decorate)([(0,s.MZ)({attribute:!1})],l.prototype,"clickAction",void 0),l=(0,i.__decorate)([(0,s.EM)("ha-md-menu-item")],l)},63801:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845),n=o(92542);class s extends r.WF{updated(e){e.has("disabled")&&(this.disabled?this._destroySortable():this._createSortable())}disconnectedCallback(){super.disconnectedCallback(),this._shouldBeDestroy=!0,setTimeout(()=>{this._shouldBeDestroy&&(this._destroySortable(),this._shouldBeDestroy=!1)},1)}connectedCallback(){super.connectedCallback(),this._shouldBeDestroy=!1,this.hasUpdated&&!this.disabled&&this._createSortable()}createRenderRoot(){return this}render(){return this.noStyle?r.s6:r.qy`
      <style>
        .sortable-fallback {
          display: none !important;
        }

        .sortable-ghost {
          box-shadow: 0 0 0 2px var(--primary-color);
          background: rgba(var(--rgb-primary-color), 0.25);
          border-radius: var(--ha-border-radius-sm);
          opacity: 0.4;
        }

        .sortable-drag {
          border-radius: var(--ha-border-radius-sm);
          opacity: 1;
          background: var(--card-background-color);
          box-shadow: 0px 4px 8px 3px #00000026;
          cursor: grabbing;
        }
      </style>
    `}async _createSortable(){if(this._sortable)return;const e=this.children[0];if(!e)return;const t=(await Promise.all([o.e("5283"),o.e("1387")]).then(o.bind(o,38214))).default,i={scroll:!0,forceAutoScrollFallback:!0,scrollSpeed:20,animation:150,...this.options,onChoose:this._handleChoose,onStart:this._handleStart,onEnd:this._handleEnd,onUpdate:this._handleUpdate,onAdd:this._handleAdd,onRemove:this._handleRemove};this.draggableSelector&&(i.draggable=this.draggableSelector),this.handleSelector&&(i.handle=this.handleSelector),void 0!==this.invertSwap&&(i.invertSwap=this.invertSwap),this.group&&(i.group=this.group),this.filter&&(i.filter=this.filter),this._sortable=new t(e,i)}_destroySortable(){this._sortable&&(this._sortable.destroy(),this._sortable=void 0)}constructor(...e){super(...e),this.disabled=!1,this.noStyle=!1,this.invertSwap=!1,this.rollback=!0,this._shouldBeDestroy=!1,this._handleUpdate=e=>{(0,n.r)(this,"item-moved",{newIndex:e.newIndex,oldIndex:e.oldIndex})},this._handleAdd=e=>{(0,n.r)(this,"item-added",{index:e.newIndex,data:e.item.sortableData,item:e.item})},this._handleRemove=e=>{(0,n.r)(this,"item-removed",{index:e.oldIndex})},this._handleEnd=async e=>{(0,n.r)(this,"drag-end"),this.rollback&&e.item.placeholder&&(e.item.placeholder.replaceWith(e.item),delete e.item.placeholder)},this._handleStart=()=>{(0,n.r)(this,"drag-start")},this._handleChoose=e=>{this.rollback&&(e.item.placeholder=document.createComment("sort-placeholder"),e.item.after(e.item.placeholder))}}}(0,i.__decorate)([(0,a.MZ)({type:Boolean})],s.prototype,"disabled",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,attribute:"no-style"})],s.prototype,"noStyle",void 0),(0,i.__decorate)([(0,a.MZ)({type:String,attribute:"draggable-selector"})],s.prototype,"draggableSelector",void 0),(0,i.__decorate)([(0,a.MZ)({type:String,attribute:"handle-selector"})],s.prototype,"handleSelector",void 0),(0,i.__decorate)([(0,a.MZ)({type:String,attribute:"filter"})],s.prototype,"filter",void 0),(0,i.__decorate)([(0,a.MZ)({type:String})],s.prototype,"group",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean,attribute:"invert-swap"})],s.prototype,"invertSwap",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:!1})],s.prototype,"options",void 0),(0,i.__decorate)([(0,a.MZ)({type:Boolean})],s.prototype,"rollback",void 0),s=(0,i.__decorate)([(0,a.EM)("ha-sortable")],s)},67591:function(e,t,o){var i=o(62826),r=o(11896),a=o(92347),n=o(75057),s=o(96196),l=o(77845);class d extends r.u{updated(e){super.updated(e),this.autogrow&&e.has("value")&&(this.mdcRoot.dataset.value=this.value+'=​"')}constructor(...e){super(...e),this.autogrow=!1}}d.styles=[a.R,n.R,s.AH`
      :host([autogrow]) .mdc-text-field {
        position: relative;
        min-height: 74px;
        min-width: 178px;
        max-height: 200px;
      }
      :host([autogrow]) .mdc-text-field:after {
        content: attr(data-value);
        margin-top: 23px;
        margin-bottom: 9px;
        line-height: var(--ha-line-height-normal);
        min-height: 42px;
        padding: 0px 32px 0 16px;
        letter-spacing: var(
          --mdc-typography-subtitle1-letter-spacing,
          0.009375em
        );
        visibility: hidden;
        white-space: pre-wrap;
      }
      :host([autogrow]) .mdc-text-field__input {
        position: absolute;
        height: calc(100% - 32px);
      }
      :host([autogrow]) .mdc-text-field.mdc-text-field--no-label:after {
        margin-top: 16px;
        margin-bottom: 16px;
      }
      .mdc-floating-label {
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start) top;
      }
      @media only screen and (min-width: 459px) {
        :host([mobile-multiline]) .mdc-text-field__input {
          white-space: nowrap;
          max-height: 16px;
        }
      }
    `],(0,i.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],d.prototype,"autogrow",void 0),d=(0,i.__decorate)([(0,l.EM)("ha-textarea")],d)},80812:function(e,t,o){o.d(t,{Dp:()=>p,Dt:()=>s,G3:()=>h,Q:()=>n,S9:()=>m,VH:()=>a,XF:()=>l,aI:()=>c,fo:()=>u,vO:()=>d});var i=o(55376),r=(o(5871),o(9169),o(10038));o(29272);const a="__DYNAMIC__",n=e=>e?.startsWith(a),s=e=>e.substring(a.length),l=e=>{if("condition"in e&&Array.isArray(e.condition))return{condition:"and",conditions:e.condition};for(const t of r.I8)if(t in e)return{condition:t,conditions:e[t]};return e};const d=e=>e?Array.isArray(e)?e.map(d):("triggers"in e&&e.triggers&&(e.triggers=d(e.triggers)),"platform"in e&&("trigger"in e||(e.trigger=e.platform),delete e.platform),e):e,c=e=>{if(!e)return[];const t=[];return(0,i.e)(e).forEach(e=>{"triggers"in e?e.triggers&&t.push(...c(e.triggers)):t.push(e)}),t},u=e=>{if(!e||"object"!=typeof e)return!1;const t=e;return"trigger"in t&&"string"==typeof t.trigger||"platform"in t&&"string"==typeof t.platform},h=e=>{if(!e||"object"!=typeof e)return!1;return"condition"in e&&"string"==typeof e.condition},p=(e,t,o,i)=>e.connection.subscribeMessage(t,{type:"subscribe_trigger",trigger:o,variables:i}),m=(e,t,o)=>e.callWS({type:"test_condition",condition:t,variables:o})},53295:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{g:()=>w,p:()=>k});var r=o(55376),a=o(88738),n=o(4359),s=o(21754),l=o(48551),d=o(91889),c=o(45996),u=o(39680),h=o(72125),p=o(10038),m=o(74687),y=o(98995),f=e([n,a,l,u]);[n,a,l,u]=f.then?(await f)():f;const g="ui.panel.config.automation.editor.triggers.type",_="ui.panel.config.automation.editor.conditions.type",v=(e,t)=>{let o;return o="number"==typeof t?(0,s.A)(t):"string"==typeof t?t:(0,a.nR)(e,t),o},b=(e,t,o)=>{const i=e.split(":");if(i.length<2||i.length>3)return e;try{const r=new Date("1970-01-01T"+e);return 2===i.length||0===Number(i[2])?(0,n.fU)(r,t,o):(0,n.ie)(r,t,o)}catch{return e}},w=(e,t,o,i=!1)=>{try{const r=x(e,t,o,i);if("string"!=typeof r)throw new Error(String(r));return r}catch(r){console.error(r);let e="Error in describing trigger";return r.message&&(e+=": "+r.message),e}},x=(e,t,o,i=!1)=>{if((0,y.H4)(e)){const o=(0,r.e)(e.triggers);if(!o||0===o.length)return t.localize(`${g}.list.description.no_trigger`);const i=o.length;return t.localize(`${g}.list.description.full`,{count:i})}if(e.alias&&!i)return e.alias;const a=$(e,t,o);if(a)return a;const n=e.trigger,s=(0,y.zz)(e.trigger),l=(0,y.hN)(e.trigger);return t.localize(`component.${s}.triggers.${l}.name`)||t.localize(`ui.panel.config.automation.editor.triggers.type.${n}.label`)||t.localize("ui.panel.config.automation.editor.triggers.unknown_trigger")},$=(e,t,o)=>{if("event"===e.trigger&&e.event_type){const o=[];if(Array.isArray(e.event_type))for(const t of e.event_type.values())o.push(t);else o.push(e.event_type);const i=(0,u.q)(t.locale,o);return t.localize(`${g}.event.description.full`,{eventTypes:i})}if("homeassistant"===e.trigger&&e.event)return t.localize("start"===e.event?`${g}.homeassistant.description.started`:`${g}.homeassistant.description.shutdown`);if("numeric_state"===e.trigger&&e.entity_id){const o=[],i=t.states,r=Array.isArray(e.entity_id)?t.states[e.entity_id[0]]:t.states[e.entity_id];if(Array.isArray(e.entity_id))for(const t of e.entity_id.values())i[t]&&o.push((0,d.u)(i[t])||t);else e.entity_id&&o.push(i[e.entity_id]?(0,d.u)(i[e.entity_id]):e.entity_id);const a=e.attribute?r?(0,l.R)(t.localize,r,t.entities,e.attribute):e.attribute:void 0,n=e.for?v(t.locale,e.for):void 0;if(void 0!==e.above&&void 0!==e.below)return t.localize(`${g}.numeric_state.description.above-below`,{attribute:a,entity:(0,u.q)(t.locale,o),numberOfEntities:o.length,above:e.above,below:e.below,duration:n});if(void 0!==e.above)return t.localize(`${g}.numeric_state.description.above`,{attribute:a,entity:(0,u.q)(t.locale,o),numberOfEntities:o.length,above:e.above,duration:n});if(void 0!==e.below)return t.localize(`${g}.numeric_state.description.below`,{attribute:a,entity:(0,u.q)(t.locale,o),numberOfEntities:o.length,below:e.below,duration:n})}if("state"===e.trigger){const o=[],i=t.states;let a="";if(e.attribute){const o=Array.isArray(e.entity_id)?t.states[e.entity_id[0]]:t.states[e.entity_id];a=o?(0,l.R)(t.localize,o,t.entities,e.attribute):e.attribute}const n=(0,r.e)(e.entity_id);if(n)for(const e of n)i[e]&&o.push((0,d.u)(i[e])||e);const s=t.states[n[0]];let c="other",h="";if(void 0!==e.from){let o=[];if(null===e.from)e.attribute||(c="null");else{o=(0,r.e)(e.from);const i=[];for(const r of o)i.push(s?e.attribute?t.formatEntityAttributeValue(s,e.attribute,r).toString():t.formatEntityState(s,r):r);0!==i.length&&(h=(0,u.q)(t.locale,i),c="fromUsed")}}let p="other",m="";if(void 0!==e.to){let o=[];if(null===e.to)e.attribute||(p="null");else{o=(0,r.e)(e.to);const i=[];for(const r of o)i.push(s?e.attribute?t.formatEntityAttributeValue(s,e.attribute,r).toString():t.formatEntityState(s,r).toString():r);0!==i.length&&(m=(0,u.q)(t.locale,i),p="toUsed")}}e.attribute||void 0!==e.from||void 0!==e.to||(p="special");let y="";return e.for&&(y=v(t.locale,e.for)??""),t.localize(`${g}.state.description.full`,{hasAttribute:""!==a?"true":"false",attribute:a,hasEntity:0!==o.length?"true":"false",entity:(0,u.q)(t.locale,o),fromChoice:c,fromString:h,toChoice:p,toString:m,hasDuration:""!==y?"true":"false",duration:y})}if("sun"===e.trigger&&e.event){let o="";return e.offset&&(o="number"==typeof e.offset?(0,s.A)(e.offset):"string"==typeof e.offset?e.offset:JSON.stringify(e.offset)),t.localize("sunset"===e.event?`${g}.sun.description.sets`:`${g}.sun.description.rises`,{hasDuration:""!==o?"true":"false",duration:o})}if("tag"===e.trigger){const o=Object.values(t.states).find(t=>t.entity_id.startsWith("tag.")&&t.attributes.tag_id===e.tag_id);return o?t.localize(`${g}.tag.description.known_tag`,{tag_name:(0,d.u)(o)}):t.localize(`${g}.tag.description.full`)}if("time"===e.trigger&&e.at){const o=(0,r.e)(e.at).map(e=>{if("string"==typeof e)return(0,c.n)(e)?`entity ${t.states[e]?(0,d.u)(t.states[e]):e}`:b(e,t.locale,t.config);return`${`entity ${t.states[e.entity_id]?(0,d.u)(t.states[e.entity_id]):e.entity_id}`}${e.offset?" "+t.localize(`${g}.time.offset_by`,{offset:v(t.locale,e.offset)}):""}`});let i=[];if(e.weekday){const o=(0,r.e)(e.weekday);o.length>0&&(i=o.map(e=>t.localize(`ui.panel.config.automation.editor.triggers.type.time.weekdays.${e}`)))}return t.localize(`${g}.time.description.full`,{time:(0,u.q)(t.locale,o),hasWeekdays:i.length>0?"true":"false",weekdays:(0,u.q)(t.locale,i)})}if("time_pattern"===e.trigger){if(!e.seconds&&!e.minutes&&!e.hours)return t.localize(`${g}.time_pattern.description.initial`);const o=[];let i="other",r="other",a="other",n=0,s=0,l=0;if(void 0!==e.seconds){const t="*"===e.seconds,r="string"==typeof e.seconds&&e.seconds.startsWith("/");n=t?0:"number"==typeof e.seconds?e.seconds:r?parseInt(e.seconds.substring(1)):parseInt(e.seconds),(isNaN(n)||n>59||n<0||r&&0===n)&&o.push("seconds"),i=t||r&&1===n?"every":r?"every_interval":"on_the_xth"}if(void 0!==e.minutes){const t="*"===e.minutes,i="string"==typeof e.minutes&&e.minutes.startsWith("/");s=t?0:"number"==typeof e.minutes?e.minutes:i?parseInt(e.minutes.substring(1)):parseInt(e.minutes),(isNaN(s)||s>59||s<0||i&&0===s)&&o.push("minutes"),r=t||i&&1===s?"every":i?"every_interval":void 0!==e.seconds?"has_seconds":"on_the_xth"}else void 0!==e.seconds&&(void 0!==e.hours?(s=0,r="has_seconds"):r="every");if(void 0!==e.hours){const t="*"===e.hours,i="string"==typeof e.hours&&e.hours.startsWith("/");l=t?0:"number"==typeof e.hours?e.hours:i?parseInt(e.hours.substring(1)):parseInt(e.hours),(isNaN(l)||l>23||l<0||i&&0===l)&&o.push("hours"),a=t||i&&1===l?"every":i?"every_interval":void 0!==e.seconds||void 0!==e.minutes?"has_seconds_or_minutes":"on_the_xth"}else a="every";return 0!==o.length?t.localize(`${g}.time_pattern.description.invalid`,{parts:(0,u.c)(t.locale,o.map(e=>t.localize(`${g}.time_pattern.${e}`)))}):t.localize(`${g}.time_pattern.description.full`,{secondsChoice:i,minutesChoice:r,hoursChoice:a,seconds:n,minutes:s,hours:l,secondsWithOrdinal:t.localize(`${g}.time_pattern.description.ordinal`,{part:n}),minutesWithOrdinal:t.localize(`${g}.time_pattern.description.ordinal`,{part:s}),hoursWithOrdinal:t.localize(`${g}.time_pattern.description.ordinal`,{part:l})})}if("zone"===e.trigger&&e.entity_id&&e.zone){const o=[],i=[],r=t.states;if(Array.isArray(e.entity_id))for(const t of e.entity_id.values())r[t]&&o.push((0,d.u)(r[t])||t);else o.push(r[e.entity_id]?(0,d.u)(r[e.entity_id]):e.entity_id);if(Array.isArray(e.zone))for(const t of e.zone.values())r[t]&&i.push((0,d.u)(r[t])||t);else i.push(r[e.zone]?(0,d.u)(r[e.zone]):e.zone);return t.localize(`${g}.zone.description.full`,{entity:(0,u.q)(t.locale,o),event:e.event.toString(),zone:(0,u.q)(t.locale,i),numberOfZones:i.length})}if("geo_location"===e.trigger&&e.source&&e.zone){const o=[],i=[],r=t.states;if(Array.isArray(e.source))for(const t of e.source.values())o.push(t);else o.push(e.source);if(Array.isArray(e.zone))for(const t of e.zone.values())r[t]&&i.push((0,d.u)(r[t])||t);else i.push(r[e.zone]?(0,d.u)(r[e.zone]):e.zone);return t.localize(`${g}.geo_location.description.full`,{source:(0,u.q)(t.locale,o),event:e.event.toString(),zone:(0,u.q)(t.locale,i),numberOfZones:i.length})}if("mqtt"===e.trigger)return t.localize(`${g}.mqtt.description.full`);if("template"===e.trigger){let o="";return e.for&&(o=v(t.locale,e.for)??""),t.localize(`${g}.template.description.full`,{hasDuration:""!==o?"true":"false",duration:o})}if("webhook"===e.trigger)return t.localize(`${g}.webhook.description.full`);if("conversation"===e.trigger){if(!e.command||!e.command.length)return t.localize(`${g}.conversation.description.empty`);const o=(0,r.e)(e.command);return 1===o.length?t.localize(`${g}.conversation.description.single`,{sentence:o[0]}):t.localize(`${g}.conversation.description.multiple`,{sentence:o[0],count:o.length-1})}if("persistent_notification"===e.trigger)return t.localize(`${g}.persistent_notification.description.full`);if("device"===e.trigger&&e.device_id){const i=e,r=(0,m.nx)(t,o,i);if(r)return r;const a=t.states[i.entity_id];return`${a?(0,d.u)(a):i.entity_id} ${i.type}`}if("calendar"===e.trigger){const o=t.states[e.entity_id]?(0,d.u)(t.states[e.entity_id]):e.entity_id;let i="other",r="";if(e.offset){i=e.offset.startsWith("-")?"before":"after",r=e.offset.startsWith("-")?e.offset.substring(1).split(":"):e.offset.split(":");const o={hours:r.length>0?+r[0]:0,minutes:r.length>1?+r[1]:0,seconds:r.length>2?+r[2]:0};r=(0,a.i)(t.locale,o),""===r&&(i="other")}return t.localize(`${g}.calendar.description.full`,{eventChoice:e.event,offsetChoice:i,offset:r,hasCalendar:e.entity_id?"true":"false",calendar:o})}},k=(e,t,o,i=!1)=>{try{const r=z(e,t,o,i);if("string"!=typeof r)throw new Error(String(r));return r}catch(r){console.error(r);let e="Error in describing condition";return r.message&&(e+=": "+r.message),e}},z=(e,t,o,i=!1)=>{if("string"==typeof e&&(0,h.r)(e))return t.localize(`${_}.template.description.full`);if(e.alias&&!i)return e.alias;if(!e.condition){const t=["and","or","not"];for(const o of t)o in e&&(0,r.e)(e[o])&&(e={condition:o,conditions:e[o]})}const a=A(e,t,o);if(a)return a;const n=e.condition,s=(0,p.ob)(e.condition),l=(0,p.YQ)(e.condition);return t.localize(`component.${s}.conditions.${l}.name`)||t.localize(`ui.panel.config.automation.editor.conditions.type.${n}.label`)||t.localize("ui.panel.config.automation.editor.conditions.unknown_condition")},A=(e,t,o)=>{if("or"===e.condition){const o=(0,r.e)(e.conditions);if(!o||0===o.length)return t.localize(`${_}.or.description.no_conditions`);const i=o.length;return t.localize(`${_}.or.description.full`,{count:i})}if("and"===e.condition){const o=(0,r.e)(e.conditions);if(!o||0===o.length)return t.localize(`${_}.and.description.no_conditions`);const i=o.length;return t.localize(`${_}.and.description.full`,{count:i})}if("not"===e.condition){const o=(0,r.e)(e.conditions);return o&&0!==o.length?1===o.length?t.localize(`${_}.not.description.one_condition`):t.localize(`${_}.not.description.full`,{count:o.length}):t.localize(`${_}.not.description.no_conditions`)}if("state"===e.condition){if(!e.entity_id)return t.localize(`${_}.state.description.no_entity`);let o="";if(e.attribute){const i=Array.isArray(e.entity_id)?t.states[e.entity_id[0]]:t.states[e.entity_id];o=i?(0,l.R)(t.localize,i,t.entities,e.attribute):e.attribute}const i=[];if(Array.isArray(e.entity_id))for(const s of e.entity_id.values())t.states[s]&&i.push((0,d.u)(t.states[s])||s);else e.entity_id&&i.push(t.states[e.entity_id]?(0,d.u)(t.states[e.entity_id]):e.entity_id);const r=[],a=t.states[Array.isArray(e.entity_id)?e.entity_id[0]:e.entity_id];if(Array.isArray(e.state))for(const s of e.state.values())r.push(a?e.attribute?t.formatEntityAttributeValue(a,e.attribute,s).toString():t.formatEntityState(a,s):s);else""!==e.state&&r.push(a?e.attribute?t.formatEntityAttributeValue(a,e.attribute,e.state).toString():t.formatEntityState(a,e.state.toString()):e.state.toString());let n="";return e.for&&(n=v(t.locale,e.for)||""),t.localize(`${_}.state.description.full`,{hasAttribute:""!==o?"true":"false",attribute:o,numberOfEntities:i.length,entities:"any"===e.match?(0,u.q)(t.locale,i):(0,u.c)(t.locale,i),numberOfStates:r.length,states:(0,u.q)(t.locale,r),hasDuration:""!==n?"true":"false",duration:n})}if("numeric_state"===e.condition&&e.entity_id){const o=(0,r.e)(e.entity_id),i=t.states[o[0]],a=(0,u.c)(t.locale,o.map(e=>t.states[e]?(0,d.u)(t.states[e]):e||"")),n=e.attribute?i?(0,l.R)(t.localize,i,t.entities,e.attribute):e.attribute:void 0;if(void 0!==e.above&&void 0!==e.below)return t.localize(`${_}.numeric_state.description.above-below`,{attribute:n,entity:a,numberOfEntities:o.length,above:e.above,below:e.below});if(void 0!==e.above)return t.localize(`${_}.numeric_state.description.above`,{attribute:n,entity:a,numberOfEntities:o.length,above:e.above});if(void 0!==e.below)return t.localize(`${_}.numeric_state.description.below`,{attribute:n,entity:a,numberOfEntities:o.length,below:e.below})}if("time"===e.condition){const o=(0,r.e)(e.weekday),i=o&&o.length>0&&o.length<7;if(e.before||e.after||i){const r="string"!=typeof e.before?e.before:e.before.includes(".")?`entity ${t.states[e.before]?(0,d.u)(t.states[e.before]):e.before}`:b(e.before,t.locale,t.config),a="string"!=typeof e.after?e.after:e.after.includes(".")?`entity ${t.states[e.after]?(0,d.u)(t.states[e.after]):e.after}`:b(e.after,t.locale,t.config);let n=[];i&&(n=o.map(e=>t.localize(`ui.panel.config.automation.editor.conditions.type.time.weekdays.${e}`)));let s="";return void 0!==a&&void 0!==r?s="after_before":void 0!==a?s="after":void 0!==r&&(s="before"),t.localize(`${_}.time.description.full`,{hasTime:s,hasTimeAndDay:(a||r)&&i?"true":"false",hasDay:i?"true":"false",time_before:r,time_after:a,day:(0,u.q)(t.locale,n)})}}if("sun"===e.condition&&(e.before||e.after)){let o="";e.after&&e.after_offset&&(o="number"==typeof e.after_offset?(0,s.A)(e.after_offset):"string"==typeof e.after_offset?e.after_offset:JSON.stringify(e.after_offset));let i="";return e.before&&e.before_offset&&(i="number"==typeof e.before_offset?(0,s.A)(e.before_offset):"string"==typeof e.before_offset?e.before_offset:JSON.stringify(e.before_offset)),t.localize(`${_}.sun.description.full`,{afterChoice:e.after??"other",afterOffsetChoice:""!==o?"offset":"other",afterOffset:o,beforeChoice:e.before??"other",beforeOffsetChoice:""!==i?"offset":"other",beforeOffset:i})}if("zone"===e.condition&&e.entity_id&&e.zone){const o=[],i=[],r=t.states;if(Array.isArray(e.entity_id))for(const t of e.entity_id.values())r[t]&&o.push((0,d.u)(r[t])||t);else o.push(r[e.entity_id]?(0,d.u)(r[e.entity_id]):e.entity_id);if(Array.isArray(e.zone))for(const t of e.zone.values())r[t]&&i.push((0,d.u)(r[t])||t);else i.push(r[e.zone]?(0,d.u)(r[e.zone]):e.zone);const a=(0,u.q)(t.locale,o),n=(0,u.q)(t.locale,i);return t.localize(`${_}.zone.description.full`,{entity:a,numberOfEntities:o.length,zone:n,numberOfZones:i.length})}if("device"===e.condition&&e.device_id){const i=e,r=(0,m.I3)(t,o,i);if(r)return r;const a=t.states[i.entity_id];return`${a?(0,d.u)(a):i.entity_id} ${i.type}`}return"template"===e.condition?t.localize(`${_}.template.description.full`):"trigger"===e.condition&&null!=e.id?t.localize(`${_}.trigger.description.full`,{id:(0,u.q)(t.locale,(0,r.e)(e.id).map(e=>e.toString()))}):void 0};i()}catch(g){i(g)}})},34485:function(e,t,o){o.d(t,{$:()=>i});const i=(e,t)=>e.callWS({type:"validate_config",...t})},34972:function(e,t,o){o.d(t,{$F:()=>l,HD:()=>u,X1:()=>a,iN:()=>r,ih:()=>d,rf:()=>c,wn:()=>s,xJ:()=>n});var i=o(16527);(0,i.q6)("connection");const r=(0,i.q6)("states"),a=(0,i.q6)("entities"),n=(0,i.q6)("devices"),s=(0,i.q6)("areas"),l=(0,i.q6)("localize"),d=((0,i.q6)("locale"),(0,i.q6)("config"),(0,i.q6)("themes"),(0,i.q6)("selectedTheme"),(0,i.q6)("user"),(0,i.q6)("userData"),(0,i.q6)("panels"),(0,i.q6)("extendedEntities")),c=(0,i.q6)("floors"),u=(0,i.q6)("labels")},74687:function(e,t,o){o.d(t,{I$:()=>c,I3:()=>g,PV:()=>f,Po:()=>p,RK:()=>w,TB:()=>u,TH:()=>b,T_:()=>v,am:()=>n,jR:()=>d,ng:()=>s,nx:()=>_,o9:()=>l});var i=o(91889),r=o(80812),a=o(22800);const n=(e,t)=>e.callWS({type:"device_automation/action/list",device_id:t}),s=(e,t)=>e.callWS({type:"device_automation/condition/list",device_id:t}),l=(e,t)=>e.callWS({type:"device_automation/trigger/list",device_id:t}).then(e=>(0,r.vO)(e)),d=(e,t)=>e.callWS({type:"device_automation/action/capabilities",action:t}),c=(e,t)=>e.callWS({type:"device_automation/condition/capabilities",condition:t}),u=(e,t)=>e.callWS({type:"device_automation/trigger/capabilities",trigger:t}),h=["device_id","domain","entity_id","type","subtype","event","condition","trigger"],p=(e,t,o)=>{if(typeof t!=typeof o)return!1;for(const i in t)if(h.includes(i))if("entity_id"!==i||t[i]?.includes(".")===o[i]?.includes(".")){if(!Object.is(t[i],o[i]))return!1}else if(!m(e,t[i],o[i]))return!1;for(const i in o)if(h.includes(i))if("entity_id"!==i||t[i]?.includes(".")===o[i]?.includes(".")){if(!Object.is(t[i],o[i]))return!1}else if(!m(e,t[i],o[i]))return!1;return!0},m=(e,t,o)=>{if(!t||!o)return!1;if(t.includes(".")){const o=(0,a.Ox)(e)[t];if(!o)return!1;t=o.id}if(o.includes(".")){const t=(0,a.Ox)(e)[o];if(!t)return!1;o=t.id}return t===o},y=(e,t,o)=>{if(!o)return"<"+e.localize("ui.panel.config.automation.editor.unknown_entity")+">";if(o.includes(".")){const t=e.states[o];return t?(0,i.u)(t):o}const r=(0,a.P9)(t)[o];return r?(0,a.jh)(e,r)||o:"<"+e.localize("ui.panel.config.automation.editor.unknown_entity")+">"},f=(e,t,o)=>e.localize(`component.${o.domain}.device_automation.action_type.${o.type}`,{entity_name:y(e,t,o.entity_id),subtype:o.subtype?e.localize(`component.${o.domain}.device_automation.action_subtype.${o.subtype}`)||o.subtype:""})||(o.subtype?`"${o.subtype}" ${o.type}`:o.type),g=(e,t,o)=>e.localize(`component.${o.domain}.device_automation.condition_type.${o.type}`,{entity_name:y(e,t,o.entity_id),subtype:o.subtype?e.localize(`component.${o.domain}.device_automation.condition_subtype.${o.subtype}`)||o.subtype:""})||(o.subtype?`"${o.subtype}" ${o.type}`:o.type),_=(e,t,o)=>e.localize(`component.${o.domain}.device_automation.trigger_type.${o.type}`,{entity_name:y(e,t,o.entity_id),subtype:o.subtype?e.localize(`component.${o.domain}.device_automation.trigger_subtype.${o.subtype}`)||o.subtype:""})||(o.subtype?`"${o.subtype}" ${o.type}`:o.type),v=(e,t)=>o=>e.localize(`component.${t.domain}.device_automation.extra_fields.${o.name}`)||o.name,b=(e,t)=>o=>e.localize(`component.${t.domain}.device_automation.extra_fields_descriptions.${o.name}`),w=(e,t)=>e.metadata?.secondary&&!t.metadata?.secondary?1:!e.metadata?.secondary&&t.metadata?.secondary?-1:0},2654:function(e,t,o){o.a(e,async function(e,i){try{o.d(t,{We:()=>s,rM:()=>n});var r=o(88738),a=e([r]);r=(a.then?(await a)():a)[0];new Set(["temperature","current_temperature","target_temperature","target_temp_temp","target_temp_high","target_temp_low","target_temp_step","min_temp","max_temp"]);const n={climate:{humidity:"%",current_humidity:"%",target_humidity_low:"%",target_humidity_high:"%",target_humidity_step:"%",min_humidity:"%",max_humidity:"%"},cover:{current_position:"%",current_tilt_position:"%"},fan:{percentage:"%"},humidifier:{humidity:"%",current_humidity:"%",min_humidity:"%",max_humidity:"%"},light:{color_temp:"mired",max_mireds:"mired",min_mireds:"mired",color_temp_kelvin:"K",min_color_temp_kelvin:"K",max_color_temp_kelvin:"K",brightness:"%"},sun:{azimuth:"°",elevation:"°"},vacuum:{battery_level:"%"},valve:{current_position:"%"},sensor:{battery_level:"%"},media_player:{volume_level:"%"}},s=["access_token","auto_update","available_modes","away_mode","changed_by","code_format","color_modes","current_activity","device_class","editable","effect_list","effect","entity_picture","event_type","event_types","fan_mode","fan_modes","fan_speed_list","forecast","friendly_name","frontend_stream_type","has_date","has_time","hs_color","hvac_mode","hvac_modes","icon","media_album_name","media_artist","media_content_type","media_position_updated_at","media_title","next_dawn","next_dusk","next_midnight","next_noon","next_rising","next_setting","operation_list","operation_mode","options","preset_mode","preset_modes","release_notes","release_summary","release_url","restored","rgb_color","rgbw_color","shuffle","sound_mode_list","sound_mode","source_list","source_type","source","state_class","supported_features","swing_mode","swing_mode","swing_modes","title","token","unit_of_measurement","xy_color"];i()}catch(n){i(n)}})},78991:function(e,t,o){o.d(t,{CO:()=>i});const i=(e,t,o,i)=>e.subscribeMessage(i,{type:"labs/subscribe",domain:t,preview_feature:o})},29272:function(e,t,o){o.d(t,{BD:()=>d,Rn:()=>h,pq:()=>c,ve:()=>u});var i=o(63533),r=o(99245),a=(o(5871),o(72125)),n=(o(9169),o(80812));(0,r.g)(["queued","parallel"]);const s=(0,i.Ik)({alias:(0,i.lq)((0,i.Yj)()),continue_on_error:(0,i.lq)((0,i.zM)()),enabled:(0,i.lq)((0,i.zM)())}),l=(0,i.Ik)({entity_id:(0,i.lq)((0,i.KC)([(0,i.Yj)(),(0,i.YO)((0,i.Yj)())])),device_id:(0,i.lq)((0,i.KC)([(0,i.Yj)(),(0,i.YO)((0,i.Yj)())])),area_id:(0,i.lq)((0,i.KC)([(0,i.Yj)(),(0,i.YO)((0,i.Yj)())])),floor_id:(0,i.lq)((0,i.KC)([(0,i.Yj)(),(0,i.YO)((0,i.Yj)())])),label_id:(0,i.lq)((0,i.KC)([(0,i.Yj)(),(0,i.YO)((0,i.Yj)())]))}),d=(0,i.kp)(s,(0,i.Ik)({action:(0,i.lq)((0,i.Yj)()),service_template:(0,i.lq)((0,i.Yj)()),entity_id:(0,i.lq)((0,i.Yj)()),target:(0,i.lq)((0,i.KC)([l,(0,i.YP)((0,i.Yj)(),"has_template",e=>(0,a.r)(e))])),data:(0,i.lq)((0,i.Ik)()),response_variable:(0,i.lq)((0,i.Yj)()),metadata:(0,i.lq)((0,i.Ik)())}));const c=e=>"string"==typeof e&&(0,a.r)(e)?"check_condition":"delay"in e?"delay":"wait_template"in e?"wait_template":["condition","and","or","not"].some(t=>t in e)?"check_condition":"event"in e?"fire_event":!("device_id"in e)||"trigger"in e||"condition"in e?"repeat"in e?"repeat":"choose"in e?"choose":"if"in e?"if":"wait_for_trigger"in e?"wait_for_trigger":"variables"in e?"variables":"stop"in e?"stop":"sequence"in e?"sequence":"parallel"in e?"parallel":"set_conversation_response"in e?"set_conversation_response":"action"in e||"service"in e?"service":"unknown":"device_action",u=e=>"unknown"!==c(e),h=e=>{if(!e)return e;if(Array.isArray(e))return e.map(h);if("object"==typeof e&&null!==e&&"service"in e&&("action"in e||(e.action=e.service),delete e.service),"object"==typeof e&&null!==e&&"scene"in e&&(e.action="scene.turn_on",e.target={entity_id:e.scene},delete e.scene),"object"==typeof e&&null!==e&&"action"in e&&"media_player.play_media"===e.action&&"data"in e&&(e.data?.media_content_id||e.data?.media_content_type)){const t={...e.data},o={media_content_id:t.media_content_id,media_content_type:t.media_content_type,metadata:{...e.metadata||{}}};delete e.metadata,delete t.media_content_id,delete t.media_content_type,e.data={...t,media:o}}if("object"==typeof e&&null!==e&&"sequence"in e){delete e.metadata;for(const t of e.sequence)h(t)}const t=c(e);if("parallel"===t){h(e.parallel)}if("choose"===t){const t=e;if(Array.isArray(t.choose))for(const e of t.choose)h(e.sequence);else t.choose&&h(t.choose.sequence);t.default&&h(t.default)}if("repeat"===t){h(e.repeat.sequence)}if("if"===t){const t=e;h(t.then),t.else&&h(t.else)}if("wait_for_trigger"===t){const t=e;(0,n.vO)(t.wait_for_trigger)}return e}},34099:function(e,t,o){var i=o(96196);o(29485),o(60961);new Set(["clear-night","cloudy","fog","lightning","lightning-rainy","partlycloudy","pouring","rainy","hail","snowy","snowy-rainy","sunny","windy","windy-variant"]),new Set(["partlycloudy","cloudy","fog","windy","windy-variant","hail","rainy","snowy","snowy-rainy","pouring","lightning","lightning-rainy"]),new Set(["hail","rainy","pouring","lightning-rainy"]),new Set(["windy","windy-variant"]),new Set(["snowy","snowy-rainy"]),new Set(["lightning","lightning-rainy"]),i.AH`
  .rain {
    fill: var(--weather-icon-rain-color, #30b3ff);
  }
  .sun {
    fill: var(--weather-icon-sun-color, #fdd93c);
  }
  .moon {
    fill: var(--weather-icon-moon-color, #fcf497);
  }
  .cloud-back {
    fill: var(--weather-icon-cloud-back-color, #d4d4d4);
  }
  .cloud-front {
    fill: var(--weather-icon-cloud-front-color, #f9f9f9);
  }
  .snow {
    fill: var(--weather-icon-snow-color, #f9f9f9);
    stroke: var(--weather-icon-snow-stroke-color, #d4d4d4);
    stroke-width: 1;
    paint-order: stroke;
  }
`},10085:function(e,t,o){o.d(t,{E:()=>a});var i=o(62826),r=o(77845);const a=e=>{class t extends e{connectedCallback(){super.connectedCallback(),this._checkSubscribed()}disconnectedCallback(){if(super.disconnectedCallback(),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then(e=>e()):e()}this.__unsubs=void 0}}updated(e){if(super.updated(e),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this._checkSubscribed()}hassSubscribe(){return[]}_checkSubscribed(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some(e=>void 0===this[e])&&(this.__unsubs=this.hassSubscribe())}}return(0,i.__decorate)([(0,r.MZ)({attribute:!1})],t.prototype,"hass",void 0),t}},13295:function(e,t,o){var i=o(62826),r=o(96196),a=o(77845);o(17963);class n extends r.WF{render(){return r.qy`
      <ha-alert
        alert-type="warning"
        .title=${this.alertTitle||this.localize("ui.errors.config.editor_not_supported")}
      >
        ${this.warnings.length&&void 0!==this.warnings[0]?r.qy`<ul>
              ${this.warnings.map(e=>r.qy`<li>${e}</li>`)}
            </ul>`:r.s6}
        ${this.localize("ui.errors.config.edit_in_yaml_supported")}
      </ha-alert>
    `}constructor(...e){super(...e),this.warnings=[]}}(0,i.__decorate)([(0,a.MZ)({attribute:!1})],n.prototype,"localize",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:"alert-title"})],n.prototype,"alertTitle",void 0),(0,i.__decorate)([(0,a.MZ)({attribute:!1})],n.prototype,"warnings",void 0),n=(0,i.__decorate)([(0,a.EM)("ha-automation-editor-warning")],n)},78232:function(e,t,o){o.d(t,{g:()=>n,u:()=>r});var i=o(92542);const r="__paste__",a=()=>Promise.all([o.e("7940"),o.e("7360"),o.e("9341")]).then(o.bind(o,53468)),n=(e,t)=>{(0,i.r)(e,"show-dialog",{dialogTag:"add-automation-element-dialog",dialogImport:a,dialogParams:t})}},20897:function(e,t,o){o.d(t,{V:()=>r,b:()=>a});var i=o(63533);const r=(0,i.Ik)({trigger:(0,i.Yj)(),id:(0,i.lq)((0,i.Yj)()),enabled:(0,i.lq)((0,i.zM)())}),a=(0,i.Ik)({days:(0,i.lq)((0,i.ai)()),hours:(0,i.lq)((0,i.ai)()),minutes:(0,i.lq)((0,i.ai)()),seconds:(0,i.lq)((0,i.ai)())})},36857:function(e,t,o){o.d(t,{Ju:()=>s,Lt:()=>l,aM:()=>n,bH:()=>r,yj:()=>a});var i=o(96196);const r=i.AH`
  ha-icon-button {
    --mdc-theme-text-primary-on-background: var(--primary-text-color);
  }
  ha-expansion-panel {
    --expansion-panel-summary-padding: 0 0 0 8px;
    --expansion-panel-content-padding: 0;
  }
  h3 {
    font-size: inherit;
    font-weight: inherit;
  }

  ha-card {
    transition: outline 0.2s;
  }
  .disabled-bar {
    background: var(--divider-color, #e0e0e0);
    text-align: center;
    border-top-right-radius: var(
      --ha-card-border-radius,
      var(--ha-border-radius-lg)
    );
    border-top-left-radius: var(
      --ha-card-border-radius,
      var(--ha-border-radius-lg)
    );
  }
  .warning ul {
    margin: 4px 0;
  }
  ha-md-menu-item > ha-svg-icon {
    --mdc-icon-size: 24px;
  }
  ha-tooltip {
    cursor: default;
  }
  .hidden {
    display: none;
  }
`,a=i.AH`
  .disabled {
    pointer-events: none;
  }

  .card-content.card {
    padding: 16px;
  }
  .card-content.yaml {
    padding: 0 1px;
    border-top: 1px solid var(--divider-color);
    border-bottom: 1px solid var(--divider-color);
  }
`,n=i.AH`
  .card-content.indent,
  .selector-row,
  :host([indent]) ha-form {
    margin-inline-start: 12px;
    padding-top: 12px;
    padding-bottom: 16px;
    padding-inline-start: 16px;
    padding-inline-end: 0px;
    border-inline-start: 2px solid var(--ha-color-border-neutral-quiet);
    border-bottom: 2px solid var(--ha-color-border-neutral-quiet);
    border-radius: var(--ha-border-radius-square);
    border-end-start-radius: var(--ha-border-radius-lg);
  }
  .card-content.indent.selected,
  :host([selected]) .card-content.indent,
  .selector-row.parent-selected,
  :host([selected]) ha-form {
    border-color: var(--primary-color);
    background: var(--ha-color-fill-primary-quiet-resting);
    background: linear-gradient(
      to right,
      var(--ha-color-fill-primary-quiet-resting) 0%,
      var(--ha-color-fill-primary-quiet-resting) 80%,
      rgba(var(--rgb-primary-color), 0) 100%
    );
  }
`,s=(i.AH`
  :host {
    overflow: hidden;
  }
  ha-fab {
    position: absolute;
    right: calc(16px + var(--safe-area-inset-right, 0px));
    bottom: calc(-80px - var(--safe-area-inset-bottom));
    transition: bottom 0.3s;
  }
  ha-fab.dirty {
    bottom: calc(16px + var(--safe-area-inset-bottom, 0px));
  }
`,i.AH`
  :host {
    display: block;
    --sidebar-width: 0;
    --sidebar-gap: 0;
  }

  .has-sidebar {
    --sidebar-width: min(
      max(var(--sidebar-dynamic-width), ${375}px),
      100vw - ${350}px - var(--mdc-drawer-width, 0px),
      var(--ha-automation-editor-max-width) -
        ${350}px - var(--mdc-drawer-width, 0px)
    );
    --sidebar-gap: var(--ha-space-4);
  }

  .fab-positioner {
    display: flex;
    justify-content: flex-end;
  }

  .fab-positioner ha-fab {
    position: fixed;
    right: unset;
    left: unset;
    bottom: calc(-80px - var(--safe-area-inset-bottom));
    transition: bottom 0.3s;
  }
  .fab-positioner ha-fab.dirty {
    bottom: calc(16px + var(--safe-area-inset-bottom, 0px));
  }

  .content-wrapper {
    padding-right: calc(var(--sidebar-width) + var(--sidebar-gap));
    padding-inline-end: calc(var(--sidebar-width) + var(--sidebar-gap));
    padding-inline-start: 0;
  }

  .content {
    padding-top: 24px;
    padding-bottom: max(var(--safe-area-inset-bottom), 32px);
    transition: padding-bottom 180ms ease-in-out;
  }

  .content.has-bottom-sheet {
    padding-bottom: calc(90vh - max(var(--safe-area-inset-bottom), 32px));
  }

  ha-automation-sidebar {
    position: fixed;
    top: calc(var(--header-height) + 16px);
    height: calc(-81px + 100vh - var(--safe-area-inset-top, 0px));
    height: calc(-81px + 100dvh - var(--safe-area-inset-top, 0px));
    width: var(--sidebar-width);
    display: block;
  }

  ha-automation-sidebar.hidden {
    display: none;
  }

  .sidebar-positioner {
    display: flex;
    justify-content: flex-end;
  }

  .description {
    margin: 0;
  }
  .header a {
    color: var(--secondary-text-color);
  }
`,i.AH`
  .rows {
    display: flex;
    flex-direction: column;
    gap: var(--ha-space-4);
  }
  .rows.no-sidebar {
    margin-inline-end: 0;
  }
  .sortable-ghost {
    background: none;
    border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
  }
  .sortable-drag {
    background: none;
  }
  ha-automation-action-row {
    display: block;
    scroll-margin-top: 48px;
  }
  .handle {
    padding: 4px;
    cursor: move; /* fallback if grab cursor is unsupported */
    cursor: grab;
    border-radius: var(--ha-border-radius-pill);
  }
  .handle:focus {
    outline: var(--wa-focus-ring);
    background: var(--ha-color-fill-neutral-quiet-resting);
  }
  .handle.active {
    outline: var(--wa-focus-ring);
    background: var(--ha-color-fill-neutral-normal-active);
  }
  .handle ha-svg-icon {
    pointer-events: none;
    height: 24px;
  }
  .buttons {
    display: flex;
    flex-wrap: wrap;
    gap: var(--ha-space-2);
    order: 1;
  }
`),l=(i.AH`
  .sidebar-editor {
    display: block;
    padding-top: 8px;
  }
  .description {
    padding-top: 16px;
  }
`,i.AH`
  .overflow-label {
    display: flex;
    justify-content: space-between;
    gap: var(--ha-space-3);
    white-space: nowrap;
  }
  .overflow-label .shortcut {
    --mdc-icon-size: 12px;
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    gap: 2px;
  }
  .overflow-label .shortcut span {
    font-size: var(--ha-font-size-s);
    font-family: var(--ha-font-family-code);
    color: var(--ha-color-text-secondary);
  }
  .shortcut-placeholder {
    display: inline-block;
    width: 60px;
  }
  .shortcut-placeholder.mac {
    width: 46px;
  }
  @media all and (max-width: 870px) {
    .shortcut-placeholder {
      display: none;
    }
  }
  ha-md-menu-item {
    --mdc-icon-size: 24px;
  }
`)},76681:function(e,t,o){o.d(t,{MR:()=>i,a_:()=>r,bg:()=>a});const i=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,r=e=>e.split("/")[4],a=e=>e.startsWith("https://brands.home-assistant.io/")},98315:function(e,t,o){o.d(t,{c:()=>i});const i=/Mac/i.test(navigator.userAgent)}};
//# sourceMappingURL=5864.2b9f0c9fc224cc62.js.map