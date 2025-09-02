export const __webpack_ids__=["8143"];export const __webpack_modules__={85163:function(e,t,i){i.d(t,{wZ:()=>a,jL:()=>o});var s=i(28105),r=i(31298);const o=e=>(e.name_by_user||e.name)?.trim(),a=(e,t,i)=>o(e)||i&&d(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),d=(e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,s=e.states[t];if(s)return(0,r.C)(s)}};(0,s.Z)((e=>function(e){const t=new Set,i=new Set;for(const s of e)i.has(s)?t.add(s):i.add(s);return t}(Object.values(e).map((e=>o(e))).filter((e=>void 0!==e)))))},31298:function(e,t,i){i.d(t,{C:()=>r});var s=i(93318);const r=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,s.p)(t).replace(/_/g," "):(i.friendly_name??"").toString();var t,i}},36678:function(e,t,i){var s=i(73742),r=i(59048),o=i(7616),a=i(28105),d=i(29740),c=i(71188),n=i(85163),l=i(76151);const h=(e,t)=>{const i=e.area_id,s=i?t.areas[i]:void 0,r=s?.floor_id;return{device:e,area:s||null,floor:(r?t.floors[r]:void 0)||null}};var u=i(51068),p=i(51729),v=i(47469),_=i(37198);i(75691);class y extends r.oi{firstUpdated(e){super.firstUpdated(e),this._loadConfigEntries()}async _loadConfigEntries(){const e=await(0,u.pB)(this.hass);this._configEntryLookup=Object.fromEntries(e.map((e=>[e.entry_id,e])))}render(){const e=this.placeholder??this.hass.localize("ui.components.device-picker.placeholder"),t=this.hass.localize("ui.components.device-picker.no_match"),i=this._valueRenderer(this._configEntryLookup);return r.dy`
      <ha-generic-picker
        .hass=${this.hass}
        .autofocus=${this.autofocus}
        .label=${this.label}
        .searchLabel=${this.searchLabel}
        .notFoundLabel=${t}
        .placeholder=${e}
        .value=${this.value}
        .rowRenderer=${this._rowRenderer}
        .getItems=${this._getItems}
        .hideClearIcon=${this.hideClearIcon}
        .valueRenderer=${i}
        @value-changed=${this._valueChanged}
      >
      </ha-generic-picker>
    `}async open(){await this.updateComplete,await(this._picker?.open())}_valueChanged(e){e.stopPropagation();const t=e.detail.value;this.value=t,(0,d.B)(this,"value-changed",{value:t})}constructor(...e){super(...e),this.autofocus=!1,this.disabled=!1,this.required=!1,this.hideClearIcon=!1,this._configEntryLookup={},this._getItems=()=>this._getDevices(this.hass.devices,this.hass.entities,this._configEntryLookup,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeDevices),this._getDevices=(0,a.Z)(((e,t,i,s,r,o,a,d,u)=>{const _=Object.values(e),y=Object.values(t);let b={};(s||r||o||d)&&(b=(0,p.R6)(y));let m=_.filter((e=>e.id===this.value||!e.disabled_by));s&&(m=m.filter((e=>{const t=b[e.id];return!(!t||!t.length)&&b[e.id].some((e=>s.includes((0,l.M)(e.entity_id))))}))),r&&(m=m.filter((e=>{const t=b[e.id];return!t||!t.length||y.every((e=>!r.includes((0,l.M)(e.entity_id))))}))),u&&(m=m.filter((e=>!u.includes(e.id)))),o&&(m=m.filter((e=>{const t=b[e.id];return!(!t||!t.length)&&b[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&o.includes(t.attributes.device_class))}))}))),d&&(m=m.filter((e=>{const t=b[e.id];return!(!t||!t.length)&&t.some((e=>{const t=this.hass.states[e.entity_id];return!!t&&d(t)}))}))),a&&(m=m.filter((e=>e.id===this.value||a(e))));return m.map((e=>{const t=(0,n.wZ)(e,this.hass,b[e.id]),{area:s}=h(e,this.hass),r=s?(0,c.D)(s):void 0,o=e.primary_config_entry?i?.[e.primary_config_entry]:void 0,a=o?.domain,d=a?(0,v.Lh)(this.hass.localize,a):void 0;return{id:e.id,label:"",primary:t||this.hass.localize("ui.components.device-picker.unnamed_device"),secondary:r,domain:o?.domain,domain_name:d,search_labels:[t,r,a,d].filter(Boolean),sorting_label:t||"zzz"}}))})),this._valueRenderer=(0,a.Z)((e=>t=>{const i=t,s=this.hass.devices[i];if(!s)return r.dy`<span slot="headline">${i}</span>`;const{area:o}=h(s,this.hass),a=s?(0,n.jL)(s):void 0,d=o?(0,c.D)(o):void 0,l=s.primary_config_entry?e[s.primary_config_entry]:void 0;return r.dy`
        ${l?r.dy`<img
              slot="start"
              alt=""
              crossorigin="anonymous"
              referrerpolicy="no-referrer"
              src=${(0,_.X1)({domain:l.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}
            />`:r.Ld}
        <span slot="headline">${a}</span>
        <span slot="supporting-text">${d}</span>
      `})),this._rowRenderer=e=>r.dy`
    <ha-combo-box-item type="button">
      ${e.domain?r.dy`
            <img
              slot="start"
              alt=""
              crossorigin="anonymous"
              referrerpolicy="no-referrer"
              src=${(0,_.X1)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes.darkMode})}
            />
          `:r.Ld}

      <span slot="headline">${e.primary}</span>
      ${e.secondary?r.dy`<span slot="supporting-text">${e.secondary}</span>`:r.Ld}
      ${e.domain_name?r.dy`
            <div slot="trailing-supporting-text" class="domain">
              ${e.domain_name}
            </div>
          `:r.Ld}
    </ha-combo-box-item>
  `}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],y.prototype,"autofocus",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],y.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],y.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"placeholder",void 0),(0,s.__decorate)([(0,o.Cb)({type:String,attribute:"search-label"})],y.prototype,"searchLabel",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1,type:Array})],y.prototype,"createDomains",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"include-domains"})],y.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-domains"})],y.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"include-device-classes"})],y.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-devices"})],y.prototype,"excludeDevices",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"deviceFilter",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"hide-clear-icon",type:Boolean})],y.prototype,"hideClearIcon",void 0),(0,s.__decorate)([(0,o.IO)("ha-generic-picker")],y.prototype,"_picker",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_configEntryLookup",void 0),y=(0,s.__decorate)([(0,o.Mo)("ha-device-picker")],y)},17827:function(e,t,i){i.r(t),i.d(t,{HaDeviceSelector:()=>v});var s=i(73742),r=i(59048),o=i(7616),a=i(28105),d=i(74608),c=i(29740),n=i(51729),l=i(71170),h=i(51068),u=i(45103);i(36678);class p extends r.oi{render(){if(!this.hass)return r.Ld;const e=this._currentDevices;return r.dy`
      ${e.map((e=>r.dy`
          <div>
            <ha-device-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .deviceFilter=${this.deviceFilter}
              .entityFilter=${this.entityFilter}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .value=${e}
              .label=${this.pickedDeviceLabel}
              .disabled=${this.disabled}
              @value-changed=${this._deviceChanged}
            ></ha-device-picker>
          </div>
        `))}
      <div>
        <ha-device-picker
          allow-custom-entity
          .hass=${this.hass}
          .helper=${this.helper}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityFilter}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .excludeDevices=${e}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .label=${this.pickDeviceLabel}
          .disabled=${this.disabled}
          .required=${this.required&&!e.length}
          @value-changed=${this._addDevice}
        ></ha-device-picker>
      </div>
    `}get _currentDevices(){return this.value||[]}async _updateDevices(e){(0,c.B)(this,"value-changed",{value:e}),this.value=e}_deviceChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;i!==t&&(void 0===i?this._updateDevices(this._currentDevices.filter((e=>e!==t))):this._updateDevices(this._currentDevices.map((e=>e===t?i:e))))}async _addDevice(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentDevices;i.includes(t)||this._updateDevices([...i,t])}constructor(...e){super(...e),this.disabled=!1,this.required=!1}}p.styles=r.iv`
    div {
      margin-top: 8px;
    }
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array})],p.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],p.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],p.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"include-domains"})],p.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"exclude-domains"})],p.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,o.Cb)({type:Array,attribute:"include-device-classes"})],p.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"picked-device-label"})],p.prototype,"pickedDeviceLabel",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"pick-device-label"})],p.prototype,"pickDeviceLabel",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],p.prototype,"deviceFilter",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],p.prototype,"entityFilter",void 0),p=(0,s.__decorate)([(0,o.Mo)("ha-devices-picker")],p);class v extends r.oi{_hasIntegration(e){return e.device?.filter&&(0,d.r)(e.device.filter).some((e=>e.integration))||e.device?.entity&&(0,d.r)(e.device.entity).some((e=>e.integration))}willUpdate(e){e.get("selector")&&void 0!==this.value&&(this.selector.device?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,c.B)(this,"value-changed",{value:this.value})):!this.selector.device?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,c.B)(this,"value-changed",{value:this.value})))}updated(e){super.updated(e),e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,l.m)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,h.pB)(this.hass).then((e=>{this._configEntries=e})))}render(){return this._hasIntegration(this.selector)&&!this._entitySources?r.Ld:this.selector.device?.multiple?r.dy`
      ${this.label?r.dy`<label>${this.label}</label>`:""}
      <ha-devices-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .deviceFilter=${this._filterDevices}
        .entityFilter=${this.selector.device?.entity?this._filterEntities:void 0}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-devices-picker>
    `:r.dy`
        <ha-device-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          .deviceFilter=${this._filterDevices}
          .entityFilter=${this.selector.device?.entity?this._filterEntities:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
          allow-custom-entity
        ></ha-device-picker>
      `}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._deviceIntegrationLookup=(0,a.Z)(n.HP),this._filterDevices=e=>{if(!this.selector.device?.filter)return!0;const t=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,d.r)(this.selector.device.filter).some((i=>(0,u.lE)(i,e,t)))},this._filterEntities=e=>(0,d.r)(this.selector.device.entity).some((t=>(0,u.lV)(t,e,this._entitySources)))}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],v.prototype,"selector",void 0),(0,s.__decorate)([(0,o.SB)()],v.prototype,"_entitySources",void 0),(0,s.__decorate)([(0,o.SB)()],v.prototype,"_configEntries",void 0),(0,s.__decorate)([(0,o.Cb)()],v.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],v.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],v.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],v.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],v.prototype,"required",void 0),v=(0,s.__decorate)([(0,o.Mo)("ha-selector-device")],v)},71170:function(e,t,i){i.d(t,{m:()=>o});const s=async(e,t,i,r,o,...a)=>{const d=o,c=d[e],n=c=>r&&r(o,c.result)!==c.cacheKey?(d[e]=void 0,s(e,t,i,r,o,...a)):c.result;if(c)return c instanceof Promise?c.then(n):n(c);const l=i(o,...a);return d[e]=l,l.then((i=>{d[e]={result:i,cacheKey:r?.(o,i)},setTimeout((()=>{d[e]=void 0}),t)}),(()=>{d[e]=void 0})),l},r=e=>e.callWS({type:"entity/source"}),o=e=>s("_entitySources",3e4,r,(e=>Object.keys(e.states).length),e)},47469:function(e,t,i){i.d(t,{F3:()=>r,Lh:()=>s,t4:()=>o});const s=(e,t,i)=>e(`component.${t}.title`)||i?.name||t,r=(e,t)=>{const i={type:"manifest/list"};return t&&(i.integrations=t),e.callWS(i)},o=(e,t)=>e.callWS({type:"manifest/get",integration:t})},37198:function(e,t,i){i.d(t,{X1:()=>s,u4:()=>r,zC:()=>o});const s=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,r=e=>e.split("/")[4],o=e=>e.startsWith("https://brands.home-assistant.io/")}};
//# sourceMappingURL=8143.676f9300fa3f0937.js.map