"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[8223],{44672:(e,t,i)=>{i.d(t,{p:()=>a});const a=e=>e.substr(e.indexOf(".")+1)},2733:(e,t,i)=>{i.d(t,{C:()=>o});var a=i(44672);const o=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,a.p)(t).replace(/_/g," "):(null!==(o=i.friendly_name)&&void 0!==o?o:"").toString();var t,i,o}},28858:(e,t,i)=>{i.d(t,{$:()=>s,f:()=>d});var a=i(14516);const o=(0,a.Z)((e=>new Intl.Collator(e))),r=(0,a.Z)((e=>new Intl.Collator(e,{sensitivity:"accent"}))),n=(e,t)=>e<t?-1:e>t?1:0,s=(e,t,i=void 0)=>{var a;return null!==(a=Intl)&&void 0!==a&&a.Collator?o(i).compare(e,t):n(e,t)},d=(e,t,i=void 0)=>{var a;return null!==(a=Intl)&&void 0!==a&&a.Collator?r(i).compare(e,t):n(e.toLowerCase(),t.toLowerCase())}},85878:(e,t,i)=>{var a=i(73958),o=i(565),r=i(47838),n=(i(6294),i(9644)),s=i(36924),d=i(47509),l=i(15815);(0,a.Z)([(0,s.Mo)("ha-button-menu")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:l.gA,value:void 0},{kind:"field",decorators:[(0,s.Cb)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,s.Cb)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,s.Cb)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,s.Cb)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,s.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,t;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(t=this._triggerButton)||void 0===t||t.focus()}},{kind:"method",key:"render",value:function(){return n.dy`
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
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,r.Z)(i.prototype),"firstUpdated",this).call(this,e),"rtl"===d.E.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const t=document.createElement("style");t.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(t)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),n.oi)},68336:(e,t,i)=>{var a=i(73958),o=i(9644),r=i(36924);(0,a.Z)([(0,r.Mo)("ha-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)()],key:"header",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"raised",value(){return!1}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
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
    `}},{kind:"method",key:"render",value:function(){return o.dy`
      ${this.header?o.dy`<h1 class="card-header">${this.header}</h1>`:o.Ld}
      <slot></slot>
    `}}]}}),o.oi)},99040:(e,t,i)=>{var a=i(73958),o=i(565),r=i(47838),n=i(48095),s=i(72477),d=i(36924),l=i(9644),c=i(47509);(0,a.Z)([(0,d.Mo)("ha-fab")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,r.Z)(i.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}},{kind:"field",static:!0,key:"styles",value(){return[s.W,l.iv`
      :host .mdc-fab--extended .mdc-fab__icon {
        margin-inline-start: -8px;
        margin-inline-end: 12px;
        direction: var(--direction);
      }
    `,"rtl"===c.E.document.dir?l.iv`
          :host .mdc-fab--extended .mdc-fab__icon {
            direction: rtl;
          }
        `:l.iv``]}}]}}),n._)},87545:(e,t,i)=>{i.d(t,{Lo:()=>n,a:()=>c,sG:()=>l});var a=i(45666),o=i(28858),r=i(72218);const n=(e,t)=>e.callWS({type:"config/area_registry/create",...t}),s=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then((e=>e.sort(((e,t)=>(0,o.$)(e.name,t.name))))),d=(e,t)=>e.subscribeEvents((0,r.D)((()=>s(e).then((e=>t.setState(e,!0)))),500,!0),"area_registry_updated"),l=(e,t)=>(0,a.B)("_areaRegistry",s,d,e,t),c=(e,t)=>(i,a)=>{const r=t?t.indexOf(i):-1,n=t?t.indexOf(a):1;if(-1===r&&-1===n){var s,d,l,c;const t=null!==(s=null==e||null===(d=e[i])||void 0===d?void 0:d.name)&&void 0!==s?s:i,r=null!==(l=null==e||null===(c=e[a])||void 0===c?void 0:c.name)&&void 0!==l?l:a;return(0,o.$)(t,r)}return-1===r?1:-1===n?-1:r-n}},51134:(e,t,i)=>{i.d(t,{HP:()=>u,R6:()=>h,_Y:()=>d,jL:()=>n,q4:()=>c,t1:()=>s});var a=i(45666),o=i(2733),r=(i(28858),i(72218));const n=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,a=e.states[t];if(a)return(0,o.C)(a)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),s=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),d=e=>e.sendMessagePromise({type:"config/device_registry/list"}),l=(e,t)=>e.subscribeEvents((0,r.D)((()=>d(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),c=(e,t)=>(0,a.B)("_dr",d,l,e,t),h=e=>{const t={};for(const i of e)i.device_id&&(i.device_id in t||(t[i.device_id]=[]),t[i.device_id].push(i));return t},u=(e,t)=>{const i={};for(const a of t){const t=e[a.entity_id];null!=t&&t.domain&&null!==a.device_id&&(i[a.device_id]||(i[a.device_id]=[]),i[a.device_id].push(t.domain))}return i}},11285:(e,t,i)=>{i.d(t,{D9:()=>d,Ys:()=>n,g7:()=>s});var a=i(18394);const o=()=>Promise.all([i.e(5084),i.e(4338)]).then(i.bind(i,44338)),r=(e,t,i)=>new Promise((r=>{const n=t.cancel,s=t.confirm;(0,a.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:{...t,...i,cancel:()=>{r(!(null==i||!i.prompt)&&null),n&&n()},confirm:e=>{r(null==i||!i.prompt||e),s&&s(e)}}})})),n=(e,t)=>r(e,t),s=(e,t)=>r(e,t,{confirmation:!0}),d=(e,t)=>r(e,t,{prompt:!0})},38122:(e,t,i)=>{var a=i(73958),o=(i(30437),i(33829),i(9644)),r=i(36924),n=i(18394),s=i(51750);i(31007),i(40841);(0,a.Z)([(0,r.Mo)("hass-tabs-subpage-data-table")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"localizeFunc",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"isWide",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"supervisor",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"main-page"})],key:"mainPage",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"columns",value(){return{}}},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"data",value(){return[]}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"selectable",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"clickable",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"hasFab",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"appendRow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String})],key:"id",value(){return"id"}},{kind:"field",decorators:[(0,r.Cb)({type:String})],key:"filter",value(){return""}},{kind:"field",decorators:[(0,r.Cb)()],key:"searchLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"activeFilters",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"hiddenLabel",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Number})],key:"numHidden",value(){return 0}},{kind:"field",decorators:[(0,r.Cb)({type:String,attribute:"back-path"})],key:"backPath",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"backCallback",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:String})],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"tabs",value(){return[]}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"hideFilterMenu",value(){return!1}},{kind:"field",decorators:[(0,r.IO)("ha-data-table",!0)],key:"_dataTable",value:void 0},{kind:"method",key:"clearSelection",value:function(){this._dataTable.clearSelection()}},{kind:"method",key:"render",value:function(){const e=this.numHidden?this.hiddenLabel||this.hass.localize("ui.components.data-table.hidden",{number:this.numHidden})||this.numHidden:void 0,t=this.activeFilters?o.dy`${this.hass.localize("ui.components.data-table.filtering_by")}
        ${this.activeFilters.join(", ")}
        ${e?`(${e})`:""}`:e,i=o.dy`<search-input
      .hass=${this.hass}
      .filter=${this.filter}
      .suffix=${!this.narrow}
      @value-changed=${this._handleSearchChange}
      .label=${this.searchLabel}
    >
      ${this.narrow?"":o.dy`<div
            class="filters"
            slot="suffix"
            @click=${this._preventDefault}
          >
            ${t?o.dy`<div class="active-filters">
                  ${t}
                  <mwc-button @click=${this._clearFilter}>
                    ${this.hass.localize("ui.components.data-table.clear")}
                  </mwc-button>
                </div>`:""}
            <slot name="filter-menu"></slot>
          </div>`}
    </search-input>`;return o.dy`
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
        ${this.hideFilterMenu?"":o.dy`
              <div slot="toolbar-icon">
                ${this.narrow?o.dy`
                      <div class="filter-menu">
                        ${this.numHidden||this.activeFilters?o.dy`<span class="badge"
                              >${this.numHidden||"!"}</span
                            >`:""}
                        <slot name="filter-menu"></slot>
                      </div>
                    `:""}<slot name="toolbar-icon"></slot>
              </div>
            `}
        ${this.narrow?o.dy`
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
          ${this.narrow?o.dy` <div slot="header"></div> `:o.dy`
                <div slot="header">
                  <slot name="header">
                    <div class="table-header">${i}</div>
                  </slot>
                </div>
              `}
        </ha-data-table>
        <div slot="fab"><slot name="fab"></slot></div>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_preventDefault",value:function(e){e.preventDefault()}},{kind:"method",key:"_handleSearchChange",value:function(e){this.filter!==e.detail.value&&(this.filter=e.detail.value,(0,n.B)(this,"search-changed",{value:this.filter}))}},{kind:"method",key:"_clearFilter",value:function(){(0,n.B)(this,"clear-filter")}},{kind:"get",static:!0,key:"styles",value:function(){return o.iv`
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
    `}}]}}),o.oi)},48223:(e,t,i)=>{i.r(t),i.d(t,{InsteonDevicesPanel:()=>k});var a=i(73958),o=i(565),r=i(47838),n=i(9644),s=i(36924),d=i(14516),l=(i(31007),i(99040),i(68336),i(85878),i(38122),i(29950)),c=i(51134),h=i(71155),u=i(87545),v=i(18394);const b=()=>Promise.all([i.e(5084),i.e(9663),i.e(9076)]).then(i.bind(i,59502)),p=()=>Promise.all([i.e(5084),i.e(9663),i.e(4347)]).then(i.bind(i,55159)),f=()=>Promise.all([i.e(5084),i.e(9663),i.e(3625)]).then(i.bind(i,10759));var m=i(8841),y=i(11285);let k=(0,a.Z)([(0,s.Mo)("insteon-devices-panel")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Object})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,s.Cb)({type:Array})],key:"_devices",value(){return[]}},{kind:"field",key:"_areas",value(){return[]}},{kind:"field",key:"_unsubs",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,r.Z)(i.prototype),"firstUpdated",this).call(this,e),this.hass&&this.insteon&&(this._unsubs||this._getDevices())}},{kind:"method",key:"updated",value:function(e){(0,o.Z)((0,r.Z)(i.prototype),"updated",this).call(this,e),this.hass&&this.insteon&&(this._unsubs||this._getDevices())}},{kind:"method",key:"disconnectedCallback",value:function(){if((0,o.Z)((0,r.Z)(i.prototype),"disconnectedCallback",this).call(this),this._unsubs){for(;this._unsubs.length;)this._unsubs.pop()();this._unsubs=void 0}}},{kind:"method",key:"_getDevices",value:function(){this.insteon&&this.hass&&(this._unsubs=[(0,u.sG)(this.hass.connection,(e=>{this._areas=e})),(0,c.q4)(this.hass.connection,(e=>{this._devices=e.filter((e=>e.config_entries&&e.config_entries.includes(this.insteon.config_entry.entry_id)))}))])}},{kind:"field",key:"_columns",value(){return(0,d.Z)((e=>e?{name:{title:this.insteon.localize("devices.fields.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0},address:{title:this.insteon.localize("devices.fields.address"),sortable:!0,filterable:!0,direction:"asc",width:"5hv"}}:{name:{title:this.insteon.localize("devices.fields.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0},address:{title:this.insteon.localize("devices.fields.address"),sortable:!0,filterable:!0,direction:"asc",width:"20%"},description:{title:this.insteon.localize("devices.fields.description"),sortable:!0,filterable:!0,direction:"asc",width:"15%"},model:{title:this.insteon.localize("devices.fields.model"),sortable:!0,filterable:!0,direction:"asc",width:"15%"},area:{title:this.insteon.localize("devices.fields.area"),sortable:!0,filterable:!0,direction:"asc",width:"15%"}}))}},{kind:"field",key:"_insteonDevices",value(){return(0,d.Z)((e=>{const t={};for(const i of this._areas)t[i.area_id]=i;return e.map((e=>{var i,a;return{id:e.id,name:e.name_by_user||e.name||"No device name",address:(null===(i=e.name)||void 0===i?void 0:i.substring(e.name.length-8))||"",description:(null===(a=e.name)||void 0===a?void 0:a.substring(0,e.name.length-8))||"",model:e.model||"",area:e.area_id?t[e.area_id].name:""}}))}))}},{kind:"method",key:"render",value:function(){return n.dy`
      <hass-tabs-subpage-data-table
        .hass=${this.hass}
        .narrow=${this.narrow}
        .tabs=${m.h}
        .route=${this.route}
        .data=${this._insteonDevices(this._devices)}
        .columns=${this._columns(this.narrow)}
        @row-click=${this._handleRowClicked}
        clickable
        .localizeFunc=${this.insteon.localize}
        .mainPage=${!0}
        .hasFab=${!0}
      >
        <ha-fab
          slot="fab"
          .label=${this.insteon.localize("devices.add_device")}
          extended
          @click=${this._addDevice}
        >
          <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage-data-table>
    `}},{kind:"method",key:"_addDevice",value:async function(){var e,t;e=this,t={hass:this.hass,insteon:this.insteon,title:this.insteon.localize("device.actions.add"),callback:async(e,t,i)=>this._handleDeviceAdd(e,t,i)},(0,v.B)(e,"show-dialog",{dialogTag:"dialog-insteon-add-device",dialogImport:b,dialogParams:t})}},{kind:"method",key:"_handleDeviceAdd",value:async function(e,t,i){if(i)return a=this,o={hass:this.hass,insteon:this.insteon,title:this.insteon.localize("device.add_x10.caption"),callback:async()=>this._handleX10DeviceAdd()},void(0,v.B)(a,"show-dialog",{dialogTag:"dialog-device-add-x10",dialogImport:f,dialogParams:o});var a,o;((e,t)=>{(0,v.B)(e,"show-dialog",{dialogTag:"dialog-insteon-adding-device",dialogImport:p,dialogParams:t})})(this,{hass:this.hass,insteon:this.insteon,multiple:t,address:e,title:this.insteon.localize("devices.adding_device")})}},{kind:"method",key:"_handleX10DeviceAdd",value:async function(){(0,y.Ys)(this,{title:this.insteon.localize("device.add_x10.caption"),text:this.insteon.localize("device.add_x10.success")})}},{kind:"method",key:"_handleRowClicked",value:async function(e){const t=e.detail.id;(0,h.c)("/insteon/device/properties/"+t)}},{kind:"get",static:!0,key:"styles",value:function(){return[n.iv`
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
        #fab {
          position: fixed;
          right: calc(16px + env(safe-area-inset-right));
          bottom: calc(16px + env(safe-area-inset-bottom));
          z-index: 1;
        }
        :host([narrow]) #fab.tabs {
          bottom: calc(84px + env(safe-area-inset-bottom));
        }
        #fab[is-wide] {
          bottom: 24px;
          right: 24px;
        }
        :host([rtl]) #fab {
          right: auto;
          left: calc(16px + env(safe-area-inset-left));
        }
        :host([rtl][is-wide]) #fab {
          bottom: 24px;
          left: 24px;
          right: auto;
        }
      `,l.Qx]}}]}}),n.oi)}}]);
//# sourceMappingURL=a374a01c.js.map