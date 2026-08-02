export const __webpack_id__="6162";export const __webpack_ids__=["6162"];export const __webpack_modules__={48833:function(e,t,o){o.d(t,{P:()=>s});var a=o(58109),i=o(70076);const r=["sunday","monday","tuesday","wednesday","thursday","friday","saturday"],s=e=>e.first_weekday===i.zt.language?"weekInfo"in Intl.Locale.prototype?new Intl.Locale(e.language).weekInfo.firstDay%7:(0,a.S)(e.language)%7:r.includes(e.first_weekday)?r.indexOf(e.first_weekday):1},4359:function(e,t,o){o.a(e,async function(e,a){try{o.d(t,{LW:()=>_,Xs:()=>p,fU:()=>d,ie:()=>h});var i=o(22),r=o(22786),s=o(74309),n=o(59006),l=e([i,s]);[i,s]=l.then?(await l)():l;const d=(e,t,o)=>c(t,o.time_zone).format(e),c=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{hour:"numeric",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),h=(e,t,o)=>u(t,o.time_zone).format(e),u=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",second:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),p=(e,t,o)=>v(t,o.time_zone).format(e),v=(0,r.A)((e,t)=>new Intl.DateTimeFormat(e.language,{weekday:"long",hour:(0,n.J)(e)?"numeric":"2-digit",minute:"2-digit",hourCycle:(0,n.J)(e)?"h12":"h23",timeZone:(0,s.w)(e.time_zone,t)})),_=(e,t,o)=>m(t,o.time_zone).format(e),m=(0,r.A)((e,t)=>new Intl.DateTimeFormat("en-GB",{hour:"numeric",minute:"2-digit",hour12:!1,timeZone:(0,s.w)(e.time_zone,t)}));a()}catch(d){a(d)}})},74309:function(e,t,o){o.a(e,async function(e,a){try{o.d(t,{w:()=>d});var i=o(22),r=o(70076),s=e([i]);i=(s.then?(await s)():s)[0];const n=Intl.DateTimeFormat?.().resolvedOptions?.().timeZone,l=n??"UTC",d=(e,t)=>e===r.Wj.local&&n?l:t;a()}catch(n){a(n)}})},59006:function(e,t,o){o.d(t,{J:()=>r});var a=o(22786),i=o(70076);const r=(0,a.A)(e=>{if(e.time_format===i.Hg.language||e.time_format===i.Hg.system){const t=e.time_format===i.Hg.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===i.Hg.am_pm})},34887:function(e,t,o){var a=o(62826),i=o(27680),r=(o(83298),o(59924)),s=o(96196),n=o(77845),l=o(32288),d=o(92542),c=(o(94343),o(78740));class h extends c.h{willUpdate(e){super.willUpdate(e),(e.has("value")||e.has("forceBlankValue"))&&this.forceBlankValue&&this.value&&(this.value="")}constructor(...e){super(...e),this.forceBlankValue=!1}}(0,a.__decorate)([(0,n.MZ)({type:Boolean,attribute:"force-blank-value"})],h.prototype,"forceBlankValue",void 0),h=(0,a.__decorate)([(0,n.EM)("ha-combo-box-textfield")],h);o(60733),o(56768);(0,r.SF)("vaadin-combo-box-item",s.AH`
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
  `);class u extends s.WF{async open(){await this.updateComplete,this._comboBox?.open()}async focus(){await this.updateComplete,await(this._inputElement?.updateComplete),this._inputElement?.focus()}disconnectedCallback(){super.disconnectedCallback(),this._overlayMutationObserver&&(this._overlayMutationObserver.disconnect(),this._overlayMutationObserver=void 0),this._bodyMutationObserver&&(this._bodyMutationObserver.disconnect(),this._bodyMutationObserver=void 0)}get selectedItem(){return this._comboBox.selectedItem}setInputValue(e){this._comboBox.value=e}setTextFieldValue(e){this._inputElement.value=e}render(){return s.qy`
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
        ${(0,i.d)(this.renderer||this._defaultRowRenderer)}
        @opened-changed=${this._openedChanged}
        @filter-changed=${this._filterChanged}
        @value-changed=${this._valueChanged}
        attr-for-value="value"
      >
        <ha-combo-box-textfield
          label=${(0,l.J)(this.label)}
          placeholder=${(0,l.J)(this.placeholder)}
          ?disabled=${this.disabled}
          ?required=${this.required}
          validationMessage=${(0,l.J)(this.validationMessage)}
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
              aria-label=${(0,l.J)(this.hass?.localize("ui.common.clear"))}
              class=${"clear-button "+(this.label?"":"no-label")}
              .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              ?disabled=${this.disabled}
              @click=${this._clearValue}
            ></ha-svg-icon>`:""}
        <ha-svg-icon
          role="button"
          tabindex="-1"
          aria-label=${(0,l.J)(this.label)}
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
        >`:""}_clearValue(e){e.stopPropagation(),(0,d.r)(this,"value-changed",{value:void 0})}_toggleOpen(e){this.opened?(this._comboBox?.close(),e.stopPropagation()):this._comboBox?.inputElement.focus()}_openedChanged(e){e.stopPropagation();const t=e.detail.value;if(setTimeout(()=>{this.opened=t,(0,d.r)(this,"opened-changed",{value:e.detail.value})},0),this.clearInitialValue&&(this.setTextFieldValue(""),t?setTimeout(()=>{this._forceBlankValue=!1},100):this._forceBlankValue=!0),t){const e=document.querySelector("vaadin-combo-box-overlay");e&&this._removeInert(e),this._observeBody()}else this._bodyMutationObserver?.disconnect(),this._bodyMutationObserver=void 0}_observeBody(){"MutationObserver"in window&&!this._bodyMutationObserver&&(this._bodyMutationObserver=new MutationObserver(e=>{e.forEach(e=>{e.addedNodes.forEach(e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&this._removeInert(e)}),e.removedNodes.forEach(e=>{"VAADIN-COMBO-BOX-OVERLAY"===e.nodeName&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0)})})}),this._bodyMutationObserver.observe(document.body,{childList:!0}))}_removeInert(e){if(e.inert)return e.inert=!1,this._overlayMutationObserver?.disconnect(),void(this._overlayMutationObserver=void 0);"MutationObserver"in window&&!this._overlayMutationObserver&&(this._overlayMutationObserver=new MutationObserver(e=>{e.forEach(e=>{if("inert"===e.attributeName){const t=e.target;t.inert&&(this._overlayMutationObserver?.disconnect(),this._overlayMutationObserver=void 0,t.inert=!1)}})}),this._overlayMutationObserver.observe(e,{attributes:!0}))}_filterChanged(e){e.stopPropagation(),(0,d.r)(this,"filter-changed",{value:e.detail.value})}_valueChanged(e){if(e.stopPropagation(),this.allowCustomValue||(this._comboBox._closeOnBlurIsPrevented=!0),!this.opened)return;const t=e.detail.value;t!==this.value&&(0,d.r)(this,"value-changed",{value:t||void 0})}constructor(...e){super(...e),this.invalid=!1,this.icon=!1,this.allowCustomValue=!1,this.itemValuePath="value",this.itemLabelPath="label",this.disabled=!1,this.required=!1,this.opened=!1,this.hideClearIcon=!1,this.clearInitialValue=!1,this._forceBlankValue=!1,this._defaultRowRenderer=e=>s.qy`
    <ha-combo-box-item type="button">
      ${this.itemLabelPath?e[this.itemLabelPath]:e}
    </ha-combo-box-item>
  `}}u.styles=s.AH`
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
  `,(0,a.__decorate)([(0,n.MZ)({attribute:!1})],u.prototype,"hass",void 0),(0,a.__decorate)([(0,n.MZ)()],u.prototype,"label",void 0),(0,a.__decorate)([(0,n.MZ)()],u.prototype,"value",void 0),(0,a.__decorate)([(0,n.MZ)()],u.prototype,"placeholder",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:!1})],u.prototype,"validationMessage",void 0),(0,a.__decorate)([(0,n.MZ)()],u.prototype,"helper",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:"error-message"})],u.prototype,"errorMessage",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean})],u.prototype,"invalid",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean})],u.prototype,"icon",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:!1})],u.prototype,"items",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:!1})],u.prototype,"filteredItems",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:!1})],u.prototype,"dataProvider",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:"allow-custom-value",type:Boolean})],u.prototype,"allowCustomValue",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:"item-value-path"})],u.prototype,"itemValuePath",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:"item-label-path"})],u.prototype,"itemLabelPath",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:"item-id-path"})],u.prototype,"itemIdPath",void 0),(0,a.__decorate)([(0,n.MZ)({attribute:!1})],u.prototype,"renderer",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean})],u.prototype,"disabled",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean})],u.prototype,"required",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean,reflect:!0})],u.prototype,"opened",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean,attribute:"hide-clear-icon"})],u.prototype,"hideClearIcon",void 0),(0,a.__decorate)([(0,n.MZ)({type:Boolean,attribute:"clear-initial-value"})],u.prototype,"clearInitialValue",void 0),(0,a.__decorate)([(0,n.P)("vaadin-combo-box-light",!0)],u.prototype,"_comboBox",void 0),(0,a.__decorate)([(0,n.P)("ha-combo-box-textfield",!0)],u.prototype,"_inputElement",void 0),(0,a.__decorate)([(0,n.wk)({type:Boolean})],u.prototype,"_forceBlankValue",void 0),u=(0,a.__decorate)([(0,n.EM)("ha-combo-box")],u)},88867:function(e,t,o){o.r(t),o.d(t,{HaIconPicker:()=>p});var a=o(62826),i=o(96196),r=o(77845),s=o(22786),n=o(92542),l=o(33978);o(34887),o(22598),o(94343);let d=[],c=!1;const h=async e=>{try{const t=l.y[e].getIconList;if("function"!=typeof t)return[];const o=await t();return o.map(t=>({icon:`${e}:${t.name}`,parts:new Set(t.name.split("-")),keywords:t.keywords??[]}))}catch(t){return console.warn(`Unable to load icon list for ${e} iconset`),[]}},u=e=>i.qy`
  <ha-combo-box-item type="button">
    <ha-icon .icon=${e.icon} slot="start"></ha-icon>
    ${e.icon}
  </ha-combo-box-item>
`;class p extends i.WF{render(){return i.qy`
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
        .renderer=${u}
        icon
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        ${this._value||this.placeholder?i.qy`
              <ha-icon .icon=${this._value||this.placeholder} slot="icon">
              </ha-icon>
            `:i.qy`<slot slot="icon" name="fallback"></slot>`}
      </ha-combo-box>
    `}async _openedChanged(e){e.detail.value&&!c&&(await(async()=>{c=!0;const e=await o.e("3451").then(o.t.bind(o,83174,19));d=e.default.map(e=>({icon:`mdi:${e.name}`,parts:new Set(e.name.split("-")),keywords:e.keywords}));const t=[];Object.keys(l.y).forEach(e=>{t.push(h(e))}),(await Promise.all(t)).forEach(e=>{d.push(...e)})})(),this.requestUpdate())}_valueChanged(e){e.stopPropagation(),this._setValue(e.detail.value)}_setValue(e){this.value=e,(0,n.r)(this,"value-changed",{value:this._value},{bubbles:!1,composed:!1})}get _value(){return this.value||""}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.invalid=!1,this._filterIcons=(0,s.A)((e,t=d)=>{if(!e)return t;const o=[],a=(e,t)=>o.push({icon:e,rank:t});for(const i of t)i.parts.has(e)?a(i.icon,1):i.keywords.includes(e)?a(i.icon,2):i.icon.includes(e)?a(i.icon,3):i.keywords.some(t=>t.includes(e))&&a(i.icon,4);return 0===o.length&&a(e,0),o.sort((e,t)=>e.rank-t.rank)}),this._iconProvider=(e,t)=>{const o=this._filterIcons(e.filter.toLowerCase(),d),a=e.page*e.pageSize,i=a+e.pageSize;t(o.slice(a,i),o.length)}}}p.styles=i.AH`
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
  `,(0,a.__decorate)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)()],p.prototype,"value",void 0),(0,a.__decorate)([(0,r.MZ)()],p.prototype,"label",void 0),(0,a.__decorate)([(0,r.MZ)()],p.prototype,"helper",void 0),(0,a.__decorate)([(0,r.MZ)()],p.prototype,"placeholder",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"error-message"})],p.prototype,"errorMessage",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],p.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],p.prototype,"required",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],p.prototype,"invalid",void 0),p=(0,a.__decorate)([(0,r.EM)("ha-icon-picker")],p)},60649:function(e,t,o){o.a(e,async function(e,a){try{o.r(t);var i=o(62826),r=o(3398),s=o(51030),n=o(29851),l=o(93464),d=o(47342),c=o(63723),h=o(92913),u=o(83309),p=o(96196),v=o(77845),_=o(48833),m=o(4359),b=o(59006),y=o(92542),g=(o(88867),o(78740),o(72550)),f=o(70076),w=o(39396),$=o(59332),x=e([l,n,r,m]);[l,n,r,m]=x.then?(await x)():x;const k={plugins:[l.A,n.Ay],headerToolbar:!1,initialView:"timeGridWeek",editable:!0,selectable:!0,selectMirror:!0,selectOverlap:!1,eventOverlap:!1,allDaySlot:!1,height:"parent",locales:s.A,firstDay:1,dayHeaderFormat:{weekday:"short",month:void 0,day:void 0}};class M extends p.WF{set item(e){this._item=e,e?(this._name=e.name||"",this._icon=e.icon||"",this._monday=e.monday||[],this._tuesday=e.tuesday||[],this._wednesday=e.wednesday||[],this._thursday=e.thursday||[],this._friday=e.friday||[],this._saturday=e.saturday||[],this._sunday=e.sunday||[]):(this._name="",this._icon="",this._monday=[],this._tuesday=[],this._wednesday=[],this._thursday=[],this._friday=[],this._saturday=[],this._sunday=[])}disconnectedCallback(){super.disconnectedCallback(),this.calendar?.destroy(),this.calendar=void 0,this.renderRoot.querySelector("style[data-fullcalendar]")?.remove()}connectedCallback(){super.connectedCallback(),this.hasUpdated&&!this.calendar&&this._setupCalendar()}focus(){this.updateComplete.then(()=>this.shadowRoot?.querySelector("[dialogInitialFocus]")?.focus())}render(){return this.hass?p.qy`
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
        ${this.disabled?p.s6:p.qy`<div id="calendar"></div>`}
      </div>
    `:p.s6}willUpdate(e){if(super.willUpdate(e),!this.calendar)return;(e.has("_sunday")||e.has("_monday")||e.has("_tuesday")||e.has("_wednesday")||e.has("_thursday")||e.has("_friday")||e.has("_saturday")||e.has("calendar"))&&(this.calendar.removeAllEventSources(),this.calendar.addEventSource(this._events));const t=e.get("hass");t&&t.language!==this.hass.language&&this.calendar.setOption("locale",this.hass.language)}firstUpdated(){this.disabled||this._setupCalendar()}_setupCalendar(){const e={...k,locale:this.hass.language,firstDay:(0,_.P)(this.hass.locale),slotLabelFormat:{hour:"numeric",minute:void 0,hour12:(0,b.J)(this.hass.locale),meridiem:!!(0,b.J)(this.hass.locale)&&"narrow"},eventTimeFormat:{hour:(0,b.J)(this.hass.locale)?"numeric":"2-digit",minute:(0,b.J)(this.hass.locale)?"numeric":"2-digit",hour12:(0,b.J)(this.hass.locale),meridiem:!!(0,b.J)(this.hass.locale)&&"narrow"}};e.eventClick=e=>this._handleEventClick(e),e.select=e=>this._handleSelect(e),e.eventResize=e=>this._handleEventResize(e),e.eventDrop=e=>this._handleEventDrop(e),this.calendar=new r.Vv(this.shadowRoot.getElementById("calendar"),e),this.calendar.render()}get _events(){const e=[];for(const[t,o]of g.mx.entries())this[`_${o}`].length&&this[`_${o}`].forEach((a,i)=>{let r=(0,d.s)(new Date,t);(0,c.R)(r,new Date,{weekStartsOn:(0,_.P)(this.hass.locale)})||(r=(0,h.f)(r,-7));const s=new Date(r),n=a.from.split(":");s.setHours(parseInt(n[0]),parseInt(n[1]),0,0);const l=new Date(r),u=a.to.split(":");l.setHours(parseInt(u[0]),parseInt(u[1]),0,0),e.push({id:`${o}-${i}`,start:s.toISOString(),end:l.toISOString()})});return e}_handleSelect(e){const{start:t,end:o}=e,a=g.mx[t.getDay()],i=[...this[`_${a}`]],r={...this._item},s=(0,m.LW)(o,{...this.hass.locale,time_zone:f.Wj.local},this.hass.config);i.push({from:(0,m.LW)(t,{...this.hass.locale,time_zone:f.Wj.local},this.hass.config),to:(0,u.r)(t,o)&&"0:00"!==s?s:"24:00"}),r[a]=i,(0,y.r)(this,"value-changed",{value:r}),(0,u.r)(t,o)||this.calendar.unselect()}_handleEventResize(e){const{id:t,start:o,end:a}=e.event,[i,r]=t.split("-"),s=this[`_${i}`][parseInt(r)],n={...this._item},l=(0,m.LW)(a,this.hass.locale,this.hass.config);n[i][r]={...n[i][r],from:s.from,to:(0,u.r)(o,a)&&"0:00"!==l?l:"24:00"},(0,y.r)(this,"value-changed",{value:n}),(0,u.r)(o,a)||(this.requestUpdate(`_${i}`),e.revert())}_handleEventDrop(e){const{id:t,start:o,end:a}=e.event,[i,r]=t.split("-"),s=g.mx[o.getDay()],n={...this._item},l=(0,m.LW)(a,this.hass.locale,this.hass.config),d={...n[i][r],from:(0,m.LW)(o,this.hass.locale,this.hass.config),to:(0,u.r)(o,a)&&"0:00"!==l?l:"24:00"};if(s===i)n[i][r]=d;else{n[i].splice(r,1);const e=[...this[`_${s}`]];e.push(d),n[s]=e}(0,y.r)(this,"value-changed",{value:n}),(0,u.r)(o,a)||(this.requestUpdate(`_${i}`),e.revert())}async _handleEventClick(e){const[t,o]=e.event.id.split("-"),a=[...this[`_${t}`]][o];(0,$.c)(this,{block:a,updateBlock:e=>this._updateBlock(t,o,e),deleteBlock:()=>this._deleteBlock(t,o)})}_updateBlock(e,t,o){const[a,i,r]=o.from.split(":");o.from=`${a}:${i}`;const[s,n,l]=o.to.split(":");o.to=`${s}:${n}`,0===Number(s)&&0===Number(n)&&(o.to="24:00");const d={...this._item};d[e]=[...this._item[e]],d[e][t]=o,(0,y.r)(this,"value-changed",{value:d})}_deleteBlock(e,t){const o=[...this[`_${e}`]],a={...this._item};o.splice(parseInt(t),1),a[e]=o,(0,y.r)(this,"value-changed",{value:a})}_valueChanged(e){if(!this.new&&!this._item)return;e.stopPropagation();const t=e.target.configValue,o=e.detail?.value||e.target.value;if(this[`_${t}`]===o)return;const a={...this._item};o?a[t]=o:delete a[t],(0,y.r)(this,"value-changed",{value:a})}static get styles(){return[w.RF,p.AH`
        .form {
          color: var(--primary-text-color);
        }

        ha-textfield {
          display: block;
          margin: 8px 0;
        }

        #calendar {
          margin: 8px 0;
          height: 450px;
          width: 100%;
          -webkit-user-select: none;
          -ms-user-select: none;
          user-select: none;
          --fc-border-color: var(--divider-color);
          --fc-event-border-color: var(--divider-color);
        }

        .fc-v-event .fc-event-time {
          white-space: inherit;
        }
        .fc-theme-standard .fc-scrollgrid {
          border: 1px solid var(--divider-color);
          border-radius: var(--mdc-shape-small, 4px);
        }

        .fc-scrollgrid-section-header td {
          border: none;
        }
        :host([narrow]) .fc-scrollgrid-sync-table {
          overflow: hidden;
        }
        table.fc-scrollgrid-sync-table
          tbody
          tr:first-child
          .fc-daygrid-day-top {
          padding-top: 0;
        }
        .fc-scroller::-webkit-scrollbar {
          width: 0.4rem;
          height: 0.4rem;
        }
        .fc-scroller::-webkit-scrollbar-thumb {
          border-radius: var(--ha-border-radius-sm);
          background: var(--scrollbar-thumb-color);
        }
        .fc-scroller {
          overflow-y: auto;
          scrollbar-color: var(--scrollbar-thumb-color) transparent;
          scrollbar-width: thin;
        }

        .fc-timegrid-event-short .fc-event-time:after {
          content: ""; /* prevent trailing dash in half hour events since we do not have event titles */
        }

        a {
          color: inherit !important;
        }

        th.fc-col-header-cell.fc-day {
          background-color: var(--table-header-background-color);
          color: var(--primary-text-color);
          font-size: var(--ha-font-size-xs);
          font-weight: var(--ha-font-weight-bold);
          text-transform: uppercase;
        }
      `]}constructor(...e){super(...e),this.new=!1,this.disabled=!1}}(0,i.__decorate)([(0,v.MZ)({attribute:!1})],M.prototype,"hass",void 0),(0,i.__decorate)([(0,v.MZ)({type:Boolean})],M.prototype,"new",void 0),(0,i.__decorate)([(0,v.MZ)({type:Boolean})],M.prototype,"disabled",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_name",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_icon",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_monday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_tuesday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_wednesday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_thursday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_friday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_saturday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"_sunday",void 0),(0,i.__decorate)([(0,v.wk)()],M.prototype,"calendar",void 0),M=(0,i.__decorate)([(0,v.EM)("ha-schedule-form")],M),a()}catch(k){a(k)}})},59332:function(e,t,o){o.d(t,{c:()=>r});var a=o(92542);const i=()=>o.e("4297").then(o.bind(o,88240)),r=(e,t)=>{(0,a.r)(e,"show-dialog",{dialogTag:"dialog-schedule-block-info",dialogImport:i,dialogParams:t})}}};
//# sourceMappingURL=6162.feac9e6c232b4225.js.map