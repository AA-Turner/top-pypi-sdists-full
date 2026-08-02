export const __webpack_id__="6080";export const __webpack_ids__=["6080"];export const __webpack_modules__={55124:function(e,t,i){i.d(t,{d:()=>o});const o=e=>e.stopPropagation()},74529:function(e,t,i){var o=i(62826),a=i(96229),r=i(26069),s=i(91735),n=i(42034),d=i(96196),l=i(77845);class c extends a.k{renderOutline(){return this.filled?d.qy`<span class="filled"></span>`:super.renderOutline()}getContainerClasses(){return{...super.getContainerClasses(),active:this.active}}renderPrimaryContent(){return d.qy`
      <span class="leading icon" aria-hidden="true">
        ${this.renderLeadingIcon()}
      </span>
      <span class="label">${this.label}</span>
      <span class="touch"></span>
      <span class="trailing leading icon" aria-hidden="true">
        ${this.renderTrailingIcon()}
      </span>
    `}renderTrailingIcon(){return d.qy`<slot name="trailing-icon"></slot>`}constructor(...e){super(...e),this.filled=!1,this.active=!1}}c.styles=[s.R,n.R,r.R,d.AH`
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
    `],(0,o.__decorate)([(0,l.MZ)({type:Boolean,reflect:!0})],c.prototype,"filled",void 0),(0,o.__decorate)([(0,l.MZ)({type:Boolean})],c.prototype,"active",void 0),c=(0,o.__decorate)([(0,l.EM)("ha-assist-chip")],c)},96294:function(e,t,i){var o=i(62826),a=i(4720),r=i(77845);class s extends a.Y{}s=(0,o.__decorate)([(0,r.EM)("ha-chip-set")],s)},25388:function(e,t,i){var o=i(62826),a=i(41216),r=i(78960),s=i(75640),n=i(91735),d=i(43826),l=i(96196),c=i(77845);class h extends a.R{}h.styles=[n.R,d.R,s.R,r.R,l.AH`
      :host {
        --md-sys-color-primary: var(--primary-text-color);
        --md-sys-color-on-surface: var(--primary-text-color);
        --md-sys-color-on-surface-variant: var(--primary-text-color);
        --md-sys-color-on-secondary-container: var(--primary-text-color);
        --md-input-chip-container-shape: 16px;
        --md-input-chip-outline-color: var(--outline-color);
        --md-input-chip-selected-container-color: rgba(
          var(--rgb-primary-text-color),
          0.15
        );
        --ha-input-chip-selected-container-opacity: 1;
        --md-input-chip-label-text-font: Roboto, sans-serif;
      }
      /** Set the size of mdc icons **/
      ::slotted([slot="icon"]) {
        display: flex;
        --mdc-icon-size: var(--md-input-chip-icon-size, 18px);
      }
      .selected::before {
        opacity: var(--ha-input-chip-selected-container-opacity);
      }
    `],h=(0,o.__decorate)([(0,c.EM)("ha-input-chip")],h)},94343:function(e,t,i){var o=i(62826),a=i(96196),r=i(77845),s=i(23897);class n extends s.G{constructor(...e){super(...e),this.borderTop=!1}}n.styles=[...s.J,a.AH`
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
    `],(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"border-top"})],n.prototype,"borderTop",void 0),n=(0,o.__decorate)([(0,r.EM)("ha-combo-box-item")],n)},34887:function(e,t,i){var o=i(62826),a=i(27680),r=(i(83298),i(59924)),s=i(96196),n=i(77845),d=i(32288),l=i(92542),c=(i(94343),i(78740));class h extends c.h{willUpdate(e){super.willUpdate(e),(e.has("value")||e.has("forceBlankValue"))&&this.forceBlankValue&&this.value&&(this.value="")}constructor(...e){super(...e),this.forceBlankValue=!1}}(0,o.__decorate)([(0,n.MZ)({type:Boolean,attribute:"force-blank-value"})],h.prototype,"forceBlankValue",void 0),h=(0,o.__decorate)([(0,n.EM)("ha-combo-box-textfield")],h);i(60733),i(56768);(0,r.SF)("vaadin-combo-box-item",s.AH`
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
  `,(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"label",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"value",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"placeholder",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"validationMessage",void 0),(0,o.__decorate)([(0,n.MZ)()],p.prototype,"helper",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"error-message"})],p.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"invalid",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"icon",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"items",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"filteredItems",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"dataProvider",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"allow-custom-value",type:Boolean})],p.prototype,"allowCustomValue",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"item-value-path"})],p.prototype,"itemValuePath",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"item-label-path"})],p.prototype,"itemLabelPath",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"item-id-path"})],p.prototype,"itemIdPath",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:!1})],p.prototype,"renderer",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],p.prototype,"required",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0})],p.prototype,"opened",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean,attribute:"hide-clear-icon"})],p.prototype,"hideClearIcon",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean,attribute:"clear-initial-value"})],p.prototype,"clearInitialValue",void 0),(0,o.__decorate)([(0,n.P)("vaadin-combo-box-light",!0)],p.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,n.P)("ha-combo-box-textfield",!0)],p.prototype,"_inputElement",void 0),(0,o.__decorate)([(0,n.wk)({type:Boolean})],p.prototype,"_forceBlankValue",void 0),p=(0,o.__decorate)([(0,n.EM)("ha-combo-box")],p)},56768:function(e,t,i){var o=i(62826),a=i(96196),r=i(77845);class s extends a.WF{render(){return a.qy`<slot></slot>`}constructor(...e){super(...e),this.disabled=!1}}s.styles=a.AH`
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
  `,(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],s.prototype,"disabled",void 0),s=(0,o.__decorate)([(0,r.EM)("ha-input-helper-text")],s)},23897:function(e,t,i){i.d(t,{G:()=>l,J:()=>d});var o=i(62826),a=i(97154),r=i(82553),s=i(96196),n=i(77845);i(95591);const d=[r.R,s.AH`
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
  `];class l extends a.n{renderRipple(){return"text"===this.type?s.s6:s.qy`<ha-ripple
      part="ripple"
      for="item"
      ?disabled=${this.disabled&&"link"!==this.type}
    ></ha-ripple>`}}l.styles=d,l=(0,o.__decorate)([(0,n.EM)("ha-md-list-item")],l)},27891:function(e,t,i){i.r(t),i.d(t,{HaSelectorEntityName:()=>y});var o=i(62826),a=i(96196),r=i(77845),s=i(10085),n=(i(1106),i(78648)),d=i(4937),l=i(22786),c=i(55376),h=i(92542),p=i(55124),u=i(87400);i(74529),i(96294),i(25388),i(34887),i(56768),i(63801);const m=e=>a.qy`
  <ha-combo-box-item type="button">
    <span slot="headline">${e.primary}</span>
    ${e.secondary?a.qy`<span slot="supporting-text">${e.secondary}</span>`:a.s6}
  </ha-combo-box-item>
`,b=new Set(["entity","device","area","floor"]),_=new Set(["entity","device","area","floor"]),v=e=>"text"===e.type&&e.text?e.text:`___${e.type}___`;class f extends a.WF{render(){const e=this._items,t=this._getOptions(this.entityId),i=this._validTypes(this.entityId);return a.qy`
      ${this.label?a.qy`<label>${this.label}</label>`:a.s6}
      <div class="container">
        <ha-sortable
          no-style
          @item-moved=${this._moveItem}
          .disabled=${this.disabled}
          handle-selector="button.primary.action"
          filter=".add"
        >
          <ha-chip-set>
            ${(0,d.u)(this._items,e=>e,(e,t)=>{const o=this._formatItem(e),r=i.has(e.type);return a.qy`
                  <ha-input-chip
                    data-idx=${t}
                    @remove=${this._removeItem}
                    @click=${this._editItem}
                    .label=${o}
                    .selected=${!this.disabled}
                    .disabled=${this.disabled}
                    class=${r?"":"invalid"}
                  >
                    <ha-svg-icon
                      slot="icon"
                      .path=${"M21 11H3V9H21V11M21 13H3V15H21V13Z"}
                    ></ha-svg-icon>
                    <span>${o}</span>
                  </ha-input-chip>
                `})}
            ${this.disabled?a.s6:a.qy`
                  <ha-assist-chip
                    @click=${this._addItem}
                    .disabled=${this.disabled}
                    label=${this.hass.localize("ui.components.entity.entity-name-picker.add")}
                    class="add"
                  >
                    <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
                  </ha-assist-chip>
                `}
          </ha-chip-set>
        </ha-sortable>

        <mwc-menu-surface
          .open=${this._opened}
          @closed=${this._onClosed}
          @opened=${this._onOpened}
          @input=${p.d}
          .anchor=${this._container}
        >
          <ha-combo-box
            .hass=${this.hass}
            .value=${""}
            .autofocus=${this.autofocus}
            .disabled=${this.disabled}
            .required=${this.required&&!e.length}
            .items=${t}
            allow-custom-value
            item-id-path="value"
            item-value-path="value"
            item-label-path="field_label"
            .renderer=${m}
            @opened-changed=${this._openedChanged}
            @value-changed=${this._comboBoxValueChanged}
            @filter-changed=${this._filterChanged}
          >
          </ha-combo-box>
        </mwc-menu-surface>
      </div>
      ${this._renderHelper()}
    `}_renderHelper(){return this.helper?a.qy`
          <ha-input-helper-text .disabled=${this.disabled}>
            ${this.helper}
          </ha-input-helper-text>
        `:a.s6}_onClosed(e){e.stopPropagation(),this._opened=!1,this._editIndex=void 0}async _onOpened(e){this._opened&&(e.stopPropagation(),this._opened=!0,await(this._comboBox?.focus()),await(this._comboBox?.open()))}async _addItem(e){e.stopPropagation(),this._opened=!0}async _editItem(e){e.stopPropagation();const t=parseInt(e.currentTarget.dataset.idx,10);this._editIndex=t,this._opened=!0}get _items(){return this._toItems(this.value)}_openedChanged(e){if(e.detail.value){const e=this._comboBox.items||[],t=null!=this._editIndex?this._items[this._editIndex]:void 0,i=t?v(t):"",o=this._filterSelectedOptions(e,i);"text"===t?.type&&t.text&&o.push(this._customNameOption(t.text)),this._comboBox.filteredItems=o,this._comboBox.setInputValue(i)}else this._opened=!1,this._comboBox.setInputValue("")}_filterChanged(e){const t=e.detail.value,i=t?.toLowerCase()||"",o=this._comboBox.items||[],a=null!=this._editIndex?this._items[this._editIndex]:void 0,r=a?v(a):"";let s=this._filterSelectedOptions(o,r);if(!i)return void(this._comboBox.filteredItems=s);const d={keys:["primary","secondary","value"],isCaseSensitive:!1,minMatchCharLength:Math.min(i.length,2),threshold:.2,ignoreDiacritics:!0};s=new n.A(s,d).search(i).map(e=>e.item),s.push(this._customNameOption(t)),this._comboBox.filteredItems=s}async _moveItem(e){e.stopPropagation();const{oldIndex:t,newIndex:i}=e.detail,o=this._items.concat(),a=o.splice(t,1)[0];o.splice(i,0,a),this._setValue(o),await this.updateComplete,this._filterChanged({detail:{value:""}})}async _removeItem(e){e.stopPropagation();const t=[...this._items],i=parseInt(e.target.dataset.idx,10);t.splice(i,1),this._setValue(t),await this.updateComplete,this._filterChanged({detail:{value:""}})}_comboBoxValueChanged(e){e.stopPropagation();const t=e.detail.value;if(this.disabled||""===t)return;const i=(e=>{if(e.startsWith("___")&&e.endsWith("___")){const t=e.slice(3,-3);if(b.has(t))return{type:t}}return{type:"text",text:e}})(t),o=[...this._items];null!=this._editIndex?o[this._editIndex]=i:o.push(i),this._setValue(o)}_setValue(e){const t=this._toValue(e);this.value=t,(0,h.r)(this,"value-changed",{value:t})}constructor(...e){super(...e),this.required=!1,this.disabled=!1,this._opened=!1,this._validTypes=(0,l.A)(e=>{const t=new Set(["text"]);if(!e)return t;const i=this.hass.states[e];if(!i)return t;t.add("entity");const o=(0,u.l)(i,this.hass.entities,this.hass.devices,this.hass.areas,this.hass.floors);return o.device&&t.add("device"),o.area&&t.add("area"),o.floor&&t.add("floor"),t}),this._getOptions=(0,l.A)(e=>{if(!e)return[];const t=this._validTypes(e);return["entity","device","area","floor"].map(i=>{const o=this.hass.states[e],a=t.has(i),r=this.hass.localize(`ui.components.entity.entity-name-picker.types.${i}`);return{primary:r,secondary:(o&&a?this.hass.formatEntityName(o,{type:i}):this.hass.localize(`ui.components.entity.entity-name-picker.types.${i}_missing`))||"-",field_label:r,value:v({type:i})}})}),this._customNameOption=(0,l.A)(e=>({primary:this.hass.localize("ui.components.entity.entity-name-picker.custom_name"),secondary:`"${e}"`,field_label:e,value:v({type:"text",text:e})})),this._formatItem=e=>"text"===e.type?`"${e.text}"`:b.has(e.type)?this.hass.localize(`ui.components.entity.entity-name-picker.types.${e.type}`):e.type,this._toItems=(0,l.A)(e=>"string"==typeof e?""===e?[]:[{type:"text",text:e}]:e?(0,c.e)(e):[]),this._toValue=(0,l.A)(e=>{if(0!==e.length){if(1===e.length){const t=e[0];return"text"===t.type?t.text:t}return e}}),this._filterSelectedOptions=(e,t)=>{const i=this._items,o=new Set(i.filter(e=>_.has(e.type)).map(e=>v(e)));return e.filter(e=>!o.has(e.value)||e.value===t)}}}f.styles=a.AH`
    :host {
      position: relative;
      width: 100%;
    }

    .container {
      position: relative;
      background-color: var(--mdc-text-field-fill-color, whitesmoke);
      border-radius: var(--ha-border-radius-sm);
      border-end-end-radius: var(--ha-border-radius-square);
      border-end-start-radius: var(--ha-border-radius-square);
    }
    .container:after {
      display: block;
      content: "";
      position: absolute;
      pointer-events: none;
      bottom: 0;
      left: 0;
      right: 0;
      height: 1px;
      width: 100%;
      background-color: var(
        --mdc-text-field-idle-line-color,
        rgba(0, 0, 0, 0.42)
      );
      transform:
        height 180ms ease-in-out,
        background-color 180ms ease-in-out;
    }
    :host([disabled]) .container:after {
      background-color: var(
        --mdc-text-field-disabled-line-color,
        rgba(0, 0, 0, 0.42)
      );
    }
    .container:focus-within:after {
      height: 2px;
      background-color: var(--mdc-theme-primary);
    }

    label {
      display: block;
      margin: 0 0 var(--ha-space-2);
    }

    .add {
      order: 1;
    }

    mwc-menu-surface {
      --mdc-menu-min-width: 100%;
    }

    ha-chip-set {
      padding: var(--ha-space-2) var(--ha-space-2);
    }

    .invalid {
      text-decoration: line-through;
    }

    .sortable-fallback {
      display: none;
      opacity: 0;
    }

    .sortable-ghost {
      opacity: 0.4;
    }

    .sortable-drag {
      cursor: grabbing;
    }

    ha-input-helper-text {
      display: block;
      margin: var(--ha-space-2) 0 0;
    }
  `,(0,o.__decorate)([(0,r.MZ)({attribute:!1})],f.prototype,"hass",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:!1})],f.prototype,"entityId",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:!1})],f.prototype,"value",void 0),(0,o.__decorate)([(0,r.MZ)()],f.prototype,"label",void 0),(0,o.__decorate)([(0,r.MZ)()],f.prototype,"helper",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],f.prototype,"required",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0})],f.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.P)(".container",!0)],f.prototype,"_container",void 0),(0,o.__decorate)([(0,r.P)("ha-combo-box",!0)],f.prototype,"_comboBox",void 0),(0,o.__decorate)([(0,r.wk)()],f.prototype,"_opened",void 0),f=(0,o.__decorate)([(0,r.EM)("ha-entity-name-picker")],f);class y extends((0,s.E)(a.WF)){render(){const e=this.value??this.selector.entity_name?.default_name;return a.qy`
      <ha-entity-name-picker
        .hass=${this.hass}
        .entityId=${this.selector.entity_name?.entity_id||this.context?.entity}
        .value=${e}
        .label=${this.label}
        .helper=${this.helper}
        .disabled=${this.disabled}
        .required=${this.required}
      ></ha-entity-name-picker>
    `}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}(0,o.__decorate)([(0,r.MZ)({attribute:!1})],y.prototype,"hass",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:!1})],y.prototype,"selector",void 0),(0,o.__decorate)([(0,r.MZ)()],y.prototype,"value",void 0),(0,o.__decorate)([(0,r.MZ)()],y.prototype,"label",void 0),(0,o.__decorate)([(0,r.MZ)()],y.prototype,"helper",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],y.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],y.prototype,"required",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:!1})],y.prototype,"context",void 0),y=(0,o.__decorate)([(0,r.EM)("ha-selector-entity_name")],y)},63801:function(e,t,i){var o=i(62826),a=i(96196),r=i(77845),s=i(92542);class n extends a.WF{updated(e){e.has("disabled")&&(this.disabled?this._destroySortable():this._createSortable())}disconnectedCallback(){super.disconnectedCallback(),this._shouldBeDestroy=!0,setTimeout(()=>{this._shouldBeDestroy&&(this._destroySortable(),this._shouldBeDestroy=!1)},1)}connectedCallback(){super.connectedCallback(),this._shouldBeDestroy=!1,this.hasUpdated&&!this.disabled&&this._createSortable()}createRenderRoot(){return this}render(){return this.noStyle?a.s6:a.qy`
      <style>
        .sortable-fallback {
          display: none !important;
        }

        .sortable-ghost {
          box-shadow: 0 0 0 2px var(--primary-color);
          background: rgba(var(--rgb-primary-color), 0.25);
          border-radius: var(--ha-border-radius-sm);
          opacity: 0.4;
        }

        .sortable-drag {
          border-radius: var(--ha-border-radius-sm);
          opacity: 1;
          background: var(--card-background-color);
          box-shadow: 0px 4px 8px 3px #00000026;
          cursor: grabbing;
        }
      </style>
    `}async _createSortable(){if(this._sortable)return;const e=this.children[0];if(!e)return;const t=(await Promise.all([i.e("5283"),i.e("1387")]).then(i.bind(i,38214))).default,o={scroll:!0,forceAutoScrollFallback:!0,scrollSpeed:20,animation:150,...this.options,onChoose:this._handleChoose,onStart:this._handleStart,onEnd:this._handleEnd,onUpdate:this._handleUpdate,onAdd:this._handleAdd,onRemove:this._handleRemove};this.draggableSelector&&(o.draggable=this.draggableSelector),this.handleSelector&&(o.handle=this.handleSelector),void 0!==this.invertSwap&&(o.invertSwap=this.invertSwap),this.group&&(o.group=this.group),this.filter&&(o.filter=this.filter),this._sortable=new t(e,o)}_destroySortable(){this._sortable&&(this._sortable.destroy(),this._sortable=void 0)}constructor(...e){super(...e),this.disabled=!1,this.noStyle=!1,this.invertSwap=!1,this.rollback=!0,this._shouldBeDestroy=!1,this._handleUpdate=e=>{(0,s.r)(this,"item-moved",{newIndex:e.newIndex,oldIndex:e.oldIndex})},this._handleAdd=e=>{(0,s.r)(this,"item-added",{index:e.newIndex,data:e.item.sortableData,item:e.item})},this._handleRemove=e=>{(0,s.r)(this,"item-removed",{index:e.oldIndex})},this._handleEnd=async e=>{(0,s.r)(this,"drag-end"),this.rollback&&e.item.placeholder&&(e.item.placeholder.replaceWith(e.item),delete e.item.placeholder)},this._handleStart=()=>{(0,s.r)(this,"drag-start")},this._handleChoose=e=>{this.rollback&&(e.item.placeholder=document.createComment("sort-placeholder"),e.item.after(e.item.placeholder))}}}(0,o.__decorate)([(0,r.MZ)({type:Boolean})],n.prototype,"disabled",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,attribute:"no-style"})],n.prototype,"noStyle",void 0),(0,o.__decorate)([(0,r.MZ)({type:String,attribute:"draggable-selector"})],n.prototype,"draggableSelector",void 0),(0,o.__decorate)([(0,r.MZ)({type:String,attribute:"handle-selector"})],n.prototype,"handleSelector",void 0),(0,o.__decorate)([(0,r.MZ)({type:String,attribute:"filter"})],n.prototype,"filter",void 0),(0,o.__decorate)([(0,r.MZ)({type:String})],n.prototype,"group",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean,attribute:"invert-swap"})],n.prototype,"invertSwap",void 0),(0,o.__decorate)([(0,r.MZ)({attribute:!1})],n.prototype,"options",void 0),(0,o.__decorate)([(0,r.MZ)({type:Boolean})],n.prototype,"rollback",void 0),n=(0,o.__decorate)([(0,r.EM)("ha-sortable")],n)},78740:function(e,t,i){i.d(t,{h:()=>l});var o=i(62826),a=i(68846),r=i(92347),s=i(96196),n=i(77845),d=i(76679);class l extends a.J{updated(e){super.updated(e),(e.has("invalid")||e.has("errorMessage"))&&(this.setCustomValidity(this.invalid?this.errorMessage||this.validationMessage||"Invalid":""),(this.invalid||this.validateOnInitialRender||e.has("invalid")&&void 0!==e.get("invalid"))&&this.reportValidity()),e.has("autocomplete")&&(this.autocomplete?this.formElement.setAttribute("autocomplete",this.autocomplete):this.formElement.removeAttribute("autocomplete")),e.has("autocorrect")&&(!1===this.autocorrect?this.formElement.setAttribute("autocorrect","off"):this.formElement.removeAttribute("autocorrect")),e.has("inputSpellcheck")&&(this.inputSpellcheck?this.formElement.setAttribute("spellcheck",this.inputSpellcheck):this.formElement.removeAttribute("spellcheck"))}renderIcon(e,t=!1){const i=t?"trailing":"leading";return s.qy`
      <span
        class="mdc-text-field__icon mdc-text-field__icon--${i}"
        tabindex=${t?1:-1}
      >
        <slot name="${i}Icon"></slot>
      </span>
    `}constructor(...e){super(...e),this.icon=!1,this.iconTrailing=!1,this.autocorrect=!0}}l.styles=[r.R,s.AH`
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
        `:s.AH``],(0,o.__decorate)([(0,n.MZ)({type:Boolean})],l.prototype,"invalid",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"error-message"})],l.prototype,"errorMessage",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],l.prototype,"icon",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],l.prototype,"iconTrailing",void 0),(0,o.__decorate)([(0,n.MZ)()],l.prototype,"autocomplete",void 0),(0,o.__decorate)([(0,n.MZ)({type:Boolean})],l.prototype,"autocorrect",void 0),(0,o.__decorate)([(0,n.MZ)({attribute:"input-spellcheck"})],l.prototype,"inputSpellcheck",void 0),(0,o.__decorate)([(0,n.P)("input")],l.prototype,"formElement",void 0),l=(0,o.__decorate)([(0,n.EM)("ha-textfield")],l)},10085:function(e,t,i){i.d(t,{E:()=>r});var o=i(62826),a=i(77845);const r=e=>{class t extends e{connectedCallback(){super.connectedCallback(),this._checkSubscribed()}disconnectedCallback(){if(super.disconnectedCallback(),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then(e=>e()):e()}this.__unsubs=void 0}}updated(e){if(super.updated(e),e.has("hass"))this._checkSubscribed();else if(this.hassSubscribeRequiredHostProps)for(const t of e.keys())if(this.hassSubscribeRequiredHostProps.includes(t))return void this._checkSubscribed()}hassSubscribe(){return[]}_checkSubscribed(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&!this.hassSubscribeRequiredHostProps?.some(e=>void 0===this[e])&&(this.__unsubs=this.hassSubscribe())}}return(0,o.__decorate)([(0,a.MZ)({attribute:!1})],t.prototype,"hass",void 0),t}}};
//# sourceMappingURL=6080.4d335667c868bb6a.js.map