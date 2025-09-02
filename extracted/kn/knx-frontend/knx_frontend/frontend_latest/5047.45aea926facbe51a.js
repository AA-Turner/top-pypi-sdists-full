export const __webpack_ids__=["5047"];export const __webpack_modules__={75972:function(e,t,i){i.a(e,(async function(e,s){try{i.d(t,{u:()=>d});var a=i(57900),r=i(28105),n=e([a]);a=(n.then?(await n)():n)[0];const d=(e,t)=>{try{return l(t)?.of(e)??e}catch{return e}},l=(0,r.Z)((e=>new Intl.DisplayNames(e.language,{type:"language",fallback:"code"})));s()}catch(d){s(d)}}))},69187:function(e,t,i){i.a(e,(async function(e,t){try{var s=i(73742),a=i(59048),r=i(7616),n=i(29740),d=i(41806),l=i(75972),p=i(32518),o=(i(93795),i(29490),e([l]));l=(o.then?(await o)():o)[0];const c="preferred",u="last_used";class h extends a.oi{get _default(){return this.includeLastUsed?u:c}render(){if(!this._pipelines)return a.Ld;const e=this.value??this._default;return a.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.pipeline-picker.pipeline")}
        .value=${e}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.includeLastUsed?a.dy`
              <ha-list-item .value=${u}>
                ${this.hass.localize("ui.components.pipeline-picker.last_used")}
              </ha-list-item>
            `:null}
        <ha-list-item .value=${c}>
          ${this.hass.localize("ui.components.pipeline-picker.preferred",{preferred:this._pipelines.find((e=>e.id===this._preferredPipeline))?.name})}
        </ha-list-item>
        ${this._pipelines.map((e=>a.dy`<ha-list-item .value=${e.id}>
              ${e.name}
              (${(0,l.u)(e.language,this.hass.locale)})
            </ha-list-item>`))}
      </ha-select>
    `}firstUpdated(e){super.firstUpdated(e),(0,p.SC)(this.hass).then((e=>{this._pipelines=e.pipelines,this._preferredPipeline=e.preferred_pipeline}))}_changed(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===this._default||(this.value=t.value===this._default?void 0:t.value,(0,n.B)(this,"value-changed",{value:this.value}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.includeLastUsed=!1,this._preferredPipeline=null}}h.styles=a.iv`
    ha-select {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,r.Cb)()],h.prototype,"value",void 0),(0,s.__decorate)([(0,r.Cb)()],h.prototype,"label",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],h.prototype,"disabled",void 0),(0,s.__decorate)([(0,r.Cb)({type:Boolean})],h.prototype,"required",void 0),(0,s.__decorate)([(0,r.Cb)({attribute:!1})],h.prototype,"includeLastUsed",void 0),(0,s.__decorate)([(0,r.SB)()],h.prototype,"_pipelines",void 0),(0,s.__decorate)([(0,r.SB)()],h.prototype,"_preferredPipeline",void 0),h=(0,s.__decorate)([(0,r.Mo)("ha-assist-pipeline-picker")],h),t()}catch(c){t(c)}}))},83019:function(e,t,i){i.a(e,(async function(e,s){try{i.r(t),i.d(t,{HaAssistPipelineSelector:()=>p});var a=i(73742),r=i(59048),n=i(7616),d=i(69187),l=e([d]);d=(l.then?(await l)():l)[0];class p extends r.oi{render(){return r.dy`
      <ha-assist-pipeline-picker
        .hass=${this.hass}
        .value=${this.value}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .includeLastUsed=${Boolean(this.selector.assist_pipeline?.include_last_used)}
      ></ha-assist-pipeline-picker>
    `}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}p.styles=r.iv`
    ha-conversation-agent-picker {
      width: 100%;
    }
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"selector",void 0),(0,a.__decorate)([(0,n.Cb)()],p.prototype,"value",void 0),(0,a.__decorate)([(0,n.Cb)()],p.prototype,"label",void 0),(0,a.__decorate)([(0,n.Cb)()],p.prototype,"helper",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],p.prototype,"disabled",void 0),(0,a.__decorate)([(0,n.Cb)({type:Boolean})],p.prototype,"required",void 0),p=(0,a.__decorate)([(0,n.Mo)("ha-selector-assist_pipeline")],p),s()}catch(p){s(p)}}))},32518:function(e,t,i){i.d(t,{Dy:()=>p,PA:()=>n,SC:()=>r,Xp:()=>a,af:()=>l,eP:()=>s,jZ:()=>d});const s=(e,t,i)=>"run-start"===t.type?e={init_options:i,stage:"ready",run:t.data,events:[t]}:e?((e="wake_word-start"===t.type?{...e,stage:"wake_word",wake_word:{...t.data,done:!1}}:"wake_word-end"===t.type?{...e,wake_word:{...e.wake_word,...t.data,done:!0}}:"stt-start"===t.type?{...e,stage:"stt",stt:{...t.data,done:!1}}:"stt-end"===t.type?{...e,stt:{...e.stt,...t.data,done:!0}}:"intent-start"===t.type?{...e,stage:"intent",intent:{...t.data,done:!1}}:"intent-end"===t.type?{...e,intent:{...e.intent,...t.data,done:!0}}:"tts-start"===t.type?{...e,stage:"tts",tts:{...t.data,done:!1}}:"tts-end"===t.type?{...e,tts:{...e.tts,...t.data,done:!0}}:"run-end"===t.type?{...e,stage:"done"}:"error"===t.type?{...e,stage:"error",error:t.data}:{...e}).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),a=(e,t,i)=>e.connection.subscribeMessage(t,{...i,type:"assist_pipeline/run"}),r=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),n=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),d=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/create",...t}),l=(e,t,i)=>e.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:t,...i}),p=e=>e.callWS({type:"assist_pipeline/language/list"})}};
//# sourceMappingURL=5047.45aea926facbe51a.js.map