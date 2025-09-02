"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["6470"],{91337:function(e,t,a){a(26847),a(81738),a(22960),a(6989),a(87799),a(1455),a(27530);var o=a(73742),r=a(59048),n=a(7616),i=a(69342),l=a(29740);a(22543),a(32986);let s,c,d,p,m,h,u,b,_,y=e=>e;const v={boolean:()=>a.e("4852").then(a.bind(a,60751)),constant:()=>a.e("177").then(a.bind(a,85184)),float:()=>a.e("2369").then(a.bind(a,94980)),grid:()=>a.e("9219").then(a.bind(a,79998)),expandable:()=>a.e("4020").then(a.bind(a,71781)),integer:()=>a.e("3703").then(a.bind(a,12960)),multi_select:()=>Promise.all([a.e("4458"),a.e("514")]).then(a.bind(a,79298)),positive_time_period_dict:()=>a.e("2010").then(a.bind(a,49058)),select:()=>a.e("3162").then(a.bind(a,64324)),string:()=>a.e("2529").then(a.bind(a,72609)),optional_actions:()=>a.e("1601").then(a.bind(a,67552))},g=(e,t)=>e?!t.name||t.flatten?e:e[t.name]:null;class f extends r.oi{getFormProperties(){return{}}async focus(){await this.updateComplete;const e=this.renderRoot.querySelector(".root");if(e)for(const t of e.children)if("HA-ALERT"!==t.tagName){t instanceof r.fl&&await t.updateComplete,t.focus();break}}willUpdate(e){e.has("schema")&&this.schema&&this.schema.forEach((e=>{var t;"selector"in e||null===(t=v[e.type])||void 0===t||t.call(v)}))}render(){return(0,r.dy)(s||(s=y`
      <div class="root" part="root">
        ${0}
        ${0}
      </div>
    `),this.error&&this.error.base?(0,r.dy)(c||(c=y`
              <ha-alert alert-type="error">
                ${0}
              </ha-alert>
            `),this._computeError(this.error.base,this.schema)):"",this.schema.map((e=>{var t;const a=((e,t)=>e&&t.name?e[t.name]:null)(this.error,e),o=((e,t)=>e&&t.name?e[t.name]:null)(this.warning,e);return(0,r.dy)(d||(d=y`
            ${0}
            ${0}
          `),a?(0,r.dy)(p||(p=y`
                  <ha-alert own-margin alert-type="error">
                    ${0}
                  </ha-alert>
                `),this._computeError(a,e)):o?(0,r.dy)(m||(m=y`
                    <ha-alert own-margin alert-type="warning">
                      ${0}
                    </ha-alert>
                  `),this._computeWarning(o,e)):"","selector"in e?(0,r.dy)(h||(h=y`<ha-selector
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
                ></ha-selector>`),e,this.hass,this.narrow,e.name,e.selector,g(this.data,e),this._computeLabel(e,this.data),e.disabled||this.disabled||!1,e.required?"":e.default,this._computeHelper(e),this.localizeValue,e.required||!1,this._generateContext(e)):(0,i.h)(this.fieldElementName(e.type),Object.assign({schema:e,data:g(this.data,e),label:this._computeLabel(e,this.data),helper:this._computeHelper(e),disabled:this.disabled||e.disabled||!1,hass:this.hass,localize:null===(t=this.hass)||void 0===t?void 0:t.localize,computeLabel:this.computeLabel,computeHelper:this.computeHelper,localizeValue:this.localizeValue,context:this._generateContext(e)},this.getFormProperties())))})))}fieldElementName(e){return`ha-form-${e}`}_generateContext(e){if(!e.context)return;const t={};for(const[a,o]of Object.entries(e.context))t[a]=this.data[o];return t}createRenderRoot(){const e=super.createRenderRoot();return this.addValueChangedListener(e),e}addValueChangedListener(e){e.addEventListener("value-changed",(e=>{e.stopPropagation();const t=e.target.schema;if(e.target===this)return;const a=!t.name||"flatten"in t&&t.flatten?e.detail.value:{[t.name]:e.detail.value};this.data=Object.assign(Object.assign({},this.data),a),(0,l.B)(this,"value-changed",{value:this.data})}))}_computeLabel(e,t){return this.computeLabel?this.computeLabel(e,t):e?e.name:""}_computeHelper(e){return this.computeHelper?this.computeHelper(e):""}_computeError(e,t){return Array.isArray(e)?(0,r.dy)(u||(u=y`<ul>
        ${0}
      </ul>`),e.map((e=>(0,r.dy)(b||(b=y`<li>
              ${0}
            </li>`),this.computeError?this.computeError(e,t):e)))):this.computeError?this.computeError(e,t):e}_computeWarning(e,t){return this.computeWarning?this.computeWarning(e,t):e}constructor(...e){super(...e),this.narrow=!1,this.disabled=!1}}f.styles=(0,r.iv)(_||(_=y`
    .root > * {
      display: block;
    }
    .root > *:not([own-margin]):not(:last-child) {
      margin-bottom: 24px;
    }
    ha-alert[own-margin] {
      margin-bottom: 4px;
    }
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],f.prototype,"narrow",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"data",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"schema",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"error",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"warning",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean})],f.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"computeError",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"computeWarning",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"computeLabel",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"computeHelper",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],f.prototype,"localizeValue",void 0),f=(0,o.__decorate)([(0,n.Mo)("ha-form")],f)},69933:function(e,t,a){a.r(t),a.d(t,{HaSelectorSelector:function(){return h}});a(26847),a(81738),a(6989),a(87799),a(27530);var o=a(73742),r=a(59048),n=a(7616),i=a(28105),l=a(29740);a(22543),a(91337);let s,c,d=e=>e;const p={number:{min:1,max:100}},m={action:[],area:[{name:"multiple",selector:{boolean:{}}}],attribute:[{name:"entity_id",selector:{entity:{}}}],boolean:[],color_temp:[{name:"unit",selector:{select:{options:["kelvin","mired"]}}},{name:"min",selector:{number:{mode:"box"}}},{name:"max",selector:{number:{mode:"box"}}}],condition:[],date:[],datetime:[],device:[{name:"multiple",selector:{boolean:{}}}],duration:[{name:"enable_day",selector:{boolean:{}}},{name:"enable_millisecond",selector:{boolean:{}}}],entity:[{name:"multiple",selector:{boolean:{}}}],floor:[{name:"multiple",selector:{boolean:{}}}],icon:[],location:[],media:[{name:"accept",selector:{text:{multiple:!0}}}],number:[{name:"min",selector:{number:{mode:"box",step:"any"}}},{name:"max",selector:{number:{mode:"box",step:"any"}}},{name:"step",selector:{number:{mode:"box",step:"any"}}}],object:[],color_rgb:[],select:[{name:"options",selector:{object:{}}},{name:"multiple",selector:{boolean:{}}}],state:[{name:"entity_id",selector:{entity:{}}}],target:[],template:[],text:[{name:"multiple",selector:{boolean:{}}},{name:"multiline",selector:{boolean:{}}},{name:"prefix",selector:{text:{}}},{name:"suffix",selector:{text:{}}}],theme:[],time:[]};class h extends r.oi{shouldUpdate(e){return 1!==e.size||!e.has("hass")}render(){let e,t;if(this._yamlMode)t="manual",e={type:t,manual:this.value};else{t=Object.keys(this.value)[0];const a=Object.values(this.value)[0];e=Object.assign({type:t},"object"==typeof a?a:[])}const a=this._schema(t,this.hass.localize);return(0,r.dy)(s||(s=d`<ha-card>
      <div class="card-content">
        <p>${0}</p>
        <ha-form
          .hass=${0}
          .data=${0}
          .schema=${0}
          .computeLabel=${0}
          @value-changed=${0}
        ></ha-form></div
    ></ha-card>`),this.label?this.label:"",this.hass,e,a,this._computeLabelCallback,this._valueChanged)}_valueChanged(e){e.stopPropagation();const t=e.detail.value,a=t.type;if(!a||"object"!=typeof t||0===Object.keys(t).length)return;const o=Object.keys(this.value)[0];if("manual"===a&&!this._yamlMode)return this._yamlMode=!0,void this.requestUpdate();if("manual"===a&&void 0===t.manual)return;let r;"manual"!==a&&(this._yamlMode=!1),delete t.type,r="manual"===a?t.manual:a===o?{[a]:Object.assign({},t.manual?t.manual[o]:t)}:{[a]:Object.assign({},p[a])},(0,l.B)(this,"value-changed",{value:r})}constructor(...e){super(...e),this.disabled=!1,this.required=!0,this._yamlMode=!1,this._schema=(0,i.Z)(((e,t)=>[{name:"type",selector:{select:{mode:"dropdown",required:!0,options:Object.keys(m).concat("manual").map((e=>({label:t(`ui.components.selectors.selector.types.${e}`)||e,value:e})))}}},..."manual"===e?[{name:"manual",selector:{object:{}}}]:[],...m[e]?m[e].length>1?[{name:"",type:"expandable",title:t("ui.components.selectors.selector.options"),schema:m[e]}]:m[e]:[]])),this._computeLabelCallback=e=>this.hass.localize(`ui.components.selectors.selector.${e.name}`)||e.name}}h.styles=(0,r.iv)(c||(c=d`
    :host {
      --expansion-panel-summary-padding: 0 16px;
    }
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    ha-card {
      margin: 0 0 16px 0;
    }
    ha-card.disabled {
      pointer-events: none;
      color: var(--disabled-text-color);
    }
    .card-content {
      padding: 0px 16px 16px 16px;
    }
    .title {
      font-size: var(--ha-font-size-l);
      padding-top: 16px;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 16px;
      padding-left: 16px;
      padding-right: 4px;
      padding-inline-start: 16px;
      padding-inline-end: 4px;
      white-space: nowrap;
    }
  `)),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],h.prototype,"hass",void 0),(0,o.__decorate)([(0,n.Cb)({attribute:!1})],h.prototype,"value",void 0),(0,o.__decorate)([(0,n.Cb)()],h.prototype,"label",void 0),(0,o.__decorate)([(0,n.Cb)()],h.prototype,"helper",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],h.prototype,"disabled",void 0),(0,o.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],h.prototype,"required",void 0),h=(0,o.__decorate)([(0,n.Mo)("ha-selector-selector")],h)}}]);
//# sourceMappingURL=6470.f3d0f84c678e32a5.js.map