export const __webpack_ids__=["6369"];export const __webpack_modules__={24684:function(e,t,i){i.r(t),i.d(t,{HaTTSVoiceSelector:()=>d});var s=i(73742),a=i(59048),o=i(7616);i(80443);class d extends a.oi{render(){return a.dy`<ha-tts-voice-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .language=${this.selector.tts_voice?.language||this.context?.language}
      .engineId=${this.selector.tts_voice?.engineId||this.context?.engineId}
      .disabled=${this.disabled}
      .required=${this.required}
    ></ha-tts-voice-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}d.styles=a.iv`
    ha-tts-picker {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],d.prototype,"selector",void 0),(0,s.__decorate)([(0,o.Cb)()],d.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],d.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],d.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],d.prototype,"context",void 0),d=(0,s.__decorate)([(0,o.Mo)("ha-selector-tts_voice")],d)},80443:function(e,t,i){var s=i(73742),a=i(59048),o=i(7616),d=i(29740),l=i(41806),c=i(16811),r=i(75055);i(93795),i(29490);const h="__NONE_OPTION__";class n extends a.oi{render(){if(!this._voices)return a.Ld;const e=this.value??(this.required?this._voices[0]?.voice_id:h);return a.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${l.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.Ld:a.dy`<ha-list-item .value=${h}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((e=>a.dy`<ha-list-item .value=${e.voice_id}>
              ${e.name}
            </ha-list-item>`))}
      </ha-select>
    `}willUpdate(e){super.willUpdate(e),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}async _updateVoices(){this.engineId&&this.language?(this._voices=(await(0,r.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,d.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}updated(e){super.updated(e),e.has("_voices")&&this._select?.value!==this.value&&(this._select?.layoutOptions(),(0,d.B)(this,"value-changed",{value:this._select?.value}))}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===h||(this.value=t.value===h?void 0:t.value,(0,d.B)(this,"value-changed",{value:this.value}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._debouncedUpdateVoices=(0,c.D)((()=>this._updateVoices()),500)}}n.styles=a.iv`
    ha-select {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,o.Cb)()],n.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],n.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],n.prototype,"engineId",void 0),(0,s.__decorate)([(0,o.Cb)()],n.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],n.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],n.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"required",void 0),(0,s.__decorate)([(0,o.SB)()],n.prototype,"_voices",void 0),(0,s.__decorate)([(0,o.IO)("ha-select")],n.prototype,"_select",void 0),n=(0,s.__decorate)([(0,o.Mo)("ha-tts-voice-picker")],n)},75055:function(e,t,i){i.d(t,{MV:()=>r,Wg:()=>l,Xk:()=>d,aT:()=>s,b_:()=>o,yP:()=>c});const s=(e,t)=>e.callApi("POST","tts_get_url",t),a="media-source://tts/",o=e=>e.startsWith(a),d=e=>e.substring(19),l=(e,t,i)=>e.callWS({type:"tts/engine/list",language:t,country:i}),c=(e,t)=>e.callWS({type:"tts/engine/get",engine_id:t}),r=(e,t,i)=>e.callWS({type:"tts/engine/voices",engine_id:t,language:i})}};
//# sourceMappingURL=6369.c70b452207bc6962.js.map