export const __webpack_ids__=["663"];export const __webpack_modules__={42691:function(e,t,i){i.r(t),i.d(t,{HaAreaSelector:()=>v});var s=i(73742),r=i(59048),a=i(7616),o=i(28105),d=i(74608),c=i(51729),l=i(29740),h=i(71170),n=i(51068),u=i(45103),p=(i(99495),i(66299));class _ extends((0,p.f)(r.oi)){render(){if(!this.hass)return r.Ld;const e=this._currentAreas;return r.dy`
      ${e.map((e=>r.dy`
          <div>
            <ha-area-picker
              .curValue=${e}
              .noAdd=${this.noAdd}
              .hass=${this.hass}
              .value=${e}
              .label=${this.pickedAreaLabel}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .deviceFilter=${this.deviceFilter}
              .entityFilter=${this.entityFilter}
              .disabled=${this.disabled}
              @value-changed=${this._areaChanged}
            ></ha-area-picker>
          </div>
        `))}
      <div>
        <ha-area-picker
          .noAdd=${this.noAdd}
          .hass=${this.hass}
          .label=${this.pickAreaLabel}
          .helper=${this.helper}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .deviceFilter=${this.deviceFilter}
          .entityFilter=${this.entityFilter}
          .disabled=${this.disabled}
          .placeholder=${this.placeholder}
          .required=${this.required&&!e.length}
          @value-changed=${this._addArea}
          .excludeAreas=${e}
        ></ha-area-picker>
      </div>
    `}get _currentAreas(){return this.value||[]}async _updateAreas(e){this.value=e,(0,l.B)(this,"value-changed",{value:e})}_areaChanged(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;if(i===t)return;const s=this._currentAreas;i&&!s.includes(i)?this._updateAreas(s.map((e=>e===t?i:e))):this._updateAreas(s.filter((e=>e!==t)))}_addArea(e){e.stopPropagation();const t=e.detail.value;if(!t)return;e.currentTarget.value="";const i=this._currentAreas;i.includes(t)||this._updateAreas([...i,t])}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1}}_.styles=r.iv`
    div {
      margin-top: 8px;
    }
  `,(0,s.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,s.__decorate)([(0,a.Cb)()],_.prototype,"label",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array})],_.prototype,"value",void 0),(0,s.__decorate)([(0,a.Cb)()],_.prototype,"helper",void 0),(0,s.__decorate)([(0,a.Cb)()],_.prototype,"placeholder",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean,attribute:"no-add"})],_.prototype,"noAdd",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array,attribute:"include-domains"})],_.prototype,"includeDomains",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array,attribute:"exclude-domains"})],_.prototype,"excludeDomains",void 0),(0,s.__decorate)([(0,a.Cb)({type:Array,attribute:"include-device-classes"})],_.prototype,"includeDeviceClasses",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"deviceFilter",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:!1})],_.prototype,"entityFilter",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:"picked-area-label"})],_.prototype,"pickedAreaLabel",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:"pick-area-label"})],_.prototype,"pickAreaLabel",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean})],_.prototype,"disabled",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean})],_.prototype,"required",void 0),_=(0,s.__decorate)([(0,a.Mo)("ha-areas-picker")],_);class v extends r.oi{_hasIntegration(e){return e.area?.entity&&(0,d.r)(e.area.entity).some((e=>e.integration))||e.area?.device&&(0,d.r)(e.area.device).some((e=>e.integration))}willUpdate(e){e.get("selector")&&void 0!==this.value&&(this.selector.area?.multiple&&!Array.isArray(this.value)?(this.value=[this.value],(0,l.B)(this,"value-changed",{value:this.value})):!this.selector.area?.multiple&&Array.isArray(this.value)&&(this.value=this.value[0],(0,l.B)(this,"value-changed",{value:this.value})))}updated(e){e.has("selector")&&this._hasIntegration(this.selector)&&!this._entitySources&&(0,h.m)(this.hass).then((e=>{this._entitySources=e})),!this._configEntries&&this._hasIntegration(this.selector)&&(this._configEntries=[],(0,n.pB)(this.hass).then((e=>{this._configEntries=e})))}render(){return this._hasIntegration(this.selector)&&!this._entitySources?r.Ld:this.selector.area?.multiple?r.dy`
      <ha-areas-picker
        .hass=${this.hass}
        .value=${this.value}
        .helper=${this.helper}
        .pickAreaLabel=${this.label}
        no-add
        .deviceFilter=${this.selector.area?.device?this._filterDevices:void 0}
        .entityFilter=${this.selector.area?.entity?this._filterEntities:void 0}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-areas-picker>
    `:r.dy`
        <ha-area-picker
          .hass=${this.hass}
          .value=${this.value}
          .label=${this.label}
          .helper=${this.helper}
          no-add
          .deviceFilter=${this.selector.area?.device?this._filterDevices:void 0}
          .entityFilter=${this.selector.area?.entity?this._filterEntities:void 0}
          .disabled=${this.disabled}
          .required=${this.required}
        ></ha-area-picker>
      `}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._deviceIntegrationLookup=(0,o.Z)(c.HP),this._filterEntities=e=>!this.selector.area?.entity||(0,d.r)(this.selector.area.entity).some((t=>(0,u.lV)(t,e,this._entitySources))),this._filterDevices=e=>{if(!this.selector.area?.device)return!0;const t=this._entitySources?this._deviceIntegrationLookup(this._entitySources,Object.values(this.hass.entities),Object.values(this.hass.devices),this._configEntries):void 0;return(0,d.r)(this.selector.area.device).some((i=>(0,u.lE)(i,e,t)))}}}(0,s.__decorate)([(0,a.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,s.__decorate)([(0,a.Cb)({attribute:!1})],v.prototype,"selector",void 0),(0,s.__decorate)([(0,a.Cb)()],v.prototype,"value",void 0),(0,s.__decorate)([(0,a.Cb)()],v.prototype,"label",void 0),(0,s.__decorate)([(0,a.Cb)()],v.prototype,"helper",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean})],v.prototype,"disabled",void 0),(0,s.__decorate)([(0,a.Cb)({type:Boolean})],v.prototype,"required",void 0),(0,s.__decorate)([(0,a.SB)()],v.prototype,"_entitySources",void 0),(0,s.__decorate)([(0,a.SB)()],v.prototype,"_configEntries",void 0),v=(0,s.__decorate)([(0,a.Mo)("ha-selector-area")],v)},71170:function(e,t,i){i.d(t,{m:()=>a});const s=async(e,t,i,r,a,...o)=>{const d=a,c=d[e],l=c=>r&&r(a,c.result)!==c.cacheKey?(d[e]=void 0,s(e,t,i,r,a,...o)):c.result;if(c)return c instanceof Promise?c.then(l):l(c);const h=i(a,...o);return d[e]=h,h.then((i=>{d[e]={result:i,cacheKey:r?.(a,i)},setTimeout((()=>{d[e]=void 0}),t)}),(()=>{d[e]=void 0})),h},r=e=>e.callWS({type:"entity/source"}),a=e=>s("_entitySources",3e4,r,(e=>Object.keys(e.states).length),e)},66299:function(e,t,i){i.d(t,{f:()=>a});var s=i(73742),r=i(7616);const a=e=>{class t extends e{connectedCallback(){super.connectedCallback(),this._checkSubscribed()}disconnectedCallback(){if(super.disconnectedCallback(),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}updated(e){if(super.updated(e),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this._checkSubscribed()}hassSubscribe(){return[]}_checkSubscribed(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some((e=>void 0===this[e]))&&(this.__unsubs=this.hassSubscribe())}}return(0,s.__decorate)([(0,r.Cb)({attribute:!1})],t.prototype,"hass",void 0),t}}};
//# sourceMappingURL=663.0bb41b05980a30a8.js.map