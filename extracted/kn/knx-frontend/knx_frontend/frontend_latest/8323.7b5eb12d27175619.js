/*! For license information please see 8323.7b5eb12d27175619.js.LICENSE.txt */
export const __webpack_ids__=["8323"];export const __webpack_modules__={85163:function(t,e,i){i.d(e,{wZ:()=>n,jL:()=>o});var s=i(28105),a=i(31298);const o=t=>(t.name_by_user||t.name)?.trim(),n=(t,e,i)=>o(t)||i&&r(e,i)||e.localize("ui.panel.config.devices.unnamed_device",{type:e.localize(`ui.panel.config.devices.type.${t.entry_type||"device"}`)}),r=(t,e)=>{for(const i of e||[]){const e="string"==typeof i?i:i.entity_id,s=t.states[e];if(s)return(0,a.C)(s)}};(0,s.Z)((t=>function(t){const e=new Set,i=new Set;for(const s of t)i.has(s)?e.add(s):i.add(s);return e}(Object.values(t).map((t=>o(t))).filter((t=>void 0!==t)))))},10996:function(t,e,i){i.d(e,{K:()=>r});var s=i(85163),a=i(31298);const o=[" ",": "," - "],n=t=>t.toLowerCase()!==t,r=(t,e)=>{const i=e.entities[t.entity_id];return i?c(i,e):(0,a.C)(t)},c=(t,e)=>{const i=t.name||("original_name"in t?t.original_name:void 0),r=t.device_id?e.devices[t.device_id]:void 0;if(!r){if(i)return i;const s=e.states[t.entity_id];return s?(0,a.C)(s):void 0}const c=(0,s.jL)(r);if(c!==i)return c&&i&&((t,e)=>{const i=t.toLowerCase(),s=e.toLowerCase();for(const a of o){const e=`${s}${a}`;if(i.startsWith(e)){const i=t.substring(e.length);if(i.length)return n(i.substr(0,i.indexOf(" ")))?i:i[0].toUpperCase()+i.slice(1)}}})(i,c)||i}},31298:function(t,e,i){i.d(e,{C:()=>a});var s=i(93318);const a=t=>{return e=t.entity_id,void 0===(i=t.attributes).friendly_name?(0,s.p)(e).replace(/_/g," "):(i.friendly_name??"").toString();var e,i}},66027:function(t,e,i){i.d(e,{U:()=>s});const s=(t,e)=>{const i=e.entities[t.entity_id];return i?a(i,e):{entity:null,device:null,area:null,floor:null}},a=(t,e)=>{const i=e.entities[t.entity_id],s=t?.device_id,a=s?e.devices[s]:void 0,o=t?.area_id||a?.area_id,n=o?e.areas[o]:void 0,r=n?.floor_id;return{entity:i,device:a||null,area:n||null,floor:(r?e.floors[r]:void 0)||null}}},62238:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(28105),r=i(74608),c=i(29740),d=i(71188),l=i(85163),h=i(10996),u=i(31298),p=i(66027),_=i(80913),y=i(47469),v=i(66855),b=i(47584),C=(i(57264),i(75691),i(78645),i(42592),i(40830),i(37351)),f=t([C]);C=(f.then?(await f)():f)[0];const $="M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z",m="M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z",g="M11,13.5V21.5H3V13.5H11M12,2L17.5,11H6.5L12,2M17.5,13C20,13 22,15 22,17.5C22,20 20,22 17.5,22C15,22 13,20 13,17.5C13,15 15,13 17.5,13Z",w=["entity","external","no_state"],S="___missing-entity___";class x extends a.oi{willUpdate(t){(!this.hasUpdated&&!this.statisticIds||t.has("statisticTypes"))&&this._getStatisticIds()}async _getStatisticIds(){this.statisticIds=await(0,v.uR)(this.hass,this.statisticTypes)}_getAdditionalItems(){return[{id:S,primary:this.hass.localize("ui.components.statistic-picker.missing_entity"),icon_path:m}]}_computeItem(t){const e=this.hass.states[t];if(e){const{area:i,device:s}=(0,p.U)(e,this.hass),a=(0,h.K)(e,this.hass),o=s?(0,l.jL)(s):void 0,n=i?(0,d.D)(i):void 0,r=(0,_.HE)(this.hass),c=a||o||t,y=[n,a?o:void 0].filter(Boolean).join(r?" ◂ ":" ▸ "),v=(0,u.C)(e);return{id:t,statistic_id:t,primary:c,secondary:y,stateObj:e,type:"entity",sorting_label:[`${w.indexOf("entity")}`,o,a].join("_"),search_labels:[a,o,n,v,t].filter(Boolean)}}const i=this.statisticIds?this._statisticMetaData(t,this.statisticIds):void 0;if(i){if("external"===(t.includes(":")&&!t.includes(".")?"external":"no_state")){const e=`${w.indexOf("external")}`,s=(0,v.Kd)(this.hass,t,i),a=t.split(":")[0],o=(0,y.Lh)(this.hass.localize,a);return{id:t,statistic_id:t,primary:s,secondary:o,type:"external",sorting_label:[e,s].join("_"),search_labels:[s,o,t],icon_path:$}}}const s=`${w.indexOf("external")}`,a=(0,v.Kd)(this.hass,t,i);return{id:t,primary:a,secondary:this.hass.localize("ui.components.statistic-picker.no_state"),type:"no_state",sorting_label:[s,a].join("_"),search_labels:[a,t],icon_path:g}}render(){const t=this.placeholder??this.hass.localize("ui.components.statistic-picker.placeholder"),e=this.hass.localize("ui.components.statistic-picker.no_match");return a.dy`
      <ha-generic-picker
        .hass=${this.hass}
        .autofocus=${this.autofocus}
        .allowCustomValue=${this.allowCustomEntity}
        .label=${this.label}
        .notFoundLabel=${e}
        .placeholder=${t}
        .value=${this.value}
        .rowRenderer=${this._rowRenderer}
        .getItems=${this._getItems}
        .getAdditionalItems=${this._getAdditionalItems}
        .hideClearIcon=${this.hideClearIcon}
        .searchFn=${this._searchFn}
        .valueRenderer=${this._valueRenderer}
        @value-changed=${this._valueChanged}
      >
      </ha-generic-picker>
    `}_valueChanged(t){t.stopPropagation();const e=t.detail.value;e!==S?(this.value=e,(0,c.B)(this,"value-changed",{value:e})):window.open((0,b.R)(this.hass,this.helpMissingEntityUrl),"_blank")}async open(){await this.updateComplete,await(this._picker?.open())}constructor(...t){super(...t),this.autofocus=!1,this.disabled=!1,this.required=!1,this.helpMissingEntityUrl="/more-info/statistics/",this.entitiesOnly=!1,this.hideClearIcon=!1,this._getItems=()=>this._getStatisticsItems(this.hass,this.statisticIds,this.includeStatisticsUnitOfMeasurement,this.includeUnitClass,this.includeDeviceClass,this.entitiesOnly,this.excludeStatistics,this.value),this._getStatisticsItems=(0,n.Z)(((t,e,i,s,a,o,n,c)=>{if(!e)return[];if(i){const t=(0,r.r)(i);e=e.filter((e=>t.includes(e.statistics_unit_of_measurement)))}if(s){const t=(0,r.r)(s);e=e.filter((e=>t.includes(e.unit_class)))}if(a){const t=(0,r.r)(a);e=e.filter((e=>{const i=this.hass.states[e.statistic_id];return!i||t.includes(i.attributes.device_class||"")}))}const b=(0,_.HE)(this.hass),C=[];return e.forEach((e=>{if(n&&e.statistic_id!==c&&n.includes(e.statistic_id))return;const i=this.hass.states[e.statistic_id];if(!i){if(!o){const t=e.statistic_id,i=(0,v.Kd)(this.hass,e.statistic_id,e),s=e.statistic_id.includes(":")&&!e.statistic_id.includes(".")?"external":"no_state",a=`${w.indexOf(s)}`;if("no_state"===s)C.push({id:t,primary:i,secondary:this.hass.localize("ui.components.statistic-picker.no_state"),type:s,sorting_label:[a,i].join("_"),search_labels:[i,t],icon_path:g});else if("external"===s){const e=t.split(":")[0],o=(0,y.Lh)(this.hass.localize,e);C.push({id:t,statistic_id:t,primary:i,secondary:o,type:s,sorting_label:[a,i].join("_"),search_labels:[i,o,t],icon_path:$})}}return}const s=e.statistic_id,{area:a,device:r}=(0,p.U)(i,t),_=(0,u.C)(i),f=(0,h.K)(i,t),m=r?(0,l.jL)(r):void 0,S=a?(0,d.D)(a):void 0,x=f||m||s,O=[S,f?m:void 0].filter(Boolean).join(b?" ◂ ":" ▸ "),k=[m,f].filter(Boolean).join(" - "),I=`${w.indexOf("entity")}`;C.push({id:s,statistic_id:s,primary:x,secondary:O,a11y_label:k,stateObj:i,type:"entity",sorting_label:[I,m,f].join("_"),search_labels:[f,m,S,_,s].filter(Boolean)})})),C})),this._statisticMetaData=(0,n.Z)(((t,e)=>{if(e)return e.find((e=>e.statistic_id===t))})),this._valueRenderer=t=>{const e=t,i=this._computeItem(e);return a.dy`
      ${i.stateObj?a.dy`
            <state-badge
              .hass=${this.hass}
              .stateObj=${i.stateObj}
              slot="start"
            ></state-badge>
          `:i.icon_path?a.dy`
              <ha-svg-icon slot="start" .path=${i.icon_path}></ha-svg-icon>
            `:a.Ld}
      <span slot="headline">${i.primary}</span>
      ${i.secondary?a.dy`<span slot="supporting-text">${i.secondary}</span>`:a.Ld}
    `},this._rowRenderer=(t,{index:e})=>{const i=this.hass.userData?.showEntityIdPicker;return a.dy`
      <ha-combo-box-item type="button" compact .borderTop=${0!==e}>
        ${t.icon_path?a.dy`
              <ha-svg-icon
                style="margin: 0 4px"
                slot="start"
                .path=${t.icon_path}
              ></ha-svg-icon>
            `:t.stateObj?a.dy`
                <state-badge
                  slot="start"
                  .stateObj=${t.stateObj}
                  .hass=${this.hass}
                ></state-badge>
              `:a.Ld}
        <span slot="headline">${t.primary} </span>
        ${t.secondary?a.dy`<span slot="supporting-text">${t.secondary}</span>`:a.Ld}
        ${t.statistic_id&&i?a.dy`<span slot="supporting-text" class="code">
              ${t.statistic_id}
            </span>`:a.Ld}
      </ha-combo-box-item>
    `},this._searchFn=(t,e)=>{const i=e.findIndex((e=>e.stateObj?.entity_id===t||e.statistic_id===t));if(-1===i)return e;const[s]=e.splice(i,1);return e.unshift(s),e}}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],x.prototype,"autofocus",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],x.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],x.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)()],x.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],x.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],x.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)()],x.prototype,"placeholder",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"statistic-types"})],x.prototype,"statisticTypes",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,attribute:"allow-custom-entity"})],x.prototype,"allowCustomEntity",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1,type:Array})],x.prototype,"statisticIds",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],x.prototype,"helpMissingEntityUrl",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"include-statistics-unit-of-measurement"})],x.prototype,"includeStatisticsUnitOfMeasurement",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"include-unit-class"})],x.prototype,"includeUnitClass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"include-device-class"})],x.prototype,"includeDeviceClass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,attribute:"entities-only"})],x.prototype,"entitiesOnly",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-statistics"})],x.prototype,"excludeStatistics",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"hide-clear-icon",type:Boolean})],x.prototype,"hideClearIcon",void 0),(0,s.__decorate)([(0,o.IO)("ha-generic-picker")],x.prototype,"_picker",void 0),x=(0,s.__decorate)([(0,o.Mo)("ha-statistic-picker")],x),e()}catch($){e($)}}))},43013:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(88245),r=i(29740),c=i(62238),d=t([c]);c=(d.then?(await d)():d)[0];class l extends a.oi{render(){if(!this.hass)return a.Ld;const t=this.ignoreRestrictionsOnFirstStatistic&&this._currentStatistics.length<=1,e=t?void 0:this.includeStatisticsUnitOfMeasurement,i=t?void 0:this.includeUnitClass,s=t?void 0:this.includeDeviceClass,o=t?void 0:this.statisticTypes;return a.dy`
      ${this.label?a.dy`<label>${this.label}</label>`:a.Ld}
      ${(0,n.r)(this._currentStatistics,(t=>t),(t=>a.dy`
          <div>
            <ha-statistic-picker
              .curValue=${t}
              .hass=${this.hass}
              .includeStatisticsUnitOfMeasurement=${e}
              .includeUnitClass=${i}
              .includeDeviceClass=${s}
              .value=${t}
              .statisticTypes=${o}
              .statisticIds=${this.statisticIds}
              .excludeStatistics=${this.value}
              .allowCustomEntity=${this.allowCustomEntity}
              @value-changed=${this._statisticChanged}
            ></ha-statistic-picker>
          </div>
        `))}
      <div>
        <ha-statistic-picker
          .hass=${this.hass}
          .includeStatisticsUnitOfMeasurement=${this.includeStatisticsUnitOfMeasurement}
          .includeUnitClass=${this.includeUnitClass}
          .includeDeviceClass=${this.includeDeviceClass}
          .statisticTypes=${this.statisticTypes}
          .statisticIds=${this.statisticIds}
          .placeholder=${this.placeholder}
          .excludeStatistics=${this.value}
          .allowCustomEntity=${this.allowCustomEntity}
          @value-changed=${this._addStatistic}
        ></ha-statistic-picker>
      </div>
    `}get _currentStatistics(){return this.value||[]}async _updateStatistics(t){this.value=t,(0,r.B)(this,"value-changed",{value:t})}_statisticChanged(t){t.stopPropagation();const e=t.currentTarget.curValue,i=t.detail.value;if(i===e)return;const s=this._currentStatistics;i&&!s.includes(i)?this._updateStatistics(s.map((t=>t===e?i:t))):this._updateStatistics(s.filter((t=>t!==e)))}async _addStatistic(t){t.stopPropagation();const e=t.detail.value;if(!e)return;if(t.currentTarget.value="",!e)return;const i=this._currentStatistics;i.includes(e)||this._updateStatistics([...i,e])}constructor(...t){super(...t),this.ignoreRestrictionsOnFirstStatistic=!1}}l.styles=a.iv`
    :host {
      display: block;
    }
    ha-statistic-picker {
      display: block;
      width: 100%;
      margin-top: 8px;
    }
    label {
      display: block;
      margin-bottom: 0 0 8px;
    }
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array})],l.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1,type:Array})],l.prototype,"statisticIds",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"statistic-types"})],l.prototype,"statisticTypes",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],l.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],l.prototype,"placeholder",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,attribute:"allow-custom-entity"})],l.prototype,"allowCustomEntity",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"include-statistics-unit-of-measurement"})],l.prototype,"includeStatisticsUnitOfMeasurement",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"include-unit-class"})],l.prototype,"includeUnitClass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"include-device-class"})],l.prototype,"includeDeviceClass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,attribute:"ignore-restrictions-on-first-statistic"})],l.prototype,"ignoreRestrictionsOnFirstStatistic",void 0),l=(0,s.__decorate)([(0,o.Mo)("ha-statistics-picker")],l),e()}catch(l){e(l)}}))},76641:function(t,e,i){i.a(t,(async function(t,s){try{i.r(e),i.d(e,{HaStatisticSelector:()=>d});var a=i(73742),o=i(59048),n=i(7616),r=i(43013),c=t([r]);r=(c.then?(await c)():c)[0];class d extends o.oi{render(){return this.selector.statistic.multiple?o.dy`
      ${this.label?o.dy`<label>${this.label}</label>`:""}
      <ha-statistics-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-statistics-picker>
    `:o.dy`<ha-statistic-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        allow-custom-entity
      ></ha-statistic-picker>`}constructor(...t){super(...t),this.disabled=!1,this.required=!0}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"selector",void 0),(0,a.__decorate)([(0,n.Cb)()],d.prototype,"value",void 0),(0,a.__decorate)([(0,n.Cb)()],d.prototype,"label",void 0),(0,a.__decorate)([(0,n.Cb)()],d.prototype,"helper",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],d.prototype,"disabled",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],d.prototype,"required",void 0),d=(0,a.__decorate)([(0,n.Mo)("ha-selector-statistic")],d),s()}catch(d){s(d)}}))},64930:function(t,e,i){i.d(e,{ON:()=>n,PX:()=>r,V_:()=>c,lz:()=>o,nZ:()=>a,rk:()=>l});var s=i(13228);const a="unavailable",o="unknown",n="on",r="off",c=[a,o],d=[a,o,r],l=(0,s.z)(c);(0,s.z)(d)},47469:function(t,e,i){i.d(e,{F3:()=>a,Lh:()=>s,t4:()=>o});const s=(t,e,i)=>t(`component.${e}.title`)||i?.name||e,a=(t,e)=>{const i={type:"manifest/list"};return e&&(i.integrations=e),t.callWS(i)},o=(t,e)=>t.callWS({type:"manifest/get",integration:e})},66855:function(t,e,i){i.d(e,{Kd:()=>o,uR:()=>a});var s=i(31298);const a=(t,e)=>t.callWS({type:"recorder/list_statistic_ids",statistic_type:e}),o=(t,e,i)=>{const a=t.states[e];return a?(0,s.C)(a):i?.name||e}},47584:function(t,e,i){i.d(e,{R:()=>s});const s=(t,e)=>`https://${t.config.version.includes("b")?"rc":t.config.version.includes("dev")?"next":"www"}.home-assistant.io${e}`},12790:function(t,e,i){i.d(e,{C:()=>u});var s=i(35340),a=i(5277),o=i(93847);class n{disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}constructor(t){this.G=t}}class r{get(){return this.Y}pause(){this.Y??=new Promise((t=>this.Z=t))}resume(){this.Z?.(),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var c=i(83522);const d=t=>!(0,a.pt)(t)&&"function"==typeof t.then,l=1073741823;class h extends o.sR{render(...t){return t.find((t=>!d(t)))??s.Jb}update(t,e){const i=this._$Cbt;let a=i.length;this._$Cbt=e;const o=this._$CK,n=this._$CX;this.isConnected||this.disconnected();for(let s=0;s<e.length&&!(s>this._$Cwt);s++){const t=e[s];if(!d(t))return this._$Cwt=s,t;s<a&&t===i[s]||(this._$Cwt=l,a=0,Promise.resolve(t).then((async e=>{for(;n.get();)await n.get();const i=o.deref();if(void 0!==i){const s=i._$Cbt.indexOf(t);s>-1&&s<i._$Cwt&&(i._$Cwt=s,i.setValue(e))}})))}return s.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=l,this._$Cbt=[],this._$CK=new n(this),this._$CX=new r}}const u=(0,c.XM)(h)}};
//# sourceMappingURL=8323.7b5eb12d27175619.js.map