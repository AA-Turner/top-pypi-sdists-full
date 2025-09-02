"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[3762],{25551:(e,t,i)=>{i.d(t,{u:()=>o});var a=i(14516);const o=(e,t)=>{try{var i,a;return null!==(i=null===(a=s(t))||void 0===a?void 0:a.of(e))&&void 0!==i?i:e}catch(o){return e}},s=(0,a.Z)((e=>Intl&&"DisplayNames"in Intl?new Intl.DisplayNames(e.language,{type:"language",fallback:"code"}):void 0))},7006:(e,t,i)=>{var a=i(73958),o=i(565),s=i(47838),n=(i(34131),i(68262)),r=i(9644),d=i(36924);(0,a.Z)([(0,d.Mo)("ha-circular-progress")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,d.Cb)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,o.Z)((0,s.Z)(i.prototype),"updated",this).call(this,e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"get",static:!0,key:"styles",value:function(){return[...(0,o.Z)((0,s.Z)(i),"styles",this),r.iv`
        :host {
          --md-sys-color-primary: var(--primary-color);
          --md-circular-progress-size: 48px;
        }
      `]}}]}}),n.B)},78680:(e,t,i)=>{var a=i(73958),o=i(9644),s=i(36924);(0,a.Z)([(0,s.Mo)("ha-dialog-header")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"method",key:"render",value:function(){return o.dy`
      <header class="header">
        <div class="header-bar">
          <section class="header-navigation-icon">
            <slot name="navigationIcon"></slot>
          </section>
          <section class="header-title">
            <slot name="title"></slot>
          </section>
          <section class="header-action-items">
            <slot name="actionItems"></slot>
          </section>
        </div>
        <slot></slot>
      </header>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[o.iv`
        :host {
          display: block;
        }
        :host([show-border]) {
          border-bottom: 1px solid
            var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
        }
        .header-bar {
          display: flex;
          flex-direction: row;
          align-items: flex-start;
          padding: 4px;
          box-sizing: border-box;
        }
        .header-title {
          flex: 1;
          font-size: 22px;
          line-height: 28px;
          font-weight: 400;
          padding: 10px 4px;
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          .header-bar {
            padding: 12px;
          }
        }
        .header-navigation-icon {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
        .header-action-items {
          flex: none;
          min-width: 8px;
          height: 100%;
          display: flex;
          flex-direction: row;
        }
      `]}}]}}),o.oi)},9828:(e,t,i)=>{i.d(t,{i:()=>u});var a=i(73958),o=i(565),s=i(47838),n=i(41085),r=i(91632),d=i(9644),l=i(36924),c=i(15815);i(54371);const h=["button","ha-list-item"],u=(e,t)=>{var i;return d.dy`
  <div class="header_title">${t}</div>
  <ha-icon-button
    .label=${null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close"}
    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
    dialogAction="close"
    class="header_button"
  ></ha-icon-button>
`};(0,a.Z)([(0,l.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return d.dy`<slot name="heading"> ${(0,o.Z)((0,s.Z)(i.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,o.Z)((0,s.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,h].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,s.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value(){return[r.W,d.iv`
      :host([scrolled]) ::slotted(ha-dialog-header) {
        border-bottom: 1px solid
          var(--mdc-dialog-scroll-divider-color, rgba(0, 0, 0, 0.12));
      }
      .mdc-dialog {
        --mdc-dialog-scroll-divider-color: var(
          --dialog-scroll-divider-color,
          var(--divider-color)
        );
        z-index: var(--dialog-z-index, 8);
        -webkit-backdrop-filter: var(--dialog-backdrop-filter, none);
        backdrop-filter: var(--dialog-backdrop-filter, none);
        --mdc-dialog-box-shadow: var(--dialog-box-shadow, none);
        --mdc-typography-headline6-font-weight: 400;
        --mdc-typography-headline6-font-size: 1.574rem;
      }
      .mdc-dialog__actions {
        justify-content: var(--justify-action-buttons, flex-end);
        padding-bottom: max(env(safe-area-inset-bottom), 24px);
      }
      .mdc-dialog__actions span:nth-child(1) {
        flex: var(--secondary-action-button-flex, unset);
      }
      .mdc-dialog__actions span:nth-child(2) {
        flex: var(--primary-action-button-flex, unset);
      }
      .mdc-dialog__container {
        align-items: var(--vertical-align-dialog, center);
      }
      .mdc-dialog__title {
        padding: 24px 24px 0 24px;
        text-overflow: ellipsis;
        overflow: hidden;
      }
      .mdc-dialog__actions {
        padding: 12px 24px 12px 24px;
      }
      .mdc-dialog__title::before {
        display: block;
        height: 0px;
      }
      .mdc-dialog .mdc-dialog__content {
        position: var(--dialog-content-position, relative);
        padding: var(--dialog-content-padding, 24px);
      }
      :host([hideactions]) .mdc-dialog .mdc-dialog__content {
        padding-bottom: max(
          var(--dialog-content-padding, 24px),
          env(safe-area-inset-bottom)
        );
      }
      .mdc-dialog .mdc-dialog__surface {
        position: var(--dialog-surface-position, relative);
        top: var(--dialog-surface-top);
        margin-top: var(--dialog-surface-margin-top);
        min-height: var(--mdc-dialog-min-height, auto);
        border-radius: var(--ha-dialog-border-radius, 28px);
      }
      :host([flexContent]) .mdc-dialog .mdc-dialog__content {
        display: flex;
        flex-direction: column;
      }
      .header_title {
        margin-right: 32px;
        margin-inline-end: 32px;
        margin-inline-start: initial;
        direction: var(--direction);
      }
      .header_button {
        position: absolute;
        right: 16px;
        top: 14px;
        text-decoration: none;
        color: inherit;
        inset-inline-start: initial;
        inset-inline-end: 16px;
        direction: var(--direction);
      }
      .dialog-actions {
        inset-inline-start: initial !important;
        inset-inline-end: 0px !important;
        direction: var(--direction);
      }
    `]}}]}}),n.M)},99040:(e,t,i)=>{var a=i(73958),o=i(565),s=i(47838),n=i(48095),r=i(72477),d=i(36924),l=i(9644),c=i(47509);(0,a.Z)([(0,d.Mo)("ha-fab")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,s.Z)(i.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}},{kind:"field",static:!0,key:"styles",value(){return[r.W,l.iv`
      :host .mdc-fab--extended .mdc-fab__icon {
        margin-inline-start: -8px;
        margin-inline-end: 12px;
        direction: var(--direction);
      }
    `,"rtl"===c.E.document.dir?l.iv`
          :host .mdc-fab--extended .mdc-fab__icon {
            direction: rtl;
          }
        `:l.iv``]}}]}}),n._)},7648:(e,t,i)=>{i.a(e,(async(e,t)=>{try{var a=i(73958),o=i(565),s=i(47838),n=i(9644),r=i(36924),d=i(14516),l=i(18394),c=i(86089),h=i(25551),u=i(28858),m=i(23216),p=i(92893),v=(i(90532),i(71133),e([m]));m=(v.then?(await v)():v)[0];(0,a.Z)([(0,r.Mo)("ha-language-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"languages",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"nativeName",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"noSort",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_defaultLanguages",value(){return[]}},{kind:"field",decorators:[(0,r.IO)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,s.Z)(i.prototype),"firstUpdated",this).call(this,e),this._computeDefaultLanguageOptions()}},{kind:"method",key:"updated",value:function(e){(0,o.Z)((0,s.Z)(i.prototype),"updated",this).call(this,e);const t=e.has("hass")&&this.hass&&e.get("hass")&&e.get("hass").locale.language!==this.hass.locale.language;if(e.has("languages")||e.has("value")||t){var a,n;if(this._select.layoutOptions(),this._select.value!==this.value&&(0,l.B)(this,"value-changed",{value:this._select.value}),!this.value)return;const e=this._getLanguagesOptions(null!==(a=this.languages)&&void 0!==a?a:this._defaultLanguages,this.nativeName,null===(n=this.hass)||void 0===n?void 0:n.locale).findIndex((e=>e.value===this.value));-1===e&&(this.value=void 0),t&&this._select.select(e)}}},{kind:"field",key:"_getLanguagesOptions",value(){return(0,d.Z)(((e,t,i)=>{let a=[];if(t){const t=p.o.translations;a=e.map((e=>{var i;let a=null===(i=t[e])||void 0===i?void 0:i.nativeName;if(!a)try{a=new Intl.DisplayNames(e,{type:"language",fallback:"code"}).of(e)}catch(o){a=e}return{value:e,label:a}}))}else i&&(a=e.map((e=>({value:e,label:(0,h.u)(e,i)}))));return!this.noSort&&i&&a.sort(((e,t)=>(0,u.f)(e.label,t.label,i.language))),a}))}},{kind:"method",key:"_computeDefaultLanguageOptions",value:function(){this._defaultLanguages=Object.keys(p.o.translations)}},{kind:"method",key:"render",value:function(){var e,t,i,a,o,s,r;const d=this._getLanguagesOptions(null!==(e=this.languages)&&void 0!==e?e:this._defaultLanguages,this.nativeName,null===(t=this.hass)||void 0===t?void 0:t.locale),l=null!==(i=this.value)&&void 0!==i?i:this.required?null===(a=d[0])||void 0===a?void 0:a.value:this.value;return n.dy`
      <ha-select
        .label=${null!==(o=this.label)&&void 0!==o?o:(null===(s=this.hass)||void 0===s?void 0:s.localize("ui.components.language-picker.language"))||"Language"}
        .value=${l||""}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${c.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${0===d.length?n.dy`<ha-list-item value=""
              >${(null===(r=this.hass)||void 0===r?void 0:r.localize("ui.components.language-picker.no_languages"))||"No languages"}</ha-list-item
            >`:d.map((e=>n.dy`
                <ha-list-item .value=${e.value}
                  >${e.label}</ha-list-item
                >
              `))}
      </ha-select>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;""!==t.value&&t.value!==this.value&&(this.value=t.value,(0,l.B)(this,"value-changed",{value:this.value}))}}]}}),n.oi);t()}catch(g){t(g)}}))},60298:(e,t,i)=>{var a=i(73958),o=i(565),s=i(47838),n=i(9644),r=i(36924),d=i(18394),l=i(86089),c=i(72218),h=i(56112);i(90532),i(71133);const u="__NONE_OPTION__";(0,a.Z)([(0,r.Mo)("ha-tts-voice-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)()],key:"value",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"engineId",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"language",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"required",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_voices",value:void 0},{kind:"field",decorators:[(0,r.IO)("ha-select")],key:"_select",value:void 0},{kind:"method",key:"render",value:function(){var e,t;if(!this._voices)return n.Ld;const i=null!==(e=this.value)&&void 0!==e?e:this.required?null===(t=this._voices[0])||void 0===t?void 0:t.voice_id:u;return n.dy`
      <ha-select
        .label=${this.label||this.hass.localize("ui.components.tts-voice-picker.voice")}
        .value=${i}
        .required=${this.required}
        .disabled=${this.disabled}
        @selected=${this._changed}
        @closed=${l.U}
        fixedMenuPosition
        naturalMenuWidth
      >
        ${this.required?n.Ld:n.dy`<ha-list-item .value=${u}>
              ${this.hass.localize("ui.components.tts-voice-picker.none")}
            </ha-list-item>`}
        ${this._voices.map((e=>n.dy`<ha-list-item .value=${e.voice_id}>
              ${e.name}
            </ha-list-item>`))}
      </ha-select>
    `}},{kind:"method",key:"willUpdate",value:function(e){(0,o.Z)((0,s.Z)(i.prototype),"willUpdate",this).call(this,e),this.hasUpdated?(e.has("language")||e.has("engineId"))&&this._debouncedUpdateVoices():this._updateVoices()}},{kind:"field",key:"_debouncedUpdateVoices",value(){return(0,c.D)((()=>this._updateVoices()),500)}},{kind:"method",key:"_updateVoices",value:async function(){this.engineId&&this.language?(this._voices=(await(0,h.MV)(this.hass,this.engineId,this.language)).voices,this.value&&(this._voices&&this._voices.find((e=>e.voice_id===this.value))||(this.value=void 0,(0,d.B)(this,"value-changed",{value:this.value})))):this._voices=void 0}},{kind:"method",key:"updated",value:function(e){var t,a,n;((0,o.Z)((0,s.Z)(i.prototype),"updated",this).call(this,e),e.has("_voices")&&(null===(t=this._select)||void 0===t?void 0:t.value)!==this.value)&&(null===(a=this._select)||void 0===a||a.layoutOptions(),(0,d.B)(this,"value-changed",{value:null===(n=this._select)||void 0===n?void 0:n.value}))}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      ha-select {
        width: 100%;
      }
    `}},{kind:"method",key:"_changed",value:function(e){const t=e.target;!this.hass||""===t.value||t.value===this.value||void 0===this.value&&t.value===u||(this.value=t.value===u?void 0:t.value,(0,d.B)(this,"value-changed",{value:this.value}))}}]}}),n.oi)},93762:(e,t,i)=>{i.a(e,(async(e,a)=>{try{i.r(t);var o=i(73958),s=i(9644),n=i(36924),r=i(18394),d=i(29950),l=(i(9828),i(78680),i(82029),i(15758)),c=i(86089),h=e([l]);l=(h.then?(await h)():h)[0];const u="M3,5A2,2 0 0,1 5,3H19A2,2 0 0,1 21,5V19A2,2 0 0,1 19,21H5C3.89,21 3,20.1 3,19V5M5,5V19H19V5H5M11,7H13A2,2 0 0,1 15,9V17H13V13H11V17H9V9A2,2 0 0,1 11,7M11,9V11H13V9H11Z",m="M20,11V13H8L13.5,18.5L12.08,19.92L4.16,12L12.08,4.08L13.5,5.5L8,11H20Z",p="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",v="M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z",g="M10,4V8H14V4H10M16,4V8H20V4H16M16,10V14H20V10H16M16,16V20H20V16H16M14,20V16H10V20H14M8,20V16H4V20H8M8,14V10H4V14H8M8,8V4H4V8H8M10,14H14V10H10V14M4,2H20A2,2 0 0,1 22,4V20A2,2 0 0,1 20,22H4C2.92,22 2,21.1 2,20V4A2,2 0 0,1 4,2Z",_="M11 15H17V17H11V15M9 7H7V9H9V7M11 13H17V11H11V13M11 9H17V7H11V9M9 11H7V13H9V11M21 5V19C21 20.1 20.1 21 19 21H5C3.9 21 3 20.1 3 19V5C3 3.9 3.9 3 5 3H19C20.1 3 21 3.9 21 5M19 5H5V19H19V5M9 15H7V17H9V15Z";(0,o.Z)([(0,n.Mo)("dialog-media-player-browse")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_currentItem",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_navigateIds",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_preferredLayout",value(){return"auto"}},{kind:"field",decorators:[(0,n.IO)("ha-media-player-browse")],key:"_browser",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this._navigateIds=e.navigateIds||[{media_content_id:void 0,media_content_type:void 0}]}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,this._navigateIds=void 0,this._currentItem=void 0,this._preferredLayout="auto",this.classList.remove("opened"),(0,r.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return this._params&&this._navigateIds?s.dy`
      <ha-dialog
        open
        scrimClickAction
        escapeKeyAction
        hideActions
        flexContent
        .heading=${this._currentItem?this._currentItem.title:this.hass.localize("ui.components.media-browser.media-player-browser")}
        @closed=${this.closeDialog}
        @opened=${this._dialogOpened}
      >
        <ha-dialog-header show-border slot="heading">
          ${this._navigateIds.length>1?s.dy`
                <ha-icon-button
                  slot="navigationIcon"
                  .path=${m}
                  @click=${this._goBack}
                ></ha-icon-button>
              `:s.Ld}
          <span slot="title">
            ${this._currentItem?this._currentItem.title:this.hass.localize("ui.components.media-browser.media-player-browser")}
          </span>
          <ha-media-manage-button
            slot="actionItems"
            .hass=${this.hass}
            .currentItem=${this._currentItem}
            @media-refresh=${this._refreshMedia}
          ></ha-media-manage-button>
          <ha-button-menu
            slot="actionItems"
            @action=${this._handleMenuAction}
            @closed=${c.U}
            fixed
          >
            <ha-icon-button
              slot="trigger"
              .label=${this.hass.localize("ui.common.menu")}
              .path=${v}
            ></ha-icon-button>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.components.media-browser.auto")}
              <ha-svg-icon
                class=${"auto"===this._preferredLayout?"selected_menu_item":""}
                slot="graphic"
                .path=${u}
              ></ha-svg-icon>
            </mwc-list-item>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.components.media-browser.grid")}
              <ha-svg-icon
                class=${"grid"===this._preferredLayout?"selected_menu_item":""}
                slot="graphic"
                .path=${g}
              ></ha-svg-icon>
            </mwc-list-item>
            <mwc-list-item graphic="icon">
              ${this.hass.localize("ui.components.media-browser.list")}
              <ha-svg-icon
                slot="graphic"
                class=${"list"===this._preferredLayout?"selected_menu_item":""}
                .path=${_}
              ></ha-svg-icon>
            </mwc-list-item>
          </ha-button-menu>
          <ha-icon-button
            .label=${this.hass.localize("ui.dialogs.generic.close")}
            .path=${p}
            dialogAction="close"
            slot="actionItems"
          ></ha-icon-button>
        </ha-dialog-header>
        <ha-media-player-browse
          dialog
          .hass=${this.hass}
          .entityId=${this._params.entityId}
          .navigateIds=${this._navigateIds}
          .action=${this._action}
          .preferredLayout=${this._preferredLayout}
          @close-dialog=${this.closeDialog}
          @media-picked=${this._mediaPicked}
          @media-browsed=${this._mediaBrowsed}
        ></ha-media-player-browse>
      </ha-dialog>
    `:s.Ld}},{kind:"method",key:"_dialogOpened",value:function(){this.classList.add("opened")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:this._preferredLayout="auto";break;case 1:this._preferredLayout="grid";break;case 2:this._preferredLayout="list"}}},{kind:"method",key:"_goBack",value:function(){var e;this._navigateIds=null===(e=this._navigateIds)||void 0===e?void 0:e.slice(0,-1),this._currentItem=void 0}},{kind:"method",key:"_mediaBrowsed",value:function(e){this._navigateIds=e.detail.ids,this._currentItem=e.detail.current}},{kind:"method",key:"_mediaPicked",value:function(e){this._params.mediaPickedCallback(e.detail),"play"!==this._action&&this.closeDialog()}},{kind:"get",key:"_action",value:function(){return this._params.action||"play"}},{kind:"method",key:"_refreshMedia",value:function(){this._browser.refresh()}},{kind:"get",static:!0,key:"styles",value:function(){return[d.yu,s.iv`
        ha-dialog {
          --dialog-z-index: 9;
          --dialog-content-padding: 0;
        }

        ha-media-player-browse {
          --media-browser-max-height: calc(100vh - 65px);
          direction: ltr;
        }

        :host(.opened) ha-media-player-browse {
          height: calc(100vh - 65px);
        }

        @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --dialog-surface-position: fixed;
            --dialog-surface-top: 40px;
            --mdc-dialog-max-height: calc(100vh - 72px);
          }
          ha-media-player-browse {
            position: initial;
            --media-browser-max-height: 100vh - 137px;
            width: 700px;
          }
        }

        ha-dialog-header ha-media-manage-button {
          --mdc-theme-primary: var(--primary-text-color);
          margin: 6px;
          display: block;
        }
      `]}}]}}),s.oi);a()}catch(u){a(u)}}))},57435:(e,t,i)=>{i.a(e,(async(e,t)=>{try{var a=i(73958),o=i(565),s=i(47838),n=(i(44577),i(9644)),r=i(36924),d=i(3747),l=i(18394),c=i(56112),h=i(29950),u=(i(99539),i(7648)),m=(i(60298),i(26884)),p=e([u]);u=(p.then?(await p)():p)[0];(0,a.Z)([(0,r.Mo)("ha-browse-media-tts")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,r.Cb)()],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"item",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"action",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_language",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_voice",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_provider",value:void 0},{kind:"field",decorators:[(0,d.t)({key:"TtsMessage",state:!0,subscribe:!1})],key:"_message",value:void 0},{kind:"method",key:"render",value:function(){var e,t;return n.dy`<ha-card>
      <div class="card-content">
        <ha-textarea
          autogrow
          .label=${this.hass.localize("ui.components.media-browser.tts.message")}
          .value=${this._message||this.hass.localize("ui.components.media-browser.tts.example_message",{name:(null===(e=this.hass.user)||void 0===e?void 0:e.name)||""})}
        >
        </ha-textarea>
        ${null!==(t=this._provider)&&void 0!==t&&null!==(t=t.supported_languages)&&void 0!==t&&t.length?n.dy` <div class="options">
              <ha-language-picker
                .hass=${this.hass}
                .languages=${this._provider.supported_languages}
                .value=${this._language}
                required
                @value-changed=${this._languageChanged}
              ></ha-language-picker>
              <ha-tts-voice-picker
                .hass=${this.hass}
                .value=${this._voice}
                .engineId=${this._provider.engine_id}
                .language=${this._language}
                required
                @value-changed=${this._voiceChanged}
              ></ha-tts-voice-picker>
            </div>`:n.Ld}
      </div>
      <div class="card-actions">
        <mwc-button @click=${this._ttsClicked}>
          ${this.hass.localize(`ui.components.media-browser.tts.action_${this.action}`)}
        </mwc-button>
      </div>
    </ha-card> `}},{kind:"method",key:"willUpdate",value:function(e){var t;if((0,o.Z)((0,s.Z)(i.prototype),"willUpdate",this).call(this,e),e.has("item")&&this.item.media_content_id){var a;const e=new URLSearchParams(this.item.media_content_id.split("?")[1]),t=e.get("message"),i=e.get("language"),o=e.get("voice");t&&(this._message=t),i&&(this._language=i),o&&(this._voice=o);const s=(0,c.Xk)(this.item.media_content_id);s!==(null===(a=this._provider)||void 0===a?void 0:a.engine_id)&&(this._provider=void 0,(0,c.yP)(this.hass,s).then((e=>{var t;if(this._provider=e.provider,!this._language&&null!==(t=e.provider.supported_languages)&&void 0!==t&&t.length){var i;const t=`${this.hass.config.language}-${this.hass.config.country}`.toLowerCase(),a=e.provider.supported_languages.find((e=>e.toLowerCase()===t));if(a)return void(this._language=a);this._language=null===(i=e.provider.supported_languages)||void 0===i?void 0:i.find((e=>e.substring(0,2)===this.hass.config.language.substring(0,2)))}})),"cloud"===s&&(0,m.LI)(this.hass).then((e=>{e.logged_in&&(this._language=e.prefs.tts_default_voice[0])})))}if(e.has("_message"))return;const n=null===(t=this.shadowRoot.querySelector("ha-textarea"))||void 0===t?void 0:t.value;void 0!==n&&n!==this._message&&(this._message=n)}},{kind:"method",key:"_languageChanged",value:function(e){this._language=e.detail.value}},{kind:"method",key:"_voiceChanged",value:function(e){this._voice=e.detail.value}},{kind:"method",key:"_ttsClicked",value:async function(){const e=this.shadowRoot.querySelector("ha-textarea").value;this._message=e;const t={...this.item},i=new URLSearchParams;i.append("message",e),this._language&&i.append("language",this._language),this._voice&&i.append("voice",this._voice),t.media_content_id=`${t.media_content_id.split("?")[0]}?${i.toString()}`,t.can_play=!0,t.title=e,(0,l.B)(this,"tts-picked",{item:t})}},{kind:"field",static:!0,key:"styles",value(){return[h.k1,n.iv`
      :host {
        margin: 16px auto;
        padding: 0 8px;
        display: flex;
        flex-direction: column;
        max-width: 448px;
      }
      .options {
        margin-top: 16px;
        display: flex;
        justify-content: space-between;
      }
      ha-textarea {
        width: 100%;
      }
      button.link {
        color: var(--primary-color);
      }
    `]}}]}}),n.oi);t()}catch(v){t(v)}}))},82029:(e,t,i)=>{var a=i(73958),o=(i(30437),i(9644)),s=i(36924),n=i(18394),r=i(23469);i(37662);(0,a.Z)([(0,s.Mo)("ha-media-manage-button")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"currentItem",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_uploading",value(){return 0}},{kind:"method",key:"render",value:function(){return this.currentItem&&(0,r.aV)(this.currentItem.media_content_id||"")?o.dy`
      <mwc-button
        .label=${this.hass.localize("ui.components.media-browser.file_management.manage")}
        @click=${this._manage}
      >
        <ha-svg-icon .path=${"M19.39 10.74L11 19.13V20H4C2.9 20 2 19.11 2 18V6C2 4.89 2.89 4 4 4H10L12 6H20C21.1 6 22 6.89 22 8V10.15C21.74 10.06 21.46 10 21.17 10C20.5 10 19.87 10.26 19.39 10.74M13 19.96V22H15.04L21.17 15.88L19.13 13.83L13 19.96M22.85 13.47L21.53 12.15C21.33 11.95 21 11.95 20.81 12.15L19.83 13.13L21.87 15.17L22.85 14.19C23.05 14 23.05 13.67 22.85 13.47Z"} slot="icon"></ha-svg-icon>
      </mwc-button>
    `:o.Ld}},{kind:"method",key:"_manage",value:function(){var e,t;e=this,t={currentItem:this.currentItem,onClose:()=>(0,n.B)(this,"media-refresh")},(0,n.B)(e,"show-dialog",{dialogTag:"dialog-media-manage",dialogImport:()=>Promise.all([i.e(1985),i.e(7165),i.e(7765)]).then(i.bind(i,77765)),dialogParams:t})}},{kind:"field",static:!0,key:"styles",value(){return o.iv`
    mwc-button {
      /* We use icon + text to show disabled state */
      --mdc-button-disabled-ink-color: --mdc-theme-primary;
    }

    ha-svg-icon[slot="icon"],
    ha-circular-progress[slot="icon"] {
      vertical-align: middle;
    }

    ha-svg-icon[slot="icon"] {
      margin-inline-start: 0px;
      margin-inline-end: 8px;
      direction: var(--direction);
    }
  `}}]}}),o.oi)},15758:(e,t,i)=>{i.a(e,(async(e,t)=>{try{var a=i(73958),o=i(565),s=i(47838),n=i(20335),r=(i(30437),i(24103),i(44577),i(33829),i(9644)),d=i(36924),l=i(8636),c=i(70483),h=i(22142),u=i(18394),m=i(51750),p=i(72218),v=i(21157),g=i(78889),_=i(23469),y=i(56112),b=i(11285),f=i(23636),k=i(29950),x=i(72824),w=i(84728),$=(i(91998),i(23860),i(85878),i(68336),i(7006),i(99040),i(54371),i(37662),i(57435)),z=i(62782),L=e([$]);$=(L.then?(await L)():L)[0];const I="M21.5 9.5L20.09 10.92L17 7.83V13.5C17 17.09 14.09 20 10.5 20H4V18H10.5C13 18 15 16 15 13.5V7.83L11.91 10.91L10.5 9.5L16 4L21.5 9.5Z",C="M8,5.14V19.14L19,12.14L8,5.14Z",H="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z";(0,a.Z)([(0,d.Mo)("ha-media-player-browse")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"entityId",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"action",value(){return"play"}},{kind:"field",decorators:[(0,d.Cb)()],key:"preferredLayout",value(){return"auto"}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"dialog",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)()],key:"navigateIds",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean,attribute:"narrow",reflect:!0})],key:"_narrow",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean,attribute:"scroll",reflect:!0})],key:"_scrolled",value(){return!1}},{kind:"field",decorators:[(0,d.SB)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_parentItem",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_currentItem",value:void 0},{kind:"field",decorators:[(0,d.IO)(".header")],key:"_header",value:void 0},{kind:"field",decorators:[(0,d.IO)(".content")],key:"_content",value:void 0},{kind:"field",decorators:[(0,d.IO)("lit-virtualizer")],key:"_virtualizer",value:void 0},{kind:"field",key:"_observed",value(){return!1}},{kind:"field",key:"_headerOffsetHeight",value(){return 0}},{kind:"field",key:"_resizeObserver",value:void 0},{kind:"method",key:"connectedCallback",value:function(){(0,o.Z)((0,s.Z)(i.prototype),"connectedCallback",this).call(this),this.updateComplete.then((()=>this._attachResizeObserver()))}},{kind:"method",key:"disconnectedCallback",value:function(){(0,o.Z)((0,s.Z)(i.prototype),"disconnectedCallback",this).call(this),this._resizeObserver&&this._resizeObserver.disconnect()}},{kind:"method",key:"refresh",value:async function(){const e=this.navigateIds[this.navigateIds.length-1];try{this._currentItem=await this._fetchData(this.entityId,e.media_content_id,e.media_content_type),(0,u.B)(this,"media-browsed",{ids:this.navigateIds,current:this._currentItem})}catch(t){this._setError(t)}}},{kind:"method",key:"play",value:function(){var e;null!==(e=this._currentItem)&&void 0!==e&&e.can_play&&this._runAction(this._currentItem)}},{kind:"method",key:"willUpdate",value:function(e){var t;if((0,o.Z)((0,s.Z)(i.prototype),"willUpdate",this).call(this,e),this.hasUpdated||(0,z.o)(),e.has("entityId"))this._setError(void 0);else if(!e.has("navigateIds"))return;this._setError(void 0);const a=e.get("navigateIds"),n=this.navigateIds;null===(t=this._content)||void 0===t||t.scrollTo(0,0),this._scrolled=!1;const r=this._currentItem,d=this._parentItem;this._currentItem=void 0,this._parentItem=void 0;const l=n[n.length-1],c=n.length>1?n[n.length-2]:void 0;let h,m;e.has("entityId")||(a&&n.length===a.length+1&&a.every(((e,t)=>{const i=n[t];return i.media_content_id===e.media_content_id&&i.media_content_type===e.media_content_type}))?m=Promise.resolve(r):a&&n.length===a.length-1&&n.every(((e,t)=>{const i=a[t];return e.media_content_id===i.media_content_id&&e.media_content_type===i.media_content_type}))&&(h=Promise.resolve(d))),h||(h=this._fetchData(this.entityId,l.media_content_id,l.media_content_type)),h.then((e=>{this._currentItem=e,(0,u.B)(this,"media-browsed",{ids:n,current:e})}),(t=>{var i;a&&e.has("entityId")&&n.length===a.length&&a.every(((e,t)=>n[t].media_content_id===e.media_content_id&&n[t].media_content_type===e.media_content_type))?(0,u.B)(this,"media-browsed",{ids:[{media_content_id:void 0,media_content_type:void 0}],replace:!0}):"entity_not_found"===t.code&&(0,v.rk)(null===(i=this.hass.states[this.entityId])||void 0===i?void 0:i.state)?this._setError({message:this.hass.localize("ui.components.media-browser.media_player_unavailable"),code:"entity_not_found"}):this._setError(t)})),m||void 0===c||(m=this._fetchData(this.entityId,c.media_content_id,c.media_content_type)),m&&m.then((e=>{this._parentItem=e}))}},{kind:"method",key:"shouldUpdate",value:function(e){if(e.size>1||!e.has("hass"))return!0;const t=e.get("hass");return void 0===t||t.localize!==this.hass.localize}},{kind:"method",key:"firstUpdated",value:function(){this._measureCard(),this._attachResizeObserver()}},{kind:"method",key:"updated",value:function(e){if((0,o.Z)((0,s.Z)(i.prototype),"updated",this).call(this,e),e.has("_scrolled"))this._animateHeaderHeight();else if(e.has("_currentItem")){var t;if(this._setHeaderHeight(),this._observed)return;const e=null===(t=this._virtualizer)||void 0===t?void 0:t._virtualizer;e&&(this._observed=!0,setTimeout((()=>e._observeMutations()),0))}}},{kind:"method",key:"render",value:function(){if(this._error)return r.dy`
        <div class="container">
          <ha-alert alert-type="error">
            ${this._renderError(this._error)}
          </ha-alert>
        </div>
      `;if(!this._currentItem)return r.dy`<ha-circular-progress indeterminate></ha-circular-progress>`;const e=this._currentItem,t=this.hass.localize(`ui.components.media-browser.class.${e.media_class}`),i=e.children||[],a=g.Fn[e.media_class],o=e.children_media_class?g.Fn[e.children_media_class]:g.Fn.directory,s=e.thumbnail?this._getThumbnailURLorBase64(e.thumbnail).then((e=>`url(${e})`)):"none";return r.dy`
              ${e.can_play?r.dy`
                      <div
                        class="header ${(0,l.$)({"no-img":!e.thumbnail,"no-dialog":!this.dialog})}"
                        @transitionend=${this._setHeaderHeight}
                      >
                        <div class="header-content">
                          ${e.thumbnail?r.dy`
                                <div
                                  class="img"
                                  style="background-image: ${(0,h.C)(s,"")}"
                                >
                                  ${this._narrow&&null!=e&&e.can_play?r.dy`
                                        <ha-fab
                                          mini
                                          .item=${e}
                                          @click=${this._actionClicked}
                                        >
                                          <ha-svg-icon
                                            slot="icon"
                                            .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                            .path=${"play"===this.action?C:H}
                                          ></ha-svg-icon>
                                          ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                                        </ha-fab>
                                      `:""}
                                </div>
                              `:r.Ld}
                          <div class="header-info">
                            <div class="breadcrumb">
                              <h1 class="title">${e.title}</h1>
                              ${t?r.dy` <h2 class="subtitle">${t}</h2> `:""}
                            </div>
                            ${!e.can_play||e.thumbnail&&this._narrow?"":r.dy`
                                  <mwc-button
                                    raised
                                    .item=${e}
                                    @click=${this._actionClicked}
                                  >
                                    <ha-svg-icon
                                      .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                                      .path=${"play"===this.action?C:H}
                                    ></ha-svg-icon>
                                    ${this.hass.localize(`ui.components.media-browser.${this.action}`)}
                                  </mwc-button>
                                `}
                          </div>
                        </div>
                      </div>
                    `:""}
          <div
            class="content"
            @scroll=${this._scroll}
            @touchmove=${this._scroll}
          >
            ${this._error?r.dy`
                    <div class="container">
                      <ha-alert alert-type="error">
                        ${this._renderError(this._error)}
                      </ha-alert>
                    </div>
                  `:(0,y.b_)(e.media_content_id)?r.dy`
                      <ha-browse-media-tts
                        .item=${e}
                        .hass=${this.hass}
                        .action=${this.action}
                        @tts-picked=${this._ttsPicked}
                      ></ha-browse-media-tts>
                    `:i.length||e.not_shown?"grid"===this.preferredLayout||"auto"===this.preferredLayout&&"grid"===o.layout?r.dy`
                          <lit-virtualizer
                            scroller
                            .layout=${(0,n.e)({itemSize:{width:"175px",height:"portrait"===o.thumbnail_ratio?"312px":"225px"},gap:"16px",flex:{preserve:"aspect-ratio"},justify:"space-evenly",direction:"vertical"})}
                            .items=${i}
                            .renderItem=${this._renderGridItem}
                            class="children ${(0,l.$)({portrait:"portrait"===o.thumbnail_ratio,not_shown:!!e.not_shown})}"
                          ></lit-virtualizer>
                          ${e.not_shown?r.dy`
                                <div class="grid not-shown">
                                  <div class="title">
                                    ${this.hass.localize("ui.components.media-browser.not_shown",{count:e.not_shown})}
                                  </div>
                                </div>
                              `:""}
                        `:r.dy`
                          <mwc-list>
                            <lit-virtualizer
                              scroller
                              .items=${i}
                              style=${(0,c.V)({height:72*i.length+26+"px"})}
                              .renderItem=${this._renderListItem}
                            ></lit-virtualizer>
                            ${e.not_shown?r.dy`
                                  <mwc-list-item
                                    noninteractive
                                    class="not-shown"
                                    .graphic=${a.show_list_images?"medium":"avatar"}
                                    dir=${(0,m.Zu)(this.hass)}
                                  >
                                    <span class="title">
                                      ${this.hass.localize("ui.components.media-browser.not_shown",{count:e.not_shown})}
                                    </span>
                                  </mwc-list-item>
                                `:""}
                          </mwc-list>
                        `:r.dy`
                        <div class="container no-items">
                          ${"media-source://media_source/local/."===e.media_content_id?r.dy`
                                <div class="highlight-add-button">
                                  <span>
                                    <ha-svg-icon
                                      .path=${I}
                                    ></ha-svg-icon>
                                  </span>
                                  <span>
                                    ${this.hass.localize("ui.components.media-browser.file_management.highlight_button")}
                                  </span>
                                </div>
                              `:this.hass.localize("ui.components.media-browser.no_items")}
                        </div>
                      `}
          </div>
        </div>
      </div>
    `}},{kind:"field",key:"_renderGridItem",value(){return e=>{const t=e.thumbnail?this._getThumbnailURLorBase64(e.thumbnail).then((e=>`url(${e})`)):"none";return r.dy`
      <div class="child" .item=${e} @click=${this._childClicked}>
        <ha-card outlined>
          <div class="thumbnail">
            ${e.thumbnail?r.dy`
                  <div
                    class="${(0,l.$)({"centered-image":["app","directory"].includes(e.media_class),"brand-image":(0,x.zC)(e.thumbnail)})} image"
                    style="background-image: ${(0,h.C)(t,"")}"
                  ></div>
                `:r.dy`
                  <div class="icon-holder image">
                    <ha-svg-icon
                      class="folder"
                      .path=${g.Fn["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
                    ></ha-svg-icon>
                  </div>
                `}
            ${e.can_play?r.dy`
                  <ha-icon-button
                    class="play ${(0,l.$)({can_expand:e.can_expand})}"
                    .item=${e}
                    .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                    .path=${"play"===this.action?C:H}
                    @click=${this._actionClicked}
                  ></ha-icon-button>
                `:""}
          </div>
          <div class="title">
            ${e.title}
            <simple-tooltip fitToVisibleBounds position="top" offset="4"
              >${e.title}</simple-tooltip
            >
          </div>
        </ha-card>
      </div>
    `}}},{kind:"field",key:"_renderListItem",value(){return e=>{const t=this._currentItem,i=g.Fn[t.media_class],a=i.show_list_images&&e.thumbnail?this._getThumbnailURLorBase64(e.thumbnail).then((e=>`url(${e})`)):"none";return r.dy`
      <mwc-list-item
        @click=${this._childClicked}
        .item=${e}
        .graphic=${i.show_list_images?"medium":"avatar"}
        dir=${(0,m.Zu)(this.hass)}
      >
        ${"none"!==a||e.can_play?r.dy`<div
              class=${(0,l.$)({graphic:!0,thumbnail:!0===i.show_list_images})}
              style="background-image: ${(0,h.C)(a,"")}"
              slot="graphic"
            >
              ${e.can_play?r.dy`<ha-icon-button
                    class="play ${(0,l.$)({show:!i.show_list_images||!e.thumbnail})}"
                    .item=${e}
                    .label=${this.hass.localize(`ui.components.media-browser.${this.action}-media`)}
                    .path=${"play"===this.action?C:H}
                    @click=${this._actionClicked}
                  ></ha-icon-button>`:r.Ld}
            </div>`:r.dy`<ha-svg-icon
              .path=${g.Fn["directory"===e.media_class&&e.children_media_class||e.media_class].icon}
              slot="graphic"
            ></ha-svg-icon>`}
        <span class="title">${e.title}</span>
      </mwc-list-item>
    `}}},{kind:"method",key:"_getThumbnailURLorBase64",value:async function(e){if(!e)return"";if(e.startsWith("/"))return new Promise(((t,i)=>{this.hass.fetchWithAuth(e).then((e=>e.blob())).then((e=>{const a=new FileReader;a.onload=()=>{const e=a.result;t("string"==typeof e?e:"")},a.onerror=e=>i(e),a.readAsDataURL(e)}))}));var t;(0,x.zC)(e)&&(e=(0,x.X1)({domain:(0,x.u4)(e),type:"icon",useFallback:!0,darkOptimized:null===(t=this.hass.themes)||void 0===t?void 0:t.darkMode}));return e}},{kind:"field",key:"_actionClicked",value(){return e=>{e.stopPropagation();const t=e.currentTarget.item;this._runAction(t)}}},{kind:"method",key:"_runAction",value:function(e){(0,u.B)(this,"media-picked",{item:e,navigateIds:this.navigateIds})}},{kind:"method",key:"_ttsPicked",value:function(e){e.stopPropagation();const t=this.navigateIds.slice(0,-1);t.push(e.detail.item),(0,u.B)(this,"media-picked",{...e.detail,navigateIds:t})}},{kind:"field",key:"_childClicked",value(){return async e=>{const t=e.currentTarget.item;t&&(t.can_expand?(0,u.B)(this,"media-browsed",{ids:[...this.navigateIds,t]}):this._runAction(t))}}},{kind:"method",key:"_fetchData",value:async function(e,t,i){return e!==g.N8?(0,g.zz)(this.hass,e,t,i):(0,_.b)(this.hass,t)}},{kind:"method",key:"_measureCard",value:function(){this._narrow=(this.dialog?window.innerWidth:this.offsetWidth)<450}},{kind:"method",key:"_attachResizeObserver",value:async function(){this._resizeObserver||(await(0,f.j)(),this._resizeObserver=new ResizeObserver((0,p.D)((()=>this._measureCard()),250,!1))),this._resizeObserver.observe(this)}},{kind:"method",key:"_closeDialogAction",value:function(){(0,u.B)(this,"close-dialog")}},{kind:"method",key:"_setError",value:function(e){this.dialog?e&&(this._closeDialogAction(),(0,b.Ys)(this,{title:this.hass.localize("ui.components.media-browser.media_browsing_error"),text:this._renderError(e)})):this._error=e}},{kind:"method",key:"_renderError",value:function(e){return"Media directory does not exist."===e.message?r.dy`
        <h2>
          ${this.hass.localize("ui.components.media-browser.no_local_media_found")}
        </h2>
        <p>
          ${this.hass.localize("ui.components.media-browser.no_media_folder")}
          <br />
          ${this.hass.localize("ui.components.media-browser.setup_local_help",{documentation:r.dy`<a
              href=${(0,w.R)(this.hass,"/more-info/local-media/setup-media")}
              target="_blank"
              rel="noreferrer"
              >${this.hass.localize("ui.components.media-browser.documentation")}</a
            >`})}
          <br />
          ${this.hass.localize("ui.components.media-browser.local_media_files")}
        </p>
      `:r.dy`<span class="error">${e.message}</span>`}},{kind:"method",key:"_setHeaderHeight",value:async function(){await this.updateComplete;const e=this._header,t=this._content;e&&t&&(this._headerOffsetHeight=e.offsetHeight,t.style.marginTop=`${this._headerOffsetHeight}px`,t.style.maxHeight=`calc(var(--media-browser-max-height, 100%) - ${this._headerOffsetHeight}px)`)}},{kind:"method",key:"_animateHeaderHeight",value:function(){let e;const t=i=>{void 0===e&&(e=i);const a=i-e;this._setHeaderHeight(),a<400&&requestAnimationFrame(t)};requestAnimationFrame(t)}},{kind:"method",decorators:[(0,d.hO)({passive:!0})],key:"_scroll",value:function(e){const t=e.currentTarget;!this._scrolled&&t.scrollTop>this._headerOffsetHeight?this._scrolled=!0:this._scrolled&&t.scrollTop<this._headerOffsetHeight&&(this._scrolled=!1)}},{kind:"get",static:!0,key:"styles",value:function(){return[k.Qx,r.iv`
        :host {
          display: flex;
          flex-direction: column;
          position: relative;
        }

        ha-circular-progress {
          --mdc-theme-primary: var(--primary-color);
          display: flex;
          justify-content: center;
          margin: 40px;
        }

        .container {
          padding: 16px;
        }

        .no-items {
          padding-left: 32px;
        }

        .highlight-add-button {
          display: flex;
          flex-direction: row-reverse;
          margin-right: 48px;
        }

        .highlight-add-button ha-svg-icon {
          position: relative;
          top: -0.5em;
          margin-left: 8px;
        }

        .content {
          overflow-y: auto;
          box-sizing: border-box;
          height: 100%;
        }

        /* HEADER */

        .header {
          display: flex;
          justify-content: space-between;
          border-bottom: 1px solid var(--divider-color);
          background-color: var(--card-background-color);
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          z-index: 3;
          padding: 16px;
        }
        .header_button {
          position: relative;
          right: -8px;
        }
        .header-content {
          display: flex;
          flex-wrap: wrap;
          flex-grow: 1;
          align-items: flex-start;
        }
        .header-content .img {
          height: 175px;
          width: 175px;
          margin-right: 16px;
          background-size: cover;
          border-radius: 2px;
          transition:
            width 0.4s,
            height 0.4s;
        }
        .header-info {
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          align-self: stretch;
          min-width: 0;
          flex: 1;
        }
        .header-info mwc-button {
          display: block;
          --mdc-theme-primary: var(--primary-color);
          padding-bottom: 16px;
        }
        .breadcrumb {
          display: flex;
          flex-direction: column;
          overflow: hidden;
          flex-grow: 1;
          padding-top: 16px;
        }
        .breadcrumb .title {
          font-size: 32px;
          line-height: 1.2;
          font-weight: bold;
          margin: 0;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 2;
          padding-right: 8px;
        }
        .breadcrumb .previous-title {
          font-size: 14px;
          padding-bottom: 8px;
          color: var(--secondary-text-color);
          overflow: hidden;
          text-overflow: ellipsis;
          cursor: pointer;
          --mdc-icon-size: 14px;
        }
        .breadcrumb .subtitle {
          font-size: 16px;
          overflow: hidden;
          text-overflow: ellipsis;
          margin-bottom: 0;
          transition:
            height 0.5s,
            margin 0.5s;
        }

        .not-shown {
          font-style: italic;
          color: var(--secondary-text-color);
          padding: 8px 16px 8px;
        }

        .grid.not-shown {
          display: flex;
          align-items: center;
          text-align: center;
        }

        /* ============= CHILDREN ============= */

        mwc-list {
          --mdc-list-vertical-padding: 0;
          --mdc-list-item-graphic-margin: 0;
          --mdc-theme-text-icon-on-background: var(--secondary-text-color);
          margin-top: 10px;
        }

        mwc-list li:last-child {
          display: none;
        }

        mwc-list li[divider] {
          border-bottom-color: var(--divider-color);
        }

        mwc-list-item {
          width: 100%;
        }

        div.children {
          display: grid;
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.1fr)
          );
          grid-gap: 16px;
          padding: 16px;
        }

        :host([dialog]) .children {
          grid-template-columns: repeat(
            auto-fit,
            minmax(var(--media-browse-item-size, 175px), 0.33fr)
          );
        }

        .child {
          display: flex;
          flex-direction: column;
          cursor: pointer;
        }

        ha-card {
          position: relative;
          width: 100%;
          box-sizing: border-box;
        }

        .children ha-card .thumbnail {
          width: 100%;
          position: relative;
          box-sizing: border-box;
          transition: padding-bottom 0.1s ease-out;
          padding-bottom: 100%;
        }

        .portrait ha-card .thumbnail {
          padding-bottom: 150%;
        }

        ha-card .image {
          border-radius: 3px 3px 0 0;
        }

        .image {
          position: absolute;
          top: 0;
          right: 0;
          left: 0;
          bottom: 0;
          background-size: cover;
          background-repeat: no-repeat;
          background-position: center;
        }

        .centered-image {
          margin: 0 8px;
          background-size: contain;
        }

        .brand-image {
          background-size: 40%;
        }

        .children ha-card .icon-holder {
          display: flex;
          justify-content: center;
          align-items: center;
        }

        .child .folder {
          color: var(--secondary-text-color);
          --mdc-icon-size: calc(var(--media-browse-item-size, 175px) * 0.4);
        }

        .child .play {
          position: absolute;
          transition: color 0.5s;
          border-radius: 50%;
          top: calc(50% - 50px);
          right: calc(50% - 35px);
          opacity: 0;
          transition: opacity 0.1s ease-out;
        }

        .child .play:not(.can_expand) {
          --mdc-icon-button-size: 70px;
          --mdc-icon-size: 48px;
        }

        ha-card:hover .play {
          opacity: 1;
        }

        ha-card:hover .play:not(.can_expand) {
          color: var(--primary-color);
        }

        ha-card:hover .play.can_expand {
          bottom: 8px;
        }

        .child .play.can_expand {
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          top: auto;
          bottom: 0px;
          right: 8px;
          transition:
            bottom 0.1s ease-out,
            opacity 0.1s ease-out;
        }

        .child .play:hover {
          color: var(--primary-color);
        }

        .child .title {
          font-size: 16px;
          padding-top: 16px;
          padding-left: 2px;
          overflow: hidden;
          display: -webkit-box;
          -webkit-box-orient: vertical;
          -webkit-line-clamp: 1;
          text-overflow: ellipsis;
        }

        .child ha-card .title {
          margin-bottom: 16px;
          padding-left: 16px;
        }

        mwc-list-item .graphic {
          background-size: contain;
          background-repeat: no-repeat;
          background-position: center;
          border-radius: 2px;
          display: flex;
          align-content: center;
          align-items: center;
          line-height: initial;
        }

        mwc-list-item .graphic .play {
          opacity: 0;
          transition: all 0.5s;
          background-color: rgba(var(--rgb-card-background-color), 0.5);
          border-radius: 50%;
          --mdc-icon-button-size: 40px;
        }

        mwc-list-item:hover .graphic .play {
          opacity: 1;
          color: var(--primary-text-color);
        }

        mwc-list-item .graphic .play.show {
          opacity: 1;
          background-color: transparent;
        }

        mwc-list-item .title {
          margin-left: 16px;
        }
        mwc-list-item[dir="rtl"] .title {
          margin-right: 16px;
          margin-left: 0;
        }

        /* ============= Narrow ============= */

        :host([narrow]) {
          padding: 0;
        }

        :host([narrow]) .media-source {
          padding: 0 24px;
        }

        :host([narrow]) div.children {
          grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        }

        :host([narrow]) .breadcrumb .title {
          font-size: 24px;
        }
        :host([narrow]) .header {
          padding: 0;
        }
        :host([narrow]) .header.no-dialog {
          display: block;
        }
        :host([narrow]) .header_button {
          position: absolute;
          top: 14px;
          right: 8px;
        }
        :host([narrow]) .header-content {
          flex-direction: column;
          flex-wrap: nowrap;
        }
        :host([narrow]) .header-content .img {
          height: auto;
          width: 100%;
          margin-right: 0;
          padding-bottom: 50%;
          margin-bottom: 8px;
          position: relative;
          background-position: center;
          border-radius: 0;
          transition:
            width 0.4s,
            height 0.4s,
            padding-bottom 0.4s;
        }
        ha-fab {
          position: absolute;
          --mdc-theme-secondary: var(--primary-color);
          bottom: -20px;
          right: 20px;
        }
        :host([narrow]) .header-info mwc-button {
          margin-top: 16px;
          margin-bottom: 8px;
        }
        :host([narrow]) .header-info {
          padding: 0 16px 8px;
        }

        /* ============= Scroll ============= */
        :host([scroll]) .breadcrumb .subtitle {
          height: 0;
          margin: 0;
        }
        :host([scroll]) .breadcrumb .title {
          -webkit-line-clamp: 1;
        }
        :host(:not([narrow])[scroll]) .header:not(.no-img) ha-icon-button {
          align-self: center;
        }
        :host([scroll]) .header-info mwc-button,
        .no-img .header-info mwc-button {
          padding-right: 4px;
        }
        :host([scroll][narrow]) .no-img .header-info mwc-button {
          padding-right: 16px;
        }
        :host([scroll]) .header-info {
          flex-direction: row;
        }
        :host([scroll]) .header-info mwc-button {
          align-self: center;
          margin-top: 0;
          margin-bottom: 0;
          padding-bottom: 0;
        }
        :host([scroll][narrow]) .no-img .header-info {
          flex-direction: row-reverse;
        }
        :host([scroll][narrow]) .header-info {
          padding: 20px 24px 10px 24px;
          align-items: center;
        }
        :host([scroll]) .header-content {
          align-items: flex-end;
          flex-direction: row;
        }
        :host([scroll]) .header-content .img {
          height: 75px;
          width: 75px;
        }
        :host([scroll]) .breadcrumb {
          padding-top: 0;
          align-self: center;
        }
        :host([scroll][narrow]) .header-content .img {
          height: 100px;
          width: 100px;
          padding-bottom: initial;
          margin-bottom: 0;
        }
        :host([scroll]) ha-fab {
          bottom: 0px;
          right: -24px;
          --mdc-fab-box-shadow: none;
          --mdc-theme-secondary: rgba(var(--rgb-primary-color), 0.5);
        }

        lit-virtualizer {
          height: 100%;
          overflow: overlay !important;
          contain: size layout !important;
        }

        lit-virtualizer.not_shown {
          height: calc(100% - 36px);
        }
      `]}}]}}),r.oi);t()}catch(I){t(I)}}))},26884:(e,t,i)=>{i.d(t,{LI:()=>a});const a=e=>e.callWS({type:"cloud/status"})},23469:(e,t,i)=>{i.d(t,{Qr:()=>n,aV:()=>o,b:()=>a,oE:()=>s});const a=(e,t)=>e.callWS({type:"media_source/browse_media",media_content_id:t}),o=e=>e.startsWith("media-source://media_source"),s=async(e,t,i)=>{const a=new FormData;a.append("media_content_id",t),a.append("file",i);const o=await e.fetchWithAuth("/api/media_source/local_source/upload",{method:"POST",body:a});if(413===o.status)throw new Error(`Uploaded file is too large (${i.name})`);if(200!==o.status)throw new Error("Unknown error");return o.json()},n=async(e,t)=>e.callWS({type:"media_source/local_source/remove",media_content_id:t})},56112:(e,t,i)=>{i.d(t,{MV:()=>d,Wg:()=>n,Xk:()=>s,b_:()=>o,yP:()=>r});const a="media-source://tts/",o=e=>e.startsWith(a),s=e=>e.substring(19),n=(e,t,i)=>e.callWS({type:"tts/engine/list",language:t,country:i}),r=(e,t)=>e.callWS({type:"tts/engine/get",engine_id:t}),d=(e,t,i)=>e.callWS({type:"tts/engine/voices",engine_id:t,language:i})},23636:(e,t,i)=>{i.d(t,{j:()=>a});const a=async()=>{try{new ResizeObserver((()=>{}))}catch(e){window.ResizeObserver=(await i.e(5442).then(i.bind(i,5442))).default}}},62782:(e,t,i)=>{i.d(t,{o:()=>o});var a=i(23636);const o=async()=>{await(0,a.j)(),await i.e(6175).then(i.bind(i,86175))}},84728:(e,t,i)=>{i.d(t,{R:()=>a});const a=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`}}]);
//# sourceMappingURL=9aac670d.js.map