export const __webpack_ids__=["7860"];export const __webpack_modules__={61587:function(e,t,o){o.r(t),o.d(t,{HaConfigEntrySelector:()=>p});var i=o(73742),a=o(59048),r=o(7616),s=o(29740),n=o(92949),d=o(51068),l=o(47469),h=o(37198);o(90256),o(57264);class c extends a.oi{open(){this._comboBox?.open()}focus(){this._comboBox?.focus()}firstUpdated(){this._getConfigEntries()}render(){return this._configEntries?a.dy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.config-entry-picker.config_entry"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${this._rowRenderer}
        .items=${this._configEntries}
        item-value-path="entry_id"
        item-id-path="entry_id"
        item-label-path="title"
        @value-changed=${this._valueChanged}
      ></ha-combo-box>
    `:a.Ld}_onImageLoad(e){e.target.style.visibility="initial"}_onImageError(e){e.target.style.visibility="hidden"}async _getConfigEntries(){(0,d.pB)(this.hass,{type:["device","hub","service"],domain:this.integration}).then((e=>{this._configEntries=e.map((e=>({...e,localized_domain_name:(0,l.Lh)(this.hass.localize,e.domain)}))).sort(((e,t)=>(0,n.fe)(e.localized_domain_name+e.title,t.localized_domain_name+t.title,this.hass.locale.language)))}))}get _value(){return this.value||""}_valueChanged(e){e.stopPropagation();const t=e.detail.value;t!==this._value&&this._setValue(t)}_setValue(e){this.value=e,setTimeout((()=>{(0,s.B)(this,"value-changed",{value:e}),(0,s.B)(this,"change")}),0)}constructor(...e){super(...e),this.value="",this.disabled=!1,this.required=!1,this._rowRenderer=e=>a.dy`
    <ha-combo-box-item type="button">
      <span slot="headline">
        ${e.title||this.hass.localize("ui.panel.config.integrations.config_entry.unnamed_entry")}
      </span>
      <span slot="supporting-text">${e.localized_domain_name}</span>
      <img
        alt=""
        slot="start"
        src=${(0,h.X1)({domain:e.domain,type:"icon",darkOptimized:this.hass.themes?.darkMode})}
        crossorigin="anonymous"
        referrerpolicy="no-referrer"
        @error=${this._onImageError}
        @load=${this._onImageLoad}
      />
    </ha-combo-box-item>
  `}}(0,i.__decorate)([(0,r.Cb)()],c.prototype,"integration",void 0),(0,i.__decorate)([(0,r.Cb)()],c.prototype,"label",void 0),(0,i.__decorate)([(0,r.Cb)()],c.prototype,"value",void 0),(0,i.__decorate)([(0,r.Cb)()],c.prototype,"helper",void 0),(0,i.__decorate)([(0,r.SB)()],c.prototype,"_configEntries",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],c.prototype,"required",void 0),(0,i.__decorate)([(0,r.IO)("ha-combo-box")],c.prototype,"_comboBox",void 0),c=(0,i.__decorate)([(0,r.Mo)("ha-config-entry-picker")],c);class p extends a.oi{render(){return a.dy`<ha-config-entry-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      .integration=${this.selector.config_entry?.integration}
      allow-custom-entity
    ></ha-config-entry-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}p.styles=a.iv`
    ha-config-entry-picker {
      width: 100%;
    }
  `,(0,i.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,i.__decorate)([(0,r.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,i.__decorate)([(0,r.Cb)()],p.prototype,"value",void 0),(0,i.__decorate)([(0,r.Cb)()],p.prototype,"label",void 0),(0,i.__decorate)([(0,r.Cb)()],p.prototype,"helper",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,i.__decorate)([(0,r.Cb)({type:Boolean})],p.prototype,"required",void 0),p=(0,i.__decorate)([(0,r.Mo)("ha-selector-config_entry")],p)},47469:function(e,t,o){o.d(t,{F3:()=>a,Lh:()=>i,t4:()=>r});const i=(e,t,o)=>e(`component.${t}.title`)||o?.name||t,a=(e,t)=>{const o={type:"manifest/list"};return t&&(o.integrations=t),e.callWS(o)},r=(e,t)=>e.callWS({type:"manifest/get",integration:t})},37198:function(e,t,o){o.d(t,{X1:()=>i,u4:()=>a,zC:()=>r});const i=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,a=e=>e.split("/")[4],r=e=>e.startsWith("https://brands.home-assistant.io/")}};
//# sourceMappingURL=7860.ed25bef001e201ee.js.map