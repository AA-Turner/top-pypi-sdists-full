export const __webpack_ids__=["297"];export const __webpack_modules__={48399:function(e,t,i){var a=i(73742),o=i(59048),s=i(7616),d=i(25191),l=i(29740),r=i(41806);i(78645),i(42592),i(93795),i(29490),i(38573);class n extends o.oi{render(){return o.dy`
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
            max=${(0,d.o)(this._hourMax)}
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
    `}_clearValue(){(0,l.B)(this,"value-changed")}_valueChanged(e){const t=e.currentTarget;this[t.name]="amPm"===t.name?t.value:Number(t.value);const i={hours:this.hours,minutes:this.minutes,seconds:this.seconds,milliseconds:this.milliseconds};this.enableDay&&(i.days=this.days),12===this.format&&(i.amPm=this.amPm),(0,l.B)(this,"value-changed",{value:i})}_onFocus(e){e.currentTarget.select()}_formatValue(e,t=2){return e.toString().padStart(t,"0")}get _hourMax(){if(!this.noHoursLimit)return 12===this.format?12:23}constructor(...e){super(...e),this.autoValidate=!1,this.required=!1,this.format=12,this.disabled=!1,this.days=0,this.hours=0,this.minutes=0,this.seconds=0,this.milliseconds=0,this.dayLabel="",this.hourLabel="",this.minLabel="",this.secLabel="",this.millisecLabel="",this.enableSecond=!1,this.enableMillisecond=!1,this.enableDay=!1,this.noHoursLimit=!1,this.amPm="AM"}}n.styles=o.iv`
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
  `,(0,a.__decorate)([(0,s.Cb)()],n.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],n.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"auto-validate",type:Boolean})],n.prototype,"autoValidate",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],n.prototype,"required",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],n.prototype,"format",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],n.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],n.prototype,"days",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],n.prototype,"hours",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],n.prototype,"minutes",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],n.prototype,"seconds",void 0),(0,a.__decorate)([(0,s.Cb)({type:Number})],n.prototype,"milliseconds",void 0),(0,a.__decorate)([(0,s.Cb)({type:String,attribute:"day-label"})],n.prototype,"dayLabel",void 0),(0,a.__decorate)([(0,s.Cb)({type:String,attribute:"hour-label"})],n.prototype,"hourLabel",void 0),(0,a.__decorate)([(0,s.Cb)({type:String,attribute:"min-label"})],n.prototype,"minLabel",void 0),(0,a.__decorate)([(0,s.Cb)({type:String,attribute:"sec-label"})],n.prototype,"secLabel",void 0),(0,a.__decorate)([(0,s.Cb)({type:String,attribute:"ms-label"})],n.prototype,"millisecLabel",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"enable-second",type:Boolean})],n.prototype,"enableSecond",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"enable-millisecond",type:Boolean})],n.prototype,"enableMillisecond",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"enable-day",type:Boolean})],n.prototype,"enableDay",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"no-hours-limit",type:Boolean})],n.prototype,"noHoursLimit",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],n.prototype,"amPm",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean,reflect:!0})],n.prototype,"clearable",void 0),n=(0,a.__decorate)([(0,s.Mo)("ha-base-time-input")],n)},90465:function(e,t,i){var a=i(73742),o=i(59048),s=i(7616),d=i(29740);i(48399);class l extends o.oi{render(){return o.dy`
      <ha-base-time-input
        .label=${this.label}
        .helper=${this.helper}
        .required=${this.required}
        .clearable=${!this.required&&void 0!==this.data}
        .autoValidate=${this.required}
        .disabled=${this.disabled}
        errorMessage="Required"
        enable-second
        .enableMillisecond=${this.enableMillisecond}
        .enableDay=${this.enableDay}
        format="24"
        .days=${this._days}
        .hours=${this._hours}
        .minutes=${this._minutes}
        .seconds=${this._seconds}
        .milliseconds=${this._milliseconds}
        @value-changed=${this._durationChanged}
        no-hours-limit
        day-label="dd"
        hour-label="hh"
        min-label="mm"
        sec-label="ss"
        ms-label="ms"
      ></ha-base-time-input>
    `}get _days(){return this.data?.days?Number(this.data.days):this.required||this.data?0:NaN}get _hours(){return this.data?.hours?Number(this.data.hours):this.required||this.data?0:NaN}get _minutes(){return this.data?.minutes?Number(this.data.minutes):this.required||this.data?0:NaN}get _seconds(){return this.data?.seconds?Number(this.data.seconds):this.required||this.data?0:NaN}get _milliseconds(){return this.data?.milliseconds?Number(this.data.milliseconds):this.required||this.data?0:NaN}_durationChanged(e){e.stopPropagation();const t=e.detail.value?{...e.detail.value}:void 0;t&&(t.hours||=0,t.minutes||=0,t.seconds||=0,"days"in t&&(t.days||=0),"milliseconds"in t&&(t.milliseconds||=0),this.enableMillisecond||t.milliseconds?t.milliseconds>999&&(t.seconds+=Math.floor(t.milliseconds/1e3),t.milliseconds%=1e3):delete t.milliseconds,t.seconds>59&&(t.minutes+=Math.floor(t.seconds/60),t.seconds%=60),t.minutes>59&&(t.hours+=Math.floor(t.minutes/60),t.minutes%=60),this.enableDay&&t.hours>24&&(t.days=(t.days??0)+Math.floor(t.hours/24),t.hours%=24)),(0,d.B)(this,"value-changed",{value:t})}constructor(...e){super(...e),this.required=!1,this.enableMillisecond=!1,this.enableDay=!1,this.disabled=!1}}(0,a.__decorate)([(0,s.Cb)({attribute:!1})],l.prototype,"data",void 0),(0,a.__decorate)([(0,s.Cb)()],l.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],l.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],l.prototype,"required",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"enable-millisecond",type:Boolean})],l.prototype,"enableMillisecond",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:"enable-day",type:Boolean})],l.prototype,"enableDay",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],l.prototype,"disabled",void 0),l=(0,a.__decorate)([(0,s.Mo)("ha-duration-input")],l)},30093:function(e,t,i){i.r(t),i.d(t,{HaTimeDuration:()=>d});var a=i(73742),o=i(59048),s=i(7616);i(90465);class d extends o.oi{render(){return o.dy`
      <ha-duration-input
        .label=${this.label}
        .helper=${this.helper}
        .data=${this.value}
        .disabled=${this.disabled}
        .required=${this.required}
        .enableDay=${this.selector.duration?.enable_day}
        .enableMillisecond=${this.selector.duration?.enable_millisecond}
      ></ha-duration-input>
    `}constructor(...e){super(...e),this.disabled=!1,this.required=!0}}(0,a.__decorate)([(0,s.Cb)({attribute:!1})],d.prototype,"hass",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],d.prototype,"selector",void 0),(0,a.__decorate)([(0,s.Cb)({attribute:!1})],d.prototype,"value",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"label",void 0),(0,a.__decorate)([(0,s.Cb)()],d.prototype,"helper",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],d.prototype,"disabled",void 0),(0,a.__decorate)([(0,s.Cb)({type:Boolean})],d.prototype,"required",void 0),d=(0,a.__decorate)([(0,s.Mo)("ha-selector-duration")],d)}};
//# sourceMappingURL=297.26eeb7392ec8a699.js.map