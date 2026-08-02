export const __webpack_id__="6568";export const __webpack_ids__=["6568"];export const __webpack_modules__={61974:function(e,t,o){var a={"./ha-icon-prev":["48268","2477"],"./ha-icon-button-toolbar":["48939","3736"],"./ha-alert":["17963"],"./ha-icon-button-toggle":["35150","2851"],"./ha-svg-icon.ts":["60961"],"./ha-alert.ts":["17963"],"./ha-icon":["22598"],"./ha-icon-next.ts":["28608","4329"],"./ha-qr-code.ts":["16618","1343","6247"],"./ha-icon-overflow-menu.ts":["53623","2016","7644"],"./ha-icon-button-toggle.ts":["35150","2851"],"./ha-icon-button-group":["39651","7760"],"./ha-svg-icon":["60961"],"./ha-icon-button-prev":["80263","8076"],"./ha-icon-button.ts":["60733"],"./ha-icon-overflow-menu":["53623","2016","7644"],"./ha-icon-button-arrow-next":["56231","5500"],"./ha-icon-button-prev.ts":["80263","8076"],"./ha-icon-picker":["88867","9291","1955"],"./ha-icon-button-toolbar.ts":["48939","3736"],"./ha-icon-button-arrow-prev.ts":["371"],"./ha-icon-button-next":["29795","9488"],"./ha-icon-next":["28608","4329"],"./ha-icon-picker.ts":["88867","9291","1955"],"./ha-icon-prev.ts":["48268","2477"],"./ha-icon-button-arrow-prev":["371"],"./ha-icon-button-next.ts":["29795","9488"],"./ha-icon.ts":["22598"],"./ha-qr-code":["16618","1343","6247"],"./ha-icon-button":["60733"],"./ha-icon-button-group.ts":["39651","7760"],"./ha-icon-button-arrow-next.ts":["56231","5500"]};function i(e){if(!o.o(a,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=a[e],i=t[0];return Promise.all(t.slice(1).map(o.e)).then(function(){return o(i)})}i.keys=()=>Object.keys(a),i.id=61974,e.exports=i},25115:function(e,t,o){var a={"./flow-preview-generic.ts":["66633","2239","7251","3577","1543","105","4916","8457","4398","5633","2478","3196","1794"],"./flow-preview-template":["71996","2239","7251","3577","1543","105","4916","8457","4398","5633","2478","3196","9149"],"./flow-preview-generic_camera":["93143","2239","7251","3577","1543","105","4916","8457","4398","5633","2478","3196","1628"],"./flow-preview-generic_camera.ts":["93143","2239","7251","3577","1543","105","4916","8457","4398","5633","2478","3196","1628"],"./flow-preview-generic":["66633","2239","7251","3577","1543","105","4916","8457","4398","5633","2478","3196","1794"],"./flow-preview-template.ts":["71996","2239","7251","3577","1543","105","4916","8457","4398","5633","2478","3196","9149"]};function i(e){if(!o.o(a,e))return Promise.resolve().then(function(){var t=new Error("Cannot find module '"+e+"'");throw t.code="MODULE_NOT_FOUND",t});var t=a[e],i=t[0];return Promise.all(t.slice(1).map(o.e)).then(function(){return o(i)})}i.keys=()=>Object.keys(a),i.id=25115,e.exports=i},45817:function(e,t,o){o.d(t,{d:()=>a});const a=(e,t=!0)=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const o=e.composedPath().find(e=>"A"===e.tagName);if(!o||o.target||o.hasAttribute("download")||"external"===o.getAttribute("rel"))return;let a=o.href;if(!a||-1!==a.indexOf("mailto:"))return;const i=window.location,r=i.origin||i.protocol+"//"+i.host;return a.startsWith(r)&&(a=a.slice(r.length),"#"!==a)?(t&&e.preventDefault(),a):void 0}},48774:function(e,t,o){o.d(t,{L:()=>a});const a=(e,t)=>{const o=e.floor_id;return{area:e,floor:(o?t[o]:void 0)||null}}},48565:function(e,t,o){o.d(t,{d:()=>a});const a=e=>{switch(e.language){case"cs":case"de":case"fi":case"fr":case"sk":case"sv":return" ";default:return""}}},53907:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(22786),s=o(92542),l=o(56403),c=o(41144),d=o(47644),p=o(48774),h=o(54110),u=o(74839),m=o(10234),g=o(82160),_=(o(94343),o(96943)),f=(o(60733),o(60961),e([_]));_=(f.then?(await f)():f)[0];const v="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z",w="M20 2H4C2.9 2 2 2.9 2 4V20C2 21.11 2.9 22 4 22H20C21.11 22 22 21.11 22 20V4C22 2.9 21.11 2 20 2M4 6L6 4H10.9L4 10.9V6M4 13.7L13.7 4H18.6L4 18.6V13.7M20 18L18 20H13.1L20 13.1V18M20 10.3L10.3 20H5.4L20 5.4V10.3Z",y="___ADD_NEW___";class b extends i.WF{async open(){await this.updateComplete,await(this._picker?.open())}render(){const e=this.placeholder??this.hass.localize("ui.components.area-picker.area"),t=this._computeValueRenderer(this.hass.areas);return i.qy`
      <ha-generic-picker
        .hass=${this.hass}
        .autofocus=${this.autofocus}
        .label=${this.label}
        .helper=${this.helper}
        .notFoundLabel=${this._notFoundLabel}
        .emptyLabel=${this.hass.localize("ui.components.area-picker.no_areas")}
        .disabled=${this.disabled}
        .required=${this.required}
        .placeholder=${e}
        .value=${this.value}
        .getItems=${this._getItems}
        .getAdditionalItems=${this._getAdditionalItems}
        .valueRenderer=${t}
        .addButtonLabel=${this.addButtonLabel}
        @value-changed=${this._valueChanged}
      >
      </ha-generic-picker>
    `}_valueChanged(e){e.stopPropagation();const t=e.detail.value;if(t){if(t.startsWith(y)){this.hass.loadFragmentTranslation("config");const e=t.substring(y.length);return void(0,g.J)(this,{suggestedName:e,createEntry:async e=>{try{const t=await(0,h.L3)(this.hass,e);this._setValue(t.area_id)}catch(t){(0,m.K$)(this,{title:this.hass.localize("ui.components.area-picker.failed_create_area"),text:t.message})}}})}this._setValue(t)}else this._setValue(void 0)}_setValue(e){this.value=e,(0,s.r)(this,"value-changed",{value:e}),(0,s.r)(this,"change")}constructor(...e){super(...e),this.noAdd=!1,this.disabled=!1,this.required=!1,this._computeValueRenderer=(0,n.A)(e=>e=>{const t=this.hass.areas[e];if(!t)return i.qy`
            <ha-svg-icon slot="start" .path=${w}></ha-svg-icon>
            <span slot="headline">${t}</span>
          `;const{floor:o}=(0,p.L)(t,this.hass.floors),a=t?(0,l.A)(t):void 0,r=o?(0,d.X)(o):void 0,n=t.icon;return i.qy`
          ${n?i.qy`<ha-icon slot="start" .icon=${n}></ha-icon>`:i.qy`<ha-svg-icon
                slot="start"
                .path=${w}
              ></ha-svg-icon>`}
          <span slot="headline">${a}</span>
          ${r?i.qy`<span slot="supporting-text">${r}</span>`:i.s6}
        `}),this._getAreas=(0,n.A)((e,t,o,a,i,r,n,s,h)=>{let m,g,_={};const f=Object.values(e),v=Object.values(t),y=Object.values(o);(a||i||r||n||s)&&(_=(0,u.g2)(y),m=v,g=y.filter(e=>e.area_id),a&&(m=m.filter(e=>{const t=_[e.id];return!(!t||!t.length)&&_[e.id].some(e=>a.includes((0,c.m)(e.entity_id)))}),g=g.filter(e=>a.includes((0,c.m)(e.entity_id)))),i&&(m=m.filter(e=>{const t=_[e.id];return!t||!t.length||y.every(e=>!i.includes((0,c.m)(e.entity_id)))}),g=g.filter(e=>!i.includes((0,c.m)(e.entity_id)))),r&&(m=m.filter(e=>{const t=_[e.id];return!(!t||!t.length)&&_[e.id].some(e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&r.includes(t.attributes.device_class))})}),g=g.filter(e=>{const t=this.hass.states[e.entity_id];return t.attributes.device_class&&r.includes(t.attributes.device_class)})),n&&(m=m.filter(e=>n(e))),s&&(m=m.filter(e=>{const t=_[e.id];return!(!t||!t.length)&&_[e.id].some(e=>{const t=this.hass.states[e.entity_id];return!!t&&s(t)})}),g=g.filter(e=>{const t=this.hass.states[e.entity_id];return!!t&&s(t)})));let b,$=f;m&&(b=m.filter(e=>e.area_id).map(e=>e.area_id)),g&&(b=(b??[]).concat(g.filter(e=>e.area_id).map(e=>e.area_id))),b&&($=$.filter(e=>b.includes(e.area_id))),h&&($=$.filter(e=>!h.includes(e.area_id)));return $.map(e=>{const{floor:t}=(0,p.L)(e,this.hass.floors),o=t?(0,d.X)(t):void 0,a=(0,l.A)(e);return{id:e.area_id,primary:a||e.area_id,secondary:o,icon:e.icon||void 0,icon_path:e.icon?void 0:w,sorting_label:a,search_labels:[a,o,e.area_id,...e.aliases].filter(e=>Boolean(e))}})}),this._getItems=()=>this._getAreas(this.hass.areas,this.hass.devices,this.hass.entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses,this.deviceFilter,this.entityFilter,this.excludeAreas),this._allAreaNames=(0,n.A)(e=>Object.values(e).map(e=>(0,l.A)(e)?.toLowerCase()).filter(Boolean)),this._getAdditionalItems=e=>{if(this.noAdd)return[];const t=this._allAreaNames(this.hass.areas);return e&&!t.includes(e.toLowerCase())?[{id:y+e,primary:this.hass.localize("ui.components.area-picker.add_new_sugestion",{name:e}),icon_path:v}]:[{id:y,primary:this.hass.localize("ui.components.area-picker.add_new"),icon_path:v}]},this._notFoundLabel=e=>this.hass.localize("ui.components.area-picker.no_match",{term:i.qy`<b>‘${e}’</b>`})}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],b.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)()],b.prototype,"label",void 0),(0,a.__decorate)([(0,r.MZ)()],b.prototype,"value",void 0),(0,a.__decorate)([(0,r.MZ)()],b.prototype,"helper",void 0),(0,a.__decorate)([(0,r.MZ)()],b.prototype,"placeholder",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean,attribute:"no-add"})],b.prototype,"noAdd",void 0),(0,a.__decorate)([(0,r.MZ)({type:Array,attribute:"include-domains"})],b.prototype,"includeDomains",void 0),(0,a.__decorate)([(0,r.MZ)({type:Array,attribute:"exclude-domains"})],b.prototype,"excludeDomains",void 0),(0,a.__decorate)([(0,r.MZ)({type:Array,attribute:"include-device-classes"})],b.prototype,"includeDeviceClasses",void 0),(0,a.__decorate)([(0,r.MZ)({type:Array,attribute:"exclude-areas"})],b.prototype,"excludeAreas",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],b.prototype,"deviceFilter",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],b.prototype,"entityFilter",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],b.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],b.prototype,"required",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"add-button-label"})],b.prototype,"addButtonLabel",void 0),(0,a.__decorate)([(0,r.P)("ha-generic-picker")],b.prototype,"_picker",void 0),b=(0,a.__decorate)([(0,r.EM)("ha-area-picker")],b),t()}catch(v){t(v)}})},89473:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(88496),r=o(96196),n=o(77845),s=e([i]);i=(s.then?(await s)():s)[0];class l extends i.A{static get styles(){return[i.A.styles,r.AH`
        :host {
          --wa-form-control-padding-inline: 16px;
          --wa-font-weight-action: var(--ha-font-weight-medium);
          --wa-form-control-border-radius: var(
            --ha-button-border-radius,
            var(--ha-border-radius-pill)
          );

          --wa-form-control-height: var(
            --ha-button-height,
            var(--button-height, 40px)
          );
        }
        .button {
          font-size: var(--ha-font-size-m);
          line-height: 1;

          transition: background-color 0.15s ease-in-out;
          text-wrap: wrap;
        }

        :host([size="small"]) .button {
          --wa-form-control-height: var(
            --ha-button-height,
            var(--button-height, 32px)
          );
          font-size: var(--wa-font-size-s, var(--ha-font-size-m));
          --wa-form-control-padding-inline: 12px;
        }

        :host([variant="brand"]) {
          --button-color-fill-normal-active: var(
            --ha-color-fill-primary-normal-active
          );
          --button-color-fill-normal-hover: var(
            --ha-color-fill-primary-normal-hover
          );
          --button-color-fill-loud-active: var(
            --ha-color-fill-primary-loud-active
          );
          --button-color-fill-loud-hover: var(
            --ha-color-fill-primary-loud-hover
          );
        }

        :host([variant="neutral"]) {
          --button-color-fill-normal-active: var(
            --ha-color-fill-neutral-normal-active
          );
          --button-color-fill-normal-hover: var(
            --ha-color-fill-neutral-normal-hover
          );
          --button-color-fill-loud-active: var(
            --ha-color-fill-neutral-loud-active
          );
          --button-color-fill-loud-hover: var(
            --ha-color-fill-neutral-loud-hover
          );
        }

        :host([variant="success"]) {
          --button-color-fill-normal-active: var(
            --ha-color-fill-success-normal-active
          );
          --button-color-fill-normal-hover: var(
            --ha-color-fill-success-normal-hover
          );
          --button-color-fill-loud-active: var(
            --ha-color-fill-success-loud-active
          );
          --button-color-fill-loud-hover: var(
            --ha-color-fill-success-loud-hover
          );
        }

        :host([variant="warning"]) {
          --button-color-fill-normal-active: var(
            --ha-color-fill-warning-normal-active
          );
          --button-color-fill-normal-hover: var(
            --ha-color-fill-warning-normal-hover
          );
          --button-color-fill-loud-active: var(
            --ha-color-fill-warning-loud-active
          );
          --button-color-fill-loud-hover: var(
            --ha-color-fill-warning-loud-hover
          );
        }

        :host([variant="danger"]) {
          --button-color-fill-normal-active: var(
            --ha-color-fill-danger-normal-active
          );
          --button-color-fill-normal-hover: var(
            --ha-color-fill-danger-normal-hover
          );
          --button-color-fill-loud-active: var(
            --ha-color-fill-danger-loud-active
          );
          --button-color-fill-loud-hover: var(
            --ha-color-fill-danger-loud-hover
          );
        }

        :host([appearance~="plain"]) .button {
          color: var(--wa-color-on-normal);
          background-color: transparent;
        }
        :host([appearance~="plain"]) .button.disabled {
          background-color: transparent;
          color: var(--ha-color-on-disabled-quiet);
        }

        :host([appearance~="outlined"]) .button.disabled {
          background-color: transparent;
          color: var(--ha-color-on-disabled-quiet);
        }

        @media (hover: hover) {
          :host([appearance~="filled"])
            .button:not(.disabled):not(.loading):hover {
            background-color: var(--button-color-fill-normal-hover);
          }
          :host([appearance~="accent"])
            .button:not(.disabled):not(.loading):hover {
            background-color: var(--button-color-fill-loud-hover);
          }
          :host([appearance~="plain"])
            .button:not(.disabled):not(.loading):hover {
            color: var(--wa-color-on-normal);
          }
        }
        :host([appearance~="filled"]) .button {
          color: var(--wa-color-on-normal);
          background-color: var(--wa-color-fill-normal);
          border-color: transparent;
        }
        :host([appearance~="filled"])
          .button:not(.disabled):not(.loading):active {
          background-color: var(--button-color-fill-normal-active);
        }
        :host([appearance~="filled"]) .button.disabled {
          background-color: var(--ha-color-fill-disabled-normal-resting);
          color: var(--ha-color-on-disabled-normal);
        }

        :host([appearance~="accent"]) .button {
          background-color: var(
            --wa-color-fill-loud,
            var(--wa-color-neutral-fill-loud)
          );
        }
        :host([appearance~="accent"])
          .button:not(.disabled):not(.loading):active {
          background-color: var(--button-color-fill-loud-active);
        }
        :host([appearance~="accent"]) .button.disabled {
          background-color: var(--ha-color-fill-disabled-loud-resting);
          color: var(--ha-color-on-disabled-loud);
        }

        :host([loading]) {
          pointer-events: none;
        }

        .button.disabled {
          opacity: 1;
        }

        slot[name="start"]::slotted(*) {
          margin-inline-end: 4px;
        }
        slot[name="end"]::slotted(*) {
          margin-inline-start: 4px;
        }

        .button.has-start {
          padding-inline-start: 8px;
        }
        .button.has-end {
          padding-inline-end: 8px;
        }

        .label {
          overflow: hidden;
          text-overflow: ellipsis;
          padding: var(--ha-space-1) 0;
        }
      `]}constructor(...e){super(...e),this.variant="brand"}}l=(0,a.__decorate)([(0,n.EM)("ha-button")],l),t()}catch(l){t(l)}})},86451:function(e,t,o){var a=o(62826),i=o(96196),r=o(77845);class n extends i.WF{render(){const e=i.qy`<div class="header-title">
      <slot name="title"></slot>
    </div>`,t=i.qy`<div class="header-subtitle">
      <slot name="subtitle"></slot>
    </div>`;return i.qy`
      <header class="header">
        <div class="header-bar">
          <section class="header-navigation-icon">
            <slot name="navigationIcon"></slot>
          </section>
          <section class="header-content">
            ${"above"===this.subtitlePosition?i.qy`${t}${e}`:i.qy`${e}${t}`}
          </section>
          <section class="header-action-items">
            <slot name="actionItems"></slot>
          </section>
        </div>
        <slot></slot>
      </header>
    `}static get styles(){return[i.AH`
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
          align-items: center;
          padding: 0 var(--ha-space-1);
          box-sizing: border-box;
        }
        .header-content {
          flex: 1;
          padding: 10px var(--ha-space-1);
          display: flex;
          flex-direction: column;
          justify-content: center;
          min-height: var(--ha-space-12);
          min-width: 0;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
        .header-title {
          height: var(
            --ha-dialog-header-title-height,
            calc(var(--ha-font-size-xl) + var(--ha-space-1))
          );
          font-size: var(--ha-font-size-xl);
          line-height: var(--ha-line-height-condensed);
          font-weight: var(--ha-font-weight-medium);
          color: var(--ha-dialog-header-title-color, var(--primary-text-color));
        }
        .header-subtitle {
          font-size: var(--ha-font-size-m);
          line-height: var(--ha-line-height-normal);
          color: var(
            --ha-dialog-header-subtitle-color,
            var(--secondary-text-color)
          );
        }
        @media all and (min-width: 450px) and (min-height: 500px) {
          .header-bar {
            padding: 0 var(--ha-space-2);
          }
        }
        .header-navigation-icon {
          flex: none;
          min-width: var(--ha-space-2);
          height: 100%;
          display: flex;
          flex-direction: row;
        }
        .header-action-items {
          flex: none;
          min-width: var(--ha-space-2);
          height: 100%;
          display: flex;
          flex-direction: row;
        }
      `]}constructor(...e){super(...e),this.subtitlePosition="below",this.showBorder=!1}}(0,a.__decorate)([(0,r.MZ)({type:String,attribute:"subtitle-position"})],n.prototype,"subtitlePosition",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean,reflect:!0,attribute:"show-border"})],n.prototype,"showBorder",void 0),n=(0,a.__decorate)([(0,r.EM)("ha-dialog-header")],n)},95637:function(e,t,o){o.d(t,{l:()=>c});var a=o(62826),i=o(30728),r=o(47705),n=o(96196),s=o(77845);o(41742),o(60733);const l=["button","ha-list-item"],c=(e,t)=>n.qy`
  <div class="header_title">
    <ha-icon-button
      .label=${e?.localize("ui.common.close")??"Close"}
      .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
      dialogAction="close"
      class="header_button"
    ></ha-icon-button>
    <span>${t}</span>
  </div>
`;class d extends i.u{scrollToPos(e,t){this.contentElement?.scrollTo(e,t)}renderHeading(){return n.qy`<slot name="heading"> ${super.renderHeading()} </slot>`}firstUpdated(){super.firstUpdated(),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,l].join(", "),this._updateScrolledAttribute(),this.contentElement?.addEventListener("scroll",this._onScroll,{passive:!0})}disconnectedCallback(){super.disconnectedCallback(),this.contentElement.removeEventListener("scroll",this._onScroll)}_updateScrolledAttribute(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}constructor(...e){super(...e),this._onScroll=()=>{this._updateScrolledAttribute()}}}d.styles=[r.R,n.AH`
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
        -webkit-backdrop-filter: var(
          --ha-dialog-scrim-backdrop-filter,
          var(--dialog-backdrop-filter, none)
        );
        backdrop-filter: var(
          --ha-dialog-scrim-backdrop-filter,
          var(--dialog-backdrop-filter, none)
        );
        --mdc-dialog-box-shadow: var(--dialog-box-shadow, none);
        --mdc-typography-headline6-font-weight: var(--ha-font-weight-normal);
        --mdc-typography-headline6-font-size: 1.574rem;
      }
      .mdc-dialog__actions {
        justify-content: var(--justify-action-buttons, flex-end);
        padding: var(--ha-space-3) var(--ha-space-4) var(--ha-space-4)
          var(--ha-space-4);
      }
      .mdc-dialog__actions span:nth-child(1) {
        flex: var(--secondary-action-button-flex, unset);
      }
      .mdc-dialog__actions span:nth-child(2) {
        flex: var(--primary-action-button-flex, unset);
      }
      .mdc-dialog__container {
        align-items: var(--vertical-align-dialog, center);
        padding: var(--dialog-container-padding, var(--ha-space-0));
      }
      .mdc-dialog__title {
        padding: var(--ha-space-4) var(--ha-space-4) var(--ha-space-0)
          var(--ha-space-4);
      }
      .mdc-dialog__title:has(span) {
        padding: var(--ha-space-3) var(--ha-space-3) var(--ha-space-0);
      }
      .mdc-dialog__title::before {
        content: unset;
      }
      .mdc-dialog .mdc-dialog__content {
        position: var(--dialog-content-position, relative);
        padding: var(--dialog-content-padding, var(--ha-space-6));
      }
      :host([hideactions]) .mdc-dialog .mdc-dialog__content {
        padding-bottom: var(--dialog-content-padding, var(--ha-space-6));
      }
      .mdc-dialog .mdc-dialog__surface {
        position: var(--dialog-surface-position, relative);
        top: var(--dialog-surface-top);
        margin-top: var(--dialog-surface-margin-top);
        min-width: var(--mdc-dialog-min-width, auto);
        min-height: var(--mdc-dialog-min-height, auto);
        border-radius: var(
          --ha-dialog-border-radius,
          var(--ha-border-radius-3xl)
        );
        -webkit-backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
        backdrop-filter: var(--ha-dialog-surface-backdrop-filter, none);
        background: var(
          --ha-dialog-surface-background,
          var(--mdc-theme-surface, #fff)
        );
        padding: var(--dialog-surface-padding, var(--ha-space-0));
      }
      :host([flexContent]) .mdc-dialog .mdc-dialog__content {
        display: flex;
        flex-direction: column;
      }

      .header_title {
        display: flex;
        align-items: center;
        direction: var(--direction);
      }
      .header_title span {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        display: block;
        padding-left: var(--ha-space-1);
        padding-right: var(--ha-space-1);
        margin-right: var(--ha-space-3);
        margin-inline-end: var(--ha-space-3);
        margin-inline-start: initial;
      }
      .header_button {
        text-decoration: none;
        color: inherit;
        inset-inline-start: initial;
        inset-inline-end: calc(var(--ha-space-3) * -1);
        direction: var(--direction);
      }
      .dialog-actions {
        inset-inline-start: initial !important;
        inset-inline-end: var(--ha-space-0) !important;
        direction: var(--direction);
      }
    `],d=(0,a.__decorate)([(0,s.EM)("ha-dialog")],d)},23442:function(e,t,o){o.d(t,{$:()=>a});const a=e=>{const t={};return e.forEach(e=>{if(void 0!==e.description?.suggested_value&&null!==e.description?.suggested_value)t[e.name]=e.description.suggested_value;else if("default"in e)t[e.name]=e.default;else if("expandable"===e.type){const o=a(e.schema);(e.required||Object.keys(o).length)&&(t[e.name]=o)}else if(e.required){if("boolean"===e.type)t[e.name]=!1;else if("string"===e.type)t[e.name]="";else if("integer"===e.type)t[e.name]="valueMin"in e?e.valueMin:0;else if("constant"===e.type)t[e.name]=e.value;else if("float"===e.type)t[e.name]=0;else if("select"===e.type){if(e.options.length){const o=e.options[0];t[e.name]=Array.isArray(o)?o[0]:o}}else if("positive_time_period_dict"===e.type)t[e.name]={hours:0,minutes:0,seconds:0};else if("selector"in e){const o=e.selector;if("device"in o)t[e.name]=o.device?.multiple?[]:"";else if("entity"in o)t[e.name]=o.entity?.multiple?[]:"";else if("area"in o)t[e.name]=o.area?.multiple?[]:"";else if("label"in o)t[e.name]=o.label?.multiple?[]:"";else if("boolean"in o)t[e.name]=!1;else if("addon"in o||"attribute"in o||"file"in o||"icon"in o||"template"in o||"text"in o||"theme"in o||"object"in o)t[e.name]="";else if("number"in o)t[e.name]=o.number?.min??0;else if("select"in o){if(o.select?.options.length){const a=o.select.options[0],i="string"==typeof a?a:a.value;t[e.name]=o.select.multiple?[i]:i}}else if("country"in o)o.country?.countries?.length&&(t[e.name]=o.country.countries[0]);else if("language"in o)o.language?.languages?.length&&(t[e.name]=o.language.languages[0]);else if("duration"in o)t[e.name]={hours:0,minutes:0,seconds:0};else if("time"in o)t[e.name]="00:00:00";else if("date"in o||"datetime"in o){const o=(new Date).toISOString().slice(0,10);t[e.name]=`${o}T00:00:00`}else if("color_rgb"in o)t[e.name]=[0,0,0];else if("color_temp"in o)t[e.name]=o.color_temp?.min_mireds??153;else if("action"in o||"trigger"in o||"condition"in o)t[e.name]=[];else if("media"in o||"target"in o)t[e.name]={};else{if(!("state"in o))throw new Error(`Selector ${Object.keys(o)[0]} not supported in initial form data`);t[e.name]=o.state?.multiple?[]:""}}}else;}),t}},28608:function(e,t,o){o.r(t),o.d(t,{HaIconNext:()=>s});var a=o(62826),i=o(77845),r=o(76679),n=o(60961);class s extends n.HaSvgIcon{constructor(...e){super(...e),this.path="rtl"===r.G.document.dir?"M15.41,16.58L10.83,12L15.41,7.41L14,6L8,12L14,18L15.41,16.58Z":"M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z"}}(0,a.__decorate)([(0,i.MZ)()],s.prototype,"path",void 0),s=(0,a.__decorate)([(0,i.EM)("ha-icon-next")],s)},28089:function(e,t,o){var a=o(62826),i=o(96196),r=o(77845),n=o(1420),s=o(30015),l=o.n(s),c=o(92542),d=o(2209);let p;const h=e=>i.qy`${e}`,u=new class{get(e){return this._cache.get(e)}set(e,t){this._cache.set(e,t),this._expiration&&window.setTimeout(()=>this._cache.delete(e),this._expiration)}has(e){return this._cache.has(e)}constructor(e){this._cache=new Map,this._expiration=e}}(1e3),m={reType:/(?<input>(\[!(?<type>caution|important|note|tip|warning)\])(?:\s|\\n)?)/i,typeToHaAlert:{caution:"error",important:"info",note:"info",tip:"success",warning:"warning"}};class g extends i.mN{disconnectedCallback(){if(super.disconnectedCallback(),this.cache){const e=this._computeCacheKey();u.set(e,this.innerHTML)}}createRenderRoot(){return this}update(e){super.update(e),void 0!==this.content&&(this._renderPromise=this._render())}async getUpdateComplete(){return await super.getUpdateComplete(),await this._renderPromise,!0}willUpdate(e){if(!this.innerHTML&&this.cache){const e=this._computeCacheKey();u.has(e)&&((0,i.XX)(h((0,n._)(u.get(e))),this.renderRoot),this._resize())}}_computeCacheKey(){return l()({content:this.content,allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl,breaks:this.breaks})}async _render(){const e=await(async(e,t,a)=>(p||(p=(0,d.LV)(new Worker(new URL(o.p+o.u("5640"),o.b)))),p.renderMarkdown(e,t,a)))(String(this.content),{breaks:this.breaks,gfm:!0},{allowSvg:this.allowSvg,allowDataUrl:this.allowDataUrl});(0,i.XX)(h((0,n._)(e.join(""))),this.renderRoot),this._resize();const t=document.createTreeWalker(this,NodeFilter.SHOW_ELEMENT,null);for(;t.nextNode();){const e=t.currentNode;if(e instanceof HTMLAnchorElement&&e.host!==document.location.host)e.target="_blank",e.rel="noreferrer noopener";else if(e instanceof HTMLImageElement)this.lazyImages&&(e.loading="lazy"),e.addEventListener("load",this._resize);else if(e instanceof HTMLQuoteElement){const o=e.firstElementChild?.firstChild?.textContent&&m.reType.exec(e.firstElementChild.firstChild.textContent);if(o){const{type:a}=o.groups,i=document.createElement("ha-alert");i.alertType=m.typeToHaAlert[a.toLowerCase()],i.append(...Array.from(e.childNodes).map(e=>{const t=Array.from(e.childNodes);if(!this.breaks&&t.length){const e=t[0];e.nodeType===Node.TEXT_NODE&&e.textContent===o.input&&e.textContent?.includes("\n")&&(e.textContent=e.textContent.split("\n").slice(1).join("\n"))}return t}).reduce((e,t)=>e.concat(t),[]).filter(e=>e.textContent&&e.textContent!==o.input)),t.parentNode().replaceChild(i,e)}}else e instanceof HTMLElement&&["ha-alert","ha-qr-code","ha-icon","ha-svg-icon"].includes(e.localName)&&o(61974)(`./${e.localName}`)}}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1,this._renderPromise=Promise.resolve(),this._resize=()=>(0,c.r)(this,"content-resize")}}(0,a.__decorate)([(0,r.MZ)()],g.prototype,"content",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],g.prototype,"allowSvg",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],g.prototype,"allowDataUrl",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"breaks",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],g.prototype,"lazyImages",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],g.prototype,"cache",void 0),g=(0,a.__decorate)([(0,r.EM)("ha-markdown-element")],g);class _ extends i.WF{async getUpdateComplete(){const e=await super.getUpdateComplete();return await(this._markdownElement?.updateComplete),e}render(){return this.content?i.qy`<ha-markdown-element
      .content=${this.content}
      .allowSvg=${this.allowSvg}
      .allowDataUrl=${this.allowDataUrl}
      .breaks=${this.breaks}
      .lazyImages=${this.lazyImages}
      .cache=${this.cache}
    ></ha-markdown-element>`:i.s6}constructor(...e){super(...e),this.allowSvg=!1,this.allowDataUrl=!1,this.breaks=!1,this.lazyImages=!1,this.cache=!1}}_.styles=i.AH`
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
      height: auto;
      width: auto;
      transition: height 0.2s ease-in-out;
    }
    p:first-child > img:first-child {
      vertical-align: top;
    }
    p:first-child > img:last-child {
      vertical-align: top;
    }
    :host > ul,
    :host > ol {
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
    table {
      border-collapse: var(--markdown-table-border-collapse, collapse);
    }
    div:has(> table) {
      overflow: auto;
    }
    th {
      text-align: start;
    }
    td,
    th {
      border-width: var(--markdown-table-border-width, 1px);
      border-style: var(--markdown-table-border-style, solid);
      border-color: var(--markdown-table-border-color, var(--divider-color));
      padding: 0.25em 0.5em;
    }
    blockquote {
      border-left: 4px solid var(--divider-color);
      margin-inline: 0;
      padding-inline: 1em;
    }
  `,(0,a.__decorate)([(0,r.MZ)()],_.prototype,"content",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"allow-svg",type:Boolean})],_.prototype,"allowSvg",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:"allow-data-url",type:Boolean})],_.prototype,"allowDataUrl",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],_.prototype,"breaks",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean,attribute:"lazy-images"})],_.prototype,"lazyImages",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],_.prototype,"cache",void 0),(0,a.__decorate)([(0,r.P)("ha-markdown-element")],_.prototype,"_markdownElement",void 0),_=(0,a.__decorate)([(0,r.EM)("ha-markdown")],_)},64109:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(65686),r=o(96196),n=o(77845),s=e([i]);i=(s.then?(await s)():s)[0];class l extends i.A{updated(e){if(super.updated(e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--ha-progress-ring-size","16px");break;case"small":this.style.setProperty("--ha-progress-ring-size","28px");break;case"medium":this.style.setProperty("--ha-progress-ring-size","48px");break;case"large":this.style.setProperty("--ha-progress-ring-size","68px");break;case void 0:this.style.removeProperty("--ha-progress-ring-size")}}static get styles(){return[i.A.styles,r.AH`
        :host {
          --indicator-color: var(
            --ha-progress-ring-indicator-color,
            var(--primary-color)
          );
          --track-color: var(
            --ha-progress-ring-divider-color,
            var(--divider-color)
          );
          --track-width: 4px;
          --speed: 3.5s;
          --size: var(--ha-progress-ring-size, 48px);
        }
      `]}}(0,a.__decorate)([(0,n.MZ)()],l.prototype,"size",void 0),l=(0,a.__decorate)([(0,n.EM)("ha-progress-ring")],l),t()}catch(l){t(l)}})},89600:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(55262),r=o(96196),n=o(77845),s=e([i]);i=(s.then?(await s)():s)[0];class l extends i.A{updated(e){if(super.updated(e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--ha-spinner-size","16px");break;case"small":this.style.setProperty("--ha-spinner-size","28px");break;case"medium":this.style.setProperty("--ha-spinner-size","48px");break;case"large":this.style.setProperty("--ha-spinner-size","68px");break;case void 0:this.style.removeProperty("--ha-progress-ring-size")}}static get styles(){return[i.A.styles,r.AH`
        :host {
          --indicator-color: var(
            --ha-spinner-indicator-color,
            var(--primary-color)
          );
          --track-color: var(--ha-spinner-divider-color, var(--divider-color));
          --track-width: 4px;
          --speed: 3.5s;
          font-size: var(--ha-spinner-size, 48px);
        }
      `]}}(0,a.__decorate)([(0,n.MZ)()],l.prototype,"size",void 0),l=(0,a.__decorate)([(0,n.EM)("ha-spinner")],l),t()}catch(l){t(l)}})},54110:function(e,t,o){o.d(t,{L3:()=>a,QI:()=>s,bQ:()=>n,gs:()=>i,uG:()=>r});const a=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),i=(e,t,o)=>e.callWS({type:"config/area_registry/update",area_id:t,...o}),r=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),n=e=>{const t={};for(const o of e)o.area_id&&(o.area_id in t||(t[o.area_id]=[]),t[o.area_id].push(o));return t},s=e=>{const t={};for(const o of e)o.area_id&&(o.area_id in t||(t[o.area_id]=[]),t[o.area_id].push(o));return t}},41558:function(e,t,o){o.d(t,{KC:()=>d,Vy:()=>l,ds:()=>r,ew:()=>s,g5:()=>c,tl:()=>n});var a=o(9477),i=o(31136);const r=(e,t,o)=>e.connection.subscribeMessage(o,{type:"assist_satellite/intercept_wake_word",entity_id:t}),n=(e,t)=>e.callWS({type:"assist_satellite/test_connection",entity_id:t}),s=(e,t,o)=>e.callService("assist_satellite","announce",o,{entity_id:t}),l=(e,t)=>e.callWS({type:"assist_satellite/get_configuration",entity_id:t}),c=(e,t,o)=>e.callWS({type:"assist_satellite/set_wake_words",entity_id:t,wake_word_ids:o}),d=e=>e&&e.state!==i.Hh&&(0,a.$)(e,1)},54193:function(e,t,o){o.d(t,{Hg:()=>a,e0:()=>i});const a=e=>e.map(e=>{if("string"!==e.type)return e;switch(e.name){case"username":return{...e,autocomplete:"username",autofocus:!0};case"password":return{...e,autocomplete:"current-password"};case"code":return{...e,autocomplete:"one-time-code",autofocus:!0};default:return e}}),i=(e,t)=>e.callWS({type:"auth/sign_path",path:t})},23608:function(e,t,o){o.d(t,{PN:()=>r,jm:()=>n,sR:()=>s,t1:()=>i,t2:()=>c,yu:()=>l});const a={"HA-Frontend-Base":`${location.protocol}//${location.host}`},i=(e,t,o)=>e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(e.userData?.showAdvanced),entry_id:o},a),r=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,a),n=(e,t,o)=>e.callApi("POST",`config/config_entries/flow/${t}`,o,a),s=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),l=(e,t)=>e.callApi("GET","config/config_entries/flow_handlers"+(t?`?type=${t}`:"")),c=e=>e.sendMessagePromise({type:"config_entries/flow/progress"})},86807:function(e,t,o){o.d(t,{K:()=>i,P:()=>a});const a=(e,t)=>e.subscribeEvents(t,"data_entry_flow_progressed"),i=(e,t)=>e.subscribeEvents(t,"data_entry_flow_progress_update")},31136:function(e,t,o){o.d(t,{HV:()=>r,Hh:()=>i,KF:()=>s,ON:()=>n,g0:()=>d,s7:()=>l});var a=o(99245);const i="unavailable",r="unknown",n="on",s="off",l=[i,r],c=[i,r,s],d=(0,a.g)(l);(0,a.g)(c)},73103:function(e,t,o){o.d(t,{F:()=>r,Q:()=>i});const a=["generic_camera","template"],i=(e,t,o,a,i,r)=>e.connection.subscribeMessage(r,{type:`${t}/start_preview`,flow_id:o,flow_type:a,user_input:i}),r=e=>a.includes(e)?e:"generic"},90313:function(e,t,o){o.a(e,async function(e,a){try{o.r(t);var i=o(62826),r=o(96196),n=o(77845),s=o(22786),l=o(92542),c=(o(95637),o(86451),o(60733),o(86807)),d=o(39396),p=o(62001),h=o(10234),u=o(93056),m=o(64533),g=o(12083),_=o(84398),f=o(19486),v=(o(59395),o(12527)),w=o(35804),y=o(53264),b=o(73042),$=e([u,m,g,_,f,v]);[u,m,g,_,f,v]=$.then?(await $)():$;const k="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z",x="M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z";let z=0;class S extends r.WF{async showDialog(e){this._params=e,this._instance=z++;const t=this._instance;let o;if(e.startFlowHandler){this._loading="loading_flow",this._handler=e.startFlowHandler;try{o=await this._params.flowConfig.createFlow(this.hass,e.startFlowHandler)}catch(a){this.closeDialog();let e=a.message||a.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,h.K$)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}if(t!==this._instance)return}else{if(!e.continueFlowId)return;this._loading="loading_flow";try{o=await e.flowConfig.fetchFlow(this.hass,e.continueFlowId)}catch(a){this.closeDialog();let e=a.message||a.body||"Unknown error";return"string"!=typeof e&&(e=JSON.stringify(e)),void(0,h.K$)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:`${this.hass.localize("ui.panel.config.integrations.config_flow.could_not_load")}: ${e}`})}}t===this._instance&&(this._processStep(o),this._loading=void 0)}closeDialog(){if(!this._params)return;const e=Boolean(this._step&&["create_entry","abort"].includes(this._step.type));!this._step||e||this._params.continueFlowId||this._params.flowConfig.deleteFlow(this.hass,this._step.flow_id),this._step&&this._params.dialogClosedCallback&&this._params.dialogClosedCallback({flowFinished:e,entryId:"result"in this._step?this._step.result?.entry_id:void 0}),this._loading=void 0,this._step=void 0,this._params=void 0,this._handler=void 0,this._unsubDataEntryFlowProgress&&(this._unsubDataEntryFlowProgress(),this._unsubDataEntryFlowProgress=void 0),(0,l.r)(this,"dialog-closed",{dialog:this.localName})}_getDialogTitle(){if(this._loading||!this._step||!this._params)return"";switch(this._step.type){case"form":return this._params.flowConfig.renderShowFormStepHeader(this.hass,this._step);case"abort":return this._params.flowConfig.renderAbortHeader?this._params.flowConfig.renderAbortHeader(this.hass,this._step):this.hass.localize(`component.${this._params.domain??this._step.handler}.title`);case"progress":return this._params.flowConfig.renderShowFormProgressHeader(this.hass,this._step);case"menu":return this._params.flowConfig.renderMenuHeader(this.hass,this._step);case"create_entry":{const e=this._devices(this._params.flowConfig.showDevices,Object.values(this.hass.devices),this._step.result?.entry_id,this._params.carryOverDevices).length;return this.hass.localize("ui.panel.config.integrations.config_flow."+(e?"device_created":"success"),{number:e})}default:return""}}_getDialogSubtitle(){if(this._loading||!this._step||!this._params)return"";switch(this._step.type){case"form":return this._params.flowConfig.renderShowFormStepSubheader?.(this.hass,this._step);case"abort":return this._params.flowConfig.renderAbortSubheader?.(this.hass,this._step);case"progress":return this._params.flowConfig.renderShowFormProgressSubheader?.(this.hass,this._step);case"menu":return this._params.flowConfig.renderMenuSubheader?.(this.hass,this._step);default:return""}}render(){if(!this._params)return r.s6;const e=["form","menu","external","progress","data_entry_flow_progressed"].includes(this._step?.type)&&this._params.manifest?.is_built_in||!!this._params.manifest?.documentation,t=this._getDialogTitle(),o=this._getDialogSubtitle();return r.qy`
      <ha-dialog
        open
        @closed=${this.closeDialog}
        scrimClickAction
        escapeKeyAction
        hideActions
        .heading=${t||!0}
      >
        <ha-dialog-header slot="heading">
          <ha-icon-button
            .label=${this.hass.localize("ui.common.close")}
            .path=${k}
            dialogAction="close"
            slot="navigationIcon"
          ></ha-icon-button>

          <div
            slot="title"
            class="dialog-title${"form"===this._step?.type?" form":""}"
            title=${t}
          >
            ${t}
          </div>

          ${o?r.qy` <div slot="subtitle">${o}</div>`:r.s6}
          ${e&&!this._loading&&this._step?r.qy`
                <a
                  slot="actionItems"
                  class="help"
                  href=${this._params.manifest.is_built_in?(0,p.o)(this.hass,`/integrations/${this._params.manifest.domain}`):this._params.manifest.documentation}
                  target="_blank"
                  rel="noreferrer noopener"
                >
                  <ha-icon-button
                    .label=${this.hass.localize("ui.common.help")}
                    .path=${x}
                  >
                  </ha-icon-button
                ></a>
              `:r.s6}
        </ha-dialog-header>
        <div>
          ${this._loading||null===this._step?r.qy`
                <step-flow-loading
                  .flowConfig=${this._params.flowConfig}
                  .hass=${this.hass}
                  .loadingReason=${this._loading}
                  .handler=${this._handler}
                  .step=${this._step}
                ></step-flow-loading>
              `:void 0===this._step?r.s6:r.qy`
                  ${"form"===this._step.type?r.qy`
                        <step-flow-form
                          narrow
                          .flowConfig=${this._params.flowConfig}
                          .step=${this._step}
                          .hass=${this.hass}
                        ></step-flow-form>
                      `:"external"===this._step.type?r.qy`
                          <step-flow-external
                            .flowConfig=${this._params.flowConfig}
                            .step=${this._step}
                            .hass=${this.hass}
                          ></step-flow-external>
                        `:"abort"===this._step.type?r.qy`
                            <step-flow-abort
                              .params=${this._params}
                              .step=${this._step}
                              .hass=${this.hass}
                              .handler=${this._step.handler}
                              .domain=${this._params.domain??this._step.handler}
                            ></step-flow-abort>
                          `:"progress"===this._step.type?r.qy`
                              <step-flow-progress
                                .flowConfig=${this._params.flowConfig}
                                .step=${this._step}
                                .hass=${this.hass}
                                .progress=${this._progress}
                              ></step-flow-progress>
                            `:"menu"===this._step.type?r.qy`
                                <step-flow-menu
                                  .flowConfig=${this._params.flowConfig}
                                  .step=${this._step}
                                  .hass=${this.hass}
                                ></step-flow-menu>
                              `:r.qy`
                                <step-flow-create-entry
                                  .flowConfig=${this._params.flowConfig}
                                  .step=${this._step}
                                  .hass=${this.hass}
                                  .navigateToResult=${this._params.navigateToResult??!1}
                                  .devices=${this._devices(this._params.flowConfig.showDevices,Object.values(this.hass.devices),this._step.result?.entry_id,this._params.carryOverDevices)}
                                ></step-flow-create-entry>
                              `}
                `}
        </div>
      </ha-dialog>
    `}firstUpdated(e){super.firstUpdated(e),this.addEventListener("flow-update",e=>{const{step:t,stepPromise:o}=e.detail;this._processStep(t||o)})}willUpdate(e){super.willUpdate(e),e.has("_step")&&this._step&&["external","progress"].includes(this._step.type)&&this._subscribeDataEntryFlowProgressed()}async _processStep(e){if(void 0===e)return void this.closeDialog();const t=setTimeout(()=>{this._loading="loading_step"},250);let o;try{o=await e}catch(a){return this.closeDialog(),void(0,h.K$)(this,{title:this.hass.localize("ui.panel.config.integrations.config_flow.error"),text:a?.body?.message})}finally{clearTimeout(t),this._loading=void 0}this._step=void 0,await this.updateComplete,this._step=o,"create_entry"!==o.type&&"abort"!==o.type||!o.next_flow||(this._step=void 0,this._handler=void 0,this._unsubDataEntryFlowProgress&&(this._unsubDataEntryFlowProgress(),this._unsubDataEntryFlowProgress=void 0),"config_flow"===o.next_flow[0]?(0,b.W)(this,{continueFlowId:o.next_flow[1],carryOverDevices:this._devices(this._params.flowConfig.showDevices,Object.values(this.hass.devices),"create_entry"===o.type?o.result?.entry_id:void 0,this._params.carryOverDevices).map(e=>e.id),dialogClosedCallback:this._params.dialogClosedCallback}):"options_flow"===o.next_flow[0]?"create_entry"===o.type&&(0,w.Q)(this,o.result,{continueFlowId:o.next_flow[1],navigateToResult:this._params.navigateToResult,dialogClosedCallback:this._params.dialogClosedCallback}):"config_subentries_flow"===o.next_flow[0]?"create_entry"===o.type&&(0,y.a)(this,o.result,o.next_flow[0],{continueFlowId:o.next_flow[1],navigateToResult:this._params.navigateToResult,dialogClosedCallback:this._params.dialogClosedCallback}):(this.closeDialog(),(0,h.K$)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error",{error:`Unsupported next flow type: ${o.next_flow[0]}`})})))}async _subscribeDataEntryFlowProgressed(){if(this._unsubDataEntryFlowProgress)return;this._progress=void 0;const e=[(0,c.P)(this.hass.connection,e=>{e.data.flow_id===this._step?.flow_id&&(this._processStep(this._params.flowConfig.fetchFlow(this.hass,this._step.flow_id)),this._progress=void 0)}),(0,c.K)(this.hass.connection,e=>{this._progress=Math.ceil(100*e.data.progress)})];this._unsubDataEntryFlowProgress=async()=>{(await Promise.all(e)).map(e=>e())}}static get styles(){return[d.nA,r.AH`
        ha-dialog {
          --dialog-content-padding: 0;
        }
        .dialog-title {
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .dialog-title.form {
          white-space: normal;
        }
        .help {
          color: var(--secondary-text-color);
        }
      `]}constructor(...e){super(...e),this._instance=z,this._devices=(0,s.A)((e,t,o,a)=>e&&o?t.filter(e=>e.config_entries.includes(o)||a?.includes(e.id)):[])}}(0,i.__decorate)([(0,n.MZ)({attribute:!1})],S.prototype,"hass",void 0),(0,i.__decorate)([(0,n.wk)()],S.prototype,"_params",void 0),(0,i.__decorate)([(0,n.wk)()],S.prototype,"_loading",void 0),(0,i.__decorate)([(0,n.wk)()],S.prototype,"_progress",void 0),(0,i.__decorate)([(0,n.wk)()],S.prototype,"_step",void 0),(0,i.__decorate)([(0,n.wk)()],S.prototype,"_handler",void 0),S=(0,i.__decorate)([(0,n.EM)("dialog-data-entry-flow")],S),a()}catch(k){a(k)}})},73042:function(e,t,o){o.d(t,{W:()=>s});var a=o(96196),i=o(23608),r=o(84125),n=o(73347);const s=(e,t)=>(0,n.g)(e,t,{flowType:"config_flow",showDevices:!0,createFlow:async(e,o)=>{const[a]=await Promise.all([(0,i.t1)(e,o,t.entryId),e.loadFragmentTranslation("config"),e.loadBackendTranslation("config",o),e.loadBackendTranslation("selector",o),e.loadBackendTranslation("title",o)]);return a},fetchFlow:async(e,t)=>{const[o]=await Promise.all([(0,i.PN)(e,t),e.loadFragmentTranslation("config")]);return await Promise.all([e.loadBackendTranslation("config",o.handler),e.loadBackendTranslation("selector",o.handler),e.loadBackendTranslation("title",o.handler)]),o},handleFlowStep:i.jm,deleteFlow:i.sR,renderAbortDescription(e,t){const o=e.localize(`component.${t.translation_domain||t.handler}.config.abort.${t.reason}`,t.description_placeholders);return o?a.qy`
            <ha-markdown allow-svg breaks .content=${o}></ha-markdown>
          `:t.reason},renderShowFormStepHeader(e,t){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.title`,t.description_placeholders)||e.localize(`component.${t.handler}.title`)},renderShowFormStepDescription(e,t){const o=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return o?a.qy`
            <ha-markdown
              .allowDataUrl=${"zwave_js"===t.handler}
              allow-svg
              breaks
              .content=${o}
            ></ha-markdown>
          `:""},renderShowFormStepFieldLabel(e,t,o,a){if("expandable"===o.type)return e.localize(`component.${t.handler}.config.step.${t.step_id}.sections.${o.name}.name`,t.description_placeholders);const i=a?.path?.[0]?`sections.${a.path[0]}.`:"";return e.localize(`component.${t.handler}.config.step.${t.step_id}.${i}data.${o.name}`,t.description_placeholders)||o.name},renderShowFormStepFieldHelper(e,t,o,i){if("expandable"===o.type)return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.sections.${o.name}.description`,t.description_placeholders);const r=i?.path?.[0]?`sections.${i.path[0]}.`:"",n=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.${r}data_description.${o.name}`,t.description_placeholders);return n?a.qy`<ha-markdown breaks .content=${n}></ha-markdown>`:""},renderShowFormStepFieldError(e,t,o){return e.localize(`component.${t.translation_domain||t.translation_domain||t.handler}.config.error.${o}`,t.description_placeholders)||o},renderShowFormStepFieldLocalizeValue(e,t,o){return e.localize(`component.${t.handler}.selector.${o}`)},renderShowFormStepSubmitButton(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===t.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(e,t){const o=e.localize(`component.${t.translation_domain||t.handler}.config.${t.step_id}.description`,t.description_placeholders);return a.qy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${o?a.qy`
              <ha-markdown
                allow-svg
                breaks
                .content=${o}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const o=e.localize(`component.${t.translation_domain||t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return a.qy`
        ${o?a.qy`
              <ha-markdown
                allow-svg
                breaks
                .content=${o}
              ></ha-markdown>
            `:a.s6}
      `},renderShowFormProgressHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderShowFormProgressDescription(e,t){const o=e.localize(`component.${t.translation_domain||t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return o?a.qy`
            <ha-markdown allow-svg breaks .content=${o}></ha-markdown>
          `:""},renderMenuHeader(e,t){return e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`)},renderMenuDescription(e,t){const o=e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return o?a.qy`
            <ha-markdown allow-svg breaks .content=${o}></ha-markdown>
          `:""},renderMenuOption(e,t,o){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.menu_options.${o}`,t.description_placeholders)},renderMenuOptionDescription(e,t,o){return e.localize(`component.${t.translation_domain||t.handler}.config.step.${t.step_id}.menu_option_descriptions.${o}`,t.description_placeholders)},renderLoadingDescription(e,t,o,a){if("loading_flow"!==t&&"loading_step"!==t)return"";const i=a?.handler||o;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:i?(0,r.p$)(e.localize,i):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},35804:function(e,t,o){o.d(t,{Q:()=>d});var a=o(96196),i=o(84125);const r=(e,t)=>e.callApi("POST","config/config_entries/options/flow",{handler:t,show_advanced_options:Boolean(e.userData?.showAdvanced)}),n=(e,t)=>e.callApi("GET",`config/config_entries/options/flow/${t}`),s=(e,t,o)=>e.callApi("POST",`config/config_entries/options/flow/${t}`,o),l=(e,t)=>e.callApi("DELETE",`config/config_entries/options/flow/${t}`);var c=o(73347);const d=(e,t,o)=>(0,c.g)(e,{startFlowHandler:t.entry_id,domain:t.domain,...o},{flowType:"options_flow",showDevices:!1,createFlow:async(e,o)=>{const[a]=await Promise.all([r(e,o),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",t.domain),e.loadBackendTranslation("selector",t.domain)]);return a},fetchFlow:async(e,o)=>{const[a]=await Promise.all([n(e,o),e.loadFragmentTranslation("config"),e.loadBackendTranslation("options",t.domain),e.loadBackendTranslation("selector",t.domain)]);return a},handleFlowStep:s,deleteFlow:l,renderAbortDescription(e,o){const i=e.localize(`component.${o.translation_domain||t.domain}.options.abort.${o.reason}`,o.description_placeholders);return i?a.qy`
              <ha-markdown
                breaks
                allow-svg
                .content=${i}
              ></ha-markdown>
            `:o.reason},renderShowFormStepHeader(e,o){return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.title`,o.description_placeholders)||e.localize("ui.dialogs.options_flow.form.header")},renderShowFormStepDescription(e,o){const i=e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.description`,o.description_placeholders);return i?a.qy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""},renderShowFormStepFieldLabel(e,o,a,i){if("expandable"===a.type)return e.localize(`component.${t.domain}.options.step.${o.step_id}.sections.${a.name}.name`,o.description_placeholders);const r=i?.path?.[0]?`sections.${i.path[0]}.`:"";return e.localize(`component.${t.domain}.options.step.${o.step_id}.${r}data.${a.name}`,o.description_placeholders)||a.name},renderShowFormStepFieldHelper(e,o,i,r){if("expandable"===i.type)return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.sections.${i.name}.description`,o.description_placeholders);const n=r?.path?.[0]?`sections.${r.path[0]}.`:"",s=e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.${n}data_description.${i.name}`,o.description_placeholders);return s?a.qy`<ha-markdown breaks .content=${s}></ha-markdown>`:""},renderShowFormStepFieldError(e,o,a){return e.localize(`component.${o.translation_domain||t.domain}.options.error.${a}`,o.description_placeholders)||a},renderShowFormStepFieldLocalizeValue(e,o,a){return e.localize(`component.${t.domain}.selector.${a}`)},renderShowFormStepSubmitButton(e,o){return e.localize(`component.${t.domain}.options.step.${o.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===o.last_step?"next":"submit"))},renderExternalStepHeader(e,t){return""},renderExternalStepDescription(e,t){return""},renderCreateEntryDescription(e,t){return a.qy`
          <p>${e.localize("ui.dialogs.options_flow.success.description")}</p>
        `},renderShowFormProgressHeader(e,o){return e.localize(`component.${t.domain}.options.step.${o.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderShowFormProgressDescription(e,o){const i=e.localize(`component.${o.translation_domain||t.domain}.options.progress.${o.progress_action}`,o.description_placeholders);return i?a.qy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""},renderMenuHeader(e,o){return e.localize(`component.${t.domain}.options.step.${o.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderMenuDescription(e,o){const i=e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.description`,o.description_placeholders);return i?a.qy`
              <ha-markdown
                allow-svg
                breaks
                .content=${i}
              ></ha-markdown>
            `:""},renderMenuOption(e,o,a){return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.menu_options.${a}`,o.description_placeholders)},renderMenuOptionDescription(e,o,a){return e.localize(`component.${o.translation_domain||t.domain}.options.step.${o.step_id}.menu_option_descriptions.${a}`,o.description_placeholders)},renderLoadingDescription(e,o){return e.localize(`component.${t.domain}.options.loading`)||("loading_flow"===o||"loading_step"===o?e.localize(`ui.dialogs.options_flow.loading.${o}`,{integration:(0,i.p$)(e.localize,t.domain)}):"")}})},53264:function(e,t,o){o.d(t,{a:()=>d});var a=o(96196),i=o(84125);const r={"HA-Frontend-Base":`${location.protocol}//${location.host}`},n=(e,t,o,a)=>e.callApi("POST","config/config_entries/subentries/flow",{handler:[t,o],show_advanced_options:Boolean(e.userData?.showAdvanced),subentry_id:a},r),s=(e,t,o)=>e.callApi("POST",`config/config_entries/subentries/flow/${t}`,o,r),l=(e,t)=>e.callApi("DELETE",`config/config_entries/subentries/flow/${t}`);var c=o(73347);const d=(e,t,o,d)=>(0,c.g)(e,d,{flowType:"config_subentries_flow",showDevices:!0,createFlow:async(e,a)=>{const[i]=await Promise.all([n(e,a,o,d.subEntryId),e.loadFragmentTranslation("config"),e.loadBackendTranslation("config_subentries",t.domain),e.loadBackendTranslation("selector",t.domain),e.loadBackendTranslation("title",t.domain)]);return i},fetchFlow:async(e,o)=>{const a=await((e,t)=>e.callApi("GET",`config/config_entries/subentries/flow/${t}`,void 0,r))(e,o);return await e.loadFragmentTranslation("config"),await e.loadBackendTranslation("config_subentries",t.domain),await e.loadBackendTranslation("selector",t.domain),a},handleFlowStep:s,deleteFlow:l,renderAbortDescription(e,i){const r=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.abort.${i.reason}`,i.description_placeholders);return r?a.qy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:i.reason},renderShowFormStepHeader(e,a){return e.localize(`component.${a.translation_domain||t.domain}.config_subentries.${o}.step.${a.step_id}.title`,a.description_placeholders)||e.localize(`component.${t.domain}.title`)},renderShowFormStepDescription(e,i){const r=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.step.${i.step_id}.description`,i.description_placeholders);return r?a.qy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepFieldLabel(e,a,i,r){if("expandable"===i.type)return e.localize(`component.${t.domain}.config_subentries.${o}.step.${a.step_id}.sections.${i.name}.name`,a.description_placeholders);const n=r?.path?.[0]?`sections.${r.path[0]}.`:"";return e.localize(`component.${t.domain}.config_subentries.${o}.step.${a.step_id}.${n}data.${i.name}`,a.description_placeholders)||i.name},renderShowFormStepFieldHelper(e,i,r,n){if("expandable"===r.type)return e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.step.${i.step_id}.sections.${r.name}.description`,i.description_placeholders);const s=n?.path?.[0]?`sections.${n.path[0]}.`:"",l=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.step.${i.step_id}.${s}data_description.${r.name}`,i.description_placeholders);return l?a.qy`<ha-markdown breaks .content=${l}></ha-markdown>`:""},renderShowFormStepFieldError(e,a,i){return e.localize(`component.${a.translation_domain||a.translation_domain||t.domain}.config_subentries.${o}.error.${i}`,a.description_placeholders)||i},renderShowFormStepFieldLocalizeValue(e,o,a){return e.localize(`component.${t.domain}.selector.${a}`)},renderShowFormStepSubmitButton(e,a){return e.localize(`component.${t.domain}.config_subentries.${o}.step.${a.step_id}.submit`)||e.localize("ui.panel.config.integrations.config_flow."+(!1===a.last_step?"next":"submit"))},renderExternalStepHeader(e,a){return e.localize(`component.${t.domain}.config_subentries.${o}.step.${a.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site")},renderExternalStepDescription(e,i){const r=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.step.${i.step_id}.description`,i.description_placeholders);return a.qy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${r?a.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,i){const r=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.create_entry.${i.description||"default"}`,i.description_placeholders);return a.qy`
        ${r?a.qy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:a.s6}
      `},renderShowFormProgressHeader(e,a){return e.localize(`component.${t.domain}.config_subentries.${o}.step.${a.step_id}.title`)||e.localize(`component.${t.domain}.title`)},renderShowFormProgressDescription(e,i){const r=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.progress.${i.progress_action}`,i.description_placeholders);return r?a.qy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderMenuHeader(e,a){return e.localize(`component.${t.domain}.config_subentries.${o}.step.${a.step_id}.title`,a.description_placeholders)||e.localize(`component.${t.domain}.title`)},renderMenuDescription(e,i){const r=e.localize(`component.${i.translation_domain||t.domain}.config_subentries.${o}.step.${i.step_id}.description`,i.description_placeholders);return r?a.qy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderMenuOption(e,a,i){return e.localize(`component.${a.translation_domain||t.domain}.config_subentries.${o}.step.${a.step_id}.menu_options.${i}`,a.description_placeholders)},renderMenuOptionDescription(e,a,i){return e.localize(`component.${a.translation_domain||t.domain}.config_subentries.${o}.step.${a.step_id}.menu_option_descriptions.${i}`,a.description_placeholders)},renderLoadingDescription(e,t,o,a){if("loading_flow"!==t&&"loading_step"!==t)return"";const r=a?.handler||o;return e.localize(`ui.panel.config.integrations.config_flow.loading.${t}`,{integration:r?(0,i.p$)(e.localize,r):e.localize("ui.panel.config.integrations.config_flow.loading.fallback_title")})}})},93056:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(92542),s=o(78778),l=o(73042),c=o(97854),d=o(89473),p=e([d]);d=(p.then?(await p)():p)[0];class h extends i.WF{firstUpdated(e){super.firstUpdated(e),"missing_credentials"===this.step.reason&&this._handleMissingCreds()}render(){return"missing_credentials"===this.step.reason?i.s6:i.qy`
      <div class="content">
        ${this.params.flowConfig.renderAbortDescription(this.hass,this.step)}
      </div>
      <div class="buttons">
        <ha-button appearance="plain" @click=${this._flowDone}
          >${this.hass.localize("ui.panel.config.integrations.config_flow.close")}</ha-button
        >
      </div>
    `}async _handleMissingCreds(){(0,s.a)(this.params.dialogParentElement,{selectedDomain:this.domain,manifest:this.params.manifest,applicationCredentialAddedCallback:()=>{(0,l.W)(this.params.dialogParentElement,{dialogClosedCallback:this.params.dialogClosedCallback,startFlowHandler:this.handler,showAdvanced:this.hass.userData?.showAdvanced,navigateToResult:this.params.navigateToResult})}}),this._flowDone()}_flowDone(){(0,n.r)(this,"flow-update",{step:void 0})}static get styles(){return c.G}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"params",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"step",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"domain",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],h.prototype,"handler",void 0),h=(0,a.__decorate)([(0,r.EM)("step-flow-abort")],h),t()}catch(h){t(h)}})},64533:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(22786),s=o(92542),l=o(16727),c=o(41144),d=o(5871),p=o(53907),h=o(89473),u=o(41558),m=o(74839),g=o(22800),_=o(84125),f=o(76681),v=o(10234),w=o(6358),y=o(97854),b=o(3950),$=e([p,h]);[p,h]=$.then?(await $)():$;class k extends i.WF{firstUpdated(e){super.firstUpdated(e),this._loadDomains()}willUpdate(e){if(!e.has("devices")&&!e.has("hass"))return;if(1!==this.devices.length||this.devices[0].primary_config_entry!==this.step.result?.entry_id||"voip"===this.step.result.domain)return;const t=this._deviceEntities(this.devices[0].id,Object.values(this.hass.entities),"assist_satellite");t.length&&t.some(e=>(0,u.KC)(this.hass.states[e.entity_id]))&&(this.navigateToResult=!1,this._flowDone(),(0,w.L)(this,{deviceId:this.devices[0].id}))}render(){const e=this.hass.localize,t=this.step.result?{...this._domains,[this.step.result.entry_id]:this.step.result.domain}:this._domains;return i.qy`
      <div class="content">
        ${this.flowConfig.renderCreateEntryDescription(this.hass,this.step)}
        ${"not_loaded"===this.step.result?.state?i.qy`<span class="error"
              >${e("ui.panel.config.integrations.config_flow.not_loaded")}</span
            >`:i.s6}
        ${0===this.devices.length&&["options_flow","repair_flow"].includes(this.flowConfig.flowType)?i.s6:0===this.devices.length?i.qy`<p>
                ${e("ui.panel.config.integrations.config_flow.created_config",{name:this.step.title})}
              </p>`:i.qy`
                <div class="devices">
                  ${this.devices.map(o=>i.qy`
                      <div class="device">
                        <div class="device-info">
                          ${o.primary_config_entry&&t[o.primary_config_entry]?i.qy`<img
                                slot="graphic"
                                alt=${(0,_.p$)(this.hass.localize,t[o.primary_config_entry])}
                                src=${(0,f.MR)({domain:t[o.primary_config_entry],type:"icon",darkOptimized:this.hass.themes?.darkMode})}
                                crossorigin="anonymous"
                                referrerpolicy="no-referrer"
                              />`:i.s6}
                          <div class="device-info-details">
                            <span>${o.model||o.manufacturer}</span>
                            ${o.model?i.qy`<span class="secondary">
                                  ${o.manufacturer}
                                </span>`:i.s6}
                          </div>
                        </div>
                        <ha-textfield
                          .label=${e("ui.panel.config.integrations.config_flow.device_name")}
                          .placeholder=${(0,l.T)(o,this.hass)}
                          .value=${this._deviceUpdate[o.id]?.name??(0,l.xn)(o)}
                          @change=${this._deviceNameChanged}
                          .device=${o.id}
                        ></ha-textfield>
                        <ha-area-picker
                          .hass=${this.hass}
                          .device=${o.id}
                          .value=${this._deviceUpdate[o.id]?.area??o.area_id??void 0}
                          @value-changed=${this._areaPicked}
                        ></ha-area-picker>
                      </div>
                    `)}
                </div>
              `}
      </div>
      <div class="buttons">
        <ha-button @click=${this._flowDone}
          >${e("ui.panel.config.integrations.config_flow."+(!this.devices.length||Object.keys(this._deviceUpdate).length?"finish":"finish_skip"))}</ha-button
        >
      </div>
    `}async _loadDomains(){const e=await(0,b.VN)(this.hass);this._domains=Object.fromEntries(e.map(e=>[e.entry_id,e.domain]))}async _flowDone(){if(Object.keys(this._deviceUpdate).length){const e=[],t=Object.entries(this._deviceUpdate).map(([t,o])=>(o.name&&e.push(t),(0,m.FB)(this.hass,t,{name_by_user:o.name,area_id:o.area}).catch(e=>{(0,v.K$)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_device",{error:e.message})})})));await Promise.allSettled(t);const o=[],a=[];e.forEach(e=>{const t=this._deviceEntities(e,Object.values(this.hass.entities));a.push(...t.map(e=>e.entity_id))});const i=await(0,g.BM)(this.hass,a);Object.entries(i).forEach(([e,t])=>{t&&o.push((0,g.G_)(this.hass,e,{new_entity_id:t}).catch(e=>(0,v.K$)(this,{text:this.hass.localize("ui.panel.config.integrations.config_flow.error_saving_entity",{error:e.message})})))}),await Promise.allSettled(o)}(0,s.r)(this,"flow-update",{step:void 0}),this.step.result&&this.navigateToResult&&(1===this.devices.length?(0,d.o)(`/config/devices/device/${this.devices[0].id}`):(0,d.o)(`/config/integrations/integration/${this.step.result.domain}#config_entry=${this.step.result.entry_id}`))}async _areaPicked(e){const t=e.currentTarget.device,o=e.detail.value;t in this._deviceUpdate||(this._deviceUpdate[t]={}),this._deviceUpdate[t].area=o,this.requestUpdate("_deviceUpdate")}_deviceNameChanged(e){const t=e.currentTarget,o=t.device,a=t.value;o in this._deviceUpdate||(this._deviceUpdate[o]={}),this._deviceUpdate[o].name=a,this.requestUpdate("_deviceUpdate")}static get styles(){return[y.G,i.AH`
        .devices {
          display: flex;
          margin: -4px;
          max-height: 600px;
          overflow-y: auto;
          flex-direction: column;
        }
        @media all and (max-width: 450px), all and (max-height: 500px) {
          .devices {
            /* header - margin content - footer */
            max-height: calc(100vh - 52px - 20px - 52px);
          }
        }
        .device {
          border: 1px solid var(--divider-color);
          padding: 6px;
          border-radius: var(--ha-border-radius-sm);
          margin: 4px;
          display: inline-block;
        }
        .device-info {
          display: flex;
          align-items: center;
          gap: var(--ha-space-2);
        }
        .device-info img {
          width: 40px;
          height: 40px;
        }
        .device-info-details {
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .secondary {
          color: var(--secondary-text-color);
        }
        ha-textfield,
        ha-area-picker {
          display: block;
        }
        ha-textfield {
          margin: 8px 0;
        }
        .buttons > *:last-child {
          margin-left: auto;
          margin-inline-start: auto;
          margin-inline-end: initial;
        }
        .error {
          color: var(--error-color);
        }
      `]}constructor(...e){super(...e),this._domains={},this.navigateToResult=!1,this._deviceUpdate={},this._deviceEntities=(0,n.A)((e,t,o)=>t.filter(t=>t.device_id===e&&(!o||(0,c.m)(t.entity_id)===o)))}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"flowConfig",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"step",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],k.prototype,"devices",void 0),(0,a.__decorate)([(0,r.wk)()],k.prototype,"_deviceUpdate",void 0),k=(0,a.__decorate)([(0,r.EM)("step-flow-create-entry")],k),t()}catch(k){t(k)}})},12083:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(97854),s=o(89473),l=e([s]);s=(l.then?(await l)():l)[0];class c extends i.WF{render(){const e=this.hass.localize;return i.qy`
      <div class="content">
        ${this.flowConfig.renderExternalStepDescription(this.hass,this.step)}
        <div class="open-button">
          <ha-button href=${this.step.url} target="_blank" rel="noreferrer">
            ${e("ui.panel.config.integrations.config_flow.external_step.open_site")}
          </ha-button>
        </div>
      </div>
    `}firstUpdated(e){super.firstUpdated(e),window.open(this.step.url)}static get styles(){return[n.G,i.AH`
        .open-button {
          text-align: center;
          padding: 24px 0;
        }
        .open-button a {
          text-decoration: none;
        }
      `]}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],c.prototype,"flowConfig",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],c.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],c.prototype,"step",void 0),c=(0,a.__decorate)([(0,r.EM)("step-flow-external")],c),t()}catch(c){t(c)}})},84398:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(22786),s=o(51757),l=o(92542),c=o(45817),d=o(89473),p=(o(17963),o(23442)),h=(o(91120),o(28089),o(89600)),u=o(54193),m=o(73103),g=o(39396),_=o(97854),f=e([d,h]);[d,h]=f.then?(await f)():f;class v extends i.WF{disconnectedCallback(){super.disconnectedCallback(),this.removeEventListener("keydown",this._handleKeyDown)}render(){const e=this.step,t=this._stepDataProcessed;return i.qy`
      <div class="content" @click=${this._clickHandler}>
        ${this.flowConfig.renderShowFormStepDescription(this.hass,this.step)}
        ${this._errorMsg?i.qy`<ha-alert alert-type="error">${this._errorMsg}</ha-alert>`:""}
        <ha-form
          .hass=${this.hass}
          .narrow=${this.narrow}
          .data=${t}
          .disabled=${this._loading}
          @value-changed=${this._stepDataChanged}
          .schema=${(0,u.Hg)(this.handleReadOnlyFields(e.data_schema))}
          .error=${this._errors}
          .computeLabel=${this._labelCallback}
          .computeHelper=${this._helperCallback}
          .computeError=${this._errorCallback}
          .localizeValue=${this._localizeValueCallback}
        ></ha-form>
      </div>
      ${e.preview?i.qy`<div class="preview" @set-flow-errors=${this._setError}>
            <h3>
              ${this.hass.localize("ui.panel.config.integrations.config_flow.preview")}:
            </h3>
            ${(0,s._)(`flow-preview-${(0,m.F)(e.preview)}`,{hass:this.hass,domain:e.preview,flowType:this.flowConfig.flowType,handler:e.handler,stepId:e.step_id,flowId:e.flow_id,stepData:t})}
          </div>`:i.s6}
      <div class="buttons">
        <ha-button @click=${this._submitStep} .loading=${this._loading}>
          ${this.flowConfig.renderShowFormStepSubmitButton(this.hass,this.step)}
        </ha-button>
      </div>
    `}_setError(e){this._previewErrors=e.detail}firstUpdated(e){super.firstUpdated(e),setTimeout(()=>this.shadowRoot.querySelector("ha-form").focus(),0),this.addEventListener("keydown",this._handleKeyDown)}willUpdate(e){super.willUpdate(e),e.has("step")&&this.step?.preview&&o(25115)(`./flow-preview-${(0,m.F)(this.step.preview)}`),(e.has("step")||e.has("_previewErrors")||e.has("_submitErrors"))&&(this._errors=this.step.errors||this._previewErrors||this._submitErrors?{...this.step.errors,...this._previewErrors,...this._submitErrors}:void 0)}_clickHandler(e){(0,c.d)(e,!1)&&(0,l.r)(this,"flow-update",{step:void 0})}get _stepDataProcessed(){return void 0!==this._stepData||(this._stepData=(0,p.$)(this.step.data_schema)),this._stepData}async _submitStep(){const e=this._stepData||{},t=(e,o)=>e.every(e=>(!e.required||!["",void 0].includes(o[e.name]))&&("expandable"!==e.type||!e.required&&void 0===o[e.name]||t(e.schema,o[e.name])));if(!(void 0===e?void 0===this.step.data_schema.find(e=>e.required):t(this.step.data_schema,e)))return void(this._errorMsg=this.hass.localize("ui.panel.config.integrations.config_flow.not_all_required_fields"));this._loading=!0,this._errorMsg=void 0,this._submitErrors=void 0;const o=this.step.flow_id,a={};Object.keys(e).forEach(t=>{const o=e[t],i=[void 0,""].includes(o),r=this.step.data_schema?.find(e=>e.name===t),n=r?.selector??{},s=Object.values(n)[0]?.read_only;i||s||(a[t]=o)});try{const e=await this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,a);if(!this.step||o!==this.step.flow_id)return;this._previewErrors=void 0,(0,l.r)(this,"flow-update",{step:e})}catch(i){i&&i.body?(i.body.message&&(this._errorMsg=i.body.message),i.body.errors&&(this._submitErrors=i.body.errors),i.body.message||i.body.errors||(this._errorMsg="Unknown error occurred")):this._errorMsg="Unknown error occurred"}finally{this._loading=!1}}_stepDataChanged(e){this._stepData=e.detail.value}static get styles(){return[g.RF,_.G,i.AH`
        .error {
          color: red;
        }

        ha-alert,
        ha-form {
          margin-top: 24px;
          display: block;
        }

        .buttons {
          padding: 16px;
        }
      `]}constructor(...e){super(...e),this.narrow=!1,this._loading=!1,this.handleReadOnlyFields=(0,n.A)(e=>e?.map(e=>({...e,...Object.values(e?.selector??{})[0]?.read_only?{disabled:!0}:{}}))),this._handleKeyDown=e=>{"Enter"===e.key&&this._submitStep()},this._labelCallback=(e,t,o)=>this.flowConfig.renderShowFormStepFieldLabel(this.hass,this.step,e,o),this._helperCallback=(e,t)=>this.flowConfig.renderShowFormStepFieldHelper(this.hass,this.step,e,t),this._errorCallback=e=>this.flowConfig.renderShowFormStepFieldError(this.hass,this.step,e),this._localizeValueCallback=e=>this.flowConfig.renderShowFormStepFieldLocalizeValue(this.hass,this.step,e)}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],v.prototype,"flowConfig",void 0),(0,a.__decorate)([(0,r.MZ)({type:Boolean})],v.prototype,"narrow",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],v.prototype,"step",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],v.prototype,"hass",void 0),(0,a.__decorate)([(0,r.wk)()],v.prototype,"_loading",void 0),(0,a.__decorate)([(0,r.wk)()],v.prototype,"_stepData",void 0),(0,a.__decorate)([(0,r.wk)()],v.prototype,"_previewErrors",void 0),(0,a.__decorate)([(0,r.wk)()],v.prototype,"_submitErrors",void 0),(0,a.__decorate)([(0,r.wk)()],v.prototype,"_errorMsg",void 0),v=(0,a.__decorate)([(0,r.EM)("step-flow-form")],v),t()}catch(v){t(v)}})},19486:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(89600),s=e([n]);n=(s.then?(await s)():s)[0];class l extends i.WF{render(){const e=this.flowConfig.renderLoadingDescription(this.hass,this.loadingReason,this.handler,this.step);return i.qy`
      <div class="content">
        <ha-spinner size="large"></ha-spinner>
        ${e?i.qy`<div>${e}</div>`:""}
      </div>
    `}}l.styles=i.AH`
    .content {
      margin-top: 0;
      padding: 50px 100px;
      text-align: center;
    }
    ha-spinner {
      margin-bottom: 16px;
    }
  `,(0,a.__decorate)([(0,r.MZ)({attribute:!1})],l.prototype,"flowConfig",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],l.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],l.prototype,"loadingReason",void 0),(0,a.__decorate)([(0,r.MZ)()],l.prototype,"handler",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],l.prototype,"step",void 0),l=(0,a.__decorate)([(0,r.EM)("step-flow-loading")],l),t()}catch(l){t(l)}})},59395:function(e,t,o){var a=o(62826),i=o(96196),r=o(77845),n=o(92542),s=(o(28608),o(56565),o(97854)),l=o(25749);class c extends i.WF{shouldUpdate(e){return e.size>1||!e.has("hass")||this.hass.localize!==e.get("hass")?.localize}render(){let e,t,o={};if(Array.isArray(this.step.menu_options)){e=this.step.menu_options,t={};for(const a of e)t[a]=this.flowConfig.renderMenuOption(this.hass,this.step,a),o[a]=this.flowConfig.renderMenuOptionDescription(this.hass,this.step,a)}else e=Object.keys(this.step.menu_options),t=this.step.menu_options,o=Object.fromEntries(e.map(e=>[e,this.flowConfig.renderMenuOptionDescription(this.hass,this.step,e)]));this.step.sort&&(e=e.sort((e,o)=>(0,l.xL)(t[e],t[o],this.hass.locale.language)));const a=this.flowConfig.renderMenuDescription(this.hass,this.step);return i.qy`
      ${a?i.qy`<div class="content">${a}</div>`:""}
      <div class="options">
        ${e.map(e=>i.qy`
            <ha-list-item
              hasMeta
              .step=${e}
              @click=${this._handleStep}
              ?twoline=${o[e]}
              ?multiline-secondary=${o[e]}
            >
              <span>${t[e]}</span>
              ${o[e]?i.qy`<span slot="secondary">
                    ${o[e]}
                  </span>`:i.s6}
              <ha-icon-next slot="meta"></ha-icon-next>
            </ha-list-item>
          `)}
      </div>
    `}_handleStep(e){(0,n.r)(this,"flow-update",{stepPromise:this.flowConfig.handleFlowStep(this.hass,this.step.flow_id,{next_step_id:e.currentTarget.step})})}}c.styles=[s.G,i.AH`
      .options {
        margin-top: 20px;
        margin-bottom: 16px;
      }
      .content {
        padding-bottom: 16px;
      }
      .content + .options {
        margin-top: 8px;
      }
      ha-list-item {
        --mdc-list-side-padding: 24px;
      }
    `],(0,a.__decorate)([(0,r.MZ)({attribute:!1})],c.prototype,"flowConfig",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],c.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],c.prototype,"step",void 0),c=(0,a.__decorate)([(0,r.EM)("step-flow-menu")],c)},12527:function(e,t,o){o.a(e,async function(e,t){try{var a=o(62826),i=o(96196),r=o(77845),n=o(48565),s=o(64109),l=o(89600),c=o(97854),d=e([s,l]);[s,l]=d.then?(await d)():d;class p extends i.WF{render(){return i.qy`
      <div class="content">
        ${this.progress?i.qy`
              <ha-progress-ring .value=${this.progress} size="large"
                >${this.progress}${(0,n.d)(this.hass.locale)}%</ha-progress-ring
              >
            `:i.qy`<ha-spinner size="large"></ha-spinner>`}
        ${this.flowConfig.renderShowFormProgressDescription(this.hass,this.step)}
      </div>
    `}static get styles(){return[c.G,i.AH`
        .content {
          margin-top: 0;
          padding: 50px 100px;
          text-align: center;
        }
        ha-spinner {
          margin-bottom: 16px;
        }
      `]}}(0,a.__decorate)([(0,r.MZ)({attribute:!1})],p.prototype,"flowConfig",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],p.prototype,"hass",void 0),(0,a.__decorate)([(0,r.MZ)({attribute:!1})],p.prototype,"step",void 0),(0,a.__decorate)([(0,r.MZ)({type:Number})],p.prototype,"progress",void 0),p=(0,a.__decorate)([(0,r.EM)("step-flow-progress")],p),t()}catch(p){t(p)}})},97854:function(e,t,o){o.d(t,{G:()=>a});const a=o(96196).AH`
  h2 {
    margin: 24px 38px 0 0;
    margin-inline-start: 0px;
    margin-inline-end: 38px;
    padding: 0 24px;
    padding-inline-start: 24px;
    padding-inline-end: 24px;
    -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
    -webkit-font-smoothing: var(--ha-font-smoothing);
    font-family: var(
      --mdc-typography-headline6-font-family,
      var(--mdc-typography-font-family, var(--ha-font-family-body))
    );
    font-size: var(--mdc-typography-headline6-font-size, var(--ha-font-size-l));
    line-height: var(--mdc-typography-headline6-line-height, 2rem);
    font-weight: var(
      --mdc-typography-headline6-font-weight,
      var(--ha-font-weight-medium)
    );
    letter-spacing: var(--mdc-typography-headline6-letter-spacing, 0.0125em);
    text-decoration: var(--mdc-typography-headline6-text-decoration, inherit);
    text-transform: var(--mdc-typography-headline6-text-transform, inherit);
    box-sizing: border-box;
  }

  .content,
  .preview {
    margin-top: 20px;
    padding: 0 24px;
  }

  .buttons {
    position: relative;
    padding: 16px;
    margin: 8px 0 0;
    color: var(--primary-color);
    display: flex;
    justify-content: flex-end;
  }

  ha-markdown {
    overflow-wrap: break-word;
  }
  ha-markdown a {
    color: var(--primary-color);
  }
  ha-markdown img:first-child:last-child {
    display: block;
    margin: 0 auto;
  }
`},6358:function(e,t,o){o.d(t,{L:()=>r});var a=o(92542);const i=()=>Promise.all([o.e("2239"),o.e("7251"),o.e("3577"),o.e("2016"),o.e("1279"),o.e("105"),o.e("9272"),o.e("4398"),o.e("5633"),o.e("293"),o.e("4775"),o.e("2097")]).then(o.bind(o,54728)),r=(e,t)=>{(0,a.r)(e,"show-dialog",{dialogTag:"ha-voice-assistant-setup-dialog",dialogImport:i,dialogParams:t})}},78778:function(e,t,o){o.d(t,{a:()=>r});var a=o(92542);const i=()=>Promise.all([o.e("9291"),o.e("4556"),o.e("8451")]).then(o.bind(o,71614)),r=(e,t)=>{(0,a.r)(e,"show-dialog",{dialogTag:"dialog-add-application-credential",dialogImport:i,dialogParams:t})}},82160:function(e,t,o){o.d(t,{J:()=>r});var a=o(92542);const i=()=>Promise.all([o.e("9291"),o.e("3785"),o.e("5989"),o.e("4398"),o.e("5633"),o.e("2757"),o.e("274"),o.e("4363"),o.e("7298"),o.e("1883")]).then(o.bind(o,76218)),r=(e,t)=>{(0,a.r)(e,"show-dialog",{dialogTag:"dialog-area-registry-detail",dialogImport:i,dialogParams:t})}},76681:function(e,t,o){o.d(t,{MR:()=>a,a_:()=>i,bg:()=>r});const a=e=>`https://brands.home-assistant.io/${e.brand?"brands/":""}${e.useFallback?"_/":""}${e.domain}/${e.darkOptimized?"dark_":""}${e.type}.png`,i=e=>e.split("/")[4],r=e=>e.startsWith("https://brands.home-assistant.io/")},62001:function(e,t,o){o.d(t,{o:()=>a});const a=(e,t)=>`https://${e.config.version.includes("b")?"rc":e.config.version.includes("dev")?"next":"www"}.home-assistant.io${t}`},2355:function(e,t,o){o.d(t,{A:()=>a});const a=o(96196).AH`:host {
  --size: 8rem;
  --track-width: 0.25em;
  --track-color: var(--wa-color-neutral-fill-normal);
  --indicator-width: var(--track-width);
  --indicator-color: var(--wa-color-brand-fill-loud);
  --indicator-transition-duration: 0.35s;
  display: inline-flex;
}
.progress-ring {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.image {
  width: var(--size);
  height: var(--size);
  rotate: -90deg;
  transform-origin: 50% 50%;
}
.track,
.indicator {
  --radius: calc(var(--size) / 2 - max(var(--track-width), var(--indicator-width)) * 0.5);
  --circumference: calc(var(--radius) * 2 * 3.141592654);
  fill: none;
  r: var(--radius);
  cx: calc(var(--size) / 2);
  cy: calc(var(--size) / 2);
}
.track {
  stroke: var(--track-color);
  stroke-width: var(--track-width);
}
.indicator {
  stroke: var(--indicator-color);
  stroke-width: var(--indicator-width);
  stroke-linecap: round;
  transition-property: stroke-dashoffset;
  transition-duration: var(--indicator-transition-duration);
  stroke-dasharray: var(--circumference) var(--circumference);
  stroke-dashoffset: calc(var(--circumference) - var(--percentage) * var(--circumference));
}
.label {
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  text-align: center;
  user-select: none;
  -webkit-user-select: none;
}
`},65686:function(e,t,o){o.a(e,async function(e,a){try{o.d(t,{A:()=>u});var i=o(96196),r=o(77845),n=o(32510),s=o(17060),l=o(2355),c=e([s]);s=(c.then?(await c)():c)[0];var d=Object.defineProperty,p=Object.getOwnPropertyDescriptor,h=(e,t,o,a)=>{for(var i,r=a>1?void 0:a?p(t,o):t,n=e.length-1;n>=0;n--)(i=e[n])&&(r=(a?i(t,o,r):i(r))||r);return a&&r&&d(t,o,r),r};let u=class extends n.A{updated(e){if(super.updated(e),e.has("value")){const e=parseFloat(getComputedStyle(this.indicator).getPropertyValue("r")),t=2*Math.PI*e,o=t-this.value/100*t;this.indicatorOffset=`${o}px`}}render(){return i.qy`
      <div
        part="base"
        class="progress-ring"
        role="progressbar"
        aria-label=${this.label.length>0?this.label:this.localize.term("progress")}
        aria-describedby="label"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow="${this.value}"
        style="--percentage: ${this.value/100}"
      >
        <svg class="image">
          <circle class="track"></circle>
          <circle class="indicator" style="stroke-dashoffset: ${this.indicatorOffset}"></circle>
        </svg>

        <slot id="label" part="label" class="label"></slot>
      </div>
    `}constructor(){super(...arguments),this.localize=new s.c(this),this.value=0,this.label=""}};u.css=l.A,h([(0,r.P)(".indicator")],u.prototype,"indicator",2),h([(0,r.wk)()],u.prototype,"indicatorOffset",2),h([(0,r.MZ)({type:Number,reflect:!0})],u.prototype,"value",2),h([(0,r.MZ)()],u.prototype,"label",2),u=h([(0,r.EM)("wa-progress-ring")],u),a()}catch(u){a(u)}})},9395:function(e,t,o){function a(e,t){const o={waitUntilFirstUpdate:!1,...t};return(t,a)=>{const{update:i}=t,r=Array.isArray(e)?e:[e];t.update=function(e){r.forEach(t=>{const i=t;if(e.has(i)){const t=e.get(i),r=this[i];t!==r&&(o.waitUntilFirstUpdate&&!this.hasUpdated||this[a](t,r))}}),i.call(this,e)}}}o.d(t,{w:()=>a})},32510:function(e,t,o){o.d(t,{A:()=>m});var a=o(96196),i=o(77845);const r=":host {\n  box-sizing: border-box !important;\n}\n\n:host *,\n:host *::before,\n:host *::after {\n  box-sizing: inherit !important;\n}\n\n[hidden] {\n  display: none !important;\n}\n";class n extends Set{add(e){super.add(e);const t=this._existing;if(t)try{t.add(e)}catch{t.add(`--${e}`)}else this._el.setAttribute(`state-${e}`,"");return this}delete(e){super.delete(e);const t=this._existing;return t?(t.delete(e),t.delete(`--${e}`)):this._el.removeAttribute(`state-${e}`),!0}has(e){return super.has(e)}clear(){for(const e of this)this.delete(e)}constructor(e,t=null){super(),this._existing=null,this._el=e,this._existing=t}}const s=CSSStyleSheet.prototype.replaceSync;Object.defineProperty(CSSStyleSheet.prototype,"replaceSync",{value:function(e){e=e.replace(/:state\(([^)]+)\)/g,":where(:state($1), :--$1, [state-$1])"),s.call(this,e)}});var l,c=Object.defineProperty,d=Object.getOwnPropertyDescriptor,p=e=>{throw TypeError(e)},h=(e,t,o,a)=>{for(var i,r=a>1?void 0:a?d(t,o):t,n=e.length-1;n>=0;n--)(i=e[n])&&(r=(a?i(t,o,r):i(r))||r);return a&&r&&c(t,o,r),r},u=(e,t,o)=>t.has(e)||p("Cannot "+o);class m extends a.WF{static get styles(){const e=Array.isArray(this.css)?this.css:this.css?[this.css]:[];return[r,...e].map(e=>"string"==typeof e?(0,a.iz)(e):e)}attachInternals(){const e=super.attachInternals();return Object.defineProperty(e,"states",{value:new n(this,e.states)}),e}attributeChangedCallback(e,t,o){var a,i,r;u(a=this,i=l,"read from private field"),(r?r.call(a):i.get(a))||(this.constructor.elementProperties.forEach((e,t)=>{e.reflect&&null!=this[t]&&this.initialReflectedProperties.set(t,this[t])}),((e,t,o,a)=>{u(e,t,"write to private field"),a?a.call(e,o):t.set(e,o)})(this,l,!0)),super.attributeChangedCallback(e,t,o)}willUpdate(e){super.willUpdate(e),this.initialReflectedProperties.forEach((t,o)=>{e.has(o)&&null==this[o]&&(this[o]=t)})}firstUpdated(e){super.firstUpdated(e),this.didSSR&&this.shadowRoot?.querySelectorAll("slot").forEach(e=>{e.dispatchEvent(new Event("slotchange",{bubbles:!0,composed:!1,cancelable:!1}))})}update(e){try{super.update(e)}catch(t){if(this.didSSR&&!this.hasUpdated){const e=new Event("lit-hydration-error",{bubbles:!0,composed:!0,cancelable:!1});e.error=t,this.dispatchEvent(e)}throw t}}relayNativeEvent(e,t){e.stopImmediatePropagation(),this.dispatchEvent(new e.constructor(e.type,{...e,...t}))}constructor(){var e,t,o;super(),e=this,o=!1,(t=l).has(e)?p("Cannot add the same private member more than once"):t instanceof WeakSet?t.add(e):t.set(e,o),this.initialReflectedProperties=new Map,this.didSSR=a.S$||Boolean(this.shadowRoot),this.customStates={set:(e,t)=>{if(Boolean(this.internals?.states))try{t?this.internals.states.add(e):this.internals.states.delete(e)}catch(o){if(!String(o).includes("must start with '--'"))throw o;console.error("Your browser implements an outdated version of CustomStateSet. Consider using a polyfill")}},has:e=>{if(!Boolean(this.internals?.states))return!1;try{return this.internals.states.has(e)}catch{return!1}}};try{this.internals=this.attachInternals()}catch{console.error("Element internals are not supported in your browser. Consider using a polyfill")}this.customStates.set("wa-defined",!0);let i=this.constructor;for(let[a,r]of i.elementProperties)"inherit"===r.default&&void 0!==r.initial&&"string"==typeof a&&this.customStates.set(`initial-${a}-${r.initial}`,!0)}}l=new WeakMap,h([(0,i.MZ)()],m.prototype,"dir",2),h([(0,i.MZ)()],m.prototype,"lang",2),h([(0,i.MZ)({type:Boolean,reflect:!0,attribute:"did-ssr"})],m.prototype,"didSSR",2)},25594:function(e,t,o){o.a(e,async function(e,a){try{o.d(t,{A:()=>n});var i=o(38640),r=e([i]);i=(r.then?(await r)():r)[0];const s={$code:"en",$name:"English",$dir:"ltr",carousel:"Carousel",clearEntry:"Clear entry",close:"Close",copied:"Copied",copy:"Copy",currentValue:"Current value",error:"Error",goToSlide:(e,t)=>`Go to slide ${e} of ${t}`,hidePassword:"Hide password",loading:"Loading",nextSlide:"Next slide",numOptionsSelected:e=>0===e?"No options selected":1===e?"1 option selected":`${e} options selected`,pauseAnimation:"Pause animation",playAnimation:"Play animation",previousSlide:"Previous slide",progress:"Progress",remove:"Remove",resize:"Resize",scrollableRegion:"Scrollable region",scrollToEnd:"Scroll to end",scrollToStart:"Scroll to start",selectAColorFromTheScreen:"Select a color from the screen",showPassword:"Show password",slideNum:e=>`Slide ${e}`,toggleColorFormat:"Toggle color format",zoomIn:"Zoom in",zoomOut:"Zoom out"};(0,i.XC)(s);var n=s;a()}catch(s){a(s)}})},17060:function(e,t,o){o.a(e,async function(e,a){try{o.d(t,{c:()=>s});var i=o(38640),r=o(25594),n=e([i,r]);[i,r]=n.then?(await n)():n;class s extends i.c2{}(0,i.XC)(r.A),a()}catch(s){a(s)}})},38640:function(e,t,o){o.a(e,async function(e,a){try{o.d(t,{XC:()=>u,c2:()=>g});var i=o(22),r=e([i]);i=(r.then?(await r)():r)[0];const s=new Set,l=new Map;let c,d="ltr",p="en";const h="undefined"!=typeof MutationObserver&&"undefined"!=typeof document&&void 0!==document.documentElement;if(h){const _=new MutationObserver(m);d=document.documentElement.dir||"ltr",p=document.documentElement.lang||navigator.language,_.observe(document.documentElement,{attributes:!0,attributeFilter:["dir","lang"]})}function u(...e){e.map(e=>{const t=e.$code.toLowerCase();l.has(t)?l.set(t,Object.assign(Object.assign({},l.get(t)),e)):l.set(t,e),c||(c=e)}),m()}function m(){h&&(d=document.documentElement.dir||"ltr",p=document.documentElement.lang||navigator.language),[...s.keys()].map(e=>{"function"==typeof e.requestUpdate&&e.requestUpdate()})}class g{hostConnected(){s.add(this.host)}hostDisconnected(){s.delete(this.host)}dir(){return`${this.host.dir||d}`.toLowerCase()}lang(){return`${this.host.lang||p}`.toLowerCase()}getTranslationData(e){var t,o;const a=new Intl.Locale(e.replace(/_/g,"-")),i=null==a?void 0:a.language.toLowerCase(),r=null!==(o=null===(t=null==a?void 0:a.region)||void 0===t?void 0:t.toLowerCase())&&void 0!==o?o:"";return{locale:a,language:i,region:r,primary:l.get(`${i}-${r}`),secondary:l.get(i)}}exists(e,t){var o;const{primary:a,secondary:i}=this.getTranslationData(null!==(o=t.lang)&&void 0!==o?o:this.lang());return t=Object.assign({includeFallback:!1},t),!!(a&&a[e]||i&&i[e]||t.includeFallback&&c&&c[e])}term(e,...t){const{primary:o,secondary:a}=this.getTranslationData(this.lang());let i;if(o&&o[e])i=o[e];else if(a&&a[e])i=a[e];else{if(!c||!c[e])return console.error(`No translation found for: ${String(e)}`),String(e);i=c[e]}return"function"==typeof i?i(...t):i}date(e,t){return e=new Date(e),new Intl.DateTimeFormat(this.lang(),t).format(e)}number(e,t){return e=Number(e),isNaN(e)?"":new Intl.NumberFormat(this.lang(),t).format(e)}relativeTime(e,t,o){return new Intl.RelativeTimeFormat(this.lang(),o).format(e,t)}constructor(e){this.host=e,this.host.addController(this)}}a()}catch(n){a(n)}})}};
//# sourceMappingURL=6568.a393d872a170d6dc.js.map