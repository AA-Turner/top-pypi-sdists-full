"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["1705"],{61221:function(t,e,i){i.d(e,{o:function(){return n}});i(26847),i(1455),i(27530);var a=i(29740);const s=()=>i.e("9952").then(i.bind(i,54695)),n=(t,e)=>{(0,a.B)(t,"show-dialog",{addHistory:!1,dialogTag:"dialog-tts-try",dialogImport:s,dialogParams:e})}},10929:function(t,e,i){i(26847),i(1455),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=i(28105);i(91337);let r,d,l=t=>t;class p extends s.oi{async focus(){var t;await this.updateComplete;const e=null===(t=this.renderRoot)||void 0===t?void 0:t.querySelector("ha-form");null==e||e.focus()}render(){return(0,s.dy)(r||(r=l`
      <div class="section">
        <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
        </div>
        <ha-form
          .schema=${0}
          .data=${0}
          .hass=${0}
          .computeLabel=${0}
        ></ha-form>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.description"),this._schema(this.supportedLanguages),this.data,this.hass,this._computeLabel)}constructor(...t){super(...t),this._schema=(0,o.Z)((t=>[{name:"",type:"grid",schema:[{name:"name",required:!0,selector:{text:{}}},t?{name:"language",required:!0,selector:{language:{languages:t}}}:{name:"",type:"constant"}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}p.styles=(0,s.iv)(d||(d=l`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      box-sizing: border-box;
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      margin-top: 0;
      margin-bottom: 0;
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"data",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1,type:Array})],p.prototype,"supportedLanguages",void 0),p=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-config")],p)},44618:function(t,e,i){i(26847),i(2394),i(87799),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=i(28105),r=(i(91337),i(29740));let d,l,p=t=>t;class h extends s.oi{render(){var t,e;return(0,s.dy)(d||(d=p`
      <div class="section">
        <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
        </div>
        <ha-form
          .schema=${0}
          .data=${0}
          .hass=${0}
          .computeLabel=${0}
          .computeHelper=${0}
          @supported-languages-changed=${0}
        ></ha-form>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.description"),this._schema(null===(t=this.data)||void 0===t?void 0:t.conversation_engine,null===(e=this.data)||void 0===e?void 0:e.language,this._supportedLanguages),this.data,this.hass,this._computeLabel,this._computeHelper,this._supportedLanguagesChanged)}_supportedLanguagesChanged(t){"*"===t.detail.value&&setTimeout((()=>{const t=Object.assign({},this.data);t.conversation_language="*",(0,r.B)(this,"value-changed",{value:t})}),0),this._supportedLanguages=t.detail.value}constructor(...t){super(...t),this._schema=(0,o.Z)(((t,e,i)=>{const a=[{name:"",type:"grid",schema:[{name:"conversation_engine",required:!0,selector:{conversation_agent:{language:e}}}]}];return"*"!==i&&null!=i&&i.length&&a[0].schema.push({name:"conversation_language",required:!0,selector:{language:{languages:i,no_sort:!0}}}),"conversation.home_assistant"!==t&&a.push({name:"prefer_local_intents",default:!0,selector:{boolean:{}}}),a})),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):"",this._computeHelper=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}_description`):""}}h.styles=(0,s.iv)(l||(l=p`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      box-sizing: border-box;
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      margin-top: 0;
      margin-bottom: 0;
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],h.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],h.prototype,"_supportedLanguages",void 0),h=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-conversation")],h)},11011:function(t,e,i){i(26847),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=i(28105);i(91337);let r,d,l=t=>t;class p extends s.oi{render(){var t;return(0,s.dy)(r||(r=l`
      <div class="section">
        <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
        </div>
        <ha-form
          .schema=${0}
          .data=${0}
          .hass=${0}
          .computeLabel=${0}
          @supported-languages-changed=${0}
        ></ha-form>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.description"),this._schema(null===(t=this.data)||void 0===t?void 0:t.language,this._supportedLanguages),this.data,this.hass,this._computeLabel,this._supportedLanguagesChanged)}_supportedLanguagesChanged(t){this._supportedLanguages=t.detail.value}constructor(...t){super(...t),this._schema=(0,o.Z)(((t,e)=>[{name:"",type:"grid",schema:[{name:"stt_engine",selector:{stt:{language:t}}},null!=e&&e.length?{name:"stt_language",required:!0,selector:{language:{languages:e,no_sort:!0}}}:{name:"",type:"constant"}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}p.styles=(0,s.iv)(d||(d=l`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      box-sizing: border-box;
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      margin-top: 0;
      margin-bottom: 0;
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],p.prototype,"_supportedLanguages",void 0),p=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-stt")],p)},26426:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(1455),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=i(28105),r=i(30337),d=(i(91337),i(61221)),l=t([r]);r=(l.then?(await l)():l)[0];let p,h,c,u=t=>t;class g extends s.oi{render(){var t,e;return(0,s.dy)(p||(p=u`
      <div class="section">
        <div class="content">
          <div class="intro">
          <h3>
            ${0}
          </h3>
          <p>
            ${0}
          </p>
          </div>
          <ha-form
            .schema=${0}
            .data=${0}
            .hass=${0}
            .computeLabel=${0}
            @supported-languages-changed=${0}
          ></ha-form>
        </div>

       ${0}
        </div>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.description"),this._schema(null===(t=this.data)||void 0===t?void 0:t.language,this._supportedLanguages),this.data,this.hass,this._computeLabel,this._supportedLanguagesChanged,null!==(e=this.data)&&void 0!==e&&e.tts_engine?(0,s.dy)(h||(h=u`<div class="footer">
               <ha-button @click=${0}>
                 ${0}
               </ha-button>
             </div>`),this._preview,this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.try_tts")):s.Ld)}async _preview(){if(!this.data)return;const t=this.data.tts_engine,e=this.data.tts_language||void 0,i=this.data.tts_voice||void 0;t&&(0,d.o)(this,{engine:t,language:e,voice:i})}_supportedLanguagesChanged(t){this._supportedLanguages=t.detail.value}constructor(...t){super(...t),this._schema=(0,o.Z)(((t,e)=>[{name:"",type:"grid",schema:[{name:"tts_engine",selector:{tts:{language:t}}},null!=e&&e.length?{name:"tts_language",required:!0,selector:{language:{languages:e,no_sort:!0}}}:{name:"",type:"constant"},{name:"tts_voice",selector:{tts_voice:{}},context:{language:"tts_language",engineId:"tts_engine"},required:!0}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}g.styles=(0,s.iv)(c||(c=u`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
    }
    .content {
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      margin-top: 0;
      margin-bottom: 0;
    }
    .footer {
      border-top: 1px solid var(--divider-color);
      padding: 8px 16px;
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],g.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],g.prototype,"_supportedLanguages",void 0),g=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-tts")],g),e()}catch(p){e(p)}}))},7235:function(t,e,i){i(26847),i(81738),i(6989),i(72489),i(87799),i(1455),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=i(28105);i(91337);var r=i(29740);let d,l,p=t=>t;class h extends s.oi{willUpdate(t){var e,i,a,s;t.has("data")&&(null===(e=t.get("data"))||void 0===e?void 0:e.wake_word_entity)!==(null===(i=this.data)||void 0===i?void 0:i.wake_word_entity)&&(null!==(a=t.get("data"))&&void 0!==a&&a.wake_word_entity&&null!==(s=this.data)&&void 0!==s&&s.wake_word_id&&(0,r.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.data),{},{wake_word_id:void 0})}),this._fetchWakeWords())}render(){return(0,s.dy)(d||(d=p`
      <div class="section">
        <div class="content">
          <div class="intro">
            <h3>
              ${0}
            </h3>
            <p>
              ${0}
            </p>
            <ha-alert alert-type="info">
              ${0}
            </ha-alert>
          </div>
          <ha-form
            .schema=${0}
            .data=${0}
            .hass=${0}
            .computeLabel=${0}
          ></ha-form>
        </div>
      </div>
    `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.description"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.note"),this._schema(this._wakeWords),this.data,this.hass,this._computeLabel)}async _fetchWakeWords(){var t,e;if(this._wakeWords=void 0,null===(t=this.data)||void 0===t||!t.wake_word_entity)return;const i=this.data.wake_word_entity,a=await(s=this.hass,n=i,s.callWS({type:"wake_word/info",entity_id:n}));var s,n,o;this.data.wake_word_entity===i&&(this._wakeWords=a.wake_words,!this.data||null!==(e=this.data)&&void 0!==e&&e.wake_word_id&&this._wakeWords.some((t=>t.id===this.data.wake_word_id))||(0,r.B)(this,"value-changed",{value:Object.assign(Object.assign({},this.data),{},{wake_word_id:null===(o=this._wakeWords[0])||void 0===o?void 0:o.id})}))}constructor(...t){super(...t),this._schema=(0,o.Z)((t=>[{name:"",type:"grid",schema:[{name:"wake_word_entity",selector:{entity:{domain:"wake_word"}}},null!=t&&t.length?{name:"wake_word_id",required:!0,selector:{select:{mode:"dropdown",sort:!0,options:t.map((t=>({value:t.id,label:t.name})))}}}:{name:"",type:"constant"}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}h.styles=(0,s.iv)(l||(l=p`
    .section {
      border: 1px solid var(--divider-color);
      border-radius: 8px;
    }
    .content {
      padding: 16px;
    }
    .intro {
      margin-bottom: 16px;
    }
    h3 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-normal);
      line-height: var(--ha-line-height-condensed);
      margin-top: 0;
      margin-bottom: 4px;
    }
    p {
      color: var(--secondary-text-color);
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      margin-top: 0;
      margin-bottom: 0;
    }
    a {
      color: var(--primary-color);
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],h.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],h.prototype,"_wakeWords",void 0),h=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-wakeword")],h)},30227:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(81738),i(22960),i(21700),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=i(28105),r=i(32518),d=i(83989),l=t([d]);d=(l.then?(await l)():l)[0];let p,h,c,u=t=>t;class g extends s.oi{render(){const t=this._processEvents(this.events);return t?(0,s.dy)(c||(c=u`
      <assist-render-pipeline-run
        .hass=${0}
        .pipelineRun=${0}
      ></assist-render-pipeline-run>
    `),this.hass,t):this.events.length?(0,s.dy)(p||(p=u`<ha-alert alert-type="error">Error showing run</ha-alert>
          <ha-card>
            <ha-expansion-panel>
              <span slot="header">Raw</span>
              <pre>${0}</pre>
            </ha-expansion-panel>
          </ha-card>`),JSON.stringify(this.events,null,2)):(0,s.dy)(h||(h=u`<ha-alert alert-type="warning"
        >There were no events in this run.</ha-alert
      >`))}constructor(...t){super(...t),this._processEvents=(0,o.Z)((t=>{let e;return t.forEach((t=>{e=(0,r.eP)(e,t)})),e}))}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],g.prototype,"events",void 0),g=(0,a.__decorate)([(0,n.Mo)("assist-render-pipeline-events")],g),e()}catch(p){e(p)}}))},83989:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(2394),i(81738),i(29981),i(6989),i(27530);var a=i(73742),s=i(59048),n=i(7616),o=(i(13965),i(22543),i(30337)),r=i(97862),d=(i(86932),i(53303)),l=i(36344),p=i(81665),h=t([o,r,l,d]);[o,r,l,d]=h.then?(await h)():h;let c,u,g,v,_,m,y,f,w,b,$,x,k,L,R,z,W,C,A,S,E,B,M,O=t=>t;const P={pipeline:"Pipeline",language:"Language"},T={engine:"Engine"},j={engine:"Engine"},D={engine:"Engine",language:"Language",intent_input:"Input"},q={engine:"Engine",language:"Language",voice:"Voice",tts_input:"Input"},Z={ready:0,wake_word:1,stt:2,intent:3,tts:4,done:5,error:6},I=(t,e)=>t.init_options?Z[t.init_options.start_stage]<=Z[e]&&Z[e]<=Z[t.init_options.end_stage]:e in t,N=(t,e,i)=>"error"in t&&i===e?(0,s.dy)(c||(c=O`
    <ha-alert alert-type="error">
      ${0} (${0})
    </ha-alert>
  `),t.error.message,t.error.code):"",U=(t,e,i,a="-start")=>{const n=e.events.find((t=>t.type===`${i}`+a)),o=e.events.find((t=>t.type===`${i}-end`));if(!n)return"";if(!o)return"error"in e?(0,s.dy)(u||(u=O`❌`)):(0,s.dy)(g||(g=O` <ha-spinner size="small"></ha-spinner> `));const r=new Date(o.timestamp).getTime()-new Date(n.timestamp).getTime(),l=(0,d.uf)(r/1e3,t.locale,{maximumFractionDigits:2});return(0,s.dy)(v||(v=O`${0}s ✅`),l)},H=(t,e)=>Object.entries(e).map((([e,i])=>(0,s.dy)(_||(_=O`
      <div class="row">
        <div>${0}</div>
        <div>${0}</div>
      </div>
    `),i,t[e]))),F=(t,e)=>{const i={};let a=!1;for(const s in t)s in e||"done"===s||(a=!0,i[s]=t[s]);return a?(0,s.dy)(m||(m=O`<ha-expansion-panel>
        <span slot="header">Raw</span>
        <ha-yaml-editor readOnly autoUpdate .value=${0}></ha-yaml-editor>
      </ha-expansion-panel>`),i):""};class V extends s.oi{render(){var t,e,i,a;const n=this.pipelineRun&&["tts","intent","stt","wake_word"].find((t=>t in this.pipelineRun))||"ready",o=[],r=(this.pipelineRun.init_options&&"text"in this.pipelineRun.init_options.input?this.pipelineRun.init_options.input.text:void 0)||(null===(t=this.pipelineRun)||void 0===t||null===(t=t.stt)||void 0===t||null===(t=t.stt_output)||void 0===t?void 0:t.text)||(null===(e=this.pipelineRun)||void 0===e||null===(e=e.intent)||void 0===e?void 0:e.intent_input);return r&&o.push({from:"user",text:r}),null!==(i=this.pipelineRun)&&void 0!==i&&null!==(i=i.intent)&&void 0!==i&&null!==(i=i.intent_output)&&void 0!==i&&null!==(i=i.response)&&void 0!==i&&null!==(i=i.speech)&&void 0!==i&&null!==(i=i.plain)&&void 0!==i&&i.speech&&o.push({from:"hass",text:this.pipelineRun.intent.intent_output.response.speech.plain.speech}),(0,s.dy)(y||(y=O`
      <ha-card>
        <div class="card-content">
          <div class="row heading">
            <div>Run</div>
            <div>${0}</div>
          </div>

          ${0}
          ${0}
        </div>
      </ha-card>

      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      ${0}
      <ha-card>
        <ha-expansion-panel>
          <span slot="header">Raw</span>
          <ha-yaml-editor
            read-only
            auto-update
            .value=${0}
          ></ha-yaml-editor>
        </ha-expansion-panel>
      </ha-card>
    `),this.pipelineRun.stage,H(this.pipelineRun.run,P),o.length>0?(0,s.dy)(f||(f=O`
                <div class="messages">
                  ${0}
                </div>
                <div style="clear:both"></div>
              `),o.map((({from:t,text:e})=>(0,s.dy)(w||(w=O`
                      <div class=${0}>${0}</div>
                    `),`message ${t}`,e)))):"",N(this.pipelineRun,"ready",n),I(this.pipelineRun,"wake_word")?(0,s.dy)(b||(b=O`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Wake word</span>
                  ${0}
                </div>
                ${0}
              </div>
            </ha-card>
          `),U(this.hass,this.pipelineRun,"wake_word"),this.pipelineRun.wake_word?(0,s.dy)($||($=O`
                      <div class="card-content">
                        ${0}
                        ${0}
                        ${0}
                      </div>
                    `),H(this.pipelineRun.wake_word,j),this.pipelineRun.wake_word.wake_word_output?(0,s.dy)(x||(x=O`<div class="row">
                                <div>Model</div>
                                <div>
                                  ${0}
                                </div>
                              </div>
                              <div class="row">
                                <div>Timestamp</div>
                                <div>
                                  ${0}
                                </div>
                              </div>`),this.pipelineRun.wake_word.wake_word_output.ww_id,this.pipelineRun.wake_word.wake_word_output.timestamp):"",F(this.pipelineRun.wake_word,T)):""):"",N(this.pipelineRun,"wake_word",n),I(this.pipelineRun,"stt")?(0,s.dy)(k||(k=O`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Speech-to-text</span>
                  ${0}
                </div>
                ${0}
              </div>
            </ha-card>
          `),U(this.hass,this.pipelineRun,"stt","-vad-end"),this.pipelineRun.stt?(0,s.dy)(L||(L=O`
                      <div class="card-content">
                        ${0}
                        <div class="row">
                          <div>Language</div>
                          <div>${0}</div>
                        </div>
                        ${0}
                        ${0}
                      </div>
                    `),H(this.pipelineRun.stt,j),this.pipelineRun.stt.metadata.language,this.pipelineRun.stt.stt_output?(0,s.dy)(R||(R=O`<div class="row">
                              <div>Output</div>
                              <div>${0}</div>
                            </div>`),this.pipelineRun.stt.stt_output.text):"",F(this.pipelineRun.stt,j)):""):"",N(this.pipelineRun,"stt",n),I(this.pipelineRun,"intent")?(0,s.dy)(z||(z=O`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Natural Language Processing</span>
                  ${0}
                </div>
                ${0}
              </div>
            </ha-card>
          `),U(this.hass,this.pipelineRun,"intent"),this.pipelineRun.intent?(0,s.dy)(W||(W=O`
                      <div class="card-content">
                        ${0}
                        ${0}
                        <div class="row">
                          <div>Prefer handling locally</div>
                          <div>
                            ${0}
                          </div>
                        </div>
                        <div class="row">
                          <div>Processed locally</div>
                          <div>
                            ${0}
                          </div>
                        </div>
                        ${0}
                      </div>
                    `),H(this.pipelineRun.intent,D),this.pipelineRun.intent.intent_output?(0,s.dy)(C||(C=O`<div class="row">
                                <div>Response type</div>
                                <div>
                                  ${0}
                                </div>
                              </div>
                              ${0}`),this.pipelineRun.intent.intent_output.response.response_type,"error"===this.pipelineRun.intent.intent_output.response.response_type?(0,s.dy)(A||(A=O`<div class="row">
                                    <div>Error code</div>
                                    <div>
                                      ${0}
                                    </div>
                                  </div>`),this.pipelineRun.intent.intent_output.response.data.code):""):"",this.pipelineRun.intent.prefer_local_intents,this.pipelineRun.intent.processed_locally,F(this.pipelineRun.intent,D)):""):"",N(this.pipelineRun,"intent",n),I(this.pipelineRun,"tts")?(0,s.dy)(S||(S=O`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Text-to-speech</span>
                  ${0}
                </div>
                ${0}
              </div>
              ${0}
            </ha-card>
          `),U(this.hass,this.pipelineRun,"tts"),this.pipelineRun.tts?(0,s.dy)(E||(E=O`
                      <div class="card-content">
                        ${0}
                        ${0}
                      </div>
                    `),H(this.pipelineRun.tts,q),F(this.pipelineRun.tts,q)):"",null!==(a=this.pipelineRun)&&void 0!==a&&null!==(a=a.tts)&&void 0!==a&&a.tts_output?(0,s.dy)(B||(B=O`
                    <div class="card-actions">
                      <ha-button @click=${0}>
                        Play Audio
                      </ha-button>
                    </div>
                  `),this._playTTS):""):"",N(this.pipelineRun,"tts",n),this.pipelineRun)}_playTTS(){const t=this.pipelineRun.tts.tts_output.url,e=new Audio(t);e.addEventListener("error",(()=>{(0,p.Ys)(this,{title:"Error",text:"Error playing audio"})})),e.addEventListener("canplaythrough",(()=>{e.play()}))}}V.styles=(0,s.iv)(M||(M=O`
    :host {
      display: block;
    }
    ha-card,
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    .row {
      display: flex;
      justify-content: space-between;
    }
    .row > div:last-child {
      text-align: right;
    }
    ha-expansion-panel {
      padding-left: 8px;
      padding-inline-start: 8px;
      padding-inline-end: initial;
    }
    .card-content ha-expansion-panel {
      padding-left: 0px;
      padding-inline-start: 0px;
      padding-inline-end: initial;
      --expansion-panel-summary-padding: 0px;
      --expansion-panel-content-padding: 0px;
    }
    .heading {
      font-weight: var(--ha-font-weight-medium);
      margin-bottom: 16px;
    }

    .messages {
      margin-top: 8px;
    }

    .message {
      font-size: var(--ha-font-size-l);
      margin: 8px 0;
      padding: 8px;
      border-radius: 15px;
      clear: both;
    }

    .message.user {
      margin-left: 24px;
      margin-inline-start: 24px;
      margin-inline-end: initial;
      float: var(--float-end);
      text-align: right;
      border-bottom-right-radius: 0px;
      background-color: var(--light-primary-color);
      color: var(--text-light-primary-color, var(--primary-text-color));
      direction: var(--direction);
    }

    .message.hass {
      margin-right: 24px;
      margin-inline-end: 24px;
      margin-inline-start: initial;
      float: var(--float-start);
      border-bottom-left-radius: 0px;
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      direction: var(--direction);
    }
  `)),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],V.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],V.prototype,"pipelineRun",void 0),V=(0,a.__decorate)([(0,n.Mo)("assist-render-pipeline-run")],V),e()}catch(c){e(c)}}))},44062:function(t,e,i){i.a(t,(async function(t,a){try{i.r(e),i.d(e,{DialogVoiceAssistantPipelineDetail:function(){return R}});i(26847),i(81738),i(22960),i(72489),i(87799),i(1455),i(44261),i(27530);var s=i(73742),n=i(59048),o=i(7616),r=i(28105),d=i(29740),l=i(41806),p=i(76151),h=i(30337),c=(i(76528),i(91337),i(93795),i(32518)),u=i(77204),g=(i(10929),i(44618),i(11011),i(26426)),v=(i(7235),i(30227)),_=t([h,g,v]);[h,g,v]=_.then?(await _)():_;let m,y,f,w,b,$,x=t=>t;const k="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",L="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";class R extends n.oi{showDialog(t){if(this._params=t,this._error=void 0,this._cloudActive=this._params.cloudActiveSubscription,this._params.pipeline)return this._data=Object.assign({prefer_local_intents:!1},this._params.pipeline),void(this._hideWakeWord=this._params.hideWakeWord||!this._data.wake_word_entity);let e,i;if(this._hideWakeWord=!0,this._cloudActive)for(const a of Object.values(this.hass.entities))if("cloud"===a.platform)if("stt"===(0,p.M)(a.entity_id)){if(e=a.entity_id,i)break}else if("tts"===(0,p.M)(a.entity_id)&&(i=a.entity_id,e))break;this._data={language:(this.hass.config.language||this.hass.locale.language).substring(0,2),stt_engine:e,tts_engine:i}}closeDialog(){this._params=void 0,this._data=void 0,this._hideWakeWord=!1,(0,d.B)(this,"dialog-closed",{dialog:this.localName})}firstUpdated(){this._getSupportedLanguages()}async _getSupportedLanguages(){const{languages:t}=await(0,c.Dy)(this.hass);this._supportedLanguages=t}render(){var t,e,i;if(!this._params||!this._data)return n.Ld;const a=null!==(t=this._params.pipeline)&&void 0!==t&&t.id?this._params.pipeline.name:this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_title");return(0,n.dy)(m||(m=x`
      <ha-dialog
        open
        @closed=${0}
        scrimClickAction
        escapeKeyAction
        .heading=${0}
      >
        <ha-dialog-header slot="heading">
          <ha-icon-button
            slot="navigationIcon"
            dialogAction="cancel"
            .label=${0}
            .path=${0}
          ></ha-icon-button>
          <span slot="title" .title=${0}>${0}</span>
          ${0}
        </ha-dialog-header>
        <div class="content">
          ${0}
          <assist-pipeline-detail-config
            .hass=${0}
            .data=${0}
            .supportedLanguages=${0}
            keys="name,language"
            @value-changed=${0}
            ?dialogInitialFocus=${0}
          ></assist-pipeline-detail-config>
          <assist-pipeline-detail-conversation
            .hass=${0}
            .data=${0}
            keys="conversation_engine,conversation_language,prefer_local_intents"
            @value-changed=${0}
          ></assist-pipeline-detail-conversation>
          ${0}
          <assist-pipeline-detail-stt
            .hass=${0}
            .data=${0}
            keys="stt_engine,stt_language"
            @value-changed=${0}
          ></assist-pipeline-detail-stt>
          <assist-pipeline-detail-tts
            .hass=${0}
            .data=${0}
            keys="tts_engine,tts_language,tts_voice"
            @value-changed=${0}
          ></assist-pipeline-detail-tts>
          ${0}
        </div>
        <ha-button
          slot="primaryAction"
          @click=${0}
          .disabled=${0}
          dialogInitialFocus
        >
          ${0}
        </ha-button>
      </ha-dialog>
    `),this.closeDialog,a,this.hass.localize("ui.common.close"),k,a,a,this._hideWakeWord&&!this._params.hideWakeWord&&this._hasWakeWorkEntities(this.hass.states)?(0,n.dy)(y||(y=x`<ha-button-menu
                slot="actionItems"
                @action=${0}
                @closed=${0}
                menu-corner="END"
                corner="BOTTOM_END"
              >
                <ha-icon-button
                  .path=${0}
                  slot="trigger"
                ></ha-icon-button>
                <ha-list-item>
                  ${0}
                </ha-list-item></ha-button-menu
              >`),this._handleShowWakeWord,l.U,L,this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_streaming_wake_word")):n.Ld,this._error?(0,n.dy)(f||(f=x`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):n.Ld,this.hass,this._data,this._supportedLanguages,this._valueChanged,!(null!==(e=this._params.pipeline)&&void 0!==e&&e.id),this.hass,this._data,this._valueChanged,this._cloudActive||"cloud"!==this._data.tts_engine&&"cloud"!==this._data.stt_engine?n.Ld:(0,n.dy)(w||(w=x`
                <ha-alert alert-type="warning">
                  ${0}
                  <ha-button size="small" href="/config/cloud" slot="action">
                    ${0}
                  </ha-button>
                </ha-alert>
              `),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_message"),this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_action")),this.hass,this._data,this._valueChanged,this.hass,this._data,this._valueChanged,this._hideWakeWord?n.Ld:(0,n.dy)(b||(b=x`<assist-pipeline-detail-wakeword
                .hass=${0}
                .data=${0}
                keys="wake_word_entity,wake_word_id"
                @value-changed=${0}
              ></assist-pipeline-detail-wakeword>`),this.hass,this._data,this._valueChanged),this._updatePipeline,this._submitting,null!==(i=this._params.pipeline)&&void 0!==i&&i.id?this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.update_assistant_action"):this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_action"))}_handleShowWakeWord(){this._hideWakeWord=!1}_valueChanged(t){this._error=void 0;const e={};t.currentTarget.getAttribute("keys").split(",").forEach((i=>{e[i]=t.detail.value[i]})),this._data=Object.assign(Object.assign({},this._data),e)}async _updatePipeline(){this._submitting=!0;try{var t,e,i,a,s,n,o,r,d,l;const p=this._data,h={name:p.name,language:p.language,conversation_engine:p.conversation_engine,conversation_language:null!==(t=p.conversation_language)&&void 0!==t?t:null,prefer_local_intents:null===(e=p.prefer_local_intents)||void 0===e||e,stt_engine:null!==(i=p.stt_engine)&&void 0!==i?i:null,stt_language:null!==(a=p.stt_language)&&void 0!==a?a:null,tts_engine:null!==(s=p.tts_engine)&&void 0!==s?s:null,tts_language:null!==(n=p.tts_language)&&void 0!==n?n:null,tts_voice:null!==(o=p.tts_voice)&&void 0!==o?o:null,wake_word_entity:null!==(r=p.wake_word_entity)&&void 0!==r?r:null,wake_word_id:null!==(d=p.wake_word_id)&&void 0!==d?d:null};null!==(l=this._params.pipeline)&&void 0!==l&&l.id?await this._params.updatePipeline(h):this._params.createPipeline?await this._params.createPipeline(h):console.error("No createPipeline function provided"),this.closeDialog()}catch(p){this._error=(null==p?void 0:p.message)||"Unknown error"}finally{this._submitting=!1}}static get styles(){return[u.yu,(0,n.iv)($||($=x`
        .content > *:not(:last-child) {
          margin-bottom: 16px;
          display: block;
        }
        ha-alert {
          margin-bottom: 16px;
          display: block;
        }
        a {
          text-decoration: none;
        }
      `))]}constructor(...t){super(...t),this._hideWakeWord=!1,this._submitting=!1,this._hasWakeWorkEntities=(0,r.Z)((t=>Object.keys(t).some((t=>t.startsWith("wake_word.")))))}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],R.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_params",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_data",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_hideWakeWord",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_cloudActive",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_submitting",void 0),(0,s.__decorate)([(0,o.SB)()],R.prototype,"_supportedLanguages",void 0),R=(0,s.__decorate)([(0,o.Mo)("dialog-voice-assistant-pipeline-detail")],R),a()}catch(m){a(m)}}))}}]);
//# sourceMappingURL=1705.52d5be22e75db7ac.js.map