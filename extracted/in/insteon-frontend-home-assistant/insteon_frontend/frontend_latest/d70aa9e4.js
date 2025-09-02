"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[4132],{44672:(e,t,i)=>{i.d(t,{p:()=>r});const r=e=>e.substr(e.indexOf(".")+1)},2733:(e,t,i)=>{i.d(t,{C:()=>a});var r=i(44672);const a=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,r.p)(t).replace(/_/g," "):(null!==(a=i.friendly_name)&&void 0!==a?a:"").toString();var t,i,a}},28858:(e,t,i)=>{i.d(t,{$:()=>s,f:()=>d});var r=i(14516);const a=(0,r.Z)((e=>new Intl.Collator(e))),o=(0,r.Z)((e=>new Intl.Collator(e,{sensitivity:"accent"}))),n=(e,t)=>e<t?-1:e>t?1:0,s=(e,t,i=void 0)=>{var r;return null!==(r=Intl)&&void 0!==r&&r.Collator?a(i).compare(e,t):n(e,t)},d=(e,t,i=void 0)=>{var r;return null!==(r=Intl)&&void 0!==r&&r.Collator?o(i).compare(e,t):n(e.toLowerCase(),t.toLowerCase())}},85878:(e,t,i)=>{var r=i(73958),a=i(565),o=i(47838),n=(i(6294),i(9644)),s=i(36924),d=i(47509),l=i(15815);(0,r.Z)([(0,s.Mo)("ha-button-menu")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:l.gA,value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,s.Cb)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,s.Cb)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,s.Cb)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return n.dy`
      <div @click=${this._handleClick}>
        <slot name="trigger" @slotchange=${this._setTriggerAria}></slot>
      </div>
      <mwc-menu
        .corner=${this.corner}
        .menuCorner=${this.menuCorner}
        .fixed=${this.fixed}
        .multi=${this.multi}
        .activatable=${this.activatable}
        .y=${this.y}
        .x=${this.x}
      >
        <slot></slot>
      </mwc-menu>
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)((0,o.Z)(i.prototype),"firstUpdated",this).call(this,e),"rtl"===d.E.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),n.oi)},68336:(e,t,i)=>{var r=i(73958),a=i(9644),o=i(36924);(0,r.Z)([(0,o.Mo)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`
      :host {
        background: var(
          --ha-card-background,
          var(--card-background-color, white)
        );
        box-shadow: var(--ha-card-box-shadow, none);
        box-sizing: border-box;
        border-radius: var(--ha-card-border-radius, 12px);
        border-width: var(--ha-card-border-width, 1px);
        border-style: solid;
        border-color: var(
          --ha-card-border-color,
          var(--divider-color, #e0e0e0)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      :host([raised]) {
        border: none;
        box-shadow: var(
          --ha-card-box-shadow,
          0px 2px 1px -1px rgba(0, 0, 0, 0.2),
          0px 1px 1px 0px rgba(0, 0, 0, 0.14),
          0px 1px 3px 0px rgba(0, 0, 0, 0.12)
        );
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 48px;
        padding: 12px 16px 16px;
        display: block;
        margin-block-start: 0px;
        margin-block-end: 0px;
        font-weight: normal;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid var(--divider-color, #e8e8e8);
        padding: 5px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return a.dy`
      ${this.header?a.dy`<h1 class="card-header">${this.header}</h1>`:a.Ld}
      <slot></slot>
    `}}]}}),a.oi)},99040:(e,t,i)=>{var r=i(73958),a=i(565),o=i(47838),n=i(48095),s=i(72477),d=i(36924),l=i(9644),c=i(47509);(0,r.Z)([(0,d.Mo)("ha-fab")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)((0,o.Z)(i.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}},{kind:"field",static:!0,key:"styles",value(){return[s.W,l.iv`
      :host .mdc-fab--extended .mdc-fab__icon {
        margin-inline-start: -8px;
        margin-inline-end: 12px;
        direction: var(--direction);
      }
    `,"rtl"===c.E.document.dir?l.iv`
          :host .mdc-fab--extended .mdc-fab__icon {
            direction: rtl;
          }
        `:l.iv``]}}]}}),n._)},51134:(e,t,i)=>{i.d(t,{HP:()=>h,R6:()=>u,_Y:()=>d,jL:()=>n,q4:()=>c,t1:()=>s});var r=i(45666),a=i(2733),o=(i(28858),i(72218));const n=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,r=e.states[t];if(r)return(0,a.C)(r)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),s=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),d=e=>e.sendMessagePromise({type:"config/device_registry/list"}),l=(e,t)=>e.subscribeEvents((0,o.D)((()=>d(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),c=(e,t)=>(0,r.B)("_dr",d,l,e,t),u=e=>{const t={};for(const i of e)i.device_id&&(i.device_id in t||(t[i.device_id]=[]),t[i.device_id].push(i));return t},h=(e,t)=>{const i={};for(const r of t){const t=e[r.entity_id];null!=t&&t.domain&&null!==r.device_id&&(i[r.device_id]||(i[r.device_id]=[]),i[r.device_id].push(t.domain))}return i}},11285:(e,t,i)=>{i.d(t,{D9:()=>d,Ys:()=>n,g7:()=>s});var r=i(18394);const a=()=>Promise.all([i.e(5084),i.e(4338)]).then(i.bind(i,44338)),o=(e,t,i)=>new Promise((o=>{const n=t.cancel,s=t.confirm;(0,r.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:a,dialogParams:{...t,...i,cancel:()=>{o(!(null==i||!i.prompt)&&null),n&&n()},confirm:e=>{o(null==i||!i.prompt||e),s&&s(e)}}})})),n=(e,t)=>o(e,t),s=(e,t)=>o(e,t,{confirmation:!0}),d=(e,t)=>o(e,t,{prompt:!0})},38122:(e,t,i)=>{var r=i(73958),a=(i(30437),i(33829),i(9644)),o=i(36924),n=i(18394),s=i(51750);i(31007),i(40841);(0,r.Z)([(0,o.Mo)("hass-tabs-subpage-data-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Object})],key:"columns",value(){return{}}},{kind:"field",decorators:[(0,o.Cb)({type:Array})],key:"data",value(){return[]}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"selectable",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"clickable",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"hasFab",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"id",value(){return"id"}},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"filter",value(){return""}},{kind:"field",decorators:[(0,o.Cb)()],key:"searchLabel",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Array})],key:"activeFilters",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"hiddenLabel",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Number})],key:"numHidden",value(){return 0}},{kind:"field",decorators:[(0,o.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,o.Cb)()],key:"tabs",value(){return[]}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"hideFilterMenu",value(){return!1}},{kind:"field",decorators:[(0,o.IO)("ha-data-table",!0)],key:"_dataTable",value:void 0},{kind:"method",key:"clearSelection",value:function(){this._dataTable.clearSelection()}},{kind:"method",key:"render",value:function(){const e=this.numHidden?this.hiddenLabel||this.hass.localize("ui.components.data-table.hidden",{number:this.numHidden})||this.numHidden:void 0,t=this.activeFilters?a.dy`${this.hass.localize("ui.components.data-table.filtering_by")}
        ${this.activeFilters.join(", ")}
        ${e?`(${e})`:""}`:e,i=a.dy`<search-input
      .hass=${this.hass}
      .filter=${this.filter}
      .suffix=${!this.narrow}
      @value-changed=${this._handleSearchChange}
      .label=${this.searchLabel}
    >
      ${this.narrow?"":a.dy`<div
            class="filters"
            slot="suffix"
            @click=${this._preventDefault}
          >
            ${t?a.dy`<div class="active-filters">
                  ${t}
                  <mwc-button @click=${this._clearFilter}>
                    ${this.hass.localize("ui.components.data-table.clear")}
                  </mwc-button>
                </div>`:""}
            <slot name="filter-menu"></slot>
          </div>`}
    </search-input>`;return a.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .localizeFunc=${this.localizeFunc}
        .narrow=${this.narrow}
        .isWide=${this.isWide}
        .backPath=${this.backPath}
        .backCallback=${this.backCallback}
        .route=${this.route}
        .tabs=${this.tabs}
        .mainPage=${this.mainPage}
        .supervisor=${this.supervisor}
      >
        ${this.hideFilterMenu?"":a.dy`
              <div slot="toolbar-icon">
                ${this.narrow?a.dy`
                      <div class="filter-menu">
                        ${this.numHidden||this.activeFilters?a.dy`<span class="badge"
                              >${this.numHidden||"!"}</span
                            >`:""}
                        <slot name="filter-menu"></slot>
                      </div>
                    `:""}<slot name="toolbar-icon"></slot>
              </div>
            `}
        ${this.narrow?a.dy`
              <div slot="header">
                <slot name="header">
                  <div class="search-toolbar">${i}</div>
                </slot>
              </div>
            `:""}
        <ha-data-table
          .hass=${this.hass}
          .columns=${this.columns}
          .data=${this.data}
          .filter=${this.filter}
          .selectable=${this.selectable}
          .hasFab=${this.hasFab}
          .id=${this.id}
          .noDataText=${this.noDataText}
          .dir=${(0,s.Zu)(this.hass)}
          .clickable=${this.clickable}
          .appendRow=${this.appendRow}
        >
          ${this.narrow?a.dy` <div slot="header"></div> `:a.dy`
                <div slot="header">
                  <slot name="header">
                    <div class="table-header">${i}</div>
                  </slot>
                </div>
              `}
        </ha-data-table>
        <div slot="fab"><slot name="fab"></slot></div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_preventDefault",value:function(e){e.preventDefault()}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter!==e.detail.value&&(this.filter=e.detail.value,(0,n.B)(this,"search-changed",{value:this.filter}))}},{kind:"method",key:"_clearFilter",value:function(){(0,n.B)(this,"clear-filter")}},{kind:"get",static:!0,key:"styles",value:function(){return a.iv`
      ha-data-table {
        width: 100%;
        height: 100%;
        --data-table-border-width: 0;
      }
      :host(:not([narrow])) ha-data-table {
        height: calc(100vh - 1px - var(--header-height));
        display: block;
      }
      :host([narrow]) hass-tabs-subpage {
        --main-title-margin: 0;
      }
      .table-header {
        display: flex;
        align-items: center;
        --mdc-shape-small: 0;
        height: 56px;
      }
      .search-toolbar {
        display: flex;
        align-items: center;
        color: var(--secondary-text-color);
      }
      search-input {
        --mdc-text-field-fill-color: var(--sidebar-background-color);
        --mdc-text-field-idle-line-color: var(--divider-color);
        --text-field-overflow: visible;
        z-index: 5;
      }
      .table-header search-input {
        display: block;
        position: absolute;
        top: 0;
        right: 0;
        left: 0;
      }
      .search-toolbar search-input {
        display: block;
        width: 100%;
        color: var(--secondary-text-color);
        --mdc-ripple-color: transparant;
      }
      .filters {
        --mdc-text-field-fill-color: var(--input-fill-color);
        --mdc-text-field-idle-line-color: var(--input-idle-line-color);
        --mdc-shape-small: 4px;
        --text-field-overflow: initial;
        display: flex;
        justify-content: flex-end;
        color: var(--primary-text-color);
      }
      .active-filters {
        color: var(--primary-text-color);
        position: relative;
        display: flex;
        align-items: center;
        padding: 2px 2px 2px 8px;
        margin-left: 4px;
        margin-inline-start: 4px;
        margin-inline-end: initial;
        font-size: 14px;
        width: max-content;
        cursor: initial;
        direction: var(--direction);
      }
      .active-filters ha-svg-icon {
        color: var(--primary-color);
      }
      .active-filters mwc-button {
        margin-left: 8px;
        margin-inline-start: 8px;
        margin-inline-end: initial;
        direction: var(--direction);
      }
      .active-filters::before {
        background-color: var(--primary-color);
        opacity: 0.12;
        border-radius: 4px;
        position: absolute;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        content: "";
      }
      .badge {
        min-width: 20px;
        box-sizing: border-box;
        border-radius: 50%;
        font-weight: 400;
        background-color: var(--primary-color);
        line-height: 20px;
        text-align: center;
        padding: 0px 4px;
        color: var(--text-primary-color);
        position: absolute;
        right: 0;
        top: 4px;
        font-size: 0.65em;
      }
      .filter-menu {
        position: relative;
      }
    `}}]}}),a.oi)},74132:(e,t,i)=>{i.r(t),i.d(t,{DeviceOverridesPanel:()=>b});var r=i(73958),a=i(565),o=i(47838),n=i(9644),s=i(36924),d=i(14516),l=(i(31007),i(99040),i(68336),i(85878),i(38122),i(51134)),c=i(34838),u=i(71155),h=i(11285),v=i(18394);const p=()=>Promise.all([i.e(5084),i.e(529),i.e(9663),i.e(226)]).then(i.bind(i,12220));var f=i(8205);let b=(0,r.Z)([(0,s.Mo)("device-overrides-panel")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Object})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Array})],key:"_devices",value(){return[]}},{kind:"field",decorators:[(0,s.SB)()],key:"_device_overrides",value(){return[]}},{kind:"field",key:"_unsubs",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)((0,o.Z)(i.prototype),"firstUpdated",this).call(this,e),this.hass&&this.insteon||(0,u.c)("/insteon"),this._getOverrides(),this._unsubs||this._getDevices()}},{kind:"method",key:"_getOverrides",value:async function(){await(0,c.uc)(this.hass).then((e=>{this._device_overrides=e.override_config}))}},{kind:"method",key:"_getDevices",value:function(){this.insteon&&this.hass&&(this._unsubs=[(0,l.q4)(this.hass.connection,(e=>{this._devices=e.filter((e=>e.config_entries&&e.config_entries.includes(this.insteon.config_entry.entry_id)))}))])}},{kind:"field",key:"_columns",value(){return(0,d.Z)((e=>e?{name:{title:this.insteon.localize("devices.fields.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0},address:{title:this.insteon.localize("devices.fields.address"),sortable:!0,filterable:!0,direction:"asc",width:"5hv"}}:{name:{title:this.insteon.localize("devices.fields.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0},address:{title:this.insteon.localize("devices.fields.address"),sortable:!0,filterable:!0,direction:"asc",width:"20%"},description:{title:this.insteon.localize("devices.fields.description"),sortable:!0,filterable:!0,direction:"asc",width:"15%"},model:{title:this.insteon.localize("devices.fields.model"),sortable:!0,filterable:!0,direction:"asc",width:"15%"},actions:{title:this.insteon.localize("devices.fields.actions"),type:"icon-button",template:e=>n.dy`
              <ha-icon-button
                .override=${e}
                .hass=${this.hass}
                .insteon=${this.insteon}
                .action=${()=>this._deleteOverride(this.hass,e.address)}
                .label=${this.insteon.localize("utils.config_device_overrides.actions.delete")}
                .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
                @click=${this._confirmDeleteOverride}
              ></ha-icon-button>
            `,width:"150px"}}))}},{kind:"field",key:"_insteonDevices",value(){return(0,d.Z)(((e,t)=>{if(!e||!t)return[];return e.map((e=>{var i,r;const a=(0,f.jT)(e.address),o=t.find((e=>{var t;return(e.name?(0,f.jT)(null===(t=e.name)||void 0===t?void 0:t.substring(e.name.length-8)):"")==a}));return{id:o.id,name:o.name_by_user||o.name||"No device name",address:(null===(i=o.name)||void 0===i?void 0:i.substring(o.name.length-8))||"",description:(null===(r=o.name)||void 0===r?void 0:r.substring(0,o.name.length-8))||"",model:o.model||""}}))}))}},{kind:"method",key:"render",value:function(){return n.dy`
      <hass-tabs-subpage-data-table
        .hass=${this.hass}
        .narrow=${this.narrow}
        .data=${this._insteonDevices(this._device_overrides,this._devices)}
        .columns=${this._columns(this.narrow)}
        .localizeFunc=${this.insteon.localize}
        .mainPage=${!1}
        .hasFab=${!0}
        .tabs=${[{translationKey:"utils.config_device_overrides.caption",path:"/insteon"}]}
      >
        <ha-fab
          slot="fab"
          .label=${this.insteon.localize("utils.config_device_overrides.add_override")}
          extended
          @click=${this._addOverride}
        >
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage-data-table>
    `}},{kind:"method",key:"_confirmDeleteOverride",value:async function(e){e.stopPropagation();const t=e.currentTarget.override,i=e.currentTarget.insteon,r=e.currentTarget.action;(0,h.g7)(this,{text:n.dy`${i.localize("utils.config_device_overrides.actions.confirm_delete")}<br />
        ${t.name}`,confirm:async()=>await r()})}},{kind:"method",key:"_deleteOverride",value:async function(e,t){console.info("Delete override clicked received: "+t),await(0,c.r$)(e,t),await this._getOverrides()}},{kind:"method",key:"_addOverride",value:async function(){var e,t;await(e=this,t={hass:this.hass,insteon:this.insteon,title:this.insteon.localize("utils.config_device_overrides.add_override")},void(0,v.B)(e,"show-dialog",{dialogTag:"dialog-add-device-override",dialogImport:p,dialogParams:t})),await this._getOverrides()}}]}}),n.oi)},34838:(e,t,i)=>{i.d(t,{Be:()=>c,Bk:()=>n,X3:()=>u,YB:()=>l,g3:()=>o,mc:()=>a,pO:()=>d,r$:()=>s,uc:()=>r});const r=e=>e.callWS({type:"insteon/config/get"}),a=e=>e.callWS({type:"insteon/config/get_modem_schema"}),o=(e,t)=>e.callWS({type:"insteon/config/update_modem_config",config:t}),n=(e,t)=>e.callWS({type:"insteon/config/device_override/add",override:t}),s=(e,t)=>e.callWS({type:"insteon/config/device_override/remove",device_address:t}),d=e=>{let t;return t="light"==e?{type:"integer",valueMin:-1,valueMax:255,name:"dim_steps",required:!0,default:22}:{type:"constant",name:"dim_steps",required:!1,default:""},[{type:"select",options:[["a","a"],["b","b"],["c","c"],["d","d"],["e","e"],["f","f"],["g","g"],["h","h"],["i","i"],["j","j"],["k","k"],["l","l"],["m","m"],["n","n"],["o","o"],["p","p"]],name:"housecode",required:!0},{type:"select",options:[[1,"1"],[2,"2"],[3,"3"],[4,"4"],[5,"5"],[6,"6"],[7,"7"],[8,"8"],[9,"9"],[10,"10"],[11,"11"],[12,"12"],[13,"13"],[14,"14"],[15,"15"],[16,"16"]],name:"unitcode",required:!0},{type:"select",options:[["binary_sensor","binary_sensor"],["switch","switch"],["light","light"]],name:"platform",required:!0},t]};function l(e){return"device"in e}const c=(e,t)=>{const i=t.slice();return i.push({type:"boolean",required:!1,name:"manual_config"}),e&&i.push({type:"string",name:"plm_manual_config",required:!0}),i},u=[{name:"address",type:"string",required:!0},{name:"cat",type:"string",required:!0},{name:"subcat",type:"string",required:!0}]},8205:(e,t,i)=>{i.d(t,{Vo:()=>a,fF:()=>r,jT:()=>n});const r=e=>{const t=n(e);return 6==t.length&&a(t)},a=e=>{"0x"==e.substring(0,2).toLocaleLowerCase()&&(e=e.substring(2));const t=[...e];if(t.length%2!=0)return!1;for(let i=0;i<t.length;i++)if(!o(t[i]))return!1;return!0},o=e=>["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"].includes(e.toLocaleLowerCase()),n=e=>e.toLocaleLowerCase().split(".").join("")}}]);
//# sourceMappingURL=d70aa9e4.js.map