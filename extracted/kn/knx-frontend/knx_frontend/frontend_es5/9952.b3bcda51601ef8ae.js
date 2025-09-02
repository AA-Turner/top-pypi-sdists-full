"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9952"],{32751:function(t,e,s){s.d(e,{t:function(){return o}});s(40777),s(2394),s(81738),s(22960),s(21700),s(87799),s(64510);class a{addFromStorage(t){if(!this._storage[t]){const e=this.storage.getItem(t);e&&(this._storage[t]=JSON.parse(e))}}subscribeChanges(t,e){return this._listeners[t]?this._listeners[t].push(e):this._listeners[t]=[e],()=>{this.unsubscribeChanges(t,e)}}unsubscribeChanges(t,e){if(!(t in this._listeners))return;const s=this._listeners[t].indexOf(e);-1!==s&&this._listeners[t].splice(s,1)}hasKey(t){return t in this._storage}getValue(t){return this._storage[t]}setValue(t,e){const s=this._storage[t];this._storage[t]=e;try{void 0===e?this.storage.removeItem(t):this.storage.setItem(t,JSON.stringify(e))}catch(a){}finally{this._listeners[t]&&this._listeners[t].forEach((t=>t(s,e)))}}constructor(t=window.localStorage){this._storage={},this._listeners={},this.storage=t,this.storage===window.localStorage&&window.addEventListener("storage",(t=>{t.key&&this.hasKey(t.key)&&(this._storage[t.key]=t.newValue?JSON.parse(t.newValue):t.newValue,this._listeners[t.key]&&this._listeners[t.key].forEach((e=>e(t.oldValue?JSON.parse(t.oldValue):t.oldValue,this._storage[t.key]))))}))}}const i={};function o(t){return(e,s)=>{if("object"==typeof s)throw new Error("This decorator does not support this compilation type.");const o=t.storage||"localStorage";let r;o&&o in i?r=i[o]:(r=new a(window[o]),i[o]=r);const n=t.key||String(s);r.addFromStorage(n);const l=!1!==t.subscribe?t=>r.subscribeChanges(n,((e,a)=>{t.requestUpdate(s,e)})):void 0,h=()=>r.hasKey(n)?t.deserializer?t.deserializer(r.getValue(n)):r.getValue(n):void 0,c=(e,a)=>{let i;t.state&&(i=h()),r.setValue(n,t.serializer?t.serializer(a):a),t.state&&e.requestUpdate(s,i)},d=e.performUpdate;if(e.performUpdate=function(){this.__initialized=!0,d.call(this)},t.subscribe){const t=e.connectedCallback,s=e.disconnectedCallback;e.connectedCallback=function(){t.call(this);const e=this;e.__unbsubLocalStorage||(e.__unbsubLocalStorage=null==l?void 0:l(this))},e.disconnectedCallback=function(){var t;s.call(this);const e=this;null===(t=e.__unbsubLocalStorage)||void 0===t||t.call(e),e.__unbsubLocalStorage=void 0}}const u=Object.getOwnPropertyDescriptor(e,s);let g;if(void 0===u)g={get(){return h()},set(t){(this.__initialized||void 0===h())&&c(this,t)},configurable:!0,enumerable:!0};else{const t=u.set;g=Object.assign(Object.assign({},u),{},{get(){return h()},set(e){(this.__initialized||void 0===h())&&c(this,e),null==t||t.call(this,e)}})}Object.defineProperty(e,s,g)}}},35993:function(t,e,s){s.a(t,(async function(t,e){try{s(26847),s(27530);var a=s(73742),i=s(59048),o=s(7616),r=s(31733),n=s(30337),l=s(97862),h=(s(40830),t([n,l]));[n,l]=h.then?(await h)():h;let c,d,u,g,p,_,b=t=>t;const v="M2.2,16.06L3.88,12L2.2,7.94L6.26,6.26L7.94,2.2L12,3.88L16.06,2.2L17.74,6.26L21.8,7.94L20.12,12L21.8,16.06L17.74,17.74L16.06,21.8L12,20.12L7.94,21.8L6.26,17.74L2.2,16.06M13,17V15H11V17H13M13,13V7H11V13H13Z",y="M9,20.42L2.79,14.21L5.62,11.38L9,14.77L18.88,4.88L21.71,7.71L9,20.42Z";class m extends i.oi{render(){const t=this.progress||this._result?"accent":this.appearance;return(0,i.dy)(c||(c=b`
      <ha-button
        .appearance=${0}
        .disabled=${0}
        .loading=${0}
        .variant=${0}
        class=${0}
      >
        ${0}

        <slot>${0}</slot>
      </ha-button>
      ${0}
    `),t,this.disabled,this.progress,"success"===this._result?"success":"error"===this._result?"danger":this.variant,(0,r.$)({result:!!this._result,success:"success"===this._result,error:"error"===this._result}),this.iconPath?(0,i.dy)(d||(d=b`<ha-svg-icon
              .path=${0}
              slot="start"
            ></ha-svg-icon>`),this.iconPath):i.Ld,this.label,this._result?(0,i.dy)(u||(u=b`
            <div class="progress">
              ${0}
            </div>
          `),"success"===this._result?(0,i.dy)(g||(g=b`<ha-svg-icon .path=${0}></ha-svg-icon>`),y):"error"===this._result?(0,i.dy)(p||(p=b`<ha-svg-icon .path=${0}></ha-svg-icon>`),v):i.Ld):i.Ld)}actionSuccess(){this._setResult("success")}actionError(){this._setResult("error")}_setResult(t){this._result=t,setTimeout((()=>{this._result=void 0}),2e3)}constructor(...t){super(...t),this.disabled=!1,this.progress=!1,this.appearance="accent",this.variant="brand"}}m.styles=(0,i.iv)(_||(_=b`
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
  `)),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"label",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean})],m.prototype,"disabled",void 0),(0,a.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],m.prototype,"progress",void 0),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"appearance",void 0),(0,a.__decorate)([(0,o.Cb)({attribute:!1})],m.prototype,"iconPath",void 0),(0,a.__decorate)([(0,o.Cb)()],m.prototype,"variant",void 0),(0,a.__decorate)([(0,o.SB)()],m.prototype,"_result",void 0),m=(0,a.__decorate)([(0,o.Mo)("ha-progress-button")],m),e()}catch(c){e(c)}}))},54695:function(t,e,s){s.a(t,(async function(t,a){try{s.r(e),s.d(e,{TTSTryDialog:function(){return y}});s(26847),s(87799),s(1455),s(27530);var i=s(73742),o=s(59048),r=s(7616),n=s(32751),l=s(29740),h=s(35993),c=s(99298),d=(s(56719),s(75055)),u=s(81665),g=t([h]);h=(g.then?(await g)():g)[0];let p,_,b=t=>t;const v="M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M10,16.5L16,12L10,7.5V16.5Z";class y extends o.oi{showDialog(t){this._params=t,this._valid=Boolean(this._defaultMessage)}closeDialog(){this._params=void 0,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}get _defaultMessage(){var t,e;const s=null===(t=this._params.language)||void 0===t?void 0:t.substring(0,2),a=this.hass.locale.language.substring(0,2);return s&&null!==(e=this._messages)&&void 0!==e&&e[s]?this._messages[s]:s===a?this.hass.localize("ui.dialogs.tts-try.message_example"):""}render(){return this._params?(0,o.dy)(p||(p=b`
      <ha-dialog
        open
        @closed=${0}
        .heading=${0}
      >
        <ha-textarea
          autogrow
          id="message"
          .label=${0}
          .placeholder=${0}
          .value=${0}
          @input=${0}
          ?dialogInitialFocus=${0}
        >
        </ha-textarea>

        <ha-progress-button
          .progress=${0}
          ?dialogInitialFocus=${0}
          slot="primaryAction"
          @click=${0}
          .disabled=${0}
          .iconPath=${0}
        >
          ${0}
        </ha-progress-button>
      </ha-dialog>
    `),this.closeDialog,(0,c.i)(this.hass,this.hass.localize("ui.dialogs.tts-try.header")),this.hass.localize("ui.dialogs.tts-try.message"),this.hass.localize("ui.dialogs.tts-try.message_placeholder"),this._defaultMessage,this._inputChanged,!this._defaultMessage,this._loadingExample,Boolean(this._defaultMessage),this._playExample,!this._valid,v,this.hass.localize("ui.dialogs.tts-try.play")):o.Ld}async _inputChanged(){var t;this._valid=Boolean(null===(t=this._messageInput)||void 0===t?void 0:t.value)}async _playExample(){var t;const e=null===(t=this._messageInput)||void 0===t?void 0:t.value;if(!e)return;const s=this._params.engine,a=this._params.language,i=this._params.voice;a&&(this._messages=Object.assign(Object.assign({},this._messages),{},{[a.substring(0,2)]:e})),this._loadingExample=!0;const o=new Audio;let r;o.play();try{r=(await(0,d.aT)(this.hass,{platform:s,message:e,language:a,options:{voice:i}})).path}catch(n){return this._loadingExample=!1,void(0,u.Ys)(this,{text:`Unable to load example. ${n.error||n.body||n}`,warning:!0})}o.src=r,o.addEventListener("canplaythrough",(()=>o.play())),o.addEventListener("playing",(()=>{this._loadingExample=!1})),o.addEventListener("error",(()=>{(0,u.Ys)(this,{title:"Error playing audio."}),this._loadingExample=!1}))}constructor(...t){super(...t),this._loadingExample=!1,this._valid=!1}}y.styles=(0,o.iv)(_||(_=b`
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
  `)),(0,i.__decorate)([(0,r.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,i.__decorate)([(0,r.SB)()],y.prototype,"_loadingExample",void 0),(0,i.__decorate)([(0,r.SB)()],y.prototype,"_params",void 0),(0,i.__decorate)([(0,r.SB)()],y.prototype,"_valid",void 0),(0,i.__decorate)([(0,r.IO)("#message")],y.prototype,"_messageInput",void 0),(0,i.__decorate)([(0,n.t)({key:"ttsTryMessages",state:!1,subscribe:!1})],y.prototype,"_messages",void 0),y=(0,i.__decorate)([(0,r.Mo)("dialog-tts-try")],y),a()}catch(p){a(p)}}))}}]);
//# sourceMappingURL=9952.b3bcda51601ef8ae.js.map