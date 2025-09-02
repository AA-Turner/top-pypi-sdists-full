export const __webpack_ids__=["6734"];export const __webpack_modules__={96382:function(e,o,t){t.r(o),t.d(o,{HaBooleanSelector:()=>l});var a=t(73742),r=t(59048),d=t(7616),i=t(29740);t(74207),t(4820),t(42592);class l extends r.oi{render(){return r.dy`
      <ha-formfield alignEnd spaceBetween .label=${this.label}>
        <ha-switch
          .checked=${this.value??!0===this.placeholder}
          @change=${this._handleChange}
          .disabled=${this.disabled}
        ></ha-switch>
        <span slot="label">
          <p class="primary">${this.label}</p>
          ${this.helper?r.dy`<p class="secondary">${this.helper}</p>`:r.Ld}
        </span>
      </ha-formfield>
    `}_handleChange(e){const o=e.target.checked;this.value!==o&&(0,i.B)(this,"value-changed",{value:o})}constructor(...e){super(...e),this.value=!1,this.disabled=!1}}l.styles=r.iv`
    ha-formfield {
      display: flex;
      min-height: 56px;
      align-items: center;
      --mdc-typography-body2-font-size: 1em;
    }
    p {
      margin: 0;
    }
    .secondary {
      direction: var(--direction);
      padding-top: 4px;
      box-sizing: border-box;
      color: var(--secondary-text-color);
      font-size: 0.875rem;
      font-weight: var(
        --mdc-typography-body2-font-weight,
        var(--ha-font-weight-normal)
      );
    }
  `,(0,a.__decorate)([(0,d.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],l.prototype,"value",void 0),(0,a.__decorate)([(0,d.Cb)()],l.prototype,"placeholder",void 0),(0,a.__decorate)([(0,d.Cb)()],l.prototype,"label",void 0),(0,a.__decorate)([(0,d.Cb)()],l.prototype,"helper",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],l.prototype,"disabled",void 0),l=(0,a.__decorate)([(0,d.Mo)("ha-selector-boolean")],l)}};
//# sourceMappingURL=6734.9e97d0b992924e78.js.map