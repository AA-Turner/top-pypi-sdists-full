/*! For license information please see 2379.99db2e9178f03143.js.LICENSE.txt */
export const __webpack_id__="2379";export const __webpack_ids__=["2379"];export const __webpack_modules__={34887:function(e,t,i){var o=i(62826),a=i(27680),r=(i(83298),i(59924)),s=i(96196),n=i(77845),d=i(32288),l=i(92542),c=(i(94343),i(78740));class h extends c.h{willUpdate(e){super.willUpdate(e),(e.has("value")||e.has("forceBlankValue"))&&this.forceBlankValue&&this.value&&(this.value="")}constructor(...e){super(...e),this.forceBlankValue=!1}}(0,o.__decorate)([(0,n.MZ)({type:Boolean,attribute:"force-blank-value"})],h.prototype,"forceBlankValue",void 0),h=(0,o.__decorate)([(0,n.EM)("ha-combo-box-textfield")],h);i(60733),i(56768);(0,r.SF)("vaadin-combo-box-item",s.AH`
    :host {
      padding: 0 !important;
    }
    :host([focused]:not([disabled])) {
      background-color: rgba(var(--rgb-primary-text-color, 0, 0, 0), 0.12);
    }
    :host([selected]:not([disabled])) {
      background-color: transparent;
      color: var(--mdc-theme-primary);
      --mdc-ripple-color: var(--mdc-theme-primary);
      --mdc-theme-text-primary-on-background: var(--mdc-theme-primary);
    }
    :host([selected]:not([disabled])):before {
      background-color: var(--mdc-theme-primary);
      opacity: 0.12;
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
    :host([selected][focused]:not([disabled])):before {
      opacity: 0.24;
    }
    :host(:hover:not([disabled])) {
      background-color: transparent;
    }
    [part="content"] {
      width: 100%;
    }
    [part="checkmark"] {
      display: none;
    }
  `);class p extends s.WF{async open(){await this.updateComplete,this._comboBox?.open()}async focus(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}disconnectedCallback(){super.disconnectedCallback(),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}get selectedItem(){return this._comboBox.selectedItem}setInputValue(e){this._comboBox.value=e}setTextFieldValue(e){this._inputElement.value=e}render(){return s.qy`
      <!-- @ts-ignore Tag definition is not included in theme folder -->
      <vaadin-combo-box-light
        .itemValuePath=${this.itemValuePath}
        .itemIdPath=${this.itemIdPath}
        .itemLabelPath=${this.itemLabelPath}
        .items=${this.items}
        .value=${this.value||""}
        .filteredItems=${this.filteredItems}
        .dataProvider=${this.dataProvider}
        .allowCustomValue=${this.allowCustomValue}
        .disabled=${this.disabled}
        .required=${this.required}
        ${(0,a.d)(this.renderer||this._defaultRowRenderer)}
        @opened-changed=${this._openedChanged}
        @filter-changed=${this._filterChanged}
        @value-changed=${this._valueChanged}
        attr-for-value="value"
      >
        <ha-combo-box-textfield
          label=${(0,d.J)(this.label)}
          placeholder=${(0,d.J)(this.placeholder)}
          ?disabled=${this.disabled}
          ?required=${this.required}
          validationMessage=${(0,d.J)(this.validationMessage)}
          .errorMessage=${this.errorMessage}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          .autocorrect=${!1}
          input-spellcheck="false"
          .suffix=${s.qy`<div
            style="width: 28px;"
            role="none presentation"
          ></div>`}
          .icon=${this.icon}
          .invalid=${this.invalid}
          .forceBlankValue=${this._forceBlankValue}
        >
          <slot name="icon" slot="leadingIcon"></slot>
        </ha-combo-box-textfield>
        ${this.value&&!this.hideClearIcon?s.qy`<ha-svg-icon
              role="button"
              tabindex="-1"
              aria-label=${(0,d.J)(this.hass?.localize("ui.common.clear"))}
              class=${"clear-button "+(this.label?"":"no-label")}
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              ?disabled=${this.disabled}
              @click=${this._clearValue}
            ></ha-svg-icon>`:""}
        <ha-svg-icon
          role="button"
          tabindex="-1"
          aria-label=${(0,d.J)(this.label)}
          aria-expanded=${this.opened?"true":"false"}
          class=${"toggle-button "+(this.label?"":"no-label")}
          .path=${this.opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}
          ?disabled=${this.disabled}
          @click=${this._toggleOpen}
        ></ha-svg-icon>
      </vaadin-combo-box-light>
      ${this._renderHelper()}
    `}_renderHelper(){return this.helper?s.qy`<ha-input-helper-text .disabled=${this.disabled}
          >${this.helper}</ha-input-helper-text
        >`:""}_clearValue(e){e.stopPropagation(),(0,l.r)(this,"value-changed",{value:void 0})}_toggleOpen(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}_openedChanged(e){e.stopPropagation();const t=e.detail.value;if(setTimeout(()=>{this.opened=t,(0,l.r)(this,"opened-changed",{value:e.detail.value})},0),this.clearInitialValue&&(this.setTextFieldValue(""),t?setTimeout(()=>{this._forceBlankValue=!1},100):this._forceBlankValue=!0),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}_observeBody(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver(e=>{e.forEach(e=>{e.addedNodes.forEach(e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)}),e.removedNodes.forEach(e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)})})}),this._bodyMutationObserver.observe(document.body,{childList:!0}))}_removeInert(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver(e=>{e.forEach(e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}})}),this._overlayMutationObserver.observe(e,{attributes:!0}))}_filterChanged(e){e.stopPropagation(),(0,l.r)(this,"filter-changed",{value:e.detail.value})}_valueChanged(e){if(e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0),!this.opened)return;const t=e.detail.value;t!==this.value&&(0,l.r)(this,"value-changed",{value:t||void 0})}constructor(...e){super(...e),this.invalid=!1,this.icon=!1,this.allowCustomValue=!1,this.itemValuePath="value",this.itemLabelPath="label",this.disabled=!1,this.required=!1,this.opened=!1,this.hideClearIcon=!1,this.clearInitialValue=!1,this._forceBlankValue=!1,this._defaultRowRenderer=e=>s.qy`
    <ha-combo-box-item type="button">
      ${this.itemLabelPath?e[this.itemLabelPath]:e}
    </ha-combo-box-item>
  `}}p.styles=s.AH`
    :host {
      display: block;
      width: 100%;
    }
    vaadin-combo-box-light {
      position: relative;
    }
    ha-combo-box-textfield {
      width: 100%;
    }
    ha-combo-box-textfield > ha-icon-button {
      --mdc-icon-button-size: 24px;
      padding: 2px;
      color: var(--secondary-text-color);
    }
    ha-svg-icon {
      color: var(--input-dropdown-icon-color);
      position: absolute;
      cursor: pointer;
    }
    .toggle-button {
      right: 12px;
      top: -10px;
      inset-inline-start: initial;
      inset-inline-end: 12px;
      direction: var(--direction);
    }
    :host([opened]) .toggle-button {
      color: var(--primary-color);
    }
    .toggle-button[disabled],
    .clear-button[disabled] {
      color: var(--disabled-text-color);
      pointer-events: none;
    }
    .toggle-button.no-label {
      top: -3px;
    }
    .clear-button {
      --mdc-icon-size: 20px;
      top: -7px;
      right: 36px;
      inset-inline-start: initial;
      inset-inline-end: 36px;
      direction: var(--direction);
    }
    .clear-button.no-label {
      top: 0;
    }
    ha-input-helper-text {
      margin-top: 4px;
    }
  `,(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"label",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"value",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"placeholder",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"validationMessage",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"helper",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"error-message"})],p.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"invalid",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"icon",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"items",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"filteredItems",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"dataProvider",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"allow-custom-value",type:Boolean})],p.prototype,"allowCustomValue",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"item-value-path"})],p.prototype,"itemValuePath",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"item-label-path"})],p.prototype,"itemLabelPath",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"item-id-path"})],p.prototype,"itemIdPath",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"renderer",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"required",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0})],p.prototype,"opened",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean,attribute:"hide-clear-icon"})],p.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean,attribute:"clear-initial-value"})],p.prototype,"clearInitialValue",void 0),(0,o.__decorate)([(0,n.P)("vaadin-combo-box-light",!0)],p.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,n.P)("ha-combo-box-textfield",!0)],p.prototype,"_inputElement",void 0),(0,o.__decorate)([(0,n.wk)({type:Boolean})],p.prototype,"_forceBlankValue",void 0),p=(0,o.__decorate)([(0,n.EM)("ha-combo-box")],p)},34811:function(e,t,i){var o=i(62826),a=i(96196),r=i(77845),s=i(94333),n=i(92542),d=i(99034);i(60961);class l extends a.WF{render(){const e=this.noCollapse?a.s6:a.qy`
          <ha-svg-icon
            .path=${"M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z"}
            class="summary-icon ${(0,s.H)({expanded:this.expanded})}"
          ></ha-svg-icon>
        `;return a.qy`
      <div class="top ${(0,s.H)({expanded:this.expanded})}">
        <div
          id="summary"
          class=${(0,s.H)({noCollapse:this.noCollapse})}
          @click=${this._toggleContainer}
          @keydown=${this._toggleContainer}
          @focus=${this._focusChanged}
          @blur=${this._focusChanged}
          role="button"
          tabindex=${this.noCollapse?-1:0}
          aria-expanded=${this.expanded}
          aria-controls="sect1"
          part="summary"
        >
          ${this.leftChevron?e:a.s6}
          <slot name="leading-icon"></slot>
          <slot name="header">
            <div class="header">
              ${this.header}
              <slot class="secondary" name="secondary">${this.secondary}</slot>
            </div>
          </slot>
          ${this.leftChevron?a.s6:e}
          <slot name="icons"></slot>
        </div>
      </div>
      <div
        class="container ${(0,s.H)({expanded:this.expanded})}"
        @transitionend=${this._handleTransitionEnd}
        role="region"
        aria-labelledby="summary"
        aria-hidden=${!this.expanded}
        tabindex="-1"
      >
        ${this._showContent?a.qy`<slot></slot>`:""}
      </div>
    `}willUpdate(e){super.willUpdate(e),e.has("expanded")&&(this._showContent=this.expanded,setTimeout(()=>{this._container.style.overflow=this.expanded?"initial":"hidden"},300))}_handleTransitionEnd(){this._container.style.removeProperty("height"),this._container.style.overflow=this.expanded?"initial":"hidden",this._showContent=this.expanded}async _toggleContainer(e){if(e.defaultPrevented)return;if("keydown"===e.type&&"Enter"!==e.key&&" "!==e.key)return;if(e.preventDefault(),this.noCollapse)return;const t=!this.expanded;(0,n.r)(this,"expanded-will-change",{expanded:t}),this._container.style.overflow="hidden",t&&(this._showContent=!0,await(0,d.E)());const i=this._container.scrollHeight;this._container.style.height=`${i}px`,t||setTimeout(()=>{this._container.style.height="0px"},0),this.expanded=t,(0,n.r)(this,"expanded-changed",{expanded:this.expanded})}_focusChanged(e){this.noCollapse||this.shadowRoot.querySelector(".top").classList.toggle("focused","focus"===e.type)}constructor(...e){super(...e),this.expanded=!1,this.outlined=!1,this.leftChevron=!1,this.noCollapse=!1,this._showContent=this.expanded}}l.styles=a.AH`
    :host {
      display: block;
    }

    .top {
      display: flex;
      align-items: center;
      border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
    }

    .top.expanded {
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }

    .top.focused {
      background: var(--input-fill-color);
    }

    :host([outlined]) {
      box-shadow: none;
      border-width: 1px;
      border-style: solid;
      border-color: var(--outline-color);
      border-radius: var(--ha-card-border-radius, var(--ha-border-radius-lg));
    }

    .summary-icon {
      transition: transform 150ms cubic-bezier(0.4, 0, 0.2, 1);
      direction: var(--direction);
      margin-left: 8px;
      margin-inline-start: 8px;
      margin-inline-end: initial;
      border-radius: var(--ha-border-radius-circle);
    }

    #summary:focus-visible ha-svg-icon.summary-icon {
      background-color: var(--ha-color-fill-neutral-normal-active);
    }

    :host([left-chevron]) .summary-icon,
    ::slotted([slot="leading-icon"]) {
      margin-left: 0;
      margin-right: 8px;
      margin-inline-start: 0;
      margin-inline-end: 8px;
    }

    #summary {
      flex: 1;
      display: flex;
      padding: var(--expansion-panel-summary-padding, 0 8px);
      min-height: 48px;
      align-items: center;
      cursor: pointer;
      overflow: hidden;
      font-weight: var(--ha-font-weight-medium);
      outline: none;
    }
    #summary.noCollapse {
      cursor: default;
    }

    .summary-icon.expanded {
      transform: rotate(180deg);
    }

    .header,
    ::slotted([slot="header"]) {
      flex: 1;
      overflow-wrap: anywhere;
      color: var(--primary-text-color);
    }

    .container {
      padding: var(--expansion-panel-content-padding, 0 8px);
      overflow: hidden;
      transition: height 300ms cubic-bezier(0.4, 0, 0.2, 1);
      height: 0px;
    }

    .container.expanded {
      height: auto;
    }

    .secondary {
      display: block;
      color: var(--secondary-text-color);
      font-size: var(--ha-font-size-s);
    }
  `,(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],l.prototype,"expanded",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],l.prototype,"outlined",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"left-chevron",type:Boolean,reflect:!0})],l.prototype,"leftChevron",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"no-collapse",type:Boolean,reflect:!0})],l.prototype,"noCollapse",void 0),(0,o.__decorate)([(0,r.MZ)()],l.prototype,"header",void 0),(0,o.__decorate)([(0,r.MZ)()],l.prototype,"secondary",void 0),(0,o.__decorate)([(0,r.wk)()],l.prototype,"_showContent",void 0),(0,o.__decorate)([(0,r.P)(".container")],l.prototype,"_container",void 0),l=(0,o.__decorate)([(0,r.EM)("ha-expansion-panel")],l)},88867:function(e,t,i){i.r(t),i.d(t,{HaIconPicker:()=>u});var o=i(62826),a=i(96196),r=i(77845),s=i(22786),n=i(92542),d=i(33978);i(34887),i(22598),i(94343);let l=[],c=!1;const h=async e=>{try{const t=d.y[e].getIconList;if("function"!=typeof t)return[];const i=await t();return i.map(t=>({icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords??[]}))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},p=e=>a.qy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    ${e.icon}
  </ha-combo-box-item>
`;class u extends a.WF{render(){return a.qy`
      <ha-combo-box
        .hass=${this.hass}
        item-value-path="icon"
        item-label-path="icon"
        .value=${this._value}
        allow-custom-value
        .dataProvider=${c?this._iconProvider:void 0}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
        .placeholder=${this.placeholder}
        .errorMessage=${this.errorMessage}
        .invalid=${this.invalid}
        .renderer=${p}
        icon
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        ${this._value||this.placeholder?a.qy`
              <ha-icon .icon=${this._value||this.placeholder} slot="icon">
              </ha-icon>
            `:a.qy`<slot slot="icon" name="fallback"></slot>`}
      </ha-combo-box>
    `}async _openedChanged(e){e.detail.value&&!c&&(await(async()=>{c=!0;const e=await i.e("3451").then(i.t.bind(i,83174,19));l=e.default.map(e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords}));const t=[];Object.keys(d.y).forEach(e=>{t.push(h(e))}),(await Promise.all(t)).forEach(e=>{l.push(...e)})})(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.r)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,s.A)((e,t=l)=>{if(!e)return t;const i=[],o=(e,t)=>i.push({icon:e,rank:t});for(const a of t)a.parts.has(e)?o(a.icon,1):a.keywords.includes(e)?o(a.icon,2):a.icon.includes(e)?o(a.icon,3):a.keywords.some(t=>t.includes(e))&&o(a.icon,4);return 0===i.length&&o(e,0),i.sort((e,t)=>e.rank-t.rank)}),this._iconProvider=(e,t)=>{const i=this._filterIcons(e.filter.toLowerCase(),l),o=e.page*e.pageSize,a=o+e.pageSize;t(i.slice(o,a),i.length)}}}u.styles=a.AH`
    *[slot="icon"] {
      color: var(--primary-text-color);
      position: relative;
      bottom: 2px;
    }
    *[slot="prefix"] {
      margin-right: 8px;
      margin-inline-end: 8px;
      margin-inline-start: initial;
    }
  `,(0,o.__decorate)([(0,r.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,o.__decorate)([(0,r.MZ)()],u.prototype,"value",void 0),(0,o.__decorate)([(0,r.MZ)()],u.prototype,"label",void 0),(0,o.__decorate)([(0,r.MZ)()],u.prototype,"helper",void 0),(0,o.__decorate)([(0,r.MZ)()],u.prototype,"placeholder",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:"error-message"})],u.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],u.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],u.prototype,"required",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],u.prototype,"invalid",void 0),u=(0,o.__decorate)([(0,r.EM)("ha-icon-picker")],u)},7153:function(e,t,i){var o=i(62826),a=i(4845),r=i(49065),s=i(96196),n=i(77845),d=i(7647);class l extends a.U{firstUpdated(){super.firstUpdated(),this.addEventListener("change",()=>{this.haptic&&(0,d.j)(this,"light")})}constructor(...e){super(...e),this.haptic=!1}}l.styles=[r.R,s.AH`
      :host {
        --mdc-theme-secondary: var(--switch-checked-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__thumb {
        background-color: var(--switch-checked-button-color);
        border-color: var(--switch-checked-button-color);
      }
      .mdc-switch.mdc-switch--checked .mdc-switch__track {
        background-color: var(--switch-checked-track-color);
        border-color: var(--switch-checked-track-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
        background-color: var(--switch-unchecked-button-color);
        border-color: var(--switch-unchecked-button-color);
      }
      .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
        background-color: var(--switch-unchecked-track-color);
        border-color: var(--switch-unchecked-track-color);
      }
    `],(0,o.__decorate)([(0,n.MZ)({type:Boolean})],l.prototype,"haptic",void 0),l=(0,o.__decorate)([(0,n.EM)("ha-switch")],l)},7647:function(e,t,i){i.d(t,{j:()=>a});var o=i(92542);const a=(e,t)=>{(0,o.r)(e,"haptic",t)}},77238:function(e,t,i){i.r(t);var o=i(62826),a=i(96196),r=i(77845),s=i(92542),n=(i(34811),i(88867),i(7153),i(78740),i(39396));class d extends a.WF{set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._maximum=e.maximum??void 0,this._minimum=e.minimum??void 0,this._restore=e.restore??!0,this._step=e.step??1,this._initial=e.initial??0):(this._name="",this._icon="",this._maximum=void 0,this._minimum=void 0,this._restore=!0,this._step=1,this._initial=0)}focus(){this.updateComplete.then(()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus())}render(){return this.hass?a.qy`
      <div class="form">
        <ha-textfield
          .value=${this._name}
          .configValue=${"name"}
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.name")}
          autoValidate
          required
          .validationMessage=${this.hass.localize("ui.dialogs.helper_settings.required_error_msg")}
          dialogInitialFocus
          .disabled=${this.disabled}
        ></ha-textfield>
        <ha-icon-picker
          .hass=${this.hass}
          .value=${this._icon}
          .configValue=${"icon"}
          @value-changed=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.generic.icon")}
          .disabled=${this.disabled}
        ></ha-icon-picker>
        <ha-textfield
          .value=${this._minimum}
          .configValue=${"minimum"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.minimum")}
          .disabled=${this.disabled}
        ></ha-textfield>
        <ha-textfield
          .value=${this._maximum}
          .configValue=${"maximum"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.maximum")}
          .disabled=${this.disabled}
        ></ha-textfield>
        <ha-textfield
          .value=${this._initial}
          .configValue=${"initial"}
          type="number"
          @input=${this._valueChanged}
          .label=${this.hass.localize("ui.dialogs.helper_settings.counter.initial")}
          .disabled=${this.disabled}
        ></ha-textfield>
        <ha-expansion-panel
          header=${this.hass.localize("ui.dialogs.helper_settings.generic.advanced_settings")}
          outlined
        >
          <ha-textfield
            .value=${this._step}
            .configValue=${"step"}
            type="number"
            @input=${this._valueChanged}
            .label=${this.hass.localize("ui.dialogs.helper_settings.counter.step")}
            .disabled=${this.disabled}
          ></ha-textfield>
          <div class="row">
            <ha-switch
              .checked=${this._restore}
              .configValue=${"restore"}
              @change=${this._valueChanged}
              .disabled=${this.disabled}
            >
            </ha-switch>
            <div>
              ${this.hass.localize("ui.dialogs.helper_settings.counter.restore")}
            </div>
          </div>
        </ha-expansion-panel>
      </div>
    `:a.s6}_valueChanged(e){if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target,i=t.configValue,o="number"===t.type?""!==t.value?Number(t.value):void 0:"ha-switch"===t.localName?e.target.checked:e.detail?.value||t.value;if(this[`_${i}`]===o)return;const a={...this._item};void 0===o||""===o?delete a[i]:a[i]=o,(0,s.r)(this,"value-changed",{value:a})}static get styles(){return[n.RF,a.AH`
        .form {
          color: var(--primary-text-color);
        }
        .row {
          margin-top: 12px;
          margin-bottom: 12px;
          color: var(--primary-text-color);
          display: flex;
          align-items: center;
        }
        .row div {
          margin-left: 16px;
          margin-inline-start: 16px;
          margin-inline-end: initial;
        }
        ha-textfield {
          display: block;
          margin: 8px 0;
        }
      `]}constructor(...e){super(...e),this.new=!1,this.disabled=!1}}(0,o.__decorate)([(0,r.MZ)({attribute:!1})],d.prototype,"hass",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],d.prototype,"new",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],d.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_name",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_icon",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_maximum",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_minimum",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_restore",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_initial",void 0),(0,o.__decorate)([(0,r.wk)()],d.prototype,"_step",void 0),d=(0,o.__decorate)([(0,r.EM)("ha-counter-form")],d)},4845:function(e,t,i){i.d(t,{U:()=>_});var o=i(62826),a=(i(27673),i(9270)),r=i(12451),s=i(56161),n=i(99864),d=i(7658),l={CHECKED:"mdc-switch--checked",DISABLED:"mdc-switch--disabled"},c={ARIA_CHECKED_ATTR:"aria-checked",NATIVE_CONTROL_SELECTOR:".mdc-switch__native-control",RIPPLE_SURFACE_SELECTOR:".mdc-switch__thumb-underlay"};const h=function(e){function t(i){return e.call(this,(0,o.__assign)((0,o.__assign)({},t.defaultAdapter),i))||this}return(0,o.__extends)(t,e),Object.defineProperty(t,"strings",{get:function(){return c},enumerable:!1,configurable:!0}),Object.defineProperty(t,"cssClasses",{get:function(){return l},enumerable:!1,configurable:!0}),Object.defineProperty(t,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlChecked:function(){},setNativeControlDisabled:function(){},setNativeControlAttr:function(){}}},enumerable:!1,configurable:!0}),t.prototype.setChecked=function(e){this.adapter.setNativeControlChecked(e),this.updateAriaChecked(e),this.updateCheckedStyling(e)},t.prototype.setDisabled=function(e){this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(l.DISABLED):this.adapter.removeClass(l.DISABLED)},t.prototype.handleChange=function(e){var t=e.target;this.updateAriaChecked(t.checked),this.updateCheckedStyling(t.checked)},t.prototype.updateCheckedStyling=function(e){e?this.adapter.addClass(l.CHECKED):this.adapter.removeClass(l.CHECKED)},t.prototype.updateAriaChecked=function(e){this.adapter.setNativeControlAttr(c.ARIA_CHECKED_ATTR,""+!!e)},t}(d.I);var p=i(96196),u=i(77845),m=i(32288);class _ extends r.O{changeHandler(e){this.mdcFoundation.handleChange(e),this.checked=this.formElement.checked}createAdapter(){return Object.assign(Object.assign({},(0,r.i)(this.mdcRoot)),{setNativeControlChecked:e=>{this.formElement.checked=e},setNativeControlDisabled:e=>{this.formElement.disabled=e},setNativeControlAttr:(e,t)=>{this.formElement.setAttribute(e,t)}})}renderRipple(){return this.shouldRenderRipple?p.qy`
        <mwc-ripple
          .accent="${this.checked}"
          .disabled="${this.disabled}"
          unbounded>
        </mwc-ripple>`:""}focus(){const e=this.formElement;e&&(this.rippleHandlers.startFocus(),e.focus())}blur(){const e=this.formElement;e&&(this.rippleHandlers.endFocus(),e.blur())}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",e=>{this.dispatchEvent(new Event("change",e))})}render(){return p.qy`
      <div class="mdc-switch">
        <div class="mdc-switch__track"></div>
        <div class="mdc-switch__thumb-underlay">
          ${this.renderRipple()}
          <div class="mdc-switch__thumb">
            <input
              type="checkbox"
              id="basic-switch"
              class="mdc-switch__native-control"
              role="switch"
              aria-label="${(0,m.J)(this.ariaLabel)}"
              aria-labelledby="${(0,m.J)(this.ariaLabelledBy)}"
              @change="${this.changeHandler}"
              @focus="${this.handleRippleFocus}"
              @blur="${this.handleRippleBlur}"
              @mousedown="${this.handleRippleMouseDown}"
              @mouseenter="${this.handleRippleMouseEnter}"
              @mouseleave="${this.handleRippleMouseLeave}"
              @touchstart="${this.handleRippleTouchStart}"
              @touchend="${this.handleRippleDeactivate}"
              @touchcancel="${this.handleRippleDeactivate}">
          </div>
        </div>
      </div>`}handleRippleMouseDown(e){const t=()=>{window.removeEventListener("mouseup",t),this.handleRippleDeactivate()};window.addEventListener("mouseup",t),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}handleRippleBlur(){this.rippleHandlers.endFocus()}constructor(){super(...arguments),this.checked=!1,this.disabled=!1,this.shouldRenderRipple=!1,this.mdcFoundationClass=h,this.rippleHandlers=new n.I(()=>(this.shouldRenderRipple=!0,this.ripple))}}(0,o.__decorate)([(0,u.MZ)({type:Boolean}),(0,s.P)(function(e){this.mdcFoundation.setChecked(e)})],_.prototype,"checked",void 0),(0,o.__decorate)([(0,u.MZ)({type:Boolean}),(0,s.P)(function(e){this.mdcFoundation.setDisabled(e)})],_.prototype,"disabled",void 0),(0,o.__decorate)([a.T,(0,u.MZ)({attribute:"aria-label"})],_.prototype,"ariaLabel",void 0),(0,o.__decorate)([a.T,(0,u.MZ)({attribute:"aria-labelledby"})],_.prototype,"ariaLabelledBy",void 0),(0,o.__decorate)([(0,u.P)(".mdc-switch")],_.prototype,"mdcRoot",void 0),(0,o.__decorate)([(0,u.P)("input")],_.prototype,"formElement",void 0),(0,o.__decorate)([(0,u.nJ)("mwc-ripple")],_.prototype,"ripple",void 0),(0,o.__decorate)([(0,u.wk)()],_.prototype,"shouldRenderRipple",void 0),(0,o.__decorate)([(0,u.Ls)({passive:!0})],_.prototype,"handleRippleMouseDown",null),(0,o.__decorate)([(0,u.Ls)({passive:!0})],_.prototype,"handleRippleTouchStart",null)},49065:function(e,t,i){i.d(t,{R:()=>o});const o=i(96196).AH`.mdc-switch__thumb-underlay{left:-14px;right:initial;top:-17px;width:48px;height:48px}[dir=rtl] .mdc-switch__thumb-underlay,.mdc-switch__thumb-underlay[dir=rtl]{left:initial;right:-14px}.mdc-switch__native-control{width:64px;height:48px}.mdc-switch{display:inline-block;position:relative;outline:none;user-select:none}.mdc-switch.mdc-switch--checked .mdc-switch__track{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-switch.mdc-switch--checked .mdc-switch__thumb{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786);border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__track{background-color:#000;background-color:var(--mdc-theme-on-surface, #000)}.mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb{background-color:#fff;background-color:var(--mdc-theme-surface, #fff);border-color:#fff;border-color:var(--mdc-theme-surface, #fff)}.mdc-switch__native-control{left:0;right:initial;position:absolute;top:0;margin:0;opacity:0;cursor:pointer;pointer-events:auto;transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1)}[dir=rtl] .mdc-switch__native-control,.mdc-switch__native-control[dir=rtl]{left:initial;right:0}.mdc-switch__track{box-sizing:border-box;width:36px;height:14px;border:1px solid transparent;border-radius:7px;opacity:.38;transition:opacity 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb-underlay{display:flex;position:absolute;align-items:center;justify-content:center;transform:translateX(0);transition:transform 90ms cubic-bezier(0.4, 0, 0.2, 1),background-color 90ms cubic-bezier(0.4, 0, 0.2, 1),border-color 90ms cubic-bezier(0.4, 0, 0.2, 1)}.mdc-switch__thumb{box-shadow:0px 3px 1px -2px rgba(0, 0, 0, 0.2),0px 2px 2px 0px rgba(0, 0, 0, 0.14),0px 1px 5px 0px rgba(0,0,0,.12);box-sizing:border-box;width:20px;height:20px;border:10px solid;border-radius:50%;pointer-events:none;z-index:1}.mdc-switch--checked .mdc-switch__track{opacity:.54}.mdc-switch--checked .mdc-switch__thumb-underlay{transform:translateX(16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__thumb-underlay,.mdc-switch--checked .mdc-switch__thumb-underlay[dir=rtl]{transform:translateX(-16px)}.mdc-switch--checked .mdc-switch__native-control{transform:translateX(-16px)}[dir=rtl] .mdc-switch--checked .mdc-switch__native-control,.mdc-switch--checked .mdc-switch__native-control[dir=rtl]{transform:translateX(16px)}.mdc-switch--disabled{opacity:.38;pointer-events:none}.mdc-switch--disabled .mdc-switch__thumb{border-width:1px}.mdc-switch--disabled .mdc-switch__native-control{cursor:default;pointer-events:none}:host{display:inline-flex;outline:none;-webkit-tap-highlight-color:transparent}`}};
//# sourceMappingURL=2379.99db2e9178f03143.js.map