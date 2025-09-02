export const __webpack_ids__=["9952"];export const __webpack_modules__={32751:function(t,e,s){s.d(e,{t:()=>o});class a{addFromStorage(t){if(!this._storage[t]){const e=this.storage.getItem(t);e&&(this._storage[t]=JSON.parse(e))}}subscribeChanges(t,e){return this._listeners[t]?this._listeners[t].push(e):this._listeners[t]=[e],()=>{this.unsubscribeChanges(t,e)}}unsubscribeChanges(t,e){if(!(t in this._listeners))return;const s=this._listeners[t].indexOf(e);-1!==s&&this._listeners[t].splice(s,1)}hasKey(t){return t in this._storage}getValue(t){return this._storage[t]}setValue(t,e){const s=this._storage[t];this._storage[t]=e;try{void 0===e?this.storage.removeItem(t):this.storage.setItem(t,JSON.stringify(e))}catch(a){}finally{this._listeners[t]&&this._listeners[t].forEach((t=>t(s,e)))}}constructor(t=window.localStorage){this._storage={},this._listeners={},this.storage=t,this.storage===window.localStorage&&window.addEventListener("storage",(t=>{t.key&&this.hasKey(t.key)&&(this._storage[t.key]=t.newValue?JSON.parse(t.newValue):t.newValue,this._listeners[t.key]&&this._listeners[t.key].forEach((e=>e(t.oldValue?JSON.parse(t.oldValue):t.oldValue,this._storage[t.key]))))}))}}const i={};function o(t){return(e,s)=>{if("object"==typeof s)throw new Error("This decorator does not support this compilation type.");const o=t.storage||"localStorage";let r;o&&o in i?r=i[o]:(r=new a(window[o]),i[o]=r);const l=t.key||String(s);r.addFromStorage(l);const n=!1!==t.subscribe?t=>r.subscribeChanges(l,((e,a)=>{t.requestUpdate(s,e)})):void 0,h=()=>r.hasKey(l)?t.deserializer?t.deserializer(r.getValue(l)):r.getValue(l):void 0,c=(e,a)=>{let i;t.state&&(i=h()),r.setValue(l,t.serializer?t.serializer(a):a),t.state&&e.requestUpdate(s,i)},d=e.performUpdate;if(e.performUpdate=function(){this.__initialized=!0,d.call(this)},t.subscribe){const t=e.connectedCallback,s=e.disconnectedCallback;e.connectedCallback=function(){t.call(this);const e=this;e.__unbsubLocalStorage||(e.__unbsubLocalStorage=n?.(this))},e.disconnectedCallback=function(){s.call(this);this.__unbsubLocalStorage?.(),this.__unbsubLocalStorage=void 0}}const u=Object.getOwnPropertyDescriptor(e,s);let p;if(void 0===u)p={get(){return h()},set(t){(this.__initialized||void 0===h())&&c(this,t)},configurable:!0,enumerable:!0};else{const t=u.set;p={...u,get(){return h()},set(e){(this.__initialized||void 0===h())&&c(this,e),t?.call(this,e)}}}Object.defineProperty(e,s,p)}}},35993:function(t,e,s){s.a(t,(async function(t,e){try{var a=s(73742),i=s(59048),o=s(7616),r=s(31733),l=s(30337),n=s(97862),h=(s(40830),t([l,n]));[l,n]=h.then?(await h)():h;const c="M2.2,16.06L3.88,12L2.2,7.94L6.26,6.26L7.94,2.2L12,3.88L16.06,2.2L17.74,6.26L21.8,7.94L20.12,12L21.8,16.06L17.74,17.74L16.06,21.8L12,20.12L7.94,21.8L6.26,17.74L2.2,16.06M13,17V15H11V17H13M13,13V7H11V13H13Z",d="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z";class u extends i.oi{render(){const t=this.progress||this._result?"accent":this.appearance;return i.dy`
      <ha-button
        .appearance=${t}
        .disabled=${this.disabled}
        .loading=${this.progress}
        .variant=${"success"===this._result?"success":"error"===this._result?"danger":this.variant}
        class=${(0,r.$)({result:!!this._result,success:"success"===this._result,error:"error"===this._result})}
      >
        ${this.iconPath?i.dy`<ha-svg-icon
              .path=${this.iconPath}
              slot="start"
            ></ha-svg-icon>`:i.Ld}

        <slot>${this.label}</slot>
      </ha-button>
      ${this._result?i.dy`
            <div class="progress">
              ${"success"===this._result?i.dy`<ha-svg-icon .path=${d}></ha-svg-icon>`:"error"===this._result?i.dy`<ha-svg-icon .path=${c}></ha-svg-icon>`:i.Ld}
            </div>
          `:i.Ld}
    `}actionSuccess(){this._setResult("success")}actionError(){this._setResult("error")}_setResult(t){this._result=t,setTimeout((()=>{this._result=void 0}),2e3)}constructor(...t){super(...t),this.disabled=!1,this.progress=!1,this.appearance="accent",this.variant="brand"}}u.styles=i.iv`
    :host {
      outline: none;
      display: inline-block;
      position: relative;
    }

    :host([progress]) {
      pointer-events: none;
    }

    .progress {
      bottom: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      position: absolute;
      top: 0;
      width: 100%;
    }

    ha-button {
      width: 100%;
    }

    ha-button.result::part(start),
    ha-button.result::part(end),
    ha-button.result::part(label),
    ha-button.result::part(caret),
    ha-button.result::part(spinner) {
      visibility: hidden;
    }

    ha-svg-icon {
      color: var(--white);
    }
  `,(0,a.__decorate)([(0,o.Cb)()],u.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],u.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],u.prototype,"progress",void 0),(0,a.__decorate)([(0,o.Cb)()],u.prototype,"appearance",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],u.prototype,"iconPath",void 0),(0,a.__decorate)([(0,o.Cb)()],u.prototype,"variant",void 0),(0,a.__decorate)([(0,o.SB)()],u.prototype,"_result",void 0),u=(0,a.__decorate)([(0,o.Mo)("ha-progress-button")],u),e()}catch(c){e(c)}}))},54695:function(t,e,s){s.a(t,(async function(t,a){try{s.r(e),s.d(e,{TTSTryDialog:()=>_});var i=s(73742),o=s(59048),r=s(7616),l=s(32751),n=s(29740),h=s(35993),c=s(99298),d=(s(56719),s(75055)),u=s(81665),p=t([h]);h=(p.then?(await p)():p)[0];const g="M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M10,16.5L16,12L10,7.5V16.5Z";class _ extends o.oi{showDialog(t){this._params=t,this._valid=Boolean(this._defaultMessage)}closeDialog(){this._params=void 0,(0,n.B)(this,"dialog-closed",{dialog:this.localName})}get _defaultMessage(){const t=this._params.language?.substring(0,2),e=this.hass.locale.language.substring(0,2);return t&&this._messages?.[t]?this._messages[t]:t===e?this.hass.localize("ui.dialogs.tts-try.message_example"):""}render(){return this._params?o.dy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        .heading=${(0,c.i)(this.hass,this.hass.localize("ui.dialogs.tts-try.header"))}
      >
        <ha-textarea
          autogrow
          id="message"
          .label=${this.hass.localize("ui.dialogs.tts-try.message")}
          .placeholder=${this.hass.localize("ui.dialogs.tts-try.message_placeholder")}
          .value=${this._defaultMessage}
          @input=${this._inputChanged}
          ?dialogInitialFocus=${!this._defaultMessage}
        >
        </ha-textarea>

        <ha-progress-button
          .progress=${this._loadingExample}
          ?dialogInitialFocus=${Boolean(this._defaultMessage)}
          slot="primaryAction"
          @click=${this._playExample}
          .disabled=${!this._valid}
          .iconPath=${g}
        >
          ${this.hass.localize("ui.dialogs.tts-try.play")}
        </ha-progress-button>
      </ha-dialog>
    `:o.Ld}async _inputChanged(){this._valid=Boolean(this._messageInput?.value)}async _playExample(){const t=this._messageInput?.value;if(!t)return;const e=this._params.engine,s=this._params.language,a=this._params.voice;s&&(this._messages={...this._messages,[s.substring(0,2)]:t}),this._loadingExample=!0;const i=new Audio;let o;i.play();try{o=(await(0,d.aT)(this.hass,{platform:e,message:t,language:s,options:{voice:a}})).path}catch(r){return this._loadingExample=!1,void(0,u.Ys)(this,{text:`Unable to load example. ${r.error||r.body||r}`,warning:!0})}i.src=o,i.addEventListener("canplaythrough",(()=>i.play())),i.addEventListener("playing",(()=>{this._loadingExample=!1})),i.addEventListener("error",(()=>{(0,u.Ys)(this,{title:"Error playing audio."}),this._loadingExample=!1}))}constructor(...t){super(...t),this._loadingExample=!1,this._valid=!1}}_.styles=o.iv`
    ha-dialog {
      --mdc-dialog-max-width: 500px;
    }
    ha-textarea,
    ha-select {
      width: 100%;
    }
    ha-select {
      margin-top: 8px;
    }
    .loading {
      height: 36px;
    }
  `,(0,i.__decorate)([(0,r.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,i.__decorate)([(0,r.SB)()],_.prototype,"_loadingExample",void 0),(0,i.__decorate)([(0,r.SB)()],_.prototype,"_params",void 0),(0,i.__decorate)([(0,r.SB)()],_.prototype,"_valid",void 0),(0,i.__decorate)([(0,r.IO)("#message")],_.prototype,"_messageInput",void 0),(0,i.__decorate)([(0,l.t)({key:"ttsTryMessages",state:!1,subscribe:!1})],_.prototype,"_messages",void 0),_=(0,i.__decorate)([(0,r.Mo)("dialog-tts-try")],_),a()}catch(g){a(g)}}))}};
//# sourceMappingURL=9952.27ef28d5c6e4237e.js.map