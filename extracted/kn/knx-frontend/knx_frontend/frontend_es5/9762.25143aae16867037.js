"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["9762"],{13539:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{Bt:function(){return c}});i(39710);var a=i(57900),o=i(3574),n=i(43956),r=t([a]);a=(r.then?(await r)():r)[0];const l=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],c=t=>t.first_weekday===n.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(t.language).weekInfo.firstDay%7:(0,o.L)(t.language)%7:l.includes(t.first_weekday)?l.indexOf(t.first_weekday):1;s()}catch(l){s(l)}}))},60495:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{G:function(){return c}});var a=i(57900),o=i(28105),n=i(58713),r=t([a,n]);[a,n]=r.then?(await r)():r;const l=(0,o.Z)((t=>new Intl.RelativeTimeFormat(t.language,{numeric:"auto"}))),c=(t,e,i,s=!0)=>{const a=(0,n.W)(t,i,e);return s?l(e).format(a.value,a.unit):Intl.NumberFormat(e.language,{style:"unit",unit:a.unit,unitDisplay:"long"}).format(Math.abs(a.value))};s()}catch(l){s(l)}}))},4757:function(t,e,i){i.d(e,{X:function(){return s}});const s=(t,e,i)=>(void 0!==i&&(i=!!i),t.hasAttribute(e)?!!i||(t.removeAttribute(e),!1):!1!==i&&(t.setAttribute(e,""),!0))},27087:function(t,e,i){i.d(e,{T:function(){return a}});i(64455),i(32192);const s=/^(\w+)\.(\w+)$/,a=t=>s.test(t)},75972:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{u:function(){return r}});var a=i(57900),o=i(28105),n=t([a]);a=(n.then?(await n)():n)[0];const r=(t,e)=>{try{var i,s;return null!==(i=null===(s=l(e))||void 0===s?void 0:s.of(t))&&void 0!==i?i:t}catch(a){return t}},l=(0,o.Z)((t=>new Intl.DisplayNames(t.language,{type:"language",fallback:"code"})));s()}catch(r){s(r)}}))},31132:function(t,e,i){i.d(e,{f:function(){return s}});const s=t=>t.charAt(0).toUpperCase()+t.slice(1)},74002:function(t,e,i){i.d(e,{v:function(){return s}});i(26847),i(65640),i(28660),i(64455),i(60142),i(56303),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(27530);const s=(t,e)=>{if(t===e)return!0;if(t&&e&&"object"==typeof t&&"object"==typeof e){if(t.constructor!==e.constructor)return!1;let i,a;if(Array.isArray(t)){if(a=t.length,a!==e.length)return!1;for(i=a;0!=i--;)if(!s(t[i],e[i]))return!1;return!0}if(t instanceof Map&&e instanceof Map){if(t.size!==e.size)return!1;for(i of t.entries())if(!e.has(i[0]))return!1;for(i of t.entries())if(!s(i[1],e.get(i[0])))return!1;return!0}if(t instanceof Set&&e instanceof Set){if(t.size!==e.size)return!1;for(i of t.entries())if(!e.has(i[0]))return!1;return!0}if(ArrayBuffer.isView(t)&&ArrayBuffer.isView(e)){if(a=t.length,a!==e.length)return!1;for(i=a;0!=i--;)if(t[i]!==e[i])return!1;return!0}if(t.constructor===RegExp)return t.source===e.source&&t.flags===e.flags;if(t.valueOf!==Object.prototype.valueOf)return t.valueOf()===e.valueOf();if(t.toString!==Object.prototype.toString)return t.toString()===e.toString();const o=Object.keys(t);if(a=o.length,a!==Object.keys(e).length)return!1;for(i=a;0!=i--;)if(!Object.prototype.hasOwnProperty.call(e,o[i]))return!1;for(i=a;0!=i--;){const a=o[i];if(!s(t[a],e[a]))return!1}return!0}return t!=t&&e!=e}},58713:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{W:function(){return p}});i(87799);var a=i(7722),o=i(66233),n=i(41238),r=i(13539),l=t([r]);r=(l.then?(await l)():l)[0];const d=1e3,h=60,u=60*h;function p(t,e=Date.now(),i,s={}){const l=Object.assign(Object.assign({},_),s||{}),c=(+t-+e)/d;if(Math.abs(c)<l.second)return{value:Math.round(c),unit:"second"};const p=c/h;if(Math.abs(p)<l.minute)return{value:Math.round(p),unit:"minute"};const g=c/u;if(Math.abs(g)<l.hour)return{value:Math.round(g),unit:"hour"};const v=new Date(t),f=new Date(e);v.setHours(0,0,0,0),f.setHours(0,0,0,0);const y=(0,a.j)(v,f);if(0===y)return{value:Math.round(g),unit:"hour"};if(Math.abs(y)<l.day)return{value:y,unit:"day"};const m=(0,r.Bt)(i),b=(0,o.z)(v,{weekStartsOn:m}),w=(0,o.z)(f,{weekStartsOn:m}),$=(0,n.p)(b,w);if(0===$)return{value:y,unit:"day"};if(Math.abs($)<l.week)return{value:$,unit:"week"};const C=v.getFullYear()-f.getFullYear(),k=12*C+v.getMonth()-f.getMonth();return 0===k?{value:$,unit:"week"}:Math.abs(k)<l.month||0===C?{value:k,unit:"month"}:{value:Math.round(C),unit:"year"}}const _={second:45,minute:45,hour:22,day:5,week:4,month:11};s()}catch(c){s(c)}}))},62335:function(t,e,i){i(26847),i(87799),i(27530);var s=i(73742),a=i(27885),o=i(67522),n=i(23533),r=i(7046),l=i(59048),c=i(7616);let d,h,u,p,_=t=>t;class g extends a.g{renderOutline(){return this.filled?(0,l.dy)(d||(d=_`<span class="filled"></span>`)):super.renderOutline()}getContainerClasses(){return Object.assign(Object.assign({},super.getContainerClasses()),{},{active:this.active})}renderPrimaryContent(){return(0,l.dy)(h||(h=_`
      <span class="leading icon" aria-hidden="true">
        ${0}
      </span>
      <span class="label">${0}</span>
      <span class="touch"></span>
      <span class="trailing leading icon" aria-hidden="true">
        ${0}
      </span>
    `),this.renderLeadingIcon(),this.label,this.renderTrailingIcon())}renderTrailingIcon(){return(0,l.dy)(u||(u=_`<slot name="trailing-icon"></slot>`))}constructor(...t){super(...t),this.filled=!1,this.active=!1}}g.styles=[n.W,r.W,o.W,(0,l.iv)(p||(p=_`
      :host {
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-assist-chip-container-shape: var(
          --ha-assist-chip-container-shape,
          16px
        );
        --md-assist-chip-outline-color: var(--outline-color);
        --md-assist-chip-label-text-weight: 400;
      }
      /** Material 3 doesn't have a filled chip, so we have to make our own **/
      .filled {
        display: flex;
        pointer-events: none;
        border-radius: inherit;
        inset: 0;
        position: absolute;
        background-color: var(--ha-assist-chip-filled-container-color);
      }
      /** Set the size of mdc icons **/
      ::slotted([slot="icon"]),
      ::slotted([slot="trailing-icon"]) {
        display: flex;
        --mdc-icon-size: var(--md-input-chip-icon-size, 18px);
        font-size: var(--_label-text-size) !important;
      }

      .trailing.icon ::slotted(*),
      .trailing.icon svg {
        margin-inline-end: unset;
        margin-inline-start: var(--_icon-label-space);
      }
      ::before {
        background: var(--ha-assist-chip-container-color, transparent);
        opacity: var(--ha-assist-chip-container-opacity, 1);
      }
      :where(.active)::before {
        background: var(--ha-assist-chip-active-container-color);
        opacity: var(--ha-assist-chip-active-container-opacity);
      }
      .label {
        font-family: var(--ha-font-family-body);
      }
    `))],(0,s.__decorate)([(0,c.Cb)({type:Boolean,reflect:!0})],g.prototype,"filled",void 0),(0,s.__decorate)([(0,c.Cb)({type:Boolean})],g.prototype,"active",void 0),g=(0,s.__decorate)([(0,c.Mo)("ha-assist-chip")],g)},86352:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{C:function(){return b}});var a=i(57900),o=(i(26847),i(18574),i(81738),i(6989),i(27530),i(73742)),n=i(59048),r=i(7616),l=i(28105),c=i(29740),d=i(41806),h=i(75972),u=i(92949),p=i(18447),_=(i(93795),i(29490),t([a,h]));[a,h]=_.then?(await _)():_;let g,v,f,y,m=t=>t;const b=(t,e,i,s)=>{let a=[];if(e){const e=p.o.translations;a=t.map((t=>{var i;let s=null===(i=e[t])||void 0===i?void 0:i.nativeName;if(!s)try{s=new Intl.DisplayNames(t,{type:"language",fallback:"code"}).of(t)}catch(a){s=t}return{value:t,label:s}}))}else s&&(a=t.map((t=>({value:t,label:(0,h.u)(t,s)}))));return!i&&s&&a.sort(((t,e)=>(0,u.fe)(t.label,e.label,s.language))),a};class w extends n.oi{firstUpdated(t){super.firstUpdated(t),this._computeDefaultLanguageOptions()}updated(t){super.updated(t);const e=t.has("hass")&&this.hass&&t.get("hass")&&t.get("hass").locale.language!==this.hass.locale.language;if(t.has("languages")||t.has("value")||e){var i,s;if(this._select.layoutOptions(),this.disabled||this._select.value===this.value||(0,c.B)(this,"value-changed",{value:this._select.value}),!this.value)return;const t=this._getLanguagesOptions(null!==(i=this.languages)&&void 0!==i?i:this._defaultLanguages,this.nativeName,this.noSort,null===(s=this.hass)||void 0===s?void 0:s.locale).findIndex((t=>t.value===this.value));-1===t&&(this.value=void 0),e&&this._select.select(t)}}_computeDefaultLanguageOptions(){this._defaultLanguages=Object.keys(p.o.translations)}render(){var t,e,i,s,a,o,r;const l=this._getLanguagesOptions(null!==(t=this.languages)&&void 0!==t?t:this._defaultLanguages,this.nativeName,this.noSort,null===(e=this.hass)||void 0===e?void 0:e.locale),c=null!==(i=this.value)&&void 0!==i?i:this.required&&!this.disabled?null===(s=l[0])||void 0===s?void 0:s.value:this.value;return(0,n.dy)(g||(g=m`
      <ha-select
        .label=${0}
        .value=${0}
        .required=${0}
        .disabled=${0}
        @selected=${0}
        @closed=${0}
        fixedMenuPosition
        naturalMenuWidth
        .inlineArrow=${0}
      >
        ${0}
      </ha-select>
    `),null!==(a=this.label)&&void 0!==a?a:(null===(o=this.hass)||void 0===o?void 0:o.localize("ui.components.language-picker.language"))||"Language",c||"",this.required,this.disabled,this._changed,d.U,this.inlineArrow,0===l.length?(0,n.dy)(v||(v=m`<ha-list-item value=""
              >${0}</ha-list-item
            >`),(null===(r=this.hass)||void 0===r?void 0:r.localize("ui.components.language-picker.no_languages"))||"No languages"):l.map((t=>(0,n.dy)(f||(f=m`
                <ha-list-item .value=${0}
                  >${0}</ha-list-item
                >
              `),t.value,t.label))))}_changed(t){const e=t.target;this.disabled||""===e.value||e.value===this.value||(this.value=e.value,(0,c.B)(this,"value-changed",{value:this.value}))}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this.nativeName=!1,this.noSort=!1,this.inlineArrow=!1,this._defaultLanguages=[],this._getLanguagesOptions=(0,l.Z)(b)}}w.styles=(0,n.iv)(y||(y=m`
    ha-select {
      width: 100%;
    }
  `)),(0,o.__decorate)([(0,r.Cb)()],w.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],w.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array})],w.prototype,"languages",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],w.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],w.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],w.prototype,"required",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"native-name",type:Boolean})],w.prototype,"nativeName",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"no-sort",type:Boolean})],w.prototype,"noSort",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"inline-arrow",type:Boolean})],w.prototype,"inlineArrow",void 0),(0,o.__decorate)([(0,r.SB)()],w.prototype,"_defaultLanguages",void 0),(0,o.__decorate)([(0,r.IO)("ha-select")],w.prototype,"_select",void 0),w=(0,o.__decorate)([(0,r.Mo)("ha-language-picker")],w),s()}catch(g){s(g)}}))},51431:function(t,e,i){i(26847),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(90380),i(10051)),l=i(91646),c=i(67419);let d;class h extends r.v2{connectedCallback(){super.connectedCallback(),this.addEventListener("close-menu",this._handleCloseMenu)}_handleCloseMenu(t){var e,i;t.detail.reason.kind===c.GB.KEYDOWN&&t.detail.reason.key===c.KC.ESCAPE||null===(e=(i=t.detail.initiator).clickAction)||void 0===e||e.call(i,t.detail.initiator)}}h.styles=[l.W,(0,a.iv)(d||(d=(t=>t)`
      :host {
        --md-sys-color-surface-container: var(--card-background-color);
      }
    `))],h=(0,s.__decorate)([(0,o.Mo)("ha-md-menu")],h);let u,p,_=t=>t;class g extends a.oi{get items(){return this._menu.items}focus(){var t;this._menu.open?this._menu.focus():null===(t=this._triggerButton)||void 0===t||t.focus()}render(){return(0,a.dy)(u||(u=_`
      <div @click=${0}>
        <slot name="trigger" @slotchange=${0}></slot>
      </div>
      <ha-md-menu
        .positioning=${0}
        .hasOverflow=${0}
        @opening=${0}
        @closing=${0}
      >
        <slot></slot>
      </ha-md-menu>
    `),this._handleClick,this._setTriggerAria,this.positioning,this.hasOverflow,this._handleOpening,this._handleClosing)}_handleOpening(){(0,n.B)(this,"opening",void 0,{composed:!1})}_handleClosing(){(0,n.B)(this,"closing",void 0,{composed:!1})}_handleClick(){this.disabled||(this._menu.anchorElement=this,this._menu.open?this._menu.close():this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"], ha-assist-chip[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...t){super(...t),this.disabled=!1,this.hasOverflow=!1}}g.styles=(0,a.iv)(p||(p=_`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `)),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],g.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)()],g.prototype,"positioning",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,attribute:"has-overflow"})],g.prototype,"hasOverflow",void 0),(0,s.__decorate)([(0,o.IO)("ha-md-menu",!0)],g.prototype,"_menu",void 0),g=(0,s.__decorate)([(0,o.Mo)("ha-md-button-menu")],g)},20455:function(t,e,i){i(26847),i(27530);var s=i(73742),a=i(59048),o=i(7616);i(78645),i(38573);let n,r,l,c=t=>t;class d extends a.oi{render(){var t;return(0,a.dy)(n||(n=c`<ha-textfield
        .invalid=${0}
        .errorMessage=${0}
        .icon=${0}
        .iconTrailing=${0}
        .autocomplete=${0}
        .autocorrect=${0}
        .inputSpellcheck=${0}
        .value=${0}
        .placeholder=${0}
        .label=${0}
        .disabled=${0}
        .required=${0}
        .minLength=${0}
        .maxLength=${0}
        .outlined=${0}
        .helper=${0}
        .validateOnInitialRender=${0}
        .validationMessage=${0}
        .autoValidate=${0}
        .pattern=${0}
        .size=${0}
        .helperPersistent=${0}
        .charCounter=${0}
        .endAligned=${0}
        .prefix=${0}
        .name=${0}
        .inputMode=${0}
        .readOnly=${0}
        .autocapitalize=${0}
        .type=${0}
        .suffix=${0}
        @input=${0}
        @change=${0}
      ></ha-textfield>
      <ha-icon-button
        .label=${0}
        @click=${0}
        .path=${0}
      ></ha-icon-button>`),this.invalid,this.errorMessage,this.icon,this.iconTrailing,this.autocomplete,this.autocorrect,this.inputSpellcheck,this.value,this.placeholder,this.label,this.disabled,this.required,this.minLength,this.maxLength,this.outlined,this.helper,this.validateOnInitialRender,this.validationMessage,this.autoValidate,this.pattern,this.size,this.helperPersistent,this.charCounter,this.endAligned,this.prefix,this.name,this.inputMode,this.readOnly,this.autocapitalize,this._unmaskedPassword?"text":"password",(0,a.dy)(r||(r=c`<div style="width: 24px"></div>`)),this._handleInputEvent,this._handleChangeEvent,(null===(t=this.hass)||void 0===t?void 0:t.localize(this._unmaskedPassword?"ui.components.selectors.text.hide_password":"ui.components.selectors.text.show_password"))||(this._unmaskedPassword?"Hide password":"Show password"),this._toggleUnmaskedPassword,this._unmaskedPassword?"M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.08L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.74,7.13 11.35,7 12,7Z":"M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z")}focus(){this._textField.focus()}checkValidity(){return this._textField.checkValidity()}reportValidity(){return this._textField.reportValidity()}setCustomValidity(t){return this._textField.setCustomValidity(t)}layout(){return this._textField.layout()}_toggleUnmaskedPassword(){this._unmaskedPassword=!this._unmaskedPassword}_handleInputEvent(t){this.value=t.target.value}_handleChangeEvent(t){this.value=t.target.value,this._reDispatchEvent(t)}_reDispatchEvent(t){const e=new Event(t.type,t);this.dispatchEvent(e)}constructor(...t){super(...t),this.icon=!1,this.iconTrailing=!1,this.value="",this.placeholder="",this.label="",this.disabled=!1,this.required=!1,this.minLength=-1,this.maxLength=-1,this.outlined=!1,this.helper="",this.validateOnInitialRender=!1,this.validationMessage="",this.autoValidate=!1,this.pattern="",this.size=null,this.helperPersistent=!1,this.charCounter=!1,this.endAligned=!1,this.prefix="",this.suffix="",this.name="",this.readOnly=!1,this.autocapitalize="",this._unmaskedPassword=!1}}d.styles=(0,a.iv)(l||(l=c`
    :host {
      display: block;
      position: relative;
    }
    ha-textfield {
      width: 100%;
    }
    ha-icon-button {
      position: absolute;
      top: 8px;
      right: 8px;
      inset-inline-start: initial;
      inset-inline-end: 8px;
      --mdc-icon-button-size: 40px;
      --mdc-icon-size: 20px;
      color: var(--secondary-text-color);
      direction: var(--direction);
    }
  `)),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"invalid",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"error-message"})],d.prototype,"errorMessage",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"icon",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"iconTrailing",void 0),(0,s.__decorate)([(0,o.Cb)()],d.prototype,"autocomplete",void 0),(0,s.__decorate)([(0,o.Cb)()],d.prototype,"autocorrect",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"input-spellcheck"})],d.prototype,"inputSpellcheck",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"placeholder",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],d.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)({type:Number})],d.prototype,"minLength",void 0),(0,s.__decorate)([(0,o.Cb)({type:Number})],d.prototype,"maxLength",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],d.prototype,"outlined",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"validateOnInitialRender",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"validationMessage",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"autoValidate",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"pattern",void 0),(0,s.__decorate)([(0,o.Cb)({type:Number})],d.prototype,"size",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"helperPersistent",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"charCounter",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"endAligned",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"prefix",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"suffix",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],d.prototype,"name",void 0),(0,s.__decorate)([(0,o.Cb)({type:String,attribute:"input-mode"})],d.prototype,"inputMode",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],d.prototype,"readOnly",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1,type:String})],d.prototype,"autocapitalize",void 0),(0,s.__decorate)([(0,o.SB)()],d.prototype,"_unmaskedPassword",void 0),(0,s.__decorate)([(0,o.IO)("ha-textfield")],d.prototype,"_textField",void 0),(0,s.__decorate)([(0,o.hO)({passive:!0})],d.prototype,"_handleInputEvent",null),(0,s.__decorate)([(0,o.hO)({passive:!0})],d.prototype,"_handleChangeEvent",null),d=(0,s.__decorate)([(0,o.Mo)("ha-password-field")],d)},25661:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(27530);var s=i(73742),a=i(78722),o=i(59048),n=i(7616),r=i(60495),l=i(31132),c=t([r]);r=(c.then?(await c)():c)[0];class d extends o.fl{disconnectedCallback(){super.disconnectedCallback(),this._clearInterval()}connectedCallback(){super.connectedCallback(),this.datetime&&this._startInterval()}createRenderRoot(){return this}firstUpdated(t){super.firstUpdated(t),this._updateRelative()}update(t){super.update(t),this._updateRelative()}_clearInterval(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}_startInterval(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}_updateRelative(){if(this.datetime){const t="string"==typeof this.datetime?(0,a.D)(this.datetime):this.datetime,e=(0,r.G)(t,this.hass.locale);this.innerHTML=this.capitalize?(0,l.f)(e):e}else this.innerHTML=this.hass.localize("ui.components.relative_time.never")}constructor(...t){super(...t),this.capitalize=!1}}(0,s.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"datetime",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],d.prototype,"capitalize",void 0),d=(0,s.__decorate)([(0,n.Mo)("ha-relative-time")],d),e()}catch(d){e(d)}}))},80443:function(t,e,i){i(26847),i(81738),i(29981),i(6989),i(1455),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(41806),l=i(16811),c=i(75055);i(93795),i(29490);let d,h,u,p,_=t=>t;const g="__NONE_OPTION__";class v extends a.oi{render(){var t,e;if(!this._voices)return a.Ld;const i=null!==(t=this.value)&&void 0!==t?t:this.required?null===(e=this._voices[0])||void 0===e?void 0:e.voice_id:g;return(0,a.dy)(d||(d=_`
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
    `),this.label||this.hass.localize("ui.components.tts-voice-picker.voice"),i,this.required,this.disabled,this._changed,r.U,this.required?a.Ld:(0,a.dy)(h||(h=_`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),g,this.hass.localize("ui.components.tts-voice-picker.none")),this._voices.map((t=>(0,a.dy)(u||(u=_`<ha-list-item .value=${0}>
              ${0}
            </ha-list-item>`),t.voice_id,t.name))))}willUpdate(t){super.willUpdate(t),this.hasUpdated?(t.has("language")||t.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}async _updateVoices(){this.engineId&&this.language?(this._voices=(await(0,c.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((t=>t.voice_id===this.value))||(this.value=void 0,(0,n.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}updated(t){var e,i,s;(super.updated(t),t.has("_voices")&&(null===(e=this._select)||void 0===e?void 0:e.value)!==this.value)&&(null===(i=this._select)||void 0===i||i.layoutOptions(),(0,n.B)(this,"value-changed",{value:null===(s=this._select)||void 0===s?void 0:s.value}))}_changed(t){const e=t.target;!this.hass||""===e.value||e.value===this.value||void 0===this.value&&e.value===g||(this.value=e.value===g?void 0:e.value,(0,n.B)(this,"value-changed",{value:this.value}))}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this._debouncedUpdateVoices=(0,l.D)((()=>this._updateVoices()),500)}}v.styles=(0,a.iv)(p||(p=_`
    ha-select {
      width: 100%;
    }
  `)),(0,s.__decorate)([(0,o.Cb)()],v.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],v.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],v.prototype,"engineId",void 0),(0,s.__decorate)([(0,o.Cb)()],v.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],v.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],v.prototype,"required",void 0),(0,s.__decorate)([(0,o.SB)()],v.prototype,"_voices",void 0),(0,s.__decorate)([(0,o.IO)("ha-select")],v.prototype,"_select",void 0),v=(0,s.__decorate)([(0,o.Mo)("ha-tts-voice-picker")],v)},32518:function(t,e,i){i.d(e,{Dy:function(){return c},PA:function(){return n},SC:function(){return o},Xp:function(){return a},af:function(){return l},eP:function(){return s},jZ:function(){return r}});i(26847),i(87799),i(27530);const s=(t,e,i)=>"run-start"===e.type?t={init_options:i,stage:"ready",run:e.data,events:[e]}:t?((t="wake_word-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"wake_word",wake_word:Object.assign(Object.assign({},e.data),{},{done:!1})}):"wake_word-end"===e.type?Object.assign(Object.assign({},t),{},{wake_word:Object.assign(Object.assign(Object.assign({},t.wake_word),e.data),{},{done:!0})}):"stt-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"stt",stt:Object.assign(Object.assign({},e.data),{},{done:!1})}):"stt-end"===e.type?Object.assign(Object.assign({},t),{},{stt:Object.assign(Object.assign(Object.assign({},t.stt),e.data),{},{done:!0})}):"intent-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"intent",intent:Object.assign(Object.assign({},e.data),{},{done:!1})}):"intent-end"===e.type?Object.assign(Object.assign({},t),{},{intent:Object.assign(Object.assign(Object.assign({},t.intent),e.data),{},{done:!0})}):"tts-start"===e.type?Object.assign(Object.assign({},t),{},{stage:"tts",tts:Object.assign(Object.assign({},e.data),{},{done:!1})}):"tts-end"===e.type?Object.assign(Object.assign({},t),{},{tts:Object.assign(Object.assign(Object.assign({},t.tts),e.data),{},{done:!0})}):"run-end"===e.type?Object.assign(Object.assign({},t),{},{stage:"done"}):"error"===e.type?Object.assign(Object.assign({},t),{},{stage:"error",error:e.data}):Object.assign({},t)).events=[...t.events,e],t):void console.warn("Received unexpected event before receiving session",e),a=(t,e,i)=>t.connection.subscribeMessage(e,Object.assign(Object.assign({},i),{},{type:"assist_pipeline/run"})),o=t=>t.callWS({type:"assist_pipeline/pipeline/list"}),n=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:e}),r=(t,e)=>t.callWS(Object.assign({type:"assist_pipeline/pipeline/create"},e)),l=(t,e,i)=>t.callWS(Object.assign({type:"assist_pipeline/pipeline/update",pipeline_id:e},i)),c=t=>t.callWS({type:"assist_pipeline/language/list"})},33848:function(t,e,i){i.d(e,{LI:function(){return l},_Y:function(){return o},_t:function(){return r},bi:function(){return n}});var s=i(47817);i(87799);const a=["hass"],o=t=>{let{hass:e}=t,i=(0,s.Z)(t,a);return e.callApi("POST","cloud/login",i)},n=(t,e,i)=>t.callApi("POST","cloud/register",{email:e,password:i}),r=(t,e)=>t.callApi("POST","cloud/resend_confirm",{email:e}),l=t=>t.callWS({type:"cloud/status"})},59753:function(t,e,i){i.d(e,{KH:function(){return o},rM:function(){return a},zt:function(){return s}});var s=function(t){return t[t.CONTROL=1]="CONTROL",t}({});const a=(t,e,i)=>t.callWS({type:"conversation/agent/list",language:e,country:i}),o=(t,e,i)=>t.callWS({type:"conversation/agent/homeassistant/language_scores",language:e,country:i})},81086:function(t,e,i){i.d(e,{fU:function(){return r},kP:function(){return n},yt:function(){return o}});i(40777),i(81738),i(29981),i(1455);var s=i(35859),a=i(10840);const o=async t=>(0,s.I)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,a.rY)(await t.callApi("GET","hassio/addons")),n=async(t,e)=>(0,s.I)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:`/addons/${e}/start`,method:"post",timeout:null}):t.callApi("POST",`hassio/addons/${e}/start`),r=async(t,e)=>{(0,s.I)(t.config.version,2021,2,4)?await t.callWS({type:"supervisor/api",endpoint:`/addons/${e}/install`,method:"post",timeout:null}):await t.callApi("POST",`hassio/addons/${e}/install`)}},10840:function(t,e,i){i.d(e,{js:function(){return a},rY:function(){return s}});i(39710),i(26847),i(1455),i(67886),i(65451),i(46015),i(38334),i(94880),i(75643),i(29761),i(56389),i(27530),i(35859);const s=t=>t.data,a=t=>"object"==typeof t?"object"==typeof t.body?t.body.message||"Unknown error, see supervisor logs":t.body||t.message||"Unknown error, see supervisor logs":t;new Set([502,503,504])},12593:function(t,e,i){i.d(e,{n:function(){return s}});const s=(t,e,i)=>t.callService("select","select_option",{option:i},{entity_id:e})},70937:function(t,e,i){i.d(e,{m:function(){return s}});const s=(t,e,i)=>t.callWS({type:"stt/engine/list",language:e,country:i})},75055:function(t,e,i){i.d(e,{MV:function(){return c},Wg:function(){return r},Xk:function(){return n},aT:function(){return s},b_:function(){return o},yP:function(){return l}});i(44261);const s=(t,e)=>t.callApi("POST","tts_get_url",e),a="media-source://tts/",o=t=>t.startsWith(a),n=t=>t.substring(19),r=(t,e,i)=>t.callWS({type:"tts/engine/list",language:e,country:i}),l=(t,e)=>t.callWS({type:"tts/engine/get",engine_id:e}),c=(t,e,i)=>t.callWS({type:"tts/engine/voices",engine_id:e,language:i})},33328:function(t,e,i){i.d(e,{w:function(){return s}});const s=t=>t.callWS({type:"wyoming/info"})},39894:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(30337),l=(i(40830),i(37198)),c=i(67616),d=t([r]);r=(d.then?(await d)():d)[0];let h,u,p=t=>t;const _="M17.9,17.39C17.64,16.59 16.89,16 16,16H15V13A1,1 0 0,0 14,12H8V10H10A1,1 0 0,0 11,9V7H13A2,2 0 0,0 15,5V4.59C17.93,5.77 20,8.64 20,12C20,14.08 19.2,15.97 17.9,17.39M11,19.93C7.05,19.44 4,16.08 4,12C4,11.38 4.08,10.78 4.21,10.21L9,15V16A2,2 0 0,0 11,18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z",g="M8,7A2,2 0 0,1 10,9V14A2,2 0 0,1 8,16A2,2 0 0,1 6,14V9A2,2 0 0,1 8,7M14,14C14,16.97 11.84,19.44 9,19.92V22H7V19.92C4.16,19.44 2,16.97 2,14H4A4,4 0 0,0 8,18A4,4 0 0,0 12,14H14M21.41,9.41L17.17,13.66L18.18,10H14A2,2 0 0,1 12,8V4A2,2 0 0,1 14,2H20A2,2 0 0,1 22,4V8C22,8.55 21.78,9.05 21.41,9.41Z",v="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class f extends a.oi{render(){var t,e,i;return(0,a.dy)(h||(h=p`<div class="content">
        <img
          src=${0}
          alt="Nabu Casa logo"
        />
        <h1>
          ${0}
        </h1>
        <div class="features">
          <div class="feature speech">
            <div class="logos">
              <div class="round-icon">
                <ha-svg-icon .path=${0}></ha-svg-icon>
              </div>
            </div>
            <h2>
              ${0}
              <span class="no-wrap"></span>
            </h2>
            <p>
              ${0}
            </p>
          </div>
          <div class="feature access">
            <div class="logos">
              <div class="round-icon">
                <ha-svg-icon .path=${0}></ha-svg-icon>
              </div>
            </div>
            <h2>
              ${0}
              <span class="no-wrap"></span>
            </h2>
            <p>
              ${0}
            </p>
          </div>
          <div class="feature">
            <div class="logos">
              <img
                alt="Google Assistant"
                src=${0}
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
              />
              <img
                alt="Amazon Alexa"
                src=${0}
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
              />
            </div>
            <h2>
              ${0}
            </h2>
            <p>
              ${0}
            </p>
          </div>
        </div>
      </div>
      <div class="footer side-by-side">
        <ha-button
          href="https://www.nabucasa.com"
          target="_blank"
          rel="noreferrer noopener"
          appearance="plain"
        >
          <ha-svg-icon .path=${0} slot="start"></ha-svg-icon>
          nabucasa.com
        </ha-button>
        <ha-button @click=${0}
          >${0}</ha-button
        >
      </div>`),`/static/images/logo_nabu_casa${null!==(t=this.hass.themes)&&void 0!==t&&t.darkMode?"_dark":""}.png`,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.cloud.title"),g,this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.speech.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.speech.text"),_,this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.remote_access.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.remote_access.text"),(0,l.X1)({domain:"google_assistant",type:"icon",darkOptimized:null===(e=this.hass.themes)||void 0===e?void 0:e.darkMode}),(0,l.X1)({domain:"alexa",type:"icon",darkOptimized:null===(i=this.hass.themes)||void 0===i?void 0:i.darkMode}),this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.assistants.title"),this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.assistants.text"),v,this._signUp,this.hass.localize("ui.panel.config.cloud.register.headline"))}_signUp(){(0,n.B)(this,"cloud-step",{step:"SIGNUP"})}}f.styles=[c._,(0,a.iv)(u||(u=p`
      :host {
        display: flex;
      }
      .features {
        display: flex;
        flex-direction: column;
        grid-gap: 16px;
        padding: 16px;
      }
      .feature {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 16px;
      }
      .feature .logos {
        margin-bottom: 16px;
      }
      .feature .logos > * {
        width: 40px;
        height: 40px;
        margin: 0 4px;
      }
      .round-icon {
        border-radius: 50%;
        color: #6e41ab;
        background-color: #e8dcf7;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: var(--ha-font-size-2xl);
      }
      .access .round-icon {
        color: #00aef8;
        background-color: #cceffe;
      }
      .feature h2 {
        font-size: var(--ha-font-size-l);
        font-weight: var(--ha-font-weight-medium);
        line-height: var(--ha-line-height-normal);
        margin-top: 0;
        margin-bottom: 8px;
      }
      .feature p {
        font-size: var(--ha-font-size-m);
        font-weight: var(--ha-font-weight-normal);
        line-height: var(--ha-line-height-condensed);
        margin: 0;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],f.prototype,"hass",void 0),f=(0,s.__decorate)([(0,o.Mo)("cloud-step-intro")],f),e()}catch(h){e(h)}}))},77474:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(87799),i(1455),i(64510),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(29173),l=(i(22543),i(30337)),c=(i(20455),i(40830),i(38573),i(33848)),d=i(51909),h=i(81665),u=i(67616),p=t([l]);l=(p.then?(await p)():p)[0];let _,g,v,f=t=>t;class y extends a.oi{render(){var t;return(0,a.dy)(_||(_=f`<div class="content">
        <img
          src=${0}
          alt="Nabu Casa logo"
        />
        <h1>${0}</h1>
        ${0}
        <ha-textfield
          autofocus
          id="email"
          name="email"
          .label=${0}
          .disabled=${0}
          type="email"
          autocomplete="email"
          required
          @keydown=${0}
          validationMessage=${0}
        ></ha-textfield>
        <ha-password-field
          id="password"
          name="password"
          .label=${0}
          .disabled=${0}
          autocomplete="new-password"
          minlength="8"
          required
          @keydown=${0}
          validationMessage=${0}
        ></ha-password-field>
      </div>
      <div class="footer">
        <ha-button
          @click=${0}
          .disabled=${0}
          >${0}</ha-button
        >
      </div>`),`/static/images/logo_nabu_casa${null!==(t=this.hass.themes)&&void 0!==t&&t.darkMode?"_dark":""}.png`,this.hass.localize("ui.panel.config.cloud.login.sign_in"),this._error?(0,a.dy)(g||(g=f`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):"",this.hass.localize("ui.panel.config.cloud.register.email_address"),this._requestInProgress,this._keyDown,this.hass.localize("ui.panel.config.cloud.register.email_error_msg"),this.hass.localize("ui.panel.config.cloud.register.password"),this._requestInProgress,this._keyDown,this.hass.localize("ui.panel.config.cloud.register.password_error_msg"),this._handleLogin,this._requestInProgress,this.hass.localize("ui.panel.config.cloud.login.sign_in"))}_keyDown(t){"Enter"===t.key&&this._handleLogin()}async _handleLogin(){const t=this._emailField,e=this._passwordField,i=t.value,s=e.value;if(!t.reportValidity())return e.reportValidity(),void t.focus();if(!e.reportValidity())return void e.focus();this._requestInProgress=!0;const a=async(e,i)=>{try{await(0,c._Y)(Object.assign(Object.assign({hass:this.hass,email:e},i?{code:i}:{password:s}),{},{check_connection:this._checkConnection}))}catch(o){const i=o&&o.body&&o.body.code;if("mfarequired"===i){const t=await(0,h.D9)(this,{title:this.hass.localize("ui.panel.config.cloud.login.totp_code_prompt_title"),inputLabel:this.hass.localize("ui.panel.config.cloud.login.totp_code"),inputType:"text",defaultValue:"",confirmText:this.hass.localize("ui.panel.config.cloud.login.submit")});if(null!==t&&""!==t)return void(await a(e,t))}if("alreadyconnectederror"===i)return void(0,d.F)(this,{details:JSON.parse(o.body.message),logInHereAction:()=>{this._checkConnection=!1,a(e)},closeDialog:()=>{this._requestInProgress=!1}});if("usernotfound"===i&&e!==e.toLowerCase())return void(await a(e.toLowerCase()));if("PasswordChangeRequired"===i)return(0,h.Ys)(this,{title:this.hass.localize("ui.panel.config.cloud.login.alert_password_change_required")}),(0,r.c)("/config/cloud/forgot-password"),void(0,n.B)(this,"closed");switch(this._requestInProgress=!1,i){case"UserNotConfirmed":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_email_confirm_necessary");break;case"mfarequired":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_mfa_code_required");break;case"mfaexpiredornotstarted":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_mfa_expired_or_not_started");break;case"invalidtotpcode":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_totp_code_invalid");break;default:this._error=o&&o.body&&o.body.message?o.body.message:"Unknown error"}t.focus()}};await a(i)}constructor(...t){super(...t),this._requestInProgress=!1,this._checkConnection=!0}}y.styles=[u._,(0,a.iv)(v||(v=f`
      :host {
        display: block;
      }
      ha-textfield,
      ha-password-field {
        display: block;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_requestInProgress",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_checkConnection",void 0),(0,s.__decorate)([(0,o.IO)("#email",!0)],y.prototype,"_emailField",void 0),(0,s.__decorate)([(0,o.IO)("#password",!0)],y.prototype,"_passwordField",void 0),y=(0,s.__decorate)([(0,o.Mo)("cloud-step-signin")],y),e()}catch(_){e(_)}}))},92442:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(1455),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(22543),i(30337)),l=(i(20455),i(40830),i(38573),i(33848)),c=i(67616),d=t([r]);r=(d.then?(await d)():d)[0];let h,u,p,_,g,v,f,y=t=>t;class m extends a.oi{render(){var t;return(0,a.dy)(h||(h=y`<div class="content">
        <img
          src=${0}
          alt="Nabu Casa logo"
        />
        <h1>
          ${0}
        </h1>
        ${0}
        ${0}
      </div>
      <div class="footer side-by-side">
        ${0}
      </div>`),`/static/images/logo_nabu_casa${null!==(t=this.hass.themes)&&void 0!==t&&t.darkMode?"_dark":""}.png`,this.hass.localize("ui.panel.config.cloud.register.create_account"),this._error?(0,a.dy)(u||(u=y`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):"","VERIFY"===this._state?(0,a.dy)(p||(p=y`<p>
              ${0}
            </p>`),this.hass.localize("ui.panel.config.cloud.register.confirm_email",{email:this._email})):(0,a.dy)(_||(_=y`<ha-textfield
                autofocus
                id="email"
                name="email"
                .label=${0}
                .disabled=${0}
                type="email"
                autocomplete="email"
                required
                @keydown=${0}
                validationMessage=${0}
              ></ha-textfield>
              <ha-password-field
                id="password"
                name="password"
                .label=${0}
                .disabled=${0}
                autocomplete="new-password"
                minlength="8"
                required
                @keydown=${0}
                validationMessage=${0}
              ></ha-password-field>`),this.hass.localize("ui.panel.config.cloud.register.email_address"),this._requestInProgress,this._keyDown,this.hass.localize("ui.panel.config.cloud.register.email_error_msg"),this.hass.localize("ui.panel.config.cloud.register.password"),this._requestInProgress,this._keyDown,this.hass.localize("ui.panel.config.cloud.register.password_error_msg")),"VERIFY"===this._state?(0,a.dy)(g||(g=y`<ha-button
                @click=${0}
                .disabled=${0}
                appearance="plain"
                >${0}</ha-button
              ><ha-button
                @click=${0}
                .disabled=${0}
                >${0}</ha-button
              >`),this._handleResendVerifyEmail,this._requestInProgress,this.hass.localize("ui.panel.config.cloud.register.resend_confirm_email"),this._login,this._requestInProgress,this.hass.localize("ui.panel.config.cloud.register.clicked_confirm")):(0,a.dy)(v||(v=y`<ha-button
                @click=${0}
                .disabled=${0}
                appearance="plain"
                >${0}</ha-button
              >
              <ha-button
                @click=${0}
                .disabled=${0}
                >${0}</ha-button
              >`),this._signIn,this._requestInProgress,this.hass.localize("ui.panel.config.cloud.login.sign_in"),this._handleRegister,this._requestInProgress,this.hass.localize("ui.common.next")))}_signIn(){(0,n.B)(this,"cloud-step",{step:"SIGNIN"})}_keyDown(t){"Enter"===t.key&&this._handleRegister()}async _handleRegister(){const t=this._emailField,e=this._passwordField;if(!t.reportValidity())return e.reportValidity(),void t.focus();if(!e.reportValidity())return void e.focus();const i=t.value.toLowerCase(),s=e.value;this._requestInProgress=!0;try{await(0,l.bi)(this.hass,i,s),this._email=i,this._password=s,this._verificationEmailSent()}catch(a){this._password="",this._error=a&&a.body&&a.body.message?a.body.message:"Unknown error"}finally{this._requestInProgress=!1}}async _handleResendVerifyEmail(){if(this._email)try{await(0,l._t)(this.hass,this._email),this._verificationEmailSent()}catch(t){this._error=t&&t.body&&t.body.message?t.body.message:"Unknown error"}}_verificationEmailSent(){this._state="VERIFY",setTimeout((()=>this._login()),5e3)}async _login(){if(this._email&&this._password)try{await(0,l._Y)({hass:this.hass,email:this._email,password:this._password}),(0,n.B)(this,"cloud-step",{step:"DONE"})}catch(e){var t;"usernotconfirmed"===(null==e||null===(t=e.body)||void 0===t?void 0:t.code)?this._verificationEmailSent():this._error="Something went wrong. Please try again."}}constructor(...t){super(...t),this._requestInProgress=!1}}m.styles=[c._,(0,a.iv)(f||(f=y`
      .content {
        width: 100%;
      }
      ha-textfield,
      ha-password-field {
        display: block;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],m.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],m.prototype,"_requestInProgress",void 0),(0,s.__decorate)([(0,o.SB)()],m.prototype,"_email",void 0),(0,s.__decorate)([(0,o.SB)()],m.prototype,"_password",void 0),(0,s.__decorate)([(0,o.SB)()],m.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],m.prototype,"_state",void 0),(0,s.__decorate)([(0,o.IO)("#email",!0)],m.prototype,"_emailField",void 0),(0,s.__decorate)([(0,o.IO)("#password",!0)],m.prototype,"_passwordField",void 0),m=(0,s.__decorate)([(0,o.Mo)("cloud-step-signup")],m),e()}catch(h){e(h)}}))},67616:function(t,e,i){i.d(e,{_:function(){return o}});var s=i(59048);let a;const o=[i(77204).Qx,(0,s.iv)(a||(a=(t=>t)`
    :host {
      align-items: center;
      text-align: center;
      min-height: 400px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      padding: 24px;
      box-sizing: border-box;
    }
    .content {
      flex: 1;
    }
    .content img {
      width: 120px;
    }
    @media all and (max-width: 450px), all and (max-height: 500px) {
      :host {
        min-height: 100%;
        height: auto;
      }
      .content img {
        margin-top: 68px;
        margin-bottom: 68px;
      }
    }
    .footer {
      display: flex;
      width: 100%;
      flex-direction: row;
      justify-content: flex-end;
    }
    .footer.full-width {
      flex-direction: column;
    }
    .footer.full-width ha-button {
      width: 100%;
    }
    .footer.centered {
      justify-content: center;
    }
    .footer.side-by-side {
      justify-content: space-between;
    }
  `))]},52398:function(t,e,i){i.a(t,(async function(t,s){try{i.r(e),i.d(e,{HaVoiceAssistantSetupDialog:function(){return G},STEP:function(){return S}});i(39710),i(26847),i(2394),i(81738),i(94814),i(29981),i(6989),i(1455),i(56389),i(27530);var a=i(73742),o=i(59048),n=i(7616),r=i(28105),l=i(29740),c=i(76151),d=i(75972),h=(i(62335),i(99298),i(86352)),u=(i(51431),i(89275)),p=i(59753),_=i(64930),g=i(77204),v=i(37503),f=i(59924),y=i(31812),m=i(95907),b=i(24144),w=i(24087),$=i(34041),C=i(73801),k=i(54503),x=t([v,f,y,m,b,w,$,C,k,d,h]);[v,f,y,m,b,w,$,C,k,d,h]=x.then?(await x)():x;let z,L,O,E,I,A,P,M,T,B,j,H,N,W,V,U,D,q,R=t=>t;const F="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z",Z="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",K="M7,10L12,15L17,10H7Z";var S=function(t){return t[t.INIT=0]="INIT",t[t.UPDATE=1]="UPDATE",t[t.CHECK=2]="CHECK",t[t.WAKEWORD=3]="WAKEWORD",t[t.AREA=4]="AREA",t[t.PIPELINE=5]="PIPELINE",t[t.SUCCESS=6]="SUCCESS",t[t.CLOUD=7]="CLOUD",t[t.LOCAL=8]="LOCAL",t[t.CHANGE_WAKEWORD=9]="CHANGE_WAKEWORD",t}({});class G extends o.oi{async showDialog(t){this._params=t,await this._fetchAssistConfiguration(),this._step=1}async closeDialog(){var t;null===(t=this.renderRoot.querySelector("ha-dialog"))||void 0===t||t.close()}willUpdate(t){t.has("_step")&&5===this._step&&this._getLanguages()}_dialogClosed(){this._params=void 0,this._assistConfiguration=void 0,this._previousSteps=[],this._nextStep=void 0,this._step=0,this._language=void 0,this._languages=[],this._localOption=void 0,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}render(){var t,e;if(!this._params)return o.Ld;const i=this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite"),s=i?this.hass.states[i]:void 0;return(0,o.dy)(z||(z=R`
      <ha-dialog
        open
        @closed=${0}
        .heading=${0}
        hideActions
        escapeKeyAction
        scrimClickAction
      >
        <ha-dialog-header slot="heading">
          ${0}
          ${0}
        </ha-dialog-header>
        <div
          class="content"
          @next-step=${0}
          @prev-step=${0}
        >
          ${0}
        </div>
      </ha-dialog>
    `),this._dialogClosed,"Voice Satellite setup",8===this._step?o.Ld:this._previousSteps.length?(0,o.dy)(L||(L=R`<ha-icon-button
                  slot="navigationIcon"
                  .label=${0}
                  .path=${0}
                  @click=${0}
                ></ha-icon-button>`),null!==(t=this.hass.localize("ui.common.back"))&&void 0!==t?t:"Back",F,this._goToPreviousStep):1!==this._step?(0,o.dy)(O||(O=R`<ha-icon-button
                    slot="navigationIcon"
                    .label=${0}
                    .path=${0}
                    @click=${0}
                  ></ha-icon-button>`),null!==(e=this.hass.localize("ui.common.close"))&&void 0!==e?e:"Close",Z,this.closeDialog):o.Ld,3===this._step||4===this._step?(0,o.dy)(E||(E=R`<ha-button
                @click=${0}
                class="skip-btn"
                slot="actionItems"
                >${0}</ha-button
              >`),this._goToNextStep,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.skip")):5===this._step&&this._language?(0,o.dy)(I||(I=R`<ha-md-button-menu
                    slot="actionItems"
                    positioning="fixed"
                  >
                    <ha-assist-chip
                      .label=${0}
                      slot="trigger"
                    >
                      <ha-svg-icon
                        slot="trailing-icon"
                        .path=${0}
                      ></ha-svg-icon
                    ></ha-assist-chip>
                    ${0}
                  </ha-md-button-menu>`),(0,d.u)(this._language,this.hass.locale),K,(0,h.C)(this._languages,!1,!1,this.hass.locale).map((t=>(0,o.dy)(A||(A=R`<ha-md-menu-item
                          .value=${0}
                          @click=${0}
                          @keydown=${0}
                          .selected=${0}
                        >
                          ${0}
                        </ha-md-menu-item>`),t.value,this._handlePickLanguage,this._handlePickLanguage,this._language===t.value,t.label)))):o.Ld,this._goToNextStep,this._goToPreviousStep,1===this._step?(0,o.dy)(P||(P=R`<ha-voice-assistant-setup-step-update
                .hass=${0}
                .updateEntityId=${0}
              ></ha-voice-assistant-setup-step-update>`),this.hass,this._findDomainEntityId(this._params.deviceId,this.hass.entities,"update")):this._error?(0,o.dy)(M||(M=R`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):(null==s?void 0:s.state)===_.nZ?(0,o.dy)(T||(T=R`<ha-alert alert-type="error"
                    >${0}</ha-alert
                  >`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.not_available")):2===this._step?(0,o.dy)(B||(B=R`<ha-voice-assistant-setup-step-check
                      .hass=${0}
                      .assistEntityId=${0}
                    ></ha-voice-assistant-setup-step-check>`),this.hass,i):3===this._step?(0,o.dy)(j||(j=R`<ha-voice-assistant-setup-step-wake-word
                        .hass=${0}
                        .assistConfiguration=${0}
                        .assistEntityId=${0}
                        .deviceEntities=${0}
                      ></ha-voice-assistant-setup-step-wake-word>`),this.hass,this._assistConfiguration,i,this._deviceEntities(this._params.deviceId,this.hass.entities)):9===this._step?(0,o.dy)(H||(H=R`
                          <ha-voice-assistant-setup-step-change-wake-word
                            .hass=${0}
                            .assistConfiguration=${0}
                            .assistEntityId=${0}
                          ></ha-voice-assistant-setup-step-change-wake-word>
                        `),this.hass,this._assistConfiguration,i):4===this._step?(0,o.dy)(N||(N=R`
                            <ha-voice-assistant-setup-step-area
                              .hass=${0}
                              .deviceId=${0}
                            ></ha-voice-assistant-setup-step-area>
                          `),this.hass,this._params.deviceId):5===this._step?(0,o.dy)(W||(W=R`<ha-voice-assistant-setup-step-pipeline
                              .hass=${0}
                              .languages=${0}
                              .language=${0}
                              .assistConfiguration=${0}
                              .assistEntityId=${0}
                              @language-changed=${0}
                            ></ha-voice-assistant-setup-step-pipeline>`),this.hass,this._languages,this._language,this._assistConfiguration,i,this._languageChanged):7===this._step?(0,o.dy)(V||(V=R`<ha-voice-assistant-setup-step-cloud
                                .hass=${0}
                              ></ha-voice-assistant-setup-step-cloud>`),this.hass):8===this._step?(0,o.dy)(U||(U=R`<ha-voice-assistant-setup-step-local
                                  .hass=${0}
                                  .language=${0}
                                  .localOption=${0}
                                  .assistConfiguration=${0}
                                ></ha-voice-assistant-setup-step-local>`),this.hass,this._language,this._localOption,this._assistConfiguration):6===this._step?(0,o.dy)(D||(D=R`<ha-voice-assistant-setup-step-success
                                    .hass=${0}
                                    .assistConfiguration=${0}
                                    .assistEntityId=${0}
                                    .deviceId=${0}
                                  ></ha-voice-assistant-setup-step-success>`),this.hass,this._assistConfiguration,i,this._params.deviceId):o.Ld)}async _getLanguages(){if(this._languages.length)return;const t=await(0,p.KH)(this.hass);this._languages=Object.entries(t.languages).filter((([t,e])=>e.cloud>0||e.full_local>0||e.focused_local>0)).map((([t,e])=>t)),this._language=t.preferred_language&&this._languages.includes(t.preferred_language)?t.preferred_language:void 0}async _fetchAssistConfiguration(){try{this._assistConfiguration=await(0,u.ko)(this.hass,this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite"))}catch(t){this._error=t.message}}_handlePickLanguage(t){"keydown"===t.type&&"Enter"!==t.key&&" "!==t.key||(this._language=t.target.value)}_languageChanged(t){t.detail.value&&(this._language=t.detail.value)}_goToPreviousStep(){this._previousSteps.length&&(this._step=this._previousSteps.pop())}_goToNextStep(t){var e,i,s,a;null!=t&&null!==(e=t.detail)&&void 0!==e&&e.updateConfig&&this._fetchAssistConfiguration(),null!=t&&null!==(i=t.detail)&&void 0!==i&&i.nextStep&&(this._nextStep=t.detail.nextStep),null!=t&&null!==(s=t.detail)&&void 0!==s&&s.noPrevious||this._previousSteps.push(this._step),null!=t&&null!==(a=t.detail)&&void 0!==a&&a.step?(this._step=t.detail.step,8===t.detail.step&&(this._localOption=t.detail.option)):this._nextStep?(this._step=this._nextStep,this._nextStep=void 0):this._step+=1}static get styles(){return[g.yu,(0,o.iv)(q||(q=R`
        ha-dialog {
          --dialog-content-padding: 0;
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          ha-dialog {
            --mdc-dialog-min-width: 560px;
            --mdc-dialog-max-width: 560px;
            --mdc-dialog-min-width: min(560px, 95vw);
            --mdc-dialog-max-width: min(560px, 95vw);
          }
        }
        ha-dialog-header {
          height: 56px;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          .content {
            height: calc(100vh - 56px);
          }
        }
        .skip-btn {
          margin-top: 6px;
        }
        ha-alert {
          margin: 24px;
          display: block;
        }
        ha-md-button-menu {
          height: 48px;
          display: flex;
          align-items: center;
          margin-right: 12px;
          margin-inline-end: 12px;
          margin-inline-start: initial;
        }
      `))]}constructor(...t){super(...t),this._step=0,this._languages=[],this._previousSteps=[],this._deviceEntities=(0,r.Z)(((t,e)=>Object.values(e).filter((e=>e.device_id===t)))),this._findDomainEntityId=(0,r.Z)(((t,e,i)=>{var s;return null===(s=this._deviceEntities(t,e).find((t=>(0,c.M)(t.entity_id)===i)))||void 0===s?void 0:s.entity_id}))}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],G.prototype,"hass",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_params",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_step",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_assistConfiguration",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_error",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_language",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_languages",void 0),(0,a.__decorate)([(0,n.SB)()],G.prototype,"_localOption",void 0),G=(0,a.__decorate)([(0,n.Mo)("ha-voice-assistant-setup-dialog")],G),s()}catch(z){s(z)}}))},37503:function(t,e,i){i.a(t,(async function(t,e){try{i(1455);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(99495),l=i(57774),c=i(81665),d=i(67616),h=t([r]);r=(h.then?(await h)():h)[0];let u,p,_=t=>t;class g extends a.oi{render(){const t=this.hass.devices[this.deviceId];return(0,a.dy)(u||(u=_`<div class="content">
        <img
          src="/static/images/voice-assistant/area.png"
          alt="Casita Home Assistant logo"
        />
        <h1>
          ${0}
        </h1>
        <p class="secondary">
          ${0}
        </p>
        <ha-area-picker
          .hass=${0}
          .value=${0}
        ></ha-area-picker>
      </div>
      <div class="footer">
        <ha-button @click=${0}
          >${0}</ha-button
        >
      </div>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.area.title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.area.secondary"),this.hass,t.area_id,this._setArea,this.hass.localize("ui.common.next"))}async _setArea(){const t=this.shadowRoot.querySelector("ha-area-picker").value;t?(await(0,l.t1)(this.hass,this.deviceId,{area_id:t}),this._nextStep()):(0,c.Ys)(this,{text:this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.area.no_selection")})}_nextStep(){(0,n.B)(this,"next-step")}}g.styles=[d._,(0,a.iv)(p||(p=_`
      ha-area-picker {
        display: block;
        width: 100%;
        margin-bottom: 24px;
        text-align: initial;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"deviceId",void 0),g=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-area")],g),e()}catch(u){e(u)}}))},59924:function(t,e,i){i.a(t,(async function(t,e){try{i(81738),i(6989),i(1455);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(89429),i(78067),i(89275)),l=i(67616),c=i(52398),d=t([c]);c=(d.then?(await d)():d)[0];let h,u,p,_=t=>t;class g extends a.oi{render(){return(0,a.dy)(h||(h=_`<div class="padding content">
        <img
          src="/static/images/voice-assistant/change-wake-word.png"
          alt="Casita Home Assistant logo"
        />
        <h1>
          ${0}
        </h1>
        <p class="secondary">
          ${0}
        </p>
      </div>
      <ha-md-list>
        ${0}
      </ha-md-list>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.change_wake_word.title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.change_wake_word.secondary"),this.assistConfiguration.available_wake_words.map((t=>(0,a.dy)(u||(u=_`<ha-md-list-item
              interactive
              type="button"
              @click=${0}
              .value=${0}
            >
              ${0}
              <ha-icon-next slot="end"></ha-icon-next>
            </ha-md-list-item>`),this._wakeWordPicked,t.id,t.wake_word))))}async _wakeWordPicked(t){if(!this.assistEntityId)return;const e=t.currentTarget.value;await(0,r.DT)(this.hass,this.assistEntityId,[e]),this._nextStep()}_nextStep(){(0,n.B)(this,"next-step",{step:c.STEP.WAKEWORD,updateConfig:!0})}}g.styles=[l._,(0,a.iv)(p||(p=_`
      :host {
        padding: 0;
      }
      .padding {
        padding: 24px;
      }
      ha-md-list {
        width: 100%;
        text-align: initial;
        margin-bottom: 24px;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"assistEntityId",void 0),g=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-change-wake-word")],g),e()}catch(h){e(h)}}))},31812:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(1455),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(30337),l=i(97862),c=i(89275),d=i(67616),h=i(47584),u=t([r,l]);[r,l]=u.then?(await u)():u;let p,_,g,v,f=t=>t;class y extends a.oi{willUpdate(t){var e;super.willUpdate(t),this.hasUpdated?"success"===this._status&&t.has("hass")&&"idle"===(null===(e=this.hass.states[this.assistEntityId])||void 0===e?void 0:e.state)&&this._nextStep():this._testConnection()}render(){return(0,a.dy)(p||(p=f`<div class="content">
      ${0}
    </div>`),"timeout"===this._status?(0,a.dy)(_||(_=f`<img
              src="/static/images/voice-assistant/error.png"
              alt="Casita Home Assistant error logo"
            />
            <h1>
              ${0}
            </h1>
            <p class="secondary">
              ${0}
            </p>
            <div class="footer">
              <ha-button
                appearance="plain"
                href=${0}
              >
                >${0}</ha-button
              >
              <ha-button @click=${0}
                >${0}</ha-button
              >
            </div>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.failed_title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.failed_secondary"),(0,h.R)(this.hass,"/voice_control/troubleshooting/#i-dont-get-a-voice-response"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.help"),this._testConnection,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.retry")):(0,a.dy)(g||(g=f`<img
              src="/static/images/voice-assistant/hi.png"
              alt="Casita Home Assistant hi logo"
            />
            <h1>
              ${0}
            </h1>
            <p class="secondary">
              ${0}
            </p>

            ${0}`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.secondary"),this._showLoader?(0,a.dy)(v||(v=f`<ha-spinner></ha-spinner>`)):a.Ld))}async _testConnection(){this._status=void 0,this._showLoader=!1;const t=setTimeout((()=>{this._showLoader=!0}),3e3),e=await(0,c.cz)(this.hass,this.assistEntityId);clearTimeout(t),this._showLoader=!1,this._status=e.status}_nextStep(){(0,n.B)(this,"next-step",{noPrevious:!0})}constructor(...t){super(...t),this._showLoader=!1}}y.styles=d._,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_status",void 0),(0,s.__decorate)([(0,o.SB)()],y.prototype,"_showLoader",void 0),y=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-check")],y),e()}catch(p){e(p)}}))},95907:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(39894),r=i(77474),l=i(92442),c=i(29740),d=i(52398),h=t([n,r,l,d]);[n,r,l,d]=h.then?(await h)():h;let u,p,_,g=t=>t;class v extends a.oi{render(){return"SIGNUP"===this._state?(0,a.dy)(u||(u=g`<cloud-step-signup
        .hass=${0}
        @cloud-step=${0}
      ></cloud-step-signup>`),this.hass,this._cloudStep):"SIGNIN"===this._state?(0,a.dy)(p||(p=g`<cloud-step-signin
        .hass=${0}
        @cloud-step=${0}
      ></cloud-step-signin>`),this.hass,this._cloudStep):(0,a.dy)(_||(_=g`<cloud-step-intro
      .hass=${0}
      @cloud-step=${0}
    ></cloud-step-intro>`),this.hass,this._cloudStep)}_cloudStep(t){"DONE"!==t.detail.step?this._state=t.detail.step:(0,c.B)(this,"next-step",{step:d.STEP.PIPELINE,noPrevious:!0})}constructor(...t){super(...t),this._state="INTRO"}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],v.prototype,"_state",void 0),v=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-cloud")],v),e()}catch(u){e(u)}}))},24144:function(t,e,i){i.a(t,(async function(t,e){try{i(40777),i(39710),i(26847),i(18574),i(81738),i(94814),i(29981),i(6989),i(72489),i(1455),i(56389),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(42822),r=i(29740),l=i(76151),c=i(97862),d=i(32518),h=i(39286),u=i(28203),p=i(81086),_=i(70937),g=i(75055),v=i(33328),f=i(47584),y=i(67616),m=i(52398),b=i(59753),w=t([c,m]);[c,m]=w.then?(await w)():w;let $,C,k,x,S,z=t=>t;const L="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class O extends a.oi{render(){return(0,a.dy)($||($=z`<div class="content">
      ${0}
    </div>`),"INSTALLING"===this._state?(0,a.dy)(C||(C=z`<img
              src="/static/images/voice-assistant/update.png"
              alt="Casita Home Assistant loading logo"
            />
            <h1>
              ${0}
            </h1>
            <p>
              ${0}
            </p>
            <ha-spinner></ha-spinner>
            <p>
              ${0}
            </p>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.secondary"),this._detailState||"Installation can take several minutes"):"ERROR"===this._state?(0,a.dy)(k||(k=z`<img
                src="/static/images/voice-assistant/error.png"
                alt="Casita Home Assistant error logo"
              />
              <h1>
                ${0}
              </h1>
              <p>${0}</p>
              <p>
                ${0}
              </p>
              <ha-button
                appearance="plain"
                size="small"
                @click=${0}
                >${0}</ha-button
              >
              <ha-button
                href=${0}
                target="_blank"
                rel="noreferrer noopener"
                size="small"
                appearance="plain"
              >
                <ha-svg-icon .path=${0} slot="start"></ha-svg-icon>
                ${0}</ha-button
              >`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.failed_title"),this._error,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.failed_secondary"),this._prevStep,this.hass.localize("ui.common.back"),(0,f.R)(this.hass,"/voice_control/voice_remote_local_assistant/"),L,this.hass.localize("ui.panel.config.common.learn_more")):"NOT_SUPPORTED"===this._state?(0,a.dy)(x||(x=z`<img
                  src="/static/images/voice-assistant/error.png"
                  alt="Casita Home Assistant error logo"
                />
                <h1>
                  ${0}
                </h1>
                <p>
                  ${0}
                </p>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${0}
                  >${0}</ha-button
                >
                <ha-button
                  href=${0}
                  target="_blank"
                  rel="noreferrer noopener"
                  appearance="plain"
                  size="small"
                >
                  <ha-svg-icon .path=${0} slot="start"></ha-svg-icon>
                  ${0}</ha-button
                >`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.not_supported_title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.not_supported_secondary"),this._prevStep,this.hass.localize("ui.common.back"),(0,f.R)(this.hass,"/voice_control/voice_remote_local_assistant/"),L,this.hass.localize("ui.panel.config.common.learn_more")):a.Ld)}willUpdate(t){super.willUpdate(t),this.hasUpdated||this._checkLocal()}_prevStep(){(0,r.B)(this,"prev-step")}_nextStep(){(0,r.B)(this,"next-step",{step:m.STEP.SUCCESS,noPrevious:!0})}async _checkLocal(){if(await this._findLocalEntities(),this._localTts&&this._localStt)try{if(this._localTts.length&&this._localStt.length)return void(await this._pickOrCreatePipelineExists());if(!(0,n.p)(this.hass,"hassio"))return void(this._state="NOT_SUPPORTED");this._state="INSTALLING";const{addons:t}=await(0,p.yt)(this.hass),e=t.find((t=>t.slug===this._ttsAddonName)),i=t.find((t=>t.slug===this._sttAddonName));this._localTts.length||(e||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.installing_${this._ttsProviderName}`),await(0,p.fU)(this.hass,this._ttsAddonName)),e&&"started"===e.state||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.starting_${this._ttsProviderName}`),await(0,p.kP)(this.hass,this._ttsAddonName)),this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.setup_${this._ttsProviderName}`),await this._setupConfigEntry("tts")),this._localStt.length||(i||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.installing_${this._sttProviderName}`),await(0,p.fU)(this.hass,this._sttAddonName)),i&&"started"===i.state||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.starting_${this._sttProviderName}`),await(0,p.kP)(this.hass,this._sttAddonName)),this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.setup_${this._sttProviderName}`),await this._setupConfigEntry("stt")),this._detailState=this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.state.creating_pipeline"),await this._findEntitiesAndCreatePipeline()}catch(t){this._state="ERROR",this._error=t.message}}get _sttProviderName(){return"focused_local"===this.localOption?"speech-to-phrase":"faster-whisper"}get _sttAddonName(){return"focused_local"===this.localOption?"core_speech-to-phrase":"core_whisper"}get _sttHostName(){return"focused_local"===this.localOption?"core-speech-to-phrase":"core-whisper"}async _findLocalEntities(){const t=Object.values(this.hass.entities).filter((t=>"wyoming"===t.platform));if(!t.length)return this._localStt=[],void(this._localTts=[]);const e=await(0,v.w)(this.hass),i=Object.values(await(0,u.Iq)(this.hass,t.map((t=>t.entity_id))));this._localTts=i.filter((t=>{var i;return"tts"===(0,l.M)(t.entity_id)&&t.config_entry_id&&(null===(i=e.info[t.config_entry_id])||void 0===i?void 0:i.tts.some((t=>t.name===this._ttsProviderName)))})),this._localStt=i.filter((t=>{var i;return"stt"===(0,l.M)(t.entity_id)&&t.config_entry_id&&(null===(i=e.info[t.config_entry_id])||void 0===i?void 0:i.asr.some((t=>t.name===this._sttProviderName)))}))}async _setupConfigEntry(t){const e=await this._findConfigFlowInProgress(t);if(e){if("create_entry"===(await(0,h.XO)(this.hass,e.flow_id,{})).type)return}return this._createConfigEntry(t)}async _findConfigFlowInProgress(t){return(await(0,h.D7)(this.hass.connection)).find((e=>"wyoming"===e.handler&&"hassio"===e.context.source&&(e.context.configuration_url&&e.context.configuration_url.includes("tts"===t?this._ttsAddonName:this._sttAddonName)||e.context.title_placeholders.name&&e.context.title_placeholders.name.toLowerCase().includes("tts"===t?this._ttsProviderName:this._sttProviderName))))}async _createConfigEntry(t){const e=await(0,h.Ky)(this.hass,"wyoming"),i=await(0,h.XO)(this.hass,e.flow_id,{host:"tts"===t?this._ttsHostName:this._sttHostName,port:"tts"===t?this._ttsPort:this._sttPort});if("create_entry"!==i.type)throw new Error(`${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.errors.failed_create_entry",{addon:"tts"===t?this._ttsProviderName:this._sttProviderName})}${"errors"in i?`: ${i.errors.base}`:""}`)}async _pickOrCreatePipelineExists(){var t,e,i;if(null===(t=this._localStt)||void 0===t||!t.length||null===(e=this._localTts)||void 0===e||!e.length)return;const s=await(0,d.SC)(this.hass);s.preferred_pipeline&&s.pipelines.sort((t=>t.id===s.preferred_pipeline?-1:0));const a=this._localTts.map((t=>t.entity_id)),o=this._localStt.map((t=>t.entity_id));let n=s.pipelines.find((t=>"conversation.home_assistant"===t.conversation_engine&&t.tts_engine&&a.includes(t.tts_engine)&&t.stt_engine&&o.includes(t.stt_engine)&&t.language.split("-")[0]===this.language.split("-")[0]));n||(n=await this._createPipeline(this._localTts[0].entity_id,this._localStt[0].entity_id)),await this.hass.callService("select","select_option",{option:n.name},{entity_id:null===(i=this.assistConfiguration)||void 0===i?void 0:i.pipeline_entity_id}),this._nextStep()}async _createPipeline(t,e){var i,s,a;const o=await(0,d.SC)(this.hass),n=(await(0,b.rM)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).agents.find((t=>"conversation.home_assistant"===t.id));if(null==n||!n.supported_languages.length)throw new Error("Conversation agent does not support requested language.");const r=(await(0,g.Wg)(this.hass,this.language,this.hass.config.country||void 0)).providers.find((e=>e.engine_id===t));if(null==r||null===(i=r.supported_languages)||void 0===i||!i.length)throw new Error("TTS engine does not support requested language.");const l=await(0,g.MV)(this.hass,t,r.supported_languages[0]);if(null===(s=l.voices)||void 0===s||!s.length)throw new Error("No voice available for requested language.");const c=(await(0,_.m)(this.hass,this.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===e));if(null==c||null===(a=c.supported_languages)||void 0===a||!a.length)throw new Error("STT engine does not support requested language.");let h=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.${this.localOption}_pipeline`),u=1;for(;o.pipelines.find((t=>t.name===h));)h=`${this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.${this.localOption}_pipeline`)} ${u}`,u++;return(0,d.jZ)(this.hass,{name:h,language:this.language.split("-")[0],conversation_engine:"conversation.home_assistant",conversation_language:n.supported_languages[0],stt_engine:e,stt_language:c.supported_languages[0],tts_engine:t,tts_language:r.supported_languages[0],tts_voice:l.voices[0].voice_id,wake_word_entity:null,wake_word_id:null})}async _findEntitiesAndCreatePipeline(t=0){var e,i,s;if(await this._findLocalEntities(),null===(e=this._localTts)||void 0===e||!e.length||null===(i=this._localStt)||void 0===i||!i.length){if(t>3)throw new Error(this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.errors.could_not_find_entities"));return await new Promise((t=>{setTimeout(t,2e3)})),this._findEntitiesAndCreatePipeline(t+1)}const a=await this._createPipeline(this._localTts[0].entity_id,this._localStt[0].entity_id);await this.hass.callService("select","select_option",{option:a.name},{entity_id:null===(s=this.assistConfiguration)||void 0===s?void 0:s.pipeline_entity_id}),this._nextStep()}constructor(...t){super(...t),this._state="INTRO",this._ttsProviderName="piper",this._ttsAddonName="core_piper",this._ttsHostName="core-piper",this._ttsPort=10200,this._sttPort=10300}}O.styles=[y._,(0,a.iv)(S||(S=z`
      ha-spinner {
        margin-top: 24px;
        margin-bottom: 24px;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],O.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],O.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],O.prototype,"localOption",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],O.prototype,"language",void 0),(0,s.__decorate)([(0,o.SB)()],O.prototype,"_state",void 0),(0,s.__decorate)([(0,o.SB)()],O.prototype,"_detailState",void 0),(0,s.__decorate)([(0,o.SB)()],O.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],O.prototype,"_localTts",void 0),(0,s.__decorate)([(0,o.SB)()],O.prototype,"_localStt",void 0),O=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-local")],O),e()}catch($){e($)}}))},24087:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(2394),i(18574),i(81738),i(29981),i(1455),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(28105),r=i(42822),l=i(29740),c=i(76151),d=i(75972),h=(i(77307),i(32518)),u=i(33848),p=i(59753),_=i(70937),g=i(75055),v=i(67616),f=i(52398),y=i(47584),m=t([d,f]);[d,f]=m.then?(await m)():m;let b,w,$,C,k=t=>t;const x=["cloud","focused_local","full_local"],S={cloud:0,focused_local:0,full_local:0};class z extends a.oi{willUpdate(t){if(super.willUpdate(t),this.hasUpdated||this._fetchData(),(t.has("language")||t.has("_languageScores"))&&this.language&&this._languageScores){var e;const t=this.language;var i;if(this._value&&0===(null===(e=this._languageScores[t])||void 0===e?void 0:e[this._value])&&(this._value=void 0),!this._value)this._value=null===(i=this._getOptions(this._languageScores[t]||S,this.hass.localize).supportedOptions[0])||void 0===i?void 0:i.value}}render(){if(!this._cloudChecked||!this._languageScores)return a.Ld;if(!this.language){const t=(0,d.u)(this.hass.config.language,this.hass.locale);return(0,a.dy)(b||(b=k`<div class="content">
        <h1>
          ${0}
        </h1>
        ${0}
        <ha-language-picker
          .hass=${0}
          .label=${0}
          .languages=${0}
          @value-changed=${0}
        ></ha-language-picker>

        <a
          href=${0}
          >${0}</a
        >
      </div>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.header"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.secondary",{language:t}),this.hass,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.language_picker"),this.languages,this._languageChanged,(0,y.R)(this.hass,"/voice_control/contribute-voice/"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.contribute",{language:t}))}const t=this._languageScores[this.language]||S,e=this._getOptions(t,this.hass.localize),i=this._value?"full_local"===this._value?"low":"high":"",s=this._value?t[this._value]>2?"high":t[this._value]>1?"ready":t[this._value]>0?"low":"":"";return(0,a.dy)(w||(w=k`<div class="content">
        <h1>
          ${0}
        </h1>
        <div class="bar-header">
          <span
            >${0}</span
          ><span
            >${0}</span
          >
        </div>
        <div class="perf-bar ${0}">
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
        </div>
        <div class="bar-header">
          <span
            >${0}</span
          ><span
            >${0}</span
          >
        </div>
        <div class="perf-bar ${0}">
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
        </div>
        <ha-select-box
          max_columns="1"
          .options=${0}
          .value=${0}
          @value-changed=${0}
        ></ha-select-box>
        ${0}
      </div>
      <div class="footer">
        <ha-button @click=${0} .disabled=${0}
          >${0}</ha-button
        >
      </div>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.performance.header"),i?this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.performance.${i}`):"",i,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.commands.header"),s?this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.commands.${s}`):"",s,e.supportedOptions,this._value,this._valueChanged,e.unsupportedOptions.length?(0,a.dy)($||($=k`<h3>
                ${0}
              </h3>
              <ha-select-box
                max_columns="1"
                .options=${0}
                disabled
              ></ha-select-box>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported"),e.unsupportedOptions):a.Ld,this._createPipeline,!this._value,this.hass.localize("ui.common.next"))}async _fetchData(){await this._hasCloud()&&await this._createCloudPipeline(!1)||(this._cloudChecked=!0,this._languageScores=(await(0,p.KH)(this.hass)).languages)}async _hasCloud(){if(!(0,r.p)(this.hass,"cloud"))return!1;const t=await(0,u.LI)(this.hass);return!(!t.logged_in||!t.active_subscription)}async _createCloudPipeline(t){let e,i;for(const r of Object.values(this.hass.entities))if("cloud"===r.platform){const t=(0,c.M)(r.entity_id);if("tts"===t)e=r.entity_id;else{if("stt"!==t)continue;i=r.entity_id}if(e&&i)break}try{var s;const n=await(0,h.SC)(this.hass);n.preferred_pipeline&&n.pipelines.sort((t=>t.id===n.preferred_pipeline?-1:0));let r=n.pipelines.find((s=>"conversation.home_assistant"===s.conversation_engine&&s.tts_engine===e&&s.stt_engine===i&&(!t||s.language.split("-")[0]===this.language.split("-")[0])));if(!r){var a,o;const t=(await(0,p.rM)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).agents.find((t=>"conversation.home_assistant"===t.id));if(null==t||!t.supported_languages.length)return!1;const s=(await(0,g.Wg)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===e));if(null==s||null===(a=s.supported_languages)||void 0===a||!a.length)return!1;const l=await(0,g.MV)(this.hass,e,s.supported_languages[0]),c=(await(0,_.m)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===i));if(null==c||null===(o=c.supported_languages)||void 0===o||!o.length)return!1;let d="Home Assistant Cloud",u=1;for(;n.pipelines.find((t=>t.name===d));)d=`Home Assistant Cloud ${u}`,u++;r=await(0,h.jZ)(this.hass,{name:d,language:(this.language||this.hass.config.language).split("-")[0],conversation_engine:"conversation.home_assistant",conversation_language:t.supported_languages[0],stt_engine:i,stt_language:c.supported_languages[0],tts_engine:e,tts_language:s.supported_languages[0],tts_voice:l.voices[0].voice_id,wake_word_entity:null,wake_word_id:null})}return await this.hass.callService("select","select_option",{option:r.name},{entity_id:null===(s=this.assistConfiguration)||void 0===s?void 0:s.pipeline_entity_id}),(0,l.B)(this,"next-step",{step:f.STEP.SUCCESS,noPrevious:!0}),!0}catch(n){return!1}}_valueChanged(t){this._value=t.detail.value}async _setupCloud(){await this._hasCloud()?this._createCloudPipeline(!0):(0,l.B)(this,"next-step",{step:f.STEP.CLOUD})}_createPipeline(){"cloud"===this._value?this._setupCloud():"focused_local"===this._value?this._setupLocalFocused():this._setupLocalFull()}_setupLocalFocused(){(0,l.B)(this,"next-step",{step:f.STEP.LOCAL,option:this._value})}_setupLocalFull(){(0,l.B)(this,"next-step",{step:f.STEP.LOCAL,option:this._value})}_languageChanged(t){t.detail.value&&(0,l.B)(this,"language-changed",{value:t.detail.value})}constructor(...t){super(...t),this.languages=[],this._cloudChecked=!1,this._getOptions=(0,n.Z)(((t,e)=>{const i=[],s=[];return x.forEach((a=>{t[a]>0?i.push({label:e(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.options.${a}.label`),description:e(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.options.${a}.description`),value:a}):s.push({label:e(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.options.${a}.label`),value:a})})),{supportedOptions:i,unsupportedOptions:s}}))}}z.styles=[v._,(0,a.iv)(C||(C=k`
      :host {
        text-align: left;
      }
      .perf-bar {
        width: 100%;
        height: 10px;
        display: flex;
        gap: 4px;
        margin: 8px 0;
      }
      .segment {
        flex-grow: 1;
        background-color: var(--disabled-color);
        transition: background-color 0.3s;
      }
      .segment:first-child {
        border-radius: 4px 0 0 4px;
      }
      .segment:last-child {
        border-radius: 0 4px 4px 0;
      }
      .perf-bar.high .segment {
        background-color: var(--success-color);
      }
      .perf-bar.ready .segment:nth-child(-n + 2) {
        background-color: var(--warning-color);
      }
      .perf-bar.low .segment:nth-child(1) {
        background-color: var(--error-color);
      }
      .bar-header {
        display: flex;
        justify-content: space-between;
        margin: 8px 0;
        margin-top: 16px;
      }
      ha-select-box {
        display: block;
      }
      ha-select-box:first-of-type {
        margin-top: 32px;
      }
      .footer {
        margin-top: 16px;
      }
      ha-language-picker {
        display: block;
        margin-top: 16px;
        margin-bottom: 16px;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],z.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],z.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],z.prototype,"deviceId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],z.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],z.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],z.prototype,"languages",void 0),(0,s.__decorate)([(0,o.SB)()],z.prototype,"_cloudChecked",void 0),(0,s.__decorate)([(0,o.SB)()],z.prototype,"_value",void 0),(0,s.__decorate)([(0,o.SB)()],z.prototype,"_languageScores",void 0),z=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-pipeline")],z),e()}catch(b){e(b)}}))},34041:function(t,e,i){i.a(t,(async function(t,e){try{i(39710),i(26847),i(81738),i(29981),i(6989),i(87799),i(1455),i(56389),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(41806),l=i(85163),c=(i(93795),i(29490),i(80443),i(32518)),d=i(89275),h=i(33848),u=i(57774),p=i(12593),_=i(26665),g=i(74183),v=i(48785),f=i(67616),y=i(52398),m=t([g,y]);[g,y]=m.then?(await m)():m;let b,w,$,C,k,x,S,z,L=t=>t;const O="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z",E="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z",I="M8,5.14V19.14L19,12.14L8,5.14Z";class A extends a.oi{willUpdate(t){if(super.willUpdate(t),t.has("assistConfiguration"))this._setTtsSettings();else if(t.has("hass")&&this.assistConfiguration){const e=t.get("hass");if(e){const t=e.states[this.assistConfiguration.pipeline_entity_id],i=this.hass.states[this.assistConfiguration.pipeline_entity_id];t.state!==i.state&&this._setTtsSettings()}}}render(){var t;const e=this.assistConfiguration?this.hass.states[this.assistConfiguration.pipeline_entity_id]:void 0,i=this.hass.devices[this.deviceId];return(0,a.dy)(b||(b=L`<div class="content">
        <img
          src="/static/images/voice-assistant/heart.png"
          alt="Casita Home Assistant logo"
        />
        <h1>
          ${0}
        </h1>
        <p class="secondary">
          ${0}
        </p>
        ${0}
        <div class="rows">
          <div class="row">
            <ha-textfield
              .label=${0}
              .placeholder=${0}
              .value=${0}
              @change=${0}
            ></ha-textfield>
          </div>
          ${0}
          ${0}
          ${0}
        </div>
      </div>
      <div class="footer">
        <ha-button @click=${0}
          >${0}</ha-button
        >
      </div>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.title"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.secondary"),this._error?(0,a.dy)(w||(w=L`<ha-alert alert-type="error">${0}</ha-alert>`),this._error):a.Ld,this.hass.localize("ui.panel.config.integrations.config_flow.device_name"),(0,l.wZ)(i,this.hass),null!==(t=this._deviceName)&&void 0!==t?t:(0,l.jL)(i),this._deviceNameChanged,this.assistConfiguration&&this.assistConfiguration.available_wake_words.length>1?(0,a.dy)($||($=L`<div class="row">
                <ha-select
                  .label=${0}
                  @closed=${0}
                  fixedMenuPosition
                  naturalMenuWidth
                  .value=${0}
                  @selected=${0}
                >
                  ${0}
                </ha-select>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${0}
                >
                  <ha-svg-icon
                    slot="start"
                    .path=${0}
                  ></ha-svg-icon>
                  ${0}
                </ha-button>
              </div>`),"Wake word",r.U,this.assistConfiguration.active_wake_words[0],this._wakeWordPicked,this.assistConfiguration.available_wake_words.map((t=>(0,a.dy)(C||(C=L`<ha-list-item .value=${0}>
                        ${0}
                      </ha-list-item>`),t.id,t.wake_word))),this._testWakeWord,E,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.test_wakeword")):a.Ld,e?(0,a.dy)(k||(k=L`<div class="row">
                <ha-select
                  .label=${0}
                  @closed=${0}
                  .value=${0}
                  fixedMenuPosition
                  naturalMenuWidth
                  @selected=${0}
                >
                  ${0}
                </ha-select>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${0}
                >
                  <ha-svg-icon slot="start" .path=${0}></ha-svg-icon>
                  ${0}
                </ha-button>
              </div>`),"Assistant",r.U,null==e?void 0:e.state,this._pipelinePicked,null==e?void 0:e.attributes.options.map((t=>(0,a.dy)(x||(x=L`<ha-list-item .value=${0}>
                        ${0}
                      </ha-list-item>`),t,this.hass.formatEntityState(e,t)))),this._openPipeline,O,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.edit_pipeline")):a.Ld,this._ttsSettings?(0,a.dy)(S||(S=L`<div class="row">
                <ha-tts-voice-picker
                  .hass=${0}
                  .engineId=${0}
                  .language=${0}
                  .value=${0}
                  @value-changed=${0}
                  @closed=${0}
                ></ha-tts-voice-picker>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${0}
                >
                  <ha-svg-icon slot="start" .path=${0}></ha-svg-icon>
                  ${0}
                </ha-button>
              </div>`),this.hass,this._ttsSettings.engine,this._ttsSettings.language,this._ttsSettings.voice,this._voicePicked,r.U,this._testTts,I,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.try_tts")):a.Ld,this._done,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.done"))}async _getPipeline(){var t,e;if(null===(t=this.assistConfiguration)||void 0===t||!t.pipeline_entity_id)return[void 0,void 0];const i=this.hass.states[null===(e=this.assistConfiguration)||void 0===e?void 0:e.pipeline_entity_id].state,s=await(0,c.SC)(this.hass);let a;return a="preferred"===i?s.pipelines.find((t=>t.id===s.preferred_pipeline)):s.pipelines.find((t=>t.name===i)),[a,s.preferred_pipeline]}_deviceNameChanged(t){this._deviceName=t.target.value}async _wakeWordPicked(t){const e=t.target.value;await(0,d.DT)(this.hass,this.assistEntityId,[e])}_pipelinePicked(t){const e=this.hass.states[this.assistConfiguration.pipeline_entity_id],i=t.target.value;i!==e.state&&e.attributes.options.includes(i)&&(0,p.n)(this.hass,e.entity_id,i)}async _setTtsSettings(){const[t]=await this._getPipeline();this._ttsSettings=t?{engine:t.tts_engine,voice:t.tts_voice,language:t.tts_language}:void 0}async _voicePicked(t){const[e]=await this._getPipeline();e&&await(0,c.af)(this.hass,e.id,Object.assign(Object.assign({},e),{},{tts_voice:t.detail.value}))}async _testTts(){const[t]=await this._getPipeline();if(t){if(t.language!==this.hass.locale.language)try{const e=await(0,v.i0)(null,t.language,!1);return void this._announce(e.data["ui.dialogs.tts-try.message_example"])}catch(e){}this._announce(this.hass.localize("ui.dialogs.tts-try.message_example"))}}async _announce(t){this.assistEntityId&&await(0,d.SY)(this.hass,this.assistEntityId,{message:t,preannounce:!1})}_testWakeWord(){(0,n.B)(this,"next-step",{step:y.STEP.WAKEWORD,nextStep:y.STEP.SUCCESS,updateConfig:!0})}async _openPipeline(){const[t]=await this._getPipeline();if(!t)return;const e=await(0,h.LI)(this.hass);(0,_.t)(this,{cloudActiveSubscription:e.logged_in&&e.active_subscription,pipeline:t,updatePipeline:async e=>{await(0,c.af)(this.hass,t.id,e)},hideWakeWord:!0})}async _done(){if(this._deviceName)try{(0,u.t1)(this.hass,this.deviceId,{name_by_user:this._deviceName})}catch(t){return void(this._error=this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.failed_rename",{error:t.message||t}))}(0,n.B)(this,"closed")}}A.styles=[f._,(0,a.iv)(z||(z=L`
      ha-md-list-item {
        text-align: initial;
      }
      ha-tts-voice-picker {
        display: block;
      }
      .footer {
        margin-top: 24px;
      }
      .rows {
        gap: 16px;
        display: flex;
        flex-direction: column;
      }
      .row {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .row > *:first-child {
        flex: 1;
        margin-right: 4px;
      }
      .row ha-button {
        width: 82px;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],A.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],A.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],A.prototype,"deviceId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],A.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.SB)()],A.prototype,"_ttsSettings",void 0),(0,s.__decorate)([(0,o.SB)()],A.prototype,"_error",void 0),A=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-success")],A),e()}catch(b){e(b)}}))},73801:function(t,e,i){i.a(t,(async function(t,e){try{i(26847),i(1455),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(21349),l=i(97862),c=i(64930),d=i(53258),h=i(67616),u=t([r,l,d]);[r,l,d]=u.then?(await u)():u;let p,_,g,v,f=t=>t;class y extends a.oi{willUpdate(t){if(super.willUpdate(t),this.updateEntityId){if(t.has("hass")&&this.updateEntityId){const e=t.get("hass");if(e){const t=e.states[this.updateEntityId],i=this.hass.states[this.updateEntityId];if((null==t?void 0:t.state)===c.nZ&&(null==i?void 0:i.state)!==c.nZ||(null==t?void 0:t.state)!==c.ON&&(null==i?void 0:i.state)===c.ON)return void this._tryUpdate(!1)}}t.has("updateEntityId")&&this._tryUpdate(!0)}else this._nextStep()}render(){if(!this.updateEntityId||!(this.updateEntityId in this.hass.states))return a.Ld;const t=this.hass.states[this.updateEntityId],e=t&&(0,d.SO)(t);return(0,a.dy)(p||(p=f`<div class="content">
      <img
        src="/static/images/voice-assistant/update.png"
        alt="Casita Home Assistant loading logo"
      />
      <h1>
        ${0}
      </h1>
      <p class="secondary">
        ${0}
      </p>
      ${0}
      <p>
        ${0}
      </p>
    </div>`),t&&("unavailable"===t.state||(0,d.Sk)(t))?this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.update.title"):this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.update.checking"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.update.secondary"),e?(0,a.dy)(_||(_=f`
            <ha-progress-ring
              .value=${0}
            ></ha-progress-ring>
          `),t.attributes.update_percentage):(0,a.dy)(g||(g=f`<ha-spinner></ha-spinner>`)),(null==t?void 0:t.state)===c.nZ?"Restarting voice assistant":e?`Installing ${t.attributes.update_percentage}%`:"")}async _tryUpdate(t){if(clearTimeout(this._refreshTimeout),!this.updateEntityId)return;const e=this.hass.states[this.updateEntityId];e&&this.hass.states[e.entity_id].state===c.ON&&(0,d.hF)(e)?(this._updated=!0,await this.hass.callService("update","install",{},{entity_id:e.entity_id})):t?(await this.hass.callService("homeassistant","update_entity",{},{entity_id:this.updateEntityId}),this._refreshTimeout=window.setTimeout((()=>{this._nextStep()}),1e4)):this._nextStep()}_nextStep(){(0,n.B)(this,"next-step",{noPrevious:!0,updateConfig:this._updated})}constructor(...t){super(...t),this._updated=!1}}y.styles=[h._,(0,a.iv)(v||(v=f`
      ha-progress-ring,
      ha-spinner {
        margin-top: 24px;
        margin-bottom: 24px;
      }
    `))],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],y.prototype,"updateEntityId",void 0),y=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-update")],y),e()}catch(p){e(p)}}))},54503:function(t,e,i){i.a(t,(async function(t,e){try{i(39710),i(26847),i(81738),i(29981),i(1455),i(56389),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(28105),r=i(29740),l=i(30337),c=i(97862),d=(i(76528),i(89275)),h=i(67616),u=i(52398),p=i(76151),_=t([l,c,u]);[l,c,u]=_.then?(await _)():_;let g,v,f,y,m,b,w,$=t=>t;class C extends a.oi{disconnectedCallback(){super.disconnectedCallback(),this._stopListeningWakeWord()}willUpdate(t){var e;(super.willUpdate(t),t.has("assistConfiguration")&&this.assistConfiguration&&!this.assistConfiguration.available_wake_words.length&&this._nextStep(),t.has("assistEntityId"))&&(this._detected=!1,this._muteSwitchEntity=null===(e=this.deviceEntities)||void 0===e||null===(e=e.find((t=>"switch"===(0,p.M)(t.entity_id)&&t.entity_id.includes("mute"))))||void 0===e?void 0:e.entity_id,this._muteSwitchEntity||this._startTimeOut(),this._listenWakeWord())}_startTimeOut(){this._timeout=window.setTimeout((()=>{this._timeout=void 0,this._timedout=!0}),15e3)}render(){if(!this.assistEntityId)return a.Ld;return"idle"!==this.hass.states[this.assistEntityId].state?(0,a.dy)(g||(g=$`<ha-spinner></ha-spinner>`)):(0,a.dy)(v||(v=$`<div class="content">
        ${0}
        ${0}
      </div>
      ${0}`),this._detected?(0,a.dy)(y||(y=$`<img
                src="/static/images/voice-assistant/ok-nabu.png"
                alt="Casita Home Assistant logo"
              />
              <h1>
                ${0}
              </h1>
              <p class="secondary">
                ${0}
              </p>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.title_2",{wakeword:this._activeWakeWord(this.assistConfiguration)}),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.secondary_2")):(0,a.dy)(f||(f=$`
          <img src="/static/images/voice-assistant/sleep.png" alt="Casita Home Assistant logo"/>
          <h1>
          ${0}  
          </h1>
          <p class="secondary">${0}</p>
        </div>`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.title",{wakeword:this._activeWakeWord(this.assistConfiguration)}),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.secondary")),this._timedout?(0,a.dy)(m||(m=$`<ha-alert alert-type="warning"
              >${0}</ha-alert
            >`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.time_out")):this._muteSwitchEntity&&"on"===this.hass.states[this._muteSwitchEntity].state?(0,a.dy)(b||(b=$`<ha-alert
                alert-type="warning"
                .title=${0}
                >${0}</ha-alert
              >`),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.muted"),this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.muted_description")):a.Ld,this.assistConfiguration&&this.assistConfiguration.available_wake_words.length>1?(0,a.dy)(w||(w=$`<div class="footer centered">
            <ha-button
              appearance="plain"
              size="small"
              @click=${0}
              >${0}</ha-button
            >
          </div>`),this._changeWakeWord,this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.change_wake_word")):a.Ld)}async _listenWakeWord(){const t=this.assistEntityId;t&&(await this._stopListeningWakeWord(),this._sub=(0,d.aJ)(this.hass,t,(()=>{this._timedout=!1,clearTimeout(this._timeout),this._stopListeningWakeWord(),this._detected?this._nextStep():(this._detected=!0,this._listenWakeWord())})))}async _stopListeningWakeWord(){try{var t;null===(t=await this._sub)||void 0===t||t()}catch(e){}this._sub=void 0}_nextStep(){(0,r.B)(this,"next-step")}_changeWakeWord(){(0,r.B)(this,"next-step",{step:u.STEP.CHANGE_WAKEWORD})}constructor(...t){super(...t),this._detected=!1,this._timedout=!1,this._activeWakeWord=(0,n.Z)((t=>{var e;if(!t)return"";const i=t.active_wake_words[0];return null===(e=t.available_wake_words.find((t=>t.id===i)))||void 0===e?void 0:e.wake_word}))}}C.styles=h._,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"deviceEntities",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_muteSwitchEntity",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_detected",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_timedout",void 0),C=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-wake-word")],C),e()}catch(g){e(g)}}))},51909:function(t,e,i){i.d(e,{F:function(){return a}});i(26847),i(87799),i(1455),i(27530);var s=i(29740);const a=(t,e)=>new Promise((a=>{const o=e.closeDialog,n=e.logInHereAction;(0,s.B)(t,"show-dialog",{dialogTag:"dialog-cloud-already-connected",dialogImport:()=>i.e("3898").then(i.bind(i,53530)),dialogParams:Object.assign(Object.assign({},e),{},{closeDialog:()=>{null==o||o(),a(!1)},logInHereAction:()=>{null==n||n(),a(!0)}})})}))},26665:function(t,e,i){i.d(e,{t:function(){return o}});i(26847),i(1455),i(27530);var s=i(29740);const a=()=>Promise.all([i.e("2335"),i.e("1705")]).then(i.bind(i,44062)),o=(t,e)=>{(0,s.B)(t,"show-dialog",{dialogTag:"dialog-voice-assistant-pipeline-detail",dialogImport:a,dialogParams:e})}},2180:function(t,e,i){i.d(e,{K:function(){return d}});i(39710),i(26847),i(87799),i(27530);var s=i(59048),a=i(79104),o=i(29740),n=i(74002),r=i(78001);class l extends HTMLElement{connectedCallback(){Object.assign(this.style,{position:"fixed",width:r.T?"100px":"50px",height:r.T?"100px":"50px",transform:"translate(-50%, -50%) scale(0)",pointerEvents:"none",zIndex:"999",background:"var(--primary-color)",display:null,opacity:"0.2",borderRadius:"50%",transition:"transform 180ms ease-in-out"}),["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((t=>{document.addEventListener(t,(()=>{this.cancelled=!0,this.timer&&(this._stopAnimation(),clearTimeout(this.timer),this.timer=void 0)}),{passive:!0})}))}bind(t,e={}){t.actionHandler&&(0,n.v)(e,t.actionHandler.options)||(t.actionHandler?(t.removeEventListener("touchstart",t.actionHandler.start),t.removeEventListener("touchend",t.actionHandler.end),t.removeEventListener("touchcancel",t.actionHandler.end),t.removeEventListener("mousedown",t.actionHandler.start),t.removeEventListener("click",t.actionHandler.end),t.removeEventListener("keydown",t.actionHandler.handleKeyDown)):t.addEventListener("contextmenu",(t=>{const e=t||window.event;return e.preventDefault&&e.preventDefault(),e.stopPropagation&&e.stopPropagation(),e.cancelBubble=!0,e.returnValue=!1,!1})),t.actionHandler={options:e},e.disabled||(t.actionHandler.start=t=>{let i,s;this.cancelled=!1,t.touches?(i=t.touches[0].clientX,s=t.touches[0].clientY):(i=t.clientX,s=t.clientY),e.hasHold&&(this.held=!1,this.timer=window.setTimeout((()=>{this._startAnimation(i,s),this.held=!0}),this.holdTime))},t.actionHandler.end=t=>{if("touchcancel"===t.type||"touchend"===t.type&&this.cancelled)return;const i=t.target;t.cancelable&&t.preventDefault(),e.hasHold&&(clearTimeout(this.timer),this._stopAnimation(),this.timer=void 0),e.hasHold&&this.held?(0,o.B)(i,"action",{action:"hold"}):e.hasDoubleClick?"click"===t.type&&t.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"double_tap"})):(0,o.B)(i,"action",{action:"tap"})},t.actionHandler.handleKeyDown=t=>{["Enter"," "].includes(t.key)&&t.currentTarget.actionHandler.end(t)},t.addEventListener("touchstart",t.actionHandler.start,{passive:!0}),t.addEventListener("touchend",t.actionHandler.end),t.addEventListener("touchcancel",t.actionHandler.end),t.addEventListener("mousedown",t.actionHandler.start,{passive:!0}),t.addEventListener("click",t.actionHandler.end),t.addEventListener("keydown",t.actionHandler.handleKeyDown)))}_startAnimation(t,e){Object.assign(this.style,{left:`${t}px`,top:`${e}px`,transform:"translate(-50%, -50%) scale(1)"})}_stopAnimation(){Object.assign(this.style,{left:null,top:null,transform:"translate(-50%, -50%) scale(0)"})}constructor(...t){super(...t),this.holdTime=500,this.held=!1,this.cancelled=!1}}customElements.define("action-handler",l);const c=(t,e)=>{const i=(()=>{const t=document.body;if(t.querySelector("action-handler"))return t.querySelector("action-handler");const e=document.createElement("action-handler");return t.appendChild(e),e})();i&&i.bind(t,e)},d=(0,a.XM)(class extends a.Xe{update(t,[e]){return c(t.element,e),s.Jb}render(t){}})},51496:function(t,e,i){i.d(e,{G:function(){return p}});i(26847),i(81738),i(72489),i(1455),i(27530);var s=i(29740),a=i(29173),o=i(19408),n=i(47469),r=i(81665);const l=()=>i.e("7395").then(i.bind(i,47609));var c=i(15606),d=(i(39710),i(56389),i(80092)),h=i(76151);const u=(t,e)=>((t,e,i=!0)=>{const s=(0,h.M)(e),a="group"===s?"homeassistant":s;let o;switch(s){case"lock":o=i?"unlock":"lock";break;case"cover":o=i?"open_cover":"close_cover";break;case"button":case"input_button":o="press";break;case"scene":o="turn_on";break;case"valve":o=i?"open_valve":"close_valve";break;default:o=i?"turn_on":"turn_off"}return t.callService(a,o,{entity_id:e})})(t,e,d.tj.includes(t.states[e].state)),p=async(t,e,i,d)=>{let h;if("double_tap"===d&&i.double_tap_action?h=i.double_tap_action:"hold"===d&&i.hold_action?h=i.hold_action:"tap"===d&&i.tap_action&&(h=i.tap_action),h||(h={action:"more-info"}),h.confirmation&&(!h.confirmation.exemptions||!h.confirmation.exemptions.some((t=>{var i;return t.user===(null===(i=e.user)||void 0===i?void 0:i.id)})))){let i;if((0,o.j)("warning"),"call-service"===h.action||"perform-action"===h.action){const[t,s]=(h.perform_action||h.service).split(".",2),a=e.services;if(t in a&&s in a[t]){await e.loadBackendTranslation("title");const o=await e.loadBackendTranslation("services");i=`${(0,n.Lh)(o,t)}: ${o(`component.${t}.services.${i}.name`)||a[t][s].name||s}`}}if(!(await(0,r.g7)(t,{text:h.confirmation.text||e.localize("ui.panel.lovelace.cards.actions.action_confirmation",{action:i||e.localize(`ui.panel.lovelace.editor.action-editor.actions.${h.action}`)||h.action})})))return}switch(h.action){case"more-info":{const a=h.entity||i.entity||i.camera_image||i.image_entity;a?(0,s.B)(t,"hass-more-info",{entityId:a}):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_entity_more_info")}),(0,o.j)("failure"));break}case"navigate":h.navigation_path?(0,a.c)(h.navigation_path,{replace:h.navigation_replace}):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_navigation_path")}),(0,o.j)("failure"));break;case"url":h.url_path?window.open(h.url_path):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_url")}),(0,o.j)("failure"));break;case"toggle":i.entity?(u(e,i.entity),(0,o.j)("light")):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_entity_toggle")}),(0,o.j)("failure"));break;case"perform-action":case"call-service":{var p;if(!h.perform_action&&!h.service)return(0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_action")}),void(0,o.j)("failure");const[i,s]=(h.perform_action||h.service).split(".",2);e.callService(i,s,null!==(p=h.data)&&void 0!==p?p:h.service_data,h.target),(0,o.j)("light");break}case"assist":var _,g;((t,e,i)=>{var a,o,n;null!==(a=e.auth.external)&&void 0!==a&&a.config.hasAssist?e.auth.external.fireMessage({type:"assist/show",payload:{pipeline_id:i.pipeline_id,start_listening:null===(n=i.start_listening)||void 0===n||n}}):(0,s.B)(t,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:l,dialogParams:{pipeline_id:i.pipeline_id,start_listening:null!==(o=i.start_listening)&&void 0!==o&&o}})})(t,e,{start_listening:null!==(_=h.start_listening)&&void 0!==_&&_,pipeline_id:null!==(g=h.pipeline_id)&&void 0!==g?g:"last_used"});break;case"fire-dom-event":(0,s.B)(t,"ll-custom",h)}}},28378:function(t,e,i){function s(t){return void 0!==t&&"none"!==t.action}function a(t){return!t.tap_action||s(t.tap_action)||s(t.hold_action)||s(t.double_tap_action)}i.d(e,{_:function(){return s},q:function(){return a}})},6251:function(t,e,i){i.d(e,{G2:function(){return n}});i(81738),i(72489),i(40777),i(6989),i(27087);function s(t,e){if(e.has("_config"))return!0;if(!e.has("hass"))return!1;const i=e.get("hass");return!i||(i.connected!==t.hass.connected||i.themes!==t.hass.themes||i.locale!==t.hass.locale||i.localize!==t.hass.localize||i.formatEntityState!==t.hass.formatEntityState||i.formatEntityAttributeName!==t.hass.formatEntityAttributeName||i.formatEntityAttributeValue!==t.hass.formatEntityAttributeValue||i.config.state!==t.hass.config.state)}function a(t,e,i){return t.states[i]!==e.states[i]}function o(t,e,i){const s=t.entities[i],a=e.entities[i];return(null==s?void 0:s.display_precision)!==(null==a?void 0:a.display_precision)}function n(t,e){if(s(t,e))return!0;if(!e.has("hass"))return!1;const i=e.get("hass"),n=t.hass;return a(i,n,t._config.entity)||o(i,n,t._config.entity)}},20376:function(t,e,i){i.a(t,(async function(t,e){try{i(39710),i(26847),i(56389),i(27530);var s=i(73742),a=i(59048),o=i(7616),n=i(31733),r=i(25191),l=i(80092),c=i(4757),d=i(76151),h=i(31298),u=i(37351),p=i(25661),_=i(2180),g=i(51496),v=i(28378),f=i(63605),y=i(41806),m=t([u,p]);[u,p]=m.then?(await m)():m;let b,w,$,C,k,x,S,z,L,O,E,I,A=t=>t;class P extends a.oi{render(){var t,e;if(!this.hass||!this.config)return a.Ld;const i=this.config.entity?this.hass.states[this.config.entity]:void 0;if(!i)return(0,a.dy)(b||(b=A`
        <hui-warning .hass=${0}>
          ${0}
        </hui-warning>
      `),this.hass,(0,f.i)(this.hass,this.config.entity));const s=(0,d.M)(this.config.entity),o=(0,v.q)(this.config),c=this.secondaryText||this.config.secondary_info,u=null!==(t=this.config.name)&&void 0!==t?t:(0,h.C)(i);return(0,a.dy)(w||(w=A`
      <div
        class="row ${0}"
        @action=${0}
        .actionHandler=${0}
        tabindex=${0}
      >
        <state-badge
          .hass=${0}
          .stateObj=${0}
          .overrideIcon=${0}
          .overrideImage=${0}
          .stateColor=${0}
        ></state-badge>
        ${0}
        ${0}
      </div>
    `),(0,n.$)({pointer:o}),this._handleAction,(0,_.K)({hasHold:(0,v._)(this.config.hold_action),hasDoubleClick:(0,v._)(this.config.double_tap_action)}),(0,r.o)(!this.config.tap_action||(0,v._)(this.config.tap_action)?"0":void 0),this.hass,i,this.config.icon,this.config.image,this.config.state_color,this.hideName?a.Ld:(0,a.dy)($||($=A`<div
              class="info ${0}"
              .title=${0}
            >
              ${0}
              ${0}
            </div>`),(0,n.$)({"text-content":!c}),u,this.config.name||(0,h.C)(i),c?(0,a.dy)(C||(C=A`
                    <div class="secondary">
                      ${0}
                    </div>
                  `),this.secondaryText||("entity-id"===this.config.secondary_info?i.entity_id:"last-changed"===this.config.secondary_info?(0,a.dy)(k||(k=A`
                              <ha-relative-time
                                .hass=${0}
                                .datetime=${0}
                                capitalize
                              ></ha-relative-time>
                            `),this.hass,i.last_changed):"last-updated"===this.config.secondary_info?(0,a.dy)(x||(x=A`
                                <ha-relative-time
                                  .hass=${0}
                                  .datetime=${0}
                                  capitalize
                                ></ha-relative-time>
                              `),this.hass,i.last_updated):"last-triggered"===this.config.secondary_info?i.attributes.last_triggered?(0,a.dy)(S||(S=A`
                                    <ha-relative-time
                                      .hass=${0}
                                      .datetime=${0}
                                      capitalize
                                    ></ha-relative-time>
                                  `),this.hass,i.attributes.last_triggered):this.hass.localize("ui.panel.lovelace.cards.entities.never_triggered"):"position"===this.config.secondary_info&&void 0!==i.attributes.current_position?`${this.hass.localize("ui.card.cover.position")}: ${i.attributes.current_position}`:"tilt-position"===this.config.secondary_info&&void 0!==i.attributes.current_tilt_position?`${this.hass.localize("ui.card.cover.tilt_position")}: ${i.attributes.current_tilt_position}`:"brightness"===this.config.secondary_info&&i.attributes.brightness?(0,a.dy)(z||(z=A`${0}
                                      %`),Math.round(i.attributes.brightness/255*100)):"state"===this.config.secondary_info?(0,a.dy)(L||(L=A`${0}`),this.hass.formatEntityState(i)):a.Ld)):a.Ld),(null!==(e=this.catchInteraction)&&void 0!==e?e:!l.AF.includes(s))?(0,a.dy)(O||(O=A`
              <div class="text-content value">
                <div class="state"><slot></slot></div>
              </div>
            `)):(0,a.dy)(E||(E=A`<slot
              @touchcancel=${0}
              @touchend=${0}
              @keydown=${0}
              @click=${0}
              @action=${0}
            ></slot>`),y.U,y.U,y.U,y.U,y.U))}updated(t){var e;super.updated(t),(0,c.X)(this,"no-secondary",!(this.secondaryText||null!==(e=this.config)&&void 0!==e&&e.secondary_info))}_handleAction(t){(0,g.G)(this,this.hass,this.config,t.detail.action)}constructor(...t){super(...t),this.hideName=!1}}P.styles=(0,a.iv)(I||(I=A`
    :host {
      display: flex;
      align-items: center;
      flex-direction: row;
    }
    .row {
      display: flex;
      align-items: center;
      flex-direction: row;
      width: 100%;
      outline: none;
      transition: background-color 180ms ease-in-out;
    }
    .row:focus-visible {
      background-color: var(--primary-background-color);
    }
    .info {
      padding-left: 16px;
      padding-right: 8px;
      padding-inline-start: 16px;
      padding-inline-end: 8px;
      flex: 1 1 30%;
    }
    .info,
    .info > * {
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .flex ::slotted(*) {
      margin-left: 8px;
      margin-inline-start: 8px;
      margin-inline-end: initial;
      min-width: 0;
    }
    .flex ::slotted([slot="secondary"]) {
      margin-left: 0;
      margin-inline-start: 0;
      margin-inline-end: initial;
    }
    .secondary,
    ha-relative-time {
      color: var(--secondary-text-color);
    }
    state-badge {
      flex: 0 0 40px;
    }
    .pointer {
      cursor: pointer;
    }
    .state {
      text-align: var(--float-end);
    }
    .value {
      direction: ltr;
    }
  `)),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],P.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],P.prototype,"config",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"secondary-text"})],P.prototype,"secondaryText",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"hide-name",type:Boolean})],P.prototype,"hideName",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"catch-interaction",type:Boolean})],P.prototype,"catchInteraction",void 0),P=(0,s.__decorate)([(0,o.Mo)("hui-generic-entity-row")],P),e()}catch(b){e(b)}}))},63605:function(t,e,i){i.d(e,{i:function(){return v}});var s=i(73742),a=i(92982),o=i(59048),n=i(7616);i(22543),i(26847),i(27530),i(13965),i(40830);let r,l,c,d,h=t=>t;const u={warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z"};class p extends o.oi{getCardSize(){return 1}getGridOptions(){return{columns:6,rows:this.preview?"auto":1,min_rows:1,min_columns:6,fixed_rows:this.preview}}setConfig(t){this._config=t,this.severity=t.severity||"error"}render(){var t,e,i,s;const a=(null===(t=this._config)||void 0===t?void 0:t.error)||(null===(e=this.hass)||void 0===e?void 0:e.localize("ui.errors.config.configuration_error")),n=void 0===this.hass||(null===(i=this.hass)||void 0===i||null===(i=i.user)||void 0===i?void 0:i.is_admin)||this.preview,d=this.preview;return(0,o.dy)(r||(r=h`
      <ha-card class="${0} ${0}">
        <div class="header">
          <div class="icon">
            <slot name="icon">
              <ha-svg-icon .path=${0}></ha-svg-icon>
            </slot>
          </div>
          ${0}
        </div>
        ${0}
      </ha-card>
    `),this.severity,n?"":"no-title",u[this.severity],n?(0,o.dy)(l||(l=h`<div class="title"><slot>${0}</slot></div>`),a):o.Ld,d&&null!==(s=this._config)&&void 0!==s&&s.message?(0,o.dy)(c||(c=h`<div class="message">${0}</div>`),this._config.message):o.Ld)}constructor(...t){super(...t),this.preview=!1,this.severity="error"}}p.styles=(0,o.iv)(d||(d=h`
    ha-card {
      height: 100%;
      border-width: 0;
    }
    ha-card::after {
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      opacity: 0.12;
      pointer-events: none;
      content: "";
      border-radius: var(--ha-card-border-radius, 12px);
    }
    .header {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 16px;
    }
    .message {
      padding: 0 16px 16px 16px;
    }
    .no-title {
      justify-content: center;
    }
    .title {
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
      font-weight: var(--ha-font-weight-bold);
    }
    ha-card.warning .icon {
      color: var(--warning-color);
    }
    ha-card.warning::after {
      background-color: var(--warning-color);
    }
    ha-card.error .icon {
      color: var(--error-color);
    }
    ha-card.error::after {
      background-color: var(--error-color);
    }
  `)),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],p.prototype,"preview",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:"severity"})],p.prototype,"severity",void 0),(0,s.__decorate)([(0,n.SB)()],p.prototype,"_config",void 0),p=(0,s.__decorate)([(0,n.Mo)("hui-error-card")],p);let _,g=t=>t;const v=(t,e)=>t.config.state!==a.UE?t.localize("ui.card.common.entity_not_found"):t.localize("ui.panel.lovelace.warning.starting");class f extends o.oi{render(){return(0,o.dy)(_||(_=g`<hui-error-card .hass=${0} severity="warning"
      ><slot></slot
    ></hui-error-card>`),this.hass)}}(0,s.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"hass",void 0),f=(0,s.__decorate)([(0,n.Mo)("hui-warning")],f)},74183:function(t,e,i){i.a(t,(async function(t,e){try{i(40777),i(39710),i(81738),i(6989),i(56389);var s=i(73742),a=i(59048),o=i(7616),n=i(41806),r=i(31298),l=(i(93795),i(29490),i(64930)),c=i(19408),d=i(12593),h=i(6251),u=i(20376),p=i(63605),_=t([u]);u=(_.then?(await _)():_)[0];let g,v,f,y,m=t=>t;class b extends a.oi{setConfig(t){if(!t||!t.entity)throw new Error("Entity must be specified");this._config=t}shouldUpdate(t){return(0,h.G2)(this,t)}render(){if(!this.hass||!this._config)return a.Ld;const t=this.hass.states[this._config.entity];return t?(0,a.dy)(v||(v=m`
      <hui-generic-entity-row
        .hass=${0}
        .config=${0}
        hide-name
      >
        <ha-select
          .label=${0}
          .value=${0}
          .options=${0}
          .disabled=${0}
          naturalMenuWidth
          @action=${0}
          @click=${0}
          @closed=${0}
        >
          ${0}
        </ha-select>
      </hui-generic-entity-row>
    `),this.hass,this._config,this._config.name||(0,r.C)(t),t.state,t.attributes.options,t.state===l.nZ,this._handleAction,n.U,n.U,t.attributes.options?t.attributes.options.map((e=>(0,a.dy)(f||(f=m`
                  <ha-list-item .value=${0}>
                    ${0}
                  </ha-list-item>
                `),e,this.hass.formatEntityState(t,e)))):""):(0,a.dy)(g||(g=m`
        <hui-warning .hass=${0}>
          ${0}
        </hui-warning>
      `),this.hass,(0,p.i)(this.hass,this._config.entity))}_handleAction(t){const e=this.hass.states[this._config.entity],i=t.target.value;i!==e.state&&e.attributes.options.includes(i)&&((0,c.j)("light"),(0,d.n)(this.hass,e.entity_id,i))}}b.styles=(0,a.iv)(y||(y=m`
    hui-generic-entity-row {
      display: flex;
      align-items: center;
    }
    ha-select {
      width: 100%;
      --ha-select-min-width: 0;
    }
  `)),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],b.prototype,"_config",void 0),b=(0,s.__decorate)([(0,o.Mo)("hui-select-entity-row")],b),e()}catch(g){e(g)}}))},78001:function(t,e,i){i.d(e,{T:function(){return s}});const s="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0},15606:function(t,e,i){i.d(e,{C:function(){return a}});var s=i(29740);const a=(t,e)=>(0,s.B)(t,"hass-notification",e)}}]);
//# sourceMappingURL=9762.25143aae16867037.js.map