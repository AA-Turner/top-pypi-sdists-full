"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["601"],{91337:function(e,t,a){a(26847),a(81738),a(22960),a(6989),a(87799),a(1455),a(27530);var r=a(73742),o=a(59048),i=a(7616),s=a(69342),n=a(29740);a(22543),a(32986);let l,d,c,h,u,p,m,_,b,g=e=>e;const v={boolean:()=>a.e("4852").then(a.bind(a,60751)),constant:()=>a.e("177").then(a.bind(a,85184)),float:()=>a.e("2369").then(a.bind(a,94980)),grid:()=>a.e("9219").then(a.bind(a,79998)),expandable:()=>a.e("4020").then(a.bind(a,71781)),integer:()=>a.e("3703").then(a.bind(a,12960)),multi_select:()=>Promise.all([a.e("4458"),a.e("514")]).then(a.bind(a,79298)),positive_time_period_dict:()=>a.e("2010").then(a.bind(a,49058)),select:()=>a.e("3162").then(a.bind(a,64324)),string:()=>a.e("2529").then(a.bind(a,72609)),optional_actions:()=>a.e("1601").then(a.bind(a,67552))},y=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;class f extends o.oi{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof o.fl&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{var t;"selector"in e||null===(t=v[e.type])||void 0===t||t.call(v)}))}render(){return(0,o.dy)(l||(l=g`
      <div class="root" part="root">
        ${0}
        ${0}
      </div>
    `),this.error&&this.error.base?(0,o.dy)(d||(d=g`
              <ha-alert alert-type="error">
                ${0}
              </ha-alert>
            `),this._computeError(this.error.base,this.schema)):"",this.schema.map((e=>{var t;const a=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),r=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return(0,o.dy)(c||(c=g`
            ${0}
            ${0}
          `),a?(0,o.dy)(h||(h=g`
                  <ha-alert own-margin alert-type="error">
                    ${0}
                  </ha-alert>
                `),this._computeError(a,e)):r?(0,o.dy)(u||(u=g`
                    <ha-alert own-margin alert-type="warning">
                      ${0}
                    </ha-alert>
                  `),this._computeWarning(r,e)):"","selector"in e?(0,o.dy)(p||(p=g`<ha-selector
                  .schema=${0}
                  .hass=${0}
                  .narrow=${0}
                  .name=${0}
                  .selector=${0}
                  .value=${0}
                  .label=${0}
                  .disabled=${0}
                  .placeholder=${0}
                  .helper=${0}
                  .localizeValue=${0}
                  .required=${0}
                  .context=${0}
                ></ha-selector>`),e,this.hass,this.narrow,e.name,e.selector,y(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?"":e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,s.h)(this.fieldElementName(e.type),Object.assign({schema:e,data:y(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))})))}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[a,r]of Object.entries(e.context))t[a]=this.data[r];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),a),(0,n.B)(this,"value-changed",{value:this.data})}))}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?(0,o.dy)(m||(m=g`<ul>
        ${0}
      </ul>`),e.map((e=>(0,o.dy)(_||(_=g`<li>
              ${0}
            </li>`),this.computeError?this.computeError(e,t):e)))):this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}f.styles=(0,o.iv)(b||(b=g`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `)),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],f.prototype,"narrow",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"data",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"schema",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"error",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"warning",void 0),(0,r.__decorate)([(0,i.Cb)({type:Boolean})],f.prototype,"disabled",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"computeError",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"computeWarning",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"computeLabel",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"computeHelper",void 0),(0,r.__decorate)([(0,i.Cb)({attribute:!1})],f.prototype,"localizeValue",void 0),f=(0,r.__decorate)([(0,i.Mo)("ha-form")],f)},74069:function(e,t,a){a.a(e,(async function(e,r){try{a.r(t);a(26847),a(27530);var o=a(73742),i=a(59048),s=a(28105),n=a(7616),l=a(29740),d=a(99298),c=(a(91337),a(30337)),h=a(77204),u=e([c]);c=(u.then?(await u)():u)[0];let p,m=e=>e;class _ extends i.oi{showDialog(e){var t;this._params=e,this._error=void 0,this._data=e.block,this._expand=!(null===(t=e.block)||void 0===t||!t.data)}closeDialog(){this._params=void 0,this._data=void 0,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}render(){return this._params&&this._data?(0,i.dy)(p||(p=m`
      <ha-dialog
        open
        @closed=${0}
        .heading=${0}
      >
        <div>
          <ha-form
            .hass=${0}
            .schema=${0}
            .data=${0}
            .error=${0}
            .computeLabel=${0}
            @value-changed=${0}
          ></ha-form>
        </div>
        <ha-button
          slot="secondaryAction"
          @click=${0}
          appearance="plain"
          variant="danger"
        >
          ${0}
        </ha-button>
        <ha-button slot="primaryAction" @click=${0}>
          ${0}
        </ha-button>
      </ha-dialog>
    `),this.closeDialog,(0,d.i)(this.hass,this.hass.localize("ui.dialogs.helper_settings.schedule.edit_schedule_block")),this.hass,this._schema(this._expand),this._data,this._error,this._computeLabelCallback,this._valueChanged,this._deleteBlock,this.hass.localize("ui.common.delete"),this._updateBlock,this.hass.localize("ui.common.save")):i.Ld}_valueChanged(e){this._error=void 0,this._data=e.detail.value}_updateBlock(){try{this._params.updateBlock(this._data),this.closeDialog()}catch(e){this._error={base:e?e.message:"Unknown error"}}}_deleteBlock(){try{this._params.deleteBlock(),this.closeDialog()}catch(e){this._error={base:e?e.message:"Unknown error"}}}static get styles(){return[h.yu]}constructor(...e){super(...e),this._expand=!1,this._schema=(0,s.Z)((e=>[{name:"from",required:!0,selector:{time:{no_second:!0}}},{name:"to",required:!0,selector:{time:{no_second:!0}}},{name:"advanced_settings",type:"expandable",flatten:!0,expanded:e,schema:[{name:"data",required:!1,selector:{object:{}}}]}])),this._computeLabelCallback=e=>{switch(e.name){case"from":return this.hass.localize("ui.dialogs.helper_settings.schedule.start");case"to":return this.hass.localize("ui.dialogs.helper_settings.schedule.end");case"data":return this.hass.localize("ui.dialogs.helper_settings.schedule.data");case"advanced_settings":return this.hass.localize("ui.dialogs.helper_settings.generic.advanced_settings")}return""}}}(0,o.__decorate)([(0,n.Cb)({attribute:!1})],_.prototype,"hass",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_error",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_data",void 0),(0,o.__decorate)([(0,n.SB)()],_.prototype,"_params",void 0),customElements.define("dialog-schedule-block-info",_),r()}catch(p){r(p)}}))}}]);
//# sourceMappingURL=601.7e0f775b2291873b.js.map