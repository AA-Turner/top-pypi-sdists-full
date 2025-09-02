/*! For license information please see bd4bc851.js.LICENSE.txt */
"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[986],{86089:(e,t,i)=>{i.d(t,{U:()=>o});const o=e=>e.stopPropagation()},44672:(e,t,i)=>{i.d(t,{p:()=>o});const o=e=>e.substr(e.indexOf(".")+1)},2733:(e,t,i)=>{i.d(t,{C:()=>r});var o=i(44672);const r=e=>{return t=e.entity_id,void 0===(i=e.attributes).friendly_name?(0,o.p)(t).replace(/_/g," "):(null!==(r=i.friendly_name)&&void 0!==r?r:"").toString();var t,i,r}},28858:(e,t,i)=>{i.d(t,{$:()=>a,f:()=>s});var o=i(14516);const r=(0,o.Z)((e=>new Intl.Collator(e))),n=(0,o.Z)((e=>new Intl.Collator(e,{sensitivity:"accent"}))),d=(e,t)=>e<t?-1:e>t?1:0,a=(e,t,i=void 0)=>{var o;return null!==(o=Intl)&&void 0!==o&&o.Collator?r(i).compare(e,t):d(e,t)},s=(e,t,i=void 0)=>{var o;return null!==(o=Intl)&&void 0!==o&&o.Collator?n(i).compare(e,t):d(e.toLowerCase(),t.toLowerCase())}},72218:(e,t,i)=>{i.d(t,{D:()=>o});const o=(e,t,i=!1)=>{let o;const r=(...r)=>{const n=i&&!o;clearTimeout(o),o=window.setTimeout((()=>{o=void 0,i||e(...r)}),t),n&&e(...r)};return r.cancel=()=>{clearTimeout(o)},r}},25799:(e,t,i)=>{var o=i(73958),r=i(565),n=i(47838),d=i(9644),a=i(36924),s=i(14516),l=i(18394),c=i(86089);const u={key:"Mod-s",run:e=>((0,l.B)(e.dom,"editor-save"),!0)},h=e=>{const t=document.createElement("ha-icon");return t.icon=e.label,t};(0,o.Z)([(0,a.Mo)("ha-code-editor")],(function(e,t){class o extends t{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",key:"codemirror",value:void 0},{kind:"field",decorators:[(0,a.Cb)()],key:"mode",value(){return"yaml"}},{kind:"field",key:"hass",value:void 0},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"autofocus",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"readOnly",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"autocomplete-entities"})],key:"autocompleteEntities",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean,attribute:"autocomplete-icons"})],key:"autocompleteIcons",value(){return!1}},{kind:"field",decorators:[(0,a.Cb)({type:Boolean})],key:"error",value(){return!1}},{kind:"field",decorators:[(0,a.SB)()],key:"_value",value(){return""}},{kind:"field",key:"_loadedCodeMirror",value:void 0},{kind:"field",key:"_iconList",value:void 0},{kind:"set",key:"value",value:function(e){this._value=e}},{kind:"get",key:"value",value:function(){return this.codemirror?this.codemirror.state.doc.toString():this._value}},{kind:"get",key:"hasComments",value:function(){if(!this.codemirror||!this._loadedCodeMirror)return!1;const e=this._loadedCodeMirror.highlightingFor(this.codemirror.state,[this._loadedCodeMirror.tags.comment]);return!!this.renderRoot.querySelector(`span.${e}`)}},{kind:"method",key:"connectedCallback",value:function(){(0,r.Z)((0,n.Z)(o.prototype),"connectedCallback",this).call(this),this.hasUpdated&&this.requestUpdate(),this.addEventListener("keydown",c.U),this.codemirror&&!1!==this.autofocus&&this.codemirror.focus()}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.Z)((0,n.Z)(o.prototype),"disconnectedCallback",this).call(this),this.removeEventListener("keydown",c.U),this.updateComplete.then((()=>{this.codemirror.destroy(),delete this.codemirror}))}},{kind:"method",key:"scheduleUpdate",value:async function(){var e;null!==(e=this._loadedCodeMirror)&&void 0!==e||(this._loadedCodeMirror=await Promise.all([i.e(8367),i.e(9146)]).then(i.bind(i,59146))),(0,r.Z)((0,n.Z)(o.prototype),"scheduleUpdate",this).call(this)}},{kind:"method",key:"update",value:function(e){if((0,r.Z)((0,n.Z)(o.prototype),"update",this).call(this,e),!this.codemirror)return void this._createCodeMirror();const t=[];e.has("mode")&&t.push({effects:this._loadedCodeMirror.langCompartment.reconfigure(this._mode)}),e.has("readOnly")&&t.push({effects:this._loadedCodeMirror.readonlyCompartment.reconfigure(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly))}),e.has("_value")&&this._value!==this.value&&t.push({changes:{from:0,to:this.codemirror.state.doc.length,insert:this._value}}),t.length>0&&this.codemirror.dispatch(...t),e.has("error")&&this.classList.toggle("error-state",this.error)}},{kind:"get",key:"_mode",value:function(){return this._loadedCodeMirror.langs[this.mode]}},{kind:"method",key:"_createCodeMirror",value:function(){if(!this._loadedCodeMirror)throw new Error("Cannot create editor before CodeMirror is loaded");const e=[this._loadedCodeMirror.lineNumbers(),this._loadedCodeMirror.history(),this._loadedCodeMirror.drawSelection(),this._loadedCodeMirror.EditorState.allowMultipleSelections.of(!0),this._loadedCodeMirror.rectangularSelection(),this._loadedCodeMirror.crosshairCursor(),this._loadedCodeMirror.highlightSelectionMatches(),this._loadedCodeMirror.highlightActiveLine(),this._loadedCodeMirror.keymap.of([...this._loadedCodeMirror.defaultKeymap,...this._loadedCodeMirror.searchKeymap,...this._loadedCodeMirror.historyKeymap,...this._loadedCodeMirror.tabKeyBindings,u]),this._loadedCodeMirror.langCompartment.of(this._mode),this._loadedCodeMirror.haTheme,this._loadedCodeMirror.haSyntaxHighlighting,this._loadedCodeMirror.readonlyCompartment.of(this._loadedCodeMirror.EditorView.editable.of(!this.readOnly)),this._loadedCodeMirror.EditorView.updateListener.of(this._onUpdate)];if(!this.readOnly){const t=[];this.autocompleteEntities&&this.hass&&t.push(this._entityCompletions.bind(this)),this.autocompleteIcons&&t.push(this._mdiCompletions.bind(this)),t.length>0&&e.push(this._loadedCodeMirror.autocompletion({override:t,maxRenderedOptions:10}))}this.codemirror=new this._loadedCodeMirror.EditorView({state:this._loadedCodeMirror.EditorState.create({doc:this._value,extensions:e}),parent:this.renderRoot})}},{kind:"field",key:"_getStates",value(){return(0,s.Z)((e=>{if(!e)return[];return Object.keys(e).map((t=>({type:"variable",label:t,detail:e[t].attributes.friendly_name,info:`State: ${e[t].state}`})))}))}},{kind:"method",key:"_entityCompletions",value:function(e){const t=e.matchBefore(/[a-z_]{3,}\.\w*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=this._getStates(this.hass.states);return i&&i.length?{from:Number(t.from),options:i,validFor:/^[a-z_]{3,}\.\w*$/}:null}},{kind:"field",key:"_getIconItems",value(){return async()=>{if(!this._iconList){let e;e=(await i.e(3893).then(i.t.bind(i,63893,19))).default,this._iconList=e.map((e=>({type:"variable",label:`mdi:${e.name}`,detail:e.keywords.join(", "),info:h})))}return this._iconList}}},{kind:"method",key:"_mdiCompletions",value:async function(e){const t=e.matchBefore(/mdi:\S*/);if(!t||t.from===t.to&&!e.explicit)return null;const i=await this._getIconItems();return{from:Number(t.from),options:i,validFor:/^mdi:\S*$/}}},{kind:"field",key:"_onUpdate",value(){return e=>{e.docChanged&&(this._value=e.state.doc.toString(),(0,l.B)(this,"value-changed",{value:this._value}))}}},{kind:"get",static:!0,key:"styles",value:function(){return d.iv`
      :host(.error-state) .cm-gutters {
        border-color: var(--error-state-color, red);
      }
    `}}]}}),d.fl)},9828:(e,t,i)=>{i.d(t,{i:()=>h});var o=i(73958),r=i(565),n=i(47838),d=i(41085),a=i(91632),s=i(9644),l=i(36924),c=i(15815);i(54371);const u=["button","ha-list-item"],h=(e,t)=>{var i;return s.dy`
  <div class="header_title">${t}</div>
  <ha-icon-button
    .label=${null!==(i=null==e?void 0:e.localize("ui.dialogs.generic.close"))&&void 0!==i?i:"Close"}
    .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
    dialogAction="close"
    class="header_button"
  ></ha-icon-button>
`};(0,o.Z)([(0,l.Mo)("ha-dialog")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",key:c.gA,value:void 0},{kind:"method",key:"scrollToPos",value:function(e,t){var i;null===(i=this.contentElement)||void 0===i||i.scrollTo(e,t)}},{kind:"method",key:"renderHeading",value:function(){return s.dy`<slot name="heading"> ${(0,r.Z)((0,n.Z)(i.prototype),"renderHeading",this).call(this)} </slot>`}},{kind:"method",key:"firstUpdated",value:function(){var e;(0,r.Z)((0,n.Z)(i.prototype),"firstUpdated",this).call(this),this.suppressDefaultPressSelector=[this.suppressDefaultPressSelector,u].join(", "),this._updateScrolledAttribute(),null===(e=this.contentElement)||void 0===e||e.addEventListener("scroll",this._onScroll,{passive:!0})}},{kind:"method",key:"disconnectedCallback",value:function(){(0,r.Z)((0,n.Z)(i.prototype),"disconnectedCallback",this).call(this),this.contentElement.removeEventListener("scroll",this._onScroll)}},{kind:"field",key:"_onScroll",value(){return()=>{this._updateScrolledAttribute()}}},{kind:"method",key:"_updateScrolledAttribute",value:function(){this.contentElement&&this.toggleAttribute("scrolled",0!==this.contentElement.scrollTop)}},{kind:"field",static:!0,key:"styles",value(){return[a.W,s.iv`
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
    `]}}]}}),d.M)},51134:(e,t,i)=>{i.d(t,{HP:()=>h,R6:()=>u,_Y:()=>s,jL:()=>d,q4:()=>c,t1:()=>a});var o=i(45666),r=i(2733),n=(i(28858),i(72218));const d=(e,t,i)=>e.name_by_user||e.name||i&&((e,t)=>{for(const i of t||[]){const t="string"==typeof i?i:i.entity_id,o=e.states[t];if(o)return(0,r.C)(o)}})(t,i)||t.localize("ui.panel.config.devices.unnamed_device",{type:t.localize(`ui.panel.config.devices.type.${e.entry_type||"device"}`)}),a=(e,t,i)=>e.callWS({type:"config/device_registry/update",device_id:t,...i}),s=e=>e.sendMessagePromise({type:"config/device_registry/list"}),l=(e,t)=>e.subscribeEvents((0,n.D)((()=>s(e).then((e=>t.setState(e,!0)))),500,!0),"device_registry_updated"),c=(e,t)=>(0,o.B)("_dr",s,l,e,t),u=e=>{const t={};for(const i of e)i.device_id&&(i.device_id in t||(t[i.device_id]=[]),t[i.device_id].push(i));return t},h=(e,t)=>{const i={};for(const o of t){const t=e[o.entity_id];null!=t&&t.domain&&null!==o.device_id&&(i[o.device_id]||(i[o.device_id]=[]),i[o.device_id].push(t.domain))}return i}},14114:(e,t,i)=>{i.d(t,{P:()=>o});const o=e=>(t,i)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,i)=>t.constructor._observers.set(i,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const i=this.constructor._observers.get(t);void 0!==i&&i.call(this,this[t],e)}))}}t.constructor._observers.set(i,e)}},6129:(e,t,i)=>{i.r(t);var o=i(73958),r=(i(30437),i(9644)),n=i(36924),d=(i(25799),i(9828)),a=(i(23860),i(29950)),s=(i(39663),i(8205)),l=i(11285),c=i(13343);const u=[{name:"address",type:"string",required:!0}];(0,o.Z)([(0,n.Mo)("dialog-delete-device")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"insteon",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_title",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_callback",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_formData",value(){return{address:void 0}}},{kind:"field",decorators:[(0,n.SB)()],key:"_error",value(){return""}},{kind:"field",decorators:[(0,n.SB)()],key:"_opened",value(){return!1}},{kind:"method",key:"showDialog",value:async function(e){this.hass=e.hass,this.insteon=e.insteon,this._callback=e.callback,this._title=e.title,this._opened=!0}},{kind:"method",key:"render",value:function(){return this._opened?r.dy`
      <ha-dialog
        open
        @closed="${this._close}"
        .heading=${(0,d.i)(this.hass,this._title)}
      >
        <div class="form">
          ${this._error?r.dy`<ha-alert>${this._error}</ha-alert>`:""}
          <ha-form
            .data=${this._formData}
            .schema=${u}
            @value-changed=${this._valueChanged}
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
    `:r.dy``}},{kind:"method",key:"_dismiss",value:function(){this._close()}},{kind:"method",key:"_submit",value:async function(){if(!(0,s.fF)(this._formData.address))return void(this._error=this.insteon.localize("common.error.address"));const e=this._formData.address;this._opened=!1,await this._confirmDeleteScope(e),this._callback&&this._callback(e)}},{kind:"method",key:"_confirmDeleteScope",value:async function(e){if(!(await(0,l.g7)(this,{text:this.insteon.localize("common.warn.delete"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),warning:!0})))return;const t=await(0,l.g7)(this,{title:this.insteon.localize("device.remove_all_refs.title"),text:r.dy`
        ${this.insteon.localize("device.remove_all_refs.description")}<br><br>
        ${this.insteon.localize("device.remove_all_refs.confirm_description")}<br>
        ${this.insteon.localize("device.remove_all_refs.dismiss_description")}`,confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no"),warning:!0,destructive:!0});await(0,c.WM)(this.hass,e,t)}},{kind:"method",key:"_close",value:function(){this._formData={address:void 0},this._opened=!1}},{kind:"method",key:"_valueChanged",value:function(e){this._formData=e.detail.value}},{kind:"get",static:!0,key:"styles",value:function(){return[a.yu,r.iv`
        table {
          width: 100%;
        }
        ha-combo-box {
          width: 20px;
        }
        .title {
          width: 200px;
        }
      `]}}]}}),r.oi)},13343:(e,t,i)=>{i.d(t,{CL:()=>_,CN:()=>h,Co:()=>r,Cy:()=>d,DT:()=>f,GU:()=>v,Ho:()=>C,Jz:()=>y,KJ:()=>b,N2:()=>s,NC:()=>n,NL:()=>u,Qs:()=>l,SL:()=>a,WM:()=>k,di:()=>m,rW:()=>g,tw:()=>c,yq:()=>p,zM:()=>o});const o=(e,t)=>e.callWS({type:"insteon/device/get",device_id:t}),r=(e,t)=>e.callWS({type:"insteon/aldb/get",device_address:t}),n=(e,t,i)=>e.callWS({type:"insteon/properties/get",device_address:t,show_advanced:i}),d=(e,t,i)=>e.callWS({type:"insteon/aldb/change",device_address:t,record:i}),a=(e,t,i,o)=>e.callWS({type:"insteon/properties/change",device_address:t,name:i,value:o}),s=(e,t,i)=>e.callWS({type:"insteon/aldb/create",device_address:t,record:i}),l=(e,t)=>e.callWS({type:"insteon/aldb/load",device_address:t}),c=(e,t)=>e.callWS({type:"insteon/properties/load",device_address:t}),u=(e,t)=>e.callWS({type:"insteon/aldb/write",device_address:t}),h=(e,t)=>e.callWS({type:"insteon/properties/write",device_address:t}),v=(e,t)=>e.callWS({type:"insteon/aldb/reset",device_address:t}),m=(e,t)=>e.callWS({type:"insteon/properties/reset",device_address:t}),p=(e,t)=>e.callWS({type:"insteon/aldb/add_default_links",device_address:t}),_=e=>[{name:"mode",options:[["c",e.localize("aldb.mode.controller")],["r",e.localize("aldb.mode.responder")]],required:!0,type:"select"},{name:"group",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"target",required:!0,type:"string"},{name:"data1",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data2",required:!0,type:"integer",valueMin:-1,valueMax:255},{name:"data3",required:!0,type:"integer",valueMin:-1,valueMax:255}],f=e=>[{name:"in_use",required:!0,type:"boolean"},..._(e)],y=(e,t)=>[{name:"multiple",required:!1,type:t?"constant":"boolean"},{name:"add_x10",required:!1,type:e?"constant":"boolean"},{name:"device_address",required:!1,type:e||t?"constant":"string"}],g=e=>e.callWS({type:"insteon/device/add/cancel"}),k=(e,t,i)=>e.callWS({type:"insteon/device/remove",device_address:t,remove_all_refs:i}),b=(e,t)=>e.callWS({type:"insteon/device/add_x10",x10_device:t}),C={name:"ramp_rate",options:[["31","0.1"],["30","0.2"],["29","0.3"],["28","0.5"],["27","2"],["26","4.5"],["25","6.5"],["24","8.5"],["23","19"],["22","21.5"],["21","23.5"],["20","26"],["19","28"],["18","30"],["17","32"],["16","34"],["15","38.5"],["14","43"],["13","47"],["12","60"],["11","90"],["10","120"],["9","150"],["8","180"],["7","210"],["6","240"],["5","270"],["4","300"],["3","360"],["2","420"],["1","480"]],required:!0,type:"select"}},8205:(e,t,i)=>{i.d(t,{Vo:()=>r,fF:()=>o,jT:()=>d});const o=e=>{const t=d(e);return 6==t.length&&r(t)},r=e=>{"0x"==e.substring(0,2).toLocaleLowerCase()&&(e=e.substring(2));const t=[...e];if(t.length%2!=0)return!1;for(let i=0;i<t.length;i++)if(!n(t[i]))return!1;return!0},n=e=>["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"].includes(e.toLocaleLowerCase()),d=e=>e.toLocaleLowerCase().split(".").join("")},45666:(e,t,i)=>{i.d(t,{B:()=>n});const o=e=>{let t=[];function i(i,o){e=o?i:Object.assign(Object.assign({},e),i);let r=t;for(let t=0;t<r.length;t++)r[t](e)}return{get state(){return e},action(t){function o(e){i(e,!1)}return function(){let i=[e];for(let e=0;e<arguments.length;e++)i.push(arguments[e]);let r=t.apply(this,i);if(null!=r)return r instanceof Promise?r.then(o):o(r)}},setState:i,clearState(){e=void 0},subscribe(e){return t.push(e),()=>{!function(e){let i=[];for(let o=0;o<t.length;o++)t[o]===e?e=null:i.push(t[o]);t=i}(e)}}}},r=(e,t,i,r,n={unsubGrace:!0})=>{if(e[t])return e[t];let d,a,s=0,l=o();const c=()=>{if(!i)throw new Error("Collection does not support refresh");return i(e).then((e=>l.setState(e,!0)))},u=()=>c().catch((t=>{if(e.connected)throw t})),h=()=>{a=void 0,d&&d.then((e=>{e()})),l.clearState(),e.removeEventListener("ready",c),e.removeEventListener("disconnected",v)},v=()=>{a&&(clearTimeout(a),h())};return e[t]={get state(){return l.state},refresh:c,subscribe(t){s++,1===s&&(()=>{if(void 0!==a)return clearTimeout(a),void(a=void 0);r&&(d=r(e,l)),i&&(e.addEventListener("ready",u),u()),e.addEventListener("disconnected",v)})();const o=l.subscribe(t);return void 0!==l.state&&setTimeout((()=>t(l.state)),0),()=>{o(),s--,s||(n.unsubGrace?a=setTimeout(h,5e3):h())}}},e[t]},n=(e,t,i,o,n)=>r(o,e,t,i).subscribe(n)},57835:(e,t,i)=>{i.d(t,{XM:()=>o.XM,Xe:()=>o.Xe,pX:()=>o.pX});var o=i(38941)}}]);
//# sourceMappingURL=bd4bc851.js.map