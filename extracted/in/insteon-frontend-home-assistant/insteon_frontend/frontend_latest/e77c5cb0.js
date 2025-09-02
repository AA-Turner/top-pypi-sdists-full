"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[3625],{86089:(e,t,i)=>{i.d(t,{U:()=>o});const o=e=>e.stopPropagation()},25799:(e,t,i)=>{var o=i(73958),r=i(565),a=i(47838),d=i(9644),n=i(36924),s=i(14516),l=i(18394),c=i(86089);const h={key:"Mod-s",run:e=>((0,l.B)(e.dom,"editor-save"),!0)},u=e=>{const t=document.createElement("ha-icon");return t.icon=e.label,t};(0,o.Z)([(0,n.Mo)("ha-code-editor")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"mode",value(){return"yaml"}},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"readOnly",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value(){return!1}},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"error",value(){return!1}},{kind:"field",decorators:[(0,n.SB)()],key:"_value",value(){return""}},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){(0,r.Z)((0,a.Z)(o.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",c.U),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.Z)((0,a.Z)(o.prototype),"disconnectedCallback",this).call(this),this.removeEventListener("keydown",c.U),this.updateComplete.then((()=>{this.codemirror.destroy(),delete this.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:async function(){var e;null!==(e=this._loadedCodeMirror)&&void 0!==e||(this._loadedCodeMirror=await Promise.all([i.e(8367),i.e(9146)]).then(i.bind(i,59146))),(0,r.Z)((0,a.Z)(o.prototype),"scheduleUpdate",this).call(this)}},{kind:"method",key:"update",value:function(e){if((0,r.Z)((0,a.Z)(o.prototype),"update",this).call(this,e),!this.codemirror)return void this._createCodeMirror();const t=[];e.has("mode")&&t.push({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&t.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&t.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),t.length>0&&this.codemirror.dispatch(...t),e.has("error")&&this.classList.toggle("error-state",this.error)}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,h]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate)];if(!this.readOnly){const t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value(){return(0,s.Z)((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))}},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=this._getStates(this.hass.states);return i&&i.length?{from:Number(t.from),options:i,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value(){return async()=>{if(!this._iconList){let e;e=(await i.e(3893).then(i.t.bind(i,63893,19))).default,this._iconList=e.map((e=>({type:"variable",label:`mdi:${e.name}`,detail:e.keywords.join(", "),info:u})))}return this._iconList}}},{kind:"method",key:"_mdiCompletions",value:async function(e){const t=e.matchBefore(/mdi:\S*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=await this._getIconItems();return{from:Number(t.from),options:i,validFor:/^mdi:\S*$/}}},{kind:"field",key:"_onUpdate",value(){return e=>{e.docChanged&&(this._value=e.state.doc.toString(),(0,l.B)(this,"value-changed",{value:this._value}))}}},{kind:"get",static:!0,key:"styles",value:function(){return d.iv`
      :host(.error-state) .cm-gutters {
        border-color: var(--error-state-color, red);
      }
    `}}]}}),d.fl)},9828:(e,t,i)=>{i.d(t,{i:()=>u});var o=i(73958),r=i(565),a=i(47838),d=i(41085),n=i(91632),s=i(9644),l=i(36924),c=i(15815);i(54371);const h=["button","ha-list-item"],u=(e,t)=>{var i;return s.dy`
  <div class="header_title">${t}</div>
  <ha-icon-button
    .label=${null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close"}
    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
    dialogAction="close"
    class="header_button"
  ></ha-icon-button>
`};(0,o.Z)([(0,l.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return s.dy`<slot name="heading"> ${(0,r.Z)((0,a.Z)(i.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,r.Z)((0,a.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,h].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.Z)((0,a.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value(){return[n.W,s.iv`
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
    `]}}]}}),d.M)},34838:(e,t,i)=>{i.d(t,{Be:()=>c,Bk:()=>d,X3:()=>h,YB:()=>l,g3:()=>a,mc:()=>r,pO:()=>s,r$:()=>n,uc:()=>o});const o=e=>e.callWS({type:"insteon/config/get"}),r=e=>e.callWS({type:"insteon/config/get_modem_schema"}),a=(e,t)=>e.callWS({type:"insteon/config/update_modem_config",config:t}),d=(e,t)=>e.callWS({type:"insteon/config/device_override/add",override:t}),n=(e,t)=>e.callWS({type:"insteon/config/device_override/remove",device_address:t}),s=e=>{let t;return t="light"==e?{type:"integer",valueMin:-1,valueMax:255,name:"dim_steps",required:!0,default:22}:{type:"constant",name:"dim_steps",required:!1,default:""},[{type:"select",options:[["a","a"],["b","b"],["c","c"],["d","d"],["e","e"],["f","f"],["g","g"],["h","h"],["i","i"],["j","j"],["k","k"],["l","l"],["m","m"],["n","n"],["o","o"],["p","p"]],name:"housecode",required:!0},{type:"select",options:[[1,"1"],[2,"2"],[3,"3"],[4,"4"],[5,"5"],[6,"6"],[7,"7"],[8,"8"],[9,"9"],[10,"10"],[11,"11"],[12,"12"],[13,"13"],[14,"14"],[15,"15"],[16,"16"]],name:"unitcode",required:!0},{type:"select",options:[["binary_sensor","binary_sensor"],["switch","switch"],["light","light"]],name:"platform",required:!0},t]};function l(e){return"device"in e}const c=(e,t)=>{const i=t.slice();return i.push({type:"boolean",required:!1,name:"manual_config"}),e&&i.push({type:"string",name:"plm_manual_config",required:!0}),i},h=[{name:"address",type:"string",required:!0},{name:"cat",type:"string",required:!0},{name:"subcat",type:"string",required:!0}]},13343:(e,t,i)=>{i.d(t,{CL:()=>_,CN:()=>u,Co:()=>r,Cy:()=>d,DT:()=>y,GU:()=>m,Ho:()=>C,Jz:()=>f,KJ:()=>b,N2:()=>s,NC:()=>a,NL:()=>h,Qs:()=>l,SL:()=>n,WM:()=>k,di:()=>p,rW:()=>g,tw:()=>c,yq:()=>v,zM:()=>o});const o=(e,t)=>e.callWS({type:"insteon/device/get",device_id:t}),r=(e,t)=>e.callWS({type:"insteon/aldb/get",device_address:t}),a=(e,t,i)=>e.callWS({type:"insteon/properties/get",device_address:t,show_advanced:i}),d=(e,t,i)=>e.callWS({type:"insteon/aldb/change",device_address:t,record:i}),n=(e,t,i,o)=>e.callWS({type:"insteon/properties/change",device_address:t,name:i,value:o}),s=(e,t,i)=>e.callWS({type:"insteon/aldb/create",device_address:t,record:i}),l=(e,t)=>e.callWS({type:"insteon/aldb/load",device_address:t}),c=(e,t)=>e.callWS({type:"insteon/properties/load",device_address:t}),h=(e,t)=>e.callWS({type:"insteon/aldb/write",device_address:t}),u=(e,t)=>e.callWS({type:"insteon/properties/write",device_address:t}),m=(e,t)=>e.callWS({type:"insteon/aldb/reset",device_address:t}),p=(e,t)=>e.callWS({type:"insteon/properties/reset",device_address:t}),v=(e,t)=>e.callWS({type:"insteon/aldb/add_default_links",device_address:t}),_=e=>[{name:"mode",options:[["c",e.localize("aldb.mode.controller")],["r",e.localize("aldb.mode.responder")]],required:!0,type:"select"},{name:"group",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"target",required:!0,type:"string"},{name:"data1",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data2",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data3",required:!0,type:"integer",valueMin:-1,valueMax:255}],y=e=>[{name:"in_use",required:!0,type:"boolean"},..._(e)],f=(e,t)=>[{name:"multiple",required:!1,type:t?"constant":"boolean"},{name:"add_x10",required:!1,type:e?"constant":"boolean"},{name:"device_address",required:!1,type:e||t?"constant":"string"}],g=e=>e.callWS({type:"insteon/device/add/cancel"}),k=(e,t,i)=>e.callWS({type:"insteon/device/remove",device_address:t,remove_all_refs:i}),b=(e,t)=>e.callWS({type:"insteon/device/add_x10",x10_device:t}),C={name:"ramp_rate",options:[["31","0.1"],["30","0.2"],["29","0.3"],["28","0.5"],["27","2"],["26","4.5"],["25","6.5"],["24","8.5"],["23","19"],["22","21.5"],["21","23.5"],["20","26"],["19","28"],["18","30"],["17","32"],["16","34"],["15","38.5"],["14","43"],["13","47"],["12","60"],["11","90"],["10","120"],["9","150"],["8","180"],["7","210"],["6","240"],["5","270"],["4","300"],["3","360"],["2","420"],["1","480"]],required:!0,type:"select"}},10759:(e,t,i)=>{i.r(t);var o=i(73958),r=i(9644),a=(i(30437),i(36924)),d=(i(25799),i(9828)),n=i(29950),s=i(34838),l=i(13343);i(39663),i(23860);(0,o.Z)([(0,a.Mo)("dialog-device-add-x10")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_title",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_callback",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_error",value(){}},{kind:"field",decorators:[(0,a.SB)()],key:"_formData",value:void 0},{kind:"field",decorators:[(0,a.SB)()],key:"_opened",value(){return!1}},{kind:"method",key:"showDialog",value:async function(e){this.hass=e.hass,this.insteon=e.insteon,this._callback=e.callback,this._title=e.title,this._opened=!0}},{kind:"method",key:"render",value:function(){var e,t;if(!this._opened)return r.dy``;const i=(0,s.pO)(null===(e=this._formData)||void 0===e?void 0:e.platform);return r.dy`
      <ha-dialog
        open
        @closed="${this._close}"
        .heading=${(0,d.i)(this.hass,this._title)}
      >
        ${this._error?r.dy`<ha-alert alertType="error">${this._error}</ha-alert>`:""}
        <div class="form">
          <ha-form
            .data=${this._haFormData()}
            .schema=${i}
            @value-changed=${this._valueChanged}
            .computeLabel=${this._computeLabel(null===(t=this.insteon)||void 0===t?void 0:t.localize)}
          ></ha-form>
        </div>
        <div class="buttons">
          <mwc-button @click=${this._dismiss} slot="secondaryAction">
            ${this.hass.localize("ui.dialogs.generic.cancel")}
          </mwc-button>
          <mwc-button @click=${this._submit} slot="primaryAction">
            ${this.hass.localize("ui.dialogs.generic.ok")}
          </mwc-button>
        </div>
      </ha-dialog>
    `}},{kind:"method",key:"_haFormData",value:function(){return{...this._formData}}},{kind:"method",key:"_dismiss",value:function(){this._close()}},{kind:"method",key:"_computeLabel",value:function(e){return t=>e("device.add_x10.fields."+t.name)||t.name}},{kind:"method",key:"_submit",value:async function(){const e={...this._formData};null==e.dim_steps&&(e.dim_steps=0);try{await(0,l.KJ)(this.hass,e),this._close(),await this._callback()}catch(t){this._error=this.insteon.localize("device.add_x10.error.duplicate_device")}}},{kind:"method",key:"_close",value:function(){this._opened=!1,this._error=void 0,this._formData=void 0}},{kind:"method",key:"_valueChanged",value:function(e){var t,i;this._formData=e.detail.value,"light"==(null===(t=this._formData)||void 0===t?void 0:t.platform)?this._formData.dim_steps||(this._formData.dim_steps=22):this._formData.dim_steps=0,null!==(i=this._formData)&&void 0!==i&&i.dim_steps&&[0,1].includes(this._formData.dim_steps)&&(this._formData.dim_steps=1)}},{kind:"get",static:!0,key:"styles",value:function(){return[n.yu,r.iv`
        table {
          width: 100%;
        }
        ha-combo-box {
          width: 20px;
        }
        .title {
          width: 200px;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=e77c5cb0.js.map