export const __webpack_ids__=["282"];export const __webpack_modules__={18252:function(e,o,t){t.r(o),t.d(o,{HaAddonSelector:()=>c});var s=t(73742),a=t(59048),i=t(7616),r=t(42822),d=t(29740),n=t(92949),l=t(81086);t(22543),t(90256),t(57264);const p=e=>a.dy`
  <ha-combo-box-item type="button">
    <span slot="headline">${e.name}</span>
    <span slot="supporting-text">${e.slug}</span>
    ${e.icon?a.dy`
          <img
            alt=""
            slot="start"
            .src="/api/hassio/addons/${e.slug}/icon"
          />
        `:a.Ld}
  </ha-combo-box-item>
`;class h extends a.oi{open(){this._comboBox?.open()}focus(){this._comboBox?.focus()}firstUpdated(){this._getAddons()}render(){return this._error?a.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:this._addons?a.dy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${p}
        .items=${this._addons}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${this._addonChanged}
      ></ha-combo-box>
    `:a.Ld}async _getAddons(){try{if((0,r.p)(this.hass,"hassio")){const e=await(0,l.yt)(this.hass);this._addons=e.addons.filter((e=>e.version)).sort(((e,o)=>(0,n.$K)(e.name,o.name,this.hass.locale.language)))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}get _value(){return this.value||""}_addonChanged(e){e.stopPropagation();const o=e.detail.value;o!==this._value&&this._setValue(o)}_setValue(e){this.value=e,setTimeout((()=>{(0,d.B)(this,"value-changed",{value:e}),(0,d.B)(this,"change")}),0)}constructor(...e){super(...e),this.value="",this.disabled=!1,this.required=!1}}(0,s.__decorate)([(0,i.Cb)()],h.prototype,"label",void 0),(0,s.__decorate)([(0,i.Cb)()],h.prototype,"value",void 0),(0,s.__decorate)([(0,i.Cb)()],h.prototype,"helper",void 0),(0,s.__decorate)([(0,i.SB)()],h.prototype,"_addons",void 0),(0,s.__decorate)([(0,i.Cb)({type:Boolean})],h.prototype,"disabled",void 0),(0,s.__decorate)([(0,i.Cb)({type:Boolean})],h.prototype,"required",void 0),(0,s.__decorate)([(0,i.IO)("ha-combo-box")],h.prototype,"_comboBox",void 0),(0,s.__decorate)([(0,i.SB)()],h.prototype,"_error",void 0),h=(0,s.__decorate)([(0,i.Mo)("ha-addon-picker")],h);class c extends a.oi{render(){return a.dy`<ha-addon-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      allow-custom-entity
    ></ha-addon-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}c.styles=a.iv`
    ha-addon-picker {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,i.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,s.__decorate)([(0,i.Cb)({attribute:!1})],c.prototype,"selector",void 0),(0,s.__decorate)([(0,i.Cb)()],c.prototype,"value",void 0),(0,s.__decorate)([(0,i.Cb)()],c.prototype,"label",void 0),(0,s.__decorate)([(0,i.Cb)()],c.prototype,"helper",void 0),(0,s.__decorate)([(0,i.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,s.__decorate)([(0,i.Cb)({type:Boolean})],c.prototype,"required",void 0),c=(0,s.__decorate)([(0,i.Mo)("ha-selector-addon")],c)},81086:function(e,o,t){t.d(o,{fU:()=>d,kP:()=>r,yt:()=>i});var s=t(35859),a=t(10840);const i=async e=>(0,s.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,a.rY)(await e.callApi("GET","hassio/addons")),r=async(e,o)=>(0,s.I)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:`/addons/${o}/start`,method:"post",timeout:null}):e.callApi("POST",`hassio/addons/${o}/start`),d=async(e,o)=>{(0,s.I)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:`/addons/${o}/install`,method:"post",timeout:null}):await e.callApi("POST",`hassio/addons/${o}/install`)}},10840:function(e,o,t){t.d(o,{js:()=>a,rY:()=>s});const s=e=>e.data,a=e=>"object"==typeof e?"object"==typeof e.body?e.body.message||"Unknown error, see supervisor logs":e.body||e.message||"Unknown error, see supervisor logs":e;new Set([502,503,504])}};
//# sourceMappingURL=282.96a1990a0da96da1.js.map