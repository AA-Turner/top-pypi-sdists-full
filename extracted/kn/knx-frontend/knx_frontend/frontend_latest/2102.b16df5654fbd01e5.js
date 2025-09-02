export const __webpack_ids__=["2102"];export const __webpack_modules__={31298:function(e,t,i){i.d(t,{C:()=>a});var s=i(93318);const a=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,s.p)(t).replace(/_/g," "):(i.friendly_name??"").toString();var t,i}},30441:function(e,t,i){i.r(t),i.d(t,{HaSTTSelector:()=>c});var s=i(73742),a=i(59048),o=i(7616),d=i(29740),n=i(41806),r=i(31298),l=i(16811),u=i(70937),h=(i(93795),i(29490),i(76151));const _="__NONE_OPTION__";class p extends a.oi{render(){if(!this._engines)return a.Ld;let e=this.value;if(!e&&this.required){for(const t of Object.values(this.hass.entities))if("cloud"===t.platform&&"stt"===(0,h.M)(t.entity_id)){e=t.entity_id;break}if(!e)for(const t of this._engines)if(0!==t?.supported_languages?.length){e=t.engine_id;break}}return e||(e=_),a.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.stt-picker.stt")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${n.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.Ld:a.dy`<ha-list-item .value=${_}>
              ${this.hass.localize("ui.components.stt-picker.none")}
            </ha-list-item>`}
        ${this._engines.map((t=>{if(t.deprecated&&t.engine_id!==e)return a.Ld;let i;if(t.engine_id.includes(".")){const e=this.hass.states[t.engine_id];i=e?(0,r.C)(e):t.engine_id}else i=t.name||t.engine_id;return a.dy`<ha-list-item
            .value=${t.engine_id}
            .disabled=${0===t.supported_languages?.length}
          >
            ${i}
          </ha-list-item>`}))}
      </ha-select>
    `}willUpdate(e){super.willUpdate(e),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}async _updateEngines(){if(this._engines=(await(0,u.m)(this.hass,this.language,this.hass.config.country||void 0)).providers,!this.value)return;const e=this._engines.find((e=>e.engine_id===this.value));(0,d.B)(this,"supported-languages-changed",{value:e?.supported_languages}),e&&0!==e.supported_languages?.length||(this.value=void 0,(0,d.B)(this,"value-changed",{value:this.value}))}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===_||(this.value=t.value===_?void 0:t.value,(0,d.B)(this,"value-changed",{value:this.value}),(0,d.B)(this,"supported-languages-changed",{value:this._engines.find((e=>e.engine_id===this.value))?.supported_languages}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._debouncedUpdateEngines=(0,l.D)((()=>this._updateEngines()),500)}}p.styles=a.iv`
    ha-select {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,o.Cb)()],p.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],p.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],p.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],p.prototype,"required",void 0),(0,s.__decorate)([(0,o.SB)()],p.prototype,"_engines",void 0),p=(0,s.__decorate)([(0,o.Mo)("ha-stt-picker")],p);class c extends a.oi{render(){return a.dy`<ha-stt-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.stt?.language||this.context?.language}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-stt-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}c.styles=a.iv`
    ha-stt-picker {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],c.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],c.prototype,"selector",void 0),(0,s.__decorate)([(0,o.Cb)()],c.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],c.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],c.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],c.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],c.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],c.prototype,"context",void 0),c=(0,s.__decorate)([(0,o.Mo)("ha-selector-stt")],c)},70937:function(e,t,i){i.d(t,{m:()=>s});const s=(e,t,i)=>e.callWS({type:"stt/engine/list",language:t,country:i})}};
//# sourceMappingURL=2102.b16df5654fbd01e5.js.map