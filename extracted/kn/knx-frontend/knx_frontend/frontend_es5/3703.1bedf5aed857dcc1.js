"use strict";(self.webpackChunkknx_frontend=self.webpackChunkknx_frontend||[]).push([["3703"],{12960:function(e,t,i){i.r(t),i.d(t,{HaFormInteger:function(){return v}});i(37908),i(84730),i(26847),i(70820),i(27530);var a=i(73742),s=i(59048),h=i(7616),d=i(29740);i(57275),i(86776),i(42592),i(38573);let l,r,o,u,n,c=e=>e;class v extends s.oi{focus(){this._input&&this._input.focus()}render(){var e,t;return void 0!==this.schema.valueMin&&void 0!==this.schema.valueMax&&this.schema.valueMax-this.schema.valueMin<256?(0,s.dy)(l||(l=c`
        <div>
          ${0}
          <div class="flex">
            ${0}
            <ha-slider
              labeled
              .value=${0}
              .min=${0}
              .max=${0}
              .disabled=${0}
              @change=${0}
            ></ha-slider>
          </div>
          ${0}
        </div>
      `),this.label,this.schema.required?"":(0,s.dy)(r||(r=c`
                  <ha-checkbox
                    @change=${0}
                    .checked=${0}
                    .disabled=${0}
                  ></ha-checkbox>
                `),this._handleCheckboxChange,void 0!==this.data,this.disabled),this._value,this.schema.valueMin,this.schema.valueMax,this.disabled||void 0===this.data&&!this.schema.required,this._valueChanged,this.helper?(0,s.dy)(o||(o=c`<ha-input-helper-text .disabled=${0}
                >${0}</ha-input-helper-text
              >`),this.disabled,this.helper):""):(0,s.dy)(u||(u=c`
      <ha-textfield
        type="number"
        inputMode="numeric"
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
    `),this.label,this.helper,void 0!==this.data?this.data:"",this.disabled,this.schema.required,this.schema.required,null===(e=this.schema.description)||void 0===e?void 0:e.suffix,this.schema.required?null===(t=this.localize)||void 0===t?void 0:t.call(this,"ui.common.error_required"):void 0,this._valueChanged)}updated(e){e.has("schema")&&this.toggleAttribute("own-margin",!("valueMin"in this.schema&&"valueMax"in this.schema||!this.schema.required))}get _value(){var e,t;return void 0!==this.data?this.data:this.schema.required?void 0!==(null===(e=this.schema.description)||void 0===e?void 0:e.suggested_value)&&null!==(null===(t=this.schema.description)||void 0===t?void 0:t.suggested_value)||this.schema.default||this.schema.valueMin||0:this.schema.valueMin||0}_handleCheckboxChange(e){let t;if(e.target.checked)for(const a of[this._lastValue,null===(i=this.schema.description)||void 0===i?void 0:i.suggested_value,this.schema.default,0]){var i;if(void 0!==a){t=a;break}}else this._lastValue=this.data;(0,d.B)(this,"value-changed",{value:t})}_valueChanged(e){const t=e.target,i=t.value;let a;if(""!==i&&(a=parseInt(String(i))),this.data!==a)(0,d.B)(this,"value-changed",{value:a});else{const e=void 0===a?"":String(a);t.value!==e&&(t.value=e)}}constructor(...e){super(...e),this.disabled=!1}}v.styles=(0,s.iv)(n||(n=c`
    :host([own-margin]) {
      margin-bottom: 5px;
    }
    .flex {
      display: flex;
    }
    ha-slider {
      flex: 1;
    }
    ha-textfield {
      display: block;
    }
  `)),(0,a.__decorate)([(0,h.Cb)({attribute:!1})],v.prototype,"localize",void 0),(0,a.__decorate)([(0,h.Cb)({attribute:!1})],v.prototype,"schema",void 0),(0,a.__decorate)([(0,h.Cb)({attribute:!1})],v.prototype,"data",void 0),(0,a.__decorate)([(0,h.Cb)()],v.prototype,"label",void 0),(0,a.__decorate)([(0,h.Cb)()],v.prototype,"helper",void 0),(0,a.__decorate)([(0,h.Cb)({type:Boolean})],v.prototype,"disabled",void 0),(0,a.__decorate)([(0,h.IO)("ha-textfield ha-slider")],v.prototype,"_input",void 0),v=(0,a.__decorate)([(0,h.Mo)("ha-form-integer")],v)}}]);
//# sourceMappingURL=3703.1bedf5aed857dcc1.js.map