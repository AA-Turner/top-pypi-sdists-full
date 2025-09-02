"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["2369"],{94980:function(e,t,i){i.r(t),i.d(t,{HaFormFloat:function(){return n}});i(37908),i(84730),i(26847),i(15519),i(64455),i(26086),i(6202),i(27530);var a=i(73742),o=i(59048),r=i(7616),d=i(29740);i(38573);let s,l,h=e=>e;class n extends o.oi{focus(){this._input&&this._input.focus()}render(){var e,t;return(0,o.dy)(s||(s=h`
      <ha-textfield
        type="number"
        inputMode="decimal"
        step="any"
        .label=${0}
        .helper=${0}
        helperPersistent
        .value=${0}
        .disabled=${0}
        .required=${0}
        .autoValidate=${0}
        .suffix=${0}
        .validationMessage=${0}
        @input=${0}
      ></ha-textfield>
    `),this.label,this.helper,void 0!==this.data?this.data:"",this.disabled,this.schema.required,this.schema.required,null===(e=this.schema.description)||void 0===e?void 0:e.suffix,this.schema.required?null===(t=this.localize)||void 0===t?void 0:t.call(this,"ui.common.error_required"):void 0,this._valueChanged)}updated(e){e.has("schema")&&this.toggleAttribute("own-margin",!!this.schema.required)}_valueChanged(e){const t=e.target.value.replace(",",".");let i;t.endsWith(".")||"-"!==t&&(""!==t&&(i=parseFloat(t),isNaN(i)&&(i=void 0)),this.data!==i&&(0,d.B)(this,"value-changed",{value:i}))}constructor(...e){super(...e),this.disabled=!1}}n.styles=(0,o.iv)(l||(l=h`
    :host([own-margin]) {
      margin-bottom: 5px;
    }
    ha-textfield {
      display: block;
    }
  `)),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],n.prototype,"localize",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],n.prototype,"schema",void 0),(0,a.__decorate)([(0,r.Cb)({attribute:!1})],n.prototype,"data",void 0),(0,a.__decorate)([(0,r.Cb)()],n.prototype,"label",void 0),(0,a.__decorate)([(0,r.Cb)()],n.prototype,"helper",void 0),(0,a.__decorate)([(0,r.Cb)({type:Boolean})],n.prototype,"disabled",void 0),(0,a.__decorate)([(0,r.IO)("ha-textfield")],n.prototype,"_input",void 0),n=(0,a.__decorate)([(0,r.Mo)("ha-form-float")],n)}}]);
//# sourceMappingURL=2369.4847638c370fb8c5.js.map