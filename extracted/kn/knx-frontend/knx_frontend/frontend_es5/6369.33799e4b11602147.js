"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6369"],{24684:function(e,t,i){i.r(t),i.d(t,{HaTTSVoiceSelector:function(){return n}});i(26847),i(27530);var o=i(73742),s=i(59048),a=i(7616);i(80443);let d,l,r=e=>e;class n extends s.oi{render(){var e,t,i,o;return(0,s.dy)(d||(d=r`<ha-tts-voice-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .language=${0}
      .engineId=${0}
      .disabled=${0}
      .required=${0}
    ></ha-tts-voice-picker>`),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.tts_voice)||void 0===e?void 0:e.language)||(null===(t=this.context)||void 0===t?void 0:t.language),(null===(i=this.selector.tts_voice)||void 0===i?void 0:i.engineId)||(null===(o=this.context)||void 0===o?void 0:o.engineId),this.disabled,this.required)}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}n.styles=(0,s.iv)(l||(l=r`
    ha-tts-picker {
      width: 100%;
    }
  `)),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],n.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],n.prototype,"selector",void 0),(0,o.__decorate)([(0,a.Cb)()],n.prototype,"value",void 0),(0,o.__decorate)([(0,a.Cb)()],n.prototype,"label",void 0),(0,o.__decorate)([(0,a.Cb)()],n.prototype,"helper",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],n.prototype,"disabled",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],n.prototype,"required",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],n.prototype,"context",void 0),n=(0,o.__decorate)([(0,a.Mo)("ha-selector-tts_voice")],n)},80443:function(e,t,i){i(26847),i(81738),i(29981),i(6989),i(1455),i(27530);var o=i(73742),s=i(59048),a=i(7616),d=i(29740),l=i(41806),r=i(16811),n=i(75055);i(93795),i(29490);let c,u,v,h,_=e=>e;const p="__NONE_OPTION__";class b extends s.oi{render(){var e,t;if(!this._voices)return s.Ld;const i=null!==(e=this.value)&&void 0!==e?e:this.required?null===(t=this._voices[0])||void 0===t?void 0:t.voice_id:p;return(0,s.dy)(c||(c=_`
      <ha-select
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        @selected=${0}
        @closed=${0}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0}
        ${0}
      </ha-select>
    `),this.label||this.hass.localize("ui.components.tts-voice-picker.voice"),i,this.required,this.disabled,this._changed,l.U,this.required?s.Ld:(0,s.dy)(u||(u=_`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),p,this.hass.localize("ui.components.tts-voice-picker.none")),this._voices.map((e=>(0,s.dy)(v||(v=_`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),e.voice_id,e.name))))}willUpdate(e){super.willUpdate(e),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}async _updateVoices(){this.engineId&&this.language?(this._voices=(await(0,n.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,d.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}updated(e){var t,i,o;(super.updated(e),e.has("_voices")&&(null===(t=this._select)||void 0===t?void 0:t.value)!==this.value)&&(null===(i=this._select)||void 0===i||i.layoutOptions(),(0,d.B)(this,"value-changed",{value:null===(o=this._select)||void 0===o?void 0:o.value}))}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===p||(this.value=t.value===p?void 0:t.value,(0,d.B)(this,"value-changed",{value:this.value}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._debouncedUpdateVoices=(0,r.D)((()=>this._updateVoices()),500)}}b.styles=(0,s.iv)(h||(h=_`
    ha-select {
      width: 100%;
    }
  `)),(0,o.__decorate)([(0,a.Cb)()],b.prototype,"value",void 0),(0,o.__decorate)([(0,a.Cb)()],b.prototype,"label",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],b.prototype,"engineId",void 0),(0,o.__decorate)([(0,a.Cb)()],b.prototype,"language",void 0),(0,o.__decorate)([(0,a.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean,reflect:!0})],b.prototype,"disabled",void 0),(0,o.__decorate)([(0,a.Cb)({type:Boolean})],b.prototype,"required",void 0),(0,o.__decorate)([(0,a.SB)()],b.prototype,"_voices",void 0),(0,o.__decorate)([(0,a.IO)("ha-select")],b.prototype,"_select",void 0),b=(0,o.__decorate)([(0,a.Mo)("ha-tts-voice-picker")],b)},75055:function(e,t,i){i.d(t,{MV:function(){return n},Wg:function(){return l},Xk:function(){return d},aT:function(){return o},b_:function(){return a},yP:function(){return r}});i(44261);const o=(e,t)=>e.callApi("POST","tts_get_url",t),s="media-source://tts/",a=e=>e.startsWith(s),d=e=>e.substring(19),l=(e,t,i)=>e.callWS({type:"tts/engine/list",language:t,country:i}),r=(e,t)=>e.callWS({type:"tts/engine/get",engine_id:t}),n=(e,t,i)=>e.callWS({type:"tts/engine/voices",engine_id:t,language:i})}}]);
//# sourceMappingURL=6369.33799e4b11602147.js.map