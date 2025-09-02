/*! For license information please see 9548.c3b48172a6b527f1.js.LICENSE.txt */
export const __webpack_ids__=["9548"];export const __webpack_modules__={13539:function(t,e,i){i.d(e,{Bt:()=>n});var s=i(3574),a=i(1066);const o=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],n=t=>t.first_weekday===a.FS.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(t.language).weekInfo.firstDay%7:(0,s.L)(t.language)%7:o.includes(t.first_weekday)?o.indexOf(t.first_weekday):1},60495:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{G:()=>c});var a=i(57900),o=i(28105),n=i(58713),r=t([a,n]);[a,n]=r.then?(await r)():r;const l=(0,o.Z)((t=>new Intl.RelativeTimeFormat(t.language,{numeric:"auto"}))),c=(t,e,i,s=!0)=>{const a=(0,n.W)(t,i,e);return s?l(e).format(a.value,a.unit):Intl.NumberFormat(e.language,{style:"unit",unit:a.unit,unitDisplay:"long"}).format(Math.abs(a.value))};s()}catch(l){s(l)}}))},4757:function(t,e,i){i.d(e,{X:()=>s});const s=(t,e,i)=>(void 0!==i&&(i=!!i),t.hasAttribute(e)?!!i||(t.removeAttribute(e),!1):!1!==i&&(t.setAttribute(e,""),!0))},75972:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{u:()=>r});var a=i(57900),o=i(28105),n=t([a]);a=(n.then?(await n)():n)[0];const r=(t,e)=>{try{return l(e)?.of(t)??t}catch{return t}},l=(0,o.Z)((t=>new Intl.DisplayNames(t.language,{type:"language",fallback:"code"})));s()}catch(r){s(r)}}))},31132:function(t,e,i){i.d(e,{f:()=>s});const s=t=>t.charAt(0).toUpperCase()+t.slice(1)},74002:function(t,e,i){i.d(e,{v:()=>s});const s=(t,e)=>{if(t===e)return!0;if(t&&e&&"object"==typeof t&&"object"==typeof e){if(t.constructor!==e.constructor)return!1;let i,a;if(Array.isArray(t)){if(a=t.length,a!==e.length)return!1;for(i=a;0!=i--;)if(!s(t[i],e[i]))return!1;return!0}if(t instanceof Map&&e instanceof Map){if(t.size!==e.size)return!1;for(i of t.entries())if(!e.has(i[0]))return!1;for(i of t.entries())if(!s(i[1],e.get(i[0])))return!1;return!0}if(t instanceof Set&&e instanceof Set){if(t.size!==e.size)return!1;for(i of t.entries())if(!e.has(i[0]))return!1;return!0}if(ArrayBuffer.isView(t)&&ArrayBuffer.isView(e)){if(a=t.length,a!==e.length)return!1;for(i=a;0!=i--;)if(t[i]!==e[i])return!1;return!0}if(t.constructor===RegExp)return t.source===e.source&&t.flags===e.flags;if(t.valueOf!==Object.prototype.valueOf)return t.valueOf()===e.valueOf();if(t.toString!==Object.prototype.toString)return t.toString()===e.toString();const o=Object.keys(t);if(a=o.length,a!==Object.keys(e).length)return!1;for(i=a;0!=i--;)if(!Object.prototype.hasOwnProperty.call(e,o[i]))return!1;for(i=a;0!=i--;){const a=o[i];if(!s(t[a],e[a]))return!1}return!0}return t!=t&&e!=e}},58713:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{W:()=>p});var a=i(7722),o=i(66233),n=i(41238),r=i(13539);const c=1e3,d=60,h=60*d;function p(t,e=Date.now(),i,s={}){const l={...u,...s||{}},p=(+t-+e)/c;if(Math.abs(p)<l.second)return{value:Math.round(p),unit:"second"};const _=p/d;if(Math.abs(_)<l.minute)return{value:Math.round(_),unit:"minute"};const g=p/h;if(Math.abs(g)<l.hour)return{value:Math.round(g),unit:"hour"};const v=new Date(t),f=new Date(e);v.setHours(0,0,0,0),f.setHours(0,0,0,0);const y=(0,a.j)(v,f);if(0===y)return{value:Math.round(g),unit:"hour"};if(Math.abs(y)<l.day)return{value:y,unit:"day"};const m=(0,r.Bt)(i),b=(0,o.z)(v,{weekStartsOn:m}),w=(0,o.z)(f,{weekStartsOn:m}),$=(0,n.p)(b,w);if(0===$)return{value:y,unit:"day"};if(Math.abs($)<l.week)return{value:$,unit:"week"};const C=v.getFullYear()-f.getFullYear(),x=12*C+v.getMonth()-f.getMonth();return 0===x?{value:$,unit:"week"}:Math.abs(x)<l.month||0===C?{value:x,unit:"month"}:{value:Math.round(C),unit:"year"}}const u={second:45,minute:45,hour:22,day:5,week:4,month:11};s()}catch(l){s(l)}}))},62335:function(t,e,i){var s=i(73742),a=i(27885),o=i(67522),n=i(23533),r=i(7046),l=i(59048),c=i(7616);class d extends a.g{renderOutline(){return this.filled?l.dy`<span class="filled"></span>`:super.renderOutline()}getContainerClasses(){return{...super.getContainerClasses(),active:this.active}}renderPrimaryContent(){return l.dy`
      <span class="leading icon" aria-hidden="true">
        ${this.renderLeadingIcon()}
      </span>
      <span class="label">${this.label}</span>
      <span class="touch"></span>
      <span class="trailing leading icon" aria-hidden="true">
        ${this.renderTrailingIcon()}
      </span>
    `}renderTrailingIcon(){return l.dy`<slot name="trailing-icon"></slot>`}constructor(...t){super(...t),this.filled=!1,this.active=!1}}d.styles=[n.W,r.W,o.W,l.iv`
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
    `],(0,s.__decorate)([(0,c.Cb)({type:Boolean,reflect:!0})],d.prototype,"filled",void 0),(0,s.__decorate)([(0,c.Cb)({type:Boolean})],d.prototype,"active",void 0),d=(0,s.__decorate)([(0,c.Mo)("ha-assist-chip")],d)},86352:function(t,e,i){i.a(t,(async function(t,s){try{i.d(e,{C:()=>g});var a=i(57900),o=i(73742),n=i(59048),r=i(7616),l=i(28105),c=i(29740),d=i(41806),h=i(75972),p=i(92949),u=i(18447),_=(i(93795),i(29490),t([a,h]));[a,h]=_.then?(await _)():_;const g=(t,e,i,s)=>{let a=[];if(e){const e=u.o.translations;a=t.map((t=>{let i=e[t]?.nativeName;if(!i)try{i=new Intl.DisplayNames(t,{type:"language",fallback:"code"}).of(t)}catch(s){i=t}return{value:t,label:i}}))}else s&&(a=t.map((t=>({value:t,label:(0,h.u)(t,s)}))));return!i&&s&&a.sort(((t,e)=>(0,p.fe)(t.label,e.label,s.language))),a};class v extends n.oi{firstUpdated(t){super.firstUpdated(t),this._computeDefaultLanguageOptions()}updated(t){super.updated(t);const e=t.has("hass")&&this.hass&&t.get("hass")&&t.get("hass").locale.language!==this.hass.locale.language;if(t.has("languages")||t.has("value")||e){if(this._select.layoutOptions(),this.disabled||this._select.value===this.value||(0,c.B)(this,"value-changed",{value:this._select.value}),!this.value)return;const t=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.noSort,this.hass?.locale).findIndex((t=>t.value===this.value));-1===t&&(this.value=void 0),e&&this._select.select(t)}}_computeDefaultLanguageOptions(){this._defaultLanguages=Object.keys(u.o.translations)}render(){const t=this._getLanguagesOptions(this.languages??this._defaultLanguages,this.nativeName,this.noSort,this.hass?.locale),e=this.value??(this.required&&!this.disabled?t[0]?.value:this.value);return n.dy`
      <ha-select
        .label=${this.label??(this.hass?.localize("ui.components.language-picker.language")||"Language")}
        .value=${e||""}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${d.U}
        fixedMenuPosition
        naturalMenuWidth
        .inlineArrow=${this.inlineArrow}
      >
        ${0===t.length?n.dy`<ha-list-item value=""
              >${this.hass?.localize("ui.components.language-picker.no_languages")||"No languages"}</ha-list-item
            >`:t.map((t=>n.dy`
                <ha-list-item .value=${t.value}
                  >${t.label}</ha-list-item
                >
              `))}
      </ha-select>
    `}_changed(t){const e=t.target;this.disabled||""===e.value||e.value===this.value||(this.value=e.value,(0,c.B)(this,"value-changed",{value:this.value}))}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this.nativeName=!1,this.noSort=!1,this.inlineArrow=!1,this._defaultLanguages=[],this._getLanguagesOptions=(0,l.Z)(g)}}v.styles=n.iv`
    ha-select {
      width: 100%;
    }
  `,(0,o.__decorate)([(0,r.Cb)()],v.prototype,"value",void 0),(0,o.__decorate)([(0,r.Cb)()],v.prototype,"label",void 0),(0,o.__decorate)([(0,r.Cb)({type:Array})],v.prototype,"languages",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:!1})],v.prototype,"hass",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean,reflect:!0})],v.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.Cb)({type:Boolean})],v.prototype,"required",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"native-name",type:Boolean})],v.prototype,"nativeName",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"no-sort",type:Boolean})],v.prototype,"noSort",void 0),(0,o.__decorate)([(0,r.Cb)({attribute:"inline-arrow",type:Boolean})],v.prototype,"inlineArrow",void 0),(0,o.__decorate)([(0,r.SB)()],v.prototype,"_defaultLanguages",void 0),(0,o.__decorate)([(0,r.IO)("ha-select")],v.prototype,"_select",void 0),v=(0,o.__decorate)([(0,r.Mo)("ha-language-picker")],v),s()}catch(g){s(g)}}))},51431:function(t,e,i){var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(90380),i(10051)),l=i(91646),c=i(67419);class d extends r.v2{connectedCallback(){super.connectedCallback(),this.addEventListener("close-menu",this._handleCloseMenu)}_handleCloseMenu(t){t.detail.reason.kind===c.GB.KEYDOWN&&t.detail.reason.key===c.KC.ESCAPE||t.detail.initiator.clickAction?.(t.detail.initiator)}}d.styles=[l.W,a.iv`
      :host {
        --md-sys-color-surface-container: var(--card-background-color);
      }
    `],d=(0,s.__decorate)([(0,o.Mo)("ha-md-menu")],d);class h extends a.oi{get items(){return this._menu.items}focus(){this._menu.open?this._menu.focus():this._triggerButton?.focus()}render(){return a.dy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <ha-md-menu
        .positioning=${this.positioning}
        .hasOverflow=${this.hasOverflow}
        @opening=${this._handleOpening}
        @closing=${this._handleClosing}
      >
        <slot></slot>
      </ha-md-menu>
    `}_handleOpening(){(0,n.B)(this,"opening",void 0,{composed:!1})}_handleClosing(){(0,n.B)(this,"closing",void 0,{composed:!1})}_handleClick(){this.disabled||(this._menu.anchorElement=this,this._menu.open?this._menu.close():this._menu.show())}get _triggerButton(){return this.querySelector('ha-icon-button[slot="trigger"], ha-button[slot="trigger"], ha-assist-chip[slot="trigger"]')}_setTriggerAria(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}constructor(...t){super(...t),this.disabled=!1,this.hasOverflow=!1}}h.styles=a.iv`
    :host {
      display: inline-block;
      position: relative;
    }
    ::slotted([disabled]) {
      color: var(--disabled-text-color);
    }
  `,(0,s.__decorate)([(0,o.Cb)({type:Boolean})],h.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)()],h.prototype,"positioning",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,attribute:"has-overflow"})],h.prototype,"hasOverflow",void 0),(0,s.__decorate)([(0,o.IO)("ha-md-menu",!0)],h.prototype,"_menu",void 0),h=(0,s.__decorate)([(0,o.Mo)("ha-md-button-menu")],h)},20455:function(t,e,i){var s=i(73742),a=i(59048),o=i(7616);i(78645),i(38573);class n extends a.oi{render(){return a.dy`<ha-textfield
        .invalid=${this.invalid}
        .errorMessage=${this.errorMessage}
        .icon=${this.icon}
        .iconTrailing=${this.iconTrailing}
        .autocomplete=${this.autocomplete}
        .autocorrect=${this.autocorrect}
        .inputSpellcheck=${this.inputSpellcheck}
        .value=${this.value}
        .placeholder=${this.placeholder}
        .label=${this.label}
        .disabled=${this.disabled}
        .required=${this.required}
        .minLength=${this.minLength}
        .maxLength=${this.maxLength}
        .outlined=${this.outlined}
        .helper=${this.helper}
        .validateOnInitialRender=${this.validateOnInitialRender}
        .validationMessage=${this.validationMessage}
        .autoValidate=${this.autoValidate}
        .pattern=${this.pattern}
        .size=${this.size}
        .helperPersistent=${this.helperPersistent}
        .charCounter=${this.charCounter}
        .endAligned=${this.endAligned}
        .prefix=${this.prefix}
        .name=${this.name}
        .inputMode=${this.inputMode}
        .readOnly=${this.readOnly}
        .autocapitalize=${this.autocapitalize}
        .type=${this._unmaskedPassword?"text":"password"}
        .suffix=${a.dy`<div style="width: 24px"></div>`}
        @input=${this._handleInputEvent}
        @change=${this._handleChangeEvent}
      ></ha-textfield>
      <ha-icon-button
        .label=${this.hass?.localize(this._unmaskedPassword?"ui.components.selectors.text.hide_password":"ui.components.selectors.text.show_password")||(this._unmaskedPassword?"Hide password":"Show password")}
        @click=${this._toggleUnmaskedPassword}
        .path=${this._unmaskedPassword?"M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.08L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.74,7.13 11.35,7 12,7Z":"M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"}
      ></ha-icon-button>`}focus(){this._textField.focus()}checkValidity(){return this._textField.checkValidity()}reportValidity(){return this._textField.reportValidity()}setCustomValidity(t){return this._textField.setCustomValidity(t)}layout(){return this._textField.layout()}_toggleUnmaskedPassword(){this._unmaskedPassword=!this._unmaskedPassword}_handleInputEvent(t){this.value=t.target.value}_handleChangeEvent(t){this.value=t.target.value,this._reDispatchEvent(t)}_reDispatchEvent(t){const e=new Event(t.type,t);this.dispatchEvent(e)}constructor(...t){super(...t),this.icon=!1,this.iconTrailing=!1,this.value="",this.placeholder="",this.label="",this.disabled=!1,this.required=!1,this.minLength=-1,this.maxLength=-1,this.outlined=!1,this.helper="",this.validateOnInitialRender=!1,this.validationMessage="",this.autoValidate=!1,this.pattern="",this.size=null,this.helperPersistent=!1,this.charCounter=!1,this.endAligned=!1,this.prefix="",this.suffix="",this.name="",this.readOnly=!1,this.autocapitalize="",this._unmaskedPassword=!1}}n.styles=a.iv`
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
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],n.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"invalid",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"error-message"})],n.prototype,"errorMessage",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"icon",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"iconTrailing",void 0),(0,s.__decorate)([(0,o.Cb)()],n.prototype,"autocomplete",void 0),(0,s.__decorate)([(0,o.Cb)()],n.prototype,"autocorrect",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"input-spellcheck"})],n.prototype,"inputSpellcheck",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"placeholder",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],n.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"required",void 0),(0,s.__decorate)([(0,o.Cb)({type:Number})],n.prototype,"minLength",void 0),(0,s.__decorate)([(0,o.Cb)({type:Number})],n.prototype,"maxLength",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],n.prototype,"outlined",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"helper",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"validateOnInitialRender",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"validationMessage",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"autoValidate",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"pattern",void 0),(0,s.__decorate)([(0,o.Cb)({type:Number})],n.prototype,"size",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"helperPersistent",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"charCounter",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"endAligned",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"prefix",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"suffix",void 0),(0,s.__decorate)([(0,o.Cb)({type:String})],n.prototype,"name",void 0),(0,s.__decorate)([(0,o.Cb)({type:String,attribute:"input-mode"})],n.prototype,"inputMode",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],n.prototype,"readOnly",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1,type:String})],n.prototype,"autocapitalize",void 0),(0,s.__decorate)([(0,o.SB)()],n.prototype,"_unmaskedPassword",void 0),(0,s.__decorate)([(0,o.IO)("ha-textfield")],n.prototype,"_textField",void 0),(0,s.__decorate)([(0,o.hO)({passive:!0})],n.prototype,"_handleInputEvent",null),(0,s.__decorate)([(0,o.hO)({passive:!0})],n.prototype,"_handleChangeEvent",null),n=(0,s.__decorate)([(0,o.Mo)("ha-password-field")],n)},25661:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(78722),o=i(59048),n=i(7616),r=i(60495),l=i(31132),c=t([r]);r=(c.then?(await c)():c)[0];class d extends o.fl{disconnectedCallback(){super.disconnectedCallback(),this._clearInterval()}connectedCallback(){super.connectedCallback(),this.datetime&&this._startInterval()}createRenderRoot(){return this}firstUpdated(t){super.firstUpdated(t),this._updateRelative()}update(t){super.update(t),this._updateRelative()}_clearInterval(){this._interval&&(window.clearInterval(this._interval),this._interval=void 0)}_startInterval(){this._clearInterval(),this._interval=window.setInterval((()=>this._updateRelative()),6e4)}_updateRelative(){if(this.datetime){const t="string"==typeof this.datetime?(0,a.D)(this.datetime):this.datetime,e=(0,r.G)(t,this.hass.locale);this.innerHTML=this.capitalize?(0,l.f)(e):e}else this.innerHTML=this.hass.localize("ui.components.relative_time.never")}constructor(...t){super(...t),this.capitalize=!1}}(0,s.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,s.__decorate)([(0,n.Cb)({attribute:!1})],d.prototype,"datetime",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],d.prototype,"capitalize",void 0),d=(0,s.__decorate)([(0,n.Mo)("ha-relative-time")],d),e()}catch(d){e(d)}}))},80443:function(t,e,i){var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(41806),l=i(16811),c=i(75055);i(93795),i(29490);const d="__NONE_OPTION__";class h extends a.oi{render(){if(!this._voices)return a.Ld;const t=this.value??(this.required?this._voices[0]?.voice_id:d);return a.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${t}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${r.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?a.Ld:a.dy`<ha-list-item .value=${d}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((t=>a.dy`<ha-list-item .value=${t.voice_id}>
              ${t.name}
            </ha-list-item>`))}
      </ha-select>
    `}willUpdate(t){super.willUpdate(t),this.hasUpdated?(t.has("language")||t.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}async _updateVoices(){this.engineId&&this.language?(this._voices=(await(0,c.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((t=>t.voice_id===this.value))||(this.value=void 0,(0,n.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}updated(t){super.updated(t),t.has("_voices")&&this._select?.value!==this.value&&(this._select?.layoutOptions(),(0,n.B)(this,"value-changed",{value:this._select?.value}))}_changed(t){const e=t.target;!this.hass||""===e.value||e.value===this.value||void 0===this.value&&e.value===d||(this.value=e.value===d?void 0:e.value,(0,n.B)(this,"value-changed",{value:this.value}))}constructor(...t){super(...t),this.disabled=!1,this.required=!1,this._debouncedUpdateVoices=(0,l.D)((()=>this._updateVoices()),500)}}h.styles=a.iv`
    ha-select {
      width: 100%;
    }
  `,(0,s.__decorate)([(0,o.Cb)()],h.prototype,"value",void 0),(0,s.__decorate)([(0,o.Cb)()],h.prototype,"label",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],h.prototype,"engineId",void 0),(0,s.__decorate)([(0,o.Cb)()],h.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean,reflect:!0})],h.prototype,"disabled",void 0),(0,s.__decorate)([(0,o.Cb)({type:Boolean})],h.prototype,"required",void 0),(0,s.__decorate)([(0,o.SB)()],h.prototype,"_voices",void 0),(0,s.__decorate)([(0,o.IO)("ha-select")],h.prototype,"_select",void 0),h=(0,s.__decorate)([(0,o.Mo)("ha-tts-voice-picker")],h)},32518:function(t,e,i){i.d(e,{Dy:()=>c,PA:()=>n,SC:()=>o,Xp:()=>a,af:()=>l,eP:()=>s,jZ:()=>r});const s=(t,e,i)=>"run-start"===e.type?t={init_options:i,stage:"ready",run:e.data,events:[e]}:t?((t="wake_word-start"===e.type?{...t,stage:"wake_word",wake_word:{...e.data,done:!1}}:"wake_word-end"===e.type?{...t,wake_word:{...t.wake_word,...e.data,done:!0}}:"stt-start"===e.type?{...t,stage:"stt",stt:{...e.data,done:!1}}:"stt-end"===e.type?{...t,stt:{...t.stt,...e.data,done:!0}}:"intent-start"===e.type?{...t,stage:"intent",intent:{...e.data,done:!1}}:"intent-end"===e.type?{...t,intent:{...t.intent,...e.data,done:!0}}:"tts-start"===e.type?{...t,stage:"tts",tts:{...e.data,done:!1}}:"tts-end"===e.type?{...t,tts:{...t.tts,...e.data,done:!0}}:"run-end"===e.type?{...t,stage:"done"}:"error"===e.type?{...t,stage:"error",error:e.data}:{...t}).events=[...t.events,e],t):void console.warn("Received unexpected event before receiving session",e),a=(t,e,i)=>t.connection.subscribeMessage(e,{...i,type:"assist_pipeline/run"}),o=t=>t.callWS({type:"assist_pipeline/pipeline/list"}),n=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/get",pipeline_id:e}),r=(t,e)=>t.callWS({type:"assist_pipeline/pipeline/create",...e}),l=(t,e,i)=>t.callWS({type:"assist_pipeline/pipeline/update",pipeline_id:e,...i}),c=t=>t.callWS({type:"assist_pipeline/language/list"})},33848:function(t,e,i){i.d(e,{LI:()=>n,_Y:()=>s,_t:()=>o,bi:()=>a});const s=({hass:t,...e})=>t.callApi("POST","cloud/login",e),a=(t,e,i)=>t.callApi("POST","cloud/register",{email:e,password:i}),o=(t,e)=>t.callApi("POST","cloud/resend_confirm",{email:e}),n=t=>t.callWS({type:"cloud/status"})},59753:function(t,e,i){i.d(e,{KH:()=>o,rM:()=>a,zt:()=>s});var s=function(t){return t[t.CONTROL=1]="CONTROL",t}({});const a=(t,e,i)=>t.callWS({type:"conversation/agent/list",language:e,country:i}),o=(t,e,i)=>t.callWS({type:"conversation/agent/homeassistant/language_scores",language:e,country:i})},81086:function(t,e,i){i.d(e,{fU:()=>r,kP:()=>n,yt:()=>o});var s=i(35859),a=i(10840);const o=async t=>(0,s.I)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):(0,a.rY)(await t.callApi("GET","hassio/addons")),n=async(t,e)=>(0,s.I)(t.config.version,2021,2,4)?t.callWS({type:"supervisor/api",endpoint:`/addons/${e}/start`,method:"post",timeout:null}):t.callApi("POST",`hassio/addons/${e}/start`),r=async(t,e)=>{(0,s.I)(t.config.version,2021,2,4)?await t.callWS({type:"supervisor/api",endpoint:`/addons/${e}/install`,method:"post",timeout:null}):await t.callApi("POST",`hassio/addons/${e}/install`)}},10840:function(t,e,i){i.d(e,{js:()=>a,rY:()=>s});const s=t=>t.data,a=t=>"object"==typeof t?"object"==typeof t.body?t.body.message||"Unknown error, see supervisor logs":t.body||t.message||"Unknown error, see supervisor logs":t;new Set([502,503,504])},12593:function(t,e,i){i.d(e,{n:()=>s});const s=(t,e,i)=>t.callService("select","select_option",{option:i},{entity_id:e})},70937:function(t,e,i){i.d(e,{m:()=>s});const s=(t,e,i)=>t.callWS({type:"stt/engine/list",language:e,country:i})},75055:function(t,e,i){i.d(e,{MV:()=>c,Wg:()=>r,Xk:()=>n,aT:()=>s,b_:()=>o,yP:()=>l});const s=(t,e)=>t.callApi("POST","tts_get_url",e),a="media-source://tts/",o=t=>t.startsWith(a),n=t=>t.substring(19),r=(t,e,i)=>t.callWS({type:"tts/engine/list",language:e,country:i}),l=(t,e)=>t.callWS({type:"tts/engine/get",engine_id:e}),c=(t,e,i)=>t.callWS({type:"tts/engine/voices",engine_id:e,language:i})},33328:function(t,e,i){i.d(e,{w:()=>s});const s=t=>t.callWS({type:"wyoming/info"})},39894:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(30337),l=(i(40830),i(37198)),c=i(67616),d=t([r]);r=(d.then?(await d)():d)[0];const h="M17.9,17.39C17.64,16.59 16.89,16 16,16H15V13A1,1 0 0,0 14,12H8V10H10A1,1 0 0,0 11,9V7H13A2,2 0 0,0 15,5V4.59C17.93,5.77 20,8.64 20,12C20,14.08 19.2,15.97 17.9,17.39M11,19.93C7.05,19.44 4,16.08 4,12C4,11.38 4.08,10.78 4.21,10.21L9,15V16A2,2 0 0,0 11,18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z",p="M8,7A2,2 0 0,1 10,9V14A2,2 0 0,1 8,16A2,2 0 0,1 6,14V9A2,2 0 0,1 8,7M14,14C14,16.97 11.84,19.44 9,19.92V22H7V19.92C4.16,19.44 2,16.97 2,14H4A4,4 0 0,0 8,18A4,4 0 0,0 12,14H14M21.41,9.41L17.17,13.66L18.18,10H14A2,2 0 0,1 12,8V4A2,2 0 0,1 14,2H20A2,2 0 0,1 22,4V8C22,8.55 21.78,9.05 21.41,9.41Z",u="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class _ extends a.oi{render(){return a.dy`<div class="content">
        <img
          src=${`/static/images/logo_nabu_casa${this.hass.themes?.darkMode?"_dark":""}.png`}
          alt="Nabu Casa logo"
        />
        <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.cloud.title")}
        </h1>
        <div class="features">
          <div class="feature speech">
            <div class="logos">
              <div class="round-icon">
                <ha-svg-icon .path=${p}></ha-svg-icon>
              </div>
            </div>
            <h2>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.speech.title")}
              <span class="no-wrap"></span>
            </h2>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.speech.text")}
            </p>
          </div>
          <div class="feature access">
            <div class="logos">
              <div class="round-icon">
                <ha-svg-icon .path=${h}></ha-svg-icon>
              </div>
            </div>
            <h2>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.remote_access.title")}
              <span class="no-wrap"></span>
            </h2>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.remote_access.text")}
            </p>
          </div>
          <div class="feature">
            <div class="logos">
              <img
                alt="Google Assistant"
                src=${(0,l.X1)({domain:"google_assistant",type:"icon",darkOptimized:this.hass.themes?.darkMode})}
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
              />
              <img
                alt="Amazon Alexa"
                src=${(0,l.X1)({domain:"alexa",type:"icon",darkOptimized:this.hass.themes?.darkMode})}
                crossorigin="anonymous"
                referrerpolicy="no-referrer"
              />
            </div>
            <h2>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.assistants.title")}
            </h2>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.assistants.cloud.features.assistants.text")}
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
          <ha-svg-icon .path=${u} slot="start"></ha-svg-icon>
          nabucasa.com
        </ha-button>
        <ha-button @click=${this._signUp}
          >${this.hass.localize("ui.panel.config.cloud.register.headline")}</ha-button
        >
      </div>`}_signUp(){(0,n.B)(this,"cloud-step",{step:"SIGNUP"})}}_.styles=[c._,a.iv`
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
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],_.prototype,"hass",void 0),_=(0,s.__decorate)([(0,o.Mo)("cloud-step-intro")],_),e()}catch(h){e(h)}}))},77474:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(29173),l=(i(22543),i(30337)),c=(i(20455),i(40830),i(38573),i(33848)),d=i(51909),h=i(81665),p=i(67616),u=t([l]);l=(u.then?(await u)():u)[0];class _ extends a.oi{render(){return a.dy`<div class="content">
        <img
          src=${`/static/images/logo_nabu_casa${this.hass.themes?.darkMode?"_dark":""}.png`}
          alt="Nabu Casa logo"
        />
        <h1>${this.hass.localize("ui.panel.config.cloud.login.sign_in")}</h1>
        ${this._error?a.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
        <ha-textfield
          autofocus
          id="email"
          name="email"
          .label=${this.hass.localize("ui.panel.config.cloud.register.email_address")}
          .disabled=${this._requestInProgress}
          type="email"
          autocomplete="email"
          required
          @keydown=${this._keyDown}
          validationMessage=${this.hass.localize("ui.panel.config.cloud.register.email_error_msg")}
        ></ha-textfield>
        <ha-password-field
          id="password"
          name="password"
          .label=${this.hass.localize("ui.panel.config.cloud.register.password")}
          .disabled=${this._requestInProgress}
          autocomplete="new-password"
          minlength="8"
          required
          @keydown=${this._keyDown}
          validationMessage=${this.hass.localize("ui.panel.config.cloud.register.password_error_msg")}
        ></ha-password-field>
      </div>
      <div class="footer">
        <ha-button
          @click=${this._handleLogin}
          .disabled=${this._requestInProgress}
          >${this.hass.localize("ui.panel.config.cloud.login.sign_in")}</ha-button
        >
      </div>`}_keyDown(t){"Enter"===t.key&&this._handleLogin()}async _handleLogin(){const t=this._emailField,e=this._passwordField,i=t.value,s=e.value;if(!t.reportValidity())return e.reportValidity(),void t.focus();if(!e.reportValidity())return void e.focus();this._requestInProgress=!0;const a=async(e,i)=>{try{await(0,c._Y)({hass:this.hass,email:e,...i?{code:i}:{password:s},check_connection:this._checkConnection})}catch(o){const i=o&&o.body&&o.body.code;if("mfarequired"===i){const t=await(0,h.D9)(this,{title:this.hass.localize("ui.panel.config.cloud.login.totp_code_prompt_title"),inputLabel:this.hass.localize("ui.panel.config.cloud.login.totp_code"),inputType:"text",defaultValue:"",confirmText:this.hass.localize("ui.panel.config.cloud.login.submit")});if(null!==t&&""!==t)return void(await a(e,t))}if("alreadyconnectederror"===i)return void(0,d.F)(this,{details:JSON.parse(o.body.message),logInHereAction:()=>{this._checkConnection=!1,a(e)},closeDialog:()=>{this._requestInProgress=!1}});if("usernotfound"===i&&e!==e.toLowerCase())return void(await a(e.toLowerCase()));if("PasswordChangeRequired"===i)return(0,h.Ys)(this,{title:this.hass.localize("ui.panel.config.cloud.login.alert_password_change_required")}),(0,r.c)("/config/cloud/forgot-password"),void(0,n.B)(this,"closed");switch(this._requestInProgress=!1,i){case"UserNotConfirmed":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_email_confirm_necessary");break;case"mfarequired":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_mfa_code_required");break;case"mfaexpiredornotstarted":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_mfa_expired_or_not_started");break;case"invalidtotpcode":this._error=this.hass.localize("ui.panel.config.cloud.login.alert_totp_code_invalid");break;default:this._error=o&&o.body&&o.body.message?o.body.message:"Unknown error"}t.focus()}};await a(i)}constructor(...t){super(...t),this._requestInProgress=!1,this._checkConnection=!0}}_.styles=[p._,a.iv`
      :host {
        display: block;
      }
      ha-textfield,
      ha-password-field {
        display: block;
      }
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],_.prototype,"_requestInProgress",void 0),(0,s.__decorate)([(0,o.SB)()],_.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],_.prototype,"_checkConnection",void 0),(0,s.__decorate)([(0,o.IO)("#email",!0)],_.prototype,"_emailField",void 0),(0,s.__decorate)([(0,o.IO)("#password",!0)],_.prototype,"_passwordField",void 0),_=(0,s.__decorate)([(0,o.Mo)("cloud-step-signin")],_),e()}catch(_){e(_)}}))},92442:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(22543),i(30337)),l=(i(20455),i(40830),i(38573),i(33848)),c=i(67616),d=t([r]);r=(d.then?(await d)():d)[0];class h extends a.oi{render(){return a.dy`<div class="content">
        <img
          src=${`/static/images/logo_nabu_casa${this.hass.themes?.darkMode?"_dark":""}.png`}
          alt="Nabu Casa logo"
        />
        <h1>
          ${this.hass.localize("ui.panel.config.cloud.register.create_account")}
        </h1>
        ${this._error?a.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:""}
        ${"VERIFY"===this._state?a.dy`<p>
              ${this.hass.localize("ui.panel.config.cloud.register.confirm_email",{email:this._email})}
            </p>`:a.dy`<ha-textfield
                autofocus
                id="email"
                name="email"
                .label=${this.hass.localize("ui.panel.config.cloud.register.email_address")}
                .disabled=${this._requestInProgress}
                type="email"
                autocomplete="email"
                required
                @keydown=${this._keyDown}
                validationMessage=${this.hass.localize("ui.panel.config.cloud.register.email_error_msg")}
              ></ha-textfield>
              <ha-password-field
                id="password"
                name="password"
                .label=${this.hass.localize("ui.panel.config.cloud.register.password")}
                .disabled=${this._requestInProgress}
                autocomplete="new-password"
                minlength="8"
                required
                @keydown=${this._keyDown}
                validationMessage=${this.hass.localize("ui.panel.config.cloud.register.password_error_msg")}
              ></ha-password-field>`}
      </div>
      <div class="footer side-by-side">
        ${"VERIFY"===this._state?a.dy`<ha-button
                @click=${this._handleResendVerifyEmail}
                .disabled=${this._requestInProgress}
                appearance="plain"
                >${this.hass.localize("ui.panel.config.cloud.register.resend_confirm_email")}</ha-button
              ><ha-button
                @click=${this._login}
                .disabled=${this._requestInProgress}
                >${this.hass.localize("ui.panel.config.cloud.register.clicked_confirm")}</ha-button
              >`:a.dy`<ha-button
                @click=${this._signIn}
                .disabled=${this._requestInProgress}
                appearance="plain"
                >${this.hass.localize("ui.panel.config.cloud.login.sign_in")}</ha-button
              >
              <ha-button
                @click=${this._handleRegister}
                .disabled=${this._requestInProgress}
                >${this.hass.localize("ui.common.next")}</ha-button
              >`}
      </div>`}_signIn(){(0,n.B)(this,"cloud-step",{step:"SIGNIN"})}_keyDown(t){"Enter"===t.key&&this._handleRegister()}async _handleRegister(){const t=this._emailField,e=this._passwordField;if(!t.reportValidity())return e.reportValidity(),void t.focus();if(!e.reportValidity())return void e.focus();const i=t.value.toLowerCase(),s=e.value;this._requestInProgress=!0;try{await(0,l.bi)(this.hass,i,s),this._email=i,this._password=s,this._verificationEmailSent()}catch(a){this._password="",this._error=a&&a.body&&a.body.message?a.body.message:"Unknown error"}finally{this._requestInProgress=!1}}async _handleResendVerifyEmail(){if(this._email)try{await(0,l._t)(this.hass,this._email),this._verificationEmailSent()}catch(t){this._error=t&&t.body&&t.body.message?t.body.message:"Unknown error"}}_verificationEmailSent(){this._state="VERIFY",setTimeout((()=>this._login()),5e3)}async _login(){if(this._email&&this._password)try{await(0,l._Y)({hass:this.hass,email:this._email,password:this._password}),(0,n.B)(this,"cloud-step",{step:"DONE"})}catch(t){"usernotconfirmed"===t?.body?.code?this._verificationEmailSent():this._error="Something went wrong. Please try again."}}constructor(...t){super(...t),this._requestInProgress=!1}}h.styles=[c._,a.iv`
      .content {
        width: 100%;
      }
      ha-textfield,
      ha-password-field {
        display: block;
      }
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],h.prototype,"_requestInProgress",void 0),(0,s.__decorate)([(0,o.SB)()],h.prototype,"_email",void 0),(0,s.__decorate)([(0,o.SB)()],h.prototype,"_password",void 0),(0,s.__decorate)([(0,o.SB)()],h.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],h.prototype,"_state",void 0),(0,s.__decorate)([(0,o.IO)("#email",!0)],h.prototype,"_emailField",void 0),(0,s.__decorate)([(0,o.IO)("#password",!0)],h.prototype,"_passwordField",void 0),h=(0,s.__decorate)([(0,o.Mo)("cloud-step-signup")],h),e()}catch(h){e(h)}}))},67616:function(t,e,i){i.d(e,{_:()=>a});var s=i(59048);const a=[i(77204).Qx,s.iv`
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
  `]},52398:function(t,e,i){i.a(t,(async function(t,s){try{i.r(e),i.d(e,{HaVoiceAssistantSetupDialog:()=>E,STEP:()=>k});var a=i(73742),o=i(59048),n=i(7616),r=i(28105),l=i(29740),c=i(76151),d=i(75972),h=(i(62335),i(99298),i(86352)),p=(i(51431),i(89275)),u=i(59753),_=i(64930),g=i(77204),v=(i(37503),i(59924)),f=i(31812),y=i(95907),m=i(24144),b=i(24087),w=i(34041),$=i(73801),C=i(54503),x=t([v,f,y,m,b,w,$,C,d,h]);[v,f,y,m,b,w,$,C,d,h]=x.then?(await x)():x;const S="M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z",z="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",L="M7,10L12,15L17,10H7Z";var k=function(t){return t[t.INIT=0]="INIT",t[t.UPDATE=1]="UPDATE",t[t.CHECK=2]="CHECK",t[t.WAKEWORD=3]="WAKEWORD",t[t.AREA=4]="AREA",t[t.PIPELINE=5]="PIPELINE",t[t.SUCCESS=6]="SUCCESS",t[t.CLOUD=7]="CLOUD",t[t.LOCAL=8]="LOCAL",t[t.CHANGE_WAKEWORD=9]="CHANGE_WAKEWORD",t}({});class E extends o.oi{async showDialog(t){this._params=t,await this._fetchAssistConfiguration(),this._step=1}async closeDialog(){this.renderRoot.querySelector("ha-dialog")?.close()}willUpdate(t){t.has("_step")&&5===this._step&&this._getLanguages()}_dialogClosed(){this._params=void 0,this._assistConfiguration=void 0,this._previousSteps=[],this._nextStep=void 0,this._step=0,this._language=void 0,this._languages=[],this._localOption=void 0,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}render(){if(!this._params)return o.Ld;const t=this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite"),e=t?this.hass.states[t]:void 0;return o.dy`
      <ha-dialog
        open
        @closed=${this._dialogClosed}
        .heading=${"Voice Satellite setup"}
        hideActions
        escapeKeyAction
        scrimClickAction
      >
        <ha-dialog-header slot="heading">
          ${8===this._step?o.Ld:this._previousSteps.length?o.dy`<ha-icon-button
                  slot="navigationIcon"
                  .label=${this.hass.localize("ui.common.back")??"Back"}
                  .path=${S}
                  @click=${this._goToPreviousStep}
                ></ha-icon-button>`:1!==this._step?o.dy`<ha-icon-button
                    slot="navigationIcon"
                    .label=${this.hass.localize("ui.common.close")??"Close"}
                    .path=${z}
                    @click=${this.closeDialog}
                  ></ha-icon-button>`:o.Ld}
          ${3===this._step||4===this._step?o.dy`<ha-button
                @click=${this._goToNextStep}
                class="skip-btn"
                slot="actionItems"
                >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.skip")}</ha-button
              >`:5===this._step&&this._language?o.dy`<ha-md-button-menu
                    slot="actionItems"
                    positioning="fixed"
                  >
                    <ha-assist-chip
                      .label=${(0,d.u)(this._language,this.hass.locale)}
                      slot="trigger"
                    >
                      <ha-svg-icon
                        slot="trailing-icon"
                        .path=${L}
                      ></ha-svg-icon
                    ></ha-assist-chip>
                    ${(0,h.C)(this._languages,!1,!1,this.hass.locale).map((t=>o.dy`<ha-md-menu-item
                          .value=${t.value}
                          @click=${this._handlePickLanguage}
                          @keydown=${this._handlePickLanguage}
                          .selected=${this._language===t.value}
                        >
                          ${t.label}
                        </ha-md-menu-item>`))}
                  </ha-md-button-menu>`:o.Ld}
        </ha-dialog-header>
        <div
          class="content"
          @next-step=${this._goToNextStep}
          @prev-step=${this._goToPreviousStep}
        >
          ${1===this._step?o.dy`<ha-voice-assistant-setup-step-update
                .hass=${this.hass}
                .updateEntityId=${this._findDomainEntityId(this._params.deviceId,this.hass.entities,"update")}
              ></ha-voice-assistant-setup-step-update>`:this._error?o.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:e?.state===_.nZ?o.dy`<ha-alert alert-type="error"
                    >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.not_available")}</ha-alert
                  >`:2===this._step?o.dy`<ha-voice-assistant-setup-step-check
                      .hass=${this.hass}
                      .assistEntityId=${t}
                    ></ha-voice-assistant-setup-step-check>`:3===this._step?o.dy`<ha-voice-assistant-setup-step-wake-word
                        .hass=${this.hass}
                        .assistConfiguration=${this._assistConfiguration}
                        .assistEntityId=${t}
                        .deviceEntities=${this._deviceEntities(this._params.deviceId,this.hass.entities)}
                      ></ha-voice-assistant-setup-step-wake-word>`:9===this._step?o.dy`
                          <ha-voice-assistant-setup-step-change-wake-word
                            .hass=${this.hass}
                            .assistConfiguration=${this._assistConfiguration}
                            .assistEntityId=${t}
                          ></ha-voice-assistant-setup-step-change-wake-word>
                        `:4===this._step?o.dy`
                            <ha-voice-assistant-setup-step-area
                              .hass=${this.hass}
                              .deviceId=${this._params.deviceId}
                            ></ha-voice-assistant-setup-step-area>
                          `:5===this._step?o.dy`<ha-voice-assistant-setup-step-pipeline
                              .hass=${this.hass}
                              .languages=${this._languages}
                              .language=${this._language}
                              .assistConfiguration=${this._assistConfiguration}
                              .assistEntityId=${t}
                              @language-changed=${this._languageChanged}
                            ></ha-voice-assistant-setup-step-pipeline>`:7===this._step?o.dy`<ha-voice-assistant-setup-step-cloud
                                .hass=${this.hass}
                              ></ha-voice-assistant-setup-step-cloud>`:8===this._step?o.dy`<ha-voice-assistant-setup-step-local
                                  .hass=${this.hass}
                                  .language=${this._language}
                                  .localOption=${this._localOption}
                                  .assistConfiguration=${this._assistConfiguration}
                                ></ha-voice-assistant-setup-step-local>`:6===this._step?o.dy`<ha-voice-assistant-setup-step-success
                                    .hass=${this.hass}
                                    .assistConfiguration=${this._assistConfiguration}
                                    .assistEntityId=${t}
                                    .deviceId=${this._params.deviceId}
                                  ></ha-voice-assistant-setup-step-success>`:o.Ld}
        </div>
      </ha-dialog>
    `}async _getLanguages(){if(this._languages.length)return;const t=await(0,u.KH)(this.hass);this._languages=Object.entries(t.languages).filter((([t,e])=>e.cloud>0||e.full_local>0||e.focused_local>0)).map((([t,e])=>t)),this._language=t.preferred_language&&this._languages.includes(t.preferred_language)?t.preferred_language:void 0}async _fetchAssistConfiguration(){try{this._assistConfiguration=await(0,p.ko)(this.hass,this._findDomainEntityId(this._params.deviceId,this.hass.entities,"assist_satellite"))}catch(t){this._error=t.message}}_handlePickLanguage(t){"keydown"===t.type&&"Enter"!==t.key&&" "!==t.key||(this._language=t.target.value)}_languageChanged(t){t.detail.value&&(this._language=t.detail.value)}_goToPreviousStep(){this._previousSteps.length&&(this._step=this._previousSteps.pop())}_goToNextStep(t){t?.detail?.updateConfig&&this._fetchAssistConfiguration(),t?.detail?.nextStep&&(this._nextStep=t.detail.nextStep),t?.detail?.noPrevious||this._previousSteps.push(this._step),t?.detail?.step?(this._step=t.detail.step,8===t.detail.step&&(this._localOption=t.detail.option)):this._nextStep?(this._step=this._nextStep,this._nextStep=void 0):this._step+=1}static get styles(){return[g.yu,o.iv`
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
      `]}constructor(...t){super(...t),this._step=0,this._languages=[],this._previousSteps=[],this._deviceEntities=(0,r.Z)(((t,e)=>Object.values(e).filter((e=>e.device_id===t)))),this._findDomainEntityId=(0,r.Z)(((t,e,i)=>{const s=this._deviceEntities(t,e);return s.find((t=>(0,c.M)(t.entity_id)===i))?.entity_id}))}}(0,a.__decorate)([(0,n.Cb)({attribute:!1})],E.prototype,"hass",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_params",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_step",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_assistConfiguration",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_error",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_language",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_languages",void 0),(0,a.__decorate)([(0,n.SB)()],E.prototype,"_localOption",void 0),E=(0,a.__decorate)([(0,n.Mo)("ha-voice-assistant-setup-dialog")],E),s()}catch(S){s(S)}}))},37503:function(t,e,i){var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(99495),i(51729)),l=i(81665),c=i(67616);class d extends a.oi{render(){const t=this.hass.devices[this.deviceId];return a.dy`<div class="content">
        <img
          src="/static/images/voice-assistant/area.png"
          alt="Casita Home Assistant logo"
        />
        <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.area.title")}
        </h1>
        <p class="secondary">
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.area.secondary")}
        </p>
        <ha-area-picker
          .hass=${this.hass}
          .value=${t.area_id}
        ></ha-area-picker>
      </div>
      <div class="footer">
        <ha-button @click=${this._setArea}
          >${this.hass.localize("ui.common.next")}</ha-button
        >
      </div>`}async _setArea(){const t=this.shadowRoot.querySelector("ha-area-picker").value;t?(await(0,r.t1)(this.hass,this.deviceId,{area_id:t}),this._nextStep()):(0,l.Ys)(this,{text:this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.area.no_selection")})}_nextStep(){(0,n.B)(this,"next-step")}}d.styles=[c._,a.iv`
      ha-area-picker {
        display: block;
        width: 100%;
        margin-bottom: 24px;
        text-align: initial;
      }
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],d.prototype,"deviceId",void 0),d=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-area")],d)},59924:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=(i(89429),i(78067),i(89275)),l=i(67616),c=i(52398),d=t([c]);c=(d.then?(await d)():d)[0];class h extends a.oi{render(){return a.dy`<div class="padding content">
        <img
          src="/static/images/voice-assistant/change-wake-word.png"
          alt="Casita Home Assistant logo"
        />
        <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.change_wake_word.title")}
        </h1>
        <p class="secondary">
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.change_wake_word.secondary")}
        </p>
      </div>
      <ha-md-list>
        ${this.assistConfiguration.available_wake_words.map((t=>a.dy`<ha-md-list-item
              interactive
              type="button"
              @click=${this._wakeWordPicked}
              .value=${t.id}
            >
              ${t.wake_word}
              <ha-icon-next slot="end"></ha-icon-next>
            </ha-md-list-item>`))}
      </ha-md-list>`}async _wakeWordPicked(t){if(!this.assistEntityId)return;const e=t.currentTarget.value;await(0,r.DT)(this.hass,this.assistEntityId,[e]),this._nextStep()}_nextStep(){(0,n.B)(this,"next-step",{step:c.STEP.WAKEWORD,updateConfig:!0})}}h.styles=[l._,a.iv`
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
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],h.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],h.prototype,"assistEntityId",void 0),h=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-change-wake-word")],h),e()}catch(h){e(h)}}))},31812:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(30337),l=i(97862),c=i(89275),d=i(67616),h=i(47584),p=t([r,l]);[r,l]=p.then?(await p)():p;class u extends a.oi{willUpdate(t){super.willUpdate(t),this.hasUpdated?"success"===this._status&&t.has("hass")&&"idle"===this.hass.states[this.assistEntityId]?.state&&this._nextStep():this._testConnection()}render(){return a.dy`<div class="content">
      ${"timeout"===this._status?a.dy`<img
              src="/static/images/voice-assistant/error.png"
              alt="Casita Home Assistant error logo"
            />
            <h1>
              ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.failed_title")}
            </h1>
            <p class="secondary">
              ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.failed_secondary")}
            </p>
            <div class="footer">
              <ha-button
                appearance="plain"
                href=${(0,h.R)(this.hass,"/voice_control/troubleshooting/#i-dont-get-a-voice-response")}
              >
                >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.help")}</ha-button
              >
              <ha-button @click=${this._testConnection}
                >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.retry")}</ha-button
              >
            </div>`:a.dy`<img
              src="/static/images/voice-assistant/hi.png"
              alt="Casita Home Assistant hi logo"
            />
            <h1>
              ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.title")}
            </h1>
            <p class="secondary">
              ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.check.secondary")}
            </p>

            ${this._showLoader?a.dy`<ha-spinner></ha-spinner>`:a.Ld}`}
    </div>`}async _testConnection(){this._status=void 0,this._showLoader=!1;const t=setTimeout((()=>{this._showLoader=!0}),3e3),e=await(0,c.cz)(this.hass,this.assistEntityId);clearTimeout(t),this._showLoader=!1,this._status=e.status}_nextStep(){(0,n.B)(this,"next-step",{noPrevious:!0})}constructor(...t){super(...t),this._showLoader=!1}}u.styles=d._,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],u.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.SB)()],u.prototype,"_status",void 0),(0,s.__decorate)([(0,o.SB)()],u.prototype,"_showLoader",void 0),u=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-check")],u),e()}catch(u){e(u)}}))},95907:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(39894),r=i(77474),l=i(92442),c=i(29740),d=i(52398),h=t([n,r,l,d]);[n,r,l,d]=h.then?(await h)():h;class p extends a.oi{render(){return"SIGNUP"===this._state?a.dy`<cloud-step-signup
        .hass=${this.hass}
        @cloud-step=${this._cloudStep}
      ></cloud-step-signup>`:"SIGNIN"===this._state?a.dy`<cloud-step-signin
        .hass=${this.hass}
        @cloud-step=${this._cloudStep}
      ></cloud-step-signin>`:a.dy`<cloud-step-intro
      .hass=${this.hass}
      @cloud-step=${this._cloudStep}
    ></cloud-step-intro>`}_cloudStep(t){"DONE"!==t.detail.step?this._state=t.detail.step:(0,c.B)(this,"next-step",{step:d.STEP.PIPELINE,noPrevious:!0})}constructor(...t){super(...t),this._state="INTRO"}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],p.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],p.prototype,"_state",void 0),p=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-cloud")],p),e()}catch(p){e(p)}}))},24144:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(42822),r=i(29740),l=i(76151),c=i(97862),d=i(32518),h=i(39286),p=i(28203),u=i(81086),_=i(70937),g=i(75055),v=i(33328),f=i(47584),y=i(67616),m=i(52398),b=i(59753),w=t([c,m]);[c,m]=w.then?(await w)():w;const $="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z";class C extends a.oi{render(){return a.dy`<div class="content">
      ${"INSTALLING"===this._state?a.dy`<img
              src="/static/images/voice-assistant/update.png"
              alt="Casita Home Assistant loading logo"
            />
            <h1>
              ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.title")}
            </h1>
            <p>
              ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.secondary")}
            </p>
            <ha-spinner></ha-spinner>
            <p>
              ${this._detailState||"Installation can take several minutes"}
            </p>`:"ERROR"===this._state?a.dy`<img
                src="/static/images/voice-assistant/error.png"
                alt="Casita Home Assistant error logo"
              />
              <h1>
                ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.failed_title")}
              </h1>
              <p>${this._error}</p>
              <p>
                ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.failed_secondary")}
              </p>
              <ha-button
                appearance="plain"
                size="small"
                @click=${this._prevStep}
                >${this.hass.localize("ui.common.back")}</ha-button
              >
              <ha-button
                href=${(0,f.R)(this.hass,"/voice_control/voice_remote_local_assistant/")}
                target="_blank"
                rel="noreferrer noopener"
                size="small"
                appearance="plain"
              >
                <ha-svg-icon .path=${$} slot="start"></ha-svg-icon>
                ${this.hass.localize("ui.panel.config.common.learn_more")}</ha-button
              >`:"NOT_SUPPORTED"===this._state?a.dy`<img
                  src="/static/images/voice-assistant/error.png"
                  alt="Casita Home Assistant error logo"
                />
                <h1>
                  ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.not_supported_title")}
                </h1>
                <p>
                  ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.not_supported_secondary")}
                </p>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${this._prevStep}
                  >${this.hass.localize("ui.common.back")}</ha-button
                >
                <ha-button
                  href=${(0,f.R)(this.hass,"/voice_control/voice_remote_local_assistant/")}
                  target="_blank"
                  rel="noreferrer noopener"
                  appearance="plain"
                  size="small"
                >
                  <ha-svg-icon .path=${$} slot="start"></ha-svg-icon>
                  ${this.hass.localize("ui.panel.config.common.learn_more")}</ha-button
                >`:a.Ld}
    </div>`}willUpdate(t){super.willUpdate(t),this.hasUpdated||this._checkLocal()}_prevStep(){(0,r.B)(this,"prev-step")}_nextStep(){(0,r.B)(this,"next-step",{step:m.STEP.SUCCESS,noPrevious:!0})}async _checkLocal(){if(await this._findLocalEntities(),this._localTts&&this._localStt)try{if(this._localTts.length&&this._localStt.length)return void(await this._pickOrCreatePipelineExists());if(!(0,n.p)(this.hass,"hassio"))return void(this._state="NOT_SUPPORTED");this._state="INSTALLING";const{addons:t}=await(0,u.yt)(this.hass),e=t.find((t=>t.slug===this._ttsAddonName)),i=t.find((t=>t.slug===this._sttAddonName));this._localTts.length||(e||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.installing_${this._ttsProviderName}`),await(0,u.fU)(this.hass,this._ttsAddonName)),e&&"started"===e.state||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.starting_${this._ttsProviderName}`),await(0,u.kP)(this.hass,this._ttsAddonName)),this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.setup_${this._ttsProviderName}`),await this._setupConfigEntry("tts")),this._localStt.length||(i||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.installing_${this._sttProviderName}`),await(0,u.fU)(this.hass,this._sttAddonName)),i&&"started"===i.state||(this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.starting_${this._sttProviderName}`),await(0,u.kP)(this.hass,this._sttAddonName)),this._detailState=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.state.setup_${this._sttProviderName}`),await this._setupConfigEntry("stt")),this._detailState=this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.state.creating_pipeline"),await this._findEntitiesAndCreatePipeline()}catch(t){this._state="ERROR",this._error=t.message}}get _sttProviderName(){return"focused_local"===this.localOption?"speech-to-phrase":"faster-whisper"}get _sttAddonName(){return"focused_local"===this.localOption?"core_speech-to-phrase":"core_whisper"}get _sttHostName(){return"focused_local"===this.localOption?"core-speech-to-phrase":"core-whisper"}async _findLocalEntities(){const t=Object.values(this.hass.entities).filter((t=>"wyoming"===t.platform));if(!t.length)return this._localStt=[],void(this._localTts=[]);const e=await(0,v.w)(this.hass),i=Object.values(await(0,p.Iq)(this.hass,t.map((t=>t.entity_id))));this._localTts=i.filter((t=>"tts"===(0,l.M)(t.entity_id)&&t.config_entry_id&&e.info[t.config_entry_id]?.tts.some((t=>t.name===this._ttsProviderName)))),this._localStt=i.filter((t=>"stt"===(0,l.M)(t.entity_id)&&t.config_entry_id&&e.info[t.config_entry_id]?.asr.some((t=>t.name===this._sttProviderName))))}async _setupConfigEntry(t){const e=await this._findConfigFlowInProgress(t);if(e){if("create_entry"===(await(0,h.XO)(this.hass,e.flow_id,{})).type)return}return this._createConfigEntry(t)}async _findConfigFlowInProgress(t){return(await(0,h.D7)(this.hass.connection)).find((e=>"wyoming"===e.handler&&"hassio"===e.context.source&&(e.context.configuration_url&&e.context.configuration_url.includes("tts"===t?this._ttsAddonName:this._sttAddonName)||e.context.title_placeholders.name&&e.context.title_placeholders.name.toLowerCase().includes("tts"===t?this._ttsProviderName:this._sttProviderName))))}async _createConfigEntry(t){const e=await(0,h.Ky)(this.hass,"wyoming"),i=await(0,h.XO)(this.hass,e.flow_id,{host:"tts"===t?this._ttsHostName:this._sttHostName,port:"tts"===t?this._ttsPort:this._sttPort});if("create_entry"!==i.type)throw new Error(`${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.errors.failed_create_entry",{addon:"tts"===t?this._ttsProviderName:this._sttProviderName})}${"errors"in i?`: ${i.errors.base}`:""}`)}async _pickOrCreatePipelineExists(){if(!this._localStt?.length||!this._localTts?.length)return;const t=await(0,d.SC)(this.hass);t.preferred_pipeline&&t.pipelines.sort((e=>e.id===t.preferred_pipeline?-1:0));const e=this._localTts.map((t=>t.entity_id)),i=this._localStt.map((t=>t.entity_id));let s=t.pipelines.find((t=>"conversation.home_assistant"===t.conversation_engine&&t.tts_engine&&e.includes(t.tts_engine)&&t.stt_engine&&i.includes(t.stt_engine)&&t.language.split("-")[0]===this.language.split("-")[0]));s||(s=await this._createPipeline(this._localTts[0].entity_id,this._localStt[0].entity_id)),await this.hass.callService("select","select_option",{option:s.name},{entity_id:this.assistConfiguration?.pipeline_entity_id}),this._nextStep()}async _createPipeline(t,e){const i=await(0,d.SC)(this.hass),s=(await(0,b.rM)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).agents.find((t=>"conversation.home_assistant"===t.id));if(!s?.supported_languages.length)throw new Error("Conversation agent does not support requested language.");const a=(await(0,g.Wg)(this.hass,this.language,this.hass.config.country||void 0)).providers.find((e=>e.engine_id===t));if(!a?.supported_languages?.length)throw new Error("TTS engine does not support requested language.");const o=await(0,g.MV)(this.hass,t,a.supported_languages[0]);if(!o.voices?.length)throw new Error("No voice available for requested language.");const n=(await(0,_.m)(this.hass,this.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===e));if(!n?.supported_languages?.length)throw new Error("STT engine does not support requested language.");let r=this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.${this.localOption}_pipeline`),l=1;for(;i.pipelines.find((t=>t.name===r));)r=`${this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.local.${this.localOption}_pipeline`)} ${l}`,l++;return(0,d.jZ)(this.hass,{name:r,language:this.language.split("-")[0],conversation_engine:"conversation.home_assistant",conversation_language:s.supported_languages[0],stt_engine:e,stt_language:n.supported_languages[0],tts_engine:t,tts_language:a.supported_languages[0],tts_voice:o.voices[0].voice_id,wake_word_entity:null,wake_word_id:null})}async _findEntitiesAndCreatePipeline(t=0){if(await this._findLocalEntities(),!this._localTts?.length||!this._localStt?.length){if(t>3)throw new Error(this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.local.errors.could_not_find_entities"));return await new Promise((t=>{setTimeout(t,2e3)})),this._findEntitiesAndCreatePipeline(t+1)}const e=await this._createPipeline(this._localTts[0].entity_id,this._localStt[0].entity_id);await this.hass.callService("select","select_option",{option:e.name},{entity_id:this.assistConfiguration?.pipeline_entity_id}),this._nextStep()}constructor(...t){super(...t),this._state="INTRO",this._ttsProviderName="piper",this._ttsAddonName="core_piper",this._ttsHostName="core-piper",this._ttsPort=10200,this._sttPort=10300}}C.styles=[y._,a.iv`
      ha-spinner {
        margin-top: 24px;
        margin-bottom: 24px;
      }
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"localOption",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"language",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_state",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_detailState",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_error",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_localTts",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_localStt",void 0),C=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-local")],C),e()}catch($){e($)}}))},24087:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(28105),r=i(42822),l=i(29740),c=i(76151),d=i(75972),h=(i(14241),i(32518)),p=i(33848),u=i(59753),_=i(70937),g=i(75055),v=i(67616),f=i(52398),y=i(47584),m=t([d,f]);[d,f]=m.then?(await m)():m;const b=["cloud","focused_local","full_local"],w={cloud:0,focused_local:0,full_local:0};class $ extends a.oi{willUpdate(t){if(super.willUpdate(t),this.hasUpdated||this._fetchData(),(t.has("language")||t.has("_languageScores"))&&this.language&&this._languageScores){const t=this.language;this._value&&0===this._languageScores[t]?.[this._value]&&(this._value=void 0),this._value||(this._value=this._getOptions(this._languageScores[t]||w,this.hass.localize).supportedOptions[0]?.value)}}render(){if(!this._cloudChecked||!this._languageScores)return a.Ld;if(!this.language){const t=(0,d.u)(this.hass.config.language,this.hass.locale);return a.dy`<div class="content">
        <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.header")}
        </h1>
        ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.secondary",{language:t})}
        <ha-language-picker
          .hass=${this.hass}
          .label=${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.language_picker")}
          .languages=${this.languages}
          @value-changed=${this._languageChanged}
        ></ha-language-picker>

        <a
          href=${(0,y.R)(this.hass,"/voice_control/contribute-voice/")}
          >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported_language.contribute",{language:t})}</a
        >
      </div>`}const t=this._languageScores[this.language]||w,e=this._getOptions(t,this.hass.localize),i=this._value?"full_local"===this._value?"low":"high":"",s=this._value?t[this._value]>2?"high":t[this._value]>1?"ready":t[this._value]>0?"low":"":"";return a.dy`<div class="content">
        <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.title")}
        </h1>
        <div class="bar-header">
          <span
            >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.performance.header")}</span
          ><span
            >${i?this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.performance.${i}`):""}</span
          >
        </div>
        <div class="perf-bar ${i}">
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
        </div>
        <div class="bar-header">
          <span
            >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.commands.header")}</span
          ><span
            >${s?this.hass.localize(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.commands.${s}`):""}</span
          >
        </div>
        <div class="perf-bar ${s}">
          <div class="segment"></div>
          <div class="segment"></div>
          <div class="segment"></div>
        </div>
        <ha-select-box
          max_columns="1"
          .options=${e.supportedOptions}
          .value=${this._value}
          @value-changed=${this._valueChanged}
        ></ha-select-box>
        ${e.unsupportedOptions.length?a.dy`<h3>
                ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.pipeline.unsupported")}
              </h3>
              <ha-select-box
                max_columns="1"
                .options=${e.unsupportedOptions}
                disabled
              ></ha-select-box>`:a.Ld}
      </div>
      <div class="footer">
        <ha-button @click=${this._createPipeline} .disabled=${!this._value}
          >${this.hass.localize("ui.common.next")}</ha-button
        >
      </div>`}async _fetchData(){await this._hasCloud()&&await this._createCloudPipeline(!1)||(this._cloudChecked=!0,this._languageScores=(await(0,u.KH)(this.hass)).languages)}async _hasCloud(){if(!(0,r.p)(this.hass,"cloud"))return!1;const t=await(0,p.LI)(this.hass);return!(!t.logged_in||!t.active_subscription)}async _createCloudPipeline(t){let e,i;for(const a of Object.values(this.hass.entities))if("cloud"===a.platform){const t=(0,c.M)(a.entity_id);if("tts"===t)e=a.entity_id;else{if("stt"!==t)continue;i=a.entity_id}if(e&&i)break}try{const s=await(0,h.SC)(this.hass);s.preferred_pipeline&&s.pipelines.sort((t=>t.id===s.preferred_pipeline?-1:0));let a=s.pipelines.find((s=>"conversation.home_assistant"===s.conversation_engine&&s.tts_engine===e&&s.stt_engine===i&&(!t||s.language.split("-")[0]===this.language.split("-")[0])));if(!a){const t=(await(0,u.rM)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).agents.find((t=>"conversation.home_assistant"===t.id));if(!t?.supported_languages.length)return!1;const o=(await(0,g.Wg)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===e));if(!o?.supported_languages?.length)return!1;const n=await(0,g.MV)(this.hass,e,o.supported_languages[0]),r=(await(0,_.m)(this.hass,this.language||this.hass.config.language,this.hass.config.country||void 0)).providers.find((t=>t.engine_id===i));if(!r?.supported_languages?.length)return!1;let l="Home Assistant Cloud",c=1;for(;s.pipelines.find((t=>t.name===l));)l=`Home Assistant Cloud ${c}`,c++;a=await(0,h.jZ)(this.hass,{name:l,language:(this.language||this.hass.config.language).split("-")[0],conversation_engine:"conversation.home_assistant",conversation_language:t.supported_languages[0],stt_engine:i,stt_language:r.supported_languages[0],tts_engine:e,tts_language:o.supported_languages[0],tts_voice:n.voices[0].voice_id,wake_word_entity:null,wake_word_id:null})}return await this.hass.callService("select","select_option",{option:a.name},{entity_id:this.assistConfiguration?.pipeline_entity_id}),(0,l.B)(this,"next-step",{step:f.STEP.SUCCESS,noPrevious:!0}),!0}catch(s){return!1}}_valueChanged(t){this._value=t.detail.value}async _setupCloud(){await this._hasCloud()?this._createCloudPipeline(!0):(0,l.B)(this,"next-step",{step:f.STEP.CLOUD})}_createPipeline(){"cloud"===this._value?this._setupCloud():"focused_local"===this._value?this._setupLocalFocused():this._setupLocalFull()}_setupLocalFocused(){(0,l.B)(this,"next-step",{step:f.STEP.LOCAL,option:this._value})}_setupLocalFull(){(0,l.B)(this,"next-step",{step:f.STEP.LOCAL,option:this._value})}_languageChanged(t){t.detail.value&&(0,l.B)(this,"language-changed",{value:t.detail.value})}constructor(...t){super(...t),this.languages=[],this._cloudChecked=!1,this._getOptions=(0,n.Z)(((t,e)=>{const i=[],s=[];return b.forEach((a=>{t[a]>0?i.push({label:e(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.options.${a}.label`),description:e(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.options.${a}.description`),value:a}):s.push({label:e(`ui.panel.config.voice_assistants.satellite_wizard.pipeline.options.${a}.label`),value:a})})),{supportedOptions:i,unsupportedOptions:s}}))}}$.styles=[v._,a.iv`
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
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],$.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],$.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],$.prototype,"deviceId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],$.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],$.prototype,"language",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],$.prototype,"languages",void 0),(0,s.__decorate)([(0,o.SB)()],$.prototype,"_cloudChecked",void 0),(0,s.__decorate)([(0,o.SB)()],$.prototype,"_value",void 0),(0,s.__decorate)([(0,o.SB)()],$.prototype,"_languageScores",void 0),$=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-pipeline")],$),e()}catch(b){e(b)}}))},34041:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(41806),l=i(85163),c=(i(93795),i(29490),i(80443),i(32518)),d=i(89275),h=i(33848),p=i(51729),u=i(12593),_=i(26665),g=i(74183),v=i(48785),f=i(67616),y=i(52398),m=t([g,y]);[g,y]=m.then?(await m)():m;const b="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z",w="M12,2A3,3 0 0,1 15,5V11A3,3 0 0,1 12,14A3,3 0 0,1 9,11V5A3,3 0 0,1 12,2M19,11C19,14.53 16.39,17.44 13,17.93V21H11V17.93C7.61,17.44 5,14.53 5,11H7A5,5 0 0,0 12,16A5,5 0 0,0 17,11H19Z",$="M8,5.14V19.14L19,12.14L8,5.14Z";class C extends a.oi{willUpdate(t){if(super.willUpdate(t),t.has("assistConfiguration"))this._setTtsSettings();else if(t.has("hass")&&this.assistConfiguration){const e=t.get("hass");if(e){const t=e.states[this.assistConfiguration.pipeline_entity_id],i=this.hass.states[this.assistConfiguration.pipeline_entity_id];t.state!==i.state&&this._setTtsSettings()}}}render(){const t=this.assistConfiguration?this.hass.states[this.assistConfiguration.pipeline_entity_id]:void 0,e=this.hass.devices[this.deviceId];return a.dy`<div class="content">
        <img
          src="/static/images/voice-assistant/heart.png"
          alt="Casita Home Assistant logo"
        />
        <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.title")}
        </h1>
        <p class="secondary">
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.secondary")}
        </p>
        ${this._error?a.dy`<ha-alert alert-type="error">${this._error}</ha-alert>`:a.Ld}
        <div class="rows">
          <div class="row">
            <ha-textfield
              .label=${this.hass.localize("ui.panel.config.integrations.config_flow.device_name")}
              .placeholder=${(0,l.wZ)(e,this.hass)}
              .value=${this._deviceName??(0,l.jL)(e)}
              @change=${this._deviceNameChanged}
            ></ha-textfield>
          </div>
          ${this.assistConfiguration&&this.assistConfiguration.available_wake_words.length>1?a.dy`<div class="row">
                <ha-select
                  .label=${"Wake word"}
                  @closed=${r.U}
                  fixedMenuPosition
                  naturalMenuWidth
                  .value=${this.assistConfiguration.active_wake_words[0]}
                  @selected=${this._wakeWordPicked}
                >
                  ${this.assistConfiguration.available_wake_words.map((t=>a.dy`<ha-list-item .value=${t.id}>
                        ${t.wake_word}
                      </ha-list-item>`))}
                </ha-select>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${this._testWakeWord}
                >
                  <ha-svg-icon
                    slot="start"
                    .path=${w}
                  ></ha-svg-icon>
                  ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.test_wakeword")}
                </ha-button>
              </div>`:a.Ld}
          ${t?a.dy`<div class="row">
                <ha-select
                  .label=${"Assistant"}
                  @closed=${r.U}
                  .value=${t?.state}
                  fixedMenuPosition
                  naturalMenuWidth
                  @selected=${this._pipelinePicked}
                >
                  ${t?.attributes.options.map((e=>a.dy`<ha-list-item .value=${e}>
                        ${this.hass.formatEntityState(t,e)}
                      </ha-list-item>`))}
                </ha-select>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${this._openPipeline}
                >
                  <ha-svg-icon slot="start" .path=${b}></ha-svg-icon>
                  ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.edit_pipeline")}
                </ha-button>
              </div>`:a.Ld}
          ${this._ttsSettings?a.dy`<div class="row">
                <ha-tts-voice-picker
                  .hass=${this.hass}
                  .engineId=${this._ttsSettings.engine}
                  .language=${this._ttsSettings.language}
                  .value=${this._ttsSettings.voice}
                  @value-changed=${this._voicePicked}
                  @closed=${r.U}
                ></ha-tts-voice-picker>
                <ha-button
                  appearance="plain"
                  size="small"
                  @click=${this._testTts}
                >
                  <ha-svg-icon slot="start" .path=${$}></ha-svg-icon>
                  ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.try_tts")}
                </ha-button>
              </div>`:a.Ld}
        </div>
      </div>
      <div class="footer">
        <ha-button @click=${this._done}
          >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.done")}</ha-button
        >
      </div>`}async _getPipeline(){if(!this.assistConfiguration?.pipeline_entity_id)return[void 0,void 0];const t=this.hass.states[this.assistConfiguration?.pipeline_entity_id].state,e=await(0,c.SC)(this.hass);let i;return i="preferred"===t?e.pipelines.find((t=>t.id===e.preferred_pipeline)):e.pipelines.find((e=>e.name===t)),[i,e.preferred_pipeline]}_deviceNameChanged(t){this._deviceName=t.target.value}async _wakeWordPicked(t){const e=t.target.value;await(0,d.DT)(this.hass,this.assistEntityId,[e])}_pipelinePicked(t){const e=this.hass.states[this.assistConfiguration.pipeline_entity_id],i=t.target.value;i!==e.state&&e.attributes.options.includes(i)&&(0,u.n)(this.hass,e.entity_id,i)}async _setTtsSettings(){const[t]=await this._getPipeline();this._ttsSettings=t?{engine:t.tts_engine,voice:t.tts_voice,language:t.tts_language}:void 0}async _voicePicked(t){const[e]=await this._getPipeline();e&&await(0,c.af)(this.hass,e.id,{...e,tts_voice:t.detail.value})}async _testTts(){const[t]=await this._getPipeline();if(t){if(t.language!==this.hass.locale.language)try{const e=await(0,v.i0)(null,t.language,!1);return void this._announce(e.data["ui.dialogs.tts-try.message_example"])}catch(e){}this._announce(this.hass.localize("ui.dialogs.tts-try.message_example"))}}async _announce(t){this.assistEntityId&&await(0,d.SY)(this.hass,this.assistEntityId,{message:t,preannounce:!1})}_testWakeWord(){(0,n.B)(this,"next-step",{step:y.STEP.WAKEWORD,nextStep:y.STEP.SUCCESS,updateConfig:!0})}async _openPipeline(){const[t]=await this._getPipeline();if(!t)return;const e=await(0,h.LI)(this.hass);(0,_.t)(this,{cloudActiveSubscription:e.logged_in&&e.active_subscription,pipeline:t,updatePipeline:async e=>{await(0,c.af)(this.hass,t.id,e)},hideWakeWord:!0})}async _done(){if(this._deviceName)try{(0,p.t1)(this.hass,this.deviceId,{name_by_user:this._deviceName})}catch(t){return void(this._error=this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.success.failed_rename",{error:t.message||t}))}(0,n.B)(this,"closed")}}C.styles=[f._,a.iv`
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
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"deviceId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],C.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_ttsSettings",void 0),(0,s.__decorate)([(0,o.SB)()],C.prototype,"_error",void 0),C=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-success")],C),e()}catch(b){e(b)}}))},73801:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(29740),r=i(21349),l=i(97862),c=i(64930),d=i(53258),h=i(67616),p=t([r,l,d]);[r,l,d]=p.then?(await p)():p;class u extends a.oi{willUpdate(t){if(super.willUpdate(t),this.updateEntityId){if(t.has("hass")&&this.updateEntityId){const e=t.get("hass");if(e){const t=e.states[this.updateEntityId],i=this.hass.states[this.updateEntityId];if(t?.state===c.nZ&&i?.state!==c.nZ||t?.state!==c.ON&&i?.state===c.ON)return void this._tryUpdate(!1)}}t.has("updateEntityId")&&this._tryUpdate(!0)}else this._nextStep()}render(){if(!this.updateEntityId||!(this.updateEntityId in this.hass.states))return a.Ld;const t=this.hass.states[this.updateEntityId],e=t&&(0,d.SO)(t);return a.dy`<div class="content">
      <img
        src="/static/images/voice-assistant/update.png"
        alt="Casita Home Assistant loading logo"
      />
      <h1>
        ${t&&("unavailable"===t.state||(0,d.Sk)(t))?this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.update.title"):this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.update.checking")}
      </h1>
      <p class="secondary">
        ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.update.secondary")}
      </p>
      ${e?a.dy`
            <ha-progress-ring
              .value=${t.attributes.update_percentage}
            ></ha-progress-ring>
          `:a.dy`<ha-spinner></ha-spinner>`}
      <p>
        ${t?.state===c.nZ?"Restarting voice assistant":e?`Installing ${t.attributes.update_percentage}%`:""}
      </p>
    </div>`}async _tryUpdate(t){if(clearTimeout(this._refreshTimeout),!this.updateEntityId)return;const e=this.hass.states[this.updateEntityId];e&&this.hass.states[e.entity_id].state===c.ON&&(0,d.hF)(e)?(this._updated=!0,await this.hass.callService("update","install",{},{entity_id:e.entity_id})):t?(await this.hass.callService("homeassistant","update_entity",{},{entity_id:this.updateEntityId}),this._refreshTimeout=window.setTimeout((()=>{this._nextStep()}),1e4)):this._nextStep()}_nextStep(){(0,n.B)(this,"next-step",{noPrevious:!0,updateConfig:this._updated})}constructor(...t){super(...t),this._updated=!1}}u.styles=[h._,a.iv`
      ha-progress-ring,
      ha-spinner {
        margin-top: 24px;
        margin-bottom: 24px;
      }
    `],(0,s.__decorate)([(0,o.Cb)({attribute:!1})],u.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],u.prototype,"updateEntityId",void 0),u=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-update")],u),e()}catch(u){e(u)}}))},54503:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(28105),r=i(29740),l=i(30337),c=i(97862),d=(i(76528),i(89275)),h=i(67616),p=i(52398),u=i(76151),_=t([l,c,p]);[l,c,p]=_.then?(await _)():_;class g extends a.oi{disconnectedCallback(){super.disconnectedCallback(),this._stopListeningWakeWord()}willUpdate(t){super.willUpdate(t),t.has("assistConfiguration")&&this.assistConfiguration&&!this.assistConfiguration.available_wake_words.length&&this._nextStep(),t.has("assistEntityId")&&(this._detected=!1,this._muteSwitchEntity=this.deviceEntities?.find((t=>"switch"===(0,u.M)(t.entity_id)&&t.entity_id.includes("mute")))?.entity_id,this._muteSwitchEntity||this._startTimeOut(),this._listenWakeWord())}_startTimeOut(){this._timeout=window.setTimeout((()=>{this._timeout=void 0,this._timedout=!0}),15e3)}render(){if(!this.assistEntityId)return a.Ld;return"idle"!==this.hass.states[this.assistEntityId].state?a.dy`<ha-spinner></ha-spinner>`:a.dy`<div class="content">
        ${this._detected?a.dy`<img
                src="/static/images/voice-assistant/ok-nabu.png"
                alt="Casita Home Assistant logo"
              />
              <h1>
                ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.title_2",{wakeword:this._activeWakeWord(this.assistConfiguration)})}
              </h1>
              <p class="secondary">
                ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.secondary_2")}
              </p>`:a.dy`
          <img src="/static/images/voice-assistant/sleep.png" alt="Casita Home Assistant logo"/>
          <h1>
          ${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.title",{wakeword:this._activeWakeWord(this.assistConfiguration)})}  
          </h1>
          <p class="secondary">${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.secondary")}</p>
        </div>`}
        ${this._timedout?a.dy`<ha-alert alert-type="warning"
              >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.time_out")}</ha-alert
            >`:this._muteSwitchEntity&&"on"===this.hass.states[this._muteSwitchEntity].state?a.dy`<ha-alert
                alert-type="warning"
                .title=${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.muted")}
                >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.muted_description")}</ha-alert
              >`:a.Ld}
      </div>
      ${this.assistConfiguration&&this.assistConfiguration.available_wake_words.length>1?a.dy`<div class="footer centered">
            <ha-button
              appearance="plain"
              size="small"
              @click=${this._changeWakeWord}
              >${this.hass.localize("ui.panel.config.voice_assistants.satellite_wizard.wake_word.change_wake_word")}</ha-button
            >
          </div>`:a.Ld}`}async _listenWakeWord(){const t=this.assistEntityId;t&&(await this._stopListeningWakeWord(),this._sub=(0,d.aJ)(this.hass,t,(()=>{this._timedout=!1,clearTimeout(this._timeout),this._stopListeningWakeWord(),this._detected?this._nextStep():(this._detected=!0,this._listenWakeWord())})))}async _stopListeningWakeWord(){try{(await this._sub)?.()}catch(t){}this._sub=void 0}_nextStep(){(0,r.B)(this,"next-step")}_changeWakeWord(){(0,r.B)(this,"next-step",{step:p.STEP.CHANGE_WAKEWORD})}constructor(...t){super(...t),this._detected=!1,this._timedout=!1,this._activeWakeWord=(0,n.Z)((t=>{if(!t)return"";const e=t.active_wake_words[0];return t.available_wake_words.find((t=>t.id===e))?.wake_word}))}}g.styles=h._,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"assistConfiguration",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"assistEntityId",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"deviceEntities",void 0),(0,s.__decorate)([(0,o.SB)()],g.prototype,"_muteSwitchEntity",void 0),(0,s.__decorate)([(0,o.SB)()],g.prototype,"_detected",void 0),(0,s.__decorate)([(0,o.SB)()],g.prototype,"_timedout",void 0),g=(0,s.__decorate)([(0,o.Mo)("ha-voice-assistant-setup-step-wake-word")],g),e()}catch(g){e(g)}}))},51909:function(t,e,i){i.d(e,{F:()=>a});var s=i(29740);const a=(t,e)=>new Promise((a=>{const o=e.closeDialog,n=e.logInHereAction;(0,s.B)(t,"show-dialog",{dialogTag:"dialog-cloud-already-connected",dialogImport:()=>i.e("3898").then(i.bind(i,53530)),dialogParams:{...e,closeDialog:()=>{o?.(),a(!1)},logInHereAction:()=>{n?.(),a(!0)}}})}))},26665:function(t,e,i){i.d(e,{t:()=>o});var s=i(29740);const a=()=>Promise.all([i.e("2335"),i.e("1705")]).then(i.bind(i,44062)),o=(t,e)=>{(0,s.B)(t,"show-dialog",{dialogTag:"dialog-voice-assistant-pipeline-detail",dialogImport:a,dialogParams:e})}},2180:function(t,e,i){i.d(e,{K:()=>d});var s=i(59048),a=i(83522),o=i(29740),n=i(74002),r=i(78001);class l extends HTMLElement{connectedCallback(){Object.assign(this.style,{position:"fixed",width:r.T?"100px":"50px",height:r.T?"100px":"50px",transform:"translate(-50%, -50%) scale(0)",pointerEvents:"none",zIndex:"999",background:"var(--primary-color)",display:null,opacity:"0.2",borderRadius:"50%",transition:"transform 180ms ease-in-out"}),["touchcancel","mouseout","mouseup","touchmove","mousewheel","wheel","scroll"].forEach((t=>{document.addEventListener(t,(()=>{this.cancelled=!0,this.timer&&(this._stopAnimation(),clearTimeout(this.timer),this.timer=void 0)}),{passive:!0})}))}bind(t,e={}){t.actionHandler&&(0,n.v)(e,t.actionHandler.options)||(t.actionHandler?(t.removeEventListener("touchstart",t.actionHandler.start),t.removeEventListener("touchend",t.actionHandler.end),t.removeEventListener("touchcancel",t.actionHandler.end),t.removeEventListener("mousedown",t.actionHandler.start),t.removeEventListener("click",t.actionHandler.end),t.removeEventListener("keydown",t.actionHandler.handleKeyDown)):t.addEventListener("contextmenu",(t=>{const e=t||window.event;return e.preventDefault&&e.preventDefault(),e.stopPropagation&&e.stopPropagation(),e.cancelBubble=!0,e.returnValue=!1,!1})),t.actionHandler={options:e},e.disabled||(t.actionHandler.start=t=>{let i,s;this.cancelled=!1,t.touches?(i=t.touches[0].clientX,s=t.touches[0].clientY):(i=t.clientX,s=t.clientY),e.hasHold&&(this.held=!1,this.timer=window.setTimeout((()=>{this._startAnimation(i,s),this.held=!0}),this.holdTime))},t.actionHandler.end=t=>{if("touchcancel"===t.type||"touchend"===t.type&&this.cancelled)return;const i=t.target;t.cancelable&&t.preventDefault(),e.hasHold&&(clearTimeout(this.timer),this._stopAnimation(),this.timer=void 0),e.hasHold&&this.held?(0,o.B)(i,"action",{action:"hold"}):e.hasDoubleClick?"click"===t.type&&t.detail<2||!this.dblClickTimeout?this.dblClickTimeout=window.setTimeout((()=>{this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"tap"})}),250):(clearTimeout(this.dblClickTimeout),this.dblClickTimeout=void 0,(0,o.B)(i,"action",{action:"double_tap"})):(0,o.B)(i,"action",{action:"tap"})},t.actionHandler.handleKeyDown=t=>{["Enter"," "].includes(t.key)&&t.currentTarget.actionHandler.end(t)},t.addEventListener("touchstart",t.actionHandler.start,{passive:!0}),t.addEventListener("touchend",t.actionHandler.end),t.addEventListener("touchcancel",t.actionHandler.end),t.addEventListener("mousedown",t.actionHandler.start,{passive:!0}),t.addEventListener("click",t.actionHandler.end),t.addEventListener("keydown",t.actionHandler.handleKeyDown)))}_startAnimation(t,e){Object.assign(this.style,{left:`${t}px`,top:`${e}px`,transform:"translate(-50%, -50%) scale(1)"})}_stopAnimation(){Object.assign(this.style,{left:null,top:null,transform:"translate(-50%, -50%) scale(0)"})}constructor(...t){super(...t),this.holdTime=500,this.held=!1,this.cancelled=!1}}customElements.define("action-handler",l);const c=(t,e)=>{const i=(()=>{const t=document.body;if(t.querySelector("action-handler"))return t.querySelector("action-handler");const e=document.createElement("action-handler");return t.appendChild(e),e})();i&&i.bind(t,e)},d=(0,a.XM)(class extends a.Xe{update(t,[e]){return c(t.element,e),s.Jb}render(t){}})},51496:function(t,e,i){i.d(e,{G:()=>u});var s=i(29740),a=i(29173),o=i(19408),n=i(47469),r=i(81665);const l=()=>i.e("7395").then(i.bind(i,47609));var c=i(15606),d=i(80092),h=i(76151);const p=(t,e)=>((t,e,i=!0)=>{const s=(0,h.M)(e),a="group"===s?"homeassistant":s;let o;switch(s){case"lock":o=i?"unlock":"lock";break;case"cover":o=i?"open_cover":"close_cover";break;case"button":case"input_button":o="press";break;case"scene":o="turn_on";break;case"valve":o=i?"open_valve":"close_valve";break;default:o=i?"turn_on":"turn_off"}return t.callService(a,o,{entity_id:e})})(t,e,d.tj.includes(t.states[e].state)),u=async(t,e,i,d)=>{let h;if("double_tap"===d&&i.double_tap_action?h=i.double_tap_action:"hold"===d&&i.hold_action?h=i.hold_action:"tap"===d&&i.tap_action&&(h=i.tap_action),h||(h={action:"more-info"}),h.confirmation&&(!h.confirmation.exemptions||!h.confirmation.exemptions.some((t=>t.user===e.user?.id)))){let i;if((0,o.j)("warning"),"call-service"===h.action||"perform-action"===h.action){const[t,s]=(h.perform_action||h.service).split(".",2),a=e.services;if(t in a&&s in a[t]){await e.loadBackendTranslation("title");const o=await e.loadBackendTranslation("services");i=`${(0,n.Lh)(o,t)}: ${o(`component.${t}.services.${i}.name`)||a[t][s].name||s}`}}if(!(await(0,r.g7)(t,{text:h.confirmation.text||e.localize("ui.panel.lovelace.cards.actions.action_confirmation",{action:i||e.localize(`ui.panel.lovelace.editor.action-editor.actions.${h.action}`)||h.action})})))return}switch(h.action){case"more-info":{const a=h.entity||i.entity||i.camera_image||i.image_entity;a?(0,s.B)(t,"hass-more-info",{entityId:a}):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_entity_more_info")}),(0,o.j)("failure"));break}case"navigate":h.navigation_path?(0,a.c)(h.navigation_path,{replace:h.navigation_replace}):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_navigation_path")}),(0,o.j)("failure"));break;case"url":h.url_path?window.open(h.url_path):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_url")}),(0,o.j)("failure"));break;case"toggle":i.entity?(p(e,i.entity),(0,o.j)("light")):((0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_entity_toggle")}),(0,o.j)("failure"));break;case"perform-action":case"call-service":{if(!h.perform_action&&!h.service)return(0,c.C)(t,{message:e.localize("ui.panel.lovelace.cards.actions.no_action")}),void(0,o.j)("failure");const[i,s]=(h.perform_action||h.service).split(".",2);e.callService(i,s,h.data??h.service_data,h.target),(0,o.j)("light");break}case"assist":((t,e,i)=>{e.auth.external?.config.hasAssist?e.auth.external.fireMessage({type:"assist/show",payload:{pipeline_id:i.pipeline_id,start_listening:i.start_listening??!0}}):(0,s.B)(t,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:l,dialogParams:{pipeline_id:i.pipeline_id,start_listening:i.start_listening??!1}})})(t,e,{start_listening:h.start_listening??!1,pipeline_id:h.pipeline_id??"last_used"});break;case"fire-dom-event":(0,s.B)(t,"ll-custom",h)}}},28378:function(t,e,i){function s(t){return void 0!==t&&"none"!==t.action}function a(t){return!t.tap_action||s(t.tap_action)||s(t.hold_action)||s(t.double_tap_action)}i.d(e,{_:()=>s,q:()=>a})},44336:function(t,e,i){function s(t,e){if(e.has("_config"))return!0;if(!e.has("hass"))return!1;const i=e.get("hass");return!i||(i.connected!==t.hass.connected||i.themes!==t.hass.themes||i.locale!==t.hass.locale||i.localize!==t.hass.localize||i.formatEntityState!==t.hass.formatEntityState||i.formatEntityAttributeName!==t.hass.formatEntityAttributeName||i.formatEntityAttributeValue!==t.hass.formatEntityAttributeValue||i.config.state!==t.hass.config.state)}function a(t,e,i){return t.states[i]!==e.states[i]}function o(t,e,i){const s=t.entities[i],a=e.entities[i];return s?.display_precision!==a?.display_precision}function n(t,e){if(s(t,e))return!0;if(!e.has("hass"))return!1;const i=e.get("hass"),n=t.hass;return a(i,n,t._config.entity)||o(i,n,t._config.entity)}i.d(e,{G2:()=>n})},20376:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(31733),r=i(25191),l=i(80092),c=i(4757),d=i(76151),h=i(31298),p=i(37351),u=i(25661),_=i(2180),g=i(51496),v=i(28378),f=i(94169),y=i(41806),m=t([p,u]);[p,u]=m.then?(await m)():m;class b extends a.oi{render(){if(!this.hass||!this.config)return a.Ld;const t=this.config.entity?this.hass.states[this.config.entity]:void 0;if(!t)return a.dy`
        <hui-warning .hass=${this.hass}>
          ${(0,f.i)(this.hass,this.config.entity)}
        </hui-warning>
      `;const e=(0,d.M)(this.config.entity),i=(0,v.q)(this.config),s=this.secondaryText||this.config.secondary_info,o=this.config.name??(0,h.C)(t);return a.dy`
      <div
        class="row ${(0,n.$)({pointer:i})}"
        @action=${this._handleAction}
        .actionHandler=${(0,_.K)({hasHold:(0,v._)(this.config.hold_action),hasDoubleClick:(0,v._)(this.config.double_tap_action)})}
        tabindex=${(0,r.o)(!this.config.tap_action||(0,v._)(this.config.tap_action)?"0":void 0)}
      >
        <state-badge
          .hass=${this.hass}
          .stateObj=${t}
          .overrideIcon=${this.config.icon}
          .overrideImage=${this.config.image}
          .stateColor=${this.config.state_color}
        ></state-badge>
        ${this.hideName?a.Ld:a.dy`<div
              class="info ${(0,n.$)({"text-content":!s})}"
              .title=${o}
            >
              ${this.config.name||(0,h.C)(t)}
              ${s?a.dy`
                    <div class="secondary">
                      ${this.secondaryText||("entity-id"===this.config.secondary_info?t.entity_id:"last-changed"===this.config.secondary_info?a.dy`
                              <ha-relative-time
                                .hass=${this.hass}
                                .datetime=${t.last_changed}
                                capitalize
                              ></ha-relative-time>
                            `:"last-updated"===this.config.secondary_info?a.dy`
                                <ha-relative-time
                                  .hass=${this.hass}
                                  .datetime=${t.last_updated}
                                  capitalize
                                ></ha-relative-time>
                              `:"last-triggered"===this.config.secondary_info?t.attributes.last_triggered?a.dy`
                                    <ha-relative-time
                                      .hass=${this.hass}
                                      .datetime=${t.attributes.last_triggered}
                                      capitalize
                                    ></ha-relative-time>
                                  `:this.hass.localize("ui.panel.lovelace.cards.entities.never_triggered"):"position"===this.config.secondary_info&&void 0!==t.attributes.current_position?`${this.hass.localize("ui.card.cover.position")}: ${t.attributes.current_position}`:"tilt-position"===this.config.secondary_info&&void 0!==t.attributes.current_tilt_position?`${this.hass.localize("ui.card.cover.tilt_position")}: ${t.attributes.current_tilt_position}`:"brightness"===this.config.secondary_info&&t.attributes.brightness?a.dy`${Math.round(t.attributes.brightness/255*100)}
                                      %`:"state"===this.config.secondary_info?a.dy`${this.hass.formatEntityState(t)}`:a.Ld)}
                    </div>
                  `:a.Ld}
            </div>`}
        ${this.catchInteraction??!l.AF.includes(e)?a.dy`
              <div class="text-content value">
                <div class="state"><slot></slot></div>
              </div>
            `:a.dy`<slot
              @touchcancel=${y.U}
              @touchend=${y.U}
              @keydown=${y.U}
              @click=${y.U}
              @action=${y.U}
            ></slot>`}
      </div>
    `}updated(t){super.updated(t),(0,c.X)(this,"no-secondary",!this.secondaryText&&!this.config?.secondary_info)}_handleAction(t){(0,g.G)(this,this.hass,this.config,t.detail.action)}constructor(...t){super(...t),this.hideName=!1}}b.styles=a.iv`
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
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],b.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],b.prototype,"config",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"secondary-text"})],b.prototype,"secondaryText",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"hide-name",type:Boolean})],b.prototype,"hideName",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"catch-interaction",type:Boolean})],b.prototype,"catchInteraction",void 0),b=(0,s.__decorate)([(0,o.Mo)("hui-generic-entity-row")],b),e()}catch(b){e(b)}}))},94169:function(t,e,i){i.d(e,{i:()=>l});var s=i(73742);var a=i(59048),o=i(7616);i(22543),i(13965),i(40830);const n={warning:"M12,2L1,21H23M12,6L19.53,19H4.47M11,10V14H13V10M11,16V18H13V16",error:"M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z"};class r extends a.oi{getCardSize(){return 1}getGridOptions(){return{columns:6,rows:this.preview?"auto":1,min_rows:1,min_columns:6,fixed_rows:this.preview}}setConfig(t){this._config=t,this.severity=t.severity||"error"}render(){const t=this._config?.error||this.hass?.localize("ui.errors.config.configuration_error"),e=void 0===this.hass||this.hass?.user?.is_admin||this.preview,i=this.preview;return a.dy`
      <ha-card class="${this.severity} ${e?"":"no-title"}">
        <div class="header">
          <div class="icon">
            <slot name="icon">
              <ha-svg-icon .path=${n[this.severity]}></ha-svg-icon>
            </slot>
          </div>
          ${e?a.dy`<div class="title"><slot>${t}</slot></div>`:a.Ld}
        </div>
        ${i&&this._config?.message?a.dy`<div class="message">${this._config.message}</div>`:a.Ld}
      </ha-card>
    `}constructor(...t){super(...t),this.preview=!1,this.severity="error"}}r.styles=a.iv`
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
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],r.prototype,"hass",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:!1})],r.prototype,"preview",void 0),(0,s.__decorate)([(0,o.Cb)({attribute:"severity"})],r.prototype,"severity",void 0),(0,s.__decorate)([(0,o.SB)()],r.prototype,"_config",void 0),r=(0,s.__decorate)([(0,o.Mo)("hui-error-card")],r);const l=(t,e)=>"NOT_RUNNING"!==t.config.state?t.localize("ui.card.common.entity_not_found"):t.localize("ui.panel.lovelace.warning.starting");class c extends a.oi{render(){return a.dy`<hui-error-card .hass=${this.hass} severity="warning"
      ><slot></slot
    ></hui-error-card>`}}(0,s.__decorate)([(0,o.Cb)({attribute:!1})],c.prototype,"hass",void 0),c=(0,s.__decorate)([(0,o.Mo)("hui-warning")],c)},74183:function(t,e,i){i.a(t,(async function(t,e){try{var s=i(73742),a=i(59048),o=i(7616),n=i(41806),r=i(31298),l=(i(93795),i(29490),i(64930)),c=i(19408),d=i(12593),h=i(44336),p=i(20376),u=i(94169),_=t([p]);p=(_.then?(await _)():_)[0];class g extends a.oi{setConfig(t){if(!t||!t.entity)throw new Error("Entity must be specified");this._config=t}shouldUpdate(t){return(0,h.G2)(this,t)}render(){if(!this.hass||!this._config)return a.Ld;const t=this.hass.states[this._config.entity];return t?a.dy`
      <hui-generic-entity-row
        .hass=${this.hass}
        .config=${this._config}
        hide-name
      >
        <ha-select
          .label=${this._config.name||(0,r.C)(t)}
          .value=${t.state}
          .options=${t.attributes.options}
          .disabled=${t.state===l.nZ}
          naturalMenuWidth
          @action=${this._handleAction}
          @click=${n.U}
          @closed=${n.U}
        >
          ${t.attributes.options?t.attributes.options.map((e=>a.dy`
                  <ha-list-item .value=${e}>
                    ${this.hass.formatEntityState(t,e)}
                  </ha-list-item>
                `)):""}
        </ha-select>
      </hui-generic-entity-row>
    `:a.dy`
        <hui-warning .hass=${this.hass}>
          ${(0,u.i)(this.hass,this._config.entity)}
        </hui-warning>
      `}_handleAction(t){const e=this.hass.states[this._config.entity],i=t.target.value;i!==e.state&&e.attributes.options.includes(i)&&((0,c.j)("light"),(0,d.n)(this.hass,e.entity_id,i))}}g.styles=a.iv`
    hui-generic-entity-row {
      display: flex;
      align-items: center;
    }
    ha-select {
      width: 100%;
      --ha-select-min-width: 0;
    }
  `,(0,s.__decorate)([(0,o.Cb)({attribute:!1})],g.prototype,"hass",void 0),(0,s.__decorate)([(0,o.SB)()],g.prototype,"_config",void 0),g=(0,s.__decorate)([(0,o.Mo)("hui-select-entity-row")],g),e()}catch(g){e(g)}}))},78001:function(t,e,i){i.d(e,{T:()=>s});const s="ontouchstart"in window||navigator.maxTouchPoints>0||navigator.msMaxTouchPoints>0},15606:function(t,e,i){i.d(e,{C:()=>a});var s=i(29740);const a=(t,e)=>(0,s.B)(t,"hass-notification",e)},27885:function(t,e,i){i.d(e,{g:()=>r});var s=i(73742),a=(i(21700),i(59048)),o=i(7616),n=i(63383);class r extends n.A{get primaryId(){return this.href?"link":"button"}get rippleDisabled(){return!this.href&&(this.disabled||this.softDisabled)}getContainerClasses(){return{...super.getContainerClasses(),disabled:!this.href&&(this.disabled||this.softDisabled),elevated:this.elevated,link:!!this.href}}renderPrimaryAction(t){const{ariaLabel:e}=this;return this.href?a.dy`
        <a
          class="primary action"
          id="link"
          aria-label=${e||a.Ld}
          href=${this.href}
          download=${this.download||a.Ld}
          target=${this.target||a.Ld}
          >${t}</a
        >
      `:a.dy`
      <button
        class="primary action"
        id="button"
        aria-label=${e||a.Ld}
        aria-disabled=${this.softDisabled||a.Ld}
        ?disabled=${this.disabled&&!this.alwaysFocusable}
        type="button"
        >${t}</button
      >
    `}renderOutline(){return this.elevated?a.dy`<md-elevation part="elevation"></md-elevation>`:super.renderOutline()}constructor(){super(...arguments),this.elevated=!1,this.href="",this.download="",this.target=""}}(0,s.__decorate)([(0,o.Cb)({type:Boolean})],r.prototype,"elevated",void 0),(0,s.__decorate)([(0,o.Cb)()],r.prototype,"href",void 0),(0,s.__decorate)([(0,o.Cb)()],r.prototype,"download",void 0),(0,s.__decorate)([(0,o.Cb)()],r.prototype,"target",void 0)},67522:function(t,e,i){i.d(e,{W:()=>s});const s=i(59048).iv`:host{--_container-height: var(--md-assist-chip-container-height, 32px);--_disabled-label-text-color: var(--md-assist-chip-disabled-label-text-color, var(--md-sys-color-on-surface, #1d1b20));--_disabled-label-text-opacity: var(--md-assist-chip-disabled-label-text-opacity, 0.38);--_elevated-container-color: var(--md-assist-chip-elevated-container-color, var(--md-sys-color-surface-container-low, #f7f2fa));--_elevated-container-elevation: var(--md-assist-chip-elevated-container-elevation, 1);--_elevated-container-shadow-color: var(--md-assist-chip-elevated-container-shadow-color, var(--md-sys-color-shadow, #000));--_elevated-disabled-container-color: var(--md-assist-chip-elevated-disabled-container-color, var(--md-sys-color-on-surface, #1d1b20));--_elevated-disabled-container-elevation: var(--md-assist-chip-elevated-disabled-container-elevation, 0);--_elevated-disabled-container-opacity: var(--md-assist-chip-elevated-disabled-container-opacity, 0.12);--_elevated-focus-container-elevation: var(--md-assist-chip-elevated-focus-container-elevation, 1);--_elevated-hover-container-elevation: var(--md-assist-chip-elevated-hover-container-elevation, 2);--_elevated-pressed-container-elevation: var(--md-assist-chip-elevated-pressed-container-elevation, 1);--_focus-label-text-color: var(--md-assist-chip-focus-label-text-color, var(--md-sys-color-on-surface, #1d1b20));--_hover-label-text-color: var(--md-assist-chip-hover-label-text-color, var(--md-sys-color-on-surface, #1d1b20));--_hover-state-layer-color: var(--md-assist-chip-hover-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--_hover-state-layer-opacity: var(--md-assist-chip-hover-state-layer-opacity, 0.08);--_label-text-color: var(--md-assist-chip-label-text-color, var(--md-sys-color-on-surface, #1d1b20));--_label-text-font: var(--md-assist-chip-label-text-font, var(--md-sys-typescale-label-large-font, var(--md-ref-typeface-plain, Roboto)));--_label-text-line-height: var(--md-assist-chip-label-text-line-height, var(--md-sys-typescale-label-large-line-height, 1.25rem));--_label-text-size: var(--md-assist-chip-label-text-size, var(--md-sys-typescale-label-large-size, 0.875rem));--_label-text-weight: var(--md-assist-chip-label-text-weight, var(--md-sys-typescale-label-large-weight, var(--md-ref-typeface-weight-medium, 500)));--_pressed-label-text-color: var(--md-assist-chip-pressed-label-text-color, var(--md-sys-color-on-surface, #1d1b20));--_pressed-state-layer-color: var(--md-assist-chip-pressed-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--_pressed-state-layer-opacity: var(--md-assist-chip-pressed-state-layer-opacity, 0.12);--_disabled-outline-color: var(--md-assist-chip-disabled-outline-color, var(--md-sys-color-on-surface, #1d1b20));--_disabled-outline-opacity: var(--md-assist-chip-disabled-outline-opacity, 0.12);--_focus-outline-color: var(--md-assist-chip-focus-outline-color, var(--md-sys-color-on-surface, #1d1b20));--_outline-color: var(--md-assist-chip-outline-color, var(--md-sys-color-outline, #79747e));--_outline-width: var(--md-assist-chip-outline-width, 1px);--_disabled-leading-icon-color: var(--md-assist-chip-disabled-leading-icon-color, var(--md-sys-color-on-surface, #1d1b20));--_disabled-leading-icon-opacity: var(--md-assist-chip-disabled-leading-icon-opacity, 0.38);--_focus-leading-icon-color: var(--md-assist-chip-focus-leading-icon-color, var(--md-sys-color-primary, #6750a4));--_hover-leading-icon-color: var(--md-assist-chip-hover-leading-icon-color, var(--md-sys-color-primary, #6750a4));--_leading-icon-color: var(--md-assist-chip-leading-icon-color, var(--md-sys-color-primary, #6750a4));--_icon-size: var(--md-assist-chip-icon-size, 18px);--_pressed-leading-icon-color: var(--md-assist-chip-pressed-leading-icon-color, var(--md-sys-color-primary, #6750a4));--_container-shape-start-start: var(--md-assist-chip-container-shape-start-start, var(--md-assist-chip-container-shape, var(--md-sys-shape-corner-small, 8px)));--_container-shape-start-end: var(--md-assist-chip-container-shape-start-end, var(--md-assist-chip-container-shape, var(--md-sys-shape-corner-small, 8px)));--_container-shape-end-end: var(--md-assist-chip-container-shape-end-end, var(--md-assist-chip-container-shape, var(--md-sys-shape-corner-small, 8px)));--_container-shape-end-start: var(--md-assist-chip-container-shape-end-start, var(--md-assist-chip-container-shape, var(--md-sys-shape-corner-small, 8px)));--_leading-space: var(--md-assist-chip-leading-space, 16px);--_trailing-space: var(--md-assist-chip-trailing-space, 16px);--_icon-label-space: var(--md-assist-chip-icon-label-space, 8px);--_with-leading-icon-leading-space: var(--md-assist-chip-with-leading-icon-leading-space, 8px)}@media(forced-colors: active){.link .outline{border-color:ActiveText}}
`},7046:function(t,e,i){i.d(e,{W:()=>s});const s=i(59048).iv`.elevated{--md-elevation-level: var(--_elevated-container-elevation);--md-elevation-shadow-color: var(--_elevated-container-shadow-color)}.elevated::before{background:var(--_elevated-container-color)}.elevated:hover{--md-elevation-level: var(--_elevated-hover-container-elevation)}.elevated:focus-within{--md-elevation-level: var(--_elevated-focus-container-elevation)}.elevated:active{--md-elevation-level: var(--_elevated-pressed-container-elevation)}.elevated.disabled{--md-elevation-level: var(--_elevated-disabled-container-elevation)}.elevated.disabled::before{background:var(--_elevated-disabled-container-color);opacity:var(--_elevated-disabled-container-opacity)}@media(forced-colors: active){.elevated md-elevation{border:1px solid CanvasText}.elevated.disabled md-elevation{border-color:GrayText}}
`},78722:function(t,e,i){i.d(e,{D:()=>n});var s=i(87191),a=i(70323),o=i(1097);function n(t,e){const i=()=>(0,a.L)(e?.in,NaN),n=e?.additionalDigits??2,g=function(t){const e={},i=t.split(r.dateTimeDelimiter);let s;if(i.length>2)return e;/:/.test(i[0])?s=i[0]:(e.date=i[0],s=i[1],r.timeZoneDelimiter.test(e.date)&&(e.date=t.split(r.timeZoneDelimiter)[0],s=t.substr(e.date.length,t.length)));if(s){const t=r.timezone.exec(s);t?(e.time=s.replace(t[1],""),e.timezone=t[1]):e.time=s}return e}(t);let v;if(g.date){const t=function(t,e){const i=new RegExp("^(?:(\\d{4}|[+-]\\d{"+(4+e)+"})|(\\d{2}|[+-]\\d{"+(2+e)+"})$)"),s=t.match(i);if(!s)return{year:NaN,restDateString:""};const a=s[1]?parseInt(s[1]):null,o=s[2]?parseInt(s[2]):null;return{year:null===o?a:100*o,restDateString:t.slice((s[1]||s[2]).length)}}(g.date,n);v=function(t,e){if(null===e)return new Date(NaN);const i=t.match(l);if(!i)return new Date(NaN);const s=!!i[4],a=h(i[1]),o=h(i[2])-1,n=h(i[3]),r=h(i[4]),c=h(i[5])-1;if(s)return function(t,e,i){return e>=1&&e<=53&&i>=0&&i<=6}(0,r,c)?function(t,e,i){const s=new Date(0);s.setUTCFullYear(t,0,4);const a=s.getUTCDay()||7,o=7*(e-1)+i+1-a;return s.setUTCDate(s.getUTCDate()+o),s}(e,r,c):new Date(NaN);{const t=new Date(0);return function(t,e,i){return e>=0&&e<=11&&i>=1&&i<=(u[e]||(_(t)?29:28))}(e,o,n)&&function(t,e){return e>=1&&e<=(_(t)?366:365)}(e,a)?(t.setUTCFullYear(e,o,Math.max(a,n)),t):new Date(NaN)}}(t.restDateString,t.year)}if(!v||isNaN(+v))return i();const f=+v;let y,m=0;if(g.time&&(m=function(t){const e=t.match(c);if(!e)return NaN;const i=p(e[1]),a=p(e[2]),o=p(e[3]);if(!function(t,e,i){if(24===t)return 0===e&&0===i;return i>=0&&i<60&&e>=0&&e<60&&t>=0&&t<25}(i,a,o))return NaN;return i*s.vh+a*s.yJ+1e3*o}(g.time),isNaN(m)))return i();if(!g.timezone){const t=new Date(f+m),i=(0,o.Q)(0,e?.in);return i.setFullYear(t.getUTCFullYear(),t.getUTCMonth(),t.getUTCDate()),i.setHours(t.getUTCHours(),t.getUTCMinutes(),t.getUTCSeconds(),t.getUTCMilliseconds()),i}return y=function(t){if("Z"===t)return 0;const e=t.match(d);if(!e)return 0;const i="+"===e[1]?-1:1,a=parseInt(e[2]),o=e[3]&&parseInt(e[3])||0;if(!function(t,e){return e>=0&&e<=59}(0,o))return NaN;return i*(a*s.vh+o*s.yJ)}(g.timezone),isNaN(y)?i():(0,o.Q)(f+m+y,e?.in)}const r={dateTimeDelimiter:/[T ]/,timeZoneDelimiter:/[Z ]/i,timezone:/([Z+-].*)$/},l=/^-?(?:(\d{3})|(\d{2})(?:-?(\d{2}))?|W(\d{2})(?:-?(\d{1}))?|)$/,c=/^(\d{2}(?:[.,]\d*)?)(?::?(\d{2}(?:[.,]\d*)?))?(?::?(\d{2}(?:[.,]\d*)?))?$/,d=/^([+-])(\d{2})(?::?(\d{2}))?$/;function h(t){return t?parseInt(t):1}function p(t){return t&&parseFloat(t.replace(",","."))||0}const u=[31,null,31,30,31,30,31,31,30,31,30,31];function _(t){return t%400==0||t%4==0&&t%100!=0}},12790:function(t,e,i){i.d(e,{C:()=>p});var s=i(35340),a=i(5277),o=i(93847);class n{disconnect(){this.G=void 0}reconnect(t){this.G=t}deref(){return this.G}constructor(t){this.G=t}}class r{get(){return this.Y}pause(){this.Y??=new Promise((t=>this.Z=t))}resume(){this.Z?.(),this.Y=this.Z=void 0}constructor(){this.Y=void 0,this.Z=void 0}}var l=i(83522);const c=t=>!(0,a.pt)(t)&&"function"==typeof t.then,d=1073741823;class h extends o.sR{render(...t){return t.find((t=>!c(t)))??s.Jb}update(t,e){const i=this._$Cbt;let a=i.length;this._$Cbt=e;const o=this._$CK,n=this._$CX;this.isConnected||this.disconnected();for(let s=0;s<e.length&&!(s>this._$Cwt);s++){const t=e[s];if(!c(t))return this._$Cwt=s,t;s<a&&t===i[s]||(this._$Cwt=d,a=0,Promise.resolve(t).then((async e=>{for(;n.get();)await n.get();const i=o.deref();if(void 0!==i){const s=i._$Cbt.indexOf(t);s>-1&&s<i._$Cwt&&(i._$Cwt=s,i.setValue(e))}})))}return s.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}constructor(){super(...arguments),this._$Cwt=d,this._$Cbt=[],this._$CK=new n(this),this._$CX=new r}}const p=(0,l.XM)(h)}};
//# sourceMappingURL=9548.c3b48172a6b527f1.js.map