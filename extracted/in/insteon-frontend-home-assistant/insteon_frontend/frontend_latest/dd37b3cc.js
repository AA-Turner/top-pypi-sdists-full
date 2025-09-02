"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[969],{85878:(e,i,t)=>{var s=t(73958),o=t(565),a=t(47838),n=(t(6294),t(9644)),r=t(36924),d=t(47509),l=t(15815);(0,s.Z)([(0,r.Mo)("ha-button-menu")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",key:l.gA,value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"corner",value(){return"BOTTOM_START"}},{kind:"field",decorators:[(0,r.Cb)()],key:"menuCorner",value(){return"START"}},{kind:"field",decorators:[(0,r.Cb)({type:Number})],key:"x",value(){return null}},{kind:"field",decorators:[(0,r.Cb)({type:Number})],key:"y",value(){return null}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"multi",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"activatable",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"fixed",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,attribute:"no-anchor"})],key:"noAnchor",value(){return!1}},{kind:"field",decorators:[(0,r.IO)("mwc-menu",!0)],key:"_menu",value:void 0},{kind:"get",key:"items",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.items}},{kind:"get",key:"selected",value:function(){var e;return null===(e=this._menu)||void 0===e?void 0:e.selected}},{kind:"method",key:"focus",value:function(){var e,i;null!==(e=this._menu)&&void 0!==e&&e.open?this._menu.focusItemAtIndex(0):null===(i=this._triggerButton)||void 0===i||i.focus()}},{kind:"method",key:"render",value:function(){return n.dy`
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
    `}},{kind:"method",key:"firstUpdated",value:function(e){(0,o.Z)((0,a.Z)(t.prototype),"firstUpdated",this).call(this,e),"rtl"===d.E.document.dir&&this.updateComplete.then((()=>{this.querySelectorAll("mwc-list-item").forEach((e=>{const i=document.createElement("style");i.innerHTML="span.material-icons:first-of-type { margin-left: var(--mdc-list-item-graphic-margin, 32px) !important; margin-right: 0px !important;}",e.shadowRoot.appendChild(i)}))}))}},{kind:"method",key:"_handleClick",value:function(){this.disabled||(this._menu.anchor=this.noAnchor?null:this,this._menu.show())}},{kind:"get",key:"_triggerButton",value:function(){return this.querySelector('ha-icon-button[slot="trigger"], mwc-button[slot="trigger"]')}},{kind:"method",key:"_setTriggerAria",value:function(){this._triggerButton&&(this._triggerButton.ariaHasPopup="menu")}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      :host {
        display: inline-block;
        position: relative;
      }
      ::slotted([disabled]) {
        color: var(--disabled-text-color);
      }
    `}}]}}),n.oi)},7006:(e,i,t)=>{var s=t(73958),o=t(565),a=t(47838),n=(t(34131),t(68262)),r=t(9644),d=t(36924);(0,s.Z)([(0,d.Mo)("ha-circular-progress")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,d.Cb)({attribute:"aria-label",type:String})],key:"ariaLabel",value(){return"Loading"}},{kind:"field",decorators:[(0,d.Cb)()],key:"size",value(){return"medium"}},{kind:"method",key:"updated",value:function(e){if((0,o.Z)((0,a.Z)(t.prototype),"updated",this).call(this,e),e.has("size"))switch(this.size){case"tiny":this.style.setProperty("--md-circular-progress-size","16px");break;case"small":this.style.setProperty("--md-circular-progress-size","28px");break;case"medium":this.style.setProperty("--md-circular-progress-size","48px");break;case"large":this.style.setProperty("--md-circular-progress-size","68px")}}},{kind:"get",static:!0,key:"styles",value:function(){return[...(0,o.Z)((0,a.Z)(t),"styles",this),r.iv`
        :host {
          --md-sys-color-primary: var(--primary-color);
          --md-circular-progress-size: 48px;
        }
      `]}}]}}),n.B)},11285:(e,i,t)=>{t.d(i,{D9:()=>d,Ys:()=>n,g7:()=>r});var s=t(18394);const o=()=>Promise.all([t.e(5084),t.e(4338)]).then(t.bind(t,44338)),a=(e,i,t)=>new Promise((a=>{const n=i.cancel,r=i.confirm;(0,s.B)(e,"show-dialog",{dialogTag:"dialog-box",dialogImport:o,dialogParams:{...i,...t,cancel:()=>{a(!(null==t||!t.prompt)&&null),n&&n()},confirm:e=>{a(null==t||!t.prompt||e),r&&r(e)}}})})),n=(e,i)=>a(e,i),r=(e,i)=>a(e,i,{confirmation:!0}),d=(e,i)=>a(e,i,{prompt:!0})},13343:(e,i,t)=>{t.d(i,{CL:()=>y,CN:()=>u,Co:()=>o,Cy:()=>n,DT:()=>k,GU:()=>p,Ho:()=>w,Jz:()=>_,KJ:()=>b,N2:()=>d,NC:()=>a,NL:()=>h,Qs:()=>l,SL:()=>r,WM:()=>g,di:()=>m,rW:()=>f,tw:()=>c,yq:()=>v,zM:()=>s});const s=(e,i)=>e.callWS({type:"insteon/device/get",device_id:i}),o=(e,i)=>e.callWS({type:"insteon/aldb/get",device_address:i}),a=(e,i,t)=>e.callWS({type:"insteon/properties/get",device_address:i,show_advanced:t}),n=(e,i,t)=>e.callWS({type:"insteon/aldb/change",device_address:i,record:t}),r=(e,i,t,s)=>e.callWS({type:"insteon/properties/change",device_address:i,name:t,value:s}),d=(e,i,t)=>e.callWS({type:"insteon/aldb/create",device_address:i,record:t}),l=(e,i)=>e.callWS({type:"insteon/aldb/load",device_address:i}),c=(e,i)=>e.callWS({type:"insteon/properties/load",device_address:i}),h=(e,i)=>e.callWS({type:"insteon/aldb/write",device_address:i}),u=(e,i)=>e.callWS({type:"insteon/properties/write",device_address:i}),p=(e,i)=>e.callWS({type:"insteon/aldb/reset",device_address:i}),m=(e,i)=>e.callWS({type:"insteon/properties/reset",device_address:i}),v=(e,i)=>e.callWS({type:"insteon/aldb/add_default_links",device_address:i}),y=e=>[{name:"mode",options:[["c",e.localize("aldb.mode.controller")],["r",e.localize("aldb.mode.responder")]],required:!0,type:"select"},{name:"group",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"target",required:!0,type:"string"},{name:"data1",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data2",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data3",required:!0,type:"integer",valueMin:-1,valueMax:255}],k=e=>[{name:"in_use",required:!0,type:"boolean"},...y(e)],_=(e,i)=>[{name:"multiple",required:!1,type:i?"constant":"boolean"},{name:"add_x10",required:!1,type:e?"constant":"boolean"},{name:"device_address",required:!1,type:e||i?"constant":"string"}],f=e=>e.callWS({type:"insteon/device/add/cancel"}),g=(e,i,t)=>e.callWS({type:"insteon/device/remove",device_address:i,remove_all_refs:t}),b=(e,i)=>e.callWS({type:"insteon/device/add_x10",x10_device:i}),w={name:"ramp_rate",options:[["31","0.1"],["30","0.2"],["29","0.3"],["28","0.5"],["27","2"],["26","4.5"],["25","6.5"],["24","8.5"],["23","19"],["22","21.5"],["21","23.5"],["20","26"],["19","28"],["18","30"],["17","32"],["16","34"],["15","38.5"],["14","43"],["13","47"],["12","60"],["11","90"],["10","120"],["9","150"],["8","180"],["7","210"],["6","240"],["5","270"],["4","300"],["3","360"],["2","420"],["1","480"]],required:!0,type:"select"}},90969:(e,i,t)=>{t.r(i);var s=t(73958),o=t(565),a=t(47838),n=(t(30437),t(9644)),r=t(36924),d=t(8636),l=(t(54371),t(14516)),c=(t(7006),t(31007),t(51750));(0,s.Z)([(0,r.Mo)("insteon-properties-data-table")],(function(e,i){return{F:class extends i{constructor(...i){super(...i),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"narrow",value(){return!1}},{kind:"field",decorators:[(0,r.Cb)({type:Array})],key:"records",value(){return[]}},{kind:"field",decorators:[(0,r.Cb)()],key:"schema",value(){return{}}},{kind:"field",decorators:[(0,r.Cb)()],key:"noDataText",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"showWait",value(){return!1}},{kind:"field",key:"_records",value(){return(0,l.Z)((e=>e.map((e=>({description:this._calcDescription(e.name),display_value:this._translateValue(e.name,e.value),...e})))))}},{kind:"method",key:"_calcDescription",value:function(e){return e.startsWith("toggle_")?this.insteon.localize("properties.descriptions.button")+" "+this._calcButtonName(e)+" "+this.insteon.localize("properties.descriptions.toggle"):e.startsWith("radio_button_group_")?this.insteon.localize("properties.descriptions.radio_button_group")+" "+this._calcButtonName(e):this.insteon.localize("properties.descriptions."+e)}},{kind:"method",key:"_calcButtonName",value:function(e){return e.endsWith("main")?this.insteon.localize("properties.descriptions.main"):e.substr(-1,1).toUpperCase()}},{kind:"field",key:"_columns",value(){return(0,l.Z)((e=>e?{name:{title:this.insteon.localize("properties.fields.name"),sortable:!0,grows:!0},modified:{title:this.insteon.localize("properties.fields.modified"),template:e=>e.modified?n.dy`${this.hass.localize("ui.common.yes")}`:n.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"20%"},display_value:{title:this.insteon.localize("properties.fields.value"),sortable:!0,width:"20%"}}:{name:{title:this.insteon.localize("properties.fields.name"),sortable:!0,width:"20%"},description:{title:this.insteon.localize("properties.fields.description"),sortable:!0,grows:!0},modified:{title:this.insteon.localize("properties.fields.modified"),template:e=>e.modified?n.dy`${this.hass.localize("ui.common.yes")}`:n.dy`${this.hass.localize("ui.common.no")}`,sortable:!0,width:"20%"},display_value:{title:this.insteon.localize("properties.fields.value"),sortable:!0,width:"20%"}}))}},{kind:"method",key:"render",value:function(){return this.showWait?n.dy`
        <ha-circular-progress
          class="fullwidth"
          active
          alt="Loading"
        ></ha-circular-progress>
      `:n.dy`
      <ha-data-table
        .hass=${this.hass}
        .columns=${this._columns(this.narrow)}
        .data=${this._records(this.records)}
        .id=${"name"}
        .dir=${(0,c.Zu)(this.hass)}
        noDataText="${this.noDataText}"
      ></ha-data-table>
    `}},{kind:"method",key:"_translateValue",value:function(e,i){const t=this.schema[e];if("radio_button_groups"==t.name)return i.length+" groups";if("multi_select"===t.type&&Array.isArray(i))return i.map((e=>t.options[e])).join(", ");if("select"===t.type){var s;return(null===(s=t.options)||void 0===s?void 0:s.reduce(((e,i)=>({...e,[i[0]]:i[1]})),{}))[i.toString()]}return i}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
      ha-circular-progress {
        align-items: center;
        justify-content: center;
        padding: 8px;
        box-sizing: border-box;
        width: 100%;
        flex-grow: 1;
      }
    `}}]}}),n.oi);var h=t(13343),u=t(18394);const p=()=>Promise.all([t.e(5084),t.e(9663),t.e(4507)]).then(t.bind(t,69546));var m=t(11285),v=(t(40841),t(68395)),y=t(71155),k=(t(85878),t(29950));(0,s.Z)([(0,r.Mo)("insteon-device-properties-page")],(function(e,i){class t extends i{constructor(...i){super(...i),e(this)}}return{F:t,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Object})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"deviceId",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_device",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_properties",value(){return[]}},{kind:"field",decorators:[(0,r.SB)()],key:"_schema",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_showWait",value(){return!1}},{kind:"field",decorators:[(0,r.SB)()],key:"_showAdvanced",value(){return!1}},{kind:"field",key:"_showHideAdvanced",value(){return"show"}},{kind:"field",key:"_advancedAvailable",value(){return!1}},{kind:"method",key:"firstUpdated",value:function(e){var i;((0,o.Z)((0,a.Z)(t.prototype),"firstUpdated",this).call(this,e),this.deviceId&&this.hass)&&(this._advancedAvailable=Boolean(null===(i=this.hass.userData)||void 0===i?void 0:i.showAdvanced),(0,h.zM)(this.hass,this.deviceId).then((e=>{this._device=e,this._getProperties()}),(()=>{this._noDeviceError()})))}},{kind:"method",key:"_dirty",value:function(){var e;return null===(e=this._properties)||void 0===e?void 0:e.reduce(((e,i)=>e||i.modified),!1)}},{kind:"method",key:"render",value:function(){var e,i;return n.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${v.insteonDeviceTabs}
        .localizeFunc=${this.insteon.localize}
        .backCallback=${async()=>this._handleBackTapped()}
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
                    <div></div>
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

          </div>
          <insteon-properties-data-table
            .hass=${this.hass}
            .insteon=${this.insteon}
            .narrow=${this.narrow}
            .records=${this._properties}
            .schema=${this._schema}
            noDataText=${this.insteon.localize("properties.no_data")}
            @row-click=${this._handleRowClicked}
            .showWait=${this._showWait}
          ></insteon-properties-data-table>
        </div>
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

        <!-- 0 -->
        <mwc-list-item>
          ${this.insteon.localize("common.actions.load")}
        </mwc-list-item>

        <!-- 1 -->
        <mwc-list-item .disabled=${!this._dirty()}>
          ${this.insteon.localize("common.actions.write")}
        </mwc-list-item>

        <!-- 2 -->
        <mwc-list-item .disabled=${!this._dirty()}>
          ${this.insteon.localize("common.actions.reset")}
        </mwc-list-item>

        <!-- 3 -->
        <mwc-list-item
          aria-label=${this.insteon.localize("device.actions.delete")}
          class=${(0,d.$)({warning:!0})}
        >
        ${this.insteon.localize("device.actions.delete")}
      </mwc-list-item>

        <!-- 4 -->
        ${this._advancedAvailable?n.dy`<mwc-list-item>
            ${this.insteon.localize("properties.actions."+this._showHideAdvanced)}
          </mwc-list-item>`:""}
      </ha-button-menu>
    `}},{kind:"method",key:"_onImageLoad",value:function(e){e.target.style.display="inline-block"}},{kind:"method",key:"_onImageError",value:function(e){e.target.style.display="none"}},{kind:"method",key:"_onLoadPropertiesClick",value:async function(){await(0,m.g7)(this,{text:this.insteon.localize("common.warn.load"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._load()})}},{kind:"method",key:"_load",value:async function(){this._device.is_battery&&await(0,m.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._showWait=!0;try{await(0,h.tw)(this.hass,this._device.address)}catch(e){(0,m.Ys)(this,{text:this.insteon.localize("common.error.load"),confirmText:this.hass.localize("ui.common.close")})}this._showWait=!1}},{kind:"method",key:"_onDeleteDevice",value:async function(){await(0,m.g7)(this,{text:this.insteon.localize("common.warn.delete"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._checkScope(),warning:!0})}},{kind:"method",key:"_delete",value:async function(e){await(0,h.WM)(this.hass,this._device.address,e),(0,y.c)("/insteon")}},{kind:"method",key:"_checkScope",value:async function(){if(this._device.address.includes("X10"))return void this._delete(!1);const e=await(0,m.g7)(this,{title:this.insteon.localize("device.remove_all_refs.title"),text:n.dy`
        ${this.insteon.localize("device.remove_all_refs.description")}<br><br>
        ${this.insteon.localize("device.remove_all_refs.confirm_description")}<br>
        ${this.insteon.localize("device.remove_all_refs.dismiss_description")}`,confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),warning:!0,destructive:!0});this._delete(e)}},{kind:"method",key:"_onWritePropertiesClick",value:async function(){await(0,m.g7)(this,{text:this.insteon.localize("common.warn.write"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:async()=>this._write()})}},{kind:"method",key:"_write",value:async function(){this._device.is_battery&&await(0,m.Ys)(this,{text:this.insteon.localize("common.warn.wake_up")}),this._showWait=!0;try{await(0,h.CN)(this.hass,this._device.address)}catch(e){(0,m.Ys)(this,{text:this.insteon.localize("common.error.write"),confirmText:this.hass.localize("ui.common.close")})}this._getProperties(),this._showWait=!1}},{kind:"method",key:"_getProperties",value:async function(){const e=await(0,h.NC)(this.hass,this._device.address,this._showAdvanced);console.info("Properties: "+e.properties.length),this._properties=e.properties,this._schema=this._translateSchema(e.schema)}},{kind:"method",key:"_onResetPropertiesClick",value:async function(){(0,h.di)(this.hass,this._device.address),this._getProperties()}},{kind:"method",key:"_handleRowClicked",value:async function(e){const i=e.detail.id,t=this._properties.find((e=>e.name===i)),s=this._schema[t.name];var o,a;o=this,a={hass:this.hass,insteon:this.insteon,schema:[s],record:t,title:this.insteon.localize("properties.actions.change"),callback:async(e,i)=>this._handlePropertyChange(e,i)},(0,u.B)(o,"show-dialog",{dialogTag:"dialog-insteon-property",dialogImport:p,dialogParams:a}),history.back()}},{kind:"method",key:"_handlePropertyChange",value:async function(e,i){await(0,h.SL)(this.hass,this._device.address,e,i),this._getProperties()}},{kind:"method",key:"_handleBackTapped",value:async function(){this._dirty()?await(0,m.g7)(this,{text:this.hass.localize("ui.panel.config.common.editor.confirm_unsaved"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),confirm:()=>this._goBack()}):(0,y.c)("/insteon/devices")}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:await this._onLoadPropertiesClick();break;case 1:await this._onWritePropertiesClick();break;case 2:await this._onResetPropertiesClick();break;case 3:await this._onDeleteDevice();break;case 4:await this._onShowHideAdvancedClicked()}}},{kind:"method",key:"_onShowHideAdvancedClicked",value:async function(){this._showAdvanced=!this._showAdvanced,this._showAdvanced?this._showHideAdvanced="hide":this._showHideAdvanced="show",this._getProperties()}},{kind:"method",key:"_goBack",value:function(){(0,h.di)(this.hass,this._device.address),(0,y.c)("/insteon/devices")}},{kind:"method",key:"_noDeviceError",value:function(){(0,m.Ys)(this,{text:this.insteon.localize("common.error.device_not_found")}),this._goBack()}},{kind:"method",key:"_translateSchema",value:function(e){const i={...e};return Object.entries(i).forEach((([e,i])=>{i.description||(i.description={}),i.description[e]=this.insteon.localize("properties.descriptions."+e),"multi_select"===i.type&&Object.entries(i.options).forEach((([e,t])=>{isNaN(+t)?i.options[e]=this.insteon.localize("properties.form_options."+t):i.options[e]=t})),"select"===i.type&&Object.entries(i.options).forEach((([e,[t,s]])=>{isNaN(+s)?i.options[e][1]=this.insteon.localize("properties.form_options."+s):i.options[e][1]=s}))})),e}},{kind:"get",static:!0,key:"styles",value:function(){return[k.Qx,n.iv`
        :host {
          --app-header-background-color: var(--sidebar-background-color);
          --app-header-text-color: var(--sidebar-text-color);
          --app-header-border-bottom: 1px solid var(--divider-color);
        }

        :host([narrow]) {
          --properties-table-height: 86vh;
        }

        :host(:not([narrow])) {
          --properties-table-height: 80vh;
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
        .device-name {
          display: flex;
          align-items: left;
          padding-left: 0px;
          padding-inline-start: 0px;
          direction: var(--direction);
          font-size: 24px;
        }
        insteon-properties-data-table {
          width: 100%;
          height: var(--properties-table-height);
          display: block;
          --data-table-border-width: 0;
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
          align-self: center;
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
//# sourceMappingURL=dd37b3cc.js.map