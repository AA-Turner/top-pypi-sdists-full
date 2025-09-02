export const __webpack_ids__=["9672"];export const __webpack_modules__={13819:function(e,t,i){i.d(t,{y:()=>d});var a=i(28105),o=i(1066);const d=(0,a.Z)((e=>{if(e.time_format===o.zt.language||e.time_format===o.zt.system){const t=e.time_format===o.zt.language?e.language:void 0;return new Date("January 1, 2023 22:00:00").toLocaleString(t).includes("10")}return e.time_format===o.zt.am_pm}))},48399:function(e,t,i){var a=i(73742),o=i(59048),d=i(7616),l=i(25191),s=i(29740),r=i(41806);i(78645),i(42592),i(93795),i(29490),i(38573);class n extends o.oi{render(){return o.dy`
      ${this.label?o.dy`<label>${this.label}${this.required?" *":""}</label>`:o.Ld}
      <div class="time-input-wrap-wrap">
        <div class="time-input-wrap">
          ${this.enableDay?o.dy`
                <ha-textfield
                  id="day"
                  type="number"
                  inputmode="numeric"
                  .value=${this.days.toFixed()}
                  .label=${this.dayLabel}
                  name="days"
                  @change=${this._valueChanged}
                  @focusin=${this._onFocus}
                  no-spinner
                  .required=${this.required}
                  .autoValidate=${this.autoValidate}
                  min="0"
                  .disabled=${this.disabled}
                  suffix=":"
                  class="hasSuffix"
                >
                </ha-textfield>
              `:o.Ld}

          <ha-textfield
            id="hour"
            type="number"
            inputmode="numeric"
            .value=${this.hours.toFixed()}
            .label=${this.hourLabel}
            name="hours"
            @change=${this._valueChanged}
            @focusin=${this._onFocus}
            no-spinner
            .required=${this.required}
            .autoValidate=${this.autoValidate}
            maxlength="2"
            max=${(0,l.o)(this._hourMax)}
            min="0"
            .disabled=${this.disabled}
            suffix=":"
            class="hasSuffix"
          >
          </ha-textfield>
          <ha-textfield
            id="min"
            type="number"
            inputmode="numeric"
            .value=${this._formatValue(this.minutes)}
            .label=${this.minLabel}
            @change=${this._valueChanged}
            @focusin=${this._onFocus}
            name="minutes"
            no-spinner
            .required=${this.required}
            .autoValidate=${this.autoValidate}
            maxlength="2"
            max="59"
            min="0"
            .disabled=${this.disabled}
            .suffix=${this.enableSecond?":":""}
            class=${this.enableSecond?"has-suffix":""}
          >
          </ha-textfield>
          ${this.enableSecond?o.dy`<ha-textfield
                id="sec"
                type="number"
                inputmode="numeric"
                .value=${this._formatValue(this.seconds)}
                .label=${this.secLabel}
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                name="seconds"
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                maxlength="2"
                max="59"
                min="0"
                .disabled=${this.disabled}
                .suffix=${this.enableMillisecond?":":""}
                class=${this.enableMillisecond?"has-suffix":""}
              >
              </ha-textfield>`:o.Ld}
          ${this.enableMillisecond?o.dy`<ha-textfield
                id="millisec"
                type="number"
                .value=${this._formatValue(this.milliseconds,3)}
                .label=${this.millisecLabel}
                @change=${this._valueChanged}
                @focusin=${this._onFocus}
                name="milliseconds"
                no-spinner
                .required=${this.required}
                .autoValidate=${this.autoValidate}
                maxlength="3"
                max="999"
                min="0"
                .disabled=${this.disabled}
              >
              </ha-textfield>`:o.Ld}
          ${!this.clearable||this.required||this.disabled?o.Ld:o.dy`<ha-icon-button
                label="clear"
                @click=${this._clearValue}
                .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
              ></ha-icon-button>`}
        </div>

        ${24===this.format?o.Ld:o.dy`<ha-select
              .required=${this.required}
              .value=${this.amPm}
              .disabled=${this.disabled}
              name="amPm"
              naturalMenuWidth
              fixedMenuPosition
              @selected=${this._valueChanged}
              @closed=${r.U}
            >
              <ha-list-item value="AM">AM</ha-list-item>
              <ha-list-item value="PM">PM</ha-list-item>
            </ha-select>`}
      </div>
      ${this.helper?o.dy`<ha-input-helper-text .disabled=${this.disabled}
            >${this.helper}</ha-input-helper-text
          >`:o.Ld}
    `}_clearValue(){(0,s.B)(this,"value-changed")}_valueChanged(e){const t=e.currentTarget;this[t.name]="amPm"===t.name?t.value:Number(t.value);const i={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};this.enableDay&&(i.days=this.days),12===this.format&&(i.amPm=this.amPm),(0,s.B)(this,"value-changed",{value:i})}_onFocus(e){e.currentTarget.select()}_formatValue(e,t=2){return e.toString().padStart(t,"0")}get _hourMax(){if(!this.noHoursLimit)return 12===this.format?12:23}constructor(...e){super(...e),this.autoValidate=!1,this.required=!1,this.format=12,this.disabled=!1,this.days=0,this.hours=0,this.minutes=0,this.seconds=0,this.milliseconds=0,this.dayLabel="",this.hourLabel="",this.minLabel="",this.secLabel="",this.millisecLabel="",this.enableSecond=!1,this.enableMillisecond=!1,this.enableDay=!1,this.noHoursLimit=!1,this.amPm="AM"}}n.styles=o.iv`
    :host([clearable]) {
      position: relative;
    }
    .time-input-wrap-wrap {
      display: flex;
    }
    .time-input-wrap {
      display: flex;
      flex: var(--time-input-flex, unset);
      border-radius: var(--mdc-shape-small, 4px) var(--mdc-shape-small, 4px) 0 0;
      overflow: hidden;
      position: relative;
      direction: ltr;
      padding-right: 3px;
    }
    ha-textfield {
      width: 60px;
      flex-grow: 1;
      text-align: center;
      --mdc-shape-small: 0;
      --text-field-appearance: none;
      --text-field-padding: 0 4px;
      --text-field-suffix-padding-left: 2px;
      --text-field-suffix-padding-right: 0;
      --text-field-text-align: center;
    }
    ha-textfield.hasSuffix {
      --text-field-padding: 0 0 0 4px;
    }
    ha-textfield:first-child {
      --text-field-border-top-left-radius: var(--mdc-shape-medium);
    }
    ha-textfield:last-child {
      --text-field-border-top-right-radius: var(--mdc-shape-medium);
    }
    ha-select {
      --mdc-shape-small: 0;
      width: 85px;
    }
    :host([clearable]) .mdc-select__anchor {
      padding-inline-end: var(--select-selected-text-padding-end, 12px);
    }
    ha-icon-button {
      position: relative;
      --mdc-icon-button-size: 36px;
      --mdc-icon-size: 20px;
      color: var(--secondary-text-color);
      direction: var(--direction);
      display: flex;
      align-items: center;
      background-color: var(--mdc-text-field-fill-color, whitesmoke);
      border-bottom-style: solid;
      border-bottom-width: 1px;
    }
    label {
      -moz-osx-font-smoothing: var(--ha-moz-osx-font-smoothing);
      -webkit-font-smoothing: var(--ha-font-smoothing);
      font-family: var(
        --mdc-typography-body2-font-family,
        var(--mdc-typography-font-family, var(--ha-font-family-body))
      );
      font-size: var(--mdc-typography-body2-font-size, var(--ha-font-size-s));
      line-height: var(
        --mdc-typography-body2-line-height,
        var(--ha-line-height-condensed)
      );
      font-weight: var(
        --mdc-typography-body2-font-weight,
        var(--ha-font-weight-normal)
      );
      letter-spacing: var(
        --mdc-typography-body2-letter-spacing,
        0.0178571429em
      );
      text-decoration: var(--mdc-typography-body2-text-decoration, inherit);
      text-transform: var(--mdc-typography-body2-text-transform, inherit);
      color: var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));
      padding-left: 4px;
      padding-inline-start: 4px;
      padding-inline-end: initial;
    }
    ha-input-helper-text {
      padding-top: 8px;
      line-height: var(--ha-line-height-condensed);
    }
  `,(0,a.__decorate)([(0,d.Cb)()],n.prototype,"label",void 0),(0,a.__decorate)([(0,d.Cb)()],n.prototype,"helper",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:"auto-validate",type:Boolean})],n.prototype,"autoValidate",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],n.prototype,"required",void 0),(0,a.__decorate)([(0,d.Cb)({type:Number})],n.prototype,"format",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],n.prototype,"disabled",void 0),(0,a.__decorate)([(0,d.Cb)({type:Number})],n.prototype,"days",void 0),(0,a.__decorate)([(0,d.Cb)({type:Number})],n.prototype,"hours",void 0),(0,a.__decorate)([(0,d.Cb)({type:Number})],n.prototype,"minutes",void 0),(0,a.__decorate)([(0,d.Cb)({type:Number})],n.prototype,"seconds",void 0),(0,a.__decorate)([(0,d.Cb)({type:Number})],n.prototype,"milliseconds",void 0),(0,a.__decorate)([(0,d.Cb)({type:String,attribute:"day-label"})],n.prototype,"dayLabel",void 0),(0,a.__decorate)([(0,d.Cb)({type:String,attribute:"hour-label"})],n.prototype,"hourLabel",void 0),(0,a.__decorate)([(0,d.Cb)({type:String,attribute:"min-label"})],n.prototype,"minLabel",void 0),(0,a.__decorate)([(0,d.Cb)({type:String,attribute:"sec-label"})],n.prototype,"secLabel",void 0),(0,a.__decorate)([(0,d.Cb)({type:String,attribute:"ms-label"})],n.prototype,"millisecLabel",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:"enable-second",type:Boolean})],n.prototype,"enableSecond",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:"enable-millisecond",type:Boolean})],n.prototype,"enableMillisecond",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:"enable-day",type:Boolean})],n.prototype,"enableDay",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:"no-hours-limit",type:Boolean})],n.prototype,"noHoursLimit",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:!1})],n.prototype,"amPm",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean,reflect:!0})],n.prototype,"clearable",void 0),n=(0,a.__decorate)([(0,d.Mo)("ha-base-time-input")],n)},8633:function(e,t,i){i.r(t),i.d(t,{HaTimeSelector:()=>l});var a=i(73742),o=i(59048),d=i(7616);i(28628);class l extends o.oi{render(){return o.dy`
      <ha-time-input
        .value=${"string"==typeof this.value?this.value:void 0}
        .locale=${this.hass.locale}
        .disabled=${this.disabled}
        .required=${this.required}
        clearable
        .helper=${this.helper}
        .label=${this.label}
        .enableSecond=${!this.selector.time?.no_second}
      ></ha-time-input>
    `}constructor(...e){super(...e),this.disabled=!1,this.required=!1}}(0,a.__decorate)([(0,d.Cb)({attribute:!1})],l.prototype,"hass",void 0),(0,a.__decorate)([(0,d.Cb)({attribute:!1})],l.prototype,"selector",void 0),(0,a.__decorate)([(0,d.Cb)()],l.prototype,"value",void 0),(0,a.__decorate)([(0,d.Cb)()],l.prototype,"label",void 0),(0,a.__decorate)([(0,d.Cb)()],l.prototype,"helper",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],l.prototype,"disabled",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],l.prototype,"required",void 0),l=(0,a.__decorate)([(0,d.Mo)("ha-selector-time")],l)},28628:function(e,t,i){var a=i(73742),o=i(59048),d=i(7616),l=i(13819),s=i(29740);i(48399);class r extends o.oi{render(){const e=(0,l.y)(this.locale);let t=NaN,i=NaN,a=NaN,d=0;if(this.value){const o=this.value?.split(":")||[];i=o[1]?Number(o[1]):0,a=o[2]?Number(o[2]):0,t=o[0]?Number(o[0]):0,d=t,d&&e&&d>12&&d<24&&(t=d-12),e&&0===d&&(t=12)}return o.dy`
      <ha-base-time-input
        .label=${this.label}
        .hours=${t}
        .minutes=${i}
        .seconds=${a}
        .format=${e?12:24}
        .amPm=${e&&d>=12?"PM":"AM"}
        .disabled=${this.disabled}
        @value-changed=${this._timeChanged}
        .enableSecond=${this.enableSecond}
        .required=${this.required}
        .clearable=${this.clearable&&void 0!==this.value}
        .helper=${this.helper}
        day-label="dd"
        hour-label="hh"
        min-label="mm"
        sec-label="ss"
        ms-label="ms"
      ></ha-base-time-input>
    `}_timeChanged(e){e.stopPropagation();const t=e.detail.value,i=(0,l.y)(this.locale);let a;if(!(void 0===t||isNaN(t.hours)&&isNaN(t.minutes)&&isNaN(t.seconds))){let e=t.hours||0;t&&i&&("PM"===t.amPm&&e<12&&(e+=12),"AM"===t.amPm&&12===e&&(e=0)),a=`${e.toString().padStart(2,"0")}:${t.minutes?t.minutes.toString().padStart(2,"0"):"00"}:${t.seconds?t.seconds.toString().padStart(2,"0"):"00"}`}a!==this.value&&(this.value=a,(0,s.B)(this,"change"),(0,s.B)(this,"value-changed",{value:a}))}constructor(...e){super(...e),this.disabled=!1,this.required=!1,this.enableSecond=!1}}(0,a.__decorate)([(0,d.Cb)({attribute:!1})],r.prototype,"locale",void 0),(0,a.__decorate)([(0,d.Cb)()],r.prototype,"value",void 0),(0,a.__decorate)([(0,d.Cb)()],r.prototype,"label",void 0),(0,a.__decorate)([(0,d.Cb)()],r.prototype,"helper",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],r.prototype,"disabled",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean})],r.prototype,"required",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean,attribute:"enable-second"})],r.prototype,"enableSecond",void 0),(0,a.__decorate)([(0,d.Cb)({type:Boolean,reflect:!0})],r.prototype,"clearable",void 0),r=(0,a.__decorate)([(0,d.Mo)("ha-time-input")],r)}};
//# sourceMappingURL=9672.5e00d991d2e45d88.js.map