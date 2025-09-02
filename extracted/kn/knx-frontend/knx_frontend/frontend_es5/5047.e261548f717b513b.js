"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["5047"],{75972:function(e,t,s){s.a(e,(async function(e,i){try{s.d(t,{u:function(){return l}});var a=s(57900),n=s(28105),r=e([a]);a=(r.then?(await r)():r)[0];const l=(e,t)=>{try{var s,i;return null!==(s=null===(i=o(t))||void 0===i?void 0:i.of(e))&&void 0!==s?s:e}catch(a){return e}},o=(0,n.Z)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})));i()}catch(l){i(l)}}))},69187:function(e,t,s){s.a(e,(async function(e,t){try{s(26847),s(81738),s(29981),s(6989),s(27530);var i=s(73742),a=s(59048),n=s(7616),r=s(29740),l=s(41806),o=s(75972),d=s(32518),c=(s(93795),s(29490),e([o]));o=(c.then?(await c)():c)[0];let p,u,h,b,_=e=>e;const g="preferred",v="last_used";class y extends a.oi{get _default(){return this.includeLastUsed?v:g}render(){var e,t;if(!this._pipelines)return a.Ld;const s=null!==(e=this.value)&&void 0!==e?e:this._default;return(0,a.dy)(p||(p=_`
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
        <ha-list-item .value=${0}>
          ${0}
        </ha-list-item>
        ${0}
      </ha-select>
    `),this.label||this.hass.localize("ui.components.pipeline-picker.pipeline"),s,this.required,this.disabled,this._changed,l.U,this.includeLastUsed?(0,a.dy)(u||(u=_`
              <ha-list-item .value=${0}>
                ${0}
              </ha-list-item>
            `),v,this.hass.localize("ui.components.pipeline-picker.last_used")):null,g,this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:null===(t=this._pipelines.find((e=>e.id===this._preferredPipeline)))||void 0===t?void 0:t.name}),this._pipelines.map((e=>(0,a.dy)(h||(h=_`<ha-list-item .value=${0}>
              ${0}
              (${0})
            </ha-list-item>`),e.id,e.name,(0,o.u)(e.language,this.hass.locale)))))}firstUpdated(e){super.firstUpdated(e),(0,d.SC)(this.hass).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===this._default||(this.value=t.value===this._default?void 0:t.value,(0,r.B)(this,"value-changed",{value:this.value}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.includeLastUsed=!1,this._preferredPipeline=null}}y.styles=(0,a.iv)(b||(b=_`
    ha-select {
      width: 100%;
    }
  `)),(0,i.__decorate)([(0,n.Cb)()],y.prototype,"value",void 0),(0,i.__decorate)([(0,n.Cb)()],y.prototype,"label",void 0),(0,i.__decorate)([(0,n.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],y.prototype,"disabled",void 0),(0,i.__decorate)([(0,n.Cb)({type:Boolean})],y.prototype,"required",void 0),(0,i.__decorate)([(0,n.Cb)({attribute:!1})],y.prototype,"includeLastUsed",void 0),(0,i.__decorate)([(0,n.SB)()],y.prototype,"_pipelines",void 0),(0,i.__decorate)([(0,n.SB)()],y.prototype,"_preferredPipeline",void 0),y=(0,i.__decorate)([(0,n.Mo)("ha-assist-pipeline-picker")],y),t()}catch(p){t(p)}}))},83019:function(e,t,s){s.a(e,(async function(e,i){try{s.r(t),s.d(t,{HaAssistPipelineSelector:function(){return u}});s(26847),s(27530);var a=s(73742),n=s(59048),r=s(7616),l=s(69187),o=e([l]);l=(o.then?(await o)():o)[0];let d,c,p=e=>e;class u extends n.oi{render(){var e;return(0,n.dy)(d||(d=p`
      <ha-assist-pipeline-picker
        .hass=${0}
        .value=${0}
        .label=${0}
        .helper=${0}
        .disabled=${0}
        .required=${0}
        .includeLastUsed=${0}
      ></ha-assist-pipeline-picker>
    `),this.hass,this.value,this.label,this.helper,this.disabled,this.required,Boolean(null===(e=this.selector.assist_pipeline)||void 0===e?void 0:e.include_last_used))}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}u.styles=(0,n.iv)(c||(c=p`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `)),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],u.prototype,"selector",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"value",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"label",void 0),(0,a.__decorate)([(0,r.Cb)()],u.prototype,"helper",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],u.prototype,"required",void 0),u=(0,a.__decorate)([(0,r.Mo)("ha-selector-assist_pipeline")],u),i()}catch(d){i(d)}}))},32518:function(e,t,s){s.d(t,{Dy:function(){return d},PA:function(){return r},SC:function(){return n},Xp:function(){return a},af:function(){return o},eP:function(){return i},jZ:function(){return l}});s(26847),s(87799),s(27530);const i=(e,t,s)=>"run-start"===t.type?e={init_options:s,stage:"ready",run:t.data,events:[t]}:e?((e="wake_word-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"wake_word",wake_word:Object.assign(Object.assign({},t.data),{},{done:!1})}):"wake_word-end"===t.type?Object.assign(Object.assign({},e),{},{wake_word:Object.assign(Object.assign(Object.assign({},e.wake_word),t.data),{},{done:!0})}):"stt-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"stt",stt:Object.assign(Object.assign({},t.data),{},{done:!1})}):"stt-end"===t.type?Object.assign(Object.assign({},e),{},{stt:Object.assign(Object.assign(Object.assign({},e.stt),t.data),{},{done:!0})}):"intent-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"intent",intent:Object.assign(Object.assign({},t.data),{},{done:!1})}):"intent-end"===t.type?Object.assign(Object.assign({},e),{},{intent:Object.assign(Object.assign(Object.assign({},e.intent),t.data),{},{done:!0})}):"tts-start"===t.type?Object.assign(Object.assign({},e),{},{stage:"tts",tts:Object.assign(Object.assign({},t.data),{},{done:!1})}):"tts-end"===t.type?Object.assign(Object.assign({},e),{},{tts:Object.assign(Object.assign(Object.assign({},e.tts),t.data),{},{done:!0})}):"run-end"===t.type?Object.assign(Object.assign({},e),{},{stage:"done"}):"error"===t.type?Object.assign(Object.assign({},e),{},{stage:"error",error:t.data}):Object.assign({},e)).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),a=(e,t,s)=>e.connection.subscribeMessage(t,Object.assign(Object.assign({},s),{},{type:"assist_pipeline/run"})),n=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),r=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),l=(e,t)=>e.callWS(Object.assign({type:"assist_pipeline/pipeline/create"},t)),o=(e,t,s)=>e.callWS(Object.assign({type:"assist_pipeline/pipeline/update",pipeline_id:t},s)),d=e=>e.callWS({type:"assist_pipeline/language/list"})}}]);
//# sourceMappingURL=5047.e261548f717b513b.js.map