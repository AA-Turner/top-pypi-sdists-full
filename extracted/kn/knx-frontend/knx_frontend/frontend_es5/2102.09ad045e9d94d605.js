"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["2102"],{30441:function(e,t,i){i.r(t),i.d(t,{HaSTTSelector:function(){return k}});i(26847),i(27530);var s=i(73742),a=i(59048),o=i(7616),d=(i(39710),i(81738),i(29981),i(6989),i(1455),i(56389),i(29740)),n=i(41806),l=i(31298),r=i(16811),u=i(70937),h=(i(93795),i(29490),i(76151));let p,c,_,v,g=e=>e;const b="__NONE_OPTION__";class y extends a.oi{render(){if(!this._engines)return a.Ld;let e=this.value;if(!e&&this.required){for(const t of Object.values(this.hass.entities))if("cloud"===t.platform&&"stt"===(0,h.M)(t.entity_id)){e=t.entity_id;break}if(!e)for(const i of this._engines){var t;if(0!==(null==i||null===(t=i.supported_languages)||void 0===t?void 0:t.length)){e=i.engine_id;break}}}return e||(e=b),(0,a.dy)(p||(p=g`
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
    `),this.label||this.hass.localize("ui.components.stt-picker.stt"),e,this.required,this.disabled,this._changed,n.U,this.required?a.Ld:(0,a.dy)(c||(c=g`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),b,this.hass.localize("ui.components.stt-picker.none")),this._engines.map((t=>{var i;if(t.deprecated&&t.engine_id!==e)return a.Ld;let s;if(t.engine_id.includes(".")){const e=this.hass.states[t.engine_id];s=e?(0,l.C)(e):t.engine_id}else s=t.name||t.engine_id;return(0,a.dy)(_||(_=g`<ha-list-item
            .value=${0}
            .disabled=${0}
          >
            ${0}
          </ha-list-item>`),t.engine_id,0===(null===(i=t.supported_languages)||void 0===i?void 0:i.length),s)})))}willUpdate(e){super.willUpdate(e),this.hasUpdated?e.has("language")&&this._debouncedUpdateEngines():this._updateEngines()}async _updateEngines(){var e;if(this._engines=(await(0,u.m)(this.hass,this.language,this.hass.config.country||void 0)).providers,!this.value)return;const t=this._engines.find((e=>e.engine_id===this.value));(0,d.B)(this,"supported-languages-changed",{value:null==t?void 0:t.supported_languages}),t&&0!==(null===(e=t.supported_languages)||void 0===e?void 0:e.length)||(this.value=void 0,(0,d.B)(this,"value-changed",{value:this.value}))}_changed(e){var t;const i=e.target;!this.hass||""===i.value||i.value===this.value||void 0===this.value&&i.value===b||(this.value=i.value===b?void 0:i.value,(0,d.B)(this,"value-changed",{value:this.value}),(0,d.B)(this,"supported-languages-changed",{value:null===(t=this._engines.find((e=>e.engine_id===this.value)))||void 0===t?void 0:t.supported_languages}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this._debouncedUpdateEngines=(0,r.D)((()=>this._updateEngines()),500)}}y.styles=(0,a.iv)(v||(v=g`
    ha-select {
      width: 100%;
    }
  `)),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],y.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],y.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],y.prototype,"required",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_engines",void 0),y=(0,s.__decorate)([(0,o.Mo)("ha-stt-picker")],y);let f,$,C=e=>e;class k extends a.oi{render(){var e,t;return(0,a.dy)(f||(f=C`<ha-stt-picker
      .hass=${0}
      .value=${0}
      .label=${0}
      .helper=${0}
      .language=${0}
      .disabled=${0}
      .required=${0}
    ></ha-stt-picker>`),this.hass,this.value,this.label,this.helper,(null===(e=this.selector.stt)||void 0===e?void 0:e.language)||(null===(t=this.context)||void 0===t?void 0:t.language),this.disabled,this.required)}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}k.styles=(0,a.iv)($||($=C`
    ha-stt-picker {
      width: 100%;
    }
  `)),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],k.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],k.prototype,"selector",void 0),(0,s.__decorate)([(0,o.Cb)()],k.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],k.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)()],k.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],k.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],k.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],k.prototype,"context",void 0),k=(0,s.__decorate)([(0,o.Mo)("ha-selector-stt")],k)},70937:function(e,t,i){i.d(t,{m:function(){return s}});const s=(e,t,i)=>e.callWS({type:"stt/engine/list",language:t,country:i})}}]);
//# sourceMappingURL=2102.09ad045e9d94d605.js.map