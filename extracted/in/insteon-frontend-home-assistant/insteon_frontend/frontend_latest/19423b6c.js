"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[6536],{85878:(e,i,t)=>{var s=t(73958),a=t(565),o=t(47838),n=(t(6294),t(9644)),d=t(36924),r=t(47509),l=t(15815);(0,s.Z)([(0,d.Mo)("ha-button-menu")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",key:l.gA,value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,d.Cb)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,d.Cb)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,d.Cb)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,d.Cb)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,d.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,i;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(i=this._triggerButton)||void 0===i||i.focus()}},{kind:"method",key:"render",value:function(){return n.dy`
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
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)((0,o.Z)(t.prototype),"firstUpdated",this).call(this,e),"rtl"===r.E.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const i=document.createElement("style");i.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(i)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),n.oi)},7006:(e,i,t)=>{var s=t(73958),a=t(565),o=t(47838),n=(t(34131),t(68262)),d=t(9644),r=t(36924);(0,s.Z)([(0,r.Mo)("ha-circular-progress")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,r.Cb)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,a.Z)((0,o.Z)(t.prototype),"updated",this).call(this,e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"get",static:!0,key:"styles",value:function(){return[...(0,a.Z)((0,o.Z)(t),"styles",this),d.iv`
        :host {
          --md-sys-color-primary: var(--primary-color);
          --md-circular-progress-size: 48px;
        }
      `]}}]}}),n.B)},99040:(e,i,t)=>{var s=t(73958),a=t(565),o=t(47838),n=t(48095),d=t(72477),r=t(36924),l=t(9644),c=t(47509);(0,s.Z)([(0,r.Mo)("ha-fab")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"method",key:"firstUpdated",value:function(e){(0,a.Z)((0,o.Z)(t.prototype),"firstUpdated",this).call(this,e),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}},{kind:"field",static:!0,key:"styles",value(){return[d.W,l.iv`
      :host .mdc-fab--extended .mdc-fab__icon {
        margin-inline-start: -8px;
        margin-inline-end: 12px;
        direction: var(--direction);
      }
    `,"rtl"===c.E.document.dir?l.iv`
          :host .mdc-fab--extended .mdc-fab__icon {
            direction: rtl;
          }
        `:l.iv``]}}]}}),n._)},11285:(e,i,t)=>{t.d(i,{D9:()=>r,Ys:()=>n,g7:()=>d});var s=t(18394);const a=()=>Promise.all([t.e(5084),t.e(4338)]).then(t.bind(t,44338)),o=(e,i,t)=>new Promise((o=>{const n=i.cancel,d=i.confirm;(0,s.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:a,dialogParams:{...i,...t,cancel:()=>{o(!(null==t||!t.prompt)&&null),n&&n()},confirm:e=>{o(null==t||!t.prompt||e),d&&d(e)}}})})),n=(e,i)=>o(e,i),d=(e,i)=>o(e,i,{confirmation:!0}),r=(e,i)=>o(e,i,{prompt:!0})},13343:(e,i,t)=>{t.d(i,{CL:()=>y,CN:()=>u,Co:()=>a,Cy:()=>n,DT:()=>k,GU:()=>m,Ho:()=>w,Jz:()=>p,KJ:()=>g,N2:()=>r,NC:()=>o,NL:()=>h,Qs:()=>l,SL:()=>d,WM:()=>f,di:()=>v,rW:()=>b,tw:()=>c,yq:()=>_,zM:()=>s});const s=(e,i)=>e.callWS({type:"insteon/device/get",device_id:i}),a=(e,i)=>e.callWS({type:"insteon/aldb/get",device_address:i}),o=(e,i,t)=>e.callWS({type:"insteon/properties/get",device_address:i,show_advanced:t}),n=(e,i,t)=>e.callWS({type:"insteon/aldb/change",device_address:i,record:t}),d=(e,i,t,s)=>e.callWS({type:"insteon/properties/change",device_address:i,name:t,value:s}),r=(e,i,t)=>e.callWS({type:"insteon/aldb/create",device_address:i,record:t}),l=(e,i)=>e.callWS({type:"insteon/aldb/load",device_address:i}),c=(e,i)=>e.callWS({type:"insteon/properties/load",device_address:i}),h=(e,i)=>e.callWS({type:"insteon/aldb/write",device_address:i}),u=(e,i)=>e.callWS({type:"insteon/properties/write",device_address:i}),m=(e,i)=>e.callWS({type:"insteon/aldb/reset",device_address:i}),v=(e,i)=>e.callWS({type:"insteon/properties/reset",device_address:i}),_=(e,i)=>e.callWS({type:"insteon/aldb/add_default_links",device_address:i}),y=e=>[{name:"mode",options:[["c",e.localize("aldb.mode.controller")],["r",e.localize("aldb.mode.responder")]],required:!0,type:"select"},{name:"group",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"target",required:!0,type:"string"},{name:"data1",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data2",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data3",required:!0,type:"integer",valueMin:-1,valueMax:255}],k=e=>[{name:"in_use",required:!0,type:"boolean"},...y(e)],p=(e,i)=>[{name:"multiple",required:!1,type:i?"constant":"boolean"},{name:"add_x10",required:!1,type:e?"constant":"boolean"},{name:"device_address",required:!1,type:e||i?"constant":"string"}],b=e=>e.callWS({type:"insteon/device/add/cancel"}),f=(e,i,t)=>e.callWS({type:"insteon/device/remove",device_address:i,remove_all_refs:t}),g=(e,i)=>e.callWS({type:"insteon/device/add_x10",x10_device:i}),w={name:"ramp_rate",options:[["31","0.1"],["30","0.2"],["29","0.3"],["28","0.5"],["27","2"],["26","4.5"],["25","6.5"],["24","8.5"],["23","19"],["22","21.5"],["21","23.5"],["20","26"],["19","28"],["18","30"],["17","32"],["16","34"],["15","38.5"],["14","43"],["13","47"],["12","60"],["11","90"],["10","120"],["9","150"],["8","180"],["7","210"],["6","240"],["5","270"],["4","300"],["3","360"],["2","420"],["1","480"]],required:!0,type:"select"}},8502:(e,i,t)=>{var s=t(73958),a=t(9644),o=t(36924),n=t(14516),d=(t(7006),t(31007),t(51750));(0,s.Z)([(0,o.Mo)("insteon-aldb-data-table")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"records",value(){return[]}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"isLoading",value(){return!1}},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"showWait",value(){return!1}},{kind:"field",key:"_records",value(){return(0,n.Z)((e=>{if(!e)return[];return e.map((e=>({...e})))}))}},{kind:"field",key:"_columns",value(){return(0,n.Z)((e=>e?{in_use:{title:this.insteon.localize("aldb.fields.in_use"),template:e=>e.in_use?a.dy`${this.hass.localize("ui.common.yes")}`:a.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"15%"},dirty:{title:this.insteon.localize("aldb.fields.modified"),template:e=>e.dirty?a.dy`${this.hass.localize("ui.common.yes")}`:a.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"15%"},target:{title:this.insteon.localize("aldb.fields.target"),sortable:!0,grows:!0},group:{title:this.insteon.localize("aldb.fields.group"),sortable:!0,width:"15%"},is_controller:{title:this.insteon.localize("aldb.fields.mode"),template:e=>e.is_controller?a.dy`${this.insteon.localize("aldb.mode.controller")}`:a.dy`${this.insteon.localize("aldb.mode.responder")}`,sortable:!0,width:"25%"}}:{mem_addr:{title:this.insteon.localize("aldb.fields.id"),template:e=>e.mem_addr<0?a.dy`New`:a.dy`${e.mem_addr}`,sortable:!0,direction:"desc",width:"10%"},in_use:{title:this.insteon.localize("aldb.fields.in_use"),template:e=>e.in_use?a.dy`${this.hass.localize("ui.common.yes")}`:a.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"10%"},dirty:{title:this.insteon.localize("aldb.fields.modified"),template:e=>e.dirty?a.dy`${this.hass.localize("ui.common.yes")}`:a.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"10%"},target:{title:this.insteon.localize("aldb.fields.target"),sortable:!0,width:"15%"},target_name:{title:this.insteon.localize("aldb.fields.target_device"),sortable:!0,grows:!0},group:{title:this.insteon.localize("aldb.fields.group"),sortable:!0,width:"10%"},is_controller:{title:this.insteon.localize("aldb.fields.mode"),template:e=>e.is_controller?a.dy`${this.insteon.localize("aldb.mode.controller")}`:a.dy`${this.insteon.localize("aldb.mode.responder")}`,sortable:!0,width:"12%"}}))}},{kind:"method",key:"_noDataText",value:function(e){return e?"":this.insteon.localize("aldb.no_data")}},{kind:"method",key:"render",value:function(){return this.showWait?a.dy`
        <ha-circular-progress active alt="Loading"></ha-circular-progress>
      `:a.dy`
      <ha-data-table
        .hass=${this.hass}
        .columns=${this._columns(this.narrow)}
        .data=${this._records(this.records)}
        .id=${"mem_addr"}
        .dir=${(0,d.Zu)(this.hass)}
        .searchLabel=${this.hass.localize("ui.components.data-table.search")}
        .noDataText="${this._noDataText(this.isLoading)}"
      >
        <ha-circular-progress active alt="Loading"></ha-circular-progress>
      </ha-data-table>
    `}}]}}),a.oi)},26536:(e,i,t)=>{t.r(i);var s=t(73958),a=t(565),o=t(47838),n=(t(30437),t(54371),t(7006),t(9644)),d=t(36924),r=t(8636),l=(t(99040),t(13343)),c=(t(40841),t(68395)),h=(t(8502),t(11285)),u=t(18394);const m=()=>Promise.all([t.e(5084),t.e(9663),t.e(1961)]).then(t.bind(t,44843)),v=(e,i)=>{(0,u.B)(e,"show-dialog",{dialogTag:"dialog-insteon-aldb-record",dialogImport:m,dialogParams:i})};var _=t(71155),y=(t(85878),t(29950));(0,s.Z)([(0,d.Mo)("insteon-device-aldb-page")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,d.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,d.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,d.Cb)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_device",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_records",value:void 0},{kind:"field",decorators:[(0,d.SB)()],key:"_allRecords",value(){return[]}},{kind:"field",decorators:[(0,d.SB)()],key:"_showHideUnused",value(){return"show"}},{kind:"field",decorators:[(0,d.SB)()],key:"_showUnused",value(){return!1}},{kind:"field",decorators:[(0,d.SB)()],key:"_isLoading",value(){return!1}},{kind:"field",key:"_subscribed",value:void 0},{kind:"field",key:"_refreshDevicesTimeoutHandle",value:void 0},{kind:"field",key:"_showUnusedAvailable",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(e){var i;(console.info("Device GUID: "+this.deviceId+" in aldb"),(0,a.Z)((0,o.Z)(t.prototype),"firstUpdated",this).call(this,e),this.deviceId&&this.hass)&&(this._showUnusedAvailable=Boolean(null===(i=this.hass.userData)||void 0===i?void 0:i.showAdvanced),(0,l.zM)(this.hass,this.deviceId).then((e=>{this._device=e,this._getRecords()}),(()=>{this._noDeviceError()})))}},{kind:"method",key:"disconnectedCallback",value:function(){(0,a.Z)((0,o.Z)(t.prototype),"disconnectedCallback",this).call(this),this._unsubscribe()}},{kind:"method",key:"_dirty",value:function(){var e;return null===(e=this._records)||void 0===e?void 0:e.reduce(((e,i)=>e||i.dirty),!1)}},{kind:"method",key:"_filterRecords",value:function(e){return e.filter((e=>e.in_use||this._showUnused&&this._showUnusedAvailable||e.dirty))}},{kind:"method",key:"render",value:function(){var e,i,t;return n.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${c.insteonDeviceTabs}
        .localizeFunc=${this.insteon.localize}
        .backCallback=${()=>this._handleBackTapped()}
        hasFab
      >
        ${this.narrow?n.dy`
            <div slot="header" class="header fullwidth">
              <div slot="header" class="narrow-header-left">
                ${null===(e=this._device)||void 0===e?void 0:e.name}
              </div>
              <div slot="header" class="narrow-header-right">
                  ${this._generateActionMenu()}
              </div>
            </div>
            `:""}
        <div class="container">
          ${this.narrow?"":n.dy`
                <div class="page-header fullwidth">
                  <table>
                    <tr>
                      <td>
                        <div class="device-name">
                          <h1>${null===(i=this._device)||void 0===i?void 0:i.name}</h1>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td>
                        <div class="aldb-status">
                          ALDB Status:
                          ${this._device?this.insteon.localize("aldb.status."+(null===(t=this._device)||void 0===t?void 0:t.aldb_status)):""}
                        </div>
                        </td>
                    </tr>
                  </table>
                  <div class="logo header-right">
                    <img
                      src="https://brands.home-assistant.io/insteon/logo.png"
                      referrerpolicy="no-referrer"
                      @load=${this._onImageLoad}
                      @error=${this._onImageError}
                    />
                        ${this._generateActionMenu()}
                  </div>
                </div>
              `}
          <insteon-aldb-data-table
            .insteon=${this.insteon}
            .hass=${this.hass}
            .narrow=${this.narrow}
            .records=${this._records}
            @row-click=${this._handleRowClicked}
            .isLoading=${this._isLoading}
          ></insteon-aldb-data-table>
        </div>
        <ha-fab
          slot="fab"
          .title="${this.insteon.localize("aldb.actions.create")}"
          .label="${this.insteon.localize("aldb.actions.create")}"
          @click=${this._createRecord}
          .extended=${!this.narrow}
        >
          <ha-svg-icon slot="icon" path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
        </ha-fab>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_generateActionMenu",value:function(){return n.dy`
      <ha-button-menu
        corner="BOTTOM_START"
        @action=${this._handleMenuAction}
        activatable
        >
        <ha-icon-button
          slot="trigger"
          .label=${this.hass.localize("ui.common.menu")}
          .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
        ></ha-icon-button>
        <mwc-list-item>
          ${this.insteon.localize("common.actions.load")}
        </mwc-list-item>
        <mwc-list-item>
          ${this.insteon.localize("aldb.actions.add_default_links")}
        </mwc-list-item>
        <mwc-list-item .disabled=${!this._dirty()}>
          ${this.insteon.localize("common.actions.write")}
        </mwc-list-item>
        <mwc-list-item .disabled=${!this._dirty()}>
          ${this.insteon.localize("common.actions.reset")}
        </mwc-list-item>

        <mwc-list-item
          aria-label=${this.insteon.localize("device.actions.delete")}
          class=${(0,r.$)({warning:!0})}
        >
          ${this.insteon.localize("device.actions.delete")}
        </mwc-list-item>

        ${this._showUnusedAvailable?n.dy`
            <mwc-list-item>
              ${this.insteon.localize("aldb.actions."+this._showHideUnused)}
            </mwc-list-item>`:""}
      </ha-button-menu>
    `}},{kind:"method",key:"_getRecords",value:function(){var e;this._device?(0,l.Co)(this.hass,null===(e=this._device)||void 0===e?void 0:e.address).then((e=>{this._allRecords=e,this._records=this._filterRecords(this._allRecords)})):this._records=[]}},{kind:"method",key:"_createRecord",value:function(){v(this,{hass:this.hass,insteon:this.insteon,schema:(0,l.CL)(this.insteon),record:{mem_addr:0,in_use:!0,is_controller:!0,highwater:!1,group:0,target:"",target_name:"",data1:0,data2:0,data3:0,dirty:!0},title:this.insteon.localize("aldb.actions.new"),callback:async e=>this._handleRecordCreate(e)})}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.display="inline-block"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.display="none"}},{kind:"method",key:"_onLoadALDBClick",value:async function(){await(0,h.g7)(this,{text:this.insteon.localize("common.warn.load"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._load()})}},{kind:"method",key:"_load",value:async function(){this._device.is_battery&&await(0,h.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._subscribe(),(0,l.Qs)(this.hass,this._device.address),this._isLoading=!0,this._records=[]}},{kind:"method",key:"_onShowHideUnusedClicked",value:async function(){this._showUnused=!this._showUnused,this._showUnused?this._showHideUnused="hide":this._showHideUnused="show",this._records=this._filterRecords(this._allRecords)}},{kind:"method",key:"_onWriteALDBClick",value:async function(){await(0,h.g7)(this,{text:this.insteon.localize("common.warn.write"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._write()})}},{kind:"method",key:"_write",value:async function(){this._device.is_battery&&await(0,h.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._subscribe(),(0,l.NL)(this.hass,this._device.address),this._isLoading=!0,this._records=[]}},{kind:"method",key:"_onDeleteDevice",value:async function(){await(0,h.g7)(this,{text:this.insteon.localize("common.warn.delete"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._checkScope(),warning:!0})}},{kind:"method",key:"_delete",value:async function(e){await(0,l.WM)(this.hass,this._device.address,e),(0,_.c)("/insteon")}},{kind:"method",key:"_checkScope",value:async function(){if(this._device.address.includes("X10"))return void this._delete(!1);const e=await(0,h.g7)(this,{title:this.insteon.localize("device.remove_all_refs.title"),text:n.dy`
        ${this.insteon.localize("device.remove_all_refs.description")}<br><br>
        ${this.insteon.localize("device.remove_all_refs.confirm_description")}<br>
        ${this.insteon.localize("device.remove_all_refs.dismiss_description")}`,confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),warning:!0,destructive:!0});this._delete(e)}},{kind:"method",key:"_onResetALDBClick",value:async function(){(0,l.GU)(this.hass,this._device.address),this._getRecords()}},{kind:"method",key:"_onAddDefaultLinksClicked",value:async function(){await(0,h.g7)(this,{text:this.insteon.localize("common.warn.add_default_links"),confirm:async()=>this._addDefaultLinks()})}},{kind:"method",key:"_addDefaultLinks",value:async function(){this._device.is_battery&&await(0,h.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._subscribe(),(0,l.yq)(this.hass,this._device.address),this._records=[]}},{kind:"method",key:"_handleRecordChange",value:async function(e){(0,l.Cy)(this.hass,this._device.address,e),this._getRecords()}},{kind:"method",key:"_handleRecordCreate",value:async function(e){(0,l.N2)(this.hass,this._device.address,e),this._getRecords()}},{kind:"method",key:"_handleRowClicked",value:async function(e){const i=e.detail.id,t=this._records.find((e=>e.mem_addr===+i));v(this,{hass:this.hass,insteon:this.insteon,schema:(0,l.DT)(this.insteon),record:t,title:this.insteon.localize("aldb.actions.change"),callback:async e=>this._handleRecordChange(e)}),history.back()}},{kind:"method",key:"_handleBackTapped",value:async function(){this._dirty()?await(0,h.g7)(this,{text:this.insteon.localize("common.warn.unsaved"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._goBack()}):(0,_.c)("/insteon/devices")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:await this._onLoadALDBClick();break;case 1:await this._onAddDefaultLinksClicked();break;case 2:await this._onWriteALDBClick();break;case 3:await this._onResetALDBClick();break;case 4:await this._onDeleteDevice();break;case 5:await this._onShowHideUnusedClicked()}}},{kind:"method",key:"_goBack",value:function(){(0,l.GU)(this.hass,this._device.address),(0,_.c)("/insteon/devices")}},{kind:"method",key:"_handleMessage",value:function(e){"record_loaded"===e.type&&this._getRecords(),"status_changed"===e.type&&((0,l.zM)(this.hass,this.deviceId).then((e=>{this._device=e})),this._isLoading=e.is_loading,e.is_loading||this._unsubscribe())}},{kind:"method",key:"_unsubscribe",value:function(){this._refreshDevicesTimeoutHandle&&clearTimeout(this._refreshDevicesTimeoutHandle),this._subscribed&&(this._subscribed.then((e=>e())),this._subscribed=void 0)}},{kind:"method",key:"_subscribe",value:function(){var e;this.hass&&(this._subscribed=this.hass.connection.subscribeMessage((e=>this._handleMessage(e)),{type:"insteon/aldb/notify",device_address:null===(e=this._device)||void 0===e?void 0:e.address}),this._refreshDevicesTimeoutHandle=window.setTimeout((()=>this._unsubscribe()),12e5))}},{kind:"method",key:"_noDeviceError",value:function(){(0,h.Ys)(this,{text:this.insteon.localize("common.error.device_not_found")}),this._goBack(),this._goBack()}},{kind:"get",static:!0,key:"styles",value:function(){return[y.Qx,n.iv`
        :host {
          --app-header-background-color: var(--sidebar-background-color);
          --app-header-text-color: var(--sidebar-text-color);
          --app-header-border-bottom: 1px solid var(--divider-color);
        }

        :host([narrow]) {
          --aldb-table-height: 86vh;
        }

        :host(:not([narrow])) {
          --aldb-table-height: 90vh;
        }

        .header {
          display: flex;
          justify-content: space-between;
        }

        .container {
          display: flex;
          flex-wrap: wrap;
          margin: 0px;
        }

        insteon-aldb-data-table {
          width: 100%;
          height: var(--aldb-table-height);
          display: block;
          --data-table-border-width: 0;
        }
        .device-name {
          display: block;
          align-items: left;
          padding-left: 0px;
          padding-inline-start: 0px;
          direction: var(--direction);
          font-size: 24px;
          position: relative;
          width: 100%;
          height: 50%;
        }
        .aldb-status {
          position: relative;
          display: block;
        }
        h1 {
          margin: 0;
          font-family: var(--paper-font-headline_-_font-family);
          -webkit-font-smoothing: var(
            --paper-font-headline_-_-webkit-font-smoothing
          );
          font-size: var(--paper-font-headline_-_font-size);
          font-weight: var(--paper-font-headline_-_font-weight);
          letter-spacing: var(--paper-font-headline_-_letter-spacing);
          line-height: var(--paper-font-headline_-_line-height);
          opacity: var(--dark-primary-opacity);
        }

        .page-header {
          padding: 8px;
          margin-left: 32px;
          margin-right: 32px;
          display: flex;
          justify-content: space-between;
        }

        .fullwidth {
          padding: 8px;
          box-sizing: border-box;
          width: 100%;
          flex-grow: 1;
        }

        .header-right {
          align-self: right;
          display: flex;
        }

        .header-right img {
          height: 30px;
        }

        .header-right:first-child {
          width: 100%;
          justify-content: flex-end;
        }

        .actions mwc-button {
          margin: 8px;
        }

        :host([narrow]) .container {
          margin-top: 0;
        }

        .narrow-header-left {
          padding: 8px;
          width: 90%;
        }
        .narrow-header-right {
          align-self: right;
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=19423b6c.js.map