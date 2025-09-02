"use strict";(self.webpackChunkinsteon_frontend_home_assistant=self.webpackChunkinsteon_frontend_home_assistant||[]).push([[4755],{34755:(e,t,a)=>{a.r(t),a.d(t,{HaSelectorSelector:()=>c});var o=a(73958),n=a(9644),l=a(36924),i=a(14516),s=a(18394);a(23860),a(39663);const r={number:{min:1,max:100}},d={action:[],area:[{name:"multiple",selector:{boolean:{}}}],attribute:[{name:"entity_id",selector:{entity:{}}}],boolean:[],color_temp:[{name:"unit",selector:{select:{options:["kelvin","mired"]}}},{name:"min",selector:{number:{mode:"box"}}},{name:"max",selector:{number:{mode:"box"}}}],condition:[],date:[],datetime:[],device:[{name:"multiple",selector:{boolean:{}}}],duration:[{name:"enable_day",selector:{boolean:{}}}],entity:[{name:"multiple",selector:{boolean:{}}}],icon:[],location:[],media:[],number:[{name:"min",selector:{number:{mode:"box"}}},{name:"max",selector:{number:{mode:"box"}}},{name:"step",selector:{number:{mode:"box"}}}],object:[],color_rgb:[],select:[{name:"options",selector:{object:{}}},{name:"multiple",selector:{boolean:{}}}],state:[{name:"entity_id",selector:{entity:{}}}],target:[],template:[],text:[{name:"multiple",selector:{boolean:{}}},{name:"multiline",selector:{boolean:{}}},{name:"prefix",selector:{text:{}}},{name:"suffix",selector:{text:{}}}],theme:[],time:[]};let c=(0,o.Z)([(0,l.Mo)("ha-selector-selector")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,l.Cb)({attribute:!1})],key:"value",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"label",value:void 0},{kind:"field",decorators:[(0,l.Cb)()],key:"helper",value:void 0},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"disabled",value(){return!1}},{kind:"field",decorators:[(0,l.Cb)({type:Boolean,reflect:!0})],key:"required",value(){return!0}},{kind:"field",key:"_yamlMode",value(){return!1}},{kind:"method",key:"shouldUpdate",value:function(e){return 1!==e.size||!e.has("hass")}},{kind:"field",key:"_schema",value(){return(0,i.Z)(((e,t)=>[{name:"type",selector:{select:{mode:"dropdown",required:!0,options:Object.keys(d).concat("manual").map((e=>({label:t(`ui.components.selectors.selector.types.${e}`)||e,value:e})))}}},..."manual"===e?[{name:"manual",selector:{object:{}}}]:[],...d[e]?d[e].length>1?[{name:"",type:"expandable",title:t("ui.components.selectors.selector.options"),schema:d[e]}]:d[e]:[]]))}},{kind:"method",key:"render",value:function(){let e,t;if(this._yamlMode)t="manual",e={type:t,manual:this.value};else{t=Object.keys(this.value)[0];const a=Object.values(this.value)[0];e={type:t,..."object"==typeof a?a:[]}}const a=this._schema(t,this.hass.localize);return n.dy`<ha-card>
      <div class="card-content">
        <p>${this.label?this.label:""}</p>
        <ha-form
          .hass=${this.hass}
          .data=${e}
          .schema=${a}
          .computeLabel=${this._computeLabelCallback}
          @value-changed=${this._valueChanged}
        ></ha-form></div
    ></ha-card>`}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value,a=t.type;if(!a||"object"!=typeof t||0===Object.keys(t).length)return;const o=Object.keys(this.value)[0];if("manual"===a&&!this._yamlMode)return this._yamlMode=!0,void this.requestUpdate();if("manual"===a&&void 0===t.manual)return;let n;"manual"!==a&&(this._yamlMode=!1),delete t.type,n="manual"===a?t.manual:a===o?{[a]:{...t.manual?t.manual[o]:t}}:{[a]:{...r[a]}},(0,s.B)(this,"value-changed",{value:n})}},{kind:"field",key:"_computeLabelCallback",value(){return e=>this.hass.localize(`ui.components.selectors.selector.${e.name}`)||e.name}},{kind:"get",static:!0,key:"styles",value:function(){return n.iv`
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
        font-size: 16px;
        padding-top: 16px;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 16px;
        padding-left: 16px;
        padding-right: 4px;
        white-space: nowrap;
      }
    `}}]}}),n.oi)}}]);
//# sourceMappingURL=213434cd.js.map