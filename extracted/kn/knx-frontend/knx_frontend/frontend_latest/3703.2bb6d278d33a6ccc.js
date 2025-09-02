export const __webpack_ids__=["3703"];export const __webpack_modules__={12960:function(e,t,a){a.r(t),a.d(t,{HaFormInteger:()=>l});var i=a(73742),s=a(59048),h=a(7616),d=a(29740);a(57275),a(86776),a(42592),a(38573);class l extends s.oi{focus(){this._input&&this._input.focus()}render(){return void 0!==this.schema.valueMin&&void 0!==this.schema.valueMax&&this.schema.valueMax-this.schema.valueMin<256?s.dy`
        <div>
          ${this.label}
          <div class="flex">
            ${this.schema.required?"":s.dy`
                  <ha-checkbox
                    @change=${this._handleCheckboxChange}
                    .checked=${void 0!==this.data}
                    .disabled=${this.disabled}
                  ></ha-checkbox>
                `}
            <ha-slider
              labeled
              .value=${this._value}
              .min=${this.schema.valueMin}
              .max=${this.schema.valueMax}
              .disabled=${this.disabled||void 0===this.data&&!this.schema.required}
              @change=${this._valueChanged}
            ></ha-slider>
          </div>
          ${this.helper?s.dy`<ha-input-helper-text .disabled=${this.disabled}
                >${this.helper}</ha-input-helper-text
              >`:""}
        </div>
      `:s.dy`
      <ha-textfield
        type="number"
        inputMode="numeric"
        .label=${this.label}
        .helper=${this.helper}
        helperPersistent
        .value=${void 0!==this.data?this.data:""}
        .disabled=${this.disabled}
        .required=${this.schema.required}
        .autoValidate=${this.schema.required}
        .suffix=${this.schema.description?.suffix}
        .validationMessage=${this.schema.required?this.localize?.("ui.common.error_required"):void 0}
        @input=${this._valueChanged}
      ></ha-textfield>
    `}updated(e){e.has("schema")&&this.toggleAttribute("own-margin",!("valueMin"in this.schema&&"valueMax"in this.schema||!this.schema.required))}get _value(){return void 0!==this.data?this.data:this.schema.required?void 0!==this.schema.description?.suggested_value&&null!==this.schema.description?.suggested_value||this.schema.default||this.schema.valueMin||0:this.schema.valueMin||0}_handleCheckboxChange(e){let t;if(e.target.checked){for(const a of[this._lastValue,this.schema.description?.suggested_value,this.schema.default,0])if(void 0!==a){t=a;break}}else this._lastValue=this.data;(0,d.B)(this,"value-changed",{value:t})}_valueChanged(e){const t=e.target,a=t.value;let i;if(""!==a&&(i=parseInt(String(a))),this.data!==i)(0,d.B)(this,"value-changed",{value:i});else{const e=void 0===i?"":String(i);t.value!==e&&(t.value=e)}}constructor(...e){super(...e),this.disabled=!1}}l.styles=s.iv`
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
  `,(0,i.__decorate)([(0,h.Cb)({attribute:!1})],l.prototype,"localize",void 0),(0,i.__decorate)([(0,h.Cb)({attribute:!1})],l.prototype,"schema",void 0),(0,i.__decorate)([(0,h.Cb)({attribute:!1})],l.prototype,"data",void 0),(0,i.__decorate)([(0,h.Cb)()],l.prototype,"label",void 0),(0,i.__decorate)([(0,h.Cb)()],l.prototype,"helper",void 0),(0,i.__decorate)([(0,h.Cb)({type:Boolean})],l.prototype,"disabled",void 0),(0,i.__decorate)([(0,h.IO)("ha-textfield ha-slider")],l.prototype,"_input",void 0),l=(0,i.__decorate)([(0,h.Mo)("ha-form-integer")],l)}};
//# sourceMappingURL=3703.2bb6d278d33a6ccc.js.map