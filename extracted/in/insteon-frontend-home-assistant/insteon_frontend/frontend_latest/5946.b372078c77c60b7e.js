/*! For license information please see 5946.b372078c77c60b7e.js.LICENSE.txt */
export const __webpack_id__="5946";export const __webpack_ids__=["5946"];export const __webpack_modules__={92209:function(e,t,i){i.d(t,{x:()=>o});const o=(e,t)=>e&&e.config.components.includes(t)},53045:function(e,t,i){i.d(t,{v:()=>o});const o=(e,t,i,o)=>{const[a,r,s]=e.split(".",3);return Number(a)>t||Number(a)===t&&(void 0===o?Number(r)>=i:Number(r)>i)||void 0!==o&&Number(a)===t&&Number(r)===i&&Number(s)>=o}},94343:function(e,t,i){var o=i(62826),a=i(96196),r=i(77845),s=i(23897);class l extends s.G{constructor(...e){super(...e),this.borderTop=!1}}l.styles=[...s.J,a.AH`
      :host {
        --md-list-item-one-line-container-height: 48px;
        --md-list-item-two-line-container-height: 64px;
      }
      :host([border-top]) md-item {
        border-top: 1px solid var(--divider-color);
      }
      [slot="start"] {
        --state-icon-color: var(--secondary-text-color);
      }
      [slot="headline"] {
        line-height: var(--ha-line-height-normal);
        font-size: var(--ha-font-size-m);
        white-space: nowrap;
      }
      [slot="supporting-text"] {
        line-height: var(--ha-line-height-normal);
        font-size: var(--ha-font-size-s);
        white-space: nowrap;
      }
      ::slotted(state-badge),
      ::slotted(img) {
        width: 32px;
        height: 32px;
      }
      ::slotted(.code) {
        font-family: var(--ha-font-family-code);
        font-size: var(--ha-font-size-xs);
      }
      ::slotted(.domain) {
        font-size: var(--ha-font-size-s);
        font-weight: var(--ha-font-weight-normal);
        line-height: var(--ha-line-height-normal);
        align-self: flex-end;
        max-width: 30%;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
      }
    `],(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"border-top"})],l.prototype,"borderTop",void 0),l=(0,o.__decorate)([(0,r.EM)("ha-combo-box-item")],l)},34887:function(e,t,i){var o=i(62826),a=i(27680),r=(i(83298),i(59924)),s=i(96196),l=i(77845),d=i(32288),n=i(92542),c=(i(94343),i(78740));class p extends c.h{willUpdate(e){super.willUpdate(e),(e.has("value")||e.has("forceBlankValue"))&&this.forceBlankValue&&this.value&&(this.value="")}constructor(...e){super(...e),this.forceBlankValue=!1}}(0,o.__decorate)([(0,l.MZ)({type:Boolean,attribute:"force-blank-value"})],p.prototype,"forceBlankValue",void 0),p=(0,o.__decorate)([(0,l.EM)("ha-combo-box-textfield")],p);i(60733),i(56768);(0,r.SF)("vaadin-combo-box-item",s.AH`
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
  `);class h extends s.WF{async open(){await this.updateComplete,this._comboBox?.open()}async focus(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}disconnectedCallback(){super.disconnectedCallback(),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}get selectedItem(){return this._comboBox.selectedItem}setInputValue(e){this._comboBox.value=e}setTextFieldValue(e){this._inputElement.value=e}render(){return s.qy`
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
        >`:""}_clearValue(e){e.stopPropagation(),(0,n.r)(this,"value-changed",{value:void 0})}_toggleOpen(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}_openedChanged(e){e.stopPropagation();const t=e.detail.value;if(setTimeout(()=>{this.opened=t,(0,n.r)(this,"opened-changed",{value:e.detail.value})},0),this.clearInitialValue&&(this.setTextFieldValue(""),t?setTimeout(()=>{this._forceBlankValue=!1},100):this._forceBlankValue=!0),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}_observeBody(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver(e=>{e.forEach(e=>{e.addedNodes.forEach(e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)}),e.removedNodes.forEach(e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)})})}),this._bodyMutationObserver.observe(document.body,{childList:!0}))}_removeInert(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver(e=>{e.forEach(e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}})}),this._overlayMutationObserver.observe(e,{attributes:!0}))}_filterChanged(e){e.stopPropagation(),(0,n.r)(this,"filter-changed",{value:e.detail.value})}_valueChanged(e){if(e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0),!this.opened)return;const t=e.detail.value;t!==this.value&&(0,n.r)(this,"value-changed",{value:t||void 0})}constructor(...e){super(...e),this.invalid=!1,this.icon=!1,this.allowCustomValue=!1,this.itemValuePath="value",this.itemLabelPath="label",this.disabled=!1,this.required=!1,this.opened=!1,this.hideClearIcon=!1,this.clearInitialValue=!1,this._forceBlankValue=!1,this._defaultRowRenderer=e=>s.qy`
    <ha-combo-box-item type="button">
      ${this.itemLabelPath?e[this.itemLabelPath]:e}
    </ha-combo-box-item>
  `}}h.styles=s.AH`
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
  `,(0,o.__decorate)([(0,l.MZ)({attribute:!1})],h.prototype,"hass",void 0),(0,o.__decorate)([(0,l.MZ)()],h.prototype,"label",void 0),(0,o.__decorate)([(0,l.MZ)()],h.prototype,"value",void 0),(0,o.__decorate)([(0,l.MZ)()],h.prototype,"placeholder",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:!1})],h.prototype,"validationMessage",void 0),(0,o.__decorate)([(0,l.MZ)()],h.prototype,"helper",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"error-message"})],h.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],h.prototype,"invalid",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],h.prototype,"icon",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:!1})],h.prototype,"items",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:!1})],h.prototype,"filteredItems",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:!1})],h.prototype,"dataProvider",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"allow-custom-value",type:Boolean})],h.prototype,"allowCustomValue",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"item-value-path"})],h.prototype,"itemValuePath",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"item-label-path"})],h.prototype,"itemLabelPath",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"item-id-path"})],h.prototype,"itemIdPath",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:!1})],h.prototype,"renderer",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],h.prototype,"disabled",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],h.prototype,"required",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],h.prototype,"opened",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean,attribute:"hide-clear-icon"})],h.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean,attribute:"clear-initial-value"})],h.prototype,"clearInitialValue",void 0),(0,o.__decorate)([(0,l.P)("vaadin-combo-box-light",!0)],h.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,l.P)("ha-combo-box-textfield",!0)],h.prototype,"_inputElement",void 0),(0,o.__decorate)([(0,l.wk)({type:Boolean})],h.prototype,"_forceBlankValue",void 0),h=(0,o.__decorate)([(0,l.EM)("ha-combo-box")],h)},56768:function(e,t,i){var o=i(62826),a=i(96196),r=i(77845);class s extends a.WF{render(){return a.qy`<slot></slot>`}constructor(...e){super(...e),this.disabled=!1}}s.styles=a.AH`
    :host {
      display: block;
      color: var(--mdc-text-field-label-ink-color, rgba(0, 0, 0, 0.6));
      font-size: 0.75rem;
      padding-left: 16px;
      padding-right: 16px;
      padding-inline-start: 16px;
      padding-inline-end: 16px;
      letter-spacing: var(
        --mdc-typography-caption-letter-spacing,
        0.0333333333em
      );
      line-height: normal;
    }
    :host([disabled]) {
      color: var(--mdc-text-field-disabled-ink-color, rgba(0, 0, 0, 0.6));
    }
  `,(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],s.prototype,"disabled",void 0),s=(0,o.__decorate)([(0,r.EM)("ha-input-helper-text")],s)},23897:function(e,t,i){i.d(t,{G:()=>n,J:()=>d});var o=i(62826),a=i(97154),r=i(82553),s=i(96196),l=i(77845);i(95591);const d=[r.R,s.AH`
    :host {
      --ha-icon-display: block;
      --md-sys-color-primary: var(--primary-text-color);
      --md-sys-color-secondary: var(--secondary-text-color);
      --md-sys-color-surface: var(--card-background-color);
      --md-sys-color-on-surface: var(--primary-text-color);
      --md-sys-color-on-surface-variant: var(--secondary-text-color);
    }
    md-item {
      overflow: var(--md-item-overflow, hidden);
      align-items: var(--md-item-align-items, center);
      gap: var(--ha-md-list-item-gap, 16px);
    }
  `];class n extends a.n{renderRipple(){return"text"===this.type?s.s6:s.qy`<ha-ripple
      part="ripple"
      for="item"
      ?disabled=${this.disabled&&"link"!==this.type}
    ></ha-ripple>`}}n.styles=d,n=(0,o.__decorate)([(0,l.EM)("ha-md-list-item")],n)},41944:function(e,t,i){i.r(t),i.d(t,{HaAddonSelector:()=>h});var o=i(62826),a=i(96196),r=i(77845),s=i(92209),l=i(92542),d=i(25749),n=i(95742);i(17963),i(34887),i(94343);const c=e=>a.qy`
  <ha-combo-box-item type="button">
    <span slot="headline">${e.name}</span>
    <span slot="supporting-text">${e.slug}</span>
    ${e.icon?a.qy`
          <img
            alt=""
            slot="start"
            .src="/api/hassio/addons/${e.slug}/icon"
          />
        `:a.s6}
  </ha-combo-box-item>
`;class p extends a.WF{open(){this._comboBox?.open()}focus(){this._comboBox?.focus()}firstUpdated(){this._getAddons()}render(){return this._error?a.qy`<ha-alert alert-type="error">${this._error}</ha-alert>`:this._addons?a.qy`
      <ha-combo-box
        .hass=${this.hass}
        .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.addon-picker.addon"):this.label}
        .value=${this._value}
        .required=${this.required}
        .disabled=${this.disabled}
        .helper=${this.helper}
        .renderer=${c}
        .items=${this._addons}
        item-value-path="slug"
        item-id-path="slug"
        item-label-path="name"
        @value-changed=${this._addonChanged}
      ></ha-combo-box>
    `:a.s6}async _getAddons(){try{if((0,s.x)(this.hass,"hassio")){const e=await(0,n.b3)(this.hass);this._addons=e.addons.filter(e=>e.version).sort((e,t)=>(0,d.xL)(e.name,t.name,this.hass.locale.language))}else this._error=this.hass.localize("ui.components.addon-picker.error.no_supervisor")}catch(e){this._error=this.hass.localize("ui.components.addon-picker.error.fetch_addons")}}get _value(){return this.value||""}_addonChanged(e){e.stopPropagation();const t=e.detail.value;t!==this._value&&this._setValue(t)}_setValue(e){this.value=e,setTimeout(()=>{(0,l.r)(this,"value-changed",{value:e}),(0,l.r)(this,"change")},0)}constructor(...e){super(...e),this.value="",this.disabled=!1,this.required=!1}}(0,o.__decorate)([(0,r.MZ)()],p.prototype,"label",void 0),(0,o.__decorate)([(0,r.MZ)()],p.prototype,"value",void 0),(0,o.__decorate)([(0,r.MZ)()],p.prototype,"helper",void 0),(0,o.__decorate)([(0,r.wk)()],p.prototype,"_addons",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],p.prototype,"required",void 0),(0,o.__decorate)([(0,r.P)("ha-combo-box")],p.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,r.wk)()],p.prototype,"_error",void 0),p=(0,o.__decorate)([(0,r.EM)("ha-addon-picker")],p);class h extends a.WF{render(){return a.qy`<ha-addon-picker
      .hass=${this.hass}
      .value=${this.value}
      .label=${this.label}
      .helper=${this.helper}
      .disabled=${this.disabled}
      .required=${this.required}
      allow-custom-entity
    ></ha-addon-picker>`}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}h.styles=a.AH`
    ha-addon-picker {
      width: 100%;
    }
  `,(0,o.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"hass",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"selector",void 0),(0,o.__decorate)([(0,r.MZ)()],h.prototype,"value",void 0),(0,o.__decorate)([(0,r.MZ)()],h.prototype,"label",void 0),(0,o.__decorate)([(0,r.MZ)()],h.prototype,"helper",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],h.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],h.prototype,"required",void 0),h=(0,o.__decorate)([(0,r.EM)("ha-selector-addon")],h)},78740:function(e,t,i){i.d(t,{h:()=>n});var o=i(62826),a=i(68846),r=i(92347),s=i(96196),l=i(77845),d=i(76679);class n extends a.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const i=t?"trailing":"leading";return s.qy`
      <span
        class="mdc-text-field__icon mdc-text-field__icon--${i}"
        tabindex=${t?1:-1}
      >
        <slot name="${i}Icon"></slot>
      </span>
    `}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}n.styles=[r.R,s.AH`
      .mdc-text-field__input {
        width: var(--ha-textfield-input-width, 100%);
      }
      .mdc-text-field:not(.mdc-text-field--with-leading-icon) {
        padding: var(--text-field-padding, 0px 16px);
      }
      .mdc-text-field__affix--suffix {
        padding-left: var(--text-field-suffix-padding-left, 12px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 12px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
        direction: ltr;
      }
      .mdc-text-field--with-leading-icon {
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 16px);
        direction: var(--direction);
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--with-trailing-icon {
        padding-left: var(--text-field-suffix-padding-left, 0px);
        padding-right: var(--text-field-suffix-padding-right, 0px);
        padding-inline-start: var(--text-field-suffix-padding-left, 0px);
        padding-inline-end: var(--text-field-suffix-padding-right, 0px);
      }
      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--suffix {
        color: var(--secondary-text-color);
      }

      .mdc-text-field:not(.mdc-text-field--disabled) .mdc-text-field__icon {
        color: var(--secondary-text-color);
      }

      .mdc-text-field__icon--leading {
        margin-inline-start: 16px;
        margin-inline-end: 8px;
        direction: var(--direction);
      }

      .mdc-text-field__icon--trailing {
        padding: var(--textfield-icon-trailing-padding, 12px);
      }

      .mdc-floating-label:not(.mdc-floating-label--float-above) {
        max-width: calc(100% - 16px);
      }

      .mdc-floating-label--float-above {
        max-width: calc((100% - 16px) / 0.75);
        transition: none;
      }

      input {
        text-align: var(--text-field-text-align, start);
      }

      input[type="color"] {
        height: 20px;
      }

      /* Edge, hide reveal password icon */
      ::-ms-reveal {
        display: none;
      }

      /* Chrome, Safari, Edge, Opera */
      :host([no-spinner]) input::-webkit-outer-spin-button,
      :host([no-spinner]) input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }

      input[type="color"]::-webkit-color-swatch-wrapper {
        padding: 0;
      }

      /* Firefox */
      :host([no-spinner]) input[type="number"] {
        -moz-appearance: textfield;
      }

      .mdc-text-field__ripple {
        overflow: hidden;
      }

      .mdc-text-field {
        overflow: var(--text-field-overflow);
      }

      .mdc-floating-label {
        padding-inline-end: 16px;
        padding-inline-start: initial;
        inset-inline-start: 16px !important;
        inset-inline-end: initial !important;
        transform-origin: var(--float-start);
        direction: var(--direction);
        text-align: var(--float-start);
        box-sizing: border-box;
        text-overflow: ellipsis;
      }

      .mdc-text-field--with-leading-icon.mdc-text-field--filled
        .mdc-floating-label {
        max-width: calc(
          100% - 48px - var(--text-field-suffix-padding-left, 0px)
        );
        inset-inline-start: calc(
          48px + var(--text-field-suffix-padding-left, 0px)
        ) !important;
        inset-inline-end: initial !important;
        direction: var(--direction);
      }

      .mdc-text-field__input[type="number"] {
        direction: var(--direction);
      }
      .mdc-text-field__affix--prefix {
        padding-right: var(--text-field-prefix-padding-right, 2px);
        padding-inline-end: var(--text-field-prefix-padding-right, 2px);
        padding-inline-start: initial;
      }

      .mdc-text-field:not(.mdc-text-field--disabled)
        .mdc-text-field__affix--prefix {
        color: var(--mdc-text-field-label-ink-color);
      }
      #helper-text ha-markdown {
        display: inline-block;
      }
    `,"rtl"===d.G.document.dir?s.AH`
          .mdc-text-field--with-leading-icon,
          .mdc-text-field__icon--leading,
          .mdc-floating-label,
          .mdc-text-field--with-leading-icon.mdc-text-field--filled
            .mdc-floating-label,
          .mdc-text-field__input[type="number"] {
            direction: rtl;
            --direction: rtl;
          }
        `:s.AH``],(0,o.__decorate)([(0,l.MZ)({type:Boolean})],n.prototype,"invalid",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"error-message"})],n.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],n.prototype,"icon",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],n.prototype,"iconTrailing",void 0),(0,o.__decorate)([(0,l.MZ)()],n.prototype,"autocomplete",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],n.prototype,"autocorrect",void 0),(0,o.__decorate)([(0,l.MZ)({attribute:"input-spellcheck"})],n.prototype,"inputSpellcheck",void 0),(0,o.__decorate)([(0,l.P)("input")],n.prototype,"formElement",void 0),n=(0,o.__decorate)([(0,l.EM)("ha-textfield")],n)},95742:function(e,t,i){i.d(t,{xG:()=>l,b3:()=>r,eK:()=>s});var o=i(53045);const a=e=>e.data,r=(new Set([502,503,504]),async e=>(0,o.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:"/addons",method:"get"}):a(await e.callApi("GET","hassio/addons"))),s=async(e,t)=>(0,o.v)(e.config.version,2021,2,4)?e.callWS({type:"supervisor/api",endpoint:`/addons/${t}/start`,method:"post",timeout:null}):e.callApi("POST",`hassio/addons/${t}/start`),l=async(e,t)=>{(0,o.v)(e.config.version,2021,2,4)?await e.callWS({type:"supervisor/api",endpoint:`/addons/${t}/install`,method:"post",timeout:null}):await e.callApi("POST",`hassio/addons/${t}/install`)}},82553:function(e,t,i){i.d(t,{R:()=>o});const o=i(96196).AH`:host{display:flex;-webkit-tap-highlight-color:rgba(0,0,0,0);--md-ripple-hover-color: var(--md-list-item-hover-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-hover-opacity: var(--md-list-item-hover-state-layer-opacity, 0.08);--md-ripple-pressed-color: var(--md-list-item-pressed-state-layer-color, var(--md-sys-color-on-surface, #1d1b20));--md-ripple-pressed-opacity: var(--md-list-item-pressed-state-layer-opacity, 0.12)}:host(:is([type=button]:not([disabled]),[type=link])){cursor:pointer}md-focus-ring{z-index:1;--md-focus-ring-shape: 8px}a,button,li{background:none;border:none;cursor:inherit;padding:0;margin:0;text-align:unset;text-decoration:none}.list-item{border-radius:inherit;display:flex;flex:1;max-width:inherit;min-width:inherit;outline:none;-webkit-tap-highlight-color:rgba(0,0,0,0);width:100%}.list-item.interactive{cursor:pointer}.list-item.disabled{opacity:var(--md-list-item-disabled-opacity, 0.3);pointer-events:none}[slot=container]{pointer-events:none}md-ripple{border-radius:inherit}md-item{border-radius:inherit;flex:1;height:100%;color:var(--md-list-item-label-text-color, var(--md-sys-color-on-surface, #1d1b20));font-family:var(--md-list-item-label-text-font, var(--md-sys-typescale-body-large-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-list-item-label-text-size, var(--md-sys-typescale-body-large-size, 1rem));line-height:var(--md-list-item-label-text-line-height, var(--md-sys-typescale-body-large-line-height, 1.5rem));font-weight:var(--md-list-item-label-text-weight, var(--md-sys-typescale-body-large-weight, var(--md-ref-typeface-weight-regular, 400)));min-height:var(--md-list-item-one-line-container-height, 56px);padding-top:var(--md-list-item-top-space, 12px);padding-bottom:var(--md-list-item-bottom-space, 12px);padding-inline-start:var(--md-list-item-leading-space, 16px);padding-inline-end:var(--md-list-item-trailing-space, 16px)}md-item[multiline]{min-height:var(--md-list-item-two-line-container-height, 72px)}[slot=supporting-text]{color:var(--md-list-item-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-list-item-supporting-text-font, var(--md-sys-typescale-body-medium-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-list-item-supporting-text-size, var(--md-sys-typescale-body-medium-size, 0.875rem));line-height:var(--md-list-item-supporting-text-line-height, var(--md-sys-typescale-body-medium-line-height, 1.25rem));font-weight:var(--md-list-item-supporting-text-weight, var(--md-sys-typescale-body-medium-weight, var(--md-ref-typeface-weight-regular, 400)))}[slot=trailing-supporting-text]{color:var(--md-list-item-trailing-supporting-text-color, var(--md-sys-color-on-surface-variant, #49454f));font-family:var(--md-list-item-trailing-supporting-text-font, var(--md-sys-typescale-label-small-font, var(--md-ref-typeface-plain, Roboto)));font-size:var(--md-list-item-trailing-supporting-text-size, var(--md-sys-typescale-label-small-size, 0.6875rem));line-height:var(--md-list-item-trailing-supporting-text-line-height, var(--md-sys-typescale-label-small-line-height, 1rem));font-weight:var(--md-list-item-trailing-supporting-text-weight, var(--md-sys-typescale-label-small-weight, var(--md-ref-typeface-weight-medium, 500)))}:is([slot=start],[slot=end])::slotted(*){fill:currentColor}[slot=start]{color:var(--md-list-item-leading-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}[slot=end]{color:var(--md-list-item-trailing-icon-color, var(--md-sys-color-on-surface-variant, #49454f))}@media(forced-colors: active){.disabled slot{color:GrayText}.list-item.disabled{color:GrayText;opacity:1}}
`},97154:function(e,t,i){i.d(t,{n:()=>p});var o=i(62826),a=(i(4469),i(20903),i(71970),i(96196)),r=i(77845),s=i(94333),l=i(28345),d=i(20618),n=i(27525);const c=(0,d.n)(a.WF);class p extends c{get isDisabled(){return this.disabled&&"link"!==this.type}willUpdate(e){this.href&&(this.type="link"),super.willUpdate(e)}render(){return this.renderListItem(a.qy`
      <md-item>
        <div slot="container">
          ${this.renderRipple()} ${this.renderFocusRing()}
        </div>
        <slot name="start" slot="start"></slot>
        <slot name="end" slot="end"></slot>
        ${this.renderBody()}
      </md-item>
    `)}renderListItem(e){const t="link"===this.type;let i;switch(this.type){case"link":i=l.eu`a`;break;case"button":i=l.eu`button`;break;default:i=l.eu`li`}const o="text"!==this.type,r=t&&this.target?this.target:a.s6;return l.qy`
      <${i}
        id="item"
        tabindex="${this.isDisabled||!o?-1:0}"
        ?disabled=${this.isDisabled}
        role="listitem"
        aria-selected=${this.ariaSelected||a.s6}
        aria-checked=${this.ariaChecked||a.s6}
        aria-expanded=${this.ariaExpanded||a.s6}
        aria-haspopup=${this.ariaHasPopup||a.s6}
        class="list-item ${(0,s.H)(this.getRenderClasses())}"
        href=${this.href||a.s6}
        target=${r}
        @focus=${this.onFocus}
      >${e}</${i}>
    `}renderRipple(){return"text"===this.type?a.s6:a.qy` <md-ripple
      part="ripple"
      for="item"
      ?disabled=${this.isDisabled}></md-ripple>`}renderFocusRing(){return"text"===this.type?a.s6:a.qy` <md-focus-ring
      @visibility-changed=${this.onFocusRingVisibilityChanged}
      part="focus-ring"
      for="item"
      inward></md-focus-ring>`}onFocusRingVisibilityChanged(e){}getRenderClasses(){return{disabled:this.isDisabled}}renderBody(){return a.qy`
      <slot></slot>
      <slot name="overline" slot="overline"></slot>
      <slot name="headline" slot="headline"></slot>
      <slot name="supporting-text" slot="supporting-text"></slot>
      <slot
        name="trailing-supporting-text"
        slot="trailing-supporting-text"></slot>
    `}onFocus(){-1===this.tabIndex&&this.dispatchEvent((0,n.cG)())}focus(){this.listItemRoot?.focus()}click(){this.listItemRoot?this.listItemRoot.click():super.click()}constructor(){super(...arguments),this.disabled=!1,this.type="text",this.isListItem=!0,this.href="",this.target=""}}p.shadowRootOptions={...a.WF.shadowRootOptions,delegatesFocus:!0},(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],p.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.MZ)({reflect:!0})],p.prototype,"type",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,attribute:"md-list-item",reflect:!0})],p.prototype,"isListItem",void 0),(0,o.__decorate)([(0,r.MZ)()],p.prototype,"href",void 0),(0,o.__decorate)([(0,r.MZ)()],p.prototype,"target",void 0),(0,o.__decorate)([(0,r.P)(".list-item")],p.prototype,"listItemRoot",void 0)},37540:function(e,t,i){i.d(t,{Kq:()=>p});var o=i(63937),a=i(42017);const r=(e,t)=>{const i=e._$AN;if(void 0===i)return!1;for(const o of i)o._$AO?.(t,!1),r(o,t);return!0},s=e=>{let t,i;do{if(void 0===(t=e._$AM))break;i=t._$AN,i.delete(e),e=t}while(0===i?.size)},l=e=>{for(let t;t=e._$AM;e=t){let i=t._$AN;if(void 0===i)t._$AN=i=new Set;else if(i.has(e))break;i.add(e),c(t)}};function d(e){void 0!==this._$AN?(s(this),this._$AM=e,l(this)):this._$AM=e}function n(e,t=!1,i=0){const o=this._$AH,a=this._$AN;if(void 0!==a&&0!==a.size)if(t)if(Array.isArray(o))for(let l=i;l<o.length;l++)r(o[l],!1),s(o[l]);else null!=o&&(r(o,!1),s(o));else r(this,e)}const c=e=>{e.type==a.OA.CHILD&&(e._$AP??=n,e._$AQ??=d)};class p extends a.WL{_$AT(e,t,i){super._$AT(e,t,i),l(this),this.isConnected=e._$AU}_$AO(e,t=!0){e!==this.isConnected&&(this.isConnected=e,e?this.reconnected?.():this.disconnected?.()),t&&(r(this,e),s(this))}setValue(e){if((0,o.Rt)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}constructor(){super(...arguments),this._$AN=void 0}}}};
//# sourceMappingURL=5946.b372078c77c60b7e.js.map