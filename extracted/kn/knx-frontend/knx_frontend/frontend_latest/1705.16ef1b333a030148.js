export const __webpack_ids__=["1705"];export const __webpack_modules__={61221:function(t,e,i){i.d(e,{o:()=>n});var a=i(29740);const s=()=>i.e("9952").then(i.bind(i,54695)),n=(t,e)=>{(0,a.B)(t,"show-dialog",{addHistory:!1,dialogTag:"dialog-tts-try",dialogImport:s,dialogParams:e})}},10929:function(t,e,i){var a=i(73742),s=i(59048),n=i(7616),o=i(28105);i(91337);class r extends s.oi{async focus(){await this.updateComplete;const t=this.renderRoot?.querySelector("ha-form");t?.focus()}render(){return s.dy`
      <div class="section">
        <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.config.description")}
          </p>
        </div>
        <ha-form
          .schema=${this._schema(this.supportedLanguages)}
          .data=${this.data}
          .hass=${this.hass}
          .computeLabel=${this._computeLabel}
        ></ha-form>
      </div>
    `}constructor(...t){super(...t),this._schema=(0,o.Z)((t=>[{name:"",type:"grid",schema:[{name:"name",required:!0,selector:{text:{}}},t?{name:"language",required:!0,selector:{language:{languages:t}}}:{name:"",type:"constant"}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}r.styles=s.iv`
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
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],r.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],r.prototype,"data",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1,type:Array})],r.prototype,"supportedLanguages",void 0),r=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-config")],r)},44618:function(t,e,i){var a=i(73742),s=i(59048),n=i(7616),o=i(28105),r=(i(91337),i(29740));class d extends s.oi{render(){return s.dy`
      <div class="section">
        <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.conversation.description")}
          </p>
        </div>
        <ha-form
          .schema=${this._schema(this.data?.conversation_engine,this.data?.language,this._supportedLanguages)}
          .data=${this.data}
          .hass=${this.hass}
          .computeLabel=${this._computeLabel}
          .computeHelper=${this._computeHelper}
          @supported-languages-changed=${this._supportedLanguagesChanged}
        ></ha-form>
      </div>
    `}_supportedLanguagesChanged(t){"*"===t.detail.value&&setTimeout((()=>{const t={...this.data};t.conversation_language="*",(0,r.B)(this,"value-changed",{value:t})}),0),this._supportedLanguages=t.detail.value}constructor(...t){super(...t),this._schema=(0,o.Z)(((t,e,i)=>{const a=[{name:"",type:"grid",schema:[{name:"conversation_engine",required:!0,selector:{conversation_agent:{language:e}}}]}];return"*"!==i&&i?.length&&a[0].schema.push({name:"conversation_language",required:!0,selector:{language:{languages:i,no_sort:!0}}}),"conversation.home_assistant"!==t&&a.push({name:"prefer_local_intents",default:!0,selector:{boolean:{}}}),a})),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):"",this._computeHelper=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}_description`):""}}d.styles=s.iv`
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
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],d.prototype,"_supportedLanguages",void 0),d=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-conversation")],d)},11011:function(t,e,i){var a=i(73742),s=i(59048),n=i(7616),o=i(28105);i(91337);class r extends s.oi{render(){return s.dy`
      <div class="section">
        <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.stt.description")}
          </p>
        </div>
        <ha-form
          .schema=${this._schema(this.data?.language,this._supportedLanguages)}
          .data=${this.data}
          .hass=${this.hass}
          .computeLabel=${this._computeLabel}
          @supported-languages-changed=${this._supportedLanguagesChanged}
        ></ha-form>
      </div>
    `}_supportedLanguagesChanged(t){this._supportedLanguages=t.detail.value}constructor(...t){super(...t),this._schema=(0,o.Z)(((t,e)=>[{name:"",type:"grid",schema:[{name:"stt_engine",selector:{stt:{language:t}}},e?.length?{name:"stt_language",required:!0,selector:{language:{languages:e,no_sort:!0}}}:{name:"",type:"constant"}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}r.styles=s.iv`
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
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],r.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],r.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],r.prototype,"_supportedLanguages",void 0),r=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-stt")],r)},26426:function(t,e,i){i.a(t,(async function(t,e){try{var a=i(73742),s=i(59048),n=i(7616),o=i(28105),r=i(30337),d=(i(91337),i(61221)),p=t([r]);r=(p.then?(await p)():p)[0];class l extends s.oi{render(){return s.dy`
      <div class="section">
        <div class="content">
          <div class="intro">
          <h3>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.title")}
          </h3>
          <p>
            ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.tts.description")}
          </p>
          </div>
          <ha-form
            .schema=${this._schema(this.data?.language,this._supportedLanguages)}
            .data=${this.data}
            .hass=${this.hass}
            .computeLabel=${this._computeLabel}
            @supported-languages-changed=${this._supportedLanguagesChanged}
          ></ha-form>
        </div>

       ${this.data?.tts_engine?s.dy`<div class="footer">
               <ha-button @click=${this._preview}>
                 ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.try_tts")}
               </ha-button>
             </div>`:s.Ld}
        </div>
      </div>
    `}async _preview(){if(!this.data)return;const t=this.data.tts_engine,e=this.data.tts_language||void 0,i=this.data.tts_voice||void 0;t&&(0,d.o)(this,{engine:t,language:e,voice:i})}_supportedLanguagesChanged(t){this._supportedLanguages=t.detail.value}constructor(...t){super(...t),this._schema=(0,o.Z)(((t,e)=>[{name:"",type:"grid",schema:[{name:"tts_engine",selector:{tts:{language:t}}},e?.length?{name:"tts_language",required:!0,selector:{language:{languages:e,no_sort:!0}}}:{name:"",type:"constant"},{name:"tts_voice",selector:{tts_voice:{}},context:{language:"tts_language",engineId:"tts_engine"},required:!0}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}l.styles=s.iv`
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
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],l.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],l.prototype,"_supportedLanguages",void 0),l=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-tts")],l),e()}catch(l){e(l)}}))},7235:function(t,e,i){var a=i(73742),s=i(59048),n=i(7616),o=i(28105);i(91337);var r=i(29740);class d extends s.oi{willUpdate(t){t.has("data")&&t.get("data")?.wake_word_entity!==this.data?.wake_word_entity&&(t.get("data")?.wake_word_entity&&this.data?.wake_word_id&&(0,r.B)(this,"value-changed",{value:{...this.data,wake_word_id:void 0}}),this._fetchWakeWords())}render(){return s.dy`
      <div class="section">
        <div class="content">
          <div class="intro">
            <h3>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.title")}
            </h3>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.description")}
            </p>
            <ha-alert alert-type="info">
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.steps.wakeword.note")}
            </ha-alert>
          </div>
          <ha-form
            .schema=${this._schema(this._wakeWords)}
            .data=${this.data}
            .hass=${this.hass}
            .computeLabel=${this._computeLabel}
          ></ha-form>
        </div>
      </div>
    `}async _fetchWakeWords(){if(this._wakeWords=void 0,!this.data?.wake_word_entity)return;const t=this.data.wake_word_entity,e=await(i=this.hass,a=t,i.callWS({type:"wake_word/info",entity_id:a}));var i,a;this.data.wake_word_entity===t&&(this._wakeWords=e.wake_words,!this.data||this.data?.wake_word_id&&this._wakeWords.some((t=>t.id===this.data.wake_word_id))||(0,r.B)(this,"value-changed",{value:{...this.data,wake_word_id:this._wakeWords[0]?.id}}))}constructor(...t){super(...t),this._schema=(0,o.Z)((t=>[{name:"",type:"grid",schema:[{name:"wake_word_entity",selector:{entity:{domain:"wake_word"}}},t?.length?{name:"wake_word_id",required:!0,selector:{select:{mode:"dropdown",sort:!0,options:t.map((t=>({value:t.id,label:t.name})))}}}:{name:"",type:"constant"}]}])),this._computeLabel=t=>t.name?this.hass.localize(`ui.panel.config.voice_assistants.assistants.pipeline.detail.form.${t.name}`):""}}d.styles=s.iv`
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
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"data",void 0),(0,a.__decorate)([(0,n.SB)()],d.prototype,"_wakeWords",void 0),d=(0,a.__decorate)([(0,n.Mo)("assist-pipeline-detail-wakeword")],d)},30227:function(t,e,i){i.a(t,(async function(t,e){try{var a=i(73742),s=i(59048),n=i(7616),o=i(28105),r=i(32518),d=i(83989),p=t([d]);d=(p.then?(await p)():p)[0];class l extends s.oi{render(){const t=this._processEvents(this.events);return t?s.dy`
      <assist-render-pipeline-run
        .hass=${this.hass}
        .pipelineRun=${t}
      ></assist-render-pipeline-run>
    `:this.events.length?s.dy`<ha-alert alert-type="error">Error showing run</ha-alert>
          <ha-card>
            <ha-expansion-panel>
              <span slot="header">Raw</span>
              <pre>${JSON.stringify(this.events,null,2)}</pre>
            </ha-expansion-panel>
          </ha-card>`:s.dy`<ha-alert alert-type="warning"
        >There were no events in this run.</ha-alert
      >`}constructor(...t){super(...t),this._processEvents=(0,o.Z)((t=>{let e;return t.forEach((t=>{e=(0,r.eP)(e,t)})),e}))}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],l.prototype,"events",void 0),l=(0,a.__decorate)([(0,n.Mo)("assist-render-pipeline-events")],l),e()}catch(l){e(l)}}))},83989:function(t,e,i){i.a(t,(async function(t,e){try{var a=i(73742),s=i(59048),n=i(7616),o=(i(13965),i(22543),i(30337)),r=i(97862),d=(i(86932),i(53303)),p=i(36344),l=i(81665),h=t([o,r,p,d]);[o,r,p,d]=h.then?(await h)():h;const c={pipeline:"Pipeline",language:"Language"},u={engine:"Engine"},g={engine:"Engine"},_={engine:"Engine",language:"Language",intent_input:"Input"},v={engine:"Engine",language:"Language",voice:"Voice",tts_input:"Input"},m={ready:0,wake_word:1,stt:2,intent:3,tts:4,done:5,error:6},y=(t,e)=>t.init_options?m[t.init_options.start_stage]<=m[e]&&m[e]<=m[t.init_options.end_stage]:e in t,w=(t,e,i)=>"error"in t&&i===e?s.dy`
    <ha-alert alert-type="error">
      ${t.error.message} (${t.error.code})
    </ha-alert>
  `:"",f=(t,e,i,a="-start")=>{const n=e.events.find((t=>t.type===`${i}`+a)),o=e.events.find((t=>t.type===`${i}-end`));if(!n)return"";if(!o)return"error"in e?s.dy`❌`:s.dy` <ha-spinner size="small"></ha-spinner> `;const r=new Date(o.timestamp).getTime()-new Date(n.timestamp).getTime(),p=(0,d.uf)(r/1e3,t.locale,{maximumFractionDigits:2});return s.dy`${p}s ✅`},b=(t,e)=>Object.entries(e).map((([e,i])=>s.dy`
      <div class="row">
        <div>${i}</div>
        <div>${t[e]}</div>
      </div>
    `)),$=(t,e)=>{const i={};let a=!1;for(const s in t)s in e||"done"===s||(a=!0,i[s]=t[s]);return a?s.dy`<ha-expansion-panel>
        <span slot="header">Raw</span>
        <ha-yaml-editor readOnly autoUpdate .value=${i}></ha-yaml-editor>
      </ha-expansion-panel>`:""};class x extends s.oi{render(){const t=this.pipelineRun&&["tts","intent","stt","wake_word"].find((t=>t in this.pipelineRun))||"ready",e=[],i=(this.pipelineRun.init_options&&"text"in this.pipelineRun.init_options.input?this.pipelineRun.init_options.input.text:void 0)||this.pipelineRun?.stt?.stt_output?.text||this.pipelineRun?.intent?.intent_input;return i&&e.push({from:"user",text:i}),this.pipelineRun?.intent?.intent_output?.response?.speech?.plain?.speech&&e.push({from:"hass",text:this.pipelineRun.intent.intent_output.response.speech.plain.speech}),s.dy`
      <ha-card>
        <div class="card-content">
          <div class="row heading">
            <div>Run</div>
            <div>${this.pipelineRun.stage}</div>
          </div>

          ${b(this.pipelineRun.run,c)}
          ${e.length>0?s.dy`
                <div class="messages">
                  ${e.map((({from:t,text:e})=>s.dy`
                      <div class=${`message ${t}`}>${e}</div>
                    `))}
                </div>
                <div style="clear:both"></div>
              `:""}
        </div>
      </ha-card>

      ${w(this.pipelineRun,"ready",t)}
      ${y(this.pipelineRun,"wake_word")?s.dy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Wake word</span>
                  ${f(this.hass,this.pipelineRun,"wake_word")}
                </div>
                ${this.pipelineRun.wake_word?s.dy`
                      <div class="card-content">
                        ${b(this.pipelineRun.wake_word,g)}
                        ${this.pipelineRun.wake_word.wake_word_output?s.dy`<div class="row">
                                <div>Model</div>
                                <div>
                                  ${this.pipelineRun.wake_word.wake_word_output.ww_id}
                                </div>
                              </div>
                              <div class="row">
                                <div>Timestamp</div>
                                <div>
                                  ${this.pipelineRun.wake_word.wake_word_output.timestamp}
                                </div>
                              </div>`:""}
                        ${$(this.pipelineRun.wake_word,u)}
                      </div>
                    `:""}
              </div>
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"wake_word",t)}
      ${y(this.pipelineRun,"stt")?s.dy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Speech-to-text</span>
                  ${f(this.hass,this.pipelineRun,"stt","-vad-end")}
                </div>
                ${this.pipelineRun.stt?s.dy`
                      <div class="card-content">
                        ${b(this.pipelineRun.stt,g)}
                        <div class="row">
                          <div>Language</div>
                          <div>${this.pipelineRun.stt.metadata.language}</div>
                        </div>
                        ${this.pipelineRun.stt.stt_output?s.dy`<div class="row">
                              <div>Output</div>
                              <div>${this.pipelineRun.stt.stt_output.text}</div>
                            </div>`:""}
                        ${$(this.pipelineRun.stt,g)}
                      </div>
                    `:""}
              </div>
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"stt",t)}
      ${y(this.pipelineRun,"intent")?s.dy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Natural Language Processing</span>
                  ${f(this.hass,this.pipelineRun,"intent")}
                </div>
                ${this.pipelineRun.intent?s.dy`
                      <div class="card-content">
                        ${b(this.pipelineRun.intent,_)}
                        ${this.pipelineRun.intent.intent_output?s.dy`<div class="row">
                                <div>Response type</div>
                                <div>
                                  ${this.pipelineRun.intent.intent_output.response.response_type}
                                </div>
                              </div>
                              ${"error"===this.pipelineRun.intent.intent_output.response.response_type?s.dy`<div class="row">
                                    <div>Error code</div>
                                    <div>
                                      ${this.pipelineRun.intent.intent_output.response.data.code}
                                    </div>
                                  </div>`:""}`:""}
                        <div class="row">
                          <div>Prefer handling locally</div>
                          <div>
                            ${this.pipelineRun.intent.prefer_local_intents}
                          </div>
                        </div>
                        <div class="row">
                          <div>Processed locally</div>
                          <div>
                            ${this.pipelineRun.intent.processed_locally}
                          </div>
                        </div>
                        ${$(this.pipelineRun.intent,_)}
                      </div>
                    `:""}
              </div>
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"intent",t)}
      ${y(this.pipelineRun,"tts")?s.dy`
            <ha-card>
              <div class="card-content">
                <div class="row heading">
                  <span>Text-to-speech</span>
                  ${f(this.hass,this.pipelineRun,"tts")}
                </div>
                ${this.pipelineRun.tts?s.dy`
                      <div class="card-content">
                        ${b(this.pipelineRun.tts,v)}
                        ${$(this.pipelineRun.tts,v)}
                      </div>
                    `:""}
              </div>
              ${this.pipelineRun?.tts?.tts_output?s.dy`
                    <div class="card-actions">
                      <ha-button @click=${this._playTTS}>
                        Play Audio
                      </ha-button>
                    </div>
                  `:""}
            </ha-card>
          `:""}
      ${w(this.pipelineRun,"tts",t)}
      <ha-card>
        <ha-expansion-panel>
          <span slot="header">Raw</span>
          <ha-yaml-editor
            read-only
            auto-update
            .value=${this.pipelineRun}
          ></ha-yaml-editor>
        </ha-expansion-panel>
      </ha-card>
    `}_playTTS(){const t=this.pipelineRun.tts.tts_output.url,e=new Audio(t);e.addEventListener("error",(()=>{(0,l.Ys)(this,{title:"Error",text:"Error playing audio"})})),e.addEventListener("canplaythrough",(()=>{e.play()}))}}x.styles=s.iv`
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
  `,(0,a.__decorate)([(0,n.Cb)({attribute:!1})],x.prototype,"hass",void 0),(0,a.__decorate)([(0,n.Cb)({attribute:!1})],x.prototype,"pipelineRun",void 0),x=(0,a.__decorate)([(0,n.Mo)("assist-render-pipeline-run")],x),e()}catch(c){e(c)}}))},44062:function(t,e,i){i.a(t,(async function(t,a){try{i.r(e),i.d(e,{DialogVoiceAssistantPipelineDetail:()=>w});var s=i(73742),n=i(59048),o=i(7616),r=i(28105),d=i(29740),p=i(41806),l=i(76151),h=i(30337),c=(i(76528),i(91337),i(93795),i(32518)),u=i(77204),g=(i(10929),i(44618),i(11011),i(26426)),_=(i(7235),i(30227)),v=t([h,g,_]);[h,g,_]=v.then?(await v)():v;const m="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",y="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z";class w extends n.oi{showDialog(t){if(this._params=t,this._error=void 0,this._cloudActive=this._params.cloudActiveSubscription,this._params.pipeline)return this._data={prefer_local_intents:!1,...this._params.pipeline},void(this._hideWakeWord=this._params.hideWakeWord||!this._data.wake_word_entity);let e,i;if(this._hideWakeWord=!0,this._cloudActive)for(const a of Object.values(this.hass.entities))if("cloud"===a.platform)if("stt"===(0,l.M)(a.entity_id)){if(e=a.entity_id,i)break}else if("tts"===(0,l.M)(a.entity_id)&&(i=a.entity_id,e))break;this._data={language:(this.hass.config.language||this.hass.locale.language).substring(0,2),stt_engine:e,tts_engine:i}}closeDialog(){this._params=void 0,this._data=void 0,this._hideWakeWord=!1,(0,d.B)(this,"dialog-closed",{dialog:this.localName})}firstUpdated(){this._getSupportedLanguages()}async _getSupportedLanguages(){const{languages:t}=await(0,c.Dy)(this.hass);this._supportedLanguages=t}render(){if(!this._params||!this._data)return n.Ld;const t=this._params.pipeline?.id?this._params.pipeline.name:this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_title");return n.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        .heading=${t}
      >
        <ha-dialog-header slot="heading">
          <ha-icon-button
            slot="navigationIcon"
            dialogAction="cancel"
            .label=${this.hass.localize("ui.common.close")}
            .path=${m}
          ></ha-icon-button>
          <span slot="title" .title=${t}>${t}</span>
          ${this._hideWakeWord&&!this._params.hideWakeWord&&this._hasWakeWorkEntities(this.hass.states)?n.dy`<ha-button-menu
                slot="actionItems"
                @action=${this._handleShowWakeWord}
                @closed=${p.U}
                menu-corner="END"
                corner="BOTTOM_END"
              >
                <ha-icon-button
                  .path=${y}
                  slot="trigger"
                ></ha-icon-button>
                <ha-list-item>
                  ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_streaming_wake_word")}
                </ha-list-item></ha-button-menu
              >`:n.Ld}
        </ha-dialog-header>
        <div class="content">
          ${this._error?n.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:n.Ld}
          <assist-pipeline-detail-config
            .hass=${this.hass}
            .data=${this._data}
            .supportedLanguages=${this._supportedLanguages}
            keys="name,language"
            @value-changed=${this._valueChanged}
            ?dialogInitialFocus=${!this._params.pipeline?.id}
          ></assist-pipeline-detail-config>
          <assist-pipeline-detail-conversation
            .hass=${this.hass}
            .data=${this._data}
            keys="conversation_engine,conversation_language,prefer_local_intents"
            @value-changed=${this._valueChanged}
          ></assist-pipeline-detail-conversation>
          ${this._cloudActive||"cloud"!==this._data.tts_engine&&"cloud"!==this._data.stt_engine?n.Ld:n.dy`
                <ha-alert alert-type="warning">
                  ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_message")}
                  <ha-button size="small" href="/config/cloud" slot="action">
                    ${this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.no_cloud_action")}
                  </ha-button>
                </ha-alert>
              `}
          <assist-pipeline-detail-stt
            .hass=${this.hass}
            .data=${this._data}
            keys="stt_engine,stt_language"
            @value-changed=${this._valueChanged}
          ></assist-pipeline-detail-stt>
          <assist-pipeline-detail-tts
            .hass=${this.hass}
            .data=${this._data}
            keys="tts_engine,tts_language,tts_voice"
            @value-changed=${this._valueChanged}
          ></assist-pipeline-detail-tts>
          ${this._hideWakeWord?n.Ld:n.dy`<assist-pipeline-detail-wakeword
                .hass=${this.hass}
                .data=${this._data}
                keys="wake_word_entity,wake_word_id"
                @value-changed=${this._valueChanged}
              ></assist-pipeline-detail-wakeword>`}
        </div>
        <ha-button
          slot="primaryAction"
          @click=${this._updatePipeline}
          .disabled=${this._submitting}
          dialogInitialFocus
        >
          ${this._params.pipeline?.id?this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.update_assistant_action"):this.hass.localize("ui.panel.config.voice_assistants.assistants.pipeline.detail.add_assistant_action")}
        </ha-button>
      </ha-dialog>
    `}_handleShowWakeWord(){this._hideWakeWord=!1}_valueChanged(t){this._error=void 0;const e={};t.currentTarget.getAttribute("keys").split(",").forEach((i=>{e[i]=t.detail.value[i]})),this._data={...this._data,...e}}async _updatePipeline(){this._submitting=!0;try{const t=this._data,e={name:t.name,language:t.language,conversation_engine:t.conversation_engine,conversation_language:t.conversation_language??null,prefer_local_intents:t.prefer_local_intents??!0,stt_engine:t.stt_engine??null,stt_language:t.stt_language??null,tts_engine:t.tts_engine??null,tts_language:t.tts_language??null,tts_voice:t.tts_voice??null,wake_word_entity:t.wake_word_entity??null,wake_word_id:t.wake_word_id??null};this._params.pipeline?.id?await this._params.updatePipeline(e):this._params.createPipeline?await this._params.createPipeline(e):console.error("No createPipeline function provided"),this.closeDialog()}catch(t){this._error=t?.message||"Unknown error"}finally{this._submitting=!1}}static get styles(){return[u.yu,n.iv`
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
      `]}constructor(...t){super(...t),this._hideWakeWord=!1,this._submitting=!1,this._hasWakeWorkEntities=(0,r.Z)((t=>Object.keys(t).some((t=>t.startsWith("wake_word.")))))}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],w.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_params",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_data",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_hideWakeWord",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_cloudActive",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_submitting",void 0),(0,s.__decorate)([(0,o.SB)()],w.prototype,"_supportedLanguages",void 0),w=(0,s.__decorate)([(0,o.Mo)("dialog-voice-assistant-pipeline-detail")],w),a()}catch(m){a(m)}}))}};
//# sourceMappingURL=1705.16ef1b333a030148.js.map