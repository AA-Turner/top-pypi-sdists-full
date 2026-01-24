export const __rspack_esm_id="28845";export const __rspack_esm_ids=["28845"];export const __webpack_modules__={85404(e,t,a){a(44114),a(16573),a(78100),a(77936),a(18111),a(61701),a(37467),a(44732),a(79577),a(41549),a(49797),a(49631),a(35623);var i=a(62826),s=a(96196),o=a(44457),n=a(94333),r=a(82286),l=a(69150),d=a(88433),c=a(65063),h=a(74209),p=a(36918);a(38962),a(3587),a(75709);class u extends s.WF{willUpdate(e){this.hasUpdated&&!e.has("pipeline")||(this._conversation=[{who:"hass",text:this.hass.localize("ui.dialogs.voice_command.how_can_i_help")}])}firstUpdated(e){super.firstUpdated(e),this.startListening&&this.pipeline&&this.pipeline.stt_engine&&h.N.isSupported&&this._toggleListening(),setTimeout(()=>this._messageInput.focus(),0)}updated(e){super.updated(e),e.has("_conversation")&&this._scrollMessagesBottom()}disconnectedCallback(){super.disconnectedCallback(),this._audioRecorder?.close(),this._unloadAudio()}render(){const e=!!this.pipeline&&(this.pipeline.prefer_local_intents||!this.hass.states[this.pipeline.conversation_engine]||(0,r.$)(this.hass.states[this.pipeline.conversation_engine],d.ZE.CONTROL)),t=h.N.isSupported,a=this.pipeline?.stt_engine&&!this.disableSpeech;return s.qy` <div class="messages"> ${e?s.s6:s.qy` <ha-alert> ${this.hass.localize("ui.dialogs.voice_command.conversation_no_control")} </ha-alert> `} <div class="spacer"></div> ${this._conversation.map(e=>s.qy` <ha-markdown class="message ${(0,n.H)({error:!!e.error,[e.who]:!0})}" breaks cache .content="${e.text}"> </ha-markdown> `)} </div> <div class="input" slot="primaryAction"> <ha-textfield id="message-input" @keyup="${this._handleKeyUp}" @input="${this._handleInput}" .label="${this.hass.localize("ui.dialogs.voice_command.input_label")}" .iconTrailing="${!0}"> <div slot="trailingIcon"> ${this._showSendButton||!a?s.qy` <ha-icon-button class="listening-icon" .path="${"M2,21L23,12L2,3V10L17,12L2,14V21Z"}" @click="${this._handleSendMessage}" .disabled="${this._processing}" .label="${this.hass.localize("ui.dialogs.voice_command.send_text")}"> </ha-icon-button> `:s.qy` ${this._audioRecorder?.active?s.qy` <div class="bouncer"> <div class="double-bounce1"></div> <div class="double-bounce2"></div> </div> `:s.s6} <div class="listening-icon"> <ha-icon-button .path="${"M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z"}" @click="${this._handleListeningButton}" .disabled="${this._processing}" .label="${this.hass.localize("ui.dialogs.voice_command.start_listening")}"> </ha-icon-button> ${t?null:s.qy` <ha-svg-icon .path="${"M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"}" class="unsupported"></ha-svg-icon> `} </div> `} </div> </ha-textfield> </div> `}async _scrollMessagesBottom(){const e=this._lastChatMessage;if(e.hasUpdated||await e.updateComplete,this._lastChatMessageImage&&!this._lastChatMessageImage.naturalHeight)try{await this._lastChatMessageImage.decode()}catch(e){console.warn("Failed to decode image:",e)}e.getBoundingClientRect().y<this.getBoundingClientRect().top+24||e.scrollIntoView({behavior:"smooth",block:"start"})}_handleKeyUp(e){const t=e.target;!this._processing&&"Enter"===e.key&&t.value&&(this._processText(t.value),t.value="",this._showSendButton=!1)}_handleInput(e){const t=e.target.value;t&&!this._showSendButton?this._showSendButton=!0:!t&&this._showSendButton&&(this._showSendButton=!1)}_handleSendMessage(){this._messageInput.value&&(this._processText(this._messageInput.value.trim()),this._messageInput.value="",this._showSendButton=!1)}_handleListeningButton(e){e.stopPropagation(),e.preventDefault(),this._toggleListening()}async _toggleListening(){h.N.isSupported?this._audioRecorder?.active?this._stopListening():this._startListening():this._showNotSupportedMessage()}_addMessage(e){this._conversation=[...this._conversation,e]}async _showNotSupportedMessage(){this._addMessage({who:"hass",text:s.qy`${this.hass.localize("ui.dialogs.voice_command.not_supported_microphone_browser")} ${this.hass.localize("ui.dialogs.voice_command.not_supported_microphone_documentation",{documentation_link:s.qy`<a target="_blank" rel="noopener noreferrer" href="${(0,p.o)(this.hass,"/docs/configuration/securing/#remote-access")}">${this.hass.localize("ui.dialogs.voice_command.not_supported_microphone_documentation_link")}</a>`})}`})}async _startListening(){this._unloadAudio(),this._processing=!0,this._audioRecorder||(this._audioRecorder=new h.N(e=>{this._audioBuffer?this._audioBuffer.push(e):this._sendAudioChunk(e)})),this._stt_binary_handler_id=void 0,this._audioBuffer=[];const e={who:"user",text:"…"};await this._audioRecorder.start(),this._addMessage(e);const t=this._createAddHassMessageProcessor();try{const a=await(0,l.vU)(this.hass,i=>{if("run-start"===i.type)this._stt_binary_handler_id=i.data.runner_data.stt_binary_handler_id,this._audio=new Audio(i.data.tts_output.url),this._audio.play(),this._audio.addEventListener("ended",()=>{this._unloadAudio(),t.continueConversation&&this._startListening()}),this._audio.addEventListener("pause",this._unloadAudio),this._audio.addEventListener("canplaythrough",()=>this._audio?.play()),this._audio.addEventListener("error",()=>{this._unloadAudio(),(0,c.showAlertDialog)(this,{title:"Error playing audio."})});else if("stt-start"===i.type&&this._audioBuffer){for(const e of this._audioBuffer)this._sendAudioChunk(e);this._audioBuffer=void 0}else"stt-end"===i.type?(this._stt_binary_handler_id=void 0,this._stopListening(),e.text=i.data.stt_output.text,this.requestUpdate("_conversation"),t.addMessage()):i.type.startsWith("intent-")?t.processEvent(i):"run-end"===i.type?(this._stt_binary_handler_id=void 0,a()):"error"===i.type&&(this._unloadAudio(),this._stt_binary_handler_id=void 0,"…"===e.text?(e.text=i.data.message,e.error=!0):t.setError(i.data.message),this._stopListening(),this.requestUpdate("_conversation"),a())},{start_stage:"stt",end_stage:this.pipeline?.tts_engine?"tts":"intent",input:{sample_rate:this._audioRecorder.sampleRate},pipeline:this.pipeline?.id,conversation_id:this._conversationId})}catch(e){await(0,c.showAlertDialog)(this,{title:"Error starting pipeline",text:e.message||e}),this._stopListening()}finally{this._processing=!1}}_stopListening(){if(this._audioRecorder?.stop(),this.requestUpdate("_audioRecorder"),this._stt_binary_handler_id){if(this._audioBuffer)for(const e of this._audioBuffer)this._sendAudioChunk(e);this._sendAudioChunk(new Int16Array),this._stt_binary_handler_id=void 0}this._audioBuffer=void 0}_sendAudioChunk(e){if(this.hass.connection.socket.binaryType="arraybuffer",null==this._stt_binary_handler_id)return;const t=new Uint8Array(1+2*e.length);t[0]=this._stt_binary_handler_id,t.set(new Uint8Array(e.buffer),1),this.hass.connection.socket.send(t)}async _processText(e){this._unloadAudio(),this._processing=!0,this._addMessage({who:"user",text:e});const t=this._createAddHassMessageProcessor();t.addMessage();try{const a=await(0,l.vU)(this.hass,e=>{e.type.startsWith("intent-")&&t.processEvent(e),"intent-end"===e.type&&a(),"error"===e.type&&(t.setError(e.data.message),a())},{start_stage:"intent",input:{text:e},end_stage:"intent",pipeline:this.pipeline?.id,conversation_id:this._conversationId})}catch{t.setError(this.hass.localize("ui.dialogs.voice_command.error"))}finally{this._processing=!1}}_createAddHassMessageProcessor(){let e="";const t=()=>{"…"!==i.hassMessage.text&&(i.hassMessage.text=i.hassMessage.text.substring(0,i.hassMessage.text.length-1),i.hassMessage={who:"hass",text:"…",error:!1},this._addMessage(i.hassMessage))},a={},i={continueConversation:!1,hassMessage:{who:"hass",text:"…",error:!1},addMessage:()=>{this._addMessage(i.hassMessage)},setError:e=>{t(),i.hassMessage.text=e,i.hassMessage.error=!0,this.requestUpdate("_conversation")},processEvent:s=>{if("intent-progress"===s.type&&s.data.chat_log_delta){const o=s.data.chat_log_delta;if(o.role&&(t(),e=o.role),"assistant"===e){if(o.content&&(i.hassMessage.text=i.hassMessage.text.substring(0,i.hassMessage.text.length-1)+o.content+"…",this.requestUpdate("_conversation")),o.tool_calls)for(const e of o.tool_calls)a[e.id]=e}else"tool_result"===e&&a[o.tool_call_id]&&delete a[o.tool_call_id]}else if("intent-end"===s.type){this._conversationId=s.data.intent_output.conversation_id,i.continueConversation=s.data.intent_output.continue_conversation;const e=s.data.intent_output.response.speech?.plain.speech;if(!e)return;"error"===s.data.intent_output.response.response_type?i.setError(e):(i.hassMessage.text=e,this.requestUpdate("_conversation"))}}};return i}constructor(...e){super(...e),this.disableSpeech=!1,this._conversation=[],this._showSendButton=!1,this._processing=!1,this._conversationId=null,this._unloadAudio=()=>{this._audio&&(this._audio.pause(),this._audio.removeAttribute("src"),this._audio=void 0)}}}u.styles=s.AH`
    :host {
      flex: 1;
      display: flex;
      flex-direction: column;
    }
    ha-alert {
      margin-bottom: 8px;
    }
    ha-textfield {
      display: block;
    }
    .messages {
      flex: 1;
      display: block;
      box-sizing: border-box;
      overflow-y: auto;
      max-height: 100%;
      display: flex;
      flex-direction: column;
      padding: 0 12px 16px;
    }
    .spacer {
      flex: 1;
    }
    .message {
      font-size: var(--ha-font-size-l);
      clear: both;
      max-width: -webkit-fill-available;
      overflow-wrap: break-word;
      scroll-margin-top: 24px;
      margin: 8px 0;
      padding: 8px;
      border-radius: var(--ha-border-radius-xl);
    }
    @media all and (max-width: 450px), all and (max-height: 500px) {
      .message {
        font-size: var(--ha-font-size-l);
      }
    }
    .message.user {
      margin-left: 24px;
      margin-inline-start: 24px;
      margin-inline-end: initial;
      align-self: flex-end;
      border-bottom-right-radius: 0px;
      --markdown-link-color: var(--text-primary-color);
      background-color: var(--chat-background-color-user, var(--primary-color));
      color: var(--text-primary-color);
      direction: var(--direction);
    }
    .message.hass {
      margin-right: 24px;
      margin-inline-end: 24px;
      margin-inline-start: initial;
      align-self: flex-start;
      border-bottom-left-radius: 0px;
      background-color: var(
        --chat-background-color-hass,
        var(--secondary-background-color)
      );

      color: var(--primary-text-color);
      direction: var(--direction);
    }
    .message.error {
      background-color: var(--error-color);
      color: var(--text-primary-color);
    }
    ha-markdown {
      --markdown-image-border-radius: calc(var(--ha-border-radius-xl) / 2);
      --markdown-table-border-color: var(--divider-color);
      --markdown-code-background-color: var(--primary-background-color);
      --markdown-code-text-color: var(--primary-text-color);
      --markdown-list-indent: 1.15em;
      &:not(:has(ha-markdown-element)) {
        min-height: 1lh;
        min-width: 1lh;
        flex-shrink: 0;
      }
    }
    .bouncer {
      width: 48px;
      height: 48px;
      position: absolute;
    }
    .double-bounce1,
    .double-bounce2 {
      width: 48px;
      height: 48px;
      border-radius: var(--ha-border-radius-circle);
      background-color: var(--primary-color);
      opacity: 0.2;
      position: absolute;
      top: 0;
      left: 0;
      -webkit-animation: sk-bounce 2s infinite ease-in-out;
      animation: sk-bounce 2s infinite ease-in-out;
    }
    .double-bounce2 {
      -webkit-animation-delay: -1s;
      animation-delay: -1s;
    }
    @-webkit-keyframes sk-bounce {
      0%,
      100% {
        -webkit-transform: scale(0);
      }
      50% {
        -webkit-transform: scale(1);
      }
    }
    @keyframes sk-bounce {
      0%,
      100% {
        transform: scale(0);
        -webkit-transform: scale(0);
      }
      50% {
        transform: scale(1);
        -webkit-transform: scale(1);
      }
    }

    .listening-icon {
      position: relative;
      color: var(--secondary-text-color);
      margin-right: -24px;
      margin-inline-end: -24px;
      margin-inline-start: initial;
      direction: var(--direction);
      transform: scaleX(var(--scale-direction));
    }

    .listening-icon[active] {
      color: var(--primary-color);
    }

    .unsupported {
      color: var(--error-color);
      position: absolute;
      --mdc-icon-size: 16px;
      right: 5px;
      inset-inline-end: 5px;
      inset-inline-start: initial;
      top: 0px;
    }
  `,(0,i.Cg)([(0,o.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,i.Cg)([(0,o.MZ)({attribute:!1})],u.prototype,"pipeline",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean,attribute:"disable-speech"})],u.prototype,"disableSpeech",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean,attribute:!1})],u.prototype,"startListening",void 0),(0,i.Cg)([(0,o.P)("#message-input")],u.prototype,"_messageInput",void 0),(0,i.Cg)([(0,o.P)(".message:last-child")],u.prototype,"_lastChatMessage",void 0),(0,i.Cg)([(0,o.P)(".message:last-child img:last-of-type")],u.prototype,"_lastChatMessageImage",void 0),(0,i.Cg)([(0,o.wk)()],u.prototype,"_conversation",void 0),(0,i.Cg)([(0,o.wk)()],u.prototype,"_showSendButton",void 0),(0,i.Cg)([(0,o.wk)()],u.prototype,"_processing",void 0),u=(0,i.Cg)([(0,o.EM)("ha-assist-chat")],u)},69709(e,t,a){a(18111),a(22489),a(61701),a(18237);var i=a(62826),s=a(96196),o=a(44457),n=a(1420),r=a(30015),l=a.n(r),d=a(1087),c=(a(14603),a(47566),a(98721),a(2209));let h;var p=a(996);const u=e=>s.qy`${e}`,_=new p.G(1e3),g={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class m extends s.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();_.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();_.has(e)&&((0,s.XX)(u((0,n._)(_.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,i)=>(h||(h=(0,c.LV)(new Worker(new URL(a.p+a.u("55640"),a.b)))),h.renderMarkdown(e,t,i)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,s.XX)(u((0,n._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const a=e.firstElementChild?.firstChild?.textContent&&g.reType.exec(e.firstElementChild.firstChild.textContent);if(a){const{type:i}=a.groups,s=document.createElement("ha-alert");s.alertType=g.typeToHaAlert[i.toLowerCase()],s.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===a.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==a.input)),t.parentNode().replaceChild(s,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&a(96175)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,d.r)(this,"content-resize")}}(0,i.Cg)([(0,o.MZ)()],m.prototype,"content",void 0),(0,i.Cg)([(0,o.MZ)({attribute:"allow-svg",type:Boolean})],m.prototype,"allowSvg",void 0),(0,i.Cg)([(0,o.MZ)({attribute:"allow-data-url",type:Boolean})],m.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean})],m.prototype,"breaks",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean,attribute:"lazy-images"})],m.prototype,"lazyImages",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean})],m.prototype,"cache",void 0),m=(0,i.Cg)([(0,o.EM)("ha-markdown-element")],m)},3587(e,t,a){var i=a(62826),s=a(96196),o=a(44457);a(69709);class n extends s.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?s.qy`<ha-markdown-element .content="${this.content}" .allowSvg="${this.allowSvg}" .allowDataUrl="${this.allowDataUrl}" .breaks="${this.breaks}" .lazyImages="${this.lazyImages}" .cache="${this.cache}"></ha-markdown-element>`:s.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}n.styles=s.AH`
    :host {
      display: block;
    }
    ha-markdown-element {
      -ms-user-select: text;
      -webkit-user-select: text;
      -moz-user-select: text;
    }
    ha-markdown-element > *:first-child {
      margin-top: 0;
    }
    ha-markdown-element > *:last-child {
      margin-bottom: 0;
    }
    ha-alert {
      display: block;
      margin: var(--ha-space-1) 0;
    }
    a {
      color: var(--markdown-link-color, var(--primary-color));
    }
    img {
      background-color: var(--markdown-image-background-color);
      border-radius: var(--markdown-image-border-radius);
      max-width: 100%;
    }
    p:first-child > img:first-child {
      vertical-align: top;
    }
    p:first-child > img:last-child {
      vertical-align: top;
    }
    ha-markdown-element > :is(ol, ul) {
      padding-inline-start: var(--markdown-list-indent, revert);
    }
    li {
      &:has(input[type="checkbox"]) {
        list-style: none;
        & > input[type="checkbox"] {
          margin-left: 0;
        }
      }
    }
    svg {
      background-color: var(--markdown-svg-background-color, none);
      color: var(--markdown-svg-color, none);
    }
    code,
    pre {
      background-color: var(--markdown-code-background-color, none);
      border-radius: var(--ha-border-radius-sm);
      color: var(--markdown-code-text-color, inherit);
    }
    code {
      font-size: var(--ha-font-size-s);
      padding: 0.2em 0.4em;
    }
    pre code {
      padding: 0;
    }
    pre {
      padding: var(--ha-space-4);
      overflow: auto;
      line-height: var(--ha-line-height-condensed);
      font-family: var(--ha-font-family-code);
    }
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
      line-height: initial;
    }
    h2 {
      font-size: var(--ha-font-size-xl);
      font-weight: var(--ha-font-weight-bold);
    }
    hr {
      border-color: var(--divider-color);
      border-bottom: none;
      margin: var(--ha-space-4) 0;
    }
    table[role="presentation"] {
      --markdown-table-border-collapse: separate;
      --markdown-table-border-width: attr(border, 0);
      --markdown-table-padding-inline: 0;
      --markdown-table-padding-block: 0;
      th {
        vertical-align: attr(align, center);
      }
      td {
        vertical-align: attr(align, left);
      }
    }
    table {
      border-collapse: var(--markdown-table-border-collapse, collapse);
    }
    div:has(> table) {
      overflow: auto;
    }
    th {
      text-align: var(--markdown-table-text-align, start);
    }
    td,
    th {
      border-width: var(--markdown-table-border-width, 1px);
      border-style: var(--markdown-table-border-style, solid);
      border-color: var(--markdown-table-border-color, var(--divider-color));
      padding-inline: var(--markdown-table-padding-inline, 0.5em);
      padding-block: var(--markdown-table-padding-block, 0.25em);
    }
    blockquote {
      border-left: 4px solid var(--divider-color);
      margin-inline: 0;
      padding-inline: 1em;
    }
  `,(0,i.Cg)([(0,o.MZ)()],n.prototype,"content",void 0),(0,i.Cg)([(0,o.MZ)({attribute:"allow-svg",type:Boolean})],n.prototype,"allowSvg",void 0),(0,i.Cg)([(0,o.MZ)({attribute:"allow-data-url",type:Boolean})],n.prototype,"allowDataUrl",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean})],n.prototype,"breaks",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean,attribute:"lazy-images"})],n.prototype,"lazyImages",void 0),(0,i.Cg)([(0,o.MZ)({type:Boolean})],n.prototype,"cache",void 0),(0,i.Cg)([(0,o.P)("ha-markdown-element")],n.prototype,"_markdownElement",void 0),n=(0,i.Cg)([(0,o.EM)("ha-markdown")],n)},69150(e,t,a){a.d(t,{$$:()=>g,AH:()=>s,NH:()=>p,QC:()=>i,Uc:()=>n,Zr:()=>u,ds:()=>_,hJ:()=>r,mp:()=>d,nx:()=>l,u6:()=>c,vU:()=>o,zn:()=>h});const i=(e,t,a)=>"run-start"===t.type?e={init_options:a,stage:"ready",run:t.data,events:[t],started:new Date(t.timestamp)}:e?((e="wake_word-start"===t.type?{...e,stage:"wake_word",wake_word:{...t.data,done:!1}}:"wake_word-end"===t.type?{...e,wake_word:{...e.wake_word,...t.data,done:!0}}:"stt-start"===t.type?{...e,stage:"stt",stt:{...t.data,done:!1}}:"stt-end"===t.type?{...e,stt:{...e.stt,...t.data,done:!0}}:"intent-start"===t.type?{...e,stage:"intent",intent:{...t.data,done:!1}}:"intent-end"===t.type?{...e,intent:{...e.intent,...t.data,done:!0}}:"tts-start"===t.type?{...e,stage:"tts",tts:{...t.data,done:!1}}:"tts-end"===t.type?{...e,tts:{...e.tts,...t.data,done:!0}}:"run-end"===t.type?{...e,finished:new Date(t.timestamp),stage:"done"}:"error"===t.type?{...e,finished:new Date(t.timestamp),stage:"error",error:t.data}:{...e}).events=[...e.events,t],e):void console.warn("Received unexpected event before receiving session",t),s=(e,t,a)=>{let s;const n=o(e,e=>{s=i(s,e,a),"run-end"!==e.type&&"error"!==e.type||n.then(e=>e()),s&&t(s)},a);return n},o=(e,t,a)=>e.connection.subscribeMessage(t,{...a,type:"assist_pipeline/run"}),n=(e,t)=>e.callWS({type:"assist_pipeline/pipeline_debug/list",pipeline_id:t}),r=(e,t,a)=>e.callWS({type:"assist_pipeline/pipeline_debug/get",pipeline_id:t,pipeline_run_id:a}),l=e=>e.callWS({type:"assist_pipeline/pipeline/list"}),d=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:t}),c=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/create",...t}),h=(e,t,a)=>e.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:t,...a}),p=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/set_preferred",pipeline_id:t}),u=(e,t)=>e.callWS({type:"assist_pipeline/pipeline/delete",pipeline_id:t}),_=e=>e.callWS({type:"assist_pipeline/language/list"}),g=e=>e.callWS({type:"assist_pipeline/device/list"})},88433(e,t,a){if(a.d(t,{RW:()=>n,ZE:()=>s,e1:()=>r,vc:()=>o}),59509==a.j)var i=a(44537);var s=function(e){return e[e.CONTROL=1]="CONTROL",e}({});const o=(e,t,a)=>e.callWS({type:"conversation/agent/list",language:t,country:a}),n=(e,t,a,s)=>e.callWS({type:"conversation/agent/homeassistant/debug",sentences:(0,i.e)(t),language:a,device_id:s}),r=(e,t,a)=>e.callWS({type:"conversation/agent/homeassistant/language_scores",language:t,country:a})},74209(e,t,a){a.d(t,{N:()=>i});a(14603),a(47566),a(98721);class i{get active(){return this._active}get sampleRate(){return this._context?.sampleRate}static get isSupported(){return window.isSecureContext&&(window.AudioContext||window.webkitAudioContext)}async start(){if(this._context&&this._stream&&this._source&&this._recorder)this._stream.getTracks()[0].enabled=!0,await this._context.resume(),this._active=!0;else try{await this._createContext()}catch(e){console.error(e),this._active=!1}}async stop(){this._active=!1,this._stream&&(this._stream.getTracks()[0].enabled=!1),await(this._context?.suspend())}close(){this._active=!1,this._stream?.getTracks()[0].stop(),this._recorder&&(this._recorder.port.onmessage=null),this._source?.disconnect(),this._context?.close(),this._stream=void 0,this._source=void 0,this._recorder=void 0,this._context=void 0}async _createContext(){const e=new(AudioContext||webkitAudioContext);this._stream=await navigator.mediaDevices.getUserMedia({audio:!0}),await e.audioWorklet.addModule(new URL(a.p+a.u("33921"),a.b)),this._context=e,this._source=this._context.createMediaStreamSource(this._stream),this._recorder=new AudioWorkletNode(this._context,"recorder-worklet"),this._recorder.port.onmessage=e=>{this._active&&this._callback(e.data)},this._active=!0,this._source.connect(this._recorder)}constructor(e){this._active=!1,this._callback=e}}},996(e,t,a){a.d(t,{G:()=>i});class i{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}},36918(e,t,a){a.d(t,{o:()=>i});const i=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},96175(e,t,a){var i={"./ha-icon-prev":["89133","61982"],"./ha-icon-button-toolbar":["9882","52074","76775"],"./ha-alert":["38962","19695"],"./ha-icon-button-toggle":["62501","77254"],"./ha-svg-icon.ts":["67094"],"./ha-alert.ts":["38962","19695"],"./ha-icon":["88945","51146"],"./ha-icon-next.ts":["43661","63902"],"./ha-qr-code.ts":["60543","51343","62740"],"./ha-icon-overflow-menu.ts":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-toggle.ts":["62501","77254"],"./ha-icon-button-group":["39826","13647"],"./ha-svg-icon":["67094"],"./ha-icon-button-prev":["45100","99197"],"./ha-icon-button.ts":["26300"],"./ha-icon-overflow-menu":["75248","46095","52074","22016","29499","56297"],"./ha-icon-button-arrow-next":["99028","54101"],"./ha-icon-button-prev.ts":["45100","99197"],"./ha-icon-picker":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-button-toolbar.ts":["9882","52074","76775"],"./ha-icon-button-arrow-prev.ts":["90248","17041"],"./ha-icon-button-next":["25440","81049"],"./ha-icon-next":["43661","63902"],"./ha-icon-picker.ts":["64138","44533","7199","46095","92769","52074","44966","80445","87234"],"./ha-icon-prev.ts":["89133","61982"],"./ha-icon-button-arrow-prev":["90248","17041"],"./ha-icon-button-next.ts":["25440","81049"],"./ha-icon.ts":["88945","51146"],"./ha-qr-code":["60543","51343","62740"],"./ha-icon-button":["26300"],"./ha-icon-button-group.ts":["39826","13647"],"./ha-icon-button-arrow-next.ts":["99028","54101"]};function s(e){if(!a.o(i,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=i[e],s=t[0];return Promise.all(t.slice(1).map(a.e)).then(function(){return a(s)})}s.keys=()=>Object.keys(i),s.id=96175,e.exports=s}};
//# sourceMappingURL=28845.f21869db92384c4f.js.map