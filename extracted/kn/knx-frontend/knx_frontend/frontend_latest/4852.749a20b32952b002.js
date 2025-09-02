export const __webpack_ids__=["4852"];export const __webpack_modules__={60751:function(e,o,t){t.r(o),t.d(o,{HaFormBoolean:()=>s});var a=t(73742),r=t(59048),d=t(7616),i=t(29740);t(86776),t(74207);class s extends r.oi{focus(){this._input&&this._input.focus()}render(){return r.dy`
      <ha-formfield .label=${this.label}>
        <ha-checkbox
          .checked=${this.data}
          .disabled=${this.disabled}
          @change=${this._valueChanged}
        ></ha-checkbox>
        <span slot="label">
          <p class="primary">${this.label}</p>
          ${this.helper?r.dy`<p class="secondary">${this.helper}</p>`:r.Ld}
        </span>
      </ha-formfield>
    `}_valueChanged(e){(0,i.B)(this,"value-changed",{value:e.target.checked})}constructor(...e){super(...e),this.disabled=!1}}s.styles=r.iv`
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
  `,(0,a.__decorate)([(0,d.Cb)({attribute:!1})],s.prototype,"schema",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:!1})],s.prototype,"data",void 0),(0,a.__decorate)([(0,d.Cb)()],s.prototype,"label",void 0),(0,a.__decorate)([(0,d.Cb)()],s.prototype,"helper",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],s.prototype,"disabled",void 0),(0,a.__decorate)([(0,d.IO)("ha-checkbox",!0)],s.prototype,"_input",void 0),s=(0,a.__decorate)([(0,d.Mo)("ha-form-boolean")],s)}};
//# sourceMappingURL=4852.749a20b32952b002.js.map